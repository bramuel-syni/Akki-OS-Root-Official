READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-HYGIENE-HF-TOKEN-GUARD · wave grounding brief

**Class:** hygiene / hardening invariant (NOT M5 milestone content).
**Author:** main agent · 2026-09-14T~13:15Z.
**Prior state:** Step 0 (HF-token ledger update) closed at master `7b858f27`. Ratchet unchanged 3851/3851.
**This wave:** first ratchet-bearing wave of the M5 session. Own RED, own mechanism, own double-green, own seal, own two-commit.

---

## §A. Verbatim owner authorization

**Rulings this session (2026-09-14), banked in `STATE/DECISIONS.md` (dated ruling entry) — quoted verbatim here for wave-gating:**

1. Secret-hygiene rule (verbatim):
   > "env-var injection only — same for ALL secrets from now on: env/askpass, never printed, never on a command line visible to ps."

2. Secret-leak guard as its own hardening wave (verbatim):
   > "SECRET-LEAK GUARD — authorized as a HARDENING INVARIANT (justified: 5+ recurrences incl. SEC-2026-09-14-01/02/03). Land it TESTS-FIRST as its own small hardening wave BEFORE the Audio-POC live reads (so it protects them). §A cites `notes/SEC_INCIDENTS_20260914.md` + the owner-endorsed hard-lock posture + this standing orchestrator directive — label it clearly as hygiene/hardening, not milestone content. Repurpose the untracked `test_wm5_sw1_hf_token_rotation.py` into THIS guard test (bank a real RED) or discard it — no phantom RED."

3. HF-token drop framing (verbatim, provides SHA-pinned identity of the active token):
   > "these are file labels but no confidential information. We have full rights on this data."

**Incident chain being guarded against** (SEC_INCIDENTS_20260914.md, banked at same-day):

* `SEC-2026-09-14-01/02/03` — three same-day XLSX-inspector transcript leaks (NAS · JUMP · RADIO). Same class of failure: pre-inspection print without a content-shape guard.
* `SEC-2026-09-14-04` — same-day `head -1` transcript leak of the ROTATED HF-token replacement itself. Same class again.
* `SEC-2026-09-13-T4-03/04/05` — prior-session same-class leaks.
* `SEC-2026-09-12-01` — original leak that motivated the rotation now being guarded.

**Justification for a runtime invariant** (rather than "just don't print"): the leak class has recurred 5+ times across three sessions despite standing "never echo" discipline. Discipline is not enforced by a runtime invariant; therefore the guard becomes a first-class check that callers MUST invoke before emitting any log/receipt/print that MIGHT contain user-supplied text.

---

## §B. Canon anchors

* **STANDING_ORDERS §4 (Runtime Law) PII / credential custody bullet** (verbatim on disk):
  > "AWS RDS Data API credentials: `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json` (mode 0600). GPU host SSH private key: `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu` (mode 0600). Host IPs and usernames: `/app/backend/.env` … Never committed. Never returned in responses. Never logged. Never in test docstrings. Redacted everywhere."

  Interpretation: the same policy binds any HF-token custody artefact under `estate_keys/data_sources/`. The guard mechanism this wave lands enforces the "never logged, never in test docstrings, redacted everywhere" clause as a runtime invariant when callers use the loader.

* **STANDING_ORDERS §3.1 (ALIVE-IS-NOT-DONE)** — informs the seal-read discipline for this wave's own close. Seal at `notes/W_HYGIENE_HF_TOKEN_GUARD_close.md` will emit its `Kind:` line via `output_verified_seal` if that primitive is present on-tree; otherwise the seal file is authored with a plain `Kind: hygiene_hardening_wave_close` line so future scans read it as a real seal.

* **Canon 8 (The Watch)** — general hygiene / hardening posture. Not cited verbatim; loose anchor only.

**Wave scope explicitly does NOT cite** any M5 milestone canon (DAP · SIA · Governance · WPW) because owner directive labels this wave "hygiene/hardening, not milestone content."

---

## §C. Mechanism scope

**Test file** (repurposed from the untracked `test_wm5_sw1_hf_token_rotation.py`):
`backend/tests/invariants/test_secret_hygiene_hf_token_guard.py` — 7 invariants (same 7 that the untracked file already carries; only the file docstring and module name change from `W-M5-SW1` framing to hygiene-wave framing).

**Mechanism modules** (new, minimal scope):

* `backend/services/secret_hygiene/__init__.py` — package marker.
* `backend/services/secret_hygiene/hf_token.py` — the guard mechanism. Exports:
  - `HF_TOKEN_ROTATION_RULING_VERBATIM` (str) — owner secret-hygiene rule quoted §A.1
  - `HF_TOKEN_ACTIVE_ARTEFACT` (str) — `/app/backend/estate_keys/data_sources/hf_token_rotated_20260914.csv`
  - `HF_TOKEN_ACTIVE_SHA256` (str) — `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`
  - `HF_TOKEN_PRE_ROTATION_ARTEFACT` (str) — `/app/backend/estate_keys/data_sources/hf_token.csv`
  - `SEC_ROTATION_LEDGER` (tuple[dict]) — records for `SEC-2026-09-12-01` (OWNER-ROTATED-PENDING-CONFIRMATION) and `SEC-2026-09-14-04` (PENDING-SECOND-ROTATION)
  - `HFTokenNotRotatedError` (Exception subclass) — declared for stale-loader refusal contract
  - `HFTokenEnvVarMissing` (Exception subclass) — raised by `load_hf_token_or_raise` when both env vars are unset
  - `load_hf_token_or_raise()` — reads `HF_TOKEN` else `HUGGING_FACE_HUB_TOKEN`; raises `HFTokenEnvVarMissing` if both absent. Does NOT fall back to reading the on-disk artefact into a string. Return value not printed by any code path in this module.
  - `assert_no_transcript_leak_of_active_token(text: str)` — reads the active-artefact file (mode 0600, custody root) ONCE into a module-level cache; if the active token value is a substring of `text`, raises `RuntimeError` with a message that does NOT include the value. Callers invoke this before emitting any `print`/`log.info`/`receipt.write`.

**Wave-scope hard limits** (what this wave does NOT do):

* Does NOT extend the guard to generic secrets (`HFTokenGuard` is HF-token-specific; a generalisation to a full SecretRegistry is a follow-on wave).
* Does NOT wire `HFTokenNotRotatedError` into any caller (declared as a fabric element only; runtime wiring is Step 2 or later when a HF-loading caller exists to wire against).
* Does NOT change any existing consumer of the pre-rotation `hf_token.csv` (there are none in the tree; grep-search confirms).
* Does NOT touch any existing test file.

---

## §D. Definition of Done

1. Grounding brief authored + banked at `notes/wave_secret_hygiene_hf_token_guard_grounding_brief.md` (this file). — DONE at authoring time.
2. Test file present in tree at `backend/tests/invariants/test_secret_hygiene_hf_token_guard.py`. Untracked precursor `test_wm5_sw1_hf_token_rotation.py` renamed (or removed) so ONE test file for this wave exists.
3. Mechanical RED banked at `phase0/drill_receipts/YYYYMMDDThhmmssZ_wave_secret_hygiene_hf_token_guard_RED_pre_impl.log`. Right-reason: `ModuleNotFoundError` on `services.secret_hygiene.hf_token` from the fabric test + downstream test failures.
4. Mechanism landed: `backend/services/secret_hygiene/__init__.py` + `backend/services/secret_hygiene/hf_token.py`. All 9 exported names present. No file-read side effects at import time.
5. Under `BASELINE_GUARD=1 python -m pytest tests/invariants/` (run from `backend/`), two consecutive runs return byte-identical pass/skip/warning tallies. Both receipts banked.
6. `baseline_failures.json` bumped: `counts_at_baseline.passed` and `passed_floor` monotonically-up by exactly N where N = number of tests contributed by `test_secret_hygiene_hf_token_guard.py`. `ratchet_history` appended with `wave: W-HYGIENE-HF-TOKEN-GUARD`, `from`, `to`, `commit: <track-a HEAD>`, `receipt: <double-green-2>`, `recorded_at_utc`.
7. Seal banked at `notes/W_HYGIENE_HF_TOKEN_GUARD_close.md` with a `Kind: hygiene_hardening_wave_close` line so it reads as a real seal under §3.1's contract.
8. Rider 1 receipt: `pip freeze` capture + `pytest --collect-only -q | wc -l` capture, both banked as attachments to the seal (per standing rider protocol).
9. Two local commits, in order:
   - **Commit A (code, repo `repos/Extraction-Akki/`, branch `programme/track-a`):** test file + `services/secret_hygiene/*.py` + `baseline_failures.json` ratchet bump. Commit message follows the wave-close convention. No push.
   - **Commit B (state, workspace `/app/assessment_workspace/`, branch `master`):** grounding brief + seal + drill receipts + rider attachments + DECISIONS.md addendum + NEXT.md current-step marker refresh. No push.

---

## §E. Wave-honest limits (candidates for follow-on)

* **E.1** Guard applies to HF token only. If a future leak class involves a different secret (JUMP / NAS / RADIO / DB / RMS creds), a generalised registry-based guard is needed. Not in this wave's scope.
* **E.2** `HFTokenNotRotatedError` is declared but not wired to any file-path-refusing loader function. A follow-on wave can add `refuse_pre_rotation_path(...)` behaviour and wire it into upstream callers if any land.
* **E.3** `assert_no_transcript_leak_of_active_token` reads the file into a module-level cache on first call. If the cached value is later garbage-collected + reloaded, there is a small window where a concurrent print could race. Wave-honest: race is acceptable at Step 1 because there is no concurrent-print caller in the tree yet. Follow-on if concurrent audio-plane transcription lands.
* **E.4** The guard checks substring membership. If a caller passes a modified/encoded copy of the token (e.g. base64-encoded, URL-encoded), the guard does NOT catch it. Wave-honest: no known caller encodes token values; encoded-form guard is a follow-on if one appears.
* **E.5** The guard does NOT enforce that env-var-loaded token values are also NOT-in-text. Wave-honest: `load_hf_token_or_raise` reads from env; if the env-var-provided token differs from the SHA-pinned artefact, that is an owner-side responsibility (token rotation should update the artefact + SHA pin in tandem). A future wave can add identity-check between env and file.

---

## §F. Commit protocol (per SO §3, per this wave's DoD.9)

* **Commit A** on `programme/track-a` in `repos/Extraction-Akki/`:
  - `backend/tests/invariants/test_secret_hygiene_hf_token_guard.py` — new (repurposed).
  - `backend/services/secret_hygiene/__init__.py` — new.
  - `backend/services/secret_hygiene/hf_token.py` — new.
  - `backend/tests/invariants/baseline_failures.json` — ratchet bump + `ratchet_history` append.
  - Commit message convention: `W-HYGIENE-HF-TOKEN-GUARD · secret-leak guard hardening · services/secret_hygiene/hf_token.py · assert_no_transcript_leak_of_active_token + load_hf_token_or_raise + SEC_ROTATION_LEDGER · SEC-2026-09-14-01/02/03/04 same-class recurrence guard · ratchet 3851 → 3851+N (+N)`.
  - **NO PUSH.**

* **Commit B** on `master` in `/app/assessment_workspace/`:
  - `notes/wave_secret_hygiene_hf_token_guard_grounding_brief.md` — new (this file).
  - `notes/W_HYGIENE_HF_TOKEN_GUARD_close.md` — new (seal).
  - `phase0/drill_receipts/*_wave_secret_hygiene_hf_token_guard_RED_pre_impl.log` — RED receipt.
  - `phase0/drill_receipts/*_wave_secret_hygiene_hf_token_guard_wave_close_double_green*.log` — 2 GREEN receipts.
  - `STATE/DECISIONS.md` — wave-close ruling appended.
  - `STATE/NEXT.md` — current-step marker refreshed for Step 2 (M5 SW1 = W-DATA-SUITE-V2-LIFT).
  - Commit message convention: `state: W-HYGIENE-HF-TOKEN-GUARD close · secret-leak guard hardening wave · ratchet 3851 → 3851+N (+N) · programme/track-a <SHA> · seal notes/W_HYGIENE_HF_TOKEN_GUARD_close.md`.
  - **NO PUSH.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
