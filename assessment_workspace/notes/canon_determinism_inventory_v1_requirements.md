READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_determinism_inventory_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Determinism_Inventory_v1.docx` sha256 `344ebf7466…` · 14,769 B. Extracted text `canon/drops/20260909/extracted/text/Determinism_Inventory_v1.txt`.
**Spec id.** `determinism_inventory_v1`. Draft for owner ratification · closes **Doc 0 G-10**.
**Scope (verbatim, Table 0 R0).** *"Every component on the platform — broader than `tcb_enumeration_v1`, which asks a narrower, conjunctive question (deterministic AND protection-critical). This document asks one question only — deterministic, or learned — of everything, whether or not it's protection-critical."*
**Basis (verbatim, Table 0 R1).** *"Attribute 10's own rule, verified: decision authority is held only by deterministic components; a learned component may detect, score, rank, propose, or draft, never decide."*

---

## §A · Classification (§1)

- *"Deterministic: given the same input and state, the same output, reasoned about exhaustively."*
- *"Learned: statistically characterised, not exhaustively reasoned about, whatever its accuracy."*
- *"A component is one or the other; where a named subsystem contains both, it is split, consistent with `tcb_enumeration_v1`'s treatment of Solva, Targeta, and the Watch."*

## §B · Per-Component Inventory (§3, Table 1 verbatim)

| Component | Class | Structural mechanism denying decision authority (if Learned) |
|---|---|---|
| SyniSense — chokepoint (custody sequence) | Deterministic | — holds decision authority directly |
| Solva — assertion-boundary seam | Deterministic | — holds decision authority over what may be asserted |
| Solva — reasoning / generation | Learned | Seam refuses anything not independently evidenced. Seam decides; Solva proposes. |
| Northena — objective-freeze mechanism | Deterministic | — |
| Mtafiti — registry storage/query | Deterministic | — |
| Mtafiti — AI-assisted classification (if built) | Learned | **DET-2**: name the deterministic confirmation step before it ships |
| Targeta — yield wall / MOAC | Deterministic | — holds acceptance authority directly |
| Targeta — model being trained | Learned | MOAC decides |
| Mkondo — hand-off registry | Deterministic | — |
| Watch — Mkono (response) | Deterministic | — holds containment authority directly |
| Watch — Grey Mirror (detection) | Learned | Mkono acts only on signed verdict Grey Mirror cannot produce authority over |
| Ledger — writer | Deterministic | — |
| CIF — ideation faculty | Learned | BR-9.2 acceptance point deterministic; **DET-1** open |
| Critic Seam — RV-tier | Deterministic | — |
| Critic Seam — QA-tier | Learned | QA-1: findings route to RV-tier or human; cannot block execution |
| Rules Service — ceremony engine | Deterministic | — |
| Rules Service — AI-assisted drafting | Learned | RBM-2: human confirms |
| Whitepaper Wizard — eligibility gate | Deterministic | — |
| Whitepaper Wizard — prose assembly | Learned | WPW-13 draws only on Tier 1/2 artefacts; gate decides |
| DAP — release budget, distance gate, output-content gate | Deterministic | — each holds own admit/refuse authority directly |
| DAP — admission-probe trigger scan (backdoor detection half) | Mixed — flagged | Where technique is statistical, it informs; canary-touch on A5.2's closed registry decides |
| Deck Rendering Engine | Deterministic | Not a governance decision authority; completeness only |

## §C · Human Oversight Against Article 14 (§2, Table 2 verbatim)

| EU AI Act Art-14 capability | State | Evidence |
|---|---|---|
| (a) Understand & monitor | Partially evidenced | STATE/NEXT.md-style tracking + Rules Registry (once built) — built for change-control; happens to serve oversight |
| (b) Aware of automation bias | Directly addressed | **A5.16** (recommendation provenance) — surfaces the recommendation at point of action |
| (c) Correctly interpret output | Evidenced by design, not tested | A8 "Walk this →"; never tested with real reviewer |
| (d) Override, disregard, reverse | Strongly evidenced | Every ruling in canon history is an instance |
| (e) Halt to safe state | Partially evidenced; **one confirmed gap** | Watch stops anything (A5.3); **DET-1** open: CIF halt independent of Targeta run |

## §D · Open findings (§3)

- **DET-1** (verbatim): *"Confirm or build a halt mechanism for CIF independent of halting the Targeta run it feeds — closing capability (e) fully rather than leaving it partially evidenced."*
- **DET-2** (verbatim): *"Where an AI-assisted classification capability is built into Mtafiti, name the deterministic confirmation step before it ships — not after, per this inventory's own method for every other learned component."*

## §E · Standing (§3)

verbatim: *"This inventory itself should be re-run, not assumed permanent, whenever a new component is added to the platform — consistent with `tcb_enumeration_v1`'s own standing clause. The two share a maintenance obligation because they share almost all their evidence."*

## §F · Amendments folded

Per `Serving_Integrity_Amendment_v1` (canon_serving_integrity_amendment_v1_requirements.md):
- Every gate's runner MUST assert **SFP-8-conforming serving path** before treating its own output as a decision (V-2). Non-conforming path = finding, not decision.

## §G · Milestone binding

- **M2** — W-DOC0-ATTR10-DETERMINISM absorbs this inventory verbatim; DET-1 + DET-2 both attach as `DEFAULT-PENDING-OVERRIDE` rows.
- **M4** — Article-14 capability (b) `A5.16 recommendation window` is KEPT in M4 as already-wired ruling constant (Security R-10 24h DEFAULT), per `MILESTONE_PROMISE_BINDING §CONFIRM` correction A2.
- **M3** — Article-14 capability (e) DET-1 CIF-halt closes as an M3 supplementary if the Pruning/Unlearning wave uncovers a CIF-halt requirement; otherwise stays OPEN.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
