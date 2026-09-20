"""Bump baseline_failures.json ratchet for CP-DAP-LIFECYCLE-BACKEND-WAVE.

Prior floor 5546 · measured delta post-GREEN +34 · new floor 5580.
Both counts_at_baseline.passed AND
invariants_enforced_when_baseline_guard_1.passed_floor bumped together
per CCS2 lesson.

Ratchet history entry appended with the same shape as prior entries.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys


def main() -> int:
    baseline_path = pathlib.Path(
        "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json"
    )

    prior_bytes = baseline_path.read_bytes()
    prior_sha = hashlib.sha256(prior_bytes).hexdigest()
    print(f"Prior sha256: {prior_sha}")

    doc = json.loads(prior_bytes)
    prior_passed = doc["counts_at_baseline"]["passed"]
    prior_floor = doc["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
    if prior_passed != 5546 or prior_floor != 5546:
        print(
            f"REFUSE · expected 5546 on both; got passed={prior_passed} "
            f"floor={prior_floor}",
            file=sys.stderr,
        )
        return 1

    new_floor = 5580
    delta = new_floor - prior_floor
    print(f"Measured delta: +{delta} (5546 -> {new_floor})")

    doc["counts_at_baseline"]["passed"] = new_floor
    doc["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = new_floor

    doc["ratchet_history"].append(
        {
            "at_utc": "20260920T122000Z",
            "commit": "PENDING-CP-DAP-LIFECYCLE-BACKEND-WAVE-COMMIT-A",
            "cp": "CP-DAP-LIFECYCLE-BACKEND-WAVE (WAVE R-70 Step 1)",
            "note": (
                "DAP Request Lifecycle backend wave · buildable-now scope frozen "
                "at 6 items per STATE/DECISIONS.md R-77 + PENDING-RULINGS "
                "register STATE/dap_lifecycle_pending_rulings.md (DAP-LIFECYCLE-Q1..Q8). "
                "Owner corrections banked at wave-open (this-session verbatim): "
                "(1) DAP-15 14-day expiry runs from SUBMISSION to DECISION · "
                "transition is In Approval → Expired · silence never = approval · "
                "Ready → Expired is NOT the DAP-15 rule; "
                "(2) Q8 is DEFAULT-class BUILD-TO-YES-READING (destination removal "
                "future-only · historical receipts untouched · DAP-26 analogy) · "
                "pending ratification; Q7 disposition-set (Blocked stays 3-kind · "
                "non-gate fault surfaces as banked TODO marker fail-closed) · "
                "spec §6 remainder hunt receipt phase0/spec_hunt_receipts/"
                "20260920T1200Z_dap_spec_section6_hunt.json confirms; "
                "(3) notification event-emission surface added to scope (toast "
                "at submission + retrieval · email stub OFF DEFAULT-class); "
                "(+) identity-discipline addition (submitter surfaceable · approver "
                "never surfaced · decisions permanent no-reopen). "
                "Measured delta +34 (34 new invariants in tests/invariants/"
                "test_dap_lifecycle_wave.py W1-W8 · owner directive 'measure "
                "empirically post-GREEN, reconcile line-by-line, then bump · "
                "write the measured number' 2026-09-20T~12:00Z verbatim). "
                "Additive-only per SO §3.8: 8 new modules under "
                "services.dap_lifecycle/{state_machine,timer,approval_service,"
                "blocked_kinds,metering_wiring,notification_surface,fail_closed} "
                "+ __init__.py + 1 new test file + 1 new lifecycle-shape snapshot "
                "at tests/invariants/dap_lifecycle_wave.lifecycle_shape_snapshot.json "
                "(NOT a .contract_snapshot.json · deliberately outside frozen-Pydantic-"
                "parity domain per test_frozen_contract_snapshot_parity.py docstring "
                "lines 118-122). Sealed contracts NOT edited (contracts.dap.MeteredEvent "
                "shape consumed via composition only; parity test read-path is my "
                "own new test file). HARD HOLDs Q1-Q6 land as NotYetSpecified "
                "placeholders + Q2 STANDING_APPROVAL_BRANCH_REACHABLE_AT_RUNTIME=False "
                "+ Q6 Q6_OWNER_TURNAROUND_LINE_ENABLED=False. Q7 lands as "
                "NonGateExecutionFaultNotYetSpecified. Q8 lands as "
                "DESTINATION_REMOVAL_HISTORICAL_UNTOUCHED=True + Q8_RATIFICATION_STATUS="
                "'pending_ratification'."
            ),
            "passed": new_floor,
            "delta": delta,
            "receipts": [
                "phase0/drill_receipts/20260920T1210Z_dap_lifecycle_wave_RED_pre.log",
                "phase0/drill_receipts/20260920T1211Z_dap_lifecycle_wave_RED_full.log",
                "phase0/drill_receipts/20260920T1215Z_dap_lifecycle_wave_GREEN_post.log",
                "phase0/drill_receipts/20260920T1216Z_dap_lifecycle_wave_GREEN_post_snapshot.log",
                "phase0/drill_receipts/20260920T1220Z_dap_lifecycle_full_sweep_post_snapshot.log",
            ],
            "hunt_receipts": [
                "phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json",
            ],
        }
    )

    baseline_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    new_bytes = baseline_path.read_bytes()
    new_sha = hashlib.sha256(new_bytes).hexdigest()
    print(f"New sha256:   {new_sha}")
    print(f"Bump complete: passed_floor 5546 -> {new_floor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
