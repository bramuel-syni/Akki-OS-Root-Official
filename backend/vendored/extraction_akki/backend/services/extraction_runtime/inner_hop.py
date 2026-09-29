"""Bounded read-only row access where the estate is reachable (direct or across the pull seam).

Every statement passes `refuse_if_write` and carries an explicit LIMIT; a write verb is a
refusal with a receipt, never an execution. Row values are made JSON-plain here.
"""
import hashlib
import json
import os
import shlex
import tempfile
import time

BOOTSTRAP = '''import sys,json,base64,tempfile,pathlib,hashlib
p=json.load(sys.stdin)
b=base64.b64decode(p['bundle'])
if hashlib.sha256(b).hexdigest()!=p['code_sha256']: raise ValueError('CODE_HASH_MISMATCH')
with tempfile.TemporaryDirectory(prefix='akki-extract-code-') as d:
 z=pathlib.Path(d)/'worker.zip'; z.write_bytes(b); sys.path.insert(0,str(z))
 from services.extraction_runtime.structured_records_worker import execute
 print(json.dumps(execute(p),sort_keys=True,default=str),flush=True)
'''


def identifier(value):
    if not value or not all(c.isalnum() or c == '_' for c in value):
        raise ValueError('UNSAFE_IDENTIFIER')
    return '`' + value + '`'


def bounded_select(database, table, columns, primary_key, after, limit, placeholder='%s'):
    from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
    cols = ', '.join(identifier(c) for c in columns)
    where = f' WHERE {identifier(primary_key)} > {placeholder}' if after is not None else ''
    sql = f'SELECT {cols} FROM {identifier(database)}.{identifier(table)}{where} ORDER BY {identifier(primary_key)} LIMIT {int(limit)}'
    return refuse_if_write(sql)


def _mysql_rows(conn, sql, after):
    import pymysql
    connection = pymysql.connect(host=conn['host'], port=int(conn['port']), user=conn['user'],
                                 password=conn['password'], connect_timeout=8, read_timeout=30, write_timeout=8,
                                 charset='utf8mb4', autocommit=True)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SET SESSION TRANSACTION READ ONLY')
            cursor.execute(sql, (after,) if after is not None else None)
            return list(cursor.fetchall()), [c[0] for c in cursor.description or []]
    finally:
        connection.close()


def _rds_data_rows(conn, database, sql, after):
    """AWS RDS Data API: the bounded statement runs inside the estate's cluster; only rows return."""
    import boto3
    from botocore.config import Config
    sdk = boto3.client('rds-data', region_name=conn['region'], aws_access_key_id=conn['aws_access_key_id'],
                       aws_secret_access_key=conn['aws_secret_access_key'],
                       config=Config(connect_timeout=10, read_timeout=45, retries={'max_attempts': 1}))
    params = {}
    if after is not None:
        typed = {'longValue': int(after)} if isinstance(after, int) and not isinstance(after, bool) else {'stringValue': str(after)}
        params = {'parameters': [{'name': 'after', 'value': typed}]}
    value = sdk.execute_statement(resourceArn=conn['cluster_arn'], secretArn=conn['secret_arn'], database=database,
                                  sql=sql, includeResultMetadata=True, **params)
    rows = [[None if cell.get('isNull') else next(iter(cell.values())) for cell in row] for row in value.get('records', [])]
    return rows, [c.get('name', '') for c in value.get('columnMetadata', [])]


def select_rows(control):
    """Run one bounded, guarded SELECT against a connection; returns plain JSON rows."""
    from services.extraction_runtime.units import plain
    conn = control['connection']
    driver = conn.get('driver', 'mysql')
    after = control.get('after')
    sql = bounded_select(control['database'], control['table'], control['columns'], control['primary_key'],
                         after, control['limit'], placeholder=':after' if driver == 'rds_data' else '%s')
    if control.get('attempt_write_sql'):
        # M3-T5 drill: the guard must refuse before any connection is used.
        from services.mtafiti.executor.readonly_sql_guard import refuse_if_write, WriteVerbRefused
        try:
            refuse_if_write(control['attempt_write_sql'])
            return {'status': 'failed', 'reason_code': 'WRITE_GUARD_DID_NOT_REFUSE'}
        except WriteVerbRefused:
            return {'status': 'refused', 'reason_code': 'WRITE_VERB_REFUSED', 'rows': [], 'columns': []}
    if driver == 'rds_data':
        raw, columns = _rds_data_rows(conn, control['database'], sql, after)
    else:
        raw, columns = _mysql_rows(conn, sql, after)
    rows = [[plain(v) for v in row] for row in raw]
    encoded = json.dumps(rows, default=str).encode()
    return {'status': 'complete', 'rows': rows, 'columns': columns, 'bytes_read': len(encoded), 'sql_sha256': hashlib.sha256(sql.encode()).hexdigest()}


def via_jump(hop, inner, bundle_b64, code_sha256, deadline):
    """Pull seam: the worker of record stays where it is; the guarded SELECT runs on the jump host."""
    import paramiko
    remaining = int(deadline - time.time())
    if remaining <= 5:
        raise TimeoutError('BUDGET_EXHAUSTED')
    client = paramiko.SSHClient()
    with tempfile.NamedTemporaryFile('w', suffix='.known_hosts', delete=False) as handle:
        handle.write(hop['known_hosts'])
        known = handle.name
    try:
        client.load_host_keys(known)
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        budget = min(20, remaining)
        client.connect(hop['host'], int(hop['port']), username=hop['user'], password=hop['password'],
                       look_for_keys=False, allow_agent=False, timeout=budget, auth_timeout=budget, banner_timeout=budget)
        control = {**inner, 'mode': 'inner_select', 'bundle': bundle_b64, 'code_sha256': code_sha256,
                   'hostname_expected': hop['hostname_expected']}
        channel = client.get_transport().open_session(timeout=15)
        channel.settimeout(remaining)
        channel.exec_command(shlex.quote(hop['python']) + ' -c ' + shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(control).encode())
        channel.shutdown_write()
        output = bytearray()
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
                if len(output) > 12 * 1024 * 1024:
                    channel.close()
                    raise ValueError('BATCH_TOO_LARGE')
            if channel.recv_stderr_ready():
                channel.recv_stderr(65536)
            if channel.exit_status_ready() and getattr(channel, 'eof_received', True) and not channel.recv_ready():
                break
            if time.time() >= deadline:
                channel.close()
                raise TimeoutError('PULL_SEAM_DEADLINE')
            time.sleep(.02)
        if channel.recv_exit_status() != 0:
            raise ValueError('PULL_SEAM_WORKER_FAILED')
        value = json.loads(output)
        if value.get('hostname') != hop['hostname_expected']:
            raise ValueError('PULL_SEAM_PROVENANCE_MISMATCH')
        return value
    finally:
        client.close()
        os.unlink(known)
