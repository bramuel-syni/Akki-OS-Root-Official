# CP-PROD-DEPLOY-SELF-CONTAINMENT · Seal Report

**Seal report · 2026-09-21T12:15:00Z · autopilot**

**Wave**: CP-PROD-DEPLOY-SELF-CONTAINMENT · production K8s deployment fix.
**Root cause line**: Kubernetes production image packages only `/app/backend` + `/app/frontend`; the sealed backend at `/app/assessment_workspace/repos/Extraction-Akki/backend/` is absent in the container, so `/app/backend/server.py`'s `sys.path.insert(0, str(SPINE_BACKEND))` is a no-op and line 26 `from routers import connect_gpu` raises `ModuleNotFoundError: No module named 'routers'` — the pod crash-loops at import.

## Owner authorization

Owner explicitly ordered this wave *during the R-91 hold*, verbatim (2026-09-21T~11:45Z):

> "NEW OWNER-PRIORITY WAVE — PRODUCTION DEPLOYMENT FIX. ... This work is authorized NOW during the R-91 hold (the hold bars the ε-apply, not owner-ordered work). R-91 still applies only at the horizon."

## R-100-UNWIND precedence

The pending §3.8 UNWIND (self-reported lapse cured) landed **before** this wave at code `42a0d3a04f13486b8929a59f8fd98d7f5a36d226` / state Commit-B `bf272c7ebe1c19545c9900fae8d41ff4d948bb53` / state Commit-C `7d7aec5a191f77bd159378d3be0a8c81f8861625` (2026-09-21T11:30–11:47Z). The vendored image built by this-wave therefore includes the wrapper shape (`services/enforce/principal_context_adapter.py` with `@contextlib.contextmanager` owning the with-block protocol) and the byte-restored sealed carrier (`services/request_context/context.py` sha256 `ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb`) — production ships the wrapper shape, not the lapsed in-place edit.

## Fix landed

**Code programme/track-a Commit-A `283524d8`**:
- NEW `backend/tests/invariants/test_vendored_tree_mirrors_spine.py` mirror-invariant test.
- `pod_shell/backend/server.py` mirror sync of the two-path edit.
- `backend/tests/invariants/baseline_failures.json` ratchet `5857 → 5858` (+1 MEASURED).

**Production-image /app main commit `25790c2c`** (companion, three-repo discipline):
- `backend/server.py` two-path spine bridge + Tigris env-discipline warning.
- `backend/requirements.txt` closure updates: `httpx`, `openpyxl`, `Pillow`.
- `backend/vendored/extraction_akki/backend/**` 999-file byte-identical mirror.
- `backend/vendored/extraction_akki/MANIFEST.json` per-file sha256 + `structural_sha256 379318b9…`.

**State master Commit-B this-seal** (banks A + companion + tools + this report):
- NEW `tools/prod_vendor_sync.py` deterministic sync tool.
- NEW `tools/cp_prod_deploy_pre_commit_a_ratchet_and_orch_boot_regen.py`.
- `notes/ORCH_BOOT.md` ratchet-only regen.
- `STATE/DECISIONS.md` this-wave append (root-cause line + cure + evidence + standing lesson).
- This report.

## Evidence

**Production simulation (`AKKI_FORCE_VENDORED=1`)** at `backend/phase0/drill_receipts/20260921T115632Z_cp_prod_deploy_production_simulation_curl_matrix.log`:

- `[spine-bridge] resolved backend source: vendored-production at /app/backend/vendored/extraction_akki/backend`
- `openapi -> 200`
- 5 R-99 canon-rules public 200 (dap, dap/DAP-1, rbm, roc, rbm-8-ceremony-mechanic).
- 9 R-100 portal with seeded JWT: `GET /requests 200`, `GET /requests/req-x 404`, `POST /requests 202`, `POST /requests/req-x/stop 200`, `POST /requests/req-x/retry 200`, `GET /entitlement/licence 200`, `GET /entitlement/catalog/listed 200`, `GET /entitlement/allowance 200`, `GET /entitlement/badges 200`.
- 4 R-100 portal without JWT: all `401`.
- Zero 500 anywhere. Sealed spine tree absent from `sys.path` proves self-containment.

**Sandbox restore verification**: supervisor log `[spine-bridge] resolved backend source: sandbox-spine at /app/assessment_workspace/repos/Extraction-Akki/backend` + preview URL openapi 200.

**Deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep** stripped-sha256 `23caeeb5ff3f71f6f5a3eeec8d117e0413d82c39fb03ad5918c05fc31853581a` IDENTICAL:
- Run 1: `20260921T121132Z_cp_prod_deploy_baseline_guard_run1v3.log` — 5858 passed · 181.00s.
- Run 2: `20260921T121507Z_cp_prod_deploy_baseline_guard_run2.log` — 5858 passed · 181.04s.
- Both with 3 R-91-pending baseline-fails · 1 skip · 438 warnings against post-bump `baseline_failures.json sha256 5266564f…`.

**RED-first drill** (drift injection on `config/__init__.py`):
- RED: `20260921T115554Z_cp_prod_deploy_mirror_invariant_RED_pre.log` — 1/1 fail right-reason (1 file byte-diverged).
- GREEN: `20260921T115556Z_cp_prod_deploy_mirror_invariant_GREEN_post.log` — 1/1 pass 0.84s post-restore.

## Runtime file-reads audit

- 120 `/app/assessment_workspace/*` references in the vendored tree — all `_DEFAULT_*` module-level string constants overridable via env, OR gracefully handled at request time (empty return / `FileNotFoundError` handled).
- Zero hardcoded writes outside `/app/backend` at runtime (grep confirmed).
- Core 14 endpoints (5 R-99 canon-rules + 9 R-100 portal) never touch `/app/assessment_workspace/*` at request time — confirmed by prod-sim.

## Env discipline

- `MONGO_URL` + `DB_NAME`: env-only, fails loud with `KeyError` at import if missing.
- Tigris (S3): env-preferred, WARN log line at import if `_is_production_env` (workspace absent) and TIGRIS_* env unset — no silent misconfig.
- CORS_ORIGINS: env-preferred, `*` default retained (compat).
- Frontend: `REACT_APP_BACKEND_URL` env-only consumption verified.

## Standing lesson banked

**Environment-differential deployment failures are structurally preventable via the vendored-mirror + two-path bridge pattern.** When two environments differ in what they package (sandbox has workspace + backend; production has backend only), the bridge must resolve at `__file__`-relative path, not cwd, and MUST have a per-environment fallback. The mirror invariant test then makes drift between "sealed source" and "shipped copy" structurally detectable BEFORE an image is built.

## R-91 posture unchanged

R-91 CP-APP-JS-UNIFY Phase 2 remains PARKED at frozen horizon `2026-09-23T03:23:15Z` (~**39.1h** out · `date -u` = 2026-09-21T12:15Z). **NO EXPEDITE.**

## Standing bounds

zero push · zero remote configured · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo discipline · ratchet floor **5858** · CONTINUITY BUNDLE at every seal (this-CP appends new bundle-set block at Commit-C) · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · **structural §3.8 guard on `services/request_context/context.py` sha-pin `ad0d9439…`** · **new mirror-invariant guard on `/app/backend/vendored/extraction_akki/backend/`**.
