READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M6 · Milestone-Open Report · 2026-09-15T~17:50Z

**Milestone status:** M6 (Audio-Plane v1.0 Production Build · §15 order) — **OPENING** per owner ratified sequencing 2026-09-15T~04:12Z (DECISIONS Effect 8) as confirmed by GO-chain 2026-09-15T~16:20Z: *"After the audit lands, resume: paired W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL → W-CENSUS-RUNTIME-ORCHESTRATION (expanded) → M6 open (Path α/β flagged) → M7 open."*

**Preconditions verified:**
- M5 complete (2026-09-15T~09:47Z · `notes/M5_SPRINT_CLOSE_20260915.md`).
- M8 quick hardening chain completed for #1–#5:
  - M8 #1 · W-M8-TESTS-FIRST-GUARD-INVARIANT (CP-M8-G1 part-B sealed 2026-09-15T~11:00Z).
  - M8 #2 · W-EXPORT-ARTEFACT-RENDER (CP-EXR1 sealed 2026-09-15T~15:58Z).
  - M8 #3+#4 · W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL paired (sealed 2026-09-15T~17:20Z).
  - M8 #5 · W-CENSUS-RUNTIME-ORCHESTRATION (scope EXPANDED · sealed 2026-09-15T~17:45Z).
- M8 #6 · W-AUDIO-PROD-MODEL-SELECT · **HALT-flagged DEFERRED** (see §C below).
- Ratchet: 4105 (green). Track-a HEAD `29ff3984`. Master HEAD `b8370491`.
- M6 grounding brief pre-banked: `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md` (10 sub-waves + P2-deferred voice-identity/music-register).

---

## §A · Path α/β decision flag (per owner directive)

Owner directive 2026-09-15T~04:12Z + 2026-09-15T~16:20Z (verbatim): *"M6 open (Path α/β flagged)"*.

**Path definitions (per DECISIONS line 8641 verbatim):**
- **Path α** — re-enumerate to `NEWSCLIPS` / `PROMOS` / `COMMERCIALS` / `ADS` / `video` shares if admin unlocks audio-bearing read access. This is the "audio corpus actually exists in the estate" path.
- **Path β** — video-plane ingestion for OFFAIRRECS (accept the video-only corpus finding at face value and build the ingestion pipeline against a video-plane input).

**Path decision at this open:** **α-pending** (default framing per owner ratified pattern — do NOT self-rule β).

**Evidence in favour of α (from disk, D12-03 corpus finding):**
- OFFAIRRECS is video-only-with-null-audio-track across all 9 media-bearing channels under the `bramwel` account (ffprobe corpus matrix 2026-09-15T~11:00Z · `phase0/d12_poc_receipts/20260915T110144Z_d12_03_channel_corpus_characterization.json`).
- 5 alternative audio-bearing shares (`NEWSCLIPS`, `PROMOS`, `COMMERCIALS`, `ADS`, `video`) returned `NT_STATUS_ACCESS_DENIED` under bramwel (`phase0/d12_poc_receipts/20260915T110930Z_d12_03_share_probe_matrix.json`).
- 4 admin/owner-desk items already surfaced (audio-plane sensitivity declarations · alternative NAS credentials · radio subnet route · transcription server host+creds).
- The estate explicitly carries audio-labelled shares — the audio corpus exists in the estate; only bramwel's ACL denies read access.

**Evidence in favour of β:** none from disk. Would require an owner ruling that the OFFAIRRECS video-only corpus is the intended audio-plane source and the video-plane input is the planned ingestion shape.

**Framing:** α-pending. Wave `W-M6-INGEST-STAGE-1` opens with an **audio-source-agnostic** contract: the ingestion capture mechanism accepts a caller-provided audio stream reference (Path α will inject a NAS SMB audio-bearing share reference · Path β could inject an OFFAIRRECS video reference with an audio-decode layer that would produce empty segments). The mechanism itself is Path-neutral. Owner ruling on α vs β is required BEFORE first live run of CP-M6-1-1 against real estate content; the invariant tests can proceed against synthetic fixtures.

**Owner ruling requested at M6-open:**
> Does the owner ratify Path α-pending framing (default), or does the owner direct Path β (video-plane ingestion for OFFAIRRECS as-is)?

Absent an owner ruling, this report proceeds with α-pending framing and CP-M6-1-1 opens against synthetic fixtures. First live-estate run of CP-M6-1-1 requires audio-source unblock OR owner β-ruling.

---

## §B · Owner-desk items outstanding (audio-source unblock)

Four items block first-live-estate audio ingestion. Reported here so they can be worked in parallel with M6 code lane.

| # | Item | Desk | Blocking | State |
|--:|---|---|---|---|
| 1 | Audio-plane sensitivity declarations | Owner | End-to-end release-gate admission for audio artefacts | Owner-desk (surfaced multiple times) |
| 2 | Alternative NAS creds with audio-share read access | Admin | Path α CP-M6-1-1 first live run | Admin-desk |
| 3 | Radio subnet route (`10.10.55.x`) INBOUND-BIND | Admin | Live radio ingestion (M6 sub-wave 1 optional) | Admin-desk |
| 4 | Transcription server host + creds | Owner | Live transcription pipeline (M6 sub-wave 4+) | Owner-desk |

Not blocking M6 code-lane opening. Blocking first-live-estate run of applicable sub-waves.

---

## §C · M8 #6 · W-AUDIO-PROD-MODEL-SELECT · HALT-flagged DEFERRED

W-AUDIO-PROD-MODEL-SELECT is HALT-flagged DEFERRED per D12-03 corpus finding. Model-selection wave requires a real audio source to select against; the current OFFAIRRECS corpus is video-only-with-null-audio under bramwel scope and produces zero transcription value per file (`notes/D12_03_CORPUS_FINDING_20260915.md`).

Model selection would produce an artefact grounded in nothing, which fails wave-honest-limit at open. Deferring until real audio source enumerates (Path α admin unblock OR Path β owner ruling with video-plane audio decode).

Owner-desk item: unblock the audio source, then W-AUDIO-PROD-MODEL-SELECT resumes as an M6-lateral wave.

---

## §D · N7 numbering gap (canon housekeeping)

Per owner directive `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md` line 23 ("fix the N7 numbering gap there"):

The M6 grounding brief inherits an N7 numbering gap in the AUDIO_PLANE_SPEC v1.0 verbatim requirements. Specifically:
- §4.1 lands N1 (language identifier).
- §4.3 lands N2 (channel condition).
- N3..N6 land in §4.4–§4.5 (deferred to sub-wave 2 open).
- **N7 gap:** §4.4 P068..P070 verbatim carries the synthesis-attribute carrier but its N-index is not explicitly named in the spec. Grounding brief §C sub-wave-1 CP-M6-1-4 marks this "specify at CP-M6-1-4 open per verbatim §4.4" — resolution deferred to CP-M6-1-4 open.

**Status:** N7 gap is BANKED for CP-M6-1-4 open. Not gating this M6-open report.

---

## §E · M6-open action-item list (chained)

1. **CP-M6-1-1 · language ID at segment level** — TESTS-FIRST · new invariant: language ID emitted per-segment · offline · in-perimeter · CPU-viable check. Grounding brief pre-banked; CP-M6-1-1 opens next.
2. **CP-M6-1-2 · code-switch point detection** — TESTS-FIRST · code-switch points annotated with confidence + language-pair.
3. **CP-M6-1-3 · channel condition profile derivation** — TESTS-FIRST · per-segment channel condition ∈ {studio, field, telephone-band} + transmission-artefacts + background-class carriers.
4. **CP-M6-1-4 · synthesis attributes (N7 gap resolution)** — TESTS-FIRST · synthesis-attribute carrier per Audio-Plane §4.4 verbatim.
5. Then W-M6-INGEST-STAGE-1 seals.
6. Then W-M6-DEDUP-INSTANCE-CONDITION-MAP (sub-wave 2) opens per §15 dependency ordering.
7. ... (per grounding brief §C).

---

## §F · Model-selection D10/D11 open rulings

Two INFERRED starting points sit as open owner rulings for sub-wave 1:
- **D10** · Silero VAD INFERRED starting point for language ID (offline · in-perimeter · CPU-viable).
- **D11** · pyannote/speaker-diarization-3.1 INFERRED starting point for speaker separation (a downstream sub-wave prerequisite).

Both are RULING_LEDGER OPEN row 13. CP-M6-1-1 lands the **pluggable seam** that admits any ratified model on ratification; the seam accepts an `[INFERRED-pending-ratification]` marker until owner ratifies.

Owner may ratify a specific model at any time; the seam contract does not depend on the model choice.

---

## §G · Ratchet & discipline receipts at M6-open

- Baseline ratchet: **4105** (green post-CP-CRO2 seal).
- Track-a HEAD: `29ff3984`.
- Master HEAD: `b8370491`.
- Discipline unchanged: tests-first double-green byte-match · ratchet monotonic-up · two-commit local-only · never push · terminal pytest only · testing_agent BANNED · position-redaction hard-lock · verbatim-canon · HALT-rather-than-guess · no refactor · case-agnostic negative-scan on every new module + tests.

---

## §H · Boundary-hygiene probe cadence (unchanged)

Per DECISIONS 2026-09-15T~09:50Z Effect 4 verbatim: *"Keep the CD/Visitors re-probe loop running at boundaries while egress is open."* Probes continue firing at each CP boundary of M6 sub-waves. Zero PASS across probes #1–#15.

---

## §I · Onward chain post-M6

Unchanged from ratified sequencing:
- M6 walks §15 in canon dependency order (10 sub-waves + P2-deferred).
- M7 opens (W0 platform integrity → W1 generalisation → W2+ as unblocked).
- Interleave: M3 W-BC-DYNAMIC-RECOVERY-BUILD · M2 W-PULL-SEAM-RECEIPT-UNIFY.
- W-AUDIO-PROD-MODEL-SELECT (M8 #6) resumes as M6-lateral wave on audio-source unblock.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
