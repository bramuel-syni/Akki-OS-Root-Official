"""Run a one-off read-only Python check on the language-cognition host with the shipped worker bundle (no data path to E1)."""
import base64
import json
import os
import shlex
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.audio_plane_v1 import language_cognition_dispatch as lc  # noqa: E402
from services.training_runner.ssh_seam import execute_remote_command  # noqa: E402

host = os.environ['LANGUAGE_COGNITION_HOST']
root = os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']
script = open(sys.argv[1]).read()
gpu = sys.argv[2] if len(sys.argv) > 2 else '0'
bundle, code_hash = lc.build_bundle('train_corrective')
remote_zip = f'{root}/checks/bundle_{code_hash[:12]}.zip'
remote_py = f'{root}/checks/check_{code_hash[:12]}.py'
command = (f"mkdir -p {shlex.quote(root + '/checks')} && echo {shlex.quote(bundle)} | base64 -d > {shlex.quote(remote_zip)} && "
           f"echo {shlex.quote(base64.b64encode(script.encode()).decode())} | base64 -d > {shlex.quote(remote_py)} && "
           f"CUDA_VISIBLE_DEVICES={gpu} {shlex.quote(lc._remote_python())} {shlex.quote(remote_py)} {shlex.quote(root)} {shlex.quote(remote_zip)} 2>&1 | tail -40")
result = execute_remote_command(host, command, purpose='m9_featurizer_check', timeout=int(os.environ.get('CHECK_TIMEOUT', '240')))
print('rc', result.rc, 'receipt', result.receipt_id, 'bundle', code_hash)
print(result.stdout_redacted[-6000:])
if result.stderr_redacted.strip():
    print('STDERR', result.stderr_redacted[-1500:])
