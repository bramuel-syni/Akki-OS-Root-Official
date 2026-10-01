"""Production inputs, separate from advisory prose and measured worker receipts."""
from typing import Literal
from pydantic import Field, model_validator
from services.training_lab.contracts import Closed


class StratumBar(Closed):
    accuracy: float = Field(ge=0, le=1)
    coverage: float = Field(ge=0, le=1)


class Outcome(Closed):
    task: str = Field(min_length=1, max_length=300)
    domain: str = Field(min_length=1, max_length=200)
    population_register_ref: str = Field(pattern=r'^m9j-[a-f0-9]{12}$')
    stratum_refs: list[str] = Field(min_length=1, max_length=500)
    acceptance: dict[str, StratumBar]
    gate_policy: Literal['missed_stratum_gates_release', 'ships_documented']
    test_set_ref: str = Field(pattern=r'^[a-f0-9]{64}$')
    constraints: dict[str, str]

    @model_validator(mode='after')
    def complete(self):
        if len(set(self.stratum_refs)) != len(self.stratum_refs) or set(self.acceptance) != set(self.stratum_refs):
            raise ValueError('Every register stratum needs its own accuracy and coverage acceptance.')
        if not all(self.constraints.get(k, '').strip() for k in ('latency', 'compute_budget', 'deployment_target')):
            raise ValueError('Latency, compute budget and deployment target are required.')
        return self


class Schema(Closed):
    baseline_tier: list[str] = Field(min_length=1, max_length=100)
    objective_tier: list[str] = Field(max_length=100)
    provenance_refs: dict[str, str]

    @model_validator(mode='after')
    def provenance(self):
        if any(not self.provenance_refs.get(k, '').strip() for k in self.objective_tier):
            raise ValueError('Each objective column requires its qualification/provenance reference.')
        return self


class Definition(Closed):
    target_outcome: Outcome
    collection_schema: Schema
    planned_epochs: int = Field(ge=1, le=1000)
    gpu_hour_cap: float = Field(gt=0)
    legal_basis: str = Field(min_length=1, max_length=1000)


class StageEvidence(Closed):
    job_id: str = Field(pattern=r'^m9j-[a-f0-9]{12}$')


class RecipeRevision(Closed):
    recipe: dict
    reason: str = Field(min_length=1, max_length=1200)
    evidence_refs: list[str] = Field(min_length=1, max_length=20)
    expected_revision: int = Field(ge=0)