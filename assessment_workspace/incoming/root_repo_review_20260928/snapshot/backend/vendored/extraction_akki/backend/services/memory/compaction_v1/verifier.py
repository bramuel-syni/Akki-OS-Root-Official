"""services.memory.compaction_v1.verifier · MEM-7 deterministic reload verifier.

Canon anchors verbatim:
  * MEM-7 (SFP-8 principle · FP-2) · reload is deterministic · same
    artefact under same key yields same context.  NO re-summarisation
    on read (MEM-R-051 hard ban).
  * MEM-R-016 · reload hash-verify or fail closed.  A reload whose
    artefact hash does not verify against the register fails closed;
    caller is refused, NOT served a best effort.

TCB inclusion: IN (MEM-7 · Spec §4 Table 3).  This module MUST NOT
import any learned/model-client surface (Canon 4 §22 rung-1
determinism · MEM-R-051 grep-negative surface).
"""
from __future__ import annotations

import hashlib


class ReloadVerifier:
    """MEM-7 · deterministic hash-verify reload gate.

    Verifies that a bytes payload sha256-matches an expected hex digest.
    Pure function surface (no I/O).  The storage layer calls this at
    read time (services.memory.compaction_v1.storage.read_artefact_bytes)
    and services.memory.compaction_v1.reload delegates to it.
    """

    __slots__ = ()

    def verify(self, *, bytes_payload: bytes, expected_hash: str) -> bool:
        """Deterministic sha256 hash-verify.

        Returns True if sha256_hex(bytes_payload) == expected_hash.
        False otherwise.  Does NOT raise; the caller decides the
        refusal shape (fail-closed at operations.reload boundary).
        """
        actual = hashlib.sha256(bytes_payload).hexdigest()
        return actual == expected_hash


__all__: tuple[str, ...] = ("ReloadVerifier",)
