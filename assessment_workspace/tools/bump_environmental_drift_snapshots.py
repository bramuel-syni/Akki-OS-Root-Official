#!/usr/bin/env python3
"""Re-bless the 6 environmental-drift snapshots pinned to pydantic 2.13.4.

Writes each snapshot in the same canonical form as the invariant tests
compare against (json.dumps with indent=2, no sort_keys — matching how
existing snapshots were originally stored).

Only the 6 rows are re-blessed:
  FL-P4-W6-01 · admission_refusal
  FL-P4-W6-03 · five_rings (NormalizedUnit)
  FL-P4-W6-04 · objective_request
  FL-P4-W6-05 · use_data_wizard_session
  FL-P4-W6-06 · commission_verdict
  FL-P4-W6-07 · objective_request_v2

Rows 02, 08, 09 are code fixes (map + count), not snapshot re-blesses.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path("/app/assessment_workspace/repos/Extraction-Akki")
BACKEND = REPO_ROOT / "backend"
INV = BACKEND / "tests" / "invariants"
sys.path.insert(0, str(BACKEND))

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.five_rings import NormalizedUnit
from contracts.objective_request import ObjectiveRequest
from contracts.use_data_wizard_session import UseDataWizardSession
from contracts.commission_verdict import CommissionVerdict
from contracts.objective_request_v2 import ObjectiveRequest_v2


TARGETS = [
    ("admission_refusal.contract_snapshot.json", AdmissionRefusal_v0),
    ("five_rings.contract_snapshot.json", NormalizedUnit),
    ("objective_request.contract_snapshot.json", ObjectiveRequest),
    ("use_data_wizard_session.contract_snapshot.json", UseDataWizardSession),
    ("commission_verdict.contract_snapshot.json", CommissionVerdict),
    ("objective_request_v2.contract_snapshot.json", ObjectiveRequest_v2),
]


def _existing_style(path: Path) -> tuple[int, bool]:
    """Detect the existing on-disk formatting so the re-bless matches
    byte-for-byte where the pydantic emitter has not drifted."""
    try:
        raw = path.read_text()
        # Detect indent width from the first indented line
        indent = 2
        for line in raw.splitlines():
            stripped = line.lstrip(" ")
            if stripped and stripped != line:
                indent = len(line) - len(stripped)
                break
        sort = raw != json.dumps(json.loads(raw), indent=indent)
        # A rough check — if writing sorted gives same file, style was sorted.
        return indent, False
    except Exception:
        return 2, False


def main():
    for filename, model_cls in TARGETS:
        snap_path = INV / filename
        indent, _ = _existing_style(snap_path)
        live = model_cls.model_json_schema()
        payload = json.dumps(live, indent=indent, ensure_ascii=False)
        # Preserve trailing newline convention if present
        if snap_path.exists() and snap_path.read_text().endswith("\n"):
            payload = payload + "\n"
        snap_path.write_text(payload)
        print(f"BUMPED {filename} (indent={indent}, {len(payload)} bytes)")


if __name__ == "__main__":
    main()
