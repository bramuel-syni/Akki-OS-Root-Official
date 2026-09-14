READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW5 · Watch Learning L-4 · research queue — close

**Sub-wave slot:** 5 of M3.  **UTC close:** 2026-09-14T05:46Z.
**Canon:** Watch_Learning_Amendment_v1 L-4 (A5.22 + AC-16).

## Scope

Unsure-case research queue.  Three-role-one-order flow enforced: CIF proposes → Solva grounds → human ratifies.  Skipping a stage refuses (`LoopOrderViolation`).  AC-16 fold-in: an accepted ratification re-classes prior identical cases (same `verdict_signature`) but the actions taken on each stand as taken.

## Ratchet

3740 → **3746** (+6)

## Files landed

- `backend/services/watch/research_queue.py`
- `backend/tests/invariants/test_wm3_sw5_watch_learning_research_queue.py` (6 invariants)

## DEFAULT-PENDING-OVERRIDE markers introduced

- `services.watch.research_queue.RESEARCH_QUEUE_R16_CADENCE_PENDING_OVERRIDE = "PENDING-OVERRIDE"` — R-16 open owner-input.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
