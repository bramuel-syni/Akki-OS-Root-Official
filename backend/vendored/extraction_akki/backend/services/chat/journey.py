"""The governed answer journey: one question → one decision → warm window answer | fresh acknowledgement | refusal.

Every turn banks: the decision and its Ledger row, the exact window (selected/excluded, tokenizer, rule), the
memory hits/misses, what was read (qualified store only; source reads are always zero here), the model receipt
and the loss statement that also closes the answer text.

WP-A3 (Doc 1 B5): a question-bearing request first captures its objective with the contained reader — the whole
un-redacted question, inside the perimeter — into ONE frozen artefact, before any read, de-identification or
model call. The artefact is consumed by reference by the scope check, the prompt and the grounding record;
demonstrated-intent observations are appended per turn. No objective → `ask` (human in the loop), never a guess.
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone
from time import perf_counter

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.chat import answer as answering, decision as deciding, sessions, spine, window as windowing
from services.critic_pass import producer_seam as critic_seam
from services.northena import ledger as northena_ledger
from services.synisense.shield import objective_capture

DEFAULT_MODEL = 'gpt-5-mini'
DEFAULT_PROVIDER = 'emergent'
# [SLOT] rule-set v1 trigger: compact the closed working context after this many un-compacted turns.
COMPACT_AFTER_TURNS = int(os.environ.get('AKKI_CHAT_COMPACT_AFTER_TURNS') or 12)
NO_READS = {'source_dispatches': 0, 'source_rows_read': 0, 'source_bytes_read': 0, 'qualified_store_calls': 0, 'qualified_bytes_read': 0, 'candidates_returned': 0, 'matched_total': 0, 'units_total': 0, 'failures': []}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _order(candidates):
    return sorted(candidates, key=lambda c: (c['kind'] != 'matched', -c['overlap'], c['position'], c['ref']))[:500]


async def _converge(session_id, turn_id, reason, objective_ref=None):
    await northena_ledger.record(LedgerRow(run_id=session_id, trace_id=turn_id, stage='converge', decision='terminate_success', reason=reason,
                                           artifact_ref=LedgerArtifactRef(artifact_type='objective_request', artifact_id=objective_ref or f'chat-{session_id}', version='v1'),
                                           lawful_basis_ref=os.environ.get('CENSUS_LAWFUL_BASIS_PATH', 'chat:governed_answer'), stamp_audit=None))


def _not_captured(question, exc, started):
    """B86/B87: a defined outcome in place of a guessed objective — no session, no read, no model call."""
    if exc.outcome == 'ask':
        reason = f'Please clarify what you are asking: {exc.reason}. Nothing was read and no model was called (Doc 1 B5.5: clarify, never guess).'
    else:
        reason = f'The question could not be bounded to an objective: {exc.reason}. Nothing proceeded on a guessed objective.'
    turn = {'turn_id': 'turn-' + uuid.uuid4().hex[:12], 'question': question, 'asked_at': _now(), 'decision': 'ask' if exc.outcome == 'ask' else 'refused', 'refused': True, 'refusal_reason': reason, 'answer': '',
            'objective_capture': {'outcome': exc.outcome, 'kind': exc.kind}, 'evidence': {'reads': dict(NO_READS), 'cited_refs': []}, 'latency_ms_total': int((perf_counter() - started) * 1000)}
    return {'session_id': None, 'title': None, 'objective': None, 'outcome': exc.outcome, 'turn': turn, 'turns': 0, 'compaction': None}


async def _frozen_objective(scope, session):
    """The session's artefact by reference (verified), or — for a session opened before WP-A3 — captured now from its frozen first question."""
    ref = session['objective'].get('artifact_id')
    if ref:
        return await asyncio.to_thread(objective_capture.verify, ref)
    artifact = await asyncio.to_thread(objective_capture.capture, session['objective']['text'], scope['tenant_id'], session['session_id'], 'human')
    record = sessions.objective_record(session['objective']['text'], artifact); record['frozen_at'] = session['objective']['frozen_at']
    await sessions.update(scope, session['session_id'], {'objective': record}); session['objective'] = record
    return artifact


async def ask(db, scope, *, question, session_id=None, model=DEFAULT_MODEL, provider=DEFAULT_PROVIDER):
    started = perf_counter()
    session = await sessions.get(scope, session_id) if session_id else None
    if session_id and session is None:
        return None
    try:
        if session is None:
            new_id = sessions.new_id()
            artifact = await asyncio.to_thread(objective_capture.capture, question, scope['tenant_id'], new_id, 'human')
            session = await sessions.create(scope, question, session_id=new_id, artifact=artifact)
        else:
            artifact = await _frozen_objective(scope, session)
    except objective_capture.ObjectiveNotCaptured as exc:
        return _not_captured(question, exc, started)
    except objective_capture.ObjectiveTampered as exc:
        turn = {'turn_id': 'turn-' + uuid.uuid4().hex[:12], 'question': question, 'asked_at': _now(), 'decision': 'refused', 'refused': True, 'refusal_reason': f'{exc} This conversation is closed to new questions; open a new one.', 'answer': '',
                'evidence': {'reads': dict(NO_READS), 'cited_refs': []}}
        return await _close(scope, session['session_id'], turn, started)
    objective_ref = artifact['artifact_id']
    turn_id = 'turn-' + uuid.uuid4().hex[:12]
    terms = spine.question_terms(question)
    artefacts = await spine.verified_artefacts(db, scope)
    read = await spine.read_candidates(db, scope, artefacts, terms) if terms else {'candidates': [], 'calls': 0, 'qualified_bytes_read': 0, 'matched_total': 0, 'units_total': 0, 'failures': []}
    candidates = _order(read['candidates'])
    decision = await deciding.decide(db, scope, session_id=session['session_id'], turn_id=turn_id, question=question, terms=terms,
                                     artefacts=artefacts, candidates=candidates, objective_ref=objective_ref)
    evidence = {'qualified_set_ref': spine.qualified_set_ref(artefacts), 'objective_ref': objective_ref,
                'artefacts': [{k: a[k] for k in ('artifact_ref', 'sha256', 'region', 'units', 'rights_receipt_ref', 'inspection_ref', 'request_id')} for a in artefacts],
                'reads': {'source_dispatches': 0, 'source_rows_read': 0, 'source_bytes_read': 0, 'qualified_store_calls': read['calls'],
                          'qualified_bytes_read': read['qualified_bytes_read'], 'candidates_returned': len(candidates),
                          'matched_total': read['matched_total'], 'units_total': read['units_total'], 'failures': read['failures']},
                'terms': terms, 'cited_refs': []}
    turn = {'turn_id': turn_id, 'question': question, 'asked_at': _now(), 'decision': decision['decision'], 'decision_detail': decision,
            'evidence': evidence, 'refused': False, 'refusal_reason': '', 'answer': '', 'model_id': model, 'provider': provider}
    if decision['decision'] == 'warm' and candidates:
        accessor = await spine.chat_plane(scope)
        context_lines = sessions.recent_context(session)
        reserved = windowing.count_tokens(question) + windowing.count_tokens(answering.SYSTEM) + windowing.count_tokens('\n'.join(context_lines)) + windowing.ANSWER_RESERVE_TOKENS
        try:
            window, selected, excluded = windowing.build(objective_text=session['objective']['text'], frame_ref=f"akki://chat/session/{session['session_id']}",
                                                         model=model, qualified_set_receipt_ref=evidence['qualified_set_ref'], candidates=candidates,
                                                         reserved_tokens=reserved)
        except ValueError:
            window = None
        if window is None:
            turn.update({'refused': True, 'refusal_reason': f"No whole qualified unit fits the window budget ({windowing.WINDOW_TOKENS - reserved} tokens free of "
                                                            f"{windowing.WINDOW_TOKENS}); {len(candidates)} candidates were read and none was split. Nothing was answered."})
            return await _close(scope, session['session_id'], turn, started)
        loss = windowing.loss_statement(window, read)
        evidence['memory'] = await spine.touch_working_set(accessor, list(window.selected_refs))
        evidence['window'] = {'selected_refs': list(window.selected_refs), 'load_bearing_refs': list(window.load_bearing_refs),
                              'excluded_counts': window.excluded_counts, 'top_excluded_handles': list(window.top_excluded_handles),
                              'window_tokens': window.window_tokens, 'reserved_tokens': window.reserved_tokens,
                              'tokens_in_window': sum(c['tokens'] for c in selected), 'candidates': len(candidates),
                              'tokenizer': windowing.TOKENIZER, 'tokenizer_sha256': window.tokenizer_sha256,
                              'ranking_rule_ref': window.ranking_rule_ref, 'objective_sha256': window.objective_sha256,
                              'loss_disclosed': window.loss_disclosed, 'loss_statement': loss,
                              'selected': [{'ref': c['ref'], 'region': c['region'], 'class': c['class_label'], 'tokens': c['tokens'],
                                            'proximity': c['proximity'], 'position': c['position'], 'content_sha256': c['content_sha256'],
                                            'source': c['unit']['provenance']['locator']} for c in selected]}
        result = await answering.answer(scope=scope, session=session, question=question, context_lines=context_lines, selected=selected,
                                        model=model, provider=provider, actor=scope['principal_id'])
        if result['refused']:
            turn.update({'refused': True, 'refusal_reason': result['refusal_reason']})
        else:
            evidence['cited_refs'] = result['cited_refs']
            evidence['grounding'] = {k: result[k] for k in ('grounding', 'sufficient', 'unsupported', 'citations_dropped')}
            evidence['shield'] = result.get('shield')
            turn.update({'answer': result['answer'] + '\n\nContext: ' + loss, 'receipt_id': result['receipt_id'], 'model_id': result['model_id'],
                         'provider': result['provider'], 'tokens_in': result['tokens_in'], 'tokens_out': result['tokens_out'],
                         'latency_ms': result['latency_ms'], 'sufficient': result['sufficient'], 'grounding': result['grounding'],
                         'critic_verdict': critic_seam.verdict_summary(critic_seam.route_through_seam(
                             artifact_ref=f"chat:{result['receipt_id']}", artifact_content=result['answer'],
                             producing_instance_id=f'chat.{provider}.{model}'))})
            await _converge(session['session_id'], turn_id, f"chat.warm_answer:units={len(selected)}:grounding={result['grounding']}:receipt={result['receipt_id']}", objective_ref)
    elif decision['decision'] == 'fresh':
        turn.update({'answer': decision['acknowledgement'], 'kind': 'fresh_acknowledgement'})
    else:
        subject = decision['sub_objective']
        weak = (decision.get('subject_match') or {}).get('weak_regions') or []
        aside = f" {len(weak)} loosely matching unit set(s) in {', '.join(weak)} were set aside under rule {deciding.SUBJECT_RULE}: the question does not name that subject." if weak else ''
        turn.update({'refused': True, 'refusal_reason': (f"Out of scope ({subject}): no qualified unit and no censused table of the {scope['tenant_id']} estate names this subject.{aside} Nothing was read or dispatched."
                     if subject == 'unresolved' else f"Refused by the gate: {decision['reason']}.")})
    # WP-A3 (Doc 1 B85): demonstrated intent is observed per turn against the declared objective; divergence is reported on the record
    observed = await asyncio.to_thread(objective_capture.observe, objective_ref, 'turn', {'turn_id': turn_id, 'decision': decision['decision'], 'reason': decision.get('reason'), 'refused': turn['refused'],
                                                                                           'grounding': turn.get('grounding'), 'citations_dropped': (evidence.get('grounding') or {}).get('citations_dropped'), 'sufficient': turn.get('sufficient'),
                                                                                           'follow_up': bool(session['turns'])})
    evidence['intent'] = await asyncio.to_thread(objective_capture.divergence, objective_ref)
    evidence['intent']['this_turn_flags'] = observed['observation']['divergence']
    return await _close(scope, session['session_id'], turn, started)


async def _close(scope, session_id, turn, started):
    """Bank the turn durably, compact when the rule-set trigger is met, and return the session view."""
    turn['latency_ms_total'] = int((perf_counter() - started) * 1000)
    await sessions.append_turn(scope, session_id, turn)
    session = await sessions.get(scope, session_id)
    compaction = None
    if sum(1 for t in session['turns'] if not t.get('compacted')) >= COMPACT_AFTER_TURNS:
        compaction = await sessions.compact(scope, session, actor=scope['principal_id'])
    return {'session_id': session['session_id'], 'title': session['title'], 'objective': session['objective'], 'turn': turn,
            'turns': len(session['turns']), 'compaction': compaction or session.get('compaction')}
