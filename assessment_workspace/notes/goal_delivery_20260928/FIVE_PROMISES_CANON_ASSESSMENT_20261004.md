# Five product promises — canon, implementation, and evidence assessment

Date: 4 October 2026. Read-only product/architecture/engineering assessment, not security certification, code implementation or authority to train.

## Owner scope

Owner asks how far Akki is from these five promises, with percentage status:
1. Govern and securely train models of different dimensions using integrated enterprise or uploaded external data.
2. Foundational Context-as-a-Service platform: estate licensing without moving data, marketing models/skills, content mining/creation, media planning, campaign strategy and further applications.
3. Background choice of the right model/agent to manage delivery; maker-chat-quality experience or better; exceptional decks/reports/whitepapers/board artifacts/briefs at a fraction of cost.
4. Agent Resource Management Interface (ARMI): profiles, purpose/JD, abilities/limits, admission/compliance/risk, resources, behaviour, completed work, collaboration and revenue/productivity contribution for admitted agents, models and skills.
5. User control through Shield (SyniSense + Solva): governed confidentiality by name AND context, PII removal and reconstruction without disclosing privileged originals, using capable permitted models.

Clarifications confirmed by owner: model dimensions means BOTH sizes/architectures and task/modalities. Shield mode is B: external frontier models may receive only approved de-identified/reconstructed context; privileged originals remain inside. Owner requested rigorous review of canon and identification of requirements needed but not originally prescribed, holistically and without flattening or overengineering.

This clarifies product intent, not an instruction to change model providers, alter policy, start training, unpause other work, or change the fixed HTML prototype. Existing scoped admissions, pauses and deferrals remain intact. Particular policy tensions below require explicit reconciliation before implementation.

## Method and headline

These are rounded, outcome-based engineering estimates, not a percentage count of all canon clauses, validated probabilities, security guarantees, remaining-effort estimates or fresh milestone acceptance. Each promise has five equally weighted delivery blocks, scored 0/25/50/75/100:
- 0: not found as an implemented product capability.
- 25: design, isolated foundation or visibly held workflow.
- 50: connected but materially incomplete/narrowly supported.
- 75: useful real slice with material breadth/assurance still outstanding.
- 100: the agreed full outcome independently verified, including ordinary user operation.

Scoring and block placement are engineering judgment. Read within roughly ten percentage points, not as statistical intervals. A critical custody/authority gap blocks a corresponding claim regardless of averaged score. No 100% promise is awarded.

| Promise | Five delivery-block scores | Estimate |
|---|---|---:|
| P1 training | Existing enterprise training 75; external-upload path 50; general architectures/modalities 25; autonomous lifecycle 50; generalized independent admission and delivery 50 | 50% |
| P2 CaaS | Estate intelligence 75; scoped context/application serving 50; rights/party licensing 50; operational billing/delivery 25; repeatable domain-product proof 25 | 45% |
| P3 right model + excellent affordable delivery | Office artifact production 75; context/chat UX 50; role/model selection 50; managed order lifecycle 50; comparative quality/economics 25 | 50% |
| P4 ARMI | Identity/mandate foundations 75; unified workforce profile 25; work/cost/admission evidence 50; operational assignment/lifecycle surface 25; defensible individual business attribution 0 | 35% |
| P5 Shield control | PII crossing/restoration 75; authored declaration lifecycle 25; semantic secrecy/intent preservation 25; universal payload/perimeter enforcement assurance 50; independent privacy/utility proof 25 | 40% |

Equal-weight headline 44%, communicate **roughly 45% of the full customer promise set**. This is NOT overall codebase completion. The previous ~85% M1/M6 figures concerned narrower workstreams; earlier M8/M9 completion explicitly concerned reduced agreed scopes. Higher primitive maturity and lower end-to-end product delivery coexist.

## Canon trace and current evidence

### P1 — Governed general training, 50%

**Already prescribed:** numbered requirements Doc13 #22/#23, A5.1/A5.5, B5.1–5.5; Doc14 model ecosystem; architectural Canon4 training/recipe discipline; later Doc17–20 general training supplements and current owner rulings. Qualified, deduplicated, rights-clean material, registered licensed bases, objective/budget freeze, held-out evaluation, regression bounds, calibration, lineage and six-criterion automatic acceptance are NOT new requests.

**Scope precision:** original “any output dimension” means a measurable output/done-condition, not a promise that every proprietary or arbitrary architecture is trainable. Canon prescribes bounded adapters on registered bases, not unrestricted base-weight rewriting. Different sizes/architectures are valid target coverage when adapters, licensing, hardware and validation exist; maintain an explicit admitted support matrix. Do not silently add foundation pretraining or assume closed frontier model weights can be trained.

**Working evidence:** real historical text and specialist audio training; signed reinforcement/autopilot; model registry/admission/rejection evidence; private uploads with checksums, quota, rights metadata and access revocation. `/api/media/config` shows storage_ready=true and 11 supported extensions (audio/text/labels/CSV/JSON), not image/video training intake. Four current uploaded-file assessments return complete assessment records but `held_before_retraining`, `training_started=false`.

**Gaps:** `services/media_library/assessment.py:1–23` is metadata readiness, not trainable-data preparation. General `training_lab/skill/scripts/backend.py::RealBackend` explicitly raises NotImplementedError. Specialist runs must not be erased by that fact; they are real independent adapters. Thirteen-language work is not merely waiting on signature (previous assessment records class/data/reporting issues). Required generic lifecycle is upload/estate selection → qualification → admitted recipe → controlled execution → independent six-criterion acceptance → scope-correct service/export. Existing Wanga-only admission-to-estate-consumer mismatch remains open. Model safety, released artifact privacy and byte/cost custody must be evidenced per supported task, not inherited by naming it training.

**Done test:** complete that lifecycle on both estate and uploaded material for each explicitly advertised task/architecture family; demonstrate rejection, budget/stop/retry, withdrawal and regression behavior. All modalities are a roadmap coverage requirement, not all necessary in first release.

### P2 — CaaS foundation, 45%

**Already prescribed:** Canon7 §§3–27 (answering, async, governed fetch, application-key memory planes, writeback/publication, revocation), §§28–33 (reference and buyer apps); DAP profiles 6–11 and metering/terms 21–29; Doc18 contribution/skill contracts; Docs9/10 estate intelligence. These describe a reusable governed context plane, not a handful of internal chat screens.

**Working:** estate intelligence and reports; principal/tenant/licence/terms foundations; context/memory/provenance metadata contracts and guarded execution; specific extraction and delivery evidence.

**Gaps:** complete third-party onboarding/key-scoped memory/use/withdrawal journey; working entitled, metered client delivery across the relevant DAP profiles; repeatable domain outputs and business validation. Current principal billing for 2026-10 resolves but has zero lines and no financial invoice—does not prove that no other user ever consumed anything, but it does not establish a working nonempty commercial cycle. Skills/strategy/app integration surfaces remain held or incomplete. A census opportunity estimate is not a customer product or proof of revenue.

**Meaning of no-data-movement:** source/raw data remains under estate custody, training compute is brought to the estate, permitted derived/de-identified context leaves only through its appropriate gate. Internal staging on authorized estate compute is not the same as selling/copying the raw estate to a customer. Authorized raw downloads and weight/skill egress are separate profiles, not disguised CaaS queries. Do not promise literally zero byte movement while offering external context inference.

**Done test:** one external application commissions a scoped licensed context product, consumes it, receives source-linked output, has measured usage billed, and loses future access/derived memory when rights are withdrawn. Domain packs reuse that contract; do not implement a new core for every opportunity.

### P3 — Best-suited agent/model, excellent output, lower cost, 50%

**Already prescribed:** Doc11 A5.1–5.4 and LC2 B2.1–2.3 require the lowest-cost sufficient rung based on measured task-class performance, inspectable selection and honest savings; Canon4 Solva; Doc15 B path-of-success; Canon7 publication/review; Doc18 context-window discipline. “Newest/largest” is not the selector. Correct interpretation of “best”: best permitted candidate for the task's quality, confidentiality, latency and budget constraints; cheap cannot weaken correctness.

**Working:** real Office reports, QA/revision/download workflows; multi-turn context and role assignments for planner/writer/reviewer, with distinct model families. `chokepoint/model_roles.py` describes JDs and strengths.

**Evidence limitation:** the same module's EVALUATION explicitly says assignments use catalog/published benchmark evidence and no independent head-to-head comparison on owner data has been run. This is useful configuration, not a measured universal selector. Catalog entitlement preference in `cascade_selector.py` is access-class routing, not task-quality selection. Existing 200-task chat checks scored 161/200, but do not directly judge factual/creative output quality or meet the full two-path comparison requirement.

**Cost evidence:** current Cost Ledger has 26,024 historical calls, partial cost=true, one model-rate entry and zero GPU-rate entries; all five savings levers report zero attributed calls. Do not infer total spend or observed savings from the small partial USD sum. Token metering can use approximate counters and does not yet represent full all-in delivery economics.

**Gaps:** measured candidates per task, permitted fallbacks/rechecks, complete objective→handoff→accepted-result orchestration across advertised work, publish-gate treatment of independent reviewer disagreement, matched blind quality comparison and all-in accepted-output cost (including retries/review/human edits/storage/compute). “Some of the best” and “fraction of the cost” remain unsubstantiated, not disproved.

**Done test:** fixed representative briefs, matched evidence, blind accepted-output scoring against named alternatives, measured latency and all-in cost; successful ordinary-user commission/revision/retrieval. External maker websites bundle tools/memory/workflow beyond the model API—API access alone is not product parity.

### P4 — ARMI, 35%

**Already prescribed:** Canon3 §6.1 declarations (objective, capability, risks); Canon8 W9 admitted mandates, W11 task identity; Canon9 one record/writer and typed handoffs; Principal Model PRIN1–4; model/skill registries, lineage, costs and task history. Do not characterize agent governance as absent just because the ARMI console is incomplete.

**Working:** immutable organisation/person/agent principal types, admitted scope, behavior-signature state, some model/skill/run records, role JDs/strength descriptions and task/receipt machinery.

**Not delivered:** an integrated agent workforce profile and workflow joining these to owner, mandate/JD, model/skill versions, admissible actions, task performance, resources, collaborators and business outcomes. The compute-resource registry is NOT ARMI; it holds resource identifiers/classes/tags and is process-scoped. `/os/build/youragents` was verified at desktop/mobile: “Your Agents is not available yet. No work has been started.” Actual active `OwnerDeferredWorkspace` maps an empty agentsListView; the old unused page is not the only evidence.

**Important canon conflict:** Canon8 §3 and W13 forbid using Watch behavioral-profile internals for analytics/scoring/pricing/management visibility. They are non-exportable, not a ready-made HR profile. ARMI can hold declared operational capability, task telemetry and authorized admission/incident assurance, but cannot feed or expose protected Watch profiles to score productivity or commercial value. Separate operational performance from security signals; no new shadow security store. A displayable “malicious conduct probability” requires a separately specified lawful/authorized calibrated risk measure, not renaming a Watch signal or LLM guess. Current source `watch/input_seat.score_input_seat` returns low/pass placeholders, not probabilities.

**Additional scope boundary:** a record naming an external agent does not contain its external tools/runtime. Arbitrary third-party execution requires a real mediated tool/runtime boundary and per-deployment evidence (Agent Containment LIM4); do not imply this chat's builder is an admitted product agent solely from its name.

**Done test:** onboard one actual agent, bind its model/skills, assign one governed objective, prove allowed/blocked actions, finish work, surface evidence-backed performance/cost and contribution, then suspend/revoke it with effect. Build a projection over existing records, not a replacement authority.

### P5 — Shield and contextual confidentiality, 40%

**Already prescribed, explicitly:** numbered Doc1 A5.1–5.8 single invocation/custody/network boundary and B5.1–5.5 intent before redaction; Doc2 A3 exact/pattern/category, A4 Generate→Review→Edit→Adopt→Approve, A5 governed addition/removal and one live entity set; Doc2 B5 independent question/data assessment and re-association/joint disclosure check; Context and Capability CC1–5 distinction between entity protection and useful entity knowledge. Semantic categories were never “new scope”.

**Working:** sole current LLM invocation function, de-identification using regex + tenant dictionary + local NER, restoration, purpose/masking/endpoint checks, receipts, preview and several refuse paths. Returned originals are for an entitled internal consumer, not the external provider. This is meaningful foundational work, not an empty Shield.

**Concrete gaps:**
- `chokepoint/dry_run.py:110–122` explicitly implements category preview by literal category name in receipt metadata, NOT a reasoning recognizer. Fresh pure helper check: literal `unreleased_pricing` matched, a synthetic paraphrase of confidential launch pricing did not. This is a narrow implementation check, not a measured leakage rate or a live disclosure.
- `synisense/shield/tenant_entities.py` reads a catalogue limited to presenters, stations, programmes and advertisers. It is not the prescribed DPO-authored live exact/pattern/category declaration workflow.
- Current `deidentifier.deidentify` does not invoke a general semantic secrecy recognizer. Names/PII redacted from a contract do not remove the trade-secret method in its clauses.
- Current `llm.invoke` de-identifies a prompt string; its separate system_message is passed directly to client construction. Canon's per-file independent question/data custody and all-payload coverage cannot be inferred from single-prompt masking. Assess actual callers, tool results, memory, attachments and system-message policies before claiming universal coverage. No exploitation/external secret payload was sent.
- The wired `watch/input_seat.score_input_seat` accepts metadata, not payload text, and returns `hostility='low', verdict='pass'` while its docstring identifies a placeholder. This is an incomplete detector in the current route, not evidence all Watch mechanisms are fictitious. An observable receipt is not content-threat detection.
- No fresh network/SDK bypass or privacy/utility certification was run. Allowlist declarations do not alone prove infrastructure enforcement. Current API admits t1_full_mask only in development; t2_partial/t3_category have no admitted environments. Normal governed-text tiers are admitted; do NOT generalise row-tier status to all model use.
- PII recognition currently uses an English NER model; wider language capability needs its own tested coverage, not borrowed from the LID task.

**Mode B architecture:** read sensitive originals and infer secrecy/intent INSIDE the trusted boundary; construct/minimize and verify the safe context; only then invoke the external frontier model; verify and restore only for an entitled recipient. Never send raw protected content to an external model in order to decide what should have been masked. The semantic detector may be advanced, but it does not own policy/approval authority. Upgrading the generator alone does not add semantic confidentiality.

**Existing-policy tension:** CC1 and the owner-approved `activation/crossing.py` allow separately authorized entity-knowledge unmasked exceptions through the same crossing. Owner's present Mode B clarification is the intended promise/default, not an automatic implementation of policy retirement. Decide explicitly whether that exceptional product mode is disabled or clearly disclosed; do not silently weaken either canon or the new no-privileged-egress promise.

**Done test:** approved declarations across exact values, patterns and contextual categories; multilingual paraphrases, attachments, memory/tool paths, joint disclosure and prompt-injection cases; demonstrate no protected spans reach the external request and useful meaning survives, including unknown/ambiguous cases refusing safely. Scoped independent evidence cannot prove universally zero future leaks.

## What is NOT new scope

1. Semantic confidentiality, pre-redaction intent preservation, dual-file/joint disclosure checks and governed declaration removal.
2. One invocation boundary, governed raw/media paths, durable provable receipts, physical outbound control and independent assurance.
3. Qualified training data, independent six-criterion model acceptance, regression/no-speaker constraints where applicable, rights lineage and scoped serving.
4. Measured task-class routing and honest cost savings; quoted costs before commissioned compute; admission recheck on changes.
5. External application identity/scope, key-specific governed memory, async retrieval, metering, revocation and failure behavior.
6. Operational objective, actor identity, capability/mandate declarations and ordinary task/resource history.

Unfinished or unproven original requirements must not be rebadged as new enhancements. Conversely, a proposed draft clause is not automatically an adopted requirement; later owner rulings and declared scope govern. This assessment does not silently ratify old proposals.

## Smallest required additions/refinements to the product contract

These are recommendations, not new adopted policy or implementation authority. “Not found” is scoped to the canon, supplements and sources reviewed, not a claim every historic document in the repository was exhaustively searched.

| ID | Requirement | Origin/status | Lean implementation boundary |
|---|---|---|---|
| N1 | Unified ARMI operational profile and lifecycle: owner/JD/objective, agent→model-version→skill-version dependencies, admission scope, operational task/cost/performance and collaborator links | New product composition; underlying identities/records already prescribed | Read projection over existing registries/Ledger. Models, agents and skills retain distinct types; no duplicate authority or evidence store |
| N2 | Defined displayable assurance/score contract: numerator, denominator, scope, task/dataset, time window, evidence, uncertainty/expiry and unknown | New specificity for requested compliance/admission/malicious-probability profile; evidence honesty already canon | Admission stays scoped pass/hold/reject; use incidents/assurance facts. No invented malicious probability; new allowed risk measure needs explicit authority and calibration, not Watch internals |
| N3 | Business-outcome attribution: claimed vs verified outcome, baseline, human effort/rework, incremental value, collaborator credit and no double counting | New detailed per-agent revenue/productivity attribution; broad value accounting already canon | Start with measured accepted work and time/cost; scenario estimates separate. Revenue contribution is not automatically causal revenue lift |
| N4 | A small named set of sellable domain-task contracts (e.g. content mining, media planning, campaign strategy) with required inputs, permitted actions, output schemas, acceptance checks and commercial unit | Product-specific domain detail not found in base canon; generic applications/skills/licensing already prescribed | Versioned skill/workflow bundles on common execution/context APIs; do not build a marketing suite, media-buying engine or connectors without demonstrated need |
| N5 | Explicit comparator contract for the stronger claims “better than maker chat” and “fraction of cost”: named comparators, same briefs/evidence, quality bar and total accepted-output cost | Sharpening beyond generic original performance/economics measurement, not a new measurement engine | Reuse existing evaluations and Cost Ledger; calibrate with blind human acceptance and real rate coverage. Publish measured result by task, not universal superiority |

Other necessary **clarifications**, not new engines: admitted architecture/modality coverage and external-boundary definition; handling of CC1 exceptions under Mode B; role-safe separation of ARMI operational profiles from Watch security internals. Do not add a framework merely to encode a decision.

## Minimal architecture and order

One reusable loop: **Objective → authorized context → eligible model/agent/skill → governed execution → independent checks → authorized delivery → cost and outcome record.** Preserve Northena, Mkondo, SyniSense/Solva, existing registries and Ledger as owners. ARMI and domain products consume that loop. Preserve separate security authority and deterministic approval/decision responsibilities. Keep UI under v2_os.html; no new decorative executive dashboard or sixth governance layer.

P0: finish contextual confidentiality/control and reconcile all-payload/detector/serving claims; identify admitted model/task coverage and scope-correct consumers. Do not begin 13-class training on a promise that names alone made the preparation path general.

P1: complete the generic upload/estate→trained-model lifecycle; one licensed external CaaS customer journey; one high-value document/media-strategy order with measured routing/quality/cost; one operational ARMI profile and assignment path. Reuse those as five end-to-end acceptance demonstrations, including denial/withdrawal/failure.

P2/owner choices retained: M5 collaboration pause, M8 site restoration/real notifications deferrals, optional additional modalities/domain bundles. They are not quietly unpaused by this assessment. No calendar/effort estimate is warranted from completeness percentages alone.

## Verification and limits

- Direct reads: original architectural Canons1/3/4/7/8/9, relevant Canon5 sections, numbered requirements Docs1/2/10/11/13/14/15 and cross-cutting anchors, DAP, Principal and Agent Containment specs, Context and Capability supplement, owner decision register, current PRD and prior assessment. Status distinctions/ruling conflicts preserved. Not a complete repo-wide security audit or reread of every canon paragraph.
- Current implementation inspection includes active server routes, active frontend routes, training/media, authority/entitlements, model-role selection, cost accounting, Shield invocation/deidentifier/tenant catalogue/preview and input-seat detector.
- Existing tests: `test_native_quality_context.py`, `test_execution_component_authority_red.py`, `test_estate_forecast.py`: **22 passed**, no skips, one dependency deprecation warning. Governance tests use **MOCKED/SYNTHETIC** fixtures; they prove component contracts, not production acceptance or model performance.
- Authenticated preview reads: media config/assessments, M9 capabilities, principal period billing, cost rates/summary, Shield allowlists all 200. No GPU/model dispatch or new external-data retrieval.
- Actual Agents screen observed at 1920×800 and 390×844; its unavailable state is visible. Browser logs `/root/.emergent/automation_output/20261004_062424/console_20261004_062424.log`.
- Pure category-preview check used synthetic text only and made no network/model calls or mutations. Semantic failure is a finding, not a repaired defect.
- Generic training fixture remains **MOCKED/SYNTHETIC** and its real generic backend unimplemented. Wired input-seat hostility is a **PLACEHOLDER**. Real text/audio specialist training, reports and uploads are not mocked.
- No code/config/credential/model/policy changes, new training, data upload, chargeable model invocation or publication. Only assessment continuity documents updated.

## Executive recommendation

Continue the platform, not a rewrite. The missing work is mostly fulfilment and verification of existing requirements; ARMI's product composition, score meanings, outcome attribution and concrete domain offerings need a small addendum. Use the five customer journeys as acceptance units rather than treating component counts or narrow milestone closures as delivered promises.