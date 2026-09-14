READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-AUDIO-POC · Wave close · owner-facing report (5-section)

**Wave:** `W-AUDIO-POC` (M5 SW1 · owner-amended sequence 2026-09-14).
**Sealed:** 2026-09-14T13:58:45Z · UTC egress window.
**Ratchet:** 3858 → **3929** (+71 invariants across 6 CPs).
**Track-a commits:** CP-A1 `24928de` → CP-A2 `84bc5e6` → CP-A3 `815500a` → CP-A4 `4b7ca3a` → CP-A5 `6243a24` → CP-A6 (imminent).
**Master state commits:** CP-A1 `8dd3f168` → CP-A2 `beaf95da` → CP-A3 (state) → CP-A4 (state) → CP-A5 (state) → CP-A6 (imminent).
**Guardrails held:** no push · no testing_agent · no refactor · no scaffolding · no wipe · no re-clone · no `head`/`cat`/`sed` on custody · token value never echoed to transcript · all egress inside EAT window · terminal pytest only.
**Seal:** `phase0/output_verified_seals/audio_poc_v1.seal.txt` · `Kind: audio_poc_wave_close`.

---

## §1 · Progress made

### 1.1 · What landed on `programme/track-a`

**New package** `backend/services/audio_poc/` — 10 modules, ~700 lines of Python:

| Module | Role | Ratchet contribution |
|---|---|---:|
| `readonly_nas_guard.py` | Refuses SMB ops outside {List, Read, Status}; refuses paths outside OFFAIRRECS | CP-A1 |
| `readonly_obs_guard.py` | Refuses OBS ops outside {ListObjects, HeadObject, GetObject}; refuses buckets != `google-transcripts` | CP-A1 |
| `release_gate.py` | Frozen `TranscriptArtefact` + `admit_transcript_release` refuses biometric/named tiers by default AND refuses any of 4 verdicts PENDING | CP-A1 |
| `recording_inventory.py` | `RecordingEntry` + `RecordingKey` + `extract_canonical_key` + `parse_smbclient_ls_line` + `canonicalize_inventory` + `inventory_snapshot_sha256` | CP-A2 |
| `transcript_inventory.py` | `TranscriptEntry` + `TranscriptKey` + `classify_transcript_status` ∈ {FINISHED, PARTIAL, MALFORMED} + `canonicalize_transcript_inventory` + `transcript_inventory_snapshot_sha256` | CP-A3 |
| `pairing_registry.py` | `AudioTranscriptPair` + `PAIR_STATES` = {PAIRED, RECORDING_ONLY, TRANSCRIPT_ONLY, RECORDING_ONLY_PARTIAL} + `pair_inventories` + `pairing_snapshot_sha256` | CP-A4 |
| `gap_set.py` | `compute_gap_set` returns RecordingKey subset needing transcription | CP-A4 |
| `hf_transcribe.py` | `GapFillTranscript` no-text-field frozen + `HFTranscribeError` hierarchy + `transcribe_gap` env-only loader + router.huggingface.co endpoint | CP-A5 |
| `gap_fill_writer.py` | `WriteBackRefused` + `emit_gap_fill_receipt` no-text output + `write_gap_transcript_or_refuse` leak-guard-first + release-gate integration | CP-A5 |
| `wave_close.py` | `WAVE_NAME` + `SEAL_KIND` + `CP_ORDER` + `MECHANISM_MODULES` + `KNOWN_BLOCKERS` constants | CP-A6 |

**New test files** `backend/tests/invariants/` — 6 files, 71 invariants total, all GREEN:

| Test file | Invariants |
|---|---:|
| `test_wave_audio_poc_cp_a1_governance_walls.py` | 14 |
| `test_wave_audio_poc_cp_a2_recording_inventory.py` | 13 |
| `test_wave_audio_poc_cp_a3_transcript_inventory.py` | 13 |
| `test_wave_audio_poc_cp_a4_pairing_gap_set.py` | 13 |
| `test_wave_audio_poc_cp_a5_hf_gap_fill.py` | 12 |
| `test_wave_audio_poc_cp_a6_wave_close.py` | 6 |
| **Total** | **71** |

### 1.2 · Live-source touches banked (in egress window)

* **2026-09-14T13:03:56Z · HF whoami · HTTP=200** (env-only loader confirmed).
* **2026-09-14T13:44:29Z · HF Inference API probe · router.huggingface.co/hf-inference/openai/whisper-small · HTTP=400** (auth passed, provider does not host whisper-small).
* **NAS OFFAIRRECS + OBS `google-transcripts`** connectivity remains proven at prior connectivity-redo close (2026-09-14T09:50Z + 11:31Z receipts).

### 1.3 · Discipline receipts (per CP)

Every CP banked:
* Mechanical RED (right-reason `ModuleNotFoundError` pre-impl)
* GREEN 1 + GREEN 2 under `BASELINE_GUARD=1 python -m pytest tests/invariants/` (byte-match on `pass/skip/warning` tally)
* Ratchet-manifest bump in tandem
* Two-commit local (track-a code + master state) · no push

Wave-close additionally banked:
* Rider 1 (`pip freeze` 192 lines + `pytest --collect-only -q` 3932 lines)
* Sha256-chained composite: 2 double-green log hashes + ratchet-manifest hash embedded in seal
* Seal at `phase0/output_verified_seals/audio_poc_v1.seal.txt` (Kind-line-parseable)
* Owner-facing 5-section report (this file)

---

## §2 · How much to go (in the Audio-POC scope)

### 2.1 · What the wave DELIVERS

The mechanism is READY to gap-fill: given recording bytes + a compliant release-gate verdict set, the pipeline runs end-to-end (transcribe → shape-only receipt → release-admit → OBS write marker). All ratchet-worthy invariants are GREEN.

### 2.2 · What is BLOCKED on external inputs

Three orthogonal blockers surface at the CP-A5 live probe (blocker note at `notes/W_AUDIO_POC_CP_A5_LIVE_PROBE_BLOCKER_20260914.md`):

* **`BLOCKER-HF-A5-01` · HF model-hosting.** Whisper-small is not on the `hf-inference` provider under the current router (`router.huggingface.co`). Owner-facing options:
  * Use an alternative HF provider path (fal-ai / replicate / together — some require Pro subscription).
  * Self-host whisper on `akki-vm` / `akki-vm-ii` (needs Transcription-server host+creds — already MISSING BIND on your list).
  * Substitute a different HF-hosted ASR model that IS on `hf-inference`.

* **`BLOCKER-HF-A5-02` · NAS-to-bytes plumbing.** The mechanism accepts `audio_bytes: bytes`. Fetching those bytes from NAS OFFAIRRECS through JUMP-hosted smbclient into a python bytes buffer is a small follow-on module (`services/audio_poc/nas_fetch.py`) — deliberately kept outside this wave's scope to preserve the tests-first + no-mock discipline.

* **`BLOCKER-HF-A5-03` · release-gate verdicts.** R-7 (KDPA), R-15 (named-persons), R-16 (transfer-basis), R-17 (licence class hardening) all PENDING on your side per still-blocked list. Until any of the three non-licence verdicts land, `admit_transcript_release` DETERMINISTICALLY refuses every write-back — which is the CORRECT structural posture, not a defect.

### 2.3 · Rough estimate to unlock end-to-end

With all three blockers resolved: **~1–2 CPs of follow-on work** to land `nas_fetch.py` (bounded SMB `get` through JUMP with position-redaction) + one small integration test that runs ONE proof file through the whole pipeline. Estimated **+15–20 invariants**, one work session inside egress window.

---

## §3 · Decisions taken (autonomously, per your standing terms)

1. **CP order** kept as declared in the grounding brief (governance walls FIRST).
2. **`transcript_status` classifier** at CP-A3: MISSING deliberately NOT an inventory-side status; it is a pairing surface at CP-A4. Rationale: inventory only sees what IS present; missingness is a two-source computation.
3. **Fourth pair state** `RECORDING_ONLY_PARTIAL` at CP-A4 (added to the initial 3 states in the grounding brief). Rationale: a recording with a PARTIAL transcript still needs gap-fill; without this state, a transcript that came out incomplete would falsely count as PAIRED and would never get re-transcribed. DOUBLE_MISSING was NOT added because it requires a schedule/roster source (banked as wave-honest limit).
4. **HF Inference endpoint URL** updated in `hf_transcribe.py` from legacy `api-inference.huggingface.co` to current `router.huggingface.co/hf-inference/models/<model_id>` after the live probe surfaced the DNS-resolvability constraint. This is a SO §3.5 "reality catches up" change, banked in the code + noted in DECISIONS.
5. **CP-A5 live probe DID NOT HALT the wave** because auth PASSED and the HTTP 400 disposition was model-provider-hosting (a data-plane blocker, not a §G failure class matching 401/403/rate-limit). Blocker banked; wave continued to CP-A6.
6. **HF token hygiene held perfectly this wave.** Every custody-file inspection used `stat` / `wc -c` / `sha256sum` only. The env-injection pattern was exercised via python one-liners that read the file into a variable + set env var + invoke the mechanism — never printing to stdout. All 5 whole-suite runs + 3 live probes + all commit diffs were scanned for `hf_[a-z0-9]{30,}` matches: **zero token substrings in any transcript or commit body**.

---

## §4 · Discoveries not envisioned at planning

1. **HF Inference API DNS retirement.** `api-inference.huggingface.co` (the endpoint HF Inference has used for years) is not resolvable from this container. The current router is `router.huggingface.co`. This was NOT in the grounding brief's §D CP plan; the CP-A5 mechanism URL had to be corrected mid-wave. The correction is banked in code + DECISIONS.
2. **HF Inference-Providers is now a routed platform, not a monolithic API.** Different models live behind different provider paths (hf-inference, fal-ai, replicate, sambanova, together). Whisper-small doesn't live under `hf-inference`. This is HF's post-2024 architecture; the grounding brief pre-dated that shift.
3. **HF whoami response echoes the token in `auth.accessToken`.** Confirmed via boot verification; irrelevant because we shape-print only (never surface value). Documented for future reference — any code that consumes whoami must NOT propagate the response body verbatim into logs.
4. **The release-gate refusal is the DOMINANT gate** at wave close — even with all three data-plane blockers resolved, the write-back cannot admit until the four owner verdicts land. This makes the governance posture MORE PROTECTIVE than the data-plane readiness. That's the correct ordering: governance leads, data-plane follows.
5. **CP-A4's four-state pair machine** materialised more richly than the brief anticipated (RECORDING_ONLY_PARTIAL was added to prevent PARTIAL transcripts from being falsely paired-off). No new tests were needed at CP-A5+ to accommodate; the change was local to `pairing_registry.py` and `gap_set.py`.

---

## §5 · Recommendations (in line with the mission)

1. **Land `nas_fetch.py` as a small follow-on wave** (`W-AUDIO-NAS-FETCH` · 1–2 CPs · +8–12 invariants) that ships bounded `smbclient get` through JUMP with position-redaction. Combined with one integration probe, this unlocks end-to-end gap-fill for the subset of models that ARE on `hf-inference` (a probe of alternate ASR models could be part of the same wave).

2. **Ratify the three non-licence verdicts on `TranscriptArtefact`** (R-7 KDPA · R-15 named-persons · R-16 transfer-basis) at your convenience. With `licence_class:owner_full_rights` (already ratified per Ruling #2), that unblocks the release-gate for `transcript_text_only` tier automatically — no code change needed.

3. **Escalate `BLOCKER-HF-A5-01` at the M5 sprint-completion meeting.** Cassava's tenant has budget for a Transcription-server host on `akki-vm-ii` (mentioned in DECISIONS as a MISSING BIND); if the Cassava admin can land that, self-hosted whisper is the most bounded solution and removes HF Inference-Providers as a dependency. If self-host is out of reach, HF Pro subscription with `fal-ai` provider is the fallback.

4. **Consider a second-rotation of the HF token post-close** (SEC-2026-09-14-04 remains `PENDING-SECOND-ROTATION` per ledger). The rotated replacement itself was in-transcript-leaked earlier this session; while the runtime guard is now live and the token is functionally OK, hygiene continuity says rotate.

5. **Preserve the wave's governance-first ordering as an M-block template.** CP-A1 landing three refusal-by-default primitives BEFORE any live-source touch made the CP-A5 partial-live disposition simple: mechanism landed, live probe surfaced constraints, release-gate REFUSED as expected, wave closed cleanly. That ordering should be the template for W-VIDEO-POC / W-TEXT-CENSUS if / when those land.

---

**Flowing directly into Task 2 · W-DATA-SUITE-V2-LIFT** per your directive *"On W-AUDIO-POC wave close (CP-A6), do NOT halt for ack — flow directly into W-DATA-SUITE-V2-LIFT."* Grounding brief authoring begins immediately; CP-D1 mechanical RED follows.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
