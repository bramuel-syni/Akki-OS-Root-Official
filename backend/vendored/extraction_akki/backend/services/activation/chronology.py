"""Temporal consistency of declarations; clocks/provenance still require real receipts."""
from datetime import datetime, timezone
from services.activation.models import issue


def parse(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def chronology_issues(d, now):
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("A timezone-aware validation instant is required.")
    errors = []
    start, end = (parse(d["identity"][k]) for k in ("run_started_at", "run_ended_at"))
    issued = parse(d["issuer"]["issued_at"])
    if not start <= end <= issued <= now.astimezone(timezone.utc):
        errors.append(issue("RUN_CHRONOLOGY_INVALID", "/identity"))
    a = d["authority"]
    for group in (a["scope"], a["expenditure"], *a["purpose_specific"]):
        for decision in group["decisions"]:
            if parse(decision["recorded_at"]) > start:
                errors.append(issue("APPROVAL_AFTER_EXECUTION", "/authority"))
    script = parse(d["evidence"]["acceptance_script"]["written_before_run_at"])
    if script >= start:
        errors.append(issue("ACCEPTANCE_SCRIPT_NOT_FROZEN_BEFORE_RUN", "/evidence/acceptance_script"))
    retrieved = parse(d["evidence"]["retrieval"]["retrieved_at"])
    if not end <= retrieved <= issued:
        errors.append(issue("RETRIEVAL_CHRONOLOGY_INVALID", "/evidence/retrieval"))
    acceptance = d["release_acceptance"]
    if acceptance["recorded_at"] and not end <= parse(acceptance["recorded_at"]) <= issued:
        errors.append(issue("ACCEPTANCE_CHRONOLOGY_INVALID", "/release_acceptance/recorded_at"))
    # Prerequisites carry record_ref, not a timestamp in the owner envelope.
    # Their actual decision times must be resolved by the evidence verifier.
    heldout = d["inputs"]["held_out_ref"]
    if heldout and parse(heldout["fixed_before_training_at"]) >= start:
        errors.append(issue("HELDOUT_NOT_FROZEN_BEFORE_RUN", "/inputs/held_out_ref"))
    return errors