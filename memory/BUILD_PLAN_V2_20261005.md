# Akki — unified build plan v2: M1–M10 ∪ five promises ∪ Mα, in waves — 5 October 2026

Owner order (OWNER_ORDERS §11): "there are elements of M alpha that should have fed some of the buckets in M1–M10. Develop a new plan with clear waves breaking down how you are planning to complete the building for the requirements you have at present. Do not flatten, be seasoned and research where possible to ensure we have a much cleaner build with absolutely no post compaction impact."

Supersedes `EXECUTION_PLAN_20261005.md` (retained; its WP numbers are cross-referenced). Governing roadmap: `assessment_workspace/notes/goal_delivery_20260928/AKKI_GOAL_ROADMAP_v1.md` (M1–M10, acceptance packs M1-T1…M10-T6, gates G1–G10). Diagnosis: `SYSTEM_DIAGNOSIS_20261005.md`. Mα job register: `M_ALPHA_PLAN.md`.

Nothing in this plan raises a completion figure. States: `planned · implementing · ready_for_test · verified_pass · failed · blocked · decision_pending`. Live state of each work package lives in `BUILD_LEDGER.md` (append-only), never in this file.

---

## 0. Compaction-proof operating design (how "no post-compaction impact" is achieved)

The failure mode is known: each fork begins from an assistant-written summary and re-plans from it. The design below makes the summary irrelevant.

| Layer | Artefact | Rule |
|---|---|---|
| Entry anchor | `/app/AGENTS.md` | First read, every fork. Names this plan, the ledger and the diagnosis. Compaction handoffs are explicitly non-authoritative. |
| Plan (static) | this file | Work packages with sources, owners, tests, pass, resume protocol. Changed only by a new owner order or a recorded supersession. |
| State (append-only) | `memory/BUILD_LEDGER.md` | One line per state change: `at · WP · state · native ids · files · tests · next command`. Written **before** any compaction/fork and after every test run. Never edited, only appended. |
| Owner authority | `M_ALPHA_OWNER_ORDERS.md` | Append-only; sections hash-frozen by test. |
| Runtime truth | Mongo (`malpha_*`, Ledger, registry) and host job files | Plan/ledger point to native ids; they never restate metrics as fact. |
| Guardrail | `backend/tests/governance/test_requirements_anchor.py` | Every WP cites resolving sources; ledger WPs exist in the plan; owner sections unchanged; AGENTS.md names the anchors. Runs in every test batch. |

**Resume protocol (every fork, before any plan or question):** (1) read `AGENTS.md`; (2) run the governance test; (3) read the last 20 ledger lines; (4) verify the native ids they cite (job status, PIDs, test XML); (5) continue the WP named in the last `next command`. A question to the owner must cite the clause search performed or a D-row. No percentage is quoted from memory; it is recomputed from evidence or omitted.

**Checkpoint cadence:** a ledger line after each WP state change, after each test run, and whenever a WP has run for more than ~2 hours without one. A WP is sized so that one fork can take it from `implementing` to `ready_for_test` in one sitting; larger items are split (A1a/A1b…).

**Build hygiene (anti-flattening):** smallest justified change inside the existing owner service; no sibling implementation (RC-8); tests before implementation; negative paths in every WP; mocked fixtures labelled and never counted as live success; no runtime model download — model ingestion is a receipted registration act; running GPU lanes are never stopped or evicted.

---

## 1. Mα → M1–M10 reconciliation (what already fed which bucket, and what still owes)

| Mα job | Lands in | Acceptance pack(s) fed | Evidence already contributed (native) | Still owed to the pack |
|---|---|---|---|---|
| MA-01/02 traceability, hardware/rates, uncapped authority | Roadmap §1 readiness rule; M1.3 Compute Connected; M7-T3 | M1-T3 (compute identity/telemetry), M7-T3 | GPU snapshot seam, `budget_mode=uncapped_until_billing`, per-job GPU-seconds, rates register with governed authoring | GPU rate facts (D3); compute telemetry on the Registry card |
| MA-03/04/05 Shield separation/register/hostility | M4-T3 (meaning preserved across masking, no unauthorised disclosure); M2-T1/T3 (new boundaries re-run under Watch); M10-T3 | M4-T3, M2 coverage | `task_separation` receipts; register (regex); gate on both payload paths; deterministic hostility rules on payload | Contained reader, pre-redaction objective, canonical lifecycle, one entity set, dual-file seam, measured leak/utility suite (Wave A) |
| MA-06/07 general commission + durable scheduling | M9.1/M9.3; M9-T3 (checkpoint/interruption); M8-T1 | M9-T3 partial (`last_checkpoint`, carry rule, lineage-pair validation) | Supervisor (Solva+CIF) lineage into native dispatch; fault retry ≤3 then hold | `RealBackend`; continuity across pod pause (D1) |
| MA-08 measured routing | M4 model selection; M7-T4 commercial modes; Doc 11 LC-2 | M7-T4 partial | Trial `rt-9e6a2c92e8`, adopt/revert operator acts | Writer/reviewer task sets; ladder with a local rung |
| MA-09/10 AIP database, real codec | M9.2 perception; M1-T1 audio dimensions | M9-T1 partial (source→perception→unit with provenance) | 88,850 segments, Mimi 100 tok/s qualified per condition, two seals identical | Codec service consolidation (one implementation); lineage replay test |
| MA-11 Character Register | M9-T2 privacy gates | — (**failed**: organic features aggregated; existing boundary bypassed) | — | Wave B |
| MA-12/13 sealed sets, calibration | M9-T2 holdout | M9-T2 partial (v3 seal, independence verified) | `malpha_corpus_audit` on both hosts | Calibration curves (MA-13) |
| MA-14/15/16/17 storyteller, identity, spectral learning, listener | M9-T2/T4 | M9-T4 partial (identity distance measured, failing) | Dev metrics per iteration; supervisor cycles | Native labels (D2); identity gate pass; controlled comparison |
| MA-18 13-language LID | M1-T1 language dimension; M9-T1 | — | serving unloaded | Wave C |
| MA-19 non-audio | M9-T1/T2 for text/tabular/document/video rows | — | — | Wave C |
| MA-20 callable skills | M6-T4 | — | — | Wave E |
| MA-21/22/23 WPW | M9-T5 | M9-T5 partial (notebooks at commissioning, Tier-2 records) | `malpha_tier2_reports`, WPW events | Completeness replay; Tier-3 decisions (D5) |
| MA-24/25/26 outputs, interaction | M6-T1/T2/T3; M4-T1; M5-T1; M10-T2 | M6-T1 partial (estate packs v3–v7, byte-identical builds) | Doc-studio pipeline hardening | Blind comparison protocol; ordinary-user paths |
| MA-27/28 CaaS, domain offers | M3-T1…T5 (commission→delivery); M6-T4; M7-T1/T3 | — | CaaS metering lane | Wave E |
| MA-29/30 ARMI, economics | M7-T3/T5; M2 actor identity; M10-T6 | M7-T5 partial (attribution rule), M7-T3 partial (metering) | ARMI overview 16 identities; rate card UI | Lifecycle; nonempty bill; rates (D3) |
| MA-31 closure | M10 | — | — | Wave F |

Unmapped capability check (roadmap §1 rule): every Mα module now has an owning milestone above; none is out of scope.

---

## 2. Waves

Each WP: **Order** · **Sources** (must resolve) · **Bucket** (milestone packs / promise / Mα) · **Owner service** · **Already there** · **Build** · **Tests** · **Pass** · **Resume** · **Mode** (fg/bg) · **Decision**.

### Wave A — Shield capability inside the perimeter (P5; M4-T3, M2 re-coverage, M10-T3)

Order of execution: A1 → A2 → A3 → A4 → A5 → A6 → A7. A1 and A2 can run in parallel (A1 is deterministic, no GPU).

**WP-A1 Register lifecycle to canon; one entity set; vault intake** (= EXECUTION_PLAN WP-03)
- Sources: `.../source_text/02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File_4ca0109d.txt` (A4 B24–B31, A5.1 B34, A5.4 B37–B39, A5.5 B40, A6 B42–B45); `assessment_workspace/notes/RATIFICATION_C3_BATCH_20260913.md` (48 h / 7 d countdown defaults); `services/synisense/shield/semantic_register.py`; `services/synisense/shield/tenant_entities.py`; `routers/shield_register.py`; `services/media_library/`.
- Bucket: M4-T3, M7-T2 (same ceremony machinery) · P5 · MA-04.
- Owner service: `semantic_register` + platform change ceremony (Doc 14 case) + media-library upload.
- Already there: versioned register doc with history; propose/adopt/author/enforcement/delete routes; `propose()` cue-based draft generation.
- Build: `adopt` → status `pending`; new `approve` (second governed act) → `active`; crossing set = approved only. `remove` → ceremony record (proposed → counter-sign → countdown C3 default → applied → re-verified) with cancel; immediate delete retired. Migrate `tenant_catalogue.v0.json` entities into the register as authored `exact` declarations (provenance `migrated_from_catalogue`), `deidentify` reads only the register. Workbook intake: `POST /api/shield/register/vault` accepting the media-library upload id → rows → `pending` exact/pattern declarations + Review reach report over **measured** material only (A5.3).
- Tests: `tests/shield/test_register_lifecycle.py` — pending never affects a crossing; approve does; remove without counter-signature → 409; countdown cancel; catalogue parity (every old entity still recognised, measured on the catalogue file); 1,000-row workbook → pending set with invalid/duplicate rows reported; history/provenance complete.
- Pass: all transitions receipted; one set consumed; parity 100%.
- Resume: ledger line + `pytest tests/shield/test_register_lifecycle.py`.
- Mode: fg. Decision: none.

**WP-A2 Contained reasoning rung on the estate serving seam** (= WP-01)
- Sources: `.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` (A5.5 B43–B45, A5.6 B46); `.../source_text/11_Cost_and_Compute_Part_1_Local_First_and_Levers_81c3f1ca.txt` (A5.1 B35, B2.1–2.3 B62–B64); `services/training_runner/m9_serving.py`; `services/model_registry/registry.py`; `services/training_runner/ssh_seam.py`.
- Bucket: M9.4 serving; M4-T1 (local rung in the ladder); P5/P3 · MA-03/04/08.
- Owner service: `m9_serving` (attested artefact, hash-verified host loopback server, lineage-stamped answers, revoke, stop) + model registry roles.
- Already there: `start/health/classify/withdraw/stop` over admitted adapters; `base_registration.json` on both hosts (Qwen3 bases, licence_verified, weight_sha256); SSH seam with receipts.
- Build: (a) registry role `contained_reader`; (b) host server gains `/read` — structured JSON (objective, meaning, categories, spans, safe rewrite) with a fixed system prompt and JSON-schema output, served from a registered base under vLLM **offline** (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `VLLM_NO_USAGE_STATS=1`, `DO_NOT_TRACK=1`, weights by local path only) with egress denied for that process (host firewall rule for the service user) — proved by a negative test that attempts an outbound connection from inside the process and must fail; (c) control-plane relay `shield_reader.read(...)` via the seam, bounded payload, request-scoped, no persistence of originals off-host; (d) unavailability refuses the Shield stage before any external client is constructed (no fallback to frontier for the read).
- Model selection (research lead, to verify on the estate at build time): Apache-2.0 Qwen3.8-27B (Aug 2026) is the strongest current dense open-weight candidate; bf16 ≈ 54 GB; Qwen3.5-9B ≈ 18 GB is the fit-safe candidate. Ingestion is a **receipted registration act** (licence text, revision, sha256, size) into `base_registration.json` + registry — not a runtime download. Pick the largest that fits the measured free memory beside the resident workload without eviction; placement is decided through the residency register (WP-C7, owner D7 ruling) and recorded there with its reason — the contained reader is class `serving_resident` (resident only under a demand lease).
- Tests: `tests/shield/test_contained_reader.py` — attest/hash; offline load; egress-denied probe; schema-valid output on SYNTHETIC contract/BRD/audit text; refusal when revoked (403); latency bound recorded; no outbound host in receipts.
- Pass: reads inside the perimeter with zero outbound connections; revoke works; registry entry complete.
- Resume: registry entry id + host port + ledger line.
- Mode: fg (control plane) + bg (host serving). Decision: D7 (default applies unless objected).

**WP-A3 Pre-redaction objective extraction, frozen and consumed downstream** (= WP-02)
- Sources: `.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` (B5.1–B5.5 B82–B98); `services/solva_v2/intent_audit.py`; `services/solva_v2/trace.py`; `services/solva_depth/pipeline.py`; `services/northena/`.
- Bucket: M4-T1/T3; P5 · MA-04/05.
- Owner service: Solva v2 faculties; Northena objective freeze; chokepoint.
- Already there: `IntentAuditRecord` (declared + demonstrated, append-only); trace; load-bearing/assertion seam; `solva/reasoning.py` frame-audit stage (external).
- Build: `shield/objective_capture.py` — reader (A2) on File 1 whole → `ObjectiveArtifact{intent, meaning, bounded_objective, declared_intent, sha256}` frozen (immutable record keyed by request id); attached to the request and **passed by reference** to the grounding/scope checks (one object, not two records); failure → `refuse` (system caller) or `ask` (human in loop) — never a guessed objective; demonstrated-intent observations appended via `intent_audit`.
- Tests: ordering (capture precedes de-identify, asserted on the receipt timeline); immutability (any mutation attempt refused); refusal on incoherent/contradictory SYNTHETIC questions; id-equality of the artefact consumed downstream; the redacted outbound still carries the extracted meaning (judged by the downstream acceptance on a fixed task set).
- Pass: all five B5 clauses exercised with negatives. Resume: ledger + test XML. Mode: fg. Depends: A2.

**WP-A4 Category-3 contained recogniser; reconstruction; cue-regex demoted** (= WP-04)
- Sources: `.../source_text/02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File_4ca0109d.txt` (A3 B21, A5.2 B35, A5.3 B36); `.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` (A5.4 B42, A6 B56); `services/synisense/shield/semantic_register.py`; `services/synisense/shield/register_gate.py`; `services/synisense/shield/task_separation.py`.
- Bucket: M4-T3; M2-T1 (new boundary re-covered by Watch); P5 · MA-03/04.
- Owner service: register + gate + reconstruct + task separation.
- Already there: `classify/reconstruct/joint_disclosure_check/inspect_outbound`; typed placeholders; local rebind; separation receipts.
- Build: Cat-3 declaration = DPO description bound to the reader (A5.2); Generate/Review/Edit use the reader to shape it and report reach on measured material; at the Shield stage the reader marks privileged spans/meanings (parties, IP, trade secret, value, status, indirect disclosure) → `reconstruct` builds the safe item; Cat-1 regex/NER and Cat-2 exact/pattern run deterministically alongside; `classify` contextual cues survive **only** inside `propose()` (draft proposer) and as advisory receipts — never a refusal cause; ambiguous reads refuse safely; `task_separation.REVEAL_CUES` replaced by the reader's intent verdict.
- Tests: `tests/shield/test_category3_reader.py` — paraphrase/indirect disclosure on SYNTHETIC contracts, BRDs, audit excerpts (English + Kiswahili); harmless-corpus regression (the 4–5 Oct false positives: "project", "internal", "token accounting", schema keys) → 0 refusals; seeded privileged meanings → 0 survivors in outbound; utility retained (downstream acceptance ≥ baseline); ambiguity → refusal; no original text in receipts.
- Pass: as listed, measured and recorded. Resume: ledger + test XML. Mode: fg. Depends: A2, A1.

**WP-A5 Shield as a discrete sealed stage; dual-file seam; chokepoint verifies the seal** (= WP-05)
- Sources: `.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` (A5.2 B36–B39, A5.3 B40–B41, A5.6 B46); `.../source_text/02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File_4ca0109d.txt` (B5.1–B5.6 B65–B85); `services/chokepoint/llm.py`.
- Bucket: M4-T3 (same window/exclusion determinism), M10-T3; P5 · MA-03/04/05.
- Owner service: chokepoint `invoke`; `task_separation`.
- Already there: de-identify → gate → emit → invoke → re-identify inside `invoke`; system+prompt both covered; receipts.
- Build: `shield/stage.py::stage(question, data, tenant, purpose)` → File 1 and File 2 assessed independently (separate passes, no shared context) → markers → re-association seam re-checks markers + minimal joint re-identification check (B5.6) → `SafeArtifact{safe_items[2], objective_ref, binding_map(local), receipt, seal}`; `invoke` gains `safe_artifact=` and **refuses any unsealed payload** once callers are migrated (mark twice); one external query with two items; mapping destroyed after the call; both files retained under masked-read custody (B5.4). Caller migration list enumerated and completed inside this WP (doc studio, chat, training-lab reviews, routing trials, CaaS); the legacy prompt path then refuses.
- Tests: `tests/shield/test_shield_stage.py` — independence (altering File 2 cannot change File 1's assessment); seam refusal on dropped marker; joint-disclosure refusal; unsealed payload refused at `invoke`; exactly one external call per request; mapping gone after call; retained files masked on read; AST sole-invocation negative scan still green.
- Pass: every live caller crosses through the stage. Resume: ledger + caller migration checklist in the WP record. Mode: fg. Depends: A3, A4.

**WP-A6 Superior NER for Category 1 (multilingual, offline, qualified)** (= WP-06)
- Sources: `.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` (A3 B21, A6 B56); `services/synisense/shield/deidentifier.py`.
- Bucket: M4-T3; M1 usability dimension (personal-data share); P5 · MA-04.
- Owner service: `deidentifier` NER slot (transformer → small fallback, fail-closed, offline since 5 Oct).
- Already there: regex layer (Luhn, phones, e-mail, IDs, P.O. Box), installed spaCy models, disclosed model name.
- Build (research lead): qualify a schema-conditioned recogniser (GLiNER2 family — `gliner2-privacy-filter-PII-multi`, `gliner2.5-multi-v1`) installed offline on the estate with licence/hash; LoRA-adapt on estate transcripts for Kiswahili/Kikuyu/Kamba using the existing training path (a real run, M9-T2 evidence); measure P/R per type (PERSON, ORG, phone, e-mail, national ID, KRA PIN, payment card, health/biometric identifiers) on a labelled SYNTHETIC + estate-derived set; winner becomes the prescribed primary; spaCy small stays the disclosed fallback; CPU/ONNX path acceptable.
- Tests: `tests/shield/test_ner_qualification.py` — per-type P/R; no network during load; fallback disclosure.
- Pass: measured P/R recorded; model disclosed on `/api/healthz/shield`. Resume: ledger + registry entry. Mode: fg + bg (LoRA run). Decision: none.

**WP-A7 Watch re-coverage of the new Shield boundaries** (roadmap: "every new operation added after M2 reruns the relevant Watch coverage tests")
- Sources: `AKKI_GOAL_ROADMAP_v1.md` §1 gates; `services/watch/input_seat.py`; `services/synisense/shield/register_gate.py`.
- Bucket: M2-T1/T3/T4 re-run on the stage/reader/vault boundaries.
- Build: enumerate the new boundaries (stage, reader relay, vault intake, approve/remove ceremony) in the Watch observed-surface inventory; emit crossings; drills on SYNTHETIC hostile inputs through the real services.
- Tests/Pass: M2 drill pack subset green on the new inventory. Mode: fg. Depends: A5.

### Wave B — Audio-as-database privacy and AIP compliance (P1; M9-T2/T4; MA-10/11/15)

**WP-B1 Attribute eligibility, write boundary, custody partition, invariant harness** (= WP-07)
- Sources: `assessment_workspace/canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec.txt` (§5–§7); `services/audio_plane_v1/character_register_write_boundary_v1.py`; `services/audio_plane_v1/leakage_path_harness.py`; `services/audio_plane_v1/cluster_storage_boundary_v1.py`; `services/training_lab/malpha_worker.py`.
- Bucket: M9-T2 privacy gates; M9-T1 (no dropped character dimension) · MA-11.
- Owner service: `audio_plane_v1` write boundary + harness (exists, unused by Mα).
- Already there: refusals for small stratum, idiolect marker, narrowing combination, exemplar storage, non-learned; min-group-size config; Mα segment rows, PCM store, codec codes, `character_register()` percentiles.
- Build: attribute eligibility table (organic: `f0_mean_hz`, `f0_range_hz`, formant/VTL proxies, absolute spectral tilt; acquired after speaker-normalisation: timing, pause ratio, chars/s, energy dynamics, prosodic contour shape); derived register written **only** via `write_character_entry` (replace `malpha_worker.character_register`); custody partition on the host: `raw_material/` (PCM, per-segment organic measurements) vs `derived_register/` with separate manifests and custody classes; read paths carry lineage; temporary speaker representations destroyed after use (test proves none persist); harness runs on register code change. Applied by a new CPU phase on the next AIP build; running jobs untouched.
- Tests: harness fails to store the four leakage paths; no organic column in the derived register; lineage on every read; cleanup proof.
- Pass: register entries pass the boundary; partition manifests exist on both hosts. Mode: bg (CPU phase). Depends: none.

**WP-B2 Biometric-excluding derived spectrum — candidates qualified by the VoicePrivacy protocol** (= WP-08)
- Sources: `Audio_Plane_Spec.txt` (§6.2 conditions, §7.2 distance gate); `services/training_lab/malpha_voice_worker.py`; `services/perception/audio_codec/`; `services/training_lab/malpha_worker.py` (Mimi content/character split).
- Bucket: M9-T2/T4 · MA-11/15/16.
- Research lead (to verify on the estate): VoicePrivacy Challenge 2024 evaluates privacy as **EER under a semi-informed attacker** (ASV retrained on anonymised data), utility as **WER** on a fixed ASR and emotion retention; its neural-codec baseline keeps semantic tokens and re-generates acoustic tokens from a pseudo-speaker pool — exactly the Mimi codebook-0 (content) / codebooks 1–7 (character) split already qualified in the AIP build. Simple signal perturbation (the owner's "basis points" idea; McAdams-type baselines) is known to give weak privacy against a semi-informed attacker — this is tested, not assumed.
- Build: three candidates measured per language on a held-out sample: (1) codec-token anonymisation (content codes kept, acoustic codes re-synthesised under a constructed identity drawn from the register strata — the inverse-of-cloning principle); (2) speaker-normalised features (per-cluster F0/formant normalisation to the group distribution); (3) parameterised perturbation of organic dimensions (owner's thought). Per candidate: linkage test (ECAPA ASV retrained on anonymised data; EER derived-vs-source → chance), utility tests (listener dev P/R, text/voice dev metrics, codec reconstruction by condition), character retention (normalised prosodic contour similarity by language stratum). Adoption only when all pass; recorded in WPW; never applied to sealed admission material.
- Tests: `tests/malpha/test_audio_privacy_transforms.py` (synthetic unit) + host phase report.
- Pass: a candidate with EER ≈ chance and utility within tolerance per language, or an honest "not yet achievable" record. Mode: bg. Depends: B1.

**WP-B3 One codec implementation** (RC-8)
- Sources: `services/perception/audio_codec/service.py` (descriptor skeleton); `services/training_lab/malpha_worker.py` (working Mimi path); `M_ALPHA_PLAN.md` MA-10.
- Bucket: M9-T1 · MA-10.
- Build: the perception codec service becomes the owner of the Mimi implementation (encode/decode, token provenance, condition refusal); `malpha_worker` imports it; descriptor contract retained.
- Tests: existing codec qualification numbers reproduced through the service; missing-codec-version refusal.
- Pass: one implementation, identical qualification results. Mode: fg. Depends: none.

### Wave C — Training generality, continuity and admission evidence (P1; M9-T1/T3/T5, M1-T1)

**WP-C1 Control-plane continuity** (= WP-09) — Sources: `.emergent/crons.yml`; `services/training_lab/malpha.py`; `M_ALPHA_EXECUTION_LOG.md` §8. Bucket: M9-T3, M8-T1 · MA-07. Build per D1: (a) deployed always-on control plane (the platform's recurring dispatcher runs against the deployed URL), or (b) host-side lane continuation under the same recipe ladder with leases. Test: simulated pause → next iteration dispatched within one tick of a lane completing. Pass: zero control-plane-attributable idle GPU-hours over 24 h. Mode: fg. Decision: **D1**.

**WP-C2 `RealBackend` and non-audio rows (MA-19)** (= WP-10) — Sources: `.../source_text/AKKI_Canon_Documents_17_20_v3_991e02ad.txt`; `services/training_lab/skill/scripts/backend.py`; `services/training_lab/production.py`; `services/training_lab/production_contracts.py`; `services/training_runner/m9_dispatch.py`. Bucket: M9-T1/T2 for text, tabular/time-series, document-vision, temporal-video rows · MA-06/19. Build: `RealBackend` dispatches qualified recipes through `m9_dispatch` phases with real artefacts; `validate_definition` admits the new kinds; `gpu_hour_cap` gains the explicit uncapped representation; closed support matrix; unsupported rows refuse. Tests: estate/upload input → recipe → artefact → six-criterion acceptance → scoped serving per row; invalid manifest/unsupported model refusals. Pass: every advertised row executes with real artefacts; no StubBackend admission. Mode: fg + bg (runs). Depends: C1 recommended.

**WP-C3 13-language LID restoration, scoped routing, capability truth (MA-18; M1 §A/§B gaps)** (= WP-11 + WP-0A) — Sources: `M1_M10_STATUS_20261003.md` §A/§B/§E; `services/audio_plane_v1/language_cognition_worker.py`; `services/census_autonomy/estate_forecast.py`; `services/training_lab/signoff.py`; `services/training_runner/m9_readjudication.py`; `routers/health.py`. Bucket: M1-T1 (language dimension), M1-T3 (honesty), M9-T1 · MA-18. Build: restore serving of the admitted 8B text-LID on free capacity (no eviction); 13-class data/worker/report prerequisites (English/Maa per D6); consumers route non-admitted languages to the recorded baseline, never the Wanga head; `m9/capabilities` projection reads the signoff store; health routes mounted; estate report exposes listing-complete / content-measured / access-blocked distinctly. Tests: per-class coverage/rejection; forecast not capped at 12; routing audit; projections consistent. Pass: admitted classes served; no surface contradicts the signoff store. Mode: fg + bg. Decision: **D6**.

**WP-C4 Native admission evidence (MA-14/15/17)** (= WP-12) — Sources: `services/training_lab/malpha_review.py`; `M_ALPHA_EXECUTION_LOG.md` §7; `services/training_lab/malpha_evaluation.py`. Bucket: M9-T2/T4 · MA-14/17. Build: reviewer identities (RMS operator principals), reviewer-only panel page under `v2_os.html`, storyteller naturalness/identity rating panel; sealed read unlocks on two labels per segment; one sealed read per candidate; exposure tracked. Pass: labels exist; sealed read performed and recorded. Mode: fg. Decision: **D2**.

**WP-C5 WPW Tier 1/2 completeness (MA-21/22)** — Sources: `services/wpw/`; `services/training_lab/malpha.py` (WPW events); `M_ALPHA_PLAN.md` MA-21/22. Bucket: M9-T5. Build: known-event replay test (every required event retained, none invented); Tier-2 nine-section skeleton + six criterion values for accepted and refused runs; private access. Pass: replay identical; reports complete for every settled run. Mode: fg.

**WP-C7 Residency register and terms of reference for what lives on GPU/host storage** (owner D7, OWNER_ORDERS §12)
- Sources: `memory/M_ALPHA_OWNER_ORDERS.md` (§12 D7 verbatim); `memory/M_ALPHA_GPU_PREFLIGHT.json`; `services/training_runner/m9_serving.py`; `services/model_registry/registry.py`; `services/training_lab/malpha.py`; `services/training_runner/ssh_seam.py`.
- Bucket: M1-T3 (compute identity/telemetry), M9-T3/M9.4 (serving residency), M7-T3 (cost of residency once D3 prices exist) · MA-01/02.
- Owner service: model registry + `m9_serving` + Mα host job files.
- Build: one register (`residency_register`) listing every class of thing that may reside on a GPU or on host disk, each with terms of reference — `active_run_data` (PCM/codec/segments a running lane reads; resident for the run's lease, released on completion or fault, never copied off the estate), `checkpoint` (per-iteration adapters; last-good + candidate on host disk, admitted one copied to the registry path, the rest pruned by rule), `admitted_model` (on host disk/CPU memory, pulled to a GPU only under a serving demand or a training order, never resident idle), `serving_resident` (resident while a demand lease exists; renewed by demand; released otherwise — the contained reader of A2 is this class), `derived_register` (AIP character register; host disk under its custody partition, reuse-first), `raw_material` (B1 partition; host disk, lineage on every read). Each entry: class, host, device/path, bytes, owning job or registry id, lease/expiry rule, reuse pointer (what may reuse it in place instead of moving it), last verified. Placement for A2 is decided by reading this register (fit beside resident workloads, no eviction) and recorded as an entry with its reason. Measured by the existing `capture_gpu_spend()` snapshot seam; nothing is moved or deleted by this WP — it records and refuses placements that violate a TOR.
- Tests: governance test `test_residency_register` — every class has a TOR; a placement that would evict a running lane is refused; an admitted model is never recorded as idle-resident; snapshot reconciliation reports unaccounted residents as findings, not silently adopted.
- Pass: register populated from both hosts; A2 placement recorded through it. Mode: fg (control plane; read-only host probes). Decision: D7 (ruled).

**WP-C6 Calibration and controlled spectral comparison (MA-13/16)** — Sources: `Audio_Plane_Spec.txt` §11; `services/training_lab/malpha.py` recipes; `services/training_lab/malpha_comparisons.py`. Bucket: M9-T2/T5. Build: 3–4 volume calibration per stratum with uncertainty; same-base/same-budget baseline vs spectral-feedback recipe; time-to-quality and GPU-hours-to-quality recorded; "no improvement" is a valid result. Pass: reproducible measured comparison in WPW. Mode: bg (uses free lane time; never pre-empts).

### Wave D — Output quality, model selection and the maker-quality experience (P3; M6-T1/T2/T3, M4-T1/T5, M5-T1, M10-T2)

**WP-D1 Blind output-quality comparison protocol (MA-24/25)** — Sources: `M_ALPHA_QUALITY_REFERENCES.md`; `services/transform_forms/doc_studio/`; `services/transform_forms/deck_engine/`. Bucket: M6-T1/T2/T3 · MA-24/25. Build: fixed briefs; same evidence; blind rubric scoring against named references; accepted-output all-in cost (money only with D3). Pass: measured result per output type; no universal-superiority claim. Mode: fg.

**WP-D2 Ladder with a local rung; writer/reviewer task sets (MA-08; Doc 11 LC-2)** — Sources: `.../source_text/11_Cost_and_Compute_Part_1_Local_First_and_Levers_81c3f1ca.txt` (B2.1–2.3, B4.2); `services/chokepoint/routing.py`; `services/chokepoint/model_roles.py`. Bucket: M4-T4/T5, M7-T4 · MA-08. Build: the contained reader (A2) enters the ladder as a measured local rung for task classes where it meets the floor (LC-2); writer and reviewer task sets; fail-transparent-upward; adoption remains an operator act. Pass: per-class routing decisions reproducible with measured evidence. Mode: fg. Depends: A2.

**WP-D3 M4 two-path capability comparison (CC-12/14) through the Shield stage** — Sources: `AKKI_GOAL_ROADMAP_v1.md` M4-T5; `M4_M5_READINESS_20260929.md`; `services/chat/`. Bucket: M4-T5 (≥200 tasks, two paths, ≥400 outcomes). Build: run the adopted task set in the isolated benchmark boundary with the stage in place; reconcile every outcome; report delta per class with named causes. Pass: measured, reconciled, no production bypass. Mode: fg (chargeable frontier calls disclosed before run). Depends: A5.

**WP-D4 Maker-quality interaction paths (MA-26)** — Sources: `M_ALPHA_PLAN.md` MA-26; `frontend/src/pages/os/` (Train Models, Documents, Chat under `v2_os.html`). Bucket: M4-T1, M5-T1, M10-T2. Build: commission → preview → refine → cancel/resume → retrieve, desktop + mobile, visible costs/status/refusals; no dead actions. Pass: ordinary-user journeys recorded by the testing agent. Mode: fg.

### Wave E — Commercial operation, CaaS, ARMI, M3/M7 closure (P2/P4; M3-T1…T5, M6-T4, M7-T1…T5)

**WP-E1 M7 rule atomicity and Rules Updates** — Sources: `services/checker/state_machine.py`; `routers/checker.py`; `assessment_workspace/notes/m7_m8_readiness_20260930/READINESS.md`. Bucket: M7-T2. Build: effective state only after Ledger emission (single transaction); Rules Updates page wired to the one registry. Pass: M7-T2 restart-at-transition test. Mode: fg.

**WP-E2 CaaS external principal journey and a nonempty reconciled bill (MA-27; M7-T3)** — Sources: `services/caas/`; `services/entitlement_service_v1/`; `routers/portal_entitlement.py`; `services/cost_ledger/`. Bucket: M3-T1…T5, M7-T1/T3 · MA-27/30. Build: second principal/app commissions a scoped licensed context product → consumes → metered → billed → withdrawal stops access and derived memory; billing routes mounted where the owner UI expects them. Pass: T27 + M7-T3 reconciliation. Mode: fg. Decision: D3 for money.

**WP-E3 Domain offers (MA-28; MA-20 skills)** — Sources: `M_ALPHA_PLAN.md` MA-20/28; `services/skill_files/`; `services/caas/`. Bucket: M6-T4, M3-T1 · MA-20/28. Build: content mining, media planning, campaign strategy as versioned bundles on the common runtime with accepted deliverable schemas; callable through the ordinary boundary. Pass: T20/T28. Mode: fg. Depends: E2.

**WP-E4 ARMI lifecycle and score contract (MA-29)** — Sources: `services/armi/`; `FIVE_PROMISES_CANON_ASSESSMENT_20261004.md` N1–N3; `.../source_text/Akki_Canon_8_The_Watch_3d48a9c9.txt` (W13). Bucket: M7-T5, M10-T6 · MA-29. Build: onboard → bind versions → assign → complete → score (N2 contract) → suspend/revoke; Watch profiles never exported; no invented malicious probability. Pass: T29. Mode: fg.

**WP-E5 M3 ordinary commissioning journey closure** — Sources: `assessment_workspace/notes/m3_execution/M3_LIVE_EXECUTION_20260929.md`; `services/northena/`; `services/custody_delivery/`. Bucket: M3-T1…T5. Build: intent → draft → feasibility → review → commission → delivery → recipient retrieval; late-rights and recovery cases. Pass: M3 pack. Mode: fg.

### Wave F — Recovery and independent acceptance (M8 nondeferred, M10; MA-31)

**WP-F1 M8 nondeferred recovery matrix** — Sources: `assessment_workspace/notes/m7_m8_readiness_20260930/READINESS.md`; `services/business_continuity/`. Bucket: M8-T1/T2/T3/T5 (site restore and real notifications remain owner-deferred). Pass: pack rows green on isolated drills. Mode: fg.

**WP-F2 M10 independent acceptance (MA-31)** — Sources: `AKKI_GOAL_ROADMAP_v1.md` M10; `M_ALPHA_PLAN.md` MA-31. Build: six journeys on one identified build by a non-builder verifier; privilege withdrawal mid-job; crash/restart; malicious context; multilingual quality; owner evaluates the two audio products and WPW outputs. Pass: all mandatory rows independently passed. Mode: fg. Last.

**WP-F3 Completion account** — Sources: `AKKI_GOAL_ROADMAP_v1.md` M10.3. Build: delivered functions, scope, metrics, evidence links, dormant/non-adopted functions, genuine future additions. Pass: published; no orphan promise.

---

## 3. Sequencing, parallelism and gates

```
time →
GPU lanes (listener/text/voice)  ═══════════════════════════════════════════════  bg, untouched
Wave A  Shield      A1 ─ A2 ─ A3 ─ A4 ─ A5 ─ A6 ─ A7
Wave B  Audio       B3 ─ B1(harness) ─────── B1(apply on next AIP build) ─ B2(candidates, bg)
Wave C  Training       C7(D7, before A2 placement) ─ C5 ─ C1(D1) ─ C2 ─ C3(D6) ─ C4(D2) ─ C6(bg)
Wave D  Output                               D2(after A2) ─ D1 ─ D3(after A5) ─ D4
Wave E  Commercial                                            E1 ─ E2 ─ E4 ─ E3 ─ E5
Wave F  Closure                                                                F1 ─ F2 ─ F3
```
- A and B start together (A is fg, B is harness-first then bg). C5 and E1 are independent deterministic items usable as fillers while A2's host work runs.
- Roadmap gates stay truthful: Wave A feeds M4-T3 and M2 re-coverage; Waves B/C feed M9; D feeds M4/M6; E feeds M3/M7; F closes M8/M10. No gate is declared passed by a wave finishing — each pack runs as written in the roadmap.
- Decisions D1–D7 (diagnosis Part F) are the only owner inputs; D1–D4 and D7 ruled in OWNER_ORDERS §12 (D7 = residency structure, WP-C7; D4 explanation owed).

## 4. Research notes (leads to verify on the estate at build time; not decisions)
- Contained rung: Qwen3.8-27B / Qwen3.5-9B, Apache-2.0; vLLM offline env + egress deny; `--gpu-memory-utilization` sized to the measured free memory beside the resident workload.
- NER: GLiNER2 schema-conditioned family; LoRA on estate transcripts for swa/kik/kam; ONNX/INT8 CPU path; regex post-processing retained.
- Audio privacy: VoicePrivacy-2024 protocol (semi-informed EER, WER, emotion/character retention); neural-codec anonymisation maps onto Mimi content/character streams; perturbation baselines known weak — measured, not assumed.
- Continuity: the platform's recurring dispatcher is always-on only against a deployed control plane (D1a); D1b is a new host-side scheduler and needs the owner's word.

## 5. What this plan does not do
It does not unpause M5, reopen owner-deferred M8 items, adopt any threshold not recovered from canon or ruling, declare any Mα job complete, send originals to an external model, or alter running GPU work.
