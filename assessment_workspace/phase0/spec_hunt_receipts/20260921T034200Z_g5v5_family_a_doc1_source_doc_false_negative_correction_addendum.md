# G5-v5 Second Slice · Family A · Source-Doc Presence Verification Addendum · Prior HUNT False-Negative Correction

**Generated:** 2026-09-21T03:42:00Z
**Wave:** G5-v5 second slice · Family A (Doc 1 M12 chokepoint) · verification addendum (not the HUNT itself)
**Countdown window:** R-91 CEREMONY-OPEN countdown 2026-09-21T03:23:15Z → 2026-09-23T03:23:15Z · this addendum lands inside the window
**Author:** main-agent Autopilot (SO §6 · state-only correction receipt · zero code delta · zero test authoring)

---

## §0 · Owner directive verbatim (2026-09-21T~03:35Z · authority for this addendum)

> "The 'missing canon .md for Doc 1/3/5' line is a CLAIM from a summary — verify against files, never accept. If during G5 slice-2 mapping the Doc-1/Doc-5 canon source docs genuinely cannot be found after scanning `canon/`, `custody/owner_drops/`, and the repo trees, THEN stop-and-report with the scan evidence and I will get an owner ruling on secondary citations vs a source drop. Verify first."

> "session summaries are NEVER evidence of seal state; git log is."

## §1 · Standing-lesson violation caught this-session

Prior Family A HUNT at `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_receipt.md` §4 claimed:

> "Doc 1 canonical source file `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md` is NOT present anywhere in the workspace. Broad search covered `custody/`, `canon/`, `repos/`, `docs/`, `phase0/` — no matches."

**That claim is FALSIFIED against files this-session.** The prior HUNT search did NOT cover `fixtures/`, and the source docs live under `fixtures/files_9_extracted/` with the exact filenames cited by v5 SRR col 9 (only differing in extension: `.docx` on disk vs `.md` in the SRR pointer text).

Owner's binding rule applied: *session summaries are NEVER evidence of seal state* — extends to *HUNT receipts are claims to verify, not treat as sealed truth*.

## §2 · Fresh workspace-wide scan evidence

Command run this-session (2026-09-21T03:41Z):

```
find /app -type f \(
    -name "01_Custody_and_the_Crossing*.md" -o
    -name "05_Direction_Scope_and_Focus*.md" -o
    -name "03_Intent_and_Security_Monitoring*.md" -o
    -name "01_Custody_and_the_Crossing*" -o
    -name "05_Direction_Scope_and_Focus*" -o
    -name "03_Intent_and_Security_Monitoring*"
\) -not -path "*/node_modules/*" -not -path "*/.git/*"
```

Matches (this-session · fully verified):

| File | Exists | SHA-256 |
|---|---|---|
| `fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx` | ✅ | `a33588298100c6224366623e64ac8632b48294649e57ad43cf67ee6730f97844` |
| `fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx`      | ✅ | `f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc` |
| `fixtures/files_9_extracted/03_Intent_and_Security_Monitoring.docx`                 | ✅ | `4c0ff293347d25fef5fc599b7362b7daf9f0a2433fa7e1a06973b1e4770fb5f3` |

No `.md` version of these files exists on disk — only `.docx`. SRR col 9 cites `.md:LINE-N` but v5 SRR was authored referencing filename-matched source (the extension is the pointer's shape, not the truth's shape).

## §3 · Doc 1 rule-content presence verification (A5.1..A5.9 CANON)

Extracted via `python-docx` from `fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx` (96 total paragraphs).

All 9 A5.1..A5.9 CANON rule statements are present verbatim in-line at paragraphs 33–51:

| Rule ID | Paragraph | Opening rule text (verbatim, truncated to 100 char) |
|---|---|---|
| A5.1 | p33 | "A5.1 · The single chokepoint [CANON] There is exactly one function in the entire codebase that i…" |
| A5.2 | p34 | "A5.2 · The custody sequence [CANON] Every model invocation transits three steps in fixed order, a…" |
| A5.3 | p38 | "A5.3 · The per-request envelope does not outlive the call [CANON] The token-to-value mapping is he…" |
| A5.4 | p40 | "A5.4 · Tenant-scoped entity resolution [CANON] De-identification is not limited to what a general…" |
| A5.5 | p41 | "A5.5 · The outbound network is closed except at the crossing [CANON] Exactly one path leaves the…" |
| A5.6 | p44 | "A5.6 · Structural impossibility, not policed prohibition [CANON] The platform's enforcement doctr…" |
| A5.7 | p45 | "A5.7 · The trust receipt [CANON] A trust receipt is emitted per invocation. It is the key-custody…" |
| A5.8 | p50 | "A5.8 · Two custody pathways, both receipted, neither bypassing the other [CANON] The platform has…" |
| A5.9 | p51 | "A5.9 · Grounding failure is a refusal, not a degraded answer [CANON] Where the model returns some…" |

Doc header (p1): `Custody & the Crossing — Part 1: The Chokepoint`. Section heading (p32): `A5 · Technical and behavioural requirements`.

Rule text length per row: ~250–600 chars each (full binding text · not a name-only stub).

## §4 · Doc 5 rule-content presence verification (spot-check)

`fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx` (75 total paragraphs). Family B rule text present:

- p1: `Direction, Scope & Focus — Part 1: The Direction Governor`
- p31: `A5 · Technical and behavioural requirements`
- A5.1..A5.6 CANON rules at p32..p37 (Deterministic by construction / accountability standard / admit-freezes / gate-strict-set-membership / converge-halt / budget-hard-stop).

Full Family B enumeration deferred to Family B HUNT proper (this addendum's scope is Family A block-clear only).

## §5 · Line-numbering discrepancy note (does NOT block canon_ref)

v5 SRR col 9 gives citations like `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:67`. The disk artefact is `.docx` with paragraph-indexed structure — .docx has no native line numbers.

**Non-blocking because** (canonical anchor chain):

1. **Ruling 5 (2026-09-20T~19:00Z):** *canon_ref = v5 SRR only.* Tests bind canon_ref to SRR row (R2..R10 for Doc 1 A5.1..A5.9) — not to the source `file:line`.
2. **Ruling 3 erratum (2026-09-20T~19:00Z):** *class column is a HINT · rule text governs.* Extends to source-column shape: the file:line pointer is a hint at rule-text location, the rule text itself governs. Rule text present verbatim in the `.docx` closes the binding.
3. **SFP-1..7 precedent (R-92 seal `ceaa24f/19030610/e8f9f168`, 2026-09-20T~23:12Z):** SRR col 2 alone was sufficient rule-text carrier for SFP because it was compact-encoded. Doc 1 SRR col 2 carries only rule names (25-70 char), rule text lives in the `.docx` — Ruling 3 erratum + Ruling 5 combined authorises `.docx` as rule-text source.

Result: canon_ref = SRR row (Ruling 5); rule text extracted from `.docx` (Ruling 3 erratum). No `.md:LINE` binding is required by any ruling.

## §6 · Effect on prior HUNT's Options ζ/η/θ/ι surface

Prior HUNT §6 surfaced four options for owner adjudication:

- **Option ζ · Owner-side source-doc drop:** DROPPED. Docs already on disk under `fixtures/files_9_extracted/` — no drop required.
- **Option η · Secondary-citation authoring:** DROPPED. Rule text is available from PRIMARY source (`.docx` under Ruling 3 erratum + Ruling 5) — no secondary source needed.
- **Option θ · Sequence reorder (Family C first):** DROPPED. Owner-directed sequencing (Doc 1 → Doc 5 → DAP → RBM/ROC) holds; block on Family A cleared.
- **Option ι · SRR-Statement-only authoring:** DROPPED. `.docx` gives full rule text; SRR col 2 name-only would be a needless thinning.

**Adjudication is not required.** Family A first sub-slice authoring is cleared to proceed under the standing canonical anchors (Rulings 3, 5) with no new ruling needed.

## §7 · Autopilot posture · Block CLEARED

Prior HUNT §8 status: **Blocked on owner adjudication among Options ζ/η/θ/ι.**
This-addendum status: **Block CLEARED · Family A first sub-slice authoring may open.**

Next autopilot action per SO §6 autonomy + NEXT.md's next-in-flight line:

1. HUNT v5 SRR sheet (sha `00072c58…`) rows R2..R10 (A5.1..A5.9) with full rule text extracted from `.docx` (Ruling 5 canon_ref binding · Ruling 3 erratum rule-text-governs).
2. Draft Family A first-sub-slice test module `backend/tests/invariants/test_g5v5_doc1_a5_1_to_a5_9.py` with 9 property tests binding SRR rows to sealed M12 chokepoint code (`services/chokepoint/*`).
3. RED-first (missing module or missing constants) → GREEN-post via new module `services/canon_doc1_chokepoint/vocabulary.py` (Final[...] constants pattern per R-88..R-92 precedent) OR reuse of existing sealed chokepoint module constants (measurement-only).
4. Pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order · POD audit mirror byte-identical sync.
5. BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 IDENTICAL run1 = run2.
6. §3.3 3-Commit Seal (Commit-A programme/track-a code + Commit-B master state + Commit-C fixup R-6 boundary regen).
7. Report at seal boundary.

## §8 · What this addendum is NOT

- NOT the Family A HUNT itself — that lives at `20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_receipt.md`.
- NOT the Family A test module — that authoring is the NEXT step (this addendum only clears the block).
- NOT a proposal to amend any ruling — the block-clear rides on existing Rulings 3 & 5.
- NOT a scope-broadening — Family A first sub-slice is what it always was; only the perceived block is dissolved.

## §9 · Canon anchors verbatim

- Owner directive this-session verbatim (2026-09-21T~03:35Z · "*verify against files, never accept … Verify first*").
- Owner standing lesson from prior-fork misreport ("*session summaries are NEVER evidence of seal state; git log is*") — extended to HUNT-receipt claims this-session.
- Owner Ruling 5 SRR-as-authority (2026-09-20T~19:00Z · v5 workbook sha `00072c58…`).
- Owner Ruling 3 erratum (2026-09-20T~19:00Z · *class column is a HINT · rule text governs*).
- Owner G5-v5 second slice sequencing (2026-09-21T~01:00Z · Doc 1 → Doc 5 → DAP → RBM/ROC).
- v5 SRR workbook (custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx · sha `00072c58…`) rows R2..R10 = Doc 1 A5.1..A5.9.
- R-92 seal `ceaa24f/19030610/e8f9f168` (SFP-1..7 precedent for Ruling-5 authoring).
- R-91 CEREMONY-OPEN commit `a30db4f7` (this-session · countdown window horizon 2026-09-23T03:23:15Z).
- Prior HUNT receipt `20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_receipt.md` (this-session · superseded §4 negative claim by this addendum).
- SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §6 autopilot governance + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary.

## §10 · Cross-refs

- Prior HUNT: `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_receipt.md` (§4 corrected by this addendum).
- Prior HUNT data JSON: `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_data.json` (§7 note: source_doc_present = TRUE with this addendum superseding).
- R-91 ceremony proposal: `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` (unaffected by this addendum · applies at horizon).
- SRR workbook: `custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx`.
- Source doc: `fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx` (sha `a33588…` this-session).

**END OF ADDENDUM.**
