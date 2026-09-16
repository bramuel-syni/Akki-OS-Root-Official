READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-M7-W1-POST-2 · Capability Registry · Grounding brief · 2026-09-16T~06:00Z · REVISED-TO-VERIFICATION-WALK

**Wave:** W-M7-W1-POST-2 (M7 W1-family follow-up).
**CP:** CP-M7-W1-POST-2 · Capability Registry.
**Type revised (from-disk discovery):** VERIFICATION WALK (not mechanism build) — the case-agnostic capability registry ALREADY EXISTS at `services/capability_registry.py`, landed 2026-09-13T06:59:30Z by W1b close commit `53645935` (ratchet 3392 → 3492 · +100).
**Predecessor seal:** CP-M7-W1-POST-1 · Resource Registry SEALED · master `358ea3d4` (Commit-C fixup).
**Concurrent:** W-M7-UTILIZATION-72H · LIVE.

---

## §A · Owner authorization verbatim (2026-09-16T~05:10Z)

> "3. **(b) CP-M7-W1-POST-2 · Capability Registry** — same pattern: generalise services/layer_b/factory.py into services/capability_registry/* case-agnostically, registry surface only, no enforcement gate. Compose with (not modify) the existing factory per no-refactor discipline; it can delegate."

## §B · From-disk discovery (2026-09-16T~06:00Z · this-shift)

Attempting to author `services/capability_registry/*` as a new package surfaced a pre-existing file `services/capability_registry.py` (112 lines · 3709 bytes) with a case-agnostic capability-registry surface that:
- Was landed **2026-09-13T06:59:30Z** by commit `53645935` in wave close *"W1b · Platform Primitives wave close · RetentionPolicy + SourceConnector Protocol + Synology FileStation (interface only) + capability_registry + generic AttributeStreamBundle_v0 + L2/L4 contract shells · ratchet 3392 -> 3492"*.
- Carries the exact case-agnostic doctrine the owner ruled for (module docstring line 15-17 verbatim): *"Case-agnostic: this module carries NO category-specific tokens. It merely stores (category, name) -> import_path mappings and resolves them lazily."*
- Composes-not-modifies with `services/layer_b/factory.py` per its own compose-freeze test (`test_layer_b_factory_registries_re_expressible_in_capability_registry` in `tests/invariants/test_w1b_cp4_capability_registry.py` line 22-27 verbatim: *"Compose-freeze test: `layer_b.factory` provider dicts can be re-registered into the generic registry and retrieved by (category, name) — proves the generic registry is a strict superset of the layer_b.factory pattern WITHOUT refactoring layer_b.factory (thin-kernel)."*).
- Is frozen by 15 W1b CP4 invariants at `tests/invariants/test_w1b_cp4_capability_registry.py` (all part of the ratchet 4358 baseline).

**Wave-honest gap in my W1 verification (this shift · 2026-09-16T~04:15Z close):** the M7 W1 verification receipt (`phase0/m7_w1_verification/verification_receipt_20260916.json`) covered ONLY the SO §3.2 `runtime_supervisor` primitive from commit `fe01e5e` (W1 close 2026-09-13T06:33Z). It did NOT enumerate the subsequent **W1b** platform-primitives close 26 minutes later (2026-09-13T06:59Z · commit `53645935`) which shipped the capability_registry (case-agnostic + compose-not-modify with layer_b.factory), the RetentionPolicy primitive, the SourceConnector Protocol, the Synology FileStation interface, the generic AttributeStreamBundle_v0, and L2/L4 contract shells. This is a **W1-verification-scope hole** — surfaced as a first-class finding in this POST-2 walk.

**Consequence for the owner's ruling:** the owner's ordered step (b) instructs "*generalise services/layer_b/factory.py into services/capability_registry/* case-agnostically*". Under Audio-Plane §1.2 verbatim (*"Anything ... that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build"*), authoring a NEW `services/capability_registry/` package (as I initially proposed) alongside the pre-existing `services/capability_registry.py` module would be rule proliferation. The correct move is **verification walk on the pre-existing W1b module** — analog of W0/W1 verification walks this shift. The owner's ruling INTENT ("case-agnostic capability registry landed with compose-not-modify posture") is ALREADY SATISFIED by W1b close 2026-09-13T06:59Z; the CP-M7-W1-POST-2 walk becomes a from-disk parse-not-paraphrase verification that the W1b implementation matches the owner's INTENT verbatim, plus a ROADMAP §A.12 reconciliation update to reflect the W1b close.

## §C · Wave scope · VERIFICATION WALK (this shift · REVISED)

**Deliverable:** verification receipt + reconciliation update + close note. **Zero code lands.** No track-a commit. Single master commit banks the state entirety (analog of W0/W1 verifications).

### C.1 · Verification checks (six · analog of W0/W1 shape)

- **C.1** Primitive surface: `services/capability_registry.py` exports `register_capability`, `get_capability`, `list_categories`, `list_capabilities_in`, `CapabilityNotRegistered`, `_reset_capabilities_for_tests` (per `__all__`).
- **C.2** Invariant tests: `tests/invariants/test_w1b_cp4_capability_registry.py` — 15 tests, all pass under file-scoped pytest. Confirms shape frozen since W1b close.
- **C.3** Case-agnostic doctrine explicit-verify: module source contains NO domain tokens (asr/diarization/vision/audio/etc. per W1b invariant `test_capability_registry_source_has_no_domain_tokens`). Enforced from-disk.
- **C.4** Module unchanged since W1b close (from-disk `git log` last-touched vs commit `53645935`): the W1b module has not drifted.
- **C.5** Compose-not-modify verified: W1b `test_layer_b_factory_registries_re_expressible_in_capability_registry` freezes the compose-freeze property (generic registry is strict superset of layer_b.factory pattern WITHOUT refactoring the factory).
- **C.6** Registry-only surface (no cross-service hard-gate): W1b surface exposes `register_capability`/`get_capability`/`list_categories`/`list_capabilities_in` only — no `refuse_pipeline_unregistered_capability` / `hard_gate` / enforcement operations. Matches the owner's scope boundary verbatim ("*registry surface only, no enforcement gate*").

**Two-path decision (identical shape to W0/W1 walks):**

- **Path α · Clean verification** — Every point C.1-C.6 confirmed clean. Close as zero-delta verification seal. Ratchet unchanged (4384 from POST-1).
- **Path β · Drift** — Any check fails → the W1b module has been silently weakened. Author `CP-M7-W1-POST-2-DRIFT-<n>` tests-first RED → mechanism.

## §D · Wave-honest limits

**D.1 · W1 verification scope hole (this-shift surface).** The M7 W1 verification receipt (`phase0/m7_w1_verification/verification_receipt_20260916.json`) covered only the W1 close (commit `fe01e5e`), missing the W1b close (commit `53645935` · 26 minutes later). W1b deliverables (capability_registry + RetentionPolicy + SourceConnector Protocol + Synology FileStation interface + generic AttributeStreamBundle_v0 + L2/L4 contract shells) went unverified this shift. This POST-2 close will bank the W1b capability_registry verification; **the OTHER W1b deliverables remain unverified as a new wave-honest limit** (candidate CP-M7-W1-POST-3-VERIFICATION for RetentionPolicy + SourceConnector Protocol + Synology FileStation + AttributeStreamBundle_v0 + L2/L4 shells).

**D.2 · ROADMAP §A.12 W1 reconciliation refinement.** The reconciliation banked at master `221573f1` this shift correctly noted "NOT DELIVERED at W1 close: `services/capability_registry/*`" but MISSED the W1b close 26 minutes later that DID deliver it as `services/capability_registry.py` (file, not package). This POST-2 close authors a refinement bumping the W1b close date + commit into the reconciliation record.

**D.3 · POST-1 vs POST-2 asymmetry.** POST-1 (Resource Registry) landed as a genuine mechanism build (26 new invariants · ratchet +26) because no pre-existing `services/resource_registry/*` existed. POST-2 (Capability Registry) landed as a zero-delta verification walk because W1b already shipped it. Both satisfy the owner's ruling INTENT (case-agnostic platform primitive landed); the delivery path differs by from-disk state.

**D.4 · Path-file vs path-package convention.** `services/capability_registry.py` is a single-file module. The owner's ruling wrote `services/capability_registry/*` (package convention). Python does not distinguish semantically at the import site (`import services.capability_registry` works either way). The module shape (single file) is a wave-honest choice at W1b close and is not modified this CP.

## §E · Concrete owner-facing decision surfaces

None at grounding-brief authoring. Every question is either owner-ruled precedent or wave-honest limit above. If C.1-C.6 clean, autonomous close.

## §F · Commit protocol (§3.3 · single-master-commit for zero-code verification walk)

Analog of W0/W1 verification walks: no track-a code change → no Commit A → single Commit B on master banks state entirety (this grounding brief + verification receipt + close note + NEXT.md pin + DECISIONS.md entry + ROADMAP §A.12 refinement + GPU util check-in artefacts). No Commit-C fixup because no seal file references a master SHA.

## §G · GPU utilization check-in interleave

- **CP-open** — this-turn.
- **CP-seal (Commit B)** — at seal write.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
