"""services.platform_control_plane.estate_entity — CP-P3-CP1 · M9.

Pure frozen carrier for the control-plane `estate` record per Akki OS
Pilot Platform Reference v0.2 §10 verbatim:

    estate (id, tenant_id, name, tier, location_summary,
            estate_contact, agent_id, sandbox_safe)

§5.1 verbatim tier vocabulary: `connected` (customer-owned estate ·
runtime remains on customer premises) or `hosted` (Syni-hosted
resource under governance). Preventive-charter refusal on unknown
tier.

§4.4 M-H-8 verbatim: "Sandbox attaches only to sandbox_safe=true
connectors + sandbox allocation." — the `sandbox_safe` field is a
bool on the estate carrier · downstream sandbox-attach CPs compose
the runtime rule.

Standing-line proof:
- All 7 str + 1 bool fields · 8 exact-order.
- No enforcement hard-gate · caller composes sandbox policy.
- Zero closed enums (tier surfaced as OPEN str · validated by ref set).
- Zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


ESTATE_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: estate (id, tenant_id, name, tier, location_summary, "
    "estate_contact, agent_id, sandbox_safe). §5.1 tier vocabulary: "
    "connected (customer-owned · runtime on customer premises) OR "
    "hosted (Syni-hosted resource under governance). §4.4 M-H-8: "
    "Sandbox attaches only to sandbox_safe=true connectors + sandbox "
    "allocation."
)


# §5.1 tier vocabulary · OPEN str per case-agnostic doctrine.
ESTATE_TIER_VALUES: Tuple[str, ...] = (
    "connected",
    "hosted",
)


@dataclasses.dataclass(frozen=True)
class EstateEntity:
    """Frozen carrier for a control-plane estate per §10.

    Exact-order 8 fields (7 str + 1 bool):
    - id · OPEN opaque estate record id.
    - tenant_id · OPEN opaque · owning tenant per §3.1 M-T-2.
    - name · OPEN str · human-readable estate name.
    - tier · OPEN str · one of ESTATE_TIER_VALUES.
    - location_summary · OPEN str · human-readable location hint.
    - estate_contact · OPEN str · contact ref.
    - agent_id · OPEN opaque · data-plane agent binding.
    - sandbox_safe · bool · whether this estate admits sandbox
      attachment per §4.4 M-H-8.
    """
    id: str
    tenant_id: str
    name: str
    tier: str
    location_summary: str
    estate_contact: str
    agent_id: str
    sandbox_safe: bool


ESTATE_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "name",
    "tier",
    "location_summary",
    "estate_contact",
    "agent_id",
    "sandbox_safe",
)


class EstateEntityRefused(Exception):
    """Root refusal for estate-entity invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never id / name / tier values in
    the exception body)."""


class UnknownEstateTierRefused(EstateEntityRefused):
    """Refused: estate.tier is not in ESTATE_TIER_VALUES (§5.1
    verbatim vocabulary: connected · hosted)."""


def assert_estate_tier_valid(*, estate: EstateEntity) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses when `estate.tier` is not in `ESTATE_TIER_VALUES`.
    Returns None on admit.

    Message reports COUNTS/positional index only (never tier value)."""
    if estate.tier not in frozenset(ESTATE_TIER_VALUES):
        raise UnknownEstateTierRefused(
            f"unknown-estate-tier refused: tier at positional index "
            f"{ESTATE_ENTITY_FIELDS.index('tier')} not among "
            f"{len(ESTATE_TIER_VALUES)} §5.1 tier values."
        )
    return None


__all__ = [
    "ESTATE_ENTITY_ANCHOR",
    "ESTATE_TIER_VALUES",
    "ESTATE_ENTITY_FIELDS",
    "EstateEntity",
    "EstateEntityRefused",
    "UnknownEstateTierRefused",
    "assert_estate_tier_valid",
]
