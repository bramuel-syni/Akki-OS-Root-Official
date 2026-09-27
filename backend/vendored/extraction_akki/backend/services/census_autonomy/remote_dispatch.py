"""Strict-host-key control-plane adapter using existing Akki host/credential configuration."""
import base64
import json
import os
import shlex
import time
from pathlib import Path

from services.training_runner import ssh_seam
from services.census_autonomy.operational_validation import PROTOCOL
from services.census_autonomy import operational_store as store
from services.census_autonomy import execution_identity
from services.census_autonomy.execution_identity import IdentityVerificationError


def _connect(host, timeout):
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.connection import connect as direct_connect
        client, _ = direct_connect(host, timeout=timeout)
        try:
            return client, ssh_seam.get_host_config(host)
        except Exception:
            client.close()
            raise
    import paramiko
    config = ssh_seam.get_host_config(host)
    key = execution_identity.verify_identity(config)
    client = paramiko.SSHClient()
    options = dict(hostname=config.host, port=config.port, username=config.username,
                   timeout=timeout, auth_timeout=timeout, banner_timeout=timeout,
                   allow_agent=False, look_for_keys=False, pkey=key)
    try:
        client.load_host_keys(os.environ["SSH_KNOWN_HOSTS_PATH"])
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(**options)
        return client, config
    except Exception:
        client.close()
        raise


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    """Try configured Akki hosts; failures are isolated and never imply GPU hardware failure."""
    hosts = ssh_seam.list_hosts()
    cursor = store.get(run_id, tenant)
    pinned = (cursor or {}).get("source_hosts", {}).get(source)
    if pinned:
        hosts = [pinned] if pinned in hosts else []
    attempts = []
    for host in hosts:
        remaining = int(deadline - time.time())
        if remaining <= 2:
            break
        client = None
        dispatched = False
        try:
            client, config = _connect(host, min(12, remaining))
            control = {"census_run_id": run_id, "tenant_id": tenant, "source_id": source,
                       "lawful_basis_sha256": lawful_hash, "hostname_expected": config.hostname_expected,
                       "max_seconds": max(1, int(deadline - time.time()) - 1),
                       "max_databases": int(os.environ["CENSUS_MAX_DATABASES"]),
                       "max_connections": int(os.environ["CENSUS_MAX_CONNECTIONS"])}
            code = Path(__file__).with_name("remote_worker.py").read_text()
            encoded = base64.b64encode(json.dumps(control).encode()).decode()
            command = "python3 -c " + shlex.quote(code) + " " + shlex.quote(encoded)
            channel = client.get_transport().open_session(timeout=min(10, remaining))
            cursor = store.get(run_id, tenant)
            if not cursor:
                raise ValueError("Durable commission cursor absent")
            cursor.setdefault("source_hosts", {})[source] = host
            store.save(cursor)
            dispatched = True
            channel.exec_command(command)
            output = bytearray()
            while True:
                if time.time() >= deadline:
                    raise TimeoutError("Execution deadline")
                if channel.recv_ready():
                    output.extend(channel.recv(16384))
                    if len(output) > 32768:
                        raise ValueError("Aggregate receipt exceeds bound")
                if channel.recv_stderr_ready():
                    channel.recv_stderr(16384)  # Never log provider diagnostics/credentials.
                if channel.exit_status_ready() and not channel.recv_ready():
                    break
                time.sleep(0.02)
            if channel.recv_exit_status() != 0:
                raise ValueError("Remote worker did not return a receipt")
            result = json.loads(output)
            attempts.append({"host": host, "transport": "connected", "worker_status": result.get("status")})
            _bank_transport(run_id, source, attempts)
            # Once a worker has run, do not retry its source on another host.
            return result
        except Exception as exc:
            attempt = {"host": host, "transport": "not_verified", "error_type": type(exc).__name__}
            if isinstance(exc, IdentityVerificationError):
                attempt["reason_code"] = exc.reason_code
            attempts.append(attempt)
            if dispatched:
                break  # Outcome uncertain: never duplicate a possible read on a different host.
        finally:
            if client:
                client.close()
    _bank_transport(run_id, source, attempts)
    identity_refused = attempts and all("reason_code" in attempt for attempt in attempts)
    return {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant, "source_id": source,
            "execution_location": "control_plane", "observed_at": store.now(), "status": "blocked",
            "worker_receipt_id": None, "source_rows_returned": 0,
            "reason_code": ("AKKI_EXECUTION_IDENTITY_NOT_VERIFIED" if identity_refused else
                            "AKKI_EXECUTION_CONNECTION_NOT_VERIFIED" if hosts else "AKKI_HOST_INVENTORY_MISSING")}


def _bank_transport(run_id, source, attempts):
    # Receipt class only; not a source/registry store. No SQL, host addresses or secrets.
    path = store.cursor_dir() / f"transport-{run_id}-{source}.json"
    path.write_text(json.dumps({"census_run_id": run_id, "source_id": source,
                                "at_utc": store.now(), "attempts": attempts}, indent=2))