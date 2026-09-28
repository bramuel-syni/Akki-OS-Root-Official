"""services.census_autonomy.producer_bridge — PHASE 3 continuation
A''''-cont-A · engine-integration LITE.

Owner directive 2026-09-22T~19:58Z (verbatim, this-slice authority):

  "close Phase 3 with an END-TO-END EXIT PROOF, curl-evidenced in the
  next report — one sequence on AKKI-TEST: (1) POST
  /api/portal/census/run (JWT) → run id; (2) poll GET .../runs/{id}/state
  showing real state-code progression to completion; (3) a
  blocked/deferred slice banks a response-required item via the
  adapter producer, visible on GET .../response-required-items with
  its actionable unblock text; (4) resolve it via POST .../resolve;
  (5) GPU-spend block shows CAPTURED with real host data; (6) census
  result visible on the registry read surface."

## Design (SO §3.8 additive-only · SO §6.4 NOTHING-BEYOND)

The sealed `services.census_autonomy.engine.run_bounded_census` writes
refusal rows to `<CENSUS_STATE_DIR>/refusal_rows/*.json` via its sealed
`_write_refusal_row` helper. Under §3.8 the engine STAYS SEALED — no
edits to `engine.py`, no new imports inside it, no override of
`_write_refusal_row`.

This bridge is a NEW additive carrier that:
1. Reads (never mutates) the sealed engine's public constants
   (`CENSUS_STATE_DIR`, `REFUSAL_ROWS_SUBDIR`) — those constants are
   ALREADY exported by the sealed engine (see `engine.py:39-47`) so no
   engine change is required.
2. Scans refusal rows for a given `census_run_id` via a deterministic
   filename glob.
3. Maps each refusal_code (member of sealed
   `REFUSAL_PATH_CLOSED_VOCAB`) to an owner-answerable unblock action
   (member of sealed A''''
   `UNBLOCK_ACTION_CLASS_CODES`) via a total mapping frozen as a
   module-level Final constant (invariant 3 verifies totality).
4. Banks each row into the sealed A'''-cont-A response-required queue
   via the sealed A'''' adapter's `emit_data_source_producer_items`
   public callable ONLY. Zero engine internals imported; zero direct
   queue-cursor writes.

The producer bridge exists to close the FIRST REAL PRODUCER path
described by the A'''' owner directive: engine's blocked/deferred rows
now surface into the A'''-cont-A queue as owner-answerable items with
actionable unblock text carried in the sealed queue's `reason_text`
field via the A'''' marker prefix.

## Public callables

- `scan_engine_refusal_rows_for_run(census_run_id) -> tuple[dict, ...]`
  — read the sealed engine's refusal cursor for a single run. Sorted
  by filename (deterministic). Returns `()` when no rows exist.
- `bank_refusal_rows_via_adapter(census_run_id, tenant_id, driver)
  -> tuple[str, ...]` — scan + bank via
  `emit_data_source_producer_items`. Refuses unknown drivers
  (fail-loud). Returns the tuple of banked item_ids (oldest-first).

## Owner-answerable action templates (verbatim mapping)

`REFUSAL_TO_UNBLOCK_ACTION_MAP` maps every code in
`REFUSAL_PATH_CLOSED_VOCAB` to `(action_class, detail_template)` where
`action_class` is a member of `UNBLOCK_ACTION_CLASS_CODES` and
`detail_template` is a Python .format() string with named placeholders
`{tenant_id}`, `{census_run_id}`, `{detail}`. The template is
interpolated at bank time with the sealed refusal row's verbatim
values so the actionable owner-answerable text carries the exact
context the sealed engine produced. NEVER fabricates numbers, NEVER
paraphrases the sealed engine's `detail` — the template always ends
with the engine's verbatim `{detail}` suffix.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, Final, Mapping, Tuple

from services.census_autonomy.data_source_adapter import (
    DATA_SOURCE_ADAPTER_DRIVER_CODES,
    UNBLOCK_ACTION_CLASS_CODES,
    emit_data_source_producer_items,
)
from services.census_autonomy.engine import (
    CENSUS_STATE_DIR,
    REFUSAL_ROWS_SUBDIR,
)
from services.census_autonomy.service_shape import REFUSAL_PATH_CLOSED_VOCAB


# ---------------------------------------------------------------------------
# Refusal-code → unblock-action mapping (total across sealed vocab).
# Every action_class MUST be in UNBLOCK_ACTION_CLASS_CODES (sealed A'''').
# ---------------------------------------------------------------------------

REFUSAL_TO_UNBLOCK_ACTION_MAP: Final[Mapping[str, Tuple[str, str]]] = {
    "BLOCKED_SURFACE_UNREACHABLE": (
        "iam_grant",
        (
            "grant read access on the source that refused the census for "
            "tenant {tenant_id} · census_run_id={census_run_id} · "
            "engine detail: {detail}"
        ),
    ),
    "DEFERRED_GPU_HOST_UNREACHABLE": (
        "host_reachability",
        (
            "restore SSH reachability to the GPU host that refused nvidia-smi "
            "for tenant {tenant_id} · census_run_id={census_run_id} · "
            "engine detail: {detail}"
        ),
    ),
    "BLOCKED_AWAITING_RESPONSE": (
        "credential_drop",
        (
            "answer the mid-run decision the engine banked for tenant "
            "{tenant_id} · census_run_id={census_run_id} · engine detail: "
            "{detail}"
        ),
    ),
    "BLOCKED_LAWFUL_BASIS_MISSING": (
        "credential_drop",
        (
            "drop a LawfulBasisAdmit ref pre-first-byte for tenant "
            "{tenant_id} · census_run_id={census_run_id} · engine detail: "
            "{detail}"
        ),
    ),
    "BLOCKED_TENANT_SCOPE_MISMATCH": (
        "iam_grant",
        (
            "admit tenant {tenant_id} to CENSUS_ADMITTED_TENANT_IDS · "
            "census_run_id={census_run_id} · engine detail: {detail}"
        ),
    ),
    "DEFERRED_BUDGET_EXCEEDED": (
        "host_reachability",
        (
            "raise CENSUS_SCHEDULER_JOB_MAX_SEC or shard the run for tenant "
            "{tenant_id} · census_run_id={census_run_id} · engine detail: "
            "{detail}"
        ),
    ),
}


# Assertion at import time: the map must be total across the sealed
# vocab. This mirrors invariant 3 — but as an import-time fail-loud so
# the pod refuses to boot with a stale bridge module.
_MAP_KEYS = frozenset(REFUSAL_TO_UNBLOCK_ACTION_MAP.keys())
_VOCAB_KEYS = frozenset(REFUSAL_PATH_CLOSED_VOCAB)
if _MAP_KEYS != _VOCAB_KEYS:
    raise RuntimeError(
        "producer_bridge.REFUSAL_TO_UNBLOCK_ACTION_MAP not total across "
        f"sealed REFUSAL_PATH_CLOSED_VOCAB · missing={sorted(_VOCAB_KEYS - _MAP_KEYS)!r} · "
        f"extra={sorted(_MAP_KEYS - _VOCAB_KEYS)!r}"
    )
for _code, (_cls, _tmpl) in REFUSAL_TO_UNBLOCK_ACTION_MAP.items():
    if _cls not in UNBLOCK_ACTION_CLASS_CODES:
        raise RuntimeError(
            f"producer_bridge mapping[{_code!r}].action_class {_cls!r} "
            f"not in sealed A'''' UNBLOCK_ACTION_CLASS_CODES {UNBLOCK_ACTION_CLASS_CODES!r}"
        )


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------


def scan_engine_refusal_rows_for_run(census_run_id: str) -> Tuple[Dict[str, Any], ...]:
    """Read (never mutate) the sealed engine's refusal_rows cursor for
    a single `census_run_id`. Returns a deterministic tuple sorted by
    filename (which the sealed engine writes with a UTC timestamp
    prefix so the order is chronological).
    """
    cursor_dir = CENSUS_STATE_DIR / REFUSAL_ROWS_SUBDIR
    if not cursor_dir.exists():
        return ()
    rows: list[Dict[str, Any]] = []
    for path in sorted(cursor_dir.glob(f"*{census_run_id}*.json")):
        try:
            rows.append(json.loads(path.read_text()))
        except Exception:  # noqa: BLE001  degradation-honesty
            # Malformed rows are skipped; bridge remains additive.
            continue
    return tuple(rows)


# ---------------------------------------------------------------------------
# Bank scanner output into sealed queue via sealed adapter
# ---------------------------------------------------------------------------


def bank_refusal_rows_via_adapter(
    *,
    census_run_id: str,
    tenant_id: str,
    driver: str,
) -> Tuple[str, ...]:
    """Scan the sealed engine's refusal cursor for `census_run_id` and
    bank each row into the sealed response-required queue via the
    sealed adapter's `emit_data_source_producer_items` public callable.

    Refuses `driver` not in :data:`DATA_SOURCE_ADAPTER_DRIVER_CODES`
    (fail-loud; zero rows leak into the queue).

    Returns the tuple of banked ``item_id`` strings, oldest-first.
    """
    if driver not in DATA_SOURCE_ADAPTER_DRIVER_CODES:
        raise ValueError(
            f"driver {driver!r} not in "
            f"{DATA_SOURCE_ADAPTER_DRIVER_CODES!r}"
        )

    refusal_rows = scan_engine_refusal_rows_for_run(census_run_id)
    if not refusal_rows:
        return ()

    producer_rows: list[Dict[str, Any]] = []
    for row in refusal_rows:
        refusal_code = row.get("refusal_code")
        if refusal_code not in REFUSAL_TO_UNBLOCK_ACTION_MAP:
            # Sealed engine emitted an out-of-vocab code — refuse the
            # entire bridge call (all-or-nothing) so downstream never
            # sees a partial bank. This should never happen given the
            # sealed engine's own vocab guard, but the discipline is
            # defence-in-depth.
            raise ValueError(
                f"engine refusal row carries out-of-vocab refusal_code "
                f"{refusal_code!r} · sealed vocab is "
                f"{REFUSAL_PATH_CLOSED_VOCAB!r}"
            )
        action_class, template = REFUSAL_TO_UNBLOCK_ACTION_MAP[refusal_code]
        action_detail = template.format(
            tenant_id=tenant_id,
            census_run_id=census_run_id,
            detail=row.get("detail", ""),
        )
        producer_rows.append(
            {
                "state_code": refusal_code,
                "detail": row.get("detail", ""),
                "unblock_action_class": action_class,
                "unblock_action_detail": action_detail,
                "decision_timestamp_utc": row.get(
                    "banked_at_utc", ""
                ),
            }
        )

    return emit_data_source_producer_items(
        driver=driver,
        rows=producer_rows,
        census_run_id=census_run_id,
        tenant_id=tenant_id,
    )
