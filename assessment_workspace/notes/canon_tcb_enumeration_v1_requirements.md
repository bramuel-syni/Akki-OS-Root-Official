READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_tcb_enumeration_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `TCB_Enumeration_v1.docx` sha256 `3bfbe5b994…` · 16,649 B. Extracted text `canon/drops/20260909/extracted/text/TCB_Enumeration_v1.txt`.
**Spec id.** `tcb_enumeration_v1`. Draft for owner ratification · closes **Doc 0 G-1**.
**Applied test (verbatim, Table 0 R0).** *"A component is in the TCB if and only if it is deterministic and its failure would falsify a guarantee this document or a document it governs makes. Two conditions, both required. Neither alone qualifies."*
**Resolves (verbatim, Table 0 R2).** Doc-0 Ruling R-3 — the Watch's TCB membership — mechanically applied via BA-1.1. Confirmed compatible with BR-9.1 (CIF) and BR-7.4 (Grey Mirror).
**Status (verbatim, Table 0 R3).** *"Draft v1. This list is itself TCB-tier content per BA-1.2 — its own future changes go through the Rules Service's system-TCB ceremony (RBM-8) once ratified."*

---

## §A · Method

- *"'Deterministic' is evaluated at the level of the mechanism actually making a decision, not the subsystem that hosts it. Several entries below split a subsystem in two for exactly this reason: the decision point inside it is deterministic even where the subsystem's broader function is not."*
- *"'Protection-critical' is evaluated by BA-1.1's own clause: would this component's failure falsify a stated guarantee. Each row below names the guarantee."*

## §B · The Enumeration (§2, Table 1 verbatim)

| Component / mechanism | Guarantee at risk | Determ.? | Verdict | Reasoning |
|---|---|:-:|:-:|---|
| SyniSense — chokepoint (custody sequence) | No leakage of confidential info (#1) | Yes | **IN** | Sole invoking function, negative-scan build test |
| SyniSense — closed outbound network | No leakage; no path around crossing | Yes | **IN** | Allowlist + static-analysis gate |
| Solva — assertion-boundary seam (import assertion) | Assertion floor (Doc 4) | Yes | **IN** | Enforcement mechanism deterministic even where constrained content isn't |
| Solva — reasoning / generation itself | — | No | OUT | Learned; the seam decides |
| Northena — objective-freeze mechanism | No silent scope recalibration (#32) | Yes | **IN** | Shared deterministic lock |
| Mtafiti — registry write/query path | Estate composition is what it's recorded to be | Yes | **IN** | Storage + retrieval logic |
| Targeta — yield wall / MOAC acceptance gate | No result accepted without every criterion (#22) | Yes | **IN** | Fixed criteria evaluated mechanically |
| Targeta — the training process itself | — | Partial | OUT | Reproducible under seed but not a decision point |
| Mkondo — hand-off registry | Clean hand-offs, no dropped context (#32) | Yes | **IN (pending build)** | Deterministic by BR-6.1 |
| Watch — Mkono (response) | Nothing misused (#6/#7) | Yes | **IN** | Signed policy against certainty registry (A5.2) |
| Watch — Grey Mirror (Macho detection) | — | No | OUT | Learned pattern-matching per BR-7.4 |
| The Ledger — writer | Every claim traceable to evidence (A8) | Yes | **IN** | Append-only hash-chained single writer |
| CIF — ideation faculty | — | No | OUT | BR-9.1 already on record |
| Critic Seam — RV-tier | Evidence integrity (Doc 19A) | Yes | **IN** | Six mechanical verification checks |
| Critic Seam — QA-tier | — | No | OUT | Detect never decide |
| MOAC — acceptance-criteria evaluation | No result accepted without every criterion (#22) | Yes | **IN** | Same guarantee as Targeta's wall |
| Rules Service — ceremony engine (RBM-7..RBM-13) | No rule in force without ceremony (I-1) | Yes | **IN** | Countdown + countersign verification + atomic apply |
| Rules Service — AI-assisted drafting (RBM-2) | — | No | OUT | Confirmation step is TCB; proposal isn't |
| Whitepaper Wizard — Tier 3 eligibility gate (WPW-11) | No human confers eligibility outside stated conditions | Yes | **IN** | Two-path mechanical check |
| Whitepaper Wizard — prose assembly | — | No | OUT | Not a governance decision |
| Connect Wizard — rights-recording at admission | Downstream checkpoints have trustworthy PIP (BR-14.1) | Yes | **IN** | PIP source of truth |
| Agent-Deploy Wizard | — | Undetermined | **UNDETERMINED** | BR-15.1 open |
| Deck Rendering Engine (DR-R2) | — | Yes | OUT | Deterministic but not protection-critical |
| DAP — estate release budget (DAP-35) | No party/coalition exceeds ruled total (Attr-7) | Yes | **IN** | Accumulator + threshold |
| DAP — artefact egress distance gate (DAP-31) | No artefact carries controlled-unit content past ruled threshold | Yes | **IN** | Fixed seed probe |
| DAP — output-content gate (A5.15) | No permitted output carries controlled content undetected | Yes | **IN** | Deterministic classifier held in TCB |
| DAP — admission-integrity probe canary check (DAP-32, A5.2 half) | No trojaned model touches estate data (T-2) | Yes | **IN** | Canary touch on A5.2's closed registry — unfakeable |
| DAP — admission-integrity probe trigger scan (capability-comparison half) | — | Mixed | **SPLIT** | Backdoor trigger-scanning may be statistical; canary-touch half decides |

## §C · Minimisation — What Was Kept Out and Why (§3)

Four **operationally central** exclusions:
- Solva's actual reasoning — most visible capability, NOT TCB (learned).
- CIF — self-improving core of training story, NOT TCB (BR-9.1).
- Grey Mirror — detection half of security layer, NOT TCB (learned, BR-7.4).
- Deck Rendering Engine — genuinely deterministic, NOT TCB (not protection-critical).

verbatim §3: *"This is the minimisation property working as intended, not a set of gaps. A small TCB is a stronger guarantee than a large one — it is what makes G-2's forthcoming architecture description and G-6's security architecture description tractable to write and to verify."*

## §D · Amendments folded

Per `Serving_Integrity_Amendment_v1 §6` (canon_serving_integrity_amendment_v1_requirements.md §G):
- **NEW IN**: the **serving-integrity gate** — load-time hash verification plus conformance assertion. Deterministic; its failure falsifies S-27.
- **NEW OUT**: the serving engine's bulk (scheduler, cache, placement logic) — deterministic, but its correctness is what the gate verifies; only the verification is TCB.

## §E · Downstream unblocks (Table 2 verbatim)

- **R-3** → RESOLVED. Watch response half (Mkono) is TCB; Grey Mirror's detection half is not.
- **G-2** — architecture description now writable against a named list.
- **G-6** — security architecture description writable (see `canon_security_architecture_description_v1_requirements.md`).
- **G-10** — determinism inventory reuses this classification (see `canon_determinism_inventory_v1_requirements.md`).

## §F · Milestone binding

- **M2** — this enumeration lands in W-DOC0-ATTR1-TCB. TCB test = **BA-1.1** verbatim (`deterministic ∧ protection-critical`). Enumeration is versioned + queryable + change-controlled per BA-1.2/BA-1.3.
- **M1** — TCB row `DAP — estate release budget (DAP-35)` requires Security R-7 to close production-grade (Coupled per RULING_LEDGER); lands with `DEFAULT-PENDING-OVERRIDE` marker.
- **M3** — DAP-32 SPLIT row (trigger-scan capability-comparison half) → flagged for build to confirm technique; if statistical, informs; canary-touch half decides.
- **M4** — Agent-Deploy Wizard UNDETERMINED row awaits BR-15.1 charter.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
