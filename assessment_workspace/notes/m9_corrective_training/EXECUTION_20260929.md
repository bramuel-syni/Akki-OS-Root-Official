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