# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-09-22T23:36:00Z (**PHASE 4 (c-i) · CP-SKILLS-LAYER-A18-1 · 5-Commit-Seal LANDED · ratchet 6160 → 6165 · Doc-18-§A18.1 8-field provisioning-record contract shape-freeze LANDED · Slice 1 of CP-SKILLS-LAYER chunked series**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i) SEALED** · CP-SKILLS-LAYER opened as chunked series · A18.1 landed.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** at `/os/work/commission` · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** per conformance ruling · **P4-c-i A18.1 provisioning-record contract shape-freeze SEALED THIS-TURN**.
  - **P4-c-i seal chain:** Code `2f7d6b58` (programme/track-a · +5 measured · new contract + snapshot + 5 pins + additive CONTRACT_TO_SNAPSHOT entry) · /app companion `7402412d2` (main · vendored twin file_count 1028→1029 + MANIFEST regen + audit ORCH_BOOT + gitlink) · State `6bc0045e` (master) · Commit-C `ff125c59` · companion-C `96d9b1f01`. Pre-Commit-A double-green stripped-sha256 `176a63e2e1968fed6ae05327c7172378492fde11d1bf115f697dfdd9cc8e1030` IDENTICAL sweep_A/B both 6169/1/0/520.
  - **CP-SKILLS-LAYER sub-slices queued** (per SPEC_COVERAGE_GAP_DIGEST 5-of-8 A18.x NOT-BUILT bucket):
    - c-ii · A18.2 write-once slice-binding guardrail — corpus_slice_ref immutability + new-material=new-skill_id enforcement.
    - c-iii · A18.3 + A18.5 governance-and-scope UI cues.
    - c-iv · A18.8 donor-code intake (∼356 lines from RMS-IQ-Core-2 + Akki-OS-V1).
  - Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- **Ratchet floor: `6165`** (was 6160 pre-P4-c-i · +5 canonical measured) · baseline_failures_sha256 `8f5e23b37b10cf3ae74783b48b1933a87c40c8f6e22dd6de455076e8ac213150`.

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

Expected: probe-7 `{'failed': 3, 'passed': 6165, 'skipped': 1, ...}` · adds **5 P4-c-i CP-SKILLS-LAYER-A18-1 invariants** most-recent (A18.1 provisioning-record shape-freeze).

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

## 8 · SEVEN BANKED LESSONS

1. **YAML plain-scalar hazard** — RE-HONORED this-turn in P4-a state Commit-C fixup (all embedded-colon patterns replaced with dashes throughout the fresh stanza).
2. Server.py mirror-edit rule — mirror pair is `/app/backend/server.py ↔ pod_shell/backend/server.py` (NOT spine ↔ pod_shell).
3. Canon-9 §3 negative-scan literal-substring hazard — compose attr-name via string concatenation.
4. Producer-bridge additive discipline — AST-scan bans engine-internal imports.
5. Frontend banned-marker discipline — docstring rephrase at same-Commit-A.
6. **ratchet_history entry `passed` field must equal NEW post-seal floor** (matching `counts_at_baseline.passed`), NOT pre-seal floor · authored this-turn after right-reason RED on `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` (6150 != 6157) cured same-slice.
7. **`json.dump(indent=2)` drift on `baseline_failures.json`** — prior file was 4-space indented · use `indent=4` on next Commit-A regen to preserve prior format · semantic content unchanged · sha256 pinned in ORCH_BOOT.md matches.

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

- **CP-SKILLS-LAYER-A18-2** (Slice 2) — write-once slice-binding guardrail (corpus_slice_ref immutability · new-material=new-skill_id enforcement).
- **CP-SKILLS-LAYER-A18-3 + A18-5** (Slice 3) — governance-and-scope UI cues.
- **CP-SKILLS-LAYER-A18-8** (Slice 4) — donor-code intake (∼356 lines LIFT from RMS-IQ-Core-2 + Akki-OS-V1).
- Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
- Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- Follow-on Connect-tab copy-alignment sub-slice deferred (banked-not-blocking).

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
