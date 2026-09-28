"""services.release_gate — release-gate services package.

Landing wave: W-RELEASE-GATE-PILOT-LIFT (chartered 2026-09-15T~03:55Z, formal M5,
grounding brief: notes/wave_release_gate_pilot_lift_grounding_brief.md).

Subpackage plan (per grounding brief §B):
- `release_ledger.py`  (CP-RG1) — append-only release-ledger writer + record_debit.
- `tokenization.py`    (CP-RG2) — placeholder (planned CP-RG2 landing).
- `admission.py`       (CP-RG4) — end-to-end admit_transcript_release wiring
                                   (planned; may extend services.audio_poc.release_gate).
- `aggregate_usage.py` (CP-RG5) — pilot-end aggregate-usage query API.

Existing service `services.audio_poc.release_gate` (module, not package) remains
the concrete transcript-artefact gate; this package is the composed/generalised
lift landing across CP-RG1..RG5.
"""
