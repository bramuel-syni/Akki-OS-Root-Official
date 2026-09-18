READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SER v1.1 · Part 6 Absorption Drafts · with canon anchors · DRAFT · notes-only

**Status:** DRAFT · notes-only · nothing applied · gates W-DAP-STACK 2D close and any containment build · does NOT gate M11/M12 per R-18 Part 8.
**Authority:** Item 4 of owner 2026-09-18T~11:35Z 4-hour autonomous window directive:
> "4. SER v1.1 deltas for the Part 6 absorption list, as drafts with canon anchors — notes-only, nothing applied."

**Part 6 absorption list source:** `notes/SER_ERRATA_v1_0_1_20260918.md §H` (banked verbatim below · §1).
**Cross-refs:** Errata v1.0.1 (`notes/SER_ERRATA_v1_0_1_20260918.md`) · 491-row registry (`custody/owner_drops/Master_Requirements_Registry_20260918.xlsx`) · memory_compaction_v1 SER delta (`notes/canon_extraction/memory_compaction_v1_SER_C13_delta_draft.md`).

---

## §1 · Part 6 absorption list (VERBATIM from errata §H)

Errata §H banked list, unedited:
> - **Discipline & privacy plane:** DAP-31, DAP-35, DAP-36, DAP-37, DAP-38.
> - **A20.15 and SFP-8** — safety-function-policy bindings.
> - **A5.19–A5.22, RBM-23, A20.16, AC-13–AC-18** — Watch/verdict/severance surface.
> - **A5.16 and A5.17** — signal registry.
> - **DAP restored to six crossings** with DAP-14 per-request approval and DAP-15 expiry-on-silence.
> - **Release budget as a TCB member.**

**Ordering in this document:** groups (a)-(f) below follow the errata list. Every draft is bounded to a proposed SER section anchor with the exact new/rewritten text; nothing is applied.

---

## §2 · (a) Discipline & Privacy Plane · DAP-31, DAP-35, DAP-36, DAP-37, DAP-38

### §2.1 · Registry-row anchors (from 491-row registry)

| Rule ID | Doc | Statement (shape-only excerpt) | Domain |
|---|---|---|---|
| DAP-31 | DAP Backend spec | "A metered event that cannot be written to the Ledger refuses the operation it meters" (composition ref) | DAP composition (Doc 0 · Component 17) |
| DAP-35 | Pruning & Unlearning Amendment | Structural pruning of fine-tuned artefacts | O13 Data & Intelligence Acquisition |
| DAP-36 | Pruning & Unlearning Amendment | Pruning receipt discipline | O13 |
| DAP-37 | Pruning & Unlearning Amendment | "A fine-tuned artefact MAY be pruned — magnitude pruning or an equivalent structural…" | O13 |
| DAP-38 | Pruning & Unlearning Amendment | "When a unit's rights status changes to withdrawn — consent revoked, licence expired…" | O13 |

### §2.2 · Proposed SER v1.1 landing

**New section: `SER §C.19.7 · Pruning & Unlearning Amendment · absorption from DAP-31..DAP-38`**

```yaml
# ─── SER §C.19.7 (new · additive) ────────────────────────────────────
- section: "C.19.7"
  title: "Pruning & Unlearning Amendment · absorbs DAP-31, DAP-35..DAP-38"
  content_summary: "Fine-tuned artefacts admit structural pruning (magnitude or equivalent); pruning writes a receipt; withdrawn-unit status triggers erasure through DAP-38's mechanism (re-derive without unit OR recall)."
  invariants:
    - "SER §C.19.7-I-1 (DAP-31): metered event that cannot be written to Ledger REFUSES the metered op. [ledger-first · fail-closed · MEM-6 pattern]"
    - "SER §C.19.7-I-2 (DAP-35): pruning of a fine-tuned artefact is a NEW artefact hash + lineage; source artefact retained within lifetime. [MEM-5 pattern]"
    - "SER §C.19.7-I-3 (DAP-36): every pruning writes a receipt naming (source_hash, target_hash, method, ratio, receipt_ref). [MEM-6 pattern]"
    - "SER §C.19.7-I-4 (DAP-37): the pruning MAY be magnitude pruning OR an equivalent structural method. Method is versioned + ratified."
    - "SER §C.19.7-I-5 (DAP-38): withdrawn-unit status triggers erasure query across compacted memory + fine-tuned artefacts (memory_compaction_v1 MEM-9 companion)."
  canon_ref:
    - "DAP-31 (Doc: DAP Backend spec)"
    - "DAP-35 (Doc: Pruning & Unlearning Amendment)"
    - "DAP-36 (Doc: Pruning & Unlearning Amendment)"
    - "DAP-37 (Doc: Pruning & Unlearning Amendment)"
    - "DAP-38 (Doc: Pruning & Unlearning Amendment)"
  gates: "W-DAP-STACK-2D close"
  interaction_with_memory_compaction_v1: "DAP-38 is the mechanism MEM-9 invokes for erasure; the two land as sibling absorption CPs, DAP-38 first."
```

---

## §3 · (b) A20.15 · SFP-8 · Safety-Function-Policy Bindings

### §3.1 · Registry-row anchors

| Rule ID | Doc | Statement (shape-only excerpt) | Domain |
|---|---|---|---|
| A20.15 | serving_integrity_v1 | Safety-function-policy binding · declaration/attestation | O16 Serving Integrity |
| SFP-8 | serving_integrity_v1 | "safety-function-policy floor · a contained agent's model MUST be served on an SFP-8-conforming path" | O16 Serving Integrity |

### §3.2 · Proposed SER v1.1 landing

**New section: `SER §C.11.7 · Serving-Integrity Floor · absorbs A20.15 + SFP-8`**

```yaml
# ─── SER §C.11.7 (new · additive) ────────────────────────────────────
- section: "C.11.7"
  title: "Serving-Integrity Floor · absorbs A20.15, SFP-8"
  content_summary: "Every model surface serving a contained agent (post-Watch W3 or W4) MUST route through an SFP-8-conforming serving path — model behaviour under containment is invariant to the containment."
  invariants:
    - "SER §C.11.7-I-1 (SFP-8): contained agent's model MUST serve on SFP-8-conforming path. [AC-14 anchor]"
    - "SER §C.11.7-I-2 (A20.15): safety-function-policy binding is declared at admission + attested at every serving surface. Attestation is a signed row on the same ledger as Watch verdicts."
    - "SER §C.11.7-I-3: 'contain' surface (AC-13) may implement as session freeze; the freeze is not a delete (no data-loss; §C.3.5 sever ≠ delete)."
  canon_ref:
    - "A20.15 (Doc: serving_integrity_v1)"
    - "SFP-8 (Doc: serving_integrity_v1)"
    - "AC-13 (Doc: serving_integrity_v1) [companion · contain-as-session-freeze]"
    - "AC-14 (Doc: serving_integrity_v1) [companion · SFP-8-conforming path]"
  gates: "W-DAP-STACK-2D close, all containment builds"
  interaction_with_M12b: "Watch W3/W4 sever+contain signals land at M12b-W1 (Ed25519 signing primitive); serving-integrity floor consumes those signals at the next serving-path wave."
```

---

## §4 · (c) A5.19–A5.22 · RBM-23 · A20.16 · AC-13–AC-18 · Watch/Verdict/Severance Surface

### §4.1 · Registry-row anchors (from 491-row registry)

| Rule ID | Doc | Statement (shape-only excerpt) |
|---|---|---|
| A5.19 | watch_learning_v1 | "Every verdict Grey Mirror passes to Mkono MUST carry a certificate: the set of observation refs anchoring the verdict." |
| A5.20 | watch_learning_v1 | "A certificate requirement is a deterministic gate: the named set of data points MUST match." |
| A5.21 | watch_learning_v1 | "The mirage is the certificate ground: a controlled environment in which a behaviour…" |
| A5.22 | watch_learning_v1 | "Every unsure case — a verdict with no applicable requirement, or an action routed…" |
| RBM-23 | watch_learning_v1 | Rule-Book of Modes · Watch mode admission ceremony |
| A20.16 | watch_learning_v1 | Attestation for Watch action class |
| AC-13 | serving_integrity_v1 | "'Contain' for a running agent session MAY be implemented as session freeze" |
| AC-14 | serving_integrity_v1 | "A contained agent's model MUST be served on an SFP-8-conforming path" |
| AC-15 | watch_learning_v1 | "Before an agent receives any scope beyond admission, it runs the certificate ground…" |
| AC-16 | watch_learning_v1 | "The containment environment feeds AC-4 and AC-6 unsure cases to the research queue" |
| AC-17 | watch_learning_v1 | "Every action or output an agent produces MUST cite the admitted capability class" |
| AC-18 | watch_learning_v1 | "A model or agent MAY propose admission of a capability class for itself. It MUST…" |

### §4.2 · Proposed SER v1.1 landing

**New section: `SER §C.7.4 · Watch Learning · absorbs A5.19–A5.22, RBM-23, A20.16, AC-13–AC-18`**

```yaml
# ─── SER §C.7.4 (new · additive) ─────────────────────────────────────
- section: "C.7.4"
  title: "Watch Learning · absorbs A5.19–A5.22, RBM-23, A20.16, AC-13–AC-18"
  content_summary: "Watch verdicts carry certificates; certificate grounds are mirages; unsure cases feed the research queue; new capability classes admit through ceremony. Every scope grant is preceded by certificate-ground evaluation; every action cites its admitted class; agents MAY propose admission for themselves."
  invariants:
    - "SER §C.7.4-I-1 (A5.19): every verdict Grey Mirror passes to Mkono carries a certificate {requirement_id, data_points[], observation_refs[]}."
    - "SER §C.7.4-I-2 (A5.20): certificate requirement is a deterministic gate — named data points MUST match."
    - "SER §C.7.4-I-3 (A5.21): the mirage is the certificate ground — controlled environment."
    - "SER §C.7.4-I-4 (A5.22): unsure case (no applicable requirement, or unadmitted action route) → research queue, NEVER a scope grant."
    - "SER §C.7.4-I-5 (RBM-23): Rule-Book of Modes gains a Watch-admission-ceremony class."
    - "SER §C.7.4-I-6 (A20.16): every Watch action class carries an attestation."
    - "SER §C.7.4-I-7 (AC-13): 'contain' MAY implement as session freeze; freeze ≠ delete."
    - "SER §C.7.4-I-8 (AC-14): contained agent served on SFP-8-conforming path (companion to §C.11.7-I-1)."
    - "SER §C.7.4-I-9 (AC-15): agent runs certificate ground BEFORE any scope beyond admission."
    - "SER §C.7.4-I-10 (AC-16): containment environment feeds unsure cases to research queue (companion to A5.22)."
    - "SER §C.7.4-I-11 (AC-17): every action/output cites admitted capability class."
    - "SER §C.7.4-I-12 (AC-18): agent MAY propose admission of a capability class for itself; MUST run the ceremony."
  canon_ref: [A5.19, A5.20, A5.21, A5.22, RBM-23, A20.16, AC-13, AC-14, AC-15, AC-16, AC-17, AC-18]
  gates: "M12b-W1 (Ed25519 Watch-key primitive) + containment builds"
  interaction_with_R18: "T-c Option (ii) Watch schema landing at CP-M11-GATE-RELEASE ships the vocabulary skeleton (annotate·shape·contain·sever); this absorption fills in the CONTENT (certificate + mirage + unsure-case + ceremony) on top of that skeleton."
```

---

## §5 · (d) A5.16 · A5.17 · Signal Registry

### §5.1 · Registry-row anchors (from 491-row registry)

Positional A5.16 and A5.17 — check registry for document coverage. These are A5.<n> positional-series IDs; each may resolve across multiple documents.

**Shape-only look-up result (from index):** A5.16 and A5.17 are in the positional set. Full document coverage list to be resolved at absorption-CP-open time via `custody/owner_drops/Master_Requirements_Registry_20260918.xlsx` grep against the two IDs.

### §5.2 · Proposed SER v1.1 landing

**New section: `SER §C.7.5 · Watch Signal Registry · absorbs A5.16, A5.17`**

```yaml
# ─── SER §C.7.5 (new · additive) ─────────────────────────────────────
- section: "C.7.5"
  title: "Watch Signal Registry · absorbs A5.16, A5.17"
  content_summary: "Watch severance signals live in a closed, versioned registry. Every 'sever' verdict names a signal_ref that resolves against the registry; unknown signals refuse."
  invariants:
    - "SER §C.7.5-I-1 (A5.16 verbatim binding · document-qualified): [PENDING · resolve against 491-row registry at absorption CP open]"
    - "SER §C.7.5-I-2 (A5.17 verbatim binding · document-qualified): [PENDING · resolve against 491-row registry at absorption CP open]"
    - "SER §C.7.5-I-3: Watch verdict schema (`contracts/watch_verdict.schema.json` landed at CP-M11-GATE-RELEASE) ALREADY carries `severance_signal_ref` bound to A5.2 signal registry; this absorption formalises the registry contents (A5.16/A5.17 rows) + resolution semantics."
  canon_ref: [A5.16, A5.17, A5.2]
  gates: "M12b-W1 (Ed25519 Watch-key primitive)"
```

**Landing-CP note:** Absorption-CP-opening agent must first grep 491-row registry for the exact `A5.16` and `A5.17` rows + their `Doc` values, and produce the document-qualified `canon_ref = "Doc N · A5.<n>"` per owner ruling 2026-09-18 positional-series rule.

---

## §6 · (e) DAP Restored to Six Crossings · DAP-14 Per-Request Approval · DAP-15 Expiry-on-Silence

### §6.1 · Registry-row anchors (from 491-row registry)

| Rule ID | Doc | Statement (shape-only excerpt) |
|---|---|---|
| DAP-14 | DAP Backend spec | "Controlled request routes to named approving authority before execution; does not…" |
| DAP-15 | DAP Backend spec | "Approval decisions recorded with authority, decision, reason; no execution on silence…" |

### §6.2 · Proposed SER v1.1 landing

**Rewritten section: `SER §C.6.2 · DAP Crossings · absorbs DAP-14, DAP-15 (DAP crossings restored to six)`**

```yaml
# ─── SER §C.6.2 (rewrite · additive to prior four-crossing shape) ────
- section: "C.6.2"
  title: "DAP Crossings · six crossings restored"
  content_summary: "The DAP taxonomy is restored to six crossings (from the prior four). The two restored crossings are DAP-14 (per-request approval) and DAP-15 (expiry-on-silence)."
  crossings:
    - "1. request-to-planning"
    - "2. planning-to-execution"
    - "3. execution-to-output"
    - "4. output-to-approval-return"
    - "5. NEW · DAP-14 · per-request approval route · controlled requests route to named approving authority BEFORE execution"
    - "6. NEW · DAP-15 · expiry-on-silence · approval decisions recorded with authority + decision + reason; NO execution on silence"
  invariants:
    - "SER §C.6.2-I-1 (DAP-14 verbatim): 'Controlled request routes to named approving authority before execution; does not execute in silence.'"
    - "SER §C.6.2-I-2 (DAP-15 verbatim): 'Approval decisions recorded with authority, decision, reason; no execution on silence.'"
    - "SER §C.6.2-I-3: expiry-on-silence has a countdown class per R-18 Part 5 (48h ordinary / 7d Watch-and-slow · default class values ratified at CP-M11-GATE-RELEASE)."
  canon_ref: [DAP-14, DAP-15]
  gates: "W-DAP-STACK-2D close"
```

---

## §7 · (f) Release Budget as TCB Member

### §7.1 · Registry-row anchors

No single Rule ID in the 491-row registry names "release budget" as a TCB row (per shape-only grep). This absorption item is a **cross-schema new member** — it declares that release-budget policy joins the TCB via the `tcb_enumeration_v1` method (SER §G.3 pattern in errata v1.0.1).

### §7.2 · Proposed SER v1.1 landing

**Addition to `SER §A.4 · TCB Enumeration (via tcb_enumeration_v1)`:**

```yaml
# ─── SER §A.4 · new TCB row (via tcb_enumeration_v1 method) ──────────
- package: services.release_budget
  entry: "Release budget policy engine · determines admissibility of releases against tenant + estate + timeline budget"
  in_tcb:
    - services.release_budget.policy_engine     # deterministic · rule-set + registry lookup
    - services.release_budget.receipt_writer    # deterministic · ledger row emission on budget decision
  out_of_tcb:
    - services.release_budget.forecast_component  # learned (optional · runs advisory forecast · decides nothing)
  rationale: "Release-budget policy is a Fixed-decision surface (Canon 3 §29 deterministic-accountability standard). Landing as TCB member ensures its rule-set version is signed and its decisions carry ledger rows on same terms as Northena Admit checks."
  canon_ref: [Canon 3 §29, BR-22 (countdown class), errata v1.0.1 §G.3 (tcb_enumeration_v1 method), Part 6 item (f)]
  review_policy: two_reviewers_plus_security_group   # inherited from TCB.yaml root
  build_status: pending_absorption_cp_open
```

**Constraint:** As with memory_compaction_v1 SER delta §5.1 (retention rule engine + reload verifier), this TCB addition enters ONLY through `tcb_enumeration_v1`'s method — rule-set-versioning present, reviewer policy inherited, canon_ref anchored, build_status flagged.

---

## §8 · Cross-item interactions (surfaced for absorption-CP sequencing)

### §8.1 · Interactions with memory_compaction_v1

- **DAP-37** (§C.19.7-I-2 pruning as new hash + lineage) is the M-precedent for **MEM-5** (§C.13.5-I-5 compacted artefact as new hash + lineage). Land DAP-37 absorption FIRST; MEM-5 absorption inherits the shape.
- **DAP-38** (§C.19.7-I-5 erasure via re-derive/recall) is the mechanism **MEM-9** (§C.13.5-I-9 erasure reaches compacted memory) invokes. Land DAP-38 absorption FIRST; MEM-9 absorption invokes it.
- **AC-13/AC-14/SFP-8** (§C.7.4-I-7/-I-8 + §C.11.7-I-1) are the containment-serving floor MEM-10 (user-memory reads under containment) implicitly relies on. Land AC-13/AC-14 + SFP-8 absorption BEFORE MEM-10 absorption.

### §8.2 · Interactions with R-18 landings

- **A5.19–A5.22** (§C.7.4-I-1..I-4 certificate + mirage + unsure-case) FILL IN the vocabulary skeleton landed at CP-M11-GATE-RELEASE (`contracts/watch_verdict.schema.json`). The schema's `certificate.requirement_id / data_points[] / observation_refs[]` structure is exactly what A5.19..A5.20 assert; absorption CP writes the SEMANTICS around the ALREADY-LANDED schema.
- **AC-17** (§C.7.4-I-11 every action cites admitted capability class) is the M9-refuser-AT-M12-CHOKEPOINT contract — M12 wires refusers as unroutable runtime chokepoints (per anchor plan §5); AC-17 provides the invariant those chokepoints enforce.

### §8.3 · Interactions with each other

- **§C.7.4 (Watch Learning) + §C.11.7 (Serving-Integrity Floor)** share AC-13/AC-14 anchors — absorb as SIBLINGS (either order), with a cross-ref between them.
- **§C.7.4 + §C.7.5 (Signal Registry)** share A5.19/A5.2 anchors — absorb §C.7.5 AFTER §C.7.4 (registry contents build on verdict schema).
- **§C.6.2 (DAP six crossings) + §C.19.7 (Pruning & Unlearning)** — independent; either order.

---

## §9 · Wave-open readiness of each absorption CP (proposed)

| Absorption CP | New/Rewritten SER section | Registry anchors | Interactions | Wave-open blocker (if any) |
|---|---|---|---|---|
| CP-SER-v11-A · Pruning & Unlearning | §C.19.7 (new) | DAP-31, DAP-35..38 | Prereq for memory_compaction_v1 MEM-5/9 absorption | None; W-DAP-STACK-2D gate open |
| CP-SER-v11-B · Serving-Integrity Floor | §C.11.7 (new) | A20.15, SFP-8, AC-13, AC-14 | Prereq for memory_compaction_v1 MEM-10 absorption | None; W-DAP-STACK-2D gate open |
| CP-SER-v11-C · Watch Learning | §C.7.4 (new) | A5.19..22, RBM-23, A20.16, AC-13..18 | Depends on M12b-W1 Ed25519 signing primitive | M12b-W1 signing primitive land |
| CP-SER-v11-D · Signal Registry | §C.7.5 (new) | A5.16, A5.17, A5.2 | Depends on CP-SER-v11-C | CP-SER-v11-C land |
| CP-SER-v11-E · DAP Six Crossings | §C.6.2 (rewrite) | DAP-14, DAP-15 | Independent | W-DAP-STACK-2D gate open |
| CP-SER-v11-F · Release Budget TCB | §A.4 (new row) | Canon 3 §29, BR-22 | Depends on `tcb_enumeration_v1` method (existing) | None |

**Proposed order** (per §8 interactions):
1. CP-SER-v11-A (Pruning & Unlearning · establishes DAP-37/38 patterns)
2. CP-SER-v11-E (DAP six crossings · independent · fills DAP-14/15 semantic)
3. CP-SER-v11-B (Serving-Integrity Floor · depends on no prereqs)
4. CP-SER-v11-F (Release Budget TCB · independent)
5. (M12b-W1 lands · Ed25519 signing primitive)
6. CP-SER-v11-C (Watch Learning · absorbs A5.19..22 + AC-13..18)
7. CP-SER-v11-D (Signal Registry · after CP-SER-v11-C)

**Sequencing is proposed, not applied.** Owner ratification required before any absorption CP opens.

---

## §10 · What this document is deliberately not

- **Not an application.** No SER text is rewritten in-tree. This is DRAFT for the absorption CP-open agent.
- **Not a schedule commitment.** Absorption CPs open on owner ratification + gate-release; the order in §9 is proposed.
- **Not a substitute for the errata v1.0.1.** Errata v1.0.1 (banked 2026-09-18) is the current authoritative correction layer for §§A-H; this Part-6 draft is for §§C.7.4/§C.7.5/§C.11.7/§C.19.7/§C.6.2/§A.4 which the errata explicitly banked as DEFERRED.
- **Not a monolithic SER.** No `SER.md` monolith is authored; this file sits alongside the errata and the memory_compaction_v1 SER delta as absorption drafts to a not-yet-monolithic SER.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
