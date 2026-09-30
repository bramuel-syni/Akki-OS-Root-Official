"""M6-T4 boundary · a permitted external-style caller invokes the provisioned DIGICOW skill through the ORDINARY boundary
(`POST /api/callable_skill/{skill_id}/query`) against the LIVE preview control plane and receives a first-class, receipted
outcome. Under owner rulings 2026-09-30 (3b/4b) no skill executor/plan is admitted, so the honest outcome today is the
receipted hold `SKILL_NATIVE_PLAN_REQUIRED` — never a fabricated answer. Also proves the M6-T5 duplicate rule on this path
(same idempotency key → same query, no duplicate effect) and the refusal edges (no key, conflicting key, anonymous, no grant,
unknown skill). Uses the existing identities from memory/test_credentials.md; creates nothing. Binding receipt:
notes/m6_execution/skill_binding_DIGICOW_*.json (tools/m6_skill_binding.py)."""
import glob
import json
import os
import re
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
DIGICOW = (os.environ.get("AKKI_DRILL_EMAIL", "demo.operator@demo.digicow.example.com"),
           os.environ.get("AKKI_DRILL_PASSWORD", "demo-digicow-operator-pw"))
RMS = (os.environ.get("AKKI_TEST_RMS_OPERATOR_EMAIL", "demo.operator@demo.rms.example.com"),
       os.environ.get("AKKI_TEST_RMS_OPERATOR_PASSWORD", "demo-operator-pw"))
CORPUS = "akki://artifact/DIGICOW/req-97999a0b46d2f51564b85dcd05d871a2/qualified-units"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
T = 150


def _binding():
    paths = sorted(glob.glob("/app/assessment_workspace/notes/m6_execution/skill_binding_DIGICOW_*.json"))
    assert paths, "run tools/m6_skill_binding.py first"
    return json.loads(open(paths[-1]).read())


def _login(email, password):
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": password}, timeout=30)
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}", "Content-Type": "application/json"}


@pytest.fixture(scope="module")
def binding():
    return _binding()


@pytest.fixture(scope="module")
def skill_id(binding):
    return binding["skill"]["skill_id"]


@pytest.fixture(scope="module")
def caller():
    return _login(*DIGICOW)


@pytest.fixture(scope="module")
def rms_operator():
    return _login(*RMS)


@pytest.fixture(scope="module")
def key():
    return "m6t4-" + uuid.uuid4().hex[:16]


def _query(skill_id, headers, key, text="Which training questions mention milk yield?"):
    h = dict(headers)
    if key is not None:
        h["Idempotency-Key"] = key
    return requests.post(f"{BASE_URL}/api/callable_skill/{skill_id}/query", headers=h, json={"query": text}, timeout=T)


class TestBinding:
    def test_binding_receipt_names_the_verified_digicow_artefact_and_the_rulings(self, binding):
        assert binding["skill"]["corpus_slice_ref"] == CORPUS
        assert binding["skill"]["corpus_sha256"] == "64a6938aa34bce613b067fce38c3ad0cd4f1ab5621297171c4932c5d6ad436aa"
        assert binding["skill"]["key_grant_id"] == binding["key_grant"]["grant_id"]
        assert (binding["key_grant"]["key_class"], binding["key_grant"]["path"], binding["key_grant"]["scope"]) == ("external", "governed_extract", "digicow_rds")
        assert binding["skill"]["floor"] == binding["key_grant"]["floor"] == "utterance"
        assert binding["rulings"]["executor"].startswith("3b HELD")
        assert "No grounded result" in binding["not_claimed"]

    def test_caller_identity_carries_exactly_the_granted_scope_tuple(self, caller, binding):
        r = requests.get(f"{BASE_URL}/api/auth/me", headers=caller, timeout=30)
        assert r.status_code == 200, r.text
        grants = [g for g in r.json()["key_grants"] if g["grant_id"] == binding["key_grant"]["grant_id"]]
        assert len(grants) == 1
        assert grants[0] == {"grant_id": binding["key_grant"]["grant_id"], "key_class": "external", "path": "governed_extract",
                             "floor": "utterance", "scope": "digicow_rds"}


class TestOrdinaryBoundary:
    def test_permitted_caller_receives_a_receipted_first_class_hold_not_a_fabricated_answer(self, skill_id, caller, key):
        r = _query(skill_id, caller, key)
        assert r.status_code == 409, r.text
        body = r.json()
        assert body["outcome"] == "held" and body["reason_code"] == "SKILL_NATIVE_PLAN_REQUIRED"
        assert body["execution_verified"] is False and body["delivery_verified"] is False
        assert body["skill_id"] == skill_id and body["query_id"].startswith("skill-query-")
        assert HEX64.match(body["intent_receipt_ref"]) and HEX64.match(body["query_sha256"])
        events = [(h["event"], h["reason_code"]) for h in body["history"]]
        assert events[0] == ("skill.query.intent", "SKILL_QUERY_INTENT_RECORDED")
        assert ("skill.query.view", "SKILL_NATIVE_PLAN_REQUIRED") in events
        assert all(HEX64.match(h["receipt_ref"]) for h in body["history"])
        assert "answer" not in body and "artifact_refs" not in body
        assert "no-store" in r.headers.get("Cache-Control", "")

    def test_duplicate_retry_with_the_same_key_creates_no_duplicate_effect(self, skill_id, caller, key):
        first = _query(skill_id, caller, key).json()
        second = _query(skill_id, caller, key).json()
        assert second["query_id"] == first["query_id"]
        assert second["intent_receipt_ref"] == first["intent_receipt_ref"]
        assert second["history"] == first["history"]

    def test_same_key_with_a_different_question_is_refused_as_a_conflict(self, skill_id, caller, key):
        r = _query(skill_id, caller, key, text="A different question under a reused key")
        assert r.status_code == 409, r.text
        assert r.json()["outcome"] == "held"
        assert r.json()["reason_code"] in {"SKILL_QUERY_IDEMPOTENCY_CONFLICT", "EXECUTION_HELD"}

    def test_query_without_idempotency_key_is_refused_before_any_effect(self, skill_id, caller):
        r = _query(skill_id, caller, None)
        assert r.status_code == 422, r.text
        assert r.json()["reason_code"] == "SKILL_QUERY_IDEMPOTENCY_REQUIRED"

    def test_intent_and_status_surfaces_restate_the_same_held_query(self, skill_id, caller, key):
        held = _query(skill_id, caller, key).json()
        r = requests.get(f"{BASE_URL}/api/callable_skill/{skill_id}/queries/{held['query_id']}", headers=caller, timeout=T)
        assert r.status_code == 200, r.text
        assert r.json()["query_id"] == held["query_id"] and r.json()["outcome"] == "held"
        assert r.json()["execution_verified"] is False
        fresh = "m6t4-" + uuid.uuid4().hex[:16]
        r = requests.post(f"{BASE_URL}/api/callable_skill/{skill_id}/query-intents", headers=caller,
                          json={"query": "Which training questions mention milk yield?", "idempotency_key": fresh}, timeout=T)
        assert r.status_code == 201, r.text
        assert r.json()["outcome"] == "held" and r.json()["reason_code"] == "SKILL_NATIVE_PLAN_REQUIRED"


class TestRefusalEdges:
    def test_anonymous_caller_is_refused(self, skill_id):
        r = requests.post(f"{BASE_URL}/api/callable_skill/{skill_id}/query", headers={"Content-Type": "application/json", "Idempotency-Key": "anon-" + uuid.uuid4().hex[:8]},
                          json={"query": "anything"}, timeout=T)
        assert r.status_code == 401, r.text

    def test_authenticated_caller_without_the_grant_is_refused_on_scope(self, skill_id, rms_operator):
        r = _query(skill_id, rms_operator, "rms-" + uuid.uuid4().hex[:8])
        assert r.status_code == 403, r.text
        assert r.json()["reason"] == "auth_scope_insufficient"

    def test_unknown_skill_is_not_found_for_the_permitted_caller(self, caller):
        r = _query(uuid.uuid4().hex, caller, "none-" + uuid.uuid4().hex[:8])
        assert r.status_code == 404, r.text
        assert r.json()["reason"] == "skill_not_found"

    def test_blank_query_is_rejected_by_the_contract(self, skill_id, caller):
        r = _query(skill_id, caller, "blank-" + uuid.uuid4().hex[:8], text="   ")
        assert r.status_code == 422, r.text
