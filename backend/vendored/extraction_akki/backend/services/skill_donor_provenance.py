"""Doc 18 A18.8 · Skill donor-code provenance manifest.

Doc 18 §A18.8 verbatim (Wave B grounding brief · Canon-of-Record):

    'A18.8  [OPEN] Complete donor code exists; it is not in this build.
     Roughly 356 lines across RMS-IQ-Core-2 and Akki-OS-V1 implement the
     frozen provisioning contract, the per-call governance gate, and
     write-once persistence — a clean ~40% of it liftable directly.
     Build scope: the remaining contracts, the corpus-slice custody
     seam (shared with Document 17's execution layer), and a skill-files
     registry surface on the frontend, delivered inside the same W11
     envelope as the trainer runner.'

Owner ruling on this-slice (2026-02-XXT~xx:xxZ verbatim via chat):

    'One rule for the donor-code LIFT from RMS-IQ-Core-2 / Akki-OS-V1:
     lifted code enters through the same additive discipline as new
     code — cite the donor repo + path + commit in the module docstring
     (provenance per §A18.8), run the lifted surface through RED-first
     pins exactly as if authored fresh, and no donor code touches
     sealed carriers.'

This module is the SINGLE additive provenance carrier for the 356
lines of donor code that were LIFTED verbatim from RMS-IQ-Core-2 +
Akki-OS-V1 into the Extraction-Akki spine at earlier waves and are
covered by this A18.8 slice's drift-detector pins. It:

  * Names the three donor files (frozen provisioning contract, per-call
    governance gate, write-once persistence).
  * Pins each file's byte-verbatim sha256 across all three trees
    (Extraction-Akki spine + RMS-IQ-Core-2 donor + Akki-OS-V1 donor).
  * Documents the donor repos' pinned commits from STATE/PINS.md.
  * Documents the ~40% liftable-directly canon claim: this slice
    covers ~40% (356 lines lifted verbatim); the remaining ~60% is
    declared as an honest-gap for Slice 5 (buildskill UI + trainer
    runner envelope + Doc 17 execution-layer corpus-slice custody seam).

This module NEVER modifies the donor code — the drift-detector pins
in `tests/invariants/test_cp_skills_layer_a18_8_phase_4_c_iv.py`
assert byte-identity from disk each run. Any future edit to any of
the three donor files will fire right-reason RED under BASELINE_GUARD=1.

DISTINCT FROM prior CP-SKILLS-LAYER slices:
  * A18.1 (Slice 1) — `contracts/skill_provisioning_record_v0.py` NEW
    additive owner-facing frozen tuple, distinct from the donor's
    `callable_skill_provisioning_v0.CallableSkillProvisioningV0`.
  * A18.2 (Slice 2) — `services/skill_provisioning_persistence.py`
    NEW additive JSONL write-once persistence keyed on skill_id +
    corpus_slice_ref, distinct from the donor's Motor MongoDB
    persistence in `callable_skill_persistence.py`.
  * A18.3 (Slice 3) — `contracts/skill_call_governance_envelope_v0.py`
    NEW additive 7-field per-call envelope, distinct from the donor's
    `callable_skill_gate.ensure_response_carries_class` runtime wire.
  * A18.5 (Slice 3) — `services/skill_call_scope_resolver.py`
    NEW additive server-side scope resolver, distinct from the donor's
    `services.auth.key_grants.check_scope`.
  * A18.7 (sealed earlier) — `services/skill_files/` buyer-facing
    provenance chain, distinct from the donor code above.
  * A18.8 (THIS SLICE) — provenance manifest + drift-detector pins
    over the donor code that landed in the spine at earlier waves.

Donor repo pins (from STATE/PINS.md, unchanged since baseline 2026-08-14):
  * RMS-IQ-Core-2 · main · ea5aa019521eee22ad4f8ea29efdfa2af357be3b
  * Akki-OS-V1 · main · 8c361903cdd319bfdc0709de3f4392f5bfa3956b

Total lifted line count: 101 + 144 + 111 = 356 (canon §A18.8 verbatim).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Final, Tuple


# -----------------------------------------------------------------------------
# DONOR MANIFEST (Final constants · frozen at slice-freeze time)
# -----------------------------------------------------------------------------

DONOR_REPOS: Final[Tuple[str, ...]] = (
    "RMS-IQ-Core-2",
    "Akki-OS-V1",
)

# Pinned HEAD SHAs from STATE/PINS.md (verified byte-identical to the
# donor files' sha256 at each pinned commit).
DONOR_REPO_PINNED_COMMITS: Final[Dict[str, str]] = {
    "RMS-IQ-Core-2": "ea5aa019521eee22ad4f8ea29efdfa2af357be3b",
    "Akki-OS-V1": "8c361903cdd319bfdc0709de3f4392f5bfa3956b",
}

# Donor + spine share identical paths (RMS-IQ-Core-2 IS the spine's
# lineage; Extraction-Akki is a superset of RMS-IQ-Core-2 per
# STATE/PINS.md "Spine cited throughout BUILD_STRATEGY as
# Extraction-Akki (≡ RMS-IQ-Core-2 byte-identical on all shared code
# ...)").
DONOR_FILE_PATHS: Final[Tuple[str, ...]] = (
    "backend/contracts/callable_skill_provisioning_v0.py",
    "backend/services/transform_forms/callable_skill_gate.py",
    "backend/services/transform_forms/callable_skill_persistence.py",
)

# Byte-verbatim sha256 of each donor file · frozen at this slice's
# 5-commit seal time · asserted equal to disk each test run.
DONOR_FILE_SHA256_FROZEN: Final[Dict[str, str]] = {
    "backend/contracts/callable_skill_provisioning_v0.py":
        "d61a446c9ba130347320085b3de95f198c2e5bb7d1503c3af524a7b1535fa391",
    "backend/services/transform_forms/callable_skill_gate.py":
        "02d5674517a804eb93ba5c8b1ab1d64368294650294a3a32a6164396c99b3871",
    "backend/services/transform_forms/callable_skill_persistence.py":
        "0590339f1efe1bb5944aeba57037f9fa27dae71cb7eb116565f1792227a5c428",
}

# Line counts per donor file · frozen at this slice · sum == 356 per
# canon §A18.8 verbatim.
DONOR_FILE_LINE_COUNTS_FROZEN: Final[Dict[str, int]] = {
    "backend/contracts/callable_skill_provisioning_v0.py": 101,
    "backend/services/transform_forms/callable_skill_gate.py": 144,
    "backend/services/transform_forms/callable_skill_persistence.py": 111,
}

TOTAL_LIFTED_LINE_COUNT: Final[int] = 356

# Canon claim: "a clean ~40% of it liftable directly."
LIFTABLE_DIRECTLY_PERCENT: Final[int] = 40

# Remaining scope (60%) declared as honest-gap for Slice 5.
# Canon §A18.8 verbatim: "Build scope: the remaining contracts, the
# corpus-slice custody seam (shared with Document 17's execution
# layer), and a skill-files registry surface on the frontend,
# delivered inside the same W11 envelope as the trainer runner."
REMAINING_SCOPE_HONEST_GAP: Final[Tuple[str, ...]] = (
    "the remaining contracts",
    "the corpus-slice custody seam (shared with Document 17's execution layer)",
    "a skill-files registry surface on the frontend",
    "delivered inside the same W11 envelope as the trainer runner",
)


# -----------------------------------------------------------------------------
# Public callables
# -----------------------------------------------------------------------------


def spine_root() -> Path:
    """Return the repo-root path (spine).

    The provenance manifest resolves donor file paths against this root.
    """
    # This module lives at backend/services/skill_donor_provenance.py.
    return Path(__file__).resolve().parents[2]


def donor_manifest() -> Dict[str, Dict[str, object]]:
    """Return the frozen donor manifest as a plain dict (REFERENCE-NOT-COPY).

    Consumers read the manifest without mutating the module-level Final
    constants. The returned dict includes per-file paths, sha256
    fingerprints, and line counts.
    """
    return {
        "canon_ref": "Doc 18 §A18.8",
        "donor_repos": list(DONOR_REPOS),
        "donor_repo_pinned_commits": dict(DONOR_REPO_PINNED_COMMITS),
        "donor_files": [
            {
                "path": p,
                "sha256_frozen": DONOR_FILE_SHA256_FROZEN[p],
                "line_count_frozen": DONOR_FILE_LINE_COUNTS_FROZEN[p],
            }
            for p in DONOR_FILE_PATHS
        ],
        "total_lifted_line_count": TOTAL_LIFTED_LINE_COUNT,
        "liftable_directly_percent": LIFTABLE_DIRECTLY_PERCENT,
        "remaining_scope_honest_gap": list(REMAINING_SCOPE_HONEST_GAP),
    }
