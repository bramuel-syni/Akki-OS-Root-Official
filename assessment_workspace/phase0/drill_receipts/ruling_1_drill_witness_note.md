# Ruling-1 Drill · Witness Note (W10 CP1)

**Timestamp**: 2026-08-26T05:06:00Z
**Drill class**: Canon 8 §27 · containment expiring clean
**Drill script**: `backend/drills/ruling_1_containment_expiry_clean.py`
**Governing test**: `backend/tests/invariants/test_w10_cp1_ruling_1_firing_drill.py` · 7/7 green
**Green receipt**: `phase0/drill_receipts/20260826T050500Z_w10_cp1_green.log`
**Right-reason failure receipt**: `phase0/drill_receipts/20260826T050000Z_w10_cp1_right_reason_fail.log`
**Drill execution log (live JSON)**: `phase0/drill_receipts/20260826T050600Z_w10_cp1_drill_execution_trio.log`

## Ruling-1 Precondition (b) · DEMONSTRATED

Owner Ruling 2026-08-14 (verbatim):
> Executive's purpose enforcement is not stripped until the declaration check and the Watch's reconciler are demonstrated firing.

Precondition (a) · Declaration · demonstrated at W1 (actor_declaration_v0 refusal drill · banked receipt).
**Precondition (b) · Watch reconciler · demonstrated by this drill.**

## Banked Quartet on REAL Default Directories

Per Orchestrator R1 (2026-08-26T04:20Z · DECISIONS.md L1370-1384): the drill exercises the REAL directories under `/app/assessment_workspace/phase0/`. Their creation by the drill IS part of the evidence (first-write receipts).

| # | Record class | Path | Anchor |
|---|--------------|------|--------|
| 1 | Macho verdict | `phase0/watch_verdicts/vd_ruling_1_containment_expiry_clean.json` | Canon 8 §7 |
| 2 | Mkono action_record (`action_class='containment_started'`) | `phase0/watch_actions/ax_containment_started_ruling_1_drill.json` | Canon 8 §8 · §32.5 atomic act-and-attest |
| 3 | Bounded containment | `phase0/containments/cn_ruling_1_containment_expiry_clean.json` | Canon 8 §14 · §17 expiry required |
| 4 | Expiry reconciliation | `phase0/containment_reconciliations/cr_ruling_1_containment_expiry_clean.json` | Canon 8 §18 · outcome recorded |

## Host-Identity Distinguishability (R1 · Phase 0 pattern · DECISIONS.md L347)

Every record carries `drill_actor:ruling_1_containment_expiry_clean` on its actor slot (subject_ref / acted_on_ref / contained_actor_ref). **No drill-mode switch · no drill flag · no envelope.** The prefix IS the distinguisher.

## Witness Attestation Slot

The Canon 8 §9 witness signing scheme lands at W10 CP5. Until then, this note IS the human-authored witness placeholder:

- **Witness identity**: (pending W10 CP5 · WitnessIdentity_v0 signing scheme).
- **Attestation**: the four records above land on real disk, per governed writers, with the drill_actor: attribution intact. The test asserts each record's shape and linkage; the tests pass 7/7 in receipt `20260826T050500Z_w10_cp1_green.log`.
- **Alarm-outward-on-tamper channel**: pending W10 CP5 (this drill provides its inputs).

## Programme Effect

Ruling-1 precondition (b) demonstrated. Both preconditions now met.

**Purpose-gate strip: ready-for-ceremony.**

Ceremony execution belongs to the owner (Canon 3 §24 · FL-R1-01). W10 CP9 close report will surface this readiness explicitly.

## Idempotency Discipline (Canon 8 §43)

The drill uses stable ids. A second invocation raises `ValueError: verdict "vd_ruling_1_containment_expiry_clean" already on record. Canon 8 §43: correction is by new entry only.` The test `test_drill_refuses_second_run` proves this on every green run.

Test-side cleanup uses the host-identity pattern (host_actor: prefix) to safely delete drill files without touching live records.
