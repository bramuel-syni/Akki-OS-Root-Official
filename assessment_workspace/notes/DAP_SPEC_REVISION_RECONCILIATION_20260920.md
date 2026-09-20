READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# DAP_SPEC_REVISION_RECONCILIATION_20260920.md

**§2.1 revision-reconciliation report to owner (evidence-based · NOT a self-ruling · owner declares canon).**

**Authored:** 2026-09-20T~08:35Z under owner directive verbatim 2026-09-20T~08:24Z (banked at `STATE/DECISIONS.md` 2026-09-20T~08:24Z OWNER DISPOSITION section) execution-order item 1.

**Standing law confirmed:** every factual claim below comes from a file opened this session (SO §6.1 files-are-truth · client's binding rule). Every path is repo-relative or absolute. Additive-only per SO §3.8.

**Scope frozen (SO §6.4 NOTHING-BEYOND):** answer §2.1 with file evidence · locate all revisions the session's rulings cited · report where DAP-6..30 grouping diverges · recommend canon WITH evidence. Owner declares canon.

---

## §1 · The question, verbatim from the DAP Backend Engineering Brief §2.1

> `STATE/HOLISTIC_PLAN.md` §3.3 describes `dap_backend_spec_v1` §4 as defining DAP-1..DAP-30 "grouped by concern (admission → controlled units → chokepoint → governed queries → row execution → audit → coalition-joint-evaluation → cumulative disclosure budget → component-boundary inspection)."
>
> The copy at `spec/dap_backend.txt` — the one §5 of this brief reviews line by line — groups them differently:
>
> | Range | `spec/dap_backend.txt` (reviewed here) | `HOLISTIC_PLAN` W-DAP-STACK wave mapping |
> |---|---|---|
> | DAP-1..5 | External-party principal | Admission + principal registry — **agrees** |
> | DAP-6..10 | Six crossing profiles | Controlled unit registry — **diverges** |
> | DAP-11..15 | Raw download · admission & keys · approval | Chokepoint per data source — **diverges** |
> | DAP-16..20 | Approval · extraction | Governed query authoring — **diverges** |
> | DAP-21..25 | Metering & receipts · owner config | Row execution + chokepoint receipt — **diverges** |
> | DAP-26..30 | Owner config · failure posture | Cumulative disclosure budget — **diverges** |
>
> Only DAP-1..5 aligns. **This is the single most important finding in this review.**

Source: `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` sha256 `3c9be71541534942d3c3038c24cc8981aea38667a3a2e521043810a23c5085fe` (§4.1 §F pinned) · §2.1 lines 130–155 of the brief.

---

## §2 · Revision inventory — every dap_backend_spec_v1 revision this session's rulings could have cited

Located by exhaustive filesystem search under `/app/**` (excluding `.git` and `custody/owner_drops/` since custody was intake-only at 2026-09-20T~08:24Z).

| # | Path (abs) | sha256 | Size | Kind | Notes |
|---|---|---|---|---|---|
| 1 | `/app/assessment_workspace/canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` | `e675990aa68e75141f41b418fd19c0a2c05b70441c6217ebdde44e5362c55263` | 21,346 B | docx (raw canon drop) | Canon-ingested spec drop of 2026-09-09 · **BANKED in `notes/spec_id_index.md` as `dap_backend_spec_v1`** with `citation_count=13` · opening_signature source. |
| 2 | `/app/assessment_workspace/canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | (extracted-text derivative of #1) | — | txt extraction | Extracted text of #1's docx bytes · consumed by `notes/canon_dap_backend_spec_v1_requirements.md` as its source. |
| 3 | `/app/assessment_workspace/notes/canon_dap_backend_spec_v1_requirements.md` | (session ingest note) | — | md | Session ingest note enumerating DAP-1..30 from #2 + amendment additions from Pruning_Unlearning_Amendment_v1 + Serving_Integrity_Amendment_v1. |
| 4 | `/app/assessment_workspace/phase0/tracking_defect_20260908/grep_dap_backend_spec_v1.txt` | (grep artefact) | — | txt | Grep-tracking artefact from 2026-09-08 spec-ID tracking defect fix. Not a spec revision. |

**Reviewer's spec (`spec/dap_backend.txt` at `bramuel-syni/Akki-OS-Root` @ `main` tree `07fb08f34a34`)** is NOT in our tree (we have `Akki-OS-V1`, `Akki-Executive-Core`, `Akki-Executive-Final`, `Extraction-Akki`, `RMS-IQ-Core-2` — not `Akki-OS-Root`). We compare against #2's raw extracted text bytes as the on-disk canon anchor.

---

## §3 · What the on-disk canon spec (revision #1/#2) ACTUALLY defines · DAP-1..30 grouping · with anchor lines from the extracted-text bytes

Reading `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` line by line:

| Range | Section header verbatim | Requirements listed |
|---|---|---|
| **§3 · The External-Party Principal** | "3   The External-Party Principal" | DAP-1 · DAP-2 · DAP-3 · DAP-4 · DAP-5 |
| **§4 · The Six Crossing Profiles** | "4   The Six Crossing Profiles" | DAP-6 · DAP-7 · DAP-8 · DAP-9 · DAP-10 · DAP-11 |
| **§5 · Back-End Services · Admission & keys** | "5   Back-End Services" then subheader "Admission & keys" | DAP-12 · DAP-13 |
| **§5 · Back-End Services · Approval** | "Approval" subheader | DAP-14 · DAP-15 · DAP-16 · DAP-17 |
| **§5 · Back-End Services · Extraction** | "Extraction" subheader | DAP-18 · DAP-19 · DAP-20 |
| **§5 · Back-End Services · Metering & receipts** | "Metering & receipts" subheader | DAP-21 · DAP-22 · DAP-23 · DAP-24 |
| **§5 · Back-End Services · Estate-owner configuration** | "Estate-owner configuration" subheader | DAP-25 · DAP-26 · DAP-27 |
| **§6 · Failure Posture** | "6   Failure Posture" | DAP-28 · DAP-29 · DAP-30 |

**No DAP-31, DAP-32, DAP-33, DAP-34, DAP-35, DAP-36, DAP-37, or DAP-38 exist in this bytes-source.** Those numbers arrive via AMENDMENT docs (see §5 below).

---

## §4 · Comparison — Reviewer's brief §2.1 grouping VS on-disk canon spec structure VS HOLISTIC_PLAN.md §3.3 paraphrase

| Range | On-disk canon spec (revision #1/#2) · verbatim section boundary | Reviewer's `spec/dap_backend.txt` §2.1 table | HOLISTIC_PLAN.md §3.3 paraphrase |
|---|---|---|---|
| DAP-1..5 | §3 External-Party Principal | External-party principal | Admission + principal registry |
| DAP-6..10 | §4 Six Crossing Profiles (DAP-6..10 inside; DAP-11 is last row same §) | Six crossing profiles | Controlled unit registry |
| DAP-11..15 | §4 tail (DAP-11) + §5 Admission & keys (DAP-12, DAP-13) + §5 Approval (DAP-14, DAP-15) | Raw download · admission & keys · approval | Chokepoint per data source |
| DAP-16..20 | §5 Approval (DAP-16, DAP-17) + §5 Extraction (DAP-18, DAP-19, DAP-20) | Approval · extraction | Governed query authoring |
| DAP-21..25 | §5 Metering & receipts (DAP-21, DAP-22, DAP-23, DAP-24) + §5 Estate-owner configuration (DAP-25) | Metering & receipts · owner config | Row execution + chokepoint receipt |
| DAP-26..30 | §5 Estate-owner configuration (DAP-26, DAP-27) + §6 Failure Posture (DAP-28, DAP-29, DAP-30) | Owner config · failure posture | Cumulative disclosure budget |

**Structural verdict:** the reviewer's grouping and the on-disk canon spec grouping are **STRUCTURALLY IDENTICAL** at the section-header level. Both agree on:
- DAP-1..5 = External-party principal (§3)
- DAP-6..10 (+ DAP-11) = Six crossing profiles (§4)
- DAP-11 straddling into "Raw download" is expected — DAP-11 IS the raw-download row of §4 Table 2
- DAP-12+ = Back-End Services sub-sections (§5)
- DAP-28+ = Failure Posture (§6)

**HOLISTIC_PLAN.md §3.3's paraphrase** ("grouped by concern (admission → controlled units → chokepoint → governed queries → row execution → audit → coalition-joint-evaluation → cumulative disclosure budget → component-boundary inspection)") **does NOT match** the on-disk canon spec's actual section structure. The reviewer's finding is correct: **HOLISTIC_PLAN.md §3.3 is inaccurate** as a paraphrase of the canon spec.

---

## §5 · What HOLISTIC_PLAN.md §3.3 says verbatim · and where its paraphrase originates

Located at `STATE/HOLISTIC_PLAN.md:117-119`:

> ### 3.3 · W-DAP-STACK — nine waves scoping `dap_backend_spec_v1` DAP-1..DAP-30
>
> **What we're building:** The **Data Access Portal (DAP)** backend and its ceremony machinery — the gate every request for data-outside-the-platform must cross. `dap_backend_spec_v1` §4 defines DAP-1..DAP-30 as thirty ordered requirements grouped by concern (admission → controlled units → chokepoint → governed queries → row execution → audit → coalition-joint-evaluation → cumulative disclosure budget → component-boundary inspection). Owner asked for the plan carved into **9 waves** matching those nine concerns.

**HOLISTIC_PLAN.md authored** 2026-09-09 under owner directive 2026-09-09T~12:55Z (per file header). Same day as the canon drop of the DAP spec (2026-09-09). Same day as `spec_id_index.md` generation (2026-09-09T11:45:41Z).

**Observation:** the HOLISTIC_PLAN's paraphrase is a "grouped by concern" wave-decomposition planning-narrative, NOT a re-statement of the canon spec's actual section headers. The DAP spec's actual grouping is by **type of governance surface** (External-party principal · Six crossing profiles · Back-End Services · Failure Posture) — not by "concern" as HOLISTIC_PLAN paraphrases.

**No evidence of a second, later, or diverging revision of `dap_backend_spec_v1`** on disk anywhere in our tree. The 9-wave "grouped by concern" narrative in HOLISTIC_PLAN.md §3.3 appears to be a PLANNING PARAPHRASE authored on-the-fly, not a re-anchoring on a different revision of the spec.

---

## §6 · Amendment additions on top of DAP-1..30 · what makes DAP-31..38 exist

Located at `notes/canon_dap_backend_spec_v1_requirements.md:11` (banked from raw canon drop 2026-09-09):

> **Amended by.** `Pruning_Unlearning_Amendment_v1` (T-3 → new DAP-37; T-4 → new DAP-38) · `Serving_Integrity_Amendment_v1` (V-2 → new DAP-31+, DAP-32+).

Additional amendments cited elsewhere in the tree:

| Amendment DAP number | Source amendment doc | Anchor evidence |
|---|---|---|
| DAP-31+, DAP-32+ | `Serving_Integrity_Amendment_v1` (drop 2026-09-13) | `STATE/PINS.md` records this drop · reviewer's brief §2.1 also cites it |
| DAP-33 | Security Amendments · W-1 · A5.15 in Doc 3 (proposed) | `notes/ingest_20260907/canon_security_amendments_requirements.md:80-83` (verbatim) · `notes/ingest_20260907/canon_security_promise_set_requirements.md:45` (S-22 promise) |
| DAP-34 | Security Amendments · W-4 · A5.18 in Doc 3 (proposed) via Att-3 addition | `notes/ingest_20260907/canon_security_amendments_requirements.md:91-94` (verbatim) · `notes/ingest_20260907/canon_security_promise_set_requirements.md:46` (S-23 promise) |
| DAP-35 | Security Amendments · onward | `notes/W_DAP_STACK_2H_close.md:74` (DAP-34, 35, AC-10) · `notes/W_M3_SW11_DAP33_DAP34_DAP35_M3_REMAINDER_close.md:3` |
| DAP-36 | (front-end-implied per reviewer's §7) | reviewer's brief §7 (P-1..P-6 relabelled DAP-36..DAP-40) |
| DAP-37 | `Pruning_Unlearning_Amendment_v1` T-3 | `notes/canon_dap_backend_spec_v1_requirements.md:11` |
| DAP-38 | `Pruning_Unlearning_Amendment_v1` T-4 | `notes/canon_dap_backend_spec_v1_requirements.md:11` |

**Conclusion:** DAP-31 through DAP-38 do NOT exist in the core `dap_backend_spec_v1` bytes. They are AMENDMENT-additions from separate documents. The reviewer's spec (revision #1/#2) STOPS AT DAP-30 — which matches our tree.

---

## §7 · Do CCS2/CCS3 freezes anchor on the correct revision?

**Direct check:** the CCS2 freeze anchored on:
- `_DAP_SIX_PROFILES` closed 6-tuple (`browse · connect_api_key_by_external_workspace · extract_processed_intelligence · fine_tune_model_on_estate_data · develop_skills_against_estate_data · download_raw_data`) — matches on-disk spec §4 Table 2 verbatim ✓
- DAP-1 principal fields (legal identity · declared governance posture · terms · trust domain identifier · admission-time mandate) — matches on-disk DAP-1 verbatim ✓
- DAP-13 API key contract (per party principal never per organisation · single-act revocable · stated lifetime · key material never in receipts) — matches on-disk DAP-13 verbatim ✓
- Six-profile matrix cited as "DAP-Spec §4 verbatim" — matches on-disk §4 verbatim ✓

**CCS3 freeze** anchored on:
- MeteredEvent 7 DAP-Spec-verbatim fields (operation_type · accessed_scope · quantity · quantity_unit · terms_id · party_id · timestamp_iso · R-C2 au_3b_defensible) — matches on-disk DAP-21 verbatim ✓
- reliable_time_source wiring cited as "DAP-Spec DAP-21 verbatim" — matches on-disk DAP-21 wording ✓

**Verdict:** CCS2/CCS3 freezes anchor on the **on-disk canon spec** (`e675990a…` docx · 21,346 B). No revision drift risk in the ratchet. If owner declares that revision canon, the freezes are correct as-is.

---

## §8 · Recommendation to owner (evidence-based · NOT a self-ruling)

The owner declares canon. My evidence supports the following recommendation:

**RECOMMEND CONFIRMING** `canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` sha256 `e675990aa68e75141f41b418fd19c0a2c05b70441c6217ebdde44e5362c55263` (21,346 B · draft dated 5 September 2026) **AS CANON** for `dap_backend_spec_v1`.

**Basis (evidence):**
1. This is the sole `dap_backend_spec_v1` file bytes on disk under `canon/drops/**` — no competing revision exists.
2. Its §3–§6 section-header grouping structurally matches the reviewer's `spec/dap_backend.txt` grouping in §2.1.
3. It is banked as canon in `notes/spec_id_index.md` at `dap_backend_spec_v1` row with 13 citations from other canon docs (opening_signature source · byte-verified).
4. `notes/canon_dap_backend_spec_v1_requirements.md` — the session's authoritative ingest doc — enumerates DAP-1..30 EXACTLY as they appear in the on-disk extracted text.
5. All CCS1/CCS2/CCS3 freezes made this session anchor on this revision's field sets, closed-tuples, and verbatim wording; no drift.

**RECOMMEND CORRECTING** `STATE/HOLISTIC_PLAN.md:117-119` via additive erratum (NOT overwrite · SO §3.8):

**Erratum text (proposed · to append at end of §3.3 body — pending owner ratification):**

> **Erratum (2026-09-20 · owner-directed via §2.1 reconciliation):** The above paraphrase — "grouped by concern (admission → controlled units → chokepoint → governed queries → row execution → audit → coalition-joint-evaluation → cumulative disclosure budget → component-boundary inspection)" — is a wave-decomposition planning narrative, NOT the canon spec's actual section grouping. The on-disk canon spec (`canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` sha256 `e675990aa68e75141f41b418fd19c0a2c05b70441c6217ebdde44e5362c55263` · draft 5 September 2026) groups DAP-1..30 by governance surface: §3 External-Party Principal (DAP-1..5) · §4 The Six Crossing Profiles (DAP-6..11) · §5 Back-End Services (DAP-12..27 · subsections: Admission & keys · Approval · Extraction · Metering & receipts · Estate-owner configuration) · §6 Failure Posture (DAP-28..30). See `notes/DAP_SPEC_REVISION_RECONCILIATION_20260920.md` §3-§4 for the full section-anchor evidence.

**No revision drift** — CCS2/CCS3 freezes are correctly anchored on the recommended canon. If owner ratifies this recommendation, no ratchet regression risk; no re-freeze needed.

**If owner declares a different revision canon** (e.g., a later revision we do not have on disk), then:
- CCS2/CCS3 freezes MUST be re-audited against that revision's DAP-1..30 field sets and wording.
- HOLISTIC_PLAN.md §3.3's paraphrase may still be incorrect (a planning-paraphrase mismatch is separate from a revision drift).
- The DAP portal work + principal-model landing MUST be scoped from the newly-declared canon revision.

---

## §9 · Provenance-chain fingerprint (for owner audit)

- **Sourced files opened this session (SO §6.1):**
  - `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` (sha256 `3c9be715…`) — reviewer's §2.1 verbatim + full brief.
  - `notes/spec_id_index.md` + `notes/spec_id_index.json` — canonical `{id, filename, sha256}` index.
  - `STATE/HOLISTIC_PLAN.md:117-119` — the paraphrase source.
  - `notes/canon_dap_backend_spec_v1_requirements.md` — session ingest doc header (line 11: Amended-by).
  - `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` — raw extracted bytes of #1's docx (§3-§6 section structure verified line-by-line).
  - `notes/ingest_20260907/canon_security_amendments_requirements.md:80-94` — DAP-33/34 amendment provenance.
  - `notes/ingest_20260907/canon_security_promise_set_requirements.md:45-46` — S-22/S-23 promise-set anchor.
- **No file was quoted from README, filename-only inference, or prior-turn recollection.** All claims are file-anchored.

---

## §10 · What HOLDS on this report

Per owner disposition (banked at STATE/DECISIONS.md 2026-09-20T~08:24Z verbatim):
1. **DAP portal work + principal-model work HOLD** until owner ratifies the canon revision.
2. **α-gap hardening wave + remaining ratifications HOLD ONE TURN** pending §2.1 answer.
3. **G5 DAP-numbered slice mappings** carry a PROVISIONAL tag pending owner ratification of canon revision.
4. **CCS2/CCS3 freezes** are unaffected (owner reaffirmed R-19/R-20/R-21 unaffected; α-gap findings BANKED pending ratification, not re-frozen).

**Owner action required:** declare canon revision (this report recommends `e675990aa68e…` docx of 2026-09-09 · full evidence in §8).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
