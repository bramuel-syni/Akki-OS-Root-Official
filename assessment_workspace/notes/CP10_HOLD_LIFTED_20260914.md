READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP10 HOLD · LIFTED · 2026-09-14T10:00Z

Owner ruling recorded verbatim, dated 2026-09-14:

> *"CP10 - confirm."*

## Effect

**W-REGISTRY-FULL-BUILD · CP10** wave-close is DONE.  The Owner-HOLD placed on CP10 (originally recorded in `STATE/NEXT.md` line 71 and echoed forward through W_M3_BLOCK_CLOSE_MANIFEST_20260914.md line 69) is now LIFTED by owner confirmation.

## Evidence already on record (referenced, not re-proven)

* **Close manifest**: `notes/W_REGISTRY_FULL_BUILD_close.md` — names all 10 CPs of W-REGISTRY-FULL-BUILD.
* **CP10 wave-close tests**: `tests/invariants/test_w_registry_full_build_cp10_wave_close.py` — 2 tests, both GREEN.  Committed at track-a `b51bfb0` ("W-REGISTRY-FULL-BUILD CP10 · real-Chromium DOM proof · finalized").
* **Harness ground-truth receipt**: `phase0/harness_ground_truth/latest.json` at `2026-09-14T05:15:51Z` (well within the 12 h freshness threshold enforced by `test_cp10_harness_receipt_is_still_recent`).
* **Real-Chromium proof screenshots** at `phase0/eyeball_proxies/` (per prior CP10 sessions).

## Manifest updates

* `notes/W_M3_BLOCK_CLOSE_MANIFEST_20260914.md` — CP10 line moved from "on owner HOLD; drafted close test still shelved-untracked" to "HOLD LIFTED by owner 2026-09-14; CP10 is DONE."

## Scope of this record

This is a governance / status-of-record update.  No new mechanism landed; no ratchet change; no test invariants added (the CP10 tests were already tracked and passing).  Two commits (local, no push) capture the status flip on the master state branch only.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
