"""Remote entry point. Runs only inside the code bundle on an admitted SSH host."""
import hashlib
import json
import platform
import shutil
import subprocess
import time
from datetime import datetime,timezone

def telemetry():
    result={'hostname':platform.node(),'python':platform.python_version(),'gpu_devices':[]}
    if shutil.which('nvidia-smi'):
        p=subprocess.run(['nvidia-smi','--query-gpu=uuid,name,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10)
        if p.returncode==0:
            for line in p.stdout.strip().splitlines():
                uuid,name,memory,util=line.split(', ')
                result['gpu_devices'].append({'uuid':uuid,'name':name,'memory_mb':int(memory),'utilization_percent':int(util)})
    return result

def execute(control):
    started=time.time(); stamp=lambda:datetime.now(timezone.utc).isoformat()
    before=telemetry()
    if before['hostname']!=control['hostname_expected']: raise ValueError('REMOTE_IDENTITY_MISMATCH')
    deadline=started+control['max_seconds']; sources=[]; seam=None; inner_reason=None; content=None
    try:
        config=control['connector']; driver=config['driver']
        if config.get('content') and driver=='nas_nfs' and config.get('pull_via'):
            # Full-content pass: the share is listed and every media file read through the jump host's SFTP onto this GPU host (owner order 2026-10-02).
            from services.census_autonomy.deep_content import nas_full
            sources=nas_full(config,deadline); content=True
        elif config.get('content') and driver=='object_store':
            from services.census_autonomy.deep_content import objects_full
            sources=objects_full(config,deadline); content=True
        elif config.get('pull_via'):
            # Pull seam: this worker stays the worker of record; the code runs where the data is.
            from services.census_autonomy.deep_pull import through_jump
            inner,seam=through_jump(control,deadline)
            sources=inner.get('sources',[]); inner_reason=inner.get('reason_code')
        elif driver in ('mysql_metadata','rds_data'):
            from services.census_autonomy.deep_sql import run
            sources=run(config,deadline)
        elif driver=='nas_nfs':
            from services.census_autonomy.deep_files import nas
            sources=nas(config,deadline)
        elif driver=='object_store':
            from services.census_autonomy.deep_files import objects
            sources=objects(config,deadline)
        else: raise ValueError('SOURCE_DRIVER_NOT_BOUND')
        good=[s for s in sources if s['status'] in ('complete','partial')]
        status='complete' if sources and all(s['status']=='complete' for s in sources) else 'partial' if good else 'blocked'
        reason=None if status=='complete' else inner_reason or 'SOURCE_COVERAGE_INCOMPLETE'
    except Exception as exc:
        status='blocked'; reason=str(exc) if isinstance(exc,(ValueError,TimeoutError)) and str(exc).isupper() else type(exc).__name__
    result={'protocol':'akki-census-deep-v1','census_run_id':control['census_run_id'],'tenant_id':control['tenant_id'],
            'source_id':control['source_id'],'execution_location':'akki_host','observed_at':stamp(),
            'status':status,'source_rows_returned':0,'sources':sources,
            'database_count':sum(s.get('database_count',0) for s in sources),
            'table_count':sum(s.get('table_count',0) for s in sources),
            'row_count_estimate':sum(s.get('row_count_estimate',0) for s in sources),
            'worker':{'runtime_id':control['runtime_id'],'code_sha256':control['code_sha256'],
                      'lawful_basis_sha256':control['lawful_basis_sha256'],'wall_seconds':round(time.time()-started,3),
                      'execution_mode':'gpu' if content else 'cpu',
                      'gpu_compute_hours':round(max((sum(d.get('elapsed_s',0) for d in ((s.get('content') or {}).get('device_reports') or [])) for s in sources),default=0)/3600,4) if content else 0,
                      'telemetry':before}}
    if seam: result['worker']['pull_seam']=seam
    if reason: result['reason_code']=reason
    result['worker_receipt_id']='cwr-'+hashlib.sha256(json.dumps(result,sort_keys=True,default=str).encode()).hexdigest()
    return result