READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2G_close.md

**Wave.** W-DAP-STACK · Sub-wave 2G · Coalition joint evaluation + estate-wide bound.
**Canon anchors.** DAP-Spec DAP-34 [S-23 · Doc 0 Att 3 · Doc 3 A5.18], DAP-35 [S-25 · new mandatory baseline], `canon_agent_containment_spec_v1` AC-10.
**Owner authorisation.** Verbatim 2026-09-13 confirmation of G-A..G-E with G-D/G-E amendments.
**Ratchet.** 3609 → 3617 (+8).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wdap_2g.seal.txt`.

---

## §A · Invariants added (8 new)

| Test | Anchor | What it enforces |
|---|---|---|
| G2-01 · module fabric present | DAP-34/35/AC-10 | `services.dap.coalition` importable with `link_shared_party`, `link_shared_mandate_lineage`, `resolve_coalition`, `check_joint_ceiling`, `record_joint_disclosure`, `joint_disclosure_used`, `set_coalition_ceiling`, `set_estate_wide_ceiling`, `DEFAULT_ESTATE_WIDE_BUDGET`, `R11_COORDINATION_SIGNATURE_DEFERRED`, `Coalition`, `JointCeilingCheck` |
| G2-02 · DAP-34 shared party = one coalition | DAP-34 verbatim | Two agents under the same parent party resolve to the same `coalition_id`; joint disclosure sums across members |
| G2-03 · DAP-34 shared mandate lineage = one coalition | DAP-34 verbatim | Two parties sharing a `parent_mandate_id` resolve to the same coalition |
| G2-04 · DAP-34 coordination signature deferred to R-11 | DAP-34 tail + §5 note | `R11_COORDINATION_SIGNATURE_DEFERRED = 'DEFAULT-PENDING-OVERRIDE'`; module docstring names R-11 as deferred (friction-only per A5.2 until R-11 rules) |
| G2-05 · DAP-35 estate-wide budget default-pending-override | DAP-35 + R-7 | `DEFAULT_ESTATE_WIDE_BUDGET = 'DEFAULT-PENDING-OVERRIDE'` — silent flip forbidden |
| G2-06 · DAP-35 estate-wide ceiling sums across ALL parties | DAP-35 verbatim | Numeric ceiling set for test; sum-across-all-parties fails closed on cumulative overflow |
| G2-07 · DAP-35 breach is a floor violation, severance-eligible | DAP-35 verbatim tail | `evaluate_estate_wide_breach` returns `floor_violation=True`, `severance_eligible=True`, reason names DAP-35 |
| G2-08 · AC-10 hard ceiling bounds aggregate agent effect (jointly) | AC-10 verbatim | Two agents sharing an operator → one coalition → coalition ceiling summed across; 12 + proposed 15 > 20 → refuse |

## §B · Mechanism landed

- `backend/services/dap/coalition.py` (~230 lines · coalition graph via union-find over structural edges: shared party, shared mandate lineage; `resolve_coalition` returns `Coalition(coalition_id, members)`; joint accumulator sums per coalition; estate-wide accumulator sums across all parties; per-coalition + estate-wide numeric ceilings; `EstateWideBreachVerdict` with `floor_violation` / `severance_eligible` flags per DAP-35 tail).
- `backend/tests/invariants/test_wdap_2g_coalition_and_estate_wide_bound.py` — 8 invariants; every test docstring quotes its canon anchor verbatim.
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3609 → 3617.

## §C · Markers held (flip-forbidden)

- R-C1, R-C2, C4 DAP_R2, S-25 `DEFAULT_RELEASE_BUDGET` (2E) — all carried forward.
- **DAP-35 estate-wide budget (new this wave)**: `DEFAULT_ESTATE_WIDE_BUDGET = "DEFAULT-PENDING-OVERRIDE"` — flip-forbidden until Security R-7 rules the estate-wide release budget number. This is the DAP-side of the same S-25 marker landed in 2E's `disclosure_budget.py` (per-party surface) — now composed with the estate-wide surface here.
- **R-11 coordination-signature threshold (new this wave)**: `R11_COORDINATION_SIGNATURE_DEFERRED = "DEFAULT-PENDING-OVERRIDE"` — flip-forbidden until Security R-11 rules the coordination-signature threshold. Detected-signature routing is friction-only per A5.2 until then.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T160938Z_wdap_2g_RED.log` | `27c63460cab8650b941dc48eea22f702b4674a0c15415f567fa5873718bdfe94` |
| GREEN 1 | `phase0/drill_receipts/20260913T161036Z_wdap_2g_GREEN1.log` | `c00e2cc5112fe9eead352c43271f59ae68ecc763feac7805aaa87deff0d34639` |
| GREEN 2 | `phase0/drill_receipts/20260913T161238Z_wdap_2g_GREEN2.log` | `ec394b35cb1a9f8ed30237c2a73b2924bdb5a241f5dd57b075800596fdd94c1d` |
| **Rider 1** pip freeze (187 pkgs) | `phase0/drill_receipts/20260913T161445Z_wdap_2g_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only (3618 items) | `phase0/drill_receipts/20260913T161445Z_wdap_2g_COLLECTONLY.txt` | `a7c42eb2c195e98b779a110e29239ddc67ff4d46828341d60c0bb846c49f03fb` |
| Seal | `phase0/output_verified_seals/wdap_2g.seal.txt` | — |
| Byte-match | Both GREEN runs 3617 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37346 bytes | — |

### RED reason verbatim (right-reason check)

Mechanical RED demonstrated 8/8 right-reason `ImportError: cannot
import name 'coalition' from 'services.dap'`. No G-D already-satisfied
rows in this wave.

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full (structural half)** — DAP-34 structural coalition detection (shared party, shared mandate lineage) with joint sum-of-disclosures.
- **Deferred (per §5 note)** — DAP-34 coordination-signature threshold (R-11 OPEN) — marker landed; gate not built.
- **Partial (mechanism)** — DAP-35 estate-wide bound + floor-violation verdict; NUMBER blocked on Security R-7. Kernel lands the accumulator + refusal path + severance-eligible verdict.
- **AC-10** — Direct reuse of DAP-34/DAP-35 pattern generalised to agent effect; test binds the aggregate-agent-ceiling invariant to the coalition mechanism.
- **A5 (Slow-play cumulative)** — 2E cumulative accumulator + 2G coalition joint eval compose end-to-end. Full A5 discharge = ready for M3 Watch composition.
- **S-23** — partially discharged (M3 remainder: coordination-signature threshold R-11 baseline-period-deferred).
- **S-25** — partially discharged (blocked on Security R-7 estate release budget number).

## §F · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- No egress. Radio T4 held. Playwright/Chromium reserved for CP10.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- ENV-DRIFT-2TESTS-20260913 remains tracked-open.
- SEC-2026-09-12-01 remains owner-side; builder not touching.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
