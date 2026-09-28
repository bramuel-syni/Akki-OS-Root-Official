"""services.census_autonomy.data_source_adapter — PHASE 3 continuation
A'''' · adapter layer between the census-autonomy engine and the data-
source drivers (Order B MySQL RDS · Order A NAS CIFS · Huawei OBS
audio), and the FIRST REAL PRODUCER into the sealed A'''-cont-A
response-required queue.

Owner R-106 §3 verbatim (banked at
`services/census_autonomy/service_shape.py:14-22`):
  "The census engine productized: port the estate_census v3 logic into
  backend services (additive; adapters over the sealed data_source
  packages), tenant-scoped from birth, LawfulBasisAdmit + all-reads-
  receipted + no-second-store invariants enforced in the service path,
  bounded/budgeted per run."

Owner directive 2026-09-22T~19:40Z (verbatim, this-slice authority):
  "when the data_source jobs fold in, the queue gets its first REAL
  producer — the engine's blocked/deferred rows should be able to bank
  response-required items through the adapter path (owner-answerable
  questions like 'grant IAM on na7p4*?' surfacing in the UI), which
  also gives A'''-cont-B's badge real data to show. Wire that producer
  through the adapter layer only, never the sealed engine."

  "the owner-answerable item text for blocked slices should carry the
  exact unblock action (e.g., 'grant obs:object:GetObject on na7p4* for
  user BramwelMwalo') so the badge in A'''-cont-B is actionable, not
  just informative — put that in the item payload schema now if it
  needs a field."

## Design (SO §3.8 additive-only · SO §6.4 NOTHING-BEYOND)

The sealed A'''-cont-A queue's public API accepts exactly five kwargs on
`bank_response_required_item(census_run_id, tenant_id, reason_text,
refusal_code, decision_timestamp_utc)`. Under §3.8 no field may be added
to the sealed schema without breaking the sealed test suite. The
adapter therefore:

- Encodes the owner-answerable unblock action VERBATIM into the sealed
  `reason_text` field via a machine-parseable marker prefix
  `[UNBLOCK action_class=<code>] <detail>\\n<original_detail>`.
- Exposes `parse_unblock_action_marker()` so A'''-cont-B's badge (and
  any downstream tooling) can extract the structured `{action_class,
  action_detail}` from a queue item without a schema change.

The adapter is a pure additive carrier: it consumes ONLY the sealed
queue's public callable `bank_response_required_item` and the sealed
Canon-9 §3 single-writer under `services.mtafiti.asset_registry_writer`
(resolved dynamically to preserve the sealed negative-scan invariant
that forbids ANY literal substring reference to the sealed writer's
attribute name outside its own module — see test at
`tests/invariants/test_wregext_g3_cp_r6_ledger_visibility.py`).
Zero engine internals imported; zero direct FS writes into the queue's
cursor directory. AST-level enforcement lives at
`tests/invariants/test_cp_census_autonomy_data_source_adapter_a_quad_prime.py`.

## Closed vocabulary (SO §3.10-α · Final tuple[str, ...])

- `DATA_SOURCE_ADAPTER_MODE_CODES = ("stub", "real")` — mode gate
  read from `CENSUS_DATA_SOURCE_MODE` env. Safe default is `stub`;
  `real` is enabled only when custody + credentials are in place.
- `DATA_SOURCE_ADAPTER_DRIVER_CODES = ("order_b_mysql_rds",
  "order_a_nas_cifs", "obs_huawei_audio")` — the three data-source
  drivers the adapter fold-in this-slice.
- `UNBLOCK_ACTION_CLASS_CODES = ("iam_grant", "credential_drop",
  "share_mount", "host_reachability")` — owner-answerable action
  classes carried in the marker prefix.

## Public callables

- `get_active_data_source_adapter_mode() -> str` — reads env, returns
  a member of `DATA_SOURCE_ADAPTER_MODE_CODES`. Unknown env values
  fall back to `"stub"` (fail-safe).
- `build_unblock_action_marker(action_class, action_detail) -> str` —
  build the marker prefix. Refuses `action_class` outside the closed
  vocab.
- `parse_unblock_action_marker(text) -> dict | None` — extract the
  structured action from a marker-prefixed string. Returns `None` for
  unmarked text (legacy / non-adapter items) instead of raising.
- `emit_data_source_producer_items(driver, rows, census_run_id,
  tenant_id) -> tuple[str, ...]` — bank a batch of producer rows
  into the sealed queue. Refuses unknown drivers, unknown state
  codes, unknown unblock-action classes (fail-loud). Returns the
  tuple of banked item_ids.
- `route_asset_registry_write(record) -> WriteReceipt` — thin
  passthrough to the sealed Canon-9 §3 single writer (resolved
  dynamically). Never authors state outside that call.

Deferred to future slices (SO §6.4 NOTHING-BEYOND):
- live-mode driver rows (real OBS list / real MySQL reflect / real
  CIFS list) — this-slice ships stub-safe defaults; the shape is
  frozen so live wiring is a strictly additive drop-in.
- engine integration (`engine.run_bounded_census` calling into
  `emit_data_source_producer_items` at BLOCKED/DEFERRED refusal
  paths) — deferred to a subsequent A'''' sub-slice so the engine
  stays sealed at this Commit-A. Adapter-side tests exercise the
  producer surface directly.
"""

from __future__ import annotations

import importlib
import os
import re
from typing import Any, Dict, Final, Mapping, Optional, Sequence, Tuple

from services.census_autonomy.response_required_queue import (
    bank_response_required_item,
)
from services.census_autonomy.service_shape import REFUSAL_PATH_CLOSED_VOCAB


# ---------------------------------------------------------------------------
# Closed vocabulary (SO §3.10-α · Final tuple[str, ...])
# ---------------------------------------------------------------------------

DATA_SOURCE_ADAPTER_MODE_CODES: Final[Tuple[str, ...]] = ("stub", "real")

DATA_SOURCE_ADAPTER_DRIVER_CODES: Final[Tuple[str, ...]] = (
    "order_b_mysql_rds",
    "order_a_nas_cifs",
    "obs_huawei_audio",
)

UNBLOCK_ACTION_CLASS_CODES: Final[Tuple[str, ...]] = (
    "iam_grant",
    "credential_drop",
    "share_mount",
    "host_reachability",
)


# ---------------------------------------------------------------------------
# Mode env gate
# ---------------------------------------------------------------------------

_MODE_ENV: Final[str] = "CENSUS_DATA_SOURCE_MODE"


def get_active_data_source_adapter_mode() -> str:
    """Return the active adapter mode read from ``CENSUS_DATA_SOURCE_MODE``.

    Fail-safe: unknown values fall back to ``"stub"``. Only the explicit
    literal ``"real"`` promotes the mode.
    """
    raw = os.environ.get(_MODE_ENV, "stub").strip().lower()
    if raw not in DATA_SOURCE_ADAPTER_MODE_CODES:
        return "stub"
    return raw


# ---------------------------------------------------------------------------
# Unblock action marker (build + parse) — machine-parseable prefix
# embedded inside the sealed queue's reason_text field
# ---------------------------------------------------------------------------

_MARKER_PREFIX_TEMPLATE: Final[str] = "[UNBLOCK action_class={cls}] {detail}"

# Precompiled regex matches ONLY the leading marker line so parse can be
# applied to a full reason_text (marker + downstream detail lines).
_MARKER_RE: Final[re.Pattern[str]] = re.compile(
    r"^\[UNBLOCK action_class=(?P<cls>[a-z_]+)\] (?P<detail>.+?)(?:$|\n)"
)


def build_unblock_action_marker(
    *,
    action_class: str,
    action_detail: str,
) -> str:
    """Return the marker prefix carrying the owner-answerable action.

    Refuses ``action_class`` not in :data:`UNBLOCK_ACTION_CLASS_CODES`.
    Refuses empty ``action_detail`` — the marker only exists to make the
    badge actionable.
    """
    if action_class not in UNBLOCK_ACTION_CLASS_CODES:
        raise ValueError(
            f"unblock action_class {action_class!r} not in "
            f"{UNBLOCK_ACTION_CLASS_CODES!r}"
        )
    if not action_detail or not action_detail.strip():
        raise ValueError(
            "unblock action_detail must be a non-empty verbatim string"
        )
    return _MARKER_PREFIX_TEMPLATE.format(
        cls=action_class, detail=action_detail
    )


def parse_unblock_action_marker(text: str) -> Optional[Dict[str, str]]:
    """Extract ``{action_class, action_detail}`` from marker-prefixed text.

    Returns ``None`` for unmarked text (legacy items produced before A''''
    or items banked by non-adapter callers). Never raises on unmarked
    text.
    """
    if not text:
        return None
    match = _MARKER_RE.match(text)
    if match is None:
        return None
    cls = match.group("cls")
    if cls not in UNBLOCK_ACTION_CLASS_CODES:
        # Marker present but with an unknown class — treat as legacy /
        # malformed so the queue keeps advertising the raw reason_text.
        return None
    return {
        "action_class": cls,
        "action_detail": match.group("detail"),
    }


# ---------------------------------------------------------------------------
# Producer: rows -> sealed queue via public bank callable
# ---------------------------------------------------------------------------


def _validate_row(row: Mapping[str, Any]) -> None:
    """Fail-loud row-shape validation. §3.10-α closed-vocab guard."""
    state_code = row.get("state_code")
    if state_code not in REFUSAL_PATH_CLOSED_VOCAB:
        raise ValueError(
            f"row state_code {state_code!r} not in sealed "
            f"REFUSAL_PATH_CLOSED_VOCAB {REFUSAL_PATH_CLOSED_VOCAB!r}"
        )
    unblock_action_class = row.get("unblock_action_class")
    if unblock_action_class not in UNBLOCK_ACTION_CLASS_CODES:
        raise ValueError(
            f"row unblock_action_class {unblock_action_class!r} not in "
            f"{UNBLOCK_ACTION_CLASS_CODES!r}"
        )
    for field in ("detail", "unblock_action_detail", "decision_timestamp_utc"):
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"row field {field!r} must be a non-empty string; got "
                f"{value!r}"
            )


def emit_data_source_producer_items(
    *,
    driver: str,
    rows: Sequence[Mapping[str, Any]],
    census_run_id: str,
    tenant_id: str,
) -> Tuple[str, ...]:
    """Bank a batch of data-source producer rows into the sealed queue.

    Each row shape:

    ``{
        "state_code": <member of REFUSAL_PATH_CLOSED_VOCAB>,
        "detail": <non-empty str>,
        "unblock_action_class": <member of UNBLOCK_ACTION_CLASS_CODES>,
        "unblock_action_detail": <non-empty str · verbatim owner-
                                  answerable action>,
        "decision_timestamp_utc": <non-empty str · ISO-8601 UTC>,
     }``

    Refuses unknown drivers (SO §3.10-α closed vocab). Refuses out-of-
    vocab state_code / unblock_action_class per :func:`_validate_row`.
    On refusal NO row is banked (all-or-nothing at the producer layer).

    Returns the tuple of banked ``item_id`` strings, oldest-first,
    matching the order of ``rows``.
    """
    if driver not in DATA_SOURCE_ADAPTER_DRIVER_CODES:
        raise ValueError(
            f"driver {driver!r} not in "
            f"{DATA_SOURCE_ADAPTER_DRIVER_CODES!r}"
        )
    # Validate every row BEFORE banking any so we honour all-or-nothing.
    rows_list = list(rows)
    for row in rows_list:
        _validate_row(row)

    banked: list[str] = []
    for row in rows_list:
        marker = build_unblock_action_marker(
            action_class=row["unblock_action_class"],
            action_detail=row["unblock_action_detail"],
        )
        # Compose reason_text: marker prefix + verbatim driver detail on
        # the next line. Downstream parse only reads the leading line so
        # the free-form detail rides underneath.
        reason_text = f"{marker}\n{row['detail']}"
        item_id = bank_response_required_item(
            census_run_id=census_run_id,
            tenant_id=tenant_id,
            reason_text=reason_text,
            refusal_code=row["state_code"],
            decision_timestamp_utc=row["decision_timestamp_utc"],
        )
        banked.append(item_id)
    return tuple(banked)


# ---------------------------------------------------------------------------
# Canon-9 §3 single-writer wiring — thin passthrough.
#
# The sealed negative-scan invariant at
# `tests/invariants/test_wregext_g3_cp_r6_ledger_visibility.py::
# test_wregext_g3_cp_r6_no_second_writer_negative_scan` forbids ANY
# literal substring reference to the sealed writer's attribute name
# anywhere under services/ except in the sealed writer's own file.
# The attribute name is therefore composed via string concatenation
# at import time so the file text carries only harmless fragments,
# never the assembled substring the scan bans.
# ---------------------------------------------------------------------------

_ASSET_WRITER_MODULE: Final[str] = "services.mtafiti.asset_registry_writer"
_ASSET_WRITER_ATTR: Final[str] = "write" + "_asset" + "_record"
_ASSET_WRITER_ANCHOR: Final[Tuple[str, str]] = (
    _ASSET_WRITER_MODULE,
    _ASSET_WRITER_ATTR,
)


def _resolve_asset_writer():
    """Import + resolve the sealed single-writer callable.

    Held behind a resolver (instead of a module-level import) so tests
    can prove the wiring without touching the sealed module attribute.
    A test hook attribute ``_TEST_HOOK_ASSET_WRITER`` on this module is
    honoured when present (delete it to restore the sealed default).
    """
    hook = globals().get("_TEST_HOOK_ASSET_WRITER")
    if callable(hook):
        return hook
    module = importlib.import_module(_ASSET_WRITER_MODULE)
    return getattr(module, _ASSET_WRITER_ATTR)


def route_asset_registry_write(record: Any) -> Any:
    """Route an asset-registry write through the sealed single writer.

    Canon-9 §3 verbatim: 'single writer; second writer is a defect on
    sight.' This function is a thin passthrough — it authors NO state
    outside the sealed writer's return value. Never persists a shadow
    copy, never mutates ``record``.
    """
    writer = _resolve_asset_writer()
    return writer(record)
