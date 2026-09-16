READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-M7-W1-POST-1 · Resource Registry · Grounding brief · 2026-09-16T~05:20Z

**Wave:** W-M7-W1-POST-1 (M7 W1-family follow-up · registry surface landing).
**CP:** CP-M7-W1-POST-1 · Resource Registry.
**Type:** MECHANISM BUILD (tests-first RED → GREEN 1 → GREEN 2 → seal → §3.3 3-commit).
**Predecessor seal:** W-M7-W1-VERIFICATION Path α clean · master `997d8398`.
**Concurrent:** W-M7-UTILIZATION-72H · LIVE from 2026-09-16T03:41:28Z · check-in at CP-open + CP-seal.

---

## §A · Owner authorization verbatim

**2026-09-16T~05:10Z (via user relay · this-shift ruling that overrides prior default):**

> "Ruling on §3/§4 — the default is OVERRIDDEN; you have more authority than you're using. The contract-shape question is ALREADY RULED by owner precedent: the 2026-09-13 verbatim correction ('job_kind must stay CASE-AGNOSTIC … Do NOT lock a closed 5-value enum into the platform') is the governing shape ruling for ALL W1-family platform kernels. Applying existing owner law is not speculation. Execute in this order:
>
> 2. **(a) CP-M7-W1-POST-1 · Resource Registry** — land services/resource_registry/* in case-agnostic-simplified shape per the same precedent (registration + enumeration + status surface; no closed workload enums; deterministic; tests-first). SCOPE BOUNDARY: registry surface ONLY — do NOT wire the §3.2 clause-5 cross-service hard-gate (refusing dispatch of unregistered resources); that enforcement semantics is a genuine owner ruling and stays on the P2 desk. Registry-without-gate is useful and shape-safe."

**2026-09-13 (governing shape precedent · W1 CP breakdown approval):**

> "CORRECTION — job_kind must stay CASE-AGNOSTIC ... Do NOT lock a closed 5-value audio-harvest enum into the platform JobManifest at CP1 — that leaks the audio case into generic platform code. Instead make job_kind reference an OPEN, registry-backed kind: a capability/job-kind REGISTRY that jobs register into."

## §B · Verbatim canon anchors

**ROADMAP §A.1 Resource Plane (aspirational shape · pre-correction):**

```python
class ComputeResource(BaseModel):
    resource_id: str                                  # e.g. "host:akki-vm:gpu:0"
    resource_class: Literal["gpu", "cpu", "tpu", "cluster"]   # ← CLOSED ENUM → CORRECTED
    capability_tags: List[str]                        # e.g. ["nvidia:h200","vram:80gb","cuda:12.4"]
    max_concurrent_workers: int
    ssh_seam_ref: Optional[str] = None                # governed access channel
    cost_class: Literal["billed_hourly", "leased_flat", "spot"]   # ← CLOSED ENUM → CORRECTED
    registered_at: str                                # ISO-8601 UTC
```

**Under the 2026-09-13 case-agnostic correction, the two `Literal[...]` closed enums (`resource_class`, `cost_class`) are FORBIDDEN — they would leak specific-case value spaces into the platform kernel.** They are the direct analog of "closed 5-value audio-harvest enum" the correction bans. The case-agnostic W1-family pattern (see `kind_registry.py`) is: open string field, registry-backed elsewhere or free-form; the platform kernel does not adopt any closed value space.

## §C · Wave scope · MECHANISM BUILD (this shift)

**Deliverable:** `services/resource_registry/*` — case-agnostic minimal registry surface.

### C.1 · Files landing

- `backend/services/resource_registry/__init__.py` — module surface (imports + __all__).
- `backend/services/resource_registry/registry.py` — canonical implementation.
- `backend/tests/invariants/test_wm7_w1_post_1_resource_registry.py` — 22-invariant tests-first freeze.

### C.2 · Public surface (case-agnostic · minimal · deterministic)

```python
@dataclass(frozen=True)
class ComputeResource:
    """A registered compute resource. Case-agnostic minimal shape.

    resource_id: non-empty string, globally unique in the registry.
    resource_class: non-empty OPEN string (case-agnostic; no closed enum
                    per 2026-09-13 owner correction). Downstream jobs
                    interpret; the platform kernel does not.
    capability_tags: sorted tuple of non-empty strings. Sorted at
                     construct time for deterministic snapshots.
    registered_at_utc: ISO-8601 with Z suffix.
    """
    resource_id: str
    resource_class: str
    capability_tags: tuple[str, ...]
    registered_at_utc: str


class ResourceRegistryInvalid(ValueError):
    """Raised at ComputeResource construct time on shape refusal."""


class ResourceNotRegistered(KeyError):
    """Raised by get_resource() when the id has no registration."""


def register_resource(resource: ComputeResource) -> None:
    """Register a resource. Idempotent for same resource_id + payload.
    RESOURCE_ID collision with a DIFFERENT payload raises
    ResourceRegistryInvalid (mutation refused — a change is a new
    resource, mirrors §10.2 verbatim discipline)."""


def is_registered(resource_id: str) -> bool:
    """Return True iff a resource with resource_id is registered."""


def list_resources() -> tuple[ComputeResource, ...]:
    """Return an immutable snapshot sorted by resource_id."""


def select_by_capability(required_tags: set[str]) -> tuple[ComputeResource, ...]:
    """Return resources whose capability_tags is a superset of required_tags.
    Empty required_tags returns all resources. Sorted by resource_id."""


def get_resource(resource_id: str) -> ComputeResource:
    """Return the registered resource. Raises ResourceNotRegistered on miss."""


def _reset_registry_for_tests() -> None:
    """Wipe the registry. Test-only determinism helper (leading _ signals
    non-stable public API)."""
```

### C.3 · Scope boundary (per owner ruling verbatim)

**IN scope this CP:**
- Registration surface (`register_resource`).
- Enumeration surface (`list_resources`, `is_registered`, `get_resource`).
- Selection surface (`select_by_capability`).
- Determinism helpers (`_reset_registry_for_tests`).

**OUT of scope this CP (owner-desk P2 · SO §3.2 clause-5 hard-gate):**
- Cross-service enforcement wiring (refusing dispatch of unregistered resources).
- Any hook into `services/training_runner/*`, `services/audio_poc/*`, or other dispatch surfaces.
- Any modification to `services/work_supervisor/*` (composes via read-only import; no wave-scope refactor).

The scope boundary matches the owner's verbatim: *"registration + enumeration + status surface; no closed workload enums; deterministic; ... Registry-without-gate is useful and shape-safe."*

### C.4 · Invariants landing (22)

The `test_wm7_w1_post_1_resource_registry.py` file freezes:

1. `test_resource_registry_module_importable` — module loads without error.
2. `test_resource_registry_exports_expected_surface` — `__all__` matches expected set.
3. `test_compute_resource_is_frozen_dataclass` — frozen (mutation raises FrozenInstanceError).
4. `test_compute_resource_refuses_empty_resource_id` — construct raises `ResourceRegistryInvalid`.
5. `test_compute_resource_refuses_empty_resource_class` — case-agnostic non-emptiness.
6. `test_compute_resource_refuses_non_iso_z_timestamp` — ISO-8601 Z suffix required.
7. `test_compute_resource_sorts_capability_tags_deterministic` — construct-time sort.
8. `test_compute_resource_capability_tags_is_tuple_not_list` — immutable snapshot.
9. `test_compute_resource_refuses_empty_capability_tag` — non-empty strings inside.
10. `test_compute_resource_open_resource_class_no_closed_enum` — case-agnostic doctrine explicit-verify.
11. `test_register_resource_stores_resource` — `is_registered` True after register.
12. `test_register_resource_idempotent_same_payload` — no-op on same id + same payload.
13. `test_register_resource_refuses_mutation_different_payload` — id-with-mismatched-payload raises `ResourceRegistryInvalid`.
14. `test_register_resource_requires_compute_resource_type` — dict rejected (strict typing).
15. `test_is_registered_returns_false_for_unknown_id` — no false positives.
16. `test_list_resources_returns_deterministic_sorted_snapshot` — sorted by resource_id.
17. `test_list_resources_returns_tuple_immutable` — cannot mutate registry via return.
18. `test_select_by_capability_returns_superset_matches` — set-superset semantics.
19. `test_select_by_capability_empty_required_returns_all` — empty selects everything.
20. `test_select_by_capability_returns_deterministic_sorted` — same sort discipline.
21. `test_get_resource_returns_registered_resource` — happy path.
22. `test_get_resource_raises_resource_not_registered_on_miss` — closed-enum-free exception; subclass of KeyError.
23. `test_reset_registry_for_tests_wipes_state` — determinism helper works.
24. `test_registry_starts_empty_no_platform_seed` — case-agnostic doctrine explicit-verify (no `platform.generic`-shaped seed for resources; resources register at their case wave).
25. `test_registry_no_terminator_names_on_public_surface` — zero-influence discipline mirror (no `kill_`, `terminate_`, `dispatch_`, `refuse_dispatch_` names in the public surface · confirms scope boundary).
26. `test_registry_does_not_import_dispatch_surfaces` — grep-based negative: `registry.py` does NOT import `services.training_runner`, `services.audio_poc`, `services.work_supervisor.supervisor`, or any other dispatch surface. Confirms scope boundary from-disk.

Actual count target: **26 invariants**. Ratchet delta: **+26**. Ratchet floor 4358 → 4384.

## §D · Wave-honest limits

**D.1 · Registry-only surface.** No cross-service binding enforcement (owner-desk P2). A dispatch surface CAN still fire commissioned work against a resource_id that was never registered — the registry does not refuse. That enforcement wiring waits on the §3.2 clause-5 hard-gate ruling.

**D.2 · No status surface.** The primitive tracks registrations, not liveness. Whether a registered resource is currently reachable/available is a `runtime_supervisor.output_verification_watchdog`-style read, not a resource-registry concern. The composition is by-design orthogonal.

**D.3 · No max_concurrent_workers / cost_class / ssh_seam_ref fields.** These four fields from the aspirational §A.1 shape are omitted at CP1: `max_concurrent_workers` is a job-scheduling concern (belongs on `WorkerLane`/`CommissionSpec` in the mounting job, not the platform-kernel resource) · `cost_class` is a closed enum (banned by 2026-09-13 correction · would need registry-backed policy elsewhere) · `ssh_seam_ref` is a source-plane binding (already available via `services/source_plane/*` and `AKKI_VM_HOST` env). Adding them later without shape-breaking change is possible (frozen dataclass with dataclasses.replace-style extension); this CP ships the minimum kernel.

**D.4 · Process-scope registry.** Like `kind_registry`, the resource registry is a process-scope in-memory registry. Durable on-disk audit trail of registrations is a later refinement mirror-precedented at `kind_registry.py` wave-honest limit E-4.

## §E · Concrete owner-facing decision surfaces

None at grounding-brief authoring. Every design decision is either:
- Directly ruled by 2026-09-16T~05:10Z (scope boundary: registry-only) or
- Directly ruled by 2026-09-13 (case-agnostic doctrine: no closed enums) or
- Wave-honest limit D.1-D.4 documented above.

If tests-first RED surfaces any ambiguity, HALT-to-owner per SO §3.

## §F · Commit protocol (§3.3 · 3-commit)

- **Commit A · code · `programme/track-a` (backend repo):** RED drill receipt + mechanism (registry.py + __init__.py) + test invariant file. `[CP-M7-W1-POST-1 · Resource Registry · services/resource_registry/* · case-agnostic minimal · ratchet 4358 -> 4384 (+26) (§3.3 · master SHA to land in commit C-fixup)]`
- **Commit B · state · `master` (state repo):** grounding brief (this file) + phase0/drill_receipts/ RED + double-green receipts + phase0/output_verified_seals/w_m7_w1_post_1_resource_registry.seal.txt with `Track-a HEAD at seal: <A SHA> · Master HEAD: TBD` + STATE/NEXT.md pin update + STATE/DECISIONS.md CP entry + GPU util check-in artefacts. Ratchet delta banked. `[CP-M7-W1-POST-1 · state + seal + probe (master SHA TBD)]`
- **Commit C · fixup · `master`:** replace `TBD` in seal file + DECISIONS.md CP entry + NEXT.md pin with the Commit-B master SHA landed. `[CP-M7-W1-POST-1 · master SHA landed in seal]`

## §G · GPU utilization check-in interleave

- **CP-open** — fired at this-turn (elapsed ~1.6h · sample state).
- **CP-seal (Commit B)** — fired at seal write.
- **CP fixup (Commit C)** — optional; fired only if wall-clock delta > 30 min.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
