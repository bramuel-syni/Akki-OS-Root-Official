# Akki — product requirements and current continuity

## Original product goals

- Increase batch throughput and H200 utilization for language-cognition and generalized M9 training, without weakening privacy, quality or admission requirements.
- Build the generalized M9 model pipeline beyond audio: qualified data, reproducible training, evaluation, certificates, admission and separately governed serving.
- Provide deep RMS data-estate intelligence: duplication, quality, degradation, dimensional monetization and evidence-backed cost reduction.
- M6: produce useful artifacts, deterministic decks and callable skills from qualified work.
- M10 standalone requirement: system-wide UI/UX review and revision—declutter technical noise, use editorial/direct copy rather than feature explanations, replace visible token-like IDs with meaningful document/artifact names, and modernize deck presentation while preserving workflows and safeguards.
- Deliver the broader Akki promise through identity-bound governed work: Registry/census, Watch, request-to-delivery, grounded answers, durable memory, collaboration, commercial controls and recovery. Functional outcomes and evidence—not scaffolds or old seals—determine completion.

## Governing roadmap and authority

`assessment_workspace/notes/goal_delivery_20260928/AKKI_GOAL_ROADMAP_v1.md` is the owner-approved goal-based roadmap. Its current meanings are:

M1 Registry/deep census → M2 Grey Mirror/Watch → M3 request-to-delivery → M4 useful grounded answers/context → M5 durable memory/collaborative work/goals/board → M6 artifacts/decks/callable skills → M7 tenant/rule/entitlement/commercial operation → M8 failure/withdrawal/continuity/recovery → M9 activated media/model/training capability → M10 independent integrated acceptance.

- `FAMILY_OWNERSHIP.json` routes the historical56 families/648 rows. Routing is not fresh clause-level closure. Prior milestone numbering is not transferable acceptance evidence.
- Preserve proven work; reopen only demonstrated regression, invalidated evidence or an explicitly changed requirement. No invented approval gates, timers, recipes or thresholds. The owner authorized explicitly labelled implementation-percentage estimates on30Sep; these are planning judgments, never measured acceptance or replacement gate criteria.
- Banked owner UI/prototypes remain the design authority. Connect original interactions rather than replace them with generic surfaces.
- English only. E1 is the control plane: no dataset extraction, training or heavyweight data processing here. RMS remains census-only unless its owner explicitly authorizes otherwise.
- M5 UI is paused under the existing “skip m5” direction; four post-M3 journey proposals remain parked. A readiness request does not unpause implementation.

## CURRENT — 2026-09-30 19:09 UTC training status and M10 presentation mandate

- Owner requested milestone percentages and a standalone M10 system-wide UI/UX overhaul, then asked “What is the status of the training?”. UI implementation has NOT started. Prioritize Documents, Census and Estate Intelligence, then inventory remaining screens; M5 remains paused and skill executor activation held.
- Reported directional implementation estimates: M1 ~80%; M2 ~80% broader scope / 100% signed-off slice; M3 ~70%; M4 ~75%; M5 ~55%; M6 ~80%; M7 ~45%; M8 100% of agreed nondeferred scope; M9 100% of activated text scope; M10 ~10%. These are planning estimates, not fresh acceptance scores. M8 site restore/notification and M9 dormant modalities are NOT claimed complete.
- Fresh authenticated external-preview GETs: M9 jobs/models/capabilities/readjudications and LC jobs all 200. No nonterminal training job appears in either job list. Both main text runs completed; 8B full/pruned admitted, 1.7B full/pruned refused for Swahili regression. Full 8B macro held-out accuracy 0.97213, coverage 7/7; this is text language identification, NOT a QA executor.
- Fresh host-backed 8B health GET: serving, registry admitted, artefact unaltered; 1,174 texts served / 331 requests. Load-test status refresh banked its completed terminal receipt (finished 07:23:21Z), superseding the stale list label “running”. No training/start/stop/classification request was issued.
- Important LC continuity correction: the older “recipe sweep awaits owner decision” note is stale. Live job records contain an owner-authorized milder-recipe sweep, four later 40-epoch runs completed by 05:12:40Z on 30 Sep. Each ~2,698–2,707 windows/s, batch 2,048, physical batch 1,024, ~50.73 GB. All remain NOT ADMISSIBLE: per-language quality gaps, speaker leakage and missing labelled code-switch/English/Sheng data. Latest four archive-test accuracy on judged windows ~61.56–68.83%, with differing abstention rates; not an acceptance pass. Audio stays dormant/research-only under the later 2a completion ruling.
- This was a status read, not a new GPU-utilization sample or whole-product test. No application code, training recipe, job launch, credential, admission or owner hold changed.

## PREVIOUS — 2026-09-30 M6 follow-on: v1.2 workbook, commission-close, page thumbnails, M6-T4 boundary (owner rulings 1a/2b/3b/4b/5a)

Evidence: `notes/m6_execution/M6_DOC_STUDIO_INSTALL_20260930.md` (addendum) and `notes/m6_execution/M6_T4_CALLABLE_SKILL_BOUNDARY_20260930.md`.

- **doc-studio v1.2** (ruling 3a): `render_xlsx.py`/`studio.py`/`workbook.schema.json` accept declared option rows; estate commission now ships a workbook with a live option model. INSTALL_MANIFEST lists five approved edits; 34 files byte-identical to the owner package.
- **Commission-close producer** `POST /api/studio/producers/commission-close/{eij}` → decide pack (close/hold). Live `com-c3d53a38d18f` released, byte-identical, pptx·docx·html·xlsx.
- **Page thumbnails**: rendered at build (LibreOffice → poppler, 60 dpi), served per page; `components/studio/DeckThumbnails.jsx` grid + enlarged page view in WORKSTUDIO · Documents. Verified at 1920×800 and 390×844.
- **M6-T4 boundary proven to a receipted hold**: DIGICOW operator holds key grant `6090156f3b936c22e8267fff` (external · governed_extract · utterance · digicow_rds, grantor `owner-ruling:M6-T4:2026-09-30:2b`); skill `1a03977aeac14421a980890f6622c91f` is write-once bound to `akki://artifact/DIGICOW/req-97999a0b46d2f51564b85dcd05d871a2/qualified-units`. Live `POST /api/callable_skill/{id}/query` → 409 `held · SKILL_NATIVE_PLAN_REQUIRED`, intent + view receipted on the tenant Ledger; duplicate key → no duplicate effect; anonymous 401 / no grant 403 / unknown 404 / no key 422. **Grounded result HELD by owner rulings 3b/4b** (no QA executor admitted, no `skill` kinds/permissions on the runtimes). Tool: `tools/m6_skill_binding.py` (idempotent).
- **Verification (condition C, terminal pytest)**: `tests/m6_doc_studio` 20 passed · `tests/m6_decks` 14 passed · `tests/m6_callable_skill` 11 passed. Finding on record: `POST /api/transform/callable_skill/provision` has no identity gate (unchanged, pending ruling).
- **To unhold M6-T4**: owner admits a QA-capable executor → DIGICOW ceremony with `kinds=[source, skill]` + `skill_response`/`anchor` permissions → skill commission (Plan/approvals), `skill/solva` adapter, eligibility + handoff providers → worker skill mode + inspector anchors → same live suite must return `200 · ready · GROUNDED_SKILL_RESULT_VERIFIED`.

## PREVIOUS — 2026-09-30 M6: doc-studio v1.1 installed as the primary production skill (owner-approved rulings 1–4, conditions A–D)

Owner uploaded `files (21).zip` (doc-studio skill: brief → content model → CIF verdict → format specs → build --prove → freeze → QA → deliver → revise) and ruled it the primary production skill for document production. Evidence: `assessment_workspace/notes/m6_execution/M6_DOC_STUDIO_INSTALL_20260930.md`.

- **Installed verbatim** at `services/transform_forms/doc_studio/skill/` with `INSTALL_MANIFEST.json` (v1.0 owner hashes vs v1.1 installed; only `scripts/build.py`+`scripts/qa.py` changed — they read `DOC_STUDIO_TOOLS_DIR`; condition A). In-repo office tools under `doc_studio/tools/`. LibreOffice 7.4.7.2 + python-pptx 1.0.2 + matplotlib 3.11.2 installed; the environment is pinned in every build manifest (ruling 1).
- **Deck engine** `/api/decks/*` kept read-only for its one recorded deck; doc-studio recorded as the DRE reference implementation (ruling 2). **Direction stage**: operator-authored verdicts under standing frame `FR-strategy-decide-v1`; non-routine → CIF ideas endpoint (not mounted → refused); no LLM path (ruling 3). Defaults `house-neutral` / "Tenant confidential" / seed = content_id/purpose/date / build_stamp frozen at creation (ruling 4).
- **Adapter** (`doc_studio/{install,store,frames,manifest_template,producer_estate,receipts,service}.py`, `routers/studio.py` → `/api/studio/*`): file-backed tenant store (condition D), census→commission producer whose verdict manifest is generated from the brief (condition B), `platform_ref` receipts resolved at build (unresolvable → blocker), prove-build, revise (strike detection), re-verdict, PDF export, downloads.
- **UI**: WORKSTUDIO · Documents (`/os/work/documents`) is the studio; Estate Intelligence has "Commission board pack".
- **Verification (condition C, no testing agent)**: `pytest tests/m6_doc_studio -n 0` 19 passed — evals 1–3 in-pod (eval 1 byte-identical, pptx hash equals the owner's shipped manifest; html/docx/xlsx differ by environment as expected), lifecycle offline, live API reads/refusals. `tests/m6_decks` 14 passed.
- **Limits on record**: no workbook for the estate commission (studio Options/Checks sheets are bound to the option-model shape); in-repo validators are not OOXML schema validators; PDF outside byte-identity; G6 still open (M6-T4 external skill call, M6-T5 async/late refusal not exercised).

## PREVIOUS — 2026-09-30 M8/M9 completion (backend + Model Approval UI)

Owner asked “Can we complete M8 and M9 fully”, ruled 1a/2a/3d/4c/5a (recorded in `assessment_workspace/notes/m8_m9_completion_20260930/OWNER_RULINGS_20260930.md`), then chose plan A for the UI. Owner's stated next wave after this: **M6 (~50%) and M5 (~55%) pending work**.

- **M9:** per-stratum acceptance = Outcome floor AND no regression below base (1a). Re-adjudication admitted 8B `m9j-74af7cef0a85` (full + pruned) → registry v3; the 8B full adapter is served on akki-vm-ii:8611 (`m9j-934daf924154`), live health returns artefact-unaltered + served/refused counters + p95. 1.7B remains refused on `swa`. LC audio is dormant/not-activated for G9 (2a). APIs: `/api/training/m9/{models,capabilities,readjudications,serving/{id}/health}`.
- **M8:** BC tiers ratified as proposed in `BC_DYNAMIC_RECOVERY_PACKET_20260915` (5a); drills M8-T1/M9-T3 interrupt-and-resume (110 steps ≈ 67.5s lost, RPO 900s, five carriers restored) and M8-T3 Ledger PITR (3,506 rows in 0.349s, chain intact, Ed25519 countersign from akki-vm) both PASS. M8-T4 site restore (4c) and M8-T5 real notification delivery (3d) are **deferred by owner** and shown as deferred, not claimed. APIs: `/api/continuity/{drills,policy}`. Services: `services/business_continuity/{policy,ledger_archive}.py`, `services/training_runner/m9_{worker,dispatch,serving,drills}.py`.
- **UI (this session):** `/os/admin/modeladmission` (APPROVALS · Model Approval) is now LIVE — replaced the honest-gap stub with `components/models/{ModelRegistry,ModelAdmissions,RecoveryDrills}.jsx` + `useModelApproval.js`, same `usePrototypeSession`/`CensusAccess` gate and `estate.css` language as Estate Intelligence. Sections: registry (with per-model “Check health”), admission decisions (per-stratum adapter/base chips, failing strata tinted), G9 capability account (activated vs dormant), failure & recovery evidence (drill receipts, four ratified tiers, owner deferrals). Testing agent `test_reports/iteration_69.json`: frontend 100% at 1920×800 and 390×844, no overflow, live health read succeeded, Estate Intelligence regression OK.

## PREVIOUS — 2026-09-30 owner-requested M1–M10 progress recap

Owner asked: “Reflect back all the milestones and give me % status progress for each and state the details and to dos for each thats not done.” Approved estimated-implementation reporting with “Go ahead.” No application or training changes authorized by this report.

- Full recap: `assessment_workspace/notes/goal_delivery_20260928/M1_M10_PROGRESS_20260930.md`; public copy `frontend/public/briefs/Akki_Milestone_Progress_20260930.md`.
- Directional estimates: **M1~80%; M2 signed-off slice100% / broader coverage~80%; M3~70%; M4~75%; M5~55%; M6~50%; M7~45%; M8~35%; M9~65%; M10~10%**. Not calculated from tests/files/epochs, not an overall-readiness average and not remaining-work-hour estimates.
- **Preserve scoped G2 PASS:** `notes/m2_execution/M2_WATCH_READINESS_AND_CLOSURE_20260929.md` verifies three commission gates + four-panel console. New paths and documented independent-watchdog/learned-detector/profile gaps remain extensions, not erasure of that sign-off.
- **Freshly reconciled M9 terminal evidence:** both full text jobs completed; both original/pruned candidates refused admission on `coverage_strata`6/7 vs required7/7. Neither registered/served. Certificates contain checkpoint adapter-state parity and drafted whitepapers; physical full-state/process-loss recovery remains narrower/unclosed. Earlier “full runs awaiting terminal” prose is stale.
- **M6 correction:** active router is `/api/decks/*`. Code asserts determinism on HTML, not PDF bytes. PDF export exists; PPTX and UI/callable-skill acceptance remain open.
- Corrected earlier M7/M8 report's acceptance-pack ID mapping to the canonical roadmap (M7-T3 usage, T4 limits, T5 attribution; M8-T1 interruption, T2 critical failure, T3 Ledger restore, T4 site restore, T5 recall/notifications). Findings/gate verdicts unchanged; note recorded in the report.
- Reporting validation: cross-checked the roadmap, retained milestone/test notes, current deck code, campaign JSON and actual model-admission records. No fresh whole-platform acceptance test or GPU probe was performed.

## Recent evidence — 2026-09-30 M7/M8 read-only readiness completed

Latest user sequence: asked for another M6/M9 requirements/repos sweep, redirected to **“Do a readiness run for M7/M8”**, then **“Proceed with your plan.”** Approved plan was read-only; no application behavior, authentication configuration, training jobs, rules or tenant business records were changed.

**Verdict:** M7 and M8 are **not acceptance-ready**; useful foundations exist and targeted implementation can proceed under its own scope. G7/G8 remain unpassed; no current acceptance pack was fabricated from historical seals.

Evidence and deliverables:
- `assessment_workspace/notes/m7_m8_readiness_20260930/READINESS.md` — full requirements/reuse matrix, ten acceptance packs, UI integration gaps, P0/P1/P2 sequence.
- `.../SOURCE_MANIFEST.json` —24 selective pinned donor-source reads and39 current evidence-file hashes; not whole-repository coverage.
- `frontend/public/briefs/Akki_M7_M8_Readiness_20260930.md` — downloadable report copy.
- `test_reports/iteration_68.json` — raw testing-agent report; **read `iteration_68_resolution.json` before acting on its generic auth recommendations**.

Repository heads reverified:
- Akki-Executive-Core: `5844eee95d5faffea0dcab98bd4fe5e8d1419f32`.
- RMS-IQ-Core-2: `ea5aa019521eee22ad4f8ea29efdfa2af357be3b`.
- Akki-OS-V1: `8c361903cdd319bfdc0709de3f4392f5bfa3956b`.
- Akki-OS-Root: `c481c1d65eb6ddd2c6630d31a736d11e46e1641a`.
- Current native billing/execution work is ahead of Root; RMS-IQ's sampled checker/revocation mechanisms already match the current vendored code. Executive-Core billing is explicitly coming-soon, not a usable current commercial implementation. OS-V1 commercial code was cut/archived. Do not overwrite current work or import a parallel authority.

### Verified in this run

- **103 scoped automated checks passed:91 existing isolated tests +12 corrected public-preview API tests.** Separate11-test M4/M5 XML is already included in91.
- Both existing tenant operators: login and `/api/auth/me`200; missing-auth reads refused; tenant-bound overview and live entitlement/billing reads work; retained census detail denies the other tenant in both directions.
- Normal RMS browser sign-in passes. Rules Updates and Entitlement render at1920×800 and390×844; inspected entitlement view has no mobile overflow.
- Historical403 not reproduced. Correct login result key is `access_token`, not `token`. Existing allowlist was already permissive; no gate/config change or strict-ingress assurance.
- Testing-agent cross-tenant test used the obsolete `rows`/numeric-ID envelope. Corrected to `records`/`record_id`, retested12/12 with no skip. Test credentials now injected through environment; no users created or modified.
- Offline evidence uses **MOCKED/SYNTHETIC workers/providers/adapters** in many suites; isolated compaction also exercises stored Mongo bytes. No preview API was mocked. No live outage, restore, notification, provider spend, GPU interruption or serving admission was performed.

### Open M7/M8 findings

- **M7/P0:** checker publishes effective state before its Ledger emission; legacy requests lack tenant scope; global system rules need explicit authority rather than reuse as tenant rules. Three partial lifecycle paths need convergence onto durable native Ledger/ROC/RBM publication. These are source-traced findings, not a live mutation exploit.
- **M7/P1:** Rules Updates remains an explicitly unwired page. Full seat/agent/profile, licence/catalog ceremony, customer-provider-key custody, organization ceiling concurrency, rollover/top-up and real nonempty usage-bill acceptance remain.
- Both operator catalogue views showed zero admitted rows; RMS period bill was resolved but empty, `scope=principal`, `financial_invoice_issued=false`. Successful empty reads do not prove commercial operation.
- **M8/P0:** continuity service records attestations, not measured restoration; breach service writes local alert files, with no delivery/ack consumer found. Need independent verifier, actual storage recovery and real recipient acknowledgements.
- **M8/P1:** interrupted graph-wide rights withdrawal/model recall, warm-memory re-derivation, TCB outage matrix, containment persistence, isolated process-loss/single-effect and full GPU-state checkpoint restore proofs remain.
- Existing Ledger recovery objective is3600s and qualifying-breach window72h. BC-3/BC-4 require owner-ratified dynamic tiers per `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md`, not invented static RPO values.
- Generic five-failure lockout, new cookie transport and password-overwriting seed behavior are not current Akki acceptance contracts. Missing rate limiting is a separately tracked hardening consideration; no auth repair was made.

## Inherited implementation snapshot — not re-certified by this assessment

### M9 generalized training / language cognition

- Throughput work in `services/training_runner/m9_worker.py`: token-budget batching, quantized-width ladder, per-base recipes, gradient-checkpointing control and padding metrics. Prior measured1.7B throughput16.6k–18.3k tokens/s;8B6.7k tokens/s. See `notes/m9_execution/M9_GENERALISED_TRAINING_20260929.md`.
- API-only campaign `assessment_workspace/tools/m9_campaign.py`; records in `notes/m9_execution/campaign_20260929_full.json`; API `/api/training/m9/*`. Recap inspection found selected8B `m9j-74af7cef0a85` completed00:48:34Z and runner-up1.7B `m9j-6af6e8c370f9` completed00:14:33Z on30Sep. Both full/pruned admissions refused `moac_criterion_below_floor` on `coverage_strata=0.857143`, floor1.0; no registry version. Terminal completion is not model acceptance. No job was altered or relaunched.
- Last recorded LC fixed-recipe A3 `lcj-427526d3a19a` and B3 `lcj-2add4984931e` completed60epochs; both **NOT ADMISSIBLE** (accuracy/abstention and speaker leakage; B3 class collapse). Throughput is not quality acceptance. Recipe sweep awaits owner decision; `notes/m9_corrective_training/EXECUTION_20260929.md` is the live evidence authority.
- M9.4 serving is separate, not started in this assessment. M9 gates/certificates/admission remain required.

### Estate intelligence and M6

- Deep report and `/os/admin/estate/intelligence` exist, including duplication, degradation, grain/licensable-unit candidates, monetization blockers, cost strategies and governed dossier. Huawei OBS/NAS metrics and source limitations remain evidence-based.
- Last documented RMS census `eij-1b359b3cbd2e`:20db/1006tables/351.3GiB/~259M estimated rows; artists_app blocked. Earlier tests iteration67:backend16/16 and desktop/mobile verified. This run did not repeat all analytics tests.
- M6 deck backend exists under `services/transform_forms/deck_engine/`, routes `routers/decks.py` mounted at `/api/decks/*`; prior handoff reports offline tests. Current determinism claim is HTML artifact bytes, not PDF bytes; PDF export exists, PPTX not built. Deck generation/view/download UI and real callable-skill acceptance remain open; no new deck work was done here.

### M3 / M4 / M5 inherited evidence

- M3 DIGICOW live source→verified artifact, cancellation, write refusal and stable retrieval evidence is in `notes/m3_execution/M3_LIVE_EXECUTION_20260929.md`. RMS not extracted. DIGICOW time-boxed HTTPS custody origin remains a separate ruling/binding; shared-mount result is not an HTTPS delivery link.
- M4 governed chat (`services/chat/*`, `POST /api/chat/ask`) is identity-scoped, uses qualified whole-unit windows and warm/fresh/refused decisions with evidence; fresh routes to a draft, not automatic dispatch. `/os/work/chat` exists.
- Durable sessions/compaction/reload/tamper/lineage exist; M5 task/document/goal/board/withdrawal backend references in `services/work/*`. User paused M5 UI. R-21 personal memory remainsOFF; no formal G4/G5 closure is inferred here.

## Architecture and key boundaries

- React frontend + FastAPI wrapper `backend/server.py` + vendored implementation at `backend/vendored/extraction_akki/backend/` + MongoDB. Mounted route order matters: native tenant-scoped routers precede or quarantine legacy unscoped aliases.
- Native control events: `services/ledger_writer/mongo_control.py` and `principal_control.py`; atomic row+payload, tenant-qualified uniqueness, authenticated actor binding. Legacy JSON/JSONL ledgers and RAM registries still exist; their mere presence does not prove shared durable runtime authority.
- Native orchestration: `services/northena/execution_*`; portal read/write composition: `services/portal_operational/*`; source admission: `services/estate_admission/*`; training/extraction execute on existing governed remote workers, not in E1.
- Environment is authoritative: frontend `REACT_APP_BACKEND_URL`; backend `MONGO_URL` and unchanged `DB_NAME`. Keep supervised ports and existing credentials. Read `memory/test_credentials.md` and `auth_testing.md`; do not seed/reset accounts to make tests pass.
- Default M7/M8 follow-up is scoped repair then genuine acceptance drills, not adding another billing database, policy store, scheduler or notification-success mock.

## Continuity documents

- `memory/ROADMAP.md`: prioritized next actions and retained backlog.
- `memory/CHANGELOG.md`: dated progress notes.
- The former723-line PRD mixed historical checkpoints with current state. Its complete byte-preserved copy is `memory/archive/PRD_20260930_before_M7_M8.md` (SHA256 `f7a397cca925f59863a257481f59620f6de887fec3acde85890f17287ef29775`). It contains all older implementation details and source pointers; read current sections here first.