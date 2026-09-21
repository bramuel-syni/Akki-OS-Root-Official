"""services.cif.halt — M16-W5 · Doc-3 DET-1 CIF own-halt surface.

**Structural placement (DET-1 · Doc-3).**  The CIF halt state
is *own*.  This module has ZERO import of ``services.targeta``
at any scope (top-level or nested) — proved structurally by
``tests/invariants/test_m16_w5_seal_integration.py`` test 2.
A simulated Targeta halt MUST leave ``is_halted()`` unchanged;
this module never consults any external halt signal (test 6).

**Append-only journal (Canon 3 §9.3).**  The single writer is
``halt(reason)``; there is NO overwrite path.  Reads via
``get_halt_journal()`` return a fresh tuple (immutable
snapshot) — mutating the returned tuple cannot affect the
internal journal (test 3).

**Closed-schema discipline (SO §3.10-α).**  ``halt(reason)``
accepts ONLY a non-empty ``str`` reason.  Non-``str`` types
raise ``TypeError``; empty string raises ``ValueError``.
Rejected calls MUST NOT touch the journal (test 4).

**One-task-one-identity (Canon 8 §W11).**  This module is the
ONLY surface that mutates CIF halt state.  The public read
surface is ``is_halted()``; the public journal read is
``get_halt_journal()``.  ``_reset_halt_for_tests()`` is
test-scope only (mirrors sealed L-5 precedent).

Canon anchors verbatim:
- **DET-1** (Doc-3): CIF halt state is *own* · structural
  independence from Targeta (AST-enforced).
- **Canon 3 §9.3**: append-only writer discipline.
- **Canon 8 §W11**: one-task-one-identity · one writer, one
  read predicate, one journal read, no cross-service leak.
- **SO §3.8**: thin-kernel additive-only · new file in existing
  ``services/cif/`` package (established at M16-W2).
- **SO §3.10-α**: closed-schema discipline · ``isinstance`` +
  non-empty guards at the trust boundary.

Card citation: STATE/OBJECTIVES/M16.md MUST-DO 5 · EXIT-W5.
"""
from __future__ import annotations

from typing import Tuple


# ---------------------------------------------------------------------------
# CIF-owned halt journal · module-level append-only per Canon 3 §9.3.
# Single writer is `halt(reason)`; read via `get_halt_journal()` returns a
# fresh tuple (immutable snapshot); no overwrite path exists.
# ---------------------------------------------------------------------------
_HALT_JOURNAL: list = []


def is_halted() -> bool:
    """Return ``True`` iff at least one CIF-owned halt has been
    recorded in this process.

    Determinism: this is a plain length check over the CIF-owned
    journal — it does NOT consult ``services.targeta``, does NOT
    read the wall clock, does NOT touch any external state.  A
    simulated Targeta halt cannot flip this predicate (DET-1).
    """
    return len(_HALT_JOURNAL) > 0


def halt(reason: str) -> None:
    """Record a CIF-owned halt with the given non-empty ``reason``.

    Trust-boundary discipline:
    1. ``reason`` MUST be a ``str`` (``TypeError`` otherwise).
    2. ``reason`` MUST be non-empty (``ValueError`` otherwise).
    3. Rejected calls MUST NOT touch the journal.

    On success the reason is APPENDED to ``_HALT_JOURNAL`` (Canon
    3 §9.3 single-writer append-only discipline).  There is no
    overwrite path.
    """
    if not isinstance(reason, str):
        raise TypeError(
            f"halt(reason) requires str; got {type(reason).__name__}"
        )
    if reason == "":
        raise ValueError(
            "halt(reason) requires non-empty string · "
            "Canon 3 §9.3 halt reasons must be observable to future readers"
        )
    _HALT_JOURNAL.append(reason)


def get_halt_journal() -> Tuple[str, ...]:
    """Return an immutable snapshot (fresh tuple) of the CIF
    halt journal.

    Snapshot discipline: mutating the returned tuple cannot
    affect the internal journal; later ``halt`` calls do NOT
    retroactively change earlier snapshots (test 3).
    """
    return tuple(_HALT_JOURNAL)


def _reset_halt_for_tests() -> None:
    """Test-scope reset · mirrors sealed L-5 precedent
    (``services.capability_registry._reset_capabilities_for_tests``).
    NOT part of the public production surface — reserved for
    invariant test isolation only."""
    _HALT_JOURNAL.clear()


__all__ = [
    "is_halted",
    "halt",
    "get_halt_journal",
    "_reset_halt_for_tests",
]
