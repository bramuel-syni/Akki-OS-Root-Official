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


class Text(BaseModel):
    text: str = Field(min_length=1, max_length=200_000)
    mode: Literal['abstract', 'remove', 'generalise'] = 'abstract'


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
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(reg.propose, actor['tenant_id'], actor['principal_id'], body.text, body.source_ref)}


@router.post('/register/{name}/adopt', response_model=c.Envelope)
async def adopt(name: str, body: Adoption, actor=Depends(census_identity)):
    """Adopt a draft → pending (B28). Nothing changes at the crossing until approval."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    doc = await asyncio.to_thread(_lifecycle, lambda: reg.adopt(actor['tenant_id'], actor['principal_id'], name, body.model_dump()))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/approve', response_model=c.Envelope)
async def approve(name: str, actor=Depends(census_identity)):
    """Approve a pending declaration into force (B29): the governed act that makes it binding at the crossing."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    doc = await asyncio.to_thread(_lifecycle, lambda: reg.approve(actor['tenant_id'], actor['principal_id'], name))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/withdraw', response_model=c.Envelope)
async def withdraw(name: str, body: Reason, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    doc = await asyncio.to_thread(_lifecycle, lambda: reg.withdraw(actor['tenant_id'], actor['principal_id'], name, body.reason))
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.post('/register/{name}/removal/countersign', response_model=c.Envelope)
async def countersign(name: str, actor=Depends(census_identity)):
    """Second signature on a proposed removal, by a different DPO/master admin; starts the visible countdown (B39)."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
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
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(_lifecycle, run)}


@router.post('/register/{name}/reach', response_model=c.Envelope)
async def reach(name: str, actor=Depends(census_identity)):
    """Review (B26): what this declaration would touch in the measured material; the unmeasured is stated."""
    _operator(actor)
    from services.synisense.shield import register_vault, semantic_register as reg
    def run():
        cats = [x for x in reg.categories(actor['tenant_id'], include_removed=False, include_drafts=True, include_pending=True) if x['name'] == name]
        if not cats: raise LookupError('No declaration with that name')
        measured, errors = register_vault.measured_material(actor['tenant_id'])
        out = register_vault.reach(cats[:1], measured)
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
    return {'tenant_id': actor['tenant_id'], 'category': await asyncio.to_thread(_lifecycle, run)}


@router.delete('/register/{name}', response_model=c.Envelope)
async def remove(name: str, reason: str = 'removed by DPO', actor=Depends(census_identity)):
    """Propose removal (A5.4 B39): starts the governed ceremony — second signature, visible countdown, apply, re-verify. Protection continues meanwhile."""
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    doc = await asyncio.to_thread(_lifecycle, lambda: reg.remove(actor['tenant_id'], actor['principal_id'], name, reason))
    return {'tenant_id': actor['tenant_id'], 'category': doc, 'removal': doc['removal']}


@router.post('/classify', response_model=c.Envelope)
async def classify(body: Text, actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import semantic_register as reg
    spans = await asyncio.to_thread(reg.classify, body.text, actor['tenant_id'])
    return {'tenant_id': actor['tenant_id'], 'spans': spans, 'categories': sorted({s['category'] for s in spans} | {a for s in spans for a in s.get('also', [])})}


@router.post('/reconstruct', response_model=c.Envelope)
async def reconstruct(body: Text, actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import semantic_register as reg
    out = await asyncio.to_thread(reg.reconstruct, body.text, actor['tenant_id'], body.mode)
    return {'tenant_id': actor['tenant_id'], **{k: v for k, v in out.items() if k != 'bindings'}, 'bindings_held_inside': len(out['bindings']), 'binding_tokens': {k: v['hint'] for k, v in out['bindings'].items()}}


@router.post('/separate', response_model=c.Envelope)
async def separate(body: Separation, actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import task_separation
    receipt = await task_separation.separate(body.document, body.task, actor['tenant_id'], actor['principal_id'], dry_run=body.dry_run)
    return {'tenant_id': actor['tenant_id'], 'receipt': receipt}


@router.get('/separations', response_model=c.Envelope)
async def separations(actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import task_separation
    return {'tenant_id': actor['tenant_id'], 'receipts': await asyncio.to_thread(task_separation.receipts, actor['tenant_id'])}
