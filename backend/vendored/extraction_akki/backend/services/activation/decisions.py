"""Native decision producer for ComponentAuthority's existing operation gate."""
from services.activation.approvals import approved_plan
from services.activation.reservations import Reservations
from services.northena.execution_models import Authority, Held
from services.northena.execution_component_models import Decision


class LedgerActivationDecisions:
    def __init__(self, receipts):
        self.receipts = receipts
        self.timeout_seconds = receipts.timeout

    async def resolve(self, request, phase, principal, licence_view):
        plan, ref, _, expiry, _ = await approved_plan(self.receipts, request)
        if principal.principal_id != request.principal_id or plan.terms_ref != licence_view.licence.terms_identifier:
            raise Held("ACTIVATION_PRINCIPAL_OR_TERMS_MISMATCH")
        if phase == "dispatch":
            await Reservations(self.receipts).reserve(plan, ref)
        return Decision(authority=Authority(authority_ref=ref, request_sha256=request.digest(),
            tenant_id=request.tenant_id, principal_id=request.principal_id, scope_refs=request.scope_refs,
            engine=request.engine, expires_epoch=expiry, terms_ref=plan.terms_ref, policy_epoch=plan.policy_epoch),
            catalog_model_identifier=plan.catalog_model_identifier, catalog_access_class=plan.catalog_access_class)