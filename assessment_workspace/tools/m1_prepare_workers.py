"""Install the census-only dependency environment on existing external workers."""
import concurrent.futures
import importlib.metadata
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

PACKAGES = ['pydantic', 'pymysql', 'boto3', 'langdetect', 'paramiko']

def prepare(runtime):
    client = None
    try:
        pins = [f'{p}=={importlib.metadata.version(p) if p!="langdetect" else "1.0.9"}' for p in PACKAGES]
        client = _connect_jump(_jump_config(),15) if runtime=='non_gpu_jump' else _connect(runtime,15)[0]
        setup = 'set -eu; if [ ! -x /opt/akki-census/bin/python ]; then apt-get update -qq; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-venv; python3 -m venv /opt/akki-census; fi; /opt/akki-census/bin/python -m pip install --quiet ' + ' '.join(shlex.quote(p) for p in pins)
        _, out, err = client.exec_command('sudo -n sh -c '+shlex.quote(setup),timeout=240)
        # Drain both channels; dependency diagnostics contain no estate credentials.
        output=out.read(); errors=err.read(); code=out.channel.recv_exit_status()
        return {'runtime_id':runtime,'exit_code':code,'packages':pins,
                'status':'prepared' if code==0 else 'blocked',
                'diagnostic': errors.decode(errors='replace')[-500:] if code else ''}
    except Exception as exc:
        return {'runtime_id':runtime,'status':'blocked','error_type':type(exc).__name__}
    finally:
        if client: client.close()

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        report=list(pool.map(prepare,['non_gpu_jump',*list_hosts()]))
    path=Path('/app/assessment_workspace/notes/m1_execution/WORKER_PREPARATION.json')
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))