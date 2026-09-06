# Gaps → Wave Proposals · LIFT / ADAPT / BUILD estimates

**Authored:** 2026-09-06T~17:45Z  
**Discipline:** every gap in canon (Doc 0 G-1..G-13 + Security Amendments T/W-1..W-8 + Promise Set Amendments 1-8 + S-7 spec gap + Rules Service Spec R-1..R-4 + Registry Enforcement-Class blankness) is mapped to a proposed wave charter. **No wave is fired here — this is a menu for owner sequencing.**

Estimate scale (borrowed from prior reuse-audit discipline):
- **LIFT** — the canon fix is documentary only; effort is authorship + ratification, no new code path.
- **ADAPT** — the mechanism already exists (in another subsystem or as a pattern) and needs generalising, extending, or wiring to a new object. Effort: 1-2 waves.
- **BUILD** — new code path required. Effort: full wave (mechanical RED → GREEN → double-green → ratchet).

Each entry cites the source finding, the fix specification (verbatim where Doc 0/amendments give one), the LIFT/ADAPT/BUILD classification, dependencies (must-close-before), and a one-line wave charter proposal.

## §A · Doc 0 Gaps (G-1 .. G-13)

### G-1 · No Enumerated Trusted Computing Base · Documentary
- **Fix (verbatim):** "Apply the Attribute 1 test to every component in Part 2 and publish the result as a Rule-Registry-tracked artefact, versioned and change-controlled like any governed configuration (Attribute 9). First-pass membership: SyniSense's chokepoint function and custody-sequence logic (BR-1.1, BR-1.2); the Watch's response half pending R-3; the Ledger's writer (BR-8.3); Northena's objective-freeze mechanism (BR-3.1); MOAC's acceptance logic. Explicitly excluded: CIF, Grey Mirror's detection half, the Critic Seam's QA-tier."
- **Classification:** **LIFT** (documentary — apply the test and publish; no code)
- **Dependencies:** R-1 (TCB membership test ratified) · R-3 (Watch membership resolved)
- **Wave charter:** `W-TCB-Enumeration-v1` — apply Attribute 1 test to Part 2 + author `governance_config/tcb_membership.v1.json` + invariant asserting the list is populated + Rules Service track.

### G-2 · No Architecture Description · Documentary
- **Fix (verbatim):** "Produce the description Part 2 of this document already implies: the subsystem list with each entry's classification (SFR-enforcing, SFR-supporting, or non-interfering with respect to governance), declared interfaces per subsystem. Record, as explicit ratified decisions: (a) the Watch sits outside the six because Attribute 12 requires its trust domain separated; (b) promises #5 and #29 are composite theorems, true if and only if their named constituent promises hold, owned jointly."
- **Classification:** **LIFT** (documentary)
- **Dependencies:** G-1 (needs TCB enumeration first for accurate SFR-enforcing classification)
- **Wave charter:** `W-Arch-Description-v1` — author `governance_config/architecture_description.v1.md` per ADV_TDS shape.

### G-3 · Governed Triad Not Formally Classed; Asset Inventory Incomplete · Documentary + Mechanical
- **Fix (verbatim):** "The documentary half is closed by this document's own Part 1 §3 — the classes now exist, defined. What remains is mechanical: tag every existing principal, asset, and operation reference across Documents 1–20 and their extensions against these classes, and extend Mtafiti's registry scope from estate sources to the full asset class, with custody class carried as a typed, queryable attribute per BR-1.4 and BR-4.1 rather than a description in prose."
- **Classification:** **ADAPT** (Mtafiti exists; extend from estate-sources to full asset class + typed custody attribute) + **LIFT** (tag references)
- **Dependencies:** none (Doc 0 §3 already defines classes)
- **Wave charter:** `W-Mtafiti-Full-Asset-Registry` — extend Mtafiti schema to cover {model, artefact, receipt, rule}, add typed `custody_class` column, back-fill Extraction-Akki's shield-train receipts (A-0-v1, A-0-v2 in-flight, B corpora) as registry entries with owners. This wave is a NATURAL FIT for the current shield-train programme — the sealed adapter `49735d51ea…` and its B counterparts are the first asset registry entries.

### G-4 · No Assessment Procedure on Any Rule · Documentary
- **Fix (verbatim):** "Attach an assessment procedure to every rule as part of the Rule Registry rollout already scheduled under rule_criteria_spec_v1 OR-1. Each procedure states its method — examine, test, or both — and its objects, following the AU-3/AU-03a–f pattern verified in Part 1 Attribute 4. Produce the Statement of Applicability as the Registry's own summary view, not a separate document to maintain."
- **Classification:** **LIFT** (documentary per rule) + **ADAPT** (Registry needs SoA view)
- **Dependencies:** Rules Service Spec ratified (RBM-1 requires assessment procedure at authoring; back-fill needed for existing 286 rules)
- **Wave charter:** `W-Rules-Registry-Assessment-Backfill` — attach assessment_procedure column + populate for all 286 existing rules + Statement of Applicability view.

### G-5 · Checkpoint Roles Named Only for the Watch · Documentary
- **Fix (verbatim):** "For MOAC, the chokepoint, the distance gate, and the format gate: name the decision role, the enforcement role (even where co-located), the information point each draws attribute values from, and the administration point where its governing policy is authored — Manage Rules for customer-facing checkpoints, the Attribute 9 procedure (once G-9 closes) for system-facing ones."
- **Classification:** **LIFT** (name roles per checkpoint in the description) + **ADAPT** (record roles as first-class fields in checkpoint definitions)
- **Dependencies:** G-9 (Rules Service Spec closes this for system-facing PAPs)
- **Wave charter:** `W-Checkpoint-Roles-Named` — for each of {MOAC, chokepoint, distance gate, format gate} produce PDP/PEP/PIP/PAP quadruple in a `checkpoint_registry.v1.json`.

### G-6 · No Security Architecture Description; Runtime Self-Protection Unaddressed · Documentary + Mechanical
- **Fix (verbatim):** "Write the description, covering all four ADV_ARC properties for each of the four monitors. For MOAC, the distance gate, and the format gate: (a) state where each monitor's governing policy is stored; (b) confirm that store is unreachable by any code path available to the run or output being evaluated; (c) add a load-time integrity check — a signature or hash comparison against the value recorded in the Rule Registry — so that an unauthorised modification is detected at the point the monitor next loads its policy, not merely prevented by convention."
- **Classification:** **LIFT** (write description) + **BUILD** (load-time integrity check for MOAC / distance / format gates)
- **Dependencies:** G-1 (need TCB enumeration to know which policies are TCB-tier)
- **Wave charter:** `W-Reference-Monitor-Arch-Description-and-Runtime-Integrity` — ADV_ARC description + load-time policy hash-check on each of the 4 monitors.

### G-7 · No Named Security Function Policies; a Subject-Alterable Floor · Documentary + Ruling
- **Fix (verbatim):** "Name every mandatory baseline's SFP explicitly. For the evidence floor: two concrete resolutions, either is sufficient. Option A — re-home the lowering decision under Attribute 9's change-control ceremony. Option B — retain the subject-facing path exactly as built, but rename and re-specify it as a discretionary threshold with its own identity."
- **Classification:** **LIFT** (name SFPs) + **BUILD** (if Option A) or **LIFT** (if Option B, plus renaming)
- **Dependencies:** **R-2 owner ruling**
- **Wave charter:** `W-Mandatory-Baselines-Named-SFP` — name every baseline's SFP over the triad + resolve R-2.

### G-8 · Trust Receipt Omits Identity and Timestamp · Mechanical
- **Fix (verbatim):** "Amend A5.7 to require, in addition to its current content: the invoking principal's identity (from Attribute 3's principal class), and a timestamp from a reliable time source. Add that reliable-time source as its own platform control — the FPT_STM.1 requirement — referenced by SyniSense's receipt and by every other audit-emitting component in Part 2, rather than each component sourcing time independently."
- **Classification:** **BUILD** (reliable-time source as a platform control, referenced by all audit-emitting components) + **ADAPT** (extend trust receipt schema)
- **Dependencies:** none
- **Wave charter:** `W-Reliable-Time-Source-and-AU3-Complete` — build platform time-source control (FPT_STM.1) + extend trust receipt schema with `invoking_principal` and `at_reliable_utc` + retroactive prospective (old receipts unchanged, new receipts complete).

### G-9 · System-Rule Change Control Is Ratification Alone · Documentary
- **Fix (verbatim):** Two-tier procedure (verbatim in Doc 0 §3 G-9 fix). Tier one mirrors Manage Rules ceremony. Tier two follows Watch precedent (BR-7.3): slowest countdown + external witness.
- **Classification:** **LIFT** (procedure) + **ADAPT** (wire into Rules Service Spec RBM-7 and RBM-8, ALREADY DRAFTED in files_11 Rules_Service_Spec_v1.docx)
- **Dependencies:** **R-2, R-3** (see Rules-Service R-1..R-4 rulings) + Rules Service Spec ratification
- **Wave charter:** **CLOSED by Rules Service Spec v1** — RBM-7 (system-ordinary/customer ceremony) and RBM-8 (system-TCB ceremony) directly implement the two-tier fix. Wave becomes `W-Rules-Service-Build` (charter below in §C).

### G-10 · Determinism Boundary Stated, Not Inventoried; Oversight Not Mapped · Documentary
- **Fix (verbatim):** "Classify every Part 2 component as deterministic or learned, in one place, cross-referenced from each component's own entry rather than re-derived per component. Map the existing ruling loop against Article 14's five capabilities explicitly: override is well-evidenced; understand-and-monitor is plausibly served by the STATE/NEXT.md-style tracking already in practice but not confirmed as designed for this purpose; automation-bias awareness, correct interpretation as distinct from override, and halt-to-safe-state for a specific learned component are none of them confirmed and should be treated as open until checked."
- **Classification:** **LIFT** (documentary inventory + Article 14 mapping)
- **Dependencies:** G-1 (TCB enumeration first) · G-2 (arch description gives the frame)
- **Wave charter:** `W-Determinism-Inventory-and-Article14-Map` — one authoritative `governance_config/determinism_boundary.v1.json` + `governance_config/oversight_article14_mapping.v1.md`.

### G-11 · Failure Types Not Enumerated; Posture Undeclared Per Checkpoint · Documentary
- **Fix (verbatim):** "Enumerate failure types per Trusted-Computing-Base and reference-monitor component: what specifically can cause SyniSense's chokepoint, MOAC, or the Ledger's writer to fail to complete an evaluation. Declare posture per checkpoint with its reasoning retained, not only its conclusion — the consumption levers' fail-safe-open choice, reasoned from 'recomputation is a safe, recoverable direction here,' becomes the template future checkpoints are checked against."
- **Classification:** **LIFT** (documentary)
- **Dependencies:** G-1 (which components are TCB)
- **Wave charter:** `W-Failure-Posture-Enumeration` — per-TCB-component failure-type table + fail-closed/fail-safe-open declaration per checkpoint + reasoning retained.

### G-12 · Trust Domains Not Described; Deployment Model Unstated · Documentary + Ruling
- **Fix (verbatim):** "Describe the domains: platform, each tenant, the Watch. Resolve Ruling R-5 — shared infrastructure with tenant-level separation, dedicated infrastructure per tenant, or both offered as distinct deployment options with the boundary stated per instance."
- **Classification:** **LIFT** (documentary) — after **R-5** ruling
- **Dependencies:** **R-5 owner ruling**
- **Wave charter:** `W-Trust-Domain-Description` — three-domain description + deployment model per R-5 outcome.

### G-13 · Job Hand-Off Contract Instantiated Once, Not Generalised · Mechanical
- **Fix (verbatim):** "Generalise the existing pattern rather than inventing a new one: the registered-handoff-contract shape (what / shape / identity / receipt) that already works for ThinkLab → Task Manager becomes a shared checkpoint every subsystem-to-subsystem hand-off routes through. Half the underlying mechanism is already reusable — Northena's objective-freeze is explicitly a shared mechanism, per BR-3.1, not specific to this one crossing. The remaining build is the registration and receipt half: a hand-off registry, owned by Mkondo per its Component 6 scope, that every crossing writes to and every receiving subsystem checks before accepting a hand-off as well-formed."
- **Classification:** **BUILD** (hand-off registry + per-crossing checkpoint) + **ADAPT** (lift ThinkLab pattern)
- **Dependencies:** G-3 (typed operation class) · G-5 (checkpoint roles named)
- **Wave charter:** `W-Handoff-Registry-Generalise` — Mkondo-owned hand-off registry + per-crossing checkpoint invariant + Northena objective-freeze wired in.

## §B · Security Assurance Promise Set Amendments (2026-09-03) · 8 items

Most are documentary (LIFT) — Amendment 6 is a re-classification with build implications for Doc 0.

- **Amendment 1 (S-7 as gap)** — **LIFT** — Update xlsx to mark S-7 Absent → gap · **DEPENDS: nothing** · Charter: `W-Promise-Set-S7-Reclassify` (single-line lift; possibly rolled into Doc 0 v1.1 amendment wave).
- **Amendment 2 (S-10, S-11 given document home)** — **LIFT** — Author Doc 3 Part D "Recovery & Notification" · Charter: `W-Doc3-PartD-Recovery-Notification`.
- **Amendment 3 (A5.4 relocated)** — **LIFT** — Update Doc 0 Attribute 9 build requirements to include A5.4 · Charter: rolled into `W-Doc0-v1.1-Amendment`.
- **Amendment 4 (six unruled bounds explicit)** — **LIFT** — Update xlsx `Bound / Ruling` column for S-2, S-4, S-5, S-19 · Charter: rolled into `W-Doc0-v1.1-Amendment` OR fired independently.
- **Amendment 5 (S-14, S-15 standard column narrowed)** — **LIFT** — Update xlsx `Standard` column to cite GDPR Art. 22 and Kenya DPA 2019 s.35 as legal analogues · rolled into `W-Doc0-v1.1-Amendment`.
- **Amendment 6 (Watch full Reference Monitor)** — **LIFT** (Doc 0 amendment) — Update Doc 0 Part 2 Component 7 tag from "Reference-Monitor-adjacent" to full Reference Monitor. Note G-6 cross-monitor requirement remains open for MOAC / distance / format gates · rolled into `W-Doc0-v1.1-Amendment`.
- **Amendment 7 (A5.9 added to Attribute 11)** — **LIFT** — Add A5.9 as Component 7 build requirement (Att 11 · status Met) · rolled into `W-Doc0-v1.1-Amendment`.
- **Amendment 8 (Doc 3 scope statement for eradicate/communicate/evidence-custody)** — **LIFT** (documentary) OR **BUILD** (if the resolution is Option (a) with a NEW named function) · **DEPENDS: owner ruling on Option (a) vs (b)** · Charter: `W-Doc3-Scope-Statement` (new proposed ruling — see rulings list).

## §C · Trojan Artefacts + Whisper Threats Amendments (2026-09-05) · 10 items

Rulings R-7..R-11 sit at the head of this pack; every wave downstream is blocked on the corresponding ruling (per doc §5).

### T-1 · Artefact Egress Distance Gate (DAP-31)
- **Classification:** **BUILD** — new gate on the deterministic side of the artefact egress path
- **Dependencies:** **R-8 ruling** (threshold + sample size + probe design) · training manifest with per-example provenance (Doc 17 dependency) · MOAC (upstream — not built yet)
- **Wave charter:** `W-Artefact-Distance-Gate` — implements membership-inference + extraction probe (Shokri 2017 / Carlini 2021 patterns) as a deterministic gate on egress. **DIRECTLY RELEVANT to current shield-train programme**: A-0-v1's adapter is banked but never went through this gate; A-0-v2 in-flight and B-REF-v2 pending will also emit adapters without this gate. **Recommend firing this wave FIRST among Trojan/Whisper waves** so future v2+ adapters ship through it.

### T-2 · Base-Model Admission Integrity (DAP-32)
- **Classification:** **BUILD** — mirage-based behavioural probe on admission of external base models
- **Dependencies:** **R-8 ruling** (battery composition + deviation thresholds) · Mirage exists (C1) · Doc 20 provenance register exists
- **Wave charter:** `W-Base-Model-Admission-Probe` — mirage-run probe battery. **Downstream** — programme currently trains on Qwen2.5 base models which entered via a separate admission path; DAP-32 would gate future model admissions.

### W-1 · Output-Content Gate (A5.15 + DAP-33)
- **Classification:** **BUILD** — new deterministic gate at every component-output boundary
- **Dependencies:** **R-8 ruling** · DAP-8 read-set recording (must be complete for scoring)
- **Wave charter:** `W-Output-Content-Gate` — deterministic gate for controlled-content reproduction + ADVISORY tagging. **Complementary to T-1**: T-1 gates artefact egress; W-1 gates output egress from every component.

### W-2 · Recommendation Provenance (A5.16)
- **Classification:** **BUILD** — action record extended with recommendation input · Watch signature mechanism extended
- **Dependencies:** **R-10 ruling** (recommendation window) · W-1 (needs A5.15 tag to attach to)
- **Wave charter:** `W-Recommendation-Provenance` — chain action records to preceding ADVISORY outputs.

### W-3 · Finding Provenance and Sybil Rules (A5.17)
- **Classification:** **BUILD** — two finding classes + collapse logic + friction accounting per raiser · **ADAPT** — extends A5.14 friction budget
- **Dependencies:** W-4 (coalition graph required for lineage collapse) · Watch built
- **Wave charter:** `W-Finding-Provenance-Sybil` — Class D vs Class A findings + lineage-collapse + raiser drift.

### W-4 · Coalition as a Principal (Att 3 addition + A5.18 + DAP-34)
- **Classification:** **BUILD** (coalition graph from admission records + coordination-signature detector) + **LIFT** (Doc 0 Attribute 3 addition)
- **Dependencies:** **R-11 ruling** (coordination-signature threshold for class (c)) · G-3 fix (principal class enumeration)
- **Wave charter:** `W-Coalition-Principal` — connected-component graph from DAP-1/DAP-2 admission edges + Watch detector for class (c).

### W-5 · Structural Independence of Review (QA-3 amended)
- **Classification:** **ADAPT** (Critic Seam QA-3 gets a graph check on assignment)
- **Dependencies:** W-4 (coalition graph)
- **Wave charter:** `W-QA3-Coalition-Independence` — graph-query on reviewer assignment.

### W-6 · Mirage Isolation Extended to Outputs (C1 amended)
- **Classification:** **ADAPT** (extend mirage's containment property to outputs) + **BUILD** (narrow-envelope trigger for coalition members)
- **Dependencies:** W-1 (output gate is the interception point) · W-4 (coalition graph)
- **Wave charter:** `W-Mirage-Bidirectional-Isolation`.

### W-7 · Estate Release Budget (DAP-35 + Att 7 new mandatory baseline)
- **Classification:** **BUILD** (single estate-level accumulator + pre-execution check + differential-privacy composition) + **LIFT** (Doc 0 Attribute 7 amendment)
- **Dependencies:** **R-7 ruling** (budget size — "most consequential value an estate owner sets") · DAP-21 metering (must be complete) · A5.2 unfakeable-signals registry
- **Wave charter:** `W-Estate-Release-Budget` — **highest owner priority per Trojan/Whisper doc §5**: "R-7 is needed before any party is admitted commercially under DAP: without a budget, DAP-35 has nothing to enforce." **BUILD-scope**: single accumulator + composer + refuse-before-execute.

### W-8 · Differentially Private Training by Default (DAP-36)
- **Classification:** **BUILD** — DP-SGD (or ruled equivalent) as the default optimiser · privacy accountant integrated with W-7 budget
- **Dependencies:** **R-9 ruling** (per-run ε, δ) · W-7 (budget must exist to debit) · shield-train programme (this replaces the current LoRA/PEFT optimiser as the default)
- **Wave charter:** `W-DP-Training-Default` — **CRITICAL for current shield-train programme**: none of A-0-v1 sealed adapter or v2 in-flight runs are DP-trained. Making DP the default retroactively affects the pilot/v2 corpus-consistency ruling. **Recommend firing AFTER W-7 (budget must exist), before v2 sealed metrics are treated as production baselines.**

## §D · Rules Service Spec v1 (files_11 · 2026-09-04) · unified wave

The whole spec is a single build charter. It CLOSES G-2, G-4, G-5, G-9 per its own §1.

- **Wave charter:** `W-Rules-Service-Build-v1` — full RBM-1..RBM-22 implementation + Rule Registry (append-only per ROC-11) + rule-book library (RB-PDP FULL + RB-AIG FULL) + profile system + adoption ceremony.
- **Classification:** **BUILD** (subsystem-scale)
- **Dependencies:** **Rules-Service R-1, R-2, R-3, R-4 rulings** (countdown lengths, second signatory, external witness, taxonomy ratification)
- **Feeds:** G-2 arch description (Rules Service is subsystem 17), G-4 assessment procedure per rule, G-5 named PAP for every checkpoint, G-9 documented change-control procedure
- **Extra prerequisite surfaced by this ingest:** Registry `Enforcement Class` column is currently BLANK on the observed 286 rules (see `canon_system_rules_registry_inventory.md` §F). RBM-6 conflict check cannot fire until this classification is populated. Add `W-Registry-Enforcement-Class-Backfill` as a **LIFT** wave preceding Rules Service Build.

## §E · S-7 Learning Mechanism Specification Gap · NEW WAVE (not a canon fix, an authoring exercise)

Doc 3 A1 says platform "learns from every attack it defeats." A5 constrains what may NOT happen. **No mechanism is specified.**

- **Classification:** **RULING + LIFT + BUILD** — this is a specification-authoring exercise, not just a fix
- **Dependencies:** owner input on WHAT should update, on WHAT evidence, at WHAT layer (Doc 3 A5.7 / A5.8 / A5.12 constrain but do not specify)
- **Wave charter:** `W-Doc3-A5-Learning-Mechanism-Spec` — draft a normative mechanism (subject to Rules Service ceremony), covering the three questions above.

## §F · Consolidated wave dependency graph (proposed sequencing)

```
   [OWNER RULINGS: R-1 · R-2 · R-3 · R-5 · R-7 · R-8 · R-9 · R-10 · R-11 · Rules-Service R-1..R-4]
        ↓
   W-TCB-Enumeration-v1 (G-1) ────┐
                                  ├─→ W-Arch-Description-v1 (G-2)
                                  │
   W-Mtafiti-Full-Asset-Registry (G-3, adapts existing Mtafiti)
        ↓
   W-Registry-Enforcement-Class-Backfill (prerequisite for Rules Service)
        ↓
   W-Rules-Service-Build-v1 (closes G-2, G-4, G-5, G-9 · needs Rules-Service R-1..R-4)
        ↓
   W-Reliable-Time-Source-and-AU3-Complete (G-8) — feeds RBM-22 audit records
        ↓
   W-Reference-Monitor-Arch-Description-and-Runtime-Integrity (G-6)
        ↓
   W-Mandatory-Baselines-Named-SFP (G-7 · needs R-2)
   W-Determinism-Inventory-and-Article14-Map (G-10)
   W-Failure-Posture-Enumeration (G-11)
   W-Trust-Domain-Description (G-12 · needs R-5)
   W-Checkpoint-Roles-Named (G-5 already closed by Rules Service)
   W-Handoff-Registry-Generalise (G-13)
   W-Doc0-v1.1-Amendment (Promise Set Amendments 3, 4, 5, 6, 7) — LIFT bundle
   W-Doc3-PartD-Recovery-Notification (Amendment 2)
   W-Promise-Set-S7-Reclassify (Amendment 1) — trivial LIFT
   W-Doc3-Scope-Statement (Amendment 8, needs new ruling)

   [Trojan/Whisper — sequenced per doc §5 note "R-7 needed before commercial admission"]
   W-Estate-Release-Budget (DAP-35 · needs R-7) — HIGHEST OWNER PRIORITY
        ↓
   W-DP-Training-Default (DAP-36 · needs R-9 · needs W-7 budget to debit) — CRITICAL for shield-train
        ↓
   W-Artefact-Distance-Gate (DAP-31 · needs R-8) — DIRECTLY RELEVANT to current programme
   W-Base-Model-Admission-Probe (DAP-32 · needs R-8)
   W-Output-Content-Gate (A5.15/DAP-33 · needs R-8)
        ↓
   W-Coalition-Principal (Att 3 · A5.18 · DAP-34 · needs R-11)
        ↓
   W-Recommendation-Provenance (A5.16 · needs R-10 · needs W-1)
   W-Finding-Provenance-Sybil (A5.17 · needs W-4)
   W-QA3-Coalition-Independence (needs W-4)
   W-Mirage-Bidirectional-Isolation (needs W-1, W-4)

   W-Doc3-A5-Learning-Mechanism-Spec (S-7 spec gap) — owner authoring exercise
```

## §G · Owner sequencing recommendation (for the owner's convenience — **not a decision made here**)

Two natural stacks emerge:

**Stack 1 — Foundation stack (closes Doc 0 gaps that unblock all downstream):**
G-1 → G-2 → G-3 → G-9 (Rules Service Build) → G-4/G-5 (folded into Rules Service).
- Rulings unblocking Stack 1: R-1, R-3, Rules-Service R-1..R-4.
- Effort: ~4 waves. High leverage (unblocks all subsequent wave classifications).

**Stack 2 — Commercial-admission stack (unblocks estate onboarding under DAP):**
R-7 ruling → W-Estate-Release-Budget → W-DP-Training-Default → W-Artefact-Distance-Gate.
- Rulings unblocking Stack 2: R-7 (single most consequential value), R-8, R-9.
- Effort: ~3 waves. **DIRECTLY affects the current shield-train programme** — v2 corpus consistency was ruled by owner this session; DP-by-default would supersede that with a stronger baseline. Owner may want R-9 (per-run ε, δ) resolved before v2 sealed metrics are treated as production references.

**Everything else (G-6, G-7, G-8, G-10, G-11, G-12, G-13, W-1..W-8, Amendments 1-8, S-7 spec gap):** the natural third stack, sequenced per §F graph and owner preference. No wave in this stack blocks the two priority stacks.
