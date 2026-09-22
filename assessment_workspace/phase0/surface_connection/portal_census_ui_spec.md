# /api/portal/census UI dashboard specification (BANKED FOR POST-R-91)

- **Wave**: CENSUS-SURFACE-A · UI slice
- **Status**: BANKED · not implemented in App.js this seal.
- **Blocker**: R-91 horizon `2026-09-23T03:23:15Z` (owner NO-EXPEDITE ruling
  2026-09-21T~06:15Z verbatim: *"the countdown that cannot be shortened is the
  ceremony … waiving it because the sweep already proved green is exactly the
  argument every future shortcut would make"*).
- **Post-R-91 ε-apply gate**: the ε-apply mirrors the current
  `/app/frontend/src/App.js` byte-identically to `pod_shell/frontend/src/App.js`.
  This UI spec lands on both files in the same seal AFTER the ε-apply completes,
  so the mirror invariant `test_app_frontend_App_js_mirrors_pod_shell_App_js`
  remains green throughout.
- **Owner confirmation (this-session point a)**: *"CORRECT: bank the UI spec +
  component sketch as receipts now, ship the dashboard post-R-91 ε-apply. Do
  NOT attempt App.js edits inside the hold — the horizon is ~25h out and the
  seal discipline matters more than a day of UI latency. Backend endpoints ship
  now."*

## 1. Placement in the existing App.js route tree

New top-level route: **`/portal/census`** (JWT-required · same `<RequireAuth>`
wrapper pattern the R-100 portal surfaces use). Nav item added to the portal
sidebar under the existing "Portal" section:

```
Portal
├── Requests (existing)
├── Entitlement (existing)
└── Census                        ← NEW (CENSUS-SURFACE-A)
    ├── Assets                    (list · count-by-class + rows)
    ├── Surfaces                  (per-surface breakdown + freshness min/max)
    ├── Access                    (readable vs blocked + unlocks)
    ├── Duplication               (Tier-1/Tier-2 chapter)
    └── Latest                    (current wave + provenance pointers)
```

## 2. Component shape (Shadcn UI, matching existing portal conventions)

### 2.1 `PortalCensusPage.jsx` — top-level route component

```jsx
import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { Card, CardHeader, CardTitle, CardContent } from "../components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../components/ui/tabs";
import { Badge } from "../components/ui/badge";
import { Table, TableBody, TableRow, TableCell, TableHead } from "../components/ui/table";
import { Skeleton } from "../components/ui/skeleton";

export default function PortalCensusPage() {
  const { token } = useAuth();
  const [latest, setLatest] = useState(null);
  const [surfaces, setSurfaces] = useState(null);
  const [access, setAccess] = useState(null);
  const [assets, setAssets] = useState(null);
  const [duplication, setDuplication] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const opts = { headers: { Authorization: `Bearer ${token}` } };
    Promise.all([
      fetch(`${API_BASE}/api/portal/census/latest`, opts).then(r => r.json()),
      fetch(`${API_BASE}/api/portal/census/surfaces`, opts).then(r => r.json()),
      fetch(`${API_BASE}/api/portal/census/access`, opts).then(r => r.json()),
      fetch(`${API_BASE}/api/portal/census/assets`, opts).then(r => r.json()),
      fetch(`${API_BASE}/api/portal/census/duplication`, opts).then(r => r.json()),
    ]).then(([l, s, ac, as, d]) => {
      setLatest(l); setSurfaces(s); setAccess(ac); setAssets(as); setDuplication(d);
      setLoading(false);
    });
  }, [token]);

  if (loading) return <Skeleton className="h-96 w-full" data-testid="portal-census-loading" />;

  return (
    <div data-testid="portal-census-page" className="space-y-6 p-6">
      <header className="flex items-baseline justify-between">
        <h1 className="text-3xl font-semibold">Census · Estate registry</h1>
        <Badge variant="outline">{latest?.wave_id}</Badge>
      </header>
      <p className="text-sm text-muted-foreground">
        Every surface by proof link · Canon-9 §13 Mtafiti authority ·
        surfaced at {latest?.surfaced_at}
      </p>

      <Tabs defaultValue="surfaces" data-testid="portal-census-tabs">
        <TabsList>
          <TabsTrigger value="surfaces">Surfaces</TabsTrigger>
          <TabsTrigger value="access">Access</TabsTrigger>
          <TabsTrigger value="assets">Assets</TabsTrigger>
          <TabsTrigger value="duplication">Duplication</TabsTrigger>
          <TabsTrigger value="proofs">Proof links</TabsTrigger>
        </TabsList>

        <TabsContent value="surfaces"><SurfacesTable data={surfaces} /></TabsContent>
        <TabsContent value="access"><AccessBoard data={access} /></TabsContent>
        <TabsContent value="assets"><AssetsGrid data={assets} /></TabsContent>
        <TabsContent value="duplication"><DuplicationChapter data={duplication} /></TabsContent>
        <TabsContent value="proofs"><ProofLinks data={latest} /></TabsContent>
      </Tabs>
    </div>
  );
}
```

### 2.2 `SurfacesTable.jsx` — freshness min/max column-visible

Reads `data.surfaces[]` from `/api/portal/census/surfaces`. Columns:

| Surface | Region | Freshness (min → max) | Media types | Audio share | Chapter |
|---|---|---|---|---|---|
| obs_huawei | multi-region | 2015-01-01 → 2026-09-22 | audio/video/image/pdf/text | 18 % | ↗ |

`data-testid="census-surfaces-table"` on the wrapper; per-row
`data-testid="census-surface-row-{surface_name}"`.

### 2.3 `AccessBoard.jsx` — readable vs blocked + unlocks CTA

Two-column layout. Left column: readable buckets list (32 items, `data-testid="census-access-readable"`). Right column: blocked (74) with an
**Unlock action** callout per blocked-slice key (from `data.unlocks`):

- `na7p4_series` → *"Request IAM grant on na7p4* audit-scope from RMS admin"*
  · button `data-testid="census-unlock-na7p4-cta"` (external link to a mailto
  template or ticketing system; product decision at UI implementation time).
- `cold_tier_restore` → *"Issue Huawei OBS RestoreObject with tier=Standard"*
  · button `data-testid="census-unlock-cold-tier-cta"`.
- `hf_token` → *"Rotate HF token out-of-band, update backend .env, lift
  SEC-2026-09-12-01"* · button `data-testid="census-unlock-hf-cta"`.

### 2.4 `AssetsGrid.jsx` — Doc-0 TA-3.1 always-five taxonomy

Five stat cards (one per `AssetClass`). Each card shows count + click-through
to filter the `rows[]` list. Follows the `mtafiti.asset_inventory.
enumerate_classes_always_five` invariant: even if a class has 0 records, its
card is rendered with count=0 (never missing).

Per-card `data-testid="census-asset-class-card-{class_name}"`.

### 2.5 `DuplicationChapter.jsx` — Tier-1 + Tier-2 summary

Two accordions:

- **Confirmed real mirrors** (from `data.real_mirror_pairs_discovered_from_evidence_not_names`):
  each row shows the pair, verdict, and evidence chain (ETag equality → 3-point
  range read equality). `data-testid="census-dup-real-mirror-{pair_id}"`.
- **Name-pattern hypotheses REJECTED by evidence** (from
  `data.name_pattern_hypotheses_rejected_by_evidence`): each row shows the
  candidate pair + verdict + "why the name-similarity is not evidence of
  duplication" note. `data-testid="census-dup-rejected-hypothesis-{pair_id}"`.

### 2.6 `ProofLinks.jsx` — Canon-9 §13 proof-link surface

Lists `data.provenance_pointers[]` as clickable links. Each pointer is a
relative path to a `phase0/census_v3/*.json` receipt. In the fullness of the
post-R-91 build, these open in a read-only JSON viewer modal; for MVP,
render as `<code>` blocks with copy-to-clipboard.

## 3. Auth wiring

Reuses the existing `useAuth` hook (bearer JWT via `/api/auth/login`).
`<RequireAuth>` wraps `<PortalCensusPage />` in the router. No new auth
concerns; the router-level guard matches `/portal/requests` + `/portal/entitlement`
patterns already in App.js.

## 4. Backend contract (unchanged from Commit-A)

- All 5 endpoints under `/api/portal/census/*` require `Authorization: Bearer <access_token>`
  and return 401 `auth_missing` without it.
- All response shapes are stable (asserted by
  `tests/invariants/test_portal_census_surface_connection.py` · 17 tests).

## 5. Post-R-91 landing checklist

1. [ ] R-91 ε-apply completes (2026-09-23T03:23:15Z or later).
2. [ ] Byte-mirror `/app/frontend/src/App.js` ↔ `pod_shell/frontend/src/App.js`
       verified GREEN (`test_app_frontend_App_js_mirrors_pod_shell_App_js`).
3. [ ] Add `PortalCensusPage` route to App.js in both locations
       (same commit).
4. [ ] Author `PortalCensusPage.jsx` + 6 sub-components in both `pod_shell/frontend/src/components/portal/census/*` and `/app/frontend/src/components/portal/census/*` (same commit).
5. [ ] Ship RED-first UI invariant tests
       (`tests/invariants/test_portal_census_ui_wired.py` — Playwright or
       React Testing Library check on `data-testid` presence).
6. [ ] Double-green sweep with `BASELINE_GUARD=1 PYTHONHASHSEED=0` on the
       combined ratchet floor `5858 + 17 (SURFACE-A backend) + N (SURFACE-A UI)`.

## 6. Non-actions (SO §6.4 NOTHING-BEYOND)

- No App.js edit this seal.
- No component file authored under `/app/frontend/*` or `pod_shell/frontend/*` this seal.
- No `data-testid` binding to a live DOM — only spec.
- No modification to existing portal routes (`/portal/requests`, `/portal/entitlement`).

**End of UI spec.**
