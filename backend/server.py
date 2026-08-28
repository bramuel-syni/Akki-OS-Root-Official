from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone
import boto3

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# --- Spine bridge: WS-BUILD-CONNECT-GPU production code lives on
#     programme/track-a in Extraction-Akki. /app/backend is the pod-shell
#     that mounts the router. Access is source-IP allowlist per owner
#     stop-order 2026-08-14 — the retired token gate no longer imports.
SPINE_BACKEND = Path("/app/assessment_workspace/repos/Extraction-Akki/backend")
if str(SPINE_BACKEND) not in sys.path:
    sys.path.insert(0, str(SPINE_BACKEND))
from routers import connect_gpu as connect_gpu_router  # noqa: E402
from services.connect_estate.router import router as connect_estate_router  # noqa: E402
from services.credentials_paste.router import router as credentials_paste_router  # noqa: E402
from services.connect.rds_data_router import router as rds_data_router  # noqa: E402
from services.connect.confirm_router import router as connect_confirm_router  # noqa: E402  # W11 R2
from services.registry_facts.router import router as registry_facts_router  # noqa: E402
from services.compute_seam.reflection_router import router as compute_reflection_router  # noqa: E402
from services.chokepoint.router import router as shield_router  # noqa: E402
from services.northena.router import router as thinklab_router  # noqa: E402
from services.chat.router import router as chat_router  # noqa: E402
from services.wizard.connect_llm_router import router as connect_llm_router  # noqa: E402
from services.cost_ledger.router import router as cost_ledger_router  # noqa: E402
from services.retention.router import router as retention_router  # noqa: E402
from services.lowered_standard.router import router as lowered_standard_router  # noqa: E402
# W7 · Model Ecosystem + Model Admission surfaces (Docs 13/14 · CA1-004/005/011).
from services.model_registry.router import router as model_registry_router  # noqa: E402
from services.model_admission.router import router as model_admission_router  # noqa: E402
from services.baseline_line.router import router as baseline_line_router  # noqa: E402
from services.model_recheck.router import router as model_recheck_router  # noqa: E402
# W8 CP5 · governance timeline surface (Doc 15 §Trace · REFERENCE-NOT-COPY).
from services.trace.router import router as trace_router  # noqa: E402
# W10 CP8 · Governance / Watch / Grey-Mirror state rollup surfaces
#   (Canon 8 §§7-19 · Doc 15 §17 · REFERENCE-NOT-COPY read-only).
from services.governance.router import router as governance_router  # noqa: E402
from services.watch.router import router as watch_router  # noqa: E402
from services.grey_mirror.router import router as grey_mirror_router  # noqa: E402
# Wave F Cleanup · CP · audit-trail Overview surface
#   (Addendum §1 CA1-001/002/003 · REFERENCE-NOT-COPY read-only).
from services.audit_trail.router import router as audit_trail_router  # noqa: E402
# Wave-G5c-CENSUS · Census Engine wire (owner ruling 2026-08-28T~14:30Z:
#   "Run the census to pull the data. There should be more than one data
#    base. Registry should work, i should see what the digicow databases
#    holds, how the census is doing").
from services.census_engine.router import router as census_engine_router  # noqa: E402
# Wave-G5c-COMPUTE-BACKEND · Compute Estate surface (owner ruling 4,
# 2026-08-28T~15:00Z: derive from banked Wave-H receipts, product language
# only, never IPs / auth / engineering vocab).
from services.compute_estate.router import router as compute_estate_router  # noqa: E402
# W11 R3 · Canon 5 §14 Shaping Wizard (Phase 7 Stage B-1 LIFT · Canon 5
# supersedes 2026-08-14 Simplification Ruling per owner 2026-08-26).
from routers import wizard_operator as wizard_operator_router  # noqa: E402
# W11 R4.1 · Doc 17 Multidimensional Training Engine (state + compile + seal).
from services.training.router import router as training_router  # noqa: E402
# W11 R4.2 · Doc 18 Callable Skill Files HTTP surface.
from routers import transform_forms as transform_forms_router  # noqa: E402
# W11 R4.3 · Doc 08 Memory plane HTTP surface.
from routers import memory as memory_router  # noqa: E402
# W11 R4.4 · Doc 15-086 CA1-009 Generalised handoff contract surface.
from routers import handoff as handoff_router  # noqa: E402
# W11 R4.5 · Doc 10-006 Opportunity briefs pipeline wired to HTTP surface.
from routers import registry as registry_router  # noqa: E402
# W11 R4.6 · Doc 14-024 CA1-005 Whitepaper HTTP surface.
from services.whitepapers.router import router as whitepapers_router  # noqa: E402
# W11 R4.7 · Doc 15 N-series breach + erasure HTTP surface.
from services.n_series.router import router as n_series_router  # noqa: E402
from services.rights_quarantine.router import router as rights_quarantine_router  # noqa: E402  # W11 E · CP-E4 · Doc14-020
# W11 B · CP4 · Doc 18 A18.7 Skill-file provenance chain HTTP surface.
from services.skill_files.router import router as skill_files_router  # noqa: E402
# W11 B · CP6 · Doc 19B §19B.4-6 · EP-1/EP-3 Evidence register + A-4.
from services.evidence_register.router import router as evidence_register_router  # noqa: E402
# W11 D · CP-D0 post-fix · A17.16 wire path · /api/service_1/v2/dispatch
# emits ModelFormOfferEnvelopeV0 for outcome_form='model'. Ship-Manifest
# DoD reconciliation 2026-08-27 (owner ruling): routers.service_1 removed
# from KNOWN_UNWIRED and mounted on the pod-shell so the A17.16 mechanism
# is reachable through the user path, not just via the unit tests.
from routers import service_1 as service_1_router  # noqa: E402
# W11 D · CP-D7 · Governance Ceremony lift (owner ruling 2026-08-27,
# verbatim: "CP-D7 Governance Ceremony (lift + UI surface)"). Doc 15
# ceremony surfaces (Register: Doc15-020 rule-change propose·countersign·
# countdown·apply·re-check depends on these landing on the pod).
from routers import govern as govern_router  # noqa: E402
from routers import checker as checker_router  # noqa: E402
from routers import compliance as compliance_router  # noqa: E402
from routers import master_admin as master_admin_router  # noqa: E402
# W11 D · CP-D8 · Cross-cutting Orchestration lift (owner ruling
# 2026-08-27, verbatim: "CP-D8 Cross-cutting Orchestration (Doc 16:
# walk-this/claim-to-evidence, disclosure grammar, remaining UI mass)").
# Doc 16 team-side approvals + access-register + constitutional seats
# surfaces. Register: Doc16-001 REUSABLE→DONE + Doc16-014 wire-through
# PARTIAL→DONE via the mounted team ceremony.
from routers import team as team_router  # noqa: E402
from services.ip_allowlist.middleware import IPAllowlistMiddleware  # noqa: E402

# Deliverables directory (read-only snapshot per Chunk-4 v1.1 delivery logistics)
DELIVERABLES_DIR = ROOT_DIR / 'deliverables'
DELIVERABLES_ALLOWLIST = {
    'BUILD_STRATEGY.md',
    'REUSE_ASSESSMENT.md',
}

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Tigris S3-compatible client
s3_client = boto3.client(
    's3',
    endpoint_url=os.environ.get('TIGRIS_ENDPOINT', 'http://localhost:8085'),
    aws_access_key_id=os.environ.get('TIGRIS_ACCESS_KEY_ID', ''),
    aws_secret_access_key=os.environ.get('TIGRIS_SECRET_ACCESS_KEY', ''),
    region_name='auto',
)
TIGRIS_BUCKET = os.environ.get('TIGRIS_BUCKET', 'default-bucket')

# Create the main app without a prefix
app = FastAPI(
    # W10 CP9 · expose OpenAPI at /api/openapi.json so it routes through
    # the ingress /api/* rule (owner tester contract-discovery seam).
    # Docs / redoc UIs stay disabled — no HTML endpoints, just the JSON
    # spec. Response boundary sanitizers (Owner Order 2026-08-25 §4)
    # continue to hold on the runtime payloads; OpenAPI reflects
    # Pydantic model shapes only, which never include raw secrets.
    openapi_url="/api/openapi.json",
    docs_url=None,
    redoc_url=None,
    title="Akki · Extraction-Akki (programme/track-a)",
    version="w10-cp9",
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)

    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()

    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)

    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])

    return status_checks


@api_router.get("/deliverables/{filename}")
async def get_deliverable(filename: str):
    """Serve read-only snapshots of Chunk-4 deliverables.

    Snapshot commit: 7ae3b1b (fixture-arrival cycle CLOSED; see /app/assessment_workspace STATE/CONTEXT.md).
    Allowlist-guarded; no path traversal. Served as text/markdown so browsers
    render / download cleanly.
    """
    if filename not in DELIVERABLES_ALLOWLIST:
        raise HTTPException(status_code=404, detail="deliverable not found")
    file_path = DELIVERABLES_DIR / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="deliverable missing on disk")
    return FileResponse(
        path=str(file_path),
        media_type="text/markdown; charset=utf-8",
        filename=filename,
    )


@api_router.get("/deliverables")
async def list_deliverables():
    """List available deliverables with size + snapshot metadata."""
    items = []
    for name in sorted(DELIVERABLES_ALLOWLIST):
        p = DELIVERABLES_DIR / name
        if p.is_file():
            items.append({
                "name": name,
                "size_bytes": p.stat().st_size,
                "url": f"/api/deliverables/{name}",
            })
    return {
        "snapshot_commit": "7ae3b1b",
        "snapshot_source": "/app/assessment_workspace/",
        "items": items,
    }

# Include the router in the main app
app.include_router(api_router)

# --- WS-BUILD-CONNECT-GPU: mount connect-gpu router; no per-route auth.
# Access control is the IP allowlist middleware installed below — it gates
# EVERY route (UI, /api/*, /api/deliverables, static). No route survives
# outside it.
app.include_router(connect_gpu_router.router)
app.include_router(connect_estate_router)
app.include_router(credentials_paste_router)
app.include_router(rds_data_router)
app.include_router(connect_confirm_router)  # W11 R2 · /api/connect/confirm/{draft_id} + /draft/{draft_id}
app.include_router(registry_facts_router)
app.include_router(compute_reflection_router)
app.include_router(shield_router)
app.include_router(thinklab_router)
app.include_router(chat_router)
app.include_router(connect_llm_router)
app.include_router(cost_ledger_router)
app.include_router(retention_router)
app.include_router(lowered_standard_router)
# W7 · Model Ecosystem + Model Admission surfaces.
app.include_router(model_registry_router)
app.include_router(model_admission_router)
app.include_router(baseline_line_router)
app.include_router(model_recheck_router)
# W8 CP5 · governance timeline surface (Doc 15 §Trace).
app.include_router(trace_router)
# W10 CP8 · Governance / Watch / Grey-Mirror state rollup surfaces.
app.include_router(governance_router)
app.include_router(watch_router)
app.include_router(grey_mirror_router)
# Wave F Cleanup · CP · audit-trail Overview surface (Addendum §1 CA1-001/002/003).
app.include_router(audit_trail_router)
# Wave-G5c-CENSUS · Census Engine wire (multi-DB RDS Data API walker;
# aggregates-only chokepoint; audit entry per read; numbered records under
# phase0/census/). Owner rulings 1–3 banked in DECISIONS.md 2026-08-28T~15:00Z.
app.include_router(census_engine_router)
# Wave-G5c-COMPUTE-BACKEND · Compute Estate wire (owner ruling 4,
# 2026-08-28T~15:00Z): derive from banked Wave-H whitepaper; product language
# only; never IPs / auth / engineering vocab.
app.include_router(compute_estate_router)
app.include_router(wizard_operator_router.router, prefix="/api")  # W11 R3 · Canon 5 §14
# W11 R4.1 · Doc 17 Training plane (state · demand-table compile · test-set seal).
app.include_router(training_router)
# W11 R4.2 · Doc 18 Callable Skill Files (/api/callable_skill/*, /api/transform/*).
app.include_router(transform_forms_router.router, prefix="/api")
# W11 R4.3 · Doc 08 Memory plane (/api/memory/planes/*).
app.include_router(memory_router.router, prefix="/api")
# W11 R4.4 · Doc 15-086 handoff (/api/handoff/*).
app.include_router(handoff_router.router, prefix="/api")
# W11 R4.5 · Doc 10-006 Registry + Opportunity briefs pipeline
# (/api/registry/opportunity_briefs, /api/registry/opportunity_briefs/regenerate,
#  /api/registry/what_you_hold, /api/registry/gap_register, /api/prove/*).
app.include_router(registry_router.router, prefix="/api")
app.include_router(registry_router.prove_router, prefix="/api")
# W11 R4.6 · Doc 14-024 Whitepaper HTTP surface (/api/whitepapers · POST + GET).
app.include_router(whitepapers_router)
# W11 R4.7 · Doc 15 N-series (/api/n_series/breach + /api/n_series/erasure).
app.include_router(n_series_router)
app.include_router(rights_quarantine_router)  # W11 E · CP-E4 · Doc14-020 quarantine surface
# W11 B · CP4 · Doc 18 A18.7 Skill-file provenance chain
# (/api/skill-files/state, /api/skill-files/{skill_id}/provenance).
app.include_router(skill_files_router)
# W11 B · CP6 · Doc 19B §19B.4-6 · EP-1 Evidence register + EP-3 A-4
# (/api/evidence-register/*, /api/claims-validation).
app.include_router(evidence_register_router)
# W11 D · CP-D0 post-fix · A17.16 wire path · service_1 router mounted
# under /api/service_1/* (service_1/run, service_1/run/{id},
# service_1/v2/dispatch). Ship-Manifest DoD reconciliation 2026-08-27:
# routers.service_1 was in KNOWN_UNWIRED with the justification 'never
# wired in either assembler; retained only for the invariant tests that
# reference it. Register: no active row cites' — that justification was
# invalidated by CP-D0 A17.16 ACCEPT shipping the ModelFormOfferEnvelopeV0
# behind this router's /v2/dispatch endpoint. KNOWN_UNWIRED entry removed
# in the same commit.
app.include_router(service_1_router.router, prefix="/api")

# W11 D · CP-D7 · Governance Ceremony lift (owner ruling 2026-08-27):
#   /api/govern/*         registries upload/diff/commit + enforcement_class_split
#                          + trust_center_record + estate_rules_record + holds
#   /api/checker/*        propose·countersign·countdown·apply ceremony
#   /api/compliance/*     Doc15 refusals/coverage/retention receipts
#   /api/master_admin/*   pending seams + audit trail + tightening/suspend
# Ship-Manifest DoD: paired with MUST_BE_LIVE_ROUTES entries in
# tests/invariants/test_ship_manifest_dod_route_table_drift.py and
# KNOWN_UNWIRED entry removal for routers.govern / .checker / .compliance /
# .master_admin in the SAME commit.
app.include_router(govern_router.router, prefix="/api")
app.include_router(checker_router.router, prefix="/api")
app.include_router(compliance_router.router, prefix="/api")
app.include_router(master_admin_router.router, prefix="/api")

# W11 D · CP-D8 · Cross-cutting Orchestration lift (owner ruling
# 2026-08-27):
#   /api/team/*  approval_surface + approval_surface/{id}/decision +
#                access_register + access_register/grant + revoke +
#                constitutional_seats
# team_router.router already carries prefix="/api/team", so mount
# WITHOUT an additional prefix (matches backend/server.py's convention).
# Same-commit KNOWN_UNWIRED entry removal + MUST_BE_LIVE_ROUTES entries
# in tests/invariants/test_ship_manifest_dod_route_table_drift.py.
app.include_router(team_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# IPAllowlistMiddleware is added LAST → outermost → runs FIRST for every
# request. Non-allowlisted IPs get HTTP 403 text/plain with the exact
# sentence "This surface answers allowlisted addresses only." before any
# other middleware or route logic sees them.
app.add_middleware(IPAllowlistMiddleware)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
