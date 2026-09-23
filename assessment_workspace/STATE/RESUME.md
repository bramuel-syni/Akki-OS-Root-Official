# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-02-23T00:32:00Z (**PHASE 4 (c-iv) · CP-SKILLS-LAYER-A18-8 · 5-Commit-Seal LANDED · ratchet 6183 → 6194 · A18.8 donor-code provenance manifest + 11 drift-detector pins over sealed 356-line donor code · Slice 4 of CP-SKILLS-LAYER chunked series · OWNER QUEUED CORRECTION banked verbatim in DECISIONS.md · slice queue reordered - CP-CENSUS-TENANT-ADMISSION-CORRECTION opens next, then CP-SKILLS-LAYER-SERIES-CLOSE**).

---

## 1 · POSITION

- **Phase:** PHASE 3 CLOSED · **P4-a + P4-(b-i) + P4-(c-i) + P4-(c-ii) + P4-(c-iii) + P4-(c-iv) SEALED** · CP-SKILLS-LAYER chunked series 4/5 complete.
- **Turn queue (condensed):**
  - PHASE 3 CLOSED · **P4-a Commission wizard LIVE** · **P4-b-i Connect-half CLOSED as ALREADY-LIVE** · **P4-c-i A18.1 shape-freeze** · **P4-c-ii A18-2 write-once slice-binding** · **P4-c-iii A18.3 + A18.5 governance-and-scope pins** · **P4-c-iv A18.8 donor-code provenance SEALED THIS-TURN**.
  - **P4-c-iv seal chain:** Code `ee505425feea114acb057f87c0125f75baa6d085` (programme/track-a · +11 measured · new services/skill_donor_provenance.py + 11 pins) · /app companion `047c1b49eb5f29ef6bb1fbc678b63cff557e75ff` (main · vendored file_count 1032→1033 · structural_sha256 358f9b0e · audit ORCH_BOOT regen 6194) · State Commit-B `55ab3335b28017613c1a50d849a0f8c7582bb0bc` · Commit-C fixup `<PENDING-P4-C-IV-CC>` · companion-C `<PENDING-P4-C-IV-CC-APP>`. Pre-Commit-A double-green stripped-sha256 `dfb8d45637954398db152812311e6036873591c80dc126b44b3fe390e3f8ed80` IDENTICAL sweep_A/B both 6199/1/0/520.
  - **QUEUED (owner correction · mid-Slice-4 · verbatim in DECISIONS.md):** CP-CENSUS-TENANT-ADMISSION-CORRECTION opens NEXT (small · RED-first · own §3.3 5-Commit-Seal): admits all four tenants (RMS + DIGICOW + BDO + Trinity) for census jobs specifically; DAP-14 controlled-request gating stays held on DQ-19/20; source-to-tenant bindings per CP-TENANT-SEPARATION §3 verbatim; retro-assignment additive; zero-mixing invariants land as RED pins.
  - **CP-SKILLS-LAYER-SERIES-CLOSE** (Slice 5 of 5) SLOTS AFTER the census correction — UI-visible tester walkthrough at `/dap/buildskill` (live-or-honest-gap per owner pacing note).
  - Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - Then −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.
- **Ratchet floor: `6194`** (was 6183 pre-P4-c-iv · +11 canonical measured) · baseline_failures_sha256 `ec58438f667cd17686b7ffcf29a58225e1bef88c2b4371f1347e2baa4b70a1ac`.

## 2 · STANDING (R-102 + R-103 + R-104 [CORRECTED] + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · PHASE 3 EXIT-EVIDENCED · PHASE 4 (a) Commission wizard LIVE · A18.3/A18.5 structural pins LANDED · A18.8 donor code with provenance manifest LANDED · Slice 5 UI-visible walkthrough queued.
- R-103: single continuous run · no check-ins · additive-reversible.
- **R-104 CORRECTED per owner queued directive (2026-02-23T00:30Z):** RMS + DIGICOW remain named-but-unseated ONLY for **DAP-14 controlled-request gating** (approvals, extractions, standing approvals — those stay held on DQ-19/20). CENSUS admission is a DIFFERENT control: all four tenants MUST be admitted for census jobs (RMS + DIGICOW + BDO + Trinity). Correction lands next slice.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CLOSED + PHASE 4 (a-c-iv) SEALED.
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

Expected: probe-7 `{'failed': 3, 'passed': 6194, 'skipped': 1, ...}` · adds **11 P4-c-iv CP-SKILLS-LAYER-A18-8 invariants** most-recent (4 provenance-manifest + 6 sealed-donor drift-detectors + 1 manifest-shape).

## 6 · POINTERS

- 10 additive modules under `services/census_autonomy/` — PHASE 3 chain sealed.
- 3 census autonomy routers + `routers/wizard_operator.py` (sealed pre-P4-a).
- **PHASE-4-a `WorkCommission.jsx` page** at `/os/work/commission` byte-identical twins.
- **NEW `contracts/skill_provisioning_record_v0.py`** (A18.1 Slice 1).
- **NEW `services/skill_provisioning_persistence.py`** (A18.2 Slice 2).
- **NEW `contracts/skill_call_governance_envelope_v0.py`** (A18.3 Slice 3) + parity snapshot + parity-map entry.
- **NEW `services/skill_call_scope_resolver.py`** (A18.5 Slice 3).
- **NEW `services/skill_donor_provenance.py`** (A18.8 Slice 4 · Final manifest · donor sha256 pinned + 356-line canon anchor).
- Sealed donor code (byte-verbatim across Extraction-Akki + RMS-IQ-Core-2 + Akki-OS-V1) at:
  - `contracts/callable_skill_provisioning_v0.py` (101 · d61a446c)
  - `services/transform_forms/callable_skill_gate.py` (144 · 02d56745)
  - `services/transform_forms/callable_skill_persistence.py` (111 · 0590339f)
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` UNCHANGED (A18.8 additive-only · zero router surface).
- Test files: **`test_cp_skills_layer_a18_8_phase_4_c_iv.py` (11 pins THIS-TURN)** + prior 4 A18 slices.
- Drill receipts: **`drill_receipts_cp_skills_layer_a18_8/`** (RED_pre + GREEN_post + sweepA + sweepB).

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · RMS approving authority · named-but-unseated · applies to DAP-14 controlled requests ONLY, not census admission**.
- **DQ-20** — **P1 · DIGICOW approving authority · named-but-unseated · applies to DAP-14 controlled requests ONLY, not census admission**.
- **DQ-GPU-SSH-KEYS** — SELF-RESOLVED 2026-09-22T19:00Z.
- **-2 collection-drift** — P1 forensic queued behind Order B audit.
- **Connect-wizard disambiguation** — RESOLVED at P4-b-i.
- **OWNER QUEUED CORRECTION (mid-Slice-4)** — CP-CENSUS-TENANT-ADMISSION-CORRECTION queued to open post-P4-c-iv seal; banked verbatim in DECISIONS.md.
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k.

## 8 · TEN BANKED LESSONS (unchanged this-slice)

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

## 9 · SEAL SUMMARY (LAST-TURN P4-c-iii + THIS-TURN P4-c-iv)

**P4-c-iii CP-SKILLS-LAYER-A18-3-A18-5** (per-call governance envelope + server-side scope resolver · ratchet 6171→6183):

| Commit | SHA | Branch |
|---|---|---|
| Code Commit-A | `dafb45c8b004bad233439920c85cfae0847c6800` | programme/track-a |
| /app companion A | `b312ec870a58a39b557b39e7c34437a8d9e485a1` | main |
| State Commit-B | `a3f228b0b070af55d4d80cf3b268c76c87950193` | master |
| State Commit-C fixup | `c87a424f66e037149e2c939a2abbc09ec7a1ee37` | master |
| /app Commit-C companion | `42f450d91...` | main |

**P4-c-iv CP-SKILLS-LAYER-A18-8** (donor-code provenance manifest + 11 drift-detector pins · ratchet 6183→6194):

| Commit | SHA | Branch | Purpose |
|---|---|---|---|
| Code Commit-A | `ee505425feea114acb057f87c0125f75baa6d085` | programme/track-a | 11 RED-first pins + provenance manifest + baseline_failures.json bump |
| /app companion A | `047c1b49eb5f29ef6bb1fbc678b63cff557e75ff` | main | vendored twin sync +1 file · MANIFEST 1032→1033 · audit + notes ORCH_BOOT regen · gitlink advance |
| State Commit-B | `55ab3335b28017613c1a50d849a0f8c7582bb0bc` | master | banks A + companion + drill receipts + OWNER QUEUED CORRECTION verbatim |
| State Commit-C fixup | `<PENDING-P4-C-IV-CC>` | master | R-6 boundary regen · fresh P4-c-iv stanza |
| /app Commit-C companion | `<PENDING-P4-C-IV-CC-APP>` | main | audit ORCH_BOOT byte-identical mirror sync |

Pre-Commit-A double-green byte-identical stripped-sha256 `dfb8d45637954398db152812311e6036873591c80dc126b44b3fe390e3f8ed80` IDENTICAL sweep_A/B both 6199 passed / 1 skipped / 0 failed / 520 warnings in ~192s each.

## 10 · AUTOPILOT NEXT

**QUEUED (owner correction · mid-Slice-4 · verbatim in DECISIONS.md):**
- **CP-CENSUS-TENANT-ADMISSION-CORRECTION** opens NEXT. Small slice, RED-first, own §3.3 5-Commit-Seal.
  - Admit all four tenants (RMS + DIGICOW + BDO + Trinity) for census jobs specifically at `CENSUS_ADMITTED_TENANT_IDS` (or its equivalent gate).
  - Bind sources per CP-TENANT-SEPARATION §3 verbatim (registration map).
  - Add RED pins proving zero-mixing (RMS census rows invisible to DIGICOW principal; vice versa).
  - Retro-assignment additive (Digicow census_0001/_0002 → DIGICOW; RMS Item-3 receipts → RMS).
  - Docstring boundary annotation at census-admission module: DAP-14 controlled-request gating stays held on DQ-19/20 · census admission is a different control.

**Then CP-SKILLS-LAYER-SERIES-CLOSE (Slice 5 · UI-visible per owner pacing note):**
- `/dap/buildskill` UI reflecting real provisioning state or honest-gap.
- Tester walkthrough report: what a human can DO at buildskill live-or-honest-gap.

Then CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped → −2 collection-drift forensic → Order B → Order A → ops lanes → BUILD_JOURNAL + OWNER_RETURN_REPORT.

Report at seal boundaries per §6.8. Zero check-ins. Standing bounds unchanged.
