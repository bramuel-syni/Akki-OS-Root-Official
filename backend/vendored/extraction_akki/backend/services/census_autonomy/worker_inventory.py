"""An explicit remote inventory command; GET consumers use retained receipts only."""
import hashlib
import json
import os
import shlex
from pathlib import Path
from services.census_autonomy.jump_dispatch import _connect_jump,_jump_config
from services.census_autonomy.remote_dispatch import _connect
from services.census_autonomy.registry_durability import collection
from services.census_autonomy.operational_store import now
from services.mtafiti.asset_registry_writer import append_census_evidence
from services.training_runner.ssh_seam import list_hosts

def refresh(tenant):
    collection(); observed=[]
    code=Path(__file__).with_name('deep_worker.py').read_text()+'\nprint(json.dumps(telemetry()))\n'
    for runtime in ['non_gpu_jump',*list_hosts()]:
        client=None; stamp=now()
        try:
            if runtime=='non_gpu_jump':
                client=_connect_jump(_jump_config(),15); expected=os.environ['CENSUS_JUMP_HOSTNAME']
            else:
                client,config=_connect(runtime,15); expected=config.hostname_expected
            _,out,err=client.exec_command('python3 -c '+shlex.quote(code),timeout=25)
            raw=out.read(); err.read()
            if out.channel.recv_exit_status()!=0: raise ValueError('Worker inventory did not complete')
            data=json.loads(raw)
            if data['hostname']!=expected: raise ValueError('Worker hostname differs from custody')
            row={'runtime_id':runtime,'telemetry':data,'observed_at':stamp,'transport_verified':True,
                 'server_key_sha256':hashlib.sha256(client.get_transport().get_remote_server_key().asbytes()).hexdigest(),
                 'status':'Connected','execution_mode':'inventory only; no workload qualification implied'}
        except Exception as exc:
            row={'runtime_id':runtime,'status':'Unreachable','reason_code':type(exc).__name__,'observed_at':stamp}
        finally:
            if client: client.close()
        evidence={'kind':'worker_inventory','observed_at':stamp,'worker':row}
        key='worker-observation:'+tenant+':'+runtime+':'+hashlib.sha256(stamp.encode()).hexdigest()[:16]
        append_census_evidence(key,tenant,evidence); observed.append(row)
    return observed