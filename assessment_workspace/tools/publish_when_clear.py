"""Wait for the re-authored estate pack to clear, then publish the static downloads (same path the autopilot uses)."""
import os
import sys
import time

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from services.transform_forms.doc_studio import publish, store  # noqa: E402

commission = sys.argv[1]
deadline = time.time() + int(sys.argv[2]) if len(sys.argv) > 2 else time.time() + 1500
while time.time() < deadline:
    record = store.load_record('RMS', commission)
    state = (record or {}).get('release', {}).get('state')
    print(time.strftime('%H:%M:%S'), state, (record or {}).get('release', {}).get('reason', '')[:140], flush=True)
    if state == 'clear':
        print(publish.publish('RMS', record), flush=True)
        break
    if state == 'blocked':
        break
    time.sleep(30)
