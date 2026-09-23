# OWNER RULING — LID RATIFICATION — 2026-02-23 (received mid-CP-AIP-9 sweep)

**Banked verbatim per Standing Order §6.8 owner-drop discipline + §6.9 desk discipline (one-sentence protected objective on every gate; markers over refusals wherever canon provides one). Supersedes any pending LID-model question.**

---

## 1 · Verbatim owner text (word-for-word)

> Language identification — ratified for use now; the gate follows.
>
> Neither offered option is the one to run: fastText LID.176 labels text, not audio, and needs a transcription model that isn't registered; Silero's language classifier carries a licence that must be verified as commercial before it can run (C5.4). Register two audio-native models instead, both under licences that need no review — Whisper language detection (MIT) and SpeechBrain VoxLingua107 (Apache 2.0) — pinning the hash and recording the licence file as the registration act.
>
> Run both on every segment of the 2h25min now. Write each label as an overlay detection carrying the model entry, confidence, execution mode, and regime pre-admission. That replaces [INFERRED-pending-ratification] with a real per-segment language label marked INFERRED — a detection that is shown, not a measure that is counted, which is exactly the line B5.4 draws.
>
> Build the admission gate alongside: a tenant-labelled sample of real RMS segments covering Swahili, English, Kikuyu, Luo, Sheng and code-switched speech; threshold DEFAULT ≥90% segment-level agreement, tagged pending; a segment below the model's confidence threshold is recorded unmeasured, never labelled. When a model clears the gate, its labels promote from overlay to measure by a receipted act, and the regime flag changes. Nothing is relabelled.
>
> fastText waits for transcripts. The only desk item is the threshold value; the default stands. Continue.

## 2 · Execution notes (verbatim owner)

> 1. Sequencing: finish the in-flight CP-AIP-9/CP-AIP-10 seals first, then this LID work runs as the FIRST item of the SO-6.9 wave (it replaces/absorbs item e of my previous message — the owner has now ratified exactly which models and how).
> 2. Registration act per model: pin the weight-file hash + record the licence file (MIT for Whisper LID, Apache-2.0 for VoxLingua107). Public unauthenticated weight pulls are permitted per SO §6.9(3) — do NOT present any old/leaked HF token; pull anonymously.
> 3. The 2h25min = the OWNER-Q3 sampled audio whose raw bytes you deleted after hashing. Re-fetch the needed files from s3://training-content-2026/audio/ (zero-cost path proven; verify sha256 against q3_aws_sample_hashes_only.json — byte-identity check is the provenance link). Write to / overlay, never /app.
> 4. Overlay detection record per segment: {label, model entry, confidence, execution mode, regime: pre-admission, marker: INFERRED}. Shown-not-counted per B5.4 — overlay labels must NOT flow into any counted measure until promotion. Below-model-confidence => record unmeasured, never labelled. Run BOTH models on every segment; disagreement between the two models is itself signal for the gate — record it, don't resolve it.
> 5. Admission gate build: schema + receipted-act promotion path + regime flag flip; gate evaluation needs a tenant-labelled sample of real RMS segments covering Swahili, English, Kikuyu, Luo, Sheng, code-switched — if no tenant-labelled sample exists yet, build the gate machinery and record the evaluation as honest-gap TENANT-LABELS-PENDING (a marker, not a refusal, per §6.9). Threshold DEFAULT >=90% segment-level agreement, tagged pending. Nothing is ever relabelled — promotion changes regime, not labels.
> 6. Rejected options bookkeeping: fastText LID.176 = WAITING-ON-TRANSCRIPTS (parked, not registered); Silero = LICENCE-REVIEW-REQUIRED C5.4 (parked, not registered). Record both.
> 7. RED-first pins for all of this in the usual baseline-guard framework; 5-commit seal; all guards binding; measure-don't-assert on runtimes and confidences (report measured values).
>
> Continue.

---

## 3 · Sequencing (recorded for succession)

- **NOW-IN-FLIGHT (unchanged):** CP-AIP-9-COMMISSION-VIEW seal completion → CP-AIP-10-TRAINING-RUNS seal → CP-AIP-10 REPORT-AND-CONTINUE per §6.9 cadence amendment.
- **SO-6.9 wave item e (LID) — REPLACED/ABSORBED by this ruling.** New item e: register **Whisper LID (MIT)** + **SpeechBrain VoxLingua107 (Apache 2.0)**; run both on every segment of the 2h25min OWNER-Q3 sample; write overlay detections per §4 below; build admission gate per §5 below.
- Items f/g/h of SO-6.9 wave unchanged (ENT-16 pilot licence seeds → private mirror → census three waves + tenant separation + CON-20/SFP-8 corrections).

## 4 · Registration-act contract (both models)

Each model's registration act consists of exactly the following, banked additively at seal time:

- **weight-file sha256** — pinned in `STATE/PINS.md` under a new `LID_MODEL_WEIGHTS` block.
- **licence file** — MIT for Whisper LID; Apache 2.0 for VoxLingua107. Both text files banked at `phase0/lid_registration_20260223/licences/`.
- **model entry** — canonical string identifier used in overlay detection records.
- **execution mode** — measured (`cpu` or `cuda`), recorded per detection.
- **pull provenance** — anonymous HTTPS from origin; the pull `URL`, response headers, and timestamp banked; **no HF token presented** (SO §6.9 clause 3 hazard scope = presentation of the leaked credential, not the host).

**Anti-token discipline:** the pull script wraps the request such that no `Authorization`/`token=` header is ever attached, and the environment is scrubbed of `HF_TOKEN`/`HUGGINGFACEHUB_API_TOKEN`/`HUGGING_FACE_HUB_TOKEN` before the process starts. RED-first pin asserts the wrapper's header dict has no bearer-like key.

## 5 · Overlay-detection record shape (contract sketch — full seal at LID slice)

Per audio segment × per model:

```
OverlayLidDetection_v1(
  segment_ref: str,              # provenance-anchored SegmentRef
  model_entry: str,              # canonical model identifier
  label: str | None,             # ISO-639-1/3 code, None if below-confidence
  confidence: float,             # measured; 0.0 <= c <= 1.0
  execution_mode: Literal["cpu","cuda"],
  regime: Literal["pre-admission","post-admission"],
  marker: Literal["INFERRED","unmeasured"],
  disagreement_with_other_model: bool | None,  # signal for the gate; do not resolve
  detected_at_utc: str,          # ISO-8601 tz-aware
)
```

- `marker="INFERRED"` when label is set (shown-not-counted per B5.4).
- `marker="unmeasured"` when label is None because below model confidence threshold.
- `regime="pre-admission"` until the model clears the admission gate; then a **receipted act** flips to `"post-admission"` on future detections. **Nothing is ever relabelled.**
- Overlay detections carry a **do-not-flow-into-counted-measure** structural guard (invariant pin enforces this at admission-gate compose boundary).

## 6 · Admission-gate contract (schema-only at this drop; full seal at LID slice)

- Input: tenant-labelled sample of real RMS segments covering Swahili, English, Kikuyu, Luo, Sheng, code-switched.
- **DEFAULT threshold ≥ 90% segment-level agreement**, tagged `pending`; owner may retune before promotion.
- Below-model-confidence → recorded `unmeasured`, never labelled.
- Promotion: **receipted act** (owner signature required per canon 8 §4 W2) flips regime `pre-admission` → `post-admission` for all future overlay detections; historical overlay detections **not relabelled**.
- **Absence of tenant-labelled sample:** record `TENANT-LABELS-PENDING` honest-gap marker (not a refusal) per §6.9 desk-discipline; gate machinery still builds, gate evaluation records honest-gap.

## 7 · Rejected-options bookkeeping (recorded)

- **fastText LID.176** → `WAITING-ON-TRANSCRIPTS` — parked, NOT registered. Reason (owner verbatim): "fastText LID.176 labels text, not audio, and needs a transcription model that isn't registered."
- **Silero language classifier** → `LICENCE-REVIEW-REQUIRED C5.4` — parked, NOT registered. Reason (owner verbatim): "Silero's language classifier carries a licence that must be verified as commercial before it can run (C5.4)."

## 8 · One-sentence protected-objective annotations (§6.9 desk discipline)

- **Whisper-LID registration act** protects: audio-provenance-and-licence traceability of an every-segment LID label without a token-presentation hazard.
- **VoxLingua107 registration act** protects: audio-native corroboration of Whisper-LID under a licence needing no review, before any regime flip.
- **Overlay `INFERRED` marker** protects: B5.4 "shown-not-counted" line — the label is displayed, never counted as a measure until the admission gate clears.
- **Admission-gate DEFAULT ≥ 90% threshold** protects: single-model overreach — a label enters measure only after tenant-labelled agreement passes the DEFAULT bar (with `pending` tag so owner may retune).
- **TENANT-LABELS-PENDING honest-gap marker** protects: function-progression when tenant labels are not yet available — the gate machinery lands and evaluates honest-gap, so nothing is blocked without naming what it protects.
- **Anti-token pull wrapper** protects: HF hazard scope (SO §6.9 clause 3) — public weight pull proceeds while presentation of the leaked credential is structurally impossible for this call.

## 9 · Re-fetch provenance (2h25min audio)

- Source of truth: `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/q3_aws_sample_hashes_only.json` (sha256 index of the 9.8 GB AWS sample downloaded during OWNER-Q3).
- Re-fetch path: `s3://training-content-2026/audio/` (zero-cost path proven at Q3 trial).
- Byte-identity check: each re-fetched file's sha256 verified against `q3_aws_sample_hashes_only.json` at the LID slice; mismatched files → `Q3-RESAMPLE-DRIFT-<n>` honest-gap, not silent proceed.
- Storage: `/overlay/lid_q3_resample_20260223/` (never `/app`), read-only after fetch.

## 10 · Received/banked timestamps

- Owner drop received: 2026-02-23, mid-CP-AIP-9 pre-Commit-A sweeps (sweep_A GREEN 6334/1/0 in 187.50s; sweep_B in flight).
- Banked verbatim in this file: **this same boundary (CP-AIP-9-COMMISSION-VIEW pre-Commit-A).**
- Execution start: **after CP-AIP-10 seal + REPORT-AND-CONTINUE dispatches**, per §6.9 cadence amendment. Sequencing is single-threaded; no parallel opens.
