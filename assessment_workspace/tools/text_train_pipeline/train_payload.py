"""LoRA fine-tune payload · staged on GPU host by orchestrator.

Reads masked_corpus.jsonl (one JSON dict per line, 'training_text' field),
fine-tunes a small open causal LM with peft LoRA, checkpoints per epoch,
emits a JSON summary at end.

Args:
  --corpus <path>       jsonl input file
  --output-dir <path>   where to write adapter + logs
  --base-model <str>    HF model id (default Qwen/Qwen2.5-0.5B)
  --epochs <int>        default 3
  --batch-size <int>    per-device batch (default 16)
  --grad-accum <int>    (default 2)
  --lr <float>          (default 2e-4)
  --max-seq-len <int>   (default 256)
  --lora-r <int>        (default 16)
  --lora-alpha <int>    (default 32)
  --seed <int>          (default 1234)

Emits JSONL log lines to <output-dir>/train.log:
  {kind: "boot", ...}
  {kind: "step", step, loss, lr, epoch, wallclock_s, ...}
  {kind: "epoch_end", epoch, mean_loss, ...}
  {kind: "summary", ...}
"""
import argparse
import json
import math
import os
import random
import sys
import time
from datetime import datetime, timezone


def _iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class _LogEmitter:
    def __init__(self, path):
        self.fp = open(path, "a")

    def emit(self, obj):
        obj = dict(obj)
        obj.setdefault("at", _iso())
        line = json.dumps(obj, separators=(",", ":"), sort_keys=True)
        print(line, flush=True)
        self.fp.write(line + "\n")
        self.fp.flush()

    def close(self):
        try:
            self.fp.close()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--base-model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--grad-accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--max-seq-len", type=int, default=256)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--lora-alpha", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1234)
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    logger = _LogEmitter(os.path.join(args.output_dir, "train.log"))

    try:
        import torch
    except Exception as e:
        logger.emit({"kind": "fatal", "err": f"torch import failed: {e}"})
        sys.exit(2)

    try:
        from transformers import (
            AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer,
            DataCollatorForLanguageModeling,
        )
        from peft import LoraConfig, get_peft_model, TaskType
    except Exception as e:
        logger.emit({"kind": "fatal", "err": f"transformers/peft import failed: {e}"})
        sys.exit(3)

    torch.manual_seed(args.seed)
    random.seed(args.seed)

    n_gpu = torch.cuda.device_count()
    logger.emit({
        "kind": "boot",
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "n_gpu": n_gpu,
        "gpu_names": [torch.cuda.get_device_name(i) for i in range(n_gpu)],
        "args": vars(args),
    })
    if n_gpu <= 0:
        logger.emit({"kind": "fatal", "err": "no CUDA devices"})
        sys.exit(4)

    # 1) Load tokenizer + model
    t0 = time.monotonic()
    logger.emit({"kind": "load_tokenizer_start", "base_model": args.base_model})
    tok = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    logger.emit({"kind": "load_tokenizer_done", "elapsed_s": round(time.monotonic() - t0, 2)})

    t0 = time.monotonic()
    logger.emit({"kind": "load_model_start"})
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    logger.emit({"kind": "load_model_done", "elapsed_s": round(time.monotonic() - t0, 2),
                 "n_params": sum(p.numel() for p in model.parameters())})

    # 2) Configure LoRA
    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "v_proj"],
    )
    model = get_peft_model(model, lora_config)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    logger.emit({"kind": "lora_configured",
                 "trainable_params": trainable,
                 "total_params": total,
                 "trainable_pct": round(trainable / total * 100, 3)})

    # 3) Load corpus
    t0 = time.monotonic()
    corpus_texts = []
    with open(args.corpus) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("training_text") or ""
            if t:
                corpus_texts.append(t)
    random.shuffle(corpus_texts)
    logger.emit({"kind": "corpus_loaded",
                 "n_examples": len(corpus_texts),
                 "elapsed_s": round(time.monotonic() - t0, 2)})

    # 4) Tokenize
    t0 = time.monotonic()
    def _tokenize(batch_texts):
        return tok(
            batch_texts,
            padding="max_length",
            truncation=True,
            max_length=args.max_seq_len,
            return_tensors="pt",
        )

    class _CorpusDataset(torch.utils.data.Dataset):
        def __init__(self, texts):
            self.texts = texts
        def __len__(self):
            return len(self.texts)
        def __getitem__(self, i):
            enc = tok(
                self.texts[i],
                padding="max_length",
                truncation=True,
                max_length=args.max_seq_len,
                return_tensors="pt",
            )
            return {
                "input_ids": enc["input_ids"].squeeze(0),
                "attention_mask": enc["attention_mask"].squeeze(0),
            }
    ds = _CorpusDataset(corpus_texts)
    logger.emit({"kind": "dataset_ready",
                 "n_examples": len(ds),
                 "elapsed_s": round(time.monotonic() - t0, 2)})

    # 5) Data collator (causal LM: labels = shifted input_ids)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tok, mlm=False)

    # 6) Training arguments
    steps_per_epoch = math.ceil(len(ds) / (args.batch_size * n_gpu * args.grad_accum))
    logger.emit({"kind": "step_estimate",
                 "steps_per_epoch": steps_per_epoch,
                 "total_steps_est": steps_per_epoch * args.epochs})

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        logging_steps=25,
        save_strategy="epoch",
        save_total_limit=args.epochs,
        report_to=[],
        bf16=True,
        seed=args.seed,
        remove_unused_columns=False,
        dataloader_num_workers=2,
    )

    # 7) Custom callback for JSONL step logging
    from transformers import TrainerCallback
    t_train_start = time.monotonic()
    class _StepLogger(TrainerCallback):
        def on_log(self, args_, state, control, logs=None, **kwargs):
            if not logs:
                return
            logger.emit({
                "kind": "step",
                "global_step": state.global_step,
                "epoch": round(state.epoch or 0, 3),
                "loss": round(logs.get("loss", 0), 4) if "loss" in logs else None,
                "learning_rate": logs.get("learning_rate"),
                "wallclock_s": round(time.monotonic() - t_train_start, 2),
            })
        def on_epoch_end(self, args_, state, control, **kwargs):
            logger.emit({
                "kind": "epoch_end",
                "epoch": round(state.epoch or 0, 3),
                "global_step": state.global_step,
                "wallclock_s": round(time.monotonic() - t_train_start, 2),
            })

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds,
        data_collator=data_collator,
        callbacks=[_StepLogger()],
    )

    logger.emit({"kind": "training_start"})
    train_result = trainer.train()
    total_train_s = time.monotonic() - t_train_start
    logger.emit({"kind": "training_done",
                 "total_train_s": round(total_train_s, 2),
                 "metrics": {k: (float(v) if isinstance(v, (int, float)) else v)
                             for k, v in (train_result.metrics or {}).items()}})

    # 8) Save adapter
    adapter_out = os.path.join(args.output_dir, "adapter")
    model.save_pretrained(adapter_out)
    tok.save_pretrained(adapter_out)
    logger.emit({"kind": "adapter_saved", "path": adapter_out})

    # 9) Compute adapter sha256
    import hashlib
    def _sha256_dir(d):
        h = hashlib.sha256()
        for root, _, files in os.walk(d):
            for f in sorted(files):
                p = os.path.join(root, f)
                h.update(p.encode())
                with open(p, "rb") as fh:
                    while True:
                        chunk = fh.read(1024 * 1024)
                        if not chunk:
                            break
                        h.update(chunk)
        return h.hexdigest()
    adapter_sha = _sha256_dir(adapter_out)

    summary = {
        "kind": "summary",
        "at": _iso(),
        "base_model": args.base_model,
        "adapter_path": adapter_out,
        "adapter_sha256": adapter_sha,
        "n_examples": len(ds),
        "epochs": args.epochs,
        "batch_size_per_gpu": args.batch_size,
        "grad_accum": args.grad_accum,
        "effective_batch": args.batch_size * n_gpu * args.grad_accum,
        "n_gpu": n_gpu,
        "total_train_s": round(total_train_s, 2),
        "final_train_metrics": {k: (float(v) if isinstance(v, (int, float)) else v)
                                for k, v in (train_result.metrics or {}).items()},
    }
    logger.emit(summary)
    with open(os.path.join(args.output_dir, "summary.json"), "w") as fw:
        json.dump(summary, fw, indent=2, sort_keys=True)
    logger.close()


if __name__ == "__main__":
    main()
