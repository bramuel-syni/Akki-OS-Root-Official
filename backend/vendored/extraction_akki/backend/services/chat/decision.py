"""One query decision per turn (Doc 8 #21 / B5): warm, fresh or refused — decided once, recorded once.

Warm: matching qualified units exist → answer from the working set with zero source reads.
Fresh: nothing qualified matches but a censused table of this tenant does → the specific missing slice is drafted
through the existing commission builder (acknowledgement + estimate); nothing is dispatched here.
Refused: no qualified unit and no censused table names the subject → out of scope, logged and dropped.
"""
import os

from services.census_autonomy.operational_scope import sources_for
from services.commissioning import census_profile, shaping
from services.commissioning.shaping import DraftBody, Reach
from services.extraction_runtime.structured_records_worker import unit_terms
from services.northena import gate

FRESH_OPERATION = 'processed_intelligence'
# Versioned relevance rule (M4): a warm answer needs the question to name its subject, not merely share one word
# with one unit. The rule, its inputs and its outcome are banked in the turn's decision so nothing is silent.
SUBJECT_RULE = 'chat.subject_match.v1'
# Versioned fresh-slice rule (M4): a censused table is the subject of a question only when the question names the
# table itself or at least two of its columns; one shared column word ('name', 'city') is not a subject.
SLICE_RULE = 'chat.fresh_slice.v2'


def _region_terms(artefact):
    raw = ' '.join([artefact.get('region') or '', *(artefact.get('columns') or [])])
    return unit_terms(raw) | unit_terms(raw.replace('_', ' ').replace('.', ' '))


def subject_match(terms, candidates, artefacts):
    """On subject when (a) a question term names the matched region or one of its columns, (b) the best matched unit
    shares at least two distinct terms with the question, or (c) a short question (under three terms) matched at all."""
    wanted = set(terms)
    matched = [c for c in candidates if c['kind'] == 'matched']
    best = max((c['overlap'] for c in matched), default=0)
    regions = sorted({c['region'] for c in matched})
    named = sorted({r for r in regions for a in artefacts if a.get('region') == r and _region_terms(a) & wanted})
    on_subject = bool(matched) and (bool(named) or best >= 2 or (len(wanted) < 3 and best >= 1))
    return {'rule': SUBJECT_RULE, 'on_subject': on_subject, 'question_terms': len(wanted), 'best_overlap': best,
            'matched_units': len(matched), 'regions_named_by_question': named,
            'weak_regions': [] if on_subject else regions,
            'basis': 'question names the region' if named else f'best unit shares {best} term(s) with a {len(wanted)}-term question'}


def _names_table(table, wanted):
    """The question names a table when it carries the table token itself or every word of its split name."""
    words = unit_terms(table.replace('_', ' '))
    return table.lower() in wanted or bool(words) and words <= set(wanted)


def _table_score(row, terms):
    wanted = set(terms)
    table = unit_terms(row['table']) | unit_terms(row['table'].replace('_', ' '))
    raw = ' '.join([row['database'], *row['columns']])
    other = (unit_terms(raw) | unit_terms(raw.replace('_', ' '))) - table
    named, columns = _names_table(row['table'], wanted), len(other & wanted)
    return (2 * len(table & wanted) + columns) if named or columns >= 2 else 0, named


async def fresh_slice(tenant, terms):
    """The censused table whose names best match the question under SLICE_RULE; None when no table names the subject.
    The row carries `table_named` so the caller knows whether the question named the table itself."""
    scored = []
    for source_id in sources_for(tenant):
        for row in (await census_profile.tables_for(tenant, source_id)) or []:
            score, named = _table_score(row, terms)
            if score:
                # best name match first; a table that holds rows before an empty one; then the smallest slice.
                scored.append((-score, row['row_count'] == 0, row['row_count'], row['database'], row['table'], {**row, 'source_id': source_id, 'table_named': named}))
    return sorted(scored, key=lambda s: s[:5])[0][5] if scored else None


async def _existing_draft(db, scope, slice_):
    """The requester's open draft for the same slice, if one exists: one gap → one draft, never a pile."""
    for row in await shaping.listing(db, scope):
        if row['state'] != 'draft' or row['operation'] != FRESH_OPERATION:
            continue
        reach = (await shaping.load(db, scope, row['draft_id']))['envelope'].get('reach') or {}
        if reach.get('database') == slice_['database'] and reach.get('table') == slice_['table']:
            return await shaping.view(db, scope, row['draft_id'])
    return None


async def decide(db, scope, *, session_id, turn_id, question, terms, artefacts, candidates):
    regions = sorted({a['region'] for a in artefacts})
    subject = subject_match(terms, candidates, artefacts)
    matched = sorted({c['region'] for c in candidates if c['kind'] == 'matched'}) if subject['on_subject'] else []
    slice_ = None
    # A question that names a censused table not yet qualified is about THAT table, even when loose units match elsewhere;
    # a question that names a qualified table itself stays warm.
    qualified_named = any(_names_table(r.split('.', 1)[-1], set(terms)) for r in regions)
    named = await fresh_slice(scope['tenant_id'], terms) if not qualified_named else None
    if named and named.get('table_named') and f"{named['database']}.{named['table']}" not in regions:
        matched, slice_ = [], named
        subject = {**subject, 'on_subject': False, 'overridden_by': SLICE_RULE, 'basis': f"question names censused table {named['database']}.{named['table']}"}
    if matched:
        sub_objective, scope_set = matched[0], set(regions)
    else:
        slice_ = slice_ or await fresh_slice(scope['tenant_id'], terms)
        if slice_:
            sub_objective = f"{slice_['database']}.{slice_['table']}"
            scope_set = set(regions) | {sub_objective}
        else:
            sub_objective, scope_set = 'unresolved', set(regions)
    route = await gate.route(run_id=session_id, trace_id=turn_id, sub_objective=sub_objective,
                             artifact_ref={'artifact_type': 'objective_request', 'artifact_id': f'chat-{session_id}', 'version': 'v1'},
                             lawful_basis_ref=os.environ.get('CENSUS_LAWFUL_BASIS_PATH', 'chat:governed_answer'),
                             scope=scope_set, warm_index=regions)
    decision = {'decision': route['decision'], 'reason': route['reason'], 'ledger_row_id': route['ledger_row']['row_id'],
                'sub_objective': sub_objective, 'scope_regions': regions, 'matched_regions': matched, 'subject_match': subject, 'slice_rule': SLICE_RULE}
    if route['decision'] == 'fresh' and slice_:
        decision['slice'] = {k: slice_[k] for k in ('source_id', 'database', 'table', 'row_count', 'column_count', 'primary_key', 'census_run_id')}
        decision['slice']['personal_columns'] = slice_['personal_columns']
        if {'operator', 'master_admin'} & set(scope['roles']):
            view = await _existing_draft(db, scope, slice_) or await shaping.save(db, scope, DraftBody(
                objective_text=question[:8000], operation=FRESH_OPERATION, units=[slice_['source_id']],
                reach=Reach(database=slice_['database'], table=slice_['table'])))
            feasibility, quote = view.get('feasibility') or {}, view.get('quote') or {}
            decision['draft'] = {**{k: view.get(k) for k in ('draft_id', 'state', 'version', 'freeze_ready')},
                                 'feasibility': {k: feasibility.get(k) for k in ('verdict', 'reason_code', 'basis', 'job_kind')},
                                 'quote': {k: quote.get(k) for k in ('model', 'total', 'currency', 'rate_card_status')}}
            decision['acknowledgement'] = (f"Nothing qualified covers this yet. The missing slice {sub_objective} has been drafted as commission "
                                           f"{view['draft_id']}; it runs only after freeze and the estate's approvals.")
        else:
            decision['draft'] = None
            decision['acknowledgement'] = (f"Nothing qualified covers this yet. The missing slice is {sub_objective}; an admitted operator "
                                           f"must commission it before it can be answered.")
    return decision
