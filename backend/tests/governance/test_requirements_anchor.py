"""WP-00 guardrail: every work package cites sources that resolve on disk; owner-order sections are append-only."""
import hashlib
import json
import re
from pathlib import Path

import pytest

APP = Path("/app")
MEMORY = APP / "memory"
PLAN = MEMORY / "EXECUTION_PLAN_20261005.md"
PLAN_V2 = MEMORY / "BUILD_PLAN_V2_20261005.md"
LEDGER = MEMORY / "BUILD_LEDGER.md"
DIAGNOSIS = MEMORY / "SYSTEM_DIAGNOSIS_20261005.md"
OWNER_ORDERS = MEMORY / "M_ALPHA_OWNER_ORDERS.md"
HASHES = MEMORY / "owner_orders_section_hashes.json"
BACKEND = APP / "backend" / "vendored" / "extraction_akki" / "backend"
SOURCE_TEXT = APP / "assessment_workspace" / "notes" / "full_requirements_gap_20260926" / "source_text"
ROOTS = (APP, BACKEND, MEMORY, APP / "assessment_workspace" / "notes", APP / "assessment_workspace" / "notes" / "goal_delivery_20260928",
         SOURCE_TEXT, APP / "assessment_workspace" / "canon" / "drops" / "20260914_audio_plane_v1" / "extracted")
PATH_TOKEN = re.compile(r"`([^`]+)`")


def _resolve(token: str):
    token = token.split("::")[0].split(" (")[0].strip()
    if token.startswith(".../"):
        token = token[4:]
        if token.startswith("source_text/"):
            token = token[len("source_text/"):]
    if not re.search(r"\.(py|md|txt|json|yml)$|/$", token):
        return None  # not a path (clause id, phrase)
    token = token.rstrip("/")
    for root in ROOTS:
        candidate = root / token.lstrip("/") if not token.startswith("/app/") else Path(token)
        if candidate.exists():
            return candidate
    return None


def _work_packages(text: str):
    blocks = re.split(r"\n(?:### |\*\*)(WP-[0-9A-Z]+)", text)
    return {blocks[i]: blocks[i + 1] for i in range(1, len(blocks), 2)}


def _sections(text: str):
    parts = re.split(r"\n## (\d+)\. ", text)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def test_plan_and_diagnosis_exist_and_are_named_in_agents_anchor():
    anchor = (APP / "AGENTS.md").read_text()
    assert PLAN.exists() and PLAN_V2.exists() and LEDGER.exists() and DIAGNOSIS.exists()
    for name in (PLAN_V2.name, LEDGER.name, DIAGNOSIS.name):
        assert name in anchor, name


def _check_sources(plan_path, minimum):
    packages = _work_packages(plan_path.read_text())
    assert len(packages) >= minimum, sorted(packages)
    missing = {}
    for wp, body in packages.items():
        source_lines = [l for l in body.splitlines() if "Sources:" in l]
        assert source_lines, f"{plan_path.name}: {wp} has no Sources line"
        tokens = PATH_TOKEN.findall(" ".join(source_lines))
        paths = [t for t in tokens if re.search(r"\.(py|md|txt|json|yml)$|/$", t.split("::")[0].split(" (")[0].strip())]
        assert paths, f"{plan_path.name}: {wp} cites no file path"
        unresolved = [t for t in paths if _resolve(t) is None]
        if unresolved:
            missing[wp] = unresolved
    assert not missing, json.dumps({plan_path.name: missing}, indent=1)
    return packages


def test_every_work_package_has_resolving_sources():
    _check_sources(PLAN, 19)
    _check_sources(PLAN_V2, 25)


def test_ledger_is_append_only_shaped_and_names_known_work_packages():
    packages = set(_work_packages(PLAN_V2.read_text())) | {"WP-00", "PLAN"}
    lines = [l for l in LEDGER.read_text().splitlines() if re.match(r"^\d{4}-\d{2}-\d{2}T", l)]
    assert lines, "ledger has no entries"
    for line in lines:
        fields = [f.strip() for f in line.split(" · ")]
        assert len(fields) >= 7, line
        assert fields[1] in packages, fields[1]
        assert fields[2] in {"planned", "implementing", "ready_for_test", "verified_pass", "failed", "blocked", "decision_pending", "recorded"}, fields[2]
        assert fields[-1].startswith("next"), line
    stamps = [l.split(" · ")[0] for l in lines]
    assert stamps == sorted(stamps), "ledger entries must be appended in time order"


def test_owner_orders_sections_are_append_only():
    sections = _sections(OWNER_ORDERS.read_text())
    current = {str(k): hashlib.sha256(v.encode()).hexdigest() for k, v in sections.items()}
    if not HASHES.exists():
        pytest.fail("owner_orders_section_hashes.json missing — generate it once from the current frozen sections")
    frozen = json.loads(HASHES.read_text())
    changed = {k: v for k, v in frozen.items() if current.get(k) != v}
    assert not changed, f"frozen owner-order sections changed: {sorted(changed)}"
    assert set(frozen) <= set(current)


def test_diagnosis_lists_pending_decisions_and_root_causes():
    text = DIAGNOSIS.read_text()
    for marker in ("RC-1", "RC-9", "| D1 |", "| D7 |", "## PART C", "## PART E"):
        assert marker in text, marker
