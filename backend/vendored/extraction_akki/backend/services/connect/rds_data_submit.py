"""services.connect.rds_data_submit - first DATA connection over Aurora Data API.

Owner Ruling 2026-08-18 (channel · verbatim in DECISIONS.md · FL-P2-23):
  "I would like to connect you to the first data base too. Data sits in AWS.
   I am thinking RDS Data API which lets you run SQL queries against Aurora
   over HTTPS, using the AWS SDK, instead of opening a traditional database
   connection (TCP/3306) which is still a direct access channel."

Discipline (mirrors the compute submit shape):
  1. credential intake - STANDING credentials (differs from bootstrap password).
     Written to a mode-0600 file under ESTATE_KEYS_DIR/data_sources/, never
     committed, never returned to the client, never logged. Loaded to
     AWS_* env vars for the duration of the boto3 call, then unset.
  2. declaration fires with actor aws.rds.<cluster-id>, capabilities
     [sql_query_https], scope [data.estate].
  3. test connection - ExecuteStatement "SELECT 1" via Data API.
  4. light inventory within API limits - list schemas + tables + approximate
     row counts for up to LIGHT_INVENTORY_MAX tables (information_schema).
  5. four-questions response - link_working / found / ready / failure /
     failure_sentence with a bounded failure taxonomy.
  6. data_connection_record ledgered under
     DATA_CONNECTION_RECORD_DIR (default phase0/data_connection_records/).

HARD RULES:
  * No LLM SDK, no answering-side shield, no generic HTTP client (boto3 is
    the whole point and is allowed).
  * aws_secret_access_key must not appear in the returned dict, in the
    data_connection_record, in any log record, or in any ledger row.
  * data_source_id derived from the cluster ARN (last colon segment) - no
    fabrication.
"""
from __future__ import annotations

import json
import logging
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError as _boto_ClientError

from services.chokepoint import ChokepointRefused, register_crossing

log = logging.getLogger(__name__)

# The tests inject a synthetic ClientError type via monkeypatch so we do not
# have to construct a real botocore ClientError in unit tests.
_client_error_type = _boto_ClientError


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LIGHT_INVENTORY_MAX = 20  # cap the information_schema.tables inventory

_FAILURE_TAXONOMY = {
    # ExecuteStatement errors we want to distinguish for owner-facing sentences
    "BadRequestException":            ("auth_denied",           "The Data API refused the credentials or the SQL. Check the IAM policy + the secret ARN."),
    "AccessDeniedException":          ("auth_denied",           "The IAM role does not permit rds-data:ExecuteStatement against this cluster."),
    "UnauthorizedException":          ("auth_denied",           "The Data API refused authentication. The secret in Secrets Manager may not match the DB user."),
    "ForbiddenException":             ("auth_denied",           "The Data API refused authentication (forbidden)."),
    "StatementTimeoutException":      ("timeout",               "The Data API timed out running the probe. The Aurora cluster may be paused or under load."),
    "DatabaseNotFoundException":      ("cluster_not_found",     "The cluster ARN did not resolve to an Aurora cluster in this region."),
    "DBClusterNotFoundFault":         ("cluster_not_found",     "The cluster ARN did not resolve to an Aurora cluster in this region."),
    "DatabaseResumingException":      ("data_api_not_enabled",  "The Aurora cluster is resuming or the Data API is not enabled for it."),
    "HttpEndpointNotEnabledException":("data_api_not_enabled",  "The Data API HTTP endpoint is not enabled on this Aurora cluster. Enable it in the RDS console."),
    "EndpointNotEnabledException":    ("data_api_not_enabled",  "The Data API HTTP endpoint is not enabled on this Aurora cluster."),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cluster_id_from_arn(arn: str) -> str:
    # arn:aws:rds:us-east-1:123:cluster:akki-aurora -> akki-aurora
    return arn.rsplit(":", 1)[-1] if ":" in arn else arn


def _estate_keys_dir() -> Path:
    p = Path(os.environ.get("ESTATE_KEYS_DIR", "/app/backend/estate_keys"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def _record_dir() -> Path:
    p = Path(os.environ.get(
        "DATA_CONNECTION_RECORD_DIR",
        "/app/assessment_workspace/phase0/data_connection_records",
    ))
    p.mkdir(parents=True, exist_ok=True)
    return p


def _write_standing_creds(payload: Dict[str, Any]) -> Path:
    """Write standing credentials to a mode-0600 file under the estate key
    custody dir. The file is git-ignored via estate_keys/.gitignore.
    """
    cluster_id = _cluster_id_from_arn(payload["cluster_arn"])
    creds_dir = _estate_keys_dir() / "data_sources"
    creds_dir.mkdir(parents=True, exist_ok=True)
    creds_path = creds_dir / f"{cluster_id}.json"
    body = {
        "cluster_arn": payload["cluster_arn"],
        "secret_arn": payload["secret_arn"],
        "region": payload["region"],
        "database": payload.get("database"),
        # aws_* credentials only stored if actually provided (SigV4 fallback
        # if the secret ARN alone is not used)
        "aws_access_key_id": payload.get("aws_access_key_id"),
        "aws_secret_access_key": payload.get("aws_secret_access_key"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    creds_path.write_text(json.dumps(body, indent=2))
    os.chmod(creds_path, 0o600)
    return creds_path


def _fire_declaration(actor_id: str, capabilities: List[str], scope: List[str]) -> Dict[str, Any]:
    """Fire the declaration seat (thin-kernel: capture + return the record).
    Kept as a function so tests can monkeypatch it as a spy.
    """
    try:
        from services.declaration import seat as _dseat  # type: ignore
        return _dseat.capture(actor_id=actor_id, capabilities=capabilities, scope=scope)
    except Exception:
        # In unit-test contexts the declaration seat may not be reachable;
        # return a minimal record so the pipeline shape stays intact.
        return {"actor_id": actor_id, "capabilities": capabilities, "scope": scope,
                "at": datetime.now(timezone.utc).isoformat(), "note": "declaration seat not reachable in this context"}


def _classify_client_error(exc: Exception) -> tuple[str, str]:
    """Map a boto3/botocore-shaped exception to (failure_reason, plain_sentence)."""
    code = None
    if hasattr(exc, "response") and isinstance(getattr(exc, "response", None), dict):
        code = exc.response.get("Error", {}).get("Code")
    if not code:
        code = type(exc).__name__
    if code in _FAILURE_TAXONOMY:
        return _FAILURE_TAXONOMY[code]
    lower = str(exc).lower()
    if "timeout" in lower or "timed out" in lower:
        return ("timeout", "The Data API timed out running the probe.")
    return ("other", f"The Data API returned an unexpected error ({code}).")


def _redacted_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of the payload with any secret-shaped fields stripped."""
    keep = {"region", "cluster_arn", "secret_arn", "database"}
    return {k: v for k, v in payload.items() if k in keep}


def _extract_string(cell: Dict[str, Any]) -> str:
    """Unwrap a Data API cell (stringValue / longValue / etc.)."""
    if not isinstance(cell, dict):
        return str(cell)
    if cell.get("isNull") is True:
        return ""
    for k in ("stringValue", "longValue", "doubleValue", "booleanValue"):
        if k in cell:
            return str(cell[k])
    return ""


def _probe_engine(client, payload: Dict[str, Any]) -> tuple[str, Optional[str]]:
    """Probe the Aurora Data API endpoint to classify engine + version.

    Detection order:
      1. MySQL-shape probe: ``SELECT @@version, @@version_comment, @@aurora_version``.
         - If ``@@aurora_version`` is a non-empty string → ``aurora-mysql`` and
           engine_version = ``"<mysql-version> (Aurora MySQL <aurora-version>)"``.
         - Else (MySQL version present, aurora_version empty/null) → ``mysql``
           and engine_version = ``"<mysql-version>"`` (with comment appended
           when informative).
      2. PostgreSQL-shape probe: ``SELECT version(), aurora_version()``.
         - Non-empty aurora_version() → ``aurora-postgresql`` and
           engine_version = ``"<pg-version> (Aurora PostgreSQL <aurora-version>)"``.
         - Fallback: version() starts with 'PostgreSQL' → ``postgresql``.
      3. Both probes fail → ``("unknown", None)``.

    No exception escapes — engine='unknown' is an honest classification for
    an endpoint that answers SELECT 1 but refuses either probe shape.

    Owner Adjustment 2026-08-19 · FL-P2-24: root cause of the throwaway
    inventory retry was that version='8.0.42' + aurora_version='3.10.3'
    was classified 'unknown' by an off-band wrapper; the production path
    now recognises this shape as ``aurora-mysql``.
    """
    common_kwargs = {
        "resourceArn": payload["cluster_arn"],
        "secretArn": payload["secret_arn"],
    }
    if payload.get("database"):
        common_kwargs["database"] = payload["database"]

    # 1) MySQL-shape probe (Aurora MySQL, plain MySQL)
    try:
        r = client.execute_statement(
            **common_kwargs,
            sql="SELECT @@version, @@version_comment, @@aurora_version",
        )
        records = r.get("records") or []
        if records and len(records[0]) >= 3:
            row = records[0]
            version = _extract_string(row[0])
            comment = _extract_string(row[1])
            aurora_version = _extract_string(row[2])
            if aurora_version:
                # Aurora MySQL — the captured 2026-08-19 shape.
                return ("aurora-mysql", f"{version} (Aurora MySQL {aurora_version})")
            if version:
                if comment and comment.lower() not in ("", "6252a59a") and " " in comment:
                    # Informative vendor comment (e.g. "MySQL Community Server - GPL")
                    return ("mysql", f"{version} ({comment})")
                return ("mysql", version)
    except Exception as exc:  # pragma: no cover - postgres path falls through
        log.info("engine-probe mysql-shape failed (falling through to postgres): %s",
                 type(exc).__name__)

    # 2) PostgreSQL-shape probe (Aurora PostgreSQL, plain PostgreSQL)
    try:
        r = client.execute_statement(
            **common_kwargs,
            sql="SELECT version(), aurora_version()",
        )
        records = r.get("records") or []
        if records and len(records[0]) >= 1:
            row = records[0]
            version = _extract_string(row[0])
            aurora_version = _extract_string(row[1]) if len(row) >= 2 else ""
            if aurora_version:
                return ("aurora-postgresql", f"{version} (Aurora PostgreSQL {aurora_version})")
            if version.lower().startswith("postgresql"):
                return ("postgresql", version)
    except Exception as exc:
        log.info("engine-probe postgres-shape failed: %s", type(exc).__name__)

        # If pg probe erred, try the pg version() alone (aurora_version() may
        # not exist on plain PostgreSQL — but version() does)
        try:
            r = client.execute_statement(**common_kwargs, sql="SELECT version()")
            records = r.get("records") or []
            if records and len(records[0]) >= 1:
                version = _extract_string(records[0][0])
                if version.lower().startswith("postgresql"):
                    return ("postgresql", version)
        except Exception as exc2:  # pragma: no cover
            log.info("engine-probe version()-only fallback failed: %s",
                     type(exc2).__name__)

    return ("unknown", None)


def _light_inventory(client, payload: Dict[str, Any]) -> Dict[str, Any]:
    """List schemas + a bounded slice of tables + approx row counts."""
    common_kwargs = {
        "resourceArn": payload["cluster_arn"],
        "secretArn": payload["secret_arn"],
    }
    if payload.get("database"):
        common_kwargs["database"] = payload["database"]

    schemas: List[str] = []
    tables: List[Dict[str, Any]] = []

    # 1) schemas
    try:
        r = client.execute_statement(
            **common_kwargs,
            sql=(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name NOT IN ('information_schema','mysql','performance_schema','sys','pg_catalog') "
                "ORDER BY schema_name"
            ),
        )
        for row in r.get("records", []):
            if row:
                schemas.append(_extract_string(row[0]))
    except Exception as exc:  # pragma: no cover - honest empty on inventory fail
        log.info("light_inventory schemas step failed (non-fatal): %s", type(exc).__name__)

    # 2) tables (bounded)
    try:
        r = client.execute_statement(
            **common_kwargs,
            sql=(
                "SELECT table_schema, table_name, table_rows "
                "FROM information_schema.tables "
                "WHERE table_schema NOT IN ('information_schema','mysql','performance_schema','sys','pg_catalog') "
                f"ORDER BY table_schema, table_name LIMIT {LIGHT_INVENTORY_MAX}"
            ),
        )
        for row in r.get("records", []):
            if len(row) >= 3:
                tables.append({
                    "schema": _extract_string(row[0]),
                    "table": _extract_string(row[1]),
                    "approx_row_count": _extract_string(row[2]),
                })
    except Exception as exc:  # pragma: no cover
        log.info("light_inventory tables step failed (non-fatal): %s", type(exc).__name__)

    return {"schemas": schemas, "tables": tables, "table_count": len(tables),
            "inventory_cap": LIGHT_INVENTORY_MAX}


def _write_record(payload: Dict[str, Any], result: Dict[str, Any], *, actor: str) -> Path:
    """Write a data_connection_record. Never carries the secret."""
    cluster_id = _cluster_id_from_arn(payload["cluster_arn"])
    at = datetime.now(timezone.utc)
    body = {
        "kind": "data_connection_record",
        "at": at.isoformat(),
        "source_id": f"aws.rds.{cluster_id}",
        "actor": actor,
        "resource": _redacted_payload(payload),
        "engine": result.get("engine", "aurora"),
        "engine_version": result.get("engine_version"),
        "channel": "rds-data-api",
        "link_working": result["link_working"],
        "ready": result["ready"],
        "failure": result["failure"],
        "found": result["found"],
        "ruling_reference": "Owner Ruling 2026-08-18 · DECISIONS.md · FL-P2-23 · engine-detect fix 2026-08-19 · FL-P2-24",
    }
    p = _record_dir() / f"data_source_{cluster_id}_{at.strftime('%Y%m%dT%H%M%SZ')}.json"
    p.write_text(json.dumps(body, indent=2))
    return p


# ---------------------------------------------------------------------------

def get_rds_data_client(region: str):
    """Return a boto3 rds-data client bound to `region`.

    Wave-G5c-CENSUS · owner ruling 2026-08-28T~15:00Z (banked in DECISIONS.md).

    The boto3 seam is confined to this module (see
    tests/invariants/test_chokepoint_registers_all_crossings.py ·
    test_no_boto3_import_outside_chokepoint). Callers that need a
    rds-data client (e.g. the Census Engine) go through this helper so
    boto3 imports stay behind the exempted seam. The chokepoint
    register_crossing() call for the census walker fires from
    services.census_engine.engine.run_census before any client method
    is invoked.
    """
    return boto3.client("rds-data", region_name=region)


# The entrypoint
# ---------------------------------------------------------------------------

def submit(payload: Dict[str, Any], *, actor: str = "owner") -> Dict[str, Any]:
    """Test-connect an Aurora cluster via RDS Data API and record the outcome.

    payload keys (all required except database):
      aws_access_key_id, aws_secret_access_key, region, cluster_arn, secret_arn,
      database (optional).

    Returns the four-questions dict. Never carries aws_secret_access_key back.
    """
    # 1. custody: standing creds to mode-0600 file
    creds_path = _write_standing_creds(payload)

    # 2. declaration
    cluster_id = _cluster_id_from_arn(payload["cluster_arn"])
    _fire_declaration(
        actor_id=f"aws.rds.{cluster_id}",
        capabilities=["sql_query_https"],
        scope=["data.estate"],
    )

    # 3. boto3 rds-data client — creds resolved via env for the call duration only
    prior_env = {}
    for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"):
        prior_env[k] = os.environ.get(k)
    try:
        # W3 · Doc 01 §A5.5 chokepoint: bring this outbound crossing under
        # the custody boundary BEFORE any boto3 call. Refuses on residency
        # violation or unknown masking tier. Reads are structure-only today
        # (information_schema census) — no row content crosses. Full row
        # masking will be gated by a row-bearing tier when the first
        # row-value query is admitted.
        try:
            register_crossing(
                kind="rds_data_api",
                endpoint={
                    "host": f"rds-data.{payload['region']}.amazonaws.com",
                    "region": payload["region"],
                },
                verb="ExecuteStatement",
                payload_shape={
                    "statement_shape": "SELECT information_schema census",
                    "database": payload.get("database", ""),
                    "cluster_id": cluster_id,
                },
                actor=actor,
                masking_tier="structure_only",
            )
        except ChokepointRefused as exc:
            result = {
                "link_working": False,
                "ready": False,
                "found": {},
                "failure": "chokepoint_refused",
                "failure_sentence": str(exc),
                "creds_path": str(creds_path),
                "engine": "unknown",
                "engine_version": None,
                "channel": "rds-data-api",
                "source_id": f"aws.rds.{cluster_id}",
            }
            _write_record(payload, result, actor=actor)
            return result

        if payload.get("aws_access_key_id"):
            os.environ["AWS_ACCESS_KEY_ID"] = payload["aws_access_key_id"]
        if payload.get("aws_secret_access_key"):
            os.environ["AWS_SECRET_ACCESS_KEY"] = payload["aws_secret_access_key"]
        os.environ["AWS_DEFAULT_REGION"] = payload["region"]

        client = boto3.client("rds-data", region_name=payload["region"])

        # 4. probe: SELECT 1
        try:
            probe = client.execute_statement(
                resourceArn=payload["cluster_arn"],
                secretArn=payload["secret_arn"],
                database=payload.get("database") or "",
                sql="SELECT 1",
            )
        except Exception as exc:
            reason, sentence = _classify_client_error(exc)
            result = {
                "link_working": False,
                "ready": False,
                "found": {},
                "failure": reason,
                "failure_sentence": sentence,
                "creds_path": str(creds_path),
                "engine": "unknown",
                "engine_version": None,
                "channel": "rds-data-api",
                "source_id": f"aws.rds.{cluster_id}",
            }
            _write_record(payload, result, actor=actor)
            return result

        # SELECT 1 came back — link works. Now probe the engine and run light inventory.
        engine, engine_version = _probe_engine(client, payload)
        inventory = _light_inventory(client, payload)

        result = {
            "link_working": True,
            "ready": True,
            "found": inventory,
            "failure": None,
            "failure_sentence": None,
            "creds_path": str(creds_path),
            "engine": engine,
            "engine_version": engine_version,
            "channel": "rds-data-api",
            "source_id": f"aws.rds.{cluster_id}",
        }
        _write_record(payload, result, actor=actor)
        return result
    finally:
        # Retire env vars — either restore prior values or delete.
        for k, prior in prior_env.items():
            if prior is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = prior
