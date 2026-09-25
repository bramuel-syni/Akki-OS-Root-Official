# Akki: verified Canon-to-code findings

**Date:** 25 September 2026. **Disposition:** evidence report delivered; exhaustive clause-by-clause conformance audit remains OPEN.

This report replaces blanket conclusions, not the owner's Canon. Akki contains substantial executable governance, data-source, registry, training and audio machinery. It also contains incomplete production bindings, misleading completion states, stale projections, and explicitly illustrative screens. Neither “essentially a mock-up” nor “fully operational governed platform” is justified by the inspected evidence.

The owner reports the GPUs are healthy. Historical receipts substantiate successful access and real GPU work. This audit establishes **no current GPU hardware failure**, no need to replace a key, and no justification for enabling password authentication speculatively.

## 1. Scope, method and limits

Owner request and approval are preserved in `SCOPE.md`. Application code, GPU hosts, estate credentials and estate databases were not changed. No source-data pull, training job, request submission, skill invocation, approval or hardening operation was performed. Existing demo-operator login and read-only API/browser observations were used. Server-side bookkeeping associated with those reads is not represented as a new extraction run.

Evidence labels:

- **CODE:** executable implementation inspected, not merely a name, comment, import or protocol.
- **WIRED:** a consumer/entry point was traced to that implementation. An imported symbol alone does not qualify.
- **OBSERVED:** exercised on the current external preview, with a banked response.
- **HISTORICAL:** a retained receipt, not a current remote retest or an independent attestation.
- **GAP:** a specific missing function/binding in a traced path; not a claim that no alternative exists anywhere.
- **UNVERIFIED:** this review has not discharged the proof. Not synonymous with absent or broken.
- **DELIBERATELY DORMANT:** an unactivated learned capability can be legitimate under the Canon; it is not automatically a defect.

Source abbreviations used below:

- `B/` = `/app/backend/vendored/extraction_akki/backend/`.
- `F/` = `/app/frontend/src/`.
- `C/` = `/app/assessment_workspace/canon/`.
- `W/` = `/app/assessment_workspace/`.
- All `path:line-range` citations refer to source text lines, not generated-corpus offsets.

### Documentary coverage actually completed

The full on-disk text of core Canons 1–9 was read, including their tables: Custody Platform (206 lines), CIF (165), Governance Engines (265), Operating Engines (365), Interface Architecture (421), User Journeys (134), Integration and Quality (288), The Watch (223), and Mkondo Charter (74).

Additional full reads:

- `C/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt:1-528` (Document 0). Its later `C/drops/20260910/extracted/text/Akki_Governance_Architecture_v1_from_15.txt` differs only in the three ruling rows 524, 526 and 527; the full comparison and changed rows were examined.
- `C/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt:1-411`.
- `C/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt:1-132`.
- `C/drops/20260910/extracted/text/Ratification_Record_v1.txt:1-73`.
- `C/drops/20260914_pull_seam/extracted/The_Pull_Seam.txt:1-123`.
- `C/text/Audio_Intelligence_Plane.md:1-432`; byte-equal to the raw Markdown in the September 14 audio drop.

**Reading these documents is not equivalent to proving every clause against code.** The accompanying inventory covers 119 files, including duplicates, DOCX containers, archives and spreadsheets. Deterministic extraction and automated summaries were not counted as line-by-line conformance review. Not every amendment, spreadsheet cell, historical note, archive, or decision has received full semantic review. In particular, the versioned Master Requirements Registry, rule/entitlement/memory/agent amendments, all archive contents and the complete historical decision ledger remain to be reconciled. There are 336 top-level Markdown notes at the time of the final inventory, excluding this report's subdirectory. No claim is made to have read them all.

Backend/frontend coverage is deep on the cited paths, not a proof over every source file. The 52 JSX files under `pages/` are an inventory denominator, **not** a completed page-by-page functionality classification. Shared components, hooks and native routes invalidate a “no fetch in page = not built” method.

### Authority handling

Document 0 explicitly says **“Spec-drafted” and “spec-closed” mean documentation exists, not code** (`...Akki_Governance_Architecture_v1.txt:364-365`). Its dated “Not built” fields are therefore historical claims requiring a fresh code comparison, not present-day verdicts.

The later Document-0 copy resolves R-3 to Mkono IN / Grey Mirror OUT of the TCB, and R-5 to dedicated infrastructure per tenant (`...from_15.txt:524-527`). The older draft's questions must not be presented to the owner as unresolved again. R-2 explicitly corrects its own earlier allegation concerning Solva's floor: **no violation found** (`...from_15.txt:525`). This report does not resurrect that allegation.

Blank signature cells in `Ratification_Record_v1.txt:65-72` are not proof that later owner rulings never occurred. Conversely, a source comment saying “ratified” does not discharge the entire ruling history. Full ruling-to-implementation reconciliation remains open.

## 2. What is actually running in this preview

`/app/backend/server.py:14-48` selects a canonical working repository when present and otherwise the vendored backend. The canonical `/app/assessment_workspace/repos/Extraction-Akki` directory is absent here; the vendored source is the available runtime implementation. Historical repository bundles are not silently treated as the current working tree.

Current source inventory: **1,004 Python files** in the vendored backend, **130 immediate service directories** excluding `__pycache__`, and **52 JSX page files**. These are filesystem counts, not capability counts. The earlier “138 services / only 54 wired” characterization has no demonstrated call-graph basis; helpers can be called through other services, workers and routers.

The current OpenAPI response exposes **215 paths / 228 HTTP operations**. This establishes mounted surface area, not working workflows. See `runtime_get_receipt.json:16-30` and `get_01.json`.

`F/App.js:1250-1367` mounts native DAP and OS routes and redirects root to `/dap`. Legacy/prototype components coexist. An old comment describing the root as an iframe is not the current executable route tree.

## 3. GPUs: real access and execution evidence, not a failure assumption

### Built mechanisms

- `B/services/compute_seam/hardening.py:1-331` contains executable key installation, key verification, SSH hardening, password handling/scrubbing and result production. It is not just a proposed sequence.
- `B/routers/connect_gpu.py:1-63` routes GPU connection requests into `B/services/connect/gpu_submit.py:1-458`. The submit service has real/mock mode branches, invokes hardening in the real path and evaluates acceptance. The presence of the mock branch does not invalidate the real path.
- `B/services/training_runner/ssh_seam.py:1-240` implements key/password SSH selection and remote command/file-transfer operations. Current usability depends on its configured identity, not GPU health alone.

### Retained evidence

- `W/phase0/keypair_hardening_receipts/20260828T162822Z_step8_password_scrub_and_final_verify.json:1-22`: final key login exit 0 and `all_green: true` after the password-scrub sequence.
- `W/phase0/gpu_probes/20260922T190000Z_GPU_LANE_REVERIFY_A_TRIPLE_PRIME.json:1-95`: records successful verification across both GPU hosts. It is a dated receipt, not today's re-probe.
- `W/phase0/gpu_probes/20260922T010600Z_GPU_LANGID_FULL_SWEEP_LAUNCH.json:1-78`: real language-ID launch evidence, with a model/cache limitation recorded rather than hidden.
- `W/phase0/training_runner/runs/txttrain_20260831T193455Z_9594859a.json:51-84`: exit 0, two GPUs, a PEFT/LoRA causal-LM workload, 2,163.99 seconds, and training loss 0.7068903529. Its artifact and corpus hashes are recorded at lines 2-5 and 30-32.

The last receipt **also** states the shielding pipeline was not yet built for that historical run and identifies an owner-authorized build bypass (`:54-59`). It proves real training occurred; it does not prove that run exercised today's fully governed pipeline or that present language-cognition acceptance criteria passed.

### Current observation and limit

`GET /api/compute/estate` returns a real receipt-backed projection, but `B/services/compute_estate/estate.py:1-186` derives it from stored host/connection records. A displayed “reachable” value is not a fresh SSH or hardware test. No new GPU connection was attempted in this audit. The claim “pod key is out of sync with remote authorized_keys” is **not established** by this review and must not be treated as fact.

**Verdict:** real mechanisms and historical execution are built/evidenced. Current pod-identity reachability is unverified; GPU hardware failure is not established. Recovery authority remains available if a specific current failure is evidenced after the audit.

## 4. Census: real connectors and records, incomplete autonomous executor

### Built and wired

`B/services/census_autonomy/data_source_adapter.py:1-343` contains adapter selection, pre-read gating and registry-writer composition. It returns a closure for the actual source read; constructing that closure is not executing it. `producer_bridge.py:1-255` and `track_4_autonomy_wiring_v1.py:1-282` implement bridge/registration mechanisms. `scheduler_program.py:1-152` supplies a recurring entry point.

The legacy `B/services/census_engine/router.py:1-218` exposes census reads and a source-walk route; a separate legacy walk is not evidence that the new autonomous engine dispatches that walk.

### Confirmed execution gap

In `B/services/census_autonomy/engine.py:149-224`, the permitted branch writes a result containing the descriptor and the note:

> Commit-A shape gate landed; data_source adapter fold-in + sealed asset_registry_writer wiring in Phase 3 continuation sub-slices per R-106 §3.

It then records completion. That branch does not invoke the data-source adapter/run closure or a job-kind executor. The adapter's existence elsewhere does not repair this missing call.

This is not only a stale comment. **All 12 result JSON files** inspected in `W/phase0/census_autonomy_state/results/` carry that placeholder payload. They include `training_runs`, `lid_pass` and `census_three_waves` descriptors. Example: `20260925T021740Z_cr-13f0bd726716_result.json`.

**Verdict:** registration, scope/refusal machinery, scheduling entry point and result persistence are built. A result marked COMPLETE on the inspected branch proves the placeholder path completed, not that the corpus was walked or a GPU job executed. This directly conflicts with the owner's “Akki runs it; E1 wires and steps back” acceptance bar for the requested autonomy flow.

### Latest retained census, precisely stated

The current `GET /api/census/latest` returns census **4**:

- 8 clusters recorded reachable/authenticated; 0 recorded failed in that historical pass.
- 41 databases; 2,642 tables.
- **428,786,937 estimated rows**, not counted/ingested rows.
- Metadata-only scope: schema/table listings, `information_schema.table_rows` estimates, and column names/types.
- Per-column null counts explicitly deferred.
- Digicow RDS explicitly not walked in that pass.

Source: `get_05.json` and `runtime_get_receipt.json:72-90`; original `W/phase0/census/census_0004/manifest.json`.

That manifest describes its own path as direct `pymysql` from the pod after a bastion-path failure. **It is evidence of a historical metadata pass, not evidence of compliance with the current no-pod-data-path rule.** It is not permission to repeat that path. No assertion of corpus completeness, language coverage, row-level deduplication, null quality or FK completeness follows from these metadata totals.

## 5. Registry: real read surfaces, stale selections and constants

### Counterevidence to “Registry is hardcoded”

`F/components/Registry.jsx:49-98` fetches `/api/registry/facts` and renders returned facts. It is not correct to describe that entire component as hardcoded. `B/services/registry_facts/router.py:1-21` calls the assembler; `facts.py:1-319` reads stored evidence (and exposes configured-provider entries, which are not fresh connectivity tests).

`B/services/mtafiti/asset_inventory.py:34-100` implements enumeration, five-class counts and cross-class filtering over the existing asset writer. It supports source/model/artifact/receipt/rules classes rather than estate sources alone. `B/routers/portal_census.py:101-129` exposes that surface. This is positive implementation beyond Document 0's old G-3 description.

### Confirmed stale projection

`B/services/mtafiti/census3_registry_hydrator.py:646-670` enumerates exactly census 1, 2 and 3. The authenticated portal response reproduces that set, while the legacy census read returns 4 as latest. Authenticated `/api/portal/census/records/4` returns **404**.

This is a concrete selection/wiring gap, not missing census data. See `authenticated_read_receipt.json`, `auth_get_00.json`, `auth_get_01.json`, and `get_06.json`.

There is also a read-governance mismatch: the owner instruction retained in `B/routers/portal_census.py:26-31` requires census topology behind the existing portal identity gate. Anonymous `/api/portal/census/records` returns 401, but anonymous `/api/census/latest` returns the census manifest including estate topology (200). Both responses are banked. This is a confirmed difference between the two mounted read paths, not a separate security-audit sign-off.

The legacy registry facts response lists Digicow/ndume with verification timestamps in August, not the census-4 inventory (`get_04.json`). Therefore “the registry endpoint responds” does not establish current estate coverage.

### Mixed measured/estimated/literal presentation

`census3_registry_hydrator.py:697-749` returns fixed condition percentages. It labels them estimates, but those numbers are not recalculated from the current evidence within the functions. `:819-838` loads a launch receipt yet assigns `gpu_hours=1.2` and `utilization_pct=62.0` as literals. Those particular display values must not be represented as fresh telemetry merely because the surrounding payload cites a real receipt.

## 6. DAP: mounted request and entitlement surfaces are not completed workflows

### Request path

`F/pages/dap/RequestLifecycle.jsx:201-226` posts to `/api/portal/requests` and shows submission success when the returned status is OK. In `B/routers/portal_requests.py:140-177`, the mounted submit path constructs an acknowledgement rather than persisting and dispatching a real job; the list/detail paths at `:77-131` also retain stub behaviour. The authenticated list returns an empty row set (`auth_get_02.json`). No submission was performed during this audit.

**Verdict:** a frontend-to-router round trip exists. Durable request creation → commissioning → worker execution → result/receipt → request history is **not completed through this inspected portal path**. This does not erase separate internal commissioning machinery.

### Entitlement path

`B/routers/portal_entitlement.py:59-80` returns `licence: None`; `:88-112` returns an empty catalogue; `:120-157` calls the allowance derivation with a `stub-...` identity, fixed `2026-09` period, zero allowance and `ledger_events=[]`; `:165-199` returns empty badges while retaining the dial-admission symbol without executing a filter over real catalogue rows.

Authenticated runtime reads reproduce null licence, a stub allowance identity and empty badges (`auth_get_03.json` through `auth_get_05.json`). These are **MOCKED/STUBBED data bindings**, not evidence that the owner has no licence or has genuinely exhausted allowance. The derivation/contracts exist; real lookup and event-stream plumbing do not exist in these handlers.

## 7. Skills: provisioning implementation exists; answer execution is stubbed

`B/routers/transform_forms.py:51-76` calls the provisioning persistence implementation. `:79-124` invokes an identity/scope/floor gate, but constructs the successful query response using:

```python
"answer": body.get("answer_stub", "governed")
class_label = body.get("class_label", provisioning.floor)
```

The checked handler does not call a trained skill, retrieval engine or model to derive the answer. **MOCKED/STUBBED answer execution remains in this route.** Provisioning and a guard are real implemented pieces, not a completed callable-skill product.

`F/pages/dap/BuildSkill.jsx:107-110` uses `useBuildSkillProvisioning`; this is another counterexample to “no direct API call in page = unwired.” Its hook requests the real `/api/dap/buildskill/provisioning-records` route (`F/hooks/useBuildSkillProvisioning.js:30-69`). Authenticated direct GET returned an empty store, not an invented record list (`auth_get_06.json`).

There is a separate, source-confirmed UI token binding mismatch: the page reads `localStorage.dap_jwt` (`BuildSkill.jsx:32-39`), while normal login writes `sessionStorage.akki_access_token` (`F/lib/apiClient.js:45-57`); the hook only sends the token it receives (`:49-53`). The normal-login-to-skill-page journey was not replayed, so this is a static wiring finding rather than a claimed browser reproduction.

## 8. Training: distinguish three different execution paths

1. **Legacy training-runner LoRA path:** `B/services/training_runner/ssh_seam.py:552-565` invokes `execute_governed_lora_run` with `backend_execute=None` and `ssh_seam=None`. The pipeline passes the backend into the row executor and then stages the corpus (`B/services/shield_train/pipeline.py:290-350`); the stage helper calls `ssh_seam.run` / `ssh_seam.put_file` without a replacement default (`B/services/shield_train/pipeline.py:123-164`). None is not an executable dependency. Thus the checked legacy path cannot complete real LoRA training merely by selecting “real” mode; an earlier admission/classification refusal may stop it first.

2. **Campaign implementation:** `B/services/campaign_infra/production_trainer.py:266-381` really constructs the backend adapter and SSH seam, supplies both to the governed pipeline, stages corpora and invokes an on-host trainer. This is substantial real code and directly contradicts “all training is stubbed.” `run_queue.py:67-141` accepts an injected trainer, takes a per-host lock and refuses advancement without a real seal. **It does not automatically select `default_trainer_fn`.** The traced direct consumer is `W/tools/launch_campaign_run.py:97-120`, which uses a pod SSH override. Its presence is not proof of today's Akki-owned autonomous commissioning path and it was not executed.

3. **Language-cognition commission boundary:** `B/services/audio_plane_v1/language_cognition_v1.py:401-447` checks references and code-switched-material presence, then returns an `lc_training_run://...` handle. That function itself does not register or launch the run. `training_run_boundary_v1.py:275-302` validates anti-pod prefixes but does not enqueue anything. The separate Track-4 bridge can persist registrations; §4 explains why the inspected autonomous executor still does not perform training.

**Verdict:** real remote training capability and historical runs exist; current requested language-cognition commissioning, corpus assembly, calibration and full MOAC admission are not demonstrated end-to-end. A launch acknowledgement, opaque handle or training loss is not proof of the required per-language/code-switch/no-speaker-ID criteria.

## 9. Governance and operating engines: implemented mechanisms deserve credit

### SyniSense / custody crossing

The actual checked file is **`B/services/chokepoint/llm.py`**, not the `services/synisense/shield/llm.py` path in the handoff. Its `:260-534` path applies policy/containment checks, envelope construction, SDK selection, a model call, response handling and receipt creation. It is executable orchestration, not a placeholder declaration.

The receipt-writing helper catches failures (`:100-139`), and the Watch call receives substituted zero scores on the checked input path (`:366-384`). These need to be evaluated against the relevant receipt/failure and input-monitoring obligations; a chokepoint's existence alone is not a proof that every clause is discharged. No live model call or fault-injected receipt-write test was performed. No claim of an independently proven system-wide single-egress boundary is made.

### Watch

`B/services/watch/macho.py:1-178` implements threshold/decision logic; `mkono.py:1-189` implements action validation and receipt paths. Separation of detection from action is real. `input_seat.py:90-287` consumes supplied scores and returns an action. The checked chokepoint supplies zero input scores rather than a content-derived detector result. Therefore the **specific crossing's hostility-detection binding is incomplete**, not “the whole Watch does not exist.” Other sensor paths were not exhaustively traced.

### Northena / record ownership

`B/services/northena/ledger.py:1-176` implements opening runs, events, sealing, reading and job identity/fingerprint support. That is real record machinery. End-to-end Northena dispatch and universal handoff coverage were not fully replayed.

Core Canon 9 makes ownership explicit **per record class** (`C/text/Akki_Canon_9_Mkondo_Charter.txt:7-29`). Several record stores for different authorities do not by themselves violate “one record.” This review does not assert duplicate authority merely because MongoDB, JSON records and per-class stores coexist.

### Targeta

`B/services/targeta/core.py:22-78` implements a hard defensibility-class filter and stable deterministic ranking. Its relevance function is explicitly simple (`:27-36`). `gate.py:59-86` refuses absent thresholds/data/functions, but its coverage-veto arm is fixed `False`. `compose_ordering` calls `evaluate_gate(thresholds)` without a held-out set/functions (`:101-103`), so the inspected normal composition stays core-only. This preserves deterministic operation; it does not establish a deployed learned yield optimizer or complete per-class coverage-veto implementation. Dormancy is not automatically a violation under core Canon 4's deterministic-first doctrine.

### CIF

`B/services/cif/detection.py:52-112` constructs typed proposals; `acceptance_point.py:1-100` implements a deterministic acceptance predicate. `output_routing.py:108-178` routes accepted proposals to capability registration or a research-loop sink. These are built mechanics. The research-loop sink is an in-memory list (`:105`, `:176-178`), with full ledger integration explicitly deferred (`:66-68`). They do not by themselves prove a durable, continuously learning conditioned faculty, archive resurrection, or class-retirement loop. No claim that every CIF mechanism is absent is made.

### Document-0 attributes / asset taxonomy

`B/services/doc0_attributes/tcb.py:26-106` enumerates classifications; `triad.py:11-55` enumerates principals/assets/operations and operation-to-checkpoint mappings; `determinism.py:18-45` supplies classification/gating; `mtafiti/asset_inventory.py:34-100` supplies the five-class reader. These directly contradict treating the old documentary gaps as untouched. Enumeration existence still does not prove inventory completeness or mediation of every runtime operation. For example, the current TCB tuple is not automatically equivalent to the 27-component document inventory.

**Still unverified in this pass:** complete Solva grounding/assertion/reasoning journeys; universal Mkondo handoffs and ceremony recovery; end-to-end memory capture, compaction, revocation and reload; all model-admission/release-budget paths; all rule-service obligations. A located router or dataclass is not a substitute for those traces.

## 10. Audio: significant implemented contracts and algorithms, not a proven trained plane

Full audio spec read: `C/text/Audio_Intelligence_Plane.md:1-432`. Its important boundaries include tokens rather than waveform carrier, in-perimeter operation, baseline capture independent of commission, empirical calibration, defined strata and all-criteria acceptance.

- `B/services/audio_plane_v1/language_identifier.py:174-205` actually invokes an injected language-ID backend per segment. The unratified backend is just one refusing implementation (`:127-154`), **not proof that no later concrete backend was used**. Historical LID receipts provide counterevidence.
- `ingestion_capture_v1.py:106-220` composes detected language, separately cited station prior, condition references and switch-point evidence, and refuses missing baseline capture. This preserves an important distinction: vernacular station identity is not falsely promoted to model-confirmed language.
- `character_register_clustering_v1.py:67-169` implements deterministic clustering and clears the provided embedding list before returning group centroids. It is not merely a protocol. Clearing that list is not, by itself, proof of destruction of every external alias or physical-memory copy; no stronger assurance is claimed.
- `calibration.py:80-168` implements carriers, volume-count checks, confidence-interval shape checks and a calibration-presence refusal. It does **not** execute the required multi-volume training/evaluation or fit a scaling curve; the values arrive from outside that module.
- `training_planner.py` implements a deterministic/learned ordering seam and reproducibility structures. The full production-bound planner and calibration executor were not traced; the source itself bounds the early layer as protocols and synthetic fixtures.
- `training_run_boundary_v1.py` and `language_cognition_v1.py` implement commission/precondition contracts but do not themselves establish successful training, per-stratum testing, admission and promotion.

**Verdict:** audio governance/type boundaries and some algorithms are built; estate-wide capture completeness and the requested trained language-cognition model are not proven. No corpus location/key failure is invented as the explanation for that uncertainty.

## 11. Frontend: do not collapse unlike states into “43 fake pages”

Observed categories, with examples:

| Category | Evidence | What it establishes |
|---|---|---|
| Literal illustrative estate figures | `F/pages/dap/DAPLanding.jsx:1-196`, `DataEstates.jsx` | Landing's 81.0 TB, five estates and access totals are source literals, not current census calculations. |
| API-backed component | `F/components/Registry.jsx:49-98` | Fetches facts; freshness/completeness depends on the backend projection. |
| Shared-hook-backed page | `F/pages/dap/BuildSkill.jsx:107-110` | Real provisioning read hook exists despite no direct fetch in page body; token mismatch remains. |
| Composed workflow | `F/pages/os/WorkCommission.jsx:27-76` | Renders `CommissionWizard`; cannot be dismissed because the wrapper does not fetch. Full wizard execution was not retested. |
| API-backed but stubbed backend | RequestLifecycle, Entitlement | A successful HTTP round trip is not a complete business flow. |
| Explicit pending/static/reference views | Multiple OS/DAP pages | An honest gap or specification explainer is not fabricated operational evidence, but is not a delivered interaction either. Exhaustive classification remains open. |

Browser baseline at **1920×800** rendered the DAP landing. At **390×844**, the large fixed sidebar left a narrow content strip with overlapping/squeezed chart labels. Screenshots are banked in this audit folder. This is an existing responsive defect observed during review; no UI changes were authorized or made.

## 12. Verification performed and not performed

Banked current checks:

- Ten unauthenticated GETs in `runtime_get_receipt.json`: health, OpenAPI, deliverables, compute, facts, census, protected portal reads and Canon rule rows.
- Existing demo-operator login returned HTTP 200; seven authenticated GETs in `authenticated_read_receipt.json` reproduced census 1–3 / census-4 404, empty request history, null/stub entitlement views and empty skill provisioning.
- Desktop/mobile browser baseline; screenshot files and console log retained.
- Source inventory, original-source line citations and response SHA-256 values retained. These establish provenance, not cryptographic proof that historical external events occurred.

Not performed: full backend/frontend regression suite, write-flow exercise, reboot/recovery, ledger fault injection, source-data pull, GPU probe, training, MOAC evaluation, privilege-boundary/security audit, or independent assurance.

The vendored tree's only `test_*.py` filename match is `B/services/training/test_set_seal.py`, a production test-set-sealing module, not the historical test suite. `/app/test_reports/iteration_1.json` is a previous report and was not represented as newly rerun. Source snapshots/archives and their test suites still need explicit version alignment before any full-suite claim.

## 13. Priorities arising from evidence — not implementation performed

### P0 — finish the requested audit

1. Reconcile every remaining Canon/amendment and Master Requirements Registry row to authority/version, implementation, consumer, receipt and verification method. Keep unexplored rows OPEN, not “not built.”
2. Complete path-by-path Solva, memory, rules, model admission, budget, handoff and frontend coverage. Distinguish deliberate dormancy from missing required execution.
3. Preserve the already-proven gaps: autonomy placeholder COMPLETE, portal request/entitlement bindings, census-4 omission, inconsistent census read gating, literal telemetry and callable-skill answer stub. Do not merge these distinct problems into “GPU access.”

### P1 — after audit, within existing architecture

- If Akki's own current connection/acceptance path evidences an identity failure, use its key-install → verify → harden → scrub pipeline, with receipts and recovery/verification. Do not generate a competing pod identity or weaken the host speculatively.
- Repair the existing producer → bounded executor → owned registry path, rather than launch another pod extraction script. Descriptor wiring alone is insufficient until the consumer actually executes it.
- Correct the existing portal read selections and honest states; do not create a second registry to conceal stale projections.

### P2 / backlog

Full content-quality/FK/dedup measurement where deferred; evidence-bound language-cognition corpus/calibration/MOAC/admission; remaining responsive issues; regression suites aligned with the deployed source snapshot. Previously asserted external credential/location blockers require fresh evidence before being repeated as current facts.

**Useful enhancement after the audit:** one receipt-backed freshness/measurement indicator on the existing registry, showing measured versus estimated versus not-read values. It should derive from Mtafiti's record, not create another summary store.

## Bottom line

Akki is not an empty façade. Real governance mechanisms, source adapters, inventories and GPU/training work exist. The strongest confirmed deficiencies are at **specific execution and evidence-projection joins**. The new autonomous pipeline can currently report completion without doing the commissioned work; the portal can acknowledge a request without commissioning it; real census records can be omitted by the portal; and real receipts can surround literal display metrics. Those findings are supported. A global “built/not-built” percentage and an exhaustive Canon-compliance sign-off are not.