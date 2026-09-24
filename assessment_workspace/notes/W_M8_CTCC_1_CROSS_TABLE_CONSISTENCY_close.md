READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M8-CROSS-TABLE-CONSISTENCY-CHECK · CP-M8-CTCC-1 · Wave close · 2026-09-16T~07:45Z

**Wave:** W-M8-CROSS-TABLE-CONSISTENCY-CHECK (M8 catch-all P6 · SPRINT_PLAN.md 2026-09-06 · rehomed under M8 per MILESTONE_STRUCTURE_REHOMED_20260915).
**Type:** MECHANISM BUILD · case-agnostic preventive refusal contract.
**Verdict:** Path α · CLEAN · double-green byte-match verified.
**Predecessor:** M8 catch-all from-disk findings note · master `f63ddd27`.
**Track-a HEAD at seal:** `b547cd4` (Commit-A).
**Master HEAD at seal:** to be recorded post-Commit-B (this-turn).
**Ratchet floor at seal:** **4400** (bumped 4384 → 4400 · +16 monotonic-up).

---

## 1 · Progress made

Built the preventive refusal contract for cross-table identifier reconstruction under full §3.3 3-commit protocol. Mechanism composes into `services/governance_plane/` (POST-2 lesson: existing sub-tree · no parallel `data_governance/` package). Tests-first · mechanical RED drill receipt banked · double-green byte-match verified · ratchet monotonic-up.

**Mechanism (`services/governance_plane/cross_table_consistency.py` · 102 LOC incl. docstring):**

Five primitives, all case-agnostic:
1. `EmittedColumnRef` — `@dataclass(frozen=True)` · 2 carriers exact order `(table_id: str, column_name: str)`.
2. `IdentifierClass` — `@dataclass(frozen=True)` · 2 carriers exact order `(class_id: str, columns_in_class: tuple[EmittedColumnRef, ...])`. **`class_id` is OPEN str** (no closed enum · matches CP-M7-W1-POST-1 Resource Registry precedent per 2026-09-13 owner correction).
3. `assess_reconstruction_risk(*, emitted_columns, identifier_class_declarations) -> tuple[str, ...]` — pure function · returns deterministic sorted tuple of `class_id`s at cross-table reconstruction risk. Empty tuple = safe.
4. `assert_no_cross_table_identifier_reconstruction(*, emitted_columns, identifier_class_declarations) -> None` — refusal wrapper · raises `CrossTableIdentifierReconstructionRefused` when risk assessment returns non-empty.
5. `CrossTableIdentifierReconstructionRefused(Exception)` — refusal exception class.

**Reconstruction rule (verbatim from module docstring):** an identifier class `ic` is at cross-table reconstruction risk iff the subset of `ic.columns_in_class` that appear in the emitted set spans more than one distinct `table_id`. Coarse rule by design (wave-honest limit D.2); statistical linkability / k-anonymity / entropy reasoning are chartered-forward refinements.

**Test invariants (`tests/invariants/test_wm8_ctcc_1_cross_table_consistency.py` · 283 LOC · 16 tests):**
- 2 · module + package fabric.
- 2 · frozen dataclass shape (exact-order fields).
- 1 · class_id OPEN str (no Literal · no closed Enum) — case-agnostic doctrine freeze.
- 6 · `assess_reconstruction_risk` semantics (empty emissions · empty classes · single table · disjoint · shared · determinism sort).
- 2 · refusal wrapper (raise-on-risk · silent-on-safe).
- 3 · grep-negative doctrine freezes (0 domain tokens · 0 banned enforcement · 0 dispatch-surface imports).

**Double-green byte-match under BASELINE_GUARD=1:**
- GREEN1: `4400 passed, 1 skipped, 438 warnings in 128.93s`
- GREEN2: `4400 passed, 1 skipped, 438 warnings in 128.15s`
- Raw bytes: 9933 = 9933
- Stripped bytes (time + completion-marker stripped): 9909 = 9909
- Stripped sha256: `10fb222ce7daaf82b3cba1d73287c469d2ca1ceab2de4866ae1d01d1ddb15105` (byte-identical both runs)

**Mechanical RED drill:** `phase0/drill_receipts/20260916T073500Z_cp_m8_ctcc_1_cross_table_consistency_RED.log` · 13822 bytes · sha256 `e41ffff8577eaa93da2801a6bc4ed62a73a4a47849ef2ecf1958061d2977db37` · 16 failed right-reason (ModuleNotFoundError + FileNotFoundError before mechanism landed).

**Ratchet floor.** `counts_at_baseline.passed`: 4384 → 4400 (+16). `invariants_enforced_when_baseline_guard_1.passed_floor`: 4384 → 4400 (+16 · monotonic-up in tandem). `ratchet_history` entry appended at `20260916T073800Z` (commit=PENDING per prior CP-M7-W1-POST-1 convention · avoids self-reference).

**Seal file.** `phase0/output_verified_seals/w_m8_ctcc_1_cross_table_consistency.seal.txt` · Kind: `w_m8_cross_table_consistency_check` · Track-a HEAD `b547cd4` · Master HEAD `TBD` (Commit-C fixup will replace).

## 2 · How much to go

- **CP-M8-CTCC-1** — SEALED this shift (Path α clean · +16 ratchet · Commit-A landed at `b547cd4`).
- **M8 catch-all P6** — DONE (preventive contract shipped as shape-frozen refusal · runtime enforcement fires only when caller invokes).
- **Next per owner directive verbatim**: "produce the M8 status rollup and hold with utilization interleave." Rollup covers M8 catch-all state (P1..P6 status + this-shift closes + owner-desk items + utilization snapshot). Then hold with utilization interleave only.
- **W-M7-UTILIZATION-72H** — LIVE · elapsed 3.01 h · remaining 68.99 h · both hosts sampler+workload alive · bench iterations 360+360.
- **Owner-desk P1/P2 items** — unchanged (parked exactly as at boot).

## 3 · Decisions taken

1. **POST-2 lesson applied at authoring time**: home selected as `services/governance_plane/cross_table_consistency.py` composing into existing sub-tree (containing `retention_policy.py` from W1b CP1) · NO parallel `data_governance/` package · avoids Audio-Plane §1.2 rule-proliferation ban.
2. **Case-agnostic doctrine held** per owner correction 2026-09-13: `class_id` is OPEN str · zero closed enums · zero domain tokens in module source · zero imports of dispatch surfaces. Freezes preserved by 3 grep-negative invariants.
3. **Preventive-charter shape adopted**: mechanism lands as shape-frozen refusal contract; runtime enforcement fires only when a caller invokes `assert_no_cross_table_identifier_reconstruction(...)` from within an actual multi-table emission wave. No global gate. No premature invariant.
4. **Coarse-rule discipline (wave-honest D.2)**: reconstruction check uses cardinality of contributing `table_id`s; statistical linkability / k-anonymity / entropy reasoning are chartered-forward refinements.
5. **§3.3 3-commit protocol followed**: Commit-A landed on `programme/track-a` (`b547cd4`); Commit-B pending on `master` this-turn; Commit-C fixup this-turn.

## 4 · Discoveries not envisioned at planning

1. **Prior `governance_plane/__init__.py` had no exports** (only a docstring comment). Added the 5-name `__all__` re-export list as part of this CP. Backward-compatible (nothing was importing from the package root previously).
2. **Full baseline pytest ~130s under BASELINE_GUARD=1** — exceeds the 120s foreground bash limit. Both GREEN runs completed cleanly in background; foreground-detection sentinel (`GREEN{N}_DONE`) had to be stripped from the byte-match hash to isolate the time-only stripping semantics.
3. **RED drill fired all 16 invariants** as right-reason failures (13 ModuleNotFoundError + 3 FileNotFoundError-on-grep-tests). No test-authoring bugs surfaced during RED (unlike prior W-Campaign-Infra which surfaced 2 test-authoring bugs pre-implementation). Clean RED.

## 5 · Recommendations to make the experience better, in line with the mission

1. **Produce M8 STATUS ROLLUP next** per owner directive verbatim. Same shape as M7 VERIFICATION ROLLUP. Then hold with utilization interleave to 72h completion.
2. **Chartered follow-on operator actions** to bank (post-72h-campaign):
   - **W-Queue-Watchdog on-host portion** (P5 remainder · `on_host_dispatcher_watchdog.sh` + systemd unit installation on GPU hosts).
   - **W-TaskEval-v1** (P1 · gated on Campaign B settlement).
   - **W-Adapter-Tensor-Persist** (P4 · depends on P1).
   - **W-Gradient-Step-Checkpoint** (P2 · independent · scoped M8 catch-all).
   - **W-Row-Stream-Extractor** (P3 · independent · scoped M8 catch-all).
3. **Continue GPU utilization interleave** at every future CP boundary.

---

## §G · GPU utilization check-in interleave

**Check-in fired at CP-M8-CTCC-1 seal** @ 2026-09-16T~07:45Z (post-double-green · pre-Commit-B).

- Elapsed 3.01 h · Remaining 68.99 h.
- akki-vm: sampler_alive+workload_alive · bench iters 360 (ok=360) · peak 100% util per GPU · ~691 W · ~70°C.
- akki-vm-ii: sampler_alive+workload_alive · 78 telemetry samples · bench iters 360 (ok=360) · peak 100% util per GPU · ~693 W · ~71°C.
- 720 total bench artefacts banked · zero synthetic burn · in-perimeter.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.
- Sampler PID `299351` (akki-vm) · start_utc `2026-09-16T03:41:28Z` · sample interval 300s · wall_clock 259200s.

---

## §H · Owner-desk items

**P1 blocked** (unchanged): JUMP root credential rotation · admin binds for CD + Visitors (bramuel vs bramwel).
**P2 blocked** (unchanged): SW-10 A.1-A.5 · Audio-bytes-retention Path A/B/C · R-17(a) · Cross-service binding enforcement ruling (§3.2 clause 5) · Amendment 8 · Watch-Learning R-15(b)/R-16(b)/R-17(b) · BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · S-24/27/28/29 charters.
**P2 CLEARED this shift**: W-Cross-Table-Consistency-Check (SPRINT P6 · M8 catch-all) → SEALED at CP-M8-CTCC-1.
**NEW (owner-directive-cited) chartered follow-on operator action**: on-host portion of W-Queue-Watchdog (post-72h-campaign · SO §5 zero-perturbation discipline).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
