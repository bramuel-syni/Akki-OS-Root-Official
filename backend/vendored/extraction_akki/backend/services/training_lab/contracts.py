"""Closed, bounded input contracts; no arbitrary prompts, paths or commands."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Closed(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)


class Assessment(Closed):
    title: str = Field(default='Audio cognition and music readiness',min_length=1,max_length=100)
    host: Literal['akki-vm','akki-vm-ii'] = 'akki-vm'
    inspect_existing_data: bool = True
    model_reviews: bool = True


class MusicBaseline(Closed):
    title: str = Field(default='Music identification baseline',min_length=1,max_length=100)
    unlabelled_library_audio: Literal['music','excluded'] = 'music'
    include_synthetic: bool = True
    include_corpus_test: bool = True


class CorpusMeasurement(Closed):
    host: Literal['akki-vm','akki-vm-ii'] = 'akki-vm'
    workers: int = Field(default=16,ge=1,le=32)
    max_seconds: float = Field(default=5400,ge=60,le=7200)
    max_files_per_language: int = Field(default=0,ge=0,le=5000)


class Reinforcement(Closed):
    title: str = Field(default='Weak-language reinforcement plan',min_length=1,max_length=100)
    floor: float = Field(default=0.9,ge=0.5,le=0.999)
    model_reviews: bool = True



class Watch(Closed):
    enabled: bool
    max_checkpoints_per_job: int = Field(default=4,ge=1,le=8)


class StatisticsRequest(Closed):
    operation: Literal['wilson','bootstrap','power_law','monitor']
    successes: int | None = Field(default=None,ge=0)
    n: int | None = Field(default=None,ge=1)
    confidence: float = Field(default=0.95,gt=0,lt=1)
    values: list[float] = Field(default_factory=list,max_length=20000)
    paired: list[float] | None = Field(default=None,max_length=20000)
    groups: list[int] | None = Field(default=None,max_length=20000)
    seed: int = Field(default=41,ge=0)
    draws: int = Field(default=1000,ge=100,le=5000)
    points: list[tuple[float,float]] = Field(default_factory=list,max_length=100)
    exponent_bounds: tuple[float,float] | None = None
    irreducible_bounds: tuple[float,float] | None = None
    floor: float | None = Field(default=None,gt=0,lt=1)
    cap: int | None = Field(default=None,ge=1)
    false_alert_rate: float | None = Field(default=None,gt=0,lt=0.5)
    calibration_ref: str | None = Field(default=None,max_length=150)

    @model_validator(mode='after')
    def required(self):
        keys = {'wilson':['successes','n'],'bootstrap':['values'],
                'power_law':['points','exponent_bounds','irreducible_bounds','floor','cap'],
                'monitor':['values','false_alert_rate','calibration_ref']}[self.operation]
        if any(getattr(self,k) is None or getattr(self,k)==[] for k in keys):
            raise ValueError('Required fields: '+', '.join(keys))
        return self


class MusicRequest(Closed):
    speech: float = Field(ge=0,le=1)
    music: float = Field(ge=0,le=1)
    speech_threshold: float = Field(gt=0,lt=1)
    music_threshold: float = Field(gt=0,lt=1)
    calibration_ref: str = Field(min_length=1,max_length=150)


class ValueRequest(Closed):
    monthly_benefit: float = Field(ge=0)
    monthly_cost: float = Field(ge=0)
    setup_cost: float = Field(ge=0)
    adoption_probability: float = Field(ge=0,le=1)
    delay_months: int = Field(ge=0,le=120)
    horizon_months: int = Field(ge=1,le=120)
    annual_discount_rate: float = Field(ge=0,le=10)
    next_best_npv: float


class Prediction(Closed):
    role: Literal['knowledge_expert','ml_ops_engineer','researcher','entrepreneur','professor']
    low: float
    high: float
    actual: float
    prediction_ref: str = Field(min_length=1,max_length=150)
    actual_ref: str = Field(min_length=1,max_length=150)


class PostmortemRequest(Closed):
    predictions: list[Prediction] = Field(min_length=1,max_length=100)


class Finding(Closed):
    severity: Literal['note','review','blocker']
    evidence_refs: list[str] = Field(min_length=1,max_length=8)
    observation: str = Field(min_length=1,max_length=1000)
    recommendation: str = Field(min_length=1,max_length=1200)
    evidence_class: Literal['measured','hypothesis','recalled','unknown']


class Advisory(Closed):
    role: Literal['knowledge_expert','ml_ops_engineer','researcher','entrepreneur','professor']
    findings: list[Finding] = Field(min_length=1,max_length=6)
    uncertainties: list[str] = Field(max_length=8)
    advisory_only: Literal[True]


class Envelope(BaseModel):
    model_config = ConfigDict(extra='allow')
    tenant_id: str