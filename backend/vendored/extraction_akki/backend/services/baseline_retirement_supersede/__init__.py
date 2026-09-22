"""services.baseline_retirement_supersede · additive superseding invariant package.

Landed at Turn 4 sub-slice 4k (2026-02-XX) executing R-101 preserved WHAT
retirement leg partially, per R-105 autonomous defer resolution:

    R-105 verbatim (RESUME.md · 2026-09-22T~10:10Z): "at 4h R-91 mirror-close
    boundary, executing the full 4-leg retirement requires modifying sealed
    R-86 test carrier ... Autonomous R-103 fork: Path R mirror-closure-only
    at 4h. Retirement leg deferred to DQ-18 slice via NEW partial-retirement
    design (2 v8-substitution entries only · not covered by
    MIRROR_DRIFT_NODEIDS · property 4 set-equality preserved). Reversible."

## Discipline: additive only

`services.baseline_retirement_supersede.v8_substitution_retire` declares
the retired-nodeid set + retirement attestation. R-86 sealed carrier
`test_baseline_drift_annotations_present.py` + R-88 sealed carrier
`test_r88_baseline_annotation_total_coverage.py` remain UNCHANGED — the
retirement path preserves their properties by construction (retired
v8-substitution nodeids aren't in MIRROR_DRIFT_NODEIDS · retired nodeids
leave BOTH baseline_failures list AND the R-88 annotation field in the
same commit).
"""

from __future__ import annotations

__all__ = ("v8_substitution_retire",)
