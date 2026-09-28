"""services/mtafiti/asset_registry_writer.py — W-REGISTRY-EXTENSION-G3.

Owner label 2026-09-13 · closes Doc-0 G-3 mechanical half.  The single
canonical writer for the extended asset-class registry (Canon-9 §3
single-writer discipline for census/registry records).

Canon anchors (first-hand):
  * Canon-9 §3   — single writer; second writer is a defect on sight.
  * Canon-3 §9.3 — writer exposes append and nothing else; no update or
                   delete path within the retention window.
  * Canon-3 §22  — governance-value four-class taxonomy binder.
  * Doc-0 TA-3.1 — finite named class list producible on request.

R-C2 marker (this module):
  WriteReceipt.au_3b_defensible defaults to False until Doc-0 G-8
  (Security_Promise_Set_Amendments.docx Amendment 3) closes.  Test
  asserts silent flip is forbidden.
"""
from __future__ import annotations

import hashlib
import threading
from typing import Dict, List, Tuple

from pydantic import BaseModel, ConfigDict, Field

from contracts.asset_registry import (
    ASSET_REGISTRY_COLLECTION,
    AssetClass,
    AssetRegistryRecord,
    CustodyClass,
    GovernanceValueClass,
)


# --- WriteReceipt (R-C2 carrier) -------------------------------------
class WriteReceipt(BaseModel):
    """Idempotent write receipt.  R-C2: au_3b_defensible=False until a
    reliable-time control closes Doc-0 G-8."""

    model_config = ConfigDict(extra="forbid")

    receipt_id: str = Field(..., description="Deterministic id from record content (idempotency).")
    collection: str = Field(..., description="Canon-9 §3 record class.")
    au_3b_defensible: bool = Field(
        default=False,
        description=(
            "R-C2: timestamp not defensible under AU-3(b) until "
            "Doc-0 G-8 closes.  Silent flip forbidden by invariant."
        ),
    )


# --- in-memory registry (thin-kernel) --------------------------------
# NOT a persistence layer.  The registry write path this wave lands is
# the deterministic-idempotent envelope; downstream persistence is a
# later wave's concern.  Keys by asset_ref → last-written record.
_REGISTRY: Dict[str, AssetRegistryRecord] = {}
_WRITE_LOCK = threading.RLock()
_PERSISTENCE = None


def configure_persistence(collection):
    """Bind the existing canonical writer to its durable collection at assembly."""
    global _PERSISTENCE
    _PERSISTENCE = collection
    collection.create_index('asset_ref', unique=True)


def persistence_enabled():
    return _PERSISTENCE is not None


def append_census_evidence(asset_ref, tenant_id, evidence):
    """Additive content-addressed evidence through the same single Registry writer."""
    import json
    from pymongo.errors import DuplicateKeyError
    if _PERSISTENCE is None:
        raise RuntimeError('Canonical Registry persistence is not configured')
    digest=hashlib.sha256(json.dumps(evidence,sort_keys=True,default=str).encode()).hexdigest()
    document={'asset_ref':asset_ref,'tenant_id':tenant_id,'evidence_sha256':digest,'census_evidence':evidence}
    try:
        _PERSISTENCE.update_one({'asset_ref':asset_ref,'evidence_sha256':digest},{'$setOnInsert':document},upsert=True)
    except DuplicateKeyError as exc:
        raise ValueError('Conflicting evidence cannot replace an accepted Registry record') from exc
    return digest


def _compute_receipt_id(record: AssetRegistryRecord) -> str:
    """Deterministic sha256-based receipt id.  Same record ⇒ same id
    ⇒ idempotency."""
    payload = record.model_dump_json().encode("utf-8")
    return "receipt_" + hashlib.sha256(payload).hexdigest()[:24]


def write_asset_record(record: AssetRegistryRecord) -> WriteReceipt:
    """Canonical write path for the extended asset registry.

    Append-only (Canon-3 §9.3).  Idempotent by record content.  R-C2
    carrier: receipt.au_3b_defensible defaults to False.
    """
    with _WRITE_LOCK:
        previous=_REGISTRY.get(record.asset_ref)
        if previous and previous!=record:
            raise ValueError('Conflicting content cannot overwrite an existing asset_ref')
        if _PERSISTENCE is not None:
            from pymongo.errors import DuplicateKeyError
            payload=record.model_dump(mode='json')
            digest=_compute_receipt_id(record)
            try:
                _PERSISTENCE.update_one({'asset_ref':record.asset_ref,'record_hash':digest},
                    {'$setOnInsert':{'asset_ref':record.asset_ref,'tenant_id':record.named_owner.owner_id,
                                     'record_hash':digest,'record':payload}},upsert=True)
            except DuplicateKeyError as exc:
                raise ValueError('Conflicting content cannot overwrite a persisted asset') from exc
        _REGISTRY[record.asset_ref] = record
    return WriteReceipt(
        receipt_id=_compute_receipt_id(record),
        collection=ASSET_REGISTRY_COLLECTION,
        au_3b_defensible=False,
    )


def find_by_custody_class(custody_class: CustodyClass) -> List[AssetRegistryRecord]:
    """Doc-0 BR-1.4 queryable custody class.  Typed parameter — free-
    text is refused at the language layer."""
    if _PERSISTENCE is not None:
        return [AssetRegistryRecord.model_validate(d['record']) for d in
                _PERSISTENCE.find({'record.custody_class':custody_class.value},{'_id':0,'record':1})]
    return [r for r in _REGISTRY.values() if r.custody_class is custody_class]


def list_registered_classes() -> Dict[str, Tuple[str, ...]]:
    """Doc-0 TA-3.1 finite named list of principal classes, asset
    classes, operations, and custody classes."""
    return {
        "principals": (
            # Canon-6 §2 role register + Doc-0 BA-3.1 principal classes
            "instance_owner",
            "compliance_owner",
            "operator",
            "watch_officer",
            "business_user",
            "commissioner",
            "technical_lead",
            "integrating_engineer",
            "external_party",
        ),
        "assets": tuple(m.value for m in AssetClass),
        "operations": (
            # DAP-Spec §4 six crossing profiles + registry ops
            "browse_estate",
            "connect_workspace",
            "processed_intelligence",
            "fine_tune_model",
            "develop_skills",
            "download_raw_data",
            "register_asset",
            "query_custody_class",
        ),
        "custody_classes": tuple(m.value for m in CustodyClass),
    }


# --- Canon-3 §22 governance-value taxonomy binder --------------------
_GOVERNANCE_TAXONOMY: Dict[str, GovernanceValueClass] = {
    # This wave's new named functions and constants are each classed.
    "asset_registry_writer": GovernanceValueClass.ENGINE_SETTINGS,
    "find_by_custody_class": GovernanceValueClass.ENGINE_SETTINGS,
    "list_registered_classes": GovernanceValueClass.REGISTRIES,
    "classify_governance_value": GovernanceValueClass.ENGINE_SETTINGS,
    "ASSET_REGISTRY_COLLECTION": GovernanceValueClass.REGISTRIES,
    "AssetClass": GovernanceValueClass.REGISTRIES,
    "CustodyClass": GovernanceValueClass.REGISTRIES,
    "GovernanceValueClass": GovernanceValueClass.REGISTRIES,
}


def classify_governance_value(name: str) -> GovernanceValueClass:
    """Canon-3 §22: every governed value is exactly one class.
    Unknown value is refused, not defaulted (§22: 'change of nature,
    not opinion')."""
    if name not in _GOVERNANCE_TAXONOMY:
        raise KeyError(
            f"Governance-value classification refused for {name!r}: "
            f"Canon-3 §22 forbids defaulting a value the taxonomy does "
            f"not know.  Register it before use."
        )
    return _GOVERNANCE_TAXONOMY[name]
