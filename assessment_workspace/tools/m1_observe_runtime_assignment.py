"""Observe runtime metadata via Akki's existing pinned remote-command seam.

No dataset/weight contents, process arguments or credentials cross this seam.
This is readiness evidence, never a training/admission/acceptance receipt.
"""
import json
import os
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.environ['AKKI_CONFIG_ENV_FILE'])
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'backend/vendored/extraction_akki/backend'))
from services.training_runner.ssh_seam import execute_remote_command, list_hosts

PROBE = '''import importlib.util,json,os,pathlib,platform,shutil,subprocess
config=json.loads(%r)
result={'hostname':platform.node(),'observed_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
 'nas_root_present':os.path.isdir(config['nas_root']),'nas_mounted':os.path.ismount(config['nas_root']),
 'census_python_present':os.path.isfile(config['python']),
 'system_python_packages':{name:bool(importlib.util.find_spec(name)) for name in ('torch','transformers','peft')},
 'gpu_process_count':None,'training_claim':'Not established by a runtime observation'}
if shutil.which('nvidia-smi'):
 p=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10)
 if p.returncode==0: result['gpu_process_count']=len([line for line in p.stdout.splitlines() if line.strip()])
print(json.dumps(result))
'''


def main():
    report = {'observed_at': datetime.now(timezone.utc).isoformat(), 'runtimes': []}
    config = json.dumps({'nas_root': os.environ['CENSUS_NAS_ROOT'], 'python': os.environ['CENSUS_REMOTE_PYTHON']})
    for host in list_hosts():
        command = 'python3 -c ' + shlex.quote(PROBE % config)
        result = execute_remote_command(host, command, purpose='m1_assignment_readiness', timeout=30)
        row = {'runtime_id': host, 'receipt_id': result.receipt_id, 'exit_code': result.rc}
        if result.rc == 0:
            row.update(json.loads(result.stdout_redacted))
        else:
            row['status'] = 'runtime_observation_failed'
        report['runtimes'].append(row)
    destination = Path(__file__).resolve().parents[1] / 'notes/m1_execution'
    path = destination / ('ASSIGNMENT_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.json')
    path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()