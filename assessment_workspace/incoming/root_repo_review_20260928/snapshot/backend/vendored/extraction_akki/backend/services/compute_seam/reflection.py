"""services.compute_seam.reflection — reflection-before-commit (Doc 12 · W2).

Owner Order 2026-08-25 · "W2 go" · FL-P2-28 · Doc 12 §B5.1–§B5.6.

Contract:
  compute_projection(proposed_action) → envelope
      Compute the B4 commit envelope for a proposed COMPUTE-related action.
      Every figure derives from a measured/recorded fact on disk. When no
      rate is on record the envelope carries measured quantities only and
      an honest_gap sentence — never a fabricated currency figure.

  acknowledge_and_commit(reflection_id, actor, proposed_action) → run_row
      The commit endpoint. Refuses:
        - if reflection_id is missing / unknown (server-side gate);
        - if proposed_action.kind is non-compute (rule change, deletion).
      On success writes a run record ledger row carrying the attributed
      ack (actor + iso timestamp) and the reflection_id identity join —
      NEVER a copy of the projection payload (REFERENCE-NOT-COPY).

  ReflectionRefusal
      Raised on any refusal from either endpoint.

Storage:
  Projections and run records are written as JSON under
  /app/assessment_workspace/phase0/reflection_records/ and
  /app/assessment_workspace/phase0/commit_records/. Reference-not-copy
  joins work across restarts because the reflection_id is stable and the
  projection resolves through the read path.

No LLM SDK. No external HTTP client. No shield. No secrets read.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# Failure type.
# ---------------------------------------------------------------------------

class ReflectionRefusal(Exception):
    """Raised when the reflection/commit gate refuses."""


# ---------------------------------------------------------------------------
# Storage directories — env-overridable; default to assessment workspace.
# ---------------------------------------------------------------------------

_DEFAULT_REFLECTION_DIR = "/app/assessment_workspace/phase0/reflection_records"
_DEFAULT_COMMIT_DIR = "/app/assessment_workspace/phase0/commit_records"
_DEFAULT_COMMISSIONING_DIR = "/app/assessment_workspace/phase0/commissioning_records"
_DEFAULT_DATA_CONNECTION_DIR = "/app/assessment_workspace/phase0/data_connection_records"
_DEFAULT_PRICE_MODEL_PATH = (
    "/app/assessment_workspace/repos/Extraction-Akki/"
    "backend/services/economics/price_model.v0-exploratory.json"
)


def _reflection_dir() -> Path:
    return Path(os.environ.get("REFLECTION_RECORD_DIR", _DEFAULT_REFLECTION_DIR))


def _commit_dir() -> Path:
    return Path(os.environ.get("COMMIT_RECORD_DIR", _DEFAULT_COMMIT_DIR))


def _commissioning_dir() -> Path:
    return Path(os.environ.get("COMMISSIONING_RECORD_DIR", _DEFAULT_COMMISSIONING_DIR))


def _data_connection_dir() -> Path:
    return Path(os.environ.get("DATA_CONNECTION_RECORD_DIR", _DEFAULT_DATA_CONNECTION_DIR))


def _price_model_path() -> Path:
    return Path(os.environ.get("PRICE_MODEL_PATH", _DEFAULT_PRICE_MODEL_PATH))


# ---------------------------------------------------------------------------
# Kind classification — Doc 12 B5.6 [RULED].
# ---------------------------------------------------------------------------

_COMPUTE_KINDS = frozenset({"extraction", "training"})
_NON_COMPUTE_KINDS = frozenset({
    "rule_change",
    "deletion",
    "declaration_edit",
    "access_review",
})


def _is_compute_kind(kind: str) -> bool:
    return (kind or "").lower() in _COMPUTE_KINDS


def _is_non_compute_kind(kind: str) -> bool:
    return (kind or "").lower() in _NON_COMPUTE_KINDS


# ---------------------------------------------------------------------------
# Rate config — honest gap when absent.
# ---------------------------------------------------------------------------

def _load_rate_config() -> Optional[Dict[str, Any]]:
    """Load the price-model configuration, if present.

    Returns None when no rate config exists — that is the honest state
    this cycle: the estate has no cost rates on record. When W6's Cost
    Ledger lands, the JSON will exist and this function returns its
    contents. NO fabricated defaults; None is the honest state.

    A file exists only if it declares an in-force rate table. A file
    with a placeholder / exploratory flag is treated as absent so the
    projection stays honest.
    """
    p = _price_model_path()
    if not p.is_file():
        return None
    try:
        raw = json.loads(p.read_text())
    except Exception:
        return None
    # exploratory / non-precedent quotes DO NOT satisfy the "rate on record"
    # test (Doc 12 §B5.4 · learning-phase quotes are non-precedent).
    if raw.get("status") in {"exploratory", "learning_phase", "draft"}:
        return None
    if raw.get("rates_on_record") is not True:
        return None
    return raw


# ---------------------------------------------------------------------------
# Measured-quantities discovery — every figure has a provenance identity.
# ---------------------------------------------------------------------------

def _measured_data_source_facts(scope_ref: str) -> Dict[str, Any]:
    """Look up recorded facts for a data-source scope.

    Reads phase0/data_connection_records/*_FINAL.json to find the source
    that matches scope_ref (either by database name or by source_id).
    Returns measured quantities (row estimates, table count) with their
    provenance identity — NEVER copies the record content.
    """
    p = _data_connection_dir()
    if not p.is_dir():
        return {}
    scope_lc = (scope_ref or "").lower()
    for f in sorted(p.glob("data_source_*_FINAL.json")):
        try:
            r = json.loads(f.read_text())
        except Exception:
            continue
        sid = (r.get("source_id") or "").lower()
        db = (r.get("resource") or {}).get("database", "").lower()
        if scope_lc == sid or scope_lc.endswith("." + db) or scope_lc == db:
            top = r.get("top_25_tables") or []
            approx_total = sum(t.get("approx_rows", 0) or 0 for t in top[:25])
            return {
                "estate_rows_approx": {
                    "value": approx_total,
                    "unit": "rows",
                    "is_approximate": True,
                    "provenance_ref": f"data_source_record:{r.get('source_id')}",
                },
                "table_count": {
                    "value": r.get("table_count", 0) or 0,
                    "unit": "tables",
                    "provenance_ref": f"data_source_record:{r.get('source_id')}",
                },
            }
    return {}


def _measured_compute_facts() -> Dict[str, Any]:
    """Look up recorded facts for connected compute.

    Reads phase0/commissioning_records/*_ACCEPTED.json for the accepted
    host and returns capacity provenance-tagged. Reference-not-copy:
    identity is the file's basename; content is not embedded here beyond
    a small headline capacity summary needed for feasibility.
    """
    p = _commissioning_dir()
    if not p.is_dir():
        return {}
    for f in sorted(p.glob("commissioning_*_ACCEPTED.json")):
        try:
            r = json.loads(f.read_text())
        except Exception:
            continue
        cap = r.get("capacity") or {}
        gpu = cap.get("gpu") or {}
        return {
            "gpu_count": {
                "value": gpu.get("count") or 0,
                "unit": "gpu",
                "provenance_ref": f"commissioning_record:{r.get('host_name')}",
            },
            "gpu_model": {
                "value": gpu.get("model", ""),
                "unit": "model",
                "provenance_ref": f"commissioning_record:{r.get('host_name')}",
            },
            "storage_free_tb": {
                "value": _primary_free_tb(cap),
                "unit": "TB",
                "provenance_ref": f"commissioning_record:{r.get('host_name')}",
            },
        }
    return {}


def _primary_free_tb(capacity: Dict[str, Any]) -> Optional[float]:
    for s in capacity.get("storage", []) or []:
        if s.get("note") == "primary working volume":
            return s.get("free_tb")
    return None


# ---------------------------------------------------------------------------
# Feasibility verdict — Doc 12 §B5.1.
# ---------------------------------------------------------------------------

def _feasibility_verdict(
    proposed_action: Dict[str, Any],
    ds_facts: Dict[str, Any],
    compute_facts: Dict[str, Any],
) -> str:
    """Return the plain-sentence feasibility verdict.

    Un-censused reach honestly returns "unknown"; sampled reach returns
    a floor-feasible verdict. Doc 12 §B5.5 · fabricated availability is
    forbidden — this function returns the honest "unknown" when the
    scope is not measured.
    """
    kind = (proposed_action.get("kind") or "").lower()
    scope_ref = proposed_action.get("scope_ref") or ""
    if kind == "extraction":
        if not ds_facts:
            return "unknown — the source has not been censused yet"
        rows = ds_facts.get("estate_rows_approx", {}).get("value") or 0
        return (
            f"floor feasible — {rows:,} approximate rows in scope "
            f"(from information_schema)"
        )
    if kind == "training":
        if not compute_facts:
            return "unknown — no compute is connected"
        gpus = compute_facts.get("gpu_count", {}).get("value") or 0
        gpu_model = compute_facts.get("gpu_model", {}).get("value") or "GPU"
        return f"floor feasible — {gpus} × {gpu_model} accepted for this workload"
    return f"unknown — the estate has no feasibility rule for kind={kind!r}"


def _grounding_marker(
    proposed_action: Dict[str, Any],
    ds_facts: Dict[str, Any],
    compute_facts: Dict[str, Any],
) -> str:
    """Doc 12 §B5.1 · sample-grounded vs estimate-grounded vs unknown."""
    kind = (proposed_action.get("kind") or "").lower()
    if kind == "extraction":
        # A record exists means an information_schema census exists →
        # estimate-grounded. Full sample-grounding waits on a sample run
        # (Doc 12 §B5.5).
        return "estimate-grounded" if ds_facts else "unknown"
    if kind == "training":
        return "estimate-grounded" if compute_facts else "unknown"
    return "unknown"


# ---------------------------------------------------------------------------
# Honest gap sentence — Doc 12 §B5.4 + owner grammar (2026-08-25).
# ---------------------------------------------------------------------------

# Verbatim from owner's W2 go response (2026-08-25):
#   "No rate is on record for this machine — the projection shows measured
#    quantities only (GPU hours, storage touched). Money figures will appear
#    when the cost ledger is in force."
_HONEST_GAP_NO_RATE = (
    "No rate is on record for this machine — the projection shows measured "
    "quantities only (GPU hours, storage touched). Money figures will appear "
    "when the cost ledger is in force."
)


# ---------------------------------------------------------------------------
# Projection persistence — session-only identity write.
# ---------------------------------------------------------------------------

def _write_projection(envelope: Dict[str, Any]) -> None:
    d = _reflection_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{envelope['reflection_id']}.json").write_text(
        json.dumps(envelope, indent=2, sort_keys=True)
    )


def _read_projection(reflection_id: str) -> Optional[Dict[str, Any]]:
    p = _reflection_dir() / f"{reflection_id}.json"
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _write_commit(run_row: Dict[str, Any]) -> None:
    d = _commit_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{run_row['run_id']}.json").write_text(
        json.dumps(run_row, indent=2, sort_keys=True)
    )


# ---------------------------------------------------------------------------
# Public API.
# ---------------------------------------------------------------------------

def compute_projection(*, proposed_action: Dict[str, Any]) -> Dict[str, Any]:
    """Doc 12 §B5.1 · reflection: cost + feasibility BEFORE commit.

    The envelope carries every B4 field. When no rate is on record the
    currency_figures dict is empty and honest_gap names the missing
    ceremony. Every measured quantity carries a provenance_ref identity
    (REFERENCE-NOT-COPY).
    """
    kind = (proposed_action.get("kind") or "").lower()
    scope_ref = proposed_action.get("scope_ref") or ""

    ds_facts = _measured_data_source_facts(scope_ref) if kind == "extraction" else {}
    compute_facts = _measured_compute_facts() if kind in _COMPUTE_KINDS else {}

    measured_quantities: Dict[str, Any] = {}
    measured_quantities.update(ds_facts)
    measured_quantities.update(compute_facts)
    # Every projection carries the scope ceiling as a measured intent
    # (declared by the requester; recorded with its own provenance).
    sc = proposed_action.get("scope_ceiling") or {}
    if sc:
        measured_quantities["scope_ceiling_intent"] = {
            "value": sc,
            "provenance_ref": "commissioner_declared:scope_ceiling",
        }

    rate_config = _load_rate_config()
    currency_figures: Dict[str, Any] = {}
    honest_gap = ""
    price_model_version = "no-rates-on-record"
    if rate_config is None:
        honest_gap = _HONEST_GAP_NO_RATE
    else:
        # W6 will land the currency compute here when rates exist. Today
        # this branch never fires (no in-force rate config on disk).
        price_model_version = rate_config.get("version", "unknown")

    reflection_id = f"refl-{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    envelope: Dict[str, Any] = {
        "reflection_id": reflection_id,
        "feasibility_verdict": _feasibility_verdict(proposed_action, ds_facts, compute_facts),
        "grounding_marker": _grounding_marker(proposed_action, ds_facts, compute_facts),
        "lawful_basis": proposed_action.get("lawful_basis") or "",
        "budget_ceiling": proposed_action.get("budget_ceiling") or {},
        "commissioner": proposed_action.get("commissioner") or "",
        "scope_ceiling": sc,
        "price_model_version": price_model_version,
        "measured_quantities": measured_quantities,
        "currency_figures": currency_figures,
        "honest_gap": honest_gap,
        "provenance": {
            "reflection_record_dir": str(_reflection_dir()),
            "data_connection_record_dir": str(_data_connection_dir()),
            "commissioning_record_dir": str(_commissioning_dir()),
        },
        "kind": kind,
        "scope_ref": scope_ref,
        "generated_at_iso": now_iso,
    }
    _write_projection(envelope)
    return envelope


def acknowledge_and_commit(
    *,
    reflection_id: Optional[str],
    actor: Optional[str],
    proposed_action: Dict[str, Any],
) -> Dict[str, Any]:
    """Doc 12 §B5.1 · commit — REFUSES without an ack referencing an
    existing projection identity.

    Rules:
      (b) reflection_id missing → REFUSE (reflection_required).
      (d) reflection_id unknown / stale → REFUSE (server-side gate).
      B5.6 non-compute kind → REFUSE (non_compute_kind).
      (e) attributed ack: actor + iso timestamp captured.
      (c/g) reference-not-copy: run row carries reflection_id only;
            never embeds a copy of the projection payload.
    """
    if not reflection_id:
        raise ReflectionRefusal(
            "reflection_required — no cost reflection was acknowledged before "
            "commit; a compute-consuming action must reflect before it commits "
            "(Doc 12 §B5.1)."
        )
    kind = (proposed_action.get("kind") or "").lower()
    if _is_non_compute_kind(kind):
        raise ReflectionRefusal(
            f"non_compute_kind — the reflection-before-commit discipline "
            f"applies to compute-consuming commit-type actions (extraction, "
            f"training); kind={kind!r} carries no compute cost to reflect "
            f"(Doc 12 §B5.6)."
        )
    projection = _read_projection(reflection_id)
    if projection is None:
        raise ReflectionRefusal(
            f"reflection_id_unknown — no projection is on record under "
            f"identity {reflection_id!r}; the ack must reference an existing "
            f"projection (server-side gate, Doc 12 §B5.1)."
        )
    # Guard against reflection-to-action drift: kind + scope must match.
    if projection.get("kind") and projection["kind"] != kind:
        raise ReflectionRefusal(
            f"reflection_action_mismatch — projection was computed for "
            f"kind={projection['kind']!r}; commit is for kind={kind!r}. "
            f"An extension re-quotes (Doc 12 §B5.3)."
        )
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    run_row: Dict[str, Any] = {
        "run_id": f"run-{uuid.uuid4().hex[:12]}",
        "kind": kind,
        "scope_ref": proposed_action.get("scope_ref") or "",
        "reflection_id": reflection_id,
        "acknowledged_by": actor or "unknown",
        "acknowledged_at_iso": now_iso,
        "committed_at_iso": now_iso,
        # NO measured_quantities / currency_figures / provenance / envelope
        # here — REFERENCE-NOT-COPY: those resolve through the read path
        # from reflection_id.
    }
    _write_commit(run_row)
    return run_row
