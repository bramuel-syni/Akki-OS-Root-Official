"""services.census_autonomy.gpu_spend_capture — real-telemetry GPU-spend
capture via sealed SSH bridge.

Owner directives (verbatim source of record):
  STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md §44:
    "NO GPU-spend fabrication. Numbers come from live host telemetry
    (akki-vm / akki-vm-ii nvidia-smi captures at run time) or the run
    is banked without a GPU-spend claim."
  STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md STOP #2:
    "If nvidia-smi telemetry is not reachable at run-time from the pod
    (SSH/network issue) STOP GPU-spend capture · honest-gap it · file
    DQ-fork; do NOT fabricate."

## Design

This module is a THIN ADAPTER over the sealed
`services.training_runner.ssh_seam` remote-execution surface. It does
NOT re-declare the SSH transport, credential handling, or the
GPU_CONNECT_MODE dispatch — it consumes them READ-ONLY (SO §3.8
sealed-carrier identity-import discipline).

### Behavioural contract

Return record shape (dict):
  { "status": <CAPTURED | HONEST_GAP_UNREACHABLE | HONEST_GAP_MOCK_MODE>,
    "captured_at_utc": <ISO-8601 string>,
    "mode": <"mock" | "real">,
    ...status-specific fields (see below) }

- **CAPTURED**: real mode + reachable ssh + successful nvidia-smi run.
  Carries `hosts_captured: list[str]` and `per_host_raw: dict` mapping
  host_slug to redacted nvidia-smi stdout. NEVER interpolates or fills
  missing values.
- **HONEST_GAP_UNREACHABLE**: real mode + at least one host unreachable
  (SSH connect error or nvidia-smi rc != 0). Carries `unreachable_hosts:
  list[str]` and `reason_per_host: dict`. NEVER carries fabricated
  telemetry.
- **HONEST_GAP_MOCK_MODE**: `GPU_CONNECT_MODE=mock` (default). No SSH
  attempted. Carries only mode marker; no numeric telemetry fields.

### Never fabricates

No `random.random`, `random.randint`, `random.choice`, no synthetic
watts / GPU-load / memory-usage values. If nvidia-smi can't be captured,
the record ONLY marks the honest gap.

### Consumed sealed surface

- `services.training_runner.ssh_seam.execute_remote_command()` — governed
  paramiko exec with redaction + ledgered receipts.
- `services.training_runner.ssh_seam.list_hosts()` — configured host
  slug enumeration.
- `services.training_runner.ssh_seam.current_mode()` / `is_mock()` /
  `is_real()` — GPU_CONNECT_MODE dispatch.

All imports identity-only per SO §3.8; the sealed carrier module is
NEVER edited by this-Commit-A.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Final, Tuple

from services.training_runner.ssh_seam import (
    current_mode,
    execute_remote_command,
    is_mock,
    list_hosts,
)

# ---------------------------------------------------------------------------
# Closed vocabulary (SO §3.10-α · Final tuple · paired-equality pinned by
# invariant 3 in tests/invariants/test_cp_census_autonomy_gpu_spend_a_triple_prime.py)
# ---------------------------------------------------------------------------

GPU_SPEND_CAPTURE_STATE_CODES: Final[Tuple[str, ...]] = (
    "CAPTURED",
    "HONEST_GAP_UNREACHABLE",
    "HONEST_GAP_MOCK_MODE",
)

# nvidia-smi query pinned as a Final constant — the same query is sent
# to every host. The query returns CSV without units so downstream banks
# the redacted stdout AS-IS with never any interpolation. Fields chosen
# per owner "live host telemetry" contract at CENSUS_PRODUCTIZATION §44.
NVIDIA_SMI_QUERY: Final[str] = (
    "nvidia-smi --query-gpu="
    "timestamp,name,index,power.draw,utilization.gpu,memory.used"
    " --format=csv,noheader"
)

# Purpose tag banked in every ssh_seam receipt for this call site (SO §3.8
# audit-trail discipline). Sealed ssh_seam writes redacted receipts to
# phase0/gpu_receipts/ for every execute_remote_command dispatch.
CAPTURE_PURPOSE: Final[str] = "census_autonomy_gpu_spend_capture"


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def capture_gpu_spend() -> Dict[str, object]:
    """Capture GPU-spend telemetry from configured hosts via sealed SSH bridge.

    Never fabricates numbers. Returns one of three status kinds per the
    closed vocabulary above. Honest-gap records STOP short of any
    numeric telemetry field.
    """
    mode = current_mode()

    # ------------------------------------------------------------------
    # Mode dispatch: mock → honest-gap; real → attempt live capture.
    # ------------------------------------------------------------------
    if is_mock():
        return {
            "status": "HONEST_GAP_MOCK_MODE",
            "captured_at_utc": _now_utc_iso(),
            "mode": mode,
            "note": (
                "GPU_CONNECT_MODE=mock — no SSH attempted; the honest-gap "
                "is banked per STOP condition #2. Flip GPU_CONNECT_MODE=real "
                "and drop SSH credentials to enable live nvidia-smi capture."
            ),
        }

    # Real mode — enumerate configured hosts + attempt live capture per host.
    hosts = list(list_hosts())
    per_host_raw: Dict[str, str] = {}
    reason_per_host: Dict[str, str] = {}

    for host_slug in hosts:
        result = execute_remote_command(
            host_slug,
            NVIDIA_SMI_QUERY,
            purpose=CAPTURE_PURPOSE,
            timeout=15,
        )
        # Sealed ssh_seam guarantees rc=-1 with error message in
        # stderr_redacted on connect failure. rc != 0 with a non-empty
        # stderr indicates nvidia-smi failure (driver absent, etc.).
        if result.rc == 0:
            per_host_raw[host_slug] = result.stdout_redacted
        else:
            reason_per_host[host_slug] = (
                f"rc={result.rc} · stderr={result.stderr_redacted}"
            )

    if reason_per_host:
        # At least one host could not be reached / query failed. Honest-gap
        # the entire capture (STOP condition #2) — never partial-fabricate.
        return {
            "status": "HONEST_GAP_UNREACHABLE",
            "captured_at_utc": _now_utc_iso(),
            "mode": mode,
            "unreachable_hosts": sorted(reason_per_host.keys()),
            "reason_per_host": reason_per_host,
            "note": (
                "One or more hosts unreachable at run-time. STOP condition #2 "
                "engaged: capture NOT partially fabricated; file DQ-fork for "
                "owner side-band."
            ),
        }

    # All hosts reachable and nvidia-smi returned rc=0 on all.
    return {
        "status": "CAPTURED",
        "captured_at_utc": _now_utc_iso(),
        "mode": mode,
        "hosts_captured": sorted(per_host_raw.keys()),
        "per_host_raw": per_host_raw,
        "query": NVIDIA_SMI_QUERY,
    }
