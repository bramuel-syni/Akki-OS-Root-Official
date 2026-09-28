"""Artifact-return hash verification for the compute seam.

Every artifact returning from the VM carries a sha256 hash claimed by the
runner. The seam verifies the claim against the actual content before
writing an `Ingestion.Artifact` or `Training.Artifact` record.

A mismatch is a Canon 8 §32 W-negative event.
"""
from __future__ import annotations

import hashlib


class ArtifactHashMismatch(Exception):
    """Raised when a returned artifact's content sha256 != the claimed hash."""


def verify_artifact_hash(content: bytes, claimed_sha256_hex: str) -> bool:
    """Return True iff sha256(content).hexdigest() == claimed. Else raise.

    Content may be empty (b""). Claimed hash must be a 64-char lower-hex
    string (sha256 output length). We do not attempt to be forgiving of
    case-variation or whitespace — governance surfaces will fail loudly.
    """
    actual = hashlib.sha256(content).hexdigest()
    if actual != claimed_sha256_hex.strip().lower():
        raise ArtifactHashMismatch(
            f"artifact_hash_mismatch: claimed={claimed_sha256_hex[:12]}… "
            f"actual={actual[:12]}… (len_content={len(content)})"
        )
    return True
