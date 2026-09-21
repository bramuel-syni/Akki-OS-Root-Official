"""services/entitlement_service_v1 · Entitlement Service v1 build wave (R-82).

CP-ENTITLEMENT-BUILD-WAVE · WAVE R-82 · own 3-Commit Seal · lands the
implementation surfaces that make the CP-ENTITLEMENT-WAVE-SETUP (R-81) RED-first
property tests transition their Phase-1 absence-attestation to Phase-2 structural
enforcement.

Owner confirmed sprint order for this wave verbatim (2026-09-20T~16:00Z):

    "CP-ENTITLEMENT-BUILD-WAVE (R-82): YES — proceed on autopilot now,
     scope exactly as you stated: Local + Your-Keys paths; reseller-frontier
     UNLISTED (HARD HOLD pending R-24); R-26..R-30 at DEFAULT-class values
     tagged pending; R-31 seats-as-default with separate agent count at
     organisation size; consumes sealed principal_v1 + contracts.dap.MeteredEvent
     + credential plane; no new identity system, no new metering path, no new
     bill; new module tree services/entitlement_service_v1/ only."

Scope frozen SO §6.4 NOTHING-BEYOND at this wave:

  · Licence object (§3 ENT-5..8) at `licence.py`.
  · Catalog row (§4 ENT-9..13) at `catalog.py`.
  · Credential envelope wrapper (§11 ENT-35..36) at `customer_key_plane.py`
    (consumes sealed `services.credential_plane` for revocation semantics).
  · Chokepoint resolver (§6 ENT-16..19) at `chokepoint_resolver.py` — pure
    function of (principal, licence, catalog_row, allowance_state).
  · Cascade selector (§8 ENT-26 + §10 ENT-34) at `cascade_selector.py` —
    emits ENT-26 fixed string on exhaustion, ENT-34 on unreachable, chooses
    customer-key over reseller-frontier per ENT-19.
  · Allowance derivation (§7 ENT-22) at `allowance.py` — pure derivation
    from Ledger events, no stored counter.

HARD HOLDs at this wave per confirmed sprint order verbatim:

  · Reseller-frontier channel — module `reseller_channel.py` NOT authored
    (ENT-32 gate: pending R-24 counsel-reviewed reseller agreement). ENT-32
    property test's Phase-2 accepts module absence as HARD-HOLD attestation.
  · R-26 rollover default (recommend 1 period), R-27 seat soft-limit default
    (recommend 80%), R-28 fairness ceiling defaults (recommend baseline
    approach), R-29 key scope default (organisation, seat-scoped permitted
    with precedence), R-30 GPU-seconds compute allowance default — all
    DEFAULT-class values tagged pending owner ratification. Constants
    exported with `_DEFAULT_PENDING_OWNER_RATIFICATION` suffix to make
    grep-visible that the numeric is not-yet-a-rule.
  · R-31 seats-as-default with separate agent count at organisation size —
    catalog `Licence.agent_count` field is Optional at this wave (None at
    small orgs · integer at organisation-size upgrades).

Standing bounds honoured at this wave:

  · SO §3.8 additive-only. Sealed contracts consumed by identity import:
    `contracts.principal_v1.PrincipalV1` + `contracts.principal_v1.PrincipalKind`
    + `contracts.dap.MeteredEvent` + `services.credential_plane.plane.
    issue_credential/revoke_credential/is_revoked/resolve_identity`. Zero
    sealed contract edit; zero sealed writer edit.
  · SO §3.10-α closed-schema on every pydantic BaseModel authored:
    `frozen=True` + `extra="forbid"`.
  · Canon 8 §W11 one-task-one-identity: each module owns one surface
    (resolve · select_cascade · derive_allowance · wrap_credential · Licence
    · CatalogRow).
  · ENT-49 (§15) state stored only as Licence field / Catalog row /
    Credential envelope / Ledger event — every pydantic model authored here
    has a name matching one of the four allowed prefixes (Licence*, Catalog*,
    Credential*, LedgerEvent*).
  · ENT-20 (§7) no entitlement-specific metered-event class authored;
    metering consumes sealed `contracts.dap.MeteredEvent` by identity import.
  · ENT-21 (§7) no second billing store authored; bill is a derived query
    over Ledger events (see `allowance.derive_allowance_remaining`).

Canon anchors verbatim (drawn from `notes/entitlement_service_v1_atomic_rules.md`
which pins the docx source sha256 `46c3670e…`):

  · §3 ENT-5..8 Licence Object · §4 ENT-9..13 Catalog · §6 ENT-16..19
    Chokepoint Resolution · §7 ENT-20..23 Metering + Bill · §8 ENT-24..28
    Credits Limits Exhaustion · §10 ENT-32..34 Reseller Channels · §11
    ENT-35..40 Bring Your Own · §14 ENT-43..46 Surfaces · §15 ENT-47..49
    Managing the Catalog · §19 R-24..R-31 Rulings.

Public API (this package):
"""
from __future__ import annotations

from services.entitlement_service_v1.licence import (
    Licence,
    LicenceRefusal,
    LICENCE_STATUS_ACTIVE,
    LICENCE_STATUS_SUSPENDED,
    LICENCE_STATUS_EXPIRED,
    R_26_ROLLOVER_PERIODS_DEFAULT_PENDING_OWNER_RATIFICATION,
    R_27_SEAT_SOFT_LIMIT_FRACTION_DEFAULT_PENDING_OWNER_RATIFICATION,
    R_29_KEY_SCOPE_DEFAULT_PENDING_OWNER_RATIFICATION,
)
from services.entitlement_service_v1.catalog import (
    CatalogRow,
    CATALOG_STATUS_LISTED,
    CATALOG_STATUS_PAUSED,
    CATALOG_STATUS_RETIRED,
    ACCESS_CLASS_LOCAL_SERVED,
    ACCESS_CLASS_CUSTOMER_KEY,
    ACCESS_CLASS_CUSTOMER_MODEL,
    ACCESS_CLASS_RESELLER_FRONTIER,
)
from services.entitlement_service_v1.customer_key_plane import (
    CredentialEnvelope,
    wrap_customer_key,
    revoke_customer_key,
    is_customer_key_revoked,
)
from services.entitlement_service_v1.chokepoint_resolver import (
    resolve,
    ResolutionRefusal,
)
from services.entitlement_service_v1.cascade_selector import (
    select_cascade,
    ENT_26_FRONTIER_EXHAUSTION_FIXED_STRING,
    ENT_34_FRONTIER_UNAVAILABLE_FIXED_STRING,
)
from services.entitlement_service_v1.allowance import (
    derive_allowance_remaining,
    LicenceAllowanceState,
)

__all__ = [
    "Licence",
    "LicenceRefusal",
    "LICENCE_STATUS_ACTIVE",
    "LICENCE_STATUS_SUSPENDED",
    "LICENCE_STATUS_EXPIRED",
    "R_26_ROLLOVER_PERIODS_DEFAULT_PENDING_OWNER_RATIFICATION",
    "R_27_SEAT_SOFT_LIMIT_FRACTION_DEFAULT_PENDING_OWNER_RATIFICATION",
    "R_29_KEY_SCOPE_DEFAULT_PENDING_OWNER_RATIFICATION",
    "CatalogRow",
    "CATALOG_STATUS_LISTED",
    "CATALOG_STATUS_PAUSED",
    "CATALOG_STATUS_RETIRED",
    "ACCESS_CLASS_LOCAL_SERVED",
    "ACCESS_CLASS_CUSTOMER_KEY",
    "ACCESS_CLASS_CUSTOMER_MODEL",
    "ACCESS_CLASS_RESELLER_FRONTIER",
    "CredentialEnvelope",
    "wrap_customer_key",
    "revoke_customer_key",
    "is_customer_key_revoked",
    "resolve",
    "ResolutionRefusal",
    "select_cascade",
    "ENT_26_FRONTIER_EXHAUSTION_FIXED_STRING",
    "ENT_34_FRONTIER_UNAVAILABLE_FIXED_STRING",
    "derive_allowance_remaining",
    "LicenceAllowanceState",
]
