"""Kind profiles: the only thing in the orchestration that knows a domain.

A KindProfile names what a job kind ships, measures, enforces, prices — and what it costs to run:
its compute class (cpu, gpu, or mixed with the split named per class) and the unit of work each
class scales with. It never names a runtime, a host or a tenant; dispatch selects an admitted
runtime whose descriptor has the class, the headroom and the reach. A kind with no compute class
is not routable. New domains register a row here and nothing in the Coordinator changes.
"""
from dataclasses import dataclass, field
from services.work_supervisor.kind_registry import register_kind

COMPUTE_CLASSES = ('cpu', 'gpu', 'mixed')
SCALING_UNITS = ('scanned_records', 'bytes_read', 'media_duration', 'tokens', 'training_steps')
CLASS_UNIT = {'cpu': 'cpu_seconds', 'gpu': 'gpu_seconds'}
BOUND_OF = {'scanned_records': ('records', lambda b: int(b['max_records']) * 2),
            'returned_records': ('records', lambda b: int(b['max_records'])),
            'bytes_read': ('bytes', lambda b: int(b['max_records']) * int(b.get('estimated_row_bytes', 512)) * 4),
            'media_duration': ('seconds', lambda b: int(b['max_media_seconds'])),
            'tokens': ('tokens', lambda b: int(b['max_tokens'])),
            'training_steps': ('steps', lambda b: int(b['max_steps'])),
            'wall_clock': ('seconds', lambda b: int(b['max_seconds'])),
            'spend': ('USD', lambda b: b.get('spend_usd', 0))}
DECLARED_PRIOR = 'declared_prior_pending_measurement'


@dataclass(frozen=True)
class KindProfile:
    job_kind: str
    request_kind: str
    engine: str
    purposes: tuple
    output_class: str
    output_contract: dict
    enforced_dimensions: tuple
    default_bounds: dict
    price_line: str
    custody_floor: str
    ladder_rung: str
    operations: tuple
    acceptance_rules: tuple
    quality_matrix_row: str
    compute_class: str
    scaling: dict
    sizing_rates: dict
    touches_source_data: bool = True
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.compute_class not in COMPUTE_CLASSES:
            raise ValueError('KIND_NOT_ROUTABLE_WITHOUT_COMPUTE_CLASS:' + self.job_kind)
        classes = {'cpu', 'gpu'} if self.compute_class == 'mixed' else {self.compute_class}
        if set(self.scaling) != classes or set(self.sizing_rates) != classes:
            raise ValueError('KIND_COMPUTE_SPLIT_UNNAMED:' + self.job_kind)
        if any(unit not in SCALING_UNITS for unit in self.scaling.values()):
            raise ValueError('KIND_SCALING_UNIT_UNKNOWN:' + self.job_kind)
        if any({'seconds_per_unit', 'memory_gb', 'overhead_seconds'} - set(rate) for rate in self.sizing_rates.values()):
            raise ValueError('KIND_SIZING_RATE_INCOMPLETE:' + self.job_kind)
        if 'active_compute' not in self.enforced_dimensions or 'wall_clock' not in self.enforced_dimensions:
            raise ValueError('KIND_COMPUTE_NOT_ENFORCED:' + self.job_kind)

    @property
    def compute_classes(self):
        return tuple(sorted(self.scaling))

    def scale(self, bounds):
        """The frozen request's scale in each class's scaling unit; upper bounds, never estimates."""
        return {unit: BOUND_OF[unit][1](bounds) for unit in set(self.scaling.values())}

    def limits(self, bounds, sizing):
        """Plan limits in the seven-dimension vocabulary; every enforced dimension is bounded and the
        compute reservation is one active_compute entry per class, sized by `work_orders.sizing`."""
        rows = []
        for dimension in self.enforced_dimensions:
            if dimension == 'active_compute':
                for cls in self.compute_classes:
                    rows.append({'dimension': 'active_compute', 'unit': CLASS_UNIT[cls],
                                 'quantity': str(int(sizing['classes'][cls]['reservation_seconds']))})
                continue
            unit, bound = BOUND_OF[dimension]
            rows.append({'dimension': dimension, 'unit': unit, 'quantity': str(bound(bounds))})
        return rows


def _profile(job_kind, request_kind, engine, purposes, output_class, compute_class, scaling, sizing_rates, *,
             enforced, bounds, operations=(), acceptance=(), touches_source_data=True, custody_floor='de_identified',
             ladder_rung='rung_1_deterministic', output_contract=None, quality_matrix_row='declaration_baseline',
             price_line='pilot.zero_rate', extra=None):
    return KindProfile(job_kind=job_kind, request_kind=request_kind, engine=engine, purposes=purposes,
                       output_class=output_class, output_contract=output_contract or {'kind': output_class},
                       enforced_dimensions=enforced, default_bounds=bounds, price_line=price_line,
                       custody_floor=custody_floor, ladder_rung=ladder_rung, operations=operations,
                       acceptance_rules=acceptance, quality_matrix_row=quality_matrix_row, compute_class=compute_class,
                       scaling=scaling, sizing_rates=sizing_rates, touches_source_data=touches_source_data,
                       extra={'sizing_rate_status': DECLARED_PRIOR, **(extra or {})})


CPU_RECORDS = ('spend', 'wall_clock', 'scanned_records', 'bytes_read', 'active_compute')
GPU_MEDIA = ('spend', 'wall_clock', 'media_duration', 'active_compute')

# M3-T1 — the first commissionable row. Deterministic SQL + regex floor: rung 1, CPU only.
STRUCTURED_RECORDS = _profile(
    'source.extract.structured_records.v1', 'source', 'mtafiti', ('extraction',), 'structured_records', 'cpu',
    {'cpu': 'scanned_records'}, {'cpu': {'seconds_per_unit': 0.002, 'memory_gb': 1, 'overhead_seconds': 20}},
    enforced=('spend', 'wall_clock', 'scanned_records', 'returned_records', 'bytes_read', 'active_compute'),
    bounds={'max_records': 500, 'max_seconds': 900, 'batch_size': 250, 'estimated_row_bytes': 512,
            'termination_grace_seconds': 60},
    operations=('browse_estate', 'processed_intelligence'),
    acceptance=('read_only_guard', 'schema_completeness', 'primary_key_present', 'duplicate_primary_key',
                'pii_floor_applied', 'independent_inspection', 'artifact_sha256_match'),
    output_contract={'kind': 'qualified_units_jsonl', 'five_rings': True, 'unqualified_partition': 'retained_not_delivered',
                     'class_label': 'utterance'},
    quality_matrix_row='structured_records:pending_first_verified_sample', price_line='pilot.zero_rate.structured_records')

# The census is the worked example of the split. Its structural walk is CPU and on a database estate
# that is the whole census; its perception passes are GPU and scale with media duration or tokens.
CENSUS_STRUCTURAL_WALK = _profile(
    'census.structural_walk.v1', 'source', 'mtafiti', ('census',), 'census_profile', 'cpu',
    {'cpu': 'scanned_records'}, {'cpu': {'seconds_per_unit': 0.0002, 'memory_gb': 2, 'overhead_seconds': 30}},
    enforced=CPU_RECORDS, bounds={'max_records': 250000, 'max_seconds': 3600, 'estimated_row_bytes': 256},
    acceptance=('read_only_guard', 'schema_completeness'), custody_floor='metadata_only',
    extra={'walk': ('schemas', 'counts', 'column_roles', 'sentinels', 'duplicates', 'foreign_keys', 'drift')})
CENSUS_PERCEPTION_TRANSCRIBE = _profile(
    'census.perception.transcribe.v1', 'source', 'mtafiti', ('census',), 'transcript_units', 'gpu',
    {'gpu': 'media_duration'}, {'gpu': {'seconds_per_unit': 0.05, 'memory_gb': 16, 'overhead_seconds': 120}},
    enforced=GPU_MEDIA, bounds={'max_media_seconds': 36000, 'max_seconds': 7200}, ladder_rung='rung_2_local_model')
CENSUS_PERCEPTION_LANGUAGE_ID = _profile(
    'census.perception.language_id.v1', 'source', 'mtafiti', ('census',), 'language_labels', 'gpu',
    {'gpu': 'media_duration'}, {'gpu': {'seconds_per_unit': 0.01, 'memory_gb': 8, 'overhead_seconds': 60}},
    enforced=GPU_MEDIA, bounds={'max_media_seconds': 36000, 'max_seconds': 3600}, ladder_rung='rung_2_local_model')
CENSUS_PERCEPTION_EMBED = _profile(
    'census.perception.embed.v1', 'source', 'mtafiti', ('census',), 'embeddings', 'gpu',
    {'gpu': 'tokens'}, {'gpu': {'seconds_per_unit': 0.00002, 'memory_gb': 12, 'overhead_seconds': 60}},
    enforced=('spend', 'wall_clock', 'scanned_records', 'active_compute'),
    bounds={'max_records': 100000, 'max_tokens': 50000000, 'max_seconds': 3600}, ladder_rung='rung_2_local_model')
CENSUS_PERCEPTION_IMAGE = _profile(
    'census.perception.image_classify.v1', 'source', 'mtafiti', ('census',), 'image_labels', 'gpu',
    {'gpu': 'bytes_read'}, {'gpu': {'seconds_per_unit': 0.00000005, 'memory_gb': 8, 'overhead_seconds': 60}},
    enforced=('spend', 'wall_clock', 'bytes_read', 'active_compute'),
    bounds={'max_records': 100000, 'max_seconds': 3600, 'estimated_row_bytes': 2000000}, ladder_rung='rung_2_local_model')
CENSUS_DEEP = _profile(
    'census.deep.v1', 'source', 'mtafiti', ('census',), 'census_profile', 'mixed',
    {'cpu': 'scanned_records', 'gpu': 'media_duration'},
    {'cpu': {'seconds_per_unit': 0.0002, 'memory_gb': 2, 'overhead_seconds': 30},
     'gpu': {'seconds_per_unit': 0.06, 'memory_gb': 16, 'overhead_seconds': 120}},
    enforced=('spend', 'wall_clock', 'scanned_records', 'bytes_read', 'media_duration', 'active_compute'),
    bounds={'max_records': 250000, 'max_media_seconds': 36000, 'max_seconds': 10800, 'estimated_row_bytes': 256},
    custody_floor='metadata_only',
    extra={'split': {'cpu': 'structural walk (schemas, counts, roles, sentinels, duplicates, FKs, drift)',
                     'gpu': 'perception passes (transcription, language id, embeddings, image classification)'},
           'rule': 'an estate with no media reserves no GPU: the gpu class is dropped when max_media_seconds is 0'})

# Cleanliness, extraction and report runs are CPU; training and local inference are GPU.
CLEANLINESS_RUN = _profile(
    'quality.cleanliness_run.v1', 'source', 'mtafiti', ('census',), 'quality_register', 'cpu',
    {'cpu': 'scanned_records'}, {'cpu': {'seconds_per_unit': 0.001, 'memory_gb': 2, 'overhead_seconds': 20}},
    enforced=CPU_RECORDS, bounds={'max_records': 250000, 'max_seconds': 3600, 'estimated_row_bytes': 512})
REPORT_RUN = _profile(
    'report.run.v1', 'source', 'mtafiti', ('extraction',), 'report_artifact', 'cpu',
    {'cpu': 'scanned_records'}, {'cpu': {'seconds_per_unit': 0.0005, 'memory_gb': 1, 'overhead_seconds': 10}},
    enforced=CPU_RECORDS, bounds={'max_records': 100000, 'max_seconds': 1800, 'estimated_row_bytes': 512},
    touches_source_data=False)
TRAINING_FINE_TUNE = _profile(
    'training.fine_tune.v1', 'training', 'targeta', ('training', 'evaluation'), 'model_artifact', 'gpu',
    {'gpu': 'training_steps'}, {'gpu': {'seconds_per_unit': 0.5, 'memory_gb': 80, 'overhead_seconds': 600}},
    enforced=('spend', 'wall_clock', 'active_compute'), bounds={'max_steps': 20000, 'max_seconds': 43200},
    ladder_rung='rung_3_trained_model', touches_source_data=False)
INFERENCE_LOCAL = _profile(
    'inference.local.v1', 'skill', 'solva', ('answering',), 'skill_response', 'gpu',
    {'gpu': 'tokens'}, {'gpu': {'seconds_per_unit': 0.00005, 'memory_gb': 40, 'overhead_seconds': 30}},
    enforced=('spend', 'wall_clock', 'active_compute'), bounds={'max_tokens': 200000, 'max_seconds': 600},
    ladder_rung='rung_2_local_model', touches_source_data=False)

REGISTRY = {p.job_kind: p for p in (
    STRUCTURED_RECORDS, CENSUS_STRUCTURAL_WALK, CENSUS_PERCEPTION_TRANSCRIBE, CENSUS_PERCEPTION_LANGUAGE_ID,
    CENSUS_PERCEPTION_EMBED, CENSUS_PERCEPTION_IMAGE, CENSUS_DEEP, CLEANLINESS_RUN, REPORT_RUN, TRAINING_FINE_TUNE,
    INFERENCE_LOCAL)}
for _kind in REGISTRY:
    register_kind(_kind)


def profile(job_kind):
    if job_kind not in REGISTRY:
        raise KeyError(job_kind)
    return REGISTRY[job_kind]


def profile_for_operation(operation):
    for value in REGISTRY.values():
        if operation in value.operations:
            return value
    return None


def engines_for_operation(operation):
    """Every (request_kind, engine) a registered kind profile admits for this DAP operation."""
    return {(p.request_kind, p.engine) for p in REGISTRY.values() if operation in p.operations}


def routable():
    """Every registered kind names its compute class and split; the registry refuses one that does not."""
    return {k: {'compute_class': p.compute_class, 'scaling': dict(p.scaling), 'request_kind': p.request_kind,
                'commissionable_operations': list(p.operations)} for k, p in REGISTRY.items()}
