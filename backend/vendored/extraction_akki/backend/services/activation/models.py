from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

Text = Annotated[str, Field(min_length=1, max_length=1024, pattern=r"^\S(?:[^\r\n]*\S)?$")]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True, allow_inf_nan=False)


class Issue(Frozen):
    code: str
    path: str

    def keys(self):
        return ("code", "path")


class ValidationResult(Frozen):
    valid: bool = False
    schema_valid: bool = False
    semantics_valid: bool = False
    evidence_verified: bool = False
    execution_authorized: Literal[False] = False
    derived_state: Literal["IMPLEMENTED", "LIVE-VERIFIED", "LIVE-BLOCKED", "PARTIALLY LIVE"] | None = None
    profile_id: str
    profile_sha256: str
    implementation_sha256: str
    certificate_sha256: str
    issues: tuple[Issue, ...] = ()


def issue(code, path="/"):
    return Issue(code=code, path=path)