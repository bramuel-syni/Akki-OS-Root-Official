"""Contained reader — control plane (WP-A2 · Doc 1 A5.5 B43–B45, A5.6 B46 · Doc 11 A5.1 B35).

The estate's reasoning rung for privileged text: a registered, licence-verified base served on a tenant host loopback by the governed
serving seam (`m9_dispatch` phase `serve_reader`), placed through the residency register (owner D7) as a `serving_resident` under a demand
lease, relayed here one bounded request at a time over the sealed SSH seam. Nothing is persisted off-host; the reading is request-scoped.
Unavailability REFUSES (`ReaderUnavailable`) — the Shield stage never falls back to an external model for the read."""
import base64
import json
import os

from services.model_registry import residency
from services.model_registry.registry import annotate_model, attest_model, current_registry_version, load_registry, register_model
from services.training_runner import m9_dispatch as m9
from services.training_runner import m9_serving as serving

ROLE = 'contained_reader'
MODEL_ID = 'contained-reader-qwen3-8b-base'
DEFAULT_BASE = 'qwen3-8b-base'
MAX_CHARS = 12000
PORT_BASE = 8641
LEASE_IDLE_LAPSE_HOURS = 72


class ReaderUnavailable(RuntimeError):
    """The contained reader is not serving (not started, revoked, unreachable, or refused the reading). Fail closed."""


def _entry(model_id=MODEL_ID):
    entry = load_registry().get(model_id)
    if entry is None: raise ReaderUnavailable(f'{model_id} is not registered; start the reader first')
    if entry.get('role') != ROLE: raise ValueError('NOT_A_CONTAINED_READER:' + model_id)
    return entry


def _job(entry):
    job_id = (entry.get('serving') or {}).get('job_id')
    return m9.refresh(job_id) if job_id else None


def base_registration(host):
    result = serving._remote(host, f"cat {os.environ['M9_REMOTE_ROOT']}/base_registration.json", purpose='contained_reader_base_registration', timeout=30)
    if result.rc != 0: raise ReaderUnavailable(f'no base registration readable on {host}: {result.stderr_redacted[:120]}')
    try: return json.loads(result.stdout_redacted), result.receipt_id
    except ValueError as exc: raise ReaderUnavailable('base registration unreadable') from exc


def start(principal_id, lawful_ref, host='akki-vm-ii', gpu_index=1, base_registry_id=DEFAULT_BASE, model_id=MODEL_ID):
    """Register (receipted act), place through the residency register, dispatch the host server. No download: the base must already be registered on the host."""
    bases, receipt = base_registration(host)
    base = bases.get(base_registry_id)
    if not base: raise ReaderUnavailable(f'base {base_registry_id!r} is not registered on {host}; ingestion is a separate receipted registration act, never a runtime download')
    if not str(base.get('licence_verified', '')).startswith('apache'): raise ReaderUnavailable(f'base licence {base.get("licence_verified")!r} is not a verified permissive licence')
    n, models = current_registry_version()
    if model_id not in models:
        register_model(model_id, {'role': ROLE, 'base': base_registry_id, 'base_repo': base.get('repo'), 'base_revision': base.get('revision'), 'licence_verified': base.get('licence_verified'), 'weight_sha256': base.get('weight_sha256'), 'weight_bytes': base.get('weight_bytes'),
                                  'host': host, 'provenance': 'estate base registration (receipted); no runtime download', 'registration_receipt_id': receipt, 'registered_by': principal_id, 'registered_at': m9.now(), 'status': 'registered',
                                  'owner_ruling_ref': 'OWNER_ORDERS §12 (Wave A autonomous; D7 residency structure) · BUILD_PLAN_V2 WP-A2/WP-C7'})
    entry = _entry(model_id); current = _job(entry)
    if current and current['status'] == 'running': return {'job': current, 'entry': entry, 'already_running': True}
    weight_bytes = int(base.get('weight_bytes') or 0) or 17_000_000_000
    placement = residency.place('serving_resident', host, gpu_index, weight_bytes + 6 * residency.MIB * 1024, {'model_id': model_id, 'principal_id': principal_id}, f'contained reader for the Shield stage (WP-A2); base {base_registry_id} {weight_bytes / 1e9:.1f} GB bf16 + KV headroom; placed beside residents without eviction',
                                lease={'kind': 'demand', 'granted_by': principal_id, 'granted_at': m9.now(), 'renew_on': 'read request', 'lapse_after_idle_hours': LEASE_IDLE_LAPSE_HOURS, 'last_demand_at': None}, reuse_pointer='the Shield stage reuses this resident for every privileged read; no second copy is loaded')
    n, _ = current_registry_version()
    port = PORT_BASE
    used = {int((e.get('serving') or {}).get('port') or 0) for e in load_registry().values() if (e.get('serving') or {}).get('status') == 'running'}
    while port in used: port += 1
    params = {'base_registry_id': base_registry_id, 'expected_weight_sha256': base['weight_sha256'], 'port': port, 'gpu_index': gpu_index, 'max_chars': MAX_CHARS, 'residency_entry_id': placement['entry_id'],
              'authority': {'model_id': model_id, 'registry_version': n, 'granted_by': principal_id, 'granted_at': m9.now(), 'owner_ruling_ref': entry.get('owner_ruling_ref')}}
    job = m9.submit('serve_reader', params, host, principal_id, lawful_ref, timeout=90)
    if job['status'] != 'running':
        residency.release(placement['entry_id'], f"dispatch refused: {job.get('reason')}")
    annotate_model(model_id, {'serving': {'job_id': job['job_id'], 'host': host, 'port': port, 'gpu_index': gpu_index, 'started_at': m9.now(), 'status': job['status'], 'started_by': principal_id, 'residency_entry_id': placement['entry_id']}},
                   authority_source=f'WP-A2 contained reader start by {principal_id} · residency entry {placement["entry_id"]} · registry v{n}')
    residency.db().residency_register.update_one({'entry_id': placement['entry_id']}, {'$set': {'owner.job_id': job['job_id']}})
    return {'job': job, 'entry': _entry(model_id), 'placement': placement, 'already_running': False}


def status(model_id=MODEL_ID):
    try: entry = _entry(model_id)
    except ReaderUnavailable as exc: return {'model_id': model_id, 'status': 'not_registered', 'reason': str(exc)}
    job = _job(entry)
    if not job: return {'model_id': model_id, 'status': 'not_serving', 'entry': entry}
    if job['status'] != 'running': return {'model_id': model_id, 'status': 'not_serving', 'job': {k: job.get(k) for k in ('job_id', 'status', 'reason', 'finished_at', 'worker_log_tail')}, 'remote_state': job.get('remote_state'), 'entry': entry}
    return {'model_id': model_id, 'status': 'running', 'job': {k: job.get(k) for k in ('job_id', 'status', 'host', 'started_at')}, 'remote_state': (job.get('remote_state') or {}).get('progress'), 'entry': entry}


def _running(model_id=MODEL_ID):
    entry = _entry(model_id); job = _job(entry)
    if not job or job['status'] != 'running': raise ReaderUnavailable(f'{model_id} is not serving' + (f" (job {job['status']}: {job.get('reason') or ''})" if job else ''))
    return entry, job, int(entry['serving']['port'])


def _get(path, model_id=MODEL_ID, timeout=60):
    entry, job, port = _running(model_id)
    result = serving._remote(job['host'], f"curl -s -m {timeout} http://127.0.0.1:{port}{path}", purpose=f'contained_reader{path.replace("/", "_")}', timeout=timeout + 15)
    try: return json.loads(result.stdout_redacted.strip()), result.receipt_id
    except ValueError as exc: raise ReaderUnavailable(f'no response from the reader loopback server ({result.stderr_redacted[:120]})') from exc


def health(model_id=MODEL_ID):
    body, receipt = _get('/health', model_id); return {**body, 'receipt_id': receipt}


def egress_probe(model_id=MODEL_ID):
    body, receipt = _get('/egress_probe', model_id); return {**body, 'receipt_id': receipt}


def read(text, categories, purpose, model_id=MODEL_ID, timeout=240):
    """One bounded, request-scoped reading inside the perimeter. Refuses (never falls back) when the reader is unavailable or the reading is unsafe."""
    entry, job, port = _running(model_id)
    clean = str(text or '')[:MAX_CHARS]
    if not clean.strip(): raise ValueError('TEXT_REQUIRED')
    payload = base64.b64encode(json.dumps({'text': clean, 'categories': [{'name': c['name'], 'description': (c.get('description') or '')[:200]} for c in categories][:60]}, ensure_ascii=False).encode()).decode()
    command = f"echo {payload} | base64 -d | curl -s -m {timeout} -o /tmp/.akki_rd_$$ -w '%{{http_code}}' -X POST -H 'Content-Type: application/json' --data-binary @- http://127.0.0.1:{port}/read; echo; cat /tmp/.akki_rd_$$; rm -f /tmp/.akki_rd_$$"
    result = serving._remote(job['host'], command, purpose=f'contained_reader_read:{purpose}', timeout=timeout + 30)
    code, _, body_text = result.stdout_redacted.strip().partition('\n')
    try: body = json.loads(body_text.strip())
    except ValueError as exc: raise ReaderUnavailable('unreadable response from the reader') from exc
    http = int(code) if code.strip().isdigit() else None
    if http == 403: raise ReaderUnavailable('reader authority revoked: ' + json.dumps(body.get('revocation')))
    if http != 200: raise ReaderUnavailable(f'reader refused the reading ({http}): {body.get("refused") or body.get("error")} {body.get("problems") or ""}')
    if (entry.get('serving') or {}).get('residency_entry_id'): residency.touch_lease(entry['serving']['residency_entry_id'])
    return {'reading': body['reading'], 'seconds': body.get('seconds'), 'lineage': body.get('lineage'), 'receipt_id': result.receipt_id, 'chars': len(clean)}


def revoke(reason, principal_id, model_id=MODEL_ID):
    """Revoke the serving authority on the host and prove the next read is refused; the registry records it by new entry."""
    entry, job, port = _running(model_id)
    receipt = serving._write_marker(job, 'revoked.json', {'reason': reason, 'by': principal_id, 'at': m9.now(), 'model_id': model_id})
    try:
        read('synthetic probe after revocation', [], 'revocation_probe', model_id); refused = False
    except ReaderUnavailable as exc:
        refused = 'revoked' in str(exc)
    annotate_model(model_id, {'serving': {**entry['serving'], 'status': 'revoked', 'revoked_at': m9.now(), 'revoked_reason': reason}}, authority_source=f'WP-A2 reader authority revoked by {principal_id}: {reason}')
    return {'model_id': model_id, 'revocation_receipt_id': receipt, 'refused_after_revocation': refused}


def stop(reason, principal_id, model_id=MODEL_ID):
    entry, job, port = _running(model_id)
    receipt = serving._write_marker(job, 'stop.json', {'reason': reason, 'by': principal_id, 'at': m9.now()})
    import time
    for _ in range(20):
        time.sleep(3); job = m9.refresh(job['job_id'])
        if job['status'] != 'running': break
    annotate_model(model_id, {'serving': {**entry['serving'], 'status': job['status'], 'stopped_at': m9.now(), 'stop_reason': reason}}, authority_source=f'WP-A2 reader stop by {principal_id}: {reason}')
    rid = (entry.get('serving') or {}).get('residency_entry_id')
    if rid:
        try: residency.release(rid, f'reader stopped: {reason}')
        except LookupError: pass
    return {'model_id': model_id, 'job': {k: job.get(k) for k in ('job_id', 'status', 'finished_at')}, 'stop_receipt_id': receipt}


__all__ = ['ReaderUnavailable', 'start', 'status', 'health', 'egress_probe', 'read', 'revoke', 'stop', 'attest_model']
