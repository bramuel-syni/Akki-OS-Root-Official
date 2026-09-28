"""services.doc0_attributes.triad — W-M2-SW9 · Doc-0 Attr-3 triad."""
from __future__ import annotations

from typing import Final, Tuple


class OperationUnmapped(KeyError):
    """Operation has no checkpoint mapping (BA-3.3 violation)."""


_PRINCIPALS: Final[Tuple[str, ...]] = (
    "internal.owner", "internal.operator", "internal.watch",
    "external.tenant", "external.witness", "external.regulator",
)

_ASSETS: Final[Tuple[str, ...]] = (
    "source", "model", "artifact", "receipt", "rules",
)

_OPERATIONS: Final[Tuple[str, ...]] = (
    "admit", "cross_boundary", "meter", "approve", "refuse",
    "record", "attest", "sever",
)

# BA-3.3 · each operation binds to exactly one checkpoint.
_OP_TO_CP: Final[dict[str, str]] = {
    "admit": "dap.admission",
    "cross_boundary": "dap.boundary",
    "meter": "dap.metering",
    "approve": "dap.approval",
    "refuse": "dap.refusal",
    "record": "ledger.write",
    "attest": "watch.witness",
    "sever": "watch.sever_signals",
}


def get_principals() -> Tuple[str, ...]:
    return _PRINCIPALS


def get_assets() -> Tuple[str, ...]:
    return _ASSETS


def get_operations() -> Tuple[str, ...]:
    return _OPERATIONS


def op_to_checkpoint(op: str) -> str:
    if op not in _OP_TO_CP:
        raise OperationUnmapped(
            f"operation {op!r} has no checkpoint mapping (BA-3.3)"
        )
    return _OP_TO_CP[op]


__all__ = [
    "OperationUnmapped",
    "get_principals", "get_assets", "get_operations",
    "op_to_checkpoint",
]
