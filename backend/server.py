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
from services.registry_facts.router import router as registry_facts_router  # noqa: E402
from services.compute_seam.reflection_router import router as compute_reflection_router  # noqa: E402
from services.chokepoint.router import router as shield_router  # noqa: E402
from services.northena.router import router as thinklab_router  # noqa: E402
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
app = FastAPI()

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
app.include_router(registry_facts_router)
app.include_router(compute_reflection_router)
app.include_router(shield_router)
app.include_router(thinklab_router)

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
