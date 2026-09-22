# CP-CONNECT-CONFORMANCE-RULING · disk-verifiable conformance receipt

**Banked:** 2026-09-22T22:58:00Z
**Slice:** PHASE 4 (b-i) · Commit-A
**Owner directive (verbatim this-turn):** "If the prototype presents Connect as the one-panel ConnectResources shape → item (b) closes as ALREADY-LIVE with a conformance receipt (screenshot/DOM-check vs prototype). If the prototype presents a different Connect flow (multi-step drawer, wizard states) → prototype wins: implement to the prototype additively, retiring nothing sealed."

**Ruling:** SHAPE MATCHES. Item (b) Connect-half closes as ALREADY-LIVE.

---

## Prototype side — RMS_DAP_LATEST.html (custody-of-record drop 2026-09-20T1140Z)

Verified via literal-substring find in `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html`:

Four Connect Resources sub-page declarations in the `PAGES` map:

```
'c:key':{eyebrow:'Connect Resources', title:'Connect your workspace', sub:'A key lets you query the data from the tools you already use. Your queries come to Digicow; the data does not go to you.'}
'c:agents':{eyebrow:'Connect Resources', title:'Connect your AI agent', sub:'The most significant thing you can do here. Your agent gets its own account, its own permissions and its own monitoring.'}
'c:compute':{eyebrow:'Connect Resources', title:'Your compute', sub:'Digicow computers handle anything that touches the data. Your own are for what you do with the results afterwards.'}
'c:models':{eyebrow:'Connect Resources', title:'Your models and recipes', sub:'What you bring for a training run, registered and fingerprinted before it is used.'}
```

Shape: FOUR single-panel sub-pages, each with `{eyebrow, title, sub}` triple. NO wizard-step state variables, NO stepped-form flow, NO multi-step drawer. Verified via negative-scan for `wizardStep`, `connectStep`, `nextStep`, `step1..step5` in a 2000-char neighborhood of `c:key` — all absent.

## React side — pod_shell/frontend/src/pages/dap/ConnectResources.jsx (50 lines)

Verified via disk-read:

```jsx
const VIEWS = {
  key:     { title: "Workspace API Key",     detail: "... No endpoint exists for API key management. ..." },
  agents:  { title: "Your AI Agent",         detail: "... No route exists for agent registration." },
  compute: { title: "Your Compute",          detail: "POST /api/connect/gpu returns the declaration → hardening → acceptance handshake. ... Wiring deferred ..." },
  models:  { title: "Your Models & Recipes", detail: "POST /api/connect/intent records a model/recipe connection intent. ... Wiring deferred ..." },
};

export default function ConnectResources() {
  const { tab } = useParams();
  const view = VIEWS[tab] || VIEWS["key"];
  // ... single-panel render, BackendPending on all four tabs
}
```

Shape: FOUR single-panel sub-pages mounted at `/dap/connect/:tab` route, single-panel render per tab, no wizard-step state, no stepped-form. Byte-identical `/app/frontend/src` twin (per wave_g mirror + Ship-Manifest DoD).

## Conformance table

| Prototype (design-of-record) | React (as-built) | Shape match |
|---|---|---|
| `c:key` → "Connect your workspace" | `tab=key` → "Workspace API Key" (BackendPending) | ✓ |
| `c:agents` → "Connect your AI agent" | `tab=agents` → "Your AI Agent" (BackendPending) | ✓ |
| `c:compute` → "Your compute" | `tab=compute` → "Your Compute" (endpoint exists · form deferred) | ✓ |
| `c:models` → "Your models and recipes" | `tab=models` → "Your Models & Recipes" (endpoint exists · form deferred) | ✓ |

Shape conformance: **4/4** single-panel sub-pages, `{eyebrow, title, sub}` triple structure honored, no wizard-step drift on either side.

## Legacy ConnectWizard.jsx status

Self-declared retired-in-place per component docstring dated 2026-08-14: `"Owner Simplification 2026-08-14: The 5-step wizard is retired as the primary path. Connect collapses to ONE panel..."`. Currently NOT mounted at any `App.js` route on either byte-identical twin. LATER-wins ordering (prototype 2026-09-20 endorses 4-panel `ConnectResources` shape, not a 5-step wizard) confirms retired-in-place stays honored. File preserved per SO §3.8 additive-only. Zero deletion.

## Follow-on lane (banked-not-closed · deferred)

Copy-alignment sub-slice: swap tab `title` + optional lead paragraph to the prototype's exact `title:'Connect your workspace'` + `sub:'A key lets you query the data ...'` wording ON tabs where backend is present (compute + models). Content-only shift, not shape. Interleaves after CP-SKILLS-LAYER opens, or triggerable by a subsequent owner directive.

## Invariant enforcement

Ratcheted via `tests/invariants/test_cp_connect_conformance_ruling_phase_4_b_i.py`:

1. `test_dap_latest_prototype_declares_four_connect_subpages_verbatim` — prototype-side pin + negative-scan for wizard-step tokens.
2. `test_connect_resources_react_component_declares_four_tabs_verbatim` — React-side pin + byte-identity twin check + negative-scan for wizard-step tokens.
3. `test_connect_wizard_legacy_component_is_retired_in_place_and_unrouted` — legacy component retention + no-mount enforcement.

Test run receipt: `20260922T2258Z_conformance_receipt.log` — 3/3 GREEN 0.70s.

## Owner-directive ordering (verbatim citations)

- **2026-08-14 (superseded):** ConnectWizard.jsx docstring — "Owner Simplification 2026-08-14: The 5-step wizard is retired as the primary path. Connect collapses to ONE panel..."
- **2026-09-20 (design-of-record · LATER-wins):** DAP LATEST prototype drop — 4 `c:*` sub-pages under 'Connect Resources' eyebrow.
- **2026-09-22 (this-turn ruling · LATER-wins ordering applied):** Owner ruling verbatim: "LATER WINS. Therefore: check the v2 OS + DAP LATEST prototypes' Connect flow (the design of record). If the prototype presents Connect as the one-panel ConnectResources shape → item (b) closes as ALREADY-LIVE with a conformance receipt (screenshot/DOM-check vs prototype)."

Conclusion: prototype 4-panel shape wins over the 2026-08-14 'ONE panel' simplification (the "ONE panel" phrase in the retirement note is contradicted by the LATER 2026-09-20 prototype declaring 4 panels; the earlier phrasing was directionally correct — one panel-per-tab — but the LATER prototype clarifies to four such panels total).

**Item (b) Connect-half → CLOSED as ALREADY-LIVE per R-102 productized-or-honest-gap.**
