READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CANON_MODEL_SPECS_VERBATIM_20260914.md

**Purpose.** Answer the owner's direct question: *"All the specs of models to use etc is all in the docs."* Search **every canon document on disk** (`/app/assessment_workspace/canon/**` + `/app/assessment_workspace/notes/canon_*_requirements.md`) for every **named model, model family, model-selection rule, or model-choice-deferral ruling** — ASR, language ID, codec, speaker verification, diarisation, LID, VAD, embeddings, LLM. Verbatim quotes only. Zero invented terminology.

**Discipline anchor:** DECISIONS.md ruling 2026-09-15T~01:40Z (Verbatim-canon discipline). Every row carries the source file, section anchor, and verbatim quote.

**Search method:** exhaustive `\b<name>\b` case-insensitive regex across 294 text files under `canon/` + `notes/` with a 55-name candidate-model list (whisper family, kaldi, vosk, wav2vec/wavlm/hubert, silero, pyannote, ecapa/titanet/x-vector, encodec/soundstream, deepgram/assemblyai/groq, langid/fasttext/cld3, etc.). Search receipts preserved in the analysis run at 2026-09-15T~01:52Z.

---

## Bottom line (owner-facing answer, up front)

The canon corpus **does** name models. It does so in three places, and the rulings partition the model-choice question into three distinct planes:

1. **CI / fixture / test-registry seed:** **CANON, EXPLICITLY NAMED.** Canon-17 §A17.10 (parity: Canon-17-20-v3 §A17.10) names `whisper-tiny` with `faster-whisper (ctranslate2)` backend, MIT licence, SHA-pinned, "**NOT for production use**". This is the only production-adjacent ASR model the canon names outright — and it is explicitly earmarked CI-only.

2. **Production ASR model:** **CANON, EXPLICITLY DEFERRED.** Canon-17 §A17.11 (parity: Canon-17-20-v3 §A17.11) rules: *"Production base model selection lands additively at a later registry bump — 'named at first census activation'"* — the canon literally forbids naming the production model in advance of the census.

3. **Production starting-point family (per weak surface):** **CANON, ENUMERATED AS 'STARTING POINTS'.** Canon-4 §50.1 (the speech instantiation of the weak-surface doctrine) enumerates concrete starting-point model families and corpora per weak surface (Swahili & Kenyan languages, code-switching, accented English, degraded audio, speaker overlap). These are labelled "Starting point" — legitimate curation, not the production choice; the production choice follows §A17.11.

4. **Audio Intelligence Plane Spec v1.0 (this new drop):** **SILENT on model names.** The v1.0 spec describes model roles (§3 codec, §4.1 LID, §7.2 speaker-verification-distance-gate) as **capabilities**, not choices. §16.2 open-decision P250 makes the codec choice explicit as a **product-owner decision deferred until Sampling & Reflection can measure it**.

**Consequence for the pending transcription POC (per owner directive):**

* The owner's earlier "faster-whisper default" for the POC **IS canon-consistent** — but only as a **CI fixture path**, not as a production ruling. Grounding: Canon-17-20-v3 §A17.10.
* Fall-back to `whisper.cpp`: **NOT SUPPORTED by canon** — no mention anywhere in the corpus. Marked INFERRED.
* Cloud ASR (Groq / Deepgram / AssemblyAI / OpenAI): **CANON-INCOMPATIBLE** under Pull Seam Principle 1 (P015.s5, P015.s6, P015.s7 — "no configuration in which estate data is transferred to compute outside the perimeter · prohibition with no exception"). This aligns with the owner's already-stated ruling.
* The POC therefore proceeds against **whisper-tiny + faster-whisper (ctranslate2)** as the canon-named CI fixture — pending owner confirmation because the canon labels this "NOT for production use" and the POC is a **transcription feasibility POC on real NAS bytes**, which straddles the CI-vs-production line. Marked **DEFAULT-PENDING-OVERRIDE** on that straddle.

---

## Table 1 · Named-model canon rulings, verbatim

| Row | Source file | Section | Verbatim quote | Classification |
|---|---|---|---|---|
| M-01 | `canon/text/Akki_Canon_Documents_17_19.txt` | §A17.10 [CANON] | *"The registry seeds with whisper-tiny — MIT-licensed (OpenAI's original release via Systran's faster-whisper/CTranslate2 conversion), weights SHA-pinned, origin URL recorded — explicitly marked "CI CPU-mode ASR fixture model. NOT for production use.""* | **Canon · CI-fixture model named** |
| M-02 | `canon/text/Akki_Canon_Documents_17_19.txt` | §A17.10 registry JSON block | *"whisper-tiny: { family: Whisper-class, role: ci_fixture_asr, backend: faster-whisper (ctranslate2), license: MIT (OpenAI Whisper original release · Systran faster-whisper conversion), purpose: CI CPU-mode ASR fixture model. NOT for production use. }"* | **Canon · registry-seed schema** (verbatim; whitespace normalised) |
| M-03 | `canon/text/Akki_Canon_Documents_17_19.txt` | §A17.11 [CANON] | *"Production selection is named after the census, not before it. Production base model selection lands additively at a later registry bump — "named at first census activation" — following the identical license-verify → checksum-pin → Owner-ruling sequence already registered for the Qwen3 and Llama text-generation candidate rows in the same file."* | **Canon · production-ASR named-after-census rule** |
| M-04 | `canon/text/Akki_Canon_Documents_17_19.txt` | §A17.11 [CANON] tail | *"The sequencing consequence is direct: the census (Documents 9–10) runs first, and the specific model is named after, informed by what the census actually finds in the estate — not chosen speculatively ahead of it on the strength of a published benchmark."* | **Canon · sequencing anchor** (loads onto the census run's Promise-12 anchor) |
| M-05 | `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt` | §A17.10 [CANON] | *[identical to M-01 · parity]* | Canon · v3 parity |
| M-06 | `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt` | §A17.11 [CANON] | *[identical to M-03/M-04 · parity]* | Canon · v3 parity |
| M-07 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 (Speech — the instantiated example) · weak-surface table row 1 | *"Swahili & Kenyan languages ⎢ Meta MMS, multilingual Whisper, Mozilla Common Voice Swahili, FLEURS, KenCorpus. ⎢ Registry-pinned base models per language; language-routed selection at job level. ⎢ Per-language word-error rate on a small real sample — measured in week one."* | **Canon · starting-point family for Swahili/Kenyan-language ASR** |
| M-08 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 weak-surface table row 2 | *"Code-switching (Sheng, Swahili–English) ⎢ Code-switch fine-tuning recipes; East African community corpora. ⎢ Census-curated code-switch corpus, fine-tuned in-perimeter; the improved model re-enters via a registry bump. ⎢ Code-switched-segment word-error rate against a monolingual baseline, same speakers."* | **Canon · starting-point for code-switch ASR** |
| M-09 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 weak-surface table row 3 | *"Accented English ⎢ Pan-African accented-English corpora and adaptation literature. ⎢ Fine-tune or adapter on an accented checkpoint, provenance pinned either way. ⎢ Accent-stratified word-error rate on real archive segments."* | **Canon · starting-point for accented-English ASR** |
| M-10 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 weak-surface table row 4 | *"Degraded, telephone, or archival audio ⎢ Standard augmentation and domain-adaptation recipes for narrowband, noisy audio. ⎢ Augmentation in the training loop; era- and quality-stratified census slices target the hard bands directly. ⎢ Word-error rate by decade and quality band — the census supplies the strata at no extra cost."* | **Canon · starting-point for degraded audio** |
| M-11 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 weak-surface table row 5 | *"Speaker overlap and call-in diarisation ⎢ Open diarisation stacks and overlap-aware recipes. ⎢ Diarisation model swap via the registry; the voice-activity detector and diariser upgrade independently. ⎢ Diarisation error rate on a multi-speaker call-in sample."* | **Canon · starting-point for diarisation** |
| M-12 | `canon/text/Akki_Canon_4_Operating_Engines.txt` | §50.1 preamble sentence | *"Engineer the inputs relentlessly; never touch the test. Model choice, fine-tuning, augmentation, and corpus curation are all legitimate curation of success. The validation verdict is drawn from measured estate composition, post-census, uncurated — a rehearsed checkpoint is preparation; a curated verdict is worthless the moment real material meets it."* | **Canon · model-choice-is-curation doctrine** |
| M-13 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §3.2 P045 | *"Service · perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."* | **Canon · codec service path (module name only · not a model name)** |
| M-14 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §3.2 P047 | *"Output · { content_tokens[], character_stream, codec_version } · Target token rate 50–100 tokens/second of audio."* | **Canon · codec output contract (spec, not model)** |
| M-15 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §3.2 P048 | *"Provenance · codec_version is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens."* | **Canon · codec_version is a mandatory provenance carrier** |
| M-16 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §4.1 P060 | *"A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."* | **Canon · LID capability spec (no named model)** |
| M-17 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §7.2 P109 | *"Every constructed identity is scored against every speaker representation derivable from the corpus using standard speaker-verification methods. A minimum distance from all of them is required."* | **Canon · speaker-verification capability spec (no named method)** |
| M-18 | `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` | v1.0 §16.2 P250 (open-decision) | *"Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built (§3, §11.2)."* | **Canon · codec choice is a v1.0 open decision** |

---

## Table 2 · Search receipts — models NOT found in canon (verbatim absence)

| Candidate | Canon corpus hits | Absent-in-canon claim |
|---|---|---|
| `kaldi` | 0 hits under `canon/` | Canon does not name Kaldi. |
| `vosk` | 0 hits under `canon/` | Canon does not name Vosk. |
| `whisper.cpp` / `whispercpp` | 0 hits under `canon/` (my previous "fall-back to whisper.cpp" suggestion is INFERRED and NOT canon-supported) | Canon does not name whisper.cpp. |
| `distil-whisper` / `whisper-turbo` / `whisperx` | 0 hits under `canon/` | Canon does not name these variants. |
| `wav2vec` / `wav2vec2` | 0 hits under `canon/` (v1.0 spec says nothing) | Canon does not name wav2vec/wav2vec2. |
| `hubert`, `wavlm` (as SSL models) | 0 hits under `canon/` (only referenced in `notes/GPU_HOST_STORAGE_PREFLIGHT_20260912.md` as candidates, not in canon) | Canon does not name HuBERT or WavLM in text. |
| `encodec` / `soundstream` / `descript` / `dac` | 0 hits under `canon/` (only in notes as SILENT-in-doc annotations) | Canon does not name any specific neural audio codec. |
| `pyannote` (as canon requirement) | 0 hits in canon text — only in `notes/*` as implementation surface | **Deployed in-repo but not named by canon.** Marked INFERRED against Canon-4 §50.1 "Open diarisation stacks" starting-point clause. |
| `silero` | 0 hits under `canon/` (deployed as `services/perception/eab_1_pipeline/a1_vad.py`; registry-pinned in `models_registry.v0.json`) | **Deployed in-repo but not named by canon in text.** Marked INFERRED. |
| `ecapa` / `ecapa-tdnn` / `x-vector` / `titanet` / `resemblyzer` | 0 hits under `canon/` | Canon does not name any speaker-verification model — the "standard speaker-verification methods" phrase (§7.2) leaves this open. |
| `deepgram` / `assemblyai` / `groq` / `openai gpt-4o-transcribe` | 0 hits in canon; cloud ASR excluded a priori by Pull Seam §2 P1 (P015.s5..s7) | Canon-incompatible for the estate pull-seam architecture. |
| `fasttext` / `cld3` / `langid` (as canon requirement) | 0 hits under `canon/` (only in `notes/*` as SILENT-in-spec annotations + one HUAWEI drill candidate) | Canon does not name a specific LID model. |

---

## Roll-up · the model-choice ladder as the canon lays it out

1. **CI fixture** (installed at registry seed): `whisper-tiny` · backend `faster-whisper (ctranslate2)` · MIT licence · SHA-pinned · **explicitly not-for-production**. Source: Canon-17-19 §A17.10 (M-01, M-02). Canon-17-20-v3 §A17.10 (M-05).
2. **Production ASR selection** — deferred by canon until **first census activation**. The census must run first; the production model is named after. Source: Canon-17-19 §A17.11 (M-03, M-04). Canon-17-20-v3 §A17.11 (M-06).
3. **Per-language starting points** enumerated in Canon-4 §50.1 — legitimate curation, not the final choice. Source: M-07..M-11.
4. **Codec (v1.0 spec)** — deferred as a §16.2 P250 **open decision, owner: product**. Source: M-18.
5. **LID (v1.0 spec)** — capability spec only, no named model. Source: M-16.
6. **Speaker verification (v1.0 spec)** — capability spec ("standard methods"), no named model. Source: M-17.
7. **Diarisation** — Canon-4 §50.1 M-11 names "Open diarisation stacks" as the starting-point family; concrete model deferred.

---

## Superseded rulings in this session

* My earlier POC framing at 2026-09-15T~01:35Z proposed **faster-whisper (a)** and **whisper.cpp (b)** as the local ASR default, and **cloud ASR (c)** rejected on Pull-Seam grounds. Re-anchored per this table:
  * **(a) faster-whisper + whisper-tiny CI-fixture** — **CANON-CONSISTENT for a CI/POC path** (Canon-17-20-v3 §A17.10, M-01/M-02).
  * **(b) whisper.cpp** — **NOT canon-supported.** Zero hits in the canon corpus. Marked **INFERRED** and dropped from the default unless the owner ratifies.
  * **(c) cloud ASR** — **Correctly rejected on Pull Seam grounds.** Confirmed by verbatim canon corpus (P015.s5..s7).
  * **Production model** — my proposal to POC a production choice was overreach. Canon-17-20-v3 §A17.11 (M-03, M-04) explicitly defers production selection until first census activation. **The POC therefore operates against the CI-fixture model only.**

---

## Cross-links

* Structured extract (v1.0 spec): `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt`.
* Verbatim requirements extract (v1.0 spec): `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md`.
* Drift audit vs built work: `notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md`.
* Canon-17-19: `canon/text/Akki_Canon_Documents_17_19.txt`.
* Canon-17-20-v3: `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt`.
* Canon-4 (Operating Engines): `canon/text/Akki_Canon_4_Operating_Engines.txt`.
* Standing rule anchor: DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
