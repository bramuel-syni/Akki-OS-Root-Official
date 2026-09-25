"""RED-first execution identity recovery tests (R01-R08). MOCKED transport; no estate hosts."""

import base64
import hashlib
import importlib
import json
import os
import stat
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


# Module under test (proposed): services.census_autonomy.execution_identity
def _load_execution_identity_module():
    try:
        return importlib.import_module("services.census_autonomy.execution_identity")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "RED-expected missing-module: services.census_autonomy.execution_identity is not implemented yet",
            pytrace=False,
        )


# Feature under test: SSH public key fingerprint shape used by receipt pinning.
def _openssh_sha256_fingerprint_from_public_line(public_line: str) -> str:
    parts = public_line.strip().split()
    key_b64 = parts[1]
    raw = base64.b64decode(key_b64.encode("ascii"))
    return "SHA256:" + base64.b64encode(hashlib.sha256(raw).digest()).decode("ascii").rstrip("=")


# Feature under test: fake-key fixtures only (test-only; never custody material).
def _write_fake_keypair(tmp_path: Path, stem: str, monkeypatch):
    import paramiko

    private_path = tmp_path / f"{stem}_id_rsa"
    key = paramiko.RSAKey.generate(1024)
    key.write_private_key_file(str(private_path))
    private_path.chmod(0o600)

    public_line = f"{key.get_name()} {key.get_base64()} {stem}@test"
    public_path = tmp_path / f"{stem}_id_rsa.pub"
    public_path.write_text(public_line + "\n")

    # Keep this test process as owner for owner-only checks.
    monkeypatch.setenv("PYTHONWARNINGS", os.environ.get("PYTHONWARNINGS", "default"))
    return private_path, public_path, public_line


# Module+feature under test: verify_identity(config) strict receipt pin checks.
def test_r01_verify_identity_matching_receipt_returns_paramiko_pkey(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "match", monkeypatch)

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    slug = "AKKI_VM_II"
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
    pkey = m.verify_identity(cfg)

    import paramiko

    assert isinstance(pkey, paramiko.PKey)


def test_r02_different_key_same_path_refused_with_reason_code(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, _ = _write_fake_keypair(tmp_path, "actual", monkeypatch)
    _, _, pinned_public_line = _write_fake_keypair(tmp_path, "pinned", monkeypatch)

    receipt = {
        "public_key_line": pinned_public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(pinned_public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    slug = "AKKI_VM_II"
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert getattr(exc.value, "reason_code", "")


@pytest.mark.parametrize(
    "receipt_payload, expected_reason",
    [
        (None, "IDENTITY_RECEIPT_MISSING"),
        ("{not-json", "IDENTITY_RECEIPT_MALFORMED"),
        ({"public_key_line": "ssh-rsa AAA"}, "IDENTITY_RECEIPT_MALFORMED"),
    ],
)
def test_r03_receipt_missing_or_malformed_refused_closed(tmp_path, monkeypatch, receipt_payload, expected_reason):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "r03", monkeypatch)
    slug = "AKKI_VM_II"

    receipt_path = tmp_path / "receipt.json"
    if receipt_payload is None:
        # Intentionally do not create file.
        pass
    elif isinstance(receipt_payload, str):
        receipt_path.write_text(receipt_payload)
    else:
        payload = dict(receipt_payload)
        payload.setdefault("public_key_fingerprint", _openssh_sha256_fingerprint_from_public_line(public_line))
        receipt_path.write_text(json.dumps(payload))

    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    if receipt_path.exists():
        monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())
    else:
        monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", "deadbeef")

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert expected_reason in getattr(exc.value, "reason_code", "")


def test_r03_receipt_hash_mismatch_refused_closed(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "hash", monkeypatch)

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    slug = "AKKI_VM_II"
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", "0" * 64)
    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")

    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert "HASH" in getattr(exc.value, "reason_code", "")


def test_r04_key_symlink_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    target_private, _, public_line = _write_fake_keypair(tmp_path, "target", monkeypatch)
    symlink_private = tmp_path / "symlink_id_rsa"
    symlink_private.symlink_to(target_private)

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    slug = "AKKI_VM_II"
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(symlink_private), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert "SYMLINK" in getattr(exc.value, "reason_code", "")


def test_r04_key_permissions_too_open_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "perm", monkeypatch)
    private_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    slug = "AKKI_VM_II"
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())
    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")

    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert "PERMISSION" in getattr(exc.value, "reason_code", "")


def test_r05_password_auth_cannot_fallback_for_census_identity(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    cfg = SimpleNamespace(name="akki-vm-ii", slug="AKKI_VM_II", key_path=None, auth_method="password")
    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert "PASSWORD" in getattr(exc.value, "reason_code", "")


def test_r06_connect_must_verify_identity_before_sshclient_construction(monkeypatch):
    from services.census_autonomy import remote_dispatch

    events = []
    sentinel_pkey = object()

    fake_cfg = SimpleNamespace(
        host="127.0.0.1",
        port=22,
        username="ubuntu",
        auth_method="key",
        key_path="/tmp/test-only-id",
        hostname_expected="test-host",
        name="akki-vm-ii",
        slug="AKKI_VM_II",
    )

    monkeypatch.setattr(remote_dispatch.ssh_seam, "get_host_config", lambda host: fake_cfg)
    monkeypatch.setattr(remote_dispatch, "execution_identity", SimpleNamespace(verify_identity=lambda cfg: events.append("verify") or sentinel_pkey), raising=False)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-only-known-hosts")

    class _RejectPolicy:
        pass

    class _FakeClient:
        def __init__(self):
            events.append("client_ctor")

        def load_host_keys(self, _):
            events.append("load_host_keys")

        def set_missing_host_key_policy(self, _):
            events.append("set_policy")

        def connect(self, **kwargs):
            events.append(("connect", kwargs))

        def close(self):
            events.append("close")

    fake_paramiko = SimpleNamespace(SSHClient=_FakeClient, RejectPolicy=_RejectPolicy)
    monkeypatch.setitem(sys.modules, "paramiko", fake_paramiko)

    remote_dispatch._connect("akki-vm-ii", timeout=5)
    assert events.index("verify") < events.index("client_ctor")


def test_r06_connect_uses_pkey_not_key_filename_or_password(monkeypatch):
    from services.census_autonomy import remote_dispatch

    sentinel_pkey = object()
    captured = {}

    fake_cfg = SimpleNamespace(
        host="127.0.0.1",
        port=22,
        username="ubuntu",
        auth_method="key",
        key_path="/tmp/test-only-id",
        hostname_expected="test-host",
        name="akki-vm-ii",
        slug="AKKI_VM_II",
    )

    monkeypatch.setattr(remote_dispatch.ssh_seam, "get_host_config", lambda host: fake_cfg)
    monkeypatch.setattr(remote_dispatch, "execution_identity", SimpleNamespace(verify_identity=lambda cfg: sentinel_pkey), raising=False)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-only-known-hosts")

    class _RejectPolicy:
        pass

    class _FakeClient:
        def load_host_keys(self, _):
            return None

        def set_missing_host_key_policy(self, _):
            return None

        def connect(self, **kwargs):
            captured.update(kwargs)

        def close(self):
            return None

    fake_paramiko = SimpleNamespace(SSHClient=_FakeClient, RejectPolicy=_RejectPolicy)
    monkeypatch.setitem(sys.modules, "paramiko", fake_paramiko)

    remote_dispatch._connect("akki-vm-ii", timeout=7)
    assert captured.get("pkey") is sentinel_pkey
    assert "key_filename" not in captured
    assert "password" not in captured
    assert captured.get("allow_agent") is False and captured.get("look_for_keys") is False


def test_r07_execute_source_identity_refusal_banked_without_network(monkeypatch, tmp_path):
    from services.census_autonomy import remote_dispatch

    # Only the typed local refusal may contribute a public reason_code;
    # arbitrary provider exception attributes are never trusted as safe text.
    from services.census_autonomy.execution_identity import IdentityVerificationError
    attempts = {}

    monkeypatch.setattr(remote_dispatch.ssh_seam, "list_hosts", lambda: ["akki-vm-ii"])
    monkeypatch.setattr(remote_dispatch, "_connect", lambda *args, **kwargs: (_ for _ in ()).throw(IdentityVerificationError("IDENTITY_PIN_MISMATCH")))
    monkeypatch.setattr(remote_dispatch.store, "get", lambda run_id, tenant: {"source_hosts": {}})
    monkeypatch.setattr(remote_dispatch.store, "now", lambda: "2026-09-25T00:00:00Z")

    def _fake_bank(run_id, source, payload):
        attempts["payload"] = payload

    monkeypatch.setattr(remote_dispatch, "_bank_transport", _fake_bank)

    out = remote_dispatch.execute_source("cr-red", "RMS", "rms_mysql", "lawful", deadline=10**10)
    assert out["status"] == "blocked"
    assert out["reason_code"] == "AKKI_EXECUTION_IDENTITY_NOT_VERIFIED"
    assert attempts["payload"][0].get("reason_code") == "IDENTITY_PIN_MISMATCH"


def test_r08_transport_path_does_not_construct_network_payload_on_identity_refusal(monkeypatch):
    from services.census_autonomy import remote_dispatch

    monkeypatch.setattr(remote_dispatch.ssh_seam, "list_hosts", lambda: ["akki-vm-ii"])
    monkeypatch.setattr(remote_dispatch, "_connect", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("identity refused")))
    monkeypatch.setattr(remote_dispatch.store, "get", lambda run_id, tenant: {"source_hosts": {}})
    monkeypatch.setattr(remote_dispatch.store, "now", lambda: "2026-09-25T00:00:00Z")

    payloads = []
    monkeypatch.setattr(remote_dispatch, "_bank_transport", lambda run_id, source, attempts: payloads.append(attempts))

    result = remote_dispatch.execute_source("cr-red-2", "RMS", "rms_mysql", "lawful", deadline=10**10)
    assert result["status"] == "blocked"
    assert payloads and payloads[-1][0]["transport"] == "not_verified"


def test_r03_missing_receipt_path_or_pin_hash_env_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "missing-env", monkeypatch)
    slug = "AKKI_VM_II"

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")

    monkeypatch.delenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", raising=False)
    monkeypatch.delenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", raising=False)
    with pytest.raises(m.IdentityVerificationError) as exc1:
        m.verify_identity(cfg)
    assert exc1.value.reason_code == "IDENTITY_RECEIPT_MISSING"

    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.delenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", raising=False)
    with pytest.raises(m.IdentityVerificationError) as exc2:
        m.verify_identity(cfg)
    assert exc2.value.reason_code == "IDENTITY_RECEIPT_HASH_MISMATCH"


def test_r03_changed_receipt_bytes_after_pin_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "receipt-change", monkeypatch)
    slug = "AKKI_VM_II"

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))
    pinned_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", pinned_hash)

    # Mutate after pinning.
    receipt["note"] = "mutated"
    receipt_path.write_text(json.dumps(receipt))

    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert exc.value.reason_code == "IDENTITY_RECEIPT_HASH_MISMATCH"


def test_r03_receipt_fingerprint_contradicts_public_line_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, public_line = _write_fake_keypair(tmp_path, "receipt-contradict", monkeypatch)
    slug = "AKKI_VM_II"

    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())
    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")

    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert exc.value.reason_code == "IDENTITY_RECEIPT_MALFORMED"


def test_r04_pub_sidecar_mismatch_is_not_trusted(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    private_path, _, _ = _write_fake_keypair(tmp_path, "actual-sidecar", monkeypatch)
    _, _, admitted_public_line = _write_fake_keypair(tmp_path, "admitted-sidecar", monkeypatch)
    slug = "AKKI_VM_II"

    # Sidecar carries admitted key, but private key is different.
    Path(str(private_path) + ".pub").write_text(admitted_public_line + "\n")

    receipt = {
        "public_key_line": admitted_public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(admitted_public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))

    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())
    cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")

    with pytest.raises(m.IdentityVerificationError) as exc:
        m.verify_identity(cfg)
    assert exc.value.reason_code == "IDENTITY_PIN_MISMATCH"


def test_r04_missing_unreadable_invalid_encrypted_key_refused(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    slug = "AKKI_VM_II"

    _, _, public_line = _write_fake_keypair(tmp_path, "baseline", monkeypatch)
    receipt = {
        "public_key_line": public_line,
        "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
    monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())

    # Missing file.
    cfg_missing = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(tmp_path / "absent_id"), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc_missing:
        m.verify_identity(cfg_missing)
    assert exc_missing.value.reason_code == "IDENTITY_KEY_UNREADABLE"

    # Unreadable by mode.
    private_path, _, _ = _write_fake_keypair(tmp_path, "chmod-zero", monkeypatch)
    private_path.chmod(0)
    cfg_unreadable = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc_unreadable:
        m.verify_identity(cfg_unreadable)
    assert exc_unreadable.value.reason_code in {"IDENTITY_KEY_UNREADABLE", "IDENTITY_KEY_PERMISSIONS"}

    # Invalid key bytes.
    invalid_path = tmp_path / "invalid_id"
    invalid_path.write_text("not-a-private-key")
    invalid_path.chmod(0o600)
    cfg_invalid = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(invalid_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc_invalid:
        m.verify_identity(cfg_invalid)
    assert exc_invalid.value.reason_code == "IDENTITY_KEY_INVALID"

    # Encrypted key refuses (password prompt forbidden).
    import paramiko

    enc_path = tmp_path / "encrypted_id_rsa"
    enc_key = paramiko.RSAKey.generate(1024)
    enc_key.write_private_key_file(str(enc_path), password="test-passphrase")
    enc_path.chmod(0o600)
    cfg_encrypted = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(enc_path), auth_method="key")
    with pytest.raises(m.IdentityVerificationError) as exc_encrypted:
        m.verify_identity(cfg_encrypted)
    assert exc_encrypted.value.reason_code == "IDENTITY_KEY_LOCKED"


def test_r01_valid_rsa_and_ecdsa_and_exact_bytes(tmp_path, monkeypatch):
    m = _load_execution_identity_module()
    import paramiko

    slug = "AKKI_VM_II"
    key_specs = [
        ("rsa", paramiko.RSAKey.generate(1024)),
        ("ecdsa", paramiko.ECDSAKey.generate(bits=256)),
    ]

    for stem, key in key_specs:
        private_path = tmp_path / f"{stem}_id"
        key.write_private_key_file(str(private_path))
        private_path.chmod(0o600)
        public_line = f"{key.get_name()} {key.get_base64()} {stem}@test"
        receipt = {
            "public_key_line": public_line,
            "public_key_fingerprint": _openssh_sha256_fingerprint_from_public_line(public_line),
        }
        receipt_path = tmp_path / f"receipt_{stem}.json"
        receipt_path.write_text(json.dumps(receipt))

        monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_PATH", str(receipt_path))
        monkeypatch.setenv(f"{slug}_SSH_IDENTITY_RECEIPT_SHA256", hashlib.sha256(receipt_path.read_bytes()).hexdigest())

        cfg = SimpleNamespace(name="akki-vm-ii", slug=slug, key_path=str(private_path), auth_method="key")
        verified = m.verify_identity(cfg)
        parsed = paramiko.PKey.from_type_string(public_line.split()[0], base64.b64decode(public_line.split()[1]))
        assert verified.asbytes() == parsed.asbytes()


def test_r06_connect_refusal_does_not_construct_sshclient(monkeypatch):
    from services.census_autonomy import remote_dispatch
    from services.census_autonomy.execution_identity import IdentityVerificationError

    fake_cfg = SimpleNamespace(
        host="127.0.0.1",
        port=22,
        username="ubuntu",
        auth_method="key",
        key_path="/tmp/test-only-id",
        hostname_expected="test-host",
        name="akki-vm-ii",
        slug="AKKI_VM_II",
    )

    events = []
    monkeypatch.setattr(remote_dispatch.ssh_seam, "get_host_config", lambda host: fake_cfg)
    monkeypatch.setattr(
        remote_dispatch,
        "execution_identity",
        SimpleNamespace(verify_identity=lambda cfg: (_ for _ in ()).throw(IdentityVerificationError("IDENTITY_PIN_MISMATCH"))),
        raising=False,
    )

    class _ClientShouldNotConstruct:
        def __init__(self):
            events.append("client_ctor")

    fake_paramiko = SimpleNamespace(SSHClient=_ClientShouldNotConstruct, RejectPolicy=object)
    monkeypatch.setitem(sys.modules, "paramiko", fake_paramiko)

    with pytest.raises(IdentityVerificationError):
        remote_dispatch._connect("akki-vm-ii", timeout=5)
    assert "client_ctor" not in events


def test_r07_execute_source_does_not_leak_provider_reason_code_or_message(monkeypatch):
    from services.census_autonomy import remote_dispatch

    class ProviderLikeError(RuntimeError):
        def __init__(self):
            super().__init__("provider-detail-do-not-leak")
            self.reason_code = "PROVIDER_SECRET_REASON"

    monkeypatch.setattr(remote_dispatch.ssh_seam, "list_hosts", lambda: ["akki-vm-ii"])
    monkeypatch.setattr(remote_dispatch, "_connect", lambda *args, **kwargs: (_ for _ in ()).throw(ProviderLikeError()))
    monkeypatch.setattr(remote_dispatch.store, "get", lambda run_id, tenant: {"source_hosts": {}})
    monkeypatch.setattr(remote_dispatch.store, "now", lambda: "2026-09-25T00:00:00Z")

    banked = {}
    monkeypatch.setattr(remote_dispatch, "_bank_transport", lambda run_id, source, attempts: banked.setdefault("attempts", attempts))

    out = remote_dispatch.execute_source("cr-red-3", "RMS", "rms_mysql", "lawful", deadline=10**10)
    assert out["reason_code"] == "AKKI_EXECUTION_CONNECTION_NOT_VERIFIED"
    assert "reason_code" not in banked["attempts"][0]
    assert "provider-detail-do-not-leak" not in json.dumps(banked["attempts"]).lower()


def test_r06_connect_known_hosts_reject_policy_and_close_on_load_failure(monkeypatch):
    from services.census_autonomy import remote_dispatch

    fake_cfg = SimpleNamespace(
        host="127.0.0.1",
        port=22,
        username="ubuntu",
        auth_method="key",
        key_path="/tmp/test-only-id",
        hostname_expected="test-host",
        name="akki-vm-ii",
        slug="AKKI_VM_II",
    )
    monkeypatch.setattr(remote_dispatch.ssh_seam, "get_host_config", lambda host: fake_cfg)
    monkeypatch.setattr(remote_dispatch, "execution_identity", SimpleNamespace(verify_identity=lambda cfg: object()), raising=False)
    monkeypatch.setenv("SSH_KNOWN_HOSTS_PATH", "/tmp/test-known-hosts")

    calls = []

    class _RejectPolicy:
        pass

    class _FakeClient:
        def load_host_keys(self, path):
            calls.append(("load_host_keys", path))
            raise RuntimeError("boom")

        def set_missing_host_key_policy(self, policy):
            calls.append(("set_policy", type(policy).__name__))

        def connect(self, **kwargs):
            calls.append(("connect", kwargs))

        def close(self):
            calls.append(("close",))

    fake_paramiko = SimpleNamespace(SSHClient=_FakeClient, RejectPolicy=_RejectPolicy)
    monkeypatch.setitem(sys.modules, "paramiko", fake_paramiko)

    with pytest.raises(RuntimeError):
        remote_dispatch._connect("akki-vm-ii", timeout=5)
    assert ("load_host_keys", "/tmp/test-known-hosts") in calls
    assert ("close",) in calls
