# FE-DISPATCH-READY · R-91 CP-APP-JS-UNIFY

**Status:** LOWERED at 2026-09-21T03:23:15Z
**Raised at:** 2026-09-20T23:58:00Z
**Lowered by:** main-agent Autopilot (R-91 CEREMONY-OPEN commit · Phase 2 blocker transferred from FE specialist to Canon 3 §24 ceremony countdown)
**Delivery outcome:** SUCCESS · specialist landed twice · second landing (`8ff2f6737` on /app main · merged App.js sha `90c8956d…` @ 1108 lines) passes shadow-mirror adjudication cleanly (63 net-new failures cleared · 2 v8-cascade wrapped baselines remain retiring at ceremony apply)
**Wave:** R-91 CP-APP-JS-UNIFY (⏳ CEREMONY-IN-FLIGHT · APPLY 2026-09-23T03:23:15Z)

---

## What this flag means

Phase 1 of R-91 is complete. The FE landing spec and its binding HUNT receipt are authored, banked, and byte-identically committed on `master` alongside the R-91-PHASE-1-PINS block, the STATE/DECISIONS.md opening banking, and the STATE/NEXT.md IN-FLIGHT marker. **The FE specialist can be dispatched from the spec verbatim the moment this flag is read.**

Phase 1 lands STATE ONLY. `programme/track-a` is untouched (HEAD stays at `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac`, R-92 Commit-A). `/app/frontend/**` is untouched. `notes/ORCH_BOOT.md` is untouched (ratchet unchanged at `5695 pass / 5 fail / 1 skip`).

## Dispatch package pointers

The FE specialist reads these three files, in this order:

1. `STATE/STANDING_ORDERS.md` — permanent law (Standing Order · SO §2.5, §3, §3.3, §3.8, §6.2, §6.4, §6.7).
2. `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` — R-91 closure card (contract · ratified 2026-09-20T21:55:00Z · sha256 `667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61`).
3. `phase0/specs/r91_cp_app_js_unify_spec.md` — this-Phase-authored landing blueprint (byte-identity direction, retirement plan, Option A/B/C surface for the CP10 non-vacuous half, discipline invariants, acceptance protocol).
4. `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md` — HUNT receipt (ground truth for every claim in the spec).

## What Phase 2 must deliver

- Byte-identity: `sha256(/app/frontend/src/App.js) == sha256(pod_shell/frontend/src/App.js)` AND `pages/**` mirror.
- CP10 non-vacuous: harness receipt regenerated with `dummies_declared > 0`, `marked_slots_count > 0`, `per_rule` non-empty (Option A/B choice — specialist proposes, owner adjudicates).
- 5 baseline entries retired atomically (mirror-drift 3 + v8-cascade 2 · both fields set to empty in the same commit as the baseline shrink).
- BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 match.
- 3-Commit Seal (A code · B state · C fixup) per SO §3.3.

## What Phase 2 must NOT do

- Edit `/app/frontend/**` in the wrong direction (spec §1 verbatim: "`/app/frontend/**` → `pod_shell/frontend/**`, NEVER the other way").
- Silently rebaseline. Both `counts_at_baseline.passed` and `passed_floor` bump together (CCS2 lesson).
- Push to any remote (zero-push discipline · no remotes configured).
- Use `testing_agent` (STRICTLY BANNED · terminal `pytest` only).
- Refactor sealed contracts/writers/tests (SO §3.8 additive-only).

## Handoff protocol

Owner dispatches `phase0/specs/r91_cp_app_js_unify_spec.md` verbatim to the FE specialist. The specialist lands per spec §4 (acceptance protocol) and §4.5 (3-Commit Seal). Owner verifies at spec §8 (handoff protocol).

---

**This flag lowers when Phase 2 seals.** At the moment of the R-91 SEALED marker in STATE/NEXT.md and the milestone_status flip in the R-91 closure card, this note is archived to `phase0/spec_hunt_receipts/<utc>_r91_phase_1_dispatch_flag_lowered.md` (or equivalent archive location) and the FE-DISPATCH-READY status flips to LOWERED in the next STATE/DECISIONS.md append.
