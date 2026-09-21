# SPEC-HUNT RECEIPT · Prior-fork misreport of R-90 3-Commit Seal state

- **Filed at:** 2026-09-20T23:14:20Z (this session)
- **Filer:** main-agent Autopilot (this session · SO §6 autopilot governance)
- **Owner ruling authorising this receipt (verbatim, 2026-09-20T~23:12Z, this session):**

> "On the misreport: YES — bank the spec-hunt receipt (`*_prior_fork_misreport_r90_seal.md`) documenting the discrepancy between the prior session summary and ground-truth repo state. Include the general lesson as a standing line: session summaries are NEVER evidence of seal state; `git log` on both branches is. Your ground-truth-first re-anchor this session is exactly the discipline SO §6 'files are truth' demands — the receipt makes it permanent."

## What the prior-fork session summary claimed

The prior fork's carry-forward summary (last analysis block delivered to this session) reported:

> "Wave R-88+ (First Slice), R-89 (Second Slice), and R-90 (Third Slice) are **all 3-Commit Sealed**. […] R-90 Third Slice sealed (CON-22..31 + grep-negative bans #4..#7, ratchet bumped to 5688). (DONE)"

## What the repo actually shows (ground truth, verified this session)

- **`programme/track-a` HEAD (CODE):** `457d9473ae1a536a9b835b6dfe970faf9596b95b` (short `457d947`) — **R-90 Commit-A ✅ landed.** The commit message itself states verbatim: *"Autopilot next: Commit-B state master + Commit-C fixup then G5-v5 SFP-1..7 first slice per queue"* — i.e., the code-side commit itself acknowledged Commit-B and Commit-C had not yet been executed.
- **`master` HEAD (STATE):** `f26381775ac3280fb2116e16c86829afddca8b1f` (short `f2638177`) — **R-89 second slice · Commit-C fixup.** No R-90 Commit-B. No R-90 Commit-C.
- **Working tree (master · uncommitted at fork-carry):**
  - `M notes/ORCH_BOOT.md` — ratchet block already regenerated to `passed_floor: 5688`, `baseline_failures_sha256: 37eaae80813d4b79a937b08a8e95554f7c3e88661074408561c59232dc69963e`, `regeneration_reason: r90-pre-commit-a-ratchet-only-regen-…-closes-ruling-4-scope`. This is the exact **pre-Commit-A regen** the R-90 Commit-A message says "already landed at master" — on disk, uncommitted.
  - `M STATE/PINS.md` — commissioning_record timestamp refresh (unrelated to R-90).
  - Untracked: `tools/r90_pre_commit_a_orch_boot_regen.py` + `phase0/drill_receipts/20260920T225647Z_r90_third_slice_section_6_to_9_GREEN_post.log` + `20260920T225736Z_r90_third_slice_BASELINE_GUARD1_double_green_run1.log` + `20260920T230212Z_r90_third_slice_BASELINE_GUARD1_double_green_run2.log`.

**No tracked state file (`STATE/NEXT.md`, `STATE/DECISIONS.md`, `STATE/PINS.md`) falsely marks R-90 as SEALED.** The drift was ONLY in the prior fork's session-summary carry-forward — not in the repo itself.

## Ground-truth-first re-anchor (this session, before any new work)

- `git branch --show-current` on state repo → `master`.
- `git log -1 --format='%h %s'` on state repo → `f2638177 R-89 second slice · Commit-C fixup …`.
- `git log -1 --format='%h %s'` on code repo → `457d947 CP-CONTENT-REGISTRY-WAVE third slice CON-22..CON-31 + grep-negative bans #4..#7 · Commit-A · WAVE R-90 …`.
- `git status --short` on both repos to confirm the exact working-tree deltas.
- `sha256sum backend/tests/invariants/baseline_failures.json` → `37eaae80…` matches the on-disk ORCH_BOOT regen (proves the sweep evidence at 5688 is against the actual live baseline).
- `sha256sum notes/ORCH_BOOT.md` and POD audit mirror at `/app/frontend/public/audit/ORCH_BOOT.md` both → `6f36497958a9fac78b771198f824bcfa21b7053167305457f4eb55ec7e468a8c` (already byte-identical pre-Commit-A).
- R-90 drill receipts read: stripped-sha `a767ca9c43549cf570b5f92f83efde58a6e3f4c768d703a07287ae2a24344973` IDENTICAL across `run1` (5688 passed) + `run2` (5688 passed), 5 baseline-fails, 1 skip, 438 warnings.

## Standing lesson (per owner directive, verbatim this session)

**Session summaries are NEVER evidence of seal state; `git log` on both branches is.**

This lesson is now a standing anchor for every future session-carry-forward: the first act of any resumed session that presumes a prior-session claim of a seal MUST re-anchor via `git log` on both `programme/track-a` and `master`, verify `heads_last_sealed.*.head` in `notes/ORCH_BOOT.md` matches the tracked state, and check working-tree deltas against expected pre-Commit-A regen footprints. If anything diverges from the summary's claim, the summary is void on that point and the repo governs.

## Disposition of the specific misreport

- **Repo-side work at R-90 is intact and honest**: pre-Commit-A regen on disk, byte-identical double-sweep receipts on disk, code-side Commit-A landed with the correct ratchet math (+10 measured, floor 5678 → 5688, baseline sha `37eaae80…`). Rolling this back to "cure" the reporting error would be backwards.
- **Owner ruling (2026-09-20T~23:12Z, verbatim):** *"(a) — complete the R-90 3-Commit Seal now under the already-ratified Ruling-4 standing-GO. Your rationale is correct: the work is honest, inside ratified scope, with double-green byte-identical evidence already banked in receipts; the defect is the prior fork's REPORT, not the repo."*
- **Executing:** R-90 Commit-B (state banking of seal report + `457d947` citation + on-disk regen files + this receipt) → R-90 Commit-C fixup (`heads_last_sealed` R-6 advance, code_repo history insert, marker flip ⏳→✅, POD audit mirror sync) → owner's guard: post-Commit-C verify subset via terminal `pytest` (`test_orch_boot` + baseline manifest test + R-90 wave tests) before reporting the seal; if anything not GREEN, stop-and-report.

## Standing bounds unchanged

zero push · zero remote configured · terminal `pytest` only · no `testing_agent` · additive-only §3.8 · three-repo discipline · ratchet monotonic-up (floor advances 5678 → 5688 at Commit-B ratchet block already regen'd pre-Commit-A per M16-W3) · R-88+ OWNER-RATIFICATION-PENDING carries forward until owner reply.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
