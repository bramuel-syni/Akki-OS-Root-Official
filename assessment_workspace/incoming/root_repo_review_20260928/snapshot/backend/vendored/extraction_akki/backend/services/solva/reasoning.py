"""services.solva.reasoning — three stages via chokepoint.llm.

Frame audit → candidate generation → synthesis. Each stage returns a
result dataclass carrying its receipt_id, model_id, and provider so
surfaces can render provenance (Owner sharpening §4).

On shield refusal (LLMShieldFailure or PurposeInvalid), the stage
result carries `refused=True` and the refusal reason VERBATIM (never a
smoothed answer per A8-Q3).
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.chokepoint import llm as _chokepoint_llm
from services.chokepoint.llm import (
    LLMShieldFailure,
    PurposeInvalid,
)

log = logging.getLogger(__name__)

_DEFAULT_RUN_DIR = "/app/assessment_workspace/phase0/solva_runs"


def _run_dir() -> Path:
    return Path(os.environ.get("SOLVA_RUN_DIR", _DEFAULT_RUN_DIR))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Stage 1 · frame_audit (deterministic regex + LLM refinement).
# ---------------------------------------------------------------------------

_DECISIONAL = re.compile(
    r"\b(decision|decide|approve|reject|choose|should we|whether to|"
    r"go/no-go|proceed|hold|defer|invest)\b", re.I,
)
_TIME_HORIZON = re.compile(
    r"\b(quarter|q[1-4]\b|h[12]\b|next year|by (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|"
    r"month|week|days|board meeting|fiscal year|fy\s*\d+)\b", re.I,
)
_SCOPE = re.compile(
    r"\b(within|limited to|specifically|in (the )?context of|for the (board|exec|cfo|ceo)|"
    r"around|archive|programme)\b", re.I,
)
_EVIDENCE = re.compile(
    r"\b(report|memo|deck|paper|attached|document|data|forecast|model|"
    r"analysis|finding|study|brief|register|record)\b", re.I,
)
_LENS = re.compile(
    r"\b(from the (cfo|ceo|chair|investor|regulator|cro|coo|ned|board)|as (a|the) (cfo|ceo|chair)|"
    r"perspective of|owner|estate)\b", re.I,
)

_VERDICT_ORDER = {"sufficient": 0, "sufficient_with_caveats": 1, "insufficient": 2}


def _score_regex(framing: str) -> List[Dict[str, Any]]:
    def _row(name, present, severity="minor", inv=None):
        if present:
            return {"dimension": name, "score": "sufficient", "severity": severity, "invalidation": None}
        return {"dimension": name, "score": "thin", "severity": severity, "invalidation": inv}

    return [
        _row("decisional_clarity", bool(_DECISIONAL.search(framing)), "material",
             "no explicit decision the direction would inform"),
        _row("time_horizon", bool(_TIME_HORIZON.search(framing)),
             "minor", "no explicit time horizon"),
        _row("scope_boundedness", bool(_SCOPE.search(framing)),
             "minor", "scope is open-ended"),
        _row("evidence_grounding", bool(_EVIDENCE.search(framing)),
             "material", "no attached material or referenced source"),
        _row("lens_fit", bool(_LENS.search(framing)),
             "minor", "no explicit lens requested"),
    ]


def _verdict_from_dims(dims: List[Dict[str, Any]]) -> str:
    absent_critical = [d for d in dims if d["score"] == "absent" and d["severity"] in ("material", "critical")]
    if absent_critical:
        return "insufficient"
    thin_material = [d for d in dims if d["score"] == "thin" and d["severity"] in ("material", "critical")]
    if thin_material:
        # material dimensions thin → insufficient (most-restrictive over LLM smoothing).
        return "insufficient"
    minor_thin = [d for d in dims if d["score"] == "thin"]
    if minor_thin:
        return "sufficient_with_caveats"
    return "sufficient"


def _refined_verdict_from_llm_text(text: str) -> Optional[str]:
    body = (text or "").lower()
    if "insufficient" in body:
        return "insufficient"
    if "sufficient_with_caveats" in body or "with caveats" in body:
        return "sufficient_with_caveats"
    if "sufficient" in body:
        return "sufficient"
    return None


@dataclass
class FrameAuditResult:
    verdict: str
    dimensions: List[Dict[str, Any]]
    llm_refinement_text: str
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


async def run_frame_audit(
    *,
    direction_statement: str,
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> FrameAuditResult:
    """Frame audit stage: deterministic regex pass + LLM refinement.

    Most-restrictive wins between deterministic and LLM verdicts.
    """
    dims = _score_regex(direction_statement or "")
    det_verdict = _verdict_from_dims(dims)

    prompt = json.dumps({
        "task": "frame_audit_refinement",
        "direction_statement": (direction_statement or "")[:1800],
        "deterministic_verdict": det_verdict,
        "deterministic_dimensions": dims,
        "output_schema": {
            "verdict": "sufficient | sufficient_with_caveats | insufficient",
            "observations": "list of short strings",
        },
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.frame_audit",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        # A8-Q3 honesty: surface refusal verbatim.
        return FrameAuditResult(
            verdict=det_verdict,   # deterministic still holds
            dimensions=dims,
            llm_refinement_text="",
            receipt_id="",
            model_id="",
            provider="",
            refused=True,
            refusal_reason=str(exc)[:400],
        )

    refined = _refined_verdict_from_llm_text(resp.text)
    # Most-restrictive wins.
    candidates = [det_verdict]
    if refined:
        candidates.append(refined)
    final_verdict = max(candidates, key=lambda v: _VERDICT_ORDER.get(v, 0))

    return FrameAuditResult(
        verdict=final_verdict,
        dimensions=dims,
        llm_refinement_text=resp.text,
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )


# ---------------------------------------------------------------------------
# Stage 2 · candidate_generation.
# ---------------------------------------------------------------------------

CANDIDATE_TYPE_DEFAULT = "cause"


def _parse_candidates_json(body: str, ctype: str) -> List[Dict[str, Any]]:
    """Extract JSON array/object from the LLM response."""
    if not body:
        return []
    start = body.find("[")
    end = body.rfind("]")
    data: List[Dict[str, Any]] = []
    if start >= 0 and end > start:
        try:
            parsed = json.loads(body[start:end + 1])
            if isinstance(parsed, list):
                data = [c for c in parsed if isinstance(c, dict)]
        except (ValueError, TypeError):
            pass
    out: List[Dict[str, Any]] = []
    for c in data[:8]:
        desc = str(c.get("description") or c.get("desc") or "").strip()
        evid = str(c.get("evidence_requirement") or c.get("evidence") or "").strip()
        if len(desc) < 10:
            continue
        if not evid:
            evid = "evidence from attached material or referenced source"
        out.append({
            "id": f"cand-{hashlib.sha1(desc.encode('utf-8')).hexdigest()[:10]}",
            "candidate_type": ctype,
            "description": desc[:240],
            "evidence_requirement": evid[:240],
            "weight": round(1.0 / max(1, min(5, len(data))), 3),
        })
    return out


@dataclass
class CandidateGenerationResult:
    candidates: List[Dict[str, Any]]
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


async def run_candidate_generation(
    *,
    direction_statement: str,
    situation_class: str = "unknown",
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> CandidateGenerationResult:
    prompt = json.dumps({
        "task": "candidate_generation",
        "situation_class": situation_class,
        "direction_statement": (direction_statement or "")[:1500],
        "target_count": 5,
        "output_schema": (
            "JSON ARRAY of EXACTLY 5 objects. Each object has TWO string "
            "fields: 'description' (the candidate, 1-2 sentences) and "
            "'evidence_requirement' (what would confirm or refute it, 1 "
            "sentence). Return ONLY the JSON array — no preamble."
        ),
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.candidate_generation",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        return CandidateGenerationResult(
            candidates=[],
            receipt_id="",
            model_id="",
            provider="",
            refused=True,
            refusal_reason=str(exc)[:400],
        )

    parsed = _parse_candidates_json(resp.text, CANDIDATE_TYPE_DEFAULT)
    return CandidateGenerationResult(
        candidates=parsed,
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )


# ---------------------------------------------------------------------------
# Stage 3 · synthesis.
# ---------------------------------------------------------------------------

@dataclass
class SynthesisResult:
    paragraph: str
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


async def run_synthesis(
    *,
    direction_statement: str,
    candidates: List[Dict[str, Any]],
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> SynthesisResult:
    prompt = json.dumps({
        "task": "synthesis",
        "direction_statement": (direction_statement or "")[:1000],
        "candidates": candidates[:5],
        "output_schema": (
            "One paragraph of 3-5 sentences in coach voice. Name the "
            "candidates that carry weight against the direction and what "
            "would tighten the reading. NO field labels, NO markdown fences."
        ),
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.synthesis",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        return SynthesisResult(
            paragraph="",
            receipt_id="",
            model_id="",
            provider="",
            refused=True,
            refusal_reason=str(exc)[:400],
        )

    return SynthesisResult(
        paragraph=(resp.text or "").strip(),
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )


# ---------------------------------------------------------------------------
# Full pipeline + persistence.
# ---------------------------------------------------------------------------

@dataclass
class SolvaRun:
    run_id: str
    direction_statement: str
    actor: str
    at_iso: str
    frame_audit: FrameAuditResult
    candidate_generation: CandidateGenerationResult
    synthesis: SynthesisResult
    receipt_ids: List[str]


def _persist_run(run: SolvaRun) -> Path:
    d = _run_dir()
    d.mkdir(parents=True, exist_ok=True)
    file_path = d / f"{run.run_id}.json"
    payload = {
        "run_id": run.run_id,
        "direction_statement": run.direction_statement,
        "actor": run.actor,
        "at_iso": run.at_iso,
        "receipt_ids": run.receipt_ids,
        "frame_audit": asdict(run.frame_audit),
        "candidate_generation": asdict(run.candidate_generation),
        "synthesis": asdict(run.synthesis),
    }
    file_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return file_path


async def run_full_pipeline(
    *,
    direction_statement: str,
    actor: str,
    situation_class: str = "unknown",
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> SolvaRun:
    run_id = f"run-{uuid.uuid4().hex[:12]}"

    fa = await run_frame_audit(
        direction_statement=direction_statement,
        actor=actor,
        model=model,
        provider=provider,
    )
    cg = await run_candidate_generation(
        direction_statement=direction_statement,
        situation_class=situation_class,
        actor=actor,
        model=model,
        provider=provider,
    )
    syn = await run_synthesis(
        direction_statement=direction_statement,
        candidates=cg.candidates,
        actor=actor,
        model=model,
        provider=provider,
    )

    receipt_ids = [r for r in (fa.receipt_id, cg.receipt_id, syn.receipt_id) if r]
    run = SolvaRun(
        run_id=run_id,
        direction_statement=direction_statement,
        actor=actor,
        at_iso=_now_iso(),
        frame_audit=fa,
        candidate_generation=cg,
        synthesis=syn,
        receipt_ids=receipt_ids,
    )
    _persist_run(run)
    return run


__all__ = [
    "FrameAuditResult",
    "CandidateGenerationResult",
    "SynthesisResult",
    "TriangulationResult",
    "TensionResult",
    "ProbabilityWeightedResult",
    "SolvaRun",
    "run_frame_audit",
    "run_candidate_generation",
    "run_synthesis",
    "run_triangulation",
    "run_tension_detection",
    "run_probability_weighting",
    "run_full_pipeline",
]


# ===========================================================================
# W6 CP4 · Grey Mirror groundwork · Solva stages 4-6.
# ===========================================================================
# Owner Ruling 2026-08-25 · W6 GO §W6-SCOPE-(c): mechanism-side only;
# NOT wired into run_full_pipeline yet — the Grey Mirror surface + full
# pipeline ratification lands with W9.

def _kind_map_kind_to_receipt(kind_or_purpose: str) -> str:
    return kind_or_purpose


def _extract_json(body: str, key: Optional[str] = None) -> Any:
    """Deterministic JSON extractor: finds the first {...} or [...] block.
    Returns the parsed value (or the whole payload if `key` is None) or
    None on unparseable body.
    """
    if not body:
        return None
    for opener, closer in [("{", "}"), ("[", "]")]:
        s = body.find(opener)
        e = body.rfind(closer)
        if s >= 0 and e > s:
            try:
                obj = json.loads(body[s:e + 1])
                if key is not None and isinstance(obj, dict):
                    return obj.get(key)
                return obj
            except (ValueError, TypeError):
                continue
    return None


# -----------------------------
# Stage 4 · triangulation
# -----------------------------

@dataclass
class TriangulationResult:
    supported: List[Dict[str, Any]]
    contested: List[Dict[str, Any]]
    unsupported: List[Dict[str, Any]]
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


async def run_triangulation(
    *,
    candidates: List[Dict[str, Any]],
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> TriangulationResult:
    """Cross-source triangulation: which candidates have support, which
    are contested, which are unsupported. Doc 04 Solva Stage 4."""
    prompt = json.dumps({
        "task": "triangulation",
        "candidates": candidates[:5],
        "output_schema": (
            "JSON object with three arrays: "
            "'supported' (each: {candidate_id, supporting_sources: [str]}), "
            "'contested' (each: {candidate_id, supporting: [str], against: [str]}), "
            "'unsupported' (each: {candidate_id, reason: str}). "
            "Return ONLY the JSON object · no preamble."
        ),
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.triangulation",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        return TriangulationResult(
            supported=[], contested=[], unsupported=[],
            receipt_id="", model_id="", provider="",
            refused=True, refusal_reason=str(exc)[:400],
        )

    body = _extract_json(resp.text) or {}
    return TriangulationResult(
        supported=body.get("supported", []) if isinstance(body, dict) else [],
        contested=body.get("contested", []) if isinstance(body, dict) else [],
        unsupported=body.get("unsupported", []) if isinstance(body, dict) else [],
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )


# -----------------------------
# Stage 5 · tension_detection
# -----------------------------

@dataclass
class TensionResult:
    tensions: List[Dict[str, Any]]
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


async def run_tension_detection(
    *,
    candidates: List[Dict[str, Any]],
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> TensionResult:
    """Find contradictions between candidates. Doc 04 Solva Stage 5."""
    prompt = json.dumps({
        "task": "tension_detection",
        "candidates": candidates[:5],
        "output_schema": (
            "JSON object with a 'tensions' array. Each tension: "
            "{between: [candidate_id, candidate_id], "
            "kind: 'mutually_exclusive'|'weakening'|'framing_conflict', "
            "reason: str}. Return ONLY the JSON · no preamble."
        ),
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.tension_detection",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        return TensionResult(
            tensions=[], receipt_id="", model_id="", provider="",
            refused=True, refusal_reason=str(exc)[:400],
        )

    body = _extract_json(resp.text) or {}
    return TensionResult(
        tensions=body.get("tensions", []) if isinstance(body, dict) else [],
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )


# -----------------------------
# Stage 6 · probability_weighting
# -----------------------------

@dataclass
class ProbabilityWeightedResult:
    candidates_with_weights: List[Dict[str, Any]]
    receipt_id: str
    model_id: str
    provider: str
    refused: bool = False
    refusal_reason: str = ""


def _normalise_weights(weighted: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rescale so weights sum to ~1.0. Proportions preserved."""
    total = sum(max(0.0, float(w.get("weight", 0) or 0)) for w in weighted)
    if total <= 0:
        # honest empty · nothing to normalise
        return weighted
    out = []
    for w in weighted:
        raw = max(0.0, float(w.get("weight", 0) or 0))
        w2 = dict(w)
        w2["weight"] = round(raw / total, 4)
        out.append(w2)
    return out


async def run_probability_weighting(
    *,
    candidates: List[Dict[str, Any]],
    triangulation: Dict[str, Any],
    tensions: List[Dict[str, Any]],
    actor: str,
    model: str = "gpt-5-mini",
    provider: str = "emergent",
) -> ProbabilityWeightedResult:
    """Bayesian-style weighting of candidates given triangulation + tensions.
    Doc 04 Solva Stage 6.

    Weights are DETERMINISTICALLY NORMALISED after the LLM returns them —
    proportions preserved, sum to ~1.0. NEVER silently invented; if the
    LLM returns nothing parseable, candidates_with_weights=[]."""
    prompt = json.dumps({
        "task": "probability_weighting",
        "candidates": candidates[:5],
        "triangulation": triangulation,
        "tensions": tensions[:10],
        "output_schema": (
            "JSON object with 'weighted_candidates' array. Each entry: "
            "{candidate_id, weight (0.0-1.0), rationale}. Weights should "
            "roughly sum to 1.0 · normalisation applied on receipt."
        ),
    }, ensure_ascii=False)

    try:
        resp = await _chokepoint_llm.invoke(
            purpose="solva.probability_weighting",
            prompt=prompt,
            masking_tier="llm_reasoning_context",
            actor=actor,
            model=model,
            provider=provider,
            tenant_id=actor or "unknown",
            custody_class="tenant_estate",
        )
    except (LLMShieldFailure, PurposeInvalid) as exc:
        return ProbabilityWeightedResult(
            candidates_with_weights=[], receipt_id="", model_id="", provider="",
            refused=True, refusal_reason=str(exc)[:400],
        )

    body = _extract_json(resp.text) or {}
    raw = body.get("weighted_candidates", []) if isinstance(body, dict) else []
    normalised = _normalise_weights(raw)
    return ProbabilityWeightedResult(
        candidates_with_weights=normalised,
        receipt_id=resp.receipt_id,
        model_id=resp.model_id,
        provider=resp.provider,
    )
