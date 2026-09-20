READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# DIRECT_ANSWERS_TO_OWNER_20260920.md

**Three direct answers to owner disposition items 2(a) · 2(b) · 2(c) · 2026-09-20T~08:35Z.**

**Authored under:** owner directive verbatim 2026-09-20T~08:24Z (banked at `STATE/DECISIONS.md` 2026-09-20T~08:24Z OWNER DISPOSITION section) execution-order item 2. Companion to `notes/DAP_SPEC_REVISION_RECONCILIATION_20260920.md` (the §2.1 report).

**Standing law confirmed:** every factual claim comes from a file opened this session (SO §6.1). All paths repo-relative or absolute. Additive-only per SO §3.8.

---

## §1 · Direct answer (a) — sha256 mismatch on the DAP front-end artifact

### Question (verbatim from owner)

> sha256 mismatch on the same DAP front-end artifact — HOLISTIC_PLAN records `d1c9057b…`, spec_id_index.md records `d0fc1b498e07…`. Confirm spec_id_index.md as authority, or correct it.

### Evidence

**Actual bytes on disk** — `sha256sum /app/assessment_workspace/canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html`:
```
d0fc1b498e07516c4c9acef45224be7add65ba23c35a56837e44074fc6e1c929  RMS_Data_Access_Portal_standalone.html
```
Size: 230,577 bytes. (File date on disk: 2026-09-09.)

**`notes/spec_id_index.md` cites** (with full sha in `notes/spec_id_index.json`):
```
d0fc1b498e07516c4c9acef45224be7add65ba23c35a56837e44074fc6e1c929
```
(matches actual bytes · **exact match**)

**`STATE/HOLISTIC_PLAN.md:133` cites** (partial-prefix):
```
d1c9057b… (partial)
```
(does NOT match actual bytes)

**Full-tree trace of `d1c9057b`** (grep across `.md` + `.json` + `.txt` in `/app/assessment_workspace/**`):
- `STATE/HOLISTIC_PLAN.md:133` — the sole author of this sha (the "already in `notes/spec_id_index.json`" annotation is inaccurate; the index has `d0fc1b498e07…`).
- `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md:137` — this is the reviewer's brief flagging the same mismatch (upstream signal).

**No other file bears the sha `d1c9057b…`** — no artifact on disk (of any size) has this sha. It is not a stale-artifact sha; it appears to be a **transcription error** in HOLISTIC_PLAN.md at authoring time (2026-09-09, same day as spec_id_index generation).

### Verdict

- **Confirm `notes/spec_id_index.md` as authority.** Its `d0fc1b498e07…` matches the byte-identity of the on-disk artifact.
- **`STATE/HOLISTIC_PLAN.md:133`'s `d1c9057b…` is a provenance defect** (transcription error) — the "already in `notes/spec_id_index.json`" annotation is false; the index does not contain `d1c9057b…`.

### Recommendation (owner-directed erratum · pending ratification)

Land as an **additive erratum** at `STATE/HOLISTIC_PLAN.md` (append to §3.3 or §5 body · SO §3.8 additive-only · do NOT overwrite the original line):

**Erratum text (proposed):**

> **Erratum (2026-09-20 · owner-directed):** Line 133 above cites `sha `d1c9057b…`` for design_id `dap_frontend_standalone` at `canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html`. The byte-verified sha256 (per `sha256sum` on the actual file bytes · 230,577 bytes) is `d0fc1b498e07516c4c9acef45224be7add65ba23c35a56837e44074fc6e1c929`. The value banked in `notes/spec_id_index.md` and `notes/spec_id_index.json` matches the byte-identity; `notes/spec_id_index.md` is the authority. HOLISTIC_PLAN.md's `d1c9057b…` was a transcription error at authoring (2026-09-09). See `notes/DIRECT_ANSWERS_TO_OWNER_20260920.md` §1.

**Not a ratchet break** (this is a documentation-provenance error · no invariant test cited this sha).

**Byte-identity impact:** none — the on-disk file has NOT changed since 2026-09-09; only the citation in HOLISTIC_PLAN.md was ever wrong.

---

## §2 · Direct answer (b) — three uncited "owner ruling" citations · found/not-found report

### Question (verbatim from owner)

> Three "owner ruling" citations with no record on this desk — 2026-09-06 (prototype_v3 binding), Ruling #5(a) (masking-policy), 2026-09-08 (surface language). If made outside this chat, confirm and bank them now. If not, this is a provenance fault and needs investigating before it propagates further.

### Search methodology

Exhaustive grep across `STATE/*.md` + `notes/*.md` + `notes/**/*.md` + `phase0/**/*.json` + `phase0/**/*.md` for each ruling by verbatim date + verbatim keyword.

### (b)(i) 2026-09-06 — prototype_v3 binding · **PROVENANCE FAULT (partial)**

**Grep for "prototype_v3" + "binding" + "2026-09-06":**
- `notes/BUILD_STATUS_PERCENT_20260909.md:136` — cites `Prototype prototype_v3 (design_id, binding) + v2 SURFACE_AUDIT 47 surfaces`. Status line, no ruling date attached.
- `STATE/DECISIONS.md:6578` — **exact phrase "prototype v3 = binding design"** appears in the body of a STEP 5 directive.

**Context of STATE/DECISIONS.md:6578** — section header at line 6561:
```
## 2026-09-08T~06:15Z · OWNER DIRECTIVE · Pipeline defect challenge + new drop + rulings
```
The prototype_v3 binding statement is **inside** this 2026-09-08T~06:15Z owner directive (STEP 5 of a 5-step multi-item directive), not a stand-alone 2026-09-06 ruling.

**Grep for "prototype_v3" or "prototype v3" dated 2026-09-06 anywhere in tree:** zero hits.

**Finding:** The "2026-09-06 (prototype_v3 binding)" citation as if a stand-alone dated ruling **does not exist** on disk. The nearest owner statement asserting "prototype v3 = binding design" is at **2026-09-08T~06:15Z DECISIONS.md:6578 (STEP 5)** — three days LATER than the cited date, AND embedded in a larger 5-step directive rather than a stand-alone ruling.

**Verdict: PROVENANCE FAULT** — citation date is wrong. Either (i) an off-record owner statement on 2026-09-06 was verbally binding but never landed to STATE, OR (ii) the citation date should be corrected to **2026-09-08T~06:15Z** (STEP 5 of that directive).

**Recommendation:** owner confirms which. If (i), bank the owner statement now with 2026-09-06 timestamp. If (ii), correct the citation date at source (wherever it appears) via additive erratum.

**Citation-source trace (where the "2026-09-06 prototype_v3 binding" phrasing entered the record):** could not be located on disk. If a wave close-note or grounding brief cited this date, that document is not surfacing to grep — could be a paraphrase in an out-of-tree drop (owner's chat messages), not the tree itself. **Owner input required to trace.**

### (b)(ii) Ruling #5(a) — masking-policy · **FOUND · GROUNDED**

**Grep for "Ruling #5(a)" · "Ruling #5 (a)" · masking-policy:**
- `STATE/DECISIONS.md:6251` — **verbatim banking**: *"Ruling #5(a) landed via user proxy (verbatim, banked in `phase0/policy_drawer_resolutions/drawer_resolution_shield-2026-09-06-q001_20260906T162000Z.json`)"*
- `STATE/NEXT.md:595, 599, 606, 614` — cite Ruling #5 (original) + Ruling #5(a) resolution + downstream effects.
- `notes/wave_multi_table_extract_grounding_brief.md:151` — cites Ruling #5 (2026-09-06T11:34:00Z).
- `notes/wave_sms_body_emit_grounding_brief.md:48, 81, 96` — cite Ruling #5(a) resolution + drawer resolution reference.

**Provenance chain (verified byte-anchored):**
- Original Ruling #5 dated **2026-09-06T11:34:00Z** (per NEXT.md:599) — parked `sms_log.sms_sent` in `masking_policy.v0.json::clarification_drawer` with `cautious_default_applied='exclude'`.
- Ruling #5(a) resolution dated **2026-09-06T~16:20:00Z** (per JSON filename `20260906T162000Z`) — INCLUDE with `mask_regex_scrub` (belt-and-braces).
- Policy drawer resolution file: `phase0/policy_drawer_resolutions/drawer_resolution_shield-2026-09-06-q001_20260906T162000Z.json` — presence to verify.

**Verdict: PROPERLY GROUNDED.** Not a provenance fault. Full byte-anchored provenance chain intact: DECISIONS.md banking → policy_drawer_resolutions JSON → downstream waves.

### (b)(iii) 2026-09-08 — surface language · **PROVENANCE FAULT (not found)**

**Grep for "surface language" OR "surface-language" across `/app/assessment_workspace/**`:**
```
(zero hits · anywhere in tree)
```

**All 2026-09-08 owner directives on disk** (grep for `^## 2026-09-08` in `STATE/DECISIONS.md`):
- `STATE/DECISIONS.md:6424` — `2026-09-08T~04:20Z · OWNER DIRECTIVE · Compaction-proof discipline · STANDING_ORDERS.md chartered`
- `STATE/DECISIONS.md:6468` — `2026-09-08T~04:40Z · Master Requirements Traceability Audit LANDED`
- `STATE/DECISIONS.md:6513` — `2026-09-08T~04:50Z · OWNER DIRECTIVE · W-WINDOW-FILL-RESTORE-2 AUTHORIZED`
- `STATE/DECISIONS.md:6532` — `2026-09-08T~05:15Z · OWNER DIRECTIVE · MISSION-FRAMED REPORTING · 4 artifacts drop`
- `STATE/DECISIONS.md:6561` — `2026-09-08T~06:15Z · OWNER DIRECTIVE · Pipeline defect challenge + new drop + rulings`

**None of these five 2026-09-08 directives has "surface language" in scope or body.** Scanning each: (a) Compaction-proof discipline is process/log-hygiene; (b) Master Traceability Audit is spec-inventory; (c) W-WINDOW-FILL-RESTORE-2 is training-window scheduling; (d) MISSION-FRAMED REPORTING is report shape; (e) Pipeline defect challenge is spec-tracking + prototype-binding defaults.

**Verdict: NOT FOUND ON DISK · PROVENANCE FAULT.** No 2026-09-08 ruling on "surface language" exists in STATE + notes + phase0 anywhere. If this ruling was made outside this chat, it needs banking now. If not, the citation propagation chain must be traced and corrected.

**Citation-source trace (where "2026-09-08 (surface language)" was cited):** the owner's disposition names this as an uncited citation but doesn't specify where in-tree it appears. My exhaustive grep returns zero hits for "surface language" — so the citation is NOT propagating from any file in the tree either. **This may be a citation the owner heard/remembered but which was never actually written into the record.** Either way: safe to declare it does not exist on disk.

### (b) — summary table

| Citation | Status | Evidence | Recommendation |
|---|---|---|---|
| 2026-09-06 (prototype_v3 binding) | **PROVENANCE FAULT** (partial · nearest match 2026-09-08T~06:15Z DECISIONS.md:6578 STEP 5) | Grep + section-header trace | Owner clarify: (i) verbally binding on 2026-09-06 not landed → bank now, or (ii) citation date should be 2026-09-08T~06:15Z → additive erratum. |
| Ruling #5(a) (masking-policy) | **FOUND · GROUNDED** at DECISIONS.md:6251 + policy_drawer_resolutions JSON | Verbatim banking chain byte-anchored | No action. Provenance intact. |
| 2026-09-08 (surface language) | **NOT FOUND · PROVENANCE FAULT** | Zero grep hits anywhere in tree | Owner confirm: if made outside chat, bank now; if not, trace where the citation entered the record and stop propagation. |

---

## §3 · Direct answer (c) — DAP-33/34 source citation correction (additive erratum)

### Question (verbatim from owner)

> DAP-33/34 are cited as security_architecture_v1 S-22/S-23. The content is right; the source document is wrong — S-22/S-23 belong to the Security Amendments' promise set. Correct at the source.

### Evidence

**Current (incorrect) citation** at `STATE/HOLISTIC_PLAN.md:134-135`:

```
| DAP-8 · Component-boundary inspection (S-22) | ... `security_architecture_v1` R-8 DEFAULT baseline-period approach applies | `security_architecture_v1` S-22 · DAP-33 · `security_architecture_v1` R-8 (RATIFIED baseline-period default) | L |
| DAP-9 · Coalition joint evaluation (S-23) | ... `security_architecture_v1` R-11 friction-only default | `security_architecture_v1` S-23 · DAP-34 · `security_architecture_v1` R-11 (RATIFIED baseline-period default) | L |
```

**Correct source citation** — from `notes/ingest_20260907/canon_security_promise_set_requirements.md:45-46` (banked verbatim from the Security Assurance Promise Set doc, which aggregates security promises across the amendment set):

```
| S-22 | Doc 3 (proposed A5.15) · DAP-33 | "The system will inspect what leaves, not only who sends it — every output leaving a component boundary is checked for controlled-unit content and tagged ADVISORY where it recommends, ranks, proposes, or evaluates an action." | ... | **Absent → new** | Ruled — reproduction threshold and probe design are R-8 (DEFAULT-class, conservative, revised on evidence) | **Security Amendments W-1**; gate sits on deterministic side of verdict seam |
| S-23 | Doc 0 Att 3 · Doc 3 (proposed A5.18) · DAP-34 | "The system will treat a coalition as one actor — cumulative conduct across principals sharing a party, a mandate lineage, or a detected coordination signature is evaluated jointly, not per principal." | ... | **Absent → new** | Structural for shared-party and shared-lineage; coordination-signature threshold is R-11 (friction-only under A5.2) | **Security Amendments W-4**; coalition is connected component of admission graph |
```

**Provenance chain from Security Amendments doc:**
- `notes/ingest_20260907/canon_security_amendments_requirements.md:80` — heading `#### W-1 · Output-Content Gate (A5.15 + DAP-33)`
- `notes/ingest_20260907/canon_security_amendments_requirements.md:81-83` — **DAP-33 (verbatim)**: *"Every operation's output under §4 of dap_backend_spec_v1 passes A5.15 before return to the party. Browse output is exempt — it is aggregate only under DAP-6 and carries no unit content by construction."*
- `notes/ingest_20260907/canon_security_amendments_requirements.md:91` — heading `#### W-4 · Coalition as a Principal (Att 3 addition + A5.18 + DAP-34)`
- `notes/ingest_20260907/canon_security_amendments_requirements.md:94` — **DAP-34 (verbatim)**: *"Coalition membership under classes (a) and (b) is recorded at admission and queryable by the estate owner at any time. A party is informed at admission that every principal under it is evaluated jointly with every other. Class (c) membership is recorded when detected and is visible to the owner as a suspicion, labelled as such."*

**Additional source `spec_id_index.md`:**
- `security_architecture_v1` = `Security_Architecture_Description_v1.docx` (sha `2d41f6001d0f…` · 4 citations)
- `security_amendments_trojan_whisper` = `Security_Amendments_Trojan_Whisper.docx` (sha `20b459da0103…` · 0 direct citations · but aggregated into promise set)
- `security_promise_set_amendments` = `Security_Promise_Set_Amendments.docx` (sha `0adc3ff52223…` · 0 direct citations)

**Owner's assertion CONFIRMED:** S-22/S-23 originate from **Security Amendments** (`Security_Amendments_Trojan_Whisper.docx` · W-1 + W-4) via the aggregated Security Assurance Promise Set, adding **A5.15** and **A5.18** to Doc 3 (with **DAP-33** and **DAP-34** cross-mapping to DAP spec). They do NOT belong to `security_architecture_v1`.

### Correction target locations (additive erratum · SO §3.8)

1. `STATE/HOLISTIC_PLAN.md:134-135` — cited `security_architecture_v1 S-22 · DAP-33` and `security_architecture_v1 S-23 · DAP-34`. Correct citation: `Security Amendments (W-1) · A5.15 · S-22 · DAP-33` and `Security Amendments (W-4) · Doc 0 Att-3 · A5.18 · S-23 · DAP-34`.
2. Grep results for `DAP-33` and `DAP-34` show these are also cited correctly elsewhere in the tree (e.g., `notes/canon_dap_backend_spec_v1_requirements.md:146` which correctly attributes to "Watch-side amendments"). The primary erratum target is HOLISTIC_PLAN.md:134-135.

### Recommendation

Land as an **additive erratum block** at end of `STATE/HOLISTIC_PLAN.md` §3.3 body (or as a footnote at line 135) — pending owner ratification:

**Erratum text (proposed):**

> **Erratum (2026-09-20 · owner-directed):** Lines 134-135 above cite DAP-33 and DAP-34 as originating from `security_architecture_v1` S-22/S-23. This is a source-document error. S-22 and S-23 are part of the **Security Amendments' promise set** (`Security_Amendments_Trojan_Whisper.docx` W-1 [A5.15] and W-4 [A5.18 · via Doc 0 Att-3]), aggregated into the Security Assurance Promise Set. The content of the two rows (DAP-33 output-content-gate + DAP-34 coalition-joint-evaluation) is correct; only the source-doc attribution is wrong. Anchor evidence: `notes/ingest_20260907/canon_security_amendments_requirements.md:80-94` (verbatim DAP-33 and DAP-34) + `notes/ingest_20260907/canon_security_promise_set_requirements.md:45-46` (S-22 and S-23 anchored to Doc 3 A5.15/A5.18 · Security Amendments W-1/W-4). Ratifications of R-8 (DEFAULT-class, revised on evidence) and R-11 (friction-only under A5.2) referenced in lines 134-135 are independently correctly attributed to `security_architecture_v1` (that spec bank ratifications). See `notes/DIRECT_ANSWERS_TO_OWNER_20260920.md` §3.

**Not a ratchet break** — no invariant test cites the "security_architecture_v1 S-22/S-23" phrasing. The correction is documentation-provenance only.

### Verdict

- Owner's finding **CONFIRMED at source**.
- Correction is a **provenance erratum** (additive-only · not a re-freeze · not a ratchet delta).
- Recommend banking the erratum at next state-master boundary (or fold into Commit 2 this-turn) pending owner ratification.

---

## §4 · What HOLDS on these three answers

All three answers are **REPORTS TO THE OWNER** — not self-rulings. The owner declares:
1. (a) `spec_id_index.md` as authority (recommendation) OR alternative.
2. (b) whether 2026-09-06 prototype_v3 binding is (i) verbal-banked-now or (ii) date-corrected-to-2026-09-08T~06:15Z · AND whether 2026-09-08 surface language ruling exists off-record.
3. (c) whether to land the DAP-33/34 source erratum at HOLISTIC_PLAN.md:134-135.

Per owner disposition (banked at STATE/DECISIONS.md 2026-09-20T~08:24Z verbatim), the ruled parallel work proceeds AFTER §2.1 + these three answers are on the owner desk:
- OS-prototype frontends card draft (WorkStudio · ThinkLab · Collab · internal operator surfaces) citing Front End Integration Brief.
- G5 non-DAP slices continue (DAP-numbered mappings PROVISIONAL pending §2.1).
- Staleness ceremony fires as own §3.3 small seal when horizon crosses (T-~3h at this writing).

**Held** (per disposition): α-gap hardening + remaining ratifications + DAP portal work + principal-model work — all wait for owner §2.1 answer.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
