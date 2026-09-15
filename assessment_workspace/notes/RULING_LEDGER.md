# RULING_LEDGER.md — owner rulings ledger (STEP 3 close, owner directive 2026-09-08T~06:15Z)

**Created:** 2026-09-09
**Owner directives banked:** 2026-09-08T~06:15Z (STEP 3) · 2026-09-09T~11:40Z (proceed straight through) · 2026-09-13 (M0-open C3 batch-ratification; see `notes/RATIFICATION_C3_BATCH_20260913.md`)
**Ratchet floor at creation:** 3017 · **at latest reconcile 2026-09-13:** 3562

## Purpose

Every owner ruling banked verbatim in `STATE/DECISIONS.md` gets its human-readable
status row here. This ledger is the source of truth for "what's ratified, what's
default, what's coupled, what's still owner-open" — mirrored from the DECISIONS
verbatim bank without paraphrasing the ruling itself.

Categories:
- **RATIFIED** — owner explicitly approved the proposed value; binding immediately.
- **DEFAULT** — owner set a working value with `DEFAULT-class · revisable on evidence` posture; wired now, may change on later ruling.
- **COUPLED** — must be ruled together with a named companion; solo ruling forbidden.
- **OPEN** — genuinely awaiting owner input; **not** an ambiguity reflected back — a concrete decision the owner has said he wants to make himself.

---

## RATIFIED (17 = original 5 + C3-batch flip of 12)

**Original 5** (2026-09-08 · unchanged):

| # | Ruling | Owner text (verbatim from DECISIONS.md 2026-09-08T~06:15Z) |
|--:|---|---|
| 1 | Rules-Service **R-4** taxonomy | Ratified as proposed. |
| 2 | DAP **R-1** controlled-unit definition | Ratified as proposed. |
| 3 | Agent-Containment **R-1** capability-ceiling list | Ratified as proposed (the four ceilings: no self-replication, no unauthorised resource acquisition, no unauthorised credential escalation, no self-access to oversight). |
| 4 | Rules-Service **R-3** witness | Same witness the Watch already uses (C3). |
| 5 | Agent-Containment **R-2** scope-ratifying authority | Syni.ai for early deployments. |

**C3-batch flip 2026-09-13** (owner verbatim: *"3 - Approved"* · see `notes/RATIFICATION_C3_BATCH_20260913.md`):

| # | Ruling | Value (flipped DEFAULT → RATIFIED) |
|--:|---|---|
| 6 | Rules-Service **R-1** countdown | 48h system-ordinary / 7 days system-TCB |
| 7 | DAP **R-4** API-key lifetime | 90-day rotation |
| 8 | DAP **R-5** AI-labs taxonomy | Separate external-party entry |
| 9 | Security **R-10** recommendation window | 24h (A5.16) |
| 10 | Security **R-8** approach | Baseline-period |
| 11 | Security **R-9** approach | Baseline-period |
| 12 | Security **R-11** approach | Baseline-period |
| 13 | Agent-Containment **R-3** sample rate | Baseline-period |
| 14 | Pruning **R-12** default | Re-derivation |
| 15 | Doc-0 **R-1** TCB test | Resolved-by-use; deterministic ∧ protection-critical (`tcb_enumeration_v1`) |
| 16 | Doc-0 **R-3** Watch TCB membership | Mkono IN · Grey Mirror OUT |
| 17 | Doc-0 **R-5** deployment model | Dedicated infrastructure per tenant (`trust_domains_v1`) |
| + | Serving-Integrity **R-13** validation cadence | Monthly + per-engine-version + per-artefact-version (folded under C3 en-masse) |

**Release-Gate-Pilot-Lift ratification 2026-09-15T~03:55Z** (owner verbatim ruling packet · see `STATE/DECISIONS.md` 2026-09-15T~03:55Z):

| # | Ruling | Value (flipped OPEN → RATIFIED) | Owner verbatim (from ruling packet) |
|--:|---|---|---|
| 18 | Security **R-7** (Audio-POC release-gate branch) | **PILOT-OPEN** (deliberately kept open during pilot · release-ledger receipts+debits accumulate from day one · real budget number ratified at pilot end from measured usage · missing receipt still refuses per Pull Seam P7) | *"for now keep this open as we are piloting ... every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed."* |
| 19 | Audio-POC release-gate **R-15(a)** (named-persons verdict) | **TOKENIZED** (per-custody-class placeholder tokens · token-table never emitted alongside artefact · Pull-Seam identity-never-crosses) | *"People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."* |
| 20 | Audio-POC release-gate **R-16(a)** (transfer-basis verdict) | **DERIVATIVE_ONLY_VIA_PULL_SEAM** (derivatives may cross · raw estate data never does except via outer gate · Pull-Seam P007 reversed-direction anchor) | *"transfer_basis resolves to derived-intelligence-only: derivatives (attributes, features, transcripts-as-derived-text with tokenized identities) may cross; raw estate data never does except via the outer gate."* |
| 21 | Drift-item **D12** (CI-fixture whisper-tiny transcription POC) | **APPROVED** (bounded single-digit-count real NAS files · runs on GPU hosts akki-vm/akki-vm-ii · outputs labeled `poc_flag=POC-NOT-PRODUCTION` in provenance · receipts banked · fires after census + after W-RELEASE-GATE-PILOT-LIFT · production model selection follows §A17.11 separately) | *"After the census completes: run the transcription pipe-proof with the canon CI fixture (whisper-tiny + faster-whisper) on a SMALL BOUNDED set of real NAS files (single-digit count), on the GPU hosts, all outputs labeled POC-NOT-PRODUCTION in provenance, receipts banked. Production model selection still follows census activation per §A17.11 — the POC does not pre-empt it."* |

**Milestone tree ratification + autonomous execution authorization 2026-09-15T~04:12Z** (owner verbatim ruling · see `STATE/DECISIONS.md` 2026-09-15T~04:12Z):

| # | Ruling | Value (flipped PROPOSED → RATIFIED) | Owner verbatim (from ruling) |
|--:|---|---|---|
| 22 | Milestone re-homing tree at `master f4a2a2df` — M0..M5 unchanged; 🧭M6 (Audio-Plane production build, §15 order) + 🧭M7 (Governed Census/Harvest Platform W0..W9 + 10-plane · lifts POC-BUILD-HOLD) + 🧭M8 (post-launch hardening + §COV/§ORPH catch-all) flip PROPOSED → FORMAL | **RATIFIED as formal programme structure** + **AUTONOMOUS EXECUTION AUTHORIZED** under initial guardrails unchanged (SO §1 boot · tests-first RED→GREEN→GREEN byte-match · ratchet monotonic-up · two-commit local-only · NEVER push · terminal pytest only · testing_agent banned · position-redaction hard-lock · egress window 08:00–02:00 UTC · verbatim-canon · HALT-rather-than-guess) | *"OK. Proceed with tree autonomously as per initial guardrails when setting up milestones. ... The re-homed milestone tree at master f4a2a2df is RATIFIED as the formal programme structure. 🧭M6 ... 🧭M7 ... 🧭M8 ... are now FORMAL milestones. Update the milestone binding accordingly (successor binding note on master, verbatim owner quote as §A). AUTONOMOUS EXECUTION AUTHORIZED through the tree in dependency order, under the initial guardrails unchanged ..."* |

**BC-3 / BC-4 · Owner ruling 2026-09-15T~03:55Z** flipped BOTH from `DEFAULT-PENDING-OVERRIDE (static number)` to `DYNAMIC-RECOVERY-PACKET (tiered policy authoring)`. Ownership of the ratification transitions from a numeric ratification to a tiered-policy ratification via `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md`. Not counted in the RATIFIED table above until owner ratifies the packet.

## DEFAULT (0 remaining after C3 batch)

All prior DEFAULT rows flipped to RATIFIED per C3 batch 2026-09-13. New DEFAULT rows would appear here as future owner rulings land with DEFAULT-class posture.

## COUPLED (1)

| # | Ruling | Coupling clause (verbatim) |
|--:|---|---|
| 1 | DAP **R-3** per-party ceilings | MUST NOT be ruled alone — allocation against Security **R-7** estate release budget; rule together. **Note (2026-09-15T~03:55Z):** R-7 flipped to PILOT-OPEN with receipts-and-debits; DAP R-3 remains COUPLED and re-rules at pilot end from measured usage. |

## OPEN (10 — genuine owner decisions; +2 reconcile from `Ratification_Record_v1` + Serving-Integrity Amendment + 2A env-drift-tracked-unknown + Watch-Learning Amendment v1 R-15(b)/R-16(b)/R-17(b) + Audio-POC release-gate R-17(a) hardening)

| # | Ruling | What owner has explicitly reserved for himself |
|--:|---|---|
| 1 | ~~Security **R-7** (Audio-POC release-gate branch)~~ | **FLIPPED → RATIFIED (PILOT-OPEN) 2026-09-15T~03:55Z** · see row 18 in RATIFIED above |
| 2 | DAP **R-6** | Pricing model |
| 3 | WPW **R-2** | External-release signatory |
| 4 | DAP named approving authority (DAP **R-2**) | Person/role identity |
| 5 | Rules-Service **R-2** | Second-signatory named role (reconciled from `Ratification_Record_v1` Section 2 R-2; not previously in RULING_LEDGER; added M0 2026-09-13) |
| 6 | Serving-Integrity Amendment **R-14** | candidate serving engine admission — deliberately unruled; gated by appliance benchmark + TCB-tier admission ceremony (added M0 2026-09-13; engine name scrubbed per owner ruling 2026-09-14) |
| 7 | **ENV-DRIFT-2TESTS-20260913** | 2 tests present in close-time env (recorded 3562 floor) but not collected in current sandbox at HEAD `e2ae44b0`. Preflight rebased floor to 3560 per owner Option A ruling 2026-09-13. Closed when close-time env info surfaces (e.g. per-test collect-only log from the close-time sandbox). Tracked, not lost. |
| 8 | Audio-POC release-gate **R-17(a)** (licence-class hardening) | Tighter licence-class taxonomy for non-`owner_full_rights` tiers. Owner-verbatim 2026-09-15T~03:55Z: *"R-17(a) hardening stays open (non-blocking)."* Not blocking end-to-end (SAFE tier already has full rights). Added 2026-09-15T~03:55Z. |
| 9 | Watch-Learning Amendment v1 **R-15(b)** | Initial certificate-library seed (spec-closed; Watch Learning surface awaits population). Owner-verbatim 2026-09-15T~03:55Z: *"The Watch-Learning R-15(b)/R-16(b)/R-17(b) set stays OPEN — do not conflate."* Added 2026-09-15T~03:55Z (disambiguated from R-15(a)). |
| 10 | Watch-Learning Amendment v1 **R-16(b)** | Ratifier role + research cadence (Watch Learning). Owner-verbatim 2026-09-15T~03:55Z: (same block as row 9). Added 2026-09-15T~03:55Z. |
| 11 | Watch-Learning Amendment v1 **R-17(b)** | Capability-class granularity (Watch Learning · AC-15..AC-18 rows). Owner-verbatim 2026-09-15T~03:55Z: (same block as row 9). Added 2026-09-15T~03:55Z. |
| 12 | Drift-item **D9** (universal receipt-before-result invariant) | Extend `admit_transcript_release` + every operation surface to write receipts before returning per Pull Seam §2 P7 P036 verbatim. Charter candidate: `W-PULL-SEAM-RECEIPT-UNIFY`. |
| 13 | Drift-items **D10** (Silero VAD INFERRED) + **D11** (pyannote/speaker-diarization-3.1 INFERRED) | Formal owner-ratification of canon-named starting-point for VAD + speaker-diarization (currently INFERRED per Verbatim-canon standing rule). Typically ruled together. |

---

## Rollup (post BC-Dynamic-Recovery-Packet + Audio-POC release-gate ratifications 2026-09-15T~03:55Z)

| Class | Count |
|---|--:|
| RATIFIED | 21 (17 original + 4 this-turn: R-7 PILOT-OPEN, R-15(a) TOKENIZED, R-16(a) DERIVATIVE_ONLY, D12 APPROVED) |
| DEFAULT (wired tests-first) | 0 (all flipped in C3) |
| COUPLED (blocked until companion) | 1 (DAP R-3 · re-rules at pilot end) |
| OPEN (owner-reserved) | 12 (row 1 flipped to RATIFIED; rows 8..13 added this turn) |
| **Total tracked** | **34** |
| **Pending-packet ratification** | +2 (BC-3 · BC-4) — awaiting `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` owner ratification |

## Also HELD (not counted in rollup; tracked for owner reference)

- **DPO-S2 reflection contract** — HELD per owner C5 disposition 2026-09-13 · reflection.run() raises NotImplementedError · 3-5 candidates in `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md` awaiting owner selection.
- **S-7 "Learn"** — HELD per Amendment 1 (spec gap) · owner-context package at `notes/S7_CONTEXT_PACKAGE_20260913.md` (4 options).
- **Amendment 8 scope-statement (eradication / communication / evidence custody)** — HOLD per owner C1 disposition 2026-09-13 · parked, no milestone assigned.

## Rule (banked)

DEFAULT-class values are **wired into `backend/services/rulings/default_class_constants.py`
tests-first**: every value in that module is frozen by an invariant test that
docstring-quotes the owner ruling verbatim. If the owner overrides a DEFAULT
later, the invariant is amended in the same commit that flips the value. A
DEFAULT value is never silently changed.

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
