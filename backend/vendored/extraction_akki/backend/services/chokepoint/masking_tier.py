"""services.chokepoint.masking_tier — governed positive allowlist.

Adapted from RMS-IQ-Core-2/backend/services/synisense/shield/masking_tier.py
(2026-07-30 · P1-R5 Owner ruling). The allowlist is a governed value —
adding a new tier requires an Owner ruling recorded in DECISIONS.md.

W3 admissible tiers on this estate (from the allowlist config):
  - structure_only   · Data API reads of information_schema (no row content).
  - attested_command · SSH seam calls limited to hardening.json's attested set.
  - receipt_only     · governance/audit reads that touch no external system.

Row-bearing tiers (t1_full_mask / t2_partial / t3_category) are DECLARED
in the allowlist but marked admissible_under_env=[] — not admissible in
any env until row-bearing queries land AND a governed masking policy
has been authored (Doc 02 §A5.2 · CA1-007 authoring surface).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List


class MaskingTierRefused(ValueError):
    """Raised when a crossing attempts to emit a non-allowlisted or non-
    admissible masking tier."""


_ALLOWLIST_PATH = Path(__file__).resolve().parent / "masking_tier_allowlist.v0.json"


def _load_allowlist() -> Dict[str, Any]:
    # M12-W1c · SEC-1 runtime wire: unverifiable policy = closed gate.
    from services.chokepoint.policy_integrity import load_policy_with_integrity
    return load_policy_with_integrity(_ALLOWLIST_PATH)


def _entries_by_tier() -> Dict[str, Dict[str, Any]]:
    return {e["tier"]: e for e in _load_allowlist().get("entries", [])}


def legal_tiers() -> List[str]:
    """Return the list of declared masking-tier values (regardless of env)."""
    return sorted(_entries_by_tier().keys())


def validate_tier(tier: str, *, akki_env: str = None) -> None:
    """Validate a masking-tier for emission.

    Raises MaskingTierRefused on:
      - empty / missing tier
      - tier not on the positive allowlist
      - tier not admissible under the current AKKI_ENV
    """
    if not tier:
        raise MaskingTierRefused(
            "masking_tier_required — empty tier refused. "
            "Every crossing must declare its masking tier."
        )
    entries = _entries_by_tier()
    entry = entries.get(tier)
    if entry is None:
        raise MaskingTierRefused(
            f"masking_tier_unknown — {tier!r} not on the positive allowlist. "
            f"Legal declared tiers: {sorted(entries.keys())}. "
            "Adding a new tier requires an Owner ruling."
        )
    if akki_env is None:
        akki_env = os.environ.get("AKKI_ENV", "development").lower()
    admissible = entry.get("admissible_under_env", [])
    if akki_env not in admissible:
        raise MaskingTierRefused(
            f"masking_tier_not_admissible_here — {tier!r} not admissible "
            f"under AKKI_ENV={akki_env!r}. Admissible under: {admissible!r}."
        )
