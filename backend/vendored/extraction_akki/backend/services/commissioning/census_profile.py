"""Read the measured census profile of a source; the first-scope rule is applied here, never guessed."""
import asyncio
import json
import time
from services.census_autonomy.operational_scope import SOURCE_TENANTS
from services.extraction_runtime.units import personal_columns

_CACHE = {}
TTL = 600


def _load(tenant, source_id):
    from services.census_autonomy.registry_durability import collection
    coll = collection()
    best, best_at = None, ''
    for doc in coll.find({'asset_ref': {'$regex': f'^census-result:{tenant}:'}}, {'census_evidence.raw_json': 1, 'asset_ref': 1}):
        raw = doc.get('census_evidence', {}).get('raw_json')
        if not raw or source_id not in raw or '"per_table"' not in raw:
            continue
        value = json.loads(raw)
        for outcome in value.get('payload', {}).get('outcomes', []):
            if outcome.get('source_id') != source_id:
                continue
            for source in outcome.get('sources', []):
                per_table = (source.get('composition') or {}).get('per_table')
                if per_table and outcome.get('observed_at', '') >= best_at:
                    best, best_at = (value['census_run_id'], outcome, source), outcome.get('observed_at', '')
    return best


def _tables(entry):
    census_run_id, outcome, source = entry
    rows = []
    for key, table in source['composition']['per_table'].items():
        database, _, name = key.partition('.')
        columns = table.get('columns') or []
        signals = table.get('role_signals') or []
        pk = [c['column_name'] for c in columns if c.get('column_key') == 'PRI']
        rows.append({'census_run_id': census_run_id, 'observed_at': outcome.get('observed_at'), 'source_ref': source['source_ref'],
                     'label': source.get('label'), 'database': database, 'table': name, 'row_count': int(table.get('row_count') or 0),
                     'column_count': int(table.get('column_count') or len(columns)), 'columns': [c['column_name'] for c in columns],
                     'column_types': {c['column_name']: c.get('data_type') for c in columns}, 'role_signals': signals,
                     'primary_key': pk[0] if len(pk) == 1 else None, 'personal_columns': personal_columns(columns, signals),
                     'data_length_bytes': int(table.get('data_length_bytes') or 0)})
    return rows


async def tables_for(tenant, source_id):
    if SOURCE_TENANTS.get(source_id) != tenant:
        return None
    cached = _CACHE.get((tenant, source_id))
    if cached and cached[0] > time.time():
        return cached[1]
    entry = await asyncio.to_thread(_load, tenant, source_id)
    rows = _tables(entry) if entry else []
    _CACHE[(tenant, source_id)] = (time.time() + TTL, rows)
    return rows


def find_table(rows, database, table):
    return next((r for r in rows if r['database'] == database and r['table'] == table), None)


def first_scope(rows):
    """Rule: smallest personal-data-clean, keyed, non-empty unit of a censused source. Basis is returned with it."""
    eligible = [r for r in rows if r['row_count'] > 0 and not r['personal_columns'] and r['primary_key']
                and r['database'].lower() not in ('mysql', 'information_schema', 'performance_schema', 'sys')]
    if not eligible:
        return None, 'No censused table satisfies the first-scope rule (non-empty, keyed, personal-data-clean).'
    chosen = sorted(eligible, key=lambda r: (r['row_count'], r['column_count'], r['database'], r['table']))[0]
    basis = (f"first-scope rule: smallest personal-data-clean keyed table among {len(eligible)} eligible of {len(rows)} censused "
             f"(census {chosen['census_run_id']} observed {chosen['observed_at']}); chosen {chosen['database']}.{chosen['table']} "
             f"rows={chosen['row_count']} columns={chosen['column_count']} pk={chosen['primary_key']}")
    return chosen, basis
