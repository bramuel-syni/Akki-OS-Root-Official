# Functionality plan and progress — decision checkpoint

Basis: last verified checkpoint, 2026-09-25. This is a planning/progress report, not a new live host verification.

Owner request: "Before i decide, surface for me the plan for the do does to achieve functionality and the % progress being made".

**Historical decision checkpoint below; continuation approved.** Owner subsequently reaffirmed the unchanged plan and said "You can pick it up". Current recovery evidence: `EXECUTION_RECOVERY.md`. Current safeguard R01–R08 is verified; real T14 remains blocked by admitted/current private-key mismatch. No host change or estate operation performed. Four non-secret receipt-pin settings were added; no credential material changed.

## Percentages that are supported

| Measure | Numerator / denominator | Percentage | What it does NOT mean |
|---|---|---|---|
| Census-slice acceptance checklist | T01–T13 passed at their stated verification levels; T14 blocked:13/14 |92.9%|Not 92.9% functional OS/DAP or 92.9% live census readiness. Several checks use isolated MOCKED executors, and T07 verifies the boundary without a successful live read.|
| Corrective census UI fidelity checklist | F01–F08:8/8 |100% of this engineering checklist|Not every prototype module functional; owner visual acceptance still pending.|
| Fresh end-to-end census activation gate | T14:0/1 |0% of this gate|Does not erase historical real GPU work or existing backend functionality. Last recorded attempt was blocked; current host access has not been re-probed.|
| Full OS/DAP functional completion |Complete agreed journey ledger not yet established|NOT YET MEASURED|No defensible whole-platform percentage. Do not derive it from tests/files/pages/routes or assign arbitrary partial credit.|

Supporting results:58 backend/source/API tests passed twice;4 rendering tests;42 route-width checks. These denominators overlap different checks and MUST NOT be combined into a platform completion percentage. Read VERIFICATION_REPORT.md for per-case limits.

The missing whole-platform denominator is unfinished audit work. The plan must close it rather than substitute the narrow census checklist score.

Continuation progress: 888 original-markup event sites inventoried with unique IDs/source hashes and conditional/list context (817 OS,71 DAP). This is an audit input, not 888 required journeys or completed mappings. Component/Canon/engine/writer/test reconciliation remains open. Current census suite:82 passed twice after opt-in refusal-drill correction, including MOCKED transport tests. Real refusal run cr-809561ad5643 is banked; live successful output remains 0/1. Safeguard acceptance R01–R08=8/8 does not raise whole-platform or Mtafiti completion.

## Ordered functionality work packages

|Order|Work package|Current evidenced state|Required next work|Functional exit|
|---|---|---|---|---|
|1|Baseline the remaining functionality|Audit and prototype mapping partial|Map every required prototype action/Canon obligation to consumer, engine, writer, executor, receipt and acceptance case; reconcile current rulings; preserve unreviewed status rather than labelling absent.|A fixed, reviewable journey ledger and defensible global progress denominator.|
|2|Akki-owned execution access|Real historical execution exists; last new census attempt refused configured identities on both hosts.|Inspect existing custody and authorized recovery alternatives through Akki; verify remote executor, source descriptor and lawful scope. No guessed key mismatch/GPU fault or pod extraction workaround.|Fresh bounded census actually executes inside Akki and emits validated output/receipts.|
|3|Census/registry coverage and resilience|Scoped retained-record reads, guards, real-state UI and adapters implemented; live output unverified.|Verify admitted source groups lane by lane, ownership/persistence, partial outcomes, stop/retry/restart and required measurements. Metadata-only estimates do not establish content/quality coverage; deeper profiling must have authority.|New authorized evidence appears consistently in OS/DAP, survives recovery, and never falsely completes.|
|4|Durable request-to-result workflow|Inspected portal submission remains an acknowledgement-only STUB; internal commissioning machinery exists.|Persist request, freeze scope/objective, dispatch through existing orchestration, wire approvals/refusals/stop/retry, results and history to the same record.|DAP request becomes the same OS work item, executes, returns a governed result and durable receipt without pod intervention.|
|5|Terms, entitlements, allowance and metering|Inspected DAP data bindings remain STUBBED.|Connect authoritative licence/catalogue/rule and usage-event readers; enforce allowed purpose/output/budget; no invented pricing, grants or zero usage.|An admitted user sees correct rights/balance; disallowed or over-budget actions are refused before work, and real work is metered.|
|6|OS operational surfaces|Census/Registry corrected; other workspace journeys mixed/unverified.|Trace and bind existing Commission/Tasks/Board/results/documents/approvals/monitoring; verify Chat/ThinkLab/Solva/memory/rules/Watch individually, reuse functioning mechanisms.|Required enabled OS actions perform the promised operation and expose evidence and recovery, within original prototype flow.|
|7|DAP output journeys|Mixed: provision/contracts exist, callable-skill query has answer_stub; full output journeys not established here.|Finish each required path: processed intelligence, trained models, callable skills and separately governed raw release; share identity/work/output records with OS.|Each enabled output can be requested, governed, executed and received with appropriate proof and history. No sample answer substitutes execution.|
|8|Governed models/audio/training|Real training code and historical runs exist; current requested governed journey and acceptance not demonstrated.|Compose real dependencies inside Akki, verify corpus rights/custody, calibration, per-stratum evaluation, MOAC/admission/promotion and failure refusal.|Actual evaluated artifacts are admitted only when all applicable criteria pass. No launch/loss/heartbeat substituted for acceptance.|
|9|Operational acceptance and handover|Slice tests verified; full runtime-aligned suite/recovery acceptance not completed.|Align test sources to runtime, run whole required journeys and negative cases, interruption/restore/idempotency/tenant/custody tests, operator runbook and owner walkthrough.|All mandatory readiness gates pass with retained evidence; exclusions only where the Canon and agreed scope permit.|

## Concurrency and recommended next deliverable

- The execution-access issue must not become a reason to stop all independent work. Journey/ruling mapping and non-executing contract/prototype binding analysis can proceed in parallel with authorized recovery after approval.
- First next deliverable: a fixed functionality ledger, plus one real Akki-owned census whose output is shown in both OS/DAP. No additional UI redesign.
- Next deliverable after that: one full DAP request → same OS work item → execution → governed result/receipt → DAP history journey.
- Skills/model/audio work is release-blocking when enabled, not silently deferred behind a readiness label.

## Progress reporting rule proposed for the full programme

Functional progress = (required journeys verified end-to-end with real execution/evidence) / (all required journeys in the baselined ledger) ×100.

Every journey carries a separate state: **verified**, **partial**, **blocked**, **unreviewed**, or **not started**. Partial/blocked/unreviewed are not counted as complete. Existing implementation receives explicit credit separately so an unverified journey is not falsely described as absent. Report test pass rate separately. Report mandatory release blockers separately: a high average never overrides a failed required gate.

No calendar or cost precision is justified until the remaining journey map and access/custody findings establish the work involved.