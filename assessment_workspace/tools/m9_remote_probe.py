"""Run a one-off read-only Python probe on an M9 GPU host with the shipped M9 worker bundle (control plane only).

usage: m9_remote_probe.py <host> <gpu_index> <script.py> [timeout_seconds]
"""
import base64
import os
import shlex
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.training_runner import m9_dispatch as m9  # noqa: E402
from services.training_runner.ssh_seam import execute_remote_command  # noqa: E402

host, gpu, script_path = sys.argv[1], sys.argv[2], sys.argv[3]
extra = " ".join(shlex.quote(a) for a in sys.argv[5:])
probe_env = os.environ.get("PROBE_ENV", "")
timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 600
root = m9._remote_root()
bundle, code_hash = m9.build_bundle()
remote_zip = f'{root}/checks/bundle_{code_hash[:12]}.zip'
remote_py = f'{root}/checks/probe_{code_hash[:12]}.py'
script_b64 = base64.b64encode(open(script_path, 'rb').read()).decode()
command = (f"mkdir -p {shlex.quote(root + '/checks')} && echo {shlex.quote(bundle)} | base64 -d > {shlex.quote(remote_zip)} && "
           f"echo {shlex.quote(script_b64)} | base64 -d > {shlex.quote(remote_py)} && "
           f"cd {shlex.quote(root)} && {probe_env} HF_HOME={shlex.quote(root + '/hf_cache')} HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 CUDA_VISIBLE_DEVICES={gpu} "
           f"{shlex.quote(m9._remote_python())} {shlex.quote(remote_py)} {shlex.quote(root)} {shlex.quote(remote_zip)} {extra} 2>&1 | grep -v 'Loading weights' | tail -60")
result = execute_remote_command(host, command, purpose='m9_remote_probe', timeout=timeout)
print('rc', result.rc, 'receipt', result.receipt_id, 'bundle', code_hash[:12])
print(result.stdout_redacted[-8000:])
if result.stderr_redacted.strip():
    print('STDERR', result.stderr_redacted[-1500:])
