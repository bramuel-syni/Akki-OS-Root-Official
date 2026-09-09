# HOLISTIC_PLAN.md — the whole programme, one page

**READ `STATE/STANDING_ORDERS.md` FIRST — permanent standing law.**

**Authored:** 2026-09-09 under owner directive 2026-09-09T~12:55Z ("compile and return the holistic programme plan · HOLD on CP2 · owner approves before any further build"). Owner ruling banked verbatim in `STATE/DECISIONS.md`.

**Sources of truth for this plan:** `STATE/STANDING_ORDERS.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md`, `notes/MASTER_TRACEABILITY_AUDIT_20260907.md` (+ its `20260909_UPDATE.md` companion), `notes/spec_id_index.json` (verbatim spec-ID authority), `notes/RULING_LEDGER.md`.

**Standing law confirmed:** terminal `pytest` only under `BASELINE_GUARD=1` · mechanical RED before every implementation · double-green byte-match to close · two-commit pattern (track-a code + workspace state) · **no push** · every owner ruling banked verbatim in DECISIONS.md before action · Ship-Manifest-DoD (pod runtime byte-identical to repo pod_shell). No testing_agent. No refactor. Thin-kernel discipline.

---

## §0 · Honest state disclosure before we go anywhere

Owner's HOLD directive names ratchet floor **3064**. That was true at CP1 close.

Between owner's prior "Proceed straight through CP2 → CP10" authorization (2026-09-09T~12:20Z) and this HOLD (2026-09-09T~12:55Z), the following landed locally on `programme/track-a` before HOLD arrived:

| CP | track-a commit | Ratchet | State |
|---|---|--:|---|
| CP1 · 22-route inventory | `9874b1d` | 3040 → 3064 | committed |
| CP2+CP3+CP4 · payload shapes | `872ed36` | 3064 → 3078 | committed |
| CP5+CP6+CP7 · real-data wires (opportunity_briefs, perception, rules_updates) | `374f9c3` | 3078 → 3086 | committed |
| CP8 · v3 substitution rules (24 bound + 13 retired-transparent) | `d691899` | 3086 → 3093 | committed |
| CP9 · 78 campaign runs in models roster with owner honest-state map | `ff20aac` | 3093 → 3098 | committed |
| CP10 · real-Chromium proof + wave-close manifest | *not committed* | 3098 → (would be 3100) | **HELD** — test file drafted, wave-close manifest drafted, ratchet not yet bumped, no commit issued after HOLD arrived |

**Live floor as of this plan: 3098.** CP10 stays uncommitted awaiting owner approval of this holistic plan. All commits are local (no push, per standing law). Owner may keep CP2-CP9 as-is, roll them back, or steer differently once he has read this plan.

---

## §1 · What we are building — one paragraph

**Akki is a custody platform.** Something enters at a chokepoint (Doc 01), gets read at the seam, gets ledgered, gets governed by a rule book (`rulebook_engine_spec_v1` + `rule_criteria_spec_v1`), gets custody-transferred by a governance ceremony, gets counter-signed under a countdown, gets a reference monitor between principals and assets (`akki_governance_architecture_v1` Attribute 6), and produces recommendations — never autonomous decisions — under a stated determinism boundary (Attribute 10). Every action leaves an append-only audit record; every ceremony leaves a Ledger row; every control has an assessment procedure. Rounding out the platform: a **Rules Service** (`rulebook_engine_spec_v1`) that authors and enforces rules; a **DAP** (`dap_backend_spec_v1`) that governs data exit and reproduction under a cumulative disclosure budget; a **Watch** (Canon 8, `security_architecture_v1`) that runs on independent authority and rules stealth-drift, poisoning, and coalitions of principals out of scope; an **Agent Swarm Containment** (`agent_containment_spec_v1`) layer that caps agentic capabilities and interventions; a **Whitepaper Wizard** (`whitepaper_wizard_spec_v1`) that produces the platform's owner-facing evidence; a **Prototype v3** design surface that is the binding UI; and a **Business Continuity Annex** (`business_continuity_v1`) covering Callable Skill Files provenance.

Everything else in this plan is a wave that delivers one concrete slice of that picture, with a spec-ID owner named, a plain-language outcome, a way to prove it closed, and the current owner-facing blockers on it.

---

## §2 · What is ALREADY done (session ledger through 2026-09-09T~13:00Z)

Waves closed in this session AND their session-scale ratchet delta:

| Wave · CP | Delivers (plain language) | Spec IDs (verbatim) | Track-a | Ratchet |
|---|---|---|---|--:|
| **W-STANDING-ORDERS-COMPACTION-PROOF** | Every session boots from `STANDING_ORDERS.md` first; owner rulings banked verbatim before action; §1..§6 discipline pinned. | STANDING_ORDERS §1..§6 | (pre-session) | 2997 → 3004 |
| **W-STANDING-ORDERS-MISSION-FRAMED** | Owner-facing reports are metrics-first, mission-framed, plain product language (never engineering vocabulary on surfaces). | STANDING_ORDERS §2 owner ruling 2026-09-08T~05:15Z verbatim | (pre-session) | 3004 → 3006 |
| **W-TRACKING-DEFECT-FIX** (STEP 1) | Every canon-cited spec now indexed by `{spec_id, filename, sha256}` — the "false-missing" tracking defect closed at the source. Also indexes the two prototypes and all HTML design drops (owner extension 2026-09-09T~11:40Z). Concurrent recovery: real-Chromium harness refreshed (37 rules, 0 orphans). | `rule_criteria_spec_v1` (BANKED-DERIVED · owner ruling 2026-09-09T~11:40Z) · `business_continuity_v1` (BANKED) · 22 more spec IDs · 11 design IDs (prototype v3 · v2 · v7 x3 · v8 · dap frontend · v8 templates) | `7f3c8cc` | 3006 → 3017 |
| **W-INGEST-AC-SPEC + W-RULING-LEDGER-STEP3** (STEPS 2+3) | 13th spec `agent_containment_spec_v1` ingested word-for-word: 12 AC-1..AC-12 requirements + 5 LIM-1..LIM-5 non-claims in a distinct NON-CLAIMS register (owner rule "so nobody assumes condition 3 was solved"). 9 DEFAULT-class + 5 RATIFIED + 1 COUPLED + 4 OPEN rulings wired tests-first at `backend/services/rulings/default_class_constants.py`. | `agent_containment_spec_v1` (§4 AC-1..AC-12 verbatim · §5 LIM-1..LIM-5) · `rulebook_engine_spec_v1` R-1..R-4 · `dap_backend_spec_v1` R-1 R-4 R-5 · `security_architecture_v1` R-8..R-11 · `pruning_unlearning_amendment_v1` R-12 | `a5324dd` | 3017 → 3040 |
| **W-AUDIT-REBUILD-STEP4** (STEP 4) | Master audit rebuilt on the corrected index: denominator 1,159 → 1,171 (+12 AC rows); missing list 17 → 5 with zero-hit receipts; ruling ledger snapshot banked. | Cross-reference: `notes/MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md` | (workspace state) | 3040 (no code delta) |
| **W-REGISTRY-FULL-BUILD CP1** | 22 missing routes wired end-to-end on the pod-shell app with honest-empty payloads. Ship-Manifest-DoD kept. | Prototype v3 (binding) · Doc 10 v2 SURFACE_AUDIT rows R1..R29 · `akki_governance_architecture_v1` §6 Registry ceremony | `9874b1d` | 3040 → 3064 |
| **W-REGISTRY-FULL-BUILD CP2+3+4** | Every new route's payload shape frozen — empty responses must carry `honest_gap` + `not_measured=True`; fabrication is a right-reason failure. | Prototype v3 anchor surfaces · Doc 0 Attr 5 (checkpoints) · Doc 4 Solva surfaces (reads only, no builds) | `872ed36` | 3064 → 3078 |
| **W-REGISTRY-FULL-BUILD CP5+6+7** | Real-data wires: `opportunity_briefs` reads `services.opportunity_briefs.brief_registry`; `perception` service module + `execution_mode_telemetry` mounted; `rules_updates/pending` reads `phase0/rules_ledger/`. | `akki_governance_architecture_v1` §5 · CA1 opportunity briefs · CA1 perception charter | `374f9c3` | 3078 → 3086 |
| **W-REGISTRY-FULL-BUILD CP8** | v3 substitution rules re-authored against prototype v3 body: 24 rules bind to v3 literally; 13 v2/v8 rules retired transparently (banked as `absent_from_v3` for real-Chromium re-admission at CP10). Owner law honoured: rule-matches-nothing = RED, never silent. | Prototype v3 (design_id `prototype_v3` sha `ee6ebe77e1c5…`) | `d691899` | 3086 → 3093 |
| **W-REGISTRY-FULL-BUILD CP9** | 78 campaign runs surfaced in `/api/model_registry/full_record` — owner-ruled honest-state map applied verbatim (2026-09-09T~12:20Z): sealed-clean → "under evaluation", synthetic-fail-seal → "did not complete", pilot-v1 → "pilot", v2/v2.1 → "under evaluation". Every row carries `state_evidence`. **78 ≥ 77 owner target met.** | Doc 14 Model Ecosystem rows · Doc 17-19B Trained-Models surface · `phase0/campaign_drafts/*_v21_lane*_queue_manifest.json` union `phase0/baseline_lines/*.json` union `phase0/solva_runs/*.json` | `ff20aac` | 3093 → 3098 |

Prior to this session (pre-2026-09-09), the following waves had already been landed under the ratchet — full history in `STATE/DECISIONS.md`:

- Doc 09 Connection & Census (fully DONE, 21/21 rows).
- Doc 10 Registry base (10 DONE, 5 PARTIAL, 3 REUSE, 0 BUILD — CP1-CP7 of this session finished the RESTing).
- Doc 12 Cost & Compute Pt 2 (9 DONE, 2 PARTIAL, 1 REUSE — W-G5c-COMPUTE-v2 + W-Compute-Residuals).
- Doc 11 CA1-008 Cost Ledger backend (DONE).
- W-Shield-Train stack (masked pipeline · governed SELECT · held-out slice hashes banked preflight · on-host trainer · deterministic 20% tail split · Doc 3 A5.2 admission).
- W-Campaign-Infra (queue dispatcher · window-fill guarantee · full-consumption invariants).
- W-Multi-Table-Extract (sequential per-table extract + pipeline-level compose · row_executor chokepoint per table).
- W-SMS-Body-Emit (owner Ruling #5(a) landed · sms_sent-inclusive corpus · re-extraction rebased).
- W-Orchestrator-Resilience r1/r1-wire/r2 (dispatcher heartbeat · reattach protocol · seal seams).
- W-WINDOW-FILL-GUARANTEE + W-WINDOW-FILL-RESTORE + W-WINDOW-FILL-RESTORE-2 (idle-lane restoration · dispatcher respawn on death).
- W-WPW-v1-a + W-WPW-v1-b (spec ingest + charter authored; Tier 3 blocked on R1/R2/R3).

Cumulative session-plus-prior ratchet at close of CP9: **3098 passed · 1 skipped · 165 D1a-1 quarantined**. Double-green byte-identical at every close.

---

## §3 · The full wave inventory, in owner-directed priority order

Owner rulings that fix priority (verbatim, DECISIONS.md):

- 2026-09-06T19:20Z — "**Priority building goes to registry. I need registry fully build.** Solva-v2 lift queues immediately behind. Commercial after baselines."
- 2026-09-08T~06:15Z — "**Then fire W-REGISTRY-FULL-BUILD** ... Solva-v2 lift queues immediately behind. ... Rules Service stack is BLOCKED on owner agreement on `rule_criteria_spec_v1` (the standalone ROC framework spec doc)."
- 2026-09-06T19:12Z — "**Commercial after baselines.**"

Every wave below cites its verbatim spec IDs and names its blockers.

### 3.1 · W-REGISTRY-FULL-BUILD — remaining work (only CP10 left · 2 invariants)

**What we're building:** The last piece of the Registry portal — the real-Chromium proof pass and the wave-close manifest.

**Why:** Prototype v3 is the binding design (owner ruling 2026-09-06T~19:20Z). CP1-CP9 landed the routes, the data wires, and the substitution-rule static file-body binding. CP10 proves the whole surface renders through real headless Chromium against the running pod, with the fresh 2026-09-09T11:49Z harness receipt showing 37 rules bound to rendered DOM and 0 orphans.

**What closes it:** the running pod loads the Registry portal in a real Chromium instance, the harness reports GREEN with substitutions applied, no dummies still present, all expected sentences rendered, style signature met. Screenshot bundle at `phase0/eyeball_proxies/`. Wave-close manifest at `notes/W_REGISTRY_FULL_BUILD_close.md` (drafted; not committed).

**Spec IDs (verbatim):** prototype v3 (design_id `prototype_v3`) · `akki_governance_architecture_v1` §6 · Doc 10 v2 SURFACE_AUDIT rows R1..R29.

**Effort class:** S (~2 invariants + 1 screenshot re-run).

**Blockers:** OWNER APPROVAL OF THIS PLAN. Nothing technical.

**Test gate:** `test_w_registry_full_build_cp10_wave_close.py` (drafted, RED captured at `phase0/drill_receipts/20260909T*_wregfullbuild_cp10_RED_pre_impl.log` — 1/2 right-reason failure on missing manifest). Full BASELINE_GUARD=1 double-green already proven at 3100 both runs in-session before HOLD arrived.

### 3.2 · W-SOLVA-V2-LIFT — Solva "read then decide" reasoning stack

**What we're building:** The **Solva** reasoning subsystem — the piece that reads a question, retrieves grounded evidence, decides which policy applies, and produces a recommendation (never an action). Lifts the mature 24,595 LOC Solva-v2 donor pool from `repos/Akki-Executive-Core/backend/services/solva*` + `repos/Akki-Executive-Final/backend/services/solva*`; diff-reviews then adopts against `akki_governance_architecture_v1` Attribute 4 (Reasoning · Grounding · Solver); reconciles with the 1,392 LOC Solva partial already in `repos/Extraction-Akki/backend/services/solva*`.

**Why:** Canon 2 CIF and Doc 04 depend on it. Every recommendation surface in the platform (Compute · Registry · DAP · Data Suite) needs Solva to be real, not honest-empty.

**What closes it:** Solva stages 1-6 unit-green (retrieval → ground-check → policy-fetch → PDP-decide → PEP-emit → PIP-log). Router mounted at `/api/solva/*`. Policy contract preserved: annotate-only surface (Determinism Boundary — no auto-execute per `akki_governance_architecture_v1` Attribute 10). Real-Chromium eyeball proxy shows Solva-driven recommendations rendered on the Registry Recommended list without dummies.

**Spec IDs (verbatim):** `akki_governance_architecture_v1` Attribute 4 BR-4.1..4.3 (BR series) · Canon 2 CIF C2-001..C2-066 · Doc 04-001..041 · Solva v2 canon rewrite 2026-08-01 (owner ruling in DECISIONS).

**Effort class:** XL (~5000-8000 LOC after 1.60× calibration · single wave · likely 10-15 CPs).

**Blockers:** DPO-5 (owner may rule LIFT-CLEAN vs LIFT-ADAPT sub-grade for the donor code). If owner accepts DPO-5 as-is, no owner blocker; W-SOLVA-V2-LIFT can open the moment W-REGISTRY-FULL-BUILD closes.

**Test gate:** every Solva stage's contract test-first RED then GREEN, then double-green. Router mount test. `/api/solva/annotate?q=…` returns `{answer, evidence[], policy_ref, decision, log_ref}` and cross-checks with the Ledger.

### 3.3 · W-DAP-STACK — nine waves scoping `dap_backend_spec_v1` DAP-1..DAP-30

**What we're building:** The **Data Access Portal (DAP)** backend and its ceremony machinery — the gate every request for data-outside-the-platform must cross. `dap_backend_spec_v1` §4 defines DAP-1..DAP-30 as thirty ordered requirements grouped by concern (admission → controlled units → chokepoint → governed queries → row execution → audit → coalition-joint-evaluation → cumulative disclosure budget → component-boundary inspection). Owner asked for the plan carved into **9 waves** matching those nine concerns.

**Why:** The DAP is the primary revenue-bearing surface (`dap_backend_spec_v1` §1 preamble — "controlled release of controlled units"). Every commercial engagement passes through it. Doc 0 Attribute 3 (Governed Triad) and Attribute 4 (Controls) both depend on it. And every S-22 / S-23 / S-25 security amendment (Trojan/Whisper 2026-09-05) closes on it.

**What closes each of the 9 waves (spec IDs verbatim throughout):**

| DAP wave | Delivers | `dap_backend_spec_v1` verbatim IDs | Effort |
|---|---|---|---|
| DAP-1 · Admission + principal registry | Every accessor is a named principal; class-registered; opened per `dap_backend_spec_v1` R-1 (RATIFIED controlled-unit definition) | DAP-1..DAP-5 · owner-RATIFIED R-1 | M |
| DAP-2 · Controlled unit registry | Every unit tagged with class/lineage/sensitivity; `agent_containment_spec_v1` AC-3 style capability history per unit | DAP-6..DAP-10 · `agent_containment_spec_v1` AC-3 | M |
| DAP-3 · Chokepoint per data source | One chokepoint per source; RDS Data API + owner-approved AWS custody keypair (already banked at `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json`) | DAP-11..DAP-15 · Doc 01 chokepoint discipline | M (largely reused from W-Shield-Train build) |
| DAP-4 · Governed query authoring | SELECT authored under masking-policy declaration; `masking_policy.v0.json` clarification_drawer discipline (owner Ruling #5(a) 2026-09-06); reject if any column unclassified | DAP-16..DAP-20 · masking_policy_v0 · Doc 03 A5.2 | L |
| DAP-5 · Row execution + chokepoint receipt | `row_executor.execute_row_bearing_query` fires per-table; refuse-unclassified-by-construction; chokepoint receipt banked to `phase0/shield_train_receipts/` per query | DAP-21..DAP-25 · reused from W-Shield-Train-RUN | S (already lifted) |
| DAP-6 · Cumulative disclosure budget (S-25) | Per-party (ε, δ) ledger; disclosure counter; refuse on breach per `security_architecture_v1` R-7 (OPEN) budget number | DAP-26..DAP-30 · `security_architecture_v1` S-25 · owner OPEN R-7 | L |
| DAP-7 · Front-end (DAP portal) | Design_id `dap_frontend_standalone` (`canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html` sha `d1c9057b…` — already in `notes/spec_id_index.json`); mount + wire per prototype-v3 discipline | Prototype `dap_frontend_standalone` | M |
| DAP-8 · Component-boundary inspection (S-22) | Every output leaving a component boundary checked for controlled-unit content; tagged ADVISORY where it recommends/ranks/proposes/evaluates; deterministic-side of verdict seam; `security_architecture_v1` R-8 DEFAULT baseline-period approach applies | `security_architecture_v1` S-22 · DAP-33 · `security_architecture_v1` R-8 (RATIFIED baseline-period default) | L |
| DAP-9 · Coalition joint evaluation (S-23) | A coalition is one actor; connected-component admission graph; shared party/lineage/coordination-signature; refuse per-principal budget bypass; `security_architecture_v1` R-11 friction-only default | `security_architecture_v1` S-23 · DAP-34 · `security_architecture_v1` R-11 (RATIFIED baseline-period default) | L |

**Blockers (owner-open):**
- **`security_architecture_v1` R-7** — estate release budget number (blocks DAP-6 only; other 8 waves proceed on DEFAULT-class disclosure ledger with `not_measured` output until R-7 lands).
- **`dap_backend_spec_v1` R-6** — pricing model (blocks nothing technical; blocks commercial launch labelling).
- **DAP named approving authority (open owner-reserved)** — blocks nothing technical; ceremony records name the authority once ruled.
- **DAP R-3 per-party ceilings** — COUPLED with `security_architecture_v1` R-7 (owner ruled DAP R-3 "MUST NOT be ruled alone"); resolves together with R-7.

**Test gate per wave:** ceremony machinery is tested-first RED then GREEN; every DAP-N requirement gets its verbatim quote in the docstring; double-green byte-match. Every wave-close adds a DAP-scoped ratchet delta (approx +8..+15 invariants per wave).

**Session-total effort class:** L average × 9 waves = ~9 weeks of foundation work under thin-kernel discipline.

### 3.4 · W-DOC0-GAP-CLOSURE — seven attribute waves closing `akki_governance_architecture_v1`

**What we're building:** The seven **not-yet-built attributes** of `akki_governance_architecture_v1` (Doc 0 v2) — the platform's governance architecture. Doc 0 has 12 attributes; the other five (4 Controls · 5 Checkpoints · 9 Ceremony · 11 Coherence · 12 Governance) either are already partly built through the Rules Service stack or roll into it (Attribute 9 explicitly, Attribute 12 fan-in on 1-11).

The seven gap-closure waves:

| Wave | Attribute | Delivers | `akki_governance_architecture_v1` verbatim IDs |
|---|---|---|---|
| W-DOC0-ATTR1-TCB | **Attr 1 · TCB** | Trusted Compute Base is enumerable: `GET /api/tcb/current` returns list; every entry has `{id, kind, deterministic:bool, guarantee_ref, ceremony_history}`; TCB modifications trigger Ledger entry. Depends on `tcb_enumeration_v1` (BANKED per `notes/spec_id_index.json`). | BA-1.1..1.3 · TA-1.1..1.3 · BR-1.1..1.2 · `tcb_enumeration_v1` |
| W-DOC0-ATTR2-SUBSYSTEMS | **Attr 2 · Subsystem Declaration Architecture** | For every guaranteed outcome, one subsystem accountable; interfaces declared; access only through interface; no side channels; linter refuses cross-boundary import except via declared interface. | BA-2.1..2.3 · TA-2.1..2.3 · BR-2.1..2.2 |
| W-DOC0-ATTR3-TRIAD | **Attr 3 · Triad Classes** | Finite named lists of principal classes, asset classes, operations; each op maps to exactly one checkpoint; dual-role (model as principal+asset) tagged explicitly. | BA-3.1..3.3 · TA-3.1..3.3 · BR-3.1..3.2 |
| W-DOC0-ATTR6-REFERENCE-MONITOR | **Attr 6 · Reference Monitor** | Non-bypassability per path; tamper-resistance; verifiability (small, readable, initialisation specified); every path from before-monitor to after-monitor enumerated and proven to traverse `monitor.evaluate()`. | BA-6.1..6.3 · TA-6.1..6.3 · BR-6.1..6.3 · `security_architecture_v1` |
| W-DOC0-ATTR7-BASELINE | **Attr 7 · Mandatory Baseline Ceremony** | Baseline unlowerable by measured; identical for class; refusal on failure (never degraded pass); lowered-standard labelled discretionary, session-scoped, logged expiry. Reuses CA1-010 partial (W6 CP5). | BA-7.1..7.3 · TA-7.1..7.3 · BR-7.1..7.3 · CA1-010 · `business_continuity_v1` |
| W-DOC0-ATTR8-AUDIT-AU3 | **Attr 8 · AU-3 Audit Record** | Every record has `{event_type, time, location, source, outcome (incl refuse), principal_identity}`; both success and refuse recorded; tamper-resistant time source; append-only or chained; non-repudiation. | BA-8.1..8.3 · TA-8.1..8.3 |
| W-DOC0-ATTR10-DETERMINISM | **Attr 10 · Determinism Boundary** | Every component classified deterministic/learned; detect-never-decide doctrine; human-oversight capabilities (a-e per EU AI Act Art. 14) each have a wired mechanism; S-13 sever tests green. Depends on `determinism_inventory_v1` (BANKED per `notes/spec_id_index.json`). | BA-10.1..10.3 · TA-10.1..10.3 · BR-10.1..10.2 · Attribute 10 preamble EU AI Act Art. 14 · `determinism_inventory_v1` · `failure_posture_v1` |

**Effort class per wave:** Attr 1 M · Attr 2 L · Attr 3 M · Attr 6 L · Attr 7 M · Attr 8 L · Attr 10 XL. Overall XL bundle (approximate 6-10 weeks).

**Blockers:** none owner-open individually. All seven can be sequenced by owner in any order Doc 0's Attribute 12 fan-in permits (`1→2→3→4→5→6→7,8; 10 depends on 1,2; 11 depends on 5,6; 12 depends on 1-9`).

**Test gate:** every Attribute's build requirements (BR-*) get verbatim-quoted invariants; ceremony machinery test-first; assessment procedure test per Attr 4 (see Rules Service block). Double-green at every wave close.

### 3.5 · W-WPW-TIER-1-2 — Whitepaper Wizard first two tiers

**What we're building:** The **Whitepaper Wizard** (`whitepaper_wizard_spec_v1` in `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx`) Tier 1 (baseline whitepaper draft from a Model Ecosystem baseline_line record) and Tier 2 (evidence-weave with citation graph frozen).

**Why:** Every model result the platform produces must have an owner-facing whitepaper (`akki_governance_architecture_v1` Attribute 7 baseline ceremony · Doc 14). Tier 1 is the pilot draft; Tier 2 is the evidence-woven version bound for internal review.

**What closes it:** Whitepaper notebook shape v1 produces a draft round-trip from a `baseline_line` record + `campaign_manifest` + `held_out_slice_hash` + `adapter_walk_sha256`; citation graph frozen; integration with campaign records proven. Router mounted at `/api/wpw/*`.

**Spec IDs (verbatim):** `whitepaper_wizard_spec_v1` WPW-1..WPW-12 (Tier 1 · Tier 2) · Doc 14-001..028 (Model Ecosystem · Baseline · Whitepaper).

**Effort class:** M (~500-800 LOC · 2 CPs).

**Blockers:** none for Tier 1+2. Tier 3 (WPW-13..WPW-18) blocked separately — see §4 open rulings.

**Test gate:** round-trip test with a known baseline_line record produces a draft that quotes verbatim from `campaign_manifest` and `held_out_slice_hash`. Citation graph consistent.

### 3.6 · W-PRUNING-UNLEARNING — pruning + retention amendment

**What we're building:** The **pruning · unlearning amendment** (`pruning_unlearning_amendment_v1` in `canon/AKKI_Canon_Addendum_1.docx` §amendments) — how to retire a rule, a control, a trained model, or a controlled unit from the platform. Owner ruling 2026-09-08T~06:15Z DEFAULT-class: **re-derivation is default; recall requires explicit case-by-case owner sign-off**. Wired tests-first at `backend/services/rulings/default_class_constants.py::PRUNING_R12_DEFAULT = "re_derivation"` + `PRUNING_R12_RECALL_REQUIRES_OWNER_SIGNOFF = True`.

**Why:** Every append-only append-only ledger surface needs a retirement path that preserves audit; every trained-model roster row needs a "retired · session-scoped · expiry logged" tag under a governance ceremony.

**What closes it:** retirement ceremony fires an actual re-derivation of downstream artifacts (default path); a recall ceremony can be requested but blocks on owner sign-off (proven by test that a recall request without owner-sign-off marker refuses with plain-language "recall requires explicit case-by-case owner sign-off").

**Spec IDs (verbatim):** `pruning_unlearning_amendment_v1` R-12 · CA1 amendments · Doc 15 governance ceremony · `akki_governance_architecture_v1` Attribute 9.

**Effort class:** M (~400-600 LOC · 3 CPs).

**Blockers:** none owner-open (R-12 DEFAULT already applied · owner may amend on evidence).

**Test gate:** already exists — `test_pruning_r12_default_is_re_derivation` + `test_pruning_r12_recall_requires_owner_signoff` are in the ratchet since STEP 3. Adding the retirement-ceremony end-to-end is the build work.

### 3.7 · Rules Service stack — BLOCKED on owner agreement on `rule_criteria_spec_v1`

**What we're building:** The **Rules Service** (`rulebook_engine_spec_v1` at `canon/drops/20260907/extracted/files_11/Rules_Service_Spec_v1.docx`) — the platform's rule authoring, ceremony, amendment, retirement, and re-verification machinery.

**Waves in the stack (four):**

| Wave | Delivers | Spec IDs verbatim |
|---|---|---|
| W-RULE-REGISTRY-BOOTSTRAP | Creator-mode authoring: classify · propose · countersign · countdown · apply · re-verify. Registry rows fully populated with every ROC-10 field (9 columns · Rule ID · Statement · Objective · Doc · Status · Enforcement Class · Domain · Assessment Procedure · Source file:line). | `rulebook_engine_spec_v1` RBM-1..RBM-4 · RBM-18..RBM-20 · I-1..I-5 · `akki_governance_architecture_v1` §4 BA-4.1..4.3 · TA-4.1..4.3 · `rule_criteria_spec_v1` (BANKED-DERIVED per owner ruling 2026-09-09T~11:40Z ROC-1..ROC-11) |
| W-RULES-SERVICE-CEREMONY | Ceremony machinery: 2-signature countersign · cancellable countdown · atomic apply · re-verify · amendment retention · retirement with attestation. Depends on `rulebook_engine_spec_v1` R-1 countdown length (48h ordinary / 7 days TCB — DEFAULT applied), R-3 witness (RATIFIED = Watch C3), R-4 taxonomy (RATIFIED as proposed). | `rulebook_engine_spec_v1` RBM-7..RBM-13 · R-1 (DEFAULT) · R-3 (RATIFIED) · R-4 (RATIFIED) |
| W-RULE-BOOK-LIBRARY | Library holds versioned rule books cited-by-clause; profile bundle per business type; adoption instantiates through customer ceremony. RB-PDP and RB-AIG are FULL; RB-FIN/HLT/MED/RES are SKELETON. | `rulebook_engine_spec_v1` RBM-14..RBM-17 · S20 catalog · S23 v2 SURFACE_AUDIT Rule Books surface |
| W-286-RULE-ENUMERATION-CLASSIFY | Per-rule enumeration of all 286 System Rules Registry rules with Enforcement Class + Assessment Procedure populated. Closes `akki_governance_architecture_v1` G-4 (272 rules without assessment procedure). | System Rules Registry (`System_Rules_Registry.md` / `.json` at `canon/drops/20260907/extracted/files_11/`) · 286 rules · `akki_governance_architecture_v1` G-4 |

**Effort class:** XL total (~10-15 weeks foundation work).

**BLOCKER (owner-level, from DECISIONS.md 2026-09-09T~11:40Z ruling — plain restatement, not paraphrase of any spec text):**

- The `rule_criteria_spec_v1` standalone spec document is **not banked as a standalone `.docx`** — its ROC-1..ROC-11 rows are banked in derived form (in `System_Rules_Registry.md` + `Master_Requirements_Registry.md` + eight-way citations across other specs). Owner ratified DEFAULT-PENDING-OVERRIDE ROC-1 on 2026-09-09T~11:40Z: "treat as BANKED-DERIVED · if owner drops a standalone `rule_criteria_spec_v1.docx` later, fold it in at the next clean boundary."
- Owner has NOT yet ratified the ROC-1..ROC-11 rows themselves as the authoritative rule-authoring criteria. The Master Requirements Registry (drop 2026-09-10) shows them as **`PROPOSED (pending ratification)`**.
- **W-RULE-REGISTRY-BOOTSTRAP requires ratified ROC rows** because ROC-1..ROC-11 are the authoring criteria the Registry validates against.
- **Therefore the four Rules Service waves are blocked** until owner either:
  - (a) drops a standalone `rule_criteria_spec_v1.docx` we can extract requirements from, OR
  - (b) explicitly ratifies the ROC-1..ROC-11 rows as banked in `Master_Requirements_Registry.md` rows 322-332 verbatim, OR
  - (c) authorises us to author the ROC framework from the eight-way citation trail (Doc 0 §4, Rules Service Spec RBM-3/RBM-6/RBM-12, Security Amendments, DAP spec, System Rules Registry, Master Registry) with the caveat that the resulting framework is a derivation, not a spec ratification.

**W-RULE-BOOK-LIBRARY and W-RULES-SERVICE-CEREMONY are structurally independent of ROC ratification** (they operate on rulebooks, ceremonies, and countdowns respectively) — owner could authorise those two waves in advance of the ROC ruling if he wants foundation progress on Rules Service without unblocking the full stack. **DEFAULT-PENDING-OVERRIDE for the plan: hold ALL four Rules Service waves until owner rules on ROC.** Owner overrides on next turn if he wants a split.

**Test gate per wave:** verbatim quote of every RBM / I / R requirement in the invariant docstring; ceremony state-change tests bank the pre/post state to the Ledger before the change; two-signature countersign refused on single-signature; re-verify test fires the assessment procedure and records the result.

### 3.8 · W-DATA-SUITE-v2-LIFT + W-TRUST-SURFACE-v2 + W-EXECUTIVE-SUITE-v2-LIFT — remaining v2/v3 non-Registry surfaces

**What we're building:** The **other portals** on prototype v3 that aren't Registry — Data Suite (3 surfaces), Trust (2 surfaces), and the 4 Executive-Suite portals (Board 360 · Exco 360 · Documents · Rule Books · Collab · Spend · Task Manager).

**Why:** Prototype v3 is binding across the whole design, not just Registry. Owner has ruled these are lower priority than Registry (2026-09-06T~19:20Z) and Solva-v2 (queues immediately behind Registry). They are the follow-on to the Registry wave.

**What closes each:** portal-swap chrome for each; every surface's substitution rules bind to v3 rendered DOM; harness real-Chromium proof; wave-close manifest.

**Spec IDs (verbatim):** design_id `prototype_v3` (BANKED) · `notes/SURFACE_AUDIT_v2_prototype_20260907.md` §Table 2 (18 non-Registry surfaces).

**Effort class:** W-DATA-SUITE-v2-LIFT S · W-TRUST-SURFACE-v2 S · W-EXECUTIVE-SUITE-v2-LIFT L.

**Blockers:** none owner-open. Sequenced by owner AFTER W-REGISTRY-FULL-BUILD CP10 close.

---

## §4 · Open owner rulings — exactly what each unblocks

Every ruling banked in `notes/RULING_LEDGER.md` as OPEN. Plain-language restatement here + which wave each unblocks.

| # | Open ruling | What owner has reserved for himself | Blocks |
|--:|---|---|---|
| 1 | **`security_architecture_v1` R-7 · estate release budget number** | The numeric ε (or budget-unit equivalent) applied cumulatively across parties for controlled-unit disclosure. Owner has framed this as commercial-decision-adjacent. | **W-DAP-STACK DAP-6 (Cumulative Disclosure Budget)** · W-S25-CUMULATIVE-DISCLOSURE · **W-DAP-STACK DAP-3 per-party ceilings (COUPLED)** |
| 2 | **`dap_backend_spec_v1` R-6 · pricing model** | How disclosure is monetised (per-query · per-unit · flat retainer · hybrid). | **W-DAP-STACK DAP-4/DAP-6 commercial labelling only** (all technical waves proceed with unpriced ceremonies) |
| 3 | **`whitepaper_wizard_spec_v1` R-2 · external-release signatory** (WPW Tier 3) | Named authority + backup for external whitepaper releases. | **W-WPW-TIER-3-DEFERRED WPW-13..WPW-18** (Tier 1+2 proceed unblocked) |
| 4 | **DAP named approving authority (person/role identity)** | Who holds the scope-ratifying authority per `agent_containment_spec_v1` R-2 for DAP-specific requests (Syni.ai is ratified for early deployments — this ruling names the specific person/role at Syni.ai) | **W-DAP-STACK DAP-1 admission ceremonies** proceed with placeholder "Syni.ai" until specific name lands · no wave blocked technically |
| 5 | **`rule_criteria_spec_v1` ROC-1..ROC-11 ratification** | Either drop a standalone `rule_criteria_spec_v1.docx` OR ratify the derived rows in `Master_Requirements_Registry.md` rows 322-332 verbatim OR authorise author-from-citation-trail with derivation caveat. | **All four Rules Service waves** (W-RULE-REGISTRY-BOOTSTRAP · W-RULES-SERVICE-CEREMONY · W-RULE-BOOK-LIBRARY · W-286-RULE-ENUMERATION-CLASSIFY) — see §3.7 DPO |
| 6 | **`whitepaper_wizard_spec_v1` R1 (exceptional retention threshold — R1-a absolute margin or R1-b percentile bar) and R3 (a/b/c DEFAULT ratifications + novelty clause)** | Numeric threshold for R1; sub-rulings for R3. Framed crisply in `STATE/WPW_CHARTER.md`. | **W-WPW-TIER-3-DEFERRED** (same wave as ruling #3) |

Plan default: **hold on rulings #1, #3, #5, #6** for their respective waves. **Rulings #2 and #4 are non-blocking technically** — proceed with placeholder/labelling until rulings land.

---

## §5 · Background GPU campaign — status + remaining runway

**What we're running:** The three-day full-consumption campaign on `akki-vm` (Campaign A · Baseline Ladder) + `akki-vm-ii` (Campaign B · Method Ablations). Owner directive: "full-consumption GPU obligations remain interrupt-priority" (STANDING_ORDERS §5).

**Numbers on record:**
- **78 unique run_ids** across queue manifests + baseline_lines + solva_runs (roster at `notes/models_roster.json`). Owner target 77 met.
- **State breakdown per owner honest-state map** (2026-09-09T~12:20Z verbatim): 70 "under evaluation" · 8 "pilot" · 0 "did not complete".
- **Version breakdown:** 52 v2.1 · 11 v2 · 8 pilot-v1 · 6 sealed-clean baseline · 1 solva.

**Window-fill guarantee:** `queue_followon_launcher.py` + `on_host_queue_dispatcher.py` + dispatcher-respawn-on-death (W-WINDOW-FILL-RESTORE-2 · already banked at floor 3006). Both dispatchers idempotent; both hosts reattach after session interruption via `campaign_infra.reconcile.pull_and_bank`.

**Watchdogs:**
- `tools/on_host_watchdog.sh` on each host — dispatcher heartbeat monitor; auto-restart on death.
- Ratchet-side: `test_launcher_respawns_dead_dispatcher.py` invariant (STEP 1 close).
- Fallback burns at `phase0/gpu_burn/` + `phase0/gpu_fill_burns/`; never mixed into `shield-train/*` or `baseline_lines/*` (STANDING_ORDERS §5).

**Remaining runway:** as of 2026-09-09 · window opened 2026-09-06 · budget was 72 productive hours · **72h campaign window closes 2026-09-09 evening.** Owner has previously ruled ("Commercial after baselines") that baselines complete before commercial waves.

**Post-campaign work stream:** window-close ceremony (WPW Tier 1+2 drafts fired per baseline_line record); data collection feeds Doc 14 Model Ecosystem rows; adapter walk sha256 banked per run per already-live `on_host_trainer.py`.

**Nothing in this plan opens or closes a campaign run.** The campaign machinery is self-driving; the plan is orthogonal.

---

## §6 · Known debt — 165 quarantined tests (D1a-1 event-loop teardown)

**What it is:** 165 tests across 6 async-heavy test files were quarantined 2026-08-27 via `pytestmark = pytest.mark.skip(reason=...)` after all four attack rungs on `D1a-1 event-loop fixture teardown` failed (rungs 1-3 real attempts, rung-4 fallback applied per owner authorisation). Root cause: pytest-anyio + FastAPI TestClient interaction producing 105 fixture-teardown errors on "Event loop is closed" during ASGI shutdown. Owner ruled 2026-08-27: "acceptable ceiling: the D1a-1 files only."

**Files quarantined:**
- `test_admission_ledger_v1.py`
- `test_admission_v1_ledger_read.py`
- `test_admission_end_to_end.py`
- `test_admission_row_persistence.py`
- `test_admission_wave2_row_ledger.py`
- `test_admission_wave2_ledger_probe.py`

**Status delta today:** owner's HOLD message says "159 quarantined tests"; on-disk today shows **165** (166 in test session — 165 D1a-1 quarantine + 1 legacy conditional skip). The 6-test drift may be:
- (a) 6 tests have been surgically un-quarantined and are running elsewhere (not surfaced in DECISIONS.md tail),
- (b) the owner's memory is one-generation stale (159 was a prior count post-partial-un-quarantine that got re-quarantined), or
- (c) a mislabel.

**DEFAULT-PENDING-OVERRIDE:** treat the debt as **165 currently-quarantined tests** (the on-disk truth), name the 6-test discrepancy in the plan for owner correction, hold at floor `passed_floor=3098 · skipped=1 (166 – 165 quarantine)`.

**Proposed clearance point in the sequence:** clear the D1a-1 debt AFTER `W-DAP-STACK` waves 1-3 land (admission + controlled-unit-registry + chokepoint) because those waves rewire the admission surface the 165 tests originally exercised. Attempting clearance before that risks re-hitting the same fixture-teardown class on a re-written surface.

**Effort class for clearance:** M (~1-2 weeks; per-file recompose with the new async fixture pattern that emerged in newer waves).

**Test gate on clearance:** each un-quarantined file passes on its own AND under `BASELINE_GUARD=1` full-suite AND with a real Redis + real Mongo instance (not just mocked seams — the D1a-1 root cause was seam-mocked lifecycle mismatch).

---

## §7 · Standing quality gate — the double-green close rule

Every wave in this plan closes the same way:
1. **Grounding brief** authored under `notes/<wave>_grounding_brief.md` before any code, verbatim spec-ID quote in §A, wave-honest-limits in §E, commit protocol in §F (STANDING_ORDERS §3).
2. **Mechanical RED** captured before code lands. Receipt at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_<wave>_<cp>_RED_pre_impl.log`. Right-reason failure required.
3. **GREEN** on the new tests after implementation.
4. **Full BASELINE_GUARD=1 double-green byte-match.** Terminal `pytest` twice back-to-back, byte-identical counts. Both receipts banked.
5. **Ratchet floor bump in tandem.** `counts_at_baseline.passed` + `invariants_enforced_when_baseline_guard_1.passed_floor` both updated; `ratchet_history` entry appended with commit SHA + one-line note.
6. **Two-commit pattern.** Commit A: code on `programme/track-a`. Commit B: STATE + notes + phase0 receipts on workspace `master`.
7. **No push.** Local commits are the record.
8. **Mission-framed owner report at every landing** unless owner has explicitly reduced cadence for the wave (as at 2026-09-09T~12:20Z for W-REGISTRY-FULL-BUILD CP2-CP7).

**Current ratchet floor: 3098** (post-CP9 close on `programme/track-a` `ff20aac`). Every wave in this plan is expected to raise it monotonically.

---

## §8 · Sequencing skeleton (metrics-only · not an order request)

Per STANDING_ORDERS §2 ("sequencing is an owner ruling"), the following is a metrics-only proposal derived from owner rulings + technical fan-in. **Owner rules order.**

**Foundation (interrupt-priority):**
1. **W-REGISTRY-FULL-BUILD CP10** — 1 remaining CP · ready to fire the moment owner approves this plan.
2. **W-SOLVA-V2-LIFT** — queued immediately behind per owner 2026-09-06T~19:20Z.

**Rules stack (blocked on ROC ruling):**
3. **Rules Service four waves** — hold on ROC ruling #5.

**DAP stack (revenue-bearing):**
4-12. **W-DAP-STACK waves 1-9** — technically independent of Rules Service ROC; owner may prioritise ahead of Rules Service if commercial launch requires. DAP-6 alone waits on ruling #1.

**Doc 0 attributes (governance closure):**
13-19. **W-DOC0-ATTR{1,2,3,6,7,8,10}** in fan-in order per Attribute 12: 1→2→3, then 6, then 7+8, then 10.

**Product surfaces (post-Registry):**
20-22. W-DATA-SUITE-v2-LIFT · W-TRUST-SURFACE-v2 · W-EXECUTIVE-SUITE-v2-LIFT.

**Whitepaper stack:**
23. W-WPW-TIER-1-2 (unblocked · can fire any time in parallel with foundation waves).
24. W-WPW-TIER-3-DEFERRED (owner rulings #3 and #6).

**Debt clearance:**
25. D1a-1 quarantine clearance (after DAP-1..3).

**Amendment ceremony:**
26. W-PRUNING-UNLEARNING (unblocked · can fire any time).

**Every downstream wave has a foundation dependency named in its §3 subsection above.** Owner may collapse, split, or parallelise per capacity.

---

## §9 · Discipline seal

- **Read-only until owner approves.** No new build fires until owner rules.
- **CP10 stays uncommitted** until owner rules on the CP2-CP9 landings that happened before HOLD arrived. Owner may accept them, roll them back, or steer differently.
- **Campaigns untouched.** Full-consumption obligation continues under existing dispatcher/watchdog machinery; not paused.
- **Every factual claim in this file traces to a file opened in this session.** Verbatim spec IDs sourced from `notes/spec_id_index.json` (24 spec IDs · 11 design IDs · sha256-locked).
- **Owner rulings banked verbatim** in `STATE/DECISIONS.md` on every ruling — including the HOLD directive that opened this plan.

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
