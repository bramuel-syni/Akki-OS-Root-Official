"""M3 live drill driver — drives the commissioning API exactly as the portal does (control plane only).

    python m3_live_drill.py draft   --table training_questions [--max-records 200]
    python m3_live_drill.py freeze  --draft <draft_id> --key <idempotency>
    python m3_live_drill.py advance --request <request_id> [--times 30] [--sleep 6]
    python m3_live_drill.py run     --request <request_id>
    python m3_live_drill.py stop    --request <request_id>
Credentials come from environment: AKKI_DRILL_EMAIL / AKKI_DRILL_PASSWORD (never written here).
"""
import argparse
import json
import os
import sys
import time

import requests

API = open('/app/frontend/.env').read().split('REACT_APP_BACKEND_URL=')[1].splitlines()[0].strip()


def session():
    login = requests.post(f'{API}/api/auth/login', json={'email': os.environ['AKKI_DRILL_EMAIL'], 'password': os.environ['AKKI_DRILL_PASSWORD']}, timeout=30)
    login.raise_for_status()
    token = login.json().get('token') or login.json().get('access_token')
    s = requests.Session()
    s.headers.update({'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
    return s


def show(response):
    try:
        body = response.json()
    except ValueError:
        body = response.text[:2000]
    print(response.status_code, json.dumps(body, indent=1, default=str)[:6000])
    return body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['draft', 'freeze', 'advance', 'run', 'stop', 'view', 'approvals'])
    parser.add_argument('--table'); parser.add_argument('--database', default='digicow_live'); parser.add_argument('--unit', default='digicow_rds')
    parser.add_argument('--operation', default='processed_intelligence'); parser.add_argument('--max-records', type=int, default=200)
    parser.add_argument('--objective', default='Pilot M3-T1: qualified, de-identified units from one censused DigiCow table for grounded answers.')
    parser.add_argument('--draft'); parser.add_argument('--key'); parser.add_argument('--request')
    parser.add_argument('--times', type=int, default=30); parser.add_argument('--sleep', type=float, default=6)
    a = parser.parse_args()
    s = session()
    if a.mode == 'draft':
        body = {'objective_text': a.objective, 'operation': a.operation, 'units': [a.unit], 'bounds': {'max_records': a.max_records, 'max_seconds': 900}}
        if a.table:
            body['reach'] = {'database': a.database, 'table': a.table}
        show(s.post(f'{API}/api/portal/commission/drafts', json=body, timeout=60))
    elif a.mode == 'view':
        show(s.get(f'{API}/api/portal/commission/drafts/{a.draft}', timeout=60))
    elif a.mode == 'freeze':
        show(s.post(f'{API}/api/portal/commission/drafts/{a.draft}/freeze', json={'idempotency_key': a.key}, timeout=120))
    elif a.mode == 'approvals':
        show(s.get(f'{API}/api/portal/approvals/{a.request}', timeout=60))
    elif a.mode == 'advance':
        for i in range(a.times):
            r = s.post(f'{API}/api/portal/commission/{a.request}/advance', timeout=180)
            body = r.json()
            print(f"[{i}] {r.status_code} state={body.get('state')} phase={body.get('phase')} reason={body.get('reason_code')} outcome={body.get('outcome')} next={str(body.get('next_action') or body.get('reason'))[:120]}")
            if body.get('state') in ('ready', 'failed', 'cancelled') or body.get('phase') in ('ready', 'complete', 'failed', 'cancelled'):
                break
            time.sleep(a.sleep)
        show(s.get(f'{API}/api/portal/requests/{a.request}/run', timeout=60))
    elif a.mode == 'run':
        show(s.get(f'{API}/api/portal/requests/{a.request}/run', timeout=60))
    elif a.mode == 'stop':
        show(s.post(f'{API}/api/portal/requests/{a.request}/stop', json={}, timeout=60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
