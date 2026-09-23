#!/usr/bin/env python3
"""CP-CENSUS-TENANT-ADMISSION-CORRECTION · PHASE 4 (c-v) · baseline_failures.json bump.

Advances passed_floor 6194 -> 6206 (+12 canonical measured):
- 12 new RED-first structural pins at
  tests/invariants/test_cp_census_tenant_admission_correction_phase_4_c_v.py

Appends a schema-complete ratchet_history entry matching prior slice format
(slice_id, sealed_at_utc, passed, commit, delta, canon_ref, note).

Zero remote · zero network · pure local read/write · deterministic.
Additive to R-6 (a) regen trigger (§3.3 seal boundary).
"""
from __future__ import annotations

import json
from pathlib import Path

BASELINE = Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json"
)

OLD_FLOOR = 6194
NEW_FLOOR = 6206
DELTA = 12

NEW_ENTRY = {
    "slice_id": "CP-CENSUS-TENANT-ADMISSION-CORRECTION-PHASE-4-C-V",
    "sealed_at_utc": "2026-02-23T00:41:00Z",
    "passed": NEW_FLOOR,
    "commit": "PENDING-P4-C-V-COMMIT-A",
    "delta": DELTA,
    "canon_ref": "Owner correction 2026-02-23T00:30Z + CP-TENANT-SEPARATION owner card §3",
    "note": (
        "PHASE 4 (c-v) · CP-CENSUS-TENANT-ADMISSION-CORRECTION · "
        "small additive slice on owner queued correction · admits all "
        "four canonical tenants for CENSUS jobs (declarative pin + "
        "drift-detector on sealed CENSUS_ADMITTED_TENANT_IDS) · "
        "§3 source-to-tenant registration map · RETRO_ASSIGNMENT "
        "records (census_0001/0002 → DIGICOW · rms_item_3_receipts → "
        "RMS · additive re-registration · sealed receipts UNCHANGED) · "
        "DAP-14 controlled-request gating stays held on DQ-19/DQ-20 "
        "(orthogonality assertion) · SO §3.8 additive-only · sealed "
        "carriers UNCHANGED (tenant_scope + tenant_registry + "
        "dap_activation) · 12 RED-first invariants at "
        "tests/invariants/test_cp_census_tenant_admission_correction_"
        "phase_4_c_v.py"
    ),
}


def main() -> int:
    data = json.loads(BASELINE.read_text())

    # 1. Verify current state matches expected pre-bump.
    if data["counts_at_baseline"]["passed"] != OLD_FLOOR:
        raise SystemExit(
            f"counts_at_baseline.passed={data['counts_at_baseline']['passed']} "
            f"expected {OLD_FLOOR}"
        )
    if (
        data["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
        != OLD_FLOOR
    ):
        raise SystemExit(
            f"passed_floor={data['invariants_enforced_when_baseline_guard_1']['passed_floor']} "
            f"expected {OLD_FLOOR}"
        )

    # 2. Bump both floor fields.
    data["counts_at_baseline"]["passed"] = NEW_FLOOR
    data["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_FLOOR

    # 3. Append new ratchet_history entry (Banked Lesson #6 respected:
    #    passed field equals NEW post-seal floor).
    data["ratchet_history"].append(NEW_ENTRY)

    # 4. Persist deterministically (preserve 2-space indent per BL #7 · preserve
    #    unicode chars via ensure_ascii=False so historical em-dashes / arrows
    #    stay literal — matching prior write pattern).
    BASELINE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"baseline_failures.json bumped: {OLD_FLOOR} → {NEW_FLOOR} (+{DELTA})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
