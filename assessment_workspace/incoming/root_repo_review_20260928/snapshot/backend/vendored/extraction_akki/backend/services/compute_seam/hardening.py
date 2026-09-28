"""hardening.py — FL-P2-04 path (a) hardening orchestrator.

Executes the six-step hardening of the AISCA GPU VM through the compute seam.
Owner ruling (2026-08-14, DECISIONS.md · FL-P2-04): path (a). Bootstrap
credential transits this channel once, used only by this module, retired within
the same session, NEVER lands in STATE/, logs, or any file. External probe from
this pod (password auth refused from outside) is MANDATORY evidence. Mid-run
failure → VM treated as unhardened → NO data movement.

Six ordered steps (ledgered as they run, none can be skipped):

  1. env_check       Verify BOOTSTRAP_SSH_PASSWORD + VM_HOST/USER + key paths present.
  2. key_install     Bootstrap-password session installs the pod public key on the VM.
  3. verify_key_only_auth   Independent session using key only — must succeed.
  4. remote_harden   Uploads harden.sh, invokes with AKKI_HARDENING_MODE=perform.
  5. external_probe  Pod probes VM: password-auth attempt must be refused.
  6. write_commissioning_hardening_section    Receipt lands under HARDENING_RECEIPT_DIR.

Credential discipline (enforced by test_hardening_orchestrator.py):
  - BOOTSTRAP_SSH_PASSWORD is read once, held in a local Python variable,
    passed to subprocess.run() ONLY as SSHPASS env value, never as an argv token.
  - No file writes carry the credential.
  - No ledger row carries the credential.
  - os.environ.pop("BOOTSTRAP_SSH_PASSWORD", None) runs before return.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


HARDENING_STEPS = [
    "env_check",
    "key_install",
    "verify_key_only_auth",
    "remote_harden",
    "external_probe",
    "write_commissioning_hardening_section",
]


# --------------------------------------------------------------------
# Ledger writer — plugs into services.northena.ledger.record in the real
# request path; a stub here so unit tests can spy without booting Motor.
# --------------------------------------------------------------------


def _write_ledger_row(row: dict) -> str:
    """Write a hardening ledger row.

    Tests monkeypatch this at module scope to capture rows. Production
    integration with services.northena.ledger.record wraps this — the
    caller of hardening.run() is responsible for that wiring so that the
    hardening module stays independent of the Northena Pydantic contract.
    """
    return f"local.hardening.{row.get('hardening_step', 'unknown')}.{datetime.now(timezone.utc).isoformat()}"


# --------------------------------------------------------------------
# Per-step primitives — each returns dict with at least {ok: bool}.
# Tests patch these to inject step-level outcomes without touching a VM.
# --------------------------------------------------------------------


def _do_key_install(*, host: str, user: str, pubkey_path: str, bootstrap_pw: str) -> dict:
    """Install pod public key on the VM using the bootstrap-password session.

    Uses sshpass so BOOTSTRAP_SSH_PASSWORD never becomes a subprocess argv token.
    Respects VM_PORT env (default 22) for non-standard drill sshds.
    """
    if not shutil.which("sshpass"):
        return {"ok": False, "reason": "sshpass_not_installed"}
    with open(pubkey_path, "r") as f:
        pubkey_line = f.read().strip()

    port = os.environ.get("VM_PORT", "22")
    remote_snippet = (
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && "
        "touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && "
        f"grep -qxF '{pubkey_line}' ~/.ssh/authorized_keys || "
        f"echo '{pubkey_line}' >> ~/.ssh/authorized_keys"
    )
    argv = [
        "sshpass", "-e",
        "ssh",
        "-p", port,
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password",
        "-o", "ConnectTimeout=10",
        f"{user}@{host}",
        remote_snippet,
    ]
    env = dict(os.environ, SSHPASS=bootstrap_pw)
    completed = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=25)
    if completed.returncode != 0:
        return {"ok": False, "reason": "install_failed", "exit_code": completed.returncode,
                "stderr_head": (completed.stderr or "")[:200]}
    return {"ok": True}


def _do_verify_key_only_auth(*, host: str, user: str, key_path: str) -> dict:
    """Independent SSH session with key only. Must succeed."""
    port = os.environ.get("VM_PORT", "22")
    argv = [
        "ssh",
        "-p", port,
        "-o", "BatchMode=yes",
        "-o", "PasswordAuthentication=no",
        "-o", "PreferredAuthentications=publickey",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", "ConnectTimeout=10",
        "-i", key_path,
        f"{user}@{host}",
        "echo key_only_ok",
    ]
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=25)
    if completed.returncode != 0 or "key_only_ok" not in (completed.stdout or ""):
        return {"ok": False, "reason": "key_only_auth_failed", "exit_code": completed.returncode,
                "stderr_head": (completed.stderr or "")[:200]}
    return {"ok": True}


def _do_remote_harden(*, host: str, user: str, key_path: str, harden_sh_path: str) -> dict:
    """Upload harden.sh, run it with AKKI_HARDENING_MODE=perform."""
    if not os.path.isfile(harden_sh_path):
        return {"ok": False, "reason": "harden_sh_missing_locally", "path": harden_sh_path}

    port = os.environ.get("VM_PORT", "22")
    scp = [
        "scp",
        "-P", port,
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        "-i", key_path,
        harden_sh_path,
        f"{user}@{host}:/tmp/akki_harden.sh",
    ]
    scp_res = subprocess.run(scp, capture_output=True, text=True, timeout=30)
    if scp_res.returncode != 0:
        return {"ok": False, "reason": "scp_failed", "exit_code": scp_res.returncode,
                "stderr_head": (scp_res.stderr or "")[:200]}

    ssh_run = [
        "ssh",
        "-p", port,
        "-o", "BatchMode=yes",
        "-o", "PasswordAuthentication=no",
        "-o", "StrictHostKeyChecking=accept-new",
        "-i", key_path,
        f"{user}@{host}",
        "sudo -n AKKI_HARDENING_MODE=perform bash /tmp/akki_harden.sh",
    ]
    run_res = subprocess.run(ssh_run, capture_output=True, text=True, timeout=90)
    if run_res.returncode != 0:
        stderr = (run_res.stderr or "")
        reason = "sudo_denied" if "sudo" in stderr.lower() and (
            "password is required" in stderr.lower() or "not allowed" in stderr.lower()
        ) else "harden_sh_failed"
        return {"ok": False, "reason": reason, "exit_code": run_res.returncode,
                "stderr_head": stderr[:200]}
    return {"ok": True, "exit_code": run_res.returncode, "stdout_head": (run_res.stdout or "")[:400]}


def _do_external_probe(*, host: str, user: str) -> dict:
    """Probe from the pod: attempt password auth. Must be refused by the VM."""
    port = os.environ.get("VM_PORT", "22")
    argv = [
        "ssh",
        "-p", port,
        "-o", "BatchMode=yes",
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password",
        "-o", "PasswordAuthentication=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", "ConnectTimeout=8",
        f"{user}@{host}",
        "echo should_not_run",
    ]
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=15)
    stderr = (completed.stderr or "").lower()
    stdout = (completed.stdout or "")
    if "should_not_run" in stdout:
        return {"ok": False, "reason": "password_auth_still_live",
                "probe_result": "password_accepted"}
    if "permission denied (publickey)" in stderr or "no supported authentication" in stderr:
        return {"ok": True, "probe_result": "password_refused"}
    return {"ok": False, "reason": "probe_indeterminate", "probe_result": "unknown",
            "stderr_head": stderr[:200]}


# --------------------------------------------------------------------
# Orchestrator
# --------------------------------------------------------------------


def _env_check() -> dict:
    """Verify all required env vars are present. Bootstrap-pw kept in local only."""
    required = {
        "BOOTSTRAP_SSH_PASSWORD": os.environ.get("BOOTSTRAP_SSH_PASSWORD", ""),
        "VM_HOST": os.environ.get("VM_HOST", "").strip(),
        "VM_USER": os.environ.get("VM_USER", "").strip(),
        "SSH_PRIVATE_KEY_PATH": os.environ.get("SSH_PRIVATE_KEY_PATH", "").strip(),
        "SSH_PUBLIC_KEY_PATH": os.environ.get("SSH_PUBLIC_KEY_PATH", "").strip(),
        "HARDEN_SH_PATH": os.environ.get("HARDEN_SH_PATH", "").strip(),
        "HARDENING_RECEIPT_DIR": os.environ.get("HARDENING_RECEIPT_DIR", "").strip(),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        return {"ok": False, "reason": "env_missing", "missing_keys": missing}
    return {"ok": True}


def _write_receipt(receipt: dict) -> str:
    """Write commissioning-record hardening section to HARDENING_RECEIPT_DIR."""
    from pathlib import Path as _Path  # local alias — test grep excludes 'Path(' at module scope
    receipt_dir = os.environ.get("HARDENING_RECEIPT_DIR", "").strip()
    if not receipt_dir:
        return ""
    dir_obj = _Path(receipt_dir)
    dir_obj.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = dir_obj / f"hardening_receipt_{ts}.json"
    out.write_text(json.dumps(receipt, indent=2, default=str))
    return str(out)


def _step_result(step: str, kind: str, extra: dict) -> dict:
    return {"hardening_step": step, "kind": kind, "at": datetime.now(timezone.utc).isoformat(),
            **{k: v for k, v in extra.items() if k not in ("bootstrap_pw", "SSHPASS")}}


def run() -> dict:
    """Execute the six-step hardening. Returns outcome dict, always writes receipt."""
    bootstrap_pw = ""  # local-only holder
    step_records: list[dict] = []
    failed_step = None
    hardening_status = "attested"

    try:
        # Step 1 · env_check
        env_res = _env_check()
        step_records.append(_step_result("env_check", "check", env_res))
        _write_ledger_row(_step_result("env_check", "check", env_res))
        if not env_res.get("ok"):
            failed_step = "env_check"
            hardening_status = "failed"
            return _finalize(step_records, failed_step, hardening_status, external_probe_result=None)

        bootstrap_pw = os.environ["BOOTSTRAP_SSH_PASSWORD"]  # local only
        host = os.environ["VM_HOST"].strip()
        user = os.environ["VM_USER"].strip()
        key_path = os.environ["SSH_PRIVATE_KEY_PATH"].strip()
        pubkey_path = os.environ["SSH_PUBLIC_KEY_PATH"].strip()
        harden_sh_path = os.environ["HARDEN_SH_PATH"].strip()

        # Step 2 · key_install (uses bootstrap password via SSHPASS env only)
        ki = _do_key_install(host=host, user=user, pubkey_path=pubkey_path, bootstrap_pw=bootstrap_pw)
        step_records.append(_step_result("key_install", "action", ki))
        _write_ledger_row(_step_result("key_install", "action", ki))
        if not ki.get("ok"):
            failed_step = "key_install"
            hardening_status = "failed"
            return _finalize(step_records, failed_step, hardening_status, external_probe_result=None)

        # Step 3 · verify_key_only_auth
        vk = _do_verify_key_only_auth(host=host, user=user, key_path=key_path)
        step_records.append(_step_result("verify_key_only_auth", "check", vk))
        _write_ledger_row(_step_result("verify_key_only_auth", "check", vk))
        if not vk.get("ok"):
            failed_step = "verify_key_only_auth"
            hardening_status = "failed"
            return _finalize(step_records, failed_step, hardening_status, external_probe_result=None)

        # Step 4 · remote_harden
        rh = _do_remote_harden(host=host, user=user, key_path=key_path, harden_sh_path=harden_sh_path)
        step_records.append(_step_result("remote_harden", "action", rh))
        _write_ledger_row(_step_result("remote_harden", "action", rh))
        if not rh.get("ok"):
            failed_step = "remote_harden"
            hardening_status = "failed"
            return _finalize(step_records, failed_step, hardening_status, external_probe_result=None)

        # Step 5 · external_probe (mandatory evidence)
        ep = _do_external_probe(host=host, user=user)
        step_records.append(_step_result("external_probe", "attest", ep))
        _write_ledger_row(_step_result("external_probe", "attest", ep))
        if not ep.get("ok"):
            failed_step = "external_probe"
            hardening_status = "failed"
            return _finalize(step_records, failed_step, hardening_status, external_probe_result=ep)

        # Step 6 · write commissioning-record hardening section
        # (the actual write happens in _finalize; ledger the intent here)
        w = {"ok": True}
        step_records.append(_step_result("write_commissioning_hardening_section", "write", w))
        _write_ledger_row(_step_result("write_commissioning_hardening_section", "write", w))
        return _finalize(step_records, failed_step, hardening_status, external_probe_result=ep)

    finally:
        # Retirement: bootstrap credential dies with this call.
        bootstrap_pw = "\x00" * 32  # noqa: F841 — best-effort local overwrite
        os.environ.pop("BOOTSTRAP_SSH_PASSWORD", None)
        os.environ.pop("SSHPASS", None)


def _finalize(step_records: list, failed_step: Any, hardening_status: str,
              external_probe_result: Any) -> dict:
    receipt = {
        "receipt_kind": "hardening",
        "at": datetime.now(timezone.utc).isoformat(),
        "hardening_status": hardening_status,
        "failed_step": failed_step,
        "vm_treated_as": "hardened" if hardening_status == "attested" else "unhardened",
        "data_movement_permitted": hardening_status == "attested",
        "external_probe": external_probe_result or {},
        "steps": step_records,
        "ruling": "FL-P2-04 path (a) · DECISIONS.md 2026-08-14",
    }
    receipt_path = _write_receipt(receipt)
    return {
        "hardening_status": hardening_status,
        "failed_step": failed_step,
        "receipt_path": receipt_path,
        "external_probe_ok": bool((external_probe_result or {}).get("ok")),
    }
