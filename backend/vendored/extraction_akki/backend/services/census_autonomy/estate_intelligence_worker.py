"""Estate Intelligence census — measures duplication, quality, degradation, freshness, integrity,
PII density and storage economics across a relational estate. Census only: rows are read where the
estate is reachable (the jump host), measured in memory and discarded. Only aggregates, sketches and
hashes leave; no row, cell or identifier value is ever returned or written.

Two entry points:
  * ``jump_execute(control)`` — runs on the jump host for ONE database (pure Python + pymysql).
  * ``execute(control)`` — the detached worker of record on akki-vm: iterates connections/databases
    through the pull seam, checkpoints per database, rolls up the estate and writes the receipt.
"""
import bisect
import hashlib
import json
import os
import re
import shlex
import socket
import struct
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL = 'akki-estate-intelligence/1'
ROW_COMPLETE_MAX = 100_000
STRATA, STRATUM_ROWS, PAGE = 8, 5_000, 5_000
TEXT_SAMPLE_CAP, LONG_TEXT, FK_SAMPLE, SKETCH_K, MINHASH_K = 4_000, 120, 400, 256, 32
MEMORY_STOP_MB = 320  # the jump host has 769 MB and no swap; the kernel killed the first run at 470 MB RSS
SYSTEM_SCHEMAS = ('information_schema', 'performance_schema', 'mysql', 'sys')
PLACEHOLDERS = {'n/a', 'na', 'null', 'none', 'nil', 'undefined', '-', '--', '.', '?', 'test', 'testing', 'tbd',
                'unknown', '0000-00-00', '0000-00-00 00:00:00', 'lorem ipsum', 'asdf', 'xxx', 'x'}
MOJIBAKE = re.compile('Ã.|â€|Â|\ufffd')
EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$')
PHONE = re.compile(r'^\+?[0-9][0-9 \-()]{6,18}$')
URL = re.compile(r'^https?://\S+$')
DATEISH = re.compile(r'^\d{4}-\d{2}-\d{2}')
TIMESTAMP_TYPES = ('timestamp', 'datetime', 'date')
NUMERIC_TYPES = ('int', 'bigint', 'smallint', 'tinyint', 'mediumint', 'decimal', 'float', 'double')
TEXT_TYPES = ('varchar', 'char', 'text', 'mediumtext', 'longtext', 'tinytext', 'json', 'enum')
_PRIMES = [(0x9E3779B1 + 2 * i + 1, 0x85EBCA77 ^ (i * 0x27D4EB2F)) for i in range(MINHASH_K)]

JUMP_BOOTSTRAP = '''import sys,json,base64,tempfile,pathlib,hashlib
p=json.load(sys.stdin)
b=base64.b64decode(p.pop('bundle'))
if hashlib.sha256(b).hexdigest()!=p['code_sha256']: raise ValueError('CODE_HASH_MISMATCH')
with tempfile.TemporaryDirectory(prefix='akki-estate-intel-') as d:
 z=pathlib.Path(d)/'worker.zip'; z.write_bytes(b); sys.path.insert(0,str(z))
 from services.census_autonomy.estate_intelligence_worker import jump_execute
 print(json.dumps(jump_execute(p),sort_keys=True,default=str),flush=True)
'''


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def ident(value):
    if not value or not all(c.isalnum() or c in '_$' for c in value):
        raise ValueError('UNSAFE_IDENTIFIER')
    return '`' + value + '`'


def h64(text):
    return struct.unpack('<Q', hashlib.blake2b(text.encode('utf-8', 'surrogatepass'), digest_size=8).digest())[0]


# ----------------------------------------------------------------------------- jump-side measurement

class Bounded:
    """Read-only, bounded statements only. Every statement is guarded; none returns more than a page."""

    def __init__(self, connection, database, deadline):
        import pymysql
        self.deadline = deadline
        self.statements = 0
        self.rows_fetched = 0
        self.connection = pymysql.connect(host=connection['host'], port=int(connection['port']), user=connection['user'],
                                          password=connection['password'], database=database, connect_timeout=10,
                                          read_timeout=120, write_timeout=10, charset='utf8mb4', autocommit=True)
        with self.connection.cursor() as cursor:
            cursor.execute('SET SESSION TRANSACTION READ ONLY')
            cursor.execute('SET SESSION MAX_EXECUTION_TIME=120000')

    def query(self, sql, params=None, limit_required=True):
        return list(self.stream(sql, params, limit_required))

    def stream(self, sql, params=None, limit_required=True):
        """Unbuffered server-side cursor: one row in memory at a time (the jump host has 769 MB and no swap)."""
        import pymysql.cursors
        from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
        if time.time() >= self.deadline:
            raise TimeoutError('BUDGET_EXHAUSTED')
        guarded = refuse_if_write(sql)
        if limit_required and ' LIMIT ' not in guarded.upper():
            raise ValueError('READ_OUTSIDE_BOUNDED_METHOD')
        self.statements += 1
        with self.connection.cursor(pymysql.cursors.SSCursor) as cursor:
            cursor.execute(guarded, params)
            for row in cursor:
                self.rows_fetched += 1
                yield row

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass


def schema(db, database):
    tables = {}
    for name, engine, rows, data_len, index_len, created, updated, collation in db.query(
            'SELECT TABLE_NAME, ENGINE, TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH, CREATE_TIME, UPDATE_TIME, TABLE_COLLATION '
            'FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_TYPE=%s LIMIT 5000', (database, 'BASE TABLE')):
        tables[name] = {'engine': engine, 'rows_estimate': int(rows or 0), 'data_bytes': int(data_len or 0),
                        'index_bytes': int(index_len or 0), 'created': str(created) if created else None,
                        'updated': str(updated) if updated else None, 'collation': collation, 'columns': [], 'indexes': {}}
    for table, column, dtype, maxlen, nullable, key, extra, position in db.query(
            'SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_KEY, EXTRA, ORDINAL_POSITION '
            'FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s ORDER BY TABLE_NAME, ORDINAL_POSITION LIMIT 100000', (database,)):
        if table in tables:
            tables[table]['columns'].append({'name': column, 'type': (dtype or '').lower(), 'max_length': int(maxlen) if maxlen else None,
                                             'nullable': nullable == 'YES', 'key': key or '', 'extra': extra or ''})
    for table, index, seq, column, non_unique in db.query(
            'SELECT TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX, COLUMN_NAME, NON_UNIQUE FROM information_schema.STATISTICS '
            'WHERE TABLE_SCHEMA=%s ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX LIMIT 100000', (database,)):
        if table in tables:
            tables[table]['indexes'].setdefault(index, {'columns': [], 'unique': not non_unique})['columns'].append(column)
    return tables


def primary_key(table):
    keys = [c for c in table['columns'] if c['key'] == 'PRI']
    if len(keys) == 1 and (keys[0]['type'] in NUMERIC_TYPES or keys[0]['type'] in TEXT_TYPES):
        return keys[0]
    return None


def redundant_indexes(indexes):
    names = sorted(indexes)
    found = []
    for a in names:
        for b in names:
            if a != b and indexes[a]['columns'] != indexes[b]['columns'] and \
                    indexes[b]['columns'][:len(indexes[a]['columns'])] == indexes[a]['columns'] and not indexes[a]['unique']:
                found.append({'index': a, 'covered_by': b})
    return found


class MinHash:
    __slots__ = ('values',)

    def __init__(self):
        self.values = [0xFFFFFFFFFFFFFFFF] * MINHASH_K

    def add(self, shingles):
        for shingle in shingles:
            base = h64(shingle)
            for i, (a, b) in enumerate(_PRIMES):
                value = (a * base + b) & 0xFFFFFFFFFFFFFFFF
                if value < self.values[i]:
                    self.values[i] = value

    def band_keys(self, bands=8):
        width = MINHASH_K // bands
        return [hashlib.blake2b(struct.pack('<%dQ' % width, *self.values[i * width:(i + 1) * width]), digest_size=8).hexdigest()
                for i in range(bands)]


def shingles(text, k=5):
    text = re.sub(r'\s+', ' ', text.lower()).strip()
    if len(text) <= k:
        return {text}
    return {text[i:i + k] for i in range(0, len(text) - k + 1, 4)}


class KMV:
    """k-minimum-values cardinality sketch: constant memory per column instead of a distinct-value set."""
    __slots__ = ('values', 'k', 'seen')

    def __init__(self, k=256):
        self.values, self.k, self.seen = [], k, 0

    def add(self, value):
        self.seen += 1
        if len(self.values) < self.k:
            bisect.insort(self.values, value)
        elif value < self.values[-1]:
            if value not in self.values:
                bisect.insort(self.values, value)
                self.values.pop()

    def estimate(self):
        if len(self.values) < self.k:
            return len(set(self.values))
        return int((self.k - 1) * (2 ** 64) / max(1, self.values[-1]))


def _rss_mb():
    try:
        with open('/proc/self/statm') as handle:
            return int(handle.read().split()[1]) * os.sysconf('SC_PAGE_SIZE') / 1048576
    except (OSError, ValueError, IndexError):
        return 0.0


class TableMeasure:
    """Streaming per-table measurement; holds hashes and counters, never row values (text values are
    reduced to MinHash signatures immediately)."""

    def __init__(self, name, table, pk):
        self.name, self.table, self.pk = name, table, pk
        self.columns = table['columns']
        self.pk_name = pk['name'] if pk else None
        self.rows = 0
        self.row_hashes = set()
        self.normalised = set()
        self.exact_dup = self.normalised_dup = 0
        self.null_rows = self.degraded_rows = self.pii_rows = self.pii_checked = self.incomplete_rows = 0
        self.pii_kinds = {}
        self.col = {c['name']: {'null': 0, 'empty': 0, 'placeholder': 0, 'mojibake': 0, 'truncated': 0, 'invalid': 0,
                                'checked': 0, 'distinct': KMV(), 'min': None, 'max': None, 'zero': 0, 'whitespace': 0}
                    for c in self.columns}
        self.sketch = []
        self.text_bands = {}
        self.text_signatures = 0
        self.text_near_dup = 0
        self.fk_values = {}

    def observe(self, row, columns):
        from services.mtafiti.detectors.pii_detector import detect_pii
        self.rows += 1
        mapped = dict(zip(columns, row))
        non_pk = [(c, mapped.get(c)) for c in columns if c != self.pk_name]
        digest = h64(json.dumps([v for _, v in non_pk], default=str, sort_keys=False))
        if digest in self.row_hashes:
            self.exact_dup += 1
        else:
            self.row_hashes.add(digest)
            if len(self.sketch) < SKETCH_K:
                self.sketch.append(digest)
                if len(self.sketch) == SKETCH_K:
                    self.sketch.sort()
            elif digest < self.sketch[-1]:
                bisect.insort(self.sketch, digest)
                self.sketch.pop()
        norm = h64(json.dumps([re.sub(r'[\W_]+', '', str(v).lower()) if isinstance(v, str) else v
                               for c, v in non_pk if self.col_type(c) not in TIMESTAMP_TYPES and not c.endswith('_at')], default=str))
        if norm in self.normalised:
            self.normalised_dup += 1
        else:
            self.normalised.add(norm)
        null_row = degraded = incomplete = False
        long_text = []
        for spec in self.columns:
            name = spec['name']
            value = mapped.get(name)
            stat = self.col[name]
            stat['checked'] += 1
            linked = name.endswith('_id') and name != self.pk_name
            if value is None:
                stat['null'] += 1
                null_row = True
                incomplete = incomplete or linked  # a linked record that is missing
                continue
            stat['distinct'].add(h64(str(value)))
            if linked and value == 0:
                incomplete = True
            if isinstance(value, str):
                stripped = value.strip()
                if stripped == '':
                    stat['empty'] += 1
                    incomplete = incomplete or not spec['nullable'] or linked  # a required field left empty
                    continue
                if stripped != value:
                    stat['whitespace'] += 1
                if stripped.lower() in PLACEHOLDERS:
                    stat['placeholder'] += 1
                    degraded = True
                    incomplete = incomplete or not spec['nullable']
                if MOJIBAKE.search(value):
                    stat['mojibake'] += 1
                    degraded = True
                if spec['max_length'] and len(value) >= spec['max_length'] and spec['max_length'] >= 8:
                    stat['truncated'] += 1
                    degraded = True
                lowered = name.lower()
                if 'email' in lowered and not EMAIL.match(stripped):
                    stat['invalid'] += 1
                elif ('phone' in lowered or 'msisdn' in lowered or 'mobile' in lowered) and not PHONE.match(stripped):
                    stat['invalid'] += 1
                elif ('url' in lowered or 'link' in lowered) and not URL.match(stripped):
                    stat['invalid'] += 1
                if len(value) >= LONG_TEXT:
                    long_text.append(value)
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if value == 0:
                    stat['zero'] += 1
                stat['min'] = value if stat['min'] is None else min(stat['min'], value)
                stat['max'] = value if stat['max'] is None else max(stat['max'], value)
            if spec['type'] in TIMESTAMP_TYPES:
                text = str(value)
                if text.startswith('0000-00-00'):
                    stat['placeholder'] += 1
                    degraded = True
                else:
                    stat['min'] = text if stat['min'] is None else min(stat['min'], text)
                    stat['max'] = text if stat['max'] is None else max(stat['max'], text)
            if name.endswith('_id') and name != self.pk_name and value is not None and isinstance(value, (int, str)):
                bucket = self.fk_values.setdefault(name, set())
                if len(bucket) < FK_SAMPLE:
                    bucket.add(value)
        self.null_rows += null_row
        self.degraded_rows += degraded
        self.incomplete_rows += incomplete
        # PII regex sweep is the costliest step on a one-core jump host: every row for the first 2,000, then one in ten.
        if self.rows <= 2000 or self.rows % 10 == 0:
            self.pii_checked += 1
            signals = detect_pii({k: v for k, v in mapped.items() if isinstance(v, str)})
            personal = [s for s in signals if s.signal_name != 'pii.url']
            if personal:
                self.pii_rows += 1
            for s in signals:
                self.pii_kinds[s.signal_name] = self.pii_kinds.get(s.signal_name, 0) + 1
        if long_text and self.text_signatures < TEXT_SAMPLE_CAP:
            sig = MinHash()
            sig.add(shingles(' '.join(long_text)[:800]))
            self.text_signatures += 1
            hit = False
            for key in sig.band_keys():
                if key in self.text_bands:
                    hit = True
                self.text_bands[key] = self.text_bands.get(key, 0) + 1
            self.text_near_dup += hit

    def col_type(self, name):
        for c in self.columns:
            if c['name'] == name:
                return c['type']
        return ''

    def result(self, method, strata=None):
        n = max(1, self.rows)
        columns = {}
        for spec in self.columns:
            s = self.col[spec['name']]
            checked = max(1, s['checked'])
            present = max(1, checked - s['null'] - s['empty'])
            entry = {'type': spec['type'], 'nullable': spec['nullable'], 'null_ratio': round(s['null'] / checked, 4),
                     'empty_ratio': round(s['empty'] / checked, 4), 'placeholder_ratio': round(s['placeholder'] / present, 4),
                     'mojibake_ratio': round(s['mojibake'] / present, 4), 'truncation_ratio': round(s['truncated'] / present, 4),
                     'invalid_format_ratio': round(s['invalid'] / present, 4) if s['invalid'] else 0.0,
                     'distinct_ratio': round(min(1.0, s['distinct'].estimate() / present), 4), 'whitespace_ratio': round(s['whitespace'] / present, 4)}
            if spec['type'] in TIMESTAMP_TYPES:
                entry['earliest'], entry['latest'] = s['min'], s['max']
            elif spec['type'] in NUMERIC_TYPES and s['min'] is not None:
                entry['zero_ratio'] = round(s['zero'] / present, 4)
            columns[spec['name']] = entry
        timestamps = [c for c in columns.values() if c.get('latest')]
        latest = max((c['latest'] for c in timestamps), default=None)
        earliest = min((c['earliest'] for c in timestamps if c.get('earliest')), default=None)
        staleness = None
        if latest and DATEISH.match(latest):
            try:
                staleness = round((datetime.now(timezone.utc) - datetime.fromisoformat(latest[:19]).replace(tzinfo=timezone.utc)).days)
            except ValueError:
                staleness = None
        return {'rows_measured': self.rows, 'method': method, 'strata': strata,
                'exact_duplicate_ratio': round(self.exact_dup / n, 5), 'normalised_duplicate_ratio': round(self.normalised_dup / n, 5),
                'null_bearing_row_ratio': round(self.null_rows / n, 4), 'incomplete_row_ratio': round(self.incomplete_rows / n, 4),
                'degraded_row_ratio': round(self.degraded_rows / n, 4),
                'pii_row_ratio': round(self.pii_rows / max(1, self.pii_checked), 4), 'pii_rows_checked': self.pii_checked, 'pii_kinds': self.pii_kinds,
                'long_text_signatures': self.text_signatures,
                'near_duplicate_text_ratio': round(self.text_near_dup / self.text_signatures, 4) if self.text_signatures else None,
                'freshness': {'latest_write': latest, 'earliest_write': earliest, 'staleness_days': staleness},
                'columns': columns, 'sketch': ['%016x' % v for v in sorted(self.sketch)]}


BOUNDED_TEXT = 1000


def select_list(columns):
    """Long text and binary columns are read bounded so a wide row never holds megabytes in memory."""
    parts = []
    for c in columns:
        if c['type'] in TEXT_TYPES + ('blob', 'mediumblob', 'longblob', 'tinyblob', 'varbinary', 'binary') and (c['max_length'] is None or c['max_length'] > BOUNDED_TEXT):
            parts.append(f'LEFT({ident(c["name"])}, {BOUNDED_TEXT}) AS {ident(c["name"])}')
        else:
            parts.append(ident(c['name']))
    return ', '.join(parts)


def keyset_pages(db, database, name, columns, pk, start, max_rows):
    after = start
    fetched = 0
    cols = select_list(columns)
    pk_index = [c['name'] for c in columns].index(pk['name'])
    while fetched < max_rows:
        limit = min(PAGE, max_rows - fetched)
        where = f' WHERE {ident(pk["name"])} > %s' if after is not None else ''
        seen = 0
        for row in db.stream(f'SELECT {cols} FROM {ident(database)}.{ident(name)}{where} ORDER BY {ident(pk["name"])} LIMIT {int(limit)}',
                             (after,) if after is not None else None):
            seen += 1
            after = row[pk_index]
            yield row
        if not seen:
            return
        fetched += seen
        if seen < limit:
            return


def measure_table(db, database, name, table, deadline):
    pk = primary_key(table)
    columns = table['columns']
    names = [c['name'] for c in columns]
    measure = TableMeasure(name, table, pk)
    estimate = table['rows_estimate']
    if not columns:
        return {'rows_measured': 0, 'method': 'no_columns'}
    if pk is None:
        for row in db.stream(f'SELECT {select_list(columns)} FROM {ident(database)}.{ident(name)} LIMIT {STRATUM_ROWS}'):
            measure.observe(row, names)
        method, strata = 'head_sample_no_single_primary_key', None
    elif estimate <= ROW_COMPLETE_MAX:
        for row in keyset_pages(db, database, name, columns, pk, None, ROW_COMPLETE_MAX + PAGE):
            measure.observe(row, names)
        method, strata = ('complete' if measure.rows < ROW_COMPLETE_MAX + PAGE else 'capped_keyset_pass'), None
    else:
        bounds = db.query(f'SELECT MIN({ident(pk["name"])}), MAX({ident(pk["name"])}) FROM {ident(database)}.{ident(name)} LIMIT 1')
        low, high = bounds[0] if bounds else (None, None)
        starts = [None]
        if isinstance(low, int) and isinstance(high, int) and high > low:
            starts = [None] + [low + (high - low) * i // STRATA for i in range(1, STRATA)]
        for start in starts:
            for row in keyset_pages(db, database, name, columns, pk, start, STRATUM_ROWS):
                measure.observe(row, names)
        method, strata = 'stratified_keyset_sample', len(starts)
    result = measure.result(method, strata)
    result['primary_key'] = pk['name'] if pk else None
    result['referential_integrity'] = {}
    if measure.fk_values and pk is not None:
        for column, values in sorted(measure.fk_values.items()):
            target = column[:-3]
            candidates = [t for t in (target, target + 's', target + 'es') if t != name]
            for candidate in candidates:
                if candidate in db.tables and primary_key(db.tables[candidate]) and values:
                    sample = sorted(values, key=str)[:FK_SAMPLE]
                    placeholders = ', '.join(['%s'] * len(sample))
                    tpk = primary_key(db.tables[candidate])['name']
                    found = db.query(f'SELECT {ident(tpk)} FROM {ident(database)}.{ident(candidate)} WHERE {ident(tpk)} IN ({placeholders}) LIMIT {len(sample)}', tuple(sample))
                    result['referential_integrity'][column] = {'target': candidate, 'sampled': len(sample),
                                                               'orphan_ratio': round(1 - len(found) / len(sample), 4)}
                    break
    return result


def _jump_measure(control):
    """Measure one database on the jump host. Returns aggregates only."""
    started = time.time()
    if control.get('hostname_expected') and socket.gethostname() != control['hostname_expected']:
        raise ValueError('REMOTE_IDENTITY_MISMATCH')
    deadline = started + int(control['max_seconds'])
    database = control['database']
    db = Bounded(control['connection'], database, deadline)
    tables, errors = {}, []
    try:
        db.tables = schema(db, database)
        order = sorted(db.tables, key=lambda t: db.tables[t]['rows_estimate'])
        memory_stop = False
        for name in order:
            table = db.tables[name]
            if time.time() >= deadline - 30:
                errors.append({'table': name, 'code': 'BUDGET_EXHAUSTED'})
                continue
            if not memory_stop and _rss_mb() > MEMORY_STOP_MB:
                import gc
                gc.collect()
                memory_stop = _rss_mb() > MEMORY_STOP_MB
            if memory_stop:
                errors.append({'table': name, 'code': 'BUDGET_MEMORY'})
                tables[name] = {'rows_measured': 0, 'method': 'failed', 'reason_code': 'BUDGET_MEMORY', 'rows_estimate': table['rows_estimate'],
                                'data_bytes': table['data_bytes'], 'index_bytes': table['index_bytes'], 'engine': table['engine'], 'column_count': len(table['columns'])}
                continue
            try:
                metrics = measure_table(db, database, name, table, deadline)
            except Exception as exc:
                code = exc.args[0] if getattr(exc, 'args', None) and type(exc.args[0]) is int else None
                metrics = {'rows_measured': 0, 'method': 'failed', 'reason_code': {1142: 'TABLE_PERMISSION_DENIED', 1146: 'TABLE_MISSING',
                           2013: 'SOURCE_TIMEOUT', 3024: 'STATEMENT_TIME_LIMIT'}.get(code, str(exc) if str(exc).isupper() else type(exc).__name__)}
                errors.append({'table': name, 'code': metrics['reason_code']})
            metrics.update(rows_estimate=table['rows_estimate'], data_bytes=table['data_bytes'], index_bytes=table['index_bytes'],
                           engine=table['engine'], column_count=len(table['columns']), created=table['created'], updated=table['updated'],
                           schema_fingerprint=hashlib.sha256(json.dumps(sorted((c['name'], c['type']) for c in table['columns'])).encode()).hexdigest()[:16],
                           column_names_fingerprint=hashlib.sha256(json.dumps(sorted(c['name'] for c in table['columns'])).encode()).hexdigest()[:16],
                           index_count=len(table['indexes']), redundant_indexes=redundant_indexes(table['indexes']),
                           has_timestamp_columns=any(c['type'] in TIMESTAMP_TYPES for c in table['columns']))
            tables[name] = metrics
    finally:
        db.close()
    return {'protocol': PROTOCOL, 'database': database, 'hostname': socket.gethostname(), 'tables': tables, 'errors': errors,
            'statements': db.statements, 'rows_fetched': db.rows_fetched, 'wall_seconds': round(time.time() - started, 1),
            'row_values_retained': False}


# ----------------------------------------------------------------------------- worker of record (akki-vm)

def _hop(hop, inner, bundle_b64, code_sha256, deadline):
    import paramiko
    remaining = int(deadline - time.time())
    if remaining <= 10:
        raise TimeoutError('BUDGET_EXHAUSTED')
    client = paramiko.SSHClient()
    with tempfile.NamedTemporaryFile('w', suffix='.known_hosts', delete=False) as handle:
        handle.write(hop['known_hosts'])
        known = handle.name
    try:
        client.load_host_keys(known)
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(hop['host'], int(hop['port']), username=hop['user'], password=hop['password'], look_for_keys=False,
                       allow_agent=False, timeout=20, auth_timeout=20, banner_timeout=20)
        client.get_transport().set_keepalive(30)
        control = {**inner, 'bundle': bundle_b64, 'code_sha256': code_sha256, 'hostname_expected': hop['hostname_expected'],
                   'max_seconds': remaining - 30}
        channel = client.get_transport().open_session(timeout=15)
        channel.settimeout(remaining)
        channel.exec_command(shlex.quote(hop['python']) + ' -c ' + shlex.quote(JUMP_BOOTSTRAP))
        channel.sendall(json.dumps(control, default=str).encode())
        channel.shutdown_write()
        output, diagnostic = bytearray(), bytearray()
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
            if channel.recv_stderr_ready():
                diagnostic.extend(channel.recv_stderr(65536)[:max(0, 65536 - len(diagnostic))])
            if channel.exit_status_ready() and getattr(channel, 'eof_received', True) and not channel.recv_ready() and not channel.recv_stderr_ready():
                break
            if time.time() >= deadline:
                channel.close()
                raise TimeoutError('PULL_SEAM_DEADLINE')
            time.sleep(.05)
        status = channel.recv_exit_status()
        if status != 0:
            tail = diagnostic.decode(errors='replace').strip().splitlines()[-1:] or [f'rc={status} no diagnostic (killed by the host, e.g. out of memory)']
            raise ValueError('PULL_SEAM_WORKER_FAILED:' + re.sub(r'[^A-Za-z0-9_:=.,() -]', '', tail[0])[:160])
        value = json.loads(output)
        if value.get('hostname') != hop['hostname_expected'] or value.get('protocol') != PROTOCOL:
            raise ValueError('PULL_SEAM_PROVENANCE_MISMATCH')
        return value
    finally:
        client.close()
        os.unlink(known)


def _list_databases(hop, connection, bundle_b64, code_sha256, deadline):
    inner = {'connection': connection, 'database': 'information_schema', 'mode': 'list'}
    value = _hop(hop, {**inner, 'list_only': True}, bundle_b64, code_sha256, min(deadline, time.time() + 300))
    return value['databases']


def _write(path, value):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=1, default=str))
    os.replace(tmp, path)


def _jaccard(a, b):
    a, b = set(a), set(b)
    if not a or not b:
        return 0.0
    union = sorted(a | b)[:SKETCH_K]
    return round(len(set(union) & a & b) / max(1, len(union)), 4)


def rollup(databases):
    """Estate roll-up from per-database aggregates: weighted ratios, duplicate table pairs, findings."""
    tables = []
    for entry in databases:
        for name, m in entry['tables'].items():
            tables.append({'database': entry['database'], 'connection': entry['connection_label'], 'table': name, **m})
    measured = [t for t in tables if t.get('rows_measured')]
    total_rows = sum(t.get('rows_estimate', 0) for t in tables)
    total_bytes = sum(t.get('data_bytes', 0) + t.get('index_bytes', 0) for t in tables)

    def weighted(key):
        num = sum((t.get(key) or 0) * t.get('rows_estimate', 0) for t in measured if t.get(key) is not None)
        den = sum(t.get('rows_estimate', 0) for t in measured if t.get(key) is not None)
        return round(num / den, 5) if den else None

    same_schema = {}
    for t in tables:
        if t.get('schema_fingerprint') and t.get('rows_estimate', 0) > 0:
            same_schema.setdefault(t['schema_fingerprint'], []).append(t)
    duplicate_pairs = []
    for group in same_schema.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                overlap = _jaccard(a.get('sketch') or [], b.get('sketch') or [])
                if overlap >= 0.2:
                    duplicate_pairs.append({'a': f"{a['connection']}/{a['database']}.{a['table']}", 'b': f"{b['connection']}/{b['database']}.{b['table']}",
                                            'content_overlap_estimate': overlap, 'bytes_smaller': min(a['data_bytes'], b['data_bytes']),
                                            'rows_smaller': min(a['rows_estimate'], b['rows_estimate'])})
    duplicate_pairs.sort(key=lambda p: -p['bytes_smaller'])
    empty = [t for t in tables if t.get('rows_estimate', 0) == 0]
    stale = sorted([t for t in measured if (t.get('freshness') or {}).get('staleness_days') is not None and t['freshness']['staleness_days'] > 365],
                   key=lambda t: -(t.get('data_bytes', 0)))
    within_dup_bytes = sum(t['exact_duplicate_ratio'] * t.get('data_bytes', 0) for t in measured if t.get('exact_duplicate_ratio'))
    cross_dup_bytes = sum(p['bytes_smaller'] * p['content_overlap_estimate'] for p in duplicate_pairs)
    redundant_index_bytes = sum(t.get('index_bytes', 0) * len(t.get('redundant_indexes') or []) / max(1, t.get('index_count') or 1) for t in tables)
    pii_tables = sorted([t for t in measured if t.get('pii_row_ratio')], key=lambda t: -t['pii_row_ratio'] * t.get('rows_estimate', 0))
    degraded = sorted([t for t in measured if t.get('degraded_row_ratio')], key=lambda t: -t['degraded_row_ratio'] * t.get('rows_estimate', 0))
    orphaned = []
    for t in measured:
        for column, ri in (t.get('referential_integrity') or {}).items():
            if ri['orphan_ratio'] > 0:
                orphaned.append({'table': f"{t['database']}.{t['table']}", 'column': column, 'target': ri['target'], 'orphan_ratio': ri['orphan_ratio'], 'sampled': ri['sampled']})
    orphaned.sort(key=lambda o: -o['orphan_ratio'])
    brief = lambda t: {'connection': t['connection'], 'database': t['database'], 'table': t['table'], 'rows_estimate': t.get('rows_estimate'),
                       'data_bytes': t.get('data_bytes'), 'method': t.get('method'), 'exact_duplicate_ratio': t.get('exact_duplicate_ratio'),
                       'degraded_row_ratio': t.get('degraded_row_ratio'), 'pii_row_ratio': t.get('pii_row_ratio'),
                       'staleness_days': (t.get('freshness') or {}).get('staleness_days')}
    return {
        'tables_total': len(tables), 'tables_measured': len(measured), 'rows_estimate_total': total_rows, 'bytes_total': total_bytes,
        'rows_measured_total': sum(t['rows_measured'] for t in measured),
        'complete_tables': sum(1 for t in measured if t.get('method') == 'complete'),
        'sampled_tables': sum(1 for t in measured if t.get('method', '').startswith('stratified')),
        'head_sampled_tables': sum(1 for t in measured if t.get('method', '').startswith('head')),
        'failed_tables': sum(1 for t in tables if t.get('method') == 'failed'),
        'weighted': {k: weighted(k) for k in ('exact_duplicate_ratio', 'normalised_duplicate_ratio', 'null_bearing_row_ratio', 'incomplete_row_ratio',
                                              'degraded_row_ratio', 'pii_row_ratio', 'near_duplicate_text_ratio')},
        'duplication': {'within_table_duplicate_bytes_estimate': int(within_dup_bytes), 'cross_table_pairs': len(duplicate_pairs),
                        'cross_table_duplicate_bytes_estimate': int(cross_dup_bytes), 'top_pairs': duplicate_pairs[:40],
                        'same_schema_groups': sum(1 for g in same_schema.values() if len(g) > 1)},
        'storage': {'empty_tables': len(empty), 'empty_table_bytes': sum(t.get('data_bytes', 0) + t.get('index_bytes', 0) for t in empty),
                    'stale_over_one_year_tables': len(stale), 'stale_bytes': sum(t.get('data_bytes', 0) + t.get('index_bytes', 0) for t in stale),
                    'redundant_index_bytes_estimate': int(redundant_index_bytes),
                    'reclaimable_bytes_estimate': int(within_dup_bytes + cross_dup_bytes + redundant_index_bytes + sum(t.get('data_bytes', 0) + t.get('index_bytes', 0) for t in empty)),
                    'top_stale': [brief(t) for t in stale[:25]]},
        'quality': {'top_degraded': [brief(t) for t in degraded[:25]], 'top_pii': [brief(t) for t in pii_tables[:25]],
                    'orphaned_references': orphaned[:40], 'pii_kinds': _merge_counts(t.get('pii_kinds') or {} for t in measured)},
        'method_note': 'Ratios are measured on complete passes (tables ≤100k rows) or stratified keyset samples (8×5k rows) and disclosed per table; '
                       'cross-table overlap is a bottom-256 sketch Jaccard estimate over same-schema tables; no row values were retained or returned.'}


def _merge_counts(items):
    out = {}
    for counts in items:
        for k, v in counts.items():
            out[k] = out.get(k, 0) + v
    return out


def execute(control):
    """Detached worker of record on the GPU host: pull seam per database, checkpoint, roll up, receipt."""
    job_dir = Path(control['job_dir'])
    job_dir.mkdir(parents=True, exist_ok=True)
    state_path, receipt_path = job_dir / 'state.json', job_dir / 'receipt.json'
    started = now()
    state = {'phase': 'estate_intelligence', 'job_id': control['job_id'], 'status': 'running', 'started_at': started,
             'hostname': socket.gethostname(), 'runtime_id': control['runtime_id'], 'progress': {}, 'databases_done': []}
    _write(state_path, state)
    hop = control['pull_via']
    bundle_b64, code_sha256 = control['bundle_b64'], control['code_sha256']
    deadline = time.time() + int(control.get('max_seconds', 3 * 86400))
    results, errors = [], []
    receipt = {'protocol': PROTOCOL, 'job_id': control['job_id'], 'phase': 'estate_intelligence', 'runtime_id': control['runtime_id'],
               'hostname': socket.gethostname(), 'started_at': started, 'code_sha256': code_sha256, 'status': 'failed'}
    try:
        if socket.gethostname() != control['hostname_expected']:
            raise ValueError('HOST_IDENTITY_MISMATCH')
        for connection in control['connections']:
            label = connection['label']
            try:
                databases = _list_databases(hop, {k: connection[k] for k in ('host', 'port', 'user', 'password')}, bundle_b64, code_sha256, deadline)
            except Exception as exc:
                errors.append({'connection': label, 'code': str(exc)[:120] if str(exc).isupper() or ':' in str(exc) else type(exc).__name__})
                continue
            for database in databases:
                key = hashlib.sha256(f'{label}|{database}'.encode()).hexdigest()[:16]
                path = job_dir / f'db_{key}.json'
                if path.exists():
                    results.append(json.loads(path.read_text()))
                    continue
                state['progress'] = {'stage': 'measuring database', 'connection': label, 'database': database,
                                     'databases_done': len(results), 'at': now()}
                _write(state_path, state)
                try:
                    value = _hop(hop, {'connection': {k: connection[k] for k in ('host', 'port', 'user', 'password')}, 'database': database},
                                 bundle_b64, code_sha256, min(deadline, time.time() + int(control.get('database_seconds', 5400))))
                    value['connection_label'] = label
                    value['measured_at'] = now()
                    _write(path, value)
                    results.append(value)
                    state['databases_done'].append({'connection': label, 'database': database, 'tables': len(value['tables']),
                                                    'rows_fetched': value['rows_fetched'], 'wall_seconds': value['wall_seconds']})
                except Exception as exc:
                    errors.append({'connection': label, 'database': database,
                                   'code': str(exc)[:160] if str(exc).isupper() or ':' in str(exc) else type(exc).__name__})
                    state['errors'] = errors
                _write(state_path, state)
        state['progress'] = {'stage': 'estate roll-up', 'databases_done': len(results), 'at': now()}
        _write(state_path, state)
        summary = rollup(results)
        detail = {'databases': [{'connection': r['connection_label'], 'database': r['database'], 'tables': r['tables'], 'errors': r['errors'],
                                 'statements': r['statements'], 'rows_fetched': r['rows_fetched'], 'wall_seconds': r['wall_seconds']} for r in results]}
        _write(job_dir / 'detail.json', detail)
        receipt['result'] = {'summary': summary, 'errors': errors, 'databases': [{'connection': r['connection_label'], 'database': r['database'],
                             'tables': len(r['tables']), 'rows_fetched': r['rows_fetched'], 'statements': r['statements'], 'wall_seconds': r['wall_seconds'],
                             'table_errors': len(r['errors'])} for r in results],
                             'detail_path': str(job_dir / 'detail.json'), 'detail_sha256': hashlib.sha256((job_dir / 'detail.json').read_bytes()).hexdigest(),
                             'row_values_retained': False, 'execution': 'jump host measured; GPU host held aggregates only'}
        receipt['status'] = 'completed' if results and not errors else 'partial' if results else 'failed'
    except Exception as exc:
        receipt['error'] = {'type': type(exc).__name__, 'message': str(exc)[:300], 'trace': traceback.format_exc()[-2000:]}
    receipt['finished_at'] = now()
    body = json.dumps(receipt, sort_keys=True, default=str).encode()
    receipt['receipt_sha256'] = hashlib.sha256(body).hexdigest()
    _write(receipt_path, receipt)
    state.update(status=receipt['status'], finished_at=receipt['finished_at'], receipt_sha256=receipt['receipt_sha256'])
    _write(state_path, state)
    return receipt


def _jump_list(control):
    db = Bounded(control['connection'], 'information_schema', time.time() + 120)
    try:
        rows = db.query('SELECT SCHEMA_NAME FROM information_schema.SCHEMATA LIMIT 500')
    finally:
        db.close()
    return {'protocol': PROTOCOL, 'hostname': socket.gethostname(), 'databases': sorted(r[0] for r in rows if r[0] not in SYSTEM_SCHEMAS)}


def jump_execute(control):
    """Jump-host entry: list databases or measure one database; identity is checked before any read."""
    if control.get('hostname_expected') and socket.gethostname() != control['hostname_expected']:
        raise ValueError('REMOTE_IDENTITY_MISMATCH')
    if control.get('list_only'):
        return _jump_list(control)
    return _jump_measure(control)
