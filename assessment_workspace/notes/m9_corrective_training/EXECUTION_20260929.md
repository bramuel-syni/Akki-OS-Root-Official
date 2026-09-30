# Corrective language cognition — live execution

## Authorisation and implementation

Owner selected review + background training and explicitly authorised **maximum utilisation, no spend limit**. See `OWNER_ORDER_AND_RECIPE.md` for the verbatim order and unmodified acceptance constraints.

One-off background jobs use the existing `language_cognition_dispatch` → hashed bundle → admitted SSH seam → detached worker → host receipt → run-certificate path. No new scheduler, recurring task, cloud instance, model provider or data-copy path was introduced. Full jobs were submitted through the normal authenticated `/api/portal/census/language-cognition/jobs` API (including its existing commission/Watch path), not a bypass. The staged authorised training corpus is distinct from the forbidden RMS estate extraction path.

## Verified smoke

- Job `lcj-07c848c58923`, completed `2026-09-29T17:18:48Z`, digest verified; one actual H200, real local corpus, real Opacus training.
- Two logical DP steps, physical batch 32; all trainable parameters had per-example gradients. RDP accountant epsilon 3.87023 at delta 1e-6, noise 1.0, clipping 1.0. This smoke epsilon is for its own small fixed subset and is NOT a prediction of campaign privacy spending.
- Optimiser, model and Python/NumPy/Torch/CUDA/loader RNG state saved. Accountant successfully reloaded from the actual checkpoint. Complete interrupted-run restoration parity was NOT proved and remains open.
- Peak allocated GPU memory ~2.88 GB. This is pipeline validation, not held-out quality or privacy acceptance. No speaker probe pass was fabricated for the smoke.
- Full prepared population: 182,816 train; 36,207 dev; 52,382 held; 161,872 archive-test windows; 1,080 excluded. Full trials use the complete prepared population, not the smoke's 1,024-window train subset.

## Full campaign (accepted, asynchronous)

| Trial | Job | GPU | Receipt/API submission | Recipe |
|---|---|---|---|---|
| A | `lcj-a6ea5b4bcdf6` | H200 index 0 | HTTP 202 at 2026-09-29T17:23:23Z | `trial_a_params.json`, adversary 0.2 |
| B | `lcj-e365bce78871` | H200 index 1 | HTTP 202 at 2026-09-29T17:23:29Z | `trial_b_params.json`, adversary 0.5 |

Both: seed 41; 20 epochs; logical/physical batch 512; distinct-window cap 180/file; host preprocessing parallelism 24 each; learning rate 3e-4; noise 1; clip 1; delta 1e-6. Same data/split, no wall-clock cutoff or declared spend cap. Their natural completion boundary is the declared 20 epochs followed by terminal evaluations, not endless compute consumption.

Pinned bundle for both: `52f3525e38da2d0c899f3ed3c9ac4e91c49f997e00ecbf140813007aec6b3c47`.

At `2026-09-29T17:27:50Z`, receipt `gpurcp-9fb52c5aa439` verified both processes alive and windowing the authorised local corpus (A 3,000/3,958 files; B 2,900/3,958). GPUs were still idle during this CPU input preparation; GPU saturation was **not** claimed at that checkpoint. Later GPU-training verification is appended below.

## Acceptance remains separate

The normal final-model commission gate still refuses `CleanMonolingualOnlyRefused`. These are admitted internal corrective research trials, not final-model commissions. Missing labelled code-switch spans and English/Sheng cannot be solved by longer optimisation. The final no-speaker-ID criterion stays chance-level; the old majority+0.05 probe is only a retained diagnostic comparator.

DP is example/window-level over the fixed manifest, not presenter-level or end-to-end privacy certification. Secure RNG is not installed; data-dependent preparation and dev/probe results are not private releases. No automatic model promotion, release, permanent-memory activation or production model replacement occurs. Results, privacy accounting and terminal diagnostics must be reviewed before any follow-on acceptance request.

## Testing and maintenance

- Testing report: `/app/test_reports/iteration_65.json`.
- Final targeted re-performance after test-harness cleanup: **42 passed, 1 skipped**, including authenticated external metadata API checks. No product defect was reported by the testing agent.
- Tests added: `backend/tests/census_operational/test_language_cognition_corrective_mode.py` and `test_language_cognition_api_get_only.py`. Live tests require opt-in and credentials from environment, not hardcoded accounts.
- Receipt corruption / wrong job or phase now fails closed; a dead worker with stale progress but no terminal receipt can no longer remain falsely running. Existing baseline regressions pass.
- App preview loaded; no UI changes. Credentials unchanged. Nothing is MOCKED in the remote training path; synthetic unit tests are not represented as real training quality evidence.

Existing read APIs list/refresh job status and bank terminal receipts/certificates on retrieval. The worker itself continues without this chat or browser and writes its host-side terminal result independently; no automatic user notification is claimed.

## Verified full-training checkpoint

At **2026-09-29T17:31:07Z**, host receipt `gpurcp-9498314f7d92` shows both full jobs in **corrective DP-SGD training**, epoch1/20: A step40 and B step50. Both report `dp_per_sample_verified=true`, logical batch512, ~25.79GB peak tensor allocation. Both worker processes are alive; no terminal quality result exists yet.

Ten-second utilisation sample ending **17:31:36Z**, receipt `gpurcp-f32616badfe0`: GPU0 mean45%, peak99%; GPU1 mean24.8%, peak100%; ~50,635MiB resident per GPU. Both GPUs are allocated to useful training but **sustained maximum utilisation has NOT been achieved**. Input preparation, per-example clipping and train-step gaps are throughput candidates; measure before changing the pinned recipe. Do not represent GPU reservation/peak utilisation as a sustained saturation benchmark. Throughput optimisation is a next action, not grounds to disable DP or alter acceptance criteria mid-run.
## Fixed-recipe retrain (owner order 4b) — TERMINAL, measured 2026-09-29T23:2xZ

Both 60-epoch trials submitted at 22:06Z through the authenticated API completed on **akki-vm** (`trial_a3_params.json` → `lcj-427526d3a19a` GPU0; `trial_b3_params.json` → `lcj-2add4984931e` GPU1): 5,340 DP-SGD steps each, logical batch 2,048 / physical 1,024, **2,705 windows/s, 50.5 GB, 72 min wall**, GPU utilisation observed 96 % / 86 % (the batch-512 trials of the afternoon ran at 45 % / 25 %). RDP accountant ε = 6.02 at δ = 1e-6 (noise 1.0, clip 1.0, Poisson sampling, secure RNG absent). Run certificates banked against the sealed defaults: `run_certificate_lcj-427526d3a19a.json`, `run_certificate_lcj-2add4984931e.json`.

| Trial | Recipe | Held-out presenters (accuracy / abstention) | Reading |
|---|---|---|---|
| A3 `lcj-427526d3a19a` | adversary 1.0 · bottleneck 32 · bottleneck noise 0.5 · speaker weight 0.5 · logit-adjust τ 1.0 | guz 0.20/0.38 · kam 0.13/0.38 · kik 0.68/0.36 · kln 0.66/0.32 · luo 0.74/0.27 · lwg 0.20/0.45 · swa 0.51/0.18; best dev epoch 28 | learns partially, far below the 0.90 default and the non-private baseline (0.94) |
| B3 `lcj-2add4984931e` | adversary 2.0 · bottleneck 16 · bottleneck noise 1.0 · speaker weight 1.0 | every language predicted **guz** (guz 1.00, all others 0.00, abstention 0.00); best dev epoch 16 | collapsed to a single class: the noise/adversary budget removes the language signal |

No-speaker-ID probe (guz, 18 presenters, chance 0.056, majority 0.30): bottleneck 0.36 / 0.37 and encoder 0.68 / 0.74 still identify presenters above chance; artefact output logits 0.32 / 0.35 sit below the majority baseline. **Verdict on both certificates: NOT ADMISSIBLE** (measured accuracy fails the default floor; speaker leakage remains in the representation; labelled code-switch / English / Sheng absent). Nothing was promoted or served.

What this establishes: the throughput problem is solved (batch 2,048, saturated H200s); the pinned corrective recipe trades away language accuracy for privacy far beyond the acceptance floor. The next move is a recipe decision, not more epochs — a controlled sweep (bottleneck noise 0.1–0.25, adversary 0.2–0.5, bottleneck 64, DP noise 0.5 at the same clip) would locate the trade-off curve. It is not launched here because the recipe was pinned by the owner (4b) and the standing rule forbids changing it silently.
