"""WPW Tier 2 technical report (Mα run) → existing document studio, deterministically. The nine WPW-8 sections are the paper's sections; the six acceptance
criteria and the per-figure receipt lines are evidence tables; every number in a paragraph is bound to a fact so the studio prints nothing it cannot source.
Internal only (WPW-10): confidentiality furniture says so and no public download is published."""
import re

from services.transform_forms.doc_studio.frames import frame_for, verdict_from_frame
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief
from services.transform_forms.doc_studio.producer_estate import commission_id_for

NUMERIC = re.compile(r'(?<![\w.])[-+]?\d[\d,]*(?:\.\d+)?(?![\w])')
DATEISH = re.compile(r'\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|\bv\d+\b|\d{4}-\d{2}-\d{2}T[\d:.]+Z?|`[^`]*`')
HEADINGS = {'problem_and_objective': 'Problem and objective', 'data_statement': 'Data statement', 'baseline_record': 'Baseline record', 'method': 'Method and adopted ideation events',
            'setup_and_reproducibility': 'Setup and reproducibility', 'results_on_held_out': 'Results on held-out material', 'ablations': 'Ablations', 'limitations': 'Limitations', 'negative_results': 'Negative results'}


def _plain(md):
    """Markdown → studio paragraphs and tables. Tables become rows_table exhibits; bullet lists stay as paragraphs; emphasis markers are dropped."""
    blocks, table = [], []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells): continue
            table.append(cells); continue
        if table: blocks.append(('table', table)); table = []
        if not s: continue
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s); s = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', s); s = re.sub(r'`', '', s)
        blocks.append(('para', s.lstrip('* ').strip()))
    if table: blocks.append(('table', table))
    return blocks


def commission_from_malpha_tier2(job_id, tenant, principal, now):
    from services.training_lab import malpha
    from services.wpw import tier2_malpha
    stored = tier2_malpha.get_report(job_id)
    report = stored['report'] if stored else tier2_malpha.draft(job_id)
    meta = report['metadata']; rec = malpha.job_detail(job_id); commission = malpha.commission(meta['commission_id']) or {}
    aip = next((j for j in malpha.jobs(phase='malpha_aip_build', host=rec['host'], status='completed')), None)
    day, stamp = now.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%dT%H:%M:%SZ')
    content_id = f'malpha-tier2-{job_id}'
    receipts = {'R01': {'resolves_to': f"Retained m9 job record and host receipt for {job_id} ({meta['lane']} iteration {meta['iteration']}, {meta['status']})", 'platform_ref': job_id},
                'R03': {'resolves_to': f"White Paper Wizard Tier 1 notebook for {meta['commission_id']} (append-only, hash-chained; entries referenced by id)"}}
    if aip: receipts['R02'] = {'resolves_to': f"AIP database build record {aip['job_id']} on {aip['host']} (segments, seals, codec qualification)", 'platform_ref': aip['job_id']}
    content = {'content_id': content_id, 'version': 1, 'title': f"Technical report (internal) — {commission.get('title', meta['commission_id'])} · {meta['lane']} v{meta['iteration']}", 'organisation': tenant,
               'receipts': receipts, 'facts': {}, 'series': {}, 'options': {}, 'calculations': {}, 'claims': {}, 'tables': {},
               'coverage': {'covers': f"The retained record of one Mα run only: {job_id}. Evidence classes are carried per figure; where the record is silent the report says so.",
                            'cannot_say': [{'gap': 'Admission of the model', 'reason': 'Dev results guide iteration; only the sealed-split evaluation decides admission' if rec['phase'] != 'malpha_evaluate' else 'This evaluation is one read of the sealed split; serving is a separate operation', 'closes_with': 'The independent evaluation run on the sealed admission split' if rec['phase'] != 'malpha_evaluate' else 'An owner decision to serve within scope'},
                                           {'gap': 'Native-speaker quality', 'reason': 'No human rating is on the record', 'closes_with': 'Native listeners judging unseen stories and transcripts'},
                                           {'gap': 'Monetary cost', 'reason': 'No governed GPU rate card; uncapped-until-billing authority', 'closes_with': 'Actual billing data joined to the measured GPU-hours'},
                                           {'gap': 'Publication', 'reason': 'Tier 2 is internal (WPW-10); Tier 3 eligibility is mechanical and its rulings are parked', 'closes_with': 'Owner rulings R1/R2 and a separate egress crossing'}]},
               'wpw': {'tier': 2, 'internal_only': True, 'settlement': meta['settlement'], 'refusal_reason': meta.get('refusal_reason'), 'figures_resolved': meta['figures_resolved'], 'figures_total': meta['figures_total']}}
    facts, claims, tables = content['facts'], content['claims'], content['tables']
    facts['F001'] = {'label': 'Figures that resolve to a retained record', 'value': meta['figures_resolved'], 'unit': 'figures', 'class': 'measured', 'receipt': 'R01'}
    facts['F002'] = {'label': 'Figures in the report (resolved and refused)', 'value': meta['figures_total'], 'unit': 'figures', 'class': 'measured', 'receipt': 'R01'}
    claims['C001'] = {'text': '{F001} of {F002} figures in this report resolve to a retained record; the rest are listed as refused and do not render as numbers (WPW-9).', 'supports': ['F001', 'F002']}
    sections = [{'heading': 'Settlement', 'blocks': [{'para': '{C001}'}, {'para': '{C002}'}]}]
    settle_text = f"Settlement: {meta['settlement']}" + (f" — {meta['refusal_reason']}" if meta.get('refusal_reason') else '') + f". Run status {meta['status']}; drafted automatically when the run settled (WPW-8). Internal — must not cross the outer gate (WPW-10)."
    claims['C002'] = {'text': settle_text, 'supports': ['F001']}

    def bind(text, receipt):
        """A paragraph with numbers becomes a claim whose literal figures are facts with their own source receipt; dates, versions and code spans are not figures."""
        key = f'C{len(claims) + 1:03}'
        scrubbed = DATEISH.sub(' ', text); supports = []
        for m in NUMERIC.finditer(scrubbed):
            literal = m.group().replace(',', '')
            try: value = float(literal) if '.' in literal else int(literal)
            except ValueError: continue
            fid = f'F{len(facts) + 1:03}'
            facts[fid] = {'label': 'Recorded value in the report statement', 'value': value, 'unit': 'as recorded', 'class': 'measured', 'receipt': receipt, 'source_statement': text[:300]}
            supports.append(fid)
        claims[key] = {'text': text, 'supports': supports or ['F001']}
        return '{' + key + '}'

    for name in ('problem_and_objective', 'data_statement', 'baseline_record', 'method', 'setup_and_reproducibility', 'results_on_held_out', 'ablations', 'limitations', 'negative_results'):
        receipt = 'R02' if name == 'data_statement' and 'R02' in receipts else 'R01'
        blocks = []
        for kind, payload in _plain(report['sections'][name]['body']):
            if kind == 'para': blocks.append({'para': bind(payload, receipt)})
            else:
                tid = f'T{len(tables) + 1:03}'; header, rows = payload[0], payload[1:]
                tables[tid] = {'label': f'{HEADINGS[name]} — table', 'class': 'measured', 'receipt': receipt, 'right_align_from': len(header), 'columns': header, 'rows': [r + [''] * (len(header) - len(r)) for r in rows],
                               'note': 'Values as recorded on the retained run record; a dash means the record is silent.'}
                blocks.append({'rows_table': {'table_ref': tid}})
        sections.append({'heading': HEADINGS[name], 'blocks': blocks})
    tid = f'T{len(tables) + 1:03}'
    tables[tid] = {'label': 'Six acceptance criteria — measured value, adopted threshold, pass', 'class': 'measured', 'receipt': 'R01', 'right_align_from': 5,
                   'columns': ['Criterion', 'Measured', 'Threshold', 'Pass', 'Evidence class'], 'note': 'Every criterion of the fixed set is named; a criterion the run did not instrument says so instead of carrying a filled value.',
                   'rows': [[c['name'], c['measured'], c['threshold'], 'pass' if c['pass'] is True else 'fail' if c['pass'] is False else 'reported, not gated', c['class'] or 'not instrumented'] for c in report['criteria']]}
    sections.append({'heading': 'Acceptance criteria', 'blocks': [{'rows_table': {'table_ref': tid}}]})
    tid = f'T{len(tables) + 1:03}'
    tables[tid] = {'label': 'Figure register — evidence class and receipt line of every rendered figure', 'class': 'measured', 'receipt': 'R01', 'right_align_from': 4, 'columns': ['Figure', 'Evidence class', 'Receipt line', 'Summary'],
                   'rows': [[f['figure_id'], f['evidence_class'], f['receipt_line'], f['summary_text'][:160]] for f in report['figures']], 'note': 'Each receipt line resolves into the retained record it names; resolution is checked mechanically before the figure renders.'}
    sections.append({'heading': 'Figure register', 'blocks': [{'rows_table': {'table_ref': tid}}]})
    if report['refused_figures']:
        tid = f'T{len(tables) + 1:03}'
        tables[tid] = {'label': 'Refused figures — receipt lines that did not resolve', 'class': 'measured', 'receipt': 'R01', 'right_align_from': 3, 'columns': ['Figure', 'Receipt line', 'Reason'], 'rows': [[f['figure_id'], f['receipt_line'], f['reason']] for f in report['refused_figures']],
                       'note': 'A figure that does not resolve does not render (WPW-9); the section it belonged to says the record is silent.'}
        sections.append({'heading': 'Refused figures', 'blocks': [{'rows_table': {'table_ref': tid}}]})
    sections += [{'heading': 'Coverage and limits', 'blocks': [{'coverage_limits': True}]}, {'heading': 'Evidence references', 'blocks': [{'receipts': True}]}]
    brief = {'brief_id': f'BR-{day}-{job_id}', 'content_ref': f'{content_id}@1',
             'purpose': {'kind': 'decide', 'statement': 'Decide the next qualified change for this lane from what the settled run measured against its fixed acceptance; every figure traceable to the run record.'},
             'audience': {'who': f'Model owner, reviewers and the research record · {tenant}', 'knowledge': 'familiar with the commission; technical', 'priorities': ['per-language results', 'traceability', 'limitations and negative results'], 'detail': 'evidence with limitations'},
             'setting': {'mode': 'read-ahead', 'read_unattended': True, 'printed': True, 'ongoing_use': True},
             'content': {'evidence': True, 'narrative': True, 'financial': False, 'diagrams': False, 'imagery': False, 'appendix': True},
             'brand': {'house': 'house-neutral', 'formality': 'formal', 'expressiveness': 'restrained', 'variation_allowed': 'within-family'},
             'outputs': [{'format': 'docx', 'role': 'internal technical report', 'editable_charts': False}, {'format': 'html', 'role': 'review surface', 'editable_charts': False}],
             'constraints': {'page_size': 'A4', 'confidentiality': 'Internal — White Paper Wizard technical report; must not cross the outer gate'}}
    frame = frame_for(brief)
    verdict = verdict_from_frame(frame, brief, f'V-{day}-{job_id}', manifest_from_brief(brief, False), principal, stamp)
    seed = f'{content_id}/decide/{day}'
    paper = {'spec_type': 'paper', 'spec_id': f'PP-{job_id}', 'content_ref': brief['content_ref'], 'brief_ref': brief['brief_id'], 'verdict_ref': verdict['verdict_id'], 'objective': 'decide', 'family': frame['family'], 'voice': frame['voice'],
             'seed': seed, 'build_stamp': stamp, 'furniture': {'paper_id': job_id, 'confidentiality': 'Internal — must not cross the outer gate'}, 'title': content['title'],
             'subtitle': 'White Paper Wizard technical report · settled automatically · internal', 'sections': sections}
    return {'commission_id': commission_id_for(tenant, content_id, 'decide', day), 'content_id': content_id, 'seed': seed, 'build_stamp': stamp, 'frame_ref': frame['frame_id'], 'voice': frame['voice'], 'producer': 'malpha-tier2',
            'source_ref': job_id, 'title': content['title'], 'files': {'brief.json': brief, 'content.json': content, 'verdict.json': verdict, 'paper.json': paper}}
