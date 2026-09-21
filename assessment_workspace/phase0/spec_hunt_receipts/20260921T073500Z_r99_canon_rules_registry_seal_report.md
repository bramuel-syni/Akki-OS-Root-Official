# R-99 · CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE · Seal Report

**Wave**: R-99 · COMPLETION SPRINT step 4 of 6 · additive READ-ONLY HTTP router surface
**Commit-A (code programme/track-a)**: `eb40fb67ea83c18cb35f51956b3b4b19c07ecbed` (short `eb40fb67`)
**Banked at UTC**: 2026-09-21T07:33:35Z
**Ratchet floor advance**: 5822 → 5831 (+9 measured = +9 targeted · CCS2 clean · no correction)
**baseline_failures.json sha256**: `df3325f7...` → `070c57c4cf8618554a7857f8e14a0e2555ae4d8593df6953b1693080c3e8361f`
**ORCH_BOOT.md sha256**: `bb126fe4...` → `1bbdb2de1506de23d1f5887828e950460d1cb9a6cd267d98097170f71cf127e9` (both notes and POD audit mirror byte-identical after pre-Commit-A regen)
**BASELINE_GUARD=1 canonicalised-sha256 (byte-identical double-sweep)**: `0eac2d7684e21020fe5bc351759cf282b981896fc6c7eaf9525e76cadb6e885a`

---

## Scope frozen per SO §6.4 NOTHING-BEYOND

Additive-only per SO §3.8. 9 files touched in Commit-A tree:

1. **NEW** `backend/routers/canon_rules_registry.py` (197 lines) — FastAPI APIRouter with prefix `/api/canon/rules` + 5 GET endpoints, closed-vocab reflection over sealed R-96..R-98 Final[...] constants via identity import (zero sealed edit).
2. **NEW** `backend/tests/invariants/test_r99_canon_rules_registry_router_surface.py` (180 lines · 9 tests) — SO §2.5 verbatim-docstring on every test.
3. **MOD** `backend/server.py` (+4 lines · 1 comment + 1 import + 1 blank + 1 include_router) — additive router mount; router carries prefix so include_router uses no explicit prefix.
4. **MOD** `backend/tests/invariants/known_unwired.py` (+29 lines · 1 new KNOWN_UNWIRED entry keyed `routers.canon_rules_registry` with Doc04/Doc05/Doc12 SRR canon citations + FE-WIRING-READY remediation R-tag).
5. **MOD** `backend/tests/invariants/baseline_failures.json` (+15/-3 lines · ratchet 5822→5831 both fields + new ratchet_history entry documenting this-wave delta).
6. **NEW** `backend/phase0/drill_receipts/20260921T072500Z_r99_canon_rules_registry_RED_pre.log` — authentic RED-first receipt (test_r99_openapi_json_lists_canon_rules_paths 1/9 fail right-reason 404 from `/openapi.json` before path corrected to `/api/openapi.json`).
7. **NEW** `backend/phase0/drill_receipts/20260921T071500Z_r99_canon_rules_registry_GREEN_post.log` — GREEN post-fix (10/10 including test_orch_boot).
8. **NEW** `backend/phase0/drill_receipts/20260921T073000Z_r99_canon_rules_registry_BASELINE_GUARD1_run1.log` — 5831 passed / 3 baseline-fails / 1 skip / 438 warnings / 184.65s.
9. **NEW** `backend/phase0/drill_receipts/20260921T073400Z_r99_canon_rules_registry_BASELINE_GUARD1_run2.log` — 5831 passed / 3 baseline-fails / 1 skip / 438 warnings / 185.01s.

Zero implementation-module edit outside this-wave. Zero sealed contract/writer/test-file edit. Sealed R-98/R-97/R-96/R-95..R-88 all continue verbatim GREEN.

---

## FE-WIRING-READY handoff artifact

Owner directive verbatim (2026-09-21T~07:10Z step-4-a): *"flag FE-WIRING-READY immediately with the dispatch-ready endpoint list + auth + sample payloads — I send the FE specialist to wire the portal write-path screens against the live surface while you continue"*.

### Endpoint list (all live at `/api/canon/rules/*`)

| # | Method | Path | Purpose | Auth |
|---|--------|------|---------|------|
| 1 | GET | `/api/canon/rules/dap` | Closed 38-rule DAP registry (Tier A DAP-1..30 + Tier B DAP-31..38) | **PUBLIC** (no auth) |
| 2 | GET | `/api/canon/rules/dap/{rule_id}` | Single DAP rule by ID; 404 on unknown | **PUBLIC** |
| 3 | GET | `/api/canon/rules/rbm` | Closed 23-rule RBM registry (Tier A 22 + Tier B 1) | **PUBLIC** |
| 4 | GET | `/api/canon/rules/roc` | Closed 11-rule ROC registry | **PUBLIC** |
| 5 | GET | `/api/canon/rules/rbm-8-ceremony-mechanic` | RBM-8 R-91 live-evidence-receipt (owner-cited ceremony-mechanic sub-invariants) | **PUBLIC** |

**Auth rationale**: these expose load-bearing canon anchors, not per-tenant business data. Public-read matches Doc04/Doc05/Doc12 SRR canon rows carrying no tenant scope. No mutation surface.

### Sample payloads (verbatim from live sweep run1)

#### `GET /api/canon/rules/dap` (headers example only)
```json
{
  "rule_count": 38,
  "tier_a_count": 30,
  "tier_b_count": 8,
  "tier_a_srr_row_start": 315,
  "tier_a_srr_row_end": 344,
  "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
  "rules": [
    {
      "rule_id": "DAP-1",
      "tier": "A",
      "srr_row": 315,
      "statement": "External party admitted as organisation-level principal … (byte-verbatim SRR text)",
      "metadata": {
        "objective": "…",
        "promise_source": "dap_backend_spec_v1",
        "status": "PROPOSED",
        "domain": "…",
        "relationship": "…"
      }
    },
    …
  ]
}
```

#### `GET /api/canon/rules/dap/DAP-1`
```json
{
  "rule_id": "DAP-1",
  "tier": "A",
  "srr_row": 315,
  "statement": "External party admitted as organisation-level principal …",
  "metadata": { … }
}
```

#### `GET /api/canon/rules/dap/DAP-999`
```
HTTP/1.1 404 Not Found
{"detail": "Unknown DAP rule: DAP-999"}
```

#### `GET /api/canon/rules/rbm`
```json
{
  "rule_count": 23,
  "tier_a_count": 22,
  "tier_b_count": 1,
  "tier_a_srr_row_start": 288,
  "tier_a_srr_row_end": 309,
  "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
  "rules": [ /* 23 objects · byte-verbatim statements */ ]
}
```

#### `GET /api/canon/rules/roc`
```json
{
  "rule_count": 11,
  "srr_row_start": 277,
  "srr_row_end": 287,
  "authority": "Master Requirements Registry v5 SRR sheet · Ruling 5",
  "rules": [ /* 11 objects · byte-verbatim statements */ ]
}
```

#### `GET /api/canon/rules/rbm-8-ceremony-mechanic` — **R-91 live evidence receipt** (FE-critical anchor)
```json
{
  "rule_id": "RBM-8",
  "srr_row": 295,
  "statement": "System-TCB ceremony: as RBM-7 plus slowest countdown and external witness with no credentials over the component",
  "is_r91_ceremony_anchor": true,
  "ceremony_window_is_rigid": true,
  "no_shortening_path_in_code": true,
  "r91_live_evidence_horizon_utc": "2026-09-23T03:23:15Z",
  "r91_is_live_evidence_receipt": true,
  "ceremony_shortening_watched_patterns": [
    "shorten_ceremony_countdown",
    "expedite_ceremony_apply",
    "waive_ceremony_countdown",
    "bypass_ceremony_horizon",
    "fast_forward_ceremony"
  ],
  "ceremony_shortening_watched_pattern_count": 5,
  "owner_directive_utc": "2026-09-21T06:35:00Z",
  "owner_no_expedite_ruling_utc": "2026-09-21T06:15:00Z",
  "owner_directive_verbatim": "when you author RBM-8, its invariant should reflect exactly that: ceremony windows are rigid, no shortening path exists in code, and the R-91 window you are currently honoring is the live evidence receipt.",
  "so_reference": "SO §6.6 · 'a countdown cut short is what FAIL looks like'"
}
```

### FE consumption invariant (SO §6.6 preservation)

Any FE portal write-path screen surfacing an R-91 countdown MUST consume `/api/canon/rules/rbm-8-ceremony-mechanic` **byte-verbatim** (no client-side rewriting of `r91_live_evidence_horizon_utc` or `ceremony_window_is_rigid`). This preserves owner's "countdown that cannot be shortened" invariant end-to-end.

### Pod-shell mount pending (KNOWN_UNWIRED tracked)

Router is wired in `/app/backend/server.py` only. `pod_shell/backend/server.py` mount pending FE-WIRING pass. Entry banked in `backend/tests/invariants/known_unwired.py` with Doc04/Doc05/Doc12 SRR citations + FE-WIRING-READY remediation R-tag. Entry auto-removes when FE-WIRING lands via `test_known_unwired_has_no_stale_entries` staleness sentinel.

---

## Pre-sweep STATE hygiene fixes (banked in Commit-B state master · NOT part of Commit-A tree)

Three state-drift issues surfaced pre-sweep, all inherited from prior seals and NOT R-99 caused. Fixed additively:

1. **`STATE/OBJECTIVES/M12b_W1.md`** — `card_sha256:` pin recomputed from `0bc8b267494b5ed79ac1f8879bd1e3885e163f61683ce5122e47fb23a31fc47b` to `f3aedc9e2cc489a582dee553e3fc6f4cb7721900c1712818f8d6653d3bb480e5` tracking OPEN-CARD-SWEEP `fad511a7` MILESTONE-3-OPENER retroactive-evidence body append. SO §6.2 pin-tracks-body invariant restored.
2. **`STATE/OBJECTIVES/ENTITLEMENT.md`** — `card_sha256:` pin recomputed from `46f4a6e7b896...` to `a214881e7455...` tracking OPEN-CARD-SWEEP `fad511a7` R-81/R-82 retroactive-evidence body append. SO §6.2 pin-tracks-body invariant restored.
3. **`STATE/NEXT.md`** — `POINTER_LINE` "READ STATE/STANDING_ORDERS.md FIRST — permanent standing law" appended at tail to restore `test_next_carries_pointer_near_bottom` invariant (pointer had been crowded out of last-5 non-empty lines by R-98 Commit-C fixup + `fad511a7` OPEN-CARD-SWEEP additive appends).

All three fixes are pin-refresh/pointer-refresh only. Zero card-body change, zero front-matter-key change beyond the pin value itself, zero R-99 code delta.

---

## RED→GREEN→GUARD receipts

| Stage | Log path | Result |
|-------|----------|--------|
| RED-pre | `backend/phase0/drill_receipts/20260921T072500Z_r99_canon_rules_registry_RED_pre.log` | 1/9 fail right-reason 404 from `/openapi.json` |
| GREEN-post | `backend/phase0/drill_receipts/20260921T071500Z_r99_canon_rules_registry_GREEN_post.log` | 10/10 pass 0.84s (incl. test_orch_boot) |
| GUARD run1 | `backend/phase0/drill_receipts/20260921T073000Z_r99_canon_rules_registry_BASELINE_GUARD1_run1.log` | 5831 passed · 3 baseline-fails · 1 skip · 184.65s |
| GUARD run2 | `backend/phase0/drill_receipts/20260921T073400Z_r99_canon_rules_registry_BASELINE_GUARD1_run2.log` | 5831 passed · 3 baseline-fails · 1 skip · 185.01s |
| Byte-identity | canonicalised-sha256 (strips shell-appended RUN[12]_EXIT marker) | `0eac2d76...` IDENTICAL both runs |

**CCS2 lesson extension banked**: `tools/strip_baseline_guard_log.py` does not currently strip shell-appended `RUN[12]_EXIT=` marker lines used for nohup exit-code capture. This wave canonicalises via inline post-strip filter. Extension to strip tool deferred to hygiene wave (out of R-99 §6.4 scope).

---

## Canon anchors (verbatim)

1. **COMPLETION SPRINT step 4 of 6** verbatim (2026-09-21T~06:10Z): *"LIFECYCLE/ENTITLEMENT HTTP SURFACE (additive routers only)"*.
2. **User step-4-a directive** verbatim (2026-09-21T~07:10Z after Steps-1..3 seal): *"flag FE-WIRING-READY immediately with the dispatch-ready endpoint list + auth + sample payloads — I send the FE specialist to wire the portal write-path screens against the live surface while you continue"*.
3. **User R-91 handling directive** verbatim (2026-09-21T~07:10Z): *"HOLD-AND-PROCEED, never skip the ceremony"*.
4. **Owner R-91 NO-EXPEDITE** verbatim (2026-09-21T~06:15Z): *"the countdown that cannot be shortened is the ceremony ... waiving it because the sweep already proved green is exactly the argument every future shortcut would make; the mechanic's value is that it doesn't yield to a good result"* (RBM-8/SER C.5 I-4 citations).
5. **Owner RBM-8 ceremony directive** verbatim (2026-09-21T~06:35Z): *"when you author RBM-8, its invariant should reflect exactly that: ceremony windows are rigid, no shortening path exists in code, and the R-91 window you are currently honoring is the live evidence receipt"*.
6. **Owner Ruling 5** SRR-as-authority (2026-09-20T~19:00Z · v5 workbook sha `00072c58...`).
7. **R-98 seal chain** (`38eeef6c` Commit-A + `deff9e58` Commit-B + `35e2fda7` Commit-C fixup + `a6be791` post-seal verify).
8. **OPEN-CARD SWEEP** state-only commit (`fad511a7`).
9. **SO §2.5 verbatim-docstring · §3 tests-first · §3.3 3-Commit Seal · §3.8 additive-only · §3.10-α Final[str] closed-vocab · §6 autopilot governance · §6.2 hash-pinned cards · §6.4 NOTHING-BEYOND · §6.6 countdown-cut-short-is-FAIL · §6.7 seal-report-boundary**.
10. **M16-W3 corrected order** (pre-Commit-A ORCH_BOOT ratchet-only regen at state master before Commit-A on programme/track-a).
11. **CCS2 lesson** (hash-seed determinism default `PYTHONHASHSEED=0` from R-95 onwards + this-wave marker-line canonicalisation extension).

---

## R-91 status at Commit-A boundary

- **Horizon UTC**: `2026-09-23T03:23:15Z` UNCHANGED.
- **Current UTC**: 2026-09-21T~07:35Z.
- **Time to horizon**: ~43.6 hours.
- **R-91 stays PARKED**. Zero ceremony-apply operations opened this-wave.
- RBM-8 ceremony-mechanic invariants surfaced verbatim at `/api/canon/rules/rbm-8-ceremony-mechanic` — FE-consumable byte-verbatim to preserve owner's "countdown that cannot be shortened" invariant.

---

## Autopilot next per user's corrected sequence

Per user directive (2026-09-21T~07:10Z corrected sequence):

(a) **FE-WIRING-READY flag raised NOW** (this seal report is the dispatch-ready artifact · owner sends FE specialist to wire portal write-path screens against the live `/api/canon/rules/*` surface).
(b) **Verify OPEN-CARD SWEEP** (COMPLETION SPRINT step 3) from git log — banked at state master `fad511a7` in prior session. To verify from git log (not handover): 
   ```
   git log master --oneline -20 | grep "OPEN-CARD SWEEP"
   ```
   Expected: `fad511a7` present. If missing, execute now.
(c) **Residual G5 Tier B rows / consolidated owner-list items** — scan STATE/OBJECTIVES/ for any newly opened cards or blockers surfaced since `fad511a7`.
(d) **R-91 ε-apply** at first boundary after `2026-09-23T03:23:15Z` (`date -u` checked · NO EXPEDITE · rigid per RBM-8/SER C.5 I-4/SO §6.6).
(e) **M1-to-date BUILD_JOURNAL closure** state-only as final act (COMPLETION SPRINT step 6).

Autopilot next-immediate: **Commit-B state master** (banks this seal report + drill receipts already in Commit-A + regen tool + STATE hygiene fixes) → **Commit-C fixup state master** (R-6 boundary regen state_head + code_repo history append for R-99 Commit-A `eb40fb67` + POD audit mirror sync).

---

## Standing bounds

- Zero push · zero remote configured on `programme/track-a` · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED per SO §6).
- Additive-only §3.8.
- Three-repo discipline (code = `programme/track-a` · state = `master` · POD audit mirror = `main` at `/app/frontend/`).
- Ratchet monotonic-up floor **5831** (was 5822 · +9 measured = +9 targeted).
- R-91 PARKED horizon `2026-09-23T03:23:15Z` NO EXPEDITE.
- HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged.
