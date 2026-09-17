READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P1-CP1 · M9 · Platform-layer tenant-context enforcement · seal note · 2026-09-17T~04:00Z

**Milestone:** M9 · Akki OS pilot platform layer (multi-tenant control plane).
**Phase:** P1 · Foundation — control-plane data model + tenancy core + isolation invariants.
**CP:** P1-CP1 · Tenant-context enforcement (foundation isolation invariant).
**Track-a HEAD at seal:** `e697ba63a9f5aa16065552109d2a86b6e17332c2` (Commit-A landed 2026-09-17T~04:00Z).
**Master HEAD at seal:** `1a2c3faa042d31d73c3376babb63221aa719fc8d` (Commit-B landed 2026-09-17T~04:05Z · this Commit-C fixup banks the SHA).
**Ratchet:** 4433 → **4440** (+7 monotonic-up).

---

## §1 · Anchor

**Ingest doc:** `notes/PLATFORM_LAYER_REQUIREMENTS_v0_2.md` (banked this-shift from customer-assets URL for **Akki OS Pilot Platform Reference v0.2** dated 17 September 2026 · Status: reference for development).

**Verbatim §3.1 + §4.3:**

> *"§3.1: A tenant maps one-to-one to a legal entity. All resources are owned by exactly one tenant and carry its tenant_id."*
>
> *"§4.3: The API gateway resolves tenant_id from the authenticated session and injects it into every request. Clients cannot supply it. Every data-plane service validates tenant_id on every call against its own provisioned identity and rejects mismatches."*

Landed as `TENANT_CONTEXT_ENFORCEMENT_ANCHOR` constant in the module source; asserted present in invariant #7.

---

## §2 · Module fabric

**Home:** `services/platform_control_plane/tenant_context.py` (POST-2 **new-home** selected — no peer existed prior to this-turn; naming mirrors source doc §4.1 *"Control plane"* language).

**Exports (`__all__`, 8 names):**
- `TENANT_CONTEXT_ENFORCEMENT_ANCHOR` — verbatim anchor.
- `TenantContext` — frozen dataclass · 1 carrier · `tenant_id: str` (OPEN).
- `TenantOwnedResourceRef` — frozen dataclass · 3 carriers · `tenant_id: str · resource_type: str · resource_id: str` (all OPEN).
- `assess_tenant_context_drift` — pure function · returns sorted tuple of drift resources · deterministic ordering by (tenant_id, resource_type, resource_id).
- `assert_tenant_context_valid` — preventive-charter refusal wrapper · caller-invoked only · returns `None` on admit · COUNTS-only refusal messages.
- `TenantContextRefused` — refusal root.
- `ClientSuppliedTenantIdRefused` — subclass · fires on any non-None `client_supplied_tenant_id`.
- `CrossTenantAccessRefused` — subclass · fires on any drift or missing `tenant_id`.

**Refusal order (fail fast on the more fundamental violation):**
1. If `client_supplied_tenant_id is not None` → `ClientSuppliedTenantIdRefused`.
2. Else if drift tuple non-empty → `CrossTenantAccessRefused`.

**Coarse rule by design.** String equality on `tenant_id`; empty string treated as missing. This is the M9 analog of the CP-M8-CSD-1 set-membership rule (a wave-honest coarse mechanism · sufficient for the foundation isolation invariant · leaves room for a downstream CP to tighten).

---

## §3 · Invariants (7)

Frozen at `tests/invariants/test_p1_cp1_tenant_context_enforcement.py`.

1. `test_module_fabric_present_and_all_exports_match` — 8-name `__all__` exact-set match + attribute presence.
2. `test_tenant_context_shape_frozen_1_carrier_exact_order` — `TenantContext` is `@dataclass(frozen=True)` · exactly 1 field · `tenant_id: str`.
3. `test_tenant_owned_resource_ref_shape_frozen_3_carrier_exact_order` — `TenantOwnedResourceRef` frozen · exactly 3 fields · exact order + all `str`.
4. `test_assess_tenant_context_drift_returns_sorted_tuple_of_drifts` — pure · deterministic sort · empty inputs return `()` · all-owned returns `()`.
5. `test_assert_tenant_context_valid_refuses_on_client_supplied_and_drift` — 4 refusal cases (client-supplied non-None with matching-tenant / client-supplied empty string / drift on cross-tenant / drift on missing tenant_id) + refusal-class hierarchy verified.
6. `test_assert_tenant_context_valid_permits_when_all_owned_and_no_client_supplied` — returns `None` on admit · empty resources also admit.
7. `test_verbatim_anchor_case_agnostic_zero_data_plane_imports` — anchor contains §3.1 + §4.3 keys · 21-token grep-negative · zero imports of `services.audio_plane_v1 / services.release_gate / services.governance_plane / services.audio_poc / services.training_runner / services.ssh_seam / services.resource_registry`.

**Standing-line proof:** no biometric material · no enforcement hard-gate (preventive-charter · caller invokes) · synthetic fixtures · no speculative shapes · upgrade path to hard-gate preserved by construction (a future CP can wrap `assert_tenant_context_valid` in a global request-time interceptor without refactoring this module).

---

## §4 · Double-green byte-match under `BASELINE_GUARD=1`

- **GREEN 1 (pre-M8-SEAL-priority-reorder, before stash):** `4440 passed, 1 skipped, 438 warnings in 190.71s` — full-suite green with new invariants + ratchet bump.
- **GREEN 2 (post-M8-SEAL-priority-reorder, post-stash-pop + rebuild):** `4440 passed, 1 skipped, 438 warnings in 124.10s` — full-suite green under `BASELINE_GUARD=1` after M8 SEAL closed.
- **Byte-match:** invariant test source unchanged across stash-and-restore cycle · module source unchanged · baseline entry unchanged. The stash-and-restore was a state-management manoeuvre, not a mechanism edit.

---

## §5 · Ratchet 4433 → 4440 (+7) monotonic-up

- `counts_at_baseline.passed`: 4433 → **4440**.
- `passed_floor`: 4433 → **4440**.
- `ratchet_history` appended at `20260917T040000Z` with full CP note.
- **Monotonic non-decreasing** across 182 total ratchet history entries.

---

## §6 · §3.3 3-commit protocol

- **Commit A** `e697ba63a9f5aa16065552109d2a86b6e17332c2` (track-a `programme/track-a`) ✅ landed 2026-09-17T~04:00Z — code + tests + ratchet bump.
- **Commit B** this-turn (`master`) — this seal note + DECISIONS entry + NEXT pin + GPU util check-in.
- **Commit C** this-turn (`master`) — fixup · replaces `TBD` in this seal note + DECISIONS + NEXT with actual Master HEAD SHA.

---

## §7 · Effects banked

1. **M9 P1 foundation** landed. Every downstream M9 CP (P1-CP2 through P6-CP6, ~34 more) composes on top of `assert_tenant_context_valid` at the API-gateway ingest boundary.
2. **Post-M8-SEAL priority-reorder discharged** per owner directive verbatim 2026-09-17T~03:00Z (*"THEN resume the P1 platform-layer work"*).
3. **Standing lines held** throughout · case-agnostic doctrine intact · zero SEC-class incidents.
4. **CONTRACT-MODELED items §8 of PLATFORM_LAYER_REQUIREMENTS_v0_2.md**: item 15 (storage namespaced by tenant_id at bucket/prefix/schema) is directly enabled by this refusal wrapper — real-infra wiring becomes a bind-only change (no refactor).
5. **Next slice**: **CP-P1-CP2 · TENANT-ENTITY** — frozen carrier for the 7-field `tenant` record with lifecycle enum values as OPEN str refs (per PLATFORM_LAYER_REQUIREMENTS_v0_2.md §7 CP breakdown proposal).

---

## §8 · Wave-honest limits

- **W.1** The refusal wrapper is preventive-charter · caller-invoked. Real-infra API-gateway wiring is a downstream CP (a request-time interceptor that wraps every inbound request with `assert_tenant_context_valid(context=session_ctx, requested_resources=deserialized_resource_refs, client_supplied_tenant_id=payload.get("tenant_id"))`). Not built this-turn.
- **W.2** The refusal messages are COUNTS-only (never `tenant_id` / `resource_id` values). This intentionally omits per-refusal diagnostic detail — the pilot's audit log (P6-CP1 · `audit_event.py`, future CP) will carry the identifying refs.
- **W.3** Empty-string `tenant_id` is treated as missing (refused). A future CP may add a stricter shape check (e.g. UUID or opaque-token regex) — this-CP keeps it OPEN str per case-agnostic doctrine.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
