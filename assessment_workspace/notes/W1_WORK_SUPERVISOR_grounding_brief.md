# W1 · WORK-SUPERVISOR · Grounding brief

**Wave name:** `W1-WORK-SUPERVISOR`
**Wave opened:** 2026-09-13T06:10Z (immediately after CP0.a + W0 close).
**Base HEAD (Extraction-Akki `programme/track-a`):** `44795f3` (W0 close · ratchet 3282).
**Base HEAD (workspace `master`):** `ac7796a3` (W0 state).

---

## §A. Owner ruling verbatim

**Preceding turn (BUILD GO CP0.a + W0), 2026-09-13T~05:15Z:**

> "W0 (Integrity Fix): Fix the "silent success" defect by parsing `Kind:`
> in seal files at 6 code sites, introduce `output_verified_seal`, and
> add "ALIVE IS NOT DONE" standing order.
> W1 (Work-Supervisor): Build L5 supervisor primitives, governance
> primitives, and JobManifest schemas."

**Ruling banked at CP0.a + W0 close (2026-09-13T~06:07Z), verbatim:**

> W0 accepted — clean close (3251→3282), and the honest correction
> (only 1 of 4 drifts real; 3 were green on pinned HEAD; nothing
> amended that wasn't broken; standing-order placed at §3.1 to
> preserve the six-header surface) is exactly right. Good work.
>
> W1 CP breakdown APPROVED with ONE correction and ONE addition.
> Everything else in your plan stands.
>
> CORRECTION — job_kind must stay CASE-AGNOSTIC (this is the whole
> point of the platform/job split the owner insisted on):
> Do NOT lock a closed 5-value audio-harvest enum (harvest_ingest/
> transcode/transcribe/diarize/release_gate) into the platform
> JobManifest at CP1 — that leaks the audio case into generic
> platform code. Instead make job_kind reference an OPEN, registry-
> backed kind: a capability/job-kind REGISTRY that jobs register
> into. At CP1 define the registry mechanism and the manifest field
> that validates against it; register ZERO or one generic sentinel
> kind in the platform. The audio-harvest kinds get registered by
> the AUDIO JobManifest instance (Part B) at mount time, not baked
> into Part A. Platform stays reusable for text-training, image-
> taxonomy, anything.
>
> ADDITION — the RUNTIME work-supervisor must land in W1, not be
> deferred to dispatch:
> Your CP2 covers admission-time supervision (admit_job/plan_next).
> But the owner's core concern — and the whole reason this wave
> exists — is the RUNTIME silent-no-progress failure. Add a CP
> (call it CP2b or fold appropriately) for the runtime supervision
> primitives: progress_signal, output_verification_watchdog,
> starvation_alarm in services/work_supervisor/. Test them against
> SIMULATED run states (no real dispatch needed): a run whose GPU-
> util stays 0 / whose output artifact doesn't grow past its SLA →
> the watchdog must raise a starvation alarm and emit a HALT
> verdict; a run producing real growing output past its gate →
> passes. This is generic and testable without W2 dispatch, and it
> must exist BEFORE any dispatch so we never ship dispatch without
> a work-supervisor watching it. Also append the second STANDING
> ORDER verbatim: "NO RUN WITHOUT A PROGRESS SIGNAL — every
> commissioned run must emit a progress signal within its SLA or
> the supervisor raises a starvation alarm and HALTS the run."
> Bank in DECISIONS too.
>
> TRACKING — the remaining generic platform primitives are NOT
> dropped, they're a follow-on platform wave (call it W1b) that
> MUST land before W2 job-mount: RetentionPolicy (four regimes,
> mismatch-refusal by construction), SourceConnector Protocol +
> read_only_guard + Synology FileStation impl (interface, no live
> NAS call), Capability registry generalisation of layer_b.factory,
> the L2/L4 contracts (TargetOutcome_v0, StratumAcceptance,
> CommissionSpec, Milestone, WorkerLane, WorkerJD), and
> AudioAttributeStreamBundle_v0. Confirm you're holding these for
> W1b — don't let them fall off. If you think any belongs inside
> W1 instead, say so.
>
> Governance-rule seed (CP3): your three generic rules are fine
> (licence_class_required, dispatch_intent_configured,
> output_contract_names_real_kind) — keep them generic, no audio
> specifics.
>
> Proceed W1: CP1 (generic registry-backed JobManifest) → CP2
> (admission supervisor) → CP2b (runtime supervisor + 2nd standing
> order) → CP3 (governance) → CP4 (compose freeze) → CP5 (wave
> close). Tests-first RED each, double-green byte-match, ratchet
> bump in tandem from 3282, two-commit local, NO push, NO
> testing_agent, credentials 0600. Keep intra-CP chatter inside
> the sprint plan; report to me at the W1 double-green close. Go.

---

## §B. What we are building (one-paragraph mission synthesis)

W1 lands the case-agnostic **Work-Supervisor kernel** on top of W0's
integrity primitive. Two supervision surfaces: (i) **admission-time**
(supervisor accepts a JobManifest, checks governance vetoes, checks
`is_real_seal` preconditions, and either admits with a plan or refuses
with a named reason), and (ii) **runtime** (watchdog checks progress
signals and output-artifact growth against an SLA; on flatline it
raises a starvation alarm and emits a HALT verdict — no dispatch is
performed by W1 itself, watchdog reads simulated run state in tests).
JobManifest carries a `job_kind` field validated against an OPEN
kind-registry (platform seeds ONE sentinel kind for testing;
downstream Part-B waves register their own kinds at mount time — no
audio strings in platform code). Governance is a rule-list applied in
order, first-veto wins, ledger row banked per verdict.

---

## §C. CP breakdown (approved · with case-agnostic correction + runtime supervisor)

- **CP1 · Registry-backed JobManifest v0.**
  New `services/work_supervisor/kind_registry.py` (open registry:
  `register_kind`, `is_registered`, `list_kinds`, `KindNotRegistered`).
  New `services/work_supervisor/job_manifest.py` (pydantic v2
  `JobManifest` + `JobManifestInvalid`; `job_kind` validated against
  the registry). Platform-side seed: ONE sentinel kind
  `"platform.generic"` (used only by W1's own tests). Audio Part-B
  kinds land at their own wave — NOT this one.
  Fields (frozen v0): `manifest_version=0`, `job_id`,
  `job_kind`, `submitter`, `submitted_at_utc`, `scope` (dict),
  `output_contract` (dict), `depends_on` (list of job_ids),
  `dispatch_intent` (`local` / `ssh_host_slug:<slug>` /
  `gpu_lane:<lane_id>`), `precondition_seals`
  (list of `{run_dir, expected_kind}`).
  ~14 invariants.

- **CP2 · Admission supervisor.**
  New `services/work_supervisor/supervisor.py` exports `admit_job(m)`,
  `plan_next(job_id)`, `SupervisorRefusal` (with kinds:
  `precondition_seal_missing`, `precondition_seal_not_real`,
  `depends_on_unresolved`, `dispatch_intent_not_configured`,
  `governance_veto`, `job_kind_not_registered`). No side effects.
  Composes over `services.output_verified_seal.is_real_seal` for
  precondition checks (inherits W0's silent-success ban by
  construction).
  ~10 invariants.

- **CP2b · Runtime supervisor + 2nd STANDING ORDER.**
  New `services/work_supervisor/runtime_supervisor.py` exports
  `ProgressSignal` (dataclass: at_utc, job_id, magnitude,
  output_bytes, output_path), `record_progress(sig)`,
  `output_verification_watchdog(job_id, sla)`, `starvation_alarm`,
  `HaltVerdict`. Watchdog reads recorded progress signals from a
  local ring (`AKKI_PROGRESS_RING` env; test-controllable), computes
  the age of the newest signal, and checks output-bytes growth
  monotonicity across a window. Flatline past SLA → starvation
  alarm → `HaltVerdict(reason="starvation")`. Tests use SIMULATED
  progress signals (no real dispatch).
  Append STANDING ORDER §3.2 verbatim to `STATE/STANDING_ORDERS.md`
  under §3 BUILD DISCIPLINE:
    "NO RUN WITHOUT A PROGRESS SIGNAL — every commissioned run must
    emit a progress signal within its SLA or the supervisor raises
    a starvation alarm and HALTS the run."
  Bank in `STATE/DECISIONS.md`.
  ~12 invariants (6 progress-signal shape + 4 watchdog verdicts +
  1 standing-order text + 1 halt-verdict integrity).

- **CP3 · Governance primitives.**
  New `services/work_supervisor/governance.py` exports
  `GovernanceRule` (ABC: `apply(manifest) → Verdict`),
  `RulingLedgerEntry`, `bank_verdict(verdict) → Path` (idempotent
  within dedupe window). Seed 3 rules (generic, per approval):
  `licence_class_required`, `dispatch_intent_configured`,
  `output_contract_names_real_kind`.
  ~10 invariants.

- **CP4 · Supervisor + Governance compose freeze.**
  Freeze that `admit_job` iterates governance rules in registration
  order, refuses on first veto with `SupervisorRefusal(kind=
  "governance_veto", rule_name=…)`, ledger row banked with rule
  name + reason + manifest fingerprint. No dispatch.
  ~6 invariants.

- **CP5 · Wave close.**
  Owner-facing wave-close doc `notes/W1_WORK_SUPERVISOR_close.md`.
  Double-green byte-match receipt. Ratchet history entry. This
  brief carries wave-honest-limits (§E) — the close doc summarises
  results against those limits.

**Estimated total: ~52 new invariants · ratchet 3282 → ~3334.**

---

## §D. W1b hold-list (case-agnostic platform primitives, GATES W2)

Confirmed holding for a separate `W1b` wave (before W2 job-mount):

- `RetentionPolicy` — four regimes (permanent, ephemeral,
  case-bound, disposal-required), mismatch-refusal by construction.
- `SourceConnector` Protocol + `read_only_guard` +
  Synology FileStation implementation (interface only, no live NAS
  call — NAS reachability remains blocked).
- `Capability` registry — generalisation of `services/layer_b/
  factory.py`.
- L2/L4 contracts: `TargetOutcome_v0`, `StratumAcceptance`,
  `CommissionSpec`, `Milestone`, `WorkerLane`, `WorkerJD`.
- `AudioAttributeStreamBundle_v0`.

None of these belong in W1. Each is a case-boundary primitive that
needs its own tests-first RED and independent close. They will not
fall off — recorded here + in `STATE/NEXT.md` at W1 close.

---

## §E. Wave-honest limits (W1)

1. **No dispatch.** W1 does not execute any command against any GPU
   host, SSH seam, or process. Runtime supervisor is tested
   exclusively against SIMULATED progress signals in `tmp_path`.

2. **No real NAS reach.** SourceConnector is W1b, not this wave.

3. **No pydantic v3 upgrade.** Manifests validated with pydantic v2
   (already installed). Cross-version tolerance out of scope.

4. **Kind registry is a process-scope singleton for W1 tests.** A
   durable on-disk registry (audit trail of registrations) is a
   later enhancement — CP1 exposes the surface and tests use
   `monkeypatch` + `register_kind`/`_reset_kinds_for_tests` for
   determinism. No production process needs multi-writer safety
   yet (no dispatcher runs in W1).

5. **Output-artifact watchdog measures byte growth, not semantic
   growth.** A run that writes zeros steadily would pass the
   flatline check. That's the honest limit at W1; semantic
   watchdogs (kind-specific: e.g., "does the transcribe output
   have the expected phone-set distribution?") are Part-B
   concerns.

6. **SLA is a scalar, not a schedule.** `output_verification_watchdog`
   accepts a single `sla_seconds` at construction. Elastic SLAs
   (per-kind, per-phase) are a later refinement.

7. **Ledger writes are best-effort file writes.** Storage failure
   swallows-and-returns-False, consistent with the campaign_infra
   zero-influence-on-write-failure discipline.

8. **No W1 change to the pod frontend surface.** Runtime supervisor
   is a backend-only surface for this wave. Owner-facing UI is a
   later wave.

9. **No refactor beyond what tests force.** Existing modules
   untouched unless a W1 test forces a change (none anticipated).

---

## §F. Commit protocol

- **Two-commit local per CP is unnecessary** — the wave itself
  follows the two-commit pattern at wave close (CP5). Intra-wave,
  a single code commit per CP is acceptable IFF (a) that CP's
  new invariants are green + no regression, (b) baseline_failures.json
  is updated with the CP-level ratchet increment and history entry,
  (c) the CP does not touch workspace state files.
- **Wave close (CP5)** produces the double-green byte-match receipt
  and TWO commits: one to `programme/track-a` (final code + baseline
  ratchet_history entry with the wave-close SHA backfilled), one to
  workspace `master` (STATE/DECISIONS append, STANDING_ORDERS §3.2
  append if not already banked, notes/W1_WORK_SUPERVISOR_close.md).
- **NO push. Ever.** Local commits are the record.
- **NO testing_agent, NO deployment_agent.** Terminal pytest under
  `BASELINE_GUARD=1` only.
- **Ratchet floor bumped in tandem** at wave close (3282 → new).
- **Report cadence:** silent through CP1-CP4; surface to owner at
  the W1 double-green close per owner's ruling above.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
