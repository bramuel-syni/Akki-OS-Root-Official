READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CREDENTIAL_DROP_BIND_DELTA_20260916.md · §E-compliant credential-drop ingestion · Path α clean · 2026-09-16T~19:10Z

**Discipline (SO §4.1 §E · owner ruling 2026-09-15T~22:30Z).** File-level metadata only. No `csv.reader` / `openpyxl.load_workbook` / `cat` / `head` / `tail` / `print` of raw values. Metadata computed via `hashlib` on raw bytes + `os.stat` primitives (equivalent to `sha256sum` + `stat` + `wc -l` — all explicitly listed as SAFE in `services/secret_hygiene/custody_file.py` lines 96–100 · this-shift use satisfies the guard by construction).

**Manifest banked at:** `phase0/credential_drop_manifests/20260916T1910Z_drop_manifest.json` (177 lines · 12 rows · shape-only fields per row).

**Custody surface inventoried:** `/app/backend/estate_keys/data_sources/` (mode 0700 · owner-only).

**Prior-pin source for reconciliation:** `notes/ADMIN_BINDS_20260915.md` §A (only durable-ledgered sha pin at boot).

---

## §1 · Bind-delta table (metadata-only · no raw values)

| # | File | Kind | Size (B) | Mode | mtime (UTC) | Line count (csv only) | Prior pin? | Class |
|--:|---|---|--:|---|---|--:|---|---|
| 1 | `RMS_Connection_Creds.xlsx` | xlsx zip | 9399 | 0600 | 2026-09-14T11:27:24Z | — | **absent** | NEW-ENTRY |
| 2 | `admin_bind_20260915_bramuel_cd_visitors.json` | json | 1321 | 0600 | 2026-09-15T07:03:22Z | — | present · matches | **UNCHANGED** |
| 3 | `akki-aurora.json` | json | 369 | 0600 | 2026-08-18T20:12:48Z | — | absent | NEW-ENTRY |
| 4 | `aws_iam_user_AKIAXGH5.json` | json | 300 | 0600 | 2026-08-19T13:12:35Z | — | absent | NEW-ENTRY |
| 5 | `db-restore-603-cluster.json` | json | 418 | 0600 | 2026-09-06T13:38:41Z | — | absent | NEW-ENTRY |
| 6 | `db_credentials.csv` | csv | 539 | 0600 | 2026-09-11T19:19:44Z | 27 | absent | NEW-ENTRY |
| 7 | `db_credentials_2.csv` | csv | 321 | 0600 | 2026-09-12T04:29:31Z | 21 | absent | NEW-ENTRY |
| 8 | `hf_token.csv` | csv | 37 | 0600 | 2026-09-13T05:21:52Z | 0 | absent | NEW-ENTRY |
| 9 | `hf_token_rotated_20260914.csv` | csv | 37 | 0600 | 2026-09-14T12:24:25Z | 0 | absent | NEW-ENTRY |
| 10 | `huawei_credentials.csv` | csv | 119 | 0600 | 2026-09-11T18:27:26Z | 1 | absent | NEW-ENTRY |
| 11 | `synthetic-nonexistent.json` | json | 359 | 0600 | 2026-08-25T19:21:22Z | — | absent | NEW-ENTRY (fixture) |
| 12 | `x.json` | json | 278 | 0600 | 2026-08-18T20:04:39Z | — | absent | NEW-ENTRY |

**sha256 pins are recorded per row in the JSON manifest** (177-line manifest at `phase0/credential_drop_manifests/20260916T1910Z_drop_manifest.json`). Values are file-level content addresses of raw bytes; they leak no field content by construction.

**Row counts:** 12 total · 1 UNCHANGED · 0 ROTATED · 11 NEW-ENTRY.

**Bind-delta reconciliation verdict:** §A bind is stable (admin JSON sha unchanged). Zero rotations detected in the reconciliation window because the durable ledger carried only one prior sha pin at boot. All other custody files land as NEW-ENTRY rows — durable-ledger sha pins for them will be added forward from this manifest.

---

## §2 · Wave-honest findings (absence-is-a-finding · SO §1)

### F.1 · Owner drop expected **two** Huawei AK/SK CSVs — only **one** present on disk

**Owner turn at compaction handoff (verbatim):** "credential-drop ingestion (files 1+2 Huawei AK/SK · file 3 RMS Connection Creds UPDATE — file already exists ...)"

**From-disk state at ingestion boundary (2026-09-16T~19:10Z):** `/app/backend/estate_keys/data_sources/` contains exactly **one** file matching the Huawei-credential shape — `huawei_credentials.csv` (119 bytes · 1 line · sha256 `8a14174c...` · mtime 2026-09-11T18:27:26Z). No second Huawei CSV present.

**Verdict:** the second Huawei AK/SK CSV expected by the owner drop is **NOT PRESENT** on the custody surface as of this ingestion. **This is a genuine absence per SO §1 · not silently papered over.** Two possibilities: (a) the second drop was expected but never landed on the pod filesystem; (b) the drop was consolidated into a single file. Neither can be resolved without owner input. Carry as **owner-desk item OWNER-DROP-01**.

### F.2 · `RMS_Connection_Creds.xlsx` has **no prior sha pin** in the durable ledger

**Owner turn framing:** "file 3 RMS Connection Creds UPDATE ... new drop is a rotation-check + delta authoring."

**From-disk state:** `RMS_Connection_Creds.xlsx` exists (9399 bytes · sha256 `d778eb1e...` · mtime 2026-09-14T11:27:24Z). No prior sha pin exists in `notes/ADMIN_BINDS_20260915.md` §A (or any other durable ledger — verified via `git grep` on `notes/` and `STATE/`).

**Verdict:** cannot perform rotation-check because no prior baseline exists. **This manifest establishes the baseline sha pin going forward.** Owner-desk item OWNER-DROP-02: bank a prior-state sha (if owner has it from admin-side) or accept this manifest's sha as the anchor.

### F.3 · `hf_token_rotated_20260914.csv` is **byte-identical** to `hf_token.csv`

**Sha256 both files:** `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`.

**Size both files:** 37 bytes exactly.

**Verdict:** the file-name rotation marker is not backed by a bytes-level change. Either (a) the rotation didn't actually change the token, or (b) both files carry the post-rotation value and the pre-rotation copy was overwritten. **Not a security incident by itself** — no leak, both files at mode 0600. Surface for owner attention as **owner-desk item OWNER-DROP-03**.

### F.4 · Multiple long-tail custody files carry **no prior sha pin** in the durable ledger

Nine JSON/CSV custody files (rows 3–12 excluding row 2) land as NEW-ENTRY in the reconciliation because the durable ledger recorded only one sha pin at ADMIN_BINDS_20260915 §A. Not a violation — the durable-ledger schema at that turn scoped to just the admin CD+Visitors bind. **This manifest becomes the forward baseline for all custody files.** Rotation reconciliations from now on can compare against `phase0/credential_drop_manifests/20260916T1910Z_drop_manifest.json`.

---

## §3 · Compliance proof (SO §4.1 §E)

- **No `cat`/`head`/`tail`/`less`/`more`/`bat`/`view`/`type`** on any custody path throughout this ingestion (grep-verifiable in ingestion tool `tools/credential_drop_manifest_20260916.py`).
- **No `csv.reader(open(...))` + `print(...)` co-occurrence** — ingestion reads files as raw bytes via `open(..., "rb")` + `hashlib`; no csv module imported.
- **No `openpyxl.load_workbook(...)` + `print(...)` co-occurrence** — the xlsx file is treated as opaque bytes (`kind = "xlsx_binary_zip"`); no xlsx parser imported.
- **No `set -x` / `bash -x` / `-o xtrace` co-occurring with credential-shaped env vars** — no shell tracing in the ingestion tool.
- **Emitted stdout on tool run** (2026-09-16T~19:10Z): only shape-level summary `rows=12 unchanged=1 rotated=0 new_entry=11` + the manifest path. No raw file values crossed stdout.

**Guard-invariant witness:** the ingestion tool source text at `tools/credential_drop_manifest_20260916.py` is amenable to review by `assert_no_transcript_cat_on_custody` + `assert_no_transcript_csv_header_emit_on_custody` + `assert_no_transcript_openpyxl_iter_rows_on_custody` + `assert_no_transcript_set_x_with_password_var` — all four assertions pass by construction (none of the banned patterns exists in the tool source).

---

## §4 · Owner-desk delta (three items surfaced this ingestion)

| # | Tag | Description | State |
|--:|---|---|---|
| 1 | OWNER-DROP-01 | Second Huawei AK/SK CSV expected but absent on custody surface | Owner-desk · surface at next report |
| 2 | OWNER-DROP-02 | RMS xlsx has no prior sha pin; this manifest establishes baseline | Owner-desk · accept-or-provide-prior-sha |
| 3 | OWNER-DROP-03 | `hf_token_rotated_20260914.csv` byte-identical to `hf_token.csv` | Owner-desk · low-severity |

---

## §5 · Next actions

- (i) **Huawei OBS wire-up** via env-injection using `huawei_credentials.csv` (single file present per F.1 above). Bounded shape-only validation call (list-bucket-metadata / HEAD) with receipt of status + counts + no secrets in stdout. Extension-not-proliferation: use existing `services/audio_poc/readonly_obs_guard.py` validator; no new client wrapper unless bounded validation forces one.
- (ii) **Probe re-fire** with the confirmed ADMIN_BINDS §A binds (CD `159.138.164.103:3306` · Visitors `110.238.75.83:3306`) since egress is OPEN and shared credential SHA `a7a616be...` UNCHANGED.
- (iii) **NAS + radio + transcription probes** remain BLOCKED per ADMIN_BINDS §B/§C (radio IPs INBOUND-BIND-PENDING · transcription server pending owner drop-in · no this-shift advance possible).
- (iv) Resume seal walk: **CP-M7-W9-UPGRADE-1** → M6 SEAL → CP-M8-CSD-1 → M8 SEAL + OVERALL BUILD STATUS.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
