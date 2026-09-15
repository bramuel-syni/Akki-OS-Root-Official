READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-EXPORT-ARTEFACT-RENDER · Grounding Brief

**Wave name.** W-EXPORT-ARTEFACT-RENDER (M8 quick-hardening #2).

**Wave charter trigger.** W-DATA-SUITE-V2-LIFT close report §5 recommendation 3 (`notes/W_DATA_SUITE_V2_LIFT_close.md:93` verbatim):

> "Land `W-EXPORT-ARTEFACT-RENDER` as a small follow-on. CP-D6 landed the contract + gate; actual export payload rendering (CSV/PDF/…) is out-of-wave (§E.3 wave-honest limit). Small scope, high user-visible value."

Owner GO chain confirmation (this-turn, 2026-09-15T~15:35Z, verbatim): *"Use the ratified framing from the W-DATA-SUITE-V2-LIFT close report (its §5 rec): CP-D6 already landed the ExportArtefact 4-carrier contract + admit_export gate; this wave lands the actual export payload RENDERING (CSV and PDF at minimum) that was declared out-of-wave under §E.3. Scope additions that are already-ratified law, not new scope: every rendered export must route through the release gate under the pilot rules (receipt+debit per R-7 PILOT-OPEN, tokenization where named persons appear per R-15(a), derivative-only content per R-16(a), receipt-written-before-result per P036) and carry derivation_unit_refs per Canon-4 §22 UnitRefs-only. Small wave — keep it tight, no scope creep into new export types beyond what the Data-Suite surfaces already declare."*

---

## §A · Verbatim discharge anchors

### A.1 · DAP-Spec §A10 (via CP-D6 substrate)
Anchor already landed at CP-D6 (`services/data_suite_v2/export_artefact.py` + `export_gate.py`):

> "exports must carry rights posture + hash + derivation from controlled units + terms cited"

Verbatim carriers (frozen at CP-D6): `rights_posture · derivation_hash · derivation_unit_refs · terms_cited`. Any empty carrier → `ExportRefused` at `admit_export()`.

### A.2 · Canon-4 §22 Load-Bearing (UnitRefs-only)
Source file: `canon/text/Akki_Canon_4_Operating_Engines.txt` line 118 verbatim:

> "The function returns unit references only. It carries no class decision. A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."

Discharge in this wave: `derivation_unit_refs` (Sequence[str] of unit refs) is the load-bearing evidence carried into the rendered payload. The payload MUST carry those refs verbatim as provenance; the render function MUST NOT interpret or class-collapse them.

### A.3 · R-7 PILOT-OPEN receipt+debit (via CP-RG1/CP-RG4 substrate)
Anchor already landed at CP-RG1/CP-RG4. DECISIONS 2026-09-15T~03:55Z Effect 1 verbatim:

> "every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."

Discharge in this wave: every render call routes through `admit_transcript_release_pilot_open` → `record_debit` before payload bytes are returned to the caller. Missing `release_receipt_id` refuses via `ReceiptMissingRefused` (no payload). `DEFAULT_PENDING_OVERRIDE` budget-state refuses via `BudgetStateRefused` (no payload).

### A.4 · R-15(a) Named-persons tokenization (via CP-RG2/CP-RG4 substrate)
Anchor already landed at CP-RG2/CP-RG4. DECISIONS 2026-09-15T~03:55Z Effect 2 verbatim:

> "People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."

Discharge in this wave: when `named_persons` is non-empty, the payload is composed AFTER passing through `tokenize_named_persons`; raw names never appear in the rendered CSV or PDF bytes. The transcript-artefact's `named_persons_verdict` is set to `TOKENIZED`.

### A.5 · R-16(a) Derivative-only via Pull Seam (via CP-RG3/CP-RG4 substrate)
Anchor already landed at CP-RG3/CP-RG4. DECISIONS 2026-09-15T~03:55Z Effect 3 verbatim:

> "Set transfer_basis: DERIVATIVE_ONLY_VIA_PULL_SEAM for the transcript-text-only tier — the Pull Seam is the model-facing seam; source data does not cross; only derivatives (tokenized transcripts) cross"

Discharge in this wave: transcript-artefact `transfer_basis` is `DERIVATIVE_ONLY_VIA_PULL_SEAM` for the render path. Values outside the closed acceptable set refuse via `TranscriptVerdictUnknown`.

### A.6 · Pull Seam §2 P7 · P036 (receipt-before-result)
Source file: `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt` · P036 verbatim (already anchored in CP-RG1):

> "The receipt is written before the result is returned. If it cannot be written, the operation is refused."

Discharge in this wave: on-success ordering is (1) admit_export → (2) tokenize (if needed) → (3) build TranscriptArtefact → (4) admit_transcript_release_pilot_open (writes debit == receipt) → (5) render payload bytes → (6) return (bytes, debit). If any step (1)–(4) refuses, NO payload bytes are rendered and NO debit is written for the failing branch (except: when admit_export raises after step (4) hypothetically — the ordering above forbids that; admit_export is step (1)).

---

## §B · CP breakdown

Single-CP wave — small scope per owner directive "keep it tight, no scope creep into new export types beyond what the Data-Suite surfaces already declare".

| CP | Deliverable | File(s) |
|----|-------------|---------|
| CP-EXR1 | Export render + release-gate composition. `render_export_and_release(*, export_kind, rows, rights_posture, derivation_hash, derivation_unit_refs, terms_cited, named_persons, transcript_id, kdpa_verdict, licence_class, release_receipt_id, release_budget_state, usage_quantity, usage_unit, debited_by_party) -> Tuple[bytes, ReleaseLedgerDebit]`. Supports `export_kind ∈ {"csv", "pdf"}` (closed set — anything else refuses via `ExportKindUnknown`). CSV rendered via `csv.writer` (stdlib) with a 3-line preamble carrying `rights_posture · derivation_hash · derivation_unit_refs · terms_cited`. PDF rendered as a minimal PDF-1.4 byte-stream (single-page ASCII text carrying the same preamble + rows) — no external deps. Named persons are tokenized via `tokenize_named_persons` BEFORE render if `named_persons` non-empty. `transfer_basis` is fixed to `DERIVATIVE_ONLY_VIA_PULL_SEAM`; `named_persons_verdict` is `TOKENIZED` when tokenization ran else `DPO-APPROVED`; both are closed-set discipline per CP-RG3. Receipt/debit ordering per P036: `admit_transcript_release_pilot_open` fires BEFORE payload bytes are rendered; return payload bytes AND the returned `ReleaseLedgerDebit`. | `services/data_suite_v2/export_render.py` + `tests/invariants/test_wexr_cp_exr1_render_export_and_release.py` |

**Estimated ratchet delta:** +8 invariants (target: **4074 → 4082**).

---

## §C · Invariants gated (right-reason ImportError REDs before mechanism)

1. **Module fabric.** `services.data_suite_v2.export_render` module exists and exports `render_export_and_release · ExportKindUnknown`.
2. **Closed-set discipline on `export_kind`.** `export_kind` outside `{"csv", "pdf"}` refuses via `ExportKindUnknown`; nothing is rendered; nothing is debited.
3. **`admit_export` refusal propagates.** Empty `derivation_unit_refs` (or any of the 4 required carriers) propagates `ExportRefused`; no debit is written to the ledger; no payload is returned.
4. **P036 receipt-before-result.** Empty `release_receipt_id` propagates `ReceiptMissingRefused`; no payload bytes; no debit.
5. **R-7 DEFAULT_PENDING_OVERRIDE refuses.** `release_budget_state = DEFAULT_PENDING_OVERRIDE` propagates `BudgetStateRefused`; no payload bytes.
6. **Canon-4 §22 UnitRefs-only preamble.** Rendered CSV bytes contain `derivation_unit_refs` verbatim in the preamble; rendered PDF bytes carry the same refs verbatim. No class-decision is emitted alongside the refs.
7. **R-15(a) tokenization in payload.** When `named_persons=("Alice", "Bob")`, rendered CSV and PDF contain `<TOKEN_NP_00>` and `<TOKEN_NP_01>` (or 3-digit width at ≥100); RAW names `"Alice"` and `"Bob"` are absent from the payload bytes; the returned debit's receipt_id is the release_receipt_id (not the tokenization receipt_id — tokenization is upstream of release).
8. **Deterministic CSV render.** Two byte-identical calls (same inputs, same at_utc pinned) produce byte-identical CSV payload bytes.

---

## §D · Wave-honest limits (declared at open)

1. **E.1** Export kinds THIS WAVE: `csv` and `pdf` only. Owner ruling verbatim: "no scope creep into new export types beyond what the Data-Suite surfaces already declare". Additional kinds (xlsx, json, html, etc.) are follow-on waves.
2. **E.2** PDF renderer is minimal (PDF-1.4 single-page ASCII text stream, no external deps). Fancy typography, embedded fonts, and multi-page layout are out-of-wave. The PDF must be a valid PDF-1.4 file (starts `%PDF-1.4`, ends `%%EOF`, has one page object) — no more, no less.
3. **E.3** `usage_quantity` unit is `rendered_bytes` (integer count of rendered payload bytes). Owner may reframe the unit at any milestone-boundary; the render function accepts unit as a caller-provided string.
4. **E.4** No LLM transit. No external network calls. No filesystem writes. Payload is returned as bytes.
5. **E.5** Named-persons detection is caller-provided (`named_persons` sequence). This wave does NOT auto-detect names in `rows` — that is CIF-owned. The wave's tokenization discipline is: if the caller declares names, tokenize them; if they don't, no tokenization happens and the payload is admitted as `named_persons_verdict = DPO-APPROVED` (existing CP-RG3 admission).
6. **E.6** Deterministic-tests use a pinned `at_utc` via test seam OR call inputs (usage_quantity is deterministic bytecount → debit_id becomes deterministic modulo the at_utc timestamp). Test invariant #8 pins via twice-back-to-back invocation within a tight time window and compares CSV payload bytes (timestamps flow through `at_utc` into `debit_id` but NOT into the CSV payload — CSV is timestamp-free).

---

## §E · Commit protocol

- **CP-EXR1 (single-CP wave):** Commit A on `programme/track-a` (code + tests + `baseline_failures.json` bump) · Commit B on `master` (state: DECISIONS entry + NEXT refresh + drill receipts).
- **Wave close:** composite seal at `phase0/output_verified_seals/w_export_artefact_render.seal.txt` (`Kind: w_export_artefact_render`).
- **Rider bank:** collect-only + pip freeze receipts at `phase0/wave_riders/w_export_artefact_render/`.
- **NEVER push.**

---

## §F · Decision points / stop conditions

Wave HALTS with a decision-point note if:
- Baseline ratchet regression at CP-EXR1 double-green.
- Any file entering the ratchet path leaks credential-shaped content (custody-cat guard fires).
- Prototype substitution rules break (rare — this wave adds no frontend surfaces).

Otherwise wave proceeds per owner directive.

---

## §G · Boundary-hygiene probe cadence

Per DECISIONS 2026-09-15T~09:50Z Effect 4 verbatim: *"Keep the CD/Visitors re-probe loop running at boundaries while egress is open."* Probe #11 fired at wave open (both FAIL errno-110-ETIMEDOUT, unchanged from probes #1-10). Probe fires again at CP-EXR1 close.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
