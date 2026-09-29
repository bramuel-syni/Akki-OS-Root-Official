"""Real-path step-time probe on one H200: actual corpus batches (token budget) vs fixed shapes, to locate the gap to the synthetic budget.
argv: root bundle_zip [tokens_per_batch] — run once per PYTORCH_CUDA_ALLOC_CONF setting."""
import os, sys, time, json, random
sys.path.insert(0, sys.argv[2])
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
import torch
from services.training_runner import m9_worker as w
root = sys.argv[1]; budget = int(sys.argv[3]) if len(sys.argv) > 3 else 12288
reg = json.load(open(f"{root}/base_registration.json"))
base = {"registry_id": "qwen3-1.7b-base", **reg["qwen3-1.7b-base"]}
cfg = {**w.RECIPE_DEFAULTS, "gradient_checkpointing": False, "max_seq_len": 256}
tok, model = w._load_model(base, cfg, "cuda"); model.train()
units, manifest, canaries, sha = w.load_corpus(root, "rms-transcripts-v1")
labels = w._label_names([u for u in units if u["stratum"] != "__canary__"])
train = [u for u in units if u["split"] == "train"]
random.Random("probe").shuffle(train); train = train[:12000]
ids = w._tokenize(tok, [w._example_text(u, "text_lid", labels) for u in train], 256)
buckets = w._batches(ids, 512, 41, 0, budget)
params = [p for p in model.parameters() if p.requires_grad]
opt = torch.optim.AdamW(params, lr=1e-4, weight_decay=0.01, betas=(0.9, 0.95))
print(json.dumps({"alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"), "buckets": len(buckets), "budget": budget}), flush=True)


def step(bucket, full_mask=False):
    idx, width = bucket
    x, mask, y = w._collate(ids, idx, tok.pad_token_id, "cuda", width)
    if full_mask:
        mask = torch.ones_like(x); y = x
    loss = model(input_ids=x, attention_mask=mask, labels=y).loss
    loss.backward(); torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step(); opt.zero_grad(set_to_none=True)
    return x.shape, int(mask.sum()), float(loss)


def run(name, chooser, n=10, full_mask=False):
    torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); times = []; tokens = 0
    for i in range(n):
        t0 = time.monotonic(); shape, real, _ = step(chooser(i), full_mask); torch.cuda.synchronize(); dt = time.monotonic() - t0
        if i >= 2:
            times.append(dt); tokens += real
    print(json.dumps({"variant": name, "step_s_mean": round(sum(times) / len(times), 3), "step_s_max": round(max(times), 3), "real_tokens_per_s": round(tokens / sum(times)),
                      "peak_gb": round(torch.cuda.max_memory_allocated() / 1e9, 1), "last_shape": list(shape)}), flush=True)


run("variable_shapes_real_batches", lambda i: buckets[i])
run("fixed_shape_same_batch", lambda i: buckets[0])
run("variable_shapes_real_batches_again", lambda i: buckets[10 + i])
run("variable_shapes_real_batches_third", lambda i: buckets[20 + i])
print(json.dumps({"distinct_shapes": sorted({(len(b[0]), b[1]) for b in buckets})}), flush=True)
