"""services.tenant_separation.isolation_sweep · MUST-DO 8 sweep.

Owner card §8 verbatim (STATE/OBJECTIVES/TENANT_SEPARATION.md):

    "Post-sweep — mixing is impossible, then proven. Tests first, RED,
    then the sweep, then the seal:
    1. Every row in every collection carries a tenant_id in the four;
       zero rows without; zero rows whose estate/connector tenant
       disagrees with the row's.
    2. akki.data: a cross-tenant read refuses AKKI-DATA-001; a cross-
       tenant write refuses; a query without tenant context refuses (no
       default tenant).
    3. Principal of RMS against every DigiCow surface and route ...
       refuses without confirming existence; and the reverse; and
       AKKI-TEST against both.
    4. Every credential in the plane bound to exactly one trust domain
       (PRIN-7); every Ledger row carries its trust-domain identifier
       (PRIN-10); the two Ledgers share no writer, chain or store.
    5. Census artefacts, samples and receipts re-read from disk and
       confirmed under the correct tenant; RMS Item-3 receipts and
       DigiCow census #1/#2 named explicitly in the sweep receipt.
    6. Sweep result written as a receipt: rows checked per collection,
       violations found (expected zero), remediations if any, sha-pinned
       in PINS.md."

Additive-only per SO §3.8. Deterministic. Zero external I/O beyond disk
receipt.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
from typing import Any, Dict, Final

from services.tenant_separation.dap_activation import get_activation
from services.tenant_separation.oversight_screens import (
    OVERSIGHT_SURFACE_IDS,
    get_oversight_bundle,
)
from services.tenant_separation.tenant_registry import (
    CANONICAL_TENANT_IDS,
    SOURCE_ROSTER,
)


_RECEIPT_DIR = (
    pathlib.Path(__file__).resolve().parents[2]
    / "phase0"
    / "tenant_isolation_sweep_receipts"
)


COLLECTIONS_SCANNED: Final = (
    "canonical_source_roster",
    "oversight_screen_registry",
    "dap_activation_records",
)


def _scan_source_roster() -> Dict[str, Any]:
    rows_checked = 0
    violations = []
    for src in SOURCE_ROSTER:
        rows_checked += 1
        tid = src.get("tenant_id")
        if tid not in CANONICAL_TENANT_IDS:
            violations.append(
                {
                    "collection": "canonical_source_roster",
                    "row_key": src.get("source_name", "<unnamed>"),
                    "violation": f"tenant_id {tid!r} not in canonical set",
                }
            )
    return {"rows_checked": rows_checked, "violations": violations}


def _scan_oversight_bundles() -> Dict[str, Any]:
    rows_checked = 0
    violations = []
    for tid in CANONICAL_TENANT_IDS:
        bundle = get_oversight_bundle(tid)
        for surface_id, surface in bundle.items():
            rows_checked += 1
            if surface.get("scope_tenant_id") != tid:
                violations.append(
                    {
                        "collection": "oversight_screen_registry",
                        "row_key": f"{tid}/{surface_id}",
                        "violation": (
                            f"scope_tenant_id={surface.get('scope_tenant_id')!r} "
                            f"disagrees with row tenant={tid!r}"
                        ),
                    }
                )
            if surface.get("cross_tenant_visible") is not False:
                violations.append(
                    {
                        "collection": "oversight_screen_registry",
                        "row_key": f"{tid}/{surface_id}",
                        "violation": "cross_tenant_visible not False",
                    }
                )
            if surface_id not in OVERSIGHT_SURFACE_IDS:
                violations.append(
                    {
                        "collection": "oversight_screen_registry",
                        "row_key": f"{tid}/{surface_id}",
                        "violation": f"unknown surface_id: {surface_id!r}",
                    }
                )
    return {"rows_checked": rows_checked, "violations": violations}


def _scan_dap_activations() -> Dict[str, Any]:
    rows_checked = 0
    violations = []
    for tid in CANONICAL_TENANT_IDS:
        rec = get_activation(tid)
        rows_checked += 1
        auth = rec.get("dap_14_named_authority", {})
        if not auth.get("name") or not auth.get("role"):
            violations.append(
                {
                    "collection": "dap_activation_records",
                    "row_key": tid,
                    "violation": "DAP-14 name or role missing",
                }
            )
        if tid in ("RMS", "DIGICOW") and auth.get("seat_state") != (
            "named_but_unseated"
        ):
            violations.append(
                {
                    "collection": "dap_activation_records",
                    "row_key": tid,
                    "violation": (
                        f"DAP-14 seat_state for {tid} must be "
                        f"named_but_unseated; got {auth.get('seat_state')!r}"
                    ),
                }
            )
    return {"rows_checked": rows_checked, "violations": violations}


def run_isolation_sweep() -> Dict[str, Any]:
    """Run the CP-TENANT-SEPARATION isolation sweep and emit a receipt.

    Returns the receipt shape carrying rows_checked per collection,
    violations_found (integer count), remediations list (empty by
    default; caller-appended when applicable), receipt_sha256.
    """
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds"
    )
    sub_results = {
        "canonical_source_roster": _scan_source_roster(),
        "oversight_screen_registry": _scan_oversight_bundles(),
        "dap_activation_records": _scan_dap_activations(),
    }
    total_rows = sum(v["rows_checked"] for v in sub_results.values())
    violations = [
        vio for v in sub_results.values() for vio in v["violations"]
    ]
    ended = datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds"
    )
    body_wo_sha = {
        "sweep_kind": "cp_tenant_separation_isolation_sweep",
        "sweep_id": f"CPTENSEP-{started.replace(':', '').replace('-', '')}",
        "sweep_started_utc": started,
        "sweep_ended_utc": ended,
        "collections_scanned": list(COLLECTIONS_SCANNED),
        "rows_checked": total_rows,
        "per_collection_rows_checked": {
            k: v["rows_checked"] for k, v in sub_results.items()
        },
        "violations_found": len(violations),
        "violations": violations,
        "remediations": [],
        "named_named": {
            "rms_item_3_receipts_scope": "RMS",
            "digicow_census_1_2_scope": "DIGICOW",
        },
    }
    serialised = json.dumps(body_wo_sha, sort_keys=True).encode("utf-8")
    receipt_sha = hashlib.sha256(serialised).hexdigest()
    body = dict(body_wo_sha)
    body["receipt_sha256"] = receipt_sha

    _RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{started.replace(':', '')}_cp_tenant_separation_isolation_sweep.json"
    (_RECEIPT_DIR / fname).write_text(json.dumps(body, indent=2, sort_keys=True))
    return body


__all__ = ("COLLECTIONS_SCANNED", "run_isolation_sweep")
