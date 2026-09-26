# Akki — promise-anchored requirements gap analysis

**Owner request:** surgical line-by-line analysis of the entire requirements list,
showing what must be done to deliver Akki's promises; report before implementation.

**Disposition:** read-only assessment. No application or Canon changes, database
writes, live source pulls, provider/model calls, GPU troubleshooting or runtime
drills. Assessment files and recovered original documents only.

## 1. Executive conclusion

Akki has substantial contract/kernel work and a narrower set of real integrated
control-plane paths. The dominant deficit is **the connection from authoritative
inputs through an effective enforcement decision to a real operation and its
durable, consumer-visible evidence**. A constant, frozen shape, vocabulary, gate
helper or green unit test is not the corresponding platform-wide promise.

Conversely, it would be wrong to call the whole platform absent. Existing custody
sequence, gate helpers, immutable types, certificates, training manifests,
compaction carriers, entitlement derivation and the tested DAP request record are
foundations to reuse. Older gap descriptions are not necessarily current gaps:
TCB/determinism inventories, handoff registration and Watch Learning mechanisms
now exist in inspected code. Some are still unproved operationally.

**No justified whole-platform delivery percentage can be computed from this
review.** Its units are scoped requirement dispositions, not independently
operational features. Several requirements express limitations or decisions,
not capabilities that should be invented.

## 2. Coverage, precision and explicit incompleteness

### Primary requirements

The latest owner workbook contains **648 distinct `(Doc, Rule ID)` rows across
56document families**. Every key is preserved exactly once in
`REQUIREMENT_GAPS_648.json`, `.csv` and `REQUIREMENTS_LINE_BY_LINE.md`, including
literal original statement, authority label, intended outcome, inspected code
references/hashes, exact gap, action and closure demonstration.

Final static-review dispositions:

| Disposition | Rows | Meaning |
|---|---:|---|
|PARTIAL|475|Relevant behavior exists, but the whole requirement is not established operationally|
|UNVERIFIED|128|Current evidence does not support a delivery claim; this is not proof of global absence|
|SOURCE_UNRESOLVED|24|Original/source authority needed to assess scope precisely|
|SPEC_DECISION_REQUIRED|7|A positive proposal, asynchronous contract or expressly unruled obligation needs disposition|
|EXPLICIT_NONCLAIM|1|The insurance-telemetry aside is expressly unadopted, not missing work|
|EVIDENCED_SCOPED|13|Inspected narrow behavior/shape is evidenced; NOT a platform-wide or production guarantee|

All35assurance promises S1–S35 have individual source text, bounds, linked
requirements, concrete delivery work and falsification scenario in
`PROMISE_GAPS_35.json` and `PROMISES_LINE_BY_LINE.md`. Product promise#N is a separate
namespace; references do not merge with S-N merely because the number matches.
The registry has no literal#5/#28/#29 cross-reference; that is a crosswalk gap,
not evidence that those promises do not exist. They require source-body resolution.

### Supplemental Canon coverage — NOT fully closed

Fifty original/derived source bodies were extracted. Principal, memory, entitlement
and content originals were recovered through prior custody URLs and matched their
previously banked hashes. The initial missing-file finding for Doc1–15 was
corrected: originals exist under `assessment_workspace/fixtures`, not just custody.

The source inventory found **848 candidate normative/limitation/ruling blocks**.
These are NOT848additional adopted requirements. They include repeated Canon,
definitions, elaborations, failure posture and historical diagnoses. Current
reconciliation:

| Supplemental disposition | Blocks |
|---|---:|
|Explicit registered-clause overlap|214|
|Ruling/authority dependency|64|
|Explicit limitation/nonclaim|34|
|Source-version duplicate|26|
|Historical diagnosis, not a current finding|1|
|Source-context linkage still requires analysis|191|
|Foundational Canon linkage still requires analysis|318|

**509source blocks still need semantic trace closure.** They are analyst-owned
review work, not509missing features or509decisions for the owner. Therefore this
report does **not** claim that every referenced Canon paragraph has received a
fully closed semantic gap assessment. The648-row matrix is complete in accounting;
the wider promised all-Canon audit is not yet complete. That distinction must
remain visible when this report is presented.

### Confidence boundaries

- No live compliance, security, resilience, quality or performance certification
  was performed. Existing146passing tests belong to a narrower previous DAP/census
  slice; some positive executor/admission cases are **MOCKED** fixtures.
- Static claims of global absence from unrelated files were rejected. Correction
  packs replace the initial broad reviewer drafts; all drafts remain banked.
- Current file hashes and actual EOF-bounded code citations are banked. A correct
  hash proves which code was read, not that the semantic conclusion is infallible.
- Some source statements are summaries. The source-body qualifiers remain
  load-bearing; missing authoritative wording is not guessed.
- The source-pending cases are11streaming-extension clauses,11ROC clauses and
  two explicitly unrecovered deck statements (DR-R10/DR-R13). Available mechanisms
  may be inspected, but exact original obligations remain bounded by source gaps.
- Shared-workspace reviewers do not establish hardened EX4 write isolation or
  different-family R37 independence. No statistical confidence is implied by the
  labels used in this desk assessment.

## 3. Objective-anchored delivery gaps

The goal is not maximal machinery. For each promise, ask whether a user can
experience the promised outcome, with the stated refusal and limitation behavior,
while the platform can produce authoritative evidence of it.

| Delivery boundary | Existing foundation | What remains necessary | Decisive closure |
|---|---|---|---|
|**Custody / no leakage / confidentiality / dual files**|Sole invocation and de/re-identification path, token maps, typed payloads and confidentiality helpers|Establish sole-client enforcement on every build and deployed network route; coverage of tenant identifiers; exception-safe envelope destruction; document/perception parity; faithful pre-mask intent and separate retained-file custody|Attempt side invokers, tenant-specific identifiers, thrown errors and a perception crossing; no forbidden content/map persists or crosses and every admitted/refused outcome is correctly receipted|
|**Principal attribution and task authority**|Principal models and read-only propagation adapter; currentJWT/account scope supports a tested portal slice|Durable owner admission, governed credentials, every record-producer binding, no caller/default identity paths, immutable async/task handoffs and correct revocation semantics|An authenticated-but-unadmitted identity cannot write; admitted identity survives queue/handoff; spoofed identity and dual authority refuse before effects|
|**Northena / DAP / work lifecycle**|Real immutable request intent, same-key replay/conflict, sharedOS/DAP records and actual-state refusals|Operation rights, price/terms disclosure, independent recorded approval, admitted engine dispatch, effect-safe metering, actual cancellation/retry/delivery/retrieval|One approved bounded request executes through an Akki engine and returns its verified artifact; denied/expired/widened/ledger-failed counterparts cannot act; same evidence appears in both products|
|**Ledger / effective state / governance atomicity**|Hash-chain writer, canonical envelopes and scoped Mongo compare-and-append; existing ceremony structures|One authority per record, all producers bound, atomic effectiveness of rulebook+registry+ledger+in-force transition, restart-safe budgets and commit ordering|Crash at each transition boundary: prior policy remains effective or a complete new version is effective; abandoned attempts remain receipted; never delete history to simulate rollback|
|**Estate connection / census / Mtafiti registry**|Connectors, census scaffolding, profiler, registry shapes and validation seams|An admitted real source, stable population/snapshot, exhaustive or explicitly bounded coverage, canonical registration and actual fields/sizes/media/rights/quality/cost updates|Akki-owned source execution reconciles exact population and registers validated output visible consistently; unavailable source is not empty or successful. Current provider/GPU path remains parked|
|**Solva / grounded reasoning / probability and assumptions**|Reasoning envelopes, evidence-floor helpers, trace and assertion boundaries|Real qualified-unit resolution, implemented decision/assumption/consistency/uncertainty behavior, load-bearing claim attribution and verified all-surface class constraints|A factual response is traceable to permitted units; contradictory/missing/revoked/unqualified support yields the Canon-defined marker/refusal rather than invented facts or fabricated probabilities|
|**Context / Service1 / memory preservation**|Five-ring units, working set, warm packaging, compaction carriers and class-preserving helpers|Whole-unit qualified delivery, deterministic retrieval/window selection, genuine re-extraction handles, loss propagation, durable publication-after-receipt and rights withdrawal|Re-derive the selected context from pinned inputs, reproduce exclusions and reload byte/hash-bound memory; no class upgrade, silent split or revoked dependency remains usable|
|**Targeta / CIF / useful retained learning**|Candidate selection, yield layer, learning proposals and separation contracts|Actual admitted training candidates, measured yield/refusal/robustness, origin-preserving proposal evaluation, independent rule/capability admission and drift ceilings|A valid proposal can improve a measured admitted artifact; its author cannot ratify it or alter a live deterministic floor; CIF halt does not stop Targeta's remaining lawful work|
|**Training / models / serving integrity**|Training runner/manifests, model registry and fixed acceptance shapes; some criteria explicitly mocked|Actual weight/engine/config hashes, objective-specific parameters, real acceptance demonstrations, holdout robustness, integrity-preserving serving under pressure and correct withdrawal descendants|Register and serve a genuinely trained accepted artifact; tampering/load/precision/context substitutions either preserve the promised token result or explicitly refuse, never silently substitute|
|**Audio / voice / language / stream modes**|Token/condition/character and distance contracts, registration boundaries, modality seams|Real acoustic tokenization, source-identity distance validation, affirmative voice exclusion/authorization, media integrity, locale/register normalization and admitted latency evaluation|Show source-identity protection and intended intelligibility with actual audio outcomes and certificates; a parameter field or training completion does not demonstrate either. Streaming authority remains partly unrecovered|
|**Watch / containment / swarm / resilience**|Typed verdicts, certificate library, closed sever signals, ladder/budget helpers, witness/continuity abstractions|Real all-boundary observation/enforcement, atomic aggregate budgets, effective friction/mirage isolation and replay, external witness, restart-proof state, operational drills and notification/recovery receipts|Exercise actual rails safely under failure/concurrency: suspicion alone cannot sever, forged signals cannot escalate, cumulative parties cannot evade ceilings, current containment survives Watch failure|
|**Rules Service / business governance / trust domain**|Ceremony, TCB/determinism declarations, handoff registry and floor checks exist|Runtime producer/consumer coverage, material-change authority, atomic effectiveness, trueappliance/network placement, SoA and actualoff-box witness; ownerRPO/site-loss choices|Refuse an unauthorized/weakening/dual-hatted/unregistered change; lawful change follows its recorded ceremony; demonstrate placement/recovery at the infrastructure boundary rather than infer it from Python types|
|**Learning withdrawal / retention / erasure**|Pruning, lineage and compaction references/helpers|Complete descendant index, admission invalidation, recorded re-derivation/notice, late-job races, lawful read/erasure authority and no refund of spent privacy budget|Revoke one unit during a queued/train/serve cycle: no affected stale artifact becomes valid, descendants are accounted for, permitted replacements are re-admitted and spent budget remains spent|
|**Entitlement / commercial truth**|Licence/catalog/allowance/cascade primitives; real read-only ledger projection returns honest unresolved state|Owner admission and canonical producers; operational own-key protection; event-time terms; correct dials; concurrent ceilings/seats; rollover and meter-before-effect for actual execution|A caller gets exactly the admitted disclosed route and terms; price/pause/revoke/seat races cannot grant unauthorized capacity; invoice and allowance derive from authoritative metered events, never a cache|
|**Product surfaces / content / reports / skills / WPW**|Owner prototypes and tested held-work bindings; content vocabulary/scanners; rendering and export structures|Full journey/slot dependencies, actual resolver/salience gates, truthful measurements, permitted Generated surfaces, working report/deck/skill materialization with class and attachment gates|Trace a rendered claim/number/action back to live authority; unavailable data is visibly unavailable; callable skill returns a grounded result only through an admitted executor; no static stub masquerades as delivery|
|**EX / DQ / CC extensions**|The previous grounded spec assessment and reusable seams|Pin EX contracts and acceptance; DQ snapshot/pack checks and downstream eligibility; CC custody/window/metrics and protected paired benchmark, after explicit rulings|Account for the actual objective population, keep unknown material out of undeserved eligibility, disclose context loss and measure genuine quality/latency/availability cost rather than manufacture compliance numbers|

## 4. Corrections to misleading older conclusions

1. **“Built” is not one status.** Older297/632desk counts refer to differing
   buildable denominators and mechanisms. They do not establish the current648
   owner requirements as delivered or missing. No new percentage is substituted.
2. **Historical gaps are not current diagnoses.** TCB inventory, independent CIF
   stop, handoff role restrictions and Watch Learning structures now have code
   evidence. Their whole deployed guarantees still need evidence where claimed.
3. **Content R32 is not pending again.** The owner whitelist is explicitly recorded
   in `STATE/DECISIONS.md:26004–26006` (also27001ff): chat answers,
   recommendation bodies, notification bodies only. Correct the stale workbook
   description; code itself is not the authority and no re-ratification is assumed.
4. **Timed constants are not timed delivery.** S10one-hour recovery and S11
   72-hour notification are PARTIAL, not proved by the constants/helper presence.
5. **In-memory does not mean MOCKED.** A real process-local helper is a durability/
   scale/continuity limitation, not automatically a mock. Actual mocked evaluation
   criteria or injected positive fixtures are labelled separately.
6. **Do not close atomicity by deleting ledger rows.** RBM10needs atomic *effective*
   state with durable commitment/abort evidence, not destructive rollback of an
   append-only authority.
7. **Not every unresolved DEFAULT needs a new owner decision.** Apply the existing
   recorded binding protocol. Genuine OWNER/ruling conflicts are distinguished
   from defaults awaiting an implementation declaration.
8. **Do not overstate the offline-revocation conflict.** The recovered principal
   specification's failure posture explicitly refuses an unreachable revoke and
   leaves credentials valid until revocation is confirmed. CC10must be reconciled
   to this acceptance semantics and freshness policy—not described as logically
   impossible merely because a revoke could not be committed. Never claim an
   offline verifier knows an unreceived revocation.

## 5. Prioritized delivery program — proposed, not authorized work

### P0: restore authority and establish the actual enforcement spine

**W0 — requirement/source closure.** Recover the24source-bounded statements; resolve
the509remaining source-context/foundational links; map product#5/#28/#29; reconcile
648registry/602QA and stale counts/authority labels. Atomize SFP1–6concatenated cells
against source, not by guess. Pin the first EX task contract with intended outcome,
exact population, failure classes and acceptance evidence. This is an audit closure
step, not a new implementation feature or demand for509owner rulings.

**W1 — identity, custody and effective authoritative writes.** Finish owner admission,
identity propagation, canonical producer bindings, failed-write refusal, immutable
task/handoff authority and operational sole-crossing controls. Protect subsequent
work from creating unowned/unreceipted effects. Preserve existing correct helpers.

**W2 — one real bounded source-to-registry operation.** Execute only through an
admitted Akki-side host, lawful scope and source snapshot; reconcile and validate
canonical output. The existing GPU/provider problem remains parked, not retried
by this report. If unavailable, this proof remains blocked; fixtures cannot close it.

**W3 — complete one real governed user outcome.** DAP commission→disclosure→approval
→admitted executor→meter→result→rights/checksum-gated retrieval, mirrored inOS/DAP.
Add cancellation/retry only with real executor/approval receipts, not status edits.
Keep refusal and unavailable outcomes explicit. No prototype redesign.

### P1: close value, quality and control loops together

**W4 — grounded answer and warm service.** Qualified units→frozen objective and
custody classification→context assembly/loss→Solva→output/content gates. Bind
memory provenance/erasure and measured request class/time. This proves useful
answers, not just stricter refusals.

**W5 — unit eligibility and commercial correctness.** DQpack/snapshot assessment
and agreed classifier/admission table; operational licence/catalog/key producers,
historical metering, concurrent quotas and rollover. Cleanliness is not truth or
rights. Quote and spend cannot live in competing stores.

**W6 — operational Watch and governance.** Certificate-driven decisions, bounded
effective rails, independent external witness, real recovery/notification drills,
party-level aggregation and atomic rule effectiveness. Explicitly preserve
security/governance separation and non-severing ambiguity behavior.

### P2: specialized faculties and release proof

**W7 — training, serving and withdrawal.** Replace mocked evaluator results with
actual acceptance experiments; preserve exact admitted artifact identity through
serving pressure; complete withdrawal/re-derivation and capability lifecycle.

**W8 — media/voice and all transformed outputs.** Actual governed voice/media outcomes,
threshold/corpus decisions, latency bounds, report/deck gates and real skill
executors. Respect unadopted proposals, absent source statements and hardware gates.

**W9 — complete surface coverage and measured releases.** Original prototypes and
registered content slots for every promised journey; held-out paired benchmark,
per-tenant hardware/load/availability evidence, genuine independent re-performance
and non-builder demonstrations. Pin the benchmark earlier so it remains held out;
run release claims only once the corresponding path truly exists.

This order is not a permission to defer foundational custody or required release
floors until after exposure. Admission/TCB/privacy/rights gates remain prerequisites
where the governing source places them; P1/P2are sequencing groups, not waivers.

## 6. What requires an owner disposition versus engineering

**Owner/source decisions:** original unrecovered obligations; expressly unruled
RPO/site loss; ambiguous DQpartition/repair/exception precedence; CCdisclosure and
benchmark experimental custody; owner-class R37; any truly unresolved rulebook
counter-signatory/threshold/corpus choices. First check the existing decision
record—do not reopen R32 or a ratified DEFAULT accidentally.

**Engineering, not another owner debate:** source/citation crosswalk repair,
all-writer identity propagation, failure-before-effect ordering, durability,
idempotency, exact artifact hashes, actual telemetry, existing policy enforcement,
receipted tests and truthful UI bindings.

**External dependencies:** admitted compute/source access, independent witness/
replica placement, benchmark/reference custody and any legal reseller agreements.
Reseller-frontier legal R24does not automatically block local or Your Keys modes.

## 7. Reading the line-by-line appendices

`REQUIREMENTS_LINE_BY_LINE.md`: all648original rows, current scoped findings,
actions, closure demonstrations and code citations. Same dataset available as
CSV/JSON. Source authority and delivery state are different fields.

`PROMISES_LINE_BY_LINE.md`: all35assurance promises with their literal bounds and
concrete delivery work. The promise's limit is part of its acceptance test, not
an inconvenience to eliminate.

`FAMILY_COVERAGE_56.json`, `PRODUCT_PROMISE_CROSSWALK.json`,
`SUPPLEMENTAL_RECONCILIATION.json`: denominator/cross-reference coverage and
remaining trace work. `CODE_SOURCE_HASHES.json` pins inspected code bytes.

**Status of this report:** the648-row requirement accounting and35promise
assessment are available for owner review. It would be false to label the entire
referenced-Canon audit fully closed while509source blocks and24original-source
cases remain unresolved. No implementation should be inferred from this report.

## 8. Verification receipt and residual assessment quality

Raw-workbook/file-hash and exact-set verification is banked in
`verification/final_verification_receipt.json` and `test_reports/iteration_13.json`:
648primary rows,35literal promises/bounds,648/35rendered cards,848supplemental IDs,
and cited code/source hashes match. No application tests were executed.

A deterministic33-row semantic sample yielded31agree/2uncertain/0disagree.
Uncertainty was retained for **DR-R14(build isolation, not render determinism)**
and **RBM12(versioned amendment with prior-history retention)**. Main-reviewer
re-reading tightened those rows with concrete scenarios and identified their
specific missing proof; it does not retroactively turn the independent sample
into33passes. The first commentary description misnamed those topics; the source
statements and corrected row cards, not that description, govern this report.

The verifier also found repeated gap/closure language in some review families.
Shared blockers legitimately affect multiple rules, but repetition cannot prove
that each rule's distinct semantics is closed. Further row-specific refinement
of affected evaluation/review/governance families remains an **assessment-quality
action**, alongside the509source trace gaps. The report must not be presented as
an airtight, fully surgical all-Canon audit until those are closed.