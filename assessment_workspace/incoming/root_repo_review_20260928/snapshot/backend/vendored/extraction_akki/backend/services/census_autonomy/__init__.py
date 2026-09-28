"""PHASE 3 CENSUS AUTONOMY SERVICE — supervisor-managed persistent worker.

Owner R-106 verbatim (2026-02-XX · banked in STATE/DECISIONS.md at 4k Commit-B
f775adf6e10cd1f32b51b6ea85d44012c26a2672):

> "the census must be a SELF-RUNNING SYSTEM CAPABILITY — a persistent
> service owned by Akki itself — not an agent-driven drill."

The `services.census_autonomy` package additively adapts (per SO §3.8
additive-only) over the sealed data-source read-only adapters + the
sealed `services.tenant_separation` carriers (4j Commit-A eed6c032) + the
sealed `services.mtafiti.asset_registry_writer` single-writer (Canon-9 §3).
Zero edits to sealed modules; all cross-imports are read-only.

R-106 8 mandatory design goals (§8 verbatim):
1. supervisor-managed persistent worker/scheduler → `scheduler_program.py`
2. weekly-default scheduled + on-demand JWT-gated trigger → engine bounded runs
3. estate_census v3 productized additively → `engine.py`
4. mid-run decision queue → `REFUSAL_PATH_CLOSED_VOCAB.BLOCKED_AWAITING_RESPONSE`
5. auto-flowing results → engine writes through sealed asset_registry_writer
6. live-progress observable → SSE-adjacent state emitter (Phase 3 continuation)
7. degradation honesty → `REFUSAL_PATH_CLOSED_VOCAB` frozen tuple
8. ops proof at seal → kill+restart resume + AKKI-TEST end-to-end no-agent
"""

from services.census_autonomy.service_shape import (  # noqa: F401
    CENSUS_SCHEDULER_SUPERVISORD_PROGRAM_NAME,
    NO_AGENT_DEPENDENCY_ANCHOR,
    REFUSAL_PATH_CLOSED_VOCAB,
    TENANT_SCOPE_ENFORCEMENT_ANCHOR,
)

__all__ = (
    "CENSUS_SCHEDULER_SUPERVISORD_PROGRAM_NAME",
    "NO_AGENT_DEPENDENCY_ANCHOR",
    "REFUSAL_PATH_CLOSED_VOCAB",
    "TENANT_SCOPE_ENFORCEMENT_ANCHOR",
)
