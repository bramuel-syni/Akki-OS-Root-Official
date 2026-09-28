"""services.skill_files — Doc 18 A18.7 provenance chain persistence + rollup.

CP4 minimum viable slice:
  * ``persistence`` — write-once JSONL append (workspace phase0/).
  * ``state``       — rollup for the /skill-files React surface.
  * ``router``      — /api/skill-files/state + /api/skill-files/{skill_id}/provenance.

Persistence discipline mirrors ``services.training.capacity_ledger``:
governed JSONL under a workspace path. No MongoDB dep at CP4 —
the MongoDB persistence for callable_skills already exists at
``services.transform_forms.callable_skill_persistence``; this module
adds the provenance-chain sidecar that Doc 18 A18.7 requires.
"""
