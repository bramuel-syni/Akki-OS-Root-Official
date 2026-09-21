"""services.census_engine — RDS Data API multi-database census.

Wave-G5c-CENSUS. Owner rulings 2026-08-28T~14:30Z + 2026-08-28T~15:00Z
banked verbatim in STATE/DECISIONS.md.

Aggregates-only chokepoint. Never emits MIN( or MAX( in SQL. Never
carries row values across the seam. Numbering starts at #1 — the
prototype's fictional "Census #4" is not history, it is copy.
"""
