"""Wave-H · install torch stack on GPU host(s) through ssh_seam.execute_remote_command.

BLOCKER 1 (a) authorized 2026-08-28. Every install step registers a crossing
via chokepoint and banks a redacted receipt to phase0/gpu_receipts/.

Order per remote host:
  1. python3 -m pip via ensurepip (pip3 not installed on hosts).
  2. pip install --user torch (cu128 wheel index to match CUDA 12.8 runtime).
  3. pip install --user pynvml transformers accelerate peft.
  4. Verify: python3 -c "import torch; ..." + version + cuda_available + device_count.
  5. Emit a summary JSON per host.

Deferred (per owner ruling): xformers, triton, bitsandbytes.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Load .env into os.environ so ssh_seam finds credentials.
ENV_PATH = "/app/backend/.env"
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())

sys.path.insert(0, "/app/assessment_workspace/repos/Extraction-Akki/backend")
from services.training_runner import ssh_seam  # noqa: E402


TORCH_INDEX_URL = "https://download.pytorch.org/whl/cu128"

# Per-step recipe. Timeouts generous for torch (~2 GB wheel).
# NO `| tail` at end — that swallows pip's non-zero rc.
STEPS = [
    (
        "apt_update",
        "sudo -n DEBIAN_FRONTEND=noninteractive apt-get update -qq 2>&1",
        300,
    ),
    (
        "apt_install_pip",
        "sudo -n DEBIAN_FRONTEND=noninteractive apt-get install -y "
        "python3-pip python3-dev 2>&1",
        600,
    ),
    (
        "pip_version",
        "python3 -m pip --version 2>&1",
        30,
    ),
    (
        "pip_upgrade",
        "python3 -m pip install --break-system-packages --upgrade "
        "pip setuptools wheel 2>&1",
        300,
    ),
    (
        "pip_install_torch",
        f"python3 -m pip install --break-system-packages "
        f"--index-url {TORCH_INDEX_URL} torch 2>&1",
        900,
    ),
    (
        "pip_install_ml_stack",
        "python3 -m pip install --break-system-packages "
        "pynvml transformers accelerate peft 2>&1",
        900,
    ),
    (
        "torch_verify",
        "python3 -c \"import torch; "
        "print('torch_version', torch.__version__); "
        "print('cuda_available', torch.cuda.is_available()); "
        "print('cuda_version_torch', torch.version.cuda); "
        "print('gpu_count', torch.cuda.device_count()); "
        "print('device_0_name', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')\" 2>&1",
        60,
    ),
    (
        "modules_verify",
        "python3 -c \""
        "import pynvml, transformers, accelerate, peft; "
        "print('pynvml', pynvml.__version__ if hasattr(pynvml,'__version__') else '<no __version__>'); "
        "print('transformers', transformers.__version__); "
        "print('accelerate', accelerate.__version__); "
        "print('peft', peft.__version__)\" 2>&1",
        60,
    ),
]


def install_on_host(host_slug: str, dry_run: bool = False) -> dict:
    print(f"\n{'='*70}")
    print(f"HOST: {host_slug}  ·  installing torch stack via ssh_seam.execute_remote_command")
    print(f"{'='*70}")
    outcomes = []
    for label, cmd, timeout in STEPS:
        print(f"\n[{host_slug}] {label} (timeout={timeout}s) ...")
        if dry_run:
            outcomes.append({"label": label, "rc": None, "dry_run": True})
            continue
        t0 = time.monotonic()
        try:
            r = ssh_seam.execute_remote_command(
                host_slug=host_slug,
                command=cmd,
                purpose=f"wave_h_install_{label}",
                timeout=timeout,
            )
        except Exception as e:
            print(f"  EXCEPTION: {type(e).__name__}: {e}")
            outcomes.append({"label": label, "exception": f"{type(e).__name__}: {e}"})
            continue
        wall = time.monotonic() - t0
        # Print truncated output (already redacted)
        out_head = "\n".join(r.stdout_redacted.splitlines()[:5]) if r.stdout_redacted else "(empty)"
        out_tail = "\n".join(r.stdout_redacted.splitlines()[-5:]) if r.stdout_redacted else "(empty)"
        print(f"  rc={r.rc}  wall={wall:.1f}s  wallclock_reported={r.wallclock_seconds:.1f}s")
        print(f"  receipt_id={r.receipt_id}")
        print(f"  stdout HEAD:\n    " + "\n    ".join(out_head.splitlines()))
        if len(r.stdout_redacted.splitlines()) > 10:
            print(f"  ...")
            print(f"  stdout TAIL:\n    " + "\n    ".join(out_tail.splitlines()))
        if r.stderr_redacted.strip():
            print(f"  stderr (first 500 chars): {r.stderr_redacted[:500]}")
        outcomes.append({
            "label": label,
            "rc": r.rc,
            "wallclock_seconds": r.wallclock_seconds,
            "receipt_id": r.receipt_id,
            "stdout_tail": out_tail[-800:],
            "stderr_tail": r.stderr_redacted[-500:] if r.stderr_redacted else "",
        })
    return {"host_slug": host_slug, "steps": outcomes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="all",
                        help="host slug or 'all' (default: all)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    hosts = ssh_seam.list_hosts()
    if args.host != "all":
        hosts = [args.host] if args.host in hosts else []
        if not hosts:
            print(f"host {args.host!r} not in inventory")
            return 1
    print(f"# Wave-H install torch stack · hosts: {hosts} · dry_run={args.dry_run}")
    print(f"# torch index: {TORCH_INDEX_URL}")

    summary = []
    for h in hosts:
        r = install_on_host(h, dry_run=args.dry_run)
        summary.append(r)

    # Emit summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for h in summary:
        print(f"\nhost: {h['host_slug']}")
        for step in h["steps"]:
            if step.get("dry_run"):
                print(f"  {step['label']}: DRY-RUN")
            elif "exception" in step:
                print(f"  {step['label']}: EXCEPTION · {step['exception']}")
            else:
                mark = "OK" if step["rc"] == 0 else "FAIL"
                print(f"  {step['label']}: {mark} rc={step['rc']} wall={step['wallclock_seconds']:.1f}s")

    # Save summary
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    summary_path = Path("/app/assessment_workspace/phase0/gpu_receipts") / f"{ts}_wave_h_install_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nsummary saved: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
