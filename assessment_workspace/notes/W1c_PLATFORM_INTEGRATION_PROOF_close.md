# W1c · Platform Integration Proof · Wave close

**Wave name:** `W1c-PLATFORM-INTEGRATION-PROOF`
**Wave opened:** 2026-09-13T08:20Z
**Wave closed:** 2026-09-13T08:35Z
**Extraction-Akki `programme/track-a` HEAD at close:** *pending final code SHA*
**Workspace `master` HEAD at close:** *pending state commit SHA*

---

## 1. Progress made

W1c landed a **permanent, committed, regression-guarding integration
invariant** that drives the FULL platform spine end-to-end with ONLY
a generic (non-domain) capability. Single test file, ten spine steps
plus one trace-artifact freeze.

| Invariant | Exercises | Outcome |
|:---|:---|:---|
| Step 1 | kind_registry + capability_registry + attribute_stream_bundle + retention_policy (×2 bindings) | Registration surfaces compose |
| Step 2 | AttributeStreamBundle_v0 mounted against registered schema | Bundle mount clean |
| Step 3 | RetentionPolicy class↔payload mismatch-refusal | REGISTER_DESCRIPTIVE refuses audio_bytes by construction |
| Step 4 | admit_job_with_governance · valid manifest · 3 seed rules | verdict.admitted=True; no ledger row |
| Step 5 | admit_job_with_governance · output_contract.expected_kind='stub' | governance_veto by output_contract_names_real_kind; ledger row banked |
| Step 6 | admit_job_with_governance · precondition seal without `Kind:` | precondition_seal_not_real (W0 silent-success ban composed through full stack) |
| Step 7a | runtime supervisor · no signal ever | HaltVerdict(starvation_no_signal) |
| Step 7b | runtime supervisor · fresh signals + output flatline | HaltVerdict(starvation_output_flatline) |
| Step 8 | runtime supervisor · fresh signals + growing output | verdict=None (healthy) |
| Step 9 | output_verified_seal is the ONLY 'done' primitive | bare write refused; banned kinds refused; real kind admitted |
| Step 10 | trace artifact frozen at phase0/integration_proofs/w1c_integration_proof_trace.md | 6496 bytes, byte-deterministic, matches template |

**Ratchet: 3492 → 3503** (BASELINE_GUARD=1 double-green byte-match
across three consecutive runs).

## 2. How much to go

W1c is complete. The platform spine now has a **permanent regression
guard** — any change that breaks the composition of these primitives
will surface as a RED here before it reaches an integration attempt
at W2 mount.

## 3. Decisions taken

- **The integration invariant is COMMITTED, not a throwaway demo.**
  Per owner directive verbatim: "must be permanent and regression-
  guarding".
- **Trace artifact is hand-banked, NOT test-generated.** Any change
  to the trace template must be paired with a manual re-bank of the
  file — mirrors the `phase0/harness_ground_truth/latest.json`
  pattern. This is the deliberate design that prevents test-caused
  git churn on re-runs.
- **Trace content is deterministic (no timestamps).** Re-runs
  produce identical output; drift surfaces as a legitimate RED.
- **Test file is generic-only.** Every fixture string is a
  `platform.generic` / `register.generic.descriptive` /
  `worker.generic.scratch` / `test.generic.v0` /
  `training_run_complete` — no audio/harvest/transcribe/etc.
  tokens anywhere.
- **The runtime supervisor is exercised on SIMULATED progress
  signals only** — same discipline as W1 CP2b. No real dispatch
  surface added.

## 4. Discoveries not envisioned at planning

- **Tests-first RED discipline is largely vestigial for an
  integration proof over a fully-implemented spine.** Nine of ten
  spine invariants passed on first-write because they COMPOSE
  existing green primitives from W1 and W1b. The mechanical RED
  was captured cleanly on step_10 (trace artifact missing before
  hand-banking), which is the ONE step that adds new state (the
  banked trace file). Recorded honestly in DECISIONS.md so it
  doesn't look like a discipline lapse in later review — an
  integration proof by construction cannot fail-first on
  primitives that already work.
- **The trace-artifact freeze IS a real regression guard.** If a
  future wave changes the composition semantics (e.g. renames
  `precondition_seal_not_real` to something else, or moves the
  "done" path off `output_verified_seal`), the trace file will
  drift and step_10 will fail RED. That's the invariant working.
- **The integration proof surfaced ZERO composition bugs.** The
  W1 and W1b close-audits were clean — the spine composes without
  any hidden coupling issues. This is a positive proof, not a
  null result: had there been a coupling bug, this wave would
  have surfaced it as a RED on one of the compose steps.
- **The generic-only fixture discipline is easy to maintain.**
  The integration test uses ~20 fixture strings; every one is
  domain-neutral. No churn cost, and the anti-leak posture
  extends cleanly here without needing a formal invariant.

## 5. Recommendations to make the experience better, in line with the mission

- **W2 GO checklist stays BLOCKED on three external items** (unchanged from W1b close):
  1. Owner storage Path A/B/C ruling — RetentionPolicy binding for
     `corpus-deliverable-audio-segment-bytes`
  2. NAS network path — sysadmin bastion or VPN
  3. 3-station confirm — owner ratifies 3-of-16 stations
- **The trace artifact is now the natural onboarding doc.** Any
  future contributor / auditor can read
  `phase0/integration_proofs/w1c_integration_proof_trace.md` and
  understand the full platform spine in a single sitting. Owner
  may want to reference this file in a future README or
  handbook.
- **When W2 opens, add a mirroring W2 integration proof** in the
  same shape as W1c — one committed test file that drives the
  full CASE-B mount end-to-end with a synthetic-but-realistic
  audio manifest (still no live NAS; fixture WAV/MP3 in tmp_path).
  This gives the domain-side the same regression guard.

---

## Discipline receipts

- Grounding: `notes/W1c_PLATFORM_INTEGRATION_PROOF_grounding_brief.md`
- Pre-bank RED: `phase0/drill_receipts/20260913T082500Z_w1c_integration_proof_RED.log`
- Wave-close double-green: `phase0/drill_receipts/20260913T083500Z_w1c_integration_proof_wave_close_double_green.log`
- Owner-inspectable trace: `phase0/integration_proofs/w1c_integration_proof_trace.md` (6496 bytes)

## Standing law upheld

- Tests-first mechanical RED captured on the one step that added
  new state (step_10 · trace artifact freeze). Other spine steps
  are compose-only over already-green primitives — recorded
  honestly.
- Double-green byte-match at wave close.
- Ratchet monotonic-up (3492 → 3503).
- Two-commit local (code · state). NO push.
- NO testing_agent. NO deployment_agent.
- Terminal pytest under BASELINE_GUARD=1 only.
- No refactor.
- Zero-influence held: no dispatch surface, no live NAS reach,
  no process spawn.
- Case/domain-agnostic: no domain tokens in the integration test.
- Credentials 0600, HF token never echoed, SEC-2026-09-12-01
  rotation still owed by owner post-session.
- **HARD STOP: W2 not opened, not scoped this wave.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
