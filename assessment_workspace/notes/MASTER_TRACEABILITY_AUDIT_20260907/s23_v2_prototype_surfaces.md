# S23 · v2 Standalone Prototype · 47 Surfaces · Detail Classification

**Source:** `notes/SURFACE_AUDIT_v2_prototype_20260907.md` (banked 2026-09-06T20:15Z) · v2 HTML at `canon/prototypes/20260907_v2_standalone/RMS_AI_Prototype_v2_Standalone.html` (sha256 `4199c49f2e1b3fd633683205b5274d0afaba98757a3ccb4df6f1ee9e459a71f9`, 1,954,907 bytes, decoded app payload 1,776,832 bytes).

**Delta vs v8:** +666,878 bytes app payload · +1,668 interpolation slots (v2 has 4,769 · v8 has 3,101) · framework bundles byte-identical.

**Total surfaces: 47** (29 Registry + 18 non-Registry). Detail rows imported from SURFACE_AUDIT_v2 §2.1 and §2.2 verbatim; classification harmonised with master audit §C.3 grades.

## §A · Registry surfaces (29 rows) · owner-priority W-REGISTRY-FULL-BUILD

**Legend:** LIVE-DATA = portal renders + at least one `/api/*` substitution fires · PROTOTYPE-SAMPLE = portal renders v8 sample text, no substitution · NOT-WIRED = surface in v2 not in v8 or v8 present but never routed. Classification uses the master audit grades.

### A.1 · Data Connected (9 rows)

| Row | Surface | v2 state | Classification | Wave / Route |
|---|---|---|---|---|
| R.0 | Registry entry page (tabs, tile grid, topline) | LIVE-DATA | DONE (portal iframe wired; substitutions bind to /api/registry/facts) | Re-anchor against v2 rendered DOM |
| R.1 | Data Connected header (census-first framing) | LIVE-DATA | PARTIAL (needs `census-id` + `census-operator` in `/api/registry/facts` payload) | Extend endpoint |
| R.2 | Reading the mix · 6-way cut | PROTOTYPE-SAMPLE | REUSE (census_engine service exists) | New route `/api/registry/mix` |
| R.3 | Sources list grouped by data-kind | PROTOTYPE-SAMPLE | PARTIAL (sources array exists; grouping NEW) | Backend grouping OR frontend grouping |
| R.4 | Source Profile drill-in (15+ efProfileVM fields) | NOT-WIRED | NEW | New route `/api/registry/source/{source_id}/profile` (depends on perception service mount) |
| R.5 | Confidential Information Register (NEW surface) | NOT-WIRED | NEW | New route `/api/registry/cir` |
| R.6 | Census intelligence panel · right rail | PROTOTYPE-SAMPLE | PARTIAL (census route exists; narrative slots NEW) | Extend `/api/census/latest` |
| R.7 | Past censuses drill-in | NOT-WIRED | NEW | New route `/api/census/history` + `/api/census/{id}/transcript` |
| R.8 | Methodology page ("How the estate is measured") | NOT-WIRED | NEW (frontend-only static explainer) | No backend |
| R.9 | Estate intelligence right-rail | PROTOTYPE-SAMPLE | PARTIAL | Extend `/api/registry/facts` |

### A.2 · Compute Connected (7 rows)

| Row | Surface | v2 state | Classification | Wave / Route |
|---|---|---|---|---|
| R.10 | Compute Connected header topline | LIVE-DATA | DONE (existing substitution) | Re-anchor against v2 |
| R.11 | Per-GPU-card enumeration (4 cards) | LIVE-DATA (partial) | PARTIAL (state labels are prototype text; needs `state`, `slot_id`, `mem`, `util`) | Extend `/api/compute/estate` |
| R.12 | Usage pattern & budget · spend line | NOT-WIRED | NEW | New route `/api/compute/spend` (reads cost_ledger service, which IS mounted) |
| R.13 | Consumption per workload | NOT-WIRED | NEW | New route `/api/compute/workloads` |
| R.14 | Reading the traffic · calls & spend | NOT-WIRED | NEW | New route `/api/compute/traffic` |
| R.15 | Per-machine drill-in | PROTOTYPE-SAMPLE | PARTIAL (POST endpoints exist; read-only page NEW) | New route `/api/compute/machine/{machine_id}` |
| R.16 | Compute intelligence right-rail | NOT-WIRED | NEW | Add narrative field to `/api/compute/estate` |

### A.3 · LLMs & Trained Models (13 rows)

| Row | Surface | v2 state | Classification | Wave / Route |
|---|---|---|---|---|
| R.17 | LLMs & Trained Models header | LIVE-DATA (partial) | PARTIAL (4 MOAC services live) | Join model_registry to cost_ledger |
| R.18 | Model roster (grid) | PROTOTYPE-SAMPLE | PARTIAL | Extend model_registry payload |
| R.19 | "Models — the full record" drill-in | NOT-WIRED | NEW | New route `/api/model_registry/full_record` |
| R.20 | How this model answers (memory vs worked-out-fresh) | NOT-WIRED | NEW | New route `/api/model_registry/{model_id}/answering` |
| R.21 | The six checks (0.85/0.80/0.05/0.10/0.75/95%) | LIVE-DATA (partial) | PARTIAL | New route `/api/model_registry/{model_id}/checks` |
| R.22 | Refusals with reason enumeration | LIVE-DATA (partial) | PARTIAL | New route `/api/model_registry/{model_id}/refusals` |
| R.23 | Why models refuse (concept explainer) | NOT-WIRED | NEW (static explainer) | No backend |
| R.24 | Model journal (per-model, 15+ tm* fields) | NOT-WIRED | NEW | New route `/api/model_registry/{model_id}/journal` |
| R.25 | Traffic breakdown (per-model) | NOT-WIRED | NEW | New route `/api/model_registry/{model_id}/traffic` |
| R.26 | Model intelligence right-rail | NOT-WIRED | NEW | Add narrative field to model_registry payload |
| R.27 | Opportunities (per-source in Registry context) | NOT-WIRED | REUSE (opportunity_briefs service exists at 1,412 LOC · UNMOUNTED) | Mount router `/api/opportunity_briefs/*` |
| R.28 | Preview outcomes modal | NOT-WIRED | NEW (frontend-only unless "preview" needs a projection route) | Optionally new route `/api/governance/preview` |

## §B · Non-Registry surfaces (18 rows)

| Row | Surface | v2 state | Classification | Wave / Route |
|---|---|---|---|---|
| L.1 | Landing greeting (rolePerson, roleDept, roleInitials) | PROTOTYPE-SAMPLE | PARTIAL | Bind to `services/auth/` (LIVE-mounted 1,714 LOC) |
| C.1 | Chat "Ask & Remember" | LIVE-DATA | DONE | Existing routes cover; re-anchor |
| W.1 | Watch surface | LIVE-DATA | DONE (Watch + Grey Mirror mounted) | Existing routes cover |
| L.2 | Ledger (Audit Trail) | LIVE-DATA | DONE | Existing route covers |
| G.1 | Rule Book Library shelf | PROTOTYPE-SAMPLE | PARTIAL (governance service mounted, shelf endpoint thin) | New route `/api/governance/rulebooks` |
| G.2 | Rule Book full detail (per-rule profile) | LIVE-DATA (partial) | PARTIAL | Extend `/api/governance/rulebook/{id}` |
| G.3 | Rulebook shelf intelligence right-rail | NOT-WIRED | NEW | New route `/api/governance/shelf_intelligence` |
| Q.1 | Rules Updates (signing queue) | NOT-WIRED | NEW | New route `/api/governance/rules_updates` + `POST .../{id}/sign` |
| Q.2 | Approval history | NOT-WIRED | NEW | New route `/api/governance/approvals` |
| WF.1 | Workflow list | PROTOTYPE-SAMPLE | PARTIAL | New route `/api/workflows` |
| WF.2 | Workflow detail (18 wfDetailVM fields) | NOT-WIRED | NEW | New route `/api/workflows/{workflow_id}` (large cross-service join) |
| WF.3 | Begin Training flow | PROTOTYPE-SAMPLE | PARTIAL (training_router LIVE-mounted at 1,568 LOC) | Wire begin-training flow |
| O.1 | Opportunities standing across estate | NOT-WIRED | REUSE (opportunity_briefs UNMOUNTED) | Mount + new route `/api/opportunities` |
| O.2 | Opportunity → workflow link | NOT-WIRED | NEW (cross-link only) | No new route beyond O.1+WF.2 |
| M.1 | Master version history (17 mrDetailVM fields) | NOT-WIRED | NEW | New route `/api/master_version_history` (baseline_line + model_registry + audit_trail join) |
| D.1 | Documents surface (implicit) | PROTOTYPE-SAMPLE | PARTIAL (whitepapers + wpw services mounted) | Bind to existing endpoints |
| X.1 | Chat archive | PROTOTYPE-SAMPLE | PARTIAL | Chat service extension |
| X.2 | Access-restricted screen | NOT-WIRED | NEW (frontend-only, static) | No backend |

## §C · S23 rollup

| Bucket | Registry | Non-Registry | Total | % of 47 |
|---|--:|--:|--:|---:|
| DONE | 2 | 4 | **6** | 12.8% |
| PARTIAL | 8 | 6 | **14** | 29.8% |
| REUSE | 1 | 1 | **2** | 4.3% |
| NEW | 18 | 7 | **25** | 53.2% |

**Master file §C.3 shows S23 as DONE 8 · PARTIAL 9 · REUSE 3 · NEW 27** — the small delta is that master audit counts some PARTIAL rows as DONE where the substitution binds a real route, even if a field is missing. This detail file is stricter; owner may pick the boundary.

## §D · v2-specific findings from SURFACE_AUDIT_v2

- **25 of 47 surfaces (53%) are NOT-WIRED to any backend today.** 68% of that gap sits inside Registry (17 of 25).
- **25 new backend routes required** for full v2 coverage.
- **2 existing but unmounted services** need mounting for v2 to work: `services/opportunity_briefs/` and `services/perception/` (2,158 LOC).
- **Rendered-DOM law risk:** 17 Registry NOT-WIRED surfaces = 17 substitution-rule authorships against v2's rendered DOM. Each rule that matches nothing = RED. Real-Chromium harness must re-run against v2 to enumerate anchor selectors before rules are authored.
- **Retired from v8 (not carried forward in v2):** "Buy Data" catalog · "Ask The Indices" · farmer-benchmark demo (How I compare · Free · Opt-in) · "Deployed — open directly" app-catalog · "Coast region — outside your licensed coverage — Ask for a quote" · "Six acceptance checks" as top-level nav · "FI Farma IQ" brand.
- **New concepts introduced in v2:** Confidential Information Register · Rules Updates (signing queue) · Preview outcomes modal · per-machine drill-in · budget/spend split · Consumption per workload · full model journal + thread · master version history · Estate intelligence right-rail (per-tab narrative).

## §E · Wave charter cross-reference

Per master §E.1:
- **W-REGISTRY-FULL-BUILD** covers rows R.0..R.28 (29 rows) — priority per owner ruling 2026-09-06T19:20Z.
- **W-DATA-SUITE-v2-LIFT** covers R.5 CIR + Q.1 Rules Updates + Q.2 Approval history (S effort).
- **W-EXECUTIVE-SUITE-v2-LIFT** covers Board 360 · Exco 360 · Documents · Rule Books · Collab · Spend · Task Manager (L effort · shared with executive-donor lifts).
- **W-TRUST-SURFACE-v2** covers L.2 · X.1 · X.2 refinements (S effort).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
