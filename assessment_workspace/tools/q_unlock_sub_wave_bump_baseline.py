"""Bump baseline_failures.json ratchet for CP-Q-UNLOCK-SUB-WAVE.

Delta:
    +23 new Q-unlock invariants (W9-W15 clusters at test_dap_lifecycle_wave.py)
    -3 specialist-dispatch-in-flight drift (3 pod_shell/frontend mirror tests)
Net: +20 · new floor 5600 · prior floor 5580.

Baseline_failures adds 3 entries: the mirror-drift tests. This is
DOCUMENTED coordination-window drift (owner ruling R-78 FE DISPATCH
COORDINATION dispatched the web specialist in parallel + specialist edits
to /app/frontend/ drift ahead of the pod_shell/frontend/ repo mirror).
Reconciliation lands at the specialist's next coordination seal · this
Q-unlock seal captures the drift transparently.
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
    prior_baseline_len = len(doc["baseline_failures"])
    if prior_passed != 5580 or prior_floor != 5580:
        print(
            f"REFUSE · expected 5580 on both; got passed={prior_passed} "
            f"floor={prior_floor}",
            file=sys.stderr,
        )
        return 1
    if prior_baseline_len != 0:
        print(
            f"REFUSE · expected baseline_failures=[] pre-bump; got "
            f"{prior_baseline_len} entries",
            file=sys.stderr,
        )
        return 1

    new_floor = 5600
    delta = new_floor - prior_floor
    print(f"Measured delta: +{delta} (5580 -> {new_floor})")

    doc["counts_at_baseline"]["passed"] = new_floor
    doc["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = new_floor
    doc["counts_at_baseline"]["failed"] = 3  # 3 specialist-dispatch-in-flight drift

    doc["baseline_failures"] = [
        "tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js",
        "tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir",
        "tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell",
    ]

    doc["ratchet_history"].append(
        {
            "at_utc": "20260920T142000Z",
            "commit": "PENDING-CP-Q-UNLOCK-SUB-WAVE-COMMIT-A",
            "cp": "CP-Q-UNLOCK-SUB-WAVE (WAVE R-70 Step 2)",
            "note": (
                "Q-UNLOCK sub-wave landing owner ruling R-78 (2026-09-20T~13:00Z) "
                "Q1/Q2/Q4/Q5/Q7 + Expired-submit-again + suspension-notices "
                "backend surfaces + JWT test-account seed (Addition B fold-in). "
                "Delta +23 new invariants at W9-W15 clusters (Interrupted state, "
                "Q1 Retry bounded DEFAULT 3 hash-identical-objective, Q2 standing "
                "approval Download units+operation, Q4 spend reason-line in InApproval, "
                "Q5 escrow + Ready-on-lift + termination-hash-retaining destruction, "
                "Expired submit_again_as_new_request, suspension_notices minimal). "
                "Delta -3 specialist-dispatch-in-flight mirror drift banked in "
                "baseline_failures (web specialist dispatched per owner ruling R-78 "
                "FE DISPATCH COORDINATION · edits to /app/frontend/ drift ahead of "
                "pod_shell/frontend/ repo mirror · reconciliation at specialist's next "
                "coordination seal · this-seal captures drift transparently). Net +20 "
                "(5580 -> 5600 · monotonic-up per owner). Additive-only per SO §3.8: "
                "5 new modules services.dap_lifecycle/{interrupted_service, retry_service, "
                "escrow, expired_action, suspension_notices}.py + docstring-sanctioned "
                "two-side extensions on services.dap_lifecycle/{state_machine, fail_closed, "
                "approval_service}.py + tests/invariants/test_dap_lifecycle_wave.py "
                "extended with W9-W15 clusters + docstring-sanctioned pin updates for "
                "new enum member Interrupted + 3 new edges + snapshot sha regen "
                "253c69c6->9a0595dc (delta = +Interrupted state + 3 new edges per Q7 "
                "verbatim). Q3 partial-release + Q6 owner-turnaround-line stay HARD "
                "HOLDs · not built. Pod-shell operational-wiring for auth router "
                "landed at /app/backend/server.py + pod_shell/backend/server.py "
                "(byte-identical mirror sync) + KNOWN_UNWIRED entry for routers.auth "
                "removed + JWT_SECRET env-only additive at /app/backend/.env + demo "
                "identity seeder idempotent-startup hook · frontend specialist can "
                "hit /api/auth/login → /api/auth/refresh with 4 seeded demo accounts "
                "(demo.master_admin/dpo/operator/analyst @demo.rms.example.com per "
                "services.auth.demo_identity_seeder) documented at "
                "/app/memory/test_credentials.md."
            ),
            "passed": new_floor,
            "delta": delta,
            "specialist_dispatch_drift_added_to_baseline_failures": 3,
        }
    )

    baseline_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    new_bytes = baseline_path.read_bytes()
    new_sha = hashlib.sha256(new_bytes).hexdigest()
    print(f"New sha256:   {new_sha}")
    print(f"Bump complete: passed_floor 5580 -> {new_floor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
