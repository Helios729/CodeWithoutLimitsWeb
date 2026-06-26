"""
Code Without Limits — extended content loaders.

Loads two new author-provided JSONs (single source of truth):

  • income_modules.json   – the 18 Income & Asset modules (microenterprise
    project bank). Participants build a monetisable digital asset.
  • app_content.json      – everything outside the 18 income modules:
    curriculum overview, programme structure, workflow stages, languages,
    supplementary modules, core rule, references.

The JSON shapes are passed through as-is to the frontend — no paraphrasing.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "curriculum_data"


def _load_json(filename: str) -> dict:
    path = DATA_DIR / filename
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# Loaded once at import. Restart backend to pick up edits.
INCOME_DOC = _load_json("income_modules.json")
PROGRAMME_DOC = _load_json("app_content.json")

INCOME_MODULES = INCOME_DOC.get("modules", []) if isinstance(INCOME_DOC, dict) else []


def income_list_summary() -> dict:
    """Lightweight catalog for the Income Bank list screen."""
    items = []
    for m in INCOME_MODULES:
        items.append(
            {
                "id": m.get("id"),
                "slug": m.get("slug"),
                "title": m.get("title"),
                "role_label": m.get("role_label"),
                "asset": m.get("asset"),
                "languages": m.get("languages", []) or [],
                "ai_basics_count": len(m.get("ai_basics_learned") or []),
            }
        )
    return {
        "title": INCOME_DOC.get("title", "Income & Asset Module Bank"),
        "description": INCOME_DOC.get("description", ""),
        "source_document": INCOME_DOC.get("source_document", ""),
        "count": len(items),
        "modules": items,
    }


def income_module_detail(module_id: int) -> dict | None:
    for m in INCOME_MODULES:
        if str(m.get("id")) == str(module_id):
            return m
    return None


def programme_overview() -> dict:
    """Curated bundle of the most useful programme-level sections for the
    About / Programme screen. Returns empty dict if the JSON wasn't loaded."""
    if not isinstance(PROGRAMME_DOC, dict) or not PROGRAMME_DOC:
        return {}
    return {
        "title": PROGRAMME_DOC.get("title", "Code Without Limits"),
        "description": PROGRAMME_DOC.get("description", ""),
        "source_document": PROGRAMME_DOC.get("source_document", ""),
        "overview": PROGRAMME_DOC.get("overview", {}),
        "core_rule": PROGRAMME_DOC.get("core_rule", ""),
        "curriculum": PROGRAMME_DOC.get("curriculum", {}),
        "system_integration": PROGRAMME_DOC.get("system_integration", {}),
        "module_bank_intro": PROGRAMME_DOC.get("module_bank_intro", {}),
        "shared_energy_to_income_workflow": PROGRAMME_DOC.get(
            "shared_energy_to_income_workflow", {}
        ),
        "languages": PROGRAMME_DOC.get("languages", {}),
        "supplementary_modules": PROGRAMME_DOC.get("supplementary_modules", {}),
        "programme_structure": PROGRAMME_DOC.get("programme_structure", {}),
        "references": PROGRAMME_DOC.get("references", []) or [],
    }
