READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2H_close.md

**Wave.** W-DAP-STACK · Sub-wave 2H · Component boundary + composition close.
**Canon anchors.** DAP-Spec DAP-30 [honesty grammar], DAP-31+ + DAP-32+ [`Serving_Integrity_Amendment_v1 §B V-2` · declared dependency markers], MILESTONE_PROMISE_BINDING §A1 (compute-to-data), DAP-Spec §7 (component boundary — compose, never execute).
**Owner authorisation.** Verbatim 2026-09-13 confirmation of G-A..G-E with G-D/G-E amendments.
**Ratchet.** 3617 → 3625 (+8).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wdap_2h.seal.txt`.

---

## §A · Invariants added (8 new)

| Test | Anchor | What it enforces |
|---|---|---|
| H2-01 · module fabric present | DAP-30/31+/32+/A1/§7 | `services.dap.boundary` importable with `browse_degraded_with_as_of`, `BrowseSnapshot`, `refuse_if_egress`, `record_refused_egress_attempt`, `listed_refused_egress_attempts`, `DAP_31_PLUS_DEPENDS_ON_SFP_8`, `DAP_32_PLUS_DEPENDS_ON_SFP_8`, `assert_composes_only`, `EgressRefused` |
| H2-02 · DAP-30 browse degrades not refuses · marks stale + as-of | DAP-30 verbatim | Partial census → BrowseSnapshot returns payload + `stale=True` + `as_of_iso` + `refused=False` |
| H2-03 · DAP-30 never silently presents incomplete as complete | DAP-30 verbatim tail | `census_complete=True` with `available < expected` → `ValueError` matching "DAP-30" |
| H2-04 · DAP-31+ declared dependency marker on SFP-8 | DAP-31+ + amendment §7 M1 | `DAP_31_PLUS_DEPENDS_ON_SFP_8` dict names SFP-8, M2_RULES_SERVICE scope, DECLARED_DEPENDENCY_NOT_GUESS posture, DAP-31+ anchor |
| H2-05 · DAP-32+ declared dependency marker on SFP-8 | DAP-32+ + amendment §7 M1 | `DAP_32_PLUS_DEPENDS_ON_SFP_8` dict names SFP-8, M2_RULES_SERVICE, DECLARED_DEPENDENCY_NOT_GUESS, DAP-32+ anchor |
| H2-06 · A1 no configuration permits egress | A1 verbatim | Five plausibly-egress destinations (outside_perimeter, external_provider, peer_estate, public_internet, kube_egress) all refused with `EgressRefused` matching "A1\|DAP" |
| H2-07 · A1 every attempt recorded | A1 verbatim tail | Refusal log carries every attempted config with `outcome='refused'` |
| H2-08 · DAP-Spec §7 DAP composes never executes | DAP-Spec §7 verbatim | `assert_composes_only()` scans every services.dap.* submodule; no callable name matches `execute_*`, `serve_*`, `run_extraction_*`, `invoke_model_*`, `perform_extraction_*` |

## §B · Mechanism landed

- `backend/services/dap/boundary.py` (~185 lines · DAP-30 BrowseSnapshot honesty grammar; A1 EgressRefused chokepoint + egress-attempt log; DAP-31+/32+ declared-dependency marker dicts; DAP-Spec §7 assert_composes_only() surface scanner over all services.dap.* submodules).
- `backend/tests/invariants/test_wdap_2h_component_boundary_and_composition_close.py` — 8 invariants; every test docstring quotes its canon anchor verbatim.
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3617 → 3625.

## §C · Markers held (flip-forbidden)

- R-C1, R-C2, C4 DAP_R2, S-25 `DEFAULT_RELEASE_BUDGET` (2E), `DEFAULT_ESTATE_WIDE_BUDGET` (2G), `R11_COORDINATION_SIGNATURE_DEFERRED` (2G) — all carried forward.
- **DAP-31+ / DAP-32+ dependency markers (new this wave)**: both dicts carry `posture='DECLARED_DEPENDENCY_NOT_GUESS'` — flip forbidden. Any change to the SFP-8 dependency requires a Rules-Service (M2) ceremony landing SFP-8 first.
- **DAP-Spec §7 composition invariant (new this wave)**: `assert_composes_only()` scans the full services.dap.* surface for forbidden execution verbs; adding an `execute_*`, `serve_*`, `run_extraction_*`, `invoke_model_*`, or `perform_extraction_*` public callable to any services.dap.* module breaks H2-08 by construction.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T161725Z_wdap_2h_RED.log` | `f72f27884116ece284b84b4d5ec8015a6928493b7f8fbd0835b83791eac9bdfc` |
| GREEN 1 | `phase0/drill_receipts/20260913T161820Z_wdap_2h_GREEN1.log` | `79663be62a448eda99c0b3fd586945d3e0a9e45eba4cc7358cf3c98416c2b28d` |
| GREEN 2 | `phase0/drill_receipts/20260913T162022Z_wdap_2h_GREEN2.log` | `899a46d2098866a733470186281db005a07f89d3db1f5941f1067a0555dcbabf` |
| **Rider 1** pip freeze (187 pkgs) | `phase0/drill_receipts/20260913T162228Z_wdap_2h_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only (3626 items) | `phase0/drill_receipts/20260913T162228Z_wdap_2h_COLLECTONLY.txt` | `3610af119aca9559de1a9574d0d2716ab4c25e968440cf206e4448a6ddd06208` |
| Seal | `phase0/output_verified_seals/wdap_2h.seal.txt` | — |
| Byte-match | Both GREEN runs 3625 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37509 bytes | — |

### RED reason verbatim (right-reason check)

Mechanical RED demonstrated 8/8 right-reason failures — all failures
originate from `ImportError: No module named 'services.dap.boundary'`
raised at the top of each test's `from services.dap import boundary`
line.  No G-D already-satisfied rows in this wave.

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-30 (browse degradation with honesty grammar), A1 (compute-to-data · no configuration permits egress + every attempt refused and recorded), DAP-Spec §7 (component boundary — DAP composes, DAP does not execute; invariant-asserted by whole-surface scan).
- **Declared dependency markers (per amendment §7 M1 note)** — DAP-31+ + DAP-32+ (SFP-8 conformance) — mechanism gated on M2 Rules-Service; markers landed and flip-forbidden.

## §F · W-DAP-STACK rollup (2A → 2H)

| Sub-wave | Delta | Ratchet | Track-a commit | Anchors |
|---|--:|--:|---|---|
| 2A | +10 | 3570 | `e578582` | DAP-1..4, DAP-12, DAP-24 |
| 2B | +8 | 3578 | `4ed29e0` | DAP-5, 6, 7, 8-partial, 13 |
| 2C | +7 | 3585 | `1c21753` | DAP-11, 14, 15, 16, 17 · C4 DAP_R2 |
| 2D | +5 | 3590 | `a1db65d` | DAP-18, 19, 20 |
| 2E | +10 | 3600 | `c383eb1` | DAP-21, 22-partial, 25, 26 · R-C2 asserted · S-25 marker |
| 2F | +9 | 3609 | `dbb0b02` | DAP-27, 28, 29 · FailedClosed composer |
| 2G | +8 | 3617 | `9adccaa` | DAP-34, 35, AC-10 · R-11 marker · DEFAULT_ESTATE_WIDE_BUDGET marker |
| 2H | +8 | 3625 | PENDING backfill | DAP-30, 31+, 32+, A1, §7 |

**Cumulative: +65 invariants across the DAP-STACK · 3560 → 3625.**

- **A1 (compute-to-data)** — discharged fully by 2H.
- **A2 (browse boundary)** — discharged: 2B DAP-6 aggregate-only + 2H DAP-30 degradation.
- **A3 (approval gate)** — discharged: 2C.
- **A4 (metering completeness)** — discharged: 2E write-before-return.
- **A5 (slow-play detection)** — discharged: 2A scaffold + 2E cumulative + 2G joint eval.
- **A6 (objective freeze)** — discharged: 2D.
- **A7 (suspension)** — discharged: 2F one-act suspend.
- **A8 (trust-domain)** — discharged: 2B trust_boundary.
- **A9 (key hygiene)** — discharged: 2B api_keys (per-principal, revoke-single-act).
- **A10 (aggregate limit)** — partial: 2E + 2G kernel + M3 Watch remainder.

## §G · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- No egress. Radio T4 held. Playwright/Chromium reserved for CP10 (next in ratified sequence).
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- ENV-DRIFT-2TESTS-20260913 remains tracked-open.
- SEC-2026-09-12-01 remains owner-side; builder not touching.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
