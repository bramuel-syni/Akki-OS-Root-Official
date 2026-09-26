# Component-led work ledger — current scope and next links

## Current owner-directed work — compute parked; autonomous continuation

Owner explicitly said skip compute recovery and continue, then authorized autonomous work while away. Current link is **Northena + DAP lifecycle + OS/DAP shared work records**, followed by **entitlements/terms/metering** and remaining operational/output journeys. D01–D12 acceptance in `STATE/OBJECTIVES/CP_DAP_OPERATIONAL_V1.md`. No additional AISCA/key operations or provider outreach. Compute/T14 stays blocked; original prototype architecture and full functionality plan unchanged. All earlier recovery entries below are historical, not resumed work.

**Latest20:06Z — AISCA control-plane recovery:** owner portal credentials now verified WORKING; both existing VMs Running in akki-workspace. Console launch fails HTTP502 on BOTH before terminal. Inspected akki-vm key field remains disabled after readiness; expanded viewer readOnly. No key generated/enrolled/revoked, no VM lifecycle/config or product UI changes. Link still blocked: provider administrator/console → replacement-key enrollment → pinned SSH → Akki executor → Mtafiti → OS/DAP. T14 stays0/1, not advanced by successful portal login. REAL browser evidence and prepared-not-sent provider request in `AISCA_AUTHENTICATED_RECOVERY.md` / `AISCA_PROVIDER_RECOVERY_REQUEST.md`. Do not ask again for already working portal credentials or new-key permission. Original component backlog unchanged.

**Latest compute recovery checkpoint18:57Z:** owner GPU workbook is secured and matched to existing host/user pairs. Fresh pinned `auth_none` queries: both server pins MATCH, both accounts advertise publickey only, neither authenticated. Passwords NOT attempted; workbook contains no original private key. Additive operational diagnostic + exclusive receipt runner verified by23 MOCKED tests; full census scope103 passed/2 intentionally skipped twice. Two REAL method-query receipts banked separately. This confirms the recovery dependency, not connection restoration. Mtafiti fresh output/T14 remains0/1. Need original key from authorized system/backup or approved console route. Details `EXECUTION_RECOVERY.md`; no UI changes, no new component-completion percentage.

Owner request: "before you continue, are you able to show which component you are tieing up, eg solva? mtaFITI?, ETC".

This is a component ownership/status map, NOT a claim that every listed component is already integrated or verified. No new execution/recovery or application changes were made while answering. Report work through this ledger and progress updates; do not create a replacement dashboard or change the owner prototypes.

## Current continuation — 2026-09-25 (supersedes the historical no-change checkpoint)

Owner reaffirmed the original plan; current work remains compute identity → Census Autonomy → Mtafiti evidence → OS/DAP consumers.

|Component / work item|Exact link advanced|Verified / acceptance|Still open|
|---|---|---|---|
|Akki compute — COMPUTE-CENSUS-IDENTITY|Banked admitted identity receipt → actual private-key verification → exact pkey used by census transport|R01–R08 **8/8 safeguard conditions**, 82 scoped tests twice; private-key mismatch stops before SSH; no password fallback or new key. Source: `execution_identity.py` + additive `remote_dispatch.py`; anchors SO §4.1, CP-CENSUS MUST DO 4 / T07.|Actual host access **BLOCKED**: current key differs from admitted August28/September22 pin. Restore admitted key/authorized recovery channel; hardening cannot install without authenticated recovery access.|
|Census Autonomy — CENSUS-REFUSAL|Authenticated commission → existing queue/executor → typed identity refusal → durable result and idempotent replay|Real API run `cr-809561ad5643`, two `IDENTITY_PIN_MISMATCH` transport records; no source read. Existing sealed result writer reused. T08/T10 regression passes.|T14 **0/1**: no newly successful Akki source outcome. Remote worker/connector custody still unverified.|
|Mtafiti — MTA-CENSUS-EVIDENCE|Same canonical receipt-class asset writer and tenant projections|Prior retained-record/regression evidence remains valid. No new source-result asset fabricated by refusal drill.|Fresh output → registration → durable OS/DAP result remains partial; no claim of full profiling/quality/semantics.|
|OS/DAP — ACTION-TRACE|Original markup → source-hashed event-site inventory → component/journey reconciliation|`PROTOTYPE_ACTION_INVENTORY.json`: 817 OS +71 DAP sites, 888 unique IDs; original DOM/HTML/application UI unchanged.|Event-site inventory is NOT a journey denominator. Component/Canon/writer/test joins remain in progress. Whole-platform completion still NOT YET MEASURED.|

Full scope, filenames, test levels, local-vs-live distinctions and remaining recovery exit: `EXECUTION_RECOVERY.md`. Unit transports are **MOCKED**; persisted API refusal is real, but is not successful execution.

## Current actual work

|Component|Specific link|Verified evidence|Limit/status|
|---|---|---|---|
|Mtafiti|Retained census manifests → tenant-scoped registry projection; validated new outcomes → canonical receipt-asset writer|`services/mtafiti/census_projection.py`; `census_result_adapter.py:7-17`; real census4 reads agree across OS/DAP; isolated writer/persistence tests|PARTIAL. Current adapter registers `AssetClass.RECEIPT`, not a complete source characterisation. No fresh real source outcome has passed the live gate.|
|Census Autonomy Service|Admitted commission → existing queue → bounded executor → validated outcome → governing result/refusal|`services/census_autonomy/operational_runner.py:25-93`; `operational_store.py`; real queued→executing→blocked receipt|WIRED / LIVE ACTIVATION BLOCKED. Completion, failure and retry checks include MOCKED executors; no claim of actual successful estate read.|
|Akki compute/connection seam|Existing host/credential configuration → strict-host-key execution connection → remote census worker|`remote_dispatch.py` composes configured host identity from `services/training_runner/ssh_seam.py`; cr-a29e3b7b16ae transport receipts|Last recorded attempt blocked by AuthenticationException on both configured identities. Not a GPU hardware diagnosis or proof of remote authorized_keys contents.|
|Identity/enforcement layer|Existing account → owner-approved server-side tenant membership → scoped read / operator-only commission|`services/enforce/census_identity.py`; `operational_scope.py`; authenticated operator/analyst/anonymous tests|VERIFIED for the tested census routes. Not certification of platform-wide governance/tenancy.|
|OS and DAP consumer surfaces|Shared census projection and actual run state → original owner-prototype Registry/history/evidence experience|`operational_reads.py:13-40`; OwnerOSPage/OwnerDAPLayout and safe original-markup renderer; F01–F08|VERIFIED for the census slice. These are consumers, not additional engine/registry authorities.|

### Important boundary on the Mtafiti claim

`operational_runner.py:60-76` validates output, calls `register_outcome`, then banks the durable result through the existing census writer. `census_result_adapter.py:10` explicitly assigns **RECEIPT** asset class. `operational_reads.py:25-27` validates and rehydrates that record through the same writer.

This establishes a specific census-evidence/registry connection. It does not establish all source inventory registration, profiling, relationships, semantic characterisation, content coverage, language/quality measurement, or all of Mtafiti's Canon duties. Do not mark “Mtafiti complete” from this slice.

## Next component-owned work in the wider functionality plan

|Component|Intended work item|Current status in this delivery|
|---|---|---|
|Northena|Tie DAP request and OS commission to the existing frozen objective/run record, dispatch, status, result and history.|Existing record machinery identified; full request-to-result link not completed by the census work.|
|Mkondo|Trace and verify governed handoff contracts/record ownership across actual component transitions.|Unverified beyond reviewed clauses/selected source. Writing a JSON receipt is not itself proof of Mkondo compliance.|
|Targeta|Trace eligibility/ranking consumers in the commissioned path and preserve deterministic-first operation; learned ordering only when duly admitted.|Deterministic implementation exists; not modified/activated by this slice.|
|Solva|Trace and connect evidence-grounded reasoning/assertion/result generation to the relevant request journeys; verify floor, provenance and refusals.|Not tied up by the census work. Full end-to-end grounding/reasoning journey remains to be verified; do not assume missing or complete.|
|SyniSense / Shield|Verify applicable model/custody crossings use the existing chokepoint and actual policy, input, output and receipt controls.|Chokepoint code exists; no global integration/compliance claim from a metadata-only census.|
|Watch — Macho/Mkono|Bind real observations to verdict/action paths and the required records; verify detection/action separation and failure posture.|Executable mechanisms identified; existing input-score binding gap in the inspected LLM crossing not fixed by census work.|
|CIF|Trace accepted proposals into the appropriate durable faculty/research/learning records and applicable reuse/retirement behaviour.|Proposal/acceptance/routing mechanics exist; complete durable learning loop not verified or changed here.|
|Model/audio/training planes|Bind actual commissions, corpus custody, calibration/evaluation and admission to real executors and outputs.|Real algorithms and historical runs exist; current governed product journey not yet established.|

These entries are work ownership labels, not an invented serial call graph. The actual allowed dependency and handoff order must be established from the Canon and implementation. Applicable governance, rights, Shield and Watch gates are cross-cutting requirements, not a final-stage add-on.

## Required format for future progress updates

1. **Component and work-item ID** (e.g. MTA-CENSUS-EVIDENCE).
2. **Promise / Canon anchor** and the owning record class.
3. **Input → exact link → output**, with upstream/downstream owners.
4. **Existing capability reused**, exact files touched and whether sealed bodies are untouched.
5. **Tests and real evidence**, explicitly separating MOCKED executor checks from actual execution.
6. **Status:** verified / partial / blocked / unreviewed / not started.
7. **Next acceptance gate and blocker.**
8. **Progress:** completed / total baselined acceptance items for THAT work item. Do not assign the shared13/14 census score to Mtafiti, Solva or the whole platform; component totals remain unmeasured until their acceptance sets are established.

## Immediate closure target

Current: Mtafiti census-evidence link + Census Autonomy + admitted compute execution + existing OS/DAP consumers. Next real proof is an Akki-owned bounded source outcome, validated canonical registration and durable evidence visible consistently in both products. Solva's reasoning workflow is a different work item and is not part of that claim.

## 2026-09-26 non-compute continuation — owner-approved

The above compute closure is PARKED per owner direction, not waived. Current
non-compute work is NORTHENA-DAP-RECORD, OS-DAP-WORK, LICENCE-READ and
SKILL-QUERY-SAFETY. Their Canon/input/output/file/evidence/status/next-gate mapping
is banked in `notes/dap_operational_v1/VERIFICATION_REPORT.md`.

- NORTHENA-DAP-RECORD: **verified durable intent**, strict scoped submission,
  immutable canonical payload+17-field row, replay/concurrency/persistence.
- OS-DAP-WORK: **partial operational parity**; same held request/work/history
  renders in original prototypes. No claim of approved/running/ready output.
- LICENCE-READ: **partial**; read-only event projection with correct unresolved
  production state. Positive licences/rates/metering are TEST-ONLY fixtures;
  actual owner-admission/ceremony/metering producers still need wiring.
- SKILL-QUERY-SAFETY: caller-supplied answer/class removed; **explicit refusal**,
  not skill execution. Positive precondition gate is MOCKED in unit tests.
- Frozen D01–D12 accounting: **4 verified, 7 partial, 1 open** for this slice.
  Broader888-action prototype→Canon coverage remains in progress/unmeasured.
- Tests:146pass/2skip twice plus real API/browser/build, chain+payload verification;
  bank `phase0/drill_receipts/dap_operational_v1/`. No GPU/source queries, licence
  seeds, external execution, account changes or billing usage. User review pending.