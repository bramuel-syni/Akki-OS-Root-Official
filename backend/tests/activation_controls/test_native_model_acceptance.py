"""Native MOAC mapping tests: numerical fixtures only, no model execution."""
import copy
import pytest
from services.activation.model_proofs import FIELDS, EvaluationStandard, CriterionSpec, check_criteria
from services.northena.execution_models import Held


def evaluation_fixture():
    spec=EvaluationStandard(standard_ref="a"*64,held_out_manifest_sha256="b"*64,fixed_epoch=100,
        criteria=tuple(CriterionSpec(criterion_id="criterion-"+str(i),native_field=f,threshold="0.5",unit="TEST-unit",method="TEST-method")
                       for i,f in enumerate(FIELDS)))
    card={"candidate_model_id":"TEST-adapter","evidence_source_kind":"uncurated_registry_sample",
          "training_lineage_resolved":True,"training_lineage_note":"SYNTHETIC lineage","computed_at":"2026-01-01T00:00:00Z"}
    rows=[]
    for i,f in enumerate(FIELDS):
        value=0.1 if f in FIELDS[-2:] else 0.9
        card[f]={"measured_value":value,"floor_value":0.5,"unit":"TEST-unit","method_of_measurement":"TEST-method","canon_anchor":"TEST"}
        rows.append({"criterion_id":"criterion-"+str(i),"measured_value":value,"threshold":0.5,"outcome":"met"})
    return spec,{"acceptance_standard_ref":"a"*64,"criteria":rows,"decision":"admitted"},card


def test_native_six_criteria_and_cost_latency_direction():
    spec,accept,card=evaluation_fixture()
    check_criteria(spec,accept,card)


@pytest.mark.parametrize("defect",["lineage_unresolved","missing_native_purpose"])
def test_missing_native_proof_or_lineage_never_admits(defect):
    spec,accept,card=evaluation_fixture()
    if defect=="lineage_unresolved":
        card["training_lineage_resolved"]=False
    if defect=="missing_native_purpose":
        card["evidence_source_kind"]="uncurated_estate_sample"
        card.pop("evidence_purpose_id",None)
    with pytest.raises(Held):
        check_criteria(spec,accept,card)


@pytest.mark.parametrize("defect",["inflated_cost","false_accuracy","changed_floor","missing_floor","invented_method","NaN"])
def test_bad_or_changed_measurements_never_admit(defect):
    spec,accept,card=evaluation_fixture()
    if defect=="inflated_cost": card["cost_per_operation"]["measured_value"]=2; accept["criteria"][4]["measured_value"]=2
    if defect=="false_accuracy": card["accuracy_uncurated"]["measured_value"]=0.1; accept["criteria"][0]["measured_value"]=0.1
    if defect=="changed_floor": accept["criteria"][0]["threshold"]=0.01
    if defect=="missing_floor": card["accuracy_uncurated"]["floor_value"]=None
    if defect=="invented_method": card["accuracy_uncurated"]["method_of_measurement"]="AFTER-THE-FACT"
    if defect=="NaN": card["accuracy_uncurated"]["measured_value"]=float("nan")
    with pytest.raises(Held): check_criteria(spec,accept,card)