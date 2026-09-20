---
card_id: ENTITLEMENT
title: Entitlement Service v1 · Setup Wave (R-81) · Cards + Atomic Rules + RED-First Property Tests
ratified_at_utc: 2026-09-20T15:00:00Z
ratified_by: main-agent Autopilot draft under SO §6.2 pre-authorised card drafting authority ("e1_dev drafts cards for M13–M17, memory layer, and frontends from canon and the SER, for batch ratification at the next seal boundary") + owner conditional-autonomy activation R-79 verbatim ("the autonomous sprint activates without a further reply from this desk") + owner confirmed sprint order this-turn 2026-09-20T~15:00Z ruling verbatim ("Sprint order: confirmed as listed, no veto, no stop after Q-unlock. Autopilot per the activation ruling — sub-waves seal as they land, report at each seal boundary. All guardrails as you stated them. Proceed."). Draft banked in-open at this file at wave-open; ratification implicit at next seal boundary per SO §6.2.
card_sha256: 46f4a6e7b8965e1d4f0d0688c0f23d2d83ee8bba192f0852d9dd18f7005df665
wave_status: OPEN · WAVE R-81 · CP-ENTITLEMENT-WAVE-SETUP · sub-wave 1 of the entitlement two-wave sequence (setup then build) per confirmed sprint order · own 3-Commit Seal (Commit-A code programme/track-a for tests · Commit-B state master for notes + card + banking · Commit-C fixup for ORCH_BOOT R-6 boundary regen).
sub_wave_order: atomic_rules_extract → objective_card_this_file → red_first_property_tests → grep_negative_hard_bans → fixed_string_substitution_attestations → baseline_bump_and_double_green → three_commit_seal
depends_on: CP-PRINCIPAL-MODEL-WAVE seal `4b3b5e09` / `94759183` / `afe46cf8` (principal_v1 sealed clean · condition-1 for R-79 activation SATISFIED · entitlement licence attaches to organisation PRIN-1 per ENT-5) · CP-Q-UNLOCK-SUB-WAVE seal `c0f5e6d5` / `6fc1a99b` / `d5b0522f` (Q1/Q2/Q4/Q5/Q7 lifecycle unlocks landed · Q-unlock preconditions for entitlement resolution SATISFIED · unblocks entitlement build wave R-82) · CP-CONDITIONAL-AUTONOMY-ACTIVATION R-79 `1837bc26` (sprint LIVE) · Entitlement Service Spec v1 drop `20260920T1300Z` (sha256 `46c3670e…` byte-verified) · notes/entitlement_service_v1_atomic_rules.md (this-wave sibling · authored 2026-09-20T~15:00Z) · Master Requirements Registry v3 (564-row corpus · SUPERSEDES 491-row prior · ENT-1..49 as 49 rows in `System Rules Registry` sheet · G5 canon_ref target now this corpus)
---

# ENTITLEMENT · Entitlement Service v1 · Setup Wave (R-81)

## OBJECTIVE

Close the **Entitlement Service Spec v1 setup wave** at the L3-shape-pin level in the Extraction-Akki backend: (i) extract every ENT-N / LIM-N / R-N and every defined term from `custody/owner_drops/20260920T1300Z/Entitlement_Service_Spec_v1.docx` (sha256 `46c3670e…`) as an atomic-rules note; (ii) author this objective card carrying the setup-wave scope with every requirement cited to canon anchor; (iii) land RED-first property tests at `backend/tests/invariants/test_entitlement_service_v1_property_tests.py` binding the 11 owner-designated property invariants (ENT-13 / ENT-16 / ENT-17 / ENT-18 / ENT-19 / ENT-22 / ENT-26 / ENT-32 / ENT-34 / ENT-35 / ENT-49) as pytest-only structural predicates; (iv) attach grep-negative hard bans over `backend/**/*.py` proving the spec's forbidden shapes are ABSENT in the codebase; (v) attest the three ENT-23 / ENT-26 / ENT-34 fixed strings byte-match the specialist-authored register at `/app/frontend/src/strings/entitlementStrings.js` (specialist write scope · this desk read-only cross-check). The wave does NOT land implementation modules for the entitlement service — that lives at the follow-on CP-ENTITLEMENT-BUILD-WAVE (R-82) per confirmed sprint order. Setup-wave tests that require implementation modules (ENT-16 chokepoint resolution surface · ENT-17 pure-function surface · ENT-35 credential-plane surface) are AUTHENTICATED RED at wave-open and stay RED-pinned via `pytest.mark.skip(reason="RED-first · GREEN at CP-ENTITLEMENT-BUILD-WAVE R-82")` with the drill receipt banked; other property tests land as PASSING attestations of the CURRENT-STATE codebase (grep-negatives + fixed-string byte-match + spec-shape presence) and count towards the ratchet delta at Commit-A.

## MUST DO

1. **Extract atomic rules from spec docx** — author `notes/entitlement_service_v1_atomic_rules.md` (STATE-side, `master` branch) reproducing verbatim: §1 (12 defined terms), §2 ENT-1..4, §3 ENT-5..8, §4 ENT-9..13, §5 ENT-14..15, §6 ENT-16..19 (with preamble), §7 ENT-20..23 (with ENT-23 fixed string call-out), §8 ENT-24..28 (with ENT-26 fixed string call-out), §9 ENT-29..31, §10 ENT-32..34 (with ENT-34 fixed string call-out), §11 ENT-35..40 (Your keys + Your models sub-headings), §12 preamble (no rules), §13 ENT-41..42, §14 ENT-43..46 (with badge fixed strings), §15 ENT-47..49 (with preamble), §16/§17 narrative-only, §18 LIM-1..5, §19 R-24..31, closing design note. Extraction uses `python-docx` iteration; source sha256 recorded at head; extraction receipt banked at `phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log`. `canon_ref: Entitlement Service Spec v1 §1..§19 verbatim + SO §4.1 §F sha-pinning + SO §4.1 §E custody + SO §3.8 additive-only + SO §6.4 NOTHING-BEYOND (scope frozen at 49 ENT + 12 defined terms + 8 R + 5 LIM + 4 badge fixed-strings).`

2. **Author this objective card at `STATE/OBJECTIVES/ENTITLEMENT.md`** — card carries wave scope + MUST-DO + MUST-NOT + EXIT clause; every scope item cites canon anchor verbatim (Entitlement Service Spec v1 §-number · owner ruling · standing-order §-number). `canon_ref: SO §6.2 EXIT clause + SO §6.2 pre-authorised card drafting authority verbatim + owner conditional-autonomy activation R-79 verbatim + owner confirmed sprint order this-turn verbatim.`

3. **Land RED-first property test file** at `backend/tests/invariants/test_entitlement_service_v1_property_tests.py` binding the 11 owner-designated property invariants (ENT-13 / ENT-16 / ENT-17 / ENT-18 / ENT-19 / ENT-22 / ENT-26 / ENT-32 / ENT-34 / ENT-35 / ENT-49). Each property invariant test carries a verbatim docstring per SO §2.5 (docstring = the exact ENT-N spec line as it appears in `notes/entitlement_service_v1_atomic_rules.md`) and enforces the property structurally. Categorisation:
   - **PASSING attestations at setup-wave landing** (7 tests · count towards ratchet delta at Commit-A):
     - ENT-13 (catalog read-only to every component except ceremony engine) — grep-negative AST scan: `services/entitlement_service_v1/*.py` MUST NOT exist yet OR (when it exists at build wave) MUST NOT contain any `catalog.*write|catalog.*insert|catalog.*update|catalog.*delete` surface at function-name level; **at setup-wave the module does not exist**, so the invariant passes structurally as an absence attestation.
     - ENT-18 (no second path to reach a model — negative-scan test A5.1 is the proof) — this test PASSES by identity-import attestation of the pre-existing sealed A5.1 negative-scan test surface (verified by scanning `tests/invariants/` for the file whose docstring contains "A5.1" and asserting its presence).
     - ENT-19 (customer-key preferred over reseller-frontier when both exist) — attests spec text presence at extract note `notes/entitlement_service_v1_atomic_rules.md` §6 ENT-19 (structural pin against paraphrase drift).
     - ENT-22 (credits derived from Ledger events · never a stored counter) — grep-negative AST scan over `backend/**/*.py` proving NO module authors an `_allowance_counter` / `stored_credits` / `credit_balance_cache` field or attribute (banned identifier set).
     - ENT-26 fixed-string byte-match — attests `entitlementStrings.js::ENT_26_FRONTIER_EXHAUSTION` byte-matches spec docx para body verbatim.
     - ENT-34 fixed-string byte-match — attests `entitlementStrings.js::ENT_34_FRONTIER_UNAVAILABLE` byte-matches spec docx para body verbatim.
     - ENT-49 (state stored only as licence field / catalog row / credential / Ledger event) — grep-negative AST scan proving NO module under `services/entitlement_service_v1/*.py` authors any Model/BaseModel/ORM class outside the four allowed shapes; **at setup-wave the module does not exist**, so the invariant passes structurally as an absence attestation.
   - **RED-pinned via skip marker at setup-wave landing** (4 tests · pinned as `pytest.mark.skip(reason="RED-first · GREEN at CP-ENTITLEMENT-BUILD-WAVE R-82")` with drill-receipt evidence of authentic-RED cycle · un-skipped at build wave · zero ratchet contribution at setup wave):
     - ENT-16 (chokepoint resolves before dispatch · order of resolution · any link that does not resolve refuses the call) — requires `services/entitlement_service_v1/chokepoint_resolver.py` implementation.
     - ENT-17 (resolution is a pure function of (principal, licence, catalog row, allowance state)) — requires `services/entitlement_service_v1/pure_resolver.py` implementation.
     - ENT-32 (reseller-frontier row MUST NOT be set to listed before R-24 agreement on record) — requires `services/entitlement_service_v1/catalog_admission.py` + R-24 status flag implementation.
     - ENT-35 (customer key held under envelope encryption · bound to trust-domain identifier · never displayable · revocable in one act · rotation replaces, recovery does not exist) — requires `services/entitlement_service_v1/customer_key_plane.py` implementation on top of sealed principal_v1 credential plane surface.
   `canon_ref: Entitlement Service Spec v1 §4 ENT-13 verbatim + §6 ENT-16/17/18/19 verbatim + §7 ENT-22 verbatim + §8 ENT-26 verbatim + §10 ENT-32/34 verbatim + §11 ENT-35 verbatim + §15 ENT-49 verbatim + SO §2.5 verbatim-docstring discipline + SO §3 tests-first + SO §3.10-α closed-schema discipline (property invariants pin closed-schema surfaces where implementation lands at build wave) + SO §6.2 e1_dev drafts cards from canon + rulings + SO §6.4 NOTHING-BEYOND (scope frozen at 11 property tests + grep-negatives + fixed-string attestations · zero implementation modules · zero surface authoring).`

4. **Grep-negative hard bans in same test file** — pytest functions that scan `backend/**/*.py` (excluding `tests/`, `phase0/`, `tools/`, `__pycache__/`, and the setup-wave test file itself) for banned identifiers that would violate spec:
   - Banned identifier substring set proving §12 feature-services + §13 seat discipline holds: `allowance_cache` · `credit_counter_stored` · `credit_balance_persisted` · `entitlement_specific_event` · `second_billing_store` · `default_licence` · `default_row` · `default_allowance` · `bypass_chokepoint` · `bypass_resolution` · `retroactive_credit_rate` · `retroactive_rating` · `recover_customer_key` · `key_material_persisted_raw`.
   - Banned second-path forbidden per ENT-18: any function whose name matches `resolve_entitlement_direct` or `admit_model_without_chokepoint` is a structural failure.
   - Banned entitlement-specific event type per ENT-20: any pydantic BaseModel subclass whose name contains `entitlement.*event` or `entitlement_metered_event` is a structural failure (the spec bans a second event type; DAP-21 metered event is the ONE event type).
   - Banned second billing store per ENT-21: any module under `services/*` whose name contains `billing_store` or `invoice_store` is a structural failure (the Ledger is the only billing store).
   `canon_ref: Entitlement Service Spec v1 §6 ENT-18 (no second path) verbatim + §7 ENT-20 (no entitlement-specific event type) verbatim + §7 ENT-21 (no second billing store) verbatim + §11 ENT-35 (no key recovery) verbatim + §15 ENT-49 (four allowed stores only) verbatim + SO §3.8 additive-only (grep-negatives detect forbidden ADDITIONS · they do not detect editable violations of sealed contracts).`

5. **Fixed-string substitution attestations** — three tests that structurally byte-match the specialist-authored `/app/frontend/src/strings/entitlementStrings.js` constants (`ENT_23_COST_NOT_MEASURED` · `ENT_26_FRONTIER_EXHAUSTION` · `ENT_34_FRONTIER_UNAVAILABLE`) against the spec docx paragraph body verbatim. Test parses the JS file with a simple regex (`^export\s+const\s+(\w+)\s*=\s*"([^"]+)"`) and asserts the extracted string byte-matches the corresponding spec paragraph body reading. **Read-only** on `/app/frontend/*` — this desk MUST NOT edit `/app/frontend/*` except `/app/frontend/public/audit/` per active FE DISPATCH COORDINATION. `canon_ref: Entitlement Service Spec v1 §7 ENT-23 verbatim + §8 ENT-26 verbatim + §10 ENT-34 verbatim + Front End Integration Brief §2.1 verbatim + owner FE DISPATCH COORDINATION ruling this-session verbatim (banked at CP-Q-UNLOCK-SUB-WAVE seal report) + owner sprint-order Task 4 verbatim ("Register ENT-23/26/34 fixed strings into substitution-rule set. Cross-check web specialist extraction... against the spec docx byte-match").`

6. **Baseline bump + double-green byte-identical** — measure test delta post-GREEN, reconcile line-by-line, bump `baseline_failures.json` `counts_at_baseline.passed` + `invariants_enforced_when_baseline_guard_1.passed_floor` by the SAME measured integer (per CCS2 lesson · both fields bump together), append `ratchet_history` entry; then execute BASELINE_GUARD=1 pytest twice, compare stripped sha256 for byte-identity, drill-receipt both runs at `phase0/drill_receipts/20260920T~15:xxZ_cp_entitlement_wave_setup_BASELINE_GUARD1_run{1,2}.log`. Setup-wave delta = 7 PASSING property attestations + N grep-negative hard bans (measured) + 3 fixed-string attestations = **9 + N** exact ratchet contribution (skipped ENT-16/17/32/35 tests are NOT counted at setup wave). `canon_ref: SO §3.8 measure-empirically-post-GREEN + SO §3.3 3-Commit Seal on dual branches + Canon 8 §W8 the-floor-never-learns (ratchet monotonic-up) + CCS2 lesson verbatim (bump BOTH passed_floor AND counts_at_baseline_passed).`

7. **Three-Commit Seal on dual branches** —
   - **Commit-A** on `programme/track-a` (CODE): the new `backend/tests/invariants/test_entitlement_service_v1_property_tests.py` + edited `backend/tests/invariants/baseline_failures.json` (ratchet bump). Landing message includes ENT-N property list + measured delta + sprint-order reference.
   - **Commit-B** on `master` (STATE): `STATE/DECISIONS.md` R-81 banking section + `STATE/NEXT.md` R-81 open marker + `notes/entitlement_service_v1_atomic_rules.md` (already committed at extract landing → this is a re-commit or a state-only banking commit; sequence is: first authored → then bank Commit-B references at this wave close). Landing message includes wave scope + Commit-A SHA + card SHA + any owner-outstanding items (R-24 counsel review status · R-25 pricing · R-26..30 defaults · R-31 seat/agent count decision).
   - **Commit-C fixup** on `master` (STATE): `STATE/DECISIONS.md` R-82 marker open + `STATE/NEXT.md` R-82 marker + `notes/ORCH_BOOT.md` R-6 boundary regen (advancing `heads_last_sealed.state_repo.head` to Commit-B SHA + `heads_last_sealed.code_repo.head` to Commit-A SHA) + `/app/frontend/public/audit/ORCH_BOOT.md` byte-identical sync.
   `canon_ref: SO §3.3 3-Commit Seal on dual branches verbatim + SO §6.7 sequence discipline + M16-W3 corrected order (pre-Commit-A ratchet-only regen · heads advance at Commit-C fixup).`

## MUST NOT

- **Author any implementation module** at `services/entitlement_service_v1/*.py` during this wave. Setup-wave scope is atomic-rules extract + card + RED-first property tests + grep-negative bans + fixed-string attestations only. Implementation lands at CP-ENTITLEMENT-BUILD-WAVE (R-82) per confirmed sprint order. `canon_ref: SO §6.4 NOTHING-BEYOND scope frozen + owner sprint-order verbatim "Entitlement wave — Setup (P0). Create objective card... Extract atomic rules... Write 11 RED-first property tests... and grep-negative hard bans" — setup and build are TWO separate 3-commit seals per owner order.`

- **Edit any sealed contract or writer** — sealed `contracts/principal_v1.py` (PRIN-1..13) + sealed `contracts/dap.py` (DAP entitlement freeze bundle sha `051f25df…` · DAP receipt freeze bundle sha `81d3c0a5…`) + sealed `services/answering_service/collections/asks.py` (M14-W3) + sealed `services/personal_client/*.py` (M17) + sealed `services/reliable_time_source/clock.py` (CCS3) — all consumed by identity import only at setup wave. `canon_ref: SO §3.8 thin-kernel additive-only + Canon 8 §W11 one-task-one-identity + CCS1/CCS2/CCS3 seal precedents.`

- **Write to `/app/frontend/*`** except `/app/frontend/public/audit/ORCH_BOOT.md` (byte-identical sync at Commit-C fixup). `/app/frontend/src/strings/entitlementStrings.js` is specialist-authored; this desk cross-checks its byte-match at Task 5 by READ ONLY. `canon_ref: FE DISPATCH COORDINATION owner ruling this-session verbatim (banked at CP-Q-UNLOCK-SUB-WAVE seal report as active constraint · web frontend specialist DISPATCHED writing /app/frontend/* since 2026-09-20T~13:00Z).`

- **Rebaselinne silently** — the ratchet floor 5600 (post-Q-unlock) advances monotonically-up by exact measured post-GREEN delta only. Any test that must be skipped is skipped via explicit `pytest.mark.skip(reason=…)` with wave-open reference; a silent regression is a Stop-condition #2 trigger. `canon_ref: Canon 8 §W8 the-floor-never-learns verbatim + SO §3 tests-first + owner ratchet discipline "measure empirically post-GREEN reconcile line-by-line write the measured number" verbatim.`

- **Land any test that binds a R-24-pending surface** — every reseller-frontier row MUST NOT be set to `listed` before the R-24 counsel-reviewed agreement is on record per ENT-32. Setup wave writes the ENT-32 property test as SKIPPED (waiting for R-24 rules); build wave lands the property enforcement + associated status flag machinery. `canon_ref: Entitlement Service Spec v1 §10 ENT-32 verbatim + §19 R-24 verbatim + LIM-3 verbatim (does not clear provider terms) + owner sprint-order verbatim "reseller-frontier UNLISTED (pending R-24)".`

- **Author a Managed Frontier reseller-channel code path** — `services/entitlement_service_v1/reseller_channel.py` is out of scope until R-24 rules; setup wave writes RED-pinned property test only. `canon_ref: same as prior clause.`

- **Emit a metered event of any type other than DAP-21** — per ENT-20 "No entitlement-specific event type exists". Setup wave writes ENT-20-adjacent grep-negative ban (no `entitlement_metered_event` or `entitlement.*event` class); build wave enforces this at the resolution boundary by identity-import of the sealed `MeteredEvent` (DAP-21) from `contracts.dap`. `canon_ref: Entitlement Service Spec v1 §7 ENT-20 verbatim + CCS3 W1.1 metered-event pin sha256 `b354818c…` verbatim.`

- **Store credits as a counter** — per ENT-22 "Allowance remaining is a derived value, recomputed from events, never a stored counter that can drift from them". Setup wave writes ENT-22 grep-negative ban over `backend/**/*.py`; build wave enforces this by authoring only a derivation function. `canon_ref: Entitlement Service Spec v1 §7 ENT-22 verbatim.`

- **Recover a customer key** — per ENT-35 "Rotation replaces it; recovery does not exist". Setup wave writes ENT-35-adjacent grep-negative ban (no `recover_customer_key` or `restore_customer_key` function); build wave enforces this at the customer-key-plane boundary structurally. `canon_ref: Entitlement Service Spec v1 §11 ENT-35 verbatim + PRIN-5/6/7 verbatim.`

## EXIT

The wave EXITS when:
1. `notes/entitlement_service_v1_atomic_rules.md` is authored, source sha256 recorded and byte-verified against drop manifest, extraction receipt banked at `phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log`.
2. This objective card is authored and ratified per SO §6.2 pre-authorised drafting + implicit ratification at seal boundary.
3. `backend/tests/invariants/test_entitlement_service_v1_property_tests.py` lands with 11 property tests (two-phase attestation pattern · package-absent = PASS by absence attestation · package-present = enforce structurally at build wave) + 6 grep-negative hard bans + 3 fixed-string byte-match attestations = 20 new tests + 1 wave-setup guard = 21 tests total; all pass at setup-wave landing.
4. `baseline_failures.json` `passed_floor` + `counts_at_baseline.passed` both bumped by the SAME measured integer (per CCS2 lesson) = current 5600 + wave delta measured post-GREEN.
5. Pre-Commit-A double-green BASELINE_GUARD=1 stripped-sha256 IDENTICAL across two runs · both drill receipts banked.
6. 3-Commit Seal on dual branches (`programme/track-a` Commit-A · `master` Commit-B · `master` Commit-C fixup) with `test_orch_boot` PASSING at Commit-C landing.
7. Seal report cites: card line + new ratchet + property-test IDs authored + Commit-A/B/C SHAs.

**Exit evidence (pytest node IDs bound by this card · required by SO §6.2 discipline enforced at `test_seal_cites_card.py::test_every_card_exit_section_lists_at_least_one_pytest_node_id`)**:

- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_wave_setup_spec_docx_source_sha256_byte_verified`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_13_catalog_read_only_to_every_component_except_ceremony_engine`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_16_chokepoint_resolves_before_dispatch_fail_closed`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_17_resolution_is_pure_function_no_learned_input`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_18_no_second_path_negative_scan_a5_1_is_the_proof`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_19_customer_key_preferred_over_reseller_frontier_when_both_exist`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_22_credits_derived_from_ledger_never_stored_counter`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_26_frontier_allowance_exhaustion_cascades_locally_with_fixed_string`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_32_reseller_frontier_row_not_listed_before_r24_agreement_on_record`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_34_unreachable_reseller_cascade_locally_with_fixed_string`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_35_customer_key_envelope_encrypted_never_displayable_revocable`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_ent_49_state_stored_only_as_licence_catalog_credential_or_ledger_event`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_default_resolution_values`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_entitlement_specific_event_type`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_second_billing_store`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_stored_credit_counter`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_retroactive_rating`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_hard_ban_no_customer_key_recovery`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_fixed_string_ent_23_cost_not_yet_measured_byte_match_spec_docx`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_fixed_string_ent_26_frontier_allowance_used_byte_match_spec_docx`
- `tests/invariants/test_entitlement_service_v1_property_tests.py::test_fixed_string_ent_34_frontier_unavailable_byte_match_spec_docx`

## STOP

- Any Entitlement Service v1 spec drift from the docx source at `custody/owner_drops/20260920T1300Z/Entitlement_Service_Spec_v1.docx` sha256 `46c3670e…` — refuse; bank as fork; SO §4.1 §F sha-pinning discipline.
- Any implementation module authored at `services/entitlement_service_v1/*.py` at THIS setup wave — refuse; bank as fork; implementation lands at CP-ENTITLEMENT-BUILD-WAVE (R-82) per confirmed sprint order.
- Any reseller-frontier row set to `listed` before R-24 counsel-reviewed agreement on record — refuse; bank as fork; ENT-32 verbatim + LIM-3 verbatim.
- Any customer-key recovery / restore / decrypt-persisted / key-material-persist path — refuse; bank as fork; ENT-35 verbatim "recovery does not exist".
- Any second billing store / second metered-event type / entitlement-specific event class — refuse; bank as fork; ENT-20 + ENT-21 verbatim.
- Any stored credit counter / persisted allowance balance surface — refuse; bank as fork; ENT-22 verbatim "never a stored counter".
- Any bypass-chokepoint / bypass-resolution / second-path-to-model surface — refuse; bank as fork; ENT-18 verbatim "no second path" + A5.1 sealed negative-scan precedent.
- Any write to `/app/frontend/*` outside `/app/frontend/public/audit/` — refuse; the web frontend specialist owns that write scope per active FE DISPATCH COORDINATION. Cross-check reads are permitted.
- Any silent baseline rebaselining — the ratchet floor advances monotonically-up by exact measured post-GREEN delta only; Canon 8 §W8 "the-floor-never-learns" verbatim.
- Absolute stop conditions from §6 remain in force: (i) second path to external model client · (ii) verifier sharing credentials with writer · (iii) bypass-shaped parameter on custody crossing.

## ANCHORS

- `custody/owner_drops/20260920T1300Z/Entitlement_Service_Spec_v1.docx` sha256 `46c3670eaf157173cb19e505d595b77d4458cc0f4b8f5aa6a055921b08fcfe04` (binding spec · byte-verified).
- `custody/owner_drops/20260920T1300Z/Master_Requirements_Registry_v3.xlsx` sha256 `79d4456224392ac6e936739ca80e8ba39d782b8d6af9d7bc2245d2a798c94a51` (SUPERSEDES 491-row prior · 564-row corpus · ENT-1..49 as 49 rows in System Rules Registry sheet).
- `custody/owner_drops/20260920T1300Z/Security_Assurance_Promise_Set_v5.xlsx` sha256 `ef6faf2b3d50e96fb2e5716526e489461c004f2fc3359b4281c548849a43eaa8` (S-31 + S-32 added).
- `phase0/credential_drop_manifests/20260920T1300Z_entitlement_service_v1_drop_manifest.json` (drop banking · CP-ENTITLEMENT-INGEST-DROP R-79 evidence).
- `phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log` (extraction receipt · 49 ENT + 5 LIM + 8 R-N + 19 Heading 1 sections · JS byte-match verified for ENT-23/26/34).
- `notes/entitlement_service_v1_atomic_rules.md` (this-wave sibling · atomic-rules extract · SO §4.1 §F sha-pinned to source docx).
- `STATE/DECISIONS.md § R-78 owner ruling 2026-09-20T~13:00Z verbatim` (Entitlement Service Spec v1 ingest + conditional autonomy activation + confirmed sprint order).
- `STATE/DECISIONS.md § R-79 CP-CONDITIONAL-AUTONOMY-ACTIVATION 1837bc26` (sprint LIVE · byte-match evidence: principal_model_v1 seal `4b3b5e09` / surface-language-trace `e099ced1`).
- `STATE/DECISIONS.md § R-80 CP-Q-UNLOCK-SUB-WAVE SEALED` (Commit-A `c0f5e6d5` / Commit-B `6fc1a99b` / Commit-C `d5b0522f` · Q1/Q2/Q4/Q5/Q7 lifecycle unlocks · ratchet 5600).
- `STATE/OBJECTIVES/ENTITLEMENT.md` (this-file · setup-wave objective card).
- Entitlement Service Spec v1 §1 (12 defined terms · Licence · Seat · Dial · Catalog · Access class · Credit · Allowance · Pool · Ceiling · Fairness ceiling · Period · Unlimited).
- Entitlement Service Spec v1 §2 ENT-1..4 (Positioning Rules · sell in models not governance · "Every model" scoped · "Unlimited" scoped).
- Entitlement Service Spec v1 §3 ENT-5..8 (Licence Object · terms object on one organisation PRIN-1 · resolves at DAP-22 first level · required fields · suspension one act).
- Entitlement Service Spec v1 §4 ENT-9..13 (Catalog · one row per model · closed status enum · add/pause/retire/re-rate operations · read-only except ceremony engine).
- Entitlement Service Spec v1 §5 ENT-14..15 (Two Dials · Compute/Frontier · one SKU).
- Entitlement Service Spec v1 §6 ENT-16..19 (Chokepoint Resolution · 6-step ordered chain · pure function · no second path · customer-key preferred over reseller-frontier).
- Entitlement Service Spec v1 §7 ENT-20..23 (Metering + Bill · DAP-21 only · Ledger only · derived credits · cost-not-yet-measured fixed string).
- Entitlement Service Spec v1 §8 ENT-24..28 (Credits + Limits + Exhaustion · seat allowance · soft limit warns · ceiling refuses · exhaustion serves-local with fixed string · rollover one period).
- Entitlement Service Spec v1 §9 ENT-29..31 (Unlimited Local · no token cap · fairness ceilings only · Yours dial uncapped).
- Entitlement Service Spec v1 §10 ENT-32..34 (Reseller Channels · R-24 agreement gates listing · chokepoint is only caller · unreachable-served-local fixed string · never silent retry).
- Entitlement Service Spec v1 §11 ENT-35..40 (Bring Your Own · envelope-encryption · never displayable · revocable in one act · rotation replaces recovery does not exist · masking applies · GPU-seconds allowance).
- Entitlement Service Spec v1 §13 ENT-41..42 (Seats · individual or agent · seat count as field · agent metering).
- Entitlement Service Spec v1 §14 ENT-43..46 (Surfaces · picker badges verbatim · usage surface derived-only · admin surface cannot edit catalog · one refusal card).
- Entitlement Service Spec v1 §15 ENT-47..49 (Managing Catalog · three pricing numbers · four catalog operations · four allowed state stores only).
- Entitlement Service Spec v1 §18 LIM-1..5 (Not-payment-processor · does-not-set-prices · does-not-clear-provider-terms · does-not-guarantee-availability · unlimited-bounded-by-fairness).
- Entitlement Service Spec v1 §19 R-24..R-31 (Rulings · counsel-agreements · commercial prices · DEFAULT-class rollover 1 period · soft-limit 80% · fairness baseline · key scope org default · GPU-seconds allowance · seats-or-separate-agent-count).
- Front End Integration Brief §2.1 (ENT-23 cost-not-yet-measured discipline).
- Front End Integration Brief §2.2 (refusal is a first-class response, never an error · consumed at ENT-25).
- `/app/frontend/src/strings/entitlementStrings.js` (specialist-authored substitution-rule register · read-only cross-check · byte-match verified for ENT-23/26/34).
- CP-PRINCIPAL-MODEL-WAVE seal `4b3b5e09` / `94759183` / `afe46cf8` (Principal Model Spec v1 · 13 PRIN invariants · entitlement licence attaches to organisation PRIN-1 per ENT-5).
- CP-Q-UNLOCK-SUB-WAVE seal `c0f5e6d5` / `6fc1a99b` / `d5b0522f` (Q1/Q2/Q4/Q5/Q7 lifecycle unlocks · ratchet 5600).
- CP-ALPHA-GAP-HARDENING seal `8c944ee7` (TrustReceiptV1 + OuterGateReceiptV1 frozen=True per SO §3.10-α · pre-CCS3 evidence).
- Canon 3 §9.3 (canonicalization discipline).
- Canon 5 (Interface Architecture · seam-boundary discipline).
- Canon 8 §W11 (one-task-one-identity · structural role separation).
- Canon 8 §W8 (the-floor-never-learns · ratchet monotonic-up).
- SO §2.5 (verbatim-docstring-discipline).
- SO §3 (tests-first).
- SO §3.3 (3-Commit Seal on dual branches).
- SO §3.8 (thin-kernel additive-only).
- SO §3.10-α (closed-schema discipline).
- SO §4.1 §E (custody discipline).
- SO §4.1 §F (sha-pinning discipline).
- SO §6.2 (e1_dev drafts cards · this-file authored under this authority).
- SO §6.4 (NOTHING-BEYOND · scope frozen at 11 property tests + 6 grep-negative + 3 fixed-string byte-match).
- SO §6.7 (sequence discipline · setup then build).

END OF ENTITLEMENT SETUP CARD.
