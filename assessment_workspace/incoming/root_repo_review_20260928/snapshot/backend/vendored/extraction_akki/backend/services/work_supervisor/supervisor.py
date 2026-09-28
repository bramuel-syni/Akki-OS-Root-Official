"""services.work_supervisor.supervisor — W1 · CP2 · admission-time supervisor.

Contract:
  admit_job(m: JobManifest, *, admitted_registry: dict[str, bool] | None
                = None) -> AdmissionVerdict
  plan_next(manifests: list[JobManifest], *,
            admitted_registry: dict[str, bool] | None = None)
                -> Plan | None
  AdmissionVerdict (dataclass): admitted, refusal, plan
  Plan (dataclass): job_id, dispatch_intent, run_dir_hint,
                    expected_output_kind
  SupervisorRefusal(ValueError): kind + rule_name + message

Refusal kinds (closed enum, v0):
  precondition_seal_missing
  precondition_seal_not_real
  precondition_seal_wrong_kind
  depends_on_unresolved
  dispatch_intent_not_configured
  job_kind_not_registered
  governance_veto        (owner-reserved for CP4 compose — this module
                          does not raise it in isolation)

Composes over services.output_verified_seal (W0 primitive) so silent-
success ban is inherited. Zero-influence: pure admission, no I/O
other than reading precondition seal files.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

from services.output_verified_seal import is_real_seal, parse_seal
from services.work_supervisor.job_manifest import JobManifest

if TYPE_CHECKING:
    from services.work_supervisor.governance import GovernanceRule


class SupervisorRefusal(ValueError):
    """Refusal from the admission supervisor. Carries `kind` (closed
    enum) + optional `rule_name` (populated by CP4 governance compose)
    + human-readable `message`."""

    def __init__(self, *, kind: str, message: str,
                 rule_name: Optional[str] = None) -> None:
        self.kind = kind
        self.rule_name = rule_name
        self.message = message
        super().__init__(f"{kind}: {message}")


@dataclass(frozen=True)
class Plan:
    """A plan the runtime supervisor (CP2b) can hand to a dispatcher.

    W1 does NOT include an actual dispatch surface — the plan is a
    data carrier. `run_dir_hint` is where the output_verified_seal is
    expected to eventually appear; `expected_output_kind` is the Kind
    the runtime supervisor will assert on completion."""
    job_id: str
    dispatch_intent: str
    run_dir_hint: str
    expected_output_kind: str


@dataclass
class AdmissionVerdict:
    admitted: bool
    plan: Optional[Plan] = None
    refusal: Optional[SupervisorRefusal] = None


def _configured_host_slugs() -> tuple[str, ...]:
    raw = os.environ.get("AKKI_GPU_HOSTS", "")
    return tuple(s.strip() for s in raw.split(",") if s.strip())


def _dispatch_configured(dispatch_intent: str) -> bool:
    if dispatch_intent == "local":
        return True
    if dispatch_intent.startswith("ssh_host_slug:"):
        slug = dispatch_intent[len("ssh_host_slug:"):]
        return slug in _configured_host_slugs()
    if dispatch_intent.startswith("gpu_lane:"):
        # gpu_lane grammar is admitted if there is a lane id;
        # per-lane configuration is a downstream wave concern.
        return len(dispatch_intent[len("gpu_lane:"):]) > 0
    return False


def _precondition_verdict(
    seals: List[Dict[str, str]],
) -> Optional[SupervisorRefusal]:
    for entry in seals:
        run_dir = Path(entry["run_dir"])
        expected = entry["expected_kind"]

        parsed = parse_seal(run_dir)
        if parsed is None:
            # Two sub-cases: seal file absent → missing; file exists
            # but no Kind: line → not-real (W0 silent-success attack).
            # Distinguish for the caller so the refusal is informative.
            from services.output_verified_seal import SEALING_FILENAME
            seal_path = run_dir / SEALING_FILENAME
            if not run_dir.exists() or not seal_path.exists():
                # Try case-insensitive.
                found = False
                if run_dir.exists() and run_dir.is_dir():
                    target = SEALING_FILENAME.lower()
                    for e in run_dir.iterdir():
                        if e.is_file() and e.name.lower() == target:
                            found = True
                            break
                if not found:
                    return SupervisorRefusal(
                        kind="precondition_seal_missing",
                        message=(
                            f"precondition seal at {run_dir} is absent"
                        ),
                    )
            # File exists but parse_seal returned None → no Kind: line.
            return SupervisorRefusal(
                kind="precondition_seal_not_real",
                message=(
                    f"seal at {run_dir} exists but carries no `Kind:` "
                    "line (W0 silent-success ban inherited)"
                ),
            )
        # Parsed. Check the kind matches expected AND is real.
        if not is_real_seal(run_dir):
            return SupervisorRefusal(
                kind="precondition_seal_not_real",
                message=(
                    f"seal at {run_dir} carries a banned Kind "
                    f"({parsed.get('kind')!r})"
                ),
            )
        if parsed.get("kind") != expected:
            return SupervisorRefusal(
                kind="precondition_seal_wrong_kind",
                message=(
                    f"seal at {run_dir} has Kind={parsed.get('kind')!r} "
                    f"but manifest expected {expected!r}"
                ),
            )
    return None


def admit_job(
    manifest: JobManifest,
    *,
    admitted_registry: Optional[Dict[str, bool]] = None,
) -> AdmissionVerdict:
    """Decide whether a JobManifest is admittable.

    Returns AdmissionVerdict. On refusal the `refusal` field carries a
    SupervisorRefusal with a `kind` from the closed refusal enum.

    Zero-influence: pure — no writes, no subprocess, no network.
    """
    admitted_registry = admitted_registry or {}

    # 1. depends_on: every declared upstream must be admitted already.
    unresolved = [d for d in manifest.depends_on
                  if not admitted_registry.get(d)]
    if unresolved:
        return AdmissionVerdict(
            admitted=False,
            refusal=SupervisorRefusal(
                kind="depends_on_unresolved",
                message=(
                    f"depends_on {unresolved!r} not yet admitted for "
                    f"job {manifest.job_id!r}"
                ),
            ),
        )

    # 2. dispatch_intent must be configured.
    if not _dispatch_configured(manifest.dispatch_intent):
        return AdmissionVerdict(
            admitted=False,
            refusal=SupervisorRefusal(
                kind="dispatch_intent_not_configured",
                message=(
                    f"dispatch_intent {manifest.dispatch_intent!r} for "
                    f"job {manifest.job_id!r} names a host/lane not "
                    "present in the pod's inventory"
                ),
            ),
        )

    # 3. precondition seals — each must be real AND match expected_kind.
    seal_refusal = _precondition_verdict(manifest.precondition_seals)
    if seal_refusal is not None:
        return AdmissionVerdict(admitted=False, refusal=seal_refusal)

    # Admitted.
    expected_output_kind = str(
        manifest.output_contract.get("expected_kind", "")
    )
    plan = Plan(
        job_id=manifest.job_id,
        dispatch_intent=manifest.dispatch_intent,
        # run_dir_hint is opaque to the platform — downstream waves
        # (Part-B mounts) can override via scope. For W1 we pass an
        # empty string (the runtime supervisor will refuse to run
        # with an empty hint, so callers must supply one via scope).
        run_dir_hint=str(manifest.scope.get("run_dir_hint", "")),
        expected_output_kind=expected_output_kind,
    )
    return AdmissionVerdict(admitted=True, plan=plan)


def plan_next(
    manifests: List[JobManifest],
    *,
    admitted_registry: Optional[Dict[str, bool]] = None,
) -> Optional[Plan]:
    """Iterate manifests in list order; return the first admittable
    plan. Skips refused manifests. Returns None if none admit."""
    for m in manifests:
        v = admit_job(m, admitted_registry=admitted_registry)
        if v.admitted and v.plan is not None:
            return v.plan
    return None


def _manifest_fingerprint(manifest: JobManifest) -> str:
    """Deterministic short hash for ledger dedupe."""
    import hashlib
    import json as _json
    payload = manifest.model_dump()
    return hashlib.sha256(
        _json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()[:16]


def admit_job_with_governance(
    manifest: JobManifest,
    *,
    rules: List["GovernanceRule"],
    ledger_root: Path,
    admitted_registry: Optional[Dict[str, bool]] = None,
) -> AdmissionVerdict:
    """CP4 compose · governance rules first, then admit_job gates.

    Semantics:
      - Apply rules in list order. On first Verdict.passed=False:
          bank a ledger row via governance.bank_verdict,
          return AdmissionVerdict(admitted=False, refusal=
              SupervisorRefusal(kind='governance_veto',
                                rule_name=<the vetoing rule>,
                                message=<verdict.reason>)).
      - If every rule passes, delegate to admit_job(manifest,
        admitted_registry=...) — which applies precondition_seal /
        depends_on / dispatch_intent_configured gates in that order.

    Zero-influence: no dispatch, no process spawn. Only writes to
    ledger_root on veto (best-effort).
    """
    from services.work_supervisor.governance import bank_verdict
    fingerprint = _manifest_fingerprint(manifest)
    for rule in rules:
        verdict = rule.apply(manifest)
        if not verdict.passed:
            bank_verdict(
                verdict,
                ledger_root=ledger_root,
                job_id=manifest.job_id,
                manifest_fingerprint=fingerprint,
            )
            return AdmissionVerdict(
                admitted=False,
                refusal=SupervisorRefusal(
                    kind="governance_veto",
                    rule_name=verdict.rule_name,
                    message=verdict.reason,
                ),
            )
    return admit_job(manifest, admitted_registry=admitted_registry)


__all__ = [
    "SupervisorRefusal",
    "AdmissionVerdict",
    "Plan",
    "admit_job",
    "plan_next",
    "admit_job_with_governance",
]
