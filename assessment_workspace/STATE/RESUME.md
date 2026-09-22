# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-02-XXT01:30:00Z (Turn 4 sub-slice **4k SEAL close** · CP-R91-RETIRE-SUPERSEDE partial-retirement · 2 v8-substitution baselines retired · ratchet 6080 → 6086 · R-106 CENSUS AUTONOMY SERVICE banked for PHASE 3 shape).

---

## 1 · POSITION

- **Phase:** PHASE 3 · **CENSUS AUTONOMY SERVICE** NEXT (per R-106 owner ruling 2026-02-XX · supervisor-managed persistent worker · scheduled weekly runs · on-demand JWT-gated trigger · productized census engine · zero-agent-in-loop · ops proof at seal).
- **Turn queue**:
  - 4a-4f ✅ SEALED (details in DECISIONS.md).
  - 4g DAP surface verification receipt ✅ SEALED at state master `3651dc80` (2026-09-22T09:55Z).
  - 4h ✅ SEALED at code `8dcbd481` · state B `4fcbaf5e` · state C `00987fdc` · /app companion `480db11f` · /app C `a4921edb` (mirror-closure-only Path R · R-105).
  - 4i ✅ SEALED at state Commit-B `c56449763f036e2cb006cf1ac1f7367c277ca20f` (state-only 3-commit · deferrals banked · ratchet UNCHANGED).
  - 4j ✅ SEALED at code `d2bfb02324bcfb0b98aa78f8b4f47dab5e631a6f` · /app companion `68b6956abcc9b3e1d1d53fdb1bac08ee7bd2bf08` · state B `8998e173d6f24c4c5b1a465facaaa577fb9c9528` · state C `51d3d2a9a321876137887e51db0f642ed1b6a0c2` · /app C `b23f783696d100a763c5292cd33f094c21a0c2a4` (CP-TENANT-SEPARATION open primary · +8 invariants · ratchet 6072→6080 · DQ-19+DQ-20 banked).
  - **4k ✅ SEALED** at code `eed6c032a1cf7155df33cac2a788eeabb72531e8` · /app companion `eb861ecae55acc6763d9096ffe0f88645a3ed502` · state B `f775adf6e10cd1f32b51b6ea85d44012c26a2672` · state C `06656965c1ca33ae025f3b156dd89cfdcebaef0a` · /app C `ebcede68da8275531fe928c40f2106fdb74c73ae` (CP-R91-RETIRE-SUPERSEDE partial · 2 v8-substitution retired · ratchet 6080→6086 +6 measured [+4 new inv + 2 absorbed] · double-green stripped-sha256 `796d3bac14c87ce8ec0902b106a6a78dc102b9c007ac31fd7d727d09825f30ed` IDENTICAL verbose · fresh-gate stripped-sha256 `a715b5c059ae1df35a47d4de1002c94197652be83608febc9aab7f00c40f89d7` IDENTICAL -q · both pairs 6087/1 skipped · post-seal-verify 6087/1 skipped 175.62s · sealed R-86 + R-88 carriers preserved by construction).
  - **PHASE 3 NEXT · CENSUS AUTONOMY SERVICE** per R-106 verbatim: supervisor-managed persistent worker · scheduled weekly runs + on-demand · engine ported from estate_census v3 additively · tenant-scoped · LawfulBasisAdmit + all-reads-receipted + no-second-store · bounded/budgeted · mid-run decision queue → UI badge (never stalls) · auto-flowing results · live progress observable · degradation honesty · ops proof at seal (pod-restart-resume + AKKI-TEST no-agent end-to-end).
  - PHASE 4 (a-h) → Order B → Order A → BUILD_JOURNAL + OWNER_RETURN_REPORT.
  - R-101 preserved WHAT: mirror closure done at 4h · v8-substitution retirement done at 4k · mirror-drift retirement queued behind CP-APP-JS-UNIFY closure (future slice).
  - R-102 MASTER DIRECTIVE: productized-or-honest-gap · autopilot · anti-compaction.
  - R-103 amendment: no check-ins · autonomous forks with annotation · applied at 4h + 4i + 4j + 4k.
  - R-104 approving authorities: named-but-unseated per owner refinement 2026-02-XX · identity material via custody path per §4.1 §F at future slice (DQ-19 + DQ-20).
  - R-105 partial-retirement design: executed at 4k.
  - **R-106 CENSUS AUTONOMY SERVICE (verbatim 2026-02-XX)**: PHASE 3 SHAPE SUPERSESSION · census is a SELF-RUNNING SYSTEM CAPABILITY · not an agent-driven drill.
  - §6.8 "No GO exists": plan is authority · report-at-seal-boundaries · run continues in same breath · no "awaiting/holding" phrasing (per §6.8.6 · owner reinforced this-session).
- **Ratchet floor: `6086`** (was 6080 pre-4k · +6 measured: +4 new invariants + 2 absorbed retirements) · sha256 `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc`.

## 2 · STANDING (R-102 + R-103 + R-104 + R-105 + R-106 + §6.8)

- R-102: productized-or-honest-gap.
- R-103: single continuous run · no check-ins · additive-reversible forks → take own recommendation + annotate.
- R-104: named-but-unseated approving authorities for RMS + DIGICOW · custody-material via §4.1 §F.
- R-105: partial-retirement design executed at 4k.
- **R-106 CENSUS AUTONOMY SERVICE (NEW)**: PHASE 3 = supervisor-managed persistent census service · zero-agent-in-loop · 8 mandatory design goals ratified as PHASE 3 MUST-DOs.
- §6.8: plan is authority · report-and-continue · no "awaiting/holding" language.

## 3 · SIX STANDING BANS (UNCHANGED)

zero push/fetch · testing_agent BANNED · no refactor · no secret values · honest-gap never fake · no history rewrite.

## 4 · BOOT-ARTIFACT WARNING

CHUNK-1 is STALE bootstrap. Never re-run/re-clone/wipe. Probe list §5 authoritative. **Session-compaction cure**: read this file + run §5 probes + open the next unit's first action in the SAME turn per §6.8.6.

## 5 · 8 DISK PROBES

```bash
ls -la /app/assessment_workspace/ && ls -la /app/assessment_workspace/STATE/
cat /app/assessment_workspace/STATE/RESUME.md 2>/dev/null || echo "not created"
head -40 /app/assessment_workspace/STATE/STANDING_ORDERS.md
git -C /app/assessment_workspace log --oneline -12
git -C /app/assessment_workspace/repos/Extraction-Akki log --oneline -6 && git -C /app/assessment_workspace/repos/Extraction-Akki branch
git -C /app log --oneline -8
python3 -c "import json; d=json.load(open('/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json')); print(d['counts_at_baseline'])"
tail -80 /app/assessment_workspace/STATE/DECISIONS.md && cat /app/assessment_workspace/STATE/NEXT.md
```

Expected: probe-7 `{'failed': 3, 'passed': 6086, ...}` · v8-substitution nodeids retired · 3 mirror-drift baselines remain pending CP-APP-JS-UNIFY closure.

## 6 · POINTERS

- 37 React OS surfaces at `/app/frontend/src/pages/os/`.
- 11 React DAP surfaces at `/app/frontend/src/pages/dap/`.
- 6 backend modules under `repos/Extraction-Akki/backend/services/tenant_separation/`.
- 2 backend modules under `repos/Extraction-Akki/backend/services/baseline_retirement_supersede/` (4k).
- Test files: `test_cp_tenant_separation.py` (8 inv · 4j) · `test_r91_v8_substitution_retirement_guard.py` (4 inv · 4k).
- Schemas: `contracts/canonical_tenant_ids.schema.json` (4j).
- `phase0/drill_receipts_sub_slice_4j/` + `_4k/` — RED-pre + GREEN-post + sweepA + sweepB + close reports each.
- Custody: `custody/credentials/rms_connection_creds_v2.xlsx` (VIUSASA/weego · sha-pinned) + v1 (Huawei OBS + NAS).

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · APPROVING AUTHORITY · RMS** · named-but-unseated · custody-material pending R-104.
- **DQ-20** — **P1 · APPROVING AUTHORITY · DIGICOW** · named-but-unseated · custody-material pending R-104.
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k (v8-substitution leg); mirror-drift leg queued behind CP-APP-JS-UNIFY closure.
- DQ-14/DQ-15/DQ-16 (SKILLS-LAYER · DECK-ENGINE · STREAMING-EXTRACTION) — BUILD lane per R-102 · PHASE 4 (c/d/e).

## 8 · CAPABILITY GAINED THIS-SEAL

**CP-R91-RETIRE-SUPERSEDE partial**: 2 v8-substitution baselines retired via NEW additive superseding module `services.baseline_retirement_supersede.v8_substitution_retire` (SO §3.8 additive-only · SO §3.10-α closed-vocab). Sealed R-86 5-property carrier + R-88 total-coverage carrier preserved BY CONSTRUCTION (retired nodeids NOT in MIRROR_DRIFT_NODEIDS · retirement executed in both baseline_failures list + R-88 annotation field in same commit → no orphan annotation). 4 property tests + retirement attestation dict banking canon_ref + so_ref + sealed_carriers_left_unchanged + retirement_scope + property_4_preservation + reversibility. R-101 preserved WHAT retirement leg partially executed. **R-106 CENSUS AUTONOMY SERVICE banked** for PHASE 3 shape.

## 9 · PHASE 3 · CENSUS AUTONOMY SERVICE · 8 MANDATORY DESIGN GOALS (R-106 verbatim)

Per owner R-106 2026-02-XX verbatim:

1. **supervisor-managed persistent worker/scheduler** — `census_scheduler` supervisord program; survives agent absence + app restarts + pod restarts.
2. **scheduled runs**: weekly default per prototype "Next census: ... in 7 days" · per-tenant configurable · on-demand JWT-gated API trigger (Run census button).
3. **census engine productized**: port `estate_census v3` logic into `services/census_autonomy/*` additively (adapters over sealed data_source packages) · tenant-scoped from birth · LawfulBasisAdmit + all-reads-receipted + no-second-store service-path invariants · bounded/budgeted per run.
4. **mid-run decisions banked**: response-required queue surfaced via UI badge ("1 response required") · service CONTINUES on non-blocked lanes · NEVER stalls.
5. **results auto-flow**: receipts written + registry/census read surfaces updated + census listing status/coverage/condition · zero agent involvement.
6. **live progress observable**: running card + ETA + sources read · via polling or SSE from service state.
7. **degradation honesty**: unreachable surface → BLOCKED row · unreachable GPU host → deferred-not-failed · run always completes and reports.
8. **ops proof at PHASE 3 SEAL**: (a) kill backend + restart · scheduler resumes; (b) on-demand AKKI-TEST census completes end-to-end with agent watching only; (c) RED-first invariants for scheduler-existence + tenant-scoping + refusal-paths + no-agent-dependency.

<!-- STATE/RESUME.md · rewritten at Turn 4 sub-slice 4k SEAL close · 2026-02-XXT01:30:00Z END -->
