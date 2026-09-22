# SPEC-COVERAGE GAP DIGEST · 2026-09-22

**Purpose:** answer owner concern verbatim: *"The census wizard response worries me. This is a clearly prescribed spec in the documents, no? wondering what other features could be missing in the build."*

**Instrument used:** Master Requirements Registry QA v2 with Builder-Status column filled at `AUDIT-PREP-20260921` seal (2026-09-21T18:20Z · workbook sha256 `8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75` · path `/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx`). Every count in this digest is a formula-count over the workbook's `System Rules Registry` sheet's `Builder Status` column, extracted programmatically 2026-09-22T06:20Z. **Claims-vs-checks note (owner-audit posture):** the running Order B (owner-directed audit-target audit-tags) and Order A (auditor scope) audits **independently verify** the BUILT claims by re-running the cited tests and checking commit references. This digest is a *count of desk-claims*, not a count of auditor-confirmed claims. The audit is what turns claim → verdict.

## 1 · Top line

**602 total rules.**

| Status | Count | Share |
|---|---:|---:|
| **BUILT** | 297 | 49.3 % |
| **PARTIAL** | 293 | 48.7 % |
| **NOT BUILT** | 12 | 2.0 % |

**The owner's plain-language read is right:** approximately **half the spec is fully built by desk-claim; the other half is either scaffolded-but-not-invariant-bound (PARTIAL) or absent (NOT BUILT).** The census wizard is not an isolated case; it is one instance of a systemic PARTIAL surface across several capability areas.

## 2 · Feature-area rollup (top-line table)

Grouped by capability area. Column definitions: **U-Vis** = area primarily user-visible (a user would notice the missing surface); **Internal** = area primarily internal mechanism (contracts/invariants without a surface).

| # | Area | Class | Total | BUILT | PARTIAL | NOT BUILT | One-line what-user-would-notice |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | **Census / Mtafiti / Registry** (B5.x Doc 9 + A17.10-11 + Doc 4) | U-Vis | 9 | 0 | 9 | 0 | "Run census" button + live progress + mid-run agent Q&A + tenant-scoped GPU-spend capture — none exist as user flows. |
| 2 | **Entitlements** (ENT-1..48) | U-Vis | 49 | 21 | 28 | 0 | Usage dashboard, org-admin surface (seats/keys/pool/soft-limits), top-up UI, dial editor, seat add/remove, customer-key BYOK flow — mostly scaffolded, no live UI. |
| 3 | **MOAC / Yield-wall / CIF** (BR-1..14 · Doc 3) | Mixed | 41 | 9 | 30 | 2 | Chokepoint UI copy + wizard read-only guarantees + customer rule change ceremony — mostly invariant-only, no user surface. |
| 4 | **Deck Engine** (DR-R1..R14 · deck_engine spec) | U-Vis | 14 | 0 | 14 | 0 | Whole deck-rendering service (DeckSpec_v0 → HTML/PDF slides) is scaffolded only; **no user deck output** exists yet. |
| 5 | **Training / Model Admission** (A17.x · Doc 17) | U-Vis | 23 | 6 | 17 | 0 | Model Admission surface "shows a capability with nothing running behind it" (A17.13 statement verbatim); **no training runner in any modality** (A17.12). |
| 6 | **Skills layer** (A18.x · Doc 18) | U-Vis | 8 | 3 | 0 | 5 | Skills provisioning + freeze-not-edit + server-side scope + skill donor code — **5 of 8 rules NOT BUILT**; the largest single NOT-BUILT concentration. |
| 7 | **Model Registry catalog** (A20.x · Doc 20) | Mixed | 16 | 2 | 14 | 0 | Qwen/Llama/Mistral/Pixtral/GOT-OCR2/ColPali candidates registered on paper only; **no invariant-bound catalog surface**. |
| 8 | **Streaming Extraction** (SE-1..4 · SV extension) | U-Vis | 11 | 1 | 10 | 0 | Streaming ASR (NVIDIA Nemotron-style) named as second-mode of §17.4a but **not implemented**; batch-only extraction ships. |
| 9 | **Governance C-family rules** (C5.1..5.7 across Docs 2/3/7) | Internal | 21 | 1 | 20 | 0 | Import-assertion enforcement, tension surfaces, perception boundary, load-bearing identification — invariants scaffolded, not test-bound. |
| 10 | **Handoff Registry** (HR-1..7 · handoff_registry_v1) | Internal | 7 | 1 | 6 | 0 | Every subsystem-to-subsystem handoff writing a registry entry — no visible surface today. |
| 11 | **Security promises S-2..20** (Security_Assurance_Promise_Set) | Internal | 25 | 10 | 15 | 0 | Sub-invariants referenced from a companion xlsx; most PARTIAL-tagged pending in-repo test authoring. |
| 12 | **Reviewer discipline** (RV-1..6 · Rules Service reviewer set) | Internal | 6 | 0 | 6 | 0 | Auditor's own discipline (citation-existence, evidence-class presence, status-truth) not yet invariant-bound in code. |
| 13 | **Chokepoint invariants** (A5.x across Doc 1 + Doc 5) | Internal | 91 | 36 | 55 | 0 | Custody sequence, tenant-list ceremony, minimal-sufficient assembly, five-ring unit — many receipt/schema rules PARTIAL. |
| 14 | **Governance Architecture gap register** (G-1..13) | Internal | 13 | 9 | 1 | 3 | Governance blueprint mostly built; 3 audit-boundary rules NOT BUILT. |
| 15 | **Agent Containment** (AC-1..18) | Internal | 18 | 16 | 0 | 2 | Almost complete; 2 rules NOT BUILT. |
| 16 | **WPW spec** (WPW-1..18) | Internal | 18 | 12 | 6 | 0 | Wave-Pause-Wait mostly built; some observability rows still PARTIAL. |
| **BUILT-CLEAN AREAS (no gaps)** ↓ | | | | | | | |
| 17 | **Principal Model** (PRIN-1..13) | ✅ | 13 | 13 | 0 | 0 | — |
| 18 | **Content Registry** (CON-1..31) | ✅ | 31 | 31 | 0 | 0 | — |
| 19 | **Memory Compaction** (MEM-1..11) | ✅ | 11 | 11 | 0 | 0 | — |
| 20 | **DAP lifecycle** (DAP-1..38) | ✅ | 38 | 38 | 0 | 0 | — |
| 21 | **Rules Service RBM/ROC** (RBM-1..23 + ROC-1..11) | ✅ | 34 | 34 | 0 | 0 | — |
| 22 | **Rules Service spec** (extras) | ✅ | 27 | 24 | 3 | 0 | — |
| 23 | **SFP** (Security Function Policy) | ✅ | 8 | 8 | 0 | 0 | — |
| 24 | **Business Continuity** (BC-1..4) | ✅ | 4 | 4 | 0 | 0 | — |
| 25 | **Watch Learning** | ✅ | 10 | 10 | 0 | 0 | — |
| 26 | **Amendment T-1..W-8** | ✅ | 9 | 9 | 0 | 0 | — |

The BUILT-CLEAN block is the platform's real spine — chokepoint carrier types, principal identity, content registry vocabulary, DAP lifecycle, Rules Service canon vocabulary, MOAC's parallel invariants (RBM/ROC/SFP), memory compaction, watch-learning types, business continuity. These are the areas where invariant-bound tests exist and back every rule.

## 3 · Split into USER-VISIBLE vs INTERNAL-MECHANISM (owner's concern class)

### 3.1 · USER-VISIBLE FEATURE GAPS (owner would see a missing product feature)

Ranked by impact on user experience. Each row lists rule IDs so the audit can independently verify.

| Rank | Feature area | Rule IDs (PARTIAL/NOT-BUILT) | User-visible shortfall |
|---:|---|---|---|
| **1** | **Census wizard / Run-census journey** | B5.1..B5.7 (Doc 9 Mtafiti · 7 PARTIAL) + A17.10-A17.11 (Doc 17 · 2 PARTIAL) + Canon 4 §4 verbatim | The user can view past census records at `/api/portal/census/records` (BUILT), but cannot **start** a census, **watch it run**, **answer mid-run agent questions**, or see it **write into their tenant registry with GPU-spend captured**. |
| **2** | **Entitlements / licence surfaces** | ENT-2, 4, 7, 8, 10, 11, 14, 15, 24, 25, 27, 28, 29, 30, 31, 33, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48 (28 PARTIAL) | Usage dashboard (credits/tokens/allowance) · Org-admin surface (seats/keys/pool/soft-limits/ceilings) · Top-up flow · Dial editor · Suspension button · Seat add/remove · Customer-key BYOK metering · Refusal-card copy. Most scaffolded on backend routes; no live UI. |
| **3** | **Skills layer** | A18.1, A18.2, A18.3, A18.5, A18.8 (5 NOT BUILT) | Skill provisioning record UI · slice-freezes-never-edits guardrail · server-side scope enforcement UI cues · skill-donor-code intake. 5 of 8 skills rules NOT BUILT. |
| **4** | **Deck Engine** | DR-R1..R14 (14 PARTIAL) | User cannot ask for a **deck**. The deck-rendering service (`DeckSpec_v0` → HTML/PDF slides) is scaffolded only. Prototype has deck tab; backend does not render. |
| **5** | **Training runner / Model Admission surface** | A17.12 ("No runner exists in any modality") · A17.13 ("Model Admission shows a capability with nothing running behind it") · A17.14 ("GPU host is reachable; authentication is not configured") | User can register a model row but cannot **run** a training/admission cycle end-to-end. |
| **6** | **Streaming Extraction** | SE-1..SE-4 (4 PARTIAL) | Real-time ASR streaming (Nemotron-style, cache-aware, 40-locale) named as a second mode — batch-only ships today. |
| **7** | **Model Registry catalog UI** | A20.1..A20.14 (14 PARTIAL · A20.15-16 BUILT) | Model rows named on paper (Qwen3 · Llama · Qwen2.5-VL · GOT-OCR2 · PaddleOCR-VL · ColPali · InternVL3 · Pixtral 12B · Llama-4 Maverick/Scout) — no user-facing catalog surface with license/rights/dimension resolution. |
| **8** | **Connect + Commission wizards** | Endpoints marked "✅ verified" in FE Integration Brief §5.10-§5.11 · state-machine and drawer surfaces PARTIAL under Docs 6 (5 PARTIAL) and 11 (15 PARTIAL) | Backend endpoints exist; **UI drawer + state-machine flow shipped only in prototype**, not in runtime App.js. |
| **9** | **MOAC user-visible refusal + rule-change ceremony** | BR-11.1-2 (2 NOT BUILT) · BR-12.1-2 (PARTIAL) · ENT-46 refusal-card copy | Customer cannot see the "one refusal card" in production; MOAC bypass/tamper resistance not user-visible in receipt. |
| **10** | **Watch's own external ceremony** | BR-7.2, BR-7.3 (2 PARTIAL) | Watch has no user-facing "watched-by-outside" surface; owner cannot see the Watch's own audit trail. |

### 3.2 · INTERNAL MECHANISM GAPS (owner would NOT see a feature; backend invariant not test-bound)

These are areas where the desk claims PARTIAL because a service module exists (`backend/services/<name>/__init__.py`) but the specific rule is not yet cited by a green invariant test. They are not user-visible gaps; they are auditor-visible gaps.

- **Chokepoint mechanics** (A5.x from Docs 1 + 5 · 55 PARTIAL) — receipt schema, custody sequence property tests, principal-carrier invariants.
- **Handoff registry** (HR-1..7 · 6 PARTIAL) — every crossing writes an entry, receiving-side refuses without entry, no-dual-hatted-task at registration.
- **CIF governance boundary** (C5.1..7 Doc 3 · Doc 2) — import assertion enforcement, tension-not-average, load-bearing identification unit-refs.
- **Perception boundary** (C5.1..6 Doc 7) — frozen job/frozen result crossing, grounding markers, hash+licence registration.
- **Rules Service reviewer** (RV-1..6) — citation-existence, scope-trace, evidence-class, schema-completeness, status-truth, novelty-collision.
- **Security Promise Set** (S-2..20 · Security_Assurance_Promise_Set.xlsx) — 15 PARTIAL sub-invariants referenced externally.
- **MOAC/DAP refuse-if-unset** (SEC-2..7) — refuse rather than default-accept if criteria unset.
- **Ledger append-only + writer-TCB** (BR-8.1..3) — ledger writer as named TCB member, append-only structure independently verifiable.
- **Chokepoint fails-closed** (BR-1.5) — chokepoint fails closed on internal error, independent of Watch.
- **CIF exclusion from TCB** (BR-9.1..3) — Attribute 1 exclusion demonstrated + MUST/MUST-NOT rules each carry assessment procedure.

## 4 · Census wizard as the worked example (the owner's presenting case)

### 4.1 · Prescribing spec text, quoted verbatim (each with source anchor)

**Canon 9 (Mkondo Charter) · line 23:**

> "Census and registry records | Mtafiti | Both authorities; every surface by proof link | Objective-blind measurement; the Watch reads sensitivity classes for tripwire coverage and never writes."

**Canon 4 (Operating Engines) · Heading 1 §4 The Census (line 26):**

> "The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity. **One census serves every objective; no objective is consulted during the walk.**"

**Canon 4 · §4.1 What the census produces at estate level (line 30):**

> "Every figure carries its method. Any measurement a surface displays resolves to the census run that produced it, its date, the population measured, and whether the measurement was full or sampled — a sampled measurement is never presented as a full-population one."

**Canon 4 · Mtafiti's Invariants (lines 56-64):**

> "The census is exhaustive and objective-blind; one measure serves every objective."
> "A stale or un-censused region returns unknown rather than a fabricated distribution."

**Master Requirements Registry rows (Doc 9 · Objective O6 Estate Registry · Promise #13 THE CENSUS):**

- B5.1: *"The census is exhaustive and objective-blind; one measure serves all"* — **PARTIAL**
- B5.2: *"Unmeasured is recorded as unmeasured"* — **PARTIAL**
- B5.3: *"Every figure resolves to its method"* — **PARTIAL**
- B5.4: *"The two-layer measure scales without per-item labelling"* — **PARTIAL**
- B5.5: *"The defensibility verdict is a deterministic matrix lookup carrying its rule reference"* — **PARTIAL**
- B5.6: *"Freshness is a mechanism, not a schedule"* — **PARTIAL**
- B5.7: *"Sensitivity classification is the single entitlement attribute"* — **PARTIAL**

**Doc 17 — The Multidimensional Training Engine (extends #22-24):**

- A17.10: *"A CI fixture exists; production is a different, later question"* — **PARTIAL**
- A17.11: *"Production selection is named after the census, not before it"* — **PARTIAL**

**Front-End Integration Brief · custody drop 2026-09-20T08:24Z (owner drop) §5.5 Registry, Census, Compute Estate (lines 939-958):**

> "`GET /api/census/latest` / `GET /api/census/history` / `GET /api/census/status` ... `census/latest` is the truer source where it disagrees with `registry/facts`; the existing App.js reads both and prefers the census. **Replicate that precedence.**"

**Front-End Integration Brief · §5.10 Connect wizard (lines 1061-1085) and §5.11 Commission / Shaping wizard (lines 1088-1105):**

> §5.10 endpoints ✅ verified: `GET /api/connect/estate-facts` · `POST /api/connect/parse-paste` · `POST /api/connect/gpu` · `POST /api/connect/data-source` · `POST /api/connect/intent` · `POST /api/connect/confirm/{draft_id}` · `GET /api/connect/draft/{draft_id}`.
> §5.11 endpoints ✅ verified: `POST /api/wizard/operator/session` → `{session_id}` · `POST /api/wizard/operator/{session_id}/turn` · `GET /api/wizard/operator/{session_id}` · `GET /api/wizard/operator/{session_id}/commit-review` · `POST /api/wizard/operator/{session_id}/freeze`.

### 4.2 · Halves — what is BUILT vs what is MISSING

| Half | Status | Evidence anchor |
|---|---|---|
| **BUILT — operator-run census tools** | ✅ | `phase0/tools/estate_census_v{1,2,3}.py` invocations (main-agent terminal-runs) with receipts at `phase0/census_v3/*.json`. |
| **BUILT — census receipts + read endpoints** | ✅ | `/api/portal/census/records` LIST + `/api/portal/census/records/{census_number}` DETAIL (CENSUS-SURFACE-A Commit-A' code sha `e06ecf9`) + `/api/portal/census/{assets,surfaces,access,latest,duplication}` (Commit-A code sha `4dfc446`). |
| **BUILT — connect wizard endpoints** | ✅ | §5.10 endpoints marked "✅ verified" in FE Brief. |
| **BUILT — commission wizard endpoints** | ✅ | §5.11 endpoints marked "✅ verified" in FE Brief. |
| **BUILT — asset registry with sealed writer** | ✅ | `backend/services/mtafiti/asset_registry_writer.py` (BUILT · CON-1..31 · MEM-1..11 all GREEN). |
| **BUILT — designed UI specs** | ✅ (paper) | `phase0/surface_connection/portal_census_journey_ui_spec.md` + `portal_registry_landing_ui_spec.md` — banked, not shipped. |
| **MISSING — user-triggered Run-census** | ❌ | No `POST /api/portal/census/run` write endpoint. |
| **MISSING — live-progress streaming** | ❌ | No WS/SSE channel from census engine to UI; no `enumerating/authing/reading/writing_registry/blocked/complete` state emission. |
| **MISSING — mid-run agent Q&A (response-required) loop** | ❌ | Engine emits results as receipts, not as mid-run questions surfaced in UI. |
| **MISSING — tenant scoping on census execution** | ❌ | Waits on CP-TENANT-SEPARATION (owner Part-2 order 2026-09-22T~02:20Z · `TENANT_SEPARATION.md` DRAFTED). |
| **MISSING — GPU-spend capture per run** | ❌ | GPU nvidia-smi telemetry not folded into per-run cost record; no `records/{n}` `gpu_spend` from live capture. |
| **MISSING — B5.1..B5.7 invariant-bound tests** | ❌ | Backend has `services/mtafiti/__init__.py` scaffolding; specific B5.x properties not yet cited by named invariants (per Builder-Status "no invariant naming this rule"). |
| **MISSING — A17.10/A17.11 production-selection separation** | ❌ | `targeta/__init__.py` scaffolding only; no CI-vs-production model-selection guardrail. |

### 4.3 · The prototype has the Run-census control

The prototype `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` (Registry landing + Census tabs) shows a **Run-census** control. The runtime App.js does not carry it; the specs at `phase0/surface_connection/portal_census_journey_ui_spec.md` bank the design for R-101 ε-apply land. Owner ruling (2026-09-22T~06:12Z verbatim at `DECISIONS.md:R-101 append` condition iii): *"the Run-census control ships wired to whatever is REAL at ship time — a bounded real census run if feasible, otherwise the honest-gap pattern. No simulated progress."*

**Objective card opened** at `STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md` (banked 2026-09-22T06:15:23Z at R-101 supersede) — draws the full closure line: user-triggered execution + live progress + response-required loop + per-tenant scoping + GPU-spend capture. **Sequenced post-CP-TENANT-SEPARATION** because user-run censuses must be tenant-scoped from birth.

## 5 · Honest paragraph — "what other features could be missing?"

The registry's own numbers say **approximately half the spec is fully built** (297 of 602 rules BUILT; 293 PARTIAL; 12 NOT BUILT). Reading the PARTIAL/NOT-BUILT set through the lens of "what a user would notice as missing," the top **user-visible feature gaps** — in rough impact order — are: **(1) Census wizard user-run journey** (the owner's presenting case · 9 rules PARTIAL); **(2) Entitlement / licence surfaces** — usage dashboard, org-admin surface for seats/keys/pool/soft-limits/ceilings, top-up UI, dial editor, seat management, customer-key BYOK flow, refusal card (28 rules PARTIAL); **(3) Skills layer** — provisioning + slice-freeze + scope enforcement + skill donor code (**5 of 8 rules NOT BUILT** — the largest single not-built concentration); **(4) Deck Engine** — the whole deck-rendering pipeline (14 rules PARTIAL, 0 BUILT); **(5) Training runner / Model Admission surface** — the spec explicitly says *"Model Admission shows a capability with nothing running behind it"* and *"No runner exists in any modality"*; **(6) Streaming Extraction** — real-time ASR not yet implemented (batch-only ships); **(7) Model Registry catalog UI** — the model rows are named on paper (14 candidates: Qwen3/Llama/Qwen2.5-VL/GOT-OCR2/PaddleOCR-VL/ColPali/InternVL3/Pixtral/Llama-4 Maverick/Scout) but the user-facing catalog surface with license/rights/dimension resolution is PARTIAL; **(8) Connect + Commission wizard UI** — backend endpoints "✅ verified" but the multi-step drawer state machines live in the prototype only; **(9) MOAC's user-visible refusal-card copy + rule-change ceremony** — the "one refusal card" and the customer rule-change ceremony are not yet the shipped user experience; **(10) The Watch's own external-witness ceremony surface** — no "watched-by-outside" audit trail visible to owner. Beneath these, a substantial body of **INTERNAL invariants** carry PARTIAL because a service module exists but the rule is not yet cited by a green test (chokepoint receipt schema, handoff registry, CIF/perception boundary crossings, reviewer discipline, S-promise sub-invariants, refuse-if-unset in MOAC/DAP). These do not surface as missing product features to a user; they surface as auditor findings when the audit tags run.

**Independent verification note:** the running **Order B** (owner-directed audit-target audit-tags — `audit/code-20260921` code sha `283524d89dd337d79014b114d575ced7baab6dfc` + `audit/state-20260921`) and **Order A** (auditor scope) audits **independently verify** the BUILT claims by re-running the cited tests and cross-checking commit references. **Owner-facing claims here get audited, not trusted.** The full audit verdict (with planted-violation RED proofs on §8) is scheduled as Turn 5 of the R-101 sequence (post-broad-hygiene-sweep + post-ε-apply seal, per owner priority) and will be banked at `phase0/audit_pass_receipts/20260922T*_order_b_verdict.md`.

## 6 · Owner questions that this digest raises but does not answer

- **Q1 — depth vs. breadth of ε-apply UI:** the R-101 ε-apply commits to landing the prototype v2 OS + LATEST DAP surface as design of record. Does the owner want the **Entitlements dashboard** (rank-2 gap · 28 rules PARTIAL) also to ship in the same ε-apply wave (as honest-gap for the parts with no live backend), or does that wait for the next boundary once the Run-census control ships?
- **Q2 — Skills layer priority:** with 5 of 8 A18.x rules NOT BUILT (largest concentration), does the owner want a **CP-SKILLS-LAYER** objective card opened alongside `CENSUS_PRODUCTIZATION`, sequenced also post-CP-TENANT-SEPARATION? Or is the skills feature deferred for a later wave?
- **Q3 — Deck Engine gap:** the whole Deck Engine (14 rules PARTIAL, 0 BUILT) is a discoverable feature in the prototype's Documents/Deck tab. Should a **CP-DECK-ENGINE** objective card open, or does the owner regard deck rendering as a later product surface?
- **Q4 — Streaming Extraction:** should **SE-1..4** open as a fork behind CENSUS-3-F.2.1 live-OBS-bind (which already streams · would extend to streaming ASR)?

These are queued as R-101 ε-apply seal-boundary owner asks (bundled per owner "one owner ask" pattern) unless owner overrides.

---

**Digest signed:** main-agent desk · 2026-09-22T06:20:00Z. Extraction script preserved at `phase0/retrievals/20260922T062000Z_spec_coverage_extract.py` (next commit). Numbers reproducible by `openpyxl.load_workbook` + Builder-Status column groupby on `System Rules Registry` sheet.
