#!/usr/bin/env python3
"""CP-SKILLS-LAYER-SERIES-CLOSE · PHASE 4 (c-vi) · baseline_failures.json bump.

Advances passed_floor 6206 -> 6218 (+12 canonical measured):
- 12 new RED-first structural pins at
  tests/invariants/test_cp_skills_layer_series_close_phase_4_c_vi.py

BL #11 respected: ensure_ascii=False to preserve historical unicode.
"""
from __future__ import annotations

import json
from pathlib import Path

BASELINE = Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json"
)

OLD_FLOOR = 6206
NEW_FLOOR = 6218
DELTA = 12

NEW_ENTRY = {
    "slice_id": "CP-SKILLS-LAYER-SERIES-CLOSE-PHASE-4-C-VI",
    "sealed_at_utc": "2026-02-23T01:05:00Z",
    "passed": NEW_FLOOR,
    "commit": "PENDING-P4-C-VI-COMMIT-A",
    "delta": DELTA,
    "canon_ref": "Doc 18 §A18 series-close + R-102 productized-or-honest-gap",
    "note": (
        "PHASE 4 (c-vi) · CP-SKILLS-LAYER-SERIES-CLOSE · Slice 5 of "
        "CP-SKILLS-LAYER chunked series · UI-visible tester walkthrough "
        "at /dap/buildskill · LIVE against sealed A18.2 persistence via "
        "public read_all() callable ONLY · NEW routers/dap_buildskill.py "
        "1 JWT-gated GET endpoint at /api/dap/buildskill/provisioning-"
        "records · NEW pages/dap/BuildSkill.jsx byte-identical twin "
        "showing honest-gap product-language when store empty and record "
        "list when populated · NEW hooks/useBuildSkillProvisioning.js "
        "poll-once + refetch hook · additive server.py mount block "
        "(spine + pod_shell + runtime byte-identical mirror pair) · "
        "additive App.js import + Route (both twins byte-identical) · "
        "12 RED-first structural pins · sealed carriers UNCHANGED per "
        "SO §3.8 · plain-product-language per SO §4 (banned tokens "
        "endpoint/manifest/ratchet/invariant/seam/hash/PID absent from "
        "user-facing surface) · data-testid discipline on every "
        "interactive element · live curl-verified 401 anonymous + 200 "
        "with JWT + screenshot-verified honest-gap render"
    ),
}


def main() -> int:
    data = json.loads(BASELINE.read_text())

    if data["counts_at_baseline"]["passed"] != OLD_FLOOR:
        raise SystemExit(
            f"counts_at_baseline.passed={data['counts_at_baseline']['passed']} "
            f"expected {OLD_FLOOR}"
        )

    data["counts_at_baseline"]["passed"] = NEW_FLOOR
    data["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_FLOOR
    data["ratchet_history"].append(NEW_ENTRY)

    # BL #11: ensure_ascii=False to preserve historical unicode chars.
    BASELINE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"baseline_failures.json bumped: {OLD_FLOOR} → {NEW_FLOOR} (+{DELTA})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
