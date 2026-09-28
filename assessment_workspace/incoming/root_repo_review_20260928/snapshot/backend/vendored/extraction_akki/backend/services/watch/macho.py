"""services.watch.macho · Doc 8 line 28 verbatim — the eyes.

'the Watch is two engines: Macho, the eyes, which senses and asserts
and holds no powers whatsoever; and Mkono, the hand, which acts and
holds no judgement — a deterministic mapping from verdict properties
to actions. This is the platform's own standing rule — learning may
detect, it may never decide — applied to security whole.'
                                                    — Canon 8 §Line 28

Two capabilities lives on this module:

1. `MachoVerdict` schema (frozen · extra=forbid). Closed two-member
   `verdict_class` grammar — 'externally_steerable' (score-shaped
   signal, cap at reversible containment per §Line 30) and
   'structural_certainty' (rooted in the closed six-signal registry
   per §Line 31). No confidence field, by construction (§Line 31
   verbatim: 'no parameter through which a detector's confidence
   can enter').

2. `mint_macho_verdict(v)`. Writes one verdict row (write-once JSONL
   via services.watch.persistence). For structural_certainty verdicts
   it dereferences the sever_certainty_signal_id against the on-record
   store — the signature is the guard (§Line 31 verbatim), not the
   caller's word.

Legacy `mint_verdict()` for the earlier WatchVerdictRow_v0 grammar is
retained unchanged so W10 CP8 rollup surfaces continue to render.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from contracts.watch_verdict import WatchVerdictRow_v0


# ---------------- W10 CP8 legacy Macho ---------------- #


_DEFAULT_DIR = "/app/assessment_workspace/phase0/watch_verdicts"


def _dir() -> Path:
    return Path(os.environ.get("WATCH_VERDICTS_DIR", _DEFAULT_DIR))


def mint_verdict(payload: Dict[str, Any]) -> WatchVerdictRow_v0:
    """Legacy Macho path (W10 CP8) — writes a WatchVerdictRow_v0 to
    disk. Retained for the state-rollup surface. Refuses overwrite
    (Canon 8 §43: NEITHER record is amended in place)."""
    v = WatchVerdictRow_v0(**payload)
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{v.verdict_id}.json"
    if path.exists():
        raise ValueError(
            f"verdict {v.verdict_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(v.model_dump(), indent=2, ensure_ascii=False))
    return v


def load_verdicts() -> List[WatchVerdictRow_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return sorted(
        (WatchVerdictRow_v0(**json.loads(p.read_text()))
         for p in d.glob("vd_*.json")),
        key=lambda v: (v.at_iso, v.verdict_id),
    )


# ---------------- W11 C CP-C2 · MachoVerdict schema ---------------- #


class MachoVerdict(BaseModel):
    """One Macho verdict · Doc 8 §Line 28 verbatim: 'the eyes, which
    senses and asserts and holds no powers whatsoever.'

    §Line 30 verbatim (closed disjoint grammar of verdict_class):
        'Structural certainty is assertable only from signals an
         outsider cannot fabricate. Everything externally steerable
         caps at reversible containment, whatever its score.'

    §Line 31 verbatim (no confidence parameter):
        'The certainty computation is a function with no parameter
         through which a detector's confidence can enter.'
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    verdict_id: str = Field(..., min_length=1)
    verdict_class: Literal["externally_steerable", "structural_certainty"] = Field(
        ...,
        description="§Line 30 verbatim: the two disjoint verdict "
                    "classes. Closed grammar - no third member without "
                    "spec ceremony (§Line 221 owner-only).",
    )
    subject_ref: str = Field(..., min_length=1)
    evidence_ref: str = Field(..., min_length=1)
    asserted_at: str = Field(..., min_length=1)
    intensity: Literal["noted", "elevated", "severe"] = Field(
        default="noted",
        description="Assertion strength for externally-steerable "
                    "verdicts. Ignored for structural_certainty (§Line "
                    "31 verbatim: 'no parameter through which a "
                    "detector's confidence can enter').",
    )
    sever_certainty_signal_id: Optional[str] = Field(
        default=None,
        description="Required (non-empty) when verdict_class == "
                    "'structural_certainty'; forbidden otherwise. "
                    "§Line 30 verbatim: 'Structural certainty is "
                    "assertable only from signals an outsider cannot "
                    "fabricate.'",
    )

    @model_validator(mode="after")
    def _class_specific_invariants(self):
        if self.verdict_class == "structural_certainty":
            if not self.sever_certainty_signal_id:
                raise ValueError(
                    "Doc 8 §Line 30 verbatim: 'Structural certainty is "
                    "assertable only from signals an outsider cannot "
                    "fabricate.' structural_certainty verdict requires "
                    "a sever_certainty_signal_id (a member of the "
                    "closed six-signal registry, §Line 31)."
                )
        else:  # externally_steerable
            if self.sever_certainty_signal_id:
                raise ValueError(
                    "Doc 8 §Line 30 verbatim: externally-steerable "
                    "signals are the ones an outsider CAN shape. They "
                    "cannot carry a sever-certainty signal — the two "
                    "verdict classes are grammatically disjoint. "
                    "Confidence-laundering into the closed registry "
                    "is refused by construction (§Line 31)."
                )
        return self


# ---------------- W11 C CP-C2 · mint_macho_verdict ---------------- #


def mint_macho_verdict(v: MachoVerdict) -> MachoVerdict:
    """Land a MachoVerdict on the shared record (§Line 6 seam law).

    For structural_certainty verdicts, we dereference the
    sever_certainty_signal_id against the on-record store — §Line 31
    verbatim: 'the signature is the guard.' A signal that is not on
    record cannot become the root of maximum autonomous force.

    Raises:
      ValueError · when a cited sever_certainty_signal is not on record.
      WriteOnceViolation · via persistence layer on duplicate verdict_id.
    """
    if v.verdict_class == "structural_certainty":
        from services.watch.sever_signals import get_sever_signal

        # Guard: signal MUST be on the shared record. Line 31 verbatim.
        assert v.sever_certainty_signal_id is not None  # schema-guaranteed
        on_record = get_sever_signal(v.sever_certainty_signal_id)
        if on_record is None:
            raise ValueError(
                f"sever_certainty_signal {v.sever_certainty_signal_id!r} "
                "not on record. Doc 8 §Line 31 verbatim: 'the signature "
                "is the guard.' A structural-certainty verdict cannot "
                "assert on a phantom signal."
            )

    from services.watch.persistence import append_verdict
    return append_verdict(v)
