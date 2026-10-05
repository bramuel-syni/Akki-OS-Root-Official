"""WP-A2 governed restart of the contained reader (stop → start) after the inference-thread fix; master-admin principal; same lawful ref."""
import json
import sys
import time

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402

PRINCIPAL = '6ab56dd48894abb269135ca0'
LAWFUL = 'OWNER_ORDERS §12 Wave A autonomous · BUILD_PLAN_V2 WP-A2'
stopped = cr.stop('WP-A2 latency root cause: cuDNN SDPA compiled a kernel per new sequence length (2.1 tok/s until every length seen, then 44.8); generate now excludes the cuDNN backend', PRINCIPAL)
print('STOPPED', json.dumps(stopped, default=str)[:400])
started = cr.start(PRINCIPAL, LAWFUL)
print('STARTED', json.dumps({'job': {k: started['job'].get(k) for k in ('job_id', 'status', 'reason')}, 'placement': (started.get('placement') or {}).get('entry_id'), 'already_running': started['already_running']}, default=str))
for _ in range(40):
    time.sleep(6)
    st = cr.status()
    stage = (st.get('remote_state') or {}).get('stage') if isinstance(st.get('remote_state'), dict) else None
    print('STATUS', st.get('status'), stage, json.dumps((st.get('remote_state') or {}).get('warmup_seconds') if isinstance(st.get('remote_state'), dict) else None))
    if st.get('status') != 'running' or stage == 'serving':
        break
print('FINAL', json.dumps({k: st.get(k) for k in ('status', 'job')}, default=str)[:600])
