"""W-DAP-STACK 2E · DAP-22 three-level terms resolution.

Verbatim DAP-22: 'Terms attach at three levels, resolved most-specific-
first: per party agreement, then per custody class, then estate default.
Every receipt cites the terms identifier actually applied, not the level
it came from.'

DAP-26 (non-retroactive) is honored by making resolve_terms a pure
lookup at call time; MeteredEvent instances stamped with an earlier
terms_id are frozen and never mutated by subsequent configuration calls.
"""

from __future__ import annotations

from typing import Dict, Tuple

from pydantic import BaseModel, ConfigDict


class TermsResolution(BaseModel):
    """DAP-22 receipt: cites the resolved terms_id (NOT the level)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    resolved_terms_id: str
    resolution_level: str  # 'party' | 'custody_class' | 'estate_default'


# in-memory config surfaces (later Rules-Service replaces these)
_party: Dict[Tuple[str, str], str] = {}          # (estate_id, party_id)
_custody: Dict[Tuple[str, str], str] = {}        # (estate_id, custody_class)
_estate: Dict[str, str] = {}                     # estate_id


def configure_party_terms(*, estate_id: str, party_id: str, terms_id: str) -> None:
    _party[(estate_id, party_id)] = terms_id


def configure_custody_class_terms(
    *, estate_id: str, custody_class: str, terms_id: str,
) -> None:
    _custody[(estate_id, custody_class)] = terms_id


def configure_estate_default_terms(*, estate_id: str, terms_id: str) -> None:
    _estate[estate_id] = terms_id


def resolve_terms(
    *, estate_id: str, custody_class: str, party_id: str,
) -> TermsResolution:
    """DAP-22: most-specific-first."""
    key_p = (estate_id, party_id)
    if key_p in _party:
        return TermsResolution(
            resolved_terms_id=_party[key_p], resolution_level="party",
        )
    key_c = (estate_id, custody_class)
    if key_c in _custody:
        return TermsResolution(
            resolved_terms_id=_custody[key_c], resolution_level="custody_class",
        )
    if estate_id in _estate:
        return TermsResolution(
            resolved_terms_id=_estate[estate_id], resolution_level="estate_default",
        )
    raise LookupError(
        f"DAP-22: no terms configured at any level for estate={estate_id!r} "
        f"custody_class={custody_class!r} party={party_id!r}"
    )


def reset_state() -> None:
    """Test-only helper."""
    _party.clear()
    _custody.clear()
    _estate.clear()
