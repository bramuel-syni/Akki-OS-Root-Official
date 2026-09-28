"""services.rights_quarantine — Doc14-020 rights-unclear quarantine.

Wave E · CP-E4 · Owner ruling verbatim (Wave E scope §4):
    "Doc14-020: QUARANTINE-pending-review path for rights-unclear
     training material — a real quarantine store + review queue +
     release/refuse resolution, wired into the training-material admit
     path (admit refuses to pass rights-unclear material through; it
     quarantines with receipt)."

Doc14-020 canon (verbatim, `notes/requirements_register_17docs.md:160`):
    "Rights-unclear material is a first-class state — ADMITS to
     inspection but does NOT ADMIT to extraction for external delivery
     until the rights state is resolved."

Owner reasoning verbatim (Wave E scope §4):
    "Quarantine is the only option that doesn't foreclose anything
     before the status is actually resolved."

State machine:
  quarantined → released (rights resolved: OK to admit)
  quarantined → refused  (rights declined: terminal, no admit)

Records: phase0/rights_quarantine/{admit_id}.json (append-only per
attempt; resolution stamped in-place on state transition).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


_DEFAULT_DIR = "/app/assessment_workspace/phase0/rights_quarantine"


def _dir() -> Path:
    return Path(os.environ.get("RIGHTS_QUARANTINE_DIR", _DEFAULT_DIR))


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RightsQuarantineRecord(BaseModel):
    """A quarantined training-material admit awaiting rights resolution."""

    model_config = ConfigDict(extra="forbid")

    admit_id: str = Field(..., min_length=1)
    training_run_id: str = Field(..., min_length=1)
    unit_manifest_ref: str = Field(..., min_length=1)
    unit_count: int = Field(..., ge=1)
    extraction_pipeline_ref: str = Field(..., min_length=1)
    rights_state: Literal["unclear"] = Field(
        default="unclear",
        description="Only rights-unclear material enters this store.",
    )
    quarantined_at: str = Field(..., min_length=1)
    quarantine_reason: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming why the rights "
                    "state is unclear (source rights posture missing / "
                    "ambiguous declaration / consent lapsed / etc.).",
    )
    resolution: Optional[Literal["released", "refused"]] = Field(
        default=None,
        description="Terminal state · None while awaiting review.",
    )
    resolution_at: Optional[str] = Field(default=None)
    resolution_summary: Optional[str] = Field(
        default=None, min_length=1,
        description="Facts-not-claims sentence naming the resolution "
                    "decision + evidence path.",
    )


def quarantine_admit(
    admit_id: str,
    training_run_id: str,
    unit_manifest_ref: str,
    unit_count: int,
    extraction_pipeline_ref: str,
    quarantine_reason: str,
) -> RightsQuarantineRecord:
    """Refuse rights-unclear material into the training admit path;
    quarantine with a receipt. Owner ruling verbatim: 'admit refuses to
    pass rights-unclear material through; it quarantines with receipt.'"""
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{admit_id}.json"
    if path.exists():
        raise ValueError(
            f"Doc14-020 · rights-quarantine record {admit_id!r} already "
            f"on disk. Canon 8 §43 discipline: correction is by new "
            f"entry only; append a NEW admit_id."
        )
    r = RightsQuarantineRecord(
        admit_id=admit_id,
        training_run_id=training_run_id,
        unit_manifest_ref=unit_manifest_ref,
        unit_count=unit_count,
        extraction_pipeline_ref=extraction_pipeline_ref,
        rights_state="unclear",
        quarantined_at=_now_iso(),
        quarantine_reason=quarantine_reason,
    )
    path.write_text(json.dumps(r.model_dump(), indent=2, ensure_ascii=False))
    return r


def list_quarantine() -> List[RightsQuarantineRecord]:
    d = _dir()
    if not d.is_dir():
        return []
    out: List[RightsQuarantineRecord] = []
    for p in sorted(d.glob("*.json")):
        out.append(RightsQuarantineRecord(**json.loads(p.read_text())))
    return out


def get_quarantine(admit_id: str) -> Optional[RightsQuarantineRecord]:
    path = _dir() / f"{admit_id}.json"
    if not path.is_file():
        return None
    return RightsQuarantineRecord(**json.loads(path.read_text()))


def resolve_quarantine(
    admit_id: str,
    resolution: Literal["released", "refused"],
    resolution_summary: str,
) -> RightsQuarantineRecord:
    """Terminal state transition. `released` = rights resolved OK;
    caller may re-run admit_material() with rights_state='clear'.
    `refused` = rights declined; terminal, no admit."""
    r = get_quarantine(admit_id)
    if r is None:
        raise ValueError(
            f"Doc14-020 · quarantine record {admit_id!r} not found. "
            f"Cannot resolve a non-existent quarantine."
        )
    if r.resolution is not None:
        raise ValueError(
            f"Doc14-020 · quarantine {admit_id!r} already resolved as "
            f"{r.resolution!r} at {r.resolution_at!r}. Canon 8 §43: "
            f"correction is by new entry only."
        )
    updated = RightsQuarantineRecord(**{
        **r.model_dump(),
        "resolution": resolution,
        "resolution_at": _now_iso(),
        "resolution_summary": resolution_summary,
    })
    (_dir() / f"{admit_id}.json").write_text(
        json.dumps(updated.model_dump(), indent=2, ensure_ascii=False)
    )
    return updated
