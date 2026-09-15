READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SEC incidents · 2026-09-14 · transcript credential-leak recurrence

Filed by main agent 2026-09-14T11:29Z during connectivity-redo task.  Owner instruction stands: *"rotation happens AFTER connection is established"* (owner directive 2026-09-14) — rotation is owner-side post-task; SEC items are on record and do not block work.

## Incidents

### `SEC-2026-09-14-01` (P0 · **new**)

* **Class**: transcript leak of NAS credential values.
* **Values leaked**: NAS user + NAS password (short-cell values from the "NAS creds" sheet · rows labelled "Username: …" and "password: …" in column c1 of a headerless mono-column layout).
* **Root cause**: my structural inspector in `tools/rms_creds_loader.py` had a fall-through branch that emitted any cell with `len < 30` under a "LABEL(...)" pretty-print, without checking whether the cell content matched credential-shape hints or whether the row's neighbouring cells labelled it as "password:" / "user:".  The header-keyword filter I wrote only guarded cells whose *column header* matched credential hints; monoline sheets fell through.
* **Same class as `SEC-2026-09-13-T4-04`**: this is a recurrence of the empty-header keyword-redaction miss originally recorded for the DB-password leak.  Bug pattern repeated.
* **Fix landed same message**: strict deny-by-default; every non-header cell now renders `<value len=N>` unless explicitly whitelisted.  `tools/rms_creds_loader.py` (persistent since first commit) already uses `HostCred.describe()` / `MySQLCluster.describe()` / `NASSite.describe()` which never emit values.
* **Blast radius**: transcript only (this session's transcript to owner); no leak to logs, receipts, files on disk.  Cred file itself lives at `/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx` mode 0600.

### `SEC-2026-09-14-02` (P0 · **re-leak of SEC-2026-09-13-T4-04**)

* **Class**: JUMP root password re-leaked in the same structural-inspection print.
* **Note**: previous SEC-T4-04 filed 2026-09-13 for the same value; still pending owner-side rotation.  My inspector reprinted it verbatim as part of the "NAS Guide + Cred" sheet dump.

### `SEC-2026-09-14-03` (P0 · **re-leak of SEC-2026-09-13-T4-03**)

* **Class**: RADIO password re-leaked in the same structural-inspection print.
* **Note**: previous SEC-T4-03 filed 2026-09-13 for the same value; still pending owner-side rotation.

### `SEC-2026-09-14-04` (P0 · **new · HF-token replacement re-leaked in-transcript**)

* **Class**: transcript leak of the rotated HF-token value.
* **When**: 2026-09-14T~12:24Z during registration of the owner-attached `hf_token_rotated_20260914.csv` drop.
* **Root cause**: I ran `head -1 /app/backend/estate_keys/data_sources/hf_token_rotated_20260914.csv` to "inspect" the file shape.  That command emits the file contents to stdout, which is captured verbatim into the session transcript.  The artefact is a single-line HF token, so the entire secret was echoed.
* **Class parallel to `SEC-2026-09-14-01/02/03`**: the SAME failure mode as the XLSX inspector — pre-inspection print without a content-shape guard.  `head`/`cat`/`sed` on a custody-root artefact is banned for exactly this reason; the ban was not enforced by a runtime guard yet, only by discipline, and discipline failed.
* **Blast radius**: transcript only (this session's transcript to owner).  No leak to logs, receipts, or files-on-disk.  The rotated artefact itself remains at mode 0600, custody-root only.
* **Ledger state**: `PENDING-SECOND-ROTATION` — owner-side rotation of THIS replacement token is required post-close (the token that was supposed to REPLACE the SEC-2026-09-12-01 leak is now itself leaked in-transcript).
* **Guard mechanism** to be landed as the next hardening wave (owner directive 2026-09-14, verbatim): *"authorized as a HARDENING INVARIANT (justified: 5+ recurrences)".*  Mechanism: `services/secret_hygiene/hf_token.py::assert_no_transcript_leak_of_active_token(text)` — raises `RuntimeError` if `text` contains the SHA-pinned active token value.  Plus `HFTokenEnvVarMissing` refusal so no path can silently `Path(...).read_text()` a custody artefact into a string that could round-trip to stdout.  Details banked in `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md` §4.

### `SEC-2026-09-12-01` — state transition (2026-09-14)

* **Prior state**: PENDING-OWNER-ROTATION (banked in every DECISIONS.md wave-close footer since 2026-09-12).
* **New state (as of 2026-09-14T~12:24Z)**: **OWNER-ROTATED-PENDING-CONFIRMATION**.
* **Basis**: owner attached the rotated replacement token to the M5-open turn (`canon/drops/20260914_hf_token/hf_token.csv` + `manifest.json`, SHA256 `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`, mode 0600).  Replacement received + SHA-pinned + custody-mode enforced.
* **Confirmation gate**: owner reply acknowledging that the leaked pre-rotation value has been de-authorised on the HF side (i.e. the leaked value can no longer pull models).  Until that reply lands, both artefacts remain on disk — the pre-rotation for forensic evidence and to let the hardened loader raise `HFTokenNotRotatedError` on stale-path callers.
* **Full record** at `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md`.

## Corrective actions taken this session (post-leak)

1. Rewrote the credential-loader with **strict deny-by-default position redaction**: every non-header cell renders `<value len=N>` unless explicitly whitelisted for host-shape or admin-guidance display.  See `tools/rms_creds_loader.py` `HostCred.describe()` / `MySQLCluster.describe()` / `NASSite.describe()`.
2. On JUMP: hygiene cleanup (shred `/root/.mysql_history`, shred `/root/.bash_history`; `/dev/shm` confirmed empty).  Receipt: `phase0/connectivity_receipts/20260914T114326Z_JUMP_hygiene_cleanup.json`.
3. For every future JUMP-side MySQL query, use `MYSQL_PWD` env var or `--defaults-file` (never `-p'<pw>'`) so the plaintext does not appear in process args.

## Owner-side follow-up

* Rotate NAS Bramwel account password (new SEC-2026-09-14-01).
* Rotate JUMP root password (SEC-2026-09-13-T4-04 / re-leak SEC-2026-09-14-02).
* Rotate RADIO ubuntu account password (SEC-2026-09-13-T4-03 / re-leak SEC-2026-09-14-03).
* Rotate the rotated-HF-token (SEC-2026-09-14-04 · **second rotation on the same secret**) once the follow-on hygiene-hardening wave lands its guard mechanism.  Confirm on the HF side that both the pre-rotation value AND the current-rotated value are de-authorised.
* Rotate any MySQL account cred values that appeared in the process-args warning of the JUMP-side mysql client output (mysql-client emitted a warning; the plaintext appeared briefly on JUMP's process table — session-transient, no persistence).

### `SEC-2026-09-15-05` (P1 · **new · owner-side transcript transmission**)

* **Class**: live credential transmission via owner chat transcript. Owner-authored, not agent-authored (distinct class from SEC-2026-09-14-01/02/03/04 which were agent-side transcript emissions; this class is owner-side transmission-mode).
* **Values transmitted**: MySQL shared credential (username: `bramuel`, password: `<12-char alphanumeric mixed case · sha256 a7a616be4577319d10387f15e2e6302e508f1cddc035d017dda8bd7d8717f70d · stored at /app/backend/estate_keys/data_sources/admin_bind_20260915_bramuel_cd_visitors.json mode 0600>`).
* **When**: 2026-09-15T~04:25Z owner turn.
* **Applies to**: MySQL hosts `citizen_digital` (159.138.164.103:3306) + `visitors` (110.238.75.83:3306).
* **Blast radius**: owner-chat transcript to agent. Value filed under position-redaction custody within the same session (mode 0600 · sha256-pinned · drop-manifest inline in file). Leak-guard sweep verifies zero occurrences in git-tracked workspace (`/app/assessment_workspace/`); one occurrence in the estate_keys custody file (expected · not git-tracked · not logged · not committed). NEVER echoed again in transcripts / receipts / notes / commit-messages going forward per owner directive verbatim: *"NEVER echo any part of it again in any transcript, receipt, or note — refer to it only by storage path + length"*.
* **Class parallel to `SEC-2026-09-14-01`**: owner-side transmission-mode is the mirror class of agent-side transcript-emission-mode. Both classes require post-verification rotation of the transmitted value on the credential-owning side.
* **Ledger state**: `PENDING-OWNER-ROTATION-POST-VERIFICATION`.
* **Owner rotation recommendation** (verbatim): *"recommend rotation once connectivity is confirmed, same class as prior SEC entries."*
* **Corrective standing**: no agent-side corrective mechanism needed (this class of leak originates outside the agent's control surface). The agent's file-then-forget custody discipline PASSED this turn (credential filed to estate_keys mode 0600 within the same turn as receipt; zero echo in any git-tracked artefact; owner's one-time DECISIONS.md-banking exception used with type+length redaction and now spent).

### `SEC-2026-09-15-05` ledger correction (2026-09-15T~04:25Z)

* **Class**: durable-ledger correction on `citizen_digital` public IP.
* **Prior stale value**: `159.138.164.124` (scratch files under `tools/_scratch/`).
* **Admin authoritative value**: `159.138.164.103`.
* **Correction landed**: `notes/ADMIN_BINDS_20260915.md` §A.
* **Not a SEC-class issue** (no credential leak); listed here alongside SEC-2026-09-15-05 so post-incident-scans surface the correction from the same anchor.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
