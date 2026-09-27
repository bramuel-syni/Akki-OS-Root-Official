"""Rebuildable native projection after the canonical envelope; no second authority."""
import fcntl
import os
from pathlib import Path
from services.handoff.contracts import attest_handoff
from services.mkondo.registry import admit_handoff
from services.northena.execution_models import Held


def configured_directory():
    value = os.environ.get("HANDOFF_CONTRACTS_DIR")
    if not value or not value.strip() or not Path(value).is_absolute():
        raise Held("HANDOFF_DIRECTORY_NOT_CONFIGURED")
    return Path(value)


def project(contract, directory):
    if configured_directory() != directory:
        raise Held("HANDOFF_DIRECTORY_CHANGED")
    try:
        directory.mkdir(parents=True, exist_ok=True)
        # Native register uses exists/write; serialize that pair across local processes.
        # This lock is metadata projection only; Ledger is still the sole authority.
        with (directory / ".execution-projection.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            path = directory / (contract.handoff_id + ".json")
            if not path.exists():
                admit_handoff(contract.model_dump(mode="json"))
            if attest_handoff(contract.handoff_id) != contract:
                raise Held("HANDOFF_PROJECTION_CONFLICT")
    except (OSError, ValueError) as exc:
        raise Held("HANDOFF_PROJECTION_UNAVAILABLE") from exc