"""services.governance_plane.cross_table_consistency — M8 · CP-M8-CTCC-1.

Preventive contract per SPRINT_PLAN.md:61-66 verbatim:

    "W-Cross-Table-Consistency-Check — for waves emitting multiple
    identifier-shaped columns. Scope: static + runtime check that no
    combination of emitted columns across tables can reconstruct an
    identifier. Prerequisites: any wave emitting >1 identifier-shaped
    column from >1 table (preventive charter). Outcome:
    refuses-unclassified-by-construction extends per-emitted-set,
    closing a theoretical cross-table leak channel."

Charter source (upstream): W-Multi-Table-Extract wave-honest-limit F.2
(cross-table PII correlation not checked when both columns excluded).

Case-agnostic doctrine (owner correction 2026-09-13 verbatim, applied):
  - class_id is OPEN str (no Literal, no closed Enum on identifier
    discriminator).
  - Zero closed enums in this module.
  - Zero domain tokens in source or docstring examples.
  - Zero imports of dispatch surfaces.
  - Zero refuse_dispatch / kill_ / terminate_ / unregister names on
    public surface.

Reconstruction rule. An identifier class ``ic`` is at cross-table
reconstruction risk iff the subset of ``ic.columns_in_class`` that
appear in the emitted set spans **more than one distinct table_id**.
Coarse rule by design (wave-honest limit D.2); statistical linkability
/ k-anonymity / entropy reasoning are chartered-forward refinements.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


__all__ = [
    "EmittedColumnRef",
    "IdentifierClass",
    "assess_reconstruction_risk",
    "assert_no_cross_table_identifier_reconstruction",
    "CrossTableIdentifierReconstructionRefused",
]


@dataclass(frozen=True)
class EmittedColumnRef:
    """A single emitted column, identified by opaque (table_id, column_name)."""

    table_id: str
    column_name: str


@dataclass(frozen=True)
class IdentifierClass:
    """A declared identifier class · maps a class_id to the tuple of
    contributing columns across tables.

    ``class_id`` is an OPEN str (case-agnostic doctrine). Caller-chosen.
    """

    class_id: str
    columns_in_class: Tuple[EmittedColumnRef, ...]


class CrossTableIdentifierReconstructionRefused(Exception):
    """Raised when the emitted-column set spans more than one table_id
    for at least one declared identifier class."""


def assess_reconstruction_risk(
    *,
    emitted_columns: Tuple[EmittedColumnRef, ...],
    identifier_class_declarations: Tuple[IdentifierClass, ...],
) -> Tuple[str, ...]:
    """Return the tuple of ``class_id``s at cross-table reconstruction
    risk. Empty tuple = safe. Output is deterministic sorted."""
    emitted_set = set(emitted_columns)
    risky = []
    for ic in identifier_class_declarations:
        contributing = tuple(c for c in ic.columns_in_class if c in emitted_set)
        tables_contributing = {c.table_id for c in contributing}
        if len(tables_contributing) > 1:
            risky.append(ic.class_id)
    return tuple(sorted(risky))


def assert_no_cross_table_identifier_reconstruction(
    *,
    emitted_columns: Tuple[EmittedColumnRef, ...],
    identifier_class_declarations: Tuple[IdentifierClass, ...],
) -> None:
    """Raise ``CrossTableIdentifierReconstructionRefused`` when
    ``assess_reconstruction_risk`` returns a non-empty tuple."""
    risky = assess_reconstruction_risk(
        emitted_columns=emitted_columns,
        identifier_class_declarations=identifier_class_declarations,
    )
    if risky:
        raise CrossTableIdentifierReconstructionRefused(
            f"identifier classes at cross-table reconstruction risk: {risky}"
        )
