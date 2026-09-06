# Consolidated Owner Rulings · One-Shot List

**Authored:** 2026-09-06T~17:50Z  
**Purpose:** every ruling this ingest wave surfaces, formatted as a one-line question the owner can rule on in a single pass. Nothing here is a decision — decisions are the owner's.

## §A · Doc 0 rulings (from `akki_governance_architecture_v1` Part 3 §3)

- **R-1 · TCB membership test** — Ratify Attribute 1's proposed test (a component is in the TCB iff it is deterministic AND its failure would falsify a guarantee this document or a document it governs makes) as the TCB membership test, or set a different one before the list is published?
- **R-2 · "Lower the standard" resolution (G-7 · evidence floor)** — Option A: re-home the lowering decision under Attribute 9's change-control ceremony (named human authority invokes per instance, on the record) so the evidence floor remains mandatory. OR Option B: retain the subject-facing path exactly as built but rename and re-specify it as a discretionary threshold with its own identity, distinct from and strictly below the assertion floor?
- **R-3 · The Watch's TCB membership** — Include the Watch's service in full in the TCB, or its deterministic response half only (Mkono) with Grey Mirror's detection half (Macho) excluded as learned under Attribute 10?
- **R-5 · Deployment model** — Shared infrastructure with tenant-level separation, dedicated infrastructure per tenant, or both offered as distinct deployment options with the boundary stated per instance?

*(R-4 in Doc 0 was resolved into G-9's two-tier fix directly and does not require a separate owner ruling.)*

## §B · Trojan/Whisper rulings (from `Security_Amendments_Trojan_Whisper.docx` §5)

- **R-7 · Estate Release Budget size** — Per estate, in natural units per data type (audio-hours, text tokens, units) AND as differential-privacy budget (ε, δ). *[Doc note: "The single most consequential value an estate owner sets under this document." Doc says "R-7 is needed before any party is admitted commercially under DAP: without a budget, DAP-35 has nothing to enforce."]*
- **R-8 · Threshold/sample/probe design for DAP-31 + A5.15 + DAP-32** — Reproduction threshold, sample size, and probe design for DAP-31 (artefact egress distance gate) and A5.15 (output-content gate); battery composition and deviation thresholds for DAP-32 (base-model admission probe)? *[Proposed by doc as DEFAULT-class values set conservatively and revised on evidence.]*
- **R-9 · Per-run DP parameter (ε, δ) for DAP-36** — Per-run differential-privacy (ε, δ) for `DAP-36 · DP-training by default`, and the natural-unit multiplier applied to approved non-DP runs?
- **R-10 · Recommendation window for A5.16** — How long after an ADVISORY-tagged output does an action get attributed to it? *[Ruled value.]*
- **R-11 · Coordination-signature threshold for A5.18 class (c)** — The suspicion level at which a set of otherwise-unrelated principals is routed to friction as a coalition? *[Doc §5 note: "R-8 through R-11 are needed before the corresponding gates are built, and each is proposed as a DEFAULT-class value so that building is not blocked on a final number."]*

## §C · Rules Service Spec v1 rulings (from `Rules_Service_Spec_v1.docx` §9)

- **Rules-Service R-1 · Countdown lengths per tier** — Countdown durations for {system-TCB, system-ordinary, customer} ceremonies?
- **Rules-Service R-2 · Second signatory for system-ordinary rules** — Named role, and who currently holds it?
- **Rules-Service R-3 · External witness for system-TCB rules** — The same witness the Watch uses, or a separate one?
- **Rules-Service R-4 · Business-type taxonomy v1 ratification** — Ratify the v1 business-type taxonomy in `Rules_Service_Spec_v1.docx` §7 (10 entries + base fallback) as the standing list?

## §D · New rulings surfaced by amendments (proposed by this ingest, not by canon)

- **Promise-Set-Amendment-8 · Doc 3 scope statement for eradicate/communicate/evidence-custody** — Resolve one of two ways: (a) name eradication, external communication, and evidence custody for proceedings as deliberately out of the Watch's scope with a separate named function identified; OR (b) declare them open gaps because no such function exists?

## §E · Consolidated · one-line-per-ruling · 14 total

Ordered as the owner may find useful (priority per canon note where stated):

**Commercial-admission blockers (per Trojan/Whisper doc §5):**
1. **R-7** — Estate Release Budget size (natural units + ε, δ). Priority: highest per doc.

**Doc 0 foundation blockers (unblock TCB enumeration, arch description, etc.):**
2. **R-1** — TCB membership test (ratify Attribute 1's proposal or set another).
3. **R-3** — Watch TCB membership (in full, or response-half only).
4. **R-5** — Deployment model (shared / dedicated / both).

**Rules Service blockers (unblock system-rule ceremony):**
5. **Rules-Service R-1** — Countdown lengths per tier.
6. **Rules-Service R-2** — Second signatory role for system-ordinary rules.
7. **Rules-Service R-3** — External witness for system-TCB rules (same as Watch, or separate).
8. **Rules-Service R-4** — Ratify business-type taxonomy v1.

**Trojan/Whisper defaults (proposed DEFAULT-class if not final):**
9. **R-8** — Reproduction threshold + sample size + probe design (DAP-31 + A5.15 + DAP-32 battery + thresholds).
10. **R-9** — Per-run DP (ε, δ) + natural-unit multiplier for approved non-DP runs.
11. **R-10** — Recommendation-window duration for A5.16.
12. **R-11** — Coordination-signature threshold for A5.18 class (c).

**Mandatory-baseline governance:**
13. **R-2** — "Lower the standard" resolution (Option A re-home vs Option B rename-as-discretionary).

**Doc 3 scope completeness:**
14. **Doc3-Scope-Ruling (proposed)** — Eradication + external communication + evidence custody: named separate function (name it), or open gaps (accept)?
