"""services.resource_registry — CP-M7-W1-POST-1 · Resource Registry kernel.

Owner ruling verbatim (2026-09-16T~05:10Z · this-shift ruling · via user
relay banked in STATE/DECISIONS.md same date):

    "CP-M7-W1-POST-1 · Resource Registry — land services/resource_registry/*
    in case-agnostic-simplified shape per the same precedent (registration +
    enumeration + status surface; no closed workload enums; deterministic;
    tests-first). SCOPE BOUNDARY: registry surface ONLY — do NOT wire the
    §3.2 clause-5 cross-service hard-gate (refusing dispatch of unregistered
    resources); that enforcement semantics is a genuine owner ruling and
    stays on the P2 desk. Registry-without-gate is useful and shape-safe."

Owner ruling verbatim (2026-09-13 · governing case-agnostic precedent):

    "CORRECTION — job_kind must stay CASE-AGNOSTIC ... Do NOT lock a closed
    5-value audio-harvest enum into the platform JobManifest at CP1 — that
    leaks the audio case into generic platform code. Instead make job_kind
    reference an OPEN, registry-backed kind: a capability/job-kind REGISTRY
    that jobs register into."

Public surface (case-agnostic minimal · frozen by
tests/invariants/test_wm7_w1_post_1_resource_registry.py at ratchet close):

  ComputeResource            frozen dataclass
  ResourceRegistryInvalid    construct-time refusal
  ResourceNotRegistered      lookup miss (subclass of KeyError)
  register_resource(r)       idempotent for same id+payload; refuses
                             id-with-mismatched-payload (mutation is a
                             NEW resource, mirrors §10.2 discipline)
  is_registered(id)          bool
  list_resources()           tuple sorted by resource_id
  select_by_capability(tags) tuple superset match · sorted
  get_resource(id)           ComputeResource or ResourceNotRegistered
  _reset_registry_for_tests  test-only determinism helper

Scope boundary (registry surface ONLY):
  - NO cross-service hard-gate for unregistered dispatch (owner-desk P2).
  - NO imports of dispatch surfaces (training_runner, audio_poc,
    work_supervisor.supervisor, campaign_infra, layer_a.dispatcher, etc.).
  - NO closed enums (resource_class is OPEN string, not Literal[...]).
  - NO platform seed (unlike kind_registry.PLATFORM_SEED_KIND); resources
    register at their case wave.
  - Registry is append-only this CP: no `unregister` operation.

See notes/wm7_w1_post_1_resource_registry_grounding_brief.md for §D
wave-honest limits.
"""
from __future__ import annotations

from services.resource_registry.registry import (
    ComputeResource,
    ResourceNotRegistered,
    ResourceRegistryInvalid,
    _reset_registry_for_tests,
    get_resource,
    is_registered,
    list_resources,
    register_resource,
    select_by_capability,
)

__all__ = [
    "ComputeResource",
    "ResourceRegistryInvalid",
    "ResourceNotRegistered",
    "register_resource",
    "is_registered",
    "list_resources",
    "select_by_capability",
    "get_resource",
    "_reset_registry_for_tests",
]
