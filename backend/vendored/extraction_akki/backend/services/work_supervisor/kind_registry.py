"""services.work_supervisor.kind_registry — case-agnostic job-kind registry.

Contract:
  register_kind(name: str) -> None
  is_registered(name: str) -> bool
  list_kinds() -> tuple[str, ...]        # sorted, immutable snapshot
  KindNotRegistered(ValueError)          # exception for unregistered kinds
  _reset_kinds_for_tests() -> None       # test-only determinism

Platform-side seed: exactly ONE sentinel kind at module-import time:
    "platform.generic"
Downstream waves register their own case-specific kinds (e.g. an audio-
harvest Part-B wave would call `register_kind("case.b.audio.transcribe")`).
No audio-case tokens are hard-coded in this module — the registry is
case-agnostic by construction.

Standing law: STATE/STANDING_ORDERS.md §3 BUILD DISCIPLINE (tests-first,
double-green, thin-kernel). See grounding brief for wave-honest limits.
"""
from __future__ import annotations

from typing import Tuple


class KindNotRegistered(ValueError):
    """Raised when a caller names a job_kind that is not in the registry."""


# Process-scope registry. Wave-honest limit E-4: durable on-disk
# audit trail of registrations is a later refinement; W1 exposes the
# surface and tests use `_reset_kinds_for_tests` for determinism.
_REGISTERED_KINDS: set[str] = set()

# The sole platform-side seed. Its purpose is to give W1's own tests a
# valid kind to reference without registering case-specific kinds.
PLATFORM_SEED_KIND = "platform.generic"


def _seed_platform_kinds() -> None:
    """Idempotent installation of the platform-side seed."""
    _REGISTERED_KINDS.add(PLATFORM_SEED_KIND)


def register_kind(name: str) -> None:
    """Register a new job-kind. Idempotent — registering the same name
    twice is a no-op (not an error)."""
    if not isinstance(name, str):
        raise TypeError(
            f"register_kind requires a str name, got {type(name).__name__}"
        )
    if not name.strip():
        raise ValueError(
            "register_kind refuses empty / whitespace-only name — "
            "a job_kind must name a real capability"
        )
    _REGISTERED_KINDS.add(name)


def is_registered(name: str) -> bool:
    """Return True iff `name` has been registered as a job-kind."""
    return name in _REGISTERED_KINDS


def list_kinds() -> Tuple[str, ...]:
    """Return an immutable, sorted snapshot of currently registered
    kinds. Sorted so hashes/diffs are deterministic; tuple so callers
    cannot mutate the registry via the return value."""
    return tuple(sorted(_REGISTERED_KINDS))


def _reset_kinds_for_tests() -> None:
    """Wipe the registry and re-seed the platform sentinel. Test-only
    determinism helper — the leading underscore signals it is not a
    stable public API."""
    _REGISTERED_KINDS.clear()
    _seed_platform_kinds()


# Install the platform seed at import time.
_seed_platform_kinds()


__all__ = [
    "PLATFORM_SEED_KIND",
    "KindNotRegistered",
    "register_kind",
    "is_registered",
    "list_kinds",
    "_reset_kinds_for_tests",
]
