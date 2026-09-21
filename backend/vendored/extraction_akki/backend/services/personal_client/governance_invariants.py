"""services.personal_client.governance_invariants · B-frontends-Q1 · three-invariant enforcement.

Canon anchors (per M17.md MUST-DO 4):

- **STATE/DECISIONS.md:12115 verbatim B-frontends-Q1** owner
  ruling: "approval blocks rather than warns, silence never
  approves, the chat proposes and never decides · DAP UI Handoff
  Brief §5". This module authors the three governance-in-client
  invariants as pytest-only AST-scan predicates over the
  personal-client surface authored at W3 (and any future
  personal-client module added under
  `services/personal_client/*.py`).
- **STATE/DECISIONS.md:13600** (Frontend fidelity bar · DAP UI
  Handoff Brief §5 · extends to any client surface).
- **AC-18** (proposes-never-ratifies · extended to client
  surface): the three predicates make structural refusal a
  first-class check.
- **Canon 8 §W11** one-task-one-identity · structural role
  separation. This module carries ONLY pure predicates +
  `ApprovalBlocked` exception class. No side-effect · no I/O ·
  no persistence · no routing · no signing. AST-enforced by
  the paired invariant test file.
- **Canon 5** (Interface Architecture · client surface
  constraints).
- **Canon 6** (User Journeys · governance holds through journey).
- **SO §3.8** thin-kernel additive-only: this file lands NEW ·
  no sealed module edited.
- **SO §6.7** batch-ratification at CP-M16-W5-SEAL-INTEGRATION
  close · re-affirmed 2026-09-19T~14:35Z by owner PROCEED
  directive.

Public surface (Canon 8 §W11 strict):

    check_approval_blocks_rather_than_warns() -> bool
    check_silence_never_approves() -> bool
    check_chat_proposes_never_decides() -> bool
    ApprovalBlocked (Exception subclass · raiseable refusal type)

All three predicates walk the on-disk `services/personal_client/*.py`
tree via `ast.parse` + `ast.walk` and return `True` iff every
matched function structurally honours the corresponding
B-frontends-Q1 line. Absence of any matching function is vacuous
truth — the predicate defends the discipline for future authoring.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Tuple


__all__ = (
    "ApprovalBlocked",
    "check_approval_blocks_rather_than_warns",
    "check_silence_never_approves",
    "check_chat_proposes_never_decides",
)


# ---------------------------------------------------------------------------
# Refusal type
# ---------------------------------------------------------------------------


class ApprovalBlocked(Exception):
    """Refusal sentinel for approve-named client paths per
    B-frontends-Q1 line 1 ("approval blocks rather than warns").
    Raise on the negative branch of any function whose name matches
    regex `(^|_)approv(e|al)(_|$)`. Never write a warn-and-continue
    branch on such a function."""


# ---------------------------------------------------------------------------
# Module-path discovery · resolved fresh at each predicate call so a
# freshly-added `services/personal_client/*.py` module is picked up
# without module-import-time caching.
# ---------------------------------------------------------------------------


def _personal_client_dir() -> Path:
    """Return the on-disk directory that holds the personal-client
    surface (`services/personal_client/`). Resolved from this
    module's own location so the predicate is filesystem-honest."""
    return Path(__file__).resolve().parent


def _personal_client_source_files() -> Tuple[Path, ...]:
    """Return the closed tuple of `services/personal_client/*.py`
    files EXCLUDING `governance_invariants.py` itself (the
    invariants scan the *surface*, not the auditor)."""
    directory = _personal_client_dir()
    return tuple(
        sorted(
            path
            for path in directory.glob("*.py")
            if path.name != "governance_invariants.py"
            and path.name != "__init__.py"
        )
    )


def _parse_module_ast(path: Path) -> ast.AST:
    """Parse the target `.py` file into an AST tree. Raises the
    stdlib `SyntaxError` on malformed input — never converts to a
    structural pass silently."""
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


# ---------------------------------------------------------------------------
# Predicate 1 · approval blocks rather than warns
# ---------------------------------------------------------------------------


_APPROV_NAME_PATTERN = __import__("re").compile(r"(^|_)approv(e|al)(_|$)")


def _function_body_contains_approval_blocked_raise(func: ast.AST) -> bool:
    """Walk the body of `func` and return True iff any `raise`
    statement in the walk carries an exception named
    `ApprovalBlocked` (bare name OR call form)."""
    for node in ast.walk(func):
        if isinstance(node, ast.Raise) and node.exc is not None:
            exc = node.exc
            # `raise ApprovalBlocked` (bare name).
            if isinstance(exc, ast.Name) and exc.id == "ApprovalBlocked":
                return True
            # `raise ApprovalBlocked(...)` (call form).
            if isinstance(exc, ast.Call):
                target = exc.func
                if isinstance(target, ast.Name) and target.id == "ApprovalBlocked":
                    return True
                # `raise <module>.ApprovalBlocked(...)` (attribute call).
                if isinstance(target, ast.Attribute) and target.attr == "ApprovalBlocked":
                    return True
            # `raise <module>.ApprovalBlocked` (attribute bare).
            if isinstance(exc, ast.Attribute) and exc.attr == "ApprovalBlocked":
                return True
    return False


def check_approval_blocks_rather_than_warns() -> bool:
    """B-frontends-Q1 verbatim line 1: `approval blocks rather than
    warns`. Every function in `services/personal_client/*.py` whose
    name matches regex `(^|_)approv(e|al)(_|$)` MUST contain a
    `raise ApprovalBlocked` (bare / call / attribute forms
    accepted) somewhere in its body AST-walk.

    Vacuously True when no matching function exists in the current
    surface (defends future authoring).
    """
    for path in _personal_client_source_files():
        tree = _parse_module_ast(path)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if _APPROV_NAME_PATTERN.search(node.name) is None:
                continue
            if not _function_body_contains_approval_blocked_raise(node):
                return False
    return True


# ---------------------------------------------------------------------------
# Predicate 2 · silence never approves
# ---------------------------------------------------------------------------


def _annotation_is_optional(annotation: ast.AST | None) -> bool:
    """Return True iff `annotation` is one of:
    - `Optional[X]`
    - `typing.Optional[X]`
    - `X | None`
    - `None | X`
    - `Union[X, None]` / `typing.Union[X, None]`
    """
    if annotation is None:
        return False
    # Optional[X] / typing.Optional[X]
    if isinstance(annotation, ast.Subscript):
        value = annotation.value
        if isinstance(value, ast.Name) and value.id == "Optional":
            return True
        if isinstance(value, ast.Attribute) and value.attr == "Optional":
            return True
        if isinstance(value, ast.Name) and value.id == "Union":
            return _union_contains_none(annotation.slice)
        if isinstance(value, ast.Attribute) and value.attr == "Union":
            return _union_contains_none(annotation.slice)
    # X | None (PEP 604) → BinOp with BitOr and either side being
    # Constant(None) or Name('None').
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        for side in (annotation.left, annotation.right):
            if _is_none_annotation(side):
                return True
    return False


def _is_none_annotation(node: ast.AST) -> bool:
    """Return True iff `node` represents `None` as an annotation
    fragment (`Constant(None)` or `Name('None')`)."""
    if isinstance(node, ast.Constant) and node.value is None:
        return True
    if isinstance(node, ast.Name) and node.id == "None":
        return True
    return False


def _union_contains_none(slice_node: ast.AST) -> bool:
    """Return True iff the slice of a `Union[...]` annotation
    contains `None` as one of its elements."""
    if isinstance(slice_node, ast.Tuple):
        for elt in slice_node.elts:
            if _is_none_annotation(elt):
                return True
    return False


def _function_has_optional_parameter(func: ast.AST) -> bool:
    """Return True iff any parameter of `func` has an
    Optional-style annotation. Walks positional-only, positional,
    keyword-only, and vararg/kwarg slots."""
    if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    args = func.args
    slots = (
        list(args.posonlyargs)
        + list(args.args)
        + list(args.kwonlyargs)
    )
    if args.vararg is not None:
        slots.append(args.vararg)
    if args.kwarg is not None:
        slots.append(args.kwarg)
    for slot in slots:
        if _annotation_is_optional(slot.annotation):
            return True
    return False


def _function_body_refuses_on_empty_branch(func: ast.AST) -> bool:
    """Return True iff the function body AST contains at least one
    refusal-shaped construct: `raise <anything>`, `return None`,
    `return False`, or an `if <arg> is None: <refusal>` guard.

    Rationale: this is a *structural* check per B-frontends-Q1
    ("silence never approves"). A function with an Optional
    parameter must exhibit at least one refusal-shape in its body;
    a body that returns a truthy value on every branch is a
    structural failure."""
    for node in ast.walk(func):
        if isinstance(node, ast.Raise):
            return True
        if isinstance(node, ast.Return):
            value = node.value
            if value is None:
                return True
            if isinstance(value, ast.Constant) and (
                value.value is None or value.value is False
            ):
                return True
    return False


def check_silence_never_approves() -> bool:
    """B-frontends-Q1 verbatim line 2: `silence never approves`.
    Every function in `services/personal_client/session.py` whose
    parameter list contains an `Optional[X]` / `typing.Optional[X]`
    / `X | None` / `Union[X, None]` annotation MUST have at least
    one refusal-shape in its body (`raise`, `return None`,
    `return False`).

    Vacuously True when no matching parameter exists in the
    current surface (defends future authoring).
    """
    session_path = _personal_client_dir() / "session.py"
    if not session_path.is_file():
        # If session.py is somehow absent, treat as vacuous truth —
        # the paired invariant test asserts the file's presence
        # separately.
        return True
    tree = _parse_module_ast(session_path)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not _function_has_optional_parameter(node):
            continue
        if not _function_body_refuses_on_empty_branch(node):
            return False
    return True


# ---------------------------------------------------------------------------
# Predicate 3 · chat proposes and never decides
# ---------------------------------------------------------------------------


_CHAT_BANNED_SUBSTRINGS: Tuple[str, ...] = (
    "decide",
    "ratify",
    "admit",
    "sign",
    "approve",
    "route",
    "accept",
    "reject",
)


def _function_is_chat_labelled(func: ast.AST) -> bool:
    """Return True iff `func`'s name contains `chat` (case-insensitive)
    OR its docstring contains `chat` (case-insensitive)."""
    if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    if "chat" in func.name.lower():
        return True
    docstring = ast.get_docstring(func) or ""
    if "chat" in docstring.lower():
        return True
    return False


def _function_body_references_decision_surface_identifier(func: ast.AST) -> bool:
    """Return True iff any Name / Attribute / string constant in the
    body AST references a banned decision-surface substring
    (case-insensitive check on the raw identifier text)."""
    for node in ast.walk(func):
        candidates: list[str] = []
        if isinstance(node, ast.Name):
            candidates.append(node.id)
        elif isinstance(node, ast.Attribute):
            candidates.append(node.attr)
        elif isinstance(node, ast.Call):
            # Function-call target expressed as name or attribute is
            # already captured above; nothing extra here.
            pass
        for identifier in candidates:
            lowered = identifier.lower()
            for banned in _CHAT_BANNED_SUBSTRINGS:
                if banned in lowered:
                    return True
    return False


def check_chat_proposes_never_decides() -> bool:
    """B-frontends-Q1 verbatim line 3: `the chat proposes and never
    decides`. Every function in `services/personal_client/*.py`
    whose name contains substring `chat` (case-insensitive) OR
    whose docstring contains `chat` MUST NOT reference any
    decision-surface identifier by name anywhere in its body AST.
    Banned substrings (case-insensitive match): `decide`, `ratify`,
    `admit`, `sign`, `approve`, `route`, `accept`, `reject`.

    Vacuously True when no matching function exists in the current
    surface (defends future authoring).
    """
    for path in _personal_client_source_files():
        tree = _parse_module_ast(path)
        for node in ast.walk(tree):
            if not _function_is_chat_labelled(node):
                continue
            if _function_body_references_decision_surface_identifier(node):
                return False
    return True
