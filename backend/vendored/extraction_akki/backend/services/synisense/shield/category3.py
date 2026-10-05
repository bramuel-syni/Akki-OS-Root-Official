"""Category-3 contained recogniser (WP-A4 · Doc 2 A3 B21, A5.2 B35, A5.3 B36 · Doc 1 A5.4 B42, A6 B56).

The DPO's Category-3 declarations are descriptions of privileged meaning ("unreleased pricing", "who the counterparty is"); canon binds them
to the reasoning layer, not to literal or pattern match (B21). Here the contained reader (WP-A2) reads the whole text inside the perimeter
and marks the spans and indirect disclosures that carry a declared meaning; the register's deterministic layers (Category 1 patterns/NER,
Category 2 exact values) run alongside. Cue words survive only as the draft proposer and as advisory receipts — never as a refusal cause
(RC-2). An ambiguous read — a marked span that cannot be located in the text for an ENFORCED category, or an unreadable reading — refuses
safely; reader unavailability refuses before any external client exists (A2 d). Receipts carry counts and digests, never the values."""
import hashlib
import re

from services.synisense.shield import contained_reader as reader
from services.synisense.shield import semantic_register as reg

RECOGNISER = 'contained_reader'
CHUNK_CHARS = 9000
PATH_SEP = '\n\n[[AKKI_PAYLOAD_PATH_BOUNDARY]]\n\n'
OTHER = 'other_privileged'


class AmbiguousReading(Exception):
    """A marked meaning could not be bound to the text (or the reading was unusable) for an enforced category: refuse rather than guess."""


def _chunks(text):
    if len(text) <= CHUNK_CHARS: return [(0, text)]
    out, pos = [], 0
    while pos < len(text):
        end = min(len(text), pos + CHUNK_CHARS)
        if end < len(text):
            cut = max(text.rfind('\n', pos + CHUNK_CHARS // 2, end), text.rfind('. ', pos + CHUNK_CHARS // 2, end))
            if cut > pos: end = cut + 1
        out.append((pos, text[pos:end])); pos = end
    return out


def _locate(text, span, start_at=0):
    """Offsets of a marked span inside the text: verbatim, then case-insensitive, then whitespace-collapsed. None when the reader paraphrased."""
    needle = span.strip()
    if len(needle) < 2: return None
    i = text.find(needle, start_at)
    if i >= 0: return i, i + len(needle)
    m = re.compile(re.escape(needle), re.IGNORECASE).search(text, start_at)
    if m: return m.start(), m.end()
    loose = re.compile(r'\s+'.join(re.escape(w) for w in needle.split()), re.IGNORECASE)
    m = loose.search(text, start_at)
    return (m.start(), m.end()) if m else None


def _locate_all(text, span):
    """Every occurrence of a marked span: a value judged privileged in one sentence is the same value everywhere in the text."""
    out, pos = [], 0
    while True:
        where = _locate(text, span, pos)
        if where is None or where[1] <= pos: return out
        out.append(where); pos = where[1]


def declared(tenant):
    """Category-3 declarations in force, bound to the reader: name → declaration."""
    return {c['name']: c for c in reg.categories(tenant) if c['kind'] == 'contextual'}


def recognise(text, tenant, purpose, categories=None):
    """Read `text` with the contained reader against the tenant's Category-3 declarations. Returns located spans (register shape), indirect
    disclosures, undeclared privileged findings (for the proposer), the ambiguities and the receipts. Raises ReaderUnavailable / AmbiguousReading."""
    cats = declared(tenant) if categories is None else {c['name']: c for c in categories}
    asked = [{'name': n, 'description': (c.get('description') or '')[:200]} for n, c in cats.items()]
    spans, indirect, undeclared, ambiguous, receipts, seconds, objective = [], [], [], [], [], 0.0, None
    for offset, chunk in _chunks(text):
        out = reader.read(chunk, asked, purpose)
        reading = out['reading']; receipts.append(out['receipt_id']); seconds += float(out.get('seconds') or 0)
        objective = objective or reading.get('objective')
        for p in reading.get('privileged') or []:
            name, value = p.get('category'), p.get('span') or ''
            cat = cats.get(name)
            places = _locate_all(chunk, value)
            if cat is None:
                undeclared.append({'category': name or OTHER, 'value': value.strip(), 'reason': (p.get('reason') or '')[:160], 'located': bool(places)}); continue
            if not places:
                ambiguous.append({'category': name, 'enforcement': cat.get('enforcement', 'enforced'), 'reason': 'marked span not found verbatim in the text', 'span_sha256': hashlib.sha256(value.encode()).hexdigest()[:16]}); continue
            for a, b in places:
                spans.append({'start': offset + a, 'end': offset + b, 'text': text[offset + a:offset + b], 'category': name, 'kind': 'contextual', 'action': cat['action'], 'enforcement': cat.get('enforcement', 'enforced'), 'cue': f"{RECOGNISER}: {(p.get('reason') or 'privileged meaning')[:80]}", 'source': RECOGNISER})
        for phrase in reading.get('indirect_disclosures') or []:
            if not isinstance(phrase, str): continue
            places = _locate_all(chunk, phrase)
            indirect.append({'located': bool(places), 'phrase_sha256': hashlib.sha256(phrase.encode()).hexdigest()[:16]})
            for a, b in places:
                spans.append({'start': offset + a, 'end': offset + b, 'text': text[offset + a:offset + b], 'category': 'indirect_disclosure', 'kind': 'contextual', 'action': 'remove', 'enforcement': 'enforced', 'cue': f'{RECOGNISER}: reveals a protected fact without naming it', 'source': RECOGNISER})
    blocking = [a for a in ambiguous if a['enforcement'] == 'enforced']
    return {'spans': spans, 'spans_total': len(spans), 'indirect_disclosures': indirect, 'undeclared': undeclared, 'ambiguous': ambiguous, 'blocking_ambiguities': len(blocking), 'objective': objective, 'receipts': receipts, 'seconds': round(seconds, 3), 'chunks': len(receipts), 'categories_asked': len(asked)}


def recognise_paths(texts, tenant, purpose):
    """Several payload paths (system message, prompt) read as ONE text when they fit one read; spans come back per path with local offsets."""
    texts = [t or '' for t in texts]
    joined = PATH_SEP.join(texts)
    if len(joined) <= CHUNK_CHARS:
        out = recognise(joined, tenant, purpose); per_path = [[] for _ in texts]
        starts, pos = [], 0
        for t in texts: starts.append(pos); pos += len(t) + len(PATH_SEP)
        for s in out['spans']:
            for i, start in enumerate(starts):
                if start <= s['start'] < start + len(texts[i]):
                    per_path[i].append({**s, 'start': s['start'] - start, 'end': min(s['end'] - start, len(texts[i])), 'text': texts[i][s['start'] - start:min(s['end'] - start, len(texts[i]))]}); break
        return per_path, {k: v for k, v in out.items() if k != 'spans'}
    outs = [recognise(t, tenant, purpose) if t.strip() else {'spans': [], 'spans_total': 0, 'indirect_disclosures': [], 'undeclared': [], 'ambiguous': [], 'blocking_ambiguities': 0, 'objective': None, 'receipts': [], 'seconds': 0.0, 'chunks': 0, 'categories_asked': 0} for t in texts]
    merged = {'spans_total': sum(o['spans_total'] for o in outs), 'indirect_disclosures': sum((o['indirect_disclosures'] for o in outs), []), 'undeclared': sum((o['undeclared'] for o in outs), []), 'ambiguous': sum((o['ambiguous'] for o in outs), []), 'blocking_ambiguities': sum(o['blocking_ambiguities'] for o in outs),
              'objective': next((o['objective'] for o in outs if o['objective']), None), 'receipts': sum((o['receipts'] for o in outs), []), 'seconds': round(sum(o['seconds'] for o in outs), 3), 'chunks': sum(o['chunks'] for o in outs), 'categories_asked': max(o['categories_asked'] for o in outs)}
    return [o['spans'] for o in outs], merged


def intent_verdict(task, tenant, purpose):
    """The reader's verdict on a task (replaces cue lists as the refusal cause in task separation): does the asker want protected meaning itself?"""
    out = reader.read(task, [{'name': n, 'description': (c.get('description') or '')[:200]} for n, c in declared(tenant).items()], purpose)
    objective = out['reading'].get('objective') or {}
    return {'requests_privileged': bool(objective.get('requests_privileged')), 'coherent': bool(objective.get('coherent')), 'bounded_objective': str(objective.get('bounded_objective') or '')[:400], 'intent': str(objective.get('intent') or 'unspecified')[:80],
            'privileged_in_task': len(out['reading'].get('privileged') or []), 'receipt_id': out['receipt_id'], 'seconds': out.get('seconds')}


def summary(out):
    """Receipt-safe summary: counts, digests of receipts, never values."""
    return {'recogniser': RECOGNISER, 'spans': out.get('spans_total', len(out['spans']) if isinstance(out.get('spans'), list) else None), 'indirect_disclosures': len(out.get('indirect_disclosures') or []), 'undeclared': len(out.get('undeclared') or []), 'ambiguous': len(out.get('ambiguous') or []),
            'blocking_ambiguities': out.get('blocking_ambiguities', 0), 'chunks': out.get('chunks'), 'seconds': out.get('seconds'), 'receipts': list(out.get('receipts') or [])[:8]}


__all__ = ['RECOGNISER', 'AmbiguousReading', 'recognise', 'recognise_paths', 'intent_verdict', 'declared', 'summary', 'CHUNK_CHARS']
