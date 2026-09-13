READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# S7_CONTEXT_PACKAGE_20260913.md

**Purpose.** Context package for owner ruling on S-7 ("Learn") — per disposition **C2**. Owner needed *"more context"* before ruling: this file provides the verbatim S-7 row, Amendment 1's reclassification language, and what a Doc-3 amendment ceremony would concretely involve (steps · who signs · what changes). Owner rules after.

**Standing.** Read-only, document-only, evidence-backed.

---

## §A · The S-7 row · VERBATIM (Security_Assurance_Promise_Set.xlsx · files_14 · R8)

| Field | Content (verbatim) |
|---|---|
| **# / ID** | **S-7** |
| **Doc** | Doc 3 |
| **Promise text (as originally drafted)** | *"Update the behavioural signature from every contained incident — above the floor, never at it."* — [Amendment 1 REPLACES this text; see §B] |
| **Promise text (as amended)** | *"SPECIFICATION GAP — no mechanism specified. Doc 3's plain-language promise stated the platform 'learns from every attack it defeats,' but every A5 clause touching learning (A5.7, A5.8, A5.12) constrains what may not happen, not what does update, on what evidence, or at what layer."* |
| **Standard column** | CC FAU_SAA (would require a specified mechanism) · ISO 27001 5.27 (learning from information security events, closest analogue) |
| **Impl. status** | **Absent → gap** |
| **Bound / Ruling** | **Unruled — no mechanism exists to bound** |
| **Where it lives / Notes** | Gap between A1 (plain-language promise) and A5 (which only constrains learning, never specifies it) |
| **System features** | *"None specified"* |
| **User requirements** | *"Not yet answerable — no mechanism exists for a user-facing guarantee"* |

## §B · Amendment 1's reclassification language · VERBATIM

Source: `canon/drops/20260907/extracted/text/Security_Promise_Set_Amendments.txt` §Amendment 1.

> **Amendment 1 · S-7 Marked as a Specification Gap, Not a Promise**
> **TARGET.** S-7 ("Learn"), Security Assurance Promise Set
> **CURRENT.** *"Update the behavioural signature from every contained incident — above the floor, never at it."* Stated as a Present promise.
> **AMENDED.** Status changed to **Absent → gap**. Promise text replaced with an explicit statement that no learning mechanism is specified: Doc 3's plain-language promise (A1) states the platform *"learns from every attack it defeats,"* but every A5 clause touching learning — **A5.7, A5.8, A5.12** — constrains what may *not* happen. None specifies what *does* update, on what evidence, or at what layer.
> **PRINCIPLE.** *"A promise cannot be asserted from the absence of a prohibition. Three clauses constrain learning and none specifies it; silence is a gap, not licence to infer a mechanism."*

## §C · The three A5 clauses that constrain (but do not specify) learning

Reference from `canon/unpacked/Akki_Canon_8_The_Watch.docx` A5 section:

- **A5.7 · Non-Conformance Ceiling.** Loss of behavioural conformance alone returns the actor to baseline verification; it is never grounds for conviction on its own. Constrains: *what conformance drift is allowed to mean*. Does not specify: *how detection re-learns from an incident*.
- **A5.8 · No Silent Recalibration (rules layer).** The rules-layer floor is not tuneable by learning — a rule change requires the two-signature countdown ceremony. Constrains: *what learning may not silently touch*. Does not specify: *what learning may touch*.
- **A5.12 · Non-Exportable Behavioural Profile.** Learned parameters live in a tenant-keyed, non-exportable, per-actor profile store — not the raw action history the trust mark leaks. Constrains: *where learned state may live*. Does not specify: *what triggers a write, at what layer, on what evidence*.

**Also cited (Doc 3 §A1 plain-language):** *"The platform learns from every attack it defeats"* — the promise that A5 fails to operationalise.

## §D · The gap in one sentence

`[framing, not canon]` — Doc-3's plain-language promise (A1 "learns") + three prohibitions on learning (A5.7/A5.8/A5.12) constrain the shape of a learning mechanism without ever specifying it. **A specification cannot promise a mechanism its own text does not describe.** Amendment 1 recognises this by demoting S-7 from "Present promise" to "Absent → gap".

## §E · What a Doc-3 amendment ceremony would concretely involve

Per `rule_criteria_spec_v1` (BANKED-DERIVED · ROC-1 ratified 2026-09-09) + Rules-Service R-1 (**RATIFIED 48h/7d** per C3 batch) + Rules-Service R-2 second-signatory (**OPEN — owner input required**) + Amendment 1's *"A promise cannot be asserted from the absence of a prohibition"* principle:

### E.1 · Steps

1. **Draft the mechanism text.** New Doc-3 A5.x clause (proposed slot: **A5.22 · Adaptive Detection Learning Floor**) stating:
   - **What updates** (learning-parameter delta writes to `services/watch/persistence.py` profile store).
   - **On what evidence** (a contained-incident record from the six-signal registry, atomic with the verdict — no ex-post inference).
   - **At what layer** (`grey_mirror` detection-layer only; NEVER the assertion boundary / rules floor / Mkono response layer — these are structurally forbidden per A5.7/A5.8/A5.12).
   - **Boundaries**: cannot tune below the ruled floor (A5.8 preservation); cannot leak into scoring / pricing / management visibility (A5.12 preservation); cannot alone convict (A5.7 preservation).
2. **Draft the failure mode.** New `failure_posture_v1` row: learning-write-failure → fail-closed-toward-not-updating (a stale profile is preferred to a broken profile).
3. **Draft the drill.** New S-8 drill row (learning-loop drill: replay one contained incident under fixed seed, assert the profile update is repeatable + bounded).
4. **Update S-7 status** from **Absent → gap** to **Present** (contingent on the ceremony completing).
5. **Update the Security_Promise_Set_Amendments register** to add an "Amendment 9" resolving the Amendment 1 gap.
6. **Update `MILESTONE_PROMISE_BINDING_20260913.md §M3`** to add S-7 discharge under the new adaptive-detection-learning wave.
7. **Wave open**: **W-DOC3-A5.22-ADAPTIVE-LEARNING** — tests-first, `BASELINE_GUARD=1`, mechanical RED, double-green byte-match, ratchet bump, seal, two-commit local.

### E.2 · Who signs (per Rules-Service ceremony R-1..R-4)

- **Author-of-record**: one named human — per RBM-2 (AI-assisted drafting OUT of TCB; confirmation is TCB). C3-batch already RATIFIED "RS R-3 witness = same witness the Watch already uses". So the author + witness pair is the same C3 pattern as the Watch's own break-in test.
- **Second signatory** (per Amendment 1's own load-bearing rule + Rules-Service R-2): **currently OPEN** — owner must name the second-signatory role BEFORE this ceremony can complete production-grade. If owner ratifies immediately, ceremony proceeds; otherwise wave lands tests-first with `SECOND_SIGNATORY_ROLE = DEFAULT-PENDING-OVERRIDE`.
- **Countdown**: system-TCB tier (this touches the Watch's promise register) → **7-day countdown** per RS R-1 (RATIFIED C3-batch).

### E.3 · What changes on ratification

- Canon-8 gains **A5.22** clause (new Watch structural property).
- Security_Assurance_Promise_Set.xlsx v3 (or higher) gains: S-7 status flipped **Absent → Present**, promise text restored (mechanism-anchored), Standard column updated (CC FAU_SAA specified).
- Security_Promise_Set_Amendments gains **Amendment 9** (S-7 gap closed via A5.22).
- `notes/canon_8_requirements.md` re-extracted for A5.22.
- `services/watch/persistence.py` grows a bounded profile-update mechanism (deterministic, seeded, bounded by ruled deltas).
- `MILESTONE_PROMISE_BINDING_20260913 §COV` removes S-7 from the coverage-gap row.

### E.4 · What does NOT change

- A5.7 / A5.8 / A5.12 unchanged in wording; A5.22 adds the missing positive specification without removing any prohibition.
- Rules floor (A5.8) unchanged — learning still cannot touch the rules layer.
- Behavioural profile (A5.12) unchanged — still tenant-keyed, non-exportable, per-actor.
- Non-conformance ceiling (A5.7) unchanged — learning still never alone convicts.
- The four Amendment-1 principles remain binding: (i) promise cannot be asserted from absence of prohibition; (ii) three clauses constrain, none specifies; (iii) silence is gap not licence; (iv) A5.22 must be specification, not inference.

## §F · Options for owner ruling

**Option 1 · DRAFT & CEREMONY NOW.** Author A5.22 in current form (§E.1). Ceremony proceeds under 7-day countdown once RS-R-2 second-signatory is named. **Cost.** ~14 days end-to-end; requires RS-R-2 ruling.
**Option 2 · DRAFT NOW, CEREMONY DEFERRED.** Author A5.22 for later. Bank as `DEFAULT-PENDING-OVERRIDE`. **Cost.** ~2 days.
**Option 3 · DECLARE PERMANENT SPECIFICATION LIMIT.** Own the gap. S-7 stays *"Absent → gap"* permanently; the platform's *"learns from every attack it defeats"* language in Doc-3 §A1 is amended to remove the learning claim. **Cost.** 1 amendment ceremony; owner-visible admission of scope.
**Option 4 · DEFER RULING.** Carry S-7 as gap indefinitely; do not open the ceremony until an actual attack-response incident forces the question. **Cost.** Zero now; strategic risk that the promise (as written in §A1) remains asserted without mechanism.

## §G · Recommendation `[framing, not canon]`

**Option 2** — draft the A5.22 text now (fast, unblocks nothing else), bank as DEFAULT-PENDING-OVERRIDE, ceremony when RS-R-2 lands. Preserves optionality; costs 2 days; does not compound the gap.

**Owner rules after reading this package.** Awaiting selection of Option 1 / 2 / 3 / 4.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
