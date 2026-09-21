"""W-CENSUS-CANON-ALIGN · CP-C1 · Deterministic sensitivity classifier.

Canon-4 §5.1 (line 35) verbatim:
    "A per-feed declaration, applied to every source under that feed —
     deterministic, low-cardinality, and always available. It is the certain
     floor the whole measure rests on … An undeclared feed resolves to
     unknown, which is the conservative value — absence of a declaration
     never resolves upward."

Master Requirements Registry Doc-9 B5.5 (:148) verbatim:
    "The defensibility verdict is a deterministic matrix lookup carrying its
     rule reference."

Master Requirements Registry Doc-9 B5.7 (:150) verbatim:
    "Sensitivity classification is the single entitlement attribute."
"""

from __future__ import annotations

from typing import Mapping

from contracts.canon_census_source_candidate import (
    Sensitivity, UNDECLARED_SENSITIVITY_CLASS_LABEL,
)


# The rule-reference token that appears in a Sensitivity produced from a
# feed-declaration-registry lookup (as opposed to the Canon-4 §5.1
# conservative-fallback path). Named so tests can assert on it.
FEED_DECLARATION_REGISTRY_KEY: str = "feed_declaration_registry"


def classify_sensitivity(
    *,
    feed_identity: str,
    feed_declaration_registry: Mapping[str, str],
) -> Sensitivity:
    """Deterministic matrix-lookup classifier.

    A feed's declaration is looked up in ``feed_declaration_registry`` by
    ``feed_identity``. Two paths:

    * declared: returns ``Sensitivity(class_label=<declared>,
      is_undeclared=False, rule_reference="feed_declaration_registry/<feed>")``
    * undeclared: returns ``Sensitivity(class_label="unknown",
      is_undeclared=True, rule_reference="Canon-4 §5.1 conservative fallback")``
      per §5.1 (absence of a declaration never resolves upward).

    The classifier is deterministic: same ``feed_identity`` + same registry
    contents → same ``Sensitivity`` value (B5.5).
    """
    if feed_identity in feed_declaration_registry:
        class_label = feed_declaration_registry[feed_identity]
        rule_reference = f"{FEED_DECLARATION_REGISTRY_KEY}/{feed_identity}"
        return Sensitivity(
            class_label=class_label,
            is_undeclared=False,
            rule_reference=rule_reference,
        )
    return Sensitivity(
        class_label=UNDECLARED_SENSITIVITY_CLASS_LABEL,
        is_undeclared=True,
        rule_reference="Canon-4 §5.1 conservative fallback",
    )
