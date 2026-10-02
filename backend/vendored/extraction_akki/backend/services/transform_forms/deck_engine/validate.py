"""DR-R5 fail-closed validation with enumerated errors {slide_index, rule, message}; one pass enumerates every violation.
DR-R6 honesty overlays that live in the schema or in resolution are checked here; DR-R7 lint is advisory and separate.
Receipt resolution is a PORT: `resolver(ref) -> record | None` (default: the platform's retained receipt stores)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from pydantic import ValidationError

from contracts.deck_spec_v1 import DeckSpec_v1, Slide
from services.transform_forms.deck_engine import plates
from services.transform_forms.deck_engine.tokens import REGISTERS

Resolver = Callable[[str], Optional[Dict[str, Any]]]
EXHIBIT_TYPES = ("exhibit", "comparison", "big_number", "table")
PLATE_REQUIRED = {"exhibit", "comparison", "big_number", "table"}


class DeckValidationError(Exception):
    def __init__(self, errors: List[Dict[str, Any]]):
        super().__init__(f"{len(errors)} deck validation error(s)")
        self.errors = errors


def _slide_index(loc) -> Optional[int]:
    if len(loc) >= 2 and loc[0] == "slides" and isinstance(loc[1], int):
        return loc[1]
    return None


def _schema_errors(exc: ValidationError) -> List[Dict[str, Any]]:
    out = []
    for e in exc.errors():
        loc = e["loc"]
        path = ".".join(str(p) for p in loc)
        rule = "schema_invalid"
        if e["type"] == "extra_forbidden":
            rule = "style_unrepresentable"
        elif e["type"] == "missing" and loc and loc[-1] == "class":
            rule = "missing_class"
        elif e["type"] == "missing" and loc and loc[0] == "coverage_and_limits":
            rule = "coverage_slide_required"
        elif loc and loc[0] == "coverage_and_limits":
            rule = "coverage_slide_required"
        out.append({"slide_index": _slide_index(loc), "rule": rule, "message": f"{path}: {e['msg']}"})
    return out


def parse(spec: Dict[str, Any]) -> DeckSpec_v1:
    if not isinstance(spec, dict):
        raise DeckValidationError([{"slide_index": None, "rule": "schema_invalid", "message": "spec must be an object"}])
    if spec.get("spec_version") == "v0":
        raise DeckValidationError([{"slide_index": None, "rule": "spec_not_renderable",
                                    "message": "DeckSpec_v0 (Slice-1 shell) carries no slides; submit the full DR-R4 shape as spec_version 'v1'"}])
    try:
        return DeckSpec_v1.model_validate(spec)
    except ValidationError as exc:
        raise DeckValidationError(_schema_errors(exc)) from None


def _exhibit_refs(slide: Slide) -> List[str]:
    refs = list(slide.receipt_refs)
    for f in slide.figures:
        refs += [r for r in f.receipt_refs if r not in refs]
    return refs


def validate(spec: Dict[str, Any], resolver: Resolver) -> Dict[str, Any]:
    """Returns {"spec": DeckSpec_v1, "plate_models": {index: model}, "receipts": {ref: record}} or raises DeckValidationError with the FULL error set."""
    deck = parse(spec)
    errors: List[Dict[str, Any]] = []
    plate_models: Dict[int, Any] = {}
    receipts: Dict[str, Any] = {}
    all_slides = list(deck.slides) + list(deck.appendix.extra_slides)
    for i, slide in enumerate(all_slides):
        if slide.type in PLATE_REQUIRED and not slide.plate:
            errors.append({"slide_index": i, "rule": "plate_required", "message": f"slide type {slide.type} needs a plate"})
        if slide.type == "big_number" and slide.plate not in (None, "P11"):
            errors.append({"slide_index": i, "rule": "plate_fit", "message": "big_number slides render on P11 only"})
        if slide.plate == "P11" and len(slide.figures) != 1:
            errors.append({"slide_index": i, "rule": "plate_schema_invalid", "message": "P11 renders exactly one figure"})
        if slide.plate:
            model, plate_errors = plates.parse_plate_data(slide.plate, slide.data)
            errors += [{"slide_index": i, **e} for e in plate_errors]
            if model is not None:
                plate_models[i] = model
        for j, fig in enumerate(slide.figures):
            if fig.value is None:
                errors.append({"slide_index": i, "rule": "no_silent_blank", "message": f"figures[{j}] value is null; figures cannot be unmeasured — declare the gap in plate data or coverage_and_limits"})
        is_exhibit = slide.type in EXHIBIT_TYPES or bool(slide.figures) or slide.plate in ("P3", "P4", "P5", "P11")
        if is_exhibit:
            refs = _exhibit_refs(slide)
            if not refs:
                errors.append({"slide_index": i, "rule": "unreceipted_exhibit", "message": "exhibit carries no receipt_refs"})
            resolved = 0
            for ref in refs:
                record = receipts.get(ref) or resolver(ref)
                if record is None:
                    errors.append({"slide_index": i, "rule": "unreceipted_exhibit", "message": f"receipt {ref} does not resolve"})
                else:
                    receipts[ref] = record; resolved += 1
            if refs and not resolved:
                errors.append({"slide_index": i, "rule": "unreceipted_exhibit", "message": "exhibit has zero resolvable receipts"})
    for k, o in enumerate(deck.selection_manifest.overrides):
        if o.field == "register" and o.value != deck.register_:
            errors.append({"slide_index": o.slide_index, "rule": "register_purity", "message": f"overrides[{k}] names register {o.value} but the artifact is {deck.register_}; one register per artifact"})
        if o.field == "plate" and o.slide_index is not None and (o.slide_index >= len(all_slides) or all_slides[o.slide_index].plate != o.value):
            errors.append({"slide_index": o.slide_index, "rule": "selection_manifest_recorded", "message": f"overrides[{k}] records plate {o.value} but the slide does not carry it"})
    if errors:
        raise DeckValidationError(sorted(errors, key=lambda e: (e["slide_index"] is None, e["slide_index"] or 0, e["rule"])))
    return {"spec": deck, "plate_models": plate_models, "receipts": receipts}


def lint(deck: DeckSpec_v1) -> List[Dict[str, Any]]:
    """DR-R7 advisory only — rendered into the production record, never blocking."""
    reg = REGISTERS[deck.register_]
    warnings = []
    body = [s for s in deck.slides if s.type not in ("title", "section", "coverage", "appendix")]
    if len(body) > reg["max_body_slides"]:
        warnings.append({"slide_index": None, "rule": "body_slide_count", "message": f"{len(body)} body slides exceed the {deck.register_} discipline of {reg['max_body_slides']}"})
    for i, s in enumerate(deck.slides):
        if len(s.title) > 2 * reg["title_chars_per_line"]:
            warnings.append({"slide_index": i, "rule": "title_two_lines", "message": f"title runs past two lines at {deck.register_} scale ({len(s.title)} chars > {2 * reg['title_chars_per_line']})"})
        words = re.findall(r"[A-Za-z0-9%€$£]+", s.title)
        if len(words) < 3 or s.title.rstrip().endswith("?") or (s.title.isupper() and len(s.title) > 8):
            warnings.append({"slide_index": i, "rule": "title_sentence_form", "message": "title should be a sentence-form assertion, not a label or a question"})
        if deck.register_ == "R1" and s.plate in ("P3", "P5") and s.data and len((s.data.get("rows") or s.data.get("cells") or [])) > 6:
            warnings.append({"slide_index": i, "rule": "plate_fit", "message": "dense table on a board-brief register; consider P4 or P11"})
    return warnings


# ----------------------------------------------------------------------------- default resolver over the retained receipt stores

def _state_root() -> Path:
    from services.census_autonomy import engine
    return Path(engine.CENSUS_STATE_DIR)


def default_resolver(ref: str) -> Optional[Dict[str, Any]]:
    """Resolves a receipt/job/run reference against the platform's retained, digest-bearing records (no network, no fabrication).
    Known families: eij- (estate intelligence census), lcj- (language cognition), m9j- (M9 training), cr- (census runs),
    rcp- (chokepoint crossing receipts), gpurcp- (SSH seam receipts), cwr- (census worker receipts inside run results)."""
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{6,120}", ref or ""):
        return None
    root = _state_root()
    phase0 = root.parent
    candidates = {"eij-": [root / "estate_intelligence" / f"{ref}.json"], "etx-": [root / "estate_intelligence" / f"{ref}.json"], "lcj-": [root / "language_cognition" / f"{ref}.json"],
                  "m9j-": [root / "m9_training" / f"{ref}.json"], "rcp-": [phase0 / "crossing_receipts" / f"{ref}.json"]}
    for prefix, paths in candidates.items():
        if ref.startswith(prefix):
            for path in paths:
                if path.is_file():
                    try:
                        doc = json.loads(path.read_text())
                    except (OSError, ValueError):
                        return None
                    return {"ref": ref, "kind": prefix.rstrip("-"), "path": str(path), "status": doc.get("status"), "verified": bool((doc.get("receipt") or {}).get("digest_verified", True))}
            return None
    if ref.startswith("cr-"):
        hits = sorted((root / "results").glob(f"*_{ref}_result.json"))
        return {"ref": ref, "kind": "census_run", "path": str(hits[-1]), "verified": True} if hits else None
    if ref.startswith("gpurcp-"):
        hits = sorted((phase0 / "gpu_receipts").glob(f"*_{ref}.log"))
        return {"ref": ref, "kind": "seam_receipt", "path": str(hits[-1]), "verified": True} if hits else None
    if ref.startswith("cwr-"):
        for path in sorted((root / "results").glob("*_result.json"), reverse=True)[:400]:
            try:
                if ref in path.read_text():
                    return {"ref": ref, "kind": "worker_receipt", "path": str(path), "verified": True}
            except OSError:
                continue
    return None
