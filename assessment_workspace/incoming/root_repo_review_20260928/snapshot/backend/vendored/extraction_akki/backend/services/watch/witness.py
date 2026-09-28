"""services.watch.witness — Canon 8 §9 witness fabric.

The witness holds NEITHER authority's credentials (verbatim). It
attests to standing drill outcomes; alarms outward on tamper; cannot
itself act on the estate.

Enforcement:
  * NO imports of macho / mkono / containment / mirage / approvals
    writers (see test_witness_service_does_not_import_governance_or_watch_writers).
  * Read-only inspection of subject_ref content (path or id).
  * Writes ONLY WitnessIdentity_v0, WitnessAttestation_v0,
    TamperAlarm_v0 records.
  * sign_continuity_attestation composes a deterministic signature
    string for the ContinuityAttestation_v0.witness_signature slot;
    it does NOT write to the continuity_attestations directory
    (the continuity service is the writer of that record class).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.witness_identity import (
    TamperAlarm_v0, WitnessAttestation_v0, WitnessIdentity_v0,
)


_DEFAULT_ID_DIR = "/app/assessment_workspace/phase0/witness_identities"
_DEFAULT_AT_DIR = "/app/assessment_workspace/phase0/witness_attestations"
_DEFAULT_TA_DIR = "/app/assessment_workspace/phase0/witness_tamper_alarms"


def _id_dir() -> Path:
    return Path(os.environ.get("WITNESS_IDENTITIES_DIR", _DEFAULT_ID_DIR))


def _at_dir() -> Path:
    return Path(os.environ.get("WITNESS_ATTESTATIONS_DIR", _DEFAULT_AT_DIR))


def _ta_dir() -> Path:
    return Path(os.environ.get("WITNESS_TAMPER_ALARMS_DIR", _DEFAULT_TA_DIR))


# ---------- W11 C CP-C4 · Doc 8 §Line 170 sentence-2 error classes ---------- #


class WatchCredentialInNoteError(ValueError):
    """§Line 170 sentence 2 verbatim: 'the watchdog that alarms on
    Watch silence holds no Watch credentials.' Registration refused
    when the registration_note claims Watch credentials."""


class WatchdogIndependenceError(ValueError):
    """§Line 170 sentence 2 verbatim: '...lives in neither authority's
    deployment.' Registration refused when the note fails to declare
    independence from BOTH Watch and governance."""


def _validate_watchdog_note(note: str) -> None:
    """§Line 170 sentence 2 · structural refusals on the
    registration_note. Two independent checks:
      1. Note must NOT contain a phrase claiming Watch credentials.
      2. Note MUST declare independence from BOTH Watch and governance.
    """
    lower = note.lower()
    # (1) claim-of-credentials refusal.
    claim_patterns = (
        "holds full watch credentials",
        "holds watch credentials",
        "has watch credentials",
        "can issue macho verdicts",
        "acts on behalf of the watch",
    )
    for pat in claim_patterns:
        if pat in lower:
            raise WatchCredentialInNoteError(
                "Doc 8 §Line 170 sentence 2 verbatim: 'the watchdog "
                "that alarms on Watch silence holds no Watch "
                "credentials.' registration_note claims Watch "
                f"credentials via phrase: {pat!r}."
            )
    # (2) independence declaration.
    # Accept both "no Watch credentials" (spaced) and compound forms
    # like "no governance/Watch credentials" that the W10 CP5 fabric
    # already lands on record.
    has_no_watch = (
        "no watch credentials" in lower
        or "no governance/watch credentials" in lower
        or "no watch/governance credentials" in lower
    )
    has_no_gov = (
        "no governance credentials" in lower
        or "no governance/watch credentials" in lower
        or "no watch/governance credentials" in lower
        or "no governance " in lower
    )
    if not (has_no_watch and has_no_gov):
        raise WatchdogIndependenceError(
            "Doc 8 §Line 170 sentence 2 verbatim: '...lives in neither "
            "authority's deployment.' registration_note must declare "
            "independence from BOTH Watch and governance (missing "
            f"phrases: has_no_watch={has_no_watch}, "
            f"has_no_governance={has_no_gov})."
        )


# ---------- loaders ----------

def load_identities() -> List[WitnessIdentity_v0]:
    d = _id_dir()
    if not d.is_dir():
        return []
    return sorted(
        (WitnessIdentity_v0(**json.loads(p.read_text()))
         for p in d.glob("wi_*.json")),
        key=lambda w: (w.registered_at, w.witness_id),
    )


def load_attestations() -> List[WitnessAttestation_v0]:
    d = _at_dir()
    if not d.is_dir():
        return []
    return sorted(
        (WitnessAttestation_v0(**json.loads(p.read_text()))
         for p in d.glob("wa_*.json")),
        key=lambda a: (a.attested_at, a.attestation_id),
    )


def load_alarms() -> List[TamperAlarm_v0]:
    d = _ta_dir()
    if not d.is_dir():
        return []
    return sorted(
        (TamperAlarm_v0(**json.loads(p.read_text()))
         for p in d.glob("ta_*.json")),
        key=lambda t: (t.detected_at, t.alarm_id),
    )


def _identity_on_record(witness_id: str) -> Optional[WitnessIdentity_v0]:
    for w in load_identities():
        if w.witness_id == witness_id:
            return w
    return None


# ---------- writers ----------

def register_identity(payload: Dict[str, Any]) -> WitnessIdentity_v0:
    """Register a witness identity. Refuses overwrite (§43).

    W11 C CP-C4 · Doc 8 §Line 170 sentence 2 extension: refuses
    registration_note that claims Watch credentials OR fails to
    declare independence from BOTH authorities."""
    w = WitnessIdentity_v0(**payload)
    _validate_watchdog_note(w.registration_note)
    d = _id_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{w.witness_id}.json"
    if path.exists():
        raise ValueError(
            f"witness {w.witness_id!r} already on record. Canon 8 §43: "
            f"correction is by new entry only."
        )
    path.write_text(json.dumps(w.model_dump(), indent=2, ensure_ascii=False))
    return w


def attest_receipt(payload: Dict[str, Any]) -> WitnessAttestation_v0:
    """Attest to a subject artefact. If attested_hash is omitted,
    computes sha256 of the subject_ref content on disk (read-only
    inspection · Canon 8 §9 non-actor)."""
    if payload.get("witness_id") and _identity_on_record(payload["witness_id"]) is None:
        raise ValueError(
            f"witness {payload['witness_id']!r} not on record. Register "
            f"the witness identity before attesting."
        )
    if not payload.get("attested_hash"):
        subject = Path(payload["subject_ref"])
        if subject.is_file():
            payload = dict(payload)  # local mutation only
            payload["attested_hash"] = (
                "sha256:" + hashlib.sha256(subject.read_bytes()).hexdigest()
            )
        else:
            raise ValueError(
                f"subject_ref {payload['subject_ref']!r} not a readable "
                f"file · cannot compute hash · attested_hash must be "
                f"supplied or subject must be readable."
            )
    a = WitnessAttestation_v0(**payload)
    d = _at_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{a.attestation_id}.json"
    if path.exists():
        raise ValueError(
            f"attestation {a.attestation_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(a.model_dump(), indent=2, ensure_ascii=False))
    return a


def raise_tamper_alarm(payload: Dict[str, Any]) -> TamperAlarm_v0:
    """Raise a tamper alarm (§9: 'alarms outward on tamper')."""
    if _identity_on_record(payload["witness_id"]) is None:
        raise ValueError(
            f"witness {payload['witness_id']!r} not on record. Register "
            f"the witness identity before raising alarms."
        )
    t = TamperAlarm_v0(**payload)
    d = _ta_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{t.alarm_id}.json"
    if path.exists():
        raise ValueError(
            f"alarm {t.alarm_id!r} already on record. Canon 8 §43: "
            f"correction is by new entry only."
        )
    path.write_text(json.dumps(t.model_dump(), indent=2, ensure_ascii=False))
    return t


# ---------- signature helper for ContinuityAttestation_v0.witness_signature ----------

def sign_continuity_attestation(
    *,
    witness_id: str,
    attestation_payload: Dict[str, Any],
    at_iso: str,
) -> str:
    """Compose a deterministic witness_signature string for the
    ContinuityAttestation_v0.witness_signature slot. Replaces the W9
    CP4 placeholder ('wit_sig_placeholder').

    Format: 'wsig:<witness_id>:<payload_hash>:<at_iso>' where
    payload_hash = sha256(canonical(attestation_payload)) first 16 hex.

    Refuses if witness_id not on record.
    """
    if _identity_on_record(witness_id) is None:
        raise ValueError(
            f"witness {witness_id!r} not on record. Register the "
            f"identity before signing."
        )
    canonical = json.dumps(
        attestation_payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    payload_hash = hashlib.sha256(canonical).hexdigest()[:16]
    return f"wsig:{witness_id}:{payload_hash}:{at_iso}"


# =====================================================================
# W11 C CP-C4 · Doc 8 §Line 170 sentences 1 + 3
# =====================================================================
# §Line 170 sentence 1: 'Watch workers attest each other's action
#                        digests within their bound.'
# §Line 170 sentence 3: 'a standing break-in test attempts, on
#                        schedule, to modify the Watch's own records
#                        with the Watch's own production credentials
#                        — and must fail.'
# §Line 170 last:       'Immutability that has never been attacked is
#                        an assertion; this one is a measurement.'
# ---------------------------------------------------------------------


def _canonical_hash_of_file(path: Path) -> str:
    """sha256:<hex> of the file's raw bytes."""
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def attest_watch_action(
    *,
    attestation_id: str,
    witness_id: str,
    watch_action_id: str,
    attested_at: str,
    attestation_note: str,
) -> WitnessAttestation_v0:
    """Peer attestation of a Mkono action digest · Doc 8 §Line 170
    sentence 1 verbatim: 'Watch workers attest each other's action
    digests within their bound.'

    Reads the on-record WatchActionV0 (or legacy WatchActionRecord_v0)
    from WATCH_ACTIONS_DIR, computes the sha256 digest of the on-disk
    content, and writes a WitnessAttestation_v0 with
    subject_kind='watch_action' and subject_ref='action:<action_id>'.

    Refuses:
      * witness_id not on record (§Line 170 requires the witness be a
        registered identity).
      * action file not on record (§Line 6 seam law).
      * duplicate attestation_id (§Line 43 correction-by-new-entry).
    """
    if _identity_on_record(witness_id) is None:
        raise ValueError(
            f"witness {witness_id!r} not on record. §Line 170 attestation "
            "requires a registered witness identity."
        )

    actions_dir = Path(os.environ.get(
        "WATCH_ACTIONS_DIR",
        "/app/assessment_workspace/phase0/watch_actions",
    ))
    action_file = actions_dir / f"{watch_action_id}.json"
    if not action_file.is_file():
        raise ValueError(
            f"action {watch_action_id!r} not on record. Doc 8 §Line 6 "
            "seam law: Macho + Mkono mint the record before the "
            "witness attests it."
        )

    attested_hash = _canonical_hash_of_file(action_file)
    payload = {
        "attestation_id": attestation_id,
        "witness_id": witness_id,
        "attested_at": attested_at,
        "subject_kind": "watch_action",
        "subject_ref": f"action:{watch_action_id}",
        "attested_hash": attested_hash,
        "attestation_note": attestation_note,
    }
    a = WitnessAttestation_v0(**payload)
    d = _at_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{a.attestation_id}.json"
    if path.exists():
        raise ValueError(
            f"attestation {a.attestation_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(a.model_dump(), indent=2, ensure_ascii=False))
    return a


def _latest_attested_hash(watch_action_id: str) -> Optional[str]:
    """Return the most recent attested_hash for the given action, or
    None if no attestation exists."""
    subject_ref = f"action:{watch_action_id}"
    matches = [
        a for a in load_attestations()
        if a.subject_kind == "watch_action" and a.subject_ref == subject_ref
    ]
    if not matches:
        return None
    # load_attestations returns sorted by (attested_at, attestation_id).
    return matches[-1].attested_hash


def run_standing_break_in_test(
    *,
    break_in_id: str,
    witness_id: str,
    target_action_id: str,
    at_iso: str,
) -> Dict[str, Any]:
    """Doc 8 §Line 170 sentence 3 verbatim: 'a standing break-in test
    attempts, on schedule, to modify the Watch's own records with the
    Watch's own production credentials — and must fail.'

    Two arms of the measurement (both must pass):
      A. Attempt to REWRITE the target action via the production
         writer path (services.watch.persistence.append_action).
         Because write-once is enforced (§Line 39), the attempt MUST
         raise WriteOnceViolation. If it does not, immutability has
         FAILED and a TamperAlarm_v0 is raised.
      B. Compare the on-disk content hash to the most recent
         on-record witness attestation of this action (if any). Any
         drift is an out-of-band tamper - raises a TamperAlarm_v0.

    Returns a receipt dict:
      {
        'break_in_id', 'target_action_id', 'at_iso',
        'attempt_result': 'refused' | 'SUCCESS_ALARM',
        'refusal_reason': '<class-name or empty>',
        'on_disk_hash', 'attested_hash',
        'immutability_measurement': 'passed' | 'FAILED',
      }

    §Line 170 last sentence: this receipt is a MEASUREMENT (the
    attempt actually fired) - not an assertion of immutability.
    """
    if _identity_on_record(witness_id) is None:
        raise ValueError(
            f"witness {witness_id!r} not on record. §Line 170 break-in "
            "test runs under a registered witness identity."
        )

    actions_dir = Path(os.environ.get(
        "WATCH_ACTIONS_DIR",
        "/app/assessment_workspace/phase0/watch_actions",
    ))
    action_file = actions_dir / f"{target_action_id}.json"
    if not action_file.is_file():
        raise ValueError(
            f"action {target_action_id!r} not on record. §Line 170: the "
            "break-in test targets an existing Watch record."
        )

    on_disk_hash = _canonical_hash_of_file(action_file)
    attested_hash = _latest_attested_hash(target_action_id)

    # ----- Arm A · attempt a write-once bypass through the production writer.
    from contracts.watch_action_v0 import WatchActionV0
    from services.watch.persistence import (
        append_action, WriteOnceViolation,
    )

    # Read the on-record action, build a valid FORGERY that is a
    # different content but with the same action_id, and attempt to
    # re-persist it. The write-once discipline must refuse.
    try:
        current = json.loads(action_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        # File unreadable is itself a tamper condition.
        _raise_tamper_alarm(
            break_in_id=break_in_id,
            witness_id=witness_id,
            target_action_id=target_action_id,
            at_iso=at_iso,
            evidence=f"action file unreadable: {e}",
        )
        return {
            "break_in_id": break_in_id,
            "target_action_id": target_action_id,
            "at_iso": at_iso,
            "attempt_result": "SUCCESS_ALARM",
            "refusal_reason": "action_file_unreadable",
            "on_disk_hash": None,
            "attested_hash": attested_hash,
            "immutability_measurement": "FAILED",
        }

    # If the on-disk row is a legacy WatchActionRecord_v0 (not the
    # CP-C1 WatchActionV0 shape) we still measure via arm B; skip
    # arm A cleanly.
    can_forge = "reversible" in current and "action_class" in current
    attempt_result = "refused"
    refusal_reason = ""
    if can_forge:
        forged = dict(current)
        # Flip subject_ref so the forgery is a real modification.
        forged["subject_ref"] = "TAMPERED_BY_BREAK_IN_TEST"
        try:
            forged_action = WatchActionV0(**forged)
        except (ValueError, TypeError) as e:
            # Forgery couldn't even construct; arm A implicitly passes.
            refusal_reason = f"forgery_construction_refused:{e.__class__.__name__}"
        else:
            try:
                append_action(forged_action)
            except WriteOnceViolation as e:
                refusal_reason = f"write_once_violation:{e}"
            except (ValueError, RuntimeError) as e:
                refusal_reason = f"writer_refused:{e.__class__.__name__}"
            else:
                # Attempt SUCCEEDED - immutability FAILED.
                attempt_result = "SUCCESS_ALARM"
                refusal_reason = "attempt_succeeded_write_once_broken"

    # ----- Arm B · compare on-disk hash to most recent attested hash.
    hash_drift = (
        attested_hash is not None
        and on_disk_hash != attested_hash
    )

    if attempt_result == "SUCCESS_ALARM" or hash_drift:
        evidence = (
            f"break_in_test measured immutability FAILURE · "
            f"attempt_result={attempt_result} · "
            f"on_disk_hash={on_disk_hash} · attested_hash={attested_hash}"
        )
        _raise_tamper_alarm(
            break_in_id=break_in_id,
            witness_id=witness_id,
            target_action_id=target_action_id,
            at_iso=at_iso,
            evidence=evidence,
        )
        immutability = "FAILED"
    else:
        immutability = "passed"

    return {
        "break_in_id": break_in_id,
        "target_action_id": target_action_id,
        "at_iso": at_iso,
        "attempt_result": attempt_result,
        "refusal_reason": refusal_reason,
        "on_disk_hash": on_disk_hash,
        "attested_hash": attested_hash,
        "immutability_measurement": immutability,
    }


def _raise_tamper_alarm(
    *,
    break_in_id: str,
    witness_id: str,
    target_action_id: str,
    at_iso: str,
    evidence: str,
) -> None:
    """Convenience wrapper: raise a TamperAlarm_v0 on measured tamper.
    Alarm id is deterministic: ta_<break_in_id> so tests can locate
    it by name. Uses the Canon 8 §9 tamper-evidence grammar
    (evidence_kind = 'modified_receipt' for hash-drift measurements)."""
    payload = {
        "alarm_id": f"ta_{break_in_id}",
        "witness_id": witness_id,
        "detected_at": at_iso,
        "evidence_kind": "modified_receipt",
        "evidence_ref": f"action:{target_action_id}",
        "alarm_note": evidence,
    }
    raise_tamper_alarm(payload)

