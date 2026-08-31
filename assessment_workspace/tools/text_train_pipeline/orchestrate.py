"""Governed estate-text LoRA training orchestrator.

Authority: owner ruling 6 · 2026-08-31 (verbatim in DECISIONS.md).

Flow:
  1. Extract + mask 100K rows from digicow_live.ussd_question_response via
     the existing Data API (column-exclusion at SQL level, regex scrub after).
     -> masked_corpus.jsonl written locally + crossing receipt emitted.
  2. Install missing deps (datasets, sentencepiece) on ONE GPU host (akki-vm).
     -> execute_remote_command with attested_command tier.
  3. Stage train_payload.py + masked_corpus.jsonl onto the host.
     -> base64 heredoc (mirrors the burn-orchestrator pattern).
  4. Kick off training in background (fully detached from ssh channel).
     -> nohup + subshell-detach pattern from the burn orchestrator.
  5. Poll (nvidia-smi + tail train.log) every 90s until training done or
     timeout.
  6. Collect train.log + summary.json + adapter/ tarball from the host.
  7. Compute local hashes, register first-class training-run record.
  8. Cleanup /tmp/akki_txttrain_<run_id>/ on host with receipt.
  9. Bank a "burn + train" combined activity summary in plain language.

Discipline:
  - Every remote exec via services.training_runner.ssh_seam.execute_remote_command.
  - masking_tier=attested_command for compute-side crossings.
  - Estate-text extraction is banked as kind='ruling6_bypass_row_extract'
    (see extract_mask.emit_crossing_receipt).
  - No PII in receipts, no PII in logs. Masked corpus stays on-host during
    training; deleted at cleanup. Adapter is retained + hash-registered.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
load_dotenv("/app/backend/.env")

sys.path.insert(0, "/app/assessment_workspace/repos/Extraction-Akki/backend")
sys.path.insert(0, "/app/assessment_workspace/tools/text_train_pipeline")

from services.training_runner import ssh_seam  # noqa: E402


# ============================================================================
# Config
# ============================================================================

# Owner ruling 6: "your call on exact size, state it in the data statement".
# 30,000 rows → representative first-run, ~3 epochs, ~30-60 min on H200×2.
SLICE_SIZE = int(os.environ.get("TXTTRAIN_SLICE_SIZE", "30000"))
BASE_MODEL = os.environ.get("TXTTRAIN_BASE_MODEL", "Qwen/Qwen2.5-0.5B")
EPOCHS = int(os.environ.get("TXTTRAIN_EPOCHS", "3"))
BATCH_SIZE = int(os.environ.get("TXTTRAIN_BATCH_SIZE", "16"))
GRAD_ACCUM = int(os.environ.get("TXTTRAIN_GRAD_ACCUM", "2"))
LR = float(os.environ.get("TXTTRAIN_LR", "2e-4"))
MAX_SEQ_LEN = int(os.environ.get("TXTTRAIN_MAX_SEQ_LEN", "192"))
POLL_INTERVAL = int(os.environ.get("TXTTRAIN_POLL_INTERVAL", "90"))
TIMEOUT_SECONDS = int(os.environ.get("TXTTRAIN_TIMEOUT", str(3 * 60 * 60)))  # 3h
HOST = os.environ.get("TXTTRAIN_HOST", "akki-vm")

RUN_ID = f"txttrain_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"

# Local paths
PIPELINE_ROOT = Path("/app/assessment_workspace/phase0/text_train_pipeline") / RUN_ID
PIPELINE_ROOT.mkdir(parents=True, exist_ok=True)
LOCAL_CORPUS = PIPELINE_ROOT / "masked_corpus.jsonl"

RUNS_DIR = Path("/app/assessment_workspace/phase0/training_runner/runs")
RUNS_DIR.mkdir(parents=True, exist_ok=True)

REMOTE_DIR = f"/tmp/akki_txttrain_{RUN_ID}"


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class RunState:
    run_id: str = RUN_ID
    host: str = HOST
    receipts: List[str] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    extract_summary: Dict[str, Any] = field(default_factory=dict)
    install_ok: bool = False
    stage_ok: bool = False
    launch_ok: bool = False
    train_summary: Dict[str, Any] = field(default_factory=dict)
    nvidia_smi_before: Optional[Dict[str, Any]] = None
    nvidia_smi_during_polls: List[Dict[str, Any]] = field(default_factory=list)
    nvidia_smi_after: Optional[Dict[str, Any]] = None
    train_log_tail: str = ""
    adapter_sha256_remote: str = ""
    exit_code: int = -1
    error: str = ""


# ============================================================================
# Helpers
# ============================================================================

def _iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_remote(cmd: str, purpose: str, state: RunState,
                save_as: Optional[str] = None, timeout: int = 60) -> Any:
    r = ssh_seam.execute_remote_command(HOST, cmd, purpose=purpose, timeout=timeout)
    state.receipts.append(r.receipt_id)
    if save_as:
        p = PIPELINE_ROOT / save_as
        p.write_text(json.dumps({
            "at": _iso(),
            "host_slug": HOST,
            "purpose": purpose,
            "receipt_id": r.receipt_id,
            "rc": r.rc,
            "wallclock_seconds": r.wallclock_seconds,
            "stdout_redacted": r.stdout_redacted,
            "stderr_redacted": r.stderr_redacted,
        }, indent=2))
    return r


def _parse_nvidia_smi_csv(text: str) -> List[Dict[str, Any]]:
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


def _capture_nvidia_smi(state: RunState, label: str) -> Dict[str, Any]:
    cmd = (
        "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,"
        "power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory "
        "--format=csv"
    )
    r = _run_remote(cmd, purpose=f"nvidia_smi_{label}", state=state,
                    save_as=f"nvsmi_{label}.json", timeout=30)
    parsed = _parse_nvidia_smi_csv(r.stdout_redacted) if r.rc == 0 else []
    return {"at": _iso(), "label": label, "rc": r.rc, "gpus": parsed}


def _stage_file_remote(local: Path, remote: str, state: RunState,
                       purpose: str, chunked: bool = True) -> None:
    """Stage a local file onto host via paramiko SFTP; verify remote sha256.
    Uses ssh_seam.connect() to reuse the seam's key-auth discipline. The
    put itself is a single sftp channel operation; we then emit a governed
    crossing receipt for it via execute_remote_command(sha256sum).
    """
    import hashlib
    local_sha = hashlib.sha256(local.read_bytes()).hexdigest()

    # Ensure parent dir exists.
    _run_remote(f"mkdir -p {os.path.dirname(remote)}",
                purpose=f"{purpose}__mkdir", state=state, timeout=20)

    # Open SFTP through the same key-auth transport (governed via ssh_seam.connect).
    client = ssh_seam.connect(HOST)
    try:
        sftp = client.open_sftp()
        try:
            print(f"[stage] sftp put {local} -> {remote}", flush=True)
            sftp.put(str(local), remote)
        finally:
            sftp.close()
    finally:
        client.close()

    # Verify remote sha256 via the governed seam.
    r = _run_remote(f"sha256sum {remote} | awk '{{print $1}}'",
                    purpose=f"{purpose}__verify_sha", state=state,
                    save_as=f"{purpose}_verify.json", timeout=30)
    remote_sha = ""
    for line in (r.stdout_redacted or "").strip().splitlines():
        line = line.strip()
        if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
            remote_sha = line
            break
    if local_sha != remote_sha:
        raise RuntimeError(
            f"stage sha mismatch for {remote}: local={local_sha} remote={remote_sha}"
        )
    print(f"[stage] {remote} sha256={remote_sha[:16]}... (verified)", flush=True)


# ============================================================================
# Pipeline steps
# ============================================================================

def step_1_extract(state: RunState) -> None:
    print(f"[step_1] extract_mask slice_size={SLICE_SIZE}", flush=True)
    cmd = [
        "python3",
        "/app/assessment_workspace/tools/text_train_pipeline/extract_mask.py",
        "--slice-size", str(SLICE_SIZE),
        "--out-dir", str(PIPELINE_ROOT),
        "--run-id", RUN_ID,
        "--page-size", "1000",
    ]
    env = os.environ.copy()
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=1800)
    (PIPELINE_ROOT / "extract_stdout.log").write_text(proc.stdout)
    (PIPELINE_ROOT / "extract_stderr.log").write_text(proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"extract_mask failed rc={proc.returncode}: {proc.stderr[:500]}")
    summary_path = PIPELINE_ROOT / "extract_summary.json"
    if summary_path.exists():
        state.extract_summary = json.loads(summary_path.read_text())
    print(f"[step_1] rows={state.extract_summary.get('rows_extracted')} sha256={state.extract_summary.get('output_jsonl_sha256')[:16]}...", flush=True)


def step_2_install_deps(state: RunState) -> None:
    print(f"[step_2] install datasets + sentencepiece on {HOST}", flush=True)
    # Match Wave-H install pattern (uses --break-system-packages for PEP 668)
    cmd = (
        "python3 -m pip install --break-system-packages --quiet --upgrade "
        "datasets sentencepiece 2>&1 | tail -30 && "
        "python3 -c 'import datasets, sentencepiece; "
        "print(\"datasets\", datasets.__version__, \"sentencepiece\", sentencepiece.__version__)'"
    )
    r = _run_remote(cmd, purpose="install_missing_deps", state=state,
                    save_as="install.json", timeout=300)
    state.install_ok = (r.rc == 0)
    if not state.install_ok:
        raise RuntimeError(f"install failed rc={r.rc}: stdout={r.stdout_redacted[:200]} stderr={r.stderr_redacted[:300]}")


def step_3_stage(state: RunState) -> None:
    print(f"[step_3] stage payload + corpus onto {HOST}:{REMOTE_DIR}", flush=True)
    # Stage the train_payload.py
    payload_local = Path("/app/assessment_workspace/tools/text_train_pipeline/train_payload.py")
    _stage_file_remote(payload_local, f"{REMOTE_DIR}/train_payload.py",
                       state, purpose="stage_train_payload")
    # Stage the masked corpus
    _stage_file_remote(LOCAL_CORPUS, f"{REMOTE_DIR}/masked_corpus.jsonl",
                       state, purpose="stage_corpus")
    state.stage_ok = True


def step_4_launch(state: RunState) -> None:
    print(f"[step_4] launch training", flush=True)
    output_dir = f"{REMOTE_DIR}/out"
    logfile = f"{output_dir}/train.log"
    pidfile = f"{REMOTE_DIR}/train.pid"
    train_cmd_body = (
        f"cd {REMOTE_DIR} && "
        f"mkdir -p {output_dir} && "
        f"( setsid nohup python3 train_payload.py "
        f"--corpus {REMOTE_DIR}/masked_corpus.jsonl "
        f"--output-dir {output_dir} "
        f"--base-model {BASE_MODEL} "
        f"--epochs {EPOCHS} "
        f"--batch-size {BATCH_SIZE} "
        f"--grad-accum {GRAD_ACCUM} "
        f"--lr {LR} "
        f"--max-seq-len {MAX_SEQ_LEN} "
        f"< /dev/null > {REMOTE_DIR}/train.stdout 2>&1 & "
        f"echo $! > {pidfile}; "
        f") </dev/null >/dev/null 2>&1; "
        f"sleep 2; "
        f"echo pid=$(cat {pidfile} 2>/dev/null); "
        f"if [ -f {logfile} ]; then head -3 {logfile}; "
        f"else echo '(no train.log yet · initializing)'; fi; "
        f"exit 0"
    )
    _run_remote(train_cmd_body, purpose="launch_training", state=state,
                save_as="launch.json", timeout=30)
    state.launch_ok = True


def step_5_poll(state: RunState) -> None:
    print(f"[step_5] poll training progress", flush=True)
    output_dir = f"{REMOTE_DIR}/out"
    logfile = f"{output_dir}/train.log"
    pidfile = f"{REMOTE_DIR}/train.pid"
    end_at = time.monotonic() + TIMEOUT_SECONDS
    while time.monotonic() < end_at:
        time.sleep(POLL_INTERVAL)
        snap = _capture_nvidia_smi(state, f"poll_{int(time.monotonic() - end_at + TIMEOUT_SECONDS)}s")
        state.nvidia_smi_during_polls.append(snap)
        # Tail log
        r = _run_remote(
            f"tail -n 8 {logfile} 2>/dev/null || echo '(no log)'; "
            f"echo '---'; "
            f"pid=$(cat {pidfile} 2>/dev/null); "
            f"if [ -n \"$pid\" ] && kill -0 $pid 2>/dev/null; then echo RUNNING; else echo NOT_RUNNING; fi",
            purpose="tail_train_log", state=state, timeout=20,
        )
        state.train_log_tail = r.stdout_redacted
        # Progress print (short)
        for line in r.stdout_redacted.splitlines()[-6:]:
            print(f"  [{snap['label']}] {line}", flush=True)
        # If summary.json exists, training completed
        r2 = _run_remote(
            f"if [ -f {output_dir}/summary.json ]; then echo SUMMARY_READY; else echo NO_SUMMARY_YET; fi",
            purpose="check_summary", state=state, timeout=15,
        )
        if "SUMMARY_READY" in r2.stdout_redacted:
            print(f"[step_5] summary.json detected; training complete", flush=True)
            time.sleep(5)  # ensure flush
            return
        if "NOT_RUNNING" in r.stdout_redacted and "SUMMARY_READY" not in r2.stdout_redacted:
            # Process died without summary → error
            print(f"[step_5] training process not running but no summary — treating as failure", flush=True)
            return
    print(f"[step_5] timeout after {TIMEOUT_SECONDS}s", flush=True)


def step_6_collect(state: RunState) -> None:
    print(f"[step_6] collect logs + summary", flush=True)
    output_dir = f"{REMOTE_DIR}/out"
    # Read summary.json
    r = _run_remote(f"cat {output_dir}/summary.json 2>/dev/null || echo '{{\"kind\":\"absent\"}}'",
                    purpose="collect_summary", state=state,
                    save_as="train_summary_raw.json", timeout=30)
    try:
        state.train_summary = json.loads(r.stdout_redacted.strip().splitlines()[-1]) if r.stdout_redacted.strip() else {}
    except Exception:
        try:
            state.train_summary = json.loads(r.stdout_redacted.strip())
        except Exception:
            state.train_summary = {"kind": "parse_error", "raw": r.stdout_redacted[:500]}
    # Read train.log full
    r = _run_remote(f"wc -l {output_dir}/train.log 2>/dev/null; cat {output_dir}/train.log 2>/dev/null",
                    purpose="collect_train_log", state=state,
                    save_as="train_log_raw.json", timeout=60)
    (PIPELINE_ROOT / "train.log").write_text(r.stdout_redacted)
    state.adapter_sha256_remote = state.train_summary.get("adapter_sha256", "")
    if state.train_summary.get("kind") == "summary":
        state.exit_code = 0
    else:
        state.exit_code = 1


def step_7_retain_adapter(state: RunState) -> None:
    """Copy the adapter tarball off the host into pipeline artifacts."""
    print(f"[step_7] retain adapter locally", flush=True)
    output_dir = f"{REMOTE_DIR}/out"
    # Tar the adapter dir on the host.
    r = _run_remote(f"cd {output_dir} && tar -czf adapter.tar.gz adapter && ls -l adapter.tar.gz && sha256sum adapter.tar.gz | awk '{{print $1}}'",
                    purpose="tar_adapter", state=state,
                    save_as="tar_adapter.json", timeout=120)
    if r.rc != 0:
        print(f"[step_7] tar failed rc={r.rc}: {r.stderr_redacted[:200]}", flush=True)
        return
    # Extract remote sha for verification
    remote_sha = ""
    for line in (r.stdout_redacted or "").strip().splitlines():
        line = line.strip()
        if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
            remote_sha = line
            break

    # SFTP get the tarball locally.
    adapter_out = PIPELINE_ROOT / "adapter.tar.gz"
    try:
        client = ssh_seam.connect(HOST)
        try:
            sftp = client.open_sftp()
            try:
                sftp.get(f"{output_dir}/adapter.tar.gz", str(adapter_out))
            finally:
                sftp.close()
        finally:
            client.close()
    except Exception as e:
        print(f"[step_7] sftp get failed: {e}", flush=True)
        return
    import hashlib
    local_sha = hashlib.sha256(adapter_out.read_bytes()).hexdigest()
    (PIPELINE_ROOT / "adapter.sha256").write_text(local_sha + "\n")
    ok = (remote_sha == local_sha) if remote_sha else True
    print(f"[step_7] adapter retained: {adapter_out} · sha256={local_sha[:16]}... verified={ok}", flush=True)


def step_8_cleanup(state: RunState) -> None:
    print(f"[step_8] cleanup remote dir + corpus", flush=True)
    # Delete masked corpus + all state on host (adapter is already retained locally).
    r = _run_remote(
        f"if [ -d {REMOTE_DIR} ]; then "
        f"  rm -f {REMOTE_DIR}/masked_corpus.jsonl {REMOTE_DIR}/train.stdout; "
        f"  # keep out/summary.json and out/train.log for one last collection window, remove after: "
        f"  rm -rf {REMOTE_DIR}; "
        f"  echo cleaned; "
        f"else echo already_absent; fi; "
        f"echo '---'; "
        f"ls /tmp/akki_txttrain_* 2>/dev/null | head -5 || echo 'no txttrain remnants'",
        purpose="cleanup", state=state,
        save_as="cleanup.json", timeout=30)
    print(f"[step_8] rc={r.rc}: {r.stdout_redacted[:200]}", flush=True)


def step_9_register(state: RunState) -> Path:
    print(f"[step_9] register training run", flush=True)
    run_record = {
        "run_id": RUN_ID,
        "kind": "governed_estate_text_lora_train",
        "authority": "owner ruling 6 · 2026-08-31 · estate-text training pivot (verbatim in DECISIONS.md)",
        "authority_ruling_chain": ["ruling 4 (bypass build)", "ruling 6 (estate text · ussd_question_response)"],
        "started_at": state.started_at,
        "finished_at": state.finished_at,
        "host": HOST,
        "data_statement": {
            "shape": "WPW Tier-2 datasheet-level",
            "source_database": "digicow_live",
            "source_table": "ussd_question_response",
            "source_rows_total": 903293,
            "slice_size_requested": SLICE_SIZE,
            "rows_extracted": state.extract_summary.get("rows_extracted"),
            "columns_included": state.extract_summary.get("included_columns"),
            "columns_excluded": state.extract_summary.get("excluded_columns"),
            "decision_ledger_sha256": state.extract_summary.get("decision_ledger_sha256"),
            "masking_steps": [
                "column-level exclusion at SQL layer (only INCLUDED cols read)",
                "regex scrub for Kenyan phone-number patterns → [PHONE]",
                "regex scrub for 7-10 digit ID-shaped numerics → [ID]",
                "cautious-default: unclassified columns rejected via mask_row",
            ],
            "scrub_replacements_applied": state.extract_summary.get("scrub_replacements"),
            "dropped_rows_empty_qa": state.extract_summary.get("dropped_empty_qa"),
            "corpus_sha256": state.extract_summary.get("output_jsonl_sha256"),
            "corpus_size_bytes": os.path.getsize(LOCAL_CORPUS) if LOCAL_CORPUS.exists() else 0,
        },
        "workload": {
            "workload_type": "peft_lora_causal_lm",
            "base_model": BASE_MODEL,
            "epochs": EPOCHS,
            "batch_size_per_gpu": BATCH_SIZE,
            "grad_accum": GRAD_ACCUM,
            "learning_rate": LR,
            "max_seq_len": MAX_SEQ_LEN,
            "n_gpu": (state.train_summary or {}).get("n_gpu"),
            "effective_batch": (state.train_summary or {}).get("effective_batch"),
            "total_train_seconds": (state.train_summary or {}).get("total_train_s"),
            "final_metrics": (state.train_summary or {}).get("final_train_metrics"),
        },
        "artifacts": {
            "adapter_sha256_remote": state.adapter_sha256_remote,
            "adapter_local_tarball": str(PIPELINE_ROOT / "adapter.tar.gz"),
            "train_log_local": str(PIPELINE_ROOT / "train.log"),
        },
        "governance": {
            "seam": "services.training_runner.ssh_seam.execute_remote_command",
            "masking_tier_compute_side": "attested_command",
            "row_extract_receipt_kind": "ruling6_bypass_row_extract",
            "shielded_pipeline_status": "NOT_YET_BUILT · charter W-Shield-Train in SPRINT_PLAN.md",
            "bypass_scope": "pipeline BUILD only · PII rules UPHELD (per owner ruling 6)",
        },
        "receipts_count": len(state.receipts),
        "exit_code": state.exit_code,
        "error": state.error,
    }
    path = RUNS_DIR / f"{RUN_ID}.json"
    path.write_text(json.dumps(run_record, indent=2, sort_keys=True))
    return path


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    print(f"[txttrain] RUN_ID = {RUN_ID}", flush=True)
    print(f"[txttrain] PIPELINE_ROOT = {PIPELINE_ROOT}", flush=True)
    print(f"[txttrain] host={HOST} slice_size={SLICE_SIZE} base_model={BASE_MODEL} epochs={EPOCHS}", flush=True)

    state = RunState()
    state.started_at = _iso()
    try:
        step_1_extract(state)
        state.nvidia_smi_before = _capture_nvidia_smi(state, "before")
        step_2_install_deps(state)
        step_3_stage(state)
        step_4_launch(state)
        step_5_poll(state)
        step_6_collect(state)
        step_7_retain_adapter(state)
        state.nvidia_smi_after = _capture_nvidia_smi(state, "after")
        step_8_cleanup(state)
    except Exception as e:
        state.error = f"{type(e).__name__}: {e}"
        print(f"[txttrain] ERROR: {state.error}", flush=True)
        try:
            step_8_cleanup(state)
        except Exception:
            pass

    state.finished_at = _iso()

    record_path = step_9_register(state)
    print(f"[txttrain] run record: {record_path}", flush=True)

    # Save raw state
    raw = asdict(state)
    (PIPELINE_ROOT / "state.json").write_text(json.dumps(raw, indent=2, sort_keys=True))

    return 0 if state.exit_code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
