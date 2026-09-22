# OBJECTIVE · CENSUS PRODUCTIZATION

**Objective ID:** CENSUS-PRODUCTIZATION
**Milestone status:** DRAFTED · pinned pre-first-RED
**Opened at:** 2026-09-22T06:15:23Z (banked at R-101 supersede banking · state master notes-only)
**Sequence gate:** opens **post-CP-TENANT-SEPARATION** (user-run censuses must be tenant-scoped from birth)
**Authored by:** main-agent desk in response to owner question this-session (verbatim below); owner correction awaited at R-101 ε-apply seal report.

## Owner question verbatim (2026-09-22T~06:12Z)

> "the census wizard will do what you/E1 are doing for Akki now, for when the user is using the system?"

## Desk gap read (honest answer · owner to confirm or correct at R-101 ε-apply seal report)

**NO — not yet fully.**

### What EXISTS today

| Layer | Artifact | Sha / anchor |
|---|---|---|
| Operator-run census tools | `phase0/tools/estate_census_v{1,2,3}.py` invocations (main-agent terminal-runs) | receipts at `phase0/census_v3/*.json` |
| Census receipts + read endpoints | `/api/portal/census/records` LIST + `.../{census_number}` DETAIL | CENSUS-SURFACE-A Commit-A' journey extension · code sha `e06ecf9` |
| Broader read surface | `/api/portal/census/{assets,surfaces,access,latest,duplication}` | CENSUS-SURFACE-A Commit-A · code sha `4dfc446` |
| Designed-not-shipped UI | `portal_census_journey_ui_spec.md` + `portal_registry_landing_ui_spec.md` | `phase0/surface_connection/` (banked pending ε-apply) |

### What does NOT exist

- **User-triggered in-product census execution** — the "Run census" button driving the real pipeline end-to-end for the user:
  - Connect-source registration (per-tenant lawful-basis admit filed, per-tenant credentials in-memory read).
  - Census run with **live progress** (real-time streaming from the census engine to the UI over WS/SSE).
  - Mid-run agent questions surfacing as **response-required** in the UI (agent-to-user callback loop when the census engine hits an ambiguous surface / undeclared feed / policy question).
  - Results write **into the registry** through the SEALED writer (per-tenant asset registry write · Canon-9 §3 single-writer discipline preserved).
  - **Per-tenant scoping** across every read + write + budget + surface.
  - **GPU-spend capture** at census-run granularity (hours × utilization × cost per host) surfaced back to the user's registry landing GPU Spend tab.

## R-101 ε-apply landing rule (interim)

In the R-101 ε-apply UI, the Run-census control ships wired to **whatever is REAL at ship time**:

- **If a bounded real census run is feasible** at ship time (e.g., a single-surface tenant-scoped shell that re-runs an existing census with a real progress signal) → wire it live.
- **Otherwise** → honest-gap pattern (control renders visibly, tooltip explains "*Coming with CP-TENANT-SEPARATION + CENSUS-PRODUCTIZATION; live audit surface at /api/portal/census/records*"). **No simulated progress. No fake state.**

## Exit criteria (for CENSUS-PRODUCTIZATION seal)

1. `/api/portal/census/run` (or equivalent write-surface endpoint) accepts per-tenant JWT + connect-source descriptor + lawful-basis admit reference → returns census_run_id + WS/SSE URL for live progress.
2. UI "Run census" control drives the endpoint end-to-end for a signed-in tenant user.
3. Live-progress channel emits at least: `enumerating`, `authing`, `reading`, `writing_registry`, `blocked_awaiting_response`, `complete` states with per-surface progress deltas.
4. Mid-run agent question flow: when engine emits `blocked_awaiting_response` with question payload, UI surfaces the question in a *response-required* modal; user answer routes back to engine.
5. Registry writes go through the SEALED asset_registry_writer per Canon-9 §3 (grep-negative scan on any hydrator public surface stays clean).
6. GPU-spend capture: engine records `gpu_seconds_used`, `gpu_utilization_avg`, `gpu_cost_estimate` per run; surfaces on `records/{census_number}` DETAIL → GPU Spend tab.
7. Per-tenant scoping enforced at every read + write + budget-guard step (CP-TENANT-SEPARATION invariants gate this — hence sequence-post).
8. RED-first invariants: no user-scope leakage across tenants · no simulated progress · no registry writes bypassing sealed writer · no GPU-spend fabrication · lawful-basis admit filed pre-first-byte.
9. §3.3 3-Commit Seal with double-green byte-identical sweep at floor bumped to reflect net-new invariants.

## Anti-patterns explicitly forbidden

- **NO simulated progress bars.** If the engine cannot emit real state, the UI shows honest-gap copy, not fake motion.
- **NO cross-tenant read/write leakage.** Every projection filters through per-tenant scope.
- **NO writer duplication.** All registry writes go through sealed `mtafiti.asset_registry_writer` (Canon-9 §3).
- **NO GPU-spend fabrication.** Numbers come from live host telemetry (akki-vm / akki-vm-ii nvidia-smi captures at run time) or the run is banked without a GPU-spend claim.
- **NO §3.8 sealed-file edits** to census_engine, asset_registry_writer, census_canon.registry_write, or any other sealed writer. Adapter-layer additions only.

## Canon anchors verbatim (at drafting)

- Owner question this-session (2026-09-22T~06:12Z · verbatim above).
- Canon-9 §3 single-writer.
- Canon-4 §4 objective-blind census walk.
- Canon-4 §8 one-record-per-source.
- Canon-9 §13 Mkondo Charter (Census and registry records | Mtafiti | Both authorities; every surface by proof link).
- Owner CONNECT-don't-duplicate ruling (2026-09-22T~02:20Z at CENSUS-SURFACE-A Commit-A).
- Owner "prototype wins" ruling (Front-End Integration Brief at `custody/owner_drops/20260920T0824Z/`).
- CENSUS-SURFACE-A Commit-A + Commit-A' code sha chain (`4dfc446` + `e06ecf9`).
- CP_APP_JS_UNIFY closure card (`STATE/OBJECTIVES/CP_APP_JS_UNIFY.md`) — R-101 ε-apply lands the Run-census control shell inside App.js.
- TENANT_SEPARATION objective card (`STATE/OBJECTIVES/TENANT_SEPARATION.md`) — REQUIRED-PRECEDES this objective.

## Autopilot posture

- Pinned pre-first-RED per owner Part-2 order precedent (TENANT_SEPARATION discipline).
- Sequenced post-CP-TENANT-SEPARATION seal.
- R-101 ε-apply Run-census control ships as honest-gap or bounded-real per shipping-layer feasibility — no fabrication.
- Owner correction on desk gap read awaited at R-101 ε-apply seal report.

## Stop-conditions

Stop-conditions #1/#2/#3 NOT applicable at drafting (state-only card open). Will apply at first RED-first commit-A on this objective post-tenant-separation seal.
