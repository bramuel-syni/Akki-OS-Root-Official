# M9 generalised (text) governed training — execution and GPU throughput, 2026-09-29/30

Owner order: "Finish M9 and retrain the language cognition model … autonomous until end, go with recommended" → this session: **1a** probe + full training in background, **2a** estate intelligence backend + portal report page, **3a** testing agent.

## 1. Throughput on the H200 (akki-vm-ii), measured, not assumed

All probes ran on the host through the pinned SSH seam with the shipped worker bundle (`tools/m9_remote_probe.py`); logs in `probe/`.

| Probe | Result |
|---|---|
| Synthetic, train mode, 1.7B, grad-checkpointing ON | 11.5k → 16.7k tok/s (4k → 32k tokens/step), 12–68 GB |
| Synthetic, train mode, 1.7B, grad-checkpointing OFF | **19.7k → 22.1k tok/s** (4k → 16k tokens/step), 31–112 GB; 32k tokens OOM |
| Synthetic, 8B, checkpointing OFF | 7.7k tok/s at 4k tokens/step (74 GB); 8k tokens/step 130 GB (too tight) |
| Synthetic, 8B, checkpointing ON | 5.3k–5.8k tok/s (4k–32k tokens/step) |
| **Real corpus batches, first token-budget batching (variable shapes)** | **1.9–2.2 s/step ≈ 6k tok/s** — 3.3× slower than the same token count at a fixed shape (0.59 s/step, 18k tok/s) |
| Same, `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` | no change (not the allocator) |
| Real batches, **shape-quantised token budget** (≤17 distinct shapes) | warm-up ≈ one step per new shape, then **0.59 s/step, 18.1k tok/s** |

Root cause of the 3× gap: every step with a never-seen (rows × width) shape pays kernel re-selection across ~1.8k GEMMs of the LoRA-wrapped model. Fix (worker `_batches`/`_collate`): sequences are bucketed to a fixed width ladder (16…512) and rows = budget ÷ width, so a run cycles through a handful of fixed shapes; eval batches are length-sorted and width-quantised the same way.

Recipe knobs added to `m9_worker.py` (all recorded on the run receipt): `tokens_per_batch` (token budget per step), `gradient_checkpointing` (off for the 1.7B, measured +35 %), per-base `base_recipes` in calibration; progress now reports `padded_tokens_per_step`, `rows_last_step`, and the result carries `padding_efficiency`.

Live effect in the campaign (worker state, not estimates): 1.7B calibration arms **16.6k–18.3k tok/s at 12.0–12.2k padded tokens/step, 90 GB** (smoke run before this session: 500 tok/s at batch 16, 26.6 GB); 8B arms 5.9k tok/s at 4.0k tokens/step, 79 GB. The first campaign launch (6k tok/s) was cancelled and superseded once the cause was measured (`campaign_20260929_full.json → superseded`).

## 2. Campaign (control plane `tools/m9_campaign.py`, every stage through the authenticated API)

Stage 1 in parallel: `calibrate` (GPU0, bases qwen3-1.7b-base + qwen3-8b-base, fractions ⅛ ¼ ½, §17.3 quote) ∥ `compare_optimizers` (GPU1, A17.5 AdamW vs Muon, ¼ data). Stage 2: full `train` on the calibration-selected base with the harness-selected optimizer (GPU0) and the runner-up base as a measured alternative (GPU1).

- `m9j-1e1b97ce8e1c` compare **completed**: baseline AdamW M-a +0.794, M-b −0.457 (non-target perplexity fell), ECE 0.011; Muon M-a +0.818 but **M-b +13.36** (non-target perplexity ×14) → harness verdict `ineligible` (quality_parity_breach on M-b) → AdamW carried forward. Banked as A17.5 comparison `m9-m9j-1e1b97ce8e1c`.
- `m9j-c4bec2810778` calibrate: results appended below when terminal.
- Full runs: appended below when terminal.

## 3. Not claimed

No model is served or admitted by this note; admission is the ceremony's record on each run certificate. MOAC floors are the disclosed DEFAULTS (M-a +5 pts, M-b 2 %). Grain, rights and language qualification for the audio plane remain M9's separate acceptance.
