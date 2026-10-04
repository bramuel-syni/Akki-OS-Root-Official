"""WPW Tier 2 for Mα runs (WPW-8..10, A4, A6). A technical report drafts automatically when a lane job settles — completed-and-met, completed-and-not-met,
failed, cancelled — from the retained m9 job record, the AIP database record and the commission's Tier 1 notebook. Nothing is paraphrased or reconstructed:
every figure carries its evidence class and a receipt line that resolves into a retained record (checked mechanically; unresolvable figures move to
`refused_figures` and the section says the record is silent). Reports are internal (WPW-10) and land in Documents through the deterministic studio."""
import logging
import re
from datetime import datetime, timezone

from services.wpw import tier1_notebook as nb
from services.wpw.tier2_report import (
    ACCEPTANCE_CRITERIA_ORDER,
    INTERNAL_ONLY_MARKER,
    SECTION_SKELETON,
    _figure,
    _refused,
)

log = logging.getLogger(__name__)
TENANT = 'RMS'
SECTION_TITLES = {'problem_and_objective': 'Problem and objective', 'data_statement': 'Data statement (classification-driven)', 'baseline_record': 'Baseline record', 'method': 'Method (including adopted ideation events)',
                  'setup_and_reproducibility': 'Setup and reproducibility', 'results_on_held_out': 'Results on held-out material', 'ablations': 'Ablations', 'limitations': 'Limitations', 'negative_results': 'Negative results'}
SILENT = '_the record is silent on this._'


# ----------------------------------------------------------------------------- record access and mechanical resolution (A4)
def _walk(obj, path):
    for part in [p for p in path.split('.') if p]:
        if isinstance(obj, list):
            try: obj = obj[int(part)]
            except (ValueError, IndexError): return None
        elif isinstance(obj, dict): obj = obj.get(part)
        else: return None
        if obj is None: return None
    return obj


def resolve_receipt_line(line):
    """`m9j-<id>#<dotted.path>` → value inside the retained m9 job file; `wpw://notebook/<run>/<entry_id>` → a notebook entry; `malpha://commission/<id>#<path>` → commission record."""
    from services.training_lab import malpha
    from services.training_runner import m9_dispatch
    if line.startswith('m9j-'):
        job_id, _, path = line.partition('#')
        job = m9_dispatch.load_job(job_id)
        return None if job is None else _walk(job, path) if path else job
    if line.startswith('wpw://notebook/'):
        run_id, _, entry_id = line[len('wpw://notebook/'):].partition('/')
        return next((e for e in nb.list_entries(run_id) if e.get('entry_id') == entry_id), None)
    if line.startswith('malpha://commission/'):
        cid, _, path = line[len('malpha://commission/'):].partition('#')
        doc = malpha.commission(cid)
        return None if doc is None else _walk(doc, path) if path else doc
    return None


class _Figures:
    def __init__(self):
        self.figures, self.refused = [], []

    def add(self, figure_id, evidence_class, receipt_line, summary):
        value = resolve_receipt_line(receipt_line)
        if value is None:
            self.refused.append(_refused(figure_id, receipt_line, 'receipt line does not resolve to a retained record; figure not rendered (WPW-9)'))
            return None
        self.figures.append(_figure(figure_id, evidence_class, receipt_line, summary))
        return value


def _fmt(v, nd=4):
    if v is None: return '—'
    if isinstance(v, bool): return 'yes' if v else 'no'
    if isinstance(v, float): return f'{v:.{nd}f}'.rstrip('0').rstrip('.') if nd else str(v)
    return str(v)


def _pct(v):
    return '—' if v is None else f'{100 * v:.1f} %'


# ----------------------------------------------------------------------------- the six criteria, per lane, from the run's own instrumentation
def _criteria(rec, job):
    """Every criterion of the fixed set is named with its number where the run measured it, its adopted threshold where the Outcome fixed one, and a pass
    where both exist. Where the run did not instrument a criterion the row says so — it is not filled."""
    lane = rec['lane'].replace('_evaluate', ''); jid = rec['job_id']; result = (job.get('receipt') or {}).get('result') or {}
    langs = rec['params'].get('languages') or []
    evaluate = rec['phase'] == 'malpha_evaluate'
    dev = result.get('evaluation') if evaluate else result.get('dev')
    base = f'{jid}#receipt.result.' + ('evaluation' if evaluate else 'dev')
    rows = []
    if lane == 'listener' and dev:
        per = {l: ((dev.get('mentions') or {}).get(l) or {}) for l in langs}
        vals = [min(p['precision'], p['recall']) for p in per.values() if p.get('precision') is not None and p.get('recall') is not None]
        rows.append({'name': 'held_out_accuracy', 'measured': 'min over languages of min(mention precision, recall) = ' + (_fmt(min(vals)) if vals else 'not measurable (no mention-bearing segments in a language)'), 'value': min(vals) if vals else None,
                     'threshold': '≥ 0.90 per language (owner 90 % target, operationalised)', 'pass': (len(vals) == len(langs) and min(vals) >= 0.9) if vals else False, 'class': 'measured', 'receipt': base + '.mentions',
                     'detail': '; '.join(f"{l}: P {_fmt(p.get('precision'))} R {_fmt(p.get('recall'))} on {p.get('segments_with_mentions')} mention segments" for l, p in per.items())})
        abst = sum(p.get('abstained_segments') or 0 for p in per.values()); segs = sum(p.get('segments') or 0 for p in per.values())
        rows.append({'name': 'abstention_calibration', 'measured': f'{abst} abstained of {segs} evaluated segments ({_pct(abst / segs) if segs else "—"})', 'value': (abst / segs) if segs else None, 'threshold': 'reported separately; no bar adopted in the Outcome', 'pass': None, 'class': 'measured', 'receipt': base + '.mentions'})
        lat = dev.get('latency') or {}
        rows.append({'name': 'latency_p95_ms', 'measured': f"real-time factor {_fmt(lat.get('real_time_factor'))} over {_fmt(lat.get('audio_seconds'), 1)} s of audio (p95 per segment not instrumented)", 'value': lat.get('real_time_factor'), 'threshold': 'reported separately; no bar adopted', 'pass': None, 'class': 'measured', 'receipt': base + '.latency'})
    elif lane == 'story_text' and dev:
        per = {l: ((dev.get('per_language') or {}).get(l) or {}) for l in langs}
        fid = [p.get('language_fidelity_rate') for p in per.values() if p.get('language_fidelity_rate') is not None]
        below = [p.get('dev_perplexity_below_base') for p in per.values()]
        ok = bool(fid) and len(fid) == len(langs) and min(fid) == 1.0 and all(b is True for b in below)
        rows.append({'name': 'held_out_accuracy', 'measured': 'language fidelity ' + ', '.join(f"{l} {_fmt(p.get('language_fidelity_rate'))}" for l, p in per.items()) + '; dev perplexity ' + ', '.join(f"{l} {_fmt(p.get('dev_perplexity'), 2)} (base {_fmt(p.get('base_perplexity'), 2)})" for l, p in per.items()),
                     'value': min(fid) if fid else None, 'threshold': 'fidelity 1.0 per language and dev perplexity below the registered base', 'pass': ok, 'class': 'measured', 'receipt': base + '.per_language'})
        rows.append({'name': 'abstention_calibration', 'measured': 'not instrumented for story generation', 'value': None, 'threshold': '—', 'pass': None, 'class': None, 'receipt': None})
        rows.append({'name': 'latency_p95_ms', 'measured': 'not instrumented for story generation', 'value': None, 'threshold': '—', 'pass': None, 'class': None, 'receipt': None})
    elif lane == 'story_voice' and dev:
        per = {l: ((dev.get('per_language') or {}).get(l) or {}) for l in langs}
        sims = [((p.get('behaviour') or {}).get('overall_similarity')) for p in per.values()]
        gates = [((p.get('identity_gate') or {}).get('passes')) for p in per.values()]
        ok = all(s is not None and s >= 0.9 for s in sims) and all(g is True for g in gates)
        rows.append({'name': 'held_out_accuracy', 'measured': 'spectral-behaviour similarity ' + ', '.join(f"{l} {_fmt((p.get('behaviour') or {}).get('overall_similarity'))}" for l, p in per.items()) + '; identity gate ' + ', '.join(f"{l} max cosine {_fmt((p.get('identity_gate') or {}).get('max_cosine_to_any_corpus_speaker'))}" for l, p in per.items()),
                     'value': min([s for s in sims if s is not None], default=None), 'threshold': 'similarity ≥ 0.90 and every corpus comparator below cosine 0.40, per language; native-listener rating is a separate human judgement', 'pass': ok, 'class': 'measured', 'receipt': base + '.per_language'})
        rows.append({'name': 'abstention_calibration', 'measured': 'rendered ' + ', '.join(f"{l} {p.get('rendered')}/{p.get('prompts')}" for l, p in per.items()) + ' prompts (a prompt the model could not render is an abstention)', 'value': None, 'threshold': 'reported separately', 'pass': None, 'class': 'measured', 'receipt': base + '.per_language'})
        rows.append({'name': 'latency_p95_ms', 'measured': 'not instrumented for rendering in this iteration', 'value': None, 'threshold': '—', 'pass': None, 'class': None, 'receipt': None})
    else:
        for name in ('held_out_accuracy', 'abstention_calibration', 'latency_p95_ms'):
            rows.append({'name': name, 'measured': f"not measured — run ended {rec['status']}", 'value': None, 'threshold': '—', 'pass': False if name == 'held_out_accuracy' else None, 'class': None, 'receipt': None})
    gpu_h = (rec.get('gpu_seconds') or 0) / 3600
    rows.append({'name': 'cost_actual_vs_estimate', 'measured': f'{gpu_h:.3f} GPU-hours measured; monetary cost unknown (no governed GPU rate card); estimate: none — budget mode uncapped_until_billing', 'value': round(gpu_h, 4),
                 'threshold': 'no numeric cap (owner order, recorded authority)', 'pass': None, 'class': 'measured', 'receipt': f'{jid}#receipt.result.compute' if result.get('compute') else f'{jid}#remote_state.progress.elapsed_s'})
    rows.append({'name': 'refusal_rate_on_out_of_domain', 'measured': 'not instrumented in this lane', 'value': None, 'threshold': '—', 'pass': None, 'class': None, 'receipt': None})
    art = result.get('artefact') or {}
    if art.get('bytes'):
        rows.append({'name': 'adapter_size_mib', 'measured': f"{art['bytes'] / 2 ** 20:.1f} MiB artefact", 'value': round(art['bytes'] / 2 ** 20, 2), 'threshold': 'reported separately', 'pass': None, 'class': 'measured', 'receipt': f'{jid}#receipt.result.artefact.bytes'})
    else:
        rows.append({'name': 'adapter_size_mib', 'measured': 'no artefact size on the record', 'value': None, 'threshold': '—', 'pass': None, 'class': None, 'receipt': None})
    order = {n: i for i, n in enumerate(ACCEPTANCE_CRITERIA_ORDER)}
    return sorted(rows, key=lambda r: order[r['name']])


# ----------------------------------------------------------------------------- sections
def _sec_problem(rec, commission, entries, fx):
    refl = next((e for e in entries if e.get('event_kind') == 'commissioning_reflection'), None)
    if not refl: return f'{SILENT} (no commissioning reflection in the notebook)'
    p = refl.get('payload') or {}; to = p.get('target_outcome') or {}
    fx.add('objective_contract', 'observed', f"wpw://notebook/{rec['commission_id']}/{refl['entry_id']}", f"commissioning reflection recorded {refl.get('at_utc')} before any compute; definition sha {str(p.get('definition_sha256'))[:12]}")
    adm = to.get('admission') or {}
    lane = rec['lane'].replace('_evaluate', '')
    bars = adm.get(lane) if lane in adm else adm
    bar_lines = '\n'.join(f"* {l}: " + ', '.join(f'{k} {v}' for k, v in (b or {}).items()) for l, b in (bars or {}).items()) if isinstance(bars, dict) else SILENT
    return (f"**Commission:** {p.get('title')} (`{rec['commission_id']}`).\n\n**Product:** {commission.get('product')}\n\n**Task:** {to.get('task')} — {to.get('domain')}.\n\n"
            f"**Admission bars for the `{lane}` lane (fixed before training):**\n{bar_lines}\n\n**Gate policy:** {to.get('gate_policy')}\n\n**Metric contract status:** {to.get('metric_contract_status')}\n\n"
            f"**Budget authority:** {p.get('budget_mode')} — recorded authority, not a number.\n\nThis report settles **{rec['lane']} iteration {rec['iteration']}** (job `{rec['job_id']}`).")


def _sec_data(rec, job, aip, requalify, fx):
    jid = rec['job_id']; result = (job.get('receipt') or {}).get('result') or {}
    parts = []
    if aip:
        aid = aip['job_id']
        segs = fx.add('corpus_shape', 'measured', f'{aid}#receipt.result.segments', 'segments and hours per language and split in the AIP database')
        files = fx.add('corpus_files', 'measured', f'{aid}#receipt.result.files', 'recordings read per language')
        if segs:
            lines = ['| Language | Train segments (h) | Dev segments (h) | Admission segments (h) | Recordings read |', '|---|---:|---:|---:|---:|']
            for l, s in segs.items():
                f = (files or {}).get(l) or {}
                lines.append(f"| {l} | {s['train']['segments']:,} ({s['train']['hours']}) | {s['dev']['segments']:,} ({s['dev']['hours']}) | {s['admission']['segments']:,} ({s['admission']['hours']}) | {f.get('read', '—')} of {f.get('files', '—')} |")
            parts.append('\n'.join(lines))
        layers = fx.add('dataset_layers', 'observed', f'{aid}#receipt.result.layers', 'declared dataset layers derived from each recording')
        if layers: parts.append('**Datasets derived from each recording (one file → several queryable layers):** ' + '; '.join(layers) + '.')
        cols = fx.add('feature_columns', 'observed', f'{aid}#receipt.result.feature_columns', 'discoverable-spectrum columns')
        if cols: parts.append(f"**Discoverable-spectrum columns ({len(cols)}):** {', '.join(cols)}.")
        rule = fx.add('split_rule', 'observed', f'{aid}#receipt.result.split_rule', 'split and sealing rule')
        if rule: parts.append(f'**Split rule:** {rule}.')
        parts.append('**Classification-driven exclusions:** raw audio never leaves the host (`raw_media_exported=false`); transcripts stay on the host (`text_exported=false`); presenter identity is a corpus-local cluster id — no voiceprint is stored; the sealed admission split is never read by training.')
        fx.add('custody_flags', 'observed', f'{aid}#receipt.result.raw_media_exported', 'raw media export flag on the database record')
    else:
        fx.refused.append(_refused('corpus_shape', 'malpha_aip_build', 'no completed AIP database build on this host; data statement cannot resolve')); parts.append(SILENT)
    if job: fx.add('database_binding', 'observed', f'{jid}#params.aip_db_dir', 'database path bound to this run')
    if requalify:
        rep = fx.add('dev_requalification', 'measured', f"{requalify['job_id']}#receipt.result.requalification.report", 'dev split before/after requalification, promoted sessions per language')
        if rep: parts.append('**Dev requalification (admission untouched):** ' + '; '.join(f"{l}: {v['before']['segments']} → {v['after']['segments']} segments ({v['after']['mention_segments']} with brand mentions; {v['promoted_sessions']} sessions promoted, `dev_basis=session_holdout`)" for l, v in rep.items()) + '.')
    data = fx.add('run_data', 'measured', f'{jid}#receipt.result.data', 'segments/hours this run trained and evaluated on') if result.get('data') else None
    if data:
        parts.append('**This run read:** ' + ', '.join(f'{k} {v}' for k, v in data.items() if not isinstance(v, dict)) + (f"; per language {data['per_language']}" if isinstance(data.get('per_language'), dict) else '') + '.')
    elif job:
        stage = _walk(job, 'remote_state.stages.data')
        if stage: parts.append('**This run read (from the host state before it ended):** ' + ', '.join(f'{k} {v}' for k, v in stage.items() if k != 'at') + '.'); fx.add('run_data', 'observed', f'{jid}#remote_state.stages.data', 'data stage recorded on the host')
    return '\n\n'.join(parts) if parts else SILENT


def _sec_baseline(rec, job, aip, entries, fx):
    jid = rec['job_id']; lane = rec['lane'].replace('_evaluate', ''); result = (job.get('receipt') or {}).get('result') or {}
    parts = []
    if lane == 'listener':
        base = fx.add('baseline_model', 'observed', f'{jid}#params.recipe.base', 'starting model for the listener')
        if base: parts.append(f'**Starting model:** `{base}` (Whisper family, adapted with added language tokens for Kikuyu and Kikamba; Kiswahili uses the model\'s own `<|sw|>`).\n\n**Licence note:** the record carries no base registration for this model — the record is silent; licence verification is owed before serving.')
    elif lane == 'story_text':
        reg = fx.add('baseline_registration', 'observed', f'{jid}#params.base_registration', 'registered base weights (repo, revision, licence verification, weight sha)')
        if reg: parts.append(f"**Starting model:** `{reg.get('repo')}` revision `{reg.get('revision')}`; licence verified: {_fmt(reg.get('licence_verified'))}; weight sha recorded on the registration.")
        if result.get('base_perplexity'): fx.add('baseline_perplexity', 'measured', f'{jid}#receipt.result.base_perplexity', 'dev perplexity of the untouched base, adapter disabled'); parts.append(f"**Baseline measurement:** dev perplexity of the registered base with the adapter disabled: {result['base_perplexity']}.")
    elif lane == 'story_voice':
        codec = fx.add('codec_provenance', 'observed', f'{jid}#receipt.result.codec_provenance' if result.get('codec_provenance') else f"{aip['job_id']}#receipt.result.codec_provenance" if aip else f'{jid}#params.recipe', 'neural codec repo/revision/codebooks')
        if isinstance(codec, dict) and codec.get('repo'): parts.append(f"**Codec:** `{codec['repo']}` revision `{codec.get('revision')}`, {codec.get('codebooks_used')} codebooks × {codec.get('frame_rate_hz')} Hz = {codec.get('tokens_per_second')} tokens/s; content stream {codec.get('content_stream')}, character stream {codec.get('character_stream')}.")
        parts.append('**Starting model:** none — the codec language model is trained from scratch on the database tokens; there is no pretrained voice and no presenter is cloned (AIP §§6–7). Pretrained MMS-TTS voices exist for Kikuyu and Kiswahili as comparators only; none exists for Kikamba.')
    sel = [e for e in entries if e.get('event_kind') == 'baseline_selection']
    if sel: fx.add('baseline_selection_event', 'measured', f"wpw://notebook/{rec['commission_id']}/{sel[-1]['entry_id']}", f"baseline selection recorded {sel[-1].get('at_utc')}: {(sel[-1].get('payload') or {}).get('what')}")
    return '\n\n'.join(parts) if parts else SILENT


def _sec_method(rec, job, entries, fx):
    jid = rec['job_id']; result = (job.get('receipt') or {}).get('result') or {}
    recipe = fx.add('recipe', 'observed', f'{jid}#params.recipe', 'the recipe this iteration ran')
    parts = []
    if rec['phase'] == 'malpha_evaluate':
        parts.append(f"**Independent admission evaluation** of artefact `{str(rec['params'].get('artefact_sha256'))[:12]}…` (trained by job `{rec['params'].get('trained_job_id')}`) on the sealed, speaker-cluster-disjoint admission split. The seal is re-verified against the database manifest before any audio is read; a mismatch aborts the run.")
        fx.add('evaluated_artefact', 'observed', f'{jid}#params.artefact_sha256', 'artefact digest under evaluation')
    elif recipe:
        parts.append('**Recipe (this iteration):** ' + ', '.join(f'{k} = {v}' for k, v in recipe.items() if k not in ('base_path',)) + '.')
    lane = rec['lane']
    if lane == 'listener': parts.append('**Training:** full fine-tune of the Whisper encoder–decoder with teacher forcing on transcripts, bf16 autocast, AdamW, cosine schedule with warm-up; brand mentions are detected on the decoded text against the fixed lexicon (exact alias match; one edit tolerated for aliases of six or more characters). Dev evaluation runs every `eval_every` steps on a stratified dev sample (all mention-bearing segments up to half the budget, then negatives).')
    if lane == 'story_text': parts.append('**Training:** LoRA adapters on the registered base over per-recording documents (title + transcript), language-tagged prompts; language fidelity is judged by character-trigram profile similarity against each language\'s own training profile; dev perplexity is compared with the base\'s own.')
    if lane == 'story_voice':
        parts.append('**Training:** a codec language model (text characters → delayed Mimi frames, eight codebooks) trained from scratch. Rendered dev prompts are measured with the same discoverable-spectrum columns as the corpus; the per-feature divergence between generated and baseline distributions is the spectral-behaviour similarity, and where it is shifted the next curriculum up-weights the under-covered side of that feature (spectral feedback). The identity gate embeds each rendering and requires its cosine to every corpus-derived speaker comparator to stay below the threshold; comparators live in memory only.')
        if result.get('spectral_feedback'): fx.add('spectral_feedback', 'measured', f'{jid}#receipt.result.spectral_feedback', f"feedback {'on' if result['spectral_feedback'].get('enabled') else 'off'}; {len(result['spectral_feedback'].get('log') or [])} re-weighting events")
    ideas = [e for e in entries if e.get('event_kind') == 'cif_ideation' and e.get('run_artefact_ref') == f'm9_training://run_log/{jid}']
    if ideas:
        lines = ['**Adopted ideation events (mirrored by reference, WPW-6):**']
        for e in ideas:
            p = e.get('payload') or {}
            lines.append(f"* `{p.get('cif_event_ref')}` · idea `{p.get('idea_ref')}` · conditions `{p.get('conditions_ref')}` · {p.get('adoption_status')} (attempt {p.get('attempt')}).")
            fx.add(f"ideation_{e['entry_id']}", 'observed', f"wpw://notebook/{rec['commission_id']}/{e['entry_id']}", f"ideation record {p.get('idea_ref')} adopted")
        parts.append('\n'.join(lines))
    else: parts.append('**Adopted ideation events:** _the record is silent — no cif_ideation entry references this run._')
    return '\n\n'.join(parts) if parts else SILENT


def _sec_setup(rec, job, fx):
    jid = rec['job_id']; result = (job.get('receipt') or {}).get('result') or {}; parts = []
    host = fx.add('host_binding', 'observed', f'{jid}#host', 'host that ran the job')
    gpu = fx.add('gpu_index', 'observed', f'{jid}#params.gpu_index', 'device index on the host')
    comp = fx.add('compute', 'measured', f'{jid}#receipt.result.compute', 'wall seconds, GPU seconds, peak memory, device name') if result.get('compute') else None
    if comp: parts.append(f"**Hardware:** {host} GPU {gpu} — {comp.get('device', 'device name not recorded')}; peak memory {_fmt(comp.get('gpu_peak_gb'), 2)} GB.\n\n**Duration:** {_fmt(comp.get('wall_seconds'), 1)} s wall, {_fmt(comp.get('gpu_hours'), 4)} GPU-hours.")
    else:
        el = fx.add('elapsed', 'measured', f'{jid}#remote_state.progress.elapsed_s', 'elapsed seconds observed on the host before the run ended')
        parts.append(f"**Hardware:** {host} GPU {gpu}.\n\n**Duration:** {_fmt(el)} s observed on the host before the run ended." if el is not None else f'**Hardware:** {host} GPU {gpu}.\n\n**Duration:** {SILENT}')
    parts.append(f"**Cost actual against estimate:** {(rec.get('gpu_seconds') or 0) / 3600:.3f} GPU-hours measured. Estimate: none — the run was commissioned under `uncapped_until_billing` (owner order), no governed GPU rate card exists, so money is not invented; WPW-18 observation line therefore has no base and is recorded as silent.")
    fx.add('budget_mode', 'observed', f'{jid}#params.budget_mode', 'budget authority bound to the job')
    seed = fx.add('seed', 'observed', f'{jid}#params.seed', 'seed bound to the job')
    code = fx.add('worker_bundle', 'observed', f'{jid}#code_sha256', 'sha256 of the hashed worker bundle executed on the host')
    parts.append(f"**Seed:** {seed}.\n\n**Worker bundle:** `{str(code)[:16]}…` (hashed, receipted on the host; digest verified at settlement: {_fmt((job.get('receipt') or {}).get('digest_verified'))}).\n\n**Iteration / attempt:** iteration {rec['iteration']}" + (f", resumed from `{rec['params']['resume_from']}`" if rec['params'].get('resume_from') else '') + '.')
    return '\n\n'.join(parts)


def _sec_results(rec, job, crit, fx):
    lines = ['| Criterion | Measured | Threshold | Pass |', '|---|---|---|---|']
    for c in crit:
        if c['receipt']:
            ok = fx.add(f"criterion_{c['name']}", c['class'], c['receipt'], f"{c['name']}: {c['measured'][:120]}")
            measured = c['measured'] if ok is not None else '_the record is silent (receipt did not resolve)_'
        else: measured = c['measured']
        lines.append(f"| `{c['name']}` | {measured} | {c['threshold']} | {'✅' if c['pass'] is True else '❌' if c['pass'] is False else '— (reported, not gated)'} |")
    body = '\n'.join(lines)
    result = (job.get('receipt') or {}).get('result') or {}
    where = 'sealed admission split (speaker-cluster-disjoint; first and only read of this artefact unless recorded otherwise)' if rec['phase'] == 'malpha_evaluate' else 'dev split (iteration feedback; the sealed admission split is read only by the independent evaluation)'
    body += f"\n\n**Held-out material:** {where}. `sealed_admission_read` = {_fmt(result.get('sealed_admission_read'))}."
    det = next((c.get('detail') for c in crit if c.get('detail')), None)
    if det: body += f"\n\n**Per language:** {det}."
    if rec['phase'] == 'malpha_evaluate' and result.get('verdict'):
        fx.add('admission_verdict', 'measured', f"{rec['job_id']}#receipt.result.verdict", 'per-language verdict on the sealed split')
        body += '\n\n| Language | Mention precision | Mention recall | WER | Meets target |\n|---|---:|---:|---:|---|\n' + '\n'.join(f"| {l} | {_fmt(v.get('mention_precision'))} | {_fmt(v.get('mention_recall'))} | {_fmt(v.get('wer'))} | {_fmt(v.get('meets_target'))} |" for l, v in result['verdict'].items())
    if result.get('history'):
        fx.add('learning_curve', 'measured', f"{rec['job_id']}#receipt.result.history", f"{len(result['history'])} dev evaluations during training")
        body += f"\n\n**Learning curve:** {len(result['history'])} dev evaluations recorded (steps " + ', '.join(str(h.get('step')) for h in result['history']) + ').'
    return body


def _sec_ablations(rec, job, fx):
    return '_No ablations were run in this settlement._ The controlled same-base comparison of spectral-feedback curricula (MA-16) is a separate commission and is not claimed here.'


def _sec_limitations(rec, job, commission, aip, crit):
    lane = rec['lane'].replace('_evaluate', ''); result = (job.get('receipt') or {}).get('result') or {}; lims = []
    if rec['phase'] != 'malpha_evaluate': lims.append('Results are on the dev split, which guides iteration; they are not admission evidence. Admission is decided only on the sealed, speaker-cluster-disjoint split by a separate evaluation run.')
    if (commission or {}).get('aip_dev_requalified'): lims.append('The dev split was requalified after the cluster-disjoint rule left it too small to measure: whole train sessions were promoted to dev (`dev_basis=session_holdout`), so presenter voices may overlap between train and dev. This is a disclosed selection effect on dev; the admission split is unchanged.')
    if lane == 'listener':
        dev = result.get('evaluation') if rec['phase'] == 'malpha_evaluate' else result.get('dev')
        if dev:
            small = [f"{l} ({(m or {}).get('segments_with_mentions')} mention segments)" for l, m in (dev.get('mentions') or {}).items() if ((m or {}).get('segments_with_mentions') or 0) < 100]
            if small: lims.append('Mention precision and recall rest on few mention-bearing segments: ' + ', '.join(small) + '. Intervals are wide; a brand list from RMS traffic logs would sharpen them.')
        lims.append(f"Brand mentions are detected against a fixed lexicon of {len(rec['params'].get('brand_lexicon') or []) or 'the recorded number of'} brands and aliases; brands outside it are not measured. Timestamps are attributed at transcript-segment granularity.")
    if lane == 'story_text': lims.append('Language fidelity is a character-trigram judgement against each language\'s own profile; it is not a reading of meaning or story quality, which only native readers can judge.')
    if lane == 'story_voice':
        lims.append('Spectral-behaviour similarity is an instrument, not naturalness: a rendering can match the corpus distributions and still sound wrong. Native-listener ratings on unseen stories are required and are recorded as pending.')
        lims.append('The identity gate is scoped to corpus-derived speaker representations of this estate; it is not a claim of global uniqueness over all humans.')
        lims.append('No pretrained Kikamba voice exists as a comparator; the Kikamba baseline is the corpus distribution alone.')
    exp = (commission or {}).get('evaluation_exposure') or {}
    if exp: lims.append('Evaluation exposure of the sealed split so far: ' + ', '.join(f'artefact {k}…: {v} read(s)' for k, v in exp.items()) + '.')
    lims.append('Monetary cost is not stated: GPU-hours are measured, no governed rate card exists, and the owner authority is uncapped until billing.')
    return '\n'.join(f'* {x}' for x in lims) if lims else SILENT


def _sec_negative(rec, job, crit, previous):
    neg = []
    if rec['status'] != 'completed':
        err = ((job.get('receipt') or {}).get('error') or {})
        neg.append(f"**Run ended `{rec['status']}`.** {rec.get('reason') or err.get('message') or 'reason not on record'}" + (f" — `{err.get('type')}`" if err.get('type') else '') + f". Retained checkpoint: `{rec.get('last_checkpoint') or 'none'}`.")
    held = next((c for c in crit if c['name'] == 'held_out_accuracy'), None)
    if held and held['pass'] is False and rec['status'] == 'completed': neg.append(f"**Admission bar not met on this material.** {held['measured']}. Threshold: {held['threshold']}.")
    if previous and (previous.get('result') or {}).get('dev') and (job.get('receipt') or {}).get('result', {}).get('dev'):
        from services.training_lab import malpha
        lane = rec['lane']; before, after = malpha._summary(lane, previous['result']), malpha._summary(lane, job['receipt']['result'])
        worse = []
        for l in after:
            for k, v in (after[l] or {}).items():
                b = (before.get(l) or {}).get(k)
                if isinstance(v, (int, float)) and isinstance(b, (int, float)) and not isinstance(v, bool):
                    if (k in ('wer', 'dev_perplexity') and v > b) or (k not in ('wer', 'dev_perplexity') and v < b): worse.append(f'{l} {k} {b} → {v}')
        if worse: neg.append(f"**Regressions against iteration {previous['iteration']}:** " + '; '.join(worse) + '.')
    return '\n\n'.join(neg) if neg else SILENT


# ----------------------------------------------------------------------------- draft
def draft(job_id):
    from services.training_lab import malpha
    from services.training_runner import m9_dispatch
    rec = malpha.job_detail(job_id)
    if not rec: raise LookupError('no Mα job with that reference')
    job = m9_dispatch.load_job(job_id) or {}
    commission = malpha.commission(rec['commission_id']) or {}
    entries = nb.list_entries(rec['commission_id'])
    aip = next((j for j in malpha.jobs(phase='malpha_aip_build', host=rec['host'], status='completed')), None)
    requalify = next((j for j in malpha.jobs(phase='malpha_aip_requalify', host=rec['host'], status='completed')), None)
    previous = next((j for j in reversed(malpha.jobs(commission_id=rec['commission_id'], lane=rec['lane'], status='completed')) if j['iteration'] < rec['iteration']), None)
    fx = _Figures(); crit = _criteria(rec, job)
    sections = {
        'problem_and_objective': _sec_problem(rec, commission, entries, fx), 'data_statement': _sec_data(rec, job, aip, requalify, fx), 'baseline_record': _sec_baseline(rec, job, aip, entries, fx),
        'method': _sec_method(rec, job, entries, fx), 'setup_and_reproducibility': _sec_setup(rec, job, fx), 'results_on_held_out': _sec_results(rec, job, crit, fx),
        'ablations': _sec_ablations(rec, job, fx), 'limitations': _sec_limitations(rec, job, commission, aip, crit), 'negative_results': _sec_negative(rec, job, crit, previous)}
    held = next(c for c in crit if c['name'] == 'held_out_accuracy')
    result = (job.get('receipt') or {}).get('result') or {}
    accepted = rec['status'] == 'completed' and (held['pass'] is True or bool(result.get('admitted_all_languages')))
    refusal = None if accepted else (f"run ended {rec['status']}: {str(rec.get('reason'))[:200]}" if rec['status'] != 'completed' else f"admission bar not met: {held['measured'][:300]}")
    body = [f"# Tier 2 Technical Report · {commission.get('title', rec['commission_id'])} · {rec['lane']} iteration {rec['iteration']} ({job_id})", '', INTERNAL_ONLY_MARKER, '',
            f"**Settlement:** {'accepted' if accepted else 'refused'}" + (f" — {refusal}" if refusal else '') + ' · **Spec:** whitepaper_wizard_spec_v1 · WPW-8..10.', '']
    for i, name in enumerate(SECTION_SKELETON, 1):
        body += [f'## {i} · {SECTION_TITLES[name]}', '', sections[name], '']
    if fx.figures:
        body += ['## Figures (WPW-9)', '', '| # | evidence_class | receipt_line | summary |', '|---|---|---|---|'] + [f"| {i} · `{f['figure_id']}` | {f['evidence_class']} | `{f['receipt_line']}` | {f['summary_text']} |" for i, f in enumerate(fx.figures, 1)] + ['']
    if fx.refused:
        body += ['## Refused figures (WPW-9)', ''] + [f"* `{f['figure_id']}` · receipt_line=`{f['receipt_line']}` · reason: {f['reason']}" for f in fx.refused] + ['']
    body.append(INTERNAL_ONLY_MARKER)
    return {'metadata': {'run_id': job_id, 'commission_id': rec['commission_id'], 'lane': rec['lane'], 'iteration': rec['iteration'], 'tier': 2, 'internal_only': True, 'settlement': 'accepted' if accepted else 'refused', 'refusal_reason': refusal,
                         'status': rec['status'], 'spec_ref': 'whitepaper_wizard_spec_v1 · WPW-8..10', 'drafted_at': datetime.now(timezone.utc).isoformat(), 'figures_total': len(fx.figures) + len(fx.refused), 'figures_resolved': len(fx.figures)},
            'sections': {k: {'body': v} for k, v in sections.items()}, 'criteria': crit, 'figures': fx.figures, 'refused_figures': fx.refused, 'body': '\n'.join(body)}


# ----------------------------------------------------------------------------- settlement: store, then land in Documents
def collection():
    from services.training_lab import malpha
    col = malpha.db().malpha_tier2_reports; col.create_index('job_id', unique=True); return col


def settle_report(job_id, principal_id='akki-autopilot'):
    report = draft(job_id)
    doc = {'job_id': job_id, **report['metadata'], 'report': report, 'documents': None}
    try:
        from services.transform_forms.doc_studio import service as studio
        record, created = studio.create_from_producer('malpha-tier2', job_id, TENANT, principal_id)
        if created or not record.get('builds'): record = studio.build(TENANT, record['commission_id'], principal_id)
        doc['documents'] = {'commission_id': record['commission_id'], 'release': record.get('release'), 'builds': len(record.get('builds') or []), 'created': created}
    except Exception as exc:
        log.exception('tier2 documents landing failed for %s', job_id)
        doc['documents'] = {'error': repr(exc)[:300]}
    collection().replace_one({'job_id': job_id}, doc, upsert=True)
    return {**report, 'documents': doc['documents']}


def get_report(job_id):
    if not re.fullmatch(r'm9j-[a-f0-9]{12}', job_id or ''): return None
    return collection().find_one({'job_id': job_id}, {'_id': 0})


def list_reports(commission_id=None):
    q = {'commission_id': commission_id} if commission_id else {}
    return list(collection().find(q, {'_id': 0, 'report': 0}, sort=[('drafted_at', -1)]))
