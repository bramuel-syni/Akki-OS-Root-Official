"""Configuration disclosure only, never an authorisation or health certificate."""
from pydantic import BaseModel
from services.activation.runtime_binding import NativeRuntime


class RuntimeStatus(BaseModel):
    configured: bool
    native_principal_lookup_bound: bool
    signer_resolution_bound: bool
    artifact_inspection_bound: bool
    worker_paths_bound: list[str]
    custody_delivery_bound: bool = False
    skill_query_execution_bound: bool = False
    reason_code: str
    execution_authorized: bool = False
    live_proof_verified: bool = False


def runtime_status(state):
    runtime = getattr(state, "native_runtime", None)
    configured = isinstance(runtime, NativeRuntime)
    paths = sorted({e.kind for e in runtime.bindings.executors.values()}) if configured else []
    return RuntimeStatus(configured=configured, native_principal_lookup_bound=configured,
        signer_resolution_bound=configured, artifact_inspection_bound=configured,
        custody_delivery_bound=configured and runtime.custody is not None,
        skill_query_execution_bound=configured and 'skill' in paths,
        worker_paths_bound=paths, reason_code="NATIVE_CONFIGURATION_INSTALLED" if configured else "NATIVE_BINDINGS_UNBOUND")