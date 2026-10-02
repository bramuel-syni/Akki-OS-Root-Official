"""services.chokepoint.llm_purpose_gate — W5 · Ruling 1 · Purpose Gate.

Owner Order 2026-08-25 · "W5 go" §5:
    "PURPOSE GATE per Ruling 1: purpose is declared per call and
     validated against an allowed-purposes register before invoke (the
     discipline Executive-Core carried); refusal on missing/unknown
     purpose. Ruling 1's strip-condition (declaration ✓ banked; Watch
     reconciler pending W9) means the purpose gate CANNOT be skipped."

Owner correction 2026-08-25 · canon vocabulary is Solva. Purpose IDs
    are `solva.frame_audit`, `solva.candidate_generation`,
    `solva.synthesis` — never `solver.*`.

ADAPTED from Akki-Executive-Final/backend/services/synisense/shield/
purpose_validator.py (60 LOC donor · same exact-match + wildcard shape).
The donor's INTERNAL_ONLY_PURPOSE_PREFIXES concept is dropped in this
adaptation because W5 has no external HTTP purpose caller — every
`invoke()` call is internal to the estate. If a boundary caller ever
lands (Doc 05 §A6 external-authority admits), the gate reintroduces
the internal-prefix constraint.

Contract:
    validate_purpose(purpose) → None on success
                              → raise PurposeInvalid on failure
    ALLOWED_PURPOSES: frozenset of exact-match strings + `.*` wildcards.

Wildcard grammar (donor semantics):
    An entry ending `.*` matches any purpose whose stem is the prefix.
    Example: `solva.*` admits `solva.frame_audit` AND `solva.custom`.
    W5 declares individual entries (no wildcards yet) — additive shape
    for later waves.

Governance:
    Adding a purpose to the allowlist requires an Owner ruling recorded
    in STATE/DECISIONS.md. This module's ALLOWED_PURPOSES set is the
    positive-allowlist authority.
"""
from __future__ import annotations

from typing import FrozenSet, Iterable, Optional


class PurposeInvalid(ValueError):
    """Raised when a call's declared purpose is not on the allowlist.

    Wire behaviour: 422 Unprocessable Entity (matches donor semantics).
    """


# Governed positive allowlist — additive.
# Owner Order 2026-08-25 §5 · six purposes for W5:
ALLOWED_PURPOSES: FrozenSet[str] = frozenset({
    # Solva reasoning stages (Doc 04):
    "solva.frame_audit",
    "solva.candidate_generation",
    "solva.synthesis",
    # W6 CP4 · Grey Mirror groundwork (mechanism-side; not wired into
    # run_full_pipeline yet · ratification lands with the Grey Mirror
    # surface in W9):
    "solva.triangulation",
    "solva.tension_detection",
    "solva.probability_weighting",
    # ThinkLab direct-answer mode (Doc 05 §A5 · Direct mode):
    "thinklab.direct_answer",
    # Chat governed answer (Doc 05 · Chat surface):
    "chat.governed_answer",
    # BYO-LLM connect verification round-trip (Owner sharpening §2):
    "llm.connect_verify",
    # Estate Intelligence dossier (Owner ruling 2026-09-29 "2 — add any relevant meaningful datapoint … go autonomous":
    # LLM-written monetisation / cost-reduction dossier composed ONLY from census aggregates, no row content):
    "census.estate_intelligence_dossier",
    # Owner 2026-09-30 hybrid training laboratory; aggregate advisory reviews only.
    "training_lab.advisory_review",
    # Owner 2026-10-01 Train Models studio: per-run conversation grounded in the run's own record; bounded actions only.
    "training_lab.conversation",
    # Owner 2026-10-02 ("deterministic should not write or produce anything in the system, mostly manage or gate; use a recent model"):
    # the document studio's frontier writer authors every sentence under the Content Manager gate; code never writes prose.
    "doc_studio.author",
})


def validate_purpose(
    purpose: str,
    *,
    allow_list: Optional[Iterable[str]] = None,
) -> None:
    """Allow-list check. Raises PurposeInvalid on rejection.

    `allow_list` is an injection seam for tests; defaults to the
    module-level ALLOWED_PURPOSES.
    """
    if not isinstance(purpose, str):
        raise PurposeInvalid(
            f"purpose_missing_or_not_string — got {type(purpose).__name__}"
        )
    p = purpose.strip()
    if not p:
        raise PurposeInvalid("purpose_empty — empty purpose refused")

    catalogue = set(allow_list) if allow_list is not None else ALLOWED_PURPOSES
    if p in catalogue:
        return

    # Wildcard check (entries ending in `.*` match any sub-namespace).
    for entry in catalogue:
        if entry.endswith(".*"):
            stem = entry[:-2]
            if p == stem or p.startswith(stem + "."):
                return

    raise PurposeInvalid(
        f"purpose_not_allowlisted — {p!r} not in allow-list. "
        f"W5 allow-list: {sorted(catalogue)}. "
        "Adding a purpose requires an Owner ruling in STATE/DECISIONS.md."
    )


__all__ = ["ALLOWED_PURPOSES", "PurposeInvalid", "validate_purpose"]
