"""CP-TENANT-SEPARATION · tenant_separation_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.11.d
CP-TENANT-SEPARATION and nothing else. Additive-only per SO §3.8. Sealed
CP-ENT-16 pilot_licence_seeds_v1 UNCHANGED. Terminal pytest only. RED-first
mechanical.

Owner directive verbatim (SO §6.9 amendment §6 item 7 +
`na7p4_park_proceed_autonomously_mirror_probe_20260223/DROP.md`):
    'tenant separation with named authorities Fred Afune / Muthoni Kiarie /
     Samuel Kibacia [RMS] + Vincent Kimani / Peninah Wanja [DigiCow],
     any-one decision rule, isolation sweep as exit evidence.'

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Tuple


# ---------------------------------------------------------------------------
# Named authorities (owner verbatim)
# ---------------------------------------------------------------------------


RMS_APPROVING_AUTHORITIES: Final[Tuple[str, str, str]] = (
    "Fred Afune",
    "Muthoni Kiarie",
    "Samuel Kibacia",
)


DIGICOW_APPROVING_AUTHORITIES: Final[Tuple[str, str]] = (
    "Vincent Kimani",
    "Peninah Wanja",
)


AKKI_TEST_APPROVING_AUTHORITIES: Final[Tuple[str, ...]] = ()


AKKI_TEST_HONEST_GAP_POSTURE: Final[str] = (
    "AKKI-TEST tenant carries no named approving authorities on record "
    "at this seal boundary. The owner has enumerated named authorities "
    "for RMS + DigiCow tenants only. AKKI-TEST is the internal test "
    "tenant per CP-ENT-16 pilot licence seeds; a follow-on owner ruling "
    "is required to name approving authorities for it. Honest-gap "
    "banked; the empty tuple is not silently accepted downstream — "
    "any tenant_name='AKKI-TEST' input to "
    "approve_by_any_one_named_authority raises UnknownAuthorityRefused "
    "because no authority is on record."
)


ALL_NAMED_APPROVING_AUTHORITIES: Final[Tuple[str, ...]] = (
    *RMS_APPROVING_AUTHORITIES,
    *DIGICOW_APPROVING_AUTHORITIES,
)


TENANT_SEPARATION_ANY_ONE_RULE_POSTURE: Final[str] = (
    "CP-TENANT-SEPARATION · SO §6.9 amendment §6 item 7 verbatim: "
    "'tenant separation with named authorities Fred Afune / Muthoni "
    "Kiarie / Samuel Kibacia [RMS] + Vincent Kimani / Peninah Wanja "
    "[DigiCow], any-one decision rule, isolation sweep as exit "
    "evidence.' Any-one rule: exactly one named authority from the "
    "tenant approves; cross-tenant authorities are refused; unknown "
    "authorities are refused. Isolation sweep proves the RMS and "
    "DigiCow authority sets are disjoint (overlap_count = 0) — this "
    "is the EXIT EVIDENCE per owner verbatim."
)


# Tenant name → authorities tuple (built after all authorities defined)
_TENANT_TO_AUTHORITIES: Final[dict] = {
    "RMS": RMS_APPROVING_AUTHORITIES,
    "DigiCow": DIGICOW_APPROVING_AUTHORITIES,
    "AKKI-TEST": AKKI_TEST_APPROVING_AUTHORITIES,
}


# ---------------------------------------------------------------------------
# Refusal hierarchy
# ---------------------------------------------------------------------------


class TenantSeparationBoundaryRefused(Exception):
    """Base for all tenant-separation boundary refusals."""


class UnknownTenantRefused(TenantSeparationBoundaryRefused):
    """Tenant name not among the three pilot-licence tenants (CP-ENT-16)."""


class UnknownAuthorityRefused(TenantSeparationBoundaryRefused):
    """Approving authority not in ALL_NAMED_APPROVING_AUTHORITIES."""


class CrossTenantAuthorityRefused(TenantSeparationBoundaryRefused):
    """Authority belongs to a different tenant than the one being approved."""


# ---------------------------------------------------------------------------
# Frozen carriers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TenantApprovalDecision_v1:
    """Structural approval receipt from the any-one rule."""
    tenant_name: str
    approving_authority: str


@dataclass(frozen=True)
class TenantIsolationSweepReceipt_v1:
    """Exit-evidence receipt from the isolation sweep."""
    rms_authorities_count: int
    digicow_authorities_count: int
    overlap_count: int
    overlap: Tuple[str, ...]
    disjoint: bool


# ---------------------------------------------------------------------------
# Boundary callables
# ---------------------------------------------------------------------------


def approve_by_any_one_named_authority(
    tenant_name: str, approving_authority: str
) -> TenantApprovalDecision_v1:
    """Any-one decision rule: exactly one named authority from the tenant approves.

    Refuses:
    - tenant_name not in {RMS, DigiCow, AKKI-TEST} → UnknownTenantRefused.
    - approving_authority not in ALL_NAMED_APPROVING_AUTHORITIES → UnknownAuthorityRefused.
    - approving_authority not in the tenant's authority tuple → CrossTenantAuthorityRefused.
    """
    if tenant_name not in _TENANT_TO_AUTHORITIES:
        raise UnknownTenantRefused(
            f"unknown tenant_name={tenant_name!r}; must be one of "
            f"{tuple(_TENANT_TO_AUTHORITIES.keys())}"
        )
    if approving_authority not in ALL_NAMED_APPROVING_AUTHORITIES:
        raise UnknownAuthorityRefused(
            f"unknown approving_authority={approving_authority!r}; "
            f"must be one of {ALL_NAMED_APPROVING_AUTHORITIES}"
        )
    tenant_authorities = _TENANT_TO_AUTHORITIES[tenant_name]
    if approving_authority not in tenant_authorities:
        raise CrossTenantAuthorityRefused(
            f"approving_authority={approving_authority!r} is not among "
            f"{tenant_name!r} authorities {tenant_authorities}"
        )
    return TenantApprovalDecision_v1(
        tenant_name=tenant_name,
        approving_authority=approving_authority,
    )


def run_tenant_isolation_sweep() -> TenantIsolationSweepReceipt_v1:
    """Compute + emit exit-evidence receipt proving RMS/DigiCow authority sets disjoint.

    Owner verbatim: 'isolation sweep as exit evidence'.
    """
    rms_set = set(RMS_APPROVING_AUTHORITIES)
    dc_set = set(DIGICOW_APPROVING_AUTHORITIES)
    overlap = tuple(sorted(rms_set & dc_set))
    return TenantIsolationSweepReceipt_v1(
        rms_authorities_count=len(RMS_APPROVING_AUTHORITIES),
        digicow_authorities_count=len(DIGICOW_APPROVING_AUTHORITIES),
        overlap_count=len(overlap),
        overlap=overlap,
        disjoint=(len(overlap) == 0),
    )
