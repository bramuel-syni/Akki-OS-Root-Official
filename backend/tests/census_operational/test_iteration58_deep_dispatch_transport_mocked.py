"""Iteration 58: deep_dispatch transport regressions (MOCKED transport only)."""

# Module focus: census_autonomy.deep_dispatch SSH channel drain/exit/budget behavior.

import hashlib
import json
import time
from types import SimpleNamespace

import pytest

from services.census_autonomy import deep_dispatch


class _FakeServerKey:
    def asbytes(self):
        return b"iteration58-server-key"


class _FakeChannel:
    def __init__(self, stdout_chunks, stderr_chunks, exit_code=0, exit_ready=True):
        self.stdout_chunks = list(stdout_chunks)
        self.stderr_chunks = list(stderr_chunks)
        self.exit_code = exit_code
        self.exit_ready = exit_ready
        self.closed = False
        self.timeout = None
        self.exit_status_calls = 0

    def settimeout(self, timeout):
        self.timeout = timeout

    def exec_command(self, _command):
        return None

    def sendall(self, _payload):
        return None

    def shutdown_write(self):
        return None

    def recv_ready(self):
        return bool(self.stdout_chunks)

    def recv(self, _size):
        return self.stdout_chunks.pop(0)

    def recv_stderr_ready(self):
        return bool(self.stderr_chunks)

    def recv_stderr(self, _size):
        return self.stderr_chunks.pop(0)

    def exit_status_ready(self):
        return self.exit_ready

    def recv_exit_status(self):
        self.exit_status_calls += 1
        return self.exit_code

    def close(self):
        self.closed = True


class _FakeTransport:
    def __init__(self, channel):
        self.channel = channel

    def open_session(self, timeout=15):
        _ = timeout
        return self.channel

    def get_remote_server_key(self):
        return _FakeServerKey()

    def set_keepalive(self, seconds):
        self.keepalive = seconds


class _FakeClient:
    def __init__(self, channel):
        self.transport = _FakeTransport(channel)
        self.client_closed = False

    def get_transport(self):
        return self.transport

    def close(self):
        self.client_closed = True


def _worker_payload(code_hash: str, runtime_id: str):
    body = {
        "status": "complete",
        "source_rows_returned": 12,
        "worker": {
            "code_sha256": code_hash,
            "runtime_id": runtime_id,
        },
        "sources": [],
    }
    digest = "cwr-" + hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
    value = dict(body)
    value["worker_receipt_id"] = digest
    return value


@pytest.fixture
def _mock_dispatch_runtime(monkeypatch, tmp_path):
    monkeypatch.setenv("CENSUS_REMOTE_PYTHON", "/usr/bin/python3")

    monkeypatch.setattr(deep_dispatch.store, "get", lambda run_id, tenant: {"worker_id": "worker-1"})
    monkeypatch.setattr(deep_dispatch.store, "now", lambda: "2026-02-01T00:00:00Z")
    monkeypatch.setattr(deep_dispatch.store, "cursor_dir", lambda: tmp_path)

    monkeypatch.setattr(deep_dispatch, "connector_for", lambda *_args, **_kwargs: {"driver": "mock", "source_id": "rms_mysql"})
    monkeypatch.setattr(deep_dispatch, "build_bundle", lambda: ("print('ok')", "hash-iteration58"))

    import services.training_runner.ssh_seam as ssh_seam

    monkeypatch.setattr(ssh_seam, "list_hosts", lambda: ["worker-1", "worker-2"])


def test_i58_transport_drains_stdout_and_stderr_before_exit_status(_mock_dispatch_runtime, monkeypatch):
    """When exit status is ready early, streams are still fully drained before status read."""
    payload = _worker_payload(code_hash="hash-iteration58", runtime_id="worker-1")
    stdout = json.dumps(payload).encode()
    channel = _FakeChannel(
        stdout_chunks=[stdout[:40], stdout[40:]],
        stderr_chunks=[b"ValueError: sample\n" + b"x" * 70000],
        exit_code=0,
        exit_ready=True,
    )
    client = _FakeClient(channel)

    monkeypatch.setattr(
        deep_dispatch,
        "_connect",
        lambda runtime, timeout: (client, SimpleNamespace(hostname_expected=f"{runtime}.example")),
    )

    result = deep_dispatch.execute_source(
        run_id="cr-i58-1",
        tenant="RMS",
        source="digicow_rds",
        lawful_hash="lawful-hash",
        deadline=time.time() + 20,
    )

    assert result["status"] == "complete"
    assert result["worker"]["transport_verified"] is True
    assert result["transport_diagnostic"]["stdout_bytes"] == len(stdout)
    assert result["transport_diagnostic"]["stderr_bytes"] == 65536
    assert channel.exit_status_calls == 1
    assert client.client_closed is True
    assert result["worker"]["server_key_sha256"] == hashlib.sha256(b"iteration58-server-key").hexdigest()


@pytest.mark.parametrize("exit_code", [1, -1])
def test_i58_transport_refuses_nonzero_or_negative_exit_codes(_mock_dispatch_runtime, monkeypatch, exit_code):
    """Non-zero/negative worker exit status must be refused as REMOTE_WORKER_FAILED."""
    channel = _FakeChannel(stdout_chunks=[b"{}"], stderr_chunks=[b"RuntimeError: fail\n"], exit_code=exit_code, exit_ready=True)
    client = _FakeClient(channel)
    monkeypatch.setattr(
        deep_dispatch,
        "_connect",
        lambda runtime, timeout: (client, SimpleNamespace(hostname_expected=f"{runtime}.example")),
    )

    result = deep_dispatch.execute_source(
        run_id=f"cr-i58-exit-{exit_code}",
        tenant="RMS",
        source="digicow_rds",
        lawful_hash="lawful-hash",
        deadline=time.time() + 20,
    )

    assert result["reason_code"] == "REMOTE_WORKER_FAILED"
    assert result["transport_diagnostic"]["exit_code"] == exit_code


def test_i58_budget_recalculated_after_connection_and_build(_mock_dispatch_runtime, monkeypatch):
    """Budget should be recalculated after connect/build and stop when exhausted."""
    channel = _FakeChannel(stdout_chunks=[], stderr_chunks=[], exit_code=0, exit_ready=False)
    client = _FakeClient(channel)
    calls = {"connect": 0, "build": 0}

    def _fake_connect(runtime, timeout):
        calls["connect"] += 1
        assert timeout == 11
        return client, SimpleNamespace(hostname_expected=f"{runtime}.example")

    def _fake_build_bundle():
        calls["build"] += 1
        return "print('ok')", "hash-iteration58"

    class _Clock:
        def __init__(self):
            self.values = iter([100, 108])

        def __call__(self):
            return next(self.values)

    monkeypatch.setattr(deep_dispatch, "_connect", _fake_connect)
    monkeypatch.setattr(deep_dispatch, "build_bundle", _fake_build_bundle)
    monkeypatch.setattr(deep_dispatch.time, "time", _Clock())

    result = deep_dispatch.execute_source(
        run_id="cr-i58-budget",
        tenant="RMS",
        source="digicow_rds",
        lawful_hash="lawful-hash",
        deadline=111,
    )

    assert result["reason_code"] == "BUDGET_EXHAUSTED"
    assert calls == {"connect": 1, "build": 1}


def test_i58_transport_timeout_is_bounded_and_classified(_mock_dispatch_runtime, monkeypatch):
    """Non-terminating channel must time out with WORKER_DEADLINE and diagnostics."""
    channel = _FakeChannel(stdout_chunks=[], stderr_chunks=[], exit_code=0, exit_ready=False)
    client = _FakeClient(channel)
    monkeypatch.setattr(
        deep_dispatch,
        "_connect",
        lambda runtime, timeout: (client, SimpleNamespace(hostname_expected=f"{runtime}.example")),
    )

    class _LoopClock:
        def __init__(self):
            self.values = [100, 100, 100, 101, 102, 106]
            self.idx = 0

        def __call__(self):
            if self.idx >= len(self.values):
                return self.values[-1]
            value = self.values[self.idx]
            self.idx += 1
            return value

    monkeypatch.setattr(deep_dispatch.time, "time", _LoopClock())

    result = deep_dispatch.execute_source(
        run_id="cr-i58-timeout",
        tenant="RMS",
        source="digicow_rds",
        lawful_hash="lawful-hash",
        deadline=105,
    )

    assert result["reason_code"] == "WORKER_DEADLINE"
    assert result["transport_diagnostic"]["stdout_bytes"] == 0
    assert result["transport_diagnostic"]["stderr_bytes"] == 0
    assert channel.closed is True
