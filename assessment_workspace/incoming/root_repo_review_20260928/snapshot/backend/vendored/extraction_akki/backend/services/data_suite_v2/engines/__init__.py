"""W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL · engines package.

Shared workspace-error exception classes for the two engine modules
(`analyze_workspace_engine`, `deep_dive_engine`).  Case-agnostic — no
executive-domain tokens in the error class names or their docstrings.
"""
from __future__ import annotations


class WorkspaceEmptyError(Exception):
    """Raised when the workspace has no `source_refs` to analyze.

    An empty workspace has no Solva units to enumerate; the engines refuse
    rather than emit a shape carrying a zero-length units-list, because the
    downstream release-gate + DAP-A10 discharge expects at least one unit
    ref to compose an ExportArtefact from (DAP-Spec §A10 mandates the
    `derivation_unit_refs` carrier be non-empty at admit_export time; the
    engines refuse the same invariant one seam earlier).
    """


class WorkspaceInvalidError(Exception):
    """Raised when a workspace input violates a shape invariant.

    Shape invariants gated:
      - `session_id` must be a non-empty string.
      - Every element of `source_refs` must be a string.
      - Every element of `prior_notes` (deep-dive only) must be a string.

    Case-agnostic; no executive-domain assumptions on the string content.
    """
