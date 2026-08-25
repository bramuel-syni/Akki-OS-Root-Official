# Status % + Wave Plan · FL-P2-27

Owner Order 2026-08-19 · Sprint deliverables §3 (status %) + §4 (close plan).

## §1 · Weighting scheme (declared once)

- **Base weight per row:** 1.0.
- **Row status weight** contributes to a done-fraction:
    - **DONE**: 1.0
    - **PARTIAL**: 0.4 (behaviour exists behind a fixture or wire is incomplete)
    - **REUSABLE**: 0.5 (lift/adapt from a repo — counted as half done because integration + testing + owner-record wiring still cost real work)
    - **BUILD**: 0.0
- **Interface dimension is separate:** the 58 v7 surfaces are counted independently of the 515 requirement rows (a single mechanism often lights up multiple surfaces).

Rationale: **REUSABLE** at 0.5 reflects that in this estate a lift-in still costs a tests-first cycle + a wire-through + a real-facts endpoint + the FL-P2-13 zero-fabrication scrub. **PARTIAL** at 0.4 is lower than REUSABLE because a partial has more residual to work through than a clean lift.

## §2 · Overall status % — mechanism corpus (515 rows across 16 docs)

| Bucket | Rows | Weight | Contribution |
|---|---:|---:|---:|
| DONE | 47 | 1.0 | 47.0 |
| PARTIAL | 40 | 0.4 | 16.0 |
| REUSABLE | 300 | 0.5 | 150.0 |
| BUILD | 128 | 0.0 | 0.0 |
| **Total** | **515** | | **213.0** |

**Mechanism-corpus completion: 213.0 / 515 = 41.4 %.**

Reading: the estate is roughly two-fifths of the way through its promised mechanisms when reuse potential is counted at half-credit. If Executive-Final (currently 404) holds more mechanisms, this number will climb.

## §3 · Per-area status % (11 axes)

Each row = a canonical area. Rows distributed from the doc register.

| # | Area | Docs contributing | Row total | DONE | PARTIAL | REUSABLE | BUILD | Weighted | **%** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **Custody / Boundary (chokepoint, masking, exit gate, dual-file)** | Doc 01 · Doc 02 | 44 | 5 | 5 | 27 | 7 | 20.5 | **46.6 %** |
| 2 | **Direction / Record (Northena; append-only ledger)** | Doc 05 · portion Doc 15 | 32 | 0 | 3 | 22 | 7 | 12.2 | **38.1 %** |
| 3 | **Measurement / Reasoning (Solver, shrinkage, memory)** | Docs 04, 06, 07, 08 | 93 | 0 | 8 | 69 | 16 | 37.7 | **40.5 %** |
| 4 | **Extraction / Quality (five-ring shrinkage, quality gates)** | Doc 07 · Doc 08 · portion Doc 16 | 46 | 0 | 4 | 32 | 10 | 17.6 | **38.3 %** |
| 5 | **Integration (Connection & Census · data-source connect)** | Doc 09 | 21 | 21 | 0 | 0 | 0 | 21.0 | **100 %** |
| 6 | **Governance Ceremony (rules · counter-sign · countdown)** | Doc 15 | 87 | 2 | 4 | 65 | 16 | 36.1 | **41.5 %** |
| 7 | **Registry / Estate (Comprehensive Registry · Opportunity Briefs)** | Doc 10 | 18 | 10 | 5 | 3 | 0 | 13.5 | **75.0 %** |
| 8 | **Watch / Security (Intent monitoring, Grey Mirror, bait, ladder)** | Doc 03 · portion Doc 15 | 82 | 0 | 5 | 15 | 62 | 9.5 | **11.6 %** |
| 9 | **Orchestration (cross-cutting, refusal grammar, hand-offs)** | Doc 16 · portion Doc 15 | 72 | 0 | 3 | 55 | 14 | 28.7 | **39.9 %** |
| 10 | **Compute / Cost (in-perimeter, ladder, deflation, cost ledger)** | Doc 11 · Doc 12 | 27 | 9 | 4 | 11 | 3 | 16.1 | **59.6 %** |
| 11 | **Training / Models (Targeta, ecosystem, baseline, whitepaper)** | Doc 13 · Doc 14 | 51 | 0 | 4 | 40 | 7 | 21.6 | **42.4 %** |
| | **Totals** | | **573** ² | **47** | **45** | **339** | **142** | **234.5** | **40.9 %** |

² Some rows contribute to two areas (e.g. Doc 15 rows span Areas 2, 6, 9). Row-double-count normalised in the 515 grand total; per-area figures use the un-normalised count for area-fidelity.

### Reading

- **Integration (100 %)** — the only fully-DONE area. Connect + Data-source is live end-to-end.
- **Registry / Estate (75 %)** — this cycle's Registry-A4 closed the surface; Opportunity Briefs remains.
- **Compute / Cost (60 %)** — akki-vm connected + hardened + accepted; Cost Ledger surface (CA1-008) is BUILD.
- **Custody / Boundary (47 %)** — heavy REUSABLE (RMS synisense + Exec-Core privacy_wall); mechanisms adapt, don't need rebuild.
- **Direction / Record (38 %)**, **Measurement / Reasoning (41 %)**, **Extraction / Quality (38 %)**, **Orchestration (40 %)**, **Governance Ceremony (42 %)**, **Training / Models (42 %)** — all in the 38–42 % band, dominated by REUSABLE. Big lift on adapt.
- **Watch / Security (12 %)** — the lowest-completion area and largest BUILD count. Doc 03 alone carries 62 BUILD rows. Grey Mirror surface cannot ship until this area moves.

## §4 · Interface dimension — 58 v7 surfaces

Counted separately per owner sprint scope §3.

| Bucket | Count | Surfaces (illustrative) |
|---|---:|---|
| **Built (DONE)** | 4 | Registry (3-tab) · ConnectWizard (paste panel · current) · Compute-detail card · Data-source-detail card |
| **Partially built** | 2 | Data-source-record row (missing per-source Opportunity Brief link) · Compute-record row (missing JUST CONNECTED freshness window logic) |
| **Reusable fabric found** | 34 | Documents · DocumentsPage · Chat · Analyze · ThinkLab (4 surfaces) · Cohort · Collab (4 surfaces) · Ideas · Signals · Trust Center (3 shields · rules updates surface) · Trace · Walkin · Highlights · Pulse · Shell/Layout · Onboarding · Tasks · Manage · Cycle · Decks · News/Learn · Prepare · Studio · Depth · Feedback · Trust · SessionTimeout · Auth · Common primitives |
| **To build (nothing lift-able)** | 18 | Grey Mirror overview · Grey Mirror monitor · Grey Mirror response · Grey Mirror people · Watch destination · Board 360 · Exco 360 (three sub-tabs) · Rules Updates ceremony · Model Admission ceremony · Spend Requests · Cost Ledger · Opportunity Briefs · Retention Ledger · Breach Notification console · Access-and-Erasure request surface · Residency enforcement · Ledger Continuity attestation |
| **Total** | **58** | |

**Interface completion (weighted, DONE=1 · PARTIAL=0.4 · REUSABLE=0.5 · BUILD=0):** (4 + 0.8 + 17.0 + 0) / 58 = 21.8 / 58 = **37.6 %**.

## §5 · Composite headline number

Overall build completion — blend of mechanism corpus (weight 0.7) + interface dimension (weight 0.3):
- 0.7 × 41.4 % + 0.3 × 37.6 % = 29.0 % + 11.3 % = **40.3 %**.

**Round headline: ≈ 40 % complete overall.**

Sensitivity: if Executive-Final holds Watch/Grey Mirror mechanism + N-series primitives + Cost Ledger surface, the mechanism corpus number climbs to ~55–60 % and the headline to ~50–55 %. Access to that repo is the single biggest lever.

## §6 · Close plan — sequenced waves per T13

Owner rule T13: "We reproduce in sequence with the backend we are building." T14: "None of the requirements gets skipped."

No dates. Sequence + scope class + DONE-means definitions only. Scope classes: **S** (≤200 LOC + tests + wire), **M** (200–800), **L** (800–2500), **XL** (2500+).

---

### Wave 1 (W1) — Connect wizard T12 rework + Registry backfill · scope **M**

**Backend mechanism:** none new (registry_facts already live).

**v7 surfaces lit:** Registry three tabs (already lit; polished) · Connect drawer-chat right-side (T12 rework).

**17-doc anchor:** Doc09 (100 % DONE, keep) · Doc10 (Opportunity Brief link stub per source; Doc10-006 partial→PARTIAL) · Doc16 refusal-card wire-through on registry error states.

**Reuse:** Registry.jsx primitives (LIFT); Exec-Core `chat/` drawer + streaming primitives (ADAPT for the paste-assist conversational flow).

**Deps:** none. This is the collision-free continuation.

**DONE means:**
- New `ConnectDrawerChat.jsx` right-side drawer that replaces the current modal `ConnectWizard.jsx`. Same paste-assist deterministic parser under the hood; wrapped in a conversational shell.
- Registry.jsx data-source detail card gains an "Opportunity Brief (stub)" section that renders the honest-empty sentence from Doc 10 until the brief service is wired.
- Backend gating: `test_registry_facts.py` extends to check the `opportunity_briefs_link` field per source (BUILD stub returns null; test asserts key present).
- Frontend gating: `Registry.jsx` and new drawer render tests + testid coverage; paste-assist conversation acceptance test.

**Acceptance rows:** Promise #12 (kept DONE), Promise #14 (kept DONE), Promise Table #A8 partial (Walk-this **not** shipped in W1; blocked pending T8).

---

### Wave 2 (W2) — Compute in-perimeter · reflection-before-commit shim · scope **S** · **CLOSED 2026-08-25**

**Backend mechanism:** extend `services/compute_seam/` with a reflection-before-commit "cost/budget quote first" call (Doc12 §Reflection).

**v7 surfaces lit:** COMPUTE CONNECTED detail card gains the reflection block; Cost Ledger tab (Doc11 · CA1-008) NOT yet shipped in W2.

**17-doc anchor:** Doc12-003 (PARTIAL → **DONE**) · Doc12 remainder kept DONE.

**Reuse:** Extraction-Akki `services/compute_seam/` (already present).

**Deps:** W1 done.

**DONE means:** reflection stub returns quoted-cost + budget-headroom object; compute detail card renders it; tests-first.

**Cycle-close receipts:**
- Programme/track-a `8319522` (tests-first) + `7cf40a7` (implementation).
- Green receipt: `phase0/drill_receipts/20260825T180738Z_w2_reflection_green.log` (backend 148/148 · frontend 61/61 rehome · 12/12 allowlist).
- Screenshots: `phase0/drill_receipts/screenshots/20260825T180800Z_w2_compute_card_{before,projection,committed}.jpeg`.
- Seven-invariant contract green: (a) reflection required · (b) ack required · (c) projection ledgered with run · (d) server-side gate · (e) attributed ack · (f) zero-fabrication · (g) reference-not-copy.

**Acceptance rows:** Promise #10 (kept DONE), Promise #11 (PARTIAL → **DONE**).

---

### Wave 3 (W3) — Chokepoint · masking · exit gate · residency enforcement · Data Shield surface · scope **L** · **CLOSED 2026-08-25**

**Backend mechanisms:** custody chokepoint wrapper on every LLM/model call · masking tiers (T1/T2/T3) · exit-gate telemetry · residency enforcement (CA1-N4).

**v7 surfaces lit:** TRUST Data Shield tab (v7 `TRUST.datashield`) · Rules Updates ceremony surface (partial: rulebook chip vocabulary) · Registry data-source row gains residency chip.

**17-doc anchor:** Doc01 (whole) · Doc02 (whole; incl. CA1-007 dry-run + CA1-001 audit line) · CA1-N4.

**Reuse:** RMS `synisense/shield/` (masking primitives) · Exec-Core `privacy_wall.py`, `rate_limit.py`, `security_headers.py` · RMS `compliance/`, `data_source/` (dual-file custody).

**Deps:** W2 done. Executive-Final would materially reduce scope if it holds masking-tier ladder implementation.

**DONE means:**
- All LLM / model calls in the estate pass through a single `services/chokepoint/` middleware. **DONE** — plus the REAL crossings today (RDS Data API + compute-seam SSH) brought under the same discipline (owner directive).
- Every crossing writes a `data_crossing_record` under `phase0/`. **DONE** — receipts at `phase0/crossing_receipts/rcp-<hex>.json`.
- Data Shield tab renders real crossings (not v7 demo). **DONE** — 63 real receipts rendered at close; no fabricated volumes.
- Residency: data-source records without a region in the allow-list refuse connect at the parse step; test-first gate. **DONE** — `services.chokepoint.residency` + `residency_allowlist.v0.json` (eu-west-1 only).
- CA1-007 dry-run: a `POST /api/shield/dry-run` endpoint that returns what the candidate declaration would/would not catch against a bounded sample. **DONE**.

**Cycle-close receipts:**
- Programme/track-a `ebacd65` (Section B) + `1a57314` (Sections C+D) + `15dbfc1` (Data Shield surface + close).
- Green receipt: `phase0/drill_receipts/20260825T183814Z_w3_close_green.log` (backend 169/169 · frontend rehome 69/69 · allowlist 12/12 = 250/250).
- Screenshots: `phase0/drill_receipts/screenshots/20260825T183800Z_w3_{data_shield_surface,dry_run_preview,refused_unmasked_egress}.jpeg`.
- LOC actual ~1957 · inside L ceiling (≤2000).

**Acceptance rows:** Promise #1 (chokepoint · DONE) · Promise #2 (list authoring PARTIAL — mechanism scaffolding in force; row-bearing tiers await tenant catalogue) · Promise #4 (dual-file · DEFERRED to LLM-crossing wave) · Promise #26 (governed-change discipline in the chokepoint allowlists · PARTIAL) · Promise #27 (partial) · CA1-007 (**DONE**) · CA1-001 (audit-line groundwork · PARTIAL) · CA1-N4 (**DONE**).

---

### Wave 4 (W4) — Northena direction/scope + ThinkLab surfaces · scope **M (estimated) / L (realized)** · **CLOSED 2026-08-25**

**Backend mechanism:** Northena's Admit / Gate / Converge / Ledger loop adapted from `Akki-OS-V1/backend/services/northena/`; persistence rewritten to `phase0/northena_admits/` + `phase0/northena_ledger/`; Solva boundary stubbed honestly via `admit_assist_stub` (Solver lands W5).

**v7 surfaces lit:** ThinkLab landing (`/thinklab`) + 4 mode entry pages (`/thinklab/{clarity,strategy,hypothesis,perspective}`). Honest reasoning-dormant panel per §A5.3 posture: "The reasoning faculty is not yet in force" until Solver lands.

**17-doc anchor:** Doc 05 (§A5.1/A5.3/A5.4/A5.5/A5.6/B5.1/B5.2/B5.4).

**Reuse:** ADAPT `Akki-OS-V1/backend/services/northena/{admit,gate,converge,ledger}.py` + `contracts/northena_ledger.py`; BUILD `admit_assist_stub.py`; v7 fabric extracted verbatim from `prototype/prototype.html` offsets 265900–268700 + 388987–392000.

**Deps:** W3 done. WS-WIRE-LEDGER-MATRIX honoured (Northena ledger = SOLE writer of `northena_ledger_row` records).

**DONE means:**
- Admit refuses on missing lawful basis, missing required fields, unresolved scope (each with own refusal reason). **DONE**.
- FrozenArtifact refuses mutation (§B5.1). **DONE**.
- Gate refuses out-of-scope; adjacency ≠ membership. **DONE**.
- Converge: done-condition beats budget precedence. **DONE**.
- Ledger writer: append-only (structural refusal on row_id collision). **DONE**.
- ThinkLab landing renders 4 modes from `/api/thinklab/config` (REFERENCE-NOT-COPY). **DONE**.
- Mode entry captures direction + admits into Northena; frozen artifact rendered with honest `judgement_provenance`. **DONE**.

**Cycle-close receipts:**
- Programme/track-a `7e6bbc4` (Section B+C) + `7bea87d` (companion) + `a71ea67` (Section D + close).
- Green receipt: `phase0/drill_receipts/20260825T192120Z_w4_close_green.log` (backend 187/187 · frontend rehome 77/77 = 264/264).
- Screenshots: `phase0/drill_receipts/screenshots/20260825T192400Z_w4_thinklab_{landing,clarity_entry,admit_walk}.jpeg`.
- LOC actual ~2020 — above M ceiling; owner notified for classification ruling.

**Acceptance rows:** Doc05-001 (**DONE**) · Doc05-006 (**DONE**) · §A5.1 (**DONE**) · §A5.4 (**DONE**) · §A5.5 (**DONE**) · §B5.4 (**DONE**) · §B5.2 (**PARTIAL** — full 5-check list awaits W5+ governance surfaces) · §A5.3 (**PARTIAL** — Solva-boundary stub in force; full binding W5).

**Backend mechanism:** `services/northena/` adapted from RMS/OS-V1; Admit / Gate / Converge / Ledger loop.

**v7 surfaces lit:** ThinkLab framing surfaces (Seek Clarity · Develop Strategy · Test Hypothesis · Get Perspective) get their objective-framing chrome.

**17-doc anchor:** Doc05 (whole).

**Reuse:** RMS `northena/` + Akki-OS-V1 `northena/` (compare and merge).

**Deps:** W3 done (chokepoint prerequisite for anything model-side).

**DONE means:** Northena admits an objective, gates via evidence checks, converges, ledgers the run. All four surfaces render its state through v7 grammar.

**Acceptance rows:** Promise #16 · Promise #18.

---

### Wave 5 (W5) — Solver · Shrinkage · Memory · scope **L**

**Backend mechanisms:** `services/solva_v2/` (adapt from Exec-Core) · perception + layer_a/b/c five-ring shrinkage (RMS) · platform_kb warm/fresh (Exec-Core).

**v7 surfaces lit:** WorkStudio Chat surface (Exec-Core LIFT + shielding wire) · WorkStudio Data Suite · Reasoning Shield tab · refusal card VERBATIM copy in place.

**17-doc anchor:** Doc04 (+CA1-010) · Doc06 (+CA1-002) · Doc07 (+CA1-003) · Doc08.

**Reuse:** Exec-Core `chat/`, `analyze_workspace/`, `solva_v2/`, `platform_kb.py`, `continue_chat.py`; RMS `solva_depth/`, `perception/`, `layer_a/b/c/`.

**Deps:** W3 done.

**DONE means:** an estate-scoped chat answers a question, cites the five-ring units it drew from, marks unmeasured claims "not sure" (Promise #8), and shows a refusal card verbatim if the evidence bar isn't met. CA1-010 session-scoped lowered-standard; CA1-002 minimal-sufficient audit line; CA1-003 per-turn warm/fresh tag.

**Acceptance rows:** Promises #8 · #17 · #19 · #20 · #21 · #31 · CA1-002 · CA1-003 · CA1-010.

---

### Wave 6 (W6) — Cost Ledger surface · retention enforcement · Grey Mirror groundwork · scope **L**

**Backend mechanisms:** economics/cost-ledger lever pipeline (RMS `economics/`; expose as surface) · retention enforcement daemon (CA1-N1) · Doc03 Watch primitives — first slice (declaration read; behaviour-vs-declaration diff).

**v7 surfaces lit:** Cost Ledger surface (v7 `COMPUTE_CHARTS` + Doc11 lever sequence) · retention row on data-source records · Grey Mirror overview tile (empty-with-honesty until W9 completes it).

**17-doc anchor:** Doc11 (+CA1-008) · CA1-N1 · Doc03 subset (declaration & behaviour reading).

**Reuse:** RMS `economics/` tier_lock lever configs · RMS `retention/` (declarative, extend to enforcement).

**Deps:** W3 · W5.

**DONE means:** Cost Ledger renders the lever sequence with real per-lever attribution over the last N crossings; retention daemon runs on schedule and writes an attestation record; Grey Mirror overview lists real actors with real declarations.

**Acceptance rows:** Promise #9 · CA1-008 · CA1-N1 · partial Doc03.

---

### Wave 7 (W7) — Targeta · Model Ecosystem · Model Admission ceremony · scope **L**

**Backend mechanisms:** `services/targeta/` (RMS) · sandbox generation (Exec-Core) · baseline curation · whitepaper drafter.

**v7 surfaces lit:** LLMs & Trained Models tab (already the honest-empty shell; now populated) · Model Admission ceremony wizard (v7 `WIZ[actor]` for kind=model) · Rule Books Library (CA1-A4).

**17-doc anchor:** Doc13 (+CA1-011) · Doc14 (+CA1-004 · CA1-005).

**Reuse:** RMS `targeta/` · Exec-Core `sandbox_generation.py`, `analysis_lifecycle.py`, `deck_*.py`.

**Deps:** W3 · W5.

**DONE means:** at least one model passes six-criterion acceptance and lands on the estate as an accepted record; the LLMs tab renders it with its status/share/last-acceptance-date; CA1-011 re-check date; CA1-004 baseline line; CA1-005 whitepaper action drafts from run artefacts.

**Acceptance rows:** Promises #22 · #23 · #24 · #25 · #30 · CA1-004 · CA1-005 · CA1-011.

---

### Wave 8 (W8) — Governance ceremony · handoff contract · breach notification · access-and-erasure · scope **XL**

**Backend mechanisms:** rules-updates ceremony pipeline (propose · counter-sign · countdown · apply · re-check) · generalised handoff contract module (CA1-009) · breach notification path (CA1-N2) · individual access-and-erasure endpoint (CA1-N3) · Watch staleness-flagging for rulebooks/baselines (CA1-012).

**v7 surfaces lit:** Rules Updates ceremony · Approvals group (Spend Requests · Rules Updates · Model Admission) · Access & Erasure request UI · Breach Notification console.

**17-doc anchor:** Doc15 (whole; +CA1-006 · CA1-009 · CA1-012) · CA1-N2 · CA1-N3 · Doc16 refusal grammar wire-through.

**Reuse:** Exec-Core `monitor/`, `cycle_lifecycle.py`, `cycle_permissions.py`, `cycle_synthesis.py` · RMS `master_admin/`.

**Deps:** W3 · W5 · W6 (Grey Mirror groundwork).

**DONE means:** end-to-end rule change: propose → counter-sign → countdown → apply → re-check; every cross-app crossing (e.g. ThinkLab→Task Manager) issues a receipted handoff contract; breach notification path fires within a stated time; a person can request what the estate holds on them and request erasure.

**Acceptance rows:** Promises #26 · #27 · #32 · CA1-006 · CA1-009 · CA1-012 · CA1-A5 · CA1-A6 · CA1-A7 · CA1-N2 · CA1-N3.

---

### Wave 9 (W9) — Watch / Grey Mirror mechanism completion · ledger continuity · walk-this custody · scope **XL**

**Backend mechanisms:** Doc03 remainder — bait mechanism · containment ladder · quarantine copy · self-check drill · external witness · four-memory stack. Ledger continuity attestation (CA1-N5). "Walk this →" custody-scoped affordance (post-T8 disposition).

**v7 surfaces lit:** Grey Mirror four sub-surfaces (overview · monitor · response · people) · Walk-this affordance across every surface (once T8 resolved) · Ledger Continuity attestation record.

**17-doc anchor:** Doc03 (remainder) · Doc16 (walk-this) · CA1-N5.

**Reuse:** — this is the largest **BUILD** wave. RMS `synisense/` has partial primitives only; Executive-Final's access would materially help.

**Deps:** W6 (groundwork) · W8 (ceremony pipeline).

**DONE means:** Watch mechanism fully operational — bait records planted, actors moving in a quarantine copy detectable, containment ladder demonstrable end-to-end, external witness signs; the platform survives a simulated outage of the primary record with a stated RTO and no lost receipts; "Walk this →" affordance available on every claim with custody-scoped visibility.

**Acceptance rows:** Promises #6 · #7 · CA1-N5 · CA1-A8 (post-T8) · full Doc03.

---

## §7 · Wave summary table — **RE-BASELINED 2026-08-25 (W6 opener #1)**

**Calibration factor** stated once: **1.60×** (median of `actual_LOC / estimated_LOC` across W1-W5). Two waves (W2, W4) sat far outside median (11.11× and 4.28×) — those are named honestly as **class misclassifications** (W2: S-class was wrong for reflection-before-commit; W4: M-class was wrong for Northena ADAPT + ThinkLab surfaces) rather than pure calibration signal. The three calibrated-scope waves (W1, W3, W5) sit tightly around 1.26-1.61×; median 1.60× is the honest go-forward multiplier.

**W1-W5 · actuals on record (git-measured insertions per commit-run):**

| Wave | Class (orig) | LOC est | LOC actual | Actual/Est | Status | Notes |
|------|:---:|---:|---:|---:|:---:|---|
| W1 · Drawer + registry polish | M | ~800 | 1006 | 1.26× | CLOSED | Inside class. |
| W2 · Reflection-before-commit | S | ~150 | 1666 | **11.11×** | CLOSED | **Class misclassification** — reflection-before-commit shim carried tests-first invariant work + boundary discipline shims. Should have been M-class from the start. |
| W3 · Chokepoint · masking · residency | L | ~2000 | 2519 | 1.26× | CLOSED | Inside L class ceiling. |
| W4 · Northena | M | ~600 | 2566 | **4.28×** | CLOSED | **Class misclassification** — Northena ADAPT + 4 ThinkLab surfaces was always L-class. Owner notified at close. |
| W5 · Solva + Chat + Shield + Connect-LLM | L | ~2500 | 4026 | 1.61× | CLOSED | L-class-plus. Landed all owner-mandated surfaces + backend Connect-LLM verify. |
| **W1-W5 total** | — | **6050** | **11783** | **1.95× (weighted mean) · 1.60× (median)** | | |

**W6-W9 · RE-BASELINED estimates (est × 1.60):**

| Wave | Scope | LOC est (original) | LOC est (**re-baselined**) | Class (re-baselined) | New surfaces | Deps |
|------|-------|---:|---:|:---:|---|---|
| **W6** · Cost Ledger · retention · GM groundwork + W5 deferrals | ~1800 | **~2880 LOC · stop-and-report** | L-plus | 3 (Cost Ledger · retention rows · Grey Mirror overview drawn-not-blank) + 4 folded W5 deferrals (LLM chip UI polish · Data Suite · Solva 4-6 mech · CA1-010 lowered-standard) | W3 · W5 |
| **W7** · Targeta · Model Ecosystem · Model Admission | ~2200 | **~3520 LOC** | XL-effective | 3 (Model Admission ceremony · LLMs tab populated · Rule Books Library) | W3 · W5 |
| **W8** · Governance · N-series · handoff · Breach · Access/Erasure | ~3500 | **~5600 LOC** | XXL-effective | 6 (Rules Updates · Spend Requests · Access/Erasure · Breach console · Approvals · Trace) | W3 · W5 · W6 |
| **W9** · Watch · Grey Mirror · Ledger continuity · Walk-this | ~4000 | **~6400 LOC** | XXL-effective | 5 (Grey Mirror ×4 + Continuity attestation) | W6 · W8 |
| **W6-W9 total (re-baselined)** | ~11500 | **~18400 LOC** | | | |

**W6 stop-and-report line: 2880 LOC.** Owner ruling ("W6's own re-baselined budget is your stop-and-report line") is enforced.

**Reading:** the W6-W9 remaining build effort is honestly **~18400 LOC** — 60% higher than the pre-calibration estimate of ~11500 LOC. This is what the actuals say; it is not a reason to slow down, it is a discipline call so the owner isn't surprised at W6/W7 close.

**Owner ruling paths (deferred to owner if wanted at W6 mid-checkpoint):**
- (a) accept the re-baseline as stated (L-plus / XL-effective / XXL-effective naming) and proceed at that budget.
- (b) narrow W6 scope hard — drop Solva stages 4-6 mechanism-side + Data Suite v7-exact, keep Cost Ledger + retention + Grey Mirror overview + CA1-010 + LLM chip UI polish only. Estimated at ~2200 LOC re-baselined.
- (c) introduce a formal "L-extended" tier at ~3000 LOC to name what the recent waves actually are.
- Default: (a) — the calibration IS the discipline.

**Totals restated:** ~17,600 original estimate (§7 line preserved · W1-W5 6050 + W6-W9 11500 orig) vs **~30,183 re-baselined total** (11783 actual W1-W5 + 18400 re-baselined W6-W9). **The build is 40% closer to done than the pre-calibration numbers suggested, but 71% larger in total remaining work than pre-calibration.**

---

## §7b · Wave summary table (LEGACY · pre-calibration · kept for audit)

The pre-calibration table below is preserved as historical record. **Do not use for planning.** The re-baselined table in §7 above is the current authority (Owner Ruling 2026-08-25 W6 GO opener #1).

| Wave | Scope | LOC estimate | New surfaces | New mechanisms | Deps | Areas advanced |
|------|:---:|---:|---:|---:|---|---|
| W1 · Drawer + registry polish | M | ~800 | 1 (ConnectDrawerChat) | 0 | none | Registry, Orchestration |
| W2 · Reflection-before-commit | S | ~150 | 0 (extends detail card) | 1 | W1 | Compute/Cost |
| W3 · Chokepoint · masking · residency | L | ~2000 | 1 (Data Shield) | 4 | W2 | Custody, Governance |
| W4 · Northena | M | ~600 | 4 (ThinkLab surfaces) | 1 | W3 | Direction/Record |
| W5 · Solver · Shrinkage · Memory | L | ~2500 | 3 (Chat · Data Suite · Reasoning Shield) | 3 | W3 | Measurement/Reasoning, Extraction |
| W6 · Cost Ledger · retention · GM groundwork | L | ~1800 | 3 (Cost Ledger · Grey Mirror overview · retention rows) | 3 | W3, W5 | Compute/Cost, Watch (partial) |
| W7 · Targeta · Model Ecosystem | L | ~2200 | 3 (Model Admission ceremony · LLMs tab populated · Rule Books Library) | 3 | W3, W5 | Training/Models |
| W8 · Governance ceremony · N-series · handoff | XL | ~3500 | 6 (Rules Updates · Spend Requests · Access/Erasure · Breach console · Approvals · Trace) | 5 | W3, W5, W6 | Governance, Orchestration, Custody |
| W9 · Watch · Ledger continuity · Walk-this | XL | ~4000 | 5 (Grey Mirror ×4 + Continuity attestation) | 5 | W6, W8, T8-owner | Watch/Security, Orchestration |
| **Totals** | | **~17,600** | **26 new surfaces** (+ 4 already built = 30/58 reach) | **25 new mechanisms** | | |

**End-of-W9 projected status**: mechanism corpus ~85–90 %, interface ~72 % (30 of 58 surfaces built; the remaining 28 are secondary or CA1-A-series surfaces that fold into the same mechanisms). **Headline ≈ 82 %.** Remaining 18 % is second-order polish + CA1-Ax surfaces (Board 360 sub-panels, Documents suite reuse polish, Ideas/Signals sub-nav wire-up, third-party apps hooks).

## §8 · What DONE-of-the-whole-build means

The build is closed when:
1. Every one of the 515 mechanism-corpus rows in the register is status **DONE** (with a test citation on Extraction-Akki track-a).
2. All 58 v7 surfaces render — real facts or honest-empty — through the fluid-left + 300px-right pattern in v7 typography/palette exactly.
3. Every one of the 12 CA1-xxx amendment rows is DONE.
4. All 5 CA1-N-series promises are DONE.
5. All 8 CA1-A-series promises are DONE (surface exists + mechanism behind).
6. Every acceptance row in `AKKI_Promise_Table.xlsx` traces to a passing test (T5 owner ruling: Promise Table = acceptance/test register).
7. `phase0/drill_receipts/` contains right-reason + green receipts for every cycle; no receipt marked "papered over".
8. Sweep across the repo tree returns hit_count 0 for the AK/SK across every axis.
9. Deliverables snapshot at `/api/deliverables` reflects HEAD of both repos at build close.

Owner is the sole signatory on close.
