"""services.watch.input_seat — Watch input-seat EMITTER (M12-W1d + M12-W1f).

Owner R-26 ruling (2026-09-18T~17:30Z verbatim):
    "Reading C is in scope for M12, as W1f, emitter half only ... The
     chokepoint owns the emitting half of that seam — every crossing
     event written to the Watch input seat before invoke() returns,
     and a crossing that cannot be observed does not happen
     (fail-closed; this is not the D-19 case, which concerns Watch
     actions when the Ledger is down)."

Canon 3 §13.1 verbatim:
    "Between de-identification and invocation sits the Watch's input
     seat, specified in Document 8: every payload bound for a model
     is scored for hostility and provenance before the call is made.
     The seat is a sensor and a graded gate under the Watch's own
     authority; it adds no second custody chain, and its verdicts
     land in the record like every other emission at this boundary."

Canon 8 §5 (Lango · the input seat) verbatim:
    "Every payload bound for a model — prompt, retrieved unit, tool
     result, memory read, agent instruction — scored for hostility
     and provenance at the boundary governor's chokepoint, between
     de-identification and invocation, per Document 3 §13.1.
     Graded verdicts: pass, annotate, hold, block."

Canon 8 §85 (learned-component discipline verbatim):
    "Detection models are learned and governed like every learned
     component on the platform: calibrated through the one
     calibration mechanism of Document 4 §49 ... a stale detector
     renders uncalibrated and loses its structural-certainty rights
     until refreshed."

Contract:

    score_input_seat(purpose, custody_class, tenant_id, provider)
        -> tuple[hostility, provenance, verdict]
        Lango scorer.  Placeholder honest-empty implementation at
        this seal: returns ('low', <provenance>, 'pass') because no
        learned detection models are wired yet (Canon 8 §85 discipline
        + Canon 1 §4.11 'never fabricate what wasn't measured').
        Provenance derives from declared custody_class:
          - synthetic         -> 'known'  (no estate content)
          - tenant_estate     -> 'known'  (tenant-attributed)
          - anything else    -> 'unknown'

    emit_crossing(crossing_event: CrossingEvent) -> None
        Persists the crossing event (including verdict + scores) to
        the Watch input seat's append-only store.  Raises
        WatchInputSeatUnobservable if the crossing cannot be
        persisted — the caller (invoke) MUST fail closed on this
        exception per Option D + R-26.

    WatchInputSeatUnobservable(RuntimeError)
        Fail-closed refusal on WRITE fault.  "A crossing that
        cannot be observed does not happen."

    WatchInputSeatVerdictRefused(RuntimeError)
        Fail-closed refusal on GRADED-GATE verdict = hold | block
        (Canon 3 §13.1 'graded gate under the Watch's own authority').
        Distinct from WatchInputSeatUnobservable: verdict-refused
        crossings are OBSERVED (persisted to the seat record with
        the refusal verdict) and then propagated as a refusal.

Scope note (M12-W1d landed emitter mechanism · M12-W1f hardens):
    W1d put the emitter mechanism in place (event dataclass +
    persistence + write-fault fail-close).  W1f adds the Lango
    scoring + verdict alphabet + graded-gate enforcement.  The
    consuming half (Grey Mirror + Mkono behaviour on seat events)
    remains the Watch milestone, NOT M12.

Storage:
    Events land under `${AKKI_WATCH_INPUT_SEAT_DIR}` (default
    `/tmp/akki/watch/input_seat/`) as per-tenant JSONL.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple


# ---------------------------------------------------------------------------
# Verdict + score alphabets (Canon 8 §5 Lango + graded-gate contract)
# ---------------------------------------------------------------------------

# Canon 8 §5 verbatim: "Graded verdicts: pass, annotate, hold, block."
VERDICT_ALPHABET: Tuple[str, str, str, str] = ("pass", "annotate", "hold", "block")

# Categorical hostility grading — Canon 8 §85 discipline: no learned model,
# no numeric score fabrication.
HOSTILITY_ALPHABET: Tuple[str, str, str] = ("low", "medium", "high")

# Categorical provenance grading.
PROVENANCE_ALPHABET: Tuple[str, str, str] = ("known", "unknown", "hostile")


# ---------------------------------------------------------------------------
# Refusal exceptions (two distinct fail-close classes)
# ---------------------------------------------------------------------------

class WatchInputSeatUnobservable(RuntimeError):
    """Fail-closed refusal when the crossing cannot be OBSERVED (write fault).

    Per R-26: 'a crossing that cannot be observed does not happen.'
    """


class WatchInputSeatVerdictRefused(RuntimeError):
    """Fail-closed refusal when Lango's verdict is hold | block.

    Per Canon 3 §13.1: 'graded gate under the Watch's own authority.'
    Distinct from WatchInputSeatUnobservable: the crossing IS observed
    (persisted with the refusal verdict) — the refusal is the graded
    gate's structural authority to prevent the outbound call.
    """


# ---------------------------------------------------------------------------
# CrossingEvent contract (Canon 3 §13.1: 'verdicts land in the record')
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CrossingEvent:
    """One crossing event.  Frozen — writers do not mutate.

    Fields hostility_score, provenance_score, and verdict are REQUIRED
    (no defaults) per Canon 3 §13.1: 'its verdicts land in the record
    like every other emission at this boundary.'  Field egress_host is
    REQUIRED per Canon 1 §A5.5 (W1g closed-outbound): 'a network-layer
    allowlist that refuses outbound connections from anywhere else' —
    the resolved outbound host is part of the closed-outbound audit
    trail.
    """
    at_utc: str
    tenant_id: str
    purpose: str
    custody_class: str
    prompt_sha256: str          # sha256(redacted_prompt) — never raw prompt
    provider: str
    model: str
    actor: str
    hostility_score: str        # W1f: one of HOSTILITY_ALPHABET · REQUIRED
    provenance_score: str       # W1f: one of PROVENANCE_ALPHABET · REQUIRED
    verdict: str                # W1f: one of VERDICT_ALPHABET · REQUIRED
    egress_host: str            # W1g: FQDN of the resolved outbound host · REQUIRED
    session_id: Optional[str] = None

    def to_json_dict(self) -> dict:
        return {
            "at_utc": self.at_utc,
            "tenant_id": self.tenant_id,
            "purpose": self.purpose,
            "custody_class": self.custody_class,
            "prompt_sha256": self.prompt_sha256,
            "provider": self.provider,
            "model": self.model,
            "actor": self.actor,
            "hostility_score": self.hostility_score,
            "provenance_score": self.provenance_score,
            "verdict": self.verdict,
            "egress_host": self.egress_host,
            "session_id": self.session_id or "",
        }


# ---------------------------------------------------------------------------
# Lango scorer (W1f · honest-empty placeholder until learned models wire)
# ---------------------------------------------------------------------------

# Custody classes that carry tenant-attributed provenance by declaration.
_TENANT_ATTRIBUTED_CUSTODY = frozenset({"tenant_estate"})

# Custody class that carries no estate content (self-check).
_SYNTHETIC_CUSTODY = "synthetic"


def score_input_seat(
    purpose: str,
    custody_class: str,
    tenant_id: str,
    provider: str,
) -> Tuple[str, str, str]:
    """Lango's hostility + provenance scoring → graded verdict.

    Canon 3 §13.1: 'every payload bound for a model is scored for
    hostility and provenance before the call is made'.

    Canon 8 §85: learned components are calibrated per Doc 4 §49; a
    stale/absent detector loses structural-certainty rights.  At this
    seal no learned models are wired, so this scorer returns the
    honest-empty grading (hostility=low, verdict=pass) that Canon 1
    §4.11 'never fabricate what wasn't measured' requires.  Provenance
    derives from the DECLARED custody_class alone (a structural fact
    the caller supplies), never from probabilistic inference at this
    seal.

    Learned scoring lands in the Watch milestone (Grey Mirror +
    Mkono).  Callers monkeypatch this function in tests to exercise
    the graded-gate enforcement path for hold / block verdicts.
    """
    # Provenance derives from declared custody class.
    if custody_class == _SYNTHETIC_CUSTODY:
        provenance = "known"        # no estate content · self-check
    elif custody_class in _TENANT_ATTRIBUTED_CUSTODY:
        provenance = "known"        # tenant-attributed
    else:
        provenance = "unknown"      # unlisted custody class

    # Hostility: honest-empty until learned model wires.
    hostility = "low"

    # Verdict: honest-empty pass until learned model wires.
    verdict = "pass"

    return (hostility, provenance, verdict)


# ---------------------------------------------------------------------------
# Seat storage
# ---------------------------------------------------------------------------

def _seat_dir() -> Path:
    return Path(os.environ.get("AKKI_WATCH_INPUT_SEAT_DIR", "/tmp/akki/watch/input_seat"))


def emit_crossing(event: CrossingEvent) -> None:
    """Persist the crossing event to the Watch input seat.

    Fail-closed on any I/O fault or malformed event via
    WatchInputSeatUnobservable.  Graded-gate refusal
    (WatchInputSeatVerdictRefused) is raised by the CALLER after
    emit_crossing writes the record — the record carries the refusal
    verdict so the seat is a complete log of graded gate history.
    """
    if not event.tenant_id:
        raise WatchInputSeatUnobservable(
            "tenant_id_empty — crossing event lacks tenant scope; "
            "unobservable custody path (canon 3 §14)."
        )
    if not event.custody_class:
        raise WatchInputSeatUnobservable(
            "custody_class_empty — crossing event lacks custody class."
        )
    if not event.prompt_sha256 or len(event.prompt_sha256) != 64:
        raise WatchInputSeatUnobservable(
            f"prompt_sha256_malformed — expected 64-hex, got {event.prompt_sha256!r}"
        )
    if event.verdict not in VERDICT_ALPHABET:
        raise WatchInputSeatUnobservable(
            f"verdict_out_of_alphabet — {event.verdict!r} not in "
            f"{VERDICT_ALPHABET}"
        )
    if event.hostility_score not in HOSTILITY_ALPHABET:
        raise WatchInputSeatUnobservable(
            f"hostility_score_out_of_alphabet — {event.hostility_score!r} "
            f"not in {HOSTILITY_ALPHABET}"
        )
    if event.provenance_score not in PROVENANCE_ALPHABET:
        raise WatchInputSeatUnobservable(
            f"provenance_score_out_of_alphabet — {event.provenance_score!r} "
            f"not in {PROVENANCE_ALPHABET}"
        )
    try:
        seat = _seat_dir()
        seat.mkdir(parents=True, exist_ok=True)
        tenant_log = seat / f"{event.tenant_id}.jsonl"
        with tenant_log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.to_json_dict(), sort_keys=True) + "\n")
    except OSError as exc:
        raise WatchInputSeatUnobservable(
            f"seat_write_failed — {type(exc).__name__}: {str(exc)[:200]}"
        ) from exc


__all__ = [
    "CrossingEvent",
    "HOSTILITY_ALPHABET",
    "PROVENANCE_ALPHABET",
    "VERDICT_ALPHABET",
    "WatchInputSeatUnobservable",
    "WatchInputSeatVerdictRefused",
    "emit_crossing",
    "score_input_seat",
]
