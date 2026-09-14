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

## Corrective actions taken this session (post-leak)

1. Rewrote the credential-loader with **strict deny-by-default position redaction**: every non-header cell renders `<value len=N>` unless explicitly whitelisted for host-shape or admin-guidance display.  See `tools/rms_creds_loader.py` `HostCred.describe()` / `MySQLCluster.describe()` / `NASSite.describe()`.
2. On JUMP: hygiene cleanup (shred `/root/.mysql_history`, shred `/root/.bash_history`; `/dev/shm` confirmed empty).  Receipt: `phase0/connectivity_receipts/20260914T114326Z_JUMP_hygiene_cleanup.json`.
3. For every future JUMP-side MySQL query, use `MYSQL_PWD` env var or `--defaults-file` (never `-p'<pw>'`) so the plaintext does not appear in process args.

## Owner-side follow-up

* Rotate NAS Bramwel account password (new SEC-2026-09-14-01).
* Rotate JUMP root password (SEC-2026-09-13-T4-04 / re-leak SEC-2026-09-14-02).
* Rotate RADIO ubuntu account password (SEC-2026-09-13-T4-03 / re-leak SEC-2026-09-14-03).
* Rotate any MySQL account cred values that appeared in the process-args warning of the JUMP-side mysql client output (mysql-client emitted a warning; the plaintext appeared briefly on JUMP's process table — session-transient, no persistence).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
