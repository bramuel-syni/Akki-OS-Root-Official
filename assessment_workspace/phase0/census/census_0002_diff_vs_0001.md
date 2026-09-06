# Census #2 · Owner-readable diff vs Census #1

**Fired:** 2026-09-06T09:35:28 UTC · **Finished:** 2026-09-06T09:36:54 UTC (86 s) · **Initiator:** owner (via POST /api/census/run)
**Registry surface confirms latest:** `/api/census/latest` returns `census_id=2` at query time.

## 1 · Headline (what changed since #1)

| Field | Census #1 (2026-08-28T15:49Z) | Census #2 (2026-09-06T09:36Z) | Delta |
|---|---:|---:|---:|
| Elapsed since #1 | — | — | **209.8 hours (~8.7 days)** |
| Databases visible to principal | 2 | 2 | **no change** (`digicow_live` + `ndume` — same set) |
| Tables (total across DBs) | 233 | 233 | **no change** |
| Total rows fleet-wide | 5,909,421 | 5,908,255 | **−1,166** (net) |
| Column-schema drift | — | — | **0 tables** (no columns added / removed anywhere) |
| Row-count drift | — | — | **15 tables** across both DBs (see §2) |
| `single_database_visibility_flag` | false | **false** | still confirms multi-DB visibility |
| New audio/media-shaped columns | — | **0** | none introduced since #1 |

**Product-language framing for the Registry status line:** *"Latest census: #2, read 2026-09-06. 2 connected sources, 233 tables held with 5,908,255 rows — 15 tables saw row-count churn since the previous census 8.7 days ago; no new tables or columns appeared, no databases dropped."*

## 2 · Row-count drift (15 tables) — full list

Signed delta (Census #2 minus Census #1). Positive = growth; negative = deletions/pruning.

### `digicow_live` (7 tables shifted)

| Table | Rows #1 | Rows #2 | Delta |
|---|---:|---:|---:|
| ussd_users | 2,286,019 | 2,285,336 | −683 |
| shortcode_questions_response | 400,373 | 400,122 | −251 |
| post_view | 293,777 | 293,709 | −68 |
| user_group_trainings | 163,793 | 163,753 | −40 |
| delete_log | 4,162 | 4,153 | −9 |
| users | 108,342 | 108,333 | −9 |
| post_location | 4,731 | 4,732 | **+1** |

### `ndume` (8 tables shifted)

| Table | Rows #1 | Rows #2 | Delta |
|---|---:|---:|---:|
| breedings_straw_logs | 5,956 | 5,896 | −60 |
| sms_log | 57,978 | 57,919 | −59 |
| breedings | 184,417 | 184,465 | **+48** |
| cows | 131,425 | 131,392 | −33 |
| calves | 475 | 482 | **+7** |
| tbl_farmer_vet | 75,382 | 75,376 | −6 |
| salary | 220 | 217 | −3 |
| healths | 24,032 | 24,031 | −1 |

**Reading:** the estate is a running production system — small write/delete churn across a handful of tables, no schema changes, no new data sources. The `delete_log` table on `digicow_live` shrunk by 9 rows over 8.7 days, which is itself a mild honest-empty datum (it's a log-of-deletions, so a shrinking `delete_log` is a strange finding — could be periodic vacuum). Not a finding to escalate; noted.

## 3 · Audit trail (Census #2)

**5 whitelisted SQL shapes** were run per database, in the same order as Census #1 — verifiable in `manifest.json.audit_trail`:
- `schemata_list` (once per estate)
- `tables_list` (once per database)
- `row_count` (once per database)
- `columns_list` (once per database)
- `null_count_per_column` (once per database)

No raw SQL exposed; every shape is on the fixed whitelist in `services/census_engine/engine.py::_ALLOWED_SQL_SHAPES`. Aggregates-only default held.

## 4 · Full artefact

Machine-readable diff (per-database, per-table, per-column): `/app/assessment_workspace/phase0/census/census_0002_diff_vs_0001.json`
