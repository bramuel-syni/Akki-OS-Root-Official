READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-D12-POC · grounding brief

**Wave scope.** Single-CP wave (CP-D12P1) firing the transcription-pipe-proof on a bounded single-digit count of REAL NAS audio files. Model = `whisper-tiny` via `faster-whisper` (CTranslate2 backend). Execution on GPU host `akki-vm` (fallback `akki-vm-ii`). All outputs labeled `POC-NOT-PRODUCTION`. Release-gate admission explicitly DEFERRED per owner ratification 2026-09-15T~09:50Z (Option A).

**Owner directive · verbatim (DECISIONS 2026-09-15T~03:55Z Effect 6):**

> "=== D12 → APPROVED (owner 'yes') === After the census completes: run the transcription pipe-proof with the canon CI fixture (whisper-tiny + faster-whisper) on a SMALL BOUNDED set of real NAS files (single-digit count), on the GPU hosts, all outputs labeled POC-NOT-PRODUCTION in provenance, receipts banked. Production model selection still follows census activation per §A17.11 — the POC does not pre-empt it."

**Owner Option-A ratification · verbatim (DECISIONS 2026-09-15T~09:50Z):**

> "Option A — ratified. Proceed with the D12 POC now: bounded single-digit NAS files, GPU hosts, POC-NOT-PRODUCTION provenance, raw transcription receipts banked under phase0/d12_poc_receipts/, release-gate admission explicitly deferred. That matches the owner's literal directive — the POC proves the pipe (NAS bytes → GPU → transcription → receipts), and release admission was never on its critical path."

## §A · Anchors verbatim

**Canon-17-19 §A17.11** (production model selection binding · owner citation): activation of the production ASR model follows the census activation list. D12 POC does NOT pre-empt this — D12 outputs are POC-labelled.

**W-AUDIO-POC seal · CP-A5** (`phase0/output_verified_seals/audio_poc_v1.seal.txt`):
- Contract landed: `GapFillTranscript` (no-text field), `transcribe_gap` env-only, `write_gap_transcript_or_refuse` leak-guard-first + release-gate integration.
- **Blocker A (NAS-to-bytes plumbing)** — deferred; must be plumbed for D12.
- **Blocker C (release-gate PENDING R-7/R-15/R-16/R-17)** — RESOLVED this session (R-7 PILOT-OPEN + R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY ratified 2026-09-15T~03:55Z; discharged at CP-RG1..RG5).
- **Blocker D (audio-plane sensitivity declarations)** — NEW · owner-desk item banked at DECISIONS 2026-09-15T~09:50Z Effect 2 · gates *release admission*, NOT the POC pipe itself (per Option A).

**NAS access · TASK_CONNECTIVITY_REDO_ADMIN_GUIDED_CLOSE_20260914 :40** (verbatim state):
> `smb.synology_nas (10.10.55.55/445)` · **PASS** ← STATE CHANGE from prior HARD_GAP · JUMP-hosted `smbclient -L //10.10.55.55` returned 12 shares · Hidden share `OFFAIRRECS` tree-connects · 16 channel folders (`channel01..channel16`).

**Recorder pipe** (verbatim: line 40): `ActRecord.exe writing 300-sec chunks per channel per day`. So each audio file is a 300-second (5-minute) chunk. At typical estate WAV/MP3 rates this is a few MB per file.

**NAS credentials custody** (`/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx`, 3 sheets: "NAS creds" · "NAS Guide + Cred" · "Huawei Creds"). Extract via `openpyxl` in-memory only · NEVER echo to transcript · reference by shape only.

## §B · Pipe design (staged with observable receipts per stage)

**Stage 1 · NAS cred extraction (in pod · in-memory only).** `openpyxl` opens `RMS_Connection_Creds.xlsx`, reads the "NAS creds" sheet, extracts username + password + host into a local Python dict. Values NEVER stdout'd; only shape metadata printed (`sha256_of_creds_dict` · `field_names`). Custody-cat guard exercised on the extraction script text.

**Stage 2 · JUMP-side smbclient probe (verify NAS still reachable this session).** SSH from pod to JUMP host (bastion CSV `/app/backend/estate_keys/bastion/jump_server_radio_system.csv` · JUMP-root creds) · run `smbclient -L //10.10.55.55` as a fresh reachability confirmation · redacted receipt (share count only).

**Stage 3 · Enumerate ≤3 audio files from a single channel** (canonical channel `channel01` · today's date UTC · pick lexicographically-first 3 files matching the recording pattern `<YYYYMMDD>_<HHMM>_*.<ext>`). Parse via sealed CP-A2 `services/audio_poc/recording_inventory.py::parse_smbclient_ls_line` + `extract_canonical_key`. Receipt records the 3 canonical keys + size bytes (no filename bytes).

**Stage 4 · Fetch bounded bytes to pod local tmp.** `smbclient //10.10.55.55/OFFAIRRECS -c "get <path> <local-tmp>"` inside JUMP · scp back to pod under `/tmp/d12_poc/`. Bank sha256 of each downloaded file (bytes-integrity). Refuse if any file exceeds a bounded size cap (default 20 MB per file · SO §5 bounded-egress-cost discipline).

**Stage 5 · scp bytes → akki-vm.** ssh + scp (mode 0400 destination · `/tmp/d12_poc/`). Verify sha256 post-scp on GPU host side.

**Stage 6 · Install faster-whisper + fetch whisper-tiny model on akki-vm.** `pip install --user faster-whisper` (CTranslate2 backend) via SSH. Trigger model download by importing `WhisperModel("tiny", compute_type="int8")`. Model persists in HuggingFace cache on GPU host. Post-D12, this cache is reusable.

**Stage 7 · Transcribe bounded set on akki-vm GPU.** Run one script per file: `WhisperModel.transcribe(file_path, beam_size=1)` · capture segments · compute wall-clock. **Do NOT emit transcript text to stdout**. Emit only receipt shape:

```json
{
  "poc_flag": "POC-NOT-PRODUCTION",
  "input_canonical_key": {"station": "...", "date_utc": "...", "slot": "...", "filename_stem": "..."},
  "input_sha256": "<64hex>",
  "input_bytes": <int>,
  "model_id": "faster-whisper:tiny",
  "model_version": "ctranslate2",
  "compute_type": "int8",
  "beam_size": 1,
  "wall_clock_seconds": <float>,
  "segment_count": <int>,
  "word_count_approx": <int>,
  "language_hint": "<iso>",
  "avg_confidence": <float>,
  "gpu_host": "akki-vm",
  "gpu_model": "NVIDIA H200",
  "provenance_note": "raw transcript body NEVER emitted · release-gate admission deferred per owner Option-A 2026-09-15T~09:50Z"
}
```

**Stage 8 · Receipts banked under `phase0/d12_poc_receipts/<yyyymmddThhmmssZ>_<canonical_key_short>.json`** (pod-side).

## §C · Invariants (target ratchet 4062 → ~4068..4072, single CP)

D12 POC ratchets on RECEIPT SHAPE, not on live-run success. The invariants freeze the *contract* the POC receipts must satisfy; the live-run itself is a wave-close artefact and may bank a specific blocker without derailing ratchet.

1. **module_fabric_present** — imports; exports `assemble_d12_poc_receipt`, `POC_NOT_PRODUCTION_FLAG`, `D12_MODEL_ID`, `D12_MODEL_VERSION`, `D12_COMPUTE_TYPE`, `D12_BEAM_SIZE`.
2. **POC_NOT_PRODUCTION_FLAG_is_canonical_token** — byte-identical string `"POC-NOT-PRODUCTION"`; matches owner directive verbatim.
3. **D12_MODEL_ID_D12_MODEL_VERSION_D12_COMPUTE_TYPE_D12_BEAM_SIZE_canonical_tokens** — `"faster-whisper:tiny"` · `"ctranslate2"` · `"int8"` · `1`.
4. **assemble_d12_poc_receipt_frozen_carrier_shape** — every produced receipt dict has exact key-set + type shape (all shape keys enumerated · silent renames fire).
5. **assemble_d12_poc_receipt_never_carries_transcript_text_field** — inspect the returned dict + a serialized JSON; no field named `text/transcript/segments_text/utterance_text/body/content` may appear; assert the field-name set is a strict subset of the canonical enumerated shape.
6. **assemble_d12_poc_receipt_stamps_poc_flag_regardless_of_success** — even on error path, the receipt structure carries `poc_flag = "POC-NOT-PRODUCTION"` in provenance (never elided under a partial-success shortcut).

## §D · Cross-benefit expectation

None expected. Module lives under `services/d12_poc/`; contracts unchanged; NON_CONTRACT_UTILITY_MODULES scope unchanged.

## §E · Wave-honest limits

* **E.1 · Live run is out-of-scope-for-ratchet.** The invariants freeze the RECEIPT CONTRACT (shape · no-text-field guarantee · POC flag). Whether the live run completes end-to-end this session or banks a specific blocker (NAS auth · faster-whisper install egress · whisper-tiny model fetch egress · GPU-side smbclient absence) is a WAVE-CLOSE outcome, not a CP-close outcome.
* **E.2 · No release-gate composition on D12 outputs.** `admit_transcript_release_pilot_open` is NOT called by D12 · outputs bank raw as `POC-NOT-PRODUCTION` under `phase0/d12_poc_receipts/` per owner Option-A verbatim.
* **E.3 · No transcript text emission.** The receipt shape enumerates fields WITHOUT any text/segments-content field. Invariant 5 freezes this. Any future D12 caller that needs actual transcript text must land a separate release-gate composition first (blocked on Effect 2 audio-plane sensitivity declarations).
* **E.4 · Bounded size cap.** Individual files > 20 MB refused (`FileTooLargeForPoc`) to preserve SO §5 bounded-egress-cost discipline. Owner may override; default is bounded.
* **E.5 · GPU-host state discovery** happens live at wave open. Findings: faster-whisper NOT pre-installed on akki-vm (probe at 09:52Z UTC · ModuleNotFoundError) · nvidia-smi confirms 2× H200 · Python 3.12.3 · NAS `10.10.55.55:445` NOT reachable directly from akki-vm (TCP timeout · GPU host on a different subnet) · smbclient NOT installed on akki-vm.

## §F · Commit protocol

* **Commit A (code · `programme/track-a` in `repos/Extraction-Akki`):** test file + receipt-assembler module + baseline_failures.json ratchet bump.
* **Commit B (state · `master`):** grounding brief + wave-close note + seal + NEXT.md refresh + DECISIONS.md entry + per-receipt banked artifacts under `phase0/d12_poc_receipts/`.

## §G · Boundary hygiene retries

Per owner directive (b) — retry CD+Visitors probe at every CP boundary while egress open. This wave has one CP boundary (CP-D12P1 seal). One probe fires there; PASS-verdicts fold into census scope; FAIL-verdicts continue the standing retry loop.

## §H · SEC-2026-09-15-08 corrective landing note

New agent-side leak class identified this wave-open (CSV-header-emit via python print pattern). Filed in SEC ledger. Standing Rule 4 banked. M8 W-TESTS-FIRST-GUARD-INVARIANT gets a scope extension for the same class (part-B, deferred). This grounding brief authored under the new discipline: NEVER `next(csv.reader(open(<custody_path>)))` + print — only `readline() + shape-only` when file kind is credential/token.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
