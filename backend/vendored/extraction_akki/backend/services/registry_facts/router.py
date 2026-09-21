"""services.registry_facts.router — GET /api/registry/facts.

Owner Order 2026-08-19 · FL-P2-25. Read-only. IP-allowlist middleware gates
access at the surface boundary; this router adds no per-route auth.
"""
from __future__ import annotations

from fastapi import APIRouter

from services.registry_facts.facts import assemble_facts

router = APIRouter()


@router.get("/api/registry/facts")
async def get_registry_facts():
    """Return the assembled Registry facts dict.

    Never carries secrets. Every figure traces to a durable record on disk.
    """
    return assemble_facts()
