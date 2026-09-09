#!/usr/bin/env python3
"""tools/scratch/build_models_roster.py

CP9 · W-REGISTRY-FULL-BUILD — surface campaign runs in the models roster
with owner-ruled honest-state map (2026-09-09T~12:20Z):

    sealed-clean         → "under evaluation"
    synthetic-fail-seal  → "did not complete" (or NOT SHOWN)
    pilot-v1             → "pilot"
    v2 / v2.1            → "under evaluation"

No fabricated states. Each row carries state_evidence naming the record
file that drove the state.

Output: notes/models_roster.json — consumed by
services/w_registry_full_build/routers.py:get_model_registry_full_record
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter


BASE = Path("/app/assessment_workspace")
OUT = BASE / "notes" / "models_roster.json"

# Owner-ruled honest-state map (2026-09-09T~12:20Z)
HONEST_STATE_MAP = {
    "sealed-clean": "under evaluation",
    "synthetic-fail-seal": "did not complete",
    "pilot-v1": "pilot",
    "v2": "under evaluation",
    "v2.1": "under evaluation",
    "baseline": "under evaluation",
    "solva": "under evaluation",
}


def _classify_manifest(fname: str) -> tuple[str, str]:
    """Return (version, honest_state) from filename patterns."""
    if "_v21_" in fname or "_v2.1_" in fname:
        return "v2.1", HONEST_STATE_MAP["v2.1"]
    if "_v2_" in fname:
        return "v2", HONEST_STATE_MAP["v2"]
    return "pilot-v1", HONEST_STATE_MAP["pilot-v1"]


def _classify_baseline(record: dict) -> tuple[str, str]:
    """Baselines are sealed unless flagged synthetic."""
    status = (record.get("status") or "").lower()
    if "synthetic" in status or "fail-seal" in status:
        return "synthetic-fail-seal", HONEST_STATE_MAP["synthetic-fail-seal"]
    return "sealed-clean", HONEST_STATE_MAP["sealed-clean"]


def main() -> None:
    runs: dict[str, dict] = {}

    # Campaign queue manifests
    for f in sorted((BASE / "phase0/campaign_drafts").glob("*_queue_manifest.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        version, state = _classify_manifest(f.name)
        for r in d.get("runs", []):
            rid = r.get("run_id")
            if not rid:
                continue
            row = {
                "run_id": rid,
                "run_name": r.get("run_name"),
                "campaign_id": d.get("campaign_id"),
                "version": version,
                "state": state,
                "state_evidence": str(f.relative_to(BASE)),
            }
            # Prefer higher-version rows
            if rid not in runs or (version, ) > (runs[rid]["version"], ):
                runs[rid] = row

    # Baseline lines (sealed baselines)
    for f in sorted((BASE / "phase0/baseline_lines").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        rid = d.get("run_id") or d.get("baseline_id") or d.get("name") or f.stem
        if rid in runs:
            continue
        version, state = _classify_baseline(d)
        runs[rid] = {
            "run_id": rid,
            "run_name": d.get("name") or rid,
            "campaign_id": d.get("campaign_id"),
            "version": version,
            "state": state,
            "state_evidence": str(f.relative_to(BASE)),
        }

    # Solva runs
    for f in sorted((BASE / "phase0/solva_runs").glob("run-*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        rid = d.get("run_id") or f.stem
        if rid in runs:
            continue
        runs[rid] = {
            "run_id": rid,
            "run_name": d.get("run_name") or rid,
            "campaign_id": "solva",
            "version": "solva",
            "state": HONEST_STATE_MAP["solva"],
            "state_evidence": str(f.relative_to(BASE)),
        }

    # Sort rows for deterministic output
    rows = sorted(runs.values(), key=lambda r: r["run_id"])
    version_counts = Counter(r["version"] for r in rows)
    state_counts = Counter(r["state"] for r in rows)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner_directive": (
            "2026-09-08T~06:15Z STEP 5: 77 campaign runs visible in models "
            "roster · 2026-09-09T~12:20Z CP9 honest-state map"
        ),
        "state_map_source": "owner ruling 2026-09-09T~12:20Z verbatim in DECISIONS.md",
        "state_map": HONEST_STATE_MAP,
        "count": len(rows),
        "version_counts": dict(version_counts),
        "state_counts": dict(state_counts),
        "rows": rows,
        "honest_gap": (
            None if len(rows) >= 77
            else f"Owner directive names 77 campaign runs visible; on-record union of queue manifests + baseline lines + solva runs is {len(rows)} — the {77 - len(rows)}-run delta is honestly named rather than back-filled with fabricated rows."
        ),
        "sources": [
            "phase0/campaign_drafts/*_queue_manifest.json",
            "phase0/baseline_lines/*.json",
            "phase0/solva_runs/*.json",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {OUT} · {len(rows)} unique run_ids")
    print(f"version breakdown: {dict(version_counts)}")
    print(f"state breakdown: {dict(state_counts)}")
    if payload["honest_gap"]:
        print(f"honest_gap: {payload['honest_gap']}")


if __name__ == "__main__":
    main()
