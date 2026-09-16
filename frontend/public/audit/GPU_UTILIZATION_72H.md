# GPU Utilization Report · 72-hour appliance benchmark suite

**Generated at UTC:** 2026-09-16T17:04:49Z
**Launch (earliest host):** 2026-09-16T03:41:28Z
**Elapsed:** 13.39 hours · **Remaining:** 58.61 hours (of 72)

## Workloads

**Appliance benchmark suite** — rotating configuration matrix (matmul bf16/fp16/fp32-tf32 at 8192/12288/16384 square × attention bf16 at 2k/4k/8k seq × batch 1/4). Each iteration = one banked artefact (throughput TFLOPs + p50/p99 latency ms). Discharges R-14 serving-engine admission precondition. No estate data; no synthetic burn loops.

## Governance

- In-perimeter (SSH via `services.training_runner.ssh_seam` · env-injection creds · §E discipline).
- No estate data (torch.randn on-device only).
- Shape-only receipts (position-redaction preserved · SEC halt reading amended for this initiation per owner ruling 2026-09-16T~03:08Z).
- Detached via `setsid nohup` — survives agent session boundaries.
- Sampler cadence: 5 minutes per host (nvidia-smi query → append-only JSONL).

## Per-host per-GPU rollup

### Host `akki-vm`

- Start (UTC): `2026-09-16T03:41:28Z`
- Telemetry samples: **332**
- Bench iterations: **1604** (ok: 1604)

| GPU | Name | Samples | Util avg | Util peak | Power avg (W) | Power peak (W) | Temp avg (°C) | Temp peak (°C) | Mem peak (MiB) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | NVIDIA H200 | 166 | 92.1% | 100.0% | 667.2 | 694.4 | 67.3 | 70.0 | 107491 |
| 1 | NVIDIA H200 | 166 | 92.3% | 100.0% | 668.2 | 694.5 | 66.9 | 70.0 | 107491 |

### Host `akki-vm-ii`

- Start (UTC): `2026-09-16T03:41:36Z`
- Telemetry samples: **326**
- Bench iterations: **1604** (ok: 1604)

| GPU | Name | Samples | Util avg | Util peak | Power avg (W) | Power peak (W) | Temp avg (°C) | Temp peak (°C) | Mem peak (MiB) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | NVIDIA H200 | 163 | 93.1% | 100.0% | 671.2 | 698.7 | 66.9 | 70.0 | 107491 |
| 1 | NVIDIA H200 | 163 | 94.1% | 100.0% | 672.2 | 695.5 | 70.6 | 75.0 | 107491 |

## Receipts index

- Local sync root: `/app/assessment_workspace/phase0/gpu_utilization_72h/{akki-vm,akki-vm-ii}/`
- Raw telemetry JSONL: `<host>/telemetry.jsonl` (one row per GPU per 5 min sample)
- Raw workload JSONL: `<host>/workload.jsonl` (one row per bench iteration)
- Machine-readable: `GPU_UTILIZATION_72H.json` (this same directory)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law