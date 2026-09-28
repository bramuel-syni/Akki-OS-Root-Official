"""services.work_supervisor.governance — W1 · CP3 · governance primitives.

Owner directive verbatim (2026-09-13, W1 CP breakdown approval):

    "Governance-rule seed (CP3): your three generic rules are fine
    (licence_class_required, dispatch_intent_configured,
    output_contract_names_real_kind) — keep them generic, no
    case-specific tokens."

Contract:
  Verdict (dataclass, frozen): passed, rule_name, reason
  GovernanceRule (ABC): name (class attr, non-empty), apply(m) -> Verdict
  apply_rules(rules, manifest) -> tuple[Verdict, ...]
                                  # verdicts in registration order
  bank_verdict(verdict, *, ledger_root, job_id, manifest_fingerprint,
               dedupe_window_seconds=60) -> Path | None
                                  # idempotent within dedupe window,
                                  # None on I/O failure (zero-influence)
  RulingLedgerEntry (dataclass, frozen): banked_at_utc, verdict, job_id,
                                         manifest_fingerprint

  Seeded generic rules:
    LicenceClassRequired
    DispatchIntentConfigured
    OutputContractNamesRealKind

Zero-influence: rules are pure functions of the manifest (no I/O).
bank_verdict writes a single ledger row (best-effort, swallows errors).
"""
from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from services.output_verified_seal import NON_REAL_KINDS
from services.work_supervisor.job_manifest import JobManifest


log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Verdict:
    passed: bool
    rule_name: str
    reason: str


@dataclass(frozen=True)
class RulingLedgerEntry:
    banked_at_utc: str
    verdict: Verdict
    job_id: str
    manifest_fingerprint: str


class GovernanceRule(ABC):
    """Base class for a generic, case-agnostic governance rule.

    Subclasses set `name` (class-level, non-empty) and implement
    `apply(manifest) -> Verdict`. Rules are pure functions — no I/O.
    """
    name: str = ""

    @abstractmethod
    def apply(self, manifest: JobManifest) -> Verdict:
        ...


# ---------------------------------------------------------------------------
# Seeded rules (generic, no case-B specifics)
# ---------------------------------------------------------------------------


class LicenceClassRequired(GovernanceRule):
    name = "licence_class_required"

    def apply(self, manifest: JobManifest) -> Verdict:
        licence = manifest.scope.get("licence_class")
        if not isinstance(licence, str) or not licence.strip():
            return Verdict(
                passed=False,
                rule_name=self.name,
                reason=(
                    "manifest.scope.licence_class is missing or empty — "
                    "every commissioned job must declare a licence class"
                ),
            )
        return Verdict(passed=True, rule_name=self.name, reason="")


class DispatchIntentConfigured(GovernanceRule):
    name = "dispatch_intent_configured"

    def apply(self, manifest: JobManifest) -> Verdict:
        intent = manifest.dispatch_intent
        if intent == "local":
            return Verdict(passed=True, rule_name=self.name, reason="")
        if intent.startswith("ssh_host_slug:"):
            slug = intent[len("ssh_host_slug:"):]
            raw = os.environ.get("AKKI_GPU_HOSTS", "")
            slugs = tuple(s.strip() for s in raw.split(",") if s.strip())
            if slug in slugs:
                return Verdict(passed=True, rule_name=self.name, reason="")
            return Verdict(
                passed=False, rule_name=self.name,
                reason=(
                    f"dispatch_intent names ssh_host_slug={slug!r} but "
                    "the slug is not in AKKI_GPU_HOSTS inventory"
                ),
            )
        if intent.startswith("gpu_lane:"):
            lane_id = intent[len("gpu_lane:"):]
            if not lane_id:
                return Verdict(
                    passed=False, rule_name=self.name,
                    reason="dispatch_intent gpu_lane grammar missing lane id",
                )
            return Verdict(passed=True, rule_name=self.name, reason="")
        return Verdict(
            passed=False, rule_name=self.name,
            reason=f"dispatch_intent {intent!r} does not match a known prefix",
        )


class OutputContractNamesRealKind(GovernanceRule):
    name = "output_contract_names_real_kind"

    def apply(self, manifest: JobManifest) -> Verdict:
        expected = manifest.output_contract.get("expected_kind")
        if not isinstance(expected, str):
            return Verdict(
                passed=False, rule_name=self.name,
                reason=(
                    "output_contract.expected_kind is missing or not a "
                    "string — cannot verify output"
                ),
            )
        if expected in NON_REAL_KINDS:
            return Verdict(
                passed=False, rule_name=self.name,
                reason=(
                    f"output_contract.expected_kind={expected!r} is a "
                    "non-real kind (W0 NON_REAL_KINDS) — this job would "
                    "silently succeed on any output artifact"
                ),
            )
        return Verdict(passed=True, rule_name=self.name, reason="")


# ---------------------------------------------------------------------------
# Compose helpers
# ---------------------------------------------------------------------------


def apply_rules(
    rules: List[GovernanceRule],
    manifest: JobManifest,
) -> Tuple[Verdict, ...]:
    """Apply every rule in the list and return all verdicts, in
    registration order. First-veto-wins semantics live at the CP4
    caller (admit_job wire); this helper is neutral."""
    return tuple(r.apply(manifest) for r in rules)


def _iso_now_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ledger_row_path(
    ledger_root: Path,
    job_id: str,
    manifest_fingerprint: str,
    rule_name: str,
) -> Path:
    # Filename encodes stability keys so dedupe is easy.
    fname = f"{job_id}__{manifest_fingerprint}__{rule_name}.json"
    return Path(ledger_root) / fname


def bank_verdict(
    verdict: Verdict,
    *,
    ledger_root: Path,
    job_id: str,
    manifest_fingerprint: str,
    dedupe_window_seconds: int = 60,
) -> Optional[Path]:
    """Write a ledger row for `verdict`. Idempotent within the dedupe
    window: if a row with the same (job_id, manifest_fingerprint,
    rule_name) exists and its mtime is within `dedupe_window_seconds`,
    return that row's path without writing.

    Returns None on I/O failure (zero-influence on write failure,
    consistent with campaign_infra discipline).
    """
    try:
        root = Path(ledger_root)
        row_path = _ledger_row_path(
            root, job_id, manifest_fingerprint, verdict.rule_name,
        )
        if row_path.exists():
            import time
            age = time.time() - row_path.stat().st_mtime
            if age <= dedupe_window_seconds:
                return row_path
        root.mkdir(parents=True, exist_ok=True)
        entry = RulingLedgerEntry(
            banked_at_utc=_iso_now_z(),
            verdict=verdict,
            job_id=job_id,
            manifest_fingerprint=manifest_fingerprint,
        )
        payload = {
            "banked_at_utc": entry.banked_at_utc,
            "verdict": asdict(entry.verdict),
            "job_id": entry.job_id,
            "manifest_fingerprint": entry.manifest_fingerprint,
        }
        row_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2),
            encoding="utf-8",
        )
        return row_path
    except Exception as exc:  # pragma: no cover
        log.warning("bank_verdict I/O failure (swallowed): %r", exc)
        return None


__all__ = [
    "Verdict",
    "RulingLedgerEntry",
    "GovernanceRule",
    "LicenceClassRequired",
    "DispatchIntentConfigured",
    "OutputContractNamesRealKind",
    "apply_rules",
    "bank_verdict",
]
