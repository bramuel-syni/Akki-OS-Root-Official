"""Pull seam hop: the admitted GPU worker runs the reviewed bundle where the data is governed.

The NAS share and the egress-pinned relational grants are reachable only from the jump
host. Nothing is mounted on, copied to or staged through the GPU host or E1: the same
code hash executes on the jump host and only metadata/measurements return over the
pinned SSH channel (Doc 12 A5.4, The Pull Seam P015). Fail closed; no fallback.
"""
import base64
import hashlib
import json
import os
import shlex
import sys
import tempfile
import time

def bundle_bytes(code_hash):
    path=next(p for p in sys.path if p.endswith('worker.zip'))
    raw=open(path,'rb').read()
    if hashlib.sha256(raw).hexdigest()!=code_hash: raise ValueError('CODE_HASH_MISMATCH')
    return raw

def through_jump(control,deadline):
    try: import paramiko
    except ImportError: raise ValueError('PULL_SEAM_TRANSPORT_UNAVAILABLE')
    from services.census_autonomy.deep_bundle import BOOTSTRAP
    hop=control['connector']['pull_via']
    raw=bundle_bytes(control['code_sha256'])
    remaining=int(deadline-time.time())
    if remaining<=5: raise TimeoutError('BUDGET_EXHAUSTED')
    client=paramiko.SSHClient()
    with tempfile.NamedTemporaryFile('w',suffix='.known_hosts',delete=False) as handle:
        handle.write(hop['known_hosts']); known=handle.name
    try:
        client.load_host_keys(known)
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        budget=min(20,remaining)
        client.connect(hop['host'],int(hop['port']),username=hop['user'],password=hop['password'],
                       look_for_keys=False,allow_agent=False,timeout=budget,auth_timeout=budget,banner_timeout=budget)
        client.get_transport().set_keepalive(30)
        remaining=int(deadline-time.time())
        if remaining<=5: raise TimeoutError('BUDGET_EXHAUSTED')
        margin=min(45,max(3,remaining//4))
        inner={**control,'bundle':base64.b64encode(raw).decode(),'runtime_id':'non_gpu_jump',
               'hostname_expected':hop['hostname_expected'],'max_seconds':remaining-margin,
               'connector':{k:v for k,v in control['connector'].items() if k!='pull_via'}}
        channel=client.get_transport().open_session(timeout=15)
        channel.settimeout(remaining)
        channel.exec_command(shlex.quote(hop['python'])+' -c '+shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(inner).encode()); channel.shutdown_write()
        output=bytearray(); diagnostic=bytearray()
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
                if len(output)>12*1024*1024: channel.close(); raise ValueError('MEASUREMENT_RECEIPT_TOO_LARGE')
            if channel.recv_stderr_ready():
                chunk=channel.recv_stderr(65536); diagnostic.extend(chunk[:max(0,65536-len(diagnostic))])
            if channel.exit_status_ready() and getattr(channel,'eof_received',True) and not channel.recv_ready() and not channel.recv_stderr_ready(): break
            if time.time()>=deadline: channel.close(); raise TimeoutError('PULL_SEAM_DEADLINE')
            time.sleep(.02)
        if channel.recv_exit_status()!=0: raise ValueError('PULL_SEAM_WORKER_FAILED')
        value=json.loads(output)
        receipt_id=value.pop('worker_receipt_id',None)
        if receipt_id!='cwr-'+hashlib.sha256(json.dumps(value,sort_keys=True,default=str).encode()).hexdigest():
            raise ValueError('PULL_SEAM_RECEIPT_DIGEST_MISMATCH')
        worker=value.get('worker',{})
        if (worker.get('code_sha256')!=control['code_sha256'] or worker.get('runtime_id')!='non_gpu_jump'
                or worker.get('telemetry',{}).get('hostname')!=hop['hostname_expected']):
            raise ValueError('PULL_SEAM_PROVENANCE_MISMATCH')
        seam={'via':'non_gpu_jump','hostname':hop['hostname_expected'],
              'server_key_sha256':hashlib.sha256(client.get_transport().get_remote_server_key().asbytes()).hexdigest(),
              'inner_worker_receipt_id':receipt_id,'inner_wall_seconds':worker.get('wall_seconds'),
              'stderr_sha256':hashlib.sha256(diagnostic).hexdigest(),
              'principle':'compute to data: reviewed code executed where the estate is reachable; no estate bytes on the GPU host'}
        return value,seam
    finally:
        client.close(); os.unlink(known)
