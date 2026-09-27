"""Production composition remains held until actual engine authorities are bound.

No successful doubles or caller-controlled adapter registration in this factory.
The same coordinator is assembled with contract doubles ONLY in architecture tests.
"""
from services.northena.execution_coordinator import Coordinator
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held
from services.portal_operational.entitlements import read_view


class ExistingAuthorityBoundary:
    def __init__(self, db):
        self.db = db

    async def authorize(self, request, phase):
        view = await read_view(self.db, {"tenant_id": request.tenant_id, "principal_id": request.principal_id})
        if not view["licence_admitted"]:
            raise Held("LICENCE_NOT_ADMITTED")
        # A real licence is not a durable operation/independent approval/custody grant.
        raise Held("OPERATION_AUTHORITY_NOT_BOUND")


class ExistingArtifactBoundary:
    async def verify(self, request, result, operation_key):
        raise Held("ARTIFACT_CHECKER_NOT_BOUND")


def build_coordinator(db):
    return Coordinator(LedgerJournal(db), ExistingAuthorityBoundary(db), {}, ExistingArtifactBoundary())