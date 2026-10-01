# Skills opportunity — service reuse, not a new agent platform

Date: 1 October 2026. Assessment only; no new integrations or skills installed.

## Source

User-supplied **Akki_Skills_Brief_Final (1).docx**, retained at `assessment_workspace/incoming/skills_brief_20261001/Akki_Skills_Brief_Final.docx`.

SHA-256: `757adc1b3248a16ad197d65acd6165b731236e919ee5a3042843924ae390349a`.

The brief's expert/manager distinction is sound:
- **Expert:** substantive domain judgment grounded in sources, exemplars and references; not just JSON filling or format conversion.
- **Production manager:** makes the work reproducible and deliverable through explicit artifacts, scripts, validators, QA and evidence. It does not redefine policy or acceptance.
- **Deterministic:** authority, eligibility, measurements, arithmetic, validation, budgets, publication/admission and other governing gates.
- **LLM:** proposals, domain synthesis, drafting, diagnosis and explanation within bounded evidence. No invented counts, rights, prices, measurements or pass decisions.

Use one self-contained skill package per domain with both roles, not two autonomous deployed agents per area. Reuse existing service APIs rather than creating parallel registries, ledgers, training schedulers or approval ceremonies. Do not import one skill into another. The installed training overlay currently depends on its host service; reconciling that with the new self-contained-packaging requirement is work, not something already satisfied.

The brief's curated library, provenance/source map, deterministic golden paths, fixtures and evals belong in the skill package. A package smoke test stays an engineering artifact. Domain deliverable QA remains enforced but is shown only where the product requirements call for it.

## Recommendation matrix

| Area | Existing building blocks | What is actually missing | Recommendation |
|---|---|---|---|
| Model training | Installed training skill, statistics and specialist review; Objective Wizard compilers; calibration and CI quote contracts; Targeta planning/yield gate; language/text runners; MOAC, admission, manifests, run board and whitepaper records | One bound expert→manager→authorized runner flow carrying the actual two artifacts, registry population, strata, measured calibration, quote CI, plan_id, recipe comparisons/revisions and complete evidence | **First priority after UI-boundary corrections. High fit; partial, not greenfield.** |
| Estate discovery and census | Census scheduler/queue/workers; durable artifacts/receipts; frontier/exclusions; tenant-scoped Registry bindings; estate-intelligence report and document producer | An expert that turns the objective into a bounded investigation; manager linking sample adequacy, explicit exclusions, findings, cost/value assumptions and proposed actions | **Second priority. High leverage using existing services.** Do not duplicate the crawler or invent completeness. |
| Rules and registry | Canon/rule registries; upload/diff/version/commit routes; checker state machine; countersign/countdown; governing records | Domain interpretation and impact/conflict proposals; one coherent existing publication/review journey with evidence and dependency ordering | **Useful bounded assistant, not an autonomous rule-maker.** Complete the existing review path before adding more infrastructure. |
| Compliance and security evidence | Evidence register and claim precheck; compliance disclosures/refusal/retention/source-standing records; Watch/audit trail; export/production path | Control-to-evidence mapping, explicit missing/expired evidence, review ownership and a reproducible pack | **Useful evidence-assembly skill.** Not a claim of certification, legal sufficiency or a completed security audit. |
| Perception datasets | Media Library; metadata assessment/rights declarations; sound observables; fingerprint/reference separation; sample/holdout and training-data contracts | Admitted worker path for the intended dataset tasks, independent rights/annotation verification, stratified dataset production, revisions and receipts | **Build with Training as a dataset skill first.** Generalized media processing is partial; do not create a second media platform or confuse metadata readiness with measured quality. |
| UI Content manager | A supplied `surface-studio` package under `assessment_workspace/attachments/training_lab_20260930/extracted/skills/surface-studio/`; current owner-markup/blueprint binding; no installed surface-studio backend package | Controlled content production and revision service: brand/voice/accessibility, provenance, content versions, render validation and permitted editing boundaries | **Not redundant, but not connected yet.** It may populate approved content slots; it must not regenerate/reinterpret the banked UI. |

## Training — preserve the whole requested contract

### Expert responsibilities

1. Translate the business objective into **two separate artifacts**, not one flattened prompt or five generic strings:
   - TargetOutcome: register-defined population, named strata, per-stratum acceptance, test-set reference and the required acceptance dimensions.
   - Collection Schema: required data fields, types, rights/provenance and collection constraints.
2. Design the stratified held-out set without leakage or unsupported population claims.
3. Propose the two-arm comparison, including comparable evaluation conditions, baseline and cost implications.
4. Diagnose failures per stratum and propose evidence-linked recipe changes. Preserve failed/abstaining/uncovered strata; do not average them away.

### Manager responsibilities

1. Compile/validate both artifacts through existing contracts; unresolved requirements remain unresolved.
2. Commission calibration before full-run quotation. The existing calibration contract calls for three to four data volumes and per-stratum evaluation/scaling; a carrier or `has_calibration=True` is not actual calibration evidence.
3. Quote with a stated uncertainty/confidence interval based on appropriate measurements. Do not rename a prior/scenario range into a measured confidence interval.
4. Carry the same evidence-linked `plan_id` across collection, recipes, manifests, evaluation and admission.
5. Track **accuracy × coverage for each stratum**, not a single pass percentage.
6. Keep the manifest 100% classed according to the governing classification scheme; an LLM assertion is not classification evidence.
7. Preserve each recipe revision with its reason, predecessor and measurements, and run the authorized two-arm comparison.
8. Assemble the full MOAC pack and whitepaper inputs. Route document production to the existing document capability; do not invent a second renderer or claim the current whitepaper suggestion already performs that handoff.

### Existing code evidence

All backend service paths below are relative to `backend/vendored/extraction_akki/backend/`:

| Requirement | Existing code | Limitation found |
|---|---|---|
| Two objective artifacts | `services/wizard/objective_compile.py`; `services/audio_plane_v1/target_outcome.py`, `collection_schema.py` | Not shown as a complete compilation path from owner-created five-field training conversations |
| Calibration and quoted CI | `services/audio_plane_v1/calibration.py`, `training_planner.py`; `services/training_lab/statistics.py` | Some modules are typed carriers/gates only; do not count them as worker execution |
| Deterministic plan/eligibility/yield | `services/targeta/plan.py`, `core.py`, `yield_layer.py` | Carry these through the training manager; do not replace with an LLM-generated plan identifier |
| Actual language training/admission | `services/training_runner/`; `services/audio_plane_v1/language_cognition_dispatch.py`; `services/model_admission/` | Specialized real paths exist; no fresh GPU validation performed in this audit |
| Installed skill and advisory roles | `services/training_lab/skill/SKILL.md`; `skill/scripts/backend.py`; `README.md` | Real generic `.train()` explicitly refuses; stub comparisons/learning curves are MOCKED/SYNTHETIC only |
| Board and revisions | `services/training_lab/board.py`, `board_runs.py`, `conversation.py`; `routers/training_lab.py` | Owner-created “Begin training” records a held request, not actual training dispatch |
| Whitepaper handoff | `routers/training_lab.py:269-270`; `services/cif/`, `services/doc_studio/` | Board explicitly says finished-document production is not connected |

## Other domains — role boundaries

### Estate discovery/census

Expert: decide which authorized sources/strata answer the business question; interpret duplication, degradation, quality and reuse/monetization opportunities with assumptions and limits. Manager: commission bounded reads through existing workers, reconcile accessible/completed/excluded scopes, retain evidence, prepare actions and reports. Deterministic: scope/rights, inventory counts, measured coverage and gates. LLM: interpretation and recommendations only.

Reuse `services/census_autonomy/` including `frontier.py`, `assist_census_v1.py`, `operational_reads.py`, `registry_surfaces.py`; estate-intelligence producer and current Registry model. Existing M1 bindings already consume frontier data. Monetization recommendations are not realized revenue; duplicate estimates are not deletion authorization.

### Rules/registry

Expert: cited interpretation, conflicts, effects and draft amendments. Manager: assemble the versioned change, affected dependencies, review and publication evidence. Deterministic service remains sole authority for publication order, authorizations, countersignature and countdown. No LLM policy execution or additional approval layer.

Reuse `/api/govern/*`, `/api/checker/*`, `/api/canon/rules/*` and their existing stores/state machine. Current Rules Updates UI is explicitly unavailable, so backend presence is not an end-to-end completed rule workflow. Some legacy registries are in-memory/pure carriers; do not equate those with the durable publication path.

### Compliance/security evidence

Expert: map requested controls/claims to available evidence and identify uncertainty. Manager: assemble a traceable pack with dates, scope, source records, responsible reviewers and gaps. Deterministic: evidence existence, provenance, access, expiry and required gate calculations. Do not invent proof, certificates, signatures or legal conclusions.

Reuse `services/evidence_register/`, `services/compliance/`, `routers/compliance.py`, governance/checker and Watch/audit services. This audit establishes reusable parts, not regulatory compliance or security assurance.

### Perception datasets

Expert: label taxonomy, strata, annotation guidance and failure diagnosis. Manager: lawful-source inclusion, independent review, measured quality, dataset versions, sealed splits, exports and receipts. Deterministic: eligibility/rights gates, split integrity, deduplication measurements and dataset accounting. LLM: proposals/assistance only.

Reuse `services/media_library/`, `services/audio_plane_v1/acoustic_observables.py`, dataset/manifest contracts and appropriate admitted workers. `media_library/assessment.py` explicitly says metadata-only, not measured quality or independently verified rights. `services/perception/sample_lifecycle.py` includes a fixed-result **MOCKED** implementation; its sample route is unmounted in the current app. Never surface those fixture numbers as real dataset measurements.

### UI Content manager

Expert: content purpose, hierarchy, voice, readability, accessibility and source-grounded wording. Manager: approved content schema, versions, edits, dependencies, preview/export and validation. Deterministic: locked structure, link/schema validity and release rules. LLM: copy proposals only in editable regions.

The supplied surface-studio package already describes page briefs, voice/brand references, component/content decisions and production commands. For this app the latest frozen-HTML rule is narrower: **content authority is not layout authority**. Broad layout generation in the supplied package must not be enabled against `v2_os.html`.

## Smallest sensible adoption

1. Correct the product/testing boundary first using the banked HTML.
2. Complete one Training expert/manager vertical path with the full requested artifacts and existing runner/gates.
3. Apply the same package discipline to Estate; attach Perception as a bounded dataset capability serving Training.
4. Add Rules and Evidence assistants around existing deterministic services, without new policy engines or approval ceremonies.
5. Connect surface-studio only for approved content surfaces; no autonomous UI redesign.

**Over-engineering would be:** a new multi-agent runtime, two separately deployed services per role, parallel stores/registries, a second training scheduler, independent policy decision agents, or a new “skill quality/testing” dashboard. None is required to realize this proposal.