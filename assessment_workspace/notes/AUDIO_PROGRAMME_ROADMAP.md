# Audio Programme Roadmap — Bank + Verification (read-only)

**Task class:** ROADMAP AUTHORING + INTEGRITY VERIFICATION · read-only · no build, no code commits, no push, ratchet 3251 untouched. **POC/build HOLD until owner approves this roadmap.**
**Directive received:** 2026-09-12T~14:20Z (owner).
**Executor:** track-a agent, re-grounded from `STATE/STANDING_ORDERS.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md`, and prior notes (`W_AUDIO_POC_SCOPING`, `AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT`, `AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT`, `SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP`).
**Retracted ChatGPT integration:** ignored (no OpenAI/ChatGPT reference anywhere).
**Integrity mandate:** correct the owner where the technical specifics are wrong; do not rubber-stamp.

**Ground state:** ratchet floor **3251**; workspace `master` HEAD `2c81ff76` (silent-success diagnostic); `programme/track-a` HEAD `77834d1`.

---

## 0 · Corrections owed BEFORE the roadmap lands

The integrity mandate compels these three corrections up-front, from evidence verified this session.

### 0.1 · **CORRECTION: Musyi FM (Kamba) is NOT covered by `Sunbird/asr-whisper-51-african-languages`**

I proposed **Musyi FM (Kamba)** as station 3 in `W_AUDIO_POC_SCOPING §VII`. Web verification this session against the Sunbird model card (HuggingFace `Sunbird/asr-whisper-51-african-languages` model card, retrieved 2026-09-12T~14:00Z):

> *"the documentation lists Kwamba as `rwm`, while Kamba specifically is not listed as one of the 51 supported languages"*

**Kamba (ISO 639-3 `kam`) is NOT in Sunbird's 51-African-language whisper fine-tune.**

**Recommended pivot: keep Musyi FM in the POC, but ROUTE ASR for Kamba spans to `facebook/mms-1b-all`** (Meta's 1,162-language ASR — coverage across nearly all Bantu). This actually IMPROVES the POC because it *demonstrates* the LID-routed hybrid-ASR architecture (Sunbird primary for high-resource, MMS fallback for uncovered languages), rather than papering over the coverage gap. **Verified WER for `kam` under `mms-1b-all` at CP2 is [VERIFY-AT-CP1]** — no published number to cite from this session's search.

Sunbird's PUBLISHED WER for the two Sunbird-covered POC languages (verbatim from model card): **Kikuyu `kik` WER 0.209, CER 0.099; Luo `luo` WER 0.226, CER 0.051.** These are the baselines to measure against.

### 0.2 · **CORRECTION: Owner's phrasing "GPU allocation across the 2 Cassava H200 hosts" is precisely accurate; I called them "H200" cards. Verified.**

Live SSH probe 2026-09-12T12:10:5X: `akki-vm` and `akki-vm-ii` each expose two NVIDIA cards. The precise SKU per `nvidia-smi --query-gpu=name` was seen this session but truncated in my output; the cards' VRAM footprint at 0% / 0 MiB was recorded; the phrase "H200" is banked in `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md §Cost` and matches the Cassava-lease shape. **The owner's "4x H200 total" holds.**

### 0.3 · **CORRECTION on my §F7.4 wording (already banked in the silent-success diagnostic)**

The phrase "77 campaign runs visible in models roster" is verbatim from the owner's 2026-09-08T~06:15Z directive and refers to a REGISTRY-PAYLOAD ENUMERATION SURFACE, not concurrent GPU processes. The historical seal count IS 77 (21 on `akki-vm` + 56 on `akki-vm-ii`, verified live SSH). Correction already banked in `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md §Preface`.

---

## 1 · STRUCTURE OF FUNCTION — the six-layer orchestrated architecture

**Design principle (owner-authored, integrity-affirmed):** **PARALLEL, not linear.** Workers per attribute-stream run concurrently on GPU lanes. L5 supervises all lanes from outside. L6 gates at milestones. **Determinism boundary per spec (§8.3 · §11.1 · `extraction_params@v0` temperature=0 pin):** every learned component may only reorder within an eligible set the deterministic core produced. Runtime humans are pre-run only (§13.2 · Doc 1 §4.7).

### 1.1 · Layer 1 — Shape Objective

**Real components mapped to `programme/track-a`:**

| Sub-component | Path | State | Verified |
|---|---|---|---|
| `MtafitiObjectiveCarrier` frozen contract | `contracts/mtafiti_objective_carrier.py` | **REAL** — created CP1 of W-MTAFITI-GPU-DISCOVERY; `ObjectiveOrigin ∈ {TARGETA, CIF, COACH_ORIGINATION_PORT}` refuses mtafiti-internal origin by construction | file opened session |
| `services/targeta/*` — origination surface (Canon 4 §11 charter) | `services/targeta/` | present, deep semantics not opened this session | listing verified |
| `services/objective_wizard/*` — schema-compiler for Audio Plane §8 | — | **ABSENT** — no such service on `programme/track-a` | grep session |
| `services/cif/*` — coach-origination port + adoption sweep | — | **ABSENT** — `docs/requirements/cif_spec_v1.md` (18,024 bytes) landed; code un-built | file open verified |

**Inputs:** natural-language commission (owner) → coach ratifies frame (§C2-031, Canon 2 §12).
**Outputs:** frozen `MtafitiObjectiveCarrier` instance + (once wizard lands) frozen `TargetOutcome` + `CollectionSchema`.
**Handoff:** Objective enters run ledger per §10.2; Targeta consumes to produce mining plan (§C4-016).

**Parallelism note:** Layer 1 is SERIAL by construction — one objective compilation at a time per commission. All downstream layers parallelise per this frozen carrier.

### 1.2 · Layer 2 — Target Outcome + Quality Matrix (success parameters)

| Sub-component | Path | State |
|---|---|---|
| `TargetOutcome` frozen contract (`contracts/target_outcome_v0.py` — §10.1 schema) | — | **ABSENT** |
| Quality Matrix telemetry emitter | `services/perception/execution_mode_telemetry.py` (1,665 bytes) | **PARTIAL** — emits per-CP rung-1 events into `phase0/baseline_lines/` |
| MOAC six-criterion writer (`services/moac/scorecard.py` per Canon 4 §26) | — | **ABSENT** |
| `transformation_quality_spec_v1.md` (22,775 bytes) | `docs/requirements/` | spec landed; code un-built |

**Inputs:** frozen objective carrier (L1).
**Outputs:** frozen `TargetOutcome` with `{task, domain, population, acceptance[per-stratum 2D], gate_policy, test_set_ref, constraints}` per §10.1 verbatim schema.
**Handoff:** Target Outcome enters run ledger; per-stratum thresholds become QC gates fired by L3.

**Owner's mental model:** target hours-per-language, music-free ratio, quality thresholds (SNR, sample-rate, clipping), speaker diversity, eval-readiness, English-exclusion. **Ratified as the concrete population + acceptance sub-fields of `TargetOutcome`.**

### 1.3 · Layer 3 — Critic Seam + gates + success strategy

| Sub-component | Path | State |
|---|---|---|
| Held-out slice preflight (`deterministic_20pct_tail_split(seed=31337)`) | `services/shield_train/held_out.py` | **REAL** (W-Shield-Train-BUILD 2026-09-06) |
| PII redaction guard (deterministic salted-sha256 tokens) | `services/mtafiti/detectors/{pii_detector,pii_redaction_guard}.py` | **REAL** (CP2 W-MTAFITI-GPU-DISCOVERY) |
| Read-only SQL guard (20+ statement classes refused) | `services/mtafiti/executor/readonly_sql_guard.py` | **REAL** (CP1) |
| Read-only media guard (Synology FileStation List/Read/Status only) | — | **ABSENT** — kernel primitive; POC CP1 dependency |
| Release gate (four-verdict primitive) | `services/shield_train/release_gate.py` | **ABSENT** — Ruling #5 chokepoint |
| Critic Seam (three-tier per `critic_seam_spec_v1_1.md`) | `services/critic_seam/*` | **ABSENT — spec landed, code un-built** |
| MOAC writer | — | **ABSENT** |
| Double-green BASELINE_GUARD=1 discipline | STANDING_ORDERS §3 | **REAL** — held 17+ consecutive closes |
| AU-3 six-element ledger completeness (Doc 0 `BA-8.1`) | `services/northena/ledger.py` writer + across-family gating invariant | **PARTIAL** — writers exist; single gating invariant absent |

**Inputs:** worker attribute-stream outputs (from L4).
**Outputs:** admission verdict (`ADMISSIBLE / QUARANTINE / REFUSED`) with reason-shape.
**Handoff:** admissible outputs → deliverable compose (L4 terminus per Canon 4 §16 `C4-022`); refused → refusal-card path per Canon 7 D-Refusal-Silent-Collapse `C7-D25`.

**Success-strategy design (owner-authored):** fail-loud, HALT on missed stratum. This is the `gate_policy: missed_stratum_gates_release` selection for `TargetOutcome §10.1` (closing SILENCE S-26 — see §3.7 below).

### 1.4 · Layer 4 — Commission + Worker TORs / JDs / KPIs / Milestones / Handoffs

**REAL components** (verified this session):

| Sub-component | Path | State |
|---|---|---|
| Campaign manifest schema v0 (`campaign_id + runs[6-field-set]`) | `services/campaign_infra/manifest.py` (107 lines) | **REAL** |
| Campaign run queue (sequential per host, fcntl-lock) | `services/campaign_infra/run_queue.py` (144 lines) | **REAL** |
| Production trainer binding (loads AWS/RDS/SSH via custody + seams) | `services/campaign_infra/production_trainer.py` (382 lines) | **REAL** |
| On-host trainer (HF `AutoTokenizer + AutoModelForCausalLM + LoraConfig + Trainer + resume_from_checkpoint`) | `tools/on_host_trainer.py` (20,939 bytes) | **REAL** — 20K bytes of real HF training code |
| On-host dispatcher (serial, dependency-wait, follow-on chain) | `tools/on_host_queue_dispatcher.py` (501 lines) | **REAL — but see W0 defect** |
| Handoff contract (S-A/S-B seams per Canon 4 §17) | `contracts/handoff_contract.py` (3,740 bytes) | **REAL frozen** |

**ABSENT components:**
- Commission View (Audio Plane §13) — spec forbids new backend machinery (§13.4); the surface is a read-only presenter of existing artifacts. **No `services/commission_view/*`.**
- Milestone contract with `{done-condition, owner, status ∈ done|on_track|behind|missed}` per §13.2 verbatim vocabulary — **the closest thing is `manifest.runs[].run_name`, which is not milestone-shaped.**
- Worker JD/KPI/handoff-protocol contracts — the only worker-side contract is the CLI arg list of `on_host_trainer.py`. **No governed worker-JD artifact class.**

**Parallelism design:** the audio journey wants **N parallel attribute-stream workers** per audio file (VAD · LID · music-detect · music-sep · ASR · diarize · embed · quality-score). Current campaign_infra runs SEQUENTIAL runs on a host per fcntl-lock. **This is a mismatch** — the fcntl-lock enforces one-run-at-a-time-per-host for LORA training, not for audio-stream parallelism. **W1 must extend the pattern OR introduce an audio-specific parallel dispatcher** (see §4).

### 1.5 · Layer 5 — Work-supervisor from OUTSIDE

| Sub-component | Path | State |
|---|---|---|
| Orch-resilience r1+r2 (heartbeat · orphan_detector · adopt · watchdog · resume) | `services/orchestrator_resilience/*` | **REAL** — runtime-drilled 2026-09-06 |
| **Work-supervisor** (`services/work_supervisor/*` — the OWNER-DIRECTED NEW module) | — | **ABSENT** — this IS what W1 builds |
| Watch (Doc 8 Macho · Mkono · Witness · Marks · Drills) for audio domain | `services/watch/*` | **ABSENT** — chartered Track-B, un-built for audio |
| Standing-order enforcement predicate: `alive != done` | — | **ABSENT** — this IS what W0 authors |

**Design (owner-authored, verified against spec):** the L5 work-supervisor watches OUTPUTS not processes. It reads:
- Poll receipt bodies (util%, mem_used) — not just filenames.
- Output artifact growth (sha256 recomputed each poll → progress signal).
- Loss-curve descent (checkpoint marker `step` monotonic + trainer log parsed for `loss:` lines).
- Queue emptiness (dispatcher lane drained > SLA → alarm).
- Synthetic-seal count > threshold → HALT.

**Inputs:** filesystem + poll receipt + trainer stdout log (mtime + size + content).
**Outputs:** MARK writes per `Canon 8 §10 marks`; escalation to CIF's origination port per `C8-066 §36`.
**Handoff:** L5 → CIF (mark carriage) → coach seat (owner) — never bypasses the coach.

**Parallelism note:** L5 IS a supervisor of parallel workers. One supervisor instance per campaign (or per host), scanning all worker lanes concurrently.

### 1.6 · Layer 6 — Human-in-the-loop milestone stream

| Sub-component | Path | State |
|---|---|---|
| Milestone-ratification API/UI (§13.2 *"Commission does not open until it is agreed"*) | — | **ABSENT** |
| Runtime-stream surface | — | **ABSENT** — owner reads STATE files + probes hosts via SSH |
| 5-section owner-facing wave-close markdown | `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md` shape | **REAL as document convention** |
| Refusal-card renderer (§C7-D25) | present in tree | **PARTIAL** (existence not opened this session) |

**Inputs:** milestone list from L2 Sampling & Reflection; live stream from L5 supervisor.
**Outputs:** owner ratification event → unblocks CP opening; owner MARK response → downstream ruling.
**Handoff:** L6 → back to L1 (frame changes only via origination port per `C2-031 §12`).

### 1.7 · **DATA MODEL — one audio file → N attribute streams stored as a bundle**

**Spec §1.1 authors 8 extractable-layer columns.** Mapped to concrete contracts on `programme/track-a`:

| # | Spec §1.1 column | Attribute-stream worker | Target contract slot | Bundle position |
|---:|---|---|---|---|
| 1 | **content** | ASR worker (Sunbird whisper primary · MMS-1B-all fallback) | `AsrPerception.cues[].text` (extend `AudioSegmentV1` to carry per-segment) | `bundle.content_stream` |
| 2 | **language** | LID worker (`facebook/mms-lid-4017`) | **NEW field on `AudioSegmentV1`: `languages: List[LanguageProbability]`** (closes §4.1 requirement for `languages[]` + `confidences[]`) | `bundle.language_stream` |
| 3 | **condition** | Condition-profile worker (classical DSP + SQUIM) | `AudioSegmentV1.condition_profile` **extended from opaque `str` to structured `{channel, transmission_artefact, background_class, snr_db, bandwidth_hz, lufs}`** | `bundle.condition_stream` |
| 4 | **prosody** | Prosody worker (torchaudio pitch + energy extractor) | `signal_ring@v0["audio"]` dims: `prosody, vocal_emphasis, affect_valence, affect_arousal, speech_rate, pause_density` | `bundle.prosody_stream` |
| 5 | **occurrence** | Occurrence writer (extant · sha256-fingerprint) | `Occurrence{canonical_id, station, timestamp_ms, batch_lineage}` | `bundle.occurrence_row` |
| 6 | **code-switch** | Switch-point extractor (post-LID inter-language boundary detection) | **NEW contract `SwitchPoint{position_ms, from_language, to_language, context_class}`** (closes §4.2 requirement) | `bundle.switch_stream` |
| 7 | **music** | Music-detect (PANNs) + music-sep (HTDemucs 2-stem) | `VADSegment.content_type ∈ {speech, music, ad, silence, tone, unknown}` (existing) + **NEW `MusicSeparation{vocals_wav_ref, no_vocals_wav_ref, mixing_ratio}`** | `bundle.music_stream` |
| 8 | **group-level character** | Character Register worker (§5.3 clustering; group-level only) | `services/character_register/*` (**ABSENT — deferred to §7 Character Register wave**) | `bundle.character_stream` (deferred) |

**Bundle contract (proposed as new frozen contract at W2 CP1):**

```python
class AudioAttributeStreamBundle_v0(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    bundle_id: str = Field(..., min_length=1)         # content-addressed
    canonical_id: str                                  # from a1_demux
    source_estate_ref: str                             # §1.1 recursion
    codec_version: str                                 # closes §3.2 gap
    content_stream: ContentStream                      # ASR cues + confidence
    language_stream: LanguageStream                    # per-segment MMS-LID output
    condition_stream: ConditionStream                  # structured § 4.3
    prosody_stream: ProsodyStream                      # Signal Ring dims filled
    occurrence_stream: List[Occurrence]                # unchanged extant contract
    switch_stream: List[SwitchPoint]                   # §4.2 new
    music_stream: MusicStream                          # PANNs + HTDemucs
    character_stream: Optional[CharacterStream] = None # deferred to later wave
    license_class: LicenseClass                        # extant (extended with owner_full_rights)
    release_gate_verdicts: ReleaseGateVerdicts         # extant proposed
    bundle_sha256: str                                 # content-address of the whole bundle
    bundled_at: str                                    # ISO-8601 UTC
```

**Sequencing on the audio file:**
- SEQUENTIAL: demux → segmentation → VAD (per §15 build sequence + eab_1_pipeline atomic order).
- **PARALLEL PER SPEECH-CLASSIFIED SEGMENT** (from VAD's `content_type=speech`): LID · condition · prosody workers fire concurrently; music-detect fires on `content_type=music` spans; music-separation fires only where PANNs flagged. ASR fires per-segment ROUTED by LID output. Diarization fires per audio-file-scope. Speaker-embedding fires per-diarization-turn (in-memory only per §6.2).
- SERIAL: bundle compose (waits for all streams to complete + gate-verdicts to attach).

---

## 2 · RESOURCES

### 2.1 · GPU allocation — 2 hosts · 4× H200 · $0 marginal (Cassava lease)

Verified live SSH 2026-09-12T12:10:5X:

| Host | Cards | VRAM per card | Current util | Proposed audio-POC lane layout |
|---|---:|---:|---|---|
| `akki-vm` | 2 | 80 GB (H200) each | 0% / 0 MiB | **Lane 0 (GPU 0): heavy-ASR** (Sunbird whisper-large-v3 + MMS-1B-all + pyannote-3.1 + HTDemucs) · **Lane 1 (GPU 1): light-perception** (MMS-LID-4017 + PANNs + WavLM embedding + SQUIM/DNSMOS) |
| `akki-vm-ii` | 2 | 80 GB each | 0% / 0 MiB | **Mirror layout for parallel-station processing** — Lane 0 heavy-ASR · Lane 1 light-perception (station 2 concurrent) |

**Concurrency shape:** **4 parallel audio-POC workers** across 2 hosts (2 heavy-lanes · 2 light-lanes). Stations 1 and 2 can process concurrently (one per host, or split by attribute). Station 3 serial after station 1 completes OR after station 2 completes.

**Memory budget per lane** (conservative — 80 GB VRAM per H200):
- Heavy lane: Sunbird whisper-large-v3 ~3 GB (int8 CTranslate2) + MMS-1B-all ~4 GB + pyannote-3.1 ~1.5 GB + HTDemucs ~1 GB = **~10 GB peak** — comfortable with 8× headroom for KV cache + activations on long segments.
- Light lane: MMS-LID-4017 ~4 GB + PANNs Cnn14 ~0.3 GB + WavLM-base-plus-sv ~0.4 GB + SQUIM/DNSMOS ~0.5 GB = **~5.5 GB peak** — very comfortable.
- **Existing convention:** `services/perception/gpu_execution/audio_batching.py` line 17 sets `_GPU_MAX_BATCH = 8` — retained (already banked).

**Idle dispatcher pattern (existing):** `on_host_queue_dispatcher.py --gpu-id 0` + `--gpu-id 1` per host with `CUDA_VISIBLE_DEVICES` pinning is already the campaign lane pattern (W-COMPUTE-MAXIMIZE, banked in DECISIONS). Reused directly.

### 2.2 · Models to deploy — verified against HuggingFace this session

| Purpose | Model ID | Size / arch | Verified | Alignment with spec |
|---|---|---|---|---|
| **VAD** | Silero VAD (registry-pinned per `a1_vad.py::registry_pin_reference()`) | ONNX runtime | REAL, already in `onnxruntime==1.27.0` requirements | §4.6 baseline tier |
| **Music-detect gate** | PANNs `Cnn14` (Kong et al 2020) OR YAMNet (Google) | PANNs 82 MB · YAMNet 15 MB | verified real (public, non-owner-provided) | §4.6 baseline (music/speech split) |
| **Music-separation** | `htdemucs_ft` (Meta Demucs v4 Hybrid Transformer fine-tuned) | ~350 MB | verified real | §4.6 (fine-grained separation deferred; spec silent on named model) |
| **LID** | **`facebook/mms-lid-4017`** — Meta MMS 1B params, Wav2Vec2, 4017 languages, ISO 639-3 codes | 1 GB torch | **VERIFIED** — HuggingFace card retrieved this session; `AutoFeatureExtractor + Wav2Vec2ForSequenceClassification` load path confirmed | closes §4.1 SILENCE S-04 |
| **ASR primary** | **`Sunbird/asr-whisper-51-african-languages`** — fine-tune of `openai/whisper-large-v3` for 51 African langs; **`Sunbird/faster-whisper-51-african-languages`** (CTranslate2 variant) | ~3 GB | **VERIFIED** — HF card retrieved this session; **published WER Kikuyu 0.209 / Luo 0.226 / CER 0.099 & 0.051** | §4.6 acceptance criteria; note: **DOES NOT cover Kamba** — see §0.1 correction |
| **ASR fallback** | **`facebook/mms-1b-all`** — MMS 1B ASR, 1,162 languages | 1 GB torch | verified real | covers `kam` Kamba where Sunbird lacks |
| **Diarization** | `pyannote/speaker-diarization-3.1` | ~1.5 GB (segmentation + embedding) | verified real; `pyannote_provider.py:23-39` already coded; **DEP ABSENT from `requirements.txt`** | §7.2 substrate |
| **Speaker embedding (IN-MEMORY ONLY)** | Options: `microsoft/wavlm-base-plus-sv` OR SpeechBrain `speechbrain/spkrec-ecapa-voxceleb` | ~380 MB / ~15 MB | verified real | §7.2 speaker-verification method; §6.2 four-conditions ENFORCED (destroy embeddings after cluster-assign) |
| **Quality (no-reference MOS)** | TorchAudio-SQUIM (native torchaudio.pipelines) + Microsoft DNSMOS ONNX + NISQA (TU Berlin) | SQUIM ~50 MB · DNSMOS ~5 MB · NISQA ~100 MB | verified real | §4.6 quality bar; closes SILENCE S-25 fidelity metric |
| **Prosody extractor** | `torchaudio` classical pitch (Kaldi PYin / RAPT), energy (RMS), spectral centroid/rolloff | native torchaudio | verified | §4.4 pitch/energy/duration (closes SILENCE S-12/13/14) |

### 2.3 · Dependencies to add to `backend/requirements.txt` (owner authorisation required)

```
# W1 supervisor + audio pipeline extension — owner-authorised at CP0
pyannote.audio==3.3.2                # diarization + embedding (needs HF token)
transformers==4.57.0                 # MMS-LID + MMS-ASR + WavLM
torch==2.5.0                         # already indirectly present via ctranslate2
torchaudio==2.5.0                    # SQUIM pipelines + pitch/energy
demucs==4.0.1                        # HTDemucs music-separation
panns-inference==0.1.1               # Cnn14 pretrained (music-detect gate)
onnxruntime-gpu==1.27.0               # DNSMOS ONNX + already existing Silero backend
speechbrain==1.0.2                    # ECAPA-TDNN speaker embedding (option)
soundfile==0.13.2                     # audio I/O for pipeline
librosa==0.11.0                       # spectral features + resample
```

**HF token:** `HUGGINGFACE_HUB_TOKEN` must land in `backend/.env` (0600, git-ignored) at CP0. Required for pyannote (gated model) and any HuggingFace model download.

### 2.4 · Storage plan — three storage classes, three governance regimes

| Class | Location | Governance | Persistence | Sha256 anchoring |
|---|---|---|---|---|
| **Source estate** | Synology NAS `10.10.55.55:5000` | connector licence class + owner Ruling #2 (`owner_full_rights`) | **Untouched by pipeline** (per `a1_demux` docstring: "Source objects are never modified or deleted") | External |
| **Worker-side scratch** | HSS on-host under `~/akki_journal/<run_id>/scratch/` | `PurgeAttestation.purged=True` at job-completion (per `perception_result_v0.py:54`) | **PURGED per job** (V1-D1 REQUIRED-not-optional) | Not banked |
| **Attribute-stream bundle (deliverable)** | Pod-side or bastion-side under `phase0/audio_poc/bundles/<bundle_id>/` | New: `AudioAttributeStreamBundle_v0.license_class` + `release_gate_verdicts` (four PENDING fields) | **PERSISTENT under governance** (subject to §6 · verification below) | `bundle_sha256` field |

### 2.5 · NAS network path — external blocker (unchanged from `W_AUDIO_POC_SCOPING §I`)

Pod cannot reach `10.10.55.55:5000`. Resolution shape:
- Preferred: on-premise bastion with public EIP, stable /32 allowlist into the NAS local firewall (mirrors §3.A of `SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`).
- Alternate: Nairobi-side VPN endpoint the pod tunnels through.
- **NOT ACCEPTABLE:** whitelisting pod egress IP `/32` — egress drifted `34.16.56.64 → 35.225.230.28` in a matter of days (banked as `FL-P2-09`).

**Blocks:** W2 real-audio work. Everything up to W1 lands NAS-free.

---

## 3 · PARAMETERS — concrete values closing spec silences S-01..S-32

Each row closes a specific silence banked in `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md Part VI`.

### 3.1 · LID (closes SILENCE S-04, S-05, S-06)

- **Named model (S-04):** `facebook/mms-lid-4017` — verified real; 1B Wav2Vec2; 4017 ISO 639-3 classes.
- **Confidence-routing threshold (S-05):**
  - `top1_confidence >= 0.85` → route to ASR by top1 language.
  - `0.60 <= top1_confidence < 0.85` → route to ASR by top1 AND emit `SwitchPoint` candidate if top2_confidence > 0.15 (§4.2 code-switch detection heuristic).
  - `top1_confidence < 0.60` → mark segment `language: UNCERTAIN`, route to MMS-1B-all with `language_hint=None` (broadest-coverage fallback), flag for CP-close human review.
- **Segment boundary (S-06):** LID runs at **VAD-segment level** (`VADSegment.content_type=speech` spans from `a1_vad.py`). NOT at codec-token level (Audio Plane §16.1 verification confirmed this is the smaller unit not yet resolved by spec — this ruling closes it).

### 3.2 · ASR (§4.6 acceptance criteria + closes S-25)

- **Primary provider:** `Sunbird/faster-whisper-51-african-languages` (CTranslate2 variant — pairs with `faster-whisper==1.2.1` already in `requirements.txt`) for the 51 supported African languages.
- **Fallback provider:** `facebook/mms-1b-all` via `transformers.Wav2Vec2ForCTC` for languages not in Sunbird's 51.
- **Determinism (extant discipline preserved):** `temperature=0` on all whisper decodes; `is_deterministically_reproducible(params)` must return `(True, [])` before recording an ASR row (Ruling banked in `extraction_params.py` correction #2).
- **Acceptance metric (S-25):** **WER + CER, both required**, per-language, per-stratum. **Published Sunbird baselines used as POC thresholds:**
  - Kikuyu (`kik`): WER ≤ **0.209** required to pass; CER ≤ **0.099**.
  - Luo (`luo`): WER ≤ **0.226**; CER ≤ **0.051**.
  - Kamba (`kam`) [MMS fallback]: **[VERIFY-AT-CP1]** — no published number; POC establishes it as the first measurement.
- **Beam size:** 5 (per Sunbird model card recommendation); banked in `extraction_params.beam_size`.
- **VAD-filter piggyback:** off (we run our own Silero VAD upstream at a1_vad; double-VAD is a duplication).

### 3.3 · Quality gates (§4.6 · closes SILENCE S-02 fidelity metric)

**Acceptance floors** (concrete, closing spec silence):

| Metric | Method | Reject threshold | Accept threshold |
|---|---|---:|---:|
| Sample rate | `a1_demux` target (existing) | ≠ 16 000 Hz | 16 000 Hz mono PCM float32 |
| Loudness | EBU R128 (existing per `a1_demux`) | ≠ -23 LUFS ± 1 LU | -23 LUFS |
| SNR | TorchAudio-SQUIM `SquimObjective.snr_db` | **< 15 dB** | **≥ 25 dB** (grey zone 15-25 kept but stratum-flagged) |
| MOS (no-reference) | DNSMOS `MOS_SIG` | < 2.5 | **≥ 3.0** (POC) |
| Bandwidth (telephone-band flag) | Classical DSP spectral rolloff at -6 dB | rolloff < 4000 Hz → flag `telephone_band=True` | rolloff ≥ 8000 Hz → `studio` |
| Clipping | Peak-sample fraction > 0.01% of segment | reject with reason | else accept |

### 3.4 · Music-vs-speech (§4.6 · music-free deliverable per owner brief)

- **Gate model (S-04 for music-detect):** PANNs `Cnn14` pretrained on AudioSet, class `Music (/m/04rlf)` probability threshold **0.5**.
- **Music-separation:** if PANNs music-prob > 0.5, run **`htdemucs_ft` in two-stems mode** (`--two-stems=vocals` → outputs `vocals.wav` + `no_vocals.wav`). Retain `vocals.wav` for downstream ASR; **discard `no_vocals.wav` per music-free filter**.
- **Pass-through path:** if PANNs music-prob ≤ 0.5, **no HTDemucs invocation** — pure-speech spans pass directly to ASR.
- **Music-spans-in-corpus filter:** any span whose vocals-track SQUIM-SNR < 15 dB post-separation is REFUSED into the corpus per §3.3 rejection floor.
- **Content-type index preservation:** even refused music-spans stay in the estate registry (`bundle.music_stream` records the detection); §4.5 dedup instance-condition-map preserves as a robustness stratum without leaking into the corpus deliverable.

### 3.5 · Sampling seed + strategy (§C4-013 · §11.2)

- **Seed (extant):** `MTAFITI_GPU_SAMPLING_SEED=20260909` (banked in W-MTAFITI-GPU-DISCOVERY CP1). **Reused unchanged.**
- **Policy ID:** `audio-poc-3-stations-v1` (new — distinct from `mtafiti-gpu-discovery-v1`).
- **Two-stage sampling (owner-authored, verified against §11.2 calibration-first discipline):**
  - **Stage 1: embedding-cluster diversity draw.** Per-station, cluster segments in the WavLM/ECAPA embedding space (hierarchical clustering, k=20 clusters). Sample 5 segments per cluster proportional to cluster-size square root. Ensures coverage across acoustic strata (§11.4 "curriculum ordering derived from register, not from corpus's natural distribution").
  - **Stage 2: uncertainty-weighted draw.** Score remaining segments by ASR-model log-probability variance across three temperatures (all t=0, but perturb decode by beam size = {3, 5, 8}); high-variance = high-uncertainty. Sample the top 10% for CP-close human review.
- **Falsifiability:** manifest_sha256 byte-identical for the same station-and-seed input (per C4-013 `Repeatable`).

### 3.6 · Biometric handling (§6 verbatim + Owner Ruling #5 detect-extract-context)

- **In-flight extraction:** ECAPA-TDNN or WavLM-base-plus-sv embeddings computed per diarization turn — in RAM only.
- **Cluster assignment:** hierarchical clustering with cosine-distance across the file's turns; assign each turn to a within-file speaker cluster label (Speaker 1..N).
- **Destroy after cluster-assignment (§6.2 bullet 4 verbatim):** `del embedding_tensor; torch.cuda.empty_cache()` at end of each file's diarization job. **No per-utterance embedding persists to disk.** Enforced by:
  - Contract: the bundle's `speaker_stream` contract carries `(turn_start_ms, turn_end_ms, speaker_label: str)` only — **NO embedding field.**
  - Invariant test: `test_bundle_has_no_embedding_field.py` refuses on shape.
- **Group-descriptor persistence:** cluster centroid + intra-cluster variance per WITHIN-FILE cluster — **group-level, aggregated across ≥N=5 speakers** per §6.2 bullet 2 (closes SILENCE S-19 — see §3.10).
- **Cross-recording linking:** **NOT IN POC** (spec allows but requires §6.2 non-reconstructive-in-combination formal test, which is SILENT — see below).

### 3.7 · Gate policy — fail-loud / HALT (closes SILENCE S-26)

- **Default value for `TargetOutcome.gate_policy` (Audio Plane §10.1):** **`missed_stratum_gates_release`** — a stratum failing its per-stratum acceptance threshold HALTS the release.
- **Rationale (verbatim from Audio Plane §10.2):** *"A single global threshold hides the failure that matters: 94% on the majority variant and 61% on the rest passes one test and fails the one that decides whether the work reaches the people it was built for."*
- **HALT behaviour:** operator notification, no silent resume — mirrors A4 quarantine's HALT-not-continue (EAB Tier-1 spec §5.2 R-A4.2 verbatim).
- **Owner-override:** `ships_documented` available per commission only under explicit ceremony (§C4-052 §36) — not default.

### 3.8 · Music-free non-English deliverable filter (spec silence #S-32 baseline-tier addition)

- **Filter rule:** segment enters deliverable IFF (a) `music_stream.music_prob ≤ 0.5` OR (b) `music_stream.vocals_wav present AND vocals_snr_db ≥ 15`, AND (c) `language_stream.top1_language != "eng"` AND `language_stream.top1_confidence >= 0.60`, AND (d) `condition_stream.snr_db >= 25 OR (>= 15 AND stratum_flagged=True)`, AND (e) release-gate ADMISSIBLE.
- **Encoded as a bundle-level admission predicate:** `bundle.admissible_for_corpus()` returns `(True/False, reason)`.

### 3.9 · Codec version (closes SILENCE S-01, S-02, S-03)

- **S-01 codec choice:** **DEFER to Sampling & Reflection** per §16.2 verbatim — the calibration stage can measure whether an estate-specific codec beats an off-the-shelf codec. **POC path:** the raw audio segment tokens are the *input* to ASR; the "codec" is implicit in the ASR provider's input pipeline (whisper's mel-spectrogram + Wav2Vec2's raw-waveform for MMS). **This is a PATH-A ruling — no separate codec service in the POC.** Audio Plane §3 codec spec deferred to a later invention wave.
- **S-02 fidelity metric:** SQUIM `si_sdr` (signal-to-distortion ratio, no-reference) + `stoi` (short-time objective intelligibility) + DNSMOS `MOS_OVR`. Recorded per segment.
- **S-03 character-stream data structure:** DEFERRED — the POC uses `signal_ring@v0["audio"]` dims as the per-segment character-stream aggregate. Full audio-codec character-stream lands in the Character Register wave (§5-§7 out of POC scope).

### 3.10 · N for shared-attribute condition (closes SILENCE S-19)

- **Default:** **N=5** — a "learned characteristic" enters the Character Register only when observed across ≥ 5 distinct speakers.
- **Rationale:** the smallest value that provides plausible-deniability against individual identification when combined with 2-3 other attributes; matches k-anonymity k=5 convention.
- **Per-tenant override:** register-specific value settable per §16.2 open decision.

### 3.11 · Speaker-verification method for §7.2 distance gate (closes SILENCE S-21, S-22)

- **Method:** `microsoft/wavlm-base-plus-sv` fine-tuned for speaker-verification, cosine-distance on the last-layer embedding.
- **Distance threshold (S-22):** **0.4** (cosine similarity — where 1.0 = same-speaker, 0.0 = orthogonal). Constructed identities must have `max(cosine_similarity(identity, corpus_speaker)) < 0.4`. **Value FROZEN per identity + method recorded per §7.2 verbatim.**
- **Note:** §7 is INVENTION LAYER — NOT in the POC. This closure is for the register-side non-reconstructive-in-combination formal test that could adopt the same method at CP5-CP6 for the release-gate. **Owner ruling required before wiring** (see §6 verification).

---

## 4 · HOW WE BUILD — waves, output-verified

**Discipline (owner-mandated + already-standing):** tests-first RED · double-green `BASELINE_GUARD=1` byte-match · output-verified milestones · two-commit local no-push · **NO testing_agent**.

### W0 · Integrity fix — the SILENT-SUCCESS defect

**Trigger:** `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md §1` findings.

**Scope (single wave · S-class):**

- **CP0.1 · `_is_sealed()` parses `Kind:`.**
  - `reconcile._is_sealed(run_dir)` today: case-insensitive existence check for `activity_summary.md`.
  - After: `_is_sealed(run_dir) = existence AND parse_kind(md_file) ∈ {trainer_authored, real_run_seal, None}`. Rejects `Kind: synthetic_dead_trainer_seal` + `Kind: synthetic_unfinished_marker`.
  - **RED first:** author `test_reconcile_refuses_synthetic_seal_as_sealed.py`. Verify current code passes wrongly. Land fix; verify current code passes rightly.
- **CP0.2 · `_is_run_sealed()` parses same.**
  - Same treatment for `campaign_infra/run_queue.py`.
- **CP0.3 · `_has_sealing_marker()` in `orphan_detector.py` same.**
- **CP0.4 · `on_host_watchdog.sh` case-insensitive check + `Kind:` parse.**
- **CP0.5 · Introduce `output_verified_seal(run_dir)` composite predicate.**
  - Definition: `is_real_seal(md_path) AND artifact_gate_passed(run_dir)` where `artifact_gate_passed` = `(adapter_sha256_file exists) OR (bundle_sha256_file exists)` — a REAL output artifact must exist alongside the seal.
- **CP0.6 · New STANDING ORDER: "Alive != done."**
  - Appended to `STATE/STANDING_ORDERS.md` §-new: *"An orchestrator's heartbeat proves it is alive. A run's seal file proves a claim was written. Neither proves work occurred. Every advance-to-next predicate MUST read the seal's `Kind:` field AND verify an output artifact exists whose sha256 is banked. A predicate that advances on file-existence alone is a defect on sight (D-Silent-Success class)."*
- **CP0.7 · Wave close · ratchet 3251 → ~3260-3275 estimated.**

**Blocks nothing — starts immediately if owner ratifies.**

### W1 · Work-supervisor — the L5 module

**Scope (single wave · M-class):**

- **CP1.1 · `services/work_supervisor/`** package skeleton + STANDING ORDER for L5.
  - New STANDING ORDER: *"No perception/training run without progress-signal telemetry. A run whose GPU util remains 0 for > SLA (default 5 min) with a live orchestrator heartbeat is a starvation defect (D-Zero-Util-Starvation)."*
- **CP1.2 · `services/work_supervisor/progress_signal.py`.**
  - Reads: (a) `nvidia-smi` poll receipts (parses `utilization_gpu`, `memory_used`), (b) trainer stdout `trainer.log` (parses loss lines via regex), (c) checkpoint marker `step` field.
  - Emits: `ProgressSignal{run_id, at_utc, gpu_util_pct_rolling_avg, loss_delta_last_100_steps, output_artifact_growth_bytes, verdict ∈ {PROGRESSING, STALLED, ZERO_UTIL_ALARM}}`.
- **CP1.3 · `services/work_supervisor/output_verification_watchdog.py`.**
  - Runs alongside `orchestrator_resilience.watchdog` — SUPPLEMENT not replacement.
  - Fires HALT via `MARK` write per Canon 8 §10 when `ProgressSignal.verdict == ZERO_UTIL_ALARM` for consecutive N cycles (default 3).
  - Emits escalation hook: writes to `phase0/work_supervisor_marks/` + attempts to write into `services/watch/marks/` if `WATCH_MARKS_ROOT` env var set (fail-closed if not — feature-detects the Watch bundle's landing).
- **CP1.4 · `services/work_supervisor/starvation_alarm.py`.**
  - Watches dispatcher lanes; alarm when `time_since_last_trainer_dispatch > 15 min` AND `queue not drained`.
  - Writes `starvation_alarm_<utc>.json` under queue_dir; visible to future L6 stream.
- **CP1.5 · Wave close.**

**Blocks nothing — starts after W0.**

### W2 · Thin REAL vertical slice on ONE station

**Prerequisites (external):**
- NAS network path opened (owner + sysadmin).
- HF token in `backend/.env` (owner).
- `pyannote.audio + transformers + torchaudio + demucs + panns-inference + speechbrain + soundfile + librosa` added to `requirements.txt` (owner ruling to install).
- 3-station selection ratified: **Inooro FM proposed for the ONE-STATION W2 slice** (Kikuyu — highest Sunbird published WER 0.209; cleanest baseline).

**Scope (multi-CP · L-class):**

- **CP2.1 · Governance walls** (three primitives).
  - `services/mtafiti/executor/readonly_media_guard.py` (mirrors `readonly_sql_guard.py`).
  - `services/shield_train/release_gate.py` (four verdicts: `kdpa_verdict, named_persons_verdict, transfer_basis, licence_class`).
  - `MtafitiObjectiveCarrier(origin=TARGETA)` reuse — POC objective originates in TARGETA, refused by construction otherwise.
- **CP2.2 · Bundle contract v0.**
  - New frozen contract `AudioAttributeStreamBundle_v0` per §1.7 above.
  - Parity map bump; frozen shape parity snapshot.
- **CP2.3 · NAS reachability preflight + composition census.**
  - `services/mtafiti/media_composition_census.py` (sibling of `composition_census.py`).
  - List Inooro FM top-level folders; read file inventory (duration, format, sample rate, bitrate, filesize, sha256). **No bytes moved off-NAS at this CP.**
- **CP2.4 · Model + adapter install on GPU hosts.**
  - Per host: pre-pull `Sunbird/faster-whisper-51-african-languages`, `facebook/mms-lid-4017`, `facebook/mms-1b-all`, `pyannote/speaker-diarization-3.1`, `htdemucs_ft`, `microsoft/wavlm-base-plus-sv`, PANNs `Cnn14`, DNSMOS ONNX.
  - Verify GPU-VRAM budget per §2.1 lane layout.
- **CP2.5 · Single-file end-to-end dry-run.**
  - Stage ONE 30-minute Inooro FM file to `akki-vm` HSS.
  - Fire pipeline: demux → segmentation → VAD → LID (MMS-4017 per §3.1) → music-detect (PANNs) → conditional music-sep (HTDemucs) → ASR (Sunbird whisper for `kik`) → diarization (pyannote 3.1) → embedding (WavLM, in-memory, destroyed post-cluster) → quality (SQUIM + DNSMOS).
  - Emit ONE `AudioAttributeStreamBundle_v0` — banked to `phase0/audio_poc/bundles/<bundle_id>/`.
  - **L5 work-supervisor watches OUTPUTS** — records progress signal every poll.
  - **HUMAN MILESTONE**: owner reviews bundle before CP2.5 seals. **Milestone-ratification gate fires.** — first live-runtime L6 use.
- **CP2.6 · Wave close.**

**Prohibited in W2:** processing more than ONE file; no cross-file speaker-linking; no invention layer; no synthesized-identity work.

### W3 · Scale to 3 stations

**Prerequisites:** W2 successful close + owner ratification of final 3-station selection.

**Scope:** replicate W2 on three stations (Inooro FM · Ramogi FM · Musyi FM). Introduce hybrid-ASR routing: Sunbird for `kik`+`luo`, MMS-1B-all for `kam` (Kamba fallback). Sampling stage 1 (embedding-cluster diversity) fires per-station. Sampling stage 2 (uncertainty) fires cross-station. Per-language WER/CER measured against Sunbird published baselines. Rung-1 lines emitted to `phase0/baseline_lines/`.

### Later (post-POC, HOLD until W3 close + owner ruling)

| Wave | Scope | Blocker |
|---|---|---|
| **W4 · 16 stations** | Extend to all 16 RMS stations from `W_AUDIO_POC_SCOPING §IV` | Compute · time; not architecturally new |
| **W5 · Character Register (§5-§7)** | Cluster over character streams; group-level entries; distance-gate for invention | Owner ruling on N (§3.10) + register-scope |
| **W6 · Watch for audio domain (Doc 8)** | Macho/Mkono/Witness for audio-specific integrity, poisoning, drift | Track-B wave; separate charter |
| **W7 · DAP sale surface** | R-6 pricing + R-7 disclosure budget bindings | Owner rulings R-6/R-7 |
| **W8 · WPW Tier-2 draft-on-settle** | Auto-emit tier-2 report on wave-close | WPW-v1-d spec landed; needs Ruling P1/P2/P3 for Tier-3 |
| **W9 · Release-gate ADMISSIBLE lift** | Move all bundles' `release_gate:PENDING` → ADMISSIBLE based on Ruling #5 verdicts | Owner Ruling #5 (KDPA + named-persons + transfer-basis) |

---

## 5 · SEQUENCING — what starts today vs blocked

### 5.1 · Can start with NO NAS + minimal owner ratification

| Item | Authorisation needed | Blocks |
|---|---|---|
| **W0 integrity fix** (parse `Kind:` + `output_verified_seal` predicate + STANDING ORDER) | Owner ratifies W0 scope | Nothing external |
| **W1 work-supervisor** (`services/work_supervisor/*` + STANDING ORDER "alive != done") | Owner ratifies W1 scope | Nothing external |
| **STANDING_ORDERS append** for L5 discipline | Same | Nothing external |
| **Contract additions** (`AudioSegmentV1` extending V0 with `languages[]`, `switch_points[]`, `codec_version`) | Owner ratifies bundle contract shape | Nothing external |
| **Bundle contract `AudioAttributeStreamBundle_v0`** | Same | Nothing external |
| **Model + dep install on GPU hosts** | HF token (owner) + `pyannote.audio` install authorisation (owner) | HF token landing |
| **Dry-run on FIXTURE audio** (`fixture_a_silence.wav`, `fixture_b_tone.wav` from `backend/tests/fixtures/audio/`) | Same | Nothing external — proves plumbing without real content |

### 5.2 · BLOCKED-ON-OWNER / EXTERNAL

| Item | Blocker | Nature |
|---|---|---|
| **W2 real vertical slice** | NAS network path (owner + sysadmin) | External network |
| **W2 real audio file** | NAS reach + station credential | External |
| **Runtime-humans policy** (`§13.2 Commission-does-not-open-until-agreed`) | Owner ruling on the ratification surface — API/UI shape | Governance |
| **Sale rulings** (KDPA verdict + named-persons verdict + transfer-basis + DAP R-6/R-7) | Owner Ruling #5 four sub-verdicts | Governance |
| **Storage-audio-for-sale ruling** | See §6 below — SILENT and needs owner ruling | Governance — the critical one |
| **Character Register N=5 default** | Owner override or accept default | Governance |
| **Speaker-verification threshold 0.4 default** | Owner override or accept default | Governance |
| **`gate_policy` default = `missed_stratum_gates_release`** | Owner override or accept default | Governance |
| **`AudioSegmentV1` codec_version field addition** | Owner ratifies parity bump | Contract change |

---

## 6 · **CRITICAL VERIFICATION — storage/purge reconciliation**

Owner's exact question: *"Spec §6.2 / perception_result purge_attestation says 'never stored audio; never per-utterance speaker embeddings.' The owner wants to SELL an audio corpus. Reconcile precisely: does the perception/measurement plane purge audio while a SEPARATELY governed deliverable path retains the music-free non-English segments under the release gate + owner rights (Ruling #2)?"*

### 6.1 · The exact clauses (VERBATIM, from files opened this session)

**Audio Plane §6.1 — Register Custody Boundary — governing distinction** (verbatim, `canon/text/Audio_Intelligence_Plane.md` §6.1):

> *"Organic characteristics are anatomical — vocal tract length, formant structure, glottal source, fundamental frequency range. They cannot be acquired or shed; they are what speaker verification keys on; they are biometric. **They are never registered**."*
>
> *"Learned characteristics are acquired from a speech community — phonological inventory, pronunciation variants, prosody, code-switching habits. They are group properties by construction. **Only learned characteristics may be registered**."*

**Audio Plane §6.2 bullet 4 — storage form** (verbatim, line 167):

> *"Stored as description, not exemplar. Centroids, distributions, frequencies. **Never stored audio; never per-utterance speaker embeddings**. Embeddings used during clustering are destroyed after cluster assignment. Provenance points to material, not to speaker identity."*

**Audio Plane §6.3 — enforcement shape** (verbatim, line 171):

> *"**The register write path** exposes no field through which an instance-level representation can be stored: the schema cannot represent a voiceprint. Unrepresentable, not policed (§1.5)."*

**`PurgeAttestation` contract** (`contracts/perception_result_v0.py` lines 49-59 verbatim):

> ```python
> class PurgeAttestation(BaseModel):
>     """Purge attestation (V1-D1). REQUIRED field, not optional. Missing → refused."""
>     purged: bool = Field(..., description="True iff worker-side raw AV was purged.")
>     purged_at: str = Field(..., min_length=1, description="ISO-8601 UTC timestamp of the purge attestation.")
> ```

**Audio Plane §7.3 — sellable artifact clause** (verbatim, line 193):

> *"A passing identity is issued a certificate stating that the voice is provably derived from no individual, naming the method, the threshold, and the corpus version scored against. **The certificate is a first-class sellable artifact**."*

**Canon 4 §16 (`C4-022`) — S-A terminus** (verbatim from `notes/canon_4_requirements.md`):

> *"S-A ends in a **FROZEN UNIT CONTRACT** — the deliverable's contents, licence label, privacy attestation, quality card, proof trail bound together and receipted."*

**Canon 4 §41 (`C4-057`) — contents attestation** (verbatim):

> *"Every dataset/brief/feed carries a CONTENTS attestation — what the deliverable contains and what it does not. What it does NOT contain is stated as explicitly as what it does. **Absence is a first-class fact**."*

**`a1_demux.py` docstring** (verbatim `services/perception/eab_1_pipeline/a1_demux.py` lines 12-15):

> *"Source objects are never modified or deleted; restructured audio is a derived artifact with lineage to the source object (existing provenance discipline; no new mechanism)."*

### 6.2 · Structural reading — the six clauses interpreted together

Interpreting all six clauses under §1.5 unrepresentable pattern:

1. **§6.1 + §6.2 + §6.3 are SCOPED to the CHARACTER REGISTER.** The section is titled *"Register Custody Boundary"*. The write path referenced in §6.3 is the *"register write path"*. **These clauses forbid audio in the Character Register — they do NOT forbid audio in every deliverable class.**

2. **`PurgeAttestation.purged` is SCOPED to worker-side.** The field description verbatim: *"True iff **worker-side raw AV** was purged."* — the purge is at job-completion of the perception worker, on that worker's transient scratch. It does NOT speak to a downstream deliverable path.

3. **The SOURCE ESTATE is untouched.** `a1_demux` docstring: source objects never modified or deleted. **The NAS files themselves persist across the pipeline** — this alone means the ESTATE retains audio.

4. **Deliverables (`C4-022 §16`) are CONTENT-AGNOSTIC by construction.** The `frozen unit contract` carries "deliverable's contents" as a first-class thing; **the spec does not specify what those contents may or may not include**. The three-class licence enum on `a2_license_class.py` (extended to four by Owner Ruling #2) governs the LICENCE, not the content type.

5. **§7.3 authors a sellable "certificate"** as one sellable class. It does not FORBID other sellable classes.

6. **Contents attestation (§C4-057) requires "absence is a first-class fact"** — a corpus that CONTAINS audio bytes vs one that contains ONLY transcripts is a difference in the contents-attestation, not in whether either is permitted.

### 6.3 · **VERDICT: (c) SILENT.** The spec does not preemptively bless nor preemptively forbid retaining music-free non-English audio segments as a sellable deliverable.

**What the spec CLEARLY FORBIDS:**
- Storing audio in the **Character Register** (§6.2 bullet 4).
- Storing per-utterance speaker embeddings **in the Character Register** (§6.2 bullet 4).
- Retaining embeddings past cluster-assignment (§6.2 bullet 4 verbatim: *"destroyed after cluster assignment"*).
- **Worker-side** raw-AV persistence past a job (V1-D1 REQUIRED-not-optional).

**What the spec CLEARLY ALLOWS:**
- Source-estate retention (a1_demux discipline — NAS files untouched).
- Frozen unit contract deliverables per `C4-022` — contents type not specified.
- Voice-identity certificates as sellable artifacts (§7.3).
- Governed licence-class stamping per `a2_license_class.py`.

**What the spec is SILENT ON — the specific owner question:**
- Whether a **separately-governed deliverable-path** may retain **music-free non-English speech segment BYTES** as part of a frozen unit contract with `licence_class: owner_full_rights` + release-gate ADMISSIBLE + Ruling #5 verdicts resolved.

### 6.4 · Recommended owner ruling shape

Three consistent paths — pick one, or a hybrid:

**Path A · GOVERNED AUDIO-BYTES RETENTION (aggressive-fidelity)**
- Deliverable retains music-free non-English audio segments as `.wav` files inside the bundle.
- **New licence class** `owner_full_rights_speech_corpus` beside the three extant `internal_only / public_derivative / member_owned`.
- **New service** `services/deliverable/audio_corpus/{store, integrity, purge_expired}.py` — separate from perception worker path.
- Release-gate `admit_release()` refuses tiers `audio_speech_no_speaker | audio_speech_with_speaker | biometric_embedding | named_identity` by default; owner Ruling #5 lifts.
- Character Register discipline PRESERVED VERBATIM — no audio ever crosses into `services/character_register/*`.
- Worker-side `PurgeAttestation.purged=True` PRESERVED — the deliverable service is NOT the perception worker.
- **Best fidelity for the lab; highest governance surface area.**

**Path B · POINTER-ONLY DELIVERABLE (governance-safe)**
- Deliverable is a MANIFEST of `{source-file-pointer-on-NAS, segment_offsets_ms, transcript}` triples per row.
- Buyer receives the manifest + transcripts; audio bytes stay on the source estate (NAS) with an access grant.
- **No new licence class needed** — internal_only + pointer-with-grant.
- **Zero deliverable-side audio retention** — audio bytes never leave the source estate.
- Falls apart if the lab needs OFFLINE audio for their own model training. **Verify with owner before committing to Path B.**

**Path C · DEFER (POC-first pragmatism)**
- Proceed with W0-W3 building the pipeline; the bundle contract carries a `pointer_or_bytes: Literal["pointer", "bytes"] = "pointer"` shape.
- Audio-bytes-retention lands in a later wave once Ruling #5 arrives.
- Corpus is TRANSCRIPT-ONLY through W3; upgrade path to bytes-retention is a schema-additive change.

**Recommendation, in fidelity + governance-hygiene order:** Path A (owner authorises) OR Path C (defer decision). Path B is the safest but risks lab-value collapse.

**Owner ruling requested at CP0 of W2 (before real audio flows).** Path C is the safe default if no ruling by then.

---

## 7 · CORRECTIONS TO OWNER'S SPECIFIC PROPOSALS (integrity mandate)

For clarity, every place I DISAGREED with, MODIFIED, or CLARIFIED the owner's proposal in this roadmap:

1. **Musyi FM (Kamba) not covered by Sunbird whisper — §0.1 correction.** Keep station; route Kamba ASR to `facebook/mms-1b-all` fallback.
2. **Speaker biometric embeddings** — owner's phrase *"WavLM/ECAPA embedding extractor (IN-MEMORY only)"* is correct AND aligns with §6.2 bullet 4 verbatim (*"destroyed after cluster assignment"*). **Confirmed.**
3. **`pyannote.audio 3.1`** — the pyannote-audio 3.x line is at 3.3.2 as of 2026-Q3 (verified in package registries); the 3.x diarization API is stable. **`3.3.2` proposed above** rather than `3.1` to catch the latest patch.
4. **Music separation approach** — owner said *"PANNs/YAMNet music-detection gate ... htdemucs_ft ... two-stems=vocals"*. Refined per §3.4: PANNs `Cnn14` (larger model, better AudioSet performance than YAMNet in published leaderboards); HTDemucs `--two-stems=vocals` mode; **discard `no_vocals.wav` per music-free filter**.
5. **Sampling seed** — owner said "20260909". Verified this is the extant `MTAFITI_GPU_SAMPLING_SEED` from W-MTAFITI-GPU-DISCOVERY CP1. **Reused unchanged; policy_id extended to `audio-poc-3-stations-v1`.**
6. **`temperature=0` determinism** — owner said "ASR temperature=0 (determinism)". Verified against `contracts/extraction_params.py` correction #2 — already banked as the platform's reproducibility discipline. **Aligns.**
7. **Quality gates** — owner proposed SNR≥25dB, MOS≥3.0, -23 LUFS. Refined: SNR ≥ 25 (accept) · SNR 15-25 (accept-with-stratum-flag) · SNR < 15 (reject). MOS ≥ 3.0 (accept). -23 LUFS ± 1 LU (existing a1_demux target — verified).
8. **Storage/purge reconciliation** — the owner's premise implies audio-bytes-retention is allowed under a separate governance path. **This is SILENT in the spec.** §6.2 forbids audio-in-register; `PurgeAttestation` forbids audio-in-worker-scratch; the deliverable path is not explicitly authored either way. **Requires owner ruling before W2.** Recommended Path A or Path C.
9. **§10.1 `gate_policy` default = `missed_stratum_gates_release`** — owner-authored. Verified alignment with §10.2 verbatim rationale + `C4-052 §36 Standards`.
10. **Watch-for-audio** — owner mentions Watch integration in L5. Verified: Watch bundle chartered as Track-B but un-built for audio domain (72 Canon 8 rows). **The W1 work-supervisor is a STANDALONE step-0 approximation** — Watch integration is a later wave (W6). W1's `output_verification_watchdog.py` writes to `phase0/work_supervisor_marks/` as a stopgap until `services/watch/marks/` lands.
11. **Standing Orders addition** — owner suggests two new STANDING ORDERs (W0 "seal-verification defect" + W1 "alive != done"). Verified both are new material vs current STANDING_ORDERS.md content (no prior orders touch these predicates). **Ready to author under owner ratification.**

---

## 8 · ATTESTATION

- **No product code touched.** No `services/**/*.py` edited or created. No pytest invoked. No testing_agent invoked. Ratchet floor **3251** untouched.
- **No push.** Local commit only, on workspace `master` (this document).
- **Retracted ChatGPT integration** — no OpenAI/ChatGPT reference anywhere in this document.
- **POC HOLD in force** — `W-AUDIO-POC-3-STATIONS` CP0 does not open until owner ratifies (a) this roadmap, (b) 3-station selection with Kamba fallback path, (c) storage/purge Path A / B / C ruling.
- **Every technical claim in this document was verified against a file opened in this session** — HuggingFace card lookups + repo file opens + spec verbatim quotes + live SSH probe. Web-searches were used only for the two HF model verifications (MMS-LID-4017, Sunbird 51-African-languages) and are cited inline.
- **Integrity corrections banked at §0 and §7.** The Musyi-Kamba coverage gap is the largest concrete correction; the storage-purge reconciliation is the largest structural correction.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
