"""Control plane for the language-cognition training run on the admitted GPU host.

E1 wires and steps back: reviewed worker code is shipped over the pinned SSH seam,
credentials cross only on stdin, the job daemonises on akki-vm-ii and writes its own
state/receipt on the host volume. E1 keeps a secret-free job record, reads status by
one bounded RPC (Northena coordinator discipline: never an in-process polling loop),
and banks Northena admit/converge rows + the Track-4 autonomy run receipt.
"""
import asyncio
import base64
import hashlib
import importlib
import io
import json
import os
import shlex
import sys
import threading
import time
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.census_autonomy import engine
from services.northena.ledger import record as ledger_record

ROOT = Path(__file__).resolve().parents[2]
WORKER = "services/audio_plane_v1/language_cognition_worker.py"
PHASES = ("corpus_census", "register_bases", "speaker_linkage", "gate_eval", "train_baseline", "train_corrective")
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
os.environ['HF_HOME']=p['root']+'/hf'; os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
sys.path.insert(0,str(z))
from services.audio_plane_v1.language_cognition_worker import execute
execute(p)
'''
_LOOP = None


def _host():
    return os.environ["LANGUAGE_COGNITION_HOST"]


def _remote_root():
    return os.environ["LANGUAGE_COGNITION_REMOTE_ROOT"]


def _remote_python():
    return _remote_root() + "/venv/bin/python"


def _jobs_dir():
    path = engine.CENSUS_STATE_DIR / "language_cognition"
    path.mkdir(parents=True, exist_ok=True)
    return path


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _loop():
    global _LOOP
    from core import client
    bound = getattr(client, "_io_loop", None)
    if bound is not None and bound.is_running():
        return bound
    if _LOOP is None:
        _LOOP = asyncio.new_event_loop()
        threading.Thread(target=_LOOP.run_forever, name="language-cognition-loop", daemon=True).start()
    return _LOOP


def _ledger(job, stage, decision, reason, stamp_audit=None):
    row = LedgerRow.new(run_id=job["northena_run_id"], trace_id=job["northena_trace_id"], stage=stage, decision=decision,
                        reason=reason, artifact_ref=LedgerArtifactRef(**job["governing_artifact_ref"]),
                        lawful_basis_ref=job["lawful_basis_ref"], stamp_audit=stamp_audit)
    asyncio.run_coroutine_threadsafe(ledger_record(row), _loop()).result(timeout=120)
    job.setdefault("ledger_rows", []).append({"row_id": row.row_id, "stage": stage, "decision": decision, "reason": reason})


def build_bundle(phase=None):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(zipfile.ZipInfo(WORKER, date_time=(2026, 1, 1, 0, 0, 0)), (ROOT / WORKER).read_bytes())
        if phase == 'train_corrective':
            for name in ('corrective_data', 'corrective_model', 'corrective_training'):
                path = f'services/audio_plane_v1/{name}.py'
                archive.writestr(zipfile.ZipInfo(path, date_time=(2026, 1, 1, 0, 0, 0)), (ROOT / path).read_bytes())
        for directory in ("services", "services/audio_plane_v1"):
            archive.writestr(zipfile.ZipInfo(directory + "/__init__.py", date_time=(2026, 1, 1, 0, 0, 0)), b"")
    raw = buffer.getvalue()
    return base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest()


def _obs_connector():
    access = json.loads(Path(os.environ["AKKI_CENSUS_JUMP_CONFIG"]).read_text())
    return dict(access["obs"])


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
    for path in _jobs_dir().glob("lcj-*.json"):
        try:
            jobs.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return sorted(jobs, key=lambda j: j.get("submitted_at", ""), reverse=True)


def _governing_ref(job_id):
    return {"artifact_type": "objective_request", "artifact_id": "CP-AIP-LANGUAGE-COGNITION", "version": job_id}


def _sealed(name):
    """The CP-AIP audio-plane / Track-4 family is authored under the vendored `backend.` package root."""
    root = str(ROOT.parent)
    if root not in sys.path:
        sys.path.append(root)
    return importlib.import_module("backend." + name)


def _sealed_language_cognition():
    return _sealed("services.audio_plane_v1.language_cognition_v1")


def submit(phase, params, principal_id, lawful_ref, timeout=60):
    """Admit through Northena, ship the worker, daemonise the phase on the GPU host."""
    if phase not in PHASES:
        raise ValueError("Unknown language-cognition phase.")
    if phase == 'train_corrective':
        from services.audio_plane_v1.corrective_training import validate
        validate(params)
    from services.census_autonomy.remote_dispatch import _connect
    sealed = _sealed_language_cognition()
    job_id = "lcj-" + uuid.uuid4().hex[:12]
    host = _host()
    job = {"job_id": job_id, "phase": phase, "host": host, "principal_id": principal_id, "submitted_at": now(),
           "params": {k: v for k, v in (params or {}).items() if k not in ("connector",)},
           "northena_run_id": f"run-{uuid.uuid4().hex[:12]}", "northena_trace_id": f"trc-{uuid.uuid4().hex[:12]}",
           "governing_artifact_ref": _governing_ref(job_id), "lawful_basis_ref": str(lawful_ref),
           "remote": {"root": _remote_root(), "job_dir": f"{_remote_root()}/jobs/{job_id}"}, "status": "submitting"}
    if phase in ("train_baseline", "train_corrective"):
        # The FINAL model's commission is refused by design until labelled code-switched spans exist;
        # this run is the measured compute receipt for the commissioned job, never the final artefact.
        try:
            sealed.commission_language_cognition_training_run(
                has_code_switched_material=bool(params.get("has_code_switched_material", False)),
                speaker_disjoint_split_ref=f"{host}://{job['remote']['root']}/split/session-disjoint",
                base_registration_ref=f"{host}://{job['remote']['root']}/base_registration.json",
                moac_contract_ref="LANGUAGE_COGNITION_MOAC_CONTRACT_DEFAULT",
                corpus_assembly_ref=f"{host}://{job['remote']['root']}/corpus_manifest.json")
            job["final_model_commission"] = {"decision": "admitted"}
        except sealed.CleanMonolingualOnlyRefused as exc:
            job["final_model_commission"] = {"decision": "refused", "reason": "CleanMonolingualOnlyRefused", "message": str(exc)[:300]}
    _ledger(job, "admit", "admitted", f"language_cognition_{phase}_admitted",
            {"host": host, "final_model_commission": job.get("final_model_commission")})
    bundle, code_hash = build_bundle(phase)
    control = {"bundle": bundle, "code_sha256": code_hash, "job_id": job_id, "phase": phase, "runtime_id": host,
               "hostname_expected": os.environ[f"{host.upper().replace('-', '_')}_HOSTNAME_EXPECTED"],
               "root": job["remote"]["root"], "job_dir": job["remote"]["job_dir"], **(params or {})}
    if phase == "corpus_census":
        control["connector"] = _obs_connector()
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
        _ledger(job, "gate", "warm", f"language_cognition_{phase}_daemonised:pid={ack['pid']}")
    except Exception as exc:
        job.update(status="refused", reason=f"{type(exc).__name__}: {str(exc)[:300]}")
        _ledger(job, "gate", "refused", f"language_cognition_{phase}_dispatch_failed:{type(exc).__name__}")
    finally:
        if client is not None:
            client.close()
    return save_job(job)


def refresh(job_id):
    """One bounded status RPC: read the host-side state and receipt (verified by digest)."""
    from services.training_runner.ssh_seam import execute_remote_command
    job = load_job(job_id)
    if not job:
        return None
    if job["status"] in ("completed", "failed", "refused"):
        return job
    job_dir = job["remote"]["job_dir"]
    command = (f"cat {shlex.quote(job_dir + '/state.json')} 2>/dev/null; echo; echo __RECEIPT__; "
               f"cat {shlex.quote(job_dir + '/receipt.json')} 2>/dev/null; echo; echo __LOG__; tail -c 1500 {shlex.quote(job_dir + '/worker.log')} 2>/dev/null; "
               f"echo; echo __ALIVE__; kill -0 {int(job['remote'].get('pid') or 0)} 2>/dev/null && echo yes || echo no")
    result = execute_remote_command(job["host"], command, purpose=f"language_cognition_status:{job_id}", timeout=45)
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
            if not receipt['digest_verified'] or receipt.get('job_id') != job_id or receipt.get('phase') != job['phase']:
                job.update(status='failed', reason='WORKER_RECEIPT_INTEGRITY_FAILED', finished_at=now())
                _close(job)
                return save_job(job)
            job["status"] = receipt.get("status", "failed")
            job["finished_at"] = receipt.get("finished_at")
            _close(job)
    elif not job["process_alive"]:
        job["status"] = "failed"
        job["reason"] = "worker process gone without a terminal receipt; retained progress is not completion"
        _close(job)
    return save_job(job)


def _close(job):
    status = "completed" if job["status"] == "completed" else "failed"
    receipt = _sealed("services.census_autonomy.track_4_autonomy_wiring_v1").emit_autonomy_engine_run_receipt(
        job_kind="training_runs", run_id=job["job_id"], started_at_utc=job.get("started_at") or job["submitted_at"],
        finished_at_utc=job.get("finished_at") or now(), status=status,
        provenance_ref=f"census_autonomy_service://run_log/{job['job_id']}")
    job["track4_run_receipt"] = receipt.__dict__
    if job["phase"] == "register_bases" and status == "completed":
        job["training_base_registration"] = _bank_base_registration(job["receipt"]["result"])
    if job["phase"] in ("train_baseline", "train_corrective") and status == "completed":
        job["run_certificate"] = _bank_run_certificate(job)
    _ledger(job, "converge", "terminate_success" if status == "completed" else "terminate_budget",
            f"language_cognition_{job['phase']}_{status}", {"receipt_sha256": (job.get("receipt") or {}).get("receipt_sha256")})


def _bank_run_certificate(job):
    """AIP §11.6 completion certificate: compute consumed, data touched, manifest hash, per-stratum results —
    read against the SEALED defaults (span rule, presenter minimum, MOAC) so nothing is silently re-thresholded."""
    sealed = _sealed_language_cognition()
    result = job["receipt"]["result"]
    span, split, moac = sealed.WINDOW_AND_SPAN_RULE_DEFAULT, sealed.SPEAKER_DISJOINT_SPLIT_CONTRACT_DEFAULT, sealed.LANGUAGE_COGNITION_MOAC_CONTRACT_DEFAULT
    rule = result["span_rule"]
    held = result["held_out"]["per_language"]
    certificate = {
        "job_id": job["job_id"], "host": job["host"], "receipt_sha256": job["receipt"]["receipt_sha256"],
        "compute": result["training"], "artefact_sha256": result["artefact"]["sha256"],
        "training_manifest_sha256": result["artefact"]["training_manifest_sha256"], "data_touched": result["split"],
        "per_stratum": {code: {"accuracy": row["accuracy"], "abstention_rate": row["abstention_rate"], "windows": row["windows"],
                               "meets_default": row["accuracy"] is not None and row["accuracy"] >= moac.per_language_accuracy_default}
                        for code, row in held.items() if row["windows"]},
        "archive_test": result.get("archive_test"),
        "dp_sgd": result.get('dp_sgd'), "recipe_sha256": result.get('recipe_sha256'),
        "checkpoint": result.get('checkpoint'),
        "sealed_contract_check": {
            "span_rule_matches_default": (span.window_seconds_min <= rule["window_seconds"] <= span.window_seconds_max
                                          and rule["min_span_seconds"] == span.min_span_duration_seconds and rule["hysteresis_windows"] == span.hysteresis_frames),
            "presenter_minimum_n_default": split.presenter_minimum_n, "presenter_minimum_n_tagged_pending": split.presenter_minimum_n_tagged_pending,
            "languages_meeting_presenter_minimum": [c for c, s in result["split"]["per_language"].items() if s.get("meets_presenter_minimum_n")],
            "per_language_accuracy_default": moac.per_language_accuracy_default, "per_language_accuracy_tagged_pending": moac.per_language_accuracy_tagged_pending,
            "code_switch_span_accuracy_default": moac.code_switch_span_accuracy_default, "code_switch_material_present": False,
            "no_speaker_id_probe": result["no_speaker_id_probe"], "abstention_rate_reported": moac.abstention_rate_reported},
        "verdict": result["artefact"]["moac"]["verdict"], "final_model": False, "certified_at": now()}
    (_jobs_dir() / f"run_certificate_{job['job_id']}.json").write_text(json.dumps(certificate, indent=1, default=str))
    return certificate


def _bank_base_registration(result):
    """Doc 20 training-base posture: extend the sealed overlay registrations by identity with the
    weight hash measured on the host, the ratified licence id and the LoRA-adapter declaration."""
    sealed = _sealed_language_cognition()
    anchors = {"whisper-lid-v1-mit": sealed.WHISPER_LID_REGISTRATION_TRAINING_BASE_ANCHOR,
               "speechbrain-voxlingua107-apache-2-0": sealed.VOXLINGUA107_REGISTRATION_TRAINING_BASE_ANCHOR}
    banked = {}
    for entry, measured in result.items():
        anchor = anchors[entry]
        carrier = sealed.LanguageCognitionTrainingBaseRegistration_v1(
            sealed_lid_registration=anchor, training_base_posture_hash=measured["weight_sha256"],
            licence_id_pinned=anchor.licence_id, lora_adapter_declaration=measured["lora_adapter_declaration"])
        banked[entry] = {"sealed_model_entry": anchor.model_entry, "training_base_posture_hash": carrier.training_base_posture_hash,
                         "licence_id_pinned": carrier.licence_id_pinned, "licence_card_measured": measured.get("licence_card"),
                         "lora_adapter_declaration": carrier.lora_adapter_declaration, "repo": measured["repo"],
                         "revision": measured["revision"], "host_path": f"{_host()}://{measured['local_path']}",
                         "execution_mode": measured["execution_mode"], "banked_at": now()}
    (_jobs_dir() / "training_base_registration.json").write_text(json.dumps(banked, indent=1))
    return banked
