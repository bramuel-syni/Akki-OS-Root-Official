"""Native principal/licence/catalogue composition; a licence is NOT approval."""
import time
import asyncio
import inspect
from contracts.principal_v1 import PrincipalKind, PrincipalV1
from services.enforce.control_scope import require_control_scope
from services.principal_store.store import get_principal, PrincipalRefusal
from services.portal_operational.entitlements import read_view, LicencePortalView
from services.entitlement_service_v1.chokepoint_resolver import resolve, ResolutionRefusal
from services.northena.execution_models import Held
from services.northena.execution_validation import authority_for
from services.northena.execution_component_models import Decision, CommercialSnapshot, Prepared


class ComponentAuthority:
    def __init__(self, db, decisions=None, principal_lookup=get_principal, clock=time.time):
        self.db, self.decisions = db, decisions
        self.principal_lookup, self.clock = principal_lookup, clock

    def principal(self, principal_id):
        try:
            stored = self.principal_lookup(principal_id)
            return self.checked_principal(stored, principal_id)
        except (PrincipalRefusal, KeyError, ValueError, AttributeError, TypeError) as exc:
            raise Held("PRINCIPAL_NOT_ADMITTED") from exc
    @staticmethod
    def checked_principal(stored, principal_id):
        value = PrincipalV1.model_validate({key: getattr(stored, key) for key in PrincipalV1.model_fields})
        if value.principal_id != principal_id or value.suspended:
            raise Held("PRINCIPAL_UNAVAILABLE")
        return value

    async def current_principal(self, principal_id):
        if not inspect.iscoroutinefunction(self.principal_lookup):
            return self.principal(principal_id)
        timeout = getattr(self.decisions, "timeout_seconds", None)
        if timeout is None:
            raise Held("PRINCIPAL_LOOKUP_NOT_BOUNDED")
        try:
            stored = await asyncio.wait_for(self.principal_lookup(principal_id), timeout)
            return self.checked_principal(stored, principal_id)
        except (TimeoutError, ConnectionError, OSError):
            raise Held("PRINCIPAL_ADMISSION_UNAVAILABLE") from None
        except (PrincipalRefusal, KeyError, ValueError, AttributeError, TypeError):
            raise Held("PRINCIPAL_NOT_ADMITTED") from None

    async def context(self, request):
        try:
            scope = require_control_scope()
        except ValueError as exc:
            raise Held("PRINCIPAL_CONTEXT_UNAVAILABLE") from exc
        if (scope.principal_id, scope.tenant_id) != (request.principal_id, request.tenant_id):
            raise Held("PRINCIPAL_CONTEXT_MISMATCH")
        principal = await self.current_principal(request.principal_id)
        org_id = principal.principal_id if principal.kind == PrincipalKind.ORGANISATION else principal.parent_organisation_id
        if not org_id:
            raise Held("ORGANISATION_NOT_ADMITTED")
        org = await self.current_principal(org_id)
        if (org.kind != PrincipalKind.ORGANISATION or org.parent_organisation_id is not None
                or org.trust_domain_identifier != principal.trust_domain_identifier):
            raise Held("ORGANISATION_CONTEXT_MISMATCH")
        view = await read_view(self.db, {"tenant_id": request.tenant_id, "principal_id": request.principal_id})
        if not isinstance(view, LicencePortalView):
            raise Held("LICENCE_VIEW_INVALID")
        view = LicencePortalView.model_validate_json(view.model_dump_json())
        if (view.status != "resolved" or view.licence is None or view.licence.status != "active"
                or view.allowance_state is None):
            raise Held(view.reason_code or "LICENCE_NOT_ADMITTED")
        if (view.principal_id != request.principal_id or view.licence.organisation_principal_id != org_id):
            raise Held("LICENCE_ORGANISATION_MISMATCH")
        return principal, view

    async def _resolve(self, request, phase):
        principal, view = await self.context(request)
        if self.decisions is None:
            raise Held("OPERATION_AUTHORITY_NOT_BOUND")
        timeout = getattr(self.decisions, "timeout_seconds", None)
        try:
            decision = await asyncio.wait_for(self.decisions.resolve(request, phase, principal, view), timeout)
        except (TimeoutError, ConnectionError, OSError):
            raise Held("OPERATION_AUTHORITY_UNAVAILABLE") from None
        if not isinstance(decision, Decision):
            raise Held("OPERATION_DECISION_INVALID")
        decision = Decision.model_validate_json(decision.model_dump_json())
        grant = authority_for(request, decision.authority, self.clock(), phase)
        if grant.terms_ref != view.licence.terms_identifier:
            raise Held("OPERATION_TERMS_MISMATCH")
        row = None
        if decision.catalog_model_identifier is None:
            if request.kind != "source":
                raise Held("MODEL_SELECTION_UNRESOLVED")
        else:
            matches = [item for item in view.rows if
                       (item.model_identifier, item.access_class) ==
                       (decision.catalog_model_identifier, decision.catalog_access_class)]
            if len(matches) != 1:
                raise Held("CATALOGUE_SELECTION_UNRESOLVED")
            row = matches[0]
            if row.access_class == "reseller_frontier":
                raise Held("RESELLER_AUTHORITY_UNRESOLVED")
            try:
                resolve(principal=principal, licence=view.licence, catalog_row=row, allowance_state=view.allowance_state)
            except ResolutionRefusal as exc:
                raise Held("ENTITLEMENT_RESOLUTION_REFUSED") from exc
        snapshot = CommercialSnapshot.model_validate_json(CommercialSnapshot(
            licence=view.licence, catalog_row=row, principal_id=principal.principal_id,
            period_iso=view.allowance_state.period_iso).model_dump_json())
        return Prepared(authority=grant, commercial_snapshot=snapshot)

    async def prepare(self, request):
        return await self._resolve(request, "dispatch")

    async def authorize(self, request, phase):
        return (await self._resolve(request, phase)).authority