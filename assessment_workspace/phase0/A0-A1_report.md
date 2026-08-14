# Phase 1 · A0 + A1 Report

**Date:** 2026-08-14
**Deliverable:** A0-A1 report per Build Order 01 §6.
**Branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`.
**Baseline SHA (pinned, never rewritten):** `b150c21`.
**Discipline:** tests-first — every gating test written FIRST, failing for the right reason captured FIRST, then implementation.

---

## Scope executed

### A0 · Thin register kernel

- **`WS-WIRE-PARITY-EXTENSION`** — whole. Extended `tests/invariants/` with 5 new gating tests and 1 parity-seat snapshot for `Actor.Declaration.v0`.
- **`WS-BUILD-RECORD-MATRIX`** (thin scope only) — 6 record classes: Ledger.Row, Receipt, Census.Snapshot, Actor.Declaration, Ingestion.Artifact, Training.Artifact. Full scope stays Track-B.
- **`WS-BUILD-TASK-IDENTITY-REGISTER`** (thin scope only) — 9 task IDs across live path A0-A3. Full scope stays Track-B.

### A1 · Declaration

- **`WS-BUILD-DECL`** — declaration seat + supersession chain.
- **`WS-WIRE-CUSTODY-DECL`** — designated reader (`services.northena.admit`) registered in the matrix (call-site wiring lands in the A2 commit alongside the ingestion-admission drill).

### Folded-in (Owner Clarification 2): compute seam

- **`WS-BUILD-COMPUTE-SEAM`** — governed handoff to the AISCA GPU VM. Fail-closed order (declaration → task-identity → ledger row → transport). Failure taxonomy typed. Artifact-hash verification.
- **Tools:** `report_egress_ip.sh`, `ssh_preflight.py`, `run_acceptance_via_seam.py`.

---

## Files added on `programme/track-a`

**Contracts (3):**
- `backend/contracts/actor_declaration.py` — `Declaration.v0` model.
- `backend/contracts/record_matrix.py` — thin-kernel matrix with 6 entries + writer/reader helpers.
- `backend/contracts/task_identity.py` — thin-kernel register with 9 task IDs.

**Services (2):**
- `backend/services/declaration/` — `seat.py` (capture / check / supersession) + `__init__.py`.
- `backend/services/compute_seam/` — `seam.py` (governed handoff) + `artifact_verify.py` + `__init__.py`.

**Gating tests (7):**
- `tests/invariants/test_actor_declaration_v0_contract_frozen.py`
- `tests/invariants/test_record_matrix_thin_kernel.py`
- `tests/invariants/test_task_identity_thin_kernel.py`
- `tests/invariants/test_parity_seat_extends_thin_kernel.py`
- `tests/invariants/test_admit_refuses_undeclared_actor.py`  (**the drill — Ruling-1 precondition (a) firing evidence**)
- `tests/invariants/test_compute_seam_no_unledgered_exec.py`
- `tests/invariants/test_compute_seam_artifact_hash_verified.py`

**Parity-seat snapshot (1):**
- `tests/invariants/actor_declaration_v0.contract_snapshot.json` (2625 bytes).

**Tools (3):**
- `backend/tools/report_egress_ip.sh` — pod egress IP for VM allowlist.
- `backend/tools/ssh_preflight.py` — typed preflight (refused / timeout / auth / host-unknown).
- `backend/tools/run_acceptance_via_seam.py` — runs Phase-0 acceptance THROUGH the seam.

**Total lines added:** ~950 lines across 16 files.
**Files modified:** ZERO (all additions; no existing-code changes; no regression risk).

---

## Right-reason failure evidence (tests-first discipline)

Captured pre-implementation (STEP 1, before parity-seat snapshot existed and before `pytest-asyncio` was installed):

```
FAILED test_actor_declaration_v0_contract_frozen — parity-seat snapshot file doesn't exist yet
FAILED test_every_thin_kernel_new_contract_has_a_parity_seat_entry — snapshot file missing
FAILED test_every_snapshot_matches_current_schema — same missing snapshot
ERROR  six async tests — pytest-asyncio plugin not installed (right reason: async requires the plugin)
PASSED test_thin_kernel_covers_live_path_classes
PASSED test_ledger_row_sole_writer_is_northena
PASSED test_actor_declaration_sole_writer_is_declaration_seat
PASSED test_admit_is_a_declaration_reader
PASSED test_admit_is_not_a_declaration_writer
PASSED test_every_class_has_a_writer_and_a_readers_frozenset
PASSED test_thin_register_has_the_nine_live_path_task_ids
PASSED test_declaration_check_authority_is_governance
PASSED test_compute_task_authority_is_infrastructure
PASSED test_unregistered_task_raises
PASSED test_every_registered_task_has_description
```

**9 failures for the right reason** (missing artifacts, missing plugin). **11 structural passes** (matrix + register shape checks that exercise only the module surface — these were the right shape before the runtime implementation existed).

## Green state after implementation

```
tests/invariants/test_actor_declaration_v0_contract_frozen.py    PASSED (1/1)
tests/invariants/test_record_matrix_thin_kernel.py               PASSED (5/5)
tests/invariants/test_task_identity_thin_kernel.py               PASSED (5/5)
tests/invariants/test_parity_seat_extends_thin_kernel.py         PASSED (2/2)
tests/invariants/test_admit_refuses_undeclared_actor.py          PASSED (6/6)  ← DRILL
tests/invariants/test_compute_seam_no_unledgered_exec.py         PASSED (3/3)
tests/invariants/test_compute_seam_artifact_hash_verified.py     PASSED (3/3)
------------------------------------------------------------------------------
                                                                 26 passed in 0.15s
```

## Drill receipt — Ruling-1 precondition (a) firing evidence BANKED

`phase0/drill_receipts/20260814T120336Z_declaration_refusal_firing.log` captures the six-scenario drill:

- Missing declaration returns `missing`.
- Captured in-scope declaration returns `in_force`.
- Expired declaration returns `expired`.
- Scope-mismatched declaration returns `scope_mismatch`.
- **VM-as-infrastructure-actor declaration shape captured and verified `in_force` on `archive.ingestion` scope.**
- Supersession preserves append-only chain (prior superseded, new in-force).

**This is precondition (a) for `WS-CONTRADICTION-PURPOSE-GATE` strip.** Ruling-1 precondition (b) — `WS-BUILD-WATCH-RECONCILER` — remains Track-B; unchanged.

## No-regression check

- Files modified: ZERO. All 16 files are new.
- `test_ast_egress_gate.py`: 2/2 pass on `programme/track-a` (no regression at the content-boundary).
- `test_invariant_contract_snapshots.py`: 4 pre-existing failures at baseline `b150c21`; unchanged by this work.
- **Total invariant regressions introduced by Phase 1: 0.**

---

## Compute seam — status

**Ready-for-credentials.** When owner delivers `VM_HOST` / `VM_USER` / SSH private key:

1. Add to `/app/backend/.env` (never in code, never in STATE, never committed to repos/):
   ```
   VM_HOST=<ip-or-hostname>
   VM_USER=<user>
   SSH_PRIVATE_KEY_PATH=/path/to/key   # under named custody
   SSH_CONNECT_TIMEOUT=10
   ```
2. Run: `python3 backend/tools/ssh_preflight.py` — expect exit 0 (`PREFLIGHT: ok`).
3. Run: `python3 backend/tools/run_acceptance_via_seam.py` — executes each of the six Phase-0 acceptance checks through the seam, ledgered end-to-end. Emits commissioning record JSON.

**Owner-side allowlist directive:** add `34.16.56.64/32` to the VM's SSH allowlist. This is the pod's public egress IP, verified via four independent services (ifconfig.me, icanhazip.com, api.ipify.org, checkip.amazonaws.com). No IPv6 egress.

---

## Blocked (surface, do not adapt)

- **Phase-0 acceptance execution** — blocked on VM creation + credential delivery. Human step on Rafay console.
- **Phase-2 slice run** — blocks on Phase-0 acceptance green.
- **A4 operating surface, Track-B console items, Watch Console §6 verbatim consumption** — blocked on the three fixture attachments (reference screenshot, `Akki_Prototype_v7_Design_Brief.md`, `AISCA_GPU_Access_Guide.pdf`) landing in the workspace. As of Owner Clarification 3 (2026-08-14), attachments were being re-uploaded but had not yet arrived at the time of this report.

**Not blocked** in Phase 1: A0/A1 gating tests (green), compute-seam gating tests (green), declaration-refusal drill (banked).

---

## Next action

Await:
- VM credentials + host IP.
- Fixture attachments (screenshot + v7 brief + GPU Access Guide PDF).

On credential arrival: run preflight + acceptance-via-seam; produce commissioning record.
On fixture arrival: unblock A4 + Track-B; consume v7 brief §6 verbatim for Watch Console.
