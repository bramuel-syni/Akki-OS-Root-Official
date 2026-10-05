"""Read-only probe: contained reader status + health + lane states (WP-A2 resume check)."""
import json
import sys

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.training_runner import m9_dispatch as m9  # noqa: E402

st = cr.status()
print('STATUS', json.dumps({k: st.get(k) for k in ('status', 'job', 'remote_state')}, default=str)[:1500])
if st.get('status') == 'running':
    try:
        h = cr.health()
        print('HEALTH', json.dumps({k: h.get(k) for k in ('status', 'requests', 'served', 'refused', 'unparseable', 'latency_seconds', 'resident_mib', 'free_mib_now', 'egress_guard')}, default=str))
    except Exception as exc:  # noqa: BLE001
        print('HEALTH_ERR', repr(exc)[:300])
for jid in ('m9j-2bc0eea34925', 'm9j-dade36472f5e', 'm9j-82202771c7fd'):
    try:
        j = m9.refresh(jid)
        print('LANE', jid, j.get('status'), j.get('host'), (j.get('remote_state') or {}).get('progress', {}).get('stage') if isinstance((j.get('remote_state') or {}).get('progress'), dict) else '')
    except Exception as exc:  # noqa: BLE001
        print('LANE_ERR', jid, repr(exc)[:200])
