READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M8 seal-readiness note · 2026-09-16T~16:45Z

**Owner directive verbatim (2026-09-16T~08:35Z):** *"M6/M8 seal-readiness notes: one compact note each stating exactly what single set of owner inputs stands between current state and the milestone seal."*

**Purpose.** State exactly what single set of owner inputs stands between the current state of M8 · catch-all Serving Integrity Amendment (SIA) + governance + canon-remainder milestone and the milestone seal. Nothing else.

---

## §1 · Current M8 state (from-disk verified at 2026-09-16T~16:45Z)

- **6 M8 CPs sealed to date** (per `notes/M8_VERIFICATION_ROLLUP_20260916.md` §1 CP-status table):
  1. CP-M8-G1 · W-M8-TESTS-FIRST-GUARD-INVARIANT (part-B) · 4068→4074 (+6) · Track-a `e02dd4d` · Master `f298b6cd` · fixup `0f0ef8f6`.
  2. CP-EXR1 · W-EXPORT-ARTEFACT-RENDER · 4074→4083 (+9) · Track-a `264f2fd` · Master `c5033e4d` · fixup `7477ec6c`.
  3. CP-DASWR1 + CP-DDDR1 (paired) · W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL · 4083→4093 (+10) · Track-a `7bde883` · Master `790b17d4` · fixup `1ff2602c`.
  4. CP-CRO1 + CP-CRO2 (paired) · W-CENSUS-RUNTIME-ORCHESTRATION · 4093→4105 (+12) · Track-a `29ff398` · Master `b8370491` · fixup `09fd4748`.
  5. CP-SW6-HYG-1 · Credential metadata shape helper (Redaction Hardening Option 1 · §4.1 amendment in-place) · 4282→4288 (+6) · Track-a `053d3f1` · Master `76a8476e` · fixup `df98f8f6`.
  6. CP-M8-CTCC-1 · W-M8-CROSS-TABLE-CONSISTENCY-CHECK · 4384→4400 (+16) · Track-a `b547cd4` · Master `a8e13913` · fixup `ecf59a14`.
- **Ratchet chain**: 4068 → 4400 = **+332 monotonic-up across chain · zero rollback**.
- **Case-agnostic doctrine** held chain-wide (zero closed enums · zero domain tokens · zero dispatch-surface imports on preventive/refusal contract modules).
- **§3.3 seal-chain parity restored 2026-09-16T~08:25Z** (owner ruling §A authorization discharged) — all 6 M8 CP entries carry both SHAs in seal + DECISIONS per §3.3 rule 2.

---

## §2 · The single set of owner inputs blocking the M8 seal

**§3.2 clause 5 · Cross-service binding enforcement ruling** — one owner ruling required (per M7 W-M7-W1-VERIFICATION wave-honest limit D.1 verbatim; per M8 STATUS ROLLUP §7 owner-desk-P2 chain).

**What the ruling says** (owner will choose one of these three shapes — this is the only ambiguity left; per prior owner-desk framing):

| Shape | What owner rules | Purpose in M8 seal |
|---|---|---|
| **(a) HARD-GATE at CP-M7-W1-POST-1-EXTENSION** | All 5 candidate dispatch surfaces (training_runner/runner.py, ssh_seam.py, audio_poc/hf_transcribe.py, audio_poc/gap_fill_writer.py, campaign_infra/run_queue.py) MUST bind to `runtime_supervisor.record_progress` in a new CP that adds gating invariants. | Closes the "no run without a progress signal" enforcement to a runtime hard-gate on every dispatch surface. |
| **(b) PREVENTIVE-CHARTER pattern (matches CP-M8-CTCC-1)** | Add a preventive assertion module (analog of `services/governance_plane/cross_table_consistency.py`) that surfaces the binding as data-in / data-out; runtime enforcement fires only when caller invokes. No hard-gate on running dispatch surfaces. | Keeps M8 catch-all shape (preventive) consistent with CP-M8-CTCC-1 precedent. |
| **(c) DEFER indefinitely** | Cross-service binding enforcement remains chartered-forward as a POST-milestone concern; M8 seals as-is with the wave-honest limit banked in the rollup. | Closes M8 immediately with the 6 CPs sealed to date. |

**Ambiguity is narrow.** M8 is a catch-all bucket by charter (per M8 STATUS ROLLUP §7 verbatim: *"M8 has no consolidated wave-close because catch-all bucket · CPs surface as they clear owner-input"*). Only §3.2 clause 5 stands between "6 CPs sealed and rolled up" and "M8 seal report authored."

---

## §3 · What is NOT blocking M8 seal (from-disk verified)

- **M8 catch-all buildable-now items** — 0 remaining this shift (per triage 2026-09-16T~08:35Z §3 · Lane 1 EXHAUSTED · Lane 2 P1 BLOCKED-ON-PREREQUISITE · P5 PARTIAL campaign-perturbation-blocked · P6 BUILDABLE-NOW discharged as CP-M8-CTCC-1).
- **§3.3 seal-chain parity** — restored 2026-09-16T~08:25Z via 4-fixup-commit back-compat batch + wrap-up (owner ruling §A authorization).
- **§4.1 CREDENTIAL CUSTODY READ DISCIPLINE** — hardened in M8 at CP-SW6-HYG-1 (Redaction Hardening Option 1); post-ratification zero SEC-class incidents.
- **§4.2 clause 6 CROSS-WAVE MODIFICATION HANDLING** — ratified 2026-09-16T~06:35Z; retroactively vindicates the 4 M5→M8 extension pattern (custody_file × 2 · data_suite_v2 engines · census_canon registry_write).
- **§5 GPU obligations** — utilization interleave check-ins on cadence to 72h completion; W-Queue-Watchdog on-host portion legitimately DEFERRED-TO-POST-72H-CAMPAIGN per zero-perturbation discipline (this is chartered follow-on, not a blocker).

---

## §4 · One paragraph · exactly what the owner needs to do

**Land one ruling on §3.2 clause 5 · cross-service binding enforcement** — pick one of shapes (a) HARD-GATE, (b) PREVENTIVE-CHARTER, or (c) DEFER (per §2 table above). That single ruling unblocks the M8 wave-close report authoring.

After the ruling lands:
- If (a): author CP-M7-W1-POST-1-EXTENSION as a new sealed CP (tests-first · §3.3 protocol · adds cross-service binding gating invariants); then M8 seal report.
- If (b): author a new preventive-charter M8 CP (`services/work_supervisor/cross_service_binding.py` analog of `cross_table_consistency.py`); then M8 seal report.
- If (c): author M8 seal report immediately with the wave-honest limit banked.

**Nothing else is blocking.** All 6 sealed M8 CPs have double-green byte-match, §3.3 seal-chain parity, and Path α clean receipts. The rollup note at `notes/M8_VERIFICATION_ROLLUP_20260916.md` is authored and audit-ready. One owner ruling.

---

## §5 · Wave-honest limits

- **W.1** M8 has no consolidated wave-close by charter (catch-all bucket). The "M8 seal" here means "M8 STATUS ROLLUP note upgraded to seal report" — not a mechanism-close seal.
- **W.2** The three shape options are exhaustive per the owner-desk framing; no fourth option is on the table.
- **W.3** Owner-desk P1 items (JUMP root credential rotation · Admin bindings for CD + Visitors · NAS credentials for audio-bearing shares · HF token status · Campaign B settlement) are BLOCKED-ON-PREREQUISITE for specific other CPs but are NOT gating the M8 seal itself — they gate downstream M6/M7 dependencies (per M8 STATUS ROLLUP §7 · P1 unchanged).
- **W.4** Owner-desk P2 items (Ruling #5 sub-verdicts · Path A/B ruling · R-6 pricing · Amendment 8 · Watch-Learning R-15(b)/R-16(b)/R-17(b) · BC tier · DAP R-2/R-3 · Rules-Service R-2 · S-24/27/28/29 · WPW R1/R2/R3 · SW-10 A.1-A.5) also do not gate the M8 seal — they gate M6 seal (Ruling #5) or downstream M7 waves (Path A/B) or WPW Tier-3, all discussed in M6 seal-readiness note.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
