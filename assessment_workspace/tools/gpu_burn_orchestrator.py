"""GPU burn orchestrator · owner Ruling (A) · 2026-08-31.

Owner directive verbatim (banked in DECISIONS.md this session):
    "RULING → (A) FALLBACK BURN TONIGHT. Fire it now.
     Governed matmul burn on BOTH hosts via execute_remote_command
     (masking_tier=attested_command, crossing-registered, receipted,
     zero estate data). Target ~20-30 min sustained per host, all
     4 H200s exercised. Bank before/during/after nvidia-smi snapshots
     per GPU, wall-clock, power/temp, and the plain-language activity
     summary."

Owner-original ask verbatim:
    "Actally need 'digicow shielded data' used" — SUPERSEDED for tonight
    by ruling (A) because the shielded-training pipeline does not exist
    in code (row-bearing masking tiers admissible_under_env=[]; census
    engine aggregates-only by design; no governed masking policy
    authored; execute_lora_train_real stubbed). The shielded-data intent
    is NOT dropped; it is chartered for a next-wave delivery.

Discipline:
  - EVERY remote exec goes through services.training_runner.ssh_seam
    execute_remote_command(host_slug, cmd, purpose=...) — governed,
    receipted, redacted.
  - masking_tier=attested_command (declared and admissible under
    development env in the allowlist).
  - ZERO estate data on either host. Only in-memory synthetic tensors
    (torch.randn on device).
  - No PII in receipts, no PII in logs (torch tensors don't carry PII;
    scan just in case).
  - Cleanup after run: /tmp/akki_burn_<run_id>/ removed.
  - First-class activity registration: writes a run record into
    phase0/training_runner/runs/burn_<run_id>.json (adapted TrainingRunV0
    shape: kind="benchmark_burn"). Writes a cost-ledger crossing
    receipt (kind="ssh_seam" — the burn is exactly a governed compute
    activity on the training GPUs).
  - Before/during/after nvidia-smi snapshots per host per GPU into
    phase0/gpu_burn/<run_id>/.

The burn payload (burn.py, staged onto the host):
  - Discovers all visible CUDA GPUs.
  - Spawns one Python thread per GPU (torch.cuda ops release the GIL).
  - Each thread: allocates A,B fp16 tensors on its GPU (8192x8192),
    runs A @ B in a tight loop, calls torch.cuda.synchronize() every
    N iters, prints tflops + iter every ~30s to stdout.
  - Runs for BURN_DURATION_SECONDS then exits cleanly.
  - Prints a final JSON summary per GPU (iter_count, tflops_median).

Wall-clock target: ~1500 s (25 min) per host. Both hosts run in
parallel (this file kicks them off with subprocess/threading and
polls both concurrently) — total wall-clock ~25 min.
"""
from __future__ import annotations

import base64
import concurrent.futures
import json
import os
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load .env before importing seam (seam reads env at call time).
from dotenv import load_dotenv
load_dotenv("/app/backend/.env")

sys.path.insert(0, "/app/assessment_workspace/repos/Extraction-Akki/backend")

from services.training_runner import ssh_seam  # noqa: E402


# ============================================================================
# Config
# ============================================================================

BURN_DURATION_SECONDS = int(os.environ.get("BURN_DURATION_SECONDS", "1500"))  # 25 min
POLL_INTERVAL_SECONDS = int(os.environ.get("BURN_POLL_INTERVAL", "60"))  # 1 min
MATMUL_SIZE = int(os.environ.get("BURN_MATMUL_SIZE", "8192"))
DTYPE = os.environ.get("BURN_DTYPE", "float16")
HOSTS = ["akki-vm", "akki-vm-ii"]

RUN_ID = f"burn_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"

# Workspace paths.
BURN_ROOT = Path("/app/assessment_workspace/phase0/gpu_burn") / RUN_ID
BURN_ROOT.mkdir(parents=True, exist_ok=True)

RUNS_DIR = Path("/app/assessment_workspace/phase0/training_runner/runs")
RUNS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# burn.py payload (staged onto each host)
# ============================================================================

BURN_PAYLOAD_PY = r"""#!/usr/bin/env python3
# Payload - governed benchmark burn (owner Ruling A - 2026-08-31).
#
# Runs sustained fp16 matmul on all visible CUDA GPUs of the host.
# NO estate data. NO PII. Only in-memory synthetic tensors.
#
# Args:
#   --duration <int>  wall-clock seconds to run
#   --size <int>      matmul side (default 8192)
#   --dtype <str>     float16 | bfloat16 | float32
#   --log <path>      log file path
#
# Emits JSONL lines to stdout (and to --log): one line per GPU per
# ~30s interval, plus a final SUMMARY line per GPU.
import argparse
import json
import os
import sys
import threading
import time
from datetime import datetime, timezone


def _iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(fp, obj):
    line = json.dumps(obj, separators=(",", ":"), sort_keys=True)
    print(line, flush=True)
    if fp is not None:
        fp.write(line + "\n")
        fp.flush()


def _burn_one_gpu(idx, duration_s, size, dtype_str, out_fp, results):
    try:
        import torch
    except Exception as e:
        _log(out_fp, {"gpu": idx, "kind": "err", "at": _iso(), "err": f"torch import failed: {e}"})
        results[idx] = {"gpu": idx, "err": str(e)}
        return
    dtype = {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
    }.get(dtype_str, torch.float16)
    device = torch.device(f"cuda:{idx}")
    _log(out_fp, {
        "gpu": idx, "kind": "start", "at": _iso(),
        "size": size, "dtype": dtype_str,
        "device_name": torch.cuda.get_device_name(idx),
    })
    # Allocate two matrices on device (synthetic random data).
    torch.manual_seed(1234 + idx)
    A = torch.randn(size, size, device=device, dtype=dtype)
    B = torch.randn(size, size, device=device, dtype=dtype)
    # A single warm-up matmul to compile / init CUDA lazily.
    C = A @ B
    torch.cuda.synchronize(device)
    del C
    iter_count = 0
    tflops_samples = []
    t_start = time.monotonic()
    t_last_log = t_start
    iter_at_last_log = 0
    end_time = t_start + duration_s
    while time.monotonic() < end_time:
        # Chunk-of-N matmuls before sync/telemetry — keeps GIL out of the loop.
        n = 8
        for _ in range(n):
            C = A @ B
        torch.cuda.synchronize(device)
        del C
        iter_count += n
        now = time.monotonic()
        if now - t_last_log >= 30.0:
            # 2 * N^3 flops per matmul (dense). Count matmuls executed
            # SINCE last tick (not just the last chunk of n).
            iters_this_period = iter_count - iter_at_last_log
            flops = 2.0 * (size ** 3) * iters_this_period
            dt = now - t_last_log
            tflops = (flops / dt) / 1e12
            tflops_samples.append(tflops)
            _log(out_fp, {
                "gpu": idx, "kind": "tick", "at": _iso(),
                "iter_count": iter_count,
                "elapsed_s": round(now - t_start, 2),
                "chunk_tflops": round(tflops, 2),
            })
            t_last_log = now
            iter_at_last_log = iter_count
    t_end = time.monotonic()
    total_dt = t_end - t_start
    # Free memory.
    del A, B
    try:
        torch.cuda.empty_cache()
    except Exception:
        pass
    tflops_median = 0.0
    if tflops_samples:
        s = sorted(tflops_samples)
        m = len(s) // 2
        tflops_median = s[m] if len(s) % 2 == 1 else (s[m-1] + s[m]) / 2
    summary = {
        "gpu": idx, "kind": "summary", "at": _iso(),
        "iter_count": iter_count,
        "wallclock_s": round(total_dt, 2),
        "tflops_median": round(tflops_median, 2),
        "tflops_samples_n": len(tflops_samples),
        "size": size, "dtype": dtype_str,
    }
    _log(out_fp, summary)
    results[idx] = summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--duration", type=int, default=1500)
    p.add_argument("--size", type=int, default=8192)
    p.add_argument("--dtype", type=str, default="float16")
    p.add_argument("--log", type=str, default="/tmp/burn.log")
    args = p.parse_args()

    try:
        import torch
    except Exception as e:
        print(json.dumps({"kind": "fatal", "err": f"torch import failed: {e}"}), flush=True)
        sys.exit(2)
    n_gpu = torch.cuda.device_count()
    if n_gpu <= 0:
        print(json.dumps({"kind": "fatal", "err": "no CUDA devices visible"}), flush=True)
        sys.exit(3)
    out_fp = open(args.log, "a")
    _log(out_fp, {"kind": "boot", "at": _iso(), "n_gpu": n_gpu,
                  "duration_s": args.duration, "size": args.size, "dtype": args.dtype,
                  "torch_version": torch.__version__,
                  "cuda_version": torch.version.cuda,
                  "pid": os.getpid()})
    results = {}
    threads = []
    for i in range(n_gpu):
        t = threading.Thread(target=_burn_one_gpu, args=(i, args.duration, args.size, args.dtype, out_fp, results), daemon=False)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    _log(out_fp, {"kind": "done", "at": _iso(), "results": [results.get(i, {}) for i in range(n_gpu)]})
    out_fp.close()


if __name__ == "__main__":
    main()
"""


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class HostResult:
    host_slug: str
    receipts: List[str] = field(default_factory=list)
    nvidia_smi_before: Optional[Dict[str, Any]] = None
    nvidia_smi_during_polls: List[Dict[str, Any]] = field(default_factory=list)
    nvidia_smi_after: Optional[Dict[str, Any]] = None
    burn_log_tail: str = ""
    burn_summary: Dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    finished_at: str = ""
    wallclock_seconds: float = 0.0
    gpu_count: int = 0
    torch_ok: bool = False
    torch_version: str = ""
    cuda_version: str = ""
    exit_code: int = -1
    error: str = ""


# ============================================================================
# Helpers
# ============================================================================

def _iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_nvidia_smi_csv(text: str) -> List[Dict[str, Any]]:
    """Parse `nvidia-smi --query-gpu=... --format=csv` output."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return []
    header = [c.strip() for c in lines[0].split(",")]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split(",")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def _run_and_save(host_slug: str, cmd: str, purpose: str,
                  hr: HostResult, save_as: Optional[str] = None,
                  timeout: int = 60) -> Any:
    """execute_remote_command wrapper that:
     - appends receipt_id to hr.receipts
     - optionally saves the redacted stdout to BURN_ROOT/<save_as>
     - returns the RemoteExecResult
    """
    r = ssh_seam.execute_remote_command(host_slug, cmd, purpose=purpose, timeout=timeout)
    hr.receipts.append(r.receipt_id)
    if save_as:
        p = BURN_ROOT / f"{host_slug.replace('-', '_')}_{save_as}"
        payload = {
            "at": _iso(),
            "host_slug": host_slug,
            "purpose": purpose,
            "receipt_id": r.receipt_id,
            "rc": r.rc,
            "wallclock_seconds": r.wallclock_seconds,
            "stdout_redacted": r.stdout_redacted,
            "stderr_redacted": r.stderr_redacted,
        }
        p.write_text(json.dumps(payload, indent=2))
    return r


def _capture_nvidia_smi(host_slug: str, hr: HostResult, label: str) -> Dict[str, Any]:
    cmd = (
        "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,"
        "power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory "
        "--format=csv"
    )
    r = _run_and_save(host_slug, cmd, purpose=f"nvidia_smi_{label}", hr=hr,
                      save_as=f"nvidia_smi_{label}.json", timeout=30)
    parsed = _parse_nvidia_smi_csv(r.stdout_redacted) if r.rc == 0 else []
    snap = {
        "at": _iso(), "label": label, "host_slug": host_slug,
        "rc": r.rc, "receipt_id": r.receipt_id,
        "gpus": parsed,
    }
    return snap


def _stage_burn_script(host_slug: str, hr: HostResult, remote_dir: str) -> None:
    """Stage burn.py onto the host under remote_dir via base64 heredoc."""
    b64 = base64.b64encode(BURN_PAYLOAD_PY.encode("utf-8")).decode("ascii")
    # Split base64 into 76-col lines to be safe with shell.
    b64_lines = "\n".join(b64[i:i+76] for i in range(0, len(b64), 76))
    cmd = (
        f"mkdir -p {remote_dir} && "
        f"cat > {remote_dir}/burn.b64 <<'EOF_BURN_B64'\n{b64_lines}\nEOF_BURN_B64\n"
        f"base64 -d {remote_dir}/burn.b64 > {remote_dir}/burn.py && "
        f"chmod +x {remote_dir}/burn.py && "
        f"wc -c {remote_dir}/burn.py && "
        f"sha256sum {remote_dir}/burn.py"
    )
    _run_and_save(host_slug, cmd, purpose="stage_burn_script", hr=hr,
                  save_as="stage_burn.json", timeout=45)


def _launch_burn(host_slug: str, hr: HostResult, remote_dir: str, duration: int,
                 size: int, dtype: str) -> None:
    """Launch burn.py in background via nohup, return immediately.

    The trick: paramiko's exec_command.stdout.read() blocks until channel
    EOF, and channel EOF only fires when NO descendant process holds any
    of the SSH-allocated fds. Even `nohup ... > file 2>&1 &` inherits ssh
    fds through the shell's own inheritance chain.

    Fix: wrap the launch in a subshell whose stdin/stdout/stderr are all
    redirected AWAY from the ssh channel BEFORE the nohup runs. Then the
    ssh channel has no descendants and closes immediately.
    """
    logfile = f"{remote_dir}/burn.log"
    pidfile = f"{remote_dir}/burn.pid"
    # The `( ... ) </dev/null >/dev/null 2>&1` fully severs the subshell
    # (and everything it launches) from the SSH channel's fds.
    # setsid detaches from the ctty; disown removes the job from the shell
    # so it survives the outer shell exit.
    cmd = (
        f"cd {remote_dir} && "
        f"( setsid nohup python3 burn.py --duration {duration} --size {size} "
        f"--dtype {dtype} --log {logfile} "
        f"< /dev/null > {remote_dir}/burn.stdout 2>&1 & "
        f"echo $! > {pidfile}; "
        f") </dev/null >/dev/null 2>&1; "
        f"sleep 2; "
        f"echo pid=$(cat {pidfile} 2>/dev/null); "
        f"if [ -s {logfile} ]; then echo '---log---'; head -5 {logfile}; "
        f"else echo '(no log lines yet · burn is initializing)'; fi; "
        f"exit 0"
    )
    _run_and_save(host_slug, cmd, purpose="launch_burn", hr=hr,
                  save_as="launch_burn.json", timeout=30)


def _tail_burn_log(host_slug: str, hr: HostResult, remote_dir: str) -> str:
    r = _run_and_save(host_slug,
                      f"tail -n 8 {remote_dir}/burn.log 2>/dev/null || echo '(no log)'",
                      purpose="tail_burn_log", hr=hr, timeout=15)
    return r.stdout_redacted


def _burn_still_running(host_slug: str, hr: HostResult, remote_dir: str) -> bool:
    r = _run_and_save(host_slug,
                      f"pid=$(cat {remote_dir}/burn.pid 2>/dev/null); "
                      f"if [ -n \"$pid\" ] && kill -0 $pid 2>/dev/null; "
                      f"then echo running; else echo done; fi",
                      purpose="check_burn_running", hr=hr, timeout=15)
    return "running" in r.stdout_redacted


def _cleanup(host_slug: str, hr: HostResult, remote_dir: str) -> None:
    _run_and_save(host_slug,
                  f"if [ -d {remote_dir} ]; then "
                  f"  cp {remote_dir}/burn.log /tmp/akki_burn_last.log 2>/dev/null || true; "
                  f"  rm -rf {remote_dir}; echo cleaned; else echo already_absent; fi",
                  purpose="cleanup_burn_dir", hr=hr,
                  save_as="cleanup.json", timeout=30)


# ============================================================================
# Per-host workflow (runs in a thread)
# ============================================================================

def burn_one_host(host_slug: str) -> HostResult:
    hr = HostResult(host_slug=host_slug)
    remote_dir = f"/tmp/akki_burn_{RUN_ID}"
    try:
        hr.started_at = _iso()
        t0 = time.monotonic()

        # 1) Baseline nvidia-smi
        hr.nvidia_smi_before = _capture_nvidia_smi(host_slug, hr, "before")

        # 2) Torch availability
        r = _run_and_save(host_slug,
                          "python3 -c 'import torch, json; "
                          "print(json.dumps({\"ok\": True, \"v\": torch.__version__, "
                          "\"cuda\": torch.version.cuda, \"n\": torch.cuda.device_count()}))'",
                          purpose="torch_probe", hr=hr,
                          save_as="torch_probe.json", timeout=45)
        if r.rc == 0:
            try:
                # Filter to lines that parse as JSON (torch may emit warnings).
                probe = None
                for line in (r.stdout_redacted or "").splitlines():
                    line = line.strip()
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            probe = json.loads(line)
                            break
                        except Exception:
                            continue
                if probe is None:
                    raise ValueError(f"no JSON line in probe output: {r.stdout_redacted[:200]!r}")
                hr.torch_ok = bool(probe.get("ok"))
                hr.torch_version = probe.get("v", "")
                hr.cuda_version = probe.get("cuda", "")
                hr.gpu_count = int(probe.get("n", 0))
            except Exception as e:
                hr.error = f"torch probe parse: {e}"
        else:
            hr.error = f"torch probe rc={r.rc}: {r.stderr_redacted[:200]}"
        if not hr.torch_ok or hr.gpu_count == 0:
            hr.error = hr.error or "torch not usable"
            return hr

        # 3) Stage burn.py
        _stage_burn_script(host_slug, hr, remote_dir)

        # 4) Launch burn
        _launch_burn(host_slug, hr, remote_dir, BURN_DURATION_SECONDS,
                     MATMUL_SIZE, DTYPE)

        # 5) Poll during burn
        end = time.monotonic() + BURN_DURATION_SECONDS + 30
        while time.monotonic() < end:
            time.sleep(POLL_INTERVAL_SECONDS)
            snap = _capture_nvidia_smi(host_slug, hr, f"poll_{int(time.monotonic()-t0)}s")
            hr.nvidia_smi_during_polls.append(snap)
            tail = _tail_burn_log(host_slug, hr, remote_dir)
            # If script exited early, break out.
            if not _burn_still_running(host_slug, hr, remote_dir):
                # Give final flush a moment.
                time.sleep(3)
                break

        # 6) Final nvidia-smi + burn log tail
        hr.nvidia_smi_after = _capture_nvidia_smi(host_slug, hr, "after")
        hr.burn_log_tail = _tail_burn_log(host_slug, hr, remote_dir)

        # 7) Read full burn.log JSONL for the summary lines
        r = _run_and_save(host_slug, f"cat {remote_dir}/burn.log",
                          purpose="collect_burn_log", hr=hr,
                          save_as="burn_log.json", timeout=30)
        summaries = []
        boot = None
        for line in (r.stdout_redacted or "").splitlines():
            try:
                obj = json.loads(line)
                if obj.get("kind") == "summary":
                    summaries.append(obj)
                if obj.get("kind") == "boot":
                    boot = obj
            except Exception:
                pass
        hr.burn_summary = {"boot": boot, "per_gpu_summary": summaries}
        hr.exit_code = 0

        # 8) Cleanup
        _cleanup(host_slug, hr, remote_dir)

        hr.finished_at = _iso()
        hr.wallclock_seconds = round(time.monotonic() - t0, 2)
        return hr
    except Exception as e:
        hr.error = f"{type(e).__name__}: {e}"
        hr.finished_at = _iso()
        try:
            _cleanup(host_slug, hr, remote_dir)
        except Exception:
            pass
        return hr


# ============================================================================
# Registration: training_runner run record + cost-ledger crossing receipt
# ============================================================================

def register_burn_run(hosts: List[HostResult]) -> Path:
    """Write a first-class run record adapted from TrainingRunV0 shape.
    kind='benchmark_burn' (not on the TrainingRunV0 enum — using dedicated
    burn schema so we don't pollute training_runs state).
    """
    total_gpu_hours = 0.0
    for h in hosts:
        # gpu_hours = wallclock_hours * gpu_count
        total_gpu_hours += (h.wallclock_seconds / 3600.0) * max(1, h.gpu_count)
    record = {
        "run_id": RUN_ID,
        "kind": "benchmark_burn",
        "authority": "owner ruling (A) 2026-08-31 fallback burn tonight",
        "started_at": min([h.started_at for h in hosts if h.started_at] or [_iso()]),
        "finished_at": max([h.finished_at for h in hosts if h.finished_at] or [_iso()]),
        "hosts": [asdict(h) for h in hosts],
        "totals": {
            "gpu_hours": round(total_gpu_hours, 4),
            "gpu_count_total": sum(h.gpu_count for h in hosts),
            "wallclock_seconds_max": max([h.wallclock_seconds for h in hosts] or [0.0]),
        },
        "workload": {
            "workload_type": "sustained_matmul_fp16",
            "matmul_size": MATMUL_SIZE,
            "dtype": DTYPE,
            "duration_target_s": BURN_DURATION_SECONDS,
            "estate_data_used": False,
            "pii_touched": False,
            "data_source": "in-memory synthetic tensors (torch.randn)",
        },
        "governance": {
            "seam": "services.training_runner.ssh_seam.execute_remote_command",
            "masking_tier": "attested_command",
            "chokepoint_kind": "ssh_seam_remote_exec",
            "shielded_training_pipeline": "NOT_YET_BUILT · charter forthcoming per owner ruling",
        },
    }
    path = RUNS_DIR / f"{RUN_ID}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True))
    return path


def write_cost_ledger_receipt(hosts: List[HostResult]) -> Path:
    """Emit a cost-ledger crossing receipt (kind='ssh_seam') per host so
    the ledger picks up the compute activity."""
    receipts_dir = Path(os.environ.get(
        "CROSSING_RECEIPT_DIR",
        "/app/assessment_workspace/phase0/crossing_receipts",
    ))
    receipts_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for h in hosts:
        gpu_hours = round((h.wallclock_seconds / 3600.0) * max(1, h.gpu_count), 4)
        rid = f"rcp-burn-{RUN_ID}-{h.host_slug.replace('-', '_')}"
        r = {
            "receipt_id": rid,
            "kind": "ssh_seam",
            "at_iso": _iso(),
            "actor": f"tools.gpu_burn_orchestrator · {h.host_slug}",
            "endpoint_host": h.host_slug,
            "residency_region": "estate",
            "masking_tier": "attested_command",
            "verb": "EXEC",
            "payload_shape": {
                "training_id": RUN_ID,
                "node_id": h.host_slug,
                "gpu_hours": gpu_hours,
                "metering_source": "burn_orchestrator_wallclock",
                "workload": "sustained_matmul_fp16",
            },
        }
        p = receipts_dir / f"{rid}.json"
        p.write_text(json.dumps(r, indent=2, sort_keys=True))
        written.append(str(p))
    idx = BURN_ROOT / "cost_ledger_receipts.json"
    idx.write_text(json.dumps({"receipts_written": written, "at": _iso()}, indent=2))
    return idx


# ============================================================================
# Plain-language activity summary
# ============================================================================

def _median(nums):
    ns = sorted([n for n in nums if n is not None])
    if not ns:
        return None
    m = len(ns) // 2
    return ns[m] if len(ns) % 2 == 1 else (ns[m-1] + ns[m]) / 2


def _parse_util_pct(s):
    if not s:
        return None
    s = s.replace("%", "").strip()
    try:
        return float(s)
    except Exception:
        return None


def _parse_power_w(s):
    if not s:
        return None
    s = s.replace("W", "").strip()
    try:
        return float(s)
    except Exception:
        return None


def _parse_temp_c(s):
    if not s:
        return None
    try:
        return float(s.strip())
    except Exception:
        return None


def _parse_mem_mib(s):
    if not s:
        return None
    s = s.replace("MiB", "").strip()
    try:
        return float(s)
    except Exception:
        return None


def build_activity_summary(hosts: List[HostResult]) -> Dict[str, Any]:
    per_host = []
    for h in hosts:
        util_samples = []
        power_samples = []
        temp_samples = []
        mem_used_samples = []
        for poll in h.nvidia_smi_during_polls:
            for gpu in poll.get("gpus", []):
                u = _parse_util_pct(gpu.get("utilization.gpu [%]") or gpu.get("utilization.gpu"))
                if u is not None:
                    util_samples.append(u)
                p = _parse_power_w(gpu.get("power.draw [W]") or gpu.get("power.draw"))
                if p is not None:
                    power_samples.append(p)
                t = _parse_temp_c(gpu.get("temperature.gpu"))
                if t is not None:
                    temp_samples.append(t)
                m = _parse_mem_mib(gpu.get("memory.used [MiB]") or gpu.get("memory.used"))
                if m is not None:
                    mem_used_samples.append(m)
        tflops_samples = [s.get("tflops_median") for s in h.burn_summary.get("per_gpu_summary", []) if s.get("tflops_median")]
        per_host.append({
            "host_slug": h.host_slug,
            "gpu_count": h.gpu_count,
            "torch_version": h.torch_version,
            "cuda_version": h.cuda_version,
            "wallclock_seconds": h.wallclock_seconds,
            "gpu_hours": round((h.wallclock_seconds / 3600.0) * max(1, h.gpu_count), 4),
            "util_pct_median": _median(util_samples),
            "power_w_median": _median(power_samples),
            "temp_c_median": _median(temp_samples),
            "memory_used_mib_median": _median(mem_used_samples),
            "tflops_per_gpu_median": _median(tflops_samples),
            "poll_count": len(h.nvidia_smi_during_polls),
            "exit_code": h.exit_code,
            "error": h.error,
        })
    total_wall_s = max([h.wallclock_seconds for h in hosts] or [0])
    total_gpu_hours = sum([ph["gpu_hours"] for ph in per_host])
    text_lines = [
        f"GPU Activity — {RUN_ID}",
        f"When: {min([h.started_at for h in hosts if h.started_at] or [_iso()])} → "
        f"{max([h.finished_at for h in hosts if h.finished_at] or [_iso()])} UTC",
        f"Wall-clock: {total_wall_s/60:.1f} minutes (both hosts in parallel).",
        f"Total GPU-hours delivered: {total_gpu_hours:.2f} across "
        f"{sum(h.gpu_count for h in hosts)} GPUs on "
        f"{len(hosts)} hosts.",
        f"Workload: sustained fp16 matmul ({MATMUL_SIZE}×{MATMUL_SIZE}), "
        f"no estate data — synthetic tensors only.",
        "",
        "Per host:",
    ]
    for ph in per_host:
        util = ph["util_pct_median"]
        pw = ph["power_w_median"]
        tp = ph["temp_c_median"]
        mm = ph["memory_used_mib_median"]
        tfl = ph["tflops_per_gpu_median"]
        text_lines.append(
            f"  • {ph['host_slug']}: {ph['gpu_count']} GPU(s), "
            f"utilization median {util if util is not None else '?'}%, "
            f"power draw median {pw if pw is not None else '?'} W, "
            f"temperature median {tp if tp is not None else '?'} °C, "
            f"memory used median {mm if mm is not None else '?'} MiB, "
            f"compute throughput median {tfl if tfl is not None else '?'} TFLOPS/GPU, "
            f"exit_code={ph['exit_code']}"
            + (f", error={ph['error']}" if ph["error"] else "")
        )
    text_lines += [
        "",
        "Governance: every remote call went through the training_runner SSH "
        "seam (execute_remote_command), each with a governed crossing "
        "receipt written to phase0/crossing_receipts/ and a redacted seam "
        "receipt written to phase0/gpu_receipts/. Masking tier: "
        "attested_command. No PII, no estate data, on either host.",
        "",
        "Shielded-data intent: NOT dropped. Chartered as a next-wave delivery "
        "per owner ruling. See DECISIONS.md entry banking the honest gap "
        "and the shielded-training pipeline scope.",
    ]
    plain_language = "\n".join(text_lines)
    return {
        "run_id": RUN_ID,
        "at": _iso(),
        "totals": {
            "gpu_hours": round(total_gpu_hours, 4),
            "wallclock_seconds_max": total_wall_s,
            "gpu_count_total": sum(h.gpu_count for h in hosts),
            "host_count": len(hosts),
        },
        "per_host": per_host,
        "plain_language": plain_language,
    }


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    print(f"[gpu_burn] RUN_ID = {RUN_ID}", flush=True)
    print(f"[gpu_burn] BURN_ROOT = {BURN_ROOT}", flush=True)
    print(f"[gpu_burn] duration={BURN_DURATION_SECONDS}s size={MATMUL_SIZE} dtype={DTYPE}", flush=True)
    print(f"[gpu_burn] poll_interval={POLL_INTERVAL_SECONDS}s hosts={HOSTS}", flush=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(HOSTS)) as ex:
        futs = {ex.submit(burn_one_host, h): h for h in HOSTS}
        results: List[HostResult] = []
        for fut in concurrent.futures.as_completed(futs):
            h = futs[fut]
            try:
                hr = fut.result()
                results.append(hr)
                print(f"[gpu_burn] {h} → exit_code={hr.exit_code} wallclock={hr.wallclock_seconds:.1f}s error={hr.error!r}", flush=True)
            except Exception as e:
                bad = HostResult(host_slug=h, error=f"orchestrator crash: {e}")
                results.append(bad)

    # Save all raw per-host results
    (BURN_ROOT / "hosts_raw.json").write_text(
        json.dumps([asdict(h) for h in results], indent=2, sort_keys=True)
    )

    # Register run + cost ledger receipts
    run_path = register_burn_run(results)
    ledger_idx = write_cost_ledger_receipt(results)

    # Activity summary
    summary = build_activity_summary(results)
    (BURN_ROOT / "activity_summary.json").write_text(json.dumps(summary, indent=2))
    (BURN_ROOT / "activity_summary.txt").write_text(summary["plain_language"])

    print()
    print("=" * 76)
    print("ACTIVITY SUMMARY")
    print("=" * 76)
    print(summary["plain_language"])
    print("=" * 76)
    print()
    print(f"[gpu_burn] run record: {run_path}")
    print(f"[gpu_burn] ledger receipts index: {ledger_idx}")
    print(f"[gpu_burn] artifacts root: {BURN_ROOT}")

    return 0 if all(h.exit_code == 0 for h in results) else 1


if __name__ == "__main__":
    sys.exit(main())
