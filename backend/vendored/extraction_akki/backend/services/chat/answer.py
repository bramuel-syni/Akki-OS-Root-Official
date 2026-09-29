"""Grounded answer (M4-T2/T3): the model reads exactly the pinned window and must cite the units it used.

The prompt is the objective, the bounded conversation ring, the question and the selected whole units. The
reply is JSON so grounding can be checked mechanically: cited units must be in the window; a reply that says the
window is insufficient is returned as a narrow answer, never dressed up as complete.
"""
import json
import re

from services.chokepoint import ChokepointRefused
from services.chokepoint import llm as chokepoint
from services.chokepoint.llm import LLMShieldFailure, PurposeInvalid
from services.chokepoint.llm_endpoint_allowlist import LLMEndpointRefused
from services.synisense.exceptions import ServiceUnavailable
from services.watch.input_seat import WatchInputSeatVerdictRefused

REFUSALS = (LLMShieldFailure, PurposeInvalid, ChokepointRefused, LLMEndpointRefused, WatchInputSeatVerdictRefused, ServiceUnavailable)

SYSTEM = ("You are Akki, a governed answerer. You may use ONLY the qualified units supplied in the window. "
          "Every statement must be supported by those units. Reply with one JSON object and nothing else: "
          '{"answer": "<plain-language answer>", "cited_units": ["<unit ref>", ...], "sufficient": true|false, '
          '"unsupported": "<what the window cannot answer, or empty>"}. '
          "If the window cannot support a complete answer, answer only the supported part and set sufficient to false. "
          "Never invent values, names or totals that are not in the units.")


def prompt_for(*, objective, context_lines, question, selected):
    parts = [f"OBJECTIVE (frozen for this session): {objective}"]
    if context_lines:
        parts.append('CONVERSATION SO FAR:\n' + '\n'.join(context_lines))
    parts.append(f"QUESTION: {question}")
    parts.append(f"WINDOW ({len(selected)} whole qualified units, one JSON per line):\n" + '\n'.join(c['text'] for c in selected))
    return '\n\n'.join(parts)


def parse(text):
    body = text.strip()
    match = re.search(r'\{.*\}', body, re.S)
    if not match:
        return None
    try:
        value = json.loads(match.group(0))
    except ValueError:
        return None
    return value if isinstance(value, dict) and isinstance(value.get('answer'), str) else None


def ground(parsed, selected_refs, raw_text):
    """Mechanical grounding: citations must name units in the window; unparsable replies are marked, not smoothed."""
    if parsed is None:
        return {'answer': raw_text.strip()[:4000], 'cited_refs': [], 'sufficient': False, 'grounding': 'unverified_format',
                'unsupported': 'The model did not return the required citation structure; treat this text as unverified.'}
    cited = [c for c in parsed.get('cited_units') or [] if isinstance(c, str)]
    known = [c for c in dict.fromkeys(cited) if c in selected_refs]
    dropped = len(cited) - len(known)
    grounding = 'cited_in_window' if known and not dropped else 'partially_cited' if known else 'uncited'
    return {'answer': parsed['answer'].strip()[:4000], 'cited_refs': known, 'sufficient': bool(parsed.get('sufficient')) and grounding == 'cited_in_window',
            'grounding': grounding, 'unsupported': str(parsed.get('unsupported') or '')[:600], 'citations_dropped': dropped}


async def answer(*, scope, session, question, context_lines, selected, model, provider, actor):
    prompt = prompt_for(objective=session['objective']['text'], context_lines=context_lines, question=question, selected=selected)
    try:
        response = await chokepoint.invoke(purpose='chat.governed_answer', prompt=prompt, masking_tier='llm_prompt_governed_text',
                                           actor=actor, model=model, provider=provider, tenant_id=scope['tenant_id'],
                                           custody_class='tenant_estate', system_message=SYSTEM, session_id=session['session_id'])
    except REFUSALS as exc:
        return {'refused': True, 'refusal_reason': str(exc)[:400], 'prompt_chars': len(prompt)}
    grounded = ground(parse(response.text), {c['ref'] for c in selected}, response.text)
    return {'refused': False, **grounded, 'receipt_id': response.receipt_id, 'model_id': response.model_id, 'provider': response.provider,
            'tokens_in': response.tokens_in, 'tokens_out': response.tokens_out, 'latency_ms': response.latency_ms,
            'shield': response.shield, 'prompt_chars': len(prompt)}
