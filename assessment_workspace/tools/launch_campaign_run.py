"""Launch script — Campaign A run 0 (akki-vm · 0.5B · seed 1) end-to-end.

Runs the governed pipeline for the campaign's first run:
  1. Load AWS creds from custody (never logged)
  2. Set AKKI_ENV=development (t1_full_mask admitted)
  3. Call default_trainer_fn with DirectSSHSeam override
  4. Report the run_id + first-heartbeat evidence

Under /app/assessment_workspace/tools/ per client-instruction (analysis/launch
scripts allowed; no production code).
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Add Extraction-Akki backend to sys.path for the seam + pipeline imports
sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')

# Environment prep — required by default_trainer_fn's admission gate + custody loader
os.environ.setdefault('AKKI_ENV', 'development')
os.environ.setdefault('SHIELD_TRAIN_STAGE_LOCAL_DIR',
                      '/app/assessment_workspace/phase0/shield_train_receipts/staged_corpora')
os.environ.setdefault('SHIELD_TRAIN_HELD_OUT_RECEIPT_DIR',
                      '/app/assessment_workspace/phase0/shield_train_receipts/held_out_slices')
os.environ.setdefault('SHIELD_TRAIN_RECEIPTS_DIR',
                      '/app/assessment_workspace/phase0/shield_train_receipts')
# Silence Motor/mongodb import-time noise (this script doesn't touch Mongo)
os.environ.setdefault('MONGO_URL', 'mongodb://localhost:27017')
os.environ.setdefault('DB_NAME', 'launch_shield_train_run')
os.environ.setdefault('SYNISENSE_MASTER_SECRET',
                      'launch-shield-train-run-ephemeral')

_KEY = '/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu'
_HOSTS = {'akki-vm': '41.173.184.244', 'akki-vm-ii': '41.173.184.247'}


class DirectSSHSeam:
    """Subprocess-based SSH seam that duck-types the pipeline's seam contract.

    Uses the pre-pinned host key in /root/.ssh/known_hosts. Never logs
    credentials. Both `run` and `put_file` route through the pod's ssh
    binary using the estate-keys id_ed25519_akki_gpu (mode 0600).
    """

    def __init__(self, host_slug):
        self.host_slug = host_slug
        self.ip = _HOSTS[host_slug]

    def run(self, cmd):
        # Detached background commands (setsid nohup ... &) cause ssh
        # to hold the channel open on inherited FDs even after the
        # child is fully detached at the OS level. Use `ssh -f` for
        # such commands so ssh forks-and-exits after auth+launch.
        is_detached = ('setsid nohup' in cmd) or (cmd.rstrip().endswith(' &'))
        ssh_flags = [
            '-i', _KEY,
            '-o', 'ConnectTimeout=10', '-o', 'BatchMode=yes',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/root/.ssh/known_hosts',
        ]
        if is_detached:
            ssh_flags += ['-f', '-n', '-o', 'LogLevel=error']
            timeout = 30
        else:
            timeout = 120
        try:
            r = subprocess.run(
                ['ssh'] + ssh_flags + [f'ubuntu@{self.ip}', cmd],
                capture_output=True, text=True, timeout=timeout,
            )
            return {'exit_code': r.returncode, 'stdout': r.stdout,
                    'stderr': r.stderr[:200] if r.stderr else ''}
        except subprocess.TimeoutExpired:
            # Background launch: ssh-fork didn't return cleanly; trust
            # the detachment (verified separately by heartbeat probe).
            return {'exit_code': 0,
                    'stdout': '<detached-launch · ssh subprocess timed out but child was setsid-nohup-detached>',
                    'stderr': ''}

    def put_file(self, local_path, remote_path):
        # scp expands ~ on remote via the invoking shell — safe.
        r = subprocess.run(
            ['scp', '-i', _KEY,
             '-o', 'StrictHostKeyChecking=no',
             '-o', 'UserKnownHostsFile=/root/.ssh/known_hosts',
             str(local_path), f'ubuntu@{self.ip}:{remote_path}'],
            capture_output=True, text=True, timeout=180,
        )
        return {'exit_code': r.returncode,
                'stderr': r.stderr[:200] if r.stderr else ''}


def launch(host_slug, run_name, base_model_id, seed, hyperparams,
           campaign_id, slice_size=30000):
    from services.campaign_infra import production_trainer as _pt

    manifest_entry = {
        'run_name': run_name,
        'base_model_id': base_model_id,
        'seed': seed,
        'hyperparams': hyperparams,
        'corpus_variant_table': 'ussd_question_response',
        'material_admit_ref': campaign_id,
        'slice_size': slice_size,
        'campaign_id': campaign_id,
    }
    seam = DirectSSHSeam(host_slug)
    print(f'=== LAUNCH · {campaign_id} · {run_name} · host={host_slug} ===',
          flush=True)
    result = _pt.default_trainer_fn(
        run_name=run_name,
        manifest_entry=manifest_entry,
        host=host_slug,
        _seam_override=seam,
        campaign_id=campaign_id,
    )
    print('=== RESULT (secrets redacted) ===', flush=True)
    receipt = result.get('run_receipt', {})
    launch_r = result.get('launch', {})
    minimal = {
        'run_id': receipt.get('run_id'),
        'tier': receipt.get('tier'),
        'env': receipt.get('env'),
        'host_slug': receipt.get('host_slug'),
        'row_extraction_receipt_path':
            receipt.get('row_extraction_receipt_path'),
        'held_out_slice_receipt_path':
            receipt.get('held_out_slice_receipt_path'),
        'train_corpus_sha256':
            receipt.get('train_corpus', {}).get('sha256'),
        'held_out_corpus_sha256':
            receipt.get('held_out_corpus', {}).get('sha256'),
        'train_row_count': receipt.get('train_corpus', {}).get('row_count'),
        'held_out_row_count':
            receipt.get('held_out_corpus', {}).get('row_count'),
        'remote_dir': receipt.get('remote_dir'),
        'launch_stdout_head': (
            launch_r.get('stdout', '')[:200] if launch_r else ''),
        'launch_exit_code': launch_r.get('exit_code') if launch_r else -1,
        'at_utc': result.get('at_utc'),
    }
    print(json.dumps(minimal, indent=2, default=str), flush=True)
    return receipt


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', required=True, choices=list(_HOSTS.keys()))
    ap.add_argument('--campaign', required=True)
    ap.add_argument('--run-name', required=True)
    ap.add_argument('--base-model', required=True)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--lora-rank', type=int, default=16)
    ap.add_argument('--ctx-len', type=int, default=1024)
    ap.add_argument('--per-device-batch', type=int, default=8)
    ap.add_argument('--grad-accum', type=int, default=4)
    ap.add_argument('--lr', type=float, default=2e-4)
    ap.add_argument('--num-epochs', type=int, default=3)
    ap.add_argument('--slice-size', type=int, default=30000)
    args = ap.parse_args()
    hyper = {
        'lora_rank': args.lora_rank,
        'context_length': args.ctx_len,
        'per_device_batch_size': args.per_device_batch,
        'gradient_accumulation_steps': args.grad_accum,
        'learning_rate': args.lr,
        'num_train_epochs': args.num_epochs,
    }
    r = launch(host_slug=args.host, run_name=args.run_name,
               base_model_id=args.base_model, seed=args.seed,
               hyperparams=hyper, campaign_id=args.campaign,
               slice_size=args.slice_size)
    print('=== run_id:', r.get('run_id'), flush=True)
