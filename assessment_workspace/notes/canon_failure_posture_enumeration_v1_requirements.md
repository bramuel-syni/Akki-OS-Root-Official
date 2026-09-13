READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_failure_posture_enumeration_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Failure_Posture_Enumeration_v1.docx` sha256 `589ebb6d0f…` · 13,905 B. Extracted text `canon/drops/20260909/extracted/text/Failure_Posture_Enumeration_v1.txt`.
**Spec id.** `failure_posture_v1`. Draft for owner ratification · closes **Doc 0 G-11**.
**Requirement answered (verbatim, Table 0 R0).** *"CC FPT_FLS.1: preserve a secure state for an enumerated list of failure types — the enumeration is the requirement, not a general commitment. NIST SC-24: fail to a known state, preserving defined state information."*

---

## §A · Platform default (§1 verbatim)

- **FP-1**: *"Every component in the Trusted Computing Base fails closed by default. An evaluation that cannot complete — configuration unset, a dependency unreachable, a check erroring — refuses the operation it governs. This is the default; §3 lists the components that correctly depart from it, and why."*
- **FP-2**: *"A gate whose governing configuration is unset or fails integrity verification at load refuses by default rather than passing by default. This absorbs `security_architecture_v1`'s SEC-4 (MOAC), SEC-6 (the distance gate), and SEC-7 (the admission probe) as one rule rather than three restatements of it — an unconfigured gate is a closed gate, platform-wide, not per-component."*

## §B · Per-component enumeration (§2 · Table 1 verbatim)

| Component | Failure types | Posture | Preserved state |
|---|---|---|---|
| SyniSense — chokepoint | Custody policy unreadable; de-id step errors; re-id key unavailable | **Fail-closed** | Crossing attempt written before attempt — failed crossing still evidenced |
| SyniSense — closed network | Allowlist config unreachable | **Fail-closed** | No outbound attempted; refusal reason |
| Solva — assertion-boundary seam | Anchor map cannot be computed; source material unreachable | **Fail-closed** | Unanchored draft discarded; refusal with structured reason (A5.5) |
| Northena — objective-freeze | Freeze record unreadable at hand-off | **Fail-closed** | Job halts rather than proceeding on unverifiable scope |
| Mtafiti — registry | Write path unavailable | **Fail-closed for writes; fail-safe-open for reads of already-committed data** | Last committed state queryable while writes refused |
| Targeta — yield wall / MOAC | Criteria config unset or unverifiable | **Fail-closed** | Run artefacts intact; nothing marked accepted |
| Mkondo — hand-off registry | Registry write fails mid-handoff | **Fail-closed** | Neither side treats as complete; attempt recorded as failed |
| Watch — Mkono | Verdict unreadable; policy table unreachable | **Fail-closed on new actions; already-active containments persist** | Active containments stay in force |
| Ledger — writer | Storage unreachable; hash-chain verification fails | **Fail-closed** — everything depending on writing fails closed | Chain up to last verified entry; no out-of-order append |
| MOAC | As Targeta's wall — listed once | — | — |
| Critic Seam — RV-tier | Deterministic check cannot execute | **Fail-closed** — escalates to human | Submission awaiting review |
| Rules Service — ceremony engine | Countdown or countersign verification unreachable | **Fail-closed** — no rule reaches CANON on unverifiable ceremony | Rule remains PROPOSED; partial progress preserved |
| DAP — release budget, distance gate, output-content gate | As DAP-28..DAP-30 | **Fail-closed** | Carried by reference |

## §C · Departures — Where Fail-Safe-Open Is Correct (§3 verbatim)

- **FP-3**: *"Mtafiti's read path fails safe-open: a write failure never blocks a query against already-committed estate composition. The alternative — refusing to answer 'what exists' because 'what changed most recently' cannot be confirmed — would make an outage indistinguishable from data loss."*
- **FP-4**: *"The Watch's already-active containments persist through a Watch outage rather than lapsing. This is fail-closed for new decisions and explicitly not fail-open for standing ones."*

## §D · Standing (§4 verbatim)

*"A component added to the Trusted Computing Base under `tcb_enumeration_v1`'s own standing clause is added here in the same turn — posture, failure types, and preserved state, not deferred to a later pass."*

## §E · Amendments folded

Per `Serving_Integrity_Amendment_v1 §6` (canon_serving_integrity_amendment_v1_requirements.md §G):
- **NEW ROW**: *"Serving path, semantic integrity unverifiable (hash mismatch; reference validation stale or failed) → fail-closed: refuse to serve. Preserved state: the artefact untouched, the refusal reason, the failed validation record."*

## §F · Milestone binding

- **M2** — Full enumeration lands in W-DOC0-ATTR11 (Coherence + Failure Posture) alongside Amendment 7 (A5.9 added to Attr-11).
- **M1** — DAP-28..DAP-30 rows already in M1 building list (2F/2H).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
