"""SSH seam · multi-host + password auth (BLOCKER 2 (a) authorized 2026-08-28).

Owner rulings banked in DECISIONS.md:

    BLOCKER 2 RULING → (a) — accept AKKI_GPU_SSH_PASSWORD as an alternative
    auth path when AKKI_GPU_SSH_PRIVATE_KEY_PATH is unset. Auth precedence:
    key path if set, else password, else raise (terminal case with dual-
    option message).

    OWNER INTERRUPT 2 (multi-host) — extend the seam from single-host to
    a host inventory. Per-host env vars; per-host redaction; per-host
    auth.

    OWNER INTERRUPT 3 (styling, G5 scope) — folded into Wave G5; unrelated
    to this file.

Env-var scheme:
    AKKI_GPU_HOSTS          — comma-separated inventory of host names.
                              slug = hostname.upper().replace('-', '_').
    {SLUG}_HOST             — IP.
    {SLUG}_PORT             — default 22.
    {SLUG}_USERNAME         — default ubuntu.
    {SLUG}_OS               — cosmetic, default ubuntu.
    {SLUG}_HOSTNAME_EXPECTED — hostname to verify on `hostname` command.
    {SLUG}_SSH_PRIVATE_KEY_PATH — optional; wins over password if set.
    {SLUG}_SSH_PASSWORD     — password auth (env-only; NEVER logged/committed/surfaced).

Legacy fallback: for slug=AKKI_VM_II (banked at Wave-H first-interrupt),
fall back to legacy AKKI_GPU_* env vars when the slug vars are unset.

Redaction discipline:
    - HostConfig exposes `password_present: bool`, NEVER the value.
    - env_report() returns per-host `password_set: bool`, NEVER the value.
    - execute_remote_command receipts are scrubbed via _redact() before
      write; a post-write leak check re-scrubs if anything survived.
    - RemoteExecResult has no password field.

Backward compat:
    - SSHKeyMissing retained as alias for SSHAuthUnconfigured (legacy try/except).
    - SeamResult / execute_lora_train_mock preserved verbatim.
    - execute_lora_train / execute_lora_train_real preserved with new host_slug kwarg.
    - env_report() retains legacy keys.
"""
from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================================
# Exceptions
# ============================================================================


class SSHAuthUnconfigured(RuntimeError):
    """No auth configured for the target host.

    Neither AKKI_*_SSH_PRIVATE_KEY_PATH nor AKKI_*_SSH_PASSWORD is set.
    Message names BOTH options.
    """


# Backward-compat alias: legacy code catches SSHKeyMissing.
SSHKeyMissing = SSHAuthUnconfigured


class UnknownHost(KeyError):
    """Slug not in AKKI_GPU_HOSTS inventory."""


class HostNotSelected(RuntimeError):
    """Multi-host inventory (>1) requires explicit host_slug kwarg."""


class RealSSHNotWiredYet(NotImplementedError):
    """Real full-LoRA training runner is stubbed pending a discrete R-step.

    For governed ad-hoc remote commands (CUDA verify, pip install, etc.)
    use `execute_remote_command(host_slug, cmd, purpose=...)` — that path
    IS wired here.
    """


# ============================================================================
# Result dataclasses
# ============================================================================


@dataclass(frozen=True)
class SeamResult:
    """LoRA-train result contract (unchanged from CP8 legacy)."""

    mocked: bool
    exit_code: int
    stdout_summary: str
    m_a_input: float
    m_b_input: float
    wallclock_seconds: int
    gpu_hours: float
    m_e_input: float


@dataclass(frozen=True)
class RemoteExecResult:
    """Governance-safe result for `execute_remote_command`.

    NEVER carries a password field or credential material.
    stdout_redacted / stderr_redacted have had every known secret
    replaced with '********' before this object is constructed.
    """

    rc: int
    stdout_redacted: str
    stderr_redacted: str
    wallclock_seconds: float
    receipt_id: str
    host_slug: str
    purpose: str


# ============================================================================
# HostConfig — repr never contains the password value
# ============================================================================


@dataclass(frozen=True)
class HostConfig:
    """Per-host connection config.

    - `password_present` is a boolean flag, NEVER the value.
    - The actual password lives in os.environ during the process lifetime;
      it enters paramiko via `connect()`.
    """

    name: str
    slug: str
    host: str
    port: int
    username: str
    os_family: str
    hostname_expected: str
    key_path: Optional[str]
    password_present: bool

    @property
    def auth_method(self) -> str:
        """Return 'key' | 'password' | raise SSHAuthUnconfigured."""
        if self.key_path:
            return "key"
        if self.password_present:
            return "password"
        raise SSHAuthUnconfigured(
            f"No auth configured for host {self.name!r}. "
            f"Set env var {self.slug}_SSH_PRIVATE_KEY_PATH (private key path) "
            f"or {self.slug}_SSH_PASSWORD (password). "
            f"Key path takes precedence when both are set."
        )

    def __repr__(self) -> str:
        # Explicitly redacted repr — never the password value.
        return (
            f"HostConfig(name={self.name!r}, slug={self.slug!r}, "
            f"host={self.host!r}, port={self.port}, username={self.username!r}, "
            f"os_family={self.os_family!r}, "
            f"hostname_expected={self.hostname_expected!r}, "
            f"key_path={self.key_path!r}, "
            f"password_present={self.password_present})"
        )


# ============================================================================
# Inventory helpers
# ============================================================================


def _slug_for(host_name: str) -> str:
    return host_name.replace("-", "_").upper()


def _env_get(key: str, default: str = "") -> str:
    v = os.environ.get(key)
    if v is None:
        return default
    v = v.strip()
    return v if v else default


def list_hosts() -> List[str]:
    """Return the multi-host inventory from AKKI_GPU_HOSTS. Empty if unset."""
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.workbook import read_targets
        return [target.name for target in read_targets()]
    raw = _env_get("AKKI_GPU_HOSTS")
    if not raw:
        return []
    return [h.strip() for h in raw.split(",") if h.strip()]


def _legacy_fallback_key(host_name: str) -> str:
    """Legacy key mapping — only for slug=AKKI_VM_II (Wave-H banked target)."""
    return "AKKI_VM_II" if host_name == "akki-vm-ii" else ""


def get_host_config(host_name: str) -> HostConfig:
    """Read {SLUG}_* env vars for the host; fall back to legacy for akki-vm-ii."""
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.workbook import get_target
        target = get_target(host_name)
        return HostConfig(name=target.name, slug=_slug_for(target.name), host=target.host,
                          port=target.port, username=target.username, os_family='unspecified',
                          hostname_expected=target.name, key_path=None, password_present=True)
    if host_name not in list_hosts():
        raise UnknownHost(
            f"Host {host_name!r} not in AKKI_GPU_HOSTS inventory "
            f"(current: {list_hosts()!r})"
        )
    slug = _slug_for(host_name)
    use_legacy_fallback = host_name == "akki-vm-ii"

    def read(key: str, legacy_key: str = "", default: str = "") -> str:
        v = _env_get(f"{slug}_{key}")
        if v:
            return v
        if use_legacy_fallback and legacy_key:
            v = _env_get(legacy_key)
            if v:
                return v
        return default

    host = read("HOST", legacy_key="AKKI_GPU_HOST")
    port_str = read("PORT", legacy_key="AKKI_GPU_PORT", default="22")
    try:
        port = int(port_str)
    except (TypeError, ValueError):
        port = 22
    username = read("USERNAME", legacy_key="AKKI_GPU_USERNAME", default="ubuntu")
    os_family = read("OS", legacy_key="AKKI_GPU_OS", default="ubuntu")
    hostname_expected = read(
        "HOSTNAME_EXPECTED", legacy_key="AKKI_GPU_HOSTNAME_EXPECTED", default=host_name
    )
    key_path = read("SSH_PRIVATE_KEY_PATH", legacy_key="AKKI_GPU_SSH_PRIVATE_KEY_PATH")
    key_path = key_path or None
    pwd = read("SSH_PASSWORD", legacy_key="AKKI_GPU_SSH_PASSWORD")
    password_present = bool(pwd)

    return HostConfig(
        name=host_name,
        slug=slug,
        host=host,
        port=port,
        username=username,
        os_family=os_family,
        hostname_expected=hostname_expected,
        key_path=key_path,
        password_present=password_present,
    )


def _get_password_for(host_name: str) -> str:
    """INTERNAL — read the password value. Callers must not persist the return."""
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.workbook import get_target
        return get_target(host_name).password
    slug = _slug_for(host_name)
    v = _env_get(f"{slug}_SSH_PASSWORD")
    if v:
        return v
    if host_name == "akki-vm-ii":
        v = _env_get("AKKI_GPU_SSH_PASSWORD")
    return v


# ============================================================================
# Redaction
# ============================================================================


def _all_secrets() -> List[str]:
    """Collect every known password value currently in os.environ."""
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.workbook import read_targets
        return [target.password for target in read_targets()]
    secrets: List[str] = []
    for h in list_hosts():
        slug = _slug_for(h)
        pwd = _env_get(f"{slug}_SSH_PASSWORD")
        if pwd and pwd not in secrets:
            secrets.append(pwd)
    legacy = _env_get("AKKI_GPU_SSH_PASSWORD")
    if legacy and legacy not in secrets:
        secrets.append(legacy)
    return secrets


def _redact(text: str) -> str:
    if not text:
        return text
    for s in _all_secrets():
        if s and s in text:
            text = text.replace(s, "********")
    return text


# ============================================================================
# Connection
# ============================================================================


def connect(host_name: str, timeout: int = 15):
    """Return a connected paramiko.SSHClient.

    Auth precedence: key > password > raise SSHAuthUnconfigured.
    """
    from services.gpu_direct.config import direct_enabled
    if direct_enabled():
        from services.gpu_direct.connection import connect as direct_connect
        client, _ = direct_connect(host_name, timeout=timeout)
        return client
    import paramiko  # local import; keeps unit-test collection cheap

    cfg = get_host_config(host_name)
    method = cfg.auth_method  # may raise SSHAuthUnconfigured

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    common = dict(
        hostname=cfg.host,
        port=cfg.port,
        username=cfg.username,
        timeout=timeout,
        allow_agent=False,
        look_for_keys=False,
    )
    if method == "key":
        client.connect(key_filename=cfg.key_path, **common)  # type: ignore[arg-type]
    else:
        client.connect(password=_get_password_for(host_name), **common)  # type: ignore[arg-type]
    return client


# ============================================================================
# execute_remote_command · governed ad-hoc remote execution
# ============================================================================


_RECEIPT_DIR_DEFAULT = "/app/assessment_workspace/phase0/gpu_receipts"


def _receipt_dir() -> Path:
    return Path(os.environ.get("GPU_RECEIPT_DIR", _RECEIPT_DIR_DEFAULT))


def _register_crossing_safe(host_slug: str, command: str, purpose: str) -> None:
    """Best-effort register_crossing() — never a failure path for the exec."""
    try:
        from services.chokepoint import register_crossing  # type: ignore
    except Exception:
        return
    try:
        cfg = get_host_config(host_slug)
    except Exception:
        return
    try:
        # Endpoint object with the two attrs chokepoint reads.
        endpoint = type("Endpoint", (), {"host": cfg.host, "region": "vendor-managed"})()
        register_crossing(
            kind="ssh_seam_remote_exec",
            endpoint=endpoint,
            verb="EXEC",
            payload_shape={"command_length": len(command), "purpose": purpose},
            actor=f"services.training_runner.ssh_seam · {host_slug}",
            masking_tier="attested_command",
        )
    except Exception:
        # Chokepoint may refuse or be misconfigured; the seam does not depend on it.
        pass


def execute_remote_command(
    host_slug: str,
    command: str,
    *,
    purpose: str,
    timeout: int = 60,
) -> RemoteExecResult:
    """Governed remote command execution.

    Steps:
      1. register_crossing() best-effort (audit).
      2. connect(host_slug) — auth precedence (key > password > raise).
      3. paramiko exec_command(command, timeout).
      4. Redact all known secrets from stdout/stderr.
      5. Write a ledgered receipt to phase0/gpu_receipts/ (redacted).
      6. Return RemoteExecResult (never carries a password field).
    """
    receipt_id = f"gpurcp-{uuid.uuid4().hex[:12]}"
    _register_crossing_safe(host_slug, command, purpose)

    t0 = time.monotonic()
    try:
        client = connect(host_slug, timeout=timeout)
    except Exception as e:
        # Redact e in case paramiko surfaced any credential.
        err_msg = _redact(f"connect failed: {type(e).__name__}: {e}")
        return RemoteExecResult(
            rc=-1,
            stdout_redacted="",
            stderr_redacted=err_msg,
            wallclock_seconds=time.monotonic() - t0,
            receipt_id=receipt_id,
            host_slug=host_slug,
            purpose=purpose,
        )

    try:
        _stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
    finally:
        try:
            client.close()
        except Exception:
            pass

    out_r = _redact(out)
    err_r = _redact(err)
    dt = time.monotonic() - t0

    result = RemoteExecResult(
        rc=rc,
        stdout_redacted=out_r,
        stderr_redacted=err_r,
        wallclock_seconds=dt,
        receipt_id=receipt_id,
        host_slug=host_slug,
        purpose=purpose,
    )

    # Persist redacted receipt to disk.
    try:
        rdir = _receipt_dir()
        rdir.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        safe_purpose = "".join(c if c.isalnum() or c in "-_" else "_" for c in purpose)[:60]
        p = rdir / f"{ts}_{host_slug.replace('-', '_')}_{safe_purpose}_{receipt_id}.log"
        body_lines = [
            f"# receipt_id: {receipt_id}",
            f"# host_slug: {host_slug}",
            f"# purpose: {purpose}",
            f"# rc: {rc}",
            f"# wallclock_seconds: {dt:.3f}",
            f"# at_utc: {ts}",
            "",
            "## COMMAND",
            command,
            "",
            "## STDOUT (redacted)",
            out_r,
            "",
            "## STDERR (redacted)",
            err_r,
        ]
        body = "\n".join(body_lines)
        # Final belt-and-braces leak check.
        for s in _all_secrets():
            if s and s in body:
                body = body.replace(s, "********")
                body += "\n\n!!! LEAK_SCAN_RESCRUBBED · secret survived initial redact !!!\n"
        p.write_text(body)
    except Exception:
        # Receipt persistence is best-effort; result is authoritative.
        pass

    return result


# ============================================================================
# Legacy LoRA train dispatch (preserved · with host_slug kwarg)
# ============================================================================


def current_mode() -> str:
    return _env_get("GPU_CONNECT_MODE", default="mock").lower() or "mock"


def is_mock() -> bool:
    return current_mode() == "mock"


def is_real() -> bool:
    return current_mode() == "real"


def execute_lora_train_mock(
    recipe_version: str, base_model_id: str, material_admit_ref: str
) -> SeamResult:
    """CP8 canned execution (unchanged from pre-refactor behaviour)."""
    h = sum(ord(c) for c in recipe_version) % 100
    return SeamResult(
        mocked=True,
        exit_code=0,
        stdout_summary=(
            f"mock trainer run: recipe={recipe_version} base={base_model_id} "
            f"material={material_admit_ref}. Nothing was actually trained; "
            f"mocked=True end-to-end."
        ),
        m_a_input=0.10 + (h / 1000.0),
        m_b_input=0.05 - (h / 5000.0),
        wallclock_seconds=1200 + h * 10,
        gpu_hours=0.3 + h / 200.0,
        m_e_input=0.85 + (h / 5000.0),
    )


def execute_lora_train_real(
    recipe_version: str,
    base_model_id: str,
    material_admit_ref: str,
    *,
    host_slug: Optional[str] = None,
) -> SeamResult:
    """Real LoRA training run — routes to a named host in the inventory.

    host_slug precedence:
      - explicit kwarg wins.
      - if only 1 host in inventory: use it.
      - if >1 in inventory AND no kwarg: raise HostNotSelected.
      - if 0 in inventory: legacy single-host path (raises SSHAuthUnconfigured
        or RealSSHNotWiredYet).
    """
    hosts = list_hosts()
    if host_slug is None:
        if len(hosts) == 1:
            host_slug = hosts[0]
        elif len(hosts) > 1:
            raise HostNotSelected(
                f"Multi-host inventory ({hosts!r}) requires an explicit "
                f"host_slug kwarg on execute_lora_train_real."
            )
        else:
            # Legacy single-host mode (no inventory, no slug).
            if not _env_get("AKKI_GPU_SSH_PRIVATE_KEY_PATH") and not _env_get("AKKI_GPU_SSH_PASSWORD"):
                raise SSHAuthUnconfigured(
                    "GPU_CONNECT_MODE=real with no AKKI_GPU_HOSTS inventory and "
                    "no legacy auth. Set AKKI_GPU_SSH_PRIVATE_KEY_PATH (private key path) "
                    "or AKKI_GPU_SSH_PASSWORD (password). Key path takes precedence."
                )
            raise RealSSHNotWiredYet(
                "Real LoRA training loop is stubbed on the legacy single-host path. "
                "Set AKKI_GPU_HOSTS to migrate to multi-host inventory + use "
                "execute_remote_command for governed ad-hoc commands."
            )

    # Multi-host path: validate config + auth.
    cfg = get_host_config(host_slug)
    _ = cfg.auth_method  # raises SSHAuthUnconfigured if neither key nor pwd

    # W-Shield-Train-build (2026-09-06): unstub. The pre-r2 unconditional
    # `RealSSHNotWiredYet` raise is gone. Instead, delegate to the
    # governed pipeline (`services.shield_train.pipeline.execute_governed_lora_run`)
    # which checks the masking-tier admission via
    # `services.chokepoint.masking_tier` and raises `MaskingTierNotAdmitted`
    # while admission remains parked. The STUB is gone; the ADMISSION GATE
    # is what remains as the honest block. Default tier for this seam is
    # `t1_full_mask` (full de-identify + re-identify per Doc 01 §A5.2) —
    # callers pin an alternate tier via AKKI_LORA_MASKING_TIER env var.
    from services.shield_train import pipeline as _shield_pipeline
    tier = os.environ.get("AKKI_LORA_MASKING_TIER", "t1_full_mask")
    return _shield_pipeline.execute_governed_lora_run(
        tier=tier,
        recipe_version=recipe_version,
        base_model_id=base_model_id,
        material_admit_ref=material_admit_ref,
        host_slug=host_slug,
        table_context=os.environ.get(
            "AKKI_LORA_TABLE_CONTEXT", "ussd_question_response"
        ),
        slice_size=int(os.environ.get("AKKI_LORA_SLICE_SIZE", "0")),
        backend_execute=None,  # backend wiring lands in W-Shield-Train-run
        ssh_seam=None,         # seam wiring lands in W-Shield-Train-run
    )


def execute_lora_train(
    recipe_version: str,
    base_model_id: str,
    material_admit_ref: str,
    *,
    host_slug: Optional[str] = None,
) -> SeamResult:
    """Dispatch by GPU_CONNECT_MODE."""
    if is_real():
        return execute_lora_train_real(
            recipe_version, base_model_id, material_admit_ref, host_slug=host_slug
        )
    return execute_lora_train_mock(recipe_version, base_model_id, material_admit_ref)


# ============================================================================
# env_report — multi-host shape, fully redacted
# ============================================================================


def env_report() -> Dict:
    """Report seam env state with per-host redacted flags.

    NEVER contains password values. Legacy fields retained transitionally.
    """
    hosts_state: Dict[str, Dict[str, bool]] = {}
    for h in list_hosts():
        slug = _slug_for(h)
        hosts_state[h] = {
            "slug": slug,
            "host_set": bool(_env_get(f"{slug}_HOST")),
            "username_set": bool(_env_get(f"{slug}_USERNAME")),
            "port_set": bool(_env_get(f"{slug}_PORT")),
            "key_path_set": bool(_env_get(f"{slug}_SSH_PRIVATE_KEY_PATH")),
            "password_set": bool(_env_get(f"{slug}_SSH_PASSWORD")),
        }
    return {
        "GPU_CONNECT_MODE": current_mode(),
        "hosts_inventory": list_hosts(),
        "hosts": hosts_state,
        # Legacy fields (transitional; retire in a later cycle).
        "AKKI_GPU_HOST_set": "yes" if _env_get("AKKI_GPU_HOST") else "no",
        "AKKI_GPU_SSH_PRIVATE_KEY_PATH_set":
            "yes" if _env_get("AKKI_GPU_SSH_PRIVATE_KEY_PATH") else "no",
        "AKKI_GPU_SSH_PASSWORD_set":
            "yes" if _env_get("AKKI_GPU_SSH_PASSWORD") else "no",
    }
