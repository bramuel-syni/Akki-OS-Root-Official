"""services.resource_registry.registry — canonical implementation.

See services/resource_registry/__init__.py for owner-ruling context +
scope-boundary discipline. All shape decisions here trace to one of:

  - 2026-09-16T~05:10Z owner ruling (registry surface ONLY · no gate).
  - 2026-09-13 owner CASE-AGNOSTIC correction (no closed enums).
  - Standing invariant test_wm7_w1_post_1_resource_registry.py (freezes
    the public surface at ratchet close).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Tuple


class ResourceRegistryInvalid(ValueError):
    """Raised at ComputeResource construct time on shape refusal, and
    by register_resource() when a mutation is attempted (id already
    registered with a different payload)."""


class ResourceNotRegistered(KeyError):
    """Raised by get_resource() when the id has no registration."""


_ISO8601_Z_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
)


def _validate_non_empty(field_name: str, value: str) -> str:
    if not isinstance(value, str):
        raise ResourceRegistryInvalid(
            f"{field_name!r} must be a str, got {type(value).__name__}"
        )
    if not value.strip():
        raise ResourceRegistryInvalid(
            f"{field_name!r} must be a non-empty / non-whitespace string; "
            f"got {value!r}"
        )
    return value


def _validate_capability_tags(tags) -> Tuple[str, ...]:
    if not isinstance(tags, (list, tuple)):
        raise ResourceRegistryInvalid(
            f"capability_tags must be a list or tuple, got "
            f"{type(tags).__name__}"
        )
    validated = []
    for t in tags:
        if not isinstance(t, str):
            raise ResourceRegistryInvalid(
                f"capability_tags must contain only strings; got "
                f"{type(t).__name__} entry"
            )
        if not t.strip():
            raise ResourceRegistryInvalid(
                f"capability_tags entries must be non-empty / non-"
                f"whitespace; got {t!r}"
            )
        validated.append(t)
    return tuple(sorted(validated))


def _validate_iso8601_z(value: str) -> str:
    if not isinstance(value, str) or not _ISO8601_Z_RE.match(value):
        raise ResourceRegistryInvalid(
            f"registered_at_utc must be ISO-8601 with Z suffix "
            f"(e.g. '2026-09-16T05:20:00Z'); got {value!r}"
        )
    return value


@dataclass(frozen=True)
class ComputeResource:
    """A registered compute resource. Case-agnostic minimal shape.

    All fields are validated at construct time via __post_init__. The
    dataclass is frozen so external code cannot mutate a snapshot.

    Fields:
      resource_id:       non-empty string; globally unique per registry.
      resource_class:    non-empty OPEN string. No closed enum per the
                         2026-09-13 owner correction; downstream jobs
                         interpret their own conventions.
      capability_tags:   tuple of non-empty strings, sorted deterministically
                         at construct time.
      registered_at_utc: ISO-8601 with Z suffix.
    """
    resource_id: str
    resource_class: str
    capability_tags: Tuple[str, ...] = field(default_factory=tuple)
    registered_at_utc: str = ""

    def __post_init__(self) -> None:
        # Validate + normalise. Because the dataclass is frozen, we use
        # object.__setattr__ to install the normalised tuple for
        # capability_tags.
        _validate_non_empty("resource_id", self.resource_id)
        _validate_non_empty("resource_class", self.resource_class)
        _validate_iso8601_z(self.registered_at_utc)
        normalised_tags = _validate_capability_tags(self.capability_tags)
        object.__setattr__(self, "capability_tags", normalised_tags)


# Process-scope registry. Wave-honest limit D.4: durable on-disk audit
# trail of registrations is a later refinement (mirrors
# kind_registry.py wave-honest limit E-4).
_REGISTERED: Dict[str, ComputeResource] = {}


def register_resource(resource: ComputeResource) -> None:
    """Register a resource.

    Idempotent for the same resource_id + identical payload. If a
    resource_id is already registered with a DIFFERENT payload,
    ResourceRegistryInvalid is raised — mutation is refused; a change
    is a NEW resource (mirrors §10.2 verbatim JobManifest discipline
    'A change is a NEW run, not a mutation').

    Requires an actual ComputeResource instance (strict typing);
    passing a dict raises TypeError.
    """
    if not isinstance(resource, ComputeResource):
        raise TypeError(
            f"register_resource requires a ComputeResource instance, "
            f"got {type(resource).__name__}"
        )
    existing = _REGISTERED.get(resource.resource_id)
    if existing is None:
        _REGISTERED[resource.resource_id] = resource
        return
    if existing == resource:
        # Idempotent no-op.
        return
    raise ResourceRegistryInvalid(
        f"resource_id {resource.resource_id!r} already registered with a "
        f"different payload; register a new resource_id instead "
        f"(a change is a NEW resource, mirrors JobManifest §10.2 "
        f"discipline)"
    )


def is_registered(resource_id: str) -> bool:
    """Return True iff a resource with resource_id is registered."""
    return resource_id in _REGISTERED


def list_resources() -> Tuple[ComputeResource, ...]:
    """Return an immutable snapshot of all registered resources, sorted
    by resource_id. Tuple so callers cannot mutate the registry via the
    return value."""
    return tuple(_REGISTERED[k] for k in sorted(_REGISTERED))


def select_by_capability(
    required_tags: set,
) -> Tuple[ComputeResource, ...]:
    """Return resources whose capability_tags is a superset of
    required_tags. Empty required_tags returns all registered resources.
    Sorted by resource_id for determinism."""
    required = set(required_tags)
    hits = []
    for rid in sorted(_REGISTERED):
        r = _REGISTERED[rid]
        if required.issubset(set(r.capability_tags)):
            hits.append(r)
    return tuple(hits)


def get_resource(resource_id: str) -> ComputeResource:
    """Return the registered resource. Raises ResourceNotRegistered on miss."""
    if resource_id not in _REGISTERED:
        raise ResourceNotRegistered(
            f"resource_id {resource_id!r} is not registered"
        )
    return _REGISTERED[resource_id]


def _reset_registry_for_tests() -> None:
    """Wipe the registry. Test-only determinism helper — the leading
    underscore signals it is not a stable public API."""
    _REGISTERED.clear()


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
