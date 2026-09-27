"""CC4–6 metadata reconstruction: whole units, pinned ranking, explicit losses.

No tokenization, retrieval, drafting or source bytes run here. Token counts are
observations of the admitted native tokenizer, not locally guessed counts.
"""
from collections import Counter
from typing import Annotated, Literal
from pydantic import Field, model_validator
from services.northena.execution_models import Frozen, Handle, Hash

Class = Literal['fact', 'inference', 'utterance', 'non_factual']
ORDER = {'fact': 0, 'inference': 1, 'utterance': 2, 'non_factual': 3}


class ContextUnit(Frozen):
    unit_ref: Handle
    content_sha256: Hash
    reextraction_ref: Handle
    class_label: Class
    tokens: Annotated[int, Field(gt=0)]
    proximity: Annotated[int, Field(ge=0)]
    source_position: Annotated[int, Field(ge=0)]
    memory_receipt_ref: Hash | None = None


class ContextWindow(Frozen):
    version: Literal['akki.context.metadata/1']
    objective_sha256: Hash
    frame_ref: Handle
    model_sha256: Hash
    tokenizer_sha256: Hash
    ranking_rule_ref: Hash
    qualified_set_receipt_ref: Hash
    load_bearing_refs: tuple[Handle, ...]
    window_tokens: Annotated[int, Field(gt=0)]
    reserved_tokens: Annotated[int, Field(ge=0)]
    units: Annotated[tuple[ContextUnit, ...], Field(min_length=1, max_length=500)]
    selected_refs: tuple[Handle, ...]
    excluded_counts: dict[Class, Annotated[int, Field(ge=0)]]
    top_excluded_handles: Annotated[tuple[Handle, ...], Field(max_length=10)]
    loss_disclosed: bool

    @model_validator(mode='after')
    def reconstructs(self):
        ids = {u.unit_ref for u in self.units}
        if (len(ids) != len(self.units) or len(set(self.load_bearing_refs)) != len(self.load_bearing_refs)
                or not set(self.load_bearing_refs) <= ids or self.reserved_tokens >= self.window_tokens):
            raise ValueError('Context identity/frame/budget is invalid.')
        selected, excluded = assemble(self)
        if not selected:
            raise ValueError('An empty window cannot ground an answer.')
        totals = Counter(u.class_label for u in excluded)
        if (self.selected_refs != tuple(u.unit_ref for u in selected)
                or self.excluded_counts != {c: totals[c] for c in ORDER}
                or self.top_excluded_handles != tuple(u.reextraction_ref for u in excluded[:10])
                or bool(excluded) != self.loss_disclosed):
            raise ValueError('Window order or loss statement cannot be reconstructed.')
        return self


def assemble(window):
    """Deterministic ranked whole-unit packing; never split or silently rerank."""
    ranked = sorted(window.units, key=lambda u: (
        u.unit_ref not in window.load_bearing_refs, ORDER[u.class_label],
        u.proximity, -u.source_position, u.unit_ref))
    remaining = window.window_tokens - window.reserved_tokens
    selected, excluded = [], []
    for unit in ranked:
        if unit.tokens <= remaining:
            selected.append(unit)
            remaining -= unit.tokens
        else:
            excluded.append(unit)
    return selected, excluded