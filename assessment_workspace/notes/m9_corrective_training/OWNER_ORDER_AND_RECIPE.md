# Language cognition corrective background run — 2026-09-29

## Owner authority (this conversation, verbatim)

Request: "For M9, before we get there - can akki run in the background a retrain of the language cognition model with lessons rewired into the trainning to resolve the issues and enhance quality?"

Confirmed choice B (review + background retrain): **"B - maximum utilization, no spend limit"**.

This authorises the corrective research campaign on the already admitted akki-vm-ii and already authorised labelled corpus. It does not waive rights/privacy/quality gates, authorise RMS estate extraction, approve new corpus sources, create paid infrastructure, or authorise final model admission. Corpus and weights remain on akki-vm-ii; only code, metadata and receipts cross the existing control channel.

## Pre-declared lessons and interventions

- Baseline `lcj-f96c86a16312` and its immutable results are retained. Luhya underperformed (~59.2% judged), speaker-ID probe failed, DP-SGD was not applied.
- More distinct windows of the existing authorised corpus, especially scarce Luhya; no duplicated examples or balancing sampler. Fixed language/recording-condition loss weighting and training-only spectrogram augmentation.
- Remove the frozen Vox embedding bypass from the new candidate (both registered bases and the old fusion baseline remain intact). Train Whisper encoder q/v LoRA plus a 128-wide bottleneck and conditional speaker/recording adversaries; this is an explicit recipe change, not a silently substituted baseline.
- Two-second native encoder input avoids computing 28 seconds of padding per two-second window.
- True Opacus clipped/noised per-example gradients across ALL trainable paths, Poisson sampling, physical-batch management, RDP accountant. No DP opt-out. Accountants remain separate per trial and privacy spending composes if more than one candidate is ever released.
- Scope of DP accounting: fixed window-example dataset only, not presenter-level DP; linkage, data-dependent corpus construction and development/probe measurements are not end-to-end privacy-certified. Cryptographically secure RNG is unavailable on this host. This is a retained internal research run, not a privacy-certified release.
- Reconstruct the original baseline presenter split with its original parameters. Never move its held-out presenters into training. Reserve every archive presenter, derive development presenters only from the training pool, exclude unlinked identities, remove audio-identical duplicates across sets. Presenter linkage is inferred within language; cross-language identity disjointness still needs independent qualification.
- Development-only checkpoint selection: minimum per-language correct/all windows, then macro score; abstentions count against selection. Original holdout is already observed and cannot be sold as a new blind test. Terminal held/archive/probe results are never used for gradient updates or candidate selection.
- Save model, optimiser, accountant, Python/NumPy/Torch/CUDA RNG, loader generator and manifest/recipe hashes at full epoch boundaries. Full interruption/resume parity is not claimed merely because a checkpoint exists.

## Execution limits and gates

- Smoke phase: two logical private steps and reload verification, pipeline evidence only.
- Real campaign: two independent trials, one per idle H200, 20 epochs each, no wall-clock/spend cutoff. Fixed stop at epoch completion or actual failure, not an endless loop to consume compute. Every trial uses the full distinct-window population allowed by the recipe. No new hardware is provisioned.
- Compare adversarial coefficients 0.2 and 0.5, same seed/data split, same DP settings. All hyperparameters declared before terminal tests. GPU utilisation will be measured, not assumed from allocation.
- Unchanged current quality thresholds: >=90% per-language, >=85% labelled code-switch span accuracy, chance-level no-speaker-ID, abstention reported. Legacy majority+0.05 probe diagnostic is retained for comparison ONLY; it is not the final acceptance criterion.
- Missing English/Sheng and verified per-span code-switch labels cannot be fabricated by longer training. They remain final-admission blockers, as do independent validation and privacy qualification.
- Final admission/promotion is ALWAYS false for this campaign. No replacement of an active model or overlay-to-measure regime flip.

## Host readiness observed

Receipt `gpurcp-ebceca9ff74b`: host `akki-vm-ii`; 2 NVIDIA H200 GPUs, both idle (0 MiB allocated, 0% sampled utilisation); ~6 TB free disk. Existing local corpus manifest, speaker clusters, corpus DB, model registrations and baseline training manifest present. Torch 2.11.0+cu128, Transformers 5.17.0, PEFT 0.21.0, Opacus 1.6.0, SpeechBrain 1.1.1; torchcsprng absent.

## Status

Implementation and initial offline regression: 36 passed, 1 skipped (2026-09-29). Live smoke and real campaign statuses are recorded in the companion execution note; this document by itself does not assert that a run has started or completed.