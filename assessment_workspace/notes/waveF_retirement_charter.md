# Wave F · Retirement Charter · D1a-1 Residue Class

Charter opened: 2026-08-27 at CP-D6 close (owner ruling this session · Q2 grant activation).

## Scope

The following **19 files** carry the D1a-1 residual quarantine per CP-D6 Q2 grant (owner ruling verbatim: "If, after CP-D6, the manifest residue is EXCLUSIVELY event-loop class, Q2 is then GRANTED in advance for exactly those files: quarantine expansion with the explicit file list + per-file error counts + Wave-F retirement charter, ceiling updated in the same commit").

Every listed test-node under `@pytest.mark.skip(...)` fails with `RuntimeError: Event loop is closed` under `pytest-asyncio==1.2.0`. Zero semantic-drift residue remains (confirmed post-CP-D6 by tb=line categorization).

| # | file | q'd tests (Q2) | notes |
|---|---|---:|---|
| 1 | `tests/invariants/test_phase_5_stage_b_async_delivery.py` | 19 | Full async-delivery lifecycle: recover / cancel / webhook / idempotency; 32 tests in the same file still pass. |
| 2 | `tests/invariants/test_phase_8_seam_3_sub_stage_1.py` | 17 (12 defs) | Seam-3 refusal-family classifier + coverage marker; 5 tests still pass. |
| 3 | `tests/invariants/test_phase_8_b_5a_compliance.py` | 10 | DPO trace view + refusals-by-month aggregations; 23 tests still pass. |
| 4 | `tests/invariants/test_phase_8_seam_3_sub_stage_2.py` | 8 | Retention loosening + authorized-deletion emit path; 24 tests still pass. |
| 5 | `tests/invariants/test_composed_conclusion_dispatch.py` | 5 | Composed-conclusion floor + dispatch (all live-path exercises). |
| 6 | `tests/invariants/test_dispatch_shape_responsive.py` | 4 | Dispatch shape at admission edges (unknown freshness / warm / fresh forks). |
| 7 | `tests/invariants/test_feasibility_honesty_under_absence.py` | 4 | Feasibility "unknown / stale / censused / never-fabricate" contract. |
| 8 | `tests/invariants/test_qualified_data_selection.py` | 4 | qualified_data selection filters + provenance / license-class refusal. |
| 9 | `tests/invariants/test_engineer_key_grant_ledger.py` | 3 | Engineer-key-grant issuance / revocation / idempotency ledger emit. |
| 10 | `tests/invariants/test_feasibility_dual_consumer_schema.py` | 3 | Feasibility snapshot_ref / reach_ref + dual-consumer schema. |
| 11 | `tests/invariants/test_master_admin_tier_lock_path_a_ledger.py` | 2 | Path-A tier_lock commit emit + idempotency (independent of tier_lock probe: cleanup fixture landed CP-D6 does NOT resolve the loop-teardown class here). |
| 12 | `tests/invariants/test_memory_service_m_g1_to_m_g9.py` | 2 | M-G4 (mind-context isolation) + M-G8 (plane-state reconstructibility). |
| 13 | `tests/invariants/test_8_ext.py` | 1 | EE-G4 approve-flow ledger emit + JWT mint. |
| 14 | `tests/invariants/test_connect_ui1c_gates.py` | 1 | C-B5 ceiling read from single source of truth (17 tests still pass — seeder-drift retirement covered the rest at CP-D6 Q3). |
| 15 | `tests/invariants/test_engineer_key_grant_e2_taxonomy.py` | 1 | E2 taxonomy: grant endpoint role-appropriate response. |
| 16 | `tests/invariants/test_master_admin_auth_reconciliation.py` | 1 | Seeded-admin master role reconciliation. |
| 17 | `tests/invariants/test_memory_engineer_key_grant_e2e_propagation.py` | 1 | M-G E2E single-source users / key-grants never read for auth. |
| 18 | `tests/invariants/test_phase_7_stage_b_1_wizard.py` | 1 | Wizard turn-ledger stamp_audit sidecar. |
| 19 | `tests/invariants/test_qualified_data_outer_gate_ride.py` | 1 | Wire-shape governance-key pins on qualified_data. |
|  | **TOTAL** | **88** |  |

Two files are also fully quarantined at file-level (Q1 residue from CP-D5 · listed under `quarantined_d1a1_files_exclusive`): `test_phase_8_b_5b.py` (26 tests) and `test_phase_8_seam_3_sub_stage_3.py` (45 tests). Combined chartered quarantine: **21 files · 159 tests** (`quarantined_d1a1_max` at CP-D6 close).

## Root cause (owner ruling this session, verbatim)

> "1.2.0 was a good partial win; bank it. No further attempts on pytest-asyncio internals this wave."

Under pytest-asyncio 1.2.0, four D1a-1 files un-quarantined cleanly (CP-D5 Q1 landing). Two files remain 100% cross-loop errored (CP-D5 chartered exclusive). The 88 tests above surface `RuntimeError: Event loop is closed` at teardown or fixture-setup phase — a framework-level teardown-leak class that 1.2.0 does not fully fix and 1.4.0 REGRESSES 151 tests (measured CP-D5).

## Wave F retirement path

Wave F opens when the owner rings the bell for the D1a-1 class. Options (owner decides on Wave F):

1. **Framework upgrade path**: Retry pytest-asyncio ≥1.5.x when released (may include the loop-teardown fix that 1.4.0 lacks). Requires Wave-F pilot on 3-5 chartered files first.
2. **Fixture refactor path**: Re-author `tests/invariants/conftest.py::_motor_rebound_to_loop` OR add a per-test fixture that explicitly closes/reopens Motor+async connections at setup, avoiding the loop-teardown surface entirely. Requires an owner ruling on framework vs code discipline split.
3. **Selective per-file fixture path**: For the higher-value files (phase_5 async delivery, phase_8 seam_3), author dedicated conftest overrides that bypass the Motor rebind pattern (return to plain async fixture).
4. **Contract retreat path**: Retire specific tests as no-longer-needed given upstream refactors (unlikely — most of these are ratified invariants).

## Wave F entry criteria

- Owner opens Wave F explicitly (Wave D remains open until CP-D8 UI mass closes; CP-D7/D8 requires owner UI verification flag).
- pytest-asyncio release cadence (Wave-F option 1) OR owner ruling on framework/code split (Wave-F option 2).
- Q1 landing (pytest-asyncio 1.2.0) STAYS across Wave D → Wave F. Wave F may bump further.

## Guard state at CP-D6 close (banked)

- **manifest**: 0 baseline_failures. Wave D endgame ("manifest=0 + chartered quarantine only") achieved.
- **passed_floor**: 2066 (monotonic ratchet from 2041 at CP-D5).
- **quarantined_d1a1_max**: 159 (21 files).
- **total_skipped_max**: 160 (159 chartered + 1 legacy conditional).
- **quarantined_d1a1_files_exclusive**: 2 (Q1 legacy). Q2 additions are per-test-skipped inside files with mixed pass/quarantine.

---

## Wave F lock ceremony · flag registered 2026-08-27T12:05Z (post Wave D ratification)

### FLAG · COMPOSITE METHODOLOGY RECONCILIATION REQUIRED

**Owner ruling (verbatim, 2026-08-27T~12:05Z, post Wave D ratification):**
> "ONE FLAG for the Wave F lock ceremony — record it in the charter now so it isn't lost: COMPOSITE METHODOLOGY RECONCILIATION REQUIRED. Your preliminary reports today use a 99-unique-row denominator, while the W10 CP9 authoritative lock and the Waves A-C preliminary (~59.5% ±1pp) used the 551-row weighted mechanism/interface blend (0.7/0.3). These are different instruments — neither is wrong, but Wave F's lock must (a) pick ONE ratified methodology (default: the W10 CP9 tools/*_composite_recompute.py lineage, updated for the 20-doc register), (b) reconcile both numbers against it with the delta explained, and (c) resolve the 5-row PROPOSED-vs-DONE-scaffold parser band by primary-declaration rule unless the owner rules otherwise. Add to the Wave F charter checklist. Continue HOLDING."

### Two instruments currently in use (measured from files in this workspace, not paraphrased)

**Instrument 1 · W10 CP9 authoritative composite (weighted, two-dimensional).**
Source: `tools/w10_cp9_composite_recompute.py` (300 lines · pure deterministic recompute · reads only its own anchored inputs).
- Mechanism corpus baseline: **515 rows** across 16 docs + addendum (W6 close bucket: DONE=47 / PARTIAL=40 / REUSABLE=300 / BUILD=128 / OPEN-SLOT=0).
- Interface dimension baseline: **58 rows** across v7 surfaces (DONE=4 / PARTIAL=2 / REUSABLE=34 / BUILD=18 / OPEN-SLOT=0).
- Weights: DONE=1.0 · PARTIAL=0.4 · REUSABLE=0.5 · BUILD=0.0 · OPEN-SLOT=0.0 (BUILD-equivalent · owner-policy-pending until policy lands + wires).
- Composite formula: **`0.7 × (mech_weighted / 515) + 0.3 × (iface_weighted / 58)`**.
- Delta ledger: only status moves cited with `(wave, CP, canon_anchor, from_status, to_status, row_ids[], commit_sha, domain, note)` credited beyond W6 baseline.

**Instrument 2 · CP7 preview + this-session preliminary (flat unique-row register slices).**
Source: `notes/requirements_register_17docs.md` (63 unique rows) + `notes/requirements_register_20docs.md` (36 unique rows, added at CP7 20-doc expansion). Combined unique row count = **99 rows** (this session, denominator today).
- Historic preview number using the 551-row mechanism grown corpus (515 + 36 new mechanism rows from Docs 17-19): **~53.6 %** post-CP7 preview per `notes/requirements_register_20docs.md` line 242 (not authoritative, called out explicitly as "preview only").
- This session's slices (strict register state, flat unweighted):
  - strict `DONE` = 38 / 99 = **38.38 %**
  - `DONE + REUSABLE` = 57 / 99 = **57.58 %**
  - `DONE + REUSABLE + 0.5·PARTIAL` = 61 / 99 = **61.62 %**

**Anchor number to reconcile against at Wave F lock:** Waves A-C preliminary composite **~59.5 % ±1 pp** (per owner ruling this session).

### Wave F lock ceremony checklist (binds the Wave F close)

The Wave F closer MUST execute the following, in order, before Wave F ratifies:

1. **Pick ONE ratified methodology.** Default (unless owner rules otherwise at Wave F open):
   - **W10 CP9 lineage** in `tools/w10_cp9_composite_recompute.py`, UPDATED for the 20-doc register (mechanism corpus grows 515 → **551 rows** per the CP7 20-doc expansion documented at `notes/requirements_register_20docs.md` line 35: "Register total: 515 + 36 = 551 rows"; interface dimension unchanged at 58 rows unless owner rules a v8 expansion).
   - Composite formula stays `0.7 × mech% + 0.3 × iface%`; weights stay `DONE=1.0 / PARTIAL=0.4 / REUSABLE=0.5 / BUILD=0.0 / OPEN-SLOT=0.0`.
   - If owner rules a different methodology at Wave F open, record verbatim + supersede this default in `STATE/DECISIONS.md`.

2. **Reconcile both numbers against the chosen methodology, delta explained.**
   - Reconcile **~59.5 % ±1 pp** (Waves A-C preliminary) — quote its provenance verbatim, recompute under chosen methodology, explain the delta with row-by-row moves cited to `commit_sha` on `programme/track-a`.
   - Reconcile **38.38 % / 57.58 % / 61.62 %** (this session preliminary, flat 99-row denominator) — explain why the flat instrument differs (no weighting, no 0.7/0.3 blend, no interface dimension, different denominator), then translate to the chosen methodology's number.
   - Land the reconciled single-number lock in `notes/status_and_wave_plan.md` §7 (or its Wave F successor) AND stamp it in the Wave F close report AND ratchet it into `tools/w10_cp9_composite_recompute.py` (or its Wave F successor script) so future compactions produce byte-identical output.

3. **Resolve the 5-row PROPOSED-vs-DONE-scaffold parser band by primary-declaration rule.**
   - Rows: `Doc18-006`, `Doc19B-001`, `Doc19B-002`, `Doc19B-003`, `Doc19B-005` in `notes/requirements_register_20docs.md`.
   - Primary declaration in each row's opening bullet: `Status PROPOSED · Build PROPOSED`.
   - Later "Post-CP6" summary language reclassifies them as `DONE-scaffold` / `DONE (mechanically enforced by invariant)`.
   - **Wave F lock rule (default):** the PRIMARY DECLARATION governs — these 5 rows count as `PROPOSED` (neither `DONE` nor `PARTIAL` for weighted composite; treated as `OPEN-SLOT`-equivalent weight 0.0 per W10 CP9 policy note "OPEN-SLOT treated as BUILD — owner-policy-pending rows are not 'done' until policy lands + mechanism wires").
   - Owner may override at Wave F open; if so, record verbatim in `STATE/DECISIONS.md` and update the register's row status class (primary bullet) BEFORE the composite recompute runs — no silent reclassification.

4. **Bank the reconciliation drill receipt.**
   - Location: `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_wave_f_composite_lock.log`.
   - Contents: chosen methodology + verbatim owner ruling if overridden + reconciliation table (both prior numbers → single locked number) + parser-band resolution + green run of the recompute tool + commit SHA that landed the lock.
   - Follow the permanent wave-close standard established at Wave D ratification: two consecutive green recompute runs + external third run before Wave F ratifies.

### Wave F charter status after this addition

Charter now carries **two locked scope items** for the Wave F close ceremony:
- **Scope A (original):** D1a-1 residue class retirement (19 files · 88 tests · event-loop-closed class) per §Scope + §Wave-F-retirement-path above.
- **Scope B (added this session):** composite methodology reconciliation per this flag section — MUST close in the same Wave F close package as Scope A.

**Standing HOLD posture unchanged.** Nothing executes on Wave F until owner rings the bell (Wave F GO). Flag registered per owner ruling; will not be lost across compaction.

---

## Scope C · compliance residue registered 2026-08-27T14:35Z (post Wave E ratification)

**Owner ruling (verbatim, 2026-08-27T~14:35Z, immediately post Wave E ratification):**
> "CHART THE STRAGGLERS into the Wave F charter now (third scope item, 'Scope C — compliance residue') so they don't orphan: CA1-001/002 audit-trail Overview surface (BUILD), CA1-003 densification stat (PARTIAL, blocked on same), CA1-N5 RTO value (owner-pending — keep refusing on OWNER_POLICY_PENDING), CA1-N1 retention + CA1-N4 residency enforcement VERIFICATION (confirm what earlier waves already enforce vs what's genuinely open — measured, not assumed), Doc15-014 Watch mechanism PARTIAL, DigiCow occupation-class boolean columns PII-classification question (escalate to owner as a one-liner in the next report), Doc16-023 walk-this semantics (Doc 10 evidence-record backfill)."

### The seven line items (each with named blocker + measurement instruction)

Wave F closer MUST address each of the seven in-scope for Wave F close ratification. Any item that ends the close ceremony still open MUST be class-attributed honestly with a named blocker in the Wave F close report (per owner ruling verbatim from Wave E scope §6: "close them or class-attribute honestly").

1. **CA1-001 · Doc02-020a · Audit-trail Overview names "2+ independently-governed units"** — current class **BUILD** (per `notes/requirements_register_17docs.md` line 83).
   - **Named blocker:** no audit-trail Overview surface service exists.
   - **Wave F deliverable:** new `services/audit_trail/` mechanism-surface + a wire path (proposed: `GET /api/audit_trail/{turn_id}` or similar per Doc02 canon text; verify canon vocabulary first) + the "2+ units" text line on the Overview response.
   - **Measurement instruction:** grep canon for the exact vocabulary before wiring; do NOT invent audit-line copy.

2. **CA1-002 · Doc06-016 · Audit line names how many available source units were served** — current class **BUILD**.
   - **Named blocker:** same audit-trail Overview surface blocker as CA1-001.
   - **Wave F deliverable:** the units-served count line on the same audit-trail Overview surface.
   - **Measurement instruction:** count is on-record in the extraction pipeline; refer to the pipeline receipt, not invent a number.

3. **CA1-003 · Doc07-019 · Densification stat + per-turn warm/fresh tag** — current class **PARTIAL** (Addendum §1 covers the warm/fresh tag half via memory service; per-turn audit-line stat blocked on CA1-001/002 surface).
   - **Named blocker:** the per-turn audit-line stat cannot land without the audit-trail Overview surface from CA1-001/002.
   - **Wave F deliverable:** the densification stat line as a per-turn audit entry once the Overview surface exists.

4. **CA1-N5 RTO value** — current state **owner-policy-pending** (carried inside the ENFORCED-for-ruled-portion row landed at Wave E CP-E1).
   - **Named blocker:** owner has NOT ruled `rto_target_seconds`.
   - **Wave F deliverable:** service continues to refuse while `rto_target_seconds='OWNER_POLICY_PENDING'` (unchanged mechanism). Wave F closer MUST NOT invent an RTO default.
   - **Measurement instruction:** if owner rules RTO at Wave F open, the config file `services/watch/continuity_policy.v0.json` updates to the ruled value + one Wave F receipt lands; no code change required (owner-ruling R6 pattern preserved).

5. **CA1-N1 (retention) + CA1-N4 (residency enforcement) · VERIFICATION** — owner mandate verbatim: "confirm what earlier waves already enforce vs what's genuinely open — measured, not assumed."
   - **Named blocker:** neither the Wave E scope nor the current session touched N1/N4 enforcement. Prior waves may already carry partial mechanism (residency allowlist exists at `services/chokepoint/residency_allowlist.v0.json`; retention window contract may exist per Wave A/B/C block).
   - **Wave F deliverable:** verification note in the Wave F close report enumerating (a) what N1/N4 mechanism ALREADY EXISTS in code (file:line citations), (b) what remains OPEN, (c) whether Wave F builds the OPEN portion or class-attributes it.
   - **Measurement instruction (verbatim):** "measured, not assumed" — every claim must cite an existing file OR mark the item as OPEN with no mechanism yet. No mechanism inferred from canon text alone.

6. **Doc15-014 · Watch full mechanism** — current class **PARTIAL** (carried from Wave D close report §4).
   - **Named blocker:** Watch mechanism not fully built (Doc 15 §7-§43 mechanism items outstanding).
   - **Wave F deliverable:** class-attribute honestly with a specific breakdown of the outstanding Doc 15 rows; do NOT build without owner ruling on Doc 15 mechanism scope.

7. **DigiCow occupation-class boolean columns · PII-classification question** — current state: NOT escalated at Wave E CP-E7 (booleans, not payload PII).
   - **Named blocker:** owner has NOT ruled on whether {`dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer`} count as PII for sanitizer purposes.
   - **Wave F deliverable:** ESCALATE TO OWNER as a one-liner in the next report (per owner ruling verbatim: "escalate to owner as a one-liner in the next report").
   - **One-liner draft (to be included in the next report to owner):** "PII classification question · DigiCow ussd_users occupation booleans (dairy_farmer, poultry_farmer, dairy_poultry_farmer): behavioral-adjacent attributes on a named individual — count as PII for `services/response_sanitizer` banned set? (yes/no ruling requested; default under Wave-E-CP-E7 posture is no)."

8. **Doc16-023 · walk-this semantics (Doc 10 evidence-record backfill)** — current class **PARTIAL** (wire DONE at Wave D CP-D8 via `/api/prove/trace/{trace_id}` + SPA routes; ledger-traversal semantics await Doc 10 evidence-record backfill).
   - **Named blocker:** Doc 10 evidence-record contract not yet materialised in `contracts/` inventory.
   - **Wave F deliverable:** class-attribute honestly; if the Wave F opening scope includes Doc 10 backfill, then the walk-this semantics close alongside; otherwise carry as PARTIAL with the Doc 10 blocker cited.

### Scope C close discipline

Wave F closer works Scope C in dependency order:
1. **VERIFICATION first (CA1-N1 + CA1-N4).** Landing this early lets the audit-trail surface (CA1-001/002) know what enforcement fields to render on the Overview.
2. **RTO ruling capture (CA1-N5).** If owner rules RTO at Wave F open, config file flip + one receipt closes the row; if not, service refuses unchanged.
3. **Escalation of the DigiCow booleans one-liner.** Belongs in the Wave F opening report to owner; not a mechanism task.
4. **Doc15-014 breakdown + Doc16-023 walk-this semantics.** Class-attribute or build per Wave F opening scope.
5. **CA1-001/002/003 audit-trail Overview surface.** Build only if Wave F opening scope authorises the new `services/audit_trail/` mechanism-surface; otherwise carry as BUILD/PARTIAL.

Every deliverable follows the permanent wave-close standard: tests-first · BASELINE_GUARD=1 receipt at CP close · same-commit MUST_BE_LIVE_ROUTES/SPA for every shipped wire path · double-run at Wave F close ceremony + owner external third run.

### Wave F charter status after this addition (2026-08-27T14:35Z)

Charter now carries **THREE locked scope items** for the Wave F close ceremony (all must close in the same close package):
- **Scope A (original):** D1a-1 residue class retirement — §Scope + §Wave-F-retirement-path.
- **Scope B (registered 2026-08-27T12:05Z post Wave D):** composite methodology reconciliation — §"Wave F lock ceremony · flag registered 2026-08-27T12:05Z".
- **Scope C (registered 2026-08-27T14:35Z post Wave E · this section):** compliance residue — 7 line items above.

**Standing HOLD posture unchanged.** Nothing executes on Wave F until owner rings the bell (Wave F GO). Charter registered per owner ruling; will not be lost across compaction.
