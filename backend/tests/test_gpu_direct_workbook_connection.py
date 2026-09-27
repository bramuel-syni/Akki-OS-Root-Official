"""Regression tests for gpu_direct workbook parsing and password-only connection flow."""

import os
import stat
from pathlib import Path

import openpyxl
import paramiko
import pytest

from services.gpu_direct.connection import connect_target
from services.gpu_direct.workbook import DirectConnectionError, Target, get_target, read_targets


# Module coverage: services.gpu_direct.workbook target parsing and custody guards.
def _write_workbook(path: Path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    for idx, row in enumerate(rows, start=1):
        ws.cell(row=idx, column=1, value=row)
    wb.save(path)
    wb.close()
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def _env_for(path: Path):
    return {
        "GPU_DIRECT_CREDENTIALS_XLSX": str(path),
        "GPU_DIRECT_SSH_PORT": "22",
    }


def test_read_targets_accepts_hostname_heading_then_record(tmp_path):
    workbook = tmp_path / "gpu.xlsx"
    _write_workbook(
        workbook,
        [
            "hostname: akki-vm-ii",
            "hostname: akki-vm",
            "public ip: 41.173.184.244",
            "username: ubuntu",
            "password: pass1",
        ],
    )
    targets = read_targets(_env_for(workbook))
    assert len(targets) == 1
    assert targets[0].name == "akki-vm"
    assert targets[0].host == "41.173.184.244"


def test_read_targets_rejects_ambiguous_duplicate_field(tmp_path):
    workbook = tmp_path / "gpu.xlsx"
    _write_workbook(
        workbook,
        [
            "hostname: akki-vm",
            "public ip: 41.173.184.244",
            "username: ubuntu",
            "username: ubuntu2",
            "password: pass1",
        ],
    )
    with pytest.raises(DirectConnectionError) as exc:
        read_targets(_env_for(workbook))
    assert exc.value.code == "DIRECT_WORKBOOK_AMBIGUOUS"


def test_get_target_not_found_raises(tmp_path):
    workbook = tmp_path / "gpu.xlsx"
    _write_workbook(
        workbook,
        [
            "hostname: akki-vm",
            "public ip: 41.173.184.244",
            "username: ubuntu",
            "password: pass1",
        ],
    )
    with pytest.raises(DirectConnectionError) as exc:
        get_target("missing-host", _env_for(workbook))
    assert exc.value.code == "DIRECT_WORKBOOK_TARGET_NOT_FOUND"


# Module coverage: services.gpu_direct.connection password auth call discipline.
def test_connect_target_calls_auth_password_once_with_fallback_false(monkeypatch):
    calls = {"auth": 0}

    class FakeServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"server-key"

    class FakePinnedKey:
        def asbytes(self):
            return b"server-key"

    class FakeHostEntry(dict):
        pass

    class FakeHostKeys:
        def __init__(self, _path):
            pass

        def lookup(self, _token):
            return FakeHostEntry({"ssh-ed25519": FakePinnedKey()})

    class FakeSecurity:
        key_types = ["ssh-ed25519"]

    class FakeTransport:
        def __init__(self, _sock):
            self.authenticated = True

        def set_log_channel(self, _name):
            return None

        def get_security_options(self):
            return FakeSecurity()

        def start_client(self, timeout):
            assert timeout == 8

        def get_remote_server_key(self):
            return FakeServerKey()

        def auth_password(self, username, password, fallback=False):
            calls["auth"] += 1
            assert username == "ubuntu"
            assert password == "secret"
            assert fallback is False
            return []

        def is_authenticated(self):
            return self.authenticated

        def close(self):
            return None

    class FakeSocket:
        def close(self):
            return None

    monkeypatch.setattr(paramiko, "HostKeys", FakeHostKeys)
    monkeypatch.setattr(paramiko, "Transport", FakeTransport)
    monkeypatch.setattr("services.gpu_direct.connection.socket.create_connection", lambda *_args, **_kwargs: FakeSocket())

    env = {
        "GPU_DIRECT_TIMEOUT_SECONDS": "8",
        "SSH_KNOWN_HOSTS_PATH": "/tmp/known_hosts",
        "AKKI_VM_SSH_PRIVATE_KEY_PATH": "/nonsense/unused",
    }
    target = Target(name="akki-vm", host="41.173.184.244", port=22, username="ubuntu", password="secret")
    client, receipt = connect_target(target, environ=env, timeout=8)
    assert client is not None
    assert calls["auth"] == 1
    assert receipt["status"] == "DIRECT_AUTHENTICATED"
    assert receipt["historical_client_identity_used"] is False


def test_connect_target_pin_mismatch_stops_before_password_auth(monkeypatch):
    calls = {"auth": 0}

    class FakeServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"actual"

    class FakePinnedKey:
        def asbytes(self):
            return b"expected"

    class FakeHostEntry(dict):
        pass

    class FakeHostKeys:
        def __init__(self, _path):
            pass

        def lookup(self, _token):
            return FakeHostEntry({"ssh-ed25519": FakePinnedKey()})

    class FakeSecurity:
        key_types = ["ssh-ed25519"]

    class FakeTransport:
        def __init__(self, _sock):
            pass

        def set_log_channel(self, _name):
            return None

        def get_security_options(self):
            return FakeSecurity()

        def start_client(self, timeout):
            assert timeout == 8

        def get_remote_server_key(self):
            return FakeServerKey()

        def auth_password(self, username, password, fallback=False):
            calls["auth"] += 1
            return []

        def close(self):
            return None

    class FakeSocket:
        def close(self):
            return None

    monkeypatch.setattr(paramiko, "HostKeys", FakeHostKeys)
    monkeypatch.setattr(paramiko, "Transport", FakeTransport)
    monkeypatch.setattr("services.gpu_direct.connection.socket.create_connection", lambda *_args, **_kwargs: FakeSocket())

    env = {
        "GPU_DIRECT_TIMEOUT_SECONDS": "8",
        "SSH_KNOWN_HOSTS_PATH": "/tmp/known_hosts",
    }
    target = Target(name="akki-vm", host="41.173.184.244", port=22, username="ubuntu", password="secret")
    client, receipt = connect_target(target, environ=env, timeout=8)
    assert client is None
    assert receipt["status"] == "DIRECT_SERVER_IDENTITY_MISMATCH"
    assert calls["auth"] == 0


def test_connect_target_bad_auth_type_redacts_and_reports_allowlist(monkeypatch):
    class FakeServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"server-key"

    class FakePinnedKey:
        def asbytes(self):
            return b"server-key"

    class FakeHostEntry(dict):
        pass

    class FakeHostKeys:
        def __init__(self, _path):
            pass

        def lookup(self, _token):
            return FakeHostEntry({"ssh-ed25519": FakePinnedKey()})

    class FakeSecurity:
        key_types = ["ssh-ed25519"]

    class FakeTransport:
        def __init__(self, _sock):
            pass

        def set_log_channel(self, _name):
            return None

        def get_security_options(self):
            return FakeSecurity()

        def start_client(self, timeout):
            assert timeout == 8

        def get_remote_server_key(self):
            return FakeServerKey()

        def auth_password(self, username, password, fallback=False):
            raise paramiko.BadAuthenticationType(explanation="no password", types=["publickey", "bogus"])

        def close(self):
            return None

    class FakeSocket:
        def close(self):
            return None

    monkeypatch.setattr(paramiko, "HostKeys", FakeHostKeys)
    monkeypatch.setattr(paramiko, "Transport", FakeTransport)
    monkeypatch.setattr("services.gpu_direct.connection.socket.create_connection", lambda *_args, **_kwargs: FakeSocket())

    env = {
        "GPU_DIRECT_TIMEOUT_SECONDS": "8",
        "SSH_KNOWN_HOSTS_PATH": "/tmp/known_hosts",
    }
    target = Target(name="akki-vm", host="41.173.184.244", port=22, username="ubuntu", password="secret")
    _client, receipt = connect_target(target, environ=env, timeout=8)
    assert receipt["status"] == "DIRECT_PASSWORD_METHOD_NOT_ALLOWED"
    assert receipt["allowed_methods"] == ["publickey"]
    assert "secret" not in str(receipt)
