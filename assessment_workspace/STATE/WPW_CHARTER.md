# WPW · Whitepaper Wizard v1 · Wave Charter

**Authored:** 2026-08-31 · main agent · under owner ruling 7 (`STATE/DECISIONS.md`, this session).
**Ingest:** `canon/fixtures/whitepaper_wizard_spec_v1/` (raw docx sha256=`7b51c5adf275ab176a18fa6a9277c593139ec6a132b7b5c923227153e4be5fed`; extracted text; README).
**Discipline:** tests-first, thin-kernel, no-bypass, double-green ratchet, no push. Every requirement below cites the WPW-N or A-N tag from the spec verbatim.

---

## 1 · Executive framing

The wizard is a research observer — read-only, event-driven, attached at commissioning of every training run (WPW-1, WPW-2). It carries a 3-tier evidence ladder:

- **Tier 1 — Notebook.** Contemporaneous, append-only, hash-chained on the Doc 5 Ledger-writer pattern. Exists for every run, including refused ones. (WPW-3, WPW-4, WPW-5, WPW-6, WPW-7)
- **Tier 2 — Technical Report.** Drafted automatically when a run settles, fixed section skeleton, every figure resolves to a run artefact. Internal — never crosses the outer gate. (WPW-8, WPW-9, WPW-10)
- **Tier 3 — White Paper.** Eligibility is mechanical (exceptional threshold + novelty gate — WPW-11, WPW-12). Assembly draws only from Tier 1/2/run record — no post-hoc narrative reconstruction (WPW-13). Redaction is a classification-driven gate, not a prompt (WPW-14). External release is a separate outer-gate egress crossing (WPW-15).

Three parked owner rulings block Tier 3 firing (R1, R2, R3). Tiers 1 and 2 are FULLY SPECIFIED AND BUILDABLE AS WRITTEN (§7 verbatim: *"Nothing in this spec is blocked by the parked rulings except Tier 3's final firing condition (R1) and the release ceremony (R2). Tiers 1 and 2 are fully specified and buildable as written."*)

---

## 2 · Sub-wave breakdown (per SPRINT_PLAN.md line W-WPW-v1)

### W-WPW-v1-a · Spec ingest (**✅ CLOSED 2026-08-31**)
- Raw docx banked at `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx` (15,858 bytes, sha256 recorded).
- Extracted text at `canon/fixtures/whitepaper_wizard_spec_v1/spec.extracted.txt` (10,687 bytes, 90 lines) — marked as derived; verbatim quotes in downstream test docstrings must spot-check against the docx.
- Discipline banked in `canon/fixtures/whitepaper_wizard_spec_v1/README.md`.

### W-WPW-v1-b · Charter + reuse assessment (**this document** · ½ day)
- ✅ Charter drafted (this file).
- ✅ Reuse assessment against donor repos + Wave-H receipts (below).
- ✅ R1/R2/R3 framed crisply for single-shot owner ruling (below).

### W-WPW-v1-c · Tier 1 (Lab Notebook) — buildable now · ~½ day
Implements: WPW-1, WPW-2, WPW-3, WPW-4, WPW-5, WPW-6, WPW-7, WPW-18, plus A1, A2, A6.

Scope:
- **Attach at commissioning.** New module `backend/services/wpw/tier1_notebook.py` registers a callback into `training_runner` at run-commissioning time. No per-run opt-in (WPW-1). Zero-influence check via A2-shape test (bit-identical training outcomes with wizard attached vs detached).
- **Event-driven capture** (WPW-3): minimum event set = commissioning reflection · baseline selection record (Promise #24) · checkpoints · each acceptance-criterion transition · every CIF ideation event · every human contribution event · anomalies · cost checkpoints against estimate. All fed from existing `training_runner` state + Doc-5 Ledger reads.
- **Append-only, hash-chained** (WPW-4): notebook entries land on the Doc 5 Ledger-writer pattern. Each entry carries: `timestamp`, `run_artefact_ref`, `evidence_class` ∈ {measured, estimated, observed}. Test A1 (notebook completeness): scripted run replay must find every event, classed + source-linked, none invented.
- **Human contribution events** (WPW-5): `actor`, `state_before`, `change`, `movement_after` — correlation-only, causal reading refused.
- **CIF ideation events** (WPW-6): mirrored by reference to `cif_spec_v1` artefacts. No paraphrase.
- **Retention on refused runs** (WPW-7): notebook survives refusal (test A6).
- **Economics** (WPW-18): observation cost as budget line on the run estimate + surfaced as anomaly if exceeded.

Deliverables:
- `backend/services/wpw/tier1_notebook.py` + append-only schema.
- Test module `backend/tests/invariants/test_wpw_tier1_notebook.py` (RED → GREEN → ratchet).
- Zero-influence invariant (A2-shape): identical run outcomes with wizard attached vs detached.

### W-WPW-v1-d · Tier 2 (Technical Report) — buildable now · ~½ day
Implements: WPW-8, WPW-9, WPW-10, plus A4, A6.

Scope:
- **Draft on settle** (WPW-8): auto-emit a Tier-2 report when a run settles (accepted OR refused). Fixed section skeleton:
  1. Problem & objective (from commissioning reflection).
  2. Data statement at datasheet level, classification-driven — **reuses the pattern from tonight's estate-text training run** (per owner ruling 7 verbatim: *"That framing IS the product's credibility. It also maps directly onto the WPW evidence-class discipline"*).
  3. Baseline record (from Promise #24).
  4. Method — including adopted ideation events.
  5. Setup & reproducibility — hardware, duration, cost actual-against-estimate, seeds.
  6. Results on held-out material — all six acceptance criteria and their numbers.
  7. Ablations where run.
  8. Limitations.
  9. Negative results.
- **Figure traceability** (WPW-9): every figure carries evidence class + receipt line resolving to a run artefact. Unresolvable figure MUST NOT render (test A4: 100% resolve).
- **Internal only** (WPW-10): reports never cross the outer gate.
- **Refused-run report** (test A6): a run failing acceptance produces a Tier-2 report with the refusal + numbers, not a hollow shell.

Deliverables:
- `backend/services/wpw/tier2_technical_report.py` + fixed section schema.
- Test module `backend/tests/invariants/test_wpw_tier2_technical_report.py`.
- Data-statement generator: reuses (a) `phase0/training_runner/runs/txttrain_20260831T193455Z_9594859a.json` shape (already WPW-Tier-2-shaped) as reference, (b) column-decision-ledger sha256 pattern from `tools/text_train_pipeline/mask.py` (per owner-facing datasheet discipline).

### W-WPW-v1-e · Tier 3 (White Paper) — **BLOCKED** by R1/R2/R3
Implements: WPW-11, WPW-12, WPW-13, WPW-14, WPW-15, plus A3, A5.

Not scoped in this wave. Blocked as follows:
- WPW-11 requires R1 (numeric exceptional threshold) — mechanical eligibility cannot fire without it.
- WPW-15 requires R2 (external-release signatory) — outer-gate publication crossing cannot ceremony without it.
- WPW-11's added novelty-claim clause requires R3 ratification (WPW-11 itself flags: *"It's carried in R3 for explicit ratification, not assumed settled."*).

After R1/R2/R3 land, Tier 3 becomes a ~1–2 day sub-wave.

### W-WPW-v1-f · Attribution & Authorship (DEFAULT-class · R3-adjacent) — ~2 hours
Implements: WPW-16 (role-only attribution unless written consent, DEFAULT-class), WPW-17 (wizard credited as instrument, not on author line, DEFAULT-class).

Both are `[DEFAULT]` — buildable now with the DEFAULT values, revisable on R3 ratification. Land as invariants that either (a) match current DEFAULT values OR (b) refer to a ratified override.

### W-WPW-v1-g · Tests-first end-to-end integration — ~2 hours
- Full pipeline invariant (RED then GREEN): a training run emits Tier-1 notebook entries, on-settle emits a Tier-2 report, evidence-class discipline enforced across, zero-influence held.
- Double-green ratchet close.
- Bank in DECISIONS.md.

**Total for W-WPW-v1 (Tiers 1 + 2 + auxiliaries):** ~2 days (matches SPRINT_PLAN.md estimate).

---

## 3 · Reuse assessment (against donor repos + Wave-H receipts)

**Repos scanned:** `RMS-IQ-Core-2`, `Akki-OS-V1`, `Extraction-Akki` (this workspace), `Akki-Executive-Core`. **Wave-H receipts scanned:** `phase0/whitepapers/wp_run_wave_h_first_governed_cuda_verify.json`, `phase0/training_runner/runs/*`.

### Reusable primitives (adopt as-is)

| Primitive | Location | WPW use |
|---|---|---|
| Doc 5 append-only Ledger writer pattern | Referenced across all repos (grep `Ledger` + `append_only`) | Tier 1 notebook MUST use this pattern (WPW-4 verbatim: *"append-only and hash-chained on the Doc 5 pattern"*). Reuse rather than reinvent. |
| `training_runner` state (this repo) | `backend/services/training_runner/*` | Tier 1 attach point at commissioning (WPW-1). Tonight's `txttrain_*` run record already carries the WPW-Tier-2 data-statement shape — direct reuse of the shape as reference. |
| Crossing-receipt discipline (this repo) | `backend/services/chokepoint/*` + `phase0/crossing_receipts/` | Tier 2 figure receipts (WPW-9) can piggyback on the crossing-receipt shape. |
| Response sanitizer + PII classification registry (this repo) | `backend/services/response_sanitizer/` | WPW-14 redaction gate — reuses classification registry directly for "confidential + personal markers" (A3). |
| Column-decision-ledger sha256 pattern (this repo · tonight's ingest) | `tools/text_train_pipeline/mask.py:_decision_ledger_hash()` | Tier 2 data statement (WPW-8 §2) — reuses this exact pattern for datasheet-level column classification with auditable sha256. |
| `evidence_class ∈ {measured, estimated, observed}` grammar | WPW spec §5 | New — but owner ruling 7 verbatim directs reusing this discipline for tonight's honest-memorisation framing. |

### Adjacent-but-not-directly-reusable

| Adjacent | Location | Why not direct reuse |
|---|---|---|
| `cif_spec_v1` (referenced in WPW dependencies) | Not in this workspace | WPW-6 requires mirroring CIF ideation events BY REFERENCE. If cif_spec_v1 artefacts don't exist yet in this codebase, WPW Tier 1 must degrade gracefully to "the record is silent" for CIF events (WPW spec §5 refusal grammar allows this). |
| `training_techniques_spec_v1` | Flagged in WPW spec §6 as "cited by name and status only — content hasn't been reviewed" | Same posture. |
| Promise #24 baseline registry | Referenced in WPW-8 §3 (baseline record) | Must confirm this registry exists in this codebase before WPW Tier 2 can cite it; else honest-empty. |

### Novel to WPW (must be built · no donor exists)

- **Novelty gate** (WPW-12): claim of new approach/knowledge MUST trace: ideation event → adoption into run → measured delta on held-out vs baseline/counterfactual. No donor pattern found.
- **Three-tier eligibility state machine** (WPW-11): mechanical, threshold-driven, no manual tagging. Novel.
- **Redaction gate at classification-driven depths** (WPW-14): methods/hyperparameters/metrics publishable · data at aggregate/datasheet level · personal data never · confidential statistically only. Partial donor: response_sanitizer covers "never PII"; the multi-depth classification layer is novel.
- **Zero-influence invariant** (WPW-2, A2): bit-identical training outcomes with wizard attached vs detached. Novel — no donor.

---

## 4 · R1 / R2 / R3 · framed for single-shot owner ruling

The WPW spec §7 lists three parked rulings blocking Tier 3. Framing them crisply so the owner can rule in one shot:

### R1 · The exceptional threshold
> **Spec verbatim:** *"The exceptional threshold: a numeric definition of an exceptional run (e.g., margin above baseline on held-out, or percentile against the run history). Value required before Tier 3 can fire."*

**What the owner is picking:** the numeric bar that mechanically qualifies a run as "exceptional" (Promise #25). Two shapes suggested by the spec:
- **(R1-a) Absolute margin:** e.g., "held-out score ≥ baseline + X% (or X σ)". Simple to define; needs owner-set X.
- **(R1-b) Percentile bar:** e.g., "run scores in the top P% of the historical run distribution". Adaptive; needs owner-set P and a minimum-run-history cutoff before firing (avoiding early-cohort noise).

**What agent recommends (non-binding):** R1-a with a conservative X (e.g., held-out ≥ baseline + 5% relative OR ≥ 2σ, whichever is more stringent). Rationale: absolute margins are auditable in isolation; percentile bars re-shift as history grows. Owner picks.

### R2 · External-release signatory
> **Spec verbatim:** *"External-release signatory: the named human authority whose sign-off an outer-gate publication crossing requires."*

**What the owner is picking:** the named human whose sign-off is required for an outer-gate Tier 3 publication crossing (WPW-15). This is a role assignment, not a code change — the signatory's identity is banked as a config artefact + a `SigningAuthorityV0` shape.

**Suggested content of the ruling (owner fills):**
- Named signatory: [owner name or delegate].
- Backup signatory (for continuity): [name] · authority conditions.
- Sign-off ceremony: banked signature-record shape (attach to the outer-gate egress crossing).

### R3 · DEFAULT ratification + three-tier structure + WPW-11 novelty clause
> **Spec verbatim:** *"Ratification of the two DEFAULT-class values (WPW-16, WPW-17), the three-tier structure, and WPW-11's added novelty-claim condition beyond Promise #25's literal text."*

**What the owner is picking (3 things bundled into R3):**
- **R3-a** · WPW-16 DEFAULT: *"Any artefact crossing the outer gate attributes contributions by role, unless the named person has given written consent to be named."* Ratify or override.
- **R3-b** · WPW-17 DEFAULT: *"Authors are humans. The wizard is credited as instrument — named in the reproducibility statement, never on the author line."* Ratify or override.
- **R3-c** · WPW-11 novelty clause: the spec adds *"AND at least one claim passing WPW-12"* on top of Promise #25's "exceptional results" alone. Spec author flags this addition explicitly (spec verbatim: *"The AND-novelty-claim clause is this spec's addition, made to serve the innovation objective directly, not a restatement of ratified canon. It's carried in R3 for explicit ratification, not assumed settled."*). Ratify the addition or run Tier-3 on "exceptional" alone.

**Agent's non-binding note on R3-c:** the addition serves the platform's innovation objective — a run can be exceptional-but-unoriginal (e.g., competent execution of a known recipe on new data). Without the novelty clause, such a run publishes as a white paper; with it, it stays Tier 2 (technical report). Owner picks.

---

## 5 · Sequencing note (owner-only)

Per SPRINT_PLAN.md, W-WPW-v1 sits after W-Shield-Train in the recommended order. The recommendation stands: W-Shield-Train unblocks the DigiCow training pipeline the owner asked for; W-WPW-v1 is unblocked by nothing and can start at any time thereafter.

If R1/R2/R3 rulings land during W-Shield-Train work, W-WPW-v1 sub-waves can partially proceed in parallel (Tier 1 + Tier 2 are unblocked; Tier 3 waits on rulings).

Ratchet discipline unchanged. No push. Local commits only.
