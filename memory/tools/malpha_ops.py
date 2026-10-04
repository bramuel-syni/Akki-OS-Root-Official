"""Mα smoke/ops helper: submit a small worker phase directly, or refresh/show a job. Usage:
  python malpha_ops.py smoke_aip <host> <gpu>      → tiny aip_build into aip_db_smoke
  python malpha_ops.py smoke_lane <host> <gpu> <phase> <extra-json>
  python malpha_ops.py refresh <job_id>
  python malpha_ops.py log <job_id> [bytes]
"""
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
os.chdir('/app/backend/vendored/extraction_akki/backend')
from services.training_runner import m9_dispatch  # noqa: E402
from services.training_lab import malpha  # noqa: E402

SMOKE_DB = f"{os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']}/malpha/aip_db_smoke"


def common(gpu, phase_extra):
    return {'commission_id': 'SMOKE', 'languages': ['kik', 'kam', 'swa'], 'gpu_index': int(gpu), 'budget_mode': 'uncapped_until_billing', 'owner_order_ref': malpha.OWNER_ORDER_REF, 'seed': malpha.SEED, 'iteration': 0, 'aip_db_dir': SMOKE_DB, **phase_extra}


cmd = sys.argv[1]
if cmd == 'smoke_aip':
    params = common(sys.argv[3], {'lab_corpus_root': os.environ['LANGUAGE_COGNITION_REMOTE_ROOT'], 'max_files_per_language': 3, 'cpu_workers': 4, 'token_max_seconds': 12.0, 'codec_sample_per_language': 3, 'brand_lexicon': malpha.BRAND_LEXICON})
    job = m9_dispatch.submit('malpha_aip_build', params, sys.argv[2], 'malpha-smoke', malpha._lawful())
    print(json.dumps({k: job.get(k) for k in ('job_id', 'status', 'reason', 'remote')}, indent=1))
elif cmd == 'smoke_lane':
    extra = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
    params = common(sys.argv[3], extra)
    job = m9_dispatch.submit(sys.argv[4], params, sys.argv[2], 'malpha-smoke', malpha._lawful())
    print(json.dumps({k: job.get(k) for k in ('job_id', 'status', 'reason', 'remote')}, indent=1))
elif cmd == 'refresh':
    job = m9_dispatch.refresh(sys.argv[2])
    out = {k: job.get(k) for k in ('job_id', 'status', 'reason', 'process_alive', 'finished_at')}
    out['progress'] = (job.get('remote_state') or {}).get('progress'); out['stages'] = list(((job.get('remote_state') or {}).get('stages') or {}).keys())
    out['log_tail'] = job.get('worker_log_tail')
    if job.get('receipt'):
        r = job['receipt']; out['receipt_status'] = r.get('status'); out['error'] = r.get('error')
        if r.get('result'): print(json.dumps(r['result'], indent=1, default=str)[:12000])
    print(json.dumps(out, indent=1, default=str))
elif cmd == 'log':
    from services.training_runner.ssh_seam import execute_remote_command
    job = m9_dispatch.load_job(sys.argv[2]); n = sys.argv[3] if len(sys.argv) > 3 else '6000'
    r = execute_remote_command(job['host'], f"tail -c {n} {job['remote']['job_dir']}/worker.log; echo; echo __STATE__; cat {job['remote']['job_dir']}/state.json | head -c 3000", purpose='malpha_log', timeout=60)
    print(r.stdout_redacted)
elif cmd == 'tick':
    print(json.dumps(malpha.tick(), indent=1, default=str))
elif cmd == 'status':
    print(json.dumps(malpha.status(), indent=1, default=str)[:20000])
