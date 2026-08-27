# Wave E · Grounding brief · Compliance & N-series close

**Wave GO ruling (owner, 2026-08-27T~12:10Z, verbatim):**

> OWNER GO — WAVE E (Compliance & N-series close). Autonomous through wave close under all standing conditions (verbatim quotes, anti-compaction, tests-first, local commits only, no push, no testing subagent, BASELINE_GUARD on every close, Ship-Manifest DoD + MUST_BE_LIVE_ROUTES/SPA same-commit for every shipped path).
>
> SCOPE — implement the banked owner rulings as enforcement, not scaffolding:
> 1. CA1-N2 breach notification: recipients = DPO + the Watch's existing external witness; window = 72 hours (canon-grounded Kenya DPA/GDPR); channel = enforcement-view record PLUS real-time alert to both recipients; threshold = a hard line ACTUALLY CROSSED — map onto the existing Watch event grammar (containment failure / actual exfiltration / unreceipted crossing). Contained/shaped events are the Watch working and MUST NOT trigger notification — encode that as an invariant, not a comment.
> 2. CA1-N3 access & erasure: requestor = named customer or employee only (no third-party without separate authorization); verification = existing platform credential, no new identity machinery; REAL erasure for raw source + five-ring units; already-trained models get FLAGGED via the A17.15 rights-lapse provenance mechanism and scheduled for retraining OR documented as residual exposure. Erasure operations route through the custody chokepoint with crossing receipts.
> 3. CA1-N5 ledger continuity: countersigner independent of the primary ledger writer's infrastructure (external-witness pattern); cadence = quarterly recorded as DEFAULT-class (preserve the proposal-class distinction in the contract/config — it is NOT canon-grounded like the 72h window).
> 4. Doc14-020: QUARANTINE-pending-review path for rights-unclear training material — a real quarantine store + review queue + release/refuse resolution, wired into the training-material admit path (admit refuses to pass rights-unclear material through; it quarantines with receipt).
> 5. A18.6 async skill delivery: ADOPT — implement per the proven platform pattern the owner cited; the PROPOSED marker resolves to RULED-ADOPTED in the register.
> 6. Remaining CA1 audit lines from the register (001/002/003/006/007/012 class): sweep for any still-open enforcement gaps and close them or class-attribute honestly in the close report.
> 7. Security/PII pass on the DigiCow paths: verify PII posture (the corpus contains farmer PII — ussd_users 2.28M rows), confirm the response-boundary sanitizer covers every new Wave E surface, and receipt the check.
>
> EXECUTION SHAPE: grounding brief first (notes/waveE_grounding_brief.md — every requirement quoted VERBATIM from the banked rulings in DECISIONS.md + the canon/N-series text; the ruling text IS the spec), CP partition dependency-ordered, stop-and-reports informational, standard halt triggers (non-config blocker / spec contradiction / guard trip / count drift). Every new surface: honest states, structured refusals, REFERENCE-NOT-COPY, sanitizer at the boundary. UI: enforcement-view additions for N2 alerts + N3 request/erasure queue + Doc14-020 quarantine queue belong on existing surfaces (governance/watch/data) unless canon names a dedicated surface — quote the canon text to decide.
>
> WAVE E CLOSE (permanent standard): two consecutive green full-suite receipts + my external third run; close package = register moves (N-series rows to DONE), waveE_close_report.md, STATE mirrors, preliminary composite note. Then HOLD for Wave F GO / SSH key.
>
> SSH interrupt remains INTERRUPT-PRIORITY over everything. Begin.

---

## 1 · Banked owner rulings (Message 315 verbatim, DECISIONS.md lines 2186-2190)

**CA1-N2 breach notification (verbatim):**
> notify = DPO + the Watch's existing external witness (independent by design); window = 72 hours (canon-grounded: Kenya DPA/GDPR); channel = enforcement-view record PLUS real-time alert to both recipients (ledger row alone is insufficient); threshold = a hard line ACTUALLY CROSSED — contained/shaped events are the Watch working as intended and are NOT reportable breaches. When Wave E implements this, map "hard line crossed" onto the existing Watch event grammar (containment failure / actual exfiltration / unreceipted crossing), never onto successful catches.

**CA1-N3 access & erasure (verbatim):**
> requestor = named customer or employee only, no third-party without separate authorization; verification = existing platform credential (no new identity machinery); posture = REAL erasure for raw source + five-ring units; already-trained models get FLAGGED via the same provenance mechanism as A17.15 rights-lapse, then scheduled for retraining OR documented as residual exposure.

**CA1-N5 ledger continuity (verbatim):**
> countersigner = party independent of the primary ledger writer's infrastructure (Watch external-witness pattern — "the verifier can't be the thing that might be down"); cadence = QUARTERLY recorded as DEFAULT-class (owner explicitly flags this as proposal-class, NOT canon-grounded — preserve that class distinction in the record).

**Doc14-020 rights-unclear material (verbatim):**
> QUARANTINE pending review. Not refuse, not admit-with-flag. Owner's reasoning verbatim: "Quarantine is the only option that doesn't foreclose anything before the status is actually resolved."

**A18.6 async skill delivery (verbatim):**
> ADOPT (proven platform pattern). Implementation lands with Wave D/E scope, not now.

---

## 2 · Canon addendum §N-series text (verbatim, notes/canon_addendum_1_requirements.md lines 76-96)

| ID | Candidate | Grounding today |
|---|---|---|
| **CA1-N2** | Time-boxed breach & incident notification (named recipient within stated time when a hard line fails) | Nothing built. Platform promises prevention/containment, not what-happens-after. |
| **CA1-N3** | Individual access-and-erasure request (a person can ask what the estate holds on them + ask for erasure) | Nothing built. Today's promises protect data from the organisation's own use, not on the individual's behalf. |
| **CA1-N5** | Continuity of the governed record (Ledger, receipts, audit trail survive an outage with stated RTO) | Nothing built. Every other promise depends on these records existing. |

**Open design questions superseded by owner rulings above:** CA1-N2-q1 (trigger scope — resolved to "hard line ACTUALLY CROSSED / refusal_bypass_only class"), CA1-N2-q2 (routing — resolved to DPO + external witness), CA1-N3-q1 (reach — resolved to raw + five-ring; models flagged not erased), CA1-N3-q2 (identity — resolved to existing platform credential), CA1-N5-q1 (continuity vs replication — resolved to external-witness pattern with independent countersigner infrastructure).

---

## 3 · Doc14-020 · rights-unclear material (verbatim, notes/requirements_register_17docs.md line 160)

> **Doc14-020** ← C4-054 §38 · Rights-unclear material is a first-class state — ADMITS to inspection but does NOT ADMIT to extraction for external delivery until the rights state is resolved. Status **OPEN-SLOT** (rights-state grammar for the mechanism-side "unclear" verdict is not yet in `contracts/` inventory · owner policy pending on the resolution ceremony · non-blocking).

**Owner Wave E ruling reduces the OPEN-SLOT to a concrete mechanism:** quarantine store + review queue + release/refuse — wired into the training-material admit path (admit refuses to pass rights-unclear material through; it quarantines with receipt).

---

## 4 · Doc18-006 · A18.6 async skill delivery (verbatim, notes/requirements_register_20docs.md lines 134-137)

> **Doc18-006** ← A18.6 · Single-shot pilot for enterprise sales; Owner ratifies before deployment. Status PROPOSED · Build **PROPOSED** · Carrying phase: **Owner ratification** (deferred to post-W11 per Owner CP3-open deprioritization: "defer A18.6 async delivery entirely").

**Owner Wave E ruling supersedes the CP3-open deprioritization:** ADOPT per the proven platform pattern already implemented at `services/service_1/dispatch.py` Phase 5 (`ROUTE_PHASE_5_ASYNC_DELIVERY_UNBUILT` → `contracts.async_delivery_accepted.AsyncDeliveryAccepted_v0` at fresh-fork admission). Register row moves PROPOSED → RULED-ADOPTED.

---

## 5 · A17.15 rights-lapse provenance mechanism (context for N3 model-flagging)

**Register row (verbatim, notes/requirements_register_20docs.md lines 103-106):**
> **Doc17-015** ← A17.15 · Interference weighting trigger: when to promote I from binary to weighted; proposed default is calibration data showing misleading strata consistently cost more than one unit of capacity. Status OPEN · Build OPEN-SLOT · Carrying phase: Owner ruling pending.

**Note on the owner's reference:** the N3 ruling refers to "the same provenance mechanism as A17.15 rights-lapse". A17.15 in the register itself is about interference weighting; the "rights-lapse" pattern being referenced is the same PROVENANCE mechanism (flag → schedule action OR document residual exposure) that A17.15 enables. Wave E implementation adopts the pattern in a new record class `RightsLapseFlag_v0` scoped to the erasure use-case; A17.15's own OPEN-SLOT policy question is unaffected (interference weighting policy is separate).

---

## 6 · Watch event grammar (verbatim, `backend/services/watch/macho.py` + `backend/services/watch/mkono.py`)

**MachoVerdict.verdict_class (backend/services/watch/macho.py line 99):**
```python
verdict_class: Literal["externally_steerable", "structural_certainty"]
```

**MachoVerdict.intensity (line 108):**
```python
intensity: Literal["noted", "elevated", "severe"]
```

**Mkono action mapping (backend/services/watch/mkono.py):**
- externally_steerable + noted → `annotate` (mark record, change nothing)
- externally_steerable + elevated → `shape` (score-shaped)
- externally_steerable + severe → `contain` (reversible containment, whatever its score — Canon 8 §Line 30 verbatim)
- structural_certainty (any intensity) → `sever` (holds rather than expires — Canon 8 §Line 99)

**Owner's N2 mapping (verbatim, Wave E scope §1):**
> map "hard line crossed" onto the existing Watch event grammar (containment failure / actual exfiltration / unreceipted crossing), never onto successful catches. Contained/shaped events are the Watch working and MUST NOT trigger notification — encode that as an invariant, not a comment.

**Wave E interpretation (mechanism-side, quoting the Watch code):**
- `containment failure` = a containment MkonoAction whose expiry reconciliation lands as `diverges` (Canon 8 §18 · MkonoAction terminal reconciliation vocabulary reuse from ContinuityAttestation_v0.outcome).
- `actual exfiltration` = a `sever` action (structural_certainty verdict → sever) — the terminal Watch action; anything below (annotate/shape/contain) is the Watch working.
- `unreceipted crossing` = a chokepoint crossing that ends without a `CrossingReceipt` on record (services/chokepoint/__init__.py invariant test suite catches this class today).

**Contained/shaped events (NOT breach-notifiable):** `annotate`, `shape`, `contain`-with-reversible-expiry, mirage encounters that expire cleanly, staleness reflags. These are Canon 8 §14 "the Watch operating at machine speed, invisibly to legitimate work."

---

## 7 · CA1 audit lines from the register (verbatim rows for the sweep, §6 of scope)

**Doc02-020 · CA1-007 (line 82):**
> Dry-run preview between Review and Adopt. Status **BUILD** (no equivalent surface exists).

**Doc02-020a · CA1-001 (line 83):**
> Audit-trail Overview names "2+ independently-governed units" when an answer drew on such. Status **BUILD**.

**Doc06-016 · CA1-002 (line 105):**
> Audit line names how many available source units were served. Status **BUILD**.

**Doc07-019 · CA1-003 (line 109):**
> Densification stat + per-turn warm/fresh tag (partial closure per Addendum §1). Status **BUILD** on the surface.

**Doc15-085 · CA1-006 (line 174):**
> Watch's self-contained exception + external witness state line. Status **BUILD** (Watch mechanism).

**Doc15-087 · CA1-012 (line 176):**
> Watch staleness-flagging extended to rulebooks + baselines. Status **BUILD**.

**Sweep rule:** anything that can be closed with a small honest wire in Wave E scope, close it; anything blocking on canon/owner ruling or a large mechanism, class-attribute honestly (retain BUILD/PARTIAL status with named blocker) in the Wave E close report.

---

## 8 · DigiCow PII posture (verbatim from phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json)

**Data source:** `aws.rds.db-restore-603-cluster.digicow_live` · region `eu-west-1`.

**Table:** `digicow_live.ussd_users` — owner's declared row count 2.28M (external knowledge, verified in AWS RDS).

**Column names carrying farmer PII (measured from the connection record):**
- `farmer_mobile_no` — direct PII (phone number, MSISDN class).
- `dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer` — occupation-class attributes on a named individual; behavioral-adjacent.
- `farmer_answer` — user-generated free-text; may contain uncontrolled PII inside answers.

**Response-boundary sanitizer contract (verbatim, `backend/services/governance/router.py` lines 36-46):**
```python
_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
}


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v for k, v in d.items()
        if k not in _BANNED_FIELDS and not k.endswith("_raw")
    }
```

**Wave E CP-E7 mandate:** verify sanitizer coverage on every new Wave E surface (N2/N3/N5/Doc14-020 routers) + confirm the DigiCow PII columns above are handled through the rights-declared/pii-declared gates already established at connect-time (services/connect/sample_fixture_seeder.py: `"rights_declared": "internal_only"`, `"pii_posture": "pseudonymize"`). Receipt in `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_wave_e_pii_sweep.log`.

---

## 9 · CP partition (dependency-ordered)

**CP-E1 · CA1-N5 ledger continuity** (independent · foundational · external-witness handle used by CP-E2).
- Contract: ContinuityAttestation_v0 already exists (backend/contracts/continuity_attestation.py) with sentinel-guarded policy fields.
- Config layer: quarterly cadence as DEFAULT-class (proposal-class distinction PRESERVED in a new config file `backend/services/n_series/continuity_policy.v0.json`).
- Independence enforcement: countersigner (`attested_by`) MUST reference a WitnessIdentity_v0 whose `infrastructure_ref` does not equal the primary ledger writer's infrastructure_ref. New invariant test: `test_continuity_countersigner_independent_infrastructure`.
- Surface: existing `/api/watch/` extended with GET/POST `/api/watch/continuity` (attestation ceremony lives on Watch per Canon 8 §9 witness).
- Wire paths: `POST /api/watch/continuity`, `GET /api/watch/continuity`.
- Ship-Manifest DoD: 2 wire paths added to `MUST_BE_LIVE_ROUTES`.

**CP-E2 · CA1-N2 breach notification** (depends on CP-E1 · witness handle).
- Contract extension: add `trigger_event_class: Literal["containment_failure","actual_exfiltration","unreceipted_crossing"]` + `notify_deadline: str` (72h from `triggered_at`) + `recipient_dpo_id` + `recipient_witness_id` + `alert_channel_receipts` (list of file drops) to BreachNotification_v0.
- Policy config: `n_series/breach_policy.v0.json` — q1=refusal_bypass_only (hard line only), q2=independent_authority (DPO + witness), q3=actor_ids_masked (Canon 8 default), q4=one_per_breach.
- Invariant test: `test_contained_shaped_annotate_events_never_trigger_breach_notification`.
- Real-time alert channel: file drop to `phase0/breach_alerts/{recipient_id}/{notification_id}.json` alongside the ledger record (structural — real-time is bookmarkable, not push).
- Wire paths: `POST /api/n_series/breach` (extended · existing), `GET /api/n_series/breach` (existing) — no NEW paths, but semantics move refuse → enforcement. Ship-Manifest DoD note: no new wire paths → the CP-E2 commit adds only invariant tests + contract fields + policy config.

**CP-E3 · CA1-N3 access & erasure** (independent).
- Contract extension: add `requestor_class: Literal["named_customer","named_employee"]` (refuse third-party) + `platform_credential_ref` (existing credential ref) + `model_flag_ids` (list of RightsLapseFlag_v0 ids emitted) + `crossing_receipt_ref` (custody chokepoint receipt for the erasure operation).
- New contract: `RightsLapseFlag_v0` (in `backend/contracts/rights_lapse_flag_v0.py`) — model_id + subject_ref + resolution: `"scheduled_retrain"|"documented_residual"` + created_at.
- Policy config: `n_series/erasure_policy.v0.json` — q1=raw_and_five_ring_units, q2=existing_platform_credential (add new sentinel value), q3=erasure_wins_over_ca1_n1 (default per owner "REAL erasure").
- Erasure operation routes through chokepoint: `services.chokepoint.write_crossing_receipt` MUST fire for every erasure fire.
- Invariant tests: `test_erasure_refuses_third_party_requestor`, `test_erasure_emits_rights_lapse_flag_for_each_trained_model`, `test_erasure_routes_through_chokepoint_with_crossing_receipt`.
- Wire paths: `POST /api/n_series/erasure` (extended · existing), `GET /api/n_series/erasure` (existing), NEW `GET /api/n_series/rights_lapse_flags` (list flags).
- Ship-Manifest DoD: 1 new wire path added to `MUST_BE_LIVE_ROUTES`.

**CP-E4 · Doc14-020 QUARANTINE-pending-review** (independent).
- New service: `backend/services/rights_quarantine/`
  - `store.py` — file-system store at `phase0/rights_quarantine/{admit_id}.json`.
  - `router.py` — endpoints below.
- Contract addition: extend `TrainingMaterialAdmit_v0` with `rights_state: Literal["clear","unclear","declared"]` (default: `"declared"`; owner-culture: existing DigiCow flow explicitly declares).
- Wire in the admit path: `services/training_runner/admit_material` REFUSES with structured refusal if `rights_state == "unclear"`; the caller path routes to `services.rights_quarantine.quarantine_admit` which writes the record.
- Invariant tests: `test_admit_material_refuses_rights_unclear`, `test_rights_unclear_material_writes_quarantine_record`, `test_rights_quarantine_release_becomes_admit`, `test_rights_quarantine_refuse_becomes_terminal_no_admit`.
- Wire paths: `GET /api/rights_quarantine`, `GET /api/rights_quarantine/{admit_id}`, `POST /api/rights_quarantine/{admit_id}/release`, `POST /api/rights_quarantine/{admit_id}/refuse`.
- SPA routes: `/rights-quarantine` (list + detail) belongs on the existing `/data` (Data Console) surface per owner ruling ("belong on existing surfaces (governance/watch/data) unless canon names a dedicated surface"). Canon does NOT name a dedicated surface for rights-quarantine; it lives on `/data` as a sub-tab.
- Ship-Manifest DoD: 4 new wire paths + 1 SPA route.

**CP-E5 · A18.6 async skill delivery ADOPT** (register move + tiny adoption trace).
- Register row `Doc18-006` moves PROPOSED → RULED-ADOPTED with citation to `services/service_1/dispatch.py:117` (`AsyncDeliveryAccepted_v0` at fresh-fork admission) as the proven platform pattern the owner cited.
- Enforcement-side: add one invariant test `test_a18_6_async_delivery_pattern_ratified_in_register` that reads the register row and asserts status == RULED-ADOPTED.
- Wire paths: none (pattern already wired).
- Ship-Manifest DoD: no route changes.

**CP-E6 · CA1 audit sweep (001/002/003/006/007/012)** (independent).
- For each row: read the current implementation state, close if a small honest wire suffices, otherwise class-attribute honestly with a named blocker.
- 001 (audit trail 2+ independently-governed units): audit trail overview surface addition — a text line naming the count when applicable. Class BUILD if the audit-trail service surface exists; PARTIAL if not.
- 002 (audit line names units-served count): same class as 001.
- 003 (densification stat + warm/fresh tag): tag exists in memory service; audit line addition.
- 006 (Watch self-contained + external witness state line): CP-E1's `/api/watch/continuity` GET response includes this state line — close inside CP-E1.
- 007 (dry-run preview): existing `services/chokepoint/dry_run.py` — surface the "between Review and Adopt" placement in a router if missing.
- 012 (Watch staleness-flagging extended to rulebooks + baselines): existing `services/watch/route_staleness_flag.py` — extend applies_to grammar if missing.
- Wire paths: any wire added carries per-CP receipt.
- Ship-Manifest DoD: variable; measured at CP-E6 close.

**CP-E7 · DigiCow PII sanitizer sweep + receipt** (blocking · final gate before close).
- Enumerate every new Wave E router; test each for `_sanitize` boundary application; test the sanitizer strips DigiCow PII field names when they leak into an internal record.
- Add DigiCow-specific PII column names (`farmer_mobile_no`) to the sanitizer's banned-set (or a `_PII_BANNED_FIELDS` disjoint set) to catch accidental echoes.
- Invariant test: `test_wave_e_routers_apply_response_boundary_sanitizer`.
- Receipt at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_wave_e_pii_sweep.log`.

**CP-E8 · Wave E close** (final).
- Register moves: N-series rows (N2/N3/N5) → DONE, Doc14-020 → DONE, Doc18-006 → RULED-ADOPTED, CA1-001/002/003/006/007/012 → measured status.
- `notes/waveE_close_report.md` — register moves + composite delta + downgrade list.
- Double-run BASELINE_GUARD=1 proof (permanent standard: two consecutive green + external third run).
- STATE mirror commit (NEXT.md + DECISIONS.md).
- Preliminary composite % note (still LOCKS at Wave F per Wave-D-ratification flag).

---

## 10 · Halt triggers (owner ruling verbatim)

> "standard halt triggers (non-config blocker / spec contradiction / guard trip / count drift)"

- **Non-config blocker** — a required capability requires code/mechanism that cannot land in this CP's scope without expanding the ruling. Report the item, continue the rest of the CP.
- **Spec contradiction** — two verbatim canon quotes contradict, or a ruling contradicts a canon quote. Halt the item, name the contradiction verbatim, continue the rest of the CP.
- **Guard trip** — `BASELINE_GUARD=1` fails at CP close, or the ratchet slips backwards on `passed`, or `baseline_failures` non-zero, or `quarantined` diverges from expected. HALT the whole CP, do NOT commit, report verbatim tally.
- **Count drift** — the two consecutive CP-close runs disagree on any of `passed / baseline-failures-remaining / quarantined / skipped`. HALT, do NOT proceed to next CP, report both tallies verbatim.

---

## 11 · Ship-Manifest DoD (permanent standard, owner ruling)

Every commit that ships a new wire path MUST include the wire path in `MUST_BE_LIVE_ROUTES` in the SAME commit (invariant test `test_must_be_live_routes_all_actually_live` enforces). Every new SPA route MUST land in `MUST_BE_LIVE_SPA_ROUTES` in the SAME commit (invariant test `test_must_be_live_spa_routes_all_render_deterministically` enforces).

---

## 12 · Wave E close standard (Wave-D-ratification permanent standard)

Two consecutive green full-suite `BASELINE_GUARD=1` receipts (IDENTICAL tally on `passed`/`baseline-failures-remaining`/`quarantined`/`skipped` + `status: OK` on BOTH) + owner external third run. Any deviation = HALT-AND-REPORT, no absorption.

**Preliminary composite % note:** reporting number only; locks at Wave F per the CP-D9→Wave-D-RATIFIED flag section in STATE/DECISIONS.md.

---

**Standing hold posture:** SSH interrupt priority remains over EVERYTHING per owner's Wave E GO ruling.
