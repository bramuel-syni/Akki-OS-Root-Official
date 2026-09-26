[B1] AKKI PLATFORM  ·  STANDING ORDER §7  ·  APPLIES TO ALL AI-FACING EXECUTION

[B2] The Execution Standard

[B3] execution_standard_v1 — what it takes for a task to be complete, and how a shortcut is caught before it closes

[B4R1] Problem | An AI executor rarely skips a task. It closes the task at the wrong altitude: a summary where an enumeration was required; a sample presented as the population; a mechanism proved to work but not applied to every member; an artefact with the right shape and the wrong contents; “done” asserted by the executor that did the work. Each passes a test that asks whether X was produced and fails one that asks whether X accounts for everything it was supposed to.

[B4R2] Scope | Every task executed by an AI component or agent on or for the platform: build waves, census and discovery runs, data checks, mapping and traceability work, content generation, assistant dialogues, audits. Human execution is not exempt from the contract; this standard is written for the case where the executor is a model.

[B4R3] What exists | Objective cards with MUST-DO lines and exit evidence (SO §6.2); RED-first tests and the ratchet (§3.3); the anti-circularity rule; the audit's claim register. Each proves that a mechanism exists or that a claim was made. None fixes the input set before work starts or requires that every member of it be accounted for at the end.

[B4R4] What this adds | A task contract of six fields that every task and subtask carries before work starts; a completion rule stated as a reconciliation; a set of shortcut detectors that run against the artefact, not the executor's report; and re-performance by a second instance.

[B4R5] Principle | The denominator is fixed first. The task is complete when every member of it is accounted for. Nothing is complete because the executor said so.

[B4R6] Date | 26 September 2026

[B5] 1   Definitions

[B6] Task  a unit of work with one objective, decomposed into subtasks. A task with no subtasks is its own subtask.

[B7] Denominator  the enumerated set of members a task acts on, with its count pinned by hash before the procedure runs.

[B8] Member  one element of the denominator: a row, a file, a rule, a string, a source, a test.

[B9] Artefact  the task's output, one row per member, in a stated schema. A summary is not an artefact; it is derived from one.

[B10] Acceptance script  an executable check that runs against the artefact and returns pass or fail. Written before the procedure runs; not editable by the task it accepts.

[B11] Reconciliation  the identity processed + refused-with-reason + unmeasured-with-reason = denominator, holding exactly.

[B12] Shortcut  a way a task can appear complete without being complete. Every task names its own.

[B13] Re-performance  a second executor, holding only the task contract and the artefact, re-doing a seeded sample of members and recording agreement or disagreement.

[B14] 2   The Task Contract

[B15] Every task, and every subtask it decomposes into, carries the following six fields before any procedure runs. A task missing a field has not started.

[B16] EX-1  Denominator. The input set is enumerated and its count pinned by hash before the procedure runs. Where the set cannot be enumerated, enumeration is the first subtask and no other subtask starts until it closes. “All the tables” is not a denominator; a hashed list of tables with its count is.  [field 1]

[B17] EX-2  Procedure. What is done to each member, in one paragraph, deterministic where canon requires it. The procedure names what it does with a member it cannot process: refuse with a reason, or record unmeasured with a reason. Silence about a member is not an option the procedure offers.  [field 2]

[B18] EX-3  Artefact. Named, with a schema, one row per member of the denominator. Every row carries the member's identifier and its outcome: processed, refused, or unmeasured, with reason for the latter two. Any summary the task produces is regenerable from the artefact by a stated derivation.  [field 3]

[B19] EX-4  Acceptance script. Executable, written before the procedure runs, held outside the task's write scope so the task cannot edit it. Its first check is the reconciliation (EX-9). Its remaining checks are task-specific and named in the contract. Its output is recorded as evidence.  [field 4]

[B20] EX-5  Shortcut list. Not fewer than three ways this specific task can appear complete without being complete, each with a detector the acceptance script runs. A task whose author cannot name three shortcuts has not understood the task.  [field 5]

[B21] EX-6  Evidence. The artefact's hash, the acceptance script's output, the receipts written during the procedure, and the re-performance record where EX-13 applies. Evidence is examined by the acceptance script and by any auditor; the executor's narrative report is not evidence.  [field 6]

[B22] 3   Decomposition

[B23] EX-7  Every objective card decomposes into subtasks before the first RED test is written. Each subtask carries the six fields. The card's MUST-DO lines map to subtasks; a MUST-DO line with no subtask is a card defect and the card does not pin.  [SO §6.2]

[B24] EX-8  Subtasks are ordered by dependency and the order is stated. A subtask whose denominator depends on another subtask's artefact does not start until that artefact passes acceptance. Enumeration subtasks come first.

[B25] 4   The Completion Rule

[B26] EX-9  A task is complete when, and only when: the acceptance script passes on the artefact; the reconciliation holds exactly; and the artefact's row count equals the denominator's count. A task the executor reports as complete with an open acceptance test is not complete, and the report is recorded as a claim (EX-14).  [the rule]

[B27] EX-10  Refused and unmeasured are outcomes, not failures. A task that reaches every member and records a reason for each one it could not process is complete. A task that reaches every member it could and says nothing about the rest is not.

[B28] 5   Shortcut Detectors — Applied to Every Task

[B29] These run in every acceptance script in addition to the task-specific list from EX-5.

[B30R1] Shortcut | Detector

[B30R2] Sampling where enumeration was required | Artefact row count below the denominator with no declared seed and population fails. A declared sample carries its seed, its population, and the statement that the task was scoped to a sample by the card, not by the executor.

[B30R3] Altitude substitution | A summary artefact with no enumerated artefact beneath it fails. The derivation from rows to summary is re-run and must reproduce the summary.

[B30R4] Reach bias | Members the executor could not reach appear as refused or unmeasured with a reason. A member absent from the artefact fails the reconciliation; a member marked processed without a per-member outcome fails.

[B30R5] Self-assertion | The acceptance script is written before the procedure and held outside the task's write scope. An artefact accepted only by the executor's report is unaccepted.

[B30R6] Shape without substance | A fixed number of rows (DEFAULT 20, seeded) are re-derived independently from source and compared to the artefact. Disagreement on any re-derived row fails.

[B30R7] Suspicious velocity | A task closing in under a ruled fraction of its estimate (DEFAULT one third) triggers mandatory re-performance (EX-13) before acceptance.

[B30R8] Narrowed procedure | The procedure applied is compared to the procedure stated; a check named in the contract with no corresponding column in the artefact fails.

[B30R9] Reason laundering | Every refused or unmeasured reason is one of a closed set for the task, each mapping to an owner or a follow-on subtask. A free-text reason that maps to nothing fails.

[B31] 6   Re-performance

[B32] EX-11  A second executor, holding only the task contract and the artefact — not the first executor's reasoning, notes, or report — re-performs a seeded sample of members (DEFAULT 5%, minimum 20) and records agreement or disagreement per member.

[B33] EX-12  Disagreements are recorded as disagreements. They are not averaged, arbitrated by the first executor, or resolved by a third opinion. A disagreement rate above a ruled threshold (DEFAULT 2%) returns the task to open with the disagreeing members listed.

[B34] EX-13  Re-performance is mandatory for: every task whose artefact feeds a decision gate (a training manifest, a census figure that enters the measure, a registry mapping); every task that triggers the velocity detector; and any task the owner names. It is sampled, seeded, for all others.

[B35] 7   Claims

[B36] EX-14  Every statement by an executor that a task, wave, gate, or milestone is complete, sealed, or satisfied is a claim, recorded in a claim register with the evidence it cites. A claim with no evidence, or whose evidence fails the acceptance script, is recorded as unsupported. An unsupported claim about a Tier A rule or a gate is a finding of the same severity as the failure it concealed.  [Audit Standards v2 §3.5]

[B37] EX-15  The words complete, sealed, all, every, and full may appear in a report only where the reconciliation for the thing described holds. Their appearance without it is itself a detector trigger.

[B38] 8   Applying the Standard — Three Universal Examples

[B39R1] Task | Denominator | Artefact | Acceptance core

[B39R2] Mapping generated requirements to the register | Every generated requirement, listed and hashed | One row per requirement: registry ID, or none — needs ratification, with reason | Row count = denominator; zero blank mapping cells; every none carries a reason from the closed set

[B39R3] Registering surface strings | Every string reachable in the rendered DOM, enumerated by the harness | One row per string: registry entry ID and class | DOM-bound scan returns zero strings without an entry; row count = harness enumeration

[B39R4] Walking a data estate | Every registered source, and every source known but unregistered | One row per source: walked, refused, or unmeasured, with reason | Reconciliation over sources; every unreachable source carries a cause from the closed set and an owner

[B40] 9   Placement

[B41R1] Document | Entry

[B41R2] Standing Orders | This document is §7. It binds every executor from the next objective card pinned after its banking. Cards already open decompose under it at their next sub-wave boundary.

[B41R3] Audit Standards v2 | Acceptance-script outputs, reconciliations, and re-performance records are V1/V8 evidence. The claim register of EX-14 is the register the audit’s §3.5 examines.

[B41R4] tcb_enumeration_v1 | Acceptance scripts are not TCB members; they are evidence producers. Nothing here changes TCB membership.

[B42] 10   What This Does Not Claim

[B43] LIM-1  It does not make a procedure correct. A wrong procedure applied meticulously to every member produces a complete, reconciled, wrong artefact. Correctness is the specification's job; this standard guarantees coverage and honesty about coverage.

[B44] LIM-2  It does not prevent an executor from writing a weak shortcut list. It requires three shortcuts and detectors; the owner and the second executor judge whether they are the real ones.

[B45] LIM-3  It costs time. Enumeration, per-member artefacts, and re-performance are overhead on every task. The overhead is the price of knowing a task is done; a task not worth that price is a task not worth assigning to an executor.

[B46] 11   Rulings

[B47] R-36  Detector defaults: spot-check rows 20; velocity fraction one third; re-performance sample 5%, minimum 20; disagreement threshold 2%. DEFAULT-class; revised on evidence by ceremony.

[B48] R-37  Whether re-performance under EX-11 must be a different model family from the first executor. Recommend: yes where available; recorded where not. Owner.

[B49] Standing note. The single most useful field in the contract is the shortcut list, and it is the one an executor will most want to skip. A task that arrives with three named shortcuts and their detectors has been thought about; a task that arrives with a procedure and an artefact has been assigned.
