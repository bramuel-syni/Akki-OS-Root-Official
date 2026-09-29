"""Admitted runtime descriptors: dispatch selects by descriptor, never by address.

A descriptor names the roles a runtime may hold, its transport seam, the kinds it executes, the
dimensions it enforces, the sources it reaches, and its compute classes with their capacity.
Selection is class-matched with headroom: a GPU job never lands on a CPU-only runtime, and a CPU
job never occupies a GPU runtime while a CPU-only runtime is free. The two hosts attested first are
the first descriptors, not the runtime.
"""
import time
from services.estate_admission.records import latest
from services.ledger_writer.principal_control import read_events
from services.northena.execution_models import Held

ROLES = ('worker', 'inspector', 'custodian')
CLASSES = ('cpu', 'gpu')
REQUIRED = {'runtime_id', 'principal_id', 'key_id', 'roles', 'transport', 'python', 'state_dir', 'kinds',
            'enforced_dimensions', 'executor_version', 'reach', 'status', 'compute_classes', 'capacity'}
CAPACITY = ('cpu_cores', 'gpu_count', 'memory_gb')


def descriptor_valid(record):
    if not REQUIRED <= set(record) or not set(record['roles']) <= set(ROLES):
        raise ValueError('Incomplete admitted runtime descriptor.')
    if record['transport'].get('kind') not in ('ssh_seam', 'jump'):
        raise ValueError('A runtime transport must be an admitted remote seam; E1 is never the data path.')
    if not record['compute_classes'] or not set(record['compute_classes']) <= set(CLASSES):
        raise ValueError('A runtime without a compute class is not routable.')
    if not set(CAPACITY) <= set(record['capacity']):
        raise ValueError('A runtime must declare its capacity per compute class.')
    return record


async def admitted_runtimes(db, tenant):
    current = await latest(db, tenant, 'admitted_runtime')
    return {rid: descriptor_valid(event['payload']['record']) for rid, event in current.items()}


def reaches(descriptor, units):
    reach = descriptor['reach']
    return all(u in reach.get('direct', []) or u in reach.get('pull_seam', []) for u in units)


async def in_flight(db, tenant):
    """Sizing needs of work orders on each runtime that have neither closed nor passed their deadline."""
    from services.extraction_runtime.objects import RESOURCE as OBJECTS
    from services.work_orders.packaging import RESOURCE as ORDERS
    closed = {e['row']['run_id'] for e in await read_events(db, {'row.tenant_id': tenant, 'row.resource_type': OBJECTS})
              if e['payload'].get('state') in ('complete', 'failed', 'cancelled')}
    load = {}
    now = time.time()
    for event in await read_events(db, {'row.tenant_id': tenant, 'row.resource_type': ORDERS}):
        order = event['payload']['order']
        if event['row']['run_id'] in closed or order.get('deadline_epoch', 0) <= now:
            continue
        needs = (order.get('sizing') or {}).get('needs', {})
        bucket = load.setdefault(order['worker_runtime_id'], {k: 0 for k in CAPACITY})
        for key in CAPACITY:
            bucket[key] += needs.get(key, 0)
    return load


def headroom(descriptor, used, needs):
    return all(used.get(k, 0) + needs.get(k, 0) <= descriptor['capacity'][k] for k in CAPACITY)


async def select(db, tenant, role, kind, units, exclude=(), sizing=None):
    """Deterministic, class-matched selection with headroom; the basis is recorded, not inferred."""
    needed = set(sizing['classes']) if sizing else set()
    load = await in_flight(db, tenant) if sizing else {}
    candidates, refused = [], []
    for rid, d in sorted((await admitted_runtimes(db, tenant)).items()):
        if d['status'] != 'active' or role not in d['roles'] or kind not in d['kinds'] or rid in exclude:
            continue
        if not reaches(d, units):
            refused.append(f'{rid}: does not reach {list(units)}')
            continue
        classes = set(d['compute_classes'])
        if not needed <= classes:
            refused.append(f"{rid}: classes {sorted(classes)} lack {sorted(needed - classes)}")
            continue
        used = load.get(rid, {})
        if sizing and not headroom(d, used, sizing['needs']):
            refused.append(f"{rid}: no headroom (in flight {used}, needs {sizing['needs']}, capacity {d['capacity']})")
            continue
        exact = 0 if classes == needed or not needed else 1
        direct = 0 if all(u in d['reach'].get('direct', []) for u in units) else 1
        candidates.append(((exact, direct, rid), rid, d))
    if not candidates:
        raise Held('ADMITTED_RUNTIME_UNAVAILABLE_FOR_' + role.upper())
    key, rid, d = sorted(candidates, key=lambda c: c[0])[0]
    basis = (f"{role}: admitted runtime {rid} selected among {len(candidates)} candidate(s) "
             f"{'with exact class match ' + str(sorted(needed)) if needed and key[0] == 0 else 'as a superset-class runtime ' + str(sorted(d['compute_classes'])) if needed else 'by role'}; "
             f"reach {'direct' if key[1] == 0 else 'via pull seam'} for {list(units)}; "
             f"in flight before this order {load.get(rid, {k: 0 for k in CAPACITY})}; "
             + (f"refused: {refused}; " if refused else '') + (f"excluding {list(exclude)}" if exclude else 'no exclusions'))
    return d, basis


async def runtime_by_id(db, tenant, runtime_id):
    event = await latest(db, tenant, 'admitted_runtime', runtime_id)
    if event is None:
        raise Held('ADMITTED_RUNTIME_UNRESOLVED')
    return descriptor_valid(event['payload']['record'])
