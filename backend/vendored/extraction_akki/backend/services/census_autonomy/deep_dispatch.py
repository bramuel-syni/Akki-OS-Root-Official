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
        if source=='rms_obs': config={**access['obs'],'driver':'object_store'}
        elif source=='digicow_rds': config={**access['digicow'],'driver':'rds_data'}
        elif source=='rms_nas': config={'driver':'nas_nfs','root':os.environ['CENSUS_NAS_ROOT']}
        else: raise ValueError('SOURCE_CUSTODY_NOT_AVAILABLE')
    return {**config,'source_id':source}

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
        remaining=int(deadline-time.time())
        if remaining<=3: raise TimeoutError('BUDGET_EXHAUSTED')
        if runtime=='non_gpu_jump':
            client=_connect_jump(_jump_config(),min(20,remaining)); expected=os.environ['CENSUS_JUMP_HOSTNAME']
        else:
            client,host_config=_connect(runtime,min(20,remaining)); expected=host_config.hostname_expected
        bundle,code_hash=build_bundle()
        # Connection and code preparation consume the same job budget.
        remaining=int(deadline-time.time())
        if remaining<=3: raise TimeoutError('BUDGET_EXHAUSTED')
        control={'bundle':bundle,'code_sha256':code_hash,'census_run_id':run_id,'tenant_id':tenant,
                 'source_id':source,'runtime_id':runtime,'hostname_expected':expected,
                 'lawful_basis_sha256':lawful_hash,'max_seconds':remaining-2,'connector':config}
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
            # the SSH window), including completion already queued at deadline.
            if channel.exit_status_ready() and not channel.recv_ready() and not channel.recv_stderr_ready(): break
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