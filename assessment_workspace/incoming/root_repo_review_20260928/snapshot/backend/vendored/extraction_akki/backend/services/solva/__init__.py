"""services.solva — the reasoning faculty (W5).

Owner correction 2026-08-25 · canon vocabulary is Solva.
Owner Order 2026-08-25 · 'W5 go' §5:
    "Solver: prefer the Akki-Executive-Final services/solva/ donor
     (cleaner shape per your own finding)"

ADAPTED from Akki-Executive-Final/backend/services/solva/reasoning/
(frame_audit_engine.py, candidate_generation.py, refusal_logic.py) —
subset carrying only the three W5 stages: frame_audit, candidate
generation, synthesis. Triangulation + tension detection + probability
weighting are DEFERRED to W6+ under Grey Mirror groundwork.

Every stage transits `services.chokepoint.llm.invoke()`. NO direct SDK
import. NO canned fallback text — on shield refusal, the stage surfaces
the refusal verbatim (Owner sharpening §4 · A8-Q3).

Persistence: `phase0/solva_runs/run-<hex>.json` records the three stage
receipt IDs joined by identity (REFERENCE-NOT-COPY).
"""
