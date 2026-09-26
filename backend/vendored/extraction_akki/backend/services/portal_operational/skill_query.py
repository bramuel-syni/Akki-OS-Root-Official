"""No response/class pass-through when a governed skill executor is unadmitted."""
import hashlib
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator
from services.ledger_writer.mongo_control import append_event


class SkillQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    query: str = Field(min_length=1, max_length=8000)

    @field_validator("query")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("A nonblank query is required.")
        return value


async def refuse_unadmitted(db, scope, skill_id, query):
    run_id = f"skill-query-{uuid.uuid4().hex}"
    event = await append_event(
        db, tenant_id=scope["tenant_id"], run_id=run_id, actor_id=scope["principal_id"],
        command_id=run_id, event_type="skill.query.refused", resource_type="skill_query",
        decision="refused", reason_code="SKILL_EXECUTOR_UNADMITTED",
        payload={"skill_id": skill_id, "principal_id": scope["principal_id"],
                 "query_sha256": hashlib.sha256(query.query.encode()).hexdigest(),
                 "reason_code": "SKILL_EXECUTOR_UNADMITTED", "execution_verified": False},
    )
    return {"outcome": "refused", "reason_code": "SKILL_EXECUTOR_UNADMITTED",
            "detail": "No admitted executor and grounded result receipt are available for this skill.",
            "skill_id": skill_id, "receipt_hash": event["row"]["hash"], "execution_verified": False}