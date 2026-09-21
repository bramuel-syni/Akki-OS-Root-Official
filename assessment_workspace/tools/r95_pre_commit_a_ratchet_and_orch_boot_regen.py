"""R-95 (G5-v5 Family B second sub-slice · Doc 5 Part B · B5.1..B5.5) pre-Commit-A.

Bumps `baseline_failures.json` `counts_at_baseline.passed` and
`invariants_enforced_when_baseline_guard_1.passed_floor` 5727 → 5738
(+11 targeted across 11 new property/scanner/registry tests in
`test_g5v5_doc5_b5_1_to_b5_5.py`), appends the ratchet_history entry,
then regens `notes/ORCH_BOOT.md` ratchet block with the new
`baseline_failures.json` sha256 and syncs the POD audit mirror
`/app/frontend/public/audit/ORCH_BOOT.md` byte-identically.

If a subsequent BASELINE_GUARD=1 sweep measures a delta different from
targeted +11 (e.g. spontaneous fail→pass transitions from the R-91
wrapped baseline set), a CCS2 measured-not-targeted correction script
lands the correction pre-double-sweep. Both counters (`counts.passed`
and `passed_floor`) bump together per CCS2 discipline.

`heads_last_sealed` unchanged this-turn (advances at Commit-C fixup per
R-6 boundary regen precedent). M16-W3 corrected order:
    1. baseline_failures.json bumped first
    2. ORCH_BOOT.md ratchet block regen'd next (reads new sha)
    3. POD audit mirror synced byte-identical
    4. Commit-A opens on programme/track-a
    5. Commit-B state master with all state banking
    6. Commit-C fixup with R-6 boundary regen

Delta components (targeted +11):
    +2 registry-shape tests (rule ID tuple · shared row metadata)
    +5 property tests (B5.1..B5.5 · one per SRR row 75..79 · verbatim rule text)
    +4 grep-negative scanner tests (B5.1, B5.2, B5.4, B5.5 · no scanner for B5.3)
    = +11 monotonic-up per CCS2 both fields bumped together

Mirrors tools/r94_pre_commit_a_ratchet_and_orch_boot_regen.py precedent exactly.
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

PRIOR_PASSED_FLOOR = 5727
NEW_PASSED_FLOOR = 5738
DELTA = 11
NEW_UTC = "2026-09-21T05:40:00Z"

RATCHET_HISTORY_ENTRY = {
    "at_utc": "20260921T054000Z",
    "commit": "PENDING-CP-G5V5-DOC5-B5-1-TO-B5-5-SECOND-SUB-SLICE-COMMIT-A",
    "cp": (
        "CP-G5V5-DOC5-B5-1-TO-B5-5 second sub-slice · WAVE R-95 · Family B · "
        "Doc 5 M10 Northena Part B · Ruling 5 · v5 SRR rows 75..79"
    ),
    "note": (
        "G5-v5 Family B second sub-slice · WAVE R-95 · Ruling 5 authority "
        "(v5 SRR sheet sha256 00072c58... · rows 75..79 = Doc 5 Part B "
        "B5.1..B5.5 · Promise #18 direction half 'Objective Preservation "
        "(Direction Half)'). Owner ruling this-session verbatim "
        "(2026-09-21T~05:20Z: 'GO — R-95 Family B Part B (B5.1..B5.5 · "
        "Promise #18 · Ledger) confirmed as the next wave, plan verbatim "
        "as you stated it. ... Standing GO continues through the G5 family "
        "queue per SO §6 — seal reports at boundaries, no per-slice "
        "check-ins needed. Proceed.'). canon_ref = v5 SRR only (Ruling 5). "
        "rule text governs (Ruling 3 erratum extended source-column shape). "
        "Rule text extracted verbatim from fixtures/files_9_extracted/"
        "05_Direction_Scope_and_Focus_Part_1_Northena.docx sha256 "
        "f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc. "
        "Adds net-new backend module services/canon_doc5_northena/"
        "northena_b5_ledger.py registering Final[...] canon vocabulary for "
        "B5.1..B5.5 (SRR row 75..79 statement + source file:line + invariant "
        "Final[bool] flags derived from rule text) plus 4 pure-data-in "
        "grep-negative scanners: scan_for_live_admission_edit (B5.1 · 5 "
        "patterns · 'A changed intent is a new admission, never an edit of "
        "a live one') + scan_for_downstream_lawful_basis_filter (B5.2 · 5 "
        "patterns · 'Purpose limitation is an admission property, not a "
        "downstream filter') + scan_for_ledger_update_or_delete (B5.4 · 6 "
        "patterns · 'No update path and no delete path exists within the "
        "retention window' and 'Out-of-scope and refused items are recorded, "
        "never silently dropped') + scan_for_side_channel_typing_or_mutation "
        "(B5.5 · 5 patterns · 'Typing it would harden it into a mutation "
        "surface' and 'Unit and audit stay in separate envelopes with "
        "separate lifecycles, joined by identity rather than embedded'). "
        "B5.3 asserts a shape invariant (two admission paths · both write "
        "Ledger row · both freeze the same way) rather than negating a "
        "specific behavior; no scanner registered for it — property test "
        "carries the rule. Adds new test module backend/tests/invariants/"
        "test_g5v5_doc5_b5_1_to_b5_5.py with 11 tests: 2 registry-shape "
        "tests + 5 property tests (one per B5.1..B5.5 · SO §2.5 "
        "verbatim-docstring quoting rule text byte-verbatim) + 4 "
        "grep-negative scanner tests (clean-input-empty + each "
        "watched-pattern-hits invariant byte-verbatim). Sealed R-94 "
        "canon_doc5_northena.northena_a5_vocabulary + test_g5v5_doc5_"
        "a5_1_to_a5_6.py UNCHANGED · sealed __init__.py package marker "
        "already forward-cites Part B UNCHANGED · sealed R-93 "
        "canon_doc1_chokepoint UNCHANGED · sealed R-92 "
        "security_function_policies UNCHANGED · sealed R-88..R-90 "
        "content_registry UNCHANGED · additive-only per SO §3.8. "
        "Delta +11 targeted (5727 → 5738 · monotonic-up per CCS2 both "
        "fields bumped together · no test flipped to fail). CCS2 "
        "measured-not-targeted correction applied pre-double-sweep if a "
        "different delta is measured. Ratchet floor advances 5727 → 5738 "
        "monotonic-up (or higher if spontaneous fail→pass transitions "
        "measured). HUNT-first via banked HUNT data at "
        "phase0/spec_hunt_receipts/20260921T045000Z_g5v5_family_b_doc5_"
        "northena_hunt_data.json (already banked at R-94 · covers SRR "
        "rows 75-79 verbatim with docx paragraph indices · v5 workbook "
        "sha-pin 00072c58 verified · Doc 5 source .docx sha f280356e "
        "verified). R-94 SEALED at 1115a332/98963a11/Commit-C fixup "
        "(immediately-precedes · establishes Family B Doc 5 Part A "
        "A5.1..A5.6 vocabulary + scanner + Final[...]-constants pattern "
        "this wave inherits). Prior seal chain R-85/R-86/R-87/R-88/R-89/"
        "R-90/R-91 Phase 1/R-92/R-93 unchanged. R-91 Phase 2 CEREMONY-"
        "IN-FLIGHT · APPLY 2026-09-23T03:23:15Z (banked at a30db4f7) · "
        "unaffected by this slice (current UTC 2026-09-21T~05:40Z < "
        "horizon). G5-v5 subsequent slices (DAP-1..38 Family C · RBM+ROC "
        "Family D · Tier B rows in each family) queued post-this-seal per "
        "owner sequencing. HF-HOLD SEC-2026-09-12-01 remains OPEN · R-24 "
        "remains UNLISTED · R-25 defaults tagged."
    ),
    "passed": NEW_PASSED_FLOOR,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

NEW_REGEN_REASON = (
    "r95-pre-commit-a-ratchet-only-regen-cp-g5v5-doc5-b5-1-to-b5-5-second-sub-"
    "slice-advancing-passed-floor-5727-to-5738-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-ruling-5-srr-rows-75-to-79-doc-5-"
    "m10-northena-part-b-b5-1-to-b5-5"
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


def regen_orch_boot() -> str:
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
