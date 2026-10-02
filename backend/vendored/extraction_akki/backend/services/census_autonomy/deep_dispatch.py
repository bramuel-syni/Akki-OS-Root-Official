"""Control-plane adapter: resolve custody, dispatch reviewed code, verify receipts.

No estate SDK or file reader is invoked in this process. Source credentials are
sent only over existing pinned SSH as stdin, never shell arguments or receipts.
"""
import hashlib
import json
import os
import shlex
import time
import traceback
import re
from pathlib import Path
from services.census_autonomy import operational_store as store
from services.census_autonomy.estate_connector_registry import resolve_connector
from services.census_autonomy.deep_bundle import build_bundle, BOOTSTRAP
from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config
from services.census_autonomy.remote_dispatch import _connect

def connector_for(run_id,tenant,source,lawful_hash):
    from services.census_autonomy.operational_scope import SOURCE_TENANTS
    if SOURCE_TENANTS.get(source)!=tenant: raise ValueError('SOURCE_TENANT_MISMATCH')
    if source=='rms_mysql':
        path,_=resolve_connector(run_id,tenant,source,lawful_hash)
        try: config=json.loads(path.read_text())['sources'][source]
        finally: path.unlink(missing_ok=True)
    else:
        access=json.loads(Path(os.environ['AKKI_CENSUS_JUMP_CONFIG']).read_text())
        # Resumable enumeration frontier lives on the admitted worker, never in E1.
        state_dir=os.environ['CENSUS_REMOTE_STATE_DIR']
        if source=='rms_obs': config={**access['obs'],'driver':'object_store','state_dir':state_dir}
        elif source=='digicow_rds': config={**access['digicow'],'driver':'rds_data'}
        elif source=='rms_nas': config={'driver':'nas_nfs','root':os.environ['CENSUS_NAS_ROOT'],'state_dir':state_dir}
        else: raise ValueError('SOURCE_CUSTODY_NOT_AVAILABLE')
    return {**config,'source_id':source}

# The NAS share and egress-pinned relational grants are reachable only from the jump host.
JUMP_GOVERNED_SOURCES=('rms_mysql','rms_nas')

def pull_seam_hop():
    jump=_jump_config()
    return {'host':jump['jump_host'],'port':int(jump['jump_port']),'user':jump['jump_user'],'password':jump['jump_password'],
            'hostname_expected':os.environ['CENSUS_JUMP_HOSTNAME'],'python':os.environ['CENSUS_REMOTE_PYTHON'],
            'known_hosts':Path(os.environ['AKKI_CENSUS_JUMP_KNOWN_HOSTS']).read_text()}

def content_settings(source=None):
    """Full-content pass bindings: the admitted audio-language and music models (by job id and artefact hash), the GPU venv that
    hosts them, and the host-volume directories for the durable inventory/rows and the purged scratch. No caps: the only bound is
    the engine's bounded run, which the resumable frontier chains until every readable object is read."""
    from services.training_lab import estate_language
    models=estate_language._models()
    nas=source=='rms_nas'   # the share is read through the jump host's SFTP: few sessions, bandwidth-bound
    return {'gpu_python':os.environ['M9_REMOTE_PYTHON'],'lab_corpus_root':os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'],
            'audio_model_dir':models['audio']['dir'],'audio_model_sha256':models['audio']['sha256'],'audio_model_job':estate_language.AUDIO_MODEL_JOB,
            'music_model_path':models['music']['path'],'music_model_sha256':models['music']['sha256'],'music_model_job':estate_language.MUSIC_MODEL_JOB,
            'state_dir':os.environ['CENSUS_CONTENT_STATE_DIR'],'scratch_dir':os.environ['CENSUS_CONTENT_SCRATCH_DIR'],'nas_root':os.environ['CENSUS_NAS_ROOT'],
            'batch_size':256,'block_windows':2048,'download_workers':2 if nas else int(os.environ.get('CENSUS_CONTENT_DOWNLOAD_WORKERS','6')),'prefetch_bytes':(2 if nas else 4)<<30,
            'priority_labels':_priority_labels(source),
            'owner_order_ref':'owner order 2026-10-02: run the census with Akki and both GPU hosts for the entire estate; no shortcuts; read everything'}

def _priority_labels(source):
    """Stores with the most audio files (from the retained enumeration) are listed and read first; image/web buckets last."""
    from services.census_autonomy.estate_intelligence_report import _latest_store_outcome
    from services.census_autonomy.deep_content import AUDIO, VIDEO
    outcome=_latest_store_outcome(source,'RMS') if source else None
    rows=[]
    for s in (outcome or {}).get('sources') or []:
        formats=s.get('formats') or {}
        rows.append((-sum(n for ext,n in formats.items() if ext in AUDIO),-sum(n for ext,n in formats.items() if ext in VIDEO),-(s.get('volume_bytes') or 0),s['label']))
    return [r[3] for r in sorted(rows)]

def execute_source(run_id,tenant,source,lawful_hash,deadline):
    from services.training_runner.ssh_seam import list_hosts
    result={'protocol':'akki-census-deep-v1','census_run_id':run_id,'tenant_id':tenant,'source_id':source,
            'execution_location':'control_plane','source_rows_returned':0,'status':'blocked',
            'observed_at':store.now(),'worker_receipt_id':None,'sources':[]}
    client=None
    try:
        cursor=store.get(run_id,tenant)
        if not cursor: raise ValueError('DURABLE_COMMISSION_REQUIRED')
        hosts=list_hosts(); selected=cursor.get('worker_id')
        runtime=selected or ('non_gpu_jump' if source in ('rms_mysql','rms_nas') else hosts[-1] if source=='digicow_rds' else hosts[0])
        if runtime!='non_gpu_jump' and runtime not in hosts: raise ValueError('UNRECOGNIZED_WORKER')
        config=connector_for(run_id,tenant,source,lawful_hash)
        if cursor.get('source_refs'): config['source_refs']=cursor['source_refs']
        # Full-content measurement (owner order 2026-10-02): the GPU worker of record reads every media object; models and host paths bind here.
        if cursor.get('measurement')=='content_full':
            if runtime=='non_gpu_jump': raise ValueError('CONTENT_MEASUREMENT_REQUIRES_GPU_WORKER')
            config['content']=content_settings(source)
        # Pull seam: a GPU worker of record executes jump-governed sources through the jump host.
        if runtime!='non_gpu_jump' and source in JUMP_GOVERNED_SOURCES: config['pull_via']=pull_seam_hop()
        remaining=int(deadline-time.time())
        if remaining<=3: raise TimeoutError('BUDGET_EXHAUSTED')
        if runtime=='non_gpu_jump':
            client=_connect_jump(_jump_config(),min(20,remaining)); expected=os.environ['CENSUS_JUMP_HOSTNAME']
        else:
            client,host_config=_connect(runtime,min(20,remaining)); expected=host_config.hostname_expected
        # Hour-long jobs are silent until the receipt; keep the pinned session alive across stateful middleboxes.
        client.get_transport().set_keepalive(30)
        bundle,code_hash=build_bundle()
        # Connection and code preparation consume the same job budget.
        remaining=int(deadline-time.time())
        if remaining<=3: raise TimeoutError('BUDGET_EXHAUSTED')
        # The worker stops measuring before E1's deadline so partial measurements can still be flushed.
        margin=min(45,max(2,remaining//4))
        control={'bundle':bundle,'code_sha256':code_hash,'census_run_id':run_id,'tenant_id':tenant,
                 'source_id':source,'runtime_id':runtime,'hostname_expected':expected,
                 'lawful_basis_sha256':lawful_hash,'max_seconds':remaining-margin,'connector':config}
        channel=client.get_transport().open_session(timeout=15)
        channel.settimeout(remaining)
        channel.exec_command(shlex.quote(os.environ['CENSUS_REMOTE_PYTHON'])+' -c '+shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(control).encode()); channel.shutdown_write()
        output=bytearray(); diagnostic=bytearray()
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
                # Mongo's document bound; schema measurements only, never unlimited raw data.
                if len(output)>12*1024*1024: channel.close(); raise ValueError('MEASUREMENT_RECEIPT_TOO_LARGE')
            if channel.recv_stderr_ready():
                chunk=channel.recv_stderr(65536)
                diagnostic.extend(chunk[:max(0,65536-len(diagnostic))])
            # SSH exit-status does not require the peer to close the channel.
            # Drain both streams before collecting it (large receipts can fill
            # the SSH window). Terminate only on channel EOF: exit-status can be
            # ready while stdout is still in flight (observed truncation at 3×64KB).
            if channel.exit_status_ready() and getattr(channel,'eof_received',True) and not channel.recv_ready() and not channel.recv_stderr_ready(): break
            if time.time()>=deadline:
                result['transport_diagnostic']={'stdout_bytes':len(output),'stderr_bytes':len(diagnostic),
                    'stderr_sha256':hashlib.sha256(diagnostic).hexdigest()}
                channel.close(); raise TimeoutError('WORKER_DEADLINE')
            time.sleep(.02)
        code=channel.recv_exit_status()
        result['transport_diagnostic']={'exit_code':code,'stdout_bytes':len(output),'stderr_bytes':len(diagnostic),
            'stderr_sha256':hashlib.sha256(diagnostic).hexdigest(),
            'error_classes':[v.decode() for v in re.findall(rb'^([A-Za-z]+(?:Error|Exception)):',diagnostic,re.M)]}
        if code!=0: raise ValueError('REMOTE_WORKER_FAILED')
        value=json.loads(output)
        if value.get('worker',{}).get('code_sha256')!=code_hash or value.get('worker',{}).get('runtime_id')!=runtime:
            raise ValueError('WORKER_PROVENANCE_MISMATCH')
        receipt_id=value.pop('worker_receipt_id',None)
        digest='cwr-'+hashlib.sha256(json.dumps(value,sort_keys=True,default=str).encode()).hexdigest()
        if receipt_id!=digest: raise ValueError('WORKER_RECEIPT_DIGEST_MISMATCH')
        value['worker_receipt_id']=receipt_id
        value['worker']['transport_verified']=True
        value['worker']['server_key_sha256']=hashlib.sha256(client.get_transport().get_remote_server_key().asbytes()).hexdigest()
        value['transport_diagnostic']=result['transport_diagnostic']
        result=value
    except Exception as exc:
        # Only local classified exceptions; never copy SDK/SSH raw credential diagnostics.
        result['reason_code']=str(exc) if isinstance(exc,(ValueError,TimeoutError)) and str(exc).isupper() else type(exc).__name__
        result['error_sites']=[f'{Path(frame.filename).name}:{frame.lineno}' for frame in traceback.extract_tb(exc.__traceback__)[-3:]]
    finally:
        if client: client.close()
    path=store.cursor_dir()/f'transport-{run_id}-{source}.json'
    path.write_text(json.dumps({'census_run_id':run_id,'source_id':source,'at_utc':store.now(),
                               'stage':'deep_external','worker_status':result['status'],
                               'worker':result.get('worker'), 'reason_code':result.get('reason_code')},indent=2))
    return result