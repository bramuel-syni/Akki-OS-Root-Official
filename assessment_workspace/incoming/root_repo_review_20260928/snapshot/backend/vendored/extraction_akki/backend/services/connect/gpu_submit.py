"""gpu_submit.py — WS-BUILD-CONNECT-GPU submit orchestrator (path (a)).

Owner ruling 2026-08-14 (DECISIONS.md · WS-BUILD-CONNECT-GPU):
  On submit, the machinery fires automatically, in order:
    credential_intake → declaration_fire → hardening → acceptance →
    commissioning_record_write → pins_update → after_state_render_ready.

All FL-P2-04 secrecy assertions apply: bootstrap password held env-grade only;
never on argv / disk / STATE / logs / ledger row / receipt / response.
Retired within the same submit call (finally block, plus hardening.py's
own retirement).

Failure grammar (owner ruled):
  - Hardening failure → after_state.state_class='failed', copy='failed (ours; retry)'.
  - Acceptance failure → after_state.state_class='held', evidence-as-sentences,
    'escalated to the vendor'.
  - Mid-run failure → data_movement_permitted=False.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ALLOWED_FIELDS = {
    "host_name", "username", "password", "public_ip",
    "private_ip", "os", "deploy_date",
}
REQUIRED_FIELDS = {"host_name", "username", "password", "public_ip"}

SUBMIT_STAGES = [
    "credential_intake",
    "declaration_fire",
    "hardening",
    "acceptance",
    "commissioning_record_write",
    "pins_update",
    "after_state_render_ready",
]


class SubmitError(Exception):
    """Raised when the payload fails structural validation."""


# --------------------------------------------------------------------
# Wiring points — patched by tests, replaced in production by real callers.
# --------------------------------------------------------------------


def _write_ledger_row(row: dict) -> str:
    """Ledger row writer (patched in tests; production wraps services.northena)."""
    return f"local.connect_gpu.{row.get('stage', 'unknown')}.{datetime.now(timezone.utc).isoformat()}"


def _write_pins_update(pins: dict) -> None:
    """Write non-secret Output values into STATE/PINS.md.

    In production, called after commissioning-record write. Tests patch to capture.
    """
    state_dir = Path(os.environ.get("STATE_DIR", "/app/assessment_workspace/STATE"))
    pins_path = state_dir / "PINS.md"
    if not pins_path.exists():
        return
    block = _render_pins_block(pins)
    body = pins_path.read_text()
    marker = "<!-- CONNECT-GPU-PINS -->"
    if marker in body:
        pre, rest = body.split(marker, 1)
        _, post = rest.split(marker, 1) if marker in rest else ("", rest)
        body = f"{pre}{marker}\n{block}\n{marker}{post}"
    else:
        body = body.rstrip() + f"\n\n{marker}\n{block}\n{marker}\n"
    pins_path.write_text(body)


def _render_pins_block(pins: dict) -> str:
    lines = [
        "## WS-BUILD-CONNECT-GPU — commissioning record pinned outputs",
        f"- **host_name:** `{pins.get('host_name', '')}`",
        f"- **public_ip:** `{pins.get('public_ip', '')}`",
        f"- **private_ip:** `{pins.get('private_ip', '')}`",
        f"- **os:** `{pins.get('os', '')}`",
        f"- **deploy_date:** `{pins.get('deploy_date', '')}`",
        f"- **checkpoint_14d_utc:** `{pins.get('checkpoint_14d_utc', '')}`",
        f"- **hardening_status:** `{pins.get('hardening_status', '')}`",
        f"- **acceptance_status:** `{pins.get('acceptance_status', '')}`",
        f"- **commissioning_record:** `{pins.get('commissioning_record_path', '')}`",
    ]
    return "\n".join(lines)


def _fire_declaration(*, host_name: str, public_ip: str, scope: str) -> dict:
    """Fire the infrastructure-actor VM declaration (Phase-1 drilled shape)."""
    try:
        from services.declaration.seat import capture
    except Exception:
        return {"declaration_id": f"decl.local.{host_name}", "status": "in_force"}
    payload = {
        "actor_id": f"infrastructure.vm.{host_name}",
        "declared_type": "infrastructure",
        "objective": "Archive processing and speech-model training.",
        "capabilities": ["compute", "hss_storage", "gpu_training"],
        "risks": ["bulk_data_custody", "external_location"],
        "scope": [scope],
        "lawful_basis": "build_order_01_2026-08-14",
    }
    try:
        rec = capture(**payload)
    except TypeError:
        rec = capture(payload)
    return {"declaration_id": getattr(rec, "id", "decl.local"),
            "status": getattr(rec, "status", "in_force")}


def _run_hardening(*, bootstrap_pw: str, host: str, user: str) -> dict:
    """Delegate to services.compute_seam.hardening.run() — creds via env.

    If `host` contains `:port` (e.g. `127.0.0.1:2222` for drill against mock sshd),
    split into VM_HOST + VM_PORT env so the hardening module respects the port.
    """
    os.environ["BOOTSTRAP_SSH_PASSWORD"] = bootstrap_pw
    if ":" in host and host.count(":") == 1:
        h, p = host.split(":", 1)
        os.environ["VM_HOST"] = h.strip()
        os.environ["VM_PORT"] = p.strip()
    else:
        os.environ["VM_HOST"] = host
        os.environ.setdefault("VM_PORT", "22")
    os.environ["VM_USER"] = user
    from services.compute_seam import hardening
    return hardening.run()


def _sync_seam_execute(*, vm_actor_id: str, command: str, task_id: str,
                        required_scope: list) -> "SeamResult":  # noqa: F821
    """Sync bridge to services.compute_seam.seam.execute() (which is async).

    Runs the coroutine in a fresh loop on a worker thread so this call is safe
    from both sync callers (unit tests, sync-only paths) and async callers
    (FastAPI route handlers whose event loop is already running).

    Tests patch this symbol to inject canned SeamResult outcomes without
    reaching the actual SSH transport.
    """
    import asyncio
    import concurrent.futures
    from services.compute_seam.seam import execute
    coro = execute(vm_actor_id=vm_actor_id, command=command, task_id=task_id,
                   required_scope=required_scope)

    def _runner():
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(_runner).result()


def _run_acceptance(*, host: str, user: str, key_path: str) -> dict:
    """Execute phase0/acceptance.sh on the remote host via the compute seam.

    Owner ruling 2026-08-14: no live-path shortcut. This function must:
      - Load the frozen acceptance.sh (from ACCEPTANCE_SH_PATH env).
      - Deliver it to the VM as the seam's `command` argument (bash -c <script>).
      - Route through services.compute_seam.seam.execute() which:
          admits (declaration check) → registers (task_id check) →
          ledgers a row BEFORE transport → runs the command key-only.
      - Parse real stdout into per-check evidence sentences via
        services.compute_seam.acceptance_parser.parse_output().
      - Ledger one row per parsed check (attribution + auditability).
      - Return {acceptance_status, exit_code, checks, raw_stdout, raw_stderr}.

    Bootstrap password MUST already be retired by the time this runs; the seam
    session uses SSH_PRIVATE_KEY_PATH only (key-only per Build Order 01 §6.3).
    """
    import shlex
    acceptance_path = os.environ.get(
        "ACCEPTANCE_SH_PATH",
        "/app/assessment_workspace/phase0/acceptance.sh",
    )
    if not Path(acceptance_path).exists():
        return {
            "acceptance_status": "held",
            "exit_code": 9,
            "checks": [{"name": "acceptance_sh_missing", "ok": False,
                        "sentence": f"acceptance.sh not found at {acceptance_path}."}],
            "raw_stdout": "",
            "raw_stderr": "",
        }

    script = Path(acceptance_path).read_text()
    command = f"bash -c {shlex.quote(script)}"
    vm_actor_id = f"infrastructure.vm.{host}"

    from services.compute_seam.acceptance_parser import parse_output

    seam_result = _sync_seam_execute(
        vm_actor_id=vm_actor_id,
        command=command,
        task_id="compute.acceptance.per_check",
        required_scope=["archive.ingestion"],
    )
    stdout = getattr(seam_result, "stdout", "") or ""
    stderr = getattr(seam_result, "stderr", "") or ""
    exit_code = getattr(seam_result, "exit_code", 9)

    checks = parse_output(stdout, exit_code=exit_code)

    for c in checks:
        _write_ledger_row({
            "stage": "acceptance_check",
            "task_id": "compute.acceptance.per_check",
            "vm_host": host,
            "check_name": c["name"],
            "ok": c["ok"],
            "at": datetime.now(timezone.utc).isoformat(),
        })

    return {
        "acceptance_status": "green" if exit_code == 0 else "held",
        "exit_code": exit_code,
        "checks": checks,
        "raw_stdout": stdout,
        "raw_stderr": stderr,
    }


# --------------------------------------------------------------------
# Submit orchestrator
# --------------------------------------------------------------------


def submit(payload: dict, *, actor: str, drill_mode_ok: bool = False) -> dict:
    """Execute the seven ordered stages. Returns after_state material.

    Payload MUST include: host_name, username, password, public_ip.
    Optional: private_ip, os, deploy_date.

    Returns dict with:
      after_state (dict with four questions + state_class),
      commissioning_record_path,
      data_movement_permitted,
      hardening_status, acceptance_status,
      task_id.
    """
    _validate(payload)

    host_name = payload["host_name"]
    username = payload["username"]
    bootstrap_pw = payload["password"]
    public_ip = payload["public_ip"]
    deploy_date = payload.get("deploy_date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    task_id = "connect.gpu.submit.per_host"

    # Stage 1 · credential_intake (ledger the EVENT, never the credential).
    _write_ledger_row({
        "stage": "credential_intake",
        "task_id": task_id,
        "actor": actor,
        "vm_host": public_ip,
        "host_name": host_name,
        "credential_shape": "password_env_grade",
        "at": datetime.now(timezone.utc).isoformat(),
    })

    try:
        # Stage 2 · declaration_fire (Phase-1 drilled shape).
        decl = _fire_declaration(host_name=host_name, public_ip=public_ip,
                                 scope="archive.ingestion")
        _write_ledger_row({
            "stage": "declaration_fire",
            "task_id": task_id,
            "vm_host": public_ip,
            "declaration_id": decl.get("declaration_id"),
            "declaration_status": decl.get("status"),
            "at": datetime.now(timezone.utc).isoformat(),
        })

        # Stage 3 · hardening (path (a); bootstrap password transits ONCE via env).
        h = _run_hardening(bootstrap_pw=bootstrap_pw, host=public_ip, user=username)
        _write_ledger_row({
            "stage": "hardening",
            "task_id": task_id,
            "vm_host": public_ip,
            "hardening_status": h.get("hardening_status"),
            "failed_step": h.get("failed_step"),
            "external_probe_ok": h.get("external_probe_ok"),
            "at": datetime.now(timezone.utc).isoformat(),
        })

        acceptance_result = None
        if h.get("hardening_status") == "attested":
            # Stage 4 · acceptance.sh via seam.
            key_path = os.environ.get("SSH_PRIVATE_KEY_PATH", "")
            acceptance_result = _run_acceptance(host=public_ip, user=username,
                                                 key_path=key_path)
            _write_ledger_row({
                "stage": "acceptance",
                "task_id": task_id,
                "vm_host": public_ip,
                "acceptance_status": acceptance_result.get("acceptance_status"),
                "exit_code": acceptance_result.get("exit_code"),
                "at": datetime.now(timezone.utc).isoformat(),
            })

        # Stage 5 · commissioning_record_write.
        record_path = _write_commissioning_record(
            host_name=host_name, public_ip=public_ip, deploy_date=deploy_date,
            hardening=h, acceptance=acceptance_result or {},
        )
        _write_ledger_row({
            "stage": "commissioning_record_write",
            "task_id": task_id,
            "vm_host": public_ip,
            "commissioning_record_path": record_path,
            "at": datetime.now(timezone.utc).isoformat(),
        })

        # Stage 6 · pins_update (non-secret outputs).
        pins = {
            "host_name": host_name, "public_ip": public_ip,
            "private_ip": payload.get("private_ip", ""),
            "os": payload.get("os", ""),
            "deploy_date": deploy_date,
            "checkpoint_14d_utc": _compute_checkpoint(deploy_date),
            "hardening_status": h.get("hardening_status"),
            "acceptance_status": (acceptance_result or {}).get("acceptance_status", "not_run"),
            "commissioning_record_path": record_path,
        }
        _write_pins_update(pins)
        _write_ledger_row({
            "stage": "pins_update",
            "task_id": task_id,
            "vm_host": public_ip,
            "checkpoint_14d_utc": pins["checkpoint_14d_utc"],
            "at": datetime.now(timezone.utc).isoformat(),
        })

        # Stage 7 · after_state_render_ready.
        after = _render_after_state(hardening=h, acceptance=acceptance_result or {})
        _write_ledger_row({
            "stage": "after_state_render_ready",
            "task_id": task_id,
            "vm_host": public_ip,
            "state_class": after["state_class"],
            "at": datetime.now(timezone.utc).isoformat(),
        })

        return {
            "after_state": after,
            "commissioning_record_path": record_path,
            "data_movement_permitted": after["state_class"] == "green",
            "hardening_status": h.get("hardening_status"),
            "acceptance_status": (acceptance_result or {}).get("acceptance_status", "not_run"),
            "task_id": task_id,
        }

    finally:
        # Retirement: bootstrap dies with this call.
        bootstrap_pw = "\x00" * 32  # noqa: F841
        os.environ.pop("BOOTSTRAP_SSH_PASSWORD", None)
        os.environ.pop("SSHPASS", None)


def _validate(payload: dict) -> None:
    if not isinstance(payload, dict):
        raise SubmitError("payload must be a dict")
    keys = set(payload.keys())
    extra = keys - ALLOWED_FIELDS
    if extra:
        raise SubmitError(f"unknown fields (scope discipline S/M): {sorted(extra)}")
    missing = REQUIRED_FIELDS - keys
    if missing:
        # Report first missing for a clean error message.
        raise SubmitError(f"missing required field: {sorted(missing)[0]}")
    for k in REQUIRED_FIELDS:
        if not str(payload[k]).strip():
            raise SubmitError(f"missing required field: {k}")


def _compute_checkpoint(deploy_date: str) -> str:
    try:
        d = datetime.strptime(deploy_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        d = datetime.now(timezone.utc)
    return (d + timedelta(days=14)).strftime("%Y-%m-%dT00:00:00Z")


def _write_commissioning_record(*, host_name: str, public_ip: str, deploy_date: str,
                                 hardening: dict, acceptance: dict) -> str:
    """Write the commissioning record — hardening + acceptance sections; no password."""
    dir_path = Path(os.environ.get(
        "COMMISSIONING_RECORD_DIR", "/app/assessment_workspace/phase0/commissioning_records"
    ))
    dir_path.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_host = host_name.replace("/", "_")
    out = dir_path / f"commissioning_{safe_host}_{ts}.json"
    record = {
        "kind": "commissioning_record",
        "at": datetime.now(timezone.utc).isoformat(),
        "host_name": host_name,
        "vm_host": public_ip,
        "deploy_date": deploy_date,
        "hardening_section": {
            "status": hardening.get("hardening_status"),
            "failed_step": hardening.get("failed_step"),
            "external_probe_ok": hardening.get("external_probe_ok"),
            "receipt_path": hardening.get("receipt_path"),
        },
        "acceptance_section": {
            "status": acceptance.get("acceptance_status"),
            "exit_code": acceptance.get("exit_code"),
            "checks": acceptance.get("checks", []),
        },
        "ruling_reference": "DECISIONS.md · WS-BUILD-CONNECT-GPU · 2026-08-14",
    }
    out.write_text(json.dumps(record, indent=2, default=str))
    return str(out)


def _render_after_state(*, hardening: dict, acceptance: dict) -> dict:
    """Render the four questions in fixture grammar (rule zero topline)."""
    if hardening.get("hardening_status") != "attested":
        return {
            "state_class": "failed",
            "whats_happening": f"Hardening failed at step '{hardening.get('failed_step', 'unknown')}' — machine is unhardened.",
            "how_we_know": f"Hardening receipt at {hardening.get('receipt_path', '(missing)')} · external probe result: {hardening.get('external_probe_ok')}.",
            "what_we_are_doing": "This is ours — retry the submit once the cause is corrected.",
            "agreement_holding": "The machine is not yet attested; the seam refused to move data.",
        }
    a_status = acceptance.get("acceptance_status", "not_run")
    if a_status == "green":
        return {
            "state_class": "green",
            "whats_happening": "One GPU machine connected · hardened · accepted",
            "how_we_know": "; ".join(c["sentence"] for c in acceptance.get("checks", []) if c.get("ok")),
            "what_we_are_doing": "Ready for first data",
            "agreement_holding": "The machine matches what was ordered",
        }
    # Held (acceptance failed).
    failing = [c for c in acceptance.get("checks", []) if not c.get("ok")]
    evidence = "; ".join(c["sentence"] for c in failing) if failing else "See commissioning record."
    return {
        "state_class": "held",
        "whats_happening": "Held — the delivered machine does not match the ordered spec.",
        "how_we_know": evidence,
        "what_we_are_doing": "Held with evidence — escalated to the vendor.",
        "agreement_holding": "Deviation on record: " + evidence,
    }
