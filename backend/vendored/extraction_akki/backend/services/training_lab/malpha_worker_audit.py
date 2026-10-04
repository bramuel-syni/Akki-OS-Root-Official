"""Native estate-runtime audit, not a training-quality or product-admission result."""
import time


def audit(control, state):
    import torch
    from services.training_lab.malpha_voice_worker import build_voice_model, delay, undelay, MIMI_CODEBOOKS, CODE_BOS
    from services.training_lab.malpha_worker_policy import rendered_identity_gate, balanced_weights
    started = time.time(); checks = {}; torch.set_num_threads(2)
    state.update(progress={'stage': 'verifying worker tensor contracts on CPU', 'synthetic_tensors_only': True})
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(20261004)
        codes = torch.randint(0, 2048, (MIMI_CODEBOOKS, 7))
        _inputs, targets = delay(codes)
        checks['delayed_codec_roundtrip'] = bool(torch.equal(undelay(targets), codes))
        for dense in (False, True):
            model = build_voice_model(16, 32, 1, 4, 32, identity_dim=192, dense_identity=dense)
            text = torch.tensor([[2, 3, 0, 0], [4, 5, 6, 0]])
            inputs = torch.full((2, MIMI_CODEBOOKS, 5), CODE_BOS, dtype=torch.long)
            identity = torch.nn.functional.normalize(torch.randn(2, 192), dim=1)
            out = model(text, inputs, identity)
            key = 'dense' if dense else 'prefix'
            checks[key + '_finite_forward'] = bool(torch.isfinite(out).all())
            loss = out.square().mean(); loss.backward()
            checks[key + '_finite_gradients'] = all(bool(torch.isfinite(p.grad).all()) for p in model.parameters() if p.grad is not None)
            model.eval()
            with torch.no_grad():
                before = model(text, inputs, identity)
                model.text_emb.weight[0].fill_(1000)
                after = model(text, inputs, identity)
            checks[key + '_text_padding_masked'] = bool(torch.allclose(before, after, atol=1e-5, rtol=1e-5))
        checks['missing_render_refused'] = not rendered_identity_gate([0.2], prompts=2, rendered=1, comparators=5)['passes']
        checks['threshold_boundary_refused'] = not rendered_identity_gate([0.4], prompts=1, rendered=1, comparators=5)['passes']
        weights = balanced_weights([{'language': l} for l in ('kik', 'kik', 'kam', 'swa')])
        checks['language_mass_balanced'] = weights == [0.5, 0.5, 1.0, 1.0]
    state.stage('worker_contract', checks)
    if not all(checks.values()): raise ValueError('WORKER_CONTRACT_FAILED:' + ','.join(k for k, v in checks.items() if not v))
    return {'status': 'passed', 'checks': checks, 'torch_version': torch.__version__, 'worker_contract_version': control['worker_contract_version'],
            'quality_evidence': False, 'synthetic_tensors_only': True, 'training_started': False, 'sealed_admission_read': False, 'raw_media_exported': False,
            'compute': {'wall_seconds': round(time.time() - started, 2), 'gpu_seconds': 0, 'device': 'cpu'}}