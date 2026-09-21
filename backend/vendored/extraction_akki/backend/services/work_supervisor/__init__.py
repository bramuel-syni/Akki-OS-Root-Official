"""services.work_supervisor — W1 · L5 Work-Supervisor kernel (case-agnostic).

Owner ruling verbatim (2026-09-13, CP breakdown approval):

    "CORRECTION — job_kind must stay CASE-AGNOSTIC ... Do NOT lock a
    closed 5-value audio-harvest enum into the platform JobManifest at
    CP1 — that leaks the audio case into generic platform code. Instead
    make job_kind reference an OPEN, registry-backed kind: a capability/
    job-kind REGISTRY that jobs register into."

W1 landing order:
  CP1 · kind_registry + job_manifest        (this CP)
  CP2 · admission supervisor
  CP2b · runtime supervisor + STANDING ORDER §3.2
  CP3 · governance primitives
  CP4 · supervisor + governance compose freeze
  CP5 · wave close

Freeze: see grounding brief at
notes/W1_WORK_SUPERVISOR_grounding_brief.md.
"""
from __future__ import annotations
