# OS-Prototype Frontends Card · CP-OS-PROTOTYPE-FRONTENDS-CARD · WAVE R-69 Step 8

**Purpose:** MISSION-FRAMED specialist-dispatch card for wiring the OS-prototype v2 surfaces (WorkStudio · ThinkLab · Collab · internal operator surfaces) to the live Akki-OS backend. **DAP portal is OUT of card scope** — held pending Step 9 (PRINCIPAL MODEL WAVE) seal per owner directive verbatim (principal-wave seal is the last gate on DAP portal frontend work · owner two-outstanding-conditions: principal-wave seals clean on its own evidence + surface-language trace resolved · **trace is resolved-clean at `e099ced1`** · wave-seal is the sole remaining gate).

**Card class:** notes-only state-master banking commit · NOT a §3.3 seal (no code · no test surface · no ratchet change · no sealed contract edited).

**Card status at authoring:** APPROVED-DRAFT · **pending owner ratification at next digest boundary** per owner steer 2026-09-20T~08:56Z verbatim ("(i) draft the frontends card for the OS-prototype surfaces ONLY citing the Front End Integration Brief — DAP portal is OUT of card scope until the owner answers §2.1"). Every DAP-portal-adjacent line in this card is tagged **[PENDING RATIFICATION]** in-line.

**Dependence-check gate verdict (Step 2 trace at `e099ced1`):** **CLEAR**. No MUST-DO/MUST-NOT line below leans on the phantom "2026-09-08 surface language" citation (PROVENANCE FAULT CONFIRMED null · downstream-assumption audit CLEAN). Card derives cleanly from Front End Integration Brief + RMS AI Prototype v2 + banked owner rulings alone.

---

## §1 · Sources (hash-pinned · §4.1 §F sha-pinning discipline)

| Source | Path | sha256 | Bytes |
| --- | --- | --- | --- |
| **Front End Integration Brief** | `custody/owner_drops/20260920T0824Z/Front_End_Integration_Brief.md` | `4a5fd14687b6ceaf700221034d91b64277eef4b0b8adb709f29795853bbe374b` | 53,284 |
| **RMS AI Prototype v2** (design of record · working-head lineage) | `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` | `9952692ce05809b3f4111c8ec3cf9dcb1008ea970895263981c2b52fb78cf199` | 2,286,992 |
| **DAP Backend Engineering Brief** (informational only · DAP portal OUT of card scope) | `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` | (sha in phase0/credential_drop_manifests/20260920T0824Z_owner_drops_manifest.json) | 88,393 |
| **RMS Data Access Portal** (informational only · DAP portal OUT of card scope) | `custody/owner_drops/20260920T0824Z/RMS_Data_Access_Portal.html` | (sha in manifest) | 327,266 |
| **Canon 5 §9.2** (refusal card copy — binding canon text) | canon anchor | — | — |
| **Owner ruling 2026-09-06** (prototype-v3 binding · Registry-priority) | STATE/DECISIONS.md verbatim | — | — |
| **Owner ruling 2026-09-19T~17:54Z** (survey now + closure waves in dependency order) | STATE/DECISIONS.md verbatim | — | — |
| **Owner ruling 2026-09-20T~08:24Z** (four-artifact drop · FEIB supersedes DAP UI Handoff Brief) | STATE/DECISIONS.md:17580 verbatim | — | — |
| **Owner ruling 2026-09-20T~08:56Z** (§2.1 CONFIRMED · OS-prototype card APPROVED · DAP portal OUT · G5 non-DAP freely) | STATE/DECISIONS.md:17615 verbatim | — | — |
| **Owner ruling this-session** (Step 8 strictly before Step 9 · principal-wave seal is last gate on DAP portal frontend work) | STATE/DECISIONS.md § this-Commit-B section verbatim | — | — |

**Provenance note (§0.2 of Brief):** `RMS AI Prototype v2 ACTIVE.dc.html` (working head) is 2,286,992 bytes; the banked `prototype_v3` sha `ee6ebe77e1c5…` was 2,032,024 bytes. Most likely reading is that v2 is the CURRENT working head of the prototype_v3 lineage and the banked sha is stale. **Confirmation required from owner** before any builder binds to either — the Brief's §0.2 raises this openly as a question to the owner.

---

## §2 · OBJECTIVE (mission-framed plain language)

**Wire the OS-prototype v2's WorkStudio · ThinkLab · Collab · and internal operator surfaces (Manage Estate · Approvals · Build Your Resources · Your Resources · 3rd Party Apps / Integration Console · The Watch · additional non-nav surfaces) to the live Akki-OS backend, without inventing UI, without inventing endpoints, and without smoothing over the three cross-cutting laws (no fabrication · refusals rendered verbatim · reference not copy). The prototype is the design of record; the Brief is the seam contract; the backend's discipline is enforced by invariant tests. A specialist ships surfaces one at a time in the order the Brief's §8 gives, and each surface is DONE when — and only when — §9 Acceptance Checks hold.**

DAP portal work is OUT of card scope until owner opens it after the principal-wave seal.

---

## §3 · MUST-DO (5–10 lines · specialist-dispatch bind)

1. **Read the Front End Integration Brief in full before writing any code.** It is a MAP, not a re-spec of the UI. sha `4a5fd14687b6…`. Where routes are `⚠ confirm`, pull `GET /api/openapi.json` and read the real Pydantic model — the JSON spec is authoritative (Brief §1.2).
2. **Wire the outer gate first (§1.3).** `IPAllowlistMiddleware` fires on FIRST PAINT with `HTTP 403 · text/plain · "This surface answers allowlisted addresses only."` This is NOT a login prompt, NOT an error state, and MUST NOT render a retry button or sign-in affordance. Every route (including static assets) is behind it. Detect `403 + text/plain body` and render a dedicated full-surface state carrying the sentence verbatim.
3. **Build the shared refusal card once (§2.2 · Canon 5 §9.2 verbatim).** Title: `Not to the standard you asked for.` Three actions in order: `Accept as recorded statement` · `Narrow the objective` · `Lower the standard`. Footer: `A refusal is the system keeping its promise.` Every surface that emits a refusal (Chat · Connect · ThinkLab/Solva stages · training seal) routes through this one card. Refusals are `200` with `refused: true` — a first-class success, never a 4xx.
4. **Enforce the three cross-cutting laws in every surface** (§2 · §6): (i) **No fabrication** — quantities always render, money only when `cost_total !== null`; when null, render literal `cost · not yet measured`; when `gaps_present` render `honest_gap_note` VERBATIM; append `(partial · lower bound)` when `total_cost_is_partial`. (ii) **Refusals rendered verbatim, never smoothed** — no paraphrase, no truncation. (iii) **Reference, not copy** — cite receipt identities (`rcp-<hex>`, `receipt_id`, `row_id`, `run_id`, `trace_id`, `preview_id`) as chips; never embed receipt content in the DOM.
5. **Follow the Brief's §8 integration order literally:** outer gate + error taxonomy → shared refusal card → Chat single-turn → Data Shield → Cost Ledger → ThinkLab → Registry/Census/Compute → Model Ecosystem → Connect/Commission wizards → Governance/Watch/Grey Mirror/Audit rollups → ceremony write paths. Steps 1-2 are prerequisites. Steps 3-5 together validate all three cross-cutting laws against real responses.
6. **Trust the repo React components (`bramuel-syni/Akki-OS-Root` @ `main` tree `07fb08f34a34`) for endpoint behaviour, NOT for UI.** They are v7-derived evidence of what each route accepts/returns and cover ~half the current design surface area. Where the repo React app and the v2 prototype differ in layout/navigation/naming/interaction, **the prototype wins** — sole exception is canon-supplied refusal copy (§2.2).
7. **Uniform transport (§1.1):** every call is `${REACT_APP_BACKEND_URL}/api/...`. No hardcoded hosts. No paths that skip `/api` (ingress routes on `/api/*` only). Resolve the `credentials: "include"` inconsistency (Training.jsx sends it, others omit it) with backend team before writing — `allow_credentials: true` combined with literal `*` origin is browser-rejected.
8. **ThinkLab (§3.2) is the best-aligned group** — 4 destinations all **W** wired to `/api/thinklab/*`. **Four-vs-five stage mismatch resolved in backend's favour** — render 5 stages sourced from `config.stage_labels`, never hardcoded, never truncated to 4. The prototype's stage model is to be brought up to 5.
9. **Honest-empty is a machine-readable contract, not a UI-team decision.** Empty responses carry `honest_gap` + `not_measured: true`. Render `honest_gap` verbatim; treat `not_measured` as machine-readable. Fabrication (rendering `$0.00` or blank when null) is a right-reason build-gate failure enforced by backend invariant tests.
10. **Every surface DONE means §9 Acceptance Checks all hold.** Do not ship a surface without: (a) receipt identity chips visible, (b) `honest_gap` rendered verbatim in the empty state, (c) refusal card routed through, (d) the outer 403 handled correctly on first paint, (e) `credentials` policy uniform with the rest of the build.

---

## §4 · MUST-NOT (specialist-dispatch bind)

1. **DAP portal work is OUT of card scope.** [PENDING RATIFICATION on principal-wave seal] Any DAP-4/DAP-7/DAP-13/DAP-21/DAP-33/DAP-34-adjacent surface (Extract · Request Lifecycle · Connect Resources · Available Resources · Data Governance · Data Estates · workspace API keys · agent registration · role gating tied to identity) waits until Step 9 (PRINCIPAL MODEL WAVE) seals clean on its own evidence. Owner-outstanding condition verbatim: "principal-wave seal is the last gate on DAP portal frontend work."
2. **Never write a second refusal component.** The one defined in §2.2 is canon (Canon 5 §9.2 verbatim). Reproduce without change wherever a refusal renders. Where the prototype's refusal wording differs from the canon copy, reconcile the prototype to the canon.
3. **Never build an auth interceptor, login screen, or 401 refresh path.** There is no auth header today (§1.5). The retired token gate no longer imports. IP allowlist is the sole access control. The prototype's role switcher (Employee → Manager → Exco → CEO) is a **view-level construct only** — never describe it as security, never ship it as access control. Before it ships as anything other than a demo control, it needs: identity plane + per-route authorization + server-side role claim. This is [PENDING RATIFICATION on principal-wave seal] scope.
4. **Never paraphrase, truncate, or replace `honest_gap`, `honest_gap_note`, `not_admissible_because`, or refusal `reason` / `what_would_raise_it` / `supported_class`.** These are server-authored prose intended for the user's eyes. Render verbatim.
5. **Never smooth a refusal into a 4xx error.** `POST /api/chat/ask` returns `200` with `refused: true`. This is by contract; treat it as a first-class successful response.
6. **Never invent chrome to display receipt content.** Use the prototype's existing audit/provenance affordances (shield glyph on each answer, audit drawer). Carry receipt identities as monospace chips (`rcp-<hex>` etc.), never receipt bodies.
7. **Never rename or reword copy on a v3-substitution-rule-bound surface without first checking `notes/v3_substitution_rules.json`.** A rule that matches nothing is RED by owner law, never silent (~37 rules bound at 2026-09-09 real-Chromium receipt · 0 orphans). A front-end change that removes or rewords a bound sentence breaks the build gate, not just the design.
8. **Never assume `RMS AI Prototype v2 ACTIVE.dc.html` (2,286,992 bytes · working head) is byte-identical to the banked `prototype_v3` sha `ee6ebe77e1c5…` (2,032,024 bytes).** Sizes differ; the naming implies v2 is ahead of v3. This is a **reading, not a fact** (§0.2 of Brief). Confirm with owner before binding.
9. **Never ingest `Principal_Model_Spec_v1.docx` (PRIN-1..PRIN-13) into card scope.** Its bindings belong to Step 9 (PRINCIPAL MODEL WAVE) RED-first tests · not to this card. This card's `role_switcher`-adjacent lines are [PENDING RATIFICATION] on Step 9's seal.
10. **Never fabricate an identity plane.** Any surface that presents itself as gated by identity/tenancy/consent is [PENDING RATIFICATION on principal-wave seal] scope — do not ship it, do not label it as access control, do not describe it as anything other than a view-level construct. R-21 (user-memory class + consent model) is owner-outstanding: no principal data written until ruled.

---

## §5 · Surface inventory (in-scope · dependence-cleared)

Legend: **W** wired (route exists) · **P** partial (route exists, covers some of the screen) · **G** gap (no route). Source: Brief §3.

### §5.1 WorkStudio (Brief §3.1 · 7 destinations)

| Destination | `appOpen` | Status | Route (per Brief) |
| --- | --- | --- | --- |
| Chat | `chat` | **P** | `POST /api/chat/ask` — Brief §5.1 |
| Data Suite | `analyze` | **G** | — |
| Documents | `documents` | **G** | — |
| My Work | `tasks` | **G** | — (Perform 360 · Brief §7.6) |
| My Team | `team` | **G** | `/api/team/*` adjacent, not equivalent |
| Company Goals | `performance` | **G** | — (Perform 360) |
| Board | `board` | **G** | — (Perform 360) |

Chat covers single-turn only; conversation rail, multi-turn history, rename/delete/archive, retry, regenerate, edit-and-resubmit, branch navigation are all client state (Brief §7.1–7.2). Composer: model picker binds to `/api/model_registry/models`; Shield Auto/Always and Think harder have no route (Brief §7.3–7.4). Perform 360 is a NEW backend plane (Brief §7.6).

### §5.2 ThinkLab (Brief §3.2 · 4 destinations · **best-aligned group in the product**)

| Destination | `appOpen` | Status | Route |
| --- | --- | --- | --- |
| Seek Clarity | `clarity` | **W** | `/api/thinklab/*` — Brief §5.3 |
| Develop Strategy | `strategy` | **W** | as above |
| Test Hypothesis | `hypothesis` | **W** | as above |
| Get Perspective | `perspective` | **W** | as above |

Three calls per session: `GET /api/thinklab/config` (all copy — modes, tips, stage labels, outputs, dormant sentence), `POST /api/thinklab/admit` (freeze objective), `POST /api/thinklab/reason` (three Solva stages). Stage mismatch resolved in backend's favour: render 5 stages from `config.stage_labels` (Frame → Name → Challenge → Weigh → Lock-in), never hardcoded, never truncated to 4.

### §5.3 Collab (Brief §3.3 · 4 destinations · **largest wholly-unbacked group**)

| Destination | `appOpen` | Status |
| --- | --- | --- |
| Mentions | `mentions` | **G** |
| Emails | `emails` | **G** |
| Projects/Tasks | `projects` | **G** |
| HR Stuff | `hrstuff` | **G** |

All four render from client-side `COLLAB` map. No mounted router covers messaging, mail, or HR. **Hold or label honestly** in specialist dispatch — needs a backend decision before it can be real.

### §5.4 Manage Estate (Brief §3.4 · 3 destinations · Admin tab)

Registry **W** `/api/registry/*` + `/api/census/*` + `/api/compute/estate` (Brief §5.5). W-REGISTRY-FULL-BUILD CP1–CP9 landed (22 routes wired end-to-end, payload shapes frozen, real-data wires for `opportunity_briefs` + `perception` + `rules_updates/pending`, 78 campaign runs in `/api/model_registry/full_record`); CP10 held pending owner approval (real-Chromium proof + wave-close manifest). Two corrections to Brief §3 verdicts: Signals and Ideas wire to real data (Brief §0.2 §"Two corrections").

### §5.5 Approvals (Brief §3.5 · 3 destinations · Admin tab)

Adjacent to `/api/team/*` per Brief §5.9 (`/api/team/access_register` + `/api/team/constitutional_seats`). **Note (Step 9 crossover):** owner ruling R-23 verbatim keeps these two team endpoints as READ-VIEWS over the new principal store landing at Step 9. Wiring against them today is safe; the read-view shape stays; the source data plane changes underneath at Step 9 seal.

### §5.6 Build Your Resources (Brief §3.6 · 4 destinations · Build tab)

Refer Brief §3.6 for status per destination.

### §5.7 Your Resources (Brief §3.7 · 2 destinations · Build tab)

Refer Brief §3.7 for status per destination.

### §5.8 3rd Party Apps / Integration Console (Brief §3.8 · 4 destinations · own tab)

Internal operator surface for 3rd party integrations. Refer Brief §3.8.

### §5.9 The Watch (Brief §3.9 · 4 destinations · Admin tab · gated by watch-officer role)

State · Record · Under Watch · Decisions per Canon 8 §13 (four app tiles). Renders with Trust shields. Route-level: four single-GET surfaces per Brief §5.7 (Governance / Watch / Grey Mirror / Audit rollups) — cheap once the pattern is set (Brief §8 step 10).

### §5.10 Additional surfaces not in nav (Brief §3.10)

Refer Brief §3.10 for the enumeration.

---

## §6 · Explicitly OUT of card scope

- **§4 DAP (Data Access Portal)** — all of: §4.1 Extract 4 modes · §4.2 request lifecycle (spine + 7 statuses · **largest single gap** in either frontend) · §4.3 Connect Resources · §4.4 Available Resources · §4.5 Data Governance · §4.6 Data Estates. [PENDING RATIFICATION on principal-wave seal]
- **§7.8 DAP workspace API keys + agents.** [PENDING RATIFICATION on principal-wave seal]
- **§7.9 Role gating tied to identity plane.** [PENDING RATIFICATION on principal-wave seal]

---

## §7 · Referenced waves (informational · scope-anchoring only)

- `W-EXECUTIVE-SUITE-v2-LIFT` (L · Board 360 · Exco 360 · Documents · Rule Books · Collab · Spend · Task Manager · Brief §0.2 §"unbacked groups").
- `W-DATA-SUITE-v2-LIFT` (S · Data Suite 3 surfaces).
- `W-TRUST-SURFACE-v2` (S · Trust 2 surfaces).
- `W-REGISTRY-FULL-BUILD` (CP1–CP9 landed · CP10 held pending owner approval).
- DAP-7 of `W-DAP-STACK` (M · mounts `dap_frontend_standalone` per prototype-v3 discipline · [PENDING RATIFICATION on principal-wave seal]).

---

## §8 · Acceptance discipline (Brief §9 · card-scope subset)

A surface is correctly integrated when ALL of these hold:

- Every call is `${REACT_APP_BACKEND_URL}/api/...` (no hardcoded hosts · no skipped `/api` prefix).
- Outer 403 handled: `text/plain` full-surface state, verbatim sentence, no retry, no sign-in.
- Every refusal renders through the single canon refusal card (§2.2 verbatim).
- Empty state renders `honest_gap` verbatim when present.
- Costs never render `$0.00` or blank when `cost_total === null` — render `cost · not yet measured` literal.
- Receipt identities render as chips; receipt content does not appear in the DOM.
- The `credentials: "include"` policy is uniform with the rest of the build.
- No substitution-rule-bound sentence has been reworded without a corresponding update in `notes/v3_substitution_rules.json`.
- No line describes anything as access control that has no identity plane behind it.

---

## §9 · Canon anchors verbatim

- **Canon 5 §9.2** (refusal card copy · binding canon text · §2.2 of Brief reproduces verbatim).
- **Canon 8 §13** (four Watch app tiles: State · Record · Under Watch · Decisions).
- **B-frontends-Q1** owner ruling (STATE/DECISIONS.md:12115): "handoff: yes, gated on frozen contracts. Frontends open when the contracts they consume are frozen under T-b — at minimum the answering-service seam contract (C.17), and DAP's entitlement and receipt contracts."
- **CCS1-C17 · CCS2 DAP entitlement · CCS3 DAP receipt** — three frozen contract pins landed prior to this card: bundle sha `a6107d46…` + `051f25df…` + `81d3c0a5e8e5…`. B-frontends-Q1 contract-pin triple CLOSED.
- **CP-ALPHA-GAP-HARDENING** (this-wave prior seal) — TrustReceiptV1 + OuterGateReceiptV1 promoted to `frozen=True` under SO §3.10-α; runtime mutation raises `pydantic.ValidationError` type `frozen_instance`; zero production mutation-site FINDINGS.
- **Owner ruling 2026-09-06** (STATE/DECISIONS.md near :6336-6360 + :6578) — prototype-v3 binding across the whole design, not just Registry (STEP 5 body verbatim: "Defaults stand: prototype v3 = binding design, Doc 0 v2 = binding"). Errata note: HOLISTIC_PLAN.md §10.2 corrects prior "prototype_v3 binding date 2026-09-06" citation to 2026-09-08T~06:15Z per CP-MECHANICAL-ERRATA-SEAL (`efcfd5d3`).
- **Owner ruling 2026-09-19T~17:54Z** item (e) — "survey now, then closure waves in dependency order — C.17 seam first."
- **Owner ruling 2026-09-20T~08:24Z** — four-artifact drop (FEIB + DAP Backend Engineering Brief + RMS AI Prototype v2 + RMS Data Access Portal); FEIB supersedes the earlier DAP UI Handoff Brief for card drafting purposes.
- **Owner ruling 2026-09-20T~08:56Z** — §2.1 CONFIRMED · OS-prototype frontends card APPROVED to proceed on the OS-prototype surfaces ONLY · DAP portal is OUT of card scope until owner opens it.
- **Owner ruling this-session (`GO — proceed on the plan as written`)** — Step 8 strictly before Step 9 · principal-wave seal is the last gate on DAP portal frontend work · when the principal-wave seals, report prominently (owner two outstanding conditions verbatim: principal-wave seals clean on its own evidence + surface-language trace resolved · trace is resolved-clean at `e099ced1` · wave-seal is the last gate).
- **Step 2 trace verdict at `e099ced1`** (CP-SURFACE-LANGUAGE-TRACE-REPORT) — **PROVENANCE FAULT CONFIRMED (null trace)**; downstream-assumption audit CLEAN across 5 locations. **Step 8 dependence-check GATE CLEAR** on the trace — this card derives cleanly from FEIB + banked owner rulings + Canon 5 §9.2 alone.
- **SO §3.8** thin-kernel additive-only (this card is notes-only additive).
- **SO §4.1 §F** sha-pinning discipline (every source in §1 hash-pinned).
- **SO §6.2** e1_dev drafts cards for M13–M17, memory layer, and frontends from canon and the SER, for batch ratification at the next seal boundary.
- **SO §6.4** NOTHING-BEYOND (scope frozen at OS-prototype surfaces only · DAP portal OUT · scope-cut discipline observed).
- **SO §6.7** sequence-discipline WAVE R-69 Step 8 (Step 8 opens after Step 7 seal · Step 9 last).

**Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.**

---

## §10 · Standing bounds unchanged

zero push · terminal pytest only · no testing_agent · additive-only §3.8 · §4.1 §E · §4.1 §F sha-pinning discipline · three-repo discipline (CODE `programme/track-a` + STATE `master` + POD `main`) · ratchet monotonic (floor **5532** post CP-ALPHA-GAP-HARDENING seal · never rebaselined silently).

---

**End of card. Autopilot next: open Step 9 (PRINCIPAL MODEL WAVE · 13 PRIN requirements RED-first with verbatim docstrings · R-22 90-day rotation DEFAULT-class · R-23 team endpoints as read-views · principal-wave seal is the last gate on DAP portal frontend work per owner directives · interlude marker discipline if budget insufficient · better to interlude at Commit-A boundary than truncate mid-wave).**
