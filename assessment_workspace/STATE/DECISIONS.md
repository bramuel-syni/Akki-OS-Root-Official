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
