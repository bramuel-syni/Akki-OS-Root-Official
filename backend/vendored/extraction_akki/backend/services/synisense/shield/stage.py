"""Shield stage — the discrete sealed stage every estate crossing passes before the chokepoint (WP-A5 · Doc 1 A5.2 B36–B39, A5.3 B40–B41,
A5.6 B46 · Doc 2 B5.1–B5.6 B65–B85).

A question-with-data request is split into two distinct files from here on (B65): File 1 — the question as asked, together with the caller's
instructions (the same side of the request); File 2 — the extracted data before redaction. Each file is de-identified and register-gated on
its own, with no shared context (B66/B76): its own NER pass, its own contained read, its own placeholder numbering. Re-association is a named
seam (B67): placeholders are unified across the pair (one value → one token; a colliding token is renumbered, never guessed), every file's
markers are re-checked against the union of protected values (mark twice), and the minimal joint re-identification check (B73/B74) refuses a
pair whose halves together point at a party each withheld alone. What leaves is a `SafeArtifact`: the safe items, a receipt of counts and
digests, and a seal the chokepoint verifies (A5.6 — a function signature, not a review). The binding map stays in the process and is
destroyed when the call returns (B40); the artifact answers exactly one query (B72). Both files are retained in full under their own custody
class and are masked again at every later read (B71), never freely readable."""
import asyncio
import hashlib
import hmac
import json
import os
import re
import uuid
from dataclasses import dataclass, field

from services.synisense.shield import register_gate
from services.synisense.shield import semantic_register as reg
from services.synisense.shield.contained_reader import ReaderUnavailable
from services.synisense.shield.deidentifier import deidentify
from services.training_lab import store as lab

_SEAL_KEY = os.urandom(32)  # per process; the chokepoint verifies in the same process — an artifact built by hand carries no valid seal
ARTIFACT_TTL_SECONDS = 15 * 60
CUSTODY_RETAINED = 'dual_file_retained'
FILE_1, FILE_2 = 'file_1_question', 'file_2_data'
TOKEN = re.compile(r'(\[\[?)([A-Z][A-Z0-9_]*?)_(\d+)(\]\]?)')
STOPWORDS = {'the', 'and', 'for', 'with', 'from', 'test', 'limited', 'ltd', 'company', 'group', 'cooperative', 'society', 'holdings', 'services', 'this', 'that', 'wa', 'ya', 'na', 'kwa'}


class StageRefused(RuntimeError):
    """The stage could not form a sealed two-item context: nothing external is constructed."""

    def __init__(self, kind, reason, **detail):
        super().__init__(f'shield_stage_refused:{kind} — {reason}'); self.kind, self.reason, self.detail = kind, reason, detail


@dataclass
class SafeArtifact:
    artifact_id: str
    tenant_id: str
    purpose: str
    custody_class: str
    safe_items: list
    safe_system: str | None
    objective_ref: str | None
    receipt: dict
    protected_digest: str
    created_at: str
    seal: str = ''
    binding_map: dict = field(default_factory=dict, repr=False)
    entity_map: dict = field(default_factory=dict, repr=False)
    protected_values: list = field(default_factory=list, repr=False)
    consumed: dict | None = None

    def payload(self):
        return {'artifact_id': self.artifact_id, 'tenant_id': self.tenant_id, 'purpose': self.purpose, 'custody_class': self.custody_class, 'safe_items': self.safe_items, 'safe_system': self.safe_system,
                'objective_ref': self.objective_ref, 'protected_digest': self.protected_digest, 'created_at': self.created_at}

    def render(self):
        """The two-item context of ONE query (B72): the question, then the data it is answered from."""
        if len(self.safe_items) == 1: return self.safe_items[0]
        return f"[ITEM 1 — QUESTION AS ASKED]\n{self.safe_items[0]}\n\n[ITEM 2 — DATA]\n{self.safe_items[1]}"

    def summary(self):
        return {'artifact_id': self.artifact_id, 'items': len(self.safe_items), 'objective_ref': self.objective_ref, 'protected': len(self.protected_values), 'consumed': bool(self.consumed), **{k: self.receipt.get(k) for k in ('files', 'seam', 'reader_receipts', 'retained')}}


def _seal(artifact):
    return hmac.new(_SEAL_KEY, json.dumps(artifact.payload(), sort_keys=True, ensure_ascii=False).encode(), hashlib.sha256).hexdigest()


def verify(artifact, *, tenant_id, purpose, custody_class):
    """The chokepoint's check (B67 mark twice · A5.6): returns None when the artifact may cross, else the refusal reason."""
    if not isinstance(artifact, SafeArtifact): return 'not a SafeArtifact'
    if not hmac.compare_digest(artifact.seal or '', _seal(artifact)): return 'seal mismatch — the artifact was not produced by the stage in this process or was altered after sealing'
    if artifact.tenant_id != tenant_id: return 'tenant mismatch'
    if artifact.purpose != purpose: return f'purpose mismatch ({artifact.purpose} sealed, {purpose} invoked)'
    if artifact.custody_class != custody_class: return 'custody class mismatch'
    if artifact.consumed: return f"already consumed by crossing {artifact.consumed.get('receipt_id')} — one artifact answers one query (B72)"
    age = (_now_dt() - _parse(artifact.created_at)).total_seconds()
    if age > ARTIFACT_TTL_SECONDS: return f'artifact expired after {int(age)} s (request-scoped)'
    if not artifact.safe_items or not str(artifact.safe_items[0]).strip(): return 'empty question item'
    return None


def recheck(artifact, outbound_text):
    """Consumption-side re-check (B67/B77): no protected value of either file survives in what is about to leave."""
    return reg.inspect_outbound(outbound_text, artifact.protected_values)


def attested_recogniser(artifact):
    """For the chokepoint's register gate under a valid seal: Category 3 was read inside the stage; the gate re-runs Category 1/2 and the inspection."""
    def _attested(texts, tenant, purpose):
        return [[] for _ in texts], {'spans_total': artifact.receipt.get('reader_spans', 0), 'indirect_disclosures': [], 'undeclared': [], 'ambiguous': [], 'blocking_ambiguities': 0, 'receipts': list(artifact.receipt.get('reader_receipts') or []),
                                     'seconds': artifact.receipt.get('reader_seconds'), 'chunks': artifact.receipt.get('reader_chunks'), 'categories_asked': artifact.receipt.get('categories_asked'), 'attested_by_seal': artifact.artifact_id}
    return _attested


def consume(artifact, receipt_id):
    """After the one call: destroy the mapping (B40), mark the artifact consumed (B72), record the crossing on the retained files."""
    artifact.consumed = {'receipt_id': receipt_id, 'at': lab.now()}
    artifact.binding_map.clear(); artifact.entity_map.clear(); artifact.protected_values.clear()
    if artifact.custody_class != 'synthetic':
        lab.db().shield_dual_files.update_one({'artifact_id': artifact.artifact_id}, {'$set': {'crossed': artifact.consumed}})


def destroy(artifact):
    artifact.binding_map.clear(); artifact.entity_map.clear(); artifact.protected_values.clear()


def rebind(text, artifact):
    """Placeholders first (a binding value may itself be the NER token that masked the raw value), then the NER tokens back to their values."""
    from services.synisense.shield.reidentifier import reidentify
    return reidentify(register_gate.rebind(text or '', artifact.binding_map), artifact.entity_map)


# ----------------------------------------------------------------------------- independent assessment of one file (B66)
async def _assess(label, system_message, text, tenant_id, purpose, custody_class):
    """Inside the perimeter the contained reader reads the ORIGINAL file (Doc 1 A5.5) together with the deterministic Category 1/2 layers; the
    NER pass then covers what the register did not. Reading the original (not an NER-masked copy) keeps the reader's spans verbatim values —
    a masked copy made it mark `Label: [[ENT_…]]` spans, which defeated one-value-one-token at the seam (seen live 5 Oct)."""
    try:
        g = await asyncio.to_thread(register_gate.gate, system_message or '', text, tenant_id, f'{purpose}:{label}', custody_class)
    except ReaderUnavailable as exc:  # the gate normally returns a refusal; a raise here is still a refusal, never a fallback
        raise StageRefused('reader_unavailable', str(exc)[:200], file=label) from exc
    if g.refused:
        raise StageRefused('file_refused', f'{label}: {g.reason}', file=label, reader=g.reader)
    sep = register_gate_sep()
    de = await deidentify((g.system_message + sep + g.prompt) if system_message else g.prompt, tenant_id=tenant_id, purpose=f'{purpose}:{label}')
    if system_message and sep not in de.redacted_text:  # the boundary did not survive the NER pass: assess the two paths apart (same fallback as the chokepoint)
        de_sys, de = await deidentify(g.system_message, tenant_id=tenant_id, purpose=f'{purpose}:{label}:instructions'), await deidentify(g.prompt, tenant_id=tenant_id, purpose=f'{purpose}:{label}')
        sysm, body = de_sys.redacted_text, de.redacted_text; de.token_map = {**de_sys.token_map, **de.token_map}
    else:
        sysm, body = de.redacted_text.split(sep, 1) if system_message else ('', de.redacted_text)
    protected = list(g.token_map.values()) + [v for v in de.token_map.values() if isinstance(v, str)]
    clean = bool(g.inspection.get('clean')) and reg.inspect_outbound(sysm + '\n' + body, protected)['clean']
    markers = {'file': label, 'sha256_original': hashlib.sha256(text.encode()).hexdigest(), 'chars': len(text), 'clean': clean, 'enforced': dict(g.enforced), 'advisory': dict(g.advisory), 'cues_advisory': dict(g.cues_advisory),
               'entities_masked': len(de.token_map), 'placeholders': len(g.token_map), 'hostility': g.hostility.get('grade'), 'reader': g.reader}
    return {'label': label, 'safe_system': sysm if system_message else None, 'safe': body, 'binding': dict(g.token_map), 'entities': dict(de.token_map), 'protected': protected, 'markers': markers}


def register_gate_sep():
    return '\n\n[[AKKI_PAYLOAD_PATH_BOUNDARY]]\n\n'


# ----------------------------------------------------------------------------- the re-association seam (B67 · B73/B74)
def _fresh(token, taken):
    m = TOKEN.fullmatch(token)
    if not m: return token + '_b'
    open_, name, num, close = m.groups(); n = int(num)
    while True:
        n += 1; candidate = f'{open_}{name}_{str(n).zfill(len(num))}{close}'
        if candidate not in taken: return candidate


def _unify(first, second):
    """One value → one token across the pair; a token that names a different value in each file is renumbered in the second. Placeholders only."""
    safe, renamed, unified = second['safe'], 0, 0
    for kind in ('binding', 'entities'):
        a, b = first[kind], second[kind]
        by_value = {v.lower(): t for t, v in a.items() if isinstance(v, str)}
        taken = set(a) | set(b) | set(first['binding']) | set(first['entities']) | set(second['binding']) | set(second['entities'])
        for token, value in list(b.items()):
            same = by_value.get(str(value).lower())
            if same and same != token:
                safe = safe.replace(token, same); b.pop(token); unified += 1
            elif token in a and a[token] != value:
                new = _fresh(token, taken); taken.add(new); safe = safe.replace(token, new); b[new] = b.pop(token); renamed += 1
    second['safe'] = safe
    return {'unified': unified, 'renumbered': renamed}


def _joint_reidentification(items, protected):
    """B74 minimal check: a distinctive word of a value one file withheld must not survive in the OTHER file's safe text — together they would
    re-identify what each alone did not."""
    groups = []
    for i, item in enumerate(items):
        others = ' '.join(o['safe'] for j, o in enumerate(items) if j != i).lower()
        for value in item['protected']:
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]{3,}", str(value)) if w.lower() not in STOPWORDS]
            if len(words) < 2: continue
            hits = [w for w in words if re.search(r'(?<![a-z])' + re.escape(w.lower()) + r'(?![a-z])', others)]
            if hits: groups.append({'withheld_in': item['label'], 'value_sha256': hashlib.sha256(str(value).encode()).hexdigest()[:16], 'distinctive_words': len(words), 'surviving_elsewhere': len(hits)})
    return {'passes': not groups, 'groups': groups}


def _outbound_token(item, value):
    """The token that stands for `value` in an item's safe text: a placeholder bound to the raw value, or to the NER token that masks it, else that NER token."""
    low = str(value).lower()
    for t, v in item['binding'].items():
        if str(v).lower() == low: return t
    ent = next((t for t, v in item['entities'].items() if str(v).lower() == low), None)
    if ent is None: return None
    return next((t for t, v in item['binding'].items() if v == ent), ent)


def _cross_bind(items):
    """B67/B73: independent assessments may diverge — a value one file withheld can survive literally in the other file's safe text. The seam
    re-associates it under the token already bound to it (one value → one token); it never invents a value. A file's OWN withheld value
    surviving in its own text is not re-bound here — that is a dropped marker and refuses below."""
    bound = {}
    for i, item in enumerate(items):
        own = {str(v).lower() for v in item['protected']}
        for j, other in enumerate(items):
            if j == i: continue
            for value in other['protected']:
                s = str(value)
                if len(s) < 3 or s.lower() in own or TOKEN.fullmatch(s): continue
                token = _outbound_token(other, s)
                if not token: continue
                item['safe'], n = re.subn(r'(?<![A-Za-z0-9])' + re.escape(s) + r'(?![A-Za-z0-9])', token.replace('\\', '\\\\'), item['safe'], flags=re.IGNORECASE)
                if n: bound[item['label']] = bound.get(item['label'], 0) + n
    return bound


def _reassociate(items):
    seam = {'unified': 0, 'renumbered': 0}
    if len(items) == 2:
        u = _unify(items[0], items[1]); seam.update(u)
        seam['cross_bound'] = _cross_bind(items)
    protected = [v for it in items for v in it['protected']]
    rechecks = []
    for it in items:
        insp = reg.inspect_outbound((it['safe_system'] or '') + '\n' + it['safe'], protected)
        rechecks.append({'file': it['label'], 'marker_clean_at_assessment': it['markers']['clean'], 'clean_at_seam': insp['clean'], 'checked': insp['checked']})
        if not it['markers']['clean'] or not insp['clean']:
            raise StageRefused('seam_marker_failed', f"{it['label']} carries a protected value at the re-association seam; the two-item context is not formed", rechecks=rechecks)
    joint = _joint_reidentification(items, protected)
    if not joint['passes']:
        raise StageRefused('joint_reidentification', f"{len(joint['groups'])} withheld value(s) would be re-identified by the pair; the two-item context is not formed", groups=joint['groups'])
    seam.update(rechecks=rechecks, joint=joint)
    return seam, protected


# ----------------------------------------------------------------------------- retention under its own custody class (B68–B71)
def _retain(artifact, files, actor, session_id):
    lab.db().shield_dual_files.insert_one({'artifact_id': artifact.artifact_id, 'tenant_id': artifact.tenant_id, 'purpose': artifact.purpose, 'actor': actor, 'session_id': session_id, 'at': artifact.created_at, 'custody_class': CUSTODY_RETAINED,
                                           'read_policy': 'masked at every read through the live stage (Doc 2 B71); never returned raw', 'objective_ref': artifact.objective_ref, 'files': [{'file': label, 'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest()} for label, text in files],
                                           'receipt': artifact.receipt, 'seal': artifact.seal})


async def read_retained(artifact_id, tenant_id, actor, purpose='dual_file.audit_read'):
    """Any later consumption of the retained record passes through the same masking discipline as a live crossing (B71): fail-closed, never raw."""
    doc = lab.db().shield_dual_files.find_one({'artifact_id': artifact_id, 'tenant_id': tenant_id}, {'_id': 0})
    if not doc: raise LookupError('no retained dual-file record with that id for this tenant')
    masked = []
    for f in doc['files']:
        a = await _assess(f['file'], None, f['text'], tenant_id, purpose, 'tenant_estate')
        masked.append({'file': f['file'], 'sha256': f['sha256'], 'masked_text': a['safe'], 'markers': {k: a['markers'][k] for k in ('enforced', 'entities_masked', 'placeholders', 'clean')}})
    lab.db().shield_dual_files.update_one({'artifact_id': artifact_id}, {'$push': {'reads': {'at': lab.now(), 'by': actor, 'purpose': purpose, 'masked': True}}})
    return {**{k: doc[k] for k in ('artifact_id', 'tenant_id', 'purpose', 'at', 'custody_class', 'read_policy', 'objective_ref', 'receipt')}, 'files': masked, 'crossed': doc.get('crossed')}


# ----------------------------------------------------------------------------- the stage
async def stage(*, question, data=None, tenant_id, purpose, actor, custody_class='tenant_estate', system_message=None, objective_ref=None, session_id=None, retain=True):
    """Split (B65) → independent assessment (B66) → seam (B67, B74) → sealed SafeArtifact. Raises StageRefused; never falls back.
    WP-A7: the stage is a Watch-observed boundary (`shield.stage`): a seal is an admitted crossing, a refusal a refused one; an unobservable
    crossing does not happen."""
    q = str(question or '')
    if not q.strip(): raise StageRefused('empty_question', 'a crossing needs a question item')
    if custody_class not in ('tenant_estate', 'synthetic'): raise StageRefused('custody_class_invalid', custody_class)
    watch_actor = {'tenant_id': tenant_id, 'principal_id': str(actor or 'system')}
    digest = hashlib.sha256(json.dumps({'purpose': purpose, 'q': hashlib.sha256(q.encode()).hexdigest(), 'd': hashlib.sha256(str(data or '').encode()).hexdigest()}, sort_keys=True).encode()).hexdigest()
    try:
        return _observed(watch_actor, digest, await _stage(q, data, tenant_id, purpose, actor, custody_class, system_message, objective_ref, session_id, retain))
    except StageRefused as exc:
        _observed(watch_actor, digest, None, status=409 if exc.kind != 'reader_unavailable' else 503)
        raise


def _observed(watch_actor, digest, artifact, status=202):
    from services.watch import commission_gate
    try:
        commission_gate.observe(watch_actor, 'shield.stage', 'admitted' if artifact is not None else 'refused', status, digest)
    except commission_gate.GateUnobservable as exc:
        if artifact is not None: destroy(artifact)
        raise StageRefused('unobservable', f'the Watch could not observe this crossing; nothing is staged ({str(exc)[:120]})') from exc
    return artifact


async def _stage(q, data, tenant_id, purpose, actor, custody_class, system_message, objective_ref, session_id, retain):
    files = [(FILE_1, q)] + ([(FILE_2, str(data))] if data is not None and str(data).strip() else [])
    items = []
    for label, text in files:  # sequential and separate: the second assessment never sees the first (B76)
        items.append(await _assess(label, system_message if label == FILE_1 else None, text, tenant_id, purpose, custody_class))
    seam, protected = _reassociate(items)
    receipt = {'files': [it['markers'] for it in items], 'seam': seam, 'reader_receipts': [r for it in items for r in (it['markers']['reader'].get('receipts') or [])], 'reader_spans': sum(int(it['markers']['reader'].get('spans') or 0) for it in items),
               'reader_seconds': round(sum(float(it['markers']['reader'].get('seconds') or 0) for it in items), 3), 'reader_chunks': sum(int(it['markers']['reader'].get('chunks') or 0) for it in items), 'categories_asked': max([0] + [int(it['markers']['reader'].get('categories_asked') or 0) for it in items]),
               'protected_values': len(protected), 'retained': bool(retain and custody_class != 'synthetic')}
    artifact = SafeArtifact(artifact_id='sa-' + uuid.uuid4().hex[:12], tenant_id=tenant_id, purpose=purpose, custody_class=custody_class, safe_items=[it['safe'] for it in items], safe_system=items[0]['safe_system'], objective_ref=objective_ref, receipt=receipt,
                            protected_digest=register_gate.digest(protected), created_at=lab.now(), binding_map={t: v for it in items for t, v in it['binding'].items()}, entity_map={t: v for it in items for t, v in it['entities'].items()}, protected_values=protected)
    artifact.seal = _seal(artifact)
    if receipt['retained']: _retain(artifact, files, actor, session_id)
    return artifact


def _now_dt():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)


def _parse(iso):
    from datetime import datetime, timezone
    dt = datetime.fromisoformat(str(iso).replace('Z', '+00:00'))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


__all__ = ['SafeArtifact', 'StageRefused', 'stage', 'verify', 'recheck', 'attested_recogniser', 'consume', 'destroy', 'rebind', 'read_retained', 'CUSTODY_RETAINED', 'ARTIFACT_TTL_SECONDS']
