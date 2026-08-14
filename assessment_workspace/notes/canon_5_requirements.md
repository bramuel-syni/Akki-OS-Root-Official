# Canon 5 — Akki Interface Architecture — Extracted Requirements

Source: `/app/assessment_workspace/canon/text/Akki_Canon_5_Interface_Architecture.txt`
(extracted from `Akki_Canon_5_Interface_Architecture.docx`). Row IDs `C5-###`.

## Part I — Scope

- **C5-001 (§1)**: Doc 5 specifies the platform's SURFACES — what a person can see, do, and prove — as a fixed architecture of consoles and reference-application surfaces. All surfaces render from the SAME single record (Doc 1 §4.3). No console maintains a private view distinct from the record.

## Part II — Language of the Surface

### §2 Claims and their marks

- **C5-002 (§2.1 Class with claim)**: Every claim on every surface is rendered WITH its evidence class chip — never a claim on its own. The chip communicates whether the claim is measured / declared / inferred.
- **C5-003 (§2.2)**: The class chip is INSEPARABLE from the claim — same visual object, same copy path. A claim rendered without its chip is a defect (Doc 7 defect classification).
- **C5-004 (§2.3 Grounding marker)**: Where a claim traces to a specific source, the grounding marker points to the source id. Clicking the marker walks the proof.

### §3 Refusal grammar

- **C5-005 (§3.1 Refusal card copy — VERBATIM)**:
    - Title: "Not to the standard you asked for"
    - Body actions (in order): "Accept as recorded statement · Narrow the objective · Lower the standard"
    - Foot: "A refusal is the system keeping its promise."
- **C5-006 (§3.1)**: Refusal card is the SAME copy in every context — every surface, every reference application. The card is a component, not a copy pattern.
- **C5-007 (§3.2)**: Three refusal shapes surface as three cards (Doc 3 §17): Evidence-class · Coverage · Contradiction. Each has the same copy pattern with the reason field filled by the specific shape.

### §9 Agent chip and dormant capability

- **C5-008 (§9.3 Agent-assumed chip)**: Where an agent acts on a person's behalf, the AGENT-ASSUMED CHIP renders alongside the resulting content — amber colour token, one-line disclosure, the agent's declared scope resolvable inline.
- **C5-009 (§9.4 Dormant capability)**: A capability the estate does not currently need (Doc 6 §4) renders UNLIT with an explicit "what would activate this" statement. It is NEVER HIDDEN.

## Part III — The Consoles

### §10 The five consoles

- **C5-010 (§10)**: Five consoles: EXTRACTION · COMPLIANCE · INTEGRATION · ADMINISTRATION · WATCH. Each is a grouping of capabilities, defined by WHAT CAN BE DONE THERE — never by a named person (Doc 1 §14).
- **C5-011 (§10)**: Consoles do NOT overlap in capability. Two consoles never expose the same action. A capability that seems to belong to two is a design defect.
- **C5-012 (§10)**: Consoles render from the single record; they do not maintain their own state (Doc 1 §4.3).

## Part IV — Extraction Console

### §12–§19

- **C5-013 (§12.1 Registry Dashboard)**: Renders the estate's measured picture — holdings per source WITH proof links; composition by language/era/type/condition WITH real counts; unmeasured territory DRAWN AS SUCH (never blank); capability the estate does not currently need shown UNLIT (never hidden).
- **C5-014 (§12.2 Models)**: Model catalogue lists every accepted adapter with base model, training lineage, inherited rights, MOAC scorecard (Doc 4 §26), full version history. Before any adapter exists for a class, the surface says so plainly.
- **C5-015 (§14 Shaping Wizard — commissioning)**: Five steps in order (Doc 6 §6):
    (1) Need in plain words · (2) Scope from what registry says exists · (3) Standards and rights against explained defaults · (4) Plan preview — extraction volume as a RANGE, reusable stock already identified, expected coverage of goal, WHAT CANNOT BE COVERED, all before any commitment · (5) Commissioning with confirmation stating precisely what becomes permanent.
- **C5-016 (§15 Freeze)**: The commissioning action freezes the objective (Doc 3 §5). Post-freeze, the surface renders the objective as immutable.
- **C5-017 (§16 Sampling)**: Pre-purchase sampling is a first-class capability. Runs under a scoped admission, receipted, output throwaway unless promoted (Doc 4 §32).
- **C5-018 (§16-A Batch Board)**: A batch board renders quarantined batches with status and resolution path (Doc 4 §34.1). Resolution actions available inline.
- **C5-019 (§17 Registry Administration)**: Source connectors are registered here (Doc 6 §3.11). Sequence: connect → test → for structured sources, confirm the mapping sample. Walked once per source.
- **C5-020 (§18 Quality Observation)**: The Critic Seam's own scorecard (Doc 4 §21) surfaces here, including when its calibration has gone stale (Doc 6 §9).
- **C5-021 (§19 Opportunity Briefs)**: Advisory-throughout briefs proposing what the estate could support. Every figure linked to its measurement. Refreshed as census grows. Marked ADVISORY at every visible line.

## Part V — Compliance Console

### §20–§23

- **C5-022 (§20 Home)**: Compliance Home renders the ceremony countdown (Doc 3 §37), the refusals-with-reasons feed, quarantines with resolutions, deletions with certificates.
- **C5-023 (§21 Prove-one-run)**: One action produces the end-to-end proof export for any operation (Doc 3 §33). Compilation entirely from the record, never assembled by hand.
- **C5-024 (§22 Retention & Rights)**: Retention and rights rules render here with their current settings, who set them, when, ceremony version, count of automated checks enforcing each.
- **C5-025 (§23 Compliance Rulebook)**: The Rulebook renders EVERY rule with its automated checks, its firing count over the observation window, and every refusal it produced.
- **C5-026 (§23)**: A rule with ZERO automated checks is surfaced as RULE ON PAPER only. Not counted as in force.

## Part V — Integration Console

### §24–§27

- **C5-027 (§24 Register an Application)**: An application is registered here — declaration captured, memory-plane parameters configured (Doc 7 Part IV), scoped key issued. Registration is ONE recorded act.
- **C5-028 (§25 First Call)**: The first call from a registered application is treated identically to the thousandth call (Doc 6 §8) — no warm-up period, no unobserved bootstrap. The engineer watches the first call appear in the compliance record IMMEDIATELY.
- **C5-029 (§26 Administer)**: Per-application configuration surface: standing objective shape, memory plane parameters (retrieval scope, write-back with per-cycle volume ceiling, storage ceiling, retention, precompute parameters — Doc 7 §19–23), key rotation.
- **C5-030 (§27 Dual-actor scoping)**: An integration acting on behalf of another actor renders BOTH actors' scopes side by side. The dual-actor chip (Doc 5 §9.3) appears on responses.

## Part VI — Administration Console

### §29–§34

- **C5-031 (§29 Home)**: Administration Home renders the binding banner "Two rules are waiting for you" (or equivalent count) when ceremonies await counter-signature. The banner is the FIRST thing surfaced.
- **C5-032 (§30 Change-a-Rule)**: The change-a-rule flow is here — propose, counter-sign, wait per countdown class, apply. Every stage receipted.
- **C5-033 (§31 What I've Changed)**: A read-back of the changes THIS admin has authored, with dates and effects.
- **C5-034 (§32 Roles & Rights)**: The role register (Doc 6 §2 — instance owner, compliance owner, operator, watch officer) with the declarations in force (Doc 3 §6.1) rendered per role.
- **C5-035 (§33 Counter-Sign Duties)**: The counter-sign queue: ceremonies awaiting my signature, with the proposal walked in full.
- **C5-036 (§34 Verification Runner)**: The plain-language test-pack execution surface (Doc 3 §31). Packs run against the live system; results are receipts.

## Part VII — Watch Console

### §34-A

- **C5-037 (§34-A)**: The Watch Console has EXACTLY FOUR panels — no more, no fewer: STATE · RECORD · UNDER-WATCH · DECISIONS.
- **C5-038 (§34-A.1 State panel)**: Renders two latency figures against their bounds, population and trust standing, spend gauges, last drill (Doc 6 §9-A).
- **C5-039 (§34-A.2 Record panel)**: Renders the Watch's shared reading of the record — findings, containments, verdicts. NOT governance's interior (Doc 9 §4).
- **C5-040 (§34-A.3 Under-Watch panel)**: Renders currently active containments and mirages as OCCUPANCY AND FINDINGS — never the internals of a mirage, never a mark's placement (Doc 8 constitutional negatives).
- **C5-041 (§34-A.4 Decisions panel)**: Renders reserved-decisions (Doc 6 §9-A.5) awaiting human sign-off: promote a containment, extend an expiry, sign a de-mark, resolve authority disagreement, cancel a ceremony in countdown.
- **C5-042 (§34-A CONSTITUTIONAL NEGATIVES)**: The Watch Console explicitly does NOT render: thresholds (they are not tunable through the surface); mark placement (the surface never shows WHERE marks were placed); profile internals (parameters are held per Doc 9 §3, W13 — no surface reads them); mirage construction (never a diagram of how a mirage is built).

## Part VIII — Reference Application (Ask)

### §36–§37

- **C5-043 (§36 Reference App)**: The Reference App is Akki's shipped Ask surface — a first-party application that reaches the platform through the identical governed boundary (Doc 1 §13). It holds no privileged path.
- **C5-044 (§36)**: The Reference App is DESIGNED, not a demo. It is used by real people; its journey is documented in Doc 6.
- **C5-045 (§37.1 Three lenses)**: Every answer in the Reference App is rendered in three progressive-disclosure lenses over ONE object: ANSWER · REASONING · RAW TRAIL. The user opens lenses in place; the lenses do not fork state.
- **C5-046 (§37.2 Answer lens)**: The answer as prose with class chips inline per claim (§2.1) and grounding markers (§2.3).
- **C5-047 (§37.3 Reasoning lens)**: The reasoning trace's readable summary — weighing steps, evidence retrieved, contradiction handling. NEVER a raw model output.
- **C5-048 (§37.4 Raw trail lens)**: The full ledger receipts for the answer — admit row, retrieval hashes, trust receipts, verdict row. Independently verifiable per Doc 3 §33.
- **C5-049 (§38 One card, not two)**: An answer is ONE composed card carrying its evidence strip, honesty strip, and actions. Never presented as two competing views.
- **C5-050 (§38 Actions)**: Standard actions on an answer card: "Break it down" · "Draft the memo" · "Walk the proof". Actions produce new admissions where they cross the boundary.
- **C5-051 (§39 Break-it-down)**: The break-it-down action explodes an answer into its per-claim retrieval basis. Each fragment carries its own class chip and grounding.

## Part IX — Pillars and Control Band

### §40–§42

- **C5-052 (§40 Five pillars)**: The pillar bar has EXACTLY FIVE pillars — LEAD · WORK · BUILD · 3RD PARTY · LEARN. No sixth. No custom-per-tenant pillar.
- **C5-053 (§40 Lead)**: Lead-pillar applications include (at minimum): ThinkLab, Monitor, Pulse, News.
- **C5-054 (§40 Work)**: Work-pillar applications include (at minimum): Chat, Analyze, Documents.
- **C5-055 (§40 Build)**: Build-pillar applications include (at minimum): Train, Studio, Extract.
- **C5-056 (§40 3rd Party)**: The 3rd Party pillar hosts registered external applications (Doc 5 §24).
- **C5-057 (§40 Learn)**: The Learn pillar hosts learning surfaces — reading rooms, walkthroughs, in-context explainers.
- **C5-058 (§41 Control band)**: Beneath the pillars runs the CONTROL BAND with EXACTLY FIVE items: CONNECT · ESTATE MAP · RULEBOOK · ACCESS · WATCH.
- **C5-059 (§41)**: Control-band items are the same across every session; they are not personalisable.
- **C5-060 (§42 Studio)**: Studio is DESIGNED, not sourced. A studio surface where an application is composed against platform primitives — no third-party ingestion of studios into the platform.

## Part X — Shape of Every Surface

### §43–§45

- **C5-061 (§43 One record only)**: Every surface reads from ONE record. No surface holds a private store rebuilt from the record — the record IS what the surface renders (Doc 1 §4.3).
- **C5-062 (§44 No override)**: No surface exposes an override, an emergency mode, an admin bypass, or a support-access path (Doc 1 §15).
- **C5-063 (§45 No compressed value)**: Where a measurement's confidence would require rounding below its floor, the surface renders "insufficient measurement" — never zero, never a compressed asterisk-flagged figure (Doc 4 §9).
- **C5-064 (§45 Absence explicit)**: Absence of an artefact renders as its own state, not as an empty slot. A model that does not exist for a class says so (Doc 6 §8).
- **C5-065 (§45 Same copy)**: Standard components (refusal card, class chips, agent chip, dormant chip) use the SAME copy in every context. Local variation is a defect.

## Part XI — What Interfaces Do NOT Do

### §46

- **C5-066 (§46)**: No surface renders another authority's interior (Doc 9 §4).
- **C5-067 (§46)**: No surface offers a bypass, an override, a shortcut through custody (Doc 1 §15).
- **C5-068 (§46)**: No surface personalises the pillar or control-band composition per tenant.
- **C5-069 (§46)**: No surface renders a claim without its class chip.
- **C5-070 (§46)**: No surface renders an unmeasured region as measured / clean / empty (Doc 4 §6).
