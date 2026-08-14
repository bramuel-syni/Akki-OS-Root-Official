# Canon 3 — Akki Governance Engines — Extracted Requirements

Source: `/app/assessment_workspace/canon/text/Akki_Canon_3_Governance_Engines.txt`
(extracted from `Akki_Canon_3_Governance_Engines.docx`). Row IDs `C3-###`.

## Part I — Scope and Method

- **C3-001 (§1)**: Doc 3 specifies the three GOVERNANCE ENGINES — Northena (admission and gating), SyniSense (custody chain), Solva (reasoning depth) — plus the compliance rulebook, refusal taxonomy, and rule-change ceremony. The security authority (the Watch, Doc 8) is peer, not subordinate.
- **C3-002 (§1)**: Doc 3 supplies the machine-checkable rules that Doc 1's doctrines commit the platform to. Doc 4 governs OPERATING engines (Mtafiti/Targeta and their services). Where Docs 3 and 4 appear to disagree, Doc 3 governs the GOVERNANCE seam; Doc 4 governs the OPERATIONAL machinery.

## Part II — Northena (Admission + Gating)

### §3–§5 Constitutional properties

- **C3-003 (§3)**: Northena is DETERMINISTIC by construction — no model, no learned weights, no adaptive behaviour. Same inputs → same verdict, always.
- **C3-004 (§3)**: Northena computes ONE thing: the verdict on every operation approaching the estate — ADMIT, HOLD, REFUSE.
- **C3-005 (§4 Universality)**: Every operation flows through Northena. First-party surfaces, third-party integrations, agent runs, employee sessions, batch jobs, evaluation drills — all cross the same gate under the same rules.
- **C3-006 (§4)**: No privileged path exists that would let ANY caller bypass Northena, not even Syni itself.
- **C3-007 (§5 Objective freeze)**: On ADMIT, the objective is FROZEN. Its scope, standard, and constraints become immutable for the run. Amendment = a new admission, superseding the prior objective by ceremony, never mutating it in place.

### §6 Declarations

- **C3-008 (§6.1)**: Every actor (human user, agent, service) that touches the platform is DECLARED — role, working interests, seat identity — before any operation. No actor operates undeclared.
- **C3-009 (§6.1)**: Re-declaration is the only mechanism for honest change. A prior declaration is superseded by a new declaration row, never overwritten.
- **C3-010 (§6.2)**: The declaration is used at admit — Northena consults it as an INPUT to the verdict, not as a rubber stamp.

### §7–§9 Verdicts

- **C3-011 (§7)**: Northena's verdict alphabet is EXACTLY THREE outcomes, no fourth: ADMIT · HOLD · REFUSE. HOLD is the acceptable middle state; there is no APPROXIMATE ADMIT.
- **C3-012 (§7)**: An ADMIT verdict carries: frozen objective, permitted material scope, standards to be met, receipt id, admit timestamp — all bound before execution.
- **C3-013 (§8 Held state)**: A held run has a NAMED holding reason. Rule change in force is the canonical example (the ceremony class per §37). A run is not silently paused.
- **C3-014 (§9 Refusal)**: A REFUSE verdict is a first-class output, not a failure. It carries: reason (compact class name), what would satisfy it if anything would, and refusal receipt id.
- **C3-015 (§9 Run ledger)**: Every admit / hold / refuse is a row on the run ledger — the append-only single record of Doc 1 §4.3. Contract-grade rows: no field is omitted, every column has a value.

## Part III — SyniSense (Custody Chain)

### §10–§13 Custody boundary

- **C3-016 (§10)**: SyniSense is the SINGLE outbound path from the perimeter. Nothing else in the platform is issued outbound capability (Doc 1 §6). Enforced at network layer AND by a static-analysis build gate that fails the build if any other module acquires outbound.
- **C3-017 (§11)**: SyniSense is a per-invocation, per-tenant custody chain. Every outbound call is (a) authorised by the caller's identity and scope, (b) shaped by the tenant's active egress rules, (c) receipted with a tenant-keyed signature.
- **C3-018 (§12 Input seat)**: The custody chain has an INPUT SEAT — content approaching the boundary is inspected under governance rules; a HOLD verdict at the seat blocks the call, rendering as the standard refusal card (Doc 5 §9.2).
- **C3-019 (§13.1 Custody sequence)**: For every outbound model call: (1) input seat inspects; (2) egress redacts to the shielded envelope; (3) call to the model; (4) response wrapped in trust receipt; (5) response classified before it reaches the caller. Steps 1–5 are indivisible.
- **C3-020 (§13.1)**: The input seat runs under GOVERNANCE identity at admission and under WATCH identity when the seat is sensing behaviourally. Two tasks, two identities, one physical point (per Doc 9 §5).
- **C3-021 (§13.2 Trust receipt)**: Every outbound call emits a trust receipt: caller id, model id, egress rule version, input hash, output hash, redaction summary, tenant signature. Receipts are ledger writes owned by SyniSense (Doc 9 §3).

## Part IV — Solva (Reasoning Depth)

### §14–§19

- **C3-022 (§14)**: Solva is the engine built to REASON — multi-step synthesis, cross-source triangulation, hypothesis weighing. Because it is the most capable, it operates under the tightest structural leash.
- **C3-023 (§14.1 The bar)**: Every Solva output must state its claim AT its evidence class, meet the platform's assertion bar for that class, surface contradiction rather than average it away, and refuse where the material cannot support it.
- **C3-024 (§14.2 No confident-with-caveat)**: A confident answer with a caveat is FORBIDDEN. Either the bar is met and the answer is stated at its class, or the answer is REFUSED with a reason.
- **C3-025 (§15 Reasoning traces)**: Every Solva run emits a reasoning trace as a ledger row (Doc 9 §3 — writer = Solva). Includes: intent audit (declared objective vs actual path taken), retrieved evidence with source ids, weighing steps, verdict.
- **C3-026 (§16 Intent audit divergence)**: A divergence field records where the run deviated from its declared intent. This field is emitted for Watch's behavioural sensing per Doc 8.
- **C3-027 (§17 Refusal shapes — three)**: Solva refusals have exactly THREE shapes:
    - **Evidence-class refusal** — material would only support a weaker claim; user offered "Accept as recorded statement / Narrow the objective / Lower the standard" (Canon 5 §9.2).
    - **Coverage refusal** — the material does not reach the objective's scope; what would satisfy is named.
    - **Contradiction refusal** — sources disagree and no reconciliation rule applies; contradiction is surfaced whole.
- **C3-028 (§18 Independence rule for validation)**: A reviewing instance must differ genuinely from the reviewed one — different base model OR materially different context shape. Same-base same-context review shares blind spots and is inadmissible.
- **C3-029 (§19 Solva-pattern validation)**: The pattern (stated-at-class, contradiction surfaced, refusal-with-reason) is the platform-wide validation rubric for every judgement engine, not Solva alone (per Canon 2 §6 CIF's use of it).

## Part V — Compliance Rulebook

### §20–§23

- **C3-030 (§20)**: The Rulebook is the compliance-owner's authored ruleset, versioned, ceremony-changed. Rules cover: retention, deletion, entitlement, mask levels, minimum evidence class per claim type, egress classes, and named refusal defaults.
- **C3-031 (§21 One rule per row)**: Every rule is a single row with: id, statement, current setting, who set it, when, ceremony version, count of automated checks enforcing it.
- **C3-032 (§21)**: A rule with ZERO automated checks is a RULE ON PAPER only — surfaced as such on the Rulebook (Canon 5 §23). Not counted as in force.
- **C3-033 (§22 Rule change ceremony)**: A ceremony is: proposed → counter-signed → waited (countdown class per §37) → applied → re-verified. Every stage is a ledger event.
- **C3-034 (§22)**: While a ceremony is in countdown, affected operations run under HOLD if the current version's setting would be violated by the pending version. Countdown is visible on the Trust Center (Canon 5 §22).
- **C3-035 (§23 Rulebook read-back)**: The Rulebook renders on the Compliance Console with every rule, its automated checks, its firing count over the observation window, and every refusal it produced. A rule that never fired is surfaced as a candidate for retirement or evidence that it is not being tested.

## Part V — Refusal Taxonomy

- **C3-036 (§24 Fixed copy)**: Refusal card fixed copy is:
    - Title: "Not to the standard you asked for"
    - Body: three offered actions in this ORDER — "Accept as recorded statement" · "Narrow the objective" · "Lower the standard"
    - Foot: "A refusal is the system keeping its promise."
- **C3-037 (§24)**: The three actions each map to a specific state change: Accept → the claim is stored at a LOWER class with a note; Narrow → the objective is amended by a new admission; Lower → a new admission with a lower standard replaces the frozen one. All three produce ledger events.
- **C3-038 (§25 Refusal receipts)**: Every refusal is receipted. Refusals are enumerable, exportable, and independently verifiable per §31 (Verification Runner).

## Part VI — Verification Runner

### §31

- **C3-039 (§31)**: The Verification Runner is the compliance-owner's plain-language test-pack executor. Packs run against the LIVE system, not a sandbox.
- **C3-040 (§31)**: Each pack demonstrates a rail firing with its proof (Doc 6 §4). A rail that cannot be demonstrated firing is NOT IN FORCE.
- **C3-041 (§31)**: Standard packs include: personal data masked before any model call; deletion requires two approvers; unanswerable question refused with a reason. Every organisation may add its own.
- **C3-042 (§31)**: The commissioning certificate (Doc 6 §4) is signed on the basis of these packs firing successfully. Signing is a ceremony-grade ledger event.

## Part VI — Ledger Discipline

- **C3-043 (§9 restated)**: The RUN LEDGER is contract-grade. Writer = Northena. Readers = both authorities + compliance surfaces. Per Doc 9 §3.
- **C3-044 (§32 Ledger completeness)**: EVERY admit, hold, refuse, retry, and outcome produces a ledger row before the operation returns to the caller. A response emitted with an unwritten row is a defect (per Doc 7 defect classification).
- **C3-045 (§32)**: Ledger rows are IMMUTABLE. Correction is by a new row citing the corrected id, never by field mutation.

## Part VII — Proof-of-Operation

### §33–§34

- **C3-046 (§33)**: Any operation must be provable end-to-end to an outside party who does NOT hold an account on the system and does NOT need operator cooperation (Doc 1 §1.2 Prove).
- **C3-047 (§33)**: The "prove one run" export packs: admit row · declaration in force · rule versions consulted · retrieved evidence with hashes · trust receipts of any outbound call · verdicts · refusal receipts. Verifiable offline by the receipt's own signatures.
- **C3-048 (§34)**: The regulator pack is a compiled export over a stated window covering EVERY class the regulator requires. Compiled entirely from the record — never assembled by hand.

## Part VIII — Two Authorities Seam

- **C3-049 (§35)**: The governing authority (Northena/SyniSense/Solva plus operating engines) and the security authority (Doc 8 Watch) are peer.
- **C3-050 (§35)**: Where governance ADMITS but the Watch's containment is engaged, the containment holds first — bounded, reversible. The disagreement is escalated for human resolution and recorded in BOTH readings as one entry (Doc 9 §6).
- **C3-051 (§35)**: Neither authority commands the other. Neither's surface renders the other's INTERIOR (Doc 9 §4).

## Part IX — Countdown Classes

### §37

- **C3-052 (§37)**: Every ceremony change has a countdown class binding its wait time. Three canonical classes: fast (measured in hours), standard (in days), slow (in weeks). The class of a rule is a property of the rule, ceremony-set.
- **C3-053 (§37)**: The Mkondo Charter (Doc 9) itself carries the SLOWEST class because it is the boundary of both authorities at once.

## Part X — What Governance Does NOT Do

### §40

- **C3-054 (§40)**: Governance does not decide behavioural intent (Watch territory).
- **C3-055 (§40)**: Governance does not run any operation on the runtime path of a person (Doc 1 §4.7).
- **C3-056 (§40)**: Governance does not maintain a second record (Doc 1 §4.3).
- **C3-057 (§40)**: Governance does not assert a figure it has not measured (Doc 1 §4.4).
- **C3-058 (§40)**: Governance does not offer an override, an emergency mode, an admin bypass, a support-access path (Doc 1 §15).

## Part XI — Enforcement (§41)

- **C3-059 (§41 Static analysis)**: Build gates: outbound-capability check; ledger-write-before-return check; declaration-required-before-operation check; frozen-objective-not-mutated check.
- **C3-060 (§41 Runtime)**: Every operation carries its verdict receipt through response emission; missing receipt = failed request, no exception.
- **C3-061 (§41)**: A gate that CANNOT DEMONSTRATE ITSELF FIRING is not in force (Doc 6 §4). The Verification Runner is the standing demonstration surface.
