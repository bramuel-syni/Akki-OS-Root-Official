"""Control plane for M9 governed training jobs on the admitted GPU hosts (akki-vm, akki-vm-ii).

Same seam as the language-cognition plane: reviewed worker code ships as a hashed bundle over the pinned
SSH connection, the job daemonises on the host and writes its own state/receipt on the host volume. E1 keeps
a secret-free job record, reads status by ONE bounded RPC, and on completion routes the measured MOAC card
through the existing admission ceremony, the optimizer-comparison harness (A17.5) and the recipe seat.
E1 is never a data path: corpora, weights and adapters stay on the tenant hosts.
"""
import base64
import hashlib
import io
import json
import os
import re
import shlex
import time
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from services.audio_plane_v1 import language_cognition_dispatch as lc
from services.census_autonomy import engine

ROOT = Path(__file__).resolve().parents[2]
WORKER = "services/training_runner/m9_worker.py"
PHASES = ("acquire_bases", "assemble", "calibrate", "compare_optimizers", "train", "pipeline", "serve", "load_test", "lab_inspect", "lab_measure", "lab_train_music", "lab_classify_estate", "lab_text_lid",
          "malpha_aip_build", "malpha_aip_requalify", "malpha_listener_train", "malpha_evaluate", "malpha_story_text_train", "malpha_voice_train", "malpha_baseline_render")
MALPHA_PHASES = {"malpha_aip_build": {'lab_corpus_root', 'max_files_per_language', 'cpu_workers', 'token_max_seconds', 'codec_sample_per_language', 'brand_lexicon'}, "malpha_aip_requalify": {'min_dev_segments', 'min_dev_mention_segments'},
                 "malpha_listener_train": {'recipe', 'brand_lexicon'}, "malpha_evaluate": {'artefact_path', 'artefact_sha256', 'brand_lexicon', 'admission_target', 'trained_job_id'},
                 "malpha_story_text_train": {'recipe', 'base_registration'}, "malpha_voice_train": {'recipe'}, "malpha_baseline_render": {'prompts_per_language'}}
MALPHA_COMMON = {'commission_id', 'languages', 'gpu_index', 'budget_mode', 'owner_order_ref', 'seed', 'iteration', 'aip_db_dir'}
OWNER_RULING_20260930 = "owner ruling 2026-09-30 (1a): per-stratum acceptance = Outcome floor AND no regression below the base; aggregate M-a global (Docs 17–19 · §26.2)"
JOB_ID = re.compile(r"m9j-[a-f0-9]{12}")
OWNER_ORDER_REF = "owner-order 2026-09-29: M9 autonomous to the end; recommended rules adopted (1c 2a 3a 4b 5a)"
BOOTSTRAP = '''import sys,json,base64,pathlib,hashlib,os
p=json.load(sys.stdin)
b=base64.b64decode(p.pop('bundle'))
if hashlib.sha256(b).hexdigest()!=p['code_sha256']: raise ValueError('CODE_HASH_MISMATCH')
d=pathlib.Path(p['job_dir']); d.mkdir(parents=True,exist_ok=True)
z=d/'worker.zip'; z.write_bytes(b)
pid=os.fork()
if pid>0:
    print(json.dumps({'job_id':p['job_id'],'pid':pid,'job_dir':str(d)}),flush=True); os._exit(0)
os.setsid(); sys.stdin.close()
out=open(d/'worker.log','ab',buffering=0); os.dup2(out.fileno(),1); os.dup2(out.fileno(),2)
os.environ['HF_HOME']=p['root']+'/hf_cache'; os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
sys.path.insert(0,str(z))
from services.training_runner.m9_worker import execute
execute(p)
'''


def hosts():
    return [h.strip() for h in os.environ["M9_TRAINING_HOSTS"].split(",") if h.strip()]


def _remote_root():
    return os.environ["M9_REMOTE_ROOT"]


def _remote_python():
    return os.environ["M9_REMOTE_PYTHON"]


def _jobs_dir():
    path = engine.CENSUS_STATE_DIR / "m9_training"
    path.mkdir(parents=True, exist_ok=True)
    return path


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_bundle():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(zipfile.ZipInfo(WORKER, date_time=(2026, 1, 1, 0, 0, 0)), (ROOT / WORKER).read_bytes())
        for module in ('services/training_lab/inspection_worker.py', 'services/training_lab/measurement_worker.py', 'services/training_lab/music_detector_worker.py', 'services/audio_plane_v1/acoustic_observables.py',
                       'services/training_lab/estate_language_worker.py', 'services/audio_plane_v1/corrective_model.py', 'services/training_lab/malpha_worker.py', 'services/training_lab/malpha_voice_worker.py'):
            archive.writestr(zipfile.ZipInfo(module, date_time=(2026, 1, 1, 0, 0, 0)), (ROOT / module).read_bytes())
        for directory in ("services", "services/training_runner", "services/training_lab", "services/audio_plane_v1"):
            archive.writestr(zipfile.ZipInfo(directory + "/__init__.py", date_time=(2026, 1, 1, 0, 0, 0)), b"")
    raw = buffer.getvalue()
    return base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest()


def save_job(job):
    path = _jobs_dir() / f"{job['job_id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(job, indent=1, default=str))
    os.replace(tmp, path)
    return job


def load_job(job_id):
    if not JOB_ID.fullmatch(job_id or ""):
        return None
    try:
        return json.loads((_jobs_dir() / f"{job_id}.json").read_text())
    except (OSError, ValueError):
        return None


def list_jobs():
    jobs = []
    for path in _jobs_dir().glob("m9j-*.json"):
        try:
            jobs.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return sorted(jobs, key=lambda j: j.get("submitted_at", ""), reverse=True)


def _ledger(job, stage, decision, reason, stamp_audit=None):
    lc._ledger(job, stage, decision, reason, stamp_audit)


def validate(phase, params, host):
    if phase not in PHASES:
        raise ValueError("Unknown M9 training phase.")
    if host not in hosts():
        raise ValueError("M9_HOST_NOT_ADMITTED:" + str(host))
    if phase == 'lab_inspect':
        if set(params) != {'lab_corpus_root','gpu_index','owner_order_ref'} or params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']:
            raise ValueError('LAB_INSPECTION_SCOPE_INVALID')
        if type(params['gpu_index']) is not int or params['gpu_index'] not in (0,1) or not params['owner_order_ref']:
            raise ValueError('LAB_INSPECTION_AUTHORITY_REQUIRED')
    if phase == 'lab_measure':
        if set(params) != {'lab_corpus_root', 'workers', 'max_seconds', 'max_files_per_language', 'owner_order_ref'} or params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']:
            raise ValueError('LAB_MEASUREMENT_SCOPE_INVALID')
        if type(params['workers']) is not int or not 1 <= params['workers'] <= 32 or type(params['max_files_per_language']) is not int or params['max_files_per_language'] < 0:
            raise ValueError('LAB_MEASUREMENT_BOUNDS_INVALID')
        if type(params['max_seconds']) not in (int, float) or not 60 <= params['max_seconds'] <= 7200 or not params['owner_order_ref']:
            raise ValueError('LAB_MEASUREMENT_AUTHORITY_REQUIRED')
    if phase == 'lab_classify_estate':
        required = {'lab_corpus_root', 'audio_model_dir', 'audio_model_sha256', 'music_model_path', 'music_model_sha256', 'compute_cap_gpu_hours', 'max_seconds_per_file', 'max_windows_per_file', 'batch_size', 'owner_order_ref'}
        if set(params) != required or params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'] or not str(params['audio_model_dir']).startswith(os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']) or not str(params['music_model_path']).startswith(os.environ['M9_REMOTE_ROOT']):
            raise ValueError('ESTATE_LANGUAGE_SCOPE_INVALID:' + ','.join(sorted(required ^ set(params))))
        if not 0 < float(params['compute_cap_gpu_hours']) <= 12 or not 60 <= float(params['max_seconds_per_file']) <= 7200 or type(params['max_windows_per_file']) is not int or not 1 <= params['max_windows_per_file'] <= 5000 or type(params['batch_size']) is not int or not 1 <= params['batch_size'] <= 1024 or not params['owner_order_ref']:
            raise ValueError('ESTATE_LANGUAGE_BOUNDS_INVALID')
    if phase == 'lab_text_lid':
        required = {'lab_corpus_root', 'port', 'chunk_chars', 'batch_size', 'compute_cap_gpu_hours', 'owner_order_ref'}
        optional = {'interleave', 'skip_refs'}  # continuation passes: read every language in turn, skip transcripts already read
        if not required <= set(params) <= required | optional or params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'] or type(params['port']) is not int or not 1024 <= params['port'] <= 65535:
            raise ValueError('TEXT_LID_SCOPE_INVALID:' + ','.join(sorted((required | optional) ^ set(params))))
        if type(params['chunk_chars']) is not int or not 200 <= params['chunk_chars'] <= 8000 or type(params['batch_size']) is not int or not 1 <= params['batch_size'] <= 256 or not 0 < float(params['compute_cap_gpu_hours']) <= 12 or not params['owner_order_ref']:
            raise ValueError('TEXT_LID_BOUNDS_INVALID')
        if type(params.get('interleave', False)) is not bool or not isinstance(params.get('skip_refs', []), list) or not all(isinstance(r, str) and len(r) == 16 for r in params.get('skip_refs', [])):
            raise ValueError('TEXT_LID_BOUNDS_INVALID')
    if phase == 'lab_train_music':
        required = {'lab_corpus_root', 'refs_dir', 'measurement_job_dir', 'labelled_manifest', 'baseline', 'smoke', 'gpu_index', 'seed', 'epochs', 'folds', 'batch_size', 'lr',
                    'max_seconds_per_file', 'max_windows_per_file', 'weak_negatives_per_language', 'weak_positive_files', 'owner_order_ref'}
        if set(params) != required or params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'] or not str(params['refs_dir']).startswith(os.environ['M9_REMOTE_ROOT']):
            raise ValueError('MUSIC_DETECTOR_SCOPE_INVALID:' + ','.join(sorted(required ^ set(params))))
        if type(params['gpu_index']) is not int or params['gpu_index'] not in (0, 1) or not params['owner_order_ref'] or not isinstance(params['labelled_manifest'], list) or len(params['labelled_manifest']) < 4:
            raise ValueError('MUSIC_DETECTOR_AUTHORITY_OR_LABELS_REQUIRED')
        for key in ('seed', 'epochs', 'folds', 'batch_size', 'max_windows_per_file', 'weak_negatives_per_language', 'weak_positive_files'):
            if type(params[key]) is not int or params[key] < 0 or (key in ('epochs', 'folds', 'batch_size', 'max_windows_per_file') and params[key] < 1):
                raise ValueError('MUSIC_DETECTOR_BOUNDS_INVALID:' + key)
        if params['epochs'] > 100 or params['folds'] > 10 or not 0 < float(params['lr']) < 1 or not 10 <= float(params['max_seconds_per_file']) <= 3600:
            raise ValueError('MUSIC_DETECTOR_BOUNDS_INVALID:recipe')
    if phase in MALPHA_PHASES:
        required = MALPHA_COMMON | MALPHA_PHASES[phase]; optional = {'resume_from'}
        if not required <= set(params) <= required | optional:
            raise ValueError('MALPHA_SCOPE_INVALID:' + ','.join(sorted((required | optional) ^ set(params))))
        if params['budget_mode'] != 'uncapped_until_billing' or not params['owner_order_ref'] or not isinstance(params['languages'], list) or not set(params['languages']) <= {'kik', 'kam', 'swa'} or not params['languages']:
            raise ValueError('MALPHA_AUTHORITY_INVALID')
        if type(params['gpu_index']) is not int or params['gpu_index'] not in (0, 1) or type(params['iteration']) is not int or params['iteration'] < 0 or not str(params['aip_db_dir']).startswith(os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']):
            raise ValueError('MALPHA_BOUNDS_INVALID')
        if 'recipe' in params and (not isinstance(params['recipe'], dict) or not params['recipe'] or 'max_steps' in params['recipe'] and not 1 <= int(params['recipe']['max_steps']) <= 2_000_000):
            raise ValueError('MALPHA_RECIPE_INVALID')
        if phase == 'malpha_aip_build' and params['lab_corpus_root'] != os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']:
            raise ValueError('MALPHA_CORPUS_SCOPE_INVALID')
        if phase == 'malpha_evaluate' and (not re.fullmatch(r'[a-f0-9]{64}', str(params['artefact_sha256'])) or not str(params['artefact_path']).startswith(os.environ['M9_REMOTE_ROOT'])):
            raise ValueError('MALPHA_ARTEFACT_INVALID')
    if phase in ("calibrate", "compare_optimizers", "train", "pipeline", "serve"):
        if type(params.get("gpu_index")) is not int or params["gpu_index"] not in (0, 1):
            raise ValueError("M9_GPU_INDEX_REQUIRED")
    if phase == "train" and not isinstance(params.get("acceptance_floor"), (int, float)):
        raise ValueError("OUTCOME_PER_STRATUM_FLOOR_REQUIRED")  # Docs 17–19: no training without the Outcome's per-stratum acceptance threshold
    if phase == "serve" and not all(params.get(k) for k in ("run_dir", "artefact_sha256", "labels", "port", "authority")):
        raise ValueError("M9_SERVE_REQUIRES_run_dir_artefact_sha256_labels_port_authority")
    if phase == "load_test" and not all(params.get(k) for k in ("port", "corpus_id")):
        raise ValueError("M9_LOAD_TEST_REQUIRES_port_corpus_id")
    if phase == "acquire_bases" and not params.get("bases"):
        raise ValueError("M9_BASES_REQUIRED")
    if phase == "assemble" and not all(params.get(k) for k in ("corpus_id", "kind", "rights_ref")):
        raise ValueError("M9_ASSEMBLE_REQUIRES_corpus_id_kind_rights_ref")
    if phase == "pipeline" and not all(k in params for k in ("assemble", "calibrate", "compare", "train")):
        raise ValueError("M9_PIPELINE_REQUIRES_assemble_calibrate_compare_train")
    for key in ("recipe",):
        if key in params and params[key].get("dp"):
            raise ValueError("DP_SGD_ARM_NOT_COMMISSIONED_IN_TEXT_WORKER")


def submit(phase, params, host, principal_id, lawful_ref, timeout=60):
    """Admit through Northena, ship the worker, daemonise the phase on the named GPU host."""
    validate(phase, params or {}, host)
    from services.census_autonomy.remote_dispatch import _connect
    job_id = "m9j-" + uuid.uuid4().hex[:12]
    job = {"job_id": job_id, "phase": phase, "host": host, "principal_id": principal_id, "submitted_at": now(), "params": dict(params or {}),
           "northena_run_id": f"run-{uuid.uuid4().hex[:12]}", "northena_trace_id": f"trc-{uuid.uuid4().hex[:12]}",
           "governing_artifact_ref": {"artifact_type": "objective_request", "artifact_id": "M9-GOVERNED-TRAINING", "version": job_id},
           "lawful_basis_ref": str(lawful_ref), "owner_order_ref": OWNER_ORDER_REF,
           "remote": {"root": _remote_root(), "job_dir": f"{_remote_root()}/jobs/{job_id}"}, "status": "submitting"}
    _ledger(job, "admit", "admitted", f"m9_{phase}_admitted", {"host": host})
    bundle, code_hash = build_bundle()
    control = {"bundle": bundle, "code_sha256": code_hash, "job_id": job_id, "phase": phase, "runtime_id": host,
               "hostname_expected": os.environ[f"{host.upper().replace('-', '_')}_HOSTNAME_EXPECTED"],
               "root": job["remote"]["root"], "job_dir": job["remote"]["job_dir"], **(params or {})}
    client = None
    try:
        client, _config = _connect(host, min(20, timeout))
        channel = client.get_transport().open_session(timeout=15)
        channel.settimeout(timeout)
        channel.exec_command(shlex.quote(_remote_python()) + " -c " + shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(control).encode()); channel.shutdown_write()
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
                channel.close(); raise TimeoutError("SUBMIT_TIMEOUT")
            time.sleep(0.05)
        code = channel.recv_exit_status()
        if code != 0:
            raise ValueError("REMOTE_BOOTSTRAP_FAILED:" + diagnostic.decode(errors="replace")[-400:])
        ack = json.loads(output.decode())
        job.update(status="running", code_sha256=code_hash, remote={**job["remote"], "pid": ack["pid"]}, started_at=now())
        _ledger(job, "gate", "warm", f"m9_{phase}_daemonised:pid={ack['pid']}")
    except Exception as exc:
        job.update(status="refused", reason=f"{type(exc).__name__}: {str(exc)[:300]}")
        _ledger(job, "gate", "refused", f"m9_{phase}_dispatch_failed:{type(exc).__name__}")
    finally:
        if client is not None:
            client.close()
    return save_job(job)


def fetch_artifact(job_id, name, max_bytes=12_000_000):
    """One bounded RPC for a named result file written by the worker into its job directory."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job or not re.fullmatch(r"[a-z_]+\.json", name):
        raise ValueError("ARTIFACT_FETCH_REQUIRES_A_KNOWN_JOB_AND_JSON_NAME")
    result = execute_remote_command(job["host"], f"head -c {int(max_bytes)} {shlex.quote(job['remote']['job_dir'] + '/' + name)}", purpose=f"m9_fetch:{job_id}:{name[:-5]}", timeout=180)
    if result.rc != 0:
        raise ValueError("ARTIFACT_FETCH_FAILED:" + result.stderr_redacted[:200])
    return result.stdout_redacted


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
    result = execute_remote_command(job["host"], command, purpose=f"m9_cancel:{job_id}", timeout=45)
    outcome = result.stdout_redacted.strip().splitlines()[-1] if result.stdout_redacted.strip() else "unknown"
    job["cancel_rpc"] = {"at": now(), "rc": result.rc, "receipt_id": result.receipt_id, "outcome": outcome, "reason": reason}
    if result.rc != 0 or outcome != "stopped":
        job["cancel_rpc"]["error"] = result.stderr_redacted[:300]
        return save_job(job)
    job.update(status="cancelled", reason=reason, finished_at=now())
    _ledger(job, "converge", "terminate_budget", f"m9_{job['phase']}_cancelled:{reason}"[:200], {"pid": pid, "cancel_receipt_id": result.receipt_id})
    return save_job(job)


def interrupt(job_id, reason, observed_step=None):
    """Physical process loss for the M8-T1 / M9-T3 drill: SIGKILL only — no graceful stop, no in-process hook. The job is recorded as
    `interrupted` with the last step E1 observed on the host; continuation is only possible from the checkpoint on the host volume."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = refresh(job_id)
    if not job or job["status"] != "running":
        return job
    pid = int(job["remote"].get("pid") or 0)
    if pid <= 0:
        raise ValueError("INTERRUPT_REQUIRES_A_KNOWN_WORKER_PID")
    state_path = shlex.quote(job["remote"]["job_dir"] + "/state.json")
    command = f"kill -KILL {pid} 2>/dev/null; sleep 0.5; kill -0 {pid} 2>/dev/null && echo still_alive || echo killed; echo __STATE__; cat {state_path} 2>/dev/null"
    result = execute_remote_command(job["host"], command, purpose=f"m9_interrupt:{job_id}", timeout=45)
    verdict, _, state_text = result.stdout_redacted.partition("__STATE__")
    try:
        host_state = json.loads(state_text.strip()) if state_text.strip() else None
    except ValueError:
        host_state = None
    progress = (host_state or {}).get("progress") or {}
    job["interrupt_rpc"] = {"at": now(), "rc": result.rc, "receipt_id": result.receipt_id, "outcome": verdict.strip().splitlines()[-1] if verdict.strip() else "unknown", "reason": reason,
                            "signal": "SIGKILL", "observed_step_at_kill": progress.get("step"), "observation_granularity_steps": 10,
                            "last_checkpoint_step_on_host": progress.get("last_checkpoint_step"), "next_checkpoint_step_on_host": progress.get("next_checkpoint_step")}
    if result.rc != 0 or job["interrupt_rpc"]["outcome"] != "killed":
        job["interrupt_rpc"]["error"] = result.stderr_redacted[:300]
        return save_job(job)
    job.update(status="interrupted", reason=reason, finished_at=now(), remote_state=host_state)
    _ledger(job, "converge", "terminate_budget", f"m9_{job['phase']}_interrupted_sigkill:{reason}"[:200], {"pid": pid, "interrupt_receipt_id": result.receipt_id, "observed_step": progress.get("step")})
    return save_job(job)


def refresh(job_id):
    """One bounded status RPC: host state + receipt (digest-verified) + log tail + liveness."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job:
        return None
    if job["status"] in ("completed", "failed", "refused", "cancelled", "interrupted"):
        return job
    job_dir = job["remote"]["job_dir"]
    command = (f"cat {shlex.quote(job_dir + '/state.json')} 2>/dev/null; echo; echo __RECEIPT__; cat {shlex.quote(job_dir + '/receipt.json')} 2>/dev/null; "
               f"echo; echo __LOG__; tail -c 1500 {shlex.quote(job_dir + '/worker.log')} 2>/dev/null; echo; echo __ALIVE__; "
               f"kill -0 {int(job['remote'].get('pid') or 0)} 2>/dev/null && echo yes || echo no")
    result = execute_remote_command(job["host"], command, purpose=f"m9_status:{job_id}", timeout=90)
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
    job["worker_log_tail"] = log_text.strip()[-1500:]
    job["process_alive"] = alive.strip() == "yes"
    stages = ((job.get("remote_state") or {}).get("stages") or {})
    if "assemble" in stages and "test_set_seal_banked_at" not in job:
        job["test_set_seal_banked_at"] = now()  # sealed test set observed on the host before any training stage completed
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
            if not receipt["digest_verified"] or receipt.get("job_id") != job_id or receipt.get("phase") != job["phase"]:
                job.update(status="failed", reason="WORKER_RECEIPT_INTEGRITY_FAILED", finished_at=now())
                _close(job)
                return save_job(job)
            job["status"] = receipt.get("status", "failed")
            job["finished_at"] = receipt.get("finished_at")
            if job["status"] == "failed":
                job["reason"] = ((receipt.get("error") or {}).get("type") or "worker_failed") + ": " + str((receipt.get("error") or {}).get("message") or "")[:200]
            _close(job)
    elif not job["process_alive"]:
        job["status"] = "failed"
        job["reason"] = "worker process gone without a terminal receipt; retained progress is not completion"
        _close(job)
    return save_job(job)


def _close(job):
    status = "completed" if job["status"] == "completed" else "failed"
    receipt = lc._sealed("services.census_autonomy.track_4_autonomy_wiring_v1").emit_autonomy_engine_run_receipt(
        job_kind="training_runs", run_id=job["job_id"], started_at_utc=job.get("started_at") or job["submitted_at"],
        finished_at_utc=job.get("finished_at") or now(), status=status, provenance_ref=f"m9_training://run_log/{job['job_id']}")
    job["track4_run_receipt"] = receipt.__dict__
    if status == "completed":
        result = job["receipt"]["result"]
        if job["phase"] == "acquire_bases":
            job["base_registration"] = _bank_base_registration(job, result)
        if job["phase"] in ("compare_optimizers", "pipeline"):
            comparison = result["stages"]["compare"] if job["phase"] == "pipeline" else result
            job["optimizer_comparison"] = _bank_optimizer_comparison(job, comparison)
        if job["phase"] in ("train", "pipeline"):
            run = result["stages"]["train"] if job["phase"] == "pipeline" else result
            job["run_certificate"] = _bank_run_certificate(job, run, (result.get("stages") or {}).get("calibrate"))
        if job["phase"] == "serve":
            job["serving_summary"] = result
        if job["phase"] == "load_test":
            job["load_test"] = result
    _ledger(job, "converge", "terminate_success" if status == "completed" else "terminate_budget", f"m9_{job['phase']}_{status}",
            {"receipt_sha256": (job.get("receipt") or {}).get("receipt_sha256")})


def _bank_base_registration(job, result):
    """Doc 20 A20.1/A20.13: licence-verified at registration, weight sha pinned at acquisition, host custody only."""
    banked = {rid: {**row, "host_path": f"{job['host']}://{row['local_path']}", "banked_at": now()} for rid, row in result.items()}
    path = _jobs_dir() / "base_registration.json"
    existing = json.loads(path.read_text()) if path.exists() else {}
    existing.update(banked)
    path.write_text(json.dumps(existing, indent=1))
    return banked


def _bank_optimizer_comparison(job, comparison):
    """A17.5 harness rows from the measured arms; the verdict applies the owner-authorised recommended rule."""
    from contracts.optimizer_comparison_v0 import ArmMeasurements
    from services.training import optimizer_harness as harness
    comparison_id = f"m9-{job['job_id']}"
    arms = comparison["arms"]
    try:
        harness.open_comparison(comparison_id=comparison_id, base_model_id=comparison["base"], evaluation_sets=[f"{comparison['corpus_id']}:held", f"{comparison['corpus_id']}:non_target"],
                                budget_cap_wallclock_seconds=max(1, max(a["wallclock_seconds_to_convergence"] for a in arms.values())),
                                budget_cap_gpu_hours=max(a["gpu_hours_to_convergence"] for a in arms.values()),
                                smallest_stratum=f"{comparison['corpus_id']}@{comparison['comparison_fraction']}", opened_at=now())
        for arm in ("baseline", "muon"):
            a = arms[arm]
            harness.record_arm_measurements(comparison_id, arm, ArmMeasurements(
                moac_m_a_improvement=a["moac_m_a_improvement"], moac_m_b_regression=a["moac_m_b_regression"],
                wallclock_seconds_to_convergence=int(a["wallclock_seconds_to_convergence"]), gpu_hours_to_convergence=float(a["gpu_hours_to_convergence"]),
                moac_m_e_calibration=float(a["moac_m_e_calibration"]), evaluation_samples_uncurated=True))
        current = harness.get_by_id(comparison_id)
        if current.verdict == "ineligible":
            ruled = current
        else:
            ruled = harness.rule_on_comparison(comparison_id, comparison["recommended_verdict"], now(),
                                               verdict_note=f"{OWNER_ORDER_REF} · rule: {comparison['recommendation_rule']}")
        return {"comparison_id": comparison_id, "verdict": ruled.verdict, "verdict_note": ruled.verdict_note, "quality_parity": comparison["quality_parity"],
                "arms": {k: {kk: v[kk] for kk in ("moac_m_a_improvement", "moac_m_b_regression", "wallclock_seconds_to_convergence", "gpu_hours_to_convergence", "moac_m_e_calibration")} for k, v in arms.items()}}
    except Exception as exc:  # the harness refusal is recorded, never hidden
        return {"comparison_id": comparison_id, "error": f"{type(exc).__name__}: {str(exc)[:300]}"}


def adapter_registry_entry(job, run, model_id, artefact_sha, adapter_dir, ruling_ref):
    """Registry entry for a trained adapter: A17.3 recipe_version, artefact hash, host custody path, corpus lineage — read from the registry, never from whoever ran the job."""
    recipe = run["training"]["recipe"]
    return {"provider": "trained_on_this_estate", "custody_kind": "estate_trained", "role": "trained_adapter",
            "recipe_version": "recipe-sha256:" + hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest(), "recipe": recipe,
            "base": run["training"]["base"], "artefact_sha256": artefact_sha, "host": job["host"], "adapter_path": f"{job['host']}://{adapter_dir}", "run_dir": run.get("run_dir") or str(Path(run["artefact"]["path"]).parent),
            "training_manifest_sha256": run["artefact"]["training_manifest_sha256"], "corpus_id": run["corpus_id"], "corpus_manifest_sha256": run["manifest_sha256"],
            "cited_units": run["artefact"]["cited_units"], "task": run["task"], "labels": run["labels"], "training_job_id": job["job_id"], "variant": "pruned" if model_id.endswith("-pruned") else "full",
            "excluded_unit_ids": (run.get("training_manifest") or {}).get("excluded_unit_ids") or [], "rederived_from": run.get("rederived_from"), "owner_ruling_ref": ruling_ref, "status": "admitted", "serving": None, "recall": None}


def _bank_run_certificate(job, run, calibration=None):
    """Completion certificate (Doc 17 §17.4 machine-facing): compute, data touched, manifest hash, per-stratum results,
    DAP-31 egress verdict, DAP-37 pruned artefact, and the admission ceremony outcome — admitted OR refused on record."""
    from services.model_admission import ceremony
    moac = run["moac"]
    egress = run["distance_probe"]["egress_permitted"]
    admission = {"attempted": False, "reason": "DAP-31 egress refused: " + "; ".join(run["distance_probe"]["refusals"])} if not egress else None
    pruned = None
    if run.get("drill"):
        admission = {"attempted": False, "reason": "interruption/resume drill run — not a candidate model; no admission attempted"}
        pruned = {"outcome": "not_attempted", "reason": "drill run"}
    elif egress:
        try:
            outcome = ceremony.run_admission(moac["card"], adapter_registry_entry(job, run, job["job_id"], run["artefact"]["sha256"], run["artefact"]["path"], OWNER_RULING_20260930))
            admission = {"attempted": True, "outcome": outcome.outcome, "reason": outcome.reason, "refusal_note": outcome.refusal_note, "registry_version_after": outcome.registry_version_after, "record_ref": outcome.record_ref}
        except Exception as exc:
            admission = {"attempted": True, "outcome": "error", "reason": f"{type(exc).__name__}: {str(exc)[:300]}"}
        try:
            outcome = ceremony.run_admission(run["pruning"]["moac_card"], adapter_registry_entry(job, run, job["job_id"] + "-pruned", run["pruning"]["artefact_sha256"], str(Path(run["artefact"]["path"]).parent / "pruned_adapter"), OWNER_RULING_20260930))
            pruned = {"outcome": outcome.outcome, "reason": outcome.reason, "registry_version_after": outcome.registry_version_after, "record_ref": outcome.record_ref}
        except Exception as exc:
            pruned = {"outcome": "error", "reason": f"{type(exc).__name__}: {str(exc)[:300]}"}
    whitepaper = _draft_whitepaper(job, run, admission)
    held = run["adapter_eval"]["held"]["per_stratum"]
    certificate = {"job_id": job["job_id"], "host": job["host"], "receipt_sha256": job["receipt"]["receipt_sha256"], "corpus": run["corpus"],
                   "manifest_sha256": run["manifest_sha256"], "training_manifest_sha256": run["artefact"]["training_manifest_sha256"],
                   "test_set_seal": run["corpus"]["test_set_seal"], "test_set_seal_banked_at": job.get("test_set_seal_banked_at"),
                   "compute": run["training"], "artefact_sha256": run["artefact"]["sha256"], "cited_units": run["artefact"]["cited_units"],
                   "per_stratum": {s: {"accuracy": r["accuracy"], "base_accuracy": run["base_eval"]["held"]["per_stratum"][s]["accuracy"], "perplexity": r["perplexity"],
                                       "base_perplexity": run["base_eval"]["held"]["per_stratum"][s]["perplexity"], "abstention_rate": r.get("abstention_rate"), "units": r["units"],
                                       "meets_m_a": moac["per_stratum_pass"].get(s)} for s, r in held.items()},
                   "moac": {"m_a_improvement": moac["m_a_improvement"], "m_b_non_target_regression": moac["m_b_non_target_regression"], "m_e_calibration_ece": moac["m_e_calibration_ece"],
                            "floors_class": moac["floors_class"], "card": moac["card"]},
                   "distance_probe": run["distance_probe"], "checkpoint": run["checkpoint"],
                   "pruned_artefact": {k: run["pruning"][k] for k in ("sparsity", "artefact_sha256", "m_a_improvement", "m_b_non_target_regression")} | {"admission": pruned},
                   "admission": admission, "whitepaper": whitepaper, "calibration": {k: calibration[k] for k in ("base_selected_by_calibration", "quotes", "proposed_milestones")} if calibration else None,
                   "optimizer_comparison": job.get("optimizer_comparison"), "dp_sgd": run["artefact"]["dp_sgd"],
                   "final_model": False, "serving": "not served; admission record only (M9.4 serving is a separate step)", "certified_at": now(),
                   "run_dir": run.get("run_dir"), "resume_from_job_id": run.get("resume_from_job_id"), "drill": bool(run.get("drill")),
                   "outcome_floor": moac.get("outcome_floor"), "excluded_unit_ids": (job.get("params") or {}).get("excluded_unit_ids") or [], "rederived_from": (job.get("params") or {}).get("rederived_from")}
    (_jobs_dir() / f"run_certificate_{job['job_id']}.json").write_text(json.dumps(certificate, indent=1, default=str))
    return certificate


def _draft_whitepaper(job, run, admission):
    """Doc 14 §33: the whitepaper cites an on-record admission and baseline line; refusals are recorded verbatim."""
    try:
        from contracts.baseline_line import BaselineLine_v0
        from services.whitepapers import draft as _wp
        safe = job["job_id"].replace("-", "_")
        baseline_dir = Path(os.environ.get("BASELINE_LINES_DIR", "/app/assessment_workspace/phase0/baseline_lines"))
        baseline_dir.mkdir(parents=True, exist_ok=True)
        baseline_id = f"bl_{safe}"
        target = baseline_dir / f"{baseline_id}.json"
        if not target.exists():
            base = run["training"]["base"]
            line = BaselineLine_v0(baseline_line_id=baseline_id, training_run_id=job["job_id"], starting_model_id=base["registry_id"],
                                   starting_model_license_note=f"licence verified at acquisition; weight sha {base['weight_sha256'][:16]}… pinned on the host registration",
                                   authored_at=now(), authored_by="m9_dispatch._bank_run_certificate")
            target.write_text(json.dumps(line.model_dump(), indent=2, ensure_ascii=False))
        if not admission or not admission.get("attempted"):
            return {"drafted": False, "reason": "no admission record to cite (egress refused)"}
        wp = _wp.draft_whitepaper({"whitepaper_id": f"wp_{safe.lower()}", "run_ref": job["job_id"], "drafted_at": now(), "drafted_by": "m9_dispatch",
                                   "cites_model_admission_id": job["job_id"], "cites_baseline_line_id": baseline_id,
                                   "summary_note": (f"M9 governed run {job['job_id']} on corpus {run['corpus_id']}: MOAC M-a {run['moac']['m_a_improvement']:+.4f}, "
                                                    f"M-b {run['moac']['m_b_non_target_regression']:+.4f}, egress {'permitted' if run['distance_probe']['egress_permitted'] else 'refused'}, "
                                                    f"admission {admission.get('outcome')}."), "retention_class": "standard"})
        wp_id = getattr(wp, "whitepaper_id", None) or (wp.get("whitepaper_id") if isinstance(wp, dict) else None)
        return {"drafted": True, "whitepaper_id": wp_id}
    except Exception as exc:
        return {"drafted": False, "reason": f"{type(exc).__name__}: {str(exc)[:300]}"}
