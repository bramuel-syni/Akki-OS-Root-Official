"""W-DATA-SUITE-V2-LIFT · CP-D6 · Export release gate (discharges DAP-Spec §A10).

DAP-A10: exports must carry rights posture + hash + derivation from controlled
units + terms cited. `admit_export` is the gate that fires; it refuses release
if any of the four required carriers is empty, naming the missing carrier in
the refusal.
"""

from __future__ import annotations

from services.data_suite_v2.export_artefact import ExportArtefact


class ExportRefused(Exception):
    """Raised when an ExportArtefact is missing any DAP-A10 carrier at release."""


REQUIRED_CARRIERS = (
    "rights_posture",
    "derivation_hash",
    "derivation_unit_refs",
    "terms_cited",
)


def admit_export(artefact: ExportArtefact) -> None:
    """Admit or refuse an export artefact per DAP-Spec §A10.

    Returns None on success; raises `ExportRefused` naming the first missing
    carrier when any of the four required carriers is empty (empty string or
    empty sequence).
    """
    for name in REQUIRED_CARRIERS:
        value = getattr(artefact, name)
        if not value:
            raise ExportRefused(
                f"DAP-A10 refusal: required carrier {name!r} is empty; "
                f"required carriers: {REQUIRED_CARRIERS}"
            )
    return None
