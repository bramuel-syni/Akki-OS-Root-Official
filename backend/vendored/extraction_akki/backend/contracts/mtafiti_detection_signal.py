"""Mtafiti DetectionSignal — frozen contract.

W-MTAFITI-GPU-DISCOVERY · CP1 kernel.

Canon binding (RMS_Mtafiti_Specification.md §4, verbatim):
    "The learned component produces detections, never verdicts. …
     Learning detects; the governed Matrix decides; the declaration
     baseline floors; the V3 gate admits."

C4-009 · Neither layer decides what a measurement means.

Rule enforced here:
  The GPU-powered enrichment layer (PII detector, semantic column
  classifier, embedding-based dedup signal emitter, language detector,
  content-type profiler, cross-table relationship candidates, cross-
  estate corroboration) emits DetectionSignal typed objects.

  DetectionSignal has a CLOSED schema — extra="forbid". No verdict-
  shaped keys (verdict / decision / classification_label /
  sensitivity_class / defensibility_class / authority / ruling /
  same_entity) may be constructed.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EvidenceClass(str, Enum):
    """Canonical evidence taxonomy — 5 classes (Doc 5 §5)."""

    FACT = "fact"
    INFERRED = "inferred"
    DETECTED = "detected"
    REPORTED = "reported"
    DECLARED = "declared"


class DetectionSignal(BaseModel):
    """One detection emitted by a mtafiti GPU-powered enrichment.

    Deliberately NEVER carries a verdict-shaped field. Deliberately
    frozen — an emitted DetectionSignal is a receipt, not a mutable
    workspace.

    `detector_version` pins the model that emitted the signal (V3-gate
    supports acceptance-per-tenant per Mtafiti-Spec §4).
    `seed` is present when the emitter was deterministic (RL / adaptive
    sampling walkers, deduplication embedding thresholds, etc.).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    signal_name: str = Field(min_length=1)
    evidence_class: EvidenceClass
    confidence: float = Field(ge=0.0, le=1.0)
    source_ref: str = Field(min_length=1)
    detector_version: str = Field(min_length=1)
    seed: Optional[int] = None
