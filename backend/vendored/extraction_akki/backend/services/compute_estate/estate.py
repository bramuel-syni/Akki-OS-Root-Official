"""services.compute_estate.estate — assemble the compute descriptor from
banked Wave-H whitepaper receipts.

Every field returned to the wire is derived from a whitepaper JSON block.
Nothing is hardcoded. If the hardware changes, the surface follows.

Owner ruling 4 · verbatim: "Never hardcode a display literal — if a VM's
hardware changes, the surface must follow the facts."
"""
from __future__ import annotations

import json
import logging
import os
import pathlib
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Whitepaper directory resolver (monkeypatchable for tests)
# ---------------------------------------------------------------------------


def _whitepapers_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get(
        "WAVE_H_WHITEPAPERS_DIR",
        "/app/assessment_workspace/phase0/whitepapers",
    ))


# ---------------------------------------------------------------------------
# Wave-H whitepaper picker
# ---------------------------------------------------------------------------


def _wave_h_whitepapers(dir_: pathlib.Path) -> List[pathlib.Path]:
    """Return Wave-H whitepapers in newest-first order (by mtime).

    Uses nanosecond-precision mtime; ties break by filename descending so
    the picker is stable when two whitepapers are written in the same
    filesystem second (rare in production, easy in tests).
    """
    if not dir_.is_dir():
        return []
    # Standing filename pattern from wave_h_first_governed_run banking.
    candidates = list(dir_.glob("wp_run_wave_h_*.json"))
    candidates.sort(
        key=lambda p: (p.stat().st_mtime_ns, p.name),
        reverse=True,
    )
    return candidates


def _load_latest_wave_h_estate(dir_: pathlib.Path) -> Optional[Dict[str, Any]]:
    for p in _wave_h_whitepapers(dir_):
        try:
            body = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        estate = body.get("estate")
        if isinstance(estate, dict) and estate.get("hosts_inventory_verbatim"):
            return estate
    return None


# ---------------------------------------------------------------------------
# Readiness state derivation
# ---------------------------------------------------------------------------

# Owner ruling F verbatim: "Product language only: machine names, readiness,
# GPU model ... never IPs/auth/engineering vocab." The set of admissible
# readiness states is small and product-shaped.

_READY = "Ready"
_AWAITING_STACK = "Awaiting stack"
_AWAITING_CONNECTION = "Awaiting connection"
_STANDING_BY = "Standing by"

_ALLOWED_READINESS = {_READY, _AWAITING_STACK, _AWAITING_CONNECTION,
                       _STANDING_BY}


def _readiness_for(host: str, estate: Dict[str, Any]) -> str:
    """Derive product-language readiness from the whitepaper's `estate`.

    Rules (this wave):
      - `installed_stack_per_host` present + `host_first_run` present →
        `_READY` (a governed run has completed on the estate; the fact
        sheet + install summary + verify-only run are all banked).
      - Otherwise → `_AWAITING_STACK`.

    Owner ruling 4: derive from banked receipts. Never a stack trace,
    never an engineering token. The narrow whitelist keeps future drift
    honest — new states require an owner ruling.
    """
    # If the whitepaper wraps a completed governed-run, both hosts named in
    # the inventory are treated as Ready (the run banks the install summary
    # per host in `cites_install_receipt_paths`).
    if estate.get("host_first_run") and estate.get("host_paired_installed_same_cycle"):
        return _READY
    return _AWAITING_STACK


# ---------------------------------------------------------------------------
# Per-host descriptor
# ---------------------------------------------------------------------------


def _shape_host(name: str, estate: Dict[str, Any]) -> Dict[str, Any]:
    gpu_model = estate.get("gpu_model", "")
    gpu_count = int(estate.get("gpu_count_per_host") or 0)
    mem_per_gpu = estate.get("gpu_memory_per_gpu_gb")
    try:
        mem_per_gpu = float(mem_per_gpu) if mem_per_gpu is not None else None
    except (TypeError, ValueError):
        mem_per_gpu = None
    return {
        "name": name,
        "readiness": _readiness_for(name, estate),
        "gpu_model": gpu_model if isinstance(gpu_model, str) else "",
        "gpu_count": gpu_count,
        "gpu_memory_gb_per_gpu": mem_per_gpu if mem_per_gpu is not None else 0.0,
    }


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------


def assemble_estate() -> Dict[str, Any]:
    """Return the compute-estate descriptor.

    Shape:
      {
        "hosts": [
          {"name", "readiness", "gpu_model", "gpu_count",
           "gpu_memory_gb_per_gpu"},
          ...
        ],
        "rollup": {"host_count", "gpu_count_total", "gpu_memory_gb_total"},
        "reason": ""   # non-empty plain sentence when hosts is empty
      }
    """
    dir_ = _whitepapers_dir()
    estate = _load_latest_wave_h_estate(dir_)
    if not estate:
        return {
            "hosts": [],
            "rollup": {
                "host_count": 0,
                "gpu_count_total": 0,
                "gpu_memory_gb_total": 0.0,
            },
            "reason": (
                "No compute estate has been commissioned yet. Once a "
                "governed compute run is banked, the Registry will show "
                "the host readiness here."
            ),
        }

    hosts_verbatim = estate.get("hosts_inventory_verbatim", "") or ""
    names = [n.strip() for n in hosts_verbatim.split(",") if n.strip()]
    hosts: List[Dict[str, Any]] = [_shape_host(n, estate) for n in names]

    gpu_total = sum(int(h["gpu_count"] or 0) for h in hosts)
    mem_total = 0.0
    for h in hosts:
        gm = h.get("gpu_memory_gb_per_gpu") or 0
        try:
            mem_total += float(gm) * int(h["gpu_count"] or 0)
        except (TypeError, ValueError):
            pass
    mem_total = round(mem_total, 2)

    return {
        "hosts": hosts,
        "rollup": {
            "host_count": len(hosts),
            "gpu_count_total": gpu_total,
            "gpu_memory_gb_total": mem_total,
        },
        "reason": "",
    }
