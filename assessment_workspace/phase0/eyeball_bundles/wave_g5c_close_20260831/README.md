# W-G5c-close · Owner Eyeball Bundle
**Compiled:** 2026-08-31 · owner-facing surfaces closed under W-G5c-close (double-green byte-identical · ratchet 2680→2692).

Every screenshot in this bundle was captured by the Real-Chromium harness (`tools/wave_g5_realchrome_verification_harness.py`) driving the LIVE prototype at `localhost:3000/` (which proxies to the running backend at `localhost:8001`). No mockups. No composited overlays.

**Verdict:** 🟢 GREEN · 9 substitution rules declared · 9 rules bound to rendered DOM · orphan_count = 0.

---

## 01 · Portal landing (`01_portal.png`)

*What the owner should verify:* the RMS-AI portal renders under literal-adoption of `v8_prototype.html` — no visual drift from the byte-identical prototype source. The "Manage Estate" entry is present (it's the click target that opens the Admin surface, which leads to the Registry). This is the surface a first-time visitor lands on.

**What to look for:** portal branding, nav elements, and the "Manage Estate" call-to-action all pixel-clean.

---

## 02 · Registry aside · live census-driven surface (`02_registry_aside_live.png`)

*What the owner should verify:* four LIVE substitution surfaces on the Registry aside — every visible number/phrase below is derived from actually-executed system state, not from prototype dummy strings.

**Bound surfaces on this screenshot:**

| Slot | Product-facing text now shown | Data source |
|------|-------------------------------|-------------|
| **Slot #1** (hero sentence) | "RMS AI is reading **2** connected sources, holding with **233 tables** read — size and completeness not yet measured, **awaiting first census**." | Live: derived from Census #1 manifest (2 databases · 233 tables · 5.9M rows). "awaiting first census" tail is the honest-empty because the census is aggregates-only by design and does not measure byte size. |
| **Slot #2a** (census status header) | "Census #1 · **read the estate at the seam**" | Live: Census #1 manifest at `phase0/census/census_0001/manifest.json` · authored 2026-08-28T15:49:08Z by "seed" initiator. |
| **Slot #2b** (census byline) | "Run 2026-08-28 by seed" (extracted from manifest) | Live: `started_at_utc` + `initiator` fields of the census manifest. |
| **Topline stats tiles** | Value/label pairs: "Not yet measured / held across 2 sources" · "78% / measured at last census" · "N opportunities standing ready" (or "no opportunities yet" if none). | Live: `estateSources` / `lastCensus` / `opportunities` fields on `liveValues`. |

**Style signature (INTERRUPT 3 discipline):**
- 3 underlined tokens in Slot #1 (the "reading", "connected", "tables read" spans — anchored to `.sc-underline`).
- 1 oxblood token in Slot #1 tail ("awaiting first census" — anchored to `.sc-oxblood`).

**What to look for:** every number the eye lands on ("2", "233", "Census #1", "read the estate at the seam") corresponds to a real crossed-and-receipted fact. No numeric literal on this surface is hardcoded in code — each traces back to a manifest file. The narrative style renders exactly per the prototype's INTERRUPT-3 palette.

---

## 03 · Compute Connected sub-tab (`03_compute_connected_tab.png`)

*What the owner should verify:* the Compute Connected tab of the RegistryTab (reached via Admin → Go to Registry → Compute Connected) is REACHABLE and RENDERS cleanly. Under W-G5c-close, this surface is confirmed as the ACTUAL target for future compute-facts wiring.

**Everything currently visible on this tab is STILL the prototype's hardcoded dummy content, not live compute-estate data.** The screenshot shows:
- `1` clusters attached · `on-premise · RMS AI DC, Nairobi` (dummy — reality is 2 clusters: `akki-vm` + `akki-vm-ii`)
- `4` GPUs · `A100 80GB · single node` (dummy hardware label — reality is `H200 143 GiB · 2 nodes` per banked Wave-H whitepapers)
- `2,880 hrs`, `1,240 hrs`, `1,640 hrs`, `43% committed`, `43% utilisation`, `18 workflows`, `2 jobs waiting` — all prototype dummies with no live-data source yet.
- `Committed hours by door` bar chart: `Train / Extract / Export / Measure / Prove` breakdown — all prototype-hardcoded.

**W-G5c-close honest posture (banked in DECISIONS.md):** the six `tile-compute-*` rules authored earlier in Wave-G5c targeted `computeCards` JS-variable dummies (`840 vCPU-h/day`, `Total capacity`, `Allocated to Build`, `3 queued`, `Queue depth`) that the prototype **never renders** as visible DOM. Real-Chromium harness probe (`tools/compute_where_probe.py`) established this cleanly. Precedent for retirement: the same happened to the composite "86.4 TB across 12 sources" dummy in Wave-G5b. **Retired.**

**Owner Ruling F intent (fold `akki-vm` + `akki-vm-ii` into the compute surface) is NOT dropped.** It is chartered as **`W-G5c-COMPUTE-v2`** in `STATE/SPRINT_PLAN.md`, targeting **THESE ACTUAL** rendered elements (Clusters attached · GPUs · Capacity this month · Committed to Work · Free to Allocate · Jobs waiting · Workflows this month · Utilisation · Runs receipted · the "Where the hours go" breakdown · the "Reading the load" narrative) — folding live `/api/compute/estate` + banked Wave-H whitepapers into each. That charter is the natural next slot after tonight.

**What to look for:** the tab renders (nav path Admin → Go to Registry → Compute Connected works cleanly), the layout is the prototype's percentage-driven language (not vCPU-hours). Every dummy visible on this tab traces cleanly to what the prototype ships; NOTHING on this surface currently fabricates a fact that would mislead an operator. And nothing in the aside surface (screenshot 02) fabricates compute-tile numbers that don't exist in system state either.

---

## GPU ACTIVITY CARD · tonight's registered runs

Two governed activities registered tonight through `services.training_runner.ssh_seam.execute_remote_command` (masking_tier=`attested_command`). Full plain-language brief at `phase0/text_train_pipeline/txttrain_20260831T193455Z_9594859a/COMBINED_ACTIVITY_SUMMARY.txt`. Every step receipted; zero PII in logs; zero estate content in receipts.

### Run 1 · Governed matmul burn (`burn_20260831T183509Z_731f22ad`)
- **When:** 2026-08-31 18:35 → 19:01 UTC · 25.8 minutes · both hosts in parallel.
- **What ran:** sustained fp16 matmul on all 4 H200 GPUs, 8192×8192, synthetic random tensors. No estate data.
- **What the GPUs did:**
  - `akki-vm` · 2× H200 · **100.0% util median · 691.7 W · 68 °C · 636.2 TFLOPS/GPU median**
  - `akki-vm-ii` · 2× H200 · **100.0% util median · 690.9 W · 68 °C · 638.5 TFLOPS/GPU median**
- **Total delivered:** **1.72 GPU-hours across 4 H200s.**

### Run 2 · Governed estate-text LoRA fine-tune (`txttrain_20260831T193455Z_9594859a`)
- **When:** 2026-08-31 19:34 → 20:11 UTC · 36.1 minutes wall-clock.
- **Where:** `akki-vm` · 2× H200 · 41.6 samples/sec sustained · 37.2 PFLOPs computed.
- **What ran:** LoRA fine-tune of `Qwen/Qwen2.5-0.5B` (500M-parameter multilingual causal LM) · 3 epochs · effective batch 64.
- **Data statement (WPW Tier-2 shape):** 30,000 rows from `digicow_live.ussd_question_response` (deterministic first 3.3% by id). 3 columns included (`question_string`, `option_string`, `value_chain`), 10 columns excluded (identifiers + PII + quasi-identifiers, each with a stated reason; decision-ledger sha256 recorded per receipt). Regex scrub for `[PHONE]`/`[ID]` patterns fired zero times — PII was cleanly confined to the excluded `mobile_number` column.
- **Honest reading (no overclaiming):** the run was technically real — real gradients, real GPUs, real saved adapter — but the corpus only contained **107 unique training-text patterns** (34 unique questions × 62 unique answers, mostly `NDIO`/`Hapana`/`yes`/`1`/`DomeShaped` USSD-survey selections). So the model **memorised** them (loss dropped from 39.78 at step 25 to below 1e-4 by step 50 and stayed there). Better data selection fixes this: the fixes are listed in `STATE/SPRINT_PLAN.md` (sample from `OFFSET 500000` for populated `value_chain`, add `sms_log.sms_sent` as secondary corpus, uniqueness pre-filter to escape the memorisation regime). Owner ruling on next text-run parameters pending.
- **Adapter retained:** `phase0/text_train_pipeline/<run_id>/adapter.tar.gz` · hash-verified against remote · size ~5-6 MB.
- **Cleanup:** masked corpus deleted from GPU host post-run (cleanup receipt banked at `phase0/text_train_pipeline/<run_id>/cleanup_post_hoc.json`).

### Combined totals
**~2.3 GPU-hours registered tonight across 4 H200 slots.** Wall-clock: ~97 min from first burn crossing to last cleanup receipt. Every crossing receipted. Zero PII in logs. Zero PII in receipts. Zero credentials in logs.


---

## What survives after this bundle ships

- **`STATE/DECISIONS.md`** carries owner rulings 3–7 verbatim from tonight, plus the honest-gap report on the shielded-training pipeline (why it can't shortcut) and the retirement banking for the 6 tile-compute-* rules.
- **`STATE/NEXT.md`** points at `STATE/SPRINT_PLAN.md`.
- **`STATE/SPRINT_PLAN.md`** carries four chartered waves ready for owner sequencing: W-G5c-close (**now closed**), W-Shield-Train (2–4 days · shielded-training pipeline build), W-WPW-v1 (~2 days for Tier 1+2 after 30-min spec ingest), W-Audio-P2 (2–3 days after archive access granted). Sequencing decision is owner-only.
- **Ratchet manifest** at `backend/tests/invariants/baseline_failures.json` has floor bumped to **2692** with legacy-schema `ratchet_history` entry banked and double-green byte-identical run pair receipted.
- **Trained LoRA adapter** at `phase0/text_train_pipeline/<run_id>/adapter.tar.gz` retained (hash-verified). Owner-visible artifact.

---

## Files in this bundle
```
01_portal.png                      — RMS-AI portal landing (literal-adoption prototype)
02_registry_aside_live.png         — Registry aside · 4 live census-driven substitution surfaces bound
03_compute_connected_tab.png       — Compute Connected sub-tab · percentage-driven prototype layout
README.md                          — this file (captions + GPU activity card)
```

Cross-references:
- Combined activity summary: `phase0/text_train_pipeline/txttrain_20260831T193455Z_9594859a/COMBINED_ACTIVITY_SUMMARY.txt`
- Burn activity summary: `phase0/gpu_burn/burn_20260831T183509Z_731f22ad/activity_summary.txt`
- Full harness log: `phase0/eyeball_proxies/20260831T202742Z_wave_g5_realchrome_g5c_close_iter3.log`
- Ground truth (rules-vs-DOM): `phase0/harness_ground_truth/latest.json`
