"""Planner → Worker → Document Content Manager → Frontier writer.

Deterministic code PLANS the document from the evidence that exists, the producers (workers) ASSEMBLE every fact with its receipt, the
Content Manager GATES the draft (every figure by reference, every reference resolvable, every slot filled, house limits met) and the frontier
model WRITES every sentence the reader sees. Code never types a sentence onto the page; the model never types a number."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Tuple

PURPOSE = 'doc_studio.author'
PLAN_PURPOSE = 'doc_studio.plan'
GLOSSARY_PER_SLIDE, TABLE_ROWS_PER_SLIDE, TABLE_COLUMNS_PER_SLIDE, TABLE_PAGES_PER_DECK = 6, 9, 7, 2
TOKEN = re.compile(r'\{([A-Za-z]\w*(?:\.[A-Za-z_]\w*)?(?::[A-Za-z_]\w*)*)\}')
DIGITS = re.compile(r'(?<![A-Za-z{\w])\d[\d,]*\.?\d*')
URL = re.compile(r'https?://|www\.', re.I)
MAX_REPAIRS = 2

SYSTEM = ('You are the frontier writer in Akki\'s document studio: a seasoned strategy-house author writing for an estate owner who will act on what you write. '
          'British English. Findings, not directives, in titles; concrete, prioritised recommendations in the actions slot. Plain, numerate, specific, no marketing, '
          'no headings or markdown inside strings, no bullet symbols. Every figure you use MUST be written as a reference token exactly as supplied — {F004}, {K001}, '
          '{O1.monthly_saving_usd}, {F006:F007:ratio} — never as digits; the only digits allowed are four-digit years. Say what the evidence shows, what it means for '
          'the owner, what to do first and why, and what cannot be said yet. Never invent a figure, a price, a right or a cause the evidence does not carry. '
          'Return ONLY the JSON object requested; no prose around it; never use unescaped double quotes inside JSON strings (prefer no quotation marks at all).')


# ----------------------------------------------------------------------------- Planner
def plan(content: Dict[str, Any], brief: Dict[str, Any]) -> Dict[str, Any]:
    """The story the document must tell, slot by slot. A producer that knows its story declares it as ordered chapters (the question each
    chapter answers, the evidence that answers it, the exhibit that shows it); the planner turns that into the outline the writer fills.
    Without a declared story the outline falls back to one section per evidence receipt."""
    facts, series, options, tables = content.get('facts') or {}, content.get('series') or {}, content.get('options') or {}, content.get('tables') or {}
    fact_ids = sorted(facts)
    story = content.get('story') or []
    slots: List[Dict[str, Any]] = [{'slot': 'exec', 'type': 'exec_summary', 'needs': fact_ids[:8]}]
    for page, start in enumerate(range(0, len(content.get('glossary') or []), GLOSSARY_PER_SLIDE), 1):
        slots.append({'slot': f'glossary{page}', 'type': 'glossary', 'rows_from': start, 'rows_to': start + GLOSSARY_PER_SLIDE})
    if story:
        for number, chapter in enumerate(story, 1):
            slots.append({'slot': f'section{number}', 'type': 'section', 'number': number, 'about': chapter['question'][:160], 'question': chapter['question']})
            needs = [t for t in chapter.get('answers_with') or [] if t in facts or t in options or t in (content.get('calculations') or {}) or t in (content.get('claims') or {})]
            for sid in [s for s in chapter.get('exhibits') or [] if s in series][:2]:
                slots.append({'slot': f'exhibit_{sid}', 'type': 'assertion_exhibit', 'series_ref': sid, 'y_format': 'pct' if series[sid].get('unit') == 'pct' else 'num', 'needs': [sid] + needs[:4], 'about': series[sid]['label'], 'question': chapter['question']})
            if chapter.get('kind') == 'comparison' and len(options) == 3:
                slots.append({'slot': 'compare', 'type': 'comparison', 'columns': sorted(options), 'needs': sorted(options), 'question': chapter['question']})
            else:
                slots.append({'slot': f'chapter{number}', 'type': 'assertion_points', 'about': chapter['question'], 'needs': needs[:6], 'question': chapter['question'], 'must_cite': needs[:3],
                              'tables': [t for t in chapter.get('tables') or [] if t in tables]})
            for tid in [t for t in chapter.get('tables') or [] if t in tables]:
                # Evidence tables are deterministic: the deck shows up to two pages of the rows the owner asked to see by name, the paper and workbook carry every row.
                columns = tables[tid].get('deck_columns') or list(tables[tid]['columns'])[:TABLE_COLUMNS_PER_SLIDE]
                for page, start in enumerate(range(0, min(len(tables[tid]['rows']), TABLE_ROWS_PER_SLIDE * TABLE_PAGES_PER_DECK), TABLE_ROWS_PER_SLIDE), 1):
                    slots.append({'slot': f'table_{tid}_{page}', 'type': 'table', 'table_ref': tid, 'rows_from': start, 'rows_to': start + TABLE_ROWS_PER_SLIDE, 'columns': columns, 'about': tables[tid]['label'], 'question': chapter['question']})
        slots.append({'slot': 'actions', 'type': 'assertion_points', 'about': 'what the owner should do first, in order, and why — each action tied to the chapter evidence it rests on', 'needs': fact_ids[:6]})
        slots.append({'slot': 'risks', 'type': 'assertion_points', 'about': 'what the evidence cannot yet establish and what would close each gap', 'needs': fact_ids[:4]})
    else:
        slots += _outline_by_receipt(content, fact_ids)
    paper = ['summary'] + [s['slot'] for s in slots if s['type'] in ('assertion_exhibit', 'assertion_points', 'comparison')]
    return {'story': [{'chapter': i + 1, 'question': c['question']} for i, c in enumerate(story)], 'slots': slots, 'paper_sections': paper,
            'limits': {'title_max_chars': 95, 'points_max': 5, 'words_per_slide_max': 90, 'paragraphs_per_section': (1, 3), 'paragraph_max_words': 110},
            'tokens': {'facts': fact_ids, 'series': sorted(series), 'options': sorted(options), 'calculations': sorted(content.get('calculations') or {})}}


def _outline_by_receipt(content: Dict[str, Any], fact_ids: List[str]) -> List[Dict[str, Any]]:
    facts, series, options, receipts = content.get('facts') or {}, content.get('series') or {}, content.get('options') or {}, content.get('receipts') or {}
    by_receipt: Dict[str, Dict[str, List[str]]] = {}
    for sid in sorted(series): by_receipt.setdefault(series[sid]['receipt'], {'series': [], 'facts': []})['series'].append(sid)
    for fid in fact_ids: by_receipt.setdefault(facts[fid]['receipt'], {'series': [], 'facts': []})['facts'].append(fid)
    slots: List[Dict[str, Any]] = []
    number, leftovers = 0, []
    for rid in sorted(by_receipt):
        group = by_receipt[rid]
        if not group['series'] and len(group['facts']) < 3:
            leftovers += group['facts']; continue
        number += 1
        slots.append({'slot': f'section{number}', 'type': 'section', 'number': number, 'about': (receipts.get(rid) or {}).get('resolves_to', rid)[:160], 'receipt': rid})
        for sid in group['series'][:3]:
            slots.append({'slot': f'exhibit_{sid}', 'type': 'assertion_exhibit', 'series_ref': sid, 'y_format': 'pct' if series[sid].get('unit') == 'pct' else 'num', 'needs': [sid], 'about': series[sid]['label']})
        for index, chunk in enumerate([group['facts'][i:i + 5] for i in range(0, len(group['facts']), 5)][:2], 1):
            slots.append({'slot': f'findings_{rid}_{index}', 'type': 'assertion_points', 'about': ' · '.join(facts[f]['label'] for f in chunk), 'needs': chunk, 'receipt': rid})
        if number >= 6: break
    if leftovers:
        slots.append({'slot': 'findings_other', 'type': 'assertion_points', 'about': ' · '.join(facts[f]['label'] for f in leftovers[:5]), 'needs': leftovers[:5]})
    if len(options) == 3:
        slots.append({'slot': 'compare', 'type': 'comparison', 'columns': sorted(options), 'needs': sorted(options)})
    slots.append({'slot': 'actions', 'type': 'assertion_points', 'about': 'what the owner should do first, in order, and why', 'needs': fact_ids[:6]})
    slots.append({'slot': 'risks', 'type': 'assertion_points', 'about': 'risks, obligations and what cannot yet be said', 'needs': fact_ids[:4]})
    return slots


# ----------------------------------------------------------------------------- Worker view of the evidence the writer may use
def _fmt(value, unit):
    """Exactly what the studio prints for a token (mirrors scripts/studio.fmt_value); the writer adds unit words only where none is printed."""
    if unit == 'GBPm': return f'£{value:,.1f}m'
    if unit == 'GBP': return f'£{value:,.2f}'
    if unit == 'pct': return f'{value * 100:.1f}%'
    if unit == 'pp': return f'{value * 100:.1f}pp'
    if unit == 'm': return f'{value:,.1f}m'
    if unit == 'FTE': return f'{int(round(value)):,}'
    if unit == 'months': return f'{value:g}'
    if unit == 'years': return f'{value:.1f}'
    if isinstance(value, float): return f'{value:,.1f}'
    return f'{value:,}' if isinstance(value, int) else f'{value}'


def evidence(content: Dict[str, Any]) -> Dict[str, Any]:
    facts = {fid: {'label': f['label'], 'renders_as': _fmt(f['value'], f['unit']), 'unit': f['unit'], 'class': f['class'], 'receipt': f['receipt'], **({'scope': f['measurement_scope']} if f.get('measurement_scope') else {})} for fid, f in (content.get('facts') or {}).items()}
    series = {sid: {'label': s['label'], 'categories': s['categories'], 'values': s['values'], 'unit': s['unit'], 'class': s['class']} for sid, s in (content.get('series') or {}).items()}
    options = {oid: {k: v for k, v in o.items() if k not in ('receipt',)} for oid, o in (content.get('options') or {}).items()}
    calcs = {kid: {'label': k['label'], 'formula': k['formula'], 'unit': k.get('unit')} for kid, k in (content.get('calculations') or {}).items()}
    tables = {tid: {'label': t['label'], 'columns': t['columns'], 'rows': len(t['rows']), 'what_it_shows': t.get('note', ''), 'rendered': 'deterministic table beside its chapter; row values are not in this prompt'} for tid, t in (content.get('tables') or {}).items()}
    return {'title': content['title'], 'organisation': content['organisation'], 'facts': facts, 'series': series, 'options': options, 'calculations': calcs, 'tables': tables,
            'glossary': [{'term': g['term'], 'meaning': g['meaning']} for g in content.get('glossary') or []],
            'receipts': {rid: r['resolves_to'] for rid, r in (content.get('receipts') or {}).items()}, 'coverage': content.get('coverage'),
            'evidence_statements': {k: v['text'] for k, v in (content.get('narrative_evidence') or {}).items()},
            'producer_claims_for_context': {k: v['text'] for k, v in (content.get('claims') or {}).items()},
            'production_plan': content.get('production_plan')}


# ----------------------------------------------------------------------------- Frontier writer
def _schema_hint(plan_: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {'title': 'string ≤ 60 chars', 'subtitle': 'string ≤ 90 chars', 'slots': {}, 'paper': {'summary': ['1-3 paragraphs'], 'sections': {}}}
    for s in plan_['slots']:
        if s['type'] == 'exec_summary': out['slots'][s['slot']] = {'kicker': 'str', 'title': 'assertion ≤ 95 chars', 'situation': 'str', 'complication': 'str', 'question': 'str', 'answer': 'str'}
        elif s['type'] == 'section': out['slots'][s['slot']] = {'title': 'short section title ≤ 60 chars'}
        elif s['type'] == 'assertion_exhibit': out['slots'][s['slot']] = {'kicker': 'str', 'title': 'assertion the exhibit proves ≤ 95 chars', 'so_what': 'one sentence ≤ 30 words'}
        elif s['type'] == 'assertion_points': out['slots'][s['slot']] = {'kicker': 'str', 'title': 'assertion ≤ 95 chars', 'points': ['3-5 points, each ≤ 28 words']}
        elif s['type'] == 'comparison': out['slots'][s['slot']] = {'kicker': 'str', 'title': 'assertion ≤ 95 chars, no winner marked', 'so_what': 'one sentence ≤ 30 words'}
        if s['type'] in ('assertion_exhibit', 'assertion_points', 'comparison'): out['paper']['sections'][s['slot']] = {'heading': 'str ≤ 70 chars', 'paragraphs': ['1-3 paragraphs ≤ 110 words each']}
    return out


async def write(content: Dict[str, Any], brief: Dict[str, Any], plan_: Dict[str, Any], tenant: str, actor: str, session: str, issues: List[str] | None = None, previous: Dict[str, Any] | None = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve
    writer = resolve('writer')
    prompt = {'brief': {k: brief.get(k) for k in ('purpose', 'audience', 'setting', 'constraints')}, 'evidence': evidence(content), 'plan': plan_, 'return_exactly': _schema_hint(plan_),
              'rules': ['every figure as a supplied token; digits only for four-digit years', 'use only tokens that exist in evidence',
                        'renders_as is exactly what the reader sees for a token (percentages carry %, money carries its symbol, m means million); add a unit word only where renders_as shows none, e.g. "{F004} GiB", "{F001} databases"',
                        'one assertion per title; titles ≤ 95 characters; the document title ≤ 60 characters',
                        'plan.story is the story to tell, in order: each chapter slot must answer its question directly, lead with the answer, and cite the chapter evidence (must_cite) — an owner reading only the titles must get the whole story',
                        'brief.constraints.owner_declarations are facts the owner has stated; honour them, never contradict them, and never condition a recommendation on something the owner has already declared settled',
                        'actions: ordered, concrete, owner-level, each tied to the evidence token it rests on', 'risks: what the evidence cannot establish and what would close the gap, drawn from coverage.cannot_say',
                        'evidence.tables are rendered beside their chapters with the exact bucket, table, share, station and language names; refer the reader to them by label (for example: the table of buckets under review) rather than naming locations yourself',
                        'evidence.glossary is printed in the pack; use its terms in their plain-English sense and never redefine them',
                        'plan.planner_notes, when present, are the orchestrator\'s directions on emphasis and order within each chapter; follow them unless they conflict with the evidence',
                        'no markdown, no bullets, no URLs, no "Source:"']}
    if issues:
        prompt['repair'] = {'your_previous_draft': previous, 'content_manager_rejections': issues, 'instruction': 'Fix every rejection and return the full corrected JSON.'}
    response = await invoke(purpose=PURPOSE, prompt=json.dumps(prompt, default=str), masking_tier='llm_prompt_governed_text', actor=actor,
                            model=writer['model'], provider=writer['connection'], tenant_id=tenant, custody_class='tenant_estate',
                            system_message=SYSTEM, session_id=session)
    raw = response.text.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    meta = {'model': response.model_id, 'provider': response.provider, 'receipt_id': response.receipt_id, 'tokens_in': response.tokens_in, 'tokens_out': response.tokens_out, 'latency_ms': response.latency_ms}
    try:
        draft = json.loads(raw[start:end + 1])
    except ValueError as exc:
        draft = _lenient_json(raw[start:end + 1]) or {'_invalid_json': f'{exc}', '_raw_excerpt': raw[max(0, getattr(exc, "pos", 0) - 160):getattr(exc, "pos", 0) + 160]}
        if '_invalid_json' not in draft: meta['json_repaired'] = str(exc)[:120]
    return draft, meta


def _lenient_json(text: str) -> Dict[str, Any] | None:
    """A stray unescaped quote inside one of fifty prose strings must not cost a whole authoring pass; the content manager still gates every token."""
    try:
        from json_repair import repair_json
        parsed = repair_json(text, return_objects=True)
    except Exception:  # noqa: BLE001
        return None
    return parsed if isinstance(parsed, dict) and parsed else None


# ----------------------------------------------------------------------------- Document Content Manager (gate; never rewrites)
def _strings(obj, path='draft'):
    if isinstance(obj, dict):
        for k, v in obj.items(): yield from _strings(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj): yield from _strings(v, f'{path}[{i}]')
    elif isinstance(obj, str): yield path, obj


def _resolvable(token: str, content: Dict[str, Any]) -> bool:
    head = token.split(':')[0]
    if head.startswith('content.'): return head.split('.', 1)[1] in content
    if '.' in head:
        oid, field = head.split('.', 1)
        return oid in (content.get('options') or {}) and field in content['options'][oid]
    pools = (content.get('facts') or {}), (content.get('series') or {}), (content.get('options') or {}), (content.get('calculations') or {}), (content.get('claims') or {})
    if ':' in token and token.count(':') == 2:
        a, b, _ = token.split(':'); return a in pools[0] and b in pools[0]
    return any(head in pool for pool in pools)


def manage(draft: Dict[str, Any], content: Dict[str, Any], plan_: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if isinstance(draft, dict) and draft.get('_invalid_json'):
        return [f"response was not valid JSON ({draft['_invalid_json']}); near: {draft.get('_raw_excerpt', '')!r}. Escape or avoid double quotes inside strings and return one complete JSON object"]
    if not isinstance(draft, dict) or not isinstance(draft.get('slots'), dict) or not isinstance(draft.get('paper'), dict):
        return ['draft is not an object with "slots" and "paper"']
    limits = plan_['limits']
    for path, text in _strings(draft):
        stripped = TOKEN.sub('', text)
        for m in DIGITS.finditer(stripped):
            if re.fullmatch(r'(19|20)\d\d', m.group()) or (m.group().isdigit() and int(m.group()) <= 12): continue
            issues.append(f'{path}: literal figure "{m.group()}" must be a reference token')
        for tok in TOKEN.findall(text):
            if not _resolvable(tok, content): issues.append(f'{path}: token {{{tok}}} does not exist in the content model')
        if URL.search(text): issues.append(f'{path}: URLs are not permitted')
        if re.search(r'\*\*|^#|\n#|^- |\n- |•', text): issues.append(f'{path}: markdown or bullet symbols are not permitted')
        if 'source:' in text.lower(): issues.append(f'{path}: "Source:" strings are not permitted; receipts are printed by the studio')
    for s in plan_['slots']:
        got = draft['slots'].get(s['slot'])
        if s['type'] in ('coverage_limits', 'appendix', 'table', 'glossary'): continue
        if not isinstance(got, dict): issues.append(f'slot {s["slot"]} missing'); continue
        title = got.get('title', '')
        if s['type'] != 'section' and (not title or len(title) > limits['title_max_chars']): issues.append(f'slot {s["slot"]}: title missing or over {limits["title_max_chars"]} characters')
        if s['type'] == 'section' and not title: issues.append(f'slot {s["slot"]}: section title missing')
        if s['type'] == 'exec_summary' and any(not got.get(k) for k in ('situation', 'complication', 'question', 'answer')): issues.append('slot exec: situation/complication/question/answer all required')
        if s['type'] in ('assertion_exhibit', 'comparison') and not got.get('so_what'): issues.append(f'slot {s["slot"]}: so_what required')
        if s['type'] == 'assertion_points':
            points = got.get('points')
            if not isinstance(points, list) or not 3 <= len(points) <= limits['points_max'] or any(not isinstance(p, str) or not p.strip() for p in points): issues.append(f'slot {s["slot"]}: 3 to {limits["points_max"]} non-empty points required')
            elif any(len(p.split()) > 32 for p in points): issues.append(f'slot {s["slot"]}: a point exceeds 32 words')
        if s['type'] in ('assertion_points', 'comparison', 'assertion_exhibit'):
            words = sum(len(str(v).split()) for k, v in got.items() if k in ('title', 'points', 'so_what'))
            if words > limits['words_per_slide_max'] + 20: issues.append(f'slot {s["slot"]}: too dense ({words} words)')
        needs = [n for n in s.get('needs', []) if n in (content.get('facts') or {}) or n in (content.get('options') or {})]
        if s['type'] in ('assertion_points', 'exec_summary') and needs and not any(TOKEN.search(str(v)) for v in got.values()):
            issues.append(f'slot {s["slot"]}: no evidence token used; cite at least one of {", ".join(needs[:4])}')
        must = s.get('must_cite') or []
        if must and not any(('{' + m) in str(v) for m in must for v in got.values()):
            issues.append(f'slot {s["slot"]}: must answer "{s.get("question", "")[:80]}" with its own evidence; cite at least one of {", ".join(must)}')
    paper = draft['paper']
    summary = paper.get('summary')
    if not isinstance(summary, list) or not 1 <= len(summary) <= 3 or any(not isinstance(p, str) or not p.strip() for p in summary): issues.append('paper.summary: 1-3 paragraphs required')
    for key in plan_['paper_sections'][1:]:
        sec = (paper.get('sections') or {}).get(key)
        if not isinstance(sec, dict) or not sec.get('heading') or not isinstance(sec.get('paragraphs'), list) or not sec['paragraphs']: issues.append(f'paper.sections.{key}: heading and paragraphs required'); continue
        lo, hi = limits['paragraphs_per_section']
        if not lo <= len(sec['paragraphs']) <= hi: issues.append(f'paper.sections.{key}: {lo}-{hi} paragraphs required')
        if any(len(p.split()) > limits['paragraph_max_words'] + 15 for p in sec['paragraphs']): issues.append(f'paper.sections.{key}: a paragraph exceeds {limits["paragraph_max_words"]} words')
    if not draft.get('title') or len(draft['title']) > 60: issues.append('title missing or over 60 characters (it must fit the cover title box)')
    if draft.get('subtitle') and len(draft['subtitle']) > 90: issues.append('subtitle over 90 characters')
    return issues


# ----------------------------------------------------------------------------- bind the gated draft into the content model and specs
def _supports(text: str, content: Dict[str, Any], fallback: str) -> List[str]:
    ids = []
    for tok in TOKEN.findall(text):
        head = tok.split(':')[0].split('.')[0]
        for part in ([head] + (tok.split(':')[:2] if tok.count(':') == 2 else [])):
            if part in (content.get('facts') or {}) or part in (content.get('series') or {}) or part in (content.get('options') or {}) or part in (content.get('calculations') or {}):
                if part not in ids: ids.append(part)
    return ids or [fallback]


def apply(files: Dict[str, Any], draft: Dict[str, Any], plan_: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    content, brief, verdict = files['content.json'], files['brief.json'], files['verdict.json']
    fallback = sorted(content['facts'])[0] if content.get('facts') else sorted(content['receipts'])[0]
    claims = content.setdefault('claims', {})
    authored = 0
    counter = [900]
    def claim(text: str) -> str:
        nonlocal authored
        counter[0] += 1; cid = f'C{counter[0]}'
        claims[cid] = {'text': text, 'supports': _supports(text, content, fallback), 'authored': True}
        authored += 1
        return '{' + cid + '}'
    content['title'] = draft['title']
    spec_template = next(v for k, v in files.items() if k not in ('brief.json', 'content.json', 'verdict.json'))
    common = {k: spec_template[k] for k in ('content_ref', 'brief_ref', 'verdict_ref', 'objective', 'family', 'voice', 'seed', 'build_stamp')}
    slides: List[Dict[str, Any]] = [{'type': 'cover', 'title': '{content.title}', 'subtitle': claim(draft.get('subtitle') or 'Authored from the measured record'), 'org': '{content.organisation}'}]
    paper_sections: List[Dict[str, Any]] = [{'heading': 'Summary', 'blocks': [{'para': claim(p)} for p in draft['paper']['summary']]}]
    for s in plan_['slots']:
        got = draft['slots'].get(s['slot']) or {}
        if s['type'] == 'exec_summary':
            slides.append({'type': 'exec_summary', 'kicker': got.get('kicker') or 'Executive summary', 'title': claim(got['title']), 'situation': claim(got['situation']), 'complication': claim(got['complication']), 'question': claim(got['question']), 'answer': claim(got['answer'])})
        elif s['type'] == 'section':
            slides.append({'type': 'section', 'number': s['number'], 'title': claim(got['title'])})
        elif s['type'] == 'assertion_exhibit':
            slides.append({'type': 'assertion_exhibit', 'kicker': got.get('kicker') or 'Evidence', 'title': claim(got['title']), 'exhibit': {'plate': 'bar', 'series_ref': s['series_ref'], 'y_format': s['y_format'], 'so_what': claim(got['so_what'])}})
        elif s['type'] == 'assertion_points':
            slides.append({'type': 'assertion_points', 'kicker': got.get('kicker') or 'Findings', 'title': claim(got['title']), 'points': [claim(p) for p in got['points']]})
        elif s['type'] == 'comparison':
            fields = [k for k in content['options'][s['columns'][0]] if isinstance(content['options'][s['columns'][0]][k], (int, float)) and k not in ('class',)][:3]
            slides.append({'type': 'comparison', 'kicker': got.get('kicker') or 'Options', 'title': claim(got['title']), 'columns': s['columns'],
                           'rows': [{'label': f.replace('_', ' ').capitalize(), 'field': f, 'format': 'num1'} for f in fields], 'so_what': claim(got['so_what'])})
        elif s['type'] == 'glossary':
            slides.append({'type': 'glossary', 'kicker': 'Plain English', 'rows_from': s['rows_from'], 'rows_to': s['rows_to']})
            if s['rows_from'] == 0:
                paper_sections.append({'heading': 'Plain English: the terms used in this pack', 'blocks': [{'glossary': {}}]})
        elif s['type'] == 'table':
            slides.append({'type': 'table', 'kicker': 'Evidence by name', 'table_ref': s['table_ref'], 'rows_from': s['rows_from'], 'rows_to': s['rows_to'], 'columns': s['columns']})
            continue
        sec = (draft['paper'].get('sections') or {}).get(s['slot'])
        if sec:
            blocks: List[Dict[str, Any]] = [{'para': claim(p)} for p in sec['paragraphs']]
            if s['type'] == 'assertion_exhibit': blocks.append({'figure': {'plate': 'bar', 'series_ref': s['series_ref'], 'y_format': s['y_format'], 'caption': claim(got['so_what'])}})
            if s['type'] == 'comparison': blocks.append({'options_table': {'columns': s['columns'], 'rows': slides[-1]['rows'], 'caption': claim(got['so_what'])}})
            for tid in s.get('tables') or []:
                blocks.append({'rows_table': {'table_ref': tid}})  # every row, every column: the paper is the complete record
            paper_sections.append({'heading': sec['heading'], 'blocks': blocks})
    slides += [{'type': 'coverage_limits'}, {'type': 'appendix'}]
    paper_sections += [{'heading': 'Coverage and limits', 'blocks': [{'coverage_limits': True}]}, {'heading': 'Appendix: receipts', 'blocks': [{'receipts': True}]}]
    outputs = {o['format'] for o in brief['outputs']}
    files = {k: v for k, v in files.items() if k in ('brief.json', 'content.json', 'verdict.json', 'workbook.json')}
    if 'pptx' in outputs:
        files['deck.json'] = {**common, 'spec_type': 'deck', 'spec_id': spec_template['spec_id'].replace('PP-', 'DK-') if spec_template['spec_id'].startswith('PP-') else spec_template['spec_id'], 'furniture': {'deck_id': spec_template.get('furniture', {}).get('deck_id') or spec_template.get('furniture', {}).get('paper_id') or 'deck', 'confidentiality': spec_template.get('furniture', {}).get('confidentiality', 'Tenant confidential')}, 'slides': slides}
    if 'docx' in outputs or 'html' in outputs:
        files['paper.json'] = {**common, 'spec_type': 'paper', 'spec_id': spec_template['spec_id'].replace('DK-', 'PP-') if spec_template['spec_id'].startswith('DK-') else spec_template['spec_id'], 'furniture': {'paper_id': spec_template.get('furniture', {}).get('paper_id') or spec_template.get('furniture', {}).get('deck_id') or 'paper', 'confidentiality': spec_template.get('furniture', {}).get('confidentiality', 'Tenant confidential')},
                               'title': '{content.title}', 'subtitle': slides[0]['subtitle'], 'sections': paper_sections}
    content['authoring'] = {**meta, 'pipeline': 'orchestrating planner → worker → content manager → frontier writer → independent reviewer', 'claims_authored': authored}
    return files


# ----------------------------------------------------------------------------- Orchestrating planner (LLM-shaped; the planner family, distinct from the reviewer)
PLAN_SYSTEM = ('You are the planning orchestrator in Akki\'s document studio. You receive the evidence model (facts, series, tables by label, glossary, coverage) and the '
               'deterministic chapter outline. You do not change the outline, the figures or the evidence. You direct the writer: for each chapter say in one or two sentences '
               'what it must lead with, which evidence tokens carry the answer, what the executive must take away, and what must not be overstated. '
               'Return ONLY JSON: {"title_direction": "one sentence", "chapter_notes": {"<slot>": "note"}, "cautions": ["..."]}. No markdown. Never type a figure; cite tokens such as {F060}.')


async def plan_notes(content: Dict[str, Any], brief: Dict[str, Any], plan_: Dict[str, Any], tenant: str, actor: str, session: str) -> Dict[str, Any]:
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve
    planner = resolve('planner')
    chapters = [{'slot': s['slot'], 'question': s.get('question'), 'needs': s.get('needs'), 'must_cite': s.get('must_cite'), 'tables': s.get('tables')} for s in plan_['slots'] if s['type'] in ('assertion_points', 'comparison', 'assertion_exhibit')]
    prompt = {'brief': {k: brief.get(k) for k in ('purpose', 'audience', 'constraints')}, 'evidence': evidence(content), 'outline': chapters, 'story': plan_['story']}
    response = await invoke(purpose=PLAN_PURPOSE, prompt=json.dumps(prompt, default=str), masking_tier='llm_prompt_governed_text', actor=actor, model=planner['model'],
                            provider=planner['connection'], tenant_id=tenant, custody_class='tenant_estate', system_message=PLAN_SYSTEM, session_id=session + ':plan')
    raw = response.text.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    try: notes = json.loads(raw[start:end + 1])
    except ValueError: notes = _lenient_json(raw[start:end + 1]) or {'title_direction': None, 'chapter_notes': {}, 'cautions': ['planner response was not valid JSON; deterministic outline stands']}
    return {'model': response.model_id, 'provider': response.provider, 'receipt_id': response.receipt_id, 'tokens_in': response.tokens_in, 'tokens_out': response.tokens_out, 'latency_ms': response.latency_ms,
            'title_direction': notes.get('title_direction'), 'chapter_notes': {k: str(v)[:600] for k, v in (notes.get('chapter_notes') or {}).items() if isinstance(k, str)}, 'cautions': [str(c)[:300] for c in (notes.get('cautions') or [])][:8]}


# ----------------------------------------------------------------------------- Independent reviewer (different model family from the writer and planner)
REVIEW_SYSTEM = ('You are the independent reviewer in Akki\'s document studio, from a different model family than the writer. You receive the evidence the writer was given, '
                 'the story plan and the gated draft. Check every sentence against the evidence: a claim that the evidence does not support, a token used for a different quantity than its label, '
                 'a recommendation that contradicts the owner declarations, a chapter that does not answer its question, or a missing material finding that the evidence plainly carries. '
                 'Return ONLY JSON: {"verdict": "accept" | "repair", "findings": [{"path": "draft.slots.x.title", "severity": "blocking" | "advisory", "issue": "...", "fix": "..."}], "summary": "one or two sentences"}. '
                 'Mark blocking only what would mislead the owner. At most eight findings. No markdown.')


async def review(content: Dict[str, Any], brief: Dict[str, Any], plan_: Dict[str, Any], draft: Dict[str, Any], tenant: str, actor: str, session: str) -> Dict[str, Any]:
    from services.chokepoint.llm import invoke
    from services.chokepoint.model_roles import resolve
    reviewer = resolve('reviewer')
    prompt = {'brief': {k: brief.get(k) for k in ('purpose', 'audience', 'constraints')}, 'evidence': evidence(content), 'plan': plan_['story'], 'draft': draft,
              'acceptance': ['every figure is a token that exists in evidence and is used for the quantity its label names', 'each chapter answers its question with its own evidence',
                             'actions follow from the evidence and honour owner_declarations', 'risks name what the evidence cannot establish, from coverage.cannot_say', 'no invented price, right or cause']}
    response = await invoke(purpose='doc_studio.review', prompt=json.dumps(prompt, default=str), masking_tier='llm_prompt_governed_text', actor=actor, model=reviewer['model'],
                            provider=reviewer['connection'], tenant_id=tenant, custody_class='tenant_estate', system_message=REVIEW_SYSTEM, session_id=session + ':review')
    raw = response.text.strip()
    if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    start, end = raw.find('{'), raw.rfind('}')
    try: verdict = json.loads(raw[start:end + 1])
    except ValueError: verdict = _lenient_json(raw[start:end + 1]) or {'verdict': 'unreadable', 'findings': [], 'summary': 'reviewer response was not valid JSON; recorded, not acted on'}
    findings = [f for f in (verdict.get('findings') or []) if isinstance(f, dict)]
    return {'model': response.model_id, 'provider': response.provider, 'receipt_id': response.receipt_id, 'tokens_in': response.tokens_in, 'tokens_out': response.tokens_out, 'latency_ms': response.latency_ms,
            'verdict': verdict.get('verdict'), 'summary': verdict.get('summary'), 'findings': findings[:8],
            'blocking': [f"{f.get('path', 'draft')}: {f.get('issue', '')} — {f.get('fix', '')}" for f in findings if f.get('severity') == 'blocking'][:8]}


async def compose(files: Dict[str, Any], tenant: str, actor: str, session: str) -> Tuple[Dict[str, Any] | None, Dict[str, Any], List[str]]:
    """Plan, write, gate, independent review; bounded repair passes. Returns (bound files or None, meta, remaining issues)."""
    content, brief = files['content.json'], files['brief.json']
    plan_ = plan(content, brief)
    try:
        planner = await plan_notes(content, brief, plan_, tenant, actor, session)
        plan_['planner_notes'] = {'title_direction': planner.get('title_direction'), 'chapter_notes': planner.get('chapter_notes'), 'cautions': planner.get('cautions')}
    except Exception as exc:
        planner = {'verdict': 'unavailable', 'error': type(exc).__name__, 'resolution': 'orchestrating planner unavailable; the deterministic outline stands and the gap is disclosed'}
    draft, meta = await write(content, brief, plan_, tenant, actor, session)
    issues = manage(draft, content, plan_); repairs = 0
    while issues and repairs < MAX_REPAIRS:
        repairs += 1
        draft, meta2 = await write(content, brief, plan_, tenant, actor, session, issues=issues, previous=draft)
        meta = {**meta2, 'tokens_in': meta['tokens_in'] + meta2['tokens_in'], 'tokens_out': meta['tokens_out'] + meta2['tokens_out'], 'repairs': repairs}
        issues = manage(draft, content, plan_)
    reviewed = None
    if not issues:
        try:
            reviewed = await review(content, brief, plan_, draft, tenant, actor, session)
            if reviewed['blocking']:
                # The writer answers the reviewer once; the content manager gates the answer like any other draft. Disagreement stays on record.
                repaired, meta2 = await write(content, brief, plan_, tenant, actor, session, issues=[f'independent reviewer ({reviewed["model"]}): {b}' for b in reviewed['blocking']], previous=draft)
                if not manage(repaired, content, plan_):
                    draft = repaired; meta = {**meta2, 'tokens_in': meta['tokens_in'] + meta2['tokens_in'], 'tokens_out': meta['tokens_out'] + meta2['tokens_out'], 'repairs': repairs + 1}
                    reviewed['resolution'] = 'writer revised the draft on the reviewer\'s blocking findings; revised draft passed the content manager'
                else:
                    reviewed['resolution'] = 'writer\'s revision failed the content manager; the gated original stands and the disagreement is recorded'
            else:
                reviewed['resolution'] = 'accepted without blocking findings'
        except Exception as exc:
            reviewed = {'verdict': 'unavailable', 'error': type(exc).__name__, 'resolution': 'independent review unavailable; the gated draft stands and the gap is disclosed'}
    meta['gate'] = {'passed': not issues, 'issues': issues, 'repairs': meta.get('repairs', repairs), 'plan_slots': len(plan_['slots'])}
    meta['review'] = reviewed
    meta['planner'] = planner
    meta['draft'] = draft
    if issues:
        return None, meta, issues
    return apply(files, draft, plan_, {k: v for k, v in meta.items() if k != 'draft'}), meta, []
