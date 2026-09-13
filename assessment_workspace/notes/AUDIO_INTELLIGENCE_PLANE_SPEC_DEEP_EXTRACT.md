# Audio Intelligence Plane Spec v1.0 — Deep Technical Extract (read-only)

**Task class:** DEEP REQUIREMENT-DOC EXTRACTION · read-only · no build, no code commits, no push, ratchet 3251 untouched. POC HOLD in force.
**Directive received:** 2026-09-12T~13:15Z (owner).
**Executor:** track-a agent, re-grounded from `STATE/STANDING_ORDERS.md`, `STATE/DECISIONS.md` (Owner Ruling 2026-09-12T~12:00Z banked), `STATE/NEXT.md`.
**Retraction acknowledged:** owner's "ChatGPT AI Models integration" request is retracted — no OpenAI/ChatGPT reference anywhere in this document.

**Discipline for this extract:**
- Every technical clause below is a **VERBATIM quote** from the source document (spec / contract / atomic module docstring / code), delimited with `>` blockquote when spec prose and with fenced code when code. Paraphrase is FORBIDDEN in the spec-content sections.
- Every clause carries its §-anchor (`Audio Plane §X.Y`) and where relevant its file:line locator.
- Where the spec is **SILENT** on a technical question the owner asked, the row says `SILENT` explicitly. Silence is a finding; it means the platform must author that policy before an autonomous run of that shape can occur.
- Where a spec clause has [VERIFY] against current code, this document resolves the verification directly against `programme/track-a` HEAD `77834d1` files opened this session.

**Ground state:** ratchet floor **3251**; workspace `master` HEAD `18b301fd` (prior capability assessment); `programme/track-a` HEAD `77834d1`; nothing else touched.

---

## §0 · Sources actually opened this session

Every line in this document was pulled from a file opened in this session. File locators + line ranges below.

| Source | Path | Lines opened |
|---|---|---:|
| **Audio Intelligence Plane Specification v1.0** (canonical .md) | `canon/text/Audio_Intelligence_Plane.md` | 1–431 (full) |
| Audio Plane duplicate (byte-parallel .txt) | `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` | 1–303 (full) |
| Contract · `AudioSegmentV0` | `repos/Extraction-Akki/backend/contracts/audio_segment_v0.py` | 1–83 (full) |
| Contract · `PerceptionJob_v0` | `repos/Extraction-Akki/backend/contracts/perception_job_v0.py` | 1–77 (full) |
| Contract · `PerceptionResult_v0` (+ `Telemetry`, `Checkpoint`, `PurgeAttestation`) | `repos/Extraction-Akki/backend/contracts/perception_result_v0.py` | 1–79 (full) |
| Contract · `SignalRing` v0 catalogue | `repos/Extraction-Akki/backend/contracts/signal_ring.py` | 1–68 (full) |
| Contract · `extraction_params@v0` catalogue | `repos/Extraction-Akki/backend/contracts/extraction_params.py` | 1–307 (full) |
| Atomic · A1.1 demux | `repos/Extraction-Akki/backend/services/perception/eab_1_pipeline/a1_demux.py` | 1–83 (full) |
| Atomic · A1.2 segmentation | `.../a1_segmentation.py` | 1–124 (full) |
| Atomic · A1.3 VAD | `.../a1_vad.py` | 1–141 (full) |
| Atomic · A1.4 dedup | `.../a1_dedup.py` | 1–130 (full) |
| Atomic · A2.1 occurrence writer | `.../a2_occurrence_writer.py` | 1–162 (full) |
| Atomic · A2.2 licence class | `.../a2_license_class.py` | 1–53 (full) |
| Atomic · A2.3 trace walker | `.../a2_trace_walker.py` | 1–87 (full) |
| Provider · Whisper API (cloud) | `.../services/layer_b/asr/whisper_provider.py` | 1–56 (full) |
| Provider · faster-whisper (local) | `.../services/layer_b/asr/faster_whisper_provider.py` | 1–90 (full) |
| Provider · pyannote diarization | `.../services/layer_b/diarization/pyannote_provider.py` | 1–80 (full) |
| Layer-B contracts + factory | `.../services/layer_b/{contracts.py, factory.py}` | 1–112, 1–94 |
| GPU execution · CPU/GPU selector | `.../services/perception/gpu_execution/cuda_runtime.py` | 1–52 (full) |
| GPU execution · audio batching | `.../services/perception/gpu_execution/audio_batching.py` | 1–33 (full) |
| GPU execution · model loader | `.../services/perception/gpu_execution/model_loader.py` | 1–46 (full) |
| Companion spec · EAB Tier-1 Adoption v1.1 (§1-§10 A1..A5 + F1..F3 + ES-1..ES-5 + P1..P4) | `repos/Extraction-Akki/docs/requirements/eab_tier1_adoption_spec_v1.1.md` | 1–217 (full) |

---

# PART I · AUDIO INTELLIGENCE PLANE — §1 through §16

## §1 · Governing Doctrine (5 principles)

> **"Five principles govern every clause in this specification. Where a later clause appears to conflict with one of these, the principle wins and the clause is defective."** (Audio Plane §1, opening)

### §1.1 · Recursion — every audio file is an estate

> **"The archive is an estate; a programme is an estate; a single file is an estate. Segments are rows; the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns; no schema exists until one is declared. Census, admission, registry, and record apply at every scale."**

**Data-point decomposition per the spec (the "columns" enumerated verbatim):**
1. content
2. language
3. condition
4. prosody
5. occurrence
6. code-switch
7. music
8. group-level character

This IS the spec's atomic answer to "what is a data point in an audio file". The spec declares **8 orthogonal extractable-layer columns** with a row-per-segment framing.

### §1.2 · Modality extension, not parallel machinery

> **"The audio plane introduces no sibling services. Mtafiti gains an audio modality; Northena gains audio data classes; the wizard gains an objective variant; Targeta gains a training object. Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."**

### §1.3 · One record

> **"Mtafiti and Northena collaborate to produce a single record, written once. Working state — loss curves, intermediate metrics, partial coverage counts — is scratch, not truth; it becomes record only when finalized and stamped. No local ledger exists. If a measured throughput ceiling ever demands relief, the relief is batched stamping (one row certifying N events with a digest), which remains a single record. That change is made only when a measurement demands it."**

### §1.4 · Measure, do not assert

> **"No data-volume requirement, accuracy expectation, or cost figure is quoted without a measurement behind it. The calibration stage exists to convert assertions into measurements before commitment."**

### §1.5 · Unrepresentable, not policed

> **"Safety boundaries are enforced by making the violating state impossible to express in the contract — the pattern established by the assertion floor — not by review after the fact. The Character Register write path (§6) and the voice identity distance gate (§7) both follow this pattern."**

**Doctrine-level SILENCE findings from §1:** none — five principles are stated exhaustively.

---

## §2 · Capability Statement and Plane Overview

> **"Given governed access to an audio estate, the plane provides four functions in one loop:**
> **• Extraction — audio is converted into provenance-paired facts: transcripts, entities, occurrences, and character observations.**
> **• Learning — a Character Register accumulates group-level knowledge of how the estate's languages and audio behave.**
> **• Training — model production is commissioned against a falsifiable Target Outcome, planned and priced before compute is spent, with per-example provenance.**
> **• Invention — synthesized voice identities are constructed from the register: authentically of the language, provably of no individual."**
>
> **"Each function feeds the next: extraction populates the register; the register defines the strata training plans against; trained models improve extraction; invention consumes the register's learned layers. The loop is the capability."**

**Flow of a commission, end to end** (verbatim from §2):

> Objective Wizard session → compile {TargetOutcome, Collection Schema}
> → Sampling & Reflection (calibration) → proposed Milestones + priced quote
> → Owner agrees milestones → Commission opens
> → Collection → Register update → Curriculum → Training runs → Certificates
> → Commission View reports against milestones throughout → Commission sealed

**Note on this flow:** the loop is **extraction → learning → training → invention**, not merely "extraction to sellable corpus". The spec's canonical loop is broader than the immediate audio-census objective — the corpus is one deliverable class INSIDE the extraction step; the register + training + invention capabilities all share the same substrate.

---

## §3 · Tokenized Audio Representation

### §3.1 · Behaviour (verbatim, four bullets)

> **"• All downstream audio work — extraction, character analysis, training — operates on discrete token sequences produced by a neural audio codec, not on waveforms.**
> **• Tokenization exposes two separable streams per segment: the content stream (what was said — input to ASR/NER) and the character stream (how it was said — input to the Character Register). The character stream is retained and routed, never discarded as noise.**
> **• Control markers (language, register, segment type) are splice-able tokens, enabling one model per estate rather than one per language, and native handling of code-switched speech.**
> **• Failure behaviour: audio in an unsupported condition fails closed with a stated reason. The codec never silently degrades quality."**

### §3.2 · Technical contract (verbatim table)

| Item | Specification |
|---|---|
| Service | `perception/audio_codec/` — registered like any other perception model; census-visible; runs in-perimeter on tenant compute. |
| Input | Audio segment (bounds per ingestion segmentation) + declared or detected condition profile. |
| Output | `{ content_tokens[], character_stream, codec_version }` Target token rate **50–100 tokens/second of audio**. |
| Provenance | `codec_version` is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens. |
| Pretraining | The codec pretrains **unsupervised on unlabelled estate audio**, under the standard commissioned-job contract. |
| [VERIFY] | Perception router contract: where model registration occurs, and whether the router carries a second output stream per segment or the character stream requires its own artifact type. |

### §3.3 · Acceptance criteria (verbatim)

> **"• Round-trip fidelity is measured and recorded per codec version before that version serves any commission.**
> **• A downstream artifact lacking codec_version in provenance is rejected at the registry boundary.**
> **• An unsupported-condition input produces a refusal with a stated reason and no output artifact."**

### §3 · SILENCE findings

- **Codec CHOICE is SILENT.** No named codec (no reference to EnCodec, DAC, SoundStream, HuBERT, wav2vec2). §16.2 defers: *"Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built."*
- **Fidelity METRIC is SILENT.** "Round-trip fidelity" is not defined as PESQ, ViSQOL, STOI, or a bit-exact test. The measurement method is un-named.
- **Character-stream data structure is SILENT.** `character_stream` is not defined — no dimensionality, no vocabulary size, no sampling rate. §16.1 flags this: *"whether the router carries a second output stream per segment or the character stream requires its own artifact type."*

### §3 · Contract linkage

`contracts/audio_segment_v0.py` field-for-field:
```python
class AudioSegmentV0(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    segment_id: str = Field(..., min_length=1)
    estate_ref: str = Field(..., min_length=1)              # §1.1 recursive framing
    codec_service: Literal["perception/audio_codec"] = ...  # §3.2 exact literal
    content_stream_tokens: List[int] = Field(..., min_length=1)      # §3.1 content stream
    character_stream_tokens: List[int] = Field(..., min_length=1)    # §3.1 character stream · never empty per §1.5
    condition_profile: str = Field(..., min_length=1)                # §3.2
    bounds_start_ms: int = Field(..., ge=0)
    bounds_end_ms: int = Field(..., ge=0)
    tokenised_at: str = Field(..., min_length=1)
```
**Enforced by §1.5 unrepresentable pattern:** both `content_stream_tokens` and `character_stream_tokens` are `min_length=1` — a segment WITHOUT a character stream cannot construct. `codec_version` per §3.2 is required in provenance but the contract's `codec_service` is a hard-coded Literal, NOT a version — the version field itself is **NOT PRESENT on the contract**. Gap flagged below.

---

## §4 · Extraction Layer

### §4.1 · Language identification (verbatim)

> **"Behaviour: every segment carries a real language signal. The current plumbing value (language_hint: None) is retired.**
> **• A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion.**
> **• Recorded per segment: languages[], confidences, and code-switch points where multiple languages occur in one utterance.**
> **• The signal routes downstream model selection (ASR path, NER path, de-identification path) and is written into provenance.**
> **[VERIFY] Segment boundaries in current ingestion — confirm the unit to which a language label attaches."**

**Spec-level LID requirements:**
1. Lightweight — the spec's own word.
2. Offline — the spec's own word (no cloud LID service).
3. CPU-viable — the spec's own word.
4. In-perimeter — no boundary crossing for the LID call.
5. Per-segment granularity.
6. Emits `languages[]` (plural), `confidences[]` (plural), and code-switch points.
7. Signal is provenance-written AND routes downstream model selection.

**SILENCE findings on LID:**
- **No named LID model.** SILENT on Whisper's language detection, MMS-LID (Meta 1,100+ language classifier), CLD3, Google's IDs, or any other named model.
- **No confidence-calibration policy.** SILENT on what confidence threshold defines "clearly language L" vs "ambiguous", vs "code-switched". The spec asks for `confidences[]` but does not floor them.
- **No abstain / unknown-language behaviour.** SILENT on what to do if all confidences are below any threshold. `§4.6` acceptance criterion requires `languages[]` to be present in provenance — but an empty list would satisfy this by min-length rule; the spec doesn't require min_length ≥ 1.

### §4.2 · Code-switch points as facts (verbatim, whole section)

> **"Switch points (position, from-language, to-language, context class) are registered facts with provenance — not preprocessing metadata. They populate the register's code-switch layer and stratify test sets."**

**Spec-level code-switch requirements:**
1. Data shape: `{position, from-language, to-language, context class}` — four fields.
2. Class: registered FACT with provenance — not throwaway metadata.
3. Two consumers: (a) Character Register code-switch layer (§5.2); (b) test-set stratification (§10.1).

**SILENCE findings:**
- **`context class` values SILENT.** No enumeration of what a "context class" can be (news, casual, formal, conversational, emotive, etc.). The spec doesn't define the vocabulary.
- **`position` unit SILENT.** Not stated whether position is a time offset (ms), a token offset (into the content stream), a word offset, or a character offset.
- **Multi-language switch (3+ languages in one utterance) SILENT.** The pair `{from, to}` implies binary switch; a Kikuyu → Swahili → English three-way switch has no data-shape declared.

### §4.3 · Condition profiling (verbatim, whole section)

> **"Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion. It is cheap to compute, directly predictive of extraction error, and required for training stratification. It is captured at first ingestion because re-ingesting an estate to recover it is the unaffordable mistake."**

**Spec-level condition-profile dimensions (named verbatim):**
1. Channel condition — studio / field / telephone band.
2. Transmission artefacts.
3. Background class.

**SILENCE findings:**
- **Enumeration for each dimension SILENT.** "studio / field / telephone band" is illustrative not exhaustive; the spec does not enumerate all channel classes. "transmission artefacts" is a class label with no sub-classes. "background class" is a class label with no sub-classes.
- **Metric SILENT.** No SNR floor, no bandwidth cutoff, no noise-floor threshold defining "telephone band" numerically.
- **Detection method SILENT.** "Cheap to compute" — no reference to classical DSP features (MFCC, spectral flatness, spectral rolloff, zero-crossing rate, PLP), no reference to a neural condition classifier.

### §4.4 · Synthesis-relevant attribute capture (verbatim, whole section)

> **"During the same ingestion pass, group-level acoustic attributes required by any future synthesis capability (pitch statistics, energy contours, duration patterns) are captured, subject to the custody conditions of §6.4. This forecloses nothing and costs little; omitting it forecloses the invention function or forces re-ingestion."**

**Named acoustic attributes (verbatim):**
1. Pitch statistics.
2. Energy contours.
3. Duration patterns.

**SILENCE findings:**
- **Pitch statistics: what statistics? SILENT.** Mean/median F0? Range? Standard deviation? Voiced-fraction? The spec is silent.
- **Energy contour shape SILENT.** Not stated whether this is raw RMS-per-frame, dB-per-frame, or a parametric envelope model.
- **Duration patterns SILENT.** Not stated whether this is syllable/phoneme duration, silence gap duration, or utterance-length statistics.
- **§6.4 backreference: idiolect rule.** These attributes are **excluded from individual-storage** by §6.2 conjunctive four conditions (see §6 below) — the spec is explicit that pitch/energy/duration are captured at GROUP level only, never per-speaker.

### §4.5 · Deduplication as augmentation (verbatim, whole section)

> **"The occurrence index already identifies repeated content. Its output contract is extended: for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored; the variant set enters training curricula as a designated robustness stratum at zero acquisition cost. No new detection work; this is a change to what dedup keeps."**

**Spec-level dedup contract:**
- Extends existing occurrence index (from EAB v1.1 §3).
- Each dedup item retains a **variant set**: `{channel, time, condition}` per instance.
- One canonical is stored; variant set enters training curricula as a **robustness stratum**.

### §4.6 · Acceptance criteria (verbatim)

> **"• No segment leaves ingestion without languages[], condition profile, and (where applicable) switch points in provenance.**
> **• A deduplicated item without its instance condition map fails the ingestion invariant test.**
> **• Baseline-tier capture (§9.2) runs for all admitted material regardless of any active objective."**

---

## §5 · The Character Register — Learning

### §5.1 · Definition (verbatim)

> **"A registry-modality store of learned, group-level audio characteristics, built from the character stream. Same doctrine as the fact registry: every entry carries provenance to source material and an occurrence count. It is Mtafiti's qualification-and-index doctrine applied to acoustic observations — an extension, not a sibling (§1.2)."**

### §5.2 · Layers (verbatim table)

| Layer | Contents | Primary consumers |
|---|---|---|
| **Phonetic** | Per-lexeme pronunciation variants, frequency, regional distribution. | Curriculum; extraction lexicons; evaluation stratification |
| **Prosodic** | Intonation contours, stress, rate distributions, pause structure. | Training; programme-type classification |
| **Condition** | Channel and environment profiles. | Stratification; error prediction |
| **Code-switch** | Switch-point patterns, language pairs, context classes. | Training; test-set design |

### §5.3 · Build process (verbatim)

> **"Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."**

**Spec-level clustering requirements:**
- Unsupervised.
- Over the character stream (not the content stream).
- Emits **candidate strata**, not final labels.
- Naming/validation is **human**, per-sample, commissioned as qualified work.

**SILENCE findings on Character Register:**
- **Clustering algorithm SILENT.** No mention of k-means, HDBSCAN, agglomerative, spectral, DBSCAN, Gaussian mixture, VAE-latent-clustering, or any other named method.
- **Cluster-count discipline SILENT.** No k, no threshold, no silhouette-score policy.
- **"Occurrence count" per entry — unit SILENT.** Number of segments? Number of speakers-attributed? Number of programme-blocks? Not specified.
- **Human-sample size SILENT.** "Applied to a sample" — no N per cluster, no confidence-based sampling policy.
- **Storage format SILENT.** Named as "centroids, distributions, frequencies" (§6.2 bullet 4) — but no schema.

---

## §6 · Register Custody Boundary

### §6.1 · Governing distinction: organic vs learned (verbatim)

> **"Organic characteristics are anatomical — vocal tract length, formant structure, glottal source, fundamental frequency range. They cannot be acquired or shed; they are what speaker verification keys on; they are biometric. They are never registered.**
>
> **Learned characteristics are acquired from a speech community — phonological inventory, pronunciation variants, prosody, code-switching habits. They are group properties by construction. Only learned characteristics may be registered."**

**THIS is the spec's answer to the owner's "unique identifiers (biometric) for language and individuals" question. The spec draws its line HERE:**

- **Organic (biometric, never stored):** vocal tract length · formant structure · glottal source · fundamental frequency range.
- **Learned (group-level, may be stored):** phonological inventory · pronunciation variants · prosody · code-switching habits.

**The spec does not authorise a per-speaker biometric identifier.** Per-individual identity is the exact thing §6 makes structurally impossible. Owner Ruling #5 (banked in DECISIONS 2026-09-12T~12:00Z) — *"extract all context you can"* — sits on top of §6 as a HIGHER-LEVEL admission for the DETECT half only; §6 says the STORAGE half can only bank group-level primitives. Reconciled below (see §Autonomy).

### §6.2 · The four conditions — all must hold (verbatim)

> **"• Acquired, not anatomical. The attribute is learnable by a speaker from a different background.**
> **• Shared. Observed across at least N distinct speakers. N is a governed seam value; its default inherits the platform minimum-group-size parameter unless the tenant sets a register-specific value.**
> **• Non-reconstructive in combination. Tested against attribute combinations, not attributes in isolation: language + region + age band + one distinctive feature can reach a single person even when each attribute is group-level.**
> **• Stored as description, not exemplar. Centroids, distributions, frequencies. Never stored audio; never per-utterance speaker embeddings. Embeddings used during clustering are destroyed after cluster assignment. Provenance points to material, not to speaker identity."**

**Four conditions are CONJUNCTIVE — all must hold** (spec's own word: "all must hold" in the header).

**Enumeration of forbidden storage classes** (verbatim from bullet 4):
1. Stored audio.
2. Per-utterance speaker embeddings.
3. Clustering embeddings after cluster assignment.

### §6.3 · Enforcement shape (verbatim)

> **"The register write path exposes no field through which an instance-level representation can be stored: the schema cannot represent a voiceprint. Unrepresentable, not policed (§1.5). An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."**

**Named leakage paths for the invariant test** (verbatim):
1. Small stratum.
2. Idiolect marker.
3. Narrowing combination.
4. Exemplar storage.

### §6.4 · Idiolect rule (verbatim, whole section)

> **"Habitual fillers, characteristic phrasings, and idiosyncratically pronounced words are learned but individuating. They fail condition 2 or 3 and are excluded. 'Learned' alone is never sufficient; the four conditions are conjunctive."**

### §6 · SILENCE findings

- **Value of N for condition 2 SILENT.** *"platform minimum-group-size parameter"* — the parameter is referenced but its default value is not in this spec. §16.2 opens it: *"N for the shared-attribute condition (§6.2.2): inherit the platform minimum-group-size seam value, or set a register-specific one."*
- **"non-reconstructive in combination" test SILENT.** The spec asserts the property must hold; it does not name a formal test (k-anonymity, l-diversity, differential-privacy epsilon). Owner Ruling #5 does not extend it.
- **"Provenance points to material, not to speaker identity" — mechanism SILENT.** How the storage-side breaks the pointer from a stored `centroid` to a speaker-identifiable trace is not specified; §6.3's "unrepresentable" pattern names the property but not the exact schema slot deletion.

---

## §7 · Synthesized Voice Identity — Invention

### §7.1 · Mechanism (verbatim)

> **"• Learned characteristics are inherited from the register — this is what makes the voice sound like a speaker of the language rather than a foreigner reading it.**
> **• Organic characteristics are constructed — vocal tract parameters, F0 range, formant structure, glottal parameters are chosen as a point in acoustic space that no real speaker occupies.**
>
> **This is the inverse of a voice clone. A clone copies the organic and frequently gets the learned wrong; this gets the learned right and owns the organic outright."**

### §7.2 · The distance guarantee (mandatory, fail-closed) (verbatim, whole section)

> **"Every constructed identity is scored against every speaker representation derivable from the corpus using standard speaker-verification methods. A minimum distance from all of them is required. Below threshold, the identity is rejected and resampled. There is no override. The threshold value and the verification method are recorded with the identity."**

**Spec-level distance-gate requirements:**
- Every constructed identity scored against **every** derivable speaker representation.
- Verification method: **"standard speaker-verification methods"** — spec doesn't name one but implies existing SOTA.
- Fail behaviour: **rejected AND resampled**, no override.
- Recorded per identity: threshold value + verification method.

### §7.3 · The certificate (verbatim, whole section)

> **"A passing identity is issued a certificate stating that the voice is provably derived from no individual, naming the method, the threshold, and the corpus version scored against. The certificate is a first-class sellable artifact."**

### §7.4 · Identity composition + versioning (verbatim table)

| Component | Source |
|---|---|
| **Acoustic identity** | Constructed organic parameters (§7.1). |
| **Speech character** | Inherited from register — phonetic and prosodic layers. |
| **Interaction character** | Turn-taking, formality, code-switch behaviour — inherited from register. |

> **"Each identity is a versioned artifact with a ledger entry. Changing one is a ceremony with the standard waiting period, because audience recognition accrues to the voice and recognition is the asset. Identities never drift."**

### §7.5 · Scope note (verbatim)

> **"Rendering requires a synthesis stack, which is a separate build from recognition. What this specification requires now is non-foreclosure: the identity specification (attribute schema, distance method, certificate format) is defined, and §4.4's ingestion capture ensures the substrate exists when rendering is built."**

### §7 · SILENCE findings

- **Named distance-verification method SILENT.** "Standard speaker-verification methods" is a shape not a choice. No mention of x-vectors, ECAPA-TDNN, ResNet-based speaker-embedding, cosine vs Euclidean distance, EER anchoring.
- **Threshold value SILENT.** The threshold is required to be *recorded* per identity — the FLOOR value is not stated. This is a policy decision the spec explicitly refuses to make.
- **Certificate format SILENT.** No schema.

---

## §8 · The Objective Wizard — Schema Compiler

### §8.1 · Role (verbatim)

> **"No business user hand-writes a Target Outcome. The Objective Wizard — a new variant of the existing shaping wizard, reusing its agent interface, guards, session persistence, and ledger sidecar — elicits an objective in plain language and compiles two governed artifacts:**
> **• TargetOutcome (§10) — handed to the Training Planner.**
> **• Collection Schema (§9) — the data dictionary for this objective: which data points are extracted from the sound, at what granularity, at what quality bar."**

### §8.2 · Elicitation sequence (verbatim, four bullets)

> **"• The question the model must answer — operational and falsifiable.**
> **• The population — resolved against existing register strata; unresolved populations are flagged as unmeasured and generate census work.**
> **• The acceptance bar — per stratum, two-dimensional (§10), with the gate-or-document decision recorded explicitly.**
> **• The collection consequences — the wizard derives required columns, shows which are already collected (baseline tier), which exist but are uncollected, and the cost of collecting them. The owner sees the price of the schema before commissioning."**

### §8.3 · Dynamism within scope: propose, qualify, graduate (verbatim, three bullets)

> **"• Propose. The agent side may propose novel data points no prior objective collected. This is where innovation enters.**
> **• Qualify. A proposed column never enters collection directly. It is admitted as a candidate: collected on a sample only, its evidence of value measured against the objective — the same qualification path any fact travels.**
> **• Graduate. Qualified candidates graduate into the objective tier for that commission. Graduation into the baseline tier is ceremony-governed (proposal, countersignature, waiting period), because a baseline column is paid on every hour ingested for the life of the estate."**
>
> **"The compile stage is deterministic throughout: the agent proposes; only qualified columns compile. Mechanical guards prove against a stub agent before any LLM is plugged in, per the existing standing disposition."**

### §8.4 · Compile-time rejections (verbatim, three bullets)

> **"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned:**
> **• An Outcome without an existing test_set_ref.**
> **• An acceptance bar missing the per-stratum dimension.**
> **• A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."**

### §8.5 · Record and handoff (verbatim)

> **"Every session stamps to the ledger via the existing turn-ledger pattern under a distinct data class (objective_session), including options considered and rejected — which is what makes a later 'why was the model built this way' answerable. Compiled artifacts hand off to Targeta through the existing admission-handoff pattern. Objective → schema → plan → run is one provenance chain."**

### §8 · SILENCE findings

- **The stub-agent proof mechanism referenced (§8.3 last paragraph "Mechanical guards prove against a stub agent before any LLM is plugged in") points to *"the existing standing disposition"* — which specific test/harness is SILENT.**

---

## §9 · The Collection Schema

### §9.1 · Definition (verbatim)

> **"The declared data dictionary of a commission: what is extracted from the sound, for what purpose, at what quality bar. It is the admission standard of the audio estate, per objective (§1.1). It has two tiers."**

### §9.2 · Baseline tier (verbatim, whole section)

> **"Standing, objective-independent, collected at first ingestion for all admitted material. Membership criterion: cheap to collect now, unaffordable to collect later. Contents at v1.0: language identification, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group-level acoustics (§4). Changes to the baseline are seam-governed — ceremony, countersignature, waiting period — because silently narrowing the baseline is how an estate quietly becomes unre-readable."**

**BASELINE-TIER CONTENTS at v1.0 (verbatim, five columns):**
1. Language identification.
2. Code-switch points.
3. Condition profile.
4. Dedup instance condition map.
5. Synthesis-relevant group-level acoustics (§4.4).

### §9.3 · Objective tier (verbatim)

> **"Declared per commission by the Objective Wizard. Collected against material already in governed scope, priced before collection starts, recorded in the commission's registry namespace. Candidate columns enter through propose–qualify–graduate (§8.3) only."**

---

## §10 · The Target Outcome

### §10.1 · Schema (verbatim, whole block)

> ```
> TargetOutcome {
>   task          operational statement of what the model must do
>   domain        context of use
>   population    defined by reference to register strata, not labels
>   acceptance    threshold per stratum; two-dimensional (accuracy, coverage)
>   gate_policy   per Outcome: missed stratum gates release | ships documented
>   test_set_ref  must exist before the Outcome is accepted
>   constraints   latency, compute budget, deployment target
> }
> ```

**Verbatim schema fields (7 named):**
- `task` (operational, falsifiable)
- `domain`
- `population` (register-strata-defined, not labels)
- `acceptance` (per-stratum, 2D — **accuracy × coverage**)
- `gate_policy` ∈ {missed_stratum_gates_release, ships_documented}
- `test_set_ref` (must pre-exist)
- `constraints` (latency + compute budget + deployment target)

### §10.2 · Binding rules (verbatim, four bullets)

> **"• Population is register-defined. 'Language L, accent clusters 1–4, telephone band and studio, adult' — never 'speakers of L.' This is what makes coverage computable.**
> **• Acceptance is per stratum. A single global threshold hides the failure that matters: 94% on the majority variant and 61% on the rest passes one test and fails the one that decides whether the work reaches the people it was built for.**
> **• The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time.**
> **• The gate decision is recorded on the Outcome at definition — not decided ad hoc at ship time."**

**Verbatim example population (§10.2):** *"Language L, accent clusters 1–4, telephone band and studio, adult"*.

### §10 · SILENCE findings

- **Named acceptance METRIC SILENT.** Two dimensions are named (accuracy · coverage) — but for accuracy: WER? Character Error Rate? BLEU? For coverage: percentage of strata? Hours passed?
- **Gate-policy DEFAULT SILENT.** §16.2 (Open decisions): *"Platform default for gate_policy (§10.1) where an Outcome does not set it: missed stratum gates release, or ships documented. This default silently decides how minority-variant quality is treated under schedule pressure."*
- **`constraints` sub-schema SILENT.** Latency in ms? p50/p95/p99? Compute in GPU-hours or dollars? Deployment target enumeration?

---

## §11 · The Training Planner

### §11.1 · Architecture (verbatim, whole block + table)

> **"The existing planner pattern is reused unchanged: a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs."**

| — | Extraction planning (existing) | Training planning (new) |
|---|---|---|
| Object | Source locations | Register strata |
| Floor | Defensibility class | Acceptance threshold — accuracy × coverage |
| Output | Mining plan | Training plan + curriculum + milestones |

### §11.2 · Sampling & Reflection (calibration) — mandatory first stage (verbatim)

> **"Data requirements for low-resource fine-tuning are empirical; no analytical answer exists. The first commissioned stage is therefore a calibration: train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold. Only then is the full run quoted, with a stated confidence interval — never a point estimate. A plan without a calibration stage is rejected. The first job prices the real job."**

**Spec-level Sampling & Reflection requirements:**
- Train at **three to four data volumes**.
- Evaluate per stratum against test set.
- Fit **scaling curve**.
- Extrapolate to acceptance threshold.
- Quote full run with **confidence interval** (never point estimate).
- Plans without a calibration stage are **REJECTED**.
- **"The first job prices the real job."** — verbatim slogan of the spec.

### §11.3 · Milestones — the accountability output (verbatim)

> **"Sampling & Reflection has two customers. It prices the real job, and it authors the accountability structure: its output to the objective owner is not a curve but a proposed milestone list — the checklist of what must be done, in what order, for the commission to succeed. Each milestone carries a done-condition and an owner. The objective owner reviews and agrees the list at commission; from that point, all reporting is against it. Accountability is set before spend, not discovered during."**

### §11.4 · Planner outputs (verbatim, four bullets)

> **"• Coverage report — per target stratum: hours available, quality distribution, gaps, cost of closing each gap.**
> **• Curriculum — ordering and weighting across strata derived from the register, not from the corpus's natural distribution, which is always skewed toward whatever occurred most. The dedup instance condition map enters as a designated robustness stratum.**
> **• Proposed milestone list (§11.3).**
> **• Cost quote with a stated confidence interval."**

### §11.5 · Provenance through training (verbatim)

> **"Every training example carries its provenance into the training manifest. Consequences: rights are enforceable per example; an example whose rights lapse is identifiable and the affected models enumerable; and 'the trained model is the customer's property' is a statement backed by a manifest, not an assertion."**

### §11.6 · Run governance (verbatim)

> **"Training runs are commissioned jobs under the existing contract: quoted before start, metered during, certificated on completion. The completion certificate records compute consumed, data touched, manifest hash, and per-stratum results against the Outcome. Failed strata are reported as plainly as passed ones."**

### §11 · SILENCE findings

- **Scaling-curve family SILENT.** Power law? Chinchilla-style? Empirical piecewise? The spec asserts "fit the scaling curve" and moves on.
- **Confidence-interval width SILENT.** No 95% vs 90% specification.
- **Number of milestones SILENT.** "Proposed milestone list" — no count or granularity guidance.

---

## §12 · Record and Registry Integration

### §12.1 · Registry (Mtafiti audio modality) (verbatim, whole section)

> **"Per commission, a scoped namespace within the registry holds: the Collection Schema (versioned), collected data points mapped against it — with declared-but-not-yet-collected as first-class state — the strata referenced by the Outcome, and coverage state per stratum. Reads compose with the global registry; writes are namespace-scoped. On close, the namespace is sealed, not deleted: it is the record of what was collected and why, and the next objective's wizard session queries prior schemas and coverage so the second project starts from the first project's map."**

### §12.2 · Record (Northena data classes) (verbatim)

> **"Training-workflow operations stamp into the one ledger under training-specific data classes: collection events, calibration runs, curriculum decisions, milestone status changes, run certificates. The workflow's view of 'its' record is a scoped lens filterable by commission ID — a view, not a store. Working state (loss curves, intermediate metrics, partial counts) is scratch until finalized and stamped once (§1.3)."**

**Enumerated Northena data classes for training workflows (verbatim, five):**
1. Collection events.
2. Calibration runs.
3. Curriculum decisions.
4. Milestone status changes.
5. Run certificates.

---

## §13 · Surface Specification — the Commission View

### §13.1 · Scope (verbatim)

> **"This surface adjustment applies to all commissioned work on the platform — extraction, census, and training commissions alike, across every extraction type. No modality receives its own UI, and no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery."**

### §13.2 · Behaviour (verbatim, whole section)

> **"The surface is milestones. The artifacts are evidence behind them.**
> **• At Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. Commission does not open until it is agreed.**
> **• The Commission View reports against the agreed checklist: each milestone with its done-condition and owner; status in plain terms — done, on track, behind, missed. Missed is shown as plainly as done.**
> **• Spend against quote is shown at the same plain level.**
> **• Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page."**

**Enumerated status vocabulary (verbatim, four states):**
- `done`
- `on_track`
- `behind`
- `missed`

### §13.3 · Modality leaf (verbatim)

> **"Modality appears at exactly one leaf: evidence inspection. Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region — the existing trust-receipt pattern ('a disputed number is answered by playing the tape'), unchanged."**

### §13.4 · Backend cost constraint (verbatim)

> **"Milestones are records with done-conditions; the platform already stamps events. No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."**

---

## §14 · Interface Summary (verbatim table)

| Surface | Contract |
|---|---|
| audio_codec | audio in → { content_tokens, character_stream, codec_version }; fail-closed on unsupported condition. |
| Language ID | segment → { languages[], confidences, switch_points }; written to provenance. |
| Occurrence index (ext.) | dedup item → + instance condition map. |
| Character Register | Write path: schema cannot represent instance-level identity (§6.3). Read path: strata queries for planner and evaluation. |
| Objective Wizard | session → { TargetOutcome, CollectionSchema }; deterministic compile; compile-time rejection of contract-violating artifacts; session stamped to ledger. |
| TargetOutcome | Rejected without existing test_set_ref; acceptance per stratum; gate_policy recorded at definition. |
| Training Planner | Outcome → { coverage report, curriculum, milestone list, quote ± interval }; reproducible plan_id; plan without calibration stage rejected. |
| Training run | Commissioned-job contract; completion certificate incl. manifest hash and per-stratum results. |
| Voice identity | register strata + constructed organic parameters → identity; distance gate mandatory, fail-closed; certificate issued on pass; versioned; change by ceremony. |
| Commission View | Reads milestones, statuses, spend, and existing artifacts only; introduces no new backend computation. |

---

## §15 · Build Sequence (verbatim table)

> **"Ordered by dependency and cost-of-deferral, not by size."**

| # | Item | Rationale for position |
|---|---|---|
| 1 | Ingestion capture: language ID, code-switch points, condition profile, synthesis attributes (§4.1–4.4) | Everything downstream consumes these; only cheap at first ingestion. Deferral cost is a full re-pass over the estate. |
| 2 | Dedup instance condition map (§4.5) | Contract change to existing machinery; near-zero new detection work. |
| 3 | Character Register schema + custody invariant harness (§6) | The boundary must exist before the first cluster is stored; retrofitting means rebuilding from source. |
| 4 | Codec service (§3) | Unsupervised pretraining starts on unlabelled audio while labelled work proceeds elsewhere. |
| 5 | Clustering + sampled human validation (§5.3) | Requires 1–4. |
| 6 | Objective Wizard variant + Collection Schema type + registry namespace (§8, §9, §12.1) | The planner must never accept a hand-authored Outcome once the wizard exists; building the planner first invites the malformed-input class the compile stage makes impossible. |
| 7 | TargetOutcome type + planner core (§10, §11.1, §11.4) | Requires register strata to plan against and the wizard to author Outcomes. |
| 8 | Sampling & Reflection machinery + milestone records (§11.2–11.3) | Requires 7 and a test set. |
| 9 | Commission View (§13) | Reads records created in 8; by §13.4 it cannot precede them. |
| 10 | Full training runs under the commissioned-job contract (§11.6) | Last by construction — the planner refuses to run earlier. |
| P2 | Voice identity rendering; music register | Phase 2. Non-foreclosure is guaranteed by item 1 and §7.5. |

---

## §16 · Verification Register and Open Decisions

### §16.1 · [VERIFY] items (verbatim, three)

> **"• Perception router contract — model registration point; whether a second output stream per segment is carried or the character stream needs its own artifact type (§3.2).**
> **• Ingestion segment boundaries — the unit a language label attaches to (§4.1).**
> **• Wizard B-2/B-3 landing state — extend the existing state machine with an objective variant, or stand a sibling machine on the shared agent interface and ledger sidecar (§8.5)."**

**§16.1 verification against this session's code opens:**
- Router contract — `services/synisense/shield/perception_router.py` exists but the "second stream per segment" question resolves to **NEGATIVE**: the current `AsrPerception` dataclass in `layer_b/contracts.py` carries `cues, language_hint, model_id, model_version, extraction_params, synthetic_plumbing_only` — no character-stream field. **Character stream is NOT carried by the current provider contract.** Landing this is a discrete §3-scoped delta.
- Language-label unit — the current pipeline attaches language at **§ segment (post-VAD) level per `a1_vad.py` VADSegment**, NOT at the codec-token level. Whether this satisfies §4.1 "segment level" depends on which "segment" the spec means (§1.1 recursion allows any). The wire contract `AudioSegmentV0` carries `condition_profile` and `bounds_start_ms/bounds_end_ms` but **no `languages[]` or `confidences[]` field**. Gap flagged.
- Wizard B-2/B-3 landing — not opened this session; no `services/objective_wizard/*` exists per prior grep (see `AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md` §F1).

### §16.2 · Open decisions (verbatim, five)

> **"• N for the shared-attribute condition (§6.2.2): inherit the platform minimum-group-size seam value, or set a register-specific one.**
> **• Platform default for gate_policy (§10.1) where an Outcome does not set it: missed stratum gates release, or ships documented. This default silently decides how minority-variant quality is treated under schedule pressure.**
> **• Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3).**
> **• Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built (§3, §11.2).**
> **• Baseline tier contents (§9.2): the v1.0 set is the proposal; every addition is paid on every hour ingested, every omission is paid at re-ingestion."**

---

# PART II · CONTRACT DEEP AUDIT (field by field · frozen shapes)

## II.1 · `AudioSegmentV0` (§3 primitive · `contracts/audio_segment_v0.py`)

**Frozen shape** (`ConfigDict(extra="forbid", frozen=True)` + parity map bump 66→67 recorded in the file header):

| Field | Type | Constraint | Spec anchor | Enforces §? |
|---|---|---|---|---|
| `segment_id` | `str` | `min_length=1` | — | uniqueness |
| `estate_ref` | `str` | `min_length=1` | §1.1 recursive framing ("a single file is an estate") | §1.1 |
| `codec_service` | `Literal["perception/audio_codec"]` | fixed literal | §3.2 service label · §1.2 no sibling services | §3.2, §1.2 |
| `content_stream_tokens` | `List[int]` | `min_length=1` | §3.1 content stream | §3.1 |
| `character_stream_tokens` | `List[int]` | `min_length=1` | §3.1 character stream ("never discarded as noise") | §3.1 + §1.5 unrepresentable-absence |
| `condition_profile` | `str` | `min_length=1` | §3.2 declared-or-detected condition | §3.2, §4.3 |
| `bounds_start_ms` | `int` | `ge=0` | §3.2 bounds per ingestion segmentation | §3.2 |
| `bounds_end_ms` | `int` | `ge=0` | §3.2 | §3.2 |
| `tokenised_at` | `str` | `min_length=1` | provenance timestamp | §1.3 |

**Fields the spec REQUIRES that the contract is MISSING:**

1. **`codec_version`** — §3.2 verbatim: *"codec_version is a mandatory field of every downstream artifact's provenance."* Also §3.3 verbatim: *"A downstream artifact lacking codec_version in provenance is rejected at the registry boundary."* **The contract does NOT have a `codec_version` field.** `codec_service` is the service name (literal), not the version. This is a **CONTRACT GAP.** Fixing it is additive (Pydantic contract land forbids in-place mutation; a `codec_version` addition = new file `audio_segment_v1.py` with parity map bump).
2. **`languages[]` + `confidences[]`** — §4.1 verbatim: *"Recorded per segment: languages[], confidences, and code-switch points."* + §4.6 acceptance criterion: *"No segment leaves ingestion without languages[], condition profile, and (where applicable) switch points in provenance."* **The contract carries no language field.** Currently these live on the downstream ASR provider's `AsrPerception.language_hint: Optional[str]` — an optional single-language field, not a list, not confidence-carrying. **CONTRACT GAP.**
3. **`switch_points[]`** — §4.2 verbatim: *"Switch points (position, from-language, to-language, context class) are registered facts with provenance — not preprocessing metadata."* Not present on this contract. `AsrPerception` also does not carry them. **CONTRACT GAP.**

## II.2 · `PerceptionJob_v0` (Phase 9 Sub-stage 9.1 · frozen contract #27)

Fields (verbatim from file lines 33–76):

| Field | Type | Constraint | Description |
|---|---|---|---|
| `job_id` | `str` | `min_length=1` | Server-minted unique. Never worker-provided. |
| `objective_ref` | `str` | `min_length=1` | ObjectiveRequest_v2.objective_id backref |
| `trace_lineage` | `str` | `min_length=1` | Carried, never minted worker-side |
| `reextraction_handles` | `List[str]` | `min_length=1` | Pointers into RMS estate |
| `modality` | `Literal["AUDIO", "VIDEO"]` | required | **"TEXT never routes to GPU (V1-I1)"** — text is CPU-only |
| `extraction_params_ref` | `str` | `min_length=1` | Frozen extraction_params contract surface |
| `idempotency_key` | `str` | `min_length=1` | **"same key => same job, never a second"** (V1-I1) |
| `issued_at` | `str` | `min_length=1` | ISO-8601 UTC timestamp at server-side mint |

**Spec anchors:** BCR §3.1 technical annex lines 79-87; Owner P9-E1 α (2026-07-08) verbatim: *"Parity 26→28 additive at 9.1 landing. The environment-boundary prior holds..."*.

**§ alignment:** this envelope is the control-plane → worker-plane contract, NOT specifically Audio Plane §-anchored. The Audio Plane spec references it implicitly via §11.6 (*"Training runs are commissioned jobs under the existing contract"*).

## II.3 · `PerceptionResult_v0` (frozen contract #28 · worker-plane → control-plane)

Nested types + top-level:

```python
class Telemetry:                              # V1-B4 · Missing → gate failure (V1-G6)
    gpu_hours: float (ge=0.0)
    broadcast_hours: float (ge=0.0)
    unit_yield: int (ge=0)
    per_modality: Dict[str, int]              # e.g. {AUDIO: 12, VIDEO: 8}

class Checkpoint:                             # V1-B2 · kill-and-restart without duplication
    last_completed_offset_s: int (ge=0)
    completed_unit_ids: List[str]

class PurgeAttestation:                       # V1-D1 · REQUIRED, not optional
    purged: bool                              # "True iff worker-side raw AV was purged"
    purged_at: str (min_length=1)             # ISO-8601 UTC of purge attestation

class PerceptionResult_v0:
    job_id: str
    units: List[NormalizedUnit]               # may be empty on partial_failed
    telemetry: Telemetry
    checkpoint: Checkpoint
    purge_attestation: PurgeAttestation
    status: Literal["complete", "partial_failed"]  # two-state honest verdict
```

**Two-state honest verdict** — `status ∈ {complete, partial_failed}` — no `in_progress`, no `succeeded`, no `failed`. Doc-comment verbatim: *"partial_failed carries whatever units + telemetry landed"*.

**Purge attestation is required-not-optional.** Owner V1-D1 verbatim intent: worker-side raw AV bytes are proven purged on every job completion. This aligns with §6.2 bullet 4 ("Never stored audio") and §7.2 fail-closed distance discipline.

## II.4 · `SignalRing v0` catalogue (`contracts/signal_ring.py`)

The **audio modality's** signal-ring dimensions (verbatim from file lines 35–41):

```python
SIGNAL_RING_DIMENSIONS_V0 = {
    "audio": ["prosody", "vocal_emphasis", "affect_valence", "affect_arousal", "speech_rate", "pause_density"],
    "video": ["visual_emphasis", "scene_change_density", "framing_markedness"],
    "image": ["visual_emphasis", "composition_markedness"],
    "text":  ["lexical_intensity", "stance_intensity", "hedging_density"],
    "composite": [],
}
```

**Six audio Signal Ring dimensions:** `prosody`, `vocal_emphasis`, `affect_valence`, `affect_arousal`, `speech_rate`, `pause_density`.

**Explicit corrections banked in the module docstring (three, verbatim):**

1. *"`on_screen_text_present` REMOVED — it is a Provenance/Relational concern, NOT a Signal depth dimension."*
2. *"`framing_intent` → `framing_markedness` ... The Signal Ring measures markedness; intent is downstream. Naming a Signal dimension `*_intent` quietly asks Solva to depth-judge a conclusion instead of a measured signal."*
3. *"COMPOSITE carries no native dimensions — aggregation rule only."*

**Alignment with Audio Plane §5.2 Character Register layers:** Signal Ring's audio dimensions (prosody, vocal_emphasis, affect_valence/arousal, speech_rate, pause_density) MAP CLEANLY onto §5.2 Prosodic layer (*"Intonation contours, stress, rate distributions, pause structure"*) — this IS the Prosodic layer's per-unit dimension set. The Phonetic and Code-switch layers of §5.2 are NOT represented in the Signal Ring.

**Guardrail** (verbatim from lines 62–66):
```python
def validate_signal_dimensions(modality: str, dims: Iterable[str]) -> None:
    """Raise SignalDimensionViolation if any dim key is not in the v0 catalogue..."""
```

## II.5 · `extraction_params@v0` catalogue (`contracts/extraction_params.py`)

**Audio-modality mandatory keys** (verbatim from lines 81–85 + BASE from lines 61–66):

```python
BASE = {
    "provider_id":       "reproducibility_anchor": True,
    "provider_version":  "reproducibility_anchor": True,
    "extraction_run_id": "reproducibility_anchor": True,
    "extracted_at":      "reproducibility_anchor": False,  # correction #1 — not an anchor
}

_AUDIO_DECODING = {
    "language_hint":  "string?",  "reproducibility_anchor": True,
    "beam_size":      "integer",  "reproducibility_anchor": True,
    "temperature":    "number",   "reproducibility_anchor": True, "determinism_pin": 0,
    "vad_threshold":  "number",   "reproducibility_anchor": True,
}

AUDIO = {
    "sample_rate_hz":         "integer", "reproducibility_anchor": True,
    "chunk_ms":               "integer", "reproducibility_anchor": True,
    "model_decoding_params":  "object",  "reproducibility_anchor": True, "nested": _AUDIO_DECODING,
}
```

**Audio-modality reproducibility contract:**
- `sample_rate_hz` (anchor) · `chunk_ms` (anchor) · `model_decoding_params.language_hint` (anchor, optional-shape) · `model_decoding_params.beam_size` (anchor) · `model_decoding_params.temperature` (anchor + **determinism_pin=0**) · `model_decoding_params.vad_threshold` (anchor).
- Every anchor field must match byte-identically for a two-run comparison to assert reproducibility.

**Correction #2 verbatim (lines 26–36):** *"Recording `temperature` isn't enough. If temperature > 0, the extraction is stochastic and cannot reproduce byte-identically... For the reproducibility path, the V1 harness must REQUIRE `temperature = 0` (or an equivalent future seed pin) on the runs it compares. A non-zero run is flagged `non_reproducible_by_construction=True`... and the harness REFUSES to assert 'outputs differ → bug' — sampling noise is not a bug."*

**Gate function** (verbatim from lines 208–220):
```python
def is_deterministically_reproducible(params) -> Tuple[bool, List[str]]:
    """Returns (True, []) iff every nested `temperature` field == 0. Otherwise
    (False, [failing_dotted_keys])."""
```

**Alignment with Audio Plane §4.1:** `language_hint` is currently `string?` (optional). Audio Plane §4.1 verbatim: *"The current plumbing value (language_hint: None) is retired."* **The `extraction_params@v0` catalogue's `_AUDIO_DECODING.language_hint` is the exact field §4.1 flags for retirement — but this file still declares it as `"string?"` (optional).** Gap flagged: closing §4.1 requires that `language_hint: None` cannot leave ingestion (currently it can).

---

# PART III · ATOMICS DEEP AUDIT (a1_* · a2_* · spec vs code)

## III.1 · A1.1 · `a1_demux.py` (83 lines · demux/normalize)

**Parameters banked in module (verbatim from lines 24–26):**
```python
TARGET_SAMPLE_RATE_HZ: int = 16000
TARGET_CHANNELS: int = 1
NORMALIZE_LUFS_TARGET: float = -23.0  # EBU R128
```

**`CanonicalAudioArtifact` dataclass (frozen · lines 29–44):**
```python
@dataclass(frozen=True)
class CanonicalAudioArtifact:
    canonical_id: str
    source_object_id: str
    duration_ms: int
    sample_rate_hz: int
    channels: int
    normalize_lufs: float
    content_sha256: str
    demuxed_at: str  # ISO8601 UTC
```

**Canonical-ID compute** (verbatim from lines 47–55):
```python
def compute_canonical_id(source_object_id: str, content_sha256: str) -> str:
    """Content-addressed canonical_id. Deterministic; source-lineage-attached.
    Format: `canon:sha256:<hex[:32]>:<source_stub>` — stable across re-runs.
    """
```

**Spec conformance vs EAB v1.1 R-A1.1** (*"Extract audio from source containers; transcode to 16 kHz mono lossless. Source objects are never modified or deleted; restructured audio is a derived artifact with lineage to the source object."*):

- 16 kHz mono ✅ (parameters banked).
- Lossless ⚠️ — the module docstring says *"Real-world backend adapter is ffmpeg (deterministic, cross-platform, in registry pin at deployment). This module provides the deterministic wire contract — the canonical audio artifact metadata envelope emitted per source. Backend adapter lives at `backend/services/perception/eab_1_pipeline/backends/` at deployment (NOT this atomic; the wire contract is what deploys)."* **The `backends/` folder does NOT exist on `programme/track-a` HEAD `77834d1`** (grepped this session — not in the file tree). The wire contract is deployed; the ffmpeg backend adapter is **UN-LANDED**.
- Source-object lineage ✅ via `source_object_id` + `canonical_id` content-addressing.
- **EBU R128 LUFS normalisation to -23 dBFS ✅** — this is an implementation-detail choice added by the atomic; the spec (R-A1.1) does not mandate LUFS, but the choice is consistent with §3 fail-closed "never silently degrades quality" doctrine.

**Deterministic property verified** (`content_sha256 = hashlib.sha256(normalized_pcm_bytes).hexdigest()` in `emit_canonical_artifact`, line 71): same input bytes → identical envelope.

## III.2 · A1.2 · `a1_segmentation.py` (124 lines · batch segmentation)

**Parameters** (verbatim lines 23–25):
```python
DEFAULT_BATCH_WINDOW_MS: int = 1_800_000  # 30 min
MIN_BATCH_WINDOW_MS: int = 900_000        # 15 min
MAX_BATCH_WINDOW_MS: int = 3_600_000      # 60 min
```

**`BatchSegment` dataclass (frozen)** (verbatim lines 36–47):
```python
@dataclass(frozen=True)
class BatchSegment:
    batch_id: str
    canonical_id: str
    start_ms: int
    end_ms: int
    window_ms: int
    programme_block_label: Optional[str] = None
```

**Batch-ID compute:**
```python
def compute_batch_id(canonical_id, start_ms, end_ms) -> str:
    material = f"{canonical_id}|{start_ms}|{end_ms}".encode("utf-8")
    return f"batch:sha256:{hashlib.sha256(material).hexdigest()[:24]}"
```

**Segmentation policy** (verbatim from `segment()` function):
- If `programme_blocks` supplied and each block within `[MIN_MS, MAX_MS]` → honour block boundaries.
- Otherwise deterministic `window_ms` (default 30 min) partitions duration.
- Sub-minimum blocks *"merge into next; deterministic downstream"* (line 111 comment).

**Spec conformance vs EAB v1.1 R-A1.2:** *"target 15–60 minutes"* → ✅ MIN 15 min, MAX 60 min, DEFAULT 30 min. Programme-block-aware ✅.

**Fields the batch schema carries vs R-A1.2 required (*"station/source id, start/end timestamps, source-object reference, content-type flags from R-A1.3/R-A1.4, and language hypothesis"*):**

| Spec-required batch field | Code field | Present? |
|---|---|---|
| `station/source id` | `canonical_id` (proxies via lineage) | ⚠️ proxy — no explicit `station` field |
| `start/end timestamps` | `start_ms`, `end_ms` | ✅ |
| `source-object reference` | via `canonical_id` (compute_canonical_id embeds `source_object_id` stub) | ✅ |
| **content-type flags from R-A1.3/R-A1.4** | **NOT PRESENT on `BatchSegment`** | ❌ **GAP** |
| **language hypothesis** | **NOT PRESENT on `BatchSegment`** | ❌ **GAP** |

## III.3 · A1.3 · `a1_vad.py` (141 lines · Silero-registry-pinned VAD)

**Parameters** (verbatim lines 19–21):
```python
SILERO_THRESHOLD_DEFAULT: float = 0.5
MIN_SPEECH_MS_DEFAULT: int = 250
MIN_SILENCE_MS_DEFAULT: int = 500
```

**Content-type enum** (verbatim line 23):
```python
ContentType = Literal["speech", "music", "ad", "silence", "tone", "unknown"]
```

**Six content-type classes** on the VAD's non-speech content-type index.

**`VADSegment` dataclass (frozen)** (verbatim lines 27–34):
```python
@dataclass(frozen=True)
class VADSegment:
    batch_id: str
    start_ms: int
    end_ms: int
    is_speech: bool
    content_type: ContentType
    confidence: float
```

**Reducer** — deterministic per-frame → run-length reduction (`reduce_probes_to_segments`, lines 56–104). Same probes + params → same segments (line 63 docstring).

**Spec conformance vs EAB v1.1 R-A1.3:**
- Silero registry-pinned ✅ (`registry_pin_reference()` returns `"family": "Silero VAD"`, `"role": "vad_gate"`, `"registry_source": "backend/services/perception/models_registry.v0.json"`).
- Non-speech spans NOT discarded — LOGGED as content-type index entries ✅ (six-class enum above; music, ad, silence, tone, unknown are all preserved).

**Spec conformance vs Audio Plane §4.3 condition profiling:**
- §4.3 requires *"channel condition — studio / field / telephone band, transmission artefacts, background class"* per segment.
- `VADSegment` carries **`content_type ∈ {speech, music, ad, silence, tone, unknown}`** — this is a NON-SPEECH-TAXONOMY, NOT a channel-condition taxonomy. **§4.3 condition profiling is NOT implemented in `a1_vad.py`.** The Silero VAD's `content_hint` field on `VADProbe` (line 42) implies an upstream detector emits the hint, but no such detector module exists. **GAP.**

**Spec conformance vs Audio Plane §4.1 language identification:**
- §4.1 requires *"a lightweight offline language identifier (CPU-viable, in-perimeter)"* per segment.
- `VADSegment` carries NO language field. `BatchSegment` carries NO language field. `AudioSegmentV0` carries NO language field. **§4.1 LID is NOT implemented anywhere in the pipeline. GAP.**

**Spec conformance vs Audio Plane §4.4 synthesis-relevant attribute capture:**
- §4.4 requires *"pitch statistics, energy contours, duration patterns"* captured at first ingestion.
- `VADSegment` carries `confidence: float` only. No pitch, no energy, no duration statistics. **§4.4 is NOT implemented. GAP.**

## III.4 · A1.4 · `a1_dedup.py` (130 lines · acoustic-fingerprint dedup)

**Parameters** (verbatim lines 20–22):
```python
FINGERPRINT_HEX_LENGTH: int = 32
MATCH_DISTANCE_THRESHOLD_DEFAULT: int = 0  # exact/near-exact only
NEWS_DEDUP_EXEMPT_LABELS = frozenset({"news", "current-affairs", "news-magazine"})
```

**`Occurrence` dataclass (frozen)** (verbatim lines 25–39):
```python
@dataclass(frozen=True)
class Occurrence:
    occurrence_id: str
    canonical_id: str            # canonical the occurrence matched
    source_canonical_id: str     # where the occurrence physically appeared
    batch_id: str
    start_ms: int
    end_ms: int
    fingerprint: str
    station: str                 # source-object publisher
    timestamp_ms: int            # absolute UTC ms
    is_news_exempt: bool         # AC-A1.d: news blocks dedup-exempt
    requeue_pointer: str         # PROM-S1 honesty grammar
```

**News-exempt policy** (verbatim from `emit_occurrence_if_duplicate`, lines 103–107):
```python
is_news = programme_block_label in NEWS_DEDUP_EXEMPT_LABELS if programme_block_label else False
if is_news:
    # News content is always registered fresh as canonical; no dedup applied.
    index.register_canonical(fp.fingerprint, source_canonical_id)
    return None
```

**Spec conformance vs EAB v1.1 R-A1.4:**
- Chromaprint-class fingerprint ✅ (module docstring names it explicitly).
- Threshold = exact/near-exact only ✅ (`MATCH_DISTANCE_THRESHOLD_DEFAULT = 0`).
- Never deletes — `requeue_pointer` retained ✅.
- News blocks dedup-exempt ✅ (AC-A1.d).

**Spec conformance vs Audio Plane §4.5 dedup-as-augmentation (instance condition map):**
- §4.5 requires each dedup item retain *"the instance condition map — the set of channel/time/condition variants under which identical content occurred"*.
- `Occurrence` carries `station`, `timestamp_ms`, `batch_id` — a **{station, time, batch}** map, NOT a **{channel, time, condition}** map.
- The **condition** dimension per §4.5 (studio / field / telephone / etc. from §4.3) is NOT in the Occurrence payload because §4.3 condition-profile IS NOT computed anywhere upstream (see §III.3 gap). **§4.5 instance-condition-map is PARTIALLY implemented — dimensions are `{station, time, batch}`, missing `condition`.**

## III.5 · A2.1 · `a2_occurrence_writer.py` (162 lines · occurrence rows → NormalizedUnits)

**MC-E1 α precedent verbatim** (lines 1–10): occurrence unit is a `NormalizedUnit` with `modality=AUDIO`; locator is a **DICT ADDITION** carrying `{canonical_id, station, timestamp, batch_lineage}` alongside base audio locator keys `{t_start_ms, t_end_ms}`. **ZERO contract mutation to `contracts/five_rings.py`.** Enforced by AST cell `test_five_rings_v0_zero_mutation_ast_cell.py`.

**`build_occurrence_locator` verbatim** (lines 39–62):
```python
def build_occurrence_locator(*, canonical_id, station, timestamp_ms, batch_lineage,
                              t_start_ms, t_end_ms) -> Dict[str, Any]:
    return {
        "t_start_ms": int(t_start_ms),
        "t_end_ms": int(t_end_ms),
        "canonical_id": canonical_id,
        "station": station,
        "timestamp_ms": int(timestamp_ms),
        "batch_lineage": list(batch_lineage),
    }
```

**`_eab1_extraction_params` verbatim** (lines 65–80):
```python
def _eab1_extraction_params() -> Dict[str, Any]:
    return {
        "provider_id": "eab_1_pipeline",
        "provider_version": "1.0.0",
        "extraction_run_id": "eab-1-occurrence-writer",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sample_rate_hz": 16000,
        "chunk_ms": 30000,
        "model_decoding_params": {
            "language_hint": "en",         # ← §4.1 "language_hint: None ... is retired" — currently hardcoded "en"
            "beam_size": 1,
            "temperature": 0,               # ← determinism-pin honoured
            "vad_threshold": 0.5,
        },
    }
```

**LANGUAGE-HINT SPECIFIC FINDING:** the occurrence-emitter hard-codes `"language_hint": "en"` on line 76. §4.1 verbatim: *"every segment carries a real language signal. The current plumbing value (language_hint: None) is retired."* The current code has REPLACED `None` with a hard-coded `"en"` — which is a different failure mode from what §4.1 was closing (None → "en") but has the same **spec-violation shape**: the language is not computed per-segment from a LID module, it's an assumption. **§4.1 defect class.**

## III.6 · A2.2 · `a2_license_class.py` (53 lines · fail-closed licence attach)

**Parameters** (verbatim lines 20–25):
```python
DEFAULT_LICENSE_CLASS: Literal["internal_only"] = "internal_only"
LicenseClass = Literal["internal_only", "public_derivative", "member_owned"]
```

**Three-class licence enum:** `internal_only` (MC-E4 α fail-closed default) · `public_derivative` · `member_owned`.

**Spec conformance vs EAB v1.1 R-A2.2:** *"license_class: occurrence intelligence derives from the estate; rows carry the connector's license_class with the MC-E4 α default (internal_only, fail-closed)"* — ✅ default is `internal_only`.

**Alignment with Owner Ruling #2 (banked verbatim 2026-09-12T~12:00Z):** owner asserts *"full rights"* — this ADDS a fourth licence class candidate `owner_full_rights` OR upgrades the corpus's licence class to `public_derivative`. **The current three-class enum does NOT carry an `owner_full_rights` class.** Ruling #2 needs a licence-class-enum extension before it can be encoded in `LicenseClassEnvelope.license_class`.

## III.7 · A2.3 · `a2_trace_walker.py` (87 lines · FENCE-1 single-code-path resolver)

**FENCE 1 discipline (verbatim from module docstring, lines 4–10):** *"Single code path. No `if modality == 'occurrence'` branch. No `if source_type == 'structured'` branch. One resolver, parameterized on locator keys."*

**Resolver** (verbatim lines 51–78):
```python
def resolve_canonical_pointer(unit: NormalizedUnit) -> CanonicalPointer:
    """canonical_pointer = locator["canonical_id"] IF present, ELSE source_ref
       t_start_ms       = locator["t_start_ms"] (default 0)
       t_end_ms         = locator["t_end_ms"]   (default 0)
       lineage_chain    = locator["batch_lineage"] (default [])
    """
    locator = unit.provenance.locator or {}
    canonical_pointer = locator.get("canonical_id") or unit.provenance.source_ref
    ...
```

**Spec conformance vs EAB v1.1 R-A2.3 (*"canonical→occurrence relation walkable in the trace"*):** ✅ direct.

---

# PART IV · PROVIDERS + GPU EXECUTION (spec vs code)

## IV.1 · `whisper_provider.py` (cloud API path · 56 lines)

**Provider stanza** (verbatim lines 27–36):
```python
class WhisperApiProvider:
    name = "whisper"
    model_id = "whisper-1"
    model_version = "openai-cloud"
    def __init__(self):
        # Construction must not network or download.
        self._params = {"language_hint": "en"}
```

**Path** (verbatim lines 38–56):
- Calls `perception_router.transcribe(...)` from `services.synisense.shield.perception_router`.
- Audio bytes brokered through Shield's Inner Gate → *"audio bytes don't escape the Inner Gate"* (module docstring line 6).
- Returns typed `AsrPerception`.

**Failure mode:** *"if `emergentintegrations` doesn't expose a whisper ASR seam yet, the provider's constructor still succeeds; `transcribe()` raises `ProviderUnavailable` with an actionable message"* (docstring lines 8–11).

**Hard-coded `language_hint = "en"`** in `_params` (line 36) — same §4.1 violation as `a2_occurrence_writer.py` (see §III.5).

## IV.2 · `faster_whisper_provider.py` (local CTranslate2 · 90 lines)

**Provider stanza** (verbatim lines 33–58):
```python
_MODEL_SIZE = os.environ.get("AKKI_FASTER_WHISPER_MODEL", "tiny")

class FasterWhisperProvider:
    name = "faster_whisper"
    model_id = f"faster-whisper:{_MODEL_SIZE}"
    model_version = "ctranslate2"
    def __init__(self):
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise ProviderUnavailable(...)
        self._params = {"model_size": _MODEL_SIZE, "compute_type": "int8", "beam_size": 1}
        self._model = None  # lazy
```

**Transcribe** (verbatim lines 60–90):
- Writes bytes to tempfile (faster-whisper consumes a path).
- Calls `model.transcribe(tmp_path, beam_size=1)`.
- Emits `AsrCue(t_start_ms, t_end_ms, text, confidence=avg_logprob)` — **note: confidence is `avg_logprob`, not a normalised 0–1 probability.**
- `language_hint = info.language if hasattr(info, "language") else None` — **whisper-info's auto-detected language IS the language hint output.** This IS the closest thing on `programme/track-a` to a §4.1 LID capability: piggy-backing on faster-whisper's built-in auto-detect.

**Bake-off rationale banked in docstring** (lines 4–14): explicitly bakes off **faster-whisper local (CTranslate2, MIT licence, fails on missing local model)** vs **Whisper cloud API (vendor terms, fails on network/quota)**. *"WHY NOT Deepgram / AssemblyAI: same family of remote API (different vendor but same architectural shape) — falsifies less."*

**Model dep:** `faster-whisper==1.2.1` present in `backend/requirements.txt` (grepped this session).

## IV.3 · `pyannote_provider.py` (local diarization · 80 lines)

**Provider stanza** (verbatim lines 23–39):
```python
class PyannoteProvider:
    name = "pyannote"
    model_id = "pyannote/speaker-diarization-3.1"
    model_version = "pyannote-audio"
    def __init__(self):
        try:
            from pyannote.audio import Pipeline
        except ImportError:
            raise ProviderUnavailable(
                "pyannote.audio not installed. "
                "Install with `pip install pyannote.audio` and set HUGGINGFACE_HUB_TOKEN."
            )
        self._params = {
            "min_speakers": int(os.environ.get("AKKI_DIA_MIN_SPEAKERS", "1")),
            "max_speakers": int(os.environ.get("AKKI_DIA_MAX_SPEAKERS", "8")),
        }
```

**Two-gate construction** (verbatim lines 42–51):
```python
def _ensure_pipeline(self):
    if self._pipeline is None:
        from pyannote.audio import Pipeline
        token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
        if not token:
            raise ProviderUnavailable(
                "pyannote.audio requires HUGGINGFACE_HUB_TOKEN to download the diarization model."
            )
        self._pipeline = Pipeline.from_pretrained(self.model_id, use_auth_token=token)
```

**Two gates fire on any live diarize path:** (a) `pyannote.audio` importable? (b) `HUGGINGFACE_HUB_TOKEN` set?

**Dep status:** `pyannote.audio` is **NOT in `backend/requirements.txt`** (verified prior session). Construction fails with `ProviderUnavailable` at import. HF token not yet in `.env`.

**§7.2 alignment (speaker-verification distance gate):** `PyannoteProvider` emits `DiarizationTurn(speaker: str, t_start_ms, t_end_ms)` — a per-turn speaker LABEL, no embedding. Speaker embeddings (needed for §7.2 distance-guarantee scoring against real speakers) are NOT emitted by this provider today. `pyannote.audio` supports embedding extraction (`pyannote.audio.Model.from_pretrained("pyannote/embedding")`) but the CURRENT provider does not expose it. **§7.2 substrate = MISSING even after `pyannote.audio` lands.** Requires a `speaker_embedding` sibling module.

## IV.4 · Layer-B contracts (`services/layer_b/contracts.py`)

**`AsrCue` dataclass** (lines 33–37):
```python
@dataclass
class AsrCue:
    t_start_ms: int
    t_end_ms: int
    text: str
    confidence: Optional[float] = None
```

**`AsrPerception` dataclass** (lines 41–47):
```python
@dataclass
class AsrPerception:
    cues: List[AsrCue]
    language_hint: Optional[str] = None
    model_id: str = ""
    model_version: str = ""
    extraction_params: Dict[str, Any] = field(default_factory=dict)
    synthetic_plumbing_only: bool = False
```

**`DiarizationTurn` + `DiarizationPerception`** (lines 50–63):
```python
@dataclass
class DiarizationTurn:
    speaker: str
    t_start_ms: int
    t_end_ms: int

@dataclass
class DiarizationPerception:
    turns: List[DiarizationTurn]
    model_id: str = ""
    model_version: str = ""
    extraction_params: Dict[str, Any] = field(default_factory=dict)
    synthetic_plumbing_only: bool = False
```

**Key gap vs Audio Plane §4.1 + §4.2:**
- `AsrPerception.language_hint: Optional[str]` — **single language, optional**. Spec §4.1 requires `languages[]` (list) + `confidences[]` (list) + code-switch points. **The provider contract carries neither `languages[]` nor `switch_points[]`.** GAP.
- `AsrCue.confidence: Optional[float]` — no confidence-calibration policy attached (see SILENCE finding §4.1).

## IV.5 · Layer-B factory (`services/layer_b/factory.py`)

Env-driven selection (verbatim lines 25–35):
```python
_ASR_REGISTRY = {
    "whisper":         "services.layer_b.asr.whisper_provider:WhisperApiProvider",
    "faster_whisper":  "services.layer_b.asr.faster_whisper_provider:FasterWhisperProvider",
}
_DIARIZATION_REGISTRY = {
    "pyannote": "services.layer_b.diarization.pyannote_provider:PyannoteProvider",
}
_VISION_REGISTRY = {
    "emergent_vision": "services.layer_b.vision.frame_perception_provider:EmergentVisionProvider",
}
```

**Env knobs** (docstring lines 8–10):
- `AKKI_ASR_PROVIDER` default `"whisper"` (cloud)
- `AKKI_DIARIZATION_PROVIDER` default `"pyannote"`
- `AKKI_VISION_PROVIDER` default `"emergent_vision"`

**Availability probe** (verbatim lines 66–85):
```python
def available_providers() -> Dict[str, Dict[str, bool]]:
    """Returns availability map... A provider is 'available' iff its class can be
    constructed without raising ProviderUnavailable. This lets the system surface
    honestly flag which providers are wired but un-installed."""
```

## IV.6 · GPU execution (`services/perception/gpu_execution/*`)

**`cuda_runtime.py`** — CPU/GPU selector, fails hard if `PERCEPTION_EXECUTION_MODE` env var unset (Owner ruling 9.2a-E2 α verbatim in module docstring lines 5–12): *"α, two conditions. (1) No silent default at deployment: env var unset -> explicit import-time failure, never a silent fallback to CPU — a GPU deployment quietly running CPU is the silent-swap risk in the other direction. CI sets cpu explicitly. (2) execution_mode lands in result telemetry — attribution of GPU-hours and yield to a mode the record doesn't carry is the same fabricated-attribution gap E1 closes for models. One field, honest attribution."*

**`audio_batching.py`** (33 lines total · verbatim lines 14–19):
```python
# Default chunk size aligned with faster-whisper's internal chunk_length_s=30
_CI_CHUNK_MS = 30_000  # 30 s (whisper native)
_CPU_MAX_BATCH = 1
_GPU_MAX_BATCH = 8
```

**Effective batching maturity:** **VERY THIN.** `iter_audio_chunks` (line 25) yields `(0, audio_bytes_or_path)` — single-chunk pass-through — with docstring line 28: *"For 9.2a fixture-mode: single chunk pass-through — faster-whisper's internal chunking handles longer audio. This function is a seam for 9.2b GPU-mode batching."* **A seam, not a batcher. VRAM-budget-aware micro-batching is UN-LANDED. Long-audio (>30s) OOM behaviour is uncharacterised.**

**`model_loader.py`** (46 lines · verbatim lines 18–35):
```python
def get_asr_model(model_id: str = "whisper-tiny"):
    attest_model(model_id)          # registers vs models_registry.v0.json
    cached = _model_cache.get(model_id)
    if cached is not None:
        return cached
    from faster_whisper import WhisperModel
    if SELECTED_BACKEND == "cpu":
        model = WhisperModel(_hf_model_name(model_id), device="cpu", compute_type="int8")
    else:
        model = WhisperModel(_hf_model_name(model_id), device="cuda", compute_type="float16")
    _model_cache[model_id] = model
    return model

def _hf_model_name(model_id: str) -> str:
    return {"whisper-tiny": "tiny"}.get(model_id, model_id)
```

**Model registry: seeded with `whisper-tiny` only** — per Ruling 9.2a-E1 α + seed-with-CI-fixture correction 2026-07-10 (banked in DECISIONS.md). This is a CI fixture, NOT a production choice. The `_hf_model_name()` map has one entry: `whisper-tiny` → `tiny`. Any multilingual production model (e.g. `openai/whisper-large-v3`, `openai/whisper-medium`) requires a registry seed + `_hf_model_name` addition + `models_registry.v0.json` update.

---

# PART V · SPEC-vs-CODE CONFORMANCE MATRIX

One row per numbered spec requirement. Verbatim spec anchor · code locator · gap.

| # | Spec § | Spec requirement (verbatim excerpt) | Code that implements it | Gap |
|---:|---|---|---|---|
| §1.1-1 | §1.1 | *"An audio file is a data estate ... segments are rows ... the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns"* | 8-column framing implicit in atomics: content=ASR, language=missing, condition=partial (via a1_vad content-type), prosody=partial (via Signal Ring audio dims), occurrence=Occurrence, code-switch=missing, music=partial (a1_vad content_type "music"), group-level-character=missing (Character Register) | **3 columns MISSING** (language, code-switch, group-level character); 3 PARTIAL (condition, prosody, music); 2 EXISTS (content, occurrence). |
| §1.5-1 | §1.5 | *"Safety boundaries are enforced by making the violating state impossible to express in the contract"* | `AudioSegmentV0` `content_stream_tokens`/`character_stream_tokens` `min_length=1`; `signal_ring.validate_signal_dimensions` raise-on-unknown | ✅ pattern held. |
| §3.1-1 | §3.1 | *"discrete token sequences produced by a neural audio codec, not on waveforms"* | `AudioSegmentV0.content_stream_tokens: List[int]` + `.character_stream_tokens: List[int]` | ✅ shape; codec service is a literal string, **no codec actually implemented** — `perception/audio_codec/` service is absent. |
| §3.1-2 | §3.1 | *"Tokenization exposes two separable streams per segment: content stream ... character stream ... never discarded as noise"* | `AudioSegmentV0` carries BOTH streams `min_length=1` | ✅ shape. Provider layer (`AsrPerception`) does NOT carry a character stream — provider is content-stream-only. GAP. |
| §3.1-3 | §3.1 | *"Control markers (language, register, segment type) are splice-able tokens"* | — | **MISSING.** No control-marker vocabulary. |
| §3.1-4 | §3.1 | *"audio in an unsupported condition fails closed with a stated reason. The codec never silently degrades quality."* | `PyannoteProvider._ensure_pipeline` raises `ProviderUnavailable(...)`; `WhisperApiProvider.transcribe` routes through perception_router | ⚠️ fail-closed pattern held at provider level, but NO codec-level unsupported-condition refusal exists (codec doesn't exist). |
| §3.2-1 | §3.2 | *"Target token rate 50–100 tokens/second of audio"* | — | **MISSING.** No token-rate policy. |
| §3.2-2 | §3.2 | *"codec_version is a mandatory field of every downstream artifact's provenance"* | `AudioSegmentV0` has `codec_service` (literal) but NOT `codec_version` | ❌ **CONTRACT GAP.** Additive v1 needed. |
| §3.3-1 | §3.3 | *"Round-trip fidelity is measured and recorded per codec version"* | — | **MISSING** (no codec, no fidelity harness). |
| §3.3-2 | §3.3 | *"A downstream artifact lacking codec_version in provenance is rejected at the registry boundary"* | — | **MISSING** (registry-boundary check absent because field absent). |
| §4.1-1 | §4.1 | *"every segment carries a real language signal. The current plumbing value (language_hint: None) is retired."* | `a2_occurrence_writer._eab1_extraction_params` hard-codes `"language_hint": "en"`; `WhisperApiProvider._params = {"language_hint": "en"}`; `AudioSegmentV0` has NO language field | ❌ **GAP.** Hard-coded `"en"` is a different failure of the SAME spec clause. Real per-segment LID is un-built. |
| §4.1-2 | §4.1 | *"A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion"* | `FasterWhisperProvider.transcribe` returns `info.language` (whisper auto-detect); happens at WHOLE-FILE level, not segment | ⚠️ PARTIAL. Whisper-auto-detect is neither lightweight (whisper-tiny CI fixture only) nor CPU-viable at production quality nor offline (multilingual whisper model) — closest available substitute. Standalone LID (fastText-LID, MMS-LID) is UN-LANDED. |
| §4.1-3 | §4.1 | *"Recorded per segment: languages[], confidences, and code-switch points"* | `AsrPerception.language_hint: Optional[str]` (single-scalar) | ❌ **GAP.** No list, no confidences, no switch points. |
| §4.1-4 | §4.1 | *"The signal routes downstream model selection (ASR path, NER path, de-identification path)"* | Factory `get_asr_provider(name=...)` routes by env var, NOT by segment language | ❌ **GAP.** Per-segment routing un-implemented. |
| §4.2-1 | §4.2 | *"Switch points (position, from-language, to-language, context class) are registered facts with provenance — not preprocessing metadata"* | — | **MISSING.** No switch-point emitter, no switch-point contract. |
| §4.3-1 | §4.3 | *"Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion"* | `AudioSegmentV0.condition_profile: str` (opaque scalar) | ⚠️ PARTIAL (field exists, no detector). |
| §4.4-1 | §4.4 | *"group-level acoustic attributes required by any future synthesis capability (pitch statistics, energy contours, duration patterns) are captured"* | Signal Ring audio dims include `prosody, vocal_emphasis, speech_rate, pause_density` — a PROXY set | ⚠️ PARTIAL. Dimensions defined; extractor un-landed. |
| §4.5-1 | §4.5 | *"for each deduplicated item, the instance condition map — the set of channel/time/condition variants — is retained"* | `Occurrence.station, .timestamp_ms, .batch_id` — a `{station, time, batch}` map | ⚠️ PARTIAL. `condition` dimension missing because §4.3 detector un-landed. |
| §4.6-1 | §4.6 | *"No segment leaves ingestion without languages[], condition profile, and (where applicable) switch points in provenance"* | Ingestion invariant test does NOT check this today (test not present per this session's file map). | ❌ **INVARIANT MISSING.** |
| §4.6-2 | §4.6 | *"A deduplicated item without its instance condition map fails the ingestion invariant test"* | — | ❌ **INVARIANT MISSING.** |
| §5-full | §5 | Character Register (Phonetic, Prosodic, Condition, Code-switch layers) | — | **MISSING.** No `services/character_register/*`. |
| §6.3-1 | §6.3 | *"An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them"* | — | **MISSING.** Custody invariant harness not present. |
| §7.2-1 | §7.2 | *"Every constructed identity is scored against every speaker representation ... minimum distance ... fail-closed ... no override"* | — | **MISSING.** Distance-guarantee harness not present (invention out of POC scope). |
| §8-full | §8 | Objective Wizard schema compiler | — | **MISSING.** No `services/objective_wizard/*`. |
| §9.2-1 | §9.2 | Baseline tier at v1.0: language ID + code-switch + condition profile + dedup condition map + synthesis-relevant acoustics | Partial: dedup ✅, condition profile field ✅ (opaque), other three ❌ | ⚠️ PARTIAL (1/5 solid, 1/5 shape, 3/5 missing). |
| §10-full | §10 | `TargetOutcome` contract | — | ❌ **MISSING.** No `contracts/target_outcome_v0.py`. |
| §11.2-1 | §11.2 | *"train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold"* | — | **MISSING.** Sampling & Reflection machinery un-built. |
| §11.5-1 | §11.5 | *"Every training example carries its provenance into the training manifest"* | `NormalizedUnit.provenance.locator + .source_ref` (`five_rings.py`) | ✅ shape held at unit level; training manifest aggregation TBD. |
| §11.6-1 | §11.6 | *"completion certificate records compute consumed, data touched, manifest hash, and per-stratum results"* | `PerceptionResult_v0.telemetry` (gpu_hours, broadcast_hours, unit_yield, per_modality) + `.purge_attestation` | ⚠️ PARTIAL. Perception result carries compute + purge; per-stratum results NOT carried at result level (that's a training-manifest artefact, un-landed). |
| §12.1-1 | §12.1 | Registry namespace per commission, sealed on close | `mtafiti/registry.py` exists; namespace-per-commission sealing behaviour un-verified this session | ⚠️ PARTIAL. |
| §12.2-1 | §12.2 | Northena data classes: collection events · calibration runs · curriculum decisions · milestone status changes · run certificates | `northena/ledger.py` writer exists; these 5 specific class labels un-verified this session. | ⚠️ PARTIAL. |
| §13.2-1 | §13.2 | Commission View status vocabulary: done · on_track · behind · missed | — | **MISSING** (surface un-built). |
| §14 (full) | §14 | Interface Summary — 10 named surfaces | 4 EXIST (`audio_codec` service label · Language ID as `language_hint` scalar · Occurrence index · Voice identity contract shape) · 6 MISSING (Character Register · Objective Wizard · TargetOutcome · Training Planner · Training run certificate · Commission View) | ⚠️ 4/10 partial · 6/10 MISSING. |
| §15 (build sequence) | §15 | 10-step build order | Items 1 (partial) · 2 (partial · condition-dimension missing) · 3 (missing) · 4 (missing) · 5 (missing) · 6 (missing) · 7 (missing) · 8 (missing) · 9 (missing) · 10 (partial — full training runs exist under `campaign_infra` but not under the Audio Plane's commissioned-job contract) | **90% of the spec's build sequence is un-landed.** The POC covers step 1 (partial) + step 2. |

---

# PART VI · SILENCE ROLL-UP — where the spec must be authored

Every SILENT finding above, one line each. **Silence is a finding.** Each row represents a policy the platform must author before an autonomous run of that shape can produce a claimable result.

| # | Silent area | Where silent | What must be authored |
|---:|---|---|---|
| S-01 | Codec CHOICE (existing open vs estate-specific) | §16.2 open decision | Owner rules an initial codec (or defers until Sampling & Reflection returns a number). |
| S-02 | Fidelity metric (round-trip) | §3.3 | Named metric (PESQ · ViSQOL · STOI · bit-exact test); a floor per commission. |
| S-03 | Character-stream data structure | §3.1 · §16.1 | Schema of the character stream (dim, vocab, sample rate) OR decision to ship as separate artifact. |
| S-04 | LID named model | §4.1 | Named LID (Meta MMS-LID · fastText-LID · whisper-auto-detect · other) + evaluation-benchmark commit. |
| S-05 | LID confidence-calibration policy | §4.1 | Threshold(s), abstain policy, unknown-language handling. |
| S-06 | Segment boundaries for language attach | §4.1 · §16.1 | Which segmentation level carries the language label — VAD-segment vs batch vs codec-token. |
| S-07 | Code-switch `context class` vocabulary | §4.2 | Enum of context classes. |
| S-08 | Switch-point `position` unit | §4.2 | ms vs token vs word offset. |
| S-09 | Multi-language switch beyond binary | §4.2 | Data shape for 3+-language switches. |
| S-10 | Condition-profile enumeration | §4.3 | Complete enum of channel/transmission/background classes. |
| S-11 | Condition-profile detection method | §4.3 | Named detector (classical DSP feature set OR neural condition classifier). |
| S-12 | §4.4 pitch statistics (which statistics?) | §4.4 | Named statistics (mean-F0 · F0-SD · voiced-fraction · other). |
| S-13 | §4.4 energy contour shape | §4.4 | Named form (RMS-per-frame · dB-per-frame · parametric envelope). |
| S-14 | §4.4 duration pattern shape | §4.4 | Named unit (phoneme · syllable · utterance-length statistics). |
| S-15 | Character Register clustering algorithm | §5.3 | Named method + hyperparameters. |
| S-16 | Character Register cluster-count discipline | §5.3 | k selection · silhouette policy · split/merge threshold. |
| S-17 | Character Register human-sample size | §5.3 | N per cluster · confidence-based sampling policy. |
| S-18 | Character Register storage schema | §5.2 · §6.2.4 | Field-level schema for centroids/distributions/frequencies. |
| S-19 | `N` for shared-attribute condition (§6.2.2) | §6.2 · §16.2 | Default minimum-group-size seam value. |
| S-20 | `non-reconstructive in combination` formal test | §6.2.3 | Named test (k-anonymity · l-diversity · epsilon-DP). |
| S-21 | Speaker-verification method for §7.2 distance gate | §7.2 | Named method (x-vector · ECAPA-TDNN · other). |
| S-22 | Speaker-distance threshold value | §7.2 | The threshold floor. |
| S-23 | Certificate format | §7.3 | Full schema. |
| S-24 | Objective Wizard's mechanical-guard stub-agent proof | §8.3 | Named test/harness. |
| S-25 | Acceptance metrics for `accuracy` × `coverage` | §10.1-2 | Named metric per output class (WER for speech transcript · Character Error Rate · F1 for tags · other). |
| S-26 | `gate_policy` default | §10.1 · §16.2 | `missed_stratum_gates_release` vs `ships_documented`. |
| S-27 | `constraints` sub-schema (latency · compute budget · deployment target) | §10.1 | Sub-fields, units, defaults. |
| S-28 | Scaling-curve family (§11.2) | §11.2 | Named curve family (power law · Chinchilla · piecewise empirical). |
| S-29 | Confidence-interval width (§11.2 / §11.4) | §11.2 · §11.4 | 95% vs 90% · analytical vs bootstrap. |
| S-30 | Milestone count/granularity (§11.3) | §11.3 | Guidance on how many milestones per commission. |
| S-31 | Cluster naming — internal vs external partner | §5.3 · §16.2 | Owner ruling. |
| S-32 | Baseline-tier additions/omissions | §9.2 · §16.2 | Owner ruling per proposed additive column. |

---

# PART VII · AUTONOMOUS-LOOP STANCE FROM THE SPEC

The owner's question: does the spec specify pseudo-labeling, active learning, human verification tiers, confidence thresholds, or determinism boundaries for the audio domain?

### Pseudo-labeling

**SILENT** on the term. The closest thing the spec authors is the `Character Register` build process (§5.3):

> *"Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."*

Unsupervised clustering + sampled human naming ≈ pseudo-labelling with a human-in-the-loop naming step, but the spec doesn't use that vocabulary. Also §8.3 propose-qualify-graduate:

> *"A proposed column never enters collection directly. It is admitted as a candidate: collected on a sample only, its evidence of value measured against the objective — the same qualification path any fact travels."*

This is closer to *bootstrap-with-qualification*, not pseudo-labelling per se.

### Active learning

**SILENT** on the term. Sampling & Reflection §11.2 is the spec's ANALOGUE:

> *"Data requirements for low-resource fine-tuning are empirical; no analytical answer exists. The first commissioned stage is therefore a calibration: train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold."*

The scaling-curve extrapolation is calibration-first, not iterative-query-selection. **Active-learning as a query-selection loop is not in the spec.** Silence.

### Human verification tiers

The spec authors ONE explicit human tier: **§5.3** cluster naming — *"Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."* Also **§10.2** *"The gate decision is recorded on the Outcome at definition"* which is an owner decision at definition time, not a mid-run human review.

**The spec explicitly EXCLUDES humans from the runtime path** — this is Doc 1 §4.7 (not in this spec but binding), restated by §11.6: *"Training runs are commissioned jobs under the existing contract: quoted before start, metered during, certificated on completion."* No mid-run human intervention.

**Runtime humans are constrained to two moments:**
1. **Commission-open ratification of the milestone list** (§13.2: *"Commission does not open until it is agreed."*).
2. **Cluster naming** (§5.3: sampled, commissioned, paid).

Both are pre-run / offline surfaces, not runtime interruptions.

### Confidence thresholds

The spec asks for `confidences[]` to be recorded (§4.1) but is **SILENT on any threshold value**. The only thresholds authored anywhere in the spec are:

- **§7.2** speaker-verification distance threshold (mandatory, fail-closed, VALUE not stated).
- **§11.4** cost quote with confidence interval (INTERVAL WIDTH not stated).
- **§10.1** acceptance threshold per stratum (VALUE not stated — that's the Objective Wizard's compile output).

Every threshold is a policy the wizard OR the owner sets per commission; **no platform-wide floor is authored.**

### Determinism boundaries

The spec authors determinism explicitly:

- **§8.3** *"The compile stage is deterministic throughout: the agent proposes; only qualified columns compile. Mechanical guards prove against a stub agent before any LLM is plugged in."* — the Objective Wizard's compile step is deterministic.
- **§11.1** *"a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs."* — the Training Planner's deterministic-core + reorder-only-learned-layer pattern.
- **§1.4** *"No data-volume requirement, accuracy expectation, or cost figure is quoted without a measurement behind it. The calibration stage exists to convert assertions into measurements before commitment."* — no assumption crosses into a claim without measurement.

**And in the extraction contract:** `extraction_params@v0` correction #2 (verbatim from `contracts/extraction_params.py` lines 26–36):
> *"For the reproducibility path, the V1 harness must REQUIRE `temperature = 0` (or an equivalent future seed pin) on the runs it compares. A non-zero run is flagged `non_reproducible_by_construction=True` with the failing keys listed, and the harness REFUSES to assert 'outputs differ → bug' — sampling noise is not a bug."*

**The determinism boundary for AUDIO EXTRACTION is: `temperature=0` at every whisper decode call.** This is verifiable at runtime via `is_deterministically_reproducible(params)`. `a2_occurrence_writer._eab1_extraction_params` line 78 sets `"temperature": 0` — ✅ pinned.

**Autonomy-loop attestation from the spec:** determinism-by-construction at (a) objective compile, (b) plan generation, (c) extraction params. Learned components are **structurally constrained** — they may only reorder eligible sets; they may never widen eligibility. Human-in-the-loop is **pre-run only** — no mid-run human path is authored. This is the exact "detect autonomously, decide/release only with owner ruling" shape the prior capability assessment named — the spec explicitly encodes it in §8.3 · §11.1 · §11.6 · §13.2.

---

# PART VIII · ATTESTATION

- **No product code touched.** No `services/**/*.py` edited or created. No pytest invoked. No testing_agent invoked. Ratchet floor **3251** untouched.
- **No push.** Local commit only, on workspace `master` (this document).
- **Retracted ChatGPT integration** — no OpenAI/ChatGPT reference anywhere in this document.
- **POC HOLD in force** — `W-AUDIO-POC-3-STATIONS` CP0 does not open until owner ratifies the 3-station selection.
- **Every VERBATIM quote in this document was pulled from a file opened in this session** — file locators + line ranges recorded in §0. Silences are marked explicitly as SILENT with a §-anchor.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
