"""services.doc0_attributes.subsystems — W-M2-SW8 · Doc-0 Attr-2."""
from __future__ import annotations

from typing import Iterable, List

from pydantic import BaseModel, ConfigDict, Field


class Subsystem(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    declared_interface: str = Field(min_length=1)


_REGISTERED: List[Subsystem] = []


def register_subsystem(s: Subsystem) -> None:
    _REGISTERED.append(s)


def list_subsystems() -> tuple[Subsystem, ...]:
    return tuple(_REGISTERED)


def linter_declared_interface_missing(
    subsystems: Iterable[Subsystem],
) -> list[str]:
    """Return names of subsystems missing a declared interface.

    Because `declared_interface` is enforced non-empty by Subsystem's
    validator, this linter serves as a defence-in-depth check across
    externally-sourced subsystem dicts before they become Subsystem
    instances.  Always returns [] for well-formed instances.
    """
    return [s.name for s in subsystems if not (s.declared_interface or "").strip()]


__all__ = [
    "Subsystem", "register_subsystem", "list_subsystems",
    "linter_declared_interface_missing",
]
