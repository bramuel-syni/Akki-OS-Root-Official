# W-G5c-COMPUTE-RESIDUALS Grounding Brief · 2026-09-06

**Wave name:** `W-G5c-COMPUTE-RESIDUALS` (sub-close of W-G5c) · residuals `-r1` (chart-captions + per-bar labels) and `-r2` (tile-notes).

**Authority — owner ruling verbatim (2026-09-06T~12:XX):**

> "(c) first: the small residuals wave — chart-caption substitutions (-r1: '1,240 hrs committed', '2,880 hrs this month', per-bar size labels) and tile-note substitutions (-r2: '43% of the month', 'wall-clock across 4 GPUs', 'quoted against, not reserved'). Same discipline as COMPUTE-v2: rules authored only against harness-verified rendered DOM, live values from /api/compute/estate where a real fact exists, honest-empty/honest-phrasing where no mechanism exists, styling preserved, RED receipts, double-green from floor 2836, harness re-verify with screenshot. This completes the Compute surface visually for the owner's pending eyeball."

**Standing conditions** (from `STATE/NEXT.md` §OWNER STANDING CONDITIONS):
- CONDITION 1 · NO PARAPHRASING REQUIREMENTS: every requirement quoted verbatim from source.
- Test docstrings MUST cite the verbatim quote (doc + region + exact words).
- Grounding brief assembled from source text, not from summaries.

---

## Section A · Verbatim source quotes (prototype)

### A.1 Chart-caption source (verbatim from `pod_shell/frontend/public/v8_prototype.html`, byte range 766300–768200)

The prototype declares a single `COMPUTE_CHARTS` object literal with three chart states (`door` / `week` / `state`). The current chart state is bound to `s.computeChart`, changed via an `<sc-raw-select>` (byte ~490811) with `sc-camel-on-change="{{ computeChartChange }}"`. Chart title/caption/rows are surfaced by view-variables `chartTitle`, `chartCaption`, `chartRows` (byte ~480163 / 480286). Chart-caption is rendered inside `<div style="font-size:11.5px;color:var(--ink3);white-space:nowrap;">{{ chartCaption }}</div>` — verbatim from prototype.

Verbatim prototype-literal object (bytes 766500–767760):

```js
const COMPUTE_CHARTS = {
  door: {
    label: 'Hours by door',
    title: 'Committed hours by door',
    caption: '1,240 hrs committed',
    rows: [
      {label:'Train',   pct:52, size:'645 hrs · 52%', fill:'var(--blue)'},
      {label:'Extract', pct:24, size:'298 hrs · 24%', fill:'#4b6a9b'},
      {label:'Export',  pct:14, size:'174 hrs · 14%', fill:'#7d93b6'},
      {label:'Measure', pct:8,  size:'99 hrs · 8%',   fill:'#9fb0c9'},
      {label:'Prove',   pct:2,  size:'24 hrs · 2%',   fill:'#c2cbd9'}
    ]
  },
  week: {
    label: 'Hours by week',
    title: 'Hours run by week',
    caption: 'of 2,880 hrs available',
    rows: [
      {label:'Aug 1–7',    pct:38, size:'274 hrs · 38%', fill:'var(--blue)'},
      {label:'Aug 8–14',   pct:47, size:'339 hrs · 47%', fill:'#4b6a9b'},
      {label:'Aug 15–21',  pct:9,  size:'65 hrs · 9%',   fill:'#9fb0c9'},
      {label:'Not yet run',pct:6,  size:'43 hrs · 6%',   fill:'repeating-linear-gradient(135deg,#d8d2c2 0 4px,#efe9da 4px 8px)'}
    ]
  },
  state: {
    label: 'Hours by state',
    title: 'Hours by state',
    caption: '2,880 hrs this month',
    rows: [
      {label:'Committed',        pct:43, size:'1,240 hrs · 43%', fill:'var(--blue)'},
      {label:'Free to allocate', pct:57, size:'1,640 hrs · 57%', fill:'var(--surface2)'}
    ]
  }
};
```

**Owner-named r1 targets (2 chart captions + "per-bar size labels" as a category):**
- Chart caption `'1,240 hrs committed'` — in `door` state
- Chart caption `'2,880 hrs this month'` — in `state` state
- Per-bar size labels (category · owner named `per-bar size labels`) — 11 total across three chart states

**Full r1 scope (chart-caption category · derived by inclusion of the third caption via chart-caption unity — same DOM slot, same substitution mechanism, same discipline):**
- `'1,240 hrs committed'` · caption of `door`
- `'of 2,880 hrs available'` · caption of `week` · IMPLICIT-SCOPE-BY-CATEGORY (unity of chart-caption surface — leaving this uncovered would render half the caption slot as live and half as prototype dummy · declared honest here)
- `'2,880 hrs this month'` · caption of `state`
- 5 per-bar labels of `door`: `'645 hrs · 52%'`, `'298 hrs · 24%'`, `'174 hrs · 14%'`, `'99 hrs · 8%'`, `'24 hrs · 2%'`
- 4 per-bar labels of `week`: `'274 hrs · 38%'`, `'339 hrs · 47%'`, `'65 hrs · 9%'`, `'43 hrs · 6%'`
- 2 per-bar labels of `state`: `'1,240 hrs · 43%'`, `'1,640 hrs · 57%'`

**r1 rule count: 3 captions + 11 per-bar labels = 14 rules.**

### A.2 Tile-note source (verbatim from `pod_shell/frontend/public/v8_prototype.html`, byte range 1198800–1199650)

Verbatim `computeStats` array (bytes 1198800–1199650):

```js
computeStats: [
  {label:'Clusters attached',    value:'1',        note:'on-premise · RMS AI DC, Nairobi'},
  {label:'GPUs',                  value:'4',        note:'A100 80GB · single node'},
  {label:'Capacity this month',   value:'2,880 hrs',note:'wall-clock across 4 GPUs'},
  {label:'Committed to work',     value:'1,240 hrs',note:'43% of the month'},
  {label:'Free to allocate',      value:'1,640 hrs',note:'quoted against, not reserved'},
  {label:'Jobs waiting',          value:'2',        note:'both under the auto-run ceiling'},
  {label:'Workflows this month',  value:'18',       note:'14 complete, 3 ongoing, 1 failed'},
  {label:'Utilisation',           value:'43%',      note:'measured against wall-clock'},
  {label:'Runs receipted',        value:'100%',     note:'runtime named in every receipt'}
],
```

**Owner-named r2 targets (3 exact notes):**
- `'43% of the month'` · note of "Committed to work" tile
- `'wall-clock across 4 GPUs'` · note of "Capacity this month" tile
- `'quoted against, not reserved'` · note of "Free to allocate" tile

**r2 rule count: 3 rules (as specified by owner).** Six other tile-notes (`on-premise · RMS AI DC, Nairobi`, `A100 80GB · single node`, `both under the auto-run ceiling`, `14 complete, 3 ongoing, 1 failed`, `measured against wall-clock`, `runtime named in every receipt`) are OUT OF SCOPE this wave. The first two are already bound by COMPUTE-v2 rules `compute-v2-clusters-byline` and `compute-v2-gpus-byline` (owner Ruling F). The remaining four are candidate scope for a future `-r3` if the owner rules to complete the tile-note surface.

### A.3 DOM-verified rendered text (`tools/compute_v2_dom_map.json`, produced by `tools/compute_v2_dom_enum.py` for W-G5c-COMPUTE-v2)

Existing probe (default-state = `s.computeChart="door"`) verifies as rendered text:
- `'1,240 hrs committed'`
- `'645 hrs · 52%'`, `'298 hrs · 24%'`, `'174 hrs · 14%'`, `'99 hrs · 8%'`, `'24 hrs · 2%'`
- `'43% of the month'`, `'wall-clock across 4 GPUs'`, `'quoted against, not reserved'`

**Missing from existing probe (require chart-state click-through):**
- `'of 2,880 hrs available'` · caption of `week` state
- `'2,880 hrs this month'` · caption of `state` state
- 4 per-bar labels of `week`: `'274 hrs · 38%'`, `'339 hrs · 47%'`, `'65 hrs · 9%'`, `'43 hrs · 6%'`
- 2 per-bar labels of `state`: `'1,240 hrs · 43%'`, `'1,640 hrs · 57%'`

**Probe extension required this wave**: `tools/compute_residuals_dom_enum.py` navigates to Admin > Registry > Compute Connected, then switches `<sc-raw-select value="{{ computeChart }}">` through each of `door` / `week` / `state` states via `page.select_option` and captures visible text at each. Output: `tools/compute_residuals_dom_map.json` covering all 17 target strings. Discipline: rules must match this extended probe artefact (rule-must-match-rendered-DOM invariant preserved).

---

## Section B · Live-vs-honest-empty determination (compute-estate `/api/compute/estate`)

Existing surface (from `services/compute_estate/estate.py` inspection at W-G5c-COMPUTE-v2 authoring):
- `estate.hosts[]` with `name`, `readiness`, `gpu_model`, `gpu_count`, `gpu_memory_gb_per_gpu`
- `estate.rollup` with `host_count`, `gpu_count_total`, `gpu_memory_gb_total`
- NO wall-clock capacity ledger · NO committed-hours ledger · NO by-door/by-week/by-state breakdown · NO free-hours-available ledger · NO utilisation percentage · NO Jobs-waiting queue-depth · NO Workflows-this-month completion breakdown.

**LIVE fact substitutions available this wave: 0.** All r1 chart-captions + all r1 per-bar labels + all r2 tile-notes present no measurable estate fact.

**Discipline consequence:** every r1 + r2 rule this wave is **HONEST-EMPTY** or **HONEST-PHRASING**, following the compute-v2 discipline `"honest-empty for anything the estate cannot measure"`. Chart-caption and per-bar rules render `'not measured'`. Tile-note rules render honest phrasings that name the missing mechanism (or preserve the prototype phrasing where it is honest product-language, e.g. `'quoted against, not reserved'`).

**Per-rule HONEST-EMPTY / HONEST-PHRASING mapping:**

| Rule | Dummy | Render |
|---|---|---|
| `compute-residuals-r1-chart-caption-door` | `1,240 hrs committed` | `not measured` |
| `compute-residuals-r1-chart-caption-week` | `of 2,880 hrs available` | `not measured` |
| `compute-residuals-r1-chart-caption-state` | `2,880 hrs this month` | `not measured` |
| `compute-residuals-r1-bar-door-train` | `645 hrs · 52%` | `not measured` |
| `compute-residuals-r1-bar-door-extract` | `298 hrs · 24%` | `not measured` |
| `compute-residuals-r1-bar-door-export` | `174 hrs · 14%` | `not measured` |
| `compute-residuals-r1-bar-door-measure` | `99 hrs · 8%` | `not measured` |
| `compute-residuals-r1-bar-door-prove` | `24 hrs · 2%` | `not measured` |
| `compute-residuals-r1-bar-week-1` | `274 hrs · 38%` | `not measured` |
| `compute-residuals-r1-bar-week-2` | `339 hrs · 47%` | `not measured` |
| `compute-residuals-r1-bar-week-3` | `65 hrs · 9%` | `not measured` |
| `compute-residuals-r1-bar-week-4` | `43 hrs · 6%` | `not measured` |
| `compute-residuals-r1-bar-state-committed` | `1,240 hrs · 43%` | `not measured` |
| `compute-residuals-r1-bar-state-free` | `1,640 hrs · 57%` | `not measured` |
| `compute-residuals-r2-note-capacity` | `wall-clock across 4 GPUs` | HONEST-PHRASING: `wall-clock ledger not measured` |
| `compute-residuals-r2-note-committed` | `43% of the month` | HONEST-PHRASING: `share-of-month not measured` |
| `compute-residuals-r2-note-free` | `quoted against, not reserved` | HONEST-PHRASING: `quoted against, not reserved` (prototype phrasing is honest product-language — preserved verbatim per compute-v2 §Product-language rule) |

Note on `compute-residuals-r2-note-free`: this dummy is not a numeric measurement — it is a governance statement about allocation policy. Preserving it verbatim as HONEST-PHRASING is analogous to `compute-v2-runs-receipted-value` (LIVE-TAUTOLOGY, governance guarantees the value). The other two r2 notes name numeric measurements that don't exist, hence honest-empty phrasing that names the missing mechanism.

---

## Section C · Anchor authorship (rule-must-match-rendered-DOM discipline)

Following COMPUTE-v2 pattern (styled-element-anchor with `anchorAncestorText`), each rule declares an ancestor-text anchor that pins its target uniquely in the rendered DOM. For chart captions + per-bar labels the anchor is the chart's `chartTitle` (e.g. `Committed hours by door`, `Hours run by week`, `Hours by state`) rendered adjacent to the caption. For tile notes the anchor is the tile `label` (e.g. `Capacity this month`, `Committed to work`, `Free to allocate`).

Anchor-text-to-rule mapping (verbatim from prototype):

| Rule (r1 caption) | anchorAncestorText |
|---|---|
| `compute-residuals-r1-chart-caption-door`  | `Committed hours by door` |
| `compute-residuals-r1-chart-caption-week`  | `Hours run by week` |
| `compute-residuals-r1-chart-caption-state` | `Hours by state` |

| Rule (r1 per-bar) | Row label (verbatim) | Chart state |
|---|---|---|
| `compute-residuals-r1-bar-door-train`   | `Train`   | `door` |
| `compute-residuals-r1-bar-door-extract` | `Extract` | `door` |
| `compute-residuals-r1-bar-door-export`  | `Export`  | `door` |
| `compute-residuals-r1-bar-door-measure` | `Measure` | `door` |
| `compute-residuals-r1-bar-door-prove`   | `Prove`   | `door` |
| `compute-residuals-r1-bar-week-1`       | `Aug 1–7`     | `week` |
| `compute-residuals-r1-bar-week-2`       | `Aug 8–14`    | `week` |
| `compute-residuals-r1-bar-week-3`       | `Aug 15–21`   | `week` |
| `compute-residuals-r1-bar-week-4`       | `Not yet run` | `week` |
| `compute-residuals-r1-bar-state-committed` | `Committed`        | `state` |
| `compute-residuals-r1-bar-state-free`      | `Free to allocate` | `state` |

Per-bar labels: the substitution anchor is the row-label text (e.g. `Train`) which is a unique text node in the same grid row as the size-label. `anchorAncestorText` pins on that per-bar row label.

| Rule (r2 note) | anchorAncestorText |
|---|---|
| `compute-residuals-r2-note-capacity`  | `Capacity this month` |
| `compute-residuals-r2-note-committed` | `Committed to work`   |
| `compute-residuals-r2-note-free`      | `Free to allocate`    |

---

## Section D · Definition of Done for this wave (verbatim from owner ruling)

1. "Rules authored only against harness-verified rendered DOM" — probe extension (`tools/compute_residuals_dom_enum.py`) + probe artefact (`tools/compute_residuals_dom_map.json`) present and covers all 17 target strings.
2. "Live values from /api/compute/estate where a real fact exists" — 0 LIVE-facts identified this wave (Section B) so all rules render honest-empty / honest-phrasing.
3. "Honest-empty/honest-phrasing where no mechanism exists" — 14 chart-caption/per-bar rules render `not measured`; 3 tile-note rules render honest phrasings that either name the missing mechanism or preserve verbatim honest product-language.
4. "Styling preserved" — every substitution keeps original DOM style attributes (font-size, color, white-space). Rules use `kind:"styled-element-anchor"` (same mechanism as compute-v2).
5. "RED receipts" — mechanical right-reason RED banked before implementation, showing each new test failing on missing rule-name / missing dummy / missing anchor before any code lands.
6. "Double-green from floor 2836" — 2 consecutive `BASELINE_GUARD=1` runs at the new floor (2836 + delta), byte-match on pass/skip/warning tallies.
7. "Harness re-verify with screenshot" — real-Chromium harness (`tools/wave_g5_realchrome_verification_harness.py`) re-run after implementation, capturing portal + registry + compute screenshots to `phase0/eyeball_proxies/`.
8. "This completes the Compute surface visually for the owner's pending eyeball" — 6 uncovered tile-notes and any un-navigated visual states banked as honest scope-limits for a follow-on `-r3`.

---

## Section E · Wave-honest-limits (banked in advance for the close DECISIONS entry)

1. **6 tile-notes remain uncovered** in this wave (owner named only 3). Uncovered: `on-premise · RMS AI DC, Nairobi` (already covered by compute-v2-clusters-byline as an owner Ruling F derivation), `A100 80GB · single node` (already covered by compute-v2-gpus-byline), `both under the auto-run ceiling` (Jobs waiting), `14 complete, 3 ongoing, 1 failed` (Workflows this month), `measured against wall-clock` (Utilisation), `runtime named in every receipt` (Runs receipted — could be LIVE-TAUTOLOGY like the compute-v2 100% receipt rule if owner extends r2). Candidate `-r3` scope.
2. **0 LIVE facts landed this wave** (see Section B). The compute-estate surface remains at 4 LIVE + 6 HONEST-EMPTY + 1 LIVE-TAUTOLOGY (11 rules from COMPUTE-v2) plus this wave's 14 + 3 = 17 all-honest-empty/honest-phrasing rules. Future waves adding hour-ledger + queue-depth + workflow-completion measurement would let the r1 and r2 dummies flip to LIVE facts.
3. **Chart-selector navigation depth**: probe extension must click through `<sc-raw-select value="{{ computeChart }}">` state (`door` / `week` / `state`) to capture all 3 chart states. If the harness cannot reliably switch chart states, HONEST-EMPTY still holds for the strings via prototype-source-verification (Section A) but the rule-must-match-rendered-DOM invariant tightens to source-verified-not-dom-verified for those strings. Banked as an honest fallback discipline.

---

## Section F · Commit protocol

- Track-a `programme/track-a`: single commit "W-G5c-COMPUTE-RESIDUALS-close" with rules + tests + baseline_failures.json bump.
- Master `master`: mirror commit + probe extension + probe artefact + eyeball_proxies output + STATE files.
- No push (local commits only).

*Grounding brief authored 2026-09-06T12:XX pre-RED. All requirements traced verbatim to prototype source and owner ruling.*
