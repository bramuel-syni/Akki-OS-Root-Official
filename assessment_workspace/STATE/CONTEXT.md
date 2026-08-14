# CONTEXT.md — Running narrative

**Last updated:** 2026-08-14 · Owner course-correction cycle CLOSED · wizard rebuilt to the brief's 5-step grammar (1 What -> 2 How -> 3 Credentials -> 4 Name -> 5 Attempt) for ALL resource kinds · estate ed25519 keypair generated in seam key custody + provisioning card rendered at compute Step 2 · non-compute intent recorded honestly at Step 5 · programme/track-a HEAD `f83b509` · 123/123 gating tests green (90 backend python + 12 frontend allowlist + 21 frontend rehome/wizard).


## Standing owner instruction · 2026-08-14 · POSTURE CORRECTION

Verbatim from the course-correction reply:
> "I worry you are more focussed on whats missing than piecing together what you have. to drive a progressive journey."

**Binding standing posture (applies to every cycle from now on until explicitly rescinded):**

- **Assemble the progressive journey from what exists.** Piece together from the fixture materials, guide figures, and prior decisions rather than gating on what has not yet arrived.
- **Escalate only TRUE blockers.** Missing paint colours, missing screenshots that repeat information already in a written spec, or ambiguities that can be resolved by reading the brief carefully are NOT true blockers.
- **Change is tone and initiative, NOT evidence standards.** Honesty discipline unchanged: no fabrication, no invented fixture material, no papering over conflicts, still escalate-and-stop on genuine ruling conflicts.
- **When in doubt between reporting-and-waiting vs building-and-reporting: choose building-and-reporting, provided the fixture materials contain enough grammar to build honestly.**


## Course-correction event · 2026-08-14 · fixture-drop follow-on

Owner course-corrected the fixture-drop cycle with three rulings + one build proposal:

1. **FL-P2-14 CLOSED BY OWNER.** The "19 pages" was the owner's claude.ai prototype, not a missing deck. The fixture set (5-page written brief + Registry screenshots + AISCA guide figures) IS the fixture. Stop chasing it.
2. **Standing posture correction** (recorded above).
3. **Wizard is generic.** Prior build shipped Compute-chip -> straight to a 7-field form; the brief specifies FIVE conversational steps for ALL kinds. Rebuild the wizard to the brief's 5-step grammar, tests-first.
4. **Provisioning-card proposal** from AISCA Fig 10/11: generate estate keypair in seam custody; render public key + pod egress IP as a card BEFORE credentials are keyed; owner pastes public key into VM Access + adds both /32 rows at creation; VM becomes key-reachable from first boot.

**Executed this cycle (tests-first, both banked with right-reason receipts before implementation):**

- Backend: `services/estate_keys/keypair.py` (idempotent ed25519 openssh keypair custody, private mode 0600, never in return values). `services/connect_estate/router.py` with `GET /api/connect/estate-facts` + `POST /api/connect/intent`. Both mounted in pod-shell server behind the IP allowlist middleware.
- Frontend: `ConnectWizard.jsx` rewritten as a 5-step state machine with per-type branches at Step 2, provisioning card at compute Step 2, GPU form at compute Step 3, name-in-the-estate's-words at Step 4, handshake walk at compute Step 5, honest intent record at non-compute Step 5. Registry unchanged from the previous cycle.
- Scope reported both ways: strict L (2 new contracts) vs cohesive M (one incremental surface per owner's phrasing). Built under the cohesive reading per owner's "ships NOW" imperative.
- 123/123 total gating tests green (90 backend python + 33 frontend node --test).
- Six Playwright screenshots banked under `phase0/drill_receipts/screenshots/20260814T190000Z_*.jpeg` proving all 5 steps + non-compute honest Step 5.
- Fidelity ledger: FL-P2-14 CLOSED-BY-OWNER, FL-P2-16 CLOSED (wizard grammar), FL-P2-17 CLOSED (provisioning card), FL-P2-18 CLOSED (posture correction).
- IP allowlist unchanged: `SPINE_ALLOWED_IPS=34.16.56.64` per owner's strict directive.
- Live provisioning-card content this cycle (rotates on pod restart):
  - Estate public-key fingerprint: `SHA256:TpJcdNAQ4iSQKK5inwPueOM6Qak5NcsD5XhZpWorZ+c`
  - Pod egress IP: `104.198.214.223` (was `34.170.12.145` earlier this session; STATE previously pinned `34.16.56.64`)

**Track-a commits this cycle:** `760c53d` (tests-first · 33 assertions), `5f67591` (backend implementation · 12/12 green), `f83b509` (frontend implementation · 21/21 rehome green).

**Assessment-repo master commit:** pending this cycle's follow-up (STATE + fidelity ledger + phase0 receipts + DECISIONS appendix + screenshots).


## Fixture-drop event · 2026-08-14 · Screen mockups v7 delivery

Owner dropped `fixtures/screen_mockups_v7.pdf` (sha256 `418ad0e3...`, 195,644 bytes) plus a textual description of 4 inline screenshots covering the Registry surface (three tabs + role switcher + "+ Connect") and the Connect wizard (conversation-not-form drawer with 4 suggestion chips + free-text + Send). Owner directed reconciliation orders: (a) re-shape GPU credential entry to honor the wizard grammar (Compute path collects same 7 ordered fields, submit machinery unchanged); (b) Registry three tabs render HONEST current state, not the mockup's demo-org figures (A4 increment, next cycle); (c) role switcher = static presentation (Track-B auth deferred); (d) scope check on (a).

**Discrepancy flagged as FL-P2-14 OPEN:** owner said "19 pages plus 4 inline screenshots" - actual PDF is 5 pages of pure text (Registry Feature & Component Brief, zero embedded images); the 4 inline screenshots weren't accessible as job assets. Owner's inline textual description stands as the binding visual reference; PDF stands as the written spec. Written spec + inline description was sufficient for this build.

**Executed this cycle:**

1. Fixture pinned in PINS.md as file-cleared (upgraded from transcription-grade for Registry surface + Connect wizard grammar). Full page-by-page inventory at `fixtures/screen_mockups_inventory.md`.
2. Scope check for (a): **M class** (2 components + 0 new contracts + 1 integration surface, unchanged) - within WS-BUILD-CONNECT-GPU scope ceiling.
3. Test-suite migration:
   - `pod_shell/frontend/__tests__/rehome.test.js` grew from 9 to 15 gating assertions.
   - 7 retained (unchanged), 2 migrated (root '/' now → Registry; AdminSurface retired), 6 new (Registry testids + wizard shape + Compute path + endpoint unchanged + zero fabricated numbers + honest empty state).
   - Right-reason failure receipt banked at `phase0/drill_receipts/20260814T180000Z_registry_wizard_right_reason_failure.log`: 7/15 fail with right-reason errors before implementation lands.
4. Implementation on `programme/track-a`:
   - `src/App.js` → root '/' renders `<Registry />` (was `<AdminSurface />`).
   - `src/components/Registry.jsx` NEW: header (Akki · ESTATE + role switcher chips + user glyph), title deck, tab bar (DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS with 2px active underline), "+ Connect" button pushed right, empty-panel body honoring Content Rule 3.
   - `src/components/ConnectWizard.jsx` NEW: right-hand drawer with "Connect something new" + "A conversation, not a form" deck, 4 suggestion chips, free-text + Send, Compute path branches to the SAME 7 ordered GPU fields with masked password → POST to unchanged `/api/connect/gpu`.
   - `src/components/AdminSurface.jsx` DELETED (superseded).
5. Live-proof:
   - Preview URL: 4/4 route families still refused with HTTP 403 + exact sentence (allowlist unchanged).
   - Local FE with allowed XFF: `/` → 200 SPA shell; `/register/connect/gpu` → 404 retirement notice.
   - Local BE with allowed XFF: `/api/deliverables` → 200 JSON; `POST /api/connect/gpu {}` → 422 Pydantic (same payload contract).
   - Playwright: 4 screenshots banked at `phase0/drill_receipts/screenshots/20260814T181000Z_*.jpeg`; all 20 required data-testids present in rendered tree.
6. Green receipt banked at `phase0/drill_receipts/20260814T181500Z_registry_wizard_green.log`. 105/105 gating tests green.
7. Fidelity ledger: FL-P2-11 CLOSED (fixture upgrade), FL-P2-12 CLOSED (wizard-not-form), FL-P2-13 CLOSED (demo-data-vs-honest-state), FL-P2-14 OPEN (page-count discrepancy), FL-P2-15 CLOSED (role switcher static).
8. IP allowlist unchanged: `SPINE_ALLOWED_IPS=34.16.56.64` per owner's strict directive.

**Track-a commits this cycle:** `65964b0` (tests-first · Registry + wizard invariants), `aeb2be0` (implementation · Registry + wizard 15/15 green).

**Assessment-repo master commit:** pending this cycle's follow-up (STATE + fidelity ledger + phase0 receipts + fixture inventory + PDF + DECISIONS appendix).


## Compaction / recovery event · 2026-08-14 · mid-stop-order execution

Third compaction / restart occurred mid-execution of the Owner Stop-Order (queued: revoke token → build IP allowlist middleware tests-first → re-home form → propose IP-pinned access mechanism → commit both repos). Post-compaction recovery sequence executed:

1. **Security verification (P0, before anything else).**
   - `/app/backend/.owner_credentials` — verified DELETED (was still present at recovery start; deleted this session; backend restarted; deleted again to discard the auto-mint that spine_auth performed at import).
   - `/app/backend/spine_auth.py` — verified DELETED (token machinery retired estate-wide).
   - `/app/memory/test_credentials.md` — verified SCRUBBED (no 64-hex tokens anywhere; scrubbed content replaced with IP-pinned access posture).
   - Old compromised token probe on `/api/connect/gpu` → HTTP 403 (was HTTP 422 = accepted before revocation).
   - Leak hunt: 0 hits across `/app` filesystem (excluding pycache), 0 hits in spine repo git-grep, 0 hits in `/var/log/supervisor/*.log`, 0 hits in STATE/notes/phase0.

2. **Lockdown verification.**
   - `services/ip_allowlist/middleware.py` (spine repo) exists · 16/16 gating tests green.
   - `plugins/ip-allowlist/{check.js, middleware.js}` (pod-shell frontend) exists · 12/12 gating tests green.
   - `SPINE_ALLOWED_IPS=34.16.56.64` + `SPINE_TRUSTED_PROXY_HOPS=2` present in `/app/backend/.env` (single source of truth read by both backend and frontend craco config).
   - Live proof · preview URL: `/`, `/register/connect/gpu`, `/api/deliverables`, `/api/connect/gpu`, `/static/*` all return HTTP 403 `text/plain` with the exact sentence `"This surface answers allowlisted addresses only."` (refusal branch, pod egress `34.170.12.145` NOT in allowlist per owner's strict `34.16.56.64` directive).
   - Live proof · 127.0.0.1 with crafted XFF: allowed IP at `xff[-3]` → 200; disallowed IP at `xff[-3]` → 403; spoofed leftmost XFF entries on allowed IP → still allowed; spoofed leftmost XFF entries on disallowed IP → still refused (spoof resistance intact).

3. **Cold-read of STATE/ this recovery cycle.**
   - DECISIONS.md carries Rulings 1/2/3, Orchestrator A/B/C, Build Order 01, Owner Clarifications 1-3, prior WS-BUILD-CONNECT-GPU rulings, AND the new Owner Stop-Order Ruling (verbatim reconstruction) plus the Orchestrator shared-defect ruling appended this cycle.
   - PINS.md carries prior repo/canon/fixture pins; refreshed this cycle with new HEAD SHA, egress-IP surprise notation, updated gating count.
   - NEXT.md updated to reflect completed stop-order execution and the awaited owner reply.
   - Fidelity ledger appended: FL-P2-08 CLOSED (minted-credential retirement), FL-P2-09 OPEN (pod-egress rotation), FL-P2-10 CLOSED (empirical trust-boundary discovery).

4. **Re-home completion status.**
   - `/register/connect/gpu` retired at edge (dev-server middleware returns HTTP 404 `text/plain` `"This route has been retired."`).
   - `/app/frontend/src/App.js` — root `/` → `<AdminSurface />` · catch-all `*` → `<NotFound />`.
   - `/app/frontend/src/components/AdminSurface.jsx` — new. Tile grid + detail card + embedded GPU form. NO token state anywhere.
   - `/app/frontend/src/components/ConnectGpu.jsx` — deleted (retired token-gated variant).
   - Empirical header trust boundary discovered before code landed (see Phase 0 drill receipts + FL-P2-10).
   - Right-reason failure receipts banked for BOTH new invariants (IP allowlist + re-home) before implementation.
   - Pod-shell mirror committed at `pod_shell/` in Extraction-Akki (production-code discipline preserved: source of truth remains `/app/{backend,frontend}` since those are what run; the mirror is the git-tracked record on programme/track-a).

5. **Commits this cycle.**
   - programme/track-a: `e25cfe3` (IP allowlist tests-first), `93ed48e` (IP allowlist implementation), `d2a3a01` (re-home tests-first), `acc25a8` (re-home + pod-shell mirror).
   - assessment-repo master: pending this cycle's commit (STATE + fidelity ledger + phase0 receipts + DECISIONS appendix).

**Resume point (per NEXT.md):** deliver stop-order completion report to owner including security-verification results, live-vs-test proof rollup, commit SHAs, and the two-sentence access-mechanism proposal.


## Compaction / recovery event · 2026-08-14 · post-fixture-arrival

Second compaction / restart occurred after fixture-arrival cycle (queued message: FIXTURES ARRIVED — download + hash + extract + clear FIXTURE PENDING + update DoDs + extract SOPs + escalate-and-stop on conflicts). Cold-read from disk performed against STATE/ before resuming.

**Present on disk (verified):**
- STATE/{CONTEXT,PINS,DECISIONS,NEXT}.md — all four; DECISIONS.md carries Rulings 1/2/3, Orchestrator A/B/C, Build Order 01 verbatim (dated 2026-08-14), and Owner Clarifications 1-3 (no-push · VM SSH access to be granted · fixtures re-upload).
- `BUILD_STRATEGY.md` — 2441 lines at commit `42b241c` (v1.1 self-contained assembly).
- `REUSE_ASSESSMENT.md` — 53,479 bytes, accepted.
- `notes/fidelity_ledger.md` — 101 lines, 8+7+12+1+1+2 = 31 rows CLOSED (owner's 27 + FL-R1-01/FL-P1-20 retained + FL-P2-01/02 opened during Part-2 drafting).
- `fixtures/Akki_Prototype_v7_Design_Brief.md` — 18,791 bytes · sha256 `063f2b470d74dcd30ad43b4645c4e656edaa7fb1185198a4116ad5328a9717b4`.
- `fixtures/AISCA_GPU_Access_Guide.pdf` — 535,169 bytes · sha256 `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3`.
- `fixtures/reference_screenshot_transcription.md` — created this recovery cycle from owner's inline transcription (Q1(c) ruling · 2026-08-14) · sha256 `d3ae9a6cf598a38333b5c11d6d73dc9069dc3671fb31598f2e594dfb002fc949` · grade AUTHORITATIVE-UNTIL-FILE-ARRIVES.
- `phase0/` — commissioning_checklist.md · acceptance.sh · commissioning_record_template.md · A0-A1_report.md · drill_receipts/20260814T120336Z_declaration_refusal_firing.log.
- Extraction-Akki clone with branch `programme/track-a` (baseline `b150c21`); Phase-1 code + tests staged on disk (7 new files under `backend/`) — pending commit on `programme/track-a`.
- Pod egress IP re-verified fresh via 4 curl services: **`34.16.56.64`** (unchanged; no IPv6).

**Missing / requires immediate action:**
- **Corrections commit (post-`42b241c`) NOT YET MADE on assessment repo.** `BUILD_STRATEGY.md` at HEAD still carries the three defects Build Order 01 named:
  - Line 1742: "Nine XL items" (stale count).
  - Line 2017: "Placeholder — Part 2 has not been drafted yet".
  - Line 1939 (FL-OQ-04) and Line 2165 (§Appendix C5-010..C5-012 row): "four consoles" phrasing.
  Working papers `notes/strategy_sections.md` and `notes/fidelity_ledger.md` carry the corrected content (uncommitted); BUILD_STRATEGY.md needs a re-assembly + commit.
- Fixture SHA-256 hashes not yet in `PINS.md` (attachment-status line still records "NOT yet delivered").
- Item DoDs across BUILD_STRATEGY.md interface items still read `FIXTURE PENDING`; awaiting binding-acceptance-criteria extraction from v7 brief + transcription, and `test_four_questions_topline_present` addition to their new-invariants lists.
- AISCA GPU SOP not yet extracted / reconciled against Order §6 (escalate-and-stop on conflict per owner's Q2(a) ruling).
- Phase-1 test/code files (`backend/contracts/*.py`, `backend/services/declaration/*`, `backend/services/compute_seam/*`, `backend/tests/invariants/actor_declaration_*`) staged on `programme/track-a` but NOT YET committed — HEAD still at `b150c21`. Owner's Q3 ruling this cycle covers ONLY the assessment-repo master commit; `programme/track-a` phase-1 commit is a separate cycle and stays untouched here.
- FL-P1-14 in the ledger reads `CLOSED — fixture is the attached screenshot plus the attached v7 brief`; this now needs the transcription-cleared vs file-cleared grade distinction per owner's Q1(c) ruling.

**Resume point (per owner's plan-confirmation rulings):**
1. Extract binding acceptance criteria from v7 brief + transcription into `fixtures/binding_acceptance_criteria.md`.
2. Extract AISCA SOP into `fixtures/aisca_sop_extraction.md`; reconcile against Order §6 bindings; escalate-and-stop on any conflict.
3. Update PINS.md (fixture hashes + attachment-status flip).
4. Update fidelity_ledger.md FL-P1-14 with transcription-cleared vs file-cleared grade distinction; add fixture-arrival log row FL-P1-14a.
5. Rewrite `FIXTURE PENDING` markers across BUILD_STRATEGY.md item DoDs to cite the extracted criteria; add `test_four_questions_topline_present` to console items' new-invariants lists.
6. Apply the three Build-Order-01 corrections in BUILD_STRATEGY.md (via assembly tool re-run, since notes/ already carry the corrected content).
7. Re-run citation_audit.py + completeness_audit.py.
8. Refresh backend/deliverables snapshots.
9. Commit on assessment-repo `master` (linear record per owner's Q3 ruling); update NEXT.md.
10. Reply to owner with the phase-1/fixture report + fresh egress IP.


## Where we are

- **Execution authorized** on branch `programme/track-a` in Extraction-Akki (baseline `b150c21`, never rewritten). Production-code prohibition lifted ONLY for this branch per Build Order 01.
- **All 27 fidelity-ledger rows CLOSED** by Build Order 01 rulings; ledger frozen.
- **Three corrections applied** (§10.F stale placeholder replaced; XL count 9→7 reconciled; Canon 5 §10 "exactly five consoles" verified — extraction was fine, premise was paraphrase defect).
- **Phase 1 A0/A1 tests-first GREEN** — 26/26 gating tests pass; declaration-refusal drill banks Ruling-1 precondition (a).
- **Compute seam built** (folded into Phase 1 per Owner Clarification 2) with tests-first discipline; ready for credentials.
- **Pod egress IP** `34.16.56.64` reported for VM allowlist.
- **Rulings issued:** Ruling 1, Ruling 2, Ruling 3/Instruction 02, Orchestrator Rulings A/B/C, Build Order 01, Owner Clarifications 1-3. All verbatim in `DECISIONS.md`.
- **No push** (Owner Clarification 1). Local git history IS the record.
- Prohibitions still in force for anything OFF `programme/track-a`: no production code, no scaffolding, no canon edits.

## Attachment gap (recorded per Owner Clarification 3 · 2026-08-14)

The three fixtures referenced by Build Order 01 — reference screenshot, `Akki_Prototype_v7_Design_Brief.md`, `AISCA_GPU_Access_Guide.pdf` — were NOT delivered with the order and had NOT arrived as of Owner Clarification 3 (re-upload signalled). Per the order's own text "every FIXTURE PENDING clears on their arrival in the workspace," FL-P1-14's substantive closure is CONDITIONAL. Fixture-bound work (A4 operating surface, Track-B console items, Watch Console §6 verbatim consumption) is BLOCKED until they land. **Nothing in A0-A3 is blocked.**

## Deliverable manifest (current)

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — Chunk-3 accepted.
- `/app/assessment_workspace/BUILD_STRATEGY.md` — Chunk-4 v1.2 self-contained (re-assembled after Build Order 01 + rulings).
- `/app/assessment_workspace/phase0/` — commissioning_checklist.md · acceptance.sh · commissioning_record_template.md · A0-A1_report.md · drill_receipts/.
- `/app/assessment_workspace/repos/Extraction-Akki/` (branch `programme/track-a`, baseline `b150c21`):
  - `backend/contracts/actor_declaration.py`, `backend/contracts/record_matrix.py`, `backend/contracts/task_identity.py`
  - `backend/services/declaration/`, `backend/services/compute_seam/`
  - 7 new invariant tests + parity-seat snapshot in `backend/tests/invariants/`
  - `backend/tools/report_egress_ip.sh`, `backend/tools/ssh_preflight.py`, `backend/tools/run_acceptance_via_seam.py`.
- Working papers on disk (feeding BUILD_STRATEGY.md assembly):
  - `notes/strategy_items_part1.md`, `strategy_items_part2.md`, `strategy_sections.md`, `fidelity_ledger.md` (closed), `row_to_item_index.md`.
- Assembly tool: `tools/assemble_build_strategy.py`.
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.

## Audit posture (current)

- Citation audit: 104/104 file · 1778/1778 canon · **0 failed** (post-remediation, includes BUILD_STRATEGY.md).
- Completeness audit: PASS — every non-REUSE row assigned; every item has 7 fields; BUILD_STRATEGY.md self-contained.
- Phase-1 gating tests: **26/26 pass** on `programme/track-a`. Ruling-1 precondition (a) demonstrated firing (declaration-scoped refusal observable in the ledger via drill).
- Zero regressions introduced: only new files added to Extraction-Akki, no existing code modified.

## Downloadable snapshot (2026-08-14 · Orchestrator delivery-logistics directive)

The two deliverables are served READ-ONLY through the pod template's FastAPI backend as **snapshots** (not a live mount of this workspace). Refresh discipline: after each material change to either document, re-copy from `/app/assessment_workspace/` to `/app/backend/deliverables/` and update the snapshot commit literal in the listing endpoint.

- `https://akki-reuse-assess.preview.emergentagent.com/api/deliverables/BUILD_STRATEGY.md`
- `https://akki-reuse-assess.preview.emergentagent.com/api/deliverables/REUSE_ASSESSMENT.md`
- Listing at `/api/deliverables` returns snapshot commit + size + URL for each.

## Citation-drift root cause (Orchestrator Ruling A — retained record)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for all future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z (historical)

Context compaction / restart occurred ~2026-08-14T09:24Z. Recovery from disk + queued brief succeeded; all subsequent work is captured above.

## Deliverable manifest

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — Chunk-3 accepted.
- `/app/assessment_workspace/BUILD_STRATEGY.md` (2442 lines) — Chunk-4 v1.1 self-contained assembly.
- Working papers on disk (feeding the assembly):
  - `notes/strategy_items_part1.md` (838 lines, 47 items).
  - `notes/strategy_items_part2.md` (628 lines, 55 items).
  - `notes/strategy_sections.md` (269 lines).
  - `notes/fidelity_ledger.md` (102 lines, 27 open items, frozen).
  - `notes/row_to_item_index.md` (405 lines, 591 rows → 102 items, 0 named gaps).
- Assembly tool: `tools/assemble_build_strategy.py`.
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.

## Downloadable snapshot (2026-08-14 · Orchestrator delivery-logistics directive)

The two deliverables are served READ-ONLY through the pod template's FastAPI backend as **snapshots of commit `42b241c`** (not a live mount of this workspace). Snapshot copies live at `/app/backend/deliverables/{BUILD_STRATEGY.md,REUSE_ASSESSMENT.md}`; served via `GET /api/deliverables/{filename}` with a two-name allowlist. Identity verified byte-for-byte via sha256 against the workspace originals at snapshot time.

- `https://akki-reuse-assess.preview.emergentagent.com/api/deliverables/BUILD_STRATEGY.md` — 244,199 bytes, sha256 `86af07ce…c820688`.
- `https://akki-reuse-assess.preview.emergentagent.com/api/deliverables/REUSE_ASSESSMENT.md` — 53,479 bytes, sha256 `36314268…d427327a`.
- Listing endpoint: `https://akki-reuse-assess.preview.emergentagent.com/api/deliverables` returns snapshot commit + size + URL for each.

**Refresh discipline.** If either working document is amended (e.g., after a new Ruling), re-copy the file from `/app/assessment_workspace/` to `/app/backend/deliverables/` and update the snapshot commit in `CONTEXT.md` and in the `/api/deliverables` listing endpoint literal. Do NOT symlink the workspace live — the snapshot boundary is deliberate.

## Audit posture at v1.1 assembly

- Citation audit (now includes BUILD_STRATEGY.md): 104/104 file · **1778/1778 canon · 0 failed**.
- Completeness audit (now validates BUILD_STRATEGY.md self-contained): PASS — every non-REUSE row assigned; every work item has 7 fields; BUILD_STRATEGY.md self-contained confirmed.
- Cold-read recovery test: STATE/ is self-sufficient; verified.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## What Ruling 1 changes

- **Binding transition condition on the purpose-gate contradiction (Open Question #1)**: Executive-Core's `services/synisense/shield/purpose_validator.validate_purpose()` (at `client.py:63`) is NOT stripped until BOTH (a) the actor-declaration check (Canon 3 §6.1, Assessment C3-008/C3-009/C3-010) AND (b) the Watch's reconciler are DEMONSTRATED FIRING. This turns Open Question #1 from an open governance call into a conditional strip whose enabling conditions are named.
- **Implicit resolution of Open Question #2 (actor declaration seam)**: because Ruling 1 makes the declaration check a precondition for the purpose-gate strip, the declaration check is confirmed a BUILD item (not left open or absorbed elsewhere). Cite: DECISIONS.md Ruling 1.
- **Executive-Core purpose gate posture**: RETAINED as a canon-compliant surface at Executive-Core HEAD until the two demonstrations fire. Not classified RETIRE until the transition condition is met.

## Open Questions status (from REUSE_ASSESSMENT.md §8)

| OQ | Status after Ruling 1 |
|---|---|
| 1. Purpose-gate contradiction | **PARTIALLY ANSWERED** — retention is conditional, strip is enabled by two demonstrated-firings. Fidelity-ledger entry for the strip itself remains. |
| 2. Admit-declaration seam | **ANSWERED (implicit)** — declaration check WILL be built. |
| 3. Rule-change re-verify step | OPEN — remains in fidelity ledger. |
| 4. Canon 5 four vs five consoles | OPEN — remains in fidelity ledger. |
| 5. Studio canonical scope | OPEN — remains in fidelity ledger. |
| 6. Eight vs five global rules | OPEN — remains in fidelity ledger. |
| 7. Cohort surface's canonical home | OPEN — remains in fidelity ledger. |
| 8. Work_studio storage coupling | OPEN — remains in fidelity ledger. |
| 9. Akki-OS-V1 non-canonical harvest items (partitions, sequencing_harness, far_endpoint) | OPEN — remains in fidelity ledger. |
| 10. Executive-Core post-IF-1 catch-up | OPEN — remains in fidelity ledger. |

## Current activity

- BUILD_STRATEGY.md ASSEMBLED. Chunk 4 complete at freeze. Awaiting owner response on 27 open fidelity-ledger items.

## Historical: recovery event · 2026-08-14T09:24Z (superseded by assembly notes above)

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. All Chunk-4 work post-recovery is documented in the assembly manifest at the top of this file.

## Ruling-2 effects on the item universe

Four WIRING items promoted (were folded); Part-1 item count 30 → 34, grand total 85 → 89.
- `WS-WIRE-CRITIC-INTO-ANSWERING` — critic_pass in-flight on the answering path (harvest lands code, wiring puts it in the request path).
- `WS-WIRE-PARITY-EXTENSION` — frozen-contract-snapshot parity discipline extended to every NEW contract this programme creates.
- `WS-WIRE-REFUSAL-FAMILY` — existing refusal-family taxonomy (`memory/memory_refusal_reasons.v0.json` + `memory/refusal.py`) wired to Canon 5 §9.2 refusal card surface.
- `WS-WIRE-LEDGER-MATRIX` — Northena ledger's sole-writer position promoted to Canon 9 §6-§18 record-matrix-governed writer.

Estimation discipline is now stranger-checkable (see Ruling 2 §1 in DECISIONS.md).
`WS-REBUILD-WORK-STUDIO-STORAGE` remains in Part 1 as a REBUILD row; its REVERSAL COST explicitly addresses user-data migration reversibility.
`fidelity_ledger.md` opens alongside Part 1 at `/app/assessment_workspace/notes/fidelity_ledger.md`; append during Part 2; freeze at BUILD_STRATEGY.md assembly.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — most reclassify to HARVEST or MODIFY (Part 1) with the Extraction-Akki donor page identified; Watch-related rows stay BUILD.
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.
- **Interface reclassification impact on item counts:** 13 Canon-5 items reclassified from Part-2 BUILD to Part-1 HARVEST/MODIFY, WS-BUILD-CONSOLE-WATCH stays Part-2 BUILD with new placement constraint, 11 Canon-5 items retain Part-2 BUILD status (no Extraction-Akki donor found). Part-1 total: 34 → 47 items; Part-2 total: 55 → 42 items. Grand total remains 89.

## Citation audit result at Part-1 close

Latest audit (post Orchestrator-Ruling-A remediation): **102/102 file citations verified · 854/854 canon citations verified · 0 failed.**

**Root cause of the initial drift (recorded per Orchestrator Ruling A):** Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for Part 2: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Doctrinal frame

- The four-test review discipline (Ruling 1 preamble) — every parameter of success is met by a named mechanism; quality discipline held exactly as canon; no build credit spent without survivable reason; nothing lands that canon does not keep. Every work item in Part 1 must satisfy all four tests.
- Canon 9 record matrix + task-identity register + handoff contract discipline — every item cites its record classes (as Canon-9 rows from `canon_9_requirements.md`) and its task identity, even though the register itself is BUILD.
- Canon 4 §32 quality matrix + Canon 3 §31 verification packs — every item states its QUALITY EVIDENCE against these.
- "Code complete" / "tests pass" are forbidden phrasings in Definition of Done (per owner instruction).

## Repos / SHAs / paths — see PINS.md
