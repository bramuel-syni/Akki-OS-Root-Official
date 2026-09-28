"""services.rules_service.rule_book_library — W-M2-SW3.

Rule-book library: deterministic file-backed source of truth for the
286-rule register.  SW3 lands the persistence layer over SW1's
RuleRegistry.  SW4 uses this library to materialise the full 286-rule
enumeration into the register.

Canon-3 §22: every load appends; the library never rewrites in place.
Canon-3 §9.3: single writer.

Immutability rationale: a RuleBook is a snapshot of ratified rules —
its content is content-hashed (sha256 hex of a canonical JSON dump)
and any mutation would silently invalidate the hash.  Freeze protects
downstream ceremonies that cite a specific rule-book state.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Tuple

from pydantic import BaseModel, ConfigDict

from services.rules_service.rule_registry import (
    RuleRecord,
    RuleRegistry,
    RuleIdCollision,
)


class RuleBookImmutable(RuntimeError):
    """Raised on any attempt to mutate a RuleBook after construction."""


class RuleBookIntegrityError(ValueError):
    """Raised when the source contains internal-integrity violations
    (duplicate ids, invalid enforcement class, unparseable line)."""


class RuleBook(BaseModel):
    """Frozen snapshot of an ordered rule list.  Content-hashed.

    Constructing a RuleBook does NOT mutate any registry — call
    `materialise_into_registry(book, registry)` for that step.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    rules: Tuple[RuleRecord, ...]

    @property
    def content_hash(self) -> str:
        """Deterministic sha256 hex of the rule list.

        Serialisation is canonical (sorted keys, no whitespace) so
        equal rule lists always produce equal hashes.
        """
        payload = [
            {
                "rule_id": r.rule_id,
                "source_citation": r.source_citation,
                "scope": r.scope,
                "enforcement_class": r.enforcement_class,
            }
            for r in self.rules
        ]
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def load_rule_book_from_jsonl(path: str | Path) -> RuleBook:
    """Load a rule book from a jsonl file.

    Each line MUST be a JSON object matching RuleRecord fields.
    Duplicate rule ids anywhere in the file raise
    RuleBookIntegrityError — Canon-3 §22 supersession requires NEW ids.
    """
    p = Path(path)
    if not p.exists():
        raise RuleBookIntegrityError(
            f"rule-book source missing: {path!r}"
        )
    rules: list[RuleRecord] = []
    seen: set[str] = set()
    with p.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuleBookIntegrityError(
                    f"rule-book line {lineno} unparseable: {exc}"
                ) from exc
            try:
                rec = RuleRecord(**d)
            except Exception as exc:
                raise RuleBookIntegrityError(
                    f"rule-book line {lineno} invalid: {exc}"
                ) from exc
            if rec.rule_id in seen:
                raise RuleBookIntegrityError(
                    f"rule-book line {lineno}: duplicate rule_id "
                    f"{rec.rule_id!r} — Canon-3 §22 supersession "
                    f"requires a NEW id"
                )
            seen.add(rec.rule_id)
            rules.append(rec)
    return RuleBook(rules=tuple(rules))


def materialise_into_registry(
    book: RuleBook, registry: RuleRegistry
) -> dict:
    """Append every rule in the book into the registry (additive).

    Rules whose id is already registered are SKIPPED (not overwritten);
    the return dict reports counts.  Canon-3 §22: supersession never
    silently overwrites — it requires a new id.
    """
    appended = 0
    skipped_existing = 0
    for rec in book.rules:
        try:
            registry.append(rec)
            appended += 1
        except RuleIdCollision:
            skipped_existing += 1
    return {
        "appended": appended,
        "skipped_existing": skipped_existing,
        "total": len(book.rules),
        "book_content_hash": book.content_hash,
    }


__all__ = [
    "RuleBook",
    "RuleBookImmutable",
    "RuleBookIntegrityError",
    "load_rule_book_from_jsonl",
    "materialise_into_registry",
]
