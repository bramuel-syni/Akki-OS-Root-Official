"""R-93 (G5-v5 Family A first sub-slice · Doc 1 A5.1..A5.9) pre-Commit-A.

Bumps `baseline_failures.json` `counts_at_baseline.passed` and
`invariants_enforced_when_baseline_guard_1.passed_floor` 5695 → 5711
(+16 measured across the 16 new property/scanner/registry tests in
`test_g5v5_doc1_a5_1_to_a5_9.py`), appends the ratchet_history entry,
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
    +9 property tests (A5.1..A5.9 · one per SRR row R2..R10 · verbatim rule text)
    +5 grep-negative scanner tests (A5.1, A5.3, A5.5, A5.7, A5.9)
    = +16 monotonic-up per CCS2 both fields bumped together
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

PRIOR_PASSED_FLOOR = 5695
NEW_PASSED_FLOOR = 5711
DELTA = 16
NEW_UTC = "2026-09-21T03:50:00Z"

RATCHET_HISTORY_ENTRY = {
    "at_utc": "20260921T035000Z",
    "commit": "PENDING-CP-G5V5-DOC1-A5-1-TO-A5-9-FIRST-SUB-SLICE-COMMIT-A",
    "cp": (
        "CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · WAVE R-93 · Family A · "
        "Doc 1 M12 chokepoint · Ruling 5 · v5 SRR rows R2..R10"
    ),
    "note": (
        "G5-v5 Family A first sub-slice · WAVE R-93 · Ruling 5 authority "
        "(v5 SRR sheet sha256 00072c58... · rows R2..R10 = Doc 1 A5.1..A5.9). "
        "Owner ruling this-session verbatim (2026-09-21T~03:53Z: 'GO — Family A "
        "first sub-slice HUNT-and-authoring, exactly per your posture plan ...'). "
        "canon_ref = v5 SRR only (Ruling 5). rule text governs (Ruling 3 erratum "
        "extended source-column shape this-session). Rule text extracted verbatim "
        "from fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_"
        "Chokepoint.docx sha256 a33588298100c6224366623e64ac8632b48294649e57ad43cf"
        "67ee6730f97844 (source-doc block cleared at state commit afd0f3c7 · "
        "correction addendum this-session). "
        "Adds net-new backend package services/canon_doc1_chokepoint/ "
        "(__init__.py + chokepoint_vocabulary.py) registering Final[...] "
        "canon vocabulary for A5.1..A5.9 (SRR row R2..R10 statement + source "
        "file:line + invariant Final[bool] flags derived from rule text) plus "
        "5 pure-data-in grep-negative scanners: scan_for_non_chokepoint_model_"
        "invocation (A5.1 · 5 patterns · 'fails the build if any module other "
        "than the chokepoint function imports or invokes the model client') + "
        "scan_for_envelope_persistence (A5.3 · 5 patterns · 'never persisted "
        "to disk as a standing record, never shared between requests, and never "
        "available to any consumer after the call completes') + scan_for_outbound_"
        "network_outside_crossing (A5.5 · 5 patterns · 'No other module in the "
        "platform holds outbound network capability' + build gate) + scan_for_"
        "credential_at_receipt (A5.7 · 5 patterns · 'the credential used to reach "
        "the model is never logged or included') + scan_for_degraded_answer_on_"
        "grounding_failure (A5.9 · 5 patterns · 'refusal, not a weaker answer "
        "offered anyway'). A5.2/A5.4/A5.6/A5.8 rule texts assert invariants "
        "without negating a specific pattern · no scanner registered for those "
        "four per owner directive 'grep-negative bans where the rule text states "
        "them' (SFP-1..7 precedent). Adds new test module backend/tests/invariants/"
        "test_g5v5_doc1_a5_1_to_a5_9.py with 16 tests: 2 registry-shape tests + "
        "9 property tests (one per A5.1..A5.9 · SO §2.5 verbatim-docstring "
        "quoting rule text byte-verbatim) + 5 grep-negative scanner tests "
        "(clean-input-empty + each watched-pattern-hits invariant byte-verbatim). "
        "Sealed M12 code (services/chokepoint/*) UNCHANGED · sealed M12 tests "
        "UNCHANGED · services/security_function_policies/* UNCHANGED · "
        "services/content_registry/* UNCHANGED · additive-only per SO §3.8. "
        "Delta +16 measured (5695 → 5711 · monotonic-up per CCS2 both fields "
        "bumped together · no test flipped to fail). Ratchet floor advances "
        "5695 → 5711 monotonic-up. HUNT-first via python-docx extraction + "
        "openpyxl SRR sha-pin verification banked at phase0/spec_hunt_receipts/"
        "20260921T034500Z_g5v5_family_a_doc1_a5_1_to_a5_9_authoring_hunt_data.json. "
        "R-92 SEALED at ceaa24f/19030610/e8f9f168 (immediately-precedes · "
        "establishes SFP-1..7 vocabulary + scanner + Final[...]-constants "
        "pattern this wave inherits). Prior seal chain R-85/R-86/R-87/R-88/"
        "R-89/R-90/R-91 Phase 1 unchanged. R-91 Phase 2 CEREMONY-IN-FLIGHT · "
        "APPLY 2026-09-23T03:23:15Z (banked at a30db4f7) · unaffected by this "
        "slice. G5-v5 subsequent slices (Family B Doc 5 Northena / Family C "
        "DAP-1..38 / Family D RBM+ROC · Tier B rows in each family) queued "
        "post-this-seal per owner sequencing (2026-09-21T~01:00Z verbatim). "
        "R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (D+A ratification "
        "banked · not restated). HF-HOLD SEC-2026-09-12-01 remains OPEN · "
        "R-24 remains UNLISTED · R-25 defaults tagged."
    ),
    "passed": NEW_PASSED_FLOOR,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

NEW_REGEN_REASON = (
    "r93-pre-commit-a-ratchet-only-regen-cp-g5v5-doc1-a5-1-to-a5-9-first-sub-"
    "slice-advancing-passed-floor-5695-to-5711-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-ruling-5-srr-rows-r2-to-r10-doc-1-"
    "a5-1-to-a5-9-chokepoint-canon"
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
