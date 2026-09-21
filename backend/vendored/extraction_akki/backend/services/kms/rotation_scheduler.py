"""90-day rotation scheduler · M13-W2 · §6.4 pre-ruling 4 verbatim.

**Structural role (Canon 8 §W11 one-task-one-identity):** this module
schedules and executes 90-day rotations. It mints new master keys via
`services.kms.tenant_key_registry.mint_tenant_master_key` and appends
a `KeyLineageRecord` binding prev_key_id → new_key_id to the append-
only lineage. It does NOT decrypt data — that responsibility belongs
to `services.kms.envelope`. AST ban enforces the boundary at
`tests/invariants/test_m13_w2_kms_envelope_and_rotation.py::
test_ast_rotation_does_not_decrypt`.

Cadence: 90 days per §6.4 pre-ruling 4 verbatim (R-4).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from services.kms.tenant_key_registry import (
    get_active_key,
    mint_tenant_master_key,
)


#: §6.4 pre-ruling 4 verbatim: "KMS: envelope encryption, per-tenant
#: keys, 90-day rotation (R-4)."
ROTATION_CADENCE_DAYS: int = 90


@dataclass(frozen=True)
class KeyLineageRecord:
    """A rotation event · binds prev_key_id → new_key_id append-only."""
    tenant_id: str
    prev_key_id: str
    new_key_id: str
    rotated_at_iso: str
    cadence_reason: str


# Append-only in-memory lineage keyed by tenant_id.
_LINEAGE: dict[str, list[KeyLineageRecord]] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def rotation_due(tenant_id: str, last_rotated_at: datetime) -> bool:
    """Return True if rotation is due for `tenant_id` given the
    provided `last_rotated_at` timestamp (must be timezone-aware).

    Cadence is `ROTATION_CADENCE_DAYS` (90 days per §6.4)."""
    age = _now() - last_rotated_at
    return age >= timedelta(days=ROTATION_CADENCE_DAYS)


def execute_rotation(tenant_id: str, reason: str) -> KeyLineageRecord:
    """Mint a new master key for `tenant_id` via the registry, and
    append a `KeyLineageRecord` capturing the prev → new transition.

    Does NOT decrypt any data. Returns the new lineage record."""
    prev = get_active_key(tenant_id)
    new = mint_tenant_master_key(tenant_id)
    record = KeyLineageRecord(
        tenant_id=tenant_id,
        prev_key_id=prev.key_id,
        new_key_id=new.key_id,
        rotated_at_iso=_now().isoformat(),
        cadence_reason=reason,
    )
    _LINEAGE.setdefault(tenant_id, []).append(record)
    return record


def list_key_lineage(tenant_id: str) -> tuple[KeyLineageRecord, ...]:
    """Return the full append-only key lineage for `tenant_id`."""
    return tuple(_LINEAGE.get(tenant_id, []))
