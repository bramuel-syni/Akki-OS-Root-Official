"""WhitepaperDraft_v0 · Doc 14 §33 · CA1-005 · W10 CP6.

CA1-005 verbatim: "Exceptional-run retention · 'Prepare white paper'
action drafting from run artefacts." Doc 14 §33. Promise #25 · BUILD
(no LIFT · Executive-Core deck_*.py is a deck-generation pipeline,
not a whitepaper artefact drafter).

Owner Q4 W7 (2026-08-26T00:25Z): 150-LOC lid on this BUILD.

Freeze contract: parity 58 → 59.
"""
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class WhitepaperDraft_v0(BaseModel):
    """A whitepaper drafted from run artefacts (§33 Promise #25)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    whitepaper_id: str = Field(..., min_length=1,
        pattern=r"^wp_[a-z0-9_-]+$",
        description="Convention: 'wp_<yyyy_mm_dd>_<n>'.")
    run_ref: str = Field(..., min_length=1,
        description="Stable reference to the run this whitepaper "
                    "summarises (task_id / run_id / commissioning_id).")
    drafted_at: str = Field(..., min_length=1,
        description="ISO-8601 UTC when the whitepaper was drafted.")
    drafted_by: str = Field(..., min_length=1,
        description="Actor id who authored the draft.")
    cites_model_admission_id: str = Field(..., min_length=1,
        description="Doc 14 §33 CITATION invariant: whitepaper MUST "
                    "cite the ModelAcceptanceCard admission record ID.")
    cites_baseline_line_id: str = Field(..., min_length=1,
        description="Doc 14 §33 CITATION invariant: whitepaper MUST "
                    "cite the BaselineLine_v0 record ID.")
    summary_note: str = Field(..., min_length=1,
        description="Facts-not-claims sentence naming what the run "
                    "produced (measured quantities · outcome).")
    retention_class: Literal["standard", "exceptional_run"] = Field(...,
        description="Doc 8 · CA1-N1 retention grammar. Exceptional-run "
                    "whitepapers ride the exceptional retention window.")
