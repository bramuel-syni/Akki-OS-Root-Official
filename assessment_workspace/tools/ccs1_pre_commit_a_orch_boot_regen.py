#!/usr/bin/env python3
"""Advance notes/ORCH_BOOT.md ratchet-only pre-CCS1-Commit-A.

Also lands the ORCH_BOOT YAML defect repair inherited from W4 Commit-C fixup's
`housekeeping pickup:` phrase (`: ` in unquoted YAML value scalar) per
R-29-BOOT housekeeping-pickup precedent.

Additive to R-6 (b) regen trigger (owner ruling that mutates ratchet).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ORCH_BOOT = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE = Path("/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json")

OLD_TIME = "2026-09-19T21:25:00Z"
NEW_TIME = "2026-09-19T21:55:00Z"
OLD_RATCHET = 5491
NEW_RATCHET = 5502
OLD_BASELINE_SHA = "98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    live_baseline_sha = _sha256(BASELINE)
    print(f"Live baseline_failures.json sha256: {live_baseline_sha}")

    body = ORCH_BOOT.read_text(encoding="utf-8")

    # 1. Update generated_at_utc.
    old_at = f"generated_at_utc: {OLD_TIME}"
    new_at = f"generated_at_utc: {NEW_TIME}"
    assert old_at in body, f"anchor not found: {old_at!r}"
    assert body.count(old_at) == 1
    body = body.replace(old_at, new_at)

    # 2. Update generator line — this is a full replacement.
    #    Find the old generator line by prefix match and replace up to and
    #    including its trailing ')'.
    old_gen_prefix = "generator: main-agent Autopilot (CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-C fixup"
    start = body.find(old_gen_prefix)
    assert start != -1, "generator line prefix anchor not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1, "generator line trailing ')' not found"
    end = end_paren + 1  # include the closing ')'

    new_generator = (
        "generator: main-agent Autopilot (CP-CCS1-C17-SEAM-BUNDLE-FREEZE pre-Commit-A "
        "· state master · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z "
        "verbatim ('Seal W4 and CONTINUE DIRECTLY into CCS1 without stopping') · "
        "ratchet 5491 → 5502 · new baseline_failures.json sha256 "
        f"`{live_baseline_sha}` · heads_last_sealed.code_repo.head + state_repo.head "
        "both stay at prior CP-MEMORY-COMPACTION-V1-W4 Commit-A/B/C pending §3.3 CCS1 seal "
        "· housekeeping pickup per R-29-BOOT precedent — W4 Commit-C fixup ORCH_BOOT "
        "generator-line YAML plain-scalar defect ('housekeeping pickup' colon-space "
        "violated YAML mapping-value syntax at column 1024) reconciled by em-dash "
        "substitution · YAML now parses cleanly · MEM-R-053 CROWN BAN NOT triggered "
        "· staleness clock T-~13.7h remains armed)"
    )
    body = body[:start] + new_generator + body[end:]

    # 3. Update regeneration_reason.
    old_reason = "regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-memory-compaction-v1-w4-one-chain-integration-advancing-state-head"
    new_reason = "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-ccs1-c17-seam-bundle-freeze-ratchet-only-plus-w4-orch-boot-yaml-repair-per-r-29-boot"
    assert old_reason in body
    body = body.replace(old_reason, new_reason)

    # 4. Update ratchet block.
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

    # 5. Sync audit mirror byte-identical.
    AUDIT.write_text(body, encoding="utf-8")
    assert _sha256(ORCH_BOOT) == _sha256(AUDIT), "byte-identity check failed"

    # 6. Verify YAML still parses.
    import re
    import yaml
    m = re.search(r"```yaml\n(.*?)\n```", body, re.DOTALL)
    parsed = yaml.safe_load(m.group(1))
    assert parsed["ratchet"]["passed_floor"] == NEW_RATCHET
    assert parsed["ratchet"]["baseline_failures_sha256"] == live_baseline_sha

    print(f"OK: ORCH_BOOT advanced to ratchet={NEW_RATCHET}, baseline_sha={live_baseline_sha}")
    print(f"    notes sha256: {_sha256(ORCH_BOOT)}")
    print(f"    audit sha256: {_sha256(AUDIT)}")
    print(f"    parsed ratchet.passed_floor: {parsed['ratchet']['passed_floor']}")
    print(f"    parsed heads_last_sealed.state_repo.head: {parsed['heads_last_sealed']['state_repo']['head'][:8]}")
    print(f"    parsed heads_last_sealed.code_repo.head:  {parsed['heads_last_sealed']['code_repo']['head'][:8]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
