"""Learn without self-authorising (roadmap M2-T5 · Canon 8 §14 'Detection findings CIF may
metabolise' · A5.22 research loop · AC-18 proposes-never-ratifies).

A finding from the gate record is authored as a CIF proposal (learned faculty, OUT TCB), passes
the deterministic acceptance point, is routed to the L-4 research loop, grounded by citation
resolution against the record, and lands on the Decisions panel. Only two distinct estate
operators can ratify it into a VERSIONED requirement. Detectors read the ratified version from
then on and name it on every new verdict; earlier verdicts keep the version they were minted
under — nothing rewrites enforcement or history silently."""
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

GROUNDING_SEAM = "watch.learning_loop.citation_resolution"
THRESHOLD_KEYS = ("WATCH_GATE_FAST_REFUSALS", "WATCH_GATE_FAST_WINDOW_S", "WATCH_GATE_SLOW_REFUSALS", "WATCH_GATE_SLOW_WINDOW_S",
                  "WATCH_GATE_DUPLICATE_ADMITS", "WATCH_GATE_DUPLICATE_WINDOW_S", "WATCH_GATE_SHAPE_WINDOW_S", "WATCH_GATE_SHAPE_MIN_INTERVAL_S")


def _dir():
    return Path(os.environ.get("WATCH_REQUIREMENTS_DIR", "/app/assessment_workspace/phase0/watch_requirements"))


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def versions():
    d = _dir()
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("v*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            continue
    return sorted(out, key=lambda v: v["version"])


def current():
    found = versions()
    return found[-1] if found else None


def ratified_value(key):
    live = current()
    return None if live is None else live["thresholds"].get(key)


def label():
    live = current()
    return f"requirements=v{live['version']}" if live else "thresholds=DEFAULT_PENDING_OWNER_RULING"


def _effective_thresholds():
    from services.watch import commission_gate
    specs = {**{spec["count"][0]: spec["count"][1] for spec in commission_gate.DETECTORS.values()},
             **{spec["window_s"][0]: spec["window_s"][1] for spec in commission_gate.DETECTORS.values()},
             commission_gate.SHAPE_WINDOW[0]: commission_gate.SHAPE_WINDOW[1], commission_gate.SHAPE_MIN_INTERVAL[0]: commission_gate.SHAPE_MIN_INTERVAL[1]}
    return {key: commission_gate._param((key, default)) for key, default in specs.items()}


def _ground(tenant_id, citations):
    from services.watch import commission_gate
    on_record = {r["evidence_ref"] for r in commission_gate.rows(tenant_id) if r["kind"] == "detection"}
    return all(c in on_record for c in citations) and bool(citations)


def propose(tenant_id, principal_id, now=None):
    """Finding → CIF proposal → acceptance point → L-4 sink → grounding → Decisions item."""
    from services.cif.acceptance_point import is_accepted
    from services.cif.detection import author_proposal
    from services.cif.output_routing import route_accepted_proposal
    from services.watch import commission_gate, decisions
    from services.watch.research_queue import ResearchQueue, UnsureCase
    now = now or datetime.now(timezone.utc)
    rows = commission_gate.rows(tenant_id)
    detections = [r for r in rows if r["kind"] == "detection" and r.get("detector") != "mirage_incrimination"]
    releases = [r for r in rows if r["kind"] == "release" and r.get("outcome") == "expired_clean"]
    effects = [r for r in rows if r["kind"] == "effect"]
    if not detections:
        raise ValueError("No gate finding is on record yet; the loop starts from a finding, not from a wish.")
    thresholds = _effective_thresholds()
    signature = hashlib.sha256(json.dumps(thresholds, sort_keys=True).encode()).hexdigest()[:16]
    for item in decisions.fold(tenant_id).values():
        if item["state"] == "open" and item["klass"] == "requirement_ratification" and item["subject_ref"] == f"requirements:{signature}":
            return item                                        # the same finding is already on the panel; no second proposal
    citations = tuple(sorted({d["evidence_ref"] for d in detections}))
    payload = {"candidate_kind": "candidate_requirement", "thresholds": thresholds, "basis_label": label(),
               "evidence": {"detections": len(detections), "by_detector": {n: sum(1 for d in detections if d["detector"] == n) for n in commission_gate.DETECTORS},
                            "released_clean": len(releases), "effects": len(effects)},
               "rationale": "Pin the operating thresholds the record was produced under as a versioned requirement so replayed conduct is judged against a named version."}
    proposal = author_proposal(proposal_id=f"cif_watch_{uuid.uuid4().hex[:12]}", proposed_at=_iso(now), kind="research_loop_item",
                               payload=json.dumps(payload, sort_keys=True), citations=citations)
    accepted = is_accepted(proposal)
    if accepted is not True:
        commission_gate._append(tenant_id, {"kind": "learning", "at": _iso(now), "tenant_id": tenant_id, "stage": "refused_at_acceptance_point", "proposal_id": proposal.proposal_id})
        raise ValueError("The CIF acceptance point refused the proposal (uncited).")
    routed = route_accepted_proposal(proposal, accepted)
    ResearchQueue().enqueue(UnsureCase(case_id=proposal.proposal_id, verdict_signature=signature, observation_record=citations))
    grounded = _ground(tenant_id, citations)
    if not grounded:
        commission_gate._append(tenant_id, {"kind": "learning", "at": _iso(now), "tenant_id": tenant_id, "stage": "grounding_failed", "proposal_id": proposal.proposal_id})
        raise ValueError("Grounding failed: a citation did not resolve to the record.")
    refs = {"proposal_id": proposal.proposal_id, "payload": payload, "citations": list(citations), "routing": routed,
            "grounding_seam_id": GROUNDING_SEAM, "verdict_signature": signature}
    item = decisions.open_decision(tenant_id, "requirement_ratification", f"requirements:{signature}", refs, principal_id,
                                   f"Finding → candidate requirement v{(current() or {'version': 0})['version'] + 1}", now)
    commission_gate._append(tenant_id, {"kind": "learning", "at": _iso(now), "tenant_id": tenant_id, "stage": "proposed", "proposal_id": proposal.proposal_id,
                                        "decision_id": item["decision_id"], "routing": routed, "grounding_seam_id": GROUNDING_SEAM})
    return item


def ratify(tenant_id, refs, approvers, now=None):
    from services.watch import commission_gate
    from services.watch.research_queue import CifProposal, Ratification, SolvaGrounding, UnsureCase, run_research_loop_step
    now = now or datetime.now(timezone.utc)
    case = UnsureCase(case_id=refs["proposal_id"], verdict_signature=refs["verdict_signature"], observation_record=tuple(refs["citations"]))
    step = run_research_loop_step(case=case,
                                  cif_proposal=CifProposal(case_id=case.case_id, candidate_kind="candidate_requirement", rationale=refs["payload"]["rationale"]),
                                  solva_grounding=SolvaGrounding(case_id=case.case_id, grounded=True, grounding_seam_id=refs["grounding_seam_id"]),
                                  ratification=Ratification(ratifier_id=",".join(approvers), verdict="accepted"))
    previous = current()
    version = {"version": (previous or {"version": 0})["version"] + 1, "thresholds": refs["payload"]["thresholds"], "ratified_by": approvers,
               "ratified_at": _iso(now), "proposal_id": refs["proposal_id"], "previous_version": previous["version"] if previous else None,
               "tenant_id": tenant_id, "loop_step": step}
    _dir().mkdir(parents=True, exist_ok=True)
    (_dir() / f"v{version['version']}.json").write_text(json.dumps(version, indent=2, sort_keys=True), encoding="utf-8")
    commission_gate._append(tenant_id, {"kind": "learning", "at": _iso(now), "tenant_id": tenant_id, "stage": "ratified", "proposal_id": refs["proposal_id"],
                                        "version": version["version"], "ratified_by": approvers})
    return {"protection_changed": False, "requirements_version": version["version"]}
