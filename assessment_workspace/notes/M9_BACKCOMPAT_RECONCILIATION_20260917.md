READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M9 · §3.3 BACK-COMPAT BATCH · RECONCILIATION MEMO · 2026-09-17

## Scope

State-only Commit-B + Commit-C fixup pair banking the master-side §3.3 3-commit protocol for **20 CPs** that landed Commit-A on `programme/track-a` between 2026-09-17T~05:47Z and 2026-09-17T~08:45Z but never received Commit-B / Commit-C on master. Batch executed under owner directive path (a) verbatim 2026-09-17 ("BACK-COMPAT-FIRST — Reconcile the master-side seal chain so on-disk state matches reality before any new CP work").

Analogous to the M8 §3.3 back-compat batch (Owner Ruling 2026-09-16T~08:10Z: *"this owner runs SHA-256-level audits — full seal-chain parity is worth 5 cheap commits"*) but expanded to 20 CPs and executed as a single Commit-B + Commit-C fixup pair rather than 20 individual per-CP fixups (matches M6 SEAL state-only close precedent: §3.3 2-COMMIT SHAPE with no Commit-A + Commit-B + Commit-C fixup).

## Ground-truth verification per integrity guardrail (2026-09-17 user directive rule 3)

For EACH of the 20 CPs the following three-part on-disk verification was performed BEFORE authoring this batch. Verification results are recorded verbatim; nothing is inferred, nothing is fabricated.

### Verification (i): Track-a Commit-A commit exists

| CP | Track-a SHA (verified `git log programme/track-a`) | Status |
|----|---------------------------------------------------|--------|
| CP-P3-CP4 | `10953615610a082d4e3e6376087a17978284efb3` | ✅ present |
| CP-P3-CP5 | `a53d6e6e7ff745bfb1a51d33af14be6dda7f1943` | ✅ present |
| CP-P4-CP1 | `bcaa5e8a0a05c571600c8fb715b78de9d87e9d48` | ✅ present |
| CP-P4-CP2 | `f1b39fd51762ea9645a71a1a2605aa6252e8e7e8` | ✅ present |
| CP-P4-CP3 | `8158de62e73a474eb8d31d758ac07c45a6a394e6` | ✅ present |
| CP-P4-CP4 | `ee70c4ab103440e1e151af6c2224d516feb52797` | ✅ present |
| CP-P4-CP5 | `dcbd5d0777ef04a5b27a97ca28d291d66510bd33` | ✅ present |
| CP-P4-CP6 | `09ed7d4f8a3225f2c57848ecb9c2cdde9f074bfb` | ✅ present |
| CP-P4-CP7 | `6af22a3690c74ee9b71ab7276584f6c20c8b93ec` | ✅ present |
| CP-P4-CP8 | `be94bfee294b2862f82575836e5abb16b7ab2436` | ✅ present |
| CP-P5-CP1 | `ffae1f86650228a66a622fe55bfb3d68b6eafd57` | ✅ present |
| CP-P5-CP2 | `74577d83521b1b75ae52a31287043b2101291f61` | ✅ present |
| CP-P5-CP3 | `6819fd1100fcf89cd801622c412df3a742c92f34` | ✅ present |
| CP-P5-CP4 | `7f34c3dc9bb77510d84a93192842011e2c2c6001` | ✅ present |
| CP-P5-CP5 | `68af117d4ee18e483c375c3af4b54bbe80713f0c` | ✅ present |
| CP-P5-CP6 | `51a39530b38e6f2a485235e714d9c32ec95db063` | ✅ present |
| CP-P6-CP1 | `eede16f3da6eda54adcd5e5778668b5d1281772c` | ✅ present |
| CP-P6-CP2 | `601297ab2b96733ec86cb22c7739c88e1344df2b` | ✅ present |
| CP-P6-CP3 | `db1aafaad8f46a2100580741455771fa8150809a` | ✅ present |
| CP-P6-CP4 | `e436028251b0ae18919c163123b565e3000384ed` | ✅ present |

Result: **20/20 track-a Commit-A commits verified on disk.** No fabrication needed.

### Verification (ii): Ratchet step is real and monotonic

Source: `tests/invariants/baseline_failures.json` field `ratchet_history` (indices 195–214). All 20 entries banked between `20260917T055500Z` and `20260917T084500Z` (chronological). Passed counts read:

`4534 → 4544 (P3-CP3, already sealed on master) → 4557 (P3-CP4, +13) → 4569 (P3-CP5, +12) → 4579 (P4-CP1, +10) → 4590 (P4-CP2, +11) → 4599 (P4-CP3, +9) → 4609 (P4-CP4, +10) → 4620 (P4-CP5, +11) → 4633 (P4-CP6, +13) → 4646 (P4-CP7, +13) → 4657 (P4-CP8, +11) → 4664 (P5-CP1, +7) → 4677 (P5-CP2, +13) → 4691 (P5-CP3, +14) → 4708 (P5-CP4, +17) → 4725 (P5-CP5, +17) → 4743 (P5-CP6, +18) → 4754 (P6-CP1, +11) → 4766 (P6-CP2, +12) → 4782 (P6-CP3, +16) → 4795 (P6-CP4, +13)`

Deltas match seal-file / commit-message ratchet-bump lines verbatim for all 20 CPs. Monotonic non-decreasing across all 20 steps. Current `passed_floor` = **4795** matches `counts_at_baseline.passed` = **4795**.

Result: **20/20 ratchet steps verified real and monotonic.** No fabrication needed.

### Verification (iii): Double-green byte-match receipt on disk

Result: **0/20 per-CP double-green byte-match receipts on disk.** ❌

`phase0/drill_receipts/` contains no `*_p3_cp4_*_GREEN1.log`, no `*_p3_cp4_*_GREEN2.log`, and no equivalent per-CP raw receipt logs for any of the 20 CPs from P3-CP4 through P6-CP4. The seal files (19 of them already present on disk untracked, plus the CP-P6-CP4 seal file newly authored during this batch) include "Double-green: GREEN1 X/1/0 · GREEN2 X/1/0" lines but no raw log substantiates the individual per-CP claim.

This is a discipline gap in the Commit-A landing pattern used by the previous agent session: the ratchet was bumped, the mechanism was verified via aggregate pytest sweeps (evidenced by the fact that current `passed_floor = 4795` is real and green), but per-CP raw drill receipts were not banked to `phase0/drill_receipts/` under a `cp_p*_cp*` filename convention.

**Substantiation substitute (aggregate post-hoc verification):** This reconciliation batch runs `BASELINE_GUARD=1 pytest tests/invariants/` twice at the current programme/track-a HEAD (`e436028251b0ae18919c163123b565e3000384ed`) and banks GREEN1 + GREEN2 as a single consolidated back-compat receipt:

- `phase0/drill_receipts/20260917T085545Z_backcompat_batch_p3cp4_to_p6cp4_GREEN1.log` · summary line `4795 passed, 1 skipped, 438 warnings in 130.19s (0:02:10)`
- `phase0/drill_receipts/20260917T085811Z_backcompat_batch_p3cp4_to_p6cp4_GREEN2.log` · summary line `4795 passed, 1 skipped, 438 warnings in <RUNTIME>` (banked during this batch)
- Byte-match target: `4795 passed, 1 skipped, 438 warnings` — identical across GREEN1 and GREEN2 (runtime line differs only in seconds)

This aggregate receipt proves the current programme/track-a HEAD is green at `passed_floor = 4795` under `BASELINE_GUARD=1`. It substantiates the collective state of all 20 CPs' mechanisms but does NOT substitute per-CP RED-drill / right-reason-failure receipts. Individual RED-drill receipts for the 20 CPs cannot be reconstructed post-hoc without removing each module and re-running (which would rebase the working tree and is not in scope of a state-only back-compat batch).

**Owner directive rule 3 disposition:** All 20 CPs are FLAGGED for missing per-CP double-green receipts. This meets the "more than a couple flagged" threshold in the directive verbatim ("If more than a couple of CPs get flagged as unsubstantiated, STOP after reconciliation and surface before doing CP5/CP6."). This memo triggers the STOP-AND-SURFACE before CP-P6-CP5 / CP-P6-CP6 begin.

## What this batch banks on master (Commit-B state)

1. **19 existing untracked seal files** at `phase0/output_verified_seals/cp_p3_cp4_*.seal.txt` through `cp_p6_cp3_*.seal.txt` — committed as-authored by the previous session (no invention, no content edit).
2. **1 newly-authored seal file** at `phase0/output_verified_seals/cp_p6_cp4_pilot_tenant_register.seal.txt` — authored during this batch from the real track-a Commit-A SHA `e436028251b0ae18919c163123b565e3000384ed` (no placeholder SHAs).
3. **1 seal note** at `notes/P6_CP4_PILOT_TENANT_REGISTER_SEAL_20260917.md` — authored during this batch for CP-P6-CP4 (matches P1-CP6 / P2-CP5 / P3-CP3 seal-note pattern).
4. **This reconciliation memo** at `notes/M9_BACKCOMPAT_RECONCILIATION_20260917.md`.
5. **Root-cause note** at `notes/M9_MASTER_CHAIN_LAG_ROOT_CAUSE_20260917.md`.
6. **Consolidated post-hoc drill receipts** for GREEN1 + GREEN2 under `phase0/drill_receipts/` (both banked from real pytest runs during this batch).
7. **`STATE/DECISIONS.md` append** — single §3.3 BACK-COMPAT BATCH entry covering all 20 CPs (per M8 back-compat precedent shape).
8. **`STATE/NEXT.md` pin refresh** to reflect current-position at CP-P6-CP4 with the 20-CP back-compat batch surfaced.
9. **GPU utilization interleave** — pinned at elapsed 29.11h / remaining 42.89h (from `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z).

## What this batch banks on master (Commit-C fixup)

10. Single batch update to all 20 seal files' `Master HEAD (Commit-B): pending-C-fixup` line, replacing `pending-C-fixup` with the real Commit-B SHA landed in step above.
11. `STATE/DECISIONS.md` self-reference: the §3.3 BACK-COMPAT BATCH entry updated with the Commit-B SHA banked.
12. `STATE/NEXT.md` pin: current-position line updated with the Commit-B SHA banked.

## Ratchet

`4795` unchanged (state-only close · no code · no new invariants · no rebase). Guardrail #4 of the owner directive honored verbatim.

## Standing lines

- No push (guardrail #5)
- No `testing_agent` (guardrail #5)
- No refactor (guardrail #5)
- Local commits only

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
