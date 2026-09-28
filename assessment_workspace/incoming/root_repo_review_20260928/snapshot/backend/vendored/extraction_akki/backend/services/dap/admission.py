"""services/dap/admission.py — Sub-wave 2A · DAP-1..4.

External-party principal + party principal admission + slow-play
attack-shape scaffold.  Admission is a governed act (DAP-12) requiring
estate owner named authority.  DAP holds no admission logic of its own
outside composing this surface.

Sub-wave 2B extension: kwargs-form convenience wrappers + lookup helpers
for the api_keys / browse / trust_boundary primitives.
"""
from __future__ import annotations

import secrets
from typing import Iterable, List, Optional, Union

from contracts.dap import (
    CumulativeHistoryEntry,
    ExternalPartyPrincipal,
    GovernancePosture,
    PartyPrincipal,
    PartyPrincipalKind,
)


# In-memory party register (thin-kernel).  Persistence is a later
# wave's concern; the invariants asserted here (idempotency, agent
# autonomy scope required, party principals live under an org) hold
# at the language/receipt layer.
_ORG_REGISTER: dict[str, ExternalPartyPrincipal] = {}
_PARTY_REGISTER: dict[str, PartyPrincipal] = {}
_CUMULATIVE_HISTORY: List[CumulativeHistoryEntry] = []


class AdmissionRefused(Exception):
    """DAP-15 verbatim spirit: 'A refusal states why.'  Silence != refusal."""


def admit_external_party(
    org: Optional[ExternalPartyPrincipal] = None,
    *,
    admitting_authority_id: str = "",
    # Kwargs-form convenience (2B): build the object here.
    legal_identity: Optional[str] = None,
    governance_posture: Optional[Union[GovernancePosture, str]] = None,
    terms_id: Optional[str] = None,
    trust_domain_id: Optional[str] = None,
    admission_mandate: Optional[str] = None,
) -> ExternalPartyPrincipal:
    """DAP-12: admission is a governed act producing the organisation
    principal, its trust domain, its terms, and its mandate.  MUST
    require the estate owner's named authority — a party is never
    self-admitting.

    Two calling forms supported:
        * pass a fully-constructed ``ExternalPartyPrincipal`` (2A form);
        * pass kwargs and let this function build one (2B convenience).
    """
    if not admitting_authority_id.strip():
        raise AdmissionRefused(
            "DAP-12: admission requires the estate owner's named authority; "
            "self-admission is refused."
        )
    if org is None:
        if not all((legal_identity, governance_posture, terms_id,
                    trust_domain_id, admission_mandate)):
            raise AdmissionRefused(
                "DAP-1: kwargs-form admission requires legal_identity, "
                "governance_posture, terms_id, trust_domain_id, "
                "admission_mandate."
            )
        posture = (
            governance_posture
            if isinstance(governance_posture, GovernancePosture)
            else GovernancePosture(governance_posture)
        )
        org = ExternalPartyPrincipal(
            legal_identity=legal_identity,
            governance_posture=posture,
            terms_id=terms_id,
            trust_domain_id=trust_domain_id,
            admission_mandate=admission_mandate,
        )
    # Index by legal_identity — the model's natural key.
    _ORG_REGISTER[org.legal_identity] = org
    return org


def admit_party_principal(
    principal: Optional[PartyPrincipal] = None,
    *,
    organisation_principal_id: Optional[str] = None,
    principal_kind: Optional[Union[PartyPrincipalKind, str]] = None,
    display_name: Optional[str] = None,  # accepted for legibility; not stored
    mandate: Optional[str] = None,
    autonomy_scope: Optional[str] = None,
) -> PartyPrincipal:
    """DAP-2/DAP-3: every request carries a party principal.  Agents
    MUST carry a stated scope of autonomy.

    Two calling forms:
        * fully-constructed ``PartyPrincipal`` (2A form);
        * kwargs (2B convenience) — org id is looked up in the register.

    Note · ``display_name`` is accepted for test-legibility only; the
    frozen PartyPrincipal model has no display_name field (DAP-2 spec).
    """
    if principal is None:
        if not all((organisation_principal_id, principal_kind, mandate)):
            raise AdmissionRefused(
                "DAP-2: kwargs-form admission requires "
                "organisation_principal_id, principal_kind, mandate."
            )
        kind = (
            principal_kind
            if isinstance(principal_kind, PartyPrincipalKind)
            else PartyPrincipalKind(principal_kind)
        )
        principal = PartyPrincipal(
            principal_id=f"prn_{secrets.token_hex(4)}",
            parent_org_id=organisation_principal_id,
            kind=kind,
            mandate=mandate,
            autonomy_scope=autonomy_scope,
        )
    if principal.parent_org_id not in _ORG_REGISTER:
        raise AdmissionRefused(
            f"DAP-1/DAP-2: party principal's organisation "
            f"{principal.parent_org_id!r} is not admitted."
        )
    if principal.kind is PartyPrincipalKind.AGENT and not (
        principal.autonomy_scope and principal.autonomy_scope.strip()
    ):
        raise AdmissionRefused(
            "DAP-3: an external agent MUST carry a stated scope of "
            "autonomy at admission."
        )
    _PARTY_REGISTER[principal.principal_id] = principal
    return principal


def record_cumulative_history(entry: CumulativeHistoryEntry) -> None:
    """DAP-24: first-class queryable record supporting DAP-4."""
    _CUMULATIVE_HISTORY.append(entry)


def detect_slow_play(party_id: str, *, aggregate_threshold: int) -> bool:
    """DAP-4: detect against the party's cumulative extraction history,
    not per-request.  Every individual request in a slow-play sequence
    is legitimate; only the aggregate is not.

    Thin-kernel: sums quantities across all history entries for the
    party.  Returns True if aggregate exceeds threshold — a real
    aggregate-reconstruction check binds in a subsequent wave when
    scope-signature reconstruction is defined.
    """
    party_entries = [e for e in _CUMULATIVE_HISTORY if e.party_id == party_id]
    total = sum(e.quantity for e in party_entries)
    return total > aggregate_threshold


def cumulative_history_for(party_id: str) -> tuple[CumulativeHistoryEntry, ...]:
    """DAP-24: readable by the estate owner at any time."""
    return tuple(e for e in _CUMULATIVE_HISTORY if e.party_id == party_id)


def get_party_principal(principal_id: str) -> Optional[PartyPrincipal]:
    """Lookup a per-principal party (individual or agent).  Returns None
    for organisation-level ids so callers (e.g. api_keys.issue_key) can
    enforce DAP-13's per-principal-never-per-organisation rule.
    """
    return _PARTY_REGISTER.get(principal_id)


# Reset helper for isolated tests
def _reset_for_test() -> None:
    _ORG_REGISTER.clear()
    _PARTY_REGISTER.clear()
    _CUMULATIVE_HISTORY.clear()


# 2B public alias — same semantics as _reset_for_test.
reset_state = _reset_for_test
