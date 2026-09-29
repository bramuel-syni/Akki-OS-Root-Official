"""Offline tests of the Estate Intelligence worker's pure measurement (synthetic rows, no estate, no MySQL)
and of the report builder that turns aggregates into the estate-handling brief."""
import json
import random

from services.census_autonomy import estate_intelligence_worker as w
from services.census_autonomy import estate_intelligence_report as r

TABLE = {'engine': 'InnoDB', 'rows_estimate': 1000, 'data_bytes': 65536, 'index_bytes': 16384, 'created': None, 'updated': None, 'collation': None,
         'columns': [{'name': 'id', 'type': 'int', 'max_length': None, 'nullable': False, 'key': 'PRI', 'extra': ''},
                     {'name': 'email', 'type': 'varchar', 'max_length': 255, 'nullable': True, 'key': '', 'extra': ''},
                     {'name': 'body', 'type': 'text', 'max_length': None, 'nullable': True, 'key': '', 'extra': ''},
                     {'name': 'amount', 'type': 'decimal', 'max_length': None, 'nullable': True, 'key': '', 'extra': ''},
                     {'name': 'created_at', 'type': 'datetime', 'max_length': None, 'nullable': True, 'key': '', 'extra': ''},
                     {'name': 'user_id', 'type': 'int', 'max_length': None, 'nullable': True, 'key': '', 'extra': ''}],
         'indexes': {'PRIMARY': {'columns': ['id'], 'unique': True}, 'ix_user': {'columns': ['user_id'], 'unique': False},
                     'ix_user_created': {'columns': ['user_id', 'created_at'], 'unique': False}}}
NAMES = [c['name'] for c in TABLE['columns']]


def _rows(n=1000):
    random.seed(7)
    previous = None
    for i in range(n):
        row = (i, f'user{i // 3}@example.com' if i % 4 else None, ('lorem ipsum dolor sit amet ' * 6) if i % 3 == 0 else 'N/A',
               random.random() * 100 if i % 5 else 0, f'2026-0{1 + i % 9}-1{i % 9} 10:00:00', (i % 97) if i % 2 else None)
        if i % 50 == 0 and previous:
            row = (i,) + previous[1:]
        previous = row
        yield row


def test_table_measure_counts_duplicates_nulls_degradation_and_pii_without_retaining_values():
    measure = w.TableMeasure('t', TABLE, TABLE['columns'][0])
    for row in _rows():
        measure.observe(row, NAMES)
    result = measure.result('complete')
    assert result['rows_measured'] == 1000
    assert 0.015 <= result['exact_duplicate_ratio'] <= 0.08           # one in fifty rows repeats the previous row, plus cyclic coincidences
    assert result['null_bearing_row_ratio'] > 0.4                     # user_id null on every even row
    assert result['degraded_row_ratio'] > 0.6                         # 'N/A' placeholder on two rows in three
    assert result['pii_kinds'] == {'pii.email': 750} and result['pii_row_ratio'] == 0.75
    assert result['columns']['id']['distinct_ratio'] == 1.0
    assert result['columns']['user_id']['null_ratio'] == 0.5
    assert result['freshness']['latest_write'].startswith('2026-09')
    text = json.dumps(result)
    assert 'example.com' not in text and 'lorem' not in text          # aggregates only: no row value survives


def test_kmv_sketch_estimates_cardinality_in_constant_memory():
    sketch = w.KMV()
    for i in range(50_000):
        sketch.add(w.h64(str(i)))
    assert len(sketch.values) == sketch.k
    assert 40_000 <= sketch.estimate() <= 60_000


def test_select_list_bounds_long_text_and_binary_columns_only():
    parts = w.select_list(TABLE['columns'])
    assert 'LEFT(`body`, 1000) AS `body`' in parts and '`email`' in parts and 'LEFT(`email`' not in parts


def test_redundant_index_detection_names_the_covering_index():
    assert w.redundant_indexes(TABLE['indexes']) == [{'index': 'ix_user', 'covered_by': 'ix_user_created'}]


def _detail():
    measure = w.TableMeasure('payments', TABLE, TABLE['columns'][0])
    for row in _rows():
        measure.observe(row, NAMES)
    metrics = measure.result('complete')
    metrics.update(rows_estimate=1000, data_bytes=65536, index_bytes=16384, engine='InnoDB', column_count=6, created=None, updated=None,
                   schema_fingerprint='abcd', column_names_fingerprint='ef01', index_count=3, redundant_indexes=w.redundant_indexes(TABLE['indexes']),
                   has_timestamp_columns=True, primary_key='id', referential_integrity={})
    empty = {'rows_measured': 0, 'method': 'complete', 'rows_estimate': 0, 'data_bytes': 16384, 'index_bytes': 0, 'engine': 'InnoDB', 'column_count': 2,
             'schema_fingerprint': 'zz', 'column_names_fingerprint': 'zz', 'index_count': 0, 'redundant_indexes': [], 'has_timestamp_columns': False}
    failed = {'rows_measured': 0, 'method': 'failed', 'reason_code': 'BUDGET_MEMORY', 'rows_estimate': 5, 'data_bytes': 1, 'index_bytes': 0}
    return {'databases': [{'connection': 'c1', 'database': 'shop', 'tables': {'payments': metrics, 'scratch': empty, 'huge': failed}, 'errors': [], 'statements': 9,
                           'rows_fetched': 1000, 'wall_seconds': 1.0}]}


def test_report_build_grades_databases_infers_dimensions_and_ranks_products_and_strategies():
    job = {'job_id': 'eij-0123456789ab', 'status': 'partial', 'finished_at': '2026-09-29T00:00:00Z',
           'receipt': {'result': {'errors': [{'connection': 'c2', 'code': 'PULL_SEAM_WORKER_FAILED:rc=137'}]}}}
    report = r.build(job, _detail())
    headline = report['headline']
    assert headline['tables'] == 3 and headline['tables_measured'] == 1 and headline['failed_tables'] == 1 and headline['empty_tables'] == 1
    assert headline['blocked_connections'] == ['c2'] and headline['pii_pct'] == 75.0
    profile = report['databases'][0]
    assert profile['readiness']['grade'] in 'ABCDE' and {'time', 'money', 'entity', 'identity'} <= set(profile['dimensions'])
    titles = [p['title'] for p in report['data_products']]
    assert 'Transaction & revenue analytics' in titles
    assert any('de-identify' in b for b in report['data_products'][0]['blockers'])
    strategies = report['cost_strategies']['items']
    assert strategies[0]['bytes'] >= strategies[-1]['bytes']
    assert any(s['key'] == 'redundant_indexes' and s['bytes'] > 0 for s in strategies)
    assert report['row_values_retained'] is False
    compact = r.compact(report)
    assert compact['job_id'] == 'eij-0123456789ab' and compact['data_products'][0]['title'] in titles
    markdown = r.render_markdown(report)
    assert '## What the data can do' in markdown and '## Strategies to reduce cost' in markdown and 'example.com' not in markdown
