"""Authorised credential resolver — builds admitted connector custody for the
non-GPU census worker from the owner's registered estate.

This resolver is the control-plane side. It reads ONLY local, restricted-custody
inputs (the owner's estate credential file staged under estate_keys, mode 0600)
and produces a connector custody document, also mode 0600, under a gitignored
custody directory. It opens NO network connections itself — the actual source
read happens exclusively inside the non-GPU worker subprocess.

Source→driver bindings are fixed here (never inferred from a request body):
  rms_mysql  -> mysql_metadata, resolved from the RMS estate CSV.
DigiCow (digicow_rds/digicow_s3) and RMS object/broadcast archives resolve to a
native secret/identity that is not present in custody yet; they refuse with an
explicit reason code rather than fabricate a connection.
"""
import csv
import hashlib
import json
import os
import re
import stat
from pathlib import Path

from services.census_autonomy.operational_scope import SOURCE_TENANTS

MYSQL_SOURCE_DRIVER = {"rms_mysql": "mysql_metadata"}
_HOST_RE = re.compile(r"^(?:\d{1,3}(?:\.\d{1,3}){3}|[A-Za-z0-9.\-]+\.[A-Za-z]{2,})$")
_MYSQL_USER_TOKENS = {"bramuel"}  # RMS relational estate account (NAS uses a distinct account).


class ConnectorResolutionError(Exception):
    """Explicit refusal; carries a safe reason code and never a secret."""

    def __init__(self, reason_code):
        self.reason_code = reason_code
        super().__init__(reason_code)


def _custody_dir():
    root = Path(os.environ["AKKI_CENSUS_CONNECTOR_DIR"])
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    return root


def _open_restricted(path):
    if path.is_symlink():
        raise ConnectorResolutionError("ESTATE_CUSTODY_SYMLINK")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        raise ConnectorResolutionError("ESTATE_CUSTODY_UNREADABLE") from None
    with os.fdopen(fd, "r", newline="") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_size > 5 * 1024 * 1024:
            raise ConnectorResolutionError("ESTATE_CUSTODY_PERMISSIONS")
        return handle.read()


def _rms_mysql_connections(port):
    """Parse the RMS estate CSV into distinct MySQL connections + a status manifest."""
    csv_path = Path(os.environ["AKKI_RMS_ESTATE_CSV"])
    text = _open_restricted(csv_path)
    connections, manifest, seen = [], [], set()
    for cells in csv.reader(text.splitlines()):
        cells = [c.strip() for c in cells]
        user_idx = next((i for i, c in enumerate(cells) if c.lower() in _MYSQL_USER_TOKENS), None)
        if user_idx is None or user_idx + 1 >= len(cells):
            continue
        host = next((c for c in cells if _HOST_RE.match(c)), None)
        password = cells[user_idx + 1]
        db_label = cells[0] if cells and cells[0] else "?"
        status = next((c for c in cells if c.upper() in ("OK", "NOT YET UHURU")), "")
        if not host or not password:
            continue
        if host in seen:
            continue
        seen.add(host)
        connections.append({"host": host, "port": port, "user": cells[user_idx],
                            "password": password, "label": db_label})
        manifest.append({"label": db_label, "host_fingerprint": hashlib.sha256(host.encode()).hexdigest()[:12],
                         "estate_status": status or "unlabelled"})
    if not connections:
        raise ConnectorResolutionError("ESTATE_NO_MYSQL_CONNECTIONS")
    return connections, manifest


def resolve_connector(run_id, tenant, source, lawful_hash):
    """Write and return a 0600 connector custody file path for (tenant, source).

    Raises ConnectorResolutionError for sources whose native identity/secret is
    not yet in custody (e.g. DigiCow RDS needs AWS Secrets Manager resolution).
    Returns (connector_path, status_manifest).
    """
    if SOURCE_TENANTS.get(source) != tenant:
        raise ConnectorResolutionError("SOURCE_NOT_ADMITTED_TO_TENANT")
    if source not in MYSQL_SOURCE_DRIVER:
        # digicow_rds / digicow_s3 / rms_obs / rms_nas: native secret/identity absent.
        raise ConnectorResolutionError("NATIVE_SECRET_RESOLVER_UNAVAILABLE")
    port = int(os.environ.get("AKKI_RMS_MYSQL_PORT", "3306"))
    connections, manifest = _rms_mysql_connections(port)
    max_connections = int(os.environ["CENSUS_MAX_CONNECTIONS"])
    connections = connections[:max_connections]
    document = {"sources": {source: {"tenant_id": tenant, "lawful_basis_sha256": lawful_hash,
                                     "driver": MYSQL_SOURCE_DRIVER[source], "connections": connections}}}
    path = _custody_dir() / f"{run_id}-{source}.json"
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as handle:
        json.dump(document, handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    return path, manifest
