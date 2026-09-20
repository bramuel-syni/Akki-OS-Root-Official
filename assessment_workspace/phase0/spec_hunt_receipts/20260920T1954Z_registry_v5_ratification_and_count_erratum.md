# CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM · 2026-09-20T~19:54Z · spec-hunt receipt

**Precedent shape:** state-master notes-only banking · same class as Ruling-3 docstring-erratum banked in the OWNER-RULINGS section at prior commit `0e7a07b0` STATE/DECISIONS.md:20429. Owner verbatim on erratum shape (this-ruling): *"`0e7a07b0` is a notes-only state-master banking commit; git history is never rewritten. The count-fix lands as a NEW state-only correction entry (same shape as the Ruling-3 erratum precedent): cite `0e7a07b0`, state the wrong text ('V1..V9 verification classes'), state the correct text ('SEVEN classes V1..V7; QA Legend rows 8-9 are sampling tiers Tier A 100% / Tier B sample ≥30%, not classes'), and correct any DERIVED notes: if a derived file is un-banked working-tree, fix it in place; if it was banked, it inherits the same erratum citation rather than an edit."*

**Owner ruling arrival:** 2026-09-20T~19:54Z — RULING on the STOP-AND-REPORT filed at `0e7a07b0` (2 net-new sheets `QA Verification` + `QA Legend` in v5 workbook · outside owner scope-description).

---

## 1 · Owner ruling verbatim (word-for-word)

> OWNER RULING on the v5 net-new sheets: **N + guidance, with one count correction. v5 IS RATIFIED on these terms. G5-v5 OPENS NOW — SFP-1..7 first slice.** Respond in English only.
>
> N FOR SCOPE — owner verbatim substance: G5 maps against the System Rules Registry sheet ONLY; canon_ref resolves to those rows and nothing else. The two QA sheets are the audit standards artefact — tooling an independent auditor fills during the audit, not canon. Register both as INFORMATIONAL, sha-pinned under the workbook hash already on record (`00072c5829d3d893…`), with this owner line attached verbatim to the registration: "classes derived by the stated rule in QA Legend; verdict columns empty by design; V7 is the floor and is reclassified upward by the auditor only, never downward, never by the builder."
>
> GUIDANCE, BOUNDED — the G5 wave MAY read the class column when choosing test shape (V1 row → golden-input test, V2 row → scan, V5 row → injection) because those are the shapes the rule text already demands and the column just confirms it. It does NOT steer authoring where it is silent: two-thirds of rows sit at V7 because a pattern-match found no mechanism in their text, not because document inspection is the right test for them. Owner verbatim: "A regex does not get to decide what an invariant looks like. Rule text governs; the column is a hint."
>
> COUNT CORRECTION — SEVEN classes, not nine. QA Legend has nine rows because rows 8 and 9 are the SAMPLING TIERS — Tier A (100%) and Tier B (sample ≥ 30%) — not classes V8/V9. Tier is an audit-sampling concept; for G5 it means only that the seven SFP rows map in the first slice. FIX THE COUNT wherever you banked "V1..V9" (the `0e7a07b0` banking and any notes derived from it) so the wrong vocabulary does not propagate — erratum or correction per whatever discipline the banked artefact's status requires.
>
> Registry authority chain now: v3 retired → v4 never ratified → **v5 `00072c58…` RATIFIED** as G5 canon_ref target.
>
> Sequencing confirmed: R-86 (mid-flight) → R-87 vocabulary correction → R-88 Content Registry wave → G5-v5 (SFP-1..7 first slice) → CP-APP-JS-UNIFY at your proposed R-91 slot (owner accepted scheduling-not-open-ended; confirm the slot in the R-86 seal report). Standing bounds unchanged. Proceed.

**Follow-up owner verdict on `0e7a07b0` erratum discipline (verbatim):**

> `0e7a07b0` is a notes-only state-master banking commit; git history is never rewritten. The count-fix lands as a NEW state-only correction entry (same shape as the Ruling-3 erratum precedent): cite `0e7a07b0`, state the wrong text ("V1..V9 verification classes"), state the correct text ("SEVEN classes V1..V7; QA Legend rows 8-9 are sampling tiers Tier A 100% / Tier B sample ≥30%, not classes"), and correct any DERIVED notes: if a derived file is un-banked working-tree, fix it in place; if it was banked, it inherits the same erratum citation rather than an edit. That matches your "inspect and match the artefact's status" read — this verdict just saves the inspection.

**Two owner reinforcements (verbatim · no plan change · banked in-flight):**

> (a) Step 3's grep-negative ban set is the full CON set as banked at ingest (no improvised copy, no numbers from generated prose, no engagement signals in ranking, no softening of unsupported claims, templated text never stored, plus the two you listed); (b) Step 4: R-32's ratified surface list (chat answers, recommendation bodies, notification bodies — nothing else) is binding on any CON invariant that touches Generated-class rendering.

---

## 2 · v5 ratification — authority chain (registered)

| Registry version | sha256 | Ratification status | Landing |
|---|---|---|---|
| v3 | `79d44562…` | **RETIRED** per this-ruling (was ratified authority per R-81 seal) | supersedes v4 predecessor |
| v4 | `72160287…` | **NEVER RATIFIED** per prior Ruling 5 (2026-09-20T~19:00Z) verbatim: *"supersedes v4, which was never ratified"* | never opened as G5 canon_ref |
| **v5** | **`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`** | **RATIFIED as G5 canon_ref target** at this-ruling | 115,136 bytes · custody `custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx` · sha-pinned in `phase0/credential_drop_manifests/20260920T1900Z_owner_drops_manifest.json` (open) |

**G5 canon_ref binding:** resolves against **`System Rules Registry` sheet only** (602 data rows). Two other sheets are INFORMATIONAL (see §3).

---

## 3 · QA Verification + QA Legend — registered as INFORMATIONAL (sha-pinned under workbook hash)

Registered under the ALREADY-ON-RECORD workbook sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d` (no separate per-sheet sha; the workbook is the canonical container).

**Registration record — owner verbatim line attached (per this-ruling):**

> *"classes derived by the stated rule in QA Legend; verdict columns empty by design; V7 is the floor and is reclassified upward by the auditor only, never downward, never by the builder."*

**Sheet-by-sheet:**

| Sheet | Rows × Cols | Classification | Role | G5 authority |
|---|---|---|---|---|
| `System Rules Registry` | 602 × 11 | **CANONICAL** | G5 canon_ref target | rule text governs invariants |
| `QA Verification` | 602 × 10 | **INFORMATIONAL** | audit-tooling companion (auditor-fill, verdict cols empty by design) | class column is a HINT for test shape only |
| `QA Legend` | 9 × 4 | **INFORMATIONAL** | vocabulary legend for V1..V7 + Tier A / Tier B (see §4 count-correction) | non-authoritative — never steers authoring where rule text is silent |

**Load-bearing rule (owner verbatim):** *"A regex does not get to decide what an invariant looks like. Rule text governs; the column is a hint."*

**Bounded read-permission** for G5 wave (per owner GUIDANCE, BOUNDED clause):
- **V1 row → golden-input test** (rule text already demands this shape · column confirms).
- **V2 row → scan** (rule text already demands this shape · column confirms).
- **V5 row → injection** (rule text already demands this shape · column confirms).
- **V7 rows (~two-thirds default)** authored **from rule text**, NOT from the column — the V7 default fires when regex found no mechanism, not because document-inspection is the right test.

**Never-do:** never author or override invariant shape from the class column against rule text; never reclassify V7-floor rows downward (auditor-only reclassification, upward-only).

---

## 4 · Count-fix erratum — cite `0e7a07b0`

**Per owner erratum-discipline verdict (§1 follow-up quote):** `0e7a07b0` is a notes-only state-master banking commit; git history is never rewritten. The count-fix lands as a NEW state-only correction entry, same shape as the Ruling-3 erratum precedent.

### 4.1 · Wrong text at `0e7a07b0` (banked · inherits erratum citation · NOT edited)

**Banked file 1:** `STATE/DECISIONS.md` @ `0e7a07b0`
- Line 20528 (verbatim): *"`QA Verification` (602 data rows · 10 cols): audit-tooling companion mapping every SRR rule to `Primary verification class` **(V1..V9)** + `Secondary class` + `Evidence required` + `Sampling tier` (SFP-1..7 all 'A — 100%') + `Auditor verdict` (empty) + `Evidence examined ref` (empty) + `Finding ref` (empty). Full 602-rule coverage. Non-authoritative for rule content (join-key = Rule ID; rule text lives in SRR)."*
- Line 20530 (verbatim): *"`QA Legend` (9 data rows · 4 cols): defines verification classes **V1..V9** (Test evidence · Structural evidence · Record evidence · Governance-record evidence · Failure-injection demonstration · **4 more**)."*
- Line 20537 (verbatim, as paraphrase in Reading B option): *"…per-rule invariants that CITE the QA Verification classification (e.g., V1-classified rules get RED-first tests, V2-classified rules get AST-scan invariants) and align sampling tier to test-authoring intensity (A/100% = full-invariant, other tiers = sampled)."*

**Banked file 2:** `phase0/spec_hunt_receipts/20260920T1945Z_registry_v5_ingest_and_verify.md` @ `0e7a07b0`
- Line 71 (verbatim): *"**Purpose (inferred from content)**: legend defining the verification classes **V1..V9** (or similar) referenced by the `QA Verification` sheet's `Primary verification class` + `Secondary class` columns."*
- Line 78 (verbatim): *"... and **4 more rows (V6-V9)**"*.
- Line 90 (verbatim, in Reading B option): *"…per-rule invariants that CITE the QA Verification classification (e.g., **V1-classified rules get RED-first tests, V2-classified rules get AST-scan invariants**) and align sampling tier to test-authoring intensity (A/100% = full-invariant, other tiers = sampled)."*

### 4.2 · Correct text (this-erratum · replaces the wrong wording downstream · v7 discipline)

**Corrected vocabulary — SEVEN classes plus TWO sampling tiers (nine rows in `QA Legend` = 7 classes + 2 tiers · NOT V1..V9):**

- **Verification classes (7 · V1..V7):**
  - V1 — Test evidence (rule text demands golden-input test where cited).
  - V2 — Structural evidence (rule text demands AST/structural scan where cited).
  - V3 — Record evidence.
  - V4 — Governance-record evidence.
  - V5 — Failure-injection demonstration (rule text demands injection where cited).
  - V6 — (per QA Legend rule text · see workbook).
  - **V7 — Document & design inspection (FLOOR)**. Owner verbatim: *"V7 is the floor and is reclassified upward by the auditor only, never downward, never by the builder."* Default when regex found no mechanism.
- **Audit-sampling tiers (2 · NOT verification classes · distinct axis):**
  - **Tier A — 100%** (all rows sampled · SFP-1..7 all Tier A per prior verification at `0e7a07b0`).
  - **Tier B — sample ≥ 30%**.

**Corrected description of `QA Legend` sheet:** 9 data rows × 4 cols · rows 1–7 define classes V1..V7 · **rows 8–9 define sampling tiers Tier A (100%) and Tier B (sample ≥ 30%)** — NOT verification classes V8/V9.

**Corrected description of `QA Verification` sheet:** 602 data rows × 10 cols · `Primary verification class` and `Secondary class` columns take values from **V1..V7** (not V1..V9) · `Sampling tier` column takes values from **Tier A / Tier B**.

**Corrected Reading-B-style paraphrase (informational only — not a G5 authoring rule):** the class column is a HINT (V1 → golden-input · V2 → scan · V5 → injection) — rule text is authority; column confirms shape where already demanded, never overrides.

### 4.3 · Derived notes — inspection result

Grep sweep across `/app/assessment_workspace/**/*.md` for `V1..V9` / `V1-V9` / `V9\b`: only 5 hits total, ALL banked in `0e7a07b0` (STATE/DECISIONS.md × 3 lines + spec-hunt receipt × 3 lines). **Zero un-banked derived working-tree occurrences** — no in-place fixes required.

`STATE/NEXT.md` grepped — clean.

Un-banked working-tree state at grep-time: only `tools/*.py` untracked files (unchanged from `0e7a07b0`).

**Disposition:** all derived-notes references inherit this erratum citation (per owner verdict). No file-body edits performed.

---

## 5 · G5-v5 STOP-AND-REPORT hold — LIFTED

**Status prior:** G5-v5 HELD pending net-new-sheets ruling (banked at `0e7a07b0`).

**Status post-this-ruling:** **UNBLOCKED**. G5-v5 opens as scheduled (see §7 sequencing).

**Reading N (Narrow) ratified** by owner:
- G5-v5 opens against **`System Rules Registry` sheet only** (602 rows).
- `QA Verification` + `QA Legend` sheets registered as INFORMATIONAL (per §3).
- SFP-1..7 land in the first slice.

---

## 6 · Two owner reinforcements banked (§1 follow-up)

### 6.1 · Reinforcement (a) — R-88+ CP-CONTENT-REGISTRY-WAVE grep-negative ban set

**Binding scope:** full CON set as banked at ingest for R-88+ Content Registry wave (Ruling 4 · CON-1..31 invariants).

**Ban set — banked verbatim (owner phrasing):**
1. no improvised copy;
2. no numbers from generated prose;
3. no engagement signals in ranking;
4. no softening of unsupported claims;
5. templated text never stored;
6. no generated text stored (the "two you listed"); and
7. no unsupported claims (the "two you listed").

R-88+ RED-first property tests + grep-negative hard bans MUST cover ALL SEVEN of the above categories. Any softening or narrowing of this ban set requires an owner ruling.

### 6.2 · Reinforcement (b) — R-32 ratified surface list · binding on any Generated-class CON invariant

**Binding scope:** any CON invariant that touches Generated-class rendering (surfaces exposing generated text to any consumer).

**Ratified surface list (per R-32 · owner verbatim ruling of 2026-09-20T~19:00Z):**
- chat answer surfaces;
- recommendation bodies;
- notification bodies;
- **nothing else.**

Adding a surface later = ordinary-tier ceremony · the new surface's card must cite CON-7.

Any CON invariant touching Generated-class rendering MUST enforce this closed surface list. No headline, quick-note, budget, status, or governance surface may render generated text.

---

## 7 · Sequencing confirmed (owner-ratified · unchanged from prior banking)

1. **R-86 · CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE** (Ruling 1 · MID-FLIGHT on `programme/track-a` in Extraction-Akki · `baseline_failures.json` annotations already added · paired invariant test authoring next · RED-first drill · BASELINE_GUARD=1 double-sweep · 3-Commit Seal · **R-86 seal report will explicitly confirm CP-APP-JS-UNIFY scheduled slot = R-91**).
2. **R-87 · CP-BLOCKED-VOCABULARY-CORRECTION** (Ruling 2 · queued · backend vocab reduced to "three Blocked kinds + Interrupted + party_halted" · FE-FIX-READY spec for FE specialist authored in seal report).
3. **R-88+ · CP-CONTENT-REGISTRY-WAVE** (Ruling 4 · queued · CON-1..31 · RED-first property tests + full grep-negative ban set from §6.1 · R-32 surface-list binding from §6.2 on Generated-class CON invariants).
4. **G5-v5 first slice · SFP-1..7** (canon_ref = System Rules Registry sheet only · class column consulted only as test-shape hint per §3 discipline · rule text governs · silent rows authored from rule text).
5. **R-91 slot · CP-APP-JS-UNIFY** (scheduled-not-open-ended per Ruling 1 · closes the 3 pod_shell mirror-drift baseline entries · closure card at `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` · to be created stub in R-86 Commit-A · full wave content in R-91 slot).

---

## 8 · Files (2 tracked · 1 new + 1 append)

1. `phase0/spec_hunt_receipts/20260920T1954Z_registry_v5_ratification_and_count_erratum.md` NEW (this-file).
2. `STATE/DECISIONS.md` this-append.
3. `STATE/NEXT.md` this-append.

Ratchet unchanged **5640**. Zero code change. Zero test change. Zero baseline change. Not a §3.3 3-Commit Seal — state-master notes-only banking (same class as Ruling-3 erratum banked at `0e7a07b0`).

---

## 9 · Autopilot next this-turn

1. Land Commit-B this-ruling on `master` (state-master notes-only banking · this-file + DECISIONS.md append + NEXT.md append).
2. Switch to `programme/track-a` in Extraction-Akki · resume R-86 mid-flight:
   - Create `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` scheduled-slot stub (R-91 slot · closure trigger for the 3 pod_shell mirror-drift baseline entries).
   - Stash working-tree `baseline_failures.json` edits (restore RED-first shape).
   - Author `backend/tests/invariants/test_baseline_drift_annotations_present.py` (5 property tests per the CCS2-corrected wave scope).
   - Pytest → confirm RED.
   - Unstash `baseline_failures.json` (restore annotations + ratchet bump).
   - Pytest → confirm GREEN.
   - `BASELINE_GUARD=1` double-sweep byte-identical.
   - 3-Commit Seal: Commit-A code (programme/track-a) → Commit-B state (master · seal-report banking · explicitly confirms R-91 slot) → Commit-C fixup / ORCH_BOOT / heads-advance.
3. R-87 → R-88+ → G5-v5 SFP-1..7 first slice → R-91 CP-APP-JS-UNIFY.

---

## 10 · Standing bounds unchanged

zero push · terminal `pytest` only · no `testing_agent` · additive-only §3.8 · three-repo discipline · ratchet monotonic-up (unchanged at **5640**).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
