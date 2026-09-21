"""campaign_infra.production_trainer — default trainer_fn binding.

Wires services.shield_train.pipeline.execute_governed_lora_run to real
production dependencies:
  - real backend_execute  via services.connect.rds_data_submit
                          (the exempted boto3 seam)
  - real ssh_seam adapter over services.training_runner.ssh_seam
                          (execute_remote_command + connect())

Owner ruling verbatim (2026-09-06T~13:XXZ):
    "WIRE trainer_fn into campaign_infra.run_queue for production:
     the campaign runner's injected trainer_fn becomes the real on-host
     invocation via the seam. Keep injection (testability) — production
     wiring is just the default binding."

Injection preserved: `default_trainer_fn` accepts optional
`_seam_override` and `_backend_override` kwargs so tests can bypass live
SSH and RDS.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# AWS custody credential loader (never logs values)
# ---------------------------------------------------------------------------

def _load_aws_credentials_from_custody(
    custody_path: Optional[str] = None,
) -> Dict[str, str]:
    """Load AWS creds from the owner-approved custody file at
    `AKKI_LORA_CREDS_PATH` (default
    `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json`).

    Custody-file convention matches services.connect.rds_data_submit's
    `_write_standing_creds` contract (mode 0600, git-ignored via
    estate_keys/.gitignore). NEVER logs values.
    """
    p = Path(custody_path or os.environ.get(
        "AKKI_LORA_CREDS_PATH",
        "/app/backend/estate_keys/data_sources/db-restore-603-cluster.json",
    ))
    if not p.exists():
        raise FileNotFoundError(
            f"AWS credentials custody file missing at {p!s}. "
            f"Set AKKI_LORA_CREDS_PATH env or ensure the default file "
            f"exists (banked by services.connect.rds_data_submit._write_standing_creds)."
        )
    creds = json.loads(p.read_text(encoding="utf-8"))
    for required in ("aws_access_key_id", "aws_secret_access_key",
                     "region", "cluster_arn", "secret_arn", "database"):
        if not creds.get(required):
            raise ValueError(
                f"AWS custody file missing required key: {required!r} "
                f"(path: {p!s})"
            )
    return creds


# ---------------------------------------------------------------------------
# Backend execute — Aurora Data API adapter (routes through exempted seam)
# ---------------------------------------------------------------------------

def _build_backend_execute(
    region: str,
    cluster_arn: str,
    secret_arn: str,
    database: str,
) -> Callable:
    """Return a backend_execute(sql, params) callable that hits the
    Aurora Data API. Routes boto3 through services.connect.rds_data_submit
    (the exempted seam per test_no_boto3_import_outside_chokepoint).

    Pagination: RDS Data API's ExecuteStatement enforces a 1 MB response
    cap. When the SQL carries a trailing `LIMIT N` with N > page_size,
    the callable transparently batches via `LIMIT page_size OFFSET k`
    calls and stitches the rows in-order. page_size default is 1000
    (typically << 1 MB for our 3-column non-PII text corpora); override
    via env `AKKI_RDS_PAGE_SIZE`. Preserves the single-call contract
    for small queries + the ORDER BY-based determinism.
    """
    import re
    # Lazy import — keeps the module-scope free of boto3 references and
    # keeps unit-test collection cheap.
    from services.connect import rds_data_submit as _rds
    client = _rds.get_rds_data_client(region)
    _page_size = int(os.environ.get("AKKI_RDS_PAGE_SIZE", "1000"))

    def _params_for_api(params):
        param_list = []
        for k, v in (params or {}).items():
            if isinstance(v, bool):
                param_list.append({"name": k, "value": {"booleanValue": v}})
            elif isinstance(v, int):
                param_list.append({"name": k, "value": {"longValue": v}})
            elif isinstance(v, float):
                param_list.append({"name": k, "value": {"doubleValue": v}})
            else:
                param_list.append({"name": k, "value": {"stringValue": str(v)}})
        return param_list

    def _parse_records(r):
        records = r.get("records") or []
        cmeta = r.get("columnMetadata") or []
        cnames = [m.get("name") or m.get("label", f"col_{i}")
                  for i, m in enumerate(cmeta)]
        rows: list = []
        for row in records:
            d: Dict[str, Any] = {}
            for i, cell in enumerate(row):
                name = cnames[i] if i < len(cnames) else f"col_{i}"
                if not isinstance(cell, dict):
                    d[name] = cell
                elif cell.get("isNull"):
                    d[name] = None
                elif "stringValue" in cell:
                    d[name] = cell["stringValue"]
                elif "longValue" in cell:
                    d[name] = cell["longValue"]
                elif "doubleValue" in cell:
                    d[name] = cell["doubleValue"]
                elif "booleanValue" in cell:
                    d[name] = cell["booleanValue"]
                else:
                    d[name] = None
            rows.append(d)
        return rows

    _LIMIT_RE = re.compile(r"\s+LIMIT\s+(\d+)\s*$", re.IGNORECASE)

    def _exec(sql: str, params: Dict[str, Any]) -> list:
        m = _LIMIT_RE.search(sql)
        total_limit = int(m.group(1)) if m else -1

        # No pagination needed for small queries (or unlimited — caller's
        # responsibility if they omit LIMIT on a big table; page-size
        # cap still applies per-call so we still batch if unlimited).
        if 0 < total_limit <= _page_size:
            kwargs = {
                "resourceArn": cluster_arn,
                "secretArn": secret_arn,
                "database": database,
                "sql": sql,
                "includeResultMetadata": True,
            }
            plist = _params_for_api(params)
            if plist:
                kwargs["parameters"] = plist
            return _parse_records(client.execute_statement(**kwargs))

        # Paginated path: strip trailing LIMIT (if any), batch by
        # (page_size OFFSET k) until we hit total_limit or exhaust.
        base_sql = sql[:m.start()] if m else sql
        cap = total_limit if total_limit > 0 else (1 << 62)  # ~unbounded
        rows: list = []
        offset = 0
        while offset < cap:
            batch = min(_page_size, cap - offset)
            paged_sql = f"{base_sql} LIMIT {batch} OFFSET {offset}"
            kwargs = {
                "resourceArn": cluster_arn,
                "secretArn": secret_arn,
                "database": database,
                "sql": paged_sql,
                "includeResultMetadata": True,
            }
            plist = _params_for_api(params)
            if plist:
                kwargs["parameters"] = plist
            page_rows = _parse_records(client.execute_statement(**kwargs))
            rows.extend(page_rows)
            if len(page_rows) < batch:
                break  # source exhausted before cap
            offset += batch
        return rows

    return _exec


# ---------------------------------------------------------------------------
# SSH seam adapter — duck-typed for shield_train.pipeline.stage_corpus_to_host
# ---------------------------------------------------------------------------

class _SeamAdapter:
    """Adapter over services.training_runner.ssh_seam.

    Exposes:
      - run(cmd) -> {"exit_code": int, "stdout": str}
      - put_file(local_path, remote_path) -> {"exit_code": int}

    Both route through the ssh_seam.connect() paramiko client so that
    every operation is a receipt-emitting governed action (never a raw
    subprocess call to a system ssh binary).
    """

    def __init__(self, host_slug: str):
        self.host_slug = host_slug

    def run(self, cmd: str) -> Dict[str, Any]:
        from services.training_runner.ssh_seam import execute_remote_command
        r = execute_remote_command(
            host_slug=self.host_slug,
            command=cmd,
            purpose="lora_stage_or_launch",
        )
        return {"exit_code": r.rc, "stdout": r.stdout_redacted}

    def put_file(self, local_path: str, remote_path: str) -> Dict[str, Any]:
        # SFTP put through the seam's paramiko client. Never shells out.
        from services.training_runner.ssh_seam import connect as _seam_connect
        client = _seam_connect(self.host_slug)
        try:
            sftp = client.open_sftp()
            try:
                sftp.put(str(local_path), str(remote_path))
            finally:
                sftp.close()
        finally:
            client.close()
        return {"exit_code": 0}


# ---------------------------------------------------------------------------
# Corpus variant resolver — maps manifest corpus_variant strings to (tables, dedup)
# ---------------------------------------------------------------------------

# W-Multi-Table-Extract: 2026-09-06 · maps manifest `corpus_variant` to
# (tables_list, dedup_flag). Refuses on unknown variants (silence + guess
# would silently rewrite the owner-approved campaign design; see
# phase0/campaign_drafts/campaign_b_run_order_reconciliation.json).
_CORPUS_VARIANT_MAP = {
    "ussd_deduplicated": (["ussd_question_response"], True),
    "ussd_plus_sms_deduplicated": (["ussd_question_response", "sms_log"], True),
    "ussd_plus_sms_raw": (["ussd_question_response", "sms_log"], False),
}


def resolve_corpus_variant(corpus_variant: str):
    """Return (tables: list[str], dedup: bool) for a manifest
    corpus_variant string. Refuses on unknown variants."""
    if corpus_variant not in _CORPUS_VARIANT_MAP:
        raise ValueError(
            f"unknown corpus_variant {corpus_variant!r}. "
            f"Known variants: {sorted(_CORPUS_VARIANT_MAP)!r}. "
            f"Adding a new variant requires an authored formatter in "
            f"services.shield_train.multi_table._TABLE_FORMATTERS + policy "
            f"classifications for all constituent tables."
        )
    tables, dedup = _CORPUS_VARIANT_MAP[corpus_variant]
    return list(tables), dedup


# ---------------------------------------------------------------------------
# Default trainer_fn — the run_queue production binding
# ---------------------------------------------------------------------------

def default_trainer_fn(
    run_name: str,
    manifest_entry: Dict[str, Any],
    host: str,
    _seam_override: Any = None,
    _backend_override: Callable = None,
    campaign_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Default production binding for
    campaign_infra.run_queue.execute_campaign(trainer_fn=...).

    Composition:
      1. Load AWS creds from custody file (never logged).
      2. Build backend_execute over rds-data-submit seam.
      3. Build ssh_seam adapter over training_runner.ssh_seam.
      4. Call execute_governed_lora_run() to extract + stage corpora.
      5. Invoke on-host trainer detached via ssh_seam remote-exec with
         setsid nohup (survives cron parent exit).
      6. Return run handle {run_receipt, launch, at_utc}.

    Test overrides:
      _seam_override: fake seam (bypasses live SSH)
      _backend_override: fake backend_execute (bypasses live RDS)
    """
    from services.shield_train import pipeline as _p

    prior_env: Dict[str, Optional[str]] = {}
    if _backend_override is None:
        creds = _load_aws_credentials_from_custody()
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
                  "AWS_DEFAULT_REGION"):
            prior_env[k] = os.environ.get(k)
        os.environ["AWS_ACCESS_KEY_ID"] = creds["aws_access_key_id"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = creds["aws_secret_access_key"]
        os.environ["AWS_DEFAULT_REGION"] = creds["region"]
        try:
            backend_execute = _build_backend_execute(
                region=creds["region"],
                cluster_arn=creds["cluster_arn"],
                secret_arn=creds["secret_arn"],
                database=creds.get("database")
                or os.environ.get("AKKI_LORA_DATABASE", "digicow_live"),
            )
        except Exception:
            for k, v in prior_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
            raise
    else:
        backend_execute = _backend_override

    try:
        ssh_seam = _seam_override or _SeamAdapter(host_slug=host)

        # Step 1-8 of §B composition: extract + build corpora + bank
        # held-out hash + stage to host.
        run_receipt = _p.execute_governed_lora_run(
            tier=os.environ.get("AKKI_LORA_MASKING_TIER", "t1_full_mask"),
            recipe_version=str(manifest_entry.get("run_name", run_name)),
            base_model_id=manifest_entry.get(
                "base_model_id", "Qwen/Qwen2.5-0.5B"),
            material_admit_ref=manifest_entry.get(
                "material_admit_ref", f"campaign-{run_name}"),
            host_slug=host,
            table_context=manifest_entry.get(
                "corpus_variant_table", "ussd_question_response"),
            slice_size=int(manifest_entry.get("slice_size", 0)),
            backend_execute=backend_execute,
            ssh_seam=ssh_seam,
        )

        # Step 9: invoke on-host trainer detached.
        hyper: Dict[str, Any] = manifest_entry.get("hyperparams", {}) or {}
        remote_dir = run_receipt["remote_dir"]
        corpus_path = f"{remote_dir}/train_corpus.jsonl"
        held_out_path = f"{remote_dir}/held_out_corpus.jsonl"

        trainer_cmd_parts = [
            "cd ~ &&",
            "setsid nohup python3 ~/akki_journal/on_host_trainer.py",
            f"--run-id {run_receipt['run_id']}",
            f"--run-dir {remote_dir}",
            f"--campaign-id {campaign_id or manifest_entry.get('campaign_id', 'unknown')}",
            f"--run-name {run_name}",
            f"--corpus {corpus_path}",
            f"--held-out {held_out_path}",
            f"--base-model {manifest_entry.get('base_model_id', 'Qwen/Qwen2.5-0.5B')}",
            f"--seed {int(manifest_entry.get('seed', 1))}",
            f"--lora-rank {int(hyper.get('lora_rank', 16))}",
            f"--ctx-len {int(hyper.get('context_length', 1024))}",
            f"--per-device-batch {int(hyper.get('per_device_batch_size', 2))}",
            f"--grad-accum {int(hyper.get('gradient_accumulation_steps', 16))}",
            f"--lr {float(hyper.get('learning_rate', 2e-4))}",
            f"--num-epochs {int(hyper.get('num_train_epochs', 3))}",
            f">> {remote_dir}/trainer_stdout.log 2>&1 &",
            "echo $!",
        ]
        launch_cmd = " ".join(trainer_cmd_parts)
        launch_r = ssh_seam.run(launch_cmd)

        return {
            "run_receipt": run_receipt,
            "launch": launch_r,
            "at_utc": _iso_utc(),
            "run_name": run_name,
            "host": host,
        }
    finally:
        # Retire AWS env vars.
        for k, v in prior_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
