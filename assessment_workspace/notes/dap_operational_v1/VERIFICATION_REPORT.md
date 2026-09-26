# DAP operational continuation — verified scope, 2026-09-26

## Outcome, not a platform-completion claim

The acknowledgement-only DAP request endpoints have been replaced with durable
intent records and shared OS/DAP projections. Live execution remains **HELD**, not
complete. No GPU/provider access, source extraction, licence seed, approval grant,
new account, external model call, or billable usage occurred in this continuation.

## Implemented links

| Work item / Canon | Input → reused capability → output | Status / next gate |
|---|---|---|
| NORTHENA-DAP-RECORD / DAP-15/18, Ledger v1 | Existing identity + server membership + strict operation/objective/source refs → sealed state transitions + CommissionedJob + canonical emitter/writer → one insert-only Mongo envelope containing exact17-field row + hash-bound payload | **Verified** durable intent/replay/read projection; not a dispatcher |
| NORTHENA-DAP-ACTIONS / DAP-17/19/28 | Stored state → existing lifecycle guard → unknown404 or ineligible409 | **Partial**; no cancellation receipt/approved retry/execution/results invented |
| OS-DAP-WORK / owner prototypes | Same request/work ID → original model bindings → request compose/history/drawer, `/dap/requests`, `/os/work/tasks` | **Verified for held records**; successful execution/action states await real upstream events |
| LICENCE-READ / ENT-5/6/16/21/22/24/39 | Server-scoped Ledger membership/licence/catalog/meter events → sealed Licence/CatalogRow/MeteredEvent/allowance derivation → return-only LicencePortalView | **Partial**: live absent records unresolved. Positive/suspension/expiry/dials/event-time-rate/seat-pool tests use TEST-ONLY injected records. Admission/ceremony producers not connected; rollover/ceilings/keys/chokepoint dispatch not proved |
| SKILL-QUERY-SAFETY / TF-E4, D07 | Strict query → existing governed skill gate → banked SKILL_EXECUTOR_UNADMITTED refusal | **Verified safety** in tests; actual admitted skill positive gate is MOCKED. Real answers/executor still **blocked/unwired**, not simulated |
| SESSION-CONSUMER / scope isolation | Existing JWT token → abortable overview read only when signed in → no stale identity render | **Verified** operator/sign-out/analyst transitions. No token/password/session-issuance changes |

### Architecture and preservation
- New service composition: `services/northena/portal_work.py`,
  `services/portal_operational/{models,access,actions,entitlements,skill_query}.py`.
- New Mongo adapter inside `services/ledger_writer/mongo_control.py`; additive
  producer inside `services/ledger_emitter/emit_intent.py`. Unique tenant-sequence
  and command indexes enforce compare-and-append and replay. No request updates,
  cached balances or new billing store. Mongo `_id` excluded from reads.
- The legacy Northena writer was NOT used as an atomic authority: its existing
  best-effort mirror swallows failures. It and all sealed writer/kernel bodies
  remain unchanged. New adapter uses the canonical frozen v1 row, not the legacy
  schema, and stores payload+row atomically in `ledger_v1_control_events`.
- `/api/portal/requests`, `/submit`, `/work`, `/{id}`, stop/retry/result routes and
  `/api/os/work[/{id}]` share one record. Frozen request transitions are
  Compose→Submitted→Routing with `ADMISSION_UNRESOLVED`. The sealed machine has no
  Routing→Blocked edge: no invented transition was introduced.
- No attempt to paper over missing operation rights/approver/license/executor.
  `permitted_actions=[]` while routing; stop/retry/result refuse instead of fake
  success. Repeated request replay does not append another commission.
- Owner generated JSON and OwnerMarkup renderer unchanged; only existing bindings
  and containment/accessibility CSS changed. Responsive objective wrapping, menu
  overlap and unverified-label contrast were checked on actual long records.

## Tests and receipts

1. Initial RED reproduced: **16 failed / 1 passed**.
2. Initial GREEN: **17 passed**. Expanded portal: **31 passed**.
3. Combined after initial corrections: **134 passed / 2 skipped**.
4. Final combined portal+census, twice: **146 passed / 2 skipped each**.
   Skips are deliberate live census/GPU drill opt-outs. They were NOT executed.
5. Frontend production build passes (final source); Python compile check passes.
   Standalone ESLint could not run: repo lacks ESLint9 flat config. No false lint
   pass is claimed; build/compiler and browser checks supplied verification.
6. Live HTTP exercises cover persistence, idempotent concurrency, body conflicts,
   scoped read/refusals, spoofed fields, frozen hashes, canonical row fields and
   actual negative skill gates. Unit faults, positive entitlement grants and skill
   gate admission fixtures are **MOCKED / TEST-ONLY**, not executed business work.
7. Browser: submit→drawer→reload→DAP history→OS same identifier; analyst disabled;
   unresolved terms. Main follow-up checked real operator→sign-out→analyst
   transitions (4 overview200, 0 overview401, no operator history for analyst).
8. Actual longest objective: mobile390 and desktop1920 `OVERFLOW[]`; mobile
   objective scrollWidth337/clientWidth337/height622 proves wrapping, not merely a
   page-width check. Drawer close restores navigation. Initial test harness
   loading screenshot/case-sensitive label/wrong close locator were corrected;
   retained final receipts distinguish harness failures from application bugs.

Bank: `assessment_workspace/phase0/drill_receipts/dap_operational_v1/`.
`VERIFICATION_RECEIPT.json` verifies the actual Mongo tenant chain using the sealed
verifier and every payload digest; `MANIFEST.json` hashes copied reports, logs,
screenshots and browser scripts. No credentials or token values are in the JSON
receipts. The existing demo passwords in test scripts are documented test accounts.

## D01–D12 acceptance reconciliation

| ID | Status | Evidence / boundary |
|---|---|---|
|D01|Verified scoped slice|Existing operator/analyst/anonymous + source/tenant/extra-field refusal tests; no new authority assumed|
|D02|Verified|Frozen exact objective/hash/scope, durable row, same-key replay and conflict|
|D03|Partial|Concurrent commissions/unique sequence and ledger-outage fail-close tested. No approval or terminal-transition coordinator yet|
|D04|Open|Approval not inferred; recorded approver authority/decisions and approval UI remain unwired|
|D05|Partial|Actual-state refusal correct; executing cancellation and bounded approved retry not implemented|
|D06|Partial|Held commissioning receipt exists; no real admitted operation dispatch|
|D07|Partial|No fake results/class/answer, retrieval refuses. Successful rights/checksum-gated retrieval remains open|
|D08|Partial|Same held work/history in both prototypes verified; full approval/command/result controls remain open|
|D09|Partial|Live unresolved truth and projection fixtures verified; real owner-admission/ceremony producers missing|
|D10|Partial|Derived event-time rates, seat/pool/org filters tested; no actual metered business operation/rollover proof|
|D11|Verified changed views|Original JSON/renderer source equality, test IDs and loaded mobile/desktop containment checked; not all888 actions|
|D12|Verified scoped slice|Repeat tests/live API/browser/receipt banking complete; owner review pending|

**4 verified + 7 partial + 1 open of the12 scoped acceptance items**; this is
not a percentage-complete platform or a claim that partials are functional end to
end. The wider OS/DAP action-to-Canon map is still in progress.

## Next actions

P0: durable owner membership/licence/ceremony and operation-approval records;
derive admission per operation; admitted engine dispatch/receipts; cancellable
executing state; approval-bounded retry; verified output/retrieval. These must be
Akki-owned integrations, never E1 data-path work.

P1: finish full action-to-Canon/component mapping; real callable executor through
the existing chokepoint and grounded evidence-derived class; entitlement
rollover/ceilings/catalog provenance/credential gates and measured usage surfaces.

P2: Solva reasoning, Mkondo handoffs, Targeta/CIF learning, governed model/audio/
training workflows. AISCA/GPU recovery stays parked until the owner reopens it.