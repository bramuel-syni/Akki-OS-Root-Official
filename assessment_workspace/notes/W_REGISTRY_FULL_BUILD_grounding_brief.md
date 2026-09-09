# W_REGISTRY_FULL_BUILD_grounding_brief.md

**Wave:** `W-REGISTRY-FULL-BUILD`
**Charter date:** 2026-09-09
**Owner ruling authorising the wave:** DECISIONS.md 2026-09-08T~06:15Z (STEP 5) + 2026-09-09T~11:40Z (proceed straight through)
**Ratchet floor at open:** 3040 (harness receipt fresh, 37 rules bound, 0 orphans)
**Predecessor closes:** W-TRACKING-DEFECT-FIX (`7f3c8cc`) · W-INGEST-AC-SPEC + W-RULING-LEDGER-STEP3 (`a5324dd`) · W-AUDIT-REBUILD-STEP4 (state mirror `4d4da670`)

---

## §A · Owner ruling (verbatim, from DECISIONS.md 2026-09-08T~06:15Z)

> STEP 5 — THEN FIRE W-REGISTRY-FULL-BUILD. Standing ruling ("Priority building goes to registry. I need registry fully build") remains. Defaults stand: prototype v3 = binding design, Doc 0 v2 = binding. Build per D.1: 22 missing routes, substitution rules against v3 rendered DOM, mount opportunity_briefs + perception, 77 campaign runs visible, real-Chromium proof, floor 3006 (fix/refresh stale harness-receipt invariant first — refresh the harness, don't relax the threshold). Solva-v2 lift queues immediately behind.

Owner extension (verbatim, 2026-09-09T~11:40Z):

> Then STEPS 2 → 5 exactly as ordered: ingest evening drop (13th spec + NON-CLAIMS register) → ruling ledger banked + DEFAULT-class values wired tests-first → audit rebuild on the corrected index → fire W-REGISTRY-FULL-BUILD from a clean floor. Mission-framed report at each landing. Go.

---

## §B · Binding sources

| Source | Path | sha256 | Kind |
|---|---|---|---|
| Design prototype (BINDING) | `canon/drops/20260909/raw/RMS_AI_Prototype_standalone_v3.html` | `ee6ebe77e1c5…` | html · 2 032 024 B |
| Governance (BINDING) | `canon/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt` (Doc 0 v2) | derived from `Akki_Governance_Architecture_v1.docx` sha `b8af25f48698…` | text (source docx) |
| Surface audit reference | `notes/SURFACE_AUDIT_v2_prototype_20260907.md` | — | md (D.1 endpoint list) |
| Master traceability audit | `notes/MASTER_TRACEABILITY_AUDIT_20260907.md` + `20260909_UPDATE.md` | — | md |

Literal-design law (STANDING_ORDERS §4) applies: prototype v3 is **byte-identical**; interpretation banned; substitution rules bind to rendered DOM only; a rule matching nothing = RED. Interpretation-banned means: do not paraphrase v3's copy, do not swap element order, do not skip surfaces even if "similar" to v2 renders.

---

## §C · Scope

### C.1 · Route inventory (22 missing routes, per D.1)

**Registry-side routes (mount at `services/registry/router.py` or extended `registry_facts` router):**
1. `GET /api/registry/mix` — six-way cut breakdown (type / rights / language / condition / duplicates / quality)
2. `GET /api/registry/source/{source_id}/profile` — 15+ `efProfileVM.*` fields (depends on perception mount)
3. `GET /api/registry/cir` — Confidential Information Register (classification rows + pending-signature count)
4. `GET /api/registry/mix/reading` — narrative reading of the mix (product-copy renderer)
5. `GET /api/registry/estate_intelligence` — standout narrative from last census
6. `GET /api/registry/opportunities` — per-source opportunity briefs (surface renderer for opportunity_briefs)

**Census-side routes:**
7. `GET /api/census/history` — census run history with operator + timestamp per run
8. `GET /api/census/status` — current census state (running / idle / last-completed)

**Model-registry-side routes:**
9. `GET /api/model_registry/full_record` — extended per-model record with journal, checks, refusals, traffic
10. `GET /api/model_registry/{model_id}/journal` — per-model journal
11. `GET /api/model_registry/{model_id}/checks` — per-model check records
12. `GET /api/model_registry/{model_id}/refusals` — per-model refusal log
13. `GET /api/model_registry/{model_id}/traffic` — per-model traffic summary
14. `GET /api/model_registry/{model_id}/answering` — per-model answering-mode summary

**Opportunity-briefs-side routes (mount `services/opportunity_briefs/`):**
15. `GET /api/opportunity_briefs` — list all briefs
16. `GET /api/opportunity_briefs/{brief_id}` — brief detail
17. `POST /api/opportunity_briefs/regenerate` — trigger pipeline_runner
18. `GET /api/opportunity_briefs/by_source/{source_id}` — per-source briefs

**Perception-side routes (mount `services/perception/`):**
19. `GET /api/perception` — perception service surface (list)
20. `GET /api/perception/{source_id}` — perception on a specific source
21. `GET /api/perception/execution_mode` — execution-mode telemetry

**Rules-updates surface (companion to `/api/registry/cir`):**
22. `GET /api/rules_updates/pending` — pending signatures + rule-book adoption state

### C.2 · Substitution rules re-authored against v3 rendered DOM

- Enumerate v3 DOM anchor elements via the real-Chromium harness (already run once at 2026-09-09T11:49:03Z against v8/v2 · needs re-run against v3).
- Author `window.V3_SUBSTITUTIONS_DUMMIES` (mirror of `V8_SUBSTITUTIONS_DUMMIES`) with (name, kind, dummyContent, anchorAncestorText, rendered_dom_selector).
- Every rule must bind to at least one anchor in the v3 DOM (rule-matches-nothing = RED).

### C.3 · 77 campaign runs visible

Owner directive: "77 campaign runs visible in models roster". Enumerate campaign records from `phase0/campaign_drafts/campaign_*_v21_lane*_queue_manifest.json` + banked baseline_line records. Surface in `/api/model_registry/models` roster payload with `campaign_id` + `phase` + `ratchet_delta`.

### C.4 · Real-Chromium proof

Re-run `tools/wave_g5_realchrome_verification_harness.py --v3 --strict` (harness needs a `--v3` flag or v3 portal-swap wired) against v3 portal. Every substitution rule must render, every dummy must be absent, every expected sentence must be present. Screenshots banked at `phase0/eyeball_proxies/`.

---

## §D · Effort classes

Provisional per-CP scope (subject to landing arithmetic):

| CP | Scope | Class |
|---|---|---|
| CP1 | Route inventory tests-first (assert 22 target endpoints exist as FastAPI routes) | S |
| CP2 | Registry-side new routes (mix, source-profile, cir, mix-reading, estate-intelligence, opportunities) | M |
| CP3 | Census-side routes (history, status) | S |
| CP4 | Model-registry extended per-model routes | M |
| CP5 | Mount opportunity_briefs · surface 4 routes | M |
| CP6 | Mount perception · surface 3 routes | M |
| CP7 | Rules-updates pending-signatures route | S |
| CP8 | v3 substitution rules re-authored against v3 rendered DOM | L |
| CP9 | 77 campaign runs surfaced in models roster | S |
| CP10 | Real-Chromium harness v3 proof · wave close | S |

Total honest class: L (approx 2 000–3 000 LOC over 10 checkpoints).

---

## §E · Wave-honest limits (declared)

- **Data availability**: some new routes (mix cut breakdowns, opportunity briefs, perception, CIR) may return **honest-empty** payloads until upstream computation exists. Empty is not fake — it renders as "not yet measured" per STANDING_ORDERS §4 (no engineering vocabulary on product surfaces).
- **v3 portal swap**: v3 is a design surface, not necessarily a live-runtime substitution target today. The real-Chromium harness may need a v3 portal-mount before it can enumerate v3 anchors; if so, that becomes CP0 (portal swap).
- **77 campaign runs**: exact count depends on banked queue manifests + baseline_line rows. If the count is < 77 today, the payload names the number honestly plus a `honest_gap` sentence rather than fabricating rows.
- **Perception execution-mode telemetry**: mount only surfaces the existing `execution_mode_telemetry.py` — no new telemetry mechanism.

---

## §F · Two-commit protocol

Per STANDING_ORDERS §3:
- **Commit A (code):** `repos/Extraction-Akki/` on `programme/track-a` per CP: routers, mounts, tests, ratchet bump.
- **Commit B (state):** `/app/assessment_workspace/` on `master` per CP: grounding brief, notes, screenshots, drill receipts.
- **No push.** Local commits are the record.
- **Terminal pytest only.** Every close is double-green byte-match under `BASELINE_GUARD=1`.

---

## §G · Ratchet plan

Floor 3040 at wave open. CP-level additions (target):

| CP | Est. +invariants | Cumulative floor |
|---|--:|--:|
| CP1 | 22 (one per target route) | 3062 |
| CP2 | 6 (payload shape per new registry route) | 3068 |
| CP3 | 2 (census history/status shape) | 3070 |
| CP4 | 6 (extended model-registry route shapes) | 3076 |
| CP5 | 4 (opportunity_briefs mount + shape) | 3080 |
| CP6 | 3 (perception mount + shape) | 3083 |
| CP7 | 1 (rules_updates shape) | 3084 |
| CP8 | ~15-30 (v3 substitution rules bind-to-DOM) | 3099-3114 |
| CP9 | 1 (77-runs visibility) | 3100-3115 |
| CP10 | 2 (real-Chromium proof + wave-close manifest) | 3102-3117 |

(Actuals will differ; ratchet moves only on real double-green.)

---

## §H · Ambiguities named + DEFAULTs applied (§H DPO log)

Per STANDING_ORDERS §2: "state the specific ambiguity, apply ONE stated default with rationale, mark it `DEFAULT-PENDING-OVERRIDE`. Owner overrides on next turn if wrong."

- **DPO-W-REGISTRY-1**: The exact 22-route inventory. Owner directive names "22 missing routes" but SURFACE_AUDIT_v2 lists 25 new endpoints; the D.1 slice in §C.1 above (22 rows) was derived from the "W-REGISTRY-FULL-BUILD covers ~14 of these" line + the v3 additions (source-profile, cir, mix-reading, opportunities, extended model-registry per-model routes, opportunity_briefs mount, perception mount, rules_updates). Default: **use the 22 rows in §C.1**. If owner names a different 22 later, migrate at the next CP boundary.
- **DPO-W-REGISTRY-2**: `77 campaign runs` — provenance ambiguous (banked v21 queue manifests total ≠ 77 today). Default: **enumerate `phase0/campaign_drafts/campaign_*_v21_lane*_queue_manifest.json` unions with `phase0/baseline_lines/` sealed records**; report the honest count in the payload; if < 77, name the gap in `honest_gap`.
- **DPO-W-REGISTRY-3**: v3 portal swap timing — v3 may not be the currently-served portal at localhost:3000. Default: **treat v3 as a design source (byte-identical HTML) whose rendered DOM the harness reads by loading the file directly**, not by mounting v3 at the pod's frontend. This preserves literal-design adoption without a frontend migration in this wave. Portal-mount to v3 is a separate wave when owner rules on it.

---

## §I · Commit protocol (this wave)

Every CP close:
1. Mechanical RED banked at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_<cp>_RED_pre_impl.log` before code lands.
2. GREEN banked at `..._<cp>_GREEN.log` post-impl.
3. Full `BASELINE_GUARD=1` twice byte-identical.
4. `baseline_failures.json` `counts_at_baseline.passed` + `invariants_enforced_when_baseline_guard_1.passed_floor` bumped in tandem; `ratchet_history` entry appended.
5. Two-commit pattern.
6. Mission-framed owner report emitted at each CP close.

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
