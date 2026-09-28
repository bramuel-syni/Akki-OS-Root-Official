"""services.capability_registry — W1b · CP4 · generic capability registry.

Contract:
  register_capability(category: str, name: str, import_path: str) -> None
                                        # idempotent for same import_path
  get_capability(category: str, name: str) -> Type
  list_categories() -> tuple[str, ...]                 # sorted snapshot
  list_capabilities_in(category: str) -> tuple[str, ...]  # sorted snapshot
  CapabilityNotRegistered(ValueError)
  _reset_capabilities_for_tests() -> None

Import-path format: "package.module:ClassName" — same shape as the
provider factories in this codebase.

Case-agnostic: this module carries NO category-specific tokens. It
merely stores (category, name) -> import_path mappings and resolves
them lazily.
"""
from __future__ import annotations

import importlib
from typing import Dict, Tuple, Type


class CapabilityNotRegistered(ValueError):
    """Raised for unknown categories/names OR conflicting rebinds."""


# Process-scope registry: {category: {name: import_path}}
_CAPABILITIES: Dict[str, Dict[str, str]] = {}


def _parse_import_path(import_path: str) -> Tuple[str, str]:
    if not isinstance(import_path, str) or ":" not in import_path:
        raise ValueError(
            f"import_path {import_path!r} must be 'module:ClassName'"
        )
    mod_path, _, cls_name = import_path.partition(":")
    if not mod_path or not cls_name:
        raise ValueError(
            f"import_path {import_path!r} must have non-empty module "
            "AND class name on either side of the ':'"
        )
    return mod_path, cls_name


def register_capability(
    category: str,
    name: str,
    import_path: str,
) -> None:
    """Register (category, name) -> import_path. Idempotent for same
    import_path; raises CapabilityNotRegistered on conflicting rebind."""
    if not isinstance(category, str) or not category.strip():
        raise ValueError("category must be a non-empty string")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    _parse_import_path(import_path)  # validates shape

    bucket = _CAPABILITIES.setdefault(category, {})
    existing = bucket.get(name)
    if existing is not None and existing != import_path:
        raise CapabilityNotRegistered(
            f"({category}, {name}) is already bound to import_path "
            f"{existing!r}; refusing to rebind to {import_path!r}"
        )
    bucket[name] = import_path


def get_capability(category: str, name: str) -> Type:
    """Resolve (category, name) to the underlying class. Raises
    CapabilityNotRegistered on unknown category or name."""
    bucket = _CAPABILITIES.get(category)
    if bucket is None:
        raise CapabilityNotRegistered(
            f"category {category!r} is not registered"
        )
    import_path = bucket.get(name)
    if import_path is None:
        raise CapabilityNotRegistered(
            f"name {name!r} is not registered under category "
            f"{category!r}"
        )
    mod_path, cls_name = _parse_import_path(import_path)
    module = importlib.import_module(mod_path)
    return getattr(module, cls_name)


def list_categories() -> Tuple[str, ...]:
    return tuple(sorted(_CAPABILITIES))


def list_capabilities_in(category: str) -> Tuple[str, ...]:
    bucket = _CAPABILITIES.get(category)
    if bucket is None:
        return ()
    return tuple(sorted(bucket))


def _reset_capabilities_for_tests() -> None:
    _CAPABILITIES.clear()


__all__ = [
    "register_capability",
    "get_capability",
    "list_categories",
    "list_capabilities_in",
    "CapabilityNotRegistered",
    "_reset_capabilities_for_tests",
]
