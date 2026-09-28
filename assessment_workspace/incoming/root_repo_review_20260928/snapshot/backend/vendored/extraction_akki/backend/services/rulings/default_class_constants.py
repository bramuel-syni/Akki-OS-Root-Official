"""backend/services/rulings/default_class_constants.py

DEFAULT-class ruled values, wired tests-first per owner directive
2026-09-08T~06:15Z STEP 3 (banked verbatim in STATE/DECISIONS.md):

    Wire every DEFAULT-class value into config where mechanism exists
    (countdown lengths, key rotation, recommendation window) — tests-first
    where contracts change.

Every constant in this module is frozen by
`backend/tests/invariants/test_default_class_ruled_constants.py`. If the
owner overrides a DEFAULT-class value later, the invariant is amended in
the SAME commit that flips the value. A DEFAULT value is never silently
changed.

Owner rule label on each value:
  - RATIFIED = owner explicitly approved (binding immediately)
  - DEFAULT-class = owner set a working value, revisable on evidence

References:
  - notes/RULING_LEDGER.md (human-readable status)
  - STATE/DECISIONS.md 2026-09-08T~06:15Z (verbatim owner directive)
"""
from __future__ import annotations

from typing import Final


# -------- Rules-Service R-1 · countdown lengths (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Rules-Service R-1 countdown = 48h system-ordinary / 7 days system-TCB"
RULES_SERVICE_COUNTDOWN_SYSTEM_ORDINARY_HOURS: Final[int] = 48
RULES_SERVICE_COUNTDOWN_SYSTEM_TCB_DAYS: Final[int] = 7


# -------- DAP R-4 · API-key rotation (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "DAP R-4 API-key lifetime = 90-day rotation"
DAP_API_KEY_LIFETIME_DAYS: Final[int] = 90


# -------- Security R-10 · recommendation window (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Security R-10 recommendation window = 24h"
SECURITY_RECOMMENDATION_WINDOW_HOURS: Final[int] = 24


# -------- Security R-8 / R-9 / R-11 · baseline-period approach (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Security R-8/R-9/R-11 = baseline-period approach"
SECURITY_R8_APPROACH: Final[str] = "baseline_period"
SECURITY_R9_APPROACH: Final[str] = "baseline_period"
SECURITY_R11_APPROACH: Final[str] = "baseline_period"


# -------- Agent-Containment R-3 · sample rate / observation window (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Agent-Containment R-3 sample rate/observation window = baseline-period approach"
AC_R3_APPROACH: Final[str] = "baseline_period"


# -------- Pruning R-12 · re-derivation default (DEFAULT-class) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Pruning R-12 = re-derivation is default, recall requires explicit
#    case-by-case owner sign-off"
PRUNING_R12_DEFAULT: Final[str] = "re_derivation"
PRUNING_R12_RECALL_REQUIRES_OWNER_SIGNOFF: Final[bool] = True


# -------- Rules-Service R-4 · taxonomy (RATIFIED) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Rules-Service R-4 taxonomy ratified as proposed"
RULES_SERVICE_R4_STATUS: Final[str] = "ratified_as_proposed"


# -------- DAP R-1 · controlled-unit definition (RATIFIED) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "DAP R-1 controlled-unit definition ratified as proposed"
DAP_R1_STATUS: Final[str] = "ratified_as_proposed"


# -------- Agent-Containment R-1 · capability-ceiling list (RATIFIED) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Agent-Containment R-1 capability-ceiling list ratified as proposed"
# The four ceilings, verbatim from agent_containment_spec_v1 §4 AC-1:
AGENT_CONTAINMENT_R1_CEILINGS: Final[tuple[str, ...]] = (
    "no_self_replication",
    "no_unauthorised_resource_acquisition",
    "no_unauthorised_credential_escalation",
    "no_self_access_to_oversight",
)


# -------- Rules-Service R-3 · witness (RATIFIED) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Rules-Service R-3 witness = same witness the Watch already uses (C3)"
RULES_SERVICE_R3_WITNESS_SOURCE: Final[str] = "watch_c3"


# -------- Agent-Containment R-2 · scope-ratifying authority (RATIFIED) --------

# Owner ruling 2026-09-08T~06:15Z verbatim:
#   "Agent-Containment R-2 scope-ratifying authority = Syni.ai for early
#    deployments"
AGENT_CONTAINMENT_R2_SCOPE_RATIFYING_AUTHORITY: Final[str] = "syni_ai"
AGENT_CONTAINMENT_R2_SCOPE_RATIFYING_STAGE: Final[str] = "early_deployments"


__all__ = [
    "RULES_SERVICE_COUNTDOWN_SYSTEM_ORDINARY_HOURS",
    "RULES_SERVICE_COUNTDOWN_SYSTEM_TCB_DAYS",
    "DAP_API_KEY_LIFETIME_DAYS",
    "SECURITY_RECOMMENDATION_WINDOW_HOURS",
    "SECURITY_R8_APPROACH",
    "SECURITY_R9_APPROACH",
    "SECURITY_R11_APPROACH",
    "AC_R3_APPROACH",
    "PRUNING_R12_DEFAULT",
    "PRUNING_R12_RECALL_REQUIRES_OWNER_SIGNOFF",
    "RULES_SERVICE_R4_STATUS",
    "DAP_R1_STATUS",
    "AGENT_CONTAINMENT_R1_CEILINGS",
    "RULES_SERVICE_R3_WITNESS_SOURCE",
    "AGENT_CONTAINMENT_R2_SCOPE_RATIFYING_AUTHORITY",
    "AGENT_CONTAINMENT_R2_SCOPE_RATIFYING_STAGE",
]
