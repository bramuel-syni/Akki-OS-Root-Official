"""Non-GPU census dispatch — the local-runtime counterpart to remote_dispatch.py.

remote_dispatch ships the census worker to an admitted GPU host over SSH. This
dispatcher runs the SAME kind of admitted worker as a bounded *local subprocess*
(the non-GPU worker), so the API/scheduler process only orchestrates and never
performs the source read itself. Selected via AKKI_CENSUS_EXECUTION_MODE.

Boundary: this function builds connector custody from local restricted inputs and
spawns the worker. All network/DB I/O happens in the spawned subprocess.
"""
import base64
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from services.census_autonomy.operational_validation import PROTOCOL
from services.census_autonomy import operational_store as store
from services.census_autonomy.estate_connector_registry import (
    resolve_connector, ConnectorResolutionError,
)

_WORKER = Path(__file__).with_name("non_gpu_census_worker.py")


def _worker_state_dir():
    root = Path(os.environ["AKKI_CENSUS_WORKER_STATE_DIR"])
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    return root


def _blocked(run_id, tenant, source, reason_code):
    return {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
            "source_id": source, "execution_location": "control_plane",
            "observed_at": store.now(), "status": "blocked", "worker_receipt_id": None,
            "source_rows_returned": 0, "reason_code": reason_code}


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    """Run the non-GPU worker for one admitted source; failures stay isolated."""
    remaining = int(deadline - time.time())
    if remaining <= 3:
        return _blocked(run_id, tenant, source, "BUDGET_EXHAUSTED")
    try:
        connector_path, manifest = resolve_connector(run_id, tenant, source, lawful_hash)
    except ConnectorResolutionError as exc:
        _bank(run_id, source, {"stage": "connector", "reason_code": exc.reason_code})
        return _blocked(run_id, tenant, source, "AKKI_CONNECTOR_" + exc.reason_code)

    state_dir = _worker_state_dir()
    detail_path = state_dir / f"{run_id}-{source}.detail.json"
    control = {"census_run_id": run_id, "tenant_id": tenant, "source_id": source,
               "lawful_basis_sha256": lawful_hash, "hostname_expected": socket.gethostname(),
               "max_seconds": max(1, remaining - 1),
               "max_databases": int(os.environ["CENSUS_MAX_DATABASES"]),
               "max_connections": int(os.environ["CENSUS_MAX_CONNECTIONS"])}
    encoded = base64.b64encode(json.dumps(control).encode()).decode()
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "AKKI_CENSUS_CONNECTOR_FILE": str(connector_path),
           "AKKI_CENSUS_STATE_DIR": str(state_dir),
           "AKKI_CENSUS_WORKER_DETAIL_FILE": str(detail_path)}
    try:
        completed = subprocess.run(
            [sys.executable, "-c", _WORKER.read_text(), encoded],
            capture_output=True, timeout=max(2, remaining), env=env, check=False)
        if completed.returncode != 0 or not completed.stdout.strip():
            _bank(run_id, source, {"stage": "worker", "reason_code": "WORKER_NO_RECEIPT"})
            return _blocked(run_id, tenant, source, "AKKI_EXECUTION_WORKER_NO_RECEIPT")
        result = json.loads(completed.stdout)
    except subprocess.TimeoutExpired:
        _bank(run_id, source, {"stage": "worker", "reason_code": "WORKER_DEADLINE"})
        return _blocked(run_id, tenant, source, "AKKI_EXECUTION_DEADLINE")
    except (ValueError, OSError):
        _bank(run_id, source, {"stage": "worker", "reason_code": "WORKER_MALFORMED"})
        return _blocked(run_id, tenant, source, "AKKI_EXECUTION_WORKER_MALFORMED")
    finally:
        try:
            connector_path.unlink()  # Connector custody is single-use; do not retain secrets.
        except OSError:
            pass

    detail = {}
    try:
        detail = json.loads(detail_path.read_text())
    except (OSError, ValueError):
        pass
    _bank(run_id, source, {"stage": "worker", "estate_manifest": manifest,
                           "worker_status": result.get("status"),
                           "connections_total": detail.get("connections_total"),
                           "connections_read": detail.get("connections_read"),
                           "connections": [{"label": c.get("label"), "estate_status": None,
                                            "status": c.get("status"),
                                            "reason_code": c.get("reason_code"),
                                            "database_count": c.get("database_count"),
                                            "table_count": c.get("table_count"),
                                            "row_count_estimate": c.get("row_count_estimate"),
                                            "schemas": c.get("schemas")}
                                           for c in detail.get("connections", [])]})
    return result


def _bank(run_id, source, payload):
    path = store.cursor_dir() / f"transport-{run_id}-{source}.json"
    body = {"census_run_id": run_id, "source_id": source, "at_utc": store.now(),
            "execution_location": "non_gpu_worker", **payload}
    path.write_text(json.dumps(body, indent=2))
