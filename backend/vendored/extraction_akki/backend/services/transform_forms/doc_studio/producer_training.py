"""Receipted training evidence → existing document studio. No invented results or admission."""
import re
from services.transform_forms.doc_studio.frames import frame_for, verdict_from_frame
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief
from services.transform_forms.doc_studio.producer_estate import commission_id_for
from services.training_lab import board, production


def commission_from_training(run_id, tenant, principal, now):
    from services.training_lab.production_evidence import measured_job
    if not run_id.startswith(('m9j-', 'lcj-')):
        raise LookupError('A completed measured training run is required for a white paper.')
    if run_id.startswith('m9j-'):
        job, _ = measured_job(tenant, run_id)
        if job.get('phase') not in ('train', 'lab_train_music'):
            raise ValueError('The worker record does not measure a training stage.')
        if (job.get('run_certificate') or {}).get('drill'):
            raise ValueError('An engineering recovery run is not a model white paper candidate.')
    else:
        from services.audio_plane_v1 import language_cognition_dispatch as lc
        job = lc.load_job(run_id) if tenant == 'RMS' else None
        if not job or job.get('status') != 'completed' or not job.get('run_certificate'):
            raise LookupError('No completed audio training record is available in this estate.')
    # A signed board run is written up under its own name; the GPU job id is how the autopilot refers to it.
    run = next((r for r in board.runs(tenant) if r['run_id'] == run_id or ((r.get('approval') or {}).get('dispatch') or {}).get('job_id') == run_id), None)
    if not run: raise LookupError('No training record with that reference is available in this estate.')
    production_plan = production.collection().find_one({'tenant_id': tenant, 'stages.training.job_id': run_id}, {'_id': 0}, sort=[('created_at', -1)])
    day, stamp = now.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%dT%H:%M:%SZ')
    content_id = 'training-' + run_id
    receipts = {'R01': {'resolves_to': f"Measured training receipt and retained acceptance record for {run_id}", 'platform_ref': run_id}}
    claims = {}
    decision = f"{run['name']}: {run['status']}. {run.get('reason') or 'See the retained admission decision; serving remains a separate operation.'}"
    narrative = {'decision': {'text': decision, 'receipt': 'R01', 'class': 'recorded'}}
    blocks = [{'heading': 'Outcome and decision', 'blocks': [{'para': decision + ' (Source: R01)'}]}]
    for i, (label, value) in enumerate(run['record_rows'], 2):
        key = f'C{i:03}'
        text = f'{label}: {value}'
        narrative[key] = {'text': text, 'receipt': 'R01', 'class': 'recorded'}
        blocks.append({'heading': label, 'blocks': [{'para': text + ' (Source: R01)'}]})
    for i, check in enumerate(run['checks'], 100):
        key = f'C{i:03}'
        text = f"{check['n']}: {check['v']}."
        narrative[key] = {'text': text, 'receipt': 'R01', 'class': 'measured'}
        blocks.append({'heading': check['n'], 'blocks': [{'para': text + ' (Source: R01)'}]})
    if production_plan:
        receipts['R02'] = {'resolves_to': 'Objective, recipe and evidence-linked production plan ' + production_plan['plan_id']}
        blocks.append({'heading': 'Production plan', 'blocks': [{'para': production_plan['plan_id'] + ' · ' + production_plan['definition']['target_outcome']['task']}]})
        cal = production_plan['stages'].get('calibration') or {}
        if cal.get('quote'):
            q = cal['quote']; low, high = q['confidence_interval_gpu_hours']
            blocks.append({'heading': 'Calibrated compute quote', 'blocks': [{'para': f"{q['estimate_gpu_hours']:.3f} GPU-hours; {q['confidence']:.0%} interval {low:.3f}–{high:.3f}. {q['assumptions']} (Source: R02)"}]})
    content = {'content_id': content_id, 'version': 1, 'title': f"Training findings — {run['name']}", 'organisation': tenant,
        'receipts': receipts, 'facts': {}, 'series': {}, 'options': {}, 'calculations': {}, 'claims': claims, 'narrative_evidence': narrative,
        'coverage': {'covers': f"Retained model measurements and decisions from {run_id} only.", 'cannot_say': [
            {'gap': 'General cognition or performance outside the measured strata', 'reason': 'Not established by this run', 'closes_with': 'An independently designed evaluation'},
            {'gap': 'Independent final acceptance after further recipe selection', 'reason': 'These results have been inspected', 'closes_with': 'Fresh independently labelled and sealed final material'}]}}
    content['production_plan'] = production_plan
    if not production_plan:
        content['coverage']['cannot_say'].append({'gap': 'Complete objective-to-production lineage', 'reason': 'No new production plan is linked to this historical run', 'closes_with': 'An explicitly compiled and evidence-linked objective; never backdated assumptions'})
    # Put numeric record statements in the content layer, with their own exact
    # source values. Specs reference claims rather than repeating literal figures.
    numeric = re.compile(r'(?<![\w])[-+]?\d[\d,]*(?:\.\d+)?')
    for index, section in enumerate(blocks):
        for block_index, block in enumerate(section.get('blocks', [])):
            text = block.get('para')
            if not text or not numeric.search(text): continue
            key = f'C{500 + index * 10 + block_index:03}'
            supports = []
            receipt = 'R02' if 'R02' in text else 'R01'
            for match in numeric.finditer(text):
                literal = match.group().replace(',', '')
                fact = f'F{len(content["facts"]) + 2:03}'
                content['facts'][fact] = {'label': section['heading'] + ' · recorded value', 'value': float(literal) if '.' in literal else int(literal),
                    'unit': 'as recorded in the source statement', 'class': 'estimated' if receipt == 'R02' else 'measured', 'receipt': receipt,
                    'measurement_scope': 'Value observed in the retained receipt; a recorded floor or recipe setting is not measured model performance.',
                    'source_statement': text}
                supports.append(fact)
            claims[key] = {'text': text, 'supports': supports}
            block['para'] = '{' + key + '}'
    content['producer_revision'] = 3
    # Qualitative record statements cite the receipt directly, never an unrelated numeric fact.
    facts = content['facts']
    facts['F001'] = {'label': 'Measured checks on the record', 'value': len(run['checks']), 'unit': 'checks', 'class': 'measured', 'receipt': 'R01'}
    claims['C001'] = {'text': '{F001} checks were measured against the signed acceptance in this record.', 'supports': ['F001']}
    brief = {'brief_id': f'BR-{day}-{run_id}', 'content_ref': f'{content_id}@1',
        'purpose': {'kind': 'decide', 'statement': 'Decide the next model or dataset improvement from the recorded measurements and limitations.'},
        'audience': {'who': f'Model owner and reviewers · {tenant}', 'knowledge': 'familiar with the objective; mixed technical depth', 'priorities': ['per-stratum performance', 'coverage', 'privacy and next work'], 'detail': 'evidence with limitations'},
        'setting': {'mode': 'read-ahead', 'read_unattended': True, 'printed': True, 'ongoing_use': False},
        'content': {'evidence': True, 'narrative': True, 'financial': False, 'diagrams': False, 'imagery': False, 'appendix': True},
        'brand': {'house': 'house-neutral', 'formality': 'formal', 'expressiveness': 'restrained', 'variation_allowed': 'within-family'},
        'outputs': [{'format': 'docx', 'role': 'training findings and decision paper', 'editable_charts': False}, {'format': 'html', 'role': 'review surface', 'editable_charts': False}],
        'constraints': {'page_size': 'A4', 'confidentiality': 'Tenant confidential'}}
    frame = frame_for(brief)
    verdict = verdict_from_frame(frame, brief, f'V-{day}-{run_id}', manifest_from_brief(brief, False), principal, stamp)
    seed = f'{content_id}/decide/{day}'
    paper = {'spec_type': 'paper', 'spec_id': f'PP-{run_id}', 'content_ref': brief['content_ref'], 'brief_ref': brief['brief_id'], 'verdict_ref': verdict['verdict_id'],
        'objective': 'decide', 'family': frame['family'], 'voice': frame['voice'], 'seed': seed, 'build_stamp': stamp,
        'furniture': {'paper_id': run_id, 'confidentiality': 'Tenant confidential'}, 'title': content['title'], 'subtitle': 'Measurements, decisions and limits',
        'sections': blocks + [{'heading': 'Coverage and limits', 'blocks': [{'coverage_limits': True}]}, {'heading': 'Evidence references', 'blocks': [{'receipts': True}]}]}
    return {'commission_id': commission_id_for(tenant, content_id, 'decide', day), 'content_id': content_id, 'seed': seed, 'build_stamp': stamp,
        'frame_ref': frame['frame_id'], 'voice': frame['voice'], 'producer': 'training-whitepaper', 'source_ref': run_id, 'title': content['title'],
        'files': {'brief.json': brief, 'content.json': content, 'verdict.json': verdict, 'paper.json': paper}}