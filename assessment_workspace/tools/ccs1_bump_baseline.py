#!/usr/bin/env python3
"""Bump baseline_failures.json ratchet for CP-CCS1-C17-SEAM-BUNDLE-FREEZE.

Surgical, idempotent, additive-only per SO §3.8. Delta = +11 (5491 → 5502).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

BF = Path("/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json")

CP = "CP-CCS1-C17-SEAM-BUNDLE-FREEZE"
OLD_FLOOR = 5491
NEW_FLOOR = 5502
DELTA = NEW_FLOOR - OLD_FLOOR  # 11

# ratchet_history entry note (verbatim seal narrative · matches prior entries' shape).
NOTE = (
    "CP-CCS1-C17-SEAM-BUNDLE-FREEZE · contract closure wave 1 · C.17 answering-service "
    "seam bundle freeze · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z "
    "verbatim ('Seal W4 and CONTINUE DIRECTLY into CCS1 without stopping ... CCS1 (C.17 "
    "answering-service seam bundle-freeze) → CCS2 (DAP entitlement) → CCS3 (DAP receipt), "
    "each frozen from dap_backend_spec_v1 under T-b (JSON-Schema authoritative — freeze "
    "from spec even where backend is thin), tests-first, §3.3 sealed. Work the survey's "
    "10 absence findings into the freeze scope: each finding either closes in its CCS "
    "wave or is banked with a reason.') + owner ruling 2026-09-19T~17:54Z item (e) "
    "verbatim (survey now, then closure waves in dependency order — C.17 seam first). "
    "DELTA 11 = 11 new invariants in tests/invariants/test_ccs1_c17_seam_bundle_freeze.py: "
    "W1.1a application_contract_v0 schema sha256 pin (re-asserts M17-W1 milestone snapshot "
    "pin ba1957df… as per-schema pin under bundle) + W1.1b ask_v0 schema sha256 pin "
    "d0f39639… + W1.1c handoff_contract_v0 schema sha256 pin e5d6c74a… + W1.1d "
    "personal_client_session_v0 schema sha256 pin cc7bd992… + W1.2 seam bundle snapshot "
    "pin a6107d46f4f5d80fa7be4d28e8c427a0a4be15438a1843ca17aeab197b708033 (name-sorted "
    "concat of 4 schemas · canonical JSON bytes · Canon 3 §9.3 canonicalization "
    "discipline) + W1.3 bundle vocabulary containment (exactly 4 named shapes) + W1.4 "
    "all 4 seam shapes SO §3.10-α compliant (frozen=True + extra='forbid') + W2.1 AST "
    "invariant: services/personal_client/**/*.py imports seam shapes only from sealed "
    "identity paths (contracts.application_contract_v0 · services.answering_service.collections.asks "
    "· contracts.handoff_contract · contracts.personal_client_session_v0) + W2.2 AST "
    "invariant: no shadow/masquerade class definition of the 4 seam shapes anywhere in "
    "backend/**/*.py outside their sealed origin files (scope excludes tests/** + tools/** "
    "+ the 4 sealed origin files themselves) + W3 integration test end-to-end binds "
    "bundle across ask flow (instantiate ApplicationContract_v0 → PersonalClientSession_v0 "
    "→ HandoffContract_v0 → Ask_v0 · recompute bundle sha at each step · assert equality "
    "with frozen constant · mirrors M17-W5 seal-integration pattern verbatim) + Banking "
    "test attests EFCS survey absence finding #4 CLOSED at this wave. NEW test file only "
    "(no new implementation module needed · all 4 seam contracts already sealed at "
    "M14-W1/M14-W3/M17-W1/M17-W3). Additive-only per SO §3.8. Sealed contracts NOT edited "
    "(ApplicationContract_v0 + Ask_v0 + HandoffContract_v0 + PersonalClientSession_v0 "
    "all consumed via identity import). Absence findings addressed at this wave: #4 "
    "CLOSED (bundle pin authored) + #2 CLOSED structurally (T-b JSON-Schema-authoritative "
    "discipline adopted · model_json_schema() output IS the frozen schema). Absence "
    "findings BANKED to future waves: #1 (DAP UI Handoff Brief §5 location) banked to "
    "frontends-card wave · #3 (DAP21MeteredEvent_v0) banked to CCS3 W1 · #5 (six-profile "
    "closed-tuple freeze) banked to CCS2 W2 · #6 (reliable_time_source wiring) banked to "
    "CCS3 W4 · #7 (ledger-write-before-return for DAP-21) banked to CCS3 W3 · #8 "
    "(approval_request/admission_refusal/erasure_request/v2_refusal/asset_registry/watch_action_v0 "
    "status) banked to status-confirmation sub-wave at frontends-card-drafting boundary · "
    "#9 (trust_receipt_v1 vs DAP-21 receipt) banked to CCS3 W1 · #10 (outer_gate_receipt_v1 "
    "vs DAP-21 receipt) banked to CCS3 W1. AUTHENTIC RED-first cycle: RED at "
    "phase0/drill_receipts/20260919T215044Z (test_ccs1_seam_bundle_snapshot_pin_matches_frozen_constant "
    "1 fail right-reason: computed sha `a6107d46f4f5d80fa7be4d28e8c427a0a4be15438a1843ca17aeab197b708033` "
    "!= corrupted-all-zeros frozen constant · other 10 tests either pass or not-yet-reached · "
    "-x stop at first fail) → intermediate GREEN attempt at 20260919T215101Z discovered "
    "W3 integration test W3 field-shape drift (ApplicationContract_v0.receipt_policy "
    "required · PersonalClientSession_v0.composed_at → started_at · HandoffContract_v0 "
    "surface differs from initial draft) · fixed with actual field discovery via "
    "model_json_schema() introspection → GREEN at drill_receipts/20260919T215151Z (11/11 "
    "pass · 1.44s). Canon anchors verbatim: Canon 5 Interface Architecture · seam-boundary "
    "discipline + Canon 17 §4 answering-service triangle · ask entity + Canon 15 §33 "
    "HandoffContract_v0 frozen contract discipline + Canon 3 §9.3 append-only writer "
    "discipline (canonicalization discipline applied to bundle sha) + Canon 8 §W11 "
    "one-task-one-identity (no shadow classes for the 4 seam shapes anywhere in "
    "services/personal_client/) + SO §3.8 thin-kernel additive-only + SO §3.10-α "
    "closed-schema discipline (Option-α · frozen=True + extra='forbid' on all 4 seam "
    "shapes) + SO §6.4 NOTHING-BEYOND (scope frozen at 4 seam shapes + 3 sub-wave test "
    "clusters + banking test · no scope beyond) + SO §6.7 sequence-from-here (CCS1 → "
    "CCS2 → CCS3 → HALT before frontends) + M17-W1 milestone snapshot pin ba1957dfbb… "
    "precedent shape (this-wave re-asserts same sha256 for ApplicationContract_v0 as "
    "its per-schema frozen constant) + M17-W5 seal-integration pattern (W3 integration "
    "test mirrors verbatim) + HR-2 hand-off entry carries the right identities "
    "(CP-M17-W6 adapter landed prior to this seal · handoff_id regex ^ho_[a-z0-9_-]+$ "
    "frozen in Ask_v0). Owner rulings verbatim: FRONTENDS-GATE-IS-HALT-POINT this-turn + "
    "owner ruling 2026-09-19T~17:54Z item (e) survey ruling. Stop-conditions #1/#2/#3 "
    "NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · "
    "staleness clock T-~14.1h remains armed · autopilot next CCS2 DAP entitlement freeze "
    "→ CCS3 DAP receipt freeze → HALT at frontends gate for owner dispatch to specialists."
)

RECEIPTS = [
    "phase0/drill_receipts/20260919T215044Z_cp_ccs1_c17_seam_bundle_freeze_RED_pre.log",
    "phase0/drill_receipts/20260919T215151Z_cp_ccs1_c17_seam_bundle_freeze_GREEN_post.log",
]

CP_AT_UTC = "20260919T215200Z"


def main() -> int:
    d = json.loads(BF.read_text(encoding="utf-8"))

    # Idempotency check: refuse if entry already present.
    for entry in d["ratchet_history"]:
        if entry.get("cp") == CP:
            print(f"SKIP: ratchet_history already carries entry for {CP}")
            return 0

    # Preconditions.
    assert d["counts_at_baseline"]["passed"] == OLD_FLOOR, (
        f"counts_at_baseline.passed drift: {d['counts_at_baseline']['passed']} != {OLD_FLOOR}"
    )
    assert d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] == OLD_FLOOR, (
        f"passed_floor drift: {d['invariants_enforced_when_baseline_guard_1']['passed_floor']} != {OLD_FLOOR}"
    )

    # Update floor fields.
    d["counts_at_baseline"]["passed"] = NEW_FLOOR
    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_FLOOR

    # Append ratchet_history entry (mirrors prior CP entries' shape).
    d["ratchet_history"].append({
        "at_utc": CP_AT_UTC,
        "cp": CP,
        "delta": DELTA,
        "passed": NEW_FLOOR,
        "note": NOTE,
        "receipts": RECEIPTS,
    })

    # Preserve exact serialization convention: sort_keys=False (preserve field
    # order established by prior writers · not a ratchet-integrity concern),
    # indent=2, ensure_ascii=True (preserves Unicode-escape encoding as noted
    # in the W3 transparency banking).
    out = json.dumps(d, indent=2, ensure_ascii=True) + "\n"
    BF.write_text(out, encoding="utf-8")

    # Report post-state.
    new_sha = hashlib.sha256(BF.read_bytes()).hexdigest()
    new_lines = sum(1 for _ in BF.read_text().splitlines())
    print(f"OK: bumped {OLD_FLOOR} → {NEW_FLOOR} (+{DELTA}) · appended ratchet_history entry for {CP}")
    print(f"    new baseline_failures.json sha256: {new_sha}")
    print(f"    new file size: {BF.stat().st_size} bytes, {new_lines} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
