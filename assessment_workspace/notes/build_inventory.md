# BUILD Inventory — Chunk 3 running list

Every capability classified BUILD across the 10 domain files. Each row cites the domain, the requirement id(s), and the canon anchor. Cross-refs to domain notes for details.

## Custody & Boundary (5.1)

- **C3-018** — Input-seat as a named canonical surface. Currently the deidentifier serves as the input inspection; Canon 3 §12 names an INPUT-SEAT surface. Deidentifier ≠ input-seat. `Extraction-Akki backend/services/synisense/shield/tenant_entities.py` is close but not named as C3-018 requires.
- **C3-020** — Dual identity at input seat (governance identity at admit; Watch identity when sensing). Watch identity does not exist anywhere → BUILD couples to 5.8.

## Direction & Record (5.2)

- **C3-008 · C3-009 · C3-010** — Actor declaration capture (Canon 3 §6.1). RESOLVED as spec-seam: `services/northena/admit.py:_REQUIRED_KEYS` = 5 fields, but declaration is NOT among them. `mtafiti/declaration.py` is a different concept (per-source declaration baseline). No server-side actor-declaration surface in any repo. Two builds needed: (i) declaration schema + capture surface, (ii) admit-time declaration check.
- Loop end-to-end orchestration (Canon 1 §10 + Canon 4 §35). Gap ranking by carried demand evidence. Partially addressable via HARVEST of `Akki-OS-V1/backend/services/targeta/gap_candidate_filer.py`.

## Measurement / Targeting / Reasoning (5.3)

- **C3-026** — Intent-audit divergence field consumer (currently emitted but unconsumed; consumer is Watch → BUILD couples to 5.8).
- **C3-028** — Machine-checked independence gate on reviewer selector (Solva-pattern independence rule).

## Extraction & Quality (5.4)

- **C4-037 (a-f)** — MOAC six criteria scorecard + measurement pipeline.
- **C4-038 · C4-039 · C4-040** — MOAC evidence from uncurated composition; rights lineage per adapter; adapter version history in registry.
- **C4-067 · C4-068** — MOAC drift measurement + "latest reading is the one in circulation" discipline.
- Critic Seam calibration observability at Compliance Console (Canon 5 §18 + Canon 7 §33) — BUILD companion to 5.5 HARVEST.
- Adapter registry backend + MOAC scorecard surface at Extraction Console (Canon 5 §12.2) — BUILD couples to 5.7.

## Integration (5.5)

- **C1-069 (S6)** — Continuous machine-speed detection/response service sentence (Doc 1 §12). Ties to 5.8.
- **C7-009** — Per-application webhook infrastructure (compliance-record notifications).
- Three-lens envelope surface backend uplift (feeds 5.7 §37 three lenses over one object).

## Governance ceremony (5.6)

- Verification Runner as compliance-console-triggered LIVE surface (Canon 3 §31).
- Regulator pack export as single-button surface (Canon 5 §21) — the "prove one run" and "regulator pack" surfaces.
- Setup + Day-Zero + Working-Rhythm consoles as named surfaces (Canon 6 §3, §4, §5-§7).
- Signed setup record artefact + commissioning certificate artefact.

## Interface (5.7) — LARGE

- **C5-002 · C5-003** — Class-chip inseparable from every claim (component library).
- **C5-004** — Grounding marker walks the proof.
- **C5-005 · C5-006 · C5-007** — Refusal card verbatim copy across every surface.
- **C5-008** — Agent-assumed chip.
- **C5-010–C5-012** — Five consoles as named surfaces (Extraction · Compliance · Integration · Administration · Watch).
- **C5-013** — Registry Dashboard four-quadrant shape (holdings/composition/unmeasured/dormant).
- **C5-014** — Model catalogue with MOAC scorecards (surface pair to 5.4 BUILD).
- **C5-018** — Batch Board with quarantined batches surface (backend HARVEST + surface BUILD).
- **C5-020** — Quality Observation with stale-calibration surface (backend HARVEST + surface BUILD).
- **C5-022–C5-026** — Compliance Console home + prove-one-run + retention & rights + rulebook + rule-on-paper flag.
- **C5-027–C5-030** — Integration Console (register / first-call / administer / dual-actor scoping) — reshape from prototype's apps catalogue.
- **C5-031–C5-036** — Administration Console home + change-a-rule + what-I've-changed + roles & rights + counter-sign duties + verification-runner surface.
- **C5-037–C5-042** — Watch Console (State / Record / Under-Watch / Decisions) + constitutional negatives (5.8 companion).
- **C5-045–C5-048** — Three lenses over one object (Answer / Reasoning / Raw trail).
- **C5-049–C5-051** — Answer card (evidence strip + honesty strip + actions).
- **C5-052** — Five pillars including Lead + Learn.
- **C5-053** — Pulse + News (Lead pillar apps).
- **C5-055** — Studio (Canon 5 §42 "designed, not sourced" application-composer).
- **C5-057** — Learn pillar surfaces.
- **C5-058 · C5-059** — Control band with all five items (Connect / Estate Map / Rulebook / Access / Watch).
- **C5-063 · C5-064 · C5-065** — "Insufficient measurement" render uniform + absence-as-state + standard-copy-same-in-every-context (component library).

## Watch (5.8) — ALL 60 IMPLEMENTABLE ROWS

- Every one of C8-004 … C8-070 (60 implementable rows) is BUILD.
- Grouped clusters (see `notes/domain_5_8.md` for full row-by-row):
  - Machine-speed, cannot-act-unobserved, proves-own-fitness discipline (C8-004–C8-007).
  - Seam: sensing → verdict row → response → action row (C8-008 · C8-055 · C8-056).
  - Three actors: Macho (sensor), Mkono (responder), Witness (C8-009–C8-013, C8-055–C8-059).
  - Register of marks + dimensions + de-mark two signatures (C8-014–C8-018, C8-057).
  - Behavioural profiles + W13 no-reader rule (C8-018 · C8-058).
  - Containment + mirage + expiries + reconciliation (C8-019–C8-026).
  - Reserved decisions + panel discipline (C8-027–C8-029).
  - Watch officer's day + what officer NEVER does (C8-030–C8-033).
  - Standing drills + fitness in receipts (C8-034–C8-039).
  - Peer authorities disagreement (C8-040–C8-044).
  - Constitutional negatives (10 items — C8-045–C8-054, BUILD as design constraints).
  - Interface with CIF (findings cross as detection input; only ratified frames cross back) (C8-066–C8-068).

## Orchestration (5.9) — Canon 9

- **C9-001–C9-003** — Mkondo maintains three registers, structure-only, answers here-not-memory (BUILD-doctrine + BUILD-code).
- **C9-006–C9-018** — Record matrix (each writer→readers row): 13 entries.
- **C9-019–C9-022** — Reading discipline (couples to 5.8).
- **C9-023–C9-035** — Task-identity register: 13 entries.
- **C9-037–C9-042** — Six handoff contracts (chokepoint→model, verdict→response, containment→decision, mirage release→reconciliation, disagreement→resolution, Watch findings→CIF). (C9-036 admission→extraction is PARTIAL, not BUILD.)
- **C9-043–C9-047** — Change & precedence + silence-as-finding.
- **C9-048–C9-050** — Canon 9 doctrinal conclusion (BUILD-doctrine).

## Cross-cutting (5.10)

- **C3-059** — Declaration-required build gate (couples to 5.2 C3-008).
- Defect classes as BUILDs from the taxonomy:
  - C7-D03 (D-Chip) — 5.7.
  - C7-D14 (D-Untraceable-Adapter) — 5.4.
  - C7-D15 (D-MOAC-Missing) — 5.4.
  - C7-D17 (D-Console-Interior) — 5.7.
  - C7-D18 (D-Watch-Interior) — 5.8.
  - C7-D22 (D-Dual-Hat) — 5.9.
  - C7-D23 (D-Cross-Auth-Credential) — 5.9.

## HARVEST inventory (not BUILD-from-scratch, but not REUSE-from-spine)

These are BUILD-adjacent because they must be lifted from Akki-OS-V1 or Executive-Core into the spine. Not counted as pure BUILD; they represent lift-and-shift risk-adjusted at low.

From Akki-OS-V1:
- `services/critic_pass/` (7 files, 950 LOC) — 5.4 & 5.5
- `services/service_1/batch_quarantine.py` (227 LOC) — 5.4
- `services/targeta/gap_candidate_filer.py` (132 LOC) — 5.3
- `services/registry_context/` (5 files) — 5.5
- `services/partitions/session_working_set.py` — 5.5/5.6
- `services/sequencing_harness/` (7 files, 426 LOC) — 5.4
- `services/far_endpoint/` + `services/generated_gates/` — 5.5

From Executive-Core:
- `services/synisense/shield/streaming.py` — 5.1 (Core-2 lacks streaming)
- `services/two_pass.py` refusal templates as Solva-pattern amendment — 5.5

## Summary counts

- **BUILD rows (implementable capability with no code today)**: 145+ (across 5.1–5.10; largest concentration in 5.7 interface and 5.8 Watch).
- **HARVEST rows (lift from Akki-OS-V1 or Executive-Core into spine)**: 9 clusters.
- Every BUILD row above is cited to its domain note; every domain note cites the row's canon anchor.
