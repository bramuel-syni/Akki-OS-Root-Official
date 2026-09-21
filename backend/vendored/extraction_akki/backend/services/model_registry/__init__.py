"""services.model_registry — top-level model registry for the Akki estate.

Owner Ruling 2026-08-25T23:30Z (W7 GO · Q3 disposition):
  Top-level `services/model_registry/` (NOT `services/perception/`).
  This estate's registry is a first-class service, consistent with how
  chokepoint / solva / northena landed. Semantics adapted from
  RMS-IQ-Core-2 `backend/services/perception/model_registry.py`
  (Owner 9.2a-E1 α · 2026-07-10).

Registry seeds from FACTS: 7 Emergent Universal models are real
(W5-connected via Owner Order 2026-08-25 §2). whisper-tiny is NOT
seeded — it stays a donor-side CI fixture, not a real model on this
estate. Only real models on record.
"""
from services.model_registry.registry import (
    HONEST_REGISTRY_LOCATION,
    attest_model,
    current_registry_version,
    load_registry,
    register_model,
)

__all__ = [
    "HONEST_REGISTRY_LOCATION",
    "attest_model",
    "current_registry_version",
    "load_registry",
    "register_model",
]
