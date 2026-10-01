"""Independent watchdog (closes the M2 §6 'watchdog not placed' gap): the Watch's own record is countersigned on a
machine the Watch does not control.

Each pass sends ONE statement to the custody host over the pinned SSH seam: per-tenant control-Ledger heads, the
hash now stored at the seq the host last recorded, the Watch observation feed's row count, whole-file digest and
the digest of the prefix the host already saw, and the gate action-store count. The host keeps its OWN
append-only chain (~/.akki_witness/watch_chain.jsonl) and its own Ed25519 key, and judges continuity itself: a
head that moved backwards or changed at a seq it already recorded, a feed prefix that no longer matches, or a
gap longer than twice the agreed interval ("Watch silence is itself an alarm") is a finding it signs as such.
E1 verifies the signature against the registered witness key, banks the pass, puts a `witness` row on the feed
and raises the existing tamper alarm on divergence. The host holds no Watch or governance credentials and cannot
act on the estate; the control plane cannot alter what the host already recorded.
"""
import base64
import hashlib
import json
import os
import shlex
import time
import uuid
from datetime import datetime, timezone

from services.ledger_writer import mongo_control
from services.watch import commission_gate

COLLECTION = 'watch_witness_passes'
HOST = os.environ.get('WATCH_WITNESS_HOST', 'akki-vm')
INTERVAL_S = int(os.environ.get('WATCH_WITNESS_INTERVAL_S') or 900)
WITNESS_ID = 'wi_akki_vm_ledger_countersigner'
SCRIPT_PATH = '~/.akki_witness/watch_witness.py'
SCRIPT = r'''
import base64, hashlib, json, os, socket, subprocess, sys, time
D = os.path.expanduser('~/.akki_witness'); CHAIN = D + '/watch_chain.jsonl'; KEY = D + '/ed25519.pem'
def canonical(o): return json.dumps(o, sort_keys=True, separators=(',', ':')).encode()
def last():
    if not os.path.exists(CHAIN): return None
    lines = [l for l in open(CHAIN, encoding='utf-8').read().splitlines() if l.strip()]
    return json.loads(lines[-1]) if lines else None
cmd = sys.argv[1]
if cmd == 'last':
    print(json.dumps((last() or {}).get('record') or {})); sys.exit(0)
stmt = json.loads(base64.b64decode(sys.argv[2])); prev = (last() or {}).get('record'); now = time.time(); findings = []
for tenant, cur in sorted(stmt['tenants'].items()):
    p = (prev or {}).get('tenants', {}).get(tenant)
    if not p: continue
    ps, ph = p['ledger']['seq'], p['ledger']['hash']
    if cur['ledger']['seq'] < ps: findings.append({'tenant': tenant, 'kind': 'ledger_head_regressed', 'recorded_seq': ps, 'seen_seq': cur['ledger']['seq']})
    elif cur['ledger']['seq'] == ps and cur['ledger']['hash'] != ph: findings.append({'tenant': tenant, 'kind': 'ledger_head_rewritten', 'seq': ps})
    elif cur.get('ledger_hash_at', {}).get(str(ps)) != ph: findings.append({'tenant': tenant, 'kind': 'ledger_history_rewritten', 'seq': ps})
    if cur['feed']['rows'] < p['feed']['rows']: findings.append({'tenant': tenant, 'kind': 'feed_truncated', 'recorded_rows': p['feed']['rows'], 'seen_rows': cur['feed']['rows']})
    elif cur['feed'].get('prefix_rows') == p['feed']['rows'] and cur['feed'].get('prefix_sha256') != p['feed']['sha256']: findings.append({'tenant': tenant, 'kind': 'feed_rewritten', 'rows': p['feed']['rows']})
gap = round(now - prev['epoch'], 1) if prev else None
if gap is not None and gap > 2 * stmt['interval_s']: findings.append({'kind': 'silence', 'gap_s': gap, 'interval_s': stmt['interval_s']})
verdict = 'divergence' if any(f['kind'] != 'silence' for f in findings) else 'silence' if findings else 'consistent'
record = {'witness_seq': ((prev or {}).get('witness_seq') or 0) + 1, 'epoch': round(now, 3), 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)), 'host': socket.gethostname(),
          'statement_sha256': hashlib.sha256(canonical(stmt)).hexdigest(), 'statement_at': stmt['at'], 'interval_s': stmt['interval_s'], 'gap_s': gap,
          'tenants': {t: {'ledger': c['ledger'], 'feed': {'rows': c['feed']['rows'], 'sha256': c['feed']['sha256']}} for t, c in stmt['tenants'].items()},
          'actions': stmt.get('actions'), 'findings': findings, 'verdict': verdict,
          'prev_record_sha256': hashlib.sha256(canonical(prev)).hexdigest() if prev else None, 'script_sha256': hashlib.sha256(open(__file__, 'rb').read()).hexdigest()}
tmp = D + '/stmt.%d' % os.getpid()
with open(tmp, 'wb') as fh: fh.write(canonical(record))
try:
    sig = subprocess.run(['openssl', 'pkeyutl', '-sign', '-inkey', KEY, '-rawin', '-in', tmp], capture_output=True, check=True).stdout
finally:
    os.remove(tmp)
pub = subprocess.run(['openssl', 'pkey', '-in', KEY, '-pubout'], capture_output=True, check=True).stdout.decode()
entry = {'record': record, 'signature_ed25519_b64': base64.b64encode(sig).decode()}
with open(CHAIN, 'a', encoding='utf-8') as fh: fh.write(json.dumps(entry, sort_keys=True) + '\n')
os.chmod(CHAIN, 0o600)
print(json.dumps({**entry, 'public_key_pem': pub}))
'''.lstrip()
SCRIPT_SHA256 = hashlib.sha256(SCRIPT.encode()).hexdigest()


def now():
    return datetime.now(timezone.utc)


def _iso(dt):
    return dt.isoformat().replace('+00:00', 'Z')


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def _feed_digests(tenant, prefix_rows):
    path = commission_gate._dir() / f'{tenant}.jsonl'
    lines = path.read_text(encoding='utf-8').splitlines() if path.exists() else []
    whole = hashlib.sha256('\n'.join(lines).encode()).hexdigest()
    prefix = hashlib.sha256('\n'.join(lines[:prefix_rows]).encode()).hexdigest() if prefix_rows is not None else None
    return {'rows': len(lines), 'sha256': whole, 'prefix_rows': prefix_rows, 'prefix_sha256': prefix}


async def statement(db, previous):
    """What the host is asked to judge: current heads plus the exact values it needs to compare with its own record."""
    events = await mongo_control.read_events(db, {})
    by_tenant = {}
    for e in events:
        by_tenant.setdefault(e['row']['tenant_id'], []).append(e['row'])
    from services.watch.persistence import read_actions
    tenants = {}
    prev_tenants = (previous or {}).get('tenants') or {}
    feed_tenants = {p.stem for p in commission_gate._dir().glob('*.jsonl')} if commission_gate._dir().exists() else set()
    for tenant in sorted(set(by_tenant) | feed_tenants | set(prev_tenants)):
        rows = by_tenant.get(tenant, [])
        head = max(rows, key=lambda r: r['seq']) if rows else None
        prev = prev_tenants.get(tenant) or {}
        prev_seq = (prev.get('ledger') or {}).get('seq')
        at_prev = next((r['hash'] for r in rows if r['seq'] == prev_seq), None) if prev_seq else None
        tenants[tenant] = {'ledger': {'seq': head['seq'], 'hash': head['hash']} if head else {'seq': 0, 'hash': None},
                           'ledger_hash_at': {str(prev_seq): at_prev} if prev_seq else {},
                           'feed': _feed_digests(tenant, (prev.get('feed') or {}).get('rows'))}
    return {'at': _iso(now()), 'interval_s': INTERVAL_S, 'tenants': tenants, 'actions': len(read_actions()), 'ledger_rows': len(events)}


def _remote(command, purpose, timeout=60):
    from services.training_runner.ssh_seam import execute_remote_command
    return execute_remote_command(HOST, command, purpose=purpose, timeout=timeout)


def _install_command():
    b64 = base64.b64encode(SCRIPT.encode()).decode()
    d = '~/.akki_witness'
    return (f"mkdir -p {d} && chmod 700 {d} && ([ -f {d}/ed25519.pem ] || openssl genpkey -algorithm ed25519 -out {d}/ed25519.pem >/dev/null 2>&1); chmod 600 {d}/ed25519.pem; "
            f"echo {b64} | base64 -d > {SCRIPT_PATH}.tmp && mv {SCRIPT_PATH}.tmp {SCRIPT_PATH} && chmod 600 {SCRIPT_PATH} && sha256sum {SCRIPT_PATH} | cut -d' ' -f1")


def _verify(entry):
    from cryptography.hazmat.primitives import serialization
    public_key = serialization.load_pem_public_key(entry['public_key_pem'].strip().encode())
    public_key.verify(base64.b64decode(entry['signature_ed25519_b64']), _canonical(entry['record']))
    return hashlib.sha256(entry['public_key_pem'].strip().encode()).hexdigest()[:32]


def _registered_fingerprint():
    from services.watch.witness import _identity_on_record
    identity = _identity_on_record(WITNESS_ID)
    if identity is None:
        return None
    ref = identity.signing_material_ref
    return ref.split('ed25519:', 1)[1].split()[0] if 'ed25519:' in ref else None


def _alarm(tenant, finding, record):
    from services.watch.witness import raise_tamper_alarm
    kind = 'missing_receipt' if finding['kind'] in ('feed_truncated', 'ledger_head_regressed') else 'modified_receipt'
    stamp = record['at'].replace('-', '_').replace(':', '').lower()
    payload = {'alarm_id': f"ta_{stamp[:10]}_{uuid.uuid4().hex[:8]}", 'witness_id': WITNESS_ID, 'detected_at': record['at'], 'evidence_kind': kind,
               'evidence_ref': f"watch_witness://{tenant}/{finding['kind']}#witness_seq={record['witness_seq']}",
               'alarm_note': f"Independent witness on {record['host']} found {finding['kind'].replace('_', ' ')} for tenant {tenant}: {json.dumps({k: v for k, v in finding.items() if k not in ('tenant', 'kind')}, sort_keys=True)}; its own prior record disagrees with what the control plane now presents."}
    try:
        return raise_tamper_alarm(payload).alarm_id
    except ValueError as exc:
        return f'alarm_not_recorded:{str(exc)[:80]}'


async def run_pass(db, actor=None):
    """One witness pass: install/refresh the host script if needed, read the host's last record, send the statement, verify and bank."""
    started = time.monotonic()
    doc = {'pass_id': 'wp-' + uuid.uuid4().hex[:12], 'at': _iso(now()), 'host': HOST, 'actor': actor, 'interval_s': INTERVAL_S, 'script_sha256': SCRIPT_SHA256}
    try:
        installed = _remote(_install_command(), 'watch_witness_install', timeout=60)
        if installed.rc != 0 or installed.stdout_redacted.strip().splitlines()[-1] != SCRIPT_SHA256:
            raise RuntimeError(f'WITNESS_SCRIPT_NOT_INSTALLED rc={installed.rc}')
        last = _remote(f'python3 {SCRIPT_PATH} last', 'watch_witness_last', timeout=40)
        if last.rc != 0:
            raise RuntimeError(f'WITNESS_LAST_FAILED rc={last.rc}')
        previous = json.loads(last.stdout_redacted.strip().splitlines()[-1] or '{}')
        stmt = await statement(db, previous)
        doc['statement'] = stmt
        judged = _remote(f"python3 {SCRIPT_PATH} judge {shlex.quote(base64.b64encode(_canonical(stmt)).decode())}", 'watch_witness_judge', timeout=60)
        if judged.rc != 0:
            raise RuntimeError(f'WITNESS_JUDGE_FAILED rc={judged.rc} {judged.stderr_redacted[-160:]}')
        entry = json.loads(judged.stdout_redacted.strip().splitlines()[-1])
        record = entry['record']
        fingerprint = _verify(entry)
        registered = _registered_fingerprint()
        if registered is None:
            from services.business_continuity.ledger_archive import _ensure_witness
            _ensure_witness(fingerprint, HOST)
            registered = fingerprint
        doc.update({'outcome': 'witnessed', 'record': record, 'signature_ed25519_b64': entry['signature_ed25519_b64'], 'signature_verified': True,
                    'key_fingerprint': fingerprint, 'key_matches_registered_identity': fingerprint == registered, 'witness_id': WITNESS_ID,
                    'verdict': record['verdict'], 'findings': record['findings'], 'host_script_sha256': record['script_sha256'],
                    'host_script_matches': record['script_sha256'] == SCRIPT_SHA256})
        if not doc['key_matches_registered_identity']:
            doc['verdict'] = 'divergence'
            doc['findings'] = doc['findings'] + [{'kind': 'witness_key_changed', 'registered': registered, 'seen': fingerprint}]
    except Exception as exc:
        doc.update({'outcome': 'unreachable', 'verdict': 'silence', 'signature_verified': False, 'findings': [{'kind': 'witness_unreachable', 'error': f'{type(exc).__name__}: {str(exc)[:200]}'}]})
    doc['duration_ms'] = int((time.monotonic() - started) * 1000)
    alarms = []
    for finding in doc.get('findings') or []:
        tenant = finding.get('tenant')
        if finding['kind'] in ('silence', 'witness_unreachable', 'witness_key_changed'):
            continue
        alarms.append(_alarm(tenant, finding, doc['record']))
    doc['alarms'] = alarms
    for tenant in (doc.get('statement') or {}).get('tenants') or {}:
        try:
            commission_gate._append(tenant, {'kind': 'witness', 'at': doc['at'], 'tenant_id': tenant, 'pass_id': doc['pass_id'], 'host': HOST, 'verdict': doc['verdict'],
                                             'witness_seq': (doc.get('record') or {}).get('witness_seq'), 'findings': [f for f in doc['findings'] if f.get('tenant') in (None, tenant)],
                                             'signature_verified': doc['signature_verified']})
        except commission_gate.GateUnobservable:
            doc.setdefault('feed_write_failed', []).append(tenant)
    await db[COLLECTION].insert_one(dict(doc))
    doc.pop('_id', None)
    return doc


async def latest(db, limit=12):
    return [_public(d) async for d in db[COLLECTION].find({}, {'statement': 0}).sort('at', -1).limit(limit)]


def _public(doc):
    doc = dict(doc)
    doc.pop('_id', None)
    return doc


async def status(db):
    """Console state: placed on which host, last pass and verdict, and whether the watchdog itself has gone silent."""
    passes = await latest(db, 12)
    last = passes[0] if passes else None
    silent = last is None or (now() - datetime.fromisoformat(last['at'].replace('Z', '+00:00'))).total_seconds() > 2 * INTERVAL_S
    return {'placed': True, 'host': HOST, 'witness_id': WITNESS_ID, 'interval_s': INTERVAL_S, 'passes_on_record': await db[COLLECTION].count_documents({}),
            'last_pass': {k: last.get(k) for k in ('pass_id', 'at', 'outcome', 'verdict', 'findings', 'signature_verified', 'key_matches_registered_identity', 'duration_ms')} if last else None,
            'host_record_seq': (last or {}).get('record', {}).get('witness_seq') if last else None,
            'silent': silent, 'divergences_on_record': await db[COLLECTION].count_documents({'verdict': 'divergence'}),
            'statement': ('Independent watchdog placed on ' + HOST + ' (own Ed25519 key, own append-only chain); '
                          + (f"last pass {last['at']} · {last['verdict']}" if last else 'no pass recorded yet')
                          + (' · WATCHDOG SILENT beyond twice the agreed interval' if silent else '')),
            'recent': passes}
