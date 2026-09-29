"""Feasibility: one Registry-grounded verdict at admission — warm, unknown or refuse. Never a guess.

A warm verdict carries the bounded scope, the custody floor, the estimate and the compute sizing:
the frozen request's scale against the kind's scaling unit, priced in CPU- or GPU-seconds from the
declared prior or the measured record. The sizing becomes the Plan's active_compute reservation.
"""
from services.census_autonomy.operational_scope import SOURCE_TENANTS
from services.commissioning.census_profile import tables_for, find_table, first_scope
from services.work_orders import sizing as sizing_rules
from services.work_orders.kind_profiles import profile_for_operation


async def assess(db, tenant, envelope):
    operation, units = envelope['operation'], envelope['units']
    profile = profile_for_operation(operation)
    if profile is None:
        return {'verdict': 'refuse', 'reason_code': 'OPERATION_NOT_COMMISSIONABLE_HERE',
                'basis': f'{operation} has no admitted kind profile on this path; raw export or model work is not implied.'}
    if len(units) != 1 or SOURCE_TENANTS.get(units[0]) != tenant:
        return {'verdict': 'refuse', 'reason_code': 'SCOPE_NOT_ADMITTED', 'basis': 'Exactly one source admitted to this estate is required.'}
    rows = await tables_for(tenant, units[0])
    if not rows:
        return {'verdict': 'unknown', 'reason_code': 'SOURCE_NOT_CENSUSED', 'basis': 'The Registry holds no measured profile for this source yet.'}
    reach = envelope.get('reach') or {}
    assumed = []
    if reach.get('database') and reach.get('table'):
        table = find_table(rows, reach['database'], reach['table'])
        if table is None:
            return {'verdict': 'unknown', 'reason_code': 'TABLE_NOT_CENSUSED',
                    'basis': f"{reach['database']}.{reach['table']} is not in the measured census profile of {units[0]}."}
        basis = f"requested table {table['database']}.{table['table']} is in the census profile ({table['census_run_id']})"
    else:
        table, basis = first_scope(rows)
        if table is None:
            return {'verdict': 'refuse', 'reason_code': 'FIRST_SCOPE_RULE_UNSATISFIED', 'basis': basis}
        assumed.append('reach')
    if not table['primary_key']:
        return {'verdict': 'refuse', 'reason_code': 'TABLE_HAS_NO_SINGLE_PRIMARY_KEY', 'basis': basis}
    bounds = {**profile.default_bounds, **{k: v for k, v in (envelope.get('bounds') or {}).items() if v is not None}}
    bounds['estimated_row_bytes'] = max(64, min(4096, table['data_length_bytes'] // max(1, table['row_count'])))
    returned = min(table['row_count'], int(bounds['max_records']))
    history = await sizing_rules.history_for(db, tenant, profile.job_kind)
    sized = sizing_rules.size(profile, bounds, history)
    if not sized['fits_wall_clock_bound']:
        return {'verdict': 'refuse', 'reason_code': 'SIZING_EXCEEDS_WALL_CLOCK_BOUND',
                'basis': f"{sized['basis']}; estimate {sized['wall_clock_estimate_seconds']} s exceeds max_seconds {bounds['max_seconds']}"}
    return {'verdict': 'warm', 'reason_code': 'REGISTRY_MEMBERSHIP_MEASURED', 'basis': basis, 'assumed': assumed,
            'job_kind': profile.job_kind, 'table': table, 'floor': {'columns': table['personal_columns'], 'name': profile.custody_floor},
            'bounds': bounds, 'estimate': {'returned_records': returned, 'scanned_records': returned,
                                           'bytes_read': returned * bounds['estimated_row_bytes']},
            'sizing': sized, 'controlled': bool(table['personal_columns']) or operation != 'browse_estate'}
