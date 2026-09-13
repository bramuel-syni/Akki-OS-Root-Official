READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2F_close.md

**Wave.** W-DAP-STACK · Sub-wave 2F · Suspension + revocation + fail-closed gates.
**Canon anchors.** DAP-Spec DAP-27 [Doc 3 A5.3 stop-never-delete], DAP-28 [FPT_FLS.1], DAP-29 [I-4 pattern].
**Owner authorisation.** Verbatim 2026-09-13 confirmation of G-A..G-E with G-D/G-E amendments.
**Ratchet.** 3600 → 3609 (+9).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wdap_2f.seal.txt`.

---

## §A · Invariants added (9 new)

| Test | Anchor | What it enforces |
|---|---|---|
| F2-01 · module fabric present | DAP-27/28/29 | `services.dap.suspension` + `services.dap.gates` importable with expected surface |
| F2-02 · DAP-27 suspend halts in-flight + future in one act | DAP-27 verbatim | `suspend_party` returns `SuspensionAct.in_flight_job_ids_stopped` naming every current job; `is_suspended=True` refuses future ops with `PermissionError("DAP-27...")`; unrelated parties unaffected |
| F2-03 · DAP-27 suspension immediate · no silent completion | DAP-27 verbatim tail | `list_stopped_in_flight_jobs` records `status='stopped'`, never `'completed'` |
| F2-04 · DAP-27 revoke_admission is a distinct act | DAP-27 verbatim | `revoke_admission` returns `AdmissionRevocation`; post-revoke ops refuse with `PermissionError("DAP-27...")` |
| F2-05 · DAP-28 approval service unreachable refuses | DAP-28 item 1 | `governed_operation` raises `FailedClosed("DAP-28...")` when approval probe raises |
| F2-06 · DAP-28 terms resolution empty refuses | DAP-28 item 3 | `governed_operation` raises `FailedClosed("DAP-28...")` when terms probe returns None/empty |
| F2-07 · DAP-28 ceiling check errors refuses | DAP-28 item 4 | `governed_operation` raises `FailedClosed("DAP-28...")` when ceiling probe raises |
| F2-08 · DAP-28 metering write cannot complete refuses | DAP-28 item 2 | `governed_operation` raises `FailedClosed("DAP-28|DAP-29")` when Ledger.append raises |
| F2-09 · DAP-29 unrecorded extraction not permitted | DAP-29 verbatim | Ledger outage → `FailedClosed` + working ledger stays empty (no half-state trace) |

## §B · Mechanism landed

- `backend/services/dap/suspension.py` (~100 lines · one-act suspend, distinct revoke, stopped-list registry, refusal on future ops).
- `backend/services/dap/gates.py` (~105 lines · `governed_operation` composer running the four DAP-28 gates + DAP-21/DAP-29 write-before-return in strict order; each failure raises `FailedClosed(anchor)`).
- `backend/tests/invariants/test_wdap_2f_suspension_and_fail_closed.py` — 9 invariants; every test docstring quotes its DAP-Spec anchor verbatim.
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3600 → 3609.

## §C · Markers held (flip-forbidden)

- R-C1, R-C2, C4 DAP_R2, S-25 DEFAULT_RELEASE_BUDGET — all carried forward.
- **DAP-28 composition invariant (new)**: `FailedClosed` is a `RuntimeError` subclass, and every raise site includes an anchor identifier ("DAP-28", "DAP-29", or "DAP-28+DAP-29") in the message so downstream test/audit code can bind to it. Silent removal of the anchor from any raise message would break F2-05..F2-09.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T160145Z_wdap_2f_RED.log` | `e2390b0b490cb9d04b58136f20267921f1f3055c69bf0c82f9699cc31137d167` |
| GREEN 1 | `phase0/drill_receipts/20260913T160240Z_wdap_2f_GREEN1.log` | `0281af8a9eeff1f66a801152b4ad7d98b24cae465e1ac64b5755ae16af6afb1e` |
| GREEN 2 | `phase0/drill_receipts/20260913T160443Z_wdap_2f_GREEN2.log` | `d1bbf43f0db9e3702374298ddbd26a6a789f68de59cae37eac9eb081353cf1d0` |
| **Rider 1** pip freeze (187 pkgs) | `phase0/drill_receipts/20260913T160651Z_wdap_2f_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only (3610 items) | `phase0/drill_receipts/20260913T160651Z_wdap_2f_COLLECTONLY.txt` | `80d5fcbf27c09523223ec9908295fc1128f5a5f2ebc9ef219339da77fdddd466` |
| Seal | `phase0/output_verified_seals/wdap_2f.seal.txt` | — |
| Byte-match | Both GREEN runs 3609 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37186 bytes | — |

### RED reason verbatim (right-reason check)

Mechanical RED demonstrated 9/9 failures with right-reason
`ImportError: cannot import name '<module>' from 'services.dap'`
across `services.dap.suspension` and `services.dap.gates`. No G-D
already-satisfied rows in this wave.

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-27 (one-act suspension + distinct revocation + no silent completion), DAP-28 (fail-closed doctrine composed across the four gate failure modes), DAP-29 (unrecorded extraction refused + no half-state trace).
- **A7 (Suspension acceptance)** — mechanism landed at kernel grade: `suspend_party` in one act stops every in-flight job for the party and refuses future ops. Full A7 discharge (composed with running-job kill signals) awaits M4 assistance surfaces.
- **Canon-1 §4.1 (fail-closed custody doctrine)** — mechanism landed at DAP surface. Chokepoint refuse-if-egress semantics carry into 2H.

## §F · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- No egress. Radio T4 held. Playwright/Chromium reserved for CP10.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- ENV-DRIFT-2TESTS-20260913 remains tracked-open; no impact this wave.
- SEC-2026-09-12-01 remains owner-side; builder not touching.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
