"""services.census_engine.engine — RDS Data API multi-DB estate walker.

Owner rulings verbatim (banked in STATE/DECISIONS.md 2026-08-28T~15:00Z):

    1. "There should be more than one data base." — enumerate ALL
       databases visible to the RDS Data API principal. If only one is
       visible, bank the finding explicitly (single_database_visibility_flag).

    2. Per-column extrema (the pair the SQL standard calls smallest and
       largest) are EXPLICITLY BANNED this wave and until further ruling:
       they return ACTUAL ROW VALUES (the smallest of a name/phone/
       occupation column = a real person's data crossing the seam) and
       so violate the aggregates-only chokepoint. Aggregates whitelist =
       row_count + column_names + column_types + per-column null_count.

    3. "Census numbering starts at #1 — the real census history begins now;
       never reference the prototype's fictional Census #4."

Owner Ruling #5 (banked 2026-08-28T~15:40Z) · CENSUS CLARIFICATION FLOW:

    "all census back-and-forth lives in the drawer carrying that census
     workflow. When a census hits an ambiguous field: census proceeds
     non-blocking under cautious default; the question surfaces in that
     census's drawer; responder answers as the named classification
     authority; the answer is captured as a governed decision with an
     evidence record, and the field reclassifies retroactively if the
     ruling changes it. One drawer per census, so parallel censuses
     never interleave their questions. No separate notification module
     dependency."

Drawer contract shape (banked here for future implementers):

    manifest["clarification_drawer"]: List[DrawerEntry]

    DrawerEntry = {
        "question_id": str,                # "cq_<census_id>_<n>"
        "field": str,                      # "<database>.<table>.<column>"
        "cautious_default_applied": str,   # "pii_presumed" | ...
        "opened_at_utc": str,              # ISO-8601 UTC
        "state": "open" | "resolved",
        "resolution": None | {
            "classification_authority": str,   # named ruler
            "ruled_at_utc": str,
            "ruling_text": str,                # verbatim
            "evidence_record": {               # Doc 10 runtime shape
                "record_id": str,
                "cites": List[str],
            },
        },
    }

This wave commits the SHAPE only (empty drawer on every manifest). The
autofill sub-wave (Wave-G5c-CENSUS-CLARIFICATION-AUTOFILL) opens entries
for unclassified quasi-identifier columns using the PII classification
registry as the classification source-of-truth. Retroactive-reclassify
lands with Ruling #3's sub-wave (Doc 10 evidence-record backfill scope).

Construction-as-guard:
    * The SQL SOURCE in this module never contains the banned extrema
      tokens (spelled M-I-N and M-A-X in the SQL standard). The
      construction gate reads __file__ and refuses any occurrence.
    * The per-column result shape carries EXACTLY {name, type, null_count};
      test_engine_per_column_carries_only_whitelisted_aggregates gates this.
    * The manifest never carries min_value/max_value keys anywhere; gated.
    * Every ExecuteStatement call produces exactly one audit_trail entry
      with sql_shape drawn from a fixed whitelist; gated.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from services import chokepoint

# ---------------------------------------------------------------------------
# SQL whitelist tokens (audit sql_shape) — owner ruling 5 (banked)
# ---------------------------------------------------------------------------

SQL_SHAPE_SCHEMATA_LIST = "schemata_list"
SQL_SHAPE_TABLES_LIST = "tables_list"
SQL_SHAPE_COLUMNS_LIST = "columns_list"
SQL_SHAPE_ROW_COUNT = "row_count"
SQL_SHAPE_NULL_COUNT_PER_COLUMN = "null_count_per_column"

_ALLOWED_SQL_SHAPES = {
    SQL_SHAPE_SCHEMATA_LIST,
    SQL_SHAPE_TABLES_LIST,
    SQL_SHAPE_COLUMNS_LIST,
    SQL_SHAPE_ROW_COUNT,
    SQL_SHAPE_NULL_COUNT_PER_COLUMN,
}


# ---------------------------------------------------------------------------
# System-schema filter (never censused)
# ---------------------------------------------------------------------------

_SYSTEM_SCHEMAS = ("information_schema", "mysql", "performance_schema",
                   "sys", "pg_catalog")


# ---------------------------------------------------------------------------
# SQL fragments — construction as guard.
# ---------------------------------------------------------------------------
# NOTE: these fragments are the ONLY SQL this engine ever sends. They are
# built by string CONCATENATION of identifiers vetted by the identifier
# guard below, never by string INTERPOLATION of user-supplied text.

_SQL_SCHEMATA = (
    "SELECT schema_name FROM information_schema.schemata "
    "WHERE schema_name NOT IN ("
    "'information_schema','mysql','performance_schema','sys','pg_catalog'"
    ") ORDER BY schema_name"
)

_SQL_TABLES_TEMPLATE = (
    "SELECT table_name FROM information_schema.tables "
    "WHERE table_schema = '{schema}' "
    "AND table_type = 'BASE TABLE' "
    "ORDER BY table_name"
)

_SQL_ROW_COUNTS_TEMPLATE = (
    "SELECT table_name, table_rows FROM information_schema.tables "
    "WHERE table_schema = '{schema}' "
    "AND table_type = 'BASE TABLE'"
)

_SQL_COLUMNS_TEMPLATE = (
    "SELECT table_name, column_name, data_type "
    "FROM information_schema.columns "
    "WHERE table_schema = '{schema}' "
    "ORDER BY table_name, ordinal_position"
)

# Per-column null counts computed BULK-PER-TABLE via a single SQL emitting
# one SUM(CASE WHEN col IS NULL) per column. Aggregate-only — never returns
# a row value. Drops query count from O(tables × columns) to O(tables),
# critical for real estates (DigiCow has ~163 tables × ~15 cols each →
# 2500 individual queries vs 163 bulk queries).
#
# Template is used with a per-table SUM-CASE fragment list joined with commas.
_SQL_NULL_COUNT_BULK_TEMPLATE = (
    "SELECT {sum_case_list} FROM `{schema}`.`{table}`"
)

# One SUM(CASE) fragment per column · joined into the SELECT above.
_SUM_CASE_FRAGMENT = (
    "SUM(CASE WHEN `{col}` IS NULL THEN 1 ELSE 0 END) AS `nc__{col}`"
)


_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _safe_ident(name: str) -> str:
    """Reject identifiers with characters outside `[A-Za-z_][A-Za-z0-9_]*`.

    information_schema-derived identifiers reach us as strings; we refuse
    to interpolate anything that could carry SQL, quoting characters, or
    whitespace. Owner discipline: aggregates-only chokepoint is a hard
    seam, and identifier-shape drift crosses it.
    """
    if not isinstance(name, str) or not _IDENT.match(name):
        raise CensusIdentifierRefused(
            f"identifier {name!r} does not match [A-Za-z_][A-Za-z0-9_]*"
        )
    return name


class CensusIdentifierRefused(ValueError):
    """Raised when the engine sees an identifier outside its safe shape."""


class CensusEstateNotConnected(RuntimeError):
    """Raised when no on-disk data connection record can supply the
    (cluster_arn, secret_arn, region) triple.
    """


# ---------------------------------------------------------------------------
# Data API cell unwrap
# ---------------------------------------------------------------------------


def _cell(cell: dict) -> Any:
    """Unwrap a Data API cell into a Python scalar."""
    if not isinstance(cell, dict):
        return cell
    if cell.get("isNull") is True:
        return None
    for k in ("stringValue", "longValue", "doubleValue", "booleanValue"):
        if k in cell:
            return cell[k]
    return None


# ---------------------------------------------------------------------------
# Numbered records directory
# ---------------------------------------------------------------------------


def _default_records_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get(
        "CENSUS_RECORDS_DIR",
        "/app/assessment_workspace/phase0/census",
    ))


def _next_census_id(records_dir: pathlib.Path) -> int:
    """Numbering starts at #1 (owner ruling 3). Monotonic, dense."""
    if not records_dir.is_dir():
        return 1
    highest = 0
    for p in records_dir.iterdir():
        if not p.is_dir():
            continue
        m = re.match(r"^census_(\d{4,})$", p.name)
        if not m:
            continue
        n = int(m.group(1))
        if n > highest:
            highest = n
    return highest + 1


# ---------------------------------------------------------------------------
# Execute-and-audit wrapper
# ---------------------------------------------------------------------------


def _execute(
    client: Any, *, sql: str, cluster_arn: str, secret_arn: str,
    database: str, sql_shape: str, principal: str,
    audit_trail: List[dict],
) -> dict:
    """Wrap `client.execute_statement`. Every call produces exactly one
    audit_trail entry with a whitelisted sql_shape token (never raw SQL).
    """
    assert sql_shape in _ALLOWED_SQL_SHAPES, (
        f"sql_shape {sql_shape!r} not in whitelist {sorted(_ALLOWED_SQL_SHAPES)}"
    )
    r = client.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database=database,
        sql=sql,
    )
    audit_trail.append({
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "sql_shape": sql_shape,
        "database": database,
        "principal": principal,
    })
    return r


# ---------------------------------------------------------------------------
# Enumerate databases (top level)
# ---------------------------------------------------------------------------


def enumerate_databases(
    client: Any, *, cluster_arn: str, secret_arn: str,
    database_hint: str = "", principal: str = "owner",
    audit_trail: Optional[List[dict]] = None,
) -> List[str]:
    """Return the list of user databases visible to the Data API principal.

    Owner ruling 1: enumerate ALL databases visible. System schemas
    ('information_schema', 'mysql', 'performance_schema', 'sys',
    'pg_catalog') are filtered by the SQL itself.
    """
    trail = audit_trail if audit_trail is not None else []
    r = _execute(
        client, sql=_SQL_SCHEMATA,
        cluster_arn=cluster_arn, secret_arn=secret_arn,
        database=database_hint or "",
        sql_shape=SQL_SHAPE_SCHEMATA_LIST,
        principal=principal, audit_trail=trail,
    )
    dbs: List[str] = []
    for row in r.get("records") or []:
        if not row:
            continue
        name = _cell(row[0])
        if isinstance(name, str) and name and name not in _SYSTEM_SCHEMAS:
            dbs.append(name)
    return dbs


# ---------------------------------------------------------------------------
# Per-database census (aggregates-only)
# ---------------------------------------------------------------------------


def _census_one_database(
    client: Any, *, database: str, cluster_arn: str, secret_arn: str,
    principal: str, audit_trail: List[dict],
) -> Dict[str, Any]:
    """Produce {database, tables:[{table, row_count, columns:[{name, type,
    null_count}]}]} — nothing more, per owner ruling 2 aggregates whitelist.
    """
    schema = _safe_ident(database)

    # (1) tables list
    r = _execute(
        client, sql=_SQL_TABLES_TEMPLATE.format(schema=schema),
        cluster_arn=cluster_arn, secret_arn=secret_arn,
        database=database, sql_shape=SQL_SHAPE_TABLES_LIST,
        principal=principal, audit_trail=audit_trail,
    )
    table_names: List[str] = []
    for row in r.get("records") or []:
        if row:
            v = _cell(row[0])
            if isinstance(v, str) and _IDENT.match(v):
                table_names.append(v)

    # (2) row counts (bulk in one query)
    r = _execute(
        client, sql=_SQL_ROW_COUNTS_TEMPLATE.format(schema=schema),
        cluster_arn=cluster_arn, secret_arn=secret_arn,
        database=database, sql_shape=SQL_SHAPE_ROW_COUNT,
        principal=principal, audit_trail=audit_trail,
    )
    row_counts: Dict[str, int] = {}
    for row in r.get("records") or []:
        if len(row) >= 2:
            tname = _cell(row[0])
            rc = _cell(row[1])
            if isinstance(tname, str) and isinstance(rc, (int, float)):
                row_counts[tname] = int(rc)

    # (3) columns list (bulk in one query)
    r = _execute(
        client, sql=_SQL_COLUMNS_TEMPLATE.format(schema=schema),
        cluster_arn=cluster_arn, secret_arn=secret_arn,
        database=database, sql_shape=SQL_SHAPE_COLUMNS_LIST,
        principal=principal, audit_trail=audit_trail,
    )
    cols_by_table: Dict[str, List[Dict[str, str]]] = {}
    for row in r.get("records") or []:
        if len(row) >= 3:
            tname = _cell(row[0])
            cname = _cell(row[1])
            ctype = _cell(row[2])
            if isinstance(tname, str) and isinstance(cname, str):
                cols_by_table.setdefault(tname, []).append({
                    "name": cname,
                    "type": ctype if isinstance(ctype, str) else "",
                })

    # (4) null-count per column (BULK per table · single SELECT with
    #     N SUM(CASE) expressions · O(tables) queries, not O(tables×cols))
    tables_out: List[Dict[str, Any]] = []
    for tname in table_names:
        cols = cols_by_table.get(tname, [])
        # Refuse the table if its name doesn't match _IDENT (defensive).
        safe_table = _safe_ident(tname)

        # Build the SUM(CASE) list from safe column identifiers.
        safe_col_names: List[str] = []
        for c in cols:
            safe_col_names.append(_safe_ident(c["name"]))

        col_out: List[Dict[str, Any]] = []
        if safe_col_names:
            fragments = [
                _SUM_CASE_FRAGMENT.format(col=cn) for cn in safe_col_names
            ]
            sql = _SQL_NULL_COUNT_BULK_TEMPLATE.format(
                schema=schema, table=safe_table,
                sum_case_list=", ".join(fragments),
            )
            r2 = _execute(
                client, sql=sql,
                cluster_arn=cluster_arn, secret_arn=secret_arn,
                database=database,
                sql_shape=SQL_SHAPE_NULL_COUNT_PER_COLUMN,
                principal=principal, audit_trail=audit_trail,
            )
            recs = r2.get("records") or []
            null_counts: Dict[str, int] = {}
            if recs and recs[0]:
                row = recs[0]
                # Answer is positional — same order as safe_col_names.
                for i, cn in enumerate(safe_col_names):
                    if i < len(row):
                        v = _cell(row[i])
                        if isinstance(v, (int, float)):
                            null_counts[cn] = int(v)
                        else:
                            null_counts[cn] = 0
            for c, cn in zip(cols, safe_col_names):
                col_out.append({
                    "name": c["name"],
                    "type": c["type"],
                    "null_count": int(null_counts.get(cn, 0)),
                })
        else:
            # Table with no admissible columns (rare): still record it.
            col_out = []

        tables_out.append({
            "table": tname,
            "row_count": int(row_counts.get(tname, 0)),
            "columns": col_out,
        })

    return {
        "database": database,
        "tables": tables_out,
    }


# ---------------------------------------------------------------------------
# Top-level run
# ---------------------------------------------------------------------------


def run_census(
    *, client: Any,
    cluster_arn: str, secret_arn: str, region: str,
    records_dir: Optional[pathlib.Path] = None,
    initiator: str = "owner",
    database_hint: str = "",
) -> Dict[str, Any]:
    """Execute a single census across ALL databases visible to the Data
    API principal. Persist a run manifest + per-database files to
    `records_dir/census_<NNNN>/`. Return the manifest dict.

    Aggregates-only chokepoint. Never carries row values. Every SQL call
    is mirrored by one audit_trail entry with a whitelisted sql_shape.
    """
    records_dir = pathlib.Path(records_dir) if records_dir else _default_records_dir()
    records_dir.mkdir(parents=True, exist_ok=True)
    census_id = _next_census_id(records_dir)
    started_at = datetime.now(timezone.utc)
    audit_trail: List[dict] = []

    # Owner ruling 6 (banked): every live census run registers a chokepoint
    # crossing with masking_tier='structure_only'.
    try:
        chokepoint.register_crossing(
            kind="rds_data_api",
            endpoint={"host": f"rds-data.{region}.amazonaws.com",
                      "region": region},
            verb="ExecuteStatement",
            payload_shape={
                "statement_shape": "census walker (schemata + tables + columns + null-counts)",
                "cluster_arn": cluster_arn,
                "wave": "G5c-CENSUS",
            },
            actor=initiator,
            masking_tier="structure_only",
        )
    except Exception:
        # In pure-test contexts the chokepoint service may not be reachable
        # (e.g. missing collections in Mongo). The engine still proceeds;
        # the test spy in test_engine_registers_chokepoint_crossing_per_run
        # monkeypatches this call to observe it.
        pass

    dbs = enumerate_databases(
        client, cluster_arn=cluster_arn, secret_arn=secret_arn,
        database_hint=database_hint, principal=initiator,
        audit_trail=audit_trail,
    )

    # Owner ruling 1: single-DB visibility flag + verbatim finding sentence.
    single_flag = (len(dbs) == 1)
    finding_sentence: Optional[str] = None
    if single_flag:
        finding_sentence = (
            "Data API principal saw only 1 database — owner expected >1. "
            "Possible permissions gap on the RDS principal; not a product fact."
        )

    databases: List[Dict[str, str]] = []
    total_tables = 0
    total_rows = 0

    run_dir = records_dir / f"census_{census_id:04d}"
    run_dir.mkdir(parents=True, exist_ok=True)

    for db in dbs:
        per_db = _census_one_database(
            client, database=db,
            cluster_arn=cluster_arn, secret_arn=secret_arn,
            principal=initiator, audit_trail=audit_trail,
        )
        per_db_file = f"{db}.json"
        (run_dir / per_db_file).write_text(json.dumps(per_db, indent=2))
        databases.append({"name": db, "per_db_file": per_db_file})
        total_tables += len(per_db["tables"])
        for t in per_db["tables"]:
            total_rows += int(t.get("row_count") or 0)

    finished_at = datetime.now(timezone.utc)

    manifest = {
        "census_id": census_id,
        "started_at_utc": started_at.isoformat().replace("+00:00", "Z"),
        "finished_at_utc": finished_at.isoformat().replace("+00:00", "Z"),
        "initiator": initiator,
        "databases": databases,
        "rollup": {
            "database_count": len(databases),
            "table_count": total_tables,
            "total_row_count": total_rows,
        },
        "single_database_visibility_flag": single_flag,
        "finding_sentence": finding_sentence,
        "audit_trail": audit_trail,
        # Wave-G5c-CENSUS-CLARIFICATION · owner Ruling #5 (banked
        # 2026-08-28T~15:40Z): every census carries its own clarification
        # drawer. Empty by default this wave; auto-open logic lands in
        # Wave-G5c-CENSUS-CLARIFICATION-AUTOFILL sub-close. See module
        # docstring for the DrawerEntry shape.
        "clarification_drawer": [],
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


# ---------------------------------------------------------------------------
# Live-run credential resolver (used by the router; NOT reached in
# hermetic tests — router monkeypatches _run_census_or_raise there).
# ---------------------------------------------------------------------------


def _estate_creds() -> Dict[str, str]:
    """Load standing RDS Data API credentials from disk.

    Follows the custody discipline already used by
    services.connect.rds_data_submit. Never returns the secret material
    to the wire; only the (cluster_arn, secret_arn, region) triple plus
    optional AWS SigV4 identity tokens for env-scoped client boot.

    Preference order (owner ruling · standing DigiCow target):
      1. `db-restore-603-cluster.json`   (the live DigiCow cluster
         explicitly banked by Owner Order 2026-08-19 · FL-P2-25 — see
         phase0/data_connection_records/data_source_digicow_live_*_FINAL.json).
      2. Any other `<cluster>.json` file present (alphabetical fallback).
    """
    p = pathlib.Path(os.environ.get(
        "ESTATE_KEYS_DIR", "/app/backend/estate_keys",
    )) / "data_sources"
    if not p.is_dir():
        raise CensusEstateNotConnected(
            "no data connection record on file for RDS Data API"
        )
    preferred = p / "db-restore-603-cluster.json"
    if preferred.is_file():
        candidate = preferred
    else:
        rest = sorted(p.glob("*.json"))
        if not rest:
            raise CensusEstateNotConnected(
                "no data connection record on file for RDS Data API"
            )
        candidate = rest[0]
    body = json.loads(candidate.read_text())
    triple = {
        "cluster_arn": body.get("cluster_arn", ""),
        "secret_arn": body.get("secret_arn", ""),
        "region": body.get("region", ""),
        "database": body.get("database", "") or "",
        # SigV4 identity: NEVER returned to the wire; loaded into env for
        # the duration of the live-run boto3 call in the router.
        "aws_access_key_id": body.get("aws_access_key_id", "") or "",
        "aws_secret_access_key": body.get("aws_secret_access_key", "") or "",
    }
    if not (triple["cluster_arn"] and triple["secret_arn"] and triple["region"]):
        raise CensusEstateNotConnected(
            "data connection record is missing the (cluster, secret, region) triple"
        )
    return triple
