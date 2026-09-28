"""CP-AIP-7-TARGET-OUTCOME-PLANNER · register_stratum_resolver_v1 · additive §1.2.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-7-TARGET-OUTCOME-PLANNER and nothing else.

Spec anchor: AIP v1.0 §11.1 verbatim: 'population is register-defined,
not label-defined.' + §10.2 verbatim: 'Population is register-defined.'

This module resolves a `TargetOutcome_v0.population` string against a
sealed `CharacterRegister.entries[].layer` value-set. Refuses with
`PopulationNotResolvableAgainstRegister` if the population string is
not a `CharacterEntry.layer` value present in the register.

Sealed carriers composed (UNCHANGED per SO §3.8):
- backend/services/audio_plane_v1/character_register.py (CP-M6-3):
  `CharacterRegister` frozen dataclass with `.entries` tuple of
  `CharacterEntry`.

Additive-only per SO §3.8 · no edit to sealed CharacterRegister.
"""
from __future__ import annotations

from typing import Final

from backend.services.audio_plane_v1.character_register import CharacterRegister


HONEST_GAP_V1_POSTURE: Final[str] = (
    "CP-AIP-7-TARGET-OUTCOME-PLANNER · §11.1 verbatim: "
    "'population is register-defined, not label-defined.' "
    "This resolver refuses population strings unresolved against the "
    "register's layer-value-set at planner entry."
)


class PopulationNotResolvableAgainstRegister(ValueError):
    """§11.1 verbatim refusal at planner entry: the population string
    is not a `CharacterEntry.layer` value present in the register."""


def resolve_population_against_register(
    *,
    population: str,
    character_register: CharacterRegister,
) -> str:
    """§11.1 verbatim boundary: resolve `population` string against
    the register's layer-value-set.

    Returns the resolved population string (identity mapping) when
    `population` is a `CharacterEntry.layer` value present in the
    register.

    Refuses with `PopulationNotResolvableAgainstRegister` otherwise.

    Args:
      population: `TargetOutcome_v0.population` string.
      character_register: sealed CP-M6-3 `CharacterRegister` instance.

    Raises:
      PopulationNotResolvableAgainstRegister: §11.1 verbatim refusal.
    """
    layer_values = frozenset(
        entry.layer for entry in character_register.entries
    )
    if population not in layer_values:
        raise PopulationNotResolvableAgainstRegister(
            f"CP-AIP-7 · §11.1 verbatim: population {population!r} is "
            f"not a CharacterEntry.layer value in the current register "
            f"(register layers: {sorted(layer_values)!r}). "
            f"§10.2 verbatim: 'Population is register-defined.'"
        )
    return population
