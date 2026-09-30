# Audio cognition and music — plan for owner review

## Current result
Training has **not** restarted. No new model was admitted or served. A background inspection completed on Akki's NVIDIA H200 worker using the already-authorized staged corpus; no recordings were copied to this workspace.

Measured staged inventory: **3,958 audio files, 529.3379 hours, 36,516,920,948 bytes**, with **3,939 transcript files**. These are audio-container durations and bytes, **not deduplicated or verified speech-only / non-music totals** and not a census of the entire RMS estate. Folder names are existing labels, not newly verified language annotations.

| Existing label | Files | Audio hours | Transcript files |
|---|---:|---:|---:|
| guz | 732 | 92.2269 | 730 |
| kam | 1,166 | 85.3711 | 1,165 |
| kik | 584 | 82.0832 | 583 |
| kln | 295 | 89.7250 | 295 |
| luo | 558 | 81.9929 | 557 |
| lwg | 60 | 9.1942 | 60 |
| swa | 549 | 87.6722 | 549 |
| bxk | 14 | 1.0724 | 0 |

All inspected headers were readable. Sample rates: 44,100 Hz (3,126 files), 48,000 (162), 22,050 (49), 11,025 (597), 16,000 (22), 32,000 (2). **These do not establish studio/telephony quality.** No 8 kHz files appeared in this staged subset; that is not a claim about RMS's full estate.

## Findings that block a credible new result
1. No verified speech/music/mixed annotation contract was established in the existing staged corpus. This is not proof that no such labels exist anywhere in RMS.
2. Existing training is markedly imbalanced. The smallest represented folders are not a substitute for well-covered, speaker-diverse language data. BXK and LWG need ontology reconciliation before merging or treating them as independent target classes.
3. The later recipe sweep did not eliminate speaker leakage or meet every language floor. More epochs alone are not a justified fix.
4. Existing final-test results have already been inspected. They remain historical/exploratory evidence; a fresh independent, sealed final set is required for credible acceptance after further selection.
5. Labelled code-switch, English and Sheng coverage remains unestablished for the dormant audio scope. Excluded strata must be explicitly excluded, never silently treated as passed.

## Proposed staged approach — NOT an approved training recipe
### A. Data and acceptance contract
- Audit rights and provenance of existing materials before re-use, including withdrawal status.
- Agree independent labels for **speech present** and **music present**; allow both, neither and uncertain. Annotate time spans rather than pretending a whole recording has one label.
- Separate recording condition, language, topic (news/education etc.) and format (presenter/interview/call-in). These are different targets.
- Validate annotation agreement on a double-labelled sample. Report disagreement and unknowns; do not convert heuristics into reference labels.
- Partition by presenter/speaker, session and source; remove exact/near duplicates across partitions. Retain native-bandwidth conditions; resampling telephony does not restore lost bandwidth.
- Agree music precision/recall and coverage floors, subgroup sample sizes, tolerable false-alert rates, privacy requirements and an explicit compute cap **before** training. No new numeric acceptance thresholds are invented in this plan.

### B. Controlled comparison
- Start with a **separate speech/music multi-label head**, compare with joint training only if data and privacy budgets permit. Preserve language behaviour as a non-target-regression check.
- Music-only windows must not be forced to carry a speech-language label. Unknown annotations must be masked, not treated as negative labels.
- Target weaker-language data quality and speaker diversity before simply oversampling rare speakers.
- Prespecify one-factor comparisons and seeds. Include preprocessing, tokenizer/normalization versions if transcription is introduced. ASR requires WER/CER, VAD/segmentation and bandwidth-aware evaluation; language-ID accuracy is not ASR quality.
- Any added trainable head must be included in the declared DP/accounting and checkpoint contract. Window-level DP must not be presented as speaker-level privacy.

### C. Feedback while work runs
- Persist development-only epoch/step metrics. The lab watches distinct checkpoints, not the sealed final test.
- Five advisory roles inspect the same allowlisted aggregates concurrently. Their output can recommend review/stop/experiments; it cannot change a live recipe, spend beyond authorization, train, admit or serve a model.
- Current safety bound: at most four model-reviewed checkpoints per audio job, with a configurable maximum of eight. Schedule configured every fifteen minutes; actual recurring scheduler delivery still needs observation. Webhook delivery and queue resumption were manually verified.
- Calibrate monitor thresholds from actual calibration observations and state empirical false-alert uncertainty. Repeated looks are exploratory unless an approved sequential-testing design exists.

### D. Final evaluation and decision
- Report per-language accuracy **and coverage**, speech/music precision/recall/AP by condition, mixed-audio errors, uncertainty via actual paired/group resampling, and speaker-leakage probes.
- Evaluate the sealed final set once after recipe selection; compare against the prior admitted/non-admitted baseline honestly.
- Report cost, risk-adjusted value, delivery delay and the next-best objective. A numeric value scenario is not investment approval.
- Score predictions against results. Any proposed prior/threshold update remains reviewable and versioned; no automatic model admission or replacement.

## Implementation versus evidence
- Live background worker inspection and five concurrent model reviews were executed and receipted.
- Independent speech/music decision logic and a GPU head forward/backward arithmetic check work. The latter used **SYNTHETIC random tensors**; no music model was trained and no accuracy claim follows from it.
- The uploaded package's real training adapter remains unimplemented. The lab does not pretend it is a universal trainer; new task families need admitted executor adapters and modality-specific evaluation contracts.
- The first model review contained a throughput/compute-hours confusion. Original output was preserved, flagged and followed by a bounded correction review. Machine checks are not a substitute for independent specialist validation.
- Final verification: **24 pytest passed (zero skipped), 14/14 package mechanical checks passed**, and all five live correction reviews passed schema/reference/bounded machine checks. The original assessment remains partial due to retained quality flags; the correction is a separate complete record.
- Live literature retrieval is not integrated into model advisory calls. Specialist guidance includes researched reference notes, but model memory is labelled advisory, not fresh literature evidence.

## Decision needed before retraining
Approve the labelled-data scope, music acceptance criteria, speaker/privacy evaluation and a bounded comparison recipe. Until those are agreed, the lab should continue inspection/planning only—**not spend H200 time on another full training run**.