"""W-Orchestrator-Resilience-r1 · resilience primitives for pod-side
orchestrators (initially: `tools/gpu_burn_orchestrator.py`).

Charter (STATE/DECISIONS.md · 2026-09-01T02:55Z reconcile section,
banked from owner sequencing directive 2026-09-06):

  "Scope: heartbeat + watchdog on the pod-side orchestrator, resumable
   polling (a restarted poller re-attaches to a running on-host job
   from its sealing/poll receipts rather than losing the window), and
   a reconcile-on-start path that detects orphaned on-host jobs."

Sub-modules:
  * heartbeat.py       — point-in-time liveness records
  * orphan_detector.py — scan run dirs, find orphaned on-host jobs
  * resume.py          — read prior poll receipts, compute next-poll
                          state, idempotent should_poll_at_elapsed

Discipline: zero-influence (matches WPW-2/A2). Every writer swallows
its own storage errors and returns a False/None sentinel rather than
raising. The resilience layer is an observer; it never terminates,
mutates, or otherwise participates in the run's critical path.
"""
