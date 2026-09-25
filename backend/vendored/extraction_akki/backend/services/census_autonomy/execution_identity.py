"""Census-only admitted-key continuity check; no network or credential mutation.

The existing host inventory remains authoritative. Per-host env pins an existing
identity receipt, not a newly generated identity. Private material is consumed
only by the SSH key loader and never returned as text or written to a receipt.
"""
import base64
import hashlib
import hmac
import json
import os
import stat
from pathlib import Path


class IdentityVerificationError(ValueError):
    """Safe local refusal; provider messages and custody paths never escape."""

    def __init__(self, reason_code):
        self.reason_code = reason_code
        super().__init__(reason_code)


def _fingerprint(public_bytes):
    return "SHA256:" + base64.b64encode(hashlib.sha256(public_bytes).digest()).decode().rstrip("=")


def _expected_fingerprint(config):
    path = os.environ.get(f"{config.slug}_SSH_IDENTITY_RECEIPT_PATH")
    if not path:
        raise IdentityVerificationError("IDENTITY_RECEIPT_MISSING")
    try:
        raw = Path(path).read_bytes()
    except OSError:
        raise IdentityVerificationError("IDENTITY_RECEIPT_MISSING") from None
    pin = os.environ.get(f"{config.slug}_SSH_IDENTITY_RECEIPT_SHA256")
    if not pin or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), pin):
        raise IdentityVerificationError("IDENTITY_RECEIPT_HASH_MISMATCH")
    try:
        import paramiko
        receipt = json.loads(raw)
        parts = receipt["public_key_line"].split()
        public = base64.b64decode(parts[1], validate=True)
        # Parse the wire format, not just a plausible base64 string.
        parsed = paramiko.PKey.from_type_string(parts[0], public)
        expected = _fingerprint(parsed.asbytes())
        claimed = receipt["public_key_fingerprint"].split()
        if claimed.count(expected) != 1 or public != parsed.asbytes():
            raise ValueError("receipt fingerprint disagrees")
        return expected
    except Exception:
        raise IdentityVerificationError("IDENTITY_RECEIPT_MALFORMED") from None


def _load_key(path):
    import paramiko
    if not path:
        raise IdentityVerificationError("IDENTITY_KEY_MISSING")
    # O_NOFOLLOW + fstat binds checks and parsing to one opened file, avoiding
    # path substitution between validation and authentication.
    if Path(path).is_symlink():
        raise IdentityVerificationError("IDENTITY_KEY_SYMLINK")
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        raise IdentityVerificationError("IDENTITY_KEY_UNREADABLE") from None
    with os.fdopen(descriptor, "r") as handle:
        info = os.fstat(handle.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o077 or not info.st_mode & stat.S_IRUSR):
            raise IdentityVerificationError("IDENTITY_KEY_PERMISSIONS")
        if info.st_size > 65536:
            raise IdentityVerificationError("IDENTITY_KEY_INVALID")
        # Read the private key itself; never trust a .pub sidecar or implicitly
        # load an adjacent SSH certificate as an alternative identity.
        for loader in (paramiko.Ed25519Key, paramiko.RSAKey, paramiko.ECDSAKey):
            handle.seek(0)
            try:
                return loader.from_private_key(handle)
            except paramiko.PasswordRequiredException:
                raise IdentityVerificationError("IDENTITY_KEY_LOCKED") from None
            except (paramiko.SSHException, ValueError, UnicodeError):
                continue
    raise IdentityVerificationError("IDENTITY_KEY_INVALID")


def verify_identity(config):
    """Return the exact admitted PKey to authenticate, or refuse before network."""
    if not config.key_path:
        raise IdentityVerificationError("IDENTITY_PASSWORD_FALLBACK_FORBIDDEN")
    expected = _expected_fingerprint(config)
    key = _load_key(config.key_path)
    if not hmac.compare_digest(_fingerprint(key.asbytes()), expected):
        raise IdentityVerificationError("IDENTITY_PIN_MISMATCH")
    return key