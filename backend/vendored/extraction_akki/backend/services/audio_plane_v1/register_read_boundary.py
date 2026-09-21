"""M6 · Audio-Plane v1.0 · CP-M6-3-4 · Register read-path scope enforcement.

Wraps `RegisterWriteBoundary` (CP-M6-3-3) to enforce the SAME conjunctive
four-conditions check on the read path per §6.4 P102 verbatim.

Discharge anchor (verbatim on single un-wrapped line):

- Audio-Plane §6.4 P102 (V67 · idiolect rule · conjunctive-four-conditions):
      "Habitual fillers, characteristic phrasings, and idiosyncratically pronounced words are learned but individuating. They fail condition 2 or 3 and are excluded. 'Learned' alone is never sufficient; the four conditions are conjunctive."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Synthetic fixtures only in tests.
  - Case-agnostic; no executive-domain tokens.

Reuse-not-refactor discipline:
  - CP-M6-3-3's `RegisterWriteBoundary.write` already codifies §6.1 P092
    + §6.2 conds 1–4 + §6.4 P102.  This module wraps that method
    without modifying it — single source of truth for the conjunctive
    check across write + read paths.

Contract:

    RegisterReadBoundary(*, write_boundary: Optional[RegisterWriteBoundary] = None)

    RegisterReadBoundary.read_or_refuse(*, entries: Sequence[CharacterEntry])
        -> Tuple[CharacterEntry, ...]
      · Returns a tuple of all entries iff every entry passes the
        conjunctive check.  On first violation, raises
        `ReadScopeViolationError`.

    RegisterReadBoundary.read_scope_filter(*, entries: Sequence[CharacterEntry])
        -> Tuple[CharacterEntry, ...]
      · Returns only the subset of entries that pass the conjunctive
        check.  Non-passing entries are dropped silently.

Refusals:
    ReadScopeViolationError  (subclass of LeakageRefusalError · same
                              family as CP-M6-3-3 write-path refusals)
"""
from __future__ import annotations

from typing import Optional, Sequence, Tuple

from services.audio_plane_v1.character_register import CharacterEntry
from services.audio_plane_v1.leakage_path_harness import LeakageRefusalError
from services.audio_plane_v1.register_write_boundary import (
    RegisterWriteBoundary,
)


class ReadScopeViolationError(LeakageRefusalError):
    """§6.4 verbatim: 'the four conditions are conjunctive'.  Raised
    when a read attempt would return a `CharacterEntry` that violates
    one or more of §6.1 P092 (organic) + §6.2 conds 1–4 + §6.4 P102
    (idiolect).

    Subclasses `LeakageRefusalError` so downstream reporting classifies
    it as a protective refusal (same family as CP-M6-3-3 write-path
    refusals)."""


class RegisterReadBoundary:
    """Register read-path scope enforcement per §6.4 P102.

    Wraps a `RegisterWriteBoundary` and reuses its refusal logic to
    enforce the SAME conjunctive-four-conditions check on the read
    path.  Two access modes:
      - `read_or_refuse` — return all entries if all pass; raise on
        first violation.
      - `read_scope_filter` — return only the subset of entries that
        pass the conjunctive check.
    """

    def __init__(
        self,
        *,
        write_boundary: Optional[RegisterWriteBoundary] = None,
    ) -> None:
        self._write_boundary = write_boundary or RegisterWriteBoundary()

    def _entry_passes(self, entry: CharacterEntry) -> Optional[LeakageRefusalError]:
        """Run the CP-M6-3-3 conjunctive check on an entry.

        Returns None if the entry passes; returns the underlying
        `LeakageRefusalError` (unraised) if it fails.  This lets both
        `read_or_refuse` and `read_scope_filter` share the same
        source-of-truth check without silent swallow.
        """
        try:
            self._write_boundary.write(entry)
        except LeakageRefusalError as exc:
            return exc
        return None

    def read_or_refuse(
        self,
        *,
        entries: Sequence[CharacterEntry],
    ) -> Tuple[CharacterEntry, ...]:
        """Return all entries iff every entry passes the conjunctive
        check.  On first violation, raise `ReadScopeViolationError`
        naming the violating entry's attribute_name."""
        coerced = tuple(entries)
        for i, entry in enumerate(coerced):
            failure = self._entry_passes(entry)
            if failure is not None:
                raise ReadScopeViolationError(
                    f"§6.4 conjunctive-four-conditions violation at "
                    f"entries[{i}] ({entry.attribute_name!r}): {failure}"
                ) from failure
        return coerced

    def read_scope_filter(
        self,
        *,
        entries: Sequence[CharacterEntry],
    ) -> Tuple[CharacterEntry, ...]:
        """Return only the subset of entries that pass the conjunctive
        four-conditions check.  Non-passing entries are dropped silently.
        """
        return tuple(
            entry
            for entry in entries
            if self._entry_passes(entry) is None
        )
