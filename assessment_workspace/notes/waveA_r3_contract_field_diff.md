# R3 · Four Lifted Wizard Contracts · Field-by-Field Diff vs Akki-OS-V1

Owner directive 2026-08-26 verbatim:
> "USE the four lifted contracts (wizard_commit_state, operator_turn, agent_assumption, committed_value) — diff them field-by-field against Akki-OS-V1 canonical shapes first (the audit gap you flagged)."

## Result: contracts are byte-identical LIFT.

```
$ diff repos/Extraction-Akki/backend/contracts/wizard_commit_state.py \
       repos/Akki-OS-V1/backend/contracts/wizard_commit_state.py
[no output]

$ diff repos/Extraction-Akki/backend/contracts/agent_assumption.py \
       repos/Akki-OS-V1/backend/contracts/agent_assumption.py
[no output]

$ diff repos/Extraction-Akki/backend/contracts/operator_turn.py \
       repos/Akki-OS-V1/backend/contracts/operator_turn.py
[no output]

$ diff repos/Extraction-Akki/backend/contracts/committed_value.py \
       repos/Akki-OS-V1/backend/contracts/committed_value.py
[no output]

$ diff repos/Extraction-Akki/backend/tests/invariants/wizard_commit_state.contract_snapshot.json \
       repos/Akki-OS-V1/backend/tests/invariants/wizard_commit_state.contract_snapshot.json
[no output]

$ diff repos/Extraction-Akki/backend/tests/invariants/agent_assumption.contract_snapshot.json \
       repos/Akki-OS-V1/backend/tests/invariants/agent_assumption.contract_snapshot.json
[no output]

$ diff repos/Extraction-Akki/backend/tests/invariants/operator_turn.contract_snapshot.json \
       repos/Akki-OS-V1/backend/tests/invariants/operator_turn.contract_snapshot.json
[no output]

$ diff repos/Extraction-Akki/backend/tests/invariants/committed_value.contract_snapshot.json \
       repos/Akki-OS-V1/backend/tests/invariants/committed_value.contract_snapshot.json
[no output]
```

All eight files (four .py + four .contract_snapshot.json) are byte-identical between Extraction-Akki `programme/track-a` HEAD `369f9b8` and Akki-OS-V1's donor tree.

## Verbatim shapes (from the on-disk contracts)

### WizardCommitState_v0

Config: `extra="forbid"`, `frozen=True`.

Fields:
- `session_id: str` (min_length=1) — "uuid-like; unique per wizard session."
- `trace_id: str` (min_length=1) — "Northena/Solva correlator; shared with downstream admission."
- `variant: Literal["operator", "buyer"]` — "Discriminator; immutable within session."
- `initiated_at: str` (min_length=1) — "ISO-8601 UTC."
- `committed_at: Optional[str]` (default None) — "ISO-8601 UTC. Set at freeze; None while session is open."
- `turns: List[OperatorTurn_v0]` (default_factory=list) — "Append-only turn ledger."
- `agent_assumptions: List[AgentAssumption_v0]` (default_factory=list) — "Append-only agent-inference ledger."
- `committed_values: Dict[str, CommittedValue_v0]` (default_factory=dict) — "Keyed by dotted-path field name; each value carries the source-tag anti-laundering seam."
- `feasibility_history: List[str]` (default_factory=list) — "Per-turn feasibility_snapshot_ref pointers. Guard 3 enforcement point."
- `license_class: Optional[str]` (default None) — "E1 Option C primary-arm value."
- `frozen_objective_ref: Optional[str]` (default None) — "Set at freeze; refs the minted ObjectiveRequest_v2's objective_id."

Freeze-time invariants (`@model_validator(mode='after')`):
- **Guard 1** (Owner ruling §3.3): every operator-mandatory field (`reach`, `output.form`, `output.consumer`, `output.grain`, `output.standard`, `envelope.done_condition`, `envelope.budget`, `envelope.lawful_basis`) MUST have `source == "operator_supplied"` at freeze. Refuse otherwise.
- **Guard 2** (Owner ruling §3.3): every `agent_assumed` value MUST reference an existing entry in `agent_assumptions[]`. Orphan refs refuse.
- **Guard 3** (Owner ruling §3.3): every OperatorTurn_v0 has a non-empty `feasibility_snapshot_ref` (structural via `min_length=1`).

**Alignment with Canon 5 §14 verbatim (lines 191-197)**:
Canon 5 §14: "Mandatory fields — reach, the four output fields, done-condition, budget, lawful basis — are asked, never pre-filled."
Contract `_OPERATOR_MANDATORY_FIELDS`: `{reach, output.form, output.consumer, output.grain, output.standard, envelope.done_condition, envelope.budget, envelope.lawful_basis}` — 8 fields = reach + 4 output + done-condition + budget + lawful basis. **Exact match.**

Canon 5 §14: "the agent asks for mandatory fields and never proposes on them."
Guard 1 enforces: mandatory fields MUST be `operator_supplied`, not `agent_assumed`. **Structurally enforced.**

Canon 5 §14: "Every turn is grounded in a real estate read; no fabricated availability, ever, under any circumstance."
OperatorTurn_v0.feasibility_snapshot_ref (min_length=1). Guard 3 refuses empty. **Structurally enforced.**

Canon 5 §15: "Frozen is immutable — a changed intent is a new objective."
`extra="forbid", frozen=True` at contract level. **Structurally enforced.**

### OperatorTurn_v0

Config: `extra="forbid"`, `frozen=True`.

- `turn_ref: str` (min_length=1) — "uuid; identifies this turn across the wizard trace."
- `at: str` (min_length=1) — "ISO-8601 UTC."
- `user_content: str` (default "") — "Empty on agent-first ask turns before the user replies."
- `agent_content: str` (default "") — "Empty on user-first turns before the agent replies."
- `feasibility_snapshot_ref: str` (min_length=1) — "Reference to WizardCommitState_v0.feasibility_history[] entry (Guard 3 enforcement point)."

### AgentAssumption_v0

Config: `extra="forbid"`, `frozen=True`.

- `assumption_id: str` (min_length=1)
- `at: str` (min_length=1)
- `field: str` (min_length=1) — "Dotted-path field name (e.g. 'output.grain')."
- `inferred_value: Any` — "Loose-as-frozen."
- `evidence_ref: str` (default "") — "Optional trace pointer."

### CommittedValue_v0

Config: `extra="forbid"`, `frozen=True`.

- `value: Any` — "Loose-as-frozen."
- `source: Literal["operator_supplied", "agent_assumed"]` — "Anti-laundering seam per Owner E3 ruling."
- `operator_turn_ref: Optional[str]` (default None) — "Set iff source='operator_supplied'."
- `agent_assumption_id: Optional[str]` (default None) — "Set iff source='agent_assumed'."
- `committed_at: str` (min_length=1) — "ISO-8601 UTC."

XOR invariant (`@model_validator(mode='after')`):
- Exactly one of `operator_turn_ref` / `agent_assumption_id` MUST be set (never both, never neither).
- `source == "operator_supplied"` ⇒ `operator_turn_ref is not None`.
- `source == "agent_assumed"` ⇒ `agent_assumption_id is not None`.

**Alignment with Canon 5 §9.3 verbatim (lines 141-144)**:
Canon 5 §9.3: "Amber, 11px label weight, attached to any field an agent filled rather than the person. It survives to the commit review unchanged — a value that was agent-assumed at draft time is never quietly reclassified as user-supplied by the act of confirming the screen it appears on."
CommittedValue_v0.source is frozen at construction; can never be silently reclassified. **Structurally enforced.**

## Ancillary state-machine + persistence on disk

`services/wizard/` (also byte-identical LIFT — spot-check confirmed):
- `operator_state_machine.py` (298 LOC)
- `turn_ledger.py` (87 LOC)
- `source_tagging.py` (93 LOC)
- `agent_interface.py` (136 LOC) · `DeterministicStubAgent` per "agent-pluggable-with-stub-agent-first" ruling
- `session_persistence.py` (72 LOC) · Mongo upsert
- `milestones.py` (145 LOC) · Canon 6 §6 five-step handshake
- `admission_handoff.py` (25 LOC) · Phase 5 admission handoff
- `router_shims.py` (128 LOC)

`routers/wizard_operator.py` (527 LOC) exposes the full HTTP surface:
- POST `/api/wizard/operator/session` — 201 with session_id, trace_id, initiated_at, variant.
- POST `/api/wizard/operator/{session_id}/turn` — advance state machine one turn.
- POST `/api/wizard/operator/{session_id}/agent-assumption` — Guard 2 seam.
- POST `/api/wizard/operator/{session_id}/commit-review` — pre-freeze review card.
- POST `/api/wizard/operator/{session_id}/freeze` — commit (Guard 1/2 fire here).
- GET  `/api/wizard/operator/{session_id}` — read state.
- POST `/api/wizard/operator/{session_id}/handoff` — Phase 5 admission.
- GET  `/api/wizard/operator/{session_id}/milestones` — Canon 6 §6.
- POST `/api/wizard/operator/{session_id}/milestones` — advance milestone.
- POST `/api/wizard/operator/{session_id}/milestones/agree` — operator agreement.

`backend/tests/invariants/test_phase_7_stage_b_1_wizard.py` (verified on disk) already covers the Guard 1/2/3 discipline and CommittedValue XOR invariant.

## R3 conclusion

The full Canon 5 §14 wizard mechanism is present on disk in Extraction-Akki, LIFTed verbatim from Akki-OS-V1. **The audit gap was reachability, not contract drift.** R3 remediation is therefore:
1. Wire `routers.wizard_operator` into `pod_shell/backend/server.py` + `/app/backend/server.py` (Ship-Manifest DoD).
2. Build a minimal `CommissionWizard.jsx` frontend surface at `/commission` that renders Canon 5 §14 grammar (chat pane + draft rail + amber chip) against the wizard_operator API.
3. Tests-first with verbatim Canon 5 §14 quotes in docstrings; tests gate the Canon 5 §14 grammar (mandatory fields asked never pre-filled; amber chip on agent-assumed rows; freeze is immutable).
4. Update KNOWN_UNWIRED to remove `routers.wizard_operator`.
5. Log the Canon-5-wins-over-Simplification supersession in DECISIONS.md (already inserted at R1 turn; will land with R3 commit).
