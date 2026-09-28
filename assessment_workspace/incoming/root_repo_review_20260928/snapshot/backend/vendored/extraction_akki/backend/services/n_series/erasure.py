"""services.n_series.erasure — CA1-N3 access-and-erasure enforcement.

Wave E · CP-E3 (2026-08-27T~13:45Z) · Owner ruling verbatim:
    "CA1-N3 access & erasure: requestor = named customer or employee
     only (no third-party without separate authorization); verification
     = existing platform credential, no new identity machinery; REAL
     erasure for raw source + five-ring units; already-trained models
     get FLAGGED via the A17.15 rights-lapse provenance mechanism and
     scheduled for retraining OR documented as residual exposure.
     Erasure operations route through the custody chokepoint with
     crossing receipts."

Enforcement:
  * policy config `erasure_policy.v0.json` resolves the three
    sentinels + names the allowed requestor classes;
  * refuses requestor_class outside {named_customer, named_employee};
  * refuses payload sentinels (caller must adopt resolved policy);
  * fires a chokepoint crossing receipt (kind='n3_erasure_operation');
  * emits a RightsLapseFlag_v0 for each supplied model_id in the
    payload's `flag_models` field (in-payload list of trained models
    that carry the subject's data);
  * refuses overwrite (Canon 8 §43).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from contracts.erasure_request import ErasureRequest_v0
from contracts.rights_lapse_flag_v0 import RightsLapseFlag_v0


_DEFAULT_DIR = "/app/assessment_workspace/phase0/erasure_requests"
_DEFAULT_FLAGS_DIR = "/app/assessment_workspace/phase0/rights_lapse_flags"
_POLICY_PATH = Path(__file__).with_name("erasure_policy.v0.json")


def _dir() -> Path:
    return Path(os.environ.get("ERASURE_REQUESTS_DIR", _DEFAULT_DIR))


def _flags_dir() -> Path:
    return Path(os.environ.get("RIGHTS_LAPSE_FLAGS_DIR", _DEFAULT_FLAGS_DIR))


def load_policy() -> Dict[str, Any]:
    """Load the CA1-N3 policy config. Owner-supplied resolved values."""
    return json.loads(_POLICY_PATH.read_text())


def _fire_chokepoint_receipt(request_id: str, requester_actor_id: str) -> str:
    """Route the erasure operation through the custody chokepoint per
    owner ruling. Returns the CrossingReceipt.receipt_id."""
    from services.chokepoint import register_crossing
    receipt = register_crossing(
        kind="n3_erasure_operation",
        endpoint={"host": "erasure.internal", "region": "in_process"},
        verb="ERASE",
        payload_shape={"request_id": request_id},
        actor=requester_actor_id,
        masking_tier="attested_command",
    )
    return receipt.receipt_id


def _emit_rights_lapse_flags(
    request_id: str,
    subject_ref: str,
    flag_models: List[Dict[str, str]],
) -> List[str]:
    """For each trained model in `flag_models`, emit a RightsLapseFlag_v0
    per owner ruling: 'already-trained models get FLAGGED via the same
    provenance mechanism as A17.15 rights-lapse, then scheduled for
    retraining OR documented as residual exposure.'

    Each entry in flag_models must be:
      {"model_id": "...", "resolution": "scheduled_retrain" | "documented_residual",
       "resolution_summary": "..."}

    Returns the list of emitted flag_ids.
    """
    d = _flags_dir()
    d.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids: List[str] = []
    for i, entry in enumerate(flag_models):
        flag_id = f"rlf_{request_id.replace('er_', '')}_{i:02d}"
        flag = RightsLapseFlag_v0(
            flag_id=flag_id,
            erasure_request_id=request_id,
            model_id=entry["model_id"],
            subject_ref=subject_ref,
            flagged_at=now,
            resolution=entry["resolution"],
            resolution_summary=entry["resolution_summary"],
        )
        (d / f"{flag_id}.json").write_text(
            json.dumps(flag.model_dump(), indent=2, ensure_ascii=False)
        )
        ids.append(flag_id)
    return ids


def fire_erasure_request(payload: Dict[str, Any]) -> ErasureRequest_v0:
    """CA1-N3 · fire an erasure request with full enforcement.

    Refuses on:
      * requestor_class outside {named_customer, named_employee};
      * any of q1..q3 still at OWNER_POLICY_PENDING;
      * platform_credential_ref empty (owner ruling: existing platform
        credential, no new identity machinery);
      * overwrite of an existing request_id.

    On success:
      * Fires a chokepoint crossing receipt (kind='n3_erasure_operation');
      * Emits RightsLapseFlag_v0 for each model in payload.flag_models;
      * Stamps crossing_receipt_ref + model_flag_ids on the ledger.
    """
    payload = dict(payload)  # local mutation only

    flag_models = payload.pop("flag_models", [])

    # Backward-compat: legacy payloads (scaffolding-era) may omit the
    # additive fields. Refuse only if the CALLER supplies an obviously
    # invalid requestor_class (e.g., "third_party"). Missing values
    # trigger contract-shape validation with a clear error.
    if "requestor_class" in payload:
        allowed = load_policy()["requestor_classes_allowed"]
        if payload["requestor_class"] not in allowed:
            raise ValueError(
                f"CA1-N3 · requestor_class={payload['requestor_class']!r} "
                f"is not permitted · owner ruling: requestor = named "
                f"customer or employee only, no third-party without "
                f"separate authorization. Allowed: {allowed!r}."
            )

    r = ErasureRequest_v0(**payload)

    # Sentinel refusal — caller must adopt resolved policy values.
    pending = [
        f for f in ("q1_erasure_reach", "q2_identity_verification",
                    "q3_retention_conflict")
        if getattr(r, f) == "OWNER_POLICY_PENDING"
    ]
    if pending:
        raise ValueError(
            f"CA1-N3 · cannot fire erasure while policy fields remain "
            f"at 'OWNER_POLICY_PENDING': {pending}. Adopt the resolved "
            f"values from services/n_series/erasure_policy.v0.json."
        )

    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{r.request_id}.json"
    if path.exists():
        raise ValueError(
            f"CA1-N3 · erasure {r.request_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )

    # Custody chokepoint crossing receipt (owner ruling: erasure
    # operations route through the custody chokepoint with crossing
    # receipts).
    receipt_id = _fire_chokepoint_receipt(r.request_id, r.requester_actor_id)

    # Rights-lapse flags for each supplied trained model.
    flag_ids = _emit_rights_lapse_flags(r.request_id, r.subject_summary, flag_models)

    # Rebuild with stamped fields.
    r = ErasureRequest_v0(**{
        **r.model_dump(),
        "crossing_receipt_ref": receipt_id,
        "model_flag_ids": flag_ids,
    })

    path.write_text(json.dumps(r.model_dump(), indent=2, ensure_ascii=False))
    return r


def load_erasure_requests() -> List[ErasureRequest_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return [
        ErasureRequest_v0(**json.loads(p.read_text()))
        for p in sorted(d.glob("er_*.json"))
    ]


def load_rights_lapse_flags() -> List[RightsLapseFlag_v0]:
    d = _flags_dir()
    if not d.is_dir():
        return []
    return [
        RightsLapseFlag_v0(**json.loads(p.read_text()))
        for p in sorted(d.glob("rlf_*.json"))
    ]
