# Akki — reuse-first closure plan and desk-response assessment

Date: 2026-09-28. Scope: source recovery, targeted read-only repository inspection,
prior-ruling reconciliation and planning. Not a security audit, full code review,
648-row reassessment, live estate test, admission ceremony or implementation release.

## Owner direction

The owner is working on GPU access and requests a plan for the previously estimated
65% gap. The owner supplies three original source families, points to
https://github.com/bramuel-syni/Akki-Executive-Core and
https://github.com/bramuel-syni/Akki-OS-V1 as existing implementations, and says
"skip" for tenant authority submissions and artists_app permission. Skip means
park these work items; it does not waive production authority or source permissions.
No GPU retries, estate scans, credential requests or UI changes in this review.

The desk offers DEFAULT-class positions ONLY if reconciliation finds no prior ruling:
- BC-3: estate state 24 hours via seal-and-bundle; Ledger effectively zero through
  continuous mirroring to its own device.
- BC-4: self-verifying bundle on replacement unit, chain intact, keys re-provisioned
  in owner's presence; 72 hours measured from replacement unit arrival.
- EP-1–4: adopt within Audit Standards v2 V1–V8, not a parallel scheme; E1 maps it.
- A18.6: permitted through Document 8's existing async contract: acknowledgement
  with estimate, first-class late refusal, governed-egress result delivery.

These are conditional policy inputs, not achieved RPO/RTO, signed admissions or
proof that prior rulings have been superseded. Current answer: seasoned direction,
provided the reconciliation genuinely constrains execution and reuse precedes build.

## 1. Verified source recovery

Originals retained unchanged under `assessment_workspace/incoming/owner_closure_plan/`.
ZIP safely extracted; each DOCX's document.xml independently extracted to adjacent
TXT. All 24 expected identifiers are present and their source bodies were read.

| Source | Historical rows | Documentary result |
|---|---|---|
| Streaming_Voice_Training_Capacity.docx | REQ-217–227: LT-1–3, RI-1–4, SE-1–4 | All 11 recovered. Source explicitly PROPOSED/NOT YET MERGED; LT-2 threshold and LT-3 calibration corpus remain OPEN in the source. Check later rulings before requesting decisions. Not a deployed telephony-service specification. |
| Supplement ZIP / Rule_Origination_Classification_Criteria.docx | REQ-276–286: ROC-1–11 (registry order is lexicographic) | All 11 recovered. Draft source must be reconciled with already-approved working default, not treated as a fresh blanket blocker. |
| AKKI_OS_Deck_Rendering_Engine_v1.docx | REQ-255 DR-R10; REQ-258 DR-R13 | Both corrupted-extraction clauses recovered. Full source includes producer mapping and named acceptance gates. |

SHA256 of original uploads:
- ZIP: `431a3fc7bacd6ab7cb14ae6d0d04a4a505a9f7a0462c7b0aa65a1cb1fc48b96c`
- Voice DOCX: `ef977165ba7c56c07065a55f317b327d21bd81c77fc2d8ba3de71fb409c8d497`
- Deck DOCX: `4f6169a7ed38d88f791f1293e3dfdbaa092eb4c333cf731bad55028598bd9f94`

This closes the missing-original dependency for these 24 clauses, not their
implementation/ratification/live-acceptance status. Historical source registers
remain unchanged; the next reconciled derivative must cite these replacement sources.

## 2. Prior rulings found — do not silently replace

References below are in `assessment_workspace/STATE/DECISIONS.md`.

| Topic | Recovered prior evidence | Consequence |
|---|---|---|
| BC-3/BC-4 | 2026-09-15 ruling, lines 8528–8552, especially 8548: "DO NOT SET A STATIC NUMBER"; tiered recovery packet, dynamic GPU checkpointing, near-zero ledger/registry RPO, immutable artifacts, site-loss alternatives and restore drills. `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` exists but full packet ratification is not established here. | Prior direction exists, so the new conditional 24h/72h defaults do NOT automatically bind. Recommend preserving tiers and considering seal-and-bundle only for an explicitly compatible tier. Bring a precise scoped amendment if needed; do not ask the same broad policy questions again. |
| A18.6 | 2026-08-27 bank, lines 2343–2364: explicit ADOPT. Current runtime has `services/service_1/a18_6_adoption_v0.json`, status RULED-ADOPTED. | Not pending owner adoption. Verify callable-skill implementation, current rights at late delivery, recovery and governed egress. |
| EP-4 | Same bank, lines 2348–2350: mandatory register + dual-judge guard before terminal testing. Runtime `services/evidence_register/terminal_test_guard.py` exists and reads registered terminal-test rows. | Preserve this ordering now. Code/register entries alone do not prove judge independence, current runtime binding or evaluation coverage. EP-1–3 adoption/mapping still needs exact reconciliation; A-4 remains validation, not a build gate. |
| ROC framework | 2026-09-09 bank, lines 6905–6919: BANKED-DERIVED approved working default; standalone source to be folded in when supplied. | Reconcile the recovered source at the next clean boundary; do not restart authorisation or reimplement the registry blindly. Draft header does not revoke the existing working default. |
| Evidence vocabulary | 2026-09-20 bank, lines 25923–25937, specifies V1–V7 for that workbook's QA Legend, with sampling tiers separate and auditor-only upward reclassification. New instruction names Audit Standards v2 V1–V8. Execution Standard v1 separately references V1/V8. | Pin/version the actual v2 definitions and crosswalk the older QA artefact. Do not invent V8's definition, rename classes silently or let a builder fill auditor verdicts. Exact EP-to-v2 class mapping remains engineering reconciliation, not a request to repeat the policy. |

Recovery acceptance considerations (recommendations, not new policy): a separate
device is not necessarily a separate site/failure domain; mirroring alone does not
prove zero committed-write loss or protect against replicated corruption. Measure
replica acknowledgement, lag, immutable recovery history and restored chain head.
Report replacement lead time separately: "72h after unit arrival" is not 72h from
incident onset. Keys need authorised recovery custody, not inclusion in a public bundle.

## 3. Repository inspection — reuse candidates, not blanket closure

Read both public main branches; pin complete non-truncated GitHub trees and selected
source snapshots under `incoming/owner_closure_plan/repositories/`. No donor code
was executed, imported, merged or substituted for the running build.

| Repository / pin | Concrete source inspected | Implication |
|---|---|---|
| Akki-Executive-Core `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | `backend/services/deck_generation_jobs.py` | Existing persisted, account-scoped generation jobs and phase/status handling. Reuse candidate, not proof of deterministic token-bound DR-R1–14 rendering. Work runs via in-process asyncio, not evidence of an admitted external estate worker. |
| Akki-OS-V1 `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | `backend/contracts/async_delivery_accepted_v1.py`; `backend/services/service_1/async_worker.py` | Existing accepted+estimate+trace contract, persisted state, refusal and recovery handling. `_dispatch_objective` handles composed conclusions/qualified data; callable-skill handling is explicitly not implemented in this inspected donor path. Reuse contract/state pattern and reconcile actual current skill dispatcher; do not claim A18.6 proved by generic async. |
| Same OS pin | `backend/services/generated_gates/instance_replication_playbook_v1.py` | File explicitly has zero generated gates. Its existence is not recovery proof. |
| Current vendored runtime | `contracts/deck_spec_v0.py` | Frozen two-field shell, not full recovered DeckSpec. Required-field additions need the existing versioned-contract process, not a silent v0 mutation. |
| Current vendored runtime | `services/rules_service/rule_registry.py` | Existing in-process registry module has a different enforcement vocabulary. Trace canonical registry and persistence before choosing an adapter; do not add a competing source of truth or equate its fields with ROC's three independent axes. |

This is targeted inspection, not an exhaustive branch/history hunt or proof that
these are the only implementations. Inspect reuse candidates and their call sites
against current Canon, existing ownership and frozen contracts before any lift.

## 4. Dependency-ordered closure plan

### P0-A — Correct the baseline and reuse map (engineering; start now)
1. Preserve original 648-row assessment; create a versioned reconciliation rather
   than treating the earlier 35%/65% blend as a measured programme baseline.
2. For each applicable row record source/hash, ruling/version, implementation
   repo/commit/function, active call path, test/evidence link, runtime/tenant scope,
   verification date, responsible party, next action and closure criterion.
3. Keep source availability, policy authority, code presence, active wiring and
   live proof as separate fields. Classify work as reuse / wire / repair / build /
   verify / scoped dependency; these are work dispositions, not ROC status values.
4. Reconcile the recovered 24 first, plus BC/EP/A18.6 and existing descriptor inventory.
   Time-box documentary work to these high-impact items and begin independent
   engineering; do not turn the full audit into a blanket pre-build dependency.
Exit: evidence-linked work queue, no false missing-source asks, named deltas rather
than an invented replacement completion percentage.

### P0-B — Qualify admitted non-GPU execution (engineering; parallel where independent)
1. Recover D-18 pilot / AKKI-TEST scope, real source/query/worker/inspection/custody
   descriptors and admissions. Validate the six supplied schemas plus signature,
   scope, expiry, revocation, tenant and provenance semantics.
2. Resolve `/mnt/nfs-share` to its actual hosting runtime. Mount visibility inside
   E1 is not permission to scan it from E1. Verify read-only access on an admitted
   external worker and the bounded OFFAIRRECS channel census there.
3. Reuse RMS/DigiCow/OBS drivers behind that admitted worker boundary; remove E1
   direct-source execution from the operative path. Secrets remain in approved
   custody; only permitted control/proof metadata returns to E1.
Exit: independently checkable worker identity/placement, bounded read receipt,
tenant isolation, failure/timeout handling, no source bytes or source execution in E1.

### P1-A — One genuine governed non-GPU journey (engineering, qualified runtime)
Use an existing admitted pilot scope on RMS or DigiCow, without widening rights:
DAP request → existing approval/entitlement → admitted worker → bounded census/
extraction → content registry + real DQ → grounded result where an admitted model
is available → measured usage → custody delivery → My Work/history.
Complete DigiCow tenant web-account plumbing without inventing approving authority.
Test cross-tenant denial, missing scope, expired/revoked entitlement, late refusal,
duplicate dispatch, crash/unknown outcome, usage reconciliation and stale delivery.
Exit: one correlated trace with genuine worker/ledger/custody receipts. A census
alone is not an answer or delivery. If a required model is unbound, hold that step
explicitly while finishing independent non-model path work.

### P1-B — Extend existing engines, close only demonstrated deltas (parallel tracks)
- Rules: canonical registry mapping, ROC origination/status/enforcement/domain
  separation, no duplicate identities, durable append-only supersession and
  existing customer rule-book boundary. No second ledger or registry authority.
- Async: reuse accepted/estimate/state/refusal contract; wire the actual callable
  skill path, restart/idempotency, current rights and governed egress. A18.6 needs
  implementation/proof, not renewed adoption.
- Decks: extend existing artifact-production service; reconcile donor report/deck
  overlap, versioned complete content-only schema, receipt resolution, token pins,
  producers DR-R10 and DR-R13 gates. Prove byte determinism, style rejection,
  unreceipted/missing-class/null-marker/coverage refusals and export fidelity;
  separately meter authoring and rerenders. No HTML/CSS redesign of owner UI.
- Voice: recover existing modules/call sites and later rulings, prepare incremental
  extraction/certified-identity synthesis/calibration contracts. Source latency
  figures are candidate benchmarks, not Akki SLAs. LT-2/3 decisions and real
  hardware/corpus measurements gate only the corresponding voice claims.
Exit: active-path contract tests plus scoped live evidence; label fixtures
SYNTHETIC/MOCKED and keep them out of live-closure counts.

### P1-C — Remaining product and operational proof
Close row-linked gaps across core promise/adaptive certainty, execution/context,
memory/learning/Watch, governance/containment, entitlements/commercial and
principals/tenancy. Reuse existing consumers; bind real producers for memory
publication/reload, Watch events/actions, withdrawals/descendant effects, usage
settlement and scoped recovery. Keep each claim within its measured scope.
Evidence-register/dual-judge prerequisites must exist BEFORE terminal evaluation;
independent verification uses a non-builder identity and required failure domain.
Exit: applicable acceptance scripts and real negative-path/drill receipts. No
programme-wide seal based on unit tests, mock signatures or historical screenshots.

### P2 — GPU and physical-recovery qualification
GPU connection/administration stays with the owner; no SSH retries until requested.
After access returns, verify admitted runtime then genuine model/media/training/
evaluation, checkpoint-resume and quality/latency outcomes; connectivity alone
does not establish compute admission. Exercise site-loss recovery only under a
reconciled authorised tier policy and approved drill scope. Independent non-GPU
work does not wait for these. Designer revisions remain separate future input.

## 5. Reporting and next actions

Each landing reports: exact requirement IDs advanced; reused vs changed components;
tests and evidence; remaining scope/holds; next executable action. Keep built and
live-proven totals separate with an explicit applicable denominator. No invented
percentage and no unsupported timeline before reuse/call-path inventory.

Immediate next actions: source/ruling/reuse crosswalk, descriptor/admission recovery,
NAS external-worker verification. Precise desk returns, if still necessary after
reconciliation: BC tier amendment, evidence-version mapping conflict, unresolved
voice calibration choices. Not a new general questionnaire.

Useful enhancement: add a concise "why still open / evidence needed" field to the
existing gap register, so closed sources and parked dependencies do not repeatedly
return as fresh owner requests. No new dashboard/UI redesign is implied.

## Verification for this planning turn

- Downloaded and SHA256-pinned all three uploads; extracted the two-member ZIP.
- Read all three DOCX source bodies and independently extracted OOXML text.
- Checked all 11 SV + 11 ROC + 2 deck identifiers against the historical 24 rows;
  baseline CSV has 648 rows. No whole-programme row closure recomputed.
- Retrieved both non-truncated repository trees at pinned main commits and read
  selected implementation files plus prior ruling records and local runtime files.
- Documentation only. No app/config/auth/credentials/UI modification, no new
  source/GPU/model calls, no acceptance/regression run or live certification.
- Broader model/answer/custody positives remain SYNTHETIC/MOCKED where not proven
  live; GPU authentication and admitted-runtime qualification remain unresolved.