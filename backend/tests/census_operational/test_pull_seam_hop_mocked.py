"""Pull-seam hop (MOCKED transport): GPU worker of record executes jump-governed sources on the jump host."""
import hashlib
import json
import time
from types import SimpleNamespace

import pytest

from services.census_autonomy import deep_dispatch, deep_worker


def _inner(sources, status, reason=None, runtime='non_gpu_jump', code='hash-seam', host='ecs-jump'):
    body = {'protocol': 'akki-census-deep-v1', 'status': status, 'sources': sources, 'source_rows_returned': 0,
            'worker': {'runtime_id': runtime, 'code_sha256': code, 'wall_seconds': 1.5, 'telemetry': {'hostname': host}}}
    if reason:
        body['reason_code'] = reason
    value = dict(body)
    value['worker_receipt_id'] = 'cwr-' + hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
    return value


def _control(hop=None):
    connector = {'driver': 'nas_nfs', 'root': '/mnt/nfs-share', 'source_id': 'rms_nas'}
    if hop:
        connector['pull_via'] = hop
    return {'census_run_id': 'cr-seam', 'tenant_id': 'RMS', 'source_id': 'rms_nas', 'runtime_id': 'akki-vm',
            'hostname_expected': 'akki-vm', 'code_sha256': 'hash-seam', 'lawful_basis_sha256': 'lawful',
            'max_seconds': 30, 'connector': connector}


@pytest.fixture
def _gpu_host(monkeypatch):
    monkeypatch.setattr(deep_worker, 'telemetry', lambda: {'hostname': 'akki-vm', 'python': '3.12', 'gpu_devices': []})


def test_worker_records_pull_seam_and_uses_jump_measurements(_gpu_host, monkeypatch):
    from services.census_autonomy import deep_pull
    sources = [{'source_ref': 'source_a', 'label': 'channel01', 'kind': 'nas', 'status': 'complete', 'file_count': 3}]
    seam = {'via': 'non_gpu_jump', 'hostname': 'ecs-jump', 'server_key_sha256': 'k' * 64}
    monkeypatch.setattr(deep_pull, 'through_jump', lambda control, deadline: (_inner(sources, 'complete'), seam))
    result = deep_worker.execute(_control(hop={'host': 'jump'}))
    assert result['status'] == 'complete'
    assert result['sources'] == sources
    assert result['worker']['runtime_id'] == 'akki-vm'
    assert result['worker']['pull_seam'] == seam
    assert result['execution_location'] == 'akki_host'
    assert 'password' not in json.dumps(result)


def test_worker_propagates_jump_side_block_reason(_gpu_host, monkeypatch):
    from services.census_autonomy import deep_pull
    monkeypatch.setattr(deep_pull, 'through_jump', lambda control, deadline: (_inner([], 'blocked', 'NAS_NO_CHANNELS_OBSERVED'), {'via': 'non_gpu_jump'}))
    result = deep_worker.execute(_control(hop={'host': 'jump'}))
    assert result['status'] == 'blocked'
    assert result['reason_code'] == 'NAS_NO_CHANNELS_OBSERVED'


def test_worker_fails_closed_when_hop_transport_missing(_gpu_host, monkeypatch):
    from services.census_autonomy import deep_pull
    def _refuse(control, deadline):
        raise ValueError('PULL_SEAM_TRANSPORT_UNAVAILABLE')
    monkeypatch.setattr(deep_pull, 'through_jump', _refuse)
    result = deep_worker.execute(_control(hop={'host': 'jump'}))
    assert result['status'] == 'blocked'
    assert result['reason_code'] == 'PULL_SEAM_TRANSPORT_UNAVAILABLE'
    assert 'pull_seam' not in result['worker']


def test_worker_without_hop_keeps_local_driver_path(_gpu_host, monkeypatch):
    from services.census_autonomy import deep_files
    monkeypatch.setattr(deep_files, 'nas', lambda config, deadline: [{'label': 'channel01', 'status': 'complete'}])
    result = deep_worker.execute(_control())
    assert result['status'] == 'complete' and 'pull_seam' not in result['worker']


def test_through_jump_refuses_provenance_mismatch(monkeypatch):
    from services.census_autonomy import deep_pull

    class _Chan:
        def __init__(self, payload):
            self.chunks = [payload]
        def settimeout(self, t): pass
        def exec_command(self, c): pass
        def sendall(self, b): pass
        def shutdown_write(self): pass
        def recv_ready(self): return bool(self.chunks)
        def recv(self, n): return self.chunks.pop(0)
        def recv_stderr_ready(self): return False
        def exit_status_ready(self): return True
        def recv_exit_status(self): return 0
        def close(self): pass

    class _Key:
        def asbytes(self): return b'jump-key'

    class _Transport:
        def __init__(self, chan): self.chan = chan
        def open_session(self, timeout=15): return self.chan
        def set_keepalive(self, seconds): self.keepalive = seconds
        def get_remote_server_key(self): return _Key()

    class _Client:
        def __init__(self, chan): self.t = _Transport(chan)
        def load_host_keys(self, p): pass
        def set_missing_host_key_policy(self, p): pass
        def connect(self, *a, **k): pass
        def get_transport(self): return self.t
        def close(self): pass

    payload = json.dumps(_inner([], 'complete', runtime='akki-vm-ii')).encode()
    fake_paramiko = SimpleNamespace(SSHClient=lambda: _Client(_Chan(payload)), RejectPolicy=lambda: None)
    monkeypatch.setitem(__import__('sys').modules, 'paramiko', fake_paramiko)
    monkeypatch.setattr(deep_pull, 'bundle_bytes', lambda h: b'zip')
    hop = {'host': 'j', 'port': 22, 'user': 'u', 'password': 'p', 'hostname_expected': 'ecs-jump',
           'python': '/opt/akki-census/bin/python', 'known_hosts': 'j ssh-ed25519 AAAA'}
    with pytest.raises(ValueError, match='PULL_SEAM_PROVENANCE_MISMATCH'):
        deep_pull.through_jump(_control(hop=hop), time.time() + 30)


def test_dispatch_attaches_hop_only_for_gpu_runtime_on_jump_governed_sources(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setenv('CENSUS_REMOTE_PYTHON', '/usr/bin/python3')
    monkeypatch.setattr(deep_dispatch.store, 'now', lambda: '2026-02-01T00:00:00Z')
    monkeypatch.setattr(deep_dispatch.store, 'cursor_dir', lambda: tmp_path)
    monkeypatch.setattr(deep_dispatch, 'connector_for', lambda *a, **k: {'driver': 'nas_nfs', 'root': '/mnt/nfs-share', 'source_id': 'rms_nas'})
    monkeypatch.setattr(deep_dispatch, 'pull_seam_hop', lambda: {'host': 'jump', 'password': 'secret', 'known_hosts': 'x'})
    monkeypatch.setattr(deep_dispatch, 'build_bundle', lambda: ('code', 'hash'))
    import services.training_runner.ssh_seam as ssh_seam
    monkeypatch.setattr(ssh_seam, 'list_hosts', lambda: ['akki-vm', 'akki-vm-ii'])

    class _Chan:
        def settimeout(self, t): pass
        def exec_command(self, c): pass
        def sendall(self, b): seen['control'] = json.loads(b)
        def shutdown_write(self): pass
        def recv_ready(self): return False
        def recv_stderr_ready(self): return False
        def exit_status_ready(self): return True
        def recv_exit_status(self): return 1
        def close(self): pass

    class _Client:
        def get_transport(self): return SimpleNamespace(open_session=lambda timeout=15: _Chan(), set_keepalive=lambda s: None)
        def close(self): pass

    monkeypatch.setattr(deep_dispatch, '_connect', lambda runtime, timeout: (_Client(), SimpleNamespace(hostname_expected=runtime)))
    monkeypatch.setattr(deep_dispatch, '_connect_jump', lambda cfg, timeout: _Client())
    monkeypatch.setattr(deep_dispatch, '_jump_config', lambda: {})
    monkeypatch.setenv('CENSUS_JUMP_HOSTNAME', 'ecs-jump')

    monkeypatch.setattr(deep_dispatch.store, 'get', lambda r, t: {'worker_id': 'akki-vm'})
    deep_dispatch.execute_source('cr-1', 'RMS', 'rms_nas', 'lawful', time.time() + 30)
    assert seen['control']['connector']['pull_via']['host'] == 'jump'
    assert seen['control']['runtime_id'] == 'akki-vm'

    monkeypatch.setattr(deep_dispatch.store, 'get', lambda r, t: {'worker_id': 'non_gpu_jump'})
    deep_dispatch.execute_source('cr-2', 'RMS', 'rms_nas', 'lawful', time.time() + 30)
    assert 'pull_via' not in seen['control']['connector']

    monkeypatch.setattr(deep_dispatch, 'connector_for', lambda *a, **k: {'driver': 'object_store', 'source_id': 'rms_obs'})
    monkeypatch.setattr(deep_dispatch.store, 'get', lambda r, t: {'worker_id': 'akki-vm'})
    deep_dispatch.execute_source('cr-3', 'RMS', 'rms_obs', 'lawful', time.time() + 30)
    assert 'pull_via' not in seen['control']['connector']
    transport = json.loads((tmp_path / 'transport-cr-1-rms_nas.json').read_text())
    assert 'secret' not in json.dumps(transport)
