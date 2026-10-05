# Requirements-first development — owner-directed operating rule

This file records a project operating rule issued by the owner in the conversation
reconciled in `memory/REQUIREMENTS_RECONCILIATION.md`. It is not a new product
governance engine and does not replace the native Ledger or canon.

## Mandatory before planning or changing this repository
0. Resume protocol, every fork, before any plan or question: read this file; run
   `backend/tests/governance/test_requirements_anchor.py`; read the last 20 lines of
   `memory/BUILD_LEDGER.md` and verify the native ids they cite; continue the work
   package named in the last `next` entry of `memory/BUILD_PLAN_V2_20261005.md`.
   `memory/SYSTEM_DIAGNOSIS_20261005.md` holds the owner-ordered diagnosis (issues,
   root causes, pending decisions D1–D7). Compaction handoff summaries are NOT
   authority: a plan or question derived from one is a defect. Append a ledger line
   after every state change and test run, and before any compaction.
1. Read `memory/PRD.md`, `memory/M_ALPHA_OWNER_ORDERS.md` (including its appended
   corrections), `memory/REQUIREMENTS_RECONCILIATION.md`, and the relevant rows in
   `memory/M_ALPHA_PLAN.md`.
2. Follow the source links to the actual governing clauses and applicable owner
   ratifications. Earlier assistant plans, handoffs, tests and code are evidence,
   not owner authority. A green historical test cannot ratify a changed requirement.
   Consult the ratification source index in `memory/REQUIREMENTS_RECONCILIATION.md`;
   an old blank signature or “pending” heading does not undo a later recorded ruling.
3. Identify requirement → existing owner/service → proposed change → test → pass
   evidence. Inspect the existing implementation before proposing a replacement.
4. Record any conflict, evolved requirement or proposed addition on disk BEFORE
   implementation. Separate `owner-issued`, `canon`, `engineering-mechanism`,
   `proposed-not-ratified`, and `verified-evidence`. Do not present an inference as
   an owner quote. Preserve earlier records; link explicit supersessions.
5. Do not ask the owner to restate settled requirements. Ask only for a genuinely
   unresolved consequential decision, after checking the recorded rulings. Every
   question put to the owner cites the clause search performed or is one of the
   recorded D-rows in the current diagnosis; compaction handoffs are never the
   authority for a question or a plan.
6. Test negative paths as well as useful outcomes. Record limits, failures and
   unmeasured quality. Do not claim functional completion from scaffolds or mocks.

## Load-bearing constraints
- Enhance existing SyniSense/Shield, Solva, CIF and context-preservation services;
  do not rebuild, flatten, bypass or introduce competing authorities.
- The user's confidentiality register governs classified content. Conventional
  identifiers, owner-named content and owner-described privileged meanings are
  distinct protection needs, not three regex modes.
- Original confidential material is read only by estate-controlled contained
  protection models. External task models receive only governed safe context.
  No external model may decide what to remove by receiving the original first.
- Preserve the sole external invocation, request-local mapping custody,
  independent question/data assessment and guarded joint-disclosure seam.
- Do not treat JSON keys as universally public; a key itself can carry a secret.
  Do not substitute a regex tweak for the required reasoning capability.
- Audio: preserve language/content/learned group character, exclude retained
  anatomical biometrics from derived registers. A suggested numerical spectrum
  offset is NOT a ratified algorithm or proof of privacy/utility.
- Preserve running GPU jobs and native capacity/lease controls. Estate-only
  training data; no public corpus intake. Do not infer current activity from old
  timestamps or waive independent admission/quality/privacy gates.
- All five promises and all 31 M Alpha jobs remain in scope. Do not silently move
  unfinished mandatory requirements into an optional backlog to claim completion.

## Continuity
Update the reconciliation and PRD after each verified work package. Keep native
operational truth in existing job/Ledger records. This instruction is a persistent
agent-entry anchor, not proof that all future agents will obey it or that runtime
policy enforcement has been completed.