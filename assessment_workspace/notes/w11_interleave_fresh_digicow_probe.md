# W11 CP2+CP3 interleave · Fresh DigiCow probe + successful seal · 2026-08-26T08:10Z

Owner directive (verbatim, this session):
> "run a FRESH DigiCow verification probe yourself now via the existing
>  owner-signed connection (/api/connect/data-source against
>  aws.rds.db-restore-603-cluster.digicow_live) — the owner's rights
>  approval + connection signature from 2026-08-19 cover it; log the
>  crossing receipt through the chokepoint as usual. Then re-attempt the
>  test-set seal so it SUCCEEDS on freshly verified rows, and bank the
>  successful seal receipt."

## §1 · Fresh probe · 2026-08-26T08:09:58Z

Fired via `tools/fresh_digicow_probe.py` (in-process, bypassing HTTP · same
chokepoint + declaration + record-write path as `/api/connect/data-source`).
Credentials read from `/app/backend/estate_keys/data_sources/aws_iam_user_*.json`
(mode-0600 · owner-signed 2026-08-19 · never printed).

Chokepoint crossing registered (residency: `eu-west-1` allowlist) ·
declaration seat fired (`aws.rds.db-restore-603-cluster` · capabilities
`sql_query_https` · scope `data.estate`).

Probe result (verbatim, creds_path redacted):

```json
{
  "channel": "rds-data-api",
  "engine": "aurora-mysql",
  "engine_version": "8.0.42 (Aurora MySQL 3.10.3)",
  "failure": null,
  "failure_sentence": null,
  "found_summary": {
    "inventory_cap": 20,
    "schemas_count": 2,
    "tables_count": 20
  },
  "link_working": true,
  "ready": true,
  "source_id": "aws.rds.db-restore-603-cluster"
}
```

Data-connection record written at
`/app/assessment_workspace/phase0/data_connection_records/data_source_db-restore-603-cluster_20260826T080958Z.json`
· `link_working: true` · `at: 2026-08-26T08:09:58.456637+00:00`.

Note on `source_id`: the current `services.connect.rds_data_submit._cluster_id_from_arn()`
derives source_id from the cluster ARN only (`aws.rds.db-restore-603-cluster`),
not the historic 2026-08-19 form that appended `.digicow_live` (that was a
manual convention from an earlier hand-created record). The canonical form
is the one the current submit code emits; the seal accepts whatever the
fresh live probe wrote.

## §2 · Test-set seal · 2026-08-26T08:10:31Z

Re-fired against the fresh source_id:

```
POST /api/training/test-set-seal
{
  "objective_id": "obj/digicow/ussd-generation",
  "source_id": "aws.rds.db-restore-603-cluster",
  "target_table": "ussd_question_response",
  "strata": ["language.sw", "language.sw+en"],
  "sample_size": 1000
}
```

Response (verbatim):

```json
{
  "ok": true,
  "seal_id": "obj_digicow_ussd-generation__ussd_question_response__6a681df4006a",
  "manifest_sha256": "6a681df4006a7cb56f9a956688cfdf22b06204b4338792339ecf8f95809aa42e",
  "sealed_at": "2026-08-26T08:10:31.522040+00:00",
  "rds_link_verified_at": "2026-08-26T08:09:58.456637+00:00"
}
```

**Time between probe and seal: 33 seconds** · well within the 24-hour
freshness window.

Seal record persisted at
`/app/assessment_workspace/phase0/training/test_set_seals/obj_digicow_ussd-generation__ussd_question_response__6a681df4006a.json`.

## §3 · State rollup post-seal

```
GET /api/training/state
{
  "ship_state": "populated",
  "demand_tables": 1,   // obj/digicow/ussd-generation
  "capacity_ledger_rows": 0,   // empty at ship · fills at CP8 calibration probe
  "test_set_seals": 1   // ← this record
}
```

Owner now sees the full honest cycle on the `/training` surface:
1. Compile the demand table for the DigiCow USSD-generation objective (§4.1).
2. Attempt seal · **REFUSED** with the stale-cache reason (2026-08-19 record 7 days old).
3. Fresh live probe re-establishes verification.
4. Attempt seal again · **SUCCESS** with a deterministic manifest hash
   referencing the fresh live-verified `rds_link_verified_at` timestamp.

## §4 · Credential discipline (this session)

* `aws_access_key_id` and `aws_secret_access_key` were read from a
  mode-0600 file on disk into locals only.
* They were passed to `submit()` and never printed, never logged
  (the code's log calls emit only `type(exc).__name__` on error path),
  never committed.
* The probe result had `creds_path` stripped before print.
* No secret material appears in this note, in the data_connection_record,
  in the seal record, or in any git commit.

## §5 · CP8 preconditions status

| Precondition | Status | Note |
|--------------|:------:|------|
| Fresh DigiCow verification | ✅ DONE (2026-08-26T08:09Z) | This interleave. |
| DigiCow rights declaration | ✅ Owner-approved | Confirmed at W11 open. |
| SSH key for GPU VM | ⏳ AWAITING OWNER | "In transit" per this ratification. |
| Base-model census activation | ⏳ AWAITING OWNER | Owner names a specific Qwen3/Qwen3.5 or Llama member. |

CP8 remains BLOCKED on SSH key + census activation; DigiCow side is
green. **This interleave does not open CP8 — it only closes the
freshness question so the Owner sees the cycle succeed at /training.**
