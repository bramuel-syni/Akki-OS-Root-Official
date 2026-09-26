"""Owner-authorized key-only SSH authentication diagnostic; no remote channels.

Bypasses ONLY the comparison of the available client key to the admitted client
fingerprint. Original key custody, receipt integrity and server pins remain.
The existing application, environment files and credentials are never modified.
An exclusive, durable per-host intent consumes the attempt even after a crash.
"""
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import socket
import sys
from datetime import datetime, timezone

import paramiko
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend/vendored/extraction_akki/backend"))
from services.training_runner import ssh_seam
from services.census_autonomy import execution_identity as identity
from services.census_autonomy.auth_methods_receipts import _write_exclusive

DIRECTORY = ROOT / "assessment_workspace/phase0/drill_receipts/census_operational_v1/execution_recovery/current_key_auth_owner_authorized_v1"
AUTHORIZED_HOSTS = ("akki-vm", "akki-vm-ii")
TIMEOUT_SECONDS = 8.0
LOGGER = "akki.owner_authorized_current_key_auth"
logging.getLogger(LOGGER).addHandler(logging.NullHandler())
logging.getLogger(LOGGER).propagate = False
ALLOWED_METHODS = {"publickey", "password", "keyboard-interactive", "hostbased",
                   "gssapi-with-mic", "gssapi-keyex", "none"}
APPLICATION_FILES = (
    ROOT / "backend/.env",
    ROOT / "backend/vendored/extraction_akki/backend/services/census_autonomy/execution_identity.py",
    ROOT / "backend/vendored/extraction_akki/backend/services/census_autonomy/remote_dispatch.py",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def prepare(host):
    """Local reads only; the caller supplies an explicitly authorized inventory ID."""
    if host not in AUTHORIZED_HOSTS:
        raise ValueError("HOST_NOT_AUTHORIZED")
    config = ssh_seam.get_host_config(host)
    # No legacy defaults or accidental alternate identity: actual values must
    # originate from the existing per-host environment configuration.
    for suffix, value in (("HOST", config.host), ("PORT", str(config.port)),
                          ("USERNAME", config.username), ("SSH_PRIVATE_KEY_PATH", config.key_path)):
        configured = os.environ.get(f"{config.slug}_{suffix}")
        if not configured or configured.strip() != value:
            raise ValueError("EXPLICIT_HOST_CONFIGURATION_REQUIRED")
    expected_client = identity._expected_fingerprint(config)  # Original receipt/hash validation.
    key = identity._load_key(config.key_path)  # Original ownership/mode/no-symlink checks.
    current_client = identity._fingerprint(key.asbytes())
    pins = paramiko.HostKeys(os.environ["SSH_KNOWN_HOSTS_PATH"])
    token = config.host if config.port == 22 else f"[{config.host}]:{config.port}"
    pinned = pins.lookup(token)
    if not pinned:
        raise ValueError("SERVER_PIN_MISSING")
    return config, key, pinned, {
        "host_alias": host, "expected_client_fingerprint": expected_client,
        "available_client_fingerprint": current_client,
        "client_identity_matches_admission": hmac.compare_digest(expected_client, current_client),
    }


def authenticate(config, key, pinned):
    """One connection and one public-key method, only after server-pin match."""
    sock = transport = None
    result = {"tcp_connected": False, "server_pin_matched": False,
              "publickey_auth_attempts": 0, "authenticated": False,
              "remote_channels_opened": 0, "remote_commands": 0,
              "stage": "tcp_connect", "status": "NOT_ATTEMPTED"}
    try:
        sock = socket.create_connection((config.host, config.port), timeout=TIMEOUT_SECONDS)
        result["tcp_connected"] = True
        transport = paramiko.Transport(sock)
        transport.set_log_channel(LOGGER)
        transport.banner_timeout = TIMEOUT_SECONDS
        transport.auth_timeout = TIMEOUT_SECONDS
        transport.handshake_timeout = TIMEOUT_SECONDS
        security = transport.get_security_options()
        compatible = set(pinned)
        if "ssh-rsa" in compatible:
            compatible.update(("rsa-sha2-512", "rsa-sha2-256"))
        key_types = tuple(k for k in security.key_types if k in compatible)
        if not key_types:
            result["status"] = "PINNED_SERVER_ALGORITHM_UNAVAILABLE"
            return result
        security.key_types = key_types
        result["stage"] = "server_key_verification"
        transport.start_client(timeout=TIMEOUT_SECONDS)
        server_key = transport.get_remote_server_key()
        expected_server = pinned.get(server_key.get_name())
        if expected_server is None or not hmac.compare_digest(expected_server.asbytes(), server_key.asbytes()):
            result["status"] = "SERVER_PIN_MISMATCH"
            return result
        result["server_pin_matched"] = True
        result["server_key_fingerprint"] = identity._fingerprint(server_key.asbytes())
        result["stage"] = "publickey_authentication"
        result["publickey_auth_attempts"] = 1
        next_methods = transport.auth_publickey(config.username, key)
        result["authenticated"] = bool(transport.is_authenticated())
        result["next_auth_methods"] = sorted(m for m in (next_methods or []) if m in ALLOWED_METHODS)
        result["status"] = "AUTHENTICATED" if result["authenticated"] else "ADDITIONAL_AUTH_REQUIRED"
        return result
    except paramiko.BadAuthenticationType as exc:
        result.update(status="PUBLICKEY_METHOD_REJECTED", error_type="BadAuthenticationType",
                      allowed_methods=sorted(m for m in exc.allowed_types if m in ALLOWED_METHODS))
    except paramiko.AuthenticationException as exc:
        # Only these known, constant messages can escape; never arbitrary provider text.
        message = str(exc).strip()
        result.update(status="AUTHENTICATION_REJECTED", error_type="AuthenticationException",
                      error_message=message if message in {"Authentication failed.", "Authentication failed", "Authentication timeout."} else "SSH authentication did not succeed.")
    except (socket.timeout, TimeoutError):
        result.update(status="TIMEOUT", error_type="TimeoutError")
    except (paramiko.SSHException, OSError, EOFError, ValueError) as exc:
        result.update(status="TRANSPORT_ERROR", error_type=type(exc).__name__)
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


def run_once():
    if set(ssh_seam.list_hosts()) != set(AUTHORIZED_HOSTS):
        raise ValueError("HOST_INVENTORY_DIFFERS_FROM_OWNER_AUTHORIZATION")
    DIRECTORY.mkdir(parents=True, exist_ok=True)
    outputs = []
    for host in AUTHORIZED_HOSTS:
        intent_path, result_path = DIRECTORY / f"{host}.intent.json", DIRECTORY / f"{host}.result.json"
        if intent_path.exists():
            outputs.append(json.loads(result_path.read_text()) if result_path.exists() else
                           {"host_alias": host, "status": "ATTEMPT_ALREADY_CONSUMED_OUTCOME_UNRECORDED"})
            continue
        config, key, pinned, meta = prepare(host)
        intent = {**meta, "at_utc": now(), "operation": "single_pinned_publickey_auth_only",
                  "authorization": "Owner: go ahead, after explicit auth-only scope",
                  "bypass": "local_client_fingerprint_equality_only",
                  "commands_allowed": False, "channels_allowed": False,
                  "password_fallback_allowed": False, "retries_allowed": False}
        try:
            _write_exclusive(intent_path, intent)
        except FileExistsError:
            outputs.append({"host_alias": host, "status": "ATTEMPT_ALREADY_CONSUMED"})
            continue
        result = {**meta, "started_at_utc": now(), **authenticate(config, key, pinned), "finished_at_utc": now()}
        _write_exclusive(result_path, result)
        outputs.append(result)
    return outputs


if __name__ == "__main__":
    load_dotenv(ROOT / "backend/.env", override=False)
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in APPLICATION_FILES}
    results = run_once()
    unchanged = all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == digest for p, digest in before.items())
    if not unchanged:
        raise RuntimeError("APPLICATION_OR_ENVIRONMENT_CHANGED_DURING_DIAGNOSTIC")
    print(json.dumps({"results": results, "application_and_env_unchanged": unchanged,
                      "no_keys_generated_or_modified": True, "no_remote_commands_or_channels": True}, indent=2))