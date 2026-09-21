"""R-90 pre-Commit-A: ORCH_BOOT ratchet-only regen per M16-W3 corrected order."""

from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE_JSON = STATE_ROOT / "repos" / "Extraction-Akki" / "backend" / "tests" / "invariants" / "baseline_failures.json"

NEW_PASSED_FLOOR = 5688
NEW_UTC = "2026-09-20T22:51:00Z"
NEW_REGEN_REASON = (
    "r90-pre-commit-a-ratchet-only-regen-cp-content-registry-wave-third-slice-"
    "advancing-passed-floor-5678-to-5688-plus-new-baseline-failures-sha256-"
    "under-m16-w3-corrected-order-closes-ruling-4-scope"
)


def regen():
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
