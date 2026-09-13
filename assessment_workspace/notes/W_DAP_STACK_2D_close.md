READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2D_close.md

**Wave.** W-DAP-STACK · Sub-wave 2D · Objective freeze + assistance chat boundary.
**Canon anchors.** DAP-Spec DAP-18, DAP-19, DAP-20 (all three anchors quoted verbatim in the test docstrings).
**Owner authorisation.** Verbatim 2026-09-13: *"Gate 1 rescinded, Gate 2 - b, Gate 3 - in-block"* + G-A..G-E confirmation with G-D/G-E amendments.
**Ratchet.** 3585 → 3590 (+5).
**Track-a commit.** Pending — will be recorded post-commit in this note and in `baseline_failures.json` ratchet_history via backfill commit.
**Seal.** `phase0/output_verified_seals/wdap_2d.seal.txt`.

---

## §A · Invariants added (5 new)

| Test | Anchor | What it enforces |
|---|---|---|
| D2-01 · module fabric present | DAP-18/19/20 | `services.dap.commission` importable with `commission_job`, `widen_scope_forbidden_after_commission`, `route_job_to_engine`, `AssistanceChatBoundary` |
| D2-02 · DAP-18 objective freeze at commission | DAP-18 verbatim | Every commissioned job carries `frozen=True` and a fixed `objective` string at commission time |
| D2-03 · DAP-18 widen-scope forbidden after commission | DAP-18 verbatim tail | Attempts to widen a commissioned job's objective — including via the portal's assistance chat — MUST raise `PermissionError` naming DAP-18 |
| D2-04 · DAP-19 route to engine · never bypass | DAP-19 verbatim | Job routing returns `governing_engine` per DAP-Spec §7 composition table; `governing_engine != "dap"` (DAP composes, does not execute) |
| D2-05 · DAP-20 assistance chat boundary | DAP-20 verbatim | `AssistanceChatBoundary` permits `propose_objective`, `propose_scope`, `explain_terms`; refuses `approve`, `widen_scope`, `decide_gate` |

## §B · Mechanism landed

- `backend/services/dap/commission.py` (119 lines · commission-time freeze, widen-scope refusal, per-§7 engine routing, assistance-chat boundary primitive).
- `backend/tests/invariants/test_wdap_2d_objective_freeze_and_assistance_chat.py` (100 lines · 5 invariants; every test carries a verbatim DAP-Spec quote in its docstring).
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3585 → 3590; ratchet_history entry appended for 2D.

## §C · Markers held (flip-forbidden)

- **R-C1**: `ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK` — carried forward. Rules-Service still not built.
- **R-C2**: `MeteredEvent.au_3b_defensible=False` default — carried forward. Doc-0 G-8 still open.
- **C4 · DAP_R2**: `DAP_R2_APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE` — carried forward from 2C.
- **DAP-19 self-composition ban**: `route_job_to_engine` raises `RuntimeError` if any operation ever maps to engine `"dap"` — defensive against future §7 additions that accidentally close the loop.

## §D · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T153632Z_wdap_2d_RED.log` | `5843c1511174aa39482a91948b3041d5f8d40f80a780b46e83ca47fe9a4ee772` |
| GREEN 1 | `phase0/drill_receipts/20260913T154122Z_wdap_2d_GREEN1.log` | `03e1a7506b5d2bb57d473734e125c6b01edb2df876b0291c272b2409460e2948` |
| GREEN 2 | `phase0/drill_receipts/20260913T154326Z_wdap_2d_GREEN2.log` | `138cea4828eb963bb28e6cebae4dec762c46ab2118ce444fa1b15c2a727df491` |
| **Rider 1** pip freeze (187 pkgs) | `phase0/drill_receipts/20260913T154537Z_wdap_2d_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only (3591 items) | `phase0/drill_receipts/20260913T154537Z_wdap_2d_COLLECTONLY.txt` | `d076b8a92e861c7707ce341747b8efdedef8cb7d6bf184dc65f5bb4c1f83515f` |
| Seal | `phase0/output_verified_seals/wdap_2d.seal.txt` | — |
| Byte-match | Both GREEN runs 3590 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 36946 bytes | — |

### RED-reason verbatim (right-reason check)

The mechanical RED demonstrated `ModuleNotFoundError: No module named
'services.dap.commission'` — the right-reason failure for a
mechanism-absent state. Reconstructed by stashing `services/dap/commission.py`
out of the tree, running the 2D test alone under `BASELINE_GUARD=1`, then
restoring the file.

## §E · G-E DECISION-POINT filed (this wave)

`notes/DECISION_POINT_ORPHAN_CP10_20260913.md` — two orphan CP10 tests from a
prior aborted `W-REGISTRY-FULL-BUILD CP10 wave close` attempt were found in
the working tree, boosting the collected count by +2 outside the 2D
declaration. Both were quarantined to
`notes/orphan_cp10_prior_session_20260913/` (preserved verbatim, not deleted)
so 2D closes at its true +5 delta. Owner may re-admit these when the CP10
wave opens in the ratified sequence.

## §F · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-18 (objective freeze + widen-scope refusal), DAP-19 (routing to §7 engines · never bypass), DAP-20 (assistance chat pre-/post-commission boundary).
- **NOT discharged in 2D**: DAP-8 (crossing profile hardening — 2E), DAP-21..23 (metering completeness — 2E), DAP-24..30 (cumulative history full wire + R-C2 real time source — 2F+).

## §G · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- No egress. Radio T4 held. The one-time Playwright download authorised under Gate 2 Option B remains reserved for CP10 (not used in 2D).
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close (this wave; retro-applied to 2B/2C in their state-side backfill close manifests).
- Rider-2 `ENV-DRIFT-2TESTS-20260913` remains tracked-open; today's +2 discrepancy was orphan CP10 tests, NOT the two env-drift-uncollected tests. Env-drift item unchanged.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
