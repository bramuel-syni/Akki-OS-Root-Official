"""R-94 (G5-v5 Family B first sub-slice · Doc 5 Part A · A5.1..A5.6) pre-Commit-A.

Bumps `baseline_failures.json` `counts_at_baseline.passed` and
`invariants_enforced_when_baseline_guard_1.passed_floor` 5711 → 5725
(+14 measured across 14 new property/scanner/registry tests in
`test_g5v5_doc5_a5_1_to_a5_6.py`), appends the ratchet_history entry,
then regens `notes/ORCH_BOOT.md` ratchet block with the new
`baseline_failures.json` sha256 and syncs the POD audit mirror
`/app/frontend/public/audit/ORCH_BOOT.md` byte-identically.

`heads_last_sealed` unchanged this-turn (advances at Commit-C fixup per
R-6 boundary regen precedent). M16-W3 corrected order:
    1. baseline_failures.json bumped first
    2. ORCH_BOOT.md ratchet block regen'd next (reads new sha)
    3. POD audit mirror synced byte-identical
    4. Commit-A opens on programme/track-a
    5. Commit-B state master with all state banking
    6. Commit-C fixup with R-6 boundary regen

Delta components:
    +2 registry-shape tests (rule ID tuple · shared row metadata)
    +6 property tests (A5.1..A5.6 · one per SRR row 64..69 · verbatim rule text)
    +6 grep-negative scanner tests (A5.1, A5.2, A5.3, A5.4, A5.5, A5.6)
    = +14 monotonic-up per CCS2 both fields bumped together

Mirrors tools/r93_pre_commit_a_ratchet_and_orch_boot_regen.py precedent exactly.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE_JSON = (
    STATE_ROOT / "repos" / "Extraction-Akki" / "backend" / "tests"
    / "invariants" / "baseline_failures.json"
)

PRIOR_PASSED_FLOOR = 5711
NEW_PASSED_FLOOR = 5725
DELTA = 14
NEW_UTC = "2026-09-21T05:00:00Z"

RATCHET_HISTORY_ENTRY = {
    "at_utc": "20260921T050000Z",
    "commit": "PENDING-CP-G5V5-DOC5-A5-1-TO-A5-6-FIRST-SUB-SLICE-COMMIT-A",
    "cp": (
        "CP-G5V5-DOC5-A5-1-TO-A5-6 first sub-slice · WAVE R-94 · Family B · "
        "Doc 5 M10 Northena Part A · Ruling 5 · v5 SRR rows 64..69"
    ),
    "note": (
        "G5-v5 Family B first sub-slice · WAVE R-94 · Ruling 5 authority "
        "(v5 SRR sheet sha256 00072c58... · rows 64..69 = Doc 5 Part A "
        "A5.1..A5.6 · Promise #16 'Focus maintained under massive context'). "
        "Owner ruling this-session verbatim (2026-09-21T~03:53Z: 'GO — Family A "
        "first sub-slice HUNT-and-authoring, exactly per your posture plan ... "
        "Standing GO extends through the R-91 window: Family A → Family B "
        "(Doc 5 Northena) → DAP-1..38 → RBM + ROC, Tier A before Tier B per "
        "the owner's sequencing, sub-slice sizes at your discretion for clean "
        "seals, no per-slice check-ins needed (SO §6 governs).'). "
        "canon_ref = v5 SRR only (Ruling 5). rule text governs (Ruling 3 erratum "
        "extended source-column shape this-session). Rule text extracted verbatim "
        "from fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_"
        "Northena.docx sha256 f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657"
        "c0fe0c9ed7cdc. Adds net-new backend package services/canon_doc5_northena/ "
        "(__init__.py + northena_a5_vocabulary.py) registering Final[...] canon "
        "vocabulary for A5.1..A5.6 (SRR row 64..69 statement + source file:line + "
        "invariant Final[bool] flags derived from rule text) plus 6 pure-data-in "
        "grep-negative scanners: scan_for_northena_ml_import (A5.1 · 5 patterns · "
        "'No Northena module imports a machine-learning library or a learned "
        "component') + scan_for_score_based_admission_rationale (A5.2 · 5 "
        "patterns · 'Admitted because the model scored it highly enough is the "
        "unauditable outcome this standard exists to prevent') + scan_for_"
        "northena_governor_internals_or_inference (A5.3 · 5 patterns · 'Northena "
        "never reads that governor's internals and never performs inference "
        "itself') + scan_for_gate_inferential_path (A5.4 · 5 patterns · 'No "
        "inferential path exists in Gate') + scan_for_learned_stopping_or_extra_"
        "halt_owner (A5.5 · 5 patterns · 'There is no learned stopping') + scan_"
        "for_executor_owned_budget_ceiling (A5.6 · 5 patterns · 'enforced by the "
        "governor rather than by the executor that could be tempted to keep "
        "going'). Adds new test module backend/tests/invariants/test_g5v5_doc5_"
        "a5_1_to_a5_6.py with 14 tests: 2 registry-shape tests + 6 property tests "
        "(one per A5.1..A5.6 · SO §2.5 verbatim-docstring quoting rule text "
        "byte-verbatim) + 6 grep-negative scanner tests (clean-input-empty + each "
        "watched-pattern-hits invariant byte-verbatim). Sealed R-93 canon_doc1_"
        "chokepoint UNCHANGED · sealed M12 code UNCHANGED · sealed M12 tests "
        "UNCHANGED · services/security_function_policies/* UNCHANGED · "
        "services/content_registry/* UNCHANGED · additive-only per SO §3.8. "
        "Delta +14 measured (5711 → 5725 · monotonic-up per CCS2 both fields "
        "bumped together · no test flipped to fail). Ratchet floor advances "
        "5711 → 5725 monotonic-up. HUNT-first via python-docx extraction + "
        "openpyxl SRR sha-pin verification banked at phase0/spec_hunt_receipts/"
        "20260921T045000Z_g5v5_family_b_doc5_northena_hunt_data.json. "
        "R-93 SEALED at 36668e3/ee30ca98/de4f31bd (immediately-precedes · "
        "establishes Family A Doc 1 A5.1..A5.9 vocabulary + scanner + Final[...]-"
        "constants pattern this wave inherits). Prior seal chain R-85/R-86/R-87/"
        "R-88/R-89/R-90/R-91 Phase 1 unchanged. R-91 Phase 2 CEREMONY-IN-FLIGHT · "
        "APPLY 2026-09-23T03:23:15Z (banked at a30db4f7) · unaffected by this "
        "slice. G5-v5 subsequent slices (Family B Part B B5.1..B5.5 · Family C "
        "DAP-1..38 · Family D RBM+ROC · Tier B rows in each family) queued "
        "post-this-seal per owner sequencing. HF-HOLD SEC-2026-09-12-01 remains "
        "OPEN · R-24 remains UNLISTED · R-25 defaults tagged."
    ),
    "passed": NEW_PASSED_FLOOR,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

NEW_REGEN_REASON = (
    "r94-pre-commit-a-ratchet-only-regen-cp-g5v5-doc5-a5-1-to-a5-6-first-sub-"
    "slice-advancing-passed-floor-5711-to-5725-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-ruling-5-srr-rows-64-to-69-doc-5-"
    "m10-northena-part-a-a5-1-to-a5-6"
)


def bump_baseline() -> None:
    """Step 1: bump baseline_failures.json passed / passed_floor + append ratchet_history entry."""
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)

    assert d["counts_at_baseline"]["passed"] == PRIOR_PASSED_FLOOR, (
        f"Expected counts_at_baseline.passed={PRIOR_PASSED_FLOOR}, "
        f"got {d['counts_at_baseline']['passed']}"
    )
    assert d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] == PRIOR_PASSED_FLOOR, (
        f"Expected passed_floor={PRIOR_PASSED_FLOOR}, "
        f"got {d['invariants_enforced_when_baseline_guard_1']['passed_floor']}"
    )

    # CCS2: both counters bump together
    d["counts_at_baseline"]["passed"] = NEW_PASSED_FLOOR
    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_PASSED_FLOOR
    d["ratchet_history"].append(RATCHET_HISTORY_ENTRY)
    d["recorded_at_utc"] = NEW_UTC.replace("-", "").replace(":", "")

    with BASELINE_JSON.open("w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def regen_orch_boot() -> None:
    """Step 2: regen ORCH_BOOT.md with new baseline sha + POD audit mirror sync."""
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    sha = hashlib.sha256(BASELINE_JSON.read_bytes()).hexdigest()
    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {NEW_REGEN_REASON}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  passed_floor: \d+$", f"  passed_floor: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  counts_at_baseline_passed: \d+$", f"  counts_at_baseline_passed: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  baseline_failures_sha256: [0-9a-f]+$", f"  baseline_failures_sha256: {sha}", text, count=1, flags=re.MULTILINE)
    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)
    return sha


if __name__ == "__main__":
    bump_baseline()
    sha = regen_orch_boot()
    print(f"baseline_failures.json sha256: {sha}")
    print(f"ratchet passed_floor: {NEW_PASSED_FLOOR}")
    print(f"delta: +{DELTA}")
