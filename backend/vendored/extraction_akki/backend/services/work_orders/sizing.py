"""Sizing: the frozen request's scale against the kind's scaling unit → a compute reservation.

The Coordinator sizes every work order for CPU or GPU before it reserves; the KindProfile tells it
which. The first estimate is the profile's declared prior; every settled run records actual seconds
per unit on the ledger, and later estimates are read from that record. Reservations are upper bounds.
"""
import math
import statistics
from services.extraction_runtime.objects import RESOURCE as OBJECTS
from services.ledger_writer.principal_control import read_events
from services.work_orders.kind_profiles import CLASS_UNIT

SAFETY = 3
MIN_RUNS_FOR_RECORD = 1


async def history_for(db, tenant, job_kind):
    """Measured seconds per scaling unit, per compute class, from settled runs of this kind."""
    samples = {}
    for event in await read_events(db, {'row.tenant_id': tenant, 'row.resource_type': OBJECTS}):
        settlement = event['payload'].get('sizing_settlement')
        if not settlement or settlement.get('job_kind') != job_kind:
            continue
        for cls, actual in settlement.get('actual', {}).items():
            if actual.get('scale') and actual.get('seconds') is not None:
                samples.setdefault(cls, []).append(float(actual['seconds']) / float(actual['scale']))
    return {cls: {'seconds_per_unit': statistics.median(values), 'runs': len(values)}
            for cls, values in samples.items() if len(values) >= MIN_RUNS_FOR_RECORD}


def size(profile, bounds, history=None):
    history = history or {}
    scale = profile.scale(bounds)
    classes, basis = {}, []
    for cls, unit in profile.scaling.items():
        if scale[unit] <= 0:
            basis.append(f'{cls}: scale in {unit} is 0, class dropped from the reservation')
            continue
        prior = profile.sizing_rates[cls]
        observed = history.get(cls)
        rate = observed['seconds_per_unit'] if observed else float(prior['seconds_per_unit'])
        estimate = float(prior['overhead_seconds']) + scale[unit] * rate
        classes[cls] = {'unit': CLASS_UNIT[cls], 'scaling_unit': unit, 'scale': scale[unit],
                        'seconds_per_unit': rate, 'rate_basis': f"measured record ({observed['runs']} settled run(s))" if observed
                        else profile.extra.get('sizing_rate_status', 'declared_prior'),
                        'estimate_seconds': round(estimate, 3), 'reservation_seconds': int(math.ceil(estimate * SAFETY)),
                        'memory_gb': prior['memory_gb']}
        basis.append(f"{cls}: {scale[unit]} {unit} × {rate:g} s/unit + {prior['overhead_seconds']} s overhead "
                     f"= {estimate:.1f} s ({classes[cls]['rate_basis']}); reserved ×{SAFETY}")
    if not classes:
        raise ValueError('SIZING_HAS_NO_COMPUTE_CLASS')
    wall = sum(c['estimate_seconds'] for c in classes.values())
    return {'compute_class': profile.compute_class, 'classes': classes,
            'wall_clock_estimate_seconds': round(wall, 3), 'fits_wall_clock_bound': wall <= int(bounds['max_seconds']),
            'needs': {'cpu_cores': 1 if 'cpu' in classes else 0, 'gpu_count': 1 if 'gpu' in classes else 0,
                      'memory_gb': max(c['memory_gb'] for c in classes.values())},
            'basis': '; '.join(basis)}


def settlement(job_kind, sizing, quantities, scale_actual):
    """Actual against reservation, per class, from the runtime's own signed measurements."""
    actual = {}
    for cls, planned in sizing['classes'].items():
        measured = next((q for q in quantities if q['dimension'] == 'active_compute' and q['unit'] == planned['unit']), None)
        if measured is None:
            continue
        actual[cls] = {'seconds': float(measured['quantity']), 'reserved_seconds': planned['reservation_seconds'],
                       'estimate_seconds': planned['estimate_seconds'],
                       'scale': scale_actual.get(planned['scaling_unit']), 'scaling_unit': planned['scaling_unit']}
    return {'job_kind': job_kind, 'estimate': sizing, 'actual': actual}
