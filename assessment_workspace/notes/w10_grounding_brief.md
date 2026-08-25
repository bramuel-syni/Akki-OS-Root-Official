# W10 Grounding Brief (polish / completion wave)

**Status**: DRAFT · awaiting owner W10 GO + scope confirmation.
**Prep timestamp**: 2026-08-26T04:10Z.
**Baseline**: Extraction-Akki `programme/track-a` HEAD `7027e16` (W9 CP5 · Canon 8 §14-§18 containment) · pod-shell `0b227d9` (W8 CP5 trace mount) · assessment-master pending post-correction commit.

W10 opens on explicit owner GO (auto-continue ruling covered W8+W9 only).

---

## 0 · Corrections carried into W10 opener (from FL-P4-W9-02)

Three W9-close report errors ratified as compaction-loss corrections:

1. **A8 ruling is ON RECORD** — DECISIONS.md L738-760 · 2026-08-19 · Q1 ON · Q2 INTERIM · Q3 ON · single-chokepoint basis · REFERENCE-NOT-COPY design law. Walk-this is UNBLOCKED (not deferred).
2. **Executive-Final is ACCESSED** — DECISIONS.md L768 · 2026-08-19 · HEAD `bba80ab` · verdict on record: no Watch/Grey-Mirror material · Grey Mirror is a BUILD (not blocked by repo access).
3. **Ruling-1 status surfaced** — reconciler AUTHORED (W9) but NOT DEMONSTRATED FIRING (no `phase0/watch_*/` records on disk). Purpose-gate strip NOT ready-for-ceremony. Needs a firing drill (W10 CP1 candidate).

**New standing discipline (FL-P4-W9-02)**: after any context compaction, first action before drafting a report or STATE change is to re-read the last 200 lines of DECISIONS.md and the current NEXT.md.

---

## 1 · Scope (owner-listed at 2026-08-26T04:00Z)

Owner's verbatim W10 scope (from correction message):
> "prep the W10 grounding brief (scope you listed: Grey Mirror flows, Watch drills+fitness, reserved-decisions, witness signing, CA1-005, Doc 14 §§23-25, and the governance/Watch/Grey-Mirror FRONTENDS incl. Walk-this under A8)"

Add: **Ruling-1 firing drill** (W10 CP1 · unblocks purpose-gate strip ready-for-ceremony).

---

## 2 · Checkpoint layout (proposed · tests-first per CP · same-commit DoD)

| CP | Scope | Canon anchor | LOC est (pre-cal · × 1.60) | Class |
|----|-------|--------------|----------------------------:|:-----:|
| CP1 | **Ruling-1 firing drill** · Canon 8 §27 · containment-expiring-clean drill harness · plants verdict + containment + reconciliation on a governed drill_actor · banks receipt trio to `phase0/watch_*` · closes Ruling-1 precondition (b) | Canon 8 §27 · Ruling-1 (2026-08-14) · FL-R1-01 | 150 · 240 | S |
| CP2 | **Grey Mirror mirage machinery** · Mirage_v0 contract (planted credential · honeytoken · decoy artefact) · services.watch.mirage.plant + engage · innocent-inside-mirage-release + guilty-inside-mirage-severance handling · atomic act-and-attest | Canon 8 §15-§16 · §32.4 (mirage construction hidden) | 900 · 1440 | L |
| CP3 | **Watch drills + fitness accounting** · standing drill cadence · drill harness for §25 (seeded hostile input) + §26 (planted credential) + §27 (containment-expiring-clean) · fitness = demonstrated firings over observation window · §32.8 no-self-cert enforced | Canon 8 §25-§28 · §32.8 | 500 · 800 | M |
| CP4 | **Reserved-decisions panel** · promote-containment · extend-expiry · sign-de-mark · resolve-authority-disagreement · cancel-ceremony-in-countdown · lands as ApprovalRequest_v0 kind='generic' with Watch-side extension · SoD enforced (Doc 15 §17 · Canon 8 §19) | Canon 8 §19 · §32.6 no-reserved-decision-by-machine | 300 · 480 | M |
| CP5 | **Witness fabric** · full signing scheme for Canon 8 §9 witness (independent credentials · alarm-outward-on-tamper · standing-drills counter · Doc 8 §9 read-only-on-governance) · replaces the CP4 W9 witness_signature placeholder string | Canon 8 §9 · §33 | 400 · 640 | M |
| CP6 | **CA1-005 whitepaper re-evaluation** · Executive-Core `deck_*.py` REJECT verdict confirmed OR minimal BUILD (150-LOC lid per Owner Q4 W7) · anchor Doc 14 §33 whitepaper-action | Doc 14 §33 · CA1-005 · Owner Q4 W7 | 150-250 · 240-400 | S |
| CP7 | **Doc 14 §§23-25 remaining 24 rows expansion** · Doc14-002..022, 025, 027, 028 · mechanism-detail continuation from W7 opener grounding | Doc 14 §§23-25 | 400 · 640 | M |
| CP8 | **Governance / Watch / Grey-Mirror frontends** · Rules Updates ceremony surface · Approvals group surface · Access-and-Erasure UI · Breach Notification console · Trace UI · Watch Console · Grey Mirror four sub-surfaces · **Walk-this per A8 ratified rulings** on every trace/preview/embed | Canon 5 v7 fabric · A8 ratified · Doc 15 · Doc 8 §12 (visibility) | 1500-2000 · 2400-3200 | L-plus |
| CP9 | **Wave close** · cohort assembly · **authoritative composite % recomputation from 17-doc register row states · method stated** · close report · STATE update | Owner correction #4 · `status_and_wave_plan.md §2-§5` weighting method | 100 · 160 | S |
| **Estimate total (pre-cal · median-of-band)** | | | **4400 · × 1.60 ≈ 7040** | XL-effective |

**Stop-and-report line**: 7040 LOC (owner may narrow to 5600 XL cap per §7 re-baselined table).

---

## 3 · CP1 firing-drill design (Ruling-1 closure precondition b)

**Owner directive · DECISIONS.md line 1354 verbatim**:
> "the Ruling-1 closure question: once the Watch reconciler is DEMONSTRATED FIRING, both Ruling-1 preconditions are met — do NOT strip the purpose gate yourself; that strip is a Canon 3 §24 ceremony per FL-R1-01's ruling and an owner act. Surface it as ready-for-ceremony in your W9 close report."

**Drill class**: Canon 8 §27 · "a containment expiring clean · verifies expiry reconciliation." Chosen because W9 CP5 already shipped both writers (`start_containment` + `reconcile_containment`) · smallest additional build.

**Drill harness (proposed)**:

1. Author `backend/drills/ruling_1_containment_expiry_clean.py` (script · NOT a service):
   - Mint `WatchVerdictRow_v0` with `sensor='macho.drill_harness'` · `signal_class='drill_containment_expiry'` · `severity='noted'` · `subject_kind='actor'` · `subject_ref='drill_actor:ruling_1_drill'` · `evidence_note='Canon 8 §27 standing drill · containment expiring clean.'` · lands in `phase0/watch_verdicts/`.
   - Call `start_containment` on drill_actor · `bound_scope='read_only_scoped_env'` · `expires_at=now+60s` · lands in `phase0/watch_actions/` (action_class='containment_started') + `phase0/containments/` (containment record).
   - Sleep 61 seconds or fast-forward the clock via a monkeypatched now_iso (choose fast-forward · avoid sleep in a governed drill).
   - Call `reconcile_containment` with outcome='expired_clean' · lands `phase0/watch_actions/` (action_class='noted_no_action' for the reconcile ack) + `phase0/containment_reconciliations/`.

2. Author `backend/tests/invariants/test_w10_cp1_ruling_1_firing_drill.py`:
   - Test asserts all four record classes land on disk atomically.
   - Test asserts Canon 8 §32.5 (atomic act-and-attest · every Mkono write carries verdict_id).
   - Test asserts Canon 8 §17 (containment record has expires_at).
   - Test asserts Canon 8 §18 (reconciliation outcome_note cites the drill purpose).
   - Test drives the drill via governed drill harness; not a mock; every record is real.

3. Right-reason failure receipt · run the test before authoring the harness · watch it fail on missing drill script.
4. Green receipt · run after authoring · bank both to `phase0/drill_receipts/<ts>_w10_cp1_ruling_1_firing_drill_{right_reason_fail,green}.log`.
5. Bank the SAMPLE receipt trio (verdict + action + containment + reconciliation) with a `ruling_1_drill_witness_note.md` in `phase0/drill_receipts/` naming the timestamp + drill class + intended witness attestation slot (§9 witness signing lands at CP5 · until then, `witness_signature` field remains a governed placeholder).

**Ruling-1 status after CP1 lands green**: precondition (b) DEMONSTRATED · purpose-gate strip **ready-for-ceremony** · surfaced explicitly in W10 close report (owner act to strip · Canon 3 §24 · never ours).

---

## 4 · CP2 Grey Mirror mirage — REFERENCE-NOT-COPY discipline reminder

Canon 8 §15 verbatim: "A mirage is a governed misdirection — planted credentials, honeytokens, decoy artefacts. Contact with a mirage is a STRUCTURAL FINDING."

Canon 8 §32.4 forbiddance: "NO surface renders mirage construction." → mirage records MUST NOT expose planting internals; only that a touch occurred + severity.

Canon 8 §15 innocent/guilty split:
- **Innocent-inside-mirage** · ordinary work · releases on expiry · period reconciled honestly (§15).
- **Guilty-inside-mirage** · a guilty actor touching a planted credential produces a MARK MINTED + a SEVERANCE executed on Mkono's own authority · the decision panel receives the AFTERMATH, not the request (§15).

**BUILD (not LIFT)** — Executive-Final does NOT hold mirage material · Executive-Core does not hold it either · this is a fresh build from Canon 8 §15-§16 verbatim.

**Contract shapes (proposed)**:
- `Mirage_v0` (planting record · minimal · does not expose construction · `mirage_id` · `class ∈ {planted_credential, honeytoken, decoy_artefact}` · `planted_at` · `expires_at`).
- `MirageTouch_v0` (touch record · `touch_id` · `mirage_id` · `touched_at` · `actor_ref` · `touch_kind ∈ {innocent_read, guilty_use}` · `evidence_note`).
- `Severance_v0` (severance record · `severance_id` · `touch_id` · `severed_at` · `severed_by='mkono.severance_manager'` · `aftermath_note`).
- Reuse `WatchActionRecord_v0` `action_class='mirage_engaged'` + `'severance_executed'` (both already in W9 CP1 grammar).

---

## 5 · CP3 drills + fitness — Canon 8 §25-§28 verbatim

Canon 8 §28: "Fitness of the Watch is stated in demonstrated firings over the observation window (Doc 6 §9-A: 'the proof is RECEIPTS, not attestation')."

Canon 8 §32.8 forbiddance: "NO drill self-certifies fitness."

**Drill classes to author (in addition to CP1's §27 drill)**:
- Canon 8 §25 · seeded hostile input at the boundary · verifies refusal at input seat · Doc 3 §12.
- Canon 8 §26 · planted credential touched · severance executed · verifies mirage machinery end-to-end (depends on CP2 landing first).

**Fitness accounting**:
- `services/watch/fitness.py` · reads `phase0/drill_receipts/*` · counts demonstrated firings per class per observation window · returns raw counts.
- **DOES NOT** self-attest fitness (§32.8) · the count is the fact · witness attestation (§9) is a separate CP5 mechanism.

---

## 6 · CP4 reserved-decisions panel — Canon 8 §19 verbatim

Reserved decisions (Canon 8 §19 verbatim list):
- Promote a containment (from a lesser bound to a greater one).
- Extend an expiry.
- Sign a de-mark.
- Resolve authority disagreement.
- Cancel a ceremony in countdown.

**Constitutional negative §32.6**: NO reserved-decision is executed by machine.

**Implementation**: extends W8 CP3 `ApprovalRequest_v0` fabric with kind='generic' · adds `reserved_decision_kind` field discriminator · SoD enforced service-side (approver ≠ proposer · already in W8 CP3).

---

## 7 · CP5 witness fabric — Canon 8 §9 verbatim

Canon 8 §9 verbatim: "The witness holds NEITHER authority's credentials. It attests to standing drill outcomes; alarms outward on tamper. It cannot itself act on the estate."

Canon 8 §33: writer=Watch workers + the witness · readers=everyone with assurance standing.

**Scope**:
- `contracts/witness_identity.py` · WitnessIdentity_v0 (independent-credentials scheme).
- `services/watch/witness.py` · standing-drills counter · alarm-outward-on-tamper channel · read-only on governance records.
- Wire into CP1 firing drill's witness_signature slot · replace the W9 CP4 placeholder string.

---

## 8 · CP6 CA1-005 whitepaper — Doc 14 §33

Owner Q4 W7 verbatim: 150-LOC hard lid; overrun → defer with named gap.

**Decision point**: on CP6 open, decide LIFT (from Executive-Core `deck_*.py`) vs BUILD-inline (150-LOC lid) vs DEFER-AGAIN with an explicit new-gap-name. Reject verdict pending from W7 CP6.

**Anchor**: Doc 14 §33 whitepaper-action · draft from run artefacts · MUST cite the model_admission ceremony record + baseline_line record it summarises.

---

## 9 · CP7 Doc 14 §§23-25 24-row expansion

W7 CP1 opener grounding named 24 remaining Doc 14 rows (Doc14-002..022, 025, 027, 028). Row-by-row expansion into the requirements register · linkage to existing model_registry + baseline_line + model_admission ceremony where applicable · honest gap where a row references an unimplemented mechanism.

Rows anchored in Doc 14 §§23-25 mechanism details.

---

## 10 · CP8 Governance / Watch / Grey-Mirror frontends (L-plus · largest CP)

**Owner-listed scope** including **Walk-this under A8 ratified rulings**.

**Surfaces to land**:

| Surface | Canon anchor | Backend records ready? |
|---------|--------------|------------------------|
| Rules Updates ceremony | Doc 15 §17 | ✓ W8 CP3 + CP6 |
| Approvals group | Doc 15 · CA1-006 | ✓ W8 CP3 |
| Access-and-Erasure request UI | CA1-N3 | Scaffolded W8 CP4 (pending owner policy) |
| Breach Notification console | CA1-N2 | Scaffolded W8 CP4 (pending owner policy) |
| Trace UI | Doc 15 §Trace | ✓ W8 CP5 |
| Watch Console | Canon 8 §22 · officer's job | ✓ W9 CP1-CP5 |
| Grey Mirror overview | Canon 8 §14-§18 | ✓ containment (W9 CP5) · mirage (W10 CP2) needed |
| Grey Mirror monitor | Canon 8 §12 (visibility) | Pending CP2 |
| Grey Mirror response | Canon 8 §14 | Pending CP2 |
| Grey Mirror people | Canon 8 §33 (marks reader) | Pending CP2 |
| Model Admission ceremony surface | Doc 13 · CA1-011 | ✓ W7 (needs polish) |
| Cost Ledger surface | CA1-008 | ✓ W6 (needs polish) |
| Model Ecosystem 3-tab surface | Doc 14 | ✓ W7 (needs polish) |
| Data Suite surface (v7-exact) | Doc 05 · W6 deferral | ✗ backend deferred (may or may not fit W10 · defer-again candidate) |

**Walk-this per A8 ratified rulings** (Owner Ruling 2026-08-19 verbatim):
- **A8-Q1 · ON** · deep-link into underlying unit re-enters governed read path · entitlement checked at point of access.
- **A8-Q2 · INTERIM** · side-by-side composition same-actor/same-window · mechanism-gated lift.
- **A8-Q3 · ON** · refused crossings show rule fired verbatim.
- **REFERENCE-NOT-COPY design law** applies to every embed/preview/trace/walk surface.

**Constitutional negatives (Canon 8 §32) enforced on Watch Console**:
- No behavioural-profile internals (§32.1) — profiles are non-exportable, tenant-keyed, non-readable on any surface.
- No thresholds as tunable (§32.2).
- No mark placement rendered (§32.3).
- No mirage construction rendered (§32.4).
- Officer reads restraint record (§22) · findings noted with no action taken.
- Officer never has action require them BEFORE it executes within bounds — they receive AFTERMATH (§22).

**Screenshots gap (honest · unchanged since 2026-08-14 stop-order)**: owner-side rendering required · curl-through-allowlist verification on record for each surface.

---

## 11 · CP9 wave close — authoritative composite % recomputation

Owner correction #4 verbatim: "the composite % has wobbled across compactions (43→46→48→43→48). At W10 close I want ONE authoritative recomputation from the 17-doc register row states, method stated, replacing the running number."

**Method to state** (per `notes/status_and_wave_plan.md §2-§5` weighting scheme):
1. Enumerate all 515 rows across 17 docs from `notes/requirements_register_17docs.md`.
2. For each row · compute current status ∈ {DONE, PARTIAL, REUSABLE, BUILD} · with citation to the closing wave commit + test.
3. Weighted sum · DONE=1.0 · PARTIAL=0.4 · REUSABLE=0.5 · BUILD=0.
4. Mechanism corpus % = weighted sum / 515.
5. Interface % = weighted sum across 58 v7 surfaces / 58 (same weight grammar).
6. Composite = 0.7 × mechanism-corpus + 0.3 × interface.
7. Present as ONE number · replace running composite in dashboard.

Owner ceremony · Canon 3 §24 · purpose-gate strip · ready-for-ceremony (assuming CP1 fires the drill).

---

## 12 · Standing rules for W10

Unchanged from W9 with FL-P4-W9-02 addition:
- After any context compaction, first action is re-read last 200 lines of DECISIONS.md + current NEXT.md.
- Tests-first + right-reason receipts.
- REFERENCE-NOT-COPY (A8-ratified · applies to every embed/preview/trace/walk).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony.
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD.
- Pod-shell + spine same-commit mount DoD.
- Correction-discipline (in-band · old wording struck-through · CORRECTION note · never silent rewrite).
- No push; local commits only.

---

## 13 · Awaiting owner for W10 open

1. **W10 GO** (auto-continue covered W8+W9 only).
2. **W10 scope confirmation** — proceed with all 9 CPs as sequenced · OR narrow (drop CP6/CP7/CP8 Data Suite · defer to a subsequent wave) · OR extend (add Data Suite v7-exact backend inline · +400 LOC pre-cal).
3. **CP2 mirage record shape ratification** — should MirageTouch_v0 carry the touch_kind grammar (`innocent_read` vs `guilty_use`) as service-time or contract-time? Proposing contract-time (§15 grammar is Canon-level · not policy).
4. **CP4 reserved-decisions panel scope** — reserved_decision_kind grammar (5 items per §19) confirmed as governed vocabulary? Or should it be extensible (owner's choice on discriminator schema).
5. **Screenshots posture** — CP8 will ship every governance/Watch/Grey-Mirror surface behind allowlist · owner-side rendering required · does owner want a batched close-of-wave render session at W10 close?

Waiting for owner receipt of this brief.
