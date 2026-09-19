#!/usr/bin/env python3
"""CP-CCS2-DAP-ENTITLEMENT-FREEZE pre-Commit-A ORCH_BOOT regen (ratchet-only).

Advances ratchet passed_floor 5502 → 5515 and refreshes baseline_failures_sha256.
Heads stay at CCS1 sealed values pending §3.3 CCS2 seal completion.
Syncs /app/frontend/public/audit/ORCH_BOOT.md byte-identically.

Additive to R-6 (b) regen trigger.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ORCH_BOOT = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE = Path("/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json")

OLD_TIME = "2026-09-19T22:30:00Z"
NEW_TIME = "2026-09-19T22:36:00Z"
OLD_RATCHET = 5502
NEW_RATCHET = 5515
OLD_BASELINE_SHA = "34b14bc7e187eb461e9d692fa62eedc86c79051521fb9b5c691158b1bbca399b"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    live_baseline_sha = _sha256(BASELINE)
    print(f"Live baseline_failures.json sha256: {live_baseline_sha}")

    body = ORCH_BOOT.read_text(encoding="utf-8")

    # generated_at_utc
    old_at = f"generated_at_utc: {OLD_TIME}"
    new_at = f"generated_at_utc: {NEW_TIME}"
    assert body.count(old_at) == 1, f"anchor not unique: {old_at!r}"
    body = body.replace(old_at, new_at)

    # generator line
    old_gen_prefix = "generator: main-agent Autopilot (CP-CCS1-C17-SEAM-BUNDLE-FREEZE Commit-C fixup"
    start = body.find(old_gen_prefix)
    assert start != -1, "generator prefix not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1
    end = end_paren + 1
    new_generator = (
        "generator: main-agent Autopilot (CP-CCS2-DAP-ENTITLEMENT-FREEZE pre-Commit-A "
        "· state master · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z "
        "verbatim + owner PROCEED ratification this-session verbatim (banked at CCS1 "
        "Commit-A banking section) · Contract Closure Wave 2 · DAP entitlement contract "
        "freeze · ratchet 5502 → 5515 · new baseline_failures.json sha256 "
        f"`{live_baseline_sha}` · heads_last_sealed.code_repo.head + state_repo.head "
        "both stay at prior CP-CCS1-C17-SEAM-BUNDLE-FREEZE Commit-A/B/C pending §3.3 "
        "CCS2 seal · MEM-R-053 CROWN BAN NOT triggered · staleness clock T-~13h remains "
        "armed)"
    )
    body = body[:start] + new_generator + body[end:]

    # regeneration_reason
    body = body.replace(
        "regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-ccs1-c17-seam-bundle-freeze-advancing-state-head-and-code-head",
        "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-ccs2-dap-entitlement-freeze-ratchet-only",
    )

    # ratchet block
    old_ratchet_block = (
        f"ratchet:\n"
        f"  passed_floor: {OLD_RATCHET}\n"
        f"  counts_at_baseline_passed: {OLD_RATCHET}\n"
        f"  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json\n"
        f"  baseline_failures_sha256: {OLD_BASELINE_SHA}\n"
    )
    new_ratchet_block = (
        f"ratchet:\n"
        f"  passed_floor: {NEW_RATCHET}\n"
        f"  counts_at_baseline_passed: {NEW_RATCHET}\n"
        f"  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json\n"
        f"  baseline_failures_sha256: {live_baseline_sha}\n"
    )
    assert old_ratchet_block in body, "ratchet block anchor not found"
    body = body.replace(old_ratchet_block, new_ratchet_block)

    ORCH_BOOT.write_text(body, encoding="utf-8")
    AUDIT.write_text(body, encoding="utf-8")
    assert _sha256(ORCH_BOOT) == _sha256(AUDIT), "byte-identity check failed"

    # Verify YAML parses.
    import re, yaml
    m = re.search(r"```yaml\n(.*?)\n```", body, re.DOTALL)
    parsed = yaml.safe_load(m.group(1))
    assert parsed["ratchet"]["passed_floor"] == NEW_RATCHET
    assert parsed["ratchet"]["baseline_failures_sha256"] == live_baseline_sha
    print(f"OK: ORCH_BOOT advanced to ratchet={NEW_RATCHET}, baseline_sha={live_baseline_sha}")
    print(f"    notes sha256: {_sha256(ORCH_BOOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
