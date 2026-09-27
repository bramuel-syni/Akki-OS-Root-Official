"""Production composition remains held until actual engine authorities are bound.

No successful doubles or caller-controlled adapter registration in this factory.
The same coordinator is assembled with contract doubles ONLY in architecture tests.
"""
from services.northena.execution_authority import ComponentAuthority
from services.northena.execution_bindings import build_coordinator
from services.northena.execution_models import Held


class ExistingAuthorityBoundary(ComponentAuthority):
    """Compatibility name; now uses real typed principal/licence resolution."""


class ExistingArtifactBoundary:
    async def verify(self, request, result, operation_key):
        raise Held("ARTIFACT_CHECKER_NOT_BOUND")
