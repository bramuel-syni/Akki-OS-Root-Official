READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_handoff_generalisation_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Handoff_Generalisation_v1.docx` sha256 `d89bbba066…` · 11,977 B. Extracted text `canon/drops/20260909/extracted/text/Handoff_Generalisation_v1.txt`.
**Spec id.** `handoff_registry_v1`. Draft for owner ratification · closes **Doc 0 G-13** (Promise #32 registered-handoff generalisation).

---

## §A · The Registry (§1 verbatim)

- **HR-1**: *"Mkondo owns a hand-off registry. Every job passed from one subsystem to another — not only ThinkLab to Task Manager — writes an entry before the receiving subsystem may act on it."*
- **HR-2**: *"A hand-off entry carries: the commissioning subsystem's identity; the receiving subsystem's identity; the job's frozen objective, from Northena's existing mechanism (BR-3.1); the shape of what is being handed off (a reasoning session, a training commission, an extraction request, a rule proposal — whatever the job class); a timestamp from the platform's reliable time source; and a receipt once the receiving subsystem acknowledges."* — **R-C2 dependency**: reliable time source (Doc-0 G-8).
- **HR-3**: *"A receiving subsystem MUST refuse to act on a hand-off that has no registry entry. This is the generalisation of the one existing guarantee (Promise #32) to every crossing, not only the instantiated one."*
- **HR-4**: *"The no-dual-hatted-task rule (Promise #32) is enforced at registration: a hand-off entry naming a job already open under a different receiving subsystem is refused, not merely discouraged. This moves the rule from convention (as BR-6.3 found it) to a registry-level check."*
- **HR-5**: *"Objective freeze applies at the point of registration, not at the point of eventual action — a receiving subsystem inherits the frozen scope Northena set at hand-off, and cannot itself widen it. This is the same discipline DAP-18 already applies to commissioned jobs, generalised to every internal hand-off, not only DAP's external-facing ones."*
- **HR-6**: *"The registry is queryable by either end of a hand-off, by job, by subsystem pair, or by time range — so 'what did we hand this subsystem, and when' has an answer without reconstructing it from each engine's own logs."*

## §B · Failure Posture (§2 verbatim)

- **HR-7**: *"A hand-off registry write that fails leaves the job un-commissioned on the receiving side — fail-closed, consistent with `failure_posture_v1`'s platform default and its own treatment of Mkondo's registry."*

## §C · What This Does Not Change (§3 verbatim)

*"ThinkLab's hand-off to Task Manager is not re-specified — it already meets HR-1 through HR-6 by construction, having been the pattern this document generalises from. No existing behaviour changes for that one crossing; every other crossing now has to meet the same bar it already does."*

## §D · Standing (§4 verbatim)

*"A new subsystem, or a new job class passed between existing ones, registers its hand-off shape here at the point it is built — not discovered later as a second uninstantiated guarantee the way this one was."*

## §E · Milestone binding

- **M4** — Full HR-1..HR-7 lands in W-JOURNEY-ASSISTANT registered-handoff-contract generalisation. **Fully discharges Promise #32** (Doc-0 STATUS: partial → full).
- **M2** — HR-7 fail-closed posture folds into Failure-Posture enumeration during W-DOC0-ATTR11 close.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
