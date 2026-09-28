"""WPW Tier 1 · Lab Notebook writer.

Spec: `canon/fixtures/whitepaper_wizard_spec_v1/spec.extracted.txt` §4
(Normative Requirements — Lifecycle & observation, Tier 1). Verbatim
quotes appear in the docstrings of the gating invariant tests at
`backend/tests/invariants/test_wpw_tier1_notebook.py` and in the
receipt banked at drill_receipts on close.

The notebook is written on the Doc 5 Ledger-writer pattern — append-
only, hash-chained (per-run `prev_entry_sha256` → `entry_sha256`),
retention class inherited from Doc 5 (indefinite by default; DPO may
rule a window).

Storage layout:
    phase0/wpw_notebook/<safe_run_id>/attach.json      · attach record
    phase0/wpw_notebook/<safe_run_id>/notebook.jsonl   · entries

Zero-influence discipline (WPW-2 · A2):
  Every public writer wraps its persistence in a defensive try/except
  that records the failure to a per-run error log and RETURNS rather
  than raising. This is the mechanical guarantee that wizard presence
  is unobservable to the run — a failed notebook write MUST NOT
  become a caller-visible exception on the run's critical path.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)


# WPW spec §5 · Evidence Classes verbatim:
#   "Three classes carry through every tier: measured (a number from
#    the run's own instrumentation), estimated (a projection, marked
#    with its basis), observed (an event that occurred, with no causal
#    reading attached)."
EVIDENCE_CLASSES = ("measured", "estimated", "observed")

# WPW-3 verbatim:
#   "Minimum event set: commissioning reflection; baseline selection
#    record (Promise #24); checkpoints; each acceptance-criterion
#    transition; every CIF ideation event; every human contribution
#    event; anomalies; cost checkpoints against estimate."
MINIMUM_EVENT_SET = (
    "commissioning_reflection",
    "baseline_selection",
    "checkpoint",
    "acceptance_criterion_transition",
    "cif_ideation",
    "human_contribution",
    "anomaly",
    "cost_checkpoint",
)

# Human contribution shape (WPW-5 verbatim):
#   "Human contribution events MUST record: actor (role and internal
#    identity), the state before, the change made, and the measured
#    movement after. Correlation MUST be recorded as correlation. A
#    causal reading MUST NOT appear in the notebook."
_HUMAN_CONTRIBUTION_REQUIRED_KEYS = (
    "actor",
    "state_before",
    "change",
    "movement_after",
)

# CIF ideation shape (WPW-6 verbatim):
#   "CIF ideation events MUST be mirrored by reference, never copied:
#    the idea, its conditions, its adoption status. The wizard MUST
#    NOT paraphrase an ideation record."
_CIF_IDEATION_REQUIRED_KEYS = (
    "cif_event_ref",       # reference to the CIF-recorded artefact
    "idea_ref",
    "conditions_ref",
    "adoption_status",
)

# Causal-reading refusal (WPW-5): forbidden lexical markers in
# human_contribution payloads.
_CAUSAL_LEXICON = (
    "because ",
    " caused ",
    " causes ",
    " resulted in ",
    " led to ",
    " triggered ",
    " due to ",
)


_DEFAULT_NB_DIR = "/app/assessment_workspace/phase0/wpw_notebook"


def _nb_root() -> Path:
    return Path(os.environ.get("WPW_NOTEBOOK_DIR", _DEFAULT_NB_DIR))


def _safe(run_id: str) -> str:
    """Filesystem-safe rendering of run_id (WPW-4: linked to run artefact)."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", run_id)


def _run_dir(run_id: str) -> Path:
    return _nb_root() / _safe(run_id)


def _attach_path(run_id: str) -> Path:
    return _run_dir(run_id) / "attach.json"


def _notebook_path(run_id: str) -> Path:
    return _run_dir(run_id) / "notebook.jsonl"


def _err_log_path(run_id: str) -> Path:
    return _run_dir(run_id) / "wpw_write_errors.log"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_bytes(entry_wo_hash: Dict[str, Any]) -> bytes:
    """Canonical JSON bytes for hash-chain computation (sort keys, no
    whitespace, UTF-8). Order-stable across languages."""
    return json.dumps(entry_wo_hash, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _log_write_error(run_id: str, kind: str, detail: str) -> None:
    """Zero-influence discipline (WPW-2 · A2): record write failures
    to a per-run error log; never raise to caller."""
    try:
        d = _run_dir(run_id)
        d.mkdir(parents=True, exist_ok=True)
        with _err_log_path(run_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "at_utc": _iso_now(),
                "kind": kind,
                "detail": detail,
            }) + "\n")
    except Exception:  # pragma: no cover — last-resort silence, log to stderr
        log.exception("wpw.tier1_notebook · error-log write failed for run_id=%r", run_id)


def _last_entry_hash(run_id: str) -> Optional[str]:
    """Return the sha256 of the last committed entry, or None if the
    notebook is empty. Hash-chain read (WPW-4 verbatim: 'append-only
    and hash-chained on the Doc 5 pattern')."""
    p = _notebook_path(run_id)
    if not p.exists():
        return None
    last = None
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                continue
    if last is None:
        return None
    return last.get("entry_sha256")


# -----------------------------------------------------------------
# Public API — attach lifecycle
# -----------------------------------------------------------------

def attach_to_run(run_id: str) -> bool:
    """WPW-1 verbatim:
        'The wizard MUST attach to every training run at commissioning.
         There is no per-run opt-in and no manual activation.'

    Idempotent per-run: a second call is a no-op (attach is a
    lifecycle event, not an ideation event). Returns True if a new
    attach was recorded, False if already attached.

    Zero-influence (WPW-2): swallows all storage exceptions to the
    error log; never raises."""
    try:
        if is_attached_to_run(run_id):
            return False
        d = _run_dir(run_id)
        d.mkdir(parents=True, exist_ok=True)
        rec = {
            "run_id": run_id,
            "attached_at_utc": _iso_now(),
            "attach_id": f"wpwa-{uuid.uuid4().hex[:12]}",
            "spec_ref": "whitepaper_wizard_spec_v1 · WPW-1",
        }
        _attach_path(run_id).write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return True
    except Exception as exc:
        _log_write_error(run_id, "attach", repr(exc))
        return False


def is_attached_to_run(run_id: str) -> bool:
    """Read-only attach probe (used by A2 zero-influence test)."""
    return _attach_path(run_id).exists()


# -----------------------------------------------------------------
# Public API — event capture
# -----------------------------------------------------------------

def record_event(
    run_id: str,
    event_kind: str,
    evidence_class: str,
    run_artefact_ref: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """WPW-3 · event-driven capture; WPW-4 · timestamped, artefact-
    linked, classed, append-only, hash-chained.

    Enforces:
      * `evidence_class` ∈ EVIDENCE_CLASSES (§5)
      * `event_kind` from MINIMUM_EVENT_SET or an explicit extension
        (unknown kinds are recorded but flagged in payload with
        `_event_kind_outside_minimum: True` — never silently accepted
        as one of the minimum kinds).
      * `human_contribution` payloads carry (actor, state_before,
        change, movement_after) and contain no causal-reading lexemes.
      * `cif_ideation` payloads carry references (cif_event_ref,
        idea_ref, conditions_ref, adoption_status). No paraphrase
        (mirrored by reference, WPW-6).

    Returns the entry_sha256 of the appended entry, or None if the
    write was refused. Zero-influence: raises no exception.

    Refusal cases (return None + write to error log):
      * evidence_class not in EVIDENCE_CLASSES
      * human_contribution missing required keys or containing a
        causal-reading lexeme
      * cif_ideation missing required reference keys
      * missing run_artefact_ref
      * empty run_id
    """
    try:
        if not run_id:
            _log_write_error("(no-run)", "record_event", "empty run_id")
            return None
        if evidence_class not in EVIDENCE_CLASSES:
            _log_write_error(run_id, "record_event",
                             f"evidence_class not in {EVIDENCE_CLASSES}: {evidence_class!r}")
            return None
        if not run_artefact_ref:
            _log_write_error(run_id, "record_event", "empty run_artefact_ref")
            return None
        payload = dict(payload or {})

        # WPW-5 · human contribution shape + causal-reading refusal.
        if event_kind == "human_contribution":
            missing = [k for k in _HUMAN_CONTRIBUTION_REQUIRED_KEYS if k not in payload]
            if missing:
                _log_write_error(run_id, "record_event",
                                 f"human_contribution missing required keys: {missing}")
                return None
            blob = json.dumps(payload, sort_keys=True).lower()
            for marker in _CAUSAL_LEXICON:
                if marker in blob:
                    _log_write_error(run_id, "record_event",
                                     f"human_contribution refused: causal-reading "
                                     f"lexeme detected ({marker!r}); WPW-5 refuses "
                                     f"causal readings in the notebook.")
                    return None

        # WPW-6 · CIF ideation is mirrored by reference, never copied.
        if event_kind == "cif_ideation":
            missing = [k for k in _CIF_IDEATION_REQUIRED_KEYS if k not in payload]
            if missing:
                _log_write_error(run_id, "record_event",
                                 f"cif_ideation missing reference keys: {missing} "
                                 f"(WPW-6: mirrored by reference, never copied).")
                return None

        # Flag outside-minimum kinds transparently (never silently accepted).
        if event_kind not in MINIMUM_EVENT_SET:
            payload["_event_kind_outside_minimum"] = True

        # Build entry (append-only append; hash-chain over prev+body).
        d = _run_dir(run_id)
        d.mkdir(parents=True, exist_ok=True)
        prev_hash = _last_entry_hash(run_id)
        entry_wo_hash: Dict[str, Any] = {
            "entry_id": f"wpwe-{uuid.uuid4().hex[:12]}",
            "run_id": run_id,
            "at_utc": _iso_now(),
            "event_kind": event_kind,
            "evidence_class": evidence_class,
            "run_artefact_ref": run_artefact_ref,
            "prev_entry_sha256": prev_hash,
            "payload": payload,
        }
        entry_hash = _sha256(_canonical_bytes(entry_wo_hash))
        entry = dict(entry_wo_hash)
        entry["entry_sha256"] = entry_hash

        with _notebook_path(run_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, sort_keys=True, separators=(",", ":"),
                                ensure_ascii=False) + "\n")
        return entry_hash
    except Exception as exc:
        _log_write_error(run_id, "record_event", f"{event_kind}:{repr(exc)}")
        return None


# -----------------------------------------------------------------
# Public API — read + retention
# -----------------------------------------------------------------

def list_entries(run_id: str) -> List[Dict[str, Any]]:
    """Read all entries for a run in write order."""
    p = _notebook_path(run_id)
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def notebook_exists_for_run(run_id: str) -> bool:
    """WPW-7 verbatim:
        'The notebook MUST be retained for every run, including
         refused runs — a rejection's record is part of the research
         record (Promise #22).'

    Returns True if a notebook file has been created for run_id.
    Presence is retention (Doc 5 default: indefinite; DPO may rule)."""
    return _notebook_path(run_id).exists()


def verify_hash_chain(run_id: str) -> Dict[str, Any]:
    """Verify the notebook's hash chain end-to-end.

    Returns {'valid': bool, 'n_entries': int, 'error': Optional[str]}.
    Used by the notebook-completeness invariant (A1)."""
    entries = list_entries(run_id)
    prev = None
    for i, e in enumerate(entries):
        if e.get("prev_entry_sha256") != prev:
            return {
                "valid": False,
                "n_entries": len(entries),
                "error": f"entry {i} prev_entry_sha256 mismatch "
                         f"(expected {prev!r}, got {e.get('prev_entry_sha256')!r})",
            }
        recompute = dict(e)
        stored = recompute.pop("entry_sha256", None)
        actual = _sha256(_canonical_bytes(recompute))
        if actual != stored:
            return {
                "valid": False,
                "n_entries": len(entries),
                "error": f"entry {i} entry_sha256 recompute mismatch "
                         f"(stored {stored!r}, recomputed {actual!r})",
            }
        prev = stored
    return {"valid": True, "n_entries": len(entries), "error": None}


# -----------------------------------------------------------------
# Public API — WPW-18 · economics
# -----------------------------------------------------------------

# WPW-18 verbatim:
#   "Observation cost MUST appear as a budget line on the run's
#    estimate and in cost-against-estimate reporting. Event capture
#    MUST NOT exceed its budgeted share without surfacing as an
#    anomaly in its own notebook."
#
# DEFAULT-class budget share (revisable on owner ratification of the
# WPW spec §7 R3): 1% of the run's total estimated compute-cost
# accounts for wizard observation, with an absolute floor of $0.01
# so tiny mock runs still carry a non-zero line.
WPW_OBSERVATION_BUDGET_SHARE_DEFAULT = 0.01
WPW_OBSERVATION_BUDGET_FLOOR_USD_DEFAULT = 0.01


def compute_observation_budget_line(run_cost_estimate_usd: float) -> Dict[str, Any]:
    """WPW-18: compute the wizard-observation budget line for a run's
    estimate. Callers append this line to the run's cost-ledger
    estimate at commissioning."""
    share = WPW_OBSERVATION_BUDGET_SHARE_DEFAULT
    floor = WPW_OBSERVATION_BUDGET_FLOOR_USD_DEFAULT
    computed = max(float(run_cost_estimate_usd) * share, floor)
    return {
        "line_kind": "wpw_observation",
        "share_of_run_estimate": share,
        "floor_usd": floor,
        "line_amount_usd": round(computed, 6),
        "class_note": "DEFAULT-class per WPW spec §7 R3; owner may re-rule.",
    }
