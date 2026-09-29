"""Estate-custody signing for E1-held principals (planner, approvers, allocator).

Private keys live only in the 0600 custody directory named by the environment;
worker keys are generated on their own admitted runtime and never appear here.
"""
import json
import os
import time
from pathlib import Path
from services.activation.receipts import SignedReceipt
from services.watch.signature_primitive import watch_keygen, watch_sign


def custody_dir():
    return Path(os.environ['AKKI_ESTATE_CUSTODY_DIR'])


def _key_path(tenant, key_id):
    path = custody_dir() / tenant / 'signers' / f'{key_id}.ed25519'
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def ensure_key(tenant, key_id):
    """Generate once; return the raw public key hex. Private bytes never leave the file."""
    path = _key_path(tenant, key_id)
    if not path.exists():
        private, public = watch_keygen()
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(private.hex().encode() + b'\n' + public.hex().encode() + b'\n')
    private_hex, public_hex = path.read_text().split()
    return public_hex


def has_key(tenant, key_id):
    return _key_path(tenant, key_id).exists()


def runtime_receipt(raw):
    """A receipt that crossed the seam as JSON (lists, not tuples) parsed under the strict model."""
    return SignedReceipt.model_validate_json(json.dumps(raw))


def sign_receipt(tenant, signer_id, key_id, kind, claims, *, scope_refs, request_sha256=None,
                 ttl_seconds=3600, now=None):
    now = int(time.time()) if now is None else int(now)
    private_hex = _key_path(tenant, key_id).read_text().split()[0]
    unsigned = SignedReceipt(version='akki.activation.receipt/1', tenant_id=tenant, signer_id=signer_id,
        key_id=key_id, kind=kind, request_sha256=request_sha256, scope_refs=tuple(scope_refs),
        issued_epoch=now, expires_epoch=now + int(ttl_seconds), claims=claims, signature_hex='0' * 128)
    signature = watch_sign(bytes.fromhex(private_hex), unsigned.signing_bytes())
    return unsigned.model_copy(update={'signature_hex': signature.hex()})
