"""R-88 first slice · CP-CONTENT-REGISTRY-WAVE · SO §2.5 verbatim-docstring package marker.

The `services.content_registry` package hosts the load-bearing
vocabulary-registration modules for Content Registry Spec v1 (Ruling 4 ·
CON-1..CON-31). This __init__.py is deliberately empty at first-slice
landing — the package structure is additive per SO §3.8, and downstream
slices (R-89 second slice · R-90 third slice) will land sibling modules
without disturbing the package identity established at this-commit.

Authority chain:
- Owner Ruling 4 verbatim (banked in STATE/DECISIONS.md OWNER RULINGS
  anchor · re-affirmed at `1250c39a` + R-86 Commit-C `e40047f4` +
  R-87 Commit-C `9823a520`).
- Master Requirements Registry v5 System Rules Registry sheet as
  authority per Ruling 5 (sha256 `00072c58…` · ratified at `1250c39a`).
- Content Registry Spec v1 canon docx at
  `custody/owner_drops/20260920T1600Z/Content_Registry_Spec_v1.docx`
  (cited for section numbering only · SRR is authoritative).
- CP-BLOCKED-VOCABULARY-CORRECTION seal `200c2c63/b4526572/9823a520`
  (R-87 immediately-precedes · establishes vocabulary-registration-
  via-Final-constants pattern this wave inherits).
"""
