"""Frozen module-level shape constants for PHASE 3 CENSUS AUTONOMY SERVICE.

Per SO §3.10-α closed-vocab paired-equality discipline: every constant
declared here is Final and typed; the four RED-first invariants at
`tests/invariants/test_cp_census_autonomy_service_shape_gate.py` pin each
by verbatim value.

Owner R-106 verbatim (2026-02-XX) BINDING SOURCE (banked in
STATE/DECISIONS.md at 4k Commit-B f775adf6):

> "8 mandatory design goals: (1) supervisor-managed persistent worker/
> scheduler process (e.g., a census_scheduler service registered in
> supervisord alongside backend) that survives agent absence, app
> restarts, and pod restarts — census runs happen with NO agent in the
> loop. (2) Scheduled runs: weekly default per the prototype ...
> (3) The census engine productized: port the estate_census v3 logic
> into backend services (additive; adapters over the sealed data_source
> packages), tenant-scoped from birth, LawfulBasisAdmit + all-reads-
> receipted + no-second-store invariants enforced in the service path,
> bounded/budgeted per run. (4) Mid-run questions: when the census
> needs a decision it banks a response-required item to a queue
> surfaced in the UI ... and CONTINUES on everything not blocked — it
> never stalls waiting for a human or agent. (5) Results flow
> automatically ... (6) Progress is observable live ... (7) Degradation
> honesty: unreachable surface → BLOCKED row with blocker; unreachable
> GPU hosts → audio deep-analysis marked deferred-not-failed; the run
> still completes and reports. (8) Ops proof at seal ... RED-first
> invariants for scheduler existence, tenant scoping, refusal paths,
> and no-agent-dependency (e.g., service runs under supervisor, not
> invoked by test harness)."
"""

from __future__ import annotations

from typing import Final, Tuple

# ---------------------------------------------------------------------------
# R-106 §8(c) invariant 1 · scheduler existence
# ---------------------------------------------------------------------------
#
# Owner-verbatim supervisord program name per R-106 §1:
# 'a census_scheduler service registered in supervisord alongside backend'.
# Bound to the actual supervisord program name in
# `backend/scripts/census_scheduler.supervisord.conf` (dropped into
# /etc/supervisor/conf.d/ at deploy time).
CENSUS_SCHEDULER_SUPERVISORD_PROGRAM_NAME: Final[str] = "census_scheduler"


# ---------------------------------------------------------------------------
# R-106 §8(c) invariant 2 · tenant scoping
# ---------------------------------------------------------------------------
#
# Dotted-path anchor to the SEALED CP-TENANT-SEPARATION carrier (4j
# Commit-A eed6c032a1cf7155df33cac2a788eeabb72531e8 — precedent) so
# tenant scope IS the sealed tenant_registry, NOT a duplicated shadow
# surface (Canon-9 §3 single-writer discipline extended to tenant
# identity discipline).
TENANT_SCOPE_ENFORCEMENT_ANCHOR: Final[str] = (
    "services.tenant_separation.tenant_registry:CANONICAL_TENANT_IDS"
)


# ---------------------------------------------------------------------------
# R-106 §8(c) invariant 3 · refusal paths (closed-vocab paired-equality)
# ---------------------------------------------------------------------------
#
# Owner R-106 §7 verbatim: 'unreachable surface → BLOCKED row with
# blocker; unreachable GPU hosts → audio deep-analysis marked
# deferred-not-failed'.
# Owner R-106 §4 verbatim: 'response-required item to a queue surfaced
# in the UI'.
#
# Closed-vocab tuple: any code emitted by the engine at a refusal
# path must be a member of this tuple. Additions require a new
# ratchet_history entry + additive test.
REFUSAL_PATH_CLOSED_VOCAB: Final[Tuple[str, ...]] = (
    "BLOCKED_SURFACE_UNREACHABLE",       # R-106 §7 · unreachable surface
    "DEFERRED_GPU_HOST_UNREACHABLE",     # R-106 §7 · unreachable GPU host
    "BLOCKED_AWAITING_RESPONSE",         # R-106 §4 · mid-run decision queue
    "BLOCKED_LAWFUL_BASIS_MISSING",      # Doc-5 B5.2 · pre-first-byte gate
    "BLOCKED_TENANT_SCOPE_MISMATCH",     # R-106 §3 + 4j CP-TENANT-SEPARATION
    "DEFERRED_BUDGET_EXCEEDED",          # R-106 §3 · bounded/budgeted per run
)


# ---------------------------------------------------------------------------
# R-106 §8(c) invariant 4 · no-agent-dependency
# ---------------------------------------------------------------------------
#
# Dotted-path anchor to the supervisor entry-point in
# `scheduler_program.py`. This module runs as a persistent worker under
# supervisord; it MUST NOT be invoked by any pytest harness or
# testing_agent. The service loop lives entirely in `main()` below.
NO_AGENT_DEPENDENCY_ANCHOR: Final[str] = (
    "services.census_autonomy.scheduler_program:main"
)
