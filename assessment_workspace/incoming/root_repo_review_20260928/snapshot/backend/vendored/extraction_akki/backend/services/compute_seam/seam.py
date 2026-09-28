"""Compute seam — governed handoff to the AISCA GPU VM.

Build Order 01 · Owner Clarification 2 (2026-08-14) · WS-BUILD-COMPUTE-SEAM.

The seam is the ONLY path by which the estate reaches the VM. It:
  1. Reads SSH config from env (never hardcoded, never in code, never in STATE).
  2. Refuses if the VM (`infrastructure.vm.<host>`) has no in-force declaration.
  3. Refuses if the task-id is not registered in the thin kernel.
  4. Writes a `Ledger.Row` BEFORE invoking the SSH transport (Canon 1 §6
     fail-closed custody).
  5. Executes the command via `ssh -o BatchMode=yes` (no interactive auth,
     key-only per Build Order 01 §6.3).
  6. Verifies any returned artifact's sha256 against a claimed hash
     (see `services.compute_seam.artifact_verify`).
  7. Emits an outer-gate receipt on exit.

Failure taxonomy:
  - refused          — declaration missing / expired / scope mismatch.
  - task_unregistered — Canon 8 W11.
  - connection_refused — TCP refused.
  - timeout          — SSH connect timed out.
  - auth_denied      — key rejected / user unknown.
  - host_unknown     — DNS or unknown-host key.

Nothing on the VM is durable via ephemeral (Build Order 01 §6.2). Storage
layout is HSS-only for durable working set; ephemeral is scratch only.
"""
from __future__ import annotations

import asyncio
import os
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from contracts.task_identity import is_registered
from services.chokepoint import ChokepointRefused, register_crossing
from services.declaration import check


class SeamRefusal(Exception):
    """Raised when the seam refuses to execute — fail-closed custody."""


@dataclass
class SeamResult:
    ledger_row_id: str
    exit_code: int
    stdout: str
    stderr: str
    failure_kind: Optional[str]


def _ssh_config() -> Dict[str, str]:
    """Load SSH config from env.

    Env vars (never hardcoded, never in STATE):
      VM_HOST                — remote hostname or IP.
      VM_USER                — remote username.
      SSH_PRIVATE_KEY_PATH   — path to private key under named custody.
      SSH_CONNECT_TIMEOUT    — seconds (default: 10).
      SSH_ALLOWLIST_EGRESS_IPS  — /32 list; owner must allowlist us on VM.
    """
    return {
        "host": os.environ.get("VM_HOST", ""),
        "user": os.environ.get("VM_USER", ""),
        "key_path": os.environ.get("SSH_PRIVATE_KEY_PATH", ""),
        "timeout": os.environ.get("SSH_CONNECT_TIMEOUT", "10"),
    }


async def _write_ledger_row(row: Dict[str, Any]) -> str:
    """Write a compute-seam ledger row. Returns the row id.

    Real implementation plugs Motor into `services.northena.ledger.record`;
    the thin-kernel test path replaces this at module scope.
    """
    from services.northena.ledger import record as _record  # noqa: WPS433
    return await _record(row)


def _ssh_transport(
    *,
    host: str,
    user: str,
    key_path: str,
    command: str,
    timeout: int,
) -> Dict[str, Any]:
    """Execute `command` on the remote VM. Key-only; batch-mode.

    Returns dict with exit_code/stdout/stderr/failure_kind.
    """
    ssh_cmd = [
        "ssh",
        "-p", os.environ.get("VM_PORT", "22"),
        "-o", "BatchMode=yes",
        "-o", "PasswordAuthentication=no",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", f"ConnectTimeout={timeout}",
        "-i", key_path,
        f"{user}@{host}",
        command,
    ]
    try:
        completed = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "stdout": "", "stderr": "timeout", "failure_kind": "timeout"}
    except FileNotFoundError:
        return {"exit_code": 127, "stdout": "", "stderr": "ssh_not_installed",
                "failure_kind": "host_unknown"}
    return _classify(completed)


def _classify(completed) -> Dict[str, Any]:
    """Classify an ssh exit into the seam's failure taxonomy."""
    fail: Optional[str] = None
    stderr = (completed.stderr or "").lower()
    if completed.returncode == 255:
        if "permission denied" in stderr or "authentication failed" in stderr:
            fail = "auth_denied"
        elif "connection refused" in stderr:
            fail = "connection_refused"
        elif "connection timed out" in stderr or "operation timed out" in stderr:
            fail = "timeout"
        elif "no route to host" in stderr or "name or service not known" in stderr:
            fail = "host_unknown"
        else:
            fail = "connection_refused"
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "failure_kind": fail,
    }


async def execute(
    *,
    vm_actor_id: str,
    command: str,
    task_id: str,
    required_scope: Optional[list[str]] = None,
) -> SeamResult:
    """Run `command` on the VM through the governed seam.

    Order (Canon 1 §6 fail-closed):
      1. Declaration check (refuse if not in force).
      2. Task-identity check (refuse if not registered).
      3. Write ledger row (BEFORE transport).
      4. Invoke transport.
      5. Return result.
    """
    verdict = await check(vm_actor_id, required_scope=required_scope)
    if verdict != "in_force":
        raise SeamRefusal(f"declaration_missing|{verdict}: {vm_actor_id}")
    if not is_registered(task_id):
        raise SeamRefusal(f"task_identity_unregistered: {task_id}")

    # W3 · Doc 01 §A5.5 chokepoint: SSH out is a real crossing today.
    # Register BEFORE the transport. Residency for akki-vm is not yet on
    # record — the commissioning record does not carry a region field —
    # so we honestly declare "not_on_record" and the chokepoint refuses.
    # A future amendment to the commissioning record will lift this.
    cfg = _ssh_config()
    ssh_host = cfg["host"] or "unset"
    ssh_region = os.environ.get("VM_REGION", "not_on_record")
    try:
        register_crossing(
            kind="ssh_seam",
            endpoint={"host": ssh_host, "region": ssh_region},
            verb="attested_command",
            payload_shape={"command_shape": command.split()[0] if command else ""},
            actor=vm_actor_id,
            masking_tier="attested_command",
        )
    except ChokepointRefused as exc:
        raise SeamRefusal(f"chokepoint_refused: {exc}") from exc

    ts = datetime.now(timezone.utc).isoformat()
    row = {
        "stage": "compute_seam_exec",
        "vm_actor_id": vm_actor_id,
        "task_id": task_id,
        "command": command,
        "at": ts,
    }
    row_id = await _write_ledger_row(row)

    transport_result = _ssh_transport(
        host=cfg["host"] or "unset",
        user=cfg["user"] or "unset",
        key_path=cfg["key_path"] or "unset",
        command=command,
        timeout=int(cfg["timeout"]),
    )
    return SeamResult(
        ledger_row_id=str(row_id),
        exit_code=transport_result["exit_code"],
        stdout=transport_result["stdout"],
        stderr=transport_result["stderr"],
        failure_kind=transport_result.get("failure_kind"),
    )
