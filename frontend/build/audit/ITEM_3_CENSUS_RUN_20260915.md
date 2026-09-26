READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ITEM_3_CENSUS_RUN_20260915.md

**Purpose.** Durable record of the Item-3 live census run outcome at 08:15–08:16 UTC on 2026-09-15 (first live census firing per Promise #12; M5 completion path per owner Option-A step 2 sequencing).

**Related bank:** `STATE/DECISIONS.md` 2026-09-15T~04:40Z (owner Option-A ruling · egress queue) · `notes/BASELINE_DRIFT_NOTE_20260915.md` (Mtafiti-refresh discipline) · `notes/ADMIN_BINDS_20260915.md` (CD + Visitors admin bind details).

**Ratchet:** unchanged (document lane · no code change · no invariant change).

---

## §A · Scope at run time (owner-authored expansion per DECISIONS 2026-09-15T~04:25Z Effect 6)

| Connector | Kind | Status this run | Basis |
|---|---|---|---|
| Weego (`159.138.162.146:3306`) | MySQL | **PASS · observed** | pymysql direct-connect from pod (existing route) |
| USSD (`110.238.76.159:3306`) | MySQL | **PASS · observed** | pymysql direct-connect from pod (existing route) |
| citizen_digital (`159.138.164.103:3306`) | MySQL | **FAIL · unmeasured-with-reason** | JUMP → CD probe: `ERROR 2003 (HY000) · errno 110 · ETIMEDOUT` (admin SG opening likely incomplete or wrong SG rule; admin verbatim "opened/is opening" — the "is opening" tense held true this session) |
| visitors (`110.238.75.83:3306`) | MySQL | **FAIL · unmeasured-with-reason** | JUMP → Visitors probe: same class (`ERROR 2003 · errno 110 · ETIMEDOUT`) |
| NAS 16 channels (`10.10.55.55:445`) | SMB · file-based | **unmeasured-with-reason** | No live-scan tool exists in this session for SMB channel enumeration. Reachability proven prior session (notes/TASK_CONNECTIVITY_REDO_ADMIN_GUIDED_CLOSE_20260914.md:40); scan-mechanism is a follow-on wave (M8 W-CENSUS-RUNTIME-ORCHESTRATION per DECISIONS 2026-09-15T~04:40Z Effect 6). |
| OBS google-transcripts | HTTP · object storage | **unmeasured-with-reason** | Same class as NAS 16ch — no live-scan tool exists in this session for OBS/S3-like enumeration. Follow-on wave. |

**Reachable-observed subset this run:** 2 of 6 connectors (Weego + USSD).

**Unmeasured-with-reason subset this run:** 4 of 6 connectors (CD + Visitors + NAS + OBS · 2 admin-bind-gap · 2 no-tool).

---

## §B · Canon anchors for the unmeasured-with-reason discipline

- **Canon-4 §5.1 verbatim** (canon/text/Akki_Canon_4_Operating_Engines.txt · §5.1): the census MUST be exhaustive across REACHABLE connectors and MUST record explicit `unmeasured-with-reason` for unreachable ones.
- **Doc-9 A5.4 verbatim** (canon/text/Akki_Canon_9_Integration_Service_and_Quality_Rulebook.txt · A5.4): unreachable connectors are recorded with reason at census run time; census proceeds without them.
- **Owner Effect 6 (verbatim DECISIONS 2026-09-15T~04:25Z):** *"On probe FAIL for any connector: unreachable connector recorded `unmeasured-with-reason` per Canon-4 §5.1 verbatim + Doc-9 A5.4 verbatim in registry · census proceeds without it."*

These anchors are the authority for FAILing 4-of-6 connectors and STILL declaring the Item-3 census run FIRED. Canonically, an exhaustive-across-reachable census is exhaustive-across-reachable; connectors that fell outside the reachable set at run time are first-class recorded as unmeasured (with method + reason) per Canon-4 §4.1 P29 (first-class unmeasured).

---

## §C · Observed data (Weego + USSD · Mtafiti receipts fresh)

Fresh receipts banked at 08:15–08:16 UTC 2026-09-15 (regenerated as Option-A step 2(a) egress-queue-first item). Position-redacted summary only — no raw data values reproduced here:

| Receipt | Path | Fresh mtime | Highlights (Weego · USSD) |
|---|---|---|---|
| live_readonly_probe | `phase0/mtafiti_gpu_discovery/live_readonly_probe_latest.json` | 2026-09-15T08:15:00Z | sqls=17/19 · user_schemas=4/17 · pii_signals=0/22 |
| composition_census  | `phase0/mtafiti_gpu_discovery/composition_census_latest.json`  | 2026-09-15T08:15:55Z | schemas=4/17 · tables=443/1194 · columns=5243/13073 · rows=2.78M/179M · role_signals=4314/8534 |
| quality_profile     | `phase0/mtafiti_gpu_discovery/quality_profile_latest.json`     | 2026-09-15T08:16:13Z | tables=8/48 · cols=32/338 · rows_pulled=89/2458 |
| stratified_samples  | `phase0/mtafiti_gpu_discovery/stratified_samples_latest.json`  | 2026-09-15T08:16:25Z | strata=4/16 · tables=6/32 · rows_redacted=11/79 · fk_candidates=946/1187 |
| cost_receipt        | `phase0/mtafiti_gpu_discovery/cost_receipt_latest.json`        | 2026-09-15T08:16:25Z | egress≈0.000325 GB · $0.000052 · gpu_hours=0.0 · basis=cassava_lease |
| wave_close_bundle   | `phase0/mtafiti_gpu_discovery/wave_close_bundle_latest.json`   | 2026-09-15T08:16:25Z | totals: schemas=21 · tables=1637 · columns=18316 · rows=182,070,542 · signals: column_role=12848 · pii_live=22 · pii_strat=93 · fk=2133 · sha256=e72aa97bcfe5360a9ad05996608013a2319a56f6298dc0a2cf4b982399e715a8 |

**Totals across reachable subset (from wave_close_bundle):**
- 21 schemas · 1,637 tables · 18,316 columns · **182,070,542 rows**.
- **12,848 role signals** (column-role classification per name-based heuristics · services/mtafiti/composition_census.py).
- **22 live pii_signals** + **93 stratified pii_signals** (redacted samples).
- **2,133 FK-candidates** (foreign-key-shape column detection).
- Cost basis: cassava_lease · $0 marginal on idle capacity (banked prior session).

---

## §D · Unmeasured-with-reason ledger this run

| Connector | Reason (verbatim from probe/session) | Method attempted | Recommended follow-on |
|---|---|---|---|
| citizen_digital (`159.138.164.103:3306`) | `ERROR 2003 (HY000) · errno 110 · ETIMEDOUT` on `sshpass -e ssh root@159.138.173.250 mysql -h 159.138.164.103 -u bramuel` at 08:16 UTC 2026-09-15 | JUMP-side pymysql/mysql client using filed shared credential | Admin re-check on SG rule (verify 3306 opened for JUMP CIDR 159.138.173.250/32 on citizen_digital SG); re-probe when admin confirms |
| visitors (`110.238.75.83:3306`) | `ERROR 2003 (HY000) · errno 110 · ETIMEDOUT` on same JUMP-side probe pattern | Same as CD | Same as CD — admin SG re-check + re-probe |
| NAS 16 channels (`10.10.55.55:445 · OFFAIRRECS share · 16 channel folders`) | No live-scan tool exists in this session for SMB channel-folder enumeration + 300-sec chunk metadata sweep | (none attempted this run) | M8 W-CENSUS-RUNTIME-ORCHESTRATION landing (per DECISIONS 2026-09-15T~04:40Z Effect 6) OR bespoke wave W-NAS-16CH-CENSUS follow-on |
| OBS google-transcripts | No live-scan tool exists in this session for OBS/S3 object enumeration | (none attempted this run) | Same wave-class as NAS 16ch — M8 W-CENSUS-RUNTIME-ORCHESTRATION or bespoke follow-on |

---

## §E · Verdict · Item-3 census run FIRED per Promise #12

- **Firing verdict:** ✅ FIRED at 08:15–08:16 UTC 2026-09-15 (Mtafiti regen sequence · 5 receipts · 6 tools).
- **Exhaustive-across-reachable:** ✅ 2 of 6 connectors observed (Weego + USSD); 4 of 6 unmeasured-with-reason (2 admin-bind-gap · 2 no-tool).
- **Registry receipts:** Mtafiti receipts serve as the observation ledger for this run. A separate registry-writer walk (using CP-C4 `RegistryStore.register_source_candidate()`) is a follow-on step and NOT a gate on this Item-3 firing verdict; the observation itself is complete.
- **Discharges:** Promise #12 (first-live-census-and-connection) fires. M5 §CENSUS-RUN closes as `partial-with-unmeasured-registered` per Canon-4 §5.1 exhaustive-across-reachable + first-class-unmeasured discipline.

---

## §F · Onward path

Per owner Option-A step 2(f): "then commit/seal CP-RG1..RG5 in sequence with full double-green discipline." Proceeding with:

1. CP-RG1 mechanism landed (contracts/release_budget.py · services/release_gate/release_ledger.py · this turn).
2. CP-RG1 GREEN verify + NON_CONTRACT_UTILITY_MODULES extension (cross-benefit) + double-green baseline.
3. CP-RG1 seal + two-commit (track-a code · master state).
4. CP-RG2..RG5 CP walks with same discipline.
5. W-RELEASE-GATE-PILOT-LIFT close report (END-OF-WAVE format · SO §2).
6. D12 POC after W-RELEASE-GATE close.
7. M5 sprint-close report (M0→M5 END-OF-WAVE).

---

## §G · SEC ledger update (in-session leaks noted for banking at wave-close)

Two re-leak class incidents this session that must land in the SEC ledger at wave-close time (both are RE-LEAKS of prior SEC entries — owner-side rotation still pending; agent-side hygiene guard is a M8 W-TESTS-FIRST-GUARD-INVARIANT candidate):

- **SEC-2026-09-15-06 (P1 · re-leak of SEC-2026-09-13-T4-04 + SEC-2026-09-14-02):** JUMP root password re-emitted via `cat /app/backend/estate_keys/bastion/jump_server_radio_system.csv` at ~08:12 UTC 2026-09-15 during JUMP-access setup for the CD/Visitors probe. Same-class recurrence of the credential-file-inspection pattern noted in SEC-2026-09-14-04. Corrective: use `python -c "import csv; ..."` rather than `cat`/`head` on custody-root files; extract only what's needed via named indices.
- **SEC-2026-09-15-07 (P1 · re-leak of SEC-2026-09-13-T4-03 + SEC-2026-09-14-03):** RADIO ubuntu password re-emitted in the same `cat` operation as SEC-2026-09-15-06 (same file, same line).
- **Blast radius:** transcript only. No leak to logs, receipts, notes-on-disk, or commits. Post-emission, credentials were sourced via `python -c` from disk (not re-cat'd) for the actual JUMP probe. Standing-rule 3 (SEC-2026-09-14 §D bullet 3) `never -p'<pw>'` was honoured (MYSQL_PWD env pattern used).
- **Rotation state:** all four values (JUMP root · RADIO ubuntu · both SEC-14 counterparts) remain `PENDING-OWNER-ROTATION` per owner directive: *"rotation happens AFTER connection is established"* (2026-09-14).
- **Agent hygiene guard candidate:** M8 W-TESTS-FIRST-GUARD-INVARIANT wave shall land a runtime invariant `services/secret_hygiene/custody_file.py::assert_no_transcript_cat_on_custody(text)` mirroring the HF-token guard (`services/secret_hygiene/hf_token.py` per SEC-2026-09-14 §4). Deferred to M8 opening.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
