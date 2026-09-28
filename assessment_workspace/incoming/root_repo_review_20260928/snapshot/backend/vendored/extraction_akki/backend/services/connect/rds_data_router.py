"""services.connect.rds_data_router - POST /api/connect/data-source (Aurora Data API).

Owner Ruling 2026-08-18 - FL-P2-23. Same custody rule as the compute path:
the request body carries the aws_secret_access_key once; the response NEVER
carries it back.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.connect.rds_data_submit import submit as _submit

log = logging.getLogger(__name__)

router = APIRouter()


class DataSourcePayload(BaseModel):
    aws_access_key_id: Optional[str] = Field(None, max_length=128)
    aws_secret_access_key: Optional[str] = Field(None, max_length=256)
    region: str = Field(..., max_length=32)
    cluster_arn: str = Field(..., max_length=256)
    secret_arn: str = Field(..., max_length=256)
    database: Optional[str] = Field(None, max_length=128)


@router.post("/api/connect/data-source")
async def post_data_source(payload: DataSourcePayload) -> Dict[str, Any]:
    """Test-connect an Aurora cluster and record the outcome.

    Returns the four-questions dict shape (link_working, found, ready, failure,
    failure_sentence). Never returns the aws_secret_access_key.
    """
    body = payload.model_dump(exclude_none=True)
    if not body.get("cluster_arn", "").startswith("arn:aws:rds:"):
        raise HTTPException(status_code=400, detail="cluster_arn does not look like an RDS cluster ARN")
    if not body.get("secret_arn", "").startswith("arn:aws:secretsmanager:"):
        raise HTTPException(status_code=400, detail="secret_arn does not look like a Secrets Manager ARN")
    result = _submit(body, actor="owner")
    # Extra belt+braces: strip any secret-shaped field that might have snuck in
    for k in ("aws_secret_access_key", "aws_access_key_id"):
        result.pop(k, None)
    return result
