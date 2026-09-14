READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-A5 · Live HF Inference API probe · blocker note · 2026-09-14T~13:44Z

**Wave:** `W-AUDIO-POC`
**CP:** CP-A5 · HF-model gap-fill transcription
**Blocker class:** §G row 3 · HF Inference API constraint (model-provider hosting), NOT auth
**Owner directive that governs this note (verbatim):** *"If NAS/OBS/HF connectivity fails or the egress window blocks you, do NOT mock anything. Record the blocker in a decision-point note and move to Task 2 while flagging the blocker back to me."*

---

## 1. What was probed

Live HF Inference API probe with a synthetic 32,044-byte 1-second 16 kHz mono silence WAV, env-injected active token (SHA256-pinned per `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md`), against the CP-A5 mechanism's default model `openai/whisper-small`.

**Probe timestamp (UTC):** 2026-09-14T13:44:29Z (in egress window · UTC ~13:44 · policy 08:00–02:00 UTC).
**Receipt:** `phase0/audio_poc/20260914T134429Z_cp_a5_live_hf_inference_probe.log` (283 B).

## 2. Findings

| # | Endpoint | Outcome | Interpretation |
|---:|---|---|---|
| 1 | `https://huggingface.co/api/whoami-v2` | HTTP=200 (boot verification) | Auth active, account confirmed |
| 2 | `https://api-inference.huggingface.co/...` | `URLError · Name or service not known` | Legacy DNS not resolvable from this container (egress policy blocks it, or HF has retired the DNS name) |
| 3 | `https://router.huggingface.co/` | HTTP=404 | Router DNS resolves; 404 is fine (root has no handler) |
| 4 | `https://router.huggingface.co/hf-inference/models/openai/whisper-small` | HTTP=400 · body `{"error":"Model not supported by provider hf-inference"}` | **AUTH PASSED** (not 401/403) · but whisper-small is NOT hosted on the `hf-inference` provider in current HF Inference-Providers setup |
| 5 | `https://serverless.huggingface.co/` | `URLError` | Not resolvable |

## 3. What this means (mapped to §G stop conditions)

* **§G row 3 (HF 401/403/rate-limit → HALT):** does NOT apply exactly — we did not get 401/403 or 429.  We got a **model-provider-hosting refusal** at HTTP 400.  Same disposition per owner directive: *"do NOT mock anything · record the blocker · move to Task 2."*
* **Auth is confirmed working** on the current router.  The blocker is NOT credential-side.
* **Not blocked on rotation:** the hardened rotated token (SHA `3ea89c94…19c5`) is fully active.  The pending second rotation (SEC-2026-09-14-04) is a separate hygiene concern, not a functional blocker for gap-fill.

## 4. Two orthogonal blockers on end-to-end gap-fill

Even if the HF-side model-hosting issue were resolved, end-to-end gap-fill would still be blocked by:

* **Blocker A (data-plane):** `NAS → bytes` fetcher.  This wave's mechanism accepts `audio_bytes: bytes` as an argument.  The plumbing that fetches ONE recording's bytes from NAS OFFAIRRECS through the JUMP-hosted smbclient into local memory is NOT landed this wave.  It is a follow-on scope: a small helper that runs `smbclient` with `-c 'get <path> <local-tmp>'` under `readonly_nas_guard` and streams bytes into a python bytes buffer.  Not started.

* **Blocker B (governance-plane):** `release_gate.admit_transcript_release` refuses ALL transcript releases at wave open because 3 of the 4 verdicts (KDPA · named-persons · transfer-basis) are `PENDING` per owner still-blocked list.  Owner ratifications pending: **R-7 · R-15 · R-16 · R-17**.  Only `licence_class:owner_full_rights` is ratified (per Ruling #2, DECISIONS 2026-09-12T~12:00Z).  Until any three of R-7/R-15/R-16/R-17 land, the write-back is DETERMINISTICALLY refused by the CP-A5 mechanism.

## 5. Blockers to escalate to owner (in the ledger)

1. **`BLOCKER-HF-A5-01` (HF model-hosting)** — `openai/whisper-small` is not on the `hf-inference` provider path.  Options for resolution:
   * Choose a different HF-hosted model for ASR that IS on `hf-inference` (a probe of alternatives would need a fresh session's egress budget).
   * Use a different HF Inference-Providers path (e.g. `router.huggingface.co/fal-ai/whisper-1` — needs a HF Inference-Providers Pro subscription).
   * Self-host whisper on `akki-vm` / `akki-vm-ii` (requires Transcription-server host+creds — already on the owner still-blocked list as a MISSING BIND).
2. **`BLOCKER-HF-A5-02` (NAS-to-bytes plumbing)** — small helper module `services/audio_poc/nas_fetch.py` needed; deferred as follow-on.
3. **`BLOCKER-HF-A5-03` (release-gate verdicts)** — R-7, R-15, R-16, R-17 pending on owner (already on the still-blocked list).

## 6. What the mechanism DOES deliver at CP-A5 close

* Full CONTRACT for gap-fill: `GapFillTranscript` frozen dataclass (no text field) + `HFTranscribeError` hierarchy + `transcribe_gap` pre-flight refusals + `emit_gap_fill_receipt` (no text field in output, guard-invoked) + `write_gap_transcript_or_refuse` (release-gate integration, refuses when any verdict PENDING, refuses on transcript-body token leak).
* 12 invariants GREEN in `tests/invariants/test_wave_audio_poc_cp_a5_hf_gap_fill.py`.
* Endpoint URL updated from legacy `api-inference.huggingface.co` to current `router.huggingface.co/hf-inference/models/<model_id>` (reality catches up per SO §3.5).
* Auth + env-only loading exercised in-container: env-injected token accepted by router, no 401/403.
* Transcript-leak guard exercised: constructed a leak-shaped transcript body, guard raised RuntimeError; guard message contains no token substring.

## 7. Disposition

* **Wave continues to CP-A6 (wave close)** per owner directive: *"On W-AUDIO-POC wave close (CP-A6), do NOT halt for ack — flow directly into W-DATA-SUITE-V2-LIFT."*
* **Full end-to-end gap-fill remains BLOCKED** on the three items above.  Wave-honest limit `E.1` in the grounding brief anticipated the transcription-server MISSING BIND; the router probe refined the blocker into three separately-resolvable items.
* **Ratchet-worthy work** (12 CP-A5 invariants + mechanism modules) closes CP-A5 with ratchet `3911 → 3923 (+12)`.
* **Owner-facing** flag: the three blockers above should be discussed at M5 sprint-completion time.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
