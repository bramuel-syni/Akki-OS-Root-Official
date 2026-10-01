# Akki requirements-alignment audit — 1 October 2026

## Decision

**The concern is substantiated. The current product is not fully aligned.** Engineering benchmark controls, milestone close-out reporting and implementation notes appear on live product routes. This is not permission to remove legitimate model evaluation, rights, approval, provenance, or document release evidence.

Scope: assessment before implementation, as approved in this conversation. No application code, prototype, authentication, database records, training jobs or runtime configuration was changed by this audit. Existing login was used for read-only inspection. This is not a security audit or a certification of every requirement.

## Authority and separation

1. The user's latest directive and attached Skills Brief govern this work. The M1/M6 implementation swipe is paused for this assessment.
2. Banked `frontend/public/prototype/v2_os.html` remains the unchangeable design authority. Its SHA-256 is `9952692ce05809b3f4111c8ec3cf9dcb1008ea970895263981c2b52fb78cf199`.
3. Domain evidence is product data when a requirement calls for it: held-out per-stratum accuracy and coverage, approval reasons, lawful use, source references, quality/release decisions, budget, calibration and uncertainty.
4. Engineering verification stays outside the product: pytest counts, benchmark launchers added for milestone closure, internal Mx-Ty progress, regression reports, phase numbers, repository paths and completion notes.
5. Tests verify requirements; tests, existing assertions, mock fixtures and a test agent's recommendations cannot create product requirements or alter the HTML design.
6. Required backend fields and rule values must not be weakened or falsified just to simplify presentation. Plain-language presentation does not change underlying authority.

## Confirmed findings

### A1 — P0: engineering benchmark promoted to a product feature

Live route: `/os/admin/modeladmission`, expanded **Answer quality (governed chat)**.

Visible: **Run 200-question check**, task-class mix, task outcome counts, grounding rules, latency, token totals and saved evaluation tasks.

Trace:
- `frontend/src/pages/os/AdminModelAdmission.jsx:43` mounts the section.
- `frontend/src/components/models/AnswerQuality.jsx:5-56` implements the bespoke dashboard and launcher.
- `backend/vendored/extraction_akki/backend/services/chat/router.py:101-132` exposes GET/POST `/api/chat/evaluations`.
- `services/chat/evaluation.py:21-26,219-255` defines an M4-T4 engineering evaluation and runs `journey.ask` on generated tasks. The route explicitly says model spend is real.
- Decoded owner HTML lines 4289-4323 define the Approvals tabs, statistics and decision rows, not this benchmark dashboard.

**Required correction:** remove engineering benchmark launch/reporting from the product composition, retaining the benchmark as engineering evidence where authorized. Preserve actual Model Approval decisions and required model-quality evidence in the original prototype slots. Do not simply rename or collapse the benchmark and call that compliance. No benchmark was started during this audit.

### A2 — P0: engineering milestone closure displayed as product recovery information

Same route, expanded **Recovery checks & deferred work**.

Browser-confirmed strings include `M8-T1 interrupt-and-resume · M9-T3 checkpoint restore`, `M8-T3 — Receipt chain audited`, and `M8-T4 / M8-T5 — Deferred by owner ruling 3a`. The latter is followed by developer close-out prose.

Trace: `frontend/src/components/models/RecoveryDrills.jsx:14-29`; `services/training_runner/m9_drills.py`; `routers/continuity.py`.

**Required correction:** keep customer-relevant recoverability, interruptions, resumptions and operational limitations, if required, in their proper original product surfaces. Remove engineering milestone IDs, proof narratives and backlog/owner-ruling status from product copy. Preserve immutable receipts in the evidence system; do not destroy them to declutter the UI.

### A3 — P0: 23 mounted routes replace intended product surfaces with implementation reports

Every route below was visited in the browser, not merely found in dead code. These pages display `HONEST GAP · SURFACE ONLY`, future PHASE promises, R-102/R-103 references, `App.js` or component paths, and/or build instructions. Most render a standalone replacement layout rather than their original full owner surface.

| Route | Mounted component under `frontend/src/pages/` |
|---|---|
| `/os/work/analyze` | `os/WorkAnalyze.jsx` |
| `/os/monitor/signals` | `os/MonitorSignals.jsx` |
| `/os/monitor/ideas` | `os/MonitorIdeas.jsx` |
| `/os/work/clarity` | `os/ThinkLabClarity.jsx` |
| `/os/work/strategy` | `os/ThinkLabStrategy.jsx` |
| `/os/work/hypothesis` | `os/ThinkLabHypothesis.jsx` |
| `/os/work/perspective` | `os/ThinkLabPerspective.jsx` |
| `/os/admin/govern` | `os/AdminGovern.jsx` |
| `/os/build/agentbuild` | `os/BuildAgent.jsx` |
| `/os/build/buildskill` | `os/BuildSkill.jsx` |
| `/os/build/extract` | `os/BuildExtract.jsx` |
| `/os/build/youragents` | `os/BuildlibAgents.jsx` |
| `/os/build/yourmodels` | `os/BuildlibModels.jsx` |
| `/os/work/mentions` | `os/CollabMentions.jsx` |
| `/os/work/emails` | `os/CollabEmails.jsx` |
| `/os/work/projects` | `os/CollabProjects.jsx` |
| `/os/work/hrstuff` | `os/CollabHrStuff.jsx` |
| `/os/apps/new` | `os/AppsNew.jsx` |
| `/os/apps/frequent` | `os/AppsFrequent.jsx` |
| `/os/apps/connected` | `os/AppsConnected.jsx` |
| `/os/apps/requests` | `os/AppsRequests.jsx` |
| `/dap/approvals-ledger` | `dap/AdminApprovalsLedger.jsx` |
| `/dap/watch-trail-bridge` | `dap/AdminWatchTrailBridge.jsx` |

Example: Build Skill says “Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment” and gives its source filename. These strings do not occur in the banked HTML.

**Required correction:** bind the existing owner surface to available services. Where functionality is genuinely unavailable, use truthful product-language unavailable/empty states within the original structure. Do not fabricate data, mark missing functions complete, remove required capability, or invent replacement cards to pass a screenshot test. Cosmetic cleanup alone cannot complete these workflows.

### A4 — P1: additional implementation/explanatory copy outside the 23 placeholders

- `/dap/connect/:tab`: `ConnectResources.jsx:11-26` describes missing endpoints and POST route names instead of presenting the required connection flow. Compute/models endpoints are described as present but unwired. Browser confirmed the shared surface; source review covers all four tabs.
- `/os/work/commission`: `WorkCommission.jsx` / `CommissionWizard.jsx` show descriptions of pane layout and internal canon implementation. Preserve actual objective questions and constraints; remove instructions about how the UI is constructed. No commissioning action was invoked.
- `/dap/buildskill`: visible “no cache, no mock” assurances plus a 401 refusal and **No skills provisioned yet** simultaneously. A failed read does not establish an empty store. Record this as a real state/flow problem, not a reason to waive access control or fabricate provisioning success. No auth changes made.
- `/dap/countdown`: raw JSON, uppercase backend field names and `NO_SHORTENING_PATH_IN_CODE` are visible. **Important qualification:** this route's source cites an earlier explicit requirement to preserve R-91 evidence values verbatim. This is a legacy evidence-presentation conflict to reconcile, not proof that all rule IDs or countdown data are invented tests. Preserve the values and actual countdown rules; do not relax or hide the required ceremony.

### A5 — P0 before claiming milestone closure: tested substitute is not complete requirement fulfillment

`AKKI_GOAL_ROADMAP_v1.md:272` records M4-T5 capability comparison as at least 200 tasks, two paths and at least 400 task-path outcomes, in an authorized isolated benchmark. The new visible evaluator calls a single answering journey per task (`evaluation.py:219-255`); its warm/fresh counters do not constitute two controlled comparison arms. It also states that generated text quality is not judged (`evaluation.py:315-316`).

This is a useful narrower engineering check, **not evidence that the full capability comparison is closed**. The audit did not run either benchmark and does not claim the broader comparison never existed elsewhere. Before closing M4, point to evidence that actually satisfies its adopted comparison requirement.

### A6 — P1: general model-training orchestration is not delivered by the current shaping dialogue

Current owner-created training rows hold five text fields (`training_lab/board_runs.py:7,56-68`). The **Begin training** action records a held request; `/api/training/lab/board/...` explicitly returns `training_started: false` (`routers/training_lab.py:256-260,324-333`).

Typed TargetOutcome/CollectionSchema compilers, calibration carriers, CI-bearing quote contracts, Targeta plan IDs, yield gates, MOAC and real specialized runners exist elsewhere. Their existence does not mean the five-field dialogue compiles and carries all of them end to end. `training_lab/skill/scripts/backend.py:42-47` deliberately refuses generic training; the README also disclaims generic compare/learning execution.

**Required correction:** preserve both objective artifacts and the full deterministic contract when completing the manager. Do not replace them with “ready”, a global accuracy score, an LLM verdict or successful fixture tests. Specialized language training is real; that does not establish a general-purpose training service.

## False positives explicitly rejected

- Training test sets, per-stratum accuracy × coverage, model acceptance and MOAC are required domain functions. Do not delete them because they contain “test”, “checks” or “passed”.
- Document validation/QA/reproducibility and build evidence are specified release safeguards in the supplied skills brief. Their exact UI placement still follows the owner HTML; removing their enforcement would be requirement flattening.
- Rule identifiers can be authoritative product references. Do not globally strip `R-*`, rule text or evidence identifiers.
- The prototype itself contains training status-weighted progress, including Refused = 92 and In Approval = 40 (decoded lines 16104-16116). These are not newly invented test-completion percentages. Do not redesign the progress control or claim they are measured accuracy.
- `CensusWorkspace.jsx` and several old Work/Watch components are not the current mounted experiences. Dead code alone is not proof of live UI leakage.
- Registry already loads `/api/portal/census/overview` via `usePrototypeSession.js` and has frontier bindings in `registryEstate.js:8-9,34-36`. The handoff's proposed first-time wiring is stale. Verify remaining M1 coverage requirements instead of adding a second Registry UI.
- The unmounted `extraction_sample.py` calls `stub_complete_sample()` and produces fixed 4,180-unit results. This is **MOCKED/SYNTHETIC**, not a live product measurement: the current runtime OpenAPI has no `/api/extraction/sample/run`. Do not wire it into a real sampling flow as if complete.

## Verification and its limits

- Read the user's DOCX, current PRD/roadmap/changelog, mounted routes, generated owner markup, decoded original HTML, relevant UI hooks, API routes and domain services.
- `owner-workspaces.json` records the current `v2_os.html` source hash. Older `os.json`/`dap.json` are generated from separately banked `assessment_workspace/canon/prototypes/20260925_owner_updated/{os,dap}.html`, not that file. Mixed provenance is not itself proof of an invented design; map each current surface to its governing owner source before any correction. This audit does not certify system-wide pixel parity.
- Existing external preview inspected as RMS operator; no new user or credential created.
- Initial desktop Model Approval inspection expanded both affected sections and confirmed the exact visible benchmark and milestone strings. No benchmark action clicked.
- One completed delegated read-only verification pass: `/app/test_reports/iteration_75.json`. It checked Model Approval, Chat, Documents, Registry, Estate intelligence, Train Models, My Work and Watch; its assertions require adjudication below.
- Supplemental browser sweep visited the 23 listed placeholders, DAP resource/rule/connection/request/entitlement/countdown/skill routes, commissioning, spend/rule approvals and training. Build Skill additionally inspected at 390×844; no horizontal overflow there. Model Approval smoke used 1920×800.
- Some supplemental request/entitlement views were still loading at the bounded observation; those are **not** counted as completed flow verification.
- External `/api/openapi.json` exposed 398 route paths. This validates route registration only, not that 398 features work. Targeted mounted families include governed chat evaluations, callable-skill provision, census overview, training lab, governance/checker/compliance and evidence-register services.
- M6 test collection reproduces `ModuleNotFoundError: No module named 'services'` with the plain command. With temporary command-local `PYTHONPATH=/app/backend/vendored/extraction_akki/backend`, seven tests collect. No test file fixed and no worker test executed in this audit.
- No census, training, GPU/SSH operation, provider call, chat send, provisioning, document generation, approval or destructive action was deliberately initiated. Reading existing views can perform their ordinary polling.
- Not verified: production runtime, all tenant/role combinations, every modal/state, complete pixel parity at all widths, every canonical requirement, or mutation/runner/quality acceptance. No milestone is newly closed.

### Adjudication of the verification report

The report incorrectly treated missing engineering prose in already-corrected My Work/Watch routes as a bug and recommended aligning with obsolete placeholder components. **Rejected:** absence of leaked engineering copy is not a failure; do not restore old routes or add the missing prose. It also missed RecoveryDrills by inspecting an unexpanded view. The main browser inspection expanded the section and confirmed A2. Its aggregate “success percentages” are not product completion measures and are not adopted.

## Corrective sequence (not yet implemented)

1. Remove A1/A2 engineering reporting from product composition while retaining internal evidence and required model/operational decisions.
2. Restore exact existing prototype bindings for A3/A4 surfaces; use existing services and truthful unavailable/error states, without inventing missing functionality.
3. Reconcile A5/A6 against original requirements before resuming the “over 65%” milestone sweep. Fix the local M6 import issue as engineering maintenance only.
4. Adopt the skill boundaries and reuse plan in `SKILLS_ASSESSMENT.md`; implement Training first, then Estate. No new orchestration platform or UI redesign.

The user's current “3-a unnecessary though” is not approval for a new identity ceremony. Existing identity and tenant protections were left unchanged. Do not perpetuate the handoff's unqualified “identity gate approved” claim or reinterpret this as permission for anonymous access.