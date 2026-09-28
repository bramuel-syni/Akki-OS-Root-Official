"""WatchActionV0 · Doc 8 line 99 verbatim · four-class action ladder.

Owner-verbatim spec (canon/text/Akki_Canon_8_The_Watch.txt line 99):
    'The action ladder has four classes — annotate (mark the record,
     change nothing), shape (friction: throttle, stricter masking,
     step-up verification, a single output held), contain (suspend
     capability, preserve state, always with a time-to-live), and
     sever (cut access or trust, hold rather than expire). There is
     no fifth class: destroy does not exist in the Watch, per W3.'

§Line 30 verbatim (steerable cap):
    'Structural certainty is assertable only from signals an outsider
     cannot fabricate. Everything externally steerable caps at
     reversible containment, whatever its score.'

§Line 103 verbatim (mirage placement):
    'the mirage entry threshold sits above the containment threshold,
     because deceiving an innocent is a worse harm than throttling one.'

Grammar-enforced invariants (§Line 99 unrepresentable posture):
  * Closed Literal 4-class grammar. No fifth class.
  * `contain` MUST carry a `ttl_seconds` > 0 (line 99 verbatim: 'always
    with a time-to-live'). Model validator refuses missing TTL.
  * `sever` MUST NOT carry a TTL (line 99 verbatim: 'hold rather than
    expire'). Model validator refuses TTL on sever.
  * `sever` MUST cite a sever_certainty_signal_id (line 30-31: the
    only path to maximum autonomous force is through the closed
    six-member registry). Model validator refuses sever without it.

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/watch_action_v0.contract_snapshot.json.
  * Parity map bump 68 -> 69.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


ACTION_CLASSES: tuple = ("annotate", "shape", "contain", "sever")


class WatchActionV0(BaseModel):
    """One Mkono (hand) action · deterministic mapping from Macho (eyes)
    verdict properties per line 28 verbatim."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    action_id: str = Field(..., min_length=1)
    action_class: Literal["annotate", "shape", "contain", "sever"] = Field(
        ...,
        description="One of the four line-99 classes. Grammar closed - "
                    "'There is no fifth class: destroy does not exist in "
                    "the Watch, per W3.' Unrepresentable posture.",
    )
    subject_ref: str = Field(
        ...,
        min_length=1,
        description="The actor / capability / session under action.",
    )
    verdict_ref: str = Field(
        ...,
        min_length=1,
        description="Macho verdict this action deterministically maps from "
                    "(line 28 · Mkono holds no judgement).",
    )
    ttl_seconds: Optional[int] = Field(
        default=None,
        description="Required for 'contain' (line 99 verbatim: 'always with "
                    "a time-to-live'); forbidden for 'sever' (line 99 "
                    "verbatim: 'hold rather than expire').",
    )
    sever_certainty_signal_id: Optional[str] = Field(
        default=None,
        description="Required for 'sever' (line 30-31: 'Structural "
                    "certainty is assertable only from signals an outsider "
                    "cannot fabricate' → member of the six-signal "
                    "closed registry). Forbidden for other classes.",
    )
    reversible: bool = Field(
        ...,
        description="Line 30 verbatim: 'Everything externally steerable "
                    "caps at reversible containment, whatever its score.' "
                    "annotate/shape/contain MUST be reversible=True; "
                    "sever MAY be reversible=False.",
    )
    issued_at: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def _class_specific_invariants(self):
        # contain MUST carry a positive ttl_seconds.
        if self.action_class == "contain":
            if self.ttl_seconds is None or self.ttl_seconds <= 0:
                raise ValueError(
                    "Doc 8 line 99 verbatim: 'contain (suspend capability, "
                    "preserve state, always with a time-to-live)'. "
                    "ttl_seconds > 0 required for contain."
                )
        # sever MUST NOT carry a ttl_seconds.
        if self.action_class == "sever":
            if self.ttl_seconds is not None:
                raise ValueError(
                    "Doc 8 line 99 verbatim: 'sever (cut access or trust, "
                    "hold rather than expire)'. ttl_seconds forbidden on "
                    "sever."
                )
            if not self.sever_certainty_signal_id:
                raise ValueError(
                    "Doc 8 line 30-31 verbatim: 'Structural certainty is "
                    "assertable only from signals an outsider cannot "
                    "fabricate. ... The closed sever-certainty registry ... "
                    "is the whole of what may unlock the Watch's maximum "
                    "autonomous force.' sever action requires a "
                    "sever_certainty_signal_id from the six-member closed "
                    "registry."
                )
        # annotate/shape/contain MUST be reversible=True.
        if self.action_class in ("annotate", "shape", "contain"):
            if not self.reversible:
                raise ValueError(
                    "Doc 8 line 30 verbatim: 'Everything externally "
                    "steerable caps at reversible containment, whatever "
                    "its score.' annotate/shape/contain must be "
                    "reversible=True."
                )
            if self.sever_certainty_signal_id is not None:
                raise ValueError(
                    "sever_certainty_signal_id is only meaningful for "
                    "'sever' action (line 30-31). Forbidden on "
                    f"'{self.action_class}'."
                )
        return self
