# G5-v5 Second Slice · Family A HUNT · Doc 1 M12 chokepoint · SOURCE-DOC-MISSING FINDING

**Generated:** 2026-09-21T03:33:30Z
**Wave:** G5-v5 second slice · Family A (Doc 1 M12 chokepoint) · Tier A first sub-slice HUNT
**Countdown window:** R-91 CEREMONY-OPEN countdown 2026-09-21T03:23:15Z → 2026-09-23T03:23:15Z · this HUNT lands inside the window per owner "do NOT idle" directive
**Author:** main-agent Autopilot (SO §6 · state-only spec-hunt · zero code delta · zero test authoring)

---

## §0 · Owner ruling this-session verbatim (2026-09-21T~01:00Z · authority for this HUNT)

> "G5-v5 SECOND SLICE ORDER — by sealed component, Tier A first, owner verbatim sequencing: 'Map the rows whose components are already built and sealed, so canon_ref bites on live code: Document 1 (chokepoint, M12) and Document 5 (the Ledger, M10) first; then DAP-1 through DAP-38 (lifecycle and principal model landing); then RBM and ROC (Rules Service). Tier B rows in each family trail their Tier A. Sequence rows 1–565 accordingly.' Slice sizes at your autopilot discretion for clean seals; report the slicing plan (families → slice boundaries → estimated invariant counts) in the next seal report."

> "Follow the banked ceremony mechanics; do not invent."

## §1 · HUNT method

Loaded v5 SRR workbook (sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`) from `custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx` (Ruling 5 authority). Read "System Rules Registry" sheet (603 rows × 11 cols). Enumerated Doc 1 rows (14 total · 11 CANON + 2 RULED + 1 "—"). Focus scope: 9 CANON A5.1..A5.9 rows (R2..R10) as Tier A first sub-slice.

## §2 · Doc 1 A5.1..A5.9 · SRR row extraction (verbatim)

| Rule ID | SRR Row | Status | Statement (col 2 verbatim) | Source (col 9 verbatim) |
|---|---|---|---|---|
| A5.1 | R2 | CANON | "The single chokepoint" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:67` |
| A5.2 | R3 | CANON | "The custody sequence" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:69` |
| A5.3 | R4 | CANON | "The per-request envelope does not outlive the call" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:77` |
| A5.4 | R5 | CANON | "Tenant-scoped entity resolution" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:81` |
| A5.5 | R6 | CANON | "The outbound network is closed except at the crossing" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:83` |
| A5.6 | R7 | CANON | "Structural impossibility, not policed prohibition" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:89` |
| A5.7 | R8 | CANON | "The trust receipt" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:91` |
| A5.8 | R9 | CANON | "Two custody pathways, both receipted, neither bypassing the other" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:101` |
| A5.9 | R10 | CANON | "Grounding failure is a refusal, not a degraded answer" | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:103` |

**HUNT data JSON banked at:** `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_data.json` (also carries `objective` + `promise_source` + `domain` fields · full 9-row measurement).

Column 4 (Promise/Source Document) verbatim for all 9 rows: `#1 — NO LEAKAGE OF CONFIDENTIAL INFORMATION`.
Column 3 (Objective) verbatim for all 9 rows: `O1 Custody & Confidentiality`.
Column 8 (Domain) verbatim for all 9 rows: `SyniSense`.

## §3 · Sealed live code map (canon_ref bites)

Sealed M12 chokepoint code at `repos/Extraction-Akki/backend/services/chokepoint/`:
- `__init__.py` (`register_crossing`, `CrossingReceipt`, `ChokepointRefused`, `list_receipts`) — docstring cites `Doc 01 §A5.1/§A5.5/§A5.6/§A5.7`.
- `router.py` (`/api/shield/dry-run`, `/api/shield/receipts`, `/api/shield/allowlists`) — docstring cites `Doc 01 §A5.7`.
- `llm.py`, `llm_endpoint_allowlist.py`, `llm_purpose_gate.py`, `masking_tier.py`, `residency.py`, `policy_integrity.py`, `dry_run.py` + JSON+SHA256 allowlist files.

Sealed M12 tests at `repos/Extraction-Akki/backend/tests/invariants/`:
- `test_chokepoint_registers_all_crossings.py` — quotes A5.1 + A5.5 + A5.6 verbatim in docstring (extracted at W3 seal 2026-08-25).
- `test_llm_chokepoint_sole_importer.py`.
- `test_m12_w1_llm_chokepoint_callsite_level_negative_scan.py`.
- `test_m12_w1b_sec1_policy_integrity.py`.
- `test_m12_w1c_sec1_policy_integrity_runtime_wire.py`.
- `test_m12_w1d_dap7_custody_option_d.py`.
- `test_m12_w1f_watch_input_seat_lango_scoring.py`.
- `test_m12_w1g_closed_outbound_network.py`.
- `test_m12_w1h_d16_d17_structural_prohibitions.py`.
- `test_m12_w1i_tcb_chokepoint_golden_input_byte_identical.py`.
- `test_emit_moac_chokepoint_admission.py`.

Sealed code covers A5.1 + A5.5 + A5.6 + A5.7 substantively. A5.2 (custody sequence), A5.3 (per-request envelope), A5.4 (tenant-scoped resolution), A5.8 (two pathways), A5.9 (grounding failure) are not each cited by their own sealed test but are implied by the codebase-wide chokepoint discipline.

## §4 · **HUNT-OUTCOME FINDING · SOURCE-DOC MISSING**

**Doc 1 canonical source file `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md` is NOT present anywhere in the workspace.** Broad search covered `custody/`, `canon/`, `repos/`, `docs/`, `phase0/` — no matches. The SRR Source column (col 9) cites lines 67-159 of that file for the 14 Doc 1 rows.

**Same pattern for Family B (Doc 5 M10 Ledger):** all 11 rows cite `05_Direction_Scope_and_Focus_Part_1_Northena.md` — MISSING from workspace.

**Same pattern for Doc 3 (SFP-2 base authority):** cites `03_Intent_and_Security_Monitoring.md` — MISSING from workspace.

**Family C (DAP-*) source doc EXISTS:** `DAP_Backend_Spec_v1.docx` per SRR col 9 — a docx of that name doesn't exist under that exact filename, but a related brief `DAP_Backend_Engineering_Brief.md` exists at `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` (measured this session).

## §5 · Deviation from G5-v5 SFP-1..7 first-slice precedent

**SFP precedent** (Ruling 5 · sha-pinned v5 SRR rows 597-603): the SRR Statement column (col 2) contained the FULL pipe-delimited rule text (~2000 chars, 7 rules concatenated at row 597). Rule text was DIRECTLY inline in SRR — no external source doc needed for authoring.

**Doc 1 / Doc 5 / Doc 3 pattern**: SRR Statement column contains only the BRIEF rule NAME (25-70 chars per row). Rule text lives in the source `.md` files (which are missing from disk).

**This is a pattern-shape divergence between the SFP-1..7 slice (compact-encoded · self-contained SRR row) and the Doc-N canon rows (registry-indexes-into-source-doc pattern).**

## §6 · Options surface (adjudication required)

- **Option ζ · Owner-side source-doc drop**: owner drops the 2 canonical `.md` files (`01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md` + `05_Direction_Scope_and_Focus_Part_1_Northena.md`) into `custody/owner_drops/` under a timestamped directory. Autopilot proceeds with Ruling-5-compliant authoring (rule text verbatim from md).
- **Option η · Secondary-citation authoring**: autopilot proceeds authoring Family A + B tests using SEALED-TEST DOCSTRING QUOTES as the rule text carrier (e.g., `test_chokepoint_registers_all_crossings.py:5-12` for A5.1/A5.5/A5.6). Cite each secondary source at test authoring. This diverges from SFP precedent but preserves canon_ref-bites-on-live-code.
- **Option θ · Sequence reorder**: autopilot pivots Family C (DAP-*) FIRST during the countdown window (source doc EXISTS at `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md`), returns to Family A + B after owner-side source drops (Option ζ) OR authorizes secondary citations (Option η). This violates owner's explicit sequencing ("Doc 1 and Doc 5 first") — requires owner override.
- **Option ι · SRR-Statement-only authoring**: autopilot authors tests using only the SRR col 2 brief statement (25-70 chars) as rule text · cite col 9 as source_of_record pointer (missing on disk but registered) · assert against sealed code shape. Thinnest binding · unclear whether it meets Ruling-5 "rule text governs" bar with a 3-word rule name.

## §7 · What this HUNT is NOT

- NOT the G5-v5 Family A test authoring itself — this is a spec-hunt receipt only.
- NOT a proposal to amend the ceremony-open decision (that is R-91 apply-scope · this-HUNT is separate G5-v5 slice work).
- NOT authorization to proceed with any of ζ/η/θ/ι without owner adjudication.
- NOT a scope-broadening beyond Family A first sub-slice (per SO §6.4 NOTHING-BEYOND).

## §8 · Autopilot posture

**Blocked on owner adjudication among Options ζ/η/θ/ι.**

Not-idle actions available during the block:
- Continue enumerating Family C (DAP-*) canon_ref bindings against `services/dap_lifecycle/` and `contracts/principal_v1.py` (pre-work · does NOT commit test files).
- Continue enumerating Family D (RBM + ROC) canon_ref bindings against `services/rules_service/`.

The R-91 apply-step at horizon 2026-09-23T03:23:15Z is unaffected by this HUNT — apply is independent of G5-v5 second-slice progress. R-91 seal will fire at horizon regardless of G5-v5 slice completion.

## §9 · Canon anchors verbatim

- Owner ruling this-session (2026-09-21T~01:00Z · G5-v5 SECOND SLICE ORDER verbatim).
- Owner Ruling 5 SRR-as-authority (2026-09-20T~19:00Z · v5 workbook sha `00072c58…`).
- Owner Ruling 3 erratum (2026-09-20T~19:00Z · class column HINT · rule text governs).
- R-91 CEREMONY-OPEN commit `a30db4f7` (this-session · establishes countdown window).
- R-92 SFP-1..7 first-slice seal `ceaa24f/19030610/e8f9f168` (immediately-precedes G5-v5 second slice).
- Sealed W3 chokepoint test file `repos/Extraction-Akki/backend/tests/invariants/test_chokepoint_registers_all_crossings.py` (2026-08-25 authoring · quotes Doc 01 §A5.1/A5.5/A5.6 verbatim).
- Sealed chokepoint module `repos/Extraction-Akki/backend/services/chokepoint/__init__.py` (docstring cites Doc 01 §A5.1/A5.5/A5.6/A5.7).
- SO §2.5 verbatim-docstring + §3 tests-first + §3.8 additive-only + §6.4 NOTHING-BEYOND.

## §10 · Cross-refs

- HUNT data JSON at `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_data.json` (this-turn banked).
- R-91 proposal at `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` (ceremony-open).
- R-91 ceremony-open banking in STATE/DECISIONS.md at `a30db4f7`.
- Sequencing plan sketch in STATE/PINS.md R-91-CEREMONY-OPEN-PINS block · Family A/B/C/D scaffolding.

**END OF HUNT RECEIPT.**
