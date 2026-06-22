"""End-to-end backend tests for Code Guardian.

Covers: health, content catalog, auth enforcement, usage snapshot,
quota gating (day_pass + monthly + free), quiz lifecycle, chat,
Stripe checkout URL generation. Stripe key is LIVE — we DO NOT
complete purchases; only verify the endpoint returns a valid URL.
"""
import os
import pytest
from tests.conftest import BASE_URL, auth_headers


# ---------- health ----------
class TestHealth:
    def test_root_health(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"


# ---------- content catalog ----------
class TestContent:
    def test_list_topics(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/content/topics")
        assert r.status_code == 200
        topics = r.json().get("topics", [])
        assert len(topics) == 8, f"expected 8 topics, got {len(topics)}"
        for t in topics:
            assert "topic_id" in t and "title" in t
            assert "source_count" in t and t["source_count"] >= 1
            assert isinstance(t.get("institutions"), list) and len(t["institutions"]) >= 1

    def test_topic_detail_requires_auth(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/content/topic/intro-ai")
        assert r.status_code == 401

    def test_topic_detail_with_auth(self, api_client, seed_user):
        u = seed_user("day_pass")
        r = api_client.get(
            f"{BASE_URL}/api/content/topic/intro-ai",
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 200
        body = r.json()
        assert body["topic_id"] == "intro-ai"
        institutions = {s["institution"] for s in body["sources"]}
        # Allowlist topics include MIT/Stanford/Berkeley for intro-ai
        assert any("MIT" in i for i in institutions)


# ---------- auth gating ----------
class TestAuthGating:
    @pytest.mark.parametrize("path,method,payload", [
        ("/api/auth/me", "get", None),
        ("/api/usage/me", "get", None),
        ("/api/quiz/generate", "post", {"topic_id": "intro-ai"}),
        ("/api/ai/chat", "post", {"message": "hi"}),
        ("/api/billing/checkout", "post", {"plan": "day_pass"}),
    ])
    def test_protected_without_token(self, api_client, path, method, payload):
        url = f"{BASE_URL}{path}"
        r = api_client.request(method, url, json=payload)
        assert r.status_code == 401, f"{path} expected 401 got {r.status_code}"


# ---------- auth/me + usage/me with seeded session ----------
class TestAuthMe:
    def test_auth_me_returns_user(self, api_client, seed_user):
        u = seed_user("day_pass")
        r = api_client.get(f"{BASE_URL}/api/auth/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == u["user_id"]
        assert body["email"] == u["email"]
        assert body["account_id"] == u["account_id"]

    def test_usage_me_day_pass_caps(self, api_client, seed_user):
        u = seed_user("day_pass")
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        body = r.json()
        assert body["tier"] == "day_pass"
        assert body["daily_prompts_cap"] == 6
        assert body["daily_tokens_cap"] == 450000
        assert body["blocked"] is False

    def test_usage_me_free_blocked(self, api_client, seed_user):
        u = seed_user("free")
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        body = r.json()
        assert body["tier"] == "free"
        assert body["blocked"] is True


# ---------- quota enforcement (no LLM call required) ----------
class TestQuotaEnforcement:
    def test_free_tier_chat_blocked_with_upgrade_message(self, api_client, seed_user):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "hello"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 429
        body = r.json()
        assert body.get("error") == "quota_exceeded"
        assert "Day Pass" in body.get("message", "") or "Upgrade" in body.get("message", "")

    def test_day_pass_at_prompt_cap_blocks(self, api_client, seed_user):
        # Pre-fill 6 prompts so the next call must be blocked.
        u = seed_user("day_pass", daily_prompts=6, daily_tokens=10)
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "hi"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 429
        assert r.json().get("error") == "quota_exceeded"

    def test_day_pass_at_token_cap_blocks(self, api_client, seed_user):
        u = seed_user("day_pass", daily_prompts=1, daily_tokens=450000)
        r = api_client.post(
            f"{BASE_URL}/api/quiz/generate",
            json={"topic_id": "intro-ai"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 429

    def test_monthly_at_token_cap_blocks(self, api_client, seed_user):
        u = seed_user("monthly", monthly_tokens=1_000_000)
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "hi"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 429
        assert "monthly" in r.json().get("message", "").lower() or "1,000,000" in r.json().get("message", "")

    def test_day_pass_expired_downgrades_to_free(self, api_client, seed_user):
        u = seed_user("day_pass", day_pass_expired=True)
        # usage/me should now report tier=free + blocked
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        assert r.json()["tier"] == "free"
        assert r.json()["blocked"] is True


# ---------- LLM-backed flows (expensive — small slice) ----------
@pytest.mark.timeout(120)
class TestQuizAndChat:
    def test_quiz_generate_and_submit(self, api_client, seed_user, db):
        u = seed_user("day_pass")
        r = api_client.post(
            f"{BASE_URL}/api/quiz/generate",
            json={"topic_id": "intro-ai"},
            headers=auth_headers(u["token"]),
            timeout=120,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert "quiz_id" in body
        assert len(body["questions"]) == 10
        for q in body["questions"]:
            assert "question" in q and isinstance(q["question"], str)
            assert len(q["options"]) == 4
            assert q.get("source") is not None
            assert "url" in q["source"] and "institution" in q["source"]
        assert body.get("tokens_charged", 0) > 0

        # Submit answers
        answers = [0] * 10
        sub = api_client.post(
            f"{BASE_URL}/api/quiz/submit",
            json={"quiz_id": body["quiz_id"], "answers": answers},
            headers=auth_headers(u["token"]),
            timeout=30,
        )
        assert sub.status_code == 200
        sbody = sub.json()
        assert sbody["total"] == 10
        assert isinstance(sbody["score"], int)
        assert len(sbody["results"]) == 10
        for d in sbody["results"]:
            assert "correct_index" in d and "chosen_index" in d
            assert "is_correct" in d

    @pytest.mark.timeout(60)
    def test_ai_chat_returns_reply_and_tokens(self, api_client, seed_user):
        u = seed_user("day_pass")
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "In one sentence: what is supervised learning?"},
            headers=auth_headers(u["token"]),
            timeout=60,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert isinstance(body.get("reply"), str) and len(body["reply"]) > 0
        assert body.get("tokens_charged", 0) > 0


# ---------- Stripe checkout (verify URL only — DO NOT pay) ----------
class TestBillingCheckout:
    def test_day_pass_checkout_returns_stripe_url(self, api_client, seed_user):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/billing/checkout",
            json={"plan": "day_pass"},
            headers=auth_headers(u["token"]),
            timeout=30,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert "url" in body and body["url"].startswith("https://checkout.stripe.com")
        assert "session_id" in body and body["session_id"].startswith("cs_")

    def test_monthly_checkout_returns_stripe_url(self, api_client, seed_user):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/billing/checkout",
            json={"plan": "monthly"},
            headers=auth_headers(u["token"]),
            timeout=30,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["url"].startswith("https://checkout.stripe.com")
        assert body["session_id"].startswith("cs_")

    def test_unknown_plan_rejected(self, api_client, seed_user):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/billing/checkout",
            json={"plan": "yearly"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 400
