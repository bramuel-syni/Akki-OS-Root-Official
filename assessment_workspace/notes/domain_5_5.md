# Domain 5.5 — Integration

Scope (instruction §5.5): answering service · warm/fresh fork · closed refusal
taxonomy · async contract · thin webhook · idempotency · memory layer + plane
isolation · Function & Promise Registry · Critic Seam (critic_pass lives ONLY
in Akki-OS-V1 — cite it there).

Spine cited: **Extraction-Akki** (≡ RMS-IQ-Core-2).

## Rows classified in this domain

### Six services (Canon 1 §12)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C1-069 (S1)** | Governed intelligence surface to integrating application | REUSE | shield chokepoint + trust receipts + refusal-family classifier |
| **C1-069 (S2)** | To operating organisation: estate onboarded, mapped, and turned into qualified intelligence | REUSE | mtafiti + targeta + outer_gate + use_data |
| **C1-069 (S3)** | To compliance officer: proof of any operation on demand | PARTIAL | trust receipts exist; end-to-end "prove one run" export surface is BUILD (5.7) |
| **C1-069 (S4)** | To data buyer: intelligence products independently verifiable | REUSE (partial) | `services/use_data/*.py` + `use_data/commission_verdict_engine.py` |
| **C1-069 (S5)** | To infrastructure consumer — RESERVED, not built | **N/A-DOCTRINE (Reserved)** | Canon 1 §12 explicit |
| **C1-069 (S6)** | To operating org + compliance officer under threat — continuous machine-speed detection/response | **BUILD** | ties directly to 5.8 Watch |
| **C1-070** | Every function traces upward to one of the six service sentences | REUSE (registry) | Function & Promise Registry — `docs/machine_readable_registry.md` + close-report; test `test_machine_readable_registry_mrr_g1_to_g6.py` |
| **C1-071** | An application is anything with an end-user in it (internal or external) | REUSE-doctrine | boundary discipline in scoped-key issuance below |
| **C1-072** | Every application through the same boundary; scoped key same way; no privileged path | REUSE | `services/auth/engineer_key_grant.py`, `engineer_key_grant_service.py`, `engineer_key_grant_ledger.py`; test `test_engineer_key_grant_load_bearing_wire_shape.py`, `test_engineer_key_grant_e2_taxonomy.py`, `test_engineer_key_grant_ledger.py`, `test_memory_engineer_key_grant_e2e_propagation.py` |

### Custody boundary contract (Canon 7 Part II)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C7-003** | Scoped key per application; scope names objective, memory-plane, model classes, refusal shapes | REUSE | engineer_key_grant service above |
| **C7-004** | Keys issued through same flow for every caller | REUSE | same service; test `test_engineer_key_grant_e2_taxonomy.py` |
| **C7-005** | Boundary crossing: authenticated + admitted + receipted + inspected | REUSE | northena admit + trust receipt + shield chain |
| **C7-006** | Answer envelope: answer, class chips, grounding, receipt id, refusal id, memory-plane status | PARTIAL | envelope exists in five_rings + normalized_unit + refusal envelope; three-lens (Canon 5 §37) surface is 5.7 BUILD |
| **C7-007** | Envelope stable across versions; additions strictly additive | REUSE | `contracts/objective_request_v2.py` frozen contract + parity #32 snapshot machinery |
| **C7-008** | Three refusal shapes distinguishable | REUSE | `services/compliance/refusal_family_classifier.py` (Chunk-2 Claim 5); test `test_service_1_refusal_v1_envelope.py`, `test_admission_refusal_v0_contract_frozen.py`, `test_admission_refusal_dispatch.py` |
| **C7-009** | Webhook: per-application receives compliance-record notifications | **BUILD** | no webhook infrastructure in spine; would need application-notification service |
| **C7-010** | No warm-up — first call governed identically to thousandth | REUSE | scoped-key issuance is atomic; no warm-up branch exists (verified by absence) |
| **C7-011 · C7-012** | Reference App registered as an application; no privileged path; key rotation same cadence | REUSE (structural) | no first-party bypass exists; reference-app surface is 5.7 |

### Memory plane (Canon 7 §19-23)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C7-013** | Per-application memory plane; plane-keyed store | REUSE | `services/memory/{ledger,plane_registry,scoped_accessor,working_set,write_back,publication,refusal,revocation}.py` (12 files); test `test_memory_service_m_g1_to_m_g9.py`, `test_memory_observability_o_g1_to_o_g6.py`, `test_memory_http_surface.py` |
| **C7-014** | Plane is not part of estate; contents don't leak across applications | REUSE | `test_instance_isolation.py`; plane_registry per-application scoping |
| **C7-015** | Retrieval scope configured per application | REUSE | scoped_accessor + plane_registry |
| **C7-016** | Write-back on/off per application; per-cycle + total storage ceilings; reaching either stops writeback and surfaces | REUSE | write_back.py; ledger + observability tests above |
| **C7-017** | Retention setting binds; expiry deletes with certificate | REUSE | `services/retention/authorized_deletion.py` (whitelisted authorized-deletion path); test `test_northena_ledger_retention.py` |
| **C7-018 · C7-019** | Precompute parameters under ceremony; Watch reads plane activity (not content) | PARTIAL | precompute infra minimal; Watch reads are BUILD (5.8) |

### Buyer/Customer path (Canon 7 §24-27)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C7-020 · C7-021 · C7-022 · C7-023** | Buyer through same boundary + scoped-key licence + consumption record + no path variation | REUSE (backend) | `services/use_data/{commission_verdict_engine,http_iter11}.py`; tests `test_use_data_http_iter11.py`, `test_use_data_iter12_addendum.py`, `test_use_data_iter14_sample_all_identities.py`, `test_use_data_commission_verdict.py`, `test_qualified_data_outer_gate_ride.py` |

### Function & Promise Registry (Canon 1 §8)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C1-053** | One canonical, versioned artifact registers every named function with its promise | REUSE | `docs/machine_readable_registry.md` (300+ close-report + auxiliary docs); test `test_machine_readable_registry_mrr_g1_to_g6.py` covers six mrr-g gates |
| **C1-054** | No gate without an honestly statable promise; no promise without a function protecting it — else retired | REUSE (discipline) | mrr-g6 asserts this — verified |
| **Akki-OS-V1 tooling: far_endpoint gate generator** | Auto-generates `generated_gates/*.py` stubs from mandate docs | HARVEST from Akki-OS-V1 | `Akki-OS-V1/backend/services/far_endpoint/*.py` + `services/generated_gates/*.py` + test `test_generated_gates_regeneration_diff.py`; also `test_registry_context_block_golden_snapshot.py` |
| **Akki-OS-V1: registry_context** | Prompt-context injection subsystem; readable registry | HARVEST from Akki-OS-V1 | `Akki-OS-V1/backend/services/registry_context/{reader,injector,prompt_builder}.py` + test above |

### Critic Seam (Canon 7 §31-34)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C7-024 · C7-025 · C7-026 · C7-027 · C7-028** | Standing quality layer + versioned rubric + amendments + calibration + independence | **HARVEST from Akki-OS-V1** | `Akki-OS-V1/backend/services/critic_pass/*` — the ONLY implementation across the four repos. Details in 5.4. Duplicated here as 5.5 mirror because Canon 7 §31-34 anchors it to Integration/Quality. |

### Answering service — Executive-Core two-pass discipline

Chunk-2 carry-forward (d) RESOLVED for `two_pass.py`:

`Akki-Executive-Core backend/services/two_pass.py` (1061 LOC) implements a **two-pass method** at chat surface with verbatim canonical prompts from `docs/MEMO.md` Item 8:
- `CANONICAL_TWO_PASS_PROMPT`, `CHAT_ADAPTED_FOUR_CHECK_PROMPT` (verbatim)
- `REFUSAL_TEMPLATES` — three verbatim patterns: `thin_input`, `unsourced_claim`, `named_assumption`
- `BANNED_WORDS` — union of MEMO §8 + WEBSITE_BRIEF §1.3
- `TURN_CLASSES`, `classify_turn(...)`, `parse_four_check_label(...)`, `detect_refusal_reason(...)`, `find_banned_word(...)`, `split_two_pass(...)`, `build_system_prompt(...)`

**Class: HARVEST (Solva-pattern amendment).** The three refusal patterns (`thin_input, unsourced_claim, named_assumption`) map cleanly onto Canon 3 §17's three refusal shapes (coverage, evidence-class, contradiction). Worth surfacing into the spine's `services/compliance/refusal_family_classifier.py` as new named families.

### Executive-Core `platform_kb.py`

Chunk-2 carry-forward (d) resolved for `platform_kb.py` (107 LOC):

Hand-curated static "what is AKKI" reference block injected into chat system prompts by `two_pass.build_system_prompt`. Explicit design decision to be static, NOT RAG. Application territory (Canon 1 §13). Not a canon capability.

**Class: RETIRE from platform** / keep as application-side.

## Domain 5.5 subtotals

- REUSE: 20 rows
- HARVEST from Akki-OS-V1: 2 clusters (critic_pass, far_endpoint+registry_context+generated_gates)
- HARVEST from Executive-Core: 1 (two_pass discipline as Solva-pattern amendment)
- BUILD: 3 (S6 Watch service sentence; webhook infrastructure; three-lens envelope surface backend uplift)
- RETIRE: 1 (platform_kb.py)
- PARTIAL: 4
- N/A-DOCTRINE / Reserved: 1 (S5 infrastructure consumer)
