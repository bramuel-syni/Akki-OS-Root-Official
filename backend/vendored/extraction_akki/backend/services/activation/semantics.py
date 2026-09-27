"""Executable consistency checks; no invented measurements, thresholds or signatures."""
from decimal import Decimal
from services.activation.models import issue
from services.activation.chronology import chronology_issues


def semantic_issues(document, *, now):
    d, errors = document, []
    if not d["inputs"]["custody_classes_in_scope"]:
        errors.append(issue("MATERIAL_SCOPE_MISSING", "/inputs/custody_classes_in_scope"))
    out, perf = d["output"], d["evidence"]["re_performance"]
    if out["manifest_row_count"] != out["denominator_count"] or sum(out["reconciliation"].values()) != out["denominator_count"]:
        errors.append(issue("UNIT_RECONCILIATION_MISMATCH", "/output"))
    if (perf["agreements"] + perf["disagreements"] != perf["sample_size"]
            or perf["sample_size"] > out["denominator_count"]
            or len(set(perf["disagreement_refs"])) != perf["disagreements"]):
        errors.append(issue("REPERFORMANCE_RECONCILIATION_MISMATCH", "/evidence/re_performance"))
    if (not perf["different_model_family"]
            or perf["second_instance_id"] == d["runtime"]["admitted_runtime_id"]):
        errors.append(issue("INDEPENDENCE_NOT_ESTABLISHED", "/evidence/re_performance"))
    dimensions = d["limits"]["dimensions"]
    keys = [(v["dimension"], v["unit"]) for v in dimensions]
    if len(keys) != len(set(keys)):
        errors.append(issue("DUPLICATE_LIMIT_DIMENSION", "/limits/dimensions"))
    if not any(v["dimension"] == "spend" for v in dimensions):
        errors.append(issue("SPEND_CEILING_MISSING", "/limits/dimensions"))
    for value in dimensions:
        if Decimal(str(value["observed"])) > Decimal(str(value["effective_limit"])):
            errors.append(issue("LIMIT_EXCEEDED", "/limits/dimensions"))
    if not d["usage"]["reservation_ref"] or not d["usage"]["reconciled_against_reservation"]:
        errors.append(issue("RESERVATION_NOT_RECONCILED", "/usage"))
    path, purposes = d["identity"]["path"], set(d["authority"]["purposes_authorised"])
    needed = {"A_source_to_registry": ({"census", "extraction"}, False),
              "B_callable_skill": ({"answering"}, True),
              "C_training_with_evaluation": ({"training", "evaluation"}, True)}
    required, all_required = needed[path]
    if not (required <= purposes if all_required else bool(required & purposes)):
        errors.append(issue("PURPOSE_NOT_AUTHORISED", "/authority/purposes_authorised"))
    groups = [d["authority"]["scope"], d["authority"]["expenditure"], *d["authority"]["purpose_specific"]]
    if len({g["group"] for g in groups}) != len(groups):
        errors.append(issue("APPROVAL_GROUPS_COLLAPSED", "/authority"))
    for group in groups:
        voters = [v["principal_id"] for v in group["decisions"]]
        if len(set(voters)) != len(voters):
            errors.append(issue("DUPLICATE_APPROVAL_VOTER", "/authority"))
    acceptance = d["release_acceptance"]
    if path == "C_training_with_evaluation":
        ids = [c["criterion_id"] for c in acceptance["criteria"]]
        if len(ids) != 6 or len(set(ids)) != 6 or not acceptance["acceptance_standard_ref"]:
            errors.append(issue("ADOPTED_SIX_CRITERIA_REQUIRED", "/release_acceptance/criteria"))
    if acceptance["decision"] == "admitted" and (not acceptance["recorded_at"] or any(
            p["outcome"] != "met" for p in acceptance["prerequisites"])):
        errors.append(issue("RELEASE_PREREQUISITES_NOT_MET", "/release_acceptance"))
    if d["supersession"]["superseded_by"] and d["state"] != "LIVE-BLOCKED":
        errors.append(issue("SUPERSEDED_CERTIFICATE_NOT_CURRENT", "/supersession"))
    errors.extend(chronology_issues(d, now))
    return tuple(errors)