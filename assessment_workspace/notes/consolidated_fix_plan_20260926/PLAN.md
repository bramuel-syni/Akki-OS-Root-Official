# Akki — consolidated, dependency-ordered fix plan

Date: 2026-09-26. Status: **PLAN FOR OWNER REVIEW; IMPLEMENTATION NOT AUTHORIZED BY THIS TURN.**

## 1. Authorization and purpose

Owner request: “As we wait for response, lets continue with the earlier plan - based on your analysis, can you formulat a fix plan for all areas flagged including what we were initially working with?”

The accepted clarification was: “I’ll formulate a consolidated fix plan—not implement it yet—covering the original DAP/request–work–result work, all flagged requirement and promise areas, EX/DQ/CC, and remaining audit/source gaps.” Owner replied: “Works. Proceed”.

The current owner's clarification confirms that this approval is for **formulation, not implementation**. It supersedes the fork handoff's incorrect instruction to begin Step 1 immediately. This document does not ratify Canon, pin a build objective, grant admission, change a runtime state, or authorize infrastructure access.

Deliverable: one programme reusing the existing components, with dependencies, concrete corrections, acceptance evidence, decision/external blockers, and explicit completion boundaries. Documentation is the only changed material in this task.

## 2. Evidence baseline — preserve, do not rebuild or inflate

- The 648 requirement rows across 56 families and S-1–S-35 are accounted for in the earlier assessment. Its dispositions remain 475 PARTIAL, 128 UNVERIFIED, 24 SOURCE_UNRESOLVED, 7 SPEC_DECISION_REQUIRED, 1 EXPLICIT_NONCLAIM, 13 EVIDENCED_SCOPED. These are not delivery percentages.
- The 509 outstanding semantic links among 848 supplemental blocks, the 24 source-bounded cases, generic acceptance wording, SFP concatenation and product-promise crosswalk gaps remain **open analysis work**. Writing this plan does not close them.
- DAP commissioning, immutable intent, replay, shared held-work history, honest action refusals and ledger-derived entitlement reads are foundations already verified in a bounded slice. D01–D12 remain **4 verified / 7 partial / 1 open**, not a completed user journey.
- Prior 146 passed / 2 intentionally skipped tests were dated, scoped evidence. Positive entitlement/admission cases and some executor tests were **MOCKED / TEST-ONLY**. They are not real approvals, charges or successful source execution.
- Census has a real refused-run record and canonical RECEIPT-asset integration. Fresh real source execution gate T14 remains blocked. A RECEIPT asset is not complete source characterisation.
- Callable-skill caller-supplied answers were removed; the current unadmitted-executor refusal is intentional. A real callable executor remains unwired. Some training/evaluation criteria are explicitly MOCKED; do not label every historical training path mocked.
- AISCA access is parked. Recorded current-key public-key authentication failed on both hosts with server pins matched. This does not establish provider fault, remote authorized_keys contents, or broken GPUs. No new SSH, portal, key, VM or provider operation belongs to this plan.

### Source of truth

All paths are under `/app/`:

1. `assessment_workspace/notes/full_requirements_gap_20260926/REPORT.md`, `REQUIREMENT_GAPS_648.json`, `PROMISE_GAPS_35.json`, `SUPPLEMENTAL_RECONCILIATION.json`, `FAMILY_COVERAGE_56.json`, `PRODUCT_PROMISE_CROSSWALK.json`.
2. `assessment_workspace/notes/enhancement_specs_20260926/INTEGRATION_REVIEW.md`, including §§4 and 8; its 59-row combined map and source extracts. The later full-gap report's R32 and offline-revocation corrections take precedence over stale review wording.
3. `assessment_workspace/notes/census_operational_v1/COMPONENT_WORK_LEDGER.md`.
4. `assessment_workspace/notes/dap_operational_v1/VERIFICATION_REPORT.md` and `assessment_workspace/STATE/OBJECTIVES/CP_DAP_OPERATIONAL_V1.md`.
5. `memory/PRD.md`; `test_reports/iteration_10.json` through `iteration_14.json`, retaining each report's original scope.

`COVERAGE.md` routes every assessment family, every assurance promise and the original DAP acceptance set into this programme. It is a planning index, not a replacement row-level semantic assessment. `DECISION_AND_BLOCKER_REGISTER.md` preserves the earlier decision questions individually.

## 3. Constraints applying to every package

1. E1 wires descriptors and control-plane composition; **Akki infrastructure alone executes estate reads, training and governed workloads**. No pod fallback, local extraction, synthetic source-success receipt or invented admission.
2. Reuse existing authorities, sealed contracts and state machines. Versioned adapters/sidecars only where permitted; a required sealed change needs its own governed authorization. Keep the canonical 17-field Ledger row intact. No competing registries, policy stores or balance stores.
3. Governing effects require their proper authenticated admitted principal, scope, version and durable authority. A JWT or owner-looking string is not admission. Async work and Mkondo handoffs cannot widen the frozen objective or acquire a second authority.
4. Preserve append-only history. Interruptions leave the previous valid effective state or a fully admitted successor; they never justify deleting Ledger rows. A failed write cannot be described as a committed refusal receipt if no authoritative commit occurred.
5. Preserve literal owner prototypes, architecture, DOM/layout and styling. Wire existing controls and registered content only. Do not replace held states, unavailable values or unmeasured quantities with invented success/zeros.
6. EX is an execution/evidence discipline; DQ is check-bound eligibility; CC is custody/context and measured cost. None substitutes for rights, evidence class, capability admission, commercial terms or security authority.
7. A positive outcome and its negative/failure cases must both be proved. An all-refused run can reconcile its denominator without delivering the promised useful result.
8. Priorities sequence work, **not permission to defer a mandatory gate**. Required custody, Watch, rights, quality, release-budget and withdrawal controls are prerequisites for whichever slice uses them.

## 4. Dependency order and parallel work

The W0–W9 labels from the gap report are retained. Cross-cutting packages are split into early prerequisites and later breadth so the original ordering cannot accidentally put entitlement or DQ after the operation they govern.

`W0(scope)` means the relevant source, authority and acceptance subset has been resolved. It does not assert all 509 links or all Canon are closed. Unrelated source gaps may remain explicitly held without blocking already-authoritative work.

| Gate ID | Depends on | Concrete exit |
|---|---|---|
| W0 | Planning approval for future execution of this package | Relevant authoritative clauses, mappings, acceptance population and decision disposition |
| W9a | W0(scope) | Protected benchmark/measurement protocol and held-out custody pinned before tuning |
| W1 | W0(scope) | Admitted identities, custody, handoffs and authoritative effectiveness for the selected boundary inventory |
| W5a | W1, W0(scope) | Actual licence/catalog/terms/operation-right producers and safe metering prerequisite |
| W6a | W1, W0(scope) | Required observation, containment, output and aggregate-release gates for the selected operation |
| W7a | W1, W0(scope) | Source-to-descendant lineage and immediate eligibility invalidation before artifacts are released |
| W2 | W1, W5a, W6a, W7a, W0(scope) | Real admitted source → reconciled population → validated canonical registry outcome |
| W3 | W2, W5a, W6a, W7a, W0(scope); W5b when the selected operation consumes quality-qualified material | Real approved DAP request → operation → metered verified artifact → authorized retrieval |
| W5b | W2, W1, W0(scope) | DQ assessment/consumer gates and broader entitlement concurrency/period correctness |
| W4 | W3, W5b, W7a, W0(scope) | Actual qualified warm answer, reproducible window/loss and class-preserving memory |
| W6b | W6a, W1, W0(scope) | Full operational Watch/governance, independent witnessing and timed resilience evidence |
| W7b | W2, W5a, W5b, W6a, W7a, W9a, W0(scope) | Actual evaluated/trained artifact, admitted serving and descendant withdrawal |
| W8 | W3, W4, W5b, W7a, W0(scope); W7b for trained/model-dependent outputs | Real media/voice, skill, report/deck and transformed artifacts with applicable gates |
| W9b | W1, W2, W3, W4, W5a, W5b, W6a, W6b, W7a, W7b, W8, W9a for a whole-platform claim; exact applicable subset for a bounded claim | Full prototype/content coverage and honest capability/performance release evidence |

This is an acceptance dependency graph, **not an invented serial component call graph**. W5a/W6a/W7a can proceed together once W1 is established. W6b need not wait for warm answers. W9a is early, not after training. W5b's commercial work independent of a source may proceed with W5a; its actual DQ proof needs W2's source snapshot.

The named first operation and its exact gate applicability must be pinned in W0. If that operation consumes DQ-qualified material, its W5b eligibility gate moves **before W3 execution**, not after it. Acquiring a source snapshot in W2 does not itself admit those records for training or factual anchoring.

Work available while GPU remains parked: source/ruling reconciliation, exact closure contracts, control-plane producer/consumer repairs, deterministic gate and fault/concurrency tests, content/journey mapping and protected measurement design. Future implementation still needs approval. Unit fixtures can support engineering readiness but cannot pass W2/W3/W4/W7b/W8 operational exits.

## 5. Work packages

### W0 — close audit, source and authority gaps (P0)

**Owners/components:** requirements/Canon custody, Rules Service authority records, Work Supervisor acceptance, component ledger. Input: banked source and assessment records. Output: versioned trace/closure register.

**Concrete work**
- Resolve all 509 supplemental links individually to registered clauses, genuine supplemental obligations, rulings, duplicates or declared limits, with source anchors and rationale; do not turn them into 509 features.
- Recover authoritative source wording/context for the 11 SV-extension clauses, 11 ROC clauses and DR-R10/DR-R13 from existing custody first. These are 24 source-bounded cases, not 24 missing documents. Request missing source only if still unavailable; preserve source-held findings instead of guessing text.
- Reconcile product-promise #5/#28/#29 without conflating them with S-N; repair SFP1–6 atomic linkage while preserving original workbook bytes and defects.
- Reconcile 648 registry / 602 QA (46 EX/DQ/CC additions), Build Status 635, Legend 286 and objective metadata. Proposed corrective derivatives are not silent edits to authoritative workbooks.
- Replace generic gap/acceptance wording with rule-specific positive, refusal, race and interruption evidence. Assign each exact `(Doc, Rule ID)` and supplemental obligation to a closure owner and gate. Preserve original assessment history and uncertainty.
- Resolve existing rulings before asking the owner; distinguish DEFAULT implementation declarations, genuine OWNER choices, missing sources and EP-5 nonclaim. Establish six-field EX contracts, protected acceptance access and an evidence/re-performance protocol for each opened package.

**Acceptance:** exact-key/literal-source integrity; every supplemental block has a supported disposition; complete separate product/S-promise crosswalk; trace from each obligation to its exact test/evidence and bounded claim. Unavailable sources are accounted-for holds, not audit closure. Independently check affected semantic mappings, retaining uncertainties.

**Boundary/dependencies:** work is documentary and can start without GPU after approval. EX adoption/R37 and source availability may constrain formal compliance claims. No current declaration that the all-Canon audit is finished.

### W1 — admitted identity, custody and durable effective governance (P0)

**Owners/components:** principal model/credential plane, SyniSense/Shield/chokepoint, Northena, Mkondo, Ledger emitter/writer, Rules Service/registry. Input: admitted principal + frozen objective/scope. Output: authorized, receipted effect or correct refusal.

**Concrete work**
- Enumerate every record producer, model/tool/estate crossing, async worker and internal consumer; bind server-authenticated admission and immutable task context. Remove caller/default actor paths, not legitimate historic records.
- Connect actual owner/delegated principal admission and governed credentials; enforce rotation, expiry, confirmed revocation and scope inheritance. Do not infer admission from existing demo membership or JWT alone.
- Preserve pre-mask intent, tenant entity coverage, approved input/output sequence, dual retained-file custody and exception-safe ephemeral mapping cleanup. Cover document/perception routes, not just text chat.
- Establish sole-invoker static checks plus actual runtime/network enforcement. The existence of a preferred wrapper is not sole-crossing proof.
- Bind each record class to its canonical producer; replace effect-authorizing best-effort behavior with an acknowledged authoritative boundary through permitted composition. Keep payload/hash/version relationships and restart-safe command idempotency.
- Complete rule/registry/Ledger/in-force commit decisions, predecessor versions and ceremony history. Readers use only effective admitted versions; failed/interrupted attempts remain distinguishable and later reconcilable. Governed handoff receipts precede receiver action.

**Acceptance:** spoofed/unadmitted and dual-authority tasks cannot write/act; admitted context survives queue/restart; side invocation cannot cross; forced exceptions retain no forbidden maps/log content. Kill/restart and race every effective-state transition; old state or fully committed successor only; no history deletion or unreceipted next gate.

**Boundary/dependencies:** W0(scope); exact authentication integration design must be obtained before later auth implementation. Local tests do not prove deployed egress isolation, secret custody or independent placement. CC disclosure/cache exceptions remain held pending applicable decisions; no guard bypass is authorized.

**Existing seams (paths relative to `/app/`):**
- `backend/vendored/extraction_akki/backend/services/chokepoint/llm.py`
- `backend/vendored/extraction_akki/backend/services/enforce/census_identity.py`
- `backend/vendored/extraction_akki/backend/services/ledger_writer/mongo_control.py`
- `backend/vendored/extraction_akki/backend/services/ledger_emitter/emit_intent.py`
- `backend/vendored/extraction_akki/backend/services/mkondo/registry.py`
- `backend/vendored/extraction_akki/backend/services/rules_service/ceremony.py`
- `backend/vendored/extraction_akki/backend/contracts/ledger_v1.py`

### W5a — licence, terms and metering prerequisites (P0 part of W5)

**Owners/components:** entitlement service, owner/principal admission, catalog/credential facility, Northena, chokepoint and Ledger. Input: admitted organisation/operation/route. Output: effective terms, route eligibility and consumption authority.

**Concrete work:** connect real membership/licence/catalog/price/approval producers to existing projections; bind disclosure to the immutable operation and terms version; protect own-key credentials in the governed facility; apply custody eligibility before preference/cascade. Establish concurrency-safe capacity reservation/commit and actual-consumption settlement per governing semantics. A planned reservation is not a measured charge, and no actual quantities may be invented before execution.

**Acceptance:** missing/expired/suspended/revoked/dial-excluded terms refuse; quote-to-execution terms changes cannot silently reprice; concurrent seat/allowance admissions cannot overspend; uncertain dispatch cannot duplicate an operation or charge. Local and Your Keys paths do not inherit reseller-only R24 holds; neither receives fabricated free grants.

**R24 scope:** reseller-frontier rows only. Local and Your Keys do not require R24 reseller agreements; all their own admission, custody and licence checks still apply.

**Boundary:** W1 + actual owner-admitted records; fixtures test logic only. This prerequisite moves before the first live operation. Broader periods/rollover belong to W5b.

### W6a — minimum operational security and release gates (P0 part of W6)

**Owners/components:** Watch Macho/Mkono, identity/party lineage, output/distance/release-budget gates and Ledger. Input: the selected operation's complete boundary inventory. Output: applicable independent observation and admitted enforcement.

**Concrete work:** attach real input observations to verdict/evidence and signed action policy; preserve detection/response separation; establish independent custody failure posture, truthful mirage marking where used, agent ceilings and relevant per-party/estate cumulative budgets. Bind every component output to controlled-content inspection and advisory tagging; govern distance/DP requirements for relevant artifact egress. Only demonstrated/admitted rails may be in force.

**Acceptance:** missing observer/certificate/config or failed authoritative write blocks the affected operation; suspicion/finding volume cannot become severance; concurrent principals cannot bypass a common party or estate ceiling; no release before required output checks. Disable Watch and verify independent custody refusal and retained containment, respecting specific safe-open read exceptions.

**Boundary:** W1 + applicable ruled thresholds/admissions. W6b supplies broad and timed operational demonstrations; no mandatory requirement is waived while waiting for it.

### W7a — lineage and withdrawal prerequisites (P0 part of W7)

**Owners/components:** Mtafiti registry, qualified units, artifact manifests, memory/retention, request/result readers. Input: source/version/rights references. Output: queryable derivation lineage and denied stale eligibility.

**Concrete work:** persist source→unit→artifact/version relationships; recheck rights at handoff/retrieval/serve; prevent queued work from publishing valid descendants after withdrawal; record recall/notice or re-derivation requirements. Do not give Watch deletion authority, erase evidence, or refund spent privacy budget.

**Acceptance:** withdrawal during queue/run/publication/retrieval invalidates every affected descendant; stale caches/jobs cannot re-admit it. Separately authorized erasure remains distinct from quality classification or security containment.

**Boundary:** W1 + scope-specific rights/retention policy. Early refusal/recall capability must precede release; full model retraining/unlearning is W7b, with unsharded R12 choices explicit.

### W2 — real bounded source to canonical registry (P0)

**Owners/components:** Connect/Source Plane, Census Autonomy, admitted Akki executor, Mtafiti, Mkondo, OS/DAP projections. Input: owner-admitted source descriptor and frozen scope. Output: a real validated registry outcome and receipts.

**Concrete work:** select one lawful source/population; pin snapshot or watermark, member identities, exclusions and credential references. Verify the admitted remote worker and connector custody through the existing execution path. Enumerate and reconcile exact members; make shard retries idempotent. Store validated artifacts and measured metadata through the canonical Mtafiti writer; receipt-class registration alone is insufficient. Unavailable members remain unavailable/unmeasured, never empty.

**Acceptance:** real Akki-side execution accounts for the pinned population, independently checks artifact/member identity, persists/reloads the canonical outcome, and presents the same evidence in OS and DAP. Retry, source churn, unreachable members and register/Ledger failure cannot publish false completion.

**Boundary:** W1/W5a/W6a/W7a and actual admitted source/compute. Existing AISCA path is **externally blocked and parked**. No alternative host is presumed admitted. CPU-suitable work still requires Akki-side infrastructure. Passing fixtures cannot pass T14; a metadata-only slice does not claim record-level DQ, full semantics or all Mtafiti duties.

### W3 — original DAP request–work–result journey (P0)

**Owners/components:** Northena, DAP lifecycle, Work Supervisor/executor, entitlement/Ledger, result registry/retrieval, OS/DAP. Input: immutable commissioned request. Output: approved real operation, measured consumption and verified retrievable artifact.

**Concrete work:** retain existing durable request/replay. Add operation-right resolution and recorded terms; obtain the required independent approval over exact objective/units/expiry. Dispatch exclusively to the admitted executor; project actual receipts through legal lifecycle edges. Meter actual work under disclosed event-time terms. Cancellation requires executor acknowledgement/outcome reconciliation; retry preserves frozen scope, reruns gates, uses still-valid approval and respects the existing bound of three. Check checksum, artifact identity and current retrieval rights; reopening an existing report must not rebill. Keep approver identity out of party views.

**Acceptance:** one real commission→disclosure→approval→dispatch→meter→verified result→retrieval works and agrees across OS/DAP after reload. Denied/expired/widened, duplicate/timeout, stop-versus-complete, retry-versus-revoke and Ledger-failed variants cannot create unauthorized effects or double charges. Current Routing hold cannot be renamed success or moved through an invented Routing→Blocked edge.

**Boundary:** W2/W5a/W6a/W7a and the actual selected operation's prerequisites. Closes the remaining D03–D10 links for a named operation, not every DAP operation or all platform capabilities. Broader DAP browsing, quality, learning and transformed modes continue in their assigned packages.

**Existing seams (paths relative to `/app/`), plus the existing DAP state machine and original OS/DAP bindings:**
- `backend/vendored/extraction_akki/backend/services/northena/portal_work.py`
- `backend/vendored/extraction_akki/backend/services/portal_operational/access.py`
- `backend/vendored/extraction_akki/backend/services/portal_operational/actions.py`
- `backend/vendored/extraction_akki/backend/services/portal_operational/entitlements.py`
- `backend/vendored/extraction_akki/backend/services/portal_operational/models.py`
- `backend/vendored/extraction_akki/backend/services/portal_operational/skill_query.py`
- `backend/vendored/extraction_akki/backend/routers/portal_requests.py`
- `backend/vendored/extraction_akki/backend/routers/portal_entitlement.py`

### W5b — Data Cleanliness and full commercial correctness (P1; prerequisites pulled forward)

**Owners/components:** Mtafiti/check packs, Rules Service, Targeta, training/MOAC, Solva, memory, entitlement and Content Registry. Input: W2 snapshot + confirmed pack. Output: per-record evidence and enforced use eligibility, plus authoritative period accounting.

**Concrete work:** implement all seven check families and applicable media checks; owner-confirm sentinels/predicates/thresholds; pin related snapshots and comparison baselines. Persist pass/fail/not-assessed evidence, deterministic duplicate selection, strata and repair/recheck lineage through canonical custody. Apply the ruled incomplete-assessment/partition/exception predicate; zero configured checks never imply Clean. Enforce quality at actual training/fact-anchor/ranking consumers; preserve distinct quality/rights/defensibility classes. Version MOAC/class adapters lawfully. Complete event-time pricing, seats, pool ceilings, pauses, rollover, model ownership and invoice derivation.

**Acceptance:** exact population/coverage/strata reconciliation under agreed policy; structural/sentinel/unknown cases cannot acquire forbidden eligibility; repairs retain original failures and rechecks; changed packs/rights invalidate downstream caches. Consumer bypass and concurrent price/period/seat/exhaustion cases fail correctly; billing is reconstructible from authoritative events.

**Boundary:** W2 for real DQ proof; decision register E02–E12 as applicable. A small check pack is declared partial, not seven-family or S34 closure. Clean is not truth or permission. W5a commercial gates stay active from first execution.

### W4 — genuinely grounded warm answer and preserved context (P1)

**Owners/components:** Solva, Targeta, Context Manager/Service1, five-ring units, custody/chokepoint, memory/retention and content/output consumers. Input: objective + actually qualified permitted units. Output: useful grounded answer with reproducible context and losses.

**Concrete work:** resolve real unit/source handles; freeze pre-mask entity-knowledge classification and admitted local route; assemble whole units deterministically using pinned graph, model/tokenizer, frame/reserves and budget. Disclose real exclusions/handles without leaking protected text. Bind each factual claim and recommendation to permitted support, assumptions, contradictions and class ceilings; distinguish measured probability from unsupported numerical confidence. Publish compacted artifacts only after required receipts; verify reload hashes/classes, genuine re-extraction and revocation. Keep user-memory class disabled until its required ruling.

**Acceptance:** another permitted reader reconstructs window/order/exclusions; real supported request yields a useful answer. Missing/conflicting/revoked/Junk/insufficient support yields the correct marker/ceiling/refusal; no class inflation or silent unit split. Compaction commit failure does not expose an unreceipted derivative; reload does not revive withdrawn support. Measure true request timing and warm delivery, not an internal model timer or routing label.

**Boundary:** W3/W5b/W7a; CC classification, disclosure, assembly and taxonomy decisions. Approved external disclosure is a narrowly governed branch at the sole chokepoint, not a new invoker. No model call or bare experiment is authorized now.

### W6b — full Watch, governance and operational resilience (P1)

**Owners/components:** Watch/Macho/Mkono/Grey Mirror, CIF/Solva research, Rules Service, security/governance task identities, Ledger, independent witness and credential/rule infrastructure. Input: actual observations/ceremonies/incidents. Output: bounded enforceable response and independently verifiable continuity.

**Concrete work:** complete machine-speed/slow-play/authorized-pattern detection paths with evidence-only certificates; connect observation→proposal→grounding→independent ratification→versioned requirement without self-admission. Persist aggregate party/mandate budgets, raiser costs/drift, TTL and reversible action/attestation. Isolate mirage stores/credentials and idempotent authorized reconciliation. Demonstrate no-delete Watch, nonexportable profiles and fixed agent ceilings. Verify deployed trust domains/TCB/SoA and genuinely external witness. Complete signed rule-cache policy, credential freshness and exclusive fenced writer failover. Wire standing drills and actual incident notification/recovery through approved infrastructure.

**Acceptance:** every in-force response rail fires in its approved drill; forged/stale signals and uncertified suspicion cannot escalate; containment survives failure. Independent liveness/tamper detection works without Watch credentials. Actual Ledger continuity restoration demonstrates the 3,600-second bound with independent countersignature; qualifying notifications demonstrate required recipient delivery within 72 hours, including channel failure/retry. Concurrent amendment/failover cannot fork effective history or activate two writers.

**Boundary:** W6a/W1; true witness/replica/notification facilities, applicable thresholds/cadences, RPO and total-site-loss rulings. Timer constants or simulated clocks are not the timed operational proof. Report unavailable rule/credential/Ledger service as an outage even when refusal is correct. Do not assert a site-loss promise from single-writer recovery.

### W7b — real training, Targeta/CIF learning, serving and withdrawal (P2)

**Owners/components:** Targeta/CIF, training runner, WPW, MOAC/model admission, model registry/serving, pruning/unlearning and retention. Input: lawful qualified corpus/commission and admitted base artifact. Output: actually evaluated capability with faithful serving identity.

**Concrete work:** replace specifically MOCKED acceptance criteria with objective-specific experiments; inspect actual baseline provenance/licence and entering-model probes. Bind corpus/pack/rights and weight/config/engine hashes through training and acceptance. Measure yield, held-out robustness, refusal, generalisation and relevant latency. Preserve learner/proposer/grounder/ratifier separation and independent CIF halt. Apply required DP or expressly approved non-DP alternative and egress gates. Integrate WPW milestones/internal versus external report rules. Invalidate capability admissions on artifact change. Exercise serving-pressure integrity and source withdrawal across queued/train/serve/compaction/report descendants, with recall or independently accepted re-derivation.

**Acceptance:** a real admitted trained artifact passes real acceptance and serves its actual recorded identity. Fixed input/seed/parameters under allowed placement/load either preserve promised semantics or refuse—no silent model/precision/context substitution. Source withdrawal finds affected descendants, stops stale serving/releases and preserves spent privacy budget. Learners cannot ratify themselves or expand reach through learned ranking.

**Boundary:** W2/W5a/W5b/W6a/W7a/W9a + admitted compute/corpora and thresholds. Serving floor's stated frontier-gateway limitation remains explicit; provider provenance does not prove local exact-token semantics. Genuine prior runs are not discarded, and a CI fixture is not production acceptance. R12 and other owner-class decisions stay scoped holds.

### W8 — audio/voice, callable skills and real transformed outputs (P2)

**Owners/components:** audio/media/voice/language planes, skill executor/provisioning, transform forms/report/deck engine, Solva/output gates, registry and retrieval. Input: admitted source/artifact or qualified skill query. Output: actually usable, verified media/skill/report/deck artifact.

**Concrete work:** establish deterministic media integrity, admitted corpora and actual acoustic/source-identity distance, exclusion/authorization, intelligibility and language/register/latency experiments. Preserve useful condition variants rather than indiscriminate deduplication. Recover SV obligations before making stream claims. Connect real skills through the admitted executor and frozen provisioning scope, not caller answers/classes. Resolve conditional fresh/async skill contracts before exposing them. Materialize and validate reports/decks via the existing backend engine; retain backend-only/parallel-safe build constraints, attachment/class/distance/retrieval controls and DQ/CC losses. Do not invent DR-R10/13.

**Acceptance:** actual media outputs meet the admitted integrity/protection/capability criteria; actual skill calls return grounded results and refuse widened/withdrawn scope. Rendered reports/decks exist, open correctly and match admitted content/artifact hashes. Missing source, threshold, approval or executor gives truthful unavailable/refusal, not metadata-only success.

**Boundary:** W3/W4/W5b/W7a, W7b where trained artifacts are required, plus real admitted facilities and unresolved source/voice/threshold decisions. Registering a parameter or completing a job is not evidence of acoustic protection or usable rendering.

### W9a / W9b — prototype/content coverage and measured release proof (early + P2)

**Owners/components:** Content Registry, original OS/DAP bindings, audit/QA, Work Supervisor, benchmark/measurement facilities. Input: registered slots and actual journey/gate evidence. Output: truthful user surfaces and bounded release claims.

**Concrete work — W9a early:** reconcile the 888 event-site inventory to actual journeys, requirements, authorities and evidence (888 is not a journey denominator). Pin measurement classes, clocks, hardware/load, warm-ratio denominator and availability windows. Protect at least 200 held-out task references before training/tuning; define at least 400 paired task-path outcomes, rubric, actual same-model/seed support and comparison protocol. Resolve experimental custody/sole-invoker boundaries before any bare-path work.

**Concrete work — W9b:** complete registered Fixed/Templated/Generated slots, dependency resolution, deterministic salience and evidence handles within original prototypes. Apply already-ruled R32 Generated whitelist (chat answers, recommendation bodies, notification bodies). Verify every promised enabled control and result across scoped user roles, reload and mobile/desktop without redesign. Run protected paired capability/performance demonstrations on real admitted infrastructure, plus all four CC16 non-builder demonstrations. Measure every gate service per tenant over the actual period.

**Acceptance:** unknown inputs cannot become invented zeros/claims; every visible action/string/number has its proper authority/dependency/class and salience reason. Actual workload evidence supports any asserted throughput/P95/availability. Preserve source-specific release semantics: CC7 below-floor is a tier blocker; CC13 above-delta needs disclosure and named evidenced cause; harness-unavailable is no measurement, subject to the unresolved S35 reconciliation—not a universal pass or invented universal block. Proposed R41–46 numbers are not achieved SLOs. Short drills cannot demonstrate a month of 99.9% availability.

**Boundary:** W9a begins after relevant W0; W9b follows applicable real path exits, required independence and hardware/time evidence. No full-platform claim while a promised capability is still held/mocked/unmeasured. Prototype review by owner remains distinct from automated comparison.

## 6. Completion and reporting protocol

Every future closure card records: component/work-item ID; exact Canon and `(Doc, Rule ID)`/promise references; admitted population and procedure; input→governing decision→real effect→canonical evidence→consumer; producer and effective-state authority; reused/sealed files; dependencies/decisions; positive, denial, fault, concurrency and restart acceptance; expected artifact/checker; independence level; and explicit nonclaims.

Report two separate dimensions:
- **Engineering state:** not started / in progress / implemented with scoped tests / blocked.
- **Outcome evidence:** not run / MOCKED-only / real refusal / real successful bounded operation / independent re-performance.

Neither a plan, a green fixture, a reconciled all-refused job, a stored request nor a declared governing engine advances the real-success column. Do not invent a platform completion percentage or count shared gates repeatedly across components.

For each opened package: specify tests before code, exercise applicable negative/race/failure boundaries, verify API and existing consumer journey, preserve prototype hashes/visual fidelity, bank hashes and receipts, update the component ledger, and report failed/held items before claiming closure. Rollback means stopping exposure or restoring a prior admitted effective version via recorded procedure—not deleting evidence.

## 7. Proposed first implementation tranche — only after approval

1. W0 source/ruling reconciliation and exact closure cards, including the original DAP residuals; create no new authorities.
2. W1 selected identity/custody/write/handoff chain, with effect-safe failure and restart tests.
3. W5a + W6a + W7a prerequisites and W9a early measurement protection in parallel where dependencies allow.
4. W2 real source proof only when admitted infrastructure/source access is available; otherwise remain blocked and continue independent engineering work.
5. W3 real DAP request through verified retrieval, with W5b first if the selected operation requires quality-qualified material. W5b always precedes the grounded W4 path; W6b in parallel; W7b/W8 and W9b as their gates become satisfiable.

No calendar or cost commitment is justified before source/decision closure and admitted facilities are known. The immediate deliverable is this reviewable plan, not an implementation or an SSH retry.

Potential enhancement after the relevant producers exist: reuse the existing request drawer to show a receipt-linked explanation of the exact unmet admission/approval/execution/retrieval prerequisite, without a new dashboard or inferred status.