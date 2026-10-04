# M Alpha execution — independent-evidence gate and native board, 2026-10-04

Owner approved the full plan (“Proceed”, then “ok”). Preserve active jobs; no new approval request or GPU cap. This batch follows the 18:44 worker/capacity update in M_ALPHA_WORKER_AUDIT_20261004.md. The broader31-job plan remains incomplete.

## CRITICAL: historical admission independence is NOT established

New read-only native metadata audit jobs `m9j-a07d621a84b4` (akki-vm) and `m9j-84826033f802` (akki-vm-ii) completed with identical findings. No transcript/audio bodies read, no model prediction on sealed content, no resealing or training interruption.

| Language | Admission positives / negatives | Recording sessions | Train↔admission shared speaker clusters | Dev↔admission shared speaker clusters |
|---|---:|---:|---:|---:|
| Kikuyu |6 /351|2|0|0|
| Kamba |8 /121|13|6|5|
| Kiswahili |9 /79|3|2|0|

Missing speaker assignments also exist (819 /425 /834 rows respectively), and exact text hashes overlap across splits. Some exact-text overlap may be common phrases, not malicious leakage; the audit deliberately calls for qualification instead of claiming every repeated phrase is contamination. All existing seal hashes are unchanged. Corpus speaker-cluster labels themselves are imperfect evidence, not guaranteed actual identities.

**Root cause confirmed in code:** old `assign_splits` hashes speaker clusters but pushes a multi-speaker straddling session to train while another session with that same speaker may remain admission. Session-disjoint was therefore not necessarily speaker-disjoint. DO NOT describe current admission data as independently speaker-disjoint. Do not randomly promote already-trained/development data to a supposedly fresh confirmation panel.

## Implemented

1. **Prospective sealing correction:** connected session/speaker/exact-text components cannot straddle splits; unknown-speaker components train-only. Input-order invariant. Used only for future database builds. Existing native corpus and active models untouched; existing data are NOT claimed repaired. Dense connection graphs may leave insufficient independent groups: disclose shortage instead of breaking components.
2. **Listener evidence protocol v1:** keeps owner point target precision AND recall≥0.90; adds Wilson95% and recording-session grouped bootstrap, explicit positive/negative/group support and independent-reference requirement. Engineering preregistration uses100positive/100negative segments and20recording groups; confidence is separately checked, so minimum counts alone do not pass. All three languages must qualify. No prediction/reference truncation; inconsistent group totals failclosed. These are stronger evidence conditions, not a lowered acceptance bar.
3. **Admission preflight:** reads already-recorded metadata only; held while reference qualification/support/independence is missing. One atomic confirmation reservation per panel, not unlimited new candidates reading the same sealed set. Reservations persist through uncertain dispatch outcome; no blind replay. Actual independent-human reference ingestion is still outstanding; current alias-derived labels never count as independent truth.
4. **Story evaluation protocol v2 (next workers only):** fixed realdev prompt panel and sample RNG isolated from training RNG, prompt/token/protocol hashes, documented token-weighted perplexity definition. No cycling a small prompt pool to pretend more distinct documents. Full generated text retained locally for future native review, only hashes/aggregates leave estate. Empty generation cannot win the language proxy. This is NOT a native quality judgement, and old/new protocol metrics are not silently treated as controlled contrasts.
5. **Native Train Models board:** M Alpha listener/text/voice and8Btrial appear on existing `/os/build/train` with actual optimizer-step progress, latest compact-stage metrics, prior attempts, data-expansion totals without double-counting host copies, and explicit development/identity/independence/reference warnings. M Alpha execution remains read-only there; no new parallel scheduler or ad-hoc training controls. Internal research record is not a product acceptance certificate.
6. **Serving truthfulness:** existing admitted text adapters without a running native serving record now show `Admitted`/`admitted · serving offline`, not `In service`. Existing admission/checkpoint preserved. Mobile selection scrolls to the selected thread; desktop and390pxmobile no horizontaloverflow.

New files: `services/training_lab/malpha_evaluation.py`, `malpha_corpus_audit.py`, `malpha_splits.py`, `malpha_board.py`. Native phases/bundle and `malpha.py` wired through existing M9. GET `/api/training/malpha/evaluation-evidence`; GET status includes evidence. Existing `/api/training/lab/board` includes MAlpha records only under the RMS tenant path. No auth or credential changes.

## Live progress verified 19:19 UTC
- Listenerit3 `m9j-63f66a09e65c`:6050/12000 steps.
- Textit5 `m9j-75e60db89466`:1770/3000.
- Voiceit5 `m9j-43924ae49fa1`:18100/40000.
- AdditionalQwen3-8Btrial `m9j-d4085045c5b6`:480/3000.
- All four processes alive; active training was never stopped.
- Kikuyu intake~37.955h/23800rows on leadinghost; otherhost~37.636h. Duplicated replicas, not75.6distincthours. Native intake still running; Kamba expansion will follow source traversal.
- LID remains temporarily unloaded on the borrowedGPU; restoration configured after8Btrial, not yet observed. Neither listener nor storyteller admitted.

## Verification
- Testing iteration89:46/46 scopedbackendtests plus desktop/mobile flows passed.
- Follow-up added mismatched-group refusal, compact livevoice readings and admitted-offline status tests: **49/49 passed**, `/app/test_reports/pytest/iteration_89_final_followup.xml`.
- Screenshots desktop1920×800/mobile390×844: no horizontaloverflow. Fixed selectedmobiletitle clipping; final titley12.67px and visible. Existing authenticated browser login and boardAPI work.
- Current-bundle native runtime audit jobs `m9j-1555bdc07323`/`m9j-1fe533642921` completed and settled at19:22UTC:10/10tensor-contract checks on EACH host. Finaltick dispatched no additionaltraining and didnotinterrupt activejobs.
- Unit test datasets/provider fixtures are **MOCKED test inputs only**; live app/APIs/audit records are not mocked. No provider calls were needed in this batch. No training-quality claim follows from syntheticunitchecks.

### Additional testing-agent observations, triaged separately
Testing agent made unsolicited fivefailed-login probes and flagged absent5-attemptlockout, create-only admin seed and previewOPTIONS origin rewriting. Existing `routers/auth.py` explicitly documents M2Watch observation-only behavior (commissioning may be gated; signin is not blocked), and credential continuity forbids unrequested rotation. No authorization was given to replace that established policy with generic playbook behavior. Therefore noauth/seedchange was made. Login, /me and authenticatedfrontend continueworking. Optional brute-forcehardening remains a policy decision, not a regressionfixedbythisbatch.

OPTIONS sent with the publicprevieworigin receives the canonicalclusterprevieworigin; same-origin authenticatedbrowserflows passed withoutCORSErrors. This edge/cross-origin discrepancy was observed, NOT fixed or claimed tested for externalcredentialedclients. Do not changeprotectedpreviewURLs or dispatch aproductiondeploy for this observation. Original `/app/test_reports/iteration_89.json` retained unchanged; this document records triage, not deletion of findings.

## Priorities
P0: qualify a genuinely fresh, independently annotated confirmation panel with adequate groups/mentions and complete speaker qualification; preserve old panel/records. Continue active runs and public intake; enforce identity<0.40; restoreLID aftertrial. Qualified story-instructiondata and native judgement remain absent.
P1: MA-13/16 real calibration/controlled contrasts (older8Btrial not causalbenchmark); MA-19 non-audio input/task/architecture matrix; MA-24/25 matched output-qualitycomparisons. Continue fullShield and ordinary-userrecovery proof.
P2/final:13-languagecompletion, acceptedskills, cross-domain CaaS/ARMIcommercial evidence, actualpriced accepted-outputeconomics, MA-31independentfive-promiseacceptance. No100%claim. A next useful workflow is native-review samples with independent double-annotation and disagreement adjudication; don't fabricate ratings.