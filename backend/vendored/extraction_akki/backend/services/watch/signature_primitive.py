"""services.watch.signature_primitive — M12b-W1 · MUST-DO 3.

Minimum Ed25519 primitive for Watch verdict signing.

Scope (owner reminder 2026-09-19T~03:37Z verbatim):
  "Ed25519 minimum scope only (Watch key: keygen/sign/verify); full
   hierarchy stays M13-W2."

Canon anchors:
  * Canon 8 §W10 (watcher-watched-from-outside · keys held only by the
    Watch's own trust boundary).
  * Canon 8 §W11 (one-task-one-identity).
  * Canon 8 §Line 31 ("The certainty computation is a function with
    no parameter through which a detector's confidence can enter —
    Solva's own assertion boundary, transplanted: the signature is
    the guard.").

Design:
  * `watch_keygen()` returns `(private_key_bytes, public_key_bytes)`
    as 32-byte raw Ed25519 encodings (RFC 8032 §5.1.5 / §5.1.6).
  * `watch_sign(priv, msg)` returns a 64-byte deterministic signature
    (RFC 8032 §5.1.6 makes signing deterministic per (priv, msg)).
  * `watch_verify(pub, msg, sig)` returns True iff the signature
    verifies; False on any tampering — never raises.

No key hierarchy. No rotation. No cross-trust-boundary key export or
import. All those land at M13-W2 per pre-ruling.
"""
from __future__ import annotations

from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)


def watch_keygen() -> Tuple[bytes, bytes]:
    """Generate a fresh Ed25519 key pair for the Watch trust boundary.

    Returns:
        (private_key_bytes, public_key_bytes) — each 32 bytes, raw
        Ed25519 encoding per RFC 8032.

    Keygen is nondeterministic (fresh entropy per call · cryptography
    library's OS random source). Callers should hold the private
    key only within the Watch's own trust boundary (Canon 8 §W10).
    """
    priv = Ed25519PrivateKey.generate()
    priv_bytes = priv.private_bytes(
        encoding=Encoding.Raw,
        format=PrivateFormat.Raw,
        encryption_algorithm=NoEncryption(),
    )
    pub_bytes = priv.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    return priv_bytes, pub_bytes


def watch_sign(private_key_bytes: bytes, message: bytes) -> bytes:
    """Sign `message` under Ed25519 with the raw 32-byte private key.

    Deterministic per RFC 8032 §5.1.6: given the same (priv, msg),
    signature bytes are identical across calls and machines.

    Returns:
        64-byte raw Ed25519 signature.
    """
    priv = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    return priv.sign(message)


def watch_verify(
    public_key_bytes: bytes, message: bytes, signature: bytes
) -> bool:
    """Verify `signature` over `message` under the raw 32-byte public
    key. Returns True on match, False on any mismatch / tampering /
    malformed input. NEVER raises — the verify predicate is the guard
    (Canon 8 §Line 31)."""
    try:
        pub = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        pub.verify(signature, message)
    except (InvalidSignature, ValueError, TypeError):
        return False
    return True


__all__ = ("watch_keygen", "watch_sign", "watch_verify")
