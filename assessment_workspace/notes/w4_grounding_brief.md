# W4 · Northena direction/scope + ThinkLab surfaces — grounding brief

**Owner Order 2026-08-25 · "W4 go"** (verbatim in `STATE/DECISIONS.md`). Scope class **M** (~600 LOC estimate).

## 1. Doc 05 register rows targeted by W4

From `notes/requirements_register_17docs.md` §Doc 05 · 20 rows.

Full Doc 05 § extracted to fixtures (see `fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx`) — grounding recap of the canon mechanisms:

**Part A — Promise #16 (focus under massive context):**
- **A5.1 · [CANON]** Determinism-by-construction: no ML/learned import in `services/northena/`; import-assertion in CI.
- **A5.2 · [CANON]** Accountability standard: every run answerable deterministically (admitted because X; gated because Y; stopped because Z; refused because W).
- **A5.3 · [CANON]** Admit freezes; judgement is borrowed via opaque handle (Solva depth governor), never performed by Northena.
- **A5.4 · [CANON]** Gate = strict set-membership; no inferential path; adjacency ≠ membership; ambiguous membership is an Admit-time defect.
- **A5.5 · [CANON]** Converge owns halt on TWO fixed conditions (done-condition · budget); no learned stopping.
- **A5.6 · [CANON]** Budget is a hard stop enforced by governor (not executor).

**Part B — Promise #18 direction half (objective preservation):**
- **B5.1 · [CANON]** Freeze is atomic; artifact immutable for the run; changed intent = new admission.
- **B5.2 · [CANON]** Lawful basis enforced at Admit; five deterministic validity checks in order; each has own refusal reason.
- **B5.3 · [CANON]** Two admission paths (external request / work order via shaping dialogue); both write ledger row with artifact + lawful-basis references.
- **B5.4 · [CANON]** Ledger writer exposes APPEND ONLY (no update, no delete); enforced by import assertion.
- **B5.5 · [CANON]** Stamp-audit side-channel deliberately permissive (absorbs Solva traces, gate receipts, refusal envelopes) without mutating frozen row contract.

## 2. Row targets for W4 (mechanism-side of Doc 05)

- **Doc05-001** ← C4-030 · Admit / Gate / Converge / Ledger loop (Promise #16). Currently **REUSABLE**. W4 target: **DONE** (adapted into estate).
- **Doc05-006** ← C4-036 · Objective is frozen; a change is a new run (Promise #18 direction half). Currently **REUSABLE**. W4 target: **DONE**.

Additional Doc 05 rows this wave lights up (per register cross-reference):
- **§A5.1** determinism-import-assertion — piggybacks on W3's `test_no_llm_sdk_anywhere_in_backend`; extended to assert `services/northena/` also excludes learned imports.
- **§B5.4** append-only ledger writer — enforced by tests-first invariant.
- **§B5.2** lawful basis at Admit — five validity checks landed inside `admit.py`.

## 3. Real state on the ground

- **No Solva in this estate yet** — Solver + shrinkage + memory land in W5. Admit's judgement-borrowing surface (§A5.3) MUST be honestly stubbed: the "resolve_scope / defensibility_floor / preservation_depth" hooks are boundary contracts the Solva shim will fulfill in W5. Today the boundary returns pass-through-with-honest-gap.
- **No LLM crossing** — the reasoning stages inside the ThinkLab modes cannot execute; the surface renders navigation + honest dormant-state copy.

## 4. Reuse pulls cited

| Pull | Source | Destination | Discipline |
|------|--------|-------------|------------|
| **ADAPT** | `Akki-OS-V1/backend/services/northena/admit.py` (167 LOC) | `Extraction-Akki/backend/services/northena/admit.py` | Keep the FrozenArtifact + AdmitOffender + AdmitValidation shape verbatim (the deterministic completeness discipline is proven). Rewrite persistence from `core.db` (MongoDB async) → phase0/ JSON files (matches W2's reflection_records pattern). Stub the Solva boundary honestly (see below). |
| **ADAPT** | `Akki-OS-V1/backend/services/northena/gate.py` (51 LOC) | `Extraction-Akki/backend/services/northena/gate.py` | Keep strict set-membership discipline. Rewrite ledger writer to phase0/. |
| **ADAPT** | `Akki-OS-V1/backend/services/northena/converge.py` (149 LOC) | `Extraction-Akki/backend/services/northena/converge.py` | Keep the done-condition-beats-budget precedence + the absorb hooks pattern. Rewrite persistence. Skip the Solva/V2 absorb hooks (they'll wire in W5/W6/W7). |
| **ADAPT** | `Akki-OS-V1/backend/services/northena/ledger.py` (115 LOC) | `Extraction-Akki/backend/services/northena/ledger.py` | Keep append-only discipline + retention_mode env config. Rewrite `record()` to append a JSON file per row + maintain `phase0/northena_ledger/index.json` for read queries. |
| **ADAPT** | `Akki-OS-V1/backend/contracts/northena_ledger.py` (frozen contract) | `Extraction-Akki/backend/contracts/northena_ledger.py` | Keep the LedgerRow shape (run_id · trace_id · stage · decision · reason · artifact_ref · lawful_basis_ref · stamp_audit · at). |
| **BUILD (honest stub)** | — | `services/northena/admit_assist_stub.py` | Solva boundary. Returns identity for `resolve_scope`, a fixed floor "L2" for `defensibility_floor`, and a fixed depth "3" for `preservation_depth`. Every stub call is annotated with `stub_reason: "Solva not yet in force"` in the resulting artifact metadata — drawn-not-blank. |
| **v7 fabric** | `prototype/prototype.html` offset 265900–268700 (thinklab renders) + 388987–392000 (TL_MODES, TL_STAGE_LABELS, TL_OUTPUTS, LANDING_TIPS) | `Extraction-Akki/pod_shell/frontend/src/components/ThinkLab.jsx` | Extract mode registry + landing tips + stage labels VERBATIM. Reproduce the "← ThinkLab / mode num / mode title / mode duration" header + Frame/Name/Challenge/Weigh/Lock-in stage strip. Honest-drawn-not-blank the reasoning body ("the reasoning faculty is not yet in force"). |

## 5. Persistence — matches W2/W3 pattern

All records land under `/app/assessment_workspace/phase0/`:
- `phase0/northena_admits/adm-<hex12>.json` — one file per admission (frozen artifact + admit ledger row).
- `phase0/northena_ledger/led-<hex12>.json` — one file per ledger row (any stage).
- `phase0/northena_ledger/index.json` — append-only ordered list `[led_id, run_id, stage, at_iso]` for read queries by run.

Reason: identity/reference-not-copy holds; no external DB dependency; matches W2 reflection_records and W3 crossing_receipts on-disk shape.

## 6. Determinism boundary — Solva stub (§A5.3)

`admit_assist_stub.py` returns:
- `resolve_scope(scope_declared: list[str], registry) -> list[str]`: identity pass-through if all items are already resolved strings; refuses (empty list) if any item is empty/whitespace-only.
- `defensibility_floor(floor_declared) -> str`: if declared, echoes it; if not declared, returns `"L2_stub_awaiting_solva"`.
- `preservation_depth(depth_declared) -> int`: if declared, echoes it; if not declared, returns `3` with annotation.

Every frozen artifact carries `judgement_provenance: {"resolve_scope": "stub", "defensibility_floor": "declared|stub", "preservation_depth": "declared|stub"}` so downstream stages can honestly render "Solva-assisted judgement pending" per Doc 05 §A5.3 discipline.

## 7. ThinkLab surface — v7 fabric shape

4 destinations, each a mode:
| key | num | title | objective | duration |
|-----|-----|-------|-----------|----------|
| clarity | 01 | Seek clarity | Untangle a messy situation into the two or three questions that actually matter. | 15–20 min |
| strategy | 02 | Develop strategy | Build a defensible position — options, trade-offs, and the recommendation you would sign. | 25–40 min |
| hypothesis | 03 | Simulate a hypothesis | Stress-test a claim before management presents it. What would have to be true? | 20–30 min |
| perspective | 04 | Get perspectives | The same problem through the eyes of the audit chair, the CFO, and the sceptical investor. | 15–25 min |

Stage labels: **Frame → Name → Challenge → Weigh → Lock-in** (5 stages).

Outputs (retained for future waves): "A one-page Brief or PDF, exportable in one click." · "A decision trail you can table at the next meeting." · "Optional handoff to Task Manager as tracked work."

## 8. What ships in W4

- **Backend Northena**: admit → gate → converge → ledger, all writing to phase0/ JSON. HTTP surface: `POST /api/thinklab/admit`, `POST /api/thinklab/gate`, `POST /api/thinklab/converge`, `GET /api/thinklab/runs`, `GET /api/thinklab/runs/{run_id}`.
- **Frontend ThinkLab**: `/thinklab` landing (4 mode tiles + LANDING_TIPS + Outputs list) + `/thinklab/{mode}` mode-entry (direction/objective capture form → submits to Northena admit). On admit success, renders the frozen artifact + the 5-stage Frame/Name/Challenge/Weigh/Lock-in navigation strip + honest dormant-state body copy for reasoning stages.
- **Refusal grammar wire-through**: Doc 16 refusal card renders Doc 05 refusal reasons (missing_required_fields / missing_lawful_basis / scope_unresolved).

## 9. Doesn't ship (deferred, documented)

- Actual Frame/Name/Challenge/Weigh/Lock-in **reasoning** (needs Solva; W5).
- Brief/PDF export (needs reasoning; W5+).
- Task Manager handoff (needs Doc 15 handoff contract; W8).
- Stamp-audit absorb hooks for Solva/V2 refusal envelopes (needs those upstream engines; W5–W7).

## 10. Scope class M discipline

W4 accounts (estimate at open — will be measured at close):
- Backend contracts + services: ~600–700 LOC.
- Frontend surface: ~500 LOC.
- Tests: 15–20 invariants.
- **Estimate total: ~1200–1300 LOC** — a hair above M's typical top-end of 800 LOC. **Stop-and-report cap** if it grows past 1500 LOC; report at close if it lands materially above M's ~600 estimate — the growth is honest-gap + refusal grammar + surface fabric extraction.

## 11. Checkpoint commit plan

- Section A · W4 ruling logged + grounding brief banked → **checkpoint 1** (this commit).
- Section B · Northena backend (admit + gate + converge + ledger + contracts) + tests-first → **checkpoint 2**.
- Section C · HTTP router + wiring in pod-shell server + live smoke → **checkpoint 3**.
- Section D · ThinkLab frontend + tests-first + admit-walk screenshot → **checkpoint 4**.
- Section E · Wave close: STATE + status + green receipt → **checkpoint 5**.
