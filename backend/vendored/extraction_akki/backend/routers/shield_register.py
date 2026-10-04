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
    description: str = Field(min_length=3, max_length=600)
    cues: list[str] = Field(default_factory=list, max_length=60)
    targets: list[str] = Field(default_factory=list, max_length=10)
    patterns: list[str] = Field(default_factory=list, max_length=20)
    values: list[str] = Field(default_factory=list, max_length=500)


class Text(BaseModel):
    text: str = Field(min_length=1, max_length=200_000)
    mode: Literal['abstract', 'remove', 'generalise'] = 'abstract'


class Separation(BaseModel):
    document: str = Field(min_length=1, max_length=200_000)
    task: str = Field(min_length=1, max_length=4000)
    dry_run: bool = True


@router.get('/register', response_model=c.Envelope)
async def register(include_removed: bool = False, actor=Depends(census_identity)):
    _operator(actor)
    from services.synisense.shield import semantic_register as reg
    return {'tenant_id': actor['tenant_id'], 'categories': await asyncio.to_thread(reg.categories, actor['tenant_id'], include_removed), 'kinds': list(reg.KINDS), 'actions': list(reg.ACTIONS)}


@router.post('/register', status_code=201, response_model=c.Envelope)
async def author(body: Category, actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    try: doc = await asyncio.to_thread(reg.author, actor['tenant_id'], actor['principal_id'], body.model_dump())
    except (ValueError, Exception) as exc:
        if isinstance(exc, ValueError) or 'pattern' in str(exc).lower(): raise HTTPException(422, str(exc)) from exc
        raise
    return {'tenant_id': actor['tenant_id'], 'category': doc}


@router.delete('/register/{name}', response_model=c.Envelope)
async def remove(name: str, reason: str = 'removed by DPO', actor=Depends(census_identity)):
    _dpo(actor)
    from services.synisense.shield import semantic_register as reg
    try: n = await asyncio.to_thread(reg.remove, actor['tenant_id'], actor['principal_id'], name, reason)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'removed': n}


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
