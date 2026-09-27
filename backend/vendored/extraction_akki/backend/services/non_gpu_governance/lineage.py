"""Immutable reference lineage and withdrawal decisions; no deletion/refund effect."""
from typing import Annotated, Literal
from pydantic import Field, model_validator
from services.northena.execution_models import Frozen, Handle, Hash, Name, Held


class Lineage(Frozen):
    version: Literal['akki.lineage.metadata/1']
    artifact_ref: Handle
    artifact_sha256: Hash
    parents: Annotated[tuple[Handle, ...], Field(min_length=1, max_length=500)]

    @model_validator(mode='after')
    def identity(self):
        if self.artifact_ref in self.parents or len(set(self.parents)) != len(self.parents):
            raise ValueError('Self/duplicate lineage references are forbidden.')
        return self


class Rights(Frozen):
    version: Literal['akki.rights.metadata/1']
    unit_ref: Handle
    status: Literal['active', 'withdrawn']
    policy_ref: Hash
    reason_code: Name


def ancestors(refs, graph):
    """Iterative cycle-safe traversal; bounded metadata cannot overflow recursion."""
    done, active, result = set(), set(), set()
    stack = [(r, False) for r in refs]
    while stack:
        ref, exiting = stack.pop()
        if exiting:
            active.remove(ref)
            done.add(ref)
            continue
        if ref in active:
            raise Held('LINEAGE_CYCLE')
        if ref in done:
            continue
        if len(result) >= 10000:
            raise Held('LINEAGE_BOUND_EXCEEDED')
        result.add(ref)
        active.add(ref)
        stack.append((ref, True))
        stack.extend((parent, False) for parent in graph.get(ref, ()))
    return result


def descendants(unit_ref, graph):
    reverse = {}
    for child, parents in graph.items():
        for parent in parents:
            reverse.setdefault(parent, []).append(child)
    # This is a projection over canonical references, not an alternate registry.
    return tuple(sorted(ancestors((unit_ref,), reverse) - {unit_ref}))