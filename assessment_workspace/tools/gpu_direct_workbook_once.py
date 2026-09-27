"""One-pass owner-authorized direct password seam from workbook targets.

Creates a timestamped exclusive receipt directory with intent + result.
Does exactly one connect_target() call per workbook target and closes any
authenticated client immediately. No remote commands/channels/workload usage.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path("/app")
BACKEND_ROOT = ROOT / "backend"
VENDORED_BACKEND = BACKEND_ROOT / "vendored/extraction_akki/backend"
if str(VENDORED_BACKEND) not in sys.path:
    sys.path.insert(0, str(VENDORED_BACKEND))

from services.gpu_direct.workbook import DirectConnectionError, read_targets
from services.gpu_direct.connection import connect_target


WORKBOOK_PATH = BACKEND_ROOT / "estate_keys/gpu_hosts/GPU_CREDs_owner_20260927T174431Z.xlsx"
SSH_PORT = "22"
TIMEOUT_SECONDS = "8"
OLD_IDENTITY_MODULE = VENDORED_BACKEND / "services/census_autonomy/execution_identity.py"


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def ts_compact():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_exclusive_json(path: Path, payload: dict):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def build_hash_targets():
    targets = [BACKEND_ROOT / ".env", OLD_IDENTITY_MODULE]
    known_hosts = os.environ.get("SSH_KNOWN_HOSTS_PATH")
    if known_hosts:
        targets.append(Path(known_hosts))
    old_client_key = os.environ.get("AKKI_VM_SSH_PRIVATE_KEY_PATH")
    if old_client_key:
        targets.append(Path(old_client_key))

    unique = []
    seen = set()
    for item in targets:
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def snapshot_hashes(paths):
    out = {}
    for p in paths:
        out[str(p)] = {
            "exists": p.exists(),
            "sha256": sha256_file(p) if p.exists() else None,
        }
    return out


def sanitize_receipt(target, receipt):
    return {
        "host_alias": target.name,
        "checked_at_utc": utc_now_iso(),
        "auth_method": receipt.get("auth_method"),
        "auth_attempts": receipt.get("auth_attempts"),
        "tcp_connected": receipt.get("tcp_connected"),
        "server_identity_verified": receipt.get("server_identity_verified"),
        "authenticated": receipt.get("authenticated"),
        "status": receipt.get("status"),
        "allowed_methods": receipt.get("allowed_methods", []),
        "credential_source": receipt.get("credential_source"),
        "historical_client_identity_used": receipt.get("historical_client_identity_used"),
        "remote_commands": receipt.get("remote_commands"),
        "remote_channels": receipt.get("remote_channels"),
    }


def main():
    load_dotenv(BACKEND_ROOT / ".env", override=False)

    # Process-local override only for the direct workbook seam.
    os.environ["GPU_DIRECT_CREDENTIALS_XLSX"] = str(WORKBOOK_PATH)
    os.environ["GPU_DIRECT_SSH_PORT"] = SSH_PORT
    os.environ["GPU_DIRECT_TIMEOUT_SECONDS"] = TIMEOUT_SECONDS

    receipt_dir = ROOT / "assessment_workspace/phase0/drill_receipts" / f"{ts_compact()}_gpu_direct_workbook"
    receipt_dir.mkdir(parents=True, exist_ok=False)

    workbook_digest = sha256_file(WORKBOOK_PATH)
    hash_targets = build_hash_targets()
    before_hashes = snapshot_hashes(hash_targets)

    intent = {
        "created_at_utc": utc_now_iso(),
        "operation": "direct_password_connect_target_once_per_workbook_target",
        "authorization_scope": "owner-authorized direct password seam; no commands/workload",
        "constraints": {
            "single_attempt_per_target": True,
            "no_retries": True,
            "ssh_port": 22,
            "timeout_seconds": 8,
            "password_method_only": True,
            "no_key_agent_or_fallback": True,
            "no_remote_commands": True,
            "no_remote_channels": True,
        },
        "workbook_custody_reference": {
            "path": str(WORKBOOK_PATH),
            "sha256": workbook_digest,
        },
    }
    write_exclusive_json(receipt_dir / "intent.json", intent)

    targets = read_targets(os.environ)
    host_results = []
    for target in targets:
        client = None
        try:
            client, receipt = connect_target(target, environ=os.environ, timeout=8)
            host_results.append(sanitize_receipt(target, receipt))
        finally:
            if client is not None:
                client.close()

    after_hashes = snapshot_hashes(hash_targets)
    result = {
        "finished_at_utc": utc_now_iso(),
        "targets_count": len(targets),
        "targets": host_results,
        "protected_file_hashes_before": before_hashes,
        "protected_file_hashes_after": after_hashes,
        "protected_files_unchanged": before_hashes == after_hashes,
        "notes": {
            "workbook_values_used_for_endpoint_user_password": True,
            "server_pin_required": True,
            "old_client_key_not_used": True,
            "legacy_identity_module_not_used_for_connection": True,
        },
    }
    write_exclusive_json(receipt_dir / "result.json", result)
    print(str(receipt_dir))


if __name__ == "__main__":
    try:
        main()
    except DirectConnectionError as exc:
        print(json.dumps({"status": "DIRECT_CONNECTION_ERROR", "code": exc.code}))
        raise
