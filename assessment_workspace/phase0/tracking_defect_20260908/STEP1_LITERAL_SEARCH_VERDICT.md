# STEP 1 · Literal-search verdict · owner directive 2026-09-08T~06:15Z

**Owner instruction (verbatim excerpt from DECISIONS.md 2026-09-08T~06:15Z):**

> STEP 1 — PIPELINE FIX (owner's exact instruction, do this FIRST): literally search the entire store for the strings "rule_criteria_spec_v1" and "business_continuity_v1" — grep across canon/ (all drops, all zips' extracted contents — re-unzip any zip not fully extracted), notes/, all five repos, STATE/, everything. Owner verbatim: "If those strings return nothing, they genuinely never arrived and I resend today. If they return something, the tracking indexes by description, not spec ID — that's the actual defect."

**Boot state at time of search (2026-09-09):**
- Workspace `master` HEAD `2c6585be`
- Extraction-Akki `programme/track-a` HEAD `89bbd1c`
- Ratchet floor `3006`
- Grep root: `/app/assessment_workspace/` (canon/ + notes/ + STATE/ + repos/ + phase0/ + fixtures/ + tools/)
- All 7 zip archives already had `extracted/text/` companion dirs; direct XML-body cross-check performed on all `.docx` binaries via `unzip -p <docx> word/document.xml | grep` to close the "extraction missed it" possibility.

---

## VERDICT

**Both strings return non-zero hits. Owner rule fires: tracking defect is confirmed, not a genuine-absence claim.**

| String | Text-mode hits | Unique paths | Docx-body hits (unzip -p) | Verdict |
|---|--:|--:|---|---|
| `rule_criteria_spec_v1` | **179** | **24 files** | 7 docx binaries carry the token in `word/document.xml` | FOUND — tracking indexed by description not spec ID → **DEFECT** |
| `business_continuity_v1` | **4** | **3 files** (excl. this receipt) | 1 docx binary (`Business_Continuity_Annex_v1.docx`) | FOUND — filename ≠ spec ID → **DEFECT** |

---

## Per-string evidence

### String 1 · `rule_criteria_spec_v1` (179 hits · 24 unique paths)

**Highest-signal citations (spec-body vs referenced-only):**

- `canon/drops/20260907/extracted/text/Rules_Service_Spec_v1.txt` — the Rules Service Spec cites `rule_criteria_spec_v1` in RBM-1, RBM-3 [ROC-6], RBM-6 [§8], §T0R1, §T1R1 [ROC-1], §T1R8 [§3], §T2R1 (this is a **citing** doc, not the spec body — its own opening signature is `rulebook_engine_spec_v1 — Draft for owner ratification`).
- `canon/drops/20260907/extracted/text/Security_Promise_Set_Amendments.txt` — cites the spec.
- `canon/drops/20260907/extracted/text/doc0_governance_architecture.txt` — Doc 0 v1 cites it.
- `canon/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt` — Doc 0 v2 cites it.
- `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` — cites it.
- `canon/drops/20260909/extracted/text/Security_Assurance_Promise_Set.md` — cites it.
- `canon/drops/20260907/extracted/text/System_Rules_Registry.{md,json}` — **enumerates the ROC-1..ROC-11 rows** derived from the spec (retrofit population per rule_criteria_spec_v1 ROC-10).
- `canon/drops/20260910/extracted/text/Master_Requirements_Registry.md` — **rows 322-332 list ROC-1..ROC-11 verbatim statements** (O12 Rule Governance | rule_criteria_spec_v1 | ROC spec | PROPOSED (pending ratification)).
- `canon/drops/20260910/extracted/text/Akki_Governance_Architecture_v1_from_15.txt` — Doc 0 v2 (from 2026-09-10 drop) cites it.

**Honest limit (declared for owner):** No `.docx` file whose OPENING signature is `rule_criteria_spec_v1 — Draft for owner ratification` was found. The spec's requirement rows ROC-1..ROC-11 are banked as a **derived population** in `System_Rules_Registry.{md,json}` and `Master_Requirements_Registry.md`, with the citation trail spread across the eight docs above. This is still a tracking defect (M-1..M-7 named it "missing" while the ROC rows exist on disk indexed under spec ID), but the standalone spec-doc for the ROC framework itself is not banked as its own separate file. **DEFAULT-PENDING-OVERRIDE**: treat ROC-1..ROC-11 as banked-in-derived-form; if owner wants the standalone spec doc filed separately, that is a new artifact to request in the next drop.

### String 2 · `business_continuity_v1` (4 hits · 3 unique paths)

- `canon/drops/20260909/extracted/text/Business_Continuity_Annex_v1.txt` — **line 3 opens with `business_continuity_v1 — Draft for owner ratification · Document 3, Part D · Houses S-10, S-11`**. The spec body IS banked.
- `STATE/DECISIONS.md` — cited in earlier owner rulings.

**Docx body cross-check:** `canon/drops/20260909/extracted/files_14/Business_Continuity_Annex_v1.docx` — 1 hit in `word/document.xml` confirming binary-level presence.

**Filename-vs-spec-ID mapping (this IS the tracking defect for BC):** Filename `Business_Continuity_Annex_v1.docx` was in `files_14.zip` (drop 2026-09-09). Spec ID `business_continuity_v1` was carried in the master audit's missing list because the master audit indexed sources by description ("Business Continuity spec") not by spec-ID ⇔ filename ⇔ sha256.

---

## What owner rule mandates next (STEP 1 remediation)

Owner verbatim (from same directive):

> If found: the missing-list entries M-1..M-7 were a TRACKING DEFECT — fix the tracking system itself: every requirement-source row in the master audit gets indexed by spec ID + exact filename + sha256, not by prose description; add an invariant that any doc cited by spec-ID anywhere in canon must either resolve to a banked file or appear on the missing list with a zero-hit grep receipt.

**Remediation obligations landing in subsequent steps of this wave:**
1. Refactor the master audit rows so each row carries `{spec_id, filename, sha256}` in addition to prose title.
2. Add a tests-first invariant:
   - Every spec-ID pattern (`*_spec_v1`, `*_v1`) cited in any `canon/**/*.txt|md` must either
     - (a) resolve to a banked file (via the `{spec_id, filename, sha256}` index), OR
     - (b) appear in the missing list with a zero-hit grep receipt at `phase0/tracking_defect_20260908/grep_<spec_id>.txt`.
   - Ratchet 3006 → 3006+N via mechanical RED then double-green.
3. Rebuild the missing list on the literal-search basis, not description basis. M-1..M-7 and `business_continuity_v1` line are re-classified from MISSING → BANKED (with the ROC standalone spec-doc caveat above named honestly).

---

## Raw evidence files (banked alongside this verdict)

- `phase0/tracking_defect_20260908/grep_rule_criteria_spec_v1.txt` — per-file grep-path listing.
- `phase0/tracking_defect_20260908/grep_business_continuity_v1.txt` — per-file grep-path listing.
- `phase0/tracking_defect_20260908/grep_dap_backend_spec_v1.txt` — companion (DAP spec, prior turn).
- `phase0/tracking_defect_20260908/grep_agent_containment_spec_v1.txt` — companion (AC spec, prior turn).
- `phase0/tracking_defect_20260908/context_rule_criteria.txt` — 13 kB context excerpt.
- `tools/scratch/step1_grep/text_hits.log` — full text-mode grep dump (this session).

---

**Verdict recorded 2026-09-09 at workspace `master` HEAD `2c6585be` · track-a `89bbd1c` · ratchet floor 3006 · read STANDING_ORDERS.md first, permanent standing law.**
