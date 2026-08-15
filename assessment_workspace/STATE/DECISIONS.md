# DECISIONS.md — Append-only log of rulings received

Rulings are recorded verbatim, dated, in receipt order. This log is append-only.
Correction is by NEW ENTRY citing the corrected id, never by mutation.
Under Ruling 1's four-test discipline, an unlogged ruling is treated as
"not having lawfully happened".

---

## Ruling 1 · 2026-08-14 · Source: owner channel

**Verbatim:**

> "Your assessment is accepted and its rulings are issued. Before any build order exists, you will submit a complete build strategy — the full technical plan, at maximum detail — for review against four tests: every parameter of success in the canon is met by a named mechanism; the quality discipline holds exactly as the canon frames it; no building credit is spent without a reason that survives challenge; and nothing lands that the canon does not keep. The response to this submission will be your build orders.
>
> [Ruling 1, binding transition condition:] Executive's purpose enforcement is not stripped until the declaration check and the Watch's reconciler are demonstrated firing.
>
> [Scope:] One document, BUILD_STRATEGY.md, in the workspace and pushed to the repo beside the assessment. It covers every non-REUSE row — all MODIFY, RE-POINT, HARVEST, BUILD, RETIRE — each traced to its canon clause and its assessment row. REUSE rows appear only where wiring them to new work creates tasks of their own.
>
> [Prohibitions still in force:] no production code; no harvesting, re-pointing, or scaffolding; no canon edits."

**Binding effects:**

1. `BUILD_STRATEGY.md` is the immediate deliverable. Paper only. Reviewed against four named tests.
2. Executive-Core's `services/synisense/shield/purpose_validator.validate_purpose()` gate (Assessment §Claim 6 REFUTED-for-Executive-Core row) is RETAINED as canon-compliant until BOTH:
    - the actor-declaration check (Assessment C3-008 / C3-009 / C3-010) is demonstrated firing, AND
    - the Watch's reconciler (Assessment §5.8 cluster including Macho verdict shape + shared-record reconciliation per Canon 8 §14–§15 + Canon 9 §6 handoff `governance→Watch verdict`) is demonstrated firing.
    Once both fire, stripping becomes possible; until then the gate STANDS.
3. Every non-REUSE assessment row lands in the strategy — MODIFY, PARTIAL, RE-POINT, HARVEST, BUILD, RETIRE. Wiring-tasks for REUSE rows also land where new work creates them.
4. Every strategy item traces to its canon clause AND its assessment row.
5. Prohibitions remain: no production code, no harvesting-in-code, no re-pointing-in-code, no scaffolding, no canon edits.

**Owner Open-Question status shift:**
- OQ #1 (purpose-gate contradiction): **CONDITIONAL** — strip enabled by (declaration firing) AND (Watch reconciler firing).
- OQ #2 (admit-declaration seam): **ANSWERED (implicit)** — declaration check is confirmed BUILD by the transition condition. Chunk-3's C3-008/9/10 stays classified BUILD.
- OQ #3–#10: remain OPEN. Every remaining OQ moves into the fidelity ledger inside BUILD_STRATEGY.md.

---

## Ruling 2 · 2026-08-14 · Source: owner channel (response to five-point plan)

**Verbatim:**

> "Rulings on your five points — mostly your defaults, with two sharpenings:
>
> 1. Estimation anchor: (b) blended review-load + integration-surface count — BUT state the discipline once with hard, auditable thresholds (e.g., S = 1 component, 0 new contracts, ≤1 integration surface; M = 1-2 components or 1 new/changed contract; L = 3+ components, new register/console, or a data migration; XL = new engine/authority or estate-wide wiring). The classes must be checkable by a stranger, not vibes.
>
> 2. REBUILD class: keep WS-REBUILD-WORK-STUDIO-STORAGE in Part 1 as its own REBUILD row. It gates the RE-POINT completion and carries the 200+ real-user-export migration risk — it needs early review attention, and its REVERSAL COST field must address user-data migration reversibility explicitly (data migrations are the canonical cheap-to-build/expensive-to-reverse case).
>
> 3. WIRING: before finalizing your 7, verify these four aren't silently folded: (a) wiring critic_pass into the spine's answering path (the seam only counts when it's in the request flow); (b) extending the frozen-contract-snapshot parity discipline to every NEW contract this programme creates (Canon 9 registers, Watch verdict contract) — the parity seat is REUSE but each extension is wiring; (c) wiring the refusal-family registry to the Canon 5 refusal card surfaces; (d) wiring the Northena ledger's sole-writer position to the Canon 9 record matrix (ledger is REUSE, its promotion to matrix-governed writer is wiring). If any of these already exist as items, say where; if folded, promote them.
>
> 4. Fidelity ledger: draft notes/fidelity_ledger.md alongside Part 1, append during Part 2, freeze at assembly. It must include the 8 still-unanswered Open Questions plus anything new.
>
> 5. CONTRADICTION: own row, agreed — WS-CONTRADICTION-PURPOSE-GATE is the natural home of the Ruling-1 transition window; its DoD is the demonstrated-firing evidence (declaration check + Watch reconciler) that lawfully permits the strip, and it must cross-reference WS-BUILD-DECL and WS-BUILD-WATCH-RECONCILER as gating dependencies.
>
> Proceed. Update STATE/ (CONTEXT.md + NEXT.md, and append this ruling to DECISIONS.md) before drafting. Then deliver Part 1 per the original brief's five outputs."

**Binding effects:**

1. **Estimation discipline hard thresholds (stranger-checkable):**
    - **S** = 1 component, 0 new contracts, ≤1 integration surface.
    - **M** = 1–2 components, OR 1 new/changed contract, ≤2 integration surfaces.
    - **L** = 3+ components, OR new register/console, OR a data migration.
    - **XL** = new engine/authority, OR estate-wide wiring.
    Every XL carries a one-paragraph defence field. Class is DECIDED per-item on those criteria alone — no vibes.

2. **WS-REBUILD-WORK-STUDIO-STORAGE stays in Part 1**, own REBUILD row. REVERSAL COST must state user-data migration reversibility explicitly (cheap to build, expensive to reverse — the canonical case).

3. **Four WIRING items promoted** — verification result (grep against Extraction-Akki HEAD `b150c21`):
    - (a) `critic_pass` **ABSENT** in Extraction-Akki spine (only in Akki-OS-V1 per Chunk 1 cross-repo). Answering surfaces (`chat/`, `documents/`) contain **zero** `critic_pass` references. Wiring is silently folded inside WS-HARVEST-CRITIC-SEAM. → **PROMOTED to `WS-WIRE-CRITIC-INTO-ANSWERING`** (separate item; harvest lands the code, wiring puts it in request flow).
    - (b) Parity-seat pattern **present** as `tests/invariants/test_invariant_contract_snapshots.py` + 10+ frozen-shape invariants. Extending to NEW contracts (Canon 9 handoffs, Watch verdicts, Task Identity Register) is folded. → **PROMOTED to `WS-WIRE-PARITY-EXTENSION`**.
    - (c) Refusal-family registry **present** as `services/memory/memory_refusal_reasons.v0.json` + `services/memory/refusal.py`. Canon 5 refusal card (§9.2) is a new UI surface. Wiring the taxonomy to that surface is folded inside WS-BUILD-REFUSAL-CARD-COPY (Part 2 BUILD). → **PROMOTED to `WS-WIRE-REFUSAL-FAMILY`** (WIRING; separate from the BUILD of the card itself).
    - (d) Northena ledger sole-writer **present** at `services/northena/ledger.py:63` `record()` with `insert_one`. Promotion to Canon 9 §6-§18 record-matrix-governed writer (i.e., ledger claims writer role for `Ledger.Row` class in matrix, all reads route through matrix reader-list) is folded. → **PROMOTED to `WS-WIRE-LEDGER-MATRIX`**.

    Part-1 WIRING count updates from 7 → 11. Total Part-1 items 30 → 34.

4. **`notes/fidelity_ledger.md` opens alongside Part 1**, appended during Part 2, frozen at BUILD_STRATEGY.md assembly. Seed contents: OQ #3, #4, #5, #6, #7, #8, #9, #10 (Ruling 1 answered #1 conditional + #2 implicit), plus every un-fillable field surfaced in item drafting.

5. **`WS-CONTRADICTION-PURPOSE-GATE`** — DoD is the demonstrated-firing evidence pair (declaration check + Watch reconciler). Cross-references `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` as gating dependencies. Retain-until-strip is the transition window; ledger the strip event separately.

---

## Ruling 3 · Instruction 02 · 2026-08-14 · Source: owner channel (interface strategy directive, additive)

**Verbatim:**

> "The owner has fixed the interface direction: governance and security control surfaces render as app tiles under the Admin surface's tile-grid-plus-detail-card grammar (reference screenshot to follow in the workspace). Your build strategy's interface section must plan Extraction-Akki's frontend as the donor, repurposed — not rebuilt — into this grammar: produce a menu-to-app mapping table (every existing Extraction-Akki page/menu → its app tile, group, and canon identity, or → RETIRE with reason), and classify the repurposing per component as HARVEST or MODIFY with the usual seven fields. The Watch renders as a fourth group of four app tiles (State, Record, Under Watch, Decisions per Canon 8 §13), gated by watch-officer role, sessions under Watch identity per Canon 9 — never nested under Trust Center — and remains BUILD. Label-versus-identity mappings land in your canon fidelity ledger as rendering decisions. Update STATE/ on receipt."

**Binding effects:**

1. **Donor is fixed as Extraction-Akki frontend** (not the prototype, not Executive-Core, not new BUILD). The Extraction-Akki frontend inventory (44 production pages across 12 menu groups + 10 shell/component files, verified by direct `find` at HEAD `b150c21`) is the donor set. Every Extraction-Akki page/menu appears in a mapping table with three columns: app tile · group · canon identity; OR is classified RETIRE with reason.
2. **Grammar is fixed as tile-grid-plus-detail-card** (the "Admin surface" grammar). Reference screenshot has not yet arrived in the workspace — recorded as a named dependency; fixture-pending field on every interface item.
3. **Interface work items reclassify from BUILD to HARVEST or MODIFY** per component, with all seven fields. Reclassification count follows in `notes/strategy_items_part1.md` §I. This partially supersedes Chunk-3 §5.7 framing where Canon-5 interface rows defaulted to BUILD.
4. **Watch Console EXCEPTION.** The Watch remains BUILD: a fourth group of four app tiles named `State`, `Record`, `Under Watch`, `Decisions` per Canon 8 §13. Gated by watch-officer role, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center.** The placement constraint is encoded in the item's Definition of Done.
5. **Label-versus-identity rendering decisions land in `notes/fidelity_ledger.md`** as `RENDERING DECISION` rows (not silent renames). This includes: prototype's "Trust Center"/"Shield" naming vs Canon 5's console identities, "WorkStudio" vs "Work", "ThinkLab/Monitor" placement under Lead, and every Extraction-Akki page label that does not carry its Canon-5 identity in the tile.
6. **Extraction-Akki §5.7 rows previously BUILD are now split**: Watch-related rows stay BUILD (Part 2); all other Canon-5 rows with an Extraction-Akki donor page reclassify to HARVEST or MODIFY (Part 1).

---

## Orchestrator Ruling A · 2026-08-14 · Source: orchestrator (citation drift remediation)

**Verbatim (paraphrased directive):**

> "Citation drift (FL-P1-20): remediate NOW, before Part 2. This is a quality defect, not a governance question — the owner's standard is a zero-failure citation audit, and 40 failed canon anchors would sink the submission. Do a systematic re-mapping: for each of the 40 drifted `Cn-0MM (§XX)` anchors, re-open the extracted canon text, find the REAL heading (by title match, since substance is grounded in heading titles), and correct the numeric anchor in row_to_item_index.md, the domain files, and strategy_items_part1.md. Rules: (a) every correction is a re-read, never a guess; (b) if a row's true anchor genuinely cannot be located by title, it stays failed and gets its own fidelity-ledger row naming exactly what was searched; (c) keep FL-P1-20 as the record of the drift AND its remediation — the defect history is part of the honest record; (d) re-run the citation audit and report the new numbers. Root-cause one line in CONTEXT.md: how did Chunk-1 extraction mint §-numbers beyond the heading span (likely sub-paragraph counting) so Part 2 doesn't repeat it."

**Binding effects:**
1. All 40 failed canon anchors re-mapped to real `[Heading]`-numbered sections by TITLE match against the extracted canon text; corrections propagate to `row_to_item_index.md`, `domain_5_*.md`, `retire_inventory.md`, `shaping_answers.md`, `strategy_items_part1.md`, `canon_[3-9]_requirements.md`, and `fidelity_ledger.md`.
2. Any row whose title match FAILS keeps `§XX-DRIFTED` marker and gets its own fidelity-ledger entry naming exactly which titles were searched and which returned no match.
3. FL-P1-20 stays open as the record of the defect AND its remediation trail — history is part of the honest record.
4. Root cause recorded in `CONTEXT.md`.
5. Citation audit re-runs; new numbers appear in `NEXT.md` + `CONTEXT.md`.

## Orchestrator Ruling B · 2026-08-14 · Source: orchestrator (Part 2 + strategy sections)

**Verbatim (paraphrased directive):**

> "Part 2 proceeds now. The owner asked for ONE complete submission, not incremental sign-offs; waiting on Part-1 shape approval would cost the round trip the owner told us to avoid. Draft the 42 BUILD items (148 canon rows) with all seven fields, same discipline. Specific requirements: (1) the Watch's 60 rows and Mkondo's 45 rows will dominate — bundle honestly (a work item per canonical mechanism, e.g., reconciler, mark registry, verdict contract, policy-table executor, response arms, mirage, signature store, attestation+witness, drill harness, Watch Console — not one mega-item per canon); (2) WS-BUILD-DECL and WS-BUILD-WATCH-RECONCILER carry the Ruling-1 transition linkage explicitly; (3) the two ports (streaming, object storage) appear as their own items if they aren't already, since multiple items gate on them — resolve FL-P1-03's placement question with a proposed answer marked as PROPOSAL, leaving the ledger row open for owner ratification; (4) every item that creates a NEW contract references WS-WIRE-PARITY-EXTENSION as a dependency. Unchanged: screenshot fixture still pending (keep FIXTURE PENDING, do not invent); unresolved rendering decisions (Use-Data landing, Verdict Demo) stay as fidelity-ledger questions for the owner. After Part 2: strategy-level sections (proposed sequence with dependency logic; transition windows named + guarded, T1 = Ruling 1; no-regression contract listing standing invariant tests + missing ones to write first; waste register; freeze the fidelity ledger), then full completeness audit (every non-REUSE row exactly once, seven fields per item — mechanical check), citation audit at zero, cold-read recovery test of STATE/, assemble BUILD_STRATEGY.md, git-commit locally beside REUSE_ASSESSMENT.md (push waits on owner's remote+token). Update STATE/ at each step."

**Binding effects:**
1. Part 2 (42 BUILD items, 148 canon rows) drafts NOW with same seven-field discipline. Bundle by canonical MECHANISM (reconciler, mark registry, verdict contract, policy-table executor, response arms, mirage, signature store, attestation+witness, drill harness, Watch Console) rather than one-mega-item-per-canon.
2. `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` carry Ruling-1 transition linkage explicitly in their WHAT / DEPENDENCIES / DoD fields.
3. Two ports get standalone BUILD items: `WS-BUILD-STREAMING-PORT` (from harvested `synisense/shield/streaming.py`) and `WS-BUILD-OBJECT-STORAGE-PORT` (proposal resolves FL-P1-03: new engine BUILD, XL). FL-P1-03 stays OPEN pending owner ratification.
4. Every item that creates a NEW contract lists `WS-WIRE-PARITY-EXTENSION` as a dependency.
5. Fidelity ledger keeps: screenshot pending (FL-P1-14); Use-Data placement (FL-P1-10); Verdict Demo classification (FL-P1-11); Chunk-1 row-extraction re-audit (FL-P1-20).
6. Post-Part-2 sections: (a) proposed sequence + transition windows T1..Tn (T1 = Ruling 1 gate); (b) no-regression contract listing all existing invariant tests + missing ones to write; (c) waste register (things reversed / abandoned / duplicated in the strategy); (d) fidelity ledger frozen at assembly.
7. Completeness audit: mechanical script confirms every non-REUSE canon row appears in exactly one item and every item has all seven fields.
8. Citation audit must return zero after remediation.
9. Cold-read recovery test: a stranger reading STATE/ can resume execution.
10. `BUILD_STRATEGY.md` assembles from strategy_items_part[12].md + strategy-level sections + STATE + fidelity ledger.
11. Git-commit locally beside REUSE_ASSESSMENT.md; push waits on owner's remote + token.

---

## Orchestrator Ruling C · 2026-08-14 · Source: orchestrator (self-contained assembly directive)

**Verbatim (paraphrased directive):**

> "One correction before I submit to the owner — this is a compliance defect against the instruction's letter, not a content problem. The owner's §1 says 'One document, BUILD_STRATEGY.md' that 'covers every non-REUSE row... each traced to its canon clause and its assessment row,' and §6 says 'the whole document is precise enough that build orders can be issued against it by item reference.' A 232-line index cross-referencing four notes files makes the reviewer assemble the submission themselves — that is exactly the kind of gap that becomes a costed question. FIX: Assemble BUILD_STRATEGY.md as ONE SELF-CONTAINED document by inlining the full content in this order: (1) Method & submission attestations ... (2) The complete 47 Part-1 items ... (3) The complete 55 Part-2 items ... (4) Proposed sequence with reasons ... (5) Transition conditions ... (6) No-regression contract ... (7) Waste register ... (8) Canon fidelity ledger ... (9) Appendix: row-to-item index ... The notes files stay on disk as working papers, but the submission document must stand alone. Then: re-run citation + completeness audits against the assembled BUILD_STRATEGY.md ... update STATE/ (CONTEXT.md posture, NEXT.md), and make a new local commit."

**Binding effects:**
1. **`BUILD_STRATEGY.md` is now SELF-CONTAINED** at 2442 lines / 244 KB. Every item, every table, every field is inlined verbatim from its working paper.
2. **Working papers in `notes/` remain on disk** as the review trail — not the submission itself.
3. **Section order in the assembled document** matches the owner's §1-§9 numbering literally: (1) Method + attestations, (2) full Part-1, (3) full Part-2, (4) sequence, (5) transitions, (6) no-regression, (7) waste, (8) fidelity ledger, (9) appendix row-to-item index. Estimation discipline and rulings stated once at §2-§3.
4. **Attestations stated explicitly in the document** per the owner's §1 requirement: STATE/ is live, cold-read test performed, audit numbers reported, pinned SHAs listed. Presence verified by inspection of §1 of the document.
5. **Audits re-run against the assembled document.** Citation audit now scans `BUILD_STRATEGY.md` in addition to notes/. Completeness audit now validates 7-field discipline against the inlined form in `BUILD_STRATEGY.md`. Results at v1.1 commit: 104/104 file · 1778/1778 canon · 0 failed; completeness PASS.
6. **Assembly tool** at `tools/assemble_build_strategy.py` is idempotent — re-running produces byte-identical output as long as working papers are unchanged.
7. **STATE/ updated:** CONTEXT.md notes v1.1 posture; NEXT.md updated with the new commit + audit numbers.
8. **New local commit issued.**

---

## Build Order 01 · 2026-08-14 · Source: owner channel · Log verbatim

**Verbatim:**

> "Build Orders — Strategy Accepted · Rulings Issued · Execution Authorized
>
> In response to: BUILD_STRATEGY.md @ 42b241c. This message is the build order. Log it verbatim in DECISIONS.md. Attached with it: the reference screenshot (clears FL-P1-14), Akki_Prototype_v7_Design_Brief.md (binding interface fixture), and AISCA_GPU_Access_Guide.pdf (compute provisioning SOP — new scope, §6 below). Push destination, write token, and my egress IPs follow in the secure channel; nothing else waits on them except the push itself and VM creation.
>
> **1 · Verdict against the four tests**
> Test 1 — PASS. 591 rows → 102 items with row-level traceability; orders below are issued by item reference. Test 2 — PASS. The tests-first discipline — 20 standing invariants held, 40+ new invariant tests written before the items they gate — is now binding: no item lands before its gating test exists and fails for the right reason. Test 3 — PASS, with one amendment (Studio, §4) removing the largest deferrable spend. Test 4 — PASS. The fidelity ledger did its job — 27 questions surfaced instead of 27 silent decisions. The citation-drift disclosure and remediation are accepted; FL-P1-20 stays on the record as handled.
>
> Three corrections in your first commit (document defects, no ceremony): (1) §10.F still reads 'Part 2 has not been drafted yet' — replace the stale placeholder with the actual Section F entries. (2) The guardrails say 'Nine XL items' and list seven — reconcile count and list. (3) FL-OQ-04's premise ('Canon 5 §10 lists four consoles') contradicts Canon 5 as shipped, whose §10 reads 'exactly five consoles' with the Watch row in the console table — re-verify your Canon 5 extraction around Part VII-A (its §34-A/B/C headings likely broke your heading parse) and re-run the citation audit if the extraction changes.
>
> **2 · Ruling sheet — all 27 rows CLOSED**
>
> Log each with the sentence below as the ruling text.
>
> A — inherited open questions. FL-OQ-03: Both — re-verified is a runtime state in the ceremony state machine and a compliance-artifact write, and the state transitions only on the artifact's successful write. FL-OQ-04: Five consoles; the Watch Console is the fifth in canon and renders as the fourth tile group on the Admin surface — 'four-plus-Watch' and 'five' are the same fact. FL-OQ-05: Studio does not ship this cycle; WS-BUILD-STUDIO leaves Wave 8 for a later cycle and its nav presence renders in the dormant-state grammar, never a dead link. FL-OQ-06: Both counts stand because they count different things — the Eight Global Rules are Canon 5's interface law, the Four Classes are Canon 3's governed-value taxonomy, and the Rulebook surface's invariant counts rules in force per instance (seeded: four), never a canon constant. FL-OQ-07: Cohort fully retires from the platform; if it returns, it returns as an application on the boundary like any third party, outside this programme. FL-OQ-08: Shadow-write-then-cutover with guards G-T3-A…D exactly as written; I sign the commissioning certificate before reader-cutover, and not before all 200+ export hashes are listed on it. FL-OQ-09: Harvest into the spine; Akki-OS-V1 becomes read-only reference at Wave-4 completion. FL-OQ-10: Executive-Core becomes an application on the boundary; nothing is maintained parallel after T2's exit; only what RETIRE names is archived.
>
> B — Part-1 field-level. FL-P1-01: Focused read at Wave-4 preparation; harvest only what Targeta and Mtafiti don't already satisfy, and on full overlap reclassify to RETIRE and log the waste. FL-P1-02: Default path A — RE-POINT through the input seat; path B only if the focused read proves a second custody path that cannot transit the chokepoint; that read is now urgent (§6). FL-P1-03: The object-storage port is its own BUILD item — a port under the boundary governor's ownership, not a new engine and not absorbed into the record matrix — contract through parity-extension as planned. FL-P1-04: A discrete milestone — T2's exit is the single completion criterion, verified by the Canon 1 §12 boundary audit. FL-P1-05/06/07: The three focused reads execute as the first task of each item's wave; WHAT-fields update in place; no build on those items before the read lands.
>
> C — rendering decisions. Governing principle for the whole section: the organisation's language renders on screen; the canon identity lives beneath; the mapping is recorded in this ledger. A label is never evidence of identity, and identity never forces a label. FL-P1-08: Ratified — memory-plane observability homes to the Compliance Console. FL-P1-09: Ratified — trace receipt homes to the Compliance Console's prove-one-run export. FL-P1-10: Use-Data landing homes to the Ask reference application (Canon 5 §43–§44); the model catalogue is the Extraction Console's. FL-P1-11: Verdict Demo retires; the walk pattern in the attached brief supersedes it. FL-P1-12: Ratified — audit trail homes to the Compliance Console export. FL-P1-13: Ratified — one canonical change-a-rule tile; the duplicate retires. FL-P1-14: CLOSED — the fixture is the attached screenshot plus the attached v7 brief; every FIXTURE PENDING clears on their arrival in the workspace. FL-P1-15 — OVERTURNED: 'Trust Center' is kept as the rendered group label, mapped to the Compliance Console identity — the reference screenshot fixes this label; record the mapping and move on. FL-P1-16 — OVERTURNED: The shield names (Data Shield · Reasoning Shield · Access Shield) are kept as rendered tile labels mapped to their canon identities per the brief's §4 table, same reason, same authority. FL-P1-17: Ratified — 'WorkStudio' renames to 'Work.' FL-P1-18: Ratified — ThinkLab and Monitor reparent under Lead. FL-P1-19: Ratified — the capability is the Integration Console plus catalogue; the on-screen tab may remain '3rd Party Apps' as org language, mapping recorded.
>
> D. FL-R1-01: The strip executes as a Canon 3 §24 rule-change ceremony — it is a rule change and the ceremony's visibility is the point; the Watch's role is witness, and the two drill attestations attach to the proposal as its evidence, not its mechanism.
>
> E. FL-P1-20: Remains on the record as handled; reopen only if a title-match is refuted.
>
> **3 · The interface fixture is binding, not illustrative**
> The attached brief carries three things every interface item now inherits as acceptance criteria: the tile-grid-plus-detail-card grammar from the screenshot; rule zero — every surface leads with plain sentences answering what's happening, how do we know, what are we doing about it, is what we agreed being done, with engineering measures (latencies, percentages, parameter codes) one tap behind 'see the working,' never on the officer's reading; and verbatim seeded copy — copy language from the brief rather than inventing it. Add a per-surface rule-zero invariant check (test_four_questions_topline_present or equivalent) to the new-invariants list for console items. Watch Console items consume the brief's §6 verbatim — four panels, plain-language walk card names, the seeded scenario.
>
> **4 · Sequence ratified, then re-cut by priority**
> The 11 waves are ratified as proposed — registers-first, tests-first, Wave-10 last under Ruling 1 — with two amendments: WS-BUILD-STUDIO leaves Wave 8 (dormant rendering folds into WS-BUILD-FIVE-PILLARS), and the brief binds Waves 7–9 per §3 above.
>
> Then this priority re-cut supersedes the wave order where they conflict: the estate goes live-capable first — data ingesting, models training, GPU capacity connected, and the surface to operate all three — while the remainder builds behind it.
>
> Track A — Live Estate, in this order:
> A0 · Thin register kernel. WS-WIRE-PARITY-EXTENSION whole. WS-BUILD-RECORD-MATRIX + WS-BUILD-TASK-IDENTITY-REGISTER at thin scope — only the record and task classes the live path touches (ledger rows, receipts, census, declarations, ingestion and training artifacts). Full scope completes in Track B. The thin kernel is the floor nothing live may bypass.
> A1 · Declaration. WS-BUILD-DECL + WS-WIRE-CUSTODY-DECL, tests-first. No live actor — human, agent, or connector service — enters undeclared. This banks Ruling-1 precondition (a) early.
> A2 · Ingestion live. Live sources through the existing admission → custody → extraction spine: connect/data-source services, WS-WIRE-ADMISSION-HANDOFF, WS-WIRE-LEDGER-MATRIX, plus the Wave-4 harvests the live path needs (batch quarantine, partitions, registry-context). No ingestion path bypasses admission — even temporarily, even for backfill.
> A3 · Compute and training — grounded in §6 below.
> A4 · Operating surface. Only what operating the live estate requires: shell grammar, component/refusal/chip harvests, the tiles Connect, Data Estate, Models, Compute, and the minimal Work pillar — under the fixtures. All other interface work waits.
>
> Track B — opens the moment A2 has live data: WS-BUILD-WATCH-FOUNDATION first (live data raises the target value; the Watch does not drift), then the remaining ratified waves. The three sign-off stops are unchanged: T2 close, T3 reader-cutover certificate, Wave-10 strip. T1's guard holds throughout — the purpose gate stands until both demonstrations fire.
>
> **5 · Standing rules for the re-cut**
> Tests-first applies to every Track-A item identically. No live-path shortcut ever lands with a promise to harden later — if it must be done for quality, it is done whole. Anything in A2–A4 that tempts a bypass of the thin kernel is a stop-and-ask, never a workaround.
>
> **6 · A3 grounded: the first live workload, environment confirmed, provisioning is GO**
> 24-week programme — ~30 TB broadcast archive processing/classification, fine-tuned speech models for select Kenyan broadcast languages with measured accuracy benchmarks, archive-scale transcription corpus; targets confirmed at two-week checkpoint, reflected in Mid-Term Report, proposed as Canon 4 §33 quality-matrix rows (correctness, loss, precision, attribution).
>
> Environment: one VM via AISCA Rafay console — 4× H200 NVLink, 84 vCPU, 948 GB RAM, 12 TB local ephemeral, Ubuntu 24.04, SSH per SOP. Vendor answers on record: routine restart does NOT wipe ephemeral (deprovisioning is the loss event; pre-deprovision check: nothing on ephemeral unreproduced); ~30 TB persistent HSS volume shared to the organisation — HSS cannot be attached after VM creation, selection at creation is the go/no-go.
>
> Four bindings: (1) VM inside the boundary — declared infrastructure actor at admission the moment A1 lands (objective: archive processing and training; capabilities: compute, HSS, GPU training; risks: bulk data custody, external location); until then default-restrictive with access events logged for retroactive ledgering; access path is a registered handoff; every training run admitted and ledgered; every artifact returns hash-registered; no second perimeter, no custody exception. (2) Storage layout fixed — raw archive + durable working set on 30 TB HSS; ephemeral is scratch only, nothing durable ever; records/receipts/ledger stay in the estate proper; VM holds compute state, never the record. (3) Access hardening precedes data — key-only SSH, password auth disabled and confirmed dead by external probe, bootstrap credentials retired, allowlist pinned to owner egress IPs /32, private key under named custody never in chat/docs/STATE. (4) A2 and A3 fuse — archive transfer is A2's first live ingestion, crosses admission with declared basis, lands under thin-kernel record classes; audio custody follows FL-P1-02 path A unless focused read proves otherwise; read due Phase 2.
>
> Execute now — Phase 0, today: pre-flight (HSS visible ~30 TB, smaller = stop-and-escalate) → provision per SOP with bindings (4× H200; HSS at creation; public IP true; SSH allowlist on receipt of IPs) → credential hardening → acceptance before any data moves, ledgered as commissioning record: HSS mounted ~30 TB writable; write-test survives one deliberate restart; nvidia-smi shows 4× H200 NVLink active; ephemeral present scratch-only; password auth probed dead. Pin 'two weeks from provisioning day' in STATE/PINS.md as checkpoint-targets deadline. HSS fail or NVLink absent: stop and escalate, never adapt.
>
> Phases: Phase 1 (A0+A1) thin kernel + declaration tests-first, declare the VM; deliverable: A0-A1 report with drill receipts, declaration-refusal demonstrated firing. Phase 2 (the slice): hash manifest of archive source before first byte moves; admit a representative slice (few hundred hours audio) end-to-end — admission → custody → transfer to HSS → manifest verification → processing → GPU training smoke-test → artifacts hash-registered back; FL-P1-02 focused read lands here; deliverable: slice report — timings, throughput, GPU utilisation, first evidence-based draft of checkpoint targets as quality-matrix rows. Phase 3 (A3 addendum): full compute plan, seven fields per item, priced from slice's measured numbers — bulk-transfer plan for ~30 TB, training-runner design (single-node 4-GPU NVLink profile, no cluster scheduler this cycle), job queueing + metering into economics, proposed checkpoint targets, operations runbook with restart/deprovision semantics verbatim; deliverable: addendum for ratification before bulk spend. Phase 4 (on ratification): bulk ingestion as ledgered runs; training live against the ladder, admitted, receipted, metered; deliverable: ingestion-complete + first training-cycle report. Phase 5 (A4, overlapping): operating surface under fixtures, seeded by real workload — Compute tile's four questions answered by real node, real jobs, real spend; deliverable: surface report with rule-zero checks passing. Phase 6 (Track B): Watch foundation the moment Phase 2 has live data; then ratified waves.
>
> **7 · Reporting and stops:** one report per phase in named deliverable shape — receipts, not narrative — plus waste-register deltas and re-opened ledger rows. Escalate-and-stop, never adapt, on: HSS absent/undersized; NVLink absent; thin-kernel bypass temptation; conflict between governing artifacts; durable state on ephemeral or record on VM. On receipt of push token: push assessment, strategy, this order, and STATE/ in first push.
>
> **8 · Done means:** all 27 rows logged CLOSED; three corrections committed; fixtures in workspace and FIXTURE PENDING cleared; Phase 0 commissioned and ledgered; A0-A1 landed tests-first with declaration drill banked; slice run end-to-end with checkpoint targets drafted from evidence; addendum ratified and bulk ingestion underway; operating surface live on real data under rule zero; Watch foundation started — STATE/ current enough that a cold replacement continues without a question."

**Binding effects (this cycle):**
1. **Production-code prohibition LIFTED** for items on branch `programme/track-a` in the Extraction-Akki clone. All other prohibitions stand.
2. **All 27 fidelity-ledger rows CLOSED** with the exact ruling sentences above (see `fidelity_ledger.md`).
3. **Three corrections** in the first execution commit: §10.F stale placeholder → actual entries; XL count 9→7 with reconciled list; Canon 5 §10 re-verified — canon text substantively says "exactly five consoles" with Watch as the fifth (the extraction parse handled §34-A/B/C correctly; premise of FL-OQ-04 was a paraphrase error, not a parse error; no audit re-run needed).
4. **Phase 0 support materials** at `/app/assessment_workspace/phase0/` — commissioning_checklist.md, acceptance.sh, commissioning_record_template.md — the VM console itself is HUMAN-EXECUTED (owner runs Rafay console + acceptance.sh on the VM).
5. **CRITICAL GAP RECORDED:** the three attachments (reference screenshot, `Akki_Prototype_v7_Design_Brief.md`, `AISCA_GPU_Access_Guide.pdf`) referenced in the order did NOT arrive in the workspace — re-upload requested. Per the order's own text "every FIXTURE PENDING clears on their arrival in the workspace," FL-P1-14's substantive closure remains **conditional-CLOSED-pending-attachment-delivery**. Fixture-bound work (A4 operating surface, Track-B console items, Watch Console §6 verbatim consumption) is BLOCKED until they land. **Nothing in A0-A2 is blocked.**
6. **Branch `programme/track-a` created** in the Extraction-Akki clone. Pinned baseline SHA `b150c21` preserved — all new work is commits on top; nothing is rewritten.
7. **Phase 1 (A0+A1) executes tests-first:** for each Track-A item the gating invariant test is written FIRST, run FIRST, right-reason failure captured FIRST, then implementation. Declaration-refusal must be demonstrated firing with a drill receipt — this banks Ruling-1 precondition (a).
8. **VM as infrastructure actor:** declaration entry shape drafted (objective: archive processing and training; capabilities: compute, HSS, GPU training; risks: bulk data custody, external location) — the actual declaration executes when the VM exists.
9. **STATE/ updates at every step** — CONTEXT.md posture, NEXT.md scope, PINS.md checkpoint placeholder.
10. **Push waits on push destination + write token** delivered via secure channel.

---

## Owner Clarifications on Build Order 01 · 2026-08-14 · Source: owner channel

**Verbatim:**

> "Owner responses — three scope updates (append to DECISIONS.md as owner clarifications, dated 2026-08-14):
>
> 1. NO PUSH. No push credentials will be provided. Everything stays as local commits; we surface only what we cannot do. Remove push steps from NEXT.md; the local git history IS the record.
>
> 2. VM ACCESS WILL BE GRANTED TO US. The owner will provide credentials for the estate to connect to the GPU VM over SSH + IP. So in addition to the Phase-0 human-run materials, BUILD THE SEAM: everything needed so that when SSH credentials + host IP arrive, the connection is a first-class governed handoff, not an ad-hoc shell. Concretely, on the programme/track-a branch: (a) a compute-seam connector service (registered handoff per the thin kernel — the VM is a declared infrastructure actor; every session/command run through the seam is admitted, ledgered, and receipt-stamped; artifacts return hash-registered); (b) remote execution of acceptance.sh through the seam so Phase-0 acceptance can be run by us once credentials land; (c) key custody: keys will arrive as env/secret material — design for a key file path + config in backend/.env, never hardcoded, never committed, never in STATE/; (d) a script that reports this pod's public egress IP (curl-based) — the owner must allowlist OUR egress IP on the VM, so we need to hand it to them; run it and include the IP in your reply so I can pass it on; (e) connection preflight (ssh -o BatchMode) + failure taxonomy (refused/timeout/auth) so credential problems surface as clear findings. Tests-first applies: the seam's gating invariants (no unledgered command execution path, artifact-return hash verification) are written and failing-for-the-right-reason before implementation.
>
> 3. ATTACHMENTS INCOMING. The three fixtures are being re-uploaded now; they may arrive in my next message. Until then FIXTURE PENDING stands; keep fixture-bound work parked.
>
> Continue the current cycle (corrections commit + 27 closures + Phase 1 A0/A1 tests-first) as ordered; fold the seam work into Phase 1 scope after A0/A1 gating tests exist. Same reporting deliverable as before, plus the pod egress IP."

**Binding effects:**
1. **No push.** Push destination expectation retired from `NEXT.md`. Local git history on `programme/track-a` IS the record. Rebasing / rewriting `b150c21` prohibited.
2. **Compute seam is now Phase-1 scope** (folded after A0/A1 gating tests exist — condition satisfied). New WS item scope for this cycle:
    - **`WS-BUILD-COMPUTE-SEAM`** (M–L) — `services/compute_seam/` connector. VM is a declared infrastructure actor (Build Order 01 §6 declaration shape already tested in `test_admit_refuses_undeclared_actor.py::test_infrastructure_declaration_shape_for_vm`). Every session/command through the seam is admitted (declaration check), ledgered (LedgerRow), receipt-stamped (outer-gate receipt), artifacts hash-registered on return.
    - Registered handoff shape: `compute.remote_exec.per_command` task identity + `Handoff.Contract` writer role (thin-kernel extension: adds `Compute.Command` to matrix as writer=`services.compute_seam`, readers=admit + ledger + Compliance Console).
    - `acceptance.sh` executed through the seam (not ad-hoc SSH) — establishes Phase-0 acceptance as a ledgered event.
    - Key custody: `SSH_PRIVATE_KEY_PATH` + `VM_HOST` + `VM_USER` + `SSH_ALLOWLIST_EGRESS_IPS` in `backend/.env` (never hardcoded, never committed, never in STATE/).
    - `tools/report_egress_ip.sh` runs curl against 4 independent IP-reporting services and outputs the pod's public egress IP.
    - Preflight: `ssh -o BatchMode=yes -o ConnectTimeout=5 -o PasswordAuthentication=no` — returns typed failure (refused / timeout / auth-denied / host-unknown) as governance-facing verdict.
    - Tests-first gating invariants:
        - `test_compute_seam_no_unledgered_exec.py` — no code path executes a remote command without writing a LedgerRow first.
        - `test_compute_seam_artifact_hash_verified.py` — every artifact returning from the VM carries a hash that matches its content.
3. **Pod egress IP recorded** in this cycle's reply and in `STATE/PINS.md`: **`34.16.56.64`** (verified via ifconfig.me, icanhazip.com, api.ipify.org, checkip.amazonaws.com; no IPv6 egress). Owner must allowlist this /32 on the VM.
4. **Attachments still not delivered** as of this clarification receipt. FIXTURE PENDING stands; A4 operating surface, Track-B console items, Watch Console §6 verbatim consumption stay BLOCKED. Nothing in A0-A3 is blocked. FL-P1-14 substantive-closure remains conditional.
5. **NEXT.md updated** — push steps removed; local-history-is-the-record posture stated explicitly.


---

## Owner Ruling on FL-P2-03 + FL-P2-04 · 2026-08-14 · Source: owner channel · Log verbatim

**Verbatim:**

> "FL-P2-03 — CLOSED, with the discrepancy explained and the freeze upheld. Your reading of the PDF is correct and the reconciliation finding is valid: the guide documents only the 1× H200 SKU. The explanation is provenance, not error: the PDF is the vendor's procedural onboarding SOP — how to click through Rafay — written around their catalogue's default single-GPU offering. The 4× H200 / 84 vCPU / 948 GB / 12 TB environment is vendor-confirmed in direct correspondence outside that document — the vendor's words on record: they accept 'the single-node shape as shown: 4× H200, 84 vCPU, 948 GB RAM, 12 TB local storage,' they confirmed a routine restart does not wipe the ephemeral tier (only deletion/deprovisioning does), and they have shared the ~30 TB HSS volume to the organisation — which you should be able to verify independently right now: it should be visible in the org's High Speed Storage section in the console. That visibility check is your first action under this ruling, and its result decides the path: If the HSS volume is visible at ~30 TB: proceed into the console per the SOP's procedure (the click-path is valid regardless of SKU) and check the Virtual Machines Catalog for a 4× H200 entry — the vendor accepting the shape implies it is provisioned through the same portal, either as a catalogue entry visible to the org or enabled vendor-side for it. If the 4× SKU appears: provision per §6, checklist unfrozen for that execution only. If the HSS is not visible, or the catalogue shows no 4× SKU: stop stands. Report the exact console state (screenshot-grade: what the catalogue lists, what HSS shows) and I take it to the vendor — that becomes a vendor-side action or an updated guide, not something you adapt around. Either way: the Phase-0 checklist and acceptance.sh stay frozen at the §6 spec. The 1× SKU is not a fallback, not a bridge, not a 'start small while we sort it' — a single-GPU machine cannot carry the committed workload, and provisioning it would spend contract term and create a machine we'd deprovision. The §6 spec is what the vendor confirmed; anything less on screen is an escalation, not an option.
>
> FL-P2-04 — CLOSED: path (a). You execute the hardening through the compute seam. Reasoning on the record: option (b)'s virtue is that the password never transits, but its cost is an unattested manual act at a console — hands outside the estate, no receipt, no drill, no replay. Option (a) puts the hardening inside the discipline everything else lives under: your module executes it, the sequence is ledgered, the external probe proving password-auth dead is the acceptance evidence, and the bootstrap credential's entire life is minutes between handover and retirement. A short-lived secret with an attested death beats a never-transited secret with an unattested procedure. Conditions binding path (a): the bootstrap credential transits this channel once, is used only by the hardening module, is retired within the same session, and never lands in STATE/, logs, or any file; the module's run writes the commissioning record's hardening section; and the external probe (password auth refused from outside) is mandatory evidence, not optional. If the hardening module fails mid-run, the VM is treated as unhardened — no data movement, re-run or escalate.
>
> Allowlist: 34.16.56.64/32 is confirmed as the sole security-group SSH source at VM creation. No IPv6 rules. If my own access is needed later it enters as a second /32 by explicit addition, never a widened range.
>
> Sequencing note: Phase 1 and the compute seam continuing on-programme is correct and unblocked. The FL-P2-03 console check is your immediate next action; on a green check, Phase 0 executes today under path (a)."

**Binding effects:**

1. **FL-P2-03 CLOSED with freeze upheld.** Provenance explanation: PDF is Rafay onboarding SOP written around 1×H200 default; the 4×H200 / 84 vCPU / 948 GB / 12 TB SKU is vendor-confirmed in direct correspondence outside the document. Vendor's on-record words: accepts the single-node shape 4×H200/84vCPU/948GB/12TB; routine restart does NOT wipe ephemeral (only deletion/deprovisioning does); ~30 TB HSS shared to the organisation. **Console check is builder's immediate next action.**
2. **Two-branch outcome for the console check** (read-only, NEVER provisioning):
   - Green: HSS ~30 TB visible AND 4× H200 Catalog entry visible → checklist unfrozen for that execution only; Phase-0 proceeds per §6 spec.
   - Not-green (HSS absent, undersized, or no 4× Catalog entry) → stop stands; report exact console state screenshot-grade; owner takes it to vendor as vendor-side action or updated guide, never adapt around it.
3. **1× SKU is not a fallback / not a bridge / not a start-small.** A single-GPU machine cannot carry the committed workload; provisioning would spend contract term and create a machine to deprovision. §6 spec is what the vendor confirmed.
4. **`phase0/acceptance.sh` and `commissioning_checklist.md` stay FROZEN at Order §6 spec** — no adaptation to 1×H200 under any circumstance.
5. **FL-P2-04 CLOSED path (a) — hardening executes through the compute seam.** Bindings on path (a):
    - Bootstrap credential transits the channel ONCE, used only by the hardening module, retired within the same session, and NEVER lands in STATE/, logs, or any file.
    - Hardening module writes the commissioning-record hardening section.
    - External probe (password auth refused from outside the pod) is MANDATORY evidence, not optional.
    - Mid-run hardening failure → VM treated as unhardened → NO data movement → re-run or escalate.
6. **Allowlist confirmed:** `34.16.56.64/32` is the sole security-group SSH source at VM creation. No IPv6 rules. Any subsequent /32 additions require explicit action, never widened ranges.
7. **Sequencing:** Phase-1 + seam continue on-programme (correct and unblocked); FL-P2-03 console check is the immediate next action; on green, Phase-0 executes today under path (a).
8. **Precondition for the console check.** Access to the Rafay console requires credentials. If Rafay console credentials have NOT been provided to this workspace, that is a PRECONDITION GAP — the check cannot be attempted; report exactly what the login page requires (URL + auth mechanism) and escalate for owner-side credential handover. NEVER provision anything in this step; never attempt provisioning; the check is read-only.


---

## Owner Ruling on Console-Access + Credential-Delivery + WS-BUILD-CONNECT-GPU · 2026-08-14 · Source: owner channel · Log verbatim

**Verbatim:**

> "Phase 1 acknowledged and accepted: 35/35 green, zero existing files touched, precondition (a) BANKED with the VM-as-infrastructure-actor shape already drilled — that declaration is ready to fire the day the machine exists. The hardening module is accepted as code-complete under the nine assertions. Good work on stopping at the console rather than clicking anything.
>
> Console access — all three options are REFUSED, and the visibility check is superseded. No credential for the Rafay console — API key, password, or SSO — will enter the workspace, now or later; that's standing policy. And the check itself is no longer yours to run: how the VM gets provisioned, and any pre-provisioning verification in the console, is handled on my side. What reaches you is the result of provisioning, through the product — see the new item below. Mark FL-P2-03 SUPERSEDED-TO-ACCEPTANCE: the go/no-go it protected moves whole to your frozen acceptance.sh on first hardened login. If the delivered machine is not the §6 spec — 4× H200 with NVLink active, ~30 TB HSS mounted/writable/restart-surviving, 84 vCPU / 948 GB, ephemeral scratch — stop, zero data movement, ledger the exact evidence (nvidia-smi, mounts, sizes), and report. The spec stays frozen; a wrong machine is escalated, never accepted. Your GO-gate concern is honoured in the same move: nothing you do spends contract term, and no data moves until acceptance runs green.
>
> Credential delivery — the 'secure channel' path is replaced by a product surface. New Track-A item, pulled forward; it now gates Phase 0's completion:
>
> WS-BUILD-CONNECT-GPU. I will key the VM credentials into the app myself: Connect tile → GPU. Build the minimal governed surface, tests-first, in the fixture grammar:
>
> Form (open state of Connect → GPU): Host Name, Username, Password, Public IP; optional Private IP, OS, and deploy date — deploy date pins the +14d checkpoint clock in PINS on submit. Password masked, never echoed, never retrievable after submit.
>
> On submit, the machinery you've already built fires automatically, in order: credential held environment-grade under the nine assertions → path-(a) hardening module (keys in, password auth disabled, bootstrap credential retired same-session, external probe confirms it dead) → acceptance.sh frozen at §6 → results ledgered as the commissioning record → non-secret Output values into PINS. The form is the trigger; no manual step sits between entry and hardening.
>
> What the surface shows afterward — the four questions, never the secret: What's happening — 'One GPU machine connected · hardened · accepted,' or its honest failure state. How do we know — acceptance results as sentences, walking to the commissioning record. What we're doing about it — 'Ready for first data,' or the exact stop reason. Is what we agreed being done — 'The machine matches what was ordered,' or the deviation verbatim. After retirement there is no password to show, anywhere, ever.
>
> Failure grammar: hardening failure renders failed (ours; retry). Acceptance failure renders held with the evidence and 'escalated to the vendor' as the stated next step.
>
> Identity and record: submission runs under a governed task identity and is receipted; the credential-entry event (never the credential) is a ledger row; the VM's declaration as an infrastructure actor fires from the same submit using the Phase-1 drilled shape.
>
> Scope discipline: one connection type on one existing tile — not a credentials manager, not a multi-provider abstraction. S/M class; if it grows past M, stop and say why.
>
> Queue updates: provisioning day reaches you via the form's deploy-date field, not a message. The bootstrap password now transits once into the estate through this surface instead of through a channel — your same secrecy assertions apply unchanged. The reference screenshot as a file still follows; transcription-grade holds until then.
>
> Order of work from here: WS-BUILD-CONNECT-GPU next (it gates Phase 0), Phase 1 follow-on and the compute seam continue in parallel, and your first report on this item is the built surface with its gating tests green — at which point I enter the credentials and Phase 0 completes end-to-end in one motion: entry → hardening → acceptance → commissioning record → clock pinned."

**Binding effects:**

1. **Standing policy — NO Rafay console credential enters this workspace**, now or later. Not password, not API key, not SSO. FL-P2-03 SUPERSEDED-TO-ACCEPTANCE (see fidelity_ledger row update).
2. **Console visibility check retired.** Owner handles provisioning + pre-provisioning verification on their side. The go/no-go moves whole to `phase0/acceptance.sh` on first hardened login. `phase0/` remains FROZEN at §6.
3. **On-arrival wrong-machine handling.** If delivered machine ≠ §6 spec (4× H200 NVLink active · ~30 TB HSS mounted/writable/restart-surviving · 84 vCPU · 948 GB · ephemeral scratch): STOP · zero data movement · ledger exact evidence (`nvidia-smi`, `mount`, size figures) · report. A wrong machine is escalated, never accepted.
4. **WS-BUILD-CONNECT-GPU is a new Track-A item, pulled forward, gates Phase-0 completion.** Tests-first on `programme/track-a` in Extraction-Akki. In the fixture grammar (tile-grid + detail card; Connect tile in the REGISTRY group per the screenshot transcription; rule-zero four-questions topline on the after state; `test_four_questions_topline_present` applies to this surface NOW).
5. **Form fields (open state of Connect → GPU tile):** Host Name, Username, Password (masked, never echoed, never retrievable), Public IP; optional Private IP, OS, Deploy Date. Deploy Date pins the `+14d checkpoint` clock in `PINS.md` on submit.
6. **Submit pipeline (automatic, no manual step between entry and hardening):**
   - credential held environment-grade under the nine hardening secrecy assertions →
   - path-(a) hardening module (keys in · password auth disabled · bootstrap credential retired same-session · external probe confirms it dead) →
   - `acceptance.sh` frozen at §6 →
   - results ledgered as the commissioning record →
   - non-secret Output values into `PINS.md`.
7. **After-state renders the four questions in fixture grammar (rule zero):**
   - What's happening: `One GPU machine connected · hardened · accepted` OR the honest failure state.
   - How do we know: acceptance results as sentences, walking to the commissioning record.
   - What we're doing about it: `Ready for first data` OR the exact stop reason.
   - Is what we agreed being done: `The machine matches what was ordered` OR the deviation verbatim.
   - After retirement there is NO password to show, anywhere, ever.
8. **Failure grammar (mandatory copy):**
   - Hardening failure → `failed (ours; retry)` — retry supported.
   - Acceptance failure → `held` with evidence and `escalated to the vendor` as next step.
9. **Identity + record.** Submission runs under a governed task identity; receipted; the credential-entry event (NEVER the credential) is a ledger row; the VM declaration as `infrastructure.vm.<host>` fires from the same submit using the Phase-1 drilled shape.
10. **Scope discipline: S/M class.** One connection type on one existing tile — not a credentials manager, not a multi-provider abstraction. If it grows past M, STOP and say why.
11. **Queue update.** Provisioning day reaches builder via the form's Deploy Date field, not a message. Bootstrap password now transits ONCE into the estate through this surface (secrecy assertions apply unchanged). Reference screenshot file still follows; transcription-grade holds.
12. **Order of work:** WS-BUILD-CONNECT-GPU next (gates Phase-0); Phase-1 follow-on + seam continue in parallel; first report on this item is the built surface + gating tests green. Then owner enters credentials, Phase-0 completes end-to-end in one motion.
13. **Orchestrator execution notes bind (see NEXT.md):** on programme/track-a AND spine app served at pod preview URL `https://akki-reuse-assess.preview.emergentagent.com`; behind spine auth (seeded owner account, strong generated password OR token) — that's an app login, not a console/VM credential; rate-limited + CSRF-protected. End-to-end drill against a local mock sshd on `127.0.0.1:2222` BEFORE any hand-off; drill distinguished by host identity, no drill-mode switch.



---

## Owner Stop-Order Ruling · 2026-08-14 · Source: owner channel (WS-BUILD-CONNECT-GPU access mechanism)

**Verbatim (owner directives, faithful reconstruction from stop-order + plan-confirmation replies):**

> Stop. The auth token you asked me to paste was transmitted in plaintext.
> Revoke that token IMMEDIATELY: delete `/app/backend/.owner_credentials`,
> scrub the value from every file it touched, confirm the compromised value
> is dead across every route (probe → 403).
>
> The minted-credential pattern is retired estate-wide. Access to this
> surface is IP-pinned from now on. Implement a source-IP allowlist
> middleware, tests-first, with the initial allowlist STRICTLY
> `34.16.56.64` (env var, not hardcoded). Trust the header the preview
> proxy sets with the true client IP — establish that EMPIRICALLY, do
> not assume. A client-spoofable XFF entry must not be able to defeat the
> allowlist; write that spoof-resistance case as one of the tests.
>
> The allowlist covers EVERYTHING: UI routes, `/api/connect/gpu`,
> `/api/deliverables`, static assets. No route survives outside it.
> Refusal is one plain sentence, estate grammar, zero detail leakage:
> `"This surface answers allowlisted addresses only."` HTTP 403,
> `text/plain`, NOT the FastAPI default.
>
> The standalone `/register/connect/gpu` route is retired. Re-home the
> Connect GPU form under: root `/` → top tab bar → **Admin**
> (right-aligned) → tile grid (TRUST CENTER + REGISTRY) → Connect tile →
> GPU form. Tests first: `/register/connect/gpu` returns 404; no
> token-gate code path remains importable; the form is reachable via
> root → Admin tab → REGISTRY → Connect tile in the rendered tree.
>
> Propose ONE access mechanism to me (IP-pinned), in exactly two
> sentences, no alternatives. Open a fidelity-ledger row recording the
> retired minted-credential pattern; close it citing this ruling.
>
> No push, ever — Owner Clarification 1 unchanged. Local commits are
> the record. Commits land on BOTH repos as their content dictates —
> code on `programme/track-a`, STATE / fidelity-ledger / phase0 artifacts
> on assessment-repo `master`. Not track-a only.
>
> The compromised token never appears in your reply, logs, commit
> messages, STATE/, or the scrub diff. Read it transiently from wherever
> it survives for the 403 probe, use it once, do not re-record it. If
> scrubbing git-tracked files, the scrub commit message says "token
> scrubbed" without the value.

**Binding effects:**

1. **Token revocation IS THE FIRST ACTION.** `/app/backend/.owner_credentials` deleted; `spine_auth.py` deleted; `/app/memory/test_credentials.md` scrubbed; compromised value confirmed dead across all routes (403 on `/api/connect/gpu` with old bearer — was 422 = accepted before). Executed 2026-08-14 15:00Z.
2. **Source-IP allowlist middleware** at `services/ip_allowlist/middleware.py` (spine repo) + `plugins/ip-allowlist/{check.js, middleware.js}` (pod-shell frontend). Config: `SPINE_ALLOWED_IPS` (comma-separated /32s, whitespace-tolerant) and `SPINE_TRUSTED_PROXY_HOPS` (default 2) both live ONLY in `/app/backend/.env`; the frontend `craco.config.js` reads them from that file to preserve single source of truth. Empirical header trust boundary: `xff.split(',')[-1 - SPINE_TRUSTED_PROXY_HOPS]` (default → `xff[-3]`) is the CF-Worker-injected true-client-IP; client-controllable leftmost entries are ignored by construction.
3. **Refusal grammar** is the exact plain sentence, HTTP 403, `text/plain; charset=utf-8`. Body carries no allowlist entry, no caller IP, no configuration hint.
4. **All routes gated.** FastAPI middleware runs before route matching (verified by a test that pings a non-existent route from a disallowed IP and expects 403 not 404). CRA dev-server middleware runs before every other middleware (verified by unshift into `setupMiddlewares`). Ingress topology: UI/static traffic goes through the frontend supervisor; `/api/*` goes through the backend supervisor — both gates now installed.
5. **Retired minted-credential pattern.** Fidelity-ledger row **FL-P2-08** opened and CLOSED same cycle. Standing rule appended (see PINS.md and Standing Rules Digest): **no minted shared secret ever gates the estate surface again.**
6. **Re-homed Connect GPU form.** Root `/` renders `<AdminSurface />` (tile grid + detail card + embedded GPU form). Retired route returns HTTP 404 with plain text `"This route has been retired."` (edge-refused before React Router). Test invariants (9 total on `pod_shell/frontend/__tests__/rehome.test.js`) cover: retired route 404, absent token-gate code paths (`spine_auth`, `owner_token`, `Bearer`, `.owner_credentials`), absent OWNER-ACCESS sign-in card copy, presence of required data-testids (admin-pill, tile-connect, 7 form fields, submit), no `owner_token` localStorage anywhere in frontend source.
7. **Empirical trust-boundary discovery** logged as **FL-P2-10** (CLOSED). Probe endpoint was installed and removed in the same session, leaving no diagnostic surface behind.
8. **Pod egress-IP rotation surprise** logged as **FL-P2-09** (OPEN). STATE had `34.16.56.64`; live verification returns `34.170.12.145`. Owner's directive to use `34.16.56.64` STRICTLY as the initial allowlist stands; the pod is NOT self-allowlisted. The two-sentence access proposal to the owner therefore says: *"Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` — every change is a ledger row and the surface renders the current allowlist state as plain sentences."*
9. **No push discipline reaffirmed.** Local commits on both `programme/track-a` (code, tests, pod-shell mirror) and assessment-repo `master` (this DECISIONS entry + fidelity-ledger rows + phase0 drill receipts + STATE/ refresh) are the record.

**Green receipt this cycle** (`phase0/drill_receipts/20260814T151500Z_lockdown_and_rehome_green.log`): **99/99** total gating tests green (78 backend python + 12 frontend allowlist + 9 re-home). Right-reason failure receipts banked for both new invariants (IP allowlist + re-home) before implementation landed.

---

## Orchestrator ruling this cycle · 2026-08-14 · Source: orchestrator note in stop-order reply (shared defect)

**Verbatim:**

> "We shared a builder-side defect this cycle: the WS-BUILD-CONNECT-GPU
> access-mechanism proposal came out as a minted shared secret, and neither
> the builder nor the orchestrator surfaced the exposure grammar before the
> owner did. Standing-Disposition infra-not-refusal applies: the mistake
> becomes doctrine. Access mechanisms proposed to the owner MUST default
> to inspectable, config-not-secret grammars (IP allowlist, cert-pinned
> mTLS, hardware key) — never a text string the owner has to paste."

**Binding effects:**

1. Recorded as a Standing Rule addendum (see Standing Rules Digest in ORCHESTRATOR.md): access proposals default to inspectable config-not-secret grammars; a shared bearer token is a smell to be refused unless explicitly ruled otherwise.
2. Applies retroactively: the retired minted-credential pattern (FL-P2-08) becomes the reference doctrine case.



---

## Owner Fixture Drop · 2026-08-14 · Source: owner channel ("Screen mockups.PDF" + 4 inline screenshots)

**Verbatim (owner's words, quoted from the drop message):**

> "To resolve the back and forth - attached is screenshots of registry and connect wizard.
>
> This is a BINDING fixture for how Registry and Connect render.
>
> DOWNLOAD + PIN: [URL] -> fixtures/screen_mockups_v7.pdf, sha256 into PINS.md. Extract ALL pages (text + layout description per page) into fixtures/screen_mockups_inventory.md. This is file-grade fixture material - upgrade the relevant FIXTURE CLEARED markers from transcription-grade where these screens cover them.
>
> WHAT THE INLINE SCREENSHOTS SHOW: (a) Registry surface, title 'Registry · ESTATE' with Back button, THREE TABS: 'DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS', a '+ Connect' navy button top-right, stat-card grids with plain-sentence sublabels ('drawn, never left blank', 'no path out skips the mask'), a right rail with small-caps eyebrow ('WHAT IS ANSWERING' / 'WHAT YOU HOLD' / 'WHAT IS CONNECTED') + large serif plain-sentence narrative with key figures underlined/red, horizontal bar charts with a 'by ...' cut selector, and record tables (models with IN SERVICE/EVALUATING/RETIRED status chips; cluster workflows with doors Train/Extract/Export/Measure/Prove; estate sources with rights chips). Header: dark navy bar, org name left ('Acme Holdings AI' - DEMO org), right-side ROLE SWITCHER: 'Compliance Owner · Watch Officer · Operator' + user chip. (b) The '+ Connect' opens 'Connect something new - A conversation, not a form': a chat-style wizard with an opening prompt + four quick chips (A data source · An LLM · A trained model · Compute) + free-text input + Send.
>
> RECONCILIATION ORDERS - critical path first: (a) PHASE-0 CRITICAL PATH: re-shape the GPU credential entry to honor the fixture: Registry surface -> '+ Connect' -> 'Connect something new' wizard -> 'Compute' chip -> the wizard collects the SAME ordered fields (Host Name, Username, Password masked, Public IP; optional Private IP, OS, Deploy date) conversationally, then triggers the SAME unchanged pipeline. The submit machinery does not change; only its front door does. Tests-first. (b) The Registry's three tabs render with HONEST CURRENT STATE, never the mockup's demo numbers. Zero fabricated numbers. COMPUTE CONNECTED tab is where the connected VM will render post-Phase-0 with its commissioning facts. (c) The role switcher renders as STATIC presentation for now (single implicit operator role) - the seat/Access model stays Track-B per the earlier ruling; do NOT build auth roles. (d) Scope check: (a) is the gate for Phase 0 - size it; if the wizard re-shape pushes past M, stop and report before building. (b) Registry honest-state tabs are the A4 increment - build after (a) lands, sized separately. Everything else in the 19 pages: inventory only this cycle, no build.
>
> IP allowlist stays exactly as-is (34.16.56.64 only - owner's IP still not received; deployment stays effectively private)."

**Binding effects:**

1. **Fixture upgraded to file-grade.** `fixtures/screen_mockups_v7.pdf` (sha256 `418ad0e3...`) pinned in PINS.md as file-cleared for Registry surface pattern + Connect wizard grammar + content rules + states/edges. `notes/fidelity_ledger.md` **FL-P2-11 CLOSED** records the upgrade from transcription-grade for the surfaces this brief covers.
2. **Discrepancy recorded (not silently reconciled).** Owner said "19 pages plus 4 inline screenshots" - actual PDF is 5 pages of pure text (feature/component brief), zero embedded images; the 4 inline screenshots were not accessible as job assets. Owner's inline textual description stands as the binding visual reference; PDF stands as the written spec. Full inventory at `fixtures/screen_mockups_inventory.md`. **FL-P2-14 OPEN** for owner disposition (does owner want to re-upload the visual mockup deck? Or is the current PDF + inline description the intended fixture?).
3. **"Wizard-not-form" rendering decision.** Connect is a right-hand drawer holding a conversation, not a form. Four suggestion chips (A data source · An LLM · A trained model · Compute); free-text input; branch-by-what; failure is a first-class outcome; success ends the conversation with a single Close and a toast. GPU credential entry moves from the current Admin surface's tile grid into the Connect wizard's Compute path. **FL-P2-12 CLOSED** records the rendering decision.
4. **Demo-data-vs-honest-state rule.** The Acme Holdings AI figures in the mockup are illustrative seed content of a demo org. The estate renders its TRUE current state ("No data connected yet." / "One machine pending connection." / "Not yet measured - drawn, never left blank"). Zero fabricated numbers ever land in code. **FL-P2-13 CLOSED** records the rule.
5. **Role switcher = static presentation.** Compliance Owner / Watch Officer / Operator chips render visually per the mockup but carry no auth wiring this cycle; seat/Access model stays Track-B per prior ruling. **FL-P2-15 CLOSED** records the deferral.
6. **Scope discipline reaffirmed.** (a) wizard-re-shape is the Phase-0 gate this reply, sized before build. (b) Registry honest-state tabs are the A4 increment, sized separately, next cycle. Everything else in the brief (opportunity list, "Reading the mix" panels, "How a model enters and leaves", stat grids with 9 metrics per tab, chart blocks, filter chips on record tables, announcement rows, ceremony/census interactions, open questions) is **INVENTORY ONLY** this cycle - no build.
7. **IP allowlist unchanged.** `SPINE_ALLOWED_IPS=34.16.56.64` remains; deployment stays effectively private until owner's `/32` arrives.

---

## Owner Course-Correction · 2026-08-14 · Source: owner channel (fixture-drop follow-on; three rulings + one build proposal)

**Verbatim (owner's words, quoted from the follow-on message):**

> "Screen shot from the guide is shared. This is the journey we will take to set up the AISCA side and then share with Akki the credentials through connect. This is one of the many connections we will do and it cannot only take one shape. You are designing as though you are building for AISCA. The connector should be a wizard as described in the brief i just shared able to connect the various resources that can be connected to the system, the screenshots i just shared is exactly what you need to reproduce. I worry you are more focussed on whats missing than piecing together what you have. to drive a progressive journey."

**Three rulings + one build proposal:**

1. **FL-P2-14 CLOSED BY OWNER.** The fixture set as received IS the fixture. The "19 pages" referred to the owner's claude.ai prototype, not a missing deck. The five-page written brief `fixtures/screen_mockups_v7.pdf` + the four Registry screenshots described inline + the AISCA guide's Figures 5-13 already held at `fixtures/AISCA_GPU_Access_Guide.pdf` are the binding fixture. Stop chasing missing pages.

2. **Standing posture correction.** Assemble the progressive journey from what exists; escalate only true blockers. This changes tone and initiative, NOT evidence standards. Honesty discipline unchanged (still no fabrication, still no invented fixture material, still no papering over conflicts). Recorded as a standing instruction at the top of `STATE/CONTEXT.md`.

3. **The wizard is generic.** The prior build shipped Compute-chip -> straight to a 7-field form. That was designing for AISCA. The brief specifies FIVE conversational steps for ALL resource kinds (PDF §5, pages 3-4): 1 What -> 2 How -> 3 Credentials -> 4 Name -> 5 Attempt. AISCA/GPU is ONE instance of the journey, not the design. Rebuild the wizard to the brief's grammar, tests-first, with per-type branches at Step 2 (SSH-over-public-IP for compute; private-link/on-premise/batch for data-source; in-seam/on-premise/sandbox for LLM; registry/imported for trained-model). Non-compute types get Steps 1-4 fully wired and an honest ledgered Step 5 ('Recorded - this connection type goes live with its wave.') rather than a fake success.

4. **Provisioning-card build proposal (piecing together from the guide's own figures — Fig 10 SSH Public Key field at creation + Fig 11 multiple /32 SG rows).** Generate the estate's ed25519 keypair NOW in the seam's key custody (private key never leaves the pod, never committed). Render the public key + pod egress IP as a 'provisioning card' the wizard shows BEFORE credentials are keyed. The owner pastes the public key into the VM's SSH Public Key field at creation and adds both /32 rows (their IP + pod egress) to the VM's Security Group SSH rules. Consequence: VM is key-reachable from first boot; the bootstrap password becomes a fallback; hardening shortens to verify-key-only -> disable password auth -> probe dead. Public keys and IPs are not secrets; they lawfully render on the surface with provenance sentences per Content Rule 1.

**Binding effects (all executed this cycle):**

1. **Honest scope reported both ways.** Strict-M reading (1 changed frontend component + 2 new backend contracts) = **L**. Cohesive reading (owner's own phrasing: "the new backend surface is the keypair/provisioning-card endpoint + intent-recording for non-compute types" — one incremental surface) = **M at ceiling**. Owner's "the journey shape ships NOW" imperative interpreted as authorisation to proceed under the cohesive reading. Build proceeded.
2. **Backend: services.estate_keys.keypair** — ed25519 openssh keypair custody. `ensure_keypair()` is idempotent; private at `${ESTATE_KEYS_DIR}/estate_ed25519` mode 0600; public at `.pub` mode 0644; fingerprint = SHA256:base64(sha256(raw-wire-bytes))-with-'='-stripped. Return value never carries private material.
3. **Backend: services.connect_estate.router** — `GET /api/connect/estate-facts` returns `{estate_public_key, estate_public_key_fingerprint, pod_egress_ip, provenance}` (4 plain sentences). `POST /api/connect/intent {kind, name, description}` writes a JSON receipt for non-compute kinds; refuses `kind='compute'` (HTTP 400 directing to `/api/connect/gpu`) and empty name (HTTP 400: 'nothing connects unnamed').
4. **Frontend: ConnectWizard** rewritten as a 5-step state machine with step-tracker, per-type Step-2 branches, provisioning card at compute Step 2, GPU form at compute Step 3, name input + `nothing connects unnamed` grammar at Step 4, handshake walk (declaration/hardening/acceptance stages) at compute Step 5, and honest 'INTENT RECORDED' amber card at non-compute Step 5. Free-text routing recognises keywords and asks again on unreadable input.
5. **Tests-first discipline** honoured with right-reason receipts BEFORE each implementation lands (backend: 12/12 ModuleNotFoundError; frontend: 6/21 assertion errors on new 5-step grammar). Green receipt banked after implementation with the six Playwright render-tree screenshots.
6. **99 -> 123 gating tests** (78 -> 90 backend python +12 for estate-keys/connect-estate; frontend 21 -> 33 = 12 allowlist + 21 rehome/wizard). Zero regressions.
7. **Fidelity ledger:** FL-P2-14 CLOSED-BY-OWNER; FL-P2-16 CLOSED (wizard-grammar completion to brief's 5 steps); FL-P2-17 CLOSED (provisioning-card built into compute path); FL-P2-18 CLOSED (posture correction recorded as standing instruction).
8. **IP allowlist unchanged.** `SPINE_ALLOWED_IPS=34.16.56.64` remains; deployment stays effectively private until owner's `/32` arrives.

---

## Owner Simplification Ruling · 2026-08-14 · Source: owner channel (course-correction follow-on; collapse the wizard)

**Verbatim:**

> "keep this simple - i need to be able to key in the creds i get form the Aisca system and any other system user needs to connect to. cannot be a winded journey unless it is impossible. we have synisence, so i should be able to key in details without worrying."

**Binding effects (this cycle):**

1. **The 5-step wizard is retired as the primary path.** Connect collapses to ONE panel opened from Registry -> + Connect: a large secure paste area with copy "Paste the connection details exactly as you received them - I will read them.", the type chips as a small one-tap selector on the same panel (default: auto-detect from the paste), and manual fallback fields inline on the same panel. The conversational step grammar survives ONLY in the progress/result view (the handshake walk from the existing seven-stage pipeline), not as navigation.
2. **Deterministic local parsing, never an LLM.** The paste text is parsed by pattern rules only, in-process, in `services/credentials_paste/parser.py`. Supported shapes: label:value lines (Host Name / Username / Password / Public IP / Private IP / OS / Ephemeral Storage - the AISCA Output panel shape) + generic `key: value` and `key=value` fallbacks. **HARD RULE, added as a gating test:** pasted credential text NEVER transits any LLM call, any external API, or the synisense shield. A password may not be de-identified, embedded, logged, or tokenised. It goes from parse -> env-grade intake -> the seven-stage pipeline, then dies per the nine assertions.
3. **"We have synisence" - rendering of intent.** Reading recorded in `STATE/CONTEXT.md` and in the fidelity ledger (FL-P2-19): synisense governs the estate's ANSWERING surfaces (retrieval, refusals, watermarks), NOT credential custody at intake. Owner can overrule; until then the ruling stands.
4. **Confirm-then-connect.** Parsed fields render once for confirmation, password shown as "•••• captured" (never in plaintext after paste). Owner taps Connect; the existing seven-stage pipeline fires UNCHANGED. Handshake walk renders as the progress/result view - this is where the step grammar lives now.
5. **Unparseable paste = ask-again grammar** naming which fields were missing, plus the manual fields already visible on the same panel as fallback.
6. **Provisioning card stays reachable from the same panel via one link** ("Provisioning a new machine? What to paste on the AISCA side") - not a step, an expanding aside.
7. **Non-compute types: same single panel, same paste-or-fields, same honest intent-record outcome.**
8. **Scope: this is simplification, not growth.** LOC delta reported. STATE + ledger updated. Fidelity ledger rows: **FL-P2-19 CLOSED** (synisense reading recorded), **FL-P2-20 CLOSED** (single-panel collapse), **FL-P2-21 CLOSED** (no-LLM-transit invariant added).
