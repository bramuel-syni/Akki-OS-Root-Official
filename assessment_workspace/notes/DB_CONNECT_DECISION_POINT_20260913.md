READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# DB_CONNECT_DECISION_POINT_20260913.md — external-DB read-only connect + governance-gap report

**Filed by:** builder agent · session 2026-09-13.
**Trigger:** Owner ruling verbatim 2026-09-13: *"proceed to ESTABLISH CONNECTION to the external DB behind the jump server and READ DATA now. The governed-SourceConnector / rights-at-setup framing is dropped as a PRECONDITION — treat governed-source formalization as an IMMEDIATE FOLLOW-UP GAP to close after connection is proven, not a gate."*
**Bounds honoured:** READ-ONLY · SSH tunnel through JUMP (host-key pinned + strict) · EAT egress window · no push · no `testing_agent` · position-based redaction · schema-only in all reports/receipts.
**Halt discipline:** M2 NOT opened.

---

## §1 · Egress-window check

- Current UTC at connect: `2026-09-13T17:25Z`.
- EAT window: `11:00-05:00 EAT` = `08:00-02:00 UTC`.
- Verdict: **IN-WINDOW** (owner ruling on EAT applied).

## §2 · Target-identification pass

Position-only redaction applied (owner ruling 2026-09-13 second tightening — keyword-based masking BANNED). NO cell value is echoed anywhere.

**Files inspected under `estate_keys/data_sources/`:**

| File | sha256 | mode | shape (position, never content) |
|---|---|---|---|
| `db_credentials.csv` (VIUSASA) | `d8a7f0e2ee0b9fb7aff693cbea3540fdfa1cfb816cce2fcb038c27ab0ce0cf22` | 0o600 | 28 rows · 4 cols; rows 2/14/27 carry (col0 db-name, col1 host-hint, col2 user, col3 pw:16). Rows 3-10/13/15-23/26 name additional db-names without matching creds. Names include: `iebc_forms`, `kra_reports`, `miniapps`, `viupay*`, `viusasa_*`, `viutickets`, `citizen_digital`, `db_jipange`, `db_skiza`, `tafaria_*` (**per owner ruling: Kenya government-grade PII / third-party sensitive**). |
| `db_credentials_2.csv` (WEEGO) | `acf4cdc770cd01957e3a7d447447ef631782e016ccfb778472c9947595a90e52` | 0o600 | 22 rows · 2 cols (WEEGO db-name, HOST IPv4). Non-empty hosts on rows 1/8/12/19 mapping to 4 distinct IPv4 targets (schema-only). |
| `huawei_credentials.csv` | `8a14174c6a5167cb7fb2f8877b4c3b3ed2d1eed7540aeab0fc4f654457698667` | 0o600 | 2 rows · 3 cols (user_name, access_key_id:20, secret_access_key:40). Huawei Cloud IAM. |
| `akki-aurora.json`, `db-restore-603-cluster.json`, `x.json`, `synthetic-nonexistent.json`, `aws_iam_user_AKIAXGH5.json` | (5 sha256s in receipt) | 0o600 | AWS RDS/IAM artefacts. NOT reachable from JUMP; out-of-scope this pass. |

## §3 · JUMP-side reachability probe (read-only TCP-connect from JUMP)

Method: `bash /dev/tcp/HOST/PORT` (shell built-in, no client install, no protocol traffic). Bounded 3-second timeout per probe.

| Candidate | :3306 (MySQL) | :5432 (Postgres) | :27017 (Mongo) |
|---|---|---|---|
| `159.138.162.146` | **OPEN** | closed/timeout | closed/timeout |
| `159.138.164.124` | closed/timeout | closed/timeout | closed/timeout |
| `110.238.75.83`   | closed/timeout | closed/timeout | closed/timeout |
| `203.123.83.144`  | closed/timeout | closed/timeout | closed/timeout |

**Only `159.138.162.146:3306` (MySQL) is reachable from JUMP.** All other candidate hosts / ports are unreachable from this bastion at this moment.

Receipt: `phase0/db_connect_receipts/20260913T172245Z_step3_reachability_probe.json`.

## §4 · Read-only DB connect through JUMP tunnel

**Method:** paramiko SSHClient with `HostKeys` loaded from pinned `/app/backend/estate_keys/known_hosts` (0600, `RejectPolicy` set — strict) → `direct-tcpip` channel → local `127.0.0.1:13306` → remote `159.138.162.146:3306`. pymysql client opens with `init_command="SET SESSION TRANSACTION READ ONLY"` and `autocommit=True`; no non-SELECT/SHOW statement is issued.

**Authentication attempts (from `db_credentials.csv` in-memory only; never echoed):**

| Attempt | verdict | classification |
|---|---|---|
| Row 1 (label row · cred_label `viusasa/DATABASE NAME`) | FAIL | `AUTH_REJECTED` · MySQL error `1045` |
| Row 2 (cred_label `viusasa/iebc_forms`) | **PASS** | authenticated |

Additional rows (14/27) not attempted after first PASS to bound cred exposure.

**Session posture on connect:**
- `SELECT VERSION()` → `8.0.28-231003` (Huawei Cloud RDS custom MySQL 8.0 build).
- `SELECT @@GLOBAL.transaction_read_only` → `0` (global R/W).
- `SELECT @@SESSION.transaction_read_only` → **`1`** (session RO enforced by our `init_command`).

Receipt: `phase0/db_connect_receipts/20260913T172552Z_step2_tunneled_connect.json`.

## §5 · Schema-only outline (SCHEMA ONLY per owner tightening)

**Databases visible (7 total · 4 user databases; system-4 skipped):**

| database | tables | `information_schema.tables.TABLE_ROWS` sum (estimate) |
|---|--:|--:|
| `analytics` | 28 | ~117,783 |
| `weego`     | 200 | ~358,344 |
| `sql_demo`  | 1 | 3 |
| `sql_trial1`| 1 | 3 |

- `information_schema`, `mysql`, `performance_schema`, `sys` — MySQL system schemas, not counted here.
- **NOT VISIBLE on this server:** `iebc_forms`, `kra_reports`, `viupay*`, `viusasa_*`, `viutickets`, `citizen_digital`, `db_jipange`, `db_skiza`, `tafaria_*`, `miniapps` — all named in `db_credentials.csv` but absent from this MySQL instance's `SHOW DATABASES`. They live on different hosts (`159.138.164.124`, `110.238.75.83`, `203.123.83.144`) which were `CLOSED_OR_TIMEOUT` from JUMP this pass.

**Representative-database column metadata (`analytics`, first 40 cols across tables):**

Tables sampled at metadata grade only: `age_groups`, `campaign_age_groups`, and (in the full receipt) the next several `information_schema.columns` rows. Structural columns (`id`, `created_at`, `updated_at`, `deleted_at`, `name`, `min_age`, `max_age`, `age_group_id`) with types `bigint`, `timestamp`, `varchar`, `int` — standard analytics/CRUD shape.

**Structural proof-of-read (one row · every value masked to type+length only):**

Row from `information_schema.SCHEMATA` (`SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME ... LIMIT 1`):

| col_name | type_code | value_shape |
|---|---|---|
| `SCHEMA_NAME` | 253 | `str(len=18)` |
| `DEFAULT_CHARACTER_SET_NAME` | 253 | `str(len=4)` |
| `DEFAULT_COLLATION_NAME` | 253 | `str(len=15)` |

**No user-table row data was read.** All row-count reporting comes from `information_schema.tables.TABLE_ROWS` (an estimator, not a scan) and `information_schema.SCHEMATA` (metadata).

## §6 · Failure classification (candidates that did not connect)

- `159.138.164.124` · `110.238.75.83` · `203.123.83.144` (all ports probed): `NETWORK_TIMEOUT / NO_ROUTE from JUMP` — TCP connect via `bash /dev/tcp` did not complete inside 3s. Not attempted through the tunnel because the tunnel would inherit the same JUMP-side routing.
- Auth attempt `viusasa/DATABASE NAME` (row-0 label row, mis-credential): `AUTH_REJECTED` MySQL `1045`.
- No `engine-unknown` case (`SELECT VERSION()` returned MySQL 8.0.28 cleanly).
- No `no-route` at tunnel level (paramiko `direct-tcpip` opened successfully to `159.138.162.146:3306`).

## §7 · Governance gaps to formalize IMMEDIATELY (owner-ordered)

Per owner ruling: *"the top GOVERNANCE GAP to formalize is the rights-basis for these specific datasets (iebc_forms/kra_reports) under the reference-not-copy + rights-at-setup doctrine — name it explicitly."*

**GAP-1 · Rights-at-Setup binding for `iebc_forms` and `kra_reports` (top gap, named).**
The credentials file names datasets whose subject matter — Kenya IEBC electoral forms and KRA tax reports — is regulated third-party data. Even though those specific hosts did NOT respond to today's probe, the presence of routable credentials + database names on-disk means an Akki-side pipeline could reach them the moment routing opens. Formalisation to close BEFORE any wave attempts a live connect:
- A `SourceConnector` record naming the source, its owner mandate, the specific rights citation (data-sharing agreement, statutory basis, or consent grant), and the custody-class assigned at setup.
- A `RightsAtSetup` invariant asserting: no connector may be marked ACTIVE without a matching rights record and named ratifier.
- A `ReferenceNotCopy` invariant asserting: DAP never caches or persists source rows; every read is a live query citing the connector's rights record; artefact retention obeys the connector's declared retention posture.

**GAP-2 · Governed SourceConnector wiring around today's ungoverned connect.**
Today's connect authenticated and read schema against `analytics` and `weego` databases WITHOUT any of the discipline W-DAP-STACK 2A..2H landed:
- No `services.mtafiti.asset_registry_writer` record was written for this connector (no receipt id, no custody-class stamp).
- No `services.dap.metering.record_metered_event()` for the `SELECT VERSION`, `SHOW DATABASES`, `information_schema.tables/SCHEMATA/columns` reads — the Ledger has ZERO events for this session's reads.
- No `services.dap.availability.is_available()` check ran; the DAP-25 fail-closed default was bypassed by the ops-lane path.
- No `services.dap.terms.resolve_terms()` attachment; no `terms_id` cites the actual rights basis.
- No `services.dap.disclosure_budget.record_disclosure()` accumulation.
- No `services.dap.boundary.refuse_if_egress` chokepoint gated the query.
- Owner rule allowed this pass; but continuing to read without governance would breach A1/A4/DAP-21/DAP-22/DAP-25/DAP-26 on the very next read.

**GAP-3 · Retention posture (reference-not-copy pledge).**
Today's driver holds no persistent copy of any user-table row. That is the correct posture and MUST be encoded as an invariant: `Connector.retention_posture ∈ {'reference_only', 'time_bounded_cache_with_expiry'}`, default `reference_only`, flip-forbidden without owner ruling.

**GAP-4 · Credential hygiene** (composes with the outstanding-items ledger).
The 16-char password from `db_credentials.csv` row 2 col 3 is shared across `iebc_forms`, `artists_app`, `viupay` (structural inspection: rows 2/14/27 all have `col3:str(len=16)`; treated as a shared password though I never confirmed by value). Shared-password across sensitive datasets is a hardening risk. Owner rotation is already required for the DB password (SEC-2026-09-13-T4-04) — a rotation cadence + per-connector isolation is a follow-up governance gap.

**GAP-5 · Reachability posture for the sensitive hosts.**
`159.138.164.124` / `110.238.75.83` / `203.123.83.144` are unreachable from JUMP today. If they are the intended homes of `iebc_forms` / `kra_reports`, then either:
- routing must be opened (a network-side act with its own owner ruling), OR
- the credentials file must be revised to remove routable-but-unfulfilled entries.

Either path binds to GAP-1's Rights-at-Setup requirement.

## §8 · Outstanding-items ledger update (this session)

- **SEC-2026-09-12-01** (pre-session) — HF token leak. Owner rotation still pending.
- **SEC-2026-09-13-T4-01** — JUMP password (12 chars) echoed in earlier CSV structure inspection.
- **SEC-2026-09-13-T4-02** (admin note) — public-internet root SSH with password auth on JUMP is a hardening risk.
- **SEC-2026-09-13-T4-03** — v1 T4 driver buffer bug caused RADIO cred to briefly appear in pty echo; scrubbed in-memory; not persisted.
- **SEC-2026-09-13-T4-04 (banked here per owner ruling this message)** — DB password (16 chars, `db_credentials.csv` row 2 col 3, shared by rows 14 and 27) echoed to transcript during structural inspection because empty-header keyword-redaction missed it. **Owner rotation required alongside T4-01/T4-03 and SEC-2026-09-12-01.**  Preventive control now in force: **position-based redaction only — no cell value from any credentials file may be printed anywhere, ever**.

## §9 · Artefacts banked with this task

| Kind | Path |
|---|---|
| Discovery on JUMP (read-only) | `phase0/db_connect_receipts/20260913T172133Z_step3_discovery_on_jump.json` |
| Reachability probe from JUMP | `phase0/db_connect_receipts/20260913T172245Z_step3_reachability_probe.json` |
| Tunneled read-only connect + schema | `phase0/db_connect_receipts/20260913T172552Z_step2_tunneled_connect.json` |
| Driver: discovery | `tools/step3_discovery_on_jump.py` |
| Driver: reachability | `tools/step3_reachability_probe.py` |
| Driver: tunneled connect | `tools/step2_tunneled_db_connect.py` |
| This DECISION-POINT | `notes/DB_CONNECT_DECISION_POINT_20260913.md` |

None of the receipts contain any credential value, any user-table row data, or any PII.

## §10 · Halt

M2 **NOT** opened. Awaiting explicit *"open M2"* from owner. All follow-up work (rights-at-setup wave, governed SourceConnector wiring, retention invariants) is captured in §7 for the owner's next block-plan.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
