READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2C_close.md

**Wave.** W-DAP-STACK · Sub-wave 2C · Approval routing + controlled ops.
**Canon anchors.** DAP-Spec DAP-11, DAP-14, DAP-15, DAP-16, DAP-17.
**Owner authorisation.** Verbatim 2026-09-13: *"Gate 1 rescinded"* + C4 owner ruling `DAP_R2_APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE`.
**Ratchet.** 3578 → 3585 (+7).
**Track-a commit.** `1c21753`.
**Seal.** `phase0/output_verified_seals/wdap_2c.seal.txt`.

---

## §A · Invariants added (7 new)

| Test | Anchor | What it enforces |
|---|---|---|
| C2-01 · module fabric present | DAP-11,14..17 | `services.dap.approval` importable with `request_controlled`, `record_decision`, `standing_approval_check`, `ApprovalDecision`, `StandingApproval` |
| C2-02 · DAP-14 controlled request routes to authority | DAP-14 verbatim | A controlled request MUST route to a named approving authority; unnamed routing refused |
| C2-03 · DAP-15 decision recorded — no silent default | DAP-15 verbatim | Every decision carries `decided_by`, `reason`, `at_iso`; missing fields refused (no silent default) |
| C2-04 · DAP-16 fine-tune always requires approval | DAP-16 verbatim | `fine_tune_model` operation ALWAYS enters the approval gate; no auto-pass path |
| C2-05 · DAP-11 raw-download-controlled always requires approval | DAP-11 verbatim | `download_raw_data` operation ALWAYS enters approval; Doc-0 Promise #25 · not ordinary crossing |
| C2-06 · DAP-17 standing approval named and bounded | DAP-17 verbatim | Standing approvals carry named authority + explicit `bound_to` scope + expiry; unbounded standing approvals refused |
| C2-07 · C4 DAP_R2 pending-override marker | C4 owner ruling 2026-09-13 | `DAP_R2_APPROVING_AUTHORITY` present in `services.dap.approval` with value `DEFAULT-PENDING-OVERRIDE`; flip requires ruling |

## §B · Mechanism landed

- `backend/services/dap/approval.py` (208 lines · approval routing, decision recording, standing-approval kernel, C4 pending-override marker).
- `backend/tests/invariants/test_wdap_2c_approval_routing_and_controlled_ops.py` (161 lines · 7 invariants).

## §C · Markers held (flip-forbidden)

- **R-C1**: `ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK` — carried forward. Rules-Service still not built.
- **R-C2**: `MeteredEvent.au_3b_defensible=False` default — carried forward. Doc-0 G-8 still open.
- **C4 · DAP_R2**: `DAP_R2_APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE` — owner ruling 2026-09-13; flip forbidden without owner override.

## §D · Discipline receipts

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T153800Z_wdap_2c_RED.log` | `346c3ab6ab9d1c4d2e9cf94e17e91944546d7d8dec8a038769072b2e3a94a8e1` |
| GREEN 1 | `phase0/drill_receipts/20260913T154000Z_wdap_2c_GREEN1.log` | `f73d69b24abc1e5141547d4892ac404e68dfb85e6affe8b352f4da8ecdf8adff` |
| GREEN 2 | `phase0/drill_receipts/20260913T154200Z_wdap_2c_GREEN2.log` | `0cd7a3804eee43b417207a463bf47ab217c516634903e3e02ddbe5232a704661` |
| **Rider 1** pip freeze | `phase0/drill_receipts/20260913T154300Z_wdap_2c_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only | `phase0/drill_receipts/20260913T154300Z_wdap_2c_COLLECTONLY.txt` | `ec2c4d6015d673b8379b1bb4ee79648ea3378448013409c3d51134c9fd264f04` |
| Seal | `phase0/output_verified_seals/wdap_2c.seal.txt` | — |
| Byte-match | 3585 passed / 1 skipped / 438 warnings — identical modulo wall-time | — |

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-11 (raw-download always controlled), DAP-14 (routing to authority), DAP-15 (decision recording · no silent default), DAP-16 (fine-tune always approved), DAP-17 (standing approval named + bounded), C4 DAP_R2 marker.
- **NOT discharged in 2C**: DAP-8 (crossing profile — completes in 2E), DAP-18..20 (objective freeze + assistance chat — completes in 2D), DAP-21..23 (metering — 2E), DAP-24..30 (cumulative history, R-C2 wiring — 2F+).

## §F · Guardrails held

- Local commit only (`programme/track-a` HEAD `1c21753`). NEVER pushed.
- No egress. Radio T4 held.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.

## §G · State-side backfill note

Master-side close manifest authored 2026-09-13 during 2D housekeeping, after
track-a commit `1c21753` had been made. No 2C content is altered by this
backfill; only state-side documentation is caught up.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
