# OWNER CONTEXT DROP · Newvault news-script/audio pairing · 2026-02-23

**Received:** 2026-02-23T07:55:30Z (right after CP-AIP-6 brief report-and-continue).
**Handling:** BANK VERBATIM · CP-AIP-7 continues uninterrupted · this drop is banked, not built · card lives in `STATE/OBJECTIVES/queued/CP_NEWVAULT_SCRIPT_AUDIO_PAIRING.md` as PARKED until ledger promotes it (candidate slot: after CP-AIP-10, before backlog items).

---

## OWNER STATEMENT (verbatim)

> "Newvault - Admin says - Those are actual news scripts, and within the news scripts you have embedded audio files. These are actual audio clips used in the news."

---

## EXAMPLE PAYLOAD (verbatim · bank as-is)

```html
<p>Muvia ula uungamie malelu ala manene KeNHA nuwetie kana kwakwa kwa kiao kya Mbakini vakuvi na soko wa Kavenge, leluni wa kuma Matuu kuenda Mwingi kwithela nthini wa myei itatu yukite.</p><p>Mweenekivila wa nzama nene ya KeNHA Winnie Ngumi atambukite kiaoni kiu nuwetie nimeusukuma contractor akatiie wia usu indi na vala uwetie nimekuikiithya nimatema nzia nzeo ya mwathuko na kiao kinini usini usu nikenda kuikiithya ukui ndunatilwa ni mbua ya El Nino kiao kiu kiiminukilwa kwakwa.</p><p><strong>Shadrack Ilava</strong></p><p><strong>MBAKINI BRIDGE</strong></p><audio controls="true" src="/storage/33oQ0WvjluzqypdgAVZEMhiylnSqkSCDId9FI4nb.mp3"></audio><p><br></p>
```

---

## WHAT THIS MEANS (banked observations from owner drop · verbatim)

1. **Newvault news scripts are HTML documents with a recognizable shape:** `<p>` script paragraphs in the station's local language, trailing `<strong>` blocks = reporter byline + story/location slug, and `<audio src="/storage/<token>.mp3">` = the actual broadcast audio clip embedded inline. The example text is a Bantu local language consistent with the station-language axis (Kamba-region references — Matuu, Mwingi, Mbakini — i.e., the Kamba-language station on the axis); language attribution should come from the axis + identifier, not asserted (§1.4 — record as unmeasured hypothesis until the identifier confirms).

2. **Strategic value:** these are **PAIRED text+audio records** — script text alongside its broadcast clip. That is near-ground-truth supervision for ASR training data at zero labeling cost, and it feeds:
   - **§4.1 language ID** (text-side signal + station prior)
   - **occurrence index** (script ↔ clip provenance pairing)
   - **future TargetOutcome test-set construction** (§10.2 stratified test sets)

3. **The `/storage/...` src paths are relative to the Newvault host** — resolving them requires the Newvault/Razuna MySQL estate access (credentials in scope per lifted holds).

---

## RECOGNIZABLE SHAPE (structural sketch · for parked card only · DO NOT BUILD)

- Structure of a Newvault news script HTML fragment (extracted from example):
  - N `<p>...</p>` paragraphs of script text in the station's local language (Bantu family in the example — likely Kamba per station-axis prior).
  - 1 or more trailing `<p><strong>...</strong></p>` blocks holding: reporter byline (e.g. `Shadrack Ilava`) then story/location slug (e.g. `MBAKINI BRIDGE`).
  - 1 or more `<audio controls="true" src="/storage/<opaque_token>.mp3"></audio>` blocks = broadcast audio references (Newvault-host-relative).
  - Optional trailing `<p><br></p>` layout markers.

- Provenance chain to preserve when parsed (extraction-layer only · custody-conditions-honoring):
  - script_html_id · byline_extracted · slug_extracted · language_hypothesis (unmeasured until §4.1 identifier confirms) · audio_refs[] (opaque tokens · resolution deferred to Newvault MySQL estate credentials).

- §4.6 (b) reminder: any parsed script→clip pair carrying a `condition_profile` in its provenance MUST route through the sealed CP-AIP-2 `DedupInstanceConditionMap_v1` write-boundary (§4.6 (b) dedup); language attribution is a §4.1 hypothesis until confirmed.

---

## ACTION LOG (this drop · additive-only · no build)

- [x] `STATE/OWNER_DROPS/newvault_script_audio_20260223/DROP.md` — verbatim banking (this file).
- [x] `STATE/DECISIONS.md` — one-line entry with dashes not colons (per drop instruction).
- [x] `STATE/OBJECTIVES/queued/CP_NEWVAULT_SCRIPT_AUDIO_PAIRING.md` — PARKED draft card (spec anchor cites this drop verbatim). Candidate slot: after CP-AIP-10, before backlog items. DO NOT build until ledger promotes it.

**Cadence unchanged.** Continuing CP-AIP-7 → CP-AIP-10 sequentially. HALT after CP-AIP-10 seals.
