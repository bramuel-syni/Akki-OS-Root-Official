"""Mα training supervisor — the caller ABOVE the sealed Solva v2 faculties and the CIF modules.

Canon 4 §19–27 (Solva): measured lane results are projected into evidence units; `reasoning_faculty` chooses the load-bearing set and
`assertion_boundary` computes the class (the one-way seam is kept by import: neither faculty is re-implemented here); every cycle leaves a
`SolvaTrace`, an intent audit (declared vs demonstrated) and, when nothing admissible remains, a `RefusalEnvelope` whose `lower_standard`
action is never offered for a governed floor. Canon 2 (CIF) + Doc-9 BR-9.2/9.4 + AC-18: every candidate change is an idea with a manifest,
authored as a `CIFProposal_v0` (`cif.detection`), decided only by `cif.acceptance_point` plus the read-only floor check, routed by
`cif.output_routing`, archived (adopted · not_yet_conditioned · unverified_provisional · superseded) with rent and a condition watcher;
the adopted hypothesis carries a prediction that is tested at settlement; two consecutive refutations of one correction class are the
absorption signature → naivety pass (frontier ideation with the inherited constraint struck) + an owner finding. Reflection
(`solva_v2.engines.reflection`) is HALTED by ruling and is recorded as such on every trace, never substituted. The owner holds the coach seat.
"""
import hashlib
import json
import logging
import math
import threading
from datetime import datetime, timedelta, timezone

from contracts.solva_reasoning import AssertionClass, RefusalAction, RefusalEnvelope, UnitRef
from services.cif.acceptance_point import is_accepted
from services.cif.detection import author_proposal
from services.cif.halt import get_halt_journal, halt, is_halted
from services.cif.output_routing import RoutingRefused, route_accepted_proposal
from services.solva_v2.assertion_boundary import compute_class
from services.solva_v2.engines import tension_detector
from services.solva_v2.intent_audit import open_intent_audit, update_intent_audit_demonstrated
from services.solva_v2.reasoning_faculty import identify_load_bearing_units
from services.solva_v2.trace import record_trace
from services.training_lab import store as lab
from services.wpw import tier1_notebook as wpw

log = logging.getLogger(__name__)
LANGUAGES = ('kik', 'kam', 'swa')
LANES = ('listener', 'story_text', 'story_voice')
COMMISSION_OF = {'listener': 'LISTEN-KIK-KAM-SWA', 'story_text': 'STORY-KIK-KAM-SWA', 'story_voice': 'STORY-KIK-KAM-SWA'}
FLOORS = {'listener': {'precision': 0.90, 'recall': 0.90}, 'story_text': {'language_fidelity_rate': 1.0, 'perplexity_ratio_to_base_below': 1.0},
          'story_voice': {'overall_similarity': 0.90, 'max_cosine_below': 0.40}}  # read-only: read here, never set or relaxed (Canon 4 §27)
PROTECTED = ('identity_cosine_threshold', 'split_version', 'include_internet_corpus', 'admission_target', 'dev_per_language', 'eval_prompts_per_language', 'eval_samples_per_language',
             'selection_policy', 'spectral_feedback', 'seed', 'worker_design_version', 'init_from', 'init_adapter', 'base_path', 'resume_from', 'carried_from_seal_version', 'max_segment_seconds')
TUNABLES = {  # only parameters the workers actually read; bounds are engineering registration, not quality claims
    'listener': {'base': {'enum': ['openai/whisper-small', 'openai/whisper-large-v3-turbo']}, 'lr': (1e-6, 3e-4), 'max_steps': (1000, 30000), 'batch_size': (4, 64), 'grad_accum': (1, 16), 'warmup_steps': (0, 2000),
                 'eval_every': (500, 5000), 'contextual_bias': bool, 'bias_prob': (0.0, 1.0), 'bias_distractors': (0, 20), 'bias_terms_per_language': (0, 200), 'mention_oversample': bool, 'language_balance': bool},
    'story_text': {'lr': (1e-5, 5e-4), 'max_steps': (500, 20000), 'batch_size': (1, 16), 'grad_accum': (1, 32), 'warmup_steps': (0, 1000), 'lora_r': {'enum': [8, 16, 32, 64]}, 'lora_alpha': (8, 128),
                   'lora_dropout': (0.0, 0.3), 'weight_decay': (0.0, 0.1), 'patience_evaluations': (2, 10), 'max_seq_len': {'enum': [512, 1024, 2048]}, 'language_balance': bool},
    'story_voice': {'lr': (1e-5, 1e-3), 'max_steps': (5000, 100000), 'batch_size': (8, 96), 'warmup_steps': (0, 5000), 'identity_noise': (0.1, 2.0), 'identity_margin': (0.0, 0.15), 'identity_candidates': (50, 1000),
                    'identity_conditioning': bool, 'dense_identity': bool, 'loudness_match': bool, 'language_balance': bool},
}
MIN_DELTA = {'listener': 0.02, 'story_text': 0.05, 'story_voice': 0.02}
RENT_DAYS = 14
ABSORPTION_REFUTATIONS = 2
FREE_DEVICE = 'a free device after the adopted hypothesis settles; re-qualified then with zero inherited credibility'
DECLARED_SITUATION = 'inquiry: reach the frozen target outcome through qualified, one-at-a-time changes; the floors are not negotiable'
REFLECTION_NOTE = 'reflection:HALTED (DPO-S2 — case-agnostic reflection question set not owner-ruled; selection uses the deterministic rank, not a substitute reflection)'
LOWER_STANDARD_NOTE = 'the 0.90/0.90 mention floors, the <0.40 identity cosine and the seal are governed floors; Solva reads them and never relaxes them (Canon 4 §27)'
CANON_REFS = ('canon4:§19-27 Solva', 'canon2:§7-§11 CIF manifests/archive/detection', 'doc9:BR-9.2 single-experiment acceptance point', 'AC-18 proposes-never-ratifies')
STRUCK = {'listener': 'more steps or a larger Whisper base on the same transcript signal will close the recall gap',
          'story_text': 'perplexity-selected adapters on radio transcripts are the right signal for story quality',
          'story_voice': 'continuing the same codec-LM weights with a resampled identity will clear the rendered-identity gate'}


def db():
    database = lab.db()
    database.malpha_hypotheses.create_index('hypothesis_id', unique=True)
    database.malpha_hypotheses.create_index([('lane', 1), ('archive_state', 1)])
    database.malpha_supervisor_cycles.create_index([('lane', 1), ('at', -1)])
    return database


def now():
    return lab.now()


def _num(v):
    return v if type(v) in (int, float) and math.isfinite(v) else None


def _hid(*parts):
    return 'hyp-' + hashlib.sha256('|'.join(str(p) for p in parts).encode()).hexdigest()[:12]


# ----------------------------------------------------------------------------- Solva: evidence units → load-bearing set → class → trace
def evidence_units(lane, job):
    """Projection of one settled result into units (value, field, language, basis). Never copies text, paths or identities."""
    dev = ((job.get('result') or {}).get('dev') or {}); units = []
    for lang in LANGUAGES:
        if lane == 'listener':
            m = (dev.get('mentions') or {}).get(lang) or {}
            basis = 'native_verified' if (m.get('evidence') or {}).get('reference_verified') else 'transcript_derived'
            rows = [('precision', m.get('precision'), basis), ('recall', m.get('recall'), basis), ('wer', ((dev.get('words') or {}).get(lang) or {}).get('wer'), 'transcript_derived')]
        elif lane == 'story_text':
            p = (dev.get('per_language') or {}).get(lang) or {}
            ratio = (p['dev_perplexity'] / p['base_perplexity']) if _num(p.get('dev_perplexity')) and _num(p.get('base_perplexity')) and p['base_perplexity'] > 0 else None
            rows = [('language_fidelity_rate', p.get('language_fidelity_rate'), 'character_trigram_proxy'), ('perplexity_ratio_to_base', ratio, 'transcript_perplexity_proxy'), ('dev_perplexity', p.get('dev_perplexity'), 'transcript_perplexity_proxy')]
        else:
            p = (dev.get('per_language') or {}).get(lang) or {}
            rows = [('overall_similarity', (p.get('behaviour') or {}).get('overall_similarity'), 'measured_acoustic_distribution'),
                    ('max_cosine', (p.get('identity_gate') or {}).get('max_cosine_to_any_corpus_speaker'), 'measured_rendered_identity')]
        for field, value, basis in rows:
            value = _num(value)
            if value is not None: units.append({'unit_id': f"{job['job_id']}#dev.{field}.{lang}", 'field': field, 'language': lang, 'value': round(value, 4), 'basis': basis, 'iteration': job.get('iteration')})
    return units


def _value(units, field, lang):
    return next((u['value'] for u in units if u['field'] == field and u['language'] == lang), None)


def _shortfall(lane, units, lang):
    if lane == 'listener':
        p, r = _value(units, 'precision', lang), _value(units, 'recall', lang)
        return {'precision': round(FLOORS[lane]['precision'] - p, 4) if p is not None else None, 'recall': round(FLOORS[lane]['recall'] - r, 4) if r is not None else None}
    if lane == 'story_text':
        f, ratio = _value(units, 'language_fidelity_rate', lang), _value(units, 'perplexity_ratio_to_base', lang)
        return {'language_fidelity_rate': round(1.0 - f, 4) if f is not None else None, 'perplexity_ratio_to_base': round(ratio - 1.0, 4) if ratio is not None else None}
    s, c = _value(units, 'overall_similarity', lang), _value(units, 'max_cosine', lang)
    return {'overall_similarity': round(FLOORS[lane]['overall_similarity'] - s, 4) if s is not None else None, 'max_cosine': round(c - FLOORS[lane]['max_cosine_below'], 4) if c is not None else None}


GATE_FIRST = {'story_voice': ('max_cosine', 'overall_similarity'), 'story_text': ('language_fidelity_rate', 'perplexity_ratio_to_base')}  # a failing safety/fidelity gate bears the load before a quality metric (AIP §§6–7)


def _target(lane, shortfall):
    """(worst language, load-bearing field): gate-first where a gate exists, otherwise the largest shortfall; a met floor (≤ 0) never bears the load while another fails."""
    fields = GATE_FIRST.get(lane) or tuple(next(iter(shortfall.values())).keys())
    for field in fields:
        failing = [(shortfall[l][field], l) for l in LANGUAGES if shortfall[l].get(field) is not None and shortfall[l][field] > 0]
        if failing and lane in GATE_FIRST: return max(failing)[1], field
    scored = [(v, l, k) for l in LANGUAGES for k, v in shortfall[l].items() if v is not None]
    if not scored: return None, None
    v, l, k = max(scored)
    return l, k


def gap(lane, history):
    """Clarity: where the latest reading stands against the read-only floors, which units bear the load, and the class those units allow."""
    latest = history[-1] if history else None
    units = evidence_units(lane, latest) if latest else []
    shortfall = {lang: _shortfall(lane, units, lang) for lang in LANGUAGES}
    worst, target_field = _target(lane, shortfall)
    worst_of = lambda lang: max((v for v in shortfall[lang].values() if v is not None), default=None)  # noqa: E731
    direction = None if not worst else ('down' if target_field in ('perplexity_ratio_to_base', 'max_cosine') else 'up')
    load_bearing = identify_load_bearing_units([UnitRef(unit_id=u['unit_id']) for u in units if worst and u['language'] == worst and u['field'] in shortfall[worst]])
    klass = compute_class(load_bearing)
    met = bool(worst) and worst_of(worst) <= 0
    if klass is AssertionClass.NON_FACTUAL: conclusion = f'{lane}: no measured reading yet; nothing is asserted about the floors.'
    else:
        basis = '/'.join(sorted({u['basis'] for u in units if u['language'] == worst}))
        reading = ', '.join(f"{u['field']} {u['value']}" for u in units if u['language'] == worst and u['field'] in shortfall[worst])
        conclusion = (f"{lane}: {basis} readings state that {worst} measures {reading}; " + ('every floor is met on this reading' if met else f"the load-bearing shortfall is {target_field} ({shortfall[worst][target_field]:+.4f} against the floor)")
                      + ". Asserted at utterance class — 'was stated' by dev labels that are transcript-derived, not native-verified; the sealed native read decides admission.")
    return {'lane': lane, 'iteration': latest.get('iteration') if latest else 0, 'units': units, 'shortfall': shortfall, 'worst_language': worst, 'target_field': target_field, 'direction': direction,
            'floors': FLOORS[lane], 'floors_met_on_dev': met, 'load_bearing': [u.unit_id for u in load_bearing.units], 'tensions': [(a.unit_id, b.unit_id) for a, b in tension_detector.run(load_bearing.units)],
            'class': klass.value, 'conclusion': conclusion, 'load_bearing_set': load_bearing}


# ----------------------------------------------------------------------------- CIF: ideas with manifests, the acceptance point
def correction_class(lane, recipe, previous):
    previous = previous or {}
    if lane == 'listener':
        if previous and recipe.get('base') != previous.get('base'): return 'base_change'
        return 'continue_from_artefact' if recipe.get('init_from') else 'fresh_ladder_step'
    if lane == 'story_text': return 'continue_adapter' if recipe.get('init_adapter') else ('restart_regularised' if previous else 'first_pass')
    if previous and recipe.get('identity_conditioning') and not previous.get('identity_conditioning'): return 'identity_mechanism'
    if previous and (recipe.get('identity_noise') or 0) > (previous.get('identity_noise') or 0): return 'identity_resample'
    return 'continue_weights' if recipe.get('init_from') else 'first_pass'


def _prediction(lane, g):
    if not g['worst_language']: return {'field': None, 'language': None, 'direction': None, 'min_delta': MIN_DELTA[lane], 'note': 'no measured baseline; the first reading is the baseline'}
    return {'field': g['target_field'], 'language': g['worst_language'], 'direction': g['direction'], 'min_delta': MIN_DELTA[lane]}


def ladder_hypothesis(lane, iteration, recipe, history, g):
    previous = ((history[-1].get('result') or {}).get('recipe') or {}) if history else {}
    klass = correction_class(lane, recipe, previous); pred = _prediction(lane, g)
    hid = _hid('ladder', lane, iteration, klass, json.dumps({k: recipe.get(k) for k in sorted(TUNABLES[lane])}, sort_keys=True, default=str))
    return {'hypothesis_id': hid, 'lane': lane, 'origin': 'measurement_rule' if history else 'planned_ladder', 'correction_class': klass, 'statement': recipe.get('rationale') or f'{lane} planned recipe step {iteration}',
            'manifest': [{'assumption': f"the {klass} change still addresses the load-bearing gap ({pred['field']} for {pred['language']})", 'class': 'inferred', 'flips_if': f"{pred['field']} for {pred['language']} does not move {pred['direction']} by ≥ {pred['min_delta']} after this iteration"},
                         {'assumption': 'transcript-derived dev labels are a usable proxy for the sealed native read', 'class': 'recalled', 'flips_if': 'native confirmation-panel labels disagree materially with transcript-derived labels'},
                         {'assumption': 'more steps on the same signal can still move the metric', 'class': 'inferred', 'flips_if': f'{ABSORPTION_REFUTATIONS} consecutive same-class iterations are refuted (absorption signature)'}],
            'prediction': pred, 'recipe_delta': {}, 'evidence_refs': g['load_bearing'], 'citations': list(g['load_bearing']) + [f'malpha://recipe/{lane}#iteration{iteration}', *CANON_REFS], 'review_verdict': None}


def frontier_hypotheses(lane, g):
    """Frontier ideation (planner + independent-family reviewer) enters the archive as ideas; a bounded recipe_delta makes an idea executable."""
    out = []; coll = db().malpha_hypotheses
    for review in db().malpha_learning_reviews.find({'status': 'reviewed'}, {'_id': 0, 'review_id': 1, 'proposal.experiments': 1, 'review.verdict': 1, 'review.required_changes': 1, 'naivety_pass': 1}):
        for index, exp in enumerate(((review.get('proposal') or {}).get('experiments') or [])):
            if exp.get('lane') != lane: continue
            hid = _hid('frontier', review['review_id'], index); stored = coll.find_one({'hypothesis_id': hid}, {'_id': 0}) or {}
            verdict = (review.get('review') or {}).get('verdict'); delta = stored.get('recipe_delta') or exp.get('recipe_delta') or {}
            conditions = []
            if verdict == 'reject': conditions.append('independent reviewer rejected the proposal; a revised proposal is required')
            elif verdict == 'revise': conditions.append('reviewer required_changes addressed in a re-run: ' + '; '.join((review.get('review') or {}).get('required_changes') or [])[:400])
            if not delta: conditions.append(f"engineering binding: a bounded recipe_delta over the {lane} tunables ({', '.join(sorted(TUNABLES[lane]))}); the idea is not executable as written")
            if review.get('naivety_pass'): conditions.append('owner call on the struck constraint (naivety-pass survivors never ship without a human call)')
            if stored.get('owner_verdict') == 'adopt': conditions = [c for c in conditions if c.startswith('engineering binding')]  # the coach ratifies; execution still needs a bound change
            out.append({'hypothesis_id': hid, 'lane': lane, 'origin': 'frontier_cif', 'correction_class': f"frontier:{hashlib.sha256(exp['change'].encode()).hexdigest()[:8]}", 'statement': exp['hypothesis'], 'change': exp['change'], 'measurement': exp.get('measurement'),
                        'manifest': [{'assumption': exp['hypothesis'], 'class': 'inferred', 'flips_if': exp.get('failure_condition') or 'the stated measurement does not move'}], 'prediction': _prediction(lane, g), 'recipe_delta': delta,
                        'evidence_refs': exp.get('evidence_refs') or [], 'citations': list(exp.get('evidence_refs') or []) + [f"malpha://learning/{review['review_id']}#proposal.experiments[{index}]"], 'review_verdict': verdict,
                        'review_id': review['review_id'], 'conditions': conditions, 'missing_condition': '; '.join(conditions) or None, 'naivety_pass': bool(review.get('naivety_pass'))})
    return out


def _remaining(hyp, *, bound=False, owner_adopted=False):
    """Conditions that survive a binding (engineering) or an owner adoption (coach): neither clears the other's condition."""
    conditions = list(hyp.get('conditions') or ([hyp['missing_condition']] if hyp.get('missing_condition') else []))
    if bound or hyp.get('recipe_delta'): conditions = [c for c in conditions if not c.startswith('engineering binding')]
    if owner_adopted or hyp.get('owner_verdict') == 'adopt': conditions = [c for c in conditions if c.startswith('engineering binding')]
    return conditions


def _in_bounds(spec, value):
    if spec is bool: return isinstance(value, bool)
    if isinstance(spec, dict): return value in spec['enum']
    lo, hi = spec
    return type(value) in (int, float) and math.isfinite(value) and lo <= value <= hi


def refuted_streak(lane, klass):
    tested = list(db().malpha_hypotheses.find({'lane': lane, 'test.verdict': {'$in': ['supported', 'refuted']}}, {'_id': 0, 'correction_class': 1, 'test.verdict': 1}).sort('test.at', -1).limit(ABSORPTION_REFUTATIONS))
    return len(tested) == ABSORPTION_REFUTATIONS and all(t['correction_class'] == klass and t['test']['verdict'] == 'refuted' for t in tested)


def accept(hyp, route=True):
    """Deterministic acceptance: the sealed CIF point (≥1 citation), the read-only floor/tunable check, the absorption rule. Owner origin never bypasses the floors."""
    proposal = author_proposal(proposal_id='cif_' + hyp['hypothesis_id'].replace('-', '_'), proposed_at=hyp.get('created_at') or now(), kind='research_loop_item',
                               payload=json.dumps({'lane': hyp['lane'], 'statement': hyp['statement'], 'recipe_delta': hyp.get('recipe_delta') or {}, 'prediction': hyp.get('prediction')}, sort_keys=True, default=str),
                               citations=tuple(hyp.get('citations') or ()))
    reasons = []
    if not is_accepted(proposal): reasons.append('CIF acceptance point refused: no citation backs the idea (BR-9.2 / AC-18)')
    for key, value in (hyp.get('recipe_delta') or {}).items():
        if key in PROTECTED: reasons.append(f'{key} is a protected parameter: floors, seals and measurement contracts are read-only (Canon 4 §27)')
        elif key not in TUNABLES[hyp['lane']]: reasons.append(f"{key} is not a parameter the {hyp['lane']} worker reads; the change would be untested")
        elif not _in_bounds(TUNABLES[hyp['lane']][key], value): reasons.append(f'{key}={value!r} is outside the registered bounds')
    if hyp.get('missing_condition'): reasons.append('not yet conditioned: ' + hyp['missing_condition'])
    if hyp['origin'] != 'owner' and refuted_streak(hyp['lane'], hyp['correction_class']):
        reasons.append(f"absorption signature: correction class {hyp['correction_class']} was refuted {ABSORPTION_REFUTATIONS} times in a row under unchanged conditions; not re-adopted autonomously (Canon 2 §7, §11)")
    routed = None
    if not reasons and route:
        try: routed = route_accepted_proposal(proposal, True)
        except RoutingRefused as exc: reasons.append(f'routing refused: {exc}')
    return {'accepted': not reasons, 'reasons': reasons, 'proposal_id': proposal.proposal_id, 'routed': routed, 'at': now()}


# ----------------------------------------------------------------------------- selection cycle (paper before compute)
def _rank(c):
    return (2 if c.get('owner_verdict') == 'adopt' else 0, {'owner': 3, 'frontier_cif': 2, 'measurement_rule': 1, 'planned_ladder': 1}.get(c['origin'], 0), c['hypothesis_id'])


def candidates(lane, iteration, ladder_recipe, history, g):
    coll = db().malpha_hypotheses
    fresh = [ladder_hypothesis(lane, iteration, ladder_recipe, history, g)] + frontier_hypotheses(lane, g)
    seen = {c['hypothesis_id'] for c in fresh}
    fresh += [r for r in coll.find({'lane': lane, 'origin': 'owner', 'archive_state': {'$in': ['not_yet_conditioned', 'unverified_provisional']}}, {'_id': 0}) if r['hypothesis_id'] not in seen]
    out = []
    for c in fresh:
        stored = coll.find_one({'hypothesis_id': c['hypothesis_id']}, {'_id': 0}) or {}
        if stored.get('job_id') or stored.get('archive_state') == 'superseded' or stored.get('owner_verdict') == 'reject': continue  # ran, withdrawn or rejected: never silently resurfaced
        c = {**c, **{k: stored[k] for k in ('owner_verdict', 'owner_reason', 'created_at') if stored.get(k)}}
        if not (c.get('prediction') or {}).get('field'): c['prediction'] = _prediction(lane, g)  # an owner idea is bound to the load-bearing gap at adoption
        c.setdefault('created_at', now())
        c['acceptance'] = accept(c, route=not (stored.get('acceptance') or {}).get('routed'))
        if not c['acceptance']['routed'] and (stored.get('acceptance') or {}).get('routed'): c['acceptance']['routed'] = stored['acceptance']['routed']
        out.append(c)
    return out


def _persist(c, archive_state, verdict, **extra):
    row = {k: v for k, v in c.items() if k not in ('load_bearing_set', 'first_seen_at', '_id')}
    row.update(archive_state=archive_state, verdict=verdict, updated_at=now(), **extra)
    if archive_state == 'not_yet_conditioned':
        row['review_by'] = row.get('review_by') or (datetime.now(timezone.utc) + timedelta(days=RENT_DAYS)).isoformat()
        bindable = (row.get('missing_condition') or '') == FREE_DEVICE
        row['watch'] = {'bindable': True, 'field': f"malpha_commissions.lane_state.{c['lane']}.status", 'fires_when': 'not in (running, submitting)'} if bindable else \
            {'bindable': False, 'review_by': row['review_by'], 'note': 'the condition does not resolve to a live telemetry field; rent-date human review instead (Canon 2 §14)'}
    db().malpha_hypotheses.update_one({'hypothesis_id': c['hypothesis_id']}, {'$set': row, '$setOnInsert': {'first_seen_at': now()}}, upsert=True)
    return row


def _trace(lane, iteration, path, g):
    return record_trace(session_id=f'malpha-supervisor:{lane}:{iteration}', reasoning_path=path, load_bearing_units=g['load_bearing_set'].units, computed_class=compute_class(g['load_bearing_set']), conclusion=g['conclusion']).model_dump(mode='json')


def select(cid, lane, iteration, history, ladder_recipe):
    """One supervised pick for the next dispatch. Returns {'hypothesis', 'recipe', ...} or None (refusal envelope recorded; lane held for the owner)."""
    g = gap(lane, history)
    path = ['evidence_projection', 'load_bearing_units(reasoning_faculty)', 'assertion_class(assertion_boundary)', 'candidate_generation', 'tension_detection', REFLECTION_NOTE, 'cif_acceptance_point', 'deterministic_rank']
    cands = candidates(lane, iteration, ladder_recipe, history, g)
    if is_halted(): cands = [c for c in cands if c['origin'] != 'frontier_cif']; path.append('cif_halted:frontier_candidates_excluded')
    admissible = [c for c in cands if c['acceptance']['accepted']]
    cycle = {'lane': lane, 'iteration': iteration, 'at': now(), 'gap': {k: v for k, v in g.items() if k not in ('load_bearing_set', 'units')}, 'cif_halted': is_halted(), 'cif_halt_journal': list(get_halt_journal()),
             'candidates': [{k: c.get(k) for k in ('hypothesis_id', 'origin', 'correction_class', 'statement', 'recipe_delta', 'acceptance', 'missing_condition', 'review_verdict', 'owner_verdict')} for c in cands]}
    if not admissible:
        actions = [RefusalAction.NARROW_OBJECTIVE] + ([RefusalAction.ACCEPT_AS_STATED] if any(c['origin'] == 'frontier_cif' for c in cands) else [])
        envelope = RefusalEnvelope(reason_class=compute_class(g['load_bearing_set']), actions_offered=actions)
        for c in cands:
            absorbed = any(r.startswith('absorption signature') for r in c['acceptance']['reasons'])
            _persist(c, 'superseded' if absorbed else 'not_yet_conditioned', 'reject' if absorbed else 'defer', missing_condition=c.get('missing_condition') or '; '.join(c['acceptance']['reasons']))
        cycle.update(outcome='refused', refusal_envelope={**envelope.model_dump(mode='json'), 'lower_standard_not_offered': LOWER_STANDARD_NOTE}, trace=_trace(lane, iteration, path + ['refusal_envelope'], g),
                     intent_audit=_observe(lane, f'iteration {iteration}: no admissible hypothesis; refusal envelope offered to the owner'))
        db().malpha_supervisor_cycles.insert_one(dict(cycle))
        wpw.record_event(cid, 'anomaly', 'observed', f'malpha://supervisor/cycle/{lane}/{iteration}', {'lane': lane, 'iteration': iteration, 'what': 'training supervisor found no admissible hypothesis; lane held with a refusal envelope', 'actions_offered': [a.value for a in actions]})
        return None
    pick = max(admissible, key=_rank)
    streak = _same_class_streak(lane, pick['correction_class'])
    observation = f"iteration {iteration}: adopted {pick['correction_class']} ({pick['origin']}); consecutive same-class adoptions {streak + 1}" + ('; DIVERGENCE: repetition without a supported test demonstrates confirmation, not inquiry' if streak >= 2 and not _recent_support(lane) else '')
    adopted = _persist(pick, 'adopted', 'adopt', adopted_at=now(), iteration=iteration, commission_id=cid,
                       baseline={'field': pick['prediction'].get('field'), 'language': pick['prediction'].get('language'), 'value': _value(g['units'], pick['prediction'].get('field'), pick['prediction'].get('language')) if pick['prediction'].get('field') else None, 'iteration_before': g['iteration']},
                       pick_manifest=[{'assumption': 'the deterministic rank (owner adoption > frontier-reviewed > measurement rule) orders admissible ideas', 'class': 'fact', 'flips_if': 'the owner records a different verdict on this cycle'},
                                      {'assumption': 'the highest-ranked admissible idea targets the load-bearing gap', 'class': 'inferred', 'flips_if': 'its prediction field differs from the gap field'}])
    for c in cands:
        if c['hypothesis_id'] == pick['hypothesis_id']: continue
        if c['acceptance']['accepted']: _persist(c, 'not_yet_conditioned', 'rank', missing_condition=FREE_DEVICE)
        else: _persist(c, 'not_yet_conditioned', 'defer', missing_condition=c.get('missing_condition') or '; '.join(c['acceptance']['reasons']))
    recipe = {**ladder_recipe, **(pick.get('recipe_delta') or {})}
    if pick.get('recipe_delta'): recipe['rationale'] = f"{ladder_recipe.get('rationale', '')} | supervisor adopted {pick['hypothesis_id']} ({pick['origin']}): {pick['statement'][:300]} → {json.dumps(pick['recipe_delta'], default=str)}"
    cycle.update(outcome='adopted', pick=pick['hypothesis_id'], trace=_trace(lane, iteration, path, g), intent_audit=_observe(lane, observation))
    db().malpha_supervisor_cycles.insert_one(dict(cycle))
    return {'hypothesis': adopted, 'recipe': recipe, 'gap': cycle['gap'], 'trace': cycle['trace'], 'proposal_id': pick['acceptance']['proposal_id']}


def _same_class_streak(lane, klass):
    n = 0
    for row in db().malpha_hypotheses.find({'lane': lane, 'archive_state': 'adopted', 'job_id': {'$exists': True}}, {'_id': 0, 'correction_class': 1}).sort('adopted_at', -1):
        if row['correction_class'] != klass: break
        n += 1
    return n


def _recent_support(lane):
    return db().malpha_hypotheses.count_documents({'lane': lane, 'test.verdict': 'supported'}) > 0


def _observe(lane, observation):
    row = db().malpha_supervisor_intent.find_one({'lane': lane}, {'_id': 0}) or {}
    audit = open_intent_audit(session_id=f'malpha-supervisor:{lane}', declared_situation_class=DECLARED_SITUATION)
    for obs in (row.get('demonstrated_observations') or [])[-39:]: audit = update_intent_audit_demonstrated(audit, obs)
    audit = update_intent_audit_demonstrated(audit, observation)
    doc = {**audit.model_dump(mode='json'), 'lane': lane, 'divergence': any('DIVERGENCE' in o for o in audit.demonstrated_observations[-3:]), 'updated_at': now()}
    db().malpha_supervisor_intent.update_one({'lane': lane}, {'$set': doc}, upsert=True)
    return doc


def bind_job(hypothesis_id, job_id):
    db().malpha_hypotheses.update_one({'hypothesis_id': hypothesis_id}, {'$set': {'job_id': job_id, 'test': {'verdict': 'pending'}}})


def release(hypothesis_id, reason):
    db().malpha_hypotheses.update_one({'hypothesis_id': hypothesis_id}, {'$set': {'archive_state': 'not_yet_conditioned', 'verdict': 'defer', 'missing_condition': f'dispatch refused: {reason}'[:300]}, '$unset': {'job_id': ''}})


# ----------------------------------------------------------------------------- hypothesis test at settlement
def on_settled(rec):
    hyp = db().malpha_hypotheses.find_one({'job_id': rec['job_id']}, {'_id': 0})
    if not hyp: return None
    lane, cid = rec['lane'], rec['commission_id']; pred, base = hyp.get('prediction') or {}, hyp.get('baseline') or {}
    if rec.get('status') != 'completed': test = {'verdict': 'inconclusive', 'reason': f"job ended {rec.get('status')}: {str(rec.get('reason'))[:160]}", 'at': now()}
    else:
        after = _value(evidence_units(lane, rec), pred.get('field'), pred.get('language')) if pred.get('field') else None
        if after is None: test = {'verdict': 'inconclusive', 'reason': 'the predicted field was not measured in this result', 'at': now()}
        elif base.get('value') is None: test = {'verdict': 'inconclusive', 'reason': 'no measured baseline before this iteration; this reading is the baseline', 'after': after, 'at': now()}
        else:
            moved = (after - base['value']) * (1 if pred.get('direction') == 'up' else -1)
            test = {'verdict': 'supported' if moved >= pred['min_delta'] else 'refuted', 'before': base['value'], 'after': after, 'movement': round(after - base['value'], 4), 'required': f"{pred['direction']} ≥ {pred['min_delta']}", 'at': now()}
    db().malpha_hypotheses.update_one({'hypothesis_id': hyp['hypothesis_id']}, {'$set': {'test': test}})
    ref = f"malpha://supervisor/hypothesis/{hyp['hypothesis_id']}"
    wpw.record_event(cid, 'cif_ideation', 'measured' if test['verdict'] in ('supported', 'refuted') else 'observed', f"m9_training://run_log/{rec['job_id']}",
                     {'cif_event_ref': ref, 'idea_ref': ref + '#statement', 'conditions_ref': ref + '#prediction', 'adoption_status': f"adopted; tested: {test['verdict']}", 'test': {k: v for k, v in test.items() if k != 'at'}})
    finding = None
    if test['verdict'] == 'refuted' and refuted_streak(lane, hyp['correction_class']):
        finding = {'finding_id': _hid('finding', lane, hyp['correction_class'], rec['job_id']), 'lane': lane, 'signature': 'absorption', 'correction_class': hyp['correction_class'], 'at': now(), 'owner_call': 'pending',
                   'hypotheses': [h['hypothesis_id'] for h in db().malpha_hypotheses.find({'lane': lane, 'correction_class': hyp['correction_class'], 'test.verdict': 'refuted'}, {'_id': 0, 'hypothesis_id': 1})],
                   'what': f"the same correction class ({hyp['correction_class']}) was patched {ABSORPTION_REFUTATIONS} times while the {pred.get('field')} gap for {pred.get('language')} persisted — a frame candidate, not another iteration",
                   'struck_constraint': STRUCK[lane], 'naivety_pass': 'scheduled' if not is_halted() else 'skipped: CIF halted'}
        db().malpha_supervisor_findings.update_one({'finding_id': finding['finding_id']}, {'$setOnInsert': finding}, upsert=True)
        wpw.record_event(cid, 'anomaly', 'observed', f"malpha://supervisor/finding/{finding['finding_id']}", {k: v for k, v in finding.items() if k != 'at'})
        if not is_halted(): _schedule_naivety_pass(lane, hyp, finding)
    return {'test': test, 'finding': finding}


def _schedule_naivety_pass(lane, hyp, finding):
    """Canon 2 §10.1: re-qualify with the inherited constraint struck; survivors wait for a human call. Own thread so settlement never blocks."""
    def run():
        import asyncio
        from services.training_lab import malpha_learning
        try:
            asyncio.run(malpha_learning.reconstruct('training-supervisor', retry_failed=True, naivety={'lane': lane, 'struck_constraint': STRUCK[lane], 'refuted_class': hyp['correction_class'], 'finding_id': finding['finding_id']}))
            db().malpha_supervisor_findings.update_one({'finding_id': finding['finding_id']}, {'$set': {'naivety_pass': 'reviewed'}})
        except Exception as exc:
            db().malpha_supervisor_findings.update_one({'finding_id': finding['finding_id']}, {'$set': {'naivety_pass': f'failed: {type(exc).__name__}'}})
            failures = db().malpha_supervisor_findings.count_documents({'naivety_pass': {'$regex': '^failed'}})
            if failures >= 3 and not is_halted(): halt(f'CIF own-halt (DET-1): frontier ideation failed {failures} times; the supervisor continues on measurement rules only until the owner clears it')
    threading.Thread(target=run, name=f'malpha-naivety-{lane}', daemon=True).start()


# ----------------------------------------------------------------------------- coach seat (owner)
def _human(cid, actor, before, change, after):
    wpw.record_event(cid, 'human_contribution', 'observed', 'malpha://supervisor/coach-seat', {'actor': {'role': 'owner/operator', 'identity': actor}, 'state_before': before, 'change': change, 'movement_after': after})


def originate(actor, lane, statement, recipe_delta, prediction=None, manifest=None):
    if lane not in LANES: raise ValueError('Unknown lane')
    if not statement or len(statement) > 1600: raise ValueError('A hypothesis statement of up to 1600 characters is required')
    if not isinstance(recipe_delta, dict) or not recipe_delta: raise ValueError('An owner hypothesis needs a recipe_delta over the lane tunables')
    hid = _hid('owner', lane, statement, json.dumps(recipe_delta, sort_keys=True, default=str))
    if db().malpha_hypotheses.find_one({'hypothesis_id': hid, 'job_id': {'$exists': True}}): raise ValueError('This exact hypothesis already ran; state a new idea')
    row = {'hypothesis_id': hid, 'lane': lane, 'origin': 'owner', 'correction_class': f'owner:{hid[-6:]}', 'statement': statement, 'recipe_delta': recipe_delta,
           'prediction': prediction or {'field': None, 'language': None, 'direction': None, 'min_delta': MIN_DELTA[lane], 'note': 'bound to the load-bearing gap at adoption'},
           'manifest': manifest or [{'assumption': statement, 'class': 'recalled', 'flips_if': 'the predicted field does not move'}], 'evidence_refs': [], 'citations': [f'owner://coach-seat/{actor}', *CANON_REFS],
           'created_at': now(), 'owner_verdict': 'adopt', 'owner_reason': 'originated at the coach seat', 'owner_identity': actor}
    row['acceptance'] = accept(row)
    ok = row['acceptance']['accepted']
    _persist(row, 'unverified_provisional' if ok else 'not_yet_conditioned', 'adopt' if ok else 'defer', missing_condition=None if ok else '; '.join(row['acceptance']['reasons']))
    if ok: _release_hold(lane)
    _human(COMMISSION_OF[lane], actor, f'{lane}: no owner hypothesis on record', f'owner originated {hid}: {statement[:200]}', 'adoption at the next free device; movement measured at settlement' if ok else 'refused at the acceptance point: ' + '; '.join(row['acceptance']['reasons']))
    return db().malpha_hypotheses.find_one({'hypothesis_id': hid}, {'_id': 0})


def verdict(actor, hypothesis_id, decision, reason, missing_condition=None):
    if decision not in ('adopt', 'reject', 'defer'): raise ValueError('verdict must be adopt, reject or defer')
    if not reason: raise ValueError('A reason is required; silence is a data state, never a verdict')
    hyp = db().malpha_hypotheses.find_one({'hypothesis_id': hypothesis_id}, {'_id': 0})
    if not hyp: raise LookupError('No hypothesis with that reference')
    if hyp.get('job_id'): raise ValueError('This hypothesis already ran; record a verdict on a new idea instead')
    patch = {'owner_verdict': decision, 'owner_reason': reason, 'owner_at': now(), 'owner_identity': actor}
    if decision == 'reject': patch.update(archive_state='superseded', verdict='reject', superseded_reason=reason)
    elif decision == 'defer':
        if not missing_condition: raise ValueError('A deferral names the missing condition specifically enough that its arrival is recognisable')
        patch.update(archive_state='not_yet_conditioned', verdict='defer', missing_condition=missing_condition, review_by=(datetime.now(timezone.utc) + timedelta(days=RENT_DAYS)).isoformat())
    else:
        remaining = _remaining(hyp, owner_adopted=True)
        acceptance = accept({**hyp, 'missing_condition': '; '.join(remaining) or None}, route=False)
        if not acceptance['accepted'] and not remaining: raise ValueError('Adoption refused at the acceptance point: ' + '; '.join(acceptance['reasons']))
        patch.update(archive_state='unverified_provisional' if acceptance['accepted'] else 'not_yet_conditioned', verdict='adopt', missing_condition='; '.join(remaining) or None, conditions=remaining)
        if acceptance['accepted']: _release_hold(hyp['lane'])
    db().malpha_hypotheses.update_one({'hypothesis_id': hypothesis_id}, {'$set': patch})
    _human(COMMISSION_OF[hyp['lane']], actor, f"{hypothesis_id} was {hyp.get('archive_state')}", f'owner verdict {decision}: {reason[:200]}', 'selection order changes at the next free device; no model or floor changed')
    return db().malpha_hypotheses.find_one({'hypothesis_id': hypothesis_id}, {'_id': 0})


def bind(actor, hypothesis_id, recipe_delta):
    hyp = db().malpha_hypotheses.find_one({'hypothesis_id': hypothesis_id}, {'_id': 0})
    if not hyp: raise LookupError('No hypothesis with that reference')
    if hyp.get('job_id'): raise ValueError('This hypothesis already ran')
    if not isinstance(recipe_delta, dict) or not recipe_delta: raise ValueError('recipe_delta must be a non-empty object over the lane tunables')
    remaining = _remaining(hyp, bound=True)
    acceptance = accept({**hyp, 'recipe_delta': recipe_delta, 'missing_condition': '; '.join(remaining) or None}, route=False)
    db().malpha_hypotheses.update_one({'hypothesis_id': hypothesis_id}, {'$set': {'recipe_delta': recipe_delta, 'bound_by': actor, 'bound_at': now(), 'binding_check': acceptance, 'conditions': remaining,
                                                                                   'missing_condition': None if acceptance['accepted'] else '; '.join(remaining or acceptance['reasons']), 'archive_state': 'unverified_provisional' if acceptance['accepted'] else 'not_yet_conditioned'}})
    _human(COMMISSION_OF[hyp['lane']], actor, f'{hypothesis_id} awaited an engineering binding', f'bound recipe_delta {json.dumps(recipe_delta, default=str)[:200]}', 'candidate at the next free device' if acceptance['accepted'] else 'refused: ' + '; '.join(acceptance['reasons']))
    return db().malpha_hypotheses.find_one({'hypothesis_id': hypothesis_id}, {'_id': 0})


def _release_hold(lane):
    cid = COMMISSION_OF[lane]
    state = ((db().malpha_commissions.find_one({'commission_id': cid}, {'_id': 0, 'lane_state': 1}) or {}).get('lane_state') or {}).get(lane) or {}
    if state.get('status') == 'held' and state.get('held_by') == 'training_supervisor':
        db().malpha_commissions.update_one({'commission_id': cid}, {'$set': {f'lane_state.{lane}.status': 'iterating', f'lane_state.{lane}.released_at': now()}})


def clear_cif_halt(actor, reason):
    """The sealed halt journal has no overwrite path by design; its reset is the only release and is recorded here as a human contribution."""
    from services.cif import halt as cif_halt
    if not reason: raise ValueError('A reason is required')
    journal = list(get_halt_journal()); cif_halt._reset_halt_for_tests()
    db().malpha_supervisor_findings.update_many({'naivety_pass': {'$regex': '^failed'}}, {'$set': {'naivety_pass': 'cleared by owner'}})
    _human('LISTEN-KIK-KAM-SWA', actor, f'CIF halted: {journal}', f'owner cleared the CIF halt: {reason[:200]}', 'frontier candidates re-enter selection at the next cycle')
    return {'cleared': journal}


# ----------------------------------------------------------------------------- views
def ledger(lane=None):
    rows = list(db().malpha_hypotheses.find({'lane': lane} if lane else {}, {'_id': 0}).sort([('updated_at', -1)]).limit(120))
    return {'hypotheses': rows, 'rent_expired': [r['hypothesis_id'] for r in rows if r.get('archive_state') == 'not_yet_conditioned' and r.get('review_by') and r['review_by'] < now()]}


def paper_cycle():
    """Paper before compute (Canon 2 §9): archive every frontier idea for every lane now — accepted ones wait for a free device, the rest carry their named condition. No dispatch, no model change."""
    from services.training_lab import malpha
    out = {}
    for lane in LANES:
        g = gap(lane, malpha.jobs(lane=lane, status='completed')); coll = db().malpha_hypotheses; n = 0
        for c in frontier_hypotheses(lane, g):
            stored = coll.find_one({'hypothesis_id': c['hypothesis_id']}, {'_id': 0}) or {}
            if stored.get('job_id') or stored.get('archive_state') in ('adopted', 'superseded') or stored.get('owner_verdict') == 'reject': continue
            c = {**c, **{k: stored[k] for k in ('owner_verdict', 'owner_reason', 'created_at') if stored.get(k)}}; c.setdefault('created_at', now())
            c['acceptance'] = accept(c, route=not (stored.get('acceptance') or {}).get('routed'))
            if not c['acceptance']['routed'] and (stored.get('acceptance') or {}).get('routed'): c['acceptance']['routed'] = stored['acceptance']['routed']
            _persist(c, 'not_yet_conditioned', 'rank' if c['acceptance']['accepted'] else 'defer', missing_condition=FREE_DEVICE if c['acceptance']['accepted'] else (c.get('missing_condition') or '; '.join(c['acceptance']['reasons'])))
            n += 1
        out[lane] = {'archived': n, 'gap': g['conclusion']}
    return out


def summary():
    from services.training_lab import malpha
    out = {'design': 'Solva v2 (load-bearing units → assertion class → trace; intent audit; refusal envelope) over CIF (manifested ideas → deterministic acceptance point → archive with rent and watchers; absorption → naivety pass → owner call)',
           'reflection': REFLECTION_NOTE, 'cif_halted': is_halted(), 'cif_halt_journal': list(get_halt_journal()), 'floors': FLOORS, 'lower_standard': LOWER_STANDARD_NOTE, 'protected_parameters': list(PROTECTED),
           'tunables': {l: {k: (list(v['enum']) if isinstance(v, dict) else 'bool' if v is bool else list(v)) for k, v in t.items()} for l, t in TUNABLES.items()}, 'lanes': {},
           'findings': list(db().malpha_supervisor_findings.find({}, {'_id': 0}).sort('at', -1).limit(20))}
    for lane in LANES:
        g = gap(lane, malpha.jobs(lane=lane, status='completed')); led = ledger(lane)
        out['lanes'][lane] = {'gap': {k: v for k, v in g.items() if k not in ('load_bearing_set', 'units')}, 'readings': g['units'], 'last_cycle': db().malpha_supervisor_cycles.find_one({'lane': lane}, {'_id': 0}, sort=[('at', -1)]),
                              'intent_audit': db().malpha_supervisor_intent.find_one({'lane': lane}, {'_id': 0}), 'adopted': next((h for h in led['hypotheses'] if h.get('archive_state') == 'adopted' and (h.get('test') or {}).get('verdict') == 'pending'), None),
                              'hypotheses': led['hypotheses'], 'rent_expired': led['rent_expired'], 'tests': {v: sum(1 for h in led['hypotheses'] if (h.get('test') or {}).get('verdict') == v) for v in ('supported', 'refuted', 'inconclusive', 'pending')},
                              'archive': {s: sum(1 for h in led['hypotheses'] if h.get('archive_state') == s) for s in ('adopted', 'not_yet_conditioned', 'unverified_provisional', 'superseded')}}
    return out
