"""Server-derived key scoping for C.13 closure.

Public surface: `derive_scoped_key(*, tenant_id, run_id, objective_id) -> str`
returning 32-char lowercase-hex (sha256[:32]) over canonical sorted-key JSON
of the input tuple. Pure-data-in per M14-W4 precedent 2026-09-19 verbatim
("a code path is a code path"). Determinism per Canon 4 §22 rung-1
machinery discipline.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "server-derived keys
from (tenant, run, objective) with cross-key reads refused".

Canon 8 §W11 structural role separation: this module carries ONLY the
deriver. No persistence · no signing · no learned surface · no decision
surface. AST-enforced by paired invariant test 8.
"""
from __future__ import annotations

import hashlib
import json


def derive_scoped_key(
    *,
    tenant_id: str,
    run_id: str,
    objective_id: str,
) -> str:
    """Return a 32-char lowercase-hex scoped-key deterministically derived
    from (tenant_id, run_id, objective_id) via sha256[:32] over the
    canonical sorted-key JSON of the tuple.

    Refuses non-string / empty-string input at boundary.
    """
    for field_name, value in (
        ("tenant_id", tenant_id),
        ("run_id", run_id),
        ("objective_id", objective_id),
    ):
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"derive_scoped_key · {field_name} MUST be a non-empty "
                f"string · got {type(value).__name__}={value!r}"
            )
    payload = json.dumps(
        {
            "tenant_id": tenant_id,
            "run_id": run_id,
            "objective_id": objective_id,
        },
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:32]
