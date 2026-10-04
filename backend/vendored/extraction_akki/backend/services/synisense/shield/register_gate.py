"""Shield register gate for EVERY model crossing (Mα MA-04/MA-05). Runs inside `chokepoint.llm.invoke` after the NER de-identifier:
the system message and the prompt are both classified against the tenant register; `enforced` categories are rewritten to typed placeholders
(or withheld) and rebound in the reply; `advisory` categories are counted and receipted; the final outbound text is inspected for every
enforced value and the crossing is refused if one survives. Hostility is scored from the payload content with a declared rule list — a
deterministic detector, not a learned model, and never a placeholder reading metadata. The binding map never leaves the process."""
import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass, field

from services.synisense.shield import semantic_register as reg

# (cue regex, weight). Weights ≥ 3 alone reach `block`; 2 reaches `hold`; one weight-1 cue is `medium` and still passes, on the record.
HOSTILITY_RULES = (
    (r'(?i)\bignore\s+(?:all\s+|any\s+)?(?:previous|prior|above|earlier)\s+(?:instructions?|rules?|prompts?)', 3, 'instruction_override'),
    (r'(?i)\bdisregard\s+(?:your|the|all)\s+(?:instructions?|rules?|guidelines?|system)', 3, 'instruction_override'),
    (r'(?i)\b(?:reveal|print|show|repeat|output|leak)\s+(?:your|the)\s+(?:hidden\s+|full\s+)?(?:system\s+prompt|instructions|developer\s+message)', 3, 'prompt_exfiltration'),
    (r'(?i)\b(?:exfiltrat|send\s+(?:this|the|all)\s+(?:data|records?|contract|file)s?\s+to\s+https?://|post\s+(?:it|them|the\s+data)\s+to\s+https?://)', 3, 'exfiltration'),
    (r'(?i)\b(?:curl|wget)\s+(?:-[A-Za-z]+\s+)*https?://', 2, 'fetch_tool'),
    (r'(?i)\byou\s+are\s+now\s+(?:dan|an?\s+unrestricted|free\s+of|no\s+longer)', 3, 'persona_hijack'),
    (r'(?i)\b(?:developer|jailbreak|god)\s+mode\b', 2, 'persona_hijack'),
    (r'(?i)<\s*script\b|javascript:', 2, 'markup_injection'),
    (r'(?i)\b(?:drop\s+table|rm\s+-rf\s+/|;\s*shutdown\b)', 2, 'destructive_command'),
    (r'(?i)\b(?:fetch|download|open|read)\s+(?:the\s+)?(?:original|raw)\s+(?:document|contract|file|records?)\b', 2, 'rehydration_request'),
    (r'[A-Za-z0-9+/]{120,}={0,2}', 1, 'opaque_blob'),
    (r'(?i)\b(?:password|api[-_ ]?key|secret\s+key|token)\s*[:=]\s*\S{6,}', 1, 'credential_in_payload'),
)
PLACEHOLDER = re.compile(r'\[[A-Z][A-Z0-9_]*_\d+\]')


@dataclass
class GateResult:
    system_message: str
    prompt: str
    token_map: dict = field(default_factory=dict)
    enforced: dict = field(default_factory=dict)
    advisory: dict = field(default_factory=dict)
    inspection: dict = field(default_factory=dict)
    hostility: dict = field(default_factory=dict)
    refused: bool = False
    reason: str | None = None

    def summary(self):
        return {'register_enforced': dict(self.enforced), 'register_advisory': dict(self.advisory), 'placeholders': len(self.token_map), 'egress_clean': self.inspection.get('clean'),
                'hostility': self.hostility.get('grade'), 'hostility_rules_hit': self.hostility.get('rules'), 'refused': self.refused, 'reason': self.reason}


def score_hostility(text):
    """Declared rule list over the full outbound content; grade low/medium/high, verdict pass/hold/block."""
    hits, weight = [], 0
    for pattern, w, label in HOSTILITY_RULES:
        n = len(re.findall(pattern, text or ''))
        if n: hits.append(label); weight += w * min(n, 3)
    grade = 'high' if weight >= 3 else 'medium' if weight else 'low'
    verdict = 'block' if weight >= 3 else 'hold' if weight == 2 else 'pass'
    return {'grade': grade, 'verdict': verdict, 'weight': weight, 'rules': sorted(set(hits)), 'detector': 'shield.register_gate.rules.v1 (deterministic, declared)'}


def _rewrite(text, spans, counters, token_map):
    out, pos = [], 0
    for s in spans:
        out.append(text[pos:s['start']])
        if s['action'] == 'remove':
            out.append('[METHOD_WITHHELD]' if s['category'].startswith('unpublished_pricing_method') else '[REDACTED_WITHHELD]')
        else:
            token, hint = reg._placeholder(s, counters); token_map[token] = s['text']; out.append(token)
        pos = s['end']
    out.append(text[pos:])
    return re.sub(r'[ \t]{2,}', ' ', ''.join(out))


def gate(system_message, prompt, tenant_id, purpose=None):
    """Classify both payload paths; rewrite enforced spans with one shared placeholder numbering; inspect the whole outbound; score hostility."""
    counters, token_map, enforced, advisory = defaultdict(int), {}, defaultdict(int), defaultdict(int)
    parts, withheld = [], []
    for text in (system_message or '', prompt or ''):
        spans = reg.classify(text, tenant_id) if text else []
        for s in spans: (enforced if s['enforcement'] == 'enforced' else advisory)[s['category']] += 1
        keep = [s for s in spans if s['enforcement'] == 'enforced']
        withheld += [s['text'] for s in keep if s['action'] == 'remove']
        parts.append(_rewrite(text, keep, counters, token_map) if keep else text)
    # the same value may appear in both paths under different tokens; one value → one token keeps the reply rebindable
    seen = {}
    for token, value in list(token_map.items()):
        key = value.lower()
        if key in seen:
            parts = [p.replace(token, seen[key]) for p in parts]; token_map.pop(token)
        else: seen[key] = token
    # a value classified protected in one sentence is the same value everywhere: every remaining literal occurrence takes the same placeholder
    for token, value in list(token_map.items()):
        rx = re.compile(r'(?<!\w)' + re.escape(value) + r'(?!\w)', re.IGNORECASE)
        parts = [rx.sub(token, p) for p in parts]
    for value in withheld:
        parts = [p.replace(value, '[REDACTED_WITHHELD]') for p in parts]
    protected = list(token_map.values()) + withheld
    inspection = reg.inspect_outbound(parts[0] + '\n' + parts[1], protected)
    hostility = score_hostility(parts[0] + '\n' + parts[1])
    result = GateResult(system_message=parts[0], prompt=parts[1], token_map=token_map, enforced=dict(enforced), advisory=dict(advisory), inspection=inspection, hostility=hostility)
    if not inspection['clean']:
        result.refused, result.reason = True, f"register_egress_refused — {len(inspection['protected_values_found'])} enforced value(s) would survive in the outbound payload"
    return result


def rebind(text, token_map):
    """Bind the model's reply back to the real values, locally. Unknown placeholders stay visible rather than being guessed."""
    out = text or ''
    for token, value in sorted(token_map.items(), key=lambda kv: -len(kv[0])): out = out.replace(token, value)
    return out


def digest(values):
    return hashlib.sha256(''.join(sorted(values)).encode()).hexdigest()
