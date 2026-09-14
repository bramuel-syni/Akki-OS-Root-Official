READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

Kind: hygiene_hardening_wave_close

# W-HYGIENE-HF-TOKEN-GUARD · wave close seal

**Wave class:** hygiene / hardening invariant (NOT M5 milestone content).
**Closed:** 2026-09-14T~12:50Z.
**Ratchet:** 3851 → 3858 (+7 invariants).
**Manifest:** unchanged at 0 (`baseline_failures` empty).
**Skipped:** unchanged at 1 (legacy conditional).
**Quarantine:** unchanged at 0.
**Track-a HEAD (pre-commit):** `d6bf1bc`; new commit lands as head after Commit A of this wave.
**Master HEAD (pre-commit):** `7b858f27` (Step 0 · HF-token ledger update, state-only).

---

## 1. Owner authorization (verbatim, this session 2026-09-14)

* Secret-hygiene rule:
  > "env-var injection only — same for ALL secrets from now on: env/askpass, never printed, never on a command line visible to ps."

* Wave authorization:
  > "SECRET-LEAK GUARD — authorized as a HARDENING INVARIANT (justified: 5+ recurrences incl. SEC-2026-09-14-01/02/03). Land it TESTS-FIRST as its own small hardening wave BEFORE the Audio-POC live reads (so it protects them). §A cites `notes/SEC_INCIDENTS_20260914.md` + the owner-endorsed hard-lock posture + this standing orchestrator directive — label it clearly as hygiene/hardening, not milestone content. Repurpose the untracked `test_wm5_sw1_hf_token_rotation.py` into THIS guard test (bank a real RED) or discard it — no phantom RED."

* M5 SW1 scope correction:
  > "CORRECTION — M5 SW1 IS NOT 'HF-token rotation / secret guards.' Reject option (c)'s scope. M5's milestone content per the ratified spine is: W-DATA-SUITE-V2-LIFT then W-AUDIO-POC."

Full rulings banked verbatim in `STATE/DECISIONS.md` under the 2026-09-14T~13:00Z ruling entry.

---

## 2. What the wave landed

**Test file** (repurposed from an untracked draft; the phantom "M5-SW1" framing was rejected):

* `backend/tests/invariants/test_secret_hygiene_hf_token_guard.py` — 7 invariants:
  1. `test_sw1_module_fabric` — 9 required names exist on the module.
  2. `test_sw1_rotation_ruling_verbatim` — owner rule quoted verbatim in module constant.
  3. `test_sw1_active_artefact_pinned_by_sha256` — SHA256 pin matches manifest.
  4. `test_sw1_pre_rotation_artefact_still_recorded` — pre-rotation path on record.
  5. `test_sw1_sec_rotation_ledger_records_all_hf_items` — both HF SEC items in ledger with correct states.
  6. `test_sw1_env_var_missing_raises_not_reads_file` — env-only loader refuses when unset (no file fallback).
  7. `test_sw1_transcript_leak_guard_against_active_token_value` — `assert_no_transcript_leak_of_active_token(...)` raises `RuntimeError` on match; passes for safe strings.

  (Test function names retain `test_sw1_` prefix for minimal-change repurpose; wave-class labelling is on the module docstring per owner "repurpose, not rewrite" directive.)

**Mechanism modules** (new, minimal scope):

* `backend/services/secret_hygiene/__init__.py` — package marker.
* `backend/services/secret_hygiene/hf_token.py` — the guard mechanism, 141 lines. Exports the 9 fabric names required by the test. Never prints the token value. Module cache reads the custody artefact once and holds it in a module-private variable; not surfaced through any accessor.

**Ratchet manifest bump** (`backend/tests/invariants/baseline_failures.json`):

* `counts_at_baseline.passed`: 3851 → 3858 (+7).
* `invariants_enforced_when_baseline_guard_1.passed_floor`: 3851 → 3858 (+7).
* `ratchet_history` appended: entry `at_utc: 20260914T124119Z`, `wave: W-HYGIENE-HF-TOKEN-GUARD`, `sub_wave: SECRET_LEAK_GUARD_HARDENING`, `passed: 3858`, `invariants_added: 7`, `commit: TBD` (backfill in follow-on state commit per convention).

---

## 3. Discipline receipts

* **Grounding brief** (§A verbatim owner quote in-file):
  `notes/wave_secret_hygiene_hf_token_guard_grounding_brief.md`.

* **Mechanical RED** (pre-implementation tree, right-reason):
  `phase0/drill_receipts/20260914T124119Z_wave_secret_hygiene_hf_token_guard_RED_pre_impl.log`.
  7 failed / 0 passed. All 7 failures traceable to `ModuleNotFoundError: No module named 'services.secret_hygiene'` (right-reason: module did not exist pre-impl).

* **Double-green byte-match** (BASELINE_GUARD=1 python -m pytest tests/invariants/):
  * Run 1: `phase0/drill_receipts/20260914T124604Z_wave_secret_hygiene_hf_token_guard_wave_close_double_green_run1.log` — `3858 passed, 1 skipped, 438 warnings in 113.71s` (41047 bytes).
  * Run 2: `phase0/drill_receipts/20260914T124805Z_wave_secret_hygiene_hf_token_guard_wave_close_double_green_run2.log` — `3858 passed, 1 skipped, 438 warnings in 114.76s` (41047 bytes).
  * Tally byte-identity confirmed on `pass/skip/warning` count.

* **Rider 1** (pip freeze + pytest --collect-only -q):
  * `phase0/drill_receipts/20260914T125022Z_wave_secret_hygiene_hf_token_guard_rider1_pip_freeze.log` — 192 lines.
  * `phase0/drill_receipts/20260914T125022Z_wave_secret_hygiene_hf_token_guard_rider1_pytest_collect.log` — 3861 lines / 3859 tests collected.

---

## 4. Guardrails held

* NO push. Two local commits only.
* NO `testing_agent`. Terminal pytest only.
* NO refactor. Only files touched: 2 new mechanism files + 1 renamed test file + 1 ratchet-manifest bump = 4 code paths.
* NO scaffolding of a new FastAPI/React app. No touch to `/app/backend` or `/app/frontend` runtime pods.
* NO wipe of `/app/assessment_workspace/`. No re-clone.
* NO custody-root inspection via `head`/`cat`/`sed`. Inspections used `stat -c` and `wc -c` only. Manifest SHA256 was lifted from the drop's paired manifest (banked at drop time), NOT re-hashed by inspecting the value.
* Token value NEVER echoed to transcript at any point in this wave. Diff scan of the staged code delta confirms no token-value leak.
* EAT window compliant: this wave performed NO egress (no HF-model pull, no external network).

---

## 5. Wave-honest limits (candidates for follow-on)

Same as banked in the grounding brief §E:

* **E.1** Guard is HF-token-specific. Generalisation to a full secret registry is a follow-on wave.
* **E.2** `HFTokenNotRotatedError` declared but not wired to a file-path-refusing loader. Follow-on wave can wire it when a real HF-loading caller lands.
* **E.3** Module cache is populated on first call; a concurrent-print race window exists but has no caller today.
* **E.4** Guard checks substring membership only; encoded copies (base64/URL) not caught.
* **E.5** No identity-check between env-var-provided token and file-pinned token.

---

## 6. Next active step

**Step 2 · M5 SW1 = W-DATA-SUITE-V2-LIFT** (per owner directive 2026-09-14):

* §A citation = owner M5 open quote + `notes/MILESTONE_PROMISE_BINDING_20260913.md §M5` + Phase-C plan §M5/§lift + Data-Suite donor path in Executive donor repos.
* Case-agnostic donor lift, same discipline as W-SOLVA-V2-LIFT.
* Do NOT invent scope; do NOT ask owner to re-paste the contract that is already banked (option-b path).
* Discipline: mechanical RED → mechanism → double-green byte-match → ratchet monotonic from **3858** → seal → two local commits.

Interim DECISION-POINT per sub-wave close (per owner comms doctrine).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
