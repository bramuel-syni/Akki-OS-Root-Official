# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-02-23T00:54:00Z (**PHASE 4 (c-v) · CP-CENSUS-TENANT-ADMISSION-CORRECTION · 5-Commit-Seal FULLY LANDED · ratchet 6194 → 6206 · owner queued correction executed · census admission ≠ DAP-14 controlled-request seating boundary annotated · retro-assignment records banked additively · Slice 5 CP-SKILLS-LAYER-SERIES-CLOSE opens NEXT**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i) + P4-(c-ii) + P4-(c-iii) + P4-(c-iv) + P4-(c-v) SEALED** · owner queued correction executed additively.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** · **P4-c-i A18.1 shape-freeze** · **P4-c-ii A18-2 write-once slice-binding** · **P4-c-iii A18.3 + A18.5 governance-and-scope pins** · **P4-c-iv A18.8 donor-code provenance** · **P4-c-v CP-CENSUS-TENANT-ADMISSION-CORRECTION FULLY SEALED THIS-TURN**.
  - **P4-c-v seal chain (COMPLETE):** Code `570750563e62c22dae76a775b7264da2d2334c74` (programme/track-a · +12 measured) · /app companion `c0d5e20537ec32b717949cea652af258c2b59e41` (main) · State Commit-B `57670cf55e3ede22618f3aaeff95f57d9e452baf` (master) · Commit-C fixup `471b47ade7321bb686394d65af9468ad03ec73f4` (master) · companion-C `63be431bca4eb3ae65ad556649062e5590418c48` (main). Pre-Commit-A double-green stripped-sha256 `8d17fd23e6050e7e53f096bcded421aa432614d419ce88b7dd5f0d6c6887f92d` IDENTICAL sweep_A/B both 6211/1/0/520.
  - **CP-SKILLS-LAYER-SERIES-CLOSE** (Slice 5 of 5) OPENS NEXT — UI-visible tester walkthrough at `/dap/buildskill` (live-or-honest-gap per owner pacing note).
  - Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- **Ratchet floor: `6206`** (was 6194 pre-P4-c-v · +12 canonical measured) · baseline_failures_sha256 `5bc2c43755c5e167b938b2c6f54280d43c344b33f03e57792b6de198ef27a55f`.

## 2 · STANDING (R-102 + R-103 + R-104 [CORRECTED] + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · PHASE 3 EXIT-EVIDENCED · PHASE 4 (a) Commission wizard LIVE · A18.3/A18.5 structural pins LANDED · A18.8 donor code with provenance manifest LANDED · **P4-c-v CENSUS-TENANT-ADMISSION-CORRECTION LANDED · owner §3 registration map declaratively pinned + retro-assignment records banked · DAP-14 orthogonality declared** · Slice 5 UI-visible walkthrough queued.
- R-103: single continuous run · no check-ins · additive-reversible.
- **R-104 CORRECTED (executed this-turn per owner queued directive 2026-02-23T00:30Z):** RMS + DIGICOW remain named-but-unseated ONLY for **DAP-14 controlled-request gating** (approvals, extractions, standing approvals — those stay held on DQ-19/20). CENSUS admission is a DIFFERENT control: all four canonical tenants ARE admitted for census jobs. Correction landed via additive `services/census_autonomy/tenant_admission_correction.py` carrier + 12 RED-first pins including drift-detector on sealed `CENSUS_ADMITTED_TENANT_IDS == CANONICAL_TENANT_IDS`.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CLOSED + PHASE 4 (a-c-v) SEALED-A.
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

Expected: probe-7 `{'failed': 3, 'passed': 6206, 'skipped': 1, ...}` · adds **12 P4-c-v CP-CENSUS-TENANT-ADMISSION-CORRECTION invariants** most-recent (module presence + declarative posture flag + drift-detector on sealed CENSUS_ADMITTED_TENANT_IDS + per-tenant admission probes + owner §3 source map + sealed SOURCE_ROSTER registration binding + RETRO_ASSIGNMENT records + product-language admission callable + DAP-14 seating held + orthogonality assertion + verbatim-anchor discipline + boundary annotation names DQ-19 + DQ-20 + sealed carriers cited).

## 6 · POINTERS

- 10 additive modules under `services/census_autonomy/` — PHASE 3 chain sealed.
- 3 census autonomy routers + `routers/wizard_operator.py` (sealed pre-P4-a).
- **PHASE-4-a `WorkCommission.jsx` page** at `/os/work/commission` byte-identical twins.
- **NEW `contracts/skill_provisioning_record_v0.py`** (A18.1 Slice 1).
- **NEW `services/skill_provisioning_persistence.py`** (A18.2 Slice 2).
- **NEW `contracts/skill_call_governance_envelope_v0.py`** (A18.3 Slice 3) + parity snapshot + parity-map entry.
- **NEW `services/skill_call_scope_resolver.py`** (A18.5 Slice 3).
- **NEW `services/skill_donor_provenance.py`** (A18.8 Slice 4 · Final manifest · donor sha256 pinned + 356-line canon anchor).
- **NEW `services/census_autonomy/tenant_admission_correction.py`** (P4-c-v THIS-TURN · owner correction verbatim + machine-readable anchor + declarative posture pin + owner §3 source map + retro-assignment records + DAP-14 orthogonality boundary annotation + 3 product-language callables).
- Sealed donor code (byte-verbatim across Extraction-Akki + RMS-IQ-Core-2 + Akki-OS-V1) at:
  - `contracts/callable_skill_provisioning_v0.py` (101 · d61a446c)
  - `services/transform_forms/callable_skill_gate.py` (144 · 02d56745)
  - `services/transform_forms/callable_skill_persistence.py` (111 · 0590339f)
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` UNCHANGED (P4-c-v additive-only · zero router surface).
- Test files: **`test_cp_census_tenant_admission_correction_phase_4_c_v.py` (12 pins THIS-TURN)** + prior 5 A18 slices.
- Drill receipts: **`drill_receipts_cp_census_tenant_admission_correction/`** (RED_pre + GREEN_post + sweepA + sweepB).
- Ratchet-bump tool: **`tools/cp_census_tenant_admission_correction_bump_baseline.py`** (ensure_ascii=False to preserve historical unicode chars · Banked Lesson #11 first-appearance).

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
- **OWNER QUEUED CORRECTION (mid-Slice-4)** — CP-CENSUS-TENANT-ADMISSION-CORRECTION **EXECUTED THIS-TURN** as P4-c-v (Code-A + /app-companion-A + State-B landed; C-fixup + /app companion-C PENDING).
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k.

## 8 · ELEVEN BANKED LESSONS (adds BL #11 THIS-TURN)

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
11. **BL #11 first-appearance THIS-TURN (P4-c-v):** `json.dumps(indent=2)` writes on `baseline_failures.json` MUST pass `ensure_ascii=False` — the historical on-disk file uses literal unicode (em-dash, arrow, middle-dot) throughout its notes/descriptions. Default `ensure_ascii=True` escape-converts every non-ASCII char into `\uXXXX` sequences, producing a ~1000-line noise diff that masks the actual +12 line ratchet_history append. Ratchet-bump tools MUST specify `ensure_ascii=False` in the json.dumps call.

## 9 · SEAL SUMMARY (LAST-TURN P4-c-iv + THIS-TURN P4-c-v)

**P4-c-iv CP-SKILLS-LAYER-A18-8** (donor-code provenance manifest + 11 drift-detector pins · ratchet 6183→6194):

| Commit | SHA | Branch |
|---|---|---|
| Code Commit-A | `ee505425feea114acb057f87c0125f75baa6d085` | programme/track-a |
| /app companion A | `047c1b49eb5f29ef6bb1fbc678b63cff557e75ff` | main |
| State Commit-B | `55ab3335b28017613c1a50d849a0f8c7582bb0bc` | master |
| State Commit-C fixup | `e9c11e51` | master |
| /app Commit-C companion | `76cbfe1b4` | main |

**P4-c-v CP-CENSUS-TENANT-ADMISSION-CORRECTION** (declarative pins + owner §3 map + retro-assignment records + DAP-14 orthogonality · ratchet 6194→6206 · THIS-TURN):

| Commit | SHA | Branch | Purpose |
|---|---|---|---|
| Code Commit-A | `570750563e62c22dae76a775b7264da2d2334c74` | programme/track-a | 12 RED-first pins + NEW `services/census_autonomy/tenant_admission_correction.py` (~300 lines · owner correction verbatim + 3 callables) + baseline_failures.json bump |
| /app companion A | `c0d5e20537ec32b717949cea652af258c2b59e41` | main | vendored twin sync +1 file · MANIFEST 1033→1034 · structural_sha256 358f9b0e→db5ad2dc · audit + notes ORCH_BOOT regen all 14 stanzas · gitlink advance ee505425→57075056 |
| State Commit-B | `57670cf55e3ede22618f3aaeff95f57d9e452baf` | master | banks Commit-A + companion + drill receipts + DECISIONS.md CP entry + NEXT.md marker + RESUME.md rewrite + ratchet-bump tool |
| State Commit-C fixup | `471b47ade7321bb686394d65af9468ad03ec73f4` | master | R-6 boundary regen · fresh P4-c-v stanza advancing heads_last_sealed |
| /app Commit-C companion | `63be431bca4eb3ae65ad556649062e5590418c48` | main | audit ORCH_BOOT byte-identical mirror sync post-fixup |

Pre-Commit-A double-green byte-identical stripped-sha256 `8d17fd23e6050e7e53f096bcded421aa432614d419ce88b7dd5f0d6c6887f92d` IDENTICAL sweep_A (193.30s) + sweep_B (193.51s) both 6211 passed / 1 skipped / 0 failed / 520 warnings.

## 10 · AUTOPILOT NEXT

**All 5 seal commits LANDED THIS-TURN.**

**Next slice · CP-SKILLS-LAYER-SERIES-CLOSE (Slice 5 · UI-visible per owner pacing note):**
- `/dap/buildskill` UI reflecting real provisioning state or honest-gap.
- Tester walkthrough report: what a human can DO at buildskill live-or-honest-gap.

Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped → −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
