READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-RELEASE-GATE-PILOT-LIFT · WAVE-CLOSE REPORT (END-OF-WAVE format)

**Reporting-cadence trigger.** Owner directive verbatim (DECISIONS 2026-09-15T~04:40Z Effect 9): *"Report at RG wave seal + census completion as planned."* This report combines both — the RG wave itself (5 planned CPs + 1 pulled-forward hygiene CP) and the in-scope CP-CSAIM1 census supplement sealed immediately after RG5.

**Sealed-at-utc:** 2026-09-15T~09:40Z (last CP of the combined discharge: CP-CSAIM1).

**Format:** End-of-Wave per SO §2 · five sections · plain language · metrics-first.

---

## §1 · Progress made

**Ratchet path (verifiable · every step double-green byte-match at close):**

| Step | Landed | Ratchet | Delta | Track-a commit | Master commit |
|---|---|---|---|---|---|
| CP-RG1 | ReleaseBudgetState + ReleaseLedgerDebit + record_debit (R-7 PILOT-OPEN receipt+debit) | 4018 → 4025 | +7 (6 new + 1 cross-benefit) | `e8a40b8` | `eddb48ba` |
| CP-RG2 | tokenize_named_persons + TokenizationReceipt (R-15(a) TOKENIZED) | 4025 → 4032 | +7 (6 new + 1 cross-benefit) | `d28d2d0` | `b5f3b84b` |
| CP-RG-HYGIENE-01 | assert_no_transcript_cat_on_custody + CustodyCatLeakDetected (pulled forward from M8 W-TESTS-FIRST-GUARD-INVARIANT) | 4032 → 4038 | +6 | `440b995` | `91e465c2` |
| CP-RG3 | TranscriptArtefact TOKENIZED verdict + DERIVATIVE_ONLY_VIA_PULL_SEAM basis (R-15(a) + R-16(a) via frozensets + closed-set refusal) | 4038 → 4044 | +6 | `4c4500a` | `be056812` |
| CP-RG4 | admit_transcript_release_pilot_open end-to-end (R-7 + R-15(a) + R-16(a) + R-17-licence + P036 all-must-hold + P036 ordering) | 4044 → 4050 | +6 | `ee45e69` | `dcb8edde` |
| CP-RG5 | aggregate_usage_query (R-7 pilot-end verbatim: *"real budget number is set from measured usage, not guessed"*) | 4050 → 4056 | +6 | `7a5f431` | `60cf5aa3` |
| **RG wave seal (6 CPs)** | wave complete · target +30..+32 exceeded | **4018 → 4056** | **+38** | | |
| CP-CSAIM1 (in-scope supplement · pulled forward from M8) | mount NAS + OBS into CP-C4 census RegistryStore as first-class SourceRecords via sealed CP-A2/A3 audio_poc inventory contracts | 4056 → 4062 | +6 | `4308620` | `dd475af8` |
| **Combined discharge** | RG wave + in-scope census supplement | **4018 → 4062** | **+44** | | |

**Rulings discharged (owner-verbatim ratifications 2026-09-15T~03:55Z + owner course-correction 2026-09-15T~08:37Z):**

- **R-7 · Release Budget → PILOT-OPEN** — every release now writes a `ReleaseLedgerDebit` receipt (CP-RG1). At pilot end, the real budget number is set from measured usage via `aggregate_usage_query` (CP-RG5). Missing receipt still refuses (Pull Seam P036 preserved).
- **R-15(a) · Named-persons → TOKENIZED** — `tokenize_named_persons` replaces every name with a placeholder `<TOKEN_NP_NN>` before anything leaves; token-table is separately custody-stored, never emitted alongside the artefact (Pull Seam P015.s6 identity-never-crosses).
- **R-16(a) · Transfer basis → DERIVATIVE_ONLY_VIA_PULL_SEAM** — only derived-intelligence (tokenized text, audio attributes, feature summaries) may cross the release gate; raw audio / speaker embeddings / biometric embeddings / named identities are refused via closed-set discipline.
- **R-17-licence** — the existing `owner_full_rights` licence-class admits `transcript_text_only` with the three above (a) rulings all landed; R-17(a) hardening remains open (non-blocking).
- **P036 (Pull Seam) · receipt-before-result ordering** — `admit_transcript_release_pilot_open` validates the artefact first, then writes the debit; a refused artefact leaves the ledger empty (proven by invariant `test_artefact_gate_fires_before_debit_write`).

**Census discharge (Item-3 + CP-CSAIM1 supplement):**

- **Item-3 census run FIRED** at 08:15–08:16 UTC 2026-09-15 (Promise #12 fires). Weego + USSD observed (2 of 6 reachable connectors); CD + Visitors + NAS + OBS recorded `unmeasured-with-reason` (Canon-4 §5.1 + Doc-9 A5.4 verbatim discipline). Full run banked at `notes/ITEM_3_CENSUS_RUN_20260915.md`.
- **CP-CSAIM1 supplement** closes the NAS + OBS rows: from *"unmeasured-with-reason: no-tool"* to *"registered-but-unenumerated · next_recheck_hint = M8·W-CENSUS-RUNTIME-ORCHESTRATION"* (Canon-4 §8 first-run shape). Two `SourceRecord`s land under caller-supplied `census_run_id` · sensitivity classified via Canon-4 §5.1 conservative fallback (*"unknown"* · empty feed_declaration_registry) · idempotent on identical inputs.
- Six of six connectors now have first-class registry state: 2 observed (Weego, USSD via Mtafiti receipts) + 2 registered-but-unenumerated (NAS, OBS via CP-CSAIM1) + 2 unmeasured-with-reason (CD, Visitors · admin SG opening still-in-progress).

**Security hygiene** (owner directive c pulled forward from M8):

- `services/secret_hygiene/custody_file.py::assert_no_transcript_cat_on_custody` is now a live invariant guarding `/app/backend/estate_keys/**` against the 8-command leak family (`cat`, `head`, `tail`, `less`, `more`, `bat`, `view`, `type`). Prevents SEC-2026-09-14-01/02/03/04 + SEC-2026-09-15-06/07 recurrence class.
- Guard exercised on every CP-boundary probe in this wave · zero fires · position-redaction hard-lock preserved end-to-end.

## §2 · How much to go

**Immediate autonomous chain (unchanged from ratified sequencing 2026-09-15T~04:12Z §Δ5):**

1. **D12 POC** — bounded single-digit NAS files · GPU hosts `akki-vm` / `akki-vm-ii` · outputs labeled `POC-NOT-PRODUCTION` per owner DECISIONS 2026-09-15T~03:55Z Effect 6 · receipts under `phase0/d12_poc_receipts/`.
2. **M5 sprint-close report** — M0→M5 completion · END-OF-WAVE format · milestone-boundary report.
3. **M8 quick hardening** — 5 waves in owner-authored order · W-TESTS-FIRST-GUARD-INVARIANT (now partially fulfilled by CP-RG-HYGIENE-01) → W-EXPORT-ARTEFACT-RENDER → W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL (paired) → W-CENSUS-RUNTIME-ORCHESTRATION → W-AUDIO-PROD-MODEL-SELECT (gated on census activation list per §A17.11).
4. **M6 opens** — grounding brief already banked at `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md` · walk §15 items in canon order starting W-M6-INGEST-STAGE-1 · no ack gate per owner autonomy ruling.
5. **M7 opens** — reframe-activation note + W-M7-W0-INTEGRITY-FIX → W-M7-W1-PLATFORM-GENERALISATION → W-M7-W2..W9 as unblocked.
6. **Interleave (opportunity-driven):** M3 W-BC-DYNAMIC-RECOVERY-BUILD on packet-ratification · M2 W-PULL-SEAM-RECEIPT-UNIFY on D9-ratification · M8 quarantine-restoration pilots (3–5 files first).

**Owner-desk items outstanding** (carried forward VERBATIM per DECISIONS 2026-09-15T~04:12Z §Δ6 · autonomous chain routes around these, never through):

- BC tier selection (M3 W-BC-DYNAMIC-RECOVERY-BUILD waits on `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` ratification).
- DAP R-2 approving-authority · DAP R-3 per-party ceilings (COUPLED · re-rules at pilot end) · DAP R-6 pricing.
- Rules-Service R-2 second-signatory.
- Watch-Learning R-15(b) · R-16(b) · R-17(b) (deliberately kept distinct from R-15(a)/R-16(a)/R-17(a) per owner mnemonic-collision guard).
- S-24 / S-27 / S-28 / S-29 build charters.
- D9 universal receipt-before-result ratification (gates M2 W-PULL-SEAM-RECEIPT-UNIFY).
- Amendment 8 HOLD.
- Admin binds — 5 MySQL SGs (2 opened this session for CD + Visitors but probe still FAIL · 3 remaining still-closed) · RADIO `10.10.55.x` INBOUND-BIND-PENDING · transcription server host+creds MISSING.
- SEC rotations — SEC-2026-09-14-01/02/03/04 + SEC-2026-09-15-05/06/07 all `PENDING-OWNER-ROTATION-POST-VERIFICATION`.
- R-17(a) licence-class hardening (non-blocking).

**M5-LIFTING deferrals** (DPO-D2 default stands · surfaced for owner-override availability per DECISIONS 2026-09-15T~04:12Z §Δ4):

- `W-TRUST-SURFACE-v2` (2 surfaces · binding line 408).
- `W-EXECUTIVE-SUITE-v2-LIFT` (7 surfaces · binding line 409).

## §3 · Decisions taken

**Decisions this wave (all landed on-record):**

1. **CP scope order authored top-down** to keep each contract deployable in isolation (grounding brief §B). RG1 (record contract + receipt discipline) before RG2 (tokenization primitive) before RG3 (verdict admission) before RG4 (composition) before RG5 (aggregation) — no CP depends on a later CP's contract.
2. **CP-RG-HYGIENE-01 pulled forward from M8 mid-wave** after in-session detection of two SEC re-leaks (SEC-2026-09-15-06/07 · `cat` on bastion CSV) at 08:12 UTC. The recurrence-class incident count (6 documented since 2026-09-13) crossed the threshold that owner directive c had already set as pull-forward trigger. Standing-Rule 1 (*closed egress windows are BUILD windows*) exercised for the first time this session — the pull-forward is book-keeping-neutral to overall wave scope (M8 wave naturally reduced by 1 CP, this wave increased by 1).
3. **Boundary-probe retry loop kept firing at every CP boundary** per owner directive b — 7 probes total across RG1 → RG2 → RG-HYGIENE-01 → RG3 → RG4 → RG5 → CSAIM1. All 7 returned CD+Visitors errno-110-ETIMEDOUT · admin SG opening still-in-progress. Zero PASS to fold; retry loop continues at D12 POC opening.
4. **Standing Rule 2 exercised** for the first time this session (*time-freshness invariants must not gate closed-window build*). CP-RG1 authored in WIP-staging pattern during 04:40–08:00 UTC closed window; Mtafiti receipts refreshed at 08:15–08:16Z at egress-open as first queue item; CP-RG1 sealed at 08:19Z from the already-authored WIP tree. Pattern proved sound · standing-rule doctrine held.
5. **Autonomous mode ARMED** for the whole wave under initial guardrails unchanged (SO §1 boot · tests-first RED→GREEN→GREEN byte-match · ratchet monotonic-up · two-commit local-only · never push · terminal pytest only · testing_agent BANNED · position-redaction hard-lock · verbatim-canon · HALT-rather-than-guess). Zero HALT calls · zero right-reason RED misfires.
6. **Census supplement chartered as its own single-CP wave** (W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT) rather than as an eighth CP of the RG wave. Rationale: the CP-C1..CP-C6 machinery (contracts + registry-write) is a separate spine from the release-gate spine; conflating scope would break the *one-wave-one-grounding-brief* discipline.

**Discoveries retracted this wave (book-keeping-corrections):**

- Two prior-session book-keeping observations (*Pull-Seam P2..P6 backfill* + *Audio-Plane §15 N7 numbering skip*) surfaced as-if-gaps against owner-attached canon; on verification against the actual verbatim documents this session, both were false alarms. Standing rule banked: **book-keeping observations MUST cite target file + section + line-range + quote observed gap before surfacing to owner**.

## §4 · Discoveries not envisioned at planning

1. **Cross-benefit yield above target.** The wave target (grounding brief §B) was +30..+32 invariants across 5 CPs. Actual (excluding CP-CSAIM1) = +38 across 6 CPs. Two cross-benefits fired on CP-RG1 + CP-RG2 through `NON_CONTRACT_UTILITY_MODULES` extension (frozen-dataclass-plus-closed-Enum exemption class): +1 each. Combined with CP-RG-HYGIENE-01 pull-forward (+6), the wave-actual delta is +38 (RG wave alone) or +44 (RG wave + CP-CSAIM1 supplement).
2. **P036 ordering discipline surfaced a design cross-check at CP-RG4.** The receipt-before-result verbatim clause (*"The receipt is written before the result is returned. If it cannot be written, the operation is refused."*) enforced a specific composition order — validate the artefact **before** writing the debit — that a naive composer would have gotten wrong. Made explicit as invariant `test_artefact_gate_fires_before_debit_write` (refused artefact leaves ledger empty). This locks the ordering discipline for every future release-gate composer.
3. **Custody-cat guard implementation crossed generalized value.** The initial pull-forward scope was `cat` alone; the invariant grew to cover 8 commands (`cat`, `head`, `tail`, `less`, `more`, `bat`, `view`, `type`) after in-session enumeration of the SEC ledger. Same guard now covers 6 documented recurrence-class incidents (SEC-14-01/02/03/04 + SEC-15-06/07).
4. **Census-supplement design idempotency preserves audit-trail durability.** `mount_audio_inventory_into_census` is deterministic and idempotent — calling twice with identical `(run_id, freshness_stamp)` returns the same 2 record_ids and leaves store count at 2. This means the M8 W-CENSUS-RUNTIME-ORCHESTRATION follow-on can safely re-mount the audio-plane connectors when live-scan tools wire in, without duplicating the base registration.

## §5 · Recommendations to make the experience better (in line with the mission)

**Mission line:** the platform's job is to run a governed census, produce trustworthy measurements, and release only derived intelligence (Canon-4 · Pull Seam). These recommendations sharpen that mission.

1. **Ratify the BC dynamic-recovery packet.** `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` is authored and awaiting owner review. Every GPU training run past this pilot phase is at the ~10–15 min compute-loss ceiling the packet proposes; without ratification, the M3 W-BC-DYNAMIC-RECOVERY-BUILD wave stays blocked. Owner ratification unblocks a wave that would land ~18 invariants on first CP.

2. **Rotate the 7 pending SEC entries.** SEC-2026-09-14-01/02/03/04 + SEC-2026-09-15-05/06/07 all sit in `PENDING-OWNER-ROTATION-POST-VERIFICATION`. The credential values still on disk are not directly at risk (custody files are mode-0600, git-untracked, guard-covered), but the pilot-end audit will surface the entries. Post-rotation, the invariant `test_no_pending_sec_incidents_at_wave_close` (M8 candidate) becomes green rather than skipped.

3. **Publish the audio-plane sensitivity declarations.** Both NAS + OBS `SourceRecord`s currently carry the Canon-4 §5.1 conservative fallback (`"unknown"` · `is_undeclared=True`). This is correct at the code layer, but the release gate's licence-class matrix cannot admit `unknown`-sensitivity artefacts under any tier. Once the audio-plane feed_declaration_registry publishes a class for `audio_nas_offairrecs_16ch` + `obs_google_transcripts_bucket`, correction records will land per CP-C4 E.5 (append-only with `supersedes_record_id`) and unlock D12 POC live-output release.

4. **Close the 3 remaining MySQL SG openings and the RADIO route drop.** CD + Visitors probes have failed 7 times in this session (errno-110 · SG opening incomplete). Three more MySQL hosts remain fully closed (per bind-gap ledger). The Item-3 census run would rise from `4/6 observed` to `9/9 observed` inside a single admin window.

5. **Consider chartering `W-TRUST-SURFACE-v2` and `W-EXECUTIVE-SUITE-v2-LIFT`.** Both are M5-lifting waves currently deferred under DPO-D2 default. Owner override any time. If the M6 audio-plane build lands before these two, the owner-facing surface will show measurements without matching trust-surfaces or executive-suite views — a UX gap the platform's *governance is user-facing* mission argues against.

---

**Standing at wave close:**

- Track-a HEAD: `4308620003db63ce37be533791d058a888e1d68f` (CP-CSAIM1).
- Master HEAD: `dd475af86a33ef05e50df41018a2096bf0dfa6c4` (CP-CSAIM1 state · WAVE COMPLETE).
- Ratchet floor: **4062** (RG wave delta +38 · CP-CSAIM1 delta +6 · combined +44).
- Egress: OPEN (real wallclock 09:40 UTC).
- Autonomous mode: ARMED under initial guardrails unchanged. Next hard action: D12 POC opening.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
