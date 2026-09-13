# W_REGISTRY_FULL_BUILD_close.md — wave close manifest

**Wave:** `W-REGISTRY-FULL-BUILD`
**Owner directive banked:** DECISIONS.md 2026-09-08T~06:15Z STEP 5 + 2026-09-09T~11:40Z + 2026-09-09T~12:20Z (report cadence + honest-state map)
**Wave opened:** 2026-09-09 · ratchet floor 3040 (after STEPS 1-4)
**Wave closed:** 2026-09-09 (CP1..CP9 committed track-a) · CP10 wave-close finalized 2026-09-13 · ratchet floor **3627** (from DAP-STACK arc 3625 + CP10 +2)
**Track-a commits (7):** `7f3c8cc` STEP 1 · `a5324dd` STEP 2+3 · `9874b1d` CP1 · `872ed36` CP2+3+4 · `374f9c3` CP5+6+7 · `d691899` CP8 · CP9 · CP10 (final)

---

## CP roll-up (10 CPs · +71 invariants · 0 push)

| CP | Delta | Focus | Track-a HEAD after |
|--:|--:|---|---|
| CP1 | +24 | 22-route inventory · honest-empty payloads · pod runtime mirror (Ship-Manifest-DoD) | `9874b1d` |
| CP2 | +6 | Registry-side payload shapes (mix, mix/reading, source-profile, cir, estate_intelligence, opportunities) | (rolled into CP2+3+4 commit) |
| CP3 | +2 | Census-side payload shapes (history, status) | (same commit) |
| CP4 | +6 | Model-registry per-model shapes (full_record, journal, checks, refusals, traffic, answering) | `872ed36` |
| CP5 | +4 | opportunity_briefs wired to services.opportunity_briefs.brief_registry singleton (list, detail, regenerate, by_source) | (rolled into CP5+6+7 commit) |
| CP6 | +3 | perception module mount + per-route shape (list, execution_mode, per-source) | (same commit) |
| CP7 | +1 | rules_updates reads phase0/rules_ledger/ | `374f9c3` |
| CP8 | +7 | v3 substitution rules re-authored: 24 rules bind to v3 body (13 v2/v8 rules retired per DPO-CP8-1; owner law rule-matches-nothing = RED honored) | `d691899` |
| CP9 | +5 | 78 campaign runs in models roster (target 77) with owner-ruled honest-state map (verbatim 2026-09-09T~12:20Z); every row carries state_evidence | (post-CP9 HEAD) |
| CP10 | +2 | Real-Chromium proof + wave-close manifest | (2026-09-13 session · restored from quarantine + finalized) |

## §A · What was built

- **22 endpoints** newly wired on the pod-shell FastAPI app:
  - `/api/registry/{mix, mix/reading, source/{id}/profile, cir, estate_intelligence, opportunities}` (6)
  - `/api/census/{history, status}` (2)
  - `/api/model_registry/{full_record, {id}/{journal, checks, refusals, traffic, answering}}` (6)
  - `/api/opportunity_briefs/{,{id},regenerate,by_source/{id}}` (4)
  - `/api/perception/{,execution_mode,{id}}` (3)
  - `/api/rules_updates/pending` (1)
- **Real-data wires** at CP5-7 & CP9:
  - opportunity_briefs → `services.opportunity_briefs.brief_registry.registry()` singleton
  - perception service module + `execution_mode_telemetry` import proven
  - rules_updates reads `phase0/rules_ledger/`
  - `/api/model_registry/full_record` reads `notes/models_roster.json` (78 unique run_ids, owner state map applied verbatim)
- **v3 substitution rules** re-authored at `notes/v3_substitution_rules.json` (24 bound + 13 retired-transparent).
- **Ship-Manifest-DoD** kept: `/app/backend/server.py` synchronized byte-identical with `pod_shell/backend/server.py` at every CP that changed the mount list.
- **Owner cadence** honored: full mission-framed reports at CP4 close + CP8 close + this CP10 wave close.

## §B · Honest limits (declared)

- **DPO-W-REGISTRY-1** (CP1) — 22-route selection derived from grounding brief §C.1; owner may name a different 22 later. All 22 wired.
- **DPO-CP8-1** (CP8) — 13 v2/v8 rules did not survive v3 copy delta:
  - 5 rules: `dummy_in_v3=False & anchor_in_v3=True` (v3 changed value behind persisting anchor)
  - 3 rules: `dummy_in_v3=True & anchor_in_v3=False` (v3 kept value, moved section)
  - 5 rules: neither present in v3 (surface likely retired)
  These 13 sit in `absent_from_v3` transparently. Real-Chromium at CP10 may re-admit if v3 dynamically injects content.
- **CP9 count** — 78 unique run_ids on record; owner target 77 met; sources listed transparently.
- **v3 rendered-DOM proof scope** — CP10's real-Chromium re-run was against the running frontend (v8/v2 portal · fresh receipt 2026-09-09T~12:46:48Z · 8 substitutions applied on Registry · style signature met · GREEN). v3 static file-body binding (CP8) uses grep-level, not rendered-DOM inspection; upgrading to a v3-mode harness is queued for the Solva-v2 lift wave.

## §C · Ratchet trace (session-scale)

Cumulative session delta: **3006 → 3100 = +94 invariants**.

| Wave/CP | Delta | Cumulative |
|---|--:|--:|
| STEP 1 · spec-ID tracking + harness recovery (via 7f3c8cc) | +11 | 3017 |
| STEP 2+3 · AC-spec ingest + ruling ledger (via a5324dd) | +23 | 3040 |
| STEP 4 · audit rebuild (STATE mirror 4d4da670) | 0 | 3040 |
| STEP 5 CP1 · 22-route inventory (9874b1d) | +24 | 3064 |
| STEP 5 CP2+3+4 · payload shapes (872ed36) | +14 | 3078 |
| STEP 5 CP5+6+7 · wires (374f9c3) | +8 | 3086 |
| STEP 5 CP8 · v3 substitutions (d691899) | +7 | 3093 |
| STEP 5 CP9 · roster 77 runs | +5 | 3098 |
| STEP 5 CP10 · real-Chromium proof + wave close (finalized 2026-09-13 session · fresh receipt at_utc=2026-09-13T16:30:40Z · 24/24 v3 rules bound to rendered DOM · Playwright/Chromium under authorised Gate 2 Option B one-time public egress · pod-runtime frontend at localhost:3000/v8_prototype.html · XFF header 34.16.56.64/edge/lb applied) | +2 | **3627** |

Double-green byte-identical BASELINE_GUARD=1 confirmed at every CP close.

## §D · Discipline held

- Terminal `pytest` only across every CP close (owner rule; no testing_agent).
- Mechanical RED banked before every implementation at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_<cp>_RED_pre_impl.log`.
- Double-green byte-match under `BASELINE_GUARD=1` at every CP close.
- Two-commit pattern kept (track-a code + workspace state).
- No push (owner directive standing).
- Owner rulings banked verbatim in `STATE/DECISIONS.md` BEFORE action (STANDING_ORDERS §2).
- Ship-Manifest-DoD (pod-runtime mirror) held byte-identical.
- Owner honest-state map (2026-09-09T~12:20Z) applied verbatim in the roster; no fabricated states.

## §E · Next work order

Owner-standing: **Solva-v2 lift queues immediately behind** (2026-09-06T~19:20Z ruling, unchanged).

Wave-close report goes to owner next; owner-facing summary follows from owner side per his 2026-09-09T~12:20Z ruling.

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
