# Enhancement-spec ingestion and all-component integration review

**Revision 2 — combined files17 + files18 report.** Owner asked to add the second
archive before responding to the original findings and confirmed review-only scope.
The prior report is preserved at `supplement_18/INTEGRATION_REVIEW_FILES17_SNAPSHOT.md`.

**Scope:** owner asked to ingest `files (17).zip` and `files (18).zip`, give thoughts,
and map integration across **all affected components**. This is analysis and custody banking only:
no application/Canon source edits, database writes, rule ratification, provider
calls, source-data reads, migrations, or GPU troubleshooting.

## 1. What was received and what changed

The first archive has4members: Execution Standard v1; Data Cleanliness v1; Security
Assurance Promise Set; Master Requirements Registry. The second has3members:
Context and Capability v1 plus revised Security/Master workbooks. This is7custodied
file versions and5currently applicable document titles (3specs +2latest workbooks),
not17or18files. Immutable first-drop bytes and hashes:
`custody/owner_drops/enhancement_specs_20260926/`; full ordered/cell-addressed
extracts and manifest alongside this report. DOCX text extraction includes tables;
paragraphs without a style are retained. No tracked insertion/deletion content
was found by the extractor; workbook formulas were not executed. Second-drop
custody is `custody/owner_drops/enhancement_specs_18_20260926/` and its extracts/delta
are in `supplement_18/`. The new specification prints27September2026; custody
was recorded26September. Preserve both dates; do not infer ratification from either.

- **Execution:** EX-1..EX-15: denominator-first task contracts, per-member outcomes,
  protected acceptance, shortcut detection, independent seeded re-performance,
  and evidence-bound completion claims. Covers runtime AND engineering/audit work.
- **Cleanliness:** DQ-1..DQ-15: seven check families, four strata, source/version
  register, deterministic repairs, training and factual-answer exclusions. DQ-8
  extends families1/4/6 to media; it is not an eighth separate check family.
- **Context and Capability:** CC-1..CC-16 adds mandatory custody-aware local routing,
  deterministic window assembly/loss disclosure, measured Ledger/request budgets,
  warm ratio, three-gate-service resilience and a standing paired capability benchmark.
- **Eleven rulings:** initialR36–40 plusR41–46 for operational floors/budgets and
  quality deltas. R37 is OWNER, not DEFAULT-class; remaining recommendations are
  DEFAULT-class, not measured service guarantees.
- **S-34 is the newly added assurance promise. S-33 is retained Content Registry,**
  not a new Execution Standard promise. Compared with the hash-verified20Sep v6,
  S1–S33 row contents are unchanged and none removed. The second archive adds
  **S35 Context and Capability**; all S1–S34 rows are byte-value unchanged in the
  workbook comparison. It neither replaces nor discharges S34 cleanliness.
- EX/DQ/CC rule statuses in the latest workbook are **PROPOSED**. The Execution
  document says SO§7 binds from next objective-card pin after banking; this review
  exposes that authority/status difference rather than silently promoting rows.
  No new build card was pinned here. Existing DAP work is not retroactively
  labelled EX-compliant just because its tests passed.

### Deterministic registry reconciliation

| Item | Directly counted |
|---|---:|
| System Rules Registry data rows / unique `(Doc,Rule ID)` keys |648 /648|
| QA Verification data rows |602|
| Registry keys missing from QA |46: exactly15EX +15DQ +16CC|
| Build Status stated total |635, with no derivation reconciling it to648 in that sheet|
| Registry Legend stated count |286; inherited note not a current denominator|
| Objectives sheet |O1–O12 plus a cross-cutting note; no O21/O22/O23 entries|

The available20Sep v4 baseline was re-fetched via its prior custody URL and matched
SHA `72160287…ad588` exactly. Against that595-row baseline:37additions,0removals,
2changed rule rows. The37 are7SFP rows (stamped20Sep(c)) plus30EX/DQ rows. Do not
pretend all37 originated in the26Sep design change. A602-row v5 is cited by code
but its workbook bytes were not located for direct comparison in this pass.

The first-drop632/602/30missing counts are historical, not discarded. Direct
files17→files18 comparison adds exactly16CC rules and removes/changes **zero**
previous rule rows; latest648QA gap46. Old EX/DQ statuses and unresolved source
findings therefore remain. The CC opening says “eight requirements” while the
operative clauses enumerate16: preserve the16rule denominator, flag that summary.

Two inherited deck rows, DR-R10/DR-R13, now explicitly say **statement unrecovered**;
do not accept those placeholders as requirements. SFP1–SFP6 Statement cells
contain subsequent SFP table rows concatenated into them, rather than only their
own atomic rule. This is a provenance/extraction problem, not permission to guess
replacement wording. Security Legend says S1–S34 are entirely Watch-scoped while
its own S31/32/33/34 rows concern Entitlement/Principal/Content/Cleanliness: revise
the scope explanation. None of these source files was silently corrected.

Workbook implementation/ruling labels are also not a runtime authority: for
example, its S33 bound still refers to R32 as owner-pending, whereas
`content_registry/content_registry_vocabulary.py:9–17,48` cites a later owner
whitelist of chat answers/recommendation bodies/notification bodies. Preserve
that already-banked authority; do not reopen it merely because the inherited
spreadsheet cell is stale. This is distinct from the new R37 owner choice.

## 2. Architectural judgement

**Strong direction; integrate as three cross-cutting capabilities, not another
standalone portal or parallel registry.**

Execution Standard answers: *Did this task account for the population it promised
to handle, and can another executor verify that?* Data Cleanliness answers: *Which
named checks did each record pass, and is that record admissible for this use?*
Context and Capability adds: *What eligible material and entity knowledge actually
reached the model, what did governance exclude, and what measurable cost did that
have on quality, latency and availability?*

They close different gaps. A fully accounted-for job may be wholly refused; that
does not mean usable output exists. A Clean record is neither proven true nor
rights-cleared. Quality, evidence class, authorization, model admission and
billing remain distinct decisions whose prerequisites are composed, never
substituted for one another.

### Proposed integration flow, not current executed functionality

```
authenticated principal + lawful purpose + approved source scope
  → Northena/Work Supervisor: six-field task contract + accepted enumeration
  → Akki-owned Census execution (never E1 as data path)
  → Mtafiti: snapshot + owner-confirmed rule-pack version
  → deterministic record/file checks → bitmap + match/disagreement evidence
  → strata/repair receipts → acceptance + re-performance → canonical register
       ├─ Targeta / training commission / MOAC / model admission
       └─ Context Manager / Service1: qualified unit population
            → frozen entity-knowledge decision → custody-admitted model route
            → deterministic window + versioned loss statement
            → Solva assertion ceiling / sole chokepoint / output gate
            → Content Registry dependencies → original OS/DAP prototype bindings
  → Ledger: hash-bound receipts and decisions; Mkondo: governed handoff refs
  → per-tenant timing/availability evidence + isolated paired benchmark
  → release acceptance (not proof supplied by this document review)
```

Use versioned payload/sidecar references around existing frozen contracts. Do not
add fields ad hoc to the17-field Ledger row, silently change sealed signatures,
create a second Mtafiti writer, or create a free-standing entitlement store.

## 3. Impact across19 component groups

All paths below are relative to `backend/vendored/extraction_akki/backend/` unless
otherwise stated. These are inspected integration seams, not certification of
every file or route in the named component.

| # | Component group | Existing evidence / boundary | Proposed integration and remaining work |
|---|---|---|---|
|1|**Northena**|`services/northena/portal_work.py:45–73`: immutable request intent, replay, Routing hold|Attach accepted task/denominator refs; project processed/refused/unmeasured accounting separately from execution, approval and output availability. No fake Ready from reconciled refusal.|
|2|**Work Supervisor / builders / agent tasks**|`work_supervisor/job_manifest.py:75–95`: scope/output_contract/dependencies/precondition seals|Add governed six-field contract adapter, dependency admission, protected acceptance boundary and second-executor dispatch. Existing opaque dicts do not enforce EX1–15.|
|3|**Connect / Source Plane / Census Autonomy**|`census_autonomy/operational_runner.py:25–91`, `census_canon/estate_enumerator.py:119–134`|Pin source and record/file populations; stream/shard remotely against stable snapshot/watermark; record unreachable members. Preserve approved connector descriptors and E1/data-path separation. GPU is still parked.|
|4|**Mtafiti / canonical estate registry**|`mtafiti/quality_profiler.py:115–186` defaults3tables/schema,10columns/table,200rows; `census_canon/stratum_measurement.py:7–13` preserves Unmeasured|Own bitmap, pack-bound stratum classifier and garbage-register publication. Existing samples are candidate/profile inputs, not record-population proof. `asset_registry_writer.py:53–78` is explicitly an in-memory thin kernel: establish durable canonical artifact backing, not a second authority.|
|5|**Rules Service / Checker / change control**|`rules_service/ceremony.py:89–190`: typed change request, countdown/witness/signatory, new record|Owner confirms source packs, sentinels and semantic predicates. Rule/threshold/repair changes must version and receipt re-stratification; no learned proposer may silently admit a rule. Reconcile proposed status, TCB scope and closed contracts first.|
|6|**Targeta**|`targeta/core.py:39–79` filters defensibility and ranks sources; `targeta/plan.py:39–74` pins registry snapshot|Consume cleanliness-qualified unit references and coverage, not a mutable aggregate cleanliness score. Quality eligibility before yield ranking; existing yield veto scaffold is not proof of a DQ gate.|
|7|**Training Runner / MOAC / Model Admission / model registry**|`training_runner/moac_emitter.py:32–42,119–126` fixed six-check card and MOCKED safeguards; `model_admission/ceremony.py:70–95` another six-field criterion mapping|Add per-unit pack/bitmap/repair/owner-exception proof at commission and bind the admitted manifest hash through training/admission. Versioned extension or new precondition envelope needs ratification; neither six-check shape can be casually called seven. Missing existing real robustness/refusal evaluation is not fixed by DQ.|
|8|**Solva / assertion and output boundaries**|`solva_v2/assertion_boundary.py:21–38` thin non_factual/utterance return, real unit lookup deferred; `solva/reasoning.py:128–191` separate chokepoint pipeline|Resolve source-unit quality before grounded class computation: Junk cannot fact-anchor; Suspect ceiling inference subject to existing taxonomy. Clean never raises class automatically. Preserve sealed signature and connect both reasoning paths; do not assume one function protects every answer.|
|9|**Callable skills / chat / deck and report consumers**|`routers/transform_forms.py`, `portal_operational/skill_query.py`: admitted-executor refusal, no fabricated answer|Propagate grounding and quality receipts per cited unit and per generated sentence through the same output gate. This spec does not supply the missing skill executor. DR-R10/13 source recovery remains a registry blocker, not prose to invent.|
|10|**Audio Plane / media and voice training**|`audio_plane_v1/channel_condition_profiler.py:154–180` unratified placeholder; `dedup_path.py:120–162` text-ref grouping with retained variants|Add deterministic file integrity/acoustic fingerprinting before training assembly. Header/decodability checks are not learned condition profiling. Distinguish redundant records from valuable condition variants; DQ must not erase the existing robustness stratum.|
|11|**Mkondo governed handoffs**|`mkondo/registry.py:48–95`: frozen handoff and role separation|Carry artifact/pack/snapshot/acceptance refs using versioned handoff payloads. Receiver verifies receipts; no second classifier or policy authority. An emitted intent alone is not durable DQ evidence.|
|12|**Watch / assurance / incident routing**|`watch/research_queue.py:74–121` proposal→grounding→ratification; `watch/verdict_interface.py` learned findings cannot act|Observe missing evidence, unsupported completion claims and integrity failures through existing verdict/certificate mechanisms. Quality anomaly or disagreement is NOT automatically malicious intent or authority to sever. Preserve Watch's closed security action signals.|
|13|**SyniSense / principal identity / custody / single chokepoint**|`services/chokepoint/llm.py`, existing principal context boundaries|Rule confirmations, repairs, exceptions and receipts must be attributed to admitted principals. Cross-source natural keys require approved linkage scope and protected identifiers; hashes of low-entropy IDs alone are not sufficient privacy. Raw rows/values stay in their governed data plane.|
|14|**CIF / research and retained learning**|`cif/output_routing.py:108–173`: proposal→deterministic acceptance→research/capability route|May propose rule candidates, not write confirmed packs or override strata. Learned quality signals remain research/plausibility flags under DQ LIM4; EX applies to proposal and evaluation populations too. Current in-memory sinks are not live durable DQ acceptance.|
|15|**Memory / retention / revocation / unlearning**|`memory/revocation.py:34–89`, `retention/authorized_deletion.py:69`|Index derived anchors by source/snapshot/record/pack/repair version. Pack changes invalidate affected eligibility views; rights withdrawals follow existing freeze/erasure paths. Junk listing is not deletion authorization; retained repair originals remain controlled assets.|
|16|**Ledger / evidence / independent audit**|`contracts/ledger_v1.py:29–46`, `ledger_writer/mongo_control.py`; `evidence_register/claims_validation.py:1–10` explicitly non-gating A4|Bank hashes, per-member outcomes, acceptance and disagreement refs via existing writer. Keep large protected bitmaps outside public receipts. Locate the intended audit completion-claim namespace: do not mutate A4 research validation into an execution gate. Acceptance scripts are evidence producers, not new TCB members per EX placement.|
|17|**Content Registry / OS / DAP**|`content_registry/content_registry_vocabulary.py:21–48` vocabulary/scanners; frontend `components/prototype/OwnerMarkup.jsx` bindings|Add registered Fixed/Templated slots for coverage, pack version, quality strata, measured/unmeasured, refusal and provenance. Generated explanations cannot supply numbers. Preserve exact prototype DOM/layout; no new dashboard design. Binding a value is not proof of a complete Content Registry resolver.|
|18|**Entitlement / cost and compute / release rights**|`services/portal_operational/entitlements.py`, existing licence/chokepoint semantics|DQ work is still subject to lawful scope, entitlement and compute budget. Meter actual governed consumption; do not invent a new quality credit balance or treat Clean as permission to train/download. EX overhead has real cost but this upload establishes no new tariffs.|
|19|**Context Manager / qualified-intelligence Service1**|`contracts/five_rings.py:169–218`, `service_1/dispatch.py:366–405`, `service_1/qualified_data.py:106–149`|Make whole qualified units the population for deterministic assembly; pin objective/frame/graph/version/budget; attach excluded-unit counts and handles. Existing class filtering and warm packaging are not CC4 assembly or measured warm/full guarantees. Bind five-ring re-extraction handles into memory without a parallel unit store.|

Universal EX scope also applies to future/less-exercised surfaces: their task
inputs must be enumerated when their build/runtime cards open. The19 groups are
an integration-impact organization, not a denominator of all platform files or
an assertion that every historic route has been audited. The additional CC impact
on the original18groups, proposed numbers and new cross-spec decisions are in
§8below; read that section as part of this combined report, not a detached proposal.

## 4. Rulings and design gaps to settle before enforcement

1. **Authority/status:** EX document effective-on-banking clause versus incoming
   PROPOSED rows. Record adoption and next-card/subwave boundary explicitly. Do not
   rewrite old evidence chronology. Recommended: follow its discipline for new
   cards while keeping implementation claims and adoption status separate.
2. **Unmeasured vs exact four-stratum partition:** DQ failure posture says unreachable
   records are unmeasured; DQ12 permits only four strata summing to source count.
   Do not invent a fifth stratum or default unknown to Clean/Junk. Recommended:
   separate assessment coverage from quality partition; withhold the final
   eligible-for-use register while required outcomes are missing. Owner must
   define whether/when a scoped preliminary report can publish.
3. **Partial register language:** the design note permits publication after cheap
   checks, while Clean requires every applicable check to pass. Partial checks may
   supply a clearly scoped coverage report, not a silent full-quality assurance.
   Pin precisely which confirmed pack is in force and which downstream purposes
   it can support. Zero configured checks must not pass vacuously as Clean.
4. **Stratum precedence:** reversible formatting failure can satisfy both Repairable
   and structural-Junk descriptions. A plausibility flag is not a fail but removes
   Clean eligibility; optional-field sentinel and missing/partial provenance need
   explicit handling. Ratify a total truth table; do not let implementation order
   decide policy. Pack identity alone is insufficient if comparison snapshot,
   related records or baseline changes: those inputs must also be pinned.
5. **Repair/training/exception semantics:** DQ14 says Clean or Repairable, the
   subtask10 table says Clean or Repaired although Repaired is not one of the four
   strata, and the same rule demands a passing bitmap for every unit while allowing
   Suspect exceptions. Recommended: require recorded repair plus recheck; retain
   original failed bitmap, and model a narrowly scoped exception as an explicit
   admission decision rather than changing failed bits to pass. Owner ruling
   must decide the final predicate. A human exception does not waive other MOAC criteria.
6. **S34 stricter than stratum wording:** it bars any sentinel from training/fact
   anchoring while Junk mentions required-field sentinels. Decide precedence for
   optional-field sentinels and Suspect exceptions. Until then, do not weaken S34
   to make a training test pass.
7. **Zero-tolerance spotcheck vs2% re-performance:** EX universal detector fails on
   any independently re-derived mismatch in its20rows; EX12 reopens above2% on
   the seeded5%/min20 second-executor sample. These can be separate gates, but must
   not be collapsed into one weaker tolerance. Define sample rounding, N<20,
   empty populations, canonical seed/sampling, nondeterministic comparisons and
   baseline estimates for velocity. Recommended N<20 approach: inspect the whole
   set, explicitly ratified rather than pretending20distinct members exist.
8. **R37 executor independence:** separate task/context is not automatically a
   different model family or technical write isolation. Record family/version
   and unavailable-family exception; protect acceptance artifacts outside the
   worker's writable scope. This analysis makes no hardened EX4 or R37 claim.
9. **Owner pack and threshold readiness:** R38 offers2%/20% candidate thresholds,
   not automatic sentinel confirmation; R39 and R40 recommend baseline-derived
   values but provide no actual fuzzy/media numbers. Pack unreadable → not-assessed.
   Missing required rules/owner decisions → explicit refusal/unmeasured; no guesses.
10. **Duplicate identity and media variants:** define row canonicalization, natural
    keys, snapshot-pinned deterministic retained-row selection and fuzzy metric.
    Duplicate membership and canonical selection must not depend on executor order.
    DQ says no merge path: keep human merge authorization separate from existing
    occurrence grouping that preserves media-condition variants. This distinction
    needs specification, not deletion of a sealed audio behavior.
11. **Changing estates and failure recovery:** pin row identity/version and source
    snapshot/watermark; otherwise identical counts can hide missing and duplicated
    members. Apply idempotent shard retries and exact ID-set reconciliation before
    publishing. Do not silently reconcile against a later row count.
12. **Existing class/schema vocabulary:** DQ uses inference; Solva's inspected
    sealed class seam currently exposes non_factual/utterance/fact-related types,
    and MOAC has two six-criterion representations. Ratify adapter/version changes
    and how DQ15's inference ceiling maps into each actual output path.

## 5. Recommended implementation sequence

**P0 — adoption and evidence discipline.** Reconcile QA/objective/summary metadata
and preserve source errors as findings. Pin EX task contracts for the next card,
an independently controlled acceptance script and closed reason taxonomy. Draft
the DQ truth table and source snapshot/pack schemas; settle the above blocking
choices. Update TCB/determinism/failure inventories precisely: DQ deterministic
runner/classifier/training gate IN; heuristic proposer OUT; EX scripts evidence,
not TCB. Do not infer a TCB decision for other new gates without the existing test.

**Revision2 prerequisite:** add CC1/2 classification/routing and CC4 assembly to
the specified TCB/determinism review; benchmark harness/proposing models stay OUT.
Pin the held-out benchmark and measurement protocol early, before tuning a model
or optimizing the path. Resolve one-call disclosure, cache revocation/freshness
and isolated bare-path authority before opening any of those paths. Do not use
CC10 as implicit permission to serve stale grants or raw controlled identities.

**P1 — smallest truthful structured-data vertical slice.** One named owner-admitted
source on Akki infrastructure: exhaustive inventory, owner-confirmed sentinel/
format rules and exact duplicates, versioned per-record results, protected
register, fail-closed training admission and the existing OS/DAP evidence view.
The slice must disclose its pack/check coverage and must not claim full seven-family
quality or live execution until those receipts exist. Source/GPU execution remains
blocked while the existing infrastructure problem is parked.

**P1 follow-on — complete families and consumers.** Owner consistency rules,
cross-source comparisons, plausibility/drift/provenance; Solva and skill fact-anchor
gate; Mkondo provenance propagation; memory invalidation and retention; registered
surface copy; real independent re-performance. Leave current DAP admission/executor
holds intact until actual upstream conditions resolve.

**Revision2 integration slice:** deliver a named warm-answer path through qualified
units, custody classification, deterministic assembly, loss-aware output and
end-to-end measurement, coupled to DQ eligibility. Add genuine gate-service
resilience and active-standby receipts through admitted infrastructure. Actual
tier floors and paired model outcomes are measured only after a working path
exists, and each image release reruns the stated acceptance protocol.

**P2 — media and broader rollout.** Deterministic file integrity/fingerprints and
ratified media thresholds; preserve audio robustness variants. Extend to other
sources with per-source contracts and scale measurements; no unsupported timeline
based on the spec's phrase “days of work”. Many cheap deterministic checks do not
need an LLM or GPU, but they still run on admitted Akki-side infrastructure.

## 6. Effect on prior status claims

The earlier146test pass count establishes the tested DAP control-plane slice,
not EX1–15 compliance or DQ1–15 coverage. No census sampled figure becomes a
per-record garbage register retroactively. No existing MOCKED training criterion
becomes real because a new prerequisite is described. The analysis clause map
initially accounted for36review items; the combined map now contains59
(15EX+15DQ+16CC+11rulings+S34/S35). That is review coverage, **not59implemented features**
or a platform-completion percentage.

## 7. Evidence index

- `DOCUMENT_MANIFEST.json`:4incoming files and source hashes.
- Full ordered DOCX `.md`/`.json` and workbook `.json` extracts: block and sheet-row citations.
- `REGISTRY_RECONCILIATION.json`: direct counts,30missing QA keys, exact baseline diff.
- `CLAUSE_IMPACT.csv`:36rows =15EX+15DQ+5rulings+S34, with evidence and integration ownership.
- `CLAUSE_IMPACT_COMBINED.csv`:preserved36 +23new rows; the new23are16CC+R41–46+S35.
- `supplement_18/`:3file hashes/full extracts, exact files17→18delta,23clause map,
  review contract and preserved prior-report snapshot. Its verification is separate.
- `REVIEW_CONTRACT.json`: checks, scope limits and proposed20-row seeded independent check.
- Source files unchanged; all outputs are assessment-side artifacts. Review validation
  status is recorded separately, not inferred from this narrative.

### Separate verification outcome

`test_reports/iteration_11.json` and `verification/verification_receipt.json`
record mechanical rechecks of the raw4-file archive/hashes,632/602 exact ID sets,
30missing QA rows,595-row historical baseline and37add/0remove/2changed delta,
S34-only security addition,36unique mapped clause IDs, and38existing code anchors.
The independent checker did not consume this narrative.

Its deterministic20-row semantic sample returned **17agree /3uncertain /0disagree**.
The3uncertain judgments are preserved, not overwritten or called passes:
- **DQ9:** a retention-deletion anchor supports retention ownership but cannot
  prove that no separate repair implementation exists anywhere else.
- **EX10:** per-source runner outcomes do not establish what reconciliation
  guarantees may be enforced by other adapters outside that anchor.
- **EX7:** the sampled card demonstrates acceptance criteria, not an exhaustive
  inspection of every possible six-field subtask decomposition.

These remain further evidence tasks before asserting platform-wide absence or
enforcement. Sixteen clause-map rows were outside the independent20-row sample.
No mocked APIs or synthetic business records were used. No live runtime behavior
was tested or changed during this document review. Neither shared-workspace
checking nor the unestablished checker model family proves EX4/R37 compliance.

## 8. Context and Capability — integrated revision2 assessment

### 8.1 How this changes the conclusion

The combined stack is now **EX: accounted-for work → DQ: admissible material →
CC: preserved context and measured capability/cost**. These are complementary,
not interchangeable. A task may be fully accounted for and still yield no usable
answer; a clean record may still lack rights or ground truth; a qualified answer
may still exclude useful material because of custody or context capacity.

CC makes those last losses visible. Most importantly, it turns local-first from
an economic preference into a **mandatory custody route for controlled entity-
knowledge objectives**, and makes window selection a governed deterministic
decision rather than a retrieval-model preference. It also makes infrastructure
availability part of the promise: a correctly refused request during a gate
outage is still an outage, not customer fault.

The overview says it changes no guarantee, but CC2 explicitly permits a narrowly
approved unmasked call and CC10 modifies outage-serving behavior. Those are
material operational policy changes requiring ratified reconciliation with the
existing no-bypass and immediate-revocation boundaries, not merely new labels.

### 8.2 Additional impact on the existing component groups

| Component / groups | Required addition or precedence | Inspected foundation and limit |
|---|---|---|
|Solva + Northena (1/8)|CC1 classifies pre-mask and freezes entity-knowledge intent; CC2 fixes custody eligibility before model selection|`solva_v2/intent_audit.py:15–38` records declared situation class, not the CC predicate. `objective_request_v2.py:151–166` has a closed envelope; use approved versioned binding, not an injected caller field.|
|SyniSense + sole chokepoint (13)|Approved disclosure is entity/custody-class/objective/model/call-scoped; all other checks remain engaged|`chokepoint/llm.py:287–299,432–468` deliberately has no bypass and sends redacted material. CC2 cannot be a raw-prompt Boolean. It must become an explicit governed policy branch, never a second provider client.|
|Entitlement + local catalog (18)|Filter candidates by CC custody rule before ENT customer-key preference, allowance or routing preference|`cascade_selector.py:113–149` currently prefers an admitted customer-key row first. Ownership of that key does not make an external provider local. No local competent/admitted model → bounded answer or refusal, not silent frontier escalation.|
|Context Manager + Service1 (19)|Assemble deterministically from the actually eligible qualified set, then preserve the committed unit order and exclusions|`five_rings.py` supplies edges/handles and `qualified_data.py` class filtering; `solva_depth/load_bearing.py:23–39` presently returns all candidates. Neither establishes CC4's budgeted ranking and selection.|
|Mtafiti + Targeta + training (4/6/7)|Provide snapshot-pinned quality/qualification/provenance inputs; exclude held-out capability references from every training/retained-learning path|DQ stays upstream of CC ranking: high rank cannot rehabilitate Junk or rights-denied units. Training must not learn the release benchmark.|
|Memory/retention (15)|CC15 binds compaction pointers to actual five-ring unit handles; CC5 shares disclosure form without copying the wrong population|Compaction currently holds free-form provenance references and8claim classes (`carriers.py:29–72`); normalized units have3defensibility classes (`five_rings.py:62–73`). A loss of a claim and a loss of a unit are not interchangeable counts.|
|Northena / Service1 / DAP (1/19/17)|Record warm/fresh/controlled request timing and actual warm delivery; controlled-human wait is reported separately|`service_1/dispatch.py:392–405` has warm packaging paths;441–491 has a persisted fresh202path with quote/enqueue. Do not call all of this a stub because the old module header says Phase2. These inspected paths have not been performance-tested here.|
|Ledger / Rules / credential plane (16/5/13)|CC7 load evidence; CC10 signed-read rules, exclusive writer failover and sealed verification cache|Mongo append correctness is not500/5000rps proof. Credential `_ISSUED` is an in-memory map, not a sealed resilient cache. Rules-change ceremony is not proof of signed offline serving. Hardware/replication/fencing/cache semantics must be separately demonstrated.|
|Content Registry + existing OS/DAP (17)|Register fixed CC3bounded-answer, CC5loss and CC11gate-outage copy; display measured per-tenant/period values and explicit not-measured|No redesign. Add model inputs/dependencies to original prototype bindings. Loss counts and performance figures are measurements, not Generated narration.|
|Mkondo + trace (11)|Carry objective/classification, pack, window, excluded-handle and benchmark artifact references across handoffs|Keep identity/custody on opaque references. Do not copy protected raw excluded-unit text into public operations surfaces.|
|CIF + Watch research (14/12)|May propose assembly-rule changes through research/ceremony; never rerank/filter the committed live window|Preserve judgement-versus-policy separation. Operational outage and context loss are not automatic security verdicts or new sever signals.|
|Work Supervisor / release / independent audit (2/16)|Standing benchmark under EX, per-release artifact hash, and four CC16functional demonstrations by non-builder identity|Generic manifests/seals are reusable carriers, not implemented CC release gates. Review tests and builder access do not meet the non-builder demonstration requirement.|
|Skills / reports / audio (9/10)|Inherit loss/custody disclosure and actual multimodal unit handling when rendering results|CC supplies no missing skill executor. Token budget and regeneration rules must cover audio/image units as well as text; no flattened counterfeit context.|

### 8.3 Proposed numbers — none measured or promised by this review

| Ruling | Source recommendation | Measurement scope |
|---|---|---|
|R41|Start500 /Grow5,000receipts per second per tenant|Sustained durable writer throughput on actual tier hardware under defined load; every image release|
|R42|10ms atP95 per receipt|Receipt latency; exact queue/commit/ack boundary still needs pinning|
|R43|Start2s /Grow1s atP95|Warm end-to-end with gates OR controlled time-to-approver-queue; not human decision time|
|R44|500ms fresh acknowledgement|P95perCC8; acknowledgement is not completed fresh work and still carries delivery estimate|
|R45|99.9% monthly per tenant|Availability of each of Rules Service, Ledger writer and credential plane|
|R46|3points for retrieval/synthesis;5for reasoning/entity-heavy on a100point rubric|Per-class quality delta; DEFAULT until first3benchmark runs establish baseline|

Current `chokepoint/llm.py:416–462` starts its latency timer after earlier gates,
so that number cannot be relabelled CC8end-to-end latency. The same call also
has no explicit seed argument and catches model-selection errors by falling
back to defaults (424–430). A benchmark must verify the **actual** model/version,
configuration and seed support, not trust the requested model name in a receipt.
No such provider/model experiment was run here.

CC7 below-floor throughput is a tier release blocker. CC13 excessive quality loss
is a release finding that may ship only with the delta and a named cause; an
unnamed cause blocks. CC placement allows an unavailable harness to be disclosed
as no measurement and forbids calling the release measured. Do not collapse
those three different consequences into one invented universal rule.

### 8.4 New decisions required in addition to §4

1. **Frozen classification and semantic uncertainty.** Solva extracts intent, but
   CC's TCB placement calls classification/routing deterministic. Specify the
   governed decision grammar, custody catalog version and unresolvable outcome.
   A learned candidate class or caller flag must not silently become authority.
   Keep pre-assembly frame commitments separate from post-draft reasoning's
   identification of the units a conclusion actually relies on.
2. **One-call unmasking precedence.** Identify authority, entity attributes allowed,
   custody class, purpose, provider/model/region, expiry and replay policy for the
   exception. Approval cannot waive source rights, secret protection, tenant
   boundary, audit receipts or unrelated entities' masks. This is a specific
   exception at the existing chokepoint, not authorization to bypass it.
3. **Local insufficiency.** Define evidence for determining that local knowledge
   is insufficient. A fixed disclaimer or an LLM confidence/self-report alone is
   not a competence measure; never guess missing knowledge. CC3 string text itself
   is not supplied verbatim and needs Content Registry registration/approval.
4. **Assembly is more than a sort key.** Pin model window/tokenizer, prompt/frame
   and output reserve, unit token/media costs, graph snapshot, distance metric,
   timestamp/source-position ordering and null/tie behavior. Same objective/set
   is insufficient to reproduce a window if any of those inputs vary. Specify
   prefix versus skip-to-fit behavior and what happens if load-bearing units alone
   exceed capacity; do not silently split or shrink the frozen unit to fit.
5. **Full warm result versus disclosed exclusions.** Document8 promises full
   synchronous warm serving while CC5allows bounded windows with loss. Define
   full at the API/artifact level versus bounded model context, so disclosure
   never disguises a missing requested unit as complete delivery. Top10exclusion
   handles means up to the number that exists, not padded invented handles.
6. **Three different taxonomies.** DQ's4quality strata, five-ring3defensibility
   classes and memory's8claim categories must remain distinct. Define adapters
   and denominators explicitly; do not sum incompatible counts or equate Clean
   with fact. This extends, rather than resolves, the earlier inference-class gap.
7. **Request-class/ratio denominator.** Controlled describes an approval phase;
   warm/fresh describe fulfilment. Specify exclusive classification per measurement
   stage, approved-controlled transitions, mixed warm/fresh requests, retries,
   refusals and zero traffic. Never improve the warm ratio by excluding inconvenient
   outcomes silently or counting a routing label as a delivered warm result.
8. **Credential cache versus immediate revocation.** Existing PRIN8 says revocation
   is immediate (`credential_plane/plane.py:167–171`); CC10refuses revocation while
   unreachable yet permits cached verification. Define maximum cache age, trusted
   signed state/epochs, expiry, emergency invalidation, trusted clocks and what
   happens if freshness cannot be established. Do not imply that an offline cache
   can know a newly revoked credential or is safe indefinitely.
9. **Rules cache and writer failover.** Signed last-verified rules need version,
   tenant scope, anti-rollback and permissible-staleness semantics. Standby writer
   needs exclusive fencing, durable head synchronization and receipted handover;
   two writers behind a health check are not sufficient. Define who can bank a
   failover event and how if the failed writer cannot write it. Missing valid
   cache or safe standby still refuses. Signing/replication are not implemented here.
10. **Bare benchmark versus sole chokepoint.** CC12calls the bare path direct and
    ungated, while existing Canon structurally forbids another production LLM
    invoker. This needs a narrowly ratified isolated experimental boundary and
    owner-approved test-data custody. **No production bypass flag, new client or
    export of controlled material is authorized by this review.** Until resolved,
    benchmark implementation remains held rather than knowingly violating Canon.
11. **Same-model comparison versus cascade attribution.** If routing chooses a
    different model, quality delta is no longer the mandated same-model pair.
    Pin pair construction and separate any end-to-end cascade comparison. Record
    actual seed support/provider version and non-determinism; a deterministic
    rubric cannot make model execution deterministic. Name causes using evidence
    or controlled comparisons, not post-hoc storytelling.
12. **Benchmark population and release semantics.** At least200tasks means at
    least400task-path outcomes, with both paths accounted for even on refusal.
    Specify class allocation, signed delta direction, reference/rubric version,
    timeouts and repeated-run aggregation. Keep references quarantined from
    training/CIF/model tuning. Resolve S35“on every release in numbers” against
    the harness-unavailable no-measurement clause, without weakening CC7's floor.

### 8.5 What remains unchanged

The original12EX/DQ decisions remain open; files18does not change their normative
rows. Existing source/approval/licence/skill/compute limitations are unchanged.
GPU/AISCA is still parked. No current operational SLO, resilient service, CC route,
benchmark score, measured warm ratio or non-builder demonstration is certified by
this document update. S34 and S35 are new promises to discharge, not completed
capabilities. Previous3uncertain semantic mappings remain uncertain.

### 8.6 Verification of this revision

`test_reports/iteration_12.json` and
`supplement_18/verification/verification_receipt_supp18.json` bank the separate
raw-source check. It reopened the actual ZIP, DOCX XML and XLSX cells, checked
extraction equality and member hashes, and inspected all23new mapped clauses and
cited source excerpts. Result: **21agree /2uncertain /0disagree**. The two are:
- **CC2:** the cited cascade and chokepoint excerpts establish integration seams,
  not an exhaustive operational trace proving every route's exception behavior.
- **R44:** the async acceptance implementation is visible, but source inspection
  alone cannot establish500msP95 or all end-to-end acknowledgement semantics.

Those uncertainties are retained; no extra opinion was used to manufacture passes.
Earlier17agree/3uncertain sample results remain historical and unchanged. Combined
semantic checking covers43of59map rows (38agree/5uncertain);16original rows remain
outside independent sampling. Review coverage is not application completion.

The raw workbook delta and composite `(Doc,Rule ID)` identities are additionally
self-rechecked before banking final hashes. No application regressions, model
calls, load tests, DB changes or new credentials were part of this task. No mocked
business/API integration was introduced. The report awaits the owner's reaction;
the proposed implementation sequence is not authorization to start it.