# Wave B Grounding Brief · Verbatim Requirements Only · 2026-08-26

Owner Condition 1: verbatim spec text only. Every requirement below is quoted directly from `canon/text/Akki_Canon_Documents_17_19.txt` (Docs 17/18/19) or `canon/w11_new_docs/audio_intel_plane.md` (Audio Intelligence Plane v1.0).

Owner Condition 2: after any compaction, re-read this brief before touching Wave B code.

## CP4 · Skill Files provenance (Doc 18 §A18.7 territory)

Register spec anchor: Doc18-007 · Skill File provenance chain.

Doc 18 verbatim on the Skill File contract discipline (line 148):
> «A18.4  [CANON] Below the floor is a refusal, never a degraded answer.»

The provenance chain contract already exists on disk uncommitted at `contracts/skill_file_provenance_v0.py` with tests. R3 confirmed the four wizard contracts are byte-identical LIFT; the skill-file contract is the paused-CP4 work that R6 register truth pass listed as "PARTIAL — contract-shape landed; wiring not started." CP4 completes:
- Contract snapshot (missing today, causes `test_frozen_contract_snapshot_parity` to fail).
- Producer wiring for skill_files_persistence.
- Ship-Manifest DoD: pod_shell import + HTTP surface + green tests, one commit.

## CP5 · Recipe seat + optimizer harness (Doc 17 §A17.3-A17.6)

### A17.3 verbatim (line 59-60)
> «A17.3  [CANON] Lineage extends to configuration.
> Every trained model's registry entry MUST cite the recipe_version that trained it. MOAC's lineage criterion (M-d) extends by this field, so "which configuration produced this model" is answered by reading the registry, never by asking whoever happened to run the job.»

### A17.4 verbatim (line 61)
> «A17.4  [CANON] Revision is DEFAULT-class, but never unevidenced.»

### A17.5-A17.6 verbatim (line 63-64)
> «A17.5–A17.6  [CANON] The optimizer-selection protocol: two arms, identical conditions, parity mandatory.
> The protocol executes at the first adapter training on real material, inside the P4-instrumented run. Its shape is one two-arm comparison — the current baseline optimizer versus a candidate, Muon named as the first — with identical training data, identical base model, identical evaluation sets, and an identical compute-budget cap, run on the smallest stratum that still yields a valid MOAC evaluation. Four measured outputs are reported for both arms without exception: target-stratum improvement (MOAC's M-a), non-target regression (M-b), wall-clock and GPU-hours to convergence, and calibration quality (an M-e input). Quality parity on M-a and M-b is mandatory for the candidate to remain eligible at all; compute-to-convergence is reported, never gating — a faster optimizer that regresses quality is not eligible regardless of its speed. The adopt/reject decision is then an Owner ruling made on the measured results, with no adoption threshold fixed in advance of the evidence, and verdict samples are uncurated per the platform's standing D-7 doctrine (evaluation inputs may be engineered; evaluation samples may not). On adoption, the winning arm writes training_params@v0 v1 with the comparison attached; on rejection, the candidate is recorded as tested, with its numbers, permanently. The identical protocol governs every future recipe-component candidate — this is not a one-time bootstrap, it is how the recipe seat is filled from now on.»

### Empty recipe seat verbatim (line 58)
> «No default recipe exists until the first training run fills it through the §3 optimizer-selection protocol (A17.5–A17.6). Nothing may pre-populate training_params@v0 by convention, template, or engineer judgement — the first value ever written to it must carry the measured comparison that produced it.»

## CP6 · Evidence Protocol EP-1, 2, 3, 5 (Doc 19B PROPOSED)

Doc 19 verbatim (line 167):
> «Two parts. Part A, the Critic Seam, is CANON — Owner-ratified 2026-07-15, reused here in full. Part B, the Evidence Protocol, is PROPOSED — my own prior synthesis from an August chat, explicitly offered there for ratification and never confirmed adopted; checked directly against both repositories, with no trace of a build or a ruling. It is written here to the same standard as everything ratified, with its status stated plainly rather than smoothed over.»

Doc 19 verbatim (lines 239-243):
> «EP-1  [PROPOSED] Build the register first — cheapest piece, and it immediately hardens the custody-recall and Model Acceptance sites above.
> EP-2  [PROPOSED] Dual-judge scoring (A-2) applies at every named site in §19B.4, plus any future site where a judgement call becomes a published number.
> EP-3  [PROPOSED] A-4 (claims validation) rides inside this capability, scoped explicitly as validation, never a build gate — its real experiments require real material and naturally sequence after the terminal test.
> EP-5  [PROPOSED] Explicitly not adopted, per the same proposal: the source spec's "insurance telemetry" aside (serves a goal never named) and its internal reduction-skill mandate (process tooling the Quality Rule Book already covers in doctrine — building enforcement machinery for it fails the platform's own reduction test).»

**Note**: EP-5 is EXPLICITLY NOT ADOPTED per the spec. CP6 lands EP-1, EP-2, EP-3 only. EP-5 gets no build — its explicit non-adoption is itself the outcome.

## CP7 · Register expansion (absorbing R6 truth pass)

Register CP7 in Wave A closed the 17→20-doc expansion (`d763721`). Wave B CP7 absorbs the Wave A truth pass (R6 note) into the register expansion so the composite lock ceremony sees the updated verdicts.

## CP8 · Trainer runner (Doc 17 full landing)

Doc 17 verbatim on the training envelope (line 15):
> «Every model the platform trains is a LoRA/PEFT adapter over a registered open base model — never a full fine-tune, never an unregistered model. This is FACT-class in the ratified spec, meaning it is not revisited per training job; it is a standing constraint on what "training" is allowed to mean on this platform. Training material is drawn exclusively from de-duplicated, VAD-cleaned, qualified units — the same units the estate's extraction pipeline already produces, never raw source reached around that pipeline. Acceptance runs exclusively through MOAC on uncurated held-out sets: a model is never accepted on the material it was tuned against.»

Doc 17 verbatim on build shape (line 88):
> «Build scope, once unblocked: contracts (training_config, training_run, training-material admit — roughly 500 LOC) plus a modality-agnostic runner service (roughly 2,000–3,000 LOC) plus a training panel frontend (recipe / run / MOAC — roughly 600–900 LOC, combined with the skill-files registry surface in Document 18). This is the W11 envelope, sized comparably to the platform's prior W10-class builds.»

Doc 17 verbatim on MOAC gate (line 90):
> «The surface displays "four of six checks passed" with all six criteria named and rejected models kept on record — real UI, real registry schema. But MOAC has a contract and no emitter: nothing in the current build actually runs a candidate through the six checks and writes the result. The surface is currently a faithful rendering of a process that has not yet executed.»

Doc 17 verbatim on acceptance (line 101):
> «No model enters service without clearing all six MOAC criteria on uncurated held-out material, with no human in the acceptance path.»

CP8 landing (owner directive): "trainer runner: LoRA/PEFT + Muon two-arm + Critic Seam gating every output + MOAC emission + cost-ledger metering + whitepaper on close."

**Sequencing**: build against MOCK SSH seam first; flip `GPU_CONNECT_MODE=real` when owner supplies SSH key; then hardware fact sheet probe → CUDA/PyTorch install (owner-approved) → first governed live training run on sealed DigiCow set.

## Audio plane (v1.0 spec · whisper-tiny CI path)

Audio plane verbatim §1.1 (line 21):
> «An audio file is a data estate, and the framing is recursive.
> The archive is an estate; a programme is an estate; a single file is an estate. Segments are rows; the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns; no schema exists until one is declared. Census, admission, registry, and record apply at every scale.»

Audio plane verbatim §1.2 (line 23):
> «Modality extension, not parallel machinery.
> The audio plane introduces no sibling services. Mtafiti gains an audio modality; Northena gains audio data classes; the wizard gains an objective variant; Targeta gains a training object. Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build.»

**Whisper-tiny CI path**: owner-supplied implementation guidance (2026-08-26) — hermetic CI must never spend real GPU compute; use `openai/whisper-tiny` (39M params, CPU-runnable) as the smoke-test model that proves the audio pipeline shape without needing production hardware. Wave B lands the CI path; Wave B+CP8 lands the real-GPU path when the SSH key arrives.

## Standing rules (from owner 2026-08-26)

- Both DoDs from R1 in force on every commit.
- Tests-first red/green receipts banked at `phase0/drill_receipts/`.
- Local commits only, NO push.
- No secrets echoed.
- pydantic 2.13.4.
- Single chokepoint.
- REFERENCE-NOT-COPY.
- N-series / A17.12-17 / A18.8 / EP-4 / Doc14-020 remain open config slots, never blockers.
- GPU-dependent work sequenced LAST; mock SSH seam first.
