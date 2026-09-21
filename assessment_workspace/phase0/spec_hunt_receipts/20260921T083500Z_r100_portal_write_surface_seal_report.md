# R-100 · CP-PORTAL-WRITE-SURFACE · Seal Report

**Wave**: R-100 · COMPLETION SPRINT step 4 continuation · additive JWT-gated portal write-path routers + additive state-machine trio
**Commit-A (code programme/track-a)**: `39412d09a6d7f0420049fd96908778eedbc56ab2` (short `39412d09`)
**Banked at UTC**: 2026-09-21T08:35:00Z
**Ratchet floor advance**: 5831 → 5852 (+21 measured = +21 targeted · CCS2 clean · no correction)
**baseline_failures.json sha256**: `070c57c4cf8618554a7857f8e14a0e2555ae4d8593df6953b1693080c3e8361f` → `b6520ba9320728c05864b4f44c35bcbdecc0c440e9cf00d8b997931f841ad0d1`
**ORCH_BOOT.md sha256 (post pre-Commit-A ratchet-only regen)**: `72354cc4a32b7dbe7dc8f839826efd751646df2ca23cde23b2f8a044cbac2e3a` → pinned via `tools/r100_pre_commit_a_ratchet_and_orch_boot_regen.py` (final Commit-C R-6 boundary sha lands next-turn)
**dap_lifecycle_wave.lifecycle_shape_snapshot.json contract_sha256**: `9a0595dce01c1f247278bc2b0490689c6c3894881448f2e3dceabb6964596259` → `de55a65a51824478e8afadcbae899d5e90b1836141e2204ccbce5950330129a3`
**BASELINE_GUARD=1 double-sweep**: both runs 5852 passed · 3 baseline-fails (test_ship_manifest_dod + 2 test_wave_g_pod_shell_frontend_mirror · all subset of baseline_failures) · 1 skip · 438 warnings. Receipts: `backend/phase0/drill_receipts/20260921T083222Z_r100_post_ratchet_sweep_run1.log` + `20260921T083536Z_r100_post_ratchet_sweep_run2.log`.

---

## Scope frozen per SO §6.4 NOTHING-BEYOND

Additive-only per SO §3.8. Commit-A tree = 10 files:

1. **NEW** `backend/routers/portal_requests.py` (265 lines) — FastAPI APIRouter with prefix `/api/portal/requests` + 5 endpoints (GET list · GET detail · POST submit · POST stop · POST retry). JWT-gated via `require_identity_or_deny` short-circuit pattern (team.py precedent). Consumes sealed `services.dap_lifecycle.{state_machine,retry_service,request_stop}` + `services.auth.{dependencies,identity}` + `services.request_context.enter_propagation` (PRIN-11 propagation).
2. **NEW** `backend/routers/portal_entitlement.py` (196 lines) — FastAPI APIRouter with prefix `/api/portal/entitlement` + 4 endpoints (GET licence · GET catalog/listed · GET allowance · GET badges). Same JWT-only pattern. Consumes sealed `services.entitlement_service_v1.{licence,catalog,allowance,chokepoint_resolver}` — per-call `derive_allowance_remaining` (ENT-22 no cache · no stored counter) · dial-admit gate reference retained via `_dial_admits_access_class`.
3. **NEW** `backend/services/dap_lifecycle/request_stop.py` (74 lines) — additive request-scoped confirm-copy renderer. BYTE-VERBATIM restatement of the request-scoped stop-confirm copy text per owner ruling this-session (2026-09-21T~07:50Z CONDITION 2: *"The stop-confirm copy may be reused if its text is request-scoped; party_halt stays behind the owner surface. A requester must never be able to halt a party, including their own."*). Zero external I/O · pure deterministic surface. Requester portal consumes this module exclusively; the owner-surface party-halt module stays intact and separate.
4. **NEW** `backend/tests/invariants/test_r100_portal_write_surface.py` (511 lines · 21 tests) — SO §2.5 verbatim-docstring on every test. Test breakdown: 5 router-surface (module importability × 2 · prefix × 2 · OpenAPI enumeration of all 9 paths) + 4 CONDITION 1 principal-JWT (grep-negative `X-Akki-App-ID` scan · `require_identity` JWT-required import · no default-principal patterns · unauthenticated 401 refusal) + 5 CONDITION 2 state-machine (Stopped state exists · Executing→Stopped edge in ALLOWED_EDGES · Stopped in TERMINAL_STATES · stop endpoint never imports party_halt_billing · stop handler references state_machine transition + Stopped) + 7 CONDITION 4 disclosure (derive_allowance_remaining call + import · no stored counter · badges through dial-admit gate · never approver identity fields · no remaining-budget response fields · retry uses attempt_retry · retry signature hash-identical — no fresh objective).
5. **MOD** `backend/services/dap_lifecycle/state_machine.py` (+26 lines) — additive `RequestState.Stopped` (12th state · was 11 with Interrupted) + `TERMINAL_STATES` entry (4th · was 3: Refused/Blocked/Expired · Stopped joins per owner ruling) + `ALLOWED_EDGES` entry `(Executing, Stopped)`. Additive-only precedent = R-78 Interrupted addition. Owner authorised verbatim: *"the state machine may need the additive Executing → Stopped transition if it doesn't exist — additive only, verify first"*.
6. **MOD** `backend/tests/invariants/test_dap_lifecycle_wave.py` (+22 lines) — expected states set adds `Stopped` · expected `TERMINAL_STATES` set adds `RequestState.Stopped` · expected_edges set adds `(RequestState.Executing, RequestState.Stopped)`. All three additions carry R-100 additive comment naming the owner verbatim ruling and the R-78 Interrupted precedent.
7. **MOD** `backend/tests/invariants/dap_lifecycle_wave.lifecycle_shape_snapshot.json` — `contract_sha256` regenerated `9a0595dc…` → `de55a65a…`. Delta note documents Stopped-state addition + TERMINAL +1 + edge +1 per owner ruling (banked at DECISIONS.md R-100).
8. **MOD** `backend/server.py` (+8 lines) — 2 additive router mounts (portal_requests + portal_entitlement · each prefix carried by router).
9. **MOD** `backend/tests/invariants/known_unwired.py` (+50 lines) — 2 new entries (`routers.portal_requests` + `routers.portal_entitlement`) with Doc04/Doc05/Doc11/Doc12 SRR canon citations · FE-WIRING-READY-2 remediation R-tag flags pod_shell mount pending.
10. **MOD** `backend/tests/invariants/baseline_failures.json` — ratchet 5831 → 5852 (+21) both `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor`. New ratchet_history entry appended (`at_utc=20260921T083000Z` · delta=+21 · specialist_dispatch_drift_carried_forward=3).

Zero sealed-file edit outside this-wave. Sealed R-99 canon_rules_registry + R-98 canon_rules_service.rbm_roc_vocabulary + R-97/R-96 canon_dap_lifecycle vocabularies + R-95..R-88 seal chain all continue verbatim GREEN.

---

## FE-WIRING-READY-2 handoff flag RAISED

Per owner directive verbatim this-session (2026-09-21T~07:50Z at scope-delta reply · CONDITION 4 framing): *"Then raise FE-WIRING-READY-2 with the COMPLETE endpoint list and I dispatch ONE specialist pass wiring everything (write paths + rbm-8 countdown surface + canon-rule displays together)."* + owner CONTINUITY BUNDLE new standing rule (2026-09-21T~08:10Z).

### Combined FE-WIRING-READY-2 endpoint dispatch list (R-99 + R-100 · 14 endpoints)

#### R-99 read-only public canon rules (5 endpoints · no auth · no per-tenant scope)

Prefix: `/api/canon/rules`

| # | Method | Path                              | Purpose                                                   |
|---|--------|-----------------------------------|-----------------------------------------------------------|
| 1 | GET    | `/dap`                            | 38-rule closed DAP registry                               |
| 2 | GET    | `/dap/{rule_id}`                  | Single DAP rule by ID (404 on unknown)                    |
| 3 | GET    | `/rbm`                            | 23-rule RBM registry                                      |
| 4 | GET    | `/roc`                            | 11-rule ROC registry                                      |
| 5 | GET    | `/rbm-8-ceremony-mechanic`        | R-91 live evidence receipt · FE-critical anchor           |

**Binding constraint for FE (inherited from R-99 seal report · §6.6)**: Any FE portal write-path R-91-countdown surface MUST consume `GET /api/canon/rules/rbm-8-ceremony-mechanic` **BYTE-VERBATIM** — no client-side rewriting of `r91_live_evidence_horizon_utc`, `ceremony_window_is_rigid`, or `no_shortening_path_in_code`. The countdown surface displays what the endpoint returns.

#### R-100 portal write/read (9 endpoints · JWT-gated · principal-scoped via PRIN-11)

Prefix: `/api/portal`

| # | Method | Path                                     | Purpose                                                              |
|---|--------|------------------------------------------|----------------------------------------------------------------------|
| 1 | GET    | `/requests`                              | Principal-scoped request history list (DAP-24 queryable)             |
| 2 | GET    | `/requests/{request_id}`                 | Principal-scoped request detail (DAP-15/DAP-35 discipline)           |
| 3 | POST   | `/requests`                              | Submit new extraction request (DAP-18/14/21 + invoke() chokepoint)   |
| 4 | POST   | `/requests/{request_id}/stop`            | Request-scoped stop · Executing → Stopped (**NOT party_halt**)       |
| 5 | POST   | `/requests/{request_id}/retry`           | Bounded-3 retry · hash-identical objective (R-78)                    |
| 6 | GET    | `/entitlement/licence`                   | Principal-scoped Licence read (ENT-5..8)                             |
| 7 | GET    | `/entitlement/catalog/listed`            | CatalogRow status=listed (ENT-9)                                     |
| 8 | GET    | `/entitlement/allowance`                 | Derived allowance from Ledger events (ENT-22 · no cache)             |
| 9 | GET    | `/entitlement/badges`                    | Picker badges filtered through dial-admit gate (ENT-3+ENT-43)        |

### Auth requirements (R-100 · all 9 endpoints)

- **JWT required** on every request. Use `Authorization: Bearer <access_token>` obtained via existing `POST /api/auth/login` → refresh flow.
- **No header-identity anywhere**. `X-Akki-App-ID` is FORBIDDEN on portal routes (grep-negative invariant `test_r100_condition1_portal_routes_never_read_x_akki_app_id_header`). Owner verbatim (2026-09-21T~07:50Z CONDITION 1): *"PRIN-12 forbids exactly that, and R-100 must not inherit it. Every new route derives the principal through PRIN-11's propagation; a request with no resolvable principal refuses, no default actor."*
- **Unauthenticated 401**: A request without a valid JWT gets 401 (or 403 for wrong-scope-type tokens like `worker_jwt` on a portal route). No default anonymous principal.

### Owner CONDITION constraints binding the FE specialist (inherit without interpretation)

Per user directive this-session: "include the owner-condition constraints that bind the FE, so the specialist inherits them without interpretation":

- **(a) Stop is request-scoped** — the confirm copy used on the stop CTA MUST be the request-scoped text (`"Stop this request? What's run so far will still be billed; nothing further will execute."` byte-verbatim from `POST /requests/{request_id}/stop` response `confirm.confirm_copy`), NEVER party-halt framing (never "Halt this party", "Stop all requests", etc.). CONDITION 2 owner verbatim: *"party_halt stays behind the owner surface. A requester must never be able to halt a party, including their own."*
- **(b) List/detail screens NEVER render approver identity** — the requester portal MUST NOT display `approver_email`, `approver_name`, `approver_user_id`, `decided_by_email`, `decided_by_name` (DAP-15 discipline · grep-negative invariant on router source guarantees the shape). Only authority, decision, reason are surfaced; the identifier of the human approver stays hidden.
- **(c) No reason line implies remaining budget** — no visible text (reason, badge, subheading, tooltip) on portal surfaces may compute or display *"credits remaining"*, *"budget headroom"*, *"credits left"*, *"remaining budget"*. DAP-35 + owner CONDITION 4 verbatim: *"no reason line implies remaining budget"*. Allowance state from `GET /entitlement/allowance` is a derived FIGURE for display; it must not be rewritten into a *"remaining"* implication or arithmetic difference in reason lines.
- **(d) Badges render ONLY licence-admitted rows** — the picker's `GET /entitlement/badges` output is already filtered through `_dial_admits_access_class` against the principal's licence dials. FE MUST render exactly what the endpoint returns — excluded rows are ABSENT from the payload, NOT greyed out or "locked" in the picker. ENT-3+ENT-43 verbatim: *"Badges show ONLY rows the licence's dials admit — excluded rows do not appear"*.
- **(e) R-91 countdown surface** consumes `GET /api/canon/rules/rbm-8-ceremony-mechanic` BYTE-VERBATIM (no client-side rewriting of the JSON keys `r91_live_evidence_horizon_utc` / `ceremony_window_is_rigid` / `no_shortening_path_in_code` / `r91_is_live_evidence_receipt`). SO §6.6.
- **(f) JWT flow only** via `POST /api/auth/login` → `POST /api/auth/refresh`. No `X-Akki-App-ID` header anywhere in the portal FE code. Grep-negative test enforces the invariant on the router source; FE code must match.

### Sample payloads (verbatim from live sweep run1 shape · stub bodies)

#### `POST /api/portal/requests` — submit
```json
Request:
POST /api/portal/requests
Authorization: Bearer <access_token>
Content-Type: application/json
{ "objective_text": "...", "units": [...] }

Response (202 Accepted):
{
  "outcome": "accepted",
  "principal_id": "<sub from JWT>",
  "authority": "DAP-18 frozen objective + DAP-14 approval routing + DAP-21 metered event + invoke() only via chokepoint",
  "next_step": "orchestration_delegated_to_sealed_services"
}
```

#### `POST /api/portal/requests/{request_id}/stop` — request-scoped stop
```json
Request:
POST /api/portal/requests/req-abc-123/stop
Authorization: Bearer <access_token>

Response (200 OK) [when request was Executing]:
{
  "request_id": "req-abc-123",
  "new_state": "Stopped",
  "confirm": {
    "request_id": "req-abc-123",
    "confirm_copy": "Stop this request? What's run so far will still be billed; nothing further will execute.",
    "figure_present": false,
    "percentage_present": false,
    "amount_present": false,
    "scope": "request"
  },
  "authority": "R-100 CONDITION 2 · request-scoped terminal transition"
}

Response (409 Conflict) [when request is not currently Executing]:
{ "detail": "<IllegalTransition reason>" }
```

#### `POST /api/portal/requests/{request_id}/retry` — bounded-3 retry
```json
Request:
POST /api/portal/requests/req-abc-123/retry
Authorization: Bearer <access_token>
(no body · fresh objectives forbidden · hash-identical original objective used)

Response (200 OK):
{
  "request_id": "req-abc-123",
  "max_attempts": 3,
  "retry_service_reference": "services.dap_lifecycle.retry_service.attempt_retry",
  "authority": "R-100 CONDITION 4 · retry re-runs every gate from failed stage forward, hash-identical objective, bounded three, each attempt receipted (R-78)",
  "sealed_exception_class": "RetryRefused"
}
```

#### `GET /api/portal/entitlement/allowance` — ENT-22 per-call derivation
```json
Request:
GET /api/portal/entitlement/allowance
Authorization: Bearer <access_token>

Response (200 OK):
{
  "principal_id": "<sub from JWT>",
  "allowance_state": {
    "licence_terms_id": "stub-<principal_id>",
    "period_iso": "2026-09",
    "credits_allowance": 0,
    "credits_debited": 0,
    "credits_remaining_deprecated": null
    // shape from sealed LicenceAllowanceState.model_dump()
  },
  "authority": "ENT-22 · derived from Ledger events only · no cache · no stored counter"
}
```

#### `GET /api/portal/entitlement/badges` — dial-admit filtered picker
```json
Response (200 OK):
{
  "principal_id": "<sub from JWT>",
  "badges": [],
  "count": 0,
  "authority": "ENT-3 + ENT-43 · picker badges filtered through licence compute_dial + frontier_dial admission gate"
}
```

#### `GET /api/portal/requests` — DAP-24 principal-scoped history
```json
Response (200 OK):
{
  "principal_id": "<sub from JWT>",
  "rows": [],
  "count": 0,
  "authority": "DAP-24 · Cumulative extraction history queryable"
}
```

#### `GET /api/portal/requests/{request_id}` — DAP-15/DAP-35 discipline
```json
Response (404 Not Found · stub in this wave):
{
  "detail": "Request not found (or not scoped to principal): <request_id>"
}
```

#### `GET /api/portal/entitlement/licence`
```json
{
  "principal_id": "<sub from JWT>",
  "licence": null,
  "authority": "ENT-5..8 · Licence terms object · Licence shape sealed"
}
```

#### `GET /api/portal/entitlement/catalog/listed`
```json
{
  "principal_id": "<sub from JWT>",
  "rows": [],
  "count": 0,
  "authority": "ENT-9 · CatalogRow status listed only"
}
```

**Note on stub bodies**: Rows/detail responses are STUB (empty lists / 404) in this wave. Full Ledger integration + Licence lookup + request record retrieval lift in the follow-on `lifecycle-integration` slice (post-R-100). Shape is stable — FE wires against these envelopes NOW; the endpoints will return live rows without shape drift.

---

## CONTINUITY BUNDLE (new standing rule this-session)

Per owner ruling this-session verbatim (2026-09-21T~08:10Z at R-100 approval reply): *"Continuity bundle scope: ALL THREE local-only repos, not code only. The owner's purpose line is 'a state that can be reconstructed from outside the sandbox' — reconstruction needs the state repo (master: DECISIONS/PINS/OBJECTIVES/receipts) and the FE repo (/app main: specialist commits, also zero-remote) as much as the code branch. Bundle each (code programme/track-a · state master · /app main), sha256-pin all three in STATE/PINS.md at the R-100 seal and every seal thereafter."*

Bundle export lands as **Commit-C fixup artefact** this-wave. sha256 pins land in `STATE/PINS.md` under a new `<!-- CONTINUITY-BUNDLE-PINS -->` block.

### Continuity Bundle plan (Commit-C fixup)

| Repo                          | Workdir                                      | Branch              | Bundle file (relative to /app/assessment_workspace/) |
|-------------------------------|----------------------------------------------|---------------------|-------------------------------------------------------|
| code                          | `repos/Extraction-Akki`                      | `programme/track-a` | `continuity_bundles/code_20260921T083500Z.bundle`     |
| state                         | `.` (assessment_workspace root)              | `master`            | `continuity_bundles/state_20260921T083500Z.bundle`    |
| FE (POD audit mirror)         | `/app/frontend`                              | `main`              | `continuity_bundles/fe_20260921T083500Z.bundle`       |

Zero push · zero remote configured · local export only per owner scope.

---

## R-91 posture unchanged

R-91 CP-APP-JS-UNIFY Phase 2 remains PARKED at frozen horizon `2026-09-23T03:23:15Z` (~42.9h out at this seal · verified `date -u` = 2026-09-21T~08:35Z). RBM-8 ceremony-mechanic invariants encoded at R-98 Commit-A `38eeef6c` continue to surface byte-verbatim at `GET /api/canon/rules/rbm-8-ceremony-mechanic` via R-99 Commit-A `eb40fb67`. Sprint bounds unchanged.

---

## COMPLETION SPRINT PROGRESS

Step 1 Family C ✅ (R-96 + R-97) · Step 2 Family D ✅ (R-98) · Step 3 OPEN-CARD SWEEP ✅ (state-only `fad511a7`) · Step 4 LIFECYCLE/ENTITLEMENT HTTP SURFACE ✅ (R-99 read surface + **this R-100 write surface**) · Steps 5-6 pending (R-91 ε-APPLY at horizon · NO EXPEDITE · then FINAL CLOSURE REPORT state-only).

---

## Autopilot next

(a) **Commit-B state master this-turn** — banks Commit-A `39412d09` + this seal report + DECISIONS append + NEXT R-100 IN-FLIGHT marker + STATE/PINS.md commissioning_record refresh.
(b) **Commit-C fixup state master next-turn** — R-6 boundary regen advancing `heads_last_sealed.state_repo.head` from `58685080` (R-99 Commit-B) to this-Commit-B + new `code_repo:` entry for R-100 Commit-A `39412d09` in ORCH_BOOT.md + POD audit mirror byte-identical sync + **Continuity Bundle export (3 bundles) + STATE/PINS.md sha256 pins for all 3**.
(c) **FE-WIRING-READY-2 dispatch** — this seal report is the artifact. All 14 endpoints (R-99 5 + R-100 9) + auth + sample payloads + 6 CONDITION constraints inheritance ready.
(d) **Residual scan** — none pending after this R-100 wave (COMPLETION SPRINT step 4 fully covered by R-99 + R-100).
(e) **R-91 ε-APPLY** at first boundary after `2026-09-23T03:23:15Z` (`date -u` checked each seal · NO EXPEDITE · rigid per RBM-8/SER C.5 I-4/SO §6.6).
(f) **M1-to-date BUILD_JOURNAL closure state-only** as final act (COMPLETION SPRINT step 6).

## Standing bounds

zero push · zero remote configured · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo discipline (code=`programme/track-a` · state=`master` · POD audit mirror=`main` at `/app/frontend/`) · ratchet monotonic-up floor **5852** · R-91 PARKED horizon `2026-09-23T03:23:15Z` NO EXPEDITE · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · R-88+ OWNER-RATIFICATION-PENDING RETIRED at `a30db4f7`.

**End of R-100 CP-PORTAL-WRITE-SURFACE seal report.**
