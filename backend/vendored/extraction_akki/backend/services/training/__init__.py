"""Training module · Doc 17 + Incremental Training Capacity Briefing.

Ships the minimum viable slice for W11 CP3:
  * ``demand_table`` — Objective → Demand Table with named-failure admissibility.
  * ``capacity_ledger`` — per-scheme, per-stratum capability rows with
    provenance-day-one. Empty at ship.
  * ``test_set_seal`` — live-verified stratified sample seal against the
    on-disk data_connection_record for the source. Refuses honestly when
    the record is stale or link_working=false.
  * ``state`` — rollup for the /training React surface. REFERENCE-NOT-COPY.

Per-Owner deprioritization at CP3 open (verbatim):
  "Capacity Ledger ships as record + basic read view only — defer
   advanced accounting/forecasting. Defer A18.6 async delivery entirely."
"""
