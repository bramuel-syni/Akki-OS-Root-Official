"""Shield register and reconstruction routes. Authoring and removal are DPO/master-admin acts; classification, reconstruction and separation need an operator."""
import asyncio
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/shield', tags=['shield'])


def _operator(actor):
    if not {'operator', 'master_admin', 'dpo'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


def _dpo(actor):
    if not {'dpo', 'master_admin'}.intersection(actor['roles']): raise HTTPException(403, 'Register authoring is a DPO act')


class Category(BaseModel):
    name: str = Field(min_length=2, max_length=80, pattern=r'^[a-z][a-z0-9_]+$')
    kind: Literal['exact', 'pattern', 'contextual']
    action: Literal['remove', 'abstract', 'generalise']
    enforcement: Literal['enforced', 'advisory'] = 'enforced'
    description: str = Field(min_length=3, max_length=600)
    cues: list[str] = Field(default_factory=list, max_length=60)
    targets: list[str] = Field(default_factory=list, max_length=10)
    patterns: list[str] = Field(default_factory=list, max_length=20)
    values: list[str] = Field(default_factory=list, max_length=500)
    entity_type: str | None = Field(default=None, pattern=r'^[A-Z][A-Z0-9_]{1,30}$')


class Proposal(BaseModel):
    text: str = Field(min_length=1, max_length=200_000)
    source_ref: str | None = Field(default=None, max_length=200)


class Adoption(BaseModel):
    action: Literal['remove', 'abstract', 'generalise'] | None = None
    enforcement: Literal['enforced', 'advisory'] | None = None
    description: str | None = Field(default=None, max_length=600)
    cues: list[str] | None = Field(default=None, max_length=60)
    values: list[str] | None = Field(default=None, max_length=500)


class Enforcement(BaseModel):
    enforcement: Literal['enforced', 'advisory']


class Reason(BaseModel):
    reason: str = Field(min_length=3, max_length=300)


class Vault(BaseModel):
    file_id: str = Field(min_length=8, max_length=64)
    source_ref: str | None = Field(default=None, max_length=200)


def _lifecycle(call):
    """Map register lifecycle refusals to HTTP: unknown → 404, invalid → 422, wrong state / missing second signature / countdown → 409."""
    from services.rules_service import ceremony
    from services.synisense.shield import semantic_register as reg
    try: return call()
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc
    except (reg.Conflict, ceremony.SecondSignatoryMissing, ceremony.CountdownNotElapsed) as exc: raise HTTPException(409, str(exc)) from exc


def _watched(actor, boundary, body):
    """WP-A7: every Shield governed act and the reader relay cross a Watch commission gate (M2 inventory) — observed, Mkono-enforced, tripwired."""
    from services.watch import commission_gate
    return commission_gate.crossing(actor, boundary, body)


class Text(BaseModel):
    text: str = Field(min_length=1, max_length=200_000)
    mode: Literal['abstract', 'remove', 'generalise'] = 'abstract'
    reader: Literal['auto', 'off'] = 'auto'


class Separation(BaseModel):
    document: str = Field(min_length=1, max_length=200_000)
    task: str = Field(min_length=1, max_length=4000)
    dry_run: bool = True


@router.get('/register', response_model=c.Envelope)
async def register(include_removed: bool = False, include_drafts: bool = True, include_pending: bool = True, actor=Depends(census_identity)):
    _operator(actor)
    from services.rules_service import ceremony
    from services.synisense.shield import semantic_register as reg
    return {'tenant_id': actor['tenant_id'], 'categories': await asyncio.to_thread(reg.categories, actor['tenant_id'], include_removed, include_drafts, include_pending), 'kinds': list(reg.KINDS), 'actions': list(reg.ACTIONS), 'enforcement': list(reg.ENFORCEMENT),
            'statuses': list(reg.STATUSES), 'removal_countdown_hours': ceremony.SYSTEM_ORDINARY_COUNTDOWN_HOURS, 'principal_id': actor['principal_id'], 'can_author': bool({'dpo', 'master_admin'}.intersection(actor['roles']))}


@router.post('/register/propose', response_model=c.Envelope)
async def propose(body: Proposal, actor=Depends(census_identity)):
    """Generate (B25): cue proposer + the contained reader's undeclared privileged findings; the reader's absence is disclosed, never hidden."""
    _dpo(actor)
    from services.synisense.shield import category3, semantic_register as reg
    from services.synisense.shield.contained_reader import ReaderUnavailable
    def run():
        findings, reader = [], {'applied': False}
        try:
            out = category3.recognise(body.text[:category3.CHUNK_CHARS * 4], actor['tenant_id'], 'register.propose'); findings = out['undeclared']; reader = {'applied': True, **category3.summary(out)}
        except ReaderUnavailable as exc: reader = {'applied': False, 'unavailable': str(exc)[:160]}
        return {**reg.propose(actor['tenant_id'], actor['principal_id'], body.text, body.source_ref, reader_findings=findings), 'reader': reader}
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(run)}


@router.post('/register/{name}/adopt', response_model=c.Envelope)
async def adopt(name: str, body: Adoption, actor=Depends(census_identity)):
    """Adopt a draft → pending (B28). Nothing changes at the crossing until approval."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_adopt', {'name': name, **body.model_dump()}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.adopt(actor['tenant_id'], actor['principal_id'], name, body.model_dump()))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/approve', response_model=c.Envelope)
async def approve(name: str, actor=Depends(census_identity)):
    """Approve a pending declaration into force (B29): the governed act that makes it binding at the crossing."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_approve', {'name': name}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.approve(actor['tenant_id'], actor['principal_id'], name))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/withdraw', response_model=c.Envelope)
async def withdraw(name: str, body: Reason, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_withdraw', {'name': name, 'reason': body.reason}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.withdraw(actor['tenant_id'], actor['principal_id'], name, body.reason))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/removal/countersign', response_model=c.Envelope)
async def countersign(name: str, actor=Depends(census_identity)):
    """Second signature on a proposed removal, by a different DPO/master admin; starts the visible countdown (B39)."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_removal_countersign', {'name': name}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.countersign_removal(actor['tenant_id'], actor['principal_id'], name))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/removal/cancel', response_model=c.Envelope)
async def cancel_removal(name: str, body: Reason, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    doc = await asyncio.to_thread(_lifecycle, lambda: reg.cancel_removal(actor['tenant_id'], actor['principal_id'], name, body.reason))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/removal/apply', response_model=c.Envelope)
async def apply_removal(name: str, actor=Depends(census_identity)):
    """Apply a counter-signed removal once its countdown has elapsed; the crossing is re-verified and the result recorded."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_removal_apply', {'name': name}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.apply_removal(actor['tenant_id'], actor['principal_id'], name))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/vault', response_model=c.Envelope)
async def vault(body: Vault, actor=Depends(census_identity)):
    """Workbook intake: a CSV/XLSX upload in the media library → pending declarations + reach over measured material only (A5.3)."""
    _dpo(actor)
    from services.media_library.storage import StorageError
    from services.synisense.shield import register_vault
    def run():
        try: return register_vault.intake_file(actor['tenant_id'], {'tenant_id': actor['tenant_id'], 'principal_id': actor['principal_id']}, body.file_id, body.source_ref)
        except StorageError as exc: raise HTTPException(503, 'The library file could not be read from storage') from exc
    with _watched(actor, 'shield.vault_intake', body.model_dump()):
        out = await asyncio.to_thread(_lifecycle, run)
    return {'tenant_id': actor['tenant_id'], **out}


@router.post('/register/{name}/reach', response_model=c.Envelope)
async def reach(name: str, actor=Depends(census_identity)):
    """Review (B26, A5.2/A5.3): what this declaration would touch in the measured material; Category-3 reach is measured by the contained reader; the unmeasured is stated."""
    _operator(actor)
    from services.synisense.shield import category3, register_vault, semantic_register as reg
    def run():
        cats = [x for x in reg.categories(actor['tenant_id'], include_removed=False, include_drafts=True, include_pending=True) if x['name'] == name]
        if not cats: raise LookupError('No declaration with that name')
        measured, errors = register_vault.measured_material(actor['tenant_id'])
        out = register_vault.reach(cats[:1], measured)
        if cats[0]['kind'] == 'contextual': out['by_declaration'][name] = register_vault.reach_contextual(cats[0], measured, actor['tenant_id'], category3.recognise)
        if errors: out['measurement_errors'] = errors
        return out
    return {'tenant_id': actor['tenant_id'], 'name': name, **await asyncio.to_thread(_lifecycle, run)}


@router.delete('/register/{name}/draft', response_model=c.Envelope)
async def discard(name: str, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    try: n = await asyncio.to_thread(reg.discard, actor['tenant_id'], actor['principal_id'], name)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'discarded': n}


@router.post('/register/{name}/enforcement', response_model=c.Envelope)
async def enforcement(name: str, body: Enforcement, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_enforcement', {'name': name, 'enforcement': body.enforcement}):
        try: doc = await asyncio.to_thread(reg.set_enforcement, actor['tenant_id'], actor['principal_id'], name, body.enforcement)
        except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.get('/crossings', response_model=c.Envelope)
async def crossings(limit: int = 40, actor=Depends(census_identity)):
    """Recent model crossings with the register gate's summary — what was found, rewritten, inspected and refused. Values never appear.
    Reads the newest receipt files only (the record holds tens of thousands)."""
    _operator(actor)
    import json
    from services.chokepoint import _receipt_dir
    def read():
        d = _receipt_dir(); files = list(d.glob('rcp-*.json')) if d.is_dir() else []
        newest = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:500]
        rows = []
        for f in newest:
            try: rows.append(json.loads(f.read_text()))
            except Exception: continue
        rows.sort(key=lambda r: r.get('at_iso', ''), reverse=True)
        out = []
        for r in rows[:max(1, min(limit, 200))]:
            shape = r.get('payload_shape') or {}
            out.append({'receipt_id': r['receipt_id'], 'at': r.get('at_iso'), 'kind': r['kind'], 'purpose': shape.get('purpose_declared'), 'model': shape.get('model_id'), 'provider': shape.get('provider'), 'masking_tier': r.get('masking_tier'),
                        'tokens_in': shape.get('tokens_in'), 'tokens_out': shape.get('tokens_out'), 'register': shape.get('shield_register'), 'gated': 'shield_register' in shape})
        return {'crossings': out, 'total_on_record': len(files), 'window': len(rows), 'gated_in_window': sum(1 for r in rows if 'shield_register' in (r.get('payload_shape') or {}))}
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(read)}


@router.post('/register', status_code=201, response_model=c.Envelope)
async def author(body: Category, actor=Depends(census_identity)):
    """Declare a category (Generate + Adopt): it lands pending; `approve` puts it in force."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    def run():
        try: return reg.author(actor['tenant_id'], actor['principal_id'], body.model_dump())
        except Exception as exc:
            if not isinstance(exc, (ValueError, LookupError, reg.Conflict)) and 'pattern' in str(exc).lower(): raise HTTPException(422, str(exc)) from exc
            raise
    with _watched(actor, 'shield.register_author', body.model_dump()):
        doc = await asyncio.to_thread(_lifecycle, run)
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.delete('/register/{name}', response_model=c.Envelope)
async def remove(name: str, reason: str = 'removed by DPO', actor=Depends(census_identity)):
    """Propose removal (A5.4 B39): starts the governed ceremony — second signature, visible countdown, apply, re-verify. Protection continues meanwhile."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    with _watched(actor, 'shield.register_removal', {'name': name, 'reason': reason}):
        doc = await asyncio.to_thread(_lifecycle, lambda: reg.remove(actor['tenant_id'], actor['principal_id'], name, reason))
    return {'tenant_id': actor['tenant_id'], 'category': doc, 'removal': doc['removal']}


@router.post('/register/{name}/removal', response_model=c.Envelope)
async def propose_removal(name: str, body: Reason, actor=Depends(census_identity)):
    """JSON-body form of the removal proposal (same ceremony as DELETE /register/{name})."""
    return await remove(name, body.reason, actor)


def _recognised(text, tenant, purpose, fail_closed):
    """Category-3 reading for the classify/reconstruct routes: `fail_closed` raises 503 when the reader is unavailable (protection); otherwise the absence is disclosed."""
    from services.synisense.shield import category3
    from services.synisense.shield.contained_reader import ReaderUnavailable
    try: return category3.recognise(text, tenant, purpose)
    except ReaderUnavailable as exc:
        if fail_closed: raise HTTPException(503, f'contained reader unavailable; reconstruction refuses rather than guess: {str(exc)[:160]}') from exc
        return {'spans': [], 'unavailable': str(exc)[:160], 'indirect_disclosures': [], 'undeclared': [], 'ambiguous': [], 'blocking_ambiguities': 0, 'receipts': [], 'seconds': 0, 'chunks': 0}


@router.post('/classify', response_model=c.Envelope)
async def classify(body: Text, actor=Depends(census_identity)):
    """Category 1/2 deterministically; Category 3 through the contained reader (`reader=auto`); cue hits are advisory receipts, listed apart."""
    _operator(actor)
    from services.synisense.shield import category3, semantic_register as reg
    def run():
        text = body.text[:category3.CHUNK_CHARS * 4]
        recognised = _recognised(text, actor['tenant_id'], 'shield.classify', fail_closed=False) if body.reader == 'auto' else {'spans': [], 'skipped': 'reader=off'}
        spans = reg.classify(text, actor['tenant_id'], reader_spans=recognised['spans'])
        found = [s for s in spans if not s.get('proposer')]
        return {'spans': spans, 'categories': sorted({s['category'] for s in found} | {a for s in found for a in s.get('also', [])}), 'cues_advisory': sorted({s['category'] for s in spans if s.get('proposer')}),
                'reader': {k: v for k, v in category3.summary(recognised).items()} | {k: recognised[k] for k in ('unavailable', 'skipped') if k in recognised}, 'undeclared_privileged': len(recognised.get('undeclared') or [])}
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(run)}


@router.post('/reconstruct', response_model=c.Envelope)
async def reconstruct(body: Text, actor=Depends(census_identity)):
    """Safe reconstruction: Category 3 by the contained reader (fail closed when it is unavailable), Category 1/2 deterministically; bindings stay inside."""
    _operator(actor)
    from services.synisense.shield import category3, semantic_register as reg
    def run():
        text = body.text[:category3.CHUNK_CHARS * 4]
        recognised = _recognised(text, actor['tenant_id'], 'shield.reconstruct', fail_closed=True) if body.reader == 'auto' else {'spans': [], 'skipped': 'reader=off', 'blocking_ambiguities': 0}
        if recognised.get('blocking_ambiguities'): raise HTTPException(409, f"{recognised['blocking_ambiguities']} marked meaning(s) of an enforced category could not be bound to the text; refusing rather than guessing")
        out = reg.reconstruct(text, actor['tenant_id'], body.mode, reader_spans=recognised['spans'])
        return {**{k: v for k, v in out.items() if k != 'bindings'}, 'bindings_held_inside': len(out['bindings']), 'binding_tokens': {k: v['hint'] for k, v in out['bindings'].items()}, 'reader': category3.summary(recognised) | {k: recognised[k] for k in ('skipped',) if k in recognised}}
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(run)}


@router.post('/separate', response_model=c.Envelope)
async def separate(body: Separation, actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import task_separation
    with _watched(actor, 'shield.separate', {'document': body.document, 'task': body.task, 'dry_run': body.dry_run}):  # the gate persists a digest only; the tripwire reads the body in-process
        receipt = await task_separation.separate(body.document, body.task, actor['tenant_id'], actor['principal_id'], dry_run=body.dry_run)
    return {'tenant_id': actor['tenant_id'], 'receipt': receipt}


@router.get('/separations', response_model=c.Envelope)
async def separations(actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import task_separation
    return {'tenant_id': actor['tenant_id'], 'receipts': await asyncio.to_thread(task_separation.receipts, actor['tenant_id'])}


# ----------------------------------------------------------------------------- contained reader (WP-A2): the estate's reasoning rung for privileged text
def _master(actor):
    if 'master_admin' not in actor['roles']: raise HTTPException(403, 'Starting, revoking or stopping the contained reader is a master-admin act')


class ReaderStart(BaseModel):
    host: str = Field(default='akki-vm-ii', pattern=r'^[a-z0-9-]+$')
    gpu_index: Literal[0, 1] = 1
    base_registry_id: str = Field(default='qwen3-8b-base', pattern=r'^[a-z0-9.-]+$')
    lawful_ref: str = Field(default='OWNER_ORDERS §12 Wave A autonomous · BUILD_PLAN_V2 WP-A2', max_length=200)


class ReaderRead(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    purpose: str = Field(default='shield.read_probe', max_length=80)


def _reader(call):
    from services.synisense.shield.contained_reader import ReaderUnavailable
    from services.model_registry.residency import PlacementRefused
    try: return call()
    except ReaderUnavailable as exc: raise HTTPException(503, str(exc)) from exc
    except PlacementRefused as exc: raise HTTPException(409, str(exc)) from exc
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc


@router.get('/reader', response_model=c.Envelope)
async def reader_status(actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import contained_reader as cr
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(cr.status)}


@router.get('/reader/health', response_model=c.Envelope)
async def reader_health(actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import contained_reader as cr
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(_reader, cr.health)}


@router.get('/reader/egress-probe', response_model=c.Envelope)
async def reader_egress_probe(actor=Depends(census_identity)):
    """A real outbound attempt from inside the reader process; it must report blocked."""
    _operator(actor)
    from services.synisense.shield import contained_reader as cr
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(_reader, cr.egress_probe)}


@router.post('/reader/start', response_model=c.Envelope)
async def reader_start(body: ReaderStart, actor=Depends(census_identity)):
    _master(actor)
    from services.synisense.shield import contained_reader as cr
    with _watched(actor, 'shield.reader_start', body.model_dump()):
        out = await asyncio.to_thread(_reader, lambda: cr.start(actor['principal_id'], body.lawful_ref, body.host, body.gpu_index, body.base_registry_id))
    return {'tenant_id': actor['tenant_id'], 'job': {k: out['job'].get(k) for k in ('job_id', 'status', 'host', 'reason', 'started_at')}, 'placement': out.get('placement'), 'already_running': out['already_running'], 'model_id': out['entry'].get('model_id')}


@router.post('/reader/read', response_model=c.Envelope)
async def reader_read(body: ReaderRead, actor=Depends(census_identity)):
    """Read a passage inside the perimeter with the tenant's declared categories; refuses when the reader is unavailable (no external fallback)."""
    _operator(actor)
    from services.synisense.shield import contained_reader as cr, semantic_register as reg
    def run():
        cats = [{'name': x['name'], 'description': x.get('description')} for x in reg.categories(actor['tenant_id'])]
        return cr.read(body.text, cats, body.purpose)
    with _watched(actor, 'shield.reader_read', {'text': body.text, 'purpose': body.purpose}):
        out = await asyncio.to_thread(_reader, run)
    return {'tenant_id': actor['tenant_id'], **out}


@router.post('/reader/revoke', response_model=c.Envelope)
async def reader_revoke(body: Reason, actor=Depends(census_identity)):
    _master(actor)
    from services.synisense.shield import contained_reader as cr
    with _watched(actor, 'shield.reader_revoke', body.model_dump()):
        out = await asyncio.to_thread(_reader, lambda: cr.revoke(body.reason, actor['principal_id']))
    return {'tenant_id': actor['tenant_id'], **out}


@router.post('/reader/stop', response_model=c.Envelope)
async def reader_stop(body: Reason, actor=Depends(census_identity)):
    _master(actor)
    from services.synisense.shield import contained_reader as cr
    with _watched(actor, 'shield.reader_stop', body.model_dump()):
        out = await asyncio.to_thread(_reader, lambda: cr.stop(body.reason, actor['principal_id']))
    return {'tenant_id': actor['tenant_id'], **out}
