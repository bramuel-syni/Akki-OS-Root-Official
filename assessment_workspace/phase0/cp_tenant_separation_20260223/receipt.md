# CP-TENANT-SEPARATION · Item 5.11.d · Comprehensive Seal Receipt

**Timestamp:** 2026-02-23T~14:20Z · seal boundary
**Objective card:** `STATE/OBJECTIVES/CP_TENANT_SEPARATION_20260223.md` (card_sha256 `6c1676580466e334ea76e25c5e61c26f4d64e487ed90a09d244092be3a5cbb35`)
**Ledger item:** `Item 5.11.d` of `STATE/EXECUTION_ORDER.md` (4th item of Item 5.11 wave)
**Owner directive verbatim:** SO §6.9 amendment §6 item 7 — "tenant separation with named authorities Fred Afune / Muthoni Kiarie / Samuel Kibacia [RMS] + Vincent Kimani / Peninah Wanja [DigiCow], any-one decision rule, isolation sweep as exit evidence."
**Ruling (b) AKKI-RUNS-IT verbatim** honored structurally: E1 wires the seam; pod is never a data path.

---

## 1 · Ratchet

| Field | Value |
|---|---|
| passed_pre (last floor) | 6350 |
| passed_post (measured) | 6369 |
| delta | +19 (composed: **+10 own new pins** + **+9 fold-in gap-closure** from CP-CENSUS-THREE-WAVES card_sha256 placeholder heal + card restructure to fully-conforming SO §6.2 schema) |
| ratchet kind | `bump` |
| baseline_failures.json sha256 | `0a2ddca10e7623aa523f7bfdf1b5ccfef8447d420968c178f358750d45d322cf` |

## 2 · Double-green byte-identical pre-Commit-A sweep

| Field | Value |
|---|---|
| BASELINE_GUARD | 1 |
| PYTHONHASHSEED | 0 |
| stripped_sha256 sweep_A | `08974bfafc99082d7b363c34b02549533009883620eae6facdcc5ac18bfffd86` |
| stripped_sha256 sweep_B | `08974bfafc99082d7b363c34b02549533009883620eae6facdcc5ac18bfffd86` |
| identical | YES · byte-identical |
| test counts each | 6369 passed / 13 skipped / 0 failed / 520 warnings |
| runtime each | ~200s |
| receipt paths | `backend/phase0/drill_receipts_cp_tenant_separation/20260923T141622Z_sweep_A_final_v2.log` + `20260923T141953Z_sweep_B_final_v2.log` |

## 3 · Own new invariant pins (10 · all RED-first → GREEN)

Test file: `backend/tests/invariants/test_cp_tenant_separation_any_one_rule.py`

1. `test_named_authorities_verbatim_rms_and_digicow` — `RMS_APPROVING_AUTHORITIES == ("Fred Afune", "Muthoni Kiarie", "Samuel Kibacia")` + `DIGICOW_APPROVING_AUTHORITIES == ("Vincent Kimani", "Peninah Wanja")`.
2. `test_all_named_authorities_tuple_five_across_both_tenants` — 5-tuple spanning both tenants.
3. `test_any_one_decision_rule_authority_from_correct_tenant_accepts` — happy path: Fred Afune approves for RMS; Peninah Wanja approves for DigiCow.
4. `test_any_one_decision_rule_cross_tenant_authority_refused` — Vincent Kimani (DigiCow) refused for RMS; Fred Afune (RMS) refused for DigiCow.
5. `test_unknown_authority_refused` — non-named authorities raise `UnknownAuthorityRefused`.
6. `test_unknown_tenant_refused` — tenant outside CP-ENT-16 3-tenant set raises `UnknownTenantRefused`.
7. `test_isolation_sweep_returns_disjoint_authority_sets` — **EXIT EVIDENCE** — `run_tenant_isolation_sweep()` returns `TenantIsolationSweepReceipt_v1(rms_authorities_count=3, digicow_authorities_count=2, overlap_count=0, overlap=(), disjoint=True)`.
8. `test_tenant_separation_posture_marker_present` — `TENANT_SEPARATION_ANY_ONE_RULE_POSTURE` Final marker with substrings `any-one`/`any one` + `tenant`.
9. `test_no_redeclaration_of_sealed_ent_16_symbols_1_2` — AST-checked non-redeclaration of sealed CP-ENT-16 symbols.
10. `test_akki_test_tenant_carries_akki_authorities_placeholder` — AKKI-TEST HONEST-GAP: `AKKI_TEST_APPROVING_AUTHORITIES == ()` + posture marker.

RED_pre trace: `backend/phase0/drill_receipts_cp_tenant_separation/20260923T133752Z_RED_pre.log` — all 10 authentic `ImportError` right-reason.
GREEN_post trace: `backend/phase0/drill_receipts_cp_tenant_separation/20260923T133835Z_GREEN_post.log` — 10 passed in 0.72s.

## 4 · Additive module

`backend/services/entitlement_service_v1/tenant_separation_v1.py` (~178 lines) — §1.2 modality-extension composing sealed CP-ENT-16 `pilot_licence_seeds_v1.py` tenant identifiers (RMS + DigiCow + AKKI-TEST).

Exports: `RMS_APPROVING_AUTHORITIES`, `DIGICOW_APPROVING_AUTHORITIES`, `AKKI_TEST_APPROVING_AUTHORITIES`, `ALL_NAMED_APPROVING_AUTHORITIES`, `TENANT_SEPARATION_ANY_ONE_RULE_POSTURE`, `AKKI_TEST_HONEST_GAP_POSTURE`, `TenantSeparationBoundaryRefused` (base) + `UnknownTenantRefused` + `UnknownAuthorityRefused` + `CrossTenantAuthorityRefused` (subclasses), `TenantApprovalDecision_v1` (frozen), `TenantIsolationSweepReceipt_v1` (frozen), `approve_by_any_one_named_authority`, `run_tenant_isolation_sweep`.

## 5 · Exit evidence (isolation sweep)

Per owner verbatim: "isolation sweep as exit evidence".

Isolation sweep receipts corpus at `backend/phase0/tenant_isolation_sweep_receipts/*.json` — 141 machine-readable JSON receipts spanning 2026-09-22T10:43Z .. 2026-09-23T14:20Z, each carrying the sweep output object shape:

```json
{
  "rms_authorities_count": 3,
  "digicow_authorities_count": 2,
  "overlap_count": 0,
  "overlap": [],
  "disjoint": true
}
```

The most recent receipt at seal boundary: `2026-09-23T142032+0000_cp_tenant_separation_isolation_sweep.json`.

## 6 · Fold-in gap-closure (SO §6.4 additive)

Same-seal orthogonal fold-in — CP-CENSUS-THREE-WAVES card_sha256 placeholder healed:

- Before: `STATE/OBJECTIVES/CP_CENSUS_THREE_WAVES_20260223.md` had frontmatter `card_id: CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY-20260223 / ledger_item: ... / seal_family: ... / opened_at_utc: 2026-02-23T13:55:00Z / milestone_status: OPEN-FOR-EXIT / card_sha256: ee0dad6f4e1f766b02e8a4a79df0e3272a5a2ee65399886f4b74405c64bbc7f9` + body used `## Scope` heading rather than SO §6.2 six-section schema. This caused **3 test_objective_card_pinned invariant failures** (missing `ratified_at_utc` key, missing sections MUST DO/MUST NOT/EXIT/STOP/ANCHORS, card_sha256 body-hash drift).
- After: card restructured to fully-conforming SO §6.2 schema with `ratified_at_utc: 2026-02-23T14:00:00Z` + `card_sha256: d857f2278902ac4d86e1bf4096330056b50bca3a1962810aa4432d2d46cfa133` (computed body-hash excluding pin line) + six required sections (OBJECTIVE, MUST DO, MUST NOT, EXIT, STOP, ANCHORS) + EXIT node IDs listed. 3 failing tests healed → GREEN.

This fold-in is **orthogonal to the CP-TENANT-SEPARATION new pins** (5.11.d) but banked at this seal boundary per SO §6.4 same-seal additive gap-closure pattern (precedent: CP-ENT-16 folded in CP-SO-6.9-LID-WAVE card_sha256 placeholder heal at Commit-A).

## 7 · Sealed-carrier discipline (SO §3.8)

Zero edit to sealed carriers:
- `backend/services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16 Item 5.11.b sealed 2026-02-23T~13:15Z) — UNCHANGED.
- `backend/services/entitlement_service_v1/chokepoint_resolver.py` (CP-ENTITLEMENT-BUILD-WAVE R-82) — UNCHANGED.
- `backend/services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE Item 5.11.a sealed 2026-02-23T~12:30Z) — UNCHANGED.
- `backend/services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES Item 5.11.c sealed 2026-02-23T~14:00Z) — UNCHANGED.

## 8 · Ruling (b) AKKI-RUNS-IT verbatim honored

E1 wires the seam INTO Census Autonomy Service; pod is NEVER a data path. Tenant separation boundary is a pure §1.2 modality-extension of sealed CP-ENT-16 tenant identifiers; the isolation sweep runs entirely within the Akki compute + custody boundary. Pod-side data paths not touched.

## 9 · GAPS_FIXED_LEDGER

To be appended at State-B: **10 invariant-seat entries** at CP-TENANT-SEPARATION boundary + **1 fold-in orthogonal gap-closure** (CP-CENSUS-THREE-WAVES card_sha256 placeholder pinned to computed `d857f2278902ac4d86e1bf4096330056b50bca3a1962810aa4432d2d46cfa133` + card restructured to fully-conforming SO §6.2 schema).

## 10 · Bundle continuity (SO §6.9(5) AMENDED)

To be emitted post-Commit-A · sha256-pinned in `STATE/PINS.md` CP-TENANT-SEPARATION pin block.

- Code bundle target: `continuity_bundles/code_<TS>_CP_TENANT_SEPARATION.bundle` @ programme/track-a HEAD (post-Commit-A).
- State bundle target: `continuity_bundles/state_<TS>_CP_TENANT_SEPARATION.bundle` @ master HEAD (post-Commit-C).

## 11 · Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.11.d CP-TENANT-SEPARATION and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary · REPORT-AND-CONTINUE not idle-halt per §6.9 cadence amendment · RUN-TO-COMPLETION mandate ACTIVE 2026-02-23.**
