# Domain 5.1 — Custody and Boundary

Scope (instruction §5.1): chokepoint · de-id→invoke→re-id · per-request envelope ·
trust receipts · egress firewall · static+runtime no-second-path proofs · outer
gate's five checks · cumulative disclosure · perception routing.

Spine cited: **Extraction-Akki** (≡ RMS-IQ-Core-2 on every path listed below;
Extraction-Akki paths verified byte-identical via Chunk-2 SHA checks unless noted).

Classes: REUSE / MODIFY / RE-POINT / BUILD / RETIRE. `N/A-DOCTRINE` for
prose-only rows that have no implementable surface at all (they still land
here for accountability).

## Rows classified in this domain

| Row | Capability | Class | Evidence | Note |
|---|---|---|---|---|
| **C1-014** | Fail-closed custody: if a custody control cannot execute, the operation does not happen | **REUSE** | `Extraction-Akki backend/services/synisense/shield/llm_router.py:207-311` + tests `backend/tests/registry/test_shield_custody_chain.py:34-140` IF1-G1/G2/G3 (≡ RMS-IQ-Core-2) | fail-closed proven at deid/reidentify/router boundaries |
| **C1-015** | Custody fail-closed vs cost fail-transparent asymmetry | **REUSE** | same as C1-014 for fail-closed side; cost meters live at `llm_router.py:263-291` | asymmetry present |
| **C1-016** | Unrepresentable-not-policed general doctrine | **N/A-DOCTRINE** | Canon 1 §4.2 | doctrine — surfaces in specific rows below |
| **C1-017** | Assertion boundary has no parameter for confidence | **REUSE** | `backend/services/solva_depth/assertion.py` — test `backend/tests/invariants/test_solva_assertion_boundary.py:test_utterance_never_asserted_as_fact` (parameterless verified) | 5.3 mirror row; classified here because "unrepresentable" is the doctrine seat |
| **C1-018** | Biometric register has no field for individual-ID biometrics | **N/A-DOCTRINE** | Canon 1 §4.2 | no biometric register exists anywhere in the four repos; unrepresentable by absence |
| **C1-019** | Watch behavioural params ≠ biometric register (separated objects) | **N/A-DOCTRINE** | Canon 1 §4.2 | neither object exists; will surface in 5.8 |
| **C1-029** | Inheritance — everything built inside Akki inherits custody | **REUSE** (partial coverage) | `backend/tests/invariants/test_ast_egress_gate.py:1-178` + `test_p1_custody_closure.py:98-161` (six P1-G-R2 gates including exemption list existence) | AST gate proves no other module can acquire outbound |
| **C1-039** | Exactly one outbound path leaves the perimeter | **REUSE** | runtime firewall `backend/services/synisense/shield/egress_firewall.py:1-138` + AST gate above | RMS-IQ-Core-2/Extraction-Akki only; **absent in Akki-OS-V1 and Executive-Core** |
| **C1-040** | Nothing else in the platform has outbound capability — allow-list + AST build gate | **REUSE** | same as C1-039 | " |
| **C1-041** | Compute does not leave the perimeter (external only where required, single crossing) | **PARTIAL** | topology assertion in Canon; no repo currently exposes an internal-model path (all model calls flow to litellm at `llm_router.py:266-269`) | flag: no in-perimeter model routing built |
| **C1-045** | SyniSense is the single chokepoint through which every outbound model call transits | **REUSE** | `llm_router.py:invoke_with_metering` (Claim 1 confirmation) + the AST + runtime gates enforcing uniqueness | Chunk-2 Claim 1 CONFIRMED spine; PARTIAL for Executive-Core (chain in `client.py`) |
| **C3-002** | Doctrines committed as machine-checkable rules | REUSE | Canon 3 §1 — implemented across the invariant suite listed in this table | doctrine seat |
| **C3-016** | SyniSense single outbound path (with allow-list + build gate) | REUSE | same as C1-039 | 5.1 anchor |
| **C3-017** | Per-invocation per-tenant custody chain | REUSE | `llm_router.py:invoke_with_metering(...tenant_id...)` + `trust_receipt.py:derive_tenant_key` HKDF | tenant-scoped end-to-end |
| **C3-018** | Input seat — content approaching boundary inspected under governance rules | **PARTIAL** | `shield/tenant_entities.py` referenced by deidentifier; **input-seat as a NAMED CANONICAL SURFACE does not exist** — no `shield/input_seat.py` in any repo | seam: the deidentifier is currently the input inspection; a separate input-seat surface per Canon 3 §12 is BUILD |
| **C3-019** | Custody sequence: input seat → egress redact → call → wrap → classify (indivisible) | REUSE | `llm_router.py:207-311` + tests IF1-G1/G2/G3 | 1→3 present; step 5 "response classified" happens at the caller layer, not in the router |
| **C3-020** | Input seat runs under governance identity at admit / Watch identity when sensing | **BUILD** | no Watch identity exists anywhere; Canon 3 §13.1 dual-identity model unimplemented | ties to 5.8 |
| **C3-021** | Trust receipt: caller_id, model_id, egress rule version, input/output hash, redaction summary, tenant signature | REUSE | `Extraction-Akki backend/services/synisense/shield/trust_receipt.py:99-146` (15 fields + signature) + `backend/contracts/trust_receipt_v1.py` frozen contract + snapshot #32 | Claim 3 CONFIRMED |
| **C3-046 · C3-047 · C3-048** | Prove-one-run end-to-end + regulator pack — receipts verifiable offline | **PARTIAL** | trust receipts sign; `services/master_admin/*` has export scaffolding (`backend/services/master_admin/*.py` — pending_seams, recent_actions, tier_lock_path_a_ledger). **The Canon-3 §33 "prove-one-run export" surface as a named single-action is BUILD.** | receipts exist; the assembly-from-record is not |
| **C1-030 · C4-057 · C4-058 · C4-059 · C4-060** | Contents / privacy / quality attestations on every deliverable | **PARTIAL** | `outer_gate/receipt.py` (48 L) mints deliverable receipts; contents attestation shape not fully implemented across all shelf deliverables | 5.4 mirror row anchored here |

## Outer-gate five checks

`backend/services/outer_gate/{mint,receipt,transform,__init__}.py` (four files, 285 LOC).

- `mint.py:_new_key` L42, `_fingerprint` L55, `MintWindowStore.open_window` L70, `.get` L82, `.purge_window` L93, `pseudonymise(window, plaintext)` L106 — one-shot per-window pseudonymisation key; window state has an explicit `purge_window` (a legitimate purge, allowed by the retention whitelist per `test_no_unauthorized_deletion_path.py`).
- `receipt.py:build_receipt` L17 — mints receipts.
- `transform.py:_generalise_feed_id` L49, `_generalise_structural_signature` L61, `transform_artifact` L68 — transformations.

The "outer gate's five checks" phrase in the instruction refers to Canon-anchored inspection points at the shelf boundary; concretely present in this repo:
- (1) pseudonymisation window is open, (2) fingerprint round-trip, (3) generalisation of feed-id, (4) generalisation of structural signature, (5) receipt mint.

Row-class: **REUSE for the pseudonymisation + generalisation + receipt-mint machinery**. Tests: `backend/tests/invariants/test_outer_gate_irreversibility.py`, `test_qualified_data_outer_gate_ride.py`, `test_v0_paths_byte_identical_after_4a.py` + `after_4b.py`.

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C4-022 · C4-023** | Frozen unit contract at end of Service-A + shelf ingest | **REUSE** | `outer_gate/{mint,receipt,transform}.py` + tests above |
| **C4-046** | Delivery receipted; licence label + privacy attestation travel with deliverable | **REUSE (partial)** | `outer_gate/receipt.py:build_receipt` + `use_data/commission_verdict_engine.py` — full "licence label" render is 5.7 |

## Perception routing

`backend/services/synisense/shield/perception_router.py` (present in RMS-IQ-Core-2 and Extraction-Akki, absent in Akki-OS-V1 and Akki-Executive-Core per Chunk-2 §Claim 6 file matrix). Test: `backend/tests/test_perception_router.py`.

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C4-004** | Mtafiti reads for Watch tripwire coverage, never writes | REUSE (readside) | present at code but Watch consumer absent; effectively half-wired |
| Perception routing (Canon 1 §1.1 modality activation) | REUSE | `perception_router.py` + `test_perception_router.py` | present in spine |

## Cumulative disclosure

`backend/contracts/cumulative_disclosure.py` + `backend/services/v2_gate/cumulative.py`.
Also `backend/services/system_state.py` and `backend/services/master_admin/pending_seams.py` feed the cumulative view.
Test: `backend/tests/invariants/test_v2_gate_refusal_cumulative.py`.

Row class: **REUSE**.

## Contradictions / Seams flagged for the client (do not resolve here)

- **PURPOSE-GATE CONTRADICTION** (from Chunk 2 Claim 6): the RMS-IQ-Core-2 / Extraction-Akki / Akki-OS-V1 line **shaved** `services/synisense/shield/purpose_validator.py` at IF-1 close (2026-07-14). Akki-Executive-Core (last commit 2026-07-08) **still enforces** `purpose_validator.validate_purpose()` at `backend/services/synisense/shield/client.py:63`, raising `PurposeInvalid` on empty / unknown / non-internal-prefix violations against an `ALLOWED_PURPOSES` catalogue. Purpose survives in the core-3 line as a trust-receipt field only (`trust_receipt.py:105,134`); the pre-deid gate is gone. Two live implementations disagree on whether the pre-deid purpose check is Canon-compliant. This is not classified — it is a governance decision surfaced.

## Domain 5.1 subtotals

- REUSE: 12 rows
- PARTIAL (treated as MODIFY for build-plan purposes): 4
- BUILD: 2 (C3-018 input-seat named surface, C3-020 dual-identity)
- N/A-DOCTRINE: 4
- CONTRADICTION rows carried: 1 (purpose gate)

The full mapping of every C1–C9 row to a domain lives across the ten domain files; this file lists only rows whose implementable surface is in Custody & Boundary.
