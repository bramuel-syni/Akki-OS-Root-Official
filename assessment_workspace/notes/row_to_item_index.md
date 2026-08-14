# row_to_item_index.md — canon row → work item mapping

**Universe:** 591 canon requirement rows (Canon 1..9 + MOAC sub-rows C4-037a..f + defect taxonomy C7-D01..D26).
**Item ID scheme:** `WS-<CLASS>-<TOPIC>-<seq>` or thematic bundles `WS-<TOPIC>`. Bundles group rows that are genuinely one buildable unit per Ruling 1's four-test framing.
**Every non-REUSE row appears in exactly ONE work item.** REUSE rows either have no item (marked `—`) or a WIRING item where new work depends on them.
**Named gaps** section at the end lists rows that would otherwise be silent.

## Bundling rationale

- Bundling is by CANONICAL SEAM (Canon 9 handoff / Canon 8 authority / Canon 4 engine / Canon 3 rulebook stage / Canon 5 console panel) — not by convenience.
- The 6 MOAC criteria (C4-037a..f) bundle as ONE scorecard item because they ARE one scorecard (Canon 4 §26 anchor).
- The 3-actor Watch cluster (C8-009..C8-013 + related) bundles as ONE item because the seam between Macho / Mkono / Witness is explicitly the Canon 8 §6 seam.
- Interface console rows (C5-013..C5-042) bundle by console because each console is its own capability grouping (Canon 5 §10).

## Mapping table

Legend for class: `REUSE` / `MODIFY` / `PARTIAL` / `RE-POINT` / `HARVEST` / `BUILD` / `RETIRE` / `REBUILD` / `N/A-DOCTRINE` / `CONTRADICTION`. The `Item` column shows the work-item ID this row lands in; `—` = no item (REUSE with no wiring, or pure doctrine).

### Canon 1 · The Custody Platform (75 rows)

| Row | Class | Item | Domain | Note |
|---|---|---|---|---|
| C1-001..C1-013 | REUSE / N/A-DOCTRINE | — | 5.1/doctrine | Doctrinal frame. Fail-closed custody (C1-014/015) covered in WIRING WS-WIRE-CUSTODY-DECL (declaration-check integration with existing fail-closed chain). |
| C1-014 · C1-015 | REUSE | WS-WIRE-CUSTODY-DECL | 5.1 | REUSE with new wiring — declaration failure must join fail-closed set. |
| C1-016..C1-019 | N/A-DOCTRINE | — | 5.1 | Unrepresentable-not-policed doctrine. |
| C1-020..C1-027 | REUSE | — | 5.2 | Ledger discipline; single-owner-per-value; twelve doctrines seat rows. |
| C1-028 | N/A-DOCTRINE | — | 5.6 | Runtime-human doctrine. |
| C1-029..C1-035 | REUSE | — | 5.1/5.2 | Inheritance, provenance, canon-before-ruling, single experiment level. |
| C1-036 · C1-037 | N/A-DOCTRINE | — | 5.6 | Precedence, peerage. |
| C1-038..C1-041 | REUSE / PARTIAL | WS-WIRE-CUSTODY-DECL | 5.1 | C1-041 in-perimeter model routing PARTIAL — flagged at 5.1 note. |
| C1-042..C1-054 | REUSE | — | 5.3 | Six-engines seat rows. |
| C1-053 · C1-054 | REUSE | WS-WIRE-REGISTRY | 5.3/5.5 | Function & Promise Registry wiring depends on WS-HARVEST-REGISTRY-CONTEXT to close new registry rows. |
| C1-055..C1-061 | REUSE | — | 5.3 | Estate + two-layer + verdict as lookup. |
| C1-062..C1-067 | PARTIAL | WS-WIRE-LOOP-ORCH | 5.2 | Operating-loop end-to-end orchestration. Depends on WS-HARVEST-GAP-FILER. |
| C1-068..C1-070 | REUSE | — | 5.5 | Six services doctrine. |
| C1-069 (S6) | BUILD | WS-BUILD-S6-WATCH-SERVICE | 5.5 | Watch service sentence — couples with Canon-8 cluster. Part-2 (BUILD) chunk. |
| C1-071 · C1-072 | REUSE | — | 5.5 | Boundary discipline for every application. |
| C1-073..C1-075 | N/A-DOCTRINE | — | 5.5 | Canonical terms + document map. |

### Canon 2 · Conditioned Ideation Faculty (66 rows) — largest un-mapped cluster before this chunk

CIF is heavy on discipline. Every implementable CIF row lands here.

| Row | Class | Item | Note |
|---|---|---|---|
| C2-001..C2-005 | N/A-DOCTRINE | — | Promise + adoption doctrine. |
| C2-006..C2-008 | N/A-DOCTRINE | — | Single-experiment principle. |
| C2-009 | BUILD | WS-CIF-COACH-SEAT | Coach seat + origination port constitutional load-bearing (Canon 2 §12). |
| C2-010 | REUSE | WS-WIRE-SOLVA-CIF | Solva-pattern validation for CIF's own claims. |
| C2-011 | HARVEST | WS-HARVEST-CRITIC-SEAM | Critic Seam extends per CIF pre-ship checklist. |
| C2-012 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE | Independence rule machine-checked (also C3-028). |
| C2-013 | REUSE | — | Bind to run telemetry (existing fields). |
| C2-014 | BUILD | WS-BUILD-WATCH-TO-CIF | Watch findings → CIF detection input (Canon 9 §6 handoff). |
| C2-015 | N/A-DOCTRINE | — | Engine walls seat. |
| C2-016..C2-018 | BUILD-with-HARVEST | WS-HARVEST-CRITIC-SEAM | Manifest schema + submission gate (critic_pass's `manifest_gate.py`). |
| C2-019..C2-023 | BUILD | WS-CIF-ARCHIVE | Living archive four-state discipline + silence-is-data-state + rejection-names-condition + rent + zero-inherited-credibility + paper-first. |
| C2-024 | N/A-DOCTRINE | — | Paper-precedes-compute doctrine. |
| C2-025..C2-028 | HARVEST | WS-HARVEST-CRITIC-SEAM | Naivety pass + pre-ship checklist extend Critic Seam rubric. |
| C2-029 · C2-030 | BUILD | WS-CIF-DETECTION | Frame signature detection (cascade / absorption / misfit). |
| C2-031 | BUILD | WS-CIF-COACH-SEAT | Origination port — only the coach adopts frames. |
| C2-032 · C2-033 | BUILD | WS-CIF-METABOLISATION | Four-step frame-adoption sweep + build check. |
| C2-034..C2-036 | BUILD | WS-CIF-MONITORING | Condition watchers + cascade detection + adversarial elicitation. |
| C2-037..C2-039 | N/A-DOCTRINE | — | Permanent bound — self-certification closed. |
| C2-040..C2-044 | BUILD | WS-CIF-PARAMETERS | Operative parameters (FACT-class) — manifest coverage, archive completeness, escalation latency, metabolisation execution, rent collection. |
| C2-045..C2-051 | BUILD | WS-CIF-PARAMETERS | Quality parameters (measured) — promise metric, manifest hit-rate, provisional honesty, metabolisation closure, overhead ceiling, false-escalation rate, defaults. |
| C2-052..C2-059 | REUSE | WS-HARVEST-CRITIC-SEAM | Enforcement uses standing vehicles + critic-seam amendment. |
| C2-060..C2-066 | N/A-DOCTRINE | — | Governance + what CIF does not do. |

**Named-gap resolution**: Every one of the 47 previously-unassigned Canon-2 rows is now mapped.

### Canon 3 · Governance Engines (61 rows)

| Row | Class | Item |
|---|---|---|
| C3-001..C3-003 | REUSE | — |
| C3-004..C3-007 | REUSE | — |
| **C3-008 · C3-009 · C3-010** | **BUILD (implicit-answered by Ruling 1)** | **WS-BUILD-DECL** — actor-declaration seat + admit-time check + supersession |
| C3-011..C3-017 | REUSE | — |
| C3-018 | BUILD | WS-BUILD-INPUT-SEAT — canonical input-seat surface distinct from deidentifier |
| C3-019 | REUSE | — |
| C3-020 | BUILD | WS-BUILD-INPUT-SEAT-DUAL — dual identity (governance/Watch), couples with Watch cluster |
| C3-021 | REUSE | — |
| C3-022..C3-025 | REUSE | — |
| C3-026 | PARTIAL | WS-WIRE-INTENT-AUDIT-WATCH — divergence-field consumer, couples with Watch |
| C3-027 | REUSE | — |
| C3-028 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE — machine-checked reviewer-selector gate |
| C3-029 | REUSE | — |
| C3-030..C3-032 | REUSE / PARTIAL | WS-BUILD-RULEBOOK-SURFACE — Compliance Rulebook read-back is 5.7 BUILD; rows anchored here |
| C3-033 | **PARTIAL (updated Chunk-3 A.2)** | WS-BUILD-CEREMONY-REVERIFY — 5th step "re-verified" missing |
| C3-034..C3-035 | REUSE / PARTIAL | WS-BUILD-RULEBOOK-SURFACE |
| C3-036..C3-038 | REUSE | — |
| C3-039..C3-042 | PARTIAL | WS-BUILD-VERIFICATION-RUNNER — Compliance-Console-triggered live surface |
| C3-043..C3-045 | REUSE | — |
| C3-046..C3-048 | PARTIAL | WS-BUILD-PROVE-ONE-RUN — Canon 3 §33 export as single action |
| C3-049..C3-051 | N/A-DOCTRINE | — |
| C3-052 · C3-053 | REUSE | — |
| C3-054..C3-058 | N/A-DOCTRINE | — |
| C3-059 | PARTIAL | WS-BUILD-DECL — declaration build gate part of declaration item |
| C3-060 · C3-061 | REUSE | — |

### Canon 4 · Operating Engines (68 rows + 6 MOAC sub-rows)

| Row | Class | Item |
|---|---|---|
| C4-001 · C4-002 | REUSE-doctrine | — |
| C4-003..C4-013 | REUSE | — |
| C4-014..C4-020 | REUSE | — |
| C4-021..C4-025 | REUSE | — |
| C4-026..C4-028 | REUSE | — |
| C4-029..C4-030 | REUSE | — |
| C4-031 | HARVEST | WS-HARVEST-CRITIC-SEAM |
| C4-032 · C4-033 | REUSE | — |
| C4-034..C4-036 | PARTIAL | WS-BUILD-ADAPTER-REGISTRY — adapter surface + no-model-for-class rendering |
| **C4-037a..C4-037f** | **BUILD** | **WS-BUILD-MOAC-SCORECARD** (six criteria one scorecard) |
| C4-038..C4-040 | BUILD | WS-BUILD-MOAC-SCORECARD (uncurated sample + lineage + version history — same scorecard) |
| C4-041 · C4-042 | REUSE | — |
| C4-043..C4-046 | REUSE | — |
| C4-047 | PARTIAL | WS-HARVEST-BATCH-QUARANTINE + WS-BUILD-BATCH-BOARD-SURFACE (see 5.7) |
| C4-048 | REUSE | — |
| C4-049..C4-051 | PARTIAL | WS-WIRE-LOOP-ORCH |
| C4-052..C4-055 | REUSE | — |
| C4-056..C4-060 | PARTIAL | WS-BUILD-DELIVERABLE-ATTESTATIONS — contents / privacy / quality attestation surface |
| C4-061..C4-064 | N/A-DOCTRINE | — |
| C4-065..C4-066 | REUSE | — |
| C4-067..C4-068 | BUILD | WS-BUILD-MOAC-SCORECARD (drift + latest reading is the one in circulation) |

### Canon 5 · Interface Architecture (70 rows) — every Part-2 BUILD row lands here

| Row | Class | Item |
|---|---|---|
| C5-001 | REUSE-doctrine | — |
| C5-002..C5-004 | BUILD | WS-BUILD-CLASS-CHIP-LIBRARY — class chip inseparable from claim + grounding marker |
| C5-005..C5-007 | BUILD | WS-BUILD-REFUSAL-CARD-COPY — verbatim Canon 5 §9.2 refusal card as component |
| C5-008 | BUILD | WS-BUILD-AGENT-ASSUMED-CHIP |
| C5-009 | PARTIAL | WS-BUILD-DORMANT-STATE-RENDER — "what would activate" statement per screen |
| C5-010..C5-012 | BUILD | WS-BUILD-CONSOLES — five consoles as named surfaces per Canon 5 §10 (FL-OQ-04 CLOSED by Build Order 01 §1: five, with Watch as the fifth rendered as fourth Admin-surface tile group per Instruction 02) |
| C5-013 | PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD |
| C5-014 | BUILD | WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE (couples with WS-BUILD-MOAC-SCORECARD) |
| C5-015..C5-017 | REUSE / PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-SHAPING-WIZARD (surface uplift for freeze + sampling) |
| C5-018 | BUILD | WS-BUILD-BATCH-BOARD-SURFACE (couples with WS-HARVEST-BATCH-QUARANTINE) |
| C5-019 | REUSE | — |
| C5-020 | BUILD | WS-BUILD-QUALITY-OBSERVATION (Critic-Seam calibration stale surface; couples with WS-HARVEST-CRITIC-SEAM) |
| C5-021 | REUSE | — |
| C5-022..C5-026 | BUILD | WS-BUILD-CONSOLE-COMPLIANCE (Home + Prove-one-run + Retention & Rights + Rulebook + rule-on-paper flag; couples with WS-BUILD-PROVE-ONE-RUN + WS-BUILD-VERIFICATION-RUNNER + WS-BUILD-RULEBOOK-SURFACE) |
| C5-027..C5-030 | BUILD | WS-BUILD-CONSOLE-INTEGRATION (Register / First-call / Administer / Dual-actor scoping) |
| C5-031..C5-036 | BUILD | WS-BUILD-CONSOLE-ADMINISTRATION (Home + Change-a-Rule + What-I've-Changed + Roles & Rights + Counter-Sign Duties + Verification-Runner surface) |
| C5-037..C5-042 | BUILD | WS-BUILD-CONSOLE-WATCH (four panels; couples with Canon-8 cluster) |
| C5-043 · C5-044 | REUSE / PARTIAL | WS-BUILD-REFERENCE-APP (Ask surface as designed application) |
| C5-045..C5-048 | BUILD | WS-BUILD-THREE-LENSES (Answer / Reasoning / Raw trail over one object) |
| C5-049..C5-051 | BUILD | WS-BUILD-ANSWER-CARD (evidence + honesty + actions) |
| C5-052 | BUILD | WS-BUILD-FIVE-PILLARS (adds Lead + Learn; four-vs-five console reconciliation in fidelity ledger OQ#4) |
| C5-053 | BUILD | WS-BUILD-PULSE-NEWS |
| C5-054 · C5-056 | REUSE | — |
| C5-055 · C5-060 | BUILD | WS-BUILD-STUDIO (application-composer; OQ #5 in fidelity ledger) |
| C5-057 | BUILD | WS-BUILD-LEARN-PILLAR |
| C5-058 · C5-059 | BUILD | WS-BUILD-CONTROL-BAND (five items: Connect / Estate Map / Rulebook / Access / Watch) |
| C5-061..C5-062 · C5-066..C5-070 | REUSE-doctrine | — |
| C5-063 · C5-064 · C5-065 | BUILD | WS-BUILD-COMPONENT-LIBRARY (insufficient-measurement render + absence-as-state + shared visual system) |

### Canon 6 · User Journeys (62 rows)

| Row | Class | Item |
|---|---|---|
| C6-001..C6-006 | REUSE-doctrine | — |
| C6-007..C6-012 | PARTIAL | WS-BUILD-SETUP-CONSOLE (setup surface + signed setup record) |
| C6-013..C6-022 | PARTIAL | WS-BUILD-DAY-ZERO (estate map + commissioning certificate + Verification Runner packs + Watch drills — couples with Canon-8) |
| C6-023..C6-028 | REUSE / PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD (Opportunity Briefs advisory rendering) |
| C6-029..C6-033 | REUSE | — |
| C6-034..C6-037 | REUSE | — |
| C6-038..C6-043 | PARTIAL | WS-BUILD-WEBHOOK + WS-BUILD-REFERENCE-APP |
| C6-044 · C6-045 | REUSE / PARTIAL | WS-BUILD-CONSOLE-COMPLIANCE |
| C6-046..C6-054 | BUILD | WS-BUILD-CONSOLE-WATCH + WS-BUILD-WATCH-DAY (Watch officer's journey — couples with Canon-8 cluster) |
| C6-055 · C6-056 | REUSE | — |
| C6-057..C6-060 | REUSE-doctrine | — |
| C6-061 · C6-062 | N/A-DOCTRINE | — |

### Canon 7 · Integration and Quality (35 + 26 = 61 rows)

Main rows:

| Row | Class | Item |
|---|---|---|
| C7-001..C7-005 | REUSE | — |
| C7-006 | PARTIAL | WS-BUILD-THREE-LENSES (envelope class-chip render) |
| C7-007 | REUSE | — |
| C7-008 | REUSE | — |
| C7-009 | BUILD | WS-BUILD-WEBHOOK |
| C7-010..C7-012 | REUSE | — |
| C7-013..C7-017 | REUSE | — |
| C7-018 · C7-019 | PARTIAL | WS-BUILD-PLANE-PRECOMPUTE + WS-WIRE-WATCH-PLANE-ACTIVITY |
| C7-020..C7-023 | REUSE | — |
| C7-024..C7-028 | HARVEST | WS-HARVEST-CRITIC-SEAM (Critic Seam is the anchor) |
| C7-029..C7-031 | REUSE / PARTIAL | WS-BUILD-STANDING-QUERY-SURFACE |
| C7-032..C7-035 | REUSE-doctrine | — |

Defect taxonomy:

| Row | Class | Item |
|---|---|---|
| C7-D01 · C7-D04..D10 · C7-D13 · C7-D16 · C7-D24 · C7-D25 | REUSE | — |
| C7-D02 · C7-D26 | HARVEST | WS-HARVEST-CRITIC-SEAM (manifest-gate + no-reset-absent) |
| C7-D03 | BUILD | WS-BUILD-CLASS-CHIP-LIBRARY |
| C7-D11 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE |
| C7-D12 | PARTIAL | WS-BUILD-RULEBOOK-SURFACE |
| C7-D14 · C7-D15 | BUILD | WS-BUILD-MOAC-SCORECARD |
| C7-D17 | BUILD | WS-BUILD-CONSOLES (interior-render forbiddance is a design constraint on consoles) |
| C7-D18 | BUILD | WS-BUILD-CONSOLE-WATCH (interior-render forbiddance on Watch console) |
| C7-D19 · C7-D20 | N/A-DOCTRINE | — (unrepresentable-by-design at any future biometric register) |
| C7-D21 | PARTIAL | WS-BUILD-HANDOFF-REGISTRY (Canon 9) |
| C7-D22 · C7-D23 | BUILD | WS-BUILD-TASK-IDENTITY-REGISTER + WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL (Canon 9) |

### Canon 8 · The Watch (72 rows) — ALL BUILD or doctrine

Bundled into cohesive Watch items per Canon 8 §6 seam + §7-§11 authorities + §13-§18 register + §19-§20 drills + §22-§24 officer's day + peer-authority.

| Row | Class | Item |
|---|---|---|
| C8-001..C8-003 | REUSE-doctrine / N/A-DOCTRINE | — |
| C8-004..C8-008 | BUILD | WS-BUILD-WATCH-FOUNDATION (machine-speed + attestation + seam sensing→verdict→response→action) |
| C8-009..C8-013 | BUILD | WS-BUILD-WATCH-ACTORS (Macho sensor + Mkono responder + Witness) |
| C8-014..C8-018 | BUILD | WS-BUILD-WATCH-MARK-REGISTER |
| C8-019..C8-026 | BUILD | WS-BUILD-WATCH-CONTAINMENT (containment + mirage + expiries + reconciliation) |
| C8-027..C8-029 | BUILD | WS-BUILD-WATCH-DECISIONS-PANEL |
| C8-030..C8-033 | BUILD | WS-BUILD-WATCH-DAY (couples with WS-BUILD-CONSOLE-WATCH) |
| C8-034..C8-039 | BUILD | WS-BUILD-WATCH-DRILLS (standing drills + fitness in receipts) |
| C8-040..C8-044 | BUILD | WS-BUILD-WATCH-AUTHORITY-PEERAGE (disagreement + task identity + new-entry-only correction; couples with WS-BUILD-TASK-IDENTITY-REGISTER) |
| C8-045..C8-054 | N/A-DOCTRINE | — (constitutional negatives as design constraints on the other Watch items) |
| C8-055..C8-059 | BUILD | WS-BUILD-WATCH-RECORD-CLASSES (verdict/action/marks/behavioural-profiles/attestation writers — couples with WS-BUILD-RECORD-MATRIX) |
| C8-060..C8-065 | N/A-DOCTRINE | — |
| C8-066..C8-068 | BUILD | WS-BUILD-WATCH-TO-CIF (findings→CIF; only ratified frames cross back) |
| C8-069 · C8-070 | REUSE-doctrine | — (boundary with Doc 9 — sits under Canon 9 handoffs) |
| C8-071 · C8-072 | N/A-DOCTRINE | — |

### Canon 9 · Mkondo Charter (50 rows) — ALL BUILD or doctrine

| Row | Class | Item |
|---|---|---|
| C9-001..C9-003 | BUILD | WS-BUILD-MKONDO-CHARTER (structure-only orchestration service) |
| C9-004 · C9-005 | REUSE-doctrine | — |
| C9-006..C9-018 | BUILD | WS-BUILD-RECORD-MATRIX (13 writer→readers rows) |
| C9-019..C9-022 | BUILD | WS-BUILD-READING-DISCIPLINE (couples with WS-BUILD-CONSOLE-WATCH + WS-BUILD-CONSOLE-COMPLIANCE) |
| C9-023..C9-035 | BUILD | WS-BUILD-TASK-IDENTITY-REGISTER |
| C9-036 | PARTIAL | WS-WIRE-ADMISSION-HANDOFF (already implemented at wizard/admission_handoff.py; wire to registered-contract shape) |
| C9-037..C9-042 | BUILD | WS-BUILD-HANDOFF-REGISTRY (six handoff contracts) |
| C9-043..C9-047 | BUILD | WS-BUILD-MKONDO-CHARTER (change + precedence + silence-as-finding) |
| C9-048..C9-050 | REUSE-doctrine | — |

## Summary — Every non-REUSE row is assigned

- **Total canon requirement rows**: 591
- **N/A-DOCTRINE / REUSE-doctrine rows** (no item): ~200
- **REUSE rows** with no wiring dependency (no item): ~155
- **REUSE rows** with wiring dependency (WIRING item): ~10
- **Non-REUSE rows mapped to a work item**: **~228** (Part-1 classes: MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE ≈ 80 rows; Part-2 BUILD ≈ 148 rows; contradiction ≈ 1 row)

## Work-item universe (deduped by ID)

Every ID that appeared above, once. Class abbreviations: **P** = Part 1 (this chunk), **B** = Part 2 (BUILD chunk, next).

### Part 1 (MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE / WIRING / CONTRADICTION)

Work items assembled from the mapping above.

| Item ID | Class | Rows covered | Item title |
|---|---|---|---|
| **WS-WIRE-CUSTODY-DECL** | WIRING | C1-014, C1-015, C1-038–C1-041 | Fail-closed custody joins declaration verdict |
| **WS-WIRE-REGISTRY** | WIRING | C1-053, C1-054 | Function & Promise Registry ↔ registry_context integration |
| **WS-WIRE-LOOP-ORCH** | PARTIAL | C1-062–C1-067, C4-049–C4-051 | Operating-loop end-to-end orchestration |
| **WS-WIRE-SOLVA-CIF** | WIRING | C2-010 | Solva-pattern validation applied to CIF's own claims |
| **WS-WIRE-INTENT-AUDIT-WATCH** | PARTIAL | C3-026 | Intent-audit divergence-field consumer wiring to Watch |
| **WS-WIRE-WATCH-PLANE-ACTIVITY** | WIRING | C7-019 | Watch reads plane activity (not content) |
| **WS-WIRE-ADMISSION-HANDOFF** | PARTIAL | C9-036 | Existing admission→extraction handoff registered as Canon-9 contract |
| **WS-WIRE-CRITIC-INTO-ANSWERING** | WIRING (Ruling 2) | (couples HARVEST-CRITIC-SEAM into request path) | Critic Seam in-flight on the answering path (§7 of Canon 7, §21-§23 of Canon 4) — separate from the harvest |
| **WS-WIRE-PARITY-EXTENSION** | WIRING (Ruling 2) | (couples every new contract) | Frozen-contract-snapshot parity discipline extended to every new contract this programme creates (Canon-9 handoffs, Watch verdicts, task-identity register) |
| **WS-WIRE-REFUSAL-FAMILY** | WIRING (Ruling 2) | (C5-005..C5-007 UI × C1-020 refusal taxonomy) | Refusal-family taxonomy in `services/memory/refusal.py` + `memory_refusal_reasons.v0.json` wired to Canon 5 §9.2 refusal card surface |
| **WS-WIRE-LEDGER-MATRIX** | WIRING (Ruling 2) | (couples C1-024, C1-027, C9-006..C9-018) | Northena ledger's sole-writer position (services/northena/ledger.py:63 `record()`) promoted to Canon 9 §6-§18 matrix-governed writer |
| **WS-HARVEST-CRITIC-SEAM** | HARVEST | C2-011, C2-016–C2-018, C2-025–C2-028, C2-052–C2-059, C4-031, C7-024–C7-028, C7-D02, C7-D26 | Critic Seam + manifest + amendments + independence hard-check |
| **WS-HARVEST-BATCH-QUARANTINE** | HARVEST | C4-047 (partial) | `services/service_1/batch_quarantine.py` (Akki-OS-V1) |
| **WS-HARVEST-GAP-FILER** | HARVEST | (couples C1-062–C1-067) | `services/targeta/gap_candidate_filer.py` (Akki-OS-V1) |
| **WS-HARVEST-REGISTRY-CONTEXT** | HARVEST | (couples C1-053, C1-054) | `services/registry_context/` (Akki-OS-V1) |
| **WS-HARVEST-PARTITIONS** | HARVEST | (couples C7-013 wiring) | `services/partitions/session_working_set.py` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-SEQUENCING-HARNESS** | HARVEST | (couples with WS-WIRE-REGISTRY) | `services/sequencing_harness/` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-FAR-ENDPOINT** | HARVEST | (couples with WS-WIRE-REGISTRY) | `services/far_endpoint/` + `services/generated_gates/` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-STREAMING** | HARVEST | (couples with RE-POINT cluster) | `services/synisense/shield/streaming.py` (Executive-Core) |
| **WS-HARVEST-TWO-PASS-AMENDMENT** | HARVEST | (couples with Solva-pattern) | `services/two_pass.py` verbatim refusal templates as Solva-pattern amendment (Executive-Core) |
| **WS-REPOINT-ANSWERING-SURFACES** | RE-POINT | (Executive-Core: chat, documents, analyze_workspace, ideas_engine, deck_*, inbox_routing) | RE-POINT answering surfaces onto spine via `SyniSenseContract` adapter swap |
| **WS-REPOINT-SOLVA-V2** | RE-POINT | (Executive-Core `services/solva_v2/`) | RE-POINT narration surface; delegate assertion boundary to spine's `solva_depth` |
| **WS-REPOINT-SOLVA-VOICE-AUDIT** | RE-POINT | (Executive-Core `services/solva_voice_audit/`) | RE-POINT coach-voice surface |
| **WS-REBUILD-WORK-STUDIO-STORAGE** | REBUILD | (Executive-Core `work_studio` storage layer) | Migrate 200+ real user exports to Doc-7 §19-§23 memory plane |
| **WS-REPOINT-WORK-STUDIO-LLM** | RE-POINT | (Executive-Core `work_studio` LLM boundary only) | Adapter swap for shield_invoke calls |
| **WS-CONTRADICTION-PURPOSE-GATE** | CONTRADICTION (conditional under Ruling 1) | (couples C7-011, C7-012) | Executive-Core `purpose_validator` gate RETAINED until WS-BUILD-DECL and WS-BUILD-WATCH-RECONCILER demonstrate firing |
| **WS-RETIRE-APP-TERRITORY** | RETIRE | (Executive-Core cohort/, stripe_webhook, owner_digest, news_aggregator, first_login_password_set, platform_kb, backfill_shield_v1) | Application-territory duplicates (Canon 1 §12/§13/§15) |
| **WS-RETIRE-XCUT-SECURITY** | RETIRE | (Executive-Core csrf, rate_limit, rbac, security_headers, session_timeout, sentry_setup, privacy_wall, clamav_service) | Cross-cutting security duplicates (Canon 5 §11 + Canon 1 §7.1 + Canon 3 §30) |
| **WS-RETIRE-FRONTEND-ARCHIVES** | RETIRE | (Executive-Core `_archived/`, `_archived_legacy/`, `_archived_coverage_loss/`, `website/`) | Codebase-marked archives + marketing website |
| **WS-RETIRE-PROTOTYPE-DIVERGENCE** | RETIRE | (prototype `hrstuff`, `datashield/reasoningshield/accessshield` labels, `compute`, `tasks`, `mentions/emails/projects`) | Prototype-only surfaces without Canon-5 anchor |
| **WS-RENAME-PROTOTYPE-TAXONOMY** | RETIRE (rename-only) | (prototype WorkStudio/ThinkLab/Monitor/Trust/Registry/Build/3rd Party labels) | Rename to Canon 5 §10 taxonomy — no code deletion |
| **WS-BUILD-INDEPENDENCE-GATE** | PARTIAL/BUILD | C2-012, C3-028, C7-D11 | Machine-checked reviewer-independence gate |
| **WS-BUILD-DELIVERABLE-ATTESTATIONS** | PARTIAL | C4-056–C4-060 | Contents / privacy / quality attestation surface uplift |
| **WS-BUILD-CEREMONY-REVERIFY** | PARTIAL (Chunk-3 A.2) | C3-033 | Rule-change ceremony's 5th "re-verified" step |
| **WS-BUILD-STANDING-QUERY-SURFACE** | PARTIAL | C7-029–C7-031 | Standing queries surface for compliance-owner review |

**Part-1 total work items: 47** (11 WIRING · 9 HARVEST (non-interface) · 4 RE-POINT · 1 REBUILD · 4 RETIRE + 1 RENAME · 1 CONTRADICTION · 4 MODIFY/PARTIAL · **13 INTERFACE HARVEST/MODIFY** (Ruling 3)). Ruling 2 promoted 4 WIRING items; Ruling 3 reclassified 13 interface items from Part-2 BUILD to Part-1 HARVEST/MODIFY.

### Part 2 (BUILD) — enumerated here for row-mapping completeness; content deferred to next chunk

| Item ID | Rows covered | Domain |
|---|---|---|
| WS-BUILD-DECL | C3-008, C3-009, C3-010, C3-059 | 5.2 (declaration seat) |
| WS-BUILD-INPUT-SEAT | C3-018 | 5.1 |
| WS-BUILD-INPUT-SEAT-DUAL | C3-020 | 5.1 (couples with Watch) |
| WS-BUILD-MOAC-SCORECARD | C4-037a..f, C4-038, C4-039, C4-040, C4-067, C4-068, C7-D14, C7-D15 | 5.4 |
| WS-BUILD-ADAPTER-REGISTRY | C4-034, C4-035, C4-036 | 5.4 |
| WS-BUILD-CONSOLES | C5-010, C5-011, C5-012, C7-D17 | 5.7 |
| WS-BUILD-CLASS-CHIP-LIBRARY | C5-002, C5-003, C5-004, C7-D03 | 5.7 |
| WS-BUILD-REFUSAL-CARD-COPY | C5-005, C5-006, C5-007 | 5.7 |
| WS-BUILD-AGENT-ASSUMED-CHIP | C5-008 | 5.7 |
| WS-BUILD-DORMANT-STATE-RENDER | C5-009 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD | C5-013, C6-023..C6-028 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE | C5-014 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-SHAPING-WIZARD | C5-015, C5-016, C5-017 | 5.7 |
| WS-BUILD-BATCH-BOARD-SURFACE | C5-018 | 5.7 |
| WS-BUILD-QUALITY-OBSERVATION | C5-020 | 5.7 |
| WS-BUILD-CONSOLE-COMPLIANCE | C5-022..C5-026, C6-044, C6-045 | 5.7 |
| WS-BUILD-CONSOLE-INTEGRATION | C5-027..C5-030 | 5.7 |
| WS-BUILD-CONSOLE-ADMINISTRATION | C5-031..C5-036 | 5.7 |
| WS-BUILD-CONSOLE-WATCH | C5-037..C5-042, C6-046..C6-054, C7-D18 | 5.7 (couples with Canon 8) |
| WS-BUILD-REFERENCE-APP | C5-043, C5-044, C6-038..C6-043 | 5.7 |
| WS-BUILD-THREE-LENSES | C5-045..C5-048, C7-006 | 5.7 |
| WS-BUILD-ANSWER-CARD | C5-049, C5-050, C5-051 | 5.7 |
| WS-BUILD-FIVE-PILLARS | C5-052 | 5.7 |
| WS-BUILD-PULSE-NEWS | C5-053 | 5.7 |
| WS-BUILD-STUDIO | C5-055, C5-060 | 5.7 (OQ #5) |
| WS-BUILD-LEARN-PILLAR | C5-057 | 5.7 |
| WS-BUILD-CONTROL-BAND | C5-058, C5-059 | 5.7 |
| WS-BUILD-COMPONENT-LIBRARY | C5-063, C5-064, C5-065 | 5.7 |
| WS-BUILD-RULEBOOK-SURFACE | C3-030..C3-032, C3-034, C3-035, C7-D12 | 5.6/5.7 |
| WS-BUILD-VERIFICATION-RUNNER | C3-039..C3-042 | 5.6 |
| WS-BUILD-PROVE-ONE-RUN | C3-046, C3-047, C3-048 | 5.6 |
| WS-BUILD-SETUP-CONSOLE | C6-007..C6-012 | 5.6 |
| WS-BUILD-DAY-ZERO | C6-013..C6-022 | 5.6 |
| WS-BUILD-WEBHOOK | C7-009, C6-042 | 5.5 |
| WS-BUILD-PLANE-PRECOMPUTE | C7-018 | 5.5 |
| WS-BUILD-S6-WATCH-SERVICE | C1-069 (S6) | 5.5 (couples with Canon 8) |
| WS-BUILD-WATCH-FOUNDATION | C8-004..C8-008 | 5.8 |
| WS-BUILD-WATCH-ACTORS | C8-009..C8-013 | 5.8 |
| WS-BUILD-WATCH-MARK-REGISTER | C8-014..C8-018 | 5.8 |
| WS-BUILD-WATCH-CONTAINMENT | C8-019..C8-026 | 5.8 |
| WS-BUILD-WATCH-DECISIONS-PANEL | C8-027..C8-029 | 5.8 |
| WS-BUILD-WATCH-DAY | C8-030..C8-033 | 5.8 |
| WS-BUILD-WATCH-DRILLS | C8-034..C8-039 | 5.8 |
| WS-BUILD-WATCH-AUTHORITY-PEERAGE | C8-040..C8-044 | 5.8 |
| WS-BUILD-WATCH-RECORD-CLASSES | C8-055..C8-059 | 5.8 (couples with WS-BUILD-RECORD-MATRIX) |
| WS-BUILD-WATCH-TO-CIF | C2-014, C8-066..C8-068 | 5.8/5.5 |
| WS-BUILD-WATCH-RECONCILER | (couples with WS-BUILD-WATCH-ACTORS Macho) | 5.8 (named by Ruling 1) |
| WS-BUILD-MKONDO-CHARTER | C9-001..C9-003, C9-043..C9-047 | 5.9 |
| WS-BUILD-RECORD-MATRIX | C9-006..C9-018 | 5.9 |
| WS-BUILD-READING-DISCIPLINE | C9-019..C9-022 | 5.9 |
| WS-BUILD-TASK-IDENTITY-REGISTER | C9-023..C9-035, C7-D22 | 5.9 |
| WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL | C7-D23 | 5.9 |
| WS-BUILD-HANDOFF-REGISTRY | C9-037..C9-042, C7-D21 | 5.9 |
| WS-CIF-COACH-SEAT | C2-009, C2-031 | Canon 2 |
| WS-CIF-ARCHIVE | C2-019..C2-023 | Canon 2 |
| WS-CIF-DETECTION | C2-029, C2-030 | Canon 2 |
| WS-CIF-METABOLISATION | C2-032, C2-033 | Canon 2 |
| WS-CIF-MONITORING | C2-034..C2-036 | Canon 2 |
| WS-CIF-PARAMETERS | C2-040..C2-051 | Canon 2 |

**Part-2 total work items: 42** (Ruling 3 moved 13 items into Part 1).

**Grand total work items: 89** (47 Part-1 + 42 Part-2). After Ruling 2: 85 → 89 via four promoted WIRING items. After Ruling 3: grand total unchanged (redistribution 34/55 → 47/42).

### Ruling 3 interface reclassification (Part 2 → Part 1)

The following items moved from Part 2 BUILD → Part 1 HARVEST or MODIFY (Extraction-Akki donor in every case):
- `WS-BUILD-CONSOLES` → `WS-HARVEST-SHELL-GRAMMAR` (HARVEST — donor: `AkkiShell.jsx`, `AkkiV4Shell.jsx`, `CanonOSShellPage.jsx`)
- `WS-BUILD-CLASS-CHIP-LIBRARY` → `WS-HARVEST-CLASS-CHIP-LIBRARY` (HARVEST — donor: `ClassBadge.js`, `ResponseClassPanel.jsx`)
- `WS-BUILD-DORMANT-STATE-RENDER` → `WS-HARVEST-DORMANT-STATE` (HARVEST — donor: `ProveDormantPage.jsx`, `TeamDormantPage.jsx`)
- `WS-BUILD-CONSOLE-EXTRACTION-*` (dashboard, shaping-wizard) → `WS-HARVEST-CONSOLE-EXTRACTION` (HARVEST — donor: `pages/registry/`, `pages/memory/`, `pages/use_data/`)
- `WS-BUILD-CONSOLE-COMPLIANCE` → `WS-HARVEST-CONSOLE-COMPLIANCE` (HARVEST — donor: `pages/prove/`, `pages/govern/` [Retention/Holds/RefusalHealth/Home/EstateRules], `pages/commission_view/`)
- `WS-BUILD-CONSOLE-INTEGRATION` → `WS-HARVEST-CONSOLE-INTEGRATION` (HARVEST — donor: `pages/connect/`, `UseDataDeveloperSurfacePage.jsx`)
- `WS-BUILD-CONSOLE-ADMINISTRATION` → `WS-HARVEST-CONSOLE-ADMINISTRATION` (HARVEST — donor: `pages/master_admin/`, `pages/team/`, `pages/govern/` [Pending/ChangeRule/Registries])
- `WS-BUILD-COMPONENT-LIBRARY` → `WS-HARVEST-COMPONENT-LIBRARY` (HARVEST — donor: 8 atom components)
- NEW: `WS-HARVEST-REFUSAL-CARD` (donor: `RefusalCard.js`; couples with `WS-WIRE-REFUSAL-FAMILY`; replaces the render-side of `WS-BUILD-REFUSAL-CARD-COPY` which stays Part 2 as copy-only)
- NEW: `WS-MODIFY-PLANE-OBSERVABILITY` (rehome from Extraction → Compliance)
- NEW: `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (`TraceReceiptPage.js` rehome)
- NEW: `WS-MODIFY-USE-DATA-PLACEMENT` (Model Catalogue vs Ask Reference App — rendering decision pending)
- NEW: `WS-MODIFY-VERDICT-DEMO` (canon-required or RETIRE — rendering decision pending)
- NEW: `WS-MODIFY-AUDIT-TRAIL-PLACEMENT` (`AuditTrailPage.js` rehome)

`WS-BUILD-CONSOLE-WATCH` REMAINS Part 2 BUILD (Instruction 02 exception; new placement constraint encoded in its DoD).

Auth pages (`AuthLoginPage.js`, `AuthRegisterPage.js`) fold into existing `WS-RETIRE-APP-TERRITORY`.

## Named gaps (rows with no work item that are not doctrine-only)

None. Every non-doctrine row is assigned to exactly one work item. The 47 previously-unassigned Canon-2 CIF rows are resolved (some to doctrine, most to new `WS-CIF-*` items).

The 8 remaining Open Questions (from Assessment §8, minus OQ#1 conditional-answered and OQ#2 implicit-answered) become fidelity-ledger entries inside BUILD_STRATEGY.md and do NOT gate item creation.

## Auditability

- Every canon row above cites its class and item.
- Every Part-1 item is drafted in `notes/strategy_items_part1.md`.
- Every Part-2 item is drafted in `notes/strategy_items_part2.md` (next chunk).
- Mechanical audit: `tools/citation_audit.py` verifies file + canon citations across all notes files + BUILD_STRATEGY.md.
