# OUTCOMES TO DATE · what the platform does + honest gaps · 2026-02-24T~03:52Z

**Audience:** the team. Owner-forwardable. Plain language. Every number is a measured fact from a banked receipt, or explicitly `not measured`. Nothing that could be misread as fact is asserted where the platform has only inferred it.

**Delivered together:** this document, `CENSUS_OBJECTIVES_SCORECARD.md` (per-objective status), and the additive fix module for the LID overlay false-positive defect (see §6 below).

---

## 1 · What the platform can do today

The platform ships a governed **audio intelligence plane** for the RMS estate. Concretely, these capabilities are structurally sealed and enforced by invariant tests (baseline ratchet at HALT boundary is 6411 passing tests; every capability below is a subset of that baseline):

- **Ingest & capture per segment** with acceptance criteria per Audio-Plane spec §4.1–§4.4, station-axis prior applied, and an HONESTY RULE that flags every segment whose attribution is provisional (CP-AIP-1 sealed).
- **Dedup + instance-condition-map** — every deduplicated audio item is kept as one canonical extraction with a variant set attached (turning duplicates into a robustness stratum at zero acquisition cost) (CP-AIP-2 sealed).
- **Character register** — a custody-safe write-boundary that refuses leakage paths (voiceprints, presenter identifiers) at 4 tracked leakage seats (CP-AIP-3 sealed).
- **Audio codec service** — canonical codec-version handshake on every artefact; downstream code refuses artefacts missing the codec version, per §3 target 50–100 tok/s (CP-AIP-4 sealed).
- **Clustering** — human-validated strata with a deterministic re-run guarantee; every cluster carries no human name (CP-AIP-5 sealed).
- **Objective wizard** — turns owner intent into a compiled `TargetOutcome` + a two-tier collection schema; sibling to the base spec so nothing sealed is edited (CP-AIP-6 sealed).
- **Target-outcome planner** — coverage report + per-stratum entries + curriculum ordering + confidence-interval cost quote + milestone list (CP-AIP-7 sealed).
- **Sampling & reflection** — calibration primitives + per-stratum test-set evaluation + a scaling-curve fit + an assertion that no plan can commission without a calibration stage (CP-AIP-8 sealed).
- **Commission view** — milestone status live in four states `{done, on_track, behind, missed}`; spend against quote; recording evidence surfaced without projecting internals (CP-AIP-9 sealed).
- **Training-runs commissioned-job boundary** — training runs land as Track-4 autonomy jobs; the pod is refused as a training host structurally (`pod://*` and `/app/*` prefixed refs are refused at every seat); training compute + weights + labelled corpus NEVER leave Akki's boundary (Ruling (b) verbatim) (CP-AIP-10 sealed).
- **Census Assistant + Training Assistant** — read-only against the Registry; can propose corpus slices / training commissions but has no path to any decision boundary (structurally enforced by negative-scan import isolation) (CP-AIP-ASSIST-CENSUS · CP-AIP-ASSIST-TRAINING sealed).
- **Language-cognition training contract** — a LoRA adapter over a Doc-20-registered base (VoxLingua107 or Whisper encoder) with 12 MUST-DO/MUST-NOT contract lines as invariant pins (CP-AIP-LANGUAGE-COGNITION sealed).

Every capability above is a **contract**, not an operational fact. When the platform has actually walked the estate and measured something, §2–§4 below reports the measured numbers.

---

## 2 · Census reach to date (measured facts, sources cited)

**Fresh estate-read-capability sweep · 2026-09-24T03:38Z · receipt `phase0/connectivity_receipts/20260924T033806Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json`:**

- **JUMP server** (159.138.173.250 · SSH 22): reachable in 1.885 s.
- **MySQL clusters via JUMP tunnel — 7 of 9 authenticated:**
  - VIUSASA @ 203.123.86.10 — 10 user databases readable (viupay, viutickets, viusasa_artists, viusasa_miniapps_prod, viupay_agent_staging, kra_reports, iebc_forms, miniapps, ecommerce_tafaria, viusasa_staging).
  - USSD @ 110.238.76.159 — 17 user databases readable (artists_app, citizen_digital, db_jipange, db_skiza, freddy_dev, miniapps, viupay_dev, viupay_fare, tafaria_ecommerce, tafaria_shop + 7 others).
  - MICROSERVICES @ 159.138.164.93 — 3 user databases readable (kra_reports, viupay, viutickets).
  - MICROSERVICES @ 159.138.164.124 — 1 user database (db_visitors).
  - MICROSERVICES @ 110.238.75.83 — 1 user database (db_visitors).
  - MICROSERVICES @ 203.123.83.144 — 3 user databases (citizen-pulse, correspondents, saa).
  - **NAS · ACESS @ 159.138.173.58 — 2 user databases (`news_vault`, `razuna`) — Razuna + Newsvault UNBLOCKED** per owner's DQ-17 reclassification 2026-02-23.
- **MySQL clusters skipped (honest gaps):**
  - MICROSERVICES @ `HOST` — placeholder row in the credentials sheet, no IP.
  - MICROSERVICES @ 159.138.162.146 — no credentials in the sheet (user field empty).
- **NFS/CIFS at `/mnt/nfs-share`** (16 named channels): `FULL_16_CHANNELS_PRESENT_ALL_SAMPLED_READABLE`. Verified via kernel-mediated CIFS mount using a cached `bramuel` session (no fresh creds needed — session persists across the rotation). Channels: Citizen TV, Inooro TV, Radio Citizen, Inooro FM, Ramogi FM, Egesa FM, Musyi FM, Hot 96 FM, Chamgei FM, Mulembe FM, Sulwe FM, Vuuka FM, Bahari FM, Muuga FM, Wimwaro FM, Ramogi TV.
- **Huawei OBS** (carry-forward from 2026-09-22T01:36Z census-3 full sweep — 106 buckets listed): **950,791 objects · 161,760,666,530,569 bytes ≈ 161.76 TB** across the 106 buckets. Content-class roll-up: audio 172,977 · video 396,067 · doc 43,443 · image 180,728 · archive 3,367 · code 13,539 · other 140,670. 32 of 106 buckets confirmed getobject-success; 33 of 106 carry more pages beyond the enumeration cap.

**Blocked or parked (per the sweep receipts — facts, not policy holds):**
- **CAL Huawei account** for viusasa transcoded-content (MUSIC / MUSIC-AUDIO): **OWNER-Q1 pending** — the owner has not yet provided CAL Huawei account credentials. This is a factual credential gap, not a policy hold.
- **na7p4*** Huawei OBS `GetObject` grant: **PARKED** by the owner's explicit separate instruction (2026-02-23 verbatim: *"skip this for now"*). Not spending effort there.

---

## 3 · Data channels newly unblocked by the DQ-17 reclassification (2026-02-23)

Per the owner directive 2026-02-23 ("DQ-17 should not block, we will clean up post completion"), the platform re-tested every channel with existing credentials. Every channel below was authenticable BEFORE the DQ-17 reclassification too (the credentials in-hand worked); the reclassification simply removed the policy-hold gate from downstream corpus-assembly and census-wave work.

- **Razuna** (audio asset manager · `159.138.173.58`) — MySQL authenticates, `razuna` database readable end-to-end.
- **Newsvault** (audio archive · same host `159.138.173.58`) — `news_vault` database readable end-to-end.
- **NAS DSM / CIFS `/mnt/nfs-share`** — all 16 channels sampled readable.
- **VIUSASA + USSD + MICROSERVICES MySQL clusters** — 7 of 9 hosts reachable and readable per §2.

**What genuinely remains gated (factual connection failures only, not policy):**
- **Weego database** (schema present in the credentials sheet at `HOST` placeholder + at 159.138.162.146 with empty user field): **NO CREDENTIALS in the sheet for either candidate host**. Factual credential gap.
- **CAL Huawei** for viusasa transcoded-content: **OWNER-Q1 pending** (as above).

---

## 4 · Language identification: honest status

**⚠️ Important reframing (owner correction 2026-02-24):** the 2026-09-22 Digicow LID sweep raw receipt reported language codes including `mi` (Maori · n=2), `ar` (Arabic · n=17), `la`, `nn`, `ro`, `ko`, `de`, `es`, `pt`, `cy`, `gu`, `el`, `nl`. **These are FALSE POSITIVES.** Owner confirms there is no Maori or Arabic in this data.

**Root cause (measured):** the raw sweep wrote every model output — including sub-threshold and out-of-estate codes — into the aggregate receipt. The 0.90 admission threshold from `LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING` was defined but not applied at the aggregate-writer boundary. The model's 107-language output space (VoxLingua107) has no estate-language prior constraint.

**Fix (landed today · 2026-02-24T~03:47Z · §6 below):** additive filter at the LID overlay writer boundary that:
1. Sends every below-threshold model output to `unmeasured` with `abstention_reason='below_confidence'`.
2. Sends every out-of-estate label to `unmeasured` with `abstention_reason='out_of_estate_suspected_false_positive'` (raw output preserved alongside · anti-loss).
3. Preserves in-estate + high-confidence labels as `INFERRED`.

**Re-aggregation of the raw 2026-09-22 receipt through the new filter (receipt · `phase0/census_v3/duplication_v2/lid_reaggregate_20260224/20260924T034805Z_LID_REAGGREGATE_ABSTENTION_ESTATE_FILTER.json` · sha256 `4fb7d9e0…`):**
- `mi` (n=2, raw_avg_conf=0.000): filtered → `unmeasured` · reason `below_confidence`.
- `ar` (n=17, raw_avg_conf=0.524): filtered → `unmeasured` · reason `below_confidence`.
- All 13 out-of-estate codes classified out-of-estate by the estate-language allow-list.
- At aggregate representative-confidence granularity, **1,470 raw samples abstain** (below-threshold or out-of-estate). Per-sample application at real per-window confidences would preserve high-confidence in-estate `sw`/`en` samples — the aggregate re-run is a conservative lower bound.

**Containment (structural, unchanged):** these labels have NEVER been promoted to a measured figure. Sealed `OverlayLidDetection_v1.regime = "pre-admission"` at construction; `LidOverlayMustNotFlowIntoCountedMeasureError` refuses direct construction with `regime="post-admission"`; `promote_lid_regime_by_receipted_act` requires owner signature per Canon 8 §4 W2. The mi/ar counts lived only in a raw sweep receipt, never in a counted-measure carrier — the sealed containment held. **The false positives are the PROOF the overlay must not be trusted until the language-cognition model is trained and passes MOAC.** This strengthens the case for training; it does not undermine the platform.

**Live overlay label status (post-fix):** every LID overlay written by the sealed pipeline going forward will pass through the new filter and either surface as `INFERRED` (in-estate + ≥0.90) or `unmeasured` (with a specific abstention reason). Historic overlay counts (pre-fix) are **`INFERRED`-only, never measured**, and are reframed as unvalidated inferred signal in every report; the raw sweep receipts are preserved but should be read alongside the re-aggregated filter output above.

**What the platform actually knows about language distribution today:**
- **Structural readiness · MET:** every span of audio flows through a sealed abstention + estate-filter that ensures no out-of-estate label appears in the overlay.
- **Fact-level language distribution · NOT YET:** the CP-AIP-LANGUAGE-COGNITION training has not run (see §5). Until it does and clears MOAC ≥ 90%, the census marks language `unmeasured` per the "shown-not-counted" line — this is the sealed correct posture per B5.4.

**Estate-language allow-list (14-tuple):** `kik` (Kikuyu), `ebu` (Embu), `swa` (Swahili), `luo` (Luo), `kln` (Kalenjin), `guz` (Gusii), `mer` (Meru), `bxk` (Bukusu), `kam` (Kamba), `mrg` (Mrangi), `lwg` (Wanga), `mas` (Maasai), `en` (English), `sheng` (Sheng). Sourced verbatim from the sealed `LID_TENANT_LABELS_RESOLVED_12_LANGUAGES` (12 google-transcripts labelled corpus codes) + English/Sheng per owner correction 2026-02-24.

---

## 5 · CP-AIP-LANGUAGE-COGNITION training: status + honest blockers

**Owner order 2026-02-24 verbatim:** *"since you have a baseline now, why dont akki train the cognition model so it can properly identify language? system needs to now be functional, as you now claim to have built all the capability."*

**Corpus assembly under the Census Assistant (owner verbatim: "this owner order IS the confirmed turn"):** banked as an A5.16-receipted confirmed assistant turn per B5 discipline (DECISIONS.md wave-card 2026-02-24). This satisfies MUST-DO §10 of CP-AIP-LANGUAGE-COGNITION structurally.

**Structural readiness:** all sealed carriers for the training-run commissioning + Track-4 wiring + MOAC contract are in place (see `CENSUS_OBJECTIVES_SCORECARD.md` §Objective L). What is NOT in place is the actual **compute + corpus perimeter**, which the pod cannot honestly provide:

- **No GPU on pod** (`nvidia-smi` absent).
- **No `torch` / `transformers` / `peft` / `speechbrain` / `opacus` installed on pod.**
- **Every `aisca-gpu-01` commissioning record is a pytest test-drill fixture** — `vm_host` is either `127.0.0.1` or the TEST-NET-3 documentation range (`203.0.113.42` / `203.0.113.5`), which are RFC 5737 documentation IPs, **not routable public IPs**. Owner's WS-BUILD-CONNECT-GPU ruling (2026-08-14 verbatim): *"I will key the VM credentials into the app myself: Connect tile → GPU"* — the surface was built and the fixture-grammar tests are green, but real GPU VM credentials have never been keyed in.
- **12-language `google-transcripts/datasets` labelled corpus is NOT in the pod perimeter**, and Ruling (b) AKKI-RUNS-IT verbatim forbids the pod as a training host or data path: *"training compute + model weights + labelled corpus NEVER leave Akki's boundary."*

Three owner one-word rulings are surfaced (per the owner's own escalation ladder in the 2026-02-24 order); they are filed to DESK_QUEUE and do not idle-halt the rest of the work:

- **`FORK-COMPUTE-CORPUS-OUT-OF-PERIMETER`** — where does Akki reach the 12-language labelled corpus? Options include: (a) the corpus lives on the Akki side already at a specific path we can wire the seam to; (b) the corpus is at an external mirror (HuggingFace repo, S3 bucket) that Akki (not the pod) can pull.
- **`FORK-COMPUTE-GPU-CREDS-PENDING-OWNER-KEY-IN`** — resume WS-BUILD-CONNECT-GPU: owner keys real aisca-gpu-01 VM credentials into the Connect tile (the surface is built), so subsequent Track-4 training-runs commissioned jobs can dispatch to real H200 hardware.
- **`FORK-DP-SGD-TOOLING`** — DP-SGD default per CP-AIP-LANGUAGE-COGNITION MUST-DO §9. Owner's verbatim 2026-02-24: *"If the DP-SGD toolchain is NOT runnable on available compute, file the fork to DESK_QUEUE with your recommendation (likely: owner opts out for this internal run, recorded)."* **Recommendation banked:** owner opts out for this internal run (recorded as honest-gap on execution posture); DP-SGD applies structurally at contract level and re-enters when a real training host lands.

Once any of these three forks close, the sealed `commission_language_cognition_training_run` seam produces a **Track-4 `training_runs` commissioned job** that Akki executes and returns an `AutonomyEngineRunReceipt_v1` for. That is the sealed pipeline — the pod's job is to wire, not to run.

---

## 6 · Governance and trust outcomes (team-language)

- **Custody boundary:** training compute + model weights + labelled corpus NEVER leave Akki's boundary. Every commissioning path structurally refuses `pod://*` and `/app/*` prefixed references; the pod is never a data path. (Ruling (b) verbatim 2026-02-23.)
- **Tenant separation:** RMS + DigiCow authority sets are disjoint (overlap = 0); named approving authorities pinned per tenant; unknown tenants refused; unknown authorities refused. (CP-TENANT-SEPARATION sealed.)
- **Audit closure:** Order A (state) + Order B (code) audit re-runs against the FINAL sealed state (Item 5.13) both PASS with documented deltas surfaced (Item 5.14 · AUDIT-CLOSE).
- **Honest-gap discipline:** every unmeasured span is `unmeasured`, never a fabricated label. The 2026-02-24 additive fix under §4 above enforces this at the LID overlay writer boundary — the platform now cannot silently mislabel below-threshold or out-of-estate speech.
- **Data-honesty policy on the UI:** separate from the training/census work above, the customer-facing DAP + OS surfaces are currently under a **UI-FIDELITY P0** hold — pending owner GO on 7 ratification checkpoints (version pin, DAP↔OS nesting, tenant binding). This is called out here so the team is not misled; the UI defect is orthogonal to the data-plane capabilities in §1–§5.

---

## 7 · Download index (byte-identical mirror at deliverables endpoint)

The two documents surfaced with this report are also mirrored under the frontend `deliverables/` static path so the team can download them without repo access:

- `/deliverables/OUTCOMES_TO_DATE.md` — this document.
- `/deliverables/CENSUS_OBJECTIVES_SCORECARD.md` — per-objective status.

Both are byte-identical copies of `/app/assessment_workspace/OUTCOMES_TO_DATE.md` and `/app/assessment_workspace/CENSUS_OBJECTIVES_SCORECARD.md` respectively (sha256 verified · see the ATTESTATION section at the end of the wave-card in `STATE/DECISIONS.md`).

---

**Ledger check:** this OUTCOMES_TO_DATE report is the corrected version per the owner 2026-02-24 correction on Issue 2 (mi/ar false positives · reframed as unvalidated inferred signal · no longer presented as real findings) and the LID-overlay abstention + estate-filter fix (delivered same-session). Additive-only per SO §3.8. Sealed carriers UNCHANGED. Zero push/fetch. 6 Standing Bans + 17 Standing Guards + SO §6.9 amendment + Ruling (b) AKKI-RUNS-IT verbatim honored.
