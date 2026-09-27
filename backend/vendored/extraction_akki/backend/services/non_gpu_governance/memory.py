"""Native compacted-memory attestations. Original bytes stay in native custody."""
from typing import Annotated, Literal
from pydantic import Field, model_validator
from services.northena.execution_models import Frozen, Handle, Hash, Name


class MemoryEvidence(Frozen):
    version: Literal['akki.memory.metadata/1']
    artifact_ref: Handle
    artifact_sha256: Hash
    source_refs: Annotated[tuple[Handle, ...], Field(min_length=1, max_length=500)]
    source_hashes: Annotated[tuple[Hash, ...], Field(min_length=1, max_length=500)]
    principal_id: Name
    run_id: Name
    key: Name
    retention_policy_ref: Hash
    publication_receipt_ref: Hash
    class_label: Literal['inference', 'utterance']
    dropped_counts: dict[Name, Annotated[int, Field(ge=0)]]
    summarised_counts: dict[Name, Annotated[int, Field(ge=0)]]
    context_only: Literal[True]
    hash_verified_on_reload: Literal[True]
    user_memory: Literal[False]

    @model_validator(mode='after')
    def lineage(self):
        if len(self.source_refs) != len(self.source_hashes) or len(set(self.source_refs)) != len(self.source_refs):
            raise ValueError('Memory needs exact source/version pairs.')
        if any(n for cls, n in self.summarised_counts.items() if cls not in {'inference', 'utterance'}):
            raise ValueError('Facts and retained evidence cannot be summarised.')
        return self