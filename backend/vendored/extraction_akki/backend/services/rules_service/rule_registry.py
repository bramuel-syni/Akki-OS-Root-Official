"""services.rules_service.rule_registry — W-M2-SW1.

The 286-rule register scaffold.  SW1 lands the framework + minimum
seed rules.  SW4 (W-286-RULE-ENUMERATION-CLASSIFY) lifts the remaining
272 rules.

Canon-3 §22: registered controls are additive.  The register is
append-only across ceremonies; supersession is a NEW entry that cites
the prior id and reason.

Canon-3 §9.3 (single-writer): a single writer commits each append;
concurrent writers converge by rejection, not by merge.  This module
holds a single in-process registry singleton reachable via
`get_rule_registry`.
"""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Finite enforcement-class taxonomy (Doc-0 Attr-4 · owner-directive).
ENFORCEMENT_CLASSES: Final[Tuple[str, ...]] = (
    "blocking",
    "declaratory",
    "reporting",
    "pending_override",
)


class RegistryAppendOnly(RuntimeError):
    """Raised on any attempt to modify or delete a registered rule."""


class RuleIdCollision(ValueError):
    """Raised when an id is re-appended.  Canon-3 §22 supersession
    requires a NEW id citing the prior."""


class RuleRecord(BaseModel):
    """A single registered control.

    * `rule_id` — canonical uppercase snake-case id.  Unique across the
      register.
    * `source_citation` — verbatim canon citation (Canon-N §... or
      Doc-0 §...).
    * `scope` — short human-readable scope tag.
    * `enforcement_class` — one of ENFORCEMENT_CLASSES.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    rule_id: str = Field(min_length=3, max_length=128)
    source_citation: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    enforcement_class: str

    @field_validator("enforcement_class")
    @classmethod
    def _enf(cls, v: str) -> str:
        if v not in ENFORCEMENT_CLASSES:
            raise ValueError(
                f"enforcement_class must be one of "
                f"{ENFORCEMENT_CLASSES}; got {v!r}"
            )
        return v


class RuleRegistry:
    """Append-only, unique-by-id, single-writer registry.

    In-process only for W-M2-SW1; persistence lands in SW3
    (W-RULE-BOOK-LIBRARY).
    """

    def __init__(self) -> None:
        self._rules: list[RuleRecord] = []
        self._index: dict[str, int] = {}

    def append(self, rec: RuleRecord) -> None:
        if rec.rule_id in self._index:
            raise RuleIdCollision(
                f"rule_id {rec.rule_id!r} already registered — Canon-3 "
                f"§22 supersession requires a NEW id citing the prior"
            )
        self._index[rec.rule_id] = len(self._rules)
        self._rules.append(rec)

    def remove(self, rule_id: str) -> None:
        raise RegistryAppendOnly(
            f"registry is append-only (Canon-3 §22); refusing to "
            f"remove {rule_id!r}"
        )

    def replace(self, rule_id: str, rec: RuleRecord) -> None:
        raise RegistryAppendOnly(
            f"registry is append-only (Canon-3 §22); refusing to "
            f"replace {rule_id!r}"
        )

    def get_by_id(self, rule_id: str) -> RuleRecord:
        if rule_id not in self._index:
            raise KeyError(f"rule_id {rule_id!r} not registered")
        return self._rules[self._index[rule_id]]

    def list_all(self) -> Tuple[RuleRecord, ...]:
        return tuple(self._rules)

    def list_by_class(self, enforcement_class: str) -> Tuple[RuleRecord, ...]:
        if enforcement_class not in ENFORCEMENT_CLASSES:
            raise ValueError(
                f"enforcement_class must be one of "
                f"{ENFORCEMENT_CLASSES}; got {enforcement_class!r}"
            )
        return tuple(
            r for r in self._rules if r.enforcement_class == enforcement_class
        )


# --- seed rules ------------------------------------------------------
# Three canonical anchors seeded at bootstrap.  SW4 lifts the remaining
# rules from Master_Requirements_Registry.xlsx (272 rows).

_SEEDS: Tuple[RuleRecord, ...] = (
    RuleRecord(
        rule_id="RULES_SERVICE_R_1",
        source_citation="Doc-0 Attr-4 · Ratification_Record_v1 R-1 · "
                        "48h system-ordinary / 7d system-TCB countdown",
        scope="rules_service.countdown",
        enforcement_class="blocking",
    ),
    RuleRecord(
        rule_id="DAP_R_1_CONTROLLED_UNIT",
        source_citation="DAP-Spec §8 · Ratification_Record_v1 DAP R-1 · "
                        "controlled-unit alignment",
        scope="dap.controlled_unit",
        enforcement_class="blocking",
    ),
    RuleRecord(
        rule_id="SFP_8",
        source_citation="Serving_Integrity_Amendment_v1 §B V-2 · "
                        "A20.15 SFP-8 serving floor",
        scope="serving_path.integrity",
        enforcement_class="blocking",
    ),
)


_SINGLETON: RuleRegistry | None = None


def get_rule_registry() -> RuleRegistry:
    """Return the process-wide singleton registry.

    Constructed on first call with the seed rules.  Subsequent
    additions (SW2..SW4) may append but never modify prior entries.
    """
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = RuleRegistry()
        for seed in _SEEDS:
            _SINGLETON.append(seed)
    return _SINGLETON


__all__ = [
    "ENFORCEMENT_CLASSES",
    "RuleRecord",
    "RuleRegistry",
    "RegistryAppendOnly",
    "RuleIdCollision",
    "get_rule_registry",
]
