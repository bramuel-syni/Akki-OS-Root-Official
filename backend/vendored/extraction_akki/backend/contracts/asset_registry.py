"""contracts/asset_registry.py — W-REGISTRY-EXTENSION-G3 contracts.

Owner label 2026-09-13 · closes Doc-0 §STATUS AS OF row G-3 mechanical
half (Mtafiti's asset-inventory extension from estate sources only to
the full asset class Doc-0 Attribute 3 defines).

Canon anchors (first-hand, this session):
  * Doc-0 §BA-3.1  — every principal belongs to a stated class and
                     carries a mandate whose source can be named.
  * Doc-0 §BR-1.4  — custody class is a typed, queryable attribute,
                     not a description in prose.
  * Doc-0 §BR-4.1  — asset-class coverage extends beyond estate sources.
  * Canon-1 §4.6   — extend an existing component; do not create a
                     sibling registry.  FreshnessStamp is REUSED from
                     contracts.mtafiti_registry rather than re-declared.
  * Canon-3 §22    — four-class governance-value taxonomy.
  * Canon-7 §35-40 — Function & Promise Registry 11-field row.
  * Canon-9 §3     — single writer (Mtafiti) for census/registry
                     records.  ASSET_REGISTRY_COLLECTION is the write
                     channel; negative-scan test asserts no second
                     writer imports this constant.

R-C1 marker (this file):
  R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE=True — until the Rules
  Service lands, controlled-unit determination is by custody class
  alone (DAP-Spec §8 dependency table verbatim).

Extension discipline:
  contracts.mtafiti_registry.MtafitiRegistryRecord is UNTOUCHED — this
  file adds a peer record shape for other asset classes (models,
  artifacts, receipts, rules) with the same freshness/named-owner
  discipline.  Nothing here mutates the existing frozen contract.
"""
from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from contracts.mtafiti_registry import FreshnessStamp


# --- named channel ----------------------------------------------------
# Canon-9 §3: single writer for census/registry records; second writer
# is a defect on sight.  Negative-scan test asserts no other module
# under services/ imports this constant.
ASSET_REGISTRY_COLLECTION = "mtafiti_asset_registry_records"


# --- R-C1 · Rules Service · GOVERNED RETIREMENT ---------------------
# Marker retired 2026-09-13 by W-M2-SW2 (W-RULES-SERVICE-CEREMONY).
# Retirement is backed by:
#   - services/rules_service/rule_registry.py  (W-M2-SW1)
#   - services/rules_service/ceremony.py       (W-M2-SW2)
# The marker constant remains as a LINEAGE ANCHOR so any future silent
# re-flip is caught by the invariant that asserts the retirement is
# mechanism-backed
# (`test_sw2_r_c1_retirement_backed_by_mechanism`).
R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE: bool = False


# --- enums -----------------------------------------------------------
class AssetClass(str, Enum):
    """Doc-0 BR-4.1 asset-class extension.  Five canon-recognised kinds."""

    SOURCE = "source"
    MODEL = "model"
    ARTIFACT = "artifact"
    RECEIPT = "receipt"
    RULE = "rule"


class CustodyClass(str, Enum):
    """Doc-0 BR-1.4 typed custody class.  DPO-1 declares this set;
    Canon-4 (Document 4) may refine at a subsequent CP boundary."""

    OPEN = "open"
    SENSITIVE = "sensitive"
    CONTROLLED = "controlled"
    FORBIDDEN = "forbidden"


class GovernanceValueClass(str, Enum):
    """Canon-3 §22 four-class taxonomy.  Every governed value is
    exactly one of these classes."""

    RAILS = "rails"
    RULES = "rules"
    ENGINE_SETTINGS = "engine_settings"
    REGISTRIES = "registries"


# --- named owner (Doc-0 BA-3.1) -------------------------------------
class NamedOwner(BaseModel):
    """Doc-0 BA-3.1 three-part owner shape."""

    model_config = ConfigDict(extra="forbid")

    owner_id: str = Field(..., description="Stable id of the owning principal.")
    owner_class: str = Field(
        ...,
        description=(
            "Doc-0 BA-3.1: 'human role, application, or subsystem acting "
            "under its own authority'."
        ),
    )
    mandate_source: str = Field(
        ...,
        description=(
            "Where the mandate is named — a canon section, a rule id, or "
            "a governance ceremony record."
        ),
    )


# --- asset-registry record ------------------------------------------
class AssetRegistryRecord(BaseModel):
    """Doc-0 BR-4.1: one record per asset in Mtafiti's extended registry.

    Peer to MtafitiRegistryRecord (which covers estate sources).  Reuses
    FreshnessStamp; does not sibling it (Canon-1 §4.6)."""

    model_config = ConfigDict(extra="forbid")

    asset_ref: str = Field(..., description="Stable pointer to the asset (e.g. 'model:adapter-v1').")
    asset_class: AssetClass = Field(..., description="Doc-0 BR-4.1 asset-class taxonomy.")
    named_owner: NamedOwner = Field(..., description="Doc-0 BA-3.1 three-part owner.")
    custody_class: CustodyClass = Field(
        ...,
        description=(
            "Doc-0 BR-1.4: typed queryable custody class.  Free-text "
            "refused by enum validation.  R-C1: custody class is the "
            "sole controlled-unit determinant until the Rules Service "
            "lands (DAP-Spec §8 dependency)."
        ),
    )
    freshness_stamp: FreshnessStamp = Field(
        ...,
        description=(
            "Reused from contracts.mtafiti_registry (Canon-1 §4.6 "
            "extension-not-sibling doctrine)."
        ),
    )


# --- Function & Promise Registry row (Canon-7 §35-40) ----------------
class FunctionPromiseRow(BaseModel):
    """Canon-7 §35 eleven mandatory fields per registered function.

    §37 verbatim: 'No gate without a promise.  No promise without a
    service trace.  No journey step without enforcement.  New functions
    register before they land.'"""

    model_config = ConfigDict(extra="forbid")

    function_id: str = Field(..., description="Dotted path or stable name.")
    governor: str = Field(..., description="The engine/authority that governs this function.")
    mandate: str = Field(..., description="Canon clause or ruling that mandates this function.")
    promise: str = Field(..., description="The single promise this function protects.")
    service_trace: str = Field(..., description="Where the promise's service trace lives.")
    surface: str = Field(..., description="User-visible surface, if any; 'internal' otherwise.")
    enforcement: str = Field(..., description="How the function enforces its promise.")
    cost: str = Field(..., description="Rent paid — perf, complexity, or maintenance.")
    dependencies: List[str] = Field(default_factory=list, description="function_ids this depends on.")
    ladder_rung: str = Field(..., description="Canon-4 §40 ladder rung, or 'n/a' for non-model.")
    owner: str = Field(..., description="Named-owner reference.")
