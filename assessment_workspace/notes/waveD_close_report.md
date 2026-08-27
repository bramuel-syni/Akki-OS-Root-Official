# Wave D · Close Report

**Prepared for owner external verification.** Wave D closes on this verification, not before (owner ruling 2026-08-27 verbatim: "Wave D closes on my external verification of D7/D8, not before").

## 1 · Guard receipt at Wave D endgame (banked)

At CP-D8 close (2026-08-27T11:45Z):

```
============================ BASELINE_GUARD receipt ============================
passed=2119 / baseline-failures-remaining=0 / quarantined=159
  manifest: tests/invariants/baseline_failures.json
  scope: BASELINE_GUARD=1  ·  invocation: cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/
  status: OK (subset · quarantine · ratchet all pass)
```

Full-directory summary: **2119 passed · 160 skipped · 0 failed · 347 warnings** in 59.30s.

Receipts (chronological):
- `phase0/drill_receipts/20260827T101500Z_cp_d5_pre_q3_measure.log`
- `phase0/drill_receipts/20260827T102000Z_cp_d5_close_partial.log`
- `phase0/drill_receipts/20260827T104500Z_cp_d6_close.log`
- `phase0/drill_receipts/20260827T113000Z_cp_d7_close.log`
- `phase0/drill_receipts/20260827T114500Z_cp_d8_close.log`

## 2 · Verification target list — NEW/CHANGED wire paths + SPA routes shipped across CP-D7 + CP-D8

### 2.1 · Wire paths — 28 new entries (all verified LIVE on pod openapi at IP-allowlisted /api/openapi.json)

**CP-D7 · Doc 15 · Governance Ceremony (18 wire paths)** — routers.govern + routers.checker + routers.compliance + routers.master_admin mounted in pod_shell at CP-D7:

| # | Method | Path | Ship note |
|---|---|---|---|
| 1 | GET | `/api/govern/enforcement_class_split` | CP-D7 · Doc 15 enforcement class rollup |
| 2 | GET | `/api/govern/trust_center_record` | CP-D7 · Doc 15 trust-center record surface |
| 3 | GET | `/api/govern/estate_rules_record` | CP-D7 · Doc 15 estate rules surface |
| 4 | POST | `/api/govern/registries/upload` | CP-D7 · Doc 15 registry-upload ceremony step |
| 5 | POST | `/api/govern/registries/diff` | CP-D7 · Doc 15 registry-diff ceremony step |
| 6 | POST | `/api/govern/registries/commit` | CP-D7 · Doc 15 registry-commit (propose+apply) |
| 7 | GET | `/api/govern/holds` | CP-D7 · Doc 15 hold ledger surface |
| 8 | POST | `/api/checker/initiate` | CP-D7 · Doc 15 checker · initiate |
| 9 | POST | `/api/checker/countersign/{request_id}` | CP-D7 · Doc 15 checker · countersign |
| 10 | POST | `/api/checker/cancel/{request_id}` | CP-D7 · Doc 15 checker · cancel |
| 11 | GET | `/api/checker/pending` | CP-D7 · Doc 15 checker · pending queue |
| 12 | GET | `/api/checker/request/{request_id}` | CP-D7 · Doc 15 checker · request detail |
| 13 | GET | `/api/compliance/refusals` | CP-D7 · Doc 15 compliance refusals feed |
| 14 | GET | `/api/compliance/refusals_coverage` | CP-D7 · Doc 15 refusals coverage rollup |
| 15 | GET | `/api/compliance/retention_config` | CP-D7 · Doc 15 retention-config governance |
| 16 | GET | `/api/master_admin/pending_seams` | CP-D7 · Doc 15 master admin queue |
| 17 | GET | `/api/master_admin/audit_trail` | CP-D7 · Doc 15 master admin audit trail |
| 18 | POST | `/api/master_admin/tightening/suspend` | CP-D7 · Doc 15 tightening-suspend ceremony |

**CP-D8 · Doc 16 · Cross-cutting Orchestration (10 wire paths)** — routers.team mounted at CP-D8 (handoff + prove already live pre-D8, now bound into MUST_BE_LIVE):

| # | Method | Path | Ship note |
|---|---|---|---|
| 19 | GET | `/api/handoff/backend_contract_surface_v1` | CP-D8 · Doc 16-001 generalised hand-off contract |
| 20 | POST | `/api/prove/ask` | CP-D8 · Doc 16-023 claim-to-evidence · ask |
| 21 | GET | `/api/prove/samples` | CP-D8 · Doc 16-023 claim-to-evidence · samples |
| 22 | GET | `/api/prove/trace/{trace_id}` | CP-D8 · Doc 16-023 walk-this trace surface |
| 23 | GET | `/api/team/approval_surface` | CP-D8 · Doc 16 team approval ceremony |
| 24 | POST | `/api/team/approval_surface/{item_id}/decision` | CP-D8 · Doc 16-014 refusal-card wire-through |
| 25 | GET | `/api/team/access_register` | CP-D8 · Doc 16 access-register readout |
| 26 | POST | `/api/team/access_register/grant` | CP-D8 · Doc 16 access-register grant |
| 27 | POST | `/api/team/access_register/revoke` | CP-D8 · Doc 16 access-register revoke |
| 28 | GET | `/api/team/constitutional_seats` | CP-D8 · Doc 16 constitutional-seats surface |

### 2.2 · SPA routes — 25 new entries in MUST_BE_LIVE_SPA_ROUTES (each verified declared in `frontend/src/App.js` or `frontend/src/pages/**`)

**CP-D7 · Doc 15 UI surface (13 SPA routes):**

| # | Path | Ship note |
|---|---|---|
| 1 | `/govern` | CP-D7 · Doc 15 govern top-level |
| 2 | `/govern/change-rule` | CP-D7 · Doc 15 rule-change wizard |
| 3 | `/govern/holds` | CP-D7 · Doc 15 holds surface |
| 4 | `/govern/pending` | CP-D7 · Doc 15 pending-seams queue |
| 5 | `/govern/refusal-health` | CP-D7 · Doc 15 refusal-health rollup |
| 6 | `/govern/registries` | CP-D7 · Doc 15 registries ceremony |
| 7 | `/govern/retention` | CP-D7 · Doc 15 retention-config UI |
| 8 | `/govern/rules` | CP-D7 · Doc 15 estate rules |
| 9 | `/master-admin` | CP-D7 · Doc 15 master admin dashboard |
| 10 | `/master-admin/audit-trail` | CP-D7 · Doc 15 audit trail UI |
| 11 | `/master-admin/change-a-rule/:ruleId` | CP-D7 · Doc 15 change-a-rule wizard |
| 12 | `/compliance` | CP-D7 · Doc 15 compliance top-level |
| 13 | `/compliance/*` | CP-D7 · Doc 15 compliance subrouter |

**CP-D8 · Doc 16 UI surface (12 SPA routes):**

| # | Path | Ship note |
|---|---|---|
| 14 | `/prove` | CP-D8 · Doc 16-023 prove surface |
| 15 | `/prove/trace/:traceId` | CP-D8 · Doc 16-023 walk-this trace drill |
| 16 | `/team` | CP-D8 · Doc 16 team top-level |
| 17 | `/team/access-register` | CP-D8 · Doc 16 access-register UI |
| 18 | `/team/approval-surface` | CP-D8 · Doc 16-014 approval surface |
| 19 | `/team/constitutional-seats` | CP-D8 · Doc 16 constitutional seats |
| 20 | `/trace` | CP-D8 · Doc 16-023 trace top-level |
| 21 | `/trace/:traceId` | CP-D8 · Doc 16-023 trace drill |
| 22 | `/registry` | CP-D8 · Doc 16 registry anchor |
| 23 | `/registry/artifact/:artifactId` | CP-D8 · Doc 16 registry artifact drill |
| 24 | `/registry/estate-map` | CP-D8 · Doc 16 registry estate map |
| 25 | `/opportunity-briefs` | CP-D8 · Doc 16 opportunity briefs |

Both lists live at `backend/tests/invariants/test_ship_manifest_dod_route_table_drift.py::MUST_BE_LIVE_ROUTES` (wire) and `::MUST_BE_LIVE_SPA_ROUTES` (SPA); each is exercised by a parametrized invariant test that gates future CP closes.

## 3 · Register REUSABLE→DONE moves (with receipts)

| Row | Canon anchor | Move at CP | Receipt |
|---|---|---|---|
| **Doc15-001** | C3-050 · Rules authored in plain language via open ceremony (Promise #27) | REUSABLE → DONE at **CP-D7** | `phase0/drill_receipts/20260827T113000Z_cp_d7_close.log` |
| **Doc15-020** | C9-005 · Every rule change: propose · counter-sign · countdown · apply · re-check | REUSABLE → DONE at **CP-D7** | `phase0/drill_receipts/20260827T113000Z_cp_d7_close.log` |
| **Doc16-001** | C6-005 · Cross-app hand-offs carry declaration + purpose (Promise #32 seed) | REUSABLE → DONE at **CP-D8** | `phase0/drill_receipts/20260827T114500Z_cp_d8_close.log` |
| **Doc16-014** | C5-095 · Refusal card copy VERBATIM across every surface | PARTIAL → DONE (wire-through) at **CP-D8** | `phase0/drill_receipts/20260827T114500Z_cp_d8_close.log` |

## 4 · Downgrade list — rows that could not honestly lift this Wave

| Row | Original target | Landing state | Reason (honest) |
|---|---|---|---|
| **Doc15-014** ← C3-055 · "Nothing operates above governance except the Watch" | REUSABLE → DONE | **stays PARTIAL** | Watch mechanism build is Wave-F retirement scope. No pod-side surface exists yet; register row unchanged in this wave. |
| **Doc16-023** ← C6-020 · Universal claim-to-evidence trace ("Walk this →") | BUILD → DONE | **PARTIAL** (surface-level DONE, semantics still open) | Walk-this UI + wire ARE live (`/api/prove/trace/{trace_id}`, `/api/trace`, `/trace/:traceId`, `/prove/trace/:traceId`). But the ledger-traversal SEMANTICS remain incomplete until Doc 10 evidence-record backfill (evidence-register beyond current samples). Owner ruled at CP-D8 opening ("REFERENCE-NOT-COPY on every rendered record"); current surfaces reference-not-copy correctly, but the underlying evidence records are minimal-sample only. Honest landing: surface DONE, semantics PARTIAL. |
| **Doc02-020** · CA1-007 dry-run BUILD (checker-adjacent) | BUILD | **stays BUILD** | Dry-run wizard UI beyond the ceremony endpoints is not in scope of CP-D7 lift. Wire endpoints live; wizard authoring is a subsequent CP. |
| **Doc15-085 / -086 / -087** · Watch, generalised handoff (CA1-009), staleness-flagging (CA1-012) | REUSABLE / BUILD | **stays BUILD/REUSABLE** | Doc15-085 (Watch): Wave-F. Doc15-086 (generalised handoff CA1-009): the /api/handoff/backend_contract_surface_v1 surface is live and lifted via Doc16-001; the row's full CA1-009 remains BUILD until wizard-driven registration ceremony lands. Doc15-087 (CA1-012 staleness-flagging): Wave-F. |

No row was downgraded from an existing higher state; downgrades listed above are "did-not-lift-as-far-as-planned" not "lost-ground" cases.

## 5 · Preliminary composite delta

**W11 D · Wave D block ratchet (across CP-D0 → CP-D8):**

| Metric | Wave-D start (post-CP-D0) | Wave-D end (CP-D8 close) | Δ |
|---|---:|---:|---:|
| `passed` | 1830 | **2119** | **+289** |
| `baseline_failures` | 156 | **0** | **−156** |
| `passed_floor` (monotonic ratchet) | 1830 | **2119** | **+289** |
| `quarantined_d1a1_max` | 165 | **159** | **−6** |
| `quarantined_d1a1_files` | 6 | 21 (2 exclusive + 19 partial) | +15 (Q2 grant) |
| `MUST_BE_LIVE_ROUTES` entries | 2 | **30** | **+28** |
| `MUST_BE_LIVE_SPA_ROUTES` entries | 0 (list did not exist) | **25** | **+25** |
| Register `DONE` rows (of the CP-D7/D8 scope) | 0 | **4** (Doc15-001, Doc15-020, Doc16-001, Doc16-014) | +4 |
| Register `PARTIAL` rows carried forward | (Doc15-014, Doc16-023, others) | (unchanged; Doc16-023 refined) | 0 net |

**Wave D block-level retirements** (baseline_failures → 0):
- **CP-D1**: 1830 → 1986 (+156 passing tests, mostly framework post-fixture drift).
- **CP-D1a**: 1932 → 1944 (+12; guard installed).
- **CP-D2**: 99 fail → 82 (+17 retirements).
- **CP-D3**: 82 → 67 (+15 retirements).
- **CP-D4**: 78 → 78 (guard OK; 6 retirements offset by new baseline surfaces — SHORTFALL flagged).
- **CP-D5**: 115 → 113 (Q1 upgrade + Q3 AST-egress-gate fix; A17.16 batched escalation).
- **CP-D6**: 113 → 0 (25 semantic retirements + Q2 grant activation).
- **CP-D7**: 0 (unchanged) + 18 new MUST_BE_LIVE tests active.
- **CP-D8**: 0 (unchanged) + 10 new wire + 25 SPA parametrized tests active.

Wave A + Wave B + Wave C ratifications remain BLOCK-RATIFIED per owner 2026-08-26T~12:40Z. Wave D endgame achieved 2026-08-27T10:45Z; Wave-D close awaits owner external verification.

## 6 · Standing items carried into Wave-F opening

1. **Framework layer**: pytest-asyncio 1.2.0 landed at CP-D5 as a good partial win. Newer versions (≥1.5) may resolve the D1a-1 residue class. Wave-F option 1 (framework upgrade pilot on 3-5 chartered files first).
2. **Watch mechanism** (Doc15-014, Doc15-085): full lift pending Wave F.
3. **Staleness-flagging CA1-012** (Doc15-087): Wave F.
4. **Walk-this semantics** (Doc16-023): surface DONE, ledger-traversal semantics await Doc 10 evidence-record backfill.
5. **Generalised handoff CA1-009** (Doc15-086): surface lifted, wizard-driven registration ceremony remains.

See `notes/waveF_retirement_charter.md` for the D1a-1 residue class charter (19 files · 88 tests · 100% event-loop-closed class).

## 7 · Wave D close criteria — owner verification list

Per owner ruling 2026-08-27 (verbatim): **"Wave D closes on my external verification of D7/D8, not before."**

To verify externally, the owner may:

1. Curl the 28 wire paths in §2.1 via the IP-allowlisted `http://127.0.0.1:8001/api/openapi.json` (already 200-verified from this session at CP-D7 + CP-D8 close).
2. Load the 25 SPA routes in §2.2 in the frontend and confirm shell renders (no 404, no blank page).
3. Sample the ceremony end-to-end from `/govern/change-rule` (propose) through `/govern/pending` (countersign) into `/master-admin/audit-trail` (apply + re-check).
4. Sample the cross-cutting drill from `/prove` (ask) to `/prove/trace/:traceId` (walk-this) to `/registry/artifact/:artifactId` (reference-not-copy landing).
5. Verify the receipts at `phase0/drill_receipts/20260827T*.log` all report `status: OK`.

Standing by for the verification outcome. SSH interrupt priority remains unchanged.
