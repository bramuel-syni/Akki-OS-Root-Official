"""MOAC reporting is not evaluation. Missing independent measurements stay null.

Legacy SeamResult contains training telemetry, not an adopted six-criterion
protected evaluation. It cannot establish robustness, rights lineage, honesty,
or thresholds; no synthetic number is presented as a real observation.
"""
from dataclasses import asdict
from services.training_runner.ssh_seam import SeamResult

CRITERION_NAMES = ("M-a", "M-b", "M-c", "M-d", "M-e", "M-f")


def emit_six_check_card(run_id: str, seam_result: SeamResult,
                        lineage_recipe_version: str, lineage_base_model_id: str):
    return {
        "moac_card_id": f"moac/{run_id}", "run_id": run_id,
        "criteria": [{"name": name, "passed": False, "measured_value": None,
                      "measurement_status": "not_measured", "uncurated_flag": False,
                      "mocked": seam_result.mocked,
                      "threshold_note": "Independent measurement and adopted criterion mapping required."}
                     for name in CRITERION_NAMES],
        "passed_count": 0, "total_criteria": 6,
        "verdict_summary": "0 of 6 checks verified (" + ("MOCKED" if seam_result.mocked else "PARTIALLY LIVE") + ")",
        "evidence_state": "MOCKED" if seam_result.mocked else "PARTIALLY LIVE",
        "accept_for_service": False, "release_decision": "held",
        "release_reason": "INDEPENDENT_EVALUATION_AND_SEPARATE_RELEASE_REQUIRED",
        "training_observations": asdict(seam_result),
        "lineage_references": {"recipe_version": lineage_recipe_version, "base_model_id": lineage_base_model_id},
        "reference_verbatim": "No model enters service without clearing all six MOAC criteria on uncurated held-out material, with no human in the acceptance path.",
    }