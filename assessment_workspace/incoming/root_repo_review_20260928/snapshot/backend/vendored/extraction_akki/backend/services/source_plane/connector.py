"""services.source_plane.connector — W1b · CP2 · SourceConnector Protocol.

Contract:
  SourceConnector (typing.Protocol):
      list_paths(prefix: str) -> tuple[str, ...]
      stat(path: str) -> SourceHandle
      open_read(path: str) -> IO[bytes]
      close() -> None

  SourceHandle (dataclass, frozen):
      kind: str
      uri: str
      opened_at_utc: str
      size_bytes: int | None

  ReadOnlyGuard — mixin. Intercepts attribute access; refuses any
      method whose name matches a WRITE_METHOD_PATTERNS entry.
      Refusal raises SourceConnectorWriteRefused.

  SourceConnectorWriteRefused(RuntimeError)

Zero-influence: no I/O in this module. Concrete implementations
live in sibling modules under services.source_plane and MAY do I/O;
the Protocol here has NO credential surface (creds live on concrete
impls, bound at job-mount time).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import IO, Optional, Protocol, Tuple, runtime_checkable


class SourceConnectorWriteRefused(RuntimeError):
    """Raised by ReadOnlyGuard when a write-shaped method is called."""


@dataclass(frozen=True)
class SourceHandle:
    kind: str
    uri: str
    opened_at_utc: str
    size_bytes: Optional[int] = None


@runtime_checkable
class SourceConnector(Protocol):
    """Read-only view into a source estate. Concrete impls implement
    these four methods and MUST NOT surface write operations."""

    def list_paths(self, prefix: str) -> Tuple[str, ...]:
        ...

    def stat(self, path: str) -> SourceHandle:
        ...

    def open_read(self, path: str) -> IO[bytes]:
        ...

    def close(self) -> None:
        ...


# Closed pattern list — extending requires a code change (this is
# deliberate: it's the whitelist boundary of "what counts as a write").
WRITE_METHOD_PATTERNS: Tuple[str, ...] = (
    "put", "write", "delete", "mkdir", "rename", "mv", "rm",
    "make_dir", "move", "remove", "unlink",
    "upload", "post", "create",
)


def is_read_only_method_name(name: str) -> bool:
    """Return True iff `name` does NOT match any write pattern.

    A method matches a pattern if the pattern appears as either the
    whole name OR a prefix segment separated by an underscore (e.g.
    `put_file`, `write_bytes`, `delete_folder`). This intentionally
    admits read-shaped names that happen to contain a write substring
    as an internal fragment (rare) — a false-positive on such names
    would be a legitimate concern for review.
    """
    if not isinstance(name, str) or not name:
        return False
    lowered = name.lower()
    for pat in WRITE_METHOD_PATTERNS:
        if lowered == pat:
            return False
        if lowered.startswith(pat + "_"):
            return False
        # Also refuse names that end with the pattern (e.g. `raw_write`).
        if lowered.endswith("_" + pat):
            return False
    return True


class ReadOnlyGuard:
    """Mixin: refuse any method call whose name is not read-only.

    Subclass ordering: place `ReadOnlyGuard` FIRST in the MRO so the
    guard's __getattribute__ wins.

    Example:
        class MyConnector(ReadOnlyGuard):
            def list_paths(self, prefix): ...
            def stat(self, path): ...
    """

    def __getattribute__(self, name: str):
        # Avoid guarding dunder/private access — those are runtime
        # machinery (repr, class, etc.) and never target the connector
        # surface. The guard only trips on plain public method names.
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        # Read `is_read_only_method_name` via module import (avoids
        # recursion through self.__getattribute__ for method lookup).
        if not is_read_only_method_name(name):
            raise SourceConnectorWriteRefused(
                f"method {name!r} refused by ReadOnlyGuard — a "
                "SourceConnector implementation must not surface "
                "write operations"
            )
        return object.__getattribute__(self, name)


__all__ = [
    "SourceConnector",
    "SourceHandle",
    "ReadOnlyGuard",
    "SourceConnectorWriteRefused",
    "is_read_only_method_name",
    "WRITE_METHOD_PATTERNS",
]
