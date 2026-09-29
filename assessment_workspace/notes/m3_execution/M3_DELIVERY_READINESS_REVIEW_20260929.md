# M3 — A request becomes completed, delivered work: readiness review (step 1 of 3)

29 September 2026. Owner directive: "Do a deep review of the various features, the orchestration engine,
etc. and check if you have touched all the key touch points … build universally so the orchestration
takes the shape of its context in case it changes from one domain area to another."
Governing source: `Akki_Goal_Roadmap_v1.md` §M3 (M3.1–M3.4, M3-T1–T5, Gate G3). Design sources read in
full before this note: Canon 3 (Northena/SyniSense, admit → gate → converge → ledger, outer gate,
entitlement), Canon 4 (the chain, the unit, batching/holds/ceilings, two services/two seams, economics,
model ladder, quality matrix), Canon 6 §6–§7 (commissioning, mining and delivery), Canon 7 Part II–III
and VII (admission fork, async contract, idempotency, cancellation, Function & Promise Registry),
Canon 9 (record matrix, task identity, handoff contracts), Canon 5 §13–§18 (Extraction Console).

**This is a review, not a close.** Nothing below is implemented yet; every "exists" claim is a file read
or a live probe made this run, and every "held" claim was measured against the running preview.

## 0. The one finding that shapes M3

Akki today has **two execution paths that never meet**:

| Path | What it is | Live state (measured 29 Sep) |
|---|---|---|
| **A · Northena Coordinator** (`services/northena/execution_*`, `activation/*`, `custody_delivery/*`, `mtafiti/execution_registry.py`) | The canon-grade orchestration engine for a commissioned request: frozen `Request` → signed `Plan` → independent approval groups → atomic `Reservation` → worker limit acknowledgement → outbox `send` → observation → independent artifact inspection → registry publication → metering → terminal → custody delivery. ~2,500 lines, ~120 named hold reasons, every seam typed and fail-closed. | **Contract-complete, zero live bindings.** `AKKI_NATIVE_RUNTIME_FACTORY` is unset, so `app.state.execution_bindings` is never installed. Every `advance` on the 1,373 recorded operator requests ends in `EXECUTOR_ADAPTER_UNBOUND` / `ADMITTED_SIGNER_RESOLVER_UNBOUND` / `ADMISSION_UNRESOLVED`. No request has ever executed. |
| **B · census_autonomy operational path** (`deep_dispatch.py`, `jump_dispatch.py`, `deep_bundle.py`, `deep_worker.py`, `remote_dispatch.py`, `operational_store.py`) | M1's real off-E1 worker path: reviewed code bundle shipped over pinned SSH, control JSON on stdin, digest-verified `cwr-` receipt, read-only SQL guard, pull seam through the jump host, cursor/transport files as durable state. | **Live and proven** (20 db / 1,013 tables / ~239.6 M rows censused on akki-vm through the jump host). But it is *outside* the Coordinator: no signed receipts, no reservation, no metering, no custody, no DAP/My Work identity. |

**M3 decision: bind A to B's transport; do not fork a third path.** The Coordinator is the orchestration
engine the canon specifies (Canon 3 §5, Canon 4 §32, Canon 9 §6 "Admission → extraction"); the census
transport is the only admitted way bytes move (E1 is never the data path). M3 supplies the *native
runtime* the Coordinator was built to receive — an admitted-signer resolver, a source executor adapter
that speaks path B's SSH discipline, an independent inspector, a custody provider — and the commission
ceremony that produces the signed `Plan`/`Approval`/`Allocation`/`Worker` receipts it requires. Nothing in
`execution_coordinator.py` changes.

## 1. Touch-point crosswalk — what the owner named, what the canon requires, what exists, what is held

Legend: **EXISTS** = read and reusable as-is · **PARTIAL** = exists but not wired to the live path ·
**HELD** = correctly refuses today; M3 must connect it · **ABSENT** = M3 must build it.

### 1.1 Work-order packaging and definition

| Canon requirement | Where it lives | State |
|---|---|---|
| Frozen governing artifact: identity, version, scope set, floor, done-condition, budget, lawful basis (C3 §6.2) | `northena/execution_models.Request` (kind · engine · objective_sha256 · input_refs · scope_refs · deadline · result_floor); `northena/admit.py` `compile_and_freeze` with the five refusal reasons (`missing_lawful_basis`, `scope_unresolved` …); `portal_work.submit` freezes objective/units/operation idempotently | **PARTIAL** — `portal_work.submit` freezes the DAP request but never writes a Northena *admit* row with a lawful-basis reference; `admit.py` is only reached from the ThinkLab surface. Budget and done-condition are not captured at submit. |
| Case-agnostic work order: kind registry, opaque scope, output contract, dispatch intent, precondition seals | `work_supervisor/job_manifest.JobManifest v0` + `kind_registry` (sole seed `platform.generic`) | **EXISTS, unused** — nothing produces a manifest. This is the universal shape M3 adopts (§3). |
| Plan carries limits per dimension, purposes, approval groups, allocation, worker, terms, policy/dial versions, grace | `activation/record_shapes.Plan` (dimensions: spend · wall_clock · scanned_records · returned_records · bytes_read · active_compute · media_duration) | **EXISTS** — no producer. |
| Descriptor bridges per kind | `northena/execution_builders.{source,skill,training,evaluation}_request` | **EXISTS** — `source_request` still shaped for census (`connect_source_descriptor`), needs an *extraction* descriptor (bounded region/table + floor + output form). |
| Reviewed code, never data, crosses to the worker | `census_autonomy/deep_bundle.build_bundle` (15 pinned modules, sha256 of the zip is part of the receipt) | **EXISTS** — extend the module list with the extraction worker; the code hash discipline is reused unchanged. |

### 1.2 Orchestration (dispatch → observe → complete → deliver)

| Canon requirement | Where it lives | State |
|---|---|---|
| One submit claim; uncertainty resumes by stable key; at-most-once effect; cancel arbitrated on the same slot (C4 §32, C7 §15–16) | `execution_coordinator.Coordinator` (`dispatch`, `send`, `observation:*`, `worker_outcome`, `terminal`, `cancel_intent` slots on the *same* canonical ledger via `execution_journal.LedgerJournal`) | **EXISTS** |
| Pre-send gate recheck (authority, commercial terms, eligibility, limits) then atomic outbox | `execution_send.claim_send` / `cancel_unsent` | **EXISTS** |
| Worker limit acknowledgement before any effect | `activation/worker_gate.WorkerLimitGate` → `executor.admit_limits_rpc` → signed `Observation(category=runtime)` | **HELD** — no executor exposes `admit_limits_rpc`; no worker signs. |
| Result verification before publication; failed verification still meters consumed work | `execution_completion.complete/meter/terminal`; `mtafiti/execution_registry.CanonicalRegistry.verify` (inspector receipt → `AssetRegistryRecord` → Mtafiti writer) | **HELD** — `ARTIFACT_INSPECTOR_NOT_BOUND`. |
| Handoff contracts for non-source kinds | `mkondo/execution_handoff`, `execution_delivery`, `registry.py` | **EXISTS** — skipped for `kind == source` by design; M3-T1 is a source kind. |
| Warm/fresh fork made once at admission (C3 §7, C7 §4) | `northena/gate.route` (ThinkLab); nothing on the DAP path | **ABSENT on DAP path** — M3.1 feasibility must run the membership + convergence check against the Registry and record `warm`/`fresh`/`refuse` once. |
| Requester controls: stop, retry-under-same-identity, result | `portal_operational/actions.py`, `routers/portal_requests.py` (`/execution/advance`, `/stop`, `/retry`, `/result`) | **EXISTS** |
| Custody delivery: grant is a capability, completion is measured, never fetch/stream in E1 | `custody_delivery/{service,ports,models,evidence,ledger}.py`, `routers/custody_delivery.py` | **HELD** — `CUSTODY_PROVIDER_UNBOUND`; provider requires exact HTTPS origins (`origin_of` refuses IPs/localhost). |
| Thin webhook, governed fetch, polling fallback (C7 §14) | none | **ABSENT** — My Work polls `GET /api/portal/requests/{id}`; acceptable for M3 (polling is the canon fallback), webhook registration belongs to Integration Console. |

### 1.3 Resourcing (who does the work)

| Canon requirement | Where it lives | State |
|---|---|---|
| Worker of record is admitted, identified, and bound to its runtime id/version | `record_shapes.Worker` receipt (runtime_id, executor_version, kinds, enforced_dimensions, `implementation_workspace_touched_data: False`); `census_autonomy/worker_inventory.refresh` (live telemetry from akki-vm, akki-vm-ii, non_gpu_jump); `execution_identity.verify_identity` (pinned SSH identity receipts) | **PARTIAL** — inventory is live; no `Worker` receipt has ever been signed/recorded. |
| Placement is declared, not inferred | `JobManifest.dispatch_intent` (`ssh_host_slug:X` \| `gpu_lane:Y` \| `local`); `operational_scope.validate_submission` (`worker_id` ∈ `non_gpu_jump` ∪ `list_hosts()`) | **EXISTS** — M3 refuses `local` for any data-touching kind (E1 is never the data path). |
| Jump-governed sources reach only through the pull seam | `deep_dispatch.JUMP_GOVERNED_SOURCES`, `pull_seam_hop` | **EXISTS** |
| Fleet apportionment is versioned configuration (C4 §39) | `economics/fleet_policy.py` | **EXISTS** — not consulted by any live dispatch. |

### 1.4 Resource management (ceilings, reservations, termination)

| Canon requirement | Where it lives | State |
|---|---|---|
| Budget ceiling is a hard stop; nothing past it is billed (C3 §8, C4 §32) | `activation/reservations.Reservations.reserve/settle` (atomic append-at-head, `ALLOCATION_CAPACITY_EXCEEDED`, settle only from a signed terminal measurement, overrun never erased); `runtime_limits.RuntimeLimiter.before_batch` (charge upper bounds *before* reading) | **EXISTS** — no `Allocation` receipt exists for RMS, so nothing can reserve. |
| Termination window inside the ceiling; worker stops measuring before E1's deadline | `RuntimeEnvelope` (starts/stop_work_by/terminate_by), `deep_dispatch` margin discipline | **EXISTS** |
| Interruption: checkpoint, idempotent re-dispatch, completion judged from durable artefacts | Coordinator slots + `guard_terminal`; `dap_lifecycle` `Interrupted` state and `retry_service` (bounded auto-retry DEFAULT 3) | **EXISTS** — worker-side checkpointing for extraction is **ABSENT** (census worker checkpoints only the NAS frontier). |

### 1.5 Quality assurance

| Canon requirement | Where it lives | State |
|---|---|---|
| Five-ring unit is the only intake contract; unqualified units never enter evidence partitions (C4 §30–31) | `contracts/five_rings.NormalizedUnit` (provenance · signal · relational · reextraction_handle · defensibility, `matrix_rule_ref`, `runtime_mode`) | **EXISTS** — no producer for structured records. |
| Verdict is a governed matrix lookup with its rule ref; declaration baseline floors; overlay gated | Mtafiti qualification matrix, declaration baseline (M1 Registry) | **EXISTS** for census; extraction must stamp each unit's `DefensibilityRing` from the *same* Registry measure, never re-derive. |
| Tier-one deterministic checks at write: schema completeness, referential integrity, statistical tripwires (C4 §49) | `non_gpu_governance/quality.py` (`QualityPack`, `QualityRegister` reconciliation), `census_dq_producer.py`, `deep_sql.observe` (null/PII/duplicate/language counts) | **PARTIAL** — measurements exist at census grain; per-batch tripwires on an extraction output are **ABSENT**. |
| Structured/tabular row: per-connector mapping proven on a human-verified sample before publish (C4 §45) | none | **ABSENT** — M3-T1's first table is the activation event for this matrix row; its threshold is *set at activation from measurement*, not invented. |
| Held batch renders on the run with rail + evidence; single-reviewer resolution (C4 §32) | Watch commission gates (M2) render holds; `dap_lifecycle/blocked_kinds` | **PARTIAL** — extraction batches do not yet emit holds. |
| Independent inspection of the artifact (hash, size, class) by a signer that is neither worker nor requester | `mtafiti/execution_record_models.InspectorReceipt`; `native_evidence` requires `independence` signer ∉ {worker, requester} | **HELD** — no inspector bound. akki-vm-ii is the natural independent re-performer. |
| Critic pass (tier two) never blocks; de-identification recall breach quarantines fail-closed | `critic_pass/*`, `rights_quarantine/*`, `de_identify/*` | **EXISTS** — not on the extraction path yet. |

### 1.6 Metering, price and usage

| Canon requirement | Where it lives | State |
|---|---|---|
| Cost is measured, price is shaped; every quote stamps its model version; learning-phase quotes are non-precedent (C4 §39) | `economics/{price_model,quote_service,delivery_time,instrumentation,expiry}.py` (versioned config, tier lock, capacity class, exploratory tier) | **EXISTS** — never invoked from the DAP path; no owner-supplied rate for structured extraction (`cost_ledger/rates.py` is honestly absent). |
| Actual usage → metered event, record-before-return, terms cited (DAP-21/22) | `execution_completion.meter` → `execution_usage.LedgerUsagePublisher` → `metered_event` rows; `dap/terms.resolve_terms` (party → custody class → estate default) | **EXISTS** — for `kind=source` with no catalogue row the publisher records `non_model_consumption_only` (usage banked, **no credit debit**). |
| Allowance and debits are read-only projections of the ledger | `portal_operational/entitlements.read_view`, `billing.debit` (debits reseller_frontier tokens only) | **EXISTS** — `demo.operator` resolves `ORGANISATION_UNRESOLVED` today: no `principal_membership` and no `entitlement_licence` record is banked for RMS. |
| Stop is charged only to the point of the stop, receipted | `dap_lifecycle/request_stop`, coordinator `meter` on cancelled/failed | **EXISTS** |
| Cancellation retains completed work; nothing partial egresses (C7 §16, C3 §20) | Coordinator terminal + custody `current()` gate | **EXISTS** |

### 1.7 Frontier-model cost reduction (the ladder)

| Canon requirement | Where it lives | State |
|---|---|---|
| Lowest rung that meets the promise; every rung-4 use answers "why not rung 3" (C4 §40) | `contracts/asset_registry.FunctionPromiseRow.ladder_rung`; `lowered_standard`, `baseline_line`, `serving_floor` | **EXISTS as registry fields** |
| Cascade builds only against demonstrated, metered cost pressure (C4 §43.4) | none | **Correctly ABSENT** — no threshold exists yet. |
| Chokepoint on any external model call; sandbox fixture vs production refusal | `chokepoint/*`, `gateway/*` | **EXISTS** |

**M3 ladder placement:** the whole M3-T1 path is rung 1–2. Structured-record extraction is
deterministic SQL + regex PII + `langdetect`; the shaping wizard's chat pane asks mandatory fields and
never proposes (Canon 5 §14) — that is a rung-1 field machine, not a model; refusal text is the closed
`hold_reasons` table. **No frontier call is admitted anywhere in M3.** The cost we avoid is recorded
as a ladder placement, not claimed as a saving.

### 1.8 Information governance

| Canon requirement | Where it lives | State |
|---|---|---|
| Lawful basis at Admit; purpose is an admission property (C3 §6.1) | `admit.py` validity sequence; `CENSUS_LAWFUL_BASIS_PATH` sha256 already in every census descriptor | **PARTIAL** on DAP path (§1.1). |
| Entitlement is ABAC over Mtafiti's sensitivity class (C3 §22.1, C7 §5.2 distinct refusal) | `entitlement_service_v1/{chokepoint_resolver,licence,catalog,allowance}`, `registry_surfaces.inventory` (`sensitivity: 'unmeasured'` per source) | **PARTIAL** — sensitivity is `unmeasured` for every RMS source; an unmeasured class must resolve *conservatively* (refuse or DPO route), never open. |
| De-identify before any boundary; PII miss is a governance event | `de_identify/*`, `mtafiti/detectors/pii_detector.py`, `pii_redaction_guard.py` | **EXISTS** — extraction must apply the custody floor per unit *on the worker*. |
| Outer gate five checks at export: rights, irreversibility, cumulative disclosure, licence issue, receipt (C3 §20) | `outer_gate/{transform,receipt,mint}.py`, `dap/disclosure_budget.py`, `dap/coalition.py` | **EXISTS** — not on the delivery path; cumulative arm is closed by construction (correct). |
| Rights withdrawal recalls descendants | `non_gpu_governance/{lineage,rights}.py` (`DESCENDANT_RIGHTS_WITHDRAWN`) | **EXISTS** |
| Read-only means read-only (M3-T5) | `readonly_sql_guard.refuse_if_write`; `deep_sql.executor` refuses anything without `information_schema`/`LIMIT` | **EXISTS** — M3 must additionally *prove* it: a write-attempt drill that is refused and receipted. |
| One record class, one writer (C9 §3) | `ledger_writer` (execution_flow · activation_receipt · activation_reservation · metered_event · dap_request) | **EXISTS** — M3 adds no new writer; custody rows already have a home. |

### 1.9 Admission and approval

| Canon requirement | Where it lives | State |
|---|---|---|
| Controlled → named approver; uncontrolled path gets no unnecessary approval (M3-T2, DAP-14/16) | `dap/approval.py` (in-memory `_ROUTES`, `DAP_R2_APPROVING_AUTHORITY = "DEFAULT-PENDING-OVERRIDE"`), `dap_lifecycle/approval_service.py`, `timer.py` (14-day expiry) | **PARTIAL** — routing kernel is process memory, not ledger; **approving authority for RMS is an open owner ruling (DAP-R-2)**. |
| Independent approval groups with quorum; latest decision per principal per group; revocation holds | `activation/approvals.approved_plan` (scope + expenditure groups mandatory; purpose groups per kind) | **EXISTS** — needs signers. |
| Approval resumes the same scoped job; denial preserves it with a reason (M3-T2) | Coordinator `advance` after `APPROVAL_GROUP_PENDING`; `Approval.decision=refused` | **EXISTS** |

### 1.10 Work history, DAP and My Work (the user-facing promise)

| Canon requirement | Where it lives | State |
|---|---|---|
| Commission wizard: chat + draft rail; entry/reach/output + envelope; mandatory fields asked never pre-filled; estate-check chip; Run a sample (C5 §14, §16) | `dapWorkModel.js` (objective text + source chips only), `journey_assistant/{never_pre_fill,estate_check_chip,three_verdicts}.py`, `wizard/objective_compile.py` | **PARTIAL** — no reach (table/region), no output form, no done-condition/budget/lawful-basis envelope, no feasibility, no sample. |
| Commit review: you supplied / agent assumed / feasibility verdict / grounding marker / envelope / Freeze (C5 §15) | none | **ABSENT** |
| Quote: line items, validity window, delivery range, cancellation liability (C6 §6) | `economics/quote_service.issue_quote` | **PARTIAL** — no surface. |
| Running list shows stage and budget consumed; batch board shows holds (C5 §13, C6 §7) | `osWorkModel.js` / `nexusWork.js` (state counts, history rail, receipt hashes) | **PARTIAL** — no execution phase, usage, artifact, or delivery rows. |
| Shelf: deliverable with contents, licence label, privacy attestation, quality card, proof trail (C6 §7) | `portal_operational/delivery_history.py` projects `delivery_*` slots into `WorkView` | **PARTIAL** — projection exists; no deliverable has ever existed. |
| Same identity in DAP, Registry and My Work after restart (M3-T5) | `work_id == request_id`; `work_snapshot.read_snapshot` | **EXISTS** |

### 1.11 The Watch (M2 obligation carried forward)

M3 adds commission gates — *commission*, *dispatch*, *deliver* — to the M2 gate inventory. Each must be
registered as a `commission_gate` boundary, evaluate mark state on every pass, and the G2 inventory
drill must be rerun before G3 closes (Canon 8 §10; M2 closure note §6 standing limit).

## 2. Probes made this run (evidence for the "held" cells)

```
POST /api/auth/login demo.operator                        → 200 (token 328 chars)
GET  /api/portal/entitlement/allowance                    → status=unresolved, ORGANISATION_UNRESOLVED
GET  /api/portal/requests                                 → 1,373 rows; every state=routing;
                                                            reasons ∈ {ADMISSION_UNRESOLVED,
                                                            EXECUTOR_ADAPTER_UNBOUND,
                                                            ADMITTED_SIGNER_RESOLVER_UNBOUND}
grep AKKI_NATIVE_RUNTIME_FACTORY backend/.env             → absent
grep -r "source_request(" (non-test)                      → no caller
kind_registry.list_kinds()                                → ('platform.generic',)
```

## 3. Universality — how the orchestration takes the shape of its context

The owner's instruction is already the canon's: *"the pipeline is the same whichever data
dimensionality the material belongs to … the layers, the unit contract, and qualification apply
identically"* (Canon 4 §28); *"the matrix is keyed by output class, never by media type, customer or
instance"* (§44); *"no instance is a development metric"* (§50). The shape M3 fixes:

```
Frozen Request (kind · engine · scope_refs · floor · deadline)          ← Northena, unchanged
        │
        ▼
JobManifest v0  { job_kind, scope (opaque), output_contract,            ← work_supervisor, unchanged
                  dispatch_intent, precondition_seals, depends_on }
        │   job_kind resolves through kind_registry to ONE KindProfile:
        ▼
KindProfile     { bundle_modules, worker_entrypoint, output_class (matrix row),
                  enforced_dimensions ⊆ Quantity.dimension, price_line_ref,
                  custody_floor_ref, jump_governed: bool, independent_inspector_kinds }
        │
        ▼
Plan receipt    { limits from Allocation ∩ quote, groups, purposes, worker_ref, terms }   ← activation, unchanged
        │
        ▼
Worker of record executes the bundle; emits Observation(runtime) · Observation(measurements) ·
Artifact refs; independent inspector emits InspectorReceipt; custody provider emits grant/completion.
```

What changes between domains is **only the KindProfile row** — the bundle it ships, the output class
it activates in the quality matrix, the dimensions it can enforce (`media_duration` for NAS audio,
`bytes_read` for OBS objects, `scanned_records` for RDS/MySQL), and whether it is jump-governed.
The Coordinator, the Plan, the reservation, the send/observe/terminal slots, the inspector contract,
the custody contract, the hold-reason table and the My Work projection do not know which domain
they are serving. M3-T1 registers `source.extract.structured_records.v1`; NAS (`media.transcribe.*`),
OBS (`object.enumerate.*`), DigiCow RDS (same structured kind, `rds_data` driver) register rows later
without touching the engine. Skill/training/evaluation kinds already have their own builders and
route through Mkondo. `dispatch_intent=local` is refused for every kind whose profile touches data.

## 4. Decisions the owner must make before M3.1 implementation

These are ruled values, not defaults I may pick (Canon 3 §22–23; M2 closure §5 precedent):

1. **Approving authority for RMS controlled operations (DAP-R-2, open since 2026-09-13).** Which admitted
   principal(s) form the *scope* group and the *expenditure* group for RMS? Proposed uncontrolled path:
   scope = {requester's operator standing}, expenditure = {`demo.master_admin` as budget holder}, quorum 1
   each; controlled path (raw download, fine-tune, skills, any controlled unit) adds the DPO group.
2. **Pilot principal membership and licence ceremony.** `demo.operator` has no banked
   `principal_membership`/`entitlement_licence`. I will bank them through the *existing* admission and
   ceremony producers with `admission_receipt_ref`s (never a seed that bypasses the writer). Confirm the
   organisation principal id for RMS and the terms identifier to cite.
3. **Custody delivery target.** The custody provider needs an exact HTTPS origin. Options: (a) worker
   pushes the sealed artifact to the tenant's own Huawei OBS bucket and the completion evidence is OBS's
   ETag/size — recipient retrieves under their own OBS identity; (b) an HTTPS artifact endpoint on
   akki-vm under a real hostname/certificate. (a) needs no new server and the bucket is already
   censused; (b) needs DNS + TLS you would have to supply. **Recommend (a).**
4. **Price model for structured extraction.** No owner rate exists. Proposal per Canon 4 §39: an
   *exploratory, time-boxed, non-precedent* model version (`v0-exploratory`, expiry stamped) with line
   items in measured units (scanned_records, returned_records, wall_clock) and a **zero credit debit**
   until you supply a rate — the quote still stamps its version and the usage is still metered.
5. **First bounded scope for M3-T1.** RMS MySQL, one table/region from the censused inventory, read-only,
   worker of record akki-vm through the pull seam, independent inspector akki-vm-ii. Name the table if
   you have a preference; otherwise I choose the smallest fully-measured table with no PII flags in the
   census sample and record the choice.
6. **Signing keys.** Each worker (akki-vm, akki-vm-ii) and each approver needs an Ed25519 identity
   admitted through the estate's admitted-signer resolver. Workers generate their keypair *on the host*
   (private key never leaves); approvers' keys are held in the same 0600 estate custody as the
   jump/OBS credentials. Confirm this custody arrangement is acceptable.

## 5. Proposed build order (step 2), each independently drillable

| Package | Builds | Drill |
|---|---|---|
| **M3.1a** Admission & ceremony | Native admitted-signer resolver (ledger-backed `AdmittedSigner` records via ceremony); bank RMS organisation, membership, licence, allocation, worker receipts through existing writers; `AKKI_NATIVE_RUNTIME_FACTORY` composition | allowance resolves; `Worker`/`Allocation` receipts verify; an unadmitted signer holds |
| **M3.1b** Shaping → freeze | Draft persistence; feasibility (Registry membership + convergence → warm/fresh/refuse, `unknown` on un-censused); commit review payload (supplied / assumed / verdict / grounding / envelope); commission = Northena admit row + `Plan` receipt + JobManifest + quote (exploratory version) | M3-T1 first half; M3-T4 widened intent → new version |
| **M3.2** Extraction worker | `source.extract.structured_records.v1` bundle: bounded SELECT … LIMIT under `refuse_if_write`, per-unit five rings from the Registry measure, PII floor applied on the worker, unqualified units partitioned out, checkpoint file, `RuntimeLimiter` coupled to a hard supervisor, signed runtime/measurements observations, artifact sealed on the worker; `BoundedEngineAdapter` (submit/status/cancel/admit_limits over pinned SSH); inspector on akki-vm-ii | M3-T1 second half; M3-T3 interruption; M3-T5 write-attempt refused |
| **M3.3** Delivery, metering, history | OBS custody provider (grant → completion with observed sha256/bytes); outer-gate five checks before grant; `LedgerUsagePublisher` line items; My Work / DAP at Registry depth: commission rail, running list with phase + budget consumed, batch/hold board, shelf with licence/quality/proof, delivery states | M3-T1 confirmed delivery; M3-T5 identity agreement after restart |
| **M3.4** Negative paths | Denied / expired approval; duplicate submit; refresh mid-run; revoked authority before send; late delivery race; refused writer displayed as hold | M3-T2, M3-T3, M3-T4 |
| **G3** | Rerun G2 inventory with the three new gates; testing agent full regression | Gate |

## 6. Standing limits stated now

- No frontier model is used anywhere in M3; the shaping "agent" is a rung-1 field machine.
- Structured-mapping quality thresholds are *set at activation from the first measured sample*, not
  written in advance; until then the quality card says "method stated, number pending".
- Delivery completion is proved by the custody provider's measured evidence, never by a link having
  been issued.
- Sensitivity for RMS sources is `unmeasured`; entitlement resolves conservatively until the census
  measures it.
