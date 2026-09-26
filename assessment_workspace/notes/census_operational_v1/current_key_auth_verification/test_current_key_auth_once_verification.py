"""Offline verification of owner-authorized current-key auth diagnostic.

MOCKED transport/socket tests only. No live network calls.
"""

from __future__ import annotations

import importlib.util
import json
import os
import socket
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path("/app")
SCRIPT_PATH = ROOT / "assessment_workspace/tools/current_key_auth_once.py"
LIVE_RESULT_PATH = ROOT / "assessment_workspace/notes/census_operational_v1/CURRENT_KEY_AUTH_LIVE_RESULT.json"
LIVE_DIR = ROOT / "assessment_workspace/phase0/drill_receipts/census_operational_v1/execution_recovery/current_key_auth_owner_authorized_v1"


def _load_module():
    spec = importlib.util.spec_from_file_location("current_key_auth_once_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _live_rows_by_host():
    payload = json.loads(LIVE_RESULT_PATH.read_text(encoding="utf-8"))
    return {row["host_alias"]: row for row in payload["results"]}, payload


def test_live_receipts_match_summary_and_owner_scope_flags():
    """Real receipts: summary and per-host artifacts are internally consistent."""
    rows_by_host, payload = _live_rows_by_host()

    assert payload["application_and_env_unchanged"] is True
    assert payload["no_keys_generated_or_modified"] is True
    assert payload["no_remote_commands_or_channels"] is True
    assert set(rows_by_host) == {"akki-vm", "akki-vm-ii"}

    for host in ("akki-vm", "akki-vm-ii"):
        intent = json.loads((LIVE_DIR / f"{host}.intent.json").read_text(encoding="utf-8"))
        result = json.loads((LIVE_DIR / f"{host}.result.json").read_text(encoding="utf-8"))
        summary = rows_by_host[host]

        assert intent["bypass"] == "local_client_fingerprint_equality_only"
        assert intent["commands_allowed"] is False
        assert intent["channels_allowed"] is False
        assert intent["password_fallback_allowed"] is False
        assert intent["retries_allowed"] is False

        assert result == summary
        assert result["tcp_connected"] is True
        assert result["server_pin_matched"] is True
        assert result["publickey_auth_attempts"] == 1
        assert result["authenticated"] is False
        assert result["remote_channels_opened"] == 0
        assert result["remote_commands"] == 0
        assert result["status"] == "AUTHENTICATION_REJECTED"
        assert result["error_type"] == "AuthenticationException"
        assert result["error_message"] == "Authentication failed."


def test_prepare_uses_existing_key_and_keeps_mismatch_metadata_without_refusal():
    """Real local-reads only: mismatch in admission/current key does not block diagnostic."""
    m = _load_module()
    rows_by_host, _ = _live_rows_by_host()

    for host in ("akki-vm", "akki-vm-ii"):
        try:
            _cfg, _key, _pinned, meta = m.prepare(host)
        except Exception as exc:
            pytest.skip(f"prepare({host}) unavailable in this offline env: {exc}")
        live = rows_by_host[host]
        assert meta["available_client_fingerprint"] == live["available_client_fingerprint"]
        assert meta["expected_client_fingerprint"] == live["expected_client_fingerprint"]
        assert meta["client_identity_matches_admission"] is False


def test_prepare_bypasses_only_identity_equality_check_not_receipt_or_permissions(monkeypatch, tmp_path):
    """Bypass scope is narrow: no verify_identity call; receipt/key loaders still mandatory."""
    m = _load_module()

    host = "akki-vm"
    slug = "AKKI_VM"
    cfg = SimpleNamespace(name=host, slug=slug, host="10.0.0.10", port=22, username="ubuntu", key_path="/tmp/key")
    monkeypatch.setattr(m, "AUTHORIZED_HOSTS", (host,))
    monkeypatch.setattr(m.ssh_seam, "get_host_config", lambda _h: cfg)

    monkeypatch.setenv(f"{slug}_HOST", cfg.host)
    monkeypatch.setenv(f"{slug}_PORT", str(cfg.port))
    monkeypatch.setenv(f"{slug}_USERNAME", cfg.username)
    monkeypatch.setenv(f"{slug}_SSH_PRIVATE_KEY_PATH", cfg.key_path)

    known_hosts = tmp_path / "known_hosts"
    known_hosts.write_text("dummy", encoding="utf-8")
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", str(known_hosts))

    calls = {"expected": 0, "load": 0, "verify_identity": 0}

    class _FakeKey:
        def asbytes(self):
            return b"key-bytes"

    class _FakeHostKeys:
        def __init__(self, *_args, **_kwargs):
            pass

        def lookup(self, token):
            assert token == cfg.host
            return {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"pin")}

    monkeypatch.setattr(m.identity, "_expected_fingerprint", lambda _cfg: calls.__setitem__("expected", calls["expected"] + 1) or "SHA256:expected")
    monkeypatch.setattr(m.identity, "_load_key", lambda _path: calls.__setitem__("load", calls["load"] + 1) or _FakeKey())
    monkeypatch.setattr(
        m.identity,
        "verify_identity",
        lambda _cfg: calls.__setitem__("verify_identity", calls["verify_identity"] + 1) or (_ for _ in ()).throw(AssertionError("must not call verify_identity")),
    )
    monkeypatch.setattr(m.identity, "_fingerprint", lambda b: "SHA256:current" if b == b"key-bytes" else "SHA256:server")
    monkeypatch.setattr(m.paramiko, "HostKeys", _FakeHostKeys)

    _cfg, key, pinned, meta = m.prepare(host)
    assert key.asbytes() == b"key-bytes"
    assert "ssh-ed25519" in pinned
    assert meta["client_identity_matches_admission"] is False
    assert calls == {"expected": 1, "load": 1, "verify_identity": 0}


def test_prepare_refuses_without_explicit_host_env(monkeypatch):
    """Diagnostic requires values to come from explicit existing env for that host."""
    m = _load_module()
    host = "akki-vm"
    slug = "AKKI_VM"
    cfg = SimpleNamespace(name=host, slug=slug, host="10.0.0.11", port=22, username="ubuntu", key_path="/tmp/key")
    monkeypatch.setattr(m, "AUTHORIZED_HOSTS", (host,))
    monkeypatch.setattr(m.ssh_seam, "get_host_config", lambda _h: cfg)
    monkeypatch.delenv(f"{slug}_HOST", raising=False)

    with pytest.raises(ValueError) as exc:
        m.prepare(host)
    assert str(exc.value) == "EXPLICIT_HOST_CONFIGURATION_REQUIRED"


def _patch_socket_and_transport(monkeypatch, m, transport_cls, sock_obj):
    monkeypatch.setattr(m.socket, "create_connection", lambda *_args, **_kwargs: sock_obj)
    monkeypatch.setattr(m.paramiko, "Transport", transport_cls)


def test_authenticate_server_pin_missing_algorithms_means_zero_auth_attempts(monkeypatch):
    """No pinned-compatible host-key algorithm => no auth attempt is sent."""
    m = _load_module()
    cfg = SimpleNamespace(host="h", port=22, username="u")
    key = object()
    closed = {"sock": 0, "transport": 0}

    class Sock:
        def close(self):
            closed["sock"] += 1

    class Transport:
        def __init__(self, _sock):
            self.banner_timeout = self.auth_timeout = self.handshake_timeout = None

        def set_log_channel(self, _):
            return None

        def get_security_options(self):
            return SimpleNamespace(key_types=["ssh-ed25519", "rsa-sha2-512"])

        def close(self):
            closed["transport"] += 1

    _patch_socket_and_transport(monkeypatch, m, Transport, Sock())
    result = m.authenticate(cfg, key, pinned={})
    assert result["status"] == "PINNED_SERVER_ALGORITHM_UNAVAILABLE"
    assert result["publickey_auth_attempts"] == 0
    assert result["stage"] == "tcp_connect"
    assert closed == {"sock": 1, "transport": 1}


def test_authenticate_server_pin_verified_before_publickey_and_partial_auth_not_success(monkeypatch):
    """Pinned server verification precedes auth_publickey; partial auth remains unauthenticated."""
    m = _load_module()
    cfg = SimpleNamespace(host="h", port=22, username="u")
    key = object()
    events = []

    class Sock:
        def close(self):
            events.append("sock_close")

    class ServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"server-bytes"

    class Transport:
        def __init__(self, _sock):
            events.append("transport_ctor")

        def set_log_channel(self, _):
            return None

        def get_security_options(self):
            return SimpleNamespace(key_types=["ssh-ed25519", "rsa-sha2-512"])

        def start_client(self, timeout):
            events.append(("start_client", timeout))

        def get_remote_server_key(self):
            events.append("get_remote_server_key")
            return ServerKey()

        def auth_publickey(self, username, pkey):
            events.append(("auth_publickey", username, pkey is key))
            return ["password", "none", "not-allowlisted"]

        def is_authenticated(self):
            return False

        def close(self):
            events.append("transport_close")

    pinned = {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"server-bytes")}
    _patch_socket_and_transport(monkeypatch, m, Transport, Sock())
    monkeypatch.setattr(m.identity, "_fingerprint", lambda _b: "SHA256:server")

    result = m.authenticate(cfg, key, pinned)
    assert result["server_pin_matched"] is True
    assert result["publickey_auth_attempts"] == 1
    assert result["authenticated"] is False
    assert result["status"] == "ADDITIONAL_AUTH_REQUIRED"
    assert result["next_auth_methods"] == ["none", "password"]
    assert events.index("get_remote_server_key") < next(i for i, e in enumerate(events) if isinstance(e, tuple) and e[0] == "auth_publickey")


def test_authenticate_success_sets_authenticated_state_only_when_transport_authenticated(monkeypatch):
    """Success state requires transport.is_authenticated() == True."""
    m = _load_module()
    cfg = SimpleNamespace(host="h", port=22, username="u")

    class Sock:
        def close(self):
            return None

    class ServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"server-bytes"

    class Transport:
        def __init__(self, _sock):
            return None

        def set_log_channel(self, _):
            return None

        def get_security_options(self):
            return SimpleNamespace(key_types=["ssh-ed25519"])

        def start_client(self, timeout):
            return None

        def get_remote_server_key(self):
            return ServerKey()

        def auth_publickey(self, username, pkey):
            return []

        def is_authenticated(self):
            return True

        def close(self):
            return None

    _patch_socket_and_transport(monkeypatch, m, Transport, Sock())
    monkeypatch.setattr(m.identity, "_fingerprint", lambda _b: "SHA256:server")
    result = m.authenticate(cfg, object(), {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"server-bytes")})
    assert result["status"] == "AUTHENTICATED"
    assert result["authenticated"] is True


def test_authenticate_auth_exception_message_allowlist_and_timeout_stage(monkeypatch):
    """AuthenticationException text is allowlisted; timeout keeps stage/attempt count."""
    m = _load_module()
    cfg = SimpleNamespace(host="h", port=22, username="u")

    class Sock:
        def close(self):
            return None

    class ServerKey:
        def get_name(self):
            return "ssh-ed25519"

        def asbytes(self):
            return b"server-bytes"

    class TransportReject:
        def __init__(self, _sock):
            return None

        def set_log_channel(self, _):
            return None

        def get_security_options(self):
            return SimpleNamespace(key_types=["ssh-ed25519"])

        def start_client(self, timeout):
            return None

        def get_remote_server_key(self):
            return ServerKey()

        def auth_publickey(self, username, pkey):
            raise m.paramiko.AuthenticationException("provider-sensitive-detail")

        def close(self):
            return None

    _patch_socket_and_transport(monkeypatch, m, TransportReject, Sock())
    monkeypatch.setattr(m.identity, "_fingerprint", lambda _b: "SHA256:server")
    reject = m.authenticate(cfg, object(), {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"server-bytes")})
    assert reject["status"] == "AUTHENTICATION_REJECTED"
    assert reject["error_message"] == "SSH authentication did not succeed."

    class TransportTimeout(TransportReject):
        def auth_publickey(self, username, pkey):
            raise TimeoutError("local-timeout")

    _patch_socket_and_transport(monkeypatch, m, TransportTimeout, Sock())
    timeout = m.authenticate(cfg, object(), {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"server-bytes")})
    assert timeout["status"] == "TIMEOUT"
    assert timeout["stage"] == "publickey_authentication"
    assert timeout["publickey_auth_attempts"] == 1


def test_authenticate_closes_socket_and_transport_on_all_paths(monkeypatch):
    """Resource closure is enforced even on transport error paths."""
    m = _load_module()
    cfg = SimpleNamespace(host="h", port=22, username="u")
    closed = {"sock": 0, "transport": 0}

    class Sock:
        def close(self):
            closed["sock"] += 1

    class Transport:
        def __init__(self, _sock):
            return None

        def set_log_channel(self, _):
            return None

        def get_security_options(self):
            return SimpleNamespace(key_types=["ssh-ed25519"])

        def start_client(self, timeout):
            raise m.paramiko.SSHException("boom")

        def close(self):
            closed["transport"] += 1

    _patch_socket_and_transport(monkeypatch, m, Transport, Sock())
    result = m.authenticate(cfg, object(), {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"server-bytes")})
    assert result["status"] == "TRANSPORT_ERROR"
    assert closed == {"sock": 1, "transport": 1}


def test_run_once_claims_intent_exclusively_before_auth_and_passes_same_key(monkeypatch, tmp_path):
    """Intent claim must exist before any auth call; auth receives the prepared key object."""
    m = _load_module()
    host = "akki-vm"
    key_obj = object()
    config_obj = SimpleNamespace(host="h", port=22, username="u")
    pinned_obj = {"ssh-ed25519": SimpleNamespace(asbytes=lambda: b"s")}

    monkeypatch.setattr(m, "AUTHORIZED_HOSTS", (host,))
    monkeypatch.setattr(m.ssh_seam, "list_hosts", lambda: [host])
    monkeypatch.setattr(m, "DIRECTORY", tmp_path)
    monkeypatch.setattr(m, "prepare", lambda _host: (config_obj, key_obj, pinned_obj, {
        "host_alias": host,
        "expected_client_fingerprint": "SHA256:expected",
        "available_client_fingerprint": "SHA256:current",
        "client_identity_matches_admission": False,
    }))

    captured = {"called": 0, "key_same": False, "intent_exists": False}

    def _auth(cfg, key, pinned):
        captured["called"] += 1
        captured["key_same"] = key is key_obj
        captured["intent_exists"] = (tmp_path / f"{host}.intent.json").is_file()
        return {
            "tcp_connected": True,
            "server_pin_matched": True,
            "publickey_auth_attempts": 1,
            "authenticated": False,
            "remote_channels_opened": 0,
            "remote_commands": 0,
            "stage": "publickey_authentication",
            "status": "AUTHENTICATION_REJECTED",
        }

    monkeypatch.setattr(m, "authenticate", _auth)
    out = m.run_once()
    assert captured == {"called": 1, "key_same": True, "intent_exists": True}
    assert out[0]["host_alias"] == host


def test_run_once_replay_or_orphan_consumes_attempt_without_network(monkeypatch, tmp_path):
    """Pre-existing intent consumes authorization; no auth callback/network on replay/orphan."""
    m = _load_module()
    host = "akki-vm"
    monkeypatch.setattr(m, "AUTHORIZED_HOSTS", (host,))
    monkeypatch.setattr(m.ssh_seam, "list_hosts", lambda: [host])
    monkeypatch.setattr(m, "DIRECTORY", tmp_path)

    (tmp_path / f"{host}.intent.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(m, "authenticate", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("should not auth")))

    out = m.run_once()
    assert out == [{"host_alias": host, "status": "ATTEMPT_ALREADY_CONSUMED_OUTCOME_UNRECORDED"}]


def test_run_once_race_fileexists_consumes_attempt_without_auth(monkeypatch, tmp_path):
    """Intent create race (FileExistsError) must consume attempt with zero auth."""
    m = _load_module()
    host = "akki-vm"
    monkeypatch.setattr(m, "AUTHORIZED_HOSTS", (host,))
    monkeypatch.setattr(m.ssh_seam, "list_hosts", lambda: [host])
    monkeypatch.setattr(m, "DIRECTORY", tmp_path)
    monkeypatch.setattr(m, "prepare", lambda _host: (SimpleNamespace(), object(), {}, {
        "host_alias": host,
        "expected_client_fingerprint": "SHA256:expected",
        "available_client_fingerprint": "SHA256:current",
        "client_identity_matches_admission": False,
    }))

    def _write(path, payload):
        if str(path).endswith(".intent.json"):
            raise FileExistsError
        raise AssertionError("result write should not happen")

    monkeypatch.setattr(m, "_write_exclusive", _write)
    monkeypatch.setattr(m, "authenticate", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("should not auth")))

    out = m.run_once()
    assert out == [{"host_alias": host, "status": "ATTEMPT_ALREADY_CONSUMED"}]


def test_source_and_outputs_do_not_expose_secrets_literals():
    """No credential material should appear in script output artifact."""
    script_text = SCRIPT_PATH.read_text(encoding="utf-8")
    live_text = LIVE_RESULT_PATH.read_text(encoding="utf-8")

    forbidden = ["BEGIN OPENSSH PRIVATE KEY", "BEGIN RSA PRIVATE KEY", "AKKI_GPU_SSH_PASSWORD"]
    for marker in forbidden:
        assert marker not in script_text
        assert marker not in live_text
