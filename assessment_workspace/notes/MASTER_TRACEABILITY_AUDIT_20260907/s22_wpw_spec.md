# S22 · Whitepaper Wizard Spec v1 · Detail Classification

**Source:** `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx` (sha256 `7b51c5adf275ab176a18fa6a9277c593139ec6a132b7b5c923227153e4be5fed`, 15,858 bytes) · extracted at `canon/fixtures/whitepaper_wizard_spec_v1/spec.extracted.txt` (10,687 bytes, 90 lines) · charter at `STATE/WPW_CHARTER.md`.

**Row inventory: 18** = WPW-1..WPW-18 (Tier 1 events + Tier 2 report + Tier 3 white paper + attribution + economics). Plus 3 parked rulings R1/R2/R3 (blocking Tier 3 only).

Ceremonial status: **All 18 rows are PROPOSED as authored** (spec draft; owner-ratification-pending). §7 verbatim: *"Nothing in this spec is blocked by the parked rulings except Tier 3's final firing condition (R1) and the release ceremony (R2). Tiers 1 and 2 are fully specified and buildable as written."*

## §A · Tier 1 · Notebook (WPW-1..WPW-7, WPW-18)

| Row ID | Requirement (compressed verbatim) | Classification | Code path / donor / gap |
|---|---|---|---|
| WPW-1 | Wizard attaches at commissioning of every training run · read-only · event-driven (no per-run opt-in) | PARTIAL | `phase0/wpw_notebook/` exists across 6 runs (run_1, run_gov-1, trn_chokepoint_*, trn_wp_close_resolution_test) · attach mechanism not yet formalised as `backend/services/wpw/tier1_notebook.py` |
| WPW-2 | Zero-influence invariant (A2): bit-identical training outcomes with wizard attached vs detached | NEW | Zero-influence build-time check NEW · noted in WPW_CHARTER §3 as novel |
| WPW-3 | Event-driven capture: min event set (commissioning reflection · baseline record Promise #24 · checkpoints · acceptance-criterion transitions · CIF ideation · human contribution · anomalies · cost checkpoints against estimate) | PARTIAL | Event notebook JSONL emission proven (phase0/wpw_notebook/*/notebook.jsonl); full 8-event minimum set not verified end-to-end |
| WPW-4 | Append-only, hash-chained on Doc 5 Ledger pattern · each entry carries {timestamp, run_artefact_ref, evidence_class ∈ measured/estimated/observed} | PARTIAL | Notebook append proven; hash-chain check + evidence_class field enforcement NEW |
| WPW-5 | Human contribution events: {actor · state_before · change · movement_after} · correlation-only, causal reading refused | NEW | Human-contribution schema NEW |
| WPW-6 | CIF ideation events mirrored by reference to `cif_spec_v1` artefacts · no paraphrase | PARTIAL | CIF ideation events land in run_gov-1; cif_spec_v1 not on disk (adjacent-not-reusable in WPW_CHARTER §3); degraded gracefully to "record silent" |
| WPW-7 | Retention on refused runs · notebook survives refusal (test A6) | DONE | Refused runs preserved in `phase0/wpw_notebook/trn_chokepoint_*/notebook.jsonl` |
| WPW-18 | Economics · observation cost as budget line on run estimate · surfaced as anomaly if exceeded | NEW | Cost-Ledger integration required (CA1-008 already partly built at W6 CP2); WPW-side hook NEW |

## §B · Tier 2 · Technical Report (WPW-8, WPW-9, WPW-10)

| Row ID | Requirement (compressed verbatim) | Classification | Code path / donor / gap |
|---|---|---|---|
| WPW-8 | Draft-on-settle · auto-emit Tier-2 report when run settles (accepted OR refused) · fixed 9-section skeleton (problem·data·baseline·method·setup·results·ablations·limitations·negatives) | REUSE | Existing `phase0/training_runner/runs/txttrain_20260831T193455Z_9594859a.json` already carries WPW-Tier-2-shaped data statement; formatter NEW |
| WPW-9 | Figure traceability · every figure carries evidence_class + receipt line resolving to run artefact · unresolvable figure MUST NOT render (test A4: 100% resolve) | NEW | Figure-receipt resolver NEW; crossing-receipt shape from `backend/services/chokepoint/` reusable |
| WPW-10 | Internal only · reports never cross outer gate | DONE (by design) | No outer-gate crossing for Tier-2 in code · verified structurally |

## §C · Tier 3 · White Paper (WPW-11..WPW-15) · **BLOCKED on R1/R2/R3**

| Row ID | Requirement (compressed verbatim) | Classification | Code / donor / gap |
|---|---|---|---|
| WPW-11 | Mechanical eligibility (exceptional threshold + novelty gate) · threshold-driven state machine | NEW · BLOCKED on R1 | State machine NEW · R1 numeric threshold parked |
| WPW-12 | Novelty gate · claim of new approach/knowledge MUST trace: ideation → adoption → measured delta on held-out vs baseline/counterfactual | NEW | No donor pattern; novel to WPW |
| WPW-13 | Assembly draws only from Tier 1/2/run record · no post-hoc narrative reconstruction | NEW | Assembly gate NEW |
| WPW-14 | Redaction is classification-driven gate (methods/hyperparameters/metrics publishable · data at aggregate/datasheet · personal never · confidential statistically only) | REUSE | `backend/services/response_sanitizer/` covers "never PII" (partial); multi-depth classification layer NEW |
| WPW-15 | External release = separate outer-gate egress crossing · signatory-gated | NEW · BLOCKED on R2 | Outer-gate publication crossing NEW · R2 signatory parked |

## §D · Attribution + DEFAULT-class (WPW-16, WPW-17)

| Row ID | Requirement (compressed) | Classification | Code / donor / gap |
|---|---|---|---|
| WPW-16 | [DEFAULT] Any artefact crossing outer gate attributes contributions by role, unless named person gave written consent | NEW · DEFAULT-PENDING-OVERRIDE (R3-a) | Attribution ledger NEW |
| WPW-17 | [DEFAULT] Authors are humans; wizard credited as instrument (reproducibility statement, never author line) | NEW · DEFAULT-PENDING-OVERRIDE (R3-b) | Author-line policy NEW |

## §E · Parked Rulings R1 / R2 / R3

Not counted as rows (blocking-only). Framing verbatim per WPW_CHARTER.md §4:

- **R1** · The exceptional threshold. Options: (R1-a) absolute margin `held-out ≥ baseline + X% or Xσ` — agent recommends X=5% relative or 2σ whichever stringent (DEFAULT-PENDING-OVERRIDE); (R1-b) percentile bar with min-run-history cutoff.
- **R2** · External-release signatory. Owner names signatory + backup + ceremony.
- **R3-a** · WPW-16 attribution DEFAULT ratification/override.
- **R3-b** · WPW-17 authorship DEFAULT ratification/override.
- **R3-c** · WPW-11 novelty clause addition ("AND at least one claim passing WPW-12") ratification. Agent's non-binding note: novelty clause discriminates exceptional-but-unoriginal runs from novel exceptional runs.

## §F · S22 rollup

| Bucket | Rows | % of 18 |
|---|--:|---:|
| DONE | 0 (technically WPW-7 + WPW-10 exist by design; conservatively counted) | 0.0% |
| PARTIAL | 5 (WPW-1, WPW-3, WPW-4, WPW-6, and by broader default WPW-7 could count) | 27.8% |
| REUSE | 2 (WPW-8, WPW-14) | 11.1% |
| NEW | 11 (WPW-2, WPW-5, WPW-9, WPW-11, WPW-12, WPW-13, WPW-15, WPW-16, WPW-17, WPW-18, WPW-10 by strict test) | 61.1% |

**Interpretation:** Tier 1 + Tier 2 are ~½ day each per WPW_CHARTER estimate (unblocked). Tier 3 (5 rows) is blocked on 3 rulings; ratchet is minimal (~1-2 days once ruled). Attribution DEFAULT-class rows (WPW-16, WPW-17) can land as DEFAULT immediately, re-ratchet on R3 override.

**Wave charters:**
- **W-WPW-TIER-1-2** (unblocked · M effort · ~2 days): WPW-1..10 + WPW-18 + WPW-16/17 DEFAULT
- **W-WPW-TIER-3-DEFERRED** (S effort once rulings land): WPW-11..15

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
