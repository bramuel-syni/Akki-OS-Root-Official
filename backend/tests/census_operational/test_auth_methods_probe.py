"""RED-first tests for services.census_autonomy.auth_methods_probe diagnose_host/run_once."""

import importlib
import socket
from types import SimpleNamespace

import pytest


# Module and feature under test: missing module should fail RED-first until implementation lands.
def _load_probe_module():
    try:
        return importlib.import_module("services.census_autonomy.auth_methods_probe")
    except ModuleNotFoundError:
        pytest.fail(
            "RED-expected missing-module: services.census_autonomy.auth_methods_probe is not implemented yet",
            pytrace=False,
        )


KNOWN_METHODS = {
    "none",
    "publickey",
    "password",
    "keyboard-interactive",
    "hostbased",
    "gssapi-with-mic",
}


class _FakeServerKey:
    def __init__(self, key_name="ssh-rsa", raw=b"server-key"):
        self._key_name = key_name
        self._raw = raw

    def get_name(self):
        return self._key_name

    def asbytes(self):
        return self._raw


class _FakeBadAuthenticationType(Exception):
    def __init__(self, allowed_types):
        super().__init__("auth failed")
        self.allowed_types = allowed_types


def _base_config(port=22):
    return SimpleNamespace(name="akki-vm-ii", host="10.0.0.10", port=port, username="ubuntu")


def _install_probe_mocks(
    m,
    monkeypatch,
    *,
    known_hosts_records,
    remote_key,
    auth_none_effect,
):
    events = {
        "socket_ctor": 0,
        "socket_close": 0,
        "transport_close": 0,
        "auth_none_calls": 0,
        "auth_password_calls": 0,
        "private_key_load_calls": 0,
        "channel_calls": 0,
        "sftp_calls": 0,
        "exec_calls": 0,
        "timeouts": [],
        "connect_calls": [],
        "set_log_channel_calls": 0,
        "banner_timeout": None,
        "auth_timeout": None,
        "handshake_timeout": None,
        "key_types_before": None,
        "key_types_after": None,
    }

    class FakeSocket:
        def __init__(self, *_, **__):
            events["socket_ctor"] += 1

        def settimeout(self, value):
            events["timeouts"].append(value)

        def connect(self, addr):
            events["connect_calls"].append(addr)

        def close(self):
            events["socket_close"] += 1

    class FakeHostKeys:
        def __init__(self, *_, **__):
            self._records = known_hosts_records

        def load(self, *_):
            return self

        def lookup(self, host_alias):
            return self._records.get(host_alias)

        def get(self, host_alias, default=None):
            return self._records.get(host_alias, default)

    class FakeTransport:
        def __init__(self, _sock):
            self._server_key = remote_key
            self.security = SimpleNamespace(key_types=("ssh-ed25519", "rsa-sha2-512", "rsa-sha2-256", "ssh-rsa"))
            events["key_types_before"] = tuple(self.security.key_types)
            self.banner_timeout = None
            self.auth_timeout = None
            self.handshake_timeout = None

        def set_log_channel(self, _name):
            events["set_log_channel_calls"] += 1

        def get_security_options(self):
            return self.security

        def is_authenticated(self):
            return auth_none_effect is True

        def start_client(self, timeout=None):
            events["timeouts"].append(timeout)

        def get_remote_server_key(self):
            return self._server_key

        def auth_none(self, _username):
            events["auth_none_calls"] += 1
            if isinstance(auth_none_effect, Exception):
                raise auth_none_effect
            return [] if auth_none_effect is True else auth_none_effect

        def auth_password(self, *_args, **_kwargs):
            events["auth_password_calls"] += 1
            raise AssertionError("auth_password must never be attempted")

        def open_session(self, *_args, **_kwargs):
            events["channel_calls"] += 1
            raise AssertionError("channel/session must never be opened")

        def open_sftp_client(self, *_args, **_kwargs):
            events["sftp_calls"] += 1
            raise AssertionError("SFTP must never be opened")

        def exec_command(self, *_args, **_kwargs):
            events["exec_calls"] += 1
            raise AssertionError("exec_command must never be called")

        def close(self):
            events["banner_timeout"] = self.banner_timeout
            events["auth_timeout"] = self.auth_timeout
            events["handshake_timeout"] = self.handshake_timeout
            events["key_types_after"] = tuple(self.security.key_types)
            events["transport_close"] += 1

    class _FakePKeyLoader:
        @staticmethod
        def from_private_key_file(*_args, **_kwargs):
            events["private_key_load_calls"] += 1
            raise AssertionError("private key loading must never be attempted")

    fake_paramiko = SimpleNamespace(
        HostKeys=FakeHostKeys,
        Transport=FakeTransport,
        BadAuthenticationType=_FakeBadAuthenticationType,
        RSAKey=_FakePKeyLoader,
        Ed25519Key=_FakePKeyLoader,
        ECDSAKey=_FakePKeyLoader,
    )

    monkeypatch.setattr(m, "paramiko", fake_paramiko, raising=False)
    monkeypatch.setattr(m.socket, "create_connection", lambda addr, timeout=None: events["connect_calls"].append((addr, timeout)) or FakeSocket())

    return events


def _assert_exact_output_shape(payload):
    assert set(payload.keys()) == {
        "host_alias",
        "pin_match",
        "allowed_methods",
        "authenticated",
        "error_code",
    }


# Module+feature under test: known_hosts missing must fail safely before host verification.
def test_diagnose_known_hosts_missing_returns_known_hosts_unavailable(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.delenv("SSH_KNOWN_HOSTS_PATH", raising=False)
    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["error_code"] == "KNOWN_HOSTS_UNAVAILABLE"
    assert out["authenticated"] is False


# Module+feature under test: HostKeys load failure must not touch network.
def test_diagnose_known_hosts_load_failure_has_no_network_calls(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    connect_calls = []

    class BrokenHostKeys:
        def __init__(self, *_args, **_kwargs):
            raise OSError("known-hosts unreadable")

    fake_paramiko = SimpleNamespace(
        HostKeys=BrokenHostKeys,
        Transport=object,
        BadAuthenticationType=_FakeBadAuthenticationType,
    )
    monkeypatch.setattr(m, "paramiko", fake_paramiko, raising=False)
    monkeypatch.setattr(m.socket, "create_connection", lambda *_a, **_k: connect_calls.append("called"))

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["error_code"] == "KNOWN_HOSTS_UNAVAILABLE"
    assert connect_calls == []


# Module+feature under test: missing host pin refuses without creating socket.
def test_diagnose_missing_host_pin_refuses_without_socket(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config(port=22)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={},
        remote_key=_FakeServerKey(),
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["error_code"] == "HOST_KEY_MISSING"
    assert events["connect_calls"] == []


# Module+feature under test: host alias lookup must use host for 22 and [host]:port otherwise.
@pytest.mark.parametrize(
    "port, expected_alias",
    [
        (22, "10.0.0.10"),
        (2202, "[10.0.0.10]:2202"),
    ],
)
def test_diagnose_host_alias_selection(monkeypatch, port, expected_alias):
    m = _load_probe_module()
    cfg = _base_config(port=port)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin_key = _FakeServerKey(key_name="ssh-rsa", raw=b"pin")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={expected_alias: {"ssh-rsa": pin_key}},
        remote_key=pin_key,
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    # The lookup uses host/[host]:port, but outward receipts expose alias only.
    assert out["host_alias"] == cfg.name
    assert len(events["connect_calls"]) == 1


# Module+feature under test: changed host key refuses before auth_none.
def test_diagnose_changed_host_key_refuses_before_auth_none(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pinned = _FakeServerKey(key_name="ssh-rsa", raw=b"pin-a")
    remote = _FakeServerKey(key_name="ssh-rsa", raw=b"pin-b")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pinned}},
        remote_key=remote,
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["error_code"] == "HOST_KEY_CHANGED"
    assert events["auth_none_calls"] == 0


# Module+feature under test: unsupported pin algorithms must not attempt auth_none.
def test_diagnose_unsupported_pin_algorithm_does_not_auth(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    unsupported = _FakeServerKey(key_name="ssh-dss", raw=b"dss")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-dss": unsupported}},
        remote_key=unsupported,
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["authenticated"] is False
    assert out["pin_match"] is False or out["error_code"]
    assert events["auth_none_calls"] == 0


# Module+feature under test: matching pin + BadAuthenticationType(publickey) returns advertised methods only.
def test_diagnose_bad_auth_type_publickey_exposes_allowed_methods(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["pin_match"] is True
    assert out["authenticated"] is False
    assert out["allowed_methods"] == ["publickey"]
    assert events["auth_password_calls"] == 0


# Module+feature under test: password-advertised auth_none path must not trigger password auth attempts.
def test_diagnose_password_advertised_does_not_attempt_password(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=_FakeBadAuthenticationType(["password", "totp-custom", "publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["allowed_methods"] == ["password", "publickey"]
    assert all(method in KNOWN_METHODS for method in out["allowed_methods"])
    assert events["auth_password_calls"] == 0


# Module+feature under test: pinned rsa permits only rsa-sha2/rsa key types, excluding unrelated algorithms.
def test_diagnose_rsa_pin_restricts_key_types(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=_FakeBadAuthenticationType(["publickey"]),
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["pin_match"] is True
    assert events["key_types_after"] == ("rsa-sha2-512", "rsa-sha2-256", "ssh-rsa")
    assert "ssh-ed25519" not in events["key_types_after"]


# Module+feature under test: successful auth_none reports authenticated true with no channel operations.
def test_diagnose_successful_auth_none_no_channel_or_exec(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=True,
    )

    out = m.diagnose_host(cfg, timeout=8.0)
    _assert_exact_output_shape(out)
    assert out["authenticated"] is True
    assert out["error_code"] in (None, "")
    assert events["channel_calls"] == 0
    assert events["sftp_calls"] == 0
    assert events["exec_calls"] == 0
    assert out["allowed_methods"] == []


# Module+feature under test: exceptions are sanitized and timeout value is applied consistently.
def test_diagnose_exception_sanitized_and_timeout_applied(monkeypatch):
    m = _load_probe_module()
    cfg = _base_config(port=2202)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"[10.0.0.10]:2202": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=RuntimeError("Server leaked: password=secret"),
    )

    out = m.diagnose_host(cfg, timeout=5.5)
    _assert_exact_output_shape(out)
    assert out["authenticated"] is False
    assert "secret" not in str(out["error_code"]).lower()
    assert out["error_code"]
    assert len(events["connect_calls"]) == 1
    assert events["connect_calls"][0][1] == 5.5
    assert events["set_log_channel_calls"] == 1
    assert events["banner_timeout"] == 5.5
    assert events["auth_timeout"] == 5.5
    assert events["handshake_timeout"] == 5.5


# Module+feature under test: resources close on both success and failure; no private key loading.
@pytest.mark.parametrize("auth_effect", [True, RuntimeError("boom")])
def test_diagnose_always_closes_socket_and_transport(monkeypatch, auth_effect):
    m = _load_probe_module()
    cfg = _base_config()
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    pin = _FakeServerKey(key_name="ssh-rsa", raw=b"same")
    events = _install_probe_mocks(
        m,
        monkeypatch,
        known_hosts_records={"10.0.0.10": {"ssh-rsa": pin}},
        remote_key=pin,
        auth_none_effect=auth_effect,
    )

    m.diagnose_host(cfg, timeout=8.0)
    assert events["socket_close"] == 1
    assert events["transport_close"] == 1
    assert events["private_key_load_calls"] == 0


# Module+feature under test: run_once should enforce assessment_workspace-bounded diagnostic dir.
def test_run_once_rejects_diagnostic_dir_outside_assessment_workspace(monkeypatch):
    m = _load_probe_module()
    if not hasattr(m, "run_once"):
        pytest.skip("run_once not implemented yet")

    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", "/tmp/outside")
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", "a" * 64)
    with pytest.raises(Exception):
        m.run_once()
