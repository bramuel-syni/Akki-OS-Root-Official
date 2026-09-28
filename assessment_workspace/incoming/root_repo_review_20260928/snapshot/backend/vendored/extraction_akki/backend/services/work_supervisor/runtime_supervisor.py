"""services.work_supervisor.runtime_supervisor — W1 · CP2b.

Owner directive verbatim (2026-09-13, W1 CP breakdown approval):

    "the RUNTIME work-supervisor must land in W1, not be deferred to
    dispatch ... progress_signal, output_verification_watchdog,
    starvation_alarm ... Test them against SIMULATED run states (no
    real dispatch needed): a run whose GPU-util stays 0 / whose output
    artifact doesn't grow past its SLA → the watchdog must raise a
    starvation alarm and emit a HALT verdict; a run producing real
    growing output past its gate → passes."

STANDING ORDER §3.2 banked in STATE/STANDING_ORDERS.md verbatim:

    NO RUN WITHOUT A PROGRESS SIGNAL — every commissioned run must
    emit a progress signal within its SLA or the supervisor raises a
    starvation alarm and HALTS the run.

Zero-influence: the watchdog READS progress signals + optionally
STATs the named output artifact. It never kills any process. A HALT
verdict is DATA (a returned dataclass); callers act on it.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


class StarvationAlarm(RuntimeError):
    """Raised by internal helpers when a run is starving. The public
    `output_verification_watchdog` returns HaltVerdict rather than
    raising, so callers can pattern-match. StarvationAlarm exists as
    a named class so downstream code can `except` on it if it wraps
    the watchdog inside a raising boundary."""


@dataclass(frozen=True)
class ProgressSignal:
    """A point-in-time record that a commissioned run emitted work."""
    job_id: str
    at_utc: str               # ISO-8601 with Z suffix
    magnitude: float          # opaque scalar; downstream can interpret
    output_bytes: int         # cumulative bytes written to output_path
    output_path: str          # absolute path or "" if no artifact


@dataclass(frozen=True)
class HaltVerdict:
    """Data record: a run has starved. Callers act on it — the runtime
    supervisor never kills anything."""
    job_id: str
    reason: str               # 'starvation_no_signal' | 'starvation_stale_signal'
                              # | 'starvation_output_flatline'
    at_utc: str
    last_progress_at_utc: Optional[str]
    message: str


def _default_ring_root() -> Path:
    """Env-driven default for the progress ring root. Test callers
    always pass an explicit ring_root; production callers can rely on
    AKKI_PROGRESS_RING (no filesystem default so misconfiguration
    fails fast)."""
    raw = os.environ.get("AKKI_PROGRESS_RING")
    if not raw:
        raise RuntimeError(
            "AKKI_PROGRESS_RING env var is unset — the runtime "
            "supervisor requires an explicit progress-ring root"
        )
    return Path(raw)


def _ring_dir_for(job_id: str, ring_root: Path) -> Path:
    return Path(ring_root) / job_id


def _parse_iso_z(v: str) -> datetime:
    if v.endswith("Z"):
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc,
        )
    return datetime.fromisoformat(v).astimezone(timezone.utc)


def record_progress(
    sig: ProgressSignal,
    *,
    ring_root: Optional[Path] = None,
) -> Path:
    """Persist a ProgressSignal to the ring. Returns the file path
    written. One JSON per signal — sortable by filename via at_utc."""
    root = Path(ring_root) if ring_root is not None else _default_ring_root()
    d = _ring_dir_for(sig.job_id, root)
    d.mkdir(parents=True, exist_ok=True)
    # Compact filename: <at_utc>__<magnitude>_<bytes>.json — sorts by
    # at_utc lexicographically.
    fname = f"{sig.at_utc}__mag{sig.magnitude}_bytes{sig.output_bytes}.json"
    p = d / fname
    p.write_text(json.dumps(asdict(sig), sort_keys=True), encoding="utf-8")
    return p


def load_progress(
    job_id: str,
    *,
    ring_root: Optional[Path] = None,
) -> List[ProgressSignal]:
    """Load all progress signals for a job, sorted ascending by
    at_utc. Empty list if the job has never recorded."""
    root = Path(ring_root) if ring_root is not None else _default_ring_root()
    d = _ring_dir_for(job_id, root)
    if not d.exists() or not d.is_dir():
        return []
    signals: List[ProgressSignal] = []
    for p in sorted(d.glob("*.json")):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        signals.append(ProgressSignal(
            job_id=payload["job_id"],
            at_utc=payload["at_utc"],
            magnitude=float(payload["magnitude"]),
            output_bytes=int(payload["output_bytes"]),
            output_path=str(payload.get("output_path", "")),
        ))
    signals.sort(key=lambda s: s.at_utc)
    return signals


def output_verification_watchdog(
    job_id: str,
    *,
    sla_seconds: int,
    ring_root: Path,
    now_utc: datetime,
    output_path: Optional[Path] = None,
) -> Optional[HaltVerdict]:
    """Read the ring for `job_id`, apply the three starvation gates
    in order (no-signal → stale → output-flatline), and return a
    HaltVerdict on the first hit. Returns None if the run is healthy.

    Zero-influence: no writes, no signals, no process interaction.

    output_path override: callers may pass a Path here explicitly.
    Otherwise the watchdog uses the `output_path` recorded in the
    signals themselves. If both are absent (empty string in signals
    AND no override), the flatline gate is skipped and only signal
    freshness is checked (wave-honest limit E-5).
    """
    now_iso = now_utc.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signals = load_progress(job_id, ring_root=ring_root)

    # Gate 1: no signal ever.
    if not signals:
        return HaltVerdict(
            job_id=job_id,
            reason="starvation_no_signal",
            at_utc=now_iso,
            last_progress_at_utc=None,
            message=(
                f"no progress signal ever recorded for job {job_id!r} — "
                "STANDING ORDER §3.2 requires a signal within the SLA"
            ),
        )

    newest = signals[-1]
    newest_dt = _parse_iso_z(newest.at_utc)
    age_s = (now_utc - newest_dt).total_seconds()

    # Gate 2: newest signal older than SLA.
    if age_s > sla_seconds:
        return HaltVerdict(
            job_id=job_id,
            reason="starvation_stale_signal",
            at_utc=now_iso,
            last_progress_at_utc=newest.at_utc,
            message=(
                f"newest progress signal age {age_s:.1f}s exceeds SLA "
                f"{sla_seconds}s — STANDING ORDER §3.2 HALT"
            ),
        )

    # Gate 3: output-flatline across the SLA window.
    # Skip if no output_path known.
    resolved_output = str(output_path) if output_path else newest.output_path
    if not resolved_output:
        return None

    window_start_dt = now_utc.astimezone(timezone.utc) - _timedelta_seconds(
        sla_seconds
    )
    in_window = [s for s in signals
                 if _parse_iso_z(s.at_utc) >= window_start_dt]
    if len(in_window) >= 2:
        window_bytes = [s.output_bytes for s in in_window]
        if window_bytes[-1] <= window_bytes[0]:
            return HaltVerdict(
                job_id=job_id,
                reason="starvation_output_flatline",
                at_utc=now_iso,
                last_progress_at_utc=newest.at_utc,
                message=(
                    f"output_bytes at {resolved_output} did not grow "
                    f"across the SLA window ({window_bytes[0]} → "
                    f"{window_bytes[-1]}) — STANDING ORDER §3.2 HALT"
                ),
            )

    return None


def _timedelta_seconds(s: int):
    from datetime import timedelta
    return timedelta(seconds=int(s))


__all__ = [
    "ProgressSignal",
    "HaltVerdict",
    "StarvationAlarm",
    "record_progress",
    "load_progress",
    "output_verification_watchdog",
]
