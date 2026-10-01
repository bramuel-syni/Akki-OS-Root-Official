"""Existing training workspace's artifact and evidence operations; no alternative approval system."""
from fastapi import APIRouter, Depends, HTTPException
from services.enforce.census_identity import census_identity
from services.training_lab.contracts import Envelope
from services.training_lab.production_contracts import Definition, StageEvidence, RecipeRevision
from services.training_lab import production, production_evidence, board_runs
from routers.training_lab import operator
from pydantic import BaseModel, Field


class DatasetSelection(BaseModel):
    file_ids: list[str] = Field(min_length=1, max_length=200)

router = APIRouter(prefix='/api/training/lab/production', tags=['training-laboratory'])


def perform(fn, *args):
    try:
        return fn(*args)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from None
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc)) from None


@router.get('/catalogue', response_model=Envelope)
def catalogue(actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'registers': production_evidence.catalogue(actor['tenant_id'])}


@router.post('/runs/{run_id}/definition', response_model=Envelope)
def define(run_id: str, body: Definition, actor=Depends(census_identity)):
    operator(actor)
    tenant = actor['tenant_id']
    doc = board_runs.get(tenant, run_id)
    if not doc: raise HTTPException(404, 'No objective with that reference is available in this estate.')
    if doc['status'] != 'Shaping': raise HTTPException(409, 'Open a new version to change a recorded objective.')
    perform(production.validate_definition, tenant, body.model_dump())
    board_runs.collection().update_one({'tenant_id': tenant, 'run_id': run_id, 'status': 'Shaping'},
        {'$set': {'definition': body.model_dump()}})
    return {'tenant_id': tenant, 'run_id': run_id, 'definition': body.model_dump(), 'state': 'draft', 'training_started': False}


@router.post('/runs/{run_id}/compile', response_model=Envelope)
def compile_definition(run_id: str, actor=Depends(census_identity)):
    operator(actor)
    doc = board_runs.get(actor['tenant_id'], run_id)
    if not doc: raise HTTPException(404, 'No objective with that reference is available in this estate.')
    plan = perform(production.compile_plan, actor['tenant_id'], actor, run_id, doc.get('definition'))
    return {'tenant_id': actor['tenant_id'], 'plan': plan}


@router.get('/plans/{plan_id}', response_model=Envelope)
def read(plan_id: str, actor=Depends(census_identity)):
    plan = production.get(actor['tenant_id'], plan_id)
    if not plan: raise HTTPException(404, 'No production plan with that reference is available in this estate.')
    return {'tenant_id': actor['tenant_id'], 'plan': plan}


@router.post('/plans/{plan_id}/evidence/{stage}', response_model=Envelope)
def attach(plan_id: str, stage: str, body: StageEvidence, actor=Depends(census_identity)):
    operator(actor)
    return {'tenant_id': actor['tenant_id'], 'plan': perform(production.attach, actor['tenant_id'], plan_id, stage, body.job_id)}


@router.post('/plans/{plan_id}/recipes', response_model=Envelope)
def recipe(plan_id: str, body: RecipeRevision, actor=Depends(census_identity)):
    operator(actor)
    return {'tenant_id': actor['tenant_id'], 'plan': perform(production.revise_recipe, actor['tenant_id'], plan_id, actor, body)}


@router.post('/plans/{plan_id}/dataset', response_model=Envelope)
def dataset(plan_id: str, body: DatasetSelection, actor=Depends(census_identity)):
    operator(actor)
    from services.media_library.dataset_preparation import prepare
    return {'tenant_id': actor['tenant_id'], 'preparation': perform(prepare, actor, plan_id, body.file_ids)}


@router.get('/plans/{plan_id}/moac', response_model=Envelope)
def moac(plan_id: str, actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'pack': perform(production.moac_request, actor['tenant_id'], plan_id)}