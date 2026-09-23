# CP-AIP-9-COMMISSION-VIEW · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §13 · Build Sequence #9.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-8 completes).

## Rationale for position (spec §15 verbatim)

> *"Reads records created in 8; by §13.4 it cannot precede them."*

## Scope

**§13.1 — applies to ALL commissioned work on the platform** (extraction, census, training commissions alike, across every extraction type). NO modality receives its own UI. NO surface is a rendering of backend internals.

**§13.2 verbatim behaviour:**

> **The surface is milestones. The artifacts are evidence behind them.**

- Sampling & Reflection proposed milestone list presented for owner agreement. Commission does NOT open until agreed.
- Commission View reports against the agreed checklist:
  - Each milestone with `done_condition` + `owner`.
  - Status in **plain terms** — done, on track, behind, missed.
  - **Missed is shown as plainly as done.**
- Spend against quote shown at the same plain level.
- Technical material (calibration results, strata coverage, Collection Schema state) is **drill-down evidence** for whoever asks WHY a milestone reads as it does. NEVER the front page.

**§13.3 modality leaf:**

- Modality appears at exactly ONE leaf: evidence inspection.
- Where provenance resolves to a recording, the source **plays at its timestamp** rather than rendering as a page region.
- Existing trust-receipt pattern (`"a disputed number is answered by playing the tape"`) unchanged.

**§13.4 backend cost constraint (STRICT):**

> *"Milestones are records with done-conditions; the platform already stamps events. **No new machinery is built for display.** Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."*

## Acceptance criteria (become RED-first pytest invariants)

1. **§13.4 no-new-backend-computation invariant**: static AST scan of the Commission View surface router confirms zero new-compute endpoints — only reads of existing ledger + registry.
2. Milestone status shape frozen enum `{"done", "on_track", "behind", "missed"}` (§13.2 verbatim four states).
3. Front-page carries milestones only — technical fields (calibration curves, strata coverage details, Collection Schema state) forbidden on front-page surface (drill-down only).
4. Modality-leaf tape-playback invariant: audio-provenance drill returns `{"kind": "tape_playback", "timestamp": <t>}` shape, never a page region render.
5. Commission-open guard: `commission.open` requires `milestone_list.agreed_at is not None`.

## New additive modules (proposed shape)

- `routers/commission_view.py` — read-only surface (§13.4 no compute).
- `services/commission_view/milestone_read.py` — read from existing ledger.
- `services/commission_view/spend_read.py` — read from existing metering ledger.
- `services/commission_view/tape_playback.py` — modality leaf handler.
- Frontend `pages/CommissionView.jsx` + `hooks/useCommissionView.js` (byte-identical pod_shell twin).
- Test file: `tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py` (≥5 RED-first pins).

## Sealed carriers to NOT edit

- Existing metering + ledger surfaces (read-only consumers).
- Existing trust-receipt tape-playback pattern.

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-9-COMMISSION-VIEW and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD · byte-identity pod_shell/frontend ↔ /app/frontend.**
