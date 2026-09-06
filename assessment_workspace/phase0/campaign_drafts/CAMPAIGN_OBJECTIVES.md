# CAMPAIGN_OBJECTIVES · 2026-09-06 → 2026-09-09

**Banked before launch per owner ruling 2026-09-06T~12:32Z:**
> "Mapping clear objectives on the campaign starting now, runs until 9th September, 2026."

Campaign window: **2026-09-06T~12:45Z → 2026-09-09T23:59Z** (~3.5 calendar days · ~72 productive hours per host · 20 % reserved for watchdog restarts + late-run overflow).

---

## Objective 1 — CAMPAIGN A · establish the baseline record (Promise #24 shape)

**Statement.** Run sequential LoRA fine-tunes across a model-size ladder on the deduplicated `ussd_question_response` corpus so that every future single run has a *measured* reference to be judged "exceptional" against. Without banked baselines, R1 ("was the run better than nothing?") cannot mechanically settle — this campaign gives R1 its ground truth.

**Host.** `akki-vm`.

**Scope (per baseline_record):** held-out loss + perplexity + task-shaped eval + cost_actual_usd + wall_clock_s + adapter_sha256 · one record per size × seed.

**Success criteria.**
- ✔ 6 baseline_records banked (0.5 B × 2 seeds, 1.5 B × 2 seeds, 3 B × 2 seeds — the ladder rungs where 2-seed reproducibility is honestly measurable in-window).
- ✔ 1 aspirational 7 B baseline_record banked (single seed — the ladder cap; 2-seed 7 B does NOT fit the window honestly; a second seed is a follow-on when the next campaign window opens).
- ✔ Held-out slice split deterministically **BEFORE** any run starts, hash banked, referenced from every baseline_record.
- ✔ 100 % of runs auto-attach a Tier 1 notebook (invariant: `test_wpw_tier1_notebook_attached_by_open_run` already gates this).
- ✔ 100 % of runs draft + settle a Tier 2 report at completion.
- ✔ Refused-run path exercised (A6 acceptance drill) if any run crashes.

---

## Objective 2 — CAMPAIGN B · measured knowledge of which method choices matter

**Statement.** Anchor at 3 B (capability inflection — 1.5 B is undersensitive to method changes; 7 B is too expensive to replicate 6 times) and run 6 one-at-a-time ablations against a reference config. Each ablation MUST be declared as a CIF-ideation event BEFORE the run so the WPW novelty-chain (ideation → adoption → measured delta vs baseline_record) is exercised end-to-end on real material.

**Host.** `akki-vm-ii`.

**Reference config (3 B):** corpus = USSD+SMS (deduplicated) · dedup = on · LoRA rank = 16 · context length = 1024.

**6 declared ablations.**
| # | Delta from reference | Hypothesis (CIF-ideation shape) |
|---|---|---|
| B1 | corpus = **USSD-only** | Removing SMS narrows domain; expect narrower held-out gain but stronger USSD-slice performance. |
| B2 | dedup = **off** | Duplicate-heavy corpus overfits to repeated prompts; expect worse held-out generalisation. |
| B3 | LoRA rank = **8** | Lower capacity underfits; expect degraded held-out vs reference. |
| B4 | LoRA rank = **32** | Higher capacity risks overfitting on this corpus size; expect diminishing returns or regression. |
| B5 | context length = **512** | Truncated context loses tail examples; expect degraded evaluation on long-response tasks. |
| B6 | context length = **2048** | Extended context increases per-step cost; expect marginal held-out gain at wall-clock premium. |

**Success criteria.**
- ✔ 1 reference run + 6 ablation runs = 7 runs banked with baseline_record shape.
- ✔ Each ablation's Tier 1 notebook opens with the CIF-ideation event (hypothesis + expected direction) written BEFORE the run starts.
- ✔ Tier 2 report at each settlement measures the delta vs Campaign-A 3 B baseline record.
- ✔ Every measured delta feeds a Tier 3 eligibility verdict (see Objective 3).

---

## Objective 3 — WIZARD LOGIC EXERCISED on real runs

**Statement (owner ruling verbatim):**
> "test the wizard logic(s) here."
> "every campaign run must (i) auto-attach Tier 1 notebook and capture live events (checkpoints, anomalies, cost checkpoints), (ii) draft a Tier 2 report at settlement that can SETTLE — held-out measurements exist this time, so acceptance criteria measure rather than refuse, (iii) evaluate Tier 3 eligibility MECHANICALLY and record the verdict (eligible/not + why) with publication still blocked pending R1/R2/R3 — that tests the eligibility gates without violating the block."

**Success criteria (A1–A6 acceptance drill mapping):**
- **A1 (attach)** — every run has `is_attached_to_run(run_id) == True` at first heartbeat.
- **A2 (event capture)** — every run's `notebook.jsonl` carries ≥1 WPW-1..WPW-7 event per {checkpoint, anomaly, cost-checkpoint} phase.
- **A3 (settlement)** — every completed run drafts a Tier 2 report whose acceptance criteria MEASURE (held-out loss / perplexity thresholds) rather than REFUSE — this is the wave's real difference from prior WPW settlements.
- **A4 (novelty verdict)** — each Campaign-B ablation's Tier 2 report carries a `novelty_verdict` field (better / worse / no-signal) computed mechanically vs the paired Campaign-A baseline record.
- **A5 (Tier 3 eligibility)** — each settled Tier 2 evaluates Tier 3 publication eligibility MECHANICALLY (measured-delta ≥ threshold + settlement-cost-under-cap + reproducibility-across-seeds). **Verdict is RECORDED, publication REMAINS BLOCKED** pending R1/R2/R3 owner rulings. Frozen by: existing WPW-v1-e-design invariants + `test_tier3_eligibility_verdict_recorded_but_publication_blocked` (chartered).
- **A6 (refused-run notebook retention)** — if any run crashes / refuses, its notebook.jsonl + reflection_records / model_admission_records / commissioning_records survive the failure (zero-influence extension pattern already frozen for the row_executor receipt path).

---

## End-of-window deliverables (by 2026-09-09T23:59Z)

1. **7 baseline_records** on akki-vm (Objective 1).
2. **6 ablation baseline_records** + **1 reference** on akki-vm-ii (Objective 2).
3. **All 13 runs** carry the wizard A1–A6 evidence (Objective 3).
4. Refused-run record retention path exercised if any failures occurred.
5. `phase0/campaign_reports/CAMPAIGN_A_SUMMARY.md` and `..._B_SUMMARY.md` authored, listing every run's baseline_record + Tier 2 settlement + Tier 3 verdict.
6. Ratchet stays monotonic-up through the campaign window (no BASELINE_GUARD regression).

**Reference to every run in the manifests**: each entry in `campaign_a_baseline_ladder.json` names `objective_ref: "Objective 1 · Campaign A"` and each entry in `campaign_b_method_ablations.json` names `objective_ref: "Objective 2 · Campaign B"` + the specific ablation ID (B1..B6). Objective 3 is covered by construction (via the auto-attach + settle + eligibility-verdict wiring that fires on every run).

---

*Authored 2026-09-06T~12:45Z pre-launch as the objectives-mapping banked artefact per owner's third ruling.*
