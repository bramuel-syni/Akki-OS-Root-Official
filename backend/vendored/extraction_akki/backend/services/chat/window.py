"""Context window (CC-4/5/6): whole units, pinned ranking, native tokenizer measurement, explicit loss.

Reuses the frozen `ContextWindow` reconstruction contract in services.non_gpu_governance.context: the window
this module returns is the one that contract can rebuild; nothing is reranked after assembly.
"""
import hashlib
import json
import os
from types import SimpleNamespace

import tiktoken

from services.non_gpu_governance.context import ContextUnit, ContextWindow, ORDER, assemble

TOKENIZER = 'tiktoken:o200k_base'
RANKING_RULE = ('CC-4/5/6 v1: load-bearing first, then class (fact, inference, utterance, non_factual), then relational '
                'proximity, then source-position recency, then unit id; whole units only; no reranking after assembly')
_ENC = tiktoken.get_encoding('o200k_base')


def _int_env(name, default):
    try:
        return int(os.environ.get(name) or default)
    except ValueError:
        return default


# [SLOT] model window budget for the qualified-unit ring; measured by the tokenizer above, never guessed.
WINDOW_TOKENS = _int_env('AKKI_ANSWER_WINDOW_TOKENS', 6000)
# [SLOT] tokens kept for the reply.
ANSWER_RESERVE_TOKENS = _int_env('AKKI_ANSWER_RESERVE_TOKENS', 900)
# [SLOT] how many best-matching units are load-bearing.
LOAD_BEARING_MAX = _int_env('AKKI_ANSWER_LOAD_BEARING_MAX', 6)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def count_tokens(text):
    return len(_ENC.encode(text, disallowed_special=()))


def render_unit(candidate):
    """The exact bytes a unit occupies in the window: id, locator, then its record."""
    unit = candidate['unit']
    locator = unit['provenance']['locator']
    return json.dumps({'unit': candidate['ref'], 'source': f"{locator['database']}.{locator['table']} {locator['primary_key']}={locator['key_value']}",
                       'class': candidate['class_label'], 'record': unit.get('record') or {}}, ensure_ascii=False, separators=(',', ':'))


def classify(candidates):
    """Load-bearing = best term matches (bounded); proximity 0 load-bearing, 1 other matches, 2 relational neighbours."""
    matched = sorted([c for c in candidates if c['kind'] == 'matched'], key=lambda c: (-c['overlap'], c['position'], c['ref']))
    load_bearing = tuple(c['ref'] for c in matched[:LOAD_BEARING_MAX])
    for c in candidates:
        c['text'] = render_unit(c)
        c['tokens'] = max(1, count_tokens(c['text']))
        c['proximity'] = 0 if c['ref'] in load_bearing else 1 if c['kind'] == 'matched' else 2
    return load_bearing


def build(*, objective_text, frame_ref, model, qualified_set_receipt_ref, candidates, reserved_tokens):
    """Deterministic window over whole units. Returns (ContextWindow, selected candidates, excluded candidates)."""
    load_bearing = classify(candidates)
    units = tuple(ContextUnit(unit_ref=c['ref'], content_sha256=c['content_sha256'], reextraction_ref=c['reextraction_ref'],
                              class_label=c['class_label'] if c['class_label'] in ORDER else 'utterance', tokens=c['tokens'],
                              proximity=c['proximity'], source_position=c['position']) for c in candidates)
    reserved = min(reserved_tokens, WINDOW_TOKENS - 1)
    draft = SimpleNamespace(units=units, load_bearing_refs=load_bearing, window_tokens=WINDOW_TOKENS, reserved_tokens=reserved)
    selected, excluded = assemble(draft)
    window = ContextWindow(version='akki.context.metadata/1', objective_sha256=sha(objective_text), frame_ref=frame_ref,
                           model_sha256=sha(model), tokenizer_sha256=sha(TOKENIZER), ranking_rule_ref=sha(RANKING_RULE),
                           qualified_set_receipt_ref=qualified_set_receipt_ref, load_bearing_refs=load_bearing,
                           window_tokens=WINDOW_TOKENS, reserved_tokens=reserved, units=units,
                           selected_refs=tuple(u.unit_ref for u in selected),
                           excluded_counts={c: sum(1 for u in excluded if u.class_label == c) for c in ORDER},
                           top_excluded_handles=tuple(u.reextraction_ref for u in excluded[:10]), loss_disclosed=bool(excluded))
    by_ref = {c['ref']: c for c in candidates}
    return window, [by_ref[u.unit_ref] for u in selected], [by_ref[u.unit_ref] for u in excluded]


def loss_statement(window, read):
    """The loss statement that travels with the trace AND the answer (CC-6)."""
    excluded = sum(window.excluded_counts.values())
    beyond = max(0, read['matched_total'] - sum(1 for u in window.units if u.proximity < 2))
    parts = [f"{len(window.selected_refs)} whole units in the window ({sum(u.tokens for u in window.units if u.unit_ref in window.selected_refs)} tokens of {window.window_tokens - window.reserved_tokens})"]
    if excluded:
        parts.append('excluded by budget: ' + ', '.join(f"{n} {c}" for c, n in window.excluded_counts.items() if n))
    if beyond:
        parts.append(f"{beyond} further matching units not retrieved (candidate bound)")
    if read.get('failures'):
        parts.append(f"{len(read['failures'])} artefact(s) unreadable this turn")
    if not excluded and not beyond and not read.get('failures'):
        parts.append('no context loss')
    return '; '.join(parts) + '.'
