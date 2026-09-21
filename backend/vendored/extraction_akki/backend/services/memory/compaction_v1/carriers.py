"""services.memory.compaction_v1.carriers · frozen pydantic carriers.

All frozen · closed-schema (`extra="forbid"`) · matches SO §3.10 Option
alpha closed-schema discipline + c13_scope precedent frozen-carrier
pattern (Canon 3 §9.3 append-only writer discipline · construction-time
immutability).

Canon anchors verbatim:
  * MEM-2 (Doc 4 A2; A5.5; C.19 I-2) · compacted artefact is a derived
    artefact · carries class 'inference' or 'utterance' · NEVER 'fact'.
    Every claim in it anchors to a retained source by provenance ref
    AND text hash.
  * MEM-5 (DAP-37 new-hash precedent) · compacted artefact is a NEW
    artefact with its own hash + lineage.
  * MEM-6 (B.4 · DAP-29) · ledger row content: source key + source
    version hashes + retention rule set version + artefact hash + loss
    statement (counts by class).
  * MEM-R-014 · loss statement class taxonomy verbatim:
    {fact, inference, utterance, receipt_ref, refusal, approval,
     objective, floor}.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Class-taxonomy allowed values (MEM-R-014 · loss statement class taxonomy
# verbatim · closed at 8 classes per spec).  Enforced at Claim construction
# via a regex-narrowed OPEN str (matches SO §3.10 Option alpha · no
# enum.Enum subclass).
_ALLOWED_CLASSES: tuple[str, ...] = (
    "fact",
    "inference",
    "utterance",
    "receipt_ref",
    "refusal",
    "approval",
    "objective",
    "floor",
)


class RetentionRuleSetVersion(BaseModel):
    """MEM-3 · versioned rule set identity (Rules Service pattern).

    Semver-like open string; v1 is the initial ratified set per
    MEM-R-004..MEM-R-009 (recommended defaults DEFAULT-class per
    owner MEMORY GO ruling · pending owner ratification of R-20).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    version: str = Field(min_length=1)


class Claim(BaseModel):
    """MEM-2 · a single claim entering compaction.

    Frozen · closed shape · class-taxonomy narrowed to the 8 allowed
    values per MEM-R-014.  text_hash MUST be a 64-hex sha256 digest of
    text bytes; provenance_ref is an OPEN string carrying the unit
    identity (URI-shaped by convention: 'unit:<id>' or free-form).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    class_: str = Field(pattern=r"^(fact|inference|utterance|receipt_ref|refusal|approval|objective|floor)$")
    text: str
    text_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    provenance_ref: str = Field(min_length=1)


class RunScopedContext(BaseModel):
    """A run-scoped context = key + tuple of claims.

    Key convention: 't_<tenant_id>/run_<run_id>/obj_<objective_id>' ·
    matches M11-W1 scoping + MEM-R-032 key scoping preservation ·
    NO principal data unless R-21 tenant flag ON (owner MEMORY GO
    default: OFF · principal data NOT written until ruled).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    key: str = Field(min_length=1)
    claims: tuple[Claim, ...]


class ClassAnchor(BaseModel):
    """MEM-2 · MEM-R-005 · pointer-by-hash anchor for a fact-class
    (or any) claim inside a compacted artefact.

    Preserves (class, provenance_ref, text_hash) tuple by-value.  The
    text itself is NEVER carried on the anchor (pointer-only for
    fact class per MEM-R-049 hard ban).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    class_: str = Field(pattern=r"^(fact|inference|utterance|receipt_ref|refusal|approval|objective|floor)$")
    provenance_ref: str = Field(min_length=1)
    text_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class CompactionArtefactRef(BaseModel):
    """MEM-5 · MEM-R-011 · NEW artefact with own hash + lineage.

    Carries: the artefact hash (sha256 of canonical body bytes) ·
    the source key + lineage_key (lineage recorded per MEM-R-011) ·
    source version hashes (per MEM-R-011) · the full superset of
    provenance references (MEM-R-002 SUPERSET rule) · the class
    anchors (MEM-R-005 pointer-by-hash for fact class) · the
    artefact class ('inference' or 'utterance' per MEM-2 · NEVER
    'fact').

    Method class_anchor(class_, provenance_ref) returns the matching
    ClassAnchor or None (deterministic lookup).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    artefact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    key: str = Field(min_length=1)
    lineage_key: str = Field(min_length=1)
    source_version_hashes: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    class_anchors: tuple[ClassAnchor, ...]
    class_: str = Field(pattern=r"^(inference|utterance)$")

    def class_anchor(
        self, *, class_: str, provenance_ref: str
    ) -> Optional[ClassAnchor]:
        """Deterministic lookup: return the matching ClassAnchor or None."""
        for a in self.class_anchors:
            if a.class_ == class_ and a.provenance_ref == provenance_ref:
                return a
        return None


class CompactionLedgerRow(BaseModel):
    """MEM-6 · MEM-R-012 · one ledger row per compaction.

    Written BEFORE the artefact becomes readable (MEM-R-012); row-write
    failure aborts the compaction (MEM-R-013).  Loss statement is
    counts-by-class (MEM-R-014) · exactly the 8-class taxonomy above.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    source_key: str = Field(min_length=1)
    source_version_hashes: tuple[str, ...]
    retention_rule_set_version: str = Field(min_length=1)
    artefact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    loss_statement: dict[str, int]
    total_drops: int = Field(ge=0)
    written_at_utc: str = Field(min_length=1)


__all__: tuple[str, ...] = (
    "Claim",
    "ClassAnchor",
    "CompactionArtefactRef",
    "CompactionLedgerRow",
    "RetentionRuleSetVersion",
    "RunScopedContext",
    "_ALLOWED_CLASSES",
)
