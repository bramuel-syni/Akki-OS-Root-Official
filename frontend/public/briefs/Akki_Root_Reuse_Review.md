# Akki-OS-Root — deep reuse assessment for the milestone roadmap

28 September 2026. Read-only functional/reuse review requested by the owner. Not a
security audit or live certification. No donor code was run, merged or substituted;
no estate/model/GPU request, database mutation or application configuration change.

## 1. Repository identity and comparison

- Source: https://github.com/bramuel-syni/Akki-OS-Root
- Pinned `main`: `c481c1d65eb6ddd2c6630d31a736d11e46e1641a`.
- GitHub's top recursive result was truncated at 55,100 entries. It is NOT used
  as proof of complete code coverage. Backend, frontend, memory and test_reports
  subtrees were fetched separately and each was non-truncated.
- Compared every donor blob under `backend/` and `frontend/src/` against the
  corresponding current workspace path: **1,215 paths; 1,200 identical Git blobs,
  15 different, zero donor-only paths**. This is code identity, NOT 98.8% completion.
- Materialised 1,204 selected code/doc files (excluded oversized/binary/non-source
  assets), verifying each via the pinned Git blob. Twenty required raw downloads;
  the others were copied only after local byte identity was established.
- Parsed 1,005 Python files into a symbol/import/route inventory, without imports
  or execution. No parse errors. Structural coverage is not a claim of manual
  review of every symbol or behavioural correctness.
- Current workspace contains substantial additions beyond this Root checkpoint:
  operational census, native activation, Northena execution, custody delivery,
  portal/skill execution, non-GPU metadata validation, frontend joins and tests.
  Preserve these; importing the older Root tree wholesale would lose work.

Evidence: `/app/assessment_workspace/incoming/root_repo_review_20260928/`
contains `top_tree.json`, non-truncated subtree files, `code_tree.json`,
`local_blob_comparison.json`, `snapshot_manifest.json`, `symbol_inventory.json`,
`current_only_source_paths.json` and `snapshot/`.

### Root's linked repositories are not embedded implementations

`assessment_workspace/repos/` entries are Git commit links:

| Repo | Root's referenced commit |
|---|---|
| Akki-Executive-Core | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` |
| Akki-OS-V1 | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` |
| Extraction-Akki | `7e84cd98f37aea50f9d0ed55fbd8d654ffc582f7` |
| RMS-IQ-Core-2 | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` |

Core/OS pins match the sources already fetched in the earlier planning review.
No claim is made that every file in Extraction/RMS-IQ gitlink targets was newly
downloaded and reviewed. Their vendored operative subset is inspected here.
At implementation of a genuinely missing function, inspect the relevant pinned
linked-repo module before calling it absent across the estate.

## 2. Operative composition and what must not regress

`/app/backend/server.py:40–53` chooses an available Extraction spine directory,
otherwise the vendored runtime. The reviewed current workspace uses the vendored
tree; verify that selection again when opening each milestone. Server assembly
is essential: code present in a service does not mean its route remains reachable.

Fifteen changed donor/current paths:
- `backend/requirements.txt`, `backend/server.py`.
- Vendored `routers/{portal_entitlement,portal_requests,transform_forms}.py`.
- `services/census_autonomy/scheduler_program.py`.
- `services/ledger_emitter/emit_intent.py`.
- `services/training/router.py` and `training_runner/{moac_emitter,runner,ssh_seam}.py`.
- `frontend/src/{App.js,components/ui/dialog.jsx,lib/apiClient.js,pages/dap/DAPLayout.jsx}`.

Important current differences:
- Scheduler now uses `operational_runner.run_bounded_census`, not the older
  shape-only `engine.run_bounded_census` completion path.
- Portal requests now join Mongo/Northena work and execution. Do not reinstate
  donor `dap_lifecycle` as a competing request authority.
- Entitlement views now derive the effective licence/allowance and billed use
  through `portal_operational`; retain the current authoritative ledger joins.
- Current skill/query routes use native query execution and custody; the older
  async dispatcher is NOT evidence that the current build has no skill support.
- Current training uses `recorded_effect.execute_once` and the persisted result
  for MOAC. Do not bring back donor re-execution to obtain canned inputs.
- Retain current assembler/client route/fidelity changes; no root-wide overwrite.

## 3. Reuse map by milestone

Paths below are relative to `/app/backend/vendored/extraction_akki/backend/`
unless explicitly marked frontend, server or tests. “Existing” means inspected
code/connection, not a passing live acceptance run.

### M1 — Registry and census: KEEP + WIRE + targeted REPAIR

**Existing path:** `routers/census_operational.py:71–92` submit→
`services/census_autonomy/operational_runner.py:25–100`→
`census_router.py:driver/execute_source`→existing RDS/OBS/non-GPU dispatch→
`mtafiti/census_result_adapter.py`→result receipt and `operational_reads`→
portal census/Registry facts→frontend `components/census/{CensusWorkspace,useCensusWorkspace}`.
Runner already checks scope/budget, locks duplicate execution, validates results,
registers complete outcomes and writes/fsyncs result receipts.

**Missing/proof tasks:** correct external-worker placement for ALL connectors;
NAS worker access; deeper source dimensions/CPU quality packs; persistent read
agreement and recovery. `mtafiti/asset_registry_writer.py:54–57` explicitly holds
an in-memory registry, while existing reads reconstruct from result receipts.
Do NOT infer total data loss just from RAM; verify authoritative receipt custody,
hydration and all consumers. Repair behind the existing writer/projection contract,
not by adding a second competing Registry.

`census_operational.install():99–109` intentionally quarantines older unscoped
census/Registry routes with 409 and keeps the current tenant-bound ones. Some
legacy mounts/comments still advertise unavailable controls. Resolve demanded
controls within the operative path and align consumers/documentation; **do not
restore the unscoped or stub path simply to make a status non-409**.
Old `engine.py:205–224` can manufacture COMPLETE without reading a source; it
cannot be used as M1 success evidence.

**Regression assets:** `backend/tests/census_operational/` contract, execution,
identity and UI-fidelity tests. Inspect/extend their actual fixtures, not assume
their names establish remote isolation.

### M2 — Watch/Grey Mirror: KEEP mechanisms; WIRE real observations/effects

**Existing:** `watch/router.py` has state AND mutations for verdict/action/mark,
sever-signal and mirage-artifact records; it is not merely read-only. `macho.py`,
`mkono.py:117–189`, `persistence.py`, `containment.py`, `certificate_library.py`,
`mark.py`, `mirage.py:148–227`, `witness.py` and `continuity.py` implement reusable
grammar, mapping, record ordering, marks, mirage records and witness checks.
`grey_mirror/router.py` is a derived state view; `/app/backend/server.py` mounts
the Watch and other associated routes.

**Missing/proof tasks:** observation producer→detector→bounded physical effect→
record/witness/console/notice at each real protected boundary. For example,
`persist_action` writes a record; `engage_mirage` labels/writes a severance—it
does not by itself demonstrate actual access revocation or mirage network routing.
Actual legitimate-work release/reconciliation and independent witness failure
domain require drills. Bind real effects behind existing mechanisms, not new engines.

State directories default beneath assessment_workspace across Watch/census/mirage.
Absent confirmed persistent runtime mounts/configuration, persistence is a risk,
not a proven deployed data-loss incident. Qualify/repair durable custody in M1/M2;
exercise recovery in M8. A writable newly-created directory alone is not durability.

### M3 — Commission/extraction/delivery: KEEP the current execution spine

**Existing active composition:** server mounts `routers/portal_requests.py`,
`activation_controls.py`, `activation_records.py`, `custody_delivery.py` and
`skill_queries.py`. Request routes use `northena.portal_work`,
`portal_operational.{access,actions,execution}` and the same Mongo-backed ledger.
`northena/execution_*` already separates authority, reservation, dispatch,
measurement, registry publication, retrieval and uncertainty/reconciliation.

`custody_delivery/service.py:13–125` already claims once, verifies current
authority/registered artifact, resolves provider receipts, handles uncertain
outcomes and checks completion separately from an offered URL. Do not build a
new custody lifecycle. Bind qualified providers and prove real recipient effects.

`activation/runtime_binding.py:59–90` explicitly loads a configured async factory
and installs a validated complete runtime. With both factory/timeout absent it
returns False—API presence then does not imply native providers are ready.
Qualification of actual factory/workers/inspection/custody is an M1/M3 task.

**Reuse tests:** `backend/tests/{execution_spine,execution_components,activation_controls,portal_operational,model_handoff}/`.
These are valuable contract/regression assets; positive fixture receipts are not
physical worker or recipient delivery evidence.

### M4 — Answers/context/reasoning: KEEP gates; qualify real capability

**Existing:** mounted `routers/service_1.py`→dispatch/qualified-data/composed-
conclusion; `services/chat/router.py:31–94`→LLM chokepoint→Critic seam;
`service_1/{answer_grounding,mechanical_composer,async_worker}`; Targeta and Solva
trace/floor machinery; newer `non_gpu_governance/{quality,context,lineage,gate}`
joins measurement/provenance to current execution releases.

**Limits:** `solva_depth/pipeline.py:37–95` explicitly contains a code-only
five-stage reasoning pipeline; `reasoning/probability.py:14–28` retains equal
weighting. This is reusable structure, not independent proof of useful measured
reasoning or deployed model capacity. `chat/router.py` accepts request actor/model
fields and does not itself provide a multi-turn persisted grounded session.
Trace actual principal/context binding and calling UI; one generic chat response
must not count as M4's source-grounded/session-aware acceptance.

`backend/tests/non_gpu_flows/test_native_quality_context.py` explicitly uses
signed SYNTHETIC lab evidence. Reuse its failure cases, replace positive proof
with actual authorised worker/model/quality/context producers during acceptance.

### M5 — Memory and collaborative work: KEEP storage/access; fill actual product gaps

**Existing:** mounted `routers/memory.py` and `services/memory/{scoped_accessor,
publication,revocation,working_set,write_back,compaction_v1}`. Publication uses
Mongo (`publication.py:74–154`) with quality/rights and event joins. Threshold
slots have historical anchors; reconcile actual later rulings, do not arbitrarily
delete them as invented or ask the owner the old question again.

`frontend/src/components/prototype/useOperationalWork.js:31–68` already fetches
real OS/portal work/entitlement and submits with idempotency. `nexusWork.js:47–58`
still provides explicit empty team/priorities/goal-detail feeds and unknown score
values. These are honest unconnected experiences, not completed source-fed team
workflow. Finish producers/commands/persistence into existing owner markup.

`backend/tests/non_gpu_flows/test_native_memory_and_certificates.py` is labelled
SYNTHETIC authority/FAKE ledger. It proves join logic only, not live memory effect.
No second memory plane, work store or reconstructed “demo productivity” metrics.

### M6 — Artifacts/decks/skills: preserve current skill execution; extend rendering

**Existing:** `transform_forms/callable_skill_persistence.py:38–112` provides
Mongo write-once provisioning and narrow revocation. `routers/skill_queries.py`
already supports intent/status/advance/delivery/status; `portal_operational/
query_execution.py:9–71` joins native coordinator/grounding/late refusal/current
rights to the same history. Current `transform_forms.py` routes into this path.
The old `service_1/async_worker.py` NotImplemented branch is not a platform-wide
absence of callable skills. Do not add another queue or intent protocol.

**Deck limits:** `contracts/deck_spec_v0.py` is a frozen small shell. Previously
inspected Executive Core has persisted deck-generation jobs; Root's Core gitlink
pins that same source. Reuse the artifact pipeline and complete source-defined
determinism/export/fidelity behaviour, not a new general-purpose deck studio.

**Proof work:** native provider admission, actual grounded caller response and
custody receipt, full async/recovery, complete DeckSpec/versioning and deterministic
exports. Reuse `backend/tests/non_gpu_flows/test_skill_queries_non_gpu.py` and
`portal_operational/test_callable_skill_query_safety.py` as regression assets.

### M7 — Rules, principals and commercial use: KEEP existing authority and accounting

**Existing:** `rules_service/{rule_registry,ceremony}`, canonical rules router,
ROC vocabulary, checker/signatory flow, `entitlement_service_v1` and platform
principal/tenant/access modules; current portal entitlements and billing.
`portal_operational/billing.py:67–149` reconciles event-time catalog/terms against
dispatch/raw meter and refuses invalid/duplicate evidence. It explicitly reports
`financial_invoice_issued=False`—do not present it as a payments/invoice integration.

`rules_service/ceremony.py:48–54` countdowns reference recorded DEFAULT constants.
That is an anchor to reconcile, not proof that every current restriction is
necessary and not licence to remove source-backed protections blindly. The
module's in-memory registry is not a reason to create another registry authority:
trace effective persisted policy and land changes through existing ownership.

**Delta:** operative tenant permissions/logins/principal attribution; lawful
effective changes and actual usage producers; round/rate/period decisions only
where still unresolved. No new auth/entitlement/billing system or public broad scope.

### M8 — Resilience: reuse recovery and attestation; prove physical behaviour

**Existing:** execution journal/completion/reconciliation, ledger writer/verifier,
`orchestrator_resilience/{heartbeat,resume,adopt,orphan_detector}`, artifact atomic
write/orphan recovery, Watch witness and continuity, `business_continuity/anchors`.
`watch/continuity.py:74–101` validates/persists an attestation. A registered boolean
claim of independence is not evidence of physically independent infrastructure;
a stored attestation is not the restore operation.

**Delta:** state custody qualification, current policy mapping, real failover,
independent restoration/chain verification and accurate RPO/RTO measurement.
No new recovery engine merely because a drill has not yet been performed.

### M9 — Audio/training/learning: KEEP mature scaffolding; qualify real runs

**Existing:** audio_plane_v1 corpus/ingestion/provenance/cluster/calibration and
three-wave modules; source read-only guards and pairing; layer-B backend seams;
training recipes, protected test-set sealing, runner, MOAC, model admission,
checkpoint infrastructure and Whitepaper Wizard Tier 1/2.
`training_runner/runner.py:101–225` admits runs, attaches WPW at commission and
uses `recorded_effect.execute_once`. `recorded_effect.py:65–97` refuses invalid
or unknown outcomes instead of resubmitting. This is valuable recovery machinery,
not proof of model quality or complete physical checkpoint restoration.

**Delta:** actual admitted compute, corpus/model licensing and rights, perception
backends, realistic heldout/independent measurement, serving, privacy/distance,
incremental voice contracts and genuine change-of-capability proofs. Owner is
handling GPUs; no SSH attempt was made. Never replace a missing real result with
seam canned measurements or old SYNTHETIC closures.

## 4. Concrete changes to the roadmap

1. Make reuse explicit in every milestone: the function may be partly built;
   retain current writer/runtime/provisioning/Watch mechanisms and prove bindings.
2. M1: start on `/api/portal/census/run`, connect the existing writer/read model,
   fix actual persistence/worker isolation/depth; never resurrect legacy stub routes.
3. M2: mutations/mapping/marks/mirage/witness mechanisms exist. Commission actual
   observation/effect loops. Do not characterise all Watch code as a read-only UI.
4. M3/M6: native execution/custody/skill paths are already implemented here beyond
   Root. Provider qualification and end-to-end results are the primary work.
5. M4/M5: preserve contracts and storage, but their synthetic tests or equal-weight
   reasoning scaffolds do not close useful live answers/memory/collaboration.
6. M7/M8/M9: preserve billing joins, recovery helpers, training single-effect/WPW;
   do not rebuild to obtain missing acceptance evidence.
7. Add post-assembly route reachability, persistent-state and no-stub-positive
   cases to milestone acceptance, not a separate “audit first” project.
8. No full M9-training prerequisite is imposed on M2. M2 proves its current real
   Watch-to-research action loop; GPU-dependent learning outcome is the explicit
   M9 extension and must not be claimed already passed.

## 5. Limitations and next action

Broad code identity/structural inventory plus manual representative end-to-end
call-path inspection and a read-only functional review were performed. This is
not a full audit of every archived historical test/branch/submodule. No application
test suite or live estate/model/restore acceptance was run. Repository tests,
commented seals and UI presence do not close those outcomes.

The conclusion is **reuse and finish, not rebuild**. These findings are engineering
tasks inside the relevant milestone, not prerequisites for another global review.
Next action remains M1.1 shaping/readiness and commissioning through the current
Akki path; all milestone acceptance runs remain NOT RUN.