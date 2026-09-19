# C.13 partial-close status unverified · MEMORY-LAYER-PRECONDITION FORK banked pre-open

**Banked:** 2026-09-19T~12:47:00Z · post-CP-M16-W5-SEAL-INTEGRATION Commit-C fixup (M16 milestone CLOSED · state `939124be` · code `462f6972` · ratchet 5414) · **pre-memory-layer open (deferred until memory-layer boundary per §6 Item-5 fork discipline)**.

**Fork status: CLOSED-ON-C13-CLOSURE-SEAL 2026-09-19T~18:18Z** at CP-C13-CLOSURE-KEY-SCOPING-PROVENANCE-TTL Commit-A `89aed4ecc592f65bb3e90b9e0b279846bce9e6a0` on programme/track-a. Owner ruling 2026-09-19T~17:54Z item (b) verbatim ratified Option (ii) recommendation ("A tightly-scoped C.13 closure wave before the memory layer") and the closure wave sealed with 10 new invariants (5452→5462 ratchet · sha256-pinned schemas · Canon 3 §9.3 + Canon 8 §W11 + Canon 4 §22 + OWNER-DROP-02 anchors). Memory layer opens on this seal.

**Fork class (historical · pre-closure):** DEFAULT-class · deferred-decision · options-with-recommendation per SO §6 Item-5 · **DID NOT BLOCK M17** (fork gate was on memory layer only, per DECISIONS.md:13655 sequence).

**Fork trigger:** at the M16-close boundary the memory-layer sequencing precondition (C.13 partial status closed · key scoping + provenance separation enforced) has **no on-disk evidence of closure**. Per SO §6 Item-5 fork discipline: bank the fork now with options + recommendation; do not resolve alone; take own recommendation at memory-layer open if unchanged; continue on everything else immediately (M17 opens).

**Owner steer verbatim (this-session, 2026-09-19T~12:45Z):**

> "Bank the C.13-partial-close-unverified state as a §6 fork NOW, deferred until memory-layer open. Fork document should state: the sequencing ruling (DECISIONS.md:12468) gates memory layer on C.13 partial closing (key scoping + provenance separation enforced); no file evidence of closure exists; options at memory-layer open are (i) owner confirms C.13 closed / provides the closure, (ii) a small C.13-closure wave is scoped and ruled before memory layer, (iii) memory layer stays deferred. Recommendation yours to draft. It joins the owner desk batch. M17 proceeds regardless — the gate is on memory layer, as you correctly verified."

**Recommendation-drafting authority verbatim (this-session):**

> "3. Draft a recommendation — the Item-5 discipline is options WITH a recommendation, never an empty slot. My steer: recommend (ii) a small, tightly-scoped C.13 closure wave (key scoping + provenance separation enforcement) before memory layer, because it keeps the run autonomous and converts an owner-verification dependency into sealed evidence; list (i) and (iii) as alternatives."

---

## §1 · Facts on disk (all citations from files opened this session)

### 1.1 · The sequencing ruling gates memory layer on C.13 partial closing

**`STATE/DECISIONS.md:12332` — memory_compaction_v1 sequencing ruling verbatim:**

> "Sequencing. Gates nothing on the R-18 effect-15 path. Gates nothing until C.13's own partial status is closed — key scoping and provenance separation must be enforced before a compaction lineage can be keyed correctly. Propose wave placement in your report; do not open a build wave for it under standing authority."

**`STATE/DECISIONS.md:12365-12366` — R-19+R-20 ratification + R-21 outstanding + sequencing reprise:**

> "8. **Sequencing.** memory_compaction_v1 gates NOTHING on R-18 effect-15 path. Gates NOTHING until C.13 partial status closed (key scoping + provenance separation enforced). Wave placement PROPOSED, not opened.
> 9. **R-19 + R-20 = DEFAULT-class · pending ratification tag.** R-21 = user-memory class behind tenant-wide flag OFF by default; no consent model assumed; no principal data written until ruled."

**`STATE/DECISIONS.md:13655` — owner END OF BUILD authority 2026-09-19T~00:20Z (sequence position verbatim):**

> "M10-W2/W3 (finish) → M10-W4 → M12b-W1 (three gates unchanged) → M13 → M14 → M15 → M16 (per the §6.4 pre-ruled scope, nothing beyond it) → M17 → **memory layer (only after C.13 partial closes per the banked ruling)** → frontends (functional parity bar per §6.4; gated on frozen C.17 + DAP entitlement + receipt contracts per the B-frontends-Q1 ruling) — G5 interleaved to completion (1,096/1,096 pre-gate-release)."

### 1.2 · The precondition contents (from the same source)

**C.13-partial-close requirements as banked in the sequencing ruling:**

- **Key scoping** must be enforced before compaction lineage can be keyed correctly.
- **Provenance separation** must be enforced before compaction lineage can be keyed correctly.

Both are C.13's own partial-status close conditions — not memory-compaction-v1's responsibilities. Memory compaction cannot be keyed correctly if the underlying C.13 keying/provenance surface is still partial.

### 1.3 · On-disk evidence of closure status

**Searched this session for on-disk closure evidence:**
- `notes/M6_SEAL_20260916.md` — M6 audio plane seal; not C.13.
- `notes/M7_VERIFICATION_ROLLUP_20260916.md`, `notes/M8_SEAL_20260917.md`, `notes/M9_SEAL_20260917.md` — M7/M8/M9 platform integrity seals; not C.13.
- `STATE/OBJECTIVES/M13.md`, `M14.md`, `M15.md`, `M16.md` — no C.13-closure milestone-wave listed.
- No `notes/C13_*_close.md` file exists.
- No banked ratification entry in `STATE/DECISIONS.md` (searched this session) confirming "C.13 partial status CLOSED" as an owner ruling.

**Finding:** C.13's partial status closure has **no on-disk evidence at the M16-close boundary**.

### 1.4 · SO §6 Item-5 fork-discipline binding

**`notes/ORCH_BOOT.md §10 · Stop-and-report conditions (from owner ruling 2026-09-18 Item 5):**

> "Fail closed on the affected fork, present options with a recommendation, continue on everything else. Do not hold the whole build on one fork."

Applied here: C.13 status is not consequential to M17 (memory layer gate is downstream); options-with-recommendation banked now; continue to M17.

### 1.5 · Non-blocking status for M17

Per `STATE/DECISIONS.md:13655` verbatim sequence and owner steer 2026-09-19T~12:45Z: "M17 proceeds regardless — the gate is on memory layer, as you correctly verified." M17.md (`notes/M17_OBJECTIVE_CARD_DRAFT_20260919.md`) opens under batch-ratification-pending status at CP-M17-W1 Commit-B. **This fork does NOT block M17 open.**

---

## §2 · Options (at memory-layer open boundary)

### Option (i) · Owner confirms C.13 closed / provides the closure directly

**Mechanic:** at memory-layer open ceremony, owner ratifies verbatim that C.13's partial status is closed (key scoping + provenance separation enforced somewhere on disk that this agent has not surveyed) OR provides the closing text as an owner ruling to be banked in DECISIONS.md as the closure of C.13 partial.

**Pros:**
- Zero build cost.
- Fastest path to memory-layer open if the closure evidence exists somewhere this agent hasn't surveyed (e.g., in a prior close report or in an earlier decision entry not surfaced by this fork's evidence walk).

**Cons:**
- Owner round-trip required. Removes the "autonomous through end of build" property banked at `STATE/DECISIONS.md:13655` for this one boundary.
- If closure evidence does NOT in fact exist on disk, this option regresses to Option (ii) after the round-trip.

### Option (ii) · Small, tightly-scoped C.13 closure wave before memory layer (RECOMMENDED)

**Mechanic:** at memory-layer open boundary, insert a small dedicated milestone (call it M17.5 or M-C13-CLOSE or promote to M18 depending on numbering convention at the moment) whose sole scope is **enforcing C.13's two named partial-status conditions** — key scoping + provenance separation — as pytest-only structural invariants over the sealed C.13 surface. Wave count: 2-3 sub-waves (W1 key-scoping AST-scan invariant · W2 provenance-separation AST-scan invariant · W3 integration seal + snapshot pin). Ratchet delta: ~20-25 tests. Time-box: ~1-2 seals (comparable to M16-W1 through W3 triple).

**Pros:**
- Keeps the run autonomous under `STATE/DECISIONS.md:13655` END OF BUILD authority. No owner round-trip for the gate itself.
- Converts an owner-verification dependency into sealed on-disk evidence (matches SO §6.1 files-are-truth doctrine).
- Follows M16 precedent verbatim (small, canon-as-written, additive-only, five-sub-wave shape).
- If C.13 partial-status closure evidence DOES exist elsewhere on disk that this agent hasn't yet surveyed, the closure wave harmlessly duplicates that evidence (additive-only per SO §3.8).
- Provides a stable, on-disk gate for memory layer that survives compaction.

**Cons:**
- Adds one small milestone-length build wave to the sequence before memory layer.
- Requires drafting a scope card for the C.13 closure wave at M17-close boundary (batch-ratification precedent from M13-M17 applies).
- If C.13 partial-status is fundamentally different from what the sequencing ruling names (i.e., "key scoping + provenance separation" is a simplification of a deeper scope), the closure wave would under-scope and require re-scoping at owner review.

### Option (iii) · Memory layer stays deferred until owner rules

**Mechanic:** at memory-layer open boundary, do NOT open memory layer. Continue to frontends work (per sequence at `STATE/DECISIONS.md:13655`) since frontends are gated on frozen C.17 + DAP entitlement/receipt contracts, not on C.13. If frontends complete before memory layer opens, hold at end-of-frontends boundary awaiting owner steer.

**Pros:**
- Zero risk of under-scoping the C.13 closure.
- Preserves the run's monotonic-forward property for everything downstream of C.13.

**Cons:**
- Loses the "run to end of build" property banked at `STATE/DECISIONS.md:13655` for the memory-layer portion of the sequence.
- Memory layer remains unbuilt at end-of-visible-scope, requiring owner attention specifically for the memory-layer gate.
- The 1,096 G5 atomic rules mapping (see `notes/G5_atomic_rules_to_registry_mapping.md`) may reveal additional memory-layer constraints during interleaved work that would surface as additional forks against a deferred boundary.

---

## §3 · Recommendation (owner steer 2026-09-19T~12:45Z verbatim: "recommendation yours to draft")

**RECOMMEND OPTION (ii)** · **small, tightly-scoped C.13 closure wave (key scoping + provenance separation enforcement) before memory layer**.

**Rationale (drafted this-session per owner steer):**

1. **Preserves autonomy.** `STATE/DECISIONS.md:13655` banks the "END OF BUILD" authority explicitly, and the whole point of §6 is that the run does not require owner intervention at every gate. Option (ii) closes this gate autonomously by converting an unproven precondition into sealed on-disk evidence, matching the SO §6.1 files-are-truth doctrine.

2. **Small-wave-precedent-anchored.** M16 (the just-closed milestone) demonstrated the small-wave shape (5 sub-waves · ~28 tests · single-day seal cycle · additive-only per SO §3.8 · zero refactor). M17 is scoped comparably. A C.13 closure wave scoped to the two named partial-status conditions (key scoping + provenance separation) would land in a similar shape and time-box.

3. **Harmless-if-duplicate.** If C.13 closure evidence exists elsewhere on disk that this agent hasn't yet surveyed, an additive-only closure wave duplicates that evidence without conflict per SO §3.8 (thin-kernel additive-only). Worst case: the wave lands, then owner points to prior closure evidence, and the wave's tests remain as belt-and-braces structural assertions. No harm.

4. **Fork-discipline aligned.** SO §6 Item-5 explicitly permits Option-recommended forks to be taken autonomously as DEFAULT-class pending owner ratification. Option (ii) fits that shape exactly.

5. **Owner batch-review preserved.** The scope card for the C.13 closure wave lands at M17-close boundary (batch-ratification precedent from M13-M17), so the owner sees the wave's scope + rationale in the digest batch before it opens, not after.

**Alternatives ranked:**

- **(iii) is the safest but slowest** — recommended only if owner explicitly rules that C.13 partial-status is out of scope for the autonomous run.
- **(i) is the fastest IF closure evidence exists somewhere unsurfaced** — recommended only if owner is willing to burn one round-trip to check.

---

## §4 · Fork resolution mechanics (at memory-layer open boundary)

**Trigger:** at the moment `STATE/OBJECTIVES/` gets a memory-layer objective card drafted (per SO §6.2 batch-ratification-at-preceding-seal at M17-close boundary), THIS FORK ACTIVATES.

**Sequence at activation:**

1. Read `notes/C13_PARTIAL_CLOSE_UNVERIFIED_FORK_20260919.md` (this file).
2. Re-verify no on-disk closure evidence has landed between now and then (walk `STATE/DECISIONS.md` tail + `notes/` for any `C13_*_close.md` / `C13_*_seal_*.md` file created in the interim + any ruling entry with "C.13" AND "closed" in it).
3. If closure evidence found: option (i) resolves automatically. Fork closes at that verification event. Memory layer opens under normal SO §6.7 sequence.
4. If NO closure evidence found: proceed with own-recommendation (option (ii)) per SO §6 Item-5 discipline. Draft a small C.13 closure milestone card (2-3 sub-waves scoped to key scoping + provenance separation enforcement), promote it to `STATE/OBJECTIVES/` under batch-ratification-pending status per M13-M17 precedent, open its W1.
5. Owner desk digest at M17-close carries this fork + its recommended resolution for owner batch-review at that boundary.

**Deferral discipline:** this fork is BANKED, not RESOLVED, at 2026-09-19T~12:47Z. It does NOT trigger at M17-W1 open or during any M17 sub-wave. It activates only at memory-layer open boundary.

---

## §5 · Owner-desk digest slot (for M17-close batch review)

**Batch item title:** C.13-partial-close-unverified fork · resolution recommendation

**Batch summary (5 lines):**

- Sequencing ruling (`STATE/DECISIONS.md:12332 + 12366 + 13655`) gates memory layer on C.13 partial closing (key scoping + provenance separation enforced).
- No on-disk evidence of C.13 partial-status closure at M16-close boundary (searched this session).
- Options at memory-layer open: (i) owner confirms closure · (ii) small C.13 closure wave before memory layer · (iii) memory layer stays deferred.
- **Recommendation: (ii)** — small tightly-scoped closure wave preserves run autonomy per `STATE/DECISIONS.md:13655` END OF BUILD authority; converts owner-verification dependency into sealed on-disk evidence; small-wave precedent from M16; harmless-if-duplicate under SO §3.8 additive-only.
- Non-blocking for M17 · activates only at memory-layer open · full detail in `notes/C13_PARTIAL_CLOSE_UNVERIFIED_FORK_20260919.md`.

---

## §6 · Cross-references

- `STATE/DECISIONS.md:12324-12341` (memory_compaction_v1 ingest ruling · C.13 sequencing precondition banked).
- `STATE/DECISIONS.md:12365-12366` (numbered sequencing reprise + R-19/R-20/R-21 dispositions).
- `STATE/DECISIONS.md:13655` (owner END OF BUILD authority 2026-09-19T~00:20Z · M17 → memory layer sequence).
- `notes/ORCH_BOOT.md §10` (SO §6 Item-5 stop-and-report / fork discipline).
- `notes/M17_OBJECTIVE_CARD_DRAFT_20260919.md` (parallel-banked at same M16-close boundary · confirms M17 proceeds regardless of this fork).
- `STATE/STANDING_ORDERS.md §6.7` (M17 → memory layer → frontends sequence).
- SO §6.1 (files-are-truth doctrine · closure evidence must live on disk to be authoritative).
- SO §3.8 (thin-kernel additive-only · closure wave harmless-if-duplicate).

---

## §7 · Provenance

**Drafted by:** main-agent Autopilot draft under SO §6.2 pre-authorised card drafting authority + SO §6 Item-5 fork-discipline binding · post-CP-M16-W5-SEAL-INTEGRATION Commit-C fixup (M16 milestone CLOSED · ratchet 5414 · state `939124be`).

**Banked at:** 2026-09-19T~12:47:00Z.

**Owner steer:** verbatim citation in §preamble + Recommendation authority verbatim.

**Status:** DEFAULT-class · deferred-decision · pending owner batch ratification at M17-close digest boundary.

**Not blocking:** M17 proceeds immediately per owner steer verbatim "M17 proceeds regardless — the gate is on memory layer".
