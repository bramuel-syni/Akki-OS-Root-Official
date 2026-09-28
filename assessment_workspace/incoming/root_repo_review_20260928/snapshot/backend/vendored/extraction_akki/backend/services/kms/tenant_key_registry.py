"""Per-tenant master key registry · M13-W2 · §6.4 pre-ruling 4 verbatim.

**Structural role (Canon 8 §W11 one-task-one-identity):** this module
mints and lists per-tenant master keys. It does NOT wrap data — that
responsibility belongs to `services.kms.envelope`. AST bans enforce
the boundary at
`tests/invariants/test_m13_w2_kms_envelope_and_rotation.py::
test_ast_registry_does_not_wrap_data`.

**Append-only per Canon 3 §9.3:** minting a fresh master key for a
tenant never overwrites an existing record — it appends a new one and
preserves prior records verbatim as historical evidence.

Canon anchors:
- Canon 8 §W10 (watcher-watched-from-outside): key material is scoped
  to the KMS trust boundary; no caller receives raw master-key bytes.
- Canon 3 §9.3 (append-only): registry is append-only.
"""
from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TenantMasterKeyRecord:
    """One tenant master-key record. Key material is scope-bound to the
    KMS trust boundary — callers see only tenant_id + key_id + version
    + active_at_iso, never the raw bytes."""
    tenant_id: str
    key_id: str
    key_version: int
    active_at_iso: str


# In-memory append-only registry keyed by tenant_id.
# Production wiring would back this with a KMS provider; the shape is
# preserved so the mechanism is testable without a live KMS in CI.
_REGISTRY: dict[str, list[TenantMasterKeyRecord]] = {}

# Raw master-key bytes are held in a separate dict scoped to this
# module. `envelope.py` reaches them ONLY through `_get_key_material`
# to preserve Canon 8 §W10 (never routed outside KMS trust boundary).
_KEY_MATERIAL: dict[str, bytes] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def mint_tenant_master_key(tenant_id: str) -> TenantMasterKeyRecord:
    """Mint a fresh 32-byte master key for `tenant_id` and append the
    record to the registry. Returns the new `TenantMasterKeyRecord`.
    Does NOT wrap any data."""
    history = _REGISTRY.setdefault(tenant_id, [])
    next_version = len(history) + 1
    # 64-hex secure random id + 32-byte random key material.
    key_id = f"km_{tenant_id}_{next_version}_{secrets.token_hex(8)}"
    key_material = secrets.token_bytes(32)
    _KEY_MATERIAL[key_id] = key_material
    record = TenantMasterKeyRecord(
        tenant_id=tenant_id,
        key_id=key_id,
        key_version=next_version,
        active_at_iso=_now_iso(),
    )
    history.append(record)
    return record


def get_active_key(tenant_id: str) -> TenantMasterKeyRecord:
    """Return the currently-active master key record for `tenant_id`
    (the most recent one). Raises KeyError if the tenant has never
    minted a master key."""
    history = _REGISTRY.get(tenant_id)
    if not history:
        raise KeyError(
            f"tenant {tenant_id!r} has no master key on record; call "
            f"mint_tenant_master_key(tenant_id) first"
        )
    return history[-1]


def list_key_history(tenant_id: str) -> tuple[TenantMasterKeyRecord, ...]:
    """Return the full append-only key history for `tenant_id` as an
    immutable tuple in insertion order."""
    return tuple(_REGISTRY.get(tenant_id, []))


def _get_key_material(key_id: str) -> bytes:
    """KMS-boundary-scoped accessor for raw key bytes. Called from
    `services.kms.envelope` alone. Not exported at module surface."""
    return _KEY_MATERIAL[key_id]
