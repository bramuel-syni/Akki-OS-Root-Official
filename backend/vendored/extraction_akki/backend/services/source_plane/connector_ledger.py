"""services.source_plane.connector_ledger — W-CONN-SP1.

Rights-at-setup governance ledger for the estate's source-plane
connectors.  Every record carries the owner's 2026-09-14 full-rights
ruling verbatim; silent removal / silent addition fires a mechanical
RED against the invariant tests.

Canon anchors baked in:

  * RIGHTS_AT_SETUP_VERBATIM — owner's 2026-09-14 full-rights ruling.
  * CREDENTIAL_ROTATION_PENDING_MARKER — owner's 2026-09-14 ruling:
    rotation happens AFTER connection is established.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Literal, Optional, Tuple


RIGHTS_AT_SETUP_VERBATIM: str = (
    "Owner ruling verbatim 2026-09-14: 'these are file labels but no "
    "confidential information. We have full rights on this data.'"
)

CREDENTIAL_ROTATION_PENDING_MARKER: str = (
    "Owner ruling verbatim 2026-09-14: 'rotation happens AFTER connection "
    "is established'."
)


ConnectorReachability = Literal["PASS", "HARD_GAP", "OWNER_HOLD"]


@dataclass(frozen=True)
class SourceConnector:
    """One connector in the source-plane ledger.

    * `rights_at_setup_basis` MUST equal RIGHTS_AT_SETUP_VERBATIM.
    * `evidence_receipts` names the phase0/connectivity_receipts/*.json
      files that back the reachability status.
    * `missing_bind_detail` is required (non-empty) iff reachability
      is HARD_GAP.
    * `credential_rotation_pending_after_setup` is True iff the PASS
      was obtained using an as-yet-unrotated credential (SEC-T4 items).
    """

    name: str
    protocol: str
    endpoint_shape: str
    reachability: ConnectorReachability
    rights_at_setup_basis: str
    evidence_receipts: Tuple[str, ...] = field(default_factory=tuple)
    missing_bind_detail: Optional[str] = None
    used_unrotated_credential: bool = False
    credential_rotation_pending_after_setup: bool = False


class LedgerRightsError(RuntimeError):
    """Rights-basis missing or drifted on a ledger record."""


def assert_rights_at_setup_present(record: dict) -> None:
    """Every record MUST carry the verbatim rights-at-setup basis."""
    if record.get("rights_at_setup_basis") != RIGHTS_AT_SETUP_VERBATIM:
        raise LedgerRightsError(
            f"connector {record.get('name')!r} rights-basis missing or "
            f"drifted from RIGHTS_AT_SETUP_VERBATIM"
        )


def _rec(**kwargs) -> dict:
    """Construct a ledger record with rights-basis auto-populated."""
    rec = SourceConnector(
        rights_at_setup_basis=RIGHTS_AT_SETUP_VERBATIM,
        **kwargs,
    )
    return asdict(rec)


# ---------------------------------------------------------------------------
# The ledger — 2026-09-14 connectivity findings encoded as records.
# ---------------------------------------------------------------------------

CONNECTOR_LEDGER: List[dict] = [
    _rec(
        name="jump.bastion",
        protocol="ssh",
        endpoint_shape="159.138.173.250/22",
        reachability="PASS",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T094725Z_T2A_jump_preflight.json",
            "phase0/connectivity_receipts/20260914T094804Z_T3_jump_auth_handshake.json",
            "phase0/connectivity_receipts/20260914T112858Z_JUMP_PREFLIGHT_admin_guided.json",
        ),
        used_unrotated_credential=True,
        credential_rotation_pending_after_setup=True,
    ),
    _rec(
        name="ssh.radio_news",
        protocol="ssh",
        endpoint_shape="10.10.19.40/22",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T094840Z_T4_radio_auth_handshake_via_jump_FAIL.json",
            "phase0/connectivity_receipts/20260914T094927Z_T4b_radio_reachability_from_jump.json",
            "phase0/connectivity_receipts/20260914T113331Z_JUMP_full_ssh_sweep.json",
        ),
        missing_bind_detail=(
            "RADIO subnet 10.10.19.0/24 unreachable from JUMP (10.10.150.0/24) "
            "even with correct credentials from the 2026-09-14 admin sheet — "
            "full /24 tcp/22 sweep returned zero opens on 10.10.19.*. JUMP's "
            "default gateway routes 10.10.55.0/24 (NAS reachable) but not "
            "10.10.19.0/24.  Need: JUMP-side route to 10.10.19.0/24 OR VPC "
            "peering / security-group opening OR an alternate RADIO host."
        ),
    ),
    _rec(
        name="ssh.transcription",
        protocol="ssh",
        endpoint_shape="unknown",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113255Z_JUMP_ssh_sweep_for_radio_transcription.json",
            "phase0/connectivity_receipts/20260914T113331Z_JUMP_full_ssh_sweep.json",
            "phase0/connectivity_receipts/20260914T113420Z_JUMP_ssh_probe_to_nas_and_gw.json",
        ),
        missing_bind_detail=(
            "Transcription-server host + credentials not in the 2026-09-14 "
            "admin sheet.  Only two SSH endpoints reachable in the "
            "10.10.55.0/24 subnet (10.10.55.1 gateway + 10.10.55.55 NAS) — "
            "both refuse Bramwel/NAS creds and ubuntu/RADIO creds.  Need: "
            "Transcription server host + username + password/key OR "
            "confirmation Transcription runs on NAS with a different account."
        ),
    ),
    _rec(
        name="mysql.viusasa",
        protocol="mysql",
        endpoint_shape="203.123.86.10/3306",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
        ),
        missing_bind_detail=(
            "203.123.86.10:3306 CLOSED from JUMP (RMS/Kenya ISP IP; likely "
            "on-prem MySQL behind private firewall).  Sheet has creds but "
            "no route to reach the port.  Need: security-group opening for "
            "JUMP source IP, OR alternate reachable host."
        ),
    ),
    _rec(
        name="mysql.ussd",
        protocol="mysql",
        endpoint_shape="110.238.76.159/3306",
        reachability="PASS",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
            "phase0/connectivity_receipts/20260914T113521Z_JUMP_mysql_auth_reachable_hosts.json",
        ),
        used_unrotated_credential=True,
        credential_rotation_pending_after_setup=True,
    ),
    _rec(
        name="mysql.microservices",
        protocol="mysql",
        endpoint_shape="159.138.164.93/3306",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
        ),
        missing_bind_detail=(
            "159.138.164.93:3306 CLOSED from JUMP (same Huawei VPC region as "
            "reachable WEEGO/USSD but blocked at security-group).  Need: "
            "security-group opening for JUMP source IP."
        ),
    ),
    _rec(
        name="mysql.weego",
        protocol="mysql",
        endpoint_shape="159.138.162.146/3306",
        reachability="PASS",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
            "phase0/connectivity_receipts/20260914T113521Z_JUMP_mysql_auth_reachable_hosts.json",
        ),
        used_unrotated_credential=True,
        credential_rotation_pending_after_setup=True,
    ),
    _rec(
        name="mysql.citizen_digital",
        protocol="mysql",
        endpoint_shape="159.138.164.124/3306",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
        ),
        missing_bind_detail=(
            "159.138.164.124:3306 CLOSED from JUMP.  Same Huawei VPC region "
            "as reachable hosts; security-group opening required."
        ),
    ),
    _rec(
        name="mysql.visitors",
        protocol="mysql",
        endpoint_shape="110.238.75.83/3306",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
        ),
        missing_bind_detail=(
            "110.238.75.83:3306 CLOSED from JUMP.  Same VPC region as "
            "reachable hosts; security-group opening required."
        ),
    ),
    _rec(
        name="mysql.shikisha",
        protocol="mysql",
        endpoint_shape="203.123.83.144/3306",
        reachability="HARD_GAP",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T113456Z_JUMP_mysql_tcp_sweep.json",
        ),
        missing_bind_detail=(
            "203.123.83.144:3306 CLOSED from JUMP (RMS/Kenya ISP IP; on-prem "
            "MySQL).  Need: security-group opening for JUMP source IP OR "
            "alternate reachable host."
        ),
    ),
    _rec(
        name="huawei.obs",
        protocol="s3-compatible",
        endpoint_shape="obs.<region>.myhuaweicloud.com/443",
        reachability="PASS",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T095044Z_T7_obs_list_buckets.json",
            "phase0/connectivity_receipts/20260914T095148Z_T7c_obs_bounded_content_read.json",
            "phase0/connectivity_receipts/20260914T095209Z_T7d_obs_content_read_bounded.json",
        ),
        used_unrotated_credential=True,
        credential_rotation_pending_after_setup=True,
    ),
    _rec(
        name="smb.synology_nas",
        protocol="cifs/smb",
        endpoint_shape="10.10.55.55/445",
        reachability="PASS",
        evidence_receipts=(
            "phase0/connectivity_receipts/20260914T112858Z_JUMP_PREFLIGHT_admin_guided.json",
            "phase0/connectivity_receipts/20260914T112945Z_JUMP_INSTALL_cifs_utils_smbclient.json",
            "phase0/connectivity_receipts/20260914T113010Z_NAS_list_shares_from_jump.json",
            "phase0/connectivity_receipts/20260914T113109Z_NAS_share_access_survey.json",
            "phase0/connectivity_receipts/20260914T113131Z_NAS_offairrecs_record_layout.json",
            "phase0/connectivity_receipts/20260914T113154Z_NAS_channel_layout.json",
            "phase0/connectivity_receipts/20260914T113225Z_NAS_bounded_content_read_proof.json",
        ),
        used_unrotated_credential=True,
        credential_rotation_pending_after_setup=True,
    ),
]


ADMIN_TOPOLOGY_REQUIRED_CONNECTORS: Tuple[str, ...] = (
    "jump.bastion",
    "ssh.radio_news",
    "ssh.transcription",
    "mysql.weego",       # Huawei "already proven"
    "huawei.obs",
    "smb.synology_nas",
)


def get_ledger() -> Tuple[dict, ...]:
    return tuple(CONNECTOR_LEDGER)


def assert_ledger_covers_admin_topology() -> None:
    """Ledger MUST cover every admin-declared connector."""
    names = {r["name"] for r in CONNECTOR_LEDGER}
    missing = [n for n in ADMIN_TOPOLOGY_REQUIRED_CONNECTORS if n not in names]
    if missing:
        raise LedgerRightsError(
            f"admin topology connectors missing from ledger: {missing!r}"
        )


__all__ = [
    "RIGHTS_AT_SETUP_VERBATIM",
    "CREDENTIAL_ROTATION_PENDING_MARKER",
    "ConnectorReachability",
    "SourceConnector",
    "LedgerRightsError",
    "CONNECTOR_LEDGER",
    "ADMIN_TOPOLOGY_REQUIRED_CONNECTORS",
    "get_ledger",
    "assert_rights_at_setup_present",
    "assert_ledger_covers_admin_topology",
]
