"""services.chokepoint.llm_endpoint_allowlist — W5 · provider-scoped egress.

Owner ruling 2026-08-25 (plan confirmation) · sharpening §2:
    "The egress allowlist gains a provider host ONLY at the moment a
     key of that provider is actually connected (allowlist entries are
     facts tied to connections, ledgered like everything else — not
     pre-opened for all three providers). Until a provider key is
     pasted, the only LLM egress host allowed is the Emergent
     integration endpoint."

Contract:
    allowlisted_providers() → set[str]
        Providers whose connection is on record RIGHT NOW.
        - "emergent" if env var EMERGENT_LLM_KEY is present.
        - <provider> if a data_connection_record file
          `data_source_llm_<provider>_*_FINAL.json` exists on disk.

    resolve_endpoint(provider) → {"host": str, "region": str}
        Governed host + region for the provider. Refuses if the
        provider is not on the live allowlist (LLMEndpointRefused).

    LLMEndpointRefused
        Raised when a crossing targets a provider host that is not on
        the live connection-scoped allowlist.

Governance:
    The `llm_endpoint_allowlist.v0.json` file names the four candidate
    provider hosts + their connection_probe (env-var or file glob).
    Adding a new provider requires an Owner ruling recorded in
    STATE/DECISIONS.md.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Set


class LLMEndpointRefused(ValueError):
    """Raised when a crossing targets an off-allowlist provider host."""


_ALLOWLIST_PATH = Path(__file__).resolve().parent / "llm_endpoint_allowlist.v0.json"

# Default data_connection_record directory — mirrors registry_facts.
_DEFAULT_DCR = "/app/assessment_workspace/phase0/data_connection_records"


def _dcr_dir() -> Path:
    return Path(os.environ.get("DATA_CONNECTION_RECORD_DIR", _DEFAULT_DCR))


def _load_allowlist() -> Dict[str, Any]:
    # M12-W1c · SEC-1 runtime wire: unverifiable policy = closed gate
    # (FP-1 fail-closed + FP-2 source-retained-on-abort). See
    # services/chokepoint/policy_integrity.py.
    from services.chokepoint.policy_integrity import load_policy_with_integrity
    return load_policy_with_integrity(_ALLOWLIST_PATH)


def _providers_config() -> Dict[str, Dict[str, Any]]:
    return {p["provider"]: p for p in _load_allowlist().get("providers", [])}


def _is_provider_connected(provider: str, config: Dict[str, Any]) -> bool:
    """Probe whether the provider currently has a connection on record."""
    probe = config.get("connection_probe", "")
    kind = config.get("connection_kind", "")

    if kind == "env_var":
        env_name = probe.split("::", 1)[1] if "::" in probe else ""
        return bool(env_name and os.environ.get(env_name))

    if kind == "estate_keys_file":
        # Match against data_connection_records/ (the authoritative
        # index for "what is connected"). The glob comes from the probe
        # string (`data_connection_record::<pattern>`).
        pattern = probe.split("::", 1)[1] if "::" in probe else ""
        if not pattern:
            return False
        d = _dcr_dir()
        if not d.is_dir():
            return False
        return any(d.glob(pattern))

    return False


def allowlisted_providers() -> Set[str]:
    """Set of providers whose connection is on record RIGHT NOW.

    Owner sharpening §2 — allowlist entries are facts tied to connections.
    """
    out: Set[str] = set()
    for provider, config in _providers_config().items():
        if _is_provider_connected(provider, config):
            out.add(provider)
    return out


def allowlisted_hosts() -> Set[str]:
    """Set of provider HOSTS currently admissible for outbound crossings."""
    out: Set[str] = set()
    config = _providers_config()
    for provider in allowlisted_providers():
        entry = config.get(provider, {})
        host = entry.get("host")
        if host:
            out.add(host)
    return out


def resolve_endpoint(provider: str) -> Dict[str, str]:
    """Return the {host, region} for `provider` if on the live allowlist.

    Raises LLMEndpointRefused if the provider has no connection on
    record.
    """
    if not provider:
        raise LLMEndpointRefused(
            "provider_required — empty provider refused."
        )
    config = _providers_config()
    entry = config.get(provider)
    if entry is None:
        raise LLMEndpointRefused(
            f"provider_unknown — {provider!r} not on the governed allowlist. "
            f"Known providers: {sorted(config.keys())}. "
            "Adding a provider requires an Owner ruling."
        )
    if not _is_provider_connected(provider, entry):
        raise LLMEndpointRefused(
            f"provider_not_connected — {provider!r} has no key on record. "
            f"Owner sharpening 2026-08-25 §2: allowlist entries are facts tied "
            "to connections. Paste a key via ConnectDrawerChat's 'An LLM' chip "
            "and verify via chokepoint's llm.connect_verify purpose."
        )
    return {"host": entry["host"], "region": entry["region"]}


__all__ = [
    "LLMEndpointRefused",
    "allowlisted_providers",
    "allowlisted_hosts",
    "resolve_endpoint",
]
