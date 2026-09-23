# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-02-23T03:15:00Z (**PHASE 4 (d-i) · CP-DECK-ENGINE-DR-R4-OPENING · 5-Commit-Seal FULLY LANDED · ratchet 6218 → 6224 · Slice 1 of CP-DECK-ENGINE 14-DR-R chunked series (OPENING) · DR-R4 DeckSpec_v0 shape-freeze OPENING · minimum-viable frozen contract shell landed at `contracts/deck_spec_v0.py` · deck_engine.md source UNRECOVERED (RD-16) · full field enumeration DEFERRED to Slice 2 · OWNER QUEUED (a) CENSUS-3-C + (b) Razuna/Newsvault binding-verify + (c) NEW RMS station→language axis directive verbatim folded to scheduler queue this-turn · CP-DECK-ENGINE Slice 2 opens NEXT**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i-vi) + P4-(d-i) FULLY SEALED · CP-SKILLS-LAYER series CLOSED · CP-DECK-ENGINE series OPENED at DR-R4 shape-freeze**.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** · **P4-(c-i-vi) CP-SKILLS-LAYER FULLY SEALED** · **P4-d-i CP-DECK-ENGINE-DR-R4-OPENING FULLY SEALED THIS-TURN**.
  - **P4-d-i seal chain (COMPLETE):** Code `b68cc02fc3e40e86e38e706bdfbf8ed0cbf6aa73` (programme/track-a · +6 measured) · /app companion `fb40d6f5bdfdb2cf37e2ec57d11cad17f4eb947b` (main) · State Commit-B `17ac82569a1e09e821bdc7f80a6344e986c35267` (master) · Commit-C fixup `f4605bd1f5ba18bfd3dcc38375615629660da8cc` (master) · companion-C `2c6354bbe12ffeff99570c240cab9c1a0fe12811` (main). Pre-Commit-A double-green stripped-sha256 `5998ae6832544cb698c861cf20c0b5699e6db8bfc42c6c6b61cfe4b9b2d360fa` IDENTICAL sweep_A (190.50s) + sweep_B (191.50s) both 6230/1/0/520.
  - **CP-DECK-ENGINE Slice 2** OPENS NEXT — full field enumeration post `deck_engine.md` verbatim restore.
  - Then CP-DECK-ENGINE Slice 3+ (DR-R1 rendering-service + DR-R2 determinism drift-detector + DR-R5 fail-closed validation) → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
  - **OWNER QUEUED CENSUS SCHEDULER TASKS (banked this-turn · fold-in only · no interrupt · ride the scheduler/job queue as their own §3.3 5-Commit-Seals when scheduler slots open):**
    - **Task 1 · CENSUS-3-C** (RMS MySQL/RDS text-column language-detection · CPU/SQL-only · no GPU) — schedule at next census-pass. Cover: razuna, news_vault, citizen_digital, weego, db_visitors, saa, kra_reports, viusasa (bounded), USSD dbs (bounded). Per-db language distribution over sampled text columns + narrative-field typology (Swahili/Sheng/French per prototype IN WHICH LANGUAGE card). Tenant-scoped to RMS. Language table lands in next census boundary report. **Blocked-on-DQ-17** for weego DB only.
    - **Task 2 · Razuna + Newsvault RMS-tenant binding-verify** — next census pass. Two receipts: (a) tenant-scope receipt against sealed `CENSUS_ADMISSION_SOURCE_MAP` (P4-c-v) confirming both are §3-map RMS-tenant sources — verify existing binding receipt on-disk under `phase0/census_autonomy_state/`; if absent, produce it as first-class additive artefact; (b) OBS audio sweep job manifest MUST include `news-vault` (19,815 audio objects) + `razuna.royalmedia` buckets when it runs. **Blocked-on-DQ-05** for §2(b) only.
    - **Task 3 · NEW · RMS STATION→LANGUAGE AXIS (owner verbatim 2026-02-23 mid-seal):** *"Audio - there are local language sample per station - each station represents local language - all research with title - eg inoro is kikuyu, ramogi is luo, etc. Update this."* Meaning: RMS is Royal Media Services (Kenya) — each station broadcasts in a specific local language, so STATION IDENTITY is authoritative language metadata for its audio. Sub-tasks: (a) **RESEARCH** full RMS station→language map with cited web sources (owner-directed *all research with title* — titles/links banked in receipt · known anchors owner-provided: Inooro = Kikuyu, Ramogi = Luo/Dholuo · complete the set; owner-suspected candidates to VERIFY, not trust: Citizen TV/Radio Citizen ≈ Swahili/English, Hot 96 ≈ English, Chamgei ≈ Kalenjin, Musyi ≈ Kamba, Muuga ≈ Kimeru, Mulembe ≈ Luhya, Egesa ≈ Ekegusii/Kisii, Bahari ≈ coastal Swahili, Wimwaro ≈ Kiembu, Sulwe/Vuuka ≈ Luhya-variants). (b) **CROSS-REFERENCE** against estate identifiers: NAS 16 off-air channels · OBS buckets `inoorotv`, `citizentv`, `citizen-vod`, `hot96backup`, `chamgei-backup`, `news-vault`, `rmsbroadcast`, `razuna.royalmedia`, `instore-radio-items`, `edailynew`, `skizaaudio`, `na7p4*` series when unblocked · MySQL station-fields. (c) **FOLD** into census language axis: per-asset `expected_language` from station attribution as first-class field alongside model-detected language. **HONESTY RULE** owner-verbatim: whisper-class models do NOT reliably distinguish Kikuyu/Luo/Kalenjin/Kamba etc.; where the model can't corroborate, attribution is `station-prior (cited), model-corroboration: unavailable` — NEVER present model output as confirming a language it can't detect. Where model says Swahili/English it corroborates those stations only. (d) Update registry/census read surfaces so the language card can show local-language split per station attribution (tenant-scoped to RMS). Bank research receipt + mapping table as state note with owner directive verbatim. **Sequencing:** additive census-model work · small slice or scheduler-job update at next natural boundary alongside CENSUS-3-C.
- **Ratchet floor: `6224`** (was 6218 pre-P4-d-i · +6 canonical measured) · baseline_failures_sha256 `66ae28aa7a7fbc2db40de200c26ffe0b9163239f6e58641bae6060eaacf6d61c`.

## 2 · STANDING (R-102 + R-103 + R-104 [CORRECTED] + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · PHASE 3 EXIT-EVIDENCED · PHASE 4 (a) Commission wizard LIVE · A18.3/A18.5 structural pins LANDED · A18.8 donor code with provenance manifest LANDED · **P4-c-v CENSUS-TENANT-ADMISSION-CORRECTION SEALED · owner §3 registration map declaratively pinned + retro-assignment records banked · DAP-14 orthogonality declared** · **P4-c-vi CP-SKILLS-LAYER-SERIES-CLOSE Slice 5 UI-visible walkthrough LIVE at `/dap/buildskill` reading sealed A18.2 persistence via public `read_all()` ONLY · ORIGIN-EMPTY renders honest-gap product-language block · CP-SKILLS-LAYER chunked series CLOSED**.
- R-103: single continuous run · no check-ins · additive-reversible.
- **R-104 CORRECTED (executed P4-c-v per owner queued directive 2026-02-23T00:30Z):** RMS + DIGICOW remain named-but-unseated ONLY for **DAP-14 controlled-request gating** (approvals, extractions, standing approvals — those stay held on DQ-19/20). CENSUS admission is a DIFFERENT control: all four canonical tenants ARE admitted for census jobs. Correction landed via additive `services/census_autonomy/tenant_admission_correction.py` carrier + 12 RED-first pins.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CLOSED + PHASE 4 (a-c-vi) SEALED-A.
- §6.8: plan is authority · report-and-continue.

## 3 · SIX STANDING BANS (UNCHANGED)

zero push/fetch · testing_agent BANNED · no refactor · no secret values · honest-gap never fake · no history rewrite.

## 4 · BOOT-ARTIFACT WARNING

CHUNK-1 is STALE bootstrap. Never re-run/re-clone/wipe. Probe list §5 authoritative.

## 5 · 8 DISK PROBES

```bash
ls -la /app/assessment_workspace/ && ls -la /app/assessment_workspace/STATE/
cat /app/assessment_workspace/STATE/RESUME.md 2>/dev/null || echo "not created"
head -40 /app/assessment_workspace/STATE/STANDING_ORDERS.md
git -C /app/assessment_workspace log --oneline -12
git -C /app/assessment_workspace/repos/Extraction-Akki log --oneline -8 && git -C /app/assessment_workspace/repos/Extraction-Akki branch
git -C /app log --oneline -10
python3 -c "import json; d=json.load(open('/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json')); print(d['counts_at_baseline'])"
tail -200 /app/assessment_workspace/STATE/DECISIONS.md && cat /app/assessment_workspace/STATE/NEXT.md
```

Expected: probe-7 `{'failed': 3, 'passed': 6218, 'skipped': 1, ...}` · adds **12 P4-c-vi CP-SKILLS-LAYER-SERIES-CLOSE invariants** most-recent (router module presence + shape / mount in spine+pod_shell+runtime / AST scan sealed-public-callable-only / endpoint returns real ORIGIN-EMPTY state / endpoint round-trip against appended record / frontend page files present at both twins byte-identical / hook files present at both twins byte-identical / App.js twin declares additive route byte-identical / page carries required data-testids / product-language discipline SO §4 banned-token scan / plain-product empty-state copy present / hook paired-equality with router route path Final).

## 6 · POINTERS

- 10 additive modules under `services/census_autonomy/` — PHASE 3 chain sealed.
- 3 census autonomy routers + `routers/wizard_operator.py` (sealed pre-P4-a) + **`routers/dap_buildskill.py` (P4-c-vi THIS-TURN · JWT-gated GET `/api/dap/buildskill/provisioning-records` reads sealed A18.2 persistence via public `read_all()` ONLY · never fabricates · never caches)**.
- **PHASE-4-a `WorkCommission.jsx` page** at `/os/work/commission` byte-identical twins.
- **NEW `contracts/skill_provisioning_record_v0.py`** (A18.1 Slice 1).
- **NEW `services/skill_provisioning_persistence.py`** (A18.2 Slice 2).
- **NEW `contracts/skill_call_governance_envelope_v0.py`** (A18.3 Slice 3) + parity snapshot + parity-map entry.
- **NEW `services/skill_call_scope_resolver.py`** (A18.5 Slice 3).
- **NEW `services/skill_donor_provenance.py`** (A18.8 Slice 4 · Final manifest · donor sha256 pinned + 356-line canon anchor).
- **NEW `services/census_autonomy/tenant_admission_correction.py`** (P4-c-v · owner correction verbatim + machine-readable anchor + declarative posture pin + owner §3 source map + retro-assignment records + DAP-14 orthogonality boundary annotation + 3 product-language callables).
- **NEW `pages/dap/BuildSkill.jsx` (~250 lines) + `hooks/useBuildSkillProvisioning.js` (~100 lines) byte-identical twins across `/app/frontend/src/**` ↔ `pod_shell/frontend/src/**`** (P4-c-vi THIS-TURN · React functional component · honest-gap product-language block when count=0 · record list when count>0 · `dap-buildskill-*` data-testid on every interactive/critical element · plain-product-language SO §4 · banned engineering tokens absent).
- Sealed donor code (byte-verbatim across Extraction-Akki + RMS-IQ-Core-2 + Akki-OS-V1) at:
  - `contracts/callable_skill_provisioning_v0.py` (101 · d61a446c)
  - `services/transform_forms/callable_skill_gate.py` (144 · 02d56745)
  - `services/transform_forms/callable_skill_persistence.py` (111 · 0590339f)
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `5bef7205ec76034ebd40e2f281d063b8907dbfd25ad898d862bcb24acf45b353` (P4-c-vi Commit-A · additive router mount block `from routers import dap_buildskill as dap_buildskill_router` + `app.include_router(dap_buildskill_router.router)` · byte-identical twins re-verified per BL #2).
- Test files: **`test_cp_skills_layer_series_close_phase_4_c_vi.py` (12 pins THIS-TURN)** + prior 6 A18-and-correction slices.
- Drill receipts: **`drill_receipts_cp_skills_layer_series_close/`** (RED_pre + GREEN_post + sweepA + sweepB).
- Ratchet-bump tool: **`tools/cp_skills_layer_series_close_bump_baseline.py`** (ensure_ascii=False per BL #11).

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · RMS approving authority · named-but-unseated · applies to DAP-14 controlled requests ONLY (census admission corrected orthogonally P4-c-v)**.
- **DQ-20** — **P1 · DIGICOW approving authority · named-but-unseated · applies to DAP-14 controlled requests ONLY (census admission corrected orthogonally P4-c-v)**.
- **DQ-GPU-SSH-KEYS** — SELF-RESOLVED 2026-09-22T19:00Z.
- **-2 collection-drift** — P1 forensic queued behind Order B audit.
- **Connect-wizard disambiguation** — RESOLVED at P4-b-i.
- **OWNER QUEUED CORRECTION (mid-Slice-4)** — CP-CENSUS-TENANT-ADMISSION-CORRECTION FULLY SEALED at P4-c-v.
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k.

## 8 · ELEVEN BANKED LESSONS (unchanged this-turn)

1. YAML plain-scalar hazard — embedded-colon patterns crash `yaml.safe_load`; use dashes.
2. Server.py mirror-edit rule — mirror pair is `/app/backend/server.py ↔ pod_shell/backend/server.py`.
3. Canon-9 §3 negative-scan literal-substring hazard — compose attr-name via string concatenation.
4. Producer-bridge additive discipline — AST-scan bans engine-internal imports.
5. Frontend banned-marker discipline — docstring rephrase at same-Commit-A.
6. ratchet_history entry `passed` field must equal NEW post-seal floor.
7. `json.dump(indent=2)` drift on `baseline_failures.json` — current format 2-space; preserve.
8. Drift-detector tests against another sealed contract must inspect the actual JSON schema before writing field-name assertions.
9. NEW file at `backend/contracts/` / `backend/services/` requires `tools/prod_vendor_sync.py` run same-Commit-A.
10. NEW Pydantic contract requires same-slice CONTRACT_TO_SNAPSHOT map additive entry alongside parity snapshot.
11. `json.dumps(indent=2)` writes on `baseline_failures.json` MUST pass `ensure_ascii=False` — historical on-disk unicode chars (em-dash, arrow, middle-dot) must NOT escape-convert. Ratchet-bump tools MUST specify `ensure_ascii=False`.

## 9 · SEAL SUMMARY (LAST-TURN P4-c-v + THIS-TURN P4-c-vi)

**P4-c-v CP-CENSUS-TENANT-ADMISSION-CORRECTION** (declarative pins + owner §3 map + retro-assignment records + DAP-14 orthogonality · ratchet 6194→6206):

| Commit | SHA | Branch |
|---|---|---|
| Code Commit-A | `570750563e62c22dae76a775b7264da2d2334c74` | programme/track-a |
| /app companion A | `c0d5e20537ec32b717949cea652af258c2b59e41` | main |
| State Commit-B | `57670cf55e3ede22618f3aaeff95f57d9e452baf` | master |
| State Commit-C fixup | `471b47ade7321bb686394d65af9468ad03ec73f4` | master |
| /app Commit-C companion | `63be431bca4eb3ae65ad556649062e5590418c48` | main |
| State mini-bank | `c848c91558dfba60ecf9b1f2bc650106b4ea0890` | master |
| /app boundary report | `af40ef93a579e92cb1819e0ed9c1af639711093a` | main |

**P4-c-vi CP-SKILLS-LAYER-SERIES-CLOSE** (Slice 5 · UI-visible tester walkthrough at `/dap/buildskill` · live reading of sealed A18.2 via public `read_all()` ONLY + honest-gap block when count=0 · ratchet 6206→6218 · THIS-TURN COMPLETE):

| Commit | SHA | Branch | Purpose |
|---|---|---|---|
| Code Commit-A | `419244cdb99cbbe6af8f85df7e39fa8519114289` | programme/track-a | NEW `backend/routers/dap_buildskill.py` (~110 lines · JWT-gated GET `/api/dap/buildskill/provisioning-records` · reads sealed A18.2 via public `read_all()` ONLY · AST-checkable no-private-import discipline) + NEW `pod_shell/frontend/src/pages/dap/BuildSkill.jsx` (~250 lines) + NEW `pod_shell/frontend/src/hooks/useBuildSkillProvisioning.js` (~100 lines) + additive router mount in server.py mirror-pair (byte-identical `/app/backend/server.py ↔ pod_shell/backend/server.py`) + additive App.js route in twin pair + 12 RED-first pins + baseline_failures.json bump |
| /app companion A | `27c7276d8` | main | frontend twins byte-identical + vendored twin sync +1 file · MANIFEST 1034→1035 · structural_sha256 db5ad2dc→7f9a3fbd · audit + notes ORCH_BOOT regen all 14 stanzas · gitlink advance 57075056→419244c |
| State Commit-B | `22738f20b40cfe112c85b837a0758782b1f29101` | master | banks Commit-A + companion + drill receipts + DECISIONS.md CP entry + NEXT.md marker + RESUME.md rewrite + ratchet-bump tool |
| State Commit-C fixup | `37bf8f4cd5c6ac1b22da283815104cfb71f67f29` | master | R-6 boundary regen · fresh P4-c-vi stanza advancing heads_last_sealed |
| /app Commit-C companion | `05d77e6cb458e488773fb65a0d0b003c23ca8f39` | main | audit ORCH_BOOT byte-identical mirror sync post-fixup |

Pre-Commit-A double-green byte-identical stripped-sha256 `2d124258c5e127e933b44e204b53b50f012e574a271906afe780705eae3063d6` IDENTICAL sweep_A (189.67s) + sweep_B (190.35s) both 6223 passed / 1 skipped / 0 failed / 520 warnings. 6223 = 6218 floor + 5 above-floor.

## 10 · AUTOPILOT NEXT

**All 5 seal commits LANDED THIS-TURN. CP-SKILLS-LAYER chunked series NOW CLOSED at Slice 5.**

**Tester walkthrough at `/dap/buildskill` (live-or-honest-gap per R-102 user-visible bar · concrete steps a human takes and what they see · owner boundary directive verbatim satisfied):**
1. Human navigates to preview URL `/dap/buildskill`.
2. Sees breadcrumb `DAP · BUILD A SKILL` and page title `Build a Skill`.
3. Page auto-fetches `/api/dap/buildskill/provisioning-records` via `useBuildSkillProvisioning` hook (uses `process.env.REACT_APP_BACKEND_URL` verbatim).
4. Unauthenticated: 401 branch preserves view + shows honest-gap "Not yet authenticated" block per `useCensusRunState.js` banked pattern.
5. Authenticated (`demo.master_admin@demo.rms.example.com` via `/api/auth/login`): endpoint returns `{records:[],count:0}` at ORIGIN-EMPTY.
6. Page renders the **NO SKILLS PROVISIONED YET** honest-gap block — plain-product-language body copy per SO §4 (banned engineering tokens absent per test pin 12 negative-scan).
7. Human clicks the `dap-buildskill-refresh-button` — hook refetches; view preserved on error, updated on success.
8. When A18.2 sealed persistence has records (via any future authorized producer surface), the page renders the record list keyed by `skill_id` with the 8 fields drawn verbatim from sealed `SkillProvisioningRecordV0`: `skill_id`, `donor_repo`, `donor_path`, `donor_commit`, `scope`, `governance_class`, `provisioned_at`, `provisioning_actor_id`.

**Next slice · CP-DECK-ENGINE (Canon 3 §13):**
- Deck-engine service pins + drift-detectors.

Then CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped → −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
