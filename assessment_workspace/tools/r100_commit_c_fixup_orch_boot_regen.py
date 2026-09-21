"""R-100 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r99_commit_c_fixup_orch_boot_regen.py precedent exactly.

- state_repo (heads_last_sealed.state_repo): replaced with R-100 Commit-B
  `e6a86c2c3f613def64cc854710837f03c468d89e` entry (was R-99 Commit-B
  `58685080caafe967111ea1af6e3f665e1b5518c5`).
- code_repo history: fresh entry for R-100 Commit-A
  `39412d09a6d7f0420049fd96908778eedbc56ab2` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order (R-99 Commit-A `eb40fb67...` remains
  as the next-most-recent entry).
- generated_at_utc + regeneration_reason: updated to R-100 Commit-C fixup.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R100_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R100_STATE_HEAD = "e6a86c2c3f613def64cc854710837f03c468d89e"
R100_CODE_HEAD = "39412d09a6d7f0420049fd96908778eedbc56ab2"
R100_STATE_SEALED_AT = "2026-09-21T08:40:00Z"
R100_CODE_SEALED_AT = "2026-09-21T08:32:00Z"
NEW_UTC = "2026-09-21T08:45:00Z"
NEW_REGEN_REASON = (
    "r100-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "e6a86c2c-cp-portal-write-surface-commit-b-plus-new-code-repo-history-"
    "entry-for-r100-commit-a-39412d09-additive-jwt-gated-portal-write-path-"
    "routers-portal-requests-plus-portal-entitlement-plus-additive-state-"
    "machine-stopped-state-edge-terminal-owner-ruled-four-conditions-jwt-"
    "principal-plus-request-scoped-stop-plus-chokepoint-invoke-plus-"
    "disclosure-discipline-plus-continuity-bundle-standing-rule-completion-"
    "sprint-step-4-continuation"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R100_STATE_HEAD}
    sealed_at_utc: {R100_STATE_SEALED_AT}
    seal_kind: "R-100 CP-PORTAL-WRITE-SURFACE · state Commit-B `{R100_STATE_HEAD}` · banks Commit-A `{R100_CODE_HEAD}` on programme/track-a · WAVE R-100 · COMPLETION SPRINT step 4 continuation · additive JWT-gated portal write-path routers (routers/portal_requests.py + routers/portal_entitlement.py) exposing sealed lifecycle + entitlement services under owner-ruled four conditions (2026-09-21T~07:50Z verbatim): (1) principal from JWT propagation never header · unauthenticated refuses (PRIN-11/PRIN-12) · (2) stop is request-scoped Executing→Stopped NOT party_halt (owner-authorised additive state-machine trio · precedent R-78 Interrupted) · (3) submit routes through sealed lifecycle stack DAP-18/14/21 + invoke() chokepoint · ENT-16 in invoke() · (4) reads carry identity + disclosure discipline ENT-22-no-cache + ENT-3/ENT-43-dial-admit-badges + DAP-15-no-approver-identity + DAP-35-no-remaining-budget + R-78-bounded-3-retry-hash-identical. Owner CONTINUITY BUNDLE new standing rule (2026-09-21T~08:10Z verbatim): at every seal git bundle create for ALL THREE local-only repos (code programme/track-a + state master + FE /app main) + sha256-pin all three in STATE/PINS.md · zero-push · landing this-Commit-C fixup as 3 bundles + STATE/PINS.md CONTINUITY-BUNDLE-PINS block. pre-Commit-A ratchet 5831 → 5852 + notes/ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + tools/r100_pre_commit_a_ratchet_and_orch_boot_regen.py + STATE/PINS.md commissioning_record pointer refresh 20260921T042214Z → 20260921T083731Z (R-29-BOOT housekeeping-pickup precedent) + phase0/spec_hunt_receipts/20260921T083500Z_r100_portal_write_surface_seal_report.md NEW FE-WIRING-READY-2 dispatch artifact (14 endpoints R-99 5 read-only + R-100 9 write/read · JWT-only auth · sample payloads · 6 owner-CONDITION binding constraints inheritance). FE-WIRING-READY-2 flag RAISED at this Commit-B for FE specialist ONE-pass dispatch (portal write paths + rbm-8 countdown surface + canon-rule displays together per owner directive verbatim). R-100 seal completes cleanly inside R-91 window with zero ceremony-apply operations opened (current UTC 2026-09-21T~08:35Z < horizon 2026-09-23T03:23:15Z · ~42.9h out). Autopilot next Commit-C fixup this-turn advances state_head + inserts code_repo entry for R-100 Commit-A 39412d09 + executes Continuity Bundle export (3 bundles) + STATE/PINS.md sha256 pins → FE-WIRING-READY-2 specialist dispatch → residual scan (none pending after R-100) → R-91 ε-APPLY at horizon (NO EXPEDITE) → M1-to-date BUILD_JOURNAL closure state-only (COMPLETION SPRINT step 6)."
"""

NEW_R100_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R100_CODE_HEAD}
    sealed_at_utc: {R100_CODE_SEALED_AT}
    seal_kind: "R-100 CP-PORTAL-WRITE-SURFACE · Commit-A `{R100_CODE_HEAD}` · code programme/track-a · WAVE R-100 · COMPLETION SPRINT step 4 continuation · additive JWT-gated portal write-path routers exposing sealed lifecycle + entitlement services + additive state-machine trio under owner-ruled four conditions (2026-09-21T~07:50Z verbatim) · Adds NEW backend router routers/portal_requests.py (265 lines · APIRouter prefix=/api/portal/requests · 5 endpoints GET list + GET detail + POST submit + POST stop + POST retry · JWT-gated via require_identity_or_deny short-circuit pattern matching team.py precedent · consumes sealed services.dap_lifecycle.{{state_machine,retry_service,request_stop}} + services.auth.{{dependencies,identity}} + services.request_context.enter_propagation PRIN-11 propagation) + NEW backend router routers/portal_entitlement.py (196 lines · APIRouter prefix=/api/portal/entitlement · 4 endpoints GET licence + GET catalog/listed + GET allowance + GET badges · same JWT-only pattern · consumes sealed services.entitlement_service_v1.{{licence,catalog,allowance,chokepoint_resolver}} · per-call derive_allowance_remaining ENT-22 no cache · dial-admit gate reference via _dial_admits_access_class ENT-3+ENT-43) + NEW backend service services/dap_lifecycle/request_stop.py (74 lines · additive request-scoped confirm-copy renderer · BYTE-VERBATIM restatement of request-scoped stop-confirm copy text per owner CONDITION 2 verbatim · owner-surface party-halt module NOT imported here · zero external I/O · pure deterministic surface) + NEW test tests/invariants/test_r100_portal_write_surface.py (511 lines · 21 tests: 5 router-surface + 4 CONDITION 1 principal-JWT + 5 CONDITION 2 state-machine + 7 CONDITION 4 disclosure · SO §2.5 verbatim-docstring) + additive services/dap_lifecycle/state_machine.py (+26 lines · additive RequestState.Stopped 12th state + TERMINAL_STATES entry 4th + ALLOWED_EDGES entry (Executing,Stopped) · precedent R-78 Interrupted addition · owner authorised verbatim 'the state machine may need the additive Executing → Stopped transition if it doesn't exist — additive only, verify first') + additive tests/invariants/test_dap_lifecycle_wave.py (+22 lines · companion expected-set additive updates for state + TERMINAL_STATES + ALLOWED_EDGES · precedent R-78) + regen tests/invariants/dap_lifecycle_wave.lifecycle_shape_snapshot.json contract_sha256 9a0595dce01c1f247278bc2b0490689c6c3894881448f2e3dceabb6964596259 → de55a65a51824478e8afadcbae899d5e90b1836141e2204ccbce5950330129a3 + additive server.py mount (+8 lines · 2 additive router mounts · each prefix carried by router) + additive backend/tests/invariants/known_unwired.py (+50 lines · 2 new entries keyed routers.portal_requests + routers.portal_entitlement with Doc04/Doc05/Doc11/Doc12 SRR canon citations + FE-WIRING-READY-2 remediation R-tag) + baseline_failures.json ratchet 5831 → 5852 both fields + new ratchet_history entry documenting this-wave · DELTA +21 MEASURED (targeted equalled measured · no CCS2 correction needed) · new baseline_failures.json sha256 b6520ba9320728c05864b4f44c35bcbdecc0c440e9cf00d8b997931f841ad0d1 was 070c57c4cf8618554a7857f8e14a0e2555ae4d8593df6953b1693080c3e8361f · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · Sealed R-99 canon_rules_registry + R-98 canon_rules_service.rbm_roc_vocabulary + R-97/R-96 canon_dap_lifecycle vocabularies + R-95..R-88 seal chain all continue verbatim GREEN · additive-only per SO §3.8 · AUTHENTIC RED-first: 21 tests authored BEFORE routers/state-machine edits · initial RED sweep 6/21 fail right-reason (docstring grep-negative hits on X-Akki-App-ID + party_halt_billing · single-line-import regex mismatch for multi-line imports · Depends-based auth pattern producing 500 instead of 401 AuthDenied uncaught) → GREEN post-fix (docstring scrubbing + single-line imports + require_identity_or_deny short-circuit pattern matching team.py precedent 15+ router precedents + async def signatures) + 4 test_dap_lifecycle_wave invariants flipped from initial RED-post-state-machine-edit to GREEN after companion additive-expected-set updates + contract snapshot regen → deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical drill_receipts/20260921T083222Z_r100_post_ratchet_sweep_run1.log + 20260921T083536Z_r100_post_ratchet_sweep_run2.log both 5852 passed · 3 baseline-fails (test_ship_manifest_dod + 2 test_wave_g_pod_shell_frontend_mirror · all subset of baseline_failures per V4 invariant) · 1 skip · 438 warnings · ~186s each · FE-WIRING-READY-2 flag raised via Commit-B seal report handoff artifact banking all 14 endpoints (R-99 5 read-only canon rules + R-100 9 portal write/read) + JWT-only auth (POST /api/auth/login → refresh · NO X-Akki-App-ID anywhere · grep-negative test enforces) + sample payloads verbatim from live sweep run1 + 6 owner-CONDITION binding constraints inheritance (a request-scoped stop confirm copy · b no approver identity in list/detail DAP-15 · c no remaining-budget reason line DAP-35 · d badges licence-admitted rows only ENT-3/ENT-43 · e R-91 countdown surface consumes /api/canon/rules/rbm-8-ceremony-mechanic byte-verbatim · f JWT via /api/auth/login → refresh no header-identity anywhere) · Canon anchors verbatim: owner COMPLETION SPRINT (2026-09-21T~06:10Z six-step directive) + owner four-conditions ruling (2026-09-21T~07:50Z verbatim CONDITIONS 1-4) + owner CONTINUITY BUNDLE standing rule (2026-09-21T~08:10Z verbatim all-three-repos) + owner R-91 NO-EXPEDITE (RBM-8/SER C.5 I-4) + Doc04 (Solva depth governor) DAP-14/15/18/21/24/28/35 + Doc11 (Custody · entitlement service) ENT-3/5-8/9/16/22/43 + Doc12 (Rulebook Engine) RBM-8 + Doc06 (PRIN-11 propagation · PRIN-12 forbid header identity) + R-78 Interrupted additive precedent · R-99 seal chain (eb40fb67/58685080/2579f74f) + prior seal chain R-98..R-85 · SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.6/§6.7 · M16-W3 corrected order · CCS2 lesson · Autopilot next: Commit-B state master (banks this-Commit-A + regen tool + seal report + STATE hygiene commissioning refresh) → Commit-C fixup (this-turn advances state_head + inserts code_repo entry + Continuity Bundle export 3 bundles + STATE/PINS.md sha256 pins) → FE-WIRING-READY-2 dispatch → residual scan (none) → R-91 ε-apply at horizon (NO EXPEDITE) → M1-to-date BUILD_JOURNAL closure state-only"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R100_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-100 Commit-B.")
    else:
        state_repo_regex = re.compile(
            r"heads_last_sealed:\n"
            r"  state_repo:\n"
            r"    workdir: /app/assessment_workspace\n"
            r"    branch: master\n"
            r"    head: [0-9a-f]{40}\n"
            r"    sealed_at_utc: [^\n]+\n"
            r'    seal_kind: "[^\n]+"\n',
            re.DOTALL,
        )
        m = state_repo_regex.search(text)
        if not m:
            raise SystemExit("Could not locate heads_last_sealed.state_repo block")
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R100_CODE_REPO_BLOCK + text[m.end():]

    text = re.sub(
        r"^generated_at_utc:.*$",
        f"generated_at_utc: {NEW_UTC}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^regeneration_reason:.*$",
        f"regeneration_reason: {NEW_REGEN_REASON}",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)


def main() -> None:
    regen_orch_boot_commit_c()
    print(f"heads_last_sealed.state_repo.head → {R100_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R100_CODE_HEAD}")


if __name__ == "__main__":
    main()
