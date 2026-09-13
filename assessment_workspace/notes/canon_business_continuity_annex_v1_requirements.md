READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_business_continuity_annex_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Business_Continuity_Annex_v1.docx` sha256 `cf5b1f34cd…` · 12,805 B. Extracted text `canon/drops/20260909/extracted/text/Business_Continuity_Annex_v1.txt`.
**Spec id.** `business_continuity_v1`. Document 3, Part D · houses S-10, S-11 (moves them from "ruled, no document" to "ruled, homed" per Amendment 2 of `Security_Promise_Set_Amendments`).

---

## §A · Recovery — S-10 (§1)

- **S-10** (verbatim) [Ruled — CA1-N5]: *"The system will restore Ledger continuity within 3,600 seconds, under independent countersign, following any continuity-affecting incident."*
- **RTO**: 3,600 s (one hour). **DEFAULT-class** — revisable on incident evidence.
- **BC-1** (verbatim): *"Restoration MUST be countersigned by someone independent of the primary Ledger writer's own infrastructure — the same logic as the Watch's external witness: the verifier cannot be the thing that might be down. A countersigner whose own access depends on the failed infrastructure does not satisfy this."*
- **BC-2** (verbatim): *"Ledger continuity is itself attested on a standing cadence, independent of any incident — proposed quarterly, DEFAULT-class, revisable on evidence. This is a routine health check, not a response to failure; its purpose is confirming the RTO would hold if tested, before it has to be."*

## §B · Notification — S-11 (§2)

- **S-11** (verbatim) [Ruled — CA1-N2]: *"The system will issue breach notification within 72 hours of a qualifying incident, to the parties and authorities the incident requires."*

## §C · What Remains Open (§3)

- **BC-3** — RPO not ruled anywhere in canon. Verbatim: *"RPO cannot be answered responsibly without first knowing whether a replica Ledger writer exists or is planned — an RPO of zero requires synchronous replication; a non-zero RPO requires stating exactly how much is acceptable to lose, in what unit (time, or number of unwritten entries). Neither is specified in canon. This document does not invent an answer; it names the precondition the answer depends on."*
- **BC-4** — Disaster scenarios beyond single-component failure. Verbatim: *"Given the appliance's own dedicated, per-site deployment model (`trust_domains_v1 §1`), a total site loss scenario has no ruled answer: whether there is an off-site backup, and if so its own RPO/RTO, is unaddressed."*

## §D · Standing (§4 verbatim)

*"This annex is Document 3, Part D. S-10 and S-11 move from 'ruled, no document' to 'ruled, homed' on ratification. BC-3 and BC-4 are not blocking … both should be resolved before the appliance programme scales past a small number of deployed units."*

## §E · Milestone binding

- **M3** — S-10 + S-11 discharge in W-WATCH-STACK Wave-C Part-D-proposed recovery + notification.
- **BC-3 + BC-4** — carried as `DEFAULT-PENDING-OVERRIDE` markers (owner scope question flagged).
- **BC-1** (independent countersigner) discharges the Watch's Amendment-6 upgraded-reference-monitor self-check discipline.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
