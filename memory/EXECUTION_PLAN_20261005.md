# Akki — execution plan for the issued orders — 5 October 2026

Form: requirement → existing owner → mechanism → test → pass, as the owner directed (OWNER_ORDERS §8 item 3). Every work package (WP) lists `Sources:` that must resolve on disk; `tests/governance/test_requirements_anchor.py` checks this. States follow `M_ALPHA_PLAN.md` §1 (`planned`, `implementing`, `ready_for_test`, `verified_pass`, `failed`, `blocked`, `decision_pending`). Nothing below raises a completion percentage until its pass evidence exists.

Standing constraints (owner): estate-only data; no GPU cap or iteration ceiling; running GPU lanes are never stopped or evicted; enhance SyniSense/Solva/CIF/context preservation, never rebuild or bypass; no runtime model downloads; external task models receive governed safe context only; fixed `v2_os.html` authority; M5 pause and M8 deferrals stand.

Read with `SYSTEM_DIAGNOSIS_20261005.md` (issues, root causes RC-1…RC-9, pending decisions D1–D7).

---

## Wave 0 — guardrails and truth (foreground, first)

### WP-00 Requirements-first guardrail (RC-1)
- Order: OWNER_ORDERS §8 closing paragraph; §8 item 3.
- Sources: `/app/AGENTS.md`; `/app/memory/M_ALPHA_OWNER_ORDERS.md`; `/app/memory/REQUIREMENTS_RECONCILIATION.md`.
- Existing owner: `AGENTS.md` operating rule (5 Oct).
- Mechanism: (1) this plan's `Sources:` lines are machine-resolved; (2) owner-order files are append-only — a test fixes the SHA-256 of each existing numbered section and fails if any changes; (3) `AGENTS.md` names the diagnosis and plan as the first reads; (4) every future `ask_human` that requests a decision must cite the clause search performed, or be a D-row from the diagnosis.
- Test: `backend/tests/governance/test_requirements_anchor.py`.
- Pass: all sources resolve; section hashes stable; no WP without sources.
- State: implementing (this wave).

### WP-0A Status truth projections (RC-5)
- Sources: `M1_M10_STATUS_20261003.md` §B/§E; `services/training_runner/m9_readjudication.py`; `routers/health.py`.
- Existing owner: `training/m9 capabilities` projection; `signoff.admit_language_scoped`; estate report `_latest_store_outcome`.
- Mechanism: capabilities projection reads the signoff store (Wanga-only, music, Mα lanes) instead of a frozen ruling string; health/readiness routes mounted at `/api/healthz`, `/api/readyz`, `/api/healthz/shield` (source definitions exist, unmounted); estate report exposes listing-complete / content-measured / access-blocked as three fields.
- Test: live reads return the signoff-consistent capability list; health routes 200 with shield NER model disclosed; report fields coherent.
- Pass: no surface contradicts the signoff store. State: planned.

---

## Wave 1 — Shield capability (owner P0: "improve capability, deliver the promise, make it functional")

### WP-01 Contained reasoning rung inside the perimeter (RC-3)
- Order: OWNER_ORDERS §1 promise 5 ("most advanced LLM that can be contained in the SyniSense box"); §8 item 2 ("latest qwen self hosted, working with a superior NER").
- Sources: Doc 1 A5.5 (`.../source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt` B43–B45); Doc 11 A5.1/B2.1–2.3 (`.../11_Cost_and_Compute_Part_1_Local_First_and_Levers_81c3f1ca.txt`); `services/training_runner/m9_serving.py`; `services/model_registry/registry.py`.
- Existing owner: `m9_serving` (admitted-artefact loopback server on the estate host, hash-verified, lineage-stamped, revocable, relayed through the sealed SSH seam). Registered Qwen3 bases in `base_registration.json` on both hosts (licence_verified, weight_sha256).
- Mechanism: extend the host serving script with a `/read` endpoint (structured JSON output: objective, meaning, categories found, safe rewrite) over a registered base — registry role `contained_reader`, same attest/hash/revoke path; the control plane relays bounded requests via the existing seam; outbound from the host process is denied at the OS level for that service (no HF, no telemetry), proven by a negative test; refusal before any external client if the reader is unavailable (no external fallback). Candidate model = the newest Qwen3 instruct/base already registered or registrable offline on the estate; selection recorded with licence/hash; "latest" is whatever the estate can contain with verified licence, not a cached old model relabelled.
- GPU: D7 — default co-residency on akki-vm-ii GPU1 after a measured fit (bf16 8B ≈ 17 GB; 141 GB device with 52.7 GB resident); no eviction, no interruption of training.
- Test: `tests/shield/test_contained_reader.py` — health, hash attest, offline load (network denied), structured output on synthetic contract text, refusal when revoked, latency bound.
- Pass: reader answers inside the perimeter with zero outbound connections observed; revoke → 403. State: planned. Depends: D7 (default applies if no objection).

### WP-02 Pre-redaction objective extraction (Doc 1 B5.1–B5.5)
- Sources: Doc 1 B64–B98; `services/solva_v2/intent_audit.py`; `services/solva_v2/trace.py`; `services/northena/` objective freezing; `services/chokepoint/llm.py`.
- Existing owner: Solva faculties + Northena freeze; chokepoint.
- Mechanism: new Shield stage `objective_capture` runs the contained reader on the **whole** question (File 1) → `ObjectiveArtifact{intent, meaning, bounded_objective, declared_intent}`; frozen (hash, immutable record) and attached to the request; the same artefact is consumed by the downstream grounding/scope checks; extraction failure → refuse (system caller) or ask (human) — never a guessed objective; demonstrated-intent observations appended via `intent_audit`.
- Test: order test (extract precedes de-identify); immutability; refusal on incoherent/contradictory question; the artefact consumed downstream is the same object (id equality); redacted outbound still carries the extracted meaning (synthetic suite).
- Pass: all five B5 clauses exercised with negatives. State: planned. Depends: WP-01.

### WP-03 Confidentiality register lifecycle to canon (Doc 2 A4/A5; owner Cat 2 vault)
- Sources: Doc 2 B23–B45 (`.../02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File_4ca0109d.txt`); `RATIFICATION_C3_BATCH_20260913.md` (48 h system-ordinary / 7 d TCB countdown defaults); `services/synisense/shield/semantic_register.py`; `services/synisense/shield/tenant_entities.py`; `services/media_library/` upload path.
- Existing owner: `semantic_register` (versioned record, propose/adopt/author/remove) + platform change-ceremony machinery (Doc 14 case).
- Mechanism: (a) **Adopt = pending, Approve = live**: `author()` no longer writes into force; a second governed act approves; only approved declarations enter the crossing set. (b) **Removal runs the ceremony**: proposed → counter-signature → visible countdown (C3 default) → applied → re-verified; immediate `remove()` retired. (c) **One entity set**: the static tenant catalogue is migrated into the register as authored exact declarations with provenance; `deidentify` reads only the register's approved set. (d) **Confidentiality Vault Manager intake**: workbook upload through the existing media-library path → rows become exact/pattern declarations in `pending`, with a Review reach report over measured material (A5.3) before approval. (e) Full provenance per declaration (A5.5).
- Test: `tests/shield/test_register_lifecycle.py` — pending does not affect a crossing; approve does; removal without counter-signature refused; countdown cancel; workbook with 1,000 rows → pending set, duplicates/invalid rows reported; catalogue parity (every old catalogue entity still recognised).
- Pass: all transitions receipted; one set consumed at the crossing. State: planned. Depends: none (deterministic).

### WP-04 Category-3 contained recogniser + reconstruction; cue-regex demoted
- Order: OWNER_ORDERS §8 item 2 (Cat 3 definition and "both deterministic and reasoning").
- Sources: Doc 2 A3 B21, A5.2 B35, A5.3 B36; Doc 1 A5.4 B42, A6 B56; `services/synisense/shield/semantic_register.py::classify/reconstruct`; `services/synisense/shield/register_gate.py`.
- Existing owner: register + gate + reconstruct.
- Mechanism: a Cat-3 declaration is the DPO's description bound to the contained reader (A5.2 "category bound to a reasoning-layer recogniser"); the Generate/Review/Edit loop uses the reader to shape it and reports reach on measured material; at the Shield stage the reader reads the original and marks privileged spans/meanings (parties, IP, value, status, indirect disclosure) → `reconstruct` produces the safe item with typed placeholders bound locally; deterministic layers (Cat 1 regex/NER, Cat 2 exact/pattern) run alongside; the cue-regex remains only as a **draft proposer** inside `propose()` and as advisory receipts — it never refuses a crossing; ambiguous reads refuse safely.
- Test: `tests/shield/test_category3_reader.py` — paraphrased/indirect disclosure caught (synthetic contracts, BRDs, audit excerpts in English and Kiswahili); harmless schema/JSON words untouched (the regression corpus of the 4–5 Oct false positives); utility retained (the task remains answerable, measured by the downstream acceptance); refusal on ambiguity; no original text in any outbound record.
- Pass: measured FP rate on the harmless corpus = 0 refusals; seeded privileged meanings 0 survivors; utility ≥ pre-change acceptance rate. State: planned. Depends: WP-01, WP-03.

### WP-05 Placement: Shield as a discrete sealed stage; dual-file seam (owner §8 item 4; Doc 2 Part B)
- Sources: Doc 1 A5.2/A5.6 B36–B46; Doc 2 B47–B85; Doc 16 §3/§7 (via `REQUIREMENTS_RECONCILIATION.md` index); `services/chokepoint/llm.py`.
- Existing owner: chokepoint `invoke`; `task_separation.py`.
- Mechanism: `shield.stage(question, data, tenant, purpose)` → File 1 and File 2 assessed independently (no cross-input), each producing its safe form and markers; re-association seam re-checks markers and runs the minimal joint re-identification check (B5.6); result is a **SafeArtifact** (safe two-item context, objective artefact, local binding map, receipt, seal = SHA-256 over safe content + tenant + purpose). `invoke` accepts a `SafeArtifact` and **refuses any payload without a valid seal** (mark twice); the external call is one query with two items (B5.5); re-identification is local and request-scoped (A5.3); both files retained under masked-read custody (B5.4). Callers migrate to the stage; the legacy prompt path stays refused-by-default once migration is complete.
- Test: `tests/shield/test_shield_stage.py` — independence (File 2 content cannot change File 1's assessment), seam refusal on dropped marker, joint-disclosure refusal, unsealed payload refused at `invoke`, one external call per request, mapping destroyed after call, retained files masked on read.
- Pass: every live caller crosses through the stage; AST gate still proves sole invocation. State: planned. Depends: WP-02, WP-04.

### WP-06 Superior NER for Cat 1 (multilingual, offline, qualified)
- Sources: Doc 1 A3 B21, A6 B56; `services/synisense/shield/deidentifier.py` (offline loader, 5 Oct).
- Existing owner: `deidentifier` NER slot (transformer → small fallback, fail-closed).
- Mechanism: qualify a stronger recogniser on estate-like fixtures (English + Kiswahili at minimum): candidates are installed offline on the estate (licence recorded, hash pinned) and measured P/R per entity type incl. HII/BII/payment identifiers; the winning model becomes the prescribed primary; the installed small model remains the disclosed fallback; no runtime download path.
- Test: `tests/shield/test_ner_qualification.py` — labelled synthetic multilingual set; FP/FN per type; no network during load.
- Pass: measured P/R recorded per type; chosen model disclosed in `/api/healthz/shield`. State: planned.

---

## Wave 2 — Audio derived-store privacy (owner §8 item 4; AIP §§6–7)

### WP-07 Attribute eligibility + custody partition + invariant harness (MA-11 repair, RC-8)
- Sources: `assessment_workspace/canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec.txt` §§5–7; `services/audio_plane_v1/character_register_write_boundary_v1.py`; `services/audio_plane_v1/leakage_path_harness.py`; `services/training_lab/malpha_worker.py`.
- Existing owner: `audio_plane_v1` Character Register write boundary and leakage harness.
- Mechanism: (a) classify every `FEATURES` column as organic (F0 absolutes, formant/VTL proxies) or acquired (timing, pause ratio, chars/s, energy dynamics after speaker normalisation); (b) the derived register is written **only through `write_character_entry`** (min-group-size, idiolect, narrowing, exemplar refusals) — `malpha_worker.character_register` is replaced by a call into that boundary; (c) custody partition: raw PCM store and per-segment organic measurements are **raw-material custody** on the estate host, separated by directory, manifest and custody class from the admissible derived register; read paths carry lineage; temporary speaker representations are destroyed after use and a test proves none persist; (d) harness runs on every register code change.
- Test: harness fails to store the four leakage paths; no organic column in the register; lineage on every read; speaker-embedding cleanup verified.
- Pass: register entries pass the boundary; raw store partitioned. State: planned. Does not touch running jobs; applies to the next AIP build (`malpha_aip_requalify`-style CPU phase).

### WP-08 Biometric-excluding derived spectrum — candidate transforms qualified by evidence
- Order: owner's illustrative "add 3 basis points" — treated as a prompt to find a transform that removes anatomical identity without harming training utility; not a ratified algorithm.
- Sources: AIP §6.2 conditions, §7.2 distance gate; `services/training_lab/malpha_voice_worker.py` (speaker comparator); `services/perception/audio_codec/`.
- Existing owner: Mα AIP build phase; voice identity gate.
- Mechanism: candidates measured on a held-out sample per language: (1) speaker-normalised features (per-cluster F0/formant normalisation to the group distribution); (2) codec-token anonymisation (acoustic codebooks re-synthesised under a constructed identity, content codebook kept); (3) controlled perturbation of organic dimensions (the owner's idea, parameterised). For each: **linkage test** — speaker-verification EER derived-vs-source should approach chance; **utility test** — listener dev P/R, text/voice dev metrics, codec reconstruction by condition, before/after. Adoption only when both tests pass; evidence to WPW; never auto-applied to sealed admission material.
- Test: `tests/malpha/test_audio_privacy_transforms.py` on synthetic + estate sample via CPU/GPU phase.
- Pass: a transform with EER ≈ chance and utility within tolerance per language; otherwise recorded as not yet achievable. State: planned. Depends: WP-07.

---

## Wave 3 — Training generality and continuity (P1)

### WP-09 Control-plane continuity (RC-4) — decision D1
- Sources: `.emergent/crons.yml`; `services/training_lab/malpha.py::tick`; `M_ALPHA_EXECUTION_LOG.md` §8.
- Mechanism: (a) deploy the control plane (always-on dispatcher) — smallest change; or (b) host-side lane continuation under the same recipe ladder with leases. Until decided: no change.
- Test: simulated pod pause → next iteration dispatched within one tick of a lane completing.
- Pass: zero idle GPU-hours attributable to control-plane absence over 24 h. State: decision_pending.

### WP-10 MA-19 non-audio coverage — `RealBackend`
- Sources: Canon Docs 17–20 (`.../AKKI_Canon_Documents_17_20_v3_991e02ad.txt`); `services/training_lab/skill/scripts/backend.py`; `services/training_lab/production.py::validate_definition`; `services/training_lab/production_contracts.py`.
- Existing owner: training-lab production contracts + m9 dispatcher.
- Mechanism: `RealBackend` dispatches qualified tabular/time-series, document-vision and temporal-video recipes through `m9_dispatch` phases with real artefacts; `validate_definition` admits the new task kinds; `gpu_hour_cap` gains the explicit `uncapped_until_billing` representation (no Infinity); closed support matrix published; unsupported rows refuse explicitly.
- Test: estate/upload input → recipe → trained artefact → independent six-criterion acceptance → scoped serving, per row; invalid manifest and unsupported model refusal.
- Pass: every advertised row executes with real artefacts; no StubBackend admission. State: planned.

### WP-11 MA-18 13-language LID restoration
- Sources: `M1_M10_STATUS_20261003.md` §A/§B; `services/audio_plane_v1/language_cognition_worker.py`; `services/census_autonomy/estate_forecast.py`; `services/training_lab/signoff.py`.
- Mechanism: restore serving of the admitted 8B text-LID (unloaded since 4 Oct) on free capacity without eviction; complete 13-class data/worker/report prerequisites (English/Maa per D6); scoped routing so non-admitted languages use the recorded baseline, not the Wanga head.
- Test: per-class coverage/rejection; forecast not capped at 12; consumer routing audit.
- Pass: admitted classes served; register arithmetic uses the classifier. State: blocked on capacity + D6.

### WP-12 Native admission evidence (MA-14/15/17) — decision D2
- Sources: `services/training_lab/malpha_review.py`; `M_ALPHA_EXECUTION_LOG.md` §7.
- Mechanism: reviewer identities + reviewer-only page under `v2_os.html`; story naturalness/identity rating panel; sealed read unlocks only on two labels per segment.
- Pass: labels exist; sealed read performed once; result recorded. State: blocked on D2.

---

## Wave 4 — Product closure (M3/M4/M6/M7/M10; MA-20, 24–31)

### WP-13 MA-24/25 output quality comparison protocol
- Sources: `M_ALPHA_QUALITY_REFERENCES.md`; deck DR1–14 and doc-studio QA (`services/transform_forms/doc_studio/`, `services/transform_forms/deck_engine/`).
- Mechanism: fixed briefs → same evidence → blind rubric scoring against named references → accepted-output all-in cost (requires D3 for money).
- Pass: measured result per output type published; no universal-superiority claim. State: planned.

### WP-14 MA-27/28 + M7 commercial cycle
- Sources: Canon 7 §§3–33; DAP profiles; `services/caas/`; `services/entitlement_service_v1/`; `routers/portal_entitlement.py`.
- Mechanism: one external principal/app commissions a scoped licensed context product, consumes, is metered and billed (nonempty reconciled bill), loses access on withdrawal; domain offers (content mining, media planning, campaign strategy) as versioned bundles on the common runtime.
- Pass: T27/T28 of `M_ALPHA_PLAN.md`. State: planned.

### WP-15 MA-29 ARMI lifecycle + M7 rule atomicity
- Sources: Canon 3 §6.1, Canon 8 §3/W13, Canon 9; `services/armi/`; `services/checker/state_machine.py`; `routers/checker.py`.
- Mechanism: onboard → bind versions → assign → complete → score (N2 contract) → suspend/revoke; checker state becomes effective only after Ledger emission (single transaction); Rules Updates page wired.
- Pass: T29; checker atomicity test. State: planned.

### WP-16 M3/M4/M6 journey closure
- Sources: `M1_M10_STATUS_20261003.md` rows M3/M4/M6; `assessment_workspace/notes/m3_execution/M3_LIVE_EXECUTION_20260929.md`.
- Mechanism: ordinary commissioning→approval→delivery→recipient retrieval; two-path answer comparison; independent-review closure rule in `author.compose`; download audience decision for client material.
- Pass: per-row acceptance packs. State: planned.

### WP-17 M8 deferrals — unchanged (owner-deferred)
- Sources: `M1_M10_STATUS_20261003.md` row M8; `assessment_workspace/notes/m7_m8_readiness_20260930/READINESS.md`.
- State: decision-held; not reopened by this plan.

### WP-18 MA-31 / M10 independent acceptance
- Sources: `M_ALPHA_PLAN.md` MA-31; `M1_M10_STATUS_20261003.md` row M10.
- Mechanism: six cross-product journeys on one identified build; privilege withdrawal mid-job; crash/restart; malicious context; multilingual quality; owner evaluates the two audio products and WPW outputs.
- Pass: all mandatory rows independently passed. State: planned (last).

---

## Sequencing and parallelism
- Foreground now: WP-00 → WP-03 (deterministic, no GPU) → WP-01 (serving extension; needs D7 default) → WP-02 → WP-04 → WP-05 → WP-06.
- Background (no interruption): three Mα lanes continue under the supervisor; WP-07 harness built offline and applied on the next AIP build; WP-08 candidates measured on CPU/free GPU slices.
- After Wave 1 passes: WP-10, WP-0A, WP-13, WP-15; WP-11/WP-12 as D6/D2 land; WP-14/WP-16/WP-18 close the product.
- Decisions D1–D7 are listed in the diagnosis; defaults are stated where one is proposed; none is assumed ratified.
