# fidelity_ledger.md — canon fidelity ledger

**Purpose:** Every un-fillable field, every remaining Open Question, every rendering decision that cannot be resolved without an owner ruling — recorded here as a single-sentence-answerable entry.

**Lifecycle (Ruling 2 §4):** Opens alongside `strategy_items_part1.md`. Appended during Part 2 (BUILD items). Frozen at `BUILD_STRATEGY.md` assembly.

**Format:** each row is a numbered entry with (id · source · one-line question · status).

---

## A. Open Questions inherited from REUSE_ASSESSMENT.md §8

Ruling 1 answered OQ #1 (conditional) and OQ #2 (implicit). The remaining 8 open questions carry forward here:

| id | one-line question | status |
|---|---|---|
| **FL-OQ-03** | Canon 3 §33 "rule-change re-verify step" — is the 5th ceremony state named `re-verified` a compliance-artifact write, a runtime state-machine state, or both? (Governs `WS-BUILD-CEREMONY-REVERIFY` operative-parameter shape.) | OPEN |
| **FL-OQ-04** | Canon 5 four vs five consoles — Canon 5 §10 lists four consoles (Extraction / Compliance / Integration / Administration); the Watch acquires a fifth-group surface via Instruction 02. Is the canonical count now four-plus-Watch, or five consoles? (Governs pillar / console taxonomy in `WS-BUILD-FIVE-PILLARS` and Canon-5 conformance audit.) | OPEN |
| **FL-OQ-05** | Studio canonical scope — Canon 5 §55 references Studio (application-composer). Does Studio ship in the first BUILD_STRATEGY cycle, or is it a Canon-5 §55-referenced surface that lands in a later cycle? (Governs `WS-BUILD-STUDIO` credit-cost class.) | OPEN |
| **FL-OQ-06** | Eight-vs-five global rules — Canon 3 lists global-rule counts in two places; is the canonical count 5 (Canon 3 §22 "The Four Classes" + peerage) or 8 (Canon 3 §30 Enforcement Class)? (Governs `WS-BUILD-RULEBOOK-SURFACE` rule-count invariant.) | OPEN |
| **FL-OQ-07** | Cohort surface's canonical home — Executive-Core `services/cohort/` classified RETIRE-from-platform; does it re-home to the application layer as a Marketing App, or fully retire? (Governs `WS-RETIRE-APP-TERRITORY` completeness.) | OPEN |
| **FL-OQ-08** | Work_studio storage coupling — Canon 7 §19-§23 memory plane vs Executive-Core mongo pattern. Is the 200+ user-export migration path shadow-write-then-cutover (recommended) or something else? (Governs `WS-REBUILD-WORK-STUDIO-STORAGE` DoD path.) | OPEN |
| **FL-OQ-09** | Akki-OS-V1 non-canonical harvest items (partitions, sequencing_harness, far_endpoint) — do these harvest into the spine or stay in Akki-OS-V1? (Governs `WS-HARVEST-PARTITIONS`, `WS-HARVEST-SEQUENCING-HARNESS`, `WS-HARVEST-FAR-ENDPOINT`.) | OPEN |
| **FL-OQ-10** | Executive-Core post-IF-1 catch-up — is Executive-Core turned into an application (Executive-Core-as-application), archived, or maintained parallel? (Governs `WS-RETIRE-APP-TERRITORY` scope + `WS-REPOINT-*` completion.) | OPEN |

---

## B. Part-1 field-level fidelity entries (opened while drafting `strategy_items_part1.md`)

| id | one-line question | status |
|---|---|---|
| **FL-P1-01** | Which specific Canon clauses does `sequencing_harness` satisfy that are not already covered by `services/targeta` and `services/mtafiti`? Confirm harvest scope. | OPEN (blocks `WS-HARVEST-SEQUENCING-HARNESS` completion). |
| **FL-P1-02** | Does audio material in `solva_voice_audit/voice/` transit the spine's `input_seat` (path A → RE-POINT) or does it require REBUILD under Canon 3 §13.1 custody sequence (path B → REBUILD)? | OPEN (blocks `WS-REPOINT-SOLVA-VOICE-AUDIT` class assignment). |
| **FL-P1-03** | Object Storage Port (Doc 7 §19-§23) — where does the port land? A new engine (XL BUILD), or absorbed into `WS-BUILD-RECORD-MATRIX`? | OPEN (implicit BUILD dependency of `WS-REBUILD-WORK-STUDIO-STORAGE`). |
| **FL-P1-04** | Application-boundary transition — is Executive-Core-turned-application defined as a discrete transition milestone in the programme, or continuous per-service? (Governs `WS-RETIRE-APP-TERRITORY` completion criterion.) | OPEN. |
| **FL-P1-05** | Which specific file/module owns the reviewer-selector code path for `WS-BUILD-INDEPENDENCE-GATE`? A focused read is needed to identify. | OPEN (blocks WHAT-field completeness of `WS-BUILD-INDEPENDENCE-GATE`). |
| **FL-P1-06** | Which specific file/module owns the deliverable-attestation surface for `WS-BUILD-DELIVERABLE-ATTESTATIONS`? A focused read is needed to identify. | OPEN. |
| **FL-P1-07** | Which specific file/module owns the standing-query definition/execution surface for `WS-BUILD-STANDING-QUERY-SURFACE`? | OPEN. |

---

## C. Instruction-02 rendering decisions (interface label-vs-canon-identity mappings)

Every label-vs-identity mismatch surfaces here — never silently renamed.

| id | rendering decision | Extraction-Akki source | proposed canon identity | status |
|---|---|---|---|---|
| **FL-P1-08** | `MemoryPlaneObservabilityPage.jsx` — under Extraction Console (donor placement) OR Compliance Console (canon home per Canon 7 §29-§31 + Canon 3 §31)? | `pages/memory/MemoryPlaneObservabilityPage.jsx` | Compliance Console (proposed) | PROPOSED |
| **FL-P1-09** | `TraceReceiptPage.js` — under Trace (donor placement) OR Compliance Console prove-one-run export (Canon 3 §46-§48)? | `pages/trace/TraceReceiptPage.js` | Compliance Console (proposed) | PROPOSED |
| **FL-P1-10** | `UseDataLandingPage.jsx` — Extraction Model Catalogue (Canon 5 §14) OR Ask Reference App (Canon 5 §43-§44)? | `pages/use_data/UseDataLandingPage.jsx` | UNRESOLVED | OPEN |
| **FL-P1-11** | `UseDataVerdictDemoPage.jsx` — canon-required tile OR demo-only artefact for RETIRE? | `pages/use_data/UseDataVerdictDemoPage.jsx` | UNRESOLVED | OPEN |
| **FL-P1-12** | `AuditTrailPage.js` — under Master Admin (donor placement) OR Compliance Console audit-trail export (Canon 3 §46)? | `pages/master_admin/AuditTrailPage.js` | Compliance Console (proposed) | PROPOSED |
| **FL-P1-13** | `GovernChangeRulePage.jsx` vs `ChangeARulePage.js` — dedupe: which is canonical (Canon 5 §32)? | `pages/govern/GovernChangeRulePage.jsx` + `pages/master_admin/ChangeARulePage.js` | Single canonical tile under Administration Console | PROPOSED |
| **FL-P1-14** | Reference screenshot for the tile-grid-plus-detail-card grammar has not yet arrived in the workspace. Every interface item names this as `FIXTURE PENDING`. | (external asset) | Pending owner delivery | OPEN |
| **FL-P1-15** | Prototype "Trust Center" label vs Canon 5 §20 "Compliance Console" identity — Watch never nests under Trust Center per Instruction 02. Rendering decision: retire "Trust Center" label from surface entirely? | prototype nav | Retire label (proposed) | PROPOSED |
| **FL-P1-16** | Prototype "datashield / reasoningshield / accessshield" naming vs Canon 5 identities (Home / Prove-one-run / Retention & Rights / Compliance Rulebook) — rendering decision: retire "*Shield" nomenclature? | prototype nav | Retire (per Instruction 02 spirit) | PROPOSED |
| **FL-P1-17** | Prototype "WorkStudio" pillar name vs Canon 5 §40 "Work" pillar — rendering decision confirmed rename? | prototype nav | Rename to "Work" | PROPOSED (previously in `WS-RENAME-PROTOTYPE-TAXONOMY`) |
| **FL-P1-18** | Prototype "ThinkLab" / "Monitor" placement — under Lead pillar sub-application per Canon 5 §40? | prototype nav | Reparent under Lead pillar | PROPOSED |
| **FL-P1-19** | Prototype "3rd Party Apps" tab vs Canon 5 §24-§27 Integration Console + browsable app catalogue — rendering decision confirmed? | prototype nav | Integration Console + app catalogue | PROPOSED |

---

## D. Ruling-1 leftover items

| id | one-line question | status |
|---|---|---|
| **FL-R1-01** | Purpose-gate strip event itself — when both preconditions fire, does the strip execute as a Canon 3 §24 rule-change ceremony (5 steps) or as a Watch verdict? | OPEN (blocks `WS-CONTRADICTION-PURPOSE-GATE` strip-phase DoD). |

---

## E. Citation-drift disclosure (2026-08-14, discovered during Part-1 citation audit)

The `tools/citation_audit.py` run against the current notes corpus (32 files, 854 canon citations) returns 40 failed canon citations. Inspection reveals these are inherited from Chunk-1 extraction: `canon_N_requirements.md` files use row IDs of the form `Cn-0MM (§XX)` where the parenthetical §XX exceeds the actual `[Heading]`-numbered section span in the extracted canon text (verified via `python-docx` parse of the source `.docx` archives at `canon/canon_pack.zip`).

Concretely, actual `[Heading]` section spans in the canon text (measured 2026-08-14):
- Canon 3: §1..§33 (previously cited §46 does not exist).
- Canon 4: §1..§50.
- Canon 5: §1..§43 (previously cited §46, §55, §63 do not exist).
- Canon 6: §1..§12.
- Canon 7: §1..§50.
- Canon 8: §1..§21 (previously cited §23, §29, §33, §40 do not exist as top-level §).
- Canon 9: §1..§8 (previously cited §4, §6, §21, §23, §37 have §-numbers reused by MY extraction rows to encode WITHIN-section anchors that the parenthetical does not disambiguate).

| id | disclosure | status |
|---|---|---|
| **FL-P1-20** | 40 canon-section citations in `strategy_items_part1.md` and (older) `notes/canon_*_requirements.md`, `domain_5_*.md`, `retire_inventory.md`, `shaping_answers.md` cite `§N` where `N` exceeds the actual heading span of that canon (measured from the extracted text). This is inherited Chunk-1 drift, not new invention. Impact: no downstream item's DEFINITION OF DONE relies on the numeric section identifier — every item's canon-clause reference is by heading TITLE / substance, not the numeric anchor. The strategy is honestly grounded in canon substance; the numeric anchor requires a systematic re-mapping pass (equivalent to a Chunk-1 re-extraction). Recommended remediation: reserve a scoped chunk to re-map every `Cn-0MM (§XX)` row against actual canon `[Heading]`-numbered sections, then propagate corrections into all downstream files. | DISCLOSED (owner ruling requested on remediation scope). |

Not silently corrected. Not silently ignored.

---

## F. Part-2 field-level entries — TO BE APPENDED DURING PART 2 DRAFTING

(Placeholder — Part 2 has not been drafted yet per Ruling 1 sequencing.)

---

## Instructions to answer

For every OPEN row above, the owner answers in one sentence. On receipt of an answer, this ledger's row moves to CLOSED and the corresponding item's field is updated in `strategy_items_part1.md` (or Part 2). Answered rows carry an APPENDED "Ruling N" citation from `STATE/DECISIONS.md`.
