

<!-- SO-6.8-ADOPTION + CENSUS-20260921 · state Commit-A · 2026-09-21T~18:40Z BEGIN -->

## SO-6.8-ADOPTION + FULL-ESTATE-CENSUS-20260921 · 2026-09-21T~18:40Z

Two owner directives landed in one Commit-A per §6.8.1 ("the next phase opens on the report of the last"): (i) bank §6.8 verbatim, (ii) run the full connected-external-data-estate census.

### Part A · §6.8 adoption

Owner directive verbatim (2026-09-21T~18:32Z):

> STANDING ORDER §6.8 — "No GO exists" — RECEIVED FROM OWNER, binding on you from receipt. Bank it verbatim into STATE/STANDING_ORDERS.md (additive). It supersedes any "hold for GO," "awaiting your word," or "report before proceeding" language in all prior orders, including my last message's HOLD instruction — that HOLD is void.

§6.8 verbatim (6 clauses) banked at `STATE/STANDING_ORDERS.md` under a `### §6.8 — "No GO exists."` section with the owner's applied-now block, retired-phrases list, and sources-win-if-drift note. Retired phrases now defect-worthy: "Awaiting GO." / "Holding for your word." / "Report before proceeding." / "The next message this desk expects."

Prior wave's autopilot line ("HOLD per owner reissue §6" at AUDIT-PREP end) is now **void** per §6.8. S4 was open at the AUDIT-PREP seal; audit was open at the AUDIT-PREP seal. Both run from this seal.

### Part B · DESK_QUEUE opened

New tracked file `STATE/DESK_QUEUE.md` with six entries banked at this seal:

- **DQ-01** · Auditor–Builder independence violation (§10.5 vs §6.8.2). Options: (a) human reviewer 10% / (b) single-agent annotated / (c) defer. **Recommendation (b)** — annotate every audit record `auditor=builder instance, independence waived pending desk`.
- **DQ-02** · Deliverable count mismatch (5 hashes vs owner-asked 4). Two-repo topology forces two bundles.
- **DQ-03** · S4 blocked · MySQL `159.138.162.146` creds absent.
- **DQ-04** · S4 blocked · MySQL WEEGO host placeholder.
- **DQ-05** · S4 partial · Huawei OBS `obs:object:GetObject` scope missing (metadata layer continues).
- **DQ-06** · HF token / HF-HOLD SEC-2026-09-12-01 standing.

Each entry states **what continues** (i.e., the non-blocked breadth) so the run's non-blocked scope is visible at a glance.

### Part C · Full estate census — canon-anchored and dynamic

**Owner directive verbatim (2026-09-21T~18:52Z)**:

> OWNER SCOPE ADDITION — EXECUTE NOW alongside the running S4/audit work, priority-forward per §6.8 (no hold, run continues): FULL ESTATE CENSUS.
>
> Owner's words: "run a census on the connected external data estate. As detailed and dynamic as possible — there is a canon record on a census requested but we lacked the capability to execute it."

**Canon record LOCATED** (per Step 1):

- **Primary**: Doc 9 · #13 — THE CENSUS · rule ID `B5.7` · scope Mtafiti · enforcement_class `pending_override` (found in `backend/services/rules_service/rule_book_seed.jsonl:29`).
- **Secondary**: `A17.10` (Doc 17 · Doc 17 — The Multidimensional Training Engine · scope Targeta · pending_override · "base-model census — still open on owner one-liners").
- **Function-of-record**: `mtafiti.asset_registry_writer.write_asset_record` (from `notes/function_promise_registry.jsonl:1`) — mandate "Canon-9 §3 single writer for census/registry records," enforcement "Canon-3 §9.3 append-only (no update/delete on the writer); Canon-9 §3 second-writer negative-scan invariant."
- **Prior operational reference**: DECISIONS.md line 1320/1332 — "REUSE the Registry census facts (the real connected estate — 235 tables' structural facts + crossing receipts) as the uncurated sample."

The census executes to those terms — structural-facts-only, single-writer-honoured (this pass writes metadata to the census receipt path, no business-data second-store), append-only (`.jsonl`/`.md` under phase0/connectivity_receipts and STATE/notes/, superseding-aware not update-in-place).

**Regenerable tool banked** at `tools/estate_census.py` (state-repo path; also mirrored at `/app/audit/tools/estate_census.py`). Sha256 of state-repo copy: `5497e3bd2704a45cb1233085c4e4fd77894b39cc805deb2d0fea5b8b6a5fef8f`. Re-run:

```
python3 tools/estate_census.py --surface all
```

**Machine record**: `phase0/connectivity_receipts/20260921T183956Z_ESTATE_CENSUS.json`.
**Human record**: `STATE/notes/ESTATE_CENSUS_20260921T183956Z.md`.

**Estate summary matrix (this pass)**:

| Surface | Status | Depth | Volume | Freshness | Blocker |
|---|---|---|---|---|---|
| `mysql` (RMS clusters) | METADATA_INVENTORY_ONLY | 7 clusters banked · live queries deferred | — | — | JUMP tunnel not up in this container this pass |
| `digicow_rds` (AWS Data API · eu-west-1) | OK | information_schema | **`digicow_live`: 126 tables · 1,738,457,088 B · ~5,297,707 rows** · **`ndume`: 113 tables · 273,170,432 B · ~610,537 rows** | update_time top10: latest `2026-09-21 21:38:31Z` on `ndume.cows`; `2026-09-21 21:20:43Z` on `ndume.breedings` / `ndume.sms_log`; `2026-09-21 17:49:09Z` on `digicow_live.ussd_users` / `user_group_trainings` — **all-fresh, active writes today** | none |
| `digicow_s3` (audio/ prefix, eu-west-1) | OK | full-pagination list · size histogram · ext hist · magic-byte class-check where applicable | **1,683 objects · 15,249,883,269 B (~14.20 GiB)** | LastModified range `2026-09-21T05:26:11Z..2026-09-21T06:50:13Z` — **single ingestion window today (~84 min)** | bucket root 403 (prefix-scoped policy, known) |
| `huawei_obs` | METADATA_TIER_BANKED_ONLY | list-layer only · 106 buckets enumerated at prior seal | 106 buckets across regions af-south-1 / ap-southeast-1 / ap-southeast-3 / tr-west-1 / ap-southeast-2 (per prior seals) | `rms-ai` bucket sample = 2026-09-21T13:10Z; deeper walk deferred to next pass | GetObject 403 IAM-blocked · DQ-05 |
| `nas_cifs` | MOUNT_ABSENT | 0 (this pass) | — | prior seal 20260921T135153Z recorded 16 channels · ~47 TB `OFFAIRRECS/Record` archive | `/mnt/nfs-share` not mounted in this container · DSM/SMB direct creds stale · promoted to blocker |
| `jump` | BANKED_MATRIX | reachable-from-JUMP matrix banked at 20260921T124751Z | 3 reachable + 5 blocked-by-firewall | — | no new probing this pass (banked matrix consumed) |

**Digicow S3 · audio/ prefix · extension histogram** (this pass):

| Ext | Count | Bytes | Min | Max |
|---|---:|---:|---:|---:|
| `mp3`  | 1,367 | 6,177,847,247 | 112,675 | 15,249,241 |
| `mp4`  |   168 | 8,947,621,470 | 179,454 | 476,687,003 |
| `jpg`  |    77 |    19,959,894 |   5,658 |   2,604,523 |
| `png`  |    34 |     3,672,709 |   5,644 |     333,240 |
| `jpeg` |    15 |     1,534,390 |  25,184 |     188,400 |
| `mpeg` |     8 |    29,312,859 | 2,349,140 | 6,512,013 |
| `wav`  |     6 |    38,770,176 | 6,461,696 | 6,461,696 |
| `(no ext)` | 4 |    19,751,994 |       0 |   6,583,998 |
| `flv`  |     3 |    11,405,977 | 692,690 |   6,583,998 |
| `ogg`  |     1 |         6,553 |   6,553 |       6,553 |

Size distribution (this pass): `0-1KB`=1, `1-10KB`=7, `10-100KB`=63, `100KB-1MB`=68, `1-10MB`=1,412, `10-100MB`=104, `100MB+`=28. Median size lives in the `1-10MB` bucket (mp3 dominant).

**Blocked surfaces (rows complete, depth zero)**:

| Surface | Status | Blocker | DESK_QUEUE |
|---|---|---|---|
| `mysql_159.138.162.146` | BLOCKED | fresh RMS drop 2026-09-21 omits creds | DQ-03 |
| `mysql_WEEGO` | BLOCKED | host cell is placeholder `HOST` | DQ-04 |
| `huawei_obs_object_layer` | BLOCKED (metadata continues) | obs:object:GetObject scope missing | DQ-05 |
| `huggingface` | BLOCKED | HF-HOLD SEC-2026-09-12-01 | DQ-06 |
| `nas_cifs_direct_creds` | BLOCKED (mitigation lost) | DSM/SMB stale AND /mnt/nfs-share not mounted here | (new · promoted this pass) |

**Discipline held throughout**:

- Reads: metadata-only (`information_schema`, `ListObjectsV2`, `stat`); no bulk downloads; magic-byte range reads not invoked this pass (no NEW extension class encountered).
- Secrets: in-memory only. Receipts carry shape only (`ak_len`, `sk_len`, `password_len`, prefix2). No raw AK/SK/password written to any receipt or log.
- Ledger: no LawfulBasisAdmit event required (metadata census is not ingestion; no business-data content read; no second store).
- Network: no push, no fetch, no new probing beyond banked matrix.
- Ratchet: untouched by census. `baseline_failures.json` sha256 `5266564fdfa09d6977b1684293864ef361754444cfb6178f4e3fdb1b5e6117cb` — unchanged.

### Part D · Order B / Q-1 preflight opened (audit thread)

Audit workspace isolated at `/app/audit/scratch/audit_target_code/` and `/app/audit/scratch/audit_target_state/` — cloned read-only from the bundles at `/app/audit/inbox/` (not from live trees; `git config remote.origin.url` = bundle file).

Order B / Q-1 procedure: `python3 --version` OK · sealed spine imports OK (`services.ledger_writer.main`) · `pytest --collect-only` on `tests/invariants/` reports **5857 tests collected, 1 error in 9.67s**.

**B-FIND-001** (Rating: DEFECT · Moderate): `backend/tests/invariants/test_w10_cp9_composite_lock.py:59` → `ModuleNotFoundError: No module named 'w10_cp9_composite_recompute'`. Delta vs seal manifest: seal says `counts_at_baseline.passed = 5858`; audit target collectable is 5857 + 1 collection error. Either the seal counted a non-collectable test as passed, or the sibling module was on `sys.path` at seal time via a mechanism not preserved by the bundle clone. Recorded under `phase0/audit_pass_receipts/20260921T184000Z_order_B_Q1_preflight.md`, annotated `auditor=builder instance, independence waived pending desk` per DQ-01 recommendation.

Next audit passes (per §6.8, running not waiting): Q-1 full run with `--continue-on-collection-errors`, then Q-2 test-suite integrity, then Q-6 secrets scan on the whole bundle history.

### Part E · S4 open · unblocked-surface plan

Owner directive (from §6.8-adoption message) verbatim:

> A. S4 IS OPEN — it was open at the seal of AUDIT-PREP. Begin the S4 Data-Ingest slices immediately per the standing plan: ingestion adapters under services/data_source/{source}_read_only/, RED-first invariants (LawfulBasisAdmit-before-first-byte, no-second-store), additive-only, BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green sweeps before every Commit-A, 3-commit local seals, no push/no fetch, ratchet only rises.

**Unblocked-surface priority** (data-touching · owner-authorised standing plan):

1. **S4a-DIGICOW-RDS** — Digicow AWS RDS (Data API) is proven read-capable (this seal's census produced fresh `information_schema` facts). First-adapter target: `services/data_source/digicow_rds_read_only/` with LawfulBasisAdmit-before-first-byte + no-second-store + all-reads-receipted + idempotent-restart-from-cursor.
2. **S4b-DIGICOW-S3-AUDIO** — S3 `training-content-2026/audio/` prefix proven read-capable (this seal: 1,683 objects · ~14.20 GiB · single ingestion window today).

Next Commit-A on `programme/track-a` (opens next in the run per §6.8): S4a adapter package skeleton + RED invariants (invariants first, expected to be RED against the empty adapter). BASELINE_GUARD=1 PYTHONHASHSEED=0 sweep before any GREEN pull.

### Part F · Standing bounds (unchanged this seal)

no push · no fetch · no remote configured · terminal only · no testing_agent (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo discipline · ratchet monotonic-up floor **5858** · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · structural §3.8 guard on `services/request_context/context.py` sha-pin `ad0d9439…` · mirror-invariant guard on `/app/backend/vendored/extraction_akki/backend/`.

**R-91**: PARKED at horizon `2026-09-23T03:23:15Z` (~33 h out at 2026-09-21T~18:40Z). Per §6.8-C: applies at next boundary AFTER expiry — seal, then M1-to-date BUILD_JOURNAL pointing at audit tags. Not touched this seal.

### Part G · Reporting cadence

Per §6.8-D: reports written and the run continues in the same breath. This entry is written at seal boundary; the next unblocked slice opens on this seal per §6.8.1.

**End of SO-6.8-ADOPTION + FULL-ESTATE-CENSUS-20260921 wave card.**

<!-- SO-6.8-ADOPTION + CENSUS-20260921 · state Commit-A · 2026-09-21T~18:40Z END -->
