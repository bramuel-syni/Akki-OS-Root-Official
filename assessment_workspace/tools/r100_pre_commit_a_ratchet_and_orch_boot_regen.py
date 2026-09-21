"""R-100 pre-Commit-A: ratchet bump 5831 → 5852 (+21) + ORCH_BOOT ratchet-only regen.

Wave R-100 · COMPLETION SPRINT step 4 continuation · CP-PORTAL-WRITE-SURFACE.

Additive-only per SO §3.8: authors two NEW JWT-gated routers
`routers/portal_requests.py` + `routers/portal_entitlement.py` exposing
sealed lifecycle + entitlement services as principal-scoped
`/api/portal/*` endpoints under owner-ruled four conditions
(2026-09-21T~07:50Z verbatim):

  CONDITION 1 · principal from JWT propagation, never from a header;
               unauthenticated requests refuse (no default actor).
  CONDITION 2 · stop is REQUEST-SCOPED · additive Executing → Stopped
               state-machine edge (owner-authorised additive edit,
               precedent = R-78 Interrupted addition); party_halt
               stays behind the owner surface, requester portal
               MUST NOT reach into it.
  CONDITION 3 · submit routes through the sealed lifecycle stack
               (DAP-18 frozen objective + DAP-14 approval routing +
               DAP-21 metered event + invoke() only via chokepoint;
               ENT-16 resolution happens inside invoke()).
  CONDITION 4 · reads carry identity + disclosure discipline
               (ENT-22 allowance recomputed from Ledger events only;
               ENT-3+ENT-43 badges show ONLY dial-admitted rows;
               DAP-15 no approver identity surfaced; DAP-35 no reason
               line implies remaining budget; retry hash-identical
               bounded-3 receipted).

State-machine additive edit (precedent R-78 Interrupted):
  * RequestState.Stopped (name="Stopped", value="Stopped")
  * TERMINAL_STATES += RequestState.Stopped
  * ALLOWED_EDGES += (RequestState.Executing, RequestState.Stopped)
Companion invariant additions in test_dap_lifecycle_wave.py + contract
snapshot regen `dap_lifecycle_wave.lifecycle_shape_snapshot.json`
(sha256 9a0595dc → de55a65a).

Delta +21 (5831 → 5852) MEASURED: 21 new tests in
`tests/invariants/test_r100_portal_write_surface.py`.

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

PRIOR = 5831
NEW = 5852
DELTA = 21
NEW_UTC = "2026-09-21T08:30:00Z"

ENTRY = {
    "at_utc": "20260921T083000Z",
    "commit": "PENDING-CP-PORTAL-WRITE-SURFACE-COMMIT-A",
    "cp": (
        "CP-PORTAL-WRITE-SURFACE · WAVE R-100 · additive JWT-gated principal-"
        "scoped portal routers (routers/portal_requests.py + routers/"
        "portal_entitlement.py) + additive state-machine Stopped state/edge/"
        "terminal per owner-ruled four conditions · COMPLETION SPRINT step 4 "
        "of 6 (write-surface continuation of R-99 read-surface)"
    ),
    "note": (
        "R-100 COMPLETION SPRINT step 4 continuation · additive-only per "
        "SO §3.8 · authors TWO NEW routers under /api/portal/* prefix + "
        "ONE additive state-machine trio (state/edge/terminal) landing "
        "the requester write-surface owner-ruled 2026-09-21T~07:50Z. "
        "portal_requests.py (5 endpoints: GET / list + GET /{id} detail "
        "+ POST / submit + POST /{id}/stop + POST /{id}/retry) uses "
        "require_identity_or_deny JWT short-circuit pattern matching "
        "team.py precedent · consumes sealed services.dap_lifecycle."
        "state_machine (RequestState/ALLOWED_EDGES/TERMINAL_STATES/"
        "transition/IllegalTransition) + services.dap_lifecycle."
        "retry_service (attempt_retry/RETRY_MAX_ATTEMPTS_DEFAULT/"
        "RetryRefused) + services.dap_lifecycle.request_stop (additive "
        "module rendering request-scoped confirm-copy · owner-surface "
        "party-halt module NOT imported here) + services.auth."
        "dependencies.require_identity_or_deny + services.auth.identity "
        ".Identity + services.request_context.enter_propagation. "
        "portal_entitlement.py (4 endpoints: GET /licence + GET /catalog/"
        "listed + GET /allowance + GET /badges) consumes sealed services."
        "entitlement_service_v1 (Licence · CatalogRow · derive_allowance_"
        "remaining · LicenceAllowanceState · _dial_admits_access_class) "
        "with ENT-22 pure per-call derivation and ENT-3+ENT-43 dial-"
        "admit gate reference retained. Additive state-machine trio: "
        "RequestState.Stopped (12th state · precedent R-78 Interrupted "
        "added 11th) + TERMINAL_STATES adds Stopped (4th terminal · was "
        "3) + ALLOWED_EDGES adds (Executing, Stopped). Companion "
        "invariant additions in tests/invariants/test_dap_lifecycle_"
        "wave.py: expected states set adds Stopped · expected "
        "TERMINAL_STATES set adds Stopped · expected_edges set adds "
        "(Executing, Stopped) · contract snapshot dap_lifecycle_wave."
        "lifecycle_shape_snapshot.json contract_sha256 regenerated "
        "9a0595dce01c1f247278bc2b0490689c6c3894881448f2e3dceabb6964596259 → "
        "de55a65a51824478e8afadcbae899d5e90b1836141e2204ccbce5950330129a3 "
        "with note documenting the additive delta. Adds NEW test "
        "tests/invariants/test_r100_portal_write_surface.py with 21 "
        "tests (5 router-surface + 4 CONDITION 1 principal-JWT + 5 "
        "CONDITION 2 state-machine + 7 CONDITION 4 disclosure). "
        "Server.py mounts (4 lines: 1 comment + 1 import + 1 blank + "
        "1 include_router × 2 routers). Delta +21 MEASURED. R-91 stays "
        "PARKED · horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC "
        "2026-09-21T~08:30Z < horizon (~42.9h out) · R-100 seal "
        "completes cleanly inside window with zero ceremony-apply "
        "operations opened. Owner directive verbatim this-session "
        "(2026-09-21T~07:50Z at scope-delta reply): four conditions "
        "CONDITION 1 principal-from-JWT-only + CONDITION 2 request-"
        "scoped-stop-not-party-halt + CONDITION 3 chokepoint-invoke + "
        "CONDITION 4 disclosure-discipline · owner-authorised additive "
        "state machine edit. Owner new standing rule this-session "
        "(2026-09-21T~08:10Z at approval reply): CONTINUITY BUNDLE — "
        "at every seal, execute `git bundle create` for ALL THREE "
        "local-only repos (code programme/track-a · state master · "
        "FE /app main) and pin sha256 in STATE/PINS.md; zero-push "
        "scope. This wave will land three bundles as a Commit-C fixup "
        "artefact. FE-WIRING-READY-2 flag RAISED at Commit-B seal "
        "report dispatching all 14 endpoints (R-99 5 read-only canon "
        "rules + R-100 9 portal write/read) with binding constraints "
        "(a) request-scoped stop confirm copy · (b) no approver "
        "identity in list/detail (DAP-15) · (c) no remaining-budget "
        "reason line (DAP-35) · (d) badges licence-admitted only "
        "(ENT-3/ENT-43) · (e) R-91 countdown consumes /api/canon/"
        "rules/rbm-8-ceremony-mechanic byte-verbatim · (f) JWT via "
        "/api/auth/login → refresh no-header-identity anywhere. This "
        "wave FE-WIRING-READY-2: dispatch-ready endpoint list lands "
        "in Commit-B seal report."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "r100-pre-commit-a-ratchet-only-regen-cp-portal-write-surface-"
    "advancing-passed-floor-5831-to-5852-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-additive-routers-portal-"
    "requests-plus-portal-entitlement-plus-additive-state-machine-"
    "stopped-state-edge-terminal-owner-ruled-four-conditions-jwt-"
    "principal-plus-request-scoped-stop-plus-chokepoint-invoke-plus-"
    "disclosure-discipline-completion-sprint-step-4-continuation"
)


def bump_baseline() -> None:
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    assert d["counts_at_baseline"]["passed"] == PRIOR, (
        f"Prior mismatch: expected {PRIOR}, "
        f"got {d['counts_at_baseline']['passed']}"
    )
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
