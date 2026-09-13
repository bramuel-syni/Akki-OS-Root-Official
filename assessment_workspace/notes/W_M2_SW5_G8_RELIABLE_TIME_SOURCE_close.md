READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW5 · W-G8-RELIABLE-TIME-SOURCE — close

**Sub-wave slot:** 5 of M2 · G-8 gap close.
**UTC close:** 2026-09-13T19:33Z · IN window.
**Canon anchors:** Doc-0 G-8 · SP 800-53 AU-3(b) · Ratification_Record_v1 R-16.
**track-a commit:** `f4fc201`.

## Scope

Landed a `ReliableClock` that emits AU-3(b)-defensible timestamps when anchored to a reference source and inside a bounded drift budget.  Enables R-C2 retirement opt-in — callers that use the clock's defensible stamp can construct records with `au_3b_defensible=True`.

## Files landed

- `backend/services/reliable_time_source/__init__.py`
- `backend/services/reliable_time_source/clock.py`
- `backend/tests/invariants/test_wm2_sw5_g8_reliable_time_source.py` (7 invariants)

## R-C2 governed retirement (opt-in style)

The R-C2 lineage-anchor invariants on `services/mtafiti/asset_registry_writer.py`, `services/dap/metering.py`, and `services/solva_v2/trace.py` remain in force — the module-level marker comment (`R-C2 …`) is preserved on each source so a silent flip is still caught.  The mechanism (`au_3b_defensible_now()`) is now callable; the DEFAULT record shape stays `au_3b_defensible=False` until each individual writer wave (M3 W-WATCH-STACK / M3 W-AGENT-CONTAINMENT / etc.) wires the clock explicitly.  Justification: flipping the defaults now would break the invariants that assert R-C2 marker presence on the writers themselves; opt-in retirement lets each downstream wave land its own governed flip.

**Enabling commit:** `track-a f4fc201`.
**Governance:** R-16 open (ratifier + cadence).  R-15 open (initial certificate library seed) shares the same governance ceremony.

## Ratchet

- Before: **3665** (SW4 close)
- After:  **3672** (+7)

## Discipline

- Mechanical RED: `phase0/m2_receipts/20260913T192900Z_M2_SW5_RED.log` (7 fails · right-reason `ModuleNotFoundError`).
- GREEN #1: `20260913T193100Z_M2_SW5_GREEN1.log` — `3672 passed · 1 skipped · 116.47s`.
- GREEN #2: `20260913T193300Z_M2_SW5_GREEN2.log` — `3672 passed · 1 skipped · 115.93s` (byte-match).
- Rider 1: `20260913T193300Z_M2_SW5_PIPFREEZE.txt` (190 lines · zero delta).

## Two-commit local (no push)

- track-a `f4fc201` · master this commit.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
