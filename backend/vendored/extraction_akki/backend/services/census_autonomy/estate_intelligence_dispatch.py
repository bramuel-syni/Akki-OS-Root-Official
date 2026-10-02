"""Control plane for the Estate Intelligence census on the admitted census worker (akki-vm).

Same discipline as the language-cognition dispatcher: reviewed code ships over the pinned SSH seam,
estate and jump credentials cross only on stdin, the job daemonises on the worker and writes its
own state/receipt there. E1 keeps a secret-free job record, reads status by one bounded RPC and
banks Northena admit/converge rows. RMS is census-only: the worker returns aggregates, never rows.
"""
import hashlib
import json
import os
import shlex
import time
import uuid
from pathlib import Path

from services.audio_plane_v1.language_cognition_dispatch import _ledger, _loop, now  # noqa: F401 (shared loop/ledger seam)
from services.census_autonomy import engine
from services.census_autonomy.deep_bundle import MODULES as CENSUS_MODULES, build_bundle
from services.census_autonomy.deep_dispatch import connector_for, pull_seam_hop

PHASE = "estate_intelligence"
WORKER = "services/census_autonomy/estate_intelligence_worker.py"
BOOTSTRAP = '''import sys,json,base64,pathlib,hashlib,os
p=json.load(sys.stdin)
p['bundle_b64']=p.pop('bundle')
b=base64.b64decode(p['bundle_b64'])
if hashlib.sha256(b).hexdigest()!=p['code_sha256']: raise ValueError('CODE_HASH_MISMATCH')
d=pathlib.Path(p['job_dir']); d.mkdir(parents=True,exist_ok=True)
z=d/'worker.zip'; z.write_bytes(b)
pid=os.fork()
if pid>0:
    print(json.dumps({'job_id':p['job_id'],'pid':pid,'job_dir':str(d)}),flush=True); os._exit(0)
os.setsid(); sys.stdin.close()
out=open(d/'worker.log','ab',buffering=0); os.dup2(out.fileno(),1); os.dup2(out.fileno(),2)
sys.path.insert(0,str(z))
from services.census_autonomy.estate_intelligence_worker import execute
execute(p)
'''


def _jobs_dir():
    path = engine.CENSUS_STATE_DIR / PHASE
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_job(job):
    path = _jobs_dir() / f"{job['job_id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(job, indent=1, default=str))
    os.replace(tmp, path)
    return job


def load_job(job_id):
    try:
        return json.loads((_jobs_dir() / f"{job_id}.json").read_text())
    except (OSError, ValueError):
        return None


def list_jobs():
    jobs = []
    for path in _jobs_dir().glob("eij-*.json"):
        if "." in path.stem:  # sidecars (.report/.detail/.dossier) live beside the job record
            continue
        try:
            jobs.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return sorted(jobs, key=lambda j: j.get("submitted_at", ""), reverse=True)


def bundle():
    return build_bundle(CENSUS_MODULES + [WORKER])


def _remote_root():
    return os.environ["CENSUS_REMOTE_STATE_DIR"].rstrip("/") + "/estate_intelligence"


PHASES = {PHASE: "eij-", "text_estate": "etx-"}  # text_estate: aggregate-only reads of the written-word stores (owner order 2026-10-02)


def submit(source, params, principal_id, lawful_ref, timeout=90, phase=PHASE):
    """Admit through Northena, resolve custody, ship the worker, daemonise on the census worker of record."""
    from services.census_autonomy.remote_dispatch import _connect
    if source != "rms_mysql":
        raise ValueError("ESTATE_INTELLIGENCE_SOURCE_NOT_ADMITTED")
    host = os.environ["CENSUS_PRIMARY_WORKER"]
    job_id = PHASES[phase] + uuid.uuid4().hex[:12]
    lawful_hash = hashlib.sha256(Path(os.environ["CENSUS_LAWFUL_BASIS_PATH"]).read_bytes()).hexdigest()
    job = {"job_id": job_id, "phase": phase, "source_id": source, "host": host, "principal_id": principal_id, "submitted_at": now(),
           "params": {k: v for k, v in (params or {}).items()}, "northena_run_id": f"run-{uuid.uuid4().hex[:12]}",
           "northena_trace_id": f"trc-{uuid.uuid4().hex[:12]}", "lawful_basis_ref": str(lawful_ref), "lawful_basis_sha256": lawful_hash,
           "governing_artifact_ref": {"artifact_type": "objective_request", "artifact_id": "CP-CENSUS-ESTATE-INTELLIGENCE", "version": job_id},
           "remote": {"root": _remote_root(), "job_dir": f"{_remote_root()}/jobs/{job_id}"}, "status": "submitting",
           "scope": "census only: aggregates, sketches and hashes; no row values retained or returned"}
    _ledger(job, "admit", "admitted", f"estate_intelligence_{source}_admitted", {"host": host, "lawful_basis_sha256": lawful_hash})
    code_b64, code_hash = bundle()
    connector = connector_for(job_id, "RMS", source, lawful_hash)
    control = {"bundle": code_b64, "code_sha256": code_hash, "job_id": job_id, "phase": phase, "runtime_id": host, **({"targets": params["targets"]} if phase == "text_estate" else {}),
               "hostname_expected": os.environ[f"{host.upper().replace('-', '_')}_HOSTNAME_EXPECTED"],
               "job_dir": job["remote"]["job_dir"], "connections": connector["connections"], "pull_via": pull_seam_hop(),
               "max_seconds": int((params or {}).get("max_seconds", 3 * 86400)), "database_seconds": int((params or {}).get("database_seconds", 5400))}
    job["connections"] = [{"label": c["label"], "host_fingerprint": hashlib.sha256(c["host"].encode()).hexdigest()[:12]} for c in connector["connections"]]
    client = None
    try:
        client, _config = _connect(host, min(20, timeout))
        channel = client.get_transport().open_session(timeout=15)
        channel.settimeout(timeout)
        channel.exec_command(shlex.quote(os.environ["CENSUS_REMOTE_PYTHON"]) + " -c " + shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(control).encode())
        channel.shutdown_write()
        output, diagnostic = bytearray(), bytearray()
        deadline = time.time() + timeout
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
            if channel.recv_stderr_ready():
                diagnostic.extend(channel.recv_stderr(65536))
            if channel.exit_status_ready() and getattr(channel, "eof_received", True) and not channel.recv_ready() and not channel.recv_stderr_ready():
                break
            if time.time() >= deadline:
                channel.close()
                raise TimeoutError("SUBMIT_TIMEOUT")
            time.sleep(0.05)
        if channel.recv_exit_status() != 0:
            raise ValueError("REMOTE_BOOTSTRAP_FAILED:" + diagnostic.decode(errors="replace")[-300:])
        ack = json.loads(output.decode())
        job.update(status="running", code_sha256=code_hash, remote={**job["remote"], "pid": ack["pid"]}, started_at=now())
        _ledger(job, "gate", "warm", f"estate_intelligence_daemonised:pid={ack['pid']}")
    except Exception as exc:
        job.update(status="refused", reason=f"{type(exc).__name__}: {str(exc)[:300]}")
        _ledger(job, "gate", "refused", f"estate_intelligence_dispatch_failed:{type(exc).__name__}")
    finally:
        if client is not None:
            client.close()
    return save_job(job)


def refresh(job_id):
    """One bounded status RPC: host-side state and receipt (digest-verified) — aggregates only."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job:
        return None
    if job["status"] in ("completed", "partial", "failed", "refused", "cancelled"):
        return job
    job_dir = job["remote"]["job_dir"]
    command = (f"cat {shlex.quote(job_dir + '/state.json')} 2>/dev/null; echo; echo __RECEIPT__; "
               f"cat {shlex.quote(job_dir + '/receipt.json')} 2>/dev/null; echo; echo __LOG__; tail -c 1200 {shlex.quote(job_dir + '/worker.log')} 2>/dev/null; "
               f"echo; echo __ALIVE__; kill -0 {int(job['remote'].get('pid') or 0)} 2>/dev/null && echo yes || echo no")
    result = execute_remote_command(job["host"], command, purpose=f"estate_intelligence_status:{job_id}", timeout=60)
    job["last_status_rpc"] = {"at": now(), "rc": result.rc, "receipt_id": result.receipt_id}
    if result.rc != 0:
        job["last_status_rpc"]["error"] = result.stderr_redacted[:300]
        return save_job(job)
    state_text, _, rest = result.stdout_redacted.partition("__RECEIPT__")
    receipt_text, _, rest = rest.partition("__LOG__")
    log_text, _, alive = rest.partition("__ALIVE__")
    try:
        job["remote_state"] = json.loads(state_text.strip()) if state_text.strip() else None
    except ValueError:
        job["remote_state"] = None
    job["worker_log_tail"] = log_text.strip()[-1200:]
    job["process_alive"] = alive.strip() == "yes"
    if receipt_text.strip():
        try:
            receipt = json.loads(receipt_text.strip())
        except ValueError:
            receipt = None
        if receipt:
            digest = receipt.pop("receipt_sha256", None)
            body = json.dumps(receipt, sort_keys=True, default=str).encode()
            receipt["receipt_sha256"] = digest
            receipt["digest_verified"] = hashlib.sha256(body).hexdigest() == digest
            job["receipt"] = receipt
            if not receipt["digest_verified"] or receipt.get("job_id") != job_id or receipt.get("phase") != job.get("phase", PHASE):
                job.update(status="failed", reason="WORKER_RECEIPT_INTEGRITY_FAILED", finished_at=now())
            else:
                job["status"] = receipt.get("status", "failed")
                job["finished_at"] = receipt.get("finished_at")
            _ledger(job, "converge", "terminate_success" if job["status"] in ("completed", "partial") else "terminate_budget",
                    f"estate_intelligence_{job['status']}", {"receipt_sha256": digest})
    elif not job["process_alive"]:
        job["status"] = "failed"
        job["reason"] = "worker process gone without a terminal receipt; retained progress is not completion"
        _ledger(job, "converge", "terminate_budget", "estate_intelligence_failed", None)
    return save_job(job)


def cancel(job_id, reason):
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job or job["status"] != "running":
        return job
    pid = int(job["remote"].get("pid") or 0)
    if pid <= 0:
        raise ValueError("CANCEL_REQUIRES_A_KNOWN_WORKER_PID")
    command = (f"kill -TERM {pid} 2>/dev/null; sleep 3; if kill -0 {pid} 2>/dev/null; then kill -KILL {pid} 2>/dev/null; sleep 1; fi; "
               f"kill -0 {pid} 2>/dev/null && echo still_alive || echo stopped")
    result = execute_remote_command(job["host"], command, purpose=f"estate_intelligence_cancel:{job_id}", timeout=45)
    outcome = result.stdout_redacted.strip().splitlines()[-1] if result.stdout_redacted.strip() else "unknown"
    job["cancel_rpc"] = {"at": now(), "rc": result.rc, "receipt_id": result.receipt_id, "outcome": outcome, "reason": reason}
    if result.rc != 0 or outcome != "stopped":
        return save_job(job)
    job.update(status="cancelled", reason=reason, finished_at=now())
    _ledger(job, "converge", "terminate_budget", f"estate_intelligence_cancelled:{reason}"[:200], {"pid": pid})
    return save_job(job)


def fetch_detail(job_id):
    """Pull the per-table aggregate detail once, verified against the receipt digest; banked beside the job."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job or not job.get("receipt") or not (job["receipt"].get("result") or {}).get("detail_sha256"):
        return None
    path = _jobs_dir() / f"{job_id}.detail.json"
    if path.exists():
        return json.loads(path.read_text())
    result = execute_remote_command(job["host"], f"cat {shlex.quote(job['remote']['job_dir'] + '/detail.json')}",
                                    purpose=f"estate_intelligence_detail:{job_id}", timeout=120)
    if result.rc != 0:
        return None
    text = result.stdout_redacted
    if hashlib.sha256(text.encode()).hexdigest() != job["receipt"]["result"]["detail_sha256"]:
        raise ValueError("DETAIL_DIGEST_MISMATCH")
    path.write_text(text)
    return json.loads(text)
