# Enhancement-spec ingestion and all-component integration review

**Scope:** owner asked to ingest `files (17).zip`, give thoughts, and map integration
across **all affected components**. This is analysis and custody banking only:
no application/Canon source edits, database writes, rule ratification, provider
calls, source-data reads, migrations, or GPU troubleshooting.

## 1. What was received and what changed

Four archive members, not17: Execution Standard v1; Data Cleanliness v1; Security
Assurance Promise Set; Master Requirements Registry. Immutable bytes and hashes:
`custody/owner_drops/enhancement_specs_20260926/`; full ordered/cell-addressed
extracts and manifest alongside this report. DOCX text extraction includes tables;
paragraphs without a style are retained. No tracked insertion/deletion content
was found by the extractor; workbook formulas were not executed.

- **Execution:** EX-1..EX-15: denominator-first task contracts, per-member outcomes,
  protected acceptance, shortcut detection, independent seeded re-performance,
  and evidence-bound completion claims. Covers runtime AND engineering/audit work.
- **Cleanliness:** DQ-1..DQ-15: seven check families, four strata, source/version
  register, deterministic repairs, training and factual-answer exclusions. DQ-8
  extends families1/4/6 to media; it is not an eighth separate check family.
- **Five rulings:** R-36/37 for execution verification; R-38/39/40 for sentinels,
  duplicate tolerances and media thresholds. R-37 is OWNER, not DEFAULT-class.
- **S-34 is the newly added assurance promise. S-33 is retained Content Registry,**
  not a new Execution Standard promise. Compared with the hash-verified20Sep v6,
  S1–S33 row contents are unchanged and none removed.
- EX/DQ rule statuses in the incoming workbook are **PROPOSED**. The Execution
  document says SO§7 binds from next objective-card pin after banking; this review
  exposes that authority/status difference rather than silently promoting rows.
  No new build card was pinned here. Existing DAP work is not retroactively
  labelled EX-compliant just because its tests passed.

### Deterministic registry reconciliation

| Item | Directly counted |
|---|---:|
| System Rules Registry data rows / unique `(Doc,Rule ID)` keys |632 /632|
| QA Verification data rows |602|
| Registry keys missing from QA |30: exactly15EX +15DQ|
| Build Status stated total |619, with no derivation reconciling it to632 in that sheet|
| Registry Legend stated count |286; inherited note not a current denominator|
| Objectives sheet |O1–O12 plus a cross-cutting note; no O21/O22 entries|

The available20Sep v4 baseline was re-fetched via its prior custody URL and matched
SHA `72160287…ad588` exactly. Against that595-row baseline:37additions,0removals,
2changed rule rows. The37 are7SFP rows (stamped20Sep(c)) plus30EX/DQ rows. Do not
pretend all37 originated in the26Sep design change. A602-row v5 is cited by code
but its workbook bytes were not located for direct comparison in this pass.

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

**Strong direction; integrate as two cross-cutting capabilities, not another
standalone portal or parallel registry.**

Execution Standard answers: *Did this task account for the population it promised
to handle, and can another executor verify that?* Data Cleanliness answers: *Which
named checks did each record pass, and is that record admissible for this use?*

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
       ├─ Solva unit eligibility / assertion-class ceiling / output gate
       └─ Content Registry dependencies → original OS/DAP prototype bindings
  → Ledger: hash-bound receipts and decisions; Mkondo: governed handoff refs
```

Use versioned payload/sidecar references around existing frozen contracts. Do not
add fields ad hoc to the17-field Ledger row, silently change sealed signatures,
create a second Mtafiti writer, or create a free-standing entitlement store.

## 3. Impact across18 component groups

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

Universal EX scope also applies to future/less-exercised surfaces: their task
inputs must be enumerated when their build/runtime cards open. The18 groups are
an integration-impact organization, not a denominator of all platform files or
an assertion that every historic route has been audited.

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
accounts for36review items; that is review coverage, **not36implemented features**
or a platform-completion percentage.

## 7. Evidence index

- `DOCUMENT_MANIFEST.json`:4incoming files and source hashes.
- Full ordered DOCX `.md`/`.json` and workbook `.json` extracts: block and sheet-row citations.
- `REGISTRY_RECONCILIATION.json`: direct counts,30missing QA keys, exact baseline diff.
- `CLAUSE_IMPACT.csv`:36rows =15EX+15DQ+5rulings+S34, with evidence and integration ownership.
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