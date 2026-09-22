"""v8_substitution_retire · CP-R91-RETIRE-SUPERSEDE retirement carrier.

Executes the R-101 preserved WHAT retirement leg partially: retires the
2 v8-substitution baseline entries from `baseline_failures[]` and from
the R-88 `known_r91_closure_scheduled_receipt_drift_annotations` field.

R-86 property 4 set-equality is preserved by construction because
neither retired nodeid is in `MIRROR_DRIFT_NODEIDS` (R-86 verbatim ·
frozenset of 3 mirror-drift nodeids only: ship_manifest_dod +
2 wave_g_pod_shell_frontend_mirror).

Owner card `TENANT_SEPARATION.md` + `CP_APP_JS_UNIFY.md` + RESUME.md
4j-close verbatim scope the partial-retirement to these two nodeids
only (mirror-drift retirement remains queued behind future closure of
CP-APP-JS-UNIFY per its milestone_status trajectory · SCHEDULED for
now).
"""

from __future__ import annotations

from typing import Final, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# Retired nodeid set (SO §3.10-α closed vocabulary)
# ═══════════════════════════════════════════════════════════════════════════

RETIRED_V8_SUBSTITUTION_NODEIDS: Final[Tuple[str, str]] = (
    "tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::"
    "test_every_v8_substitution_rule_binds_to_harness_rendered_dom",
    "tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::"
    "test_slot1_registry_aside_marker_present",
)

RETIREMENT_SEAL_SLICE: Final[str] = "Turn 4 sub-slice 4k"

RETIREMENT_ATTESTATION: Final = {
    "canon_ref": (
        "Owner card CP_APP_JS_UNIFY.md + TENANT_SEPARATION.md 4j-close "
        "verbatim + RESUME.md turn-queue 4k · R-101 preserved WHAT "
        "retirement leg (partial) · R-105 Path R defer at 4h + partial-"
        "retirement design at 4k."
    ),
    "so_ref": (
        "SO §3.8 additive-only (no sealed carrier modified) · SO §3.10-α "
        "closed vocabulary · SO §6.4 NOTHING-BEYOND (retirement of 2 "
        "nodeids only) · SO §6.7 seal-report-boundary · SO §7 R-6 "
        "anti-forget boot manifest regen at fixup."
    ),
    "sealed_carriers_left_unchanged": (
        "tests/invariants/test_baseline_drift_annotations_present.py "
        "(R-86 5-property enforcement · MIRROR_DRIFT_NODEIDS frozenset "
        "unchanged) · "
        "tests/invariants/test_r88_baseline_annotation_total_coverage.py "
        "(R-88 total-coverage · both properties preserved by removing "
        "retired nodeids from BOTH baseline_failures list AND R-88 "
        "annotation field in the same commit)."
    ),
    "retirement_scope": (
        "2 v8-substitution nodeids from tests/invariants/"
        "test_v8_substitution_rules_bind_to_rendered_dom.py: "
        "test_every_v8_substitution_rule_binds_to_harness_rendered_dom + "
        "test_slot1_registry_aside_marker_present. "
        "3 R-91 mirror-drift baselines retained (ship_manifest_dod + "
        "2 wave_g_pod_shell_frontend_mirror) pending CP-APP-JS-UNIFY "
        "closure."
    ),
    "property_4_preservation": (
        "MIRROR_DRIFT_NODEIDS ∩ baseline_failures set-equality holds "
        "post-retirement because the 2 retired v8-substitution nodeids "
        "are NOT in MIRROR_DRIFT_NODEIDS by definition. The intersection "
        "remains {3 mirror-drift entries} · annotations.keys() remains "
        "{3 mirror-drift entries} · set-equality preserved."
    ),
    "reversibility": (
        "Reversible: retirement can be reversed by re-adding the 2 "
        "nodeids to baseline_failures[] and the R-88 annotation field. "
        "Not expected to reverse — the retired invariants are transiently "
        "GREEN in real bytes at 4h + 4i + 4j sweeps and no known future "
        "drift is scoped for them."
    ),
}


__all__ = (
    "RETIRED_V8_SUBSTITUTION_NODEIDS",
    "RETIREMENT_ATTESTATION",
    "RETIREMENT_SEAL_SLICE",
)
