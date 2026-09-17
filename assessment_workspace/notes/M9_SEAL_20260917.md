READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M9 · SEAL WAVE-CLOSE + PLATFORM LAYER OVERALL COMPLETION ROLLUP · 2026-09-17

**CP-P6-CP6 · M9-SEAL** per PLATFORM_LAYER_REQUIREMENTS_v0_2.md Row 211 verbatim: *"wave-close report notes/M9_SEAL_YYYYMMDD.md · Inline OVERALL BUILD STATUS table per owner directive."*

**M9 Wave Window**: `programme/track-a` HEAD `1a2c3faa` (M8 SEAL close · 4433) → HEAD `2e82e4f` (CP-P6-CP5 · 4809). Master HEAD arc: `db98cf64` (M8 SEAL) → `7cc5b637` (CP-P6-CP5 fixup).

**M9 Wave Status: COMPLETE** — 36 code CPs sealed across P1..P6 + 1 wave-close CP · **+376 ratchet delta** (4433 → 4809) · zero rollback · one back-compat batch reconciliation · R-1..R-5 seal-chain integrity rules adopted mid-wave.

---

## §1 · Progress — what now works end-to-end

The Akki OS Pilot Platform Layer's **control-plane data model and invariant fabric are complete**. Every entity mandated by PLATFORM_LAYER_REQUIREMENTS_v0_2.md §10 exists as a frozen dataclass carrier. Every acceptance-criterion refusal in §12 has an executable preventive-charter refusal wrapper. Every mandate in §3 that is representable at the carrier layer is representable. The 15 CONTRACT-MODELED-vs-Real items in §8 all have shape-frozen carriers such that real-infra wiring is a bind-only change.

Concretely, at the end of M9 the platform layer refuses:
- Cross-tenant reads / writes / metering / audit visibility (P1-CP1 + P6-CP3)
- Clients supplying `tenant_id` at any surface (P1-CP1)
- Illegal tenant-lifecycle transitions (P1-CP6)
- Terminal-state `offboarded` outbound transitions (P1-CP6)
- Unknown roles (P2-CP1) · self-grants (P2-CP2) · deny-by-default permission grants (P2-CP3)
- Sessions unbound to tenant / revoked / >12h absolute / >1h idle (P2-CP4)
- Break-glass sessions without reason / 2nd-approver / notification / >4h duration (P2-CP5)
- Estates with unknown tier (P3-CP1)
- Connectors with empty scope / missing mou_task_ref (P3-CP2)
- Mode upgrades without approval (P3-CP3 + P3-CP4)
- Connection tests that attempt content read (P3-CP5 · SAFETY-FIRST)
- Compute integrations with unknown kind (P4-CP1) · allocations with unknown environment (P4-CP2)
- Jobs reading connectors not on task / above task-spec mode (P4-CP4)
- Task changes without approval reset (P4-CP5)
- Scheduler admission on wrong tenant / wrong class / capacity exceedance (P4-CP6)
- Metering wrong-tenant / wrong-period / reconciliation mismatch (P4-CP7)
- Reserved-capacity preemption (P4-CP8)
- Apps enabled without required connector-types / modes / compute-classes (P5-CP2)
- Enablement claims with inconsistent status / missing missing-requirements naming (P5-CP3)
- Wizard non-sequential progression / drafts >30 days / non-sandbox provisioning (P5-CP4)
- Provisioning reports with missing sub-lists / MoU reconciliation mismatch (P5-CP5)
- Theme entities with unknown tokens / oversized logos / oversized names (P5-CP6)
- Audit event mutation / deletion (P6-CP1) · missing required event types (P6-CP2)
- Cross-tenant access at any of 6 planes (P6-CP3)
- Unknown pilot-tenant keys / missing capture-at-provisioning (P6-CP4)
- Sandbox offboarding without cert-revocation / allocation-return / artefact-delete evidence (P6-CP5)

**Ratchet floor 4809 · aggregate BASELINE_GUARD=1 double-green byte-match on `4809 passed, 1 skipped, 438 warnings`.**

Every mechanism is preventive-charter (caller invokes at composition boundary), never enforcement hard-gate. Zero closed enums in any P1-P6 module; zero data-plane imports; zero domain tokens in any module source (grep-negative on the 21-token vocabulary per case-agnostic doctrine).

---

## §2 · How-much-to-go (§7 CPs remaining post-M9)

M9's §7 CP breakdown proposed ~35 CPs; final count: **36 code CPs + 1 wave-close = 37 total**. Zero CPs deferred.

Post-M9 platform-layer scope: **CONTRACT-MODELED items 1-15 real-infra bindings** (see §7 below). Each is a bind-only change — no refactor. Estimated: 15 downstream CPs across future milestones when real infra becomes available.

---

## §3 · Decisions taken (banked in DECISIONS.md, chronological)

1. **Owner-approved autonomous P2..P6 walk** (2026-09-17T~05:00Z): after P1 completion report, proceed through P2..P6 reporting only at phase seal boundaries.
2. **Path (a) BACK-COMPAT-FIRST** (2026-09-17T~08:55Z): reconcile master-side seal chain before opening CP-P6-CP5, in response to on-disk-vs-brief discrepancy surfaced by incoming session grounding.
3. **R-1..R-5 seal-chain integrity rules ratified** (2026-09-17T~09:15Z): five additive discipline rules banked at STANDING_ORDERS.md §7. R-5 (seal-file writer refuses Double-green line without raw logs) is now MANDATORY for every new CP.
4. **Path (c) SCOPED RECONSTRUCTION** (2026-09-17T~09:15Z): reconstruct per-CP receipts for the 4 P6 back-compat CPs (P6-CP1..CP4); leave P3/P4/P5 aggregate-only with honest disclosure; label all reconstructed receipts "RECONSTRUCTED POST-HOC AT HEAD <SHA> · <DATE>".
5. **Scope-count correction** (2026-09-17T~09:00Z): the actual back-compat gap is 20 CPs (P3-CP4 → P6-CP4), not 22. Grounded in `git log programme/track-a`.

---

## §4 · Discoveries not envisioned at M9 planning

1. **Case-agnostic self-catch keeps firing** (CP-P6-CP5): the `zero_domain_tokens` invariant caught its OWN test-source containing `"kikuyu"` in the `DOMAIN_TOKENS_21` tuple literal — same shape as the M7-W2-CP1 self-catch. The mechanism enforces the doctrine automatically; author vigilance is not the safeguard.
2. **Standing-orders pointer invariant** (CP-P6-CP5): `test_decisions_carries_pointer_near_bottom` caught a legitimate DECISIONS.md discipline slip during the R-1..R-5 ratification append. Regression prevented at delta-sweep time.
3. **The `pending-C-fixup` scale-invisibility failure mode** (root-cause note): 20 CPs of master-side sealing was missed because no writer-side check counted the accumulating placeholder tokens. R-1 + R-2 close this class of defect.
4. **Aggregate-vs-per-CP substantiation gap** (R-5 root cause): the ratchet_history's `commit: "PENDING"` entries created plausible-looking numeric evidence without raw drill logs. R-3 + R-5 close this class of defect.
5. **Seal-file writer as a discipline enforcer** (R-5 design insight): the R-5 rule makes the seal file itself the enforcement point — if the raw logs aren't on disk, the seal-file writer refuses to compose the Double-green line, so the chain becomes self-auditing.

---

## §5 · Recommendations

1. **Ratify R-1..R-4 into SO §7 with binding force** (R-5 is already mandatory per owner ruling 2026-09-17T~09:15Z). R-1..R-4 are currently recorded as "banked additive discipline" — elevating them to binding would prevent recurrence of the master-chain lag pattern.
2. **Author a boot-ritual probe script** at `tools/boot_ritual_seal_chain_probe.py` that mechanically executes R-1 + R-2 + R-3 checks and refuses to proceed if any fires. Not built yet; proposed as post-M9 discipline tooling (S-class, ~1 hour).
3. **Author a per-CP receipt-naming linter** at `tools/lint_seal_double_green.py` that scans every `phase0/output_verified_seals/cp_*.seal.txt` and verifies each referenced `GREEN1/GREEN2/RED/DELTA_GUARD0` log exists on disk. Would make R-5 grep-positive-verifiable at any time.
4. **Consider a downstream M-CONTRACT-MODELED milestone** to bind the 15 §8 items to real infrastructure. Each is a bind-only change per M9 discipline; the milestone would be a walk through the 15 items as real-infra becomes available (K8s cluster · MIG-enabled GPUs · Real IdP · Real PKI · Real KMS · Real session store · Real object store · etc.).
5. **The obfuscated pair-halves pattern for grep-negative doctrine** (CP-M7-W2-CP1 precedent, re-exercised at CP-P6-CP5) should be documented as the canonical way to encode a grep-negative check in a test whose source must be grep-negative — worth adding to SO as a small pattern-note.

---

## §6 · M9 OVERALL BUILD STATUS TABLE (per Row 211 verbatim: "Inline OVERALL BUILD STATUS table per owner directive")

### Phase P1 · Foundation (6/6 CPs SEALED · +35 ratchet · 4433 → 4468)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P1-CP1 · TENANT-CONTEXT-ENFORCEMENT | `services/platform_control_plane/tenant_context.py` | `e697ba63a9f5aa16065552109d2a86b6e17332c2` | `1a2c3faa042d31d73c3376babb63221aa719fc8d` | 4433 → 4440 (+7) | 7 |
| P1-CP2 · TENANT-ENTITY | `services/platform_control_plane/tenant_entity.py` | `95fbd8ebcd9f785927c4237363ec052ff6960678` | `a14e668dbe0b8d7bb3118882432a2ff63bf2a90e` | 4440 → 4445 (+5) | 5 |
| P1-CP3 · WORKSPACE-ENTITY | `services/platform_control_plane/workspace_entity.py` | `1f32d8d18dd1db73ad28978389b38c1cd61335cf` | `868c4af13dc8badd3ac866666b5ba9285a3c1a2c` | 4445 → 4450 (+5) | 5 |
| P1-CP4 · USER-ENTITY | `services/platform_control_plane/user_entity.py` | `711817de204aef74f78ca57a343658f50c26234f` | `2ec94b18caf5e638c220b4b8c5a897b953190a88` | 4450 → 4455 (+5) | 5 |
| P1-CP5 · SERVICE-ACCOUNT-ENTITY | `services/platform_control_plane/service_account_entity.py` | `a2857843fa8f80dde6330a926245ef02b930aeef` | `d0cdcb39ca74831c6d09494f17c99efe1d0d70e2` | 4455 → 4460 (+5) | 5 |
| P1-CP6 · TENANT-LIFECYCLE-FSM | `services/platform_control_plane/tenant_lifecycle.py` | `07fccbd0f142f0a58e7972577750aa840516e642` | `5b7944d1bd417f66fb2e2303c8e3144b80ec45b0` | 4460 → 4468 (+8) | 8 |

### Phase P2 · RBAC + session + break-glass (5/5 CPs SEALED · +48 ratchet · 4468 → 4516)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P2-CP1 · ROLE-REGISTRY | `services/platform_control_plane/role_registry.py` | `1031ccd35aaa10619c669c7dd40b094e441968a6` | `21125b706d19112406adf2a1672c76a4c8057411` | 4468 → 4473 (+5) | 5 |
| P2-CP2 · ROLE-ASSIGNMENT | `services/platform_control_plane/role_assignment.py` | `04eb3c753541f6b085c9df14b6b13679f4227160` | `e090d4c27d6801d44ae9fdd61e84e13f84ad8bab` | 4473 → 4480 (+7) | 7 |
| P2-CP3 · PERMISSION-EVALUATION | `services/platform_control_plane/permission_evaluation.py` | `f3c90a5aedf27f53869134aceccc6b31d844851a` | `b29317116e4010316ed076f5f6da76410a81f533` | 4480 → 4490 (+10) | 10 |
| P2-CP4 · SESSION-BINDER | `services/platform_control_plane/session_binder.py` | `a5af53fa088ae8a016b38effe5f32b982467192a` | `e1681becb0731710d93d9f1ce82ee7fe08561c96` | 4490 → 4502 (+12) | 12 |
| P2-CP5 · BREAK-GLASS-SESSION | `services/platform_control_plane/break_glass_session.py` | `ec07fdb0924b3a076a62e52286c309749d2d2f30` | `00309180714043e9b0b3fa19a7a8dff872cb1bdb` | 4502 → 4516 (+14) | 14 |

### Phase P3 · Estate + connector modes + connection test + mode-change approval (5/5 CPs SEALED · +53 ratchet · 4516 → 4569)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P3-CP1 · ESTATE-ENTITY | `services/platform_control_plane/estate_entity.py` | `1fcc34bf67bb74c070c626ea95a96535a56bcaa2` | `d27d2a2289c6e925880864c506a3e3e21e22984e` | 4516 → 4525 (+9) | 9 |
| P3-CP2 · CONNECTOR-ENTITY | `services/platform_control_plane/connector_entity.py` | `df6d3cf6dada703d28af5c92717a977a2bf2df9f` | `f974aa6177db3e8246cf93a9ecaac725578fd759` | 4525 → 4534 (+9) | 9 |
| P3-CP3 · CONNECTOR-MODE-LATTICE | `services/platform_control_plane/connector_mode_lattice.py` | `547ba3975d5ba4a199881eb5c8948f424a685d12` | `29a6da446c4b250cba2c476ad470811dd1699640` | 4534 → 4544 (+10) | 10 |
| P3-CP4 · MODE-CHANGE-APPROVAL | `services/platform_control_plane/mode_change_approval.py` | `10953615610a082d4e3e6376087a17978284efb3` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4544 → 4557 (+13) | 13 |
| P3-CP5 · CONNECTION-TEST | `services/platform_control_plane/connection_test.py` | `a53d6e6e7ff745bfb1a51d33af14be6dda7f1943` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4557 → 4569 (+12) | 12 |

### Phase P4 · Task-scoped access + compute + allocation + scheduler + metering (8/8 CPs SEALED · +88 ratchet · 4569 → 4657)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P4-CP1 · COMPUTE-INTEGRATION | `services/platform_control_plane/compute_integration.py` | `bcaa5e8a0a05c571600c8fb715b78de9d87e9d48` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4569 → 4579 (+10) | 10 |
| P4-CP2 · ALLOCATION-ENTITY | `services/platform_control_plane/allocation_entity.py` | `f1b39fd51762ea9645a71a1a2605aa6252e8e7e8` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4579 → 4590 (+11) | 11 |
| P4-CP3 · TASK-ENTITY | `services/platform_control_plane/task_entity.py` | `8158de62e73a474eb8d31d758ac07c45a6a394e6` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4590 → 4599 (+9) | 9 |
| P4-CP4 · TASK-SCOPE-ENFORCEMENT | `services/platform_control_plane/task_scope_enforcement.py` | `ee70c4ab103440e1e151af6c2224d516feb52797` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4599 → 4609 (+10) | 10 |
| P4-CP5 · TASK-INVALIDATION | `services/platform_control_plane/task_invalidation.py` | `dcbd5d0777ef04a5b27a97ca28d291d66510bd33` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4609 → 4620 (+11) | 11 |
| P4-CP6 · SCHEDULER-ADMISSION | `services/platform_control_plane/scheduler_admission.py` | `09ed7d4f8a3225f2c57848ecb9c2cdde9f074bfb` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4620 → 4633 (+13) | 13 |
| P4-CP7 · METERING-LEDGER | `services/platform_control_plane/metering_ledger.py` | `6af22a3690c74ee9b71ab7276584f6c20c8b93ec` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4633 → 4646 (+13) | 13 |
| P4-CP8 · PREEMPTION-CONTRACT | `services/platform_control_plane/preemption_contract.py` | `be94bfee294b2862f82575836e5abb16b7ab2436` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4646 → 4657 (+11) | 11 |

### Phase P5 · App catalogue + enablement + wizard + provisioning report + theme (6/6 CPs SEALED · +86 ratchet · 4657 → 4743)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P5-CP1 · APP-ENTITY | `services/platform_control_plane/app_entity.py` | `ffae1f86650228a66a622fe55bfb3d68b6eafd57` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4657 → 4664 (+7) | 7 |
| P5-CP2 · APP-ENABLEMENT | `services/platform_control_plane/app_enablement.py` | `74577d83521b1b75ae52a31287043b2101291f61` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4664 → 4677 (+13) | 13 |
| P5-CP3 · APP-REVALIDATION | `services/platform_control_plane/app_revalidation.py` | `6819fd1100fcf89cd801622c412df3a742c92f34` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4677 → 4691 (+14) | 14 |
| P5-CP4 · WIZARD-STATE-MACHINE | `services/platform_control_plane/wizard_state_machine.py` | `7f34c3dc9bb77510d84a93192842011e2c2c6001` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4691 → 4708 (+17) | 17 |
| P5-CP5 · PROVISIONING-REPORT | `services/platform_control_plane/provisioning_report.py` | `68af117d4ee18e483c375c3af4b54bbe80713f0c` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4708 → 4725 (+17) | 17 |
| P5-CP6 · THEME-ENTITY | `services/platform_control_plane/theme_entity.py` | `51a39530b38e6f2a485235e714d9c32ec95db063` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4725 → 4743 (+18) | 18 |

### Phase P6 · Audit + cross-tenant suite + pilot register + offboarding + M9-SEAL (6/6 CPs SEALED · +66 ratchet · 4743 → 4809)

| CP | Module | Track-a SHA (Commit-A) | Master SHA (Commit-B) | Ratchet | Invariants |
|----|--------|-----------------------|-----------------------|---------|------------|
| P6-CP1 · AUDIT-EVENT-ENTITY | `services/platform_control_plane/audit_event.py` | `eede16f3da6eda54adcd5e5778668b5d1281772c` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4743 → 4754 (+11) | 11 |
| P6-CP2 · AUDIT-EVENT-TYPES | `services/platform_control_plane/audit_event_types.py` | `601297ab2b96733ec86cb22c7739c88e1344df2b` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4754 → 4766 (+12) | 12 |
| P6-CP3 · CROSS-TENANT-ACCESS-SUITE | `services/platform_control_plane/cross_tenant_access_suite.py` | `db1aafaad8f46a2100580741455771fa8150809a` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4766 → 4782 (+16) | 16 |
| P6-CP4 · PILOT-TENANT-REGISTER | `services/platform_control_plane/pilot_tenant_register.py` | `e436028251b0ae18919c163123b565e3000384ed` | `f6c4909b41a182671c1f276ab68e08f1a7fe702b` (BACK-COMPAT BATCH) | 4782 → 4795 (+13) | 13 |
| P6-CP5 · SANDBOX-OFFBOARDING | `services/platform_control_plane/sandbox_offboarding.py` | `2e82e4f` | `df6ed42445305b8c6ccb0274a5a08d2486ffa88c` | 4795 → 4809 (+14) | 14 |
| P6-CP6 · M9-SEAL | this document (`notes/M9_SEAL_20260917.md`) | N/A (state-only) | landing this-turn (Commit-B) | 4809 (unchanged) | N/A (wave-close) |

**Total M9 code CPs**: 36 · **Total invariants added in M9**: 373 · **Ratchet delta**: 4433 → **4809** (+376) · **Zero rollback**.

**Phase-total ratchet deltas**: P1 +35 · P2 +48 · P3 +53 · P4 +88 · P5 +86 · P6 +66 = **+376 total**.

---

## §7 · Consolidated CONTRACT-MODELED-vs-Real inventory

All 15 items from PLATFORM_LAYER_REQUIREMENTS_v0_2.md §8 have shape-frozen carriers at M9 close. Real-infra wiring is a bind-only change for every item.

| # | Item (§8 verbatim) | Depends on infra | Enabling M9 CP(s) | Bind-only wiring status |
|--:|---|---|---|---|
| 1 | Per-tenant Kubernetes namespace isolation (§6.4 M-Cp-3) | K8s cluster + namespace RBAC + NetworkPolicy | P4-CP6 SCHEDULER-ADMISSION | Refuses when execution-context ref lacks tenant-scoped namespace ref; K8s wiring is bind-only |
| 2 | Per-tenant GPU MIG partition / taints (§6.4 M-Cp-3) | Nvidia GPU + MIG + K8s device-plugin | P4-CP6 SCHEDULER-ADMISSION | Refuses when GPU partition ref lacks tenant scope; MIG config is bind-only |
| 3 | Network policy default-deny cross-namespace (§6.4 M-Cp-3) | K8s NetworkPolicy CNI | P4-CP6 SCHEDULER-ADMISSION | Refuses on missing network_policy_ref; NetworkPolicy object is bind-only |
| 4 | Reserved-never-preempted / burst-preemptible-within-SLA (§6.4 M-Cp-4) | Scheduler runtime | P4-CP8 PREEMPTION-CONTRACT | Refuses invalid transitions; live scheduler is bind-only |
| 5 | Live OIDC / SAML SSO per tenant (§7.2 M-A-6) | Real IdP | P2-CP4 SESSION-BINDER · P1-CP4 USER-ENTITY | Refuses on unsigned session claim; auth_method OPEN str; IdP wiring is bind-only |
| 6 | Data-plane agent cert issuance (§7.2, §4.5) | Real PKI + CA | P1-CP5 SERVICE-ACCOUNT-ENTITY | Frozen carrier + expiration refusal; real cert issuance is bind-only |
| 7 | Real 12-hour absolute / 1-hour idle session lifecycle (§7.2) | Session store | P2-CP4 SESSION-BINDER | Refusal on ttl > 12h / idle > 1h; real session store is bind-only |
| 8 | Break-glass owner notification via email/webhook (§7.8 M-A-8) | Email / webhook service | P2-CP5 BREAK-GLASS-SESSION | Refusal on missing notification refs at open+close; real webhook is bind-only |
| 9 | WCAG-AA contrast check for colour_primary (§8.3) | Colour-contrast library / real render | P5-CP6 THEME-ENTITY | Refusal on missing contrast_verify_ref; real WCAG measurement is bind-only |
| 10 | Envelope-encryption per-tenant secret store (§4.5) | KMS / HSM | P1-CP5 SERVICE-ACCOUNT-ENTITY | Refuses on missing envelope_key_ref; real KMS round-trip is bind-only |
| 11 | Audit log append-only durability (§7.7) | Append-only store | P6-CP1 AUDIT-EVENT + P6-CP2 AUDIT-EVENT-TYPES | Frozen carrier + append-only refusal + superset check; real store is bind-only |
| 12 | 30-day irreversible offboarding delete (§4.7) | Real storage + wall-clock scheduler | P1-CP6 TENANT-LIFECYCLE-FSM + **P6-CP5 SANDBOX-OFFBOARDING** | Terminal-state invariant + evidence-refs carrier + missing-evidence refusal; real storage/scheduler is bind-only |
| 13 | Cross-tenant access suite runs on every deploy (§4.3 M-H-6) | CI/CD pipeline | P6-CP3 CROSS-TENANT-ACCESS-SUITE | Aggregator runs in-CI locally; deploy-pipeline integration is bind-only |
| 14 | Real connector runtime enforcing mode (§5.3 M-C-3) | Data-plane connector agents | P3-CP3 CONNECTOR-MODE-LATTICE + P3-CP4 MODE-CHANGE-APPROVAL | Vocabulary + partial order + upgrade-refuses-without-approval; runtime wiring is bind-only |
| 15 | Storage namespaced by tenant_id at bucket/prefix/schema (§4.3 M-H-3) | Real object store + DB schema | P1-CP1 TENANT-CONTEXT-ENFORCEMENT | Refusal on storage_path_ref not tenant-prefixed; real bucket/prefix policy is bind-only |

**Additional CONTRACT-MODELED items enabled**:
- **Item 19** (Real pilot-tenant descriptor registry with governed capture flow) — enabled by P6-CP4 PILOT-TENANT-REGISTER (Row 209 verbatim).
- **Item 22** (Real preemption controller) — enabled by P4-CP8 PREEMPTION-CONTRACT.

---

## §8 · SEAL-CHAIN / RECEIPT PROVENANCE (mandatory disclosure per owner directive 2026-09-17T~09:15Z verbatim)

*Per owner ruling verbatim: "In the M9 rollup, include an explicit 'SEAL-CHAIN / RECEIPT PROVENANCE' section stating plainly: 20 CPs (P3-CP4→P6-CP3) had no historical per-CP double-green receipts on disk; substantiated by aggregate BASELINE_GUARD=1 green sweep ×2 at 4795 (byte-matched counts) plus verified track-a Commit-A (20/20) and monotonic ratchet (20/20); the 4 P6 CPs reconstructed post-hoc; R-5 adopted to prevent recurrence. Name it as a known provenance gap — do not gloss it."*

### 8.1 · The gap

Between 2026-09-17T~05:47Z (P3-CP3 Commit-C fixup) and 2026-09-17T~08:45Z (P6-CP4 Commit-A landing), a previous agent session landed 20 code CPs on `programme/track-a` — P3-CP4, P3-CP5, P4-CP1..CP8, P5-CP1..CP6, P6-CP1..CP4 — but did NOT:

1. Land Commit-B (master state) for any of them.
2. Land Commit-C fixup (master self-reference) for any of them.
3. Bank per-CP raw drill receipts (`<TS>_<cp>_RED.log` · `<TS>_<cp>_GREEN1.log` · `<TS>_<cp>_GREEN2.log`) for any of them.
4. Author a seal file for CP-P6-CP4 (P3-CP4..P6-CP3 had seal files on disk untracked; P6-CP4 had none at all).

### 8.2 · What DID substantiate the 20 CPs

- **Track-a Commit-A SHA**: 20/20 verified via `git log programme/track-a`. Every CP's code + tests + ratchet_history entry landed atomically.
- **Ratchet monotonic non-decreasing**: 20/20 verified in `tests/invariants/baseline_failures.json` `ratchet_history` indices 195-214. Full arc `4544 → 4557 → 4569 → 4579 → 4590 → 4599 → 4609 → 4620 → 4633 → 4646 → 4657 → 4664 → 4677 → 4691 → 4708 → 4725 → 4743 → 4754 → 4766 → 4782 → 4795`. Each delta matches the seal-file / commit-message declarations verbatim.
- **Aggregate post-hoc BASELINE_GUARD=1 sweep × 2** (2026-09-17T~08:55Z during the back-compat batch reconciliation): both sweeps returned `4795 passed, 1 skipped, 438 warnings` — byte-matched on counts. This proves the aggregate mechanism state is green at ratchet 4795 across all 20 CPs. Receipts at `phase0/drill_receipts/20260917T085545Z_backcompat_batch_p3cp4_to_p6cp4_GREEN1.log` + `20260917T085811Z_backcompat_batch_p3cp4_to_p6cp4_GREEN2.log`.

### 8.3 · What was NOT substantiated

- Per-CP RED drill receipts for the 20 CPs — no raw `<TS>_<cp>_RED.log` on disk showing right-reason failures before the module landed. This means the "tests-first" claim for each of these 20 CPs is not raw-log-substantiated — it is inferred from the correctness of the aggregate green state + the fact that the tests exist and pass.
- Per-CP GREEN1/GREEN2 byte-match receipts for the 20 CPs — no raw `<TS>_<cp>_GREEN[12].log` on disk showing per-CP byte-match.

### 8.4 · Reconstruction disposition

Per owner ruling path (c) SCOPED RECONSTRUCTION verbatim: reconstruct per-CP receipts for the 4 P6 back-compat CPs; leave P3/P4/P5 aggregate-only with honest disclosure; label all reconstructed receipts explicitly.

- **P3-CP4 · P3-CP5** (2 CPs) — NOT reconstructed. Aggregate-only substantiation. Historical gap disclosed.
- **P4-CP1 through P4-CP8** (8 CPs) — NOT reconstructed. Aggregate-only substantiation. Historical gap disclosed.
- **P5-CP1 through P5-CP6** (6 CPs) — NOT reconstructed. Aggregate-only substantiation. Historical gap disclosed.
- **P6-CP1 through P6-CP4** (4 CPs) — RECONSTRUCTED POST-HOC AT HEAD `e436028251b0ae18919c163123b565e3000384ed` · 2026-09-17. Receipts at `phase0/drill_receipts/20260917T09091[7]Z_p6_cp1_audit_event_*` · `20260917T09092[0]Z_p6_cp2_audit_event_types_*` · `20260917T09092[3]Z_p6_cp3_cross_tenant_access_suite_*` · `20260917T09092[6]Z_p6_cp4_pilot_tenant_register_*`. Each receipt file starts with a `# RECONSTRUCTED POST-HOC` header comment. RED counts match invariant counts exactly (11 / 12 / 16 / 13 = 52 total invariants across the 4 P6 CPs). GREEN1/GREEN2 byte-match on `N passed` per CP.

### 8.5 · Reconstructed-post-hoc labeling discipline

Per owner directive verbatim: *"HONEST LABELING is mandatory: any reconstructed receipt must be labeled 'RECONSTRUCTED POST-HOC AT HEAD <date>' — never presented as captured-at-seal-time."*

- The 12 reconstructed raw log files have `# RECONSTRUCTED POST-HOC AT HEAD e436028251b0ae18919c163123b565e3000384ed · 2026-09-17` in their header comments.
- The 4 P6 seal files (CP-P6-CP1..CP4) have a `Double-green (RECONSTRUCTED POST-HOC AT HEAD e436028251b0ae18919c163123b565e3000384ed · 2026-09-17):` line appended alongside (not replacing) the previous session's Double-green line.
- The CP-P6-CP4 seal note explicitly names its back-compat authorship in a dedicated section.

### 8.6 · R-5 adopted to prevent recurrence

Per DECISIONS.md §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17T~09:15Z: **R-5 (per-CP double-green raw-log requirement) is now MANDATORY**. Every new CP from this ruling forward must capture per-CP RED + DELTA_GUARD0 + GREEN1 + GREEN2 raw drill logs at seal time. Seal-file writer refuses to compose Double-green line unless both raw byte-match logs exist on disk. **CP-P6-CP5 was the FIRST CP sealed under R-5 enforcement** — all 5 raw drill receipts (RED, DELTA_GUARD0, DELTA_GUARD0_v2, GREEN1, GREEN2) captured at seal time and verified on disk pre-seal.

R-1..R-4 are additionally recorded as banked additive discipline at STANDING_ORDERS.md §7:
- R-1 · Master-parity check at CP boundary.
- R-2 · Seal-file `pending-C-fixup` counter.
- R-3 · Ratchet-history / git-log cross-check.
- R-4 · Session-handoff brief reconciliation.

The root-cause note at `notes/M9_MASTER_CHAIN_LAG_ROOT_CAUSE_20260917.md` records the 5 contributing factors that produced the 20-CP master-chain lag and the 5 additive discipline rules that close the class of defect.

---

## §9 · GPU utilization at M9 SEAL boundary

Per `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z + ~40 minutes of pytest campaign since:

- **Elapsed**: ~29.6 h · **Remaining**: ~42.4 h · **Wall-clock total**: 72 h
- **Hosts**: `akki-vm` + `akki-vm-ii` · both `sampler_alive+workload_alive`
- **Workload**: appliance benchmark suite (matmul bf16/fp16/fp32-tf32 · attention bf16 @ 2k/4k/8k · batch 1/4) — R-14 serving-engine admission precondition
- **In-perimeter**: True · **No estate data**: True · **Sampler interval**: 300 s · **Detachment**: setsid + nohup
- **Zero synthetic burn** · **No anomalies** · **No workload death** · **Both hosts reachable**

The GPU campaign is on cadence to 72h completion. No anomaly-interrupt-priority conditions raised during M9.

---

## §10 · Standing lines held across M9

- No push (all commits local · guardrail #5 of owner directive path (a) verbatim)
- No `testing_agent` (BANNED per user session directive)
- No refactor (only additive CPs; no existing code modified beyond seal-file line-appends and standing-orders §7 addition)
- No biometric material
- No enforcement hard-gate (all M9 refusal surfaces are preventive-charter · caller-invoked)
- No speculative shapes
- No closed enums in any P1-P6 module
- No data-plane imports in any P1-P6 module
- No domain tokens in any P1-P6 module source (21-token grep-negative)
- Local git history IS the record

---

## §11 · Receipts index

**Seal files** (36 code CPs + 1 wave-close):
- `phase0/output_verified_seals/cp_p1_cp1_tenant_context_enforcement.seal.txt` .. `cp_p1_cp6_tenant_lifecycle.seal.txt`
- `phase0/output_verified_seals/cp_p2_cp1_role_registry.seal.txt` .. `cp_p2_cp5_break_glass_session.seal.txt`
- `phase0/output_verified_seals/cp_p3_cp1_estate_entity.seal.txt` .. `cp_p3_cp5_connection_test.seal.txt`
- `phase0/output_verified_seals/cp_p4_cp1_compute_integration.seal.txt` .. `cp_p4_cp8_preemption_contract.seal.txt`
- `phase0/output_verified_seals/cp_p5_cp1_app_entity.seal.txt` .. `cp_p5_cp6_theme_entity.seal.txt`
- `phase0/output_verified_seals/cp_p6_cp1_audit_event.seal.txt` .. `cp_p6_cp5_sandbox_offboarding.seal.txt`
- `notes/M9_SEAL_20260917.md` (this document · CP-P6-CP6 wave-close)

**Seal notes**:
- `notes/P1_CP1_TENANT_CONTEXT_SEAL_20260917.md` .. `P1_CP6_TENANT_LIFECYCLE_SEAL_20260917.md`
- `notes/P2_CP1_ROLE_REGISTRY_SEAL_20260917.md` .. `P2_CP5_BREAK_GLASS_SESSION_SEAL_20260917.md`
- `notes/P3_CP1_ESTATE_ENTITY_SEAL_20260917.md` .. `P3_CP3_CONNECTOR_MODE_LATTICE_SEAL_20260917.md`
- `notes/P6_CP4_PILOT_TENANT_REGISTER_SEAL_20260917.md` (back-compat authored)
- `notes/P6_CP5_SANDBOX_OFFBOARDING_SEAL_20260917.md` (full R-5 compliant)
- **Note**: seal notes for P3-CP4, P3-CP5, P4-CP1..CP8, P5-CP1..CP6, P6-CP1..CP3 were NOT authored by the previous session and are not being retro-authored (aggregate reconciliation memo covers them collectively).

**Auxiliary notes**:
- `notes/M9_BACKCOMPAT_RECONCILIATION_20260917.md` — 20-CP back-compat reconciliation memo
- `notes/M9_MASTER_CHAIN_LAG_ROOT_CAUSE_20260917.md` — root-cause note + R-1..R-5 proposal

**Drill receipts** (present on disk under `phase0/drill_receipts/`):
- Aggregate back-compat: `20260917T085545Z_backcompat_batch_p3cp4_to_p6cp4_GREEN1.log` + `20260917T085811Z_backcompat_batch_p3cp4_to_p6cp4_GREEN2.log`
- P6-CP1..CP4 reconstructed post-hoc: 12 files at `20260917T09091[7]Z_p6_cp1_*` · `20260917T09092[0]Z_p6_cp2_*` · `20260917T09092[3]Z_p6_cp3_*` · `20260917T09092[6]Z_p6_cp4_*`
- P6-CP5 full R-5: `20260917T091401Z_p6_cp5_*_RED.log` · `20260917T091806Z_p6_cp5_*_DELTA_GUARD0_v2.log` · `20260917T092056Z_p6_cp5_*_GREEN1.log` · `20260917T092325Z_p6_cp5_*_GREEN2.log`

**STATE**:
- `STATE/DECISIONS.md` — 3 new entries for M9 close (§3.3 BACK-COMPAT BATCH · §3.3 SEAL-CHAIN INTEGRITY RULINGS · CP-P6-CP5 SEAL)
- `STATE/NEXT.md` — 3 new current-position markers
- `STATE/STANDING_ORDERS.md` — new §7 (R-1..R-5)

---

## §12 · Wave-honest limits at M9 SEAL

1. **Per-CP receipt provenance gap for 16 CPs (P3-CP4 · P3-CP5 · P4-CP1..CP8 · P5-CP1..CP6)** — aggregate-only substantiation. Owner ruling accepted this disposition with explicit disclosure. Post-M9 P3/P4/P5 back-compat receipt reconstruction is available if ever required (mechanical process · ~64 minutes at ~4 min per CP).
2. **CONTRACT-MODELED items 1-15 are shape-frozen but not runtime-bound.** Real K8s cluster · MIG-enabled GPUs · Real IdP · Real PKI · Real KMS · Real session store · Real object store · Real webhook · Real WCAG-AA library are all outside this pod and outside M9's scope. Post-M9 milestone can walk each item as real infra becomes available.
3. **The M9 rollup does NOT propose sequencing / phases / build order for post-M9 work** — per standing owner rule ("Do not propose sequencing, phases, or build order").
4. **The GPU campaign is still open** (42.4h remaining · 29.6h elapsed). This M9 SEAL landing does not close the GPU campaign; utilization interleave check-ins continue on cadence per hold-pattern discipline.
5. **The R-5 discipline was ratified mid-wave, not from wave start.** All CPs before the 2026-09-17T~09:15Z ruling are back-compat labeled or aggregate-substantiated; only CP-P6-CP5 was sealed with full R-5 enforcement at seal time.

---

**M9 · Akki OS Pilot Platform Layer · COMPLETE · 2026-09-17T~09:30Z · ratchet 4809 · 36 code CPs + 1 wave-close · zero rollback.**

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
