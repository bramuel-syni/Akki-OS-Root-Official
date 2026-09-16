"""M7 · W-M7-UTILIZATION-72H · orchestrator + sync + report generator.

Modes (via argv[1]):
  build_and_launch  — stage payloads on both hosts, launch detached
                      (setsid + nohup), verify PIDs alive, write initial
                      report.
  check_in          — sync telemetry.jsonl + workload.jsonl + status
                      files from both hosts to
                      /app/assessment_workspace/phase0/gpu_utilization_72h/
                      <host>/*, then regenerate report.
  status_only       — probe both hosts for state, do not sync JSONL, print
                      to stdout (fast health check).

Discipline (§E · SO §4.1):
  - All host reads/writes go through ssh_seam.execute_remote_command.
  - Payloads staged via base64 to avoid shell-quoting issues.
  - No credentials in receipts (ssh_seam handles redaction).
  - Report served at /app/frontend/public/audit/GPU_UTILIZATION_72H.{md,json}.

Owner ruling · 2026-09-16T~03:08Z:
  "show utilization over the next 3 days (72 hours) ... build a job and
   commence a run ... appliance benchmark suite on both H200 boxes
   (discharges precondition (a) of the deliberately-unruled R-14
   serving-engine admission) ... NEVER run synthetic burn loops; every
   GPU-hour must produce a banked artefact."
"""
from __future__ import annotations

import base64
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
load_dotenv("/app/backend/.env")

sys.path.insert(0, "/app/assessment_workspace/repos/Extraction-Akki/backend")
from services.training_runner import ssh_seam  # noqa: E402


HOSTS = ("akki-vm", "akki-vm-ii")
REMOTE_DIR = "~/akki_util_72h"
BENCH_LOCAL = Path("/app/assessment_workspace/tools/m7_util_72h_bench_workload.py")
SAMPLER_LOCAL = Path("/app/assessment_workspace/tools/m7_util_72h_sampler.sh")

LOCAL_SYNC_ROOT = Path("/app/assessment_workspace/phase0/gpu_utilization_72h")
AUDIT_DIR = Path("/app/frontend/public/audit")
REPORT_MD = AUDIT_DIR / "GPU_UTILIZATION_72H.md"
REPORT_JSON = AUDIT_DIR / "GPU_UTILIZATION_72H.json"

WALL_CLOCK_H = 72


def _b64(payload: bytes) -> str:
    return base64.b64encode(payload).decode("ascii")


def _run(host: str, cmd: str, purpose: str, timeout: int = 30):
    return ssh_seam.execute_remote_command(host, cmd, purpose=purpose, timeout=timeout)


def stage_payloads(host: str) -> Dict[str, Any]:
    bench_b64 = _b64(BENCH_LOCAL.read_bytes())
    sampler_b64 = _b64(SAMPLER_LOCAL.read_bytes())
    cmd = (
        f"mkdir -p {REMOTE_DIR} && "
        f"echo {bench_b64} | base64 -d > {REMOTE_DIR}/bench_workload.py && "
        f"echo {sampler_b64} | base64 -d > {REMOTE_DIR}/sampler.sh && "
        f"chmod +x {REMOTE_DIR}/sampler.sh && "
        f"ls -la {REMOTE_DIR}/"
    )
    r = _run(host, cmd, purpose="w_m7_util_72h_stage", timeout=45)
    return {"host": host, "rc": r.rc, "stdout": r.stdout_redacted, "stderr": r.stderr_redacted}


def launch_detached(host: str) -> Dict[str, Any]:
    # Fully detach via file-staged launcher script.  Prior in-line variant
    # lost $! to outer-bash parameter expansion (json.dumps quoting expands
    # $! in the outer shell BEFORE bash -c evaluates the inner body, so
    # sampler_pid.txt + workload_pid.txt landed empty).  Fix: stage a
    # launcher.sh via base64, then setsid + nohup + redirected fds fire
    # /bin/bash launcher.sh — $! evaluates inside the launcher.sh process
    # where sampler / bench_workload are actually the last-backgrounded PIDs.
    launcher_src = (
        "#!/bin/bash\n"
        f"cd {REMOTE_DIR}\n"
        "date -u +%Y-%m-%dT%H:%M:%SZ > start_utc.txt\n"
        "nohup bash sampler.sh > sampler.log 2>&1 </dev/null &\n"
        "echo $! > sampler_pid.txt\n"
        "nohup python3 bench_workload.py > workload.log 2>&1 </dev/null &\n"
        "echo $! > workload_pid.txt\n"
        "disown -a\n"
        "exit 0\n"
    )
    launcher_b64 = _b64(launcher_src.encode("utf-8"))
    stage_cmd = (
        f"echo {launcher_b64} | base64 -d > {REMOTE_DIR}/launcher.sh && "
        f"chmod +x {REMOTE_DIR}/launcher.sh && "
        f"ls -la {REMOTE_DIR}/launcher.sh"
    )
    _run(host, stage_cmd, purpose="w_m7_util_72h_stage_launcher", timeout=15)
    cmd = (
        f"setsid nohup bash {REMOTE_DIR}/launcher.sh </dev/null >/dev/null 2>&1 & "
        f"disown; sleep 2; echo launched; "
        f"cat {REMOTE_DIR}/sampler_pid.txt {REMOTE_DIR}/workload_pid.txt 2>/dev/null"
    )
    r = _run(host, cmd, purpose="w_m7_util_72h_launch", timeout=20)
    return {"host": host, "rc": r.rc, "stdout": r.stdout_redacted, "stderr": r.stderr_redacted}


def probe_state(host: str) -> Dict[str, Any]:
    cmd = (
        f"echo '===host==='&& hostname && date -u +%Y-%m-%dT%H:%M:%SZ && "
        f"echo '===start==='&& cat {REMOTE_DIR}/start_utc.txt 2>/dev/null; "
        f"echo '===sampler_status==='&& cat {REMOTE_DIR}/sampler_status.json 2>/dev/null; "
        f"echo '===workload_status==='&& cat {REMOTE_DIR}/workload_status.json 2>/dev/null; "
        f"echo '===pids==='&& cat {REMOTE_DIR}/sampler_pid.txt {REMOTE_DIR}/workload_pid.txt 2>/dev/null; "
        f"echo '===alive==='&& "
        f"SP=$(cat {REMOTE_DIR}/sampler_pid.txt 2>/dev/null); "
        f"WP=$(cat {REMOTE_DIR}/workload_pid.txt 2>/dev/null); "
        f"[ -n \"$SP\" ] && kill -0 $SP 2>/dev/null && echo sampler_alive || echo sampler_dead; "
        f"[ -n \"$WP\" ] && kill -0 $WP 2>/dev/null && echo workload_alive || echo workload_dead; "
        f"echo '===sizes==='&& wc -l {REMOTE_DIR}/telemetry.jsonl {REMOTE_DIR}/workload.jsonl 2>/dev/null; "
        f"echo '===tail_tele==='&& tail -2 {REMOTE_DIR}/telemetry.jsonl 2>/dev/null; "
        f"echo '===tail_wl==='&& tail -2 {REMOTE_DIR}/workload.jsonl 2>/dev/null; "
        f"echo '===nvsmi==='&& nvidia-smi --query-gpu=index,utilization.gpu,memory.used,power.draw --format=csv,noheader"
    )
    r = _run(host, cmd, purpose="w_m7_util_72h_probe", timeout=30)
    return {"host": host, "rc": r.rc, "stdout": r.stdout_redacted, "stderr": r.stderr_redacted}


def sync_jsonl(host: str) -> Dict[str, Any]:
    """Pull telemetry.jsonl + workload.jsonl + status files back."""
    local_host_dir = LOCAL_SYNC_ROOT / host
    local_host_dir.mkdir(parents=True, exist_ok=True)
    out = {"host": host, "files": {}}
    for remote_name in ("telemetry.jsonl", "workload.jsonl", "sampler_status.json", "workload_status.json", "start_utc.txt", "sampler_pid.txt", "workload_pid.txt"):
        r = _run(host, f"cat {REMOTE_DIR}/{remote_name} 2>/dev/null", purpose=f"w_m7_util_72h_pull_{remote_name.replace('.','_')}", timeout=60)
        (local_host_dir / remote_name).write_text(r.stdout_redacted)
        out["files"][remote_name] = {"bytes": len(r.stdout_redacted), "rc": r.rc}
    return out


def _load_jsonl(p: Path) -> List[Dict[str, Any]]:
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _rollup_host(host: str) -> Dict[str, Any]:
    hdir = LOCAL_SYNC_ROOT / host
    tele = _load_jsonl(hdir / "telemetry.jsonl")
    wl = _load_jsonl(hdir / "workload.jsonl")
    start_utc = (hdir / "start_utc.txt").read_text().strip() if (hdir / "start_utc.txt").exists() else ""
    per_gpu: Dict[int, Dict[str, Any]] = {}
    for row in tele:
        gi = row.get("gpu_index")
        if gi is None:
            continue
        d = per_gpu.setdefault(gi, {"utilizations": [], "power_w": [], "temp_c": [], "mem_used_mib": [], "gpu_name": row.get("gpu_name", "")})
        try:
            d["utilizations"].append(float(row.get("utilization_gpu_pct", 0)))
            d["power_w"].append(float(row.get("power_w", 0)))
            d["temp_c"].append(float(row.get("temperature_c", 0)))
            d["mem_used_mib"].append(float(row.get("memory_used_mib", 0)))
        except (ValueError, TypeError):
            pass
    gpu_rollup = {}
    for gi, d in per_gpu.items():
        u = d["utilizations"]
        gpu_rollup[str(gi)] = {
            "gpu_name": d["gpu_name"],
            "samples": len(u),
            "utilization_gpu_pct_avg": round(statistics.mean(u), 1) if u else 0,
            "utilization_gpu_pct_peak": round(max(u), 1) if u else 0,
            "power_w_avg": round(statistics.mean(d["power_w"]), 1) if d["power_w"] else 0,
            "power_w_peak": round(max(d["power_w"]), 1) if d["power_w"] else 0,
            "temp_c_avg": round(statistics.mean(d["temp_c"]), 1) if d["temp_c"] else 0,
            "temp_c_peak": round(max(d["temp_c"]), 1) if d["temp_c"] else 0,
            "mem_used_mib_peak": round(max(d["mem_used_mib"]), 0) if d["mem_used_mib"] else 0,
        }
    # workload bench iterations count
    bench_configs_run = len(wl)
    bench_ok = sum(1 for r in wl if r.get("ok"))
    return {
        "host": host,
        "start_utc": start_utc,
        "telemetry_samples": len(tele),
        "bench_iterations": bench_configs_run,
        "bench_ok": bench_ok,
        "per_gpu": gpu_rollup,
    }


def _elapsed_hours(start_utc: str) -> float:
    if not start_utc:
        return 0.0
    try:
        t0 = time.strptime(start_utc, "%Y-%m-%dT%H:%M:%SZ")
        t0_epoch = int(time.mktime(t0))  # local; not perfect but close enough for report
        # gmtime path:
        import calendar
        t0_epoch = calendar.timegm(t0)
        now = int(time.time())
        return round((now - t0_epoch) / 3600, 2)
    except Exception:
        return 0.0


def regenerate_report(host_states: List[Dict[str, Any]]) -> Dict[str, Any]:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    earliest = ""
    for h in host_states:
        s = h.get("start_utc", "")
        if s and (not earliest or s < earliest):
            earliest = s
    elapsed_h = _elapsed_hours(earliest) if earliest else 0.0
    remaining_h = max(0.0, WALL_CLOCK_H - elapsed_h)

    # JSON payload
    payload = {
        "kind": "w_m7_utilization_72h_report",
        "generated_at_utc": generated_at,
        "launch_earliest_utc": earliest,
        "wall_clock_hours_total": WALL_CLOCK_H,
        "elapsed_hours": elapsed_h,
        "remaining_hours": remaining_h,
        "hosts": host_states,
        "receipt_index": {
            "local_sync_root": str(LOCAL_SYNC_ROOT),
            "audit_report_md": str(REPORT_MD),
            "audit_report_json": str(REPORT_JSON),
        },
        "governance": {
            "workloads": "appliance benchmark suite (matmul bf16/fp16/fp32-tf32 · attention bf16 @ 2k/4k/8k · batch 1/4) — R-14 serving-engine admission precondition",
            "in_perimeter": True,
            "no_estate_data": True,
            "sampler_interval_s": 300,
            "detachment": "setsid + nohup",
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2))

    # Markdown report
    lines = []
    lines.append("# GPU Utilization Report · 72-hour appliance benchmark suite")
    lines.append("")
    lines.append(f"**Generated at UTC:** {generated_at}")
    lines.append(f"**Launch (earliest host):** {earliest or 'PENDING'}")
    lines.append(f"**Elapsed:** {elapsed_h:.2f} hours · **Remaining:** {remaining_h:.2f} hours (of {WALL_CLOCK_H})")
    lines.append("")
    lines.append("## Workloads")
    lines.append("")
    lines.append("**Appliance benchmark suite** — rotating configuration matrix (matmul bf16/fp16/fp32-tf32 at 8192/12288/16384 square × attention bf16 at 2k/4k/8k seq × batch 1/4). Each iteration = one banked artefact (throughput TFLOPs + p50/p99 latency ms). Discharges R-14 serving-engine admission precondition. No estate data; no synthetic burn loops.")
    lines.append("")
    lines.append("## Governance")
    lines.append("")
    lines.append("- In-perimeter (SSH via `services.training_runner.ssh_seam` · env-injection creds · §E discipline).")
    lines.append("- No estate data (torch.randn on-device only).")
    lines.append("- Shape-only receipts (position-redaction preserved · SEC halt reading amended for this initiation per owner ruling 2026-09-16T~03:08Z).")
    lines.append("- Detached via `setsid nohup` — survives agent session boundaries.")
    lines.append("- Sampler cadence: 5 minutes per host (nvidia-smi query → append-only JSONL).")
    lines.append("")
    lines.append("## Per-host per-GPU rollup")
    lines.append("")
    if not host_states:
        lines.append("_(no host state yet)_")
    else:
        for h in host_states:
            lines.append(f"### Host `{h['host']}`")
            lines.append("")
            lines.append(f"- Start (UTC): `{h.get('start_utc') or 'PENDING'}`")
            lines.append(f"- Telemetry samples: **{h['telemetry_samples']}**")
            lines.append(f"- Bench iterations: **{h['bench_iterations']}** (ok: {h['bench_ok']})")
            lines.append("")
            if h["per_gpu"]:
                lines.append("| GPU | Name | Samples | Util avg | Util peak | Power avg (W) | Power peak (W) | Temp avg (°C) | Temp peak (°C) | Mem peak (MiB) |")
                lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
                for gi_s, g in sorted(h["per_gpu"].items(), key=lambda kv: int(kv[0])):
                    lines.append(
                        f"| {gi_s} | {g['gpu_name']} | {g['samples']} | "
                        f"{g['utilization_gpu_pct_avg']}% | {g['utilization_gpu_pct_peak']}% | "
                        f"{g['power_w_avg']} | {g['power_w_peak']} | "
                        f"{g['temp_c_avg']} | {g['temp_c_peak']} | "
                        f"{int(g['mem_used_mib_peak'])} |"
                    )
            else:
                lines.append("_(no per-GPU samples yet · sampler still initializing)_")
            lines.append("")
    lines.append("## Receipts index")
    lines.append("")
    lines.append("- Local sync root: `/app/assessment_workspace/phase0/gpu_utilization_72h/{akki-vm,akki-vm-ii}/`")
    lines.append("- Raw telemetry JSONL: `<host>/telemetry.jsonl` (one row per GPU per 5 min sample)")
    lines.append("- Raw workload JSONL: `<host>/workload.jsonl` (one row per bench iteration)")
    lines.append("- Machine-readable: `GPU_UTILIZATION_72H.json` (this same directory)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("READ STATE/STANDING_ORDERS.md FIRST — permanent standing law")
    REPORT_MD.write_text("\n".join(lines))
    return payload


def cmd_build_and_launch() -> int:
    print("== stage payloads ==")
    for h in HOSTS:
        r = stage_payloads(h)
        print(f"[{h}] rc={r['rc']}")
        print("  " + "\n  ".join(r["stdout"].splitlines()[-6:]))
    print("== launch detached ==")
    for h in HOSTS:
        r = launch_detached(h)
        print(f"[{h}] rc={r['rc']}")
        print("  " + "\n  ".join(r["stdout"].splitlines()[-14:]))
    print("== initial sync + report ==")
    time.sleep(6)
    return cmd_check_in()


def cmd_check_in() -> int:
    print("== sync jsonl ==")
    for h in HOSTS:
        r = sync_jsonl(h)
        print(f"[{h}] files: {r['files']}")
    print("== rollup ==")
    states = [_rollup_host(h) for h in HOSTS]
    for s in states:
        print(f"[{s['host']}] telemetry_samples={s['telemetry_samples']} bench_iters={s['bench_iterations']} per_gpu={len(s['per_gpu'])}")
    print("== regenerate report ==")
    payload = regenerate_report(states)
    print(f"REPORT_MD={REPORT_MD}")
    print(f"REPORT_JSON={REPORT_JSON}")
    print(f"elapsed_h={payload['elapsed_hours']} remaining_h={payload['remaining_hours']}")
    return 0


def cmd_status_only() -> int:
    for h in HOSTS:
        r = probe_state(h)
        print(f"====[{h}]==== rc={r['rc']}")
        print(r["stdout"])
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "status_only"
    if mode == "build_and_launch":
        sys.exit(cmd_build_and_launch())
    elif mode == "check_in":
        sys.exit(cmd_check_in())
    elif mode == "status_only":
        sys.exit(cmd_status_only())
    else:
        print(f"unknown mode: {mode}", file=sys.stderr)
        sys.exit(2)
