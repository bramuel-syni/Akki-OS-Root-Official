READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SER v1.1 · C.13 Memory Layer · Delta Draft · memory_compaction_v1

**Status:** DRAFT · notes-only · nothing applied · pending owner ratification per Spec §Sequencing.
**Authority:** Ingest directive 2026-09-18T~11:35Z (banked verbatim in `STATE/DECISIONS.md`) · Step 2 of `memory_compaction_v1` ingestion.
**Applies to:** SER §C.13 (memory layer) · SER §A.4 (TCB row) · SER §B.8 (`akki.arch` deliverables) · SER `failure_posture_v1` rows.
**Blocked-by (per Spec §Sequencing):** C.13 own `partial` build status — key scoping and provenance separation must be enforced BEFORE a compaction lineage can be keyed correctly. NO build wave opens under standing authority.
**Cross-refs:** `notes/canon_extraction/memory_compaction_v1_requirements.md` (atomic rules) · `notes/SER_ERRATA_v1_0_1_20260918.md` (v1.0.1 corrections layer).

---

## §1 · Nature of this delta

Two changes at v1.0 → v1.1 in C.13:

1. **Data model** — four context lifetimes replace two (spec §2 Table 2). The addition is `compacted lineage` + `user memory`; run-scoped and estate remain byte-identical.
2. **Invariants** — MEM-1..MEM-11 land as new C.13.5 invariant block (was: not present). MEM-1..MEM-11 boundary behaviour lands as C.13.6.

TCB placement (SER §A.4 · via `tcb_enumeration_v1` reconciliation) + `akki.arch` R-A-2 allowed_import_targets extension (SER §B.8) + `failure_posture_v1` rows follow.

No SER text is DELETED. All additions are additive; existing C.13 text stays byte-identical.

---

## §2 · Proposed §C.13 Data Model — from 2 lifetimes to 4

### §2.1 · v1.0 shape (existing · byte-identical retained)

Two lifetimes only:
- **run-scoped** · key `(tenant, run, objective)` · populated from the run · expires 7 days after closure.
- **estate** · key `(tenant, source hash, class)` · populated from accepted results only · lives with the source.

Build status: `partial` (key scoping and provenance separation not yet enforced).

### §2.2 · v1.1 shape (proposed · additive)

| Class | Key | Populated from | Expires |
|---|---|---|---|
| Run-scoped (existing) | `(tenant, run, objective)` | The run itself | 7 days after closure — unchanged |
| **Compacted lineage (new)** | `(tenant, objective lineage, compaction version)` | Compaction of run-scoped context under MEM-3 | Ruled retention; erasure overrides (MEM-9) |
| **User memory (new)** | `(tenant, principal, class)` | Compacted artefacts attributed to that principal's own closed runs | With the principal's admission; erasure on request (MEM-10) |
| Estate (existing) | `(tenant, source hash, class)` | Accepted results only — unchanged | With the source |

**Key-scoping preservation** across all four (MEM-R-032): no compaction merges keys across objectives, principals, or tenants. Cross-objective org memory is estate-class only (MEM-R-033).

**Build status pathway:** v1.0 C.13 `partial` → landing key scoping + provenance separation (a M11+ deliverable, TBD wave) → then v1.1 `partial` for compacted lineage + user memory → build fills in.

---

## §3 · Proposed §C.13.5 · Invariants (new section · additive)

Landing verbatim from spec §3 Requirements, with atomic-rule cross-refs from `memory_compaction_v1_requirements.md`:

- **§C.13.5-I-1 (MEM-1)** · Compaction applies to context values only; the Ledger, receipts, provenance documents, and the reasoning audit log MUST NOT be compacted, summarised, or rewritten. [MEM-R-001; B.4; BR-8.1]
- **§C.13.5-I-2 (MEM-2)** · A compacted artefact is a derived artefact — class `inference` or `utterance`, NEVER `fact`; every claim anchors to a retained source by provenance reference AND text hash; unanchored claims refuse. [MEM-R-002; Doc 4 A2; A5.5; C.19 I-2]
- **§C.13.5-I-3 (MEM-3)** · Retention is decided by a deterministic rule set, versioned + ratified under the Rules Service; a learned component MAY draft the compacted text, MUST NOT decide what is retained. Five keep-rules v1 (a-e per MEM-3). [MEM-R-003..R-009; Attribute 10; A5.5; Doc 5 objective freeze]
- **§C.13.5-I-4 (MEM-4)** · Compaction is triggered deterministically — run closure · ruled size threshold · TTL-approach margin — NEVER by a model's judgement. Trigger values ruled by R-19. [MEM-R-010; FP-2 pattern]
- **§C.13.5-I-5 (MEM-5)** · A compacted artefact is a NEW artefact with its own hash + lineage; source versions recorded by hash; NEVER overwrites the version it was compacted from within that version's own lifetime. [MEM-R-011; DAP-37 new-hash precedent]
- **§C.13.5-I-6 (MEM-6)** · Every compaction writes a ledger row BEFORE the artefact becomes readable (source key + source version hashes + retention rule set version + artefact hash + loss statement counts-by-class). Row-write failure aborts compaction; source retained untouched. [MEM-R-012..R-014; B.4; DAP-29 pattern]
- **§C.13.5-I-7 (MEM-7)** · Reload is deterministic — same artefact under same key yields same context. NO re-summarisation on read. Hash-verify or fail closed. [MEM-R-015..R-016; SFP-8 principle; FP-2]
- **§C.13.5-I-8 (MEM-8)** · Reload from a compacted artefact STATES it is compacted + names depth lost (per MEM-6 record). Consuming component MUST NOT present conclusions at a class HIGHER than the artefact carries. [MEM-R-017..R-018; A5.5]
- **§C.13.5-I-9 (MEM-9)** · Erasure reaches compacted memory — every artefact whose provenance cites a withdrawn unit is re-derived without the unit OR recalled on DAP-38's mechanism; erasure overrides retention lengthening (D-14 does NOT apply against lawful erasure). [MEM-R-019..R-021; DAP-38; Kenya DPA 2019 s.40]
- **§C.13.5-I-10 (MEM-10)** · User memory is personal data of the principal — populated only from own closed runs; readable by the principal; erased on request or deprovisioning with a ledger row; tenant MAY disable class tenant-wide; tenant MAY NOT read without documented lawful basis. Class ships DISABLED behind tenant-wide flag OFF by default (per R-21 · owner ingest directive). [MEM-R-022..R-026; Applicable Data Protection Law; C.13 I-1]
- **§C.13.5-I-11 (MEM-11)** · Compaction is idempotent per (key, source version hash); append-only per lineage; concurrent runs on same objective compact own run-scoped keys only. Tenant-admin purge produces a ledger row on same terms as compaction. [MEM-R-027..R-030; C.13.6]

---

## §4 · Proposed §C.13.6 · Boundary Behaviour (new section · additive)

Landing verbatim boundary rules from MEM-1..MEM-11 (spec §3-close) as C.13.6:

- **§C.13.6-B-1** · **Compaction never touches Ledger / receipts / provenance / reasoning audit log** (MEM-1 boundary). Any code path that attempts is refused.
- **§C.13.6-B-2** · **Compacted artefacts refuse unanchored claims** (MEM-2 boundary). A claim without provenance ref + text hash never becomes stored.
- **§C.13.6-B-3** · **Compaction fail-closed on rule-set unreadable OR receipt-unwritable** (MEM-6/failure-posture boundary). Source retained untouched.
- **§C.13.6-B-4** · **Reload fail-closed on hash mismatch** (MEM-7 boundary). Caller refused; NOT served best-effort.
- **§C.13.6-B-5** · **TTL race deferred to compaction decision** (spec §4 failure-posture). TTL reached during a pending compaction defers expiry until the compaction is recorded — context is never lost to a race.
- **§C.13.6-B-6** · **Erasure supersedes retention** (MEM-9 boundary). D-14 tenant lengthening does not apply against lawful erasure.
- **§C.13.6-B-7** · **Concurrent-run key-isolation** (MEM-11 boundary). Compaction on same objective never touches another run's keys.

---

## §5 · Placement in Standing Enumerations (Spec §4 → SER §A.4, §B.8, failure_posture_v1)

### §5.1 · SER §A.4 TCB row (via `tcb_enumeration_v1` reconciliation method)

**Add TCB row (proposed):**

```yaml
- package: services.memory
  entry: "MEM-3 retention rule engine · MEM-7 reload verifier"
  in_tcb:
    - services.memory.retention_engine    # MEM-3 · deterministic
    - services.memory.reload_verifier     # MEM-7 · deterministic
  out_of_tcb:
    - services.memory.drafting_component  # learned · proposes text · decides nothing
  rationale: "Same wall-not-the-run split as Targeta and the Watch. MEM-3 is the wall (retention decision · deterministic); the drafting component is the run (learned · proposes text)."
  canon_ref: [MEM-3, MEM-7, Spec §4 Table 3]
  review_policy: two_reviewers_plus_security_group   # inherited from TCB.yaml root
  build_status: pending_c13_partial_close
```

**Reconciliation constraint:** TCB additions enter ONLY through `tcb_enumeration_v1`'s method (which requires (i) rule-set-versioning present, (ii) reviewer policy inherited, (iii) canon_ref anchored, (iv) build_status flagged). Row above satisfies all four.

### §5.2 · SER §B.8 · `akki.arch` R-A-2 `allowed_import_targets` extension

**Add to R-A-2 `allowed_import_targets`:**

```yaml
- from: services.memory.retention_engine
  targets: [services.rules_service.registry]  # deterministic dependency · retention rule set version lookup
- from: services.memory.reload_verifier
  targets: [services.data.repository]         # deterministic dependency · hash lookup against ledger row · SOLE Motor via M11-W1
- from: services.memory.drafting_component
  targets: [services.chokepoint.llm]          # learned · MUST route through chokepoint · never direct provider SDK
```

**Constraint:** memory.retention_engine + memory.reload_verifier are IN TCB (M11-W1 primitive is their dependency direction · sole Motor importer discipline); memory.drafting_component is OUT TCB and MUST route through chokepoint (D-16 CASCADE + D-17 FRONTIER ACCOUNTS applies at the LLM edge).

### §5.3 · SER `failure_posture_v1` row

**Add row:**

```yaml
- surface: memory_compaction
  failure_class: rule_set_unreadable_OR_receipt_unwritable
  posture: fail_closed_on_compaction
  source_treatment: retained_untouched
  canon_ref: [MEM-6, Spec §4 failure-posture row]

- surface: memory_compaction_reload
  failure_class: artefact_hash_verify_fail
  posture: refuse_caller
  source_treatment: n_a
  canon_ref: [MEM-7, Spec §4 failure-posture row]

- surface: memory_compaction_ttl_race
  failure_class: ttl_reached_during_pending_compaction
  posture: defer_expiry_until_compaction_recorded
  source_treatment: never_lost_to_race
  canon_ref: [Spec §4 failure-posture row]
```

### §5.4 · SER `determinism_inventory_v1` row

**Add row:**

```yaml
- surface: memory_compaction
  classification: hybrid
  learned_components: [drafting_component]
  deterministic_components: [retention_engine, reload_verifier, trigger, receipt_writer, reload_server]
  article_14_c_surface: loss_statement_on_reload  # what lets an overseer know what a compacted context no longer contains
  canon_ref: [Spec §4 determinism_inventory row, MEM-3, MEM-6, MEM-7]
```

### §5.5 · Master Requirements Registry entry (at next refresh)

Per Spec §4 close: "MEM-1 through MEM-11 and S-30 [land] at next refresh." Owner-scheduled; not a this-window action. Transitional `canon_ref` = `memory_compaction_v1 · MEM-<n>` until refresh (per owner directive).

---

## §6 · What this delta does NOT touch

- **Existing C.13 §§1-4 text** — byte-identical. Additive only.
- **Existing C.13 build status** — `partial` remains until key scoping + provenance separation are enforced (independent M11+ deliverable, not gated by this ingest).
- **Ledger schema (BR-13/BR-14)** — MEM-R-041 (LIM-2) explicit: the Ledger grows as it always has; this service governs working context only.
- **Determinism inventory outside memory** — additive row only.
- **`tcb_enumeration_v1` method itself** — TCB row addition follows the method; the method is not amended.
- **Existing R-A-1..R-A-4 `akki.arch` invariants (M13-W1 sealed at CP-M13W1)** — additive `allowed_import_targets` extension only, precedent-anchored to CP-M13W1's own R-A-2 extension pattern.

---

## §7 · Sequencing (per spec §Sequencing + ingest directive)

- **Gates nothing on the R-18 effect-15 path.** M11-W1 through M12b-W1 open independently.
- **Gates nothing until C.13 own `partial` status is closed** — key scoping + provenance separation must be enforced BEFORE compaction lineage keying is correct. That closure is a M11+ wave; the specific wave placement is PROPOSED here, NOT opened.
- **Wave placement PROPOSED:** land memory_compaction_v1 build waves in the **M12b → M13 rest** interval (after M11 finishes key scoping + provenance separation, after M12 wires M9 refusers as unroutable runtime chokepoints, after M12b lands the Ed25519 Watch-key primitive that memory_compaction_v1 will use for signing loss-statement rows). Full wave breakdown authored at the wave-open turn.
- **NO build wave opened under standing authority** per owner directive.

---

## §8 · Rulings (per ingest directive)

- **R-19 (compaction triggers) · DEFAULT-class · pending ratification** — implement against Spec §7 R-19 recommended defaults (size threshold + TTL-approach margin · baseline-period conservative defaults · Doc-3 pattern), tagged pending.
- **R-20 (retention rule set v1) · DEFAULT-class · pending ratification** — implement Spec §3 MEM-3 five keep-rules (a-e) as written; additions arrive through ceremony.
- **R-21 (user-memory class + consent model) · owner input outstanding** — implement user-memory class behind tenant-wide flag OFF by default; no consent model assumed; no principal data written until ruled. Ships DISABLED.

---

## §9 · Property tests authored (Step 3 of ingestion · see companion file)

Companion test file `backend/tests/invariants/test_memory_compaction_v1_property_tests_red.py` (state-repo mirror at `notes/canon_extraction/test_memory_compaction_v1_property_tests_red.py`) authors 7 property tests RED per ingest directive:

1. `test_fact_text_hash_unchanged_through_compaction`
2. `test_every_provenance_reference_preserved_through_compaction`
3. `test_loss_statement_counts_equal_actual_drops_by_class`
4. `test_reload_byte_identical_for_same_artefact_key`
5. `test_reload_refuses_on_hash_mismatch`
6. `test_erasure_query_finds_every_artefact_whose_provenance_cites_a_given_unit`
7. `test_compaction_artefact_not_readable_without_ledger_row`

Test authored in state-repo ONLY (no code-repo landing under standing authority · per ingest directive step 3 "author the property tests before any implementation, tests-first RED per §3.3" — the implementation is a NON-scope wave, so the tests are banked for the future wave open · they are not registered in the current invariants tree until the wave opens).

---

## §10 · Conflict-with-C.13 audit (per ingest directive "any conflict with existing C.13 invariants surfaced as a stop-and-report, not resolved silently")

**Result:** NO conflict surfaced on shape-only ingest read.

- C.13 current text describes two lifetimes with build status `partial`. Spec §2 explicitly preserves both existing lifetimes byte-identical and adds two new classes. Non-overlapping additive change.
- MEM-1 (compaction scope-of-effect) EXCLUDES Ledger + receipts + provenance + reasoning audit log — these surfaces are governed by their own C.n sections (C.4 Ledger, C.11 receipts, etc.) which remain unchanged.
- MEM-10 (user memory · lawful-basis for reads) aligns with C.13 I-1 (existing principal-scoped read discipline).
- MEM-11 (idempotency + append-only) aligns with C.13.6 (existing shape rule; this expansion adds explicit concurrency semantics that were latent).

**Nothing resolved silently.**

---

## §11 · Report line (per ingest directive close)

- **Atomic-rule count:** 53 (MEM-R-001..MEM-R-053) in `notes/canon_extraction/memory_compaction_v1_requirements.md`.
- **§-citation coverage:** 100% — every atomic rule cites its MEM-<n> requirement, spec §, canon anchor, or ruling.
- **SER v1.1 C.13 delta:** this file (§§1-11).
- **Test IDs authored (RED):** 7 (§9 above · companion file).
- **Proposed wave placement:** M12b → M13-rest interval (after M11 closes C.13 partial; after M12b lands Ed25519 signing primitive).
- **Conflict with existing C.13 invariants:** NONE.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
