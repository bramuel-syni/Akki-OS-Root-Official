"""Mα storyteller lanes on the GPU host. Text lane: LoRA on a registered Qwen3 base turns the per-language transcripts into a story model with
held-out perplexity and language-fidelity checks. Voice lane: a codec language model trained from scratch on the AIP Mimi tokens (text → content
and character streams), rendered through the same codec; generated speech is measured with the same discoverable-spectrum columns as the
corpus so baseline-versus-generated behaviour is a number per language and feature, that divergence re-weights the next curriculum
(spectral feedback), and an invented-identity gate keeps the voice at a measured distance from every corpus-derived speaker representation.
Comparator embeddings live in memory for the gate only and are destroyed with the process."""
import hashlib
import json
import math
import random
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from services.training_lab.malpha_worker_policy import balanced_weights, rendered_identity_gate, story_score

from services.training_lab.malpha_worker import (
    CODE_BOS,
    CODE_EOS,
    CODE_PAD,
    CODE_VOCAB,
    FEATURES,
    LANG_NAMES,
    MIMI_CODEBOOKS,
    MIMI_FRAME_HZ,
    SR16,
    SR24,
    PcmStore,
    _save_ckpt,
    gpu_lock,
    load_mimi,
    load_rows,
    lr_at,
    mimi_decode,
    normalise_text,
    now,
    percentiles,
    resample,
    spectrum_features,
)


# ----------------------------------------------------------------------------- language fidelity without a labelled judge: character trigram profiles
def trigram_profile(texts, top=3000):
    c = Counter()
    for t in texts:
        t = f' {normalise_text(t)} '
        c.update(t[i:i + 3] for i in range(len(t) - 2))
    total = sum(c.values()) or 1
    return {k: v / total for k, v in c.most_common(top)}


def profile_cosine(a, b):
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys); na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def distinct_n(text, n=2):
    w = normalise_text(text).split()
    grams = [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]
    return round(len(set(grams)) / len(grams), 4) if grams else 0.0


def _documents(rows, lang):
    by_file = defaultdict(list)
    for r in rows: by_file[(r['session'], r['file'])].append(r)
    docs = []
    for (session, file), segs in by_file.items():
        segs.sort(key=lambda r: r['start']); text = ' '.join(s['text'] for s in segs if s['text']).strip()
        title = re.sub(r'^rms_\d{4}_[a-z]{3}_[a-z]{2}_', '', session).replace('_', ' ').strip(' -+') or 'untitled'
        if len(text) > 200: docs.append({'lang': lang, 'title': title, 'text': text, 'split': segs[0]['split'], 'session': session})
    return docs


def _prompt(lang, title):
    return f"<|lang|>{lang} ({LANG_NAMES.get(lang, lang)})\n<|title|>{title}\n<|story|>\n"


def story_text_train(control, state):
    import numpy as np
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    lock = gpu_lock(control); device = 'cuda'; started = time.time()
    aip = Path(control['aip_db_dir']); langs = list(control['languages']); recipe = dict(control['recipe']); job_dir = Path(control['job_dir'])
    ckpt_dir = job_dir / 'checkpoints'; ckpt_dir.mkdir(exist_ok=True)
    docs = []
    for lang in langs: docs.extend(_documents(load_rows(aip, lang, with_text=True, splits=('train', 'dev')), lang))
    train = [d for d in docs if d['split'] == 'train']; dev = [d for d in docs if d['split'] == 'dev']
    profiles = {lang: trigram_profile([d['text'] for d in train if d['lang'] == lang]) for lang in langs}
    state.stage('data', {'train_documents': len(train), 'dev_documents': len(dev), 'per_language': {l: {'train': sum(1 for d in train if d['lang'] == l), 'dev': sum(1 for d in dev if d['lang'] == l)} for l in langs}, 'admission_read': False})
    tokenizer = AutoTokenizer.from_pretrained(recipe['base_path']); tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(recipe['base_path'], torch_dtype=torch.bfloat16).to(device)
    model.gradient_checkpointing_enable(); model.config.use_cache = False
    if recipe.get('init_adapter'): model = PeftModel.from_pretrained(model, recipe['init_adapter'], is_trainable=True)
    else: model = get_peft_model(model, LoraConfig(r=int(recipe.get('lora_r', 32)), lora_alpha=int(recipe.get('lora_alpha', 64)), lora_dropout=float(recipe.get('lora_dropout', 0.05)), target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], task_type='CAUSAL_LM'))
    max_len = int(recipe.get('max_seq_len', 1024))
    n_samples, patience = int(recipe.get('eval_samples_per_language', 2)), int(recipe.get('patience_evaluations', 0))  # patience 0 = run to max_steps (earlier recipes)

    def chunks(doc_list):
        out = []
        for d in doc_list:
            head = tokenizer(_prompt(d['lang'], d['title']), add_special_tokens=False).input_ids
            body = tokenizer(d['text'], add_special_tokens=False).input_ids + [tokenizer.eos_token_id]
            if len(head) >= max_len - 8: head = head[:max_len // 4]
            room = max_len - len(head)
            for i in range(0, len(body), room): out.append((d['lang'], head + body[i:i + room]))
        return out
    train_chunks, dev_chunks = chunks(train), chunks(dev)
    from services.training_lab.malpha_evaluation import fingerprint
    panel = {l: [d['title'] for d in sorted(dev, key=lambda d: (d['lang'], d['session'], d['title'])) if d['lang'] == l][:n_samples] for l in langs}
    if any(not panel[l] for l in langs): raise ValueError('REAL_DEVELOPMENT_PROMPTS_REQUIRED_FOR_EVERY_LANGUAGE')
    evaluation_protocol = {'version': 'malpha-story-eval-v2', 'prompt_panel_sha256': fingerprint(panel),
        'prompts_per_language': {l: len(panel[l]) for l in langs}, 'sample_seed': int(control['seed']),
        'perplexity_definition': 'token-weighted causal NLL over first64 registered dev chunks per language; includes prompt tokens; naturalness NOT measured',
        'dev_tokens_sha256': fingerprint(dev_chunks), 'max_new_tokens': 320, 'temperature': .8, 'top_p': .95}
    state.stage('evaluation_protocol', evaluation_protocol)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(recipe['lr']), weight_decay=float(recipe.get('weight_decay', 0.0)))
    batch, accum, max_steps, warmup = int(recipe['batch_size']), int(recipe.get('grad_accum', 1)), int(recipe['max_steps']), int(recipe.get('warmup_steps', 100))
    ckpt_every, eval_every = int(recipe.get('checkpoint_every', 200)), int(recipe.get('eval_every', 500))
    step, history = 0, []
    if control.get('resume_from') and Path(control['resume_from']).exists():
        ck = torch.load(control['resume_from'], map_location='cpu'); model.load_state_dict(ck['model'], strict=False); optimizer.load_state_dict(ck['optimizer']); step = int(ck['step']); history = ck.get('history', [])
    rng = random.Random(int(control['seed']) + step)

    def collate(items):
        width = max(len(x) for _, x in items)
        ids = torch.full((len(items), width), tokenizer.pad_token_id, dtype=torch.long); labels = torch.full((len(items), width), -100, dtype=torch.long)
        for i, (_, x) in enumerate(items): ids[i, :len(x)] = torch.tensor(x); labels[i, :len(x)] = torch.tensor(x)
        return ids.to(device), labels.to(device)

    def perplexity(lang):
        model.eval(); nll, n = 0.0, 0
        items = [c for c in dev_chunks if c[0] == lang][:64]
        with torch.no_grad():
            for i in range(0, len(items), batch):
                ids, labels = collate(items[i:i + batch]); out = model(input_ids=ids, labels=labels)
                tokens = int((labels[:, 1:] != -100).sum()); nll += float(out.loss) * tokens; n += tokens
        model.train()
        return round(math.exp(nll / n), 3) if n else None

    def generate(lang, title, max_new=320):
        model.eval(); ids = tokenizer(_prompt(lang, title), return_tensors='pt').input_ids.to(device)
        with torch.no_grad():
            out = model.generate(ids, max_new_tokens=max_new, do_sample=True, temperature=0.8, top_p=0.95, repetition_penalty=1.15, pad_token_id=tokenizer.pad_token_id)
        model.train()
        return tokenizer.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()

    def evaluation():
        ev = {'step': step, 'at': now(), 'per_language': {}, 'evaluation_protocol': evaluation_protocol}
        for lang in langs:
            titles = panel[lang]; samples, local_samples = [], []
            for index, t in enumerate(titles):
                with torch.random.fork_rng(devices=[torch.cuda.current_device()]):
                    torch.manual_seed(int(control['seed']) + langs.index(lang)*1000 + index)
                    text = generate(lang, t)
                sims = {l: round(profile_cosine(trigram_profile([text]), profiles[l]), 4) for l in langs}
                sample = {'prompt_sha256': hashlib.sha256(_prompt(lang, t).encode()).hexdigest(), 'chars': len(text), 'words': len(text.split()), 'distinct_2': distinct_n(text), 'trigram_similarity': sims, 'language_fidelity': bool(text.strip()) and max(sims, key=sims.get) == lang, 'excerpt_sha256': hashlib.sha256(text.encode()).hexdigest()}
                samples.append(sample); local_samples.append({**sample, 'title': t, 'text': text})
            (job_dir / f'samples_{lang}_step{step}.json').write_text(json.dumps({'samples': local_samples, 'evaluation_protocol': evaluation_protocol, 'custody': 'estate_only'}, ensure_ascii=False, indent=1))
            ppl = perplexity(lang); base = (base_perplexity or {}).get(lang)
            ev['per_language'][lang] = {'dev_perplexity': ppl, 'base_perplexity': base, 'dev_perplexity_below_base': (ppl is not None and base is not None and ppl < base) if base is not None else None,
                                        'language_fidelity_rate': round(sum(s['language_fidelity'] for s in samples) / len(samples), 3), 'mean_distinct_2': round(sum(s['distinct_2'] for s in samples) / len(samples), 4), 'samples': samples}
        return ev
    # the registered base's own dev perplexity is the baseline the admission contract compares against; measured with the adapter disabled, carried by reference afterwards
    def _base_perplexity():
        with model.disable_adapter(): return {lang: perplexity(lang) for lang in langs}
    base_perplexity = _base_perplexity()
    if base_perplexity: state.stage('base_perplexity', base_perplexity)
    art = job_dir / 'artefact'

    def score(ev):
        return story_score(ev)

    def save_adapter():
        model.save_pretrained(art / 'lora_adapter'); tokenizer.save_pretrained(art / 'lora_adapter')
    model.train(); losses = []; best, since_best, stopped_by = None, 0, 'max_steps'
    by_lang = {l: [c for c in train_chunks if c[0] == l] for l in langs}; balance = bool(recipe.get('language_balance', False))
    micro = 0
    while step < max_steps and stopped_by == 'max_steps':
        # language-balanced sampling (recipe) draws each micro-batch from one language chosen uniformly, so a small language is not out-voted by the large ones
        pool = (by_lang[rng.choice(langs)] or train_chunks) if balance else train_chunks
        ids, labels = collate([pool[rng.randrange(len(pool))] for _ in range(batch)])
        loss = model(input_ids=ids, labels=labels).loss / accum; loss.backward(); losses.append(float(loss) * accum); micro += 1
        if micro % accum: continue
        for g in optimizer.param_groups: g['lr'] = lr_at(step, max_steps, float(recipe['lr']), warmup)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
        if step % 10 == 0:
            state.update(progress={'stage': 'training', 'step': step, 'of': max_steps, 'loss': round(float(np.mean(losses[-50:])), 4), 'elapsed_s': int(time.time() - started), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                                   'last_checkpoint_step': (step // ckpt_every) * ckpt_every, 'next_checkpoint_step': (step // ckpt_every + 1) * ckpt_every, 'best_step': best['step'] if best else None})
        if step % ckpt_every == 0: _save_ckpt(ckpt_dir / 'latest.pt', model, optimizer, step, {'history': history})
        if step % eval_every == 0 or step == max_steps:
            ev = evaluation(); ev['train_loss'] = round(float(np.mean(losses[-100:])), 4); history.append(ev); s = score(ev)
            if s is not None and (best is None or s > best['score']): best, since_best = {'score': s, 'step': step, 'eval': ev}, 0; save_adapter()
            else: since_best += 1
            state.stage(f'dev_eval_step_{step}', {l: {k: v[k] for k in ('dev_perplexity', 'base_perplexity', 'dev_perplexity_below_base', 'language_fidelity_rate', 'mean_distinct_2')} for l, v in ev['per_language'].items()} | {'_score': list(s) if s else None, '_best_step': best['step'] if best else None, '_selection': 'worst-language fidelity first, perplexity tie-break'})
            if best and patience and since_best >= patience: stopped_by = f'patience ({patience} evaluations without improved language-first score; best at step {best["step"]})'
    if best is None: save_adapter()  # no dev perplexity could be measured: the final adapter is the artefact, stated as such
    digest = hashlib.sha256(); nbytes = 0
    for f in sorted(p for p in (art / 'lora_adapter').rglob('*') if p.is_file()): digest.update(f.read_bytes()); nbytes += f.stat().st_size
    lock.close()
    reported = best['eval'] if best else (history[-1] if history else None)
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'lane': 'story_text', 'recipe': recipe, 'languages': langs, 'data': state.doc['stages']['data'], 'steps': step, 'base_perplexity': base_perplexity,
            'dev': reported, 'best_step': best['step'] if best else None, 'stopped_by': stopped_by, 'artefact_is': 'adapter at best worst-language fidelity, then perplexity' if best else 'final adapter (complete dev score unavailable)',
            'history': [{'step': h['step'], 'train_loss': h.get('train_loss'), 'per_language': {l: {k: v[k] for k in ('dev_perplexity', 'base_perplexity', 'dev_perplexity_below_base', 'language_fidelity_rate', 'mean_distinct_2')} for l, v in h['per_language'].items()}} for h in history],
            'artefact': {'path': str(art / 'lora_adapter'), 'sha256': digest.hexdigest(), 'bytes': nbytes, 'base': recipe['base_path']},
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)},
            'sealed_admission_read': False, 'training_started': True, 'raw_media_exported': False, 'text_exported': False}


# ----------------------------------------------------------------------------- voice: codec language model over Mimi tokens
def build_voice_model(text_vocab, d_model, layers, heads, max_frames, identity_dim=0, dense_identity=False):
    import torch
    from torch import nn

    class VoiceLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.text_emb = nn.Embedding(text_vocab, d_model); self.audio_emb = nn.ModuleList([nn.Embedding(CODE_VOCAB, d_model) for _ in range(MIMI_CODEBOOKS)])
            self.pos = nn.Embedding(max_frames + 512, d_model); self.kind = nn.Embedding(3, d_model)
            self.spk_proj = nn.Linear(identity_dim, d_model) if identity_dim else None  # one identity prefix token: the voice is a conditioning input, never a corpus speaker baked into the weights
            layer = nn.TransformerEncoderLayer(d_model, heads, 4 * d_model, dropout=0.1, activation='gelu', batch_first=True, norm_first=True)
            self.body = nn.TransformerEncoder(layer, layers); self.norm = nn.LayerNorm(d_model)
            self.heads = nn.ModuleList([nn.Linear(d_model, CODE_VOCAB) for _ in range(MIMI_CODEBOOKS)])

        def forward(self, text_ids, codes_in, spk=None):
            """text_ids (B, Lt), codes_in (B, 8, T) delayed inputs, spk (B, D) identity → logits (8, B, T, V) for the next delayed frame."""
            B, Lt = text_ids.shape; T = codes_in.shape[2]
            t = self.text_emb(text_ids) + self.kind.weight[0]; a = sum(self.audio_emb[k](codes_in[:, k]) for k in range(MIMI_CODEBOOKS)) + self.kind.weight[1]
            if dense_identity and self.spk_proj is not None and spk is not None:
                a = a + self.spk_proj(spk)[:, None]
            parts = [t, a]; Lp = 0
            if self.spk_proj is not None and spk is not None: parts.insert(0, self.spk_proj(spk)[:, None] + self.kind.weight[2]); Lp = 1
            x = torch.cat(parts, 1) + self.pos(torch.arange(Lp + Lt + T, device=text_ids.device))[None]
            mask = torch.triu(torch.full((Lp + Lt + T, Lp + Lt + T), float('-inf'), device=x.device), 1)
            mask[:Lp + Lt, :Lp + Lt] = 0  # identity and text prompt attend to themselves fully; audio frames are causal
            padding = torch.cat([torch.zeros((B, Lp), dtype=torch.bool, device=x.device), text_ids == 0,
                                 (codes_in == CODE_PAD).all(1)], dim=1)
            h = self.norm(self.body(x, mask=mask, src_key_padding_mask=padding))[:, Lp + Lt:Lp + Lt + T]
            return torch.stack([head(h) for head in self.heads])
    return VoiceLM()


def delay(codes):
    """MusicGen-style delay: codebook k is shifted right by k frames; inputs begin with a BOS frame and targets end with EOS on every codebook."""
    import torch
    K, T = codes.shape; width = T + K
    inp = torch.full((K, width), CODE_PAD, dtype=torch.long); tgt = torch.full((K, width), -100, dtype=torch.long)
    for k in range(K):
        inp[k, 1 + k:1 + k + T] = codes[k]; tgt[k, k:k + T] = codes[k]; tgt[k, k + T] = CODE_EOS
    inp[:, 0] = CODE_BOS
    return inp, tgt


def undelay(frames):
    """frames (K, W) generated delayed frames → codes (K, T)."""
    K, W = frames.shape; T = W - K
    import torch
    return torch.stack([frames[k, k:k + T] for k in range(K)]) if T > 0 else frames[:, :0]


MAX_TEXT_CHARS = 400  # normalised characters per segment prompt; longer transcripts on a ≤12 s segment are misaligned and are excluded, not truncated silently
ECAPA_DIM = 192  # speechbrain/spkrec-ecapa-voxceleb representation width (temporary identity representations and the invented identity live in this space)


class TextCodec:
    def __init__(self, texts, langs):
        chars = sorted({c for t in texts for c in normalise_text(t)})
        self.itos = ['<pad>', '<bos>', '<eos>'] + [f'<{l}>' for l in langs] + chars; self.stoi = {s: i for i, s in enumerate(self.itos)}

    def encode(self, lang, text):
        return [1, self.stoi[f'<{lang}>']] + [self.stoi[c] for c in normalise_text(text)[:MAX_TEXT_CHARS] if c in self.stoi] + [2]


def _resample(y, src, dst):
    return resample(y, src, dst)


def behaviour_divergence(baseline_rows, generated_feats):
    """Per feature: standardized mean difference and normalised 1-D Wasserstein distance of generated versus baseline; similarity in (0,1]."""
    import numpy as np
    out = {}
    for f in FEATURES:
        if f in ('duration_s', 'chars_per_s'): continue
        base = np.array([r['features'][f] for r in baseline_rows if r['features'].get(f) is not None], dtype=float)
        gen = np.array([g[f] for g in generated_feats if g.get(f) is not None], dtype=float)
        if len(base) < 10 or len(gen) < 3: continue
        std = base.std() or 1e-6
        qs = np.linspace(0.02, 0.98, 25); w = float(np.abs(np.quantile(base, qs) - np.quantile(gen, qs)).mean() / std)
        out[f] = {'baseline_p50': round(float(np.median(base)), 3), 'generated_p50': round(float(np.median(gen)), 3), 'standardized_mean_diff': round(float((gen.mean() - base.mean()) / std), 3),
                  'wasserstein_norm': round(w, 3), 'similarity': round(float(math.exp(-w)), 4)}
    overall = round(float(np.mean([v['similarity'] for v in out.values()])), 4) if out else None
    return {'features': out, 'overall_similarity': overall}


def curriculum_weights(train_rows, divergence, alpha=0.6, floor=0.3):
    """Spectral feedback: where generated behaviour is shifted from the baseline, segments on the under-covered side are weighted up for the next pass."""
    import numpy as np
    w = np.ones(len(train_rows))
    applied = {}
    for f, d in (divergence.get('features') or {}).items():
        smd = d['standardized_mean_diff']
        if abs(smd) < 0.3: continue
        vals = np.array([r['features'].get(f) if r['features'].get(f) is not None else np.nan for r in train_rows], dtype=float)
        mu, sd = np.nanmean(vals), np.nanstd(vals) or 1e-6
        z = np.nan_to_num((vals - mu) / sd)
        w *= np.clip(1 + alpha * (-np.sign(smd)) * z, floor, 3.0); applied[f] = {'direction': 'up-weight lower values' if smd > 0 else 'up-weight higher values', 'smd': smd}
    w = w / w.mean()
    return w, applied


def voice_train(control, state):
    import numpy as np
    import torch
    lock = gpu_lock(control); device = 'cuda'; started = time.time()
    aip = Path(control['aip_db_dir']); langs = list(control['languages']); recipe = dict(control['recipe']); job_dir = Path(control['job_dir'])
    ckpt_dir = job_dir / 'checkpoints'; ckpt_dir.mkdir(exist_ok=True); seed = int(control['seed'])
    rows = []
    for lang in langs:
        for r in load_rows(aip, lang, with_text=True, splits=('train', 'dev')): r['language'] = lang; rows.append(r)
    tokens = {}
    for lang in langs: tokens.update(torch.load(aip / f'tokens_{lang}.pt'))
    max_s = float(recipe.get('max_segment_seconds', 12.0)); max_T = int(max_s * MIMI_FRAME_HZ) + 2; max_frames = max_T + MIMI_CODEBOOKS + 2
    eligible = [r for r in rows if r['seg_id'] in tokens and r['text'] and r['features']['duration_s'] <= max_s]
    overlong = [r for r in eligible if len(normalise_text(r['text'])) > MAX_TEXT_CHARS]
    eligible = [r for r in eligible if len(normalise_text(r['text'])) <= MAX_TEXT_CHARS]
    train = [r for r in eligible if r['split'] == 'train']
    dev = [r for r in eligible if r['split'] == 'dev' and r['features']['duration_s'] >= 2.0]
    codec = TextCodec([r['text'] for r in train], langs)
    state.stage('data', {'train_segments': len(train), 'train_hours': round(sum(r['features']['duration_s'] for r in train) / 3600, 2), 'dev_segments': len(dev), 'text_vocab': len(codec.itos), 'admission_read': False,
                         'per_language': {l: sum(1 for r in train if r['language'] == l) for l in langs}, 'excluded_overlong_transcripts': len(overlong), 'max_text_chars': MAX_TEXT_CHARS, 'max_codec_frames': max_T})
    identity_on = bool(recipe.get('identity_conditioning', False)); loud_on = bool(recipe.get('loudness_match', False))
    model = build_voice_model(len(codec.itos), int(recipe.get('d_model', 768)), int(recipe.get('layers', 12)), int(recipe.get('heads', 12)), max_frames + MAX_TEXT_CHARS + 16, identity_dim=ECAPA_DIM if identity_on else 0, dense_identity=bool(recipe.get('dense_identity', False))).to(device)
    params = sum(p.numel() for p in model.parameters())
    if recipe.get('init_from') and Path(recipe['init_from']).exists():  # continue a measured iteration of the same architecture and text vocabulary; otherwise start clean and say so
        prior = torch.load(recipe['init_from'], map_location='cpu')
        if prior.get('text_vocab') == codec.itos and bool(prior.get('identity_vector') is not None) == identity_on: model.load_state_dict(prior['model'], strict=False); state.event(f"weights initialised from {recipe['init_from']}")
        else: state.event(f"init_from ignored: {recipe['init_from']} has a different text vocabulary or identity architecture; training from scratch")
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(recipe['lr']), betas=(0.9, 0.95), weight_decay=0.1)
    batch, max_steps, warmup = int(recipe['batch_size']), int(recipe['max_steps']), int(recipe.get('warmup_steps', 1000))
    ckpt_every, eval_every = int(recipe.get('checkpoint_every', 500)), int(recipe.get('eval_every', 2500))
    feedback_on = bool(recipe.get('spectral_feedback', True))
    step, history, weights, feedback_log, identity = 0, [], np.ones(len(train)), [], None
    if control.get('resume_from') and Path(control['resume_from']).exists():
        ck = torch.load(control['resume_from'], map_location='cpu'); model.load_state_dict(ck['model']); optimizer.load_state_dict(ck['optimizer']); step = int(ck['step']); history = ck.get('history', [])
        if ck.get('weights') is not None: weights = np.array(ck['weights'])
        if ck.get('identity') is not None: identity = torch.tensor(ck['identity'], device=device)
    rng = np.random.default_rng(seed + step)
    sampling = np.array(balanced_weights(train, weights)) if recipe.get('language_balance') else weights
    mimi, fe, codec_provenance = load_mimi(device)
    from speechbrain.inference.speaker import EncoderClassifier
    ecapa = EncoderClassifier.from_hparams(source='speechbrain/spkrec-ecapa-voxceleb', savedir=str(Path(control['root']) / 'hf_cache' / 'ecapa'), run_opts={'device': device})
    pcm_store = PcmStore(aip)

    def embed16(y16):
        with torch.no_grad(): return torch.nn.functional.normalize(ecapa.encode_batch(torch.from_numpy(y16).float()[None].to(device)).squeeze(), dim=0)

    # corpus-scoped comparators: one embedding per (session, speaker) from up to two segments, memory only (temporary identity representation)
    comparators = {}
    for lang in langs:
        groups = defaultdict(list)
        for r in [r for r in rows if r['language'] == lang]: groups[(r['session'], r['speaker'])].append(r)
        keys = sorted(groups)  # every eligible research-corpus group, not the first 300
        embs = []
        for k in keys:
            segs = [r for r in groups[k] if r['features']['duration_s'] >= 2.0][:2]
            if not segs: continue
            e = torch.stack([embed16(pcm_store.read(lang, s).astype(np.float32) / 32767.0) for s in segs]).mean(0)
            if not bool(torch.isfinite(e).all()): continue
            embs.append(torch.nn.functional.normalize(e, dim=0))
        comparators[lang] = torch.stack(embs) if embs else None
        state.stage('identity_scope_' + lang, {'expected_groups': len(keys), 'represented_groups': len(embs), 'missing_groups': len(keys) - len(embs),
                    'group_set_sha256': hashlib.sha256(json.dumps(keys, sort_keys=True).encode()).hexdigest(), 'sealed_admission_excluded': True})
    state.event(f'identity comparators prepared in memory: {{{", ".join(f"{l}: {0 if comparators[l] is None else comparators[l].shape[0]}" for l in langs)}}}; never written to disk')
    threshold = float(recipe.get('identity_cosine_threshold', 0.40)); margin = float(recipe.get('identity_margin', 0.05))
    if threshold != 0.40: raise ValueError('IDENTITY_THRESHOLD_MUST_REMAIN_0_40')
    scope_complete = all(state.doc['stages']['identity_scope_' + l]['missing_groups'] == 0 for l in langs)
    # speaker-conditioned training: every training segment carries the temporary representation of its own (session, speaker) group, so the model learns
    # voice as a conditioning input; representations are computed here, kept in memory and destroyed with the process (AIP: no stored human voiceprint)
    group_of = {r['seg_id']: (r['language'], r['session'], r['speaker']) for r in train}; spk_by_group = {}
    if identity_on:
        members = defaultdict(list)
        for r in train: members[group_of[r['seg_id']]].append(r)
        for n_done, (k, segs) in enumerate(members.items()):
            segs = sorted(segs, key=lambda r: -r['features']['duration_s'])[:3]
            spk_by_group[k] = torch.nn.functional.normalize(torch.stack([embed16(pcm_store.read(k[0], s).astype(np.float32) / 32767.0) for s in segs]).mean(0), dim=0)
            if n_done % 500 == 0: state.update(progress={'stage': 'speaker representations (temporary, in memory)', 'done': n_done, 'of': len(members), 'elapsed_s': int(time.time() - started)})
        state.event(f'{len(spk_by_group)} temporary (session, speaker) representations prepared in memory for conditioning; never written to disk')
    corpus_reps = torch.cat([torch.stack(list(spk_by_group.values()))] + [comparators[l] for l in langs if comparators[l] is not None]) if identity_on else None
    if corpus_reps is None or not len(corpus_reps): raise ValueError('Complete identity comparators required')

    def invent_identity():
        """MA-15: a synthetic acoustic identity — the mean of eight corpus-derived representations plus isotropic noise, re-normalised, resampled until it clears
        the gate threshold by a margin against EVERY corpus-derived representation. Failure after the candidate budget is reported, not overridden."""
        g = torch.Generator().manual_seed(seed + 7919 + int(control['iteration'])); keys = list(spk_by_group); best = None; noise = float(recipe.get('identity_noise', 0.5))
        for n in range(int(recipe.get('identity_candidates', 200))):
            pick = torch.randperm(len(keys), generator=g)[:8].tolist(); cand = torch.stack([spk_by_group[keys[i]] for i in pick]).mean(0)
            cand = torch.nn.functional.normalize(cand + noise * cand.norm() * torch.randn(cand.shape, generator=g).to(device), dim=0)
            mx = float((corpus_reps @ cand).max())
            if best is None or mx < best['max_cosine']: best = {'vector': cand, 'max_cosine': round(mx, 4), 'candidates_tried': n + 1}
            if mx < threshold - margin: break
        best['certificate'] = {'method': 'mean of 8 corpus-derived (session, speaker) representations + isotropic noise (sigma %.2f × norm), re-normalised; resampled until max cosine to every corpus-derived representation < threshold − margin' % noise,
                               'representation_space': 'speechbrain/spkrec-ecapa-voxceleb (192-d, unit norm)', 'corpus_representations_checked': int(corpus_reps.shape[0]), 'gate_threshold': threshold, 'construction_margin': margin,
                               'max_cosine_to_any_corpus_representation': best['max_cosine'], 'passes_construction_check': best['max_cosine'] < threshold - margin, 'candidates_tried': best['candidates_tried'],
                               'scope': 'corpus-derived speaker representations of this estate only; not a global uniqueness claim over all humans', 'conditioning_input_fixed_at_serving': True}
        if not best['certificate']['passes_construction_check']: raise ValueError('INVENTED_IDENTITY_CONSTRUCTION_REFUSED')
        return best
    invented = None
    if identity_on:
        invented = invent_identity()
        # A resumed vector needs its own certificate, not the newly sampled vector's certificate.
        if identity is not None:
            maximum = float((corpus_reps @ identity).max())
            if maximum >= threshold - margin: raise ValueError('RESUMED_IDENTITY_CONSTRUCTION_REFUSED')
            invented['certificate'].update(max_cosine_to_any_corpus_representation=round(maximum, 4), resumed_identity=True)
        else: identity = invented['vector']
        state.stage('invented_identity', invented['certificate'])
    target_db = {lang: float(np.median([r['features']['energy_db_mean'] for r in train if r['language'] == lang and r['features'].get('energy_db_mean') is not None])) for lang in langs} if loud_on else {}

    def collate(items):
        texts = [codec.encode(r['language'], r['text']) for r in items]; Lt = max(len(t) for t in texts)
        text_ids = torch.zeros((len(items), Lt), dtype=torch.long)
        for i, t in enumerate(texts): text_ids[i, :len(t)] = torch.tensor(t)
        pairs = [delay(tokens[r['seg_id']][:, :max_T].long().clamp(0, CODE_PAD - 1)) for r in items]; W = max(p[0].shape[1] for p in pairs)
        inp = torch.full((len(items), MIMI_CODEBOOKS, W), CODE_PAD, dtype=torch.long); tgt = torch.full((len(items), MIMI_CODEBOOKS, W), -100, dtype=torch.long)
        for i, (a, b) in enumerate(pairs): inp[i, :, :a.shape[1]] = a; tgt[i, :, :b.shape[1]] = b
        spk = torch.stack([spk_by_group[group_of[r['seg_id']]] for r in items]) if identity_on else None
        return text_ids.to(device), inp.to(device), tgt.to(device), spk

    def synthesize(lang, text, temperature=0.8, top_k=50, max_seconds=max_s):
        model.eval(); text_ids = torch.tensor([codec.encode(lang, text)], device=device); spk = identity[None] if identity_on else None
        frames = torch.full((1, MIMI_CODEBOOKS, 1), CODE_BOS, dtype=torch.long, device=device); limit = int(max_seconds * MIMI_FRAME_HZ) + MIMI_CODEBOOKS
        end_frame = None
        with torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
            for t in range(limit):
                logits = model(text_ids, frames, spk)[:, 0, -1].float() / temperature  # (K, V)
                logits[:, CODE_BOS] = -1e9; logits[:, CODE_PAD] = -1e9
                top = torch.topk(logits, top_k, dim=-1); probs = torch.softmax(top.values, -1)
                nxt = top.indices.gather(1, torch.multinomial(probs, 1)).squeeze(1)
                if end_frame is None and int(nxt[0]) == CODE_EOS: end_frame = t
                for k in range(MIMI_CODEBOOKS):
                    if t < k: nxt[k] = CODE_PAD
                    elif end_frame is not None and t >= end_frame + k: nxt[k] = CODE_EOS
                    elif k and int(nxt[k]) == CODE_EOS: nxt[k] = logits[k, :CODE_EOS].argmax()
                frames = torch.cat([frames, nxt[None, :, None]], 2)
                if end_frame is not None and t >= end_frame + MIMI_CODEBOOKS - 1: break
        codes = undelay(frames[0, :, 1:])
        codes = codes[:, (codes != CODE_EOS).all(0) & (codes != CODE_PAD).all(0)]
        model.train()
        if codes.shape[1] < 3: return None
        return mimi_decode(mimi, codes.clamp(0, 2047), device)

    def evaluation():
        ev = {'step': step, 'at': now(), 'per_language': {}}
        rng_e = random.Random(seed)  # same held-out prompts every checkpoint; no moving evaluation target
        for lang in langs:
            prompts = rng_e.sample([r for r in dev if r['language'] == lang], min(int(recipe.get('eval_prompts_per_language', 12)), sum(1 for r in dev if r['language'] == lang)))
            feats, cos_max, rendered, last_wav, gains = [], [], 0, None, []
            for r in prompts:
                wav24 = synthesize(lang, r['text'])
                if wav24 is None: continue
                rendered += 1; y16 = _resample(wav24, SR24, SR16); f = spectrum_features(y16, SR16, len(r['text']))
                if f and loud_on and f.get('energy_db_mean') is not None:  # rendering parameter from the data: output loudness set to the language baseline median (scale-invariant features unchanged)
                    gain_db = target_db[lang] - f['energy_db_mean']; gain = 10 ** (gain_db / 20); gains.append(round(gain_db, 2))
                    wav24 = np.clip(wav24 * gain, -1.0, 1.0); y16 = _resample(wav24, SR24, SR16)
                    f = spectrum_features(y16, SR16, len(r['text']))  # measure actual post-clipping output
                last_wav = wav24
                if f: feats.append(f)
                if len(y16) > SR16: cos_max.append(float((corpus_reps @ embed16(y16)).max()))
            if last_wav is not None:
                import soundfile as sf
                sf.write(job_dir / f'sample_{lang}_step{step}.wav', last_wav, SR24)
            div = behaviour_divergence([r for r in train if r['language'] == lang], feats)
            ev['per_language'][lang] = {'prompts': len(prompts), 'rendered': rendered, 'behaviour': div, 'identity_gate': rendered_identity_gate(cos_max, prompts=len(prompts), rendered=rendered, comparators=int(corpus_reps.shape[0]), threshold=threshold, comparator_coverage_complete=scope_complete),
                                        'loudness_match': {'applied': loud_on, 'target_db': round(target_db[lang], 2), 'mean_gain_db': round(float(np.mean(gains)), 2)} if loud_on and gains else {'applied': False},
                                        'generated_spectrum': {f: percentiles([x.get(f) for x in feats]) for f in ('f0_mean_hz', 'f0_range_hz', 'pause_ratio', 'energy_db_std', 'spectral_centroid_hz')}}
        return ev
    model.train(); losses = []
    while step < max_steps:
        idx = rng.choice(len(train), size=batch, replace=True, p=sampling / sampling.sum())
        text_ids, inp, tgt, spk = collate([train[i] for i in idx])
        with torch.autocast('cuda', dtype=torch.bfloat16):
            logits = model(text_ids, inp, spk)  # (K, B, W, V)
        loss = torch.nn.functional.cross_entropy(logits.float().reshape(-1, CODE_VOCAB), tgt.permute(1, 0, 2).reshape(-1), ignore_index=-100)
        loss.backward(); losses.append(float(loss))
        for g in optimizer.param_groups: g['lr'] = lr_at(step, max_steps, float(recipe['lr']), warmup)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
        if step % 25 == 0:
            state.update(progress={'stage': 'training codec language model', 'step': step, 'of': max_steps, 'loss': round(float(np.mean(losses[-100:])), 4), 'elapsed_s': int(time.time() - started), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                                   'last_checkpoint_step': (step // ckpt_every) * ckpt_every, 'next_checkpoint_step': (step // ckpt_every + 1) * ckpt_every, 'parameters': params})
        if step % ckpt_every == 0: _save_ckpt(ckpt_dir / 'latest.pt', model, optimizer, step, {'history': history, 'weights': weights.tolist(), 'text_vocab': codec.itos, 'identity': identity.cpu().tolist() if identity is not None else None})
        if step % eval_every == 0 or step == max_steps:
            ev = evaluation(); ev['train_loss'] = round(float(np.mean(losses[-200:])), 4); history.append(ev)
            if feedback_on:
                for lang in langs:
                    sel = [i for i, r in enumerate(train) if r['language'] == lang]
                    w_l, applied = curriculum_weights([train[i] for i in sel], ev['per_language'][lang]['behaviour'])
                    for j, i in enumerate(sel): weights[i] = w_l[j]
                    feedback_log.append({'step': step, 'language': lang, 'applied': applied})
                ev['spectral_feedback_applied'] = feedback_log[-len(langs):]
                sampling = np.array(balanced_weights(train, weights)) if recipe.get('language_balance') else weights
            state.stage(f'dev_eval_step_{step}', {l: {'overall_similarity': v['behaviour']['overall_similarity'], 'identity_gate_passes': v['identity_gate']['passes'], 'max_cosine': v['identity_gate']['max_cosine_to_any_corpus_speaker'], 'rendered': v['rendered']} for l, v in ev['per_language'].items()})
    art = job_dir / 'artefact'; art.mkdir(exist_ok=True)
    torch.save({'model': model.state_dict(), 'text_vocab': codec.itos, 'recipe': recipe, 'languages': langs, 'step': step, 'codec_provenance': codec_provenance,
                'identity_vector': identity.cpu() if identity is not None else None, 'identity_certificate': invented['certificate'] if invented else None}, art / 'voice_lm.pt')
    sha = hashlib.sha256((art / 'voice_lm.pt').read_bytes()).hexdigest()
    comparators.clear(); spk_by_group.clear(); corpus_reps = None; torch.cuda.empty_cache(); lock.close()
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'lane': 'story_voice', 'recipe': recipe, 'languages': langs, 'data': state.doc['stages']['data'], 'steps': step, 'parameters': params,
            'codec_provenance': codec_provenance, 'dev': history[-1] if history else None, 'history': [{'step': h['step'], 'train_loss': h.get('train_loss'), 'per_language': {l: {'overall_similarity': v['behaviour']['overall_similarity'], 'identity_gate': v['identity_gate'], 'rendered': v['rendered']} for l, v in h['per_language'].items()}} for h in history],
            'spectral_feedback': {'enabled': feedback_on, 'log': feedback_log}, 'artefact': {'path': str(art / 'voice_lm.pt'), 'sha256': sha, 'bytes': (art / 'voice_lm.pt').stat().st_size},
            'identity': {'temporary_identity_representations_destroyed': True, 'persistent_voiceprint_register': False, 'conditioning': 'invented identity vector (synthetic; certificate in artefact)' if identity_on else 'none — the model rendered an unconditioned corpus-average voice',
                         'invented_identity_certificate': invented['certificate'] if invented else None, 'loudness_match': {'enabled': loud_on, 'target_db_by_language': {l: round(v, 2) for l, v in target_db.items()}}},
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)},
            'sealed_admission_read': False, 'training_started': True, 'raw_media_exported': False}


def baseline_render(control, state):
    """Reference rendering with the pretrained MMS-TTS voices where they exist (kik, swh); measured with the same columns — comparator, not the product."""
    import torch
    lock = gpu_lock(control); device = 'cuda'; started = time.time()
    aip = Path(control['aip_db_dir']); langs = list(control['languages']); job_dir = Path(control['job_dir']); out = {}
    repos = {'kik': 'facebook/mms-tts-kik', 'swa': 'facebook/mms-tts-swh'}
    from transformers import AutoTokenizer, VitsModel
    for lang in langs:
        rows = [r for r in load_rows(aip, lang, with_text=True) if r['split'] == 'dev' and 2.0 <= r['features']['duration_s'] <= 12.0]
        if lang not in repos: out[lang] = {'available': False, 'reason': 'no pretrained baseline voice published for this language'}; continue
        tok = AutoTokenizer.from_pretrained(repos[lang]); vits = VitsModel.from_pretrained(repos[lang]).to(device).eval()
        prompts = random.Random(int(control['seed'])).sample(rows, min(int(control.get('prompts_per_language', 12)), len(rows))); feats = []
        for r in prompts:
            ids = tok(normalise_text(r['text']), return_tensors='pt').to(device)
            with torch.no_grad(): wav = vits(**ids).waveform[0].float().cpu().numpy()
            y16 = _resample(wav, int(vits.config.sampling_rate), SR16); f = spectrum_features(y16, SR16, len(r['text']))
            if f: feats.append(f)
        train = load_rows(aip, lang)
        out[lang] = {'available': True, 'repo': repos[lang], 'rendered': len(feats), 'behaviour': behaviour_divergence([r for r in train if r['split'] == 'train'], feats)}
    lock.close()
    return {'commission_id': control['commission_id'], 'lane': 'baseline_render', 'per_language': out, 'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4)}, 'training_started': False}
