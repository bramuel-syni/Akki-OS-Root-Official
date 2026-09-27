"""Versioned validation profile over immutable owner v1.1; never fetch remote schemas."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from services.activation.models import issue

PROFILE_ID = "akki.activation.validation/1"
MAX_BYTES = 262144
ORIGINAL_SHA = "ad848bd95e76dcf4ef71cd0e0688914632de33e68ceb4168e7ede4209ad256d2"
POLICY_SHA = "472b6369ef7059f9b451504e329605f02a8918081dbf3d5438239853ba6c8830"


def owner_artifact(name, sha):
    raw = (Path(__file__).parent / "policies" / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise RuntimeError("Activation policy custody hash mismatch.")
    return json.loads(raw)


def _profile():
    schema = deepcopy(owner_artifact("owner_certificate_v1_1.json", ORIGINAL_SHA))
    schema["$id"] = "akki://schemas/activation-validation-profile-v1"
    p = schema["properties"]
    refusal_kind = "out_of_scope_question"
    if refusal_kind not in p["evidence"]["properties"]["refusal_demonstration"]["properties"]["kind"]["enum"]:
        raise RuntimeError("Activation refusal-kind profile is incompatible with its owner schema.")
    rp = p["evidence"]["properties"]["re_performance"]["properties"]
    for name in ("agreements", "disagreements"):
        rp[name]["minimum"] = 0
    # The specific state law also applies to a real core with peripheral mocks.
    schema["allOf"].append({
        "if": {"properties": {"state": {"const": "PARTIALLY LIVE"}}},
        "then": {"properties": {
            "supersession": {"properties": {"revalidation": {"properties": {
                "blocked": {"const": False}, "triggers_fired": {"maxItems": 0}}}}},
            "evidence": {"properties": {"acceptance_script": {"properties": {"result": {"const": "pass"}}}}}
        }}})
    schema["allOf"].append({
        "if": {"properties": {"identity": {"properties": {"path": {"const": "B_callable_skill"}}}}},
        "then": {"properties": {"evidence": {"properties": {"refusal_demonstration": {
            "properties": {"kind": {"const": refusal_kind}}}}}}}})
    # Bounding a metadata envelope is separate from workload limits.
    def bound(node):
        if isinstance(node, dict):
            t = node.get("type")
            if t == "string" or isinstance(t, list) and "string" in t:
                node.setdefault("minLength", 1)
                node.setdefault("maxLength", 4096)
                if node.get("format") != "date-time":
                    node.setdefault("pattern", r"\S")
            if t == "array":
                node.setdefault("maxItems", 1000)
            for value in list(node.values()):
                bound(value)
        elif isinstance(node, list):
            for value in node:
                bound(value)
    bound(schema)
    Draft202012Validator.check_schema(schema)
    checker = FormatChecker()
    if "date-time" not in checker.checkers:
        raise RuntimeError("Activation requires the date-time format dependency.")
    return Draft202012Validator(schema, format_checker=checker)


VALIDATOR = _profile()
PROFILE_SHA = hashlib.sha256(json.dumps(VALIDATOR.schema, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
IMPLEMENTATION_SHA = hashlib.sha256(b"".join((Path(__file__).parent / name).read_bytes()
    for name in ("models.py", "schema.py", "chronology.py", "semantics.py", "evidence.py", "validation.py", "crossing.py",
                 "receipts.py", "record_shapes.py", "approvals.py", "reservations.py", "runtime_limits.py",
                 "worker_gate.py", "native_evidence.py", "native_joins.py", "issuance.py",
                 "composition.py", "timed_ports.py", "bounded_adapter.py", "decisions.py", "model_proofs.py",
                 "runtime_binding.py", "runtime_status.py", "portal_plans.py", "evaluation_joins.py", "runtime_evidence.py"))).hexdigest()


def canonical_document(document):
    if not isinstance(document, dict):
        raise ValueError("A certificate object is required.")
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    if len(encoded) > MAX_BYTES:
        raise ValueError("Certificate metadata envelope is too large.")
    return json.loads(encoded), hashlib.sha256(encoded).hexdigest()


def schema_issues(document):
    # Paths only; error.message can contain submitted values or signature text.
    return tuple(issue("SCHEMA_" + str(e.validator).upper(),
                       "/" + "/".join(str(x) for x in e.absolute_path))
                 for e in list(VALIDATOR.iter_errors(document))[:100])