"""services.registry_facts — Registry surface facts assembler.

Owner Order 2026-08-19 · DECISIONS.md · FL-P2-25.

Reads the estate's durable JSON records from phase0/ and assembles a
read-only facts dict for GET /api/registry/facts. NEVER invents a figure:
if a fact is not in a record on disk, it is not served.

  - data_sources ← phase0/data_connection_records/*_FINAL.json
  - compute       ← phase0/commissioning_records/*_ACCEPTED.json
  - models        ← []  (no records yet; honest empty)

No secret material transits this module.
"""
