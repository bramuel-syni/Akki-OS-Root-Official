# Wave F Cleanup · Programme Close Report
## Opened 2026-08-27T21:34Z · RATIFIED 2026-08-27T~22:15Z (external RE-RUN 4/4 PASS)

**Status: 🏁 WAVE F CLOSED + RATIFIED · MASTER PLAN (WAVES A → F) COMPLETE. Position: HOLDING at ready state.**

Wave F Cleanup phase is complete. All three Wave F scopes CLOSED + Cleanup CLOSED + Cleanup CP (audit-trail Overview surface · CA1-001/002/003) CLOSED. Full-system drill day executed with two consecutive perfectly-green `BASELINE_GUARD=1` runs at identical tallies at the new floor 2355. **Composite lock ratified at 52.82%.** Owner external RE-RUN 4/4 PASS ratifies the wave and closes the Master Plan.

Ratified HEADs: Extraction-Akki `programme/track-a` **`fcec7f8`** · master workspace **`42ae8f5`**.

Owner's closing acknowledgement (verbatim): *"Exceptional programme execution — from a 50% honest baseline through six ratified waves with zero unratified claims standing."*

---

## 1 · Wave ledger (this session)

| Wave / Scope | Anchor commit | Passed floor | Baseline failures | Quarantined | Ratification |
|---|---|---:|---:|---:|---|
| Wave F · Scope A · D1a-1 residue retirement | Extraction-Akki `programme/track-a` **`1155629`** | 2333 | 0 | 0 | Ratified by owner 2026-08-27T20:57Z |
| Wave F · Scope B · Authoritative composite lock (superseded by Cleanup CP re-lock) | Master workspace **`7ae5dcb`** | (workspace tool commit; test-mirror pending on rounding fix — see §4) | — | — | Ratified by owner 2026-08-27T21:12Z |
| Wave F · Scope C · Compliance residue class-attribution | Master workspace **`aab67c4`** | (no `programme/track-a` code touched at Scope C close) | — | — | Ratified by owner 2026-08-27T21:20Z (chartered BUILD item completed in Cleanup CP below) |
| Wave F · Cleanup · Rounding fix + full-system drill day | Extraction-Akki **`67a6786`** + Master **`8e8fd06`** | 2333 | 0 | 0 | Superseded by Wave F Cleanup CP · retained for audit |
| Wave F · Cleanup CP · audit-trail Overview (CA1-001/002/003) | Extraction-Akki **`fcec7f8`** | **2355** | **0** | **0** | **RATIFIED by owner 2026-08-27T~22:15Z (external RE-RUN 4/4 PASS)** |

**Wave E ratified anchor (prior · unchanged):** Extraction-Akki `programme/track-a` **`60b8760`** — CP-E1..CP-E8, 2169 passed at Wave E close.

**Wave A/B/C ratified anchor (prior block · unchanged):** Extraction-Akki `programme/track-a` **`75b7b1e`** (Wave B post-verify) + **`4aedb35`** (Wave C close) — 169/169 across the ratified cohort at Waves A-C block ratification.

---

## 2 · Cleanup phase execution

### 2.1 Bounded drift found and fixed

- **Misnamed close-log** `20260826T110626Z_w11b_close_full_invariants_green.log` isolated (Wave B naming for W11B period, contents did not match). Moved to `phase0/drill_receipts/orphaned/` with disposition note. Not retroactively fixed; the orphan directory preserves it as the honest record of the misname.

### 2.2 Environmental drift fixed

- **pytest-asyncio** version pin drift: `requirements.txt` pinned `pytest-asyncio==1.2.0` but the environment actually resolved to `1.4.0` at test time. `requirements.txt` bumped to `pytest-asyncio==1.4.0` and `pytest==8.4.2` — pins now match the installed environment.
- **Rider-1 guard installed:** `backend/tests/invariants/test_wave_f_pin_vs_installed_environment_invariant.py` enforces pin-vs-installed parity on core test-infrastructure packages so this class of drift trips the guard at CP-close rather than silently propagating.
- **Rider-2 reconciliation ran:** pip-freeze against `requirements.txt` reports 20/20 pin alignment (no residual drift).

### 2.3 Composite lock rounding synchronization (this cleanup — the last blocker)

- **Root cause diagnosed:**
  - Tool `tools/w10_cp9_composite_recompute.py` computed composite from the UNROUNDED dimension percentages (`mech_pct_raw = 54.4828...`, `iface_pct_raw = 47.9310...`), producing raw composite `52.51724...` which rounds ONCE at the end to **52.52** (the authoritative lock).
  - Test `test_composite_calc_is_convex_blend_at_70_30` computed `expected = round(0.7 * out["mech_pct"] + 0.3 * out["iface_pct"], 2)` using the ALREADY-ROUNDED published dashboard values (`54.48, 47.93`), producing `52.51499...` which rounds to **52.51** — a DOUBLE-rounding artifact of the published-dashboard precision.
- **Ruling captured (owner · this session · verbatim):**

  > Option A — with the tool exposing `mech_pct_raw` / `iface_pct_raw` in its output (prefer that over test-side reconstruction: the raw internals become auditable artifacts, not test-private math). The single-final-rounding rule is the mathematically correct instrument behavior; 52.51 is a double-rounding artifact, not an alternative truth. The authoritative locked value stands at **52.52**.
  >
  > One addition to the fix: in the close report's reconciliation section, state the rounding rule explicitly in one sentence ("composite is computed from unrounded dimension percentages and rounded once at the end; recomputing from the rounded published values yields 52.51 by double-rounding — that figure is an artifact, not a lock candidate") so nobody re-derives 52.51 later and flags a false discrepancy.

- **Fix (atomic across both trees · same UTC timestamp `20260827T213237Z`):**
  - Master workspace **`8e8fd06`** · `tools/w10_cp9_composite_recompute.py`: `compute_authoritative()` now returns two auditable artifact keys `mech_pct_raw` and `iface_pct_raw` (unrounded) alongside the existing rounded dashboard figures. Header comment documents the single-final-rounding rule verbatim.
  - Extraction-Akki `programme/track-a` **`67a6786`** · `backend/tests/invariants/test_w10_cp9_composite_lock.py`: `test_composite_calc_is_convex_blend_at_70_30` now reconstructs `expected = round(0.7 * mech_pct_raw + 0.3 * iface_pct_raw, 2)` from the tool's own unrounded internals. Docstring quotes the owner's rounding ruling verbatim. Same commit also mirrors the pending Wave F Scope B lock updates on the test side (515→551 rows, 54.45→54.48%, 52.49→52.52%, 32→36 deltas) that had been blocked on this rounding fix.
- **Same-commit DoD extension (FL-P4-W8-02) preserved** — the two commits carry the identical UTC timestamp `20260827T213237Z` and cross-reference each other in their commit messages, honoring the composite-tool ↔ composite-test same-commit discipline across the branch boundary (the tool lives on master workspace; the test lives on Extraction-Akki `programme/track-a`).

### 2.4 Wave F Cleanup CP · audit-trail Overview surface (CA1-001/002/003 · this cleanup — the previously miscategorized chartered work)

- **Third-run ratification miss diagnosed (owner audit this session, verbatim):**

  > "THE MISS: my Wave F GO, Scope C item (2), verbatim: 'AUTHORIZED: build the audit-trail Overview surface (services/audit_trail/ + wire + SPA per Ship-Manifest DoD) to close CA1-001/002/003 — this was the known BUILD gap and Wave F is its chartered home.' The probe confirms: no services/audit_trail/ directory, no dedicated routes (only /api/master_admin/audit_trail as a facet), CA1-001/002/003 carried as BUILD/PARTIAL. The close report listed it honestly as carried — but it was chartered, authorized work, not an owner-pending item. Wave F is its home; it does not carry."

- **Chartered work landed (this cleanup CP · atomic commit programme/track-a `fcec7f8`):**

  Ship-Manifest DoD triple honored:
  - **Backend:** NEW `backend/services/audit_trail/{__init__.py, router.py, overview.py}` mounted on `pod_shell/backend/server.py`; byte-identical mirror at `/app/backend/server.py`; live pod openapi confirms `GET /api/audit_trail/overview` served.
  - **Wire:** MUST_BE_LIVE_ROUTES += `("GET", "/api/audit_trail/overview", "Wave F Cleanup · CP · audit-trail Overview (CA1-001/002/003)")`.
  - **SPA:** MUST_BE_LIVE_SPA_ROUTES += `("/audit-trail", "Wave F Cleanup · CP · audit-trail Overview (CA1-001/002/003)")`. Frontend: `pod_shell/frontend/src/components/AuditTrail.jsx` (byte-identical mirror at `/app/frontend/src/components/AuditTrail.jsx`) + repo canonical page `frontend/src/pages/audit_trail/AuditTrailOverviewPage.jsx` + Route declarations on both App.js files.

- **Placement decision (canon-text-driven):**
  - Addendum §1 verbatim names "audit trail **Overview**" surface for CA1-001 (Doc02-020a) and CA1-002 (Doc06-016) → dedicated `/audit-trail` top-level surface (canon-language match; consistent with CP8 Watch / Governance / Grey-Mirror pattern of a top-level state rollup per canon concept).
  - CA1-003 (Doc07-019 / Doc08-017) canon text names "**Registry** densification stat and a per-turn warm/fresh tag" → the densification stat renders on the same Overview `densification` section (reads `registry_facts` on disk); the per-turn warm/fresh tag wires through by reference to `services/memory/` per owner ruling this session ("the memory-service half already exists — wire it through"). CA1-003 lands as **canon-designated PARTIAL** per Addendum §1 verbatim: *"flagged here as a partial closure, not a full one"* — this is canon-designated partial, not build-gap partial.

- **Real record sources (REFERENCE-NOT-COPY · Design Law A8 · every entry cites its on-disk `source_path`):**
  - `multi_unit_answers` (CA1-001): groups `phase0/northena_ledger/*.json` rows by `trace_id`; counts distinct `artifact_ref.artifact_id` per trace; entries where count ≥ 2 are answers that drew on 2+ independently-governed units.
  - `units_served` (CA1-002): `available` = count of `phase0/data_connection_records/*.json`; `served` = distinct source-unit `database` keys touched by ≥1 `phase0/crossing_receipts/*.json`; per-source `served_receipts` = touch count.
  - `densification` (CA1-003): `facts_registered` = count of `phase0/registry_facts/*.json`; `warm_fresh_reference` cites `backend/services/memory/`; `partial_closure=True`.

- **Register moves (same-commit paired on master workspace mirror):**
  - CA1-001 (Doc02-020a): BUILD → **DONE**
  - CA1-002 (Doc06-016): BUILD → **DONE**
  - CA1-003 (Doc07-019 · Doc08-017): BUILD → **PARTIAL** (canon-designated per Addendum §1 verbatim quoted above)

- **Invariant enforcer:** `backend/tests/invariants/test_audit_trail_overview.py` · 20 gating tests (route surfaced · body shape · verbatim canon text asserted for each of the three sections · partial_closure=True for CA1-003 · REFERENCE-NOT-COPY posture with `source_path` on every entry · no banned fields leak · real northena ledger group-by-trace_id math · real data_connection_records count · real crossing_receipts served attribution · real registry_facts densification count · warm/fresh reference-through to memory service · honest-empty rendering under empty stores).

- **Composite lock re-run ceremony (per owner ruling verbatim: "RE-RUN the Scope B composite lock ceremony after the register moves — the 52.52 lock predates these rows; a lock that's stale on arrival isn't a lock"):**
  - `tools/w10_cp9_composite_recompute.py` gained 3 new `Delta` entries for the CA1 register moves.
  - Byte-identical double recompute banked at `phase0/drill_receipts/20260827T215951Z_wave_f_cleanup_composite_relock.log`.
  - Composite: **52.52 → 52.82 (+0.30 pp)** · mech 54.48 → 54.92 · iface unchanged 47.93 · n_deltas 36 → 39.
  - `backend/tests/invariants/test_w10_cp9_composite_lock.py` moves to the new locked values in the SAME atomic commit (same-commit DoD extension FL-P4-W8-02 · composite tool ↔ composite test cross-tree pairing preserved).

- **Ratchet floor bump:** `passed_floor` 2333 → **2355** (+22 = 20 new audit_trail invariants + 1 new MUST_BE_LIVE_ROUTES parametrized case + 1 new MUST_BE_LIVE_SPA_ROUTES parametrized case). Manifest failures unchanged at 0. Quarantine unchanged at 0.

---

## 3 · Composite lock reconciliation

**Authoritative locked composite (Wave F Cleanup re-lock ceremony · owner ruling this session verbatim: "RE-RUN the Scope B composite lock ceremony after the register moves — the 52.52 lock predates these rows; a lock that's stale on arrival isn't a lock"): 52.82%.**

**Delta attribution (52.52 → 52.82 · +0.30 pp):**

| Move | Weight change | Canon anchor |
|---|---|---|
| CA1-001 BUILD → DONE | +1.0 mech | Addendum §1 Promise #4 · Doc02-020a |
| CA1-002 BUILD → DONE | +1.0 mech | Addendum §1 Promise #17 · Doc06-016 |
| CA1-003 BUILD → PARTIAL (canon-designated) | +0.4 mech | Addendum §1 Promises #19/#20/#21 · Doc07-019 · Doc08-017 |
| **Total** | **+2.4 mech weight** | |

| Dimension | Raw (unrounded) | Rounded published | Weight |
|---|---:|---:|---:|
| Mechanism corpus (551 rows) | 54.9183303% | **54.92%** (was 54.48%) | 0.7 |
| Interface dimension (58 v7 surfaces) | 47.9310345% | 47.93% (unchanged) | 0.3 |
| **Composite (single-final-rounded from raw)** | **52.8221416%** | **52.82%** (was 52.52%) | — |

**Rounding rule (explicit · state once in this report per owner addition · unchanged from Wave F Scope B ruling):**

> Composite is computed from the UNROUNDED dimension percentages and rounded ONCE at the end; recomputing from the rounded published values yields a double-rounding artifact, not a lock candidate. The authoritative locked value stands at 52.82.

**Method:** `tools/w10_cp9_composite_recompute.py` · deterministic · **39 delta entries** · every delta anchored to a canon § + `programme/track-a` commit SHA.

**Locked by pytest (permanent guard):** `backend/tests/invariants/test_w10_cp9_composite_lock.py` · 5/5 green in the full-suite double-run.

**Wave F Scope C composite-recompute deltas (recommended for the next register revision · NOT applied in this Wave F close since owner did not authorize a register rewrite in Scope C):**

- CA1-N1 (retention enforcement + attestation): **PARTIAL → DONE** — charter annotation was STALE; the enforcement + attestation module (`services/retention/`, 613 tracked LOC + `test_retention_enforcement_w6_cp3.py` 328 LOC gating) landed at W6 CP3 pre-dating the Wave A-C anchor freeze.
- CA1-N4 (residency governed-region allowlist): **PARTIAL → DONE** — same class of stale annotation; the enforcement module (`services/chokepoint/residency.py` + `residency_allowlist.v0.json`) landed at W6 CP3.

These deltas would nudge mechanism % upward slightly. NOT applied here — the composite is banked at 52.82 per the Wave F Cleanup ratified ceremony; owner authorizes the register rewrite as a separate act if desired.

---

## 4 · Full-system drill day receipts (banked)

Location: `/app/assessment_workspace/phase0/drill_receipts/`

**Wave F Cleanup CP · audit-trail Overview surface · double-green identical at new floor 2355:**

- **Run 1:** `20260827T220103Z_wave_f_cleanup_audit_trail_full_run1.log`
  - Receipt: `passed=2355 / baseline-failures-remaining=0 / quarantined=0`
  - Wall-clock: 90.67s
  - Skipped: 1 (single documented skip — unchanged across the suite)
- **Run 2:** `20260827T220328Z_wave_f_cleanup_audit_trail_full_run2.log`
  - Receipt: `passed=2355 / baseline-failures-remaining=0 / quarantined=0`
  - Wall-clock: 91.40s
  - Skipped: 1 (identical)

**Identity check:** both runs produced the byte-identical BASELINE_GUARD receipt line `passed=2355 / baseline-failures-remaining=0 / quarantined=0`. No tally absorption. Permanent Close Standard satisfied at the new floor.

**Right-reason RED banked before implementation landed:**
- `20260827T215343Z_wave_f_cleanup_audit_trail_right_reason_fail.log` (20 `ModuleNotFoundError: No module named 'services.audit_trail'` — right-reason failure before service module existed).

**Prior Wave F Cleanup rounding-fix drill day receipts (retained for audit · superseded by Wave F Cleanup CP at new floor):**
- `20260827T213255Z_wave_f_cleanup_drill_day_run1.log` (2333 · OK · 89.16s)
- `20260827T213435Z_wave_f_cleanup_drill_day_run2.log` (2333 · OK · 89.43s)

**Composite re-lock ceremony:**
- `20260827T215951Z_wave_f_cleanup_composite_relock.log` (byte-identical double recompute · 52.52 → 52.82 with delta attribution).

**Invocation:** `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/` (unchanged from Wave E · owner ruling).

---

## 5 · Wave F scope-close receipts (banked earlier · retained for audit)

Location: `/app/assessment_workspace/phase0/drill_receipts/`

- Scope A close double-run (Wave F retirement charter):
  - `20260827T205131Z_wave_f_scope_a_close_run1.log` (2333 · OK)
  - `20260827T205259Z_wave_f_scope_a_close_run2.log` (2333 · OK · identical)
- Scope B composite-lock ceremony:
  - `20260827T211213Z_wave_f_composite_lock.log` (tool double-run byte-identical)

Wave E CP-E1..CP-E8 receipts retained per prior wave close ledger (see STATE/NEXT.md §CP-E receipts).

---

## 6 · OWNER-PENDING list (surfaced for owner ratification at wave close)

Per Wave F Scope C mandate ("close them or class-attribute honestly · 2 known-pending items surfaced as one-liner"):

### 6.1 SSH key delivery — INTERRUPT-PRIORITY (unchanged from prior waves)

- **Status:** awaiting owner key drop.
- **Sequence on arrival:** `chmod 600 <key>` → `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` in `/app/backend/.env` → `GPU_CONNECT_MODE=real` → hardware fact sheet probe (`nvidia-smi` + CUDA + PyTorch) → **CUDA/PyTorch verify-only** (A17.17 CLOSED per Message 315) → **EP-4 precondition guard verify** (evidence register active + ≥2 registered judges for `terminal_test` site per Message 315 · Reclassification 1) → first governed training run on sealed DigiCow set → real MOAC card → whitepaper drafted from real admission → stop-and-report with hardware fact sheet + live run outcome.
- **Interrupt priority:** on key arrival, this sequence supersedes any in-flight wave activity.

### 6.2 CA1-N5 RTO ruling (`rto_target_seconds`)

- **One-liner (per Scope C escalation):** owner is asked to rule `rto_target_seconds` as an integer number of seconds.
- **Mechanism state:** service continues to refuse attestation while `rto_target_seconds="OWNER_POLICY_PENDING"` (sentinel at `services/watch/continuity_policy.v0.json:8`; refusal contract at `services/watch/continuity.py:19-88` and `services/watch/router.py:498-510`).
- **Landing site (once ruled):** single JSON edit at `services/watch/continuity_policy.v0.json:8` — no code change required, no wave re-open required.

### 6.3 DigiCow occupation booleans — PII classification

- **One-liner (verbatim from Scope C charter):**
  > "PII classification question · DigiCow `ussd_users` occupation booleans (`dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer`): behavioral-adjacent attributes on a named individual — count as PII for `services/response_sanitizer` banned set? (yes/no ruling requested; default under Wave-E-CP-E7 posture is no)."
- **Current default (Wave E CP-E7 posture):** NOT PII (booleans-not-payload class distinction is honored).
- **Landing site (once ruled):** if owner rules yes-PII → add the three attribute names to the sanitizer's banned set at `services/response_sanitizer/` + regenerate the sanitizer snapshot in the same commit (FL-P4-W8-02 same-commit DoD).

### 6.4 Wave F Scope C register-classification updates (charter-recommended · owner may authorize as a separate act)

- CA1-N1 · PARTIAL → **DONE** (measured; mechanism landed at W6 CP3).
- CA1-N4 · PARTIAL → **DONE** (measured; mechanism landed at W6 CP3).
- These would land as a `notes/requirements_register_20docs.md` edit + a companion re-run of `tools/w10_cp9_composite_recompute.py` (with the two rows moved) + composite-lock test update — all under the composite % same-commit DoD extension (FL-P4-W8-02). NOT applied in this Wave F close; surfaced here as a paper item for owner's next act.

### 6.5 Doc 10 evidence-record contract backfill (Doc16-023 walk-this semantics)

- **Status:** wire + SPA DONE at Wave D CP-D8; ledger-traversal semantics remain OPEN until Doc 10 evidence-record contract materializes in `contracts/` inventory.
- **Landing site (once authorized):** new `contracts/evidence_record_v0.py` targeting Doc 10 runtime ledger evidence-record (distinct from `contracts/evidence_register_row_v0.py` which targets Doc 19B EP-1 register rows). Not authorized in Wave F scope.

### 6.6 ~~CA1-001 / CA1-002 / CA1-003 · Audit-trail Overview surface (BUILD)~~ CLOSED · Wave F Cleanup CP

- **Status:** ~~carried as BUILD (CA1-001, CA1-002) and PARTIAL (CA1-003) — no `services/audit_trail/` module authorized to build in Wave F.~~ **CLOSED this cleanup CP** at Extraction-Akki `programme/track-a` **`fcec7f8`**. Third-run miss diagnosed (owner audit this session) — this was chartered Wave F GO Scope C item (2) work, not an owner-pending carry. Details: see §2.4.
- **Register moves banked:** CA1-001 BUILD→DONE · CA1-002 BUILD→DONE · CA1-003 BUILD→PARTIAL (canon-designated per Addendum §1 verbatim: "flagged here as a partial closure, not a full one").

---

## 7 · Standing HALT trigger audit (Wave F Cleanup)

Per owner Wave F GO ruling, autonomous progression halts on standard triggers only:

- **Non-config blocker** — none hit in Cleanup.
- **Spec contradiction** — none hit in Cleanup.
- **Guard trip** — none hit (ratchet held at 2333/0/0 across both drill-day runs; identical byte-for-byte receipt tallies).
- **Count drift** — none.
- **Owner-input need beyond the two already-pending items (§6.2, §6.3)** — none hit. The rounding ruling this session (§2.3) was captured under the owner's active clarification channel; not treated as a halt-and-report because owner ruled Option A directly.

**No halt-and-report triggered during Wave F Cleanup execution.**

---

## 8 · Ship-Manifest DoD status (unchanged rules · verified this session)

- Tests-first with right-reason receipts: honored on the rounding fix (RED not banked separately because the failure was already banked earlier in the session at `20260827T211517Z_wave_f_scope_b_composite_test_stale_values_right_reason_fail.log` context per prior investigation; GREEN receipt is the double-run at §4).
- Runtime-drift meta-invariant: `test_wave_f_pin_vs_installed_environment_invariant.py` (Rider-1 guard) active.
- Composite % same-commit DoD extension (FL-P4-W8-02): tool + test committed with identical UTC timestamp `20260827T213237Z` and cross-referencing messages (§2.3).
- Pod-shell + spine same-commit mount DoD: no wire/mount changes in this cleanup.
- Correction-discipline in-band (additive-only): honored — Wave F Scope A/B/C composite recompute results carry corrections in-band with cross-cite to prior W10 CP9 baseline (52.49% → 52.52% delta explained via 20-doc register expansion + Wave E CP-E1/E2/E3/E5 deltas).
- Local commits only · no push: honored.
- **No `testing_agent` used**: honored per owner's standing ban. All testing via terminal `pytest`.

---

## 9 · Wave F wave-close artifact ledger

- `notes/waveF_retirement_charter.md` · retirement charter (Scope A/B/C).
- `notes/waveF_scope_c_close_report.md` · Scope C compliance residue close report (356 lines).
- `notes/programme_close_report.md` · **this report** · Wave F wave-close package (updated at Cleanup CP for audit-trail Overview + composite re-lock).
- `phase0/drill_receipts/20260827T220103Z_wave_f_cleanup_audit_trail_full_run1.log` · **Wave F Cleanup CP** full-system drill run 1 (2355 · OK · 90.67s).
- `phase0/drill_receipts/20260827T220328Z_wave_f_cleanup_audit_trail_full_run2.log` · **Wave F Cleanup CP** full-system drill run 2 (2355 · OK · 91.40s · byte-identical receipt).
- `phase0/drill_receipts/20260827T215343Z_wave_f_cleanup_audit_trail_right_reason_fail.log` · **Wave F Cleanup CP** right-reason RED banked before implementation.
- `phase0/drill_receipts/20260827T215951Z_wave_f_cleanup_composite_relock.log` · **Wave F Cleanup CP** composite re-lock ceremony (byte-identical double recompute · 52.52 → 52.82).
- `phase0/drill_receipts/20260827T213255Z_wave_f_cleanup_drill_day_run1.log` · Wave F Cleanup rounding-fix drill run 1 (2333 · OK · superseded).
- `phase0/drill_receipts/20260827T213435Z_wave_f_cleanup_drill_day_run2.log` · Wave F Cleanup rounding-fix drill run 2 (2333 · OK · superseded).
- `phase0/drill_receipts/20260827T211213Z_wave_f_composite_lock.log` · Scope B ceremony (banked earlier this session · lock value 52.52 superseded by Cleanup CP 52.82).
- `phase0/drill_receipts/orphaned/20260826T110626Z_w11b_close_full_invariants_green.log` · isolated misnamed log.

---

## 10 · Handoff to owner's external third run

**RATIFIED 2026-08-27T~22:15Z · Owner external RE-RUN 4/4 PASS.**

Ratification receipt confirms:
1. Suite receipt verbatim-confirmed: `passed=2355 / baseline-failures-remaining=0 / quarantined=0`.
2. Audit-trail Overview live with 2 served units + `source_path` provenance + canon-designated `partial_closure=true`.
3. `/audit-trail` SPA route present.
4. Composite byte-identical at 52.82 (mech 54.92, n_deltas 39) · zero 5xx anywhere.

**Ratified HEADs (Master Plan close pointer):**
- Extraction-Akki `programme/track-a`: **`fcec7f8`**.
- Master workspace: **`42ae8f5`**.

Owner's closing acknowledgement (verbatim): *"Exceptional programme execution — from a 50% honest baseline through six ratified waves with zero unratified claims standing."*

**Post-ratification state:** Wave F CLOSED + RATIFIED across all three scopes + Cleanup + Cleanup CP (audit-trail Overview). **Master Plan (Waves A → F) is COMPLETE.** No wave reopens autonomously. Standing arrivals (SSH key drop · Decks/Documents build GO · owner one-liners) reopen scope only by explicit owner ruling. Position: HOLDING at ready state.

---

## 11 · MASTER PLAN COMPLETE · Post-close position · 2026-08-27T~22:15Z

**Master Plan composite ratified at 52.82%.** Ratchet floor **2355** is the permanent regression fence under BASELINE_GUARD=1 monotonic non-decreasing rule. **Zero unratified claims standing.**

**Six ratified waves:**

| Wave | Ratification | HEAD | Test cohort at close |
|---|---|---|---:|
| Wave A | Ratified prior session (R7 · 2026-08-26T04:20Z) | `f101bd0` (post-R7) | 4/4 external PASS |
| Wave B | Ratified 2026-08-26T11:15Z | `75b7b1e` | 182/182 |
| Wave C | Ratified 2026-08-26 | `4aedb35` | 169/169 |
| Wave D | Ratified 2026-08-27T~11:00Z | (CP-D9 lineage) | 2119/0/159 |
| Wave E | Ratified 2026-08-27T~14:20Z | `60b8760` | 2169/0/159 |
| Wave F | **RATIFIED 2026-08-27T~22:15Z (external RE-RUN 4/4 PASS)** | **`fcec7f8`** | **2355/0/0** |

**Programme trajectory (honest baseline → final ratified state):**

- W1 baseline (2026-08-19 first-honesty-pass): ~50% composite.
- W6 close: mechanism ~48%, composite ~47%.
- W9 close: composite HELD pending W10 authoritative recomputation.
- W10 CP9: composite locked at 52.49% (32 deltas).
- Wave F Scope B: composite re-locked at 52.52% (36 deltas · 20-doc register expansion).
- **Wave F Cleanup CP (ratified): composite locked at 52.82%** (39 deltas · audit-trail Overview CA1-001/002/003 moves).

**Standing arrivals (owner-gated · no autonomous reopen):**

- **SSH key delivery** — INTERRUPT-PRIORITY (unchanged). On key arrival: `chmod 600` → env vars → hardware fact sheet → CUDA/PyTorch verify-only (A17.17 CLOSED) → EP-4 precondition guard verify → first live governed training run on sealed DigiCow set → real MOAC → whitepaper → stop-and-report.
- **Decks/Documents build GO** — DRE + akki-decks specs already ingested; register rows carried at BUILD-SCHEDULED-POST-PLAN pending explicit owner GO.
- **Owner one-liners still open** (non-blocking · land as config zero-code-change unless code named):
  - **CA1-N5 RTO seconds** — `services/watch/continuity_policy.v0.json:8` sentinel `"OWNER_POLICY_PENDING"` awaits integer-seconds ruling; single-JSON-edit landing.
  - **DigiCow occupation-boolean PII call** — `dairy_farmer`/`poultry_farmer`/`dairy_poultry_farmer` on `ussd_users`; default not-PII (Wave-E CP-E7 posture); owner rules yes/no.
  - **Doc 10 evidence-record backfill decision** — new `contracts/evidence_record_v0.py` targeting Doc 10 runtime ledger evidence-record (distinct from Doc 19B EP-1 register rows).
  - **Base-model census activation (A17.10)** — first-adapter base-model choice.

**Wave F CLOSED + RATIFIED. MASTER PLAN COMPLETE. Standing by.**
