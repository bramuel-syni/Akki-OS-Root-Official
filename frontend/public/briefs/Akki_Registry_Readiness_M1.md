# M1 — Registry readiness: owner design, reuse and closure reconciliation

**28 September 2026 · Readiness revision 2 · No implementation or live census launched.**

## Outcome

An owner can connect and inspect the estate, commission a census through Akki,
read the complete designed report, inspect its sources and methods, understand
compute use and carry the same findings into DAP and subsequent work. Backend,
frontend, interaction and integration are one deliverable, not separate claims.

**Current result: the owner-report fidelity does not pass, and Registry is not
closed.** This is a concrete M1 implementation delta, not permission to reduce
the design or rebuild existing engines. Previously verified narrow corrections
retain their credit. The original ten milestones and 51 acceptance packs stand.

## 1. Authoritative design and demonstrated mismatch

The three new owner screenshots show the same selected Census #4 at successive
scroll positions. Their illustrative numbers are NOT current estate findings.
Browser/editor controls are not application requirements.

- Original latest source: `canon/prototypes/20260928_owner_nexus/nexus.html`.
- SHA-256: `0330a1712aad3b76dfe6f5e97207707fa35a1ed774a134313635a59ba0a67d3d`.
- Decoded owner markup: census/report lines **5804–5985**, Registry landing
  **6165–6463**, compute **6464–6787**, models **6789–7193**, sources **4908–5036**,
  Connect drawer **9325–9398**. Model report bindings: `reference_model_0.js`
  **11858–11987**; Connect transitions **6730–6929**.
- The actual application mounts `OwnerOSPage → generated/os.json → osModel /
  historyModel → OwnerMarkup`. That OS source hash is
  `a0a6df580d034cd9eef8efa7ddd130a131b1f97600c181b50002bd30846911b2`.
- `extract_nexus_reference.py:36–44` adopts newer work/board/company/Watch/drawer
  and header fragments, **not Registry**. Earlier adoption deliberately did not
  cover all applications; its proof cannot certify this newer Registry journey.
- `historyModel.js:38–49` renames all four tabs, replaces the designed three
  groups with **Inventory / Execution outcome**, substitutes the GPU fields and
  forces the no-conversation state. This is functional/semantic flattening,
  not just CSS drift or a shortage of real numbers.
- Live retained RMS `census-4` captured at 1920×800 and 390×844: all four exact
  owner tab labels and all three group headings are absent. No horizontal overflow
  was observed, **but containment is not design fidelity**. Current history also
  renders `Census #undefined` for operational results.

Live capture: `/root/.emergent/automation_output/20260928_181043/`.
Independent baseline: `/app/test_reports/iteration_55.json`.

## 2. UI/UX contract — preserve the actual experience

No new palette, typography, dashboard, simplified report, alternative Registry,
or generic notice in place of an entire designed surface. The existing owner
source is the implementation reference; archived generic design guidance is not.

| Owner element | Required preserved experience | Present delta and M1 work |
|---|---|---|
| Every census | Master/detail, selected-row treatment, run status colour, initiator, date, covered/declared source count, failure annotation, pagination and two distinct back controls | Current list omits actor/coverage, uses generic status colours, puts attempts before records and uses 8/page rather than reference 5/page. Bind real chronology, stable identity and reference behaviour; preserve historical refusals. M1.3/T4/T5. |
| Report header | Census identity, status badge, duration, initiator/date/source coverage, specific exclusion note | Do not substitute tenant for initiator or hard-code one authentication reason for every failure. Resolve actual reason and time evidence; unknown stays explicit. M1.3/T3/T4. |
| Four tabs | **Discovery Summary · GPU Spend · Conversation with Agent · Discovery Details**, in that order | Restore exact names and their full original content/behaviour, not shorter substitutes. M1.3/T4. |
| Condition of what was read | Original bar, five labelled categories, legend, percentages and stated total/population | Preserve the component and legends. Missing measurements do not justify deleting the report or inventing proportional widths. M1.3/T1/T3/T4. |
| Coverage / Condition / Readiness | All 13 rows below, explanatory copy, value and comparison columns | Current Inventory table is not an acceptable substitute. Every row needs its real evidence binding. M1.3/T1/T3/T4. |
| GPU Spend | **GPU hours, Wall time, GPUs in parallel, Sources swept**, with in-progress versus final wording | Current Utilization/Cost/Energy replacement omits required fields. Bind run-attributed telemetry; do not copy eight-GPU sample arithmetic or derive spend from SSH. M1.2/M1.3/T3/T4. |
| Conversation with Agent | Actual question, person/reply/time, acknowledgement and **How it was settled**; accurate no-pause case | `hasPause:false` and a forced empty state do not implement the designed journey. Reuse recorded response queue/decision/work events and same-run continuation. M1.3/T4/T5. |
| Discovery Details | **What it found**, sources checked, exclusions, reader and initiator; drill-through to methods/evidence | Receipt hash alone does not explain the discovery. Keep original detail composition with source/run-backed content. M1.3/T3/T4. |
| How the estate is measured | Retained provenance plus Four ways of knowing, method basis, declaration disclosure and source population | Bind selected scope consistently, not latest-run evidence on an older selected report. M1.3/T3/T4. |
| Data Connected | Four toplines; Read/Care/Mix/How disclosures; composition/rights/held-by-census views; Census intelligence rail, run card, response and history links | Full original panels remain. Use real method-bearing values, not generic replacements. Match original mutually exclusive disclosure interactions where specified. M1.3/T4. |
| Source catalogue and profiles | Data-kind grouping, overview vs source selection, condition/rights/duplication, source profile, relationships/evidence and return navigation | Current source-group row goes back to history rather than opening the real source profile. Reuse existing profile/dimensions/linkage surfaces. M1.3/T1/T4. |
| Connect | Original conversational drawer, type/method/credential custody/naming/rights/confirmation, duplicate identity, handshake diagnostics, retry and retained outcome | Current notice does not implement Connect. Bind existing descriptors/intake/governed connection services; do not run prototype success/failure simulation or mint authority from UI. M1.2/M1.3/T2/T4/T5. |
| Compute Connected | Capacity/toplines, usage disclosures, cards, job/queue/resource detail and contextual rail | Current tab cannot open this surface. Bind real admitted inventory and census use under M1; broader commercial reconciliation remains M7 without hiding its designed fields. M1.3/T4. |
| LLMs & Trained Models | Inventory, original full record, licence/approval/provenance, usage/method/refusal/custody detail and return controls | Current tab cannot open it. M1 presents real recorded capability/admission states. M4/M9 produce and qualify new capabilities; M7 owns broader accounting. Never turn “registered” into “in service”. |

### Exact 13-row measurement-to-UI map

All figures must retain tenant, source/stratum, run/version, date, method,
population, unit and full/sampled/estimated/unmeasured status in existing records.
Presentation is formatting, not a second calculation/authority store.

| Group / row | Evidence and producer requirement | Comparison / integrity requirement |
|---|---|---|
| Coverage — **Data held** | External SQL/file/object enumeration and byte measurements/manifests | Previous comparable run reference and byte delta; no constant bytes-per-row multiplier or repeated-run double count. |
| Coverage — **Sources read in full** | Frozen declared source/connection denominator and completed full row/file-header traversal | Full means full, not “at least one cluster succeeded”; show excluded names/reasons. |
| Coverage — **Share measured** | Portion directly measured in this census under its declared population | Percentage-point change on like-for-like scope; cached or sampled coverage does not become a full direct read. |
| Coverage — **Not read** | Unread/failed/skipped source regions and byte volume when independently known | An unreachable source may also have unknown size; never invent TB from a source-count fraction. |
| Condition — **Duplicates** | Existing duplication/detection candidates extended to required grades, evidence, method and source pairs | Distinguish suspected/exact/near duplicates; counts/bytes where measured; flag only, never merge/delete. |
| Condition — **Degraded** | File validity/decodability/structural and applicable media checks | Pin the check standard; no invented transcription-quality result from metadata. |
| Condition — **Incomplete records** | Required-field and actual FK-resolution checks using existing profiler/candidate graph | Candidate key names do not prove integrity or orphan counts. |
| Condition — **Stale** | Source-specific freshness timestamps and adopted stale-window definition | Preserve row/explanation; reconcile the prototype's 90-day example with supplied source rules, not an unanchored universal timer. |
| Condition — **Schema drift** | Actual structural signatures and change against a pinned prior census | Count affected sources; link actual conversation if one exists, otherwise discovery evidence. Never infer drift from chat keyword presence. |
| Readiness — **Share verified** | Independent corroboration or retained human verification evidence and coverage | Compare same basis, not quality-check pass rate. |
| Readiness — **Share carrying PII** | Existing PII detector results with assessed population | Detection share and masking enforcement are different facts. The explanatory protection claim requires the real guarded path; no inference from tenant login. |
| Readiness — **Usable today** | Actual measured, clean, non-duplicated intersection plus applicable purpose/rights limits | Do not multiply unrelated marginal percentages or claim “verified within usable” from overall verified share. |
| Readiness — **Things worth building** | Existing advisory Opportunity Briefs, grounded in this census and retained with references | Count actual supported briefs, not invented ideas or zero because the provider is unbound; stale briefs stay labelled. |

### Layout and interaction fidelity

Reference markup is the source of the actual values: head font Iowan Old Style /
Georgia; body Söhne / Helvetica Neue; source `--paper`, `--ink`, `--blue`,
`--sage`, `--brass` and severity tokens. Do not apply a generic design guide over it.
The report uses a maximum 1180px composition, 32%/divider/68% master/detail,
32px column gaps, sticky independently scrollable history, restrained 11–14px
corners, 19px report heading and compact annotated three-column metric rows.
Keep the owner's spacing, alignment, separators, exact hierarchy, hover/focus
behaviour and status distinctions. Its existing component language takes priority
over generic card-radius or font preferences.

Responsive work must adapt that same content, not drop fields or flatten the
journey. Current mobile overrides target older numeric source lines. They must be
mapped deliberately when adopting Nexus nodes, not copied blindly. Verify all
rows, all tabs, long real IDs, failure text, drawer focus/escape/return, selected
record persistence, comparison identity and list pagination. Desktop/mobile
screenshots are evidence, not a substitute for exercising the interactions.

### Keep design fidelity and measurement truth together

1. The prototype's generated percentages trend by census number; bytes and
   duplicate-file counts are arithmetic examples. GPU hours use a fixed eight
   GPUs. These **SYNTHETIC/MOCKED** formulas must not enter runtime.
2. The five UI categories are a condition display, not a replacement for the
   governed Clean/Repairable/Suspect/Junk register. Define the evidence-backed
   presentation mapping and overlap/population basis; never normalize overlapping
   condition flags by subtracting them from 100 and calling the remainder clean.
3. Full inventory/coverage rows must meet the owner's direct-reading meaning.
   Where Canon allows sampled deeper measurements, disclose those in the original
   methodology/detail experience; do not silently label them full or water down
   “Sources read in full”. Full estate census and event-driven regional refresh
   remain distinct operations with truthful scope.
4. Preserve genuine explanatory copy; bind claims about current measurements,
   people, rights and protection to actual evidence. Any material source-policy
   conflict is explicitly reconciled against supplied rulings, not silently
   rewritten as a weaker product promise.
5. Prototype-only preview outcome shortcuts/editor knobs are not production
   commands. Removing simulated success is not permission to remove the real
   failure, approval, recovery or conversation experience they illustrate.

## 3. Reuse findings — the work is connection and completion

Paths below are relative to `backend/vendored/extraction_akki/backend/services/`.

| Existing implementation | Reuse and exact remaining delta |
|---|---|
| `census_autonomy/operational_runner`, store, scope, reads, dispatchers | Existing queue/run lifecycle and scoped readers remain. Move RDS/OBS reads off E1, qualify worker identity/source custody, support file/object drivers, carry connection-level coverage. A local subprocess is still E1. |
| `census_canon/estate_enumerator`, classifier, `stratum_measurement`, `activation_list`, contracts | Region/feed/sensitivity, method/unmeasured and observed/dormant carriers exist. Wire actual enumeration/measurements, not placeholder targets or a new census engine. |
| `audio_poc/recording_inventory`, transcript inventory, pairing/gaps and read guards | Real parsers/canonical keys/snapshot helpers exist; guard is call-shape-only. Actual NAS layout/access belongs on external worker. Preserve rejected/unparseable paths and key collisions in coverage instead of silently dropping them. |
| `census_canon/audio_inventory_supplement` | Explicitly registers two unenumerated placeholders; not proof that NAS/OBS was scanned. Use this lineage rather than duplicating identities. |
| `mtafiti/composition_census`, `quality_profiler`, samplers, `relationship_signals`, PII detectors | Reuse probes/profiles; name-based FK candidates are not resolved relationships. Complete applicable actual checks and all four ruled linkage types. |
| `mtafiti/declaration`, standing, inference, measure, verdict, overlay, registry | Two-layer composition and conservative baseline already exist. Wire lawful feed declarations/current sources; preserve closed overlay until qualified. Existing raw-pointer hash fallback is not proof of real schema change; supply measured structure. |
| `census_canon/registry_write`, `mtafiti/registry`, asset writer, result adapter/projection | Deterministic supersession writer and Mongo registry both exist. Reconcile authoritative roles through current contracts, not a fifth Registry. Asset writer conflicting overwrite remains a defect. Qualify durable custody/all consumers and source-record lineage, not only receipt registration. |
| `non_gpu_governance/quality` | Existing pack/bitmap/stratum/population reconciliation is a **consumer**, not a profiler. Bind external check results and complete garbage-register evidence. Its 500-record metadata bound requires estate-scale chunk/aggregate integration, not a claim that a large estate was assessed. |
| `opportunity_briefs` selector/generator/grounding/registry | Advisory and quantitative-grounding machinery exists. Bind actual Registry reads and qualified source-local/provider boundary; do not compute estate aggregates in synthesis or create another brief service. |
| `census_dq_producer` / response-required queue | Failed-host item producer exists. Complete scoped queue read, exact displayed cause, authorised response and same-run/recovery linkage. It is not the deep data-quality profiler. |
| Current owner renderer, markup extraction, session and DAP models | Reuse composition and actual scoped census API. Adopt complete Registry reference and bind fields/interactions; don't mount orphan `Registry.jsx` or resurrect old mock hydrators merely to fill panels. |

## 4. Historical gap reconciliation — closed is closed, at its proven scope

Primary prior audit: `notes/REGISTRY_MODULE_AUDIT_20260925.md`, D1–D11.
“Closed exposure” means the old misleading path is no longer reachable; it does
**not** mean its promised functionality is delivered. These two facts are tracked
separately. Original audit/report files remain unchanged as historical evidence.

| Prior ID | Current disposition and evidence | Remaining M1 task, if any |
|---|---|---|
| D1 — shape-only COMPLETE | **Closed for rejected legacy success / current route replacement.** Existing operational runner and output validation are active; prior unverified completions not promoted. | Real complete deep execution and partial-connection honesty still open, M1.2–4/T1/T2/T3/T5. Do not rebuild the runner. |
| D2 — fabricated landing values | **Closed exposure:** unsafe legacy hydrator quarantined; current owner reads scoped evidence/unknowns. | Deep condition/composition values and full designed report still open, M1.3/T1/T4. |
| D3 — fictional DAP figures | **Closed on current routes:** old DAPLanding/DataEstates are not mounted; current OwnerDAPLayout/dapModel uses scoped records. Independently rechecked. | Preserve this correction. Broader source profiles remain incomplete; don't reopen fabrication without a reproducer. |
| D4 — census4 / NAS hidden | **Partial closure:** census4 list/detail/latest supported and dynamically retained operational records appear. | NAS deep source registration and its condition evidence still open, M1.2/M1.3. |
| D5 — compact timestamp breaks reads | **Closed for current scoped projection:** historical census4 displays dated evidence and APIs pass. | Historical unsafe parser remains quarantined; run-duration and selected-record UI binding are distinct open work, not a rollback of date correction. |
| D6 — asset writer overwrite | **Open:** same `asset_ref` assignment still replaces prior value. | Reuse existing version/supersession/collision contract; prove duplicate idempotency and conflicting content refusal, M1.3/T4/T5. |
| D7 — NAS fresh ID on restart | **Closed exposure by quarantine**, not a repaired historical hydrator. | Actual NAS source identity must be deterministic on current worker/publication path, M1.2/M1.3/T5. |
| D8 — nonexistent collections / salted ring hash | **Closed exposure by quarantine** of the old what-you-hold reader. | One durable source account/all-consumer joins still open, M1.3/T4/T5. Do not assert current collection counts from the old audit. |
| D9 — no frontend consumer / orphan Registry | **Partial closure:** actual owner frontend consumes current census overview/projection; orphan component is not the required architecture. | Full latest-owner Registry bindings still open, M1.3/T4. Wiring means full experience, not merely one GET. |
| D10 — unauthenticated stale facts | **Closed for current route:** authenticated `/api/registry/facts` returns scoped overview **200**, anonymous denied. It is NOT blanket 409. | Preserve as regression; do not replace with old facts assembler. |
| D11 — sensitivity never computed | **Open operational integration:** deterministic classifier exists and is used by older census-canon enumerator; active aggregate publication does not deliver the single classification to consumers. | Wire declarations, actual source measurement and entitlement's same attribute, M1.3/T2/T3/T4. Do not build another classifier. |

### Earlier census-spec gaps (15 September) also remain accounted for

`CENSUS_SPEC_AS_DESIGNED_20260915.md` §F listed eleven gaps; its “Docs 9–10 absent”
note is **superseded**: both full source texts were recovered on 26 September and
read in this readiness pass. Do not request them again.

| Earlier gap | Current reuse/closure position |
|---|---|
| Feed identity; region; sensitivity (three gaps) | Canon source candidate/enumerator/classifier carriers now exist. Active source publication remains partial; not missing foundational classes. |
| Explicit unmeasured | Contract + stratum union exist; current metadata nulls have explicit limitations. Narrow honesty correction retained; full 13-row presentation and deep measures remain open. |
| Per-figure method/run/date/population/full-vs-sampled | `canon_census_measurement.Measurement` already carries these. Connect through worker, durable record and every designed figure; a report-level SHA alone is insufficient. |
| Registry write-back | Canon source writer and operational RECEIPT registration exist. Complete durable source characterisation and all-reader joins; do not call a notes report or receipt asset the whole Registry. |
| Generic JobManifest rather than audio-only tool | Case-agnostic enumerator and operational descriptor/commission exist. Bind original descriptor schemas, actual drivers and recovery to this spine; do not create another job engine. |
| Class activation | `activation_list.compute_activation_list` exists. Wire real observed classes and retained downstream handoff; prototype model roster is not activated capability. |
| Structural-delta freshness | `mtafiti.registry.detect_stale_records` exists. Feed actual structural signatures and connect scoped refresh/retraction; timestamp/raw-pointer fallbacks are not schema evidence. |
| Two-layer measure | Existing declaration/measure/verdict/overlay modules and Mongo composition exist. Operational binding remains open; no new measure engine. |
| Connector completeness | Failed-host producer and per-connection details exist. Public full/partial coverage and response action still need integration. |

### Closure rule — “once done, done”

For each specific gap preserve its original ID, affected scope/version, source
requirement, producer → writer → consumer link, real/fixture evidence distinction,
acceptance result and residual work. A closed correction remains closed unless
there is a **specific reproduced regression, invalidated evidence, or an explicit
new requirement/version change**. A newer prototype is a named delta, not a reason
to throw away working code. No automatic expiry, arbitrary timer or recurring
whole-module audit. M1 closes only when its full pinned outcome passes; later
milestones rerun affected regressions, not reopen Registry as unfinished by default.

## 5. Implementation work within the existing M1 sequence

1. **M1.1 readiness:** this report captures design, current bindings, source
   requirements and prior-gap dispositions. Carry the field/interaction map and
   exact remaining code reads into the work record; retain existing descriptors,
   authority and selected-card identity. No additional audit milestone.
2. **M1.2 external execution:** bind existing connectors/read guards and both
   worker classes; implement missing adapter effects only after reviewing their
   candidates. No E1 source reads, no generic local subprocess fallback, no
   fabricated worker provenance. NAS access is proved externally.
3. **M1.3 integrated Registry:** implement source-level deep measurement,
   defensibility/sensitivity/quality/relationships/opportunities and durable
   publication **together with the exact owner frontend and interactions**.
   Every required field/control has its producer/evidence/command mapping.
   Current unknown states keep the full design; they are not a completed M1.
4. **M1.4 acceptance/repair:** run existing M1-T1–T5 through ordinary user paths,
   including both worker classes, source completeness, selected history,
   comparisons, response/recovery, source detail, Compute/DAP consistency,
   restart, mutation exclusion and tenant isolation. Owner-design comparisons
   and interaction checks are part of T4, not a post-completion cosmetic phase.

Required visible states: actual running/progress, completed with complete
measurement coverage, partial/needs attention with exact exclusions, blocked,
no genuine prior comparison, genuine measured zero, unmeasured, stale, operator
response, same-run continuation and immutable historical result. Use actual
state evidence; never fabricate new runs just to fill these cases in production.

**Pinned acceptance distinctions:** M1 owns current Registry/source/compute/model
inventory and required read journeys. New model capability evaluation is M4/M9;
full commercial reconciliation is M7; whole-site restore is M8. Their designed
surfaces and existing state must not disappear, and their deferred capabilities
must not be represented as M1 achievements. Those ownership boundaries are not
an excuse to omit Registry integration or claim complete product readiness.

## 6. Verification and read limits

- Original latest prototype hash preserved; generated Registry source mismatch
  and field substitutions traced directly. Three owner screenshots transcribed
  and compared against source, not inferred redesigns.
- Live owner report desktop/mobile: **fidelity FAIL**, overflow checks empty.
- Scoped API regression: **16 passed**; offline contract regression **24 passed,
  SYNTHETIC/MOCKED**. These prove only those cases, not backend deep-census
  readiness or production modality support. Do not use the testing report's
  arbitrary frontend/backend percentages as delivery scores.
- Original D1–D11 dispositions and all eleven older field-gap entries reconciled.
  All **22 Doc-9/Doc-10 requirement rows**, **15 DQ rows** and **3 trust-domain rows**
  receive explicit scope/status in the companion clause map; this is coverage,
  not forty closed requirements.
- Full text of Docs 9/10, relevant owner Registry/source/report/compute/model/
  Connect markup, report/connection reference transitions and current model /
  renderer/style bindings were read. Backend reuse was traced in the modules
  named above, with explicit new deep reads of canonical writers/carriers,
  enumerator, classifier, activation, audio inventory/guard, two-layer composition,
  relationship scaffold, quality consumer and brief generator.
- Remaining targeted reads before changing their work: full dependency/test
  branches of perception and all four linkage implementations; complete source
  profile/compute/model-detail binding builders, opportunity provider/tenancy
  boundaries, descriptor admission schemas, and retained ruling reconciliation.
  Those are named M1 work-package preparation tasks, **not claims of absent code**.
  No assertion that every M1 transitive file, all linked repositories or the
  whole programme has now been read line-by-line.
- No runtime/UI/auth/config/credential change, no source/GPU call, no census
  commission, no new authority or prototype execution. Known runtime and design
  defects are recorded for the requested subsequent implementation, not claimed
  fixed. All live milestone gates remain **NOT RUN / NOT PASSED**.

Companion: [Requirement and shared-dependency map](Akki_Registry_Clause_Map_M1.md).
Governing plan: [Akki works roadmap](Akki_Goal_Roadmap_v1.md).