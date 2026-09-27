"""Offline selection tests: no socket, key load or GPU activity permitted."""
from types import SimpleNamespace
import pytest
from test_gpu_direct_workbook_connection import _write_workbook
from services.gpu_direct.workbook import DirectConnectionError


@pytest.fixture
def selected(monkeypatch, tmp_path):
    path = tmp_path / 'owner.xlsx'
    _write_workbook(path, ['hostname: TEST-only-owner', 'username: TEST-user',
                          'password: TEST-secret-with:colon ', 'public ip: 192.0.2.10'])
    monkeypatch.setenv('AKKI_GPU_CONNECTION_MODE', 'direct_workbook')
    monkeypatch.setenv('GPU_DIRECT_CREDENTIALS_XLSX', str(path))
    monkeypatch.setenv('GPU_DIRECT_SSH_PORT', '22')
    monkeypatch.setenv('AKKI_GPU_HOSTS', 'OLD-must-not-be-used')
    monkeypatch.setenv('AKKI_GPU_SSH_PRIVATE_KEY_PATH', '/missing-old-key')
    from services.census_autonomy import execution_identity
    def forbidden(*args, **kwargs):
        raise AssertionError('Old client identity must not be consulted')
    monkeypatch.setattr(execution_identity, 'verify_identity', forbidden)
    monkeypatch.setattr(execution_identity, '_load_key', forbidden)
    monkeypatch.setattr(execution_identity, '_expected_fingerprint', forbidden)
    return path


def test_active_inventory_and_redaction_are_from_owner_workbook(selected):
    from services.training_runner import ssh_seam
    assert ssh_seam.list_hosts() == ['TEST-only-owner']
    config = ssh_seam.get_host_config('TEST-only-owner')
    assert config.host == '192.0.2.10' and config.username == 'TEST-user'
    assert config.auth_method == 'password' and config.key_path is None
    assert ssh_seam._get_password_for('TEST-only-owner') == 'TEST-secret-with:colon '
    assert ssh_seam._redact('TEST-secret-with:colon ') == '********'


@pytest.mark.parametrize('entrypoint', ['runner', 'census'])
def test_active_entrypoints_never_touch_old_identity_or_fallback(monkeypatch, selected, entrypoint):
    from services.training_runner import ssh_seam
    from services.census_autonomy import remote_dispatch
    from services.gpu_direct import connection
    calls = []
    client = SimpleNamespace(close=lambda: None)
    def direct(name, *, timeout):
        calls.append((name, timeout))
        return client, SimpleNamespace()
    monkeypatch.setattr(connection, 'connect', direct)
    if entrypoint == 'runner':
        assert ssh_seam.connect('TEST-only-owner', timeout=8) is client
    else:
        returned, config = remote_dispatch._connect('TEST-only-owner', 8)
        assert returned is client and config.hostname_expected == 'TEST-only-owner'
    assert calls == [('TEST-only-owner', 8)]


@pytest.mark.parametrize('entrypoint', ['runner', 'census'])
def test_direct_failure_does_not_attempt_old_key(monkeypatch, selected, entrypoint):
    from services.training_runner import ssh_seam
    from services.census_autonomy import remote_dispatch
    from services.gpu_direct import connection
    def refused(*args, **kwargs):
        raise DirectConnectionError('DIRECT_PASSWORD_METHOD_NOT_ALLOWED')
    monkeypatch.setattr(connection, 'connect', refused)
    with pytest.raises(DirectConnectionError, match='DIRECT_PASSWORD_METHOD_NOT_ALLOWED'):
        if entrypoint == 'runner':
            ssh_seam.connect('TEST-only-owner', timeout=8)
        else:
            remote_dispatch._connect('TEST-only-owner', 8)


def test_broken_workbook_cannot_silently_restore_old_inventory(monkeypatch, selected):
    from services.training_runner import ssh_seam
    monkeypatch.setenv('GPU_DIRECT_CREDENTIALS_XLSX', '/missing-new-workbook')
    with pytest.raises(DirectConnectionError):
        ssh_seam.list_hosts()


def test_invalid_mode_does_not_select_legacy(monkeypatch):
    from services.training_runner import ssh_seam
    monkeypatch.setenv('AKKI_GPU_CONNECTION_MODE', 'misspelled')
    with pytest.raises(DirectConnectionError, match='DIRECT_CONNECTION_MODE_INVALID'):
        ssh_seam.list_hosts()