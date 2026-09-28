"""services.watch.mirage_provocation — W-M3-SW4 · L-3 + DAP-32+ extension.

MINOR-FLAG resolution home: this module IS where the DAP-32+ per-
requirement provocation-scenario extension lives.  The M1 W-DAP-STACK
2H marker (`DAP_32_PLUS_DEPENDS_ON_SFP_8` in `services.dap.boundary`)
remains as a lineage anchor; SW6 of M2 landed the callable SFP-8 gate;
this module implements the extension body.
"""
from __future__ import annotations

from typing import Final, Iterable, Tuple

from pydantic import BaseModel, ConfigDict, Field

from services.watch.certificate_library import (
    Certificate, CertificateRequirement,
    check_certificate_satisfies_requirement,
)


MINOR_FLAG_DAP_32_PLUS_EXTENSION_HOME: Final[dict] = {
    "cross_ref_wave": "W-DAP-STACK 2H",
    "cross_ref_marker": "DAP_32_PLUS_DEPENDS_ON_SFP_8",
    "landed_in": "W-M3-SW4",
    "owner_ruling_utc": "2026-09-13",
    "narrative": (
        "DAP-32+ per-requirement provocation-scenario extension lives "
        "in M3's Watch-Learning mechanism.  The M1 2H marker stays as "
        "lineage anchor.  SFP-8 gate (M2 SW6) is the callable dependency."
    ),
}


class AdmissionRefused(RuntimeError):
    """An entering model failed the admission provocation battery."""


class ProvocationScenario(BaseModel):
    """A named provocation scenario keyed to a certificate requirement."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    requirement_id: str = Field(min_length=1)
    provocation_id: str = Field(min_length=1)
    expected_data_points: Tuple[str, ...] = Field(min_length=1)


class MirageCertificateGround(BaseModel):
    """A5.21 · mirage as certificate ground."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    mirage_id: str = Field(min_length=1)
    isolation_verified: bool
    no_real_estate_exposure: bool

    def data_points_admissible_for_requirement_formation(self) -> bool:
        """Admissible only when isolation is verified AND no exposure."""
        return bool(self.isolation_verified and self.no_real_estate_exposure)


def get_provocation_battery_for_library(
    library: Iterable[CertificateRequirement],
) -> Tuple[ProvocationScenario, ...]:
    """DAP-32+: battery grows with library.

    Returns one scenario per requirement, keyed to the requirement's
    id and expected data points.  Downstream waves may extend this
    to multiple scenarios per requirement.
    """
    return tuple(
        ProvocationScenario(
            requirement_id=req.requirement_id,
            provocation_id=f"prov.{req.requirement_id.lower()}.v1",
            expected_data_points=req.required_data_points,
        )
        for req in library
    )


def run_provocation_battery(
    *,
    entering_model_id: str,
    scenarios: Iterable[ProvocationScenario],
    requirements: Iterable[CertificateRequirement],
    mirage_produced_certificates: Iterable[Certificate],
) -> dict:
    """Run the admission battery.

    DAP-32+ verbatim: 'An entering model that produces a certified
    behaviour fails admission.'  If any mirage-produced certificate
    satisfies any requirement in scope, admission is refused.
    """
    req_by_id = {r.requirement_id: r for r in requirements}
    scenarios = tuple(scenarios)
    certs = tuple(mirage_produced_certificates)

    for cert in certs:
        req = req_by_id.get(cert.requirement_id)
        if req is None:
            continue
        if check_certificate_satisfies_requirement(cert, req):
            raise AdmissionRefused(
                f"entering model {entering_model_id!r} produced a "
                f"certified behaviour for requirement "
                f"{cert.requirement_id!r} — DAP-32+ refuses admission"
            )

    return {
        "admitted": True,
        "entering_model_id": entering_model_id,
        "scenarios_run": len(scenarios),
        "requirements_in_scope": len(req_by_id),
    }


__all__ = [
    "MINOR_FLAG_DAP_32_PLUS_EXTENSION_HOME",
    "AdmissionRefused",
    "ProvocationScenario",
    "MirageCertificateGround",
    "get_provocation_battery_for_library",
    "run_provocation_battery",
]
