"""M1 control-plane commissioning of remote runtime prerequisite observations.

No estate source is read here; remote observations use existing pinned transport.
No passwords, addresses or raw stderr are printed or stored in the report.
"""
import json
import shlex
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config
from services.census_autonomy.remote_dispatch import _connect
from services.training_runner.ssh_seam import list_hosts

PROBE = '''import importlib.util,json,os,platform,shutil,subprocess
mods=['pymysql','boto3','pydantic','langdetect','numpy']
d={'hostname':platform.node(),'python':platform.python_version(),
 'packages':{m:bool(importlib.util.find_spec(m)) for m in mods},
 'commands':{m:bool(shutil.which(m)) for m in ['mysql','smbclient','ffprobe','nvidia-smi','pip3']},
 'mounts':{m:os.path.isdir(m) for m in ['/mnt/nfs-share','/mnt/volume_dkgjrkx','/mnt/akki-storage-3388s']}}
if shutil.which('nvidia-smi'):
 p=subprocess.run(['nvidia-smi','--query-gpu=uuid,name,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10)
 d['gpu_inventory']=p.stdout.strip().splitlines() if p.returncode==0 else []
print(json.dumps(d))
'''

def main():
    results = []
    for runtime in ['non_gpu_jump', *list_hosts()]:
        client = None
        try:
            client = _connect_jump(_jump_config(), 15) if runtime == 'non_gpu_jump' else _connect(runtime, 15)[0]
            _, out, err = client.exec_command('python3 -c ' + shlex.quote(PROBE), timeout=30)
            raw = out.read(); err.read()
            if out.channel.recv_exit_status() != 0:
                raise RuntimeError('PREREQUISITE_PROBE_FAILED')
            results.append({'runtime_id': runtime, 'status': 'observed', **json.loads(raw)})
        except Exception as exc:
            results.append({'runtime_id':runtime,'status':'blocked','error_type':type(exc).__name__})
        finally:
            if client:
                client.close()
    path=Path('/app/assessment_workspace/notes/m1_execution/PREREQUISITES.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    main()