# CP-NEWVAULT-SCRIPT-AUDIO-PAIRING · objective card · 2026-02-23T08:02:00Z (PARKED)

**Status:** ⚪ **PARKED** — banked at CP-AIP-7 State Commit-B on owner's 2026-02-23 drop. DO NOT BUILD until ledger promotes it.

**Candidate slot:** after CP-AIP-10 seals · before Item 6 backlog. Owner's cadence directive verbatim (2026-02-23 CP-AIP-4 GO): 'HALT after CP-AIP-10 for full plane completion report' — CP-NEWVAULT-SCRIPT-AUDIO-PAIRING is proposed for promotion out of PARKED at that HALT.

**Spec anchor:** Owner context drop `STATE/OWNER_DROPS/newvault_script_audio_20260223/DROP.md` verbatim (2026-02-23T07:55:30Z) + AIP v1.0 §4.1 language ID + §4.6 (b) dedup instance condition map + §10.2 test-set-construction stratification.

## Rationale for parking (SO §3.8 scope-freeze verbatim)

Owner cadence directive is sequential CP-AIP-4 → CP-AIP-10 with HALT after CP-AIP-10 for full plane completion report. Newvault script-audio pairing is a NEW build item outside CP-AIP-1..10 scope. Anti-drift guard: banked as context, held out of build until owner promotes it via ledger.

## Scope sketch (structural only · no build until promotion)

Parse Newvault news-script HTML → extract:
  - `script_text_paragraphs` — the `<p>...</p>` script paragraphs in the station's local language.
  - `byline` — the reporter name extracted from trailing `<p><strong>...</strong></p>` block.
  - `slug` — the story/location slug from the second trailing `<p><strong>...</strong></p>` block.
  - `audio_refs[]` — the `<audio src="/storage/<opaque_token>.mp3">` broadcast-clip references.

Then:
  - Census the audio refs as first-class items with provenance to parent script (script_html_id · byline · slug · language_hypothesis · audio_ref).
  - Pair `script_text` with `audio_clip` as an extraction-layer artifact honoring §4.6 (b) dedup instance condition map (routes through sealed CP-AIP-2 write-boundary) and §6.2 custody boundary (no voiceprint / per-utterance-embedding / speaker-identity).
  - Language attribution is a §4.1 unmeasured HYPOTHESIS (station prior + text-side signal) until the sealed language identifier confirms it (§1.4 record-as-unmeasured-until-measured discipline).

## Strategic value (owner-banked · verbatim)

- Near-ground-truth supervision for ASR training data at zero labeling cost.
- Feeds §4.1 language ID · occurrence index · §10.2 test-set stratification.

## Dependencies / blockers

- **Newvault/Razuna MySQL estate access** — credentials in scope per lifted DQ-06 holds; specific IAM grant for MySQL read still owner-side. `/storage/...` src paths are Newvault-host-relative; resolving to actual audio bytes requires host access.
- **Sealed CP-AIP-1 ingest capture** must have already accepted the parent HTML script as a first-class ingested artifact.
- **Sealed CP-AIP-2 dedup condition map** must be composed for §4.6 (b) at write time.

## PROPOSED shape (structural only · DO NOT BUILD until promoted)

- `backend/services/audio_plane_v1/newvault_script_html_parser_v1.py` (parser: HTML → `NewvaultScript_v1` frozen carrier).
- `backend/services/audio_plane_v1/script_audio_pairing_v1.py` (pairing carrier + census helper + provenance to parent script).
- Refusal classes: `NewvaultScriptShapeInvalid` (malformed HTML fragment) · `AudioRefUnresolvableAtNewvaultHost` (host resolution failure) · `LanguageHypothesisAssertedAsMeasured` (§1.4 discipline).

## Acceptance criteria (become RED-first pytest invariants when promoted)

1. Parser refuses HTML fragment missing all `<p>` paragraphs → `NewvaultScriptShapeInvalid`.
2. Parser refuses HTML fragment with no `<audio src="...">` → `NewvaultScriptShapeInvalid` (a news-script without audio is not a Newvault script).
3. Parsed `NewvaultScript_v1` carries `language_hypothesis` field marked UNMEASURED (§1.4) until identifier confirms.
4. Pairing routes `condition_profile` through sealed CP-AIP-2 `DedupInstanceConditionMap_v1` write boundary; refuses direct write bypassing dedup.
5. Custody discipline: pairing carrier does NOT carry voiceprint / per-utterance-embedding / speaker-identity payload (§6.2 cond-4 verbatim); structural token scan.
6. Occurrence index binds `script_html_id ↔ audio_ref` with source provenance and no bidirectional identity leakage.

## MUST NOT (when promoted)

- Assert language on the parsed script — §1.4 verbatim: record as unmeasured HYPOTHESIS until §4.1 identifier confirms.
- Ingest `/storage/...` audio bytes without Newvault-host access authorization.
- Bypass sealed CP-AIP-2 dedup instance condition map write-boundary at §4.6 (b).
- Carry any §6.2 custody-violating token in the pairing carrier.
- Sprawl beyond parsing + census + pairing shape — full training-material pipeline is DEFERRED to CP-AIP-10 downstream.

## Anchors

- Owner drop: `STATE/OWNER_DROPS/newvault_script_audio_20260223/DROP.md` verbatim (2026-02-23T07:55:30Z).
- AIP v1.0 §4.1 language identification.
- AIP v1.0 §4.6 (b) dedup instance condition map — sealed CP-AIP-2 boundary.
- AIP v1.0 §6.2 custody conditions cond-4.
- AIP v1.0 §10.2 test-set-precedes-training + population-register-defined.
- AIP v1.0 §1.4 record-as-unmeasured-until-measured.
- AIP v1.0 §1.5 unrepresentable-not-policed.

## Ledger check

**Ledger check** — this card is PARKED. It is banked, not built. It becomes an EXECUTION_ORDER.md ledger item only when the owner promotes it out of PARKED (candidate slot: after CP-AIP-10). Until then, additive-only + scope-freeze SO §3.8 binds this scope entirely out of build.
