READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ROOT-CAUSE NOTE · Master seal-chain lag from CP-P3-CP3 · 2026-09-17

Banked per owner directive verbatim 2026-09-17 (path (a) guardrail #6): *"Write a short ROOT-CAUSE note (banked to state) explaining how/why the master chain fell behind from CP-P3-CP3, so it doesn't recur."*

## Timeline reconstruction (from-disk evidence only)

**Last clean §3.3 seal-chain state on master:** `7d065efe` (2026-09-17T~05:40Z) · CP-P3-CP3 Commit-C fixup · Master HEAD `29a6da446c4b250cba2c476ad470811dd1699640` banked.

**Track-a activity 2026-09-17T~05:47Z → T~08:45Z** (per `git log programme/track-a`):
- 20 CP-P3-CP4..CP-P6-CP4 Commit-A landings (each with code + tests + ratchet bump + commit message ending "§3.3 · master SHA to land in commit C-fixup").
- Each Commit-A message declares the intent to complete §3.3 (Commit-B on master + Commit-C fixup) but that intent was never landed.

**Master activity 2026-09-17T~05:40Z → T~08:45Z (~3h):** none. Master HEAD did not advance from `7d065efe` during the entire 20-CP Commit-A wave.

**Session boundary suspicion:** the previous agent session either compacted mid-wave or entered a fire-forward pattern that landed track-a Commit-A's rapidly but never returned to close each with Commit-B + Commit-C on master. The user's session-handoff brief 2026-09-17 reported "CP-P6-CP4 COMPLETED (Verified locally, sealed, committed, GPU check-in updated)" — this claim was true for the track-a side (Commit-A landed, ratchet bumped, GPU util regenerated) but false for the master side (no Commit-B, no Commit-C, no seal file for CP-P6-CP4). The brief conflated "sealed" (which requires all three §3.3 commits) with "Commit-A landed on track-a".

## Contributing factors

1. **§3.3 3-commit protocol requires two repos:** Commit-A on `Extraction-Akki/backend/programme/track-a`; Commit-B + Commit-C fixup on `assessment_workspace/master`. Switching working directories between two git worktrees is a discipline burden that accumulates cost across a batch. Under time pressure or context pressure, the master-side commits can be deferred to "end of batch" and then get dropped at a session boundary.

2. **Seal-file placeholder shape hides the drift:** each Commit-A seal file (untracked) carries `Master HEAD (Commit-B): pending-C-fixup` — a valid pre-fixup shape. Nothing in the seal-file writer detects that `pending-C-fixup` has stayed in place across 20 CPs. There's no "linter" that checks the seal-file inventory against DECISIONS.md tail.

3. **Ratchet history writes silently:** the ratchet_history JSON block records `commit: "PENDING"` for each entry — indicating that the entry was banked before the Commit-A SHA was known. This is inverted from the intended flow (bank Commit-A SHA first, then update ratchet). Combined with no post-hoc check that reconciles ratchet_history's `commit: "PENDING"` entries against actual `git log` SHAs, the drift is invisible.

4. **No back-compat check at CP boundary:** each new Commit-A on track-a assumed the master chain was current. Nothing enforced "before starting CP-N+1, verify Master HEAD banks CP-N's Commit-B SHA in seal + DECISIONS + NEXT." The M8 back-compat precedent (owner ruling 2026-09-16T~08:10Z) had already established that master-chain parity matters, but that precedent was for 5 CPs done sequentially with drift caught immediately; the current gap accumulated across 20 CPs before any observer noticed.

5. **No compaction-time boot-ritual seal-chain probe:** SO §1 boot ritual requires reading DECISIONS.md tail + NEXT.md, but neither prescribes running a "master HEAD banks latest track-a CP" check. A recovering agent reads NEXT.md's CP-P3-CP3 pin and continues; only cross-repo probing surfaces the drift.

## Recurrence-prevention rules (proposed · owner-ratifiable · no code)

Recorded as candidate SO amendments — none of these bind until the owner ratifies:

**R-1 · Master-parity check at CP boundary.** Before opening a new Commit-A on track-a for CP-N+1, verify Master HEAD banks the Commit-B SHA for CP-N in each of (a) the seal file at `phase0/output_verified_seals/cp_p*_*.seal.txt`, (b) `STATE/DECISIONS.md` tail, and (c) `STATE/NEXT.md` "CURRENT AS OF" line. If any of (a)/(b)/(c) shows `pending-C-fixup` or a stale SHA, STOP and reconcile before opening CP-N+1.

**R-2 · Seal-file `pending-C-fixup` counter.** Every boot ritual and every pre-CP-open probe counts occurrences of the string `pending-C-fixup` in `phase0/output_verified_seals/`. If the count is > 0, the seal chain is not clean; refuse to open a new CP until Commit-C fixup lands and reduces the count to 0.

**R-3 · Ratchet-history / git-log cross-check.** Every boot ritual runs a probe that walks `tests/invariants/baseline_failures.json` `ratchet_history` from the last-known-clean master HEAD forward and verifies each entry with `commit: "PENDING"` or a real SHA has a matching `git log programme/track-a` entry and a matching seal file. Divergences are surfaced.

**R-4 · Session-handoff brief reconciliation.** When an incoming session receives a brief claiming CP-N is "sealed", the incoming agent's FIRST action is to verify §3.3 3-commit completeness for CP-N on disk before touching any downstream work. "Sealed" without Commit-B + Commit-C fixup on master is a discipline mislabel and must trigger reconciliation before forward progress.

**R-5 · Per-CP drill receipt shape.** Every Commit-A landing must include the two raw drill logs it references in its seal file: `phase0/drill_receipts/<TS>_<kind>_GREEN1.log` and `phase0/drill_receipts/<TS>_<kind>_GREEN2.log`. The seal-file writer should refuse to compose the `Double-green: GREEN1 X/Y/Z · GREEN2 X/Y/Z` line unless both logs exist on disk with the referenced timestamps. This closes the "receipt-line-but-no-log" gap that the 20-CP batch exposed.

None of R-1..R-5 alter existing rules; each is additive discipline. No code changes required — all are procedural / boot-ritual checks that live in `STATE/STANDING_ORDERS.md` (subject to owner ratification).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
