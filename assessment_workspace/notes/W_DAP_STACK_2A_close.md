READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2A_close.md

**Wave.** W-DAP-STACK · Sub-wave 2A · External-party principal + admission.
**Canon anchors.** DAP-Spec DAP-1..4, DAP-12, DAP-24; DAP-Spec §7 (composition); DAP-Spec §9 A5 (slow-play detection); Doc-0 §BR-2.1 (external-party principal class).
**Owner authorisation.** Verbatim 2026-09-13: *"Gate 1 rescinded, Gate 2 - b, Gate 3 - in-block"*. ROLE OVERRIDE rescinded for this session.
**Ratchet.** 3560 → 3570 (+10).
**Track-a commit.** `e578582`.
**Seal.** `phase0/output_verified_seals/wdap_2a.seal.txt`.

---

## §A · Invariants added (9 new · 1 recovered)

| Test | Anchor | What it enforces |
|---|---|---|
| A2-01 · contracts import + forbid_extra | DAP-1..3 | `contracts.dap` imports; `ExternalPartyPrincipal`, `PartyPrincipal`, `GovernancePosture`, `PartyPrincipalKind`, `CumulativeHistoryEntry` exist; `extra="forbid"` on frozen models |
| A2-02 · DAP-1 required fields | DAP-1 verbatim | `ExternalPartyPrincipal` carries all 5 DAP-1 required fields (`legal_identity`, `governance_posture`, `terms_id`, `trust_domain_id`, `admission_mandate`) |
| A2-03 · closed GovernancePosture | DAP-1 | `GovernancePosture` is a closed enum {research, commercial, regulatory, ai_lab} |
| A2-04 · closed PartyPrincipalKind | DAP-2/DAP-3 | `PartyPrincipalKind` is {individual, agent} |
| A2-05 · DAP-3 agent autonomy | DAP-3 | Agent principal without `autonomy_scope` refused; agent WITH scope accepted |
| A2-06 · DAP-12 named authority | DAP-12 | Admission with empty `admitting_authority_id` refused |
| A2-07 · under-organisation | DAP-1 | Party principal for unadmitted org refused |
| A2-08 · DAP-24 fields + R-C2 | DAP-24 | `CumulativeHistoryEntry` carries required fields; `timestamp_iso` description names R-C2 |
| A2-09 · DAP-Spec §9 A5 slow-play | DAP-4 / §9 A5 | Aggregate detection over history triggers above threshold, not per-request |
| **RECOVERED** · ratchet monotonicity segment | Owner Option A ruling | Env-drift-reset entries exempt from pre-reset monotonicity; post-reset resumes |

## §B · Mechanism landed

- `backend/contracts/dap.py` (288 lines · 14 pydantic BaseModels + 4 enums covering DAP-1..30) — previously untracked, now committed.
- `backend/services/dap/admission.py` (101 lines · thin-kernel admission + slow-play detection) — previously untracked, now committed.
- 14 new `.contract_snapshot.json` files banked (primary + 13 secondaries).
- `test_frozen_contract_snapshot_parity.py` updated: `dap.py → external_party_principal.contract_snapshot.json` + 13 secondaries added to `CONTRACT_TO_SNAPSHOT_SECONDARIES`.
- `test_baseline_no_new_breakage.py` updated: monotonicity assertion segments across `env_drift_reset` boundaries per owner Option A.

## §C · Markers held (flip-forbidden)

- **R-C1**: `ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK` binding in `contracts/dap.py` — silent flip forbidden. Rules-Service not yet built (Doc-0 §8 dependency).
- **R-C2**: `MeteredEvent.au_3b_defensible=False` default + `CumulativeHistoryEntry.timestamp_iso.description` names R-C2 — silent flip forbidden. Doc-0 G-8 (reliable time source) still open.
- **DPO-1 linkage**: `controlled` custody-class value maps to DAP R-1 (RATIFIED per C3 batch 2026-09-13). NOT Document 4's enum. Change requires Rules-Service ceremony.

## §D · Discipline receipts

| Kind | Path |
|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T150500Z_wdap_2a_RED.log` (4 failed / 5 passed — right-reason: `ModuleNotFoundError: services.dap.admission`) |
| GREEN 1 | `phase0/drill_receipts/20260913T151600Z_wdap_2a_GREEN1.log` (3570 passed / 1 skipped / 438 warnings / 112.97s) |
| GREEN 2 | `phase0/drill_receipts/20260913T152000Z_wdap_2a_GREEN2.log` (3570 passed / 1 skipped / 438 warnings / 114.52s) |
| **Rider 1** pip freeze | `phase0/drill_receipts/20260913T152100Z_wdap_2a_PIPFREEZE.txt` (187 packages) |
| **Rider 1** collect-only | `phase0/drill_receipts/20260913T152100Z_wdap_2a_COLLECTONLY.txt` (3571 items) |
| Seal | `phase0/output_verified_seals/wdap_2a.seal.txt` |
| Byte-match | Identical modulo wall-time (`diff` on tail excluding time line = clean) |

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Partial** — DAP-1, DAP-2, DAP-3, DAP-4 (spec-level, mechanism landed at thin-kernel grade), DAP-12 (mechanism landed), DAP-24 (schema landed with R-C2 marker acknowledged).
- **Cross-refs pending sub-wave close**: DAP-Spec §9 A5 (slow-play) — mechanism scaffold in place; production-grade requires DAP-4's aggregate-reconstruction check in a later sub-wave.
- **NOT discharged in 2A**: A1 (compute-to-data), A2 (browse boundary), A3 (approval gate), A4 (metering completeness), A6..A10 — these are 2B..2H scope.

## §F · Guardrails held

- ROLE OVERRIDE rescinded 2026-09-13; production code writing authorised for this session only. **Rescission recorded verbatim** in the seal + this note + commit message.
- Local commit only (`programme/track-a` HEAD `e578582`). NEVER pushed.
- No egress. Radio T4 held.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- Rider-2 `ENV-DRIFT-2TESTS-20260913` tracked as open item in `notes/RULING_LEDGER.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
