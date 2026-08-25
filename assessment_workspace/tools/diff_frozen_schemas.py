#!/usr/bin/env python3
"""Per-drift diff report for the 9 failing frozen contract snapshots.

Read-only analysis. Prints for each drift:
  * the live schema vs on-disk snapshot delta (added/removed/changed keys
    at each nested level),
  * the git blame of the model file to name the wave that likely introduced
    the drift,
  * and the parity errors (unmapped sources / orphan snapshots) so we can
    judge INTENDED-vs-UNINTENDED before deciding to bump-or-revert.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path("/app/assessment_workspace/repos/Extraction-Akki")
BACKEND = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND))

INVARIANTS_DIR = BACKEND / "tests" / "invariants"
CONTRACTS_DIR = BACKEND / "contracts"


# The six schema-based drifts (per test failure names).
DRIFTS = [
    {
        "row": "FL-P4-W6-01",
        "test": "test_admission_refusal_v0_contract_frozen",
        "snapshot": "admission_refusal.contract_snapshot.json",
        "contract_source": "contracts/admission_refusal.py",
        "model_import": "from contracts.admission_refusal import AdmissionRefusal_v0",
        "model_name": "AdmissionRefusal_v0",
    },
    {
        "row": "FL-P4-W6-02",
        "test": "test_composed_conclusion_snapshot_parity_at_18",
        "snapshot": "composed_conclusion.contract_snapshot.json",
        "contract_source": "contracts/composed_conclusion.py",
        "model_import": "from contracts.composed_conclusion import ComposedConclusion_v0",
        "model_name": "ComposedConclusion_v0",
    },
    {
        "row": "FL-P4-W6-03",
        "test": "test_five_rings_schema_frozen",
        "snapshot": "five_rings.contract_snapshot.json",
        "contract_source": "contracts/five_rings.py",
        "model_import": "from contracts.five_rings import NormalizedUnit",
        "model_name": "NormalizedUnit",
    },
    {
        "row": "FL-P4-W6-04",
        "test": "test_objective_request_schema_frozen",
        "snapshot": "objective_request.contract_snapshot.json",
        "contract_source": "contracts/objective_request.py",
        "model_import": "from contracts.objective_request import ObjectiveRequest",
        "model_name": "ObjectiveRequest",
    },
    {
        "row": "FL-P4-W6-05",
        "test": "test_use_data_wizard_session_schema_frozen",
        "snapshot": "use_data_wizard_session.contract_snapshot.json",
        "contract_source": "contracts/use_data_wizard_session.py",
        "model_import": "from contracts.use_data_wizard_session import UseDataWizardSession",
        "model_name": "UseDataWizardSession",
    },
    {
        "row": "FL-P4-W6-06",
        "test": "test_commission_verdict_schema_frozen",
        "snapshot": "commission_verdict.contract_snapshot.json",
        "contract_source": "contracts/commission_verdict.py",
        "model_import": "from contracts.commission_verdict import CommissionVerdict",
        "model_name": "CommissionVerdict",
    },
    {
        "row": "FL-P4-W6-07",
        "test": "test_objective_request_v2_contract_frozen",
        "snapshot": "objective_request_v2.contract_snapshot.json",
        "contract_source": "contracts/objective_request_v2.py",
        "model_import": "from contracts.objective_request_v2 import ObjectiveRequest_v2",
        "model_name": "ObjectiveRequest_v2",
    },
]

# Parity failures (rows 08 and 09) — the meta-tests
PARITY_DRIFTS = [
    {
        "row": "FL-P4-W6-08",
        "test": "test_every_frozen_contract_has_snapshot",
        "kind": "parity-source-unmapped",
    },
    {
        "row": "FL-P4-W6-09",
        "test": "test_every_snapshot_maps_to_a_contract",
        "kind": "parity-snapshot-orphan",
    },
]


def _load_model(module_dotted: str, cls_name: str):
    """Import model class dynamically."""
    parts = module_dotted.split(".")
    module = __import__(module_dotted, fromlist=[cls_name])
    return getattr(module, cls_name)


def _paths_walk(obj, prefix=""):
    """Enumerate JSON paths → primitive values for shallow set comparison."""
    if isinstance(obj, dict):
        yield (prefix, "<dict>", tuple(sorted(obj.keys())))
        for k, v in obj.items():
            yield from _paths_walk(v, f"{prefix}.{k}")
    elif isinstance(obj, list):
        yield (prefix, "<list>", len(obj))
        for i, item in enumerate(obj):
            yield from _paths_walk(item, f"{prefix}[{i}]")
    else:
        yield (prefix, type(obj).__name__, obj)


def _git_blame(rel_path: str) -> list[tuple[str, str, str]]:
    """Get last N commits touching the file."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--pretty=format:%h|%ai|%s", "--", rel_path],
            cwd=REPO_ROOT,
            text=True,
        )
        rows = []
        for line in out.strip().split("\n"):
            if not line:
                continue
            sha, when, summary = line.split("|", 2)
            rows.append((sha, when, summary))
        return rows
    except subprocess.CalledProcessError:
        return []


def _summarise_json_diff(actual, expected):
    """Produce a short text summary of the delta."""
    diffs = []
    actual_paths = {p: (t, v) for p, t, v in _paths_walk(actual)}
    expected_paths = {p: (t, v) for p, t, v in _paths_walk(expected)}
    added = sorted(set(actual_paths) - set(expected_paths))
    removed = sorted(set(expected_paths) - set(actual_paths))
    changed = []
    for p in sorted(set(actual_paths) & set(expected_paths)):
        if actual_paths[p] != expected_paths[p]:
            changed.append((p, expected_paths[p], actual_paths[p]))
    return {
        "added_paths": added[:30],
        "added_total": len(added),
        "removed_paths": removed[:30],
        "removed_total": len(removed),
        "changed_paths": changed[:30],
        "changed_total": len(changed),
    }


def analyse_schema_drift(drift):
    """Load live model, compare against snapshot, blame model file."""
    snap_path = INVARIANTS_DIR / drift["snapshot"]
    contract_path = BACKEND / drift["contract_source"]
    module_name = drift["contract_source"].replace("/", ".").replace(".py", "")
    model = _load_model(module_name, drift["model_name"])
    live = model.model_json_schema()
    stored = json.loads(snap_path.read_text())
    delta = _summarise_json_diff(live, stored)
    contract_blame = _git_blame(f"backend/{drift['contract_source']}")
    snap_blame = _git_blame(f"backend/tests/invariants/{drift['snapshot']}")
    return {
        "row": drift["row"],
        "test": drift["test"],
        "delta": delta,
        "contract_blame_last3": contract_blame[:3],
        "snapshot_blame_last3": snap_blame[:3],
    }


def analyse_parity():
    """Enumerate unmapped/orphan for meta-tests."""
    sys.path.insert(0, str(BACKEND / "tests"))
    from invariants.test_frozen_contract_snapshot_parity import (
        CONTRACT_TO_SNAPSHOT,
        _enumerate_contract_sources,
        _enumerate_canonical_snapshots,
    )
    disk_sources = _enumerate_contract_sources()
    disk_snaps = _enumerate_canonical_snapshots()
    mapped_sources = set(CONTRACT_TO_SNAPSHOT.keys())
    mapped_snaps = set(CONTRACT_TO_SNAPSHOT.values())
    unmapped_sources = sorted(disk_sources - mapped_sources)
    orphan_snaps = sorted(disk_snaps - mapped_snaps)
    per_unmapped_blame = {
        s: _git_blame(f"backend/contracts/{s}")[:3] for s in unmapped_sources
    }
    per_orphan_blame = {
        s: _git_blame(f"backend/tests/invariants/{s}")[:3] for s in orphan_snaps
    }
    return {
        "unmapped_sources": unmapped_sources,
        "unmapped_blame": per_unmapped_blame,
        "orphan_snapshots": orphan_snaps,
        "orphan_blame": per_orphan_blame,
    }


def main():
    out = {"schema_drifts": [], "parity": None}
    for drift in DRIFTS:
        try:
            out["schema_drifts"].append(analyse_schema_drift(drift))
        except Exception as e:
            out["schema_drifts"].append(
                {"row": drift["row"], "test": drift["test"], "error": str(e)}
            )
    try:
        out["parity"] = analyse_parity()
    except Exception as e:
        out["parity"] = {"error": str(e)}
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
