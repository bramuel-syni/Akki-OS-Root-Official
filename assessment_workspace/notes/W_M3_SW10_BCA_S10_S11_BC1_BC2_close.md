READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW10 · Business Continuity Annex · S-10 + S-11 + BC-1 + BC-2 — close

**Sub-wave slot:** 10 of M3.  **UTC close:** 2026-09-14T09:07Z.
**Canon:** `Business_Continuity_Annex_v1` Document 3 Part D · §1 (S-10 · BC-1 · BC-2) · §2 (S-11) · §3 (BC-3 · BC-4).

## Scope

New surface `services/business_continuity/anchors.py` pins the BCA canon anchors to the existing mechanism that landed at Wave E (CP-E1 CA1-N5 · CP-E2 CA1-N2) and Wave G5c Ruling #1 (RTO=3600).  The BCA is Doc-3 Part D per its own §4 ("this annex is Document 3, Part D"); this sub-wave brings the extracted canon anchors on-record inside M3 as the milestone binding demands (§E: "M3 — S-10 + S-11 discharge in W-WATCH-STACK Wave-C Part-D-proposed recovery + notification").

## Files landed

* `backend/services/business_continuity/__init__.py`
* `backend/services/business_continuity/anchors.py` — verbatim canon strings + `BCADriftError` + four drift-check helpers.
* `backend/tests/invariants/test_wm3_sw10_bca_s10_s11_bc1_bc2.py` — 10 tests.

## Invariants landed

1. Module fabric present (14 exports).
2. S-10 verbatim quoted (byte-for-byte from §1).
3. S-10 3,600 s pins `continuity_policy.v0.json.rto_target_seconds` (Wave G5c Ruling #1).
4. BC-1 verbatim quoted with key clauses ("Restoration MUST be countersigned by someone independent" + "the verifier cannot be the thing that might be down").
5. BC-1 pins the presence of `services.watch.continuity._witness_or_refuse` (mechanism drift ⇒ RED).
6. BC-2 verbatim quoted with key clauses.
7. BC-2 pins `continuity_policy.v0.json.cadence == "quarterly"` + `cadence_class == "default"`.
8. S-11 verbatim quoted (byte-for-byte from §2).
9. S-11 72 h pins `breach_policy.v0.json.window_hours`.
10. BC-3 + BC-4 markers preserved as `DEFAULT-PENDING-OVERRIDE` — silent flip forbidden until owner rules RPO / site-loss.

## Discipline

Strict tests-first held.  Mechanical RED at `phase0/m3_receipts/20260914T090453Z_M3_SW10_RED.log` (10/10 `ModuleNotFoundError` against `services.business_continuity`).  Double-green byte-match `3782 passed, 1 skipped, 438 warnings` on two consecutive full-suite runs (stripped-timing diff = 0).

## Ratchet

3772 → **3782** (+10)

## Notes

* No mechanism re-implementation.  The BCA-anchor helpers READ the on-disk `continuity_policy.v0.json` + `breach_policy.v0.json` that the runtime services already read; drift between mechanism and canon anchor now fires here as a mechanical RED.
* BC-3 (RPO) and BC-4 (site-loss) remain open per canon §3.  This sub-wave preserves the DEFAULT-PENDING-OVERRIDE markers so that any silent flip breaks the ratchet.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
