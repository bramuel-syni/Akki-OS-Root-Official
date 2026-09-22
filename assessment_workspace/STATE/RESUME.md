# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-09-22T23:54:00Z (**PHASE 4 (c-ii) · CP-SKILLS-LAYER-A18-2 · 5-Commit-Seal LANDED · ratchet 6165 → 6171 · A18-2 write-once slice-binding guardrail LANDED on top of P4-c-i A18.1 contract · Slice 2 of CP-SKILLS-LAYER chunked series**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i) + P4-(c-ii) SEALED** · CP-SKILLS-LAYER chunked series 2/5 complete.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** · **P4-c-i A18.1 shape-freeze** · **P4-c-ii A18-2 write-once slice-binding SEALED THIS-TURN**.
  - **P4-c-ii seal chain:** Code `f7f08207da458007db4a2024a2934f97dffe9537` (programme/track-a · +6 measured · new services/skill_provisioning_persistence.py + 6 pins) · /app companion `8989afd4420a250d47138f29d45f45eea845ac63` (main · vendored file_count 1029→1030) · State `d847070dc3e23726ae38c621b3895b4dd99194b0` · Commit-C `b21b9192a8d4b65409d0cfb8bb8fa21badad3da8` · companion-C `3b048cb30a2a4c1d66708c4aa490f2e636b90d5e`. Pre-Commit-A double-green stripped-sha256 `b2a90405dcbee9f076cb039870e24ac83428f6894d5521f3f6133b3bbcbb45f3` IDENTICAL sweep_A/B both 6175/1/0/520.
  - **CP-SKILLS-LAYER sub-slices REMAINING:**
    - c-iii · A18.3 + A18.5 governance-and-scope UI cues (per-call gate + server-side scope enforcement).
    - c-iv · A18.8 donor-code intake (~356 lines LIFT).
    - **c-CLOSE · CP-SKILLS-LAYER-SERIES-CLOSE** UI-visible tester walkthrough (buildskill UI reflecting real provisioning state or honest gap per owner pacing note).
  - Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- **Ratchet floor: `6171`** (was 6165 pre-P4-c-ii · +6 canonical measured) · baseline_failures_sha256 `263c8586947d5b6ce838036920a94f841065053a781afe3c511d981c97e978c2`.

## 2 · STANDING (R-102 + R-103 + R-104 + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · PHASE 3 EXIT-EVIDENCED · PHASE 4 (a) Commission wizard now LIVE (backend verified live via curl · frontend routed at `/os/work/commission`).
- R-103: single continuous run · no check-ins · additive-reversible.
- R-104: RMS + DIGICOW named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CLOSED + PHASE 4 (a) SEALED.
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
tail -80 /app/assessment_workspace/STATE/DECISIONS.md && cat /app/assessment_workspace/STATE/NEXT.md
```

Expected: probe-7 `{'failed': 3, 'passed': 6171, 'skipped': 1, ...}` · adds **6 P4-c-ii CP-SKILLS-LAYER-A18-2 invariants** most-recent (A18-2 write-once slice-binding guardrail).

## 6 · POINTERS

- 10 additive modules under `services/census_autonomy/` — PHASE 3 chain sealed.
- 3 census autonomy routers + `routers/wizard_operator.py` (sealed pre-P4-a · 6 endpoints at `/wizard/operator` prefix consumed by `CommissionWizard.jsx`).
- **NEW `pod_shell/frontend/src/pages/os/WorkCommission.jsx` + `/app/frontend/src/` twin** (byte-identical · renders `<CommissionWizard />` at `/os/work/commission`).
- 3 additive React overlays: `CensusAutonomyDrawer.jsx` + `ResponseRequiredBadge.jsx` (portal overlays) + hooks + **PHASE-4-a `WorkCommission.jsx` page** — all `/app/frontend/src/` twins byte-identical to `pod_shell/frontend/src/`.
- App.js additive mounts byte-identical across twins (drawer + badge overlays above prototype iframe + Route `/os/work/commission` in workstudio block).
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` (post-A''''-cont-A · A'''-cont-B + P4-a were frontend-only · zero server.py edits).
- Test files: 10 CP-CENSUS-AUTONOMY test files + **`test_cp_commission_wizard_live_phase_4_a.py` (7 pins THIS-TURN)**.
- Drill receipts: 9 census autonomy dirs + E2E exit proof + **`_cp_commission_wizard_live_phase_4_a/` (RED-pre + GREEN-post + pre-Commit-A double-green + post-seal double-green logs)**.

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · RMS approving authority · named-but-unseated**.
- **DQ-20** — **P1 · DIGICOW approving authority · named-but-unseated**.
- **DQ-GPU-SSH-KEYS** — SELF-RESOLVED 2026-09-22T19:00Z.
- **-2 collection-drift** — P1 forensic queued behind Order B audit.
- **NEW: Connect-wizard disambiguation** — **RESOLVED THIS-TURN** via P4-b-i CP-CONNECT-CONFORMANCE-RULING · LATER-wins ordering applied · prototype 4-panel shape MATCHES React 4-tab shape · Item (b) Connect-half CLOSED as ALREADY-LIVE per R-102. Follow-on copy-alignment sub-slice deferred (banked-not-blocking).
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k.

## 8 · NINE BANKED LESSONS

1. **YAML plain-scalar hazard** — embedded-colon patterns crash `yaml.safe_load`; use dashes in generator/regeneration_reason plain-scalar values.
2. Server.py mirror-edit rule — mirror pair is `/app/backend/server.py ↔ pod_shell/backend/server.py` (NOT spine ↔ pod_shell).
3. Canon-9 §3 negative-scan literal-substring hazard — compose attr-name via string concatenation.
4. Producer-bridge additive discipline — AST-scan bans engine-internal imports.
5. Frontend banned-marker discipline — docstring rephrase at same-Commit-A.
6. **ratchet_history entry `passed` field must equal NEW post-seal floor** (not pre-seal) — matching `counts_at_baseline.passed`.
7. **`json.dump(indent=2)` drift on `baseline_failures.json`** — prior file was 4-space indented; current format is 2-space post-P4-a; preserve current format on subsequent Commit-As.
8. **Drift-detector tests against another sealed contract must inspect the actual JSON schema before writing field-name assertions** — my P4-c-i initial `test_provisioning_record_is_distinct_from_a18_7_provenance_contract` incorrectly assumed A18.7 had a `steps` field (actual: `provenance_chain`). Cured same-slice. Pattern-of-record: mirror the shape-freeze pattern of `test_snapshot_matches_current_schema` rather than hard-coding specific field names; if hard-coding field names is unavoidable (as in non-collision proofs), assert with both DIRECTIONS (each contract has a field the other doesn't).
9. **NEW file at `backend/contracts/` requires `tools/prod_vendor_sync.py` run same-Commit-A** — else `test_vendored_tree_byte_identical_mirror_of_spine` fires right-reason. Vendored MANIFEST.json file_count + structural_sha256 must be updated before double-green sweep. Also applies to `backend/services/` and `backend/routers/` — any new file within the vendored scope requires re-sync.

## 9 · SEAL SUMMARY (LAST-TURN P4-a + THIS-TURN P4-b-i)

**P4-a CP-COMMISSION-WIZARD-LIVE** (Commission wizard now LIVE at `/os/work/commission` · ratchet 6150→6157):

| Commit | SHA | Branch |
|---|---|---|
| Code Commit-A | `032ada921d8e359ec0c5322d9a354af9f5b973fa` | programme/track-a |
| /app companion A | `42bab1711a013f489b8fad1d0dd71729be7299f6` | main |
| State Commit-B | `56461dfa3802ecf4f71e810695d892d33e5e4ab9` | master |
| State Commit-C fixup | `d5be537165c8d16591e3ea836a7cf408101e7206` | master |
| /app Commit-C companion | `5b4cd68e06f80995cc2d630283a5ae2e8d89f68a` | main |

**P4-b-i CP-CONNECT-CONFORMANCE-RULING** (Item (b) Connect-half CLOSED as ALREADY-LIVE per R-102 · ratchet 6157→6160):

| Commit | SHA | Branch | Purpose |
|---|---|---|---|
| Code Commit-A | `d6eee5d6b94bc6fef28a076459bd41011fdbabbe` | programme/track-a | 3 forward-drift-detector pins + conformance ruling + baseline_failures.json bump |
| /app companion A | `9f8411716bfc9a1fcd92b87f42a503ee7edb7d39` | main | audit ORCH_BOOT ratchet regen + gitlink advance |
| State Commit-B | `760ce38f02b607ea686b39098bea056ca8a51230` | master | banks A + companion + drill receipts + baseline_failures_sha256 `48c13b0d...` |
| State Commit-C fixup | `6f532a767f45d63b1dc296b4867b1f7085320e8c` | master | R-6 boundary regen · fresh P4-b-i stanza · Banked-Lesson-#1 respected |
| /app Commit-C companion | `216569fc5fea2d3e414372e93037d2875636425d` | main | audit ORCH_BOOT byte-identical mirror sync |

Pre-Commit-A double-green byte-identical stripped-sha256 `033467633e7e62f8c72b76b92d4467ae1a643a82da42aedb50c168552b58f4a5` IDENTICAL sweep_A/B both 6163 passed / 1 skipped / 0 failed / 520 warnings in ~192s each.

## 10 · AUTOPILOT NEXT

**Owner pacing note banked** (2026-09-22T~23:38Z verbatim): "the skills series is contract/guardrail-heavy — remember R-102's bar is USER-visible productized-or-honest-gap, so when the series closes, ensure the skills surface in the UI (buildskill view) reflects the real provisioning state or an honest gap, and note in the series-close report what a tester can DO with skills, not just what contracts exist."

Implication: CP-SKILLS-LAYER series close (after A18-8 lands) MUST include a UI-visible surface tying `/dap/buildskill` (or equivalent) to real `SkillProvisioningRecordV0` state or an honest-gap `BackendPending` cite. Series-close report MUST document a concrete tester-facing what-can-I-do-with-skills walkthrough (or the honest-gap declaration if backend-pending).

- **CP-SKILLS-LAYER-A18-3 + A18-5** (Slice 3) — governance-and-scope UI cues (per-call gate + server-side scope enforcement UI cues). OPENS NEXT.
- **CP-SKILLS-LAYER-A18-8** (Slice 4) — donor-code intake (∼356 lines LIFT from RMS-IQ-Core-2 + Akki-OS-V1).
- **CP-SKILLS-LAYER-SERIES-CLOSE** (Slice 5 · UI-visible per owner pacing note) — `buildskill` (or workstudio/skills) UI reflecting real provisioning state or honest-gap · series-close tester walkthrough report.
- Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
- Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- Follow-on Connect-tab copy-alignment sub-slice deferred (banked-not-blocking).

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
