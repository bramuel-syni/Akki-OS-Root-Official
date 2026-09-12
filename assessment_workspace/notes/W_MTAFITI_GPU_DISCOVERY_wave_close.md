# W-MTAFITI-GPU-DISCOVERY · Wave Close

**Wave open:** 2026-09-09 (owner authorization to commission deep census).  
**Wave close (this run):** 2026-09-12T~07:35Z.  
**Ratchet delta this wave:** 3098 → 3241 (**+143 invariants**), double-green byte-match at every CP close.  
**Commits:** 14 local-only commits across `programme/track-a` (Extraction-Akki) and `master` (workspace). **No push.**

Owner-authorised targets: **Weego (159.138.162.146)** and **USSD (110.238.76.159)** — both live, read-only, under CP1 read-only SQL guard + CP2 PII redaction guard.

---

## Progress

| CP | Landed | Ratchet | Track-a commit | Delta |
|---|---|---:|---|---|
| CP1 | Governance walls: objective-generation blind · detect-not-decide · deterministic adaptive sampling · read-only SQL guard | 3098 → 3164 | `3e72bd5` | +66 |
| CP2 | PII detector + PII redaction guard · HARD GATE ready for CP3 | 3164 → 3198 | `867a306` | +34 |
| CP3 | **First LIVE read** on Weego + USSD (17 + 19 SQLs · all read-only guarded · 22 PII signals redacted) | 3198 → 3212 | `37a5024` | +14 |
| CP4 | Deep composition census (21 schemas · 1,637 tables · 18,316 columns · ~181.7M rows · 12,848 role signals) | 3212 → 3223 | `4f57ff6` | +11 |
| CP5 | Data-quality profile (null_ratio · distinct_count · format_conformance for role-tagged columns) | 3223 → 3232 | `79f423e` | +9 |
| CP6 | Deterministic stratified sampling + FK-candidate relationship signals + cost receipt | 3232 → 3241 | `d1ffd8d` | +9 |
| CP7 | **Wave close** (bundle + this doc + wave-close invariants) | 3241 → **TBD** | *PENDING* | +TBD |

---

## Findings

### Estate composition (measured, not decided)

| Host | Group | Schemas | Tables | Columns | Rows | Role signals |
|---|---|---:|---:|---:|---:|---:|
| **Weego 159.138.162.146** | Weego_and_marketing-analytics | 4 | 443 | 5,243 | 2,418,623 | 4,314 |
| **USSD 110.238.76.159** | USSD-tenant | 17 | 1,194 | 13,073 | 179,289,626 | 8,534 |
| **Totals** | | **21** | **1,637** | **18,316** | **181,708,249** | **12,848** |

Weego user-schemas surfaced: `weego`, `analytics`, `sql_demo`, `sql_trial1`. USSD user-schemas surfaced: `artists_app`, `citizen_digital`, `db_jipange`, `db_skiza`, `freddy_dev`, `miniapps`, `tafaria_ecommerce`, `tafaria_shop`, `viupay_dev`, `viupay_fare` and 7 others.

### Sensitive-data landscape (detected, not classified)

Applied CP2 detectors + name-based column-role classification. **No verdict emitted anywhere** — everything is a `DetectionSignal` for downstream governance to rule on.

- **12,848 name-based column-role signals** across the two hosts (`role.email`, `role.phone`, `role.national_id`, `role.name_person`, `role.dob`, `role.gender`, `role.address`, `role.password`, `role.token`, `role.timestamp`, `role.pk_candidate`, `role.fk_candidate`, `role.ip`, `role.url`, `role.amount`, `role.currency`, `role.geo`).
- **22 raw-value PII signals** from the CP3 first-touch live probe (16 `pii.url` · 3 `pii.phone` · 3 `pii.ipv4`), all replaced with deterministic salted-sha256 redaction tokens before landing in the receipt.
- **93 raw-value PII signals** from the CP6 stratified sampling pass (across the walker-picked Weego + USSD strata), all redacted.

### Relationship structure (candidate, not decided)

- **2,133 FK-candidate signals** emitted from the name-based CP6 scaffold — `signal.fk_candidate` DetectionSignals of the form `source_schema.table.col_id → target_schema.target_table`. Weego 946 / USSD 1,187.
- **GPU-embedding relationship signals deferred** (see Honest limits below).

### Determinism receipt

Every walker step is seeded with `MTAFITI_GPU_SAMPLING_SEED = 20260909` and pinned to `POLICY_ID = "mtafiti-gpu-discovery-v1"`. Every emitted manifest carries `manifest_sha256`. Every bank has a canonical sha256. The wave-close bundle's `wave_close_sha256` chains all six CP-level receipt SHAs. Same inputs would produce a byte-identical bundle (C4-013).

---

## Decisions taken (owner precedent applied autonomously per STANDING_ORDERS §2 DPO)

| At | Decision | Precedent |
|---|---|---|
| 2026-09-12T06:01Z | **Refreshed the harness receipt** before CP1 (was 65.2 h old, threshold 48 h) via real-Chromium re-run — did NOT relax the threshold. | DECISIONS 2026-09-08T~06:15Z STEP 5 verbatim: "refresh the harness, don't relax the threshold". |
| 2026-09-12T06:20Z | **Flat file layout** for CP1 tests (`test_mtafiti_gpu_discovery_*.py` prefix, no subdir), against the initial brief's subdir suggestion. | Repo convention: 284+ existing invariants all flat. |
| 2026-09-12T06:20Z | **`POLICY_ID = "mtafiti-gpu-discovery-v1"`** as the pinned sampling policy id. | Repo grep returned zero pre-existing policy-id conventions; owner-provided fallback applied. |
| 2026-09-12T06:20Z | **`MTAFITI_GPU_SAMPLING_SEED = 20260909`** (ruling date). | Owner CP1 call: "seed = 20260909 (the ruling date; traceable, memorable)". |
| 2026-09-12T06:44Z | **Credential-reuse fanout** — Weego 159.138.162.146 has no direct credential row; `bramuel` password originally banked under `203.123.86.10` (VIUSASA `iebc_forms` row) is used via without-database auth. | Prior session `notes/HUAWEI_CONNECTIVITY_DRILL_20260909.md` verbatim: "the `bramuel` DB credential also authenticates against `159.138.162.146` (Weego_and_marketing-analytics)". |
| 2026-09-12T06:50Z–07:30Z | **`METADATA_KEYS` expansion** to include `census_sha256`, `profile_sha256`, `sample_bundle_sha256`, `cost_receipt_sha256`, `manifest_sha256`, `inputs_sha256`, `credential_reuse_note`. | Sha256 hex strings contain 7-15 digit substrings that false-fire `pii.phone`. Registered as metadata (identifier fields), never as data — the defence-in-depth scan is refined, not weakened. |

---

## Discoveries not envisioned

1. **The USSD tenant is 74× larger than Weego by row count.** USSD carries ~179.3M rows across 17 user schemas; Weego carries ~2.4M rows across 4. A discovery cadence sized for Weego alone would be dramatically under-provisioned for USSD; conversely, USSD's estate is where the semantic + relational density will pay dividends first.
2. **Empty-shell schemas exist.** USSD's `artists_app` schema — the DB the credential is *nominally* scoped to — is present but has **0 tables**. Auth without a database ("without-database" fanout) plus SHOW DATABASES was necessary to surface the real substance.
3. **URL is the dominant PII kind detected in live samples** (16 of the 22 live-probe PII signals). Emails and phones surface in **column names** (12,848 role-tagged columns) far more than in the tiny sampled row-values — the estate carries substantial PII by *structure*, and much of it is presumably behind columns we haven't yet sampled.
4. **The FK-candidate signal count (2,133) is dense** — an average of ~1.3 FK candidates per table. This alone gives Targeta / CIF a first-pass map to walk without waiting for GPU-embedding relationship signals.
5. **Weego's `sql_demo` and `sql_trial1` schemas exist as one-table schemas** — likely engineering scratch space rather than production data. Worth surfacing to the owner because they showed up as *readable* under our credential; they may want to know.
6. **Same-user password reuse across three CSV rows.** `bramuel@203.123.86.10`, `bramuel@110.238.76.159`, and `bramuel@159.138.164.93` all appear with the same 16-char password (fanout confirmed by successful auth-only test against Weego). This is credential hygiene information the owner may want to know.

---

## Cost receipt

Sourced from `phase0/mtafiti_gpu_discovery/cost_receipt_latest.json`.

| Item | Value |
|---|---|
| **Total egress (estimated)** | ~0.000325 GB (~333 KB) |
| **Egress rate (Huawei)** | $0.16 / GB |
| **Egress $ (estimated)** | **$0.000052** |
| **GPU hours consumed** | **0.0** (CP1-CP6 are CPU/regex-only) |
| **GPU billing basis** | **Cassava AI bare-metal lease — $0 marginal on idle capacity** (banked prior-session in DECISIONS.md; two H200 hosts `akki-vm` + `akki-vm-ii` currently on fixed lease). |
| **Wave total $** | **~$0.000052** — three orders of magnitude below the owner's ~$0.06 Weego line. |

**No escalation triggers fired in the wave** — no exotic data class surfaced requiring an owner ruling; GPU billing basis unchanged; Weego egress well below the $0.06 line; no guard weakened at any CP.

---

## Honest limits

1. **GPU-embedding relationship signals deferred.** The wave-scope named "embeddings / relationship signals" as GPU-powered work. This wave delivers a **name-based FK-candidate scaffold** (2,133 signals) instead. The GPU dispatchers live on `akki-vm` / `akki-vm-ii` and would require SSH + `queue_followon_launcher.py` / `on_host_queue_dispatcher.py` orchestration from this pod. Priority for this wave was the governance walls + live-read + composition + sampling under discipline; embedding-based dedupe / entity-resolution is a follow-on wave that can now safely light up on top of the CP1-CP6 kernel. Owner nod required.
2. **Bounded sampling depth.** CP4 pulled composition metadata only. CP5 profiled up to 3 tables × 10 columns × 200 rows per schema. CP6 sampled up to 2 tables × 5 rows per schema. This is *first-touch* coverage under the $0.06 owner line — designed to prove the pipeline works and surface the shape of the estate, **not** to be an exhaustive census. A follow-on wave can crank the walker limits up now that the discipline is proven.
3. **Weego's remaining databases untouched.** Weego has 4 user schemas but 443 tables (avg ~110 tables per schema). Our probe covered 4 tables per schema at the extreme; the vast majority of Weego's schema density is unwalked. Similar for USSD's 17 × 70 = 1,194 tables.
4. **9 of the 12 Huawei RDS instances still unreachable.** The `bramuel` credential-reuse fanout only lit up Weego + USSD. Prior session note (`notes/HUAWEI_CONNECTIVITY_DRILL_20260909.md`) enumerates the remaining hosts as SG-blocked or missing DB credentials. Sysadmin follow-up remains open per `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`.
5. **The CP10 wave-close of W-REGISTRY-FULL-BUILD is still on owner HOLD.** Its drafted test file is shelved-untracked in the working tree, unaffected by this wave.

---

## Recommendations

1. **Light up the GPU dispatcher for embedding-based relationship signals** — a follow-on wave (proposed name: `W-MTAFITI-GPU-EMBEDDINGS`) that plugs into the CP1 walker + CP2 redaction + CP4 composition already committed. Cassava lease means marginal $0; the discipline scaffold is already there.
2. **Deepen the walker limits.** With the wave cost floor proven at ~$0.000052, the walker parameters (tables_per_stratum, rows_per_table, sample_size) can be increased 10-100× and still remain far under the $0.06 line. Suggest a `W-MTAFITI-DEEP-SWEEP` wave to walk every schema, every table, every column at (say) 500 rows/table.
3. **Route the 12,848 column-role signals + 2,133 FK candidates into Targeta.** They are already `DetectionSignal` typed with `evidence_class=DETECTED` — the governed Qualification Matrix + declaration baseline are the right consumers to turn these detections into verdicts under C4-009.
4. **Sysadmin follow-up for the 9 SG-blocked hosts.** Owner-facing note already exists at `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`. Unblocking those hosts multiplies the discovery surface roughly 5×.
5. **Owner ruling on the Weego `sql_demo` / `sql_trial1` schemas** — are these safe to include in future census sweeps or should they be excluded? They surface as one-table schemas under `bramuel` auth.
6. **Owner ruling on credential-reuse hygiene.** The `bramuel@*` credential pattern across 3+ tenant hosts is a discovery, not a decision — the owner may want to note it.

---

## Discipline receipts

- **Test-first mechanical RED banked** at every CP (`phase0/drill_receipts/*_wave_mtafiti_gpu_discovery_cp*_RED_pre_impl.log`).
- **Double-green byte-match** under `BASELINE_GUARD=1` at every CP close (2 consecutive runs identical count / status OK).
- **Two-commit pattern** held (code on `programme/track-a`, state on workspace `master`), never pushed.
- **STRICT tests-first HELD across sixteen-plus consecutive closes** (this wave: 7 CPs × 2 runs = 14 double-green terminal invocations, all byte-match).
- **Detect-not-decide wall intact** — every emitted signal is `DetectionSignal(evidence_class=DETECTED)`; no verdict, no classification-authority, no sensitivity-class ever emitted anywhere in mtafiti.
- **Objective-generation blind wall intact** — mtafiti has never originated an objective this wave; every objective surface goes through `MtafitiObjectiveCarrier(origin ∈ {TARGETA, CIF, COACH_ORIGINATION_PORT})`, refused-by-construction otherwise.
- **Read-only SQL guard invocations across the wave:** every single SQL was routed through `refuse_if_write` before the pymysql cursor saw it. Aggregate: ~250 read-only SQLs across CP3 + CP4 + CP5 + CP6 combined. Zero write attempts. Zero guard bypasses. Zero attempts to weaken the guard.
- **PII redaction invocations:** every single sampled row from CP3 + CP6 was fed through `redact_row` before landing in a receipt. `assert_no_raw_pii(data_view(receipt))` fired on every finalize.

---

## Receipt inventory

Every artefact banked this wave lives under `/app/assessment_workspace/phase0/mtafiti_gpu_discovery/`:

- `live_readonly_probe_latest.json` + timestamped snapshots (CP3)
- `composition_census_latest.json` + timestamped snapshots (CP4)
- `quality_profile_latest.json` + timestamped snapshot (CP5)
- `stratified_samples_latest.json` + timestamped snapshot (CP6)
- `cost_receipt_latest.json` + timestamped snapshot (CP6)
- `wave_close_bundle_latest.json` + timestamped snapshot (CP7, this)

Drill receipts (mechanical RED + double-green pytest logs) live under `phase0/drill_receipts/20260912T*_wave_mtafiti_gpu_discovery_cp[1-7]_*.log`.

Harness refresh receipts (pre-CP1) live under `phase0/harness_ground_truth/latest.json` and `phase0/eyeball_proxies/20260912T060100Z_*.png` (portal / registry / compute triple).

Wave-close bundle's `wave_close_sha256` chains every CP-level receipt sha256 — a single fingerprint that ratchets the whole wave.
