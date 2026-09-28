# M1.1 — second verification and execution-plan tightening

28 September 2026. **Readiness work, not milestone acceptance.**

## Outcome and owner direction

The owner clarified that the second review is the verification already proposed,
then execution follows the governing ten-milestone roadmap. Every milestone must
review all relevant built repository implementation during readiness to avoid
rebuilding. Communication, questions, refusals and recommendations remain tied
to the milestone's outcome, rather than separate priority/approval frameworks.

The roadmap's readiness revision 1 now states this explicitly for M1.1–M10.1.
It retains ten milestones and 51 acceptance packs. M1 covers admitted non-GPU
workers and both connected GPU-hosted worker routes; new model/perception/training
capability qualification remains M9. Existing qualified GPU census measurements
are not automatically deferred merely because they use GPUs.

## Verified baseline

- Existing RMS operator login succeeded. Authenticated census overview, records,
  latest, detail/state and Registry aliases respond; unauthenticated reads deny.
- The observed RMS overview contains **seven retained records and zero PENDING
  runs**, with latest `cr-dd05196d837f`. This is a scoped snapshot, not the whole
  estate or another tenant's current state.
- Historical blocked runs `cr-809561ad5643` and `cr-a29e3b7b16ae` remain. They are
  candidates for the owner's card reference, not a conclusively identified card.
  Do not manufacture a new pending entry or rewrite a historical refusal.
- `GET /api/portal/census/gpu-spend` and
  `GET /api/portal/census/response-required-items` return **409** through the
  assembled application. They are intentionally quarantined, not working compute
  or card-resolution APIs. The handoff's public GPU-spend success claim was wrong.
- Retained 17:15 UTC GPU receipts show both expected hostnames and two NVIDIA H200
  devices per host. This verifies the historical remote connection, not a fresh
  connection, admitted census worker, accelerator workload or model capability.
- The compound connection command has rc=0 but stderr says `nvcc: command not
  found`. Pipeline exit status must not certify every subcommand. Compiler on
  PATH is unverified; this does not prove a toolkit is absent elsewhere. Driver
  compatibility, a toolkit path and an operational model runtime are different.

Evidence: `/app/test_reports/iteration_54.json`; the current source and existing
`assessment_workspace/phase0/gpu_receipts/20260928T1715*` connection/telemetry
receipts. No new GPU/SSH/source call was made in this review.

## Implementation findings and ownership

Runtime paths below are under `backend/vendored/extraction_akki/backend/`.

| Finding and evidence | Classification | Existing work package / proof |
|---|---|---|
| `census_autonomy/rds_data_dispatch.py` and `obs_dispatch.py` invoke estate SDKs in E1 and self-label output `akki_host`; `operational_validation.py` accepts that shape. | Confirmed placement/provenance defect, not merely an untested provider. | M1.2: move reads to admitted external workers; M1-T2/T3. |
| `non_gpu_dispatch.py:43–103` launches a local subprocess. `AKKI_CENSUS_EXECUTION_MODE=non_gpu_jump` currently selects the external jump for RMS, but the local alternative is not compliant off-E1 execution. | Existing fallback cannot establish independence. | M1.2: inspect all configured alternatives; M1-T2. |
| `census_router.py:25–35` falls back to remote dispatch for NAS; `remote_worker.py:41–42` only accepts `mysql_metadata`. | Concrete active adapter gap. Do not conclude no reusable file/media adapter exists elsewhere. | M1.2: inspect remaining repo adapters, qualify NAS access on an external worker, bind/extend; M1-T1/T2. |
| `remote_dispatch.py:16–25` uses direct workbook connection when selected; real GPU telemetry and direct-workbook modes are present in current configuration. | Connectivity mechanism exists; worker custody/dependencies and actual remote job still require proof. | M1.2: reuse, do not rebuild SSH; M1-T1/T2/T3. |
| `non_gpu_census_worker.py:99–121` reports source complete after any connection succeeds; per-connection failures stay in separate details. | Full-scope coverage can be overstated if this receipt is used alone. | M1.3: carry frozen denominator and each connection's status into public evidence; M1-T1/T3/T5. |
| `operational_reads.py:28–37` publishes bounded aggregate metadata with volume/quality unmeasured. | This is not the promised deep census. | M1.3: wire existing deeper producers, preserve method/coverage; M1-T1/T3. |
| `mtafiti/composition_census.py`, `quality_profiler.py`, sampling and detection helpers already exist. | Reusable implementations; not live-complete merely because their code is present. | M1.1/M1.3: read dependencies, fix demonstrated limits and run externally; do not rebuild profiling. |
| `asset_registry_writer.py:53–77` uses a RAM projection; `census_result_adapter.py:20–25` restores from retained receipts; `operational_reads.py:13–40` invokes restoration. | Recovery implementation exists; actual durable storage/all-consumer recovery is unqualified, not proven lost. | M1.3/M1.4: qualify current custody and hydrate all readers; M1-T4/T5. |
| `routers/census_operational.py:99–109` quarantines legacy handlers. The old synchronous producer calls the shape-only engine. | Retain guardrail. Do not simply restore a handler or add it to an allowlist. | M1.3: demanded compute/card controls need current tenant-bound implementation; M1-T4. |
| `frontend/src/pages/os/OwnerOSPage.jsx` mounts `osModel/historyModel`; compute opens an informational notice, and GPU spend rows are static unmeasured values. | Real owner UI not yet connected to compute evidence. `CensusWorkspace` alone is not the active UI acceptance target. | M1.3: bind existing owner surfaces to the same records; M1-T4. |
| `historyModel.js:18,32` uses `census_number || census_run_id`, while operational result records use `record_id`. | Current desktop/mobile smoke visibly showed `Census #undefined`; exact id mapping needs repair. | M1.3: retain real record identity in cards/detail without changing prototype; M1-T4. |

## Review coverage — explicit limits

Independent static review covered route assembly, the operational census router,
runner/store/reads/scope/validation, dispatch variants, engine/telemetry and the
legacy producer/response-required paths. Main-agent reads additionally covered
the actual owner OS/session/history bindings, GPU remote worker and local worker
bodies, Mtafiti census/result adapter/writer/composition/quality modules, existing
tests, prior reuse evidence and current non-secret configuration/receipts.

**This is not a claim that every relevant M1 file, every repository file, or all
linked-repository implementations have been read.** Remaining relevant modules,
contracts, schemas, alternative file/media adapters and dependency/test branches
must be read in full before their implementation work. Each readiness record must
list what was read, what remains, and why each candidate is reused, wired, repaired,
extended, superseded or genuinely insufficient. The prior 1,215-path comparison
is structural identity evidence, not behavioural or line-by-line review.

## Tests and reconciliation

- External-preview owner Registry/history smoke: existing login; actual retained
  RMS data; desktop 1920×800 and mobile 390×844; **no horizontal overflow**.
  Screenshots: `/root/.emergent/automation_output/20260928_173505/`.
- Independent verification: **24/24 isolated offline contract cases pass**.
  Those positive fixtures are **SYNTHETIC/MOCKED**, not live estate acceptance.
- The original live test wrongly applied fixed census #4 counts to `/latest`.
  Corrected only the test: current latest must agree with its own record and keep
  aggregate semantics; the owner's exact historical #4 counts remain asserted on
  `/records/4`. No source values or acceptance thresholds were weakened.
- Read-only live retest: **12/12 pass**, including authenticated scope/aliases,
  anonymous denial, current and historical counts, and historical refusal state.
  Evidence: `pytest_iteration_54_readonly_resolution.xml`.
- The testing agent did not reproduce the undefined label; the main-agent live
  screenshot and source branch above establish it as a current finding, not a
  historical-only dismissal. Runtime repair is scoped to M1.3, not claimed done.
- Its generic missing-sign-in-test-ID recommendation is unsupported: existing
  `CensusAccess.jsx:26–32` supplies unique IDs and the main smoke used them
  successfully. `OwnerMarkup.jsx` generates history/action IDs. Inspect actual
  mounted control identifiers before adding duplicate instrumentation.

No app runtime, auth, credentials, configuration or prototype was changed; no
census submitted, source scanned, service restarted, admission minted or GPU
workload run. The only non-document edit repairs an existing read-only test.

## Next execution, within the plan

1. **M1.1:** finish the complete relevant-code/dependency review and existing-card
   reconciliation; recover actual descriptor/authority records and freeze source,
   measurement and worker coverage through the existing commission mechanism.
2. **M1.2:** reuse/bind external workers, source drivers and source custody for
   both worker classes; establish NAS access externally; eliminate E1 source reads.
3. **M1.3:** connect existing deep measurements, honest per-region coverage,
   durable Registry hydration and real compute/card/history bindings.
4. **M1.4:** commission the real census through Akki and run M1-T1–T5; repair
   until all mandatory tests pass. Only then close G1 and open M2 delivery.

M2–M10 retain the agreed sequence and each begins with the same complete reuse
review. Artists_app and missing tenant authority remain scoped dependencies, not
blanket blockers. All live milestone gates remain **NOT RUN / NOT PASSED**.