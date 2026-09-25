"""Exclusive, durable intent before the explicitly authorized SSH diagnostic."""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from services.training_runner import ssh_seam


def _write_exclusive(path, payload):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as handle:
        json.dump(payload, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def run_once(diagnose):
    directory = Path(os.environ["AKKI_RECOVERY_DIAGNOSTIC_DIR"]).resolve()
    boundary = Path("/app/assessment_workspace").resolve()
    if directory == boundary or not directory.is_relative_to(boundary):
        raise ValueError("DIAGNOSTIC_DIRECTORY_NOT_ADMITTED")
    digest = os.environ["AKKI_RECOVERY_WORKBOOK_SHA256"]
    if not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError("WORKBOOK_DIGEST_REQUIRED")
    timeout = float(os.environ["AKKI_RECOVERY_PROBE_TIMEOUT_SEC"])
    hosts = ssh_seam.list_hosts()
    if not 0 < len(hosts) <= 2 or len(set(hosts)) != len(hosts):
        raise ValueError("ADMITTED_HOST_SET_INVALID")
    if not all(re.fullmatch(r"[a-zA-Z0-9_-]+", host) for host in hosts):
        raise ValueError("ADMITTED_HOST_ALIAS_INVALID")
    directory.mkdir(parents=True, exist_ok=True)
    results = []
    for host in hosts:
        config = ssh_seam.get_host_config(host)
        prefix = f"auth-none-{digest}-{host}"
        intent_path = directory / f"{prefix}.intent.json"
        receipt_path = directory / f"{prefix}.result.json"
        intent = {"at_utc": datetime.now(timezone.utc).isoformat(), "host_alias": host,
                  "workbook_sha256": digest, "operation": "pinned_auth_none_only",
                  "credentials_sent": False, "commands_permitted": False}
        try:
            _write_exclusive(intent_path, intent)
        except FileExistsError:
            if receipt_path.is_file():
                results.append(json.loads(receipt_path.read_text()))
            else:
                results.append({"host_alias": host, "error_code": "ATTEMPT_ALREADY_CONSUMED"})
            continue
        # A crash after the intent deliberately consumes the attempt. No retries
        # or removal of this marker are allowed by this runner.
        result = diagnose(config, timeout=timeout)
        receipt = {"at_utc": datetime.now(timezone.utc).isoformat(), "intent_ref": intent_path.name,
                   "workbook_sha256": digest, "result": result}
        _write_exclusive(receipt_path, receipt)
        results.append(receipt)
    return results