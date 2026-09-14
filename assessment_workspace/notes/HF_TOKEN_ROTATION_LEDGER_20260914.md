READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# HF-token rotation ledger · 2026-09-14

Canonical state-ledger record for the Hugging Face access token used by the platform for gated-model pulls (audio POC). This file is a STATE UPDATE — not a wave close, no RED, no ratchet. It supersedes prior DECISIONS.md footers that read *"SEC-2026-09-12-01 rotation still owed by owner post-session"* (last carried in the W1c close, 2026-09-13T~08:30Z).

## 1. Owner rulings (verbatim, 2026-09-14)

* **M5 open directive (this session):**
  > "recommendation approved, but M5 being the last thing in the sprint. As we wait for the admin, we can proceed with what is reachable."

* **HF-token rotation ruling** (attached to M5-open):
  > "these are file labels but no confidential information. We have full rights on this data."
  (Applies to the rotated-replacement artefact — grants full ingestion rights but does NOT relax the transcript-leakage guard.)

* **Secret-hygiene rule** (2026-09-14, verbatim):
  > "env-var injection only — same for ALL secrets from now on: env/askpass, never printed, never on a command line visible to ps."

* **Wave sequencing (this session, 2026-09-14):**
  > "HF-TOKEN ROTATION — this is a STATE/LEDGER update, NOT a ratchet wave: register the new token (0600, env-only, never printed), mark `SEC-2026-09-12-01` OWNER-ROTATED (pending owner confirmation), pin the new token active. Commit to master state. No RED/ratchet needed for a ledger update."

## 2. Active token pin (immutable · SHA256-anchored)

| Field | Value |
|---|---|
| Artefact filename | `hf_token_rotated_20260914.csv` |
| Runtime custody path | `/app/backend/estate_keys/data_sources/hf_token_rotated_20260914.csv` |
| Workspace mirror | `/app/assessment_workspace/canon/drops/20260914_hf_token/hf_token.csv` |
| Mode (both copies) | `0600` (verified via `stat -c %a` 2026-09-14T~13:00Z) |
| Owner | `root:root` |
| Size | 37 bytes |
| SHA256 | `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5` |
| Content class | HuggingFace access token (single-line, `hf_`-prefix) |
| Received | 2026-09-14T12:23:58Z (attached to owner M5-open turn) |
| Manifest | `canon/drops/20260914_hf_token/manifest.json` (1193 B, 0644) |
| Injection contract | env-var only: `HUGGING_FACE_HUB_TOKEN` OR `HF_TOKEN`. Never printed. Never on a command line visible to `ps`. Never `head`/`cat`/`sed`/`awk` on the artefact. `wc -c` / `file` / `stat` only. |

## 3. Supersession chain

| Position | Artefact | State | SEC ID |
|---|---|---|---|
| pre-rotation | `hf_token.csv` (runtime + workspace) | LEAKED · SUPERSEDED | `SEC-2026-09-12-01` |
| rotated (this drop) | `hf_token_rotated_20260914.csv` | ACTIVE · re-leaked in-transcript same day; pending second owner-side rotation | `SEC-2026-09-14-04` |

The pre-rotation artefact stays on disk (mode 0600) so that (a) forensic evidence for `SEC-2026-09-12-01` is preserved and (b) the hardened loader can raise `HFTokenNotRotatedError` if a stale caller points at the old path.

## 4. SEC state transitions banked (2026-09-14)

| SEC ID | Prior state | New state (as of 2026-09-14) | Notes |
|---|---|---|---|
| `SEC-2026-09-12-01` | PENDING-OWNER-ROTATION | **OWNER-ROTATED-PENDING-CONFIRMATION** | Replacement artefact received + SHA-pinned + mode 0600. Confirmation = owner reply banking that the leaked value has been de-authorised on the HF side. |
| `SEC-2026-09-14-04` | (new · filed by main agent 2026-09-14T~12:24Z) | **PENDING-SECOND-ROTATION** | The rotated replacement itself was leaked via `head -1` on the artefact during registration inspection. Root cause: pre-inspection print without a content-shape guard. Owner-side rotation required post-close. Guard mechanism lands in the follow-on hardening wave (this file lists it as the WHY for that wave, not the mechanism itself.) |

Cross-reference: `notes/SEC_INCIDENTS_20260914.md` (main incident log, updated in parallel with this ledger).

## 5. Custody-path inventory (as of 2026-09-14T~13:00Z, via `stat` only — no `head`/`cat`)

`/app/backend/estate_keys/data_sources/`:

| File | Size | Mode | mtime | Purpose |
|---|---:|---|---|---|
| `hf_token_rotated_20260914.csv` | 37 | 0600 | 2026-09-14T12:24Z | ACTIVE HF token (this ledger) |
| `hf_token.csv` | 37 | 0600 | 2026-09-13T05:21Z | PRE-ROTATION (retained for forensic; loader must refuse) |
| `RMS_Connection_Creds.xlsx` | 9399 | 0600 | 2026-09-14T11:27Z | Estate creds (RMS network) — separate SEC scope |
| `db-restore-603-cluster.json` | 418 | 0600 | 2026-09-06T13:38Z | AWS RDS Data API creds (WPW campaigns) |
| `db_credentials.csv` / `db_credentials_2.csv` | 539 / 321 | 0600 | prior sessions | Legacy DB creds |
| `huawei_credentials.csv` | 119 | 0600 | 2026-09-11T18:27Z | Huawei OBS/RDS creds |
| `akki-aurora.json` · `aws_iam_user_AKIAXGH5.json` · `synthetic-nonexistent.json` · `x.json` | (various) | 0600 | prior sessions | Legacy custody files |

## 6. Rights-at-setup basis

Owner ruling 2026-09-14 verbatim (see §1 above): *"we have full rights on this data."* Interpretation: full ingestion + full-model-pull rights against the HF token. Does NOT relax:

* mode-0600 on disk
* env-var-only runtime injection
* transcript-leakage refusal (guard wave `test_secret_hygiene_hf_token_guard.py` — banked next)
* rotation obligation on future leaks

## 7. Downstream consumers (informational only — no code touched by this ledger update)

The rotated token becomes the ACTIVE credential for the M5 W-AUDIO-POC audio-plane HF-model pulls (transcription-gap fills against NAS `OFFAIRRECS` recordings for which OBS `google-transcripts` has no paired transcript). Consumers must import the loader banked by the hardening wave, never read the file directly.

## 8. What this ledger does NOT do

* Does not land the loader mechanism (that is the follow-on hygiene/hardening wave — see NEXT.md current-step marker).
* Does not modify `baseline_failures.json` (no ratchet; state-only).
* Does not touch `programme/track-a` (state-only, master-branch commit).
* Does not commit any secret value to git (both `.csv` files are outside repo trees, custody-only).
* Does not modify the pre-rotation artefact (retained for forensic).

## 9. Standing hygiene reminder (binding across sessions)

Inspecting any file under `estate_keys/data_sources/`:

* PERMITTED: `wc -c <path>`, `stat -c '%s %a %U:%G %y' <path>`, `file <path>`, `sha256sum <path>` (hash is safe; the value is not).
* BANNED: `cat`, `head`, `tail`, `less`, `more`, `sed 's|.*|&|' <path>`, `awk`, `python3 -c "print(open(...).read())"`, `xxd`, `od`, any `cp` that would land the artefact outside the custody root.
* BANNED: process-visible plaintext (`ps auxww` must never surface the value in `argv[]`). Use env var or askpass.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
