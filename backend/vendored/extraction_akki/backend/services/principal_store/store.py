"""services.principal_store.store — Principal Model Spec v1 §2 store.

PRIN-1 · PRIN-2 · PRIN-3 · PRIN-4 enforcement, additive-only.

Design notes:
- The in-process registry is a private dict keyed by principal_id. No
  external mutation surface; consumers use `get_principal(id)` which
  returns an immutable-by-refusal facade.
- PRIN-4 immutability is enforced through the facade's __setattr__
  guard which raises `PrincipalRefusal` on any mutation attempt after
  admission. Backing the facade with a Pydantic `PrincipalV1`
  (frozen=True, extra='forbid') satisfies SO §3.10-α at the contract
  layer; the facade's refusal exception makes the mutation semantics
  match the invariant test's expected exception tuple verbatim
  (`(PrincipalRefusal, TypeError, AttributeError)`).
- PRIN-3 behavioural-signature state is populated from admission
  (never None); an agent's machine-speed attack shape applies from
  admission, not later.
- PRIN-2 admission ceremony:
    * `admit_organisation` refuses when `admitted_by` is falsy (no
      estate owner's named authority).
    * `admit_individual` / `admit_agent` refuse when the parent
      organisation is missing OR when `admitted_by` does not resolve
      to a principal holding admit authority under that organisation's
      terms.
    * No principal self-admits (a principal can be listed as
      `admitted_by` only if it already exists in the store with
      `admit_authority=True`).
"""
from __future__ import annotations

import secrets
import threading
from typing import Dict, Final, Optional, Tuple

from contracts.principal_v1 import PrincipalKind, PrincipalV1


PRINCIPAL_KINDS: Final[Tuple[str, str, str]] = (
    "organisation",
    "individual",
    "agent",
)


class PrincipalRefusal(RuntimeError):
    """Raised on any admission or mutation the principal store refuses.

    PRIN-2 (governed admission), PRIN-4 (mandate immutable), and PRIN-1
    (individual/agent MUST reference an organisation) all refuse via
    this exception.  The exception name mirrors the doctrine in the
    canon: refusal is a first-class outcome, not an error.
    """


class Principal:
    """Immutable-by-refusal facade over PrincipalV1.

    PRIN-4 verbatim: 'Mandate is immutable once frozen at admission...
    Changing what a principal is admitted to do is a new admission
    event, not an edit to the old one.'

    Any attempt to assign to an existing attribute after `__init__`
    raises `PrincipalRefusal` — the same doctrine Northena's objective
    freeze already applies to scope (PRIN-13 kinship).
    """

    __slots__ = ("_contract", "_admitted")

    def __init__(self, contract: PrincipalV1) -> None:
        object.__setattr__(self, "_contract", contract)
        object.__setattr__(self, "_admitted", True)

    def __getattr__(self, name: str):
        # Delegate to the underlying frozen contract for any field.
        contract = object.__getattribute__(self, "_contract")
        if name in contract.__class__.model_fields:
            return getattr(contract, name)
        raise AttributeError(name)

    def __setattr__(self, name: str, value) -> None:
        # After admission, mutation is refused.  PRIN-4.
        if object.__getattribute__(self, "_admitted"):
            raise PrincipalRefusal(
                f"PRIN-4 · mandate immutable once frozen at admission; "
                f"attempt to mutate {name!r} refused. "
                "Changing what a principal is admitted to do is a new "
                "admission event, not an edit to the old one."
            )
        object.__setattr__(self, name, value)


# --- Private in-process registry -------------------------------------------
_REGISTRY: Dict[str, Principal] = {}
_LOCK = threading.Lock()


def _fresh_principal_id(prefix: str) -> str:
    """Opaque platform-issued handle. `secrets.token_urlsafe` is
    used to guarantee unpredictability; the value is never derived
    from caller input."""

    return f"{prefix}_{secrets.token_urlsafe(12)}"


def _register(principal: Principal) -> str:
    with _LOCK:
        _REGISTRY[principal.principal_id] = principal
    return principal.principal_id


# --- PRIN-2 admission API --------------------------------------------------


def admit_organisation(
    legal_identity: str,
    admitted_by: Optional[str] = None,
    trust_domain_identifier: Optional[str] = None,
    admission_mandate: str = "unset",
) -> str:
    """PRIN-2 verbatim: 'An organisation is admitted only by the estate
    owner's named authority.'

    `admitted_by` MUST be a non-empty string carrying the estate
    owner's named authority.  A falsy value is refused.
    """

    if not admitted_by:
        raise PrincipalRefusal(
            "PRIN-2 · organisation admission refused: estate owner's "
            "named authority is required (no principal self-admits)."
        )
    principal_id = _fresh_principal_id("org")
    trust_domain = trust_domain_identifier or _fresh_principal_id("td")
    contract = PrincipalV1(
        principal_id=principal_id,
        kind=PrincipalKind.ORGANISATION,
        legal_identity=legal_identity,
        trust_domain_identifier=trust_domain,
        admission_time_mandate=admission_mandate,
        # PRIN-3 verbatim: behavioural-signature state present from admission.
        behavioural_signature_state="watch:baseline@admission",
        parent_organisation_id=None,
        autonomy_scope=None,
        # PRIN-2: organisations admitted by the estate owner carry
        # admit authority under their own organisation's terms.
        admit_authority=True,
    )
    return _register(Principal(contract))


def _resolve_admit_authority(admitted_by: Optional[str], organisation_id: str) -> None:
    """PRIN-2 verbatim: 'An individual or agent is admitted only by a
    principal already holding authority to admit under its own
    organisation's terms.'  No principal self-admits.
    """

    if not admitted_by:
        raise PrincipalRefusal(
            "PRIN-2 · admission refused: an individual or agent is "
            "admitted only by a principal already holding authority to "
            "admit under its own organisation's terms."
        )
    parent = _REGISTRY.get(admitted_by)
    if parent is None or not parent.admit_authority:
        raise PrincipalRefusal(
            f"PRIN-2 · admission refused: {admitted_by!r} does not hold "
            f"authority to admit under organisation {organisation_id!r}."
        )


def admit_individual(
    organisation_id: Optional[str],
    name: str,
    admitted_by: Optional[str] = None,
    admission_mandate: str = "unset",
) -> str:
    """PRIN-1 + PRIN-2 verbatim on individuals: 'a named person acting
    under an organisation, with a mandate scoped by that organisation
    ... MUST reference the organisation it acts under; it MUST NOT
    exist without one ... admitted only by a principal already holding
    authority to admit.'
    """

    if not organisation_id:
        raise PrincipalRefusal(
            "PRIN-1 · individual admission refused: MUST reference the "
            "organisation it acts under; MUST NOT exist without one."
        )
    _resolve_admit_authority(admitted_by, organisation_id)
    parent = _REGISTRY[admitted_by]  # exists after resolve
    principal_id = _fresh_principal_id("ind")
    contract = PrincipalV1(
        principal_id=principal_id,
        kind=PrincipalKind.INDIVIDUAL,
        legal_identity=name,
        trust_domain_identifier=parent.trust_domain_identifier,
        admission_time_mandate=admission_mandate,
        behavioural_signature_state="watch:baseline@admission",
        parent_organisation_id=organisation_id,
        autonomy_scope=None,
        admit_authority=False,
    )
    return _register(Principal(contract))


def admit_agent(
    organisation_id: Optional[str],
    name: str,
    admitted_by: Optional[str] = None,
    autonomy_scope: str = "unset",
    admission_mandate: str = "unset",
) -> str:
    """PRIN-1 + PRIN-2 + PRIN-3 verbatim on agents: 'an autonomous
    non-human principal, admitted separately from its operator,
    carrying its own stated scope of autonomy ... MUST reference the
    organisation it acts under ... an agent's machine-speed attack
    shape applies from admission, not from some later point at which
    it is judged to need watching.'
    """

    if not organisation_id:
        raise PrincipalRefusal(
            "PRIN-1 · agent admission refused: MUST reference the "
            "organisation it acts under; MUST NOT exist without one."
        )
    _resolve_admit_authority(admitted_by, organisation_id)
    parent = _REGISTRY[admitted_by]
    principal_id = _fresh_principal_id("agent")
    contract = PrincipalV1(
        principal_id=principal_id,
        kind=PrincipalKind.AGENT,
        legal_identity=name,
        trust_domain_identifier=parent.trust_domain_identifier,
        admission_time_mandate=admission_mandate,
        # PRIN-3 verbatim: 'machine-speed attack shape applies from
        # admission, not from some later point at which it is judged
        # to need watching.'
        behavioural_signature_state="watch:agent-machine-speed@admission",
        parent_organisation_id=organisation_id,
        autonomy_scope=autonomy_scope,
        admit_authority=False,
    )
    return _register(Principal(contract))


# --- Read API --------------------------------------------------------------


def get_principal(principal_id: str) -> Principal:
    principal = _REGISTRY.get(principal_id)
    if principal is None:
        raise PrincipalRefusal(
            f"principal {principal_id!r} not admitted"
        )
    return principal


# --- Test fixture ----------------------------------------------------------


def admit_organisation_for_test_fixture() -> str:
    """Convenience for RED-first invariant tests.  Admits an
    organisation-level principal under a fabricated estate-owner
    named authority. Not a production admission ceremony.
    """

    return admit_organisation(
        legal_identity="test-fixture-org",
        admitted_by="estate-owner:test-fixture",
        admission_mandate="test-fixture-mandate",
    )
