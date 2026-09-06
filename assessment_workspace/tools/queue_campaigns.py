"""Queue campaigns · W-Multi-Table-Extract close · 2026-09-06T~14:XXZ.

Prepares corpora and queue manifests for both campaigns, then fires
on-host dispatchers detached. No pod-side polling after this.

Sequence per host:
  1. Rsync on_host_queue_dispatcher.py to ~/akki_journal/ (both hosts)
  2. Extract 2 shared corpora (ussd_plus_sms_deduplicated · used by
     B-REF/B3/B4/B5/B6, and ussd_plus_sms_raw · used by B2)
  3. Build campaign-A queue manifest (A-1/A-2 queue behind A-0; A-3-7B
     TRIMMED per owner's trim-last guidance)
  4. Build campaign-B queue manifest (B-REF/B2/B3/B4/B5/B6 queue behind B1)
  5. scp queue manifests to hosts
  6. Fire dispatcher detached on both hosts via ssh -f
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/app/assessment_workspace/repos/Extraction-Akki/backend")

# Prep env for pipeline calls
os.environ.setdefault("AKKI_ENV", "development")
os.environ.setdefault("SHIELD_TRAIN_STAGE_LOCAL_DIR",
                      "/app/assessment_workspace/phase0/shield_train_receipts/staged_corpora")
os.environ.setdefault("SHIELD_TRAIN_HELD_OUT_RECEIPT_DIR",
                      "/app/assessment_workspace/phase0/shield_train_receipts/held_out_slices")
os.environ.setdefault("SHIELD_TRAIN_RECEIPTS_DIR",
                      "/app/assessment_workspace/phase0/shield_train_receipts")
os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")
os.environ.setdefault("DB_NAME", "queue_campaigns_ephemeral")
os.environ.setdefault("SYNISENSE_MASTER_SECRET",
                      "queue-campaigns-ephemeral")

_KEY = "/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu"
_HOSTS = {"akki-vm": "41.173.184.244", "akki-vm-ii": "41.173.184.247"}
_SSH_OPTS = ["-i", _KEY,
             "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
             "-o", "StrictHostKeyChecking=no",
             "-o", "UserKnownHostsFile=/root/.ssh/known_hosts"]


class DirectSSHSeam:
    def __init__(self, host_slug):
        self.host_slug = host_slug
        self.ip = _HOSTS[host_slug]

    def run(self, cmd):
        r = subprocess.run(["ssh"] + _SSH_OPTS + [f"ubuntu@{self.ip}", cmd],
                           capture_output=True, text=True, timeout=120)
        return {"exit_code": r.returncode, "stdout": r.stdout,
                "stderr": r.stderr[:200] if r.stderr else ""}

    def put_file(self, local_path, remote_path):
        r = subprocess.run(["scp"] + _SSH_OPTS +
                           [str(local_path), f"ubuntu@{self.ip}:{remote_path}"],
                           capture_output=True, text=True, timeout=180)
        return {"exit_code": r.returncode,
                "stderr": r.stderr[:200] if r.stderr else ""}


def _iso_utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_creds():
    with open("/app/backend/estate_keys/data_sources/db-restore-603-cluster.json") as f:
        c = json.load(f)
    os.environ["AWS_ACCESS_KEY_ID"] = c["aws_access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = c["aws_secret_access_key"]
    os.environ["AWS_DEFAULT_REGION"] = c["region"]
    return c


def _build_backend_execute():
    from services.campaign_infra.production_trainer import _build_backend_execute
    c = _load_creds()
    return _build_backend_execute(
        region=c["region"], cluster_arn=c["cluster_arn"],
        secret_arn=c["secret_arn"], database=c["database"],
    )


def rsync_dispatcher():
    """Rsync on_host_queue_dispatcher.py to both hosts."""
    src = "/app/assessment_workspace/repos/Extraction-Akki/tools/on_host_queue_dispatcher.py"
    for host_slug, ip in _HOSTS.items():
        r = subprocess.run(
            ["scp"] + _SSH_OPTS + [src, f"ubuntu@{ip}:/home/ubuntu/akki_journal/"],
            capture_output=True, text=True, timeout=60)
        print(f"  {host_slug}: rsync rc={r.returncode}", flush=True)


def extract_corpus(host_slug, corpus_variant, material_admit_ref,
                   slice_size=30000):
    """Fire execute_governed_lora_run on `host_slug` for `corpus_variant`
    (extracts + stages, does NOT invoke trainer). Returns run_receipt."""
    from services.shield_train import pipeline as _p
    from services.campaign_infra.production_trainer import (
        resolve_corpus_variant,
    )
    tables, dedup_flag = resolve_corpus_variant(corpus_variant)
    variant_str = "raw" if not dedup_flag else "deduplicated"
    backend_execute = _build_backend_execute()
    seam = DirectSSHSeam(host_slug)
    print(f"  extracting {corpus_variant} for {host_slug} ({tables})...", flush=True)
    r = _p.execute_governed_lora_run(
        tier="t1_full_mask", recipe_version=corpus_variant,
        base_model_id="Qwen/Qwen2.5-3B",
        material_admit_ref=material_admit_ref, host_slug=host_slug,
        table_context=tables, slice_size=slice_size,
        backend_execute=backend_execute, ssh_seam=seam,
        corpus_variant=variant_str,
    )
    print(f"    run_id: {r['run_id']}", flush=True)
    print(f"    train_sha256: {r['train_corpus']['sha256'][:20]}...", flush=True)
    print(f"    train rows: {r['train_corpus']['row_count']}", flush=True)
    print(f"    held-out rows: {r['held_out_corpus']['row_count']}", flush=True)
    print(f"    remote_dir: {r['remote_dir']}", flush=True)
    return r


def build_queue_entry(run_name, campaign_id, run_id_prefix, base_model,
                       lora_rank, ctx_len, per_device_batch, grad_accum, lr,
                       num_epochs, seed, corpus_remote_dir,
                       wait_for_run_id=None):
    """Build one queue entry dict for on_host_queue_dispatcher.py."""
    run_id_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Each queue entry gets a unique run_id (dispatcher writes its own
    # trainer output under ~/akki_journal/<run_id>/). Base timestamp
    # advances by 1 second per entry to avoid identical run_ids.
    run_id = f"shield-train-{run_id_prefix}-{run_id_ts}"
    run_dir = f"/home/ubuntu/akki_journal/{run_id}"
    entry = {
        "run_name": run_name,
        "run_id": run_id,
        "trainer_args": {
            "--run-id": run_id, "--run-dir": run_dir,
            "--campaign-id": campaign_id, "--run-name": run_name,
            "--corpus": f"{corpus_remote_dir}/train_corpus.jsonl",
            "--held-out": f"{corpus_remote_dir}/held_out_corpus.jsonl",
            "--base-model": base_model, "--seed": seed,
            "--lora-rank": lora_rank, "--ctx-len": ctx_len,
            "--per-device-batch": per_device_batch,
            "--grad-accum": grad_accum, "--lr": lr,
            "--num-epochs": num_epochs,
        },
    }
    if wait_for_run_id:
        entry["wait_for_run_id"] = wait_for_run_id
    return entry


def build_campaign_b_queue(dedup_run_receipt, raw_run_receipt):
    """Build 6-entry queue for Campaign B behind B1's completion."""
    B1_RUN_ID = "shield-train-campaign-b-method-ablations-20260906-20260906T141344Z"
    CAMPAIGN_ID = "campaign-b-method-ablations-20260906"
    dedup_dir = dedup_run_receipt["remote_dir"].replace("~", "/home/ubuntu")
    raw_dir = raw_run_receipt["remote_dir"].replace("~", "/home/ubuntu")

    runs = []
    # B-REF-3B · ussd_plus_sms_deduplicated · rank 16 · ctx 1024
    e = build_queue_entry("B-REF-3B", CAMPAIGN_ID, "campaign-b-B-REF-3B",
                          "Qwen/Qwen2.5-3B", "16", "1024", "2", "16",
                          "0.0002", "3", "1", dedup_dir,
                          wait_for_run_id=B1_RUN_ID)
    runs.append(e)
    time.sleep(1)  # unique timestamp
    # B2-DEDUP-OFF · ussd_plus_sms_raw · rank 16 · ctx 1024
    e = build_queue_entry("B2-DEDUP-OFF", CAMPAIGN_ID, "campaign-b-B2-DEDUP-OFF",
                          "Qwen/Qwen2.5-3B", "16", "1024", "2", "16",
                          "0.0002", "3", "1", raw_dir)
    runs.append(e)
    time.sleep(1)
    # B3-RANK-8 · ussd_plus_sms_deduplicated (reuse dedup corpus) · rank 8
    e = build_queue_entry("B3-RANK-8", CAMPAIGN_ID, "campaign-b-B3-RANK-8",
                          "Qwen/Qwen2.5-3B", "8", "1024", "2", "16",
                          "0.0002", "3", "1", dedup_dir)
    runs.append(e)
    time.sleep(1)
    # B4-RANK-32 · ussd_plus_sms_deduplicated · rank 32
    e = build_queue_entry("B4-RANK-32", CAMPAIGN_ID, "campaign-b-B4-RANK-32",
                          "Qwen/Qwen2.5-3B", "32", "1024", "2", "16",
                          "0.0002", "3", "1", dedup_dir)
    runs.append(e)
    time.sleep(1)
    # B5-CTX-512 · ussd_plus_sms_deduplicated · ctx 512
    e = build_queue_entry("B5-CTX-512", CAMPAIGN_ID, "campaign-b-B5-CTX-512",
                          "Qwen/Qwen2.5-3B", "16", "512", "4", "8",
                          "0.0002", "3", "1", dedup_dir)
    runs.append(e)
    time.sleep(1)
    # B6-CTX-2048 · ussd_plus_sms_deduplicated · ctx 2048
    e = build_queue_entry("B6-CTX-2048", CAMPAIGN_ID, "campaign-b-B6-CTX-2048",
                          "Qwen/Qwen2.5-3B", "16", "2048", "1", "32",
                          "0.0002", "3", "1", dedup_dir)
    runs.append(e)

    return {"campaign_id": CAMPAIGN_ID, "generated_at_utc": _iso_utc(),
            "runs": runs, "waits_behind_run_id": B1_RUN_ID,
            "notes": "Corpus paths for B-REF/B3/B4/B5/B6 reference the shared "
                     "ussd_plus_sms_deduplicated staged corpus (dedup_run_id: "
                     f"{dedup_run_receipt['run_id']}). B2 uses independently-"
                     f"staged ussd_plus_sms_raw (raw_run_id: {raw_run_receipt['run_id']}). "
                     "SMS emit = sms_title only per Ruling #5."}


def build_campaign_a_queue(a1_corpus_receipt=None, a2_corpus_receipt=None):
    """Build queue for Campaign A behind A0. A-3-7B TRIMMED per owner's
    trim-last guidance to fit the 3-day window.

    For A-1 (1.5B) and A-2 (3B), same USSD corpus as A0. Rather than re-
    extracting (identical corpus), the dispatcher launches each with
    fresh run_id + reuses A0's staged corpus paths. This is safe because
    A0's staged corpus is on-host permanently; the dispatcher just
    dispatches a new trainer against those files.
    """
    A0_RUN_ID = "shield-train-campaign-a-baseline-ladder-20260906-20260906T140930Z"
    CAMPAIGN_ID = "campaign-a-baseline-ladder-20260906"
    # A0's staged corpus paths on akki-vm.
    a0_dir = f"/home/ubuntu/akki_journal/{A0_RUN_ID}"

    runs = []
    # A-1-1p5B · Qwen2.5-1.5B · behind A0
    e = build_queue_entry("A-1-1p5B", CAMPAIGN_ID, "campaign-a-A-1-1p5B",
                          "Qwen/Qwen2.5-1.5B", "16", "1024", "4", "8",
                          "0.0002", "3", "1", a0_dir,
                          wait_for_run_id=A0_RUN_ID)
    runs.append(e)
    time.sleep(1)
    # A-2-3B · Qwen2.5-3B · behind A-1
    e = build_queue_entry("A-2-3B", CAMPAIGN_ID, "campaign-a-A-2-3B",
                          "Qwen/Qwen2.5-3B", "16", "1024", "2", "16",
                          "0.0002", "3", "1", a0_dir)
    runs.append(e)
    # A-3-7B TRIMMED per owner's trim-last guidance.

    return {"campaign_id": CAMPAIGN_ID, "generated_at_utc": _iso_utc(),
            "runs": runs, "waits_behind_run_id": A0_RUN_ID,
            "notes": "A-3-7B trimmed per owner ruling ('cut Campaign A's 7B run "
                     "or B's ctx-2048 BEFORE cutting anything else — window "
                     "integrity beats ladder completeness'). Queue keeps A-1 + "
                     "A-2 which fit the remaining window on a 2-H200 host. "
                     "Corpus reused from A0 (identical ussd_deduplicated)."}


def deploy_queue(host_slug, queue_manifest, local_path, remote_path):
    """Write queue JSON locally then scp to host."""
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "w") as f:
        json.dump(queue_manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    r = subprocess.run(
        ["scp"] + _SSH_OPTS + [local_path,
                                    f"ubuntu@{_HOSTS[host_slug]}:{remote_path}"],
        capture_output=True, text=True, timeout=60)
    print(f"  {host_slug}: queue scp rc={r.returncode}", flush=True)
    return remote_path


def fire_dispatcher(host_slug, queue_remote_path, campaign_id):
    """Fire on_host_queue_dispatcher.py detached on host via ssh -f."""
    cmd = (
        f"cd ~ && "
        f"mkdir -p ~/akki_journal/queue && "
        f"setsid nohup python3 ~/akki_journal/on_host_queue_dispatcher.py "
        f"--queue-file {queue_remote_path} "
        f"--campaign-id {campaign_id} "
        f">> ~/akki_journal/queue/dispatcher_stdout.log 2>&1 &"
        f" echo $!"
    )
    ssh_flags = ["-f", "-n", "-o", "LogLevel=error"] + _SSH_OPTS
    try:
        r = subprocess.run(
            ["ssh"] + ssh_flags + [f"ubuntu@{_HOSTS[host_slug]}", cmd],
            capture_output=True, text=True, timeout=30)
        print(f"  {host_slug}: dispatcher fire rc={r.returncode} stdout={r.stdout[:100]!r}",
              flush=True)
    except subprocess.TimeoutExpired:
        print(f"  {host_slug}: dispatcher fire timed out (expected; -f fork-exit)",
              flush=True)


def main():
    print("=" * 60, flush=True)
    print("W-MULTI-TABLE-EXTRACT · QUEUE CAMPAIGNS", flush=True)
    print("=" * 60, flush=True)

    print("\n[1/6] Rsync dispatcher to both hosts", flush=True)
    rsync_dispatcher()

    print("\n[2/6] Extract ussd_plus_sms_deduplicated for akki-vm-ii", flush=True)
    dedup_receipt = extract_corpus(
        host_slug="akki-vm-ii",
        corpus_variant="ussd_plus_sms_deduplicated",
        material_admit_ref="campaign-b-multi-table-dedup-20260906",
    )

    print("\n[3/6] Extract ussd_plus_sms_raw for akki-vm-ii", flush=True)
    raw_receipt = extract_corpus(
        host_slug="akki-vm-ii",
        corpus_variant="ussd_plus_sms_raw",
        material_admit_ref="campaign-b-multi-table-raw-20260906",
    )

    print("\n[4/6] Build Campaign B queue manifest", flush=True)
    b_queue = build_campaign_b_queue(dedup_receipt, raw_receipt)
    b_local = "/app/assessment_workspace/phase0/campaign_drafts/campaign_b_queue_manifest.json"
    b_remote = "/home/ubuntu/akki_journal/queue/campaign_b_queue.json"
    deploy_queue("akki-vm-ii", b_queue, b_local, b_remote)

    print("\n[5/6] Build Campaign A queue manifest", flush=True)
    a_queue = build_campaign_a_queue()
    a_local = "/app/assessment_workspace/phase0/campaign_drafts/campaign_a_queue_manifest.json"
    a_remote = "/home/ubuntu/akki_journal/queue/campaign_a_queue.json"
    deploy_queue("akki-vm", a_queue, a_local, a_remote)

    print("\n[6/6] Fire dispatchers detached on both hosts", flush=True)
    fire_dispatcher("akki-vm-ii", b_remote, b_queue["campaign_id"])
    fire_dispatcher("akki-vm", a_remote, a_queue["campaign_id"])

    print("\n[VERIFY] Wait 5s then probe dispatcher heartbeats", flush=True)
    time.sleep(5)
    for host in _HOSTS:
        r = subprocess.run(
            ["ssh"] + _SSH_OPTS + [f"ubuntu@{_HOSTS[host]}",
                                    "cat ~/akki_journal/queue/dispatcher_heartbeat.json 2>/dev/null && echo '---' && ps auxf | grep on_host_queue_dispatcher | grep -v grep | head -1"],
            capture_output=True, text=True, timeout=15)
        print(f"  {host}:\n{r.stdout}", flush=True)


if __name__ == "__main__":
    main()
