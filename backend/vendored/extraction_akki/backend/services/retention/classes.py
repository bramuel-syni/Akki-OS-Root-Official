"""services.retention.classes — CA1-N1 · governed per-record-class letter.

Owner Ruling 2026-08-25 · W6 GO §W6-SCOPE-(b):
    Retention on append-only classes = mark-expired + excluded-from-render,
    NEVER hard delete.

Canon 1 §4.3 · "One record ... every admission, measurement, commission,
    operation, answer, refusal, rule change, and access grant writes to
    a single append-only ledger."
"""
from __future__ import annotations

from typing import Any, Dict, Optional


# W1-W5 record classes we hold on disk · CA1-N1 letter.
# Adding a class requires an Owner ruling recorded in STATE/DECISIONS.md.
RETENTION_CLASSES: Dict[str, Dict[str, Any]] = {
    "crossing_receipts": {
        "storage_kind": "append_only",
        "storage_dir_env": "CROSSING_RECEIPT_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/crossing_receipts",
        "file_glob": "rcp-*.json",
        "at_iso_field": "at_iso",
        "default_retention_days": 90,
        "marked_expired_after_days": 90,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "Canon 1 §4.3 (single log) + Doc 01 §A5.7 (trust receipt)",
        "letter": (
            "Crossing receipts are the estate's single trust log. They are "
            "append-only. Retention beyond 90 days marks them expired and "
            "excludes them from render. The record on disk remains for audit."
        ),
    },
    "northena_ledger": {
        "storage_kind": "append_only",
        "storage_dir_env": "NORTHENA_LEDGER_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/northena_ledger",
        "file_glob": "row-*.json",
        "at_iso_field": "at",
        "default_retention_days": 365,
        "marked_expired_after_days": 365,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "Doc 05 §B5.4 (Northena sole writer of ledger rows)",
        "letter": (
            "Northena ledger rows record direction admissions, gates, "
            "converges. Append-only. Retention beyond 365 days marks "
            "expired; row on disk remains for audit."
        ),
    },
    "reflection_records": {
        "storage_kind": "append_only",
        "storage_dir_env": "REFLECTION_RECORD_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/reflection_records",
        "file_glob": "refl-*.json",
        "at_iso_field": "at_iso",
        "default_retention_days": 90,
        "marked_expired_after_days": 90,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "Doc 12 §B5 (Reflection-before-commit)",
        "letter": (
            "Compute-seam reflections record what a run would cost / touch "
            "before it is committed. Append-only. Retention 90 days · "
            "marked-expired excluded from render."
        ),
    },
    "solva_runs": {
        "storage_kind": "append_only",
        "storage_dir_env": "SOLVA_RUN_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/solva_runs",
        "file_glob": "run-*.json",
        "at_iso_field": "at_iso",
        "default_retention_days": 90,
        "marked_expired_after_days": 90,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "W5 CP3 discipline (Solva reasoning traces)",
        "letter": (
            "Solva reasoning runs record the three-stage walk with joined "
            "receipt identities. Append-only. Retention 90 days · marked-"
            "expired excluded from render."
        ),
    },
    "northena_admits": {
        "storage_kind": "append_only",
        "storage_dir_env": "NORTHENA_ADMIT_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/northena_admits",
        "file_glob": "admit-*.json",
        "at_iso_field": "at",
        "default_retention_days": 365,
        "marked_expired_after_days": 365,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "Doc 05 §B5.2 (Northena admit records)",
        "letter": (
            "Admit records witness the direction accepted into an "
            "objective. Append-once. Revocation is a separate ledger row "
            "· the admit itself is never deleted. Retention 365 days · "
            "marked-expired excluded from render."
        ),
    },
    "commissioning_records": {
        "storage_kind": "append_only",
        "storage_dir_env": "COMMISSIONING_RECORD_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/commissioning_records",
        "file_glob": "commissioning_*.json",
        "at_iso_field": "commissioned_at",
        "default_retention_days": 730,
        "marked_expired_after_days": 730,
        "enforcement_verb": "mark_expired",
        "canon_anchor": "Doc 09 · connected estate records",
        "letter": (
            "Commissioning records witness how each engine's connection "
            "was verified. Append-only. Retention 730 days · marked-"
            "expired excluded from render."
        ),
    },
    "data_connection_records": {
        "storage_kind": "governed_delete",
        "storage_dir_env": "DATA_CONNECTION_RECORD_DIR",
        "storage_dir_default": "/app/assessment_workspace/phase0/data_connection_records",
        "file_glob": "data_source_*_FINAL.json",
        "at_iso_field": "at",
        "default_retention_days": 365,
        "grace_period_days": 90,
        "enforcement_verb": "soft_delete",
        "canon_anchor": "Doc 09 · connections can be retired",
        "letter": (
            "Data connection records can be retired when a connection is "
            "removed. Retention 365 days · then soft-delete (moved to "
            "retired/) for a 90-day grace-period audit window · then "
            "hard-delete per the register letter."
        ),
    },
}


def class_for(name: str) -> Optional[Dict[str, Any]]:
    """Return the retention letter for `name` or None."""
    return RETENTION_CLASSES.get(name)


def letter_for(name: str) -> str:
    """Return the plain-language letter for `name` (empty string if unknown)."""
    c = class_for(name)
    return c.get("letter", "") if c else ""


__all__ = ["RETENTION_CLASSES", "class_for", "letter_for"]
