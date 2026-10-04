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
    for lang in langs: docs.extend(_documents(load_rows(aip, lang, with_text=True), lang))
    train = [d for d in docs if d['split'] == 'train']; dev = [d for d in docs if d['split'] == 'dev']
    profiles = {lang: trigram_profile([d['text'] for d in train if d['lang'] == lang]) for lang in langs}
    state.stage('data', {'train_documents': len(train), 'dev_documents': len(dev), 'per_language': {l: {'train': sum(1 for d in train if d['lang'] == l), 'dev': sum(1 for d in dev if d['lang'] == l)} for l in langs}, 'admission_read': False})
    tokenizer = AutoTokenizer.from_pretrained(recipe['base_path']); tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(recipe['base_path'], torch_dtype=torch.bfloat16).to(device)
    model.gradient_checkpointing_enable(); model.config.use_cache = False
    if recipe.get('init_adapter'): model = PeftModel.from_pretrained(model, recipe['init_adapter'], is_trainable=True)
    else: model = get_peft_model(model, LoraConfig(r=int(recipe.get('lora_r', 32)), lora_alpha=int(recipe.get('lora_alpha', 64)), lora_dropout=0.05, target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], task_type='CAUSAL_LM'))
    max_len = int(recipe.get('max_seq_len', 1024))

    def chunks(doc_list):
        out = []
        for d in doc_list:
            head = tokenizer(_prompt(d['lang'], d['title']), add_special_tokens=False).input_ids
            body = tokenizer(d['text'], add_special_tokens=False).input_ids + [tokenizer.eos_token_id]
            room = max_len - len(head)
            for i in range(0, len(body), room): out.append((d['lang'], head + body[i:i + room]))
        return out
    train_chunks, dev_chunks = chunks(train), chunks(dev)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(recipe['lr']), weight_decay=0.0)
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
        ev = {'step': step, 'at': now(), 'per_language': {}}
        for lang in langs:
            titles = [d['title'] for d in dev if d['lang'] == lang][:2] or ['a story told on the radio']
            samples = []
            for t in titles:
                text = generate(lang, t); sims = {l: round(profile_cosine(trigram_profile([text]), profiles[l]), 4) for l in langs}
                samples.append({'title': t, 'chars': len(text), 'words': len(text.split()), 'distinct_2': distinct_n(text), 'trigram_similarity': sims, 'language_fidelity': max(sims, key=sims.get) == lang, 'excerpt_sha256': hashlib.sha256(text.encode()).hexdigest()})
            (job_dir / f'samples_{lang}_step{step}.json').write_text(json.dumps({'samples': samples}, ensure_ascii=False, indent=1))
            ppl = perplexity(lang); base = (base_perplexity or {}).get(lang)
            ev['per_language'][lang] = {'dev_perplexity': ppl, 'base_perplexity': base, 'dev_perplexity_below_base': (ppl is not None and base is not None and ppl < base) if base is not None else None,
                                        'language_fidelity_rate': round(sum(s['language_fidelity'] for s in samples) / len(samples), 3), 'mean_distinct_2': round(sum(s['distinct_2'] for s in samples) / len(samples), 4), 'samples': samples}
        return ev
    # the registered base's own dev perplexity is the baseline the admission contract compares against; measured with the adapter disabled, carried by reference afterwards
    def _base_perplexity():
        with model.disable_adapter(): return {lang: perplexity(lang) for lang in langs}
    base_perplexity = _base_perplexity()
    if base_perplexity: state.stage('base_perplexity', base_perplexity)
    model.train(); losses = []
    while step < max_steps:
        rng.shuffle(train_chunks)
        for i in range(0, len(train_chunks), batch):
            if step >= max_steps: break
            ids, labels = collate(train_chunks[i:i + batch])
            loss = model(input_ids=ids, labels=labels).loss / accum; loss.backward(); losses.append(float(loss) * accum)
            if len(losses) % accum: continue
            for g in optimizer.param_groups: g['lr'] = lr_at(step, max_steps, float(recipe['lr']), warmup)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
            if step % 10 == 0:
                state.update(progress={'stage': 'training', 'step': step, 'of': max_steps, 'loss': round(float(np.mean(losses[-50:])), 4), 'elapsed_s': int(time.time() - started), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                                       'last_checkpoint_step': (step // ckpt_every) * ckpt_every, 'next_checkpoint_step': (step // ckpt_every + 1) * ckpt_every})
            if step % ckpt_every == 0: _save_ckpt(ckpt_dir / 'latest.pt', model, optimizer, step, {'history': history})
            if step % eval_every == 0 or step == max_steps:
                ev = evaluation(); ev['train_loss'] = round(float(np.mean(losses[-100:])), 4); history.append(ev)
                state.stage(f'dev_eval_step_{step}', {l: {k: v[k] for k in ('dev_perplexity', 'base_perplexity', 'dev_perplexity_below_base', 'language_fidelity_rate', 'mean_distinct_2')} for l, v in ev['per_language'].items()})
    art = job_dir / 'artefact'; model.save_pretrained(art / 'lora_adapter'); tokenizer.save_pretrained(art / 'lora_adapter')
    digest = hashlib.sha256(); nbytes = 0
    for f in sorted(p for p in (art / 'lora_adapter').rglob('*') if p.is_file()): digest.update(f.read_bytes()); nbytes += f.stat().st_size
    lock.close()
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'lane': 'story_text', 'recipe': recipe, 'languages': langs, 'data': state.doc['stages']['data'], 'steps': step, 'base_perplexity': base_perplexity,
            'dev': history[-1] if history else None, 'history': [{'step': h['step'], 'train_loss': h.get('train_loss'), 'per_language': {l: {k: v[k] for k in ('dev_perplexity', 'base_perplexity', 'dev_perplexity_below_base', 'language_fidelity_rate', 'mean_distinct_2')} for l, v in h['per_language'].items()}} for h in history],
            'artefact': {'path': str(art / 'lora_adapter'), 'sha256': digest.hexdigest(), 'bytes': nbytes, 'base': recipe['base_path']},
            'compute': {'wall_seconds': round(time.time() - started, 1), 'gpu_seconds': round(time.time() - started, 1), 'gpu_hours': round((time.time() - started) / 3600, 4), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)},
            'sealed_admission_read': False, 'training_started': True, 'raw_media_exported': False, 'text_exported': False}


# ----------------------------------------------------------------------------- voice: codec language model over Mimi tokens
def build_voice_model(text_vocab, d_model, layers, heads, max_frames):
    import torch
    from torch import nn

    class VoiceLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.text_emb = nn.Embedding(text_vocab, d_model); self.audio_emb = nn.ModuleList([nn.Embedding(CODE_VOCAB, d_model) for _ in range(MIMI_CODEBOOKS)])
            self.pos = nn.Embedding(max_frames + 512, d_model); self.kind = nn.Embedding(2, d_model)
            layer = nn.TransformerEncoderLayer(d_model, heads, 4 * d_model, dropout=0.1, activation='gelu', batch_first=True, norm_first=True)
            self.body = nn.TransformerEncoder(layer, layers); self.norm = nn.LayerNorm(d_model)
            self.heads = nn.ModuleList([nn.Linear(d_model, CODE_VOCAB) for _ in range(MIMI_CODEBOOKS)])

        def forward(self, text_ids, codes_in):
            """text_ids (B, Lt), codes_in (B, 8, T) delayed inputs → logits (8, B, T, V) for the next delayed frame."""
            B, Lt = text_ids.shape; T = codes_in.shape[2]
            t = self.text_emb(text_ids) + self.kind.weight[0]; a = sum(self.audio_emb[k](codes_in[:, k]) for k in range(MIMI_CODEBOOKS)) + self.kind.weight[1]
            x = torch.cat([t, a], 1) + self.pos(torch.arange(Lt + T, device=text_ids.device))[None]
            mask = torch.triu(torch.full((Lt + T, Lt + T), float('-inf'), device=x.device), 1)
            mask[:Lt, :Lt] = 0  # the text prompt attends to itself fully; audio frames are causal
            h = self.norm(self.body(x, mask=mask))[:, Lt:Lt + T]
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
        for r in load_rows(aip, lang, with_text=True): r['language'] = lang; rows.append(r)
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
    model = build_voice_model(len(codec.itos), int(recipe.get('d_model', 768)), int(recipe.get('layers', 12)), int(recipe.get('heads', 12)), max_frames + MAX_TEXT_CHARS + 16).to(device)
    params = sum(p.numel() for p in model.parameters())
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(recipe['lr']), betas=(0.9, 0.95), weight_decay=0.1)
    batch, max_steps, warmup = int(recipe['batch_size']), int(recipe['max_steps']), int(recipe.get('warmup_steps', 1000))
    ckpt_every, eval_every = int(recipe.get('checkpoint_every', 500)), int(recipe.get('eval_every', 2500))
    feedback_on = bool(recipe.get('spectral_feedback', True))
    step, history, weights, feedback_log = 0, [], np.ones(len(train)), []
    if control.get('resume_from') and Path(control['resume_from']).exists():
        ck = torch.load(control['resume_from'], map_location='cpu'); model.load_state_dict(ck['model']); optimizer.load_state_dict(ck['optimizer']); step = int(ck['step']); history = ck.get('history', [])
        if ck.get('weights') is not None: weights = np.array(ck['weights'])
    rng = np.random.default_rng(seed + step)
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
        for r in [r for r in rows if r['language'] == lang and r['features']['duration_s'] >= 2.0]: groups[(r['session'], r['speaker'])].append(r)
        keys = sorted(groups)[: int(recipe.get('comparators_per_language', 300))]
        embs = []
        for k in keys:
            segs = groups[k][:2]; e = torch.stack([embed16(pcm_store.read(lang, s).astype(np.float32) / 32767.0) for s in segs]).mean(0)
            embs.append(torch.nn.functional.normalize(e, dim=0))
        comparators[lang] = torch.stack(embs) if embs else None
    state.event(f'identity comparators prepared in memory: {{{", ".join(f"{l}: {0 if comparators[l] is None else comparators[l].shape[0]}" for l in langs)}}}; never written to disk')
    threshold = float(recipe.get('identity_cosine_threshold', 0.40))

    def collate(items):
        texts = [codec.encode(r['language'], r['text']) for r in items]; Lt = max(len(t) for t in texts)
        text_ids = torch.zeros((len(items), Lt), dtype=torch.long)
        for i, t in enumerate(texts): text_ids[i, :len(t)] = torch.tensor(t)
        pairs = [delay(tokens[r['seg_id']][:, :max_T].long().clamp(0, CODE_PAD - 1)) for r in items]; W = max(p[0].shape[1] for p in pairs)
        inp = torch.full((len(items), MIMI_CODEBOOKS, W), CODE_PAD, dtype=torch.long); tgt = torch.full((len(items), MIMI_CODEBOOKS, W), -100, dtype=torch.long)
        for i, (a, b) in enumerate(pairs): inp[i, :, :a.shape[1]] = a; tgt[i, :, :b.shape[1]] = b
        return text_ids.to(device), inp.to(device), tgt.to(device)

    def synthesize(lang, text, temperature=0.8, top_k=50, max_seconds=max_s):
        model.eval(); text_ids = torch.tensor([codec.encode(lang, text)], device=device)
        frames = torch.full((1, MIMI_CODEBOOKS, 1), CODE_BOS, dtype=torch.long, device=device); limit = int(max_seconds * MIMI_FRAME_HZ) + MIMI_CODEBOOKS
        with torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
            for t in range(limit):
                logits = model(text_ids, frames)[:, 0, -1].float() / temperature  # (K, V)
                logits[:, CODE_BOS] = -1e9; logits[:, CODE_PAD] = -1e9
                top = torch.topk(logits, top_k, dim=-1); probs = torch.softmax(top.values, -1)
                nxt = top.indices.gather(1, torch.multinomial(probs, 1)).squeeze(1)
                for k in range(MIMI_CODEBOOKS):
                    if t < k: nxt[k] = CODE_PAD
                frames = torch.cat([frames, nxt[None, :, None]], 2)
                if int(nxt[0]) == CODE_EOS: break
        codes = undelay(frames[0, :, 1:])
        codes = codes[:, (codes != CODE_EOS).all(0) & (codes != CODE_PAD).all(0)]
        model.train()
        if codes.shape[1] < 3: return None
        return mimi_decode(mimi, codes.clamp(0, 2047), device)

    def evaluation():
        ev = {'step': step, 'at': now(), 'per_language': {}}
        rng_e = random.Random(seed + step)
        for lang in langs:
            prompts = rng_e.sample([r for r in dev if r['language'] == lang], min(int(recipe.get('eval_prompts_per_language', 12)), sum(1 for r in dev if r['language'] == lang)))
            feats, cos_max, rendered, last_wav = [], [], 0, None
            for r in prompts:
                wav24 = synthesize(lang, r['text'])
                if wav24 is None: continue
                rendered += 1; last_wav = wav24; y16 = _resample(wav24, SR24, SR16); f = spectrum_features(y16, SR16, len(r['text']))
                if f: feats.append(f)
                if comparators[lang] is not None and len(y16) > SR16: cos_max.append(float((comparators[lang] @ embed16(y16)).max()))
            if last_wav is not None:
                import soundfile as sf
                sf.write(job_dir / f'sample_{lang}_step{step}.wav', last_wav, SR24)
            div = behaviour_divergence([r for r in train if r['language'] == lang], feats)
            ev['per_language'][lang] = {'prompts': len(prompts), 'rendered': rendered, 'behaviour': div, 'identity_gate': {'comparators': 0 if comparators[lang] is None else int(comparators[lang].shape[0]), 'threshold_cosine': threshold,
                                        'max_cosine_to_any_corpus_speaker': round(max(cos_max), 4) if cos_max else None, 'mean_max_cosine': round(sum(cos_max) / len(cos_max), 4) if cos_max else None,
                                        'passes': bool(cos_max) and max(cos_max) < threshold, 'scope': 'corpus-derived speaker representations of this estate only; not a global uniqueness claim'},
                                        'generated_spectrum': {f: percentiles([x.get(f) for x in feats]) for f in ('f0_mean_hz', 'f0_range_hz', 'pause_ratio', 'energy_db_std', 'spectral_centroid_hz')}}
        return ev
    model.train(); losses = []
    while step < max_steps:
        idx = rng.choice(len(train), size=batch, replace=True, p=weights / weights.sum())
        text_ids, inp, tgt = collate([train[i] for i in idx])
        with torch.autocast('cuda', dtype=torch.bfloat16):
            logits = model(text_ids, inp)  # (K, B, W, V)
        loss = torch.nn.functional.cross_entropy(logits.float().reshape(-1, CODE_VOCAB), tgt.permute(1, 0, 2).reshape(-1), ignore_index=-100)
        loss.backward(); losses.append(float(loss))
        for g in optimizer.param_groups: g['lr'] = lr_at(step, max_steps, float(recipe['lr']), warmup)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
        if step % 25 == 0:
            state.update(progress={'stage': 'training codec language model', 'step': step, 'of': max_steps, 'loss': round(float(np.mean(losses[-100:])), 4), 'elapsed_s': int(time.time() - started), 'gpu_peak_gb': round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                                   'last_checkpoint_step': (step // ckpt_every) * ckpt_every, 'next_checkpoint_step': (step // ckpt_every + 1) * ckpt_every, 'parameters': params})
        if step % ckpt_every == 0: _save_ckpt(ckpt_dir / 'latest.pt', model, optimizer, step, {'history': history, 'weights': weights.tolist(), 'text_vocab': codec.itos})
        if step % eval_every == 0 or step == max_steps:
            ev = evaluation(); ev['train_loss'] = round(float(np.mean(losses[-200:])), 4); history.append(ev)
            if feedback_on:
                for lang in langs:
                    sel = [i for i, r in enumerate(train) if r['language'] == lang]
                    w_l, applied = curriculum_weights([train[i] for i in sel], ev['per_language'][lang]['behaviour'])
                    for j, i in enumerate(sel): weights[i] = w_l[j]
                    feedback_log.append({'step': step, 'language': lang, 'applied': applied})
                ev['spectral_feedback_applied'] = feedback_log[-len(langs):]
            state.stage(f'dev_eval_step_{step}', {l: {'overall_similarity': v['behaviour']['overall_similarity'], 'identity_gate_passes': v['identity_gate']['passes'], 'max_cosine': v['identity_gate']['max_cosine_to_any_corpus_speaker'], 'rendered': v['rendered']} for l, v in ev['per_language'].items()})
    art = job_dir / 'artefact'; art.mkdir(exist_ok=True)
    torch.save({'model': model.state_dict(), 'text_vocab': codec.itos, 'recipe': recipe, 'languages': langs, 'step': step, 'codec_provenance': codec_provenance}, art / 'voice_lm.pt')
    sha = hashlib.sha256((art / 'voice_lm.pt').read_bytes()).hexdigest()
    comparators.clear(); torch.cuda.empty_cache(); lock.close()
    return {'commission_id': control['commission_id'], 'iteration': control['iteration'], 'lane': 'story_voice', 'recipe': recipe, 'languages': langs, 'data': state.doc['stages']['data'], 'steps': step, 'parameters': params,
            'codec_provenance': codec_provenance, 'dev': history[-1] if history else None, 'history': [{'step': h['step'], 'train_loss': h.get('train_loss'), 'per_language': {l: {'overall_similarity': v['behaviour']['overall_similarity'], 'identity_gate': v['identity_gate'], 'rendered': v['rendered']} for l, v in h['per_language'].items()}} for h in history],
            'spectral_feedback': {'enabled': feedback_on, 'log': feedback_log}, 'artefact': {'path': str(art / 'voice_lm.pt'), 'sha256': sha, 'bytes': (art / 'voice_lm.pt').stat().st_size},
            'identity': {'temporary_identity_representations_destroyed': True, 'persistent_voiceprint_register': False},
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
