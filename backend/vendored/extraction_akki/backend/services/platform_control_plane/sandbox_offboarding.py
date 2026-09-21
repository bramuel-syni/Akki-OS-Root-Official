"""Platform-layer sandbox offboarding evidence carrier + refusal.

CP-P6-CP5 · M9 · SANDBOX-OFFBOARDING.

Anchor: PLATFORM_LAYER_REQUIREMENTS_v0_2.md §4.7 (tenant lifecycle terminal state
`offboarded`) + Row 210 verbatim.

Verbatim Row 210: "P6-CP5 · SANDBOX-OFFBOARDING · services/platform_control_plane/
sandbox_offboarding.py · 30-day irreversible-delete contract; refusal on missing
cert-revocation / allocation-return / artefact-delete evidence refs."

CONTRACT-MODELED item 12 (from §8 of the requirements doc): "30-day irreversible
offboarding delete" · depends on "Real storage + wall-clock scheduler" · this CP
holds the evidence-refs carrier + missing-evidence refusal · concrete storage-
object-list-after-delete assertion + wall-clock 30-day countdown are downstream
bind-only work.

Standing lines: no biometric material · no enforcement hard-gate (preventive-
charter · caller invokes) · synthetic fixtures · no speculative shapes · zero
closed enum type · zero domain tokens · zero data-plane imports.

Composition: caller invokes `assert_sandbox_offboarding_valid` only when the
tenant transitions INTO `offboarded` per CP-P1-CP6 TenantLifecycleFSM
`assert_transition_valid`. Deletion is treated as irreversible (Row 210 verbatim
"irreversible-delete contract") — once committed_at is populated, the caller is
responsible for enforcing that the underlying storage/allocation/cert artefacts
are actually gone. This carrier only refuses on missing evidence refs; the real
30-day wall-clock scheduler + storage-object-list-after-delete assertion are
CONTRACT-MODELED at caller.
"""

from dataclasses import dataclass


SANDBOX_OFFBOARDING_ANCHOR = (
    "§4.7 tenant lifecycle terminal state `offboarded` · Row 210 verbatim: "
    "30-day irreversible-delete contract; refusal on missing cert-revocation / "
    "allocation-return / artefact-delete evidence refs. "
    "CONTRACT-MODELED item 12 (Real storage + wall-clock scheduler) shape-frozen: "
    "the three evidence refs (cert-revocation · allocation-return · artefact-delete) "
    "are OPEN str carriers; real storage/scheduler wiring is a bind-only change."
)


SANDBOX_OFFBOARDING_RECORD_FIELDS = (
    "id",
    "tenant_id",
    "cert_revocation_ref",
    "allocation_return_ref",
    "artefact_delete_ref",
    "initiated_at",
    "committed_at",
)


@dataclass(frozen=True)
class SandboxOffboardingRecord:
    """Frozen 7-carrier for a sandbox offboarding record.

    Fields (all str OPEN per case-agnostic doctrine):
      - id: opaque offboarding record id
      - tenant_id: owning tenant (ownership isolation at index 1)
      - cert_revocation_ref: opaque ref to cert-revocation evidence artefact
      - allocation_return_ref: opaque ref to allocation-return evidence artefact
      - artefact_delete_ref: opaque ref to artefact-delete evidence artefact
      - initiated_at: ISO-8601 UTC 'Z' timestamp when offboarding was initiated
      - committed_at: ISO-8601 UTC 'Z' timestamp when the 30-day irreversible
        point-of-no-return was crossed (empty-string convention if not yet
        committed)

    Empty-string convention: an evidence ref that is `""` (empty str) is treated
    as MISSING; a non-empty str value satisfies the presence requirement.
    """

    id: str
    tenant_id: str
    cert_revocation_ref: str
    allocation_return_ref: str
    artefact_delete_ref: str
    initiated_at: str
    committed_at: str


class SandboxOffboardingRefused(Exception):
    """Root refusal for sandbox offboarding evidence validation."""


class MissingCertRevocationEvidenceRefused(SandboxOffboardingRefused):
    """cert_revocation_ref is empty · fires FIRST in refusal order."""


class MissingAllocationReturnEvidenceRefused(SandboxOffboardingRefused):
    """allocation_return_ref is empty · fires SECOND (after cert-revocation)."""


class MissingArtefactDeleteEvidenceRefused(SandboxOffboardingRefused):
    """artefact_delete_ref is empty · fires THIRD (after cert + allocation)."""


def assert_sandbox_offboarding_valid(*, record: SandboxOffboardingRecord) -> None:
    """Preventive-charter refusal wrapper for sandbox offboarding evidence.

    Refusal order (fail-fast, positional):
      1. cert_revocation_ref empty → MissingCertRevocationEvidenceRefused
      2. allocation_return_ref empty → MissingAllocationReturnEvidenceRefused
      3. artefact_delete_ref empty → MissingArtefactDeleteEvidenceRefused

    Returns None on admit.

    COUNTS-only refusal messages: no field values / tenant_id / evidence-ref
    content leaks into exception bodies. Positional-index-only.
    """
    # Refusal 1: cert-revocation evidence
    if not record.cert_revocation_ref:
        raise MissingCertRevocationEvidenceRefused(
            "sandbox offboarding refused: missing evidence ref at position 2"
        )

    # Refusal 2: allocation-return evidence
    if not record.allocation_return_ref:
        raise MissingAllocationReturnEvidenceRefused(
            "sandbox offboarding refused: missing evidence ref at position 3"
        )

    # Refusal 3: artefact-delete evidence
    if not record.artefact_delete_ref:
        raise MissingArtefactDeleteEvidenceRefused(
            "sandbox offboarding refused: missing evidence ref at position 4"
        )

    return None
