"""services.watch.continuity — CA1-N5 ledger continuity attestation.

Wave E · CP-E1 · 2026-08-27T~12:15Z (post Wave D ratification).

Owner ruling (Wave E scope §3 verbatim):
    "CA1-N5 ledger continuity: countersigner independent of the primary
     ledger writer's infrastructure (external-witness pattern);
     cadence = quarterly recorded as DEFAULT-class (preserve the
     proposal-class distinction in the contract/config — it is NOT
     canon-grounded like the 72h window)."

Enforcement (mechanism · not scaffolding):
  * countersigner (`attested_by`) MUST be a registered
    WitnessIdentity_v0 with `independent_of_authorities=True`.
    Contract-shape guarantees the flag; service-side defence-in-depth
    check catches out-of-band tampering of the on-disk record.
  * `verification_mechanism = "independent_backup_check"` is the
    canonical resolved value (see continuity_policy.v0.json).
  * `rto_target_seconds = OWNER_POLICY_PENDING` remains a service
    refusal — owner has NOT ruled RTO (honest stop).
  * cadence policy lives in `continuity_policy.v0.json` alongside;
    proposal-class-vs-canon-class distinction preserved.

Records: phase0/continuity_attestations/ca_*.json (append-only ·
Canon 8 §43 correction-by-new-entry-only).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from contracts.continuity_attestation import ContinuityAttestation_v0
from services.watch.witness import load_identities


_DEFAULT_DIR = "/app/assessment_workspace/phase0/continuity_attestations"
_PENDING_SENTINEL = "OWNER_POLICY_PENDING"
_POLICY_PATH = Path(__file__).with_name("continuity_policy.v0.json")


def _dir() -> Path:
    return Path(os.environ.get("CONTINUITY_ATTESTATIONS_DIR", _DEFAULT_DIR))


def load_policy() -> Dict[str, Any]:
    """Load the CA1-N5 policy config. Owner-supplied values live here;
    the mechanism reads-only."""
    return json.loads(_POLICY_PATH.read_text())


def _witness_or_refuse(witness_id: str) -> None:
    """Refuse if the countersigner is not on record OR is not
    canonically independent (Canon 8 §9 verbatim invariant)."""
    for w in load_identities():
        if w.witness_id == witness_id:
            if w.independent_of_authorities is not True:
                raise ValueError(
                    f"CA1-N5 · countersigner {witness_id!r} on record but "
                    f"`independent_of_authorities` is not True — Canon 8 "
                    f"§9 verbatim invariant violated (witness holds "
                    f"NEITHER authority's credentials). The on-disk "
                    f"record has been tampered with; refuse to attest."
                )
            return
    raise ValueError(
        f"CA1-N5 · witness {witness_id!r} not on record. Register the "
        f"witness identity (POST /api/watch/witness/identity) before "
        f"firing a continuity attestation."
    )


def write_attestation(payload: Dict[str, Any]) -> ContinuityAttestation_v0:
    """Witness writes a continuity attestation to disk. Refuses to fire
    while any owner-policy field is pending. Refuses overwrite. Enforces
    countersigner independence."""
    a = ContinuityAttestation_v0(**payload)
    pending_fields = []
    for f in ("rto_target_seconds", "verification_mechanism"):
        if getattr(a, f) == _PENDING_SENTINEL:
            pending_fields.append(f)
    if pending_fields:
        raise ValueError(
            f"CA1-N5 · {_PENDING_SENTINEL} fields present: "
            f"{pending_fields}. Owner ruling on 2026-08-27 resolved "
            f"verification_mechanism='independent_backup_check' "
            f"(external-witness pattern) but rto_target_seconds is "
            f"still owner-pending. Cannot fire attestation."
        )
    _witness_or_refuse(a.attested_by)
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{a.attestation_id}.json"
    if path.exists():
        raise ValueError(
            f"attestation {a.attestation_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(a.model_dump(), indent=2, ensure_ascii=False))
    return a


def load_attestations() -> List[ContinuityAttestation_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return sorted(
        (ContinuityAttestation_v0(**json.loads(p.read_text()))
         for p in d.glob("ca_*.json")),
        key=lambda a: (a.attested_at, a.attestation_id),
    )

