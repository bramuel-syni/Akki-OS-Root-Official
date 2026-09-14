READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-AUDIO-POC · wave grounding brief

**Wave name:** `W-AUDIO-POC` (M5 SW1 · owner-amended sequence 2026-09-14).
**Wave class:** M (multi-CP · governance-first · perception-plane extension).
**Milestone:** M5 (final of the sprint · Data-Suite lift + Audio-POC).
**Discipline template:** `W-SOLVA-V2-LIFT` close + `W-HYGIENE-HF-TOKEN-GUARD` close (tests-first · per-CP mechanical RED · double-green byte-match · ratchet monotonic-up · two-commit local no-push · terminal pytest only · `testing_agent` BANNED · position-redaction hard-lock · EAT-window egress).
**Ratchet floor at wave open:** **3858** (banked green at boot 2026-09-14T13:00:32Z).
**Author:** main agent · 2026-09-14T~13:05Z.
**Prior state:** Steps 0 + 1 of the M5 session closed (HF-token ledger + secret-leak guard hardening). Track-a HEAD `c044112` · master HEAD `f34f33d0`.

---

## §A · Owner authorization (verbatim, 2026-09-14)

**Sequence amendment (this turn):**

> "The M5 order is reordered by the owner: **W-AUDIO-POC runs FIRST, then W-DATA-SUITE-V2-LIFT.** Record this ruling in STATE/DECISIONS.md and the ruling ledger with today's date, then proceed."

**Wave scope (this turn):**

> "TASK 1 (NOW): W-AUDIO-POC (P0). Built against the LIVE NAS `OFFAIRRECS` corpus (SMB via JUMP, creds already validated on disk/ops notes) and OBS bucket `google-transcripts` (user-provided OBS API keys). Scope: (a) enumerate/verify FINISHED transcripts already present; (b) transcribe via HF models ONLY where transcripts are missing; (c) never re-transcribe what already exists. HF token was recently rotated — load from existing secret storage, never print it. Tests-first: author invariants before implementation; every checkpoint closes with double-green byte-match and ratchet increase. Author a grounding brief note in assessment_workspace/notes/ before implementation (consistent with prior wave-open convention), commit to master. If NAS/OBS/HF connectivity fails or the egress window blocks you, do NOT mock anything. Record the blocker in a decision-point note and move to Task 2 while flagging the blocker back to me."

**HF-token hygiene (2026-09-14):**

> "env-var injection only — same for ALL secrets from now on: env/askpass, never printed, never on a command line visible to ps."

**Standing constraints re-confirmed (2026-09-14):**

> "ALL testing via terminal pytest ONLY … testing sub-agent is STRICTLY BANNED. Double-green byte-match required for every wave close. LOCAL COMMITS ONLY. Two-commit pattern: code on `programme/track-a` (Extraction-Akki), state/docs on `master` (assessment_workspace). NEVER push to remote. POSITION-REDACTION ONLY: never echo DB values, passwords, tokens, or credentials in the transcript. Use length/type mapping only. EGRESS WINDOW: any operational/network task (NAS, OBS, RDS, JUMP, HF) must respect 11:00–05:00 EAT (08:00–02:00 UTC). Tests-first invariant development. Ratchet may only go UP from 3858."

**On-disk supporting artefacts referenced by this brief:**

* `notes/W_AUDIO_POC_SCOPING_20260912.md` — original W-AUDIO-POC scoping doc (340 lines · 40584 B) · Rulings #1–#6 banked with owner quotes. This brief AMENDS the scoping-doc CP breakdown to the enumerate-and-gap-fill scope owner has narrowed to (this turn), while retaining the governance-wall CP-A1 verbatim.
* `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` — 1408 lines · Audio Intelligence Plane canon.
* `notes/AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md` — 574 lines · capability audit.
* `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md` — active HF token pin + hardening posture (this session).
* `notes/W_HYGIENE_HF_TOKEN_GUARD_close.md` — Step 1 seal, guard mechanism installed.
* `notes/SEC_INCIDENTS_20260914.md` — SEC-14-04 (HF re-leak · PENDING-SECOND-ROTATION) still tracked.
* `phase0/connectivity_receipts/20260914T113131Z_NAS_offairrecs_record_layout.json` — NAS reach proven via JUMP smbclient.
* `phase0/connectivity_receipts/20260914T095044Z_T7_obs_list_buckets.json` — OBS reach proven (106 buckets, `google-transcripts` in the set).
* `phase0/connectivity_receipts/20260914T113225Z_NAS_bounded_content_read_proof.json` — bounded read of NAS files proven.

---

## §B · Canon anchors

* **Canon-1 §4.6 · Extension not proliferation.** Audio modality is an EXTENSION of Mtafiti census, NOT a sibling registry. Discharges by structural composition (no new engine).
* **Audio Intelligence Plane §1.2 · No parallel machinery.** Audio pipeline composes existing platform primitives (chokepoint · release_gate · MtafitiObjectiveCarrier · perception EAB-1 pipeline modules). Deep-extract at `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` §II.
* **Doc-0 Promise #12 · Census and connection** (Doc-0 STATUS: partial → fully discharged by this wave via audio-modality extension of Mtafiti).
* **DAP-Spec A10 · Artefact egress remainder** (from M1) — discharged by this wave: any transcript artefact carries rights posture + hash + derivation from controlled units + terms cited.
* **Canon-3 §9.3 · Append-only ledger spirit** — transcript-registry rows never overwrite; each gap-fill event emits a new row.
* **Canon-4 §22 (via Solva assertion boundary reused shape)** — release verdicts return `UnitRef`s only.
* **Owner Ruling #2 (DECISIONS 2026-09-12T~12:00Z) — copyright layer** — `licence_class:owner_full_rights` on the transcript output for NAS OFFAIRRECS content per owner ruling; still bound to KDPA §V.2/V.3 verdicts on the release gate.
* **KDPA · V.2/V.3** (per scoping doc §V) — voice recordings are biometric sensitive personal data + named-persons detection is a KDPA-42 concern. Detection is TAGGED at wave close; RELEASE is REFUSED by construction until owner rulings on `kdpa_verdict` + `named_persons_verdict` + `transfer_basis` land.

---

## §C · Mechanism scope (this wave · amended per 2026-09-14 owner narrowing)

**Owner-narrowed scope** = **enumerate-and-gap-fill**, NOT the original 7-CP full language-ID + diarization + biometric pipeline. The mechanism this wave lands is:

1. **Governance walls** (three primitives, tests-first, refuse-by-default).
2. **NAS OFFAIRRECS recording inventory** — bounded read, position-redacted.
3. **OBS `google-transcripts` transcript inventory** — bounded list, position-redacted.
4. **Recording ↔ transcript pairing registry** — deterministic mapping via a canonical key (station · date · slot · filename-stem) with sha256-chained receipts.
5. **Gap set computation** — `recordings \ transcripts` under the canonical key.
6. **Gap-fill transcription via HF model** — invocation goes through the hardened HF-token loader (env-injection · never printed). Emits one transcript per gap-set entry. Transcripts land on OBS under `google-transcripts/` with a receipt in `phase0/audio_poc/`.
7. **Wave-close bundle** — sha256-chained; 5-section owner-facing plain-language report.

**Mechanism modules (new, under `programme/track-a`):**

| Path | Class | Purpose |
|---|---|---|
| `backend/services/audio_poc/__init__.py` | package marker | new package |
| `backend/services/audio_poc/readonly_nas_guard.py` | governance wall | refuse any Synology/SMB call outside `List/Read/Status`; multi-call refused; refuses if the URL/share is not the whitelisted OFFAIRRECS pattern |
| `backend/services/audio_poc/readonly_obs_guard.py` | governance wall | refuse any OBS call outside `ListObjects/HeadObject/GetObject` on `google-transcripts` bucket; refuses PutObject/DeleteObject/DeleteBucket unconditionally at the read-side; a companion writer `write_gap_transcript` uses PutObject but is gate-guarded (see release_gate.py) |
| `backend/services/audio_poc/release_gate.py` | governance wall | `admit_transcript_release(artifact, tier)` refuses `biometric_embedding \| named_identity \| speaker_labeled_audio` tiers by default; four release-verdict fields per artefact: `kdpa_verdict`, `named_persons_verdict`, `transfer_basis`, `licence_class`. Transcripts default to tier=`transcript_text_only` with `licence_class:owner_full_rights` (per Ruling #2) but the other three verdicts stay `PENDING` until owner unblocks |
| `backend/services/audio_poc/recording_inventory.py` | recording inventory | reads NAS OFFAIRRECS via `readonly_nas_guard` · returns a bounded, canonically-keyed inventory of recordings with (station, date_utc, slot, filename_stem, size_bytes, mtime_utc, sha256) tuples · position-redacts any embedded free-text that looks credential-shaped |
| `backend/services/audio_poc/transcript_inventory.py` | transcript inventory | reads OBS `google-transcripts` via `readonly_obs_guard` · returns a bounded, canonically-keyed inventory of transcripts with (station, date_utc, slot, filename_stem, size_bytes, mtime_utc, sha256, transcript_status) tuples · transcript_status ∈ {FINISHED, PARTIAL, MISSING, MALFORMED} |
| `backend/services/audio_poc/pairing_registry.py` | pairing | joins the two inventories on canonical key; emits `AudioTranscriptPair` frozen dataclass rows with `pair_state` ∈ {PAIRED, RECORDING_ONLY, TRANSCRIPT_ONLY, DOUBLE_MISSING} · deterministic ordering · sha256 over the full registry |
| `backend/services/audio_poc/gap_set.py` | gap compute | `compute_gap_set(pairs) -> Sequence[RecordingKey]` returns the RECORDING_ONLY subset — the deterministic "needs transcription" set |
| `backend/services/audio_poc/hf_transcribe.py` | transcription | loads HF token via `services.secret_hygiene.hf_token.load_hf_token_or_raise()`; invokes an HF-hosted whisper (or equivalent) model; emits `GapFillTranscript` records with (recording_key, transcript_text_len, model_id, hf_revision, elapsed_s, cost_usd_est) · text length only in receipts, transcript text is NEVER in transcripts of pytest/logs; goes via `assert_no_transcript_leak_of_active_token` guard before any receipt write |
| `backend/services/audio_poc/write_back.py` | writer | uploads new transcripts to OBS `google-transcripts` under a deterministic key derived from canonical key; refused unless `release_gate.admit_transcript_release` returns admit; emits sha256 verification |
| `backend/services/audio_poc/receipts.py` | receipts | banked shape-only receipts under `phase0/audio_poc/` (recording census · transcript census · pairing snapshot · gap-set · gap-fill outcomes · wave-close bundle) |

**Contracts (new, under `backend/contracts/`):**

| Path | Purpose |
|---|---|
| `backend/contracts/audio_poc_pairing.py` | `RecordingKey`, `TranscriptKey`, `AudioTranscriptPair` (frozen dataclass with `pair_state` Literal) |
| `backend/contracts/audio_poc_gap_fill.py` | `GapFillTranscript` (frozen dataclass; `text_len` field only, no text field) |

Every contract lands snapshot-registered in `CONTRACT_TO_SNAPSHOT`.

**Test files (new, under `backend/tests/invariants/`):**

One per CP · naming convention `test_wave_audio_poc_cp_a<N>_*.py`. Total per-CP invariants targeted (see §D for CP breakdown).

---

## §D · Checkpoint plan (owner-facing)

Each CP: mechanical RED → mechanism → per-CP double-green byte-match under `BASELINE_GUARD=1 python -m pytest tests/invariants/` → ratchet monotonic-up → per-CP seal note. Wave-close is the composite; two commits at wave close.

| CP | Owner-facing name | New invariants (est.) | Ratchet target (running) | Egress this CP? |
|---:|---|---:|---:|---|
| **CP-A1** | **Governance walls · reused-and-adapted from Mtafiti** | 12–16 | 3870–3874 | No — pure structure |
| **CP-A2** | **NAS OFFAIRRECS recording inventory** — bounded read via smbclient-through-JUMP · canonical key extraction · position-redacted census · deterministic ordering | 10–14 | 3880–3888 | Yes — 1 SMB list + N `stat`-shape reads; no bytes moved off NAS |
| **CP-A3** | **OBS `google-transcripts` transcript inventory** — bounded ListObjects · HeadObject-shape reads · transcript_status classification | 10–14 | 3890–3902 | Yes — 1 ListObjects, N HeadObject; no GetObject at inventory stage |
| **CP-A4** | **Pairing registry + gap-set compute** — deterministic join · `AudioTranscriptPair` snapshot · gap-set is a pure function of the two inventories | 10–14 | 3900–3916 | No — pure structure over CP-A2 + CP-A3 outputs |
| **CP-A5** | **HF-model gap-fill transcription** — ONE representative gap-set entry first (proof); on green, bounded loop over the full gap set. Every call uses env-injected token via the hardened loader; every receipt uses `assert_no_transcript_leak_of_active_token` before write | 10–14 | 3910–3930 | Yes — HF model pull + OBS PutObject |
| **CP-A6** | **Wave close** — bundle sha256-chained · seal `output_verified_seal.audio_poc_v1` · 5-section owner-facing report | 6–10 | 3916–3940 | No — receipts + seal |

**Wave total invariant estimate: +58 to +82 (ratchet 3858 → ~3916–3940).**

**Ordering discipline:**

* CP-A1 lands FIRST (governance walls before any live-source touch).
* CP-A2 lands after CP-A1 green.
* CP-A3 can land in parallel with CP-A2 authoring (independent surfaces) but committed sequentially.
* CP-A4 requires CP-A2 + CP-A3 both green.
* CP-A5 requires CP-A4 green AND blocks unless all pre-conditions match (HF token loads · release_gate admit_transcript_release returns True for the target artefact class · egress window in-effect · owner has not filed a HALT).
* CP-A6 always closes at least SOMETHING even if CP-A5 halts on a HALT-worthy blocker; the wave-close report enumerates whatever was closed and marks the rest EXPLICITLY BLOCKED (per owner "do NOT mock anything" directive).

---

## §E · Wave-honest limits (declared at wave open · candidates for follow-on)

1. **E.1 · Transcription server host+creds is a MISSING BIND** (owner-listed still-blocked). This wave uses HF-hosted model calls via env-injected token, NOT a separately-provisioned transcription server. If HF-hosted invocation is inadequate for the corpus (e.g. rate limits, model unavailability for the target languages), CP-A5 will HALT with a HALT-worthy blocker note and the wave closes at whatever CPs are complete.
2. **E.2 · Named-persons / KDPA / cross-border / purpose-limitation verdicts** all stay `PENDING` at the release_gate. No transcript leaves OBS until owner rulings on `R-7` · `R-15` · `R-16` · `R-17` land. This is by construction: `release_gate.admit_transcript_release` refuses if any of the four verdicts is PENDING for a non-safe tier. `licence_class:owner_full_rights` (per Ruling #2) does NOT bypass the KDPA/named-persons refusal — orthogonal axis.
3. **E.3 · No diarization / speaker-embedding / language-ID module in scope this wave** — the amended scope is enumerate-and-gap-fill only. Diarization + biometric embedding + language-ID are the full-pipeline CPs from the original W-AUDIO-POC-3-STATIONS scoping doc (§VIII.2 CPs 4/5); they are follow-on wave candidates once owner rules on the release-gate axes.
4. **E.4 · Cross-recording speaker-identity linking is NOT in scope** (per scoping doc §VIII.1).
5. **E.5 · The gap-set is deterministic on the two inventories** — if the OBS bucket contains malformed or partial transcripts under different filename conventions than the canonical key, they will be classified `MALFORMED` at CP-A3 and NOT included in the FINISHED set. A follow-on remediation wave can add a name-normaliser.
6. **E.6 · No delta-transcription across time** — if a recording exists at t0 and a transcript is added later, this wave's pairing registry is a snapshot at wave-close time. Live watching / re-triggering is a follow-on.
7. **E.7 · Cost estimate this wave** (Cassava lease basis, HF-hosted): $0 marginal for the compute (GPU idle capacity); HF-model pull egress $0.10-0.50 depending on model + gap-set size; OBS PutObject writes are intra-Nairobi to Huawei = $0 egress. Estimated total: **$0 to $2** across the full wave.
8. **E.8 · SEC-2026-09-14-04 (rotated-replacement HF-token re-leak) is still tracked as PENDING-SECOND-ROTATION.** This wave does NOT depend on a further rotation to close: the Step 1 guard (`assert_no_transcript_leak_of_active_token`) is live and the loader is env-only. But the underlying leak means owner-side rotation is still owed.

---

## §F · Commit protocol

* **Two-commit pattern per CP** (per Solva-V2-LIFT and HYGIENE-HF-TOKEN-GUARD precedents):
  * **Commit A** on `programme/track-a` in `repos/Extraction-Akki/`: test file(s), mechanism module(s), contract snapshot(s), `baseline_failures.json` ratchet bump. Commit-message convention: `W-AUDIO-POC · CP-A<N> · <one-line scope> · services/audio_poc/<file> · ratchet <from>->>>(<to>) (+<N>)`.
  * **Commit B** on `master` in `/app/assessment_workspace/`: brief updates (if any), per-CP close note, drill receipts (RED + 2 GREEN + rider 1), DECISIONS.md entry, NEXT.md refresh. Commit-message convention: `state: W-AUDIO-POC · CP-A<N> close · ratchet <from>->>>(<to>) (+<N>) · programme/track-a <SHA> · seal <path>`.
* **Wave close: additional composite commit pair** — bundle + 5-section report + full seal.
* **NEVER push.** Local commits are the record.

---

## §G · Decision points and stop conditions

Wave HALTS (blocker → decision-point note + advance to Task 2 W-DATA-SUITE-V2-LIFT) if any of the following surfaces during a live-source touch:

1. **NAS unreachable via JUMP** at CP-A2 attempt — record blocker to `notes/W_AUDIO_POC_DECISION_POINT_<TS>.md`, retain governance walls receipts, advance.
2. **OBS `google-transcripts` bucket unreadable** at CP-A3 attempt — same protocol.
3. **HF model invocation fails** at CP-A5 (rate limit / model unavailable / auth 401 / auth 403) — same protocol. **Note:** HF whoami PASSED at boot with HTTP=200; auth is confirmed alive.
4. **Egress window closes mid-CP** (UTC 02:00 = EAT 05:00) — pause CP mid-flight, resume at next window open.
5. **Any credential value observed in a receipt** or transcript — immediate HALT + file SEC-2026-09-14-05+ + owner escalation.
6. **Baseline ratchet regression** at any CP double-green — immediate HALT + investigate (no ratchet drop).

Wave PROCEEDS AUTONOMOUSLY under all other conditions per owner directive: *"Halt for owner input only at genuine decision points; otherwise proceed through both waves."*

---

## §H · DoD

1. Grounding brief authored + banked (this file). ✅ at authoring time.
2. Sequence-reorder ruling banked in `STATE/DECISIONS.md`. ✅
3. Each CP: mechanical RED + double-green byte-match + ratchet-monotonic-up + per-CP seal.
4. Wave-close bundle sha256-chained.
5. Output-verified seal at `phase0/output_verified_seals/audio_poc_v1.seal.txt` with `Kind: audio_poc_wave_close`.
6. 5-section owner-facing plain-language report at `notes/W_AUDIO_POC_wave_close.md`.
7. Every gap-fill transcript admitted through `release_gate.admit_transcript_release`; no transcript uploaded to OBS unless all four verdicts are non-PENDING (or the artefact class is `transcript_text_only` + `licence_class:owner_full_rights`).
8. Token value NEVER echoed to transcript across the entire wave.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
