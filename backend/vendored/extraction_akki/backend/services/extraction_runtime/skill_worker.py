"""Deterministic grounded-retrieval skill executor. Runs only inside an admitted runtime, never in E1.

Modes (dispatched from structured_records_worker.execute):
  skill_prepare · skill_register · skill_window · handoff_ack · skill_submit · skill_response · anchor
The answer is the set of whole qualified units whose terms match the question, sealed as a five-ring
JSONL artefact in the tenant's store; every anchor is the content hash of one such unit, attested
on a separately controlled runtime. No model, no paraphrase, no source read — the sealed corpus only.
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

from services.extraction_runtime import worker_identity as identity

FRAME_REF = 'akki://frame/deterministic-unit-retrieval/v1'
MODEL_ID = 'deterministic.unit_retrieval.v1'
TOKENIZER_DEFINITION = 'unit_terms/v1: lowercase [a-z0-9][a-z0-9_]{2,} minus the fixed stop list; one token = one whole unit'
WINDOW_TOKENS = 100000
RESERVED_TOKENS = 0
MAX_ANCHORS = 8
FAMILIES = ('structural', 'sentinel', 'cross_field', 'duplicate', 'cross_source', 'plausibility', 'provenance')
RANK = {'Clean': 0, 'Repairable': 1, 'Suspect': 2, 'Junk': 3}
SENTINELS = {'', 'null', 'none', 'n/a', 'na', '-', '--', '?', 'undefined', 'nan', '0000-00-00', '0000-00-00 00:00:00'}


def digest(value):
    return identity.digest(value)


def tokenizer_sha256():
    return hashlib.sha256(TOKENIZER_DEFINITION.encode()).hexdigest()


def snapshot_sha256(corpus):
    return digest({'corpus_slice_ref': corpus['ref'], 'artifact_sha256': corpus['sha256'], 'size_bytes': int(corpus['size_bytes'])})


RULES = [
    ('five_rings_present', 'structural', 'Junk', 'every line parses as JSON and carries provenance, signal, relational, reextraction_handle and defensibility'),
    ('no_sentinel_values', 'sentinel', 'Repairable', 'no record field equals a known sentinel placeholder (null, n/a, -, 0000-00-00, ...)'),
    ('primary_key_locator_consistent', 'cross_field', 'Suspect', 'record[primary_key] equals provenance.locator.key_value for every unit'),
    ('unit_id_unique', 'duplicate', 'Junk', 'no two units share a unit_id'),
    ('cross_source_corroboration', 'cross_source', 'Suspect', 'a second independent source corroborates the unit; not assessed by this executor'),
    ('completeness_floor', 'plausibility', 'Repairable', 'median signal.dimensions.completeness >= 0.5'),
    ('provenance_ring_resolves', 'provenance', 'Junk', 'provenance.source_ref and locator.database/table are present on every unit'),
]


def quality_pack(version):
    return {'version': version, 'media_applicable': False, 'media_rule_ids': [],
            'rules': [{'rule_id': rid, 'family': fam, 'definition_sha256': hashlib.sha256(text.encode()).hexdigest(), 'failure_stratum': stratum}
                      for rid, fam, stratum, text in RULES]}


def classify(checks, provenance_known, pack):
    failure = {r['rule_id']: r['failure_stratum'] for r in pack['rules']}
    ceiling = 'Clean' if provenance_known else 'Suspect'
    for check in checks:
        value = failure[check['rule_id']] if check['outcome'] == 'fail' else 'Suspect' if check['outcome'] in ('flag', 'not_assessed') else 'Clean'
        ceiling = max((ceiling, value), key=RANK.get)
    return ceiling


def parse_units(body):
    rows, broken = [], 0
    for position, line in enumerate(body.split(b'\n')):
        if not line.strip():
            continue
        try:
            unit = json.loads(line)
            rows.append({'position': position, 'line': line, 'unit': unit, 'content_sha256': hashlib.sha256(line).hexdigest()})
        except ValueError:
            broken += 1
    return rows, broken


def assess(rows, broken):
    """Seven check families over the whole sealed artefact; outcomes are facts about the population, not accuracy."""
    rings = {'provenance', 'signal', 'relational', 'reextraction_handle', 'defensibility'}
    five = all(rings <= set(r['unit']) for r in rows) and broken == 0 and bool(rows)
    sentinel_hits = sum(1 for r in rows for v in (r['unit'].get('record') or {}).values() if isinstance(v, str) and v.strip().lower() in SENTINELS)
    pk_ok = all(str((r['unit'].get('record') or {}).get(r['unit'].get('provenance', {}).get('locator', {}).get('primary_key'))) ==
                str(r['unit'].get('provenance', {}).get('locator', {}).get('key_value')) for r in rows)
    ids = [r['unit'].get('unit_id') for r in rows]
    completeness = sorted(float(r['unit'].get('signal', {}).get('dimensions', {}).get('completeness', 0)) for r in rows)
    median = completeness[len(completeness) // 2] if completeness else 0.0
    provenance = all(r['unit'].get('provenance', {}).get('source_ref') and r['unit'].get('provenance', {}).get('locator', {}).get('database')
                     and r['unit'].get('provenance', {}).get('locator', {}).get('table') for r in rows)
    outcomes = {'five_rings_present': 'pass' if five else 'fail', 'no_sentinel_values': 'pass' if sentinel_hits == 0 else 'fail',
                'primary_key_locator_consistent': 'pass' if pk_ok else 'fail', 'unit_id_unique': 'pass' if len(set(ids)) == len(ids) else 'fail',
                'cross_source_corroboration': 'not_assessed', 'completeness_floor': 'pass' if median >= 0.5 else 'fail',
                'provenance_ring_resolves': 'pass' if provenance else 'fail'}
    return outcomes, {'units_total': len(rows), 'broken_lines': broken, 'sentinel_hits': sentinel_hits, 'median_completeness': median,
                      'duplicate_unit_ids': len(ids) - len(set(ids))}


def _store(control):
    from services.extraction_runtime.structured_records_worker import _Store
    return _Store(control['secrets']['object_store'])


def _job(control):
    from services.extraction_runtime.structured_records_worker import _job_dir
    return _job_dir(control)


def _load_corpus(control):
    corpus = control['corpus']
    body = _store(control).get(corpus['key'])
    if hashlib.sha256(body).hexdigest() != corpus['sha256'] or len(body) != int(corpus['size_bytes']):
        raise ValueError('ARTIFACT_DIGEST_MISMATCH')
    return body


def _sign(control, category, claim, **kw):
    from services.extraction_runtime.structured_records_worker import _sign_observation
    return _sign_observation(control, category, control['request_sha256'], claim, **kw)


def _state(control, name, value=None):
    from services.extraction_runtime.structured_records_worker import _read, _write
    path = _job(control) / name
    if value is None:
        return _read(path)
    _write(path, value)
    return value


# ----------------------------------------------------------------------------- commission-time measurements

def skill_prepare(control):
    body = _load_corpus(control)
    rows, broken = parse_units(body)
    outcomes, facts = assess(rows, broken)
    snapshot = snapshot_sha256(control['corpus'])
    claim = {'snapshot_sha256': snapshot, 'population_refs': [control['corpus']['ref']]}
    prepared = {'outcomes': outcomes, 'facts': facts, 'snapshot_sha256': snapshot, 'corpus': control['corpus'], 'code_sha256': control['code_sha256']}
    _state(control, 'prepare.json', prepared)
    return {'status': 'complete', 'snapshot_sha256': snapshot, 'facts': facts, 'outcomes': outcomes,
            'receipt': _sign(control, 'quality_population', claim)}


def register_dict(prepared, pack, policy_ref, population_ref, request_id):
    corpus = prepared['corpus']
    checks = [{'rule_id': r['rule_id'], 'outcome': prepared['outcomes'][r['rule_id']],
               'evidence_ref': f"akki://evidence/{corpus['tenant_id']}/{request_id}/{r['rule_id']}"} for r in pack['rules']]
    stratum = classify(checks, True, pack)
    record = {'unit_ref': corpus['ref'], 'content_sha256': corpus['sha256'], 'checks': checks, 'stratum': stratum, 'provenance_known': True}
    counts = {s: (1 if s == stratum else 0) for s in ('Clean', 'Repairable', 'Suspect', 'Junk')}
    return {'version': 'akki.quality.metadata/1', 'snapshot_sha256': prepared['snapshot_sha256'], 'pack': pack,
            'policy_receipt_ref': policy_ref, 'population_receipt_ref': population_ref, 'population_refs': [corpus['ref']],
            'records': [record], 'counts': counts, 'accuracy': 'not_measured'}


def skill_register(control):
    prepared = _state(control, 'prepare.json')
    if prepared is None:
        return {'status': 'failed', 'reason_code': 'SKILL_PREPARE_MISSING'}
    register = register_dict(prepared, control['quality_pack'], control['policy_receipt_ref'], control['population_receipt_ref'], control['request_id'])
    _state(control, 'register.json', register)
    return {'status': 'complete', 'stratum': register['records'][0]['stratum'],
            'receipt': _sign(control, 'quality_register', register, typed={'quality_register': register})}


def window_dict(prepared, ranking_rule_ref, qualified_set_receipt_ref, objective_sha256):
    corpus = prepared['corpus']
    unit = {'unit_ref': corpus['ref'], 'content_sha256': corpus['sha256'], 'reextraction_ref': corpus['ref'], 'class_label': 'utterance',
            'tokens': max(1, int(prepared['facts']['units_total'])), 'proximity': 0, 'source_position': 0, 'memory_receipt_ref': None}
    return {'version': 'akki.context.metadata/1', 'objective_sha256': objective_sha256, 'frame_ref': FRAME_REF,
            'model_sha256': prepared['code_sha256'], 'tokenizer_sha256': tokenizer_sha256(), 'ranking_rule_ref': ranking_rule_ref,
            'qualified_set_receipt_ref': qualified_set_receipt_ref, 'load_bearing_refs': [corpus['ref']],
            'window_tokens': WINDOW_TOKENS, 'reserved_tokens': RESERVED_TOKENS, 'units': [unit], 'selected_refs': [corpus['ref']],
            'excluded_counts': {'fact': 0, 'inference': 0, 'utterance': 0, 'non_factual': 0}, 'top_excluded_handles': [], 'loss_disclosed': False}


def context_policy_committed(code_sha256, corpus_ref):
    return {'frame_ref': FRAME_REF, 'model_sha256': code_sha256, 'tokenizer_sha256': tokenizer_sha256(),
            'load_bearing_refs': [corpus_ref], 'window_tokens': WINDOW_TOKENS, 'reserved_tokens': RESERVED_TOKENS}


def skill_window(control):
    prepared = _state(control, 'prepare.json')
    if prepared is None:
        return {'status': 'failed', 'reason_code': 'SKILL_PREPARE_MISSING'}
    window = window_dict(prepared, control['ranking_rule_ref'], control['qualified_set_receipt_ref'], control['objective_sha256'])
    return {'status': 'complete', 'window': window, 'receipt': _sign(control, 'context_window', window, typed={'context_window': window})}


def handoff_ack(control):
    """The receiver of record acknowledges the contract on its own runtime; the ack is a fact about this job directory."""
    contract = control['contract']
    _state(control, 'handoff.json', {'contract': contract, 'acknowledged_epoch': int(time.time())})
    return {'status': 'acknowledged', 'receipt_id': 'hak-' + digest(contract)[:32], 'contract_sha256': digest(contract)}


# ----------------------------------------------------------------------------- execution

def skill_submit(control):
    from services.extraction_runtime.structured_records_worker import (_read, _result, _usage, _measurements, _receipted, Limiter,
                                                                        unit_terms, _unit_text, _relational_keys)
    job = _job(control)
    existing = _read(job / 'result.json')
    if existing is not None:
        return existing
    envelope = _read(job / 'envelope.json')
    if envelope is None:
        return _result(control, 'failed', 'RUNTIME_LIMITS_NOT_ADMITTED')
    limiter = Limiter(envelope)
    control = {**control, 'envelope': envelope}
    try:
        corpus = control['corpus']
        limiter.before_batch({('bytes_read', 'bytes'): int(corpus['size_bytes'])})
        body = _load_corpus(control)
        rows, broken = parse_units(body)
        wanted = set(control.get('terms') or [])
        for row in rows:
            row['overlap'] = len(wanted & unit_terms(_unit_text(row['unit'])))
            row['rel_keys'] = _relational_keys(row['unit'])
        matched = [r for r in rows if r['overlap'] > 0]
        matched.sort(key=lambda r: (-r['overlap'], r['position'], r['unit']['unit_id']))
        chosen = matched[:int(control.get('max_candidates', 64))]
        keys = set().union(*(r['rel_keys'] for r in chosen)) if chosen else set()
        chosen_ids = {r['unit']['unit_id'] for r in chosen}
        neighbours = sorted((r for r in rows if r['unit']['unit_id'] not in chosen_ids and r['rel_keys'] & keys), key=lambda r: r['position'])
        selected = chosen + neighbours[:int(control.get('max_neighbours', 16))]
        if ('bytes_read', 'bytes') in limiter.used:
            limiter.used[('bytes_read', 'bytes')] = float(len(body))
        if not chosen:
            refusal = {'request_ref': control['intent_receipt_ref'], 'outcome': 'refused', 'reason_code': 'OUT_OF_SCOPE'}
            receipts = _measurements(control, limiter, 0)
            receipts['refusal'] = _sign(control, 'refusal', refusal, typed={'refusal': refusal})
            result = _result(control, 'failed', 'OUT_OF_SCOPE', usage=_usage(limiter.quantities(0)),
                             extra={'receipts': receipts, 'retrieval': {'units_total': len(rows), 'matched_total': 0, 'terms_count': len(wanted)}})
        else:
            answer = b''.join(r['line'] + b'\n' for r in selected)
            sha256, size = hashlib.sha256(answer).hexdigest(), len(answer)
            store = _store(control)
            etag = store.put(control['object_key'], answer)
            artifact = {'ref': control['artifact_ref'], 'sha256': sha256, 'size_bytes': size, 'tenant_id': control['tenant_id'], 'class_label': 'utterance'}
            lineage = {'version': 'akki.lineage.metadata/1', 'artifact_ref': artifact['ref'], 'artifact_sha256': sha256,
                       'parents': list(control['parent_refs'])}
            receipts = _measurements(control, limiter, len(selected))
            receipts['lineage'] = _sign(control, 'lineage', lineage, typed={'lineage': lineage})
            anchors = [r['content_sha256'] for r in chosen[:MAX_ANCHORS]]
            result = _result(control, 'complete', 'GROUNDED_UNITS_SEALED', artifacts=[artifact], usage=_usage(limiter.quantities(len(selected))),
                             extra={'receipts': receipts, 'object': {'provider': store.provider, 'bucket': store.bucket, 'key': control['object_key'],
                                                                     'etag': etag, 'size': size},
                                    'retrieval': {'units_total': len(rows), 'broken_lines': broken, 'matched_total': len(matched),
                                                  'returned': len(selected), 'neighbours': len(selected) - len(chosen),
                                                  'anchor_sha256s': anchors, 'terms_count': len(wanted), 'model': MODEL_ID}})
    except Exception as exc:  # classified locally; never raw diagnostics
        reason = str(exc) if str(exc).isupper() or str(exc).split(':')[0].isupper() else type(exc).__name__
        result = _result(control, 'failed', reason[:120], usage=_usage(limiter.quantities(0)), extra={'receipts': _measurements(control, limiter, 0)})
    result = _receipted(result)
    from services.extraction_runtime.structured_records_worker import _write
    _write(job / 'result.json', result)
    return result


def skill_response(control):
    from services.extraction_runtime.structured_records_worker import _read
    result = _read(_job(control) / 'result.json')
    if result is None or result.get('state') != 'complete':
        return {'status': 'failed', 'reason_code': 'SKILL_RESULT_MISSING'}
    artifact = result['artifacts'][0]
    grounding = {'query_ref': control['query_ref'], 'answer_sha256': artifact['sha256'],
                 'anchors': [{'snapshot_sha256': a['snapshot_sha256'], 'anchor_sha256': a['anchor_sha256'], 'source_receipt_ref': a['source_receipt_ref']}
                             for a in control['anchors']],
                 'context_lost': False, 'context_loss_disclosed': False}
    expected = set(result.get('retrieval', {}).get('anchor_sha256s', []))
    if not grounding['anchors'] or any(a['anchor_sha256'] not in expected for a in grounding['anchors']):
        return {'status': 'failed', 'reason_code': 'ANCHOR_SET_MISMATCH'}
    claim = {'request_sha256': control['request_sha256'], 'artifact': artifact, 'grounding': grounding}
    return {'status': 'complete', 'grounding': grounding, 'receipt': _sign(control, 'skill_response', claim, typed={'grounding': grounding})}


def anchor(control):
    """Independent attestation: each anchor is a byte-identical unit line present in the sealed corpus AND in the answer."""
    store = _store(control)
    corpus_body = store.get(control['corpus']['key'])
    answer_body = store.get(control['answer']['key'])
    if (hashlib.sha256(corpus_body).hexdigest() != control['corpus']['sha256']
            or hashlib.sha256(answer_body).hexdigest() != control['answer']['sha256']):
        return {'status': 'failed', 'reason_code': 'ARTIFACT_DIGEST_MISMATCH', 'verified': False, 'receipts': []}
    in_corpus = {hashlib.sha256(l).hexdigest() for l in corpus_body.split(b'\n') if l.strip()}
    in_answer = {hashlib.sha256(l).hexdigest() for l in answer_body.split(b'\n') if l.strip()}
    receipts, verified = [], True
    for anchor_sha256 in control['anchor_sha256s']:
        present = anchor_sha256 in in_corpus and anchor_sha256 in in_answer
        verified = verified and present
        if present:
            claim = {'snapshot_sha256': control['snapshot_sha256'], 'anchor_sha256': anchor_sha256,
                     'answer_sha256': control['answer']['sha256'], 'query_ref': control['query_ref']}
            receipts.append({'anchor_sha256': anchor_sha256, 'receipt': _sign(control, 'anchor', claim)})
    return {'status': 'complete' if verified else 'failed', 'verified': verified, 'receipts': receipts,
            'answer_units': len(in_answer), 'answer_subset_of_corpus': in_answer <= in_corpus}


MODES = {'skill_prepare': skill_prepare, 'skill_register': skill_register, 'skill_window': skill_window, 'handoff_ack': handoff_ack,
         'skill_submit': skill_submit, 'skill_response': skill_response, 'anchor': anchor}
