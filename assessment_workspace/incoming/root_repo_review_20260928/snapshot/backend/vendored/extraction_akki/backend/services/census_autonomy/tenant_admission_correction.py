"""services.census_autonomy.tenant_admission_correction · owner correction §5 boundary.

Owner queued correction (2026-02-23T00:30Z · verbatim · mid-Slice-4 · banked
in STATE/DECISIONS.md at Slice-4 State Commit-B 55ab3335 · executed
here at PHASE 4 (c-v) · CP-CENSUS-TENANT-ADMISSION-CORRECTION):

    "QUEUED FOR NEXT BOUNDARY — owner correction on census tenant
    admission, do not break the current slice. Owner's words: 'the
    census results are supposed to be admitted in the tenants without
    mixing up — RMS results go into RMS tenant, DigiCow goes into
    DigiCow tenant.'

    The owner is right, and the current gating conflates two different
    controls:
    1. DAP-14 approving-authority seating gates CONTROLLED REQUESTS —
       a party asking to extract/receive data. That is what stays held
       until identity material arrives via custody (DQ-19/20).
    2. CENSUS admission is NOT a controlled request. Per the owner's
       CP-TENANT-SEPARATION order §3, data assignment is BY
       REGISTRATION: every source is bound to exactly one tenant, and
       census artefacts carry their tenant_id via akki.data
       auto-injection (census_0001/0002 → DIGICOW; Item-3 receipts →
       RMS; the §3 source map is the registry). The census is the
       estate owner's own metadata survey under the banked
       LawfulBasisAdmit — it does not need an approving authority to
       run or to land results in the owning tenant.

    CORRECTION TO EXECUTE at the next boundary (small slice, RED-first):
    - Remove RMS and DIGICOW from the census-admission exclusion:
      CENSUS_ADMITTED_TENANT_IDS (or its equivalent gate) admits all
      four tenants for CENSUS jobs specifically.
    - Bind sources per the owner's §3 map at registration: RMS ← Weego,
      USSD, Citizen Digital, Visitors (MySQL), NAS 16 channels, OBS
      google-transcripts, Razuna/Newsvault, GaussDB/Viusasa-when-creds;
      DIGICOW ← digicow_live, ndume, the Digicow AWS account (creds
      already held).
    - Census runs and their artefacts/receipts land tenant-scoped: RMS
      census results visible only in the RMS tenant, DigiCow only in
      DigiCow — the existing zero-mixing invariants (AKKI-DATA-001
      refusals, no default tenant) enforce the separation; add RED pins
      proving an RMS census run's rows are invisible to a DIGICOW
      principal and vice versa.
    - Retro-assignment: the already-banked census artefacts (Digicow
      census chapters → DIGICOW; RMS estate receipts → RMS) get their
      tenant binding per §3 verbatim — additive re-registration, no
      rewriting of sealed receipts.
    - What STAYS gated on DQ-19/20: only DAP controlled-request
      execution (approvals, extractions, standing approvals) for those
      tenants — annotate that boundary explicitly in the census
      admission module docstring.
    Bank the owner's correction verbatim as a ruling; report the fix in
    the boundary report after the current skills slice seals. Current
    slice continues uninterrupted."

## §3.8 additive-only posture (sealed carriers UNCHANGED)

This carrier is ADDITIVE. It edits ZERO sealed modules. Sealed carriers
consumed READ-ONLY:

- ``services.census_autonomy.tenant_scope`` — sealed at PHASE 3 A'
  (55ffc389). Runtime finding this-slice: its ``CENSUS_ADMITTED_
  TENANT_IDS`` filter matches nothing because sealed ``TENANT_ROLES``
  never sets ``named_but_unseated`` (that state lives on ``services.
  tenant_separation.dap_activation._ACTIVATIONS[t]["dap_14_named_
  authority"]["seat_state"]`` for DAP-14 controlled-request gating).
  Runtime already admits every canonical tenant for census — the
  correction lands as declarative pins + drift-detector on the sealed
  behaviour, not as an edit to the sealed carrier's stale comment.
- ``services.tenant_separation.tenant_registry`` — sealed at 4j
  Commit-A eed6c032. Its ``SOURCE_ROSTER`` already binds every named
  RMS + DIGICOW source per owner §3 verbatim.
- ``services.tenant_separation.dap_activation`` — sealed at 4j
  Commit-A eed6c032. RMS + DIGICOW ``dap_14_named_authority.seat_state``
  remains ``"named_but_unseated"``; DAP-14 controlled-request execution
  stays held on DQ-19/DQ-20 until custody-material drop.

## Boundary annotation (owner correction §5 verbatim)

**Census admission ≠ DAP-14 controlled-request seating.** These are two
distinct controls. This carrier PROVES the boundary declaratively:
``CENSUS_ADMITS_ALL_FOUR_CANONICAL_TENANTS`` (True) is orthogonal to
``DAP_14_CONTROLLED_REQUEST_GATING_STAYS_HELD`` (RMS, DIGICOW). DQ-19
(RMS approving authority) and DQ-20 (DIGICOW approving authority) hold
the DAP-14 gate for controlled-request execution ONLY; they do NOT
gate census jobs.

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO
§3.10-α · zero external I/O · deterministic · verbatim per SO §2.5 ·
zero push per Owner Clarification 1.
"""

from __future__ import annotations

from typing import Dict, Final, Tuple

# Sealed carriers imported READ-ONLY per SO §3.8.
from services.census_autonomy.tenant_scope import (  # noqa: E402
    CENSUS_ADMITTED_TENANT_IDS,
    is_census_admitted_tenant,
)
from services.tenant_separation.dap_activation import (  # noqa: E402
    _ACTIVATIONS,
)
from services.tenant_separation.tenant_registry import (  # noqa: E402
    CANONICAL_TENANT_IDS,
)

# ═══════════════════════════════════════════════════════════════════════════
# OWNER_CORRECTION_VERBATIM_ANCHOR — SO §2.5 machine-readable verbatim quote
# ═══════════════════════════════════════════════════════════════════════════

OWNER_CORRECTION_VERBATIM_ANCHOR: Final[str] = (
    "QUEUED FOR NEXT BOUNDARY — owner correction on census tenant "
    "admission, do not break the current slice. Owner's words: 'the "
    "census results are supposed to be admitted in the tenants "
    "without mixing up — RMS results go into RMS tenant, DigiCow "
    "goes into DigiCow tenant.'\n\n"
    "The owner is right, and the current gating conflates two "
    "different controls:\n"
    "1. DAP-14 approving-authority seating gates CONTROLLED REQUESTS "
    "— a party asking to extract/receive data. That is what stays "
    "held until identity material arrives via custody (DQ-19/20).\n"
    "2. CENSUS admission is NOT a controlled request. Per the "
    "owner's CP-TENANT-SEPARATION order §3, data assignment is BY "
    "REGISTRATION: every source is bound to exactly one tenant, and "
    "census artefacts carry their tenant_id via akki.data "
    "auto-injection (census_0001/0002 → DIGICOW; Item-3 receipts → "
    "RMS; the §3 source map is the registry). The census is the "
    "estate owner's own metadata survey under the banked "
    "LawfulBasisAdmit — it does not need an approving authority to "
    "run or to land results in the owning tenant.\n\n"
    "CORRECTION TO EXECUTE at the next boundary (small slice, "
    "RED-first):\n"
    "- Remove RMS and DIGICOW from the census-admission exclusion: "
    "CENSUS_ADMITTED_TENANT_IDS (or its equivalent gate) admits all "
    "four tenants for CENSUS jobs specifically.\n"
    "- Bind sources per the owner's §3 map at registration: RMS ← "
    "Weego, USSD, Citizen Digital, Visitors (MySQL), NAS 16 "
    "channels, OBS google-transcripts, Razuna/Newsvault, "
    "GaussDB/Viusasa-when-creds; DIGICOW ← digicow_live, ndume, the "
    "Digicow AWS account (creds already held).\n"
    "- Census runs and their artefacts/receipts land tenant-scoped: "
    "RMS census results visible only in the RMS tenant, DigiCow "
    "only in DigiCow — the existing zero-mixing invariants "
    "(AKKI-DATA-001 refusals, no default tenant) enforce the "
    "separation; add RED pins proving an RMS census run's rows are "
    "invisible to a DIGICOW principal and vice versa.\n"
    "- Retro-assignment: the already-banked census artefacts "
    "(Digicow census chapters → DIGICOW; RMS estate receipts → "
    "RMS) get their tenant binding per §3 verbatim — additive "
    "re-registration, no rewriting of sealed receipts.\n"
    "- What STAYS gated on DQ-19/20: only DAP controlled-request "
    "execution (approvals, extractions, standing approvals) for "
    "those tenants — annotate that boundary explicitly in the "
    "census admission module docstring.\n"
    "Bank the owner's correction verbatim as a ruling; report the "
    "fix in the boundary report after the current skills slice "
    "seals. Current slice continues uninterrupted."
)


# ═══════════════════════════════════════════════════════════════════════════
# Declarative posture pin — corrected census admission
# ═══════════════════════════════════════════════════════════════════════════

# Owner correction bullet 1 verbatim: "CENSUS_ADMITTED_TENANT_IDS (or its
# equivalent gate) admits all four tenants for CENSUS jobs specifically."
# On-disk runtime already satisfies this by construction (sealed filter
# matches nothing). This Final pins the corrected posture declaratively.
CENSUS_ADMITS_ALL_FOUR_CANONICAL_TENANTS: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §3 registration map — owner §3 verbatim source-to-tenant bindings
# ═══════════════════════════════════════════════════════════════════════════

# Owner §3 verbatim (from OWNER_CORRECTION_VERBATIM_ANCHOR bullet 2):
#
#   RMS ← Weego, USSD, Citizen Digital, Visitors (MySQL), NAS 16 channels,
#         OBS google-transcripts, Razuna/Newsvault, GaussDB/Viusasa-when-creds
#   DIGICOW ← digicow_live, ndume, the Digicow AWS account (creds already held)
#
# Keys are kebab_lower snake-safe canonical forms. Values are Final tuples so
# the map cannot be mutated at import site. Sealed backbone: every RMS/DIGICOW
# key below EXCEPT `gaussdb_viusasa_when_creds` + `digicow_aws_account` is
# ALREADY present in the sealed `services.tenant_separation.tenant_registry.
# SOURCE_ROSTER` at 4j; those two are named-in-map-only (creds not yet in
# custody · registration-pending · ledger presence without wiring).
CENSUS_ADMISSION_SOURCE_MAP: Final[Dict[str, Tuple[str, ...]]] = {
    "RMS": (
        "weego",
        "ussd",
        "citizen_digital",
        "visitors_mysql",
        "nas_16_channels",
        "obs_google_transcripts",
        "razuna_newsvault",
        "gaussdb_viusasa_when_creds",
    ),
    "DIGICOW": (
        "digicow_live",
        "ndume",
        "digicow_aws_account",
    ),
    # AKKI-TEST and AUDIT-FIXTURE-20260921 admit their sealed synthetic
    # / audit sources per 4j SOURCE_ROSTER (no additional §3 bindings
    # this-slice — they are unchanged from sealed backbone).
    "AKKI-TEST": ("akki_test_synthetic_pack",),
    "AUDIT-FIXTURE-20260921": ("audit_fixture_20260921_bundle",),
}


# ═══════════════════════════════════════════════════════════════════════════
# RETRO_ASSIGNMENT_RECORDS — additive re-registration per owner correction §4
# ═══════════════════════════════════════════════════════════════════════════

# Owner correction bullet 4 verbatim: "the already-banked census artefacts
# (Digicow census chapters → DIGICOW; RMS estate receipts → RMS) get their
# tenant binding per §3 verbatim — additive re-registration, no rewriting of
# sealed receipts."
#
# Every entry MUST carry kind='additive_re_registration' to make the §3.8
# discipline machine-checkable: sealed receipts are NOT rewritten; a new
# additive record binds the artefact to its owning tenant per §3.
RETRO_ASSIGNMENT_RECORDS: Final[Tuple[Dict[str, str], ...]] = (
    {
        "artefact_key": "census_0001",
        "tenant_id": "DIGICOW",
        "kind": "additive_re_registration",
        "owner_correction_anchor_bullet": "4",
        "source_family": "digicow_census_chapters",
    },
    {
        "artefact_key": "census_0002",
        "tenant_id": "DIGICOW",
        "kind": "additive_re_registration",
        "owner_correction_anchor_bullet": "4",
        "source_family": "digicow_census_chapters",
    },
    {
        "artefact_key": "rms_item_3_receipts",
        "tenant_id": "RMS",
        "kind": "additive_re_registration",
        "owner_correction_anchor_bullet": "4",
        "source_family": "rms_estate_receipts",
    },
)


# ═══════════════════════════════════════════════════════════════════════════
# DAP-14 controlled-request gating boundary annotation (owner correction §5)
# ═══════════════════════════════════════════════════════════════════════════

# Owner correction bullet 5 verbatim: "What STAYS gated on DQ-19/20: only
# DAP controlled-request execution (approvals, extractions, standing
# approvals) for those tenants."
#
# This tuple names the tenants whose DAP-14 approving-authority seating is
# held pending custody-material drop. Note: this does NOT gate census
# admission — the two controls are orthogonal by design.
DAP_14_CONTROLLED_REQUEST_GATING_STAYS_HELD: Final[Tuple[str, ...]] = (
    "RMS",       # DQ-19 · RMS approving authority · named-but-unseated
    "DIGICOW",   # DQ-20 · DIGICOW approving authority · named-but-unseated
)


# ═══════════════════════════════════════════════════════════════════════════
# Public callables — product-language wrappers
# ═══════════════════════════════════════════════════════════════════════════

def census_lawful_basis_admits(tenant_id: str) -> bool:
    """Return True iff tenant_id is admitted to run a census job.

    Product-language wrapper over the sealed
    ``services.census_autonomy.tenant_scope.is_census_admitted_tenant``.
    Every canonical tenant is admitted per owner correction bullet 1 —
    census is the estate owner's own metadata survey under the banked
    LawfulBasisAdmit and does not require an approving authority.
    Non-canonical tenant ids are refused (never fabricated).
    """
    if not isinstance(tenant_id, str) or not tenant_id.strip():
        return False
    return is_census_admitted_tenant(tenant_id)


def retro_assignment_for_artefact(artefact_key: str) -> str:
    """Return the owning tenant_id for a banked census artefact.

    Reads the additive ``RETRO_ASSIGNMENT_RECORDS`` map. Unknown keys
    raise ``KeyError`` — never fabricate a tenant binding.

    Owner correction bullet 4 verbatim: additive re-registration, no
    rewriting of sealed receipts.
    """
    for record in RETRO_ASSIGNMENT_RECORDS:
        if record["artefact_key"] == artefact_key:
            return record["tenant_id"]
    raise KeyError(
        f"artefact_key {artefact_key!r} has no additive re-registration "
        f"record; RETRO_ASSIGNMENT_RECORDS covers only banked census "
        f"artefacts listed in owner correction bullet 4"
    )


def is_census_admission_orthogonal_to_dap_14_seating() -> bool:
    """Structural assertion: census admission and DAP-14 seating are
    two distinct controls (owner correction bullet 5 boundary).

    Returns True iff every tenant listed in
    ``DAP_14_CONTROLLED_REQUEST_GATING_STAYS_HELD`` is SIMULTANEOUSLY
    census-admitted AND held at DAP-14 seat_state
    ``"named_but_unseated"``. Orthogonality proof: the two controls
    disagree on those tenants by design — census OK, DAP-14 held.
    """
    for tenant_id in DAP_14_CONTROLLED_REQUEST_GATING_STAYS_HELD:
        # (a) Must be census-admitted (owner correction bullet 1).
        if not is_census_admitted_tenant(tenant_id):
            return False
        # (b) DAP-14 seat MUST still be held (owner correction bullet 5).
        activation = _ACTIVATIONS.get(tenant_id, {})
        seat_state = (
            activation.get("dap_14_named_authority", {}).get("seat_state")
        )
        if seat_state != "named_but_unseated":
            return False
    # (c) Corrected posture pin agrees.
    if not CENSUS_ADMITS_ALL_FOUR_CANONICAL_TENANTS:
        return False
    # (d) Runtime drift-detector: sealed carriers agree with the pin.
    if tuple(sorted(CENSUS_ADMITTED_TENANT_IDS)) != tuple(
        sorted(CANONICAL_TENANT_IDS)
    ):
        return False
    return True


__all__ = (
    "OWNER_CORRECTION_VERBATIM_ANCHOR",
    "CENSUS_ADMITS_ALL_FOUR_CANONICAL_TENANTS",
    "CENSUS_ADMISSION_SOURCE_MAP",
    "RETRO_ASSIGNMENT_RECORDS",
    "DAP_14_CONTROLLED_REQUEST_GATING_STAYS_HELD",
    "census_lawful_basis_admits",
    "retro_assignment_for_artefact",
    "is_census_admission_orthogonal_to_dap_14_seating",
)
