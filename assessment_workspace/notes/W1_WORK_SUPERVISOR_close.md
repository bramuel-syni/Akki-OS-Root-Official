# W1 · Work-Supervisor · Wave close

**Wave name:** `W1-WORK-SUPERVISOR`
**Wave opened:** 2026-09-13T06:10Z (immediately after CP0.a + W0 close)
**Wave closed:** 2026-09-13T07:10Z
**Extraction-Akki `programme/track-a` HEAD at close:** *pending final code SHA · this doc lives at workspace master*
**Workspace `master` HEAD at close:** *pending state commit SHA*

---

## 1. Progress made

W1 landed the case-agnostic **Work-Supervisor kernel** on top of W0's
integrity primitive. Five CPs delivered in strict tests-first order:

| CP | Scope | New invariants |
|:---|:---|---:|
| CP1 | Registry-backed JobManifest v0 (kind_registry + job_manifest) | +41 |
| CP2 | Admission supervisor (admit_job / plan_next / AdmissionVerdict / Plan / SupervisorRefusal) | +19 |
| CP2b | Runtime supervisor (progress ring + output_verification_watchdog + HaltVerdict) + STANDING ORDER §3.2 verbatim | +16 |
| CP3 | Governance primitives (Verdict + GovernanceRule ABC + apply_rules + bank_verdict + 3 seeded rules) | +23 |
| CP4 | Supervisor + Governance compose freeze (`admit_job_with_governance`) | +11 |
| **W1 total** |  | **+110** |

Ratchet: **3282 → 3392** (monotonic-up · double-green byte-match).

The admission supervisor composes over W0's `is_real_seal` so the
silent-success ban is inherited by construction. The runtime supervisor
enforces STANDING ORDER §3.2 "NO RUN WITHOUT A PROGRESS SIGNAL" by
returning a `HaltVerdict` (data — never a signal) on
starvation_no_signal / starvation_stale_signal / starvation_output_flatline.

## 2. How much to go

The Work-Supervisor kernel is complete for W1 scope. Remaining pre-W2
platform-primitive work is deferred (with owner acknowledgement) to a
follow-on wave **W1b** — see §5 recommendations for the CP breakdown
holding.

## 3. Decisions taken

- **Job-kind stays case-agnostic** via an open registry mechanism.
  Platform seeds exactly ONE sentinel kind (`platform.generic`). No
  audio-case kinds anywhere in platform code. Downstream Part-B waves
  will call `kind_registry.register_kind()` at their mount time.
- **Runtime supervisor lands BEFORE any dispatch.** Owner-inserted
  CP2b — starvation gates test against SIMULATED run states in
  `tmp_path`. Zero real dispatch. HaltVerdict is DATA, not a signal.
- **STANDING ORDER §3.2 added** as a subsection of §3 BUILD DISCIPLINE
  (mirrors the §3.1 placement to preserve the six-header top-level
  surface frozen by `test_standing_orders_present`).
- **Fixture-correction discipline held.** No pre-W1 test was amended
  to green. The three W0 fixture updates (in CP0.a+W0) remain the
  only fixture writes touched.
- **Governance rules are pure functions of the manifest.** No I/O
  inside rule bodies. Only `bank_verdict` touches disk (best-effort
  ledger row).
- **First-veto-wins compose semantic.** `admit_job_with_governance`
  stops at the first Verdict.passed=False and does NOT apply
  subsequent rules — frozen by CP4 invariant
  `test_admit_job_with_governance_stops_at_first_veto_does_not_check_downstream`.

## 4. Discoveries not envisioned at planning

- **Ruff blocking-lint feedback caught a forward-reference gap.** The
  compose function's `rules: List["GovernanceRule"]` string annotation
  tripped F821 until I added a `TYPE_CHECKING` guard. Zero impact on
  runtime; a small quality tightening.
- **The `signal` word appears legitimately in `ProgressSignal`.** The
  existing r2 zero-influence rule bans "signal" on public surfaces to
  prevent process-signal delivery names. Refined the CP2b invariant
  to ban only `terminate`/`kill` — the data-emission concept of a
  progress signal is orthogonal to a killer signal and the wave-close
  DECISIONS entry records this narrowing.
- **`is_real_seal` composition is inherited-by-construction.** The
  admission supervisor gets the W0 silent-success ban for free —
  every W1 precondition-seal test that exercises the "bare seal
  without Kind" fixture directly proves the composition.
- **Governance ledger dedupe key is (job_id, manifest_fingerprint,
  rule_name).** This lets the same rule log distinct vetoes for
  distinct manifest revisions of the same job — useful for later
  amendment flows.

## 5. Recommendations to make the experience better, in line with the mission

- **Charter W1b next, BEFORE opening W2 job-mount.** The remaining
  case-agnostic primitives (RetentionPolicy · SourceConnector
  Protocol + FileStation impl · Capability registry generalisation ·
  L2/L4 contracts · AudioAttributeStreamBundle_v0) each have their
  own tests-first RED and independent close. Recommended CP order:
    CP1 · RetentionPolicy (four regimes + mismatch-refusal)
    CP2 · SourceConnector Protocol + read_only_guard
    CP3 · FileStation impl (interface only, no live NAS)
    CP4 · Capability registry generalisation (folds layer_b.factory
          under the same open-registry mechanism as kind_registry)
    CP5 · L2/L4 contract shells + AudioAttributeStreamBundle_v0
    CP6 · Wave close.
- **On W2 open, wire the AUDIO JobManifest instance at mount time.**
  That's where `case.b.audio.ingest`, `case.b.audio.transcribe` etc.
  get registered via `kind_registry.register_kind()`. No platform-
  side change.
- **Consider an owner-facing surface for the ledger** in a later
  wave: a plain-language "governance activity" view that reads the
  ledger rows and renders `<rule name> refused <job id> at <utc>`.
  Not W1 scope — banked as a UI concern.
- **Watchdog SLA schedule elasticity** (per-kind / per-phase) is a
  clean W2b enhancement. Current W1 scalar SLA is enough to unblock
  W2 dispatch.

---

## Discipline receipts

- Grounding brief: `notes/W1_WORK_SUPERVISOR_grounding_brief.md`
- Per-CP RED receipts:
  - `phase0/drill_receipts/20260913T061000Z_w1_cp1_manifest_registry_RED.log`
  - `phase0/drill_receipts/20260913T062000Z_w1_cp2_admission_supervisor_RED.log`
  - `phase0/drill_receipts/20260913T063500Z_w1_cp2b_runtime_supervisor_RED.log`
  - `phase0/drill_receipts/20260913T064500Z_w1_cp3_governance_RED.log`
  - `phase0/drill_receipts/20260913T065000Z_w1_cp4_compose_RED.log`
- Wave-close double-green:
  - `phase0/drill_receipts/20260913T071000Z_w1_work_supervisor_wave_close_double_green.log`

## Standing law upheld

- Tests-first mechanical RED before every code change.
- Double-green byte-match at wave close.
- Ratchet monotonic-up.
- Two-commit local (code · state). NO push.
- NO testing_agent.
- Terminal pytest under BASELINE_GUARD=1 only.
- Credentials 0600, HF token never echoed, SEC-2026-09-12-01 rotation
  still owed by owner post-session.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
