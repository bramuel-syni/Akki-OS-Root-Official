"""services.model_recheck.status — CA1-011 re-check state surface (W7 half).

Returns the honest state of a model's standing re-check date, or names
the gap if the model is unregistered / not applicable (purchased LLM).

W9 will attach the Watch route to fire on `state == 'overdue'`. The
seam name is a stable string on every payload.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from services.model_registry.registry import load_registry


CA1_011_WATCH_SEAM = "services.watch.route_recheck_failure (lands W9)"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso_utc(s: str) -> datetime:
    """Parse an ISO-8601 UTC string with trailing 'Z' into an aware
    datetime. Only supports the exact format we author with."""
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def status_for(model_id: str) -> Dict[str, Any]:
    """Return the re-check state for `model_id`.

    States:
      * 'not_registered'  — model_id is not in the registry (honest gap).
      * 'not_applicable'  — model is a purchased LLM (Emergent Universal
                            seed); re-check cadence does not apply.
                            Named honestly, no fabricated due date.
      * 'due_later'       — re-check is on record and in the future.
      * 'overdue'         — re-check date has passed. W9 Watch route
                            fires here (W7 stamps state only).
    """
    models = load_registry()
    entry = models.get(model_id)
    if entry is None:
        return {
            "model_id": model_id,
            "state": "not_registered",
            "honest_note": (
                f"{model_id!r} is not on record in services/model_registry. "
                f"Register via admission ceremony before re-check applies."
            ),
            "ca1_011_watch_seam": CA1_011_WATCH_SEAM,
            "observed_at": _now_iso(),
        }
    if "re_check_due_at" not in entry:
        return {
            "model_id": model_id,
            "state": "not_applicable",
            "honest_note": (
                f"{model_id!r} is a purchased LLM (provider={entry.get('provider')!r}); "
                f"CA1-011 cadence applies to trained adapters, not purchased LLMs. "
                f"Not a trained model — no re-check due date on record."
            ),
            "ca1_011_watch_seam": CA1_011_WATCH_SEAM,
            "observed_at": _now_iso(),
        }
    due = _parse_iso_utc(entry["re_check_due_at"])
    now = datetime.now(timezone.utc)
    state = "overdue" if due < now else "due_later"
    return {
        "model_id": model_id,
        "state": state,
        "re_check_due_at": entry["re_check_due_at"],
        "connected_at": entry.get("connected_at"),
        "role": entry.get("role"),
        "ca1_011_watch_seam": CA1_011_WATCH_SEAM,
        "observed_at": _now_iso(),
    }
