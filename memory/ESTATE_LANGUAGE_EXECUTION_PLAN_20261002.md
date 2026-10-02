# Estate intelligence, language evidence and training continuity — approval plan

Status: PROPOSED; awaiting owner approval of the expanded scope. No application code, thresholds, model configuration, admissions, serving state or GPU jobs changed during this assessment.

## Owner orders
- Approved the previous report design. Produce downloadable DOCX, PPTX and supporting XLSX.
- Explain terminology in plain English, identify exact evidenced folders/files/tables, and state specific executive decisions for organization, cost management and storage discipline.
- Add estate-held non-English/non-music audio and text, broken down by language, audio hours and quality, with evidence for written news scripts and their hourly frequency.
- Lower the admission floor for Luhya only, leaving others unchanged, and admit.
- Use both GPUs for this evidence/classification job with current cognition-language model versions.
- Give the training assistant persistent memory of the specific job and its prior iterations.
- Completed training window: three tabs, Chat / Overview / Learning report, preserving banked HTML design.
- Assign LLM-shaped planners, wizards, managers, writers and orchestrators by independently evaluated task strengths; use different orchestrator/reviewer model families. Preserve Shield and designed governance.
- Reflect the expanded order for approval BEFORE autonomous launch.

## Read-only findings (2026-10-02)
- The prior handoff is stale about Luhya v3. Mongo `training_lab_signoffs`, queried directly with `_id` excluded, already contains completed v3 `lcj-7128593897d4` / board run `reinforcement-lwg-v3`.
- V3 outcome: refused; LWG accuracy 0.75795 on judged windows, abstention 0.12785; existing floor 0.9. Other-language regressions recorded: guz, kam, kik, kln, luo, swa. Served-output speaker probe above chance. Neither admission nor a threshold update occurred in this assessment.
- V1 `lcj-1dd5012c909c`: 0.72283 LWG accuracy, 0.18831 abstention; other-language regressions and speaker check failure. V2 `lcj-7841bcce8855`: complete abstention, no measured accuracy.
- Training assistant and advisory roles currently share `TRAINING_LAB_MODEL=gpt-5.4`. Existing report writer recorded as `claude-sonnet-5-5`.
- Conversation storage is durable but the prompt retrieves only eight recent messages plus selected current-run evidence. Parent lineage exists; comprehensive job-specific retrieval and prior-version evidence are not yet supplied.
- Completed training UI currently has Overview / Learning report tabs; chat visibility is separate. Implement explicit three-tab behavior without redesigning the prototype.
- Existing audio measurement worker is CPU DSP on the host, uses staged corpus only, and keeps `results_map.json` paths on-host. It is NOT already a two-GPU whole-estate language classification pipeline.
- Existing census/report lacks verified full object paths and keeper/removal pairs for some findings. Collect missing evidence rather than invent filenames or assert confirmed reclaimable capacity.
- No board GET was used in this assessment because that route can kick the autopilot. No new GPU availability/occupancy measurement was performed; historical idle status must not be presented as current.

## Proposed execution

### 1. Luhya-scoped acceptance revision
- Proposed owner decision: lower Wanga (`lwg`) accuracy floor from 90% to 75%; this is a disclosed policy choice, not a new model improvement or independent blind validation. Do not extend to Bukusu or all Luhya varieties by inference.
- Record a new revision linked to the owner order, candidate checksum and original evaluation. Do not overwrite signed historic plans or their refusals.
- Keep every other language's threshold and existing model selection unchanged.
- Assess a genuinely language-scoped candidate/routing path rather than promoting the regressed multilingual checkpoint wholesale. Verify the routing behavior and remaining existing acceptance requirements.
- A lower floor alone does not erase the recorded regressions or speaker-check failure. If these still prevent admission under unchanged governance, disclose exactly which result remains and return the decision to the owner. Do not silently disable checks or label a refused checkpoint admitted.
- This order is not authorization for another undisclosed retraining recipe. No new retraining proposed as part of the measurement job.

### 2. Two-GPU evidence collection and classification
- After approval, discover actual available devices on the approved worker host; use both GPUs for parallel batches, not control-plane processing. Do not interrupt an existing serving process.
- Pin exact current permitted text-language, audio-language and music-detector artifact versions/hashes and log them with each classification batch. Audio research predictions must not be presented as admitted or human-verified classifications.
- Balance the two queues by estimated work, collect actual utilization/throughput, checkpoint progress, avoid replaying completed batches. Deterministic inventory/hash/quality measures remain appropriate CPU work.
- Proposed initial measurement allocation: 6 GPU-hours total, counted across both devices, not 6 per device. This is a new proposal for approval, NOT an inherited approved cap. A calibration batch determines the expected coverage/time; if scope exceeds allocation, report completed coverage and request continuation rather than claim an estate-wide complete result.
- Enumerate DB/NAS/object-store sources, distinguish accessible scope from unreadable sources, and join original paths/DB references to classified outputs.
- Report total recorded hours separately from speech-only/non-music segments. Explicitly retain mixed-language, code-switched, music/mixed and uncertain outcomes; do not force classification from folder names.
- Measure decode failures, silence, clipping, noise/channel condition and intelligibility only to the extent supported by the available measurement/model. Do not call sample rate alone an audio-quality grade.
- Text: per-language source documents/scripts, characters/words, bytes, duplicates/completeness, date range and observed hourly coverage. Verify the owner's hourly-news-script observation with actual DB table/field/time counts; report gaps and represented dates, not assumed 24 scripts/day/language.
- Avoid double counting staged copies, transcripts, DB records and archived originals. Keep deduplicated and gross inventory separate.
- Owner rights declaration remains established; access errors are operational findings, not reopened ownership questions.

### 3. One evidence-backed report pack
- Native pipeline: Planner → measurement Workers → Document Content Manager → Frontier Writer → independent Reviewer → existing QA/release. Human-readable explanations and LLM work do not replace deterministic arithmetic and evidence checks.
- DOCX: full executive report, glossary, precise locations, findings, recommendations and evidence appendix.
- PPTX: editable decision presentation consistent with the DOCX and workbook.
- XLSX: methodology/definitions, source register, per-language summary, audio-file/segment evidence, text/script evidence, hourly coverage, quality, duplicate/reclassification candidates, cost assumptions/formulas, executive decisions, model versions and coverage gaps.
- Source records include evidence ID, exact source location, measurement time, version/hash where available, classification basis/confidence, source duration versus measured duration, and trace to report claim. Use indexed sheet parts if evidence exceeds Excel's row limit; do not silently truncate.
- Local/private binding restores exact names into final owner documents after Shield-approved external authoring; raw paths/content are not sent around Shield just to make reports specific.
- Explain “reclaimable” as potentially removable or cheaper-to-store capacity subject to the documented verification, not bytes already deleted or guaranteed cash savings. Explain “empty required-looking fields” as blank fields that appear important from naming/patterns, not proven violations of declared DB constraints.
- Distinguish archive/tiering, deletion and duplicate removal; unchanged-write dates are not evidence of no reads. Reference tariffs are not actual invoices. Do not add overlapping savings.
- Each executive decision identifies actual evidenced source, proposed destination/rule, action, benefit, assumption, responsible role, proposed timing and remaining evidence. Proposed paths are labelled proposed, never existing facts.
- Recommend naming/versioning, authoritative master copies, working-copy cleanup, storage tiers, ownership and review/retention discipline. This commission does not execute moves, deletions or reorganization.

### 4. Durable training job memory and three tabs
- Retrieve tenant/job-specific objectives, signed decisions, data manifests, recipes, metrics, errors, lessons, prior-version links and reports, with references and version timestamps.
- Keep older approvals separate from current authority; remembered text never signs a new plan.
- Verify multi-turn history, reload/resume, older-than-eight-message retrieval, parent-to-child continuity and cross-job/tenant isolation. New external context still crosses Shield.
- Chat: full conversation and composer. Overview: objective, recipe, compute, models, outcome and sign-off. Learning report: measured improvements/regressions, errors, lessons, evidence and next-iteration recommendations.
- Preserve `v2_os.html` as design authority; extend the existing tab pattern only. Unique test IDs; desktop/mobile verification.

### 5. Task-specific LLM assignments
- Inventory all actual LLM-shaped callers and role job descriptions, not only the training assistant. Keep authority/arithmetic/scheduling deterministic where designed that way.
- Proposed pair: GPT-6 Astra (`gpt-6-astra`) planning/orchestration; Claude Fable 5.1 (`claude-fable-5-1`) independent review. Writer candidates include current Claude Sonnet 5.5 and Fable 5.1, chosen by a task-specific evidence-grounding/writing comparison rather than model branding.
- Public official documentation and the available integration model list include the proposed pair. Actual account calls were NOT tested during this planning assessment. Independent Fable evaluation was consulted; vendor GPT-6 performance claims are not independent proof of planning superiority.
- Evaluate evidence fidelity, plan completeness, complex task/tool success, review error detection, document quality, latency and cost against role-specific examples. Include local candidates where fit is demonstrated. Publish the assignment rationale, measured score, version and evaluation date.
- Reviewer gets source evidence and acceptance criteria, not just the orchestrator's conclusion. Record disagreement and resolution. Different families reduce shared blind spots but do not guarantee independence or correctness.
- No silent downgrade, role/model replacement or Qwen report-author fallback. Unavailable candidates are disclosed.
- All external requests retain the sole Shield invocation boundary, purpose/tenant/actor binding, masking, allowlisted connection, credentials protections and receipts. Preserve governance engines and release checks.

## Before launch / acceptance
- Owner approval needed for this expanded plan, proposed 75% Wanga-only floor, and proposed 6 aggregate GPU-hour measurement allocation.
- No new credentials needed from the owner at this stage; existing access is used. Ask only if a real unavailable source or model connection cannot be resolved from existing configuration.
- Test unchanged floors for other languages; admission revision provenance; two-device allocation/checkpointing/budget accounting; Shield for all new calls; durable scoped memory; three-tab desktop/mobile behavior; exact claim-to-XLSX evidence joins; OOXML opening and actual downloads for all three artifacts.
- Do not claim scope complete from tests alone or historical reports. Do not republish old report files as the requested new pack.
- Remaining M1/M6 and M5/M7/M8 backlog unchanged. This approval is for this job's implementation/measurement/release, not an application production deployment.