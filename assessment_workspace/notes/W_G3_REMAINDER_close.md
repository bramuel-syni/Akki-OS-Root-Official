READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_G3_REMAINDER_close.md

**Wave.** `W-G3-REMAINDER` — Mtafiti full asset-inventory generalisation. Doc-0 G-3 mechanical-half REMAINDER (the Mtafiti-side extension left open after predecessor wave W-REGISTRY-EXTENSION-G3 closed the schema half).
**Canon anchors.** Doc-0 §STATUS AS OF row G-3, Doc-0 Component 4 BR-4.1, Doc-0 Attribute 3 §TA-3.1, Canon-9 §3, Canon-3 §22.1, Canon-1 §4.6 extension-not-sibling.
**Owner authorisation.** Verbatim 2026-09-13: G-A ratified sequence's terminal item "G-3 remainder, exactly as stated" (STOP before M2).
**Ratchet.** 3627 → 3633 (+6).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wg3_remainder.seal.txt`.
**Predecessor.** `W-REGISTRY-EXTENSION-G3` (commit `33edf56` · closed 2026-09-13 · ratchet 3531).

---

## §A · Invariants added (6 new)

| Test | Anchor | What it enforces |
|---|---|---|
| GS-01 · module fabric present | Canon-1 §4.6 | `services.mtafiti.asset_inventory` importable with `list_all_assets`, `count_by_class`, `enumerate_classes_always_five`, `cross_class_governance_query`, `single_writer_still_holds` |
| GS-02 · BR-4.1 · all 5 AssetClass kinds covered | Doc-0 BR-4.1 verbatim | Given one record per each of the 5 `AssetClass` kinds, `count_by_class()` returns all 5 keys with correct counts. No class missing. |
| GS-03 · BR-4.1 · no asset hidden from inventory | Doc-0 BR-4.1 verbatim | Every written record retrievable via `list_all_assets()`; every `receipt_id` returned matches the writer's WriteReceipt.receipt_id (deterministic content-hash). |
| GS-04 · TA-3.1 · enum stable at zero records | Doc-0 TA-3.1 verbatim | With EMPTY inventory, `enumerate_classes_always_five()` still returns all 5 asset-class names. Silent flip forbidden. |
| GS-05 · BR-4.1 · cross-class governance query | Doc-0 BR-4.1 + Canon-3 §22.1 | Three-filter query `(custody_class, asset_class, owner_class)` returns exactly the intersection; each filter honored. |
| GS-06 · Canon-9 §3 · single writer preserved | Canon-9 §3 verbatim | `single_writer_still_holds()` returns True; no `write_*`/`append_*`/`update_*`/`delete_*`/`add_*`/`put_*`/`set_*` public name on the inventory module surface. Predecessor's CP-R6 negative-scan `test_wregext_g3_cp_r6_no_second_writer_negative_scan` STILL PASSES (no `ASSET_REGISTRY_COLLECTION` or `write_asset_record` reference in the new module). |

## §B · Mechanism landed

- `backend/services/mtafiti/asset_inventory.py` (~90 lines · reader-only surface composing OVER `services.mtafiti.asset_registry_writer` without touching it; `list_all_assets`, `count_by_class`, `enumerate_classes_always_five`, `cross_class_governance_query`, `single_writer_still_holds`).
- `backend/tests/invariants/test_w_g3_remainder_asset_inventory_generalisation.py` — 6 invariants; each test docstring quotes its Doc-0 / canon anchor verbatim.
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3627 → 3633; ratchet_history entry appended.

## §C · Zero-churn discipline preserved

Per W-REGISTRY-EXTENSION-G3 close §E: *"Zero track-a churn to prior-wave code."*  This wave preserves that by:
- **Untouched**: `backend/contracts/asset_registry.py` (predecessor schema).
- **Untouched**: `backend/services/mtafiti/asset_registry_writer.py` (predecessor writer).
- **Untouched**: predecessor tests `test_wregext_g3_cp_r{1..6}*.py`.
- **New only**: `services/mtafiti/asset_inventory.py` (reader-only) + one new invariant file.
- **Reused**: `AssetClass`, `CustodyClass`, `_REGISTRY`, `_compute_receipt_id` — imported, not redefined.

Canon-1 §4.6 "extension not sibling" doctrine held: no new registry, no sibling collection, no second write path.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T164948Z_wg3_remainder_RED.log` | `a15cd2794def774f126b34acea743da77773611ffd0c5517372f1a74e68f2af9` |
| GREEN 1 (authoritative) | `phase0/drill_receipts/20260913T165725Z_wg3_remainder_GREEN1.log` | `7d6fcd34d6bd391f3e4412a44709b2f37c82220b72bb23b0b1c4d1b871415932` |
| GREEN 2 (authoritative) | `phase0/drill_receipts/20260913T165929Z_wg3_remainder_GREEN2.log` | `30fbb37199c7936e73d999a4bc3173a51a3d2fecf21d000ed372a2c7093aa79e` |
| **Rider 1** pip freeze (190 pkgs, unchanged from CP10) | `phase0/drill_receipts/20260913T170139Z_wg3_remainder_PIPFREEZE.txt` | `f6296cd2848bcf2eb6189ed1c68c35a7f262317f90ef176df3cf69b24c6778a0` |
| **Rider 1** collect-only (3634 items) | `phase0/drill_receipts/20260913T170139Z_wg3_remainder_COLLECTONLY.txt` | `ace8a2d2e66dfdee98f4e87954c4c8336af95390d27337749c195392296636ab` |
| Seal | `phase0/output_verified_seals/wg3_remainder.seal.txt` | — |
| Byte-match | Both authoritative GREEN runs 3633 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37749 bytes | — |

### Intermediate iteration receipts (honesty record)

Two intermediate GREEN1 attempts (`165210Z`, `165503Z`) preceded the authoritative GREEN1. These are BANKED as evidence of two mid-wave defects and their remediation:
1. `165210Z`: test-authoring field-name errors (I used `name=` / `owner=` / `freshness_stamp={...unknown fields...}` on `AssetRegistryRecord`; predecessor's `extra="forbid"` refused them). Fix: use `asset_ref=`, `named_owner=`, `freshness_stamp={"logged_date": "..."}`.
2. `165503Z`: my inventory docstring mentioned `asset_registry_writer.write_asset_record()` which tripped predecessor's `test_wregext_g3_cp_r6_no_second_writer_negative_scan` (case-insensitive string scan over `services/`). Fix: rewrite docstring without the reference.

### RED reason verbatim (right-reason check)

Mechanical RED demonstrated 6/6 right-reason `ImportError: cannot import name 'asset_inventory' from 'services.mtafiti'`. No G-D already-satisfied rows in this wave.

## §E · Promises discharged

- **Doc-0 §STATUS AS OF row G-3 · mechanical-half remainder** — fully discharged this wave. Mechanical half is now complete:
  - Schema (predecessor wave 2026-09-13 morning): `AssetClass` × 5, `AssetRegistryRecord`, `NamedOwner`, `CustodyClass`, `WriteReceipt` (R-C2 carrier).
  - Writer (predecessor wave): `write_asset_record` idempotent, single-writer.
  - Reader (this wave): `list_all_assets`, `count_by_class`, `enumerate_classes_always_five`, `cross_class_governance_query` + `single_writer_still_holds` self-check.
- **Doc-0 Component 4 BR-4.1 STATUS** lifted from `"Not Met — current coverage is estate sources only (Promises #12, #13)"` to `"Met at kernel grade for the 5-AssetClass taxonomy currently in schema."` If BR-4.1 needs a wider taxonomy later, that is a follow-on wave (owner scope question per MILESTONE_PROMISE_BINDING line 469 — remains open: M2 Attr-3 or a separate wave).
- **Doc-0 §TA-3.1** — `enumerate_classes_always_five()` proves finite-list-at-zero-records invariant.
- **Doc-0 G-3 · documentary half (general triad formalisation)** — remains DEFERRED per predecessor's §F. Documentary wave, not mechanical; owner scope question.

## §F · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- Egress: none this wave. Playwright/Chromium install from CP10 remains the only public egress this session.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close (env-delta unchanged from CP10).
- ENV-DRIFT-2TESTS-20260913 remains tracked-open.
- SEC-2026-09-12-01, SEC-2026-09-13-T4-01, SEC-2026-09-13-T4-02, SEC-2026-09-13-T4-03 remain owner-side; builder not touching.

## §G · Block sequence complete

**Ratified sequence per G-A (owner verbatim 2026-09-13):** *"2E → 2F → 2G → 2H → CP10 → G-3 remainder, exactly as stated."*

All six waves closed this session:

| Wave | Delta | Ratchet | Track-a commit |
|---|--:|--:|---|
| W-DAP-STACK 2E | +10 | 3600 | `c383eb1` |
| W-DAP-STACK 2F | +9 | 3609 | `dbb0b02` |
| W-DAP-STACK 2G | +8 | 3617 | `9adccaa` |
| W-DAP-STACK 2H | +8 | 3625 | `47c5d05` |
| W-REGISTRY-FULL-BUILD CP10 | +2 | 3627 | `b51bfb0` |
| W-G3-REMAINDER (this wave) | +6 | 3633 | PENDING backfill |

Plus housekeeping (2B/2C state backfill + 2D full close): 3560 → 3590 (+30).
Plus T4 side-task banked (JUMP PASS + RADIO NETWORK_TIMEOUT · admin bastion Q&A ratified).

**Cumulative this session: 3560 → 3633 (+73 invariants across 6 waves + housekeeping).**

**STOP before M2 per owner instruction.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
