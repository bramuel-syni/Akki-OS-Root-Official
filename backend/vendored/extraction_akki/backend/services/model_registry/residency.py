"""Residency register — what lives on a GPU or on host storage, in which class, under which terms of reference (owner D7, OWNER_ORDERS §12).

Owner: "there needs to be a clear structure of what data/agents are we storing in GPU and for how long — if it's data needed for an active
run, what are the TORs for that; if it's for an admitted model, should it be stored … to save cost and free up capacity … reuse or
realtime no-data-movement pull seam has a play here." This module is that structure: a closed set of residency classes, each with terms of
reference; a register of placements (Mongo `residency_register`); a measured snapshot of both hosts through the sealed SSH seam; attribution
of every resident process to a known job or a finding; and a placement check that refuses anything a TOR forbids — above all eviction of a
running lane. It records and refuses; it never moves or deletes anything."""
import re
import uuid

from services.training_lab import store as lab

MIB = 1024 * 1024
DEFAULT_HEADROOM_MIB = 8192
TRAINING_PHASES = frozenset({'train', 'pipeline', 'calibrate', 'compare_optimizers', 'lab_train_music', 'malpha_listener_train', 'malpha_story_text_train', 'malpha_voice_train', 'malpha_aip_build', 'malpha_aip_reseal', 'malpha_aip_requalify', 'malpha_aip_relabel', 'malpha_evaluate', 'malpha_baseline_render', 'lab_classify_estate', 'lab_text_lid'})
SERVING_PHASES = frozenset({'serve', 'serve_reader'})

CLASSES = {
    'active_run_data': {'where': 'gpu+host_disk', 'tor': "Resident for the owning run's lease only: PCM/codec codes/segments the lane reads, optimizer and model state. Released on completion or fault. Never copied off the estate. The next iteration of the same lane reuses the prepared material in place (reuse pointer), it is not moved.",
                        'release': 'on run completion or fault', 'coresidence': 'exclusive on its GPU (one reserved visible GPU per training run)', 'idle_resident': False},
    'checkpoint': {'where': 'host_disk', 'tor': 'Per-iteration adapters stay on host disk: last-good and the current candidate are retained; the admitted artefact is copied to the registry path; the rest are pruned by rule. A checkpoint is never resident on a GPU between runs.',
                   'release': 'pruned by rule after admission or supersession', 'coresidence': 'n/a (disk)', 'idle_resident': False},
    'admitted_model': {'where': 'host_disk/cpu', 'tor': 'Admitted weights live on host disk (or CPU memory when warm). They are pulled to a GPU only under a serving demand lease or a training order, and are never resident idle on a GPU — capacity is freed for lanes.',
                       'release': 'after the demand lease lapses', 'coresidence': 'as serving_resident only', 'idle_resident': False},
    'serving_resident': {'where': 'gpu', 'tor': 'Resident while a demand lease exists; the lease is renewed by requests and lapses after the recorded idle period, after which the control-plane tick stops the server (WP-C1 applies the stop). May co-reside with other residents when the measured free memory fits it with headroom; never evicts a running lane.',
                         'release': 'stop when the demand lease lapses', 'coresidence': 'allowed when measured free memory fits (no eviction)', 'idle_resident': False},
    'derived_register': {'where': 'host_disk', 'tor': 'AIP learned character register: host disk under its custody partition, written only through the character-register write boundary, reuse-first, no organic (anatomical) columns, lineage on every read.',
                         'release': 'superseded by a later register version; never deleted silently', 'coresidence': 'n/a (disk)', 'idle_resident': False},
    'raw_material': {'where': 'host_disk', 'tor': 'Raw PCM and per-segment organic measurements: host disk under the raw_material partition with its own manifest; read with lineage; never leaves the estate; temporary speaker representations destroyed after use.',
                     'release': 'retention per custody class; archive is not deletion', 'coresidence': 'n/a (disk)', 'idle_resident': False},
}
SMI_DEVICES = "nvidia-smi --query-gpu=index,uuid,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits"
SMI_APPS = "nvidia-smi --query-compute-apps=pid,used_memory,gpu_uuid --format=csv,noheader,nounits"


class PlacementRefused(ValueError):
    """A placement that a term of reference forbids (eviction, idle residency, exclusivity)."""


def db():
    database = lab.db()
    database.residency_register.create_index([('host', 1), ('gpu_index', 1), ('status', 1)])
    return database


def now():
    return lab.now()


def terms():
    return {name: dict(spec) for name, spec in CLASSES.items()}


# ----------------------------------------------------------------------------- measured snapshot (sealed SSH seam; honest gaps, never fabricated)
def snapshot(hosts=None):
    from services.training_runner import m9_dispatch as m9
    from services.training_runner.ssh_seam import execute_remote_command
    out = {'at': now(), 'devices': [], 'gaps': [], 'receipts': []}
    for host in hosts or m9.hosts():
        result = execute_remote_command(host, f"{SMI_DEVICES}; echo __APPS__; {SMI_APPS}", purpose='residency_snapshot', timeout=30)
        out['receipts'].append(result.receipt_id)
        if result.rc != 0:
            out['gaps'].append({'host': host, 'reason': result.stderr_redacted[:200] or 'unreachable'}); continue
        devices_text, _, apps_text = result.stdout_redacted.partition('__APPS__')
        by_uuid = {}
        for line in devices_text.strip().splitlines():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 5 or not parts[0].isdigit(): continue
            dev = {'host': host, 'gpu_index': int(parts[0]), 'uuid': parts[1], 'used_mib': int(float(parts[2])), 'total_mib': int(float(parts[3])), 'utilization_pct': int(float(parts[4])) if re.fullmatch(r'[\d.]+', parts[4]) else None, 'processes': []}
            by_uuid[dev['uuid']] = dev; out['devices'].append(dev)
        for line in apps_text.strip().splitlines():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 3 or not parts[0].isdigit(): continue
            dev = by_uuid.get(parts[2])
            if dev: dev['processes'].append({'pid': int(parts[0]), 'used_mib': int(float(parts[1])) if re.fullmatch(r'[\d.]+', parts[1]) else None})
    return out


def _running_jobs():
    from services.training_runner import m9_dispatch as m9
    return [j for j in m9.list_jobs() if j.get('status') == 'running']


def attribute(snap, jobs):
    """Every resident process → a known job and residency class, or a finding. Nothing is adopted silently."""
    by_pid = {(j['host'], int((j.get('remote') or {}).get('pid') or 0)): j for j in jobs}
    residents, findings = [], []
    for dev in snap['devices']:
        for proc in dev['processes']:
            job = by_pid.get((dev['host'], proc['pid']))
            if job is None:
                findings.append({'kind': 'unaccounted_resident', 'host': dev['host'], 'gpu_index': dev['gpu_index'], 'pid': proc['pid'], 'used_mib': proc['used_mib'], 'note': 'no running job records this pid (a worker subprocess, a stale server or foreign work); not adopted into the register'})
                continue
            phase = job.get('phase', '')
            cls = 'serving_resident' if phase in SERVING_PHASES else 'active_run_data' if phase in TRAINING_PHASES or phase.startswith('malpha_') or phase.startswith('lab_') else None
            if cls is None:
                findings.append({'kind': 'unclassified_phase', 'host': dev['host'], 'gpu_index': dev['gpu_index'], 'pid': proc['pid'], 'job_id': job['job_id'], 'phase': phase}); continue
            residents.append({'host': dev['host'], 'gpu_index': dev['gpu_index'], 'pid': proc['pid'], 'used_mib': proc['used_mib'], 'job_id': job['job_id'], 'phase': phase, 'class': cls, 'tor': CLASSES[cls]['tor'], 'release': CLASSES[cls]['release']})
    for dev in snap['devices']:
        if not dev['processes'] and dev['used_mib'] > 1024:
            findings.append({'kind': 'memory_without_process', 'host': dev['host'], 'gpu_index': dev['gpu_index'], 'used_mib': dev['used_mib'], 'note': 'memory in use but no compute process listed (container or driver context); reported, not attributed'})
    return residents, findings


# ----------------------------------------------------------------------------- placements (recorded; refused when a TOR forbids them)
def place(cls, host, gpu_index, bytes_needed, owner, reason, *, lease=None, snap=None, jobs=None, headroom_mib=DEFAULT_HEADROOM_MIB, reuse_pointer=None):
    if cls not in CLASSES: raise PlacementRefused(f'unknown residency class {cls!r}')
    spec = CLASSES[cls]
    if spec['where'] != 'gpu' and cls != 'active_run_data': raise PlacementRefused(f'{cls} is a host-storage class ({spec["where"]}); it is not placed on a GPU')
    if cls == 'serving_resident' and not (lease and lease.get('kind') == 'demand'): raise PlacementRefused('a serving resident needs a demand lease (renewed by requests, lapses when idle); without one it would be an idle resident, which the TOR forbids')
    snap = snap or snapshot([host]); jobs = _running_jobs() if jobs is None else jobs
    dev = next((d for d in snap['devices'] if d['host'] == host and d['gpu_index'] == gpu_index), None)
    if dev is None: raise PlacementRefused(f'{host} GPU {gpu_index} is not in the measured snapshot (gaps: {snap.get("gaps")}) — no placement without a measurement')
    residents, _ = attribute(snap, jobs)
    here = [r for r in residents if r['host'] == host and r['gpu_index'] == gpu_index]
    if cls == 'active_run_data' and (here or dev['processes']): raise PlacementRefused(f'a training run needs its GPU exclusively; {host} GPU {gpu_index} already carries {len(dev["processes"])} resident process(es)')
    need_mib = int(bytes_needed // MIB) + headroom_mib; free_mib = dev['total_mib'] - dev['used_mib']
    if need_mib > free_mib: raise PlacementRefused(f'{host} GPU {gpu_index} has {free_mib} MiB free; {need_mib} MiB needed with headroom — placement would require evicting a resident, which no TOR permits')
    entry = {'entry_id': 'res-' + uuid.uuid4().hex[:10], 'at': now(), 'class': cls, 'tor': spec['tor'], 'release': spec['release'], 'host': host, 'gpu_index': gpu_index, 'device_uuid': dev.get('uuid'), 'bytes': int(bytes_needed), 'owner': owner, 'reason': reason, 'lease': lease,
             'reuse_pointer': reuse_pointer, 'measured': {'free_mib_before': free_mib, 'used_mib_before': dev['used_mib'], 'total_mib': dev['total_mib'], 'coresidents': [{k: r[k] for k in ('job_id', 'phase', 'class', 'used_mib')} for r in here], 'snapshot_at': snap['at'], 'receipts': snap.get('receipts', [])},
             'status': 'placed', 'last_verified': now()}
    db().residency_register.insert_one(dict(entry)); return entry


def touch_lease(entry_id):
    return db().residency_register.update_one({'entry_id': entry_id, 'status': 'placed'}, {'$set': {'lease.last_demand_at': now()}}).matched_count


def release(entry_id, reason):
    doc = db().residency_register.find_one_and_update({'entry_id': entry_id, 'status': 'placed'}, {'$set': {'status': 'released', 'released_at': now(), 'release_reason': reason}}, return_document=True)
    if not doc: raise LookupError('no placed entry with that id')
    doc.pop('_id', None); return doc


def entries(status=None):
    query = {'status': status} if status else {}
    return list(db().residency_register.find(query, {'_id': 0}).sort('at', -1).limit(200))


def reconcile(snap=None, jobs=None):
    """Measured residents vs the register: unaccounted residents and placed entries without a live process are findings, never silently adopted or dropped."""
    snap = snap or snapshot(); jobs = _running_jobs() if jobs is None else jobs
    residents, findings = attribute(snap, jobs)
    placed = entries('placed')
    for e in placed:
        owner_job = (e.get('owner') or {}).get('job_id')
        live = any(r['job_id'] == owner_job for r in residents) if owner_job else None
        if owner_job and not live: findings.append({'kind': 'placed_without_live_process', 'entry_id': e['entry_id'], 'class': e['class'], 'host': e['host'], 'gpu_index': e['gpu_index'], 'job_id': owner_job, 'note': 'the register says placed but no resident process carries this job; release it or re-verify'})
    return {'at': snap['at'], 'devices': snap['devices'], 'gaps': snap.get('gaps', []), 'residents': residents, 'findings': findings, 'placed_entries': placed, 'terms': terms()}
