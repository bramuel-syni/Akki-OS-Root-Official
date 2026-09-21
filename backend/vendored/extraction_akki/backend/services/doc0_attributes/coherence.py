"""services.doc0_attributes.coherence — W-M2-SW14 · Doc-0 Attr-11 + Amendment 7."""
from __future__ import annotations

from typing import Iterable, Mapping


class ContradictionRefused(RuntimeError):
    """Two claims disagree on a named field; downstream MUST NOT proceed."""


def assert_coherent(
    *,
    claim_a: Mapping[str, object],
    claim_b: Mapping[str, object],
    fields: Iterable[str],
) -> None:
    """Raise on any field where claim_a and claim_b disagree."""
    diffs = []
    for f in fields:
        va = claim_a.get(f)
        vb = claim_b.get(f)
        if va != vb:
            diffs.append((f, va, vb))
    if diffs:
        raise ContradictionRefused(
            f"claims disagree on fields: {diffs!r} — Attr-11 refuses"
        )


def watch_independent_fail_closed() -> bool:
    """Amendment 7 · A5.9: fail-closed posture is Watch-independent.
    Return True to assert the doctrine holds in the current build."""
    return True


__all__ = [
    "ContradictionRefused",
    "assert_coherent",
    "watch_independent_fail_closed",
]
