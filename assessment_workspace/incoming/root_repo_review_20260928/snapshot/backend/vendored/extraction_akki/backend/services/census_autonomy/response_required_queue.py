"""services.census_autonomy.response_required_queue — filesystem-cursor-
backed queue for mid-run "response-required" items surfaced in the portal
UI.

Owner R-106 §4 verbatim (banked at services/census_autonomy/service_shape.py:70):
  "'response-required item to a queue surfaced ... in the portal UI'"

Owner directive 2026-09-22T~19:05Z (verbatim):
  "the drawer advertises response-required; the backing queue + endpoints
  must exist before anything else — an advertised control with no
  endpoint is a fake state by another name."

## Design

Queue rooted at `CENSUS_STATE_DIR/response_required/` — adjacent to the
sealed engine's `pending/` / `running/` cursor directories, following the
same filesystem-cursor convention. Items are `{item_id}.json` files. Each
file mutation is atomic (write to `.tmp` then rename).

Public callables:
- `bank_response_required_item(census_run_id, tenant_id, reason_text,
  refusal_code, decision_timestamp_utc) -> item_id`
- `list_pending_response_required_items() -> list[dict]` (sorted by
  banked_at_utc ascending)
- `resolve_response_required_item(item_id, resolver_id, resolution_text,
  resolved_state) -> dict`

Public constants:
- `RESPONSE_REQUIRED_ITEM_STATE_CODES: Final[tuple]` — closed vocab
  ("PENDING", "RESOLVED_ACCEPTED", "RESOLVED_REJECTED"). No other codes
  admitted per SO §3.10-α.
- `RESPONSE_REQUIRED_DIR: Final[Path]` — the on-disk root; derived off
  `CENSUS_AUTONOMY_STATE_DIR` env at import time.

Public exception classes:
- `ItemNotFound` — raised by resolve when item_id does not exist.
- `InvalidResolvedState` — raised by resolve when resolved_state is not
  in {"RESOLVED_ACCEPTED", "RESOLVED_REJECTED"}. PENDING is the initial
  state banked by `bank_response_required_item` and is NEVER a valid
  target of `resolve_response_required_item`.

## SO §3.8 additive-only compliance

Consumes no sealed carrier modules. Sits parallel to the sealed engine —
production writers into the queue (refusal-bank bridge, drawer-owner-in-
the-loop button, ...) are DEFERRED to future slices. This slice provides
the queue infrastructure only.
"""

from __future__ import annotations

import json
import os
import pathlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Final, List, Tuple


# ---------------------------------------------------------------------------
# Closed vocabulary (SO §3.10-α · Final tuple · paired-equality pinned by
# invariant 3 in tests/invariants/test_cp_census_autonomy_response_required_a_triple_prime_cont_a.py)
# ---------------------------------------------------------------------------

RESPONSE_REQUIRED_ITEM_STATE_CODES: Final[Tuple[str, ...]] = (
    "PENDING",
    "RESOLVED_ACCEPTED",
    "RESOLVED_REJECTED",
)

_VALID_RESOLVED_TARGETS: Final[frozenset] = frozenset(
    {"RESOLVED_ACCEPTED", "RESOLVED_REJECTED"}
)


# ---------------------------------------------------------------------------
# Filesystem cursor root — off CENSUS_AUTONOMY_STATE_DIR env
# ---------------------------------------------------------------------------

_CENSUS_STATE_DIR: Final[pathlib.Path] = pathlib.Path(
    os.environ.get(
        "CENSUS_AUTONOMY_STATE_DIR",
        "/var/lib/akki/census_autonomy",
    )
)

RESPONSE_REQUIRED_DIR: Final[pathlib.Path] = _CENSUS_STATE_DIR / "response_required"


# ---------------------------------------------------------------------------
# Exception classes
# ---------------------------------------------------------------------------


class ItemNotFound(Exception):
    """Raised by resolve when item_id does not exist on the cursor."""


class InvalidResolvedState(Exception):
    """Raised by resolve when resolved_state is not in the closed vocab."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_dir() -> None:
    RESPONSE_REQUIRED_DIR.mkdir(parents=True, exist_ok=True)


def _item_path(item_id: str) -> pathlib.Path:
    return RESPONSE_REQUIRED_DIR / f"{item_id}.json"


def _atomic_write(path: pathlib.Path, payload: Dict[str, Any]) -> None:
    """Atomic write via tempfile in same dir + rename (POSIX atomic on
    same filesystem)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
    tmp.replace(path)


def _read_item(item_id: str) -> Dict[str, Any]:
    path = _item_path(item_id)
    if not path.exists():
        raise ItemNotFound(f"response-required item {item_id!r} not found")
    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# Public callables
# ---------------------------------------------------------------------------


def bank_response_required_item(
    *,
    census_run_id: str,
    tenant_id: str,
    reason_text: str,
    refusal_code: str,
    decision_timestamp_utc: str,
) -> str:
    """Bank a new response-required item into the queue. Returns the
    generated `item_id`. Item is banked in state PENDING per closed
    vocab."""
    _ensure_dir()
    item_id = f"rri-{uuid.uuid4().hex[:16]}"
    banked_at = _now_utc_iso()
    payload = {
        "item_id": item_id,
        "state": "PENDING",
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "reason_text": reason_text,
        "refusal_code": refusal_code,
        "decision_timestamp_utc": decision_timestamp_utc,
        "banked_at_utc": banked_at,
        # resolution fields are None until resolve() is called
        "resolver_id": None,
        "resolution_text": None,
        "resolved_at_utc": None,
    }
    _atomic_write(_item_path(item_id), payload)
    return item_id


def list_pending_response_required_items() -> List[Dict[str, Any]]:
    """Return the list of PENDING items sorted by banked_at_utc
    ascending. Resolved items are NOT surfaced by this API."""
    _ensure_dir()
    items: List[Dict[str, Any]] = []
    for path in RESPONSE_REQUIRED_DIR.glob("*.json"):
        try:
            payload = json.loads(path.read_text())
        except (OSError, ValueError):
            # Skip malformed files; sealed engine's cursor pattern is to
            # never crash on transient FS states.
            continue
        if payload.get("state") == "PENDING":
            items.append(payload)
    items.sort(key=lambda x: x.get("banked_at_utc", ""))
    return items


def resolve_response_required_item(
    *,
    item_id: str,
    resolver_id: str,
    resolution_text: str,
    resolved_state: str,
) -> Dict[str, Any]:
    """Transition an item from PENDING to a resolved state per closed
    vocab. Raises ItemNotFound if item_id is unknown; raises
    InvalidResolvedState if resolved_state is not in
    {RESOLVED_ACCEPTED, RESOLVED_REJECTED}. Returns the resolved item
    payload."""
    if resolved_state not in _VALID_RESOLVED_TARGETS:
        raise InvalidResolvedState(
            f"resolved_state must be one of {sorted(_VALID_RESOLVED_TARGETS)}, "
            f"got {resolved_state!r}"
        )
    payload = _read_item(item_id)
    payload["state"] = resolved_state
    payload["resolver_id"] = resolver_id
    payload["resolution_text"] = resolution_text
    payload["resolved_at_utc"] = _now_utc_iso()
    _atomic_write(_item_path(item_id), payload)
    return payload
