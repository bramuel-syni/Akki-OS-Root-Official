READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-M7-W9-CONTRACT-1 · Path C default corpus_deliverable_v1 schema · grounding brief

**Sealed:** 2026-09-16T~16:37Z · Path α clean · double-green byte-match.
**Track-a HEAD:** `2e227dd22deb5bae52452fedcfe7f6b200aab9d6`.
**Master HEAD:** TBD (Commit-C fixup this-turn replaces).
**Ratchet:** 4400 → **4406** (+6).

## §A · Verbatim owner authority

> "OWNER STEER: 'On to the nxt milestone?' — read as: advance the milestone frontier as far as existing owner law allows. Exit pure hold, run this sequence (boot ritual first if resuming): 1. W2..W9 GATING TRIAGE (from-disk, honest) ... 2. FIRE whatever is BUILDABLE-NOW or PARTIALLY-BUILDABLE, in dependency order, tests-first, case-agnostic, §3.3 seals ... 3. M6/M8 seal-readiness notes ... 4. Utilization interleave continues at every boundary. Report at triage completion with the table + what you started building." (owner ruling 2026-09-16T~08:35Z)

**Standing lines the owner reasserted (verbatim):**
- No training on estate audio (SW-10 deferred).
- No biometric material.
- No enforcement hard-gate.
- No speculative shapes beyond existing owner law.

**Continuation ruling (verbatim 2026-09-16T~16:20Z):**

> "(a) Do NOT stop after Task 3 — roll straight into Task 4. The M6/M8 seal-readiness notes are owner-facing artifacts, not gates ... (c) Earliest-numbered unblocked wave/CP from the triage doc, in dependency order — with the POST-2 from-disk existence check before every build, and the standing lines intact (no estate-audio training, no biometric material, no enforcement hard-gate, no speculative shapes; blocked slices banked honestly)."

## §B · ROADMAP charter (verbatim §C.2)

> "Path C · DEFER — W2/W3 build with `pointer_or_bytes` schema; audio-bytes retention lands in W9 after Ruling #5 arrives. Corpus is transcript-only through W3.
> Default if no ruling by W2 CP0: Path C.
> Path C · POINTER-ONLY DELIVERABLE — corpus is `{source-file-pointer, segment_offsets_ms, transcript}` triples. Audio bytes stay on the source estate. `regime=SOURCE_UNTOUCHED` for audio, `regime=DELIVERABLE_GOVERNED` for the manifest."

## §C · Files landed

**On `programme/track-a` (Commit A `2e227dd`):**
- `backend/services/audio_plane_v1/corpus_deliverable_v1.py` (116 LOC).
  - `PATH_C_DEFAULT_ROADMAP_ANCHOR` (module-level verbatim anchor).
  - `CorpusSegment_v1` frozen dataclass · exact-order 3 carriers `(source_file_pointer: str, segment_offsets_ms: Tuple[Tuple[int, int], ...], transcript: str)`.
  - `CorpusDeliverable_v1` frozen dataclass · exact-order 3 carriers `(deliverable_id: str, retention_policy_ref: str, segments: Tuple[CorpusSegment_v1, ...])`.
  - `CorpusDeliverableRefused(Exception)` root refusal class.
  - `AudioBytesPayloadRefused(CorpusDeliverableRefused)` defensive symmetry (no caller yet triggers; Path A upgrades will).
- `backend/tests/invariants/test_wm7_w9_cp1_corpus_deliverable_v1.py` (237 LOC · 6 invariants).
- `backend/tests/invariants/baseline_failures.json` (`passed_floor`: 4400 → 4406 · `ratchet_history` append at `20260916T163000Z`).

## §D · Six invariants freezing this CP

| # | Invariant | What it locks |
|---|---|---|
| 1 | `test_wm7_w9_cp1_module_fabric_present` | `__all__` has the 5 expected exports (module fabric present). |
| 2 | `test_wm7_w9_cp1_corpus_segment_v1_frozen_carrier_shape` | Frozen · exact-order fields `(source_file_pointer, segment_offsets_ms, transcript)` — §C.2 verbatim triple. |
| 3 | `test_wm7_w9_cp1_corpus_deliverable_v1_frozen_carrier_shape` | Frozen · exact-order fields `(deliverable_id, retention_policy_ref, segments)`. |
| 4 | `test_wm7_w9_cp1_refuses_audio_bytes_payload_by_construction` | §6.2 unrepresentable-by-construction: no `bytes`/`bytearray`/`memoryview` type-hint on any field · no `audio_bytes`/`wav_bytes`/`pcm_bytes`/`voiceprint`/`embedding`/`raw_audio` field-name substring. |
| 5 | `test_wm7_w9_cp1_path_c_default_verbatim_anchor_present_in_module_source` | Verbatim canon anchor phrases present in module source (`Default if no ruling by W2 CP0: Path C` · `source-file-pointer` · `segment_offsets_ms` · `transcript`). |
| 6 | `test_wm7_w9_cp1_case_agnostic_zero_domain_tokens_in_module_source` | 21-token grep-negative in module source (kikuyu/dholuo/kamba/swahili/nairobi/inooro/ramogi/musyi/sunbird/whisper/pyannote/htdemucs/mms-1b/mms-lid/wavlm/panns/squim/dnsmos/broadcast/off-air/synology). Case-agnostic doctrine held. |

## §E · Wave-honest limits (banked)

- **W.1** Path A/B upgrades remain BLOCKED-on-Ruling-#5 sub-verdicts (kdpa_verdict / named_persons_verdict / transfer_basis). Path C default in force per §C.2.
- **W.2** `CorpusDeliverable_v1` has no `regime` field — regime binding lives on caller-side composition with `services.governance_plane.retention_policy` (`SOURCE_UNTOUCHED` for audio · `DELIVERABLE_GOVERNED` for the manifest). Composition surface only; caller enforces regime.
- **W.3** No canonical segment ordering imposed. Caller-defined per §C.2 (deliverable_id is opaque caller-supplied str).
- **W.4** `AudioBytesPayloadRefused` is a defensive-symmetry class only — no caller yet triggers it (Path A upgrades will).
- **W.5** No import of `services.governance_plane.retention_policy` — case-agnostic decoupling. `retention_policy_ref` is opaque str; caller-side composition is expected to bind.

## §F · §3.3 commit protocol

- **Commit A** (`programme/track-a` code + tests + ratchet): `2e227dd22deb5bae52452fedcfe7f6b200aab9d6` ✅ landed 2026-09-16T~16:37Z.
- **Commit B** (`master` state + seal + close note + grounding brief + DECISIONS + NEXT pin + GPU util files): this turn.
- **Commit C** (`master` fixup): replaces `TBD` in seal + DECISIONS + NEXT with the actual Commit-B master SHA.

## §G · Pre-seal drift-repair (banked wave-honest)

CP10 harness receipt aged 12.48h > 12h threshold at first-green attempt (time-drift during hold pattern between last CP-M8-CTCC-1 close and this CP open). Refreshed per owner directive verbatim 2026-09-08T~06:15Z:

> "real-Chromium proof, floor 3006 (fix/refresh stale harness-receipt invariant first — refresh the harness, don't relax the threshold)."

New harness receipt at `phase0/harness_ground_truth/latest.json` (at_utc `2026-09-16T16:26:53Z` · all 37 rules `bound_to_rendered_dom` · dummies absent · expected present · style signature MET). Zero-perturbation to GPU hosts (harness runs against localhost pod only).

## §H · GPU utilization at seal boundary

- Elapsed 12.93 h · Remaining 59.07 h.
- akki-vm: sampler_alive + workload_alive · telemetry_samples=320 · bench_iters=1548 (ok=1548 across 2 GPUs) · peak 100% GPU util per H200.
- akki-vm-ii: sampler_alive + workload_alive · telemetry_samples=314 · bench_iters=1548 (ok=1548 across 2 GPUs) · peak 100% GPU util per H200.
- 3096 total bench artefacts banked · zero synthetic burn · in-perimeter.
- Report served at owner-facing URL.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
