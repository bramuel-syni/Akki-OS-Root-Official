# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-02-23T00:17:00Z (**PHASE 4 (c-iii) · CP-SKILLS-LAYER-A18-3 + A18-5 · 5-Commit-Seal LANDED · ratchet 6171 → 6183 · A18.3 per-call governance envelope contract + A18.5 server-side scope resolver LANDED on top of P4-c-ii A18.2 write-once persistence · Slice 3 of CP-SKILLS-LAYER chunked series**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i) + P4-(c-ii) + P4-(c-iii) SEALED** · CP-SKILLS-LAYER chunked series 3/5 complete.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** · **P4-c-i A18.1 shape-freeze** · **P4-c-ii A18-2 write-once slice-binding** · **P4-c-iii A18.3 + A18.5 governance-and-scope structural pins SEALED THIS-TURN**.
  - **P4-c-iii seal chain:** Code `dafb45c8b004bad233439920c85cfae0847c6800` (programme/track-a · +12 measured · new contracts/skill_call_governance_envelope_v0.py + new services/skill_call_scope_resolver.py + new parity snapshot + 12 pins + parity-map additive entry) · /app companion `b312ec870a58a39b557b39e7c34437a8d9e485a1` (main · vendored file_count 1030→1032 · structural_sha256 141cac1c · audit ORCH_BOOT regen 6183) · State Commit-B `a3f228b0b070af55d4d80cf3b268c76c87950193` · Commit-C fixup `<PENDING-P4-C-III-CC>` · companion-C `<PENDING-P4-C-III-CC-APP>`. Pre-Commit-A double-green stripped-sha256 `32d6e0969064b9fd947be0e1f91c9f46d042393b6044b3a40640cccd1e521739` IDENTICAL sweep_A/B both 6188/1/0/520.
  - **CP-SKILLS-LAYER sub-slices REMAINING:**
    - c-iv · A18.8 donor-code intake (~356 lines LIFT from RMS-IQ-Core-2 + Akki-OS-V1).
    - **c-CLOSE · CP-SKILLS-LAYER-SERIES-CLOSE** UI-visible tester walkthrough (buildskill UI reflecting real provisioning state or honest gap per owner pacing note).
  - Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- **Ratchet floor: `6183`** (was 6171 pre-P4-c-iii · +12 canonical measured) · baseline_failures_sha256 `81e790bbbc42cc13aa178c178c6a84d73001d83150ebfba880bd317351759a88`.

## 2 · STANDING (R-102 + R-103 + R-104 + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · PHASE 3 EXIT-EVIDENCED · PHASE 4 (a) Commission wizard LIVE · A18.3 + A18.5 structural pins LANDED (runtime wiring deferred to CP-SKILLS-LAYER-SERIES-CLOSE per Slice 5 owner pacing).
- R-103: single continuous run · no check-ins · additive-reversible.
- R-104: RMS + DIGICOW named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CLOSED + PHASE 4 (a-c-iii) SEALED.
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

Expected: probe-7 `{'failed': 3, 'passed': 6183, 'skipped': 1, ...}` · adds **12 P4-c-iii CP-SKILLS-LAYER-A18-3-A18-5 invariants** most-recent (6 A18.3 envelope pins + 6 A18.5 resolver pins).

## 6 · POINTERS

- 10 additive modules under `services/census_autonomy/` — PHASE 3 chain sealed.
- 3 census autonomy routers + `routers/wizard_operator.py` (sealed pre-P4-a).
- **PHASE-4-a `WorkCommission.jsx` page** at `/os/work/commission` byte-identical twins across `/app/frontend/src` + `pod_shell/frontend/src`.
- **NEW `contracts/skill_call_governance_envelope_v0.py`** (A18.3 · Pydantic 7-field frozen envelope · extra=forbid · ISO-8601 tz-aware decision_ts) + parity snapshot + parity-map entry.
- **NEW `services/skill_call_scope_resolver.py`** (A18.5 · resolve_scope_for_call() + ClientSuppliedScopeRefused + SkillNotProvisioned · reads scope from sealed A18.1 record via A18.2 persistence · REFERENCE-NOT-COPY).
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` UNCHANGED (A18-3-A18-5 additive-only · zero router surface at this slice).
- Test files: 10 CP-CENSUS-AUTONOMY + `test_cp_commission_wizard_live_phase_4_a.py` + `test_cp_connect_conformance_ruling_phase_4_b_i.py` + `test_cp_skills_layer_a18_1_phase_4_c_i.py` + `test_cp_skills_layer_a18_2_phase_4_c_ii.py` + **`test_cp_skills_layer_a18_3_a18_5_phase_4_c_iii.py` (12 pins THIS-TURN)**.
- Drill receipts: existing + **`drill_receipts_cp_skills_layer_a18_3_a18_5/` (RED-pre + GREEN-post + Sweep A + Sweep B logs)**.

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · RMS approving authority · named-but-unseated**.
- **DQ-20** — **P1 · DIGICOW approving authority · named-but-unseated**.
- **DQ-GPU-SSH-KEYS** — SELF-RESOLVED 2026-09-22T19:00Z.
- **-2 collection-drift** — P1 forensic queued behind Order B audit.
- **Connect-wizard disambiguation** — RESOLVED at P4-b-i (LATER-wins · React ≡ prototype 4-panel shape · Item (b) Connect-half CLOSED as ALREADY-LIVE). Follow-on copy-alignment sub-slice banked-not-blocking.
- **CP-SKILLS-LAYER Slice 3 owner ratification** — user confirmed plan verbatim (a) Y proceed (b) primary Doc-18 §A18-3 / §A18-5 anchors + secondary carrier cite for engineer_key_grant.py (c) no owner action landed since P4-c-ii · boundary unchanged.
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k.

## 8 · TEN BANKED LESSONS

1. **YAML plain-scalar hazard** — embedded-colon patterns crash `yaml.safe_load`; use dashes in generator/regeneration_reason plain-scalar values.
2. Server.py mirror-edit rule — mirror pair is `/app/backend/server.py ↔ pod_shell/backend/server.py` (NOT spine ↔ pod_shell).
3. Canon-9 §3 negative-scan literal-substring hazard — compose attr-name via string concatenation.
4. Producer-bridge additive discipline — AST-scan bans engine-internal imports.
5. Frontend banned-marker discipline — docstring rephrase at same-Commit-A.
6. **ratchet_history entry `passed` field must equal NEW post-seal floor** (not pre-seal) — matching `counts_at_baseline.passed`.
7. **`json.dump(indent=2)` drift on `baseline_failures.json`** — current format is 2-space post-P4-a; preserve on subsequent Commit-As.
8. **Drift-detector tests against another sealed contract must inspect the actual JSON schema before writing field-name assertions** — mirror the shape-freeze pattern of `test_snapshot_matches_current_schema` rather than hard-coding specific field names; if hard-coding is unavoidable (non-collision proofs), assert with both DIRECTIONS.
9. **NEW file at `backend/contracts/` / `backend/services/` requires `tools/prod_vendor_sync.py` run same-Commit-A** — else `test_vendored_tree_mirrors_spine` fires right-reason. Vendored MANIFEST.json file_count + structural_sha256 must update before double-green sweep.
10. **NEW Pydantic contract requires same-slice CONTRACT_TO_SNAPSHOT map additive entry** at `tests/invariants/test_frozen_contract_snapshot_parity.py` (line ~93 area) alongside the parity snapshot JSON — else parity bijectivity test fires right-reason RED. Same-slice cure per BL from A18.1 slice.

## 9 · SEAL SUMMARY (LAST-TURN P4-c-ii + THIS-TURN P4-c-iii)

**P4-c-ii CP-SKILLS-LAYER-A18-2** (write-once slice-binding guardrail LANDED · ratchet 6165→6171):

| Commit | SHA | Branch |
|---|---|---|
| Code Commit-A | `f7f08207da458007db4a2024a2934f97dffe9537` | programme/track-a |
| /app companion A | `8989afd4420a250d47138f29d45f45eea845ac63` | main |
| State Commit-B | `d847070dc3e23726ae38c621b3895b4dd99194b0` | master |
| State Commit-C fixup | `b21b9192a8d4b65409d0cfb8bb8fa21badad3da8` | master |
| /app Commit-C companion | `3b048cb30a2a4c1d66708c4aa490f2e636b90d5e` | main |

**P4-c-iii CP-SKILLS-LAYER-A18-3-A18-5** (per-call governance envelope contract + server-side scope resolver LANDED · ratchet 6171→6183):

| Commit | SHA | Branch | Purpose |
|---|---|---|---|
| Code Commit-A | `dafb45c8b004bad233439920c85cfae0847c6800` | programme/track-a | 12 RED-first structural pins + envelope contract + parity snapshot + scope resolver + parity-map entry + baseline_failures.json bump |
| /app companion A | `b312ec870a58a39b557b39e7c34437a8d9e485a1` | main | vendored twin sync +2 files · MANIFEST regen 1030→1032 · audit + notes ORCH_BOOT regen 6183 · gitlink advance |
| State Commit-B | `a3f228b0b070af55d4d80cf3b268c76c87950193` | master | banks A + companion + drill receipts + baseline_failures_sha256 `81e790bb...` |
| State Commit-C fixup | `<PENDING-P4-C-III-CC>` | master | R-6 boundary regen · fresh P4-c-iii stanza · BL #10 first-appearance |
| /app Commit-C companion | `<PENDING-P4-C-III-CC-APP>` | main | audit ORCH_BOOT byte-identical mirror sync |

Pre-Commit-A double-green byte-identical stripped-sha256 `32d6e0969064b9fd947be0e1f91c9f46d042393b6044b3a40640cccd1e521739` IDENTICAL sweep_A/B both 6188 passed / 1 skipped / 0 failed / 520 warnings in ~191s each.

## 10 · AUTOPILOT NEXT

**Owner pacing note banked** (2026-09-22T~23:38Z verbatim): "the skills series is contract/guardrail-heavy — remember R-102's bar is USER-visible productized-or-honest-gap, so when the series closes, ensure the skills surface in the UI (buildskill view) reflects the real provisioning state or an honest gap, and note in the series-close report what a tester can DO with skills, not just what contracts exist."

Implication: CP-SKILLS-LAYER series close (after A18.8 lands) MUST include a UI-visible surface tying `/dap/buildskill` (or equivalent) to real `SkillProvisioningRecordV0` state or an honest-gap `BackendPending` cite. Series-close report MUST document a concrete tester-facing what-can-I-do-with-skills walkthrough.

- **CP-SKILLS-LAYER-A18-8** (Slice 4 · NEXT) — donor-code intake (~356 lines LIFT from RMS-IQ-Core-2 + Akki-OS-V1 · frozen provisioning contract impl + per-call gate + write-once persistence — pattern already sealed at A18.1/2/3/5, so this slice absorbs the actual donor code as additive verbatim carriers with parity attestation).
- **CP-SKILLS-LAYER-SERIES-CLOSE** (Slice 5 · UI-visible per owner pacing note) — `buildskill` (or workstudio/skills) UI reflecting real provisioning state or honest-gap · series-close tester walkthrough report.
- Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
- Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- Follow-on Connect-tab copy-alignment sub-slice deferred (banked-not-blocking).

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
