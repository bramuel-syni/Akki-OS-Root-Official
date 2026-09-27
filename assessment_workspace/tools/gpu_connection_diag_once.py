import base64
import hashlib
import hmac
import json
import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

import paramiko
from dotenv import load_dotenv


ROOT = Path("/app")
BACKEND_ROOT = ROOT / "backend"
VENDORED_BACKEND = BACKEND_ROOT / "vendored/extraction_akki/backend"
if str(VENDORED_BACKEND) not in sys.path:
    sys.path.insert(0, str(VENDORED_BACKEND))

from services.training_runner import ssh_seam
from services.census_autonomy import execution_identity
from services.census_autonomy.execution_identity import IdentityVerificationError


TIMEOUT_SECONDS = 8.0
ALLOWED_AUTH_MESSAGES = {
    "Authentication failed.",
    "Authentication failed",
    "Authentication timeout.",
}


def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()


def ts_compact():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(public_bytes: bytes):
    digest = hashlib.sha256(public_bytes).digest()
    return "SHA256:" + base64.b64encode(digest).decode().rstrip("=")


def exclusive_write_json(path: Path, payload: dict):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def known_hosts_token(host: str, port: int):
    return host if port == 22 else f"[{host}]:{port}"


def collect_hash_targets(hosts):
    targets = [
        ROOT / "backend/.env",
        VENDORED_BACKEND / "services/census_autonomy/execution_identity.py",
        VENDORED_BACKEND / "services/census_autonomy/remote_dispatch.py",
    ]
    known_hosts = os.environ.get("SSH_KNOWN_HOSTS_PATH")
    if known_hosts:
        targets.append(Path(known_hosts))

    for host_alias in hosts:
        cfg = ssh_seam.get_host_config(host_alias)
        if cfg.key_path:
            targets.append(Path(cfg.key_path))

    unique = []
    seen = set()
    for item in targets:
        item = item.resolve() if item.exists() else item
        key = str(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def resolve_pin_info(cfg):
    token = known_hosts_token(cfg.host, cfg.port)
    host_keys_path = os.environ.get("SSH_KNOWN_HOSTS_PATH")
    if not host_keys_path:
        return {
            "known_hosts_path": None,
            "token": token,
            "pin_present": False,
            "pin_algorithms": [],
            "pin_fingerprints": {},
            "pin_reason": "KNOWN_HOSTS_PATH_MISSING",
        }

    path = Path(host_keys_path)
    if not path.exists():
        return {
            "known_hosts_path": str(path),
            "token": token,
            "pin_present": False,
            "pin_algorithms": [],
            "pin_fingerprints": {},
            "pin_reason": "KNOWN_HOSTS_FILE_MISSING",
        }

    pins = paramiko.HostKeys(str(path))
    pinned = pins.lookup(token)
    if not pinned:
        return {
            "known_hosts_path": str(path),
            "token": token,
            "pin_present": False,
            "pin_algorithms": [],
            "pin_fingerprints": {},
            "pin_reason": "SERVER_PIN_MISSING",
        }

    fp = {alg: fingerprint(pinned[alg].asbytes()) for alg in pinned.keys()}
    return {
        "known_hosts_path": str(path),
        "token": token,
        "pin_present": True,
        "pin_algorithms": sorted(list(pinned.keys())),
        "pin_fingerprints": fp,
        "pin_reason": None,
    }


def run_single_handshake(cfg, pin_info, identity_ok, admitted_key):
    result = {
        "host_alias": cfg.name,
        "checked_at_utc": now_utc_iso(),
        "tcp_connected": False,
        "server_pin_matched": False,
        "auth_attempts": [],
        "authenticated": False,
        "channels_opened": 0,
        "commands_executed": 0,
        "advertised_auth_methods": [],
        "status": "NOT_ATTEMPTED",
    }

    if not pin_info.get("pin_present"):
        result["status"] = "PIN_MISSING_STOPPED"
        result["error_type"] = "PinValidationError"
        return result

    sock = None
    transport = None
    try:
        sock = socket.create_connection((cfg.host, cfg.port), timeout=TIMEOUT_SECONDS)
        result["tcp_connected"] = True
        transport = paramiko.Transport(sock)
        transport.banner_timeout = TIMEOUT_SECONDS
        transport.auth_timeout = TIMEOUT_SECONDS
        transport.handshake_timeout = TIMEOUT_SECONDS

        sec = transport.get_security_options()
        pinned_algs = set(pin_info["pin_algorithms"])
        if "ssh-rsa" in pinned_algs:
            pinned_algs.update({"rsa-sha2-512", "rsa-sha2-256"})
        key_types = tuple(k for k in sec.key_types if k in pinned_algs)
        if not key_types:
            result["status"] = "PINNED_SERVER_ALGORITHM_UNAVAILABLE"
            result["error_type"] = "PinValidationError"
            return result
        sec.key_types = key_types

        transport.start_client(timeout=TIMEOUT_SECONDS)
        server_key = transport.get_remote_server_key()
        expected_fp = pin_info["pin_fingerprints"].get(server_key.get_name())
        actual_fp = fingerprint(server_key.asbytes())
        result["server_key_algorithm"] = server_key.get_name()
        result["server_key_fingerprint"] = actual_fp
        if expected_fp is None or not hmac.compare_digest(expected_fp, actual_fp):
            result["status"] = "SERVER_PIN_MISMATCH_STOPPED"
            result["error_type"] = "PinValidationError"
            return result

        result["server_pin_matched"] = True

        if identity_ok and admitted_key is not None:
            result["auth_attempts"].append("publickey")
            next_methods = transport.auth_publickey(cfg.username, admitted_key)
            result["authenticated"] = bool(transport.is_authenticated())
            result["advertised_auth_methods"] = sorted(next_methods or [])
            result["status"] = "AUTHENTICATED" if result["authenticated"] else "PUBLICKEY_REJECTED"
        else:
            result["auth_attempts"].append("auth_none")
            try:
                next_methods = transport.auth_none(cfg.username)
                result["authenticated"] = bool(transport.is_authenticated())
                result["advertised_auth_methods"] = sorted(next_methods or [])
                result["status"] = "AUTH_NONE_COMPLETED"
            except paramiko.BadAuthenticationType as exc:
                result["authenticated"] = False
                result["advertised_auth_methods"] = sorted(exc.allowed_types or [])
                result["status"] = "AUTH_NONE_REJECTED_METHODS_ADVERTISED"
                result["error_type"] = "BadAuthenticationType"
            except paramiko.AuthenticationException as exc:
                result["authenticated"] = False
                msg = str(exc).strip()
                result["status"] = "AUTH_NONE_REJECTED"
                result["error_type"] = "AuthenticationException"
                result["error_message"] = msg if msg in ALLOWED_AUTH_MESSAGES else "SSH authentication did not succeed."

    except (socket.timeout, TimeoutError):
        result["status"] = "TIMEOUT"
        result["error_type"] = "TimeoutError"
    except paramiko.BadAuthenticationType as exc:
        result["status"] = "PUBLICKEY_METHOD_REJECTED"
        result["error_type"] = "BadAuthenticationType"
        result["advertised_auth_methods"] = sorted(exc.allowed_types or [])
    except paramiko.AuthenticationException as exc:
        msg = str(exc).strip()
        result["status"] = "AUTHENTICATION_REJECTED"
        result["error_type"] = "AuthenticationException"
        result["error_message"] = msg if msg in ALLOWED_AUTH_MESSAGES else "SSH authentication did not succeed."
    except (paramiko.SSHException, OSError, EOFError, ValueError) as exc:
        result["status"] = "TRANSPORT_ERROR"
        result["error_type"] = type(exc).__name__
    finally:
        if transport is not None:
            try:
                transport.close()
            finally:
                if sock is not None:
                    sock.close()
        elif sock is not None:
            sock.close()

    return result


def main():
    load_dotenv(BACKEND_ROOT / ".env", override=False)

    hosts = ssh_seam.list_hosts()
    receipt_dir = ROOT / "assessment_workspace/phase0/drill_receipts" / f"{ts_compact()}_gpu_connection_diag_once"
    receipt_dir.mkdir(parents=True, exist_ok=False)

    hash_targets = collect_hash_targets(hosts)
    before_hashes = {}
    for file_path in hash_targets:
        before_hashes[str(file_path)] = {
            "exists": file_path.exists(),
            "sha256": sha256_file(file_path) if file_path.exists() else None,
        }

    intent = {
        "created_at_utc": now_utc_iso(),
        "operation": "one_read_only_tcp_ssh_handshake_per_configured_gpu_host",
        "constraints": {
            "retries": 0,
            "stage_timeout_seconds": TIMEOUT_SECONDS,
            "remote_channels_allowed": False,
            "remote_commands_allowed": False,
            "workloads_allowed": False,
            "pin_mismatch_stop_before_auth": True,
            "identity_guard_bypass": False,
            "inventory_source": "AKKI_GPU_HOSTS",
        },
        "hosts_requested": hosts,
    }
    exclusive_write_json(receipt_dir / "intent.json", intent)

    host_results = []
    for host_alias in hosts:
        cfg = ssh_seam.get_host_config(host_alias)
        pin_info = resolve_pin_info(cfg)

        identity_ok = False
        identity_reason = None
        admitted_key = None
        admitted_key_fp = None
        try:
            admitted_key = execution_identity.verify_identity(cfg)
            admitted_key_fp = fingerprint(admitted_key.asbytes())
            identity_ok = True
        except IdentityVerificationError as exc:
            identity_reason = exc.reason_code

        host_record = {
            "host_alias": host_alias,
            "checked_at_utc": now_utc_iso(),
            "resolved_config": {
                "host": cfg.host,
                "port": cfg.port,
                "username": cfg.username,
                "key_path": cfg.key_path,
                "slug": cfg.slug,
            },
            "local_admission": {
                "valid": identity_ok,
                "reason": None if identity_ok else identity_reason,
                "admitted_key_fingerprint": admitted_key_fp,
            },
            "server_pin": {
                "known_hosts_path": pin_info["known_hosts_path"],
                "lookup_token": pin_info["token"],
                "pin_present": pin_info["pin_present"],
                "pin_reason": pin_info["pin_reason"],
                "pin_algorithms": pin_info["pin_algorithms"],
                "pin_fingerprints": pin_info["pin_fingerprints"],
            },
            "connection": run_single_handshake(cfg, pin_info, identity_ok, admitted_key),
        }
        host_results.append(host_record)

    after_hashes = {}
    for file_path in hash_targets:
        after_hashes[str(file_path)] = {
            "exists": file_path.exists(),
            "sha256": sha256_file(file_path) if file_path.exists() else None,
        }

    unchanged = before_hashes == after_hashes

    result_payload = {
        "finished_at_utc": now_utc_iso(),
        "hosts_checked": len(hosts),
        "hosts": host_results,
        "protected_file_hashes_before": before_hashes,
        "protected_file_hashes_after": after_hashes,
        "protected_files_unchanged": unchanged,
        "notes": {
            "no_remote_channels_opened": True,
            "no_remote_commands_executed": True,
            "no_key_or_known_hosts_mutation": True,
            "single_attempt_per_host": True,
        },
    }

    exclusive_write_json(receipt_dir / "result.json", result_payload)
    print(str(receipt_dir))


if __name__ == "__main__":
    main()