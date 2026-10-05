# Requirements reconciliation — current owner correction

## Authority and scope
Owner source: `M_ALPHA_OWNER_ORDERS.md` §8, followed by “Proceed” and the supplied
prior exchange. This record reconciles that exchange; it does not ratify earlier
assistant assumptions. Applies to all 31 M Alpha jobs and all explicitly issued
requirements, building guardrails and ratifications, not only confidentiality.

Read `../AGENTS.md` before work. Existing canonical/ratification source documents
remain authoritative; this index does not assert an exhaustive clause audit.

## Reconciliation of the earlier statements
| Earlier statement/proposal | Corrected position | Evidence/status |
|---|---|---|
| Fix JSON false positives and carry on | Necessary utility regression work is not delivery of contextual confidentiality | `semantic_register.classify` still uses sentence cues/capitalisation; no contained semantic reader in that path |
| Schema keys are harmless | No blanket exemption: a key can itself contain owner-classified material | Doc 1 A3/A5.4; owner §8 |
| Use Qwen3-8B and dedicate a GPU | Candidate suggested by assistant, NOT owner-selected version/capacity assignment | Owner asks strongest suitable contained capability; inventory/qualification required |
| Shield inside versus outside LLM processing | Estate-side protection precedes external task inference; the sole invocation still enforces custody | Doc 1 A5.1–5.8 and B5.1–5.5 |
| Current register = user's three categories | Exact/pattern/contextual are mechanisms; owner needs conventional identifiers, named content, descriptive privileged meaning | Doc 2 A3/A5; owner §8 |
| “Adopt” immediately enforces; DPO removal is enough | Canon separates adopt/pending from approve/live and requires governed removal ceremony | Doc 2 A4/A5.4; current register contradicts this unless a later explicit ruling is found |
| Two strings processed = dual-file compliance | System/prompt payload coverage is not proof of question/data independent assessment | Doc 2 B5; `llm.invoke` currently joins system+prompt before de-identification |
| No intent mechanism exists anywhere | Too broad: Solva intent audit exists and the supervisor uses it; pre-redaction question objective extraction is not wired in the inspected crossing | `malpha_supervisor.py` imports existing Solva faculties; `llm.py` sequence |
| Audio spectrum offset removes biometrics | Illustrative owner thought, not an accepted algorithm or privacy proof | AIP §§6–7; utility and linkage/speaker tests required |
| Dispatcher rejection proves Shield placement issue | Separate payload-schema contract defect; confirm with isolated validator reproduction | `training_runner/m9_dispatch.py` and supervisor producer |
| 04:22 claims establish current GPU progress/Shield success | Historical claims only; fresh job/PID/heartbeat and crossing evidence required | Native job ledger; no fresh claim yet |

## Governing sources read for this reconciliation
- `assessment_workspace/notes/full_requirements_gap_20260926/source_text/01_Custody_and_the_Crossing_Part_1_The_Chokepoint_a3358829.txt`
- `assessment_workspace/notes/full_requirements_gap_20260926/source_text/02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File_4ca0109d.txt`
- `assessment_workspace/canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec.txt` (relevant biometric/character clauses located; full audio path assessment pending).
- `M_ALPHA_PLAN.md`, `M_ALPHA_OWNER_ORDERS.md`, `M_ALPHA_EXECUTION_LOG.md`, `PRD.md`.

### Ratification source index (preserve successive rulings, not just document titles)
- `assessment_workspace/canon/drops/20260910/extracted/text/Ratification_Record_v1.txt`
  is the original consolidated list, not current proof all its unsigned rows are open.
- `assessment_workspace/notes/RATIFICATION_C3_BATCH_20260913.md` records actual
  owner-approved defaults, including the 48-hour/system-ordinary and 7-day/TCB
  countdowns. These are recovered rulings, not newly invented thresholds.
- `assessment_workspace/notes/PENDING_RATIFICATIONS_LEDGER_20260915.md` contains
  later flips inside a file still named “PENDING”: R-7 PILOT-OPEN, R-15(a)
  TOKENIZED, and other separately scoped decisions. Read each row and its cited
  authority; do not reopen a settled row or conflate duplicate R-numbers.
- Existing master registry:
  `assessment_workspace/canon/drops/20260910/extracted/text/Master_Requirements_Registry.md`.
  M Alpha's 31 jobs organize delivery; they do not replace its underlying clauses.
- No source inspected here ratifies replacing the confidentiality addition/removal
  ceremony with the current immediate adopt/remove functions. Full later-ruling
  tracing remains required before that lifecycle is changed.

## Required capability → mechanism → test → pass
All rows below are REQUIRED unless explicitly marked engineering-mechanism;
they are not claims of implementation or acceptance.

| ID / source | Existing owner and required capability | Verification / pass evidence | Current status |
|---|---|---|---|
| RQ-01 · latest owner; MA-01 | Requirements-first disk anchor for all work; preserve ratifications and supersessions | Source links resolve; proposals cannot be confused with owner-issued decisions; next agent is directed to read them | Recorded; independent verification pending |
| RQ-02 · Doc 1 A3/A5.4; owner category 1 | Shield deterministic identifiers + qualified local NER for PII/HII/BII/payment identifiers | Positive/negative, multilingual and document tests with false-positive/false-negative measurements; no payload leakage | Regex and local spaCy exist; breadth/quality not certified |
| RQ-03 · Doc 2 A3–A5; owner category 2 | Existing tenant confidentiality authority consumes named values, including workbook intake | Tenant/version isolation; bulk input validation; governed adoption/approval/removal; effective declarations consumed on all paths | Exact-value backend exists; vault workbook flow and canonical lifecycle not verified |
| RQ-04 · Doc 2 A3/A5.2; owner category 3 | Contained reasoning reads user descriptions and originals; local NER supports—not replaces—reasoning | Paraphrases/indirect disclosure, contracts/BRDs/audit/IP; unchanged harmless schemas; ambiguous case refused; useful task retained | GAP: cue matcher is not this capability |
| RQ-05 · Doc 1 B5; Solva/Northena | Read question intent/meaning/objective before redaction; freeze same artifact consumed by downstream checks | Order, immutable artifact, declared/demonstrated separation, refusal on incoherent objective | GAP in inspected crossing; reuse existing faculties, not a new Solva |
| RQ-06 · Doc 1 A5; Doc 2 B5 | Independent question/data assessment then guarded association; safe-only outbound; local re-identification | Combination attack, tainted marking, both payload paths, request-local mapping lifetime, exception cleanup; all calls receipted | Existing chokepoint preserved; full compliance not established |
| RQ-07 · owner contained model; Doc 1 A5.5 | Estate-owned inference with no external-world contact | Admitted local model/version/hash/license; offline loading; enforced egress deny/telemetry/log limits; failure refuses before external client | Model/capacity/network qualification pending; no external fallback permitted |
| RQ-08 · owner audio; AIP §§6–7; MA-11/15 | Derived spectrum/character datasets exclude anatomical identity while retaining content/language/group character | No per-utterance embeddings persisted; temporary cleanup; independent speaker/linkage/memorisation tests AND utility tests by language | Assessment pending; no transform or threshold invented |
| RQ-09 · supervised training; MA-07 | Supervisor/CIF lineage reaches native dispatch without changing authority/floors | Valid training-phase metadata passes; malformed/other-phase metadata and unknown fields refuse; existing gates unchanged | Missing allowlist entries observed; isolated reproduction pending |

## Execution order after reconciliation
1. Preserve this owner record and persistent entry anchor; verify trace links and
   contradictions. Review existing ratification records before changing lifecycle.
2. Verify the separate dispatcher defect and native job state without stopping,
   re-planning or evicting running jobs. Test any bounded contract correction.
3. Qualify the contained-reader/NER implementation and containment using existing
   estate model/compute/serving seams. No external originals, hidden fallback,
   arbitrary GPU reassignment, or claim of “latest/best” from an old cached model.
4. Extend the existing boundary with source-traced intent, confidentiality and
   dual-file behavior. Tests first; no cue-list patch presented as completion.
5. Assess and qualify audio privacy transformations with existing AIP controls;
   keep running jobs untouched and do not auto-admit unsafe artifacts.
6. Continue the remaining registered M Alpha jobs (including MA-19) without
   erasing pending native review, LID, output comparisons or CaaS obligations.

No paid planner/reviewer replay, new model installation, GPU eviction, public-data
intake or new scheduler is authorized merely by recording this reconciliation.
Existing owner execution authority is preserved; readiness must be demonstrated.

## Bounded implementation record — 2026-10-05
Engineering mechanisms under RQ-07/RQ-09, not new owner requirements:
- Native validator reproduction at 09:26 UTC refused the story-text supervisor's
  `hypothesis_id`/`cif_proposal_id`. Permit a validated matching pair ONLY on the
  three supervised training phases; retain every prior field/authority/recipe
  check. Correct error reporting so absent optional fields are not falsely named.
- Shield `_attempt_load` invokes `python -m spacy download` after any load failure.
  Remove that request/startup-time network path. Preserve already-prescribed
  installed transformer → installed small fallback and existing 503 fail-closed
  behavior when neither works. Report the actual model, not unsupported F1 claims.
  This is offline-loader hardening, NOT network-isolation certification or the
  missing contained reasoning capability. No package/model installation.
- Existing Watch scorer is NOT wholly mocked: `score_input_seat(payload_text=...)`
  calls a deterministic rule detector; the no-payload compatibility path is
  unmeasured low/pass and provenance is declared. Correct stale documentation,
  not thresholds, authority or behavior. Learned/calibrated detection remains open.
- Corrected integration guidance confirms: contained semantic reading of originals
  precedes redaction; EXTERNAL models alone are safe-context-only. No new service,
  auth, UI, database, model choice or GPU assignment is introduced.

Read-only ledger at 09:26 UTC: story_text it.8 completed, listener it.4 completed,
story_voice it.9 completed; `hyp-2711588de01d` adopted with no bound job. Therefore
the supplied earlier claim “listener and voice are still running” is stale for this
observation. No job was stopped or manually dispatched during reconciliation.

## Audio assessment — source evidence, not privacy certification
- `malpha_worker.py:_analyse_file/run_shard/build_aip` persists per-segment
  acoustic features plus PCM and codec codes on estate hosts. Codec conversion is
  NOT evidence of anonymisation. Raw-source custody and admissible derived
  register custody must not be conflated.
- `character_register(rows)` currently aggregates every `FEATURES` field,
  including absolute F0-related fields, without a visible minimum-distinct-speaker
  or non-reconstructive-combination check in this function. Its “no anatomical
  identity” docstring alone does not establish AIP §6 compliance.
- `malpha_voice_worker.py` computes temporary speaker-comparison/conditioning
  representations in memory and gates generated identity distance. That output
  gate does not establish that the stored input spectrum is de-identified.
- Required next evidence: attribute-level eligibility under all FOUR AIP custody
  conditions, group-size/combination/idiolect storage attacks, read-path lineage,
  independent speaker/linkage tests, and per-language utility before/after any
  proposed transformation. Do not delete raw estate material or replace ongoing
  worker data under this assessment. No arbitrary “3 basis points” transform.

## Verification — 2026-10-05
- `test_reports/iteration_92.json`: 23/23 focused backend tests passed; synthetic
  fixtures/fake-client branches **MOCKED**, real installed small NER also exercised.
- `test_reports/iteration_92_adjudication.md` corrects the report's old-log inference:
  last referenced dispatch failure 09:15; hot reload 09:29:53; all three lanes
  dispatched under the existing scheduler at 09:30. No manual tick or GPU stop.
- Current shell's `/api/healthz`, `/api/readyz`, `/api/healthz/shield` are UNMOUNTED.
  Comments now distinguish source definitions from working readiness routes.
- No live frontier replay performed; no contextual Shield completion claimed.
  No Qwen or replacement NER selected/installed, no network-isolation certificate,
  no audio privacy/utility admission, no declaration-governance waiver.
- Final self-verification after test isolation and additional loader cases:
  **28/28 passed**, `test_reports/pytest/iteration_92_final.xml`; 31 unique M Alpha
  rows intact, all seven cited governing source paths resolve, zero scope errors
  after the 09:29:53 reload observed through the final log check. All three remote
  worker PIDs verified active ~09:41 UTC. This is bounded evidence, not MA-04/05
  or full five-promise acceptance.

## Optional engineering enhancement — proposed, not ratified or implemented
Machine-check clause-to-change evidence receipts (source/version, existing service,
test result and explicit unresolved gaps) to supplement the persistent agent-entry
rule. Reuse existing requirement/Ledger records; do not create a second operational
authority. This could detect future requirement drift automatically. It is not a
new owner requirement, settled product behavior or a claimed runtime safeguard.