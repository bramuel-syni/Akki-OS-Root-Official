"""services.watch.router — /api/watch/state (W10 CP8).

Read-only rollup of Watch surface state — verdicts + actions +
containments + reconciliations + continuity attestations + witness
attestations + tamper alarms + fitness summary. Every entry cites
its `source_path` (REFERENCE-NOT-COPY · Design Law A8).

Sources (env-overridable per test seam):
  * WATCH_VERDICTS_DIR              → phase0/watch_verdicts/
  * WATCH_ACTIONS_DIR               → phase0/watch_actions/
  * CONTAINMENTS_DIR                → phase0/containments/
  * CONTAINMENT_RECONCILIATIONS_DIR → phase0/containment_reconciliations/
  * CONTINUITY_ATTESTATIONS_DIR     → phase0/continuity_attestations/
  * WITNESS_ATTESTATIONS_DIR        → phase0/witness_attestations/
  * WITNESS_TAMPER_ALARMS_DIR       → phase0/witness_tamper_alarms/
  * WATCH_DRILL_RECEIPTS_DIR        → phase0/drill_receipts/ (fitness)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter


router = APIRouter()

_DEFAULTS = {
    "verdicts":                    "/app/assessment_workspace/phase0/watch_verdicts",
    "actions":                     "/app/assessment_workspace/phase0/watch_actions",
    "containments":                "/app/assessment_workspace/phase0/containments",
    "containment_reconciliations": "/app/assessment_workspace/phase0/containment_reconciliations",
    "continuity_attestations":     "/app/assessment_workspace/phase0/continuity_attestations",
    "witness_attestations":        "/app/assessment_workspace/phase0/witness_attestations",
    "tamper_alarms":               "/app/assessment_workspace/phase0/witness_tamper_alarms",
    "drill_receipts":              "/app/assessment_workspace/phase0/drill_receipts",
    "mirage_artifacts":            "/app/assessment_workspace/phase0/watch_mirage_artifacts",
    "marks":                       "/app/assessment_workspace/phase0/watch_marks",
}
_ENV_KEYS = {
    "verdicts":                    "WATCH_VERDICTS_DIR",
    "actions":                     "WATCH_ACTIONS_DIR",
    "containments":                "CONTAINMENTS_DIR",
    "containment_reconciliations": "CONTAINMENT_RECONCILIATIONS_DIR",
    "continuity_attestations":     "CONTINUITY_ATTESTATIONS_DIR",
    "witness_attestations":        "WITNESS_ATTESTATIONS_DIR",
    "tamper_alarms":               "WITNESS_TAMPER_ALARMS_DIR",
    "drill_receipts":              "WATCH_DRILL_RECEIPTS_DIR",
    "mirage_artifacts":            "WATCH_MIRAGE_ARTIFACTS_DIR",
    "marks":                       "WATCH_MARKS_DIR",
}
_ID_KEYS = {
    "verdicts":                    "verdict_id",
    "actions":                     "action_id",
    "containments":                "containment_id",
    "containment_reconciliations": "reconciliation_id",
    "continuity_attestations":     "attestation_id",
    "witness_attestations":        "attestation_id",
    "tamper_alarms":               "alarm_id",
    "mirage_artifacts":            "artifact_id",
    "marks":                       "mark_id",
}
_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
}


def _dir(kind: str) -> Path:
    return Path(os.environ.get(_ENV_KEYS[kind], _DEFAULTS[kind]))


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v for k, v in d.items()
        if k not in _BANNED_FIELDS and not k.endswith("_raw")
    }


def _load_kind(kind: str) -> List[Dict[str, Any]]:
    d = _dir(kind)
    if not d.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(body, dict):
            continue
        rid = body.get(_ID_KEYS[kind]) or p.stem
        entry = {"record_id": rid, **_sanitize(body), "source_path": str(p)}
        out.append(entry)
    return out


def _fitness_summary() -> Dict[str, Any]:
    """Rolls up fitness = demonstrated firings over observation window
    (Canon 8 §25-§28 · W10 CP3). We surface the counts derived from
    the same on-disk records as the fitness classifier — verdicts +
    actions + drill receipts naming a firing."""
    verdicts = _load_kind("verdicts")
    actions = _load_kind("actions")
    drill_dir = _dir("drill_receipts")
    drill_green = 0
    if drill_dir.is_dir():
        drill_green = sum(1 for p in drill_dir.glob("*_green.log"))
    return {
        "verdicts_over_window": len(verdicts),
        "actions_over_window": len(actions),
        "drill_green_receipts_on_record": drill_green,
        "ruling_1_precondition_b_demonstrated": (drill_dir / "ruling_1_drill_witness_note.md").exists(),
    }


@router.get("/api/watch/state")
async def get_watch_state() -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    for kind in _ENV_KEYS:
        if kind == "drill_receipts":
            continue  # rolled up under fitness
        entries = _load_kind(kind)
        body[kind] = {"count": len(entries), "entries": entries}
    body["fitness"] = _fitness_summary()
    body["sources"] = {k: str(_dir(k)) for k in _ENV_KEYS}
    body["reference_note"] = (
        "REFERENCE-NOT-COPY · Design Law A8 · every Watch entry cites "
        "its source_path on disk; raw signing material never appears "
        "on this surface (Owner Order 2026-08-25 §4). Ruling-1 "
        "precondition (b) demonstrated at W10 CP1 · see "
        "phase0/drill_receipts/ruling_1_drill_witness_note.md."
    )
    return body


# =====================================================================
# W11 C CP-C2 · Macho verdict + Mkono action HTTP surfaces
# =====================================================================
# Doc 8 §Line 28 verbatim: 'the Watch is two engines: Macho, the eyes,
# which senses and asserts and holds no powers whatsoever; and Mkono,
# the hand, which acts and holds no judgement — a deterministic
# mapping from verdict properties to actions.'
# ---------------------------------------------------------------------

from fastapi import HTTPException  # noqa: E402
from pydantic import BaseModel, ConfigDict, Field  # noqa: E402
from typing import Literal, Optional  # noqa: E402


class _VerdictInput(BaseModel):
    """HTTP boundary schema · same fields as MachoVerdict."""

    model_config = ConfigDict(extra="forbid")

    verdict_id: str = Field(..., min_length=1)
    verdict_class: Literal["externally_steerable", "structural_certainty"]
    subject_ref: str = Field(..., min_length=1)
    evidence_ref: str = Field(..., min_length=1)
    asserted_at: str = Field(..., min_length=1)
    intensity: Literal["noted", "elevated", "severe"] = Field(default="noted")
    sever_certainty_signal_id: Optional[str] = Field(default=None)


class _ActInput(BaseModel):
    """HTTP boundary schema for Mkono action request."""

    model_config = ConfigDict(extra="forbid")

    verdict_id: str = Field(..., min_length=1)
    action_id: str = Field(..., min_length=1)
    issued_at: str = Field(..., min_length=1)


class _SeverSignalInput(BaseModel):
    """HTTP boundary schema for a sever-certainty signal write."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(..., min_length=1)
    signal_kind: Literal[
        "canary_touch",
        "attestation_failure",
        "mark_hit",
        "witness_write_attempt",
        "floor_violation",
        "mirage_incrimination",
    ]
    asserted_by: str = Field(..., min_length=1)
    asserted_at: str = Field(..., min_length=1)
    evidence_ref: str = Field(..., min_length=1)


@router.post("/api/watch/verdict", status_code=201)
async def post_watch_verdict(payload: _VerdictInput) -> Dict[str, Any]:
    """Macho mints a verdict on the shared record. Doc 8 §Line 28 +
    §Line 30 + §Line 31 govern the grammar; MachoVerdict enforces."""
    from services.watch.macho import MachoVerdict, mint_macho_verdict
    from services.watch.persistence import WriteOnceViolation

    try:
        v = MachoVerdict(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        minted = mint_macho_verdict(v)
    except WriteOnceViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        # e.g. sever_certainty_signal not on record.
        raise HTTPException(status_code=422, detail=str(e))

    return minted.model_dump()


@router.post("/api/watch/act", status_code=201)
async def post_watch_act(payload: _ActInput) -> Dict[str, Any]:
    """Mkono deterministically maps a Macho verdict to an action and
    persists it. Doc 8 §Line 28 verbatim: 'a deterministic mapping
    from verdict properties to actions.'"""
    from services.watch.mkono import map_verdict_to_action, persist_action
    from services.watch.persistence import get_verdict, WriteOnceViolation

    v = get_verdict(payload.verdict_id)
    if v is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"verdict {payload.verdict_id!r} not on record. "
                "Doc 8 §Line 6 verbatim (seam law): Macho mints the "
                "verdict before Mkono acts."
            ),
        )

    try:
        action = map_verdict_to_action(
            v,
            action_id=payload.action_id,
            issued_at=payload.issued_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        persisted = persist_action(action)
    except WriteOnceViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return persisted.model_dump()


@router.post("/api/watch/sever-signal", status_code=201)
async def post_watch_sever_signal(payload: _SeverSignalInput) -> Dict[str, Any]:
    """Land a sever-certainty signal on the shared record. Membership
    in the closed six-signal registry (Doc 8 §Line 31) is enforced
    by SeverCertaintySignalV0's signal_kind Literal."""
    from contracts.sever_certainty_signal_v0 import SeverCertaintySignalV0
    from services.watch.sever_signals import append_sever_signal, WriteOnceViolation

    try:
        signal = SeverCertaintySignalV0(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        landed = append_sever_signal(signal)
    except WriteOnceViolation as e:
        raise HTTPException(status_code=409, detail=str(e))

    return landed.model_dump()



# =====================================================================
# W11 C CP-C3 · Mirage-Artifact + Mark HTTP surfaces
# =====================================================================
# Doc 8 §Line 127 (mark/dye pack), §Line 136 (bleed unrepresentable),
# §Line 183 (mirage isolation).
# ---------------------------------------------------------------------

from fastapi import Query  # noqa: E402


class _MirageArtifactInput(BaseModel):
    """HTTP boundary schema for MirageArtifactV0 write."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(..., min_length=1)
    mirage_session_id: str = Field(..., min_length=1)
    is_synthetic: Literal[True]
    synthetic_provenance: str = Field(..., min_length=1)
    production_store_leak_check: Literal["passed"]
    outward_lie_only: Literal[True]
    created_at: str = Field(..., min_length=1)


class _MarkInput(BaseModel):
    """HTTP boundary schema for MarkV0 mint request."""

    model_config = ConfigDict(extra="forbid")

    mark_id: str = Field(..., min_length=1)
    verdict_ref: str = Field(..., min_length=1)
    action_ref: str = Field(..., min_length=1)
    identity: str = Field(..., min_length=1)
    credentials: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    device_fingerprint: str = Field(..., min_length=1)
    behavioural_signature: str = Field(..., min_length=1)
    content_hashes: list = Field(..., min_length=1)
    minted_at: str = Field(..., min_length=1)


@router.post("/api/watch/mirage-artifact", status_code=201)
async def post_watch_mirage_artifact(payload: _MirageArtifactInput) -> Dict[str, Any]:
    """Land a mirage artifact in the isolated mirage store.
    Doc 8 §Line 183 verbatim: 'Mirage isolation. Synthetic state shares
    no store with production; synthetic provenance is carried
    internally on every mirage artifact.'"""
    from services.watch.mirage_artifacts import (
        write_mirage_artifact,
        WriteOnceViolation as _MAWriteOnce,
        MirageStoreBleedError,
    )

    try:
        artifact = write_mirage_artifact(payload.model_dump())
    except _MAWriteOnce as e:
        raise HTTPException(status_code=409, detail=str(e))
    except MirageStoreBleedError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return artifact.model_dump()


@router.post("/api/watch/mark", status_code=201)
async def post_watch_mark(payload: _MarkInput) -> Dict[str, Any]:
    """Mint a mark on conviction. Doc 8 §Line 127 verbatim: 'A mark —
    the dye pack — is minted on conviction and binds every dimension
    the system can observe.'"""
    from services.watch.mark import mint_mark, WriteOnceViolation as _MkWriteOnce

    try:
        mark = mint_mark(**payload.model_dump())
    except _MkWriteOnce as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        # Discriminate 'action not on record' (→404) vs grammar or
        # 'action is not a sever' (→422).
        msg = str(e).lower()
        if "not on record" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))

    return mark.model_dump()


@router.get("/api/watch/mark-hits")
async def get_watch_mark_hits(
    content_hash: str = Query(..., min_length=1),
) -> Dict[str, Any]:
    """Doc 8 §Line 127 verbatim: 'its resurfacing anywhere, ever, is a
    structural detection.' Returns every mark on record whose
    content_hashes list contains the query hash."""
    from services.watch.mark import mark_hits_for_hash

    hits = mark_hits_for_hash(content_hash)
    return {
        "content_hash": content_hash,
        "count": len(hits),
        "hits": [m.model_dump() for m in hits],
    }



# =====================================================================
# W11 C CP-C4 · Witness HTTP surfaces (§Line 170 · three components)
# =====================================================================


class _WitnessIdentityInput(BaseModel):
    """HTTP boundary for WitnessIdentity_v0 registration."""

    model_config = ConfigDict(extra="forbid")

    witness_id: str = Field(..., min_length=1, pattern=r"^wi_[a-z0-9_-]+$")
    registered_at: str = Field(..., min_length=1)
    signing_material_ref: str = Field(..., min_length=1)
    independent_of_authorities: Literal[True]
    registration_note: str = Field(..., min_length=1)


class _WitnessAttestActionInput(BaseModel):
    """HTTP boundary for peer attestation of a Mkono action digest."""

    model_config = ConfigDict(extra="forbid")

    attestation_id: str = Field(..., min_length=1, pattern=r"^wa_[a-z0-9_-]+$")
    witness_id: str = Field(..., min_length=1)
    watch_action_id: str = Field(..., min_length=1)
    attested_at: str = Field(..., min_length=1)
    attestation_note: str = Field(..., min_length=1)


class _BreakInTestInput(BaseModel):
    """HTTP boundary for the standing break-in test."""

    model_config = ConfigDict(extra="forbid")

    break_in_id: str = Field(..., min_length=1, pattern=r"^bit_[a-z0-9_-]+$")
    witness_id: str = Field(..., min_length=1)
    target_action_id: str = Field(..., min_length=1)
    at_iso: str = Field(..., min_length=1)


@router.post("/api/watch/witness/identity", status_code=201)
async def post_witness_identity(payload: _WitnessIdentityInput) -> Dict[str, Any]:
    """Register a witness identity. Doc 8 §Line 170 sentence 2 verbatim:
    'the watchdog that alarms on Watch silence holds no Watch
    credentials and lives in neither authority's deployment.'"""
    from services.watch.witness import (
        register_identity,
        WatchCredentialInNoteError,
        WatchdogIndependenceError,
    )

    try:
        w = register_identity(payload.model_dump())
    except WatchCredentialInNoteError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except WatchdogIndependenceError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return w.model_dump()


@router.post("/api/watch/witness/attest-action-digest", status_code=201)
async def post_witness_attest_action(
    payload: _WitnessAttestActionInput,
) -> Dict[str, Any]:
    """Doc 8 §Line 170 sentence 1 verbatim: 'Watch workers attest each
    other's action digests within their bound.'"""
    from services.watch.witness import attest_watch_action

    try:
        a = attest_watch_action(**payload.model_dump())
    except ValueError as e:
        msg = str(e).lower()
        if "action" in msg and "not on record" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        if "witness" in msg and "not on record" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        if "already on record" in msg:
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    return a.model_dump()


@router.post("/api/watch/witness/break-in-test", status_code=200)
async def post_witness_break_in_test(payload: _BreakInTestInput) -> Dict[str, Any]:
    """Doc 8 §Line 170 sentence 3 verbatim: 'a standing break-in test
    attempts, on schedule, to modify the Watch's own records with the
    Watch's own production credentials — and must fail.'"""
    from services.watch.witness import run_standing_break_in_test

    try:
        result = run_standing_break_in_test(**payload.model_dump())
    except ValueError as e:
        msg = str(e).lower()
        if "not on record" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    return result


# ---------- CA1-N5 · Ledger continuity (Wave E · CP-E1) ----------

class _ContinuityAttestationInput(BaseModel):
    """POST /api/watch/continuity payload · CA1-N5.

    Owner ruling 2026-08-27 (Wave E §3 verbatim): countersigner
    independent of the primary ledger writer's infrastructure
    (external-witness pattern); cadence = quarterly recorded as
    DEFAULT-class (see continuity_policy.v0.json)."""
    model_config = ConfigDict(extra="forbid")
    attestation_id: str = Field(..., min_length=1)
    attested_at: str = Field(..., min_length=1)
    attested_by: str = Field(..., min_length=1)
    attested_scope: str = Field(..., min_length=1)
    rto_target_seconds: str = Field(..., min_length=1)
    verification_mechanism: str = Field(..., min_length=1)
    witness_signature: str = Field(..., min_length=1)
    outcome: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)


@router.post("/api/watch/continuity", status_code=201)
async def post_watch_continuity(payload: _ContinuityAttestationInput) -> Dict[str, Any]:
    """CA1-N5 · fire a continuity attestation. Refuses on:
      - countersigner not registered as WitnessIdentity_v0;
      - witness `independent_of_authorities` not True (tampered record);
      - any owner-policy field still at OWNER_POLICY_PENDING;
      - overwrite of an existing attestation_id.
    """
    from services.watch.continuity import write_attestation

    try:
        a = write_attestation(payload.model_dump())
    except ValueError as e:
        msg = str(e).lower()
        if "not on record" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        if "already on record" in msg:
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    return a.model_dump()


@router.get("/api/watch/continuity")
async def get_watch_continuity() -> Dict[str, Any]:
    """CA1-N5 · list continuity attestations + the resolved policy
    anchor (cadence + cadence_class + verification_mechanism + the
    proposal-class-vs-canon-class distinction, per owner ruling).

    Wave E · CP-E6 · CA1-006 (Doc15-085) closure: response includes a
    `witness_state_line` summarising the external witness state
    (Watch's 'self-contained exception + external witness state line')."""
    from services.watch.continuity import load_attestations, load_policy
    from services.watch.witness import load_identities
    identities = load_identities()
    witness_state_line = (
        f"{len(identities)} external witness identit"
        f"{'ies' if len(identities) != 1 else 'y'} on record; "
        f"{sum(1 for w in identities if w.independent_of_authorities)} "
        f"canonically independent of Watch and governance authorities. "
        f"The Watch remains its own witness for its own records "
        f"(Doc 8 §Line 30 self-contained exception)."
    )
    rows = [_sanitize(a.model_dump()) for a in load_attestations()]
    return {
        "policy": load_policy(),
        "witness_state_line": witness_state_line,
        "attestations": rows,
        "count": len(rows),
    }

