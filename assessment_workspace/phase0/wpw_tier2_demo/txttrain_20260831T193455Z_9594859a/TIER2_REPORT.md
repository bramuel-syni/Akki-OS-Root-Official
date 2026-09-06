# Tier 2 Technical Report · txttrain_20260831T193455Z_9594859a

[INTERNAL · Tier 2 · MUST NOT cross the outer gate — WPW-10]

**Settlement:** refused  · **Spec:** whitepaper_wizard_spec_v1 · WPW-8..10.

## 1 · Problem & Objective

Objective: shape a small LoRA adapter on top of Qwen/Qwen2.5-0.5B, the multilingual 500M-parameter causal LM, to summarise/triage USSD question-response text from the DigiCow shortcode question path.

Problem: no adopted text adapter yet exists on the seat for USSD question triage. Baseline is the un-adapted Qwen 0.5B checkpoint (Promise #24 auto-minted at run open).

## 2 · Data Statement (classification-driven)

Source: `digicow_live.ussd_question_response`  · rows extracted: **30000**  · dropped empty QA: 4648

**Included columns (governed as text):** option_string, question_string, value_chain.

**Excluded columns (classification-driven refusal):** id, ussd_user_id, mobile_number, training_code, post_id, question_id, option_id, created_at, number_of_animals, forage_area.

**Scrub pass replacements:** id=0, phone=0.

Output corpus sha256 (shape-only receipt): `484a174cdbec4927fd21228b4fbca42a8f5265a431061fae114374df223fdcc8`.

## 3 · Baseline Record (Promise #24)

Baseline line id: `bl_txttrain_20260831T193455Z_9594859a`  · starting model: `Qwen/Qwen2.5-0.5B`.

Licence note: Apache-2.0 (verified from HF model card at extract time).

Authored at 2026-08-31T19:34:55Z by `training_runner.open_run` (Promise #24 auto-mint at run open).

## 4 · Method (including adopted ideation events)

Method: LoRA/PEFT fine-tune per the adopted recipe on the Promise #24 baseline.

**Adopted ideation events:** _the record is silent — no cif_ideation events with adoption_status='adopted' appear in the run notebook._

## 5 · Setup & Reproducibility

**Hardware:** NVIDIA H200 #0, NVIDIA H200 #1.

**Duration:** 2163.99 s (~36 min)  · **epochs:** 3  · **effective batch:** 64  · **n_gpu:** 2  · **base model:** `Qwen/Qwen2.5-0.5B`  · **adapter sha256:** `a369304911566bbac263a0b3552f239289472c98663119d0243e11e7862f8468`.

**Cost actual vs estimate:** $0.00 actual / $0.00 estimate (0 % of estimate).

**Seed:** _not applicable / the record is silent._

## 6 · Results on held-out material

| Criterion | Measured | Threshold | Pass? |
|---|---:|---:|---|
| `held_out_accuracy` | None | 0.75 | ❌ |
| `abstention_calibration` | None | 0.85 | ❌ |
| `cost_actual_vs_estimate` | 1.0 | 1.1 | ✅ |
| `latency_p95_ms` | None | 250 | ❌ |
| `refusal_rate_on_out_of_domain` | None | 0.6 | ❌ |
| `adapter_size_mib` | 8.4 | 32 | ✅ |

## 7 · Ablations

_No ablations run for this settlement._

## 8 · Limitations

_the record is silent on limitations._

## 9 · Negative Results

**Run refused.** MOAC 4-of-6 criteria HONEST-EMPTY (no held-out slice, no abstention head, no served seat, no OOD eval). Only 2 criteria measured cleanly (cost_actual_vs_estimate and adapter_size_mib). Per §5 evidence grammar, this run must NOT claim acceptance without the missing measurements. Banked as an honest-refused settlement — the adapter is real but its held-out virtue is not.

## Figures (WPW-9)

| # | evidence_class | receipt_line | summary |
|---|---|---|---|
| 1 · `corpus_shape` | measured | `extract_summary.json` | 30000 rows · included=['option_string', 'question_string', 'value_chain'] · excluded=['id', 'ussd_user_id', 'mobile_number', 'training_code', 'post_id', 'question_id', 'option_id', 'created_at', 'number_of_animals', 'forage_area'] · scrub={'id': 0, 'phone': 0} |
| 2 · `baseline_line` | measured | `baseline_line.json` | baseline=bl_txttrain_20260831T193455Z_9594859a · model=Qwen/Qwen2.5-0.5B |
| 3 · `hardware_fingerprint` | measured | `nvidia_smi_before.json` | gpus=2: NVIDIA H200 #0, NVIDIA H200 #1 |
| 4 · `wall_clock_and_flops` | measured | `train_summary_raw.json` | duration=2163.99 s (~36 min) · flops=3.721898999808e+16 |
| 5 · `acceptance_criteria` | measured | `state.json` | 6 acceptance criteria · pass=2/6 |

[INTERNAL · Tier 2 · MUST NOT cross the outer gate — WPW-10]