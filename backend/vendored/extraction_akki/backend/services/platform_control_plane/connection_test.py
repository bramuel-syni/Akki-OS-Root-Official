"""services.platform_control_plane.connection_test — CP-P3-CP5 · M9.

Preventive-charter connection-test outcome carrier per Akki OS Pilot
Platform Reference v0.2 §5.4 M-C-5 verbatim:

    Every connector passes a connection test before it can be
    attached to a task. The test verifies reachability,
    authentication and scope resolution. It does not read content.

Carrier shape (7 fields · pre-attach admission record · not in §10):
- id · connector_id
- reachability_ref · authentication_ref · scope_resolution_ref
  (three evidence refs · empty = check not performed)
- content_read_attempted (bool · MUST be False per M-C-5 "does not
  read content")
- tested_at

Refusals (safety-first ordering — content-read fires FIRST):
- content_read_attempted True → ContentReadDuringTestRefused
- reachability_ref empty → MissingReachabilityCheckRefused
- authentication_ref empty → MissingAuthenticationCheckRefused
- scope_resolution_ref empty → MissingScopeResolutionRefused

Composes with CP-P3-CP2 ConnectorEntity: caller passes a
ConnectionTestOutcome bound to a connector_id · this CP admits or
refuses the outcome record only · attaching to a task is a downstream
P4 CP.

Standing-line proof:
- 6 str + 1 bool · 7 fields exact-order.
- No enforcement hard-gate · caller composes.
- Zero closed enums · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


CONNECTION_TEST_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §5.4 "
    "M-C-5 verbatim: Every connector passes a connection test before "
    "it can be attached to a task. The test verifies reachability, "
    "authentication and scope resolution. It does not read content."
)


@dataclasses.dataclass(frozen=True)
class ConnectionTestOutcome:
    """Frozen carrier for a connector connection-test outcome record.

    Exact-order 7 fields (6 str + 1 bool):
    - id · outcome record id.
    - connector_id · id of the connector being tested (composes with
      CP-P3-CP2 ConnectorEntity).
    - reachability_ref · evidence ref that reachability was verified
      (§5.4 M-C-5 "verifies reachability") · empty = check missing.
    - authentication_ref · evidence ref that authentication was
      verified · empty = check missing.
    - scope_resolution_ref · evidence ref that scope resolution was
      performed · empty = check missing.
    - content_read_attempted · bool · MUST be False (§5.4 M-C-5 "does
      not read content"); True is refused.
    - tested_at · ISO-8601 UTC 'Z' str.
    """
    id: str
    connector_id: str
    reachability_ref: str
    authentication_ref: str
    scope_resolution_ref: str
    content_read_attempted: bool
    tested_at: str


CONNECTION_TEST_OUTCOME_FIELDS: Tuple[str, ...] = (
    "id",
    "connector_id",
    "reachability_ref",
    "authentication_ref",
    "scope_resolution_ref",
    "content_read_attempted",
    "tested_at",
)


class ConnectionTestRefused(Exception):
    """Root refusal for connection-test-outcome invariants."""


class ContentReadDuringTestRefused(ConnectionTestRefused):
    """Refused: content_read_attempted is True · §5.4 M-C-5 forbids
    content read during connection test."""


class MissingReachabilityCheckRefused(ConnectionTestRefused):
    """Refused: reachability_ref empty · §5.4 M-C-5 requires
    reachability verification."""


class MissingAuthenticationCheckRefused(ConnectionTestRefused):
    """Refused: authentication_ref empty · §5.4 M-C-5 requires
    authentication verification."""


class MissingScopeResolutionRefused(ConnectionTestRefused):
    """Refused: scope_resolution_ref empty · §5.4 M-C-5 requires
    scope-resolution verification."""


def assert_connection_test_valid(
    *, outcome: ConnectionTestOutcome,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (safety-first fail-fast):
    1. content_read_attempted True → ContentReadDuringTestRefused.
    2. reachability_ref empty → MissingReachabilityCheckRefused.
    3. authentication_ref empty → MissingAuthenticationCheckRefused.
    4. scope_resolution_ref empty → MissingScopeResolutionRefused.

    Returns None on admit."""
    if outcome.content_read_attempted:
        raise ContentReadDuringTestRefused(
            f"content-read-during-test refused: "
            f"content_read_attempted flag set at positional index "
            f"{CONNECTION_TEST_OUTCOME_FIELDS.index('content_read_attempted')} "
            f"· §5.4 M-C-5 forbids content read during connection test."
        )
    if outcome.reachability_ref == "":
        raise MissingReachabilityCheckRefused(
            f"missing-reachability-check refused: reachability_ref at "
            f"positional index "
            f"{CONNECTION_TEST_OUTCOME_FIELDS.index('reachability_ref')} "
            f"empty · §5.4 M-C-5 requires reachability verification."
        )
    if outcome.authentication_ref == "":
        raise MissingAuthenticationCheckRefused(
            f"missing-authentication-check refused: authentication_ref "
            f"at positional index "
            f"{CONNECTION_TEST_OUTCOME_FIELDS.index('authentication_ref')} "
            f"empty · §5.4 M-C-5 requires authentication verification."
        )
    if outcome.scope_resolution_ref == "":
        raise MissingScopeResolutionRefused(
            f"missing-scope-resolution refused: scope_resolution_ref "
            f"at positional index "
            f"{CONNECTION_TEST_OUTCOME_FIELDS.index('scope_resolution_ref')} "
            f"empty · §5.4 M-C-5 requires scope-resolution verification."
        )
    return None


__all__ = [
    "CONNECTION_TEST_ANCHOR",
    "CONNECTION_TEST_OUTCOME_FIELDS",
    "ConnectionTestOutcome",
    "ConnectionTestRefused",
    "ContentReadDuringTestRefused",
    "MissingReachabilityCheckRefused",
    "MissingAuthenticationCheckRefused",
    "MissingScopeResolutionRefused",
    "assert_connection_test_valid",
]
