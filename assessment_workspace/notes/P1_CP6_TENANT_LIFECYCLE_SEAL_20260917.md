READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP6 · M9 · Platform-layer tenant lifecycle FSM · seal note · 2026-09-17T~04:55Z

**Milestone:** M9 · P1 · Foundation. **CP:** P1-CP6 (**LAST CP of P1 · P1 COMPLETE**).
**Track-a HEAD:** `07fccbd0f142f0a58e7972577750aa840516e642` (Commit-A).
**Ratchet:** 4460 → **4468** (+8).

## Anchor
§4.7 verbatim tenant lifecycle:

    provisioning → sandbox_active → production_active → suspended
                                                     → offboarded
    suspended     → production_active (unsuspend) OR offboarded
    offboarded    → (terminal · irreversible)

§4.4: promotion `sandbox_active → production_active` requires `tenant_owner + platform_operator` joint approval — recorded as `approver_refs` tuple on the `TenantLifecycleTransition` carrier · **NOT enforced here** · caller composes via CP-P2-CP1 role-registry (P2 scope).

§4.7 effects on entry to `suspended`: sessions revoked · jobs halted · allocations released · data retained.
§4.7 effects on entry to `offboarded`: control-plane metadata + Syni-hosted derived artefacts deleted within 30 days · data-plane certs revoked · allocation returned.

Effects tracked as OPEN str refs in `effects_refs: Tuple[str, ...]` on the Transition carrier — enforcement is composed by downstream CPs (P4 allocation return · P5 artefact delete · P6 cert revocation).

## Mechanism
Preventive-charter FSM at `services/platform_control_plane/tenant_lifecycle.py`:

- `TENANT_LIFECYCLE_ANCHOR` — verbatim §4.7 quote (module source).
- `TENANT_LIFECYCLE_STATES` — tuple of 5 OPEN str.
- `TENANT_LIFECYCLE_TERMINAL_STATES` — tuple = `("offboarded",)`.
- `TENANT_LIFECYCLE_TRANSITIONS` — tuple of 8 (source, target) OPEN str pairs verbatim from §4.7.
- `TenantLifecycleTransition` — frozen dataclass 6 exact-order fields (`tenant_id: str · source_state: str · target_state: str · reason_ref: str · approver_refs: Tuple[str, ...] · effects_refs: Tuple[str, ...]`). Ownership isolation at `tenant_id` index 0 — composition surface for CP-P1-CP1 cross-tenant refusal.
- `assess_transition_drift(*, transitions)` — pure function returning sorted tuple (by `(tenant_id, source_state, target_state)`) of drift entries (terminal-outbound OR illegal-pair).
- `assert_transition_valid(*, transition)` — preventive-charter refusal wrapper · terminal check fires **FIRST** (fail fast) → `TerminalStateOutboundRefused` · then matrix check → `IllegalTransitionRefused` · returns `None` on admit.
- Refusal classes: `TenantLifecycleTransitionRefused` (root) + `IllegalTransitionRefused` + `TerminalStateOutboundRefused`. COUNTS-only exception messages (never state values or `tenant_id` in exception body).

## Invariants (8)
1. `test_module_fabric_present_and_all_exports_match` — 10-name `__all__`.
2. `test_lifecycle_states_and_terminal_are_frozen_tuples_of_open_str` — 5 states · terminal = `('offboarded',)`.
3. `test_lifecycle_transitions_matrix_matches_4_7_verbatim` — 8 (source, target) pairs exactly.
4. `test_tenant_lifecycle_transition_frozen_shape` — 6 exact-order fields.
5. `test_assess_transition_drift_returns_sorted_tuple` — determinism + all-ok + empty.
6. `test_assert_transition_valid_refuses_on_illegal_and_terminal` — 3 refusal classes · terminal fires first.
7. `test_assert_transition_valid_permits_all_legal_pairs_deterministic` — every legal pair admits.
8. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports` — anchor present · 21-token grep-negative · zero data-plane imports.

## Double-green byte-match under `BASELINE_GUARD=1`
GREEN 1 `4468 passed / 1 skipped / 0 failed in 124.37s` + GREEN 2 `4468 passed / 1 skipped / 0 failed in 124.54s` (count byte-identical across runs).

## §3.3 3-commit protocol
- Commit A `07fccbd0f142f0a58e7972577750aa840516e642` (track-a) ✅.
- Commit B `5b7944d1bd417f66fb2e2303c8e3144b80ec45b0` (master) ✅.
- Commit C on `master` this-turn (fixup · banks Commit-B SHA).

## CONTRACT-MODELED items enabled
- **Item 12** · 30-day irreversible offboarding delete · real wall-clock scheduler. Terminal-state invariant shaped at carrier layer via `TerminalStateOutboundRefused`. The 30-day delete itself is a downstream P5 CP.

## GPU utilization interleave at seal boundary
Elapsed **24.22 h** · remaining **47.78 h**. Both hosts `sampler_alive` + `workload_alive`. `akki-vm` telemetry_samples=592 bench_iters=2902 (per_gpu=2). `akki-vm-ii` telemetry_samples=586 bench_iters=2902 (per_gpu=2). Zero synthetic burn · no anomalies · in-perimeter. Reports regenerated at `/app/frontend/public/audit/GPU_UTILIZATION_72H.{md,json}`.

## M9 Phase P1 COMPLETE — 6/6 CPs sealed
| CP | Module | Ratchet | Track-a Commit-A |
|----|--------|---------|------------------|
| CP-P1-CP1 · tenant-context enforcement | `services/platform_control_plane/tenant_context.py` | 4433→4440 (+7) | `e697ba63a9f5aa16065552109d2a86b6e17332c2` |
| CP-P1-CP2 · tenant entity carrier | `services/platform_control_plane/tenant_entity.py` | 4440→4445 (+5) | `95fbd8ebcd9f785927c4237363ec052ff6960678` |
| CP-P1-CP3 · workspace entity carrier | `services/platform_control_plane/workspace_entity.py` | 4445→4450 (+5) | `1f32d8d18dd1db73ad28978389b38c1cd61335cf` |
| CP-P1-CP4 · user entity carrier | `services/platform_control_plane/user_entity.py` | 4450→4455 (+5) | `711817de204aef74f78ca57a343658f50c26234f` |
| CP-P1-CP5 · service-account entity carrier | `services/platform_control_plane/service_account_entity.py` | 4455→4460 (+5) | `a2857843fa8f80dde6330a926245ef02b930aeef` |
| CP-P1-CP6 · tenant lifecycle FSM | `services/platform_control_plane/tenant_lifecycle.py` | 4460→4468 (+8) | `07fccbd0f142f0a58e7972577750aa840516e642` |

**Cumulative P1 ratchet delta:** +35 monotonic-up · zero rollback.
**CONTRACT-MODELED items enabled across P1:** items 6 (PKI cert issuance) · 12 (30-day irreversible offboarding delete) · 15 (storage namespaced by tenant_id at bucket/prefix/schema).

## Next
STOP. Report P1 completion to owner. Await explicit owner "go" before starting P2 (RBAC · 7 roles · deny-by-default · action × resource × scope · session/break-glass).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
