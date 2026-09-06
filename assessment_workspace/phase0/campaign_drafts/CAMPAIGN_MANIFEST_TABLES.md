# Campaign manifests · owner-readable tables · 2026-09-06 → 2026-09-09

Both campaigns fit the 72-hour host window with the 20% watchdog margin (target: 58 productive hours per host).

---

## CAMPAIGN A · BASELINE LADDER · host = akki-vm

| # | Run name | Model | Base model ID | Corpus | Seed | LoRA rank | Ctx | Expected wall-clock (h · min/mean/max) | Objective |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `A-0-0p5B-seed01` | 0.5B | `Qwen/Qwen2.5-0.5B` | ussd_deduplicated | 1 | 16 | 1024 | 1.0 / 1.5 / 2.0 | Baseline · 0.5B rung · seed 1 |
| 2 | `A-0-0p5B-seed02` | 0.5B | `Qwen/Qwen2.5-0.5B` | ussd_deduplicated | 2 | 16 | 1024 | 1.0 / 1.5 / 2.0 | Baseline · 0.5B rung · seed 2 (reproducibility) |
| 3 | `A-1-1p5B-seed01` | 1.5B | `Qwen/Qwen2.5-1.5B` | ussd_deduplicated | 1 | 16 | 1024 | 3.0 / 4.5 / 6.0 | Baseline · 1.5B rung · seed 1 |
| 4 | `A-1-1p5B-seed02` | 1.5B | `Qwen/Qwen2.5-1.5B` | ussd_deduplicated | 2 | 16 | 1024 | 3.0 / 4.5 / 6.0 | Baseline · 1.5B rung · seed 2 (reproducibility) |
| 5 | `A-2-3B-seed01` | 3B | `Qwen/Qwen2.5-3B` | ussd_deduplicated | 1 | 16 | 1024 | 5.0 / 7.5 / 10.0 | Baseline · 3B rung · seed 1 |
| 6 | `A-2-3B-seed02` | 3B | `Qwen/Qwen2.5-3B` | ussd_deduplicated | 2 | 16 | 1024 | 5.0 / 7.5 / 10.0 | Baseline · 3B rung · seed 2 (reproducibility) |
| 7 | `A-3-7B-seed01` | 7B | `Qwen/Qwen2.5-7B` | ussd_deduplicated | 1 | 16 | 1024 | **10.0 / 17.5 / 25.0** | Baseline · 7B rung · **single seed** (ladder cap) |

**Wall-clock budget summary (Campaign A):** 28.0 h (min) / **44.5 h (mean)** / 61.0 h (max) · target 58 productive hours · **fits at mean with margin; may spill past productive hours if 7B lands at max estimate — trim recommendation: none this window (7B is already single-seed only).**

**Honesty note (banked in the JSON manifest):**
> 7B rung is single-seed only. 2-seed 7B (~20–50 h projected) does not fit the window with margin. Trim rationale: single-seed 7B is a ladder-cap reference point; reproducibility measurement is preserved at 0.5B/1.5B/3B where 2 seeds fit honestly.

**Disk estimate:** 24 GB (base-model snapshots for 4 sizes) + 2 GB (corpus + held-out) + 4 GB (adapter checkpoints across all 7 runs) = **~30 GB · 5.86 TiB volume · ~195× headroom.**

---

## CAMPAIGN B · METHOD ABLATIONS · host = akki-vm-ii · anchor = 3B

| # | Run name | Ablation delta from reference | Corpus | Dedup | LoRA rank | Ctx | Wall-clock (h · min/mean/max) | Hypothesis (CIF-ideation shape · declared BEFORE run) |
|---|---|---|---|---|---|---|---|---|
| 1 | `B-REF-3B` | — reference — | ussd + sms deduplicated | on | 16 | 1024 | 5.0 / 7.5 / 10.0 | Reference config · comparable to Campaign-A 3B seed 1 on USSD slice + additional generalisation from SMS contribution. |
| 2 | `B1-CORPUS-USSD-ONLY` | corpus = **USSD-only** (drop SMS) | ussd deduplicated | on | 16 | 1024 | 5.0 / 7.5 / 10.0 | Removing SMS narrows domain. Expected: narrower held-out generalisation, stronger USSD-slice performance. |
| 3 | `B2-DEDUP-OFF` | dedup = **off** | ussd + sms raw | **off** | 16 | 1024 | 5.0 / 7.5 / 10.0 | Duplicate-heavy corpus overfits repeated prompts. Expected: worse held-out generalisation than reference. |
| 4 | `B3-RANK-8` | LoRA rank = **8** | ussd + sms deduplicated | on | **8** | 1024 | 5.0 / 7.0 / 9.0 | Lower rank underfits. Expected: degraded held-out vs reference. |
| 5 | `B4-RANK-32` | LoRA rank = **32** | ussd + sms deduplicated | on | **32** | 1024 | 6.0 / 8.5 / 11.0 | Higher rank risks overfitting on this corpus size. Expected: diminishing returns or regression. |
| 6 | `B5-CTX-512` | context = **512** | ussd + sms deduplicated | on | 16 | **512** | 3.0 / 5.0 / 7.0 | Truncated context loses tail examples. Expected: degraded evaluation on long-response tasks. |
| 7 | `B6-CTX-2048` | context = **2048** | ussd + sms deduplicated | on | 16 | **2048** | **8.0 / 11.5 / 15.0** | Extended context increases per-step cost. Expected: marginal held-out gain at wall-clock premium. |

**Wall-clock budget summary (Campaign B):** 37.0 h (min) / **54.5 h (mean)** / 72.0 h (max) · target 58 productive hours · **fits at mean; MAX estimate hits the raw 72h ceiling — trim recommendation: drop B6 (ctx=2048) LAST if window is tight (context-length effect partially observable via B5 alone).**

**Honesty note (banked in the JSON manifest):**
> One-at-a-time ablation design (not full factorial) — 6 ablations × 1 seed each = 6 runs. 2×2×3×3=36-run full factorial doesn't fit any 3-day window at 3B. Single-seed ablations show DIRECTION of effect; a second seed at each ablation is a follow-on if the campaign window is extended.

**Disk estimate:** 6 GB (3B base-model snapshot) + 4 GB (2 corpus variants + held-out) + 3 GB (adapter checkpoints across 7 runs) = **~13 GB · 5.86 TiB volume · ~450× headroom.**

---

## Wizard-testing weave (Objective 3 · both campaigns)

Every run — Campaign A and Campaign B alike — carries by construction (owner-explicit "test the wizard logic(s) here"):

- **A1** · auto-attach Tier 1 notebook at first heartbeat.
- **A2** · WPW-1..WPW-7 events captured on checkpoints + anomalies + cost checkpoints.
- **A3** · Tier 2 report drafted at settlement · acceptance criteria MEASURE (held-out loss / perplexity thresholds) rather than REFUSE (this is the wave's real difference from prior WPW settlements — held-out measurements EXIST).
- **A4** · Campaign B novelty verdict computed mechanically vs paired Campaign-A baseline record.
- **A5** · Tier 3 eligibility MECHANICALLY evaluated + verdict recorded (**publication REMAINS BLOCKED** pending R1/R2/R3 owner rulings).
- **A6** · refused-run notebook retention path exercised if any run crashes/refuses.

---

## DATA GATE (never forget)

**t1_full_mask is admitted ONLY under `AKKI_ENV=development`** per owner ruling 2026-09-06T~12:40Z. `sandbox` and `production` remain gated. Every governed extraction crossing the chokepoint carries `tier=t1_full_mask` and is refused outside `development`. Frozen by 3 invariants (`test_row_bearing_admission_state_reflects_owner_ruling`, `test_t1_full_mask_admission_ruling_banked_verbatim`, `test_masking_tier_allowlist_admission_reflects_owner_ruling`) + the HARD-GATE regression (`test_execute_governed_lora_run_raises_on_parked_tier` uses `AKKI_ENV=sandbox` to prove t1 is still gated outside the ruled env).

---

*Authored 2026-09-06T~12:50Z from `campaign_a_baseline_ladder.json` and `campaign_b_method_ablations.json` for owner review.*
