"""Read-only latency probe: the SYNTHETIC BRD read in isolation, timed on host; prints output size."""
import json
import sys
import time

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402

sys.path.insert(0, '/app/backend/tests/shield')
from test_contained_reader import CATEGORIES, SYNTHETIC  # noqa: E402

for i in range(2):
    t0 = time.monotonic()
    out = cr.read(SYNTHETIC, CATEGORIES, 'latency_probe_long')
    body = json.dumps(out['reading'], ensure_ascii=False)
    print(f'LONG_READ_{i} seconds_on_host', out['seconds'], 'wall', round(time.monotonic() - t0, 1), 'reading_chars', len(body), 'privileged', len(out['reading']['privileged']))
h = cr.health()
print('HEALTH', json.dumps(h.get('latency_seconds')))
