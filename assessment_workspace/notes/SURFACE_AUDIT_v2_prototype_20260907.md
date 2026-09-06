# Surface Audit · Prototype v2-standalone drop 2026-09-07

**Banked:** 2026-09-06T20:15Z. Delivered verbatim to owner per rulings 2026-09-06T~19:20Z ("Surface audit report here") + ~19:40Z pinging ("surfacw audit"). Precedes Registry build.

**Files under audit:**

- **NEW (binding):** `/app/assessment_workspace/canon/prototypes/20260907_v2_standalone/RMS_AI_Prototype_v2_Standalone.html` · sha256 `4199c49f2e1b3fd633683205b5274d0afaba98757a3ccb4df6f1ee9e459a71f9` · 1 954 907 bytes · 389 wrapper lines · **decoded app payload 1 776 832 bytes**.
- **PRIOR (superseded):** `/app/assessment_workspace/fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` · sha256 `e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2` · 1 262 835 bytes · 395 wrapper lines · **decoded app payload 1 109 954 bytes**.

**Delta:** +**666 878 bytes** in the app payload (v2 is 60 % larger than v8). Framework bundles (React 18.3.1 UMD, prototyping runtime) are BYTE-IDENTICAL across v2 and v8 by sha256 — all four blobs match. The delta is entirely in the inline `<x-dc>`-rooted app HTML template.

---

## STEP 1 · Structural diff summary

**Method:** decode both files' script[4] JSON-string payloads → strip scripts/styles → extract visible text + attributes + IDs. Compare `set(sentence)` for text delta; compare `set(id="…")` and `data-*` attributes for structural delta.

### 1.1 · Root shell (unchanged)

Both use `<!DOCTYPE html><html><head><script src="[uuid]"></script></head><body><x-dc><helmet>…</helmet><div style="--paper:…var(--paper);color:var(--ink)">` as the prototyping-tool root wrapper. CSS design tokens (`--paper #f5f2ea · --surface #f0ece1 · --ink #1b1f27 · --blue2 #0f1b33 · --brass #b08d2e · --sage #1d7a6e · --oxblood #b8395b · --accent #4c5fd5 · --shadow-pop 0 22px 64px rgba(15,27,51,.26) · --head Iowan Old Style,Georgia,serif · --body Söhne,Helvetica Neue,Arial,sans-serif · --mono ui-monospace,Menlo,Consolas,monospace`) are IDENTICAL between v2 and v8. **Design system unchanged.** V2 adds one token (`--gate #7c3aaf` for the Rule Book "gate" states) and one drawer-width variable (`--drawer-wide max(480px,50vw)`).

### 1.2 · dc-runtime template changes

- **Framework bundles: BYTE-IDENTICAL.** All 4 blob-uuids across v2 vs v8 sha256-match (React 18.3.1 UMD + ReactDOM + prototyping runtime + prop-types). The runtime layer is unchanged.
- **Interpolation counts:** v2 = 4 769 `{{ }}` slots · v8 = 3 101. **+1 668 slots (+53 %)** — 1 668 new data bindings the runtime must resolve.
- **Additional scoped CSS in v2 helmet:** ID-scoped scroll containers (`#reg-notes`, `#census-hist-scroll`, `#measured-scroll`, `#ef-gaps-scroll`, `.sp-scroll`, `#load-scroll`, `#mr-scroll`) with `scrollbar-width:none` — these are new virtualized/scrollable panes inside Registry. v8 had none of these.

### 1.3 · IDs added in v2 (5 new, ALL Registry)

`#reg-notes` · `#census-hist-scroll` · `#measured-scroll` · `#load-scroll` · `#mr-scroll`

**Interpretation:** v2 introduces five virtualized scroll containers inside the Registry surface. `mr` = mixed-rows or method-run; `load` = load/consumption chart pane; `measured` = the "measured vs declared" rows; `census-hist` = past-censuses list; `reg-notes` = Registry side-notes/narrative panel.

### 1.4 · Text delta (sentence-level, order-insensitive)

- **Common sentences:** 900.
- **Added in v2:** 671 (of which ~300 are new visible copy, ~371 are new `{{ }}` binding slots).
- **Removed from v8:** 217 (of which ~90 are visible copy retirements, ~127 are `{{ }}` bindings removed).

### 1.5 · Registry-section changes (v2 vs v8)

| Registry surface | v8 (before) | v2 (after) | Delta |
|---|---|---|---|
| **Data Connected** header line | "What the estate holds, as last read at the seam." | "What the estate holds, as last counted Jul 21, 2026 by J. Mwangi." | Reworded to name the census run + operator |
| **Data Connected — census** | Reference to "the seam" | Reference to census #4 + first-census date May 12, 2026 + last-count timestamp | Census-first framing |
| **Reading the mix** (data cut) | Table view (6 cuts) | Table view (6 cuts) + narrative: "Five kinds of data in seven languages, held across twelve connected sources" + drill-in to "← Back to Registry Reading the mix" full page | Full drill-in page added |
| **Sources list** | "Your data, source by source" · Source Size Rights Extracted (4 cols) | "Every connected source, grouped by the kind of data it holds" + Source Profile drill-in (`efProfileVM.*` — 15+ view-model fields incl. rightsLabel, typeLabel, qualityState, qualityReason, staleText, proof, perception, description, relationships, recommended) | Full Source Profile drill-in page added |
| **Confidential Information Register (CIR)** | ❌ ABSENT | ✅ NEW SUB-SURFACE — "Every content class the estate has declared and counter-signed, and whether a rule is actually holding it." Path breadcrumb "Shield / Rule Books / Confidential Information Register" · rows carry `sr.cls`, `sr.declaredBy`, `sr.n`, `sr.v` + "· declared by" · "Add a classification" CTA · "1 response required" tally | **New surface introduced** |
| **Census intelligence panel** | ❌ ABSENT | ✅ NEW — "What the last count found, and what it did not reach. Census run status. Next census: {{ censusNextLabel }}. Progress: {{ censusProgressLabel }}. Count: {{ censusCountLabel }}" + narrative slots (measuredPopulation, measuredMethod, measuredDeclared, mixTypeReading, mixRightsReading, mixQualityReading, mixLanguageReading, mixConditionReading, mixDuplicatesReading) | **New Registry-side narrative panel** |
| **Past censuses** | ❌ ABSENT | ✅ NEW — full drill-in page "A census is a full sweep of every connected source — there is no single-source refresh" · list of prior censuses with time/operator/duration · Census transcript view | **New drill-in surface** |
| **Estate intelligence** | Static "What you hold" ticker | ✅ NEW panel — "What stands out in the estate right now, read from the last census" · with narrative slots and "View more" drills | **New narrative panel per tab** |
| **Compute Connected header** | "How this month's committed hours divide, by whichever cut you choose" | "Reading the load — Training carries most of the month, and the reporting work is small but constant" | Rewritten with narrative default text |
| **Compute Connected — what sits on the machines** | "One cluster in Nairobi carries 2,880 hours this month — 43 % committed, with two jobs waiting" | "Four graphics cards on one cluster in Nairobi, in the same jurisdiction as your data" + 4 GPU cards enumerated with slot/state/mem/util/summary | **Per-card enumeration** |
| **Compute Connected — Usage pattern** | ❌ ABSENT | ✅ NEW — "What you've spent this month, what's left, and what's waiting on it" + budget line "Used £2,910 Left £3,890 of £6,800" + monthly spend chart with £6,800 limit line + peak annotation ("Spend peaked in July at £3,420 when the voice model was first trained") | **New budget/spend panel** |
| **Compute Connected — Consumption per workload** | ❌ ABSENT | ✅ NEW — "How the hours were used. Where the hours go, spend month by month, and who is using it." + workload cards (`wc.name`, `wc.share`, `wc.hrs`, `wc.avg`, `wc.cost`, `wc.turn`) + insight ("More than half of this month's hours went to training the voice model") | **New workload-split view** |
| **Compute Connected — per-machine drill-in** | ❌ ABSENT | ✅ NEW — per-machine detail: "This machine is free" / "Nothing on this machine needs a decision" / "One is stuck on a signature, not on capacity" · GPU card details · `gp.card`, `gp.slot`, `gp.state`, `gp.mem`, `gp.util` | **New drill-in surface** |
| **LLMs & Trained Models header** | "LLMs and trained models, on the same record — Model Origin Calls Status Share" | "The models you can call on — bought in or trained here — how much work each is doing, and what it costs" | Reworded, warmer |
| **LLMs — Model detail page** | Card-only | ✅ NEW — full "← Back to LLMs & Trained Models Models — the full record" page · 12 models grouped by state · `Twelve models, grouped by what they are doing now` · per-model: reason for group, share, calls, cost | **New full-record surface** |
| **The six checks** | Present at model-summary level ("Six acceptance checks") | Present + full drill-in explanation: **Precision on held-out set 0.85 required · Recall on held-out set 0.80 required · Calibration check 0.05 max error · Fairness slice review 0.10 max spread · Drift stability 0.75 required · Explainability sample 95 % traced** + per-check narrative: "The gap between the best and worst slice is the score" · "The minimum for each check was set at founding and has not moved" · "One failed check is enough" · "There is no partial approval and no exception path" | **Fully enumerated with narratives** |
| **Refusals** | "1,842 answers were refused this month" | Same headline + full breakdown: **"Not enough proof 811 · 44 %"** (evidence gate) · **"Not allowed to see it 663 · 36 %"** (permission gate) · "The three reasons sum to the total exactly. Nothing is reclassified after the fact" · trust-receipt reconciliation ("128 400 calls this month, 128 400 trust receipts") | **New refusal-reason enumeration** |
| **Why models refuse** | Implicit | ✅ NEW dedicated surface — "When a model cannot answer responsibly it declines rather than guesses" · gate names: Refused — permission · Refused — evidence minimum | **New concept surface** |
| **Model journal / journal thread** | Implicit "model record" | ✅ NEW — `tmJournalTitle` · `tmJournalMeta` · `tmThreadTitle` · `tmThreadStatus` · `tmThreadMeta` · `tmDetailLearnings` · `tmObjectiveText` · `tmPaperTitle` · `tmPaperObs` · `tmPaperMeta` · `tmReportLead` · `tmReportObs` · `tmSumName` · `tmSumRecap` — 15+ view-model fields for a per-model journal/thread | **New model-journal drill-in** |
| **Model intelligence panel** | ❌ ABSENT | ✅ NEW — `modelAsideEyebrow` / `modelAsideHeadline` / `llmBlurb` / `llmChartReading` / `llmCardsLabel` / `llmRailHead` — narrative aside for LLMs & Trained Models tab | **New tab-narrative panel** |
| **Compute intelligence panel** | ❌ ABSENT | ✅ NEW — `computeGraphsLabel` / `gpuBlurb` / `gpuCardsLabel` narrative aside | **New tab-narrative panel** |
| **Opportunities (in-tab)** | Implicit "Five more opportunities sit on the sources" | ✅ EXPANDED — "Opportunities recommended for this source" + "Standing across the estate" · Estimated cost · GPU hours · "What your data can do — Six things could be built from what is already verified. Four are ready today" | **Per-source Opportunities drill-in** |
| **Master version history** | ❌ ABSENT | ✅ NEW — "MASTER VERSION HISTORY No matches" placeholder + populated view with `mrDetailVM.*` (17 fields incl. custodyPath, custodyRef, custodyWhen, receipt, receiptNote, tier, tierNote, trendNote, trendRange, provTitle, licence, insight, statusLabel, admBadge, code, name, origin, what, bannerText) | **New history surface** |

### 1.6 · Non-Registry surface deltas (v2 vs v8)

**Added:**
- **Rules Updates** (NEW) — "A classification still waiting for a signature is not here — it sits in Rules Updates until it is signed" · signing queue with countdown · referenced from Confidential Information Register.
- **Rule Book Library** (expanded) — "Currently Running" / "Open Rule Book Library (Not yet adopted)" / "All Rule Books — adopted and yet to be adopted library" · standard rulebooks shelf · ISO 27001 mapping / adopted flag per row · "Rulebook shelf intelligence — Tracks what the shelf is missing and which standard rulebooks are worth bringing in next".
- **Workflow / job detail** (NEW class of surface) — `wfDetailVM.*` (18 fields incl. name, statusLine, metaLine, backLabel, actionLabel, actionNote, ceilingLine, costLine, queueEta, queuePos, progressLabel, receipt, receiptNote, producedText, trackHead, trackBody, narrativeTitle, pillLabel, bannerText, what) + workflow list (`wfAttCount`, `wfDoneCount`, `wfSaveCount`, `wfMonth`, `wfNoteFix`, `wfNoteSlack`, `wfCardBarReading`, `wfCardReading`, `wfConsumeReading`, `wfStateReading`).
- **Watch — headline mentions** (deepened) — "Watch — Branch Interaction Logs read with problems and nothing verified; extraction has not started" · "Watch — evidence-gate hedges rose to 136 this month, the highest since founding" · "Watch — the Model Training Data Rulebook is only partly in force, carried by a single training rule".
- **Approval history** (NEW) — approval-history surface implied by "Approval history" heading + Rule signing sequences ("How rules change: Someone proposes it, a second person signs off, a countdown runs in the open, then it applies and is re-checked").
- **Preview outcomes (review only)** modal — `× Preview outcomes (review only)` — new pre-adoption review pattern.
- **Rulebook shelf intelligence** — the "shelf" is the standard-rulebook catalog with adopted/not-yet-adopted state.

**Removed / retired from v8:**
- **"Buy Data" catalog** — external data purchase surface (7 sentences retired, e.g., "Cancel Confirm purchase", "Nothing is delivered until you confirm", "Quote, confirm, receive the file — every purchase receipted", "Committed hours are quoted per commission").
- **"Ask The Indices"** as separate top-level surface — the Indices card with "Published on a fixed cadence" · "Every index and every answer, programmatically — scoped to your terms" · "· in your Documents API" — retired; index concept folded into other surfaces.
- **"How I compare · Free · Opt-in"** — the farmer/herd comparison scenario ("Your AI success rate is above the Nakuru average this quarter (61 % vs 54 %)" · "Your last vaccination record is 2 weeks fresher than most herds near you" · "Withdraw any time" · "THIS QUARTER, BY SMS RMS AI · today 09:14 Habari Jane" · "Reply STOP to opt out") — dropped. **This retires the farmer-benchmark demo entirely from the design.**
- **"Deployed — open directly"** app-catalog surface with `da.mark`, `da.name` — the app-tile grid on landing.
- **"Coast region — outside your licensed coverage — Ask for a quote"** — regional-quote flow.
- **"Six acceptance checks" as a top-level nav item** — the checks are now shown ONLY inside the LLMs & Trained Models tab / model detail, not standalone.
- **"FI Farma IQ"** brand slot on landing — retired.

### 1.7 · dc-runtime nav surface

Neither prototype uses explicit HTML nav elements (no `<nav>`, no `data-nav`, no `setView(...)` handlers exposed in the flat text). Navigation is JS-driven inside the runtime bundle (35 KB minified in blob `865daeb9` — this blob is IDENTICAL between v2 and v8). Menu labels + section-switch state are held in the runtime; the template exposes them via `{{ }}` interpolations (`landingGroupLabel`, `landingAppName`, `landingGreeting`, `landingCtaLabel`, `landingGlimpseLabel`, `landingGlimpseTime`, `nv.label`, `vw.label`).

**Literal-adoption law:** the current pod-shell iframe portal walks the RENDERED DOM (post-runtime) and substitutes prototype-sample values with `/api/*` facts, cited by CSS selector — not by DOM structure prediction. That contract is unchanged by v2. The v2 rendered DOM has more nodes and more `{{ }}` slots, so substitution rules will need to be re-authored against v2's rendered output, and rules matching nothing must fail RED per the rendered-DOM law banked in prior rulings.

---

## STEP 2 · Surface audit table

**Legend for column 3 ("current live state"):**
- **LIVE-DATA** — the surface is rendered by the current pod-shell iframe portal AND at least one figure/list on it is hydrated from a real `/api/*` route (substitution applied against a durable record).
- **PROTOTYPE-SAMPLE** — the surface renders because the portal iframe shows the v8 HTML, but the values are the prototyping-tool sample text, not backed by any `/api/*` call.
- **NOT-WIRED** — the surface is defined in the v2 HTML but does not exist in the currently-loaded v8 HTML, or is present in v8 but the portal never routes to it.

**Portal note:** the current pod-shell renders **one iframe** rooted at `/v8_prototype.html` (verified at `App.js:1056 · data-testid="v8-prototype-iframe"`); all "surfaces" are DOM regions inside that single iframe reached via the runtime's own routing. There are no React routes to sub-surfaces — the 15 legacy deep-links (Registry.jsx, Watch.jsx, etc.) are retained in `pod_shell/frontend/src/components/` but not routed (App.js §"All paths (root + wildcard) render <PortalIframe/>. The 15 legacy deep-link routes are retired").

### 2.1 · Registry (priority build target — maximum detail)

| # | Surface | What the design shows | Current live state | What full build requires |
|---|---|---|---|---|
| **R.0** | Registry — entry page | Two-column: left (topline + visual + table rows) fluid, right 300 px (headliner + context panels). Title deck names the estate, the last-count and its operator. Tab bar: Data Connected / Compute Connected / LLMs & Trained Models. | **LIVE-DATA** — portal swaps v2 for v8 iframe; runtime routes to Registry surface; `/api/registry/facts` hydrates topline figures (86.4 TB, 12 sources, 78 % measured, 6 opportunities). | Portal swap: point iframe at `/v2_prototype.html`. Re-author substitution rules against v2 rendered DOM. Registry-topline substitutions already have a live route (`/api/registry/facts`); binding needs to walk to the new v2 anchor elements. |
| **R.1** | Data Connected · header topline | "What the estate holds, as last counted Jul 21, 2026 by J. Mwangi." + total-TB + total-sources tile. | LIVE-DATA (existing figure bindings) | Re-anchor substitutions against v2's new element positions. Add `census-#` and `census-operator` fields to `/api/registry/facts` payload (currently ships `last_verified` timestamp, not census-id/operator name). |
| **R.2** | Data Connected · Reading the mix (6-way cut) | Six cuts of the 86.4 TB: type, rights, language, condition, duplicates, quality. Each with narrative reading ("Five kinds of data in seven languages, held across twelve connected sources"). | PROTOTYPE-SAMPLE (v8 has same 6 cuts, but only the total-TB is substituted from live data; individual cut breakdowns are prototype samples). | Backend: extend `/api/registry/facts` (or new `/api/registry/mix`) to return cut breakdowns keyed by (type / rights / lang / condition / duplicates / quality). Read from census output (`services/census_engine/`) at census-close. Substitutions bind cuts to `mixTypeReading` / `mixRightsReading` / `mixLanguageReading` etc. |
| **R.3** | Data Connected · Sources list (grouped by kind) | Every connected source, grouped by data-kind. Per-source row: name, size, records, PII, quality, rule coverage. | PROTOTYPE-SAMPLE (the v8 version had a flat sources list — v2's grouped view is new). | Backend: `/api/registry/facts` already returns sources array; need to group by `kind` (customer-service-calls, complaints-docs, branch-logs, etc.) in payload OR let frontend group. |
| **R.4** | Data Connected · Source Profile (drill-in) | Full page per source: header (name, type, rights), quality state, description, perception (what it's for), proof (how measured), relationships (related sources), recommended (opportunities on this source), staleness pill. 15+ view-model fields (`efProfileVM.*`). | NOT-WIRED (drill-in did not exist in v8; no route today). | **New backend: `GET /api/registry/source/{source_id}/profile`** — returns the 15 `efProfileVM.*` fields. Reads from `services/registry_facts/` + `services/perception/` (perception service is BUILT-UNMOUNTED per TRUE_STATE — needs mounting first). |
| **R.5** | Data Connected · Confidential Information Register (NEW) | "Shield / Rule Books / Confidential Information Register — Every content class the estate has declared and counter-signed, and whether a rule is actually holding it." Rows: classification, declared-by (person), row-count, tally-line. "1 response required" pending-signature tally. "+ Add a classification" CTA. Opens Rules Updates on click. | NOT-WIRED (surface did not exist in v8). | **New backend: `GET /api/registry/cir`** — returns classification rows + pending-signature count. Cross-service: reads `services/governance/` (rule adoption) + a new "declared classes" store. `services/rights_quarantine/` may already cover the "declared with rule holding" concept — audit that first. **Depends on Rules Updates surface (Q.1 below) since CIR is the entry point to Rules Updates.** |
| **R.6** | Data Connected · Census intelligence panel (right rail) | "What the last count found, and what it did not reach. Census run status. Next census: {{ censusNextLabel }}. Progress: {{ censusProgressLabel }}. Count: {{ censusCountLabel }}." Narrative slots for what census measured vs what it did not reach. | PROTOTYPE-SAMPLE (census route exists — `/api/census/latest` — but the narrative slots are not populated). | Extend `/api/census/latest` (or add `/api/census/status`) to return: `next_scheduled_utc`, `progress_pct`, `count_label`, `not_reached_bytes`, and narrative-ready phrases. `services/census_engine/` owns the source of truth. |
| **R.7** | Data Connected · Past censuses (drill-in) | "A census is a full sweep of every connected source — there is no single-source refresh." List of prior censuses with time / operator / duration. Census transcript view per row. | NOT-WIRED (v8 didn't have a past-censuses drill). | **New backend: `GET /api/census/history`** returning list; `GET /api/census/{census_id}/transcript` returning per-run transcript. Reads census-engine output history. |
| **R.8** | Data Connected · "How the estate is measured" (methodology page) | "Four principles are not view-specific" — declared, measured, method, population. Explains what "population" and "method" mean at census time. | NOT-WIRED (methodology page is new). | **Frontend-only page** — no backend route; static explainer bound to `measuredDeclared`, `measuredMethod`, `measuredPopulation` labels (may be constants). Bank the four principles as canon-fixed strings. |
| **R.9** | Data Connected · Estate intelligence (right-rail insight) | "What stands out in the estate right now, read from the last census." Narrative + "View more →" drill. | PROTOTYPE-SAMPLE | Extend `/api/registry/facts` to include an `estate_intelligence` narrative object (top-N standout facts computed from census + rights + quality signals). |
| **R.10** | Compute Connected · header topline | "Reading the load. Training carries most of the month, and the reporting work is small but constant." | LIVE-DATA (existing `/api/compute/estate` substitution) | Re-anchor against v2. |
| **R.11** | Compute Connected · What sits on the machines (per-card enumeration) | 4 GPU cards, one cluster in Nairobi. Per card: card model, slot, state (Free / Busy / Waiting-on-signature), memory used/total, util %, one-line summary. | LIVE-DATA (partial) — `/api/compute/estate` returns cluster facts; per-card enumeration exists but state labels are prototype text. | Extend `/api/compute/estate` payload to per-GPU: `state ∈ {free, busy, waiting_on_signature, degraded}`, `slot_id`, `mem_used_gb`, `mem_total_gb`, `util_pct`, `summary_line`. Reads from `services/compute_estate/` + nvidia-smi ingestion + `services/compute_seam/`. Cross-lane awareness: needs to bind the two campaigns (A on akki-vm · B on akki-vm-ii) as "workflows" occupying slots. |
| **R.12** | Compute Connected · Usage pattern & budget | "What you've spent this month, what's left, and what's waiting on it." Budget line: "Used £2 910 · Left £3 890 of £6 800". Monthly spend chart with limit ceiling. Peak-month annotation. | NOT-WIRED (v8 didn't have budget/spend). | **New backend: `GET /api/compute/spend`** returning per-month spend, current-month split (used/left/limit), peak annotation. `services/cost_ledger/` is LIVE-mounted and likely holds the raw ledger — needs a spend-rollup endpoint. |
| **R.13** | Compute Connected · Consumption per workload | "Where the hours go, spend month by month, and who is using it." Workload cards: name, share of hours, hours-used, avg-turn-time, cost, per-workload insight ("More than half of this month's hours went to training the voice model"). | NOT-WIRED (v8 didn't have per-workload split). | **New backend: `GET /api/compute/workloads`** — reads cost_ledger + training receipts (`phase0/shield_train_receipts/`) + campaign records to group hours by workload class (training, extraction, evidence-gate, chat, etc.). |
| **R.14** | Compute Connected · Reading the traffic (calls & spend) | "Where this month's calls and spend landed" · by-cut view. Two-panel chart: calls · spend. Insight line + `trafficVM.*`. | NOT-WIRED | **New backend: `GET /api/compute/traffic`** returning per-cut calls+spend arrays and computed insight. Reads chat-history/trace router + cost_ledger. |
| **R.15** | Compute Connected · Per-machine drill-in | Per-machine detail page: "This machine is free" / "Nothing on this machine needs a decision" / "One is stuck on a signature, not on capacity". GPU-card fields (`gp.card`, `gp.slot`, `gp.state`, `gp.mem`, `gp.util`, `gp.summary`). | PROTOTYPE-SAMPLE (partial) — `/api/compute/reflection` POST + `/api/compute/commit` POST exist for the ackward flow but the read-only per-machine page is not built. | Add `GET /api/compute/machine/{machine_id}` returning per-machine dashboard (all GPU cards on that machine, running workflows, waiting-on-signature list). |
| **R.16** | Compute Connected · Compute intelligence (right-rail) | Aside narrative — `computeGraphsLabel` / `gpuBlurb` / `gpuCardsLabel`. | NOT-WIRED | Add narrative field to `/api/compute/estate` payload; frontend renders. |
| **R.17** | LLMs & Trained Models · header topline | "The models you can call on — bought in or trained here — how much work each is doing, and what it costs." | LIVE-DATA (partial) — 4 MOAC services live (`model_registry`, `model_admission`, `baseline_line`, `model_recheck`). | `/api/model_registry/*` returns model list; needs joining to `services/cost_ledger/` for the "how much work · what it costs" figures per model. |
| **R.18** | LLMs · Model roster | Grid of models with per-model: name, origin (bought / trained), state (in service / under evaluation / retired), calls, share of traffic, tier badge. "One model is under evaluation The reasoning model has passed four of six checks." | PROTOTYPE-SAMPLE | Extend model_registry payload to include `state`, `calls_this_month`, `share_pct`, `tier`, `checks_passed_of_six`. |
| **R.19** | LLMs · "Models — the full record" (drill-in page) | "← Back to LLMs & Trained Models Models — the full record" · 12 models grouped by state · per-model reason line, share, calls, cost. | NOT-WIRED | **New backend: `GET /api/model_registry/full_record`** — all models with grouping key + reason lines. |
| **R.20** | LLMs · Model detail — "How this model answers" | Explains the two answering modes for a model: memory (stored answer) vs worked-out-fresh. "This month 76 400 answers came from memory and 52 000 were worked out fresh." Memory-carrying stats. | NOT-WIRED | **New backend: `GET /api/model_registry/{model_id}/answering`** — reads `services/memory/` (LIVE-mounted, 1 429 LOC) + chat-service call counts for split. |
| **R.21** | LLMs · Model detail — The six checks | Full enumeration with thresholds: Precision 0.85 · Recall 0.80 · Calibration 0.05 max error · Fairness slice 0.10 max spread · Drift stability 0.75 · Explainability sample 95 % traced. Each with a plain-English rationale sentence. Six-check status pass/fail per model. | LIVE-DATA (partial) — `services/model_admission/` (342 LOC) + `services/model_recheck/` (126 LOC) run the check machinery; UI shows `ModelEcosystem.jsx` today with the four-service model. | Extend admission/recheck outputs to bind six-check per-model into a normalized JSON. `GET /api/model_registry/{model_id}/checks` returning the six values + pass/fail + minimum-thresholds (owner-set at founding, "has not moved" per canon). |
| **R.22** | LLMs · Model detail — Refusals | Refusal totals with reason enumeration: "Not enough proof 811 · 44 %" (evidence gate) + "Not allowed to see it 663 · 36 %" (permission gate) + third gate. Trust-receipt reconciliation ("128 400 calls this month, 128 400 trust receipts"). | LIVE-DATA (partial) — `services/audit_trail/` (298 LOC, mounted) holds trust receipts; `services/rights_quarantine/` + `services/lowered_standard/` know refusal reasons. | **New endpoint: `GET /api/model_registry/{model_id}/refusals`** joining audit_trail (call+receipt count) + rights_quarantine (permission refusals) + evidence-floor refusals from shield. |
| **R.23** | LLMs · Model detail — Why models refuse | Concept explainer: three refusal gates (permission / evidence / entitlement) with narrative for each. | NOT-WIRED (concept page is new) | Static explainer page — bank the three gate names and rationales as canon-fixed strings. No new backend route. |
| **R.24** | LLMs · Model detail — Model journal | Per-model journal/thread with title, meta, status, learnings, objectives, paper title, paper observations, report lead, summaries (15+ `tm*` fields). | NOT-WIRED | **New backend: `GET /api/model_registry/{model_id}/journal`** — reads `services/training/` (1 568 LOC, LIVE-mounted) run history + `services/whitepapers/` (150 LOC) + `services/wpw/` (923 LOC, invariant-frozen) whitepaper output. Cross-service join between training-run receipts (`phase0/shield_train_receipts/`) and model_registry entries. |
| **R.25** | LLMs · Model detail — Traffic breakdown | "Where the calls go, by origin" — traffic split for THIS model. `trafficVM.ansTitle`, `trafficVM.barsNote`, `trafficVM.insight`, `trafficVM.reasonTotal`, `trafficVM.trendRange`, `trafficVM.trendTitle`. | NOT-WIRED | `GET /api/model_registry/{model_id}/traffic` — same shape as R.14 but scoped to model. |
| **R.26** | LLMs · Model intelligence (right-rail) | Aside narrative for the tab. | NOT-WIRED | Add narrative field to model_registry payload. |
| **R.27** | LLMs · Opportunities recommended (per-source, in Registry context) | "Six things could be built from what is already verified. Four are ready today. Two are the larger kind, suited to training a model; two are smaller and handle everyday reading and extraction." Ties back to sources. | NOT-WIRED (Opportunities exists as a service — `services/opportunity_briefs/` — but is UNMOUNTED per grep; not surfaced today). | Mount `opportunity_briefs.router` at `/api/opportunity_briefs/*`. Extend Registry.jsx (or the new portal substitution) to bind opportunity cards to per-source and per-tab context. |
| **R.28** | Cross-tab · "Preview outcomes (review only)" modal | Pre-adoption review overlay — a preview drawer that opens over any of the three Registry tabs. | NOT-WIRED | Frontend-only modal — no new backend route unless the "preview" pulls a projection (e.g. "if this rulebook were adopted, what changes on this Registry surface?") — that would need a `/api/governance/preview` route. |

**Registry sub-total: 29 rows.** LIVE-DATA (partial or full): 5 · PROTOTYPE-SAMPLE: 7 · NOT-WIRED: 17.

**Rendered-DOM law risk in Registry:** 17 NOT-WIRED surfaces means 17 substitution-rule authorships to add against v2's rendered DOM. Each rule that matches no element = RED. Real-Chromium harness must be re-run against v2 to enumerate the anchor selectors before rules are authored (per rendered-DOM law banked in prior rulings).

### 2.2 · Non-Registry surfaces the new v2 HTML defines

| # | Surface | What the design shows | Current live state | What full build requires |
|---|---|---|---|---|
| **L.1** | Landing — "Habari, {{ rolePerson }}" | Greeting + role person / dept / initials + tile grid of what's available. | PROTOTYPE-SAMPLE | Substitutions bind `rolePerson`, `roleDept`, `roleInitials` to the pod's auth-service user identity. `services/auth/` (1 714 LOC) supplies. |
| **C.1** | Chat — "Ask & Remember" | Chat surface with memory carry, cited answers, trust receipt per call. Archive / delete flows. | LIVE-DATA — `/api/chat/*` (mounted `chat_router`) + `services/memory/` (LIVE-mounted). | Existing routes cover; re-anchor substitutions. |
| **W.1** | Watch | Watch surface for metric monitoring + Grey Mirror + Watch alerts. | LIVE-DATA — `/api/watch/*` + `/api/grey_mirror/*` mounted. Substitutions bind. | Existing routes cover; new v2 phrases ("Watch — Branch Interaction Logs read with problems") need matching Watch service phrasing endpoint. |
| **L.2** | Ledger (Audit Trail) | Every call → trust receipt. Receipt count = call count. | LIVE-DATA — `/api/audit_trail/*` mounted. | Existing route covers. |
| **G.1** | Rule Book Library | "All Rule Books — adopted and yet to be adopted library" · Currently Running · Open Rule Book Library (Not yet adopted) · shelf with ISO 27001 mapping per row. | PROTOTYPE-SAMPLE — `services/governance/` (129 LOC, mounted) + `routers/govern` (mounted) cover the write side; read-side shelf enumeration is thin. | **New endpoint: `GET /api/governance/rulebooks`** returning the shelf (adopted + not-yet-adopted) with per-rulebook ISO 27001 mapping. Extend `governance/` service to hold the shelf catalog. |
| **G.2** | Rule Book — full detail | Every rule in the book, grouped by category. Rule profile: what promise it holds up + what it changes. | LIVE-DATA (partial) — governance service returns rules. | Extend `/api/governance/rulebook/{id}` to include per-rule profile fields (`what_promise_upheld`, `what_it_changes`). |
| **G.3** | Rulebook shelf intelligence (right-rail) | "Tracks what the shelf is missing and which standard rulebooks are worth bringing in next." | NOT-WIRED | Backend: shelf-gap analysis endpoint. Reads adopted rulebooks + a canon-fixed reference-shelf (ISO 27001 etc.) + compares. |
| **Q.1** | Rules Updates (NEW) | Signing queue with countdown. "A classification still waiting for a signature is not here — it sits in Rules Updates until it is signed." "Adopting a rulebook and changing a single rule move through the same ceremony." | NOT-WIRED | **New backend: `GET /api/governance/rules_updates`** returning pending-signature queue + per-item countdown + proposer + first-signer + status. **New POST: `/api/governance/rules_updates/{id}/sign`** for the second signer. Reads/writes `services/governance/` — needs a "pending signatures" data model added. |
| **Q.2** | Approval history | Approval-history log surface. "How rules change: proposal → sign-off → countdown → apply → re-check." | NOT-WIRED | Backend: `/api/governance/approvals` returning history. Reads `services/audit_trail/` (already captures approvals) + `services/governance/`. |
| **WF.1** | Workflow list | Grid of workflows/jobs with month header, done-count, save-count, note lines, per-card readings, consumption reading, state reading. | PROTOTYPE-SAMPLE | Cross-service. Reads `services/training/` runs + `phase0/shield_train_receipts/` + `services/campaign_infra/`. New endpoint: `GET /api/workflows` returning grouped workflow list. |
| **WF.2** | Workflow detail | Per-workflow detail: status line, meta, cost, GPU hours, ceiling, action label / note, banner text, queue position + ETA, progress, receipt, receipt note, produced text, track head + body, narrative title, pill label, what. | NOT-WIRED | `GET /api/workflows/{workflow_id}` returning 18 `wfDetailVM.*` fields. Big cross-service join. |
| **WF.3** | Workflow — begin training | "Begin Training The record Tier 1" · "Objective" · "Before it starts" · "It will cost / It will use / When it will finish" · "Preview outcomes" · Resubmit / Retire this attempt. | PROTOTYPE-SAMPLE | Backend: `/api/training/*` mounted (`training_router`, 1 568 LOC). Wire begin-training flow. |
| **O.1** | Opportunities — standing across the estate | "Six things could be built" · list with tier, estimated cost, GPU hours, workflow link. "Rough estimate — nothing committed yet." Get a fresh estimate / Request review. | NOT-WIRED | Mount `services/opportunity_briefs/` (currently UNMOUNTED). Endpoint: `GET /api/opportunities` returning brief list + per-brief detail via `GET /api/opportunities/{id}`. |
| **O.2** | Opportunity → workflow | "View workflow:" — link from opportunity to workflow-detail. | NOT-WIRED | Cross-linking only — no new backend beyond O.1 + WF.2. |
| **M.1** | Master version history | Placeholder + populated view. 17 `mrDetailVM.*` fields including custody path/ref/when, receipt, receipt note, tier, tier note, trend note, trend range, provenance title, licence, insight, status label, admission badge, code, name, origin, what, banner text. | NOT-WIRED | **New backend: `GET /api/master_version_history`** — reads `services/baseline_line/` (102 LOC, mounted — is the model-baseline record) + `services/model_registry/` + `services/audit_trail/`. Big join. |
| **D.1** | Documents (implicit) | "It's drafted in Documents." Documents surface for prepared training whitepapers, drafts, decks. | PROTOTYPE-SAMPLE | `services/whitepapers/` (150 LOC, mounted `whitepapers_router`) + `services/wpw/` (923 LOC, invariant-frozen). Endpoint likely exists; needs binding. |
| **X.1** | Chat archive | "Archived conversations" · Archive this chat? · Permanently delete this chat? modal flows. | PROTOTYPE-SAMPLE | Chat service extension for archive/delete. |
| **X.2** | Access-restricted screen | "Access restricted × ← Back You don't have access to {{ efDeniedName }}. Contact your Registry admin if you need access." | NOT-WIRED | Frontend-only. Static screen bound to auth service's denial reason. |

**Non-Registry sub-total: 18 rows.** LIVE-DATA (partial or full): 4 · PROTOTYPE-SAMPLE: 6 · NOT-WIRED: 8.

### 2.3 · Aggregate surface counts

**Total surfaces the new v2 HTML defines: 47 rows** (29 Registry + 18 non-Registry).

| State | Registry | Non-Registry | Total |
|---|---|---|---|
| LIVE-DATA (partial/full) | 5 | 4 | 9 |
| PROTOTYPE-SAMPLE | 7 | 6 | 13 |
| NOT-WIRED | 17 | 8 | 25 |

**25 of 47 surfaces (53 %) are NOT-WIRED to any backend today.** Registry (owner priority) has 17 of those 25 (68 % of the gap sits inside Registry). Full Registry build closes 22 of 29 rows against real routes.

**New backend routes needed for a fully-live v2 (union across all rows):**

- `/api/registry/mix` (or extend `/api/registry/facts` with cut breakdowns)
- `/api/registry/source/{source_id}/profile`
- `/api/registry/cir` (Confidential Information Register)
- `/api/census/status` (or extend `/api/census/latest`)
- `/api/census/history`
- `/api/census/{census_id}/transcript`
- `/api/compute/spend` (rollup from `services/cost_ledger/`)
- `/api/compute/workloads`
- `/api/compute/traffic`
- `/api/compute/machine/{machine_id}`
- `/api/model_registry/full_record`
- `/api/model_registry/{model_id}/answering`
- `/api/model_registry/{model_id}/checks`
- `/api/model_registry/{model_id}/refusals`
- `/api/model_registry/{model_id}/journal`
- `/api/model_registry/{model_id}/traffic`
- `/api/opportunities` + `/api/opportunities/{id}` (mount existing `services/opportunity_briefs/`)
- `/api/governance/rulebooks` (shelf)
- `/api/governance/rulebook/{id}` (extend with per-rule profile fields)
- `/api/governance/rules_updates` + `POST /api/governance/rules_updates/{id}/sign`
- `/api/governance/approvals`
- `/api/governance/preview` (for "Preview outcomes")
- `/api/governance/shelf_intelligence`
- `/api/workflows` + `/api/workflows/{workflow_id}`
- `/api/master_version_history`

**Total new endpoints: 25** (all read; 1 write: rules_updates signing). Owner priority W-REGISTRY-FULL-BUILD covers ~14 of these (all `/api/registry/*`, `/api/census/*`, `/api/compute/*`, `/api/model_registry/*`).

**Existing services to mount that already have code:**

- `services/opportunity_briefs/` — UNMOUNTED today per grep.
- `services/perception/` (2 158 LOC) — UNMOUNTED, needed for Source Profile perception field.

---

## §3 · Registry-first build order (proposed, awaiting owner steer)

Not fired until owner has seen this table and steered. Sequence proposal:

1. **Portal swap** — point iframe at `/v2_prototype.html`. Real-Chromium harness re-run to capture new anchor selectors. Byte-identity + rendered-DOM law preserved.
2. **Substitution re-authoring** — re-anchor the ~17 existing substitution rules (Registry topline / compute estate / etc.) against v2's rendered anchors. Rules matching nothing = RED.
3. **Registry Data Connected** — add `/api/registry/mix`, `/api/registry/cir`, `/api/registry/source/{id}/profile`, `/api/census/status`, `/api/census/history`. Fill 5 NOT-WIRED cells.
4. **Registry Compute Connected** — add `/api/compute/spend`, `/api/compute/workloads`, `/api/compute/traffic`, `/api/compute/machine/{id}`. Extend `/api/compute/estate` for per-GPU state. Fill 6 NOT-WIRED cells.
5. **Registry LLMs & Trained Models** — add 5 per-model endpoints (answering, checks, refusals, journal, traffic) + `full_record`. Mount opportunity_briefs. Fill 6 NOT-WIRED cells.
6. **Non-Registry Rules Updates + Rule Book Library shelf** — priority-adjacent because CIR entry from Registry drops into Rules Updates.

Each step tests-first, `BASELINE_GUARD=1` ratchet from **2991**, real-Chromium harness re-run after each substitution wave.

---

**Discipline note:** this audit is the deliverable the owner asked for; no build has started. STEP 3 (Registry build) does not fire until owner has read this table and steered.
