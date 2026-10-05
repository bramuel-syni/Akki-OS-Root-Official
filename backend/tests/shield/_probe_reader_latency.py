"""Read-only latency probe for the contained reader: health latency + one short SYNTHETIC read timed end to end."""
import json
import sys
import time

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402

h = cr.health()
print('HEALTH', json.dumps({k: h.get(k) for k in ('requests', 'served', 'unparseable', 'latency_seconds', 'free_mib_now')}))
t0 = time.monotonic()
out = cr.read('Summarise the attached board paper in three bullet points for the finance committee.', [], 'latency_probe')
print('SHORT_READ seconds_on_host', out['seconds'], 'wall', round(time.monotonic() - t0, 1))
print('READING', json.dumps(out['reading'], ensure_ascii=False)[:600])
