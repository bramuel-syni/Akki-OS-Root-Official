"""R-89 pre-Commit-A: ORCH_BOOT ratchet-only regen per M16-W3 corrected order.

Bumps passed_floor + counts_at_baseline_passed 5668 → 5678 in ORCH_BOOT.md
and syncs POD audit mirror byte-identically. heads_last_sealed unchanged
(advances at Commit-C fixup per R-6 boundary regen precedent).

Delta components:
  + 10 CON-12..CON-21 property invariants (Content Registry Spec v1 §4
    The Resolver + §5 The Slot Model / Salience)
  = +10 monotonic-up per CCS2 both fields bumped together
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
    STATE_ROOT
    / "repos"
    / "Extraction-Akki"
    / "backend"
    / "tests"
    / "invariants"
    / "baseline_failures.json"
)

NEW_PASSED_FLOOR = 5678
NEW_UTC = "2026-09-20T22:36:00Z"
NEW_REGEN_REASON = (
    "r89-pre-commit-a-ratchet-only-regen-cp-content-registry-wave-second-slice-"
    "advancing-passed-floor-5668-to-5678-plus-new-baseline-failures-sha256-under-"
    "m16-w3-corrected-order"
)


def new_baseline_sha256() -> str:
    return hashlib.sha256(BASELINE_JSON.read_bytes()).hexdigest()


def regen_orch_boot() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    sha = new_baseline_sha256()

    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {NEW_REGEN_REASON}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  passed_floor: \d+$", f"  passed_floor: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  counts_at_baseline_passed: \d+$", f"  counts_at_baseline_passed: {NEW_PASSED_FLOOR}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  baseline_failures_sha256: [0-9a-f]+$", f"  baseline_failures_sha256: {sha}", text, count=1, flags=re.MULTILINE)

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)

    print(f"baseline_failures.json sha256: {sha}")
    print(f"ratchet passed_floor: {NEW_PASSED_FLOOR}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    regen_orch_boot()
