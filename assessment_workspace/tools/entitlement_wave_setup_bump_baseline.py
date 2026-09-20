"""tools/entitlement_wave_setup_bump_baseline.py

Bump `backend/tests/invariants/baseline_failures.json` for CP-ENTITLEMENT-WAVE-SETUP
Commit-A landing on programme/track-a.

Delta measurement (post-GREEN reconcile line-by-line):
  Baseline (post-CP-Q-UNLOCK-SUB-WAVE):
    passed_floor = 5600
    counts_at_baseline.passed = 5600
  Full-sweep post-GREEN result (mid-authoring, before card fix):
    5618 pass · 6 failed (3 pod_shell mirror-drift banked + 3 card-integrity broken by
    incomplete ENTITLEMENT.md pre-fix)
  Full-sweep post-GREEN result (after card fix + complete authoring):
    Expected: 5621 pass · 3 failed (only the 3 pod_shell mirror-drift · already
    banked in baseline_failures.json specialist-dispatch-in-flight section)
  Delta: +21 exactly = 20 new entitlement tests + 1 wave-setup spec-verify guard

Both fields MUST be bumped together (CCS2 lesson · CCS3 seal precedent).

Bank ratchet_history append with Q-unlock predecessor SHA + this-wave narrative.
"""
from __future__ import annotations
import hashlib
import json
import pathlib

BASELINE = pathlib.Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json"
)
EXPECTED_PRIOR = 5600
NEW_FLOOR = 5621

with open(BASELINE) as f:
    data = json.load(f)

prior_passed_floor = data["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
prior_counts = data["counts_at_baseline"]["passed"]
assert prior_passed_floor == EXPECTED_PRIOR, (
    f"passed_floor drift: expected {EXPECTED_PRIOR} · actual {prior_passed_floor}"
)
assert prior_counts == EXPECTED_PRIOR, (
    f"counts_at_baseline.passed drift: expected {EXPECTED_PRIOR} · actual {prior_counts}"
)

data["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_FLOOR
data["counts_at_baseline"]["passed"] = NEW_FLOOR

data.setdefault("ratchet_history", []).append({
    "at_utc": "20260920T151500Z",
    "commit": "PENDING-CP-ENTITLEMENT-WAVE-SETUP-COMMIT-A",
    "cp": "CP-ENTITLEMENT-WAVE-SETUP (WAVE R-81)",
    "note": (
        "CP-ENTITLEMENT-WAVE-SETUP · WAVE R-81 opening seal · Entitlement Service Spec v1 setup wave. "
        "State-side extract at notes/entitlement_service_v1_atomic_rules.md (49 ENT + 12 defined terms + 8 R + 5 LIM · byte-verbatim from custody docx sha256 46c3670e...). "
        "Objective card at STATE/OBJECTIVES/ENTITLEMENT.md (SO §6.2 pre-authorised drafting · card_sha256 pinned). "
        "Code-side new test surface at backend/tests/invariants/test_entitlement_service_v1_property_tests.py = 21 tests total: "
        "1 wave-setup spec docx byte-verify guard + 11 owner-designated property tests (ENT-13/16/17/18/19/22/26/32/34/35/49 with two-phase attestation pattern · package-absent PASS as absence attestation · package-present enforce structurally at build wave) + 6 grep-negative hard bans (ENT-16 no default values + ENT-20 no entitlement event type + ENT-21 no second billing store + ENT-22 no stored counter + ENT-12 no retroactive rating + ENT-35 no key recovery) + 3 fixed-string byte-match attestations (ENT-23 cost-not-yet-measured + ENT-26 frontier-allowance-used-served-locally + ENT-34 frontier-unavailable-served-locally) byte-matched against custody docx + specialist /app/frontend/src/strings/entitlementStrings.js. "
        "Delta +21 measured (5600 -> 5621 · monotonic-up per owner directive). "
        "Additive-only per SO §3.8: NEW test file only · zero implementation module (services/entitlement_service_v1/*.py NOT authored at setup wave · lands at CP-ENTITLEMENT-BUILD-WAVE R-82 per confirmed sprint order) · zero sealed contract edit · zero writer edit. "
        "Cross-check byte-match verified against specialist entitlementStrings.js at phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log. "
        "AUTHENTIC RED-first cycle receipt at phase0/drill_receipts/20260920T1510Z_cp_entitlement_wave_setup_RED_pre_ent22.log (controlled ENT-22 violation introduced via services/_TEMP_ent22_drill_violation.py · 2 fail right-reason ENT-22 property + ENT-22 grep-negative catching credit_counter_stored identifier · violation removed) -> GREEN at 20260920T1512Z_cp_entitlement_wave_setup_GREEN_post.log (21/21 pass in 1.85s). "
        "Setup wave produces: atomic-rules extract + objective card + RED-first property tests + grep-negative hard bans + fixed-string byte-match attestations. Build wave (CP-ENTITLEMENT-BUILD-WAVE R-82) will land implementation modules for local + Your-Keys paths (Managed Frontier reseller-channel HARD HOLD pending R-24 counsel review · R-26..30 defaults tagged pending · R-31 seats as default with separate agent count at organisation size)."
    ),
    "passed": NEW_FLOOR,
    "delta": 21,
    "specialist_dispatch_drift_carried_forward": 3,
})

new_bytes = json.dumps(data, indent=2, sort_keys=False).encode() + b"\n"
with open(BASELINE, "wb") as f:
    f.write(new_bytes)

new_sha = hashlib.sha256(new_bytes).hexdigest()
print(f"BASELINE_FAILURES_JSON new sha256: {new_sha}")
print(f"passed_floor: {prior_passed_floor} -> {NEW_FLOOR} (delta +{NEW_FLOOR - prior_passed_floor})")
print(f"counts_at_baseline.passed: {prior_counts} -> {NEW_FLOOR}")
