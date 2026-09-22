# Portal Census journey · UI dashboard spec (BANKED FOR POST-R-91)

- **Wave**: CENSUS-SURFACE-A (Commit-A base) + Commit-A' journey extension
- **Design source**: RMS AI Prototype Ver 2.0 Sep 2026 · 20-page spec (owner
  share 2026-09-22T~03:10Z). The census journey lives INSIDE the Registry
  page ("Registry — MANAGE ESTATE", Shield report button slot). This is
  NOT a separate app — it is the Registry page's census section.
- **Status**: BANKED · not implemented in App.js this seal.
- **Blocker**: R-91 horizon `2026-09-23T03:23:15Z` (owner NO-EXPEDITE ruling
  2026-09-21T~06:15Z verbatim: *"the countdown that cannot be shortened is
  the ceremony … waiving it because the sweep already proved green is
  exactly the argument every future shortcut would make"*).
- **Post-R-91 ε-apply gate**: the ε-apply mirrors the current
  `/app/frontend/src/App.js` byte-identically to `pod_shell/frontend/src/App.js`.
  UI spec lands on both files in the SAME seal AFTER ε-apply completes.
- **Owner directive verbatim (2026-09-22T~03:10Z)**: *"Design shared: Registry
  → 'see past census' → census listings → click one → full detail (Discovery
  Summary / GPU Spend / Conversation / Discovery Details tabs)."*

## 1. Journey shape (owner design pixel-for-layout)

```
Registry (MANAGE ESTATE)
└── "see past census" link
    └── Every census LIST view  ← /api/portal/census/records
        │   intro: "Here is every census that has run..."
        │   [← Back to Registry]
        │   ┌──────────────────────────────────────────────────────┐
        │   │  #3 · NEEDS_ATTENTION · owner · 2026-09-22T01:36:48Z │
        │   │  32 of 106 sources · 28m 12s                         │
        │   │  ⚠ 74 buckets IAM-denied — na7p4* audit-scope ...    │
        │   │  ⚠ Cold-tier buckets returning InvalidObjectState... │
        │   │  ⚠ HF-HOLD SEC-2026-09-12-01 still standing...       │
        │   └──────────────────────────────────────────────────────┘
        │   ┌──────────────────────────────────────────────────────┐
        │   │  #2 · COMPLETE · owner · 2026-09-06T09:35:28Z        │
        │   │  2 of 2 sources · 1m 26s                             │
        │   └──────────────────────────────────────────────────────┘
        │   ┌──────────────────────────────────────────────────────┐
        │   │  #1 · COMPLETE · owner · 2026-08-28T15:48:38Z        │
        │   │  2 of 2 sources · 0m 56s                             │
        │   └──────────────────────────────────────────────────────┘
        │
        └── Click row → DETAIL view  ← /api/portal/census/records/{id}
            │   [← Back to how the estate is measured]
            │
            │   ┌── HEADER CARD ─────────────────────────────────┐
            │   │  Census #3 · NEEDS_ATTENTION                   │
            │   │  Initiator: owner                              │
            │   │  Started: 2026-09-22T01:36:48Z                 │
            │   │  Duration: 28m 12s · 32 of 106 sources         │
            │   │  ⚠ 74 buckets IAM-denied — banked to desk queue│
            │   └────────────────────────────────────────────────┘
            │
            │   WHAT THIS CENSUS DISCOVERED
            │   ┌──[Discovery Summary]──[GPU Spend]──[Conversation with Agent]──[Discovery Details]──┐
            │   │                                                                                    │
            │   │  Tab 1 · DISCOVERY SUMMARY                                                         │
            │   │    intro: "Everything this census touched, grouped the way a data engineer..."    │
            │   │                                                                                    │
            │   │    CONDITION OF WHAT WAS READ                                                      │
            │   │      ┌─── of 161.76 TB held ────────────────────────────────────────────────┐    │
            │   │      │████ Clean 15.5%   ██ Duplicate 2%   █ Degraded 0.5%   ██ Incomplete 2%│    │
            │   │      │██████████████████████████████████████████████████████ Not read 80.0% │    │
            │   │      └─────────────────────────────────────────────────────────────────────┘    │
            │   │                                                                                    │
            │   │    COVERAGE                                                                        │
            │   │      Data held: 161.76 TB — Total volume across every connected OBS surface       │
            │   │      Sources read in full: 32 of 106                                               │
            │   │      Left out: na7p4* audit-scope (74) · cold-tier buckets                        │
            │   │                                                                                    │
            │   │  Tab 2 · GPU SPEND                                                                 │
            │   │    2 hosts (akki-vm + akki-vm-ii) · 4x H200 · 1.2 GPU-hours · 62% util             │
            │   │    1,568 audio objects processed · faster-whisper tiny int8 · 1 proc/GPU           │
            │   │                                                                                    │
            │   │  Tab 3 · CONVERSATION WITH AGENT                                                   │
            │   │    8 entries chronological · owner directives + agent replies at each pivot        │
            │   │                                                                                    │
            │   │  Tab 4 · DISCOVERY DETAILS                                                         │
            │   │    6 surfaces · per-surface freshness + chapter proof-links                        │
            │   │    Duplication chapter · Access map (readable/blocked/unlocks)                     │
            │   └────────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Backend contract (LIVE at Commit-A' · this seal)

Route family: `/api/portal/census/*` (JWT-gated · same pattern as R-100 portal).

| Route | Purpose | Powers |
|---|---|---|
| `GET /records` | LIST view | `EveryCensusList.jsx` |
| `GET /records/{id}` | DETAIL view (header + 4 tabs) | `CensusDetailPage.jsx` |
| `GET /assets` | Mtafiti asset inventory | Discovery Details tab · assets grid |
| `GET /surfaces` | Per-surface breakdown | Discovery Details tab · surface list |
| `GET /access` | Readable/blocked/unlocks | Discovery Details tab · access map |
| `GET /latest` | Current chapter refs + provenance | Registry hub · "latest census" tile |
| `GET /duplication` | Tier-1/Tier-2 dup chapter | Discovery Details tab · duplication panel |

All routes tested by `tests/invariants/test_portal_census_surface_connection.py` (17) + `tests/invariants/test_portal_census_journey.py` (18) — total 35 invariants.

## 3. Component shape (Shadcn UI · matching existing portal conventions)

### 3.1 `RegistryCensusSection.jsx` — embedded inside existing Registry page

Placed inside the "MANAGE ESTATE" area of the Registry page (next to the Shield report button per design). Renders "see past census" link that opens `EveryCensusList.jsx`.

```jsx
<section data-testid="registry-census-section">
  <h2>Estate census</h2>
  <p>Every measure of the estate, since the first sweep.</p>
  <Link to="/portal/census" data-testid="see-past-census-link">
    → See past census
  </Link>
</section>
```

### 3.2 `EveryCensusList.jsx` — LIST view

- Route: `/portal/census` (JWT-gated · existing `<RequireAuth>` wrapper).
- Data: `GET /api/portal/census/records`.
- Layout: intro copy + back-link + rows.
- `data-testid="every-census-list"` on wrapper.
- Per-row `data-testid="census-list-row-{census_number}"`.
- Status badge component (variant by status): COMPLETE=default, RUNNING=primary+pulse, NEEDS_ATTENTION=warning (amber).

```jsx
{records.map(r => (
  <div data-testid={`census-list-row-${r.census_number}`} key={r.census_number}
       className="border-b py-4 cursor-pointer hover:bg-accent"
       onClick={() => navigate(`/portal/census/${r.census_number}`)}>
    <div className="flex items-baseline justify-between">
      <span className="text-xl font-mono">#{r.census_number}</span>
      <Badge variant={statusVariant(r.status)} data-testid={`status-${r.status}`}>
        {r.status.replace("_"," ")}
      </Badge>
    </div>
    <div className="mt-1 text-sm text-muted-foreground">
      {r.initiator} · {r.started_at_utc} · {r.duration} · {r.sources_read} of {r.sources_total} sources
    </div>
    {r.annotations.map((a, i) => (
      <div key={i} className="mt-2 text-sm text-amber-600" data-testid={`annotation-${r.census_number}-${i}`}>
        ⚠ {a}
      </div>
    ))}
  </div>
))}
```

### 3.3 `CensusDetailPage.jsx` — DETAIL view (header + 4 tabs)

- Route: `/portal/census/:id`.
- Data: `GET /api/portal/census/records/{id}`.
- Header card + Shadcn `Tabs` for four sections.
- Back-link uses `body.back_link_copy` verbatim (single source of truth — no hard-coded strings on FE).

```jsx
<div data-testid="census-detail-page">
  <Link to="/portal/census" data-testid="detail-back-link">
    {body.back_link_copy}
  </Link>
  <Card data-testid="census-detail-header">
    <CardHeader>
      <CardTitle>Census #{h.census_number}</CardTitle>
      <Badge variant={statusVariant(h.status)}>{h.status.replace("_"," ")}</Badge>
    </CardHeader>
    <CardContent>
      <div>Initiator: {h.initiator}</div>
      <div>Started: {h.started_at_utc}</div>
      <div>Duration: {h.duration} · {h.sources_read} of {h.sources_total} sources</div>
      {h.annotations.map((a, i) => (
        <div key={i} className="text-amber-600">⚠ {a}</div>
      ))}
    </CardContent>
  </Card>

  <h2>WHAT THIS CENSUS DISCOVERED</h2>
  <Tabs defaultValue="summary" data-testid="census-detail-tabs">
    <TabsList>
      <TabsTrigger value="summary" data-testid="tab-summary">Discovery Summary</TabsTrigger>
      <TabsTrigger value="gpu" data-testid="tab-gpu">GPU Spend</TabsTrigger>
      <TabsTrigger value="conv" data-testid="tab-conversation">Conversation with Agent</TabsTrigger>
      <TabsTrigger value="details" data-testid="tab-details">Discovery Details</TabsTrigger>
    </TabsList>
    <TabsContent value="summary"><DiscoverySummaryTab data={ds} /></TabsContent>
    <TabsContent value="gpu"><GpuSpendTab data={gs} /></TabsContent>
    <TabsContent value="conv"><ConversationTab data={conv} /></TabsContent>
    <TabsContent value="details"><DiscoveryDetailsTab data={dd} subSlices={ss} /></TabsContent>
  </Tabs>
</div>
```

### 3.4 `DiscoverySummaryTab.jsx` — stacked bar + coverage rows

- Intro copy from `data.intro_copy` verbatim.
- Stacked horizontal bar: divs with `width: {pct}%` for each of the 5 buckets, colour-coded per design.
  - Clean → green
  - Duplicate → yellow
  - Degraded → orange
  - Incomplete → grey-blue
  - Not read → muted grey
- Bar caption: `of {(total_bytes_held / 1e12).toFixed(2)} TB held`.
- Legend row below bar with 5 labels + percentages.
- Below bar: `measurement_note` in small muted text (transparency about how the numbers were derived — critical for CENSUS-3 where "not_read=80%" needs the na7p4* IAM-blocked explanation).
- COVERAGE rows: `data_held_bytes` + `data_held_note` + delta chip (only if `delta_vs_previous_bytes` not null) + sources_full/sources_partial + sources_left_out.

`data-testid="condition-bar"` · `data-testid="condition-legend-{bucket}"` per legend item · `data-testid="coverage-data-held"` etc.

### 3.5 `GpuSpendTab.jsx`

- Hosts table (host + gpus).
- Stat cards: gpu_hours · utilization_pct · objects_processed.
- Model name + concurrency note.
- Receipt link.
- For CENSUS-1/-2: shows "No GPU used" empty state (metadata or CPU-only census).

### 3.6 `ConversationTab.jsx`

- Timeline layout: alternating owner/agent bubbles chronological by `at_utc`.
- Owner bubbles on the left (dark accent), agent bubbles on the right (muted).
- Authority footer citing STATE/DECISIONS.md source.

`data-testid="conversation-timeline"` · per-entry `data-testid="conv-entry-{index}-{role}"`.

### 3.7 `DiscoveryDetailsTab.jsx`

- Sub-tabs: Surfaces · Duplication · Access · Sub-slices (when present).
- Surfaces: from `data.surfaces[]` — table with surface_name / region / freshness_min → max / audio_share / chapter link.
- Duplication: real mirrors + rejected hypotheses (from `/api/portal/census/duplication`).
- Access: readable/blocked columns + `unlocks` action CTAs (see original UI spec at `phase0/surface_connection/portal_census_ui_spec.md` §2.3).
- Sub-slices: for CENSUS-3 only — chips showing slice_label + sub_wave_id + chapter_pointer link.

## 4. Post-R-91 landing checklist

1. [ ] R-91 ε-apply completes (2026-09-23T03:23:15Z or later).
2. [ ] Mirror `/app/frontend/src/App.js` ↔ `pod_shell/frontend/src/App.js` GREEN.
3. [ ] Add `/portal/census` route to App.js in BOTH locations same commit.
4. [ ] Author 7 components in BOTH `pod_shell/frontend/src/components/portal/census/*` and `/app/frontend/src/components/portal/census/*` same commit:
   - `RegistryCensusSection.jsx`
   - `EveryCensusList.jsx`
   - `CensusDetailPage.jsx`
   - `DiscoverySummaryTab.jsx`
   - `GpuSpendTab.jsx`
   - `ConversationTab.jsx`
   - `DiscoveryDetailsTab.jsx`
5. [ ] Ship RED-first UI invariant tests
       (`tests/invariants/test_portal_census_ui_wired.py` — Playwright checking `data-testid` presence + navigation + tab switching + status-badge variant selection).
6. [ ] Update `Registry` page (existing Registry component) to embed `RegistryCensusSection.jsx` next to the Shield report button.
7. [ ] Double-green sweep with `BASELINE_GUARD=1 PYTHONHASHSEED=0` against post-ε-apply ratchet floor.

## 5. Non-actions (SO §6.4 NOTHING-BEYOND)

- No App.js edit this seal.
- No component file authored under `/app/frontend/*` or `pod_shell/frontend/*` this seal.
- No modification to existing `Registry` page component this seal.
- No `data-testid` binding to a live DOM — spec only.
- No changes to R-99 canon-rules or R-100 portal routes.

**End of journey UI spec.**
