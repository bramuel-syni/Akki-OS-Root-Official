READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2E_close.md

**Wave.** W-DAP-STACK · Sub-wave 2E · Metering + cumulative disclosure budget.
**Canon anchors.** DAP-Spec DAP-21 [AU-3], DAP-22 (partial — R-6 pricing OPEN), DAP-25 (fail-closed), DAP-26.
**Marker anchors.** R-C2 (`au_3b_defensible=False` flip-forbidden), S-25 (`DEFAULT_RELEASE_BUDGET = "DEFAULT-PENDING-OVERRIDE"` — blocked on Security R-7).
**Owner authorisation.** Verbatim 2026-09-13: confirmation of G-A..G-E (with G-D/G-E amendments).
**Ratchet.** 3590 → 3600 (+10).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wdap_2e.seal.txt`.

---

## §A · Invariants added (10 new · 1 G-D already-satisfied)

| Test | Anchor | What it enforces |
|---|---|---|
| E2-01 · module fabric present | DAP-21/22/25/26 | `services.dap.metering`, `services.dap.terms`, `services.dap.availability`, `services.dap.disclosure_budget` all importable with expected surface |
| E2-02 · DAP-21 MeteredEvent carries all required fields | DAP-21 verbatim | `operation_type`, `accessed_scope`, `quantity`, `quantity_unit`, `terms_id`, `party_id`, `timestamp_iso` all present on `MeteredEvent` — **G-D case, see §E** |
| E2-03 · DAP-21 write-to-Ledger before result return | DAP-21 verbatim tail | `record_metered_event` appends to the Ledger BEFORE returning; if ledger write raises, `RuntimeError` naming DAP-21 propagates and no receipt is returned |
| E2-04 · DAP-21 R-C2 `au_3b_defensible=False` flip-forbidden | R-C2 marker | Fresh `MeteredEvent` carries `au_3b_defensible=False`; default construction preserves that; field description names `R-C2` |
| E2-05 · DAP-22 three-level resolution most-specific-first | DAP-22 verbatim | `resolve_terms` returns party > custody_class > estate_default in that order |
| E2-06 · DAP-22 receipt cites resolved terms_id, not level | DAP-22 verbatim tail | `MeteredEvent.terms_id` carries the resolved `terms_id`, never the level string |
| E2-07 · DAP-25 default availability is UNAVAILABLE | DAP-25 verbatim | `is_available` returns `OperationAvailability.UNAVAILABLE` for any un-configured `(estate, custody_class, operation)` triple |
| E2-08 · DAP-25 granting one combination does not grant others | DAP-25 verbatim tail | Configuring one triple leaves all other triples still `UNAVAILABLE` (per-combination granting only) |
| E2-09 · DAP-26 terms change is not retroactive | DAP-26 verbatim | Frozen `MeteredEvent` receipts written under earlier terms retain that `terms_id` after a ceremony configures a new one; new receipts pick up the new terms |
| E2-10 · DAP-26 per-party ceiling + release-budget pending-override | DAP-26 + S-25 | `DEFAULT_RELEASE_BUDGET == "DEFAULT-PENDING-OVERRIDE"` (silent flip forbidden); per-party numeric ceiling fails closed on cumulative overflow |

## §B · Mechanism landed

- `backend/services/dap/metering.py` — DAP-21 Ledger + `record_metered_event` (writes BEFORE returning; RuntimeError on write failure).
- `backend/services/dap/terms.py` — DAP-22 three-level resolver with `TermsResolution` inline model (`resolved_terms_id`, `resolution_level`).
- `backend/services/dap/availability.py` — DAP-25 fail-closed availability config with `AVAILABILITY_DEFAULT_UNAVAILABLE = OperationAvailability.UNAVAILABLE`.
- `backend/services/dap/disclosure_budget.py` — DAP-26 per-party ceiling accumulator + S-25 `DEFAULT_RELEASE_BUDGET` pending-override marker + `CeilingCheck` result model.
- `backend/tests/invariants/test_wdap_2e_metering_and_cumulative_disclosure.py` — 10 invariants; every test docstring quotes its DAP-Spec anchor verbatim.
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3590 → 3600; ratchet_history entry appended for 2E.

## §C · Markers held (flip-forbidden)

- **R-C1**: `ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK` — carried forward. Rules-Service still not built.
- **R-C2**: `MeteredEvent.au_3b_defensible=False` — now invariant-asserted by E2-04 (default construction preserves False; description names R-C2). Doc-0 G-8 still open.
- **C4 · DAP_R2**: `DAP_R2_APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE` — carried forward from 2C.
- **S-25 (new this wave)**: `DEFAULT_RELEASE_BUDGET = "DEFAULT-PENDING-OVERRIDE"` — flip-forbidden until Security R-7 rules the estate-wide release budget number.
- **DPO · DAP-22 R-6 pricing**: R-6 tariff/pricing dependency remains OPEN. 2E lands DAP-22 pricing RAILS only (terms resolution + receipt citation); no tariff/billing/price computation.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T155239Z_wdap_2e_RED.log` | `b29fb9f00f5c1a06aa8188ef0b5dc006a325d4e9e7bbe35ee0f9848918e9aa78` |
| GREEN 1 | `phase0/drill_receipts/20260913T155423Z_wdap_2e_GREEN1.log` | `2002d2a2c688578819ee83814e5d19839d4dff462f51279e2511ae561d40ad60` |
| GREEN 2 | `phase0/drill_receipts/20260913T155624Z_wdap_2e_GREEN2.log` | `452c7414c3f726214ed13c0dd63fc211964b7254d82e38d91c1bcac3b8c5c7de` |
| **Rider 1** pip freeze (187 pkgs) | `phase0/drill_receipts/20260913T155830Z_wdap_2e_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only (3601 items) | `phase0/drill_receipts/20260913T155830Z_wdap_2e_COLLECTONLY.txt` | `76994e3bddce0a39ce1c6bb54e5d06dc46a3b4a4210baad6c3109f787790ff39` |
| Seal | `phase0/output_verified_seals/wdap_2e.seal.txt` | — |
| Byte-match | Both GREEN runs 3600 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37106 bytes | — |

### RED reason verbatim (right-reason check)

The mechanical RED demonstrated 9 failures — 8 with `ImportError: cannot
import name '<module>' from 'services.dap'` and 1 with `AssertionError`
on the module-fabric probe.  1 test (`test_dap_21_metered_event_carries_all_required_fields`)
passed at RED time because MeteredEvent was already landed in W-DAP-STACK
2A (commit `e578582`) — see §E.

## §E · G-D · already-satisfied row (per owner amendment 2026-09-13)

Per G-D as amended by owner verbatim: *"if mechanical RED cannot be
produced because banked code ALREADY satisfies the row — do NOT
fabricate a failing test, and do NOT halt.  Instead: (1) document the
finding as `RED-NOT-PRODUCIBLE: already satisfied by <commit/service
ref>` with evidence; (2) land the invariant test anyway as a regression
guard (it passes immediately — that is the truthful state); (3) list
every such row in a dedicated section of the block completion report
for review."*

| Row | Provenance | Disposition |
|---|---|---|
| E2-02 · DAP-21 MeteredEvent carries all required fields | `RED-NOT-PRODUCIBLE: already satisfied by W-DAP-STACK 2A commit e578582 · contracts/dap.py:237-257`. MeteredEvent + all 6 required DAP-21 fields were landed as schema in the 2A wave. | Landed as regression guard (test passes immediately). No fabrication. Listed here + in block completion report per G-D. |

## §F · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-21 (metering with all six fields + write-before-return + R-C2 marker), DAP-25 (fail-closed availability defaults + granted-never-assumed), DAP-26 (three-level terms non-retroactivity + per-party ceiling mechanism).
- **Partial** — DAP-22 (rails only: three-level resolution + receipt cites resolved terms_id; NO tariff/pricing/billing — R-6 stays OPEN). `DEFAULT_RELEASE_BUDGET = "DEFAULT-PENDING-OVERRIDE"` marker landed for S-25 (blocked on Security R-7).
- **A4 (Metering completeness)** — mechanism landed at kernel grade: any of the six §4 operations now writes a MeteredEvent to the Ledger before result return. Full A4 discharge (six-op run) happens when 2F..2H compose the operations end-to-end; the write-before-return + Ledger surface is the mechanism.
- **A5 (Slow-play cumulative)** — cumulative accumulator landed (`record_disclosure` + `check_disclosure_ceiling`); ready to feed 2G coalition joint evaluation. Slow-play scaffold from 2A (`services/dap/admission.py`) now composes with this accumulator.

## §G · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- No egress. Radio T4 held. Playwright/Chromium download authorised under Gate 2 Option B remains reserved for CP10 (not used in 2E).
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- Rider-2 `ENV-DRIFT-2TESTS-20260913` remains tracked-open; no impact this wave.
- `SEC-2026-09-12-01` (leaked HF token) remains owner-side; builder not touching.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
