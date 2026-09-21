"""services.trace.timeline — assemble governance timeline from
existing on-disk records. REFERENCE-NOT-COPY discipline.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class TraceEntry:
    """One row in the governance timeline. References the underlying
    record file rather than duplicating its content."""
    at_iso: str
    kind: str
    entry_id: str
    summary: str
    source_path: str


# Producers we scan for timeline entries. Each producer names:
#   env_var:   env var overriding the default path (matches producer service)
#   default:   default directory relative to phase0
#   glob:      filename glob within that directory
#   kind:      trace kind label
#   at_field:  the record's timestamp field name
#   id_field:  the record's id field name
#   summary:   function to derive a summary from the record
_PRODUCERS = [
    {
        "env_var": "MODEL_ADMISSION_RECORDS_DIR",
        "default": "model_admission_records",
        "glob": "admit_*.json",
        "kind": "model_admission",
        "at_field": "computed_at",
        "id_field": "candidate_model_id",
        "summary": lambda r: (
            f"admission {r.get('outcome', '?')} for "
            f"{r.get('candidate_model_id', '?')}"
        ),
    },
    {
        "env_var": "APPROVAL_RECORDS_DIR",
        "default": "approval_records/requests",
        "glob": "ar_*.json",
        "kind": "approval_request",
        "at_field": "proposed_at",
        "id_field": "request_id",
        "summary": lambda r: (
            f"approval requested ({r.get('kind', '?')}): "
            f"{r.get('subject_summary', '')}"
        ),
    },
    {
        "env_var": "APPROVAL_RECORDS_DIR_DECISIONS",
        "default": "approval_records/decisions",
        "glob": "ad_*.json",
        "kind": "approval_decision",
        "at_field": "decided_at",
        "id_field": "decision_id",
        "summary": lambda r: (
            f"approval {r.get('verdict', '?')} on {r.get('request_id', '?')}"
        ),
    },
    {
        "env_var": "HANDOFF_CONTRACTS_DIR",
        "default": "handoff_contracts",
        "glob": "ho_*.json",
        "kind": "handoff_contract",
        "at_field": "authored_at",
        "id_field": "handoff_id",
        "summary": lambda r: (
            f"handoff registered: {r.get('what', '')}"
        ),
    },
    {
        "env_var": "BASELINE_LINES_DIR",
        "default": "baseline_lines",
        "glob": "bl_*.json",
        "kind": "baseline_line",
        "at_field": "authored_at",
        "id_field": "baseline_line_id",
        "summary": lambda r: (
            f"baseline line for {r.get('training_run_id', '?')} · "
            f"starting {r.get('starting_model_id', '?')}"
        ),
    },
    {
        "env_var": "BREACH_NOTIFICATIONS_DIR",
        "default": "breach_notifications",
        "glob": "bn_*.json",
        "kind": "breach_notification",
        "at_field": "triggered_at",
        "id_field": "notification_id",
        "summary": lambda r: (
            f"CA1-N2 · {r.get('breach_summary', '')}"
        ),
    },
    {
        "env_var": "ERASURE_REQUESTS_DIR",
        "default": "erasure_requests",
        "glob": "er_*.json",
        "kind": "erasure_request",
        "at_field": "requested_at",
        "id_field": "request_id",
        "summary": lambda r: (
            f"CA1-N3 · {r.get('subject_summary', '')}"
        ),
    },
]


def _phase0_root() -> Path:
    return Path("/app/assessment_workspace/phase0")


def _dir_for(producer: Dict[str, Any]) -> Path:
    env = os.environ.get(producer["env_var"])
    if env:
        return Path(env)
    return _phase0_root() / producer["default"]


def _read_entries_for(producer: Dict[str, Any]) -> List[TraceEntry]:
    d = _dir_for(producer)
    if not d.is_dir():
        return []
    out: List[TraceEntry] = []
    for p in sorted(d.glob(producer["glob"])):
        try:
            r = json.loads(p.read_text())
        except Exception:
            continue
        at = r.get(producer["at_field"], "")
        entry_id = r.get(producer["id_field"], p.stem)
        summary = producer["summary"](r)
        out.append(TraceEntry(
            at_iso=at,
            kind=producer["kind"],
            entry_id=entry_id,
            summary=summary,
            source_path=str(p),
        ))
    return out


def load_timeline(since_iso: str | None = None,
                  kinds: List[str] | None = None) -> List[TraceEntry]:
    """Assemble the governance timeline from every producer.

    - `since_iso`: filter to entries with at_iso >= since_iso (ISO
      string compare — safe because our timestamps are all
      YYYY-MM-DDTHH:MM:SSZ).
    - `kinds`: filter to specific kinds; None = every kind.
    """
    all_entries: List[TraceEntry] = []
    for producer in _PRODUCERS:
        if kinds is not None and producer["kind"] not in kinds:
            continue
        all_entries.extend(_read_entries_for(producer))
    if since_iso is not None:
        all_entries = [e for e in all_entries if e.at_iso >= since_iso]
    all_entries.sort(key=lambda e: (e.at_iso, e.kind, e.entry_id))
    return all_entries
