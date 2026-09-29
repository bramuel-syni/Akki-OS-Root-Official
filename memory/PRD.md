# Akki — product requirements and current continuity

## CURRENT — 2026-09-29 (night) M3 request→verified result PROVEN LIVE on DIGICOW · M3.3 delivery = ruled rest-in-store · UI wiring OPEN

Owner directives this increment: "a" (proceed autonomously with the 4-step plan); "switch — remember you
cannot extract data from rms" (RMS is census-only; extraction scope stays DIGICOW / AKKI-TEST). English only.
E1 stayed control plane: bytes moved akki-vm → `/mnt/akki-storage-3388s`; E1 saw metadata + signed receipts.

**Live proof (deployed backend, operator `demo.operator@demo.digicow.example.com`, see
`assessment_workspace/notes/m3_execution/M3_LIVE_EXECUTION_20260929.md`):**
- M3-T1 `req-97999a0b46d2f51564b85dcd05d871a2` (`digicow_live.training_questions`, max 200): warm feasibility →
  zero-rate quote → requester + interim stand-in approvals → cpu-class dispatch to akki-vm → envelope ack →
  200 scanned / 200 qualified / 2 PII-floor redactions → sealed 341,643 B → independent inspection on
  akki-vm-ii → registry → rights follow lineage → settled + metered → **terminal `ready · VERIFIED_RESULT_RECORDED`
  (measured)**; identical after 11 retrievals and a backend restart.
- M3-T3 `req-393db89ef35ac94ccae17770f52b1c1f` (`shortcode_response`, max 20,000): sizing now MEASURED from 2
  settled runs; `running` → requester stop → cancelled at 2,500 rows, usage metered, nothing published.
- M3-T5: DELETE/UPDATE/DROP/INSERT refused on akki-vm before any connection, 4 signed refusal receipts banked.
- M3-T4: widened intent → version 2 (v1 immutable); revise-commissioned 409; un-censused → `unknown`; `users`
  floored on 6 personal columns; withdrawn/duplicate freeze 409; cross-tenant 404, analyst 403, anon 401.
- M3.3: `POST /delivery` → custodian verified size then **held `CUSTODY_ORIGIN_UNAVAILABLE`** (shared store has
  no HTTPS origin — the ruled pilot state; artefact rests in the tenant's store).

**Fixed this increment (each surfaced live):** NEW `extraction_runtime/derived_rights.py` — rights authority
extends the source grant to a verified artefact along worker-signed lineage (idempotent; withdrawn parent
holds), called from `IndependentInspector.inspect` before the registry is written (publish gate was holding
every completed run at `NATIVE_RIGHTS_PROOF_REQUIRED`); inspector freshness stamp = recorded inspection time
(was `now()` → `ARTIFACT_REGISTRATION_CHANGED` on every revalidate); `_REQUIRED` holds are `Interrupted`
(retryable) not `Blocked`; custodian `Held` propagates from `custody_delivery/service.py` with honest
disclosures; run-view `active_compute` consumed mapped. Offline `tests/m3_commission` 10/10 (+ lineage-rights
test); regression 170 pass over m3_commission/non_gpu governance/execution_spine/portal_operational.
Two live legacy tests (`test_entitlement_allowance_without_licence…`, `test_execution_advance_held_unbound…`)
assert the pre-ceremony world (no RMS licence / no bindings) — superseded, not regressions.
`test_non_gpu_worker.py` failures are pre-existing at git HEAD.

**Standing limits:** `req-c1f2738b3449081569aebfbfd537e2a6` (first completion, pre-fix) is `Blocked` on
`ARTIFACT_REGISTRATION_CHANGED` (now disclosed honestly) — registry written before rights existed with a
call-time stamp, immutable; rights later extended by `m3_extend_rights.py`; real work metered.
Testing agent iteration 64 (13/15; the 2 "failures" were my brief's wrong expectation of `Interrupted` for
this refusal) → suite `tests/m3_commission/test_m3_live_bindings.py` aligned, 15/15 live.
DIGICOW custody grant needs an HTTPS-origin ruling (or delivery by mount); `CustodyBinding` is single-tenant
(RMS origin). Quality matrix threshold pending the first human-verified sample. DigiCow authorities unseated
(stand-in cited on every approval). No commissioning UI yet. M2 Watch inventory must be rerun for the new
`dap.commission` / `dap.delivery` gates.

**NEXT:** P1 wire DAP Request / My Work UI to `/api/portal/commission/*` (drafts, feasibility, freeze,
advance, run view, deliveries) with prototype fidelity; rerun M2 inventory; then M4 grounded answers on the
verified DIGICOW units.

## SUPERSEDED — 2026-09-29 (evening) M2 Grey Mirror / Watch CLOSED — G2 PASS on the admitted inventory · M3 OPEN

Owner directive: "Did you follow the three steps … readiness review, implementation, testing with
the same rigour as M1? If so finish M2 cleanly in one autonomous run. Use the same depth of front
end as you did in registry." English only. E1 stays a control plane.

**Readiness:** Canon 8 read in full; every `services/watch` + `services/cif` module, contracts,
drills and the Nexus `mirror`/`watch` fragments read before code. Crosswalk + limits:
`assessment_workspace/notes/m2_execution/M2_WATCH_READINESS_AND_CLOSURE_20260929.md` (public copy
`frontend/public/briefs/Akki_Watch_Readiness_M2.md`; both roadmap copies link it under Gate G2).

**Implemented (reuse-first, no new engine/grammar):**
- `commission_gate.py`: mark/sever state evaluated FIRST on every pass at the 3 protected
  boundaries (403 hold, effect receipt); tripwire hook; expired containments reconciled on every
  READ (not only the subject's next crossing) with a release row + notice; witness digest
  attestation at every mint; verdicts name `requirements=vN` or `thresholds=DEFAULT_PENDING_OWNER_RULING`;
  contain-release-contain anomaly flag; console reads receipted.
- NEW `tripwire.py`: operator plants a decoy one-way (hash only) after a MEASURED isolation check of
  the mirage store against 7 production stores; touching it at a gate → `mirage_incrimination`
  signal (closed registry) → `structural_certainty` verdict → `sever` (holds) → `MarkV0` (6
  dimensions: principal, session_ref, device_ref one-way, behavioural digest, content hashes) →
  witness → detection/effect rows → pre-opened Decisions item → notice.
- NEW `decisions.py`: reserved human set; approve needs TWO DISTINCT operator/master_admin
  principals (same approver twice → 409, empty note → 409); acknowledge changes nothing; decline
  keeps protection; execution = `release_sever` (real restoration, gate admits again) or
  `learning_loop.ratify`.
- NEW `notices.py` (notify posture, owner default), `learning_loop.py` (finding → `services.cif`
  detection→acceptance point→L-4 routing → `research_queue` → grounding by citation resolution →
  Decisions → `watch_requirements/v{n}.json`; detectors read the ratified version, history keeps
  its label), `witness_binding.py` (`wi_gate_record_witness`, digest attestations, standing
  break-in via production writer — must refuse), `console_projection.py` (tiles, charts, patterns,
  mirage, marked, decisions panel, walks, budgets).
- Routes (tenant-bound): GET `/api/portal/watch/state` (+legacy aliases, same envelope), GET
  `/api/portal/watch/notices` (own), POST `/api/portal/watch/decisions/{id}`, `/requests/demark`,
  `/requests/redeclaration`, `/learning/propose`, `/mirage/plant`, `/witness/break-in`. Legacy
  `/api/watch/*` mutations stay 401/409.
- Frontend (prototype DOM/CSS unchanged; bindings + testids only): State tiles/G2/G3/chart/budget
  gauges/ledger walks; Record lanes + "The notice we sent →" + six-step evidence walk ("Walk
  incomplete" when a step is missing); Under watch curves (inline SVG), Watch closer, re-declaration
  notice, mirage findings, real Marked lines (L7300 sample text replaced), de-mark request →
  Decisions; Decisions Review/Approve(n of 2)/Decline/Acknowledge with side-by-side records; bell
  merges Watch notices. `OwnerMarkup` exact-binding interpolation now trims whitespace.

**Drill pack (live, deployed backend; nothing dispatched to any worker):** T1 (iter 62 + sever
`ma_gate_505031dd5f5e`), T2 (benign zero verdicts; 8 refusals → contain never sever; dual-control
release `wd_1be2814bcdf4` → DPO's next crossing reached the handler), T3 (decoy
`mr_gate_ce1aa789274a`, touch `mt_gate_505031dd5f5e`, mark `mark_gate_505031dd5f5e` checked at all
3 gates, reads unaffected, no dimension leaks), T4 (503 fail-closed offline; break-in `passed` live;
drift → tamper alarm offline; acknowledge leaves protection), T5 (`cif_watch_71a04299eb53` →
`wd_6ac4580d762a` → `watch_requirements/v1.json`; new verdicts cite v1, old keep DEFAULT).
Tests: offline 14 (`test_watch_commission_gate.py`, `test_watch_m2_full_loop.py`), live drill 8/8
(`test_watch_m2_live_drill.py`), iteration 63: 29/29 live backend + all four panels desktop/mobile,
zero overflow; frontend unit 31/31. Drill subject: demo.dpo (severed then released).

**Standing limits (recorded in the closure note, not hidden):** inventory = 3 commission gates +
console (auth/invocation/egress mark checks not yet in inventory); independent watchdog not placed
(record witness runs in-pod); learned detectors/behavioural signature not built; mirage entry
above containment not autonomous (owner ruling pending — highest bar holds); jittered bands not
implemented; budget gauges measure drill traffic (friction gauge will show the analyst's drill
effects as friction once released clean — a standing §19 finding on drill traffic). Each
`learning/propose` call while an identical finding is open returns the open item (no duplicate
proposal). Testing agent left ONE open `requirement_ratification` (`wd_9f099816b25f`, v2 candidate)
and one extra live decoy (`mr_gate_8d182331a121`, TTL 600 s).

**NEXT: M3.1** — intent → saved draft → feasibility → review → commission made durable on the
existing DAP/Northena path; M3-T1 first bounded extraction scope to confirm with owner (RMS MySQL is
the fully-censused candidate). Rerun the M2 inventory as M3 adds gates (G2 says later milestones
extend and rerun it).

## SUPERSEDED — 2026-09-29 (late) M2 language cognition TRAINED on akki-vm-ii (measured, not final)

Owner directive: "Akki trains language cognition model on akki-vm ii … Run M2
autonomously. Maintain same rigour." Owner inputs this increment: 2 h+ budget;
train on the extracted `google-transcripts/datasets` clean-cut labelled audio; other
material tests model success; audio is a database (AIP §1.1); use the repo's
biometric (speaker) layer. Owner said "Proceed without check in 1-5". English only.

**Done this increment (all phases ran as daemonised jobs on akki-vm-ii through
`services/audio_plane_v1/language_cognition_dispatch.py`; E1 never a data path):**
- Worker fixed/hardened (`language_cognition_worker.py`): `win` NameError; real
  layout `datasets/<code>/<session>/{audio,transcript,metadata}`; files are MP3 in
  `.wav` containers → ffprobe facts (duration/codec/sample rate); prefix-marker
  objects skipped; 262 archive-only sessions unpacked + per-session origin index;
  corpus read as a database (`corpus_db/files.jsonl` 3,958 rows, `segments.jsonl`
  351,021 rows). NEW phase `speaker_linkage` (ECAPA speaker embeddings → presenters;
  embeddings destroyed after clustering, AIP §6.2.4). `train_baseline` now splits by
  PRESENTER (MUST-DO §3), keeps archive-only sessions as a second test set, reports
  per-language + per-condition (sample-rate) accuracy with abstention, runs the
  no-speaker-ID linear probe (MUST-DO §4), checkpoints, banks manifest hash.
- Control plane: `_bank_run_certificate` (AIP §11.6) checks receipts against SEALED
  defaults (`WINDOW_AND_SPAN_RULE_DEFAULT`, `SPEAKER_DISJOINT_SPLIT_CONTRACT_DEFAULT`,
  `LANGUAGE_COGNITION_MOAC_CONTRACT_DEFAULT`) — no silent re-thresholding.
- Receipts (digest-verified, Northena admit/gate/converge + Track-4 rows):
  corpus_census `lcj-1851c62aee3b` — 15,899 objects/54.1 GB; 529.5 h audio, 828.6 h
  segment time, 8 languages with audio (guz/kam/kik/kln/luo/lwg/swa/bxk), English +
  Sheng absent, no per-span labels. speaker_linkage `lcj-e16f26a43d22` — e.g. kik
  1,372 session-local ids → 203 presenters; all 7 transcribed languages meet N≥20.
  gate_eval `lcj-4e9283997834` — pre-trained Whisper-LID/VoxLingua107 label every
  Kenyan language `sw` (agreement 1.00 swa, 0.00 elsewhere): the overlay cannot
  deliver the census distribution. train_baseline smoke `lcj-229ca62fe5cb` proved the
  pipeline. FULL RUN `lcj-f96c86a16312` (05:22–07:07 UTC, 14,511 steps/8 epochs/6,405 s
  on one H200, 124,273 train windows): held-out PRESENTERS 32,781 windows → overall
  accuracy on judged **0.940**, abstention 1.9 %; kik 0.976 · kln 0.957 · kam 0.951 ·
  guz 0.944 · swa 0.939 · luo 0.925 (all ≥ 0.90 default) · **lwg 0.592 (fails; 43 train
  presenters)**; archive-only sessions 0.954; per-condition reported (22/48 kHz weakest).
  **No-speaker-ID probe MEASURED FAIL** (encoder rep. 0.77–0.84 presenter-ID; output
  logits above chance in kam/kik/kln) → `no_speaker_id_probe_passed: False`. Verdict NOT
  ADMISSIBLE (MUST-NOT §1 + MUST-DO §4); artefact `d2cd0497…` on host, not admitted;
  certificate `run_certificate_lcj-f96c86a16312.json` banked against sealed defaults.
- Tests: offline worker (10) + dispatch (8) pass; live API suite iteration 61 9/9
  (`tests/census_operational/test_language_cognition_api.py`). Operator tool:
  `assessment_workspace/tools/m2_language_cognition_run.py`. Evidence:
  `assessment_workspace/notes/m2_execution/LANGUAGE_COGNITION_RUN_20260929.md`.

**Standing facts / not done:** artefact is `final_model: False` (MUST-NOT §1 — no
labelled code-switched spans; English/Sheng absent; DP-SGD not applied, DQ-24
recorded). No UI surface exists for LC jobs (AIP §13: milestones surface; none
invented). Roadmap M2 (Grey Mirror/Watch) and M9 (final LC qualification) remain as
sequenced. Never POST a valid phase from tests — it spawns real GPU jobs.

## SUPERSEDED — 2026-09-29 (pm) M1 P0 pull-seam census now consumes fully

Owner P0/P1: "holistic Census on akki-vm (entire deep census as designed) consume
fully; train language cognition on akki-vm-ii." E1 stays control plane; akki-vm is
worker of record and hops to the jump host via the pull seam (NAS/MySQL reachable
only there). No estate bytes on E1 or the GPU host.

**M1 P0 FIXED and PROVEN LIVE (this increment):**
- Root causes: (1) CIFS directory listing on the jump is RTT-bound (57 ms) and does
  NOT scale with threads on one session (~95 files/s ceiling, 1 vCPU) — a multi-TB
  share cannot be walked in one bounded pass; (2) MySQL receipt truncated at 3×64 KiB
  because paramiko `exit_status_ready()` fired before stdout drained → `JSONDecodeError`.
- `deep_files.py` rewritten to **resumable** enumeration: durable frontier
  (NAS directory paths; OBS continuation tokens + 16-byte ETag+size fingerprints)
  checkpointed on the worker every 30 s; shared work queue commits a dir only when
  fully scanned; per-pass cumulative totals + `directories_pending`/`progress_this_run`
  + `epoch`; flock refuses concurrent same-scope runs; completing a share opens a
  fresh re-census epoch. `CENSUS_REMOTE_STATE_DIR` added to backend/.env.
- `deep_dispatch.py` + `deep_pull.py`: drain to channel EOF (`eof_received`) not just
  exit-status (fixes MySQL truncation); SSH `set_keepalive(30)` for hour-long jobs.
- `operational_runner.continue_if_resumable()`: progressive-consumption cadence now
  supervised by the DESIGNED Supervision Plane engine `services/work_supervisor/
  runtime_supervisor.py` (reuse, not proliferation): each finished pass records a
  `ProgressSignal` (cumulative files+objects, volume bytes) into a progress ring and
  the canon `output_verification_watchdog` decides continue-vs-halt. A scope keeps
  scooping while coverage grows; a flatlined scope HALTS + banks `scope_halt`
  (STANDING ORDER §3.2 "NO RUN WITHOUT A PROGRESS SIGNAL / alive ≠ done") instead of
  looping. Unit-tested: grows→continue, flatline→halt+escalate.
- Read word-for-word the designed engines that own progressive consumption:
  Targeta (deterministic eligibility+ranking → reproducible MiningPlan of ordered
  target regions; yield layer gated admitted=False), Northena (admit crossing +
  execution coordinator), CIF (Doc-9 Conditioned Ideation Faculty: detection.author_
  proposal → acceptance_point.is_accepted single-experiment gate → output_routing to
  L-4/L-5; proposes-never-ratifies), Solva (reasoning/critic seam), and the harvest
  roadmap recursion principle (archive=programme=file are all estates; census applies
  at every scale = the shovel). NEXT: originate the census scoop ORDER through Targeta
  and coordinate through Northena rather than the bespoke census_scoop_planner
  (anti-proliferation §1.2) — scope to confirm with owner (touches census↔Northena).
- Bespoke `census_scoop_planner.py` + `POST /api/portal/census/plan` exist and work
  (1 TB bin-packed ordered scoops + cadence estimate) but OVERLAP Targeta's MiningPlan;
  slated to collapse into Targeta origination per the owner's engine directive.
- LIVE: MySQL `cr-3b6b013458de` 6/7 scopes COMPLETE — **20 db, 1013 tables, ~239.6M
  rows** (was 1/7); only `artists_app` blocked (needs MySQL GRANT — owner dep, banked).
  NAS consuming via scheduler: epoch 1, 84,616 files/16 channels, 4,844 dirs pending,
  checkpoint advancing; probes showed cumulative growth 4,388→13,794 files. OBS
  resumable by continuation token (99+ buckets). Evidence:
  `assessment_workspace/notes/m1_execution/PULL_SEAM_CONSUME_FULLY_20260929.md`.
- Tests: pull-seam-hop, deep-dispatch-transport, Watch-M2 mocked suites pass; 116
  census_operational pass. Pre-existing `test_execution.py` t08/t09 fail identically
  at git HEAD (legacy aggregate protocol) — not introduced here.

**M1 remaining (not a mock): NAS/OBS "fully" is many autonomous bounded passes**
(now lossless via worker checkpoint); artists_app GRANT; full designed producers
beyond metadata+sampled-media; D6 duplicate-label identity reconciliation; M1-T1–T5.

**M2 language-cognition training on akki-vm-ii — HONEST WALL (real SSH telemetry):**
2× H200 143 GB idle, no GPU procs, `nvcc` off PATH; torch/torchaudio/transformers/
peft/speechbrain/datasets/accelerate ALL MISSING (system + census venv); 5.9 TB
volume empty; no base weights / no labelled corpus / no split on disk. The
`commission_language_cognition_training_run` callable returns a handle, not job
pickup. A REAL run cannot launch until framework is provisioned, a base model
(Whisper/VoxLingua107) is registered, and a labelled code-switched speaker-disjoint
corpus is assembled — none may be mocked (MUST-NOT §9). Owner direction requested
before provisioning (cost/data/base-model choice). Final training acceptance is M9.

## SUPERSEDED — 2026-09-29 M1 repairs / independent M2 preparation

Latest owner directive: “Akki trains language cognition model on akki-vm ii,
holistc Census on akii-vm (entire deep census as initially designed) consume fully.
Fix P1 +P0. Close this and commence M2. Run M2 autonomously. Maintain same rigour
in the structure shaped in M1”. Owner confirmed “Proceed”. Do not repeat a
blanket planning/approval loop; preserve the existing10-milestone roadmap.

**M1 NOT CLOSED; G1 NOT PASSED. M2 preparation/scoped reader started; G2 NOT RUN.**
No full-census/training/enforcement completion claim is supported by this repair.
English only. E1 remains the control plane, not a source/corpus/weights data path.

Verified this increment:
- SSH worker completion recognizes exit-status after draining both streams,
  recalculates remaining budget after connection, preserves transport diagnostics.
  Original failed runs retained. Five MOCKED transport tests are not live gate proof.
- Source category/legend/row/child CTA/profile bindings and async-close race repaired;
  original Nexus source catalogue made responsive and populated from retained data
  instead of hardcoded prototype totals. Single child click sends one source read.
- Credentialed CORS now uses explicit configured frontend + observed proxy alias,
  not wildcard; unrelated origins denied. Auth/accounts/credentials unchanged.
- New implicit census jobs select env `CENSUS_PRIMARY_WORKER=akki-vm`. Verified
  idempotent replay returns original SQL successor with no extra dispatch.
- M2 original Grey Mirror/Watch reads tenant-bound retained observations/records;
  old unadmitted Watch HTTP mutation paths are authenticated409, not authority
  minting. No detector/physical effect/witness qualification inferred from records.
  Overview ledger/filters, refresh and evidence→selected census work. Duplicate
  outer OS drawer obstruction and mobile Watch/overview layout repaired.
- Final targeted backend28 pass; existing frontend9 pass; real UI source/profile,
  Watch record/drawer/overview verified at1920×800 and390×844, overflow[].

Actual successor census placement/status:
- `cr-d5d34eb632a9`, akki-vm, PARTIAL: external43.385s,1/7 scopes complete;
  five MySQL scopes unreachable, artists_app authentication failure.
- `cr-b13eaacdc4bb`, akki-vm, REFUSED: external0.05s, NAS root absent/not mounted.
- `cr-b47b981d2035`, akki-vm, PENDING/executing at final read; OBS not yet verified.
  Existing supervised dispatcher continues it; do not submit a duplicate blindly.

Training target is **akki-vm-ii**; **NOT LAUNCHED**. Remote readiness observed expected
hostnames, no GPU processes at that instant and no torch/transformers/peft in system
Python (not proof about other environments). The fully read language-cognition
commission function returns a handle, not job-pickup evidence. Recover/qualify
existing base/corpus/speaker-disjoint split/frozen MOAC references and wire actual
Akki-native language training; do not use text LoRA or legacy MOCKED training as
a substitute. Preserve original biometric/DP/abstention/custody rules and M9's
independent acceptance; pending owner defaults are not measured passes.

P0/P1 next: restore akki-vm NAS/MySQL access; inspect OBS terminal receipt; complete
all40source clauses/deep producer integration and M1-T1–T5. D6 duplicate-label SQL
source identity still needs descriptor-safe historical reconciliation. Current
metadata/64-row samples/object lists/media probes are not the full designed census.
M2 next: finish full reuse/callsite/readiness crosswalk, bind real detection→bounded
physical effect→record→independent witness→notice→legitimate restoration; then T1–T5.
P2: M3–M10 unchanged, with M9 final language-cognition qualification.

Evidence:
- `assessment_workspace/notes/m1_execution/REPAIR_AND_SUCCESSOR_STATUS_20260929.md`
- `assessment_workspace/notes/m2_readiness_20260929/READINESS_AND_PROGRESS.md`
- `test_reports/iteration_59_resolution.md` and passing pytest XML; original
  iteration58/59 reports preserved. No five-attempt lockout policy invented.

## Original problem statement

Deeply understand, assess and operate Akki Extraction under strict architectural
and governance rules. Wire DAP requests, work history and entitlement lifecycles
to actual engines; reconcile the 648-row requirements assessment against genuine
closure evidence rather than fixtures or claims. Preserve frozen Canon contracts,
one authoritative append-only ledger, and 100% fidelity to owner HTML prototypes.

## Users and boundaries

- Estate owners/tenant approving authorities commission governed read-only census
  and separately scoped extraction, answers, evaluation and delivery.
- Work users consume scoped results/history; operators administer controls and
  independent inspectors establish evidence without inheriting worker authority.
- **E1 is NEVER the estate-data execution path.** E1 wires admitted descriptors;
  a local subprocess or HTTPS source SDK does not itself establish an external
  admitted runtime. Do not manufacture admissions, signatures or trust roots.
- Owner authorises independent non-GPU work; no fresh blanket approval is needed.
  GPU/SSH CONNECTED 2026-09-28 17:15 UTC via GPU CRED 3 workbook (password auth).
- English only. Keep source credentials in ignored custody, not chat/reports/UI.
- Source requirement text is immutable; hardening is a versioned derivative.
- A schema, chat ruling, ordinary login or historical fixture is not a live
  signed approval. Use existing rulings/defaults before requesting owner decisions.

## Architecture

- React frontend, FastAPI, MongoDB. URLs/credentials/database configuration use
  existing environment variables. API routes use `/api`.
- Bootstrap: `/app/backend/server.py`; runtime:
  `/app/backend/vendored/extraction_akki/backend/`.
- Canonical ledger: `services/ledger_writer/{principal_control,mongo_control}.py`.
- Coordination: `services/northena/execution_*.py`; Mkondo native handoffs;
  Mtafiti registry; `services/activation/`; `services/non_gpu_governance/`.
- DAP: `routers/portal_requests.py`, `services/portal_operational/`.
- Census: `services/census_autonomy/` including `census_router.py`,
  `jump_dispatch.py`, `rds_data_dispatch.py`, `obs_dispatch.py`,
  `non_gpu_census_worker.py`, `census_dq_producer.py`.
- UI: owner prototype/OwnerMarkup composition. Do not redesign CSS/layout/DOM.
- Credentials unchanged: `/app/memory/test_credentials.md`; estate access is
  held in ignored `/app/backend/estate_keys/owner_20260928/`.

## Current checkpoint — 2026-09-28, M1 Registry readiness revision 2

Owner accepts roadmap but rejects flattened Registry report. Three new screenshots
show selected Census4, successive scroll: exact Discovery Summary/GPU Spend/
Conversation with Agent/Discovery Details; five-category condition bar; Coverage,
Condition, Readiness with13 annotated value/delta rows. Source is latest Nexus
HTML0330a171… (not sample values as runtime data). Original design must remain full.
Every milestone readiness now explicitly includes FRONTEND source/UI/UX capture,
backend integration mapping and prior-gap closure reconciliation. Once a scoped
correction is verified, keep it closed unless specific regression/evidence change/
new requirement justifies reopening. No arbitrary recurring re-audit/new gates.

Current readiness report: `notes/registry_readiness_ui_20260928/REGISTRY_READINESS.md`;
companion `CLAUSE_MAP.md` maps all22Doc9/10+15DQ+3trust-domain rows (coverage, not
closure). Full Doc9/10 source texts recovered26Sep and read; never ask again based
on15Sep missing-document note. Historical audit D1–D11 and original11field gaps
reconciled without overwriting original evidence. Ready-to-implement delta includes
complete UI/interaction AND backend functions; no cosmetic-only fix accepted.

Concrete mismatch: OwnerOSPage still uses generated/os.json, source a0a6df580…;
Nexus fragment generator excludes Registry. historyModel explicitly renames tabs,
replaces3groups with Inventory/Execution outcome, omits actor/coverage, changes
pagination to8 and GPU rows, forces no conversation; Census #undefined persists.
Full original Registry/source/report/compute/model/Connect markup and report/
Connect model transitions reviewed. Preserve source styles, responsive adaptation,
all fields/controls and non-fabricated states; use existing renderer.

Verified narrow closures: D3 fictional DAP pages no longer mounted; D10 facts is
authenticated scoped200 (NOT blanket409); census4 read/date visibility retained.
D1/D2/D7/D8 unsafe legacy exposure quarantined—not corresponding capabilities
complete. D6 conflicting asset overwrite still open; D11 actual sensitivity,
RDS/OBS off-E1, deeper profiles/coverage, durable source Registry, NAS/worker and
full UI/compute/response integration remain open. Existing Canon source writer,
Measurement/Unmeasured, stratum, activation, classifier, enumerator, NAS inventory,
two-layer composition, quality bitmap consumer and brief generator MUST be reused.
Quality consumer is not profiler; name-FK scaffold not all4ruled linkage types.

Evidence iteration55:16scoped API tests PASS,24offline tests PASS (SYNTHETIC/MOCKED),
actual census4 desktop1920x800/mobile390x844 comparison: fidelity FAIL, no overflow.
Ignore arbitrary tester percent scores/global backend-healthy statement beyond
its read-path tests. Known defects deliberately not fixed in this readiness-only
request. No app/UI/auth/credential/config edits, no source/GPU calls or new census.
Published readiness report, clause map and revised roadmap verified exact against
canonical HTTP downloads. VALIDATION.json banks source/screenshot links, hashes,
all13rows, originalD1–D11, all40exactclauseIDs and unchanged runtime/source checks.
Ten milestones/51packs preserved; M1 acceptance NOT RUN. Remaining full dependency
reads explicitly listed; no exhaustive repository-read claim. Next work when
implementation begins: M1.2 external effects and M1.3 whole designed Registry
integration together, then M1.4 all5acceptance packs and closure. No new questionnaire.

## Previous checkpoint — 2026-09-28, M1.1 second verification / readiness revision 1

Owner clarifies “2nd review” means the proposed verification, then rollout within
the governing milestone framework. Explicitly requires a full relevant-repository
reuse review in EVERY milestone's readiness phase: read built implementations,
alternatives, dependencies, tests and actual callers before proposing new code.
Keep all communications/questions/refusals/recommendations tied to that outcome;
no detached P0/P1/P2 approval questionnaire and no repeated blanket consent ask.

Updated canonical `notes/goal_delivery_20260928/AKKI_GOAL_ROADMAP_v1.md` and matching
public brief: readiness revision 1, ten milestones / 51 packs preserved. Added
readiness homes M1.1–M10.1, explicit full-read/reuse/change justification, and both
non-GPU and GPU-hosted worker verification within M1-T1–T5. GPU host access is not
GPU acceleration proof. Use already-qualified GPU census functions where applicable;
new model/perception/training qualification remains M9. Do not defer M1 adapter gaps
to M9. No claim that all repo files or even all relevant M1 candidates are now read.

Report: `notes/m1_second_verification/READINESS_REVIEW.md`.
Current baseline: RMS overview seven retained records, zero PENDING; latest
`cr-dd05196d837f`; historical blocked `cr-809561ad5643` and `cr-a29e3b7b16ae` remain.
Owner's precise intended pending card is not conclusively identified. Reconcile
the existing history; never invent a pending job or rewrite old refusals.

Confirmed M1 work: RDS/OBS SDKs still execute in E1 with incorrect akki_host claim;
local subprocess fallback is not off-E1 either. GPU remote worker is mysql_metadata
only, NAS falls to it. Deeper Mtafiti composition/quality/sampling code exists and
must be reused after dependency review. Current compute tab/GPU spend are not wired;
public gpu-spend and response-required routes return intentional 409 quarantine.
Do not unquarantine unsafe/stub producers. Existing receipt hydration must be
qualified on durable custody/all consumers, not replaced with another Registry.
Current owner history has an observed `Census #undefined` result-ID mapping defect
for records without census_number; M1.3 repair remains open.

Verification: source review + external-preview owner history at 1920x800/390x844,
no horizontal overflow; 24 isolated offline contract tests pass (SYNTHETIC/MOCKED);
12 read-only live API tests pass after correcting a stale historical-count test.
Preserved owner census4 expected values on record4; latest checks its own detail.
Reports `iteration_54.json` and `iteration_54_resolution.json`. Published readiness
revision verified accessible; canonical/public copies match and still contain
ten milestones, 51 unique packs and all ten explicit readiness review homes.
No runtime/auth/
credential/config/UI changes, no new source/GPU calls, no census commission or
service restart. All M1–M10 live gates remain NOT RUN. Next: M1.1 full review/card/
descriptor reconciliation → M1.2 external workers → M1.3 deep Registry/compute
bindings → M1.4 acceptance/repair. M2–M10 follow the same readiness discipline.

## Previous checkpoint — 2026-09-28 17:15 UTC, GPU hosts CONNECTED

Owner supplied `GPU CRED 3.xlsx` and said: "Connect GPUs first then we activate the
2nd review, then roll out." Both GPU VMs now authenticate through Akki's existing
governed seam (`services/gpu_direct` workbook → pinned server key → password →
`training_runner.ssh_seam.execute_remote_command` with redacted receipts).
`capture_gpu_spend()` returns CAPTURED for akki-vm and akki-vm-ii. Provider had
re-assigned public IPs (akki-vm .230, akki-vm-ii .244); env + known_hosts updated.
Hardware per host: 2× H200, 36 vCPU, 460 GB RAM, 5.9 TB data volume. Prior notes
report CUDA 12.8 and no docker/pip/torch; the inspected connection receipts show
`nvcc: command not found`, so compiler-on-PATH/runtime readiness is not established.
GPU/SSH is NO LONGER PARKED. Details and
custody path in `test_credentials.md`. `/api/portal/census/gpu-spend` remains an
intentionally 409-quarantined legacy unscoped route; the seam proof ran in-process.

## Previous checkpoint — 2026-09-28, governing goal-based delivery roadmap

Owner requests goal-based milestones with outcome/performance test runs opening
the next milestone; readiness gaps must become tasks within that milestone. Start
with Registry/deep non-GPU census commissioned through Akki by the agent acting
as objective-shaping wizard; Grey Mirror and all core functions follow. Exact
direction: "The plan you will develope is canon going forward." Function and
integrity serve the promise; eliminate unanchored invented restrictions/timers,
not ratified safeguards. GPU credentials/additional datasets stay with owner.
Planning only: do not begin source runs or implementation during this turn.

**Governing execution document:**
`assessment_workspace/notes/goal_delivery_20260928/AKKI_GOAL_ROADMAP_v1.md`.
Companion `FAMILY_OWNERSHIP.json` routes all historical 56 families / 648 rows,
and E01–E14 experiences. Routing is not clause-level adjudication or closure.
Ten milestones / 51 acceptance packs, all NOT RUN:
M1 Registry + deep census → M2 Grey Mirror/Watch → M3 request-to-delivery →
M4 useful grounded answers/context → M5 memory/collaborative work/goals/board →
M6 artifacts/decks/callable skills → M7 tenant/rules/commercial operation →
M8 resilience/withdrawal/recovery → M9 activated media/model/training capability →
M10 integrated independent acceptance. Independent preparations can overlap;
mandatory FAIL/BLOCKED runs never count as PASS. GPU preparation runs in parallel.
No new percentage, arbitrary milestone duration or test threshold. Source-default
metrics require prior-ruling reconciliation; informational findings are not
silently made into blocking gates. Existing UI fidelity and E1 isolation stand.

Owner added explicit deep reuse review of https://github.com/bramuel-syni/Akki-OS-Root.
Pinned main `c481c1d65eb6ddd2c6630d31a736d11e46e1641a`. Root recursive API listing
was truncated; complete backend/frontend/memory subtrees fetched separately.
Backend + frontend/src comparison: 1,215 donor paths, 1,200 identical current
blobs, 15 different, zero donor-only. 1,204 selected source/docs materialised;
1,005 Python files statically indexed without execution. Root links Core/OS/
Extraction/RMS-IQ as gitlinks. No claim that all archive/submodule code was read.

**Reuse review:** `notes/goal_delivery_20260928/ROOT_REUSE_REVIEW.md`.
Current workspace is ahead of Root in operational census, execution/activation,
custody/native skill queries, billing joins and UI. Do NOT overwrite with Root.
Existing memory, Watch action/mirage/witness, registry, skill provisioning,
training/WPW and single-effect mechanisms must be reused. Old async dispatcher's
NotImplemented branch is not proof that current native skill queries are absent.

Concrete milestone tasks from read-only review: deepen census; qualify external
worker/provider placement; retain tenant-bound `/api/portal/census/run`; old
unscoped routes are intentionally 409-quarantined and shape-only COMPLETE is not
success. Verify durable receipt custody and RAM registry hydration/all consumers;
workspace-based state needs persistent-runtime qualification. Watch has mutation
mechanisms but recorded actions do not prove effects. Solva equal-weight scaffold
and synthetic quality/memory tests do not establish useful live answers. Team/
goal feeds have explicit empty placeholders. Repair these within owning milestones.

Verification: documentary/source/identity coverage and static review only; no
application tests, estate/GPU/model calls, state/config/auth/UI modification or
live milestone pass. Broader positives remain SYNTHETIC/MOCKED where unproved.
Next execution is M1.1 readiness and objective shaping, then commissioning the
deep non-GPU census through Akki—not direct source execution from E1.

## Previous checkpoint — 2026-09-28, reuse-first closure plan

Owner works on GPUs; asks to plan closure of the previously estimated 65% gap.
Supplied Supplement 2 ZIP, Streaming Voice Training Capacity DOCX and Deck Engine
v1 DOCX; points to Akki-Executive-Core and Akki-OS-V1 for reuse. Says "skip" for
tenant authority submissions and artists_app permission: park, do not waive gates.

Current report: `notes/owner_closure_plan_20260928/PLAN.md`. Originals and pinned
repository snapshots: `assessment_workspace/incoming/owner_closure_plan/`.
All 24 historical source-unresolved clause bodies recovered (11 SV, 11 ROC, two
deck). This closes source recovery only, not implementation or live acceptance.
Voice remains PROPOSED/NOT YET MERGED in source; LT-2/3 OPEN there. ROC source draft
must reconcile existing 2026-09-09 BANKED-DERIVED approved working default.

Important recovered prior rulings in `STATE/DECISIONS.md`:
- A18.6 already ADOPTED on 2026-08-27; current runtime adoption record exists.
- EP-4 mandatory dual-judge/register precondition already directed; guard exists.
- BC-3/4 on 2026-09-15 explicitly reject a blanket static recovery number and
  direct a tiered dynamic-recovery packet. Full packet ratification not established.
  New 24h estate / near-zero Ledger / 72h-after-unit-arrival defaults were offered
  ONLY absent a prior ruling, so do not silently bind them over this direction.
- Older QA workbook has a 2026-09-20 V1–V7 ruling; owner now references Audit
  Standards v2 V1–V8. Pin/version/crosswalk actual definitions, never invent V8 or
  overwrite auditor verdicts. EP-1–3 adoption/mapping needs precise reconciliation.

Both public main trees fetched without truncation: Core `5844eee95d5faffea0dcab98bd4fe5e8d1419f32`,
OS `8c361903cdd319bfdc0709de3f4392f5bfa3956b`. Targeted inspection found existing
deck async jobs, async accepted/estimate/state/refusal, current rules register and
EP guard. Donor OS async dispatch explicitly lacks callable-skill support there;
current DeckSpec is only a frozen two-field shell. Reuse candidates are not proof
of active current full-spec conformity; trace ownership and extend, do not duplicate.

Next: evidence-linked reuse/call-path crosswalk; six-schema descriptor/admission
integration; NAS verification on an admitted EXTERNAL worker; genuine governed
non-GPU path; parallel rules/deck/async deltas; remaining product/live proofs.
GPU/SSH stays with owner; no retries. Never scan NAS/source data from E1.

Verification: all three originals hashed/read; direct OOXML extraction confirms
24 expected clause IDs; historical baseline confirmed 648 rows; targeted code and
prior-ruling reads. Planning/docs only: no app, auth, config, credential, UI or
estate changes; no new tests/live certification. Broader positives remain
SYNTHETIC/MOCKED without live evidence. No completion percentage recomputed.

## Previous checkpoint — 2026-09-28, descriptor requirements review

Owner: “Attached are some of the requirements. NAS - mounted on: /mnt/nfs-share.
You now have data to close alot of the gaps. What is pending from me?”
Then quoted the previous “everything verified”, ~35% and live census report.

Reviewed files (20).zip: six JSON schemas (source/query/worker/inspection/custody
descriptors and admission record) plus an 18-entry inventory. All six schemas
pass Draft 2020-12 meta-validation. Direct workbook inspection: all 18 location
cells and all 18 status cells blank. These are contracts/inventory, not populated
verified descriptors or signed admissions. Originals retained unchanged at
`assessment_workspace/incoming/requirements_files20/`, hashes in report below.

Historical owner-action reconciliation (superseded above where changed):
`assessment_workspace/notes/descriptor_requirements_20260928/OWNER_PENDING.md`.

### Owner dependencies, limited to affected work
- Workbook explicitly lacks identity drops for RMS Fred Afune / Muthoni Kiarie /
  Samuel Kibacia and DigiCow Vincent Kimani / Peninah Wanja. Recover custody refs
  first; missing identity/mandate evidence goes through existing tenant custody.
- artists_app previously denied; owner earlier said “ok”. Do not assert GRANT was
  applied. Only continuing denial after confirmed update needs narrow admin access.
- Historical missing-source clauses: SV extension 11, ROC 11, deck DR-R10/R13 two.
  New archive contains none. Recovery is E1's first task, then precise owner sources.
- Seven historical decision rows are EP-1–4 adoption, A18.6 async delivery, BC-3/4
  continuity policy — NOT seven numeric thresholds. Reconcile existing rulings;
  only genuinely missing policy decisions return to owner at their affected gate.
- AISCA/GPU administrator dependency stays parked, not a non-GPU blanket blocker.

### Engineering work, not more owner inputs
- Verify NAS mount host/admitted-worker/read-only scope; mount path alone proves
  neither NFS/CIFS nor successful census. Do not request SMB password by default.
- Populate descriptor inventory and pin recovered actual worker/inspection/custody
  evidence; recover D-18 pilot and AKKI-TEST records, not replace existing authority.
- Platform-principal MT-13 workflow and explicitly SYNTHETIC test estates are E1
  build tasks; DigiCow tenant web access is engineering/admission wiring.
- Qualify worker separation/admissions, real DQ/extraction/answers/metering/delivery.

### Evidence corrections
- Prior report records real aggregate reads: RMS 20 databases/1,015 tables/~257M
  estimated rows on six hosts; DigiCow 239 tables/~5.9M estimated rows; OBS 106
  bucket listing. These are HISTORICAL, not rerun in this review, not full content
  census or full product/security/admitted-runtime certification.
- Current RDS/OBS dispatchers call SDKs directly; hash-derived worker receipt IDs
  and execution_location strings are not signed runtime admission/independence.
  These findings are engineering follow-up, not credential requests or live fixes.
- ~35% is an unreconciled estimate; old remaining shares total 93%. Do not assert
  built-and-proven programme percentage until row-level reconciliation. No new %.
- Broader positive answer/model/custody/governance fixtures remain
  **SYNTHETIC/MOCKED**; live end-to-end acceptance is not established.
- This turn changed assessment/continuity documentation only. No app/config/auth/
  credentials/UI changed, no source/GPU reads, no new admission or certificate.
  Prior 733-test result is historical, not a new regression run.

## Continuity and priorities

- `ROADMAP.md`: latest P0/P1/P2 ownership and historical roadmap.
- `CHANGELOG.md`: implementation/review history and verification.
- `ARCHIVE_PRD_BEFORE_DESCRIPTOR_REVIEW.md`: exact prior 761-line PRD preserved;
  includes detailed 2026-09-27/28 controls/UI/non-GPU implementation checkpoints.
- `ARCHIVE_PRD_BEFORE_ACTIVATION_CONTROLS.md`: earlier history.
- Original audit: `notes/full_requirements_gap_20260926/REQUIREMENT_GAPS_648.csv`.
- Decision ownership: `notes/consolidated_fix_plan_20260926/DECISION_AND_BLOCKER_REGISTER.md`.
- Accepted owner v1.1 activation inputs remain final desk handoff; no generic
  revision questionnaire. See `notes/live_activation_v1_3_artifact_review/revision_v1_1/`.
- Next: versioned descriptor/admission integration and evidence reconciliation,
  admitted non-GPU mount/source verification, then real governed path proofs.
  Preserve current authority and prototype fidelity. GPU connectivity is available;
  qualify census-worker bindings under the current M1 scope above, not old parked notes.