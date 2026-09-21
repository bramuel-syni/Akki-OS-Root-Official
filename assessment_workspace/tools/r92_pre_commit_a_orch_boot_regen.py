"""R-92 (G5-v5 SFP-1..7 first slice) pre-Commit-A: ORCH_BOOT ratchet-only regen.

Bumps passed_floor + counts_at_baseline_passed 5688 → 5695 in ORCH_BOOT.md
and syncs POD audit mirror byte-identically. heads_last_sealed unchanged
(advances at Commit-C fixup per R-6 boundary regen precedent).

Delta components:
  + 7 SFP-1..7 property invariants (Security Function Policies · Ruling 5
    v5 SRR sheet rows 597-603 · rule text governs)
  = +7 monotonic-up per CCS2 both fields bumped together
"""

from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE_JSON = (
    STATE_ROOT / "repos" / "Extraction-Akki" / "backend" / "tests"
    / "invariants" / "baseline_failures.json"
)

NEW_PASSED_FLOOR = 5695
NEW_UTC = "2026-09-20T23:30:00Z"
NEW_REGEN_REASON = (
    "r92-pre-commit-a-ratchet-only-regen-cp-g5v5-sfp-1-7-first-slice-"
    "advancing-passed-floor-5688-to-5695-plus-new-baseline-failures-sha256-"
    "under-m16-w3-corrected-order-ruling-5-srr-rows-597-603"
)


def regen() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    sha = hashlib.sha256(BASELINE_JSON.read_bytes()).hexdigest()
    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {NEW_REGEN_REASON}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  passed_floor: \d+$", f"  passed_floor: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  counts_at_baseline_passed: \d+$", f"  counts_at_baseline_passed: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  baseline_failures_sha256: [0-9a-f]+$", f"  baseline_failures_sha256: {sha}", text, count=1, flags=re.MULTILINE)
    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)
    print(f"baseline_failures.json sha256: {sha}")
    print(f"ratchet passed_floor: {NEW_PASSED_FLOOR}")


if __name__ == "__main__":
    regen()
