"""services/estate_keys/keypair.py - ed25519 keypair custody for the estate.

Owner course-correction 2026-08-14: the wizard's compute path shows a
provisioning card BEFORE credentials are keyed. The card renders the
estate's public key + its SHA256 fingerprint. This module owns the
keypair on the pod's disk: generate-once, read-many, private-never-leaves.

Storage:
  Directory: env var ESTATE_KEYS_DIR (required; default None -> ValueError)
  Private:   {DIR}/estate_ed25519       (mode 0600, never returned by any function here)
  Public:    {DIR}/estate_ed25519.pub   (mode 0644, openssh format)

Idempotency: first call generates + writes; subsequent calls read the
existing files and return the same public-openssh + fingerprint.
"""
from __future__ import annotations

import base64
import hashlib
import os
import stat
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def _keys_dir() -> Path:
    raw = os.environ.get("ESTATE_KEYS_DIR")
    if not raw:
        raise ValueError("ESTATE_KEYS_DIR env var not set")
    d = Path(raw)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _fingerprint(public_openssh: str) -> str:
    """openssh convention: SHA256:base64(sha256(raw-wire-bytes)) with '=' stripped."""
    parts = public_openssh.strip().split()
    if len(parts) < 2:
        raise ValueError("public key not in openssh format")
    raw = base64.b64decode(parts[1])
    digest = hashlib.sha256(raw).digest()
    return "SHA256:" + base64.b64encode(digest).decode().rstrip("=")


def ensure_keypair() -> dict:
    """Return {public_openssh, fingerprint} - idempotent; never returns private material."""
    d = _keys_dir()
    priv_path = d / "estate_ed25519"
    pub_path = d / "estate_ed25519.pub"

    if not priv_path.exists() or not pub_path.exists():
        # Generate fresh
        pk = Ed25519PrivateKey.generate()
        priv_bytes = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = pk.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        # Append a comment so operators know where the key came from
        pub_str = pub_bytes.decode() + " estate@akki\n"
        priv_path.write_bytes(priv_bytes)
        pub_path.write_text(pub_str)
        priv_path.chmod(0o600)
        pub_path.chmod(0o644)
    else:
        # Read existing; enforce modes on every read so a permission drift is corrected fast
        priv_mode = stat.S_IMODE(priv_path.stat().st_mode)
        pub_mode = stat.S_IMODE(pub_path.stat().st_mode)
        if priv_mode != 0o600:
            priv_path.chmod(0o600)
        if pub_mode != 0o644:
            pub_path.chmod(0o644)

    public_openssh = pub_path.read_text().strip()
    # Strip trailing comment for fingerprint calculation; fingerprint uses key bytes only
    return {
        "public_openssh": public_openssh,
        "fingerprint": _fingerprint(public_openssh),
    }
