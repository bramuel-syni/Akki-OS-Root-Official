"""DQ evidence reconciliation, not a profiler or an owner-policy generator.

Actual check execution remains on the admitted source side. This consumer rejects
incomplete bitmaps, invented Clean populations and quality-as-accuracy claims.
"""
from collections import Counter
from typing import Annotated, Literal
from pydantic import Field, model_validator
from services.northena.execution_models import Frozen, Handle, Hash, Name

Family = Literal['structural', 'sentinel', 'cross_field', 'duplicate',
                 'cross_source', 'plausibility', 'provenance']
Stratum = Literal['Clean', 'Repairable', 'Suspect', 'Junk']
FAMILIES = {'structural', 'sentinel', 'cross_field', 'duplicate',
            'cross_source', 'plausibility', 'provenance'}


class CheckRule(Frozen):
    rule_id: Name
    family: Family
    definition_sha256: Hash
    failure_stratum: Literal['Repairable', 'Suspect', 'Junk']


class QualityPack(Frozen):
    version: Name
    rules: Annotated[tuple[CheckRule, ...], Field(min_length=1, max_length=100)]
    media_applicable: bool
    media_rule_ids: tuple[Name, ...] = ()

    @model_validator(mode='after')
    def complete(self):
        ids = {r.rule_id for r in self.rules}
        if len(ids) != len(self.rules) or {r.family for r in self.rules} != FAMILIES:
            raise ValueError('Every check family and unique rule identity is required.')
        structural = {r.rule_id for r in self.rules if r.family == 'structural'}
        if (len(set(self.media_rule_ids)) != len(self.media_rule_ids)
                or not set(self.media_rule_ids) <= structural
                or self.media_applicable != bool(self.media_rule_ids)):
            raise ValueError('Applicable media integrity checks must be explicit.')
        return self


class CheckResult(Frozen):
    rule_id: Name
    outcome: Literal['pass', 'fail', 'flag', 'not_assessed']
    evidence_ref: Handle


class RecordQuality(Frozen):
    unit_ref: Handle
    content_sha256: Hash
    checks: Annotated[tuple[CheckResult, ...], Field(min_length=1, max_length=100)]
    stratum: Stratum
    provenance_known: bool


def classify(record, pack):
    rules = {r.rule_id: r for r in pack.rules}
    outcomes = {r.rule_id: r for r in record.checks}
    if len(outcomes) != len(record.checks) or set(outcomes) != set(rules):
        raise ValueError('Assessment bitmap must cover the entire confirmed pack exactly once.')
    rank = {'Clean': 0, 'Repairable': 1, 'Suspect': 2, 'Junk': 3}
    ceiling = 'Clean' if record.provenance_known else 'Suspect'
    for key, result in outcomes.items():
        value = (rules[key].failure_stratum if result.outcome == 'fail'
                 else 'Suspect' if result.outcome in {'flag', 'not_assessed'} else 'Clean')
        ceiling = max((ceiling, value), key=rank.get)
    return ceiling


class QualityRegister(Frozen):
    version: Literal['akki.quality.metadata/1']
    snapshot_sha256: Hash
    pack: QualityPack
    policy_receipt_ref: Hash
    population_receipt_ref: Hash
    population_refs: Annotated[tuple[Handle, ...], Field(min_length=1, max_length=500)]
    records: Annotated[tuple[RecordQuality, ...], Field(min_length=1, max_length=500)]
    counts: dict[Stratum, Annotated[int, Field(ge=0)]]
    accuracy: Literal['not_measured']

    @model_validator(mode='after')
    def reconciles(self):
        population = set(self.population_refs)
        if (len(population) != len(self.population_refs)
                or len({r.unit_ref for r in self.records}) != len(self.records)
                or {r.unit_ref for r in self.records} != population):
            raise ValueError('Exact pinned population reconciliation is required.')
        totals = Counter()
        for record in self.records:
            if classify(record, self.pack) != record.stratum:
                raise ValueError('Stratum does not follow the confirmed bitmap.')
            totals[record.stratum] += 1
        if self.counts != {s: totals[s] for s in ('Clean', 'Repairable', 'Suspect', 'Junk')}:
            raise ValueError('Garbage-register counts must reconcile exactly.')
        return self