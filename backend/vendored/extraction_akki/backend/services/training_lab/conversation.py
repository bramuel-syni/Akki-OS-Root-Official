"""Per-run conversation with Akki in the owner's Train Models studio. Every turn is grounded in the run's own record; the model
may propose one bounded action from a closed list, which the control plane then performs itself. Training is never an action."""
import asyncio
import json
import os
import re
import uuid

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from services.training_lab import store as lab

ACTIONS = {
    'run_music_baseline': 'Measure the music-identification baseline on the labelled recordings in the library (no training).',
    'measure_staged_corpus': 'Measure sound observables across the staged corpus on the GPU host (readings only).',
    'import_reference_recordings': 'Import public-domain reference recordings (LibriVox speech, Musopen piano) into the library.',
    'ask_specialists': 'Ask the five advisory specialists to review the held reinforcement plan (advice only).',
    'record_training_request': 'Record that the owner asks for training; the request stays held until approved through Model Approval.',
}
SYSTEM = ('You are Akki, the owner\'s training collaborator in the Train Models studio — the same voice the owner has worked with to produce every model on record. '
          'Write like a seasoned machine-learning collaborator: direct, plain English, short paragraphs, no marketing, no headings, no bullet symbols. '
          'Ground every figure in the supplied record; if a figure is not in the record, say it has not been measured rather than estimating it. '
          'You cannot start, stop, approve or admit training. If asked to train, explain that the request stays held until the owner approves it through Model Approval, and offer record_training_request only when the run allows it. '
          'When the owner asks you to do something that matches an allowed action, propose exactly that action and say what it will do; otherwise action is null. '
          'Think in two to four short steps the owner can inspect. Return ONLY JSON matching the schema. No markdown.')
SHAPING = ('This run is still being shaped. Five things are needed before anything can be recorded, in this order: what it produces; what material it reads '
           '(only the estate\'s existing authorized data — RMS transcripts, staged RMS audio, the private media library); how we\'ll know it worked (a number or a clear pass-or-fail on held-out material); '
           'the spend limit in GPU-hours; and the legal basis for using that data. Ask for exactly one missing field per turn and never fill one in yourself — if you guessed, the owner would be committing to a decision they never made. '
           'When the owner\'s message gives one or more fields, return them in `fields` in their own words, tightened. Once what it produces is known, propose a short plain-English `name` for the run (four words or fewer, no version numbers). '
           'When every field is present, say what they are committing to in one short paragraph and that it stays held until approved through Model Approval; offer record_training_request only then.')


class Fields(BaseModel):
    model_config = ConfigDict(extra='forbid')
    produces: str | None = Field(default=None, max_length=400)
    material: str | None = Field(default=None, max_length=400)
    acceptance: str | None = Field(default=None, max_length=400)
    spend_limit: str | None = Field(default=None, max_length=120)
    legal_basis: str | None = Field(default=None, max_length=400)


class Turn(BaseModel):
    model_config = ConfigDict(extra='forbid')
    reply: str = Field(min_length=1, max_length=2000)
    think: list[str] = Field(default_factory=list, max_length=6)
    action: Literal['run_music_baseline', 'measure_staged_corpus', 'import_reference_recordings', 'ask_specialists', 'record_training_request'] | None = None
    fields: Fields | None = None
    name: str | None = Field(default=None, max_length=80)


def collection():
    coll = lab.db().training_lab_conversations
    coll.create_index([('tenant_id', 1), ('run_id', 1)], unique=True)
    return coll


def messages(tenant, run_id):
    doc = collection().find_one({'tenant_id': tenant, 'run_id': run_id}, {'_id': 0})
    return (doc or {}).get('messages', [])


def _append(tenant, run_id, *items):
    collection().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$push': {'messages': {'$each': list(items)}}, '$set': {'updated_at': lab.now()}}, upsert=True)
    return items


def _message(role, text, **extra):
    return {'id': 'tm-' + uuid.uuid4().hex[:10], 'role': role, 'origin': 'conversation', 'at': lab.now(), 'text': text, **extra}


def _figures(text):
    out = set()
    for raw in re.findall(r'\d[\d,]*(?:\.\d+)?', text or ''):
        value = raw.replace(',', '')
        out.add(value)
        try:
            num = float(value)
            out.update({f'{num:g}', f'{num:.1f}', f'{num:.2f}', f'{num:.0f}'})
            if 0 <= num <= 1: out.update({f'{num * 100:.0f}', f'{num * 100:.1f}'})
            if num > 1: out.update({f'{num / 100:.2f}', f'{num / 100:.3f}', f'{num / 100:.4f}'})
        except ValueError:
            pass
    return out


def unverified_figures(reply, evidence):
    """Figures in the reply that cannot be found in the record (in any plain rendering). Years and tiny counts are not flagged."""
    known = _figures(json.dumps(evidence, default=str))
    flagged = []
    for raw in re.findall(r'\d[\d,]*(?:\.\d+)?', reply):
        value = raw.replace(',', '')
        try: num = float(value)
        except ValueError: continue
        if 1900 <= num <= 2100 or num <= 12: continue
        if not (_figures(value) & known): flagged.append(raw)
    return sorted(set(flagged))


async def turn(tenant, actor, run, text):
    from services.chokepoint.llm import invoke
    from services.training_lab import board_runs
    history = [m for m in messages(tenant, run['run_id']) if m['role'] in ('user', 'akki')][-8:]
    user = _message('user', text)
    _append(tenant, run['run_id'], user)
    allowed = {k: ACTIONS[k] for k in run.get('actions', [])}
    if run['status'] == 'In Approval': allowed['record_training_request'] = ACTIONS['record_training_request']
    shaping = run.get('family') == 'owner' and run['status'] == 'Shaping'
    if shaping and run.get('ready'): allowed['record_training_request'] = ACTIONS['record_training_request']
    try:
        response = await asyncio.wait_for(invoke(
            purpose='training_lab.conversation', provider=os.environ['TRAINING_LAB_CONNECTION'], model=os.environ['TRAINING_LAB_MODEL'],
            tenant_id=tenant, actor=actor['principal_id'], custody_class='tenant_estate', masking_tier='llm_prompt_governed_text',
            session_id=f"train-models:{run['run_id']}", system_message=SYSTEM + (' ' + SHAPING if shaping else ''),
            prompt=json.dumps({'schema': Turn.model_json_schema(), 'run': {'name': run['name'], 'status': run['status'], 'objective': run['objective'], 'record': run.get('evidence'),
                                                                               'record_rows': run.get('record_rows'), 'checks': [{'name': c['n'], 'value': c['v']} for c in run.get('checks', [])], 'reason': run.get('reason')},
                               'allowed_actions': allowed, 'recent_messages': [{'role': m['role'], 'text': m['text']} for m in history], 'owner_says': text})), timeout=120)
        raw = response.text.strip()
        if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
        parsed = Turn.model_validate_json(raw)
        fields = {k: v for k, v in (parsed.fields.model_dump() if parsed.fields else {}).items() if v} if shaping else {}
        if shaping and (fields or parsed.name): board_runs.update(tenant, run['run_id'], fields=fields, name=parsed.name if run['name'] == 'New model' else None)
        action = parsed.action if parsed.action in allowed else None
        if action == 'record_training_request' and shaping and not board_runs.ready(board_runs.get(tenant, run['run_id']) or {}): action = None
        flags = unverified_figures(parsed.reply, {'record': run.get('evidence'), 'rows': run.get('record_rows'), 'checks': run.get('checks'), 'owner_says': text, 'fields': fields})
        reply = _message('akki', parsed.reply, think=parsed.think, action=action, flags=flags, receipt_id=response.receipt_id, model=response.model_id, fields=fields or None)
    except Exception as exc:
        reply = _message('akki', 'I could not reach the model boundary just now, so I have not answered that. Nothing about the run has changed.', think=[f'Boundary unavailable · {type(exc).__name__}'], action=None, status='unavailable')
    _append(tenant, run['run_id'], reply)
    return user, reply


def decision(tenant, text, **extra):
    """A deterministic entry the owner made with a control (no model call)."""
    return _message('user', text, widget='decision', **extra)


def note(tenant, text, **extra):
    return _message('akki', text, **extra)


def record(tenant, run_id, *items):
    return _append(tenant, run_id, *items)
