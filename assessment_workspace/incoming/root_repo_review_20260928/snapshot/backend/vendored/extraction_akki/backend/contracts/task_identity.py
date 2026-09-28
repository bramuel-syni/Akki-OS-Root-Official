"""Task Identity Register (thin kernel) — Canon 9 §5, Build Order 01 §4.A0.

Thin scope: only the task classes the live path touches. Full scope
completes in Track B per WS-BUILD-TASK-IDENTITY-REGISTER.

Canon 8 §4.11 W11: one task, one identity. Every runtime task carries
exactly one registered task identity. Dual-hat tasks refuse.
"""
from __future__ import annotations

from typing import Dict, Literal, NamedTuple


# Authority axis — Canon 8 §4.12 W12 (peer, not subordinate).
Authority = Literal["governance", "watch", "infrastructure"]


class TaskIdentity(NamedTuple):
    task_id: str        # dotted namespace, e.g. "custody.admit.declaration_check"
    authority: Authority
    description: str    # one-sentence purpose


# THIN KERNEL — Build Order 01 §4.A0.
# Nine task identities cover the A0-A2 live path.
THIN_TASK_REGISTER: Dict[str, TaskIdentity] = {
    # A0 — thin register kernel operations
    "matrix.entry.per_class": TaskIdentity(
        task_id="matrix.entry.per_class",
        authority="governance",
        description="Governance writes a record-matrix entry for a class.",
    ),
    "parity_seat.contract_freeze.per_shape": TaskIdentity(
        task_id="parity_seat.contract_freeze.per_shape",
        authority="governance",
        description="Governance freezes a contract shape into the parity seat.",
    ),
    # A1 — declaration
    "declaration.capture": TaskIdentity(
        task_id="declaration.capture",
        authority="governance",
        description="Declaration seat captures an actor declaration.",
    ),
    "declaration.check.per_admit": TaskIdentity(
        task_id="declaration.check.per_admit",
        authority="governance",
        description="Admit checks the in-force declaration for an actor.",
    ),
    "custody.admit.declaration_join": TaskIdentity(
        task_id="custody.admit.declaration_join",
        authority="governance",
        description="Custody joins declaration verdict into admit's fail-closed chain.",
    ),
    # A2 — ingestion
    "ingestion.admit.per_source": TaskIdentity(
        task_id="ingestion.admit.per_source",
        authority="governance",
        description="Admit for an ingestion run against a declared source.",
    ),
    "ledger.writer.matrix_governed": TaskIdentity(
        task_id="ledger.writer.matrix_governed",
        authority="governance",
        description="Northena writer role governed by the record matrix.",
    ),
    # A3 — compute (infrastructure)
    "compute.training.per_run": TaskIdentity(
        task_id="compute.training.per_run",
        authority="infrastructure",
        description="Infrastructure runs a GPU training job under declared basis.",
    ),
    "compute.transfer.per_batch": TaskIdentity(
        task_id="compute.transfer.per_batch",
        authority="infrastructure",
        description="Infrastructure transfers an ingestion batch to HSS.",
    ),
    "compute.acceptance.per_check": TaskIdentity(
        task_id="compute.acceptance.per_check",
        authority="infrastructure",
        description="Infrastructure runs phase0/acceptance.sh remotely and returns per-check results.",
    ),
    # WS-BUILD-CONNECT-GPU — governed credential-entry surface (Phase-0 gate)
    "connect.gpu.submit.per_host": TaskIdentity(
        task_id="connect.gpu.submit.per_host",
        authority="governance",
        description="Governance intake of a VM connection request; fires declaration + hardening + acceptance.",
    ),
}


def get_identity(task_id: str) -> TaskIdentity:
    """Return the registered TaskIdentity or raise KeyError."""
    if task_id not in THIN_TASK_REGISTER:
        raise KeyError(f"task_id {task_id!r} not registered in thin kernel")
    return THIN_TASK_REGISTER[task_id]


def is_registered(task_id: str) -> bool:
    return task_id in THIN_TASK_REGISTER


def thin_task_ids() -> list[str]:
    return list(THIN_TASK_REGISTER.keys())
