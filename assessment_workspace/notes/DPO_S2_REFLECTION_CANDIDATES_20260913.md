READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# DPO_S2_REFLECTION_CANDIDATES_20260913.md — proposal (not ratification)

**Standing.** Read-only proposal note. RBM-2 propose-confirm shape: drafting proposes; a NAMED HUMAN confirms. **This note does NOT close the DPO-S2 HALT.** `services/solva_v2/engines/reflection.py::run()` STAYS raising `NotImplementedError` with its HALT tag until owner sign-off lands.

**Standing after this note (verbatim commitment)**:
- Zero track-a code change for Part A.
- Zero ratchet movement for Part A.
- No push (SO §4).

**Purpose.** Draft 3–5 case-agnostic candidate reflection questions grounded first-hand in A5.5 (Doc 4 · Canon-4 §24) and Canon-4 §22 (load-bearing seam), for owner ratification.

---

## §0 · A5.5 first-hand (Canon-4 §24, lines 129–130 verbatim)

Line 129:
> "A conclusion whose computed class falls below the objective's floor is refused with a structured reason, stating what was asked, the supported class, and what would raise it. It is refused visibly, never silently downgraded and served."

Line 130:
> "The refusal is actionable, and it offers exactly the three things a person can actually do about it: accept the result as a recorded statement, narrow the objective, or lower the standard. Offering anything else would be offering something the system cannot actually deliver."

**The A5.5 triad (as owner named it):**
- **(i)** "what was asked" — objective clarity
- **(ii)** "the supported class" — the assertion boundary
- **(iii)** "what would raise it" — the gap

## §1 · The structural job (fixed, not proposed)

Reflection's job is fixed by Canon-4 §21 and the wave's CP-S8 contract shape:
- **INPUT**: tension pairs (from tension_detector.py)
- **OUTPUT**: `LoadBearingSet` (Canon-4 §22 refs-only) — feeds `compute_class(LoadBearingSet) -> AssertionClass`

Every candidate below must surface **load-bearing material** for CP-S2's classifier — nothing else. No question may compute a class, no question may narrow scope, no question may lower a standard (those are the caller's actions on the refusal envelope, not reflection's).

## §2 · Candidate reflection questions (5 candidates)

Each candidate cites its specific canon clause; a candidate that cannot name its anchor was dropped before landing here (per Condition (a)).

### CAND-1 · "What is in scope?" — from A5.5 leg (i)

> **"Of the candidate units in the surfaced tensions, which bear directly on the objective as asked — as opposed to bearing on an adjacent question the answer happens to also address?"**

- **Anchor (first-hand)**: Canon-4 §24 line 129 verbatim "stating what was asked".
- **Cross-anchor**: Canon-4 §22 "Solva chooses the units."
- **Surfaces**: the subset of candidate units whose relation to the objective is direct-bearing rather than tangential.
- **Refuses**: NOT a class computation; NOT a scope narrowing (the caller narrows in the refusal envelope, not reflection).
- **Case-agnostic**: uses only "candidate units", "objective", "adjacent question" — no domain vocabulary.

### CAND-2 · "What class does each unit support, as stamped?" — from A5.5 leg (ii)

> **"For each candidate unit under consideration, what is the highest class its own ledger stamp supports — read as-is, without reasoning-strength adjustment — utterance, fact, or non-factual?"**

- **Anchor (first-hand)**: Canon-4 §24 line 129 verbatim "the supported class".
- **Cross-anchor**: Canon-4 §23 "the weakest load-bearing unit sets the ceiling for the whole"; Canon-4 §23.1 "the signature is the guard" — reflection reads unit class stamps, it does NOT recompute them.
- **Surfaces**: the per-unit class information the boundary needs from the LoadBearingSet.
- **Refuses**: NOT a reweighting; NOT a strength-adjusted class. Reads ledger stamps as-is.
- **Case-agnostic**: names only the three AssertionClass values (already canon).

### CAND-3 · "What would raise the class?" — from A5.5 leg (iii)

> **"For any candidate unit whose class would keep the conclusion below the objective's floor, what specifically-missing evidence would let a stronger unit take its place?"**

- **Anchor (first-hand)**: Canon-4 §24 line 129 verbatim "what would raise it".
- **Cross-anchor**: Canon-4 §11 "reach objective-satisfying, floor-meeting intelligence"; Canon-4 §4.1 "unmeasured is a first-class value" — surfaces gaps, does NOT fabricate them.
- **Surfaces**: the "gap" leg of A5.5 as structured, not as a hand-wave. Produces filed-gap candidates (Canon-6 §11 mining loop).
- **Refuses**: NOT a fabrication of evidence; NOT a promise the gap can be closed. Just names what would.
- **Case-agnostic**: only "candidate unit", "conclusion", "objective's floor", "stronger unit".

### CAND-4 · "Which units are load-bearing vs corroborative?" — from Canon-4 §22

> **"Among the surfaced tensions, which candidate unit — if included in the load-bearing set — would change the class of the conclusion, and which would only add corroboration without changing class?"**

- **Anchor (first-hand)**: Canon-4 §22 "A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."
- **Cross-anchor**: Canon-4 §26 "the reasoning path across its stages"; the CP-S3 invariant that load-bearing return is refs-only.
- **Surfaces**: the definitional heart of "load-bearing" — units that change class if included, distinguished from units that merely add weight. This is the very function reflection performs.
- **Refuses**: NOT a class output — the classification of "load-bearing vs corroborative" is a structural property of the tension pair against the conclusion, not a class of the conclusion itself.
- **Case-agnostic**: only "candidate unit", "class", "corroboration".

### CAND-5 · "Is any downgrade visible?" — from A5.5 "never silently downgraded and served"

> **"If the load-bearing set as chosen would force a class-downgrade of the conclusion, is the downgrade visible in the reasoning path — such that the caller sees which specific unit's class-floor is what limited the class?"**

- **Anchor (first-hand)**: Canon-4 §24 line 129 verbatim "never silently downgraded and served".
- **Cross-anchor**: Canon-4 §23 "the weakest load-bearing unit sets the ceiling for the whole"; Canon-4 §26 "auditability that justifies letting a component reason at all".
- **Surfaces**: the downgrade-witness — every class-limiting unit is nameable in the trace, so the refusal envelope can point to it under A5.5 leg (ii).
- **Refuses**: NOT a silent fold; NOT an aggregate hand-wave. Every downgrade names its limiting unit.
- **Case-agnostic**: only "load-bearing set", "class-downgrade", "reasoning path".

## §3 · What the questions DO NOT do (invariants for the case-agnostic contract)

- **Do not offer any of the three refusal-envelope actions** — those are the caller's under Canon-4 §24 line 130, not reflection's.
- **Do not compute an AssertionClass** — that is compute_class()'s parameterless job (Canon-4 §23.1); reflection returns UnitRefs only (Canon-4 §22 · CP-S3 invariant).
- **Do not fabricate evidence for the gap** — Canon-4 §4.1 "Unmeasured is a first-class value; a dimension not measured is recorded as unmeasured, never as zero, absent, or clean."
- **Do not carry executive-domain vocabulary** — CP-S8 negative-scan continues to enforce (`diagnosis`, `LOCKED_QUESTIONS`, sector-tag triangulation, etc. absent).

## §4 · Proposed structural output (case-agnostic ReflectionRubric)

`[framing, not canon]` — proposed shape for the case-agnostic reflection contract when owner ratifies. Not committed here; recorded so ratification can be a yes/no on a concrete artefact:

```python
# Proposed contract shape — DO NOT LAND without owner ratification.
class ReflectionRubric(BaseModel):
    """RBM-2 candidate — awaiting NAMED HUMAN sign-off (DPO-S2)."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    # One entry per A5.5-leg or Canon-4 §22 anchor.  Ratification is
    # per-question, so owner can accept a subset.
    ratified_questions: Tuple[Literal[
        "in_scope",          # CAND-1
        "supported_class",   # CAND-2
        "raise_the_class",   # CAND-3
        "load_bearing_vs_corroborative",  # CAND-4
        "downgrade_visibility",           # CAND-5
    ], ...]
```

## §5 · What this note does NOT do

- Does NOT close the DPO-S2 HALT — `engines/reflection.py::run()` still raises `NotImplementedError` with the HALT tag.
- Does NOT modify any track-a code — this is a state-branch note only.
- Does NOT commit anything to the ratchet or move `passed_floor`.
- Does NOT presume owner's ratification: if owner selects zero of the five candidates, the HALT persists and this note is a discarded draft (banked for audit trail per Doc-0 BR-8.1 "a refusal is as much a record as a success").

## §6 · Owner action requested

Owner may:
1. **Ratify one, some, or all** of CAND-1..CAND-5 → an owner-signed ruling names which candidates are accepted. On ratification the HALT closes in a follow-up wave that lands the ReflectionRubric contract + updated `engines/reflection.py::run()` + invariant tests.
2. **Reject all five** with named reason → HALT persists; next drafting round proposes different candidates.
3. **Request additional derivation seeds** beyond A5.5 (e.g., F&P Registry rows for reflection functions per Canon-7 §37) → drafting round two.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
