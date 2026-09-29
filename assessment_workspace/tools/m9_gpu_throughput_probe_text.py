"""Throughput probe for the M9 text worker on one H200 in TRAIN mode: gradient-checkpointing × tokens-per-step variants (read-only, no estate data)."""
import sys, time, json, torch
sys.path.insert(0, sys.argv[2])
from services.training_runner.m9_worker import _load_model
root = sys.argv[1]
base_id = sys.argv[3] if len(sys.argv) > 3 else "qwen3-1.7b-base"
reg = json.load(open(f"{root}/base_registration.json"))
base = {"registry_id": base_id, **reg[base_id]}
cfg = {"lora_r": 16, "lora_alpha": 32, "lora_dropout": 0.05, "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]}
tok, model = _load_model(base, cfg, "cuda")
model.train()
print(json.dumps({"base": base_id, "device": torch.cuda.get_device_name(0), "total_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1), "training_mode": model.training}), flush=True)
variants = [(True, 32, 128), (False, 32, 128), (True, 64, 128), (False, 64, 128), (True, 128, 128), (False, 128, 128), (True, 256, 128), (False, 256, 128), (True, 128, 256), (False, 128, 256), (True, 512, 128), (True, 256, 256)]
params = [p for p in model.parameters() if p.requires_grad]
for gc_on, bs, seq in variants:
    if gc_on:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    else:
        model.gradient_checkpointing_disable()
    opt = torch.optim.AdamW(params, lr=1e-4)
    try:
        x = torch.randint(100, 5000, (bs, seq), device="cuda"); mask = torch.ones_like(x)
        torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
        for i in range(6):
            if i == 2:
                torch.cuda.synchronize(); t0 = time.monotonic()
            loss = model(input_ids=x, attention_mask=mask, labels=x).loss
            loss.backward(); torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step(); opt.zero_grad(set_to_none=True)
        torch.cuda.synchronize(); dt = (time.monotonic() - t0) / 4
        print(json.dumps({"grad_ckpt": gc_on, "batch": bs, "seq": seq, "tokens": bs * seq, "step_s": round(dt, 3), "tokens_per_s": round(bs * seq / dt), "peak_gb": round(torch.cuda.max_memory_allocated() / 1e9, 1)}), flush=True)
    except torch.cuda.OutOfMemoryError:
        print(json.dumps({"grad_ckpt": gc_on, "batch": bs, "seq": seq, "tokens": bs * seq, "oom": True}), flush=True)
    opt.zero_grad(set_to_none=True); del opt; torch.cuda.empty_cache()
