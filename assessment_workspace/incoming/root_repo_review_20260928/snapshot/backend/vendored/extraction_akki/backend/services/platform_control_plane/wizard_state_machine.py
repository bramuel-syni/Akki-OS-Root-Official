"""services.platform_control_plane.wizard_state_machine — CP-P5-CP4 · M9.

Preventive-charter wizard state machine per Akki OS Pilot Platform
Reference v0.2 §8:

    §8.1 M-W-1 verbatim: Wizard produces a provisioned sandbox
        tenant and a provisioning report. Drafts saveable +
        resumable for 30 days.
    §8.2 M-W-2 verbatim: 9-step ordered wizard:
        Company → Identity → Estates → Connectors → Compute →
        Apps → Theme → Workspaces/Users → Review/Provision.

Vocabulary (§8.2 verbatim step order):
- WIZARD_STEPS = 9-tuple in exact source order.
- WIZARD_MAX_DRAFT_DAYS = 30 (§8.1 verbatim).
- WIZARD_OUTPUT_ENVIRONMENT = "sandbox" (§8.1 verbatim).

Refusals:
- Unknown step name → UnknownWizardStepRefused
- Non-sequential transition → NonSequentialProgressionRefused
- Draft age > 30d → DraftExpiredRefused
- Output env != "sandbox" → WrongProvisionedEnvironmentRefused

Numeric parsing of draft_age_days is CONTRACT-MODELED at caller.

Standing-line proof:
- Pure functions · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple


WIZARD_STATE_MACHINE_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §8.1 "
    "M-W-1 verbatim: Wizard produces a provisioned sandbox tenant "
    "and a provisioning report. Drafts saveable + resumable for 30 "
    "days. §8.2 M-W-2 verbatim: 9-step ordered wizard: Company → "
    "Identity → Estates → Connectors → Compute → Apps → Theme → "
    "Workspaces/Users → Review/Provision."
)


# §8.2 verbatim 9-step order · OPEN str · case-sensitive.
WIZARD_STEPS: Tuple[str, ...] = (
    "Company",
    "Identity",
    "Estates",
    "Connectors",
    "Compute",
    "Apps",
    "Theme",
    "Workspaces/Users",
    "Review/Provision",
)


# §8.1 verbatim numeric floor.
WIZARD_MAX_DRAFT_DAYS: int = 30


# §8.1 verbatim: "provisioned sandbox tenant".
WIZARD_OUTPUT_ENVIRONMENT: str = "sandbox"


class WizardStateMachineRefused(Exception):
    """Root refusal for wizard-state-machine invariants."""


class UnknownWizardStepRefused(WizardStateMachineRefused):
    """Refused: step name not in WIZARD_STEPS (case-sensitive)."""


class NonSequentialProgressionRefused(WizardStateMachineRefused):
    """Refused: next_step is not the immediate successor of
    current_step (§8.2 verbatim 'ordered')."""


class DraftExpiredRefused(WizardStateMachineRefused):
    """Refused: draft age exceeds WIZARD_MAX_DRAFT_DAYS (§8.1)."""


class WrongProvisionedEnvironmentRefused(WizardStateMachineRefused):
    """Refused: provisioned environment is not WIZARD_OUTPUT_ENVIRONMENT
    (§8.1 verbatim 'sandbox tenant')."""


def step_ordinal(*, step_name: str) -> int:
    """Return the ordinal (0..8) of step_name in WIZARD_STEPS.

    Raises UnknownWizardStepRefused when step_name is not among the
    9 verbatim steps (case-sensitive)."""
    if step_name not in WIZARD_STEPS:
        raise UnknownWizardStepRefused(
            f"unknown-wizard-step refused: step_name not among "
            f"{len(WIZARD_STEPS)} §8.2 steps (case-sensitive)."
        )
    return WIZARD_STEPS.index(step_name)


def assert_transition_admissible(
    *, current_step: str, next_step: str,
) -> None:
    """Preventive-charter refusal wrapper for a wizard transition.

    Refusal order (fail fast):
    1. current_step or next_step not in WIZARD_STEPS →
       UnknownWizardStepRefused (bubbled from step_ordinal).
    2. step_ordinal(next_step) != step_ordinal(current_step) + 1 →
       NonSequentialProgressionRefused.

    Returns None on admit (forward-by-one only)."""
    cur = step_ordinal(step_name=current_step)
    nxt = step_ordinal(step_name=next_step)
    if nxt != cur + 1:
        raise NonSequentialProgressionRefused(
            f"non-sequential-progression refused: next_step is not "
            f"the immediate successor of current_step · §8.2 ordered."
        )
    return None


def assert_draft_within_ttl(*, draft_age_days: int) -> None:
    """Preventive-charter refusal for draft TTL.

    Refuses DraftExpiredRefused when draft_age_days >
    WIZARD_MAX_DRAFT_DAYS. Returns None on admit (equal-to boundary
    admits)."""
    if draft_age_days > WIZARD_MAX_DRAFT_DAYS:
        raise DraftExpiredRefused(
            f"draft-expired refused: draft age exceeds "
            f"{WIZARD_MAX_DRAFT_DAYS}-day §8.1 ceiling."
        )
    return None


def assert_provisioned_environment_valid(
    *, provisioned_environment: str,
) -> None:
    """Preventive-charter refusal for provisioned environment.

    Refuses WrongProvisionedEnvironmentRefused when
    provisioned_environment != WIZARD_OUTPUT_ENVIRONMENT (case-
    sensitive). Returns None on admit."""
    if provisioned_environment != WIZARD_OUTPUT_ENVIRONMENT:
        raise WrongProvisionedEnvironmentRefused(
            f"wrong-provisioned-environment refused: expected "
            f"WIZARD_OUTPUT_ENVIRONMENT · §8.1 sandbox-only output."
        )
    return None


__all__ = [
    "WIZARD_STATE_MACHINE_ANCHOR",
    "WIZARD_STEPS",
    "WIZARD_MAX_DRAFT_DAYS",
    "WIZARD_OUTPUT_ENVIRONMENT",
    "WizardStateMachineRefused",
    "UnknownWizardStepRefused",
    "NonSequentialProgressionRefused",
    "DraftExpiredRefused",
    "WrongProvisionedEnvironmentRefused",
    "step_ordinal",
    "assert_transition_admissible",
    "assert_draft_within_ttl",
    "assert_provisioned_environment_valid",
]
