READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# wave_release_gate_pilot_lift_grounding_brief.md

**Wave name:** `W-RELEASE-GATE-PILOT-LIFT`
**Chartered:** 2026-09-15T~03:55Z (owner-ratified)
**Owner authorization (verbatim, DECISIONS.md 2026-09-15T~03:55Z):** *"Charter this as a proper wave (e.g. W-RELEASE-GATE-PILOT-LIFT): tests-first, RED for each verdict transition, double-green, seals, two commits."*
**Sequencing pin (owner verbatim):** *"census at 08:00 UTC (unchanged, first priority) → W-RELEASE-GATE-PILOT-LIFT → D12 POC"*.
**Wave scope class:** M-class (verdict wiring + tokenization capability + release-ledger debit) — 5..7 CPs · target ratchet delta ≈ +30..+40.

---

## §A · Authorization anchors (verbatim quotes with source-file + section anchors)

**A1 · R-7 · PILOT-OPEN (DECISIONS.md 2026-09-15T~03:55Z · Effect 1):**

> *"budget state = PILOT-OPEN (owner-ratified, supersedes DEFAULT-PENDING-OVERRIDE refusal), BUT every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."*

**A2 · R-15(a) · TOKENIZE (DECISIONS.md 2026-09-15T~03:55Z · Effect 2):**

> *"People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."*

**A3 · R-16(a) · DERIVATIVE-ONLY VIA PULL SEAM (DECISIONS.md 2026-09-15T~03:55Z · Effect 3):**

> *"transfer_basis resolves to derived-intelligence-only: derivatives (attributes, features, transcripts-as-derived-text with tokenized identities) may cross; raw estate data never does except via the outer gate."*

**A4 · Pull Seam §2 P7 P036 (canon anchor for receipt-invariant, unchanged):**

> *"Each operation writes a receipt: what was accessed, in what quantity, under which terms, by which party, at what time."* (`canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P036.s1`)
> *"The receipt is written before the result is returned. If it cannot be written, the operation is refused."* (canon Pull Seam §2 P7 · P036)

**A5 · Pull Seam §2 P1 P015.s6 (identity-never-crosses anchor):**

> *"There is no configuration in which estate data is transferred to compute outside the perimeter."* (`canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P015.s6`)

**A6 · Pull Seam §2 P1 P007 (reversed-direction-of-travel anchor):**

> *"Reverse the direction of travel. Instead of sending data to where the compute is, put the compute where the data is, and let only governed results travel out."* (`canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P007`)

**A7 · R-17(a) OPEN reaffirmation (DECISIONS.md 2026-09-15T~03:55Z · Effect 4):**

> *"R-17(a) hardening stays open (non-blocking). ... tighter-tier granularity awaits R-17(a) hardening in a follow-on wave."*

**A8 · Watch-Learning R-15(b)/R-16(b)/R-17(b) STAYS OPEN (DECISIONS.md 2026-09-15T~03:55Z · Effect 5):**

> *"The Watch-Learning R-15(b)/R-16(b)/R-17(b) set stays OPEN — do not conflate (the mnemonic collision you flagged)."*

---

## §B · CP walk (5 CPs · tests-first · target ratchet +30)

| CP | Focus | Canon anchor | Landing module(s) | Target invariants |
|---|---|---|---|---:|
| **CP-RG1** | `ReleaseBudgetState` enum + `ReleaseLedgerDebit` frozen carrier · pilot-open state · receipt+debit invariant | A1 · A4 | `contracts/release_budget.py` + `services/release_gate/release_ledger.py` | 6 |
| **CP-RG2** | `tokenize_named_persons` capability + `TokenizationReceipt` · per-transcript token-table · never-emitted-alongside-artefact invariant | A2 · A5 | `services/de_identify/tokenize_named_persons.py` + `contracts/tokenization_receipt.py` | 6 |
| **CP-RG3** | `TranscriptArtefact` extends admissible values: `named_persons_verdict = "TOKENIZED"` · `transfer_basis = "DERIVATIVE_ONLY_VIA_PULL_SEAM"` · new refusal invariants on `raw_audio` / `waveform_bytes` / `per_utterance_speaker_embedding` under DERIVATIVE_ONLY basis | A2 · A3 · A5 | Extend `contracts/transcript_artefact.py` + `services/audio_poc/release_gate.py` | 6 |
| **CP-RG4** | `admit_transcript_release` end-to-end wiring · flip refusal to admission when (R-7 PILOT_OPEN + R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY + R-17-licence `owner_full_rights` + receipt written) all hold · P036 receipt-before-result invariant | A1 · A2 · A3 · A4 | Extend `services/audio_poc/release_gate.py::admit_transcript_release` | 6 |
| **CP-RG5** | `release_ledger_debit_writer` end-to-end · integration test that a full transcript-release cycle writes a `ReleaseLedgerDebit` row, a `TokenizationReceipt`, and a `Receipt.v0`-shaped receipt · ledger-append invariant · aggregate-usage query API (for pilot-end budget-number derivation) | A1 · A4 | `services/release_gate/release_ledger.py::aggregate_usage_query` | 6 |

**Wave-total target:** +30 invariants (5 CPs × 6 baseline). Cross-benefit possible from `NON_CONTRACT_UTILITY_MODULES` extension for `release_budget.py` + `tokenization_receipt.py` (both `@dataclass(frozen=True)` under `contracts/`). Target ratchet **4018 → 4048..4050** (depending on cross-benefit).

## §C · Wave-honest limits (in-brief-declared, not-in-scope for this wave)

* **E.1 · R-17(a) hardening** — tighter licence-class taxonomy for non-`owner_full_rights` tiers. Owner-verbatim: *"stays open (non-blocking)."* Follow-on wave.
* **E.2 · R-15(b)/R-16(b)/R-17(b) (Watch-Learning Amendment)** — separate ruling set · this wave DOES NOT conflate. Follow-on: `W-WATCH-LEARNING-CERTIFICATE-LIBRARY-SEED` when owner rules R-15(b)/R-16(b)/R-17(b).
* **E.3 · Pull-Seam Receipt.v0 unified schema** — this wave uses a local receipt shape for release-ledger debits; the unified `Receipt.v0` schema across every operation surface (D9 drift) is the separate `W-PULL-SEAM-RECEIPT-UNIFY` charter.
* **E.4 · Actual pilot-end budget-number ratification** — happens outside the wave: owner runs the aggregate-usage-query at pilot end and rules the real budget number.
* **E.5 · Non-transcript deliverable classes** (audio-attribute bundles from D12+, feature summaries, etc.) — same tokenization + derivative-only-basis discipline applies conceptually; encoding for those classes is a follow-on when the class shapes exist.
* **E.6 · Outer-gate ceremony** for raw-bytes crossings — governed by DAP outer-gate (not this release-gate). Untouched.
* **E.7 · Cross-border transfer chokepoint** (KDPA §48/§51 · Governance Plane primitive #10 per roadmap `:437`) — untouched this wave; the `DERIVATIVE_ONLY_VIA_PULL_SEAM` transfer-basis is orthogonal.

## §D · Ordering rationale (why this CP order)

1. **CP-RG1 first** — the budget-state enum + release-ledger writer are the deepest prerequisites; every subsequent CP depends on the receipt-writer being callable.
2. **CP-RG2 second** — tokenization is a leaf capability with no upstream deps; landing it before the verdict-extension keeps the shape independent.
3. **CP-RG3 third** — extends TranscriptArtefact once RG1's receipt shape and RG2's tokenization shape are both frozen.
4. **CP-RG4 fourth** — wires the end-to-end admission logic; requires all three predecessors.
5. **CP-RG5 last** — the aggregate-usage query API is the last piece; it depends on the receipt writer having accumulated real receipts (test fixtures).

## §E · Guardrails (standing law honoured across this wave)

* No push (`programme/track-a` two-commit pattern · master state commit).
* No testing_agent (terminal `pytest tests/invariants/` exclusively).
* No refactor · thin-kernel per CP.
* Position-redaction: transcript-text in tests uses fixture text with no real PII; token-table receipts NEVER emit alongside the tokenized artefact.
* Verbatim-canon: every module docstring + test docstring carries §A anchors verbatim on single un-wrapped lines (whitespace-fidelity rule per CP-C3 corrective).
* SO §1 boot ritual at each session-start (STANDING_ORDERS · DECISIONS tail · NEXT top · baseline green run).

## §F · Deferred-until-ratchet-recovery notes

* Pytest wallclock is currently ~2 min at 4018 tests. Adding +30 tests keeps wallclock <2.5 min · unchanged discipline.
* No dependency additions expected · pip-freeze should stay at 192 lines.

## §G · Post-wave receipts pinned by charter

* Wave seal at `phase0/output_verified_seals/release_gate_pilot_lift.seal.txt` (`Kind: release_gate_pilot_lift`).
* Owner-facing 5-section wave-close report at `notes/W_RELEASE_GATE_PILOT_LIFT_close.md`.
* Rider 1 at `phase0/wave_riders/w_release_gate_pilot_lift/rider1_*.log`.

## §H · Sequencing pin (owner verbatim)

> "Sequencing: census at 08:00 UTC (unchanged, first priority) → W-RELEASE-GATE-PILOT-LIFT → D12 POC → BC packet authoring can happen in closed-window time as it's non-egress."

* **Predecessor:** Item-3 · live census run at 08:00 UTC re-open (armed at W-CENSUS-CANON-ALIGN seal 2026-09-15T~03:22Z).
* **Successor:** D12 POC on GPU hosts (bounded single-digit-count NAS files · POC-NOT-PRODUCTION provenance labels · receipts banked at `phase0/d12_poc_receipts/`).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
