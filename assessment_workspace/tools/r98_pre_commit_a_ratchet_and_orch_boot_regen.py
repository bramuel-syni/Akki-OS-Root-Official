"""R-98 pre-Commit-A: ratchet bump 5782 → 5822 (+40) + ORCH_BOOT ratchet-only regen.

Wave R-98 · G5-v5 Family D · RBM 1..23 + ROC 1..11 (34 rules · 40 tests).

Follows M16-W3 corrected order: ratchet bump + ORCH_BOOT ratchet-only regen
BEFORE Commit-A. Deterministic · idempotent · zero remote · zero network ·
zero subprocess · zero git ops · pure local Path.read_text + Path.write_text
+ shutil.copyfile.
"""
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

PRIOR = 5782
NEW = 5822
DELTA = 40
NEW_UTC = "2026-09-21T06:50:00Z"

ENTRY = {
    "at_utc": "20260921T065000Z",
    "commit": "PENDING-CP-G5V5-FAMILY-D-RBM-ROC-COMMIT-A",
    "cp": (
        "CP-G5V5-FAMILY-D-RBM-ROC · WAVE R-98 · Family D · RBM-1..23 + ROC-1..11 · "
        "Rules Service · Ruling 5 · v5 SRR rows 277..309 + 483"
    ),
    "note": (
        "G5-v5 Family D · WAVE R-98 · Ruling 5 authority (v5 SRR sheet sha256 "
        "00072c58... · RBM Tier A rows 288..309 = RBM-1..22 · promise=rulebook_engine_spec_v1 · "
        "domain=Rules Service · RBM Tier B row 483 = RBM-23 · promise=watch_learning_v1 · "
        "domain=O2 Security & Intent · ROC Tier A rows 277..287 = ROC-1..11 · "
        "promise=rule_criteria_spec_v1 · domain=Rules Service · status PROPOSED "
        "landed under COMPLETION SPRINT directive 2026-09-21T~06:10Z step 2 "
        "'R-98 — G5 Family D: RBM + ROC (Rules Service)' + owner G5-v5 sequencing "
        "2026-09-21T~01:00Z at a30db4f7 + owner NO-EXPEDITE ruling 2026-09-21T~06:15Z "
        "verbatim: 'The countdown that cannot be shortened is the ceremony "
        "(RBM-8; SER C.5 I-4), and it's a Tier A check in the audit standard "
        "about to be applied to this repository — §6.6, \"a countdown cut short\" "
        "is what FAIL looks like'). Adds NEW backend package services/canon_rules_service/"
        "__init__.py + services/canon_rules_service/rbm_roc_vocabulary.py registering "
        "34 Final[...] {ID}_STATEMENT + {ID}_SRR_ROW pairs + RBM_RULE_IDS 23-tuple + "
        "RBM_TIER_A_RULE_IDS 22-tuple + RBM_TIER_B_RULE_IDS 1-tuple + ROC_RULE_IDS "
        "11-tuple + registry metadata dicts + RBM-8 ceremony-mechanic invariants "
        "(RBM_8_CEREMONY_WINDOW_IS_RIGID + RBM_8_NO_SHORTENING_PATH_IN_CODE + "
        "RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC='2026-09-23T03:23:15Z' + "
        "RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT) + scan_for_ceremony_shortening_path "
        "5-pattern grep-negative scanner (shorten_ceremony_countdown/"
        "expedite_ceremony_apply/waive_ceremony_countdown/bypass_ceremony_horizon/"
        "fast_forward_ceremony) enforcing owner directive 2026-09-21T~06:35Z: "
        "'when you author RBM-8, its invariant should reflect exactly that: "
        "ceremony windows are rigid, no shortening path exists in code, and "
        "the R-91 window you are currently honoring is the live evidence "
        "receipt.'). Adds NEW test module tests/invariants/test_g5v5_family_d_"
        "rbm_roc.py with 40 tests: 4 registry-shape + 22 RBM Tier A property "
        "(RBM-1..22) + 1 RBM Tier B property (RBM-23) + 11 ROC property (ROC-"
        "1..11) + 1 extended RBM-8 ceremony-mechanic invariant + 2 RBM-8 "
        "grep-negative scanner tests (clean-input-empty + each-pattern-hits). "
        "SO §2.5 verbatim-docstring. SCOPE FROZEN SO §6.4 NOTHING-BEYOND. "
        "zero implementation module edit outside this-wave. Sealed R-97 "
        "canon_dap_lifecycle.dap_tier_b_vocabulary + R-96 dap_tier_a_vocabulary "
        "+ R-95 canon_doc5_northena.northena_b5_ledger + R-94 northena_a5_"
        "vocabulary + R-93 canon_doc1_chokepoint + R-92 security_function_"
        "policies + R-88..R-90 content_registry all continue verbatim GREEN · "
        "additive-only per SO §3.8. Delta +40 targeted (5782 → 5822 · "
        "monotonic-up per CCS2 both fields bumped together · no test flipped "
        "to fail). CCS2 measured-not-targeted correction applied pre-double-"
        "sweep if a different delta is measured. RBM-8 is the ceremony "
        "mechanic governing R-91's frozen horizon 2026-09-23T03:23:15Z · "
        "current UTC 2026-09-21T~06:50Z < horizon (~44.6h out) · R-91 stays "
        "PARKED · R-98 seal completes cleanly inside window with zero "
        "ceremony-apply operations opened."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "r98-pre-commit-a-ratchet-only-regen-cp-g5v5-family-d-rbm-roc-"
    "advancing-passed-floor-5782-to-5822-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-ruling-5-srr-rows-277-to-309-"
    "plus-483-rbm-1-to-22-tier-a-rulebook-engine-spec-v1-rbm-23-tier-b-"
    "watch-learning-v1-roc-1-to-11-tier-a-rule-criteria-spec-v1-plus-rbm-8-"
    "ceremony-mechanic-invariants-per-owner-no-expedite-and-this-session-"
    "ceremony-window-rigid-directive-completion-sprint-step-2-of-6"
)


def bump_baseline() -> None:
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    assert d["counts_at_baseline"]["passed"] == PRIOR, f"Prior mismatch: expected {PRIOR}, got {d['counts_at_baseline']['passed']}"
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
