# Canon 1 — Akki, The Custody Platform — Extracted Requirements

Source: `/app/assessment_workspace/canon/text/Akki_Canon_1_Custody_Platform.txt`
(extracted from `Akki_Canon_1_Custody_Platform.docx`). Every entry cites its
Canon-1 section by number. Each row is one concrete required capability,
contract, or binding rule. Row IDs are `C1-###` and stable — they become
Chunk-3 assessment rows.

## Part I — What Akki Is

- **C1-001 (Canon 1 §1)**: Platform runs as a *custody platform* performing four custodian duties on the estate — HOLD, RECORD, SETTLE, PROVE. Requires the platform to implement all four, on data and on AI operations touching data.
- **C1-002 (§1)**: Platform is NOT a model, a model wrapper, or an assistant. All models and all applications reach data ONLY through the platform.
- **C1-003 (§1)**: Single-tenant by construction: one organisation → one installation → one record. No multi-tenant deployment mode; no shared control plane.
- **C1-004 (§1)**: Estate contents (never customer identity) determine which capabilities activate. A media-heavy estate activates perception classes; a text-only estate does not.
- **C1-005 (§1)**: No installation is a development metric for another. No instance-specific assumption may enter the platform's own specification.
- **C1-006 (§1.1)**: Estate is EVERYTHING an organisation holds that an AI system could read — structured stores, documents, message archives, media, calls, tickets, uncatalogued material. Rights-clear AND rights-unclear material both first-class.
- **C1-007 (§1.1)**: The rights-unclear state is treated as a first-class fact, not an administrative footnote.
- **C1-008 (§1.1)**: Same operations apply at every scale — whole org, department, archive, single file. A mechanism working at only one scale is not depended on.
- **C1-009 (§1.2)**: Four verbs describe the whole platform: Measure, Govern, Extract, Prove. Every capability is one of these or a composition of them.
- **C1-010 (§1.2)**: Measure — establishes what the estate actually contains; must state plainly which regions are unmeasured. An unmeasured region is reported as unmeasured, NEVER as empty and NEVER as clean.
- **C1-011 (§1.2)**: Govern — enforces on every operation the rules declared: what may be read, by whom, for what purpose, under what masking, with what evidence.
- **C1-012 (§1.2)**: Extract — converts estate material into qualified facts, trained models, licensed datasets, memory available to applications, as commissioned work priced before it runs.
- **C1-013 (§1.2)**: Prove — every operation emits a receipt verifiable by an outside party WITHOUT an account on the system and WITHOUT operator cooperation.

## Part II — Binding Doctrine (§4)

The twelve doctrines are binding contracts.

- **C1-014 (§4.1 Fail-closed custody)**: If a custody control cannot execute, the operation does not happen. When de-identification cannot run, external calls are refused, naming the cause. No config flag or code path may bypass. A build gate must fail the build if a path around a custody control is introduced.
- **C1-015 (§4.1)**: Custody controls fail closed; cost optimisations fail transparent. Fail-open custody = breach; fail-closed cost optimisation = outage. Both misdirections are defects.
- **C1-016 (§4.2 Unrepresentable, not policed)**: Where a state must never occur, it must be built so the state cannot be expressed (function signature, type, or schema).
- **C1-017 (§4.2)**: The function computing what an answer may claim has no parameter through which a model's confidence can enter.
- **C1-018 (§4.2)**: The register that could hold individual-level identification biometrics (voiceprint, faceprint, any body-identity template) has no field in which such a value could be placed.
- **C1-019 (§4.2)**: Watch's behavioural-conformance parameters (Doc 8) are a different object with a different owner — never a field in the biometric register, and vice versa.
- **C1-020 (§4.3 One record)**: Exactly ONE record. Nothing maintains a second. Every admission/measurement/commission/operation/answer/refusal/rule change/access grant writes to a single append-only ledger.
- **C1-021 (§4.3)**: No service keeps a local log constituting a separate account. Working/scratch state becomes record only when finalised and stamped; the moment of stamping is itself recorded.
- **C1-022 (§4.4 Measure, do not assert)**: No figure enters the system as a claim; every figure carries HOW it was obtained.
- **C1-023 (§4.4)**: Accuracy, coverage, cost, and time are measured on the organisation's OWN material before they are stated. An estimate renders AS an estimate on the number wherever it appears.
- **C1-024 (§4.4)**: Vendor benchmarks / published literature may inform what to measure; they never substitute for the measurement.
- **C1-025 (§4.5 Single owner per value)**: Every value is computed ONCE by ONE component and carried forward as fact. A downstream component does not recompute, re-validate, or second-guess.
- **C1-026 (§4.6 Extension, not proliferation)**: New capability extends an existing component; it does not create a sibling. A new material kind → registry gains a modality, not a sibling registry. A new event class → the record gains a data class, not a second ledger.
- **C1-027 (§4.7 Authority is people; work is the platform)**: No person is placed in the runtime path of an operation. People declare rules, approve rule sets, set escalation criteria, and disposition exceptions.
- **C1-028 (§4.7)**: If the same class of item repeatedly reaches an approver, the criteria are wrong — the fix is to redefine them, never to process the queue faster.
- **C1-029 (§4.8 Inheritance)**: Everything built inside Akki or integrated into it inherits its custody. There is no other way to build. If any application can reach the estate by any route that bypasses the platform, this doctrine is broken.
- **C1-030 (§4.9 Provenance)**: A fact that cannot name its source cannot be stored. Provenance is paired with a fact at the moment of writing, never attached afterwards. A fact arriving without resolvable source is rejected at the boundary.
- **C1-031 (§4.9)**: The same rule applies to capability: a record that a model can perform a task carries which work established that, on what material, when.
- **C1-032 (§4.10 Verdicts never curated)**: Inputs, models, and corpora may be engineered without limit. The evidence a verdict is measured against may not be. Every validating sample is drawn from measured uncurated composition and published internally whatever it says.
- **C1-033 (§4.11 Canon before ruling)**: No decision proceeds from memory or summary where the governing document exists. Unread canon is read before ruling.
- **C1-034 (§4.12 Experimentation at one level)**: The assembled system is the sole object under test. No component beneath it is experimental. Every mechanic deploys in force with conditions of success and quality measured, OR its parameters are undefined (a spec gap to close), NEVER as a pilot/shadow/observe-first.
- **C1-035 (§4.12)**: Gates bind spend, output quality, or a platform claim. They NEVER bind whether a fully specified mechanism runs at all.

## Part II — Precedence & Peerage (§5)

- **C1-036 (§5)**: Precedence order highest first: (1) Doctrine (the twelve); (2) The Promise Register (Part VI); (3) This canon's specifications (Docs 1–9); (4) Implementation convenience — never decisive. A shipped divergence is never retrospective evidence the spec was wrong.
- **C1-037 (§5)**: Where two authorities meet: within the security domain the Watch canon governs; within governance domain this canon and its companions govern; at every seam, Doc 8 peerage clauses and Doc 9 matrix decide. A surviving conflict is a spec defect escalated — never resolved by whichever document was read most recently.

## Part III — Architecture

- **C1-038 (§6 Topology)**: Akki installs inside the organisation's perimeter — data centre, private cloud, or org's own cloud tenancy. Organisation controls infrastructure/network boundary/identity; Syni operates the software.
- **C1-039 (§6)**: Exactly ONE outbound path leaves the perimeter — the custody boundary.
- **C1-040 (§6)**: Nothing else in the platform holds outbound network capability. Enforced by (a) network-layer allowlist refusing outbound from anywhere else, AND (b) static-analysis build gate that fails the build if any other module acquires outbound capability.
- **C1-041 (§6)**: Compute does not leave — models the org hosts and GPU capacity the platform allocates run inside the perimeter. External frontier models are permitted only where "genuinely required", and the custody boundary governs that single crossing.
- **C1-042 (§7 Six engines, three axes)**: The platform is six engines each governing exactly one thing on three orthogonal axes that never collapse: Northena (Direction), SyniSense (Boundary), Solva (Depth), Mtafiti (Measurement), Targeta (Targeting), CIF (Judgement).
- **C1-043 (§7)**: A governor performing another's function creates a single point at which a run could be admitted, bounded, and asserted by the same logic. Disallowed.
- **C1-044 (§7)**: Northena is deterministic by construction — no model, no learned weights, no adaptive behaviour.
- **C1-045 (§7)**: SyniSense is the SINGLE chokepoint through which every outbound model call transits.
- **C1-046 (§7)**: Solva is the one engine built to reason, and therefore built with the tightest structural leash.
- **C1-047 (§7)**: The six engines compose into TWO services connected by TWO named seams (per Doc 4): a service that builds the asset (census/extraction, ending in a frozen unit contract) and a service that serves an objective against it, calling back into the first only for what has not yet converged.
- **C1-048 (§7.1 Two authorities)**: The six engines together are the *governing authority* — the answer to "was this permitted, and is it right?" The Watch (Doc 8) is the *security authority* — "is this intended, and authentic?" Peer, not subordinate.
- **C1-049 (§7.1)**: Neither authority commands the other. Each consumes what the other produces.
- **C1-050 (§7.1)**: Every task in the platform executes under exactly ONE authority's identity.
- **C1-051 (§7.1)**: On disagreement (permitted-but-not-intended): the Watch's containment acts first (bounded, reversible); a person resolves the conflict; the disagreement is recorded.
- **C1-052 (§7.1)**: Record classes, task identity register, and handoff contracts between the two authorities are held in Doc 9 (the Mkondo Charter).
- **C1-053 (§8 Function & Promise Registry)**: One canonical, versioned artifact registers every named function (gate, engine behaviour, worker obligation, console guarantee) with the promise it protects and its full accounting. Every function belongs to one of the six engines or a named surface.
- **C1-054 (§8)**: No gate exists without an honestly statable promise. No promise exists that traces to no function protecting it. Otherwise the function is retired, not preserved.

## Part IV — The Estate

- **C1-055 (§9)**: Estate is treated as a SINGLE measurable object at whatever scale.
- **C1-056 (§9.1 Three states)**: Every region is in EXACTLY one state, rendered with equal prominence wherever the estate is described: (a) Measured — sound; (b) Measured — degraded (specific limitation named); (c) Not yet measured.
- **C1-057 (§9.1)**: An unmeasured region is NEVER rendered as empty, clean, or zero. Absence of measurement is a fact about the platform's knowledge, not about the estate.
- **C1-058 (§9.2)**: Defensibility is produced in TWO layers: a deterministic declaration (per source, always available — the floor) AND an inference layer detecting signals in content (corroboration, contested status).
- **C1-059 (§9.2)**: Inference contributes ONLY after its own accuracy has been proven; until then, declaration stands alone.
- **C1-060 (§9.2)**: Neither layer decides what a measurement means — the verdict is always a governed, versioned lookup, never a model's output.
- **C1-061 (§9.2)**: General rule: learning may detect; it may never decide.

## Part V — The Operating Loop

- **C1-062 (§10)**: Loop: Questions arrive → most answered → unanswered become ranked gaps → gaps become commissioned objectives → extraction changes what next round can answer.
- **C1-063 (§10)**: The loop must continue WITHOUT a role required to be present.
- **C1-064 (§10)**: The record must carry context (why a gap was filed, what was tried, what the material could not support) — not living only in someone's head.
- **C1-065 (§10)**: Demand is DISCOVERED, not forecast — by observing what people try to ask, not by upfront value assessment.
- **C1-066 (§10)**: Loop is self-limiting — when the gap list stops producing high-demand candidates, the estate has been mined to its current questions' depth.
- **C1-067 (§10)**: Each cycle compounds. Cleaner material, better models, and more accurate mining accumulate in the record rather than being rebuilt per project.

## Part VI — Who Akki Serves

- **C1-068 (§11)**: No platform decision optimises an end-user's experience directly. The platform optimises the guarantees it issues to the applications built on it.
- **C1-069 (§12 Six Services)**: Six canonical service sentences (changeable only by rule-change ceremony):
    - S1: to the integrating application — a governed intelligence surface (answers/skills/artifacts with class, receipt, refusal semantics intact).
    - S2: to the operating organisation — estate onboarded, mapped, and turned into qualified intelligence.
    - S3: to the compliance officer — proof of any operation on demand, and governed control of rules over data.
    - S4: to the data buyer — intelligence products independently verifiable before use.
    - S5: to the infrastructure consumer — RESERVED. Not built.
    - S6: to the operating org + compliance officer under threat — continuous machine-speed detection/response, invisible in legitimate use, incapable of acting unobserved, proving its own fitness on a standing cadence. (Doc 8.)
- **C1-070 (§12)**: No platform function is proposed, evaluated, or justified except by tracing to one of these sentences. A function that cannot trace upward is doing the wrong job well.
- **C1-071 (§13 Applications vs platform)**: An application is anything with an end-user in it — internal or external. The boundary is mechanical, not organisational: if a person not running the platform touches it, it is an application.
- **C1-072 (§13)**: Every application enters through the same governed boundary as any third party, holds a scoped key issued the same way, is subject to the same custody on every call. NO privileged path anywhere — not for a first-party surface, not for one built by Syni itself.

## Part VII — Vocabulary and Boundaries

- **C1-073 (§14 Canonical terms)**: These terms have fixed meanings platform-wide: custody boundary, estate, commission, objective (frozen at admission, immutable for the run), the record, receipt, console (a capability grouping, defined by what can be done there — NEVER by a named person), application.
- **C1-074 (§15 What the platform will not do — six absolutes)**:
    - Will not answer beyond its evidence — bounds the claim or declines; no confident answer with a caveat.
    - Will not provide an override — no emergency mode, no admin bypass, no support-access path skipping custody.
    - Will not quote unmeasured figures — not in an interface, not in a report, not in a proposal.
    - Will not maintain a second record.
    - Will not place a person in the runtime path of an operation.
    - Will not know a buyer, a price, or an order — commerce is application territory.

## Part VII — Document map (§16)

- **C1-075 (§16)**: This canon set is Documents 1–9; each downstream doc assumes Doc 1. Where any appears to contradict Doc 1, Doc 1 governs.
