"""services.watch.certificate_library — W-M3-SW3 · Watch Learning L-1/L-2.

Certificate requirement library + deterministic gate.  RBM-23:
certificate requirements are tier system-TCB · enter force through
RBM-8 ceremony.
"""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator


CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE: Final[str] = "PENDING-OVERRIDE"


class CertificateGateRefused(RuntimeError):
    """Fail-closed certificate gate refusal."""


class CertificateRequirement(BaseModel):
    """A ratified certificate requirement (A5.20)."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    requirement_id: str = Field(min_length=1)
    behaviour_asserted: str = Field(min_length=1)
    required_data_points: Tuple[str, ...] = Field(min_length=1)
    ratifier_role_pending_override: str  # PENDING-OVERRIDE per R-16
    tier: str

    @field_validator("tier")
    @classmethod
    def _tier(cls, v: str) -> str:
        # RBM-23: tier is exactly 'system_tcb'.
        if v != "system_tcb":
            raise ValueError(
                f"RBM-23 requires tier=='system_tcb'; got {v!r}"
            )
        return v


class Certificate(BaseModel):
    """A certificate as A5.19 defines it — carried on the verdict."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    requirement_id: str = Field(min_length=1)
    data_points: Tuple[str, ...] = Field(min_length=1)
    observation_refs: Tuple[str, ...] = Field(min_length=1)


def check_certificate_satisfies_requirement(
    cert: Certificate, req: CertificateRequirement
) -> bool:
    """Deterministic satisfaction check (A5.20).  Pure predicate."""
    if cert.requirement_id != req.requirement_id:
        return False
    # Every required data point must appear in the certificate's
    # observed data points.
    return set(req.required_data_points) <= set(cert.data_points)


def certificate_gate(
    cert: Certificate, req: CertificateRequirement
) -> None:
    """Fail-closed gate — refuse if not satisfied."""
    if cert.requirement_id != req.requirement_id:
        raise CertificateGateRefused(
            f"certificate cites requirement {cert.requirement_id!r} "
            f"but requirement is {req.requirement_id!r}"
        )
    missing = set(req.required_data_points) - set(cert.data_points)
    if missing:
        raise CertificateGateRefused(
            f"certificate for {req.requirement_id!r} missing required "
            f"data points: {sorted(missing)!r}"
        )


# --- R-15 seed: DAP-32 canary + AC-1 four ceilings ------------------
# Amendment §3 recommendation.  Rows carry PENDING-OVERRIDE marker on
# `ratifier_role_pending_override` — an owner ruling flips one bit +
# a lineage entry to make each row ratified.

_R15_SEED: Tuple[CertificateRequirement, ...] = (
    CertificateRequirement(
        requirement_id="DAP32_CANARY_TOUCH",
        behaviour_asserted="probe.canary_touched",
        required_data_points=("dp.canary_hash", "dp.access_time", "dp.principal_id"),
        ratifier_role_pending_override=CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE,
        tier="system_tcb",
    ),
    CertificateRequirement(
        requirement_id="AC1_SELF_REPLICATION",
        behaviour_asserted="ac1.self_replication",
        required_data_points=("dp.replica_evidence", "dp.spawn_signal"),
        ratifier_role_pending_override=CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE,
        tier="system_tcb",
    ),
    CertificateRequirement(
        requirement_id="AC1_RESOURCE_ACQUISITION",
        behaviour_asserted="ac1.resource_acquisition",
        required_data_points=("dp.resource_grant", "dp.acquiring_principal"),
        ratifier_role_pending_override=CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE,
        tier="system_tcb",
    ),
    CertificateRequirement(
        requirement_id="AC1_CREDENTIAL_ESCALATION",
        behaviour_asserted="ac1.credential_escalation",
        required_data_points=("dp.cred_before", "dp.cred_after", "dp.escalating_principal"),
        ratifier_role_pending_override=CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE,
        tier="system_tcb",
    ),
    CertificateRequirement(
        requirement_id="AC1_OVERSIGHT_TAMPERING",
        behaviour_asserted="ac1.oversight_tampering",
        required_data_points=("dp.oversight_target", "dp.tamper_signal"),
        ratifier_role_pending_override=CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE,
        tier="system_tcb",
    ),
)


def get_certificate_library() -> Tuple[CertificateRequirement, ...]:
    """Return the current certificate-requirement library.

    Seeded with R-15 defaults (DEFAULT-PENDING-OVERRIDE); an owner
    ruling swaps rows in via RBM-8 ceremony + lineage entry.
    """
    return _R15_SEED


__all__ = [
    "CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE",
    "CertificateGateRefused",
    "CertificateRequirement",
    "Certificate",
    "check_certificate_satisfies_requirement",
    "certificate_gate",
    "get_certificate_library",
]
