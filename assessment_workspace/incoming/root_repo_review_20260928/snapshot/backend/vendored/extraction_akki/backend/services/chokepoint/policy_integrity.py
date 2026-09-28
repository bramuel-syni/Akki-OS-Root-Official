"""services.chokepoint.policy_integrity — SEC-1 crossing-policy integrity.

Owner Run Order 2026-09-18T~15:30Z · Milestone 1 · M12:
    "Crossing policy integrity-verified at load (SEC-1); an
     unverifiable policy is a closed gate (FP-1, FP-2)."

Canon anchor · SEC-1 (structural-safety-by-construction):
    A crossing policy that cannot be verified is refused — the load
    itself is the gate.  This module gives the chokepoint a pure
    integrity check that other loader functions call before parse.

The three crossing-policy files owned by the chokepoint:

    services/chokepoint/llm_endpoint_allowlist.v0.json
    services/chokepoint/masking_tier_allowlist.v0.json
    services/chokepoint/residency_allowlist.v0.json

Each carries a companion `.sha256` file with a single line: the
lowercase hex sha256 of the JSON file's byte content.  Any drift to
the JSON without updating the companion `.sha256` file fires the
gate at the next load.

Contract:

    verify_policy_integrity(policy_path: Path) -> None
        Raises PolicyIntegrityRefused if:
        - the policy file does not exist (unverifiable → closed gate).
        - the companion `.sha256` file does not exist (unverifiable → closed).
        - the recorded hash does not match the byte-content sha256 (drift).

    load_policy_with_integrity(policy_path: Path) -> dict
        Verifies then parses.  Never returns a partial policy.

    PolicyIntegrityRefused(RuntimeError)
        Closed-gate refusal per FP-1 (fail-closed) + FP-2 (source retained on abort).
        Do NOT map to a Watch signal — this is a build-time gate at load.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict


class PolicyIntegrityRefused(RuntimeError):
    """Closed-gate refusal on unverifiable / drifted crossing policy.

    Follows FP-1 (fail-closed) and FP-2 (source retained on abort).
    Any load that surfaces this exception MUST NOT proceed — the
    caller MUST propagate rather than swallow.
    """


def _companion_sha256_path(policy_path: Path) -> Path:
    """Return the sibling `<policy>.sha256` path."""
    return policy_path.parent / (policy_path.name + ".sha256")


def _read_recorded_hash(sha256_path: Path) -> str:
    """Read the single-line lowercase hex hash from the companion file."""
    line = sha256_path.read_text(encoding="utf-8").strip()
    # Some sha256sum-style files carry `<hash>  <filename>` — take the first token.
    return line.split()[0].lower() if line else ""


def _compute_content_hash(policy_path: Path) -> str:
    """Return lowercase hex sha256 of the policy file's byte content."""
    h = hashlib.sha256()
    h.update(policy_path.read_bytes())
    return h.hexdigest()


def verify_policy_integrity(policy_path: Path) -> None:
    """Assert the policy file exists AND its companion hash matches.

    Raises PolicyIntegrityRefused with a closed-gate diagnostic on any
    of the three fault classes (file-missing, companion-missing, drift).
    """
    if not policy_path.exists():
        raise PolicyIntegrityRefused(
            f"policy_missing — {policy_path} does not exist. "
            "Unverifiable policy is a closed gate (SEC-1 · FP-1 · FP-2)."
        )
    sha256_path = _companion_sha256_path(policy_path)
    if not sha256_path.exists():
        raise PolicyIntegrityRefused(
            f"companion_sha256_missing — {sha256_path.name} is required "
            f"for {policy_path.name} but does not exist on disk. "
            "Unverifiable policy is a closed gate (SEC-1 · FP-1 · FP-2). "
            "Author the companion .sha256 file in the same commit as the "
            "policy change."
        )
    recorded = _read_recorded_hash(sha256_path)
    if not recorded or len(recorded) != 64:
        raise PolicyIntegrityRefused(
            f"companion_sha256_malformed — {sha256_path.name} does not "
            f"carry a valid 64-hex sha256 (got {recorded!r})."
        )
    actual = _compute_content_hash(policy_path)
    if actual != recorded:
        raise PolicyIntegrityRefused(
            f"policy_integrity_mismatch — {policy_path.name} content-hash "
            f"({actual}) does not match recorded hash ({recorded}) in "
            f"{sha256_path.name}. Either the policy was edited without "
            "updating its companion .sha256, or the .sha256 has drifted "
            "from the policy. Closed gate per SEC-1 · FP-1 · FP-2."
        )


def load_policy_with_integrity(policy_path: Path) -> Dict[str, Any]:
    """Verify integrity, then parse the policy JSON.

    Never returns a partial policy — any fault raises PolicyIntegrityRefused
    before parse.
    """
    verify_policy_integrity(policy_path)
    return json.loads(policy_path.read_text(encoding="utf-8"))


__all__ = [
    "PolicyIntegrityRefused",
    "verify_policy_integrity",
    "load_policy_with_integrity",
]
