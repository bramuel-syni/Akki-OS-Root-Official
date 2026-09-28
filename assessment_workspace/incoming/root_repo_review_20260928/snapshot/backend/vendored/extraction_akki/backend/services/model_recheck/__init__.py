"""services.model_recheck — CA1-011 re-check state (W7 half).

Orchestrator Ruling 2026-08-25T23:15Z (CA1-011 SPLIT): W7 lands the
re-check-date register + surfacing; W9 lands the Watch-routed
enforcement. This module is the W7 half — status queries and honest
renders. The Watch route is a NAMED SEAM on every status payload
(`services.watch.route_recheck_failure (lands W9)`) so W9 has a
binding point.

Do NOT fake the enforcement half in W7 (owner ruling verbatim).
"""
from services.model_recheck.status import status_for

__all__ = ["status_for"]
