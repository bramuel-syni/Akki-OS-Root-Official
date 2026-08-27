# Wave F Cleanup · Programme Close Report
## 2026-08-27T21:34Z

**Status: ready for owner's external third-run ratification.**

Wave F Cleanup phase is complete. All three Wave F scopes CLOSED; full-system drill day executed with two consecutive perfectly-green `BASELINE_GUARD=1` runs at identical tallies. Composite lock stands authoritative at 52.52%. This report is the wave-close package for owner ratification.

---

## 1 · Wave ledger (this session)

| Wave / Scope | Anchor commit | Passed floor | Baseline failures | Quarantined | Ratification |
|---|---|---:|---:|---:|---|
| Wave F · Scope A · D1a-1 residue retirement | Extraction-Akki `programme/track-a` **`1155629`** | 2333 | 0 | 0 | Ratified by owner 2026-08-27T20:57Z |
| Wave F · Scope B · Authoritative composite lock | Master workspace **`7ae5dcb`** | (workspace tool commit; test-mirror pending on rounding fix — see §4) | — | — | Ratified by owner 2026-08-27T21:12Z |
| Wave F · Scope C · Compliance residue class-attribution | Master workspace **`aab67c4`** | (no `programme/track-a` code touched) | — | — | Ratified by owner 2026-08-27T21:20Z |
| Wave F · Cleanup · Full-system drill day | Extraction-Akki **`67a6786`** + Master **`8e8fd06`** | **2333** | **0** | **0** | **PENDING · this report** |

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

---

## 3 · Composite lock reconciliation

**Authoritative locked composite: 52.52%.**

| Dimension | Raw (unrounded) | Rounded published | Weight |
|---|---:|---:|---:|
| Mechanism corpus (551 rows) | 54.4827586% | 54.48% | 0.7 |
| Interface dimension (58 v7 surfaces) | 47.9310345% | 47.93% | 0.3 |
| **Composite (single-final-rounded from raw)** | **52.51724%** | **52.52%** | — |

**Rounding rule (explicit · state once in this report per owner addition):**

> Composite is computed from the UNROUNDED dimension percentages and rounded ONCE at the end; recomputing from the rounded published values (54.48, 47.93) yields 52.51 by double-rounding — that figure is an artifact of the published-dashboard precision, not a lock candidate. The authoritative locked value stands at 52.52.

**Method:** `tools/w10_cp9_composite_recompute.py` · deterministic · 36 delta entries · every delta anchored to a canon § + `programme/track-a` commit SHA.

**Locked by pytest (permanent guard):** `backend/tests/invariants/test_w10_cp9_composite_lock.py` · 5/5 green in the full-suite double-run.

**Wave F Scope C composite-recompute deltas (recommended for the next register revision · NOT applied in this Wave F close since owner did not authorize a register rewrite in Scope C):**

- CA1-N1 (retention enforcement + attestation): **PARTIAL → DONE** — charter annotation was STALE; the enforcement + attestation module (`services/retention/`, 613 tracked LOC + `test_retention_enforcement_w6_cp3.py` 328 LOC gating) landed at W6 CP3 pre-dating the Wave A-C anchor freeze.
- CA1-N4 (residency governed-region allowlist): **PARTIAL → DONE** — same class of stale annotation; the enforcement module (`services/chokepoint/residency.py` + `residency_allowlist.v0.json`) landed at W6 CP3.

These deltas would nudge mechanism % upward slightly. NOT applied here — the composite is banked at 52.52 per the Scope B ratified ceremony; owner authorizes the register rewrite as a separate act if desired.

---

## 4 · Full-system drill day receipts (banked)

Location: `/app/assessment_workspace/phase0/drill_receipts/`

- **Run 1:** `20260827T213255Z_wave_f_cleanup_drill_day_run1.log`
  - Receipt: `passed=2333 / baseline-failures-remaining=0 / quarantined=0`
  - Wall-clock: 89.16s
  - Skipped: 1 (single documented skip — unchanged across the suite)
- **Run 2:** `20260827T213435Z_wave_f_cleanup_drill_day_run2.log`
  - Receipt: `passed=2333 / baseline-failures-remaining=0 / quarantined=0`
  - Wall-clock: 89.43s
  - Skipped: 1 (identical)

**Identity check:** both runs produced the byte-identical BASELINE_GUARD receipt line `passed=2333 / baseline-failures-remaining=0 / quarantined=0`. No tally absorption. Permanent Close Standard satisfied.

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

### 6.6 CA1-001 / CA1-002 / CA1-003 · Audit-trail Overview surface (BUILD)

- **Status:** carried as BUILD (CA1-001, CA1-002) and PARTIAL (CA1-003) — no `services/audit_trail/` module authorized to build in Wave F.
- **Landing site (once authorized):** new `services/audit_trail/` mechanism-surface. Named blockers preserved in `notes/waveF_scope_c_close_report.md` items 1/2/3.

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
- `notes/programme_close_report.md` · **this report** · Wave F wave-close package.
- `phase0/drill_receipts/20260827T213255Z_wave_f_cleanup_drill_day_run1.log` · full-system drill run 1.
- `phase0/drill_receipts/20260827T213435Z_wave_f_cleanup_drill_day_run2.log` · full-system drill run 2 (identical).
- `phase0/drill_receipts/20260827T211213Z_wave_f_composite_lock.log` · Scope B ceremony (banked earlier this session).
- `phase0/drill_receipts/orphaned/20260826T110626Z_w11b_close_full_invariants_green.log` · isolated misnamed log.

---

## 10 · Handoff to owner's external third run

Per owner rule ("MY external third run at the WAVE close"), the third ratification run is the owner's act. This report is the wave-close package awaiting that run.

**Suggested owner probe recipe (unchanged from prior wave closes):**

```
cd /app/assessment_workspace/repos/Extraction-Akki/backend && \
  BASELINE_GUARD=1 python -m pytest tests/invariants/ 2>&1 | tail -20
```

Expected receipt line: `passed=2333 / baseline-failures-remaining=0 / quarantined=0`.

**Post-ratification state expected:** Wave F CLOSED + RATIFIED across all three scopes + Cleanup. Next scope opens on owner GO (SSH key drop if that path fires, or Wave G scope ratification, whichever arrives first).

---

## 11 · Non-halting posture continues

SSH key interrupt remains INTERRUPT-PRIORITY (see §6.1). No other pending items block wave close. Ratchet held at 2333/0/0. Composite locked at 52.52%. Autonomous progression completed per owner Wave F GO ruling.

**Wave F CLOSED PENDING OWNER'S EXTERNAL THIRD-RUN RATIFICATION.**
