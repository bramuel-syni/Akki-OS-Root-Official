# Canon Addendum 1 — extracted requirements (CA1-xxx)

Source: `canon/AKKI_Canon_Addendum_1.docx` (sha256 `9f00f7bc20e7c8d8dd7ad7957d0960eb9695f990409dc1292f08907d89f4dedc`, 16,794 bytes). Read via `python-docx`; full text at `/tmp/v7_ingest/addendum_dump.txt` (158 lines).

Header (verbatim):
> **AKKI CANON — ADDENDUM 1**
> Gap Closures, Amendments, and New Promise Candidates
> Companion to Documents 1–16 and the build audit. The 16 canon documents are unedited by this addendum — amendments are recorded here and target their document by number; nothing is rewritten in place.

Structure: three sections — (1) Confirmed Closures, (2) Amendments to Existing Documents, (3) New Promise Candidates (Full Write-Up).

## §1 · Confirmed Closures (build-only gap closures; no canon change)

Six promises the canon already fully specified; the gap was in the build, and the addendum records the closures without amending the canon.

| ID | Target | Closure | Amends canon? |
|---|---|---|---|
| **CA1-001** | Doc 2 · Promise #4 | Two-item custody split · audit trail Overview states when an answer drew on 2+ independently-governed units | No — build only |
| **CA1-002** | Doc 6 · Promise #17 | Minimal-sufficient disclosure · audit trail Overview states how many available source units were actually served | No — build only |
| **CA1-003** | Docs 7–8 · Promises #19/#20/#21 | Five-ring unit & warm/fresh fork · Registry densification stat + per-turn warm/fresh tag (partial closure, flagged) | No — build only |
| **CA1-004** | Doc 14 · Promise #24 | Baseline curation · baseline line naming the licence-verified starting model per training run | No — build only |
| **CA1-005** | Doc 14 · Promise #25 | Exceptional-run retention · "Prepare white paper" action drafting from run artefacts | No — build only |
| **CA1-006** | Doc 15 · Promise #26 | Watch's self-contained exception · State line naming the Watch's containment and external witness | No — build only |

## §2 · Amendments to Existing Documents (targeted canon additions)

Six binding additions; each amends exactly one document. Written as new required capabilities the platform must gain.

| ID | Target | Requirement (verbatim compressed) |
|---|---|---|
| **CA1-007** | Doc 2 · Promise #2 | Add a dry-run preview step between Review and Adopt in the declaration workflow: given a candidate declaration, run it against a bounded sample of recent traffic and return what it would and would not have caught, before the DPO adopts it. |
| **CA1-008** | Doc 11 · Promise #9 | Add a Cost Ledger surface exposing the lever sequence itself — cache → route → narrow → cascade → waste report — as named, ordered steps with the saving attributable to each, not just the final per-call cost. |
| **CA1-009** | Doc 15 · Promise #32 | Generalise the registered handoff contract (what / shape / identity / receipt) to every cross-app crossing, not the single ThinkLab→Task Manager instance. Any new hand-off must be expressed in this contract before it ships, the same way any new model call must cross the single chokepoint in Document 1. |
| **CA1-010** | Doc 4 · Promise #8 | Scope the "lower the standard" refusal action to the originating session, with a logged expiry. Unscoped today; unscoped ⇒ a standard lowered for one question persists as the de facto floor for every question after. |
| **CA1-011** | Doc 13 · Promise #22 | Add a standing re-check date, visible per in-service model, on the same cadence the six acceptance criteria already run on. An early failure on a re-check routes to the Watch (Doc 3) the same way behavioural drift already does. |
| **CA1-012** | Doc 15 · Promise #27 | Extend the Watch's existing self-flagging of stale baits (Doc 3) to rulebook re-certification and training baselines: anything adopted from an external standard carries a staleness check against that standard's own revision history, using the same flagging mechanism. |

## §3 · New Promise Candidates (Full Write-Up)

Thirteen items. Eight already built in the v7 prototype with no canon backing (A1–A8), five neither built nor specified (N1–N5). Each carries **Promise + Delivery Experience** at full canon confidence; **Technical Requirements are deliberately absent** — Addendum §3 preface says the source material to write them honestly does not exist yet, so each candidate ends with a set of **Open Design Questions**.

### A-series — built, awaiting canon backing

| ID | Candidate | Built where (per v7 prototype) |
|---|---|---|
| **CA1-A1** | Board submission traceability | Board 360 (four tabs: Signals / Performance / Board Documents / Open Questions) |
| **CA1-A2** | Tracked commitment/goal traceability | Exco 360 (tracked goals with at-risk flags, recommendations traced to signals) |
| **CA1-A3** | Governed artefact inheritance & distribution visibility | Documents suite (Create-doc-from-chat wizard, Exposure Site Map, Questions tab with @mentions) |
| **CA1-A4** | Governed template adoption | Rule Books Library (eight standard rulebooks mapped to ISO 27001 Annex A) |
| **CA1-A5** | Universal entitlement & shielding discipline | Collab group (Mentions / Emails / Projects-Tasks / HR Stuff; HR Stuff aggregate-only by rule) |
| **CA1-A6** | Threshold-gated commitment routing | Spend Requests (auto-approve ceiling; above-ceiling requires named approver) |
| **CA1-A7** | Cross-app hand-off of governed work | ThinkLab → Task Manager (carries locked-in load-bearing set); generalisation tracked via CA1-009 |
| **CA1-A8** | Universal claim-to-evidence trace | "Walk this →" affordance on rule rows, Watch patterns, decisions, and registry figures |

Each A-item names 2–3 **Open Design Questions** — those questions are constraints on the Chunk-3 assessment and are extracted as sub-rows below.

### A-series Open Design Questions (must resolve before promotion to full canon)

- **CA1-A1-q1** Custody class of board submissions themselves — governed under Doc 1 estate rules, or a separate class with its own crossing rules?
- **CA1-A1-q2** When a cited submission is amended/superseded, does the Q&A citation re-verify on Doc 9's freshness logic or silently point at stale material?
- **CA1-A1-q3** Is authorship of a Q&A question access-controlled on Doc 6's minimal-sufficient logic, or open to anyone with the board document?
- **CA1-A2-q1** Is a human challenge to a tracked goal a new artifact on Doc 5's append-only Ledger, or an in-place status flag update (the second loses history)?
- **CA1-A2-q2** Recommendation supersession chain when the underlying signal is retracted — on Doc 10's duplicate/superseded record pattern?
- **CA1-A3-q1** Mixed-custody source chat → generated document — strictest custody, or a document-side mixed-custody marker?
- **CA1-A3-q2** Exposure Site Map — append-only on Doc 5's Ledger-writer pattern, or mutable view?
- **CA1-A3-q3** Does distribution tracking cover downloaded/emailed material, or does visibility stop at the platform boundary?
- **CA1-A4-q1** When an external framework revises (new ISO 27001 edition), what re-certifies an adopted rulebook — the same rule-version stamping (Doc 15), or a separate template staleness check?
- **CA1-A4-q2** Modified template rule after adoption — keeps framework-provenance tag, or forks to an org-authored rule?
- **CA1-A5-q1** Minimum aggregation threshold that qualifies as "aggregate" — fixed platform-wide, or configurable per category (like Doc 2 declared categories)?
- **CA1-A5-q2** Universal aggregate-only rule vs Master-Admin/DPO investigation exception — receipted-crossing treatment (Doc 1) applied?
- **CA1-A6-q1** Auto-approve ceiling — governed by Doc 15's propose/counter-sign/countdown ceremony, or plain config any admin can change?
- **CA1-A6-q2** Approver sees the same feasibility/cost/budget reflection (Doc 12) as the requester, or a reduced summary?
- **CA1-A7-q1** Hand-off carries Doc 4's full reasoning trace (tension/contradiction view re-openable), or only the concluded load-bearing set?
- **CA1-A8-q1** **Load-bearing.** Does "Walk this →" inherit the source's custody rules? An unscoped trace affordance is a second, ungoverned path to the same data Doc 1 built one chokepoint to control.

### N-series — new promises not yet built or specified

| ID | Candidate | Grounding today |
|---|---|---|
| **CA1-N1** | Retention enforcement & attestation (data past retention actually deleted, deletion attested) | Partially grounded: Legal Hold & Retention Rulebook adoptable; refusal traces carry a 90-day retention figure. No enforcement/attestation mechanism. |
| **CA1-N2** | Time-boxed breach & incident notification (named recipient within stated time when a hard line fails) | Nothing built. Platform promises prevention/containment, not what-happens-after. |
| **CA1-N3** | Individual access-and-erasure request (a person can ask what the estate holds on them + ask for erasure) | Nothing built. Today's promises protect data from the organisation's own use, not on the individual's behalf. |
| **CA1-N4** | Data residency & cross-border transfer control (data held only where authorised, jurisdiction boundaries enforced) | Partially grounded: per-source region captured at Connect (Doc 9). Enforcement rule missing. |
| **CA1-N5** | Continuity of the governed record (Ledger, receipts, audit trail survive an outage with stated RTO) | Nothing built. Every other promise depends on these records existing. |

### N-series Open Design Questions

- **CA1-N1-q1** Retention-triggered deletion — through Doc 15's full propose/counter-sign/countdown ceremony, or a lighter path since no judgement is exercised at fire-time?
- **CA1-N1-q2** Legal hold + expired retention on same data — hold overrides indefinitely; authority to lift; separate authority model on Doc 15's Watch-exception pattern?
- **CA1-N2-q1** Trigger — only confirmed successful bypass, or also near-miss/attempted-and-contained?
- **CA1-N2-q2** Notification routing — Watch's existing self-witnessing (Doc 15 exception), or an authority independent of the Watch (since the Watch cannot be the sole reporter of its own containment failure)?
- **CA1-N3-q1** Erasure reach — raw source only, or also five-ring units (Doc 7) AND weights of a model trained on the erased data (Doc 13)? If a model cannot practically be untrained, what does the promise guarantee at that layer?
- **CA1-N3-q2** Requester identity verification — this is a close-to-independent promise the erasure promise depends on but does not itself supply.
- **CA1-N4-q1** Doc 12 defines "in-perimeter" as a single boundary — does multi-region deployment mean multiple perimeters or one perimeter spanning regions? Residency is meaningless without a defined boundary.
- **CA1-N4-q2** Given Doc 9 already captures per-source region, is the remaining gap purely an enforcement rule (hard line refusing any cross-boundary operation) layered on data already tagged?
- **CA1-N5-q1** Continuity as a replication/backup property of the same Ledger writer (Doc 5), or its own independently-governed layer on Doc 15's Watch-record-classes pattern? If separate, who verifies a backup's integrity when the primary verification mechanism is the thing that's down?

## Totals

- **CA1-001 … CA1-012** (12 formal amendments/closures) — direct additions to the canon-of-record.
- **CA1-A1 … CA1-A8** (8 built-without-canon candidates) — required next canon promises with full Delivery Experience text.
- **CA1-N1 … CA1-N5** (5 new promises) — canon backing missing AND no built instance yet.
- **~28 Open Design Questions** — constraints on how each new candidate can be specified.

**Total new canon requirements added by Addendum 1: 12 + 13 = 25 rows.** These land in Chunk-3's assessment matrix as separate rows and must not be silently merged with the 31 canon promises.

## How the Addendum bears on standing rulings + built estate

- **Resolves** ambiguity on FL-P2-13 (no-fabrication) for the six "Absent → added" promises — the Addendum §1 confirms those additions are legitimate build-side closures, not fabrication.
- **Amends** the built handoff instance (ThinkLab→Task Manager) into a general contract requirement (CA1-009). Our built estate ships no handoffs yet, so this is a forward-looking rule.
- **Creates** a new load-bearing question (CA1-A8-q1) about "Walk this →" custody — before we build any trace affordance, we must scope it under Doc 1's chokepoint or accept a second ungoverned path.
- **Introduces** N-series promises (retention enforcement, breach notification, individual access-and-erasure, residency, ledger continuity) — none of which we have anything for. These are Chunk-3 rows classed as BUILD (net-new).

**No collision with the current Registry-A4 build** (services.registry_facts + Registry.jsx render real-record facts across three tabs). The Registry tab shape is not touched by the Addendum; the addendum-visible surface additions (Board 360, Exco 360, Documents suite, Rule Books Library, Collab, Spend Requests, "Walk this →", Cost Ledger) are DIFFERENT surfaces, not Registry tabs.

## Wave E ratification (2026-08-27 · CP-E1 + CP-E2 + CP-E3 · autonomous)

Three N-series promises moved from "Nothing built" to ENFORCED via mechanism. Owner ruling verbatim recorded in `STATE/DECISIONS.md · Wave E scope §1..§3 (2026-08-27T~12:10Z)`.

- **CA1-N2 · Breach notification** · Status → **DONE (ENFORCED)** at CP-E2.
  - Mechanism: `services/n_series/breach.py::fire_breach_notification` + policy config `breach_policy.v0.json` (q1='refusal_bypass_only', q2='independent_authority', q3='actor_ids_masked', q4='one_per_breach', window_hours=72, canon_grounded=true).
  - Contract additive fields: `trigger_event_class` Literal[containment_failure | actual_exfiltration | unreceipted_crossing], `recipient_dpo_id` + `recipient_witness_id` (wi_ pattern), `source_watch_action_class`, `notify_deadline_utc` (auto-computed +72h), `alert_channel_receipts` list.
  - Invariant encoded (not commented): `source_watch_action_class` in {annotate, shape, contain} REFUSES — "contained/shaped events are the Watch working and MUST NOT trigger notification" (owner ruling verbatim).
  - Real-time channel: file drops under `phase0/breach_alerts/{recipient_id}/{notification_id}.json` for BOTH DPO and witness on every fire.
  - Wire paths: POST/GET `/api/n_series/breach` (existing shell, now enforcement).
  - Receipt: `phase0/drill_receipts/20260827T134130Z_cp_e2_close_run1.log` + `..._run2.log`.

- **CA1-N3 · Access & erasure** · Status → **DONE (ENFORCED)** at CP-E3.
  - Mechanism: `services/n_series/erasure.py::fire_erasure_request` + policy config `erasure_policy.v0.json` (q1='raw_and_five_ring_units', q2='existing_platform_credential', q3='erasure_wins_over_ca1_n1', requestor_classes_allowed=[named_customer, named_employee]).
  - Contract additive fields: `requestor_class` Literal[named_customer|named_employee], `platform_credential_ref`, `model_flag_ids` list, `crossing_receipt_ref`.
  - New contract: `RightsLapseFlag_v0` at `contracts/rights_lapse_flag_v0.py` with resolution Literal[scheduled_retrain|documented_residual] (owner ruling: "scheduled for retraining OR documented as residual exposure").
  - Custody chokepoint routing: every erasure fires a `CrossingReceipt` with `kind='n3_erasure_operation'`, `masking_tier='attested_command'`.
  - Wire paths: POST/GET `/api/n_series/erasure` + NEW GET `/api/n_series/rights_lapse_flags`.
  - Receipt: `phase0/drill_receipts/20260827T135155Z_cp_e3_close_run1.log` + `..._run2.log`.

- **CA1-N5 · Ledger continuity** · Status → **DONE (ENFORCED for ruled portion; RTO owner-pending)** at CP-E1.
  - Mechanism: `services/watch/continuity.py::write_attestation` + policy config `continuity_policy.v0.json` (cadence='quarterly', cadence_class='default', canon_grounded=false — proposal-class distinction preserved per owner ruling; verification_mechanism='independent_backup_check').
  - Countersigner enforcement: `attested_by` MUST be a registered `WitnessIdentity_v0` with `independent_of_authorities=True` (defence-in-depth check catches out-of-band tampering).
  - Wire paths: POST/GET `/api/watch/continuity`.
  - **Open item** (honest carry): `rto_target_seconds='OWNER_POLICY_PENDING'` — owner has NOT ruled RTO; service refuses to fire while sentinel present.
  - Receipt: `phase0/drill_receipts/20260827T132858Z_cp_e1_close_run1.log` + `..._run2.log`.

### N-series q-questions ratified this wave

- CA1-N2-q1 → **refusal_bypass_only** (hard line ACTUALLY CROSSED).
- CA1-N2-q2 → **independent_authority** (DPO + external witness).
- CA1-N3-q1 → **raw_and_five_ring_units** (models FLAGGED via A17.15 pattern, not erased).
- CA1-N3-q2 → **existing_platform_credential** (no new identity machinery).
- CA1-N5-q1 → **external-witness pattern with independent countersigner infrastructure** (cadence quarterly · DEFAULT-class · NOT canon-grounded; RTO remains owner-pending).

### N-series still open

- CA1-N1 (retention enforcement · Wave E did NOT touch).
- CA1-N4 (residency enforcement · Wave E did NOT touch; per-source region tag exists via Doc 9).
- CA1-N5 RTO target (owner has NOT ruled).
