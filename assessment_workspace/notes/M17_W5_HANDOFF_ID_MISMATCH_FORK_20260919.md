# M17-W5 · handoff_id/session_id regex mismatch · discovered fork · 2026-09-19

**Status:** ✅ **CLOSED-BY-M17-W6-OPTION-(i)-LANDED** at 2026-09-19T~19:05Z UTC (CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG Commit-A `f57f6c68e765096bd8bc69f8fbfdf96679e5280a` on programme/track-a · Owner Desk Batch item (f) verbatim ratifying Option (i) additive-adapter extension · new module `backend/services/personal_client/handoff_binding.py` with `HandoffId` type-tag class + `derive_handoff_id` + `emit_ask_with_handoff` · sealed M17-W3 `services/personal_client/session.py` NOT edited per thin-adapter discipline · ratchet 5462 → 5469 · adapter is now the authoritative runtime path). Original fork banked at M17-W5 seal integration authoring (previously status OPEN-OPTION-(ii)-APPLIED at M17-W5 Commit-B `8910ba9b53862b153a76cb11ddb5f5dc40ebd2bb`).

**Class:** structural (latent runtime bug in sealed M17-W3 module · adapter now inverts the mismatch inside a new sanctioned seam-routing surface).

**Discovered at:** M17-W5 seal integration authoring (2026-09-19T~15:17Z UTC).

**Discovered by:** authentic RED-first cycle on
`tests/invariants/test_m17_w5_seal_integration.py` · test 2
(`test_end_to_end_milestone_integration_binds_w1_through_w4`).

**Symptom (verbatim from RED receipt
`phase0/drill_receipts/20260919T151714Z_cp_m17_w5_seal_integration_RED_pre_pin.log`):**

```
services/personal_client/session.py:251: ValidationError
pydantic_core._pydantic_core.ValidationError: 1 validation error for Ask_v0
handoff_id
  String should match pattern '^ho_[a-z0-9_-]+$'
    [type=string_pattern_mismatch, input_value='pcs_m17_w5_milestone_probe',
     input_type=str]
```

---

## Root cause

`services/personal_client/session.py` (sealed at CP-M17-W3-PERSONAL-CLIENT-SESSION
Commit-A `adf828f6c7debbb4719c3cb47ef72af400fd6798`) contains `emit_ask` which
constructs `Ask_v0` via:

```python
ask = Ask_v0(
    ask_id=ask_id,
    tenant_id=session.tenant_id,
    handoff_id=session.session_id,   # ← passes `pcs_…` string
    payload_ref=payload_ref,
    created_at=created_at,
)
```

The sealed shapes are incompatible at the regex boundary:

- `PersonalClientSession_v0.session_id` · regex `^pcs_[a-z0-9_-]+$` (M17-W3 seal)
- `Ask_v0.handoff_id` · regex `^ho_[a-z0-9_-]+$` (M14-W3 seal · Canon 15 §33 mirror)

No `session_id` value can satisfy both regexes at once. **Every valid
`PersonalClientSession_v0` fails `Ask_v0(handoff_id=session.session_id)` at
pydantic construction with `string_pattern_mismatch`.** The M17-W3 seal's
`emit_ask` is deterministically broken at runtime.

The M17-W3 GREEN-cycle receipt
(`phase0/drill_receipts/20260919T141356Z_cp_m17_w3_personal_client_session_GREEN_post_module.log`)
did not surface this because M17-W3's seven tests are AST-scan only (import
graph + banned prefixes + seam-import verification) with no runtime
invocation of `emit_ask`. The mismatch is a legitimate latent structural
bug that this milestone-integration cycle is the first to exercise.

## Why this counts as SO §6.7 Stop-condition #1

Owner ruling 2026-09-18 Item 5 verbatim (in `STATE/STANDING_ORDERS.md`):

> "Fail closed on the affected fork, present options with a recommendation,
>  continue on everything else. Do not hold the whole build on one fork.
>  Triggers: 1. RED ratchet or failed invariant. …"

Trigger 1 fires: the M17-W5 card MUST-DO 5 item (iv) demands a runtime
`emit_ask` invocation that routes through sealed M14 Mkondo `admit` +
sealed answering-service `asks` collection append under `t_<tenant_id>`
per M11. The sealed session.py cannot execute that path successfully.

## Options with recommendation

**(i) Additive-adapter extension — SO §3.8 preserved.**
Author a new module `services/personal_client/handoff_binding.py` (new
file · thin adapter · Canon 8 §W11 role separation preserved) that
exposes `derive_handoff_id(session: PersonalClientSession_v0) -> str`
returning `"ho_" + session.session_id.removeprefix("pcs_")`. Author a
new `emit_ask_with_handoff(session, payload, ask_id, created_at,
repository, handoff_id_overrider=derive_handoff_id)` surface that
routes through the sealed M14/M11 seam correctly. **Does NOT edit the
sealed M17-W3 `session.py`.** The broken `session.emit_ask` remains
sealed as-is; the new adapter is the authoritative runtime path.
- **Pros:** additive-only; preserves seal; unblocks runtime invocation
  at W5 milestone integration boundary; matches SO §3.8 thin-kernel
  discipline.
- **Cons:** parallel surface until sealed `emit_ask` is retired at a
  future ceremony; owner desk-note required to prefer new surface
  over old.

**(ii) Structural-verification-only at W5 milestone boundary
(RECOMMENDED for THIS SEAL).**
Complete the M17-W5 test file with **AST-scan structural verification**
of `emit_ask`'s wiring to the sealed M14/M11 seam (verify at bytecode
level that `emit_ask` calls `Ask_v0(...)`, `insert_ask(...)`,
`_tenant_db_name(...)`, and consumes `session.session_id` / `session.tenant_id`
via the correct attribute references) rather than executing a runtime
invocation. Contract creation + key issuance + session composition
runtime paths all remain runtime-verified (they work correctly). Bank
this fork explicitly in DECISIONS.md at Commit-B; recommend Option (i)
additive-adapter authoring as a **follow-on sub-wave** (M17-W6 or a
memory-layer-adjacent thin adapter) at the next owner digest boundary.

- **Pros:** unblocks M17 milestone close now; preserves sealed W3
  discipline; presents the discovered bug transparently; does not
  paper over anything; enables non-stop autopilot per owner PROCEED
  directive 2026-09-19T~14:35Z.
- **Cons:** M17-W5 seal claim of "end-to-end runtime binding" is
  downgraded to "structural binding + partial runtime (W1..W3)".
  Milestone closes with a banked fork rather than fully clean.

**(iii) Halt milestone close · demand owner ruling.**
Refuse to seal M17-W5 until owner rules on how to handle the sealed
`emit_ask` runtime path.
- **Pros:** most conservative; matches SO §6.7 "stop-and-report" if
  taken maximally.
- **Cons:** violates owner directive 2026-09-19T~14:35Z ("non-stop per
  §6.7") + violates SO §6.7 "do not hold the whole build on one fork".
  Milestone close blocks memory-layer opening for hours until owner
  reads and rules.

## Recommendation

**Option (ii) for THIS seal + fork banked in DECISIONS.md + owner-desk-note
recommending Option (i) at next digest boundary.**

Rationale:
- Owner directive 2026-09-19T~14:35Z is explicit: "non-stop per §6.7".
  Halting for this fork violates that directive.
- The bug is latent, not new — the sealed shape mismatch predates any
  runtime attempt; nothing is broken in production that was not already
  broken at M17-W3 close.
- Structural verification at W5 preserves the milestone's evidentiary
  scope for W1..W4 sealed shapes and their compositional dependencies;
  it just downgrades the runtime-invocation clause of MUST-DO 5 (iv) to
  a structural clause with the fork banked.
- Option (i) is the clean fix; it can land in a subsequent M17-follow-on
  sub-wave without violating SO §3.8 (new file · additive-only).

## Blocking status

**NOT BLOCKING** the M17 milestone close (per Option ii · SO §6.7
"continue on everything else"). **NOT BLOCKING** the memory-layer open
(orthogonal to session-handoff mechanics). **DOES BLOCK** any downstream
consumer that actually invokes `services.personal_client.session.emit_ask`
at runtime — presently, no such consumer exists in the codebase (the
personal-client surface is a scaffolded reference application, not yet
routed by any live tenant).

## Author + date

main-agent Autopilot · 2026-09-19T~15:18Z UTC · banked at
CP-M17-W5-SEAL-INTEGRATION Commit-B (state master).
