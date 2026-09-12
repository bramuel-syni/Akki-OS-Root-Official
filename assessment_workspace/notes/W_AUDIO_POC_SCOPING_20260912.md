# Media / Audio Census — POC Scoping (read-only)

**Task class:** Scoping / Discovery ONLY. No product code. No pytest. No ratchet touch (floor 3251 held). No downloads. No commits of credentials. No push.
**Directive received:** 2026-09-12T~11:30Z (owner) + 2026-09-12T~12:00Z (addendum — 6-point owner rulings, banked verbatim in `STATE/DECISIONS.md`).
**Executor:** track-a agent, this session, from a compaction-safe restart re-grounded against `STATE/STANDING_ORDERS.md` + `STATE/DECISIONS.md` + `STATE/NEXT.md` + `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md` + `notes/HUAWEI_CONNECTIVITY_DRILL_20260909.md` + `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`.
**Ground state at task open:** ratchet floor **3251** (double-green byte-match), last wave closed **W-MTAFITI-GPU-DISCOVERY** at 2026-09-12T~07:35Z, `programme/track-a` HEAD `77834d1`, workspace `master` HEAD is this commit.

---

## I · NAS reachability (owner scoping item 1)

**Verdict: NAS `10.10.55.55:5000` is unreachable from this pod.**

Evidence (single-shot, all four probes agree):

| Probe | Result | Time |
|---|---|---|
| Pod egress IP | `35.225.230.28` (Google LLC AS396982, us-central1) — **drifted again since the prior `34.16.56.64` recorded in Part 5 of `HUAWEI_CONNECTIVITY_DRILL_20260909.md`; live proof that egress-IP whitelisting is not the right shape for this network** | now |
| Kernel route to `10.10.55.55` | `via 169.254.4.6 dev eth0 src 10.232.137.133` — the default GKE link-local gateway; the pod does not have an intra-VPC route into `10.0.0.0/8` | — |
| TCP handshake `10.10.55.55:5000` | `TimeoutError` after 5,004 ms | — |
| HTTP GET `http://10.10.55.55:5000/` | curl exit 28 · HTTP 000 · `Connection timed out after 5000 milliseconds` | 5.001 s |
| `traceroute` | tool not installed in this image | — |

**Why:** `10.10.55.55` is an RFC-1918 private-space address. The pod is a GKE-hosted container in `us-central1` (Council Bluffs, Iowa) with no VPN, no VPC peering, and no Direct Interconnect to the on-premise Nairobi network where the Synology NAS lives. The kernel returns a route via the default gateway because the pod has no more-specific route for `10.10.0.0/16` — the packet is then dropped or blackholed at the first hop.

**What is needed to reach:** identical shape to what §3.A of `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md` proposes for the Huawei RDS estate — either (a) an on-premise bastion with a stable public EIP that we allowlist by /32 into the NAS's local firewall, or (b) a Nairobi-side VPN endpoint we can tunnel through, or (c) an alternative access-path the sysadmin can name. Directly whitelisting a `34.x.x.x/32` in the on-premise firewall repeats the ephemerality risk we already banked (`FL-P2-09` from the Huawei drill: egress IP drifted `34.16.56.64` → `35.225.230.28` inside the intervening days).

**Read-only ceiling:** even if reach lands, the standing law's scoping-only clause holds — at most enumerate top-level folder names and confirm the API surface (Synology DSM `FileStation` API at `/webapi/entry.cgi?api=SYNO.FileStation.List`). **No file downloads. No audio movement.** The POC's first live probe becomes CP2 of the new wave (see §VII).

**Ambiguity applied under STANDING_ORDERS §2:** the owner's directive named creds "in the owner's message" but no NAS credential file has landed at `/app/backend/estate_keys/data_sources/`. If the owner has already sent one, it did not arrive in this workspace — flag before POC opens. **DEFAULT-PENDING-OVERRIDE:** treat reachability as the blocker and defer credential handling to the same conversation that fixes the network path.

---

## II · Audio capability location, maturity, model deps (owner scoping item 2 · Ruling #1)

**Verdict: the audio capability lives in `Extraction-Akki` and only in `Extraction-Akki`. It is a well-structured, contract-first, CI-fixture-tier pipeline with real ASR + diarization providers wired but not-yet-run-against-real-audio.**

### II.1 Exact paths + LoC

Directly opened this session on branch `programme/track-a` (SHA at wave-close `77834d1`):

| File | LoC | Purpose |
|---|---:|---|
| `backend/services/perception/eab_1_pipeline/__init__.py` | 45 | Pipeline atomic registry (A1.1 demux · A1.2 segmentation · A1.3 VAD · A1.4 dedup · A2.1 occurrence writer · A2.2 trace walker · A2.3 licence class) |
| `backend/services/perception/eab_1_pipeline/a1_demux.py` | 82 | FFmpeg-backed demux + normalize (target 16 kHz mono PCM float32; -23 LUFS EBU R128) · **wire contract module, real backend adapter deploys under `backends/`** |
| `backend/services/perception/eab_1_pipeline/a1_segmentation.py` | 127 | Content-addressed batch segmentation · 15–60 min windows (default 30 min) · programme-block-hint aware |
| `backend/services/perception/eab_1_pipeline/a1_vad.py` | 140 | Silero VAD (registry-pinned) · non-speech LOGGED as content-type index entries (`music \| ad \| silence \| tone \| unknown`), never discarded (R-A1.3 honesty grammar) |
| `backend/services/perception/eab_1_pipeline/a1_dedup.py` | 129 | Cross-batch dedup — same source, overlapping content |
| `backend/services/perception/eab_1_pipeline/a2_occurrence_writer.py` | 156 | Emit A2 occurrence rows to registry |
| `backend/services/perception/eab_1_pipeline/a2_trace_walker.py` | 118 | Provenance-chain walker |
| `backend/services/perception/eab_1_pipeline/a2_license_class.py` | 62 | Licence-class tagging |
| `backend/services/perception/asr_worker.py` | 248 | ASR worker orchestration (factory-dispatched provider) |
| `backend/services/perception/diarization_worker.py` | 197 | Diarization worker orchestration |
| `backend/services/perception/gpu_execution/audio_batching.py` | 32 | GPU batch composer |
| `backend/services/perception/gpu_execution/model_loader.py` | 45 | GPU model loader (fp16/int8 profile) |
| `backend/services/perception/job_dispatcher.py` | ~130 | Perception job dispatcher |
| `backend/services/perception/model_registry.py` | ~120 | Perception model registry |
| `backend/services/perception/models_registry.v0.json` | — | Seeded models — **only `whisper-tiny` present** (CI fixture) |
| `backend/services/perception/connectors/archive_reader.py` | — | Archive-reader connector (candidate NAS-integration point) |
| `backend/services/perception/source_connector_adapter.py` | 42 | Source-connector adapter |
| `backend/services/perception/worker_credential.py` | ~110 | Worker-side credential holder |
| `backend/services/layer_b/__init__.py` | — | Layer-B contract package |
| `backend/services/layer_b/contracts.py` | — | `AsrCue`, `AsrPerception`, `AsrProvider`, `DiarizationTurn`, `DiarizationPerception`, `ProviderUnavailable` |
| `backend/services/layer_b/factory.py` | — | Provider factory (dispatches to `whisper`, `faster_whisper`, `pyannote`) |
| `backend/services/layer_b/asr/whisper_provider.py` | 56 | **Cloud path** — OpenAI Whisper API brokered through `services/synisense/shield/perception_router` (audio bytes never escape the Inner Gate) |
| `backend/services/layer_b/asr/faster_whisper_provider.py` | 90 | **Local path** — CTranslate2 backend, `WhisperModel(_MODEL_SIZE)`. **`faster-whisper==1.2.1` IS listed in `backend/requirements.txt`**. Lazy download on first `transcribe()`; construction alone does not download. |
| `backend/services/layer_b/diarization/pyannote_provider.py` | 80 | **Local path** — `pyannote/speaker-diarization-3.1` via `pyannote.audio.Pipeline.from_pretrained`. **`pyannote.audio` is NOT in `backend/requirements.txt`.** `ProviderUnavailable` at construction until installed; token gate enforced at `_ensure_pipeline()` via `HUGGINGFACE_HUB_TOKEN`. |
| `backend/services/layer_b/vision/frame_perception_provider.py` | — | Vision (frame-perception) sibling |
| `backend/services/synisense/shield/perception_router.py` | — | Shield's Inner-Gate broker for outbound perception calls |
| `backend/services/synisense/shield/tenant_catalogue.v0.json` | — | Tenant catalogue (includes audio classes) |
| `backend/contracts/audio_segment_v0.py` | — | Frozen audio-segment contract (Pydantic BaseModel) |
| `backend/contracts/perception_job_v0.py` | — | Frozen perception-job contract |
| `backend/contracts/perception_result_v0.py` | — | Frozen perception-result contract |
| `backend/tests/invariants/audio_segment_v0.contract_snapshot.json` | — | Frozen-contract-parity snapshot (audio segment) |
| `backend/tests/fixtures/audio/__init__.py` | — | Test audio fixtures |

Total: **~2,000 LoC** of dedicated audio pipeline + ~5 frozen contracts + fixture set + 2 real provider families (whisper API cloud path AND local faster-whisper) + local pyannote diarization + Silero VAD.

### II.2 Model deps actually in `backend/requirements.txt`

Directly grepped this session:

- `faster-whisper==1.2.1` ✅
- `ctranslate2==4.8.1` ✅ (faster-whisper's backend)
- `onnxruntime==1.27.0` ✅ (Silero VAD's runtime)
- **`pyannote.audio` — ABSENT** (provider raises `ProviderUnavailable` at construction) — a POC needing diarization must install this + provide `HUGGINGFACE_HUB_TOKEN`.
- **`torch` / `torchaudio` — not visible in a first-pass grep** — must be re-verified before the POC opens (faster-whisper does not strictly need torch, but pyannote does).
- **No `librosa`, no `pydub`, no `demucs`, no `speechbrain`, no explicit `music_detect` or `source_separation` module** — these are gaps if the POC needs them.
- **`ffmpeg`** — the pipeline's demux comment says "Real-world backend adapter is `ffmpeg` (deterministic, cross-platform, in registry pin at deployment)"; a POC must confirm `ffmpeg` binary is available on the GPU host image.

### II.3 Maturity assessment

Applying the same evidence-class discipline as W-MTAFITI (no verdict, only detection):

| Component | Evidence class | Notes |
|---|---|---|
| Wire contracts (audio_segment_v0, perception_job_v0, perception_result_v0) | **DETECTED — DEPLOY-READY** | Frozen · parity-snapshot present · Pydantic BaseModel |
| Demux / segmentation / VAD (a1_*) | **DETECTED — WIRE-CONTRACT-READY** | Python module carries the deterministic wire contract; the real ffmpeg + Silero backend adapters "deploy under `backends/`" per the module docstring. **The `backends/` folder is not visible in `backend/services/perception/eab_1_pipeline/`** — that adapter shim is missing on `programme/track-a` HEAD. |
| ASR cloud (whisper_provider) | **DETECTED — INNER-GATE-ROUTED** | Constructs without network. `transcribe()` calls `perception_router.transcribe()` which resolves the outbound SDK at call time. If `emergentintegrations` doesn't expose a whisper seam, provider raises `ProviderUnavailable` with an actionable message. **The seam exists as a contract; whether it resolves live is a POC probe, not a scoping fact.** |
| ASR local (faster_whisper_provider) | **DETECTED — CONSTRUCTION-CHECKS-IMPORT · MODEL-DOWNLOAD-LAZY** | `faster-whisper` library is in requirements. Construction attempts `from faster_whisper import WhisperModel` and raises `ProviderUnavailable` if the import fails. **Model download happens on first `transcribe()`, not at import** — a POC must accept a first-run download latency, or pre-warm the model on the GPU host. |
| Diarization (pyannote_provider) | **DETECTED — MISSING-DEP + MISSING-TOKEN** | `pyannote.audio` not in requirements; `HUGGINGFACE_HUB_TOKEN` not in `backend/.env` (unverified — should verify before POC opens). Two known gaps that must be closed at CP1 of the POC wave, not deferred. |
| GPU execution (`gpu_execution/`) | **DETECTED — SMALL** | 32 LoC batching + 45 LoC model_loader. Framework, not implementation depth. |
| Language identification | **DETECTED — GAP** | Zero language-id modules found. The `WhisperApiProvider` uses `language_hint="en"` as a hard-coded default; language-id must either come from `whisper.transcribe(language=None, task="transcribe")` auto-detection (multilingual-model-only) or a separate LID module. Owner ruling #4 makes this critical. |
| Music/speech split, source-separation | **DETECTED — GAP** | Silero VAD's non-speech content-type index (`music \| ad \| silence \| tone \| unknown`) is only a label emitted by the VAD; there is no separate music-detect / demucs / source-separation module. |
| Speaker biometrics beyond diarization | **DETECTED — GAP** | Diarization emits `(t_start_ms, t_end_ms, speaker_label)` tuples; no persistent speaker-embedding store or cross-recording identity re-linking module. Owner ruling #5 asks for "voice/biometric embeddings" which needs an added pyannote embedding extractor OR speechbrain / nemo module. |
| Model registry seed | **DETECTED — CI-TIER** | `perception/models_registry.v0.json` names only `whisper-tiny` (per owner Ruling 9.2a-E1 α + seed-with-CI-fixture correction 2026-07-10). This is a CI fixture, not a shipping production choice. |

**Overall maturity read (paper, not decision):** the AUDIO PIPELINE IS THERE. Contracts, atomics, providers, GPU framework — the shape is complete. What's missing is (a) the ffmpeg/Silero backend adapters under `backends/`, (b) pyannote.audio + HF token installed for local diarization, (c) a language-ID module, (d) a music/speech binary classifier (vs the VAD's label-only content-type index), (e) a speaker-embedding extractor. **Zero of these are new engines; four of five are wave-scope adds inside the existing perception package. That's a MODIFY / EXTEND posture, not a BUILD-FROM-SCRATCH.**

**Nothing in `Akki-OS-V1`, `Akki-Executive-Core`, `Akki-Executive-Final`, or `RMS-IQ-Core-2` competes with Extraction-Akki's perception package. The Akki-OS-V1 `layer_a/handlers/audio.py` is a thin dispatcher stub, not a pipeline.**

---

## III · Surface map (owner scoping item 3)

Each existing Akki surface hosts a stage of the audio-census pipeline the same way it hosts the DB-census one. Nothing new is built at the surface layer for the POC — surfaces are consumers of receipts, not producers of audio.

| Surface | POC stage it hosts | Mechanism (existing, referenced-not-copy) |
|---|---|---|
| **Connect · Data tile** | NAS admission event — the Synology NAS is a declared data source. | `services/connect/data_source_admit` — writes admission record + ledger row + declaration entry (VM-as-actor precedent from `WS-BUILD-CONNECT-GPU`). Reuse-first per Ruling 3. |
| **Mtafiti (Registry)** | Media-composition census — the audio equivalent of the DB composition census landed at CP4 of W-MTAFITI-GPU-DISCOVERY. Per-station file inventory · duration · format · sample-rate · bitrate · language-hint · programme-block hint. | `services/mtafiti/composition_census.py` shape — new `services/mtafiti/media_composition_census.py` sibling, same `MtafitiObjectiveCarrier` origin discipline, same `DetectionSignal` output shape. |
| **Audio capability (Extraction-Akki perception)** | The actual pipeline. Runs the eab_1 atomics (demux → segmentation → VAD → language-ID → ASR → diarization → biometric embeddings → quality) with `synthetic_plumbing_only=False` for the first time on real off-air files. | Modules enumerated in §II.1. |
| **Targeta + CIF** | Objective + qualification for the corpus — Mtafiti-Ruling on `MtafitiObjectiveCarrier.origin`: origin is **`TARGETA`** (owner has stated the objective: "sellable non-English music-free quality-graded speech corpus"). CIF hosts any ideation that happens during the POC's ablation runs (e.g. "should we filter for min-3s speech spans"). | Existing `contracts/mtafiti_objective_carrier.py` refuses mtafiti-internal origin by construction — reused directly. |
| **Solva** | Where the corpus becomes a sellable product-shape — sample packaging, per-language QA reports, corpus manifest, licence-class stamping. **Not this POC wave.** POC ends at sample-bundle + quality-profile; Solva packaging is a subsequent wave. | `services/solva/*` (existing) — no touch this POC. |
| **Shield / Train** | Governance chokepoint for the biometric artifacts — Ruling #5 gate lives here as `release_gate: PENDING` on every biometric artifact until owner + KDPA rule clears. Prevents Solva packaging from consuming ungated biometric material by construction (mirror of the `MaskingTierNotAdmitted` HARD GATE from `W-Shield-Train-BUILD`). | `services/shield_train/` — Add `services/shield_train/release_gate.py`: `admit_release(artifact, tier: {'text_non_english', 'text_english', 'audio_speech_no_speaker', 'audio_speech_with_speaker', 'biometric_embedding', 'named_identity'})` — refuses tiers 4/5 by default until admissibility banked. |
| **DAP (Data-Access-Plane)** | The lab is a third-party access. DAP hosts the lab's actor identity, the outbound handoff, the rate-limit, the R-6 pricing and R-7 disclosure-budget rulings mentioned in the owner's scoping directive point 5. Delivery to the lab flows through DAP with attribution + receipt, never a bulk copy. | `services/dap/*` (existing per BUILD_STRATEGY.md Part 2 BUILD items). Adds nothing new; the lab is another registered actor. **Owner-side action: bind lab identity + R-6/R-7 configs when the POC's release gate lifts.** |
| **Whitepaper Wizard (WPW)** | Tier-1 notebook AUTO-ATTACHES to every POC checkpoint per the campaign discipline from `W-CAMPAIGN-INFRA`. Tier-2 report at wave close (POC's held-out measurements = quality-profile per station). Tier-3 white paper (corpus-shape publication) stays gated on R1/R2/R3 rulings — unchanged. | `services/whitepaper_wizard/` — reused as-is. |
| **GPU infra (Cassava H200 hosts)** | The actual compute. Ruling #6 confirms audio processing runs on `akki-vm` + `akki-vm-ii` at $0 marginal (Cassava lease). Dispatcher pattern from `W-CAMPAIGN-INFRA` runs POC jobs as another campaign. | `campaign_infra/production_trainer.py` shape — new `campaign_infra/production_audio_extractor.py` sibling, same `on_host_queue_dispatcher` + heartbeat + reconcile discipline. **Dispatchers are already alive on both hosts** — see §VI. |

**One diagonal:** the same registry / matrix / ledger discipline that gated `W-MTAFITI-GPU-DISCOVERY`'s live SQL applies to the media reads. The `readonly_sql_guard.py` primitive becomes a `readonly_media_guard.py` sibling — refuses any operation on the Synology FileStation API other than READ / LIST / STATUS / DOWNLOAD-TO-HSS. Every fetched audio file's sha256 gets banked as it lands; every extract call routes through `refuse_if_write`-style admission; every biometric-affected artifact carries `release_gate:PENDING`. **Same walls, different domain.**

---

## IV · Station → Language map (owner scoping item 4)

Per web search (Royal Media Services official site + Kenyan-media directories; 2 sources per row; see the Sources block at foot of table). **Owner said 16 stations; the RMS official site lists 13 primary radio brands, several third-party directories add up to 14+, and there is no directory that names 16.** This is a naming-scope question the sysadmin should confirm the moment the NAS becomes reachable — the top-level folder names on `10.10.55.55:5000` will settle it in one probe. Until then, this map is the best construction of a 16-slot list from public sources:

| # | Station | Language | Language-family | Region / audience | Owner |
|---:|---|---|---|---|---|
| 1 | **Radio Citizen** | Swahili | Bantu · Sabaki | National | Royal Media Services |
| 2 | **Hot 96** | English (music/talk) | Germanic | Urban / national | RMS |
| 3 | **Inooro FM** | **Kikuyu (Gĩkũyũ)** | Bantu · Central Kenya | Mt Kenya + Central + diaspora — largest single-ethnicity population (~7 M+) | RMS |
| 4 | **Ramogi FM** | **Dholuo (Luo)** | Nilo-Saharan · Western Nilotic | Nyanza / western Kenya · ~4–5 M | RMS |
| 5 | **Mulembe FM** | **Luhya (Luhyia cluster · Luyia macro-dialect)** | Bantu · Great Lakes | Western Kenya · ~5 M · **NB: Luhya is a macro-family of 14+ sub-dialects → ASR-benchmark noisy** | RMS |
| 6 | **Musyi FM** | **Kamba (Kikamba)** | Bantu · Central Kenya | Eastern (Machakos, Kitui, Makueni) · ~4 M | RMS |
| 7 | **Chamgei FM** | **Kalenjin (Nandi / cluster)** | Nilo-Saharan · Southern Nilotic | Rift Valley · ~6 M cluster | RMS |
| 8 | **Egesa FM** | **Ekegusii (Kisii)** | Bantu · Great Lakes | South-western (Kisii, Nyamira) · ~2 M | RMS |
| 9 | **Bahari FM** | Swahili (coastal register) + some Mijikenda content | Bantu · Sabaki | Coastal (Mombasa, Kilifi, Kwale) | RMS |
| 10 | **Wimwaro FM** | **Kiembu (Embu + Mbeere)** | Bantu · Central Kenya | Embu county · ~0.6 M · *matches prior-session finding verbatim: "Wimwaro=Embu"* | RMS |
| 11 | **Muuga FM** | **Kimeru (Meru)** | Bantu · Central Kenya | Meru county + Tharaka-Nithi · ~2 M | RMS |
| 12 | **Sulwe FM** | **Bukusu (Luhya-Bukusu subdialect)** | Bantu · Great Lakes | Bungoma / Trans-Nzoia · ~1.5 M | RMS |
| 13 | **Vuuka FM** | Likely **Kuria** (western Kenya near Tanzanian border) — **NOT confirmed by RMS official site; two third-party directories name it but do not state the language explicitly** | Bantu · Great Lakes | Kuria (Migori) | RMS (third-party attribution) |
| 14 | **Bilitu FM** | Language not confirmed by any source found in this session | — | Western Kenya per directories | RMS (third-party attribution) |
| 15 | **Citizen TV** | English + Swahili (bilingual news) | — | National | RMS · TV brand |
| 16 | **Inooro TV** | Kikuyu | — | Mt Kenya + diaspora | RMS · TV brand |

**Two rows carry a UNKNOWN cell.** Ruling: keep them in the census as `language = UNKNOWN-PENDING-CONFIRM`; on first NAS reach, the top-level folder inventory will name what's actually on the drive. **Do not paper over.**

**Sources (this session):**
- `royalmedia.co.ke/radio/` (RMS official radio brand list — 13 brands)
- `royalmedia.co.ke/our-programming/` (RMS programming grid)
- `royalmedia.co.ke/brands/inooro-fm/` (Inooro brand page)
- `majira.co.ke/list-of-all-royal-media-stations-contacts-and-their-location/` (third-party directory, includes Vuuka + Bilitu)
- `whownskenya.com/leading-vernacular-radio-stations-owned-by-sk-macharia/` (third-party, vernacular list)
- `mediacouncil.or.ke/~mediaco7/sites/default/files/registers/radio-broadcasters-addresses.pdf` (Kenya Media Council register)
- `linkedin.com/company/royal-media-services-ltd` (RMS corporate LinkedIn)
- Population estimates: 2019 Kenya Population and Housing Census cross-referenced through the source pages above.

**Non-English speech-language shortlist (station × language × est. speaker base):**

| Station | Language | Family | Speakers |
|---|---|---|---:|
| Inooro FM | Kikuyu | Bantu-Central | ~7 M |
| Chamgei FM | Kalenjin | Nilo-Saharan-S-Nilotic | ~6 M cluster |
| Mulembe FM | Luhya cluster | Bantu-Great-Lakes | ~5 M (noisy — multi-dialect) |
| Ramogi FM | Dholuo | Nilo-Saharan-W-Nilotic | ~4–5 M |
| Musyi FM | Kamba | Bantu-Central | ~4 M |
| Muuga FM | Kimeru | Bantu-Central | ~2 M |
| Egesa FM | Ekegusii | Bantu-Great-Lakes | ~2 M |
| Sulwe FM | Bukusu | Bantu-Great-Lakes | ~1.5 M |
| Wimwaro FM | Kiembu | Bantu-Central | ~0.6 M |

Excluded from POC candidacy (English-carrying): Radio Citizen (Swahili+English mix), Hot 96 (English), Bahari FM (Swahili-dominant coastal), Citizen TV (bilingual), Inooro TV (Kikuyu-video, duplicates Inooro FM's language line).

---

## V · Governance / legal scan for SELLING the corpus (owner scoping item 5)

Three distinct legal / governance layers. Owner's Ruling #2 clears layer 1; layers 2 and 3 remain OPEN.

### V.1 · Copyright of broadcasts (Kenya Copyright Act, Cap 130 · consolidated per `new.kenyalaw.org/akn/ke/act/2001/12/eng@2022-12-31`)

- **Owner Ruling #2 — CLOSED.** Owner asserts "yes - full rights" to the off-air recordings for building and selling the corpus. This banks the copyright chokepoint as CLEARED-BY-OWNER-DECLARATION.
- **Nuance preserved (owner's own words):** rights-clearance is for the SOUND-RECORDING copyright layer only. It does not by itself resolve the biometric or named-individual layers (V.2, V.3).
- **Practical: encode as `licence_class:owner_full_rights` on every corpus artifact via the existing `a2_license_class.py` module.** No new mechanism.

### V.2 · Voice = biometric = sensitive personal data (Kenya Data Protection Act, 2019 · Act No. 24 of 2019 · `new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31`)

**Voice recognition is CLASSIFIED AS BIOMETRIC DATA under KDPA** — biometric data is "personal data resulting from specific technical processing based on the physical, physiological or behavioural characterisation of a natural person" (KDPA §2 interpretation, referenced by ODPC Draft Guidance on Biometric Data 2025). Biometric data sits in the KDPA §44 sensitive-personal-data category (health, sex-life, race, biometric, genetic, etc.).

**Processing conditions (KDPA §45 + ODPC guidance):**
1. **Lawful basis** — explicit, unequivocal, free, informed consent unless another lawful basis (contract, legal obligation, vital interest, public interest, legitimate interest) clearly applies.
2. **Indirect collection notification** — where biometric data is collected indirectly (broadcast recording = the data subject did not hand it over), the controller must notify the data subject within **14 days** (Data Protection General Regulations 2021 · §17 · via ODPC PDF).
3. **DPIA (Data Protection Impact Assessment)** — mandatory when processing is high-risk or at scale. A corpus census over 16 stations × 24/7 recordings, sold to a foreign research lab, is textbook high-risk-and-scale.
4. **Purpose limitation** — the sale purpose must be specific; expanded purposes require re-consent.
5. **Data-subject rights** — access, rectification, erasure, portability. Non-negotiable.
6. **Third-party disclosure** — the lab is a third party; disclosure requires either (a) fresh consent naming the lab, or (b) a data-sharing agreement + adequacy / SCC-equivalent for cross-border transfer (ODPC has SCC templates as of 2024).

**Standing enforcement in the estate:**
- Ties directly to the owner's **OPEN NAMED-PEOPLE RULING** (banked in `DECISIONS.md` — the open question is whether identifiable-natural-person artifacts leave the estate at all).
- Ties to the **DAP R-6 (pricing)** and **R-7 (disclosure budget)** rulings — the corpus sale is the archetypal DAP disclosure event; its budget must exist before the sale executes.

**Chokepoint surface:** Shield / Train's release_gate. Add a KDPA-verdict field to every biometric-affected artifact: `kdpa_verdict ∈ {PENDING, ADMISSIBLE_UNDER_CONSENT, ADMISSIBLE_UNDER_LEGITIMATE_INTEREST, ADMISSIBLE_UNDER_DPIA_APPROVED, REFUSED}`. Default PENDING. Release-to-DAP refuses on PENDING or REFUSED. **This is Ruling #5's mechanical enforcement.**

### V.3 · Named individuals + persons-of-interest (Constitution of Kenya 2010 §31 right to privacy + KDPA + defamation common law)

**Beyond biometrics**, identifiable natural persons named in broadcast content (politicians, callers, victims, minors, court-anonymised subjects) carry their own consent + right-to-privacy layers. This is what the owner's OPEN NAMED-PEOPLE RULING is about.

**Content classes to flag from ASR + diarization output:**
- Named minors (any name of a person under 18) — Children Act 2022 §54 hard prohibition on unauthorised commercial use.
- Politicians / public officials in personal (not public-function) speech.
- Callers-in on live phone-in segments — implicit consent for the broadcast, no implied consent for corpus sale.
- Court-related content — sub judice / anonymisation obligations under Judiciary Recording Rules.
- Health / religion / sexual orientation mentions tied to a named individual — KDPA §44 sensitive category cross-tag.

**Chokepoint surface:** the same Shield / Train release_gate, tagged `named_persons_verdict ∈ {PENDING, DE_IDENTIFIED_PASS, REDACTED_PASS, REFUSED}`. Ties to `refusal_family_registry` (`memory_refusal_reasons.v0.json`) for the "person identifiable — release refused" refusal class.

### V.4 · Foreign transfer + research-use carve-outs

- KDPA §48 cross-border transfer requires: (a) adequacy decision, (b) appropriate safeguards (SCCs), (c) explicit consent for the transfer, (d) transfer for the establishment / defence of legal claims. A research lab overseas needs (a) or (b) or (c).
- KDPA §51 permits processing for **historical, statistical, scientific or research purposes** without individual consent under strict conditions (data minimisation, no decisions targeting specific individuals, security safeguards). This is the most likely lawful-basis surface for a corpus sale — but ODPC guidance is that it does NOT extend to commercial-sale-without-research-carve-out; the research purpose must be genuine and documented.
- Owner Ruling #5 is where this collapses into a single verdict.

### V.5 · Governance chokepoint list (Ruling #5 enforcement surface)

| # | Chokepoint | Surface | Mechanism | Default state |
|---:|---|---|---|---|
| 1 | Copyright of the sound recording | Extraction-Akki `a2_license_class.py` | `licence_class:owner_full_rights` per Ruling #2 | **CLEARED** |
| 2 | Voice biometric — KDPA sensitive-category | Shield/Train release_gate | `kdpa_verdict:PENDING` on every biometric-affected artifact | PENDING (Ruling #5) |
| 3 | Named individuals — privacy + special categories (minors, court, health) | Shield/Train release_gate | `named_persons_verdict:PENDING` | PENDING (Ruling #5 + OPEN NAMED-PEOPLE RULING) |
| 4 | Cross-border transfer to lab | DAP | `transfer_basis:PENDING` (§48 vs §51 research carve-out) | PENDING |
| 5 | Purpose-limitation compliance (corpus-sale vs research) | DAP purpose gate (existing) | `disclosure_budget:{R-7 value}` | PENDING |
| 6 | Pricing surface | DAP R-6 | Owner's R-6 pricing schedule | PENDING |
| 7 | Music / non-speech material in the sale | Extraction-Akki VAD content-type index | Owner's brief said "music-free speech corpus" → filter at CP5 of POC; music spans stay in the census as detection signals, never in the release bundle | ENFORCEABLE BY CONSTRUCTION |

**Chokepoint 1 is the only one Ruling #2 clears. The other six remain open — each maps to a specific surface where the ruling lands.**

---

## VI · GPU idleness confirmation (owner Ruling #6)

Live SSH probe **2026-09-12T12:10:52Z (`akki-vm`) + 12:10:55Z (`akki-vm-ii`)**, both hosts, both cards:

| Host | Uptime | Card 0 util / mem | Card 1 util / mem | Trainer processes | Last training run |
|---|---|---|---|---|---|
| `akki-vm` | 15 days · load 0.03 0.02 0.00 | **0% / 0 MiB** | **0% / 0 MiB** | `on_host_queue_dispatcher.py` idle-polling (gpu-id 1) · no active trainer | shield-train-campaign-a-v21-A-3-7B-s5 · **2026-09-09 02:13Z** (76 h old) |
| `akki-vm-ii` | 15 days · load 0.09 0.05 0.00 | **0% / 0 MiB** | **0% / 0 MiB** | `queue_followon_launcher.py` + `on_host_queue_dispatcher.py` idle-polling · no active trainer | shield-train-campaign-b-v21-B-REF-3B-s7 · **2026-09-08 23:55Z** (78 h old) |

**Verdict: BOTH HOSTS IDLE. 4 × H200 at 0% / 0 MiB. Marginal $0 on Cassava lease.** POC compute budget requirement satisfied. Idle dispatchers are the correct posture (adoption discipline from `W-Orchestrator-Resilience-r2` remains in force — a new campaign attaches without disturbing the dispatchers).

---

## VII · Proposed 3 stations for POC (Ruling #3)

**Proposal: Inooro FM · Ramogi FM · Musyi FM.**

Rationale (from §IV):
- **Inooro FM (Kikuyu · Bantu-Central · ~7 M speakers).** Highest speaker-base non-English language in the estate. Owner's default proposal named it — accepted.
- **Ramogi FM (Dholuo · Nilo-Saharan Western-Nilotic · ~4–5 M).** Owner named it. Deliberately different language FAMILY from Kikuyu (Nilo-Saharan vs Bantu) — falsifies "the ASR works on Bantu but fails everywhere else" without needing a fourth station.
- **Musyi FM (Kamba · Bantu-Central · ~4 M)** **rather than Mulembe FM (Luhya)**. Two reasons:
  - **Rationale (a):** Luhya is a 14+ sub-dialect macro-family; Mulembe FM's programming mixes them. Cleaner ASR benchmarking on the POC with a SINGLE-LANGUAGE station (Musyi = Kamba only). Mulembe's dialect-noise will be present at scale but is not what the POC should demonstrate first.
  - **Rationale (b):** Musyi keeps THREE distinct geographic regions in the sample — Mt Kenya (Inooro), Nyanza (Ramogi), Eastern (Musyi). Mulembe repeats the western-Kenya region already sampled by Ramogi.

**One acknowledged pending: station-name-vs-folder-name confirmation.** The exact 16-station list on the NAS is set by the folder names on `10.10.55.55:5000`, which we cannot read yet (§I). If the NAS folder names disagree with the RMS brand list (e.g. one is "Inooro-2025-Q3-archive" rather than "Inooro FM"), the mapping stands and the folder-name is the override. **Confirm at CP2 of the POC wave, first live-probe on the NAS.**

---

## VIII · Proposed POC wave (paper only, tests-first, subject to owner confirmation)

**Wave name:** `W-AUDIO-POC-3-STATIONS`
**Class:** M (multi-CP, multi-file, but no new engine — all extensions of `services/perception/` + `services/mtafiti/` + `services/shield_train/` on `programme/track-a`)
**Ratchet floor at wave open:** 3251 (untouched during scoping).
**Discipline:** identical to `W-MTAFITI-GPU-DISCOVERY` — mechanical RED → smallest kernel → double-green BASELINE_GUARD=1 byte-match → two-commit local no-push → terminal pytest only → no testing_agent → grounding brief with verbatim owner-ruling quotes in §A.

### VIII.1 · Wave-honest-limits (declared at wave open)

- No fixture for `pyannote.audio` diarization end-to-end unless HF token lands in `backend/.env`; construction test proves the ProviderUnavailable message; real diarization is CP5.
- No language-ID module exists yet; a small module lands at CP3 wrapping `faster_whisper` auto-detection + a fallback (optional `langid.py` or `whisper.detect_language`).
- No `demucs` / source-separation. Music/speech split at CP4 uses the Silero VAD content-type index (`music \| speech \| ad \| ...`) — coarse, no vocal isolation. Fine-grained separation deferred.
- No named-entity redaction. Named-persons detection runs at CP6 via a NER pass on the ASR transcript, but redaction is NOT applied — only tagged for the release_gate.
- Cross-recording speaker-identity linking (same-person-in-two-broadcasts) is NOT in the POC. Only within-recording diarization.
- 3 stations only, not 16. Extending to 16 is a follow-on wave.

### VIII.2 · CP breakdown (tests-first, one CP = one mechanical RED + one double-green close)

| CP | Landing | Track-a scope | New invariants (est.) |
|---:|---|---|---:|
| CP0 | Grounding brief authored + station selection ratified by owner. No code. | `notes/wave_audio_poc_3_stations_grounding_brief.md` + `notes/wave_audio_poc_3_stations_station_selection.md` | 0 |
| CP1 | **Governance walls.** Three primitives: (a) `readonly_media_guard.py` — refuses any Synology FileStation API call outside `List / Read / Status / DownloadToHSS`; multi-call refused. (b) `release_gate.py` under `shield_train/` — `admit_release(artifact, tier)` refuses `biometric_embedding \| named_identity \| speaker_labeled_audio` tiers by default; four release-verdict fields per artifact: `kdpa_verdict`, `named_persons_verdict`, `transfer_basis`, `licence_class`. (c) `MtafitiObjectiveCarrier` reuse — POC objective originates in TARGETA, refused by construction if mtafiti-internal. | +40 to +60 |
| CP2 | **NAS reachability preflight + composition census.** Prerequisite: NAS network path is opened (owner action per §I). On reach, list stations (top-level folders), read file inventory for the 3 selected stations only — duration + format + sample rate + bitrate + filesize + sha256, no bytes moved off-NAS. Cost receipt banked. `MediaComposition` DetectionSignals emitted per file. | +20 to +30 |
| CP3 | **Single-file end-to-end dry-run.** One representative file per station (3 files total) staged to HSS on `akki-vm`. Full pipeline: demux → segmentation → VAD → language-ID (auto-detect via faster-whisper) → ASR (whisper-multilingual model, not `tiny` — a POC production choice, model registry updated) → diarization (pyannote local · HF token confirmed present in .env). Every stage emits a receipt. `synthetic_plumbing_only=False` for the first time. If diarization fails (no HF token / no library), CP3 lands anyway with a right-reason RED on the diarization test → CP3.1 unblocks it. | +25 to +40 |
| CP4 | **Music / speech split + language-ID at slice scale.** ~10 hours per station (30 hours total) through VAD's content-type index; language-ID per speech-span; segregate English spans from non-English spans (Ruling #4 · non-English is what the lab wants). Emit `LanguageIdSignal` DetectionSignals per span. No English content deleted — kept in the estate as `english_content:True` flagged, never released. | +15 to +25 |
| CP5 | **ASR + diarization + speaker biometric embeddings on the non-English speech slice.** Non-English spans only. ASR transcript per span (multilingual whisper). Diarization per file. **Speaker embeddings via `pyannote.audio.EmbeddingModel`** (added dependency at CP1, admitted here). Every biometric artifact carries `release_gate:PENDING`. GPU utilization telemetry to `phase0/audio_poc/gpu_receipts/`. | +30 to +50 |
| CP6 | **Quality profile + non-English segregation + NER for named persons + sample bundle.** Held-out slice sha256 banked BEFORE any downstream consumer sees a sample. NER over the ASR transcript (existing `services/perception/` NER capability OR added minimal spaCy multilingual pass at this CP). Named-persons detection tagged as `named_persons_verdict:PENDING` — no auto-redaction. Sample bundle sha256-chained. | +20 to +30 |
| CP7 | **Wave close.** Wave-close doc analogous to `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md`: Progress + Findings + Decisions taken + Discoveries + Cost + Honest limits + Recommendations. Quality bar identical: 5-section owner-facing plain-language report; ratchet history appended; wave-close bundle sha256 sealed. | +10 to +20 |

**Wave total invariant estimate: +160 to +255 (ratchet 3251 → ~3410–3505).**

### VIII.3 · Cost estimate (Cassava lease basis, NAS reads local-network)

| Line | Estimate |
|---|---|
| GPU-hours (H200 · 3 stations × ~10 hrs audio × whisper-multilingual + pyannote + embeddings) | ~8–16 GPU-hours across both hosts · Cassava lease **$0 marginal** |
| Egress (NAS → HSS, if HSS is on-premise or cross-region-Huawei — TBD by sysadmin) | 30 hrs × 16 kHz × mono × PCM float32 ≈ 3.4 GB per station × 3 stations ≈ **~10.3 GB one-time**; if egress metered at ~$0.10/GB, ≈ **~$1.05**; if intra-Nairobi zero-egress, **$0** |
| Pod compute | free (pod is orchestrator-only) |
| **Total** | **$0 to ~$1** |

### VIII.4 · Sequencing / stop conditions

- **CP0 lands only after owner confirms the 3 stations** (this document is the trigger).
- **CP1 lands only after CP0** and re-verifies GPU idleness at wave-open.
- **CP2 lands only after NAS reachability is resolved** (owner-side + sysadmin — potentially a Nairobi bastion analogous to §3.A of `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`).
- **CP5 lands only if** `pyannote.audio` + `HUGGINGFACE_HUB_TOKEN` are both present in the estate (CP1 verifies).
- **Any release from the release_gate lands only after** the owner's Ruling #5 arrives with a `kdpa_verdict` + `named_persons_verdict` + `transfer_basis` + DAP R-6/R-7 bindings.
- **Ratchet floor 3251** stays untouched during CP0. From CP1 onward, ratchet bumps monotonically per double-green.

---

## IX · Artefacts of this scoping task (local, uncommitted at time of writing, banked to `master` at commit close)

- `notes/W_AUDIO_POC_SCOPING_20260912.md` — this document.
- `STATE/DECISIONS.md` — owner Ruling appended verbatim (six-point addendum).
- No product code touched. No pytest invoked. No ratchet touched. No `testing_agent` invoked. No push.

**Guardrail attestation:** the 5 read-only probes above touched only network-reachability, existing repo-tree contents, and public web sources. Zero write to Extraction-Akki `programme/track-a`. Zero write to any remote system. Credentials remain 0600 / git-ignored / never echoed. Session transcript carries no biometric material, no audio bytes, no credential values.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
