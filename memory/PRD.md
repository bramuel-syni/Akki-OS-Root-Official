# Akki — product requirements and current continuity

## Original problem statement

The user requires the AI to deeply understand, audit and operate the Akki Extraction
platform under strict architectural and governance rules; wire DAP requests, work
history and entitlement lifecycles to actual backend engines; and execute a
dependency-ordered fix plan based on a648-row gap analysis, bridging isolated
components into a continuous governed end-to-end chain with durable evidence.

Product requirements:
- **E1 is NEVER the source-data execution path.** It wires admitted descriptors.
- Evidence-based accounts of what is built, mocked, unbound or actually verified.
- Strict100% UI fidelity to the user's literal HTML prototypes; data wiring only.
- Preserve frozen Canon contracts and single authoritative append-only ledger.
- Architecture testing is distinct from real-element/operational qualification.
- Owner permissions and live results cannot be manufactured from fixtures or chat.

## Current owner instruction and operating boundary

"Proceed, only blocked issue is GPU/SSH. Rest you are cleared to go".
Continue autonomously with all independent implementation/integration/testing and
properly admitted non-GPU activity. Do not impose blanket source/model/credential
work bans. Required authority is a workflow to implement/use, not a reason to stop
all work. No blind GPU retries, key replacement or disturbance of original runtime.
Use English in all communication.

Live Activation v1.3 document review closed. Owner v1.1 certificate schema/crossing
table accepted as final desk-authored inputs; E1 owns versioned hardening, semantic
verification, policy integration and record recovery. No further generic specification
round. Actual unknown policy decisions must be precise, resolved before protected
evaluation; never infer measurements or thresholds after observing results.

Owner rulings to recover/validate in native records (not automatically applied):
scope/expenditure/purpose-specific approval categories, independent required groups,
any-one within each unless ceremony quorum; per-run authority through gate; existing
allocation20 GPU-hours/run and USD0 external; controlled pilot custody, masked
uncontrolled-only frontier crossing, controlled exception unavailable, no disclosure
counterparties; any loosening receipted. File/chat claims do not establish live records.

## Architecture and source of truth

- React frontend + FastAPI + MongoDB. Environment-configured URLs, databases and
  credentials only. Canonical backend imports vendored Akki services.
- Runtime: `/app/backend/vendored/extraction_akki/backend/`.
- Bootstrap: `/app/backend/server.py`.
- Canonical ledger: `services/ledger_writer/{principal_control,mongo_control}.py`.
- Coordinator/ports/native adapters: `services/northena/execution_*.py`.
- Handoff sidecars: `services/mkondo/execution_*.py`, native registry/contract intact.
- Registry/inspection consumer: `services/mtafiti/execution_registry.py`.
- Portal: `routers/portal_requests.py`, `services/portal_operational/`,
  `services/northena/portal_work.py`.
- New activation controls: `services/activation/`, `routers/activation_controls.py`.
- Frontend owner markup: `frontend/src/.../OwnerMarkup.js` and original public
  `prototype/dap_latest.html`, `prototype/v2_os.html`; neither changed this batch.
- Every Mongo response excludes BSON IDs; immutable request identity and canonical
  evidence are preserved. Do not introduce a parallel job/admission/receipt authority.

## CURRENT checkpoint — 2026-09-28 06:40 UTC, NON-GPU WORKER BUILT + LIVE ESTATE READ

Owner instruction: "no non-gpu worker. build one, operates similar to the gpu
worker. Repository to be ready once done. Can you read the estate i have shared?"
Owner answers: (1) dedicated worker inside the akki environment; (2) both routes
legitimate depending on commissioned work type; (3) DigiCow — "see attached";
(4) will share additional data repository to connect; (5) commission Akki to fully
read the connected estate registered in the right tenant, do not rebuild what
exists. Owner also demanded a plan with NAMED GAPS and how each contributes to the
remaining % to completion, plus a done/remaining roadmap.

DELIVERED (verified, unmocked):
- Built the missing non-GPU ingestion worker mirroring the GPU worker's contract:
  `services/census_autonomy/non_gpu_census_worker.py` (worker; bounded subprocess,
  local counterpart of remote_worker.py), `estate_connector_registry.py`
  (authorised credential resolver → 0600 connector custody from the registered
  estate), `non_gpu_dispatch.py` (dispatch authority, local counterpart of
  remote_dispatch.py). Selected via `AKKI_CENSUS_EXECUTION_MODE=non_gpu_worker`
  (new .env keys: AKKI_RMS_ESTATE_CSV, AKKI_CENSUS_CONNECTOR_DIR,
  AKKI_CENSUS_WORKER_STATE_DIR, AKKI_RMS_MYSQL_PORT). Only 5-line additive change
  to operational_runner.py (mode selector; remote_dispatch remains default). No
  sealed engine/scheduler/store/validator/registry rebuilt. E1 pod never the data
  path — DB I/O runs only in the spawned worker subprocess.
- GENUINE estate read (RMS tenant, source rms_mysql, counts only, no rows/PII):
  connected host Razuna/Newsvault read live → 2 databases (news_vault, razuna),
  119 tables, 2,198,643 estimated rows. 6 other RMS MySQL hosts isolated as
  not-yet-connected ("NOT YET UHURU") / IP-restricted — partial estate never
  blocks the read. Full HTTP journey POST /api/portal/census/run → COMPLETE,
  tenant-scoped, execution_verified=true, signed proof receipt on disk.
  Cross-tenant isolation verified (RMS run invisible to DIGICOW principal).
- 723 backend tests pass (710 existing + 13 new non-GPU worker tests), 17 gated
  skips, 0 failures. No regressions.

BLOCKED ON OWNER (not code): DigiCow — the attached workbook is byte-identical to
before and contains only ARNs (region, cluster ARN, secret ARN, db names), NOT an
AWS credential. Resolver refuses cleanly (NATIVE_SECRET_RESOLVER_UNAVAILABLE)
until AWS access key with secretsmanager:GetSecretValue OR resolved
endpoint/user/pass is supplied. RMS OBS/NAS need OBS/CIFS drivers (next slices).

ROADMAP + NAMED GAPS (answers owner's % demand):
`assessment_workspace/notes/non_gpu_worker_20260928/ROADMAP_AND_GAPS.md` +
`PROGRESS_MODEL.json`. Denominator = 648 assessed rows / 56 families. Two axes:
architecture ~47%; live-verified ~1% before this session (all positive
provider/source results were SYNTHETIC/MOCKED) — Area A now off zero (first live
evidence). 8 named areas with rows / architecture% / share-of-remaining:
A Ingestion 93/51%/13% (STARTED live), B Core-promise 92/38%/17%,
C Execution/model 63/37%/12%, D Memory/Watch 30/56%/4%,
E Governance/security 116/54%/15%, F Entitlements/commercial 58/55%/8%,
G Rules/amendments/decision-engines 149/42%/25% (incl. 24 source-unresolved + 5
spec-decision), H Principals/tenancy/continuity 47/52%/7%. Biggest levers: G then
B. P0 = finish Area A live ingestion (remaining RMS hosts, DigiCow when creds,
OBS/NAS drivers, live DQ/content-registry producers).


## CURRENT checkpoint — 2026-09-28 05:23 UTC, requirement-led designer brief/intake

Latest user instructions supersede HTML-placement briefs:
**“Connection is per Registry journey and requirements - this is read only link
that census will use and later extraction for the specific.”**
**“For the brief - dont write against my html. Write against what it is, does etc
(seasoned brief to a UI UX designer), according to your vision, not where it is
supposed to be.”** All backend/integrations must finish against established
requirements, with testing following—not define completion by passing tests. User
asks overall%progress. Do not infer that current backend is fully integrated.

Delivered standalone designer brief:
- `assessment_workspace/notes/designer_handoff_20260928/AKKI_EXPERIENCE_BRIEF.md`:
  product promise/personas,14outcome-based capabilities with stories/journeys/
  experience requirements/acceptance,7complete representativejourneys,5additional
  valueproposals, state/error/recovery/accessibility/performance and deliverables.
  It does NOT prescribe screen placement or a new architecture. Machine-purpose
  components explicitly stay behind human-readable outcomes.
- Public downloads: `/briefs/Akki_Designer_Brief.docx`, `/briefs/Akki_Designer_Brief.md`,
  `/briefs/Akki_Build_Status.md`. Export contains no credentials/ARNs/endpoints/source
  account values. Wordfilechecked; Markdown matches authoritativebrief/status.
- Separate `BUILD_STATUS.md` and `PROGRESS_EVIDENCE.json`: **overallcompletionpercent
  remains NOT ESTABLISHED/null**, not0/notanestimate.26Sept648-rowassessment is
  historical475partial128unverified24sourceunresolved13scopedevidenced7decision1nonclaim
  across56families; it is not currentclosure.13scoped rows are not13completefeatures;
  no2%/75%/80%or90%completionclaim. Laterworkneedsfullrowreconciliation and adopted
  denominator/closureevidence. This is a real reporting gap, not absenceofallwork.

Owner-supplied credential inputs handled OFFLINE only:
- RMS CREDS3.csv andDigicow.xlsx staged under
  `/app/backend/estate_keys/owner_20260928/`,both0600andgitignored; no source secrets
  inreport/transcript/frontend. Originalartifacts retained; no key/accountrotation.
- RMS shape:8endpoint/account/secret-shapedrows,1endpointmissingaccount/secret.
  Not8verifiedMySQLconnections. No scopeclassification inferred fromlayout, no
  hiddenfallback tooldercredentials for incompletefields.
- Digicow workbook containsregion,clusterARN,secretARN,database-nameref; shape/
  account/regionconsistent. It is connectionreferences, NOTadataestatepayload.
  It doesnotprovide nativeAWSidentity authorised toresolve the secret.
- `estate_intake_20260928.py` emits only custodyhashes/counts/booleans/knownfieldnames;
  it has no network, Registrywrites, admission or source-read path. Report
  `CONNECTION_INTAKE.json` explicitlyfalse forregistered/admitted/connected/census/
  extraction/GPU. Fileprotectionsandbadshape/duplicate/mismatch/reporttests added.

Current runtime blocker independentlyverified: readonly
`/api/portal/activation/runtime` returns **configured=false,NATIVE_BINDINGS_UNBOUND**.
Existingcensusremote_dispatch routes viaparkedconfiguredSSHhosts; no admitted
nonGPUworker/nativefactory/credentialresolverestablished. DO NOT runcensusPOST or
useworkspaceDB/S3/SSH to“finish”connections. E1neverdatapath. Requireddependencyis
access toadmitted nativeingestionworker outsideE1 plus its source/network/secret
authority. Repositoryavailabilityaloneisnotadmission/connectioncompletion.

Verified independent53: **712backendpassed,2gatedskips**;31unchangedfrontendlastpass.
New7tests are offlineintake/documentchecks, NOTliveintegrationprogress. Public3files
200actualpayloads/Wordvalid,reportcountsconsistent,ruffFclean,unchangedappsmokeOK.
No productionUI/API/authbehaviorchanged, noauthcredentialscreated/modified, no
sourceconnection/GPU/SSH/nativeeffect/holisticacceptance attempted. Positive broader
provider/authorityfixtures remain **SYNTHETIC/MOCKED**. Reportiteration53.

NextP0: nativeRegistry/worker/credentialbinding and current648-rowclosureledger;
finish source/extraction/answers/custody and durabletask/goal/team/Board/Watch flows.
P1: commercial/withdrawal/memory/witness/recoveryeffects and matched-quality/latency
verification. P2: source/supplementreleaseclosure and ownerprioritisation of extra
V01–V05designopportunities. No claim allnonGPUdone; substantialintegration remains.

## Previous checkpoint — 2026-09-28 04:17 UTC, actual owner HTML adoption

User rejected invented/limited experience wrappers and supplied the new authoritative
`Nexus Bank AI Prototype Sep 2026 (standalone) (1).html`. Latest instruction:
**“Mostly the same - review attached. Your recommendationd are fine and approve
just integrate the appropriately without intoducing new architecture”**.
The five recommendations are now APPROVED for appropriate integration, not deferred.
No new experience architecture, product tiles, theme or fake feature data is authorised.

Source is preserved at `assessment_workspace/canon/prototypes/20260928_owner_nexus/`:
`nexus.html` SHA256 **0330a1712aad3b76dfe6f5e97207707fa35a1ed774a134313635a59ba0a67d3d**.
Parsed `__bundler/template` as data; prototype JavaScript and demo outcomes are NOT
executed/imported into production.8649markupnodes/898events are STRUCTURAL counts,
not feature-completion percentages. Compiled300KB literal source fragments retain
exact original subtrees; all earlier canonical HTML/generated templates unchanged.

Verified UI correction:
- Deleted custom OSFeatureViews/osFeatures replacement shells. Actual source My Work,
  Company Goals, Board, Grey Mirror/Watch and evidence-drawer subtrees now render in
  the existing app shell with existing product branding. This adoption is scoped to
  these affected areas, NOT a claim that all prototype apps have been implemented.
- Restored Today/My team/The work/Execution score/Sources & governance, plus approved
  nested Company Goals/Board. Restored original3-taskpreview, Viewall/search, full
  task workspace, intelligence rail and disclosures. No hidden dataset truncation.
- Source Board4views and filters, goal filters, Grey Mirror original views and
  nested Watch lanes retain their original layouts/controls. Missing feeds show
  unknown/unavailable state within those layouts, not substitute dead-end pages.
- Original header notice popup uses real held-work records (NOT invented Watch
  alerts); opens original drawer with exact reason/next action and task link.
  Session-only read markers do not resolve any Watch case. Fixed parent-slot36
  wiring, responsive popup bounds, Escape/focus return and account access.
- Original task intake keeps all4sourceprompts and11choiceoptions. Redundant second
  prototype rendering of the SAME intake is hidden. Local intake completion offers
  original return control labelled “Back to the work”. **Draft is UNSAVED, session-
  local, NOT submitted/scheduled, and no native write occurs.** No AI answers claimed.
- Preserved design tokens and original components; mobile statistic rows2×2, long
  text containment, original drawer/popover responsiveness and keyboard focus checked.
  No models, prompt policy, context budgets or backend execution limits downgraded.

Verification: **705backendpassed,2existinggatedskips,0fail/errors**; **31frontendtests
passed**. Independent52 plus final self-tests. Bell→originaldrawer reason/next action,
focus return,4-stage/intakechoices, return-to-work with ZERO native POSTs verified.
Desktop1920×800/mobile390×844: no horizontal overflow. Final references:
`test_reports/pytest/nexus_non_gpu_final.xml`, `nexus_frontend_final.log`,
`test_reports/iteration_52.json`, `iteration_52_resolution.json`.

Five enhancements are only PARTIALLY integrated: in-place blocker notices and scoped
work-record navigation function; goal-linked native delivery, genuine Watch actions,
cross-app AI/context handoffs and native streaming still require real services.
Prototype prompts/options and unknown-value UI are not proof of complete features.
Native task submission/save, team/goals/board/Watch feeds, source/model/custody effects,
DQ/repair/memory/recall, commercial/witness/recovery and original audit remain open.
No genuine native model-quality/latency benchmark, live certificate or final holistic
handoff acceptance run. Positive authority/provider tests remain **SYNTHETIC/MOCKED**.
GPU untouched; no credentials, auth architecture or native runtime factory changed.

Test52 auth-policy advisories are not reported as fixed: six failed logins do not
establish the authoritative throttle policy; the existing bearer-token flow has no
httpOnly session-cookie requirement established; wildcard/credential CORS alignment
remains a release-policy follow-up. No unsolicited auth redesign/security audit.
Details, source mappings and exact enhancement status:
`assessment_workspace/notes/nexus_owner_adoption_20260928/STATUS.md`.

## Previous checkpoint — 2026-09-28 02:45 UTC, hierarchy/performance/reliability

Latest user objective: complete pending non-GPU requirements before the holistic
component-handoff acceptance test; preserve model capability, responsiveness and
crisp owner-prototype UX. Circled components must not appear as standalone apps.
User approved **existing requirements/hierarchy first, five recommendations deferred**.
User's latest answer: **“1 - as recommended. 2 - there is no repository, setting up
the repository now”**. Do not ask for generic scope approval again.

Implemented and verified this continuation:
- Workstudio launcher contains Chat, Data Suite, Documents, My Work. My Team,
  Company Goals and Board are nested under My Work alongside Work records.
  Board retains the intended board-pack/minutes meaning, not a new kanban product.
- Grey Mirror contains The Watch, with State/Record/Under Watch/Decisions as its
  subviews. No separate Watch launcher or component tiles. Seven old deep links
  redirect to exact nested paths, preserving search/hash, back/forward and refresh.
- Original HTML and generated prototypes remain unchanged. Only application
  composition and scoped owner-style overrides changed. Placeholder developer
  scaffolding pages are bypassed; absent native team/goals/board/Watch records are
  explicitly unavailable, not fake populated features or zero activity claims.
- My Work row selection preserves `?request` across sibling views. Loading/failure
  is distinct from a successfully empty dataset; unavailable counts show dashes.
  Duplicate renderer IDs fixed, scoped replacement labels resolve safely without
  template literals/eval. Sign-in palette variables and margin-style warnings fixed.
- `useOperationalWork`: selecting a record fetches detail only, not list+allowance
  again. Refresh still rereads current records; delayed responses/logout/principal
  switches cannot expose previous rows/detail/terms. No global authority cache.
- Work list/detail use `work_snapshot.py`: **one fully verified canonical prefix
  rather than three** with identical scoped/redacted public projections. Integrity,
  current release checks and append-only semantics unchanged. This measures fewer
  reads, not a fabricated 3x wall-time/model-throughput improvement.
- Recurring503 finally traced to **binding entry with a CLOSED inherited request
  lease**, not a TTL or proved ledger contention. Added a fresh local request-scope
  boundary ONLY after current `census_identity` authentication. Old direct/copied
  contexts still fail, active nested identity substitution still fails, cancellation
  closes child contexts. No JWT/native admission/PrincipalV1/credential changes.
  Protected Canon/writer/control/prototype hash tests pass unchanged.

Final independent verification51: **694 backend passed,2 pre-existing gated skips,
0 failures/errors** (696 collected); **22 frontend tests passed**. Previously flaky
API suites passed three repeated rounds with no new binding503. Five explicit
closed-carrier/auth-failure/nesting/cancellation regression tests pass. Scoped F
lint passes. Tested loaded desktop/mobile UI with1,218 persisted demo work records:
selection/tab/history/refresh preserved, zero overflow/duplicate IDs/literal bindings.
Final margin cleanup self-test: zero shorthand warnings, margins0px, no overflow.
Reports: `test_reports/iteration_50.json`, `iteration_51.json`,
`iteration_51_resolution.json`, and `pytest/pytest_iteration_51_non_gpu.xml`.

**Still NOT complete:** native provider/source/query/custody connections and signed
records are absent. Team/goals/board/Watch data is not connected. No source/model
quality or end-to-end latency benchmark was possible; model config/prompts/context
budgets were not reduced. Positive authority/provider fixtures remain
**SYNTHETIC/MOCKED**; persisted demo held-work records are not estate execution proof.
GPU untouched. The requested final holistic component-handoff test was **NOT run**.
Repository availability alone will not satisfy admitted provider/effect evidence.

P0 next: inspect the repository/location when user supplies it; recover actual native
bindings and owning-service producers without routing bytes through E1. Complete
source-side DQ/repair/memory/recall effects and real source→registry→delivery/skill
flows. P1: full commercial/Watch/witness/recovery and source-backed experience tests.
P2: audit648/source-supplement closure and then owner-approved enhancements.
Optional CORS explicit-origin hardening and legacy App.js decomposition remain
maintenance notes, not completed security-review work. No security review requested.
Five deferred proposals and the holistic acceptance gate are documented in
`assessment_workspace/notes/non_gpu_hierarchy_20260928/CLOSURE.md`.

## Previous checkpoint — 2026-09-27 20:34 UTC, autonomous non-GPU governance

User repeated: **“Complete all non-GPU work in one autonomous go. Dont stop.”**
Scope approval is already granted; no further generic permission round. GPU/SSH
remained parked with no connection, credential, workbook, key or workload activity.
**This batch is verified, but all non-GPU work is NOT complete.**

Implemented:
- New `services/non_gpu_governance/` versioned metadata consumers enforce complete
  seven-family quality bitmap/population reconciliation, confirmed pack/snapshot
  joins, explicit unknown/flag/non-clean outcomes and no accuracy fabrication.
  This is NOT the actual seven-family source-side check/repair executor.
- Deterministic whole-unit context reconstruction with pinned frame/model/tokenizer,
  native measured token counts, rule order, per-class exclusions and ten highest
  excluded re-extraction handles. Quality/class ceilings remain distinct from rights.
- Signed native lineage/current-rights gate traverses descendants, rejects cycles/
  changed artifact identities and prevents reactivation of immutable withdrawn refs.
  It denies stale release; it does NOT execute recall notifications, deletion or
  replacement training, and it does not refund spent budgets.
- Native memory reload evidence checks publication ordering, original closed-run/
  principal, source hashes/lineage, recorded loss and inference/utterance ceilings.
  User-memory stays disabled. No memory bytes are compacted/reloaded through E1.
- Native coordinator composition enforces these gates at reserve/send/verify/
  publish/retrieve. Existing custody inherits result-retrieval gates. Current query
  GET repeats release checks after awaited grounding. Live startup verification and
  certificate-issuance route use `GovernedNativeEvidence`; legacy v1 LAB verification
  remains distinguishable and cannot alone satisfy that live route.
- `GET /api/portal/entitlement/billing?period=<existing-period-id>` returns principal-
  scoped usage lines only from canonical dispatch/meter/event joins; half-open periods,
  event-time prices, duplicate detection, no other-seat detail or silent fractional
  rounding. No second bill store or fiscal invoice issued; broader seats/period
  producers/rounding-policy cases remain open.
- Bounded contention backoff is an additive `ledger_writer/contention_control.py`
  adapter composed in InsertGuard. Initial direct edits to protected mongo_control
  and principal_control were removed byte-identically; original hashes/tests were
  NOT altered. Both full-prefix checks and conditional-head fencing remain intact.
  Payload-free diagnostic error codes added; no auth behavior/credentials changed.
- Pre-existing mobile header clipping corrected in existing CSS override: compact
  status badge hides as intended while account avatar/menu remains accessible.
  Original owner HTML, generated templates, desktop structure and styles unchanged.

Final verification: **684 backend passed, 2 pre-existing explicitly gated custody
drills skipped, 0 failures/errors; all 7 frontend tests pass.** Both GPU-direct suites
were explicitly excluded. New focused metadata/billing tests originally72; memory/
certificate/backoff extension adds10, total82 new tests. Scoped Ruff F checks pass.
Desktop1920×800/mobile390×844 screenshots: no overflow; mobile account menu opens.
Canonical evidence: `test_reports/pytest/non_gpu_governance_final.{xml,log}`,
`non_gpu_governance_frontend.log`, `iteration_49.json` and `iteration_49_resolution.json`.

Earlier full runs had intermittent app503 and external TCP timeouts. Final full
run and targeted33-test diagnostics passed. Retry contention was a hypothesis, not
a fully proven cause of every503; diagnostics remain to distinguish recurrence.
Do not change URLs to localhost or hide outages with relaxed test assertions.
Testing-agent suggestion to overwrite seeded admin passwords was intentionally
not adopted: no credential reset was requested and idempotent seed must preserve
existing account changes. Existing test_credentials.md remains current.

**Live reality:** no actual admitted native worker/query ingress/inspector/custody
provider was recovered/configured. Runtime remains unconfigured. Live billing read
correctly returns ORGANISATION_UNRESOLVED rather than fabricated credit/usage.
Positive signed authority/source/quality/context/memory observations remain
**SYNTHETIC/MOCKED test fixtures**, not live estate effects. No genuine source read,
warm answer, byte delivery, physical-host recovery or live certificate was issued.

Remaining P0: admitted provider/record recovery, genuine source→registry→delivery
and grounded skill proofs, actual DQ/repair/exception producers and memory effects.
P1: full commercial producer/period/seat semantics, Watch/witness/notification/
physical-host evidence and recall orchestration. P2: original source/supplemental
audit closure (24 source-bounded rows,509 mappings), remaining transformed/media
journeys and measured release acceptance. Do not call the648-row programme closed.
Details: `assessment_workspace/notes/non_gpu_governance_20260927/IMPLEMENTATION.md`.

## Previous implementation checkpoint — 2026-09-27

First autonomous control-plane implementation batch verified. Detailed result:
`assessment_workspace/notes/activation_controls_20260927/IMPLEMENTATION_RESULT.md`.

Implemented: hash-preserved owner policy bundle, versioned/fingerprinted validation
profile, bounded certificate consistency/chronology/reconciliation checks,
server-owned evidence-verification interface, fail-closed table-driven crossing
resolver, authenticated profile/validation APIs with native audit, portal history
and stop/retry/result-reference joins to the same execution coordinator. Immutable
deadline/scope/objective replay enforced; unsafe fabricated training descriptors removed.

New endpoints:
- `GET /api/portal/activation/profile`
- `POST /api/portal/activation/certificates/validate`

No certificate or admission issued by these endpoints. `execution_authorized=false`,
`certificate_issued=false`; output handles do not prove byte delivery
(`delivery_verified=false`). No default fake-positive provider installed.

**Final full backend tests:451 passed,0 failures/errors,2 explicitly gated custody/
identity/refusal drills skipped.** JUnit:
`/app/test_reports/pytest/pytest_activation_portal_final_full.xml`.
Positive signature/worker/inspector/authority verdicts are **MOCKED/SYNTHETIC** and
positive storage FAKE. Real API tests cover auth/scope/refusal and validation-audit
writes, not live source/model operations.9 protected and owner JSON hashes unchanged.

At that checkpoint, not complete: native signature/provenance/ref adapters, durable approval-group and
estate activation joins, runtime dimensional limits/reservations, genuine DQ/worker/
inspection/usage producers, native model descriptor/callable wiring, real training/
evaluation, actual custody delivery, certificate issuance and independent live proof.
See ROADMAP.md. Do not call the typed EvidenceVerdict interface real cryptographic
verification or infer that the14 readiness packages are complete.

## Previous checkpoint — 2026-09-27 combined activation continuation

User explicitly reconfirmed the combined scope (controls + real A/B/C proofs), not
separate approval per package. Engineering continued; GPU/SSH remained untouched.
**Control-plane batch verified; the complete live-path scope is NOT complete.**

Implemented and tested:
- Signed native control-receipt consumer using existing Watch Ed25519 verification
  primitive and canonical Ledger. Admitted signer/key/permissions must resolve from
  a SERVER-OWNED native admission bridge. No keys, accounts or trust roots installed.
- Frozen activation plans with owner `inputs.dial_versions` / `inputs.policy_versions`
  mappings, script/input commitments, independent approval groups/quorum/current
  decisions/revocation, allocation and already-admitted worker attestations.
- Native ComponentAuthority decision join and SAME-ledger atomic reservations with
  compare-and-append; unknown usage remains reserved; signed terminal reconciliation
  preserves overruns. Real two-client Mongo CAS tested in isolated SYNTHETIC tenants.
- Explicit BoundedEngineAdapter, pre-send signed runtime-limit ACK, operation/fence
  binding, bounded metadata calls, worker-side counter/deadline helper including
  termination and late-admission/wall-clock-rollback checks. The helper is NOT an
  installed remote hard supervisor or proof that a real workload was terminated.
- Concrete certificate verification joins for signatures, request/objective,
  native approvals/policies/registry/usage/reservation/termination, independent
  evidence, predeclared acceptance, prefix chronology and supersession. Recording
  an already signed certificate is proof-gated; E1 never signs as the owner.
- Model-proof consumers require anchored skill/context/refusal evidence and a
  separate completed native evaluation consuming the trained artifact, predeclared
  six-criterion mapping/thresholds/protected split and distinct release decision.
- Legacy training now captures one write-once effect/result; emit and close reuse
  it, uncertain/historical outcomes cannot silently retrain. Missing MOAC evaluation
  values are null / `not_measured`; no fabricated zero scores or automatic dummy
  admission ceremony. Mocked close produces no chargeable metering receipt.

New metadata endpoints under `/api/portal/activation`: `/receipts`, `/readiness`,
`/reservations/settle`, `/certificates/issue`. Existing profile/validate remain
diagnostics; current issuance endpoint holds with no admitted signer bridge.

**Canonical regression: 520 passed, 2 explicitly gated custody drills skipped,
0 failures/errors** (`test_reports/pytest/activation_combined_canonical.xml`).
Testing reports42/43, protected-hash checks, unchanged UI desktop smoke and scoped
Python lint pass. Original EngineAdapter contract preserved; extension is a subtype.
No auth credentials, .env settings, original GPU/SSH runtime or frontend files changed.

Evidence limits: full signed Path-A verification/issuance positive is SYNTHETIC on
FAKE ledger, not real source/retrieval proof. Signature math is real but signer
admissions, worker/evaluator observations and trainer test effects are **MOCKED /
SYNTHETIC**. Mongo concurrency alone is real storage evidence. No live certificate
issued; no complete native positive B/C chain tested. No real worker installed.

Recovery: initial real control ledger had DAP/execution-request/portal-view and
validation-audit events, **no activation approvals, allocations or worker records**.
Legacy local runner metadata contained4 mock-mode records (3 closed_rejected,
1 historical closed_adopted); no historical row was rewritten or treated as live.
This finding is local to this composition, not proof the original estate is offline.

Current binding gap: `activation_receipts`/admitted-key resolver, real worker RPCs,
native inspector/eligibility and model query transports are not installed in app
startup. `services.activation.composition.native_activation_bindings` is an explicit
composition factory, NOT a running integration. Do not replace missing native
admissions with fixture roots. Preserve ordinary auth and PrincipalV1 architecture.
Detailed result and required interfaces:
`assessment_workspace/notes/activation_combined_20260927/{RESULT,BINDING_SPEC}.md`.

## Previous checkpoint — 2026-09-27 native startup, recovery and disclosure

User authorised the next actions, backlog and suggested hold-reason enhancement
together, then explicitly said “Go ahead”. Completed the independently executable
engineering below; genuine effects still need an existing admitted native provider.

- Added opt-in FastAPI native runtime startup/shutdown and coherent, same-ledger
  `NativeRuntime`/`NativeExecutionBindings` validation. Async native PrincipalV1
  lookup is bounded and works through operation authority AND Mkondo receiver
  revalidation. No new identity store, account, key or admission is manufactured.
- `AKKI_NATIVE_RUNTIME_FACTORY` and `AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS` are
  optional SERVER configuration, not currently populated. Both absent performs
  no provider import/probe. Partial/invalid/wrong-ledger configurations fail closed.
  `/api/portal/activation/runtime` reports configuration only, never authorisation.
- Portal answering/training recovers an exact signed native descriptor matching
  frozen principal/tenant/objective/scope/operation/deadline. Missing descriptors
  append `descriptor_held` to the existing DAP ledger and return409; no fabricated
  model input handles. Provisioning/delivery remain distinct unbound operations.
- DAP/OS drawer shows safe reason codes, explanations/actions and receipt history
  inside the existing owner prototype elements. Unknown native errors/hidden
  identities are not echoed. No prototype HTML, CSS, layout or typography change.
- Durable `worker_outcome` locks definitive worker facts; legacy checkpoints remain
  readable. Conflicting terminal facts hold; equivalent/stale running replies
  reconcile instead of causing false failures. Crashes before portal-view writes
  expose retry/reconciliation, and late views cannot reopen a canonical terminal.
- Four real-Mongo fresh-process crash drills prove one simulated operation/fence,
  submit/effect/meter/completion across recovery. SAME HOST, MOCKED worker/authority/
  inspector; NOT genuine multi-host, source/model or custody-transfer qualification.
- FULL signed A/B/C native certificate verification/issuance LAB chains now pass,
  using actual NativeReceipts/NativeEvidence rather than fake verdict flags.
  Independent evaluation must itself have approved native plan, distinct admitted
  worker, bounded ACK/fence, reservation, metering/terms and terminal settlement.
  Parent/child/supporting evidence must precede the verifier head. Repeated usage
  units are summed rather than overwritten. Signatures/claims/fixtures are all
  explicitly SYNTHETIC; this is software evidence, not real execution.

**Final regression:565 passed,2 explicitly gated custody drills skipped,0 failures/
errors; all7 frontend tests pass.** Canonical JUnit/log:
`test_reports/pytest/native_continuation_verified.{xml,log}` (131.853s).
Reports44/45 and targeted hardening tests document findings/fixes. Desktop1920×800
and mobile390×844 tested the actual drawer with an existing1071-character objective
among hundreds of records; no horizontal overflow. Scoped Python lint passes.
Original frozen owner/Canon/EngineAdapter hash/shape tests remain green.

**Still held:** no actual admitted native provider/connection descriptor and signed
activation records recovered for this workspace. Startup code is connected, but
runtime configuration remains absent. No genuine A/B/C effects or live certificate
issued. No GPU/SSH action, source/model-data processing in E1, credential/env change
or account/auth-policy mutation. Physical cross-host drills remain pending an
admitted independent interface, not falsely satisfied by local processes.

Indispensable next input: the existing admitted non-GPU runtime/provider descriptor
(module:function OR owning service endpoint/credential REFERENCE), plus references
to existing signed activation/approval records. Do not mint replacement roots or
install test providers. This local absence does not establish original-estate health.
Details: `assessment_workspace/notes/native_continuation_20260927/RESULT.md` and
updated `activation_combined_20260927/BINDING_SPEC.md`.

## Workspace versus original live Akki

### CURRENT checkpoint — 2026-09-27 18:49 UTC, non-GPU continuation
User: “Proceed with everything else except GPU”, followed by “Proceed”. GPU/SSH
is parked again under this latest scope. No live GPU connection, workbook/key/
account change or workload was performed in this batch. Existing direct connector
configuration was left untouched; GPU connector tests excluded from this run.

Implemented:
- Durable per-tenant/principal/skill query intents with exact question/provisioning
  hashes, idempotency conflicts, separate query sessions and receipted history.
  No raw question, source data or answer bytes persist/execute through this flow.
- Existing signed native plans feed the unchanged skill_request builder/coordinator
  and original Keygrant/owner/scope/floor/crossing checks. Native answer release
  requires measured signed artifact/class/grounding, independently signed anchors
  and context-loss disclosure. Genuine OUT_OF_SCOPE refusals are distinct from
  administrative holds and must come from the admitted worker for this intent.
- Query status/replay revalidates current provisioning and admission; changed
  corpus, withdrawn rights, missing runtime or expired evidence cannot re-expose
  historical ready artifact references. Gates repeat after awaited native work.
- Typed native custody-delivery adapter, explicit origin/expiry/recipient/artifact
  bounds, one dispatch per idempotency key and status-only uncertainty recovery.
  Capability URLs never enter Ledger/log/history. E1 never fetches/streams bytes.
  Issuance of a URL is NOT completion: exact-byte/hash signed terminal proof is
  required, including legal redemption chronology and current rights. Completed
  past delivery remains auditable after link expiry without restoring the link.
- Custody intent/grant/uncertainty/completion joins existing WorkView/history.
  Partial delivery never marks the whole result delivered: all expected artifacts
  must have completion evidence. Existing four-key result-response contract kept.
  No prototype HTML/CSS, page layout or new UI control was added; native APIs and
  existing DAP/OS receipt history are wired. Provider query-ingress/provisioning
  and real transports are not invented by this work.

New endpoints: `/api/callable_skill/{id}/query-intents`, `/queries/{query_id}`,
`/queries/{query_id}/advance`, `/queries/{query_id}/delivery`,
`/queries/{query_id}/deliveries/{delivery_id}`; source request delivery equivalents
under `/api/portal/requests/{request_id}/delivery` and `/deliveries/{delivery_id}`.
Existing skill `/query` upgrades only when a native runtime and Idempotency-Key
are present; without one it still records the original safe409 refusal.

**Final verification:602 non-GPU backend tests passed,2 pre-existing explicitly
gated custody drills skipped,0 failures/errors (64.635s); all7 frontend tests pass.**
Evidence: `test_reports/pytest/non_gpu_verified.{xml,log}`, report48 and its main-
agent resolution. Scoped Python lint passes. Actual drawer with1083-character
objective among971 requests checked at1920×800 and390×844: zero overflow.

Public API reality: authenticated native runtime status200 reports configured=false,
custody_delivery_bound=false, skill_query_execution_bound=false, worker_paths_bound=[],
execution_authorized=false/live_proof_verified=false. Anonymous new routes401.
**All positive custody/grounded-answer/receipt fixtures are SYNTHETIC/MOCKED; no
genuine source read, grounded answer, byte delivery or live certificate was issued.**
Signatures and ledger contracts are real test mechanics, not native provider access.

Remaining: actual admitted non-GPU query ingress/execution/inspector/custody
bindings and signed controls, then genuine bounded A/B proofs, usage/retrieval
reconciliation and certificates. Native provisioning and physical-host recovery
qualification remain pending genuine interfaces. Do not process data in E1 or
substitute test roots/Tigris credentials for these missing admissions.
Details: `assessment_workspace/notes/non_gpu_queries_delivery_20260927/{RESULT,NATIVE_PORTS}.md`.

### Latest active connection decision — 2026-09-27 17:47 UTC
Owner supplied NEW GPU CREDs.xlsx and explicitly overrode old CLIENT-admission
dependency: fresh direct login from that workbook, no rotation/administrative
changes; connection first. Historical audit may remain but cannot gate login.

Implemented `services.gpu_direct` workbook-only password seam. Both active runner
and census connection entrypoints select it through explicit
`AKKI_GPU_CONNECTION_MODE=direct_workbook`; endpoint/user/password and inventory
come from the new workbook, NEVER historical client key/receipt or fallback.
Non-secret connector path/port/timeout added to existing backend.env and backend
restarted. Existing initial keys retained but old client values are inactive in
this connector. No GPU credentials changed, no account/key created. Custody path
and digest are in test_credentials.md (NO password values). SERVER endpoint
verification remains separate, passed for both targets, and did not block login.

ACTUAL direct auth result17:47:10–17:47:14UTC: both SSH servers reachable/pinned,
one password auth call each, both replied `DIRECT_PASSWORD_METHOD_NOT_ALLOWED`
with `allowed_methods=[publickey]`. No old CLIENT key checks ran. No authenticated
session, shell/workload or key fallback. This does NOT establish wrong passwords;
the password method itself was rejected. Do not report this as local key mismatch.

Report47/live receipts under
`phase0/drill_receipts/20260927T174710Z_gpu_direct_workbook/`.13targeted offline
MOCKED tests pass, including proving both active entrypoints never invoke old
identity verification and cannot fall back on direct failure. Final full-suite:
**578 passed,2 existing explicitly gated custody drills skipped,0 failures/errors**
in116.234s; `test_reports/pytest/gpu_direct_full_regression.xml`. Active configured
inventory check with networking blocked reports password auth and no client-key
path for either target. Restarted backend responds401 on the authenticated profile
route when accessed anonymously, as expected. Details:
`notes/census_operational_v1/DIRECT_WORKBOOK_CONNECTION_20260927.md`.

Next required connection detail: provider's actual Connect command/instructions,
not a generic request for an integration design. Workbook contains passwords but
the SSH listeners offer publickey only; determine intended console/SSH route from
the provider's supplied instructions. No blind retries, pin rewrites, server auth
changes or generated identities. Connection/workload still not successful.

### 2026-09-27 17:33 UTC — newly requested GPU connection check
User asked whether other work is complete and explicitly requested a GPU connection
attempt. This authorised one read-only diagnostic per configured host, NOT a
workload, key replacement, identity-guard bypass or recurring retries. Prior parked
status was lifted only for this diagnostic; the attempt has now been consumed.

Both `akki-vm` and `akki-vm-ii` accepted TCP/SSH negotiation and matched their saved
SERVER identity pins. Both failed original LOCAL client-key admission with
`IDENTITY_PIN_MISMATCH`. Therefore zero key-auth calls were made; `auth_none`
discovery alone returned `publickey` as the supported method. Neither authenticated.
No session/channel/remote command/GPU workload ran. Protected key, known-hosts,
environment and identity/dispatch code hashes remained unchanged.

Evidence: `/app/test_reports/iteration_46.json` and
`assessment_workspace/phase0/drill_receipts/20260927T173352Z_gpu_connection_diag_once/`.
Interpretation correction: `notes/census_operational_v1/GPU_RECHECK_20260927.md`.
Do NOT follow advice to merely repin the currently available mismatched key.
Remote `authorized_keys` were not inspected. Today's result does not establish
remote key rejection or GPU health; Sept26 key rejection remains HISTORICAL.
Neither old nor new key's current remote authorisation is established by this test.

Plain status: engineering controls/recovery/UI improvements are tested, but NOT
all work is complete. Genuine source/skill/training/evaluation/retrieval proofs,
live certificates and independent-host qualification remain outstanding. A/B/C
positive lab evidence is SYNTHETIC/MOCKED. Next safe access step is to recover the
originally admitted key/runtime connection through its existing custody/admin,
without changing working original infrastructure or requesting private keys in chat.

Owner reports original runtime live on amazing-gates-8. Current configured workspace
is pensive-goodall-6 and uses local credentials/vendored code, not inherited sessions.
Read-only comparison: `notes/workspace_repo_connection_review/REVIEW.md` under
assessment_workspace. Git origin is Akki-OS-Root; remote read failed, so latest owner
push NOT verified. The apparent Extraction-Akki directory has no own backend/git.
Local key/receipt file presence is not proof of authorisation or connection.
Original real-training records are historical; current original health unobserved.
Current unbound findings concern this new activation composition, not a claim that
the entire original estate is mocked/disconnected. No new GPU/SSH action performed.

## Continuity and next work

- `CHANGELOG.md`: implemented changes/testing, with links to durable evidence.
- `ROADMAP.md`: R01–R14 progress, next slice, P1/P2 backlog.
- `ARCHIVE_PRD_BEFORE_ACTIVATION_CONTROLS.md`: complete previous699-line record.
- Original fix plan: `assessment_workspace/notes/consolidated_fix_plan_20260926/`.
- Owner artifacts/review: `notes/live_activation_v1_3_artifact_review/revision_v1_1/`.
- Readiness register: `notes/live_activation_v1_3_readiness/READINESS_REGISTER.md`.
- Existing auth credentials: `/app/memory/test_credentials.md`; unchanged this batch.

Next: obtain/recover the actual admitted native provider descriptor and signed
activation records, connect its existing worker/inspector/eligibility transports,
then run real bounded A→B→C proofs and physical-host recovery wherever admitted.
Complete any provider-specific provisioning/delivery glue from those actual
contracts, not invented interfaces. GPU/SSH remains parked. No further generic
approval of the combined scope is needed; only indispensable native binding input.