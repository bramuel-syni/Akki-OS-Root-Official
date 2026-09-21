"""W-DAP-STACK 2E · DAP-25 fail-closed operation availability.

Verbatim DAP-25: 'An estate owner configures, per custody class and per
operation, whether that operation is available at all, available on
approval, or available under standing terms.  The default for every
combination is unavailable — availability is granted, never assumed.'
"""

from __future__ import annotations

from typing import Dict, Tuple

from contracts.dap import OperationAvailability


# The fail-closed default surface — every combination is UNAVAILABLE
# until an owner grants it.  Silent flip forbidden by DAP-25 verbatim.
AVAILABILITY_DEFAULT_UNAVAILABLE: OperationAvailability = (
    OperationAvailability.UNAVAILABLE
)


_config: Dict[Tuple[str, str, str], OperationAvailability] = {}
# key: (estate_id, custody_class, operation)


def configure_availability(
    *,
    estate_id: str,
    custody_class: str,
    operation: str,
    availability: OperationAvailability,
) -> None:
    _config[(estate_id, custody_class, operation)] = availability


def is_available(
    *, estate_id: str, custody_class: str, operation: str,
) -> OperationAvailability:
    """DAP-25: fail-closed — return UNAVAILABLE unless owner-granted."""
    return _config.get(
        (estate_id, custody_class, operation),
        AVAILABILITY_DEFAULT_UNAVAILABLE,
    )


def reset_state() -> None:
    """Test-only helper."""
    _config.clear()
