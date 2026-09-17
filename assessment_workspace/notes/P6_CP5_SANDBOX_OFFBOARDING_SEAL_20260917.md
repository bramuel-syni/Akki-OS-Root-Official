READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P6-CP5 · M9 · Platform-layer sandbox_offboarding · seal note · 2026-09-17T~09:25Z

**Track-a HEAD:** `2e82e4f`. **Ratchet:** 4795 → **4809** (+14).

## Anchor

§4.7 tenant lifecycle terminal state `offboarded` + Row 210 verbatim: *"30-day irreversible-delete contract; refusal on missing cert-revocation / allocation-return / artefact-delete evidence refs."*

## Mechanism

`services/platform_control_plane/sandbox_offboarding.py` ·
- `SANDBOX_OFFBOARDING_ANCHOR` module-level verbatim anchor string (§4.7 + Row 210 verbatim + item-12 CONTRACT-MODELED note)
- `SANDBOX_OFFBOARDING_RECORD_FIELDS = ("id", "tenant_id", "cert_revocation_ref", "allocation_return_ref", "artefact_delete_ref", "initiated_at", "committed_at")` verbatim 7-tuple
- `SandboxOffboardingRecord` frozen dataclass 7-carrier all str OPEN
- `assert_sandbox_offboarding_valid(*, record)` preventive-charter refusal order fail-fast:
  1. `cert_revocation_ref` empty → `MissingCertRevocationEvidenceRefused`
  2. `allocation_return_ref` empty → `MissingAllocationReturnEvidenceRefused`
  3. `artefact_delete_ref` empty → `MissingArtefactDeleteEvidenceRefused`
- Returns `None` on admit. `SandboxOffboardingRefused` root · 4 refusal classes total. COUNTS-only messages · positional-index refusal bodies.

## Invariants (14)

Module fabric · fields tuple exact-order · frozen 7-carrier shape · refusal class hierarchy · missing-cert-first refusal · missing-alloc-second refusal · missing-artefact-third refusal · admit all three refs present · ownership isolation at tenant_id index 1 · COUNTS-only refusal messages · zero closed enum type · zero domain tokens (21-token obfuscated pair-halves grep) · zero data-plane imports · SANDBOX_OFFBOARDING_ANCHOR references §4.7 + Row 210 + 30-day + three evidence categories verbatim.

## Double-green (R-5 compliant · captured at seal time)

- **GREEN1**: `phase0/drill_receipts/20260917T092056Z_p6_cp5_sandbox_offboarding_GREEN1.log` → `4809 passed, 1 skipped, 438 warnings in 130.58s (0:02:10)`
- **GREEN2**: `phase0/drill_receipts/20260917T092325Z_p6_cp5_sandbox_offboarding_GREEN2.log` → `4809 passed, 1 skipped, 438 warnings in 130.99s (0:02:10)`
- **Byte-match target on counts**: `4809 passed, 1 skipped, 438 warnings` — MATCHED

## RED drill (pre-implementation)

`phase0/drill_receipts/20260917T091401Z_p6_cp5_sandbox_offboarding_RED.log` — 14 failed with `ModuleNotFoundError: No module named 'services.platform_control_plane.sandbox_offboarding'` (right-reason).

## Delta sweep (pre-ratchet-bump)

`phase0/drill_receipts/20260917T091806Z_p6_cp5_sandbox_offboarding_DELTA_GUARD0_v2.log` → `BASELINE_GUARD=0` → 4809 passed / 1 skipped / 0 failed. Delta from floor 4795 = **+14 exact**, matching the 14 new invariants. No silent rebaselining.

## Self-catch discipline honored (case-agnostic doctrine)

Initial DELTA sweep caught two right-reason failures that the tests-first discipline is designed to surface:
1. `test_p6_cp5_zero_domain_tokens` caught its OWN test-source containing `"kikuyu"` in the `DOMAIN_TOKENS_21` tuple literal → fixed by obfuscating to pair-halves rebuilt at runtime (matches CP-M7-W2-CP1 precedent 2026-09-16). **The mechanism enforced the doctrine, not the author's vigilance.**
2. `test_decisions_carries_pointer_near_bottom` caught the DECISIONS.md ratification entry not ending with the standing-orders pointer → fixed by appending the pointer line at the bottom.

Both fixes landed pre-Commit-A. Second DELTA sweep clean at 4809.

## §3.3

- **A** `2e82e4f` ✅ landed on `programme/track-a` 2026-09-17T~09:25Z.
- **B** this-turn on master (state + seal file + this seal note + DECISIONS append + NEXT pin + drill receipts + GPU util).
- **C** this-turn fixup on master (self-reference · banks Master HEAD in seal file + DECISIONS + NEXT).

## GPU util

Elapsed **~29.6 h** · remaining **~42.4 h** (per `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z + pytest campaign since · both hosts sampler_alive+workload_alive · in-perimeter · no anomalies).

## CONTRACT-MODELED items enabled

- **Item 12** · 30-day irreversible offboarding delete (§4.7 · depends on Real storage + wall-clock scheduler). Combined P1-CP6 TenantLifecycleFSM (5-state lifecycle with `offboarded` as terminal) + this CP-P6-CP5 evidence carrier (three evidence refs + missing-evidence refusal) shape-freeze the entire offboarding contract at the carrier layer. Real wall-clock 30-day countdown + real storage-object-list-after-delete assertion + real cert-authority-revoke + real allocation-ledger-return are all downstream bind-only changes — no refactor.

## R-5 compliance

Per DECISIONS.md §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17T~09:15Z verbatim: this seal file's Double-green line is composed only after both raw byte-match logs exist on disk at the referenced timestamps. Verified on disk pre-authorship. No fabrication. First CP to be sealed under R-5 discipline enforced-from-forward.

## Standing lines

no biometric material · no enforcement hard-gate · preventive-charter · caller invokes · synthetic fixtures · no speculative shapes · upgrade path to hard-gate preserved by construction · zero closed enum type · zero domain tokens · zero data-plane imports.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
