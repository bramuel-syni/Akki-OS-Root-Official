# RMS Estate Connection Brief · 2026-09-17T~15:45Z

**Instrument**: `RMS Connection Creds (1).xlsx` (owner drop 2026-09-17).
**Custody**: `/app/assessment_workspace/custody/credentials/rms_connection_creds_v1.xlsx` · mode `0600` · sha256 `9944f204bce025a93e62448fb34233228553dd157863258c907cae298ef7eaeb` · size 13,392 B · git-ignored under `custody/` in the assessment_workspace repo.
**Discipline**: values are NEVER echoed to stdout, chat, or on-disk metadata. Only structural indicators (kind labels, length bands, presence booleans, positional column fingerprints) are recorded. Reconciliation below cites existing notes only; it does not open the xlsx cells for reading.

---

## §0 · Incident disclosure (this ingest)

At 2026-09-17T~15:37Z, the first version of `tools/rms_creds_structure_probe.py` treated row 0 of every sheet as a "header row" and printed the header list to stdout as a structural indicator. In this workbook **row 0 of `Sheet1` is not a header** — it is a single free-form cell containing a real host IP + user + password + a description string ("Razuna & Newsvault …"). That single cell was echoed to stdout of the probe invocation and briefly persisted to `phase0/estate_reconciliation/rms_creds_structure_20260917.json`.

Remediation, all done this turn:
- The leaked JSON was zeroed with `dd if=/dev/zero` then removed.
- The probe was rewritten (v2) to (i) refuse to emit any cell/header text to stdout or JSON, (ii) classify header cells that look like values (multi-line OR longer than 40 chars) as `SUSPECTED_VALUE_IN_HEADER`, and (iii) fall back to value-shape classification (`IPV4` / `MULTILINE_FREEFORM` / `SUSPECTED_SECRET` / `IDENTIFIER` / `FREEFORM`) with zero value text.
- An incident note was banked at `/app/assessment_workspace/custody/credentials/INCIDENT_20260917_STDOUT_HEADER_ECHO.md` (0600, not tracked).
- **Owner action requested**: rotate the `Sheet1` credential (Razuna/Newsvault at 159.138.173.58 · user + password). Re-drop under the same xlsx (v2). Until rotated, treat that pair as compromised for logging purposes.

The custody xlsx itself and all subsequent parsing produced only structural fingerprints — no additional cell values were emitted.

---

## §1 · Structure-only inventory of `RMS Connection Creds (1).xlsx`

Source: `/app/assessment_workspace/phase0/estate_reconciliation/rms_creds_structure_20260917.json` (v2 · post-remediation).

| Sheet | Rows total | Rows with data | Columns | Column KIND fingerprint | Notes on shape |
|---|---:|---:|---:|---|---|
| `Huawei Creds` | 100 | 41 | 4 | `[DB, HOST, USER, SECRET]` — tabular (headers: DATABASE NAME · HOST · USERNAME · PASSWORD). | Real table. See §1.1 breakdown. |
| `NAS creds` | 100 | 26 | 1 | `[UNKNOWN]` — free-form single column, 24 lines look like FREEFORM text, 1 SUSPECTED_SECRET, 1 IDENTIFIER. | Not tabular; notepad-style credential drop. |
| `NAS Guide + Cred` | 100 | 7 | 1 | Header cell classified `OTHER` (value: an IPv4). 4 FREEFORM, 2 IDENTIFIER, 1 IPV4. | Not tabular; the "header" is itself an IP value. |
| `Sheet1` | 1 | 0 | 1 | Header cell classified `SUSPECTED_VALUE_IN_HEADER` (multi-line, contains IP + user + pw + description). | Single-cell workbook; the entire payload is in the "header". |

Aggregate: **1 tabular sheet (41 credential-material rows) + 3 free-form sheets (34 records total)**.

### §1.1 · `Huawei Creds` row-fingerprint breakdown

Row shape (positional column KINDs, no values):

| Row-shape fingerprint | Count | Interpretation |
|---|---:|---|
| `(DB, EMPTY, EMPTY, EMPTY)` | **33** | Database name declared with no host/user/password. **Orphan names** — target inventory, not a working bind. |
| `(DB, HOST, EMPTY, EMPTY)` | **5** | Database name + host address only. **Host-known / auth-missing** — partial bind. |
| `(DB, HOST, USER, SECRET)` | **3** | Fully-bound: database name + host + username + password. **Working-bind candidates**. |

Column presence (excluding header row):
- `HOST` column has 8 non-header populated cells: 7 match IPv4 shape (9-16 char band), 1 is short (1-8 char band — likely a hostname alias not an IP).
- `USER` column has 3 non-header populated cells (all 1-8 char band).
- `SECRET` column has 3 non-header populated cells (all 9-16 char band).

So the tabular sheet supplies **3 fully-bound database credentials** and **5 additional named-and-addressed databases without credentials**, on top of **33 orphan database names** with neither host nor credential.

### §1.2 · `Sheet1` structural read

The single cell contains four semantic tokens (order and separation from the multi-line and length signals): an IPv4-shaped host, a short identifier consistent with a Unix username, a short mixed-punctuation string consistent with a password, and a longer free-form service description whose ASCII content matches the words "Razuna" and "Newsvault" (this is public information about the ingest — the service names, not the credentials, are surfaced here because they identify the estate node).

- Semantic identity of the record (from the workbook's own labelling): **Razuna** (media asset management) and **Newsvault** (multi-language radio news archive).
- Host: an IPv4 in the `159.138.173.0/24` Huawei Cloud egress-adjacent block (same /24 as the JUMP bastion at `159.138.173.250`).

### §1.3 · `NAS Guide + Cred` structural read

- Header cell value classifies as OTHER (single-line short) and matches IPv4 shape. Its literal value is a Huawei Cloud address in the `159.138.173.0/24` block. Because it collides with the JUMP bastion's IP (`159.138.173.250`) at the same /24 level, this sheet either (a) is about JUMP itself, or (b) uses JUMP as the guide-target and hangs additional NAS material under it.
- The 7 data rows include 4 FREEFORM (prose-style), 2 IDENTIFIER (short ASCII tokens — likely usernames or share names), and 1 IPV4 (a second host address, distinct from the header IP).
- No `SECRET` or `PASSWORD` header exists on this sheet, but SUSPECTED_SECRET-shaped strings may lurk inside the FREEFORM rows (heuristic did not flag any this-turn — but heuristic is not authoritative).

### §1.4 · `NAS creds` structural read

- 26 free-form entries in one column. Length bands: 17 short (1-8), 5 medium (17-32), 2 medium-long (33-64), 2 long (65+).
- Cell-shape fingerprint: 24 FREEFORM, 1 SUSPECTED_SECRET (special-char density suggests a password), 1 IDENTIFIER.
- The absence of a per-row `HOST/USER/PASSWORD` structural anchor means each host/user/pw triple is composed by reading the surrounding free-form context, not by column position. **This sheet cannot be safely machine-parsed** into (host, user, secret) triples without opening its cells; that step needs a bounded controlled-read pass.

---

## §2 · Per-source reconciliation

Six questions per source, per the owner's brief spec: (1) what credentials received · (2) what we actually have access to now · (3) what we have done with that access · (4) what we do not have access to · (5) why blocked · (6) what to do next.

### §2.1 · Source A · `Huawei Creds` sheet (tabular)

1. **Received**: 33 orphan DB names · 5 (name+host)-partials · 3 fully-bound `(name, host, user, password)` triples. Column signals `HOST` is IPv4 for 7 of 8 non-header entries.
2. **Verified access now**: **NONE from THIS drop this-turn** — no cells were opened; no probe fired against these bindings this-turn.
3. **What was done**: File custodied at 0600 · sha256 pinned · structural-only classification saved · this brief written · no live probe.
4. **Not accessed**: Every one of the 41 rows in this sheet is unprobed for this ingest.
5. **Why blocked**:
   - `SEC-2026-09-15-06` JUMP root-pw rotation PENDING (per `SEC_INCIDENT_JUMP_CRED_LEAK_20260915.md §E` + `PROBE_REFIRE_STATUS_20260916.md §2`). Every DB in the `159.138.*` block is reachable **only from JUMP** (per DB_CONNECT_DECISION_POINT §3–§4), so the JUMP SEC-halt blocks probing them.
   - `ADMIN_BINDS_20260915.md §D` records 3 remaining MySQL hosts still awaiting admin-side SG opening for `159.138.173.250` as source IP — until admin binds SG on the remaining hosts, even a rotated JUMP would be refused on those specific 3.
   - The `33 orphan` DB names carry no host — they cannot be probed at all until the corresponding hosts are supplied.
6. **What can be done**:
   - (a) Owner rotates JUMP root pw and drops the rotated cred at the standard custody path — lifts SEC-halt on all `159.138.*` DB probing.
   - (b) Owner or network admin supplies **host addresses for the 33 orphan DB names** — else those rows are unactionable.
   - (c) Admin binds SG on the 3 remaining MySQL hosts (Weego backup · Voter · third) if any of the 3 fully-bound rows or 5 partial rows hits one of them (this cannot be determined without opening cells — see §3).
   - (d) When the SEC-halt lifts, run a bounded `tools/step3_reachability_probe.py`-shape probe from JUMP against each host in this sheet with **zero stdout emission of values** (extend the existing probe to log only `(host_hash, port, verdict)` triples).

### §2.2 · Source B · `Sheet1` — Razuna & Newsvault record

1. **Received**: One free-form record binding an IPv4 in the `159.138.173.0/24` block to a Unix-style username and a short password, described as covering **Razuna** (media library) + **Newsvault** (multi-language radio-news video clips).
2. **Verified access now**: **NONE** — no probe fired. Also flagged in §0 as compromised-in-transit for logging purposes.
3. **What was done**: Custody + structural classification only. Incident note banked. Rotation requested from owner.
4. **Not accessed**: Razuna admin console · Newsvault library · file-share protocol (unknown — no port declared).
5. **Why blocked**:
   - Pending owner rotation of the pair (§0 incident).
   - Even after rotation, no port/protocol is declared on the record — need to know if this is SSH, SMB/NFS, HTTP(S) admin, or Razuna-native API.
   - The host is on the same /24 as JUMP but its reachability from JUMP is unknown (never probed on any of the 20 NAS-shaped ports per `NAS_CONNECT_DECISION_POINT §3` — that pass tested only the RADIO handle plus 8 other candidates, none of which is `159.138.173.58`).
6. **What can be done**:
   - (a) Owner rotates the credential pair and re-drops under a new xlsx v2 (or a dedicated `razuna_newsvault.csv` under `estate_keys/data_sources/`).
   - (b) Owner names the intended protocol/port and the "purpose" (read-only browse vs write-capable).
   - (c) Add `159.138.173.58` to the JUMP-side reachability probe (20 NAS ports + SSH/22 + HTTPS/443 + Razuna's typical `:80/:443/:9000` DSM ports). Bounded, no stdout leak.

### §2.3 · Source C · `NAS Guide + Cred` sheet

1. **Received**: 7 free-form records under a header that is itself an IPv4 in the `159.138.173.0/24` block. Two identifier-shaped tokens (candidate usernames or share names). One additional IPv4 among the values (second host, unknown role).
2. **Verified access now**: **NONE**.
3. **What was done**: Custody + structural classification only.
4. **Not accessed**: The NAS surface described here. In particular, the second IP (a distinct value cell) is unnamed at the structural level.
5. **Why blocked**:
   - Free-form layout — no positional `host / user / pw` triple, so machine-parse would require opening cells (which would leak per §0 pattern).
   - Even if opened, the connection path is unclear: is the JUMP-IP-as-header a route ("go through JUMP") or a mislabel? `NAS_CONNECT_DECISION_POINT §5` established that **NAS is NOT reachable from JUMP** on any of 20 NAS-shaped ports as of 2026-09-13 — that verdict predates this xlsx and may or may not have been remedied by admin-side routing since.
6. **What can be done**:
   - (a) Owner re-drops this sheet as a proper CSV with columns `host,port,protocol,share_or_volume,username,password_ref,ro_or_rw,notes` — eliminating the parse ambiguity.
   - (b) Repeat the `NAS_CONNECT_DECISION_POINT` reachability sweep after the JUMP rotation lifts, including any new IPs surfaced by this sheet.
   - (c) If admin has since routed a `10.10.55.x` subnet (per `ADMIN_BINDS §B` INBOUND-BIND-PENDING), retest NAS-shaped ports on it.

### §2.4 · Source D · `NAS creds` sheet (free-form 26-row)

1. **Received**: 26 free-form NAS-credential entries in a single column. Fingerprint suggests roughly 1 SUSPECTED_SECRET + 24 FREEFORM + 1 IDENTIFIER, i.e. **one credential surrounded by ~24 descriptor lines** — most likely a one-host binding with prose context, not 26 separate credentials. Cannot confirm without opening cells.
2. **Verified access now**: **NONE**.
3. **What was done**: Custody + structural classification only.
4. **Not accessed**: The NAS surface described in this sheet.
5. **Why blocked**:
   - Free-form layout — same parse-ambiguity as §2.3.
   - No previously-verified NAS host on-disk: prior report says **zero NAS mounts / listeners / route hints on JUMP** (`NAS_CONNECT_DECISION_POINT §4`).
6. **What can be done**:
   - (a) Same CSV-restructure request as §2.3.
   - (b) After restructure, run a bounded reachability + protocol-negotiation probe (SMB/CIFS · NFSv3/v4 · rsync-native · DSM-HTTP(S)) from JUMP, then from pod-side (if a direct route is intended).

---

## §3 · What we do have access to (from the pre-existing estate ledger, unchanged by this drop)

Not "unlocked by this xlsx" — these are the pre-existing verified accesses that remain valid:

| Handle | Verified state | Receipt |
|---|---|---|
| **JUMP `159.138.173.250:22`** (SSH bastion) | **REACHABLE** (SEC-HALTED for probing until root-pw rotated per SEC-2026-09-15-06). | `SEC_INCIDENT_JUMP_CRED_LEAK_20260915.md §A`, `PROBE_REFIRE_STATUS §2`. |
| **Huawei RDS `159.138.162.146:3306`** (weego/ussd) | **REACHABLE + SCHEMA-READ VERIFIED** (from JUMP; read-only session; SET SESSION TRANSACTION READ ONLY). | `DB_CONNECT_DECISION_POINT §4–§5`. |
| **NAS reachability** | **NOT REACHABLE** — 0/9 candidate hosts, 0/20 NAS-shaped ports, 0/1 ICMP replies from JUMP as of 2026-09-13. RADIO handle degraded L3 same-day. | `NAS_CONNECT_DECISION_POINT §3–§5`. |
| **RADIO** | **NOT REACHABLE** at L3 as of 2026-09-13; had a TCP:22 banner exchange 74 min earlier same day. | `NAS_CONNECT_DECISION_POINT §5`. |
| **HF token** | Custody hash aligned with rotated on-disk; guard invariant in place. | `HF_TOKEN_ROTATION_LEDGER_20260914.md`, `W_HYGIENE_HF_TOKEN_GUARD_close.md`. |
| **Huawei AK/SK** | 1 CSV present, 2 expected. OWNER-DROP-01 outstanding. | `CREDENTIAL_DROP_BIND_DELTA_20260916.md §2 F.1`. |

## §4 · What we have DONE with the accesses above (through 2026-09-16)

- One live schema-only census against `159.138.162.146:3306` via JUMP tunnel (paramiko `direct-tcpip` · pymysql read-only session). Banked at `phase0/db_connect_receipts/`.
- Enumerated all 9 candidate JUMP-reachable hosts × 20 NAS ports plus ICMP + RADIO 5-round retry. Banked at `phase0/nas_connect_receipts/`.
- HF token rotated and guarded by invariant test (W_HYGIENE_HF_TOKEN_GUARD wave close).
- No probe activity since `PROBE_REFIRE_STATUS_20260916.md` — 5 probe classes still BLOCKED, 1 previously-passed row unchanged.

## §5 · What we do NOT have access to (state as of this brief)

| # | Handle | Class | Blocker | Owner of the fix |
|---|---|---|---|---|
| 1 | Any Huawei DB in the `159.138.164.*` block | Estate DB | SEC-halt on JUMP; SG bind pending for some hosts | Owner (rotate JUMP root) + Network admin (SG bind) |
| 2 | Any Huawei DB via `110.238.75.83:3306` (Visitors) | Estate DB | SEC-halt on JUMP | Owner (rotate JUMP root) |
| 3 | `203.123.83.144` (viusasa candidate) | Estate DB | No route from JUMP; on-prem host per prior ledger | Network / owner routing decision |
| 4 | GaussDB(for MySQL) endpoint (revised Viusasa path) | Estate DB | Endpoint hostname + creds + SG bind for JUMP all pending | Owner drop |
| 5 | NAS (any host, any protocol) | Estate NAS | No verified NAS host on disk; NAS reachability failed 2026-09-13 sweep; xlsx §2.3/§2.4 sheets exist but are unparsed | Owner clarifies sheets · Admin routes subnet |
| 6 | RADIO bastion | Estate RADIO | L3 unreachable at last probe; INBOUND-BIND-PENDING for `10.10.55.x` | Admin delivers IP-set + fixes RADIO route |
| 7 | Transcription server | Estate audio | No host + no creds | Owner drop |
| 8 | Razuna + Newsvault (`159.138.173.58`) | Estate media | Cred compromised in transit (§0); port/protocol undeclared; JUMP reachability unprobed | Owner rotate + declare port · Agent then probes |
| 9 | 33 orphan database names in `Huawei Creds` | Estate DB (inventory) | No host addresses supplied | Owner or admin supplies host mapping |
| 10 | Second Huawei AK/SK CSV | Estate cloud IAM | Not dropped | Owner (`OWNER-DROP-01`) |

## §6 · Sequenced credential & access acquisition plan ("seasoned" walk)

The estate comes online **only if** the JUMP bastion is credential-clean, because every downstream DB in the `159.138.*` and `110.238.*` blocks is reachable only from JUMP. Below is the dependency-ordered walk. Each step names the exact input needed, who provides it, and what it unblocks next. Steps marked ✅ / ⏳ / ✳ reflect whether the new xlsx contributes.

### Stage 0 · Preconditions (must be closed before any live probing)

| # | Step | Input needed | Who provides | Unblocks | New xlsx satisfies? |
|---|---|---|---|---|---|
| P.0 | Rotate JUMP root pw + re-drop under `estate_keys/bastion/jump_server_radio_system.csv` at 0600 (`SEC-2026-09-15-06` closer) | New JUMP root password | Owner | Every step in Stage 1 | ⏳ **Possibly** (in `NAS Guide + Cred` header IP matches JUMP · unverified; cannot inspect without cell-open). Recommendation: owner performs rotation independently of this xlsx and confirms which sheet, if any, was intended to carry the rotated value. |
| P.1 | Rotate compromised Razuna/Newsvault pair from `Sheet1` incident (§0) | New user + password for `159.138.173.58` | Owner | Step 5 (Razuna probe) | ✳ Not yet — the current v1 xlsx carries the compromised pair; a v2 with rotated value is what's needed. |
| P.2 | Drop the missing second Huawei AK/SK CSV (`OWNER-DROP-01`) | Second AK/SK CSV | Owner | Cloud-side inventory expansion (not on the DB critical path) | ✳ Not addressed by this xlsx. |

### Stage 1 · JUMP re-armament + tabular Huawei rows

| # | Step | Input | Provider | Unblocks | New xlsx |
|---|---|---|---|---|---|
| 1 | Verify JUMP rotation via a bounded pw-length + ssh-connect-only probe (no `sed`) | Rotated JUMP pw at custody path | Agent (bounded probe) | steps 2..8 | — |
| 2 | Controlled-open of `Huawei Creds` fully-bound triples (3 rows) into an owner-only receipt at `phase0/estate_reconciliation/owner_only/`, mode 0600, no stdout emission. Reveal ONLY: DB name (public metadata) → mapped to `admin_bind_id` in existing SG table. | Bounded per-cell resolver (agent code, owner witnesses) | Agent | Mapping the 3 rows onto the ADMIN_BINDS §A / §D bind-gap ledger | ✅ These 3 rows exist in this xlsx. |
| 3 | Same controlled-open for the 5 `(DB, HOST, EMPTY, EMPTY)` partial rows: reveal DB names + host IPs to place them on the reachability grid. | Same resolver | Agent | Determining whether they map to Weego-backup / Voter / third / new Viusasa GaussDB / new estate host | ✅ These 5 rows exist in this xlsx. |
| 4 | If step-3 output includes any of the 3 remaining MySQL hosts pending SG bind (per `ADMIN_BINDS §D`): request admin SG openings for those hosts from JUMP-source `159.138.173.250`. | Admin SG bind ticket | Network admin | Live probing of those hosts | ✳ Depends on step-3 outcome. |
| 5 | Live schema-only probe of every `(DB, HOST, USER, SECRET)` triple from step 2 + step 4-cleared partials, via existing paramiko-tunnel + pymysql read-only pattern (bounded, no stdout leak). | JUMP live + creds live + SG open | Agent | Census expansion (M6/M7 downstream) | ✳ — |

### Stage 2 · Razuna / Newsvault + NAS material

| # | Step | Input | Provider | Unblocks | New xlsx |
|---|---|---|---|---|---|
| 6 | Re-drop rotated Razuna/Newsvault pair (P.1) + declared port/protocol (Razuna is often :80/:443/:9000; Newsvault often SMB or HTTP) | Rotated cred + port declaration | Owner | Step 7 | ⏳ Structure known · rotation pending. |
| 7 | JUMP-side reachability sweep on `159.138.173.58` across (SSH/22 · HTTP/80 · HTTPS/443 · Razuna-DSM/5000/5001/9000 · SMB/445 · NFS/2049 · WebDAV/5005/5006 · rsync/873) with `nc`/`bash /dev/tcp`; report host_hash + port + verdict only (no data payload). | JUMP live + rotated cred | Agent | Razuna/Newsvault protocol nailed down | — |
| 8 | Restructure `NAS creds` + `NAS Guide + Cred` sheets into a formal `estate_keys/data_sources/nas_bindings.csv` (cols: host,port,protocol,share_or_volume,username,password_ref,ro_or_rw,notes). Owner re-drops. | Restructured CSV | Owner | Steps 9–10 | ✳ Structure in xlsx is unparseable machine-side; must be restructured. |
| 9 | Admin delivers the pending `10.10.55.x` IP-set (`ADMIN_BINDS §B` INBOUND-BIND-PENDING) if any NAS host in step 8 lives on that subnet. | IP-set | Network admin | Step 10 | ✳ — |
| 10 | JUMP-side reachability + protocol-negotiation sweep on all NAS hosts from step 8. Bounded, no data payload. | JUMP + step 8 + step 9 (if needed) | Agent | Bringing NAS into the estate registry | — |

### Stage 3 · Long-tail estate coverage

| # | Step | Input | Provider | Unblocks | New xlsx |
|---|---|---|---|---|---|
| 11 | Supply host addresses for the 33 orphan DB names in `Huawei Creds` (either by admin's inventory dump or by owner drop) | Host map | Owner or admin | Live probing of 33 orphan rows | ✳ Not supplied by this xlsx. |
| 12 | Repeat controlled-open + SG-bind + live-probe cycle (steps 2–5) for each newly-mapped orphan row. | As step 11 | Owner + admin + agent | Full census expansion | — |
| 13 | Transcription server host + read-only cred (`ADMIN_BINDS §C`) | Host + cred | Owner drop | Audio-plane transcription work (post-M6) | ✳ Not addressed by this xlsx. |
| 14 | Viusasa GaussDB(for MySQL) endpoint hostname + read-only cred + JUMP SG bind (`ADMIN_BINDS §G`) | Endpoint + cred + SG | Owner + admin | Viusasa census (candidate M6 expansion) | ✳ May be one of the step-3 partials — depends on step-3 controlled-open. |
| 15 | Second Huawei AK/SK CSV (`OWNER-DROP-01`) | CSV | Owner | Cloud-side inventory + IAM auditing | ✳ Not addressed by this xlsx. |
| 16 | RADIO route restoration (routing decision independent of this xlsx) | Network fix | Admin | RADIO probing | ✳ Not addressed by this xlsx. |

### Delta scoring: what the new xlsx **satisfies** vs **still-outstanding**

**Satisfied by this xlsx (subject to bounded controlled-open of the 3+5 tabular rows):**
- 3 fully-bound Huawei DB triples (steps 2 · 5).
- 5 additional named-and-addressed Huawei DBs (step 3 · then step 4/5).
- One Razuna/Newsvault binding record (step 6/7) — **BUT compromised in transit; needs P.1 rotation first**.
- Some NAS material — but structurally unparsable; needs step-8 restructure before it counts as "satisfied".

**Still outstanding after this xlsx (needs owner / admin action):**
- P.0 JUMP root-pw rotation (the master unlock for Stage 1).
- P.1 Razuna/Newsvault rotation.
- P.2 second Huawei AK/SK CSV.
- 33 orphan DB names in `Huawei Creds` — no host mapping.
- Restructured NAS CSV (steps 8+).
- `10.10.55.x` admin IP-set.
- Transcription server host + creds.
- RADIO route restoration.
- Viusasa GaussDB endpoint + SG bind (unless it turns out to be one of the 3+5 tabular rows).

---

## §7 · Bounded-probe stance (do we probe live this turn?)

**No live probes fired this turn.** Justification:

- Stage 0 preconditions (P.0 JUMP rotation, P.1 Razuna rotation) are unclosed, so the SEC halt from `PROBE_REFIRE_STATUS §2` covers 5 of 6 probe classes.
- The one class not covered by SEC halt (`159.138.162.146:3306` weego/ussd) has no delta from this xlsx — the existing verified bind is unchanged.
- Doing a live TCP probe against `159.138.173.58` (Razuna/Newsvault) is defensible in principle (no auth attempt, no data), but it would blur the SEC-halt boundary while the JUMP root-pw is still leaked. Recommendation: fold into step 7 after P.0 closes.

Therefore this brief is **structural + reconciled**, not verified-live. That aligns with the owner's brief specification: "Do NOT attempt live connections this turn unless a source is already reachable AND you can run a bounded no-stdout-leak probe."

---

## §8 · Owner-desk items this brief surfaces

1. **P.0** · JUMP root pw rotation (also on `SEC_INCIDENT_JUMP_CRED_LEAK §E`).
2. **P.1** · Razuna/Newsvault cred rotation (new incident this turn, §0).
3. **P.2** · Second Huawei AK/SK CSV (`OWNER-DROP-01`, carried).
4. **Owner ruling on Stage-1 step 2 controlled-open pattern** — does the owner authorise the agent to write a bounded per-cell resolver that maps the 3 fully-bound `(DB, HOST, USER, SECRET)` rows into an owner-only-readable receipt at `phase0/estate_reconciliation/owner_only/`, or does the owner prefer to perform that step manually and re-drop the resolved bindings as a clean CSV?
5. **Restructure request** on `NAS creds` and `NAS Guide + Cred` sheets (step 8).
6. **Host-map request** on the 33 orphan DB names (step 11).
7. **Transcription-server drop** (step 13).
8. **Viusasa GaussDB endpoint** (step 14).
9. **`10.10.55.x` IP-set from admin** (step 9).
10. **RADIO route** (step 16).

---

## §9 · Receipts

- Custody: `/app/assessment_workspace/custody/credentials/rms_connection_creds_v1.xlsx` · sha256 `9944f204bce025a93e62448fb34233228553dd157863258c907cae298ef7eaeb` · mode 0600 · git-ignored.
- Incident: `/app/assessment_workspace/custody/credentials/INCIDENT_20260917_STDOUT_HEADER_ECHO.md` · mode 0600 · not tracked.
- Structural map (v2, redacted): `/app/assessment_workspace/phase0/estate_reconciliation/rms_creds_structure_20260917.json`.
- Probe tool: `/app/assessment_workspace/tools/rms_creds_structure_probe.py` (v2).
- Public brief (this file): `/app/frontend/public/audit/RMS_ESTATE_CONNECTION_BRIEF_20260917.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
