# SPRINT PLAN · post-tonight-GPU-activity

**Author:** main agent · 2026-08-31
**Authority:** synthesized under owner rulings 3–5 (2026-08-31 tonight thread, banked in DECISIONS.md)
**Discipline:** tests-first, thin-kernel, no-bypass, double-green ratchet, no push. Every line item below is chartered work — the owner ratifies scope and sequencing before commits land.
**Current ratchet floor:** 2680 (per `backend/tests/invariants/baseline_failures.json · counts_at_baseline.passed`). Local uncommitted work: keypair-hardening tests (11 tests) + Wave-G5c-COMPUTE-FRONTEND (declared).

---

## Executive framing — what's on the table

Four independent tracks compete for wave slots. Each is chartered with scope, prerequisite, tests-first shape, receipts, and honest estimate. Owner picks sequencing; agent does not sequence.

| # | Track | Chartered? | Estimate | Blocker |
|---|-------|-----------|----------|---------|
| **W-G5c-close** | Wave-G5c frontend close + owner eyeball bundle | ✅ **CLOSED 2026-08-31** · ratchet 2680→2692 · bundle in `phase0/eyeball_bundles/wave_g5c_close_20260831/` | Done | — |
| **W-G5c-COMPUTE-v2** | Compute-surface real-facts wiring (successor to retired tile-compute-* rules · targets the ACTUAL rendered Compute Connected dummies) | ✅ **CLOSED 2026-08-31T~21:30Z** · ratchet 2692→2703 · 11 tile-value rules bound to `/api/compute/estate` (4 LIVE · 6 HONEST-EMPTY · 1 LIVE-TAUTOLOGY) · harness green (compute-view: distinctive dummies absent, live phrasings present, `marked_slots=11`) · residuals `-r1` (chart-captions) + `-r2` (tile-notes) banked, not fixed | Done | — |
| **W-WPW-v1-c** | WPW Tier 1 Lab Notebook writer + auto-attach at commissioning (WPW-1..-7, WPW-18 + A1/A2/A6) | ✅ **CLOSED 2026-08-31T~22:00Z** · ratchet 2703→2717 · 14 invariants in `test_wpw_tier1_notebook.py` · `services/wpw/tier1_notebook.py` (append-only + hash-chained + zero-influence + causal-lexicon refusal + reference-only CIF) · `training_runner.open_run()` hooked · **concession banked**: tests+module co-authored, right-reason validity by inspection only, no mechanical RED drill receipt | Done | — |
| **W-WPW-v1-d** | WPW Tier 2 Technical Report drafter (WPW-8..-10 + A4/A6) — auto-draft on run-settle, fixed section skeleton, every figure resolves to run artefact | Yes (next in sequence per WPW_CHARTER.md sub-wave map) | ~½ day | Unblocked |
| **W-TxtTrain-v2** | Improved LoRA text training run · deeper row sampling (OFFSET~500K) + `sms_log.sms_sent` secondary corpus + uniqueness pre-filter + larger slice · same masking discipline as v1 | Yes (unblocked by owner 2026-08-31T~21:20Z "run a longer one" go-ahead, banked verbatim) | ~1 day (corpus prep 60–90 min + ~2h train + collect/register) | Unblocked (owner-authorized) |
| **W-Orchestrator-Resilience-r1** | Teach pod-side orchestrator to heartbeat-log + run under supervisor + resume idempotently + expose orphan-run API — after the pod-side observer died at ~22:02Z during the 2h burn (on-host burns completed fine; only the observer failed) | Yes (banked in DECISIONS.md 2026-09-01T02:55Z reconcile section, not scheduled) | ~½ day | Unblocked |
| **W-Shield-Train** | Shielded-training pipeline (masking policy → row executor → transport → LoRA unstub → cleanup) | Yes (this document) | 2–4 days | Owner ruling on masking-tier admission + Doc 02 §A5.2 authoring surface |
| **W-Audio-P2** | Audio archive Phase 2 admission (manifest hash → representative slice → HSS → GPU smoke) | Yes (this document) | 2–3 days after archive access granted | Access to source (bucket + credentials + manifest source) — currently absent |
| **W-WPW-v1** | Whitepaper Wizard v1 (Tier 1 lab notebook + Tier 2 technical report; Tier 3 blocked on R1/R2/R3) | Yes (charter forthcoming after v1 spec ingest) | ~2 days for Tier 1+2 | R1/R2/R3 owner rulings for Tier 3 |
| **Reuse-audit** | Cat 6–8 reuse audit resume | Parked | 1–2 days | Wave G close |

---

## Wave W-G5c-close · Wave-G5c frontend close · **CLOSED 2026-08-31**

**Status:** ✅ CLOSED · double-green byte-identical · ratchet 2680→2692.
**Bundle:** `phase0/eyeball_bundles/wave_g5c_close_20260831/` (portal, Registry aside live, Compute Connected tab · README + GPU-activity card).
**Retirements banked in DECISIONS.md:** 6 `tile-compute-*` rules (prototype never renders their dummies — `tools/compute_where_probe.py`).
**Follow-up chartered:** W-G5c-COMPUTE-v2 (below).

---

## Wave W-G5c-COMPUTE-v2 · Compute-surface real-facts wiring · **CLOSED 2026-08-31T~21:30Z**

**Status:** ✅ CLOSED · double-green byte-identical at floor 2703 (+11 from 2692) · harness green on Compute view · local commits only.

**What landed (11 rules total, all bound to `/api/compute/estate` via `pod_shell/frontend/src/App.js` V8_SUBSTITUTIONS + runtime mirror `/app/frontend/src/App.js`):**
- **LIVE (4):** `compute-v2-clusters-value` / `-byline`; `compute-v2-gpus-value` / `-byline`. Bylines derive from `v.compute.hosts[]` and `rollup.gpu_count_total`; no hardcoded host names or GPU model strings (invariant enforced).
- **HONEST-EMPTY (6):** `compute-v2-{capacity,committed,free,jobs-waiting,workflows-month,utilisation}-value` render `"not measured"` — estate has no mechanism yet for wall-clock capacity / allocation ledger / queue-depth / workflows-month / utilisation.
- **LIVE-TAUTOLOGY (1):** `compute-v2-runs-receipted-value` renders `"100%"` — governance guarantees a receipt per crossing by construction.

**Invariants (`backend/tests/invariants/test_compute_v2_frontend.py`, 11 tests, all green in double-green):**
- rule-must-match-rendered-DOM (each dummy present in probe artefact `tools/compute_v2_dom_map.json` from `tools/compute_v2_dom_enum.py`).
- LIVE rules derive from `v.compute` / `hosts` / `gpu_count_total` / `gpu_model` / `gpu_memory_gb` — no hardcoded literals allowed.
- HONEST-EMPTY rules render `"not measured"` and NEVER echo the prototype dummy.
- LIVE-TAUTOLOGY rule honestly asserts `"100%"`.
- No banned engineering vocab (IPs / ARNs / SSH / cluster IDs) leaks to the compute rendering.

**Harness (`tools/wave_g5_realchrome_verification_harness.py`, run receipt `phase0/eyeball_proxies/20260831T212715Z_..._v2.log`):**
- 20 rules declared (9 legacy + 11 compute-v2), `marked_slots=20` in merged Registry+Compute ground-truth, 0 orphans.
- Compute-view distinctive dummies absent: `on-premise · RMS AI DC, Nairobi`, `A100 80GB · single node`.
- Compute-view live phrasings present: `on-premise · akki-vm + akki-vm-ii`, `H200 140 GiB · 2 nodes`, `not measured`.
- Screenshot receipts: portal / registry / compute PNGs at same directory.

**Residuals banked (NOT bugs · scope statements, in queue for follow-on waves):**
- **W-G5c-COMPUTE-v2-r1** · CHART-CAPTION substitution. `COMPUTE_CHARTS.door.caption='1,240 hrs committed'`, `.state.caption='2,880 hrs this month'`, and per-bar `size` labels remain as prototype text. Tile substitution is complete; chart captions are separate scope.
- **W-G5c-COMPUTE-v2-r2** · TILE-NOTE substitution. Prototype tile notes (e.g. `'43% of the month'`, `'wall-clock across 4 GPUs'`, `'quoted against, not reserved'`) remain as prototype text. Tile values are substituted; notes are separate scope.

**Estimate:** 1 day each (small · same discipline). Both unblocked; owner sequences.

**Historical charter (retained for audit · what was authored ended up scoped as tile-values-only; residuals -r1/-r2 above cover the deferred surface):**
The 11 rules substituted the tile-VALUE elements below; tile-note and chart-caption dummies remained (banked as -r1 / -r2).

| Prototype element (visible on Compute Connected tab) | Prototype dummy | Landed render |
|---|---|---|
| Clusters attached · value | `1` | `2` (LIVE from `hosts.length`) |
| Clusters attached · byline | `on-premise · RMS AI DC, Nairobi` | `on-premise · akki-vm + akki-vm-ii` (LIVE) |
| GPUs · value | `4` | `4` (LIVE from `rollup.gpu_count_total`) |
| GPUs · byline | `A100 80GB · single node` | `H200 140 GiB · 2 nodes` (LIVE from gpu_model + gpu_memory_gb + hosts) |
| Capacity this month · value | `2,880 hrs` | `not measured` (HONEST-EMPTY) |
| Committed to Work · value | `1,240 hrs` | `not measured` (HONEST-EMPTY) |
| Free to Allocate · value | `1,640 hrs` | `not measured` (HONEST-EMPTY) |
| Jobs waiting · value | `2` | `not measured` (HONEST-EMPTY) |
| Workflows this month · value | `18` | `not measured` (HONEST-EMPTY) |
| Utilisation · value | `43%` | `not measured` (HONEST-EMPTY) |
| Runs receipted · value | `100%` | `100%` (LIVE-TAUTOLOGY · governance guaranteed) |

---

## Wave W-Shield-Train · Shielded-training pipeline (charter)

**Owner authority:** ruling 3 (2026-08-31 tonight thread, banked verbatim) — *"the shield path does not get shortcut under deadline pressure"*.

**Honest gap that motivated this charter (verbatim from main agent's report banked in DECISIONS.md):**
- Row-bearing masking tiers t1/t2/t3 DECLARED but `admissible_under_env: []`.
- Census engine aggregates-only by design; no row-bearing SQL executor exists.
- PII classification registry has 1 entry (occupation), needs comprehensive per-column classification.
- Governed masking policy (Doc 02 §A5.2) NOT authored.
- `execute_lora_train_real` stubbed.

**Sub-wave breakdown (owner sequencing):**

### W-Shield-Train-a · Governed masking policy authoring
- Author `backend/services/chokepoint/masking_policy.v0.json` per Doc 02 §A5.2, per-column classifications for the chosen training-material table(s). At minimum: (i) column classification (identity / PII / quasi-identifier / free-text / non-sensitive) with cautious default = PII; (ii) per-classification masking transform (drop / hash / bucket / k-anonymize / free-text sanitize); (iii) refusal semantics for unclassified columns.
- Tests-first: schema validation, cautious-default enforcement, refusal on unclassified columns, no-cleartext-PII invariant on masking-transform output.
- Deliverable: policy JSON + validator + test suite.
- Estimate: ~½ day.

### W-Shield-Train-b · Masking-tier admission ruling
- Owner ruling required. Frame as: "under `development` env, admit masking tier `t1_full_mask` (or a new tier `t_training_extract`) for training-material extraction. Acknowledge that LLM-crossing prerequisite is not landed. Bank the ruling verbatim in DECISIONS.md."
- Prerequisites stated honestly (from allowlist verbatim): (i) LLM chokepoint landed, (ii) tenant entity catalogue populated, (iii) governed masking policy authored (W-Shield-Train-a).
- Deliverable: DECISIONS.md ruling + updated `masking_tier_allowlist.v0.json` under owner authority stamp.
- Estimate: 0 code, owner-only.

### W-Shield-Train-c · Row-bearing SQL executor via chokepoint
- New module: `backend/services/chokepoint/row_extractor.py`. Registers as `kind="row_extract"` crossing. Refuses on any un-classified column. Applies per-column masking-transform BEFORE crossing. Emits crossing receipt with **shape only** (row count, column list, masking-transform summary) — NEVER content.
- Tests-first: refusal on unclassified column, masking-transform correctness per policy, receipt shape-only invariant, PII-free-receipt invariant, no-content-in-log invariant.
- Deliverable: module + test suite; wired to existing chokepoint validator.
- Estimate: ~1 day.

### W-Shield-Train-d · Masked-file transport to GPU host
- New module: `backend/services/training_runner/masked_transport.py`. Given a row_extractor output stream, materialises into a masked file on local disk, computes sha256, uploads to GPU host via `ssh_seam.execute_remote_command` (base64 heredoc or existing scp-equivalent seam), verifies remote sha256 matches, emits transport receipt.
- Tests-first: sha256 round-trip, PII-free receipts, cleanup-on-failure, refusal-if-remote-hash-mismatch.
- Deliverable: module + test suite.
- Estimate: ~½ day.

### W-Shield-Train-e · LoRA training-loop unstub
- Unstub `services.training_runner.ssh_seam.execute_lora_train_real`. Wire to a small open checkpoint already on GPU host (or download in a separate governed step). Consumes the masked file from W-Shield-Train-d, runs LoRA fine-tune, emits training-run record + step-loss log.
- Tests-first: run-record shape, receipts-per-epoch invariant, cost-against-estimate crossing.
- Deliverable: unstubbed function + test suite + smoke run on masked slice.
- Estimate: ~1 day (contingent on a–d).

### W-Shield-Train-f · Cleanup-receipt path
- Deletes masked file from GPU host after training completes. Verifies deletion with a follow-up `ls`. Emits cleanup receipt.
- Tests-first: no-material-resident-after-cleanup invariant.
- Deliverable: cleanup module + invariant.
- Estimate: ~2 hours.

### W-Shield-Train-g · Tests-first end-to-end integration
- Full pipeline invariant (RED then GREEN): a governed shielded LoRA run leaves (i) run-record, (ii) crossing receipts for extraction + transport + training + cleanup, (iii) no PII in any receipt or log, (iv) cleanup verified.
- Double-green ratchet close.
- Estimate: ~½ day.

**Total estimate: 2–4 days concentrated.** Depends on: owner ruling for W-Shield-Train-b.

---

## Wave W-Audio-P2 · Audio archive Phase 2 admission (charter)

**Owner authority:** DECISIONS.md L208 (Phase 2 declared, not-executed) + ruling 5 (2026-08-31 tonight thread) instructing "add the audio-archive admission … as its own wave line".

**Access gap (honest, banked):** The DigiCow audio archive referenced in Phase 2 is not accessible from this environment. Zero S3/bucket references in the two data-source connection records. Owner must provide (or confirm) archive location + read credentials + manifest source.

**Sub-wave breakdown:**

### W-Audio-P2-a · Access gathering (owner-facing)
- Owner supplies: endpoint (S3 / GCS / SharePoint / on-prem NAS / other), bucket names, read credentials (kept in `backend/.env` only), allowed egress path, manifest source (hash of the manifest before first byte crosses).
- Deliverable: banked in DECISIONS.md, credentials in `.env` only.
- Estimate: 0 code, owner-only.

### W-Audio-P2-b · Manifest hash-before-first-byte
- New module: `backend/services/data_source/audio_archive_manifest.py`. Reads the manifest (list of audio files, sizes, sha256 per file). Computes manifest sha256 BEFORE any byte crosses. Emits manifest-admission receipt.
- Tests-first: refusal-if-manifest-hash-changes invariant, no-byte-crosses-until-manifest-hashed invariant.
- Deliverable: module + tests.
- Estimate: ~½ day.

### W-Audio-P2-c · Representative slice admission (few hundred hours)
- New module: `backend/services/data_source/audio_slice_admission.py`. Given manifest, admits a representative slice (few hundred hours; owner-chosen sampling rule — random / stratified by language / by source / other) into estate custody. Materialises to `estate_root/audio_slice_<slice_id>/`. Verifies each file's sha256 matches manifest. Emits per-file crossing receipt (shape only).
- Tests-first: sampling determinism (given seed), sha256 verification per file, receipt shape-only invariant.
- Deliverable: module + tests + slice materialisation.
- Estimate: ~½ day + wall-clock for actual byte transfer.

### W-Audio-P2-d · HSS ingest + manifest verification
- Existing Layer-A audio handler consumes the slice into HSS custody with hash-registered artifacts. Verify slice sha256 matches manifest post-ingest.
- Tests-first: HSS-registration invariant, hash-round-trip invariant.
- Deliverable: HSS-registered artifact set + tests.
- Estimate: ~½ day.

### W-Audio-P2-e · GPU smoke test (small Whisper fine-tune or ASR eval)
- Governed training-runner run on the HSS-registered slice. Small Whisper family fine-tune OR eval-only pass, at owner discretion.
- Tests-first: run-record shape, receipts-per-epoch, artifacts hash-registered back.
- Deliverable: run record + hash-registered training artifacts.
- Estimate: ~1 day (contingent on a–d).

**Total estimate: 2–3 days after archive access granted.** Depends on: W-Audio-P2-a (owner-facing).

---

## Wave W-WPW-v1 · Whitepaper Wizard v1 (charter)

**Owner authority:** Part 2 of tonight-thread initial directive — ingest WPW v1 spec, bank verbatim, quote in test docstrings, charter Tier 1 + 2 implementation.

**Deferred prerequisite:** WPW v1 spec docx has NOT been ingested this session (blocked by GPU-activity thread and superseded by ruling 4). Ingestion is P0 for this wave; it's fast (< 30 min).

**Sub-wave breakdown:**

### W-WPW-v1-a · Spec ingest
- Download `cxm0vm8t_Whitepaper_Wizard_Spec_v1.docx` from provided customer-assets URL. Bank raw docx bytes in `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx` with sha256 recorded. Extract text with `tools/extract_docx.py`. Bank extracted text alongside as derived artifact (note the docx is authoritative; text is derived; verbatim quotes in test docstrings spot-checked against docx). Owner discipline (ruling 2 in prior session): "Bank BOTH: raw docx bytes … AND the extracted text alongside it".
- Deliverable: 2 files banked + sha256.
- Estimate: ~30 min.

### W-WPW-v1-b · Wave charter + reuse assessment
- Draft WPW wave charter: sub-wave breakdown, hooks to `training_runner`, Doc 5 ledger integration, audit trail. Reuse assessment against donor repos + Wave-H receipts (which of Tier 1/2 concepts already exist somewhere).
- Deliverable: `STATE/WPW_charter.md` + reuse-assessment section.
- Estimate: ~½ day.

### W-WPW-v1-c · Tier 1 (observational lab notebook)
- Contemporaneous run-notebook entry pattern per WPW spec Tier 1. Structured JSON schema (owner-visible fields: what ran, on which machines, what the GPUs did, wall-clock, results). Tests-first for schema + emit shape.
- Deliverable: `services/wpw/tier1_lab_notebook.py` + schema + tests.
- Estimate: ~½ day.

### W-WPW-v1-d · Tier 2 (technical report + data-statement)
- Data-statement pattern (datasheet-level: sources, row counts, fields included/excluded and why) — same shape the shielded-training W-Shield-Train pipeline will emit at run-registration time. Tier-2 technical report body per spec.
- Deliverable: `services/wpw/tier2_technical_report.py` + schema + tests.
- Estimate: ~½ day.

### W-WPW-v1-e · Tier 3 (BLOCKED)
- Blocked on parked rulings R1/R2/R3 (banked in prior session state — currently no rulings landed). Frame R1/R2/R3 crisply in the WPW charter (W-WPW-v1-b) as a single-shot owner question. Do not scope work until rulings land.

**Total estimate: ~2 days for Tier 1 + 2** after spec ingest. Tier 3 estimate deferred pending rulings.

---

## Sequencing — owner picks, agent does not

**Suggested prompts to help owner sequence (agent has no authority to choose):**
- If the eyeball bundle is what the owner has been waiting on, W-G5c-close closes it fast (< 1 day).
- If the shielded-training pipeline is the strategic priority, W-Shield-Train unblocks the DigiCow training run the owner asked for tonight — 2–4 days honest.
- If the audio archive path is the strategic priority, W-Audio-P2 unblocks a real Whisper fine-tune — 2–3 days after archive access granted.
- WPW ingest + charter (W-WPW-v1-a/b) is 30 min + ½ day and unblocks the WPW backlog.
- Reuse audit resume is Cat 6–8, deferred until Wave G closes.

**One friendly enhancement (agent's non-binding suggestion):** if the owner is optimizing for the shortest path to a real DigiCow training run tonight-plus, the natural sequence is:
1. W-G5c-close (½–1 day — closes the eyeball bundle owner has been waiting on).
2. **In parallel:** W-WPW-v1-a spec ingest (30 min — cheap, unblocks the WPW backlog).
3. Owner picks W-Shield-Train (build the shield) OR W-Audio-P2 (admit the audio archive) OR both (they are independent — different sub-teams could run them in parallel if resource allows).

Ratchet discipline unchanged throughout. No push. Local commits only.

---

## Tonight-GPU-activity thread carriers (banked)

- **Fallback burn ran tonight:** run_id `burn_20260831T183509Z_731f22ad` — see DECISIONS.md 2026-08-31 tonight entry for verbatim ruling + activity summary.
- **Audio-vs-text A-vs-C owner ruling still pending** (per owner ruling 5, escalated in parallel by the owner's own hand). If it lands audio: W-Audio-P2-a is the immediate blocker. If it lands text: same shielded-training scope (W-Shield-Train) applies (bypass ruling would authorize a masked-text extract under identifier-strip + PII-column-exclusion discipline).

