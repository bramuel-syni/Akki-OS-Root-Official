# M17 objective-card DRAFT · Milestone 8 · Tenant Apps + Personal Client (C.23)

**Banked as draft:** 2026-09-19T~12:45:00Z · post-CP-M16-W5-SEAL-INTEGRATION Commit-C fixup (`939124be` state · `462f6972` code · M16 milestone CLOSED at ratchet 5414 · milestone snapshot pin `cba422542da…` binding CIFProposal_v0) · pre-CP-M17-W1-APPLICATION-CONTRACT-SHAPE-FREEZE open.

**Draft authority:** SO §6.2 pre-authorised card drafting ("e1_dev drafts cards for M13–M17, memory layer, and frontends from canon and the SER, for batch ratification at the next seal boundary") + SO §6.7 batch-ratification-at-preceding-seal at CP-M16-W5-SEAL-INTEGRATION close (M16 milestone close · state master `939124be757beebc687a4661d0a82a1817ad1f16` · 2026-09-19T~12:32Z). **Scope tagged pending owner ratification** — landed at next digest boundary per owner steer 2026-09-19T~12:45Z.

**Owner steer verbatim (this-session, 2026-09-19T~12:45Z):**

> "5-10 MUST-DO lines stands. Anchor priority: span BOTH surfaces of M17 — (a) the tenant-facing/journey surface (Canon 6 journeys, Canon 5 interface) AND (b) the governance constraints that must hold in any client surface: approval blocks rather than warns, silence never approves, the chat proposes and never decides (the owner's B-frontends-Q1 ruling language / DAP UI Handoff Brief §5 — these bind the personal client too, not just the later web frontends). If the personal client's canon anchor requires any principal/user-memory data handling, remember R-21 is still owner-outstanding: tenant-wide flag off, no consent model assumed, no principal data written until ruled — put that in MUST-NOT with the ruling cite."

**Scope anchors (all files opened this session):**

- `notes/NEXT_MILESTONES_PLAN_20260917.md §11` verbatim: "MILESTONE M17 · Tenant Apps + Personal Client (C.23) · Application-contract enforcement + personal client for tenant-of-one · Depends on: M9 P5 · M11 · M12 · Risk: Low-medium."
- `notes/PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md line 144`: "Tenant Apps (C.23) · L1 (external repo) · RMS-IQ-Core-2 separate repo. No application-contract enforcement wire in Extraction-Akki."
- `STATE/AUTONOMOUS_RUN_PLAN.md line 67`: "M17 · Tenant Apps + Personal Client (C.23) · Reference application on the Integration-Console-issued-key model (Canon 7 §28)."
- `STATE/DECISIONS.md:12115` (B-frontends-Q1 owner ruling verbatim): "handoff: yes, gated on frozen contracts. Frontends open when the contracts they consume are frozen under T-b — at minimum the answering-service seam contract (C.17, currently partial) and DAP's entitlement and receipt contracts. Specialist agents inherit the same Standing Orders and R-18's order of authority, start from the DAP UI Handoff Brief, and build to its §5 constraints — **approval blocks rather than warns, silence never approves, the chat proposes and never decides.** Nothing on the governance path waits for them."
- `STATE/DECISIONS.md:13600 · 13630 · STATE/STANDING_ORDERS.md:445`: "Frontend fidelity bar — ruled. Functional parity with the established five-stage pattern and the DAP UI Handoff Brief §5 constraints. Prototype adoption where a screen exists; no literal pixel fidelity. The expensive path is not authorised." (fidelity bar extends to any client surface).
- `STATE/DECISIONS.md:12333 + 12366` (R-21 owner-outstanding verbatim): "R-21 (user-memory class, consent model): owner input outstanding — implement the class behind a tenant-wide flag, off by default, no consent model assumed, no principal data written until ruled."
- `STATE/DECISIONS.md:13655` (owner END OF BUILD authority 2026-09-19T~00:20Z): "M17 → memory layer (only after C.13 partial closes per the banked ruling) → frontends (functional parity bar per §6.4; gated on frozen C.17 + DAP entitlement + receipt contracts per the B-frontends-Q1 ruling)."

---

## PROMOTION-TO-STATE/OBJECTIVES/M17.md PROTOCOL

This draft becomes `STATE/OBJECTIVES/M17.md` at CP-M17-W1-APPLICATION-CONTRACT-SHAPE-FREEZE Commit-B (state master), when the W1 test file exists on disk so that `test_every_cited_exit_test_file_exists_on_disk` invariant passes. Between now and that moment this draft is banked in `notes/` for owner-review visibility without triggering the STATE/OBJECTIVES/ invariants.

At promotion time:
1. `card_sha256:` is computed over the promoted body with the pin line removed (per `test_every_card_hash_pin_matches_body` verbatim mechanism at `backend/tests/invariants/test_objective_card_pinned.py`).
2. `ratified_at_utc:` stamped to CP-M17-W1 Commit-A time.
3. `ratified_by:` cites CP-M16-W5-SEAL-INTEGRATION close as the batch-ratification boundary + this draft's `banked_at_utc` as the pre-open draft record.
4. `milestone_status:` starts as `DRAFTED · scope pending owner ratification per SO §6.2 · card drafted from canon + banked owner steer 2026-09-19T~12:45Z`.
5. At Commit-C fixup the card_sha256 is re-pinned if the body changed between Commit-A and Commit-B (per M14/M15/M16 fresh-landing precedent).

---

## FRONT-MATTER (to be prepended at promotion)

```yaml
---
card_id: M17
title: Milestone 8 · Tenant Apps + Personal Client (C.23)
ratified_at_utc: <CP-M17-W1-COMMIT-A-TIMESTAMP>
ratified_by: main-agent Autopilot draft under SO §6.2 pre-authorised card drafting authority + SO §6.7 batch-ratification-at-preceding-seal at CP-M16-W5-SEAL-INTEGRATION close (M16 milestone close · state master `939124be757beebc687a4661d0a82a1817ad1f16` · code `462f6972a2090d6e6faf0293a1958e84996549fc` · 2026-09-19T~12:32Z) · scope from `notes/NEXT_MILESTONES_PLAN_20260917.md §11` verbatim + `STATE/AUTONOMOUS_RUN_PLAN.md §11 Reference application on the Integration-Console-issued-key model (Canon 7 §28)` + owner steer 2026-09-19T~12:45Z (span both surfaces: tenant-facing/journey surface Canon 6/Canon 5 AND governance-in-client three invariants per B-frontends-Q1 DECISIONS.md:12115 verbatim / DAP UI Handoff Brief §5) · **scope pending owner ratification at next digest boundary per SO §6.2**
card_sha256: <computed-at-promotion-body-hash-with-pin-line-stripped>
milestone_status: DRAFTED · scope pending owner ratification per SO §6.2 · card drafted from canon + banked owner steer 2026-09-19T~12:45Z · promoted to STATE/OBJECTIVES/M17.md at CP-M17-W1-APPLICATION-CONTRACT-SHAPE-FREEZE Commit-B
sub_wave_order: application_contract_shape_freeze → integration_console_issued_key_model → personal_client_session_surface → governance_in_client_three_invariants → integration_seal_and_milestone_snapshot_pin
depends_on: M14 (answering service seam + Mkondo registry + per-tenant Ed25519 sealed · consumed at W3 by identity import for session ask routing) · M11 (per-tenant DB provisioning sealed · consumed at W3 for `t_<tenant_id>` ask persistence discipline) · services/capability_registry.py (sealed W1b·CP4 · L-5 A20.16 downstream register · consumed at W1 as capability_manifest anchor) · services/watch/signature_primitive.py (sealed M12b-W1 · consumed at W2 by identity import for keygen-only at trust boundary · pure-data-in per M14-W4 precedent) · services/doc0_attributes/tcb.py (sealed W-M2-SW7 · consumed structurally by W2/W3/W4 AST-scan invariants where TCB membership is asserted)
---
```

---

# M17 · Tenant Apps + Personal Client (C.23)

## OBJECTIVE

Close **C.23** at the L3-shape-freeze level in the Extraction-Akki backend: implement application-contract enforcement + a personal client for tenant-of-one built as a reference application on the Integration-Console-issued-key model (Canon 7 §28 · `STATE/AUTONOMOUS_RUN_PLAN.md §11`). Two surfaces span M17: (a) the **tenant-facing/journey surface** — an application authors an `ApplicationContract_v0`, receives a scoped bearer-key prefix from an Integration Console issuance ceremony, and composes a session as a personal client of the answering service (M14-sealed seam), consumed by tenant journey code per Canon 6 and interface constraints per Canon 5; (b) the **governance-in-client constraints** — approval blocks rather than warns, silence never approves, the chat proposes and never decides — bound structurally at W4 as pytest-only AST-scan invariants over the personal-client surface authored at W3, per B-frontends-Q1 owner ruling (`STATE/DECISIONS.md:12115` verbatim, DAP UI Handoff Brief §5). No principal / user-memory data is written by any M17 surface until R-21 rules (`STATE/DECISIONS.md:12333 + 12366` verbatim — user-memory class behind tenant-wide flag OFF by default, no consent model assumed). W5 is the milestone integration seal binding all four sub-waves + milestone snapshot pin over `ApplicationContract_v0.model_json_schema()`.

## MUST DO

1. **W1 · `ApplicationContract_v0` shape-freeze** — author `contracts/application_contract_v0.py` (`ApplicationContract_v0` frozen pydantic with `model_config = ConfigDict(extra="forbid", frozen=True)`, closed 7-field tuple: `application_id · tenant_id · issued_at · issuer_console_id · capability_manifest · receipt_policy · citations`); `application_id` regex `^app_[a-z0-9_-]+$`; `tenant_id` regex `^t_[a-z0-9_-]+$` mirroring M11 per-tenant DB naming discipline; `issued_at` ISO-8601 string; `issuer_console_id` regex `^console_[a-z0-9_-]+$`; `capability_manifest: Tuple[str, ...]` with `default_factory=tuple` binding at contract level to sealed L-5 register category names; `receipt_policy: Literal["required", "forbidden"]` closed 2-tuple; `citations: Tuple[str, ...]` with `default_factory=tuple`. Additive-only per SO §3.8: NEW module + NEW invariant test file + NEW `application_contract_v0.contract_snapshot.json` (frozen JSON schema snapshot for parity registry) + APPEND-ONLY entry to `test_frozen_contract_snapshot_parity.py` mapping (mirrors M16-W1 precedent). Zero ratification-adjacent field per AC-18. `canon_ref: NEXT_MILESTONES_PLAN §11 (C.23 goal "Application-contract enforcement + personal client for tenant-of-one" verbatim) + Canon 7 §28 (Integration-Console-issued-key model · AUTONOMOUS_RUN_PLAN §11) + Canon 5 (Interface Architecture · shape constraint on client-consumable contract) + Canon 6 (User Journeys · anchor for `application_id` + `tenant_id` binding a journey to a tenant) + SO §3.8 + SO §3.10-α (closed-schema discipline · frozen pydantic + extra=forbid + closed Literal + regex + sha256 snapshot pin) + AC-18 (proposes-never-ratifies · contract carries no decision-adjacent field).`

2. **W2 · Integration Console issued-key model (Canon 7 §28)** — author `services/integration_console/__init__.py` + `services/integration_console/key_issuance.py` with a single public surface `issue_application_key(*, application_contract: ApplicationContract_v0) -> Tuple[str, str]` returning `(application_id, opaque_bearer_key_prefix)` where `opaque_bearer_key_prefix` is a `sha256[:32]` deterministically derived from the canonical sorted-key JSON of the contract's `application_id + tenant_id + issued_at + issuer_console_id` tuple (deterministic pure-data-in per M14-W4 owner tier-1 ruling 2026-09-19 "a code path is a code path" precedent · no live signing at issuance boundary · signing/verification stays under sealed M12b-W1 primitive at any point that requires it). Structural role separation per Canon 8 §W11: this module does **NOT** persist keys (persistence stays at M11 tenant DBs consumed by W3 for session composition), does **NOT** compose sessions (composition stays at W3), does **NOT** sign session tokens (signing stays at W3 or later if authored at all). AST-scan invariants: (i) zero import of `motor` / `services.data.repository` / `services.answering_service.*` (persistence + session composition stays out); (ii) zero import of `services.watch.signature_primitive` at execution scope beyond keygen-only helper reference (pure-data-in); (iii) zero write/decision surface function names beyond `issue_*` (banned prefixes across `ast.walk` FunctionDef/AsyncFunctionDef: `sign_`, `decide_`, `ratify_`, `admit_`, `route_`, `author_`, `persist_`, `emit_`, `store_`, `compose_`). Fail-closed: any `ApplicationContract_v0` shape drift refuses at pydantic construction. `canon_ref: Canon 7 §28 (Integration-Console-issued-key model verbatim per AUTONOMOUS_RUN_PLAN §11) + Canon 8 §W11 (one-task-one-identity · structural role separation · AST-enforced) + Canon 5 (Interface Architecture · issuance boundary constraint) + M12b-W1 (Ed25519 primitive sealed · reference only · no signing at issuance) + M11 (tenant DBs sealed · not imported here) + M14 (answering service sealed · not imported here · role-separated) + SO §3.8 + SO §3.10-α + SO §6.7.`

3. **W3 · Personal Client session surface (tenant-of-one)** — author `services/personal_client/__init__.py` + `services/personal_client/session.py` + `contracts/personal_client_session_v0.py` binding a `PersonalClientSession_v0` frozen pydantic contract (closed 6-field tuple: `session_id · application_id · tenant_id · started_at · ask_ids · pending_receipts`; `session_id` regex `^pcs_[a-z0-9_-]+$`; `ask_ids: Tuple[str, ...]` and `pending_receipts: Tuple[str, ...]` both with `default_factory=tuple`; `extra="forbid"` + `frozen=True`) and a single public composition surface `compose_session(*, application_contract: ApplicationContract_v0, bearer_key_prefix: str) -> PersonalClientSession_v0` (deterministic pure-data-in per M14-W4 precedent · returns identity instance per SO §3.10-α `type() is` discipline). Session ask emission surface `emit_ask(*, session: PersonalClientSession_v0, payload: str) -> str` routes through **sealed M14-W2 Mkondo registry `admit`** + **sealed M14-W3 `asks` collection append** under `t_<tenant_id>` per M11 discipline; returns the ask_id string. Structural role separation per Canon 8 §W11 · AST-scan invariants: (i) module authors NO decision surface (banned prefixes: `decide_`, `ratify_`, `admit_`, `accept_`, `reject_`, `approve_`, `sign_`); (ii) **R-21 hard ban** — module does NOT import any principal-data / user-memory surface (banned: `services.memory.*`, `services.principal_data.*`, `services.user_memory.*`, `services.memory_compaction.*` — enforced via `ast.Import` + `ast.ImportFrom` walk with prefix match on any of the banned roots · owner-outstanding per `STATE/DECISIONS.md:12333 + 12366` verbatim); (iii) zero learned / model-client import (banned: `openai`, `anthropic`, `services.solva_v2`, `services.mtafiti`, `services.perception`, `services.cif.detection` + case-insensitive `llm` substring); (iv) session composition + ask emission consume sealed M14 seam by identity import (`services.mkondo.registry` module import present · `services.answering_service.collections` module import present). Second new contract `contracts/personal_client_session_v0.py` gets its own frozen JSON schema snapshot + parity registry entry per M16-W1 precedent. `canon_ref: NEXT_MILESTONES_PLAN §11 (personal client for tenant-of-one) + Canon 6 (User Journeys · session composition anchor) + Canon 5 (Interface Architecture · session surface constraint) + M14 (answering service seam sealed · consumed by identity import) + M11 (per-tenant DB sealed · consumed via t_<tenant_id> discipline) + Canon 8 §W11 (one-task-one-identity · structural role separation) + R-21 (STATE/DECISIONS.md:12333 + 12366 verbatim owner-outstanding · no principal data written) + SO §3.8 + SO §3.10-α + AC-18 (contract carries no decision-adjacent field · proposes-never-ratifies applied to session boundary).`

4. **W4 · Governance-in-client three-invariant enforcement (B-frontends-Q1 verbatim)** — author `services/personal_client/governance_invariants.py` binding the **three B-frontends-Q1 governance invariants** as pytest-only AST-scan predicates over the personal-client surface authored at W3 (and any future personal-client module added under `services/personal_client/*.py`): (a) **approval blocks rather than warns** — every function whose name matches regex `(^|_)approv(e|al)(_|$)` in any `services/personal_client/*.py` module MUST contain `raise ApprovalBlocked` (or a sealed subclass) somewhere in its body AST-walk; a `logging.warning`-only path with no subsequent raise on the negative branch is a structural failure; enforced by scanning all matched function bodies + asserting the AST contains a `Raise` node whose exception name is `ApprovalBlocked` or resolves to it structurally. (b) **silence never approves** — every function in `services/personal_client/session.py` (session-boundary module) whose parameter list contains an `Optional[X]` / `X | None` annotation MUST have an early-return / raise on the None branch producing a refusal (structural: AST-walk asserts the function body contains either `raise <name>Error` OR `return False` OR `return None` OR `raise <name>Refused` on the empty-input branch before any other action); a function whose empty-input path silently succeeds is a structural failure. (c) **chat proposes and never decides** — every function in `services/personal_client/*.py` whose name contains substring `chat` (case-insensitive) OR whose docstring contains "chat" MUST NOT reference any decision-surface identifier by name anywhere in its body AST (banned identifier substring set: `decide`, `ratify`, `admit`, `sign`, `approve`, `route`, `accept`, `reject`); a match is a structural failure. Module itself contains ONLY pure predicates: `check_approval_blocks_rather_than_warns() -> bool` + `check_silence_never_approves() -> bool` + `check_chat_proposes_never_decides() -> bool` + `ApprovalBlocked` exception class. AST-scan invariant on module itself: (i) zero side-effect / write surface (no I/O · no persistence · no logging beyond the exception class docstring); (ii) module name `governance_invariants.py` itself has zero decision-surface function names; (iii) `type(ApprovalBlocked) is type` (real exception class not shadow). `canon_ref: STATE/DECISIONS.md:12115 verbatim B-frontends-Q1 owner ruling ("approval blocks rather than warns, silence never approves, the chat proposes and never decides · DAP UI Handoff Brief §5") + STATE/DECISIONS.md:13600 (Frontend fidelity bar · DAP UI Handoff Brief §5 · extends to any client surface) + AC-18 (proposes-never-ratifies · extended to client surface) + Canon 8 §W11 (one-task-one-identity · structural role separation) + Canon 5 (Interface Architecture · client surface constraints) + Canon 6 (User Journeys · governance holds through journey) + SO §3.8 + SO §6.7.`

5. **W5 · M17 milestone integration seal + snapshot pin (M17 closing gate)** — author full integration test at Commit-A binding W1..W4 end-to-end: (i) instantiate an `ApplicationContract_v0` via W1 → (ii) issue a `(application_id, bearer_key_prefix)` via W2 `issue_application_key` → (iii) compose a `PersonalClientSession_v0` via W3 `compose_session` → (iv) emit a single ask via W3 `emit_ask` routing through sealed M14 Mkondo `admit` + sealed answering-service `asks` collection append under `t_<tenant_id>` per M11 → (v) verify all three W4 governance invariants pass end-to-end over the promoted personal-client surface (`check_approval_blocks_rather_than_warns()`, `check_silence_never_approves()`, `check_chat_proposes_never_decides()` all return True) → (vi) assert **NO principal-data write occurred** structurally (R-21 discipline verified end-to-end · module import graph inspected structurally · no `services.memory.*` / `services.principal_data.*` / `services.user_memory.*` at any node in the personal-client dependency closure). **Milestone snapshot pin**: sha256 of canonical sorted-key JSON of `ApplicationContract_v0.model_json_schema()` binding the W1 surface across milestone (mirrors M16-W5 `cba422542da…` precedent · pinned as constant `_M17_MILESTONE_SNAPSHOT_SHA256` in test file). `canon_ref: SO §6.2 EXIT clause (milestone gate closes on a test that binds all sub-waves' evidence) + all W1..W4 canon anchors + SO §3.10-α (milestone snapshot sha256 pin binds cross-milestone drift-catch) + R-21 verbatim (no principal data written · end-to-end proof).`

## MUST NOT

- Admit an `ApplicationContract_v0` via any M17 surface that does not shape-match the W1-sealed pydantic verbatim (shape drift refuses at pydantic construction). `canon_ref: SO §3.10-α + AC-18.`
- Import any principal-data / user-memory / memory-compaction surface into any M17 module until R-21 rules — banned root prefixes across `ast.Import` + `ast.ImportFrom` walk: `services.memory.*` · `services.principal_data.*` · `services.user_memory.*` · `services.memory_compaction.*`. AST-scan enforced at W3 module + assured at W5 by dependency-closure walk. `canon_ref: STATE/DECISIONS.md:12333 + 12366 verbatim R-21 ("R-21 (user-memory class, consent model): owner input outstanding — implement the class behind a tenant-wide flag, off by default, no consent model assumed, no principal data written until ruled").`
- Route a personal-client session ask that has NOT first passed through sealed M14-W2 Mkondo registry `admit` + sealed M14-W3 `asks` collection append (single-writer + role-separation preserved). `canon_ref: M14 seal · Canon 1 §62 (single-writer ledger discipline extended to ask persistence) · Canon 8 §W11.`
- Author any personal-client path at W4 that treats a `logging.warning` as substitute for an `ApprovalBlocked` raise on the negative branch of an approve/approval-named function (owner B-frontends-Q1 verbatim: "approval blocks rather than warns"). AST-scan enforced at W4. `canon_ref: STATE/DECISIONS.md:12115 verbatim.`
- Author any session-boundary surface at W4 that admits silent/empty / None input as an approval without an explicit refusal on the empty-input branch (owner B-frontends-Q1 verbatim: "silence never approves"). AST-scan enforced at W4. `canon_ref: STATE/DECISIONS.md:12115 verbatim.`
- Author any chat-named or chat-docstring-annotated path at W4 that also references a decision-surface identifier (owner B-frontends-Q1 verbatim: "the chat proposes and never decides"). AST-scan enforced at W4. `canon_ref: STATE/DECISIONS.md:12115 verbatim + AC-18.`
- Sign session tokens in `services/integration_console/key_issuance.py` — signing stays under sealed M12b-W1 primitive at any authoring point that requires it (structural role separation per Canon 8 §W11). `canon_ref: Canon 8 §W11 + M12b-W1 + SO §6.7.`
- Persist keys / sessions / asks in `services/integration_console/key_issuance.py` — persistence stays under M11 tenant DBs consumed by W3 for session composition only (structural role separation). `canon_ref: Canon 8 §W11 + M11 seal.`
- Compose sessions in `services/integration_console/key_issuance.py` — session composition stays at W3 (structural role separation). `canon_ref: Canon 8 §W11 + M12b-W1 precedent (signing primitive isolated at Watch service).`
- Add any new TCB member outside `tcb_enumeration_v1`'s R-3 method (Stop-Condition #3 · owner-only ruling · applies to all M17 waves). `canon_ref: SO §6 stop-conditions.`
- Widen `ApplicationContract_v0` / `PersonalClientSession_v0` shape after W1 / W3 seal without a ceremony (shape-freeze mandate · sha256-pinned baselines per SO §3.10-α). `canon_ref: SO §3.10-α + SO §6.4 NOTHING-BEYOND clause applied to M17.`
- Refactor any sealed module (`contracts/*` pre-M17 · sealed M14 modules · sealed M11 tenant-DB primitives · sealed M12b-W1 signature primitive · sealed M16 CIF surfaces · sealed W1/W2/W3/W4 M17 surfaces after their seal boundary) at any point during M17. Any change to those files is a refactor and refused. `canon_ref: SO §3.8.`
- Anything not in the five MUST-DO items above. SO §6.4 NOTHING-BEYOND clause applied to M17 per owner steer 2026-09-19T~12:45Z ("if the card needs something canon doesn't anchor, that is a fork · bank it · don't improvise it").

## EXIT

**Placeholder EXIT node IDs (to be filled at CP-M17-W1..W5 Commit-A pinning · every cited test file MUST exist on disk at promotion for `test_every_cited_exit_test_file_exists_on_disk` invariant per `backend/tests/invariants/test_seal_cites_card.py`):**

**W1 (Commit-A `<pending>` · `ApplicationContract_v0` shape-freeze · target +8 tests = 7 CIF-parallel invariants + 1 auto-collected wizard existence check · additive-only per SO §3.8):**
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_module_importable_end_to_end
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_required_field_set_matches_c23_scope
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_config_extra_forbid
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_config_frozen
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_application_id_pattern_matches_app_prefix
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_tenant_id_pattern_matches_t_prefix_m11_discipline
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_receipt_policy_is_closed_two_tuple_literal
- tests/invariants/test_m17_w1_application_contract_shape_freeze.py::test_application_contract_v0_shape_snapshot_sha256_matches_pinned_baseline
- tests/invariants/test_phase_7_stage_b_3_wizard.py::test_prior_contract_file_exists_and_stable_at_7b_3[application_contract_v0.py] (auto-collected +1)
- W1 shape-snapshot sha256 pinned baseline: `<computed at W1 Commit-A>`.

**W2 (Commit-A `<pending>` · Integration Console issued-key model · target +7 tests):**
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_integration_console_module_surface_importable_end_to_end
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_issue_application_key_yields_deterministic_prefix_for_same_contract
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_issue_application_key_yields_distinct_prefixes_for_different_tenants
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_integration_console_ast_no_persistence_import
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_integration_console_ast_no_session_composition_import
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_integration_console_ast_no_decision_surface_function_names
- tests/invariants/test_m17_w2_integration_console_key_issuance.py::test_integration_console_refuses_shape_drifted_contract_at_pydantic_construction

**W3 (Commit-A `<pending>` · Personal Client session surface · target +8 tests = 7 session invariants + 1 auto-collected wizard existence check for `personal_client_session_v0.py`):**
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_session_module_surface_importable_end_to_end
- tests/invariants/test_m17_w3_personal_client_session.py::test_compose_session_yields_identity_personalclientsession_v0_instance
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_ast_no_principal_data_import_r21_hard_ban
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_ast_no_decision_surface_function_names
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_ast_no_learned_or_model_client_import
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_emit_ask_routes_through_sealed_m14_mkondo_registry_admit
- tests/invariants/test_m17_w3_personal_client_session.py::test_personal_client_emit_ask_persists_under_t_prefix_per_tenant_db_m11_discipline
- tests/invariants/test_phase_7_stage_b_3_wizard.py::test_prior_contract_file_exists_and_stable_at_7b_3[personal_client_session_v0.py] (auto-collected +1)

**W4 (Commit-A `<pending>` · Governance-in-client three-invariant · target +7 tests):**
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_governance_invariants_module_surface_importable_end_to_end
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_approval_blocks_rather_than_warns_ast_scan_across_personal_client_surface
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_silence_never_approves_ast_scan_on_session_boundary_signatures
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_chat_proposes_and_never_decides_ast_scan_across_personal_client_surface
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_approvalblocked_exception_is_structural_refusal_type
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_governance_invariants_module_pure_predicates_no_side_effects_on_import
- tests/invariants/test_m17_w4_governance_in_client_invariants.py::test_governance_invariants_module_no_decision_surface_function_names

**W5 (Commit-A `<pending>` · M17 milestone closing gate · target +7 tests · milestone_status DRAFTED → CLOSED at this seal):**
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_all_sub_wave_surfaces_importable_end_to_end
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_end_to_end_application_registers_key_issued_session_composed_ask_emitted
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_governance_three_invariants_pass_end_to_end
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_no_principal_data_write_under_r21_hard_ban_end_to_end_dependency_closure
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_milestone_snapshot_pin_over_applicationcontract_v0_json_schema
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_ask_persists_under_t_prefix_tenant_db_and_receipt_policy_honored
- tests/invariants/test_m17_w5_seal_integration.py::test_m17_bearer_key_prefix_is_deterministic_pure_data_in
- W5 milestone snapshot pin sha256 baseline: `<computed at W5 Commit-A>`.

**Target ratchet delta for M17:** ratchet 5414 → 5414 + ~37 across five sub-waves (W1 +8 · W2 +7 · W3 +8 · W4 +7 · W5 +7). Exact deltas reconciled line-by-line at each Commit-A per SO §3 no-silent-rebaselining discipline.

**Gate to close M17 as a milestone:** all five sub-waves W1–W5 sealed with full pre-seal `BASELINE_GUARD=1` double-green byte-identical proof + zero regression + zero flip + card_sha256 re-pinned at `milestone_status → CLOSED`.

## STOP

- Any `ApplicationContract_v0` / `PersonalClientSession_v0` shape drift from the W1 / W3 shape-freeze verbatim — PRE-RULED at SO §3.10-α: refuse the widening; bank as fork.
- Any Integration Console module implementation that reaches into persistence or session composition surfaces at W2 — refuse the coupling; bank as fork (Canon 8 §W11 structural role separation).
- Any Personal Client module implementation that imports any principal-data / user-memory surface at W3 — refuse the coupling; bank as fork (R-21 hard ban until ruled per `STATE/DECISIONS.md:12333 + 12366` verbatim).
- Any personal-client path at W4 that carries a warn-and-continue pattern on the negative branch of an approve-named function — refuse the pattern; bank as fork (`STATE/DECISIONS.md:12115` verbatim "approval blocks rather than warns").
- Any session-boundary surface at W4 that admits silent/empty input as approval — refuse the pattern; bank as fork (`STATE/DECISIONS.md:12115` verbatim "silence never approves").
- Any chat-named path at W4 that carries a decision-surface identifier — refuse the coupling; bank as fork (`STATE/DECISIONS.md:12115` verbatim "the chat proposes and never decides").
- Any milestone-integration binding at W5 that requires a canon anchor not extracted in this card — refuse; bank as fork per SO §6.4 NOTHING-BEYOND applied to M17 (owner steer 2026-09-19T~12:45Z verbatim: "if the card needs something canon doesn't anchor, that is a fork · bank it · don't improvise it").
- Any proposal for a MUST-DO item that is not one of the five above — refuse and report as fork under SO §6.4 NOTHING-BEYOND clause applied to M17.
- Absolute stop conditions from §6 remain in force: (i) second path to external model client · (ii) verifier sharing credentials with writer · (iii) bypass-shaped parameter on custody crossing.

## ANCHORS

**Scope-anchor canon files (all opened this session):**
- `notes/NEXT_MILESTONES_PLAN_20260917.md §11` verbatim (C.23 goal · Application-contract enforcement + personal client for tenant-of-one · depends M9 P5 / M11 / M12 · risk Low-medium).
- `notes/PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md §Tenant Apps (C.23) row · line 144` (C.23 L1 external-repo baseline · no enforcement wire in Extraction-Akki).
- `STATE/AUTONOMOUS_RUN_PLAN.md line 67` (M17 · Reference application on the Integration-Console-issued-key model · Canon 7 §28).

**Owner-ruling anchors (verbatim, banked):**
- `STATE/DECISIONS.md:12115` B-frontends-Q1 (verbatim · governance-in-client three invariants · DAP UI Handoff Brief §5).
- `STATE/DECISIONS.md:13600 + 13630 + STATE/STANDING_ORDERS.md:445` (Frontend fidelity bar · functional parity with five-stage pattern + DAP UI Handoff Brief §5 · extends to any client surface).
- `STATE/DECISIONS.md:12333 + 12366` (R-21 owner-outstanding verbatim · user-memory class · tenant-wide flag OFF by default · no consent model assumed · no principal data written until ruled).
- `STATE/DECISIONS.md:13655` (owner END OF BUILD authority 2026-09-19T~00:20Z · M17 sequence position).
- Owner steer 2026-09-19T~12:45Z verbatim (this-session · banked at CP-M17-W1 Commit-B DECISIONS preamble).

**Canon anchors:**
- Canon 5 (Interface Architecture · client surface constraints · consumed as interface anchor across W1..W4).
- Canon 6 (User Journeys · session composition anchor · consumed as journey anchor at W1 + W3).
- Canon 7 §28 (Integration-Console-issued-key model).
- Canon 8 §W11 (one-task-one-identity · structural role separation · consumed by all M17 AST scans).

**Consumed sealed modules (by identity import · additive-only per SO §3.8):**
- `contracts/handoff_contract.py` (sealed M14-W1 · precedent frozen pydantic model for W1 + W3 shape-freeze pattern).
- `services/mkondo/registry.py` (sealed M14-W2 · consumed by W3 for session ask routing).
- `services/answering_service/collections/*.py` (sealed M14-W3 · consumed by W3 for ask persistence under `t_<tenant_id>` DB per M11).
- `services/capability_registry.py` (sealed W1b·CP4 · consumed at W1 as `capability_manifest` category-name anchor).
- `services/watch/signature_primitive.py` (sealed M12b-W1 · consumed at W2 by identity reference only · no signing at issuance).
- `services/doc0_attributes/tcb.py` (sealed W-M2-SW7 · Doc-0 Attr-1 · consumed structurally by W2/W3/W4 AST-scan invariants where TCB membership is asserted).
- `tests/invariants/test_phase_7_stage_b_3_wizard.py` (sealed W-7bB wizard invariant · parametrizes over every `contracts/*.py` · adding two new contracts at M17 auto-generates two new parametrizations).
- `tests/invariants/test_frozen_contract_snapshot_parity.py` (append-only entries for `application_contract_v0.py` + `personal_client_session_v0.py` mappings per M16-W1 precedent).

**Standing-order anchors:**
- SO §3.8 (thin-kernel additive-only).
- SO §3.10-α (closed-schema discipline · frozen pydantic + extra=forbid + closed Literal + regex + sha256 snapshot pin).
- SO §6.2 (pre-authorised card drafting · batch-ratification at preceding-milestone seal · "e1_dev drafts cards for M13–M17, memory layer, and frontends from canon and the SER").
- SO §6.4 NOTHING-BEYOND clause applied to M17 scope (owner steer 2026-09-19T~12:45Z).
- SO §6.7 M17 sequence position (M16 close → M17 → memory layer after C.13 close → frontends).
- SO §3.3 3-commit seal protocol (Commit-A code · Commit-B state · Commit-C fixup).
- SO §7 R-1..R-6 (seal integrity + ORCH_BOOT R-6 regen at boundaries).

---

## DRAFT NOTES (removed at promotion)

**Why sub-wave order:** the order `W1 → W2 → W3 → W4 → W5` follows the M14/M15/M16 precedent of shape-freeze-first (contract at W1) → issuance-surface (W2) → composition-surface (W3) → invariant-enforcement (W4) → milestone-integration-seal (W5). This mirrors M16's `contract → detection → acceptance → routing → halt+seal` pattern exactly.

**Why 5 MUST-DOs vs 5-10 authorised range:** the C.23 scope in `NEXT_MILESTONES_PLAN §11` is compact ("Application-contract enforcement + personal client for tenant-of-one"). A 5-MUST-DO decomposition maps 1:1 onto the two-surface span the owner requested (three MUST-DOs on the tenant-facing/journey surface at W1+W2+W3, one MUST-DO on the governance-in-client surface at W4, one milestone seal at W5). Expanding above 5 would either introduce scope not anchored in canon (fork per owner steer verbatim) or split existing MUST-DOs artificially. If owner rules at ratification that any of these MUST-DOs should split (e.g., separate `PersonalClientSession_v0` contract from session surface), the split lands as a re-pin at the ratification boundary.

**Card-drift-risk items surfaced during drafting (bank at CP-M17-W1 Commit-B DECISIONS preamble if any fires during build):**
1. **DAP UI Handoff Brief location** — not opened this session (referenced only via banked owner citations `STATE/DECISIONS.md:12115` + `STATE/DECISIONS.md:13600`). If W4 build reveals the Brief carries §5-language details not fully captured by the three-invariant AST decomposition, bank as fork.
2. **Five-stage pattern** — the "established five-stage pattern" from `STATE/DECISIONS.md:13600` maps to ThinkLab's `Frame → Name/Candidates → Challenge/Tension → Weigh → Lock-in` per `notes/prototype_inventory_v8.md:341` + `notes/wave_g_step0_v8/v8_design_spec.txt:201`. This is a **fidelity bar reference** not a MUST-DO for M17 (M17 builds the reference application not the ThinkLab client). If the personal client at W3 needs a stage-strip surface to be a genuine tenant-facing surface, bank as fork at W3 Commit-B (owner steer: don't improvise scope).
3. **`ApprovalBlocked` exception class location** — first authored in this card at W4 module. If W3 surface needs to raise `ApprovalBlocked` at session composition, the exception class needs to be importable at W3 authoring time — which requires either (i) authoring `ApprovalBlocked` first at W4 (out of sub-wave order) OR (ii) authoring it as a small module `services/personal_client/exceptions.py` at W3 that W4 governance_invariants imports. Bank the choice as a small state-only decision at W3 Commit-B.
4. **Answering-service `asks` collection surface** — W3 assumes M14-W3 authored a stable `asks` append surface. Verified at drafting: `services/answering_service/collections/asks.py` (or equivalent under M14-W3 seal) exists per M14.md EXIT-W3. If the surface signature has drifted from what W3 expects at build time, bank as fork.

**End of DRAFT NOTES.**
