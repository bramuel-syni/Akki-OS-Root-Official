# Mα — verbatim owner orders and interpretation boundaries

Recorded 2026-10-04 before further research/compaction. These are visible conversation records, not a substitute for the canon. Read with `M_ALPHA_PLAN.md`, `M_ALPHA_HANDOFF.md`, and the response archive once populated. Do not discard, paraphrase away or silently narrow these orders.

## 1. Owner — five promises (verbatim)

There are a few promises i would like you to check the promises against 
- Akki OS can be used to govern & securely train models of different dimensions using integrated enterprise data or uploaded external data
- Akki OS can be used as foundational system to power a context as a service product productizing capability such as as estate licencing without moving data, model and skill training for marketing, content mining for content creation, media planning, campaign strategizing, and many other opportunities based of the innate capabilities.
- Akki OS is designed to pick the right model for the task in the backgroud where you will get the best agent managing and executing the deliver of your order. E.G. You experience AI the same way you experience LLM in their makers chat websites or probably even better. For instance, Akki produces some of the best decks, reports, white papers, board artefacts, executive brief at a fraction of the cost.
- Akki OS also serves as an Agent Resource management interface (ARMI), similar to Human Resource management, Akki is designed to hold the profile, performance, business objective it serves, JD, etc of all the agents, LLMs, skills that have been admitted to do any sort of work in an enterprise, e.g. E1 is a software developer, has a compliance score of xx, Admission pass off xx, malicious conduct probability of xx, strengths, JD, what it can do and not do, resources it consumes, behaviour and tasks it has complete, who it has coworked with and how it has contributed to revenue/productivity etc. 
- Akki OS gives you control. Within Akki (AI in a box), user has control, theys can shield how LLMs see their data by managing a confidentiality register thats is both classification by name or classification by contentext - example - PII is removed, or if a contract that has trade sectrets or etc, The Shield (Synisense + Solva) will recontruct message to LLM withough diivulding priviledged information. Use the most advanced LLM here that can be contained in the synisense box.

How fare are we from delivering this promises, % status

## 2. Owner — dimensions / boundary / rigor clarification (verbatim)

1. A and B, 2. B - How synisense is designed to work

I agree, rigorously review the canon requirements. Also list - if any - requirements needed but were not originally prescribed. Act as a seasoned products designer, architecture and engineer to ensure you look at this holistically, objectively without flattening or over engineering.

### Options to which that reply referred
- Dimensions A = different sizes and architectures; B = different tasks and modalities (text, audio, image/video, tabular, etc.). Owner chose BOTH.
- Boundary B = frontier models may run externally, but receive only Shield-approved de-identified/reconstructed context; privileged originals remain inside.

## 3. Owner — Mα request (verbatim)

Can you develop M alpha - focussing on getting the 5 promise requirements as you have listed to 100%. What do you need?

## 4. Assistant — immediately preceding clarification/plan offer (verbatim)

I can develop **Mα as one delivery programme with five acceptance tracks**: governed training, Context-as-a-Service, model/agent-led delivery, ARMI, and Shield.

I already have the canon, codebase, fixed HTML design authority and your Mode B clarification. **No new credentials are needed to begin the requirements reconciliation and build plan.** Five decisions are needed:

**1. Release scope**
- Approve me drafting a concrete acceptance matrix covering all five promises and every business use case you named, with explicit model sizes/architectures and modality coverage.
- You review that matrix before we freeze scope. “100%” means every agreed requirement works and passes its acceptance tests—not just a pilot or working components.

**2. Shield’s remaining policy conflict**
- **A. Strict masked-only external calls:** no privileged originals leave, including disabling the existing unmasked entity-knowledge exception.
- **B. Retain that separately authorised exception**, explicitly distinguished from the normal masked-only promise.
Your Mode B clarification points toward A, but changing an existing policy needs explicit approval.

**3. Quality, cost and final acceptance**
- Who is the named owner/reviewer for final acceptance?
- Do you already have quality targets, comparison products and a target cost reduction? Otherwise, may I draft measurable criteria for your approval—without treating proposed thresholds as agreed?

**4. Execution authority and spending limits**
- May I implement and run local/preview tests once you approve the Mα charter, while holding GPU training and chargeable model evaluations for separate approval?
- Alternatively, provide a **GPU-hour cap and external-model spend cap** for autonomous execution. Existing infrastructure access alone will not count as spending authority.

**5. Representative acceptance material**
- May we use the existing RMS estate and authorised uploads, plus synthetic confidential-contract cases initially?
- For final acceptance, we will also need representative confidential documents, business briefs with expected outcomes, and a named client/application workflow. Can you supply or nominate those? Please do not paste sensitive documents or credentials into chat.

Once confirmed, I’ll produce the **Mα charter, canon-to-requirement traceability, five-track acceptance matrix, dependency-ordered implementation plan, and evidence-based effort/cost estimate**. Existing requirements, necessary additions and owner decisions will remain clearly separated. Full acceptance will require independent evidence; security and superiority claims will not be certified merely because tests are green.

## 5. Owner — latest approval, correction and execution order (verbatim)

1 - approved, yes
2 - I think its a mix of 2 where we have data pass through and task asignment - For instance there is a workflow that is triggered by a contract with confidential information - the how to (e.g delivery planner, graphics designer), frontier LLM doing this has no access to data from whatever angle but can participate. 
3. Quality targets have already been prescibed. There is definition of "best" in most of the outputs we are producing - eg best ai generated decks are known to be produced by xxx, this is how this is achieved, surgically do your research - a mix of what you have, what you had (i think in akki core) and "best decks" production requirements can do this for the deck. Do the same for the others for quality standards - as promise is "experience and quality of output is the same or better than..."
4. For now there is no GPU cap until we get billing data. Package your job for best outpu no limit on GPU for now, we will adjust later. As a test I am a customer working on a local language story telling agent - I would like you to train a multi language (kikuyu, kamba, swahili), story telling model that can deliver a story with the same dynamism as the presenters in the audio recordings you have. It needs to be as natural sounding as the presenter. what i will evaluate is how you implement the AIP requirements - treating Audio as a database, how akki maintains the unique language signature, invention of biometric of the AI voice, learning/training technique thats beyond listening, where audio file is treated as a data base, from a single file multiple data sets (discoverable spectrum) are generated. this data is used to engineer training parameters and engineer performance targets. The discoverable spectrum data behavior is used for similarity modeling - baseline spectrum data behavior vs AI generated audio sperctrum data behavior and how fast this can accelerate training. I also want to see the performance of the white paper wizard (see canon docs for requirements). Also note that training is not just for audio, ensure you have covered all other dimensions as well. Another model that can be used to test milti dimensionalism is a multi language (kikuyu, kamba, swahili) listening model that can be used to monitor brand mentions on radio. Akki can run this autonomously in the back ground until admission pass of 90% is achieve. no limit to the number of iterations it needs to run to achieve this autonomously. Divide the work on the GPUs, let it run in the back ground as you build.
5. I think you can create this sample docs for testing and go ahead and use existing 

Break this work down with clear job requirements = capability = test = pass
Register this plan and our last two sets of responses+order from me pre compaction on disk and any other important piece of information or strategy that will avoid leakage/loss of specs. Share with me M alpha plan and reflect back to me my asks.

## 6. Interpretation boundaries — assistant assessment, NOT additional owner quotes

- Latest order authorizes Mα planning and development toward the five promises, existing-data/synthetic-document testing, and GPU work without an owner GPU cap or iteration ceiling for now. Do not reinstate the prior need to ask for a GPU-hour cap. Record measured billing/usage and revisit when actual rates/bills arrive.
- Uncapped GPU usage does not mean permission to acquire unbounded new infrastructure, unbounded paid external API use, bypass custody/licences, train on unqualified data, evict other workloads or waive acceptance. Existing hardware must be discovered and capacity-admitted. An arbitrary finite cap must not silently replace the order.
- Owner requests two genuine three-language workloads: **generative spoken storytelling** and **listening/brand monitoring** for Kikuyu (`kik`), Kamba (`kam`), Swahili (`swa`). Neither is satisfied by training only a language-identification classifier. Previous 13-language LID expansion remains a distinct requirement, not replaced or automatically completed.
- AIP database/discoverable-spectrum/parameter-engineering/spectral-feedback requirements and White Paper Wizard are first-class acceptance scope, not appendices or demonstrations.
- “Inventing biometric of the AI voice” is interpreted as creating a distinct synthetic voice identity with language/prosody fidelity, not cloning or identifying an actual presenter. Preserve the canon's no-identification-biometric register and no-speaker-ID constraints. If the AIP canon requires clarification, record it explicitly; do not silently override.
- The owner explicitly wants natural presenter-like dynamics; frequency/spectrum similarity alone cannot demonstrate intelligibility, meaning, language authenticity, expressiveness, distinct identity or absence of memorisation.
- 90% is the owner's stated admission target, not authority to waive failed safety/rights/regression gates or average a weak language away. Recover task-specific canon metrics first. Any necessary mapping of this target onto WER, mention precision/recall, listener ratings, etc. must be explicitly labelled derived/proposed, never fabricated as an existing ruling. Do not repeatedly tune on sealed admission material.
- Unlimited iterations means a resumable governed improvement process, not a promise convergence is guaranteed or permission to loop wastefully on absent labels/access. Checkpoint/hold honestly for data, safety, worker failures or no actionable next experiment; retain research evidence and resume with cause addressed.
- Latest Shield explanation requires **data/task separation**: privileged data stays within trusted workers; an external planner/designer may receive an abstract non-sensitive task/structure and return instructions or layout without accessing the protected data. Do not equate this to authorization to send raw contracts externally or automatically disable an unrelated existing CC1 policy exception.
- Quality targets already exist: recover them from canon and existing/legacy Akki Core, then perform targeted current external research. Do not ask the owner to recreate prescribed standards or invent numeric thresholds. “xxx” names no actual vendor; do not manufacture a universal best competitor.
- Latest order changes the previous assessment-only scope. It does not authorize claiming jobs running before actual native job/PID/heartbeat evidence, or claiming 100% delivery on documentation/fixtures.
- Preserve `v2_os.html` authority and existing service boundaries. Existing M5/M8 deferrals stay unless directly required by the newly approved promise-completion scope; identify conflicts rather than silently dropping or unpausing unrelated work.

## 7. Existing continuity anchors
- Five-promise assessment: `/app/assessment_workspace/notes/goal_delivery_20260928/FIVE_PROMISES_CANON_ASSESSMENT_20261004.md`.
- M1–M10 assessment: `/app/assessment_workspace/notes/goal_delivery_20260928/M1_M10_STATUS_20261003.md`.
- Runtime source: `/app/backend/vendored/extraction_akki/backend/`.
- Current credentials: `/app/memory/test_credentials.md` (do not duplicate secrets here).
- Runtime URLs: use current frontend/backend environment files, never archived preview URLs.
- Last verified status before this order: general trainer RealBackend unimplemented; special-purpose runners real; uploaded media stops at metadata readiness; semantic category protection and input-seat detector incomplete; cost data partial; Agents page unavailable. Do not erase these findings with a new milestone label.

## 8. Owner — Shield capability, placement and requirements-first correction (verbatim)

Source: current continuation conversation; the owner subsequently said “Proceed”
and supplied the preceding exchange for reconciliation. Preserved as supplied;
the numbering refers to the earlier assistant questions, not fresh options.

1 - this is already prescribed, your question shows that you have not rigourously reviewed the requirements.
2 - the "confidential identification register" is the user set point of reference that the agent uses to know what is "classified". Category 1 - conventional identifiers scrapping (PII, HII, BII, Credit card numbers, and so on), Category 2 - specific named content that user has listed and could be uploaded in an excel to a Confidentiality Vault Manager (information that only the user has), Category 3 - this is descriptive requirements where user describes the kind of information they would not like to see shared - e.g specifics in  contracts, product briefs, BRDs, Audit reports that could directly or indirectly disclose parties, IP, trade secret, value, status or any kind of information that can be deemed as privilage. The required capability here is both deterministic and reasoning by models that do not have any contact with the external world - fully owned and controlled by the estate owner e.g the latest qwen self hosted, working with a superior NER type model, and so. the foundation of this is in the requirements, i just need you to improve capability, deliver the promise and make it functional.
3. I agree, do this for all the registered requirements on disc documents or narrated over chat, the building guard rails i have asked to implemented and the ratification i have asked to date. (ones i have explicitly issued here)
4. This sounds like a placement issue, shield should happen outside LLM processing. What you are describing is Shield being inside a processing journey. Audio is unique as first the worker converts it into a spectrum data base with the data that makes the biometric data is scrapped or modified without affecting the quality for training, so this spectrun data is not stored with the the actual biometric info - eg to every biometric spectrum data point add 3 basis points (random thought, you can figure out how to work this out without messing up with the quality of the data.

Generally there needs to be clear disc recorded can rule that you primarily operate from issued requirements and if in anycase we need to evolve/ratify a feature or add new things for better function, performance qaulity or function, we need to record on disk and consistently anchor agent to read these things before inventing from top of mind.

## 9. Reconciliation boundaries — NOT additional owner quotes

- Section 8 requires a requirements-first operating rule across ALL issued
  requirements, not a Shield-only checklist. `/app/AGENTS.md` is the persistent
  entry anchor; `REQUIREMENTS_RECONCILIATION.md` holds sources and evidence.
- The three owner categories are protection needs; existing `exact`, `pattern`,
  `contextual` are implementation mechanisms, NOT a replacement taxonomy.
- The owner did not nominate Qwen3-8B as the final model, approve dedicating or
  evicting a GPU, adopt a “three basis points” transformation, or waive biometric
  privacy/quality tests. Those were examples or earlier assistant proposals.
- Placement means estate-side protection before external task processing. Doc 1
  still requires the sole invocation to enforce custody, and expressly requires
  contained pre-redaction meaning extraction. Moving checks out of the call stack
  while leaving a bypass would violate, not satisfy, this requirement.
- Earlier 04:22 UTC job/Shield claims supplied by the owner are historical
  assistant claims to verify. They are not fresh live observations in this fork.
- Dispatcher metadata rejection is a separate control-plane contract defect; it
  is not caused by Shield placement. Repair does not ratify or replace Shield.
- Do not carry forward the earlier regex-only repair plus paid frontier replay
  plus immediate MA-19 jump as the settled sequence. Reconcile first, then execute
  source-traced work packages, retaining all remaining M Alpha obligations.