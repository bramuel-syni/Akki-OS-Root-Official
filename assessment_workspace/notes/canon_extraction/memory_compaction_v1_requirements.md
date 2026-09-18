READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# memory_compaction_v1 · Atomic Rules · Requirements Checklist

**Source:** `custody/owner_drops/Memory_Compaction_Spec_v1.docx` (sha256 `a0ab271c093405607e472e04ba14d532c4a758ef8a7a9b60ee483a8cbbec3b6a` · verified this-turn)
**Doc title verbatim:** "Memory Compaction & Preservation · memory_compaction_v1 — Draft for owner ratification · extends SER C.13 (memory layer)"
**Authority layer:** (a) per R-18 effect 1 (canon-derived spec · owner-authored · PROPOSED · ratification pending)
**Ingestion authorised by:** Owner ruling 2026-09-18T~11:35Z INGEST directive · banked verbatim in `STATE/DECISIONS.md` "OWNER RULING · 4-HOUR AUTONOMOUS WINDOW · INGEST memory_compaction_v1"
**Rule set:** 2c · atomic single-line rule + one-line rationale + canon anchor.
**canon_ref (transitional, per owner):** `memory_compaction_v1 · MEM-<n>` until next Master Requirements Registry refresh (MEM-1..MEM-11 + S-30 join at next refresh).

---

## Part I · Boundary (MEM-1, MEM-2)

- **MEM-R-001 · Compaction scope-of-effect.** Compaction applies to context values only; the Ledger, receipts, provenance documents, and the reasoning audit log are OUTSIDE its scope and MUST NOT be compacted, summarised, or rewritten. *Rationale:* memory gets smaller; evidence stays whole. *Canon anchor:* MEM-1 [B.4; BR-8.1].
- **MEM-R-002 · Compacted artefact is a derived artefact.** Carries class `inference` — or `utterance` where it quotes — and NEVER class `fact`. Every claim in it anchors to a retained source by provenance reference AND text hash. A compacted artefact with an unanchored claim is refused, not stored. *Rationale:* fact-class integrity is preserved by pointer, never paraphrase. *Canon anchor:* MEM-2 [Doc 4 A2; A5.5; C.19 I-2].

## Part II · Retention · What Is Kept, Who Decides (MEM-3, MEM-4, MEM-5)

- **MEM-R-003 · Retention is deterministic + versioned + ratified.** Decided by a deterministic rule set, versioned and ratified under the Rules Service. A learned component MAY draft the compacted text; it MUST NOT decide what is retained. *Canon anchor:* MEM-3 [Attribute 10; A5.5; Doc 5 objective freeze].
- **MEM-R-004 · Retention rule set v1 keeps (a) every crossing/extraction receipt value by reference, never paraphrased.** *Canon anchor:* MEM-3(a) [R-20 default].
- **MEM-R-005 · Retention rule set v1 keeps (b) every fact-class claim by text hash pointer, never rewritten; a fact MAY be dropped, NEVER altered.** *Canon anchor:* MEM-3(b) [A5.5; R-20].
- **MEM-R-006 · Retention rule set v1 keeps (c) the frozen objective, floor, and frame reference verbatim.** *Canon anchor:* MEM-3(c) [Doc 5 objective freeze; R-20].
- **MEM-R-007 · Retention rule set v1 keeps (d) every refusal and its stated reason.** *Canon anchor:* MEM-3(d) [R-20].
- **MEM-R-008 · Retention rule set v1 keeps (e) every approval decision.** *Canon anchor:* MEM-3(e) [R-20].
- **MEM-R-009 · Retention rule set v1 permits summary of inference/utterance ONLY.** Class `inference` and class `utterance` MAY be summarised under MEM-2. All other classes (fact, receipt reference, refusal, approval, objective/floor) are pointer-or-drop, never paraphrase. *Canon anchor:* MEM-3 · MEM-2.
- **MEM-R-010 · Compaction is triggered deterministically.** Triggers: run closure · ruled size threshold · approach to TTL. NEVER by a model's judgement that context is "no longer needed." Trigger values are ruled by R-19. *Canon anchor:* MEM-4 [FP-2 pattern].
- **MEM-R-011 · Compacted artefact is a NEW artefact with its own hash + lineage.** Registered against its lineage; source versions recorded by hash. NEVER overwrites the version it was compacted from while that version is within its own lifetime. *Canon anchor:* MEM-5 [DAP-37 new-hash precedent].

## Part III · The Record (MEM-6)

- **MEM-R-012 · Every compaction writes a ledger row BEFORE the artefact becomes readable.** Row content: source key + source version hashes + retention rule set version + artefact hash + loss statement (counts by class of what was dropped / summarised). *Canon anchor:* MEM-6 [B.4; DAP-29 pattern].
- **MEM-R-013 · Row-write failure aborts compaction.** If the ledger row cannot be written, the compaction does not complete and the source is retained untouched. *Rationale:* no ledger row = no compaction. *Canon anchor:* MEM-6 · DAP-29 (Ledger-unavailable containment).
- **MEM-R-014 · Loss statement is counts-by-class.** The loss statement in the ledger row is enumerated by class — not summarised, not narrated. Class taxonomy = {fact, inference, utterance, receipt_ref, refusal, approval, objective, floor}. *Canon anchor:* MEM-6.

## Part IV · Reload (MEM-7, MEM-8)

- **MEM-R-015 · Reload is deterministic.** Same artefact under same key yields same context. NO re-summarisation on read. *Canon anchor:* MEM-7 [SFP-8 principle; FP-2].
- **MEM-R-016 · Reload hash-verify or fail closed.** A reload whose artefact hash does not verify against the register fails closed; the caller is refused, NOT served a best effort. *Canon anchor:* MEM-7.
- **MEM-R-017 · Reload from a compacted artefact STATES it is compacted + names depth lost.** In the form MEM-6 recorded. *Canon anchor:* MEM-8 [A5.5].
- **MEM-R-018 · Consuming compacted context cannot upgrade class.** A component consuming compacted context MUST NOT present conclusions drawn from it at a class HIGHER than the artefact carries. *Rationale:* never silently downgraded and served. *Canon anchor:* MEM-8 [A5.5].

## Part V · Erasure & Retention (MEM-9)

- **MEM-R-019 · Erasure reaches compacted memory.** When a unit's rights are withdrawn, every compacted artefact whose provenance cites it is FOUND by provenance reference and either re-derived without the unit OR recalled. *Canon anchor:* MEM-9 [DAP-38].
- **MEM-R-020 · Erasure obligations override retention lengthening.** D-14's "tenants may lengthen, not shorten" DOES NOT apply against a lawful erasure. *Canon anchor:* MEM-9 [Kenya DPA 2019 s.40; DAP-38].
- **MEM-R-021 · DAP-38 mechanism is the mode for either re-derive or recall.** *Canon anchor:* MEM-9 [DAP-38].

## Part VI · User Memory (MEM-10)

- **MEM-R-022 · User memory is personal data of the principal.** Populated only from that principal's own closed runs, never from another principal's. *Canon anchor:* MEM-10 [C.13 I-1].
- **MEM-R-023 · User memory is readable by the principal.** *Canon anchor:* MEM-10.
- **MEM-R-024 · User memory is erased on principal request OR deprovisioning, with a ledger row.** *Canon anchor:* MEM-10 [DAP-38].
- **MEM-R-025 · Organisation MAY disable the class tenant-wide.** *Canon anchor:* MEM-10 [R-21 · tenant-wide flag off by default per owner ingest directive].
- **MEM-R-026 · Organisation MAY NOT read a principal's user memory without a documented lawful basis.** *Canon anchor:* MEM-10 [Applicable Data Protection Law].

## Part VII · Scale · Idempotency + Concurrency (MEM-11)

- **MEM-R-027 · Compaction is idempotent per (key, source version hash).** Same call twice produces the same artefact. *Canon anchor:* MEM-11 [C.13.6].
- **MEM-R-028 · Compaction is append-only per lineage.** *Canon anchor:* MEM-11.
- **MEM-R-029 · Concurrent runs on same objective compact own run-scoped keys, never each other's.** *Canon anchor:* MEM-11 [key-scoping preservation].
- **MEM-R-030 · Purge by tenant admin produces a ledger row on same terms as compaction.** *Canon anchor:* MEM-11 [DAP-38 precedent].

## Part VIII · Four-Lifetime Data Model (Spec §2)

- **MEM-R-031 · Four context lifetimes replace two.** Run-scoped (existing · unchanged 7-day expiry) · Compacted lineage (NEW · ruled retention · erasure overrides MEM-9) · User memory (NEW · principal-scoped · admission-gated MEM-10) · Estate (existing · unchanged · accepted results only). *Canon anchor:* Spec §2 (Table 2).
- **MEM-R-032 · Key scoping preserved across all four lifetimes.** No compaction merges keys across objectives, principals, or tenants. *Canon anchor:* Spec §2.
- **MEM-R-033 · Cross-objective org memory is estate-class only.** Any organisational memory that must cross objectives is an estate-class key, admitted the way estate keys already are — from accepted results ONLY, NEVER a merge. *Canon anchor:* Spec §2 close.

## Part IX · Placement in the Standing Enumerations (Spec §4)

- **MEM-R-034 · TCB additions (`tcb_enumeration_v1`).** IN: the retention rule engine (MEM-3) and the reload verifier (MEM-7). OUT: the drafting component (learned). Same wall-not-the-run split as Targeta and the Watch. *Canon anchor:* Spec §4 (Table 3) [TCB row entry].
- **MEM-R-035 · Determinism inventory (`determinism_inventory_v1`).** Memory compaction is **Hybrid** — drafting Learned; retention decision, trigger, receipt, and reload Deterministic. *Canon anchor:* Spec §4.
- **MEM-R-036 · Article 14(c) surface.** The loss statement on reload is what lets an overseer know what a compacted context no longer contains. *Canon anchor:* Spec §4.
- **MEM-R-037 · Failure posture (`failure_posture_v1`).** Compaction cannot complete (rule set unreadable, receipt unwritable) → fail-closed on the compaction · source retained untouched. Reload unverifiable → refuse. TTL reached while a compaction is pending → expiry is deferred until the compaction decision is recorded; context is never lost to a race. *Canon anchor:* Spec §4.
- **MEM-R-038 · MRR entry.** MEM-1 through MEM-11 and S-30 join the Master Requirements Registry at next refresh. *Canon anchor:* Spec §4.

## Part X · New Promise · S-30 (Spec §5)

- **MEM-R-039 · S-30 promise verbatim.** "The system will make what it holds smaller without losing what it can prove — every compaction is decided by rule, receipted, anchored to its sources, and says on reload what it no longer contains." Rests on MEM-1..MEM-11. Bounds: R-19 (triggers), R-20 (rule set v1). Scope edge: the Ledger is NEVER compacted; user memory exists only where R-21 admits it. *Canon anchor:* Spec §5 (Table 4) [Security Assurance Promise Set S-30 · verified present this-turn].

## Part XI · Explicit Non-Claims (Spec §6)

- **MEM-R-040 · LIM-1 · Does not decide what matters.** Retention rule set keeps what canon says must be kept; whether a summarised inference was the one a person would have wanted is not something a rule set can know. Tuning is by ceremony on evidence, not by drafting model's judgement. *Canon anchor:* Spec §6 LIM-1.
- **MEM-R-041 · LIM-2 · Does not make the record smaller.** The Ledger grows as it always has; this service governs working context only. *Canon anchor:* Spec §6 LIM-2.
- **MEM-R-042 · LIM-3 · Does not create memory across organisations.** A principal's user memory is scoped to the tenant it was formed in. *Canon anchor:* Spec §6 LIM-3.
- **MEM-R-043 · LIM-4 · Does not solve context-window budgeting inside a single run.** That is the run's own budget (C.19.6); this service governs what survives a run, not how a run spends its window. *Canon anchor:* Spec §6 LIM-4.

## Part XII · Rulings (Spec §7 · pending owner ratification)

- **MEM-R-044 · R-19 · Compaction triggers.** Size threshold + TTL-approach margin. Recommended: baseline-period approach — conservative defaults, revised on observed evidence, per Doc 3's own pattern. DEFAULT-class · pending ratification. *Canon anchor:* Spec §7 R-19.
- **MEM-R-045 · R-20 · Retention rule set v1.** Ratify the five keep-rules in MEM-3 as the initial set. Recommended: ratify as written; additions arrive through ceremony. DEFAULT-class · pending ratification. *Canon anchor:* Spec §7 R-20.
- **MEM-R-046 · R-21 · User-memory class + consent model.** Whether the user-memory class exists at all, and under what consent model — opt-in per principal / opt-out / tenant-decided. Product + data-protection decision, NOT technical. Owner input required; class ships DISABLED until ruled. Implementation: **behind tenant-wide flag OFF by default · no consent model assumed · no principal data written until ruled** (per owner ingest directive 2026-09-18). *Canon anchor:* Spec §7 R-21.

## Part XIII · Design Note (Spec closing)

- **MEM-R-047 · Whole-value-is-in-the-rules design premise.** The reason this is a specification and not a feature request is that the obvious implementation — summarise with a model, delete the original — is fast to build and violates FOUR standing rules at once (learned retention · fact paraphrase · silent downgrade · no record). The service's whole value is in the rules that prevent that, not in the summarisation, which is the easy part. *Canon anchor:* Spec closing "Design note."

## Part XIV · Hard Bans (from ingestion · grep-negative surface per owner)

- **MEM-R-048 · No learned component decides retention.** Grep-negative on any code path where an ML component makes a keep/drop call. *Canon anchor:* Ingest directive [Attribute 10].
- **MEM-R-049 · No fact-class text is paraphrased.** Pointer-by-hash or drop. Grep-negative on any code path that transforms fact-class strings. *Canon anchor:* Ingest directive [Doc 4 A2; A5.5].
- **MEM-R-050 · No compaction without a ledger row written first.** Grep-negative on any code path that writes a compacted artefact before its ledger row. *Canon anchor:* Ingest directive [B.4].
- **MEM-R-051 · No re-summarisation on read.** Grep-negative on any code path that regenerates compacted text at reload time. *Canon anchor:* Ingest directive [MEM-7].
- **MEM-R-052 · No compaction of Ledger / receipts / provenance / reasoning audit log.** Grep-negative on any code path that touches these four classes. *Canon anchor:* Ingest directive [MEM-1; B.4; BR-8.1].
- **MEM-R-053 · Design-converges-on-obvious-implementation triggers stop-and-report.** If any design in the workspace converges on "summarise with a model, delete the original," halt and surface to owner. *Canon anchor:* Ingest directive closing.

---

## Summary

- **Total atomic rules extracted this-turn:** **53** (MEM-R-001..MEM-R-053).
- **Coverage:** 11 MEM-* requirements (each expanded to 1-6 atomic rules) + 3 rulings (R-19..R-21) + 4 non-claims (LIM-1..LIM-4) + placement + hard-bans surface.
- **§-citation coverage:** 100% of atomic rules cite either a MEM-<n> requirement, a spec §, a canon anchor (B.4, A5.5, DAP-37/38, SFP-8, FP-2, C.13, C.19), or a ruling (R-19..R-21).
- **canon_ref target (transitional):** `memory_compaction_v1 · MEM-<n>` per owner directive until MRR refresh.
- **Conflict with existing C.13 invariants:** **NONE surfaced** on shape-only ingest read. C.13 (existing SER) has two lifetimes with `partial` build status; spec extends to four with C.13 partial status remaining unaffected until key scoping + provenance separation are enforced (per spec §Sequencing).
- **Rulings status:** R-19 + R-20 landing as DEFAULT-class pending ratification; R-21 landing as tenant-wide-flag-OFF per owner ingest directive.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
