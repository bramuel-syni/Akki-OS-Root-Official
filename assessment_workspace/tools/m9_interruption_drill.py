#!/usr/bin/env python3
"""M8-T1 / M9-T3 physical interruption drill — API-only orchestration (the same seam an operator uses).

1. commission a short governed text run (1.7B · sealed corpus · Young/Daly cadence · durable off-host copy);
2. wait until the host has written at least one checkpoint and advanced past it;
3. SIGKILL the worker process through /interrupt (physical process loss — no in-process hook);
4. commission the continuation (`resume_from_job_id`) — the worker restores all five carriers from the host checkpoint or refuses;
5. compose the receipt from the two banked records (work lost vs the ratified 15-min RPO; single certificate; single usage receipt).

Usage: AKKI_DRILL_EMAIL / AKKI_DRILL_PASSWORD in the environment; python3 m9_interruption_drill.py [--host akki-vm-ii] [--gpu 0]
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = Path("/app/frontend/.env").read_text().split("REACT_APP_BACKEND_URL=")[1].splitlines()[0].strip()
LOG = Path("/app/assessment_workspace/notes/m8_m9_completion_20260930/interruption_drill.log")


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def call(method, path, token=None, body=None, timeout=180):
    headers = {"Content-Type": "application/json", "User-Agent": "akki-drill/1.0", **({"Authorization": "Bearer " + token} if token else {})}
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read() or b"{}"
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw.decode(errors="replace")[:300]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--host", default="akki-vm-ii"); ap.add_argument("--gpu", type=int, default=0); ap.add_argument("--kill-after-steps", type=int, default=160)
    ap.add_argument("--max-steps", type=int, default=320); ap.add_argument("--checkpoint-every", type=int, default=100)
    args = ap.parse_args()
    code, body = call("POST", "/api/auth/login", body={"email": os.environ["AKKI_DRILL_EMAIL"], "password": os.environ["AKKI_DRILL_PASSWORD"]})
    assert code == 200, body
    token = body["access_token"]
    params = {"tenant_id": "RMS", "phase": "train", "host": args.host, "gpu_index": args.gpu, "corpus_id": "rms-transcripts-v1", "non_target_corpus_id": "digicow-sealed-units-v1",
              "base": "qwen3-1.7b-base", "acceptance_floor": 0.9, "drill": True, "prune_fraction": 0.3, "distance_probe": {"samples": 40, "max_new_tokens": 24},
              "recipe": {"lr": 0.0002, "epochs": 1, "max_steps": args.max_steps, "batch_size": 512, "grad_accum": 1, "max_seq_len": 256, "tokens_per_batch": 12288, "gradient_checkpointing": False,
                         "warmup_steps": 20, "checkpoint_every": args.checkpoint_every, "checkpoint_cadence": "young_daly", "durable_checkpoint_dir": "/mnt/akki-storage-3388s/akki-m9-durable",
                         "eval_every": 0, "eval_batch_size": 64, "eval_cap_per_stratum": 100}}
    code, body = call("POST", "/api/training/m9/jobs", token, params)
    assert code == 202, body
    job = body["job"]; killed_id = job["job_id"]
    log(f"submitted drill run {killed_id} status={job['status']} reason={job.get('reason')}")
    assert job["status"] == "running", job
    step = 0
    while True:
        time.sleep(20)
        code, body = call("GET", f"/api/training/m9/jobs/{killed_id}", token)
        j = body["job"]; prog = ((j.get("remote_state") or {}).get("progress") or {})
        step = prog.get("step") or 0
        log(f"{killed_id} {j['status']} stage={prog.get('stage')} step={step} last_ckpt={prog.get('last_checkpoint_step')} next_ckpt={prog.get('next_checkpoint_step')} tps={prog.get('tokens_per_second')}")
        if j["status"] != "running":
            log("run ended before the kill point; abort"); sys.exit(2)
        if prog.get("last_checkpoint_step") and step >= args.kill_after_steps:
            break
    code, body = call("POST", f"/api/training/m9/jobs/{killed_id}/interrupt", token, {"tenant_id": "RMS", "reason": "M8-T1/M9-T3 physical process-loss drill (SIGKILL)"})
    log(f"interrupt → {code} {json.dumps((body.get('job') or {}).get('interrupt_rpc'))} status={(body.get('job') or {}).get('status')}")
    assert code == 200 and body["job"]["status"] == "interrupted", body
    time.sleep(5)
    resume = {**params, "resume_from_job_id": killed_id}
    code, body = call("POST", "/api/training/m9/jobs", token, resume)
    assert code == 202, body
    resumed_id = body["job"]["job_id"]
    log(f"submitted continuation {resumed_id} status={body['job']['status']} reason={body['job'].get('reason')}")
    while True:
        time.sleep(30)
        code, body = call("GET", f"/api/training/m9/jobs/{resumed_id}", token)
        j = body["job"]; prog = ((j.get("remote_state") or {}).get("progress") or {})
        log(f"{resumed_id} {j['status']} stage={prog.get('stage')} step={prog.get('step')} resumed={json.dumps(prog.get('resumed'))[:160]}")
        if j["status"] != "running":
            break
    if j["status"] != "completed":
        log(f"continuation ended {j['status']}: {j.get('reason')} log_tail={j.get('worker_log_tail','')[-600:]}"); sys.exit(3)
    code, body = call("POST", "/api/training/m9/drills/interruption", token, {"tenant_id": "RMS", "killed_job_id": killed_id, "resumed_job_id": resumed_id})
    log(f"receipt → {code} {json.dumps(body.get('receipt', body).get('measured'))} verdict={body.get('receipt', {}).get('verdict')} path={body.get('receipt', {}).get('receipt_path')}")


if __name__ == "__main__":
    main()
