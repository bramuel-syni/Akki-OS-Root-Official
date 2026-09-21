"""R-96 pre-Commit-A: ratchet bump 5738 → 5771 (+33) + ORCH_BOOT ratchet-only regen."""
from __future__ import annotations
import hashlib, json, re, shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE_JSON = (
    STATE_ROOT / "repos" / "Extraction-Akki" / "backend" / "tests"
    / "invariants" / "baseline_failures.json"
)

PRIOR = 5738
NEW = 5771
DELTA = 33
NEW_UTC = "2026-09-21T06:20:00Z"

ENTRY = {
    "at_utc": "20260921T062000Z",
    "commit": "PENDING-CP-G5V5-DAP-TIER-A-1-30-FIRST-SUB-SLICE-COMMIT-A",
    "cp": "CP-G5V5-DAP-TIER-A-1-30 first sub-slice · WAVE R-96 · Family C · DAP-1..DAP-30 Tier A base admission-and-metering · Ruling 5 · v5 SRR rows 315..344",
    "note": (
        "G5-v5 Family C first sub-slice · WAVE R-96 · Ruling 5 authority (v5 SRR sheet "
        "sha256 00072c58... · rows 315..344 = DAP-1..DAP-30 · promise=dap_backend_spec_v1 · "
        "Tier A base admission-and-metering · status PROPOSED landed under owner G5-v5 "
        "sequencing directive 2026-09-21T~01:00Z at a30db4f7 + COMPLETION SPRINT directive "
        "2026-09-21T~06:10Z: 'R-96+ — G5 Family C: DAP-1..38 rows, Tier A first, sub-slices "
        "at your discretion (in flight — continue).'). SRR row shape: rule_id + statement "
        "(byte-verbatim) + srr_row + shared metadata (objective/promise_source/status/domain/"
        "relationship). Adds NEW backend package services/canon_dap_lifecycle/__init__.py + "
        "services/canon_dap_lifecycle/dap_tier_a_vocabulary.py registering 30 Final[...] "
        "DAP_N_STATEMENT + DAP_N_SRR_ROW pairs + DAP_TIER_A_RULE_IDS 30-tuple + "
        "DAP_TIER_A_RULE_COUNT=30 + DAP_TIER_A_SRR_ROW_START=315 + "
        "DAP_TIER_A_SRR_ROW_END=344 + DAP_TIER_A_ROW_SHARED_METADATA 5-key dict. Adds "
        "NEW test module tests/invariants/test_g5v5_dap_tier_a_1_to_30.py with 33 tests: "
        "3 registry-shape/metadata + 30 property tests (one per DAP-1..DAP-30 · SO §2.5 "
        "verbatim-docstring quoting SRR statement byte-verbatim). SCOPE FROZEN SO §6.4 "
        "NOTHING-BEYOND. zero implementation module edit outside this-wave. Sealed R-95 "
        "canon_doc5_northena.northena_b5_ledger + R-94 northena_a5_vocabulary + R-93 "
        "canon_doc1_chokepoint + R-92 security_function_policies + R-88..R-90 "
        "content_registry all continue verbatim GREEN · additive-only per SO §3.8. "
        "Delta +33 targeted (5738 → 5771 · monotonic-up per CCS2 both fields bumped "
        "together · no test flipped to fail). CCS2 measured-not-targeted correction "
        "applied pre-double-sweep if a different delta is measured."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "r96-pre-commit-a-ratchet-only-regen-cp-g5v5-dap-tier-a-1-30-first-sub-"
    "slice-advancing-passed-floor-5738-to-5771-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-ruling-5-srr-rows-315-to-344-"
    "dap-1-to-dap-30-tier-a-base-admission-and-metering"
)


def bump_baseline() -> None:
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    assert d["counts_at_baseline"]["passed"] == PRIOR
    assert d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] == PRIOR
    d["counts_at_baseline"]["passed"] = NEW
    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW
    d["ratchet_history"].append(ENTRY)
    d["recorded_at_utc"] = NEW_UTC.replace("-", "").replace(":", "")
    with BASELINE_JSON.open("w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def regen_orch_boot() -> str:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    sha = hashlib.sha256(BASELINE_JSON.read_bytes()).hexdigest()
    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {REGEN_REASON}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  passed_floor: \d+$", f"  passed_floor: {NEW}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  counts_at_baseline_passed: \d+$", f"  counts_at_baseline_passed: {NEW}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  baseline_failures_sha256: [0-9a-f]+$", f"  baseline_failures_sha256: {sha}", text, count=1, flags=re.MULTILINE)
    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)
    return sha


if __name__ == "__main__":
    bump_baseline()
    sha = regen_orch_boot()
    print(f"baseline_failures.json sha256: {sha}")
    print(f"ratchet passed_floor: {NEW}")
    print(f"delta: +{DELTA}")
