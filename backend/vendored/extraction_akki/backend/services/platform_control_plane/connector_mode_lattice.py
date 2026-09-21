"""services.platform_control_plane.connector_mode_lattice — CP-P3-CP3 · M9.

3-mode partial order per Akki OS Pilot Platform Reference v0.2 §5.3
verbatim (M-C-2 + M-C-3 + M-C-4):

    Modes: discovery (list/metadata/count/sample-headers; no content)
    · read (discovery + content extraction) · write (read + derived-
    output write within designated path).

    "Mode is enforced in the connector runtime, not in the calling app."
    "Raising a connector's mode requires approval by a data_steward
    or tenant_admin, is logged, and invalidates any task that
    referenced the connector until the task is re-approved."

Partial order: `discovery < read < write` (chain).

This CP provides:
- `CONNECTOR_MODES` tuple in rank order.
- `MODE_RANK` mapping.
- `assert_downgrade_only(*, from_mode, to_mode)` preventive-charter:
  - permits downgrade (rank(to) < rank(from)).
  - permits same-mode (rank(to) == rank(from)).
  - refuses upgrade (rank(to) > rank(from)) → the caller must invoke
    CP-P3-CP4 `mode_change_approval` to obtain a data_steward or
    tenant_admin approval + log-ref + dependent-task-invalidation set.

CONTRACT-MODELED items enabled (from §8):
- Item 14 · Real connector runtime enforcing mode — §5.3 M-C-3
  states mode is enforced in the connector runtime; this CP fixes
  the vocabulary + partial order + upgrade-refuses-without-approval
  invariant so the connector runtime binding is a bind-only change.

Standing-line proof:
- No `bytes` field · all str.
- No enforcement hard-gate · caller composes.
- Zero closed enums TYPE (OPEN str vocabulary constrained by tuple).
- Zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Dict, Tuple


CONNECTOR_MODE_LATTICE_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §5.3 "
    "verbatim: Modes: discovery (list/metadata/count/sample-headers; "
    "no content) · read (discovery + content extraction) · write "
    "(read + derived-output write within designated path). §5.3 "
    "M-C-3: Mode is enforced in the connector runtime, not in the "
    "calling app. §5.3 M-C-4: Raising a connector's mode requires "
    "approval by a data_steward or tenant_admin, is logged, and "
    "invalidates any task that referenced the connector until the "
    "task is re-approved."
)


# §5.3 verbatim vocabulary · OPEN str · listed in ascending rank order.
CONNECTOR_MODES: Tuple[str, ...] = (
    "discovery",
    "read",
    "write",
)


# Rank map: chain partial order.
MODE_RANK: Dict[str, int] = {
    "discovery": 0,
    "read": 1,
    "write": 2,
}


class ConnectorModeLatticeRefused(Exception):
    """Root refusal for connector-mode-lattice invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never mode values)."""


class UnknownModeRefused(ConnectorModeLatticeRefused):
    """Refused: mode is not in CONNECTOR_MODES (§5.3 3-mode
    vocabulary verbatim)."""


class UpgradeRequiresApprovalRefused(ConnectorModeLatticeRefused):
    """Refused: to_mode rank > from_mode rank (upgrade attempted).
    Upgrades require approval per §5.3 M-C-4 · composed at
    CP-P3-CP4 mode_change_approval."""


def mode_rank(*, mode: str) -> int:
    """Return the chain-rank of `mode` (0=discovery, 1=read, 2=write).
    Raises UnknownModeRefused if mode not in CONNECTOR_MODES."""
    if mode not in MODE_RANK:
        raise UnknownModeRefused(
            f"unknown-mode refused: mode not among "
            f"{len(CONNECTOR_MODES)} §5.3 mode values."
        )
    return MODE_RANK[mode]


def assert_downgrade_only(*, from_mode: str, to_mode: str) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order:
    1. from_mode or to_mode not in CONNECTOR_MODES → UnknownModeRefused.
    2. rank(to_mode) > rank(from_mode) → UpgradeRequiresApprovalRefused.

    Returns None on same-mode or downgrade."""
    fr = mode_rank(mode=from_mode)  # raises UnknownModeRefused on unknown
    tr = mode_rank(mode=to_mode)    # raises UnknownModeRefused on unknown
    if tr > fr:
        raise UpgradeRequiresApprovalRefused(
            f"upgrade-requires-approval refused: rank({tr}) > "
            f"rank({fr}) · §5.3 M-C-4 · compose CP-P3-CP4 "
            f"mode_change_approval."
        )
    return None


__all__ = [
    "CONNECTOR_MODE_LATTICE_ANCHOR",
    "CONNECTOR_MODES",
    "MODE_RANK",
    "ConnectorModeLatticeRefused",
    "UnknownModeRefused",
    "UpgradeRequiresApprovalRefused",
    "mode_rank",
    "assert_downgrade_only",
]
