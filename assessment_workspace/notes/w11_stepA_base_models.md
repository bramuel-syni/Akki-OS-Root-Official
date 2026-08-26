# W11 · Step A · Base-Model Findings

**Owner directive**: Ingest new audio specs / base-models docs · cross-reference `models_registry.v0.json` · extract predefined base-model choices per modality (audio vs text).

**Session**: W11 Step A (spec ingestion phase · read-only) · closed 2026-08-26.

## §1 · Sources read in this session

| File | Lines | Purpose |
|------|------:|---------|
| `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` | 303 | Consolidated build spec · supersedes Audio Capability Spec v1.0 + Addendum v1.1.2 |
| `canon/text/Audio_Intelligence_Plane.md` | 431 | Companion .md version of same spec |
| `canon/text/Akki_Training_Techniques_Spec.txt` | 52 | T-1..T-4 governed artefact · Owner-ratified 2026-07-17 |
| `canon/text/Akki_OS_Incremental_Training_Capacity_Briefing.txt` | 231 | Doc 17 companion · TCO theory · Demand/Capacity/Gap grammar |
| `backend/services/perception/models_registry.v0.json` (Extraction-Akki) | ~135 | On-disk seeded registry |

All reads verbatim · zero paraphrasing above the anchor level.

## §2 · Base-model extraction · per modality

### 2.1 · Audio modality

Authority anchors (in reading order):

1. **`models_registry.v0.json` §`models.whisper-tiny`** (already on disk):
   - **Model ID**: `whisper-tiny`
   - **Role**: `ci_fixture_asr` (NOT production)
   - **Family**: Whisper-class
   - **Backend**: faster-whisper (ctranslate2)
   - **License**: MIT (OpenAI Whisper original release · Systran faster-whisper conversion)
   - **Origin URL**: `https://huggingface.co/Systran/faster-whisper-tiny`
   - **Weights SHA256**: `dcb76c6586fc06cbdac6dd21f14cfd129cc4cdd9dce19bf4ffa62e59cbe6e6d1`
   - **HF snapshot revision**: `d90ca5fe260221311c53c58e660288d3deb8d356`
   - **Purpose (verbatim)**: "CI CPU-mode ASR fixture model. NOT for production use. Production model lands additively at 9.2b via v0 -> v1 registry bump per Owner ruling."

2. **`models_registry.v0.json` §`authority_source`** (verbatim Owner ruling 9.2a-E1 α + seed-with-CI-fixture correction 2026-07-10):
   > "the registry does NOT seed empty — it seeds with the CI fixture model's entry. Empty per data-blind misapplies the posture: data-blind governs assumptions about the estate's content, not tool provenance — a model registry entry is tooling attestation, and an empty registry plus a provenance gate is the CD-E3 deadlock again (nothing can pass). Seed models_registry.v0.json with whisper-tiny pinned (SHA + license + origin URL) as the CI fixture model; production models land additively at 9.2b via the registry bump, selected then."

3. **`Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` §3 (Tokenized Audio Representation)**:
   - Spec introduces a NEW model class: the **audio codec** (`perception/audio_codec/`).
   - Function: pretraining unsupervised on unlabelled estate audio; outputs `{ content_tokens[], character_stream, codec_version }` per segment.
   - Target token rate: 50–100 tokens/second of audio.
   - Registration: "registered like any other perception model; census-visible; runs in-perimeter on tenant compute."
   - **[VERIFY] item §16.1** — perception router carries a second output stream per segment or the character stream needs its own artifact type.
   - Spec does NOT name a specific codec candidate. Choice is deferred to Sampling & Reflection machinery per Open Decision §16.2 (last bullet).

4. **§4.1 (Language identification)**:
   - "A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."
   - No specific model named.

5. **§5 (Character Register / Learning)** and **§7 (Voice identity synthesis)**:
   - Both consume the codec's `character_stream`. No separate base model named.
   - Voice synthesis rendering is P2 (§7.5 scope note).

**Audio-modality base-model status** (as of this reading):

| Function | Named model | License | Status on Extraction-Akki disk |
|----------|-------------|---------|--------------------------------|
| ASR (CI fixture) | `whisper-tiny` | MIT | Registered (SHA-pinned) |
| ASR (production) | — not named — | pending 9.2b registry bump | Registry v0 · production row pending Owner naming at first census activation |
| Audio codec | — new build (unsupervised pretraining on estate audio) — | own — codec is a commissioned job under the standard contract | BUILD (§16.2 Open Decision: "Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built") |
| Segment language ID | "lightweight offline · CPU-viable · in-perimeter" | — | BUILD (unnamed candidate) |
| Diarization / speaker attribution | — pyannote provider path referenced in `diarization_worker.py` — | — | Provider path on disk (`backend/services/perception/diarization_worker.py`) — specific model not fixed by spec |

### 2.2 · Text modality

Authority anchors:

1. **`models_registry.v0.json` §`c1_candidates.qwen3_family`** (already on disk):
   - **Class**: C1
   - **Family**: Qwen3 / Qwen3.5 (Alibaba Cloud)
   - **Modality**: text
   - **Role**: `text_generation_candidate`
   - **License**: Apache-2.0
   - **License verification URL**: `https://huggingface.co/Qwen`
   - **Checksum policy**: "SHA-256 pinned per member at acquisition"
   - **Specific members**: "Named at first census activation (Owner-ruled)"

2. **`models_registry.v0.json` §`c1_candidates.llama_family`** (already on disk):
   - **Class**: C1
   - **Family**: Llama (Meta)
   - **Modality**: text
   - **Role**: `text_generation_comparison_arm`
   - **License**: `verify_at_acquisition` (Llama license has commercial-use gates that require attestation at acquisition)
   - **License verification URL**: `https://ai.meta.com/llama/license/`
   - **Purpose**: "C1 candidate row as text-generation comparison arm to Qwen. Modality-symmetric registration only."

3. **`Akki_Training_Techniques_Spec.txt` §2 T-1.5 (Foundation methods, FACT)**:
   > "LoRA/PEFT adapters on registered open bases; training material drawn exclusively from de-duplicated, VAD-cleaned, qualified units; acceptance exclusively through MOAC on uncurated held-out sets."

   Interpretation: the base is one of the C1 candidates registered above; adapter methodology (LoRA/PEFT) is FACT-class.

**Text-modality base-model status** (as of this reading):

| Function | Named model | License | Status on Extraction-Akki disk |
|----------|-------------|---------|--------------------------------|
| Text generation (primary) | Qwen3 / Qwen3.5 (family — specific member pending) | Apache-2.0 | C1 candidate row (class-level) — specific member "Named at first census activation" |
| Text generation (comparison arm) | Llama (family — specific member pending) | verify_at_acquisition | C1 candidate row (class-level) — specific member "Named at first census activation" |
| Adapter methodology | LoRA/PEFT (T-1.5 FACT) | — | BUILD (trainer runner is CP8 · gated on SSH + rights) |

### 2.3 · Document / Vision modalities (registered classes only · no members yet)

- **document_ocr_class** — Class C1 · role `document_ocr_candidate` · license `per_member` · specific candidates named at first census activation.
- **vision_class** — Class C1 · role `vision_perception_candidate` · license `per_member` · specific candidates named at first census activation.

## §3 · Optimizer selection · protocol notes

`Akki_Training_Techniques_Spec.txt` §3 (T-2 protocol) governs optimizer selection:

- **T-2.1 Trigger**: protocol executes at first adapter training on real material, inside the P4-instrumented run.
- **T-2.2 Shape**: one two-arm comparison — baseline optimizer vs. candidate — identical training data · identical base model · identical eval sets · identical compute-budget cap · executed on smallest stratum that yields valid MOAC evaluation.
- **T-2.4 Verdict rule**: quality parity on M-a and M-b is MANDATORY for a candidate to remain eligible. Compute-to-convergence is REPORTED. **Adopt/reject decision is an Owner ruling made on the measured results; no adoption threshold exists in advance of the evidence.**
- **First named candidate**: **Muon** (§2 T-2 verbatim: "Muon is the first named candidate").
- **Baseline arm**: not named in spec; default is the T-1 recipe seat baseline once it is filled (T-1.2: seat ships EMPTY).

## §4 · Recipe seat · T-1 status

Per `Akki_Training_Techniques_Spec.txt` §2:

- **T-1.1**: All training configuration (optimizer + params, LR schedule, batch/epoch, adapter rank, target modules) MUST live under `training_params@v0`, a sidecar configuration class with the same discipline as `extraction_params@v0` — **versioned · ledgered · outside `contracts/` · no Parity contact**.
- **T-1.2**: The seat ships EMPTY. No default recipe exists until the first training run fills it through the §3 protocol.
- **T-1.3**: Every trained model's registry entry MUST cite the `recipe_version` that trained it. MOAC M-d (lineage) extends by this field.

**Status on Extraction-Akki disk**: `backend/contracts/extraction_params.py` exists (the analog pattern). `training_params@v0` sidecar does NOT exist yet — pending CP5 (per W11 reassessment §5.2).

## §5 · Answers to Owner Step A

**Q**: What are the pre-defined base-model choices per modality (audio vs text)?

**Answer**:

- **Audio · ASR · CI-fixture level**: `whisper-tiny` (MIT · Systran faster-whisper conversion · SHA-pinned at `dcb76c6...cbe6e6d1`) — already on disk in the seeded v0 registry. This is the only concrete audio model pinned.
- **Audio · ASR · production level**: NOT NAMED IN CANON. Registry v0 authority anchor states production models land additively at 9.2b via v0→v1 registry bump; owner selects at first census activation.
- **Audio · Codec**: NOT NAMED. Spec §3 requires a codec service that pretrains unsupervised; specific existing-codec vs. train-estate-specific is an **Open Decision** in §16.2 answered by Sampling & Reflection once built.
- **Audio · Language ID**: NOT NAMED. Spec §4.1 constrains only that it be lightweight, offline, CPU-viable, in-perimeter.
- **Text · Primary arm**: **Qwen3 / Qwen3.5 family** (Apache-2.0) · specific member Named at first census activation.
- **Text · Comparison arm**: **Llama family** (Meta, verify_at_acquisition) · specific member Named at first census activation.
- **Text · Adapter methodology**: LoRA/PEFT (FACT · T-1.5).
- **Document · OCR**: candidate CLASS registered; no member named.
- **Vision · Perception**: candidate CLASS registered; no member named.
- **Optimizer · First candidate**: **Muon** (T-2 protocol) · baseline arm = whatever fills the T-1 seat on first training run.

## §6 · What the Owner must supply before real training fires (CP8 gate)

1. **Census activation**: pick a specific member of the Qwen3/Qwen3.5 family (e.g., a specific parameter count · tokenizer variant · HF revision) OR name the specific Llama member.
2. **License attestation on Llama** (if chosen) — the `verify_at_acquisition` flag requires an Owner-signed license verification per row before the acquisition harness may proceed.
3. **Codec ruling**: adopt open codec (name it) OR commission estate-specific codec (unsupervised pretraining job).
4. **Language ID picker**: name the offline CPU-viable model (e.g., fastText LID.176, whisper-language-id small variant, or similar).

None of these block CP2 (Critic Seam LIFT) or CP3 (Demand Table + Capacity Ledger + Test-set seal + Training panel).

## §7 · No policy change proposed by this note

This is a reading receipt. No inferences drawn beyond what the canon and registry state verbatim. The single non-verbatim claim — that the audio codec "is a NEW model class to be built via unsupervised pretraining" — is directly quoted from spec §3 (Pretraining row of the §3.2 technical contract table).

---

**Step A: DONE.** Proceeding to Step B (CP2 · Critic Seam LIFT).
