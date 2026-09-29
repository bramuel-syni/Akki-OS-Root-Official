# M2 — language cognition trained on akki-vm-ii · 29 Sep 2026

Owner directive: "Akki trains language cognition model on akki-vm ii … Run M2
autonomously. Maintain same rigour in the structure shaped in M1." Owner inputs
this increment: 2 h+ training budget; train on the extracted `google-transcripts/
datasets` material (clean-cut, labelled), keep other material for testing model
success; treat audio as a database (AIP §1.1) and use the biometric (speaker)
layer already designed in the repo to shorten the learning curve.

E1 is the control plane only. Every phase below ran as a daemonised job on
**akki-vm-ii** (2× H200), dispatched through `services/audio_plane_v1/
language_cognition_dispatch.py` (Northena admit → reviewed code bundle over the
pinned SSH seam → job state/receipt on the host volume → one bounded status RPC →
Northena converge row + Track-4 run receipt). No corpus bytes, weights or
embeddings touched E1. Job records: `phase0/census_autonomy_state/language_cognition/`.

## What was wrong at handoff and what was fixed

- `language_cognition_worker.py` line 428 `NameError: win` (train phase could not
  start) — fixed.
- The previous corpus receipt classified every object as `other` (wrong layout
  guess) and `measure_staged` used the `wave` module on files that are **MP3 in a
  `.wav` container** → 100 % "unreadable". Layout parser rewritten for the real
  `datasets/<code>/<session>/{audio,transcript,metadata}/<id>.*` shape; duration/
  codec/sample-rate now read with `ffprobe` (the declared suffix is a claim, the
  codec is the fact).
- Zero-byte extension-less prefix-marker objects (182) collided with directories at
  staging (`IsADirectoryError`) — they are now counted and skipped.
- 262 sessions existed **only** as `<session>.tar.xz` archives; the worker now
  unpacks archive-only sessions and indexes each session's origin
  (`folder` 1300 · `folder+archive` 2976 · `archive` 262) so archive-only sessions
  can serve as a session-disjoint second test set.
- New phase `speaker_linkage` (AIP §6 custody-compliant biometric linkage) and a
  presenter-disjoint split + no-speaker-ID probe in `train_baseline` (MUST-DO §3/§4).
- Control plane: `_bank_run_certificate` writes the AIP §11.6 completion certificate
  and checks the receipt against the SEALED defaults (span rule, presenter N,
  MOAC) instead of re-thresholding. Offline tests: `tests/census_operational/
  test_language_cognition_worker.py` (10) + `..._dispatch.py` (8); live API suite
  `..._api.py` (testing agent, iteration 61, 9/9 pass).

## Phase receipts (all `digest_verified`, Northena admit/gate/converge rows banked)

### corpus_census `lcj-1851c62aee3b` (05:03–05:06 UTC)

- Bucket `google-transcripts`, prefix `datasets/`: **15,899 objects · 54.1 GB**
  (+182 prefix markers). Survey of the rest of the bucket (facts, not staged):
  `transcripts/` 6,106 txt (no audio) · `roadshows/` 1,439 jpg/png · `oms/` 3 txt ·
  root `datasets*.tar.xz` 3 archives. So "the other files" with audio for testing
  model success are **not in this bucket** — they are the M1 NAS estate; that
  evaluation is the M9 acceptance path.
- Staged corpus read as a database on the host: `corpus_db/files.jsonl` (3,958
  rows) and `corpus_db/segments.jsonl` (351,021 rows; language/session/file/start/
  end/speaker/chars; `code_switch: unlabelled`). Totals: **529.5 h audio, 828.6 h of
  transcribed segment time** (segments overlap — speaker turns — so segment time
  exceeds audio time in kln/luo/kam), 12 language codes, 8 with audio:

| code | language | files | audio h | speech h | segments | session-local speaker ids | actual codec | sample rates |
|---|---|---|---|---|---|---|---|---|
| guz | Kisii | 732 | 92.2 | 107.5 | 58,291 | 1,904 | mp3 | 44.1k 726 · 48k 5 · 22k 1 |
| kam | Akamba | 1,166 | 85.4 | 144.6 | 21,190 | 1,795 | mp3 | 44.1k 752 · **11k 311** · 48k 92 · 22k 11 |
| kik | Kikuyu | 584 | 82.1 | 81.2 | 44,549 | 1,470 | mp3 | 44.1k 527 · 48k 19 · 11k 18 · 22k 16 · 16k 4 |
| kln | Kalenjin | 295 | 89.8 | 183.7 | 101,499 | 1,496 | mp3 | 44.1k 284 · 48k 6 · 22k 5 |
| luo | Luo | 558 | 82.1 | 206.8 | 66,577 | 1,666 | mp3 | 44.1k 296 · **11k 225** · 16k 18 · 22k 16 |
| lwg | Luhya | 60 | 9.2 | 18.5 | 8,849 | 293 | mp3 | 44.1k 44 · 48k 16 |
| swa | Kiswahili | 549 | 87.7 | 86.3 | 50,066 | 1,495 | mp3 | 44.1k 484 · 11k 43 · 48k 22 |
| bxk | Bukusu | 14 | 1.1 | 0 | 0 | 0 | mp3 | 44.1k 13 · 48k 1 |
| ebu/mas/mer/mrg | — | 0 | manifests only | | | | | |

- Honest gap (unchanged): English and Sheng absent; no per-span language labels →
  code-switched spans unlabelled → **MUST-NOT §1 stands for the final model.**
  Condition columns (age/device/environment) blank in every metadata row; the one
  measurable condition is source sample rate (11 kHz telephone-band material is
  concentrated in kam/luo — a confound the evaluation reports per condition).

### register_bases `lcj-e3ca45b010eb` (earlier this session)

Whisper-small (MIT) + VoxLingua107 ECAPA (Apache-2.0) pulled on the host, weight
sha256 pinned, banked through `LanguageCognitionTrainingBaseRegistration_v1`
(`training_base_registration.json`). Torch 2.11+cu128, CUDA available.

### speaker_linkage `lcj-e16f26a43d22` (05:07–05:13 UTC)

Instrument `speechbrain/spkrec-ecapa-voxceleb` (Apache-2.0, weight sha256
`f42e1c9f…`). ≤6 three-second crops per session-local speaker id → mean ECAPA
embedding → average-linkage cosine clustering at 0.45. **Embeddings destroyed after
cluster assignment; only opaque presenter ids persist** (`speaker_clusters.json`).

| code | session-local ids | presenters | spanning >1 session | singletons | largest | mixed-gender-suffix clusters | N≥20 |
|---|---|---|---|---|---|---|---|
| guz | 1,729 | 201 | 89 | 105 | 199 | 25 | yes |
| kam | 1,728 | 296 | 151 | 140 | 182 | 24 | yes |
| kik | 1,372 | 203 | 80 | 107 | 200 | 41 | yes |
| kln | 1,112 | 204 | 103 | 90 | 115 | 37 | yes |
| luo | 1,446 | 235 | 105 | 113 | 164 | 35 | yes |
| lwg | 254 | 69 | 36 | 29 | 20 | 8 | yes |
| swa | 1,392 | 253 | 119 | 127 | 148 | 13 | yes |

Reading: a radio station's hosts recur across hundreds of programmes (largest
presenter = ~200 session-local ids), which is exactly why session-disjoint ≠
speaker-disjoint. Over-merging at this threshold is conservative for disjointness
(it can only move more material to one side), and the mixed-gender-suffix count is
the visible error signal. This is a measured linkage, not ground truth.

### gate_eval `lcj-4e9283997834` (05:15–05:20 UTC) — pre-trained overlay, 60 files/language

| code | Whisper-LID top / agree / abstain | VoxLingua107 top / agree / abstain |
|---|---|---|
| swa | sw 60 · **1.00** · 0.00 | sw 60 · **1.00** · 0.00 |
| kik | sw 53 · 0.00 · 0.10 | sw 52 · 0.00 · 0.08 |
| luo | sw 53 · 0.00 · 0.10 | sw 49 · 0.00 · 0.12 |
| kam | sw 50 · 0.00 · 0.17 | sw 47 · 0.00 · 0.18 |
| guz | sw 20 · 0.00 · 0.60 | sw 25 · 0.00 · 0.37 |
| kln | sw 23 · 0.00 · 0.57 | sw 35 · 0.00 · 0.20 |
| lwg | sw 43 · 0.00 · 0.27 | sw 37 / sn 14 · 0.00 · 0.03 |

Measured, not asserted: both pre-trained bases collapse every Kenyan language onto
`sw`. The overlay cannot deliver the census's language distribution; the trained
model is required. (Gate default 0.90 is met only for Swahili.)

### train_baseline smoke `lcj-229ca62fe5cb` (05:14–05:18 UTC)

6 files/language, 420 s budget: pipeline proven end to end on the host — windows,
presenter-disjoint split, LoRA+head training in bf16, held-out + archive-test
evaluation per language and per condition, no-speaker-ID probe, span rule, artefact
hash, certificate banked. Numbers are not meaningful at that size and are not
quoted.

### train_baseline full run `lcj-f96c86a16312` — see "Training result" below

Parameters: budget 9,600 s (training share 0.65), ≤60 windows/file, ≤30,000
windows/language, batch 64, lr 2e-4, LoRA r=16 on Whisper-small encoder q/v
projections ⊕ frozen VoxLingua107 ECAPA (256-d) → LayerNorm/Dropout/Linear head,
2 s windows cut only inside transcribed speech, bf16 autocast, H200.

## Training result — `lcj-f96c86a16312` (05:22–07:07 UTC, receipt digest-verified, certificate banked)

Compute: 14,511 steps · 8 epochs · batch 64 · 6,405 s on one H200 (28.99 GB peak) · bf16 ·
600,072 trainable parameters (LoRA r=16 + head). Data touched (training manifest sha256
`f407af1d…`): 3,284 train files / 124,273 windows; 1,384 held-out-presenter files /
32,781 windows; 262 archive-only sessions / 7,776 windows. Learning curve (held subset,
accuracy on judged / abstention): step 500 → 0.925 / 0.33 · 2,500 → 0.916 / 0.075 ·
6,500 → 0.938 / 0.041 · 12,500 → 0.932 / 0.018 · 14,500 → 0.932 / 0.018.

**Held-out PRESENTERS (never seen in training) — accuracy on judged windows, abstention
at confidence 0.6, overall 0.940 / 1.9 %:**

| code | language | held presenters | windows | accuracy | abstention | ≥ 0.90 default |
|---|---|---|---|---|---|---|
| kik | Kikuyu | 22 | 5,853 | **0.976** | 0.008 | yes |
| kln | Kalenjin | 42 | 3,518 | **0.957** | 0.016 | yes |
| kam | Akamba | 60 | 5,557 | **0.951** | 0.017 | yes |
| guz | Kisii | 32 | 5,340 | **0.944** | 0.017 | yes |
| swa | Kiswahili | 36 | 6,116 | **0.939** | 0.021 | yes |
| luo | Luo | 83 | 5,583 | **0.925** | 0.025 | yes |
| lwg | Luhya | 15 | 814 | **0.592** | 0.095 | **no** (43 train presenters, 2,501 windows — under-resourced; confused with swa/kik) |
| bxk | Bukusu | — | 0 | unmeasured | — | no transcripts → no windows |

Archive-only sessions (session-disjoint second test set, 7,776 windows): overall **0.954**
(guz 0.978 · kam 0.943 · kik 0.948 · kln 1.00 on 60 · luo 0.948).

Per condition (source sample rate, held-out): 44.1 kHz 0.942 (25,880) · 11.025 kHz 0.959
(4,476) · 48 kHz 0.895 (1,244) · 16 kHz 0.886 (693) · 22.05 kHz 0.818 (391) · 32 kHz 0.989
(97). The 11 kHz telephone-band stratum is NOT the weak one; the rarer 22/48 kHz strata are.

Top confusions: luo→kik 169 / swa 141; swa→kik 137 / kam 98; guz→kik 134; lwg→swa 114 / kik 76.

Span rule (2 s windows, min span 0.5 s, hysteresis 2 — equal to the sealed default) produces
monolingual spans on held-out files, e.g. `67263.wav` → `guz` 8.0–482.0 s.

**No-speaker-ID probe (MUST-DO §4) — MEASURED FAIL.** A linear probe on held-out presenters
(≥20 windows each, 50/50 split): the LoRA-encoder representation identifies presenters at
0.77–0.84 accuracy (chance 0.03–0.07, majority 0.16–0.55) in every language; the artefact's
OUTPUT logits identify presenters above chance+margin in kam (0.616 vs majority 0.396), kik
(0.565 vs 0.481) and kln (0.367 vs 0.161); not in guz. → `no_speaker_id_probe_passed: False`.
The artefact carries speaker information; the final model needs speaker-adversarial or
DP-SGD training (DP-SGD not applied here — DQ-24 fork stands, recorded in the receipt).

**Verdict (unchanged by the good numbers): NOT ADMISSIBLE as the final model.** MUST-NOT §1
(no labelled code-switched spans; English/Sheng absent) and MUST-DO §4 (probe failed).
Six of seven measured languages meet the 0.90 per-language DEFAULT on presenter-disjoint
material; the seventh (Luhya) does not. Artefact `d2cd0497…` stays on akki-vm-ii under
RMS_TENANT custody, not admitted; nothing relabelled. Certificate:
`phase0/census_autonomy_state/language_cognition/run_certificate_lcj-f96c86a16312.json`.

## What this is and is not

- It IS: a measured compute receipt for the commissioned language-cognition job
  on the tenant's material inside the perimeter, with a presenter-disjoint split,
  abstention reported, per-condition readings, a no-speaker-ID probe and a signed
  artefact hash + training manifest hash (AIP §11.5/§11.6).
- It is NOT the final model: MUST-NOT §1 (no labelled code-switched spans), English
  and Sheng absent, DP-SGD not applied (DQ-24 fork stands, recorded), presenter
  linkage is inferred. `final_model: False`; artefact custody RMS_TENANT on
  akki-vm-ii; not admitted; nothing relabelled. Final qualification is roadmap M9.

## Reproduce / operate (control plane only)

    python assessment_workspace/tools/m2_language_cognition_run.py list
    python assessment_workspace/tools/m2_language_cognition_run.py refresh <job_id>
    python assessment_workspace/tools/m2_language_cognition_run.py submit <phase> '{...}'
    GET /api/portal/census/language-cognition/jobs[/{job_id}]   (RMS operator)
