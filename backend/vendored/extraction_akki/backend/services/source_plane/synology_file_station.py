"""services.source_plane.synology_file_station — W1b · CP3.

Interface-only implementation of SourceConnector for a Synology
FileStation. Runtime is gated by AKKI_SYNOLOGY_ALLOWED_RUNTIME=1;
without that env value every read method raises
NotConfiguredForRuntime. W1b never sets that env — the platform-side
implementation is complete at the interface boundary; the specific
NAS host + credentials are a JOB binding at mount time.

Zero I/O in construction. Zero I/O in any test path (the runtime
env is deliberately never enabled in the invariant suite).
"""
from __future__ import annotations

import os
from typing import IO, Tuple

from services.source_plane.connector import (
    ReadOnlyGuard, SourceHandle,
)


class NotConfiguredForRuntime(RuntimeError):
    """Raised when a read method is called without the runtime-gate
    env value in place. The interface is complete; the runtime binding
    lives at a downstream wave."""


class SynologyFileStationConnector(ReadOnlyGuard):
    """SourceConnector implementation for a Synology FileStation.

    Args:
        base_url: HTTP endpoint of the FileStation surface (opaque
            here; job binding at mount).
        auth_ref: OPAQUE string reference to a credential row in the
            estate_keys store — the credential value itself never
            passes through this constructor.
        timeout_seconds: per-request timeout.

    All read methods raise NotConfiguredForRuntime unless
    AKKI_SYNOLOGY_ALLOWED_RUNTIME == "1".
    """

    def __init__(
        self,
        base_url: str,
        auth_ref: str,
        timeout_seconds: int = 15,
    ) -> None:
        self.base_url = base_url
        self.auth_ref = auth_ref
        self.timeout_seconds = timeout_seconds

    def _guard_runtime(self) -> None:
        if os.environ.get("AKKI_SYNOLOGY_ALLOWED_RUNTIME") != "1":
            raise NotConfiguredForRuntime(
                "runtime binding is not configured — set "
                "AKKI_SYNOLOGY_ALLOWED_RUNTIME=1 at the mount wave to "
                "enable live reads (platform-side implementation is "
                "interface-only)"
            )

    def list_paths(self, prefix: str) -> Tuple[str, ...]:
        self._guard_runtime()
        # Not exercised in W1b — runtime path is a mount-wave concern.
        raise NotConfiguredForRuntime(
            "runtime read path not implemented in this wave"
        )

    def stat(self, path: str) -> SourceHandle:
        self._guard_runtime()
        raise NotConfiguredForRuntime(
            "runtime read path not implemented in this wave"
        )

    def open_read(self, path: str) -> IO[bytes]:
        self._guard_runtime()
        raise NotConfiguredForRuntime(
            "runtime read path not implemented in this wave"
        )

    def close(self) -> None:
        # close is always legal — cleanup must succeed regardless of
        # whether reads were ever admitted.
        return None


__all__ = ["SynologyFileStationConnector", "NotConfiguredForRuntime"]
