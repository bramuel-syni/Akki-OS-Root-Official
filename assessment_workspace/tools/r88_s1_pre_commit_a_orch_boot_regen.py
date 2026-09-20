"""R-88 first slice · pre-Commit-A ORCH_BOOT.md ratchet-only regen.

M16-W3 corrected order · ratchet advances first (ORCH_BOOT ratchet block
must match live baseline_failures.json) then Commit-A opens with the
updated ratchet in scope.

Regenerates:
- notes/ORCH_BOOT.md ratchet block: passed_floor 5651 → 5662 ·
  counts_at_baseline_passed 5651 → 5662 · baseline_failures_sha256
  ccb45068... → ecf7fabe... (wait: was c0af7a31 · now ecf7fabe).
- generated_at_utc + regeneration_reason updated.
- POD audit mirror /app/frontend/public/audit/ORCH_BOOT.md
  byte-identically synced via shutil.copyfile.

heads_last_sealed block is UNCHANGED at this pre-Commit-A regen
(advances at Commit-C fixup per R-6 boundary regen precedent).

Deterministic · idempotent (skips ratchet update if passed_floor
already equals R88_S1_NEW_FLOOR).

Standing bounds: zero push · zero remote · zero network · zero
subprocess · zero git ops. Pure local Path.read_text +
Path.write_text + shutil.copyfile.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R88_S1_NEW_FLOOR = 5662
R88_S1_NEW_BASELINE_SHA256 = "ecf7fabe4dba1b32f8817a6e8eb908e8990e00e292c880f921a346c3afd55286"
R88_S1_OLD_FLOOR = 5651
R88_S1_OLD_BASELINE_SHA256 = "c0af7a314841e78af4507149539e3f59892ace811bf15a5afce527878b65bbb7"
NEW_UTC = "2026-09-20T21:37:00Z"
NEW_REGEN_REASON = (
    "r88-first-slice-pre-commit-a-ratchet-only-regen-cp-content-registry-wave-"
    "section-2-and-3-con-1-to-con-11-advancing-passed-floor-5651-to-5662-plus-"
    "new-baseline-failures-sha256-under-m16-w3-corrected-order"
)


def regen_orch_boot_ratchet_only() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    # Idempotency guard: if passed_floor already == R88_S1_NEW_FLOOR, skip
    # the ratchet block rewrite (still update generated_at_utc + reason).
    ratchet_block_pattern = re.compile(
        r"ratchet:\n"
        r"  passed_floor: (\d+)\n"
        r"  counts_at_baseline_passed: (\d+)\n"
        r"  baseline_failures_path_rel: [^\n]+\n"
        r"  baseline_failures_sha256: [0-9a-f]{64}",
        re.MULTILINE,
    )
    m = ratchet_block_pattern.search(text)
    if not m:
        raise SystemExit("Could not locate ratchet block in ORCH_BOOT.md")

    current_floor = int(m.group(1))
    if current_floor == R88_S1_NEW_FLOOR:
        print(f"Idempotent skip: ratchet already at floor {R88_S1_NEW_FLOOR}.")
    else:
        # Verify we're advancing from the expected old floor.
        assert current_floor == R88_S1_OLD_FLOOR, (
            f"Unexpected current floor {current_floor} · expected {R88_S1_OLD_FLOOR}"
        )
        new_ratchet_block = (
            f"ratchet:\n"
            f"  passed_floor: {R88_S1_NEW_FLOOR}\n"
            f"  counts_at_baseline_passed: {R88_S1_NEW_FLOOR}\n"
            f"  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json\n"
            f"  baseline_failures_sha256: {R88_S1_NEW_BASELINE_SHA256}"
        )
        text = ratchet_block_pattern.sub(new_ratchet_block, text, count=1)

    # Update generated_at_utc + regeneration_reason
    text = re.sub(
        r"^generated_at_utc:.*$",
        f"generated_at_utc: {NEW_UTC}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^regeneration_reason:.*$",
        f"regeneration_reason: {NEW_REGEN_REASON}",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)


def main() -> None:
    regen_orch_boot_ratchet_only()
    print(f"passed_floor + counts_at_baseline_passed → {R88_S1_NEW_FLOOR}")
    print(f"baseline_failures_sha256 → {R88_S1_NEW_BASELINE_SHA256}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
