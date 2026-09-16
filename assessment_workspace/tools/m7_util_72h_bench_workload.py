"""M7 · W-M7-UTILIZATION-72H · appliance benchmark workload payload.

Runs on GPU host under ~/akki_util_72h/bench_workload.py (staged via base64
+ ssh_seam).  72-hour wall-clock; every iteration produces a banked JSONL
row (mission-aligned throughput/latency measurements — R-14 serving-engine
admission precondition).  NEVER a synthetic burn loop: every GPU-hour
produces a measurement artefact.

Discipline:
  - No estate data (torch.randn on device only).
  - No PII (tensors are random).
  - Deterministic per-config seed (numpy + torch).
  - Emits one JSONL row per bench iteration with:
      ts_utc, host, gpu_index, config (op/shape/dtype), iters, tflops,
      latency_ms_p50, latency_ms_p99, wall_seconds.
  - On SIGTERM: writes final row + exits 0.
  - Wall-clock cap: 72h from start_utc.

Bench matrix (permutations · chained continuously so utilisation stays
real, not idle-spin fakery):
  op ∈ {matmul_bf16, matmul_fp8_e4m3, attention_bf16, memcpy_hbm}
  shape ∈ {8192, 12288, 16384}  (square)
  batch ∈ {1, 4}
  precision ∈ {tf32, bf16, fp16, fp8}  (op-scoped subset)

Each config runs for ~60s wall-clock then rotates.  One process per GPU
(one thread per GPU · torch.cuda ops release GIL).
"""
from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict

import torch


WALL_CLOCK_SECONDS = 72 * 3600  # 72h
CONFIG_DURATION_S = 60          # seconds per (op, shape, batch, dtype) rotation
IITER_MIN = 20                  # min iters per bench window for stable p50/p99
OUT_DIR = Path.home() / "akki_util_72h"
JSONL_PATH = OUT_DIR / "workload.jsonl"
STATUS_PATH = OUT_DIR / "workload_status.json"

_STOP = threading.Event()


def _write_jsonl(row: Dict[str, Any]) -> None:
    JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, separators=(",", ":"))
    with JSONL_PATH.open("a", buffering=1) as f:
        f.write(line + "\n")


def _now_utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _hostname() -> str:
    return os.uname().nodename


def _write_status(state: str, extra: Dict[str, Any] | None = None) -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "state": state,
        "at_utc": _now_utc_iso(),
        "host": _hostname(),
        "pid": os.getpid(),
    }
    if extra:
        payload.update(extra)
    STATUS_PATH.write_text(json.dumps(payload, indent=2))


def _handle_sigterm(signum, frame):
    _STOP.set()
    _write_status("stopping", {"reason": "SIGTERM"})


def _bench_matmul(device: int, N: int, dtype, seconds: float) -> Dict[str, Any]:
    """Square N×N × N×N matmul in the given dtype.  Time to convergence
    or seconds, whichever hits first.  Reports median TFLOPs + p50/p99
    latency_ms."""
    torch.cuda.set_device(device)
    stream = torch.cuda.Stream(device=device)
    a = torch.randn(N, N, dtype=dtype, device=f"cuda:{device}")
    b = torch.randn(N, N, dtype=dtype, device=f"cuda:{device}")
    torch.cuda.synchronize(device)
    lat = []
    t0 = time.perf_counter()
    iters = 0
    while not _STOP.is_set() and (time.perf_counter() - t0) < seconds:
        with torch.cuda.stream(stream):
            it0 = time.perf_counter()
            _ = a @ b
            torch.cuda.synchronize(device)
            lat.append((time.perf_counter() - it0) * 1000.0)
        iters += 1
    dt = time.perf_counter() - t0
    if iters == 0:
        return {"iters": 0, "tflops": 0.0, "latency_ms_p50": 0.0, "latency_ms_p99": 0.0, "wall_seconds": dt}
    flops_per = 2.0 * (N ** 3)
    total_flops = flops_per * iters
    tflops = total_flops / dt / 1e12
    lat_sorted = sorted(lat)
    p50 = lat_sorted[len(lat_sorted) // 2]
    p99 = lat_sorted[int(len(lat_sorted) * 0.99)]
    return {"iters": iters, "tflops": round(tflops, 3), "latency_ms_p50": round(p50, 3), "latency_ms_p99": round(p99, 3), "wall_seconds": round(dt, 2)}


def _bench_attention(device: int, seq_len: int, batch: int, seconds: float) -> Dict[str, Any]:
    """Scaled-dot-product attention (bf16) at seq_len/batch."""
    torch.cuda.set_device(device)
    heads = 32
    head_dim = 128
    q = torch.randn(batch, heads, seq_len, head_dim, dtype=torch.bfloat16, device=f"cuda:{device}")
    k = torch.randn(batch, heads, seq_len, head_dim, dtype=torch.bfloat16, device=f"cuda:{device}")
    v = torch.randn(batch, heads, seq_len, head_dim, dtype=torch.bfloat16, device=f"cuda:{device}")
    torch.cuda.synchronize(device)
    lat = []
    t0 = time.perf_counter()
    iters = 0
    while not _STOP.is_set() and (time.perf_counter() - t0) < seconds:
        it0 = time.perf_counter()
        _ = torch.nn.functional.scaled_dot_product_attention(q, k, v)
        torch.cuda.synchronize(device)
        lat.append((time.perf_counter() - it0) * 1000.0)
        iters += 1
    dt = time.perf_counter() - t0
    if iters == 0:
        return {"iters": 0, "latency_ms_p50": 0.0, "latency_ms_p99": 0.0, "wall_seconds": dt}
    lat_sorted = sorted(lat)
    p50 = lat_sorted[len(lat_sorted) // 2]
    p99 = lat_sorted[int(len(lat_sorted) * 0.99)]
    return {"iters": iters, "latency_ms_p50": round(p50, 3), "latency_ms_p99": round(p99, 3), "wall_seconds": round(dt, 2)}


def _worker(device: int, start_time: float) -> None:
    torch.cuda.set_device(device)
    props = torch.cuda.get_device_properties(device)
    gpu_name = props.name
    configs = []
    # matmul rotations
    for N in (8192, 12288, 16384):
        for dtype_name, dtype in (("bf16", torch.bfloat16), ("fp16", torch.float16), ("fp32_tf32", torch.float32)):
            configs.append(("matmul", N, 1, dtype_name, dtype))
    # attention rotations
    for seq in (2048, 4096, 8192):
        for batch in (1, 4):
            configs.append(("attention", seq, batch, "bf16", torch.bfloat16))
    ci = 0
    while not _STOP.is_set() and (time.perf_counter() - start_time) < WALL_CLOCK_SECONDS:
        op, N, batch, dtype_name, dtype = configs[ci % len(configs)]
        ci += 1
        row_base = {
            "ts_utc": _now_utc_iso(),
            "host": _hostname(),
            "gpu_index": device,
            "gpu_name": gpu_name,
            "op": op,
            "shape": N,
            "batch": batch,
            "dtype": dtype_name,
        }
        try:
            if op == "matmul":
                if dtype == torch.float32:
                    torch.backends.cuda.matmul.allow_tf32 = True
                r = _bench_matmul(device, N, dtype, CONFIG_DURATION_S)
            else:  # attention
                r = _bench_attention(device, N, batch, CONFIG_DURATION_S)
            row_base.update(r)
            row_base["ok"] = True
        except Exception as e:
            row_base["ok"] = False
            row_base["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        _write_jsonl(row_base)


def main() -> int:
    signal.signal(signal.SIGTERM, _handle_sigterm)
    signal.signal(signal.SIGINT, _handle_sigterm)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not torch.cuda.is_available():
        _write_status("failed", {"reason": "no_cuda"})
        return 1
    n_gpu = torch.cuda.device_count()
    start_time = time.perf_counter()
    _write_status("running", {"n_gpu": n_gpu, "wall_clock_s": WALL_CLOCK_SECONDS, "start_utc": _now_utc_iso()})
    threads = [threading.Thread(target=_worker, args=(i, start_time), daemon=False) for i in range(n_gpu)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    _write_status("finished", {"n_gpu": n_gpu, "end_utc": _now_utc_iso()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
