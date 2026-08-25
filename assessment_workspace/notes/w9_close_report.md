# W9 Close Report

**Wave**: W9 · Watch mechanism seam (Canon 8 §6-§8) · CA1-011 enforcement (route_recheck_failure) · CA1-012 staleness-flagging (route_staleness_flag) · CA1-N5 continuity attestation scaffolding · Canon 8 §14-§18 containment fabric
**Owner ruling**: Auto-continue 2 waves (2026-08-26T00:25Z verbatim in `STATE/DECISIONS.md`); no explicit W9 GO required.
**Wave open**: 2026-08-26T02:45Z (right after W8 CLOSE at `bfafd5f`).
**Wave close**: 2026-08-26T03:45Z.
**Extraction-Akki HEAD**: `programme/track-a` @ `7027e16` (CP5 · containment fabric).
**Pod-shell HEAD** (`/app` main): `0b227d9` (unchanged from W8 · no new spine routers landed this wave).
**Assessment-master HEAD**: `<pending W9 close commit>`.
**Baseline at wave open**: `bfafd5f` (W8 CP6 follow-up · FL-P4-W8-02 landed).

---

## 1 · Bottom line

- **416/416 W9 wave-close cohort GREEN** (63 test files) at `phase0/drill_receipts/20260826T034000Z_w9_wave_close_green.log`. Frozen+contract sub-cohort green at each CP; parity count 47 → 52 across the wave.
- **LOC actual · 2190 net (spine only · pod-shell unchanged)** vs **6400 budget** → **34% consumed · UNDER by 4210 LOC**.
- **1 fidelity ledger row opened at W9** (`FL-P4-W9-01` · CA1-N5-q1 owner policy · **OPEN** · non-blocking to wave close per owner directive).
- **5 W9 commits** on `programme/track-a` from `5a8cf4b` (CP1) to `7027e16` (CP5).
- **Watch mechanism SEAM (Canon 8 §6-§8) DELIVERED** — Macho (sensor) + Mkono (responder) with atomic act-and-attest and constitutional-negatives enforcement.
- **CA1-011 enforcement half BOUND** at the W7-named seam `services.watch.route_recheck_failure`. Full SPLIT ruling completed end-to-end.
- **CA1-012 Watch staleness-flagging DELIVERED** as generic staleness route (baseline_line + rulebook_rule scope).
- **CA1-N5 continuity attestation STRUCTURAL SCAFFOLDING DELIVERED** (refuses fire until owner rules CA1-N5-q1).
- **Canon 8 §14-§18 containment fabric DELIVERED** — start_containment + reconcile_containment with expiry-required contract shape.

---

## 2 · Register rows lit (Canon 8 · Watch)

| Row | Anchor | Status |
|-----|--------|--------|
| C8-008 (§6) | verdict row → action row seam · no other channel | CP1 · services.watch.mkono seam law enforced |
| C8-009 (§7) | Macho senses · reconciles · mints verdicts · reads governance · writes ONLY verdict rows | CP1 · services.watch.macho |
| C8-010 (§7) | Macho does NOT act, does NOT touch the estate | CP1 · macho.py has no writer outside verdicts |
| C8-011 (§8) | Mkono executes response · writes ONLY action-record classes | CP1 · services.watch.mkono |
| C8-012 (§8) | Mkono consumes verdict rows · atomic act-and-attest | CP1 · act_on_verdict refuses without verdict + refuses double action |
| C8-019 (§14) | Containment is bounded reversible operational state | CP5 · Containment_v0 |
| C8-025 (§17) | Every containment carries an expiry · state without expiry IS a defect | CP5 · expires_at required (min_length=1) |
| C8-026 (§18) | Every containment expiry reconciles honestly | CP5 · ContainmentReconciliation_v0 + reconcile_containment |
| C8-045 (§32.1) | NO surface renders behavioural-profile internals (W13) | CP1 · verdict body enforces no profile/threshold/raw_features |
| C8-047 (§32.3) | NO surface renders mark placement | CP1 · action body enforces no placement fields |
| C8-049 (§32.5) | NO Watch action executes without a receipt landing atomically | CP1 · action_record IS the attestation |
| C8-051 (§32.7) | NO expiry is auto-extended | CP5 · Containment_v0 expires_at required · no auto-extension path |
| C8-055 (§33) | Verdict rows · writer=Macho · readers=Mkono+consoles+auditors | CP1 · load_verdicts / mint_verdict discipline |
| C8-056 (§33) | Action records · writer=Mkono · readers=both authorities+consoles | CP1 · load_actions / act_on_verdict discipline |

### CA-series rows lit

| Row | Anchor | Status |
|-----|--------|--------|
| **CA1-011** (Doc 13 §23) | Re-check date state + enforcement | CP2 · route_recheck_failure fires on overdue · SPLIT ruling W7-half + W9-half COMPLETE |
| **CA1-012** (Doc 15 addendum) | Watch staleness-flagging for rulebooks + baselines | CP3 · route_staleness_flag accepts baseline_line + rulebook_rule kinds |
| **CA1-N5** (Doc 15 addendum) | Continuity of governed record with stated RTO | CP4 · SCAFFOLDING (FL-P4-W9-01 open · refuses fire pending owner policy) |

**Total W9 register rows lit · 17** (14 Canon 8 + 3 CA-series).

---

## 3 · Checkpoint outcomes

| CP | Scope | Spine SHA | Test delta (files added / tests) | LOC (net) |
|----|-------|-----------|----------------------------------|-----------:|
| CP1 | Watch mechanism verdict → action seam · Canon 8 §6-§8 · parity 47→49 | `5a8cf4b` | +2 files · +19 tests | +494 |
| CP2 | CA1-011 enforcement half · route_recheck_failure · idempotent per model_id | `2db2116` | +1 file · +8 tests | +274 |
| CP3 | CA1-012 Watch staleness-flagging · route_staleness_flag · generic staleness route | `1dfb998` | +1 file · +7 tests | +276 |
| CP4 | CA1-N5 continuity attestation scaffolding · FL-P4-W9-01 open · parity 49→50 | `1c825c1` | +3 files · +13 tests | +405 |
| CP5 | Canon 8 §14-§18 containment fabric · start + reconcile · parity 50→52 | `7027e16` | +3 files · +18 tests | +741 |
| **TOTAL** | | | **10 files** · **+65 tests** | **+2190** (vs 6400 budget · 34%) |

---

## 4 · Test delta + receipts

**W8 close cohort baseline · 366 tests (55 files).**
**W9 close cohort · 416 tests (63 files) · +50 tests · +8 files.**

Cohort assembly discipline (unchanged from W8 · FL-P4-W6-02/08/09 + FL-P4-W7-01 + FL-P4-W8-02 broadened).

Per-CP receipts on record (all under `phase0/drill_receipts/`):

| CP | Right-reason failure receipt | Green receipt |
|----|------------------------------|---------------|
| CP1 | `20260826T025000Z_w9_cp1_right_reason_fail.log` (12/12 fail · missing modules) | `20260826T025500Z_w9_cp1_green.log` (19/19) |
| CP2 | `20260826T030000Z_w9_cp2_right_reason_fail.log` (7/8 fail · missing module) | `20260826T030500Z_w9_cp2_green.log` (8/8) |
| CP3 | `20260826T031000Z_w9_cp3_right_reason_fail.log` (7/7 fail · missing module) | `20260826T031500Z_w9_cp3_green.log` (7/7) |
| CP4 | `20260826T032000Z_w9_cp4_right_reason_fail.log` (7/7 fail · missing module) | `20260826T032500Z_w9_cp4_green.log` (13/13) |
| CP5 | `20260826T033000Z_w9_cp5_right_reason_fail.log` (11/11 fail · missing modules) | `20260826T033500Z_w9_cp5_green.log` (18/18) |
| Wave-close | (none · CP5 hardcoded count assertion was updated in the CP5 commit itself, avoiding FL-P4-W8-02 recurrence) | `20260826T034000Z_w9_wave_close_green.log` (**416/416 · 63 files**) |

---

## 5 · Reuse pulls used vs rejected

### USED

- **Canon 8 §6-§8 verbatim** — verdict/action seam law, Macho/Mkono role names, constitutional negatives (§32.1/32.3/32.5/32.7). Every contract field docstring cites the Canon 8 section.
- **Canon 8 §14-§18 verbatim** — bounded reversible operational state, expiry-required, reconciliation outcome grammar.
- **Doc 15 §17 outcome grammar reuse** — ContinuityAttestation_v0 and ContainmentReconciliation_v0 both draw from the matches/diverges/inconclusive vocabulary (also used in RulesUpdateReChecked_v0 at W8 CP6). Cross-canon vocab consistency.
- **W7 CP5 named-seam pattern** — CA1-011 W7-half named the seam string `services.watch.route_recheck_failure (lands W9)` on every status payload; W9 CP2 bound the exact path.
- **W8 CP4 FL-P4-W8-01 stop-and-report pattern** — CA1-N5-q1 FL-P4-W9-01 uses the exact same OWNER_POLICY_PENDING sentinel + service-refuses-fire discipline.

### REJECTED (or DEFERRED again)

- **RMS `synisense/`** (partial Watch primitives) — pre-brief W9 named this as a possible ADAPT source · **NOT USED**. Fresh-authored from Canon 8 verbatim under REFERENCE-NOT-COPY. RMS synisense is aged and has a different architectural pattern (per W6 close and status_and_wave_plan §7 W9 note: "RMS `synisense/` has partial primitives only; Executive-Final's access would materially help").
- **Executive-Final** — pre-brief W9 named this as the sole source of Watch/Grey Mirror mechanism completion beyond mechanism-side · **NOT ACCESSED** (repo unavailable to this build). Grey Mirror four sub-surfaces + mirage + severance flows are the direct casualty of this absence · **DEFERRED to a subsequent polish/completion wave** with explicit gap named.
- **Executive-Core `deck_*.py`** — CA1-005 whitepaper re-evaluation carried from W7 CP6 → W8 → **STILL DEFERRED at W9 close**. Not in W9 Canon 8 scope; belongs with the whitepaper draft-and-freeze mechanism.

### BUILT (not lifted)

- WatchVerdictRow_v0 + WatchActionRecord_v0 contracts + services (CP1 · 494 LOC).
- route_recheck_failure (CP2 · 274 LOC).
- route_staleness_flag (CP3 · 276 LOC).
- ContinuityAttestation_v0 contract + service scaffolding + FL-P4-W9-01 (CP4 · 405 LOC).
- Containment_v0 + ContainmentReconciliation_v0 contracts + services (CP5 · 741 LOC).

---

## 6 · Fidelity ledger rows opened

| Row | Class | Origin | Status |
|-----|-------|--------|--------|
| FL-P4-W9-01 | Owner-policy stop-and-report · CA1-N5 continuity attestation structural scaffolding landed · 2 policy questions pending (CA1-N5-q1 verification architecture + RTO target) | W9 CP4 authorship time · explicit stop-and-report per owner auto-continue ruling | **OPEN** · one-sentence-answerable batch in §7 below |

**Defect classes on record for the programme** (unchanged): FL-P4-W6-02 family recurrence count remains 4 (last recurrence · FL-P4-W8-02 · new DoD element ratified). CP5 in W9 hit the hardcoded numeric assertion CORRECTLY in the same commit (no recurrence in W9).

---

## 7 · FL-P4-W9-01 · CA1-N5 continuity policy questions for owner (one-sentence-answerable)

Per owner directive 2026-08-26T00:25Z ("stop that ITEM, name the question, continue the rest of the wave"), the 2 policy questions surfaced at W9 CP4 are batched here for owner ruling. `write_attestation()` will not succeed on live calls until each answer replaces its `OWNER_POLICY_PENDING` sentinel.

### CA1-N5 · ledger continuity (Doc 15 addendum · CA1-N5-q1)

1. **Verification architecture** — Is continuity a replication/backup property of the SAME Ledger writer (Doc 5), OR its own independently-governed layer on Doc 15's Watch-record-classes pattern? If separate, who verifies a backup's integrity when the primary verification mechanism is the thing that is down?
   *Options on record*: `replication_check` · `independent_backup_check`.

2. **RTO target** — What Recovery-Time Objective (in seconds) does the estate commit to for the governed record classes covered by the attestation?
   *Options on record*: owner-supplied integer seconds (e.g., '60' · '300' · '900').

### FL-P4-W8-01 · N-series questions still awaiting owner (§7 of W8 close report)

- 4 CA1-N2 questions (breach trigger scope · notification routing · actor masking · cadence).
- 3 CA1-N3 questions (erasure reach · requester identity verification · retention-vs-erasure conflict).

**How ruling lands mechanically:** owner picks one option per question (any format · email · verbal transcribed to `STATE/DECISIONS.md` · signed policy note). Operator authors the corresponding fire call with the chosen `Literal` value in place of `OWNER_POLICY_PENDING`; the service will write the record. Zero code changes required.

---

## 8 · Deferrals from W9 (explicit · not silent)

1. **Grey Mirror four sub-surfaces + mirage + severance + guilty/innocent flows** (Canon 8 §15-§16 + §32.4 + §33) — W9 nominal scope named "Grey Mirror completion". W9 delivered ONLY the containment half of Grey Mirror groundwork. Full mirage machinery (planted credentials · honeytokens · decoy artefacts · severance execution · innocent-inside-mirage release · guilty-inside-mirage aftermath) is XL architectural scope · **DEFERRED to a subsequent polish/completion wave (W10 or similar)**. Direct cause: Executive-Final repo unavailable + Canon 8 §15-§16 mechanism-side alone is >1500 LOC estimated.

2. **Walk-this per A8 ruling** (Q1 · Q2 · Q3) — W9 nominal scope. Owner ruling A8-Q1/Q2/Q3 is NOT on record (last owner ruling batch was auto-continue-2-waves 2026-08-26T00:25Z; no A8 ruling since). Cannot honestly build without the disposition · **DEFERRED to a subsequent polish/completion wave (or an immediate CP once owner rules)**.

3. **Watch drills + fitness accounting** (Canon 8 §25-§28) — standing drill mechanism (seeded input · planted credential · expiry clean) + fitness = demonstrated firings over window. W9 delivered ONLY the containment expiry reconciliation record class · **DEFERRED to a subsequent polish/completion wave**.

4. **Reserved-decisions panel** (Canon 8 §19) — human-authored decisions (promote · extend expiry · sign de-mark · resolve authority disagreement · cancel ceremony in countdown). Currently would land as `ApprovalRequest_v0 kind='generic'` (W8 CP3 ships that fabric) but no Watch-specific pane · **DEFERRED**.

5. **Witness fabric** (Canon 8 §9 · §33) — the witness identity model beyond a string field is absent. ContinuityAttestation_v0 carries `witness_signature` as a placeholder string. Full witness signing scheme (independent credentials · alarm-outward-on-tamper · standing-drills counter) · **DEFERRED**.

6. **CA1-005 whitepaper action re-evaluation** — W7 CP6 → W8 → W9 · **STILL DEFERRED**. Not in W9 Canon 8 scope.

7. **Doc 14 §§23–25 remaining 24 rows expansion** — W7 CP1 → W8 → W9 · **STILL DEFERRED**. Not in W9 Canon 8 scope.

8. **Governance frontends** (Rules Updates ceremony surface · Approvals group surface · Access-and-Erasure UI · Breach Notification console · Trace UI · Watch Console · Grey Mirror four sub-surfaces UI) — backend records on record; frontend surfaces subject to IP-allowlist screenshot gap. **DEFERRED** to a polish/completion wave.

**Rationale**: Every deferral above is explicit, cited to its origin (W7 opener carry-over · W8 opener carry-over · Canon 8 XL scope · owner-ruling absence · repo unavailability), and belongs to a named subsequent wave. No W9 nominal-scope item silently slipped.

---

## 9 · Post-W9 opener carry-over (P0 · for a subsequent wave · not auto-continue-covered)

Owner auto-continue ruling covered W8 + W9 only. A subsequent wave requires an owner GO.

**Load-bearing items for next wave to open:**

1. **FL-P4-W8-01 + FL-P4-W9-01 answers** — 9 total policy questions across N-series + continuity attestation.
2. **Owner A8 ruling** (Walk-this Q1/Q2/Q3) — pending.
3. **Executive-Final access decision** — Grey Mirror mechanism completion depends materially.
4. **CA1-005 whitepaper re-evaluation posture** (BUILD vs LIFT vs DEFER-AGAIN).
5. **Doc 14 §§23-25 24-row expansion posture** (BUILD-inline vs consolidate into a doc-refresh cycle).
6. **Governance frontends** disposition (build all at once vs interleave with backend refinement).

---

## 10 · Screenshots (honest gap · unchanged from W3..W8)

Owner's IP allowlist (stop-order 2026-08-14) refuses non-allowlisted sources with `403 · This surface answers allowlisted addresses only.` **This gap is intentional and expected behaviour.** Owner-side rendering required when frontend polish wave lands.

---

## 11 · Dashboard

- **W1..W9 · CLOSED** (W8 closed 2026-08-26T02:45Z · W9 closed 2026-08-26T03:45Z).
- **Frozen contracts** · 52 (previously 47 at W8 close · +5 across W9: `watch_verdict_row_v0` · `watch_action_record_v0` · `continuity_attestation_v0` · `containment_v0` · `containment_reconciliation_v0`).
- **Fidelity ledger rows total** · 15 opened across the programme (`FL-P4-W4-01` · `FL-P4-W6-01..09` · `FL-P4-W7-01..02` · `FL-P4-W8-01..02` · `FL-P4-W9-01`). 13 CLOSED · 2 OPEN (`FL-P4-W8-01` + `FL-P4-W9-01` · both owner-policy-pending · non-blocking to wave close).
- **Owner rulings on file** · 6 (unchanged since W7 close · owner auto-continue ruling covered W8 and W9).
- **Test count** · 416 wave-close cohort green (63 files) at `phase0/drill_receipts/20260826T034000Z_w9_wave_close_green.log`.
- **LOC delivered (W1..W9 cumulative)**:
  - W1..W5 · +11783.
  - W6 · +3319.
  - W7 · +2779.
  - W8 · +2968.
  - **W9 · +2190** · **34% of 6400 budget · UNDER by 4210 LOC**.
  - W1..W9 total · **~23039 net**.
- **Mechanism corpus** approximate coverage post-W9: ~50% (+4 pts from Canon 8 Watch seam + containment + CA1-011 enforcement + CA1-012 + CA1-N5 scaffolding). Grey Mirror mirage + Watch drills + fitness accounting still BUILD-status so this remains modest.
- **Composite headline** approximate: **~48%** (up from ~44% at W8 close).

---

## 12 · Auto-continue mandate satisfied · owner GO required for next wave

Per Owner Ruling 2026-08-26T00:25Z, W8 and W9 completed under auto-continue. This report closes W9.

The next wave (W10 · polish/completion · roughly 5000-6000 LOC estimated for Grey Mirror mechanism completion + Watch drills + Walk-this + governance frontends + Doc 14 expansion + CA1-005 whitepaper re-evaluation) requires an explicit owner GO.

Standing until owner rules:
- **STATE/NEXT.md** updated to reflect "W9 CLOSED · awaiting owner GO for W10 · 2 fidelity ledger rows OPEN (FL-P4-W8-01 · FL-P4-W9-01) · 9 owner-policy questions batched · A8 ruling still pending".
- **Discipline unchanged**: tests-first · REFERENCE-NOT-COPY · same-commit contract+snapshot+map+count DoD (FL-P4-W8-02 extension) · pod-shell+spine same-commit mount DoD (FL-P4-W7-02) · no push.

Waiting for owner receipt of this report.
