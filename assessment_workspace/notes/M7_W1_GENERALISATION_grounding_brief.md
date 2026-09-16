READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M7-W1-VERIFICATION · Grounding brief · 2026-09-16T~04:05Z

**Wave:** W-M7-W1-VERIFICATION (M7 W1 generalisation-primitive verification walk).
**Type:** VERIFICATION WALK — not a mechanism build.
**Predecessor:** W-M7-W0-VERIFICATION close (Path α clean · zero-delta · master `6fd96b10`).
**Concurrent:** W-M7-UTILIZATION-72H · LIVE from 2026-09-16T03:41:28Z · elapsed 0.31h at W0 close.

---

## §A · Owner authorization verbatim

**2026-09-16T~04:05Z · this shift (via user relay · OWNER GO banked):**

> "Continue with build."

**2026-09-16T~03:08Z · sequence directive verbatim (via user relay):**

> "M7 OPENS per the ratified tree (W0 platform integrity → W1 generalisation → W2..W9). Author the M7-open milestone-boundary note + W0 grounding brief, then walk autonomously under all standing guardrails."

**2026-09-15T~04:12Z · M7 reframe verbatim:**

> "Then M7 open: same pattern — reframe-activation note + W0 platform integrity → W1 generalisation → W2+ as unblocked."

## §B · Verbatim canon anchors

**STANDING_ORDERS.md §3.2 · "NO RUN WITHOUT A PROGRESS SIGNAL" (banked 2026-09-13 · verbatim owner directive "W1 CP breakdown approval"):**

> **NO RUN WITHOUT A PROGRESS SIGNAL** — every commissioned run must
> emit a progress signal within its SLA or the supervisor raises a
> starvation alarm and HALTS the run.

**Binding contract on every commissioned run (STANDING_ORDERS §3.2 clauses 1-5):**

> 1. Every dispatch surface in the codebase MUST bind its run_id to
>    the `services.work_supervisor.runtime_supervisor` progress-ring:
>    the running trainer/harvester/extractor emits `ProgressSignal`
>    records at least once per SLA window via
>    `runtime_supervisor.record_progress(sig, ring_root=…)`.
> 2. Before treating a run as still-in-flight, callers MUST invoke
>    `runtime_supervisor.output_verification_watchdog(job_id, ...)`.
>    A returned `HaltVerdict` binds the caller to STOP dispatching
>    further work on that run and surface the verdict.
> 3. Halt reasons are closed-enum data (`starvation_no_signal` /
>    `starvation_stale_signal` / `starvation_output_flatline`). A
>    HALT verdict is DATA — the runtime supervisor NEVER kills any
>    process. Callers act on the verdict; observation and mutation
>    remain separate (zero-influence discipline preserved).
> 4. Wave-honest limit: the W1 watchdog measures BYTE growth, not
>    semantic growth. A run that writes zeros steadily would pass
>    the flatline check. Semantic watchdogs (per-kind output shape
>    validators) are Part-B concerns.
> 5. Invariant `test_w1_cp2b_runtime_supervisor.py` freezes this
>    contract. Any dispatch surface added later that does NOT bind
>    to the progress ring is a right-reason RED under BASELINE_GUARD=1.

**W1 CP2b primitive contract (from `services/work_supervisor/runtime_supervisor.py` docstring · verbatim):**

> `ProgressSignal` (frozen dataclass): job_id, at_utc (ISO Z), magnitude, output_bytes, output_path.
> `record_progress(sig, *, ring_root) -> Path` — persist ProgressSignal to the ring.
> `load_progress(job_id, *, ring_root) -> list[ProgressSignal]` — read ring sorted by at_utc.
> `output_verification_watchdog(job_id, *, sla_seconds, ring_root, now_utc, output_path=None) -> HaltVerdict | None` — reads the ring, returns HaltVerdict on first starvation hit, None on healthy.
> `HaltVerdict` (frozen dataclass): job_id, reason ∈ {starvation_no_signal, starvation_stale_signal, starvation_output_flatline}, at_utc, last_progress_at_utc, message.
> `StarvationAlarm(RuntimeError)` — named exception class for wrapping-boundary use.

**Zero-influence contract (verbatim `runtime_supervisor.py` line 19-21):**

> "the watchdog READS progress signals + optionally STATs the named output artifact. It never kills any process. A HALT verdict is DATA (a returned dataclass); callers act on it."

## §C · Wave scope · VERIFICATION WALK (this shift)

**Goal.** Verify from-disk that:

- **C.1** The `runtime_supervisor` module is importable and exports the expected surface (`ProgressSignal`, `HaltVerdict`, `StarvationAlarm`, `record_progress`, `load_progress`, `output_verification_watchdog`).
- **C.2** The `test_w1_cp2b_runtime_supervisor.py` invariant file is present with its 16 contract-freezing tests, all passing.
- **C.3** The standing order §3.2 text is present verbatim in `STATE/STANDING_ORDERS.md` at the canonical `## 3.2 NO RUN WITHOUT A PROGRESS SIGNAL` heading, including the 5-clause binding contract.
- **C.4** No modification to `runtime_supervisor.py` has been made since W1 close 2026-09-13 that would silently weaken the primitive contract (from-disk diff-since-W1-close read).
- **C.5** Companion W1 modules (`kind_registry.py`, `job_manifest.py`, `supervisor.py`, `governance.py`) still exhibit their W1 CP1/CP2/CP3/CP4 contracts (all 68 W1 invariants pass under a file-scoped pytest run).
- **C.6** Enumerate all candidate dispatch surfaces currently in `services/` (trainers/harvesters/extractors) and report — honestly — whether each binds to the runtime_supervisor progress-ring, noting explicitly which surfaces do NOT bind. This surfaces the wave-honest limit: the CP2b invariant freezes the PRIMITIVES but does not gate cross-service binding (clause 5 is aspirational until per-dispatch invariants land).

**Two-path decision (identical shape to W0 walk):**

- **Path α · Clean verification** — Every point C.1–C.5 is confirmed clean. C.6 surfaces as WAVE-HONEST LIMIT (not drift): the CP2b invariant did not freeze cross-service binding enforcement, so absence-of-binding at a dispatch surface is a Part-B concern to be authored as a future CP-M7-W1-POST-* if/when the owner rules that cross-service binding is a hard-gate. Close W0-shape: verification receipt + close note + single master commit.
- **Path β · Drift discovered** — Any of C.1–C.5 fails: the W1 CP2b primitive has been silently weakened. Each drift is a first-class CP-M7-W1-<n> with tests-first RED → mechanism → double-green → seal → §3.3 3-commit.

## §D · Wave-honest limits

**D.1 (cross-service binding gate deferred).** The CP2b invariant `test_w1_cp2b_runtime_supervisor.py` freezes the primitive shape and confirms the standing order text is present. It does NOT enforce "every dispatch surface binds to the ring" (the inclusive contract of §3.2 clauses 1-2). Enforcing that would require a per-dispatch-surface invariant that greps the codebase for `execute_run`-shaped functions and asserts each imports `runtime_supervisor.record_progress` — a form invariant that would BLOCK any future dispatch surface from landing without binding. The 2026-09-13 W1 CP breakdown did not scope this invariant (owner directive verbatim: "Test them against SIMULATED run states (no real dispatch needed)... This is generic and testable without W2 dispatch"). Wave-honest reading: cross-service binding enforcement is a Part-B / W2-preparation concern, not a W1 CP2b concern.

**D.2 (byte-growth-only watchdog).** SO §3.2 clause 4 verbatim: "the W1 watchdog measures BYTE growth, not semantic growth. A run that writes zeros steadily would pass the flatline check." Semantic watchdogs are out of W1 scope by owner ratification.

**D.3 (zero-influence separation).** The watchdog cannot kill processes. HALT verdicts are data; callers act on them. This is enforced by `test_watchdog_public_surface_has_no_terminator_names` (line 352 of the invariant file · covered under C.2).

**D.4 (72h utilization job not W1 dispatch surface).** The concurrent `W-M7-UTILIZATION-72H` job dispatches long-running work via `tools/m7_util_72h_orchestrator.py` (state-repo tooling · not `services/`). It carries its OWN progress signal (sampler JSONL + workload JSONL + regenerated report) rather than binding to `runtime_supervisor.record_progress`. This is by design: the utilization job is one-off tooling for an owner-facing deliverable, not a platform-commissioned run subject to §3.2. Documented as a wave-honest note; not a drift item.

## §E · Concrete owner-facing decision surfaces

None at grounding-brief authoring. Verification is case-agnostic. If Path β fires (drift), the specific drift will surface as a HALT-to-owner if it touches load-bearing PII / custody / owner-desk items; otherwise autonomous per SO §3.

## §F · Commit protocol (per §3.3 · with W0-precedented deviation for zero-code-delta verification walks)

- **Path α (clean · this shift target):** ONE state commit on master carrying:
  1. `notes/M7_W0_VERIFICATION_close.md` — prior; already banked at master `6fd96b10`.
  2. `notes/M7_W1_GENERALISATION_grounding_brief.md` — this file.
  3. `phase0/m7_w1_verification/verification_receipt_20260916.json` — banked at walk close.
  4. `notes/W_M7_W1_VERIFICATION_close.md` — 5-section END-OF-WAVE format.
  5. `STATE/NEXT.md` pin update.
  6. `STATE/DECISIONS.md` W1 verification-close entry.
  7. GPU utilization check-in artefacts (phase0/gpu_utilization_72h/ delta + phase0/gpu_receipts/ new probes).
  Commit message: `W-M7-W1-VERIFICATION · verification walk · verdict={clean|drift} · surfaces=N · ratchet unchanged 4358`.
- **Path β (drift · this shift or next):** per §3.3 3-commit pattern per CP.
  - Commit A on `programme/track-a`: code fix + tests-first invariant.
  - Commit B on `master`: state + notes + seal file (master SHA TBD).
  - Commit C on `master`: fixup (master SHA landed).

## §G · GPU utilization check-in interleave (per M7 grounding pattern)

Check-in `python3 tools/m7_util_72h_orchestrator.py check_in` fires at:
- **W1 open** — this-turn check-in (fired at W0-close ~04:00Z, still fresh; refresh at W1-walk mid-point).
- **W1 seal** — at Path α close.
- Continuously as W-M7-W1 progresses if wall-clock > 30 min.

If the current bench workload iteration finishes early (unlikely on a 72h run at ~650 TFLOPS sustained), chain next mission-aligned workload (Mtafiti embeddings) rather than idle-burn.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
