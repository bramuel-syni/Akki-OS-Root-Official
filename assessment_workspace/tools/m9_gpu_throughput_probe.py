"""Read-only throughput probe for the running corrective trials (control plane only, no data path)."""
import json
import os
import shlex
import sys
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.training_runner.ssh_seam import execute_remote_command  # noqa: E402

host = os.environ['LANGUAGE_COGNITION_HOST']
root = os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']
jobs = sys.argv[1:] or ['lcj-a6ea5b4bcdf6', 'lcj-e365bce78871']
seconds = int(os.environ.get('PROBE_SECONDS', '10'))
parts = [f"date -u +%FT%TZ; nvidia-smi --query-gpu=index,utilization.gpu,memory.used,power.draw --format=csv,noheader"]
for j in jobs:
    parts.append(f"echo __JOB__ {j}; cat {shlex.quote(root + '/jobs/' + j + '/state.json')} 2>/dev/null; echo; tail -c 600 {shlex.quote(root + '/jobs/' + j + '/worker.log')} 2>/dev/null")
parts.append(f"echo __UTIL__; nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader -l 1 & sleep {seconds}; kill %1 2>/dev/null; echo __PS__; ps -eo pid,pcpu,pmem,etimes,args | grep -E 'language_cognition|lcj-' | grep -v grep | cut -c1-160; echo __TOP__; top -bn1 | head -5")
result = execute_remote_command(host, '; '.join(parts), purpose='m9_gpu_throughput_probe', timeout=seconds + 60)
print('rc', result.rc, 'receipt', result.receipt_id)
out = result.stdout_redacted
head, _, rest = out.partition('__UTIL__')
print(head)
util, _, tail = rest.partition('__PS__')
per = {}
for line in util.strip().splitlines():
    if ',' in line:
        idx, u = [x.strip() for x in line.split(',')[:2]]
        per.setdefault(idx, []).append(int(u.replace('%', '').strip() or 0))
for idx, vals in sorted(per.items()):
    print(f'GPU{idx}: samples={len(vals)} mean={sum(vals)/len(vals):.1f}% min={min(vals)} max={max(vals)}')
print(tail[:3000])
if result.rc != 0:
    print('STDERR', result.stderr_redacted[-800:])
