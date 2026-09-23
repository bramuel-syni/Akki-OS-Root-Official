"""CP-DECK-ENGINE-DR-R4-OPENING · Phase 4 (d-i) · ratchet floor bump.

Bumps baseline_failures.json passed_floor 6218 -> 6224 (+6 canonical
measured) reflecting the 6 RED-first structural pins landed by
test_cp_deck_engine_dr_r4_opening_phase_4_d_i.py.

BL #11 respected: json.dumps writes with ensure_ascii=False to preserve
historical on-disk unicode chars verbatim (em-dash, arrow, middle-dot).
BL #7 respected: indent=2 preserved to match on-disk format.
BL #6 respected: ratchet_history entry `passed` field equals the NEW
post-seal floor (6224).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "repos"
    / "Extraction-Akki"
    / "backend"
    / "tests"
    / "invariants"
    / "baseline_failures.json"
)


def main() -> None:
    d = json.loads(BASELINE_PATH.read_text())

    old_floor = d["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
    new_floor = 6224
    assert old_floor == 6218, (
        f"expected old_floor 6218 · got {old_floor}"
    )

    # Update passed_floor + counts_at_baseline.passed atomically.
    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = new_floor
    d["counts_at_baseline"]["passed"] = new_floor
    d["recorded_at_utc"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    # Append ratchet_history entry (schema-complete per BL #6).
    history_entry = {
        "at_utc": d["recorded_at_utc"],
        "from_floor": old_floor,
        "to_floor": new_floor,
        "delta": new_floor - old_floor,
        "passed": new_floor,
        "cp": (
            "CP-DECK-ENGINE-DR-R4-OPENING · P4 (d-i) · DR-R4 DeckSpec_v0 "
            "shape-freeze OPENING slice · Master_Requirements_Registry.md "
            "line 269 truncated verbatim · source deck_engine.md UNRECOVERED "
            "(RD-16 extraction-artefact flag against DR-R10 + DR-R13) · "
            "Slice-1 minimum-viable shape: deck_id (stable-identity for "
            "DR-R2 determinism + DR-R12 metering) + spec_version "
            "(Literal['v0'] version anchor) · SO §3.10-α closed-schema "
            "discipline (frozen=True + extra='forbid' from day one) · "
            "6 RED-first structural pins at "
            "tests/invariants/test_cp_deck_engine_dr_r4_opening_phase_4_d_i.py"
        ),
        "note": (
            "6 RED-first pins landed additively per SO §3.8 · module "
            "presence + Canon anchor · snapshot parity · Slice-1 minimum-"
            "viable field set (deck_id + spec_version) · frozen=True + "
            "extra='forbid' closed-schema discipline · "
            "DR_R4_SOURCE_RESTORE_HONEST_GAP Final constant naming "
            "deck_engine.md verbatim per R-102 honest-gap discipline · "
            "CONTRACT_TO_SNAPSHOT map additive entry per BL #10. Sealed "
            "carriers UNCHANGED per SO §3.8. RED-pre 6 ImportError/"
            "assertion right-reason failures · GREEN-post 6/6 pass 0.70s."
        ),
    }
    d.setdefault("ratchet_history", []).append(history_entry)

    # BL #11: ensure_ascii=False; BL #7: indent=2 to preserve on-disk format.
    BASELINE_PATH.write_text(
        json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"baseline_failures.json bumped {old_floor} -> {new_floor}")


if __name__ == "__main__":
    main()
