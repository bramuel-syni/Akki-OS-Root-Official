"""services.watch.mark · Doc 8 §Line 127 verbatim · dye-pack minting.

§Line 127 verbatim (canon/text/Akki_Canon_8_The_Watch.txt):
    'A mark — the dye pack — is minted on conviction and binds every
     dimension the system can observe: identity, credentials, session
     and device fingerprint, the behavioural signature, and the
     content hashes of everything touched in the mirage, so the loot
     itself is dyed and its resurfacing anywhere, ever, is a
     structural detection. The mark survives the attacker shedding
     any one dimension, because the others still resolve.'

Two capabilities:

1. `mint_mark(**dimensions)` — writes a MarkV0 on conviction. Refuses
   if the referenced action is not on record OR is not a `sever`
   action (§Line 127 verbatim: 'minted on conviction'; conviction ≡
   sever in the four-class ladder of §Line 99).

2. `mark_hits_for_hash(content_hash)` — 'its resurfacing anywhere,
   ever, is a structural detection.' Returns every mark on record
   whose content_hashes list contains the given hash.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List, Optional

from contracts.mark_v0 import MarkV0


class WriteOnceViolation(RuntimeError):
    pass


_DEFAULT_DIR = "/app/assessment_workspace/phase0/watch_marks"


def _dir() -> Path:
    d = Path(os.environ.get("WATCH_MARKS_DIR", _DEFAULT_DIR))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _safe_filename(mark_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", mark_id)
    return f"{safe}.json"


def _get_sever_action_on_record(action_ref: str):
    """Return the on-record WatchActionV0 with action_class='sever'
    matching action_ref, else None. Enforces §Line 127 'conviction ≡
    sever' by dispatching through the persistence-layer readers."""
    from services.watch.persistence import get_action

    a = get_action(action_ref)
    if a is None:
        return None
    if a.action_class != "sever":
        # Present on record, but not a conviction.
        return "not_sever"
    return a


def mint_mark(
    *,
    mark_id: str,
    verdict_ref: str,
    action_ref: str,
    identity: str,
    credentials: str,
    session_id: str,
    device_fingerprint: str,
    behavioural_signature: str,
    content_hashes: List[str],
    minted_at: str,
) -> MarkV0:
    """Mint a mark on conviction. §Line 127 verbatim.

    Raises:
      * ValueError · when action_ref is not on record.
      * ValueError · when action_ref exists but is not a sever action
        ('conviction' ≡ sever per §Line 99).
      * ValueError · via MarkV0 grammar on missing/empty dimension.
      * WriteOnceViolation · on duplicate mark_id.
    """
    on_record = _get_sever_action_on_record(action_ref)
    if on_record is None:
        raise ValueError(
            f"action {action_ref!r} not on record. Doc 8 §Line 127 "
            "verbatim: a mark is 'minted on conviction' - conviction "
            "must be an on-record sever action."
        )
    if on_record == "not_sever":
        raise ValueError(
            f"action {action_ref!r} is on record but is not a sever "
            "action. Doc 8 §Line 127 verbatim: a mark is 'minted on "
            "conviction' - conviction ≡ sever (§Line 99 four-class "
            "ladder). Marks against annotate/shape/contain are a "
            "category error."
        )

    mark = MarkV0(
        mark_id=mark_id,
        verdict_ref=verdict_ref,
        action_ref=action_ref,
        identity=identity,
        credentials=credentials,
        session_id=session_id,
        device_fingerprint=device_fingerprint,
        behavioural_signature=behavioural_signature,
        content_hashes=list(content_hashes),
        minted_at=minted_at,
    )

    path = _dir() / _safe_filename(mark.mark_id)
    if path.exists():
        raise WriteOnceViolation(
            f"mark_id {mark.mark_id!r} already on record."
        )
    path.write_text(mark.model_dump_json(indent=2), encoding="utf-8")
    return mark


def read_marks() -> List[MarkV0]:
    d = _dir()
    if not d.is_dir():
        return []
    out: List[MarkV0] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        try:
            out.append(MarkV0(**body))
        except (ValueError, TypeError):
            continue
    return out


def get_mark(mark_id: str) -> Optional[MarkV0]:
    for m in read_marks():
        if m.mark_id == mark_id:
            return m
    return None


def mark_hits_for_hash(content_hash: str) -> List[MarkV0]:
    """§Line 127 verbatim: 'its resurfacing anywhere, ever, is a
    structural detection.' Every mark whose content_hashes contains
    the query hash is returned."""
    return [m for m in read_marks() if content_hash in m.content_hashes]


def resolvable_dimensions(m: MarkV0) -> List[str]:
    """§Line 127 last sentence verbatim: 'The mark survives the
    attacker shedding any one dimension, because the others still
    resolve.'

    Returns the ordered list of dimensions the on-record mark binds.
    Load-bearing for the resilience invariant test."""
    dims: List[str] = []
    if m.identity:
        dims.append("identity")
    if m.credentials:
        dims.append("credentials")
    if m.session_id:
        dims.append("session_id")
    if m.device_fingerprint:
        dims.append("device_fingerprint")
    if m.behavioural_signature:
        dims.append("behavioural_signature")
    if m.content_hashes:
        dims.append("content_hashes")
    return dims
