# OWNER DROP — RMS CREDS 3 + labelled multilingual ASR corpus — 2026-02-23

**Banked verbatim per SO §6.8 owner-drop discipline + §6.9 desk discipline. Do NOT interrupt in-flight CP-AIP-9/10 seals. Feeds SO-6.9 LID wave + CP-AIP-10 training. Additive-only.**

---

## 1 · Verbatim owner text — what the owner said

> "Additional data access granted - with clean data that can be used to finetune for different languages. This data is transcribed audio for the various languages... On the sheet the OBS bucket with the content is there plus the folders that have the various languages. Each language has an individual file path, the path contains a folder with the audio (called audio) and the transcript (folder with the transcript file)."

## 2 · The corpus (strategic payload)

- **Bucket:** `google-transcripts/datasets`
- **Layout per language:** `datasets/<code>/audio/` (audio files) + `datasets/<code>/transcript/` (transcript file).
- **12 languages / codes:**

| Language | Code |
|---|---|
| Kikuyu | kik |
| Embu | ebu |
| Kiswahili | swa |
| Luo | luo |
| Kalenjin | kln |
| Kisii | guz |
| Meru | mer |
| Bukusu | bxk |
| Akamba | kam |
| Maragoli | mrg |
| Luhya | lwg |
| Maasai | mas |

- **Status:** paired audio + transcript, clean, tenant-labelled — near-ground-truth supervision for ASR fine-tuning AND the exact tenant-labelled sample the LID admission gate was waiting on (resolves `TENANT-LABELS-PENDING` from the LID ruling for the 12 languages listed; other gate languages (English, Sheng, code-switched) retain honest-gap for their scope).

## 3 · Credentials CSV — landed under credential discipline

- **Source (verbatim):** `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/iux6debp_RMS%20CREDS%203.csv`
- **Landed at (non-tracked estate_keys):** `/app/backend/estate_keys/data_sources/rms_creds_3_20260223.csv`
- **Permissions:** `0600` (root:root)
- **sha256 (banked in `phase0/credential_drop_manifests/`):** `9d02dffbceb2dbe2bb0639c05874740cf06029d4e3fe9c4fcb38cf4ea83060c8`
- **Size:** 1,908 bytes; 78 lines; 7 columns.
- **Column labels row2 verbatim:** `DATABASE NAME · HOST · USERNAME · PASSWORD · STATUS · ISSUE · ISSUE RESOLUTION STATUS`.
- **Section labels (4 sections):** `VIUSASA` (L1) · `USSD` (L14) · `MICROSERVICES` (L27) · `NAS - ACESS` (L57).
- **Redacted manifest banked at:** `phase0/credential_drop_manifests/20260223T101800Z_rms_creds_3_drop_manifest.json` · manifest sha256 `d899737c935e68121109606af55294bc80db6bf81d13023dba1b12abc8ef1775` · 55 redacted row summaries.
- **Redaction policy applied:** hosts → `[MASKED · len=N]` no partial exposure; passwords → `[REDACTED · len=N]`; keys → `first 4 chars only`; database names + usernames + status/issue columns kept verbatim per owner directive (metadata).

## 4 · Application sequence (verbatim owner, item-by-item)

1. **Credential handling (name-the-objective guard).** Objective protected: not baking leaked plaintext passwords into permanent additive git history that cannot be rewritten. Raw CSV → non-tracked `estate_keys` only. Committed to track-a/main/master: REDACTED manifest ONLY. Access proceeds now (holds lifted per §6.9 clause 3). DQ-17/DQ-13 recorded — deferred rotation post-build; do not gate on it. **DONE this-drop.**
2. **Locate the bucket `google-transcripts/datasets`.** Probe with existing Huawei OBS keys AND existing AWS keys; the name suggests Google-origin transcripts but bucket may live in the OBS estate. Record endpoint + storage class + readability (List/Get) per census pattern. If blocked, record exact error as honest-gap, name the objective, request specific grant from owner — do not fake. **QUEUED — SO-6.9 wave item e2 (bucket-locate) opens after CP-AIP-9/10 seal.**
3. **Census the corpus.** For each of the 12 language folders: enumerate `datasets/<code>/audio/` + `datasets/<code>/transcript/` → object counts, total bytes, extensions, audio↔transcript pairing coverage (matched pairs count). One census receipt, measured values only. **QUEUED — SO-6.9 wave item e3 (corpus census) opens after item e2 unblocks.**
4. **Feed the LID admission gate.** Use these labelled segments as the tenant-labelled sample. Compute segment-level agreement of Whisper-LID + VoxLingua107 against transcript-folder-label ground truth; evaluate against threshold DEFAULT ≥ 90%, tagged pending. Overlay-not-measure discipline holds. Promotion overlay → measure only by receipted act; nothing relabelled. Honest-gap markers preserved for English / Sheng / code-switched (not present in this corpus). **QUEUED — SO-6.9 wave item e4 (LID gate evaluation) after item e3.**
5. **CP-AIP-10 training linkage.** Card this corpus as the labelled fine-tune / test-set source per §10.2 stratified test sets by language. Do NOT launch heavy fine-tune runs in-pod without a measured cost/compute receipt first (§1.4). Build data-ingestion + pairing seam; actual training is a commissioned-job contract item. **QUEUED — CP-AIP-10 card gains this corpus as a data-source anchor at seal time; heavy training deferred to commissioned-job contract.**
6. **Station → language axis cross-check.** These language codes are the authoritative label side — reconcile against the station→language axis. Provisional cross-map from this-drop (measured only from banked axis + owner corpus list — no fabrication):

   | Station (axis-banked) | Axis language | Corpus code | Corpus folder present? |
   |---|---|---|---|
   | Inooro FM / Inooro TV | Kikuyu | `kik` | (to be measured at census) |
   | Ramogi FM / Ramogi TV | Luo | `luo` | (to be measured at census) |
   | Citizen TV | Kiswahili | `swa` | (to be measured at census) |
   | (other RMS stations) | — | — | — |

   Full reconciliation lands in the census receipt (SO-6.9 item e3); the `present?` column is filled from measured List output, never claimed.

## 5 · Sequencing (recorded verbatim from owner)

> Sequencing: finish CP-AIP-9/10 seals → SO-6.9 LID wave now uses THIS corpus for the gate → then census + training seam. RED-first pins, 5-commit seal, all guards binding, measure-don't-assert. Report the corpus census + LID gate agreement numbers in your next report-and-continue. Continue.

## 6 · One-sentence protected-objective annotations (§6.9 desk discipline)

- **Non-tracked credential landing (§4.1 §E + §F)** protects: no leaked plaintext credential ever enters the additive git history that cannot be rewritten.
- **Redacted state manifest** protects: tenant-scoped audit trail of what was received, when, and in what shape — without ever surfacing values.
- **Corpus-locate probe (item 2)** protects: measured readability of `google-transcripts/datasets` before any downstream compute is planned; honest-gap on failure rather than fabricated readability.
- **Corpus census (item 3)** protects: measured audio↔transcript pairing coverage before the LID gate consumes the corpus as ground truth.
- **LID gate evaluation using this corpus (item 4)** protects: the shown-not-counted line per canon B5.4 — overlay labels never flow into a counted measure until the receipted-act promotion, and honest-gap markers persist for gate languages not present in this corpus.
- **CP-AIP-10 training linkage (item 5)** protects: the §1.4 cost/compute receipt discipline — no heavy fine-tune runs in-pod without a measured receipt; commissioned-job contract remains the seat.
- **Station → language axis cross-check (item 6)** protects: measured authority of the axis against the labelled ground-truth folders — no station relabelled; folder-present column filled only from measured List output.

## 7 · Received / banked timestamps

- Owner drop received: 2026-02-23, mid-CP-AIP-9 pre-Commit-A boundary (immediately after post-R-91-ε retirement double-green byte-identical sweep confirmed).
- Banked verbatim in this file: **this same boundary (CP-AIP-9-COMMISSION-VIEW pre-Commit-A).**
- Execution start: **items 2–6 open in SO-6.9 wave AFTER CP-AIP-10 seal + REPORT-AND-CONTINUE dispatches.**
