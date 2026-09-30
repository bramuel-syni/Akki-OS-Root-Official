"""Corrective research run, on the existing admitted host/dispatcher only. Never auto-promotes.

Two independent H200 trials may run concurrently. Poisson DP-SGD is window-example-level,
not presenter-level privacy; dataset construction and dev/probe measurements are not DP.
"""
import hashlib
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

from services.audio_plane_v1 import language_cognition_worker as w


OPTIONAL_DEFAULTS = {'logit_adjustment_tau': 0.0, 'bottleneck_dim': 128, 'bottleneck_noise': 0.0, 'speaker_loss_weight': 0.1,
                     'condition_loss_weight': 0.05}


def validate(params):
    required = {'baseline_job_id', 'gpu_index', 'seed', 'epochs', 'batch_size', 'physical_batch_size',
                'max_windows_per_file', 'parallelism', 'lr', 'adversary_strength', 'noise_multiplier',
                'max_grad_norm', 'delta', 'smoke_steps', 'owner_order_ref'}
    unknown = set(params) - required - set(OPTIONAL_DEFAULTS)
    if unknown or not required <= set(params):
        raise ValueError('CORRECTIVE_PARAMETERS_REQUIRED:' + ','.join(sorted((required - set(params)) | unknown)))
    if params['baseline_job_id'] != 'lcj-f96c86a16312':
        raise ValueError('UNREVIEWED_BASELINE_REQUIRES_A_NEW_RECIPE')
    for key in ('gpu_index', 'seed', 'epochs', 'batch_size', 'physical_batch_size', 'max_windows_per_file', 'parallelism', 'smoke_steps'):
        if type(params[key]) is not int or params[key] < (0 if key in {'gpu_index', 'seed', 'smoke_steps'} else 1):
            raise ValueError('INVALID_CORRECTIVE_INTEGER:' + key)
    if params['gpu_index'] not in (0, 1) or params['parallelism'] > 32 or params['physical_batch_size'] > params['batch_size']:
        raise ValueError('INVALID_GPU_OR_BATCH_ALLOCATION')
    for key in ('lr', 'adversary_strength', 'noise_multiplier', 'max_grad_norm', 'delta'):
        if type(params[key]) not in (int, float) or not math.isfinite(params[key]) or params[key] <= 0:
            raise ValueError('INVALID_CORRECTIVE_NUMBER:' + key)
    for key in ('logit_adjustment_tau', 'bottleneck_noise', 'speaker_loss_weight', 'condition_loss_weight'):
        if key in params and (type(params[key]) not in (int, float) or not math.isfinite(params[key]) or params[key] < 0):
            raise ValueError('INVALID_CORRECTIVE_NUMBER:' + key)
    if 'bottleneck_dim' in params and (type(params['bottleneck_dim']) is not int or not 8 <= params['bottleneck_dim'] <= 512):
        raise ValueError('INVALID_CORRECTIVE_INTEGER:bottleneck_dim')
    if params['delta'] >= 1 or not isinstance(params['owner_order_ref'], str) or not params['owner_order_ref'].strip():
        raise ValueError('CORRECTIVE_AUTHORITY_OR_DELTA_INVALID')


def _served_output_features(logits, threshold=0.6):
    """What the artefact exposes when served in-perimeter: the window label and a coarse confidence bucket.
    Weights never leave the tenant host; this is the egress surface a consumer could probe."""
    import torch
    probs = torch.softmax(torch.as_tensor(logits, dtype=torch.float32), -1)
    conf, pred = probs.max(-1)
    label = torch.nn.functional.one_hot(pred, probs.shape[-1]).float()
    bucket = torch.stack([(conf < threshold), (conf >= threshold) & (conf < 0.85), conf >= 0.85], -1).float()
    return torch.cat([label, bucket], -1).numpy()


def _balanced_speaker_probe(features, presenters, seed=5, min_windows=20):
    """MUST-DO §4 probe on a presenter-BALANCED held-out test half, so chance == majority == 1/N and
    'fail to exceed chance' is a fair, unambiguous criterion."""
    import torch
    by = {}
    for i, p in enumerate(presenters):
        by.setdefault(p, []).append(i)
    keep = {p: idx for p, idx in by.items() if len(idx) >= min_windows}
    if len(keep) < 2:
        return {'measured': False, 'reason': f'fewer than two held-out presenters with >= {min_windows} windows'}
    rnd = random.Random(seed)
    per = min(len(idx) for idx in keep.values())
    labels = {p: i for i, p in enumerate(sorted(keep))}
    tr, te = [], []
    for p, idx in keep.items():
        idx = idx[:]; rnd.shuffle(idx); idx = idx[:per]; h = per // 2
        tr += [(i, labels[p]) for i in idx[:h]]; te += [(i, labels[p]) for i in idx[h:]]
    x = torch.as_tensor(features, dtype=torch.float32)
    x = (x - x.mean(0)) / (x.std(0) + 1e-6)
    xtr, ytr = x[[i for i, _ in tr]], torch.tensor([y for _, y in tr])
    xte, yte = x[[i for i, _ in te]], torch.tensor([y for _, y in te])
    lin = torch.nn.Linear(x.shape[1], len(labels))
    opt = torch.optim.Adam(lin.parameters(), lr=1e-2, weight_decay=1e-3)
    for _ in range(300):
        opt.zero_grad(); torch.nn.functional.cross_entropy(lin(xtr), ytr).backward(); opt.step()
    with torch.no_grad():
        acc = float((lin(xte).argmax(-1) == yte).float().mean())
    chance = 1.0 / len(labels)
    # Binomial 95 % upper bound of a chance-level probe on this many balanced test windows.
    tolerance = 1.96 * math.sqrt(chance * (1 - chance) / max(1, len(te)))
    return {'measured': True, 'presenters': len(labels), 'test_windows': len(te), 'windows_per_presenter': per, 'accuracy': round(acc, 4),
            'chance': round(chance, 4), 'chance_upper_95': round(chance + tolerance, 4), 'at_chance': acc <= chance + tolerance}


def _evaluate(model, featurizer, rows, codes, device, batch=1024, collect=False):
    import numpy as np
    import torch
    per = {c: {'windows': 0, 'correct': 0, 'abstain': 0} for c in codes}
    conditions, confusion, features, logits_all, encoder_all, presenters = {}, {}, [], [], [], []
    model.eval(); model.disable_hooks()
    try:
        with torch.no_grad():
            for i in range(0, len(rows), batch):
                chunk = rows[i:i + batch]
                mel = featurizer(torch.from_numpy(np.stack([r[0] for r in chunk])))
                logits, _, _, z, enc = model(mel)
                conf, pred = logits.softmax(-1).max(-1)
                if collect:
                    features.append(z.cpu()); logits_all.append(logits.cpu()); encoder_all.append(enc.cpu())
                    presenters.extend(r[2] for r in chunk)
                for row, confidence, prediction in zip(chunk, conf.tolist(), pred.tolist()):
                    code = codes[row[1]]
                    cond = conditions.setdefault(row[6], {'windows': 0, 'correct': 0, 'abstain': 0})
                    for stat in (per[code], cond):
                        stat['windows'] += 1; stat['abstain'] += int(confidence < 0.6)
                        stat['correct'] += int(confidence >= 0.6 and prediction == row[1])
                    if confidence >= 0.6:
                        confusion.setdefault(code, Counter())[codes[prediction]] += 1
    finally:
        model.enable_hooks(); model.train()
    for row in list(per.values()) + list(conditions.values()):
        judged = row['windows'] - row['abstain']
        row['accuracy'] = round(row['correct'] / judged, 5) if judged else None
        row['abstention_rate'] = round(row['abstain'] / row['windows'], 5) if row['windows'] else None
    judged = sum(r['windows'] - r['abstain'] for r in per.values())
    report = {'windows': len(rows), 'per_language': per, 'per_condition_sample_rate': conditions,
              'overall_accuracy_on_judged': round(sum(r['correct'] for r in per.values()) / judged, 5) if judged else None,
              'overall_abstention_rate': round(sum(r['abstain'] for r in per.values()) / len(rows), 5) if rows else None,
              'confidence_threshold': 0.6, 'confusion_top': {c: dict(v.most_common(5)) for c, v in confusion.items()}}
    extra = (torch.cat(features).numpy(), torch.cat(logits_all).numpy(), torch.cat(encoder_all).numpy(), presenters) if features else None
    return report, extra


def _checkpoint(path, model, optimizer, privacy, epoch, steps, generator, recipe_hash, manifest_hash):
    import numpy as np
    import os
    import torch
    state = {'model': {k: v.detach().cpu() for k, v in model.state_dict().items()},
             'optimizer': optimizer.state_dict(), 'privacy_accountant': privacy.accountant.state_dict(),
             'epoch': epoch, 'steps': steps, 'python_rng': random.getstate(), 'numpy_rng': np.random.get_state(),
             'torch_rng': torch.get_rng_state(), 'cuda_rng': torch.cuda.get_rng_state_all(),
             'loader_rng': generator.get_state(), 'recipe_sha256': recipe_hash, 'manifest_sha256': manifest_hash}
    temp = path.with_suffix('.tmp'); torch.save(state, temp); os.replace(temp, path)


def train(control, state):
    import numpy as np
    import torch
    from opacus import PrivacyEngine
    from opacus.utils.batch_memory_manager import BatchMemoryManager
    from opacus.validators import ModuleValidator
    from torch.utils.data import DataLoader, TensorDataset
    from transformers import WhisperProcessor
    from services.audio_plane_v1.corrective_data import prepare
    from services.audio_plane_v1.corrective_model import CorrectiveModel, Featurizer
    start = time.monotonic()
    torch.set_num_threads(8)
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise ValueError('CORRECTIVE_REQUIRES_ONE_RESERVED_VISIBLE_GPU')
    # Owner order 2026-09-29 (maximum utilisation): TF32 tensor-core matmul. Clipping and noise stay fp32 tensors.
    torch.backends.cuda.matmul.allow_tf32 = True; torch.backends.cudnn.allow_tf32 = True
    torch.set_float32_matmul_precision('high')
    torch.manual_seed(control['seed']); np.random.seed(control['seed']); random.seed(control['seed'])
    control = {**OPTIONAL_DEFAULTS, **control}
    device = 'cuda'
    codes, sets, split, manifest_hash, art = prepare(control, state)
    reg = json.loads((Path(control['root']) / 'base_registration.json').read_text())
    local = reg['whisper-lid-v1-mit']['local_path']
    featurizer = Featurizer(WhisperProcessor.from_pretrained(local, local_files_only=True), device)
    train_rows = sets['train']
    if not control['delta'] < 1 / len(train_rows):
        raise ValueError('DELTA_MUST_BE_SMALLER_THAN_INVERSE_WINDOW_POPULATION')
    presenters = {p: i for i, p in enumerate(sorted({r[2] for r in train_rows}))}
    conditions = {c: i for i, c in enumerate(sorted({r[6] for r in train_rows}))}
    raw = CorrectiveModel(local, len(codes), len(presenters), {**control, 'condition_count': len(conditions)}).to(device)
    raw.train(); ModuleValidator.validate(raw, strict=True)
    language_counts = Counter(r[1] for r in train_rows)
    # Logit adjustment (training-time prior offset): per-example clipping under DP neutralises loss re-weighting,
    # so minority languages are balanced through the loss landscape instead. Aggregate class counts only.
    prior = torch.tensor([language_counts[c] / len(train_rows) for c in range(len(codes))], device=device)
    logit_offset = control['logit_adjustment_tau'] * prior.clamp_min(1e-9).log()
    group_counts = Counter((r[1], r[6]) for r in train_rows)
    # Reweight losses on the fixed corpus, never oversample/duplicate Poisson examples.
    group_weights = {g: min(8.0, math.sqrt(len(train_rows) / (len(group_counts) * n))) for g, n in group_counts.items()}
    presenter_language = {presenters[r[2]]: r[1] for r in train_rows}
    allowed = torch.tensor([[presenter_language[p] == c for p in range(len(presenters))] for c in range(len(codes))], device=device)
    ds = TensorDataset(torch.from_numpy(np.stack([r[0] for r in train_rows])),
        torch.tensor([r[1] for r in train_rows]), torch.tensor([presenters[r[2]] for r in train_rows]),
        torch.tensor([conditions[r[6]] for r in train_rows]), torch.tensor([group_weights[(r[1], r[6])] for r in train_rows]))
    generator = torch.Generator(); generator.manual_seed(control['seed'])
    loader = DataLoader(ds, batch_size=control['batch_size'], shuffle=True, generator=generator,
                        num_workers=4, pin_memory=True, prefetch_factor=4)
    optimizer = torch.optim.AdamW((p for p in raw.parameters() if p.requires_grad), lr=control['lr'], weight_decay=0.01)
    privacy = PrivacyEngine(accountant='rdp', secure_mode=False)
    model, optimizer, loader = privacy.make_private(module=raw, optimizer=optimizer, data_loader=loader,
        noise_multiplier=control['noise_multiplier'], max_grad_norm=control['max_grad_norm'], poisson_sampling=True,
        grad_sample_mode='hooks', wrap_model=True, rand_on_empty=False)
    recipe = {k: control[k] for k in ('baseline_job_id', 'seed', 'epochs', 'batch_size', 'physical_batch_size', 'lr',
        'adversary_strength', 'noise_multiplier', 'max_grad_norm', 'delta', 'max_windows_per_file', 'owner_order_ref', 'smoke_steps')}
    recipe.update(encoder_seconds=2, frozen_vox_fusion=False, lora_r=16, bottleneck=control['bottleneck_dim'], bottleneck_noise=control['bottleneck_noise'],
                  logit_adjustment_tau=control['logit_adjustment_tau'], speaker_loss_weight=control['speaker_loss_weight'],
                  condition_loss_weight=control['condition_loss_weight'],
                  loss_balance='fixed language/condition square-root inverse frequency, cap8; no oversampling; training-time logit adjustment by class prior',
                  model_base_sha256=reg['whisper-lid-v1-mit']['weight_sha256'],
                  feature_path='device log-mel over the declared 2 s window (no 30 s CPU padding); vectorised training-only augmentation',
                  precision='TF32 tensor-core matmul; per-sample clipping, noise and accountant in fp32 tensors',
                  loader='4 prefetching workers, pinned memory; Poisson sampler and RNG in the main process',
                  selection='minimum dev-language correct/ALL windows (abstentions included), then macro; no test selection',
                  privacy_scope='window-example DP on fixed manifest; not presenter-level or end-to-end DP certification',
                  secure_rng=False, auto_admission=False, checkpoint_custody='internal only; speaker adversary never exported')
    recipe_text = json.dumps(recipe, sort_keys=True); recipe_hash = hashlib.sha256(recipe_text.encode()).hexdigest()
    (art / 'recipe.json').write_text(recipe_text)
    curve, steps, best, best_epoch = [], 0, (-1.0, -1.0), 0
    checkpoint = art / 'checkpoint.pt'
    trainable = [p for p in model.parameters() if p.requires_grad]
    per_sample_verified = False
    state.update(progress={'stage': 'DP-SGD ready', 'train_windows': len(train_rows), 'gpu_index': control['gpu_index'],
                           'manifest_sha256': manifest_hash, 'recipe_sha256': recipe_hash, 'opacus': 'validated'})
    training_started, step_clock = time.monotonic(), []
    for epoch in range(control['epochs']):
        losses = []
        # BatchMemoryManager controls physical accumulation; noise/accountant step once per logical Poisson batch.
        with BatchMemoryManager(data_loader=loader, max_physical_batch_size=control['physical_batch_size'], optimizer=optimizer) as batches:
            for pcm, language, speaker, condition, weight in batches:
                optimizer.zero_grad(set_to_none=True)
                if len(pcm) == 0:
                    # Empty Poisson draw still adds noise and spends one accountant step.
                    for p in trainable:
                        p.grad_sample = torch.zeros((0, *p.shape), dtype=p.dtype, device=p.device)
                        p.grad = torch.zeros_like(p)
                    loss_value = 0.0
                else:
                    mel = featurizer(pcm, augment=True)
                    language, speaker, condition, weight = (v.to(device, non_blocking=True) for v in (language, speaker, condition, weight))
                    logits, voice, recording, _, _ = model(mel)
                    # Conditional adversary cannot fight language identity itself as a presenter shortcut.
                    voice = voice.masked_fill(~allowed[language], -1e4)
                    ce = torch.nn.functional.cross_entropy
                    loss = (weight * ce(logits + logit_offset, language, reduction='none')
                            + control['speaker_loss_weight'] * ce(voice, speaker, reduction='none')
                            + control['condition_loss_weight'] * ce(recording, condition, reduction='none')).mean()
                    if not torch.isfinite(loss):
                        raise ValueError('NONFINITE_CORRECTIVE_LOSS')
                    loss.backward(); loss_value = float(loss.detach())
                    if not per_sample_verified:
                        if any(p.grad_sample is None for p in trainable):
                            raise ValueError('UNPRIVATIZED_TRAINABLE_PARAMETER')
                        per_sample_verified = True
                optimizer.step(); losses.append(loss_value)
                if optimizer._is_last_step_skipped:
                    continue
                steps += 1
                step_clock.append(time.monotonic())
                if steps % 10 == 0 or steps == 1:
                    recent = step_clock[-21:]
                    state.update(progress={'stage': 'corrective DP-SGD training', 'epoch': epoch + 1, 'epochs': control['epochs'],
                        'step': steps, 'loss': round(float(np.mean(losses[-20:])), 5), 'gpu_index': control['gpu_index'],
                        'elapsed_seconds': round(time.monotonic() - start), 'gpu_memory_gb': round(torch.cuda.max_memory_allocated()/1e9, 2),
                        'examples_per_logical_batch': control['batch_size'], 'dp_per_sample_verified': per_sample_verified,
                        'windows_per_second': round(steps * control['batch_size'] / max(1e-6, time.monotonic() - training_started), 1),
                        'recent_step_seconds': round((recent[-1] - recent[0]) / max(1, len(recent) - 1), 3) if len(recent) > 1 else None,
                        'latest_dev': curve[-1] if curve else None})
                if control['smoke_steps'] and steps >= control['smoke_steps']:
                    break
        state.update(progress={'stage': 'development evaluation (test still untouched)', 'epoch': epoch + 1, 'step': steps})
        before = privacy.accountant.state_dict()
        dev, _ = _evaluate(model, featurizer, sets['dev'], codes, device)
        if before != privacy.accountant.state_dict():
            raise ValueError('VALIDATION_CHANGED_PRIVACY_ACCOUNTANT')
        scores = [r['correct']/r['windows'] for r in dev['per_language'].values() if r['windows']]
        score = (min(scores), sum(scores)/len(scores))
        epsilon = privacy.get_epsilon(control['delta'])
        curve.append({'epoch': epoch + 1, 'step': steps, 'dev': dev, 'epsilon': epsilon, 'selection_score': score})
        # Durable development-only checkpoint for the lab; no held-out data used for feedback.
        state.update(lab_checkpoint={'epoch':epoch+1,'step':steps,'dev':dev,'epsilon':epsilon})
        if score > best:
            best, best_epoch = score, epoch + 1
            torch.save({k: v.detach().cpu() for k, v in model.state_dict().items()}, art / 'best_internal.pt')
        _checkpoint(checkpoint, model, optimizer, privacy, epoch + 1, steps, generator, recipe_hash, manifest_hash)
        if control['smoke_steps']:
            break
    # Verify the actual serialized optimizer/accountant and RNG state; do not reset spending at selection.
    saved = torch.load(checkpoint, map_location='cpu', weights_only=False)
    original_epsilon = privacy.get_epsilon(control['delta'])
    privacy.accountant.load_state_dict(saved['privacy_accountant'])
    if abs(privacy.get_epsilon(control['delta']) - original_epsilon) > 1e-9:
        raise ValueError('PRIVACY_CHECKPOINT_RELOAD_MISMATCH')
    model.load_state_dict(torch.load(art / 'best_internal.pt', map_location=device, weights_only=True))
    state.update(progress={'stage': 'terminal protected-set evaluation', 'step': steps, 'best_dev_epoch': best_epoch})
    held, extra = _evaluate(model, featurizer, sets['held'], codes, device, collect=not control['smoke_steps'])
    archive, _ = _evaluate(model, featurizer, sets['archive_test'], codes, device)
    probe = {'measured': False, 'reason': 'pipeline smoke, not a quality or privacy acceptance run'}
    if extra:
        z, logits, enc, presenters_held = extra
        served = _served_output_features(logits)
        per_language, egress = {}, {}
        for code in codes:
            idx = [i for i, p in enumerate(presenters_held) if p.startswith(code + ':')]
            if len(idx) < 40:
                continue
            ids = [presenters_held[i] for i in idx]
            per_language[code] = {name: w._speaker_probe(feat[idx], ids) for name, feat in
                                  [('bottleneck', z), ('artefact_output_logits', logits), ('encoder_representation', enc)]}
            egress[code] = {name: _balanced_speaker_probe(feat[idx], ids) for name, feat in
                            [('served_output', served), ('artefact_output_logits', logits), ('bottleneck', z), ('encoder_representation', enc)]}
        served_rows = [r['served_output'] for r in egress.values() if r['served_output'].get('measured')]
        probe = {'measured': bool(per_language), 'per_language': per_language,
                 'reading': 'Legacy diagnostic margin retained for comparison ONLY. Final criterion remains chance-level, not majority+0.05.',
                 'strict_chance_met': bool(per_language) and all(r.get('measured') and r['accuracy'] <= r['chance']
                    for language in per_language.values() for r in language.values()),
                 'balanced_probe': egress,
                 'egress_surface': {'surface': 'served_output: window label + coarse confidence bucket (weights stay in tenant custody, served in-perimeter)',
                                    'at_chance_all_languages': bool(served_rows) and all(r['at_chance'] for r in served_rows),
                                    'per_language': {c: r['served_output'] for c, r in egress.items()},
                                    'internal_representations_at_chance': all(r[name]['at_chance'] for r in egress.values() for name in ('bottleneck', 'encoder_representation') if r[name].get('measured')),
                                    'ruling_status': 'PENDING OWNER RATIFICATION — reading MUST-DO §4 "against the artefact" as the served egress surface; internal representations reported alongside, not hidden'}}
        del z, logits, enc, extra, served
    # Inference candidate omits both adversary heads. All checkpoints stay inside tenant custody.
    raw.encoder.save_pretrained(str(art / 'lora_adapter'))
    torch.save({'projection': raw.project.state_dict(), 'language_head': raw.language_head.state_dict(),
                'classes': codes, 'window_seconds': 2.0, 'threshold': 0.6, 'recipe_sha256': recipe_hash}, art / 'language_head.pt')
    digest = hashlib.sha256()
    for f in sorted(p for p in art.rglob('*') if p.is_file() and p.name not in {'checkpoint.pt', 'best_internal.pt'}):
        digest.update(str(f.relative_to(art)).encode()); digest.update(bytes.fromhex(w.sha256_file(f)))
    return {'classes': codes, 'split': split, 'held_out': held, 'archive_test': archive, 'development': curve,
        'no_speaker_id_probe': probe, 'recipe': recipe, 'recipe_sha256': recipe_hash,
        'training': {'steps': steps, 'epochs_completed': len(curve), 'best_dev_epoch': best_epoch,
                     'elapsed_seconds': round(time.monotonic()-start), 'device': device, 'gpu_index': control['gpu_index'],
                     'gpu': torch.cuda.get_device_name(0), 'gpu_max_memory_gb': round(torch.cuda.max_memory_allocated()/1e9, 2),
                     'batch_size': control['batch_size'], 'physical_batch_size': control['physical_batch_size'],
                     'precision': recipe['precision'], 'feature_path': recipe['feature_path'],
                     'windows_per_second': round(steps * control['batch_size'] / max(1e-6, time.monotonic() - training_started), 1)},
        'dp_sgd': {'applied': per_sample_verified, 'epsilon': original_epsilon, 'delta': control['delta'],
                   'noise_multiplier': control['noise_multiplier'], 'max_grad_norm': control['max_grad_norm'],
                   'accountant': 'rdp', 'poisson_sampling': True, 'secure_rng': False, 'checkpoint_accountant_verified': True,
                   'scope': recipe['privacy_scope'], 'release_privacy_certified': False},
        'checkpoint': {'optimizer_saved': bool(saved['optimizer']), 'rng_saved': all(k in saved for k in
                       ('python_rng','numpy_rng','torch_rng','cuda_rng','loader_rng')), 'path': str(checkpoint),
                       'full_interruption_resume_proven': False},
        'span_rule': {'window_seconds': 2.0, 'min_span_seconds': w.MIN_SPAN_SECONDS, 'hysteresis_windows': w.HYSTERESIS_WINDOWS},
        'artefact': {'path': str(art), 'sha256': digest.hexdigest(), 'training_manifest_sha256': manifest_hash,
                    'final_model': False, 'custody': 'RMS_TENANT; inside akki-vm-ii; never auto-admitted',
                    'moac': {'verdict': 'NOT ADMISSIBLE — research corrective candidate; missing labelled code-switch/English/Sheng and independent M9 acceptance',
                             'code_switch_material_present': False, 'no_speaker_id_probe_passed': probe.get('strict_chance_met'),
                             'no_speaker_id_probe_on_egress_surface': (probe.get('egress_surface') or {}).get('at_chance_all_languages'),
                             'per_language_meets_default': {c: (r['accuracy'] or 0) >= 0.90 for c, r in held['per_language'].items() if r['windows']}}}}