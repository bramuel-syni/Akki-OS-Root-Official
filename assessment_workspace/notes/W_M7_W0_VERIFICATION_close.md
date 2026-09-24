READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M7-W0-VERIFICATION · Wave close · 2026-09-16T~04:00Z

**Wave:** W-M7-W0-VERIFICATION (M7 W0 platform integrity walk).
**Verdict:** Path α · CLEAN VERIFICATION · zero-delta close.
**Predecessor:** CP-M6-9-2 · 4358 · track-a `7b45a890` · master `89371cdd` (SW-9 close).
**Track-a HEAD at close:** `7b45a890` (unchanged · verification walk landed no track-a code change).
**Master HEAD at close:** to be recorded post-Commit-B.
**Ratchet floor at close:** **4358** (unchanged).
**Baseline post-close:** `4358 passed, 1 skipped, 438 warnings` (139.15 s).

---

## 1 · Progress made

The M7 W0 walk verified that the platform's "ALIVE IS NOT DONE" contract (STANDING_ORDERS §3.1 · sealed 2026-09-13 at ratchet 3282) is still enforced end-to-end at M6-9-2-close state. Every seal-read and seal-write surface in `services/` was opened, read, and confirmed to route through the `services.output_verified_seal` primitive.

**What was verified from disk this walk:**
- All **6 W0-original refactored sites** — `reconcile.py`, `run_queue.py`, `orphan_detector.py`, `adopt.py`, `watchdog.py` (via composition through `orphan_detector`), `on_host_logging.py` — still import `is_real_seal` or `output_verified_seal` from the primitive module. Line-referenced evidence banked in the machine receipt.
- **5 new seal-adjacent surfaces** added since 2026-09-13 W0 close — `audio_poc/wave_close.py`, `census_canon/audio_inventory_supplement.py`, `output_verified_seal/__init__.py` (the primitive itself), `work_supervisor/governance.py`, `work_supervisor/supervisor.py` — either compose correctly with the primitive (governance, supervisor) or reference the seal in docstring only (audio_poc constants, audio_inventory_supplement).
- **31 W0 invariants** in `tests/invariants/test_output_verified_seal.py` all pass (file-scoped BASELINE_GUARD run confirms).
- **Full baseline** green at 4358 both before and after the walk.

Machine-readable receipt: `phase0/m7_w0_verification/verification_receipt_20260916.json`.

## 2 · How much to go

- **W-M7-W0-VERIFICATION** — CLOSED this shift (Path α clean · zero-delta).
- **W-M7-W1-VERIFICATION** — next in sequence · identical shape (SO §3.2 progress-signal contract · `services.work_supervisor.runtime_supervisor` + `test_w1_cp2b_runtime_supervisor.py`). Estimated single-shift walk.
- **W2 (job-mount)..W9 (retention ruling)** — blocked-on-owner per ROADMAP §E.2 (NAS reachability · HF token · 3-station selection · RetentionPolicy binding · Ruling #5 sub-verdicts).
- **W-M7-UTILIZATION-72H** — concurrent priority interleave · running since 2026-09-16T03:41:28Z · deadline 2026-09-19T~03:41Z · remaining 71.69 h at W0-close check-in.

## 3 · Decisions taken

1. **W0 walk scope frozen as VERIFICATION** (not re-build): the W0 platform primitive was sealed 2026-09-13; the M7 activation of W0 is a parse-not-paraphrase verification against the current tree. Documented in the grounding brief §C two-path (α clean / β drift) decision.
2. **Path α taken this walk** (verdict: clean · no drift): every seal-check surface currently in `services/` routes through the primitive. No CP-M7-W0-1..N is authored. No tests-first RED / mechanism / seal / ratchet delta fires. This is by-design under Path α.
3. **Standing Rule 2 exercised for freshness-class drift**: `test_cp10_harness_receipt_is_still_recent` fired between the two baseline runs this shift (first run at 03:37Z passed with age ~11.9h; second run at 03:53Z failed with age ~12.3h). Sanctioned regeneration via `tools/wave_g5_realchrome_verification_harness.py --strict` at 03:55:59Z → GREEN, ground-truth metrics unchanged (body_len=608177 · dummies_declared=37 · marked_slots_count=29). Not a rebaselining; per prior precedent (CP-EXR1 shift 2026-09-15T~15:58Z).
4. **W0 close pattern deviates from §3.3 3-commit** (single-master-commit): no track-a code change lands, so no Commit A fires. Commit B on master banks all this-wave state (M7-open note + W0 grounding brief + verification receipt + W0 close report + NEXT.md pin + DECISIONS.md entry + freshness-regeneration artefacts). No Commit C fixup needed because no seal file references a master SHA.

## 4 · Discoveries not envisioned at planning

1. **W0 primitive coverage has strengthened during M6, not weakened**: 5 new seal-adjacent surfaces authored during M6's 9 sub-waves (audio-poc close, work-supervisor supervisor + governance, census-canon supplement, plus the primitive module itself as it was born at W0) all compose correctly with the primitive rather than reinventing seal-check logic. This is the "anti-proliferation" pattern (Audio-Plane §1.2 verbatim: *"Anything ... that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build"*) materially working across a real 253-invariant milestone.
2. **The W0 invariant `test_output_verified_seal.py` acts as a hard perimeter**: any new site added after 2026-09-13 that bypassed the primitive would have surfaced as a right-reason RED against one of the 31 existing invariants. That the file has 31 tests collected (unchanged from 2026-09-13 close count) is itself evidence the contract has not been weakened by any inadvertent test relaxation during M6.

## 5 · Recommendations to make the experience better, in line with the mission

1. **Repeat the W0 pattern for W1** next (SO §3.2 "NO RUN WITHOUT A PROGRESS SIGNAL"): enumerate every dispatch surface in `services/` for the token union `runtime_supervisor|record_progress|output_verification_watchdog|ProgressSignal|HaltVerdict`; confirm each binds to the progress-ring per SO §3.2 clause 1; if any dispatch surface added since 2026-09-13 does not bind, that is a first-class CP-M7-W1-1. Deliverable shape identical to this W0 walk: verification receipt (JSON) + close report + single master commit.
2. **Do NOT add an invariant enforcing the base64-launcher idiom** to gate SSH-detach flows across `tools/`: the launcher pattern is a state-repo utility idiom (recovery banked in `notes/M7_UTIL_72H_LAUNCH_RECOVERY_20260916.md`), not a `services/**` contract. Adding a test invariant would over-couple the ratchet to a tooling implementation detail. If the pattern recurs, promote it to a `tools/launcher_helpers.py` shared surface with its own tests.
3. **Pre-author the W2 JobManifest v1 skeleton** during the current owner-blocked window (NAS reachability · HF token · 3-station selection): a config-only YAML at `phase0/jobmanifest_drafts/audio-census-rms-16-stations-non-english-music-free-v1.yaml` with all deterministic fields populated. When the four owner-blockers unblock together, W2 CP1 (Mount) becomes a one-line commit.

---

## §G · Freshness-class drift Standing Rule 2 exercise (verbatim receipt)

**Trigger.** `test_cp10_harness_receipt_is_still_recent` failed on the second baseline run this shift:
- First baseline (boot ritual · 03:37Z): `4358 passed, 1 skipped, 438 warnings` at receipt age ~11.9h.
- Second baseline (verification confirmation · 03:53Z): `1 failed, 4357 passed, 1 skipped, 438 warnings` at receipt age ~12.3h.

**Cause.** Time-based freshness threshold (12h) crossed during the shift. Not a real regression.

**Sanctioned regeneration.** `python3 tools/wave_g5_realchrome_verification_harness.py --strict` at 03:55:59Z.

**Result (verbatim harness log tail):**
> GREEN · verification PASSED · dummies absent, expected present, styled-element-anchor spans intact
> substitutions applied (portal): 0
> substitutions applied (registry): 8
> dummies still present on Registry: []
> expected present on Registry: ['RMS AI is reading', 'awaiting first census', 'read the estate at the seam']
> expected missing on Registry: []
> style signature (INTERRUPT 3): underline=3/3, oxblood=1/1, met=True

**Ground truth unchanged.** `body_len=608177 · dummies_declared=37 · marked_slots_count=29` — identical to 2026-09-15T15:40:21Z receipt.

**Post-regeneration baseline.** `4358 passed, 1 skipped, 438 warnings` (139.15 s). Green.

---

## §H · GPU utilization check-in interleave (per grounding brief §G)

**Check-in fired at W0 close:** `python3 tools/m7_util_72h_orchestrator.py check_in` @ 2026-09-16T~04:00Z.

**Rollup (as of check-in):**
- akki-vm: sampler_alive + workload_alive · telemetry_samples=18 · bench_iterations=34 (ok=34) · per-GPU peak util 100% · peak power 689/692 W · peak temp 69°C · peak mem 12.9 GB.
- akki-vm-ii: sampler_alive + workload_alive · telemetry_samples=12 · bench_iterations=36 (ok=36) · per-GPU peak util 100% · peak power 691/693 W · peak temp 70/71°C · peak mem 12.9 GB.
- Elapsed: 0.31 h · Remaining: 71.69 h.
- Report served (HTTP 200): `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
