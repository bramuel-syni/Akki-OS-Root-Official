"""On-runtime Ed25519 identity. Generated where the worker runs; the private key never leaves.

Pure stdlib + cryptography: this module executes inside the admitted runtime's venv.
The receipt envelope reproduces `SignedReceipt.signing_bytes` byte for byte.
"""
import hashlib
import json
import os
import socket
import time
from pathlib import Path

ENVELOPE = b'akki.activation.receipt/1\n'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def identity_dir(state_dir):
    path = Path(os.path.expanduser(state_dir)) / 'identity'
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def ensure(state_dir):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    path = identity_dir(state_dir) / 'worker.ed25519'
    if not path.exists():
        private = Ed25519PrivateKey.generate()
        raw = private.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                                    serialization.NoEncryption())
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
    private = Ed25519PrivateKey.from_private_bytes(path.read_bytes())
    public = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return {'key_id': 'rk-' + hashlib.sha256(public).hexdigest()[:20], 'public_key_hex': public.hex(),
            'hostname': socket.gethostname()}


def sign(state_dir, message):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    private = Ed25519PrivateKey.from_private_bytes((identity_dir(state_dir) / 'worker.ed25519').read_bytes())
    return private.sign(message)


def receipt(state_dir, *, tenant_id, signer_id, key_id, kind, claims, scope_refs, request_sha256=None,
            ttl_seconds=3600, now=None):
    now = int(time.time()) - 2 if now is None else int(now)  # tolerate small clock lead versus E1's verifier
    body = {'version': 'akki.activation.receipt/1', 'tenant_id': tenant_id, 'signer_id': signer_id,
            'key_id': key_id, 'kind': kind, 'request_sha256': request_sha256, 'scope_refs': list(scope_refs),
            'issued_epoch': now, 'expires_epoch': now + int(ttl_seconds), 'claims': claims}
    message = ENVELOPE + json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return {**body, 'signature_hex': sign(state_dir, message).hex()}


def observation(category, context_sha256, claim, *, reservation_ref=None, quantities=(), terminal=False,
                typed=None):
    """Minimal Observation claims; optional fields are omitted so strict parsing accepts them."""
    value = {'category': category, 'context_sha256': context_sha256, 'claim_sha256': digest(claim),
             'evidence_mode': 'measured', 'terminal': bool(terminal)}
    if reservation_ref is not None:
        value['reservation_ref'] = reservation_ref
    if quantities:
        value['quantities'] = [dict(q) for q in quantities]
    if typed:
        value.update(typed)
    return value
