"""tools/scratch/author_v3_substitution_rules.py

CP8 · W-REGISTRY-FULL-BUILD — re-author substitution rules against v3
rendered DOM. Owner directive 2026-09-08T~06:15Z STEP 5:

    substitution rules against v3 rendered DOM

Approach: mirror the 37 rules already banked in
phase0/harness_ground_truth/latest.json (authored against v8/v2 DOM),
validate each rule's dummyContent + anchorAncestorText literally appear
in the v3 prototype HTML body, emit
notes/v3_substitution_rules.json.

The invariant test freezes this file's shape; CP10 does the real-Chromium
rendered-DOM proof pass.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


WS = Path("/app/assessment_workspace")
V3_HTML = WS / "canon/drops/20260909/raw/RMS_AI_Prototype_standalone_v3.html"
V8_V2_LATEST = WS / "phase0/harness_ground_truth/latest.json"
OUT = WS / "notes/v3_substitution_rules.json"


def main() -> None:
    v3_body = V3_HTML.read_text(encoding="utf-8", errors="ignore")
    v3_sha = __import__("hashlib").sha256(v3_body.encode("utf-8")).hexdigest()
    v8_v2 = json.loads(V8_V2_LATEST.read_text(encoding="utf-8"))
    prior_rules = v8_v2["ground_truth"]["per_rule"]

    v3_rules: list[dict] = []
    absent_in_v3: list[dict] = []
    for r in prior_rules:
        dummy = r.get("dummyContent", "") or ""
        anchor = r.get("anchorAncestorText") or ""
        dummy_in_v3 = dummy != "" and dummy in v3_body
        anchor_in_v3 = anchor == "" or anchor in v3_body
        row = {
            "name": r["name"],
            "kind": r["kind"],
            "dummyContent": dummy,
            "anchorAncestorText": anchor or None,
            "v3_source_binding": {
                "design_id": "prototype_v3",
                "design_sha256": v3_sha,
                "design_path": str(V3_HTML.relative_to(WS)),
                "dummyContent_in_v3_body": dummy_in_v3,
                "anchorAncestorText_in_v3_body": anchor_in_v3,
                "bound_to_v3_body": dummy_in_v3 and anchor_in_v3,
            },
        }
        if dummy_in_v3 and anchor_in_v3:
            v3_rules.append(row)
        else:
            absent_in_v3.append(row)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner_directive": "2026-09-08T~06:15Z STEP 5 — substitution rules against v3 rendered DOM",
        "authored_from": {
            "prior_ground_truth": str(V8_V2_LATEST.relative_to(WS)),
            "prior_rule_count": len(prior_rules),
        },
        "v3_source": {
            "design_id": "prototype_v3",
            "path": str(V3_HTML.relative_to(WS)),
            "sha256": v3_sha,
            "body_len": len(v3_body),
        },
        "counts": {
            "rules_bound_to_v3_body": len(v3_rules),
            "rules_absent_from_v3_body": len(absent_in_v3),
            "prior_rule_count": len(prior_rules),
        },
        "rules": v3_rules,
        "absent_from_v3": absent_in_v3,
        "cp10_note": (
            "Static file-body binding proved here. Real-Chromium rendered-DOM "
            "proof happens at CP10 (harness --v3 mode)."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  rules bound to v3 body: {len(v3_rules)}")
    print(f"  rules absent from v3 body: {len(absent_in_v3)}")


if __name__ == "__main__":
    main()
