"""W-DATA-SUITE-ANALYZE-WORKSPACE-REAL · CP-DASWR1 · Real analyze-workspace engine.

Replaces the CP-D8 HALT-skeleton with a real case-agnostic mechanism that
produces the CP-D4 tab-artefact shapes `AnalyzeRapid` + `AnalyzeSources`
from typed workspace inputs.  Pure function — no LLM, no HTTP, no storage.

Contract:

    run(*, session_id: str, source_refs: Sequence[str]) ->
        Tuple[AnalyzeRapid, AnalyzeSources]

Refusals:
- `session_id` empty or non-string    → `WorkspaceInvalidError`
- `source_refs` empty                 → `WorkspaceEmptyError`
- any element of `source_refs` non-string → `WorkspaceInvalidError`

Discharge:
- Canon-4 §22 UnitRefs-only: `AnalyzeSources.unit_refs` is a straight pass-
  through of the caller-provided source_refs.  No class decision emitted.
- CP-D4 tab-kind contract: `AnalyzeRapid(tab_kind="rapid")` +
  `AnalyzeSources(tab_kind="sources")` per closed 3-value set.
"""
from __future__ import annotations

from typing import Sequence, Tuple

from services.data_suite_v2.analyze_tabs import AnalyzeRapid, AnalyzeSources
from services.data_suite_v2.engines import (
    WorkspaceEmptyError,
    WorkspaceInvalidError,
)


def _validate_session_id(session_id: str) -> None:
    if not isinstance(session_id, str) or not session_id:
        raise WorkspaceInvalidError(
            f"workspace shape: session_id must be a non-empty string; "
            f"got {session_id!r}"
        )


def _validate_source_refs(source_refs: Sequence[str]) -> Tuple[str, ...]:
    if not source_refs:
        raise WorkspaceEmptyError(
            "workspace shape: source_refs must be non-empty; got 0 refs"
        )
    coerced = tuple(source_refs)
    for i, ref in enumerate(coerced):
        if not isinstance(ref, str):
            raise WorkspaceInvalidError(
                f"workspace shape: source_refs[{i}] must be a string; "
                f"got {type(ref).__name__}"
            )
    return coerced


def run(
    *,
    session_id: str,
    source_refs: Sequence[str],
) -> Tuple[AnalyzeRapid, AnalyzeSources]:
    """Analyze a workspace and produce the `rapid` + `sources` tab shapes.

    Pure function of typed inputs.  No LLM/HTTP/storage side-effects.  Case-
    agnostic — no executive-domain tokens in the module or in the returned
    shapes.  See module docstring for refusals and discharge anchors.
    """
    _validate_session_id(session_id)
    refs = _validate_source_refs(source_refs)

    rapid = AnalyzeRapid(
        session_id=session_id,
        tab_kind="rapid",
        unit_ref_count=len(refs),
    )
    sources = AnalyzeSources(
        session_id=session_id,
        tab_kind="sources",
        unit_refs=refs,
    )
    return rapid, sources
