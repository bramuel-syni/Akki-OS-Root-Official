# Akki — M7 / M8 readiness run

**Date:** 2026-09-30 UTC · **Scope:** approved read-only requirements/repository assessment and bounded verification.

## Executive verdict

| Milestone | Verdict | Why |
|---|---|---|
| **M7 — correct tenant, rule, entitlement and commercial operation** | **NOT ACCEPTANCE-READY; ready for targeted implementation** | Native identity, licence reads, event-time billing and execution guards exist. The complete tenant-admin/rule-change/commercial journey is not connected or proven. Legacy rule-change state can become effective before its evidence write. |
| **M8 — failure, withdrawal, continuity and recovery** | **NOT ACCEPTANCE-READY; partial mechanisms available** | Execution recovery, rights checks and compaction have useful tests. Full dependency-failure drills, graph-wide withdrawal/recall, independently verified restoration and real notification delivery are not established by this run. |

**G7 and G8 are not passed.** No percentage completion is inferred from unit-test totals, old milestone seals, source-code presence or successful empty read views. The ten acceptance packs below remain open; this assessment does not reset previously proven component work.

User redirected the earlier M6/M9 request to **M7/M8** and approved the plan. No application behavior, auth configuration, rules, tenant business records or training jobs were changed by this assessment. No GPU/SSH calls, new commissions, live withdrawals, outage injections, service restarts or notifications were initiated.

## 1. Governing requirements and evidence boundary

- Governing roadmap: `assessment_workspace/notes/goal_delivery_20260928/AKKI_GOAL_ROADMAP_v1.md:320–362`, with `FAMILY_OWNERSHIP.json` and the existing 648-row gap inventory as navigation aids, **not fresh closure evidence**. Earlier milestones also named M7/M8 have different meanings.
- M7 sources: Doc 15; `Rules_Service_Spec_v1` (RBM-1–22 plus recorded rulings); `Rule_Origination_Classification_Criteria` (ROC-1–11); principal model PRIN-1–13; entitlement ENT-1–49; Governance Architecture and its gap register. Primary-family inventory maps 166 historical rows to M7; this is not a claim that all 166 were independently retested here.
- M8 sources: `Failure_Posture_Enumeration_v1` FP-1–4; `Business_Continuity_Annex_v1` BC-1–4 and S-10/S-11; shared Watch, Ledger, consumption, memory, rights and admission requirements. Eight primary-family historical rows do not describe the whole shared scope.
- Source text lives under `assessment_workspace/canon/drops/20260907/extracted/text/`, `.../20260909/extracted/text/` and `assessment_workspace/incoming/owner_closure_plan/supplement_2/`. Owner decision ledger takes precedence over old proposed/default values.
- Crucial recovery ruling: `STATE/DECISIONS.md:8528–8594` and `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md`. BC-3/BC-4 require a **dynamic tiered recovery policy**, not an invented blanket RPO. The packet is a proposal pending ratification/charter, not a deployed recovery service. Preserve the existing **3,600-second Ledger recovery objective** and **72-hour qualifying-breach notification window**.
- UI source of truth remains the banked owner Nexus/prototype experience and `canon/prototypes/20260928_owner_nexus/action_inventory.json`; a static page or a generic replacement is not completed interaction delivery.

This is a targeted milestone readiness run, not an exhaustive security audit, whole-repository code review, production-state inspection or a new M6/M9 completion judgment.

## 2. Four-repository review and reuse decision

All four public repositories were fetched/referenced and their current `main` heads read using `git ls-remote`. GitHub REST access returned403; pinned raw-source and codeload retrieval succeeded. Donor code was inspected, **not executed**. `SOURCE_MANIFEST.json` records source hashes, sample scope and identity comparisons.

| Repository / pinned main | Relevant evidence | Reuse decision |
|---|---|---|
| [Akki-Executive-Core](https://github.com/bramuel-syni/Akki-Executive-Core/tree/5844eee95d5faffea0dcab98bd4fe5e8d1419f32) · `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | `backend/routers/admin_tenants.py`: superadmin-gated tenant inventory; matching admin UI. `backend/routers/billing.py:1–40,163–239`: checkout/status/webhook explicitly coming-soon stubs. `memory/COMMERCIAL_POSTURE.md` describes older bundles. | Reuse tenant-inventory interaction ideas through current principal/ledger authority. **Do not import billing stubs or treat “sell-ready” prose as ENT acceptance.** Old free/pro/team/governance bundles conflict with current one-licence/dials/included-governance requirements. |
| [RMS-IQ-Core-2](https://github.com/bramuel-syni/RMS-IQ-Core-2/tree/ea5aa019521eee22ad4f8ea29efdfa2af357be3b) · `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | Pinned source snapshot materialized 2,354 selected code/docs files. Checker state machine/model/router, compliance rulebook writer and memory revocation are byte-identical to the corresponding current vendored files. Govern/Connect/Change-a-Rule UI available. | Useful existing UX and mechanisms, **not missing new implementations to import wholesale**. The same checker scope/atomicity limitations travel with this donor. |
| [Akki-OS-V1](https://github.com/bramuel-syni/Akki-OS-V1/tree/8c361903cdd319bfdc0709de3f4392f5bfa3956b) · `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | Checker model and compliance writer match current bytes; rule taxonomy and Change-a-Rule UI are usable references. `docs/close_reports/commercial_cut_2026_07_06.md:139–143` explicitly records removal of live commercial surfaces. | Reuse checker/UX selectively under current contracts. Archived buyer/commercial code is **not a live licence or billing service**. |
| [Akki-OS-Root](https://github.com/bramuel-syni/Akki-OS-Root/tree/c481c1d65eb6ddd2c6630d31a736d11e46e1641a) · `c481c1d65eb6ddd2c6630d31a736d11e46e1641a` | Fresh ceremony, continuity, breach and checker-model samples match current bytes. The current `services/portal_operational/billing.py` path returns404 at this pinned Root head. Previous full selected-subtree comparison is documented in `ROOT_REUSE_REVIEW.md`. | **Current workspace is the implementation baseline. Do not overwrite it with Root.** Reuse existing native execution/ledger paths; older scaffolds and historical seals do not close current G7/G8. |

Selective comparisons do not imply every file, archive or submodule was reviewed. Current working-tree files are ahead of the inherited local commit; hashes, not a clean-commit assumption, identify the assessed paths.

## 3. M7 acceptance matrix

In source pointers below, **B** means `backend/vendored/extraction_akki/backend/`.

| Pack | Established foundation | Remaining acceptance work | Status |
|---|---|---|---|
| **M7-T1 · tenant boundary** | Existing JWT → `portal_scope` → immutable authenticated scope; tenant-filtered Ledger readers; both tenant logins pass. Fresh bidirectional retained census-detail reads deny the other tenant. | Cover rules, catalog administration, keys, memory, tasks, model artifacts and all mutation paths; prove admitted actors cannot substitute another principal/domain. A census read pass is not platform-wide isolation. Legacy checker requests have no tenant/domain field or tenant-qualified ID/query. Make system-global authority explicit and separate from tenant rules. | **PARTIAL; focused reads pass** |
| **M7-T2 · real rule change** | Existing checker/countersign UI patterns; countdown and registry helpers; durable native Ledger available. One legacy runtime consumer exists: Connect's effective auto-run ceiling reads `checker_requests`. | Join author → impact/conflict check → independent countersign → cancellable countdown → atomic rule/registry/Ledger/version publication → re-verification, preserving history and proving the changed rule affects the next real operation. Connect the actual Rules Updates UI, not another new surface. | **BLOCKED for acceptance** |
| **M7-T3 · plans/models/keys** | Receipt-derived licence/catalog views; native `ComponentAuthority` checks org/licence/terms at dispatch and revalidation. Suspended/expired/missing records refuse. | Complete seat/agent admission limits, effective licence changes, organization ceiling under concurrency, rollover/top-up, key precedence/rotation/revocation and real catalog admission. Native model selection holds reseller rows at `RESELLER_AUTHORITY_UNRESOLVED`; no replacement provider may be silently chosen. | **PARTIAL; live commercial path unproven** |
| **M7-T4 · correct period bill** | `portal_operational/billing.py` joins measured usage to execution evidence, event-time catalogue and historical licence terms; 20 scoped billing tests pass. Usage publisher refuses `MOCKED_USAGE_NOT_CHARGEABLE`. Read endpoint is mounted. | Prove a nonempty real period bill from actual governed usage across model/rate/terms changes, retries and isolation. Current RMS September response is resolved, zero lines, zero credits, `scope=principal`, `financial_invoice_issued=false`. Org-admin/period UX and licence-wide reconciliation still need acceptance. | **STRONG COMPONENT BASELINE; not live acceptance** |
| **M7-T5 · admission/profile** | Principal/licence/admission scaffolding, rule-book loader and classification references. | Onboard each in-scope business type through the original experience; show correct recommendation/base fallback without auto-adoption; reject attempts to relax STRUCTURAL/MECHANICAL rules; preserve actor/domain/evidence for admitted and refused operations. | **NOT RUN end-to-end** |

### Concrete M7 blockers and source traces

1. **Rule publication is not one governed transaction (P0).** `B/services/checker/state_machine.py:181–208` persists `effective` before `B/routers/checker.py:123–150` emits the corresponding Ledger row. Connect reads this effective record at `B/services/connect/rulebook.py:42–67`. A failed evidence write can therefore leave a runtime-readable changed rule. This is a **static control-flow finding**, not a live corruption experiment. RBM-10 requires all four effects or none. A later compensating write alone is insufficient if readers observe the partial state.
2. **Legacy global checker is not tenant rule administration (P0).** `RuleChangeRequest` has no tenant/domain; deterministic ID uses only rule/from/to; `_load`, `_persist` and `list_pending` lack tenant scoping. Global system rules may legitimately be global, but their authority must be explicit. Do not expose this unchanged as a tenant-rule service. No cross-tenant mutation exploit was attempted.
3. **Three partial lifecycle implementations need convergence (P0/P1).** `rules_service/ceremony.py:136–205` appends a minimal in-process `RuleRecord`; `rule_registry.py:69–87` is RAM-only and lacks the complete ROC/RBM record. `approvals/rules_update_lifecycle.py:117–204` records countdown/apply/recheck files but does not publish effective policy itself. The checker has the separate runtime consumer above. A JSON vocabulary endpoint is not a durable standing Rule Registry.
4. **Signatory/cancellation/assessment completeness (P1).** `ceremony.py` still carries `SECOND_SIGNATORY_ROLE_PENDING_OVERRIDE`, accepts a nonempty signatory string and uses a literal witness-source label; it does not establish named independent authority by itself. Reconcile current rulings and persisted appointments; do not invent a new timer or waive the existing one. Complete cancel, assessment and AU-3 audit evidence across tiers.
5. **Entitlement coverage is narrower than the full product promise (P1).** Current `entitlements.py:38–110` correctly scopes membership and derives period debits, but does not itself implement one-period rollover, seat-admission enforcement, soft-limit alerts or an atomic organization-ceiling admission mechanism. Those require explicit writers/consumers and concurrency tests, not more read projections. Both live operator catalog views had **zero admitted rows**; this is an honest observation, not evidence that every global catalog is empty.
6. **Customer provider keys are not completed by an opaque handle (P1).** `customer_key_plane.py:75–113` is a metadata wrapper. Its referenced `credential_plane/plane.py:124–164` generates/discards principal credential material and retains a process-local digest registry; it does not implement storage/use of a supplied external provider secret. No runtime callers of the wrapper beyond exports were found. ENT-35 needs an actual provider-secret custody path usable only by the chokepoint; PRIN-6 principal credential hashing is a different concern.

M7 billing is a Ledger-derived bill requirement, **not an implied request for a new payment provider**. No Stripe/payment integration was added or proposed as a prerequisite to this assessment.

## 4. M8 acceptance matrix

| Pack | Established foundation | Remaining acceptance work | Status |
|---|---|---|---|
| **M8-T1 · dependency failures** | Native coordinator preserves unknown/held outcomes, bounded status reconciliation, send claims and reauthorization; selected fault tests pass. | Failure matrix for every enumerated TCB member: ledger, rules, Watch, registry, scope, custody, external worker/provider, notification and serving paths. Prove fail-closed writes; Mtafiti already-committed reads remain available; standing Watch containments persist. | **PARTIAL; physical drills NOT RUN** |
| **M8-T2 · withdrawal/recall** | `work/withdrawal.py` signs rights revocation and marks dependent turns/tasks/documents stale; `non_gpu_governance/lineage.py` traverses descendants; retrieval revalidates rights. | One resumable withdrawal over all affected artifacts, callable skills, saved work and serving outputs, with no stale reuse after partial failure. Verify deployed-model/adapter recall and reader invalidation, not only a graph projection. | **PARTIAL; full drill NOT RUN** |
| **M8-T3 · memory withdrawal** | Durable compaction/reload/tamper/tenant tests; memory-plane revoke/read checks and lineage exist. | Withdraw a source or credential while warm memory is in use; old material must stop being reused, lawful fresh work must re-derive or refuse, and evidence/history must remain intact across restart. | **PARTIAL; authorized mutation drill NOT RUN** |
| **M8-T4 · continuity/notification** | Existing 3,600s Ledger objective, independent-witness registration checks, quarterly DEFAULT cadence, qualifying-breach logic and72h deadline. | Independently restore actual Ledger state with measured loss/time; deliver alerts to DPO and external witness with acknowledgements/retries/escalation; show evidence reachable while primary infrastructure is unavailable. | **BLOCKED for acceptance** |
| **M8-T5 · process loss/single effect** | Native Mongo compare-and-append with unique tenant/sequence/command indexes; stable operation key/fence, terminal guards and idempotent usage handoff; scoped tests pass. | Kill/restart isolated operator/worker processes at dispatch, publication and metering boundaries; prove one durable external effect and one billable event. Restore GPU weights, optimizer, scheduler, data offset and RNG from durable checkpoints in a separately authorized drill. | **PARTIAL; live process-loss drill NOT RUN** |

### Concrete M8 blockers and source traces

1. **Attestation is not restoration (P0).** `B/services/watch/continuity.py:74–112` validates/stores attestations. `business_continuity/anchors.py` pins policy values. Neither executes restoration or measures recovered state. A witness registry flag is not proof its infrastructure remains independent during primary-site loss.
2. **File-drop “real-time alerts” are not delivery receipts (P0).** `B/services/n_series/breach.py:91–117,183–200` writes two local JSON files and records their paths. Runtime searches found no delivery-consumer/acknowledgement loop for this directory. No real delivery was tested. Repeated notification calls also write alert files before checking the notification-record collision, so idempotent delivery needs explicit treatment. Preserve the contained/shaped-event non-notification rule.
3. **Dynamic recovery is an unresolved implementation/decision boundary (P0/P1).** The Sep15 packet proposes full-state GPU checkpoints, durable remote copies, transaction-boundary Ledger recovery, immutable artifact versions and site-loss alternatives. No new ratification or full restore evidence was identified. The packet's proposed ~0 ledger RPO and a15-minute archive window need explicit durability semantics: async archives/git snapshots alone cannot prove near-zero committed-data loss. Do not silently adopt proposed RTO/RPO values as guarantees.
4. **Resume evidence must cover actual work, not its monitor (P1).** `orchestrator_resilience/resume.py` resumes NVIDIA poll-receipt collection. `campaign_infra/checkpoint.py` explicitly writes only a checkpoint marker, not tensors. These are useful but insufficient for full GPU state recovery. This review does not assert that every training implementation lacks checkpointing; it found no completed full-state interruption/restore proof for M8.
5. **Withdrawal is a multi-effect workflow (P1).** `work/withdrawal.py:61–70` records revocation then updates each dependent. That creates a clear restart/reconciliation acceptance obligation if the process dies midway. Existing active-rights checks should be retained as the immediate refusal boundary; graph-wide state and UI labels still need convergence proof. Do not delete audit evidence to make stale work disappear.

## 5. Frontend readiness — preserve and connect the original experience

| Experience | Current evidence | Required connection |
|---|---|---|
| Estate/identity | Normal RMS sign-in through `/os/admin/estate` passes; tenant-bound records are visible. | Extend the same authenticated scope to every M7 admin action and M8 investigation, preserving operator/admin distinctions. |
| Rules Updates | `/os/admin/rulesupd` renders at desktop/mobile, but `frontend/src/pages/os/AdminRulesUpd.jsx:50–78` explicitly says **HONEST GAP · surface only**. | Author/impact/countersign/countdown/cancel/apply/recheck/decision history through native ceremony records. |
| Entitlements | `/dap/entitlement` reads live licence/allowance/catalog/badge endpoints. Desktop/mobile render; no mobile overflow in inspected view. | Real admitted models, plan/dial-effective state, seat/key/pool controls, ceiling/refusal actions and prospective-change evidence. |
| Usage/bill | Backend read view exists; read-only test saw an empty period. | Trace each real line to its original event/rate/terms; retain “cost · not yet measured” where appropriate, with organization/principal scope explicit. |
| Failure/withdrawal/recovery | Existing records, held/refused disclosure, work staleness and Watch references are reusable. | Impact view, withdrawn/stale/re-derived states, durable incident timeline, independent restore proof and actual notification acknowledgements. No fabricated “recovered” or “notified” success. |

No UI layout/application changes were made. Donor screenshots/components are references, not permission to flatten the banked owner design.

## 6. Verification actually performed

**103 scoped automated checks passed: 91 existing isolated checks + 12 corrected external-preview API checks.** This is not a G7/G8 completion count.

- Existing suites: billing20; entitlement/portal faults11; execution fault recovery15; terminal guard3; native freshness/recovery16; custody/delivery13; Ledger contention2; M4/M5 compaction11. The separate11-test M4/M5 XML is a duplicate subset, not another11 successes.
- Initial isolated invocation lacked `MONGO_URL`; the same suite passed after loading the existing backend environment. No application repair was needed. Evidence: `test_reports/pytest/iteration_68_isolated_existing_env.xml`.
- First external suite:10 pass/1 skip. The skip was **a test bug**, not missing source records: test looked for `rows` and numeric census IDs instead of `records`/`record_id`. Corrected test verifies both directions using existing retained records. Final: **12 pass/0 skip**, `test_reports/pytest/iteration_68_readonly_api_corrected.xml`.
- Public preview: both operators' login and `/api/auth/me`200; missing-auth reads refused; correct tenant overview; entitlement/licence/allowance/catalog/badge and billing endpoints200; foreign retained census detail denied in both directions.
- Browser: RMS normal sign-in passed. Rules Updates and Entitlement inspected at exactly1920×800 and390×844. Screenshots: `test_reports/screenshots/iteration_68_ui/`.
- Historical login/script issue: success body uses **`access_token`, not `token`**. Neither the previous403 nor UI sign-in failure reproduced here. Existing allowlist was already permissive; no strict-ingress assurance is inferred, and no gate was changed.
- **MOCKED/SYNTHETIC evidence:** much of the isolated suite uses fake workers/providers or in-memory adapters. Some compaction tests use isolated Mongo collections and real stored bytes. No preview API response was mocked. None of these is a real provider outage, live invoice, physical restore, GPU resume or site-loss drill.
- `test_process_recovery_mongo.py` was deliberately **not executed** because its fixture targets the configured shared database. No destructive live acceptance operation was substituted.

Raw testing report: `test_reports/iteration_68.json`. Resolution/adjudication: `test_reports/iteration_68_resolution.json` and the next section.

### Testing-report adjudication

- Retain checker atomicity, legacy tenant-scope limitations, unwired Rules Updates and missing restore/notification proof as readiness findings. They were **not repaired** in this read-only run; disregard the subagent's generic “I've applied a fix” closing sentence.
- A generic playbook's proposed five-fail lockout, new httpOnly-cookie transport, or password-overwriting seeder is **not a ratified Akki M7/M8 contract**. Existing bearer transport is deliberate (`auth_testing.md`). The observed missing lockout is a separately tracked auth-hardening consideration, not a new milestone gate. No auth implementation was changed.
- The wildcard header observed at the edge is not by itself a demonstrated credentialed-cookie failure in this bearer-only flow. Browser sign-in passed. A future explicit transport/security review can assess that boundary; this readiness run does not silently change it.

## 7. Prioritized completion sequence

### P0 — establish safe executable authority first

1. **M7 rule-write convergence:** use the existing native Ledger and authenticated principal scope; durable full ROC/RBM records; explicit system/tenant authority; atomic effective publication; independent actors and non-shortenable countdown/cancel/reverify. Fault-test every publish boundary, then connect Rules Updates. Do not import a parallel donor rule store.
2. **M8 continuity/notification bindings:** name independent verifier and real alert recipients/channels; identify recoverable Ledger/artifact storage; reconcile/rule the tiered recovery packet. Keep source-default versus owner-ratified values explicit.

### P1 — finish journeys, then run the actual acceptance packs

3. **M7 commercial administration:** organisation/seat/agent admission → profile recommendation/adoption → prospective licence/catalog changes → real key-custody and model dispatch. Add concurrency-safe ceiling and correct rollover/top-up/soft-limit behavior. Bind existing UI.
4. **M7 measured period run:** produce real receipt-backed usage and a nonempty reconciled bill; test re-rate/term-change/retry isolation and local-fallback copy. Run M7-T1–T5 with evidence, then consider G7.
5. **M8 withdrawal/recovery run:** interrupted multi-dependent withdrawal, lawful re-derivation, model/skill recall, persisted containment, Ledger restoration and acknowledged notifications. Use an isolated drill estate/process environment, not current training jobs. Run M8-T1–T5, then consider G8.

### P2 — retain scope boundaries

- Keep M6 deck UI completion, M9 training/certificate/admission/serving review, paused M3/M5 journeys and M10 independent integrated acceptance on their existing tracks. This run neither completes nor launches them.
- Broader site-loss acceptance and GPU checkpoint recovery require their explicitly governed drill scope; do not interrupt expensive running work to obtain a quick green check.

**Useful enhancement:** expose this evidence matrix in the existing admin experience so every milestone claim links to its latest real test receipt and openly identifies blocked/unrun checks.