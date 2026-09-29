"""The deployable extraction worker. Runs only inside an admitted runtime, never in E1.

One entrypoint, `execute(control)`, dispatched by `control['mode']`:
  attest · admit_limits · submit · status · cancel · inner_select · inspect ·
  custody_prepare · custody_status · write_attempt · unit_select
Durable state lives in the runtime's state directory; E1 receives metadata and signed
receipts only. Credentials arrive on stdin inside the SSH channel and are held in a 0600
job file consumed by the detached runner, which deletes it after connecting.
"""
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from services.extraction_runtime import worker_identity as identity

PROTOCOL = 'akki-extraction-runtime/1'
EXECUTOR_VERSION = 'extraction-runtime/1'
RUNNER = ("import sys; sys.path.insert(0, sys.argv[1] + '/worker.zip'); "
          "from services.extraction_runtime.structured_records_worker import run_job; run_job(sys.argv[1])")


def _state(control):
    return Path(os.path.expanduser(control['state_dir']))


def _job_dir(control, operation_key=None):
    path = _state(control) / 'jobs' / (operation_key or control['operation_key'])
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def _read(path):
    return json.loads(path.read_text()) if path.exists() else None


def _write(path, value, mode=0o600):
    tmp = path.with_suffix(path.suffix + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    with os.fdopen(fd, 'w') as handle:
        json.dump(value, handle, sort_keys=True, default=str)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def _receipted(value):
    body = {k: v for k, v in value.items() if k != 'worker_receipt_id'}
    return {**body, 'worker_receipt_id': 'ewr-' + hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()}


def _sign_observation(control, category, context, claim, **kw):
    return identity.receipt(control['state_dir'], tenant_id=control['tenant_id'], signer_id=control['signer_id'],
        key_id=control['key_id'], kind='observation', scope_refs=control['scope_refs'],
        request_sha256=control.get('request_sha256'), ttl_seconds=control.get('receipt_ttl_seconds', 30 * 86400),
        claims=identity.observation(category, context, claim, **kw))


class _Store:
    """The tenant's resting place for sealed artefacts: an S3-compatible object store, or a filesystem
    shared by the admitted runtimes. Keys are relative; the bucket is the root. E1 never holds a client."""

    def __init__(self, store):
        self.provider = store.get('provider', 'huawei_obs')
        self.bucket = store['bucket']
        if self.provider == 'shared_filesystem':
            self.root = Path(self.bucket)
            self.client = None
        else:
            import boto3
            from botocore.config import Config
            self.client = boto3.client('s3', endpoint_url=store['endpoint'], region_name=store['region'],
                                       aws_access_key_id=store['access_key_id'], aws_secret_access_key=store['secret_access_key'],
                                       config=Config(signature_version='s3v4', s3={'addressing_style': 'path'},
                                                     connect_timeout=10, read_timeout=60, retries={'max_attempts': 2}))

    def _path(self, key):
        path = (self.root / key.lstrip('/')).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError('STORE_KEY_OUTSIDE_ROOT')
        return path

    def put(self, key, body):
        if self.client is None:
            path = self._path(key)
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
            tmp = path.with_suffix(path.suffix + '.tmp')
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o640)
            with os.fdopen(fd, 'wb') as handle:
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
            return hashlib.sha256(body).hexdigest()[:32]
        return self.client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType='application/x-ndjson').get('ETag', '').strip('"')

    def head(self, key):
        if self.client is None:
            stat = self._path(key).stat()
            return {'size': stat.st_size, 'etag': hashlib.sha256(self._path(key).read_bytes()).hexdigest()[:32],
                    'last_modified': str(stat.st_mtime)}
        head = self.client.head_object(Bucket=self.bucket, Key=key)
        return {'size': head['ContentLength'], 'etag': head.get('ETag', '').strip('"'), 'last_modified': str(head.get('LastModified'))}

    def get(self, key, limit=64 * 1024 * 1024 + 1):
        if self.client is None:
            with open(self._path(key), 'rb') as handle:
                return handle.read(limit)
        return self.client.get_object(Bucket=self.bucket, Key=key)['Body'].read(limit)

    def url(self, key, seconds):
        """A time-boxed retrieval capability, or None where the store has no HTTPS origin."""
        if self.client is None:
            return None
        return self.client.generate_presigned_url('get_object', Params={'Bucket': self.bucket, 'Key': key}, ExpiresIn=int(seconds))


# ----------------------------------------------------------------------------- modes

def _capacity_observed():
    memory_gb = None
    try:
        with open('/proc/meminfo') as handle:
            for line in handle:
                if line.startswith('MemTotal:'):
                    memory_gb = int(line.split()[1]) // (1024 * 1024)
                    break
    except OSError:
        pass
    gpus = 0
    try:
        out = subprocess.run(['nvidia-smi', '-L'], capture_output=True, text=True, timeout=10)
        gpus = sum(1 for line in out.stdout.splitlines() if line.startswith('GPU ')) if out.returncode == 0 else 0
    except (OSError, subprocess.SubprocessError):
        gpus = 0
    return {'cpu_cores': os.cpu_count() or 0, 'gpu_count': gpus, 'memory_gb': memory_gb or 0,
            'compute_classes': ['cpu'] + (['gpu'] if gpus else []), 'accounting': list(MEASURABLE_COMPUTE)}


def attest(control):
    key = identity.ensure(control['state_dir'])
    modules = {}
    for name in ('pymysql', 'boto3', 'paramiko', 'cryptography', 'pydantic'):
        try:
            __import__(name)
            modules[name] = True
        except Exception:
            modules[name] = False
    return {'protocol': PROTOCOL, 'executor_version': EXECUTOR_VERSION, 'hostname': socket.gethostname(),
            'python': sys.executable, 'state_dir': control['state_dir'], 'modules': modules,
            'capacity_observed': _capacity_observed(), **key}


MEASURABLE_COMPUTE = ('cpu_seconds',)  # this worker accounts CPU with os.times(); it has no GPU accounting


def admit_limits(control):
    envelope = control['envelope']
    now = int(time.time())
    if not envelope['starts_epoch'] <= now < envelope['stop_work_by_epoch']:
        return {'status': 'refused', 'reason_code': 'RUNTIME_ADMISSION_WINDOW_INVALID'}
    unmeasurable = [q['unit'] for q in envelope['limits'] if q['dimension'] == 'active_compute' and q['unit'] not in MEASURABLE_COMPUTE]
    if unmeasurable:
        return {'status': 'refused', 'reason_code': 'RUNTIME_ACCOUNTING_UNAVAILABLE:' + ','.join(unmeasurable)}
    job = _job_dir(control)
    _write(job / 'envelope.json', envelope)
    receipt = _sign_observation(control, 'runtime', control['request_sha256'], envelope,
                                reservation_ref=envelope['reservation_ref'])
    return {'status': 'acknowledged', 'receipt': receipt, 'runtime_id': control['runtime_id']}


def submit(control):
    job = _job_dir(control)
    if (job / 'job.json').exists():
        return status(control)
    envelope = _read(job / 'envelope.json')
    if envelope is None:
        return _result(control, 'failed', 'RUNTIME_LIMITS_NOT_ADMITTED')
    _write(job / 'secrets.json', control['secrets'])
    (job / 'worker.zip').write_bytes(__import__('base64').b64decode(control['bundle']))
    public = {k: v for k, v in control.items() if k not in ('secrets', 'bundle')}
    public['envelope'] = envelope
    public['accepted_epoch'] = int(time.time())
    _write(job / 'job.json', public)
    log = open(job / 'runner.log', 'ab')
    process = subprocess.Popen([sys.executable, '-c', RUNNER, str(job)], stdin=subprocess.DEVNULL, stdout=log,
                               stderr=log, start_new_session=True, close_fds=True, cwd=str(job))
    (job / 'runner.pid').write_text(str(process.pid))
    return _result(control, 'accepted', 'RUNNER_STARTED', progress={'pid': process.pid})


def _alive(job):
    try:
        pid = int((job / 'runner.pid').read_text())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def status(control):
    job = _job_dir(control)
    result = _read(job / 'result.json')
    if result is not None:
        return result
    if not (job / 'job.json').exists():
        return _result(control, 'unknown', 'JOB_NOT_SUBMITTED')
    checkpoint = _read(job / 'checkpoint.json') or {}
    if _alive(job) is None:
        # A detached runner that vanished without a result is a fact, not a guess.
        return _result(control, 'failed', 'RUNNER_EXITED_WITHOUT_RESULT', progress=checkpoint)
    return _result(control, 'running', 'RUNNER_ALIVE', progress=checkpoint)


def cancel(control):
    job = _job_dir(control)
    (job / 'stop').write_text(str(int(time.time())))
    for _ in range(50):
        result = _read(job / 'result.json')
        if result is not None:
            return result
        if _alive(job) is None:
            break
        time.sleep(.1)
    pid = _alive(job)
    if pid is not None:
        os.kill(pid, signal.SIGTERM)
        time.sleep(.5)
    result = _read(job / 'result.json')
    if result is not None:
        return result
    return _result(control, 'cancelled', 'CANCELLED_BEFORE_RESULT', usage=[])


def write_attempt(control):
    """M3-T5 drill: prove the guard refuses a write verb before any connection is opened."""
    from services.mtafiti.executor.readonly_sql_guard import refuse_if_write, WriteVerbRefused
    try:
        refuse_if_write(control['sql'])
    except WriteVerbRefused as exc:
        claim = {'sql_sha256': hashlib.sha256(control['sql'].encode()).hexdigest(), 'refused': True,
                 'reason': type(exc).__name__}
        return {'status': 'refused', 'reason_code': 'WRITE_VERB_REFUSED', 'claim': claim,
                'receipt': _sign_observation(control, 'refusal', control['request_sha256'], claim) if control.get('sign') else None}
    return {'status': 'failed', 'reason_code': 'WRITE_GUARD_DID_NOT_REFUSE'}


def inspect(control):
    store = _Store(control['secrets']['object_store'])
    observed, verified = [], True
    for artifact in control['artifacts']:
        body = store.get(artifact['key'])
        digest = hashlib.sha256(body).hexdigest()
        units = 0
        rings_ok = True
        for line in body.splitlines():
            if not line.strip():
                continue
            units += 1
            try:
                unit = json.loads(line)
                rings_ok = rings_ok and {'provenance', 'signal', 'relational', 'reextraction_handle', 'defensibility'} <= set(unit)
            except ValueError:
                rings_ok = False
        ok = digest == artifact['sha256'] and len(body) == artifact['size_bytes'] and rings_ok
        verified = verified and ok
        observed.append({'ref': artifact['ref'], 'sha256': digest, 'size_bytes': len(body), 'units': units,
                         'five_rings': rings_ok, 'etag': store.head(artifact['key'])['etag'], 'matches': ok})
    claim = {'artifacts': [{k: o[k] for k in ('ref', 'sha256', 'size_bytes')} for o in observed],
             'inspector_runtime_id': control['runtime_id'], 'verified': verified}
    return {'status': 'complete' if verified else 'failed', 'verified': verified, 'observed': observed,
            'receipt': _sign_observation(control, 'independence', control['request_sha256'], claim)}


def _proof(control, stage, **fields):
    proof = {'delivery_id': control['delivery_id'], 'principal_id': control['principal_id'],
             'artifact_sha256': control['artifact']['sha256'], 'artifact_size_bytes': control['artifact']['size_bytes'],
             'stage': stage, 'provider_event_id': fields.pop('provider_event_id'),
             'current_rights_at_redemption': True, 'workspace_touched_bytes': False,
             'origin': None, 'endpoint_sha256': None, 'grant_receipt_ref': None, 'redeemed_epoch': None,
             'completed_epoch': None, 'delivered_bytes': None, 'observed_sha256': None}
    proof.update(fields)
    return proof


def custody_prepare(control):
    store = _Store(control['secrets']['object_store'])
    head = store.head(control['artifact']['key'])
    if head['size'] != control['artifact']['size_bytes']:
        return {'status': 'failed', 'reason_code': 'CUSTODY_OBJECT_SIZE_MISMATCH'}
    url = store.url(control['artifact']['key'], control['grant_seconds'])
    if url is None or not control.get('origin'):
        # The artefact rests in the store; a retrieval capability needs an HTTPS origin this store does not have.
        return {'status': 'held', 'reason_code': 'CUSTODY_ORIGIN_UNAVAILABLE', 'store': head}
    proof = _proof(control, 'grant', provider_event_id='head:' + (head['etag'].replace('-', '_') or 'head'),
                   origin=control['origin'], endpoint_sha256=hashlib.sha256(url.encode()).hexdigest())
    receipt = identity.receipt(control['state_dir'], tenant_id=control['tenant_id'], signer_id=control['signer_id'],
        key_id=control['key_id'], kind='observation', scope_refs=control['scope_refs'],
        request_sha256=control['request_sha256'], ttl_seconds=int(control['grant_seconds']),
        claims=identity.observation('delivery_grant', control['descriptor_sha256'], proof, typed={'delivery': proof}))
    return {'status': 'offered', 'receipt': receipt, 'url': url, 'store': head}


def custody_status(control):
    store = _Store(control['secrets']['object_store'])
    body = store.get(control['artifact']['key'])
    etag = store.head(control['artifact']['key'])['etag']
    now = int(time.time()) - 2
    proof = _proof(control, 'completed', provider_event_id='get:' + (etag.replace('-', '_') or 'get'),
                   grant_receipt_ref=control['grant_receipt_ref'], redeemed_epoch=int(control['redeemed_epoch']),
                   completed_epoch=now, delivered_bytes=len(body), observed_sha256=hashlib.sha256(body).hexdigest())
    receipt = identity.receipt(control['state_dir'], tenant_id=control['tenant_id'], signer_id=control['signer_id'],
        key_id=control['key_id'], kind='observation', scope_refs=control['scope_refs'],
        request_sha256=control['request_sha256'], ttl_seconds=control.get('receipt_ttl_seconds', 30 * 86400), now=now,
        claims=identity.observation('delivery_completion', control['descriptor_sha256'], proof, terminal=True,
                                    typed={'delivery': proof}))
    return {'status': 'completed', 'receipt': receipt, 'observed': {'sha256': proof['observed_sha256'], 'bytes': len(body)}}


def inner_select(control):
    from services.extraction_runtime.inner_hop import select_rows
    value = select_rows(control)
    value['hostname'] = socket.gethostname()
    return value


_STOP = {'the', 'and', 'for', 'are', 'was', 'were', 'what', 'which', 'who', 'how', 'many', 'much', 'with', 'from',
         'that', 'this', 'these', 'those', 'there', 'their', 'have', 'has', 'had', 'does', 'did', 'about', 'into',
         'than', 'then', 'them', 'they', 'you', 'your', 'our', 'any', 'all', 'can', 'not', 'but', 'its', 'per',
         'show', 'list', 'tell', 'give', 'find', 'when', 'where', 'why', 'will', 'would', 'should', 'could'}


def unit_terms(text):
    import re
    return {t for t in re.findall(r'[a-z0-9][a-z0-9_]{2,}', str(text).lower()) if t not in _STOP}


def _unit_text(unit):
    record = unit.get('record') or {}
    parts = [str(v) for v in record.values() if v is not None and not str(v).startswith('redacted:')]
    parts.append(str(unit.get('provenance', {}).get('context', '')))
    return ' '.join(parts)


def _relational_keys(unit):
    record = unit.get('record') or {}
    keys = set()
    for edge in unit.get('relational', {}).get('edges', []):
        column = str(edge.get('target_unit_ref', '')).rsplit('.', 1)[-1]
        if record.get(column) is not None:
            keys.add(f"{edge['target_unit_ref']}={record[column]}")
    return keys


def unit_select(control):
    """Qualified-memory read: whole units matching the question's terms, plus relational neighbours.
    Reads the sealed artefact only — never a source — and returns bounded, ordered candidates."""
    store = _Store(control['secrets']['object_store'])
    body = store.get(control['artifact']['key'])
    digest = hashlib.sha256(body).hexdigest()
    if digest != control['artifact']['sha256'] or len(body) != control['artifact']['size_bytes']:
        return {'status': 'failed', 'reason_code': 'ARTIFACT_DIGEST_MISMATCH', 'bytes_read': len(body)}
    wanted = set(control.get('terms') or [])
    pinned = set(control.get('unit_ids') or [])
    limit = int(control.get('max_candidates', 64))
    neighbour_limit = int(control.get('max_neighbours', 16))
    rows = []
    for position, line in enumerate(body.splitlines()):
        if not line.strip():
            continue
        unit = json.loads(line)
        overlap = len(wanted & unit_terms(_unit_text(unit)))
        rows.append({'position': position, 'unit': unit, 'overlap': overlap, 'rel_keys': _relational_keys(unit),
                     'content_sha256': hashlib.sha256(line.encode() if isinstance(line, str) else line).hexdigest()})
    matched = [r for r in rows if r['overlap'] > 0 or r['unit']['unit_id'] in pinned]
    matched.sort(key=lambda r: (-r['overlap'], r['position'], r['unit']['unit_id']))
    chosen = matched[:limit]
    chosen_ids = {r['unit']['unit_id'] for r in chosen}
    chosen_keys = set().union(*(r['rel_keys'] for r in chosen)) if chosen else set()
    neighbours = [r for r in rows if r['unit']['unit_id'] not in chosen_ids and r['rel_keys'] & chosen_keys]
    neighbours.sort(key=lambda r: (r['position'], r['unit']['unit_id']))

    def out(r, kind):
        return {'unit': r['unit'], 'position': r['position'], 'overlap': r['overlap'], 'kind': kind,
                'rel_keys': sorted(r['rel_keys']), 'content_sha256': r['content_sha256']}
    return {'status': 'complete', 'artifact_sha256': digest, 'bytes_read': len(body), 'units_total': len(rows),
            'matched_total': len(matched), 'neighbours_total': len(neighbours),
            'candidates': [out(r, 'matched') for r in chosen] + [out(r, 'neighbour') for r in neighbours[:neighbour_limit]]}


def sign_worker(control):
    """Self-attestation: the runtime signs its own Worker receipt with the key generated here."""
    identity.ensure(control['state_dir'])
    return {'status': 'signed', 'receipt': identity.receipt(control['state_dir'], tenant_id=control['tenant_id'],
        signer_id=control['signer_id'], key_id=control['key_id'], kind='worker', claims=control['claims'],
        scope_refs=control['scope_refs'], ttl_seconds=365 * 86400)}


MODES = {'attest': attest, 'admit_limits': admit_limits, 'submit': submit, 'status': status, 'cancel': cancel,
         'inspect': inspect, 'custody_prepare': custody_prepare, 'custody_status': custody_status,
         'inner_select': inner_select, 'write_attempt': write_attempt, 'sign_worker': sign_worker,
         'unit_select': unit_select}


def execute(control):
    if control.get('hostname_expected') and socket.gethostname() != control['hostname_expected']:
        raise ValueError('REMOTE_IDENTITY_MISMATCH')
    return _receipted({'protocol': PROTOCOL, 'mode': control['mode'], **MODES[control['mode']](control)})


def _result(control, state, reason, *, artifacts=(), usage=None, progress=None, extra=None):
    value = {'runtime_id': control['runtime_id'], 'operation_key': control['operation_key'],
             'request_sha256': control['request_sha256'], 'fence': control['fence'], 'state': state,
             'reason_code': reason, 'artifacts': list(artifacts), 'usage': usage, 'progress': progress or {}}
    if extra:
        value.update(extra)
    return value


# ----------------------------------------------------------------------------- detached runner

class Limiter:
    """Charge conservative upper bounds before reading; coupled to the hard watchdog below.
    Active compute is the runtime's own accounting: user+system CPU seconds of this runner and its children."""

    def __init__(self, envelope):
        self.limits = {(q['dimension'], q['unit']): float(q['quantity']) for q in envelope['limits']}
        self.used = {k: 0.0 for k in self.limits}
        self.envelope = envelope
        self.start = time.time()
        self.cpu_start = self._cpu()

    @staticmethod
    def _cpu():
        t = os.times()
        return t.user + t.system + t.children_user + t.children_system

    def remaining(self, dimension, unit):
        key = (dimension, unit)
        return self.limits[key] - self.used[key] if key in self.limits else float('inf')

    def before_batch(self, charges):
        if time.time() >= self.envelope['stop_work_by_epoch']:
            raise TimeoutError('RUNTIME_STOP_WORK_REACHED')
        cpu = ('active_compute', 'cpu_seconds')
        if cpu in self.limits:
            self.used[cpu] = round(self._cpu() - self.cpu_start, 3)
            if self.used[cpu] > self.limits[cpu]:
                raise ValueError('RUNTIME_LIMIT_WOULD_BE_EXCEEDED:active_compute')
        for key, value in charges.items():
            if key in self.limits and self.used[key] + value > self.limits[key]:
                raise ValueError('RUNTIME_LIMIT_WOULD_BE_EXCEEDED:' + key[0])
        for key, value in charges.items():
            if key in self.limits:
                self.used[key] += value

    def quantities(self, returned):
        self.used[('wall_clock', 'seconds')] = round(time.time() - self.start, 3)
        if ('returned_records', 'records') in self.limits:
            self.used[('returned_records', 'records')] = returned
        if ('active_compute', 'cpu_seconds') in self.limits:
            self.used[('active_compute', 'cpu_seconds')] = round(self._cpu() - self.cpu_start, 3)
        return [{'dimension': k[0], 'unit': k[1], 'quantity': str(int(v) if float(v).is_integer() else round(v, 3))}
                for k, v in sorted(self.used.items())]


def run_job(job_dir):
    job = Path(job_dir)
    control = json.loads((job / 'job.json').read_text())
    secrets = json.loads((job / 'secrets.json').read_text())
    (job / 'secrets.json').unlink()
    envelope = control['envelope']
    limiter = Limiter(envelope)
    done = threading.Event()

    def watchdog():
        while not done.wait(0.5):
            if time.time() >= envelope['terminate_by_epoch']:
                if not (job / 'result.json').exists():
                    _write(job / 'result.json', _receipted(_result(control, 'failed', 'RUNTIME_TERMINATION_CEILING_EXCEEDED',
                        usage=_usage(limiter.quantities(0)), extra={'receipts': _measurements(control, limiter, 0)})))
                os._exit(3)
    threading.Thread(target=watchdog, daemon=True).start()
    try:
        result = _extract(job, control, secrets, limiter)
    except Exception as exc:  # classified locally; never raw provider diagnostics
        reason = str(exc) if str(exc).isupper() or str(exc).split(':')[0].isupper() else type(exc).__name__
        result = _result(control, 'failed', reason[:120], usage=_usage(limiter.quantities(0)),
                         extra={'receipts': _measurements(control, limiter, 0)})
    done.set()
    _write(job / 'result.json', _receipted(result))


USAGE_UNITS = {('spend', 'USD'): 'usd_spend', ('wall_clock', 'seconds'): 'seconds',
               ('scanned_records', 'records'): 'records_scanned', ('returned_records', 'records'): 'records_returned',
               ('bytes_read', 'bytes'): 'bytes_read'}


def _usage(quantities):
    return [{'unit': USAGE_UNITS.get((q['dimension'], q['unit']), q['dimension'] + ':' + q['unit']), 'quantity': q['quantity']}
            for q in quantities]


def _measurements(control, limiter, returned):
    quantities = limiter.quantities(returned)
    return {'measurements': _sign_observation(control, 'measurements', control['request_sha256'],
                {'quantities': quantities, 'operation_key': control['operation_key']},
                reservation_ref=control['envelope']['reservation_ref'], quantities=quantities, terminal=True)}


def _extract(job, control, secrets, limiter):
    from services.extraction_runtime.units import compose
    from services.extraction_runtime.inner_hop import select_rows, via_jump
    selection, floor = control['selection'], control['floor']
    checkpoint = _read(job / 'checkpoint.json') or {'after': None, 'scanned': 0, 'returned': 0, 'bytes_read': 0,
                                                     'unqualified': 0, 'redactions': 0, 'seen': []}
    seen = set(checkpoint.pop('seen', []))
    units_path, unqualified_path = job / 'units.jsonl', job / 'unqualified.jsonl'
    bundle_b64 = __import__('base64').b64encode((job / 'worker.zip').read_bytes()).decode()
    code_sha256 = hashlib.sha256((job / 'worker.zip').read_bytes()).hexdigest()
    columns = selection['columns']
    meta = {'source_ref': selection['source_ref'], 'database': selection['database'], 'table': selection['table'],
            'primary_key': selection['primary_key'], 'role_signals': selection.get('role_signals', []),
            'job_kind': control['job_kind'], 'driver': secrets['connection'].get('driver', 'mysql')}
    row_bytes = max(64, int(selection.get('estimated_row_bytes', 512)))
    max_records = int(selection['max_records'])
    with open(units_path, 'a') as out, open(unqualified_path, 'a') as bad:
        while checkpoint['returned'] + checkpoint['unqualified'] < max_records:
            if (job / 'stop').exists():
                return _result(control, 'cancelled', 'STOPPED_BY_REQUESTER', usage=_usage(limiter.quantities(checkpoint['returned'])),
                               extra={'receipts': _measurements(control, limiter, checkpoint['returned']), 'progress': checkpoint})
            batch = min(int(selection.get('batch_size', 500)), max_records - checkpoint['returned'] - checkpoint['unqualified'])
            batch = int(min(batch, limiter.remaining('scanned_records', 'records')))
            if batch <= 0:
                break
            limiter.before_batch({('scanned_records', 'records'): batch, ('bytes_read', 'bytes'): batch * row_bytes})
            inner = {'connection': secrets['connection'], 'database': selection['database'], 'table': selection['table'],
                     'columns': columns, 'primary_key': selection['primary_key'], 'after': checkpoint['after'], 'limit': batch}
            if secrets.get('pull_via'):
                page = via_jump(secrets['pull_via'], inner, bundle_b64, code_sha256, control['envelope']['stop_work_by_epoch'])
            else:
                page = select_rows(inner)
            if page.get('status') != 'complete':
                raise ValueError(page.get('reason_code', 'SOURCE_READ_FAILED'))
            rows = page['rows']
            checkpoint['scanned'] += len(rows)
            checkpoint['bytes_read'] += int(page.get('bytes_read', 0))
            if ('bytes_read', 'bytes') in limiter.used:
                limiter.used[('bytes_read', 'bytes')] = float(checkpoint['bytes_read'])
            for row in rows:
                unit, reason = compose(row, page['columns'], meta, floor['columns'])
                key = str(row[page['columns'].index(selection['primary_key'])]) if selection['primary_key'] in page['columns'] else None
                if unit is not None and key in seen:
                    unit, reason = None, 'DUPLICATE_PRIMARY_KEY'
                if unit is None:
                    bad.write(json.dumps({'reason': reason, 'locator': {'table': selection['table'], 'key': key}}, sort_keys=True) + '\n')
                    checkpoint['unqualified'] += 1
                    continue
                seen.add(key)
                checkpoint['redactions'] += int(round(unit['signal']['dimensions']['redaction_ratio'] * len(page['columns'])))
                out.write(json.dumps(unit, sort_keys=True, default=str) + '\n')
                checkpoint['returned'] += 1
            out.flush(); bad.flush()
            if rows:
                checkpoint['after'] = rows[-1][page['columns'].index(selection['primary_key'])]
            _write(job / 'checkpoint.json', {**checkpoint, 'seen': sorted(seen)[:50000]})
            if len(rows) < batch:
                break
    return _seal_and_deliver(job, control, secrets, limiter, checkpoint)


def _seal_and_deliver(job, control, secrets, limiter, checkpoint):
    units_path = job / 'units.jsonl'
    body = units_path.read_bytes()
    sha256, size = hashlib.sha256(body).hexdigest(), len(body)
    store = _Store(secrets['object_store'])
    key = control['object_key']
    etag = store.put(key, body)
    artifact = {'ref': control['artifact_ref'], 'sha256': sha256, 'size_bytes': size, 'tenant_id': control['tenant_id'],
                'class_label': 'utterance'}
    lineage = {'version': 'akki.lineage.metadata/1', 'artifact_ref': artifact['ref'], 'artifact_sha256': sha256,
               'parents': list(control['parent_refs'])}
    receipts = _measurements(control, limiter, checkpoint['returned'])
    receipts['lineage'] = _sign_observation(control, 'lineage', control['request_sha256'], lineage, typed={'lineage': lineage})
    quality = {'qualified_units': checkpoint['returned'], 'unqualified_units': checkpoint['unqualified'],
               'redactions': checkpoint['redactions'], 'scanned_records': checkpoint['scanned'],
               'tripwires': ['schema_completeness', 'primary_key_present', 'duplicate_primary_key', 'pii_floor'],
               'matrix_rule_ref': 'matrix.structured_records.v0:pending_first_verified_sample'}
    return _result(control, 'complete', 'EXTRACTION_SEALED', artifacts=[artifact],
                   usage=_usage(limiter.quantities(checkpoint['returned'])),
                   extra={'receipts': receipts, 'object': {'provider': store.provider, 'bucket': store.bucket, 'key': key, 'etag': etag, 'size': size},
                          'quality': quality, 'progress': {k: v for k, v in checkpoint.items() if k != 'seen'}})
