"""End-to-end backend tests for Code Guardian (BYOK iteration).

Covers: health, content catalog, auth enforcement, usage snapshot, BYOK
free-tier behavior (402 on missing key, quota counters NOT incremented),
quota gating (day_pass + monthly), quiz lifecycle, chat, Stripe checkout.
"""
import pytest
from tests.conftest import BASE_URL, auth_headers


# ---------- health ----------
class TestHealth:
    def test_root_health(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"


# ---------- content catalog ----------
class TestContent:
    def test_list_topics(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/content/topics")
        assert r.status_code == 200
        topics = r.json().get("topics", [])
        assert len(topics) == 8

    def test_topic_detail_requires_auth(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/content/topic/intro-ai")
        assert r.status_code == 401


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
        r = api_client.request(method, f"{BASE_URL}{path}", json=payload)
        assert r.status_code == 401


# ---------- usage/me with seeded session ----------
class TestUsageMe:
    def test_usage_me_day_pass_caps(self, api_client, seed_user):
        u = seed_user("day_pass")
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        body = r.json()
        assert body["tier"] == "day_pass"
        assert body["daily_prompts_cap"] == 6
        assert body["daily_tokens_cap"] == 450000
        assert body["blocked"] is False

    def test_usage_me_free_unblocked_byok(self, api_client, seed_user):
        """BYOK regression: free tier must now be unblocked (was blocked=true before)."""
        u = seed_user("free")
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        body = r.json()
        assert body["tier"] == "free"
        assert body["blocked"] is False, f"Free tier must NOT be blocked under BYOK. Got body={body}"


# ---------- BYOK free-tier behavior ----------
class TestByokFreeTier:
    def test_chat_free_no_byok_returns_402(self, api_client, seed_user, db):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "hello"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 402, f"expected 402 got {r.status_code} body={r.text}"
        body = r.json()
        assert body.get("error") == "byok_required"
        assert "key" in body.get("message", "").lower()
        # Verify quota counters NOT incremented
        daily = db.daily_usage.find_one({"user_id": u["user_id"]})
        assert daily is None or daily.get("prompts", 0) == 0, "BYOK 402 must NOT touch daily_usage"

    def test_quiz_free_no_byok_returns_402(self, api_client, seed_user, db):
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/quiz/generate",
            json={"topic_id": "intro-ai"},
            headers=auth_headers(u["token"]),
        )
        assert r.status_code == 402
        body = r.json()
        assert body.get("error") == "byok_required"
        daily = db.daily_usage.find_one({"user_id": u["user_id"]})
        assert daily is None or daily.get("prompts", 0) == 0

    def test_chat_free_with_invalid_byok_does_not_touch_quota(
        self, api_client, seed_user, db
    ):
        """Invalid Gemini key → upstream LLM fails → 4xx/5xx, but platform
        quota counters MUST remain 0 (BYOK never charges platform)."""
        u = seed_user("free")
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "hello", "byok_key": "AIza_invalid_test_key"},
            headers=auth_headers(u["token"]),
            timeout=60,
        )
        # Either upstream error code or 200 — what matters is no quota
        assert r.status_code >= 400, (
            f"invalid BYOK key should cause an upstream failure, got {r.status_code}: {r.text[:300]}"
        )
        daily = db.daily_usage.find_one({"user_id": u["user_id"]})
        assert daily is None or daily.get("prompts", 0) == 0, (
            f"BYOK invalid-key path must NOT increment platform quota. daily_usage={daily}"
        )
        monthly = db.monthly_usage.find_one({"account_id": u["account_id"]})
        assert monthly is None or monthly.get("tokens", 0) == 0


# ---------- paid tier quota regression ----------
class TestQuotaEnforcement:
    def test_day_pass_at_prompt_cap_blocks(self, api_client, seed_user):
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

    def test_day_pass_expired_downgrades_to_free_unblocked(self, api_client, seed_user):
        u = seed_user("day_pass", day_pass_expired=True)
        r = api_client.get(f"{BASE_URL}/api/usage/me", headers=auth_headers(u["token"]))
        assert r.status_code == 200
        assert r.json()["tier"] == "free"
        # BYOK regression: expired day_pass → free → blocked=False now
        assert r.json()["blocked"] is False


# ---------- LLM-backed paid flows (real Gemini calls) ----------
@pytest.mark.timeout(180)
class TestPaidLLMFlows:
    def test_day_pass_chat_increments_quota(self, api_client, seed_user, db):
        u = seed_user("day_pass")
        r = api_client.post(
            f"{BASE_URL}/api/ai/chat",
            json={"message": "In one sentence: what is supervised learning?"},
            headers=auth_headers(u["token"]),
            timeout=90,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert isinstance(body.get("reply"), str) and len(body["reply"]) > 0
        assert body.get("tokens_charged", 0) > 0
        assert body.get("byok") is False
        # Quota MUST have incremented by exactly 1 prompt for day_pass paid call
        daily = db.daily_usage.find_one({"user_id": u["user_id"]})
        assert daily is not None
        assert daily.get("prompts", 0) == 1
        assert daily.get("tokens", 0) > 0


# ---------- Stripe checkout (verify URL only) ----------
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
