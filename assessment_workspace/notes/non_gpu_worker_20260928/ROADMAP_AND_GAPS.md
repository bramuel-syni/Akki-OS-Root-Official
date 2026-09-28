# Akki — non-GPU worker delivered + named-gap roadmap to completion

**Date:** 2026-09-28 · **Owner ask:** "build a non-GPU worker (operates like the
GPU worker)… can you read the estate… give me the plan with named gaps, how each
gap contributes to the remaining % to completion, and a clear roadmap of what we
have done and what is left."

---

## 1. What shipped this session (verified, unmocked)

**A real non-GPU worker now exists and it read your estate.** It mirrors the GPU
worker exactly: same aggregate-only census contract, same custody model, runs as
a *separate process* so the API pod is never the data path.

- `services/census_autonomy/non_gpu_census_worker.py` — the worker (runs as a
  bounded subprocess; local counterpart of `remote_worker.py`).
- `services/census_autonomy/estate_connector_registry.py` — authorised credential
  resolver; builds 0600 connector custody from the registered estate.
- `services/census_autonomy/non_gpu_dispatch.py` — dispatch authority (local
  counterpart of `remote_dispatch.py`); selected via
  `AKKI_CENSUS_EXECUTION_MODE=non_gpu_worker`.

**Genuine estate read (RMS tenant, source `rms_mysql`), counts only — no rows/PII:**

| Connected host | Result | databases | tables | rows (est.) |
|---|---|---|---|---|
| Razuna / Newsvault (`…173.58`) | **READ** | 2 (`news_vault`, `razuna`) | 119 | 2,198,643 |
| 6 other RMS MySQL hosts | not-yet-connected ("NOT YET UHURU") / IP-restricted | — | — | — |

- End-to-end via HTTP: `POST /api/portal/census/run` → COMPLETE, tenant-scoped to
  RMS, `execution_verified=true`, signed proof receipt on disk.
- Cross-tenant isolation proven (RMS run invisible to a DIGICOW principal).
- **723 backend tests pass** (710 existing + 13 new non-GPU worker tests), 17 gated
  skips, 0 failures.

**Honest limits:**
- Only the currently-connected RMS host returns data. The other 6 hosts are
  reachable-but-not-ready or firewalled to our egress — the worker isolates each
  one, so a partial estate never blocks the read.
- **DigiCow is blocked on a real credential, not on code.** The workbook you sent
  contains only ARNs (region, cluster ARN, secret ARN, db names) — these are
  *identifiers*, not an AWS key. To read DigiCow we need either AWS access
  credentials with `secretsmanager:GetSecretValue` on
  `arn:aws:secretsmanager:eu-west-1:…:secret:rds/data/api/user/secrets-8rZuVc`, or
  the resolved RDS endpoint + username + password. The resolver refuses cleanly
  (`NATIVE_SECRET_RESOLVER_UNAVAILABLE`) until that arrives.
- RMS object archive (OBS) and NAS/broadcast archive need OBS/CIFS drivers — next
  build slices, same worker pattern.

---

## 2. How "% complete" is measured (transparent model)

- **Denominator:** the **648 assessed requirement rows** across **56 spec
  families** (Sept-26 gap analysis). This is the real requirement surface.
- **Two axes** (both matter, they are different questions):
  1. **Architecture axis** — is the governed behaviour built in code?
     Weights: PARTIAL 0.55, EVIDENCED_SCOPED 0.75, UNVERIFIED 0.25,
     SOURCE_UNRESOLVED / SPEC_DECISION_REQUIRED 0.0, EXPLICIT_NONCLAIM 1.0.
  2. **Live-verified axis** — is it proven against real estates/models (not
     synthetic fixtures)?
- **Architecture completion ≈ 47%.** **Live-verified completion was ≈ 0–2%**
  before this session because every positive provider/source result was
  SYNTHETIC/MOCKED. **This session lands the first genuine live evidence** (Area A
  ingestion), so the live axis is now off zero and Area A is the proven beachhead.

> The previous "% not established" answer was because the whole platform hinged on
> a runtime that did not exist. That runtime now exists — so the roadmap below is
> concrete, not deferred.

---

## 3. Named gaps by capability area (grounded in the 648 rows)

`share of remaining` = each area's contribution to the work still outstanding.

| # | Capability area | Rows | Architecture % | Share of remaining | Live-verified? |
|---|---|---|---|---|---|
| **A** | Ingestion, Connection & Census (source→registry) | 93 | 51% | **13%** | **STARTED — RMS MySQL live** |
| **B** | Core Promise & Adaptive Certainty | 92 | 38% | 17% | No (mocked) |
| **C** | Execution, Context & Model Quality | 63 | 37% | 12% | No (mocked) |
| **D** | Memory, Learning & Watch | 30 | 56% | 4% | No (mocked) |
| **E** | Governance, Security & Containment | 116 | 54% | 15% | Static only |
| **F** | Entitlements & Commercial | 58 | 55% | 8% | No (ledger fixtures) |
| **G** | Rules, Amendments & Decision Engines | 149 | 42% | **25%** | Static + 24 source-unresolved |
| **H** | Principals, Tenancy & Continuity | 47 | 52% | 7% | Partial |

**Biggest levers:** Area **G** (25% — largest surface, incl. 24 rows blocked on
unrecovered source specs + 5 spec-decisions) and Area **B** (17% — 52 rows only
claimed, not even statically confirmed).

### Area A named gaps (the one we just moved — finish it first)
- **A-1 DONE:** RMS MySQL census — connected host read live, tenant-scoped. ✅
- **A-2:** Connect the remaining 6 RMS MySQL hosts as they come "UHURU" (config
  only — worker already handles them).
- **A-3:** RMS OBS (object archive) driver — needs Huawei OBS list capability.
- **A-4:** RMS NAS / broadcast archive driver — needs CIFS/SMB walk capability.
- **A-5:** DigiCow RDS census — **blocked on AWS credential** (secret ARN resolution).
- **A-6:** content_registry + data_cleanliness live producers over real census
  output (currently PARTIAL/UNVERIFIED, mocked).

---

## 4. Roadmap (dependency-ordered)

**P0 — finish the live ingestion beachhead (Area A):**
1. Connect remaining RMS MySQL hosts (A-2) — pure config as owner opens them.
2. Resolve DigiCow (A-5) — needs AWS creds OR resolved endpoint/user/pass.
3. Add OBS + NAS drivers (A-3, A-4) — same worker pattern, new source drivers.
4. Wire real DQ/cleanliness + content-registry producers off live census (A-6).

**P1 — convert built-but-mocked control planes to live-verified:**
5. Area C execution/context/model-quality proofs against a real model runtime.
6. Area F entitlement/commercial producers off live usage (not ledger fixtures).
7. Area E security/containment runtime qualification (currently static-only).

**P2 — reconcile the long tail:**
8. Area G: recover the 24 SOURCE_UNRESOLVED rows (SV extension, ROC spec, Deck
   Engine) — **needs owner source docs**; resolve the 5 SPEC_DECISION rows.
9. Areas B/D/H remaining PARTIAL/UNVERIFIED rows to live evidence.

**Blocked on owner (not code):**
- DigiCow AWS credential (A-5).
- 24 source-unresolved requirement specs in Area G.
- 7 spec-decision rows (measurement thresholds must be set *before* observation).

---

## 5. Repository / additional data estates

The worker's connector registry is source-driver extensible: each new estate the
owner shares is added as a `source_id → driver` binding + a custody resolver, with
no change to the worker, the census contract, the ledger, or the UI. Ready to
receive the additional data repository referenced by the owner.
