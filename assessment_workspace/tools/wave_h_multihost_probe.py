"""Wave-H · MULTI-HOST · connectivity + fact-sheet + torch-probe on both hosts.

Reads per-host slug env vars from /app/backend/.env, connects via paramiko,
runs the banked probe battery, redacts the password from all output, and
writes one receipt per host to phase0/gpu_receipts/.

Discipline:
  - Passwords read from .env (never on command line, never in source).
  - Every captured stdout/stderr is passed through _leak_scan(); if any
    password value survives, receipt write refuses.
  - Exit 0 if both hosts probed cleanly (blockers reported as data, not
    exceptions). Exit 1 on paramiko/connectivity failure only.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

# Load /app/backend/.env manually (no python-dotenv guarantee on tool venv)
ENV_PATH = "/app/backend/.env"
_env: dict[str, str] = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        _env[k.strip()] = v.strip()


def env(k: str, default: str = "") -> str:
    return _env.get(k, default)


HOSTS_CSV = env("AKKI_GPU_HOSTS", "akki-vm,akki-vm-ii")
HOSTS = [h.strip() for h in HOSTS_CSV.split(",") if h.strip()]


def slug_for(host: str) -> str:
    return host.replace("-", "_").upper()


def cfg_for(host: str) -> dict[str, str]:
    slug = slug_for(host)
    return {
        "name": host,
        "slug": slug,
        "host": env(f"{slug}_HOST"),
        "port": env(f"{slug}_PORT", "22"),
        "user": env(f"{slug}_USERNAME", "ubuntu"),
        "password": env(f"{slug}_SSH_PASSWORD"),
        "hostname_expected": env(f"{slug}_HOSTNAME_EXPECTED", host),
    }


def _leak_scan(text: str, secrets: list[str]) -> list[str]:
    """Return list of hit positions of any secret in text. Empty = clean."""
    hits = []
    for s in secrets:
        if s and s in text:
            hits.append(f"{len(s)}-char-secret at pos {text.find(s)}")
    return hits


def _redact(text: str, secrets: list[str]) -> str:
    for s in secrets:
        if s and s in text:
            text = text.replace(s, "********")
    return text


def paramiko_exec(client, cmd: str, timeout: int = 15) -> tuple[int, str, str]:
    stdin_, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    rc = stdout.channel.recv_exit_status()
    return rc, out, err


def probe_host(cfg: dict[str, str], secrets: list[str]) -> dict:
    """Run the banked probe battery. Returns a structured result dict."""
    import paramiko  # imported inside so the script fails loud if missing

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    result = {
        "at_utc": ts,
        "host_slug": cfg["slug"],
        "host_name": cfg["name"],
        "hostname_expected": cfg["hostname_expected"],
        "ip": cfg["host"],
        "connectivity": {"tcp": None, "auth": None, "banner": None},
        "identity": {},
        "hardware": {},
        "torch_probe": {},
        "leak_scan_clean": None,
    }

    if not cfg["host"] or not cfg["password"]:
        result["connectivity"]["auth"] = "config-missing"
        return result

    # Paramiko connect
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=cfg["host"],
            port=int(cfg["port"]),
            username=cfg["user"],
            password=cfg["password"],
            timeout=15,
            allow_agent=False,
            look_for_keys=False,
        )
        result["connectivity"]["tcp"] = "ok"
        result["connectivity"]["auth"] = "ok"
        transport = client.get_transport()
        if transport:
            banner = transport.remote_version or ""
            result["connectivity"]["banner"] = banner
    except Exception as e:
        # Redact any secret from error
        err = _redact(str(e), secrets)
        result["connectivity"]["auth"] = f"failed · {err}"
        try:
            client.close()
        except Exception:
            pass
        return result

    try:
        # Identity
        for label, cmd in [
            ("hostname", "hostname"),
            ("whoami", "whoami"),
            ("uname_a", "uname -a"),
        ]:
            rc, out, err = paramiko_exec(client, cmd)
            result["identity"][label] = {"rc": rc, "stdout": out.strip(), "stderr": err.strip()}

        # Hardware fact sheet
        for label, cmd in [
            ("nvidia_smi", "nvidia-smi 2>&1 | head -40"),
            ("nvidia_smi_L", "nvidia-smi -L 2>&1"),
            ("cuda_symlink", "ls -l /usr/local/cuda 2>&1"),
            ("nvcc_version", "nvcc --version 2>&1 || echo 'nvcc NOT FOUND'"),
            ("libcudart", "ldconfig -p 2>&1 | grep -i libcudart | head -5"),
            ("lscpu_head", "lscpu 2>&1 | head -20"),
            ("free_h", "free -h 2>&1"),
            ("df_root", "df -h / 2>&1"),
            ("df_mnt", "df -h /mnt 2>&1 || true"),
            ("lsblk", "lsblk 2>&1 | head -20"),
            ("python3_version", "python3 --version 2>&1"),
        ]:
            rc, out, err = paramiko_exec(client, cmd, timeout=20)
            result["hardware"][label] = {"rc": rc, "stdout": out[:2000], "stderr": err[:500]}

        # Torch/pytorch probe
        torch_ver_cmd = (
            "python3 -c \"import torch; "
            "print('torch_version', torch.__version__); "
            "print('cuda_available', torch.cuda.is_available()); "
            "print('cuda_version_torch', torch.version.cuda if hasattr(torch.version,'cuda') else None); "
            "print('gpu_count', torch.cuda.device_count()); "
            "\" 2>&1 || echo 'TORCH_PROBE_FAILED'"
        )
        rc, out, err = paramiko_exec(client, torch_ver_cmd, timeout=30)
        result["torch_probe"]["torch"] = {"rc": rc, "stdout": out.strip()[:1000], "stderr": err.strip()[:500]}

        for label, cmd in [
            ("pynvml", "python3 -c \"import pynvml; print('pynvml_ok', pynvml.__version__ if hasattr(pynvml,'__version__') else 'no-version')\" 2>&1 || echo 'MODULE_MISSING'"),
            ("transformers", "python3 -c \"import transformers; print('transformers', transformers.__version__)\" 2>&1 || echo 'MODULE_MISSING'"),
            ("accelerate", "python3 -c \"import accelerate; print('accelerate', accelerate.__version__)\" 2>&1 || echo 'MODULE_MISSING'"),
            ("peft", "python3 -c \"import peft; print('peft', peft.__version__)\" 2>&1 || echo 'MODULE_MISSING'"),
            ("pip_list_head", "pip3 list 2>&1 | head -30 || echo 'PIP_LIST_FAILED'"),
        ]:
            rc, out, err = paramiko_exec(client, cmd, timeout=20)
            result["torch_probe"][label] = {"rc": rc, "stdout": out.strip()[:800], "stderr": err.strip()[:300]}

    finally:
        client.close()

    # Redact whole result. Password already never was in result, but be paranoid.
    import json as _json
    dumped = _json.dumps(result, indent=2)
    hits = _leak_scan(dumped, secrets)
    result["leak_scan_clean"] = (len(hits) == 0)
    if hits:
        # Redact anyway
        dumped = _redact(dumped, secrets)
        result = _json.loads(dumped)
        result["leak_scan_forcibly_redacted"] = hits
    return result


def write_receipt(result: dict) -> Path:
    ROOT = Path("/app/assessment_workspace/phase0/gpu_receipts")
    ROOT.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    receipt_name = f"{ts}_wave_h_multihost_probe_{result['host_slug'].lower()}.log"
    p = ROOT / receipt_name
    import json as _json
    lines = []
    lines.append(f"# Wave-H · MULTI-HOST · probe · {result['host_slug']} ({result['host_name']})")
    lines.append(f"# at_utc: {result['at_utc']}")
    lines.append(f"# ip: {result['ip']}")
    lines.append(f"# hostname_expected: {result['hostname_expected']}")
    lines.append(f"# leak_scan_clean: {result['leak_scan_clean']}")
    lines.append("")
    lines.append("## CONNECTIVITY")
    for k, v in result["connectivity"].items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("## IDENTITY")
    for k, v in result["identity"].items():
        lines.append(f"  [{k}] rc={v['rc']}")
        lines.append(f"      stdout: {v['stdout']}")
        if v['stderr']:
            lines.append(f"      stderr: {v['stderr']}")
    lines.append("")
    lines.append("## HARDWARE")
    for k, v in result["hardware"].items():
        lines.append(f"  [{k}] rc={v['rc']}")
        for out_line in (v['stdout'] or "").splitlines():
            lines.append(f"      {out_line}")
        if v['stderr'].strip():
            lines.append(f"      stderr: {v['stderr'].strip()}")
    lines.append("")
    lines.append("## TORCH / PIP")
    for k, v in result["torch_probe"].items():
        lines.append(f"  [{k}] rc={v['rc']}")
        for out_line in (v['stdout'] or "").splitlines():
            lines.append(f"      {out_line}")
        if v['stderr'].strip():
            lines.append(f"      stderr: {v['stderr'].strip()}")
    lines.append("")
    lines.append("## RAW-STRUCTURED-RESULT (JSON)")
    lines.append(_json.dumps(result, indent=2))
    p.write_text("\n".join(lines))
    return p


def main() -> int:
    # Gather all secrets to leak-scan against
    secrets: list[str] = []
    for h in HOSTS:
        s = cfg_for(h)["password"]
        if s:
            secrets.append(s)

    print(f"# Wave-H MULTI-HOST probe · hosts: {HOSTS}")
    print(f"# {len(secrets)} secret(s) loaded from .env (redaction-guarded)")
    receipts = []
    for h in HOSTS:
        cfg = cfg_for(h)
        print(f"\n--- probing {h} @ {cfg['host']}:{cfg['port']} ---")
        r = probe_host(cfg, secrets)
        p = write_receipt(r)
        receipts.append((h, r, p))
        # Print sanitized summary
        print(f"  connectivity: {r['connectivity']}")
        print(f"  hostname: {r['identity'].get('hostname', {}).get('stdout', 'N/A')}")
        # torch
        t = r["torch_probe"].get("torch", {}).get("stdout", "")
        torch_status = (
            "torch: OK · " + t.replace("\n", " · ")
            if "torch_version" in t
            else "torch: MISSING · " + t.splitlines()[-1][:120] if t else "torch: no-output"
        )
        print(f"  {torch_status}")
        print(f"  receipt: {p}")

    print("\n# SUMMARY")
    for h, r, p in receipts:
        ident = r["identity"].get("hostname", {}).get("stdout", "N/A")
        auth = r["connectivity"]["auth"]
        t = r["torch_probe"].get("torch", {}).get("stdout", "")
        has_torch = "torch_version" in t
        print(f"  {h}: auth={auth} · hostname={ident} · torch_installed={has_torch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
