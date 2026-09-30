"""services.business_continuity.ledger_archive — Tier 2/3 mechanism and the M8-T3 Ledger recovery drill.

Archive: the hash-chained control Ledger (`ledger_v1_control_events`) is read with per-row integrity verification and written
ONCE into the WORM tier (versioned key, 0444, sha-256 receipt; overwrite refuses structurally) and, when a custody host is named,
copied off the application infrastructure with the remote digest verified.

Restore drill: an archive is restored into an ISOLATED drill database, every restored row re-verified (payload digest, row hash,
prev_hash linkage, seq continuity), row counts and per-tenant heads compared to the archive and to the live Ledger (measured
committed-write loss), the restore time measured against the ratified Tier 2 RTO and the S-10 3,600 s bound, and the restored
head COUNTERSIGNED by an Ed25519 key held on a GPU host that is not the Ledger writer's infrastructure (BC-1). The signature is
verified in E1 before the ContinuityAttestation is written. A stored attestation without these measurements is not restoration.
"""
import base64
import gzip
import hashlib
import json
import os
import shlex
import time
from datetime import datetime, timezone
from pathlib import Path

from services.business_continuity import policy
from services.ledger_writer import mongo_control
from services.ledger_writer.main import compute_row_hash

WITNESS_ID = "wi_akki_vm_ledger_countersigner"
WITNESS_KEY_DIR = "~/.akki_witness"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _worm_dir():
    path = Path(os.environ.get("BC_WORM_DIR", "/app/assessment_workspace/phase0/worm")) / mongo_control.COLLECTION
    path.mkdir(parents=True, exist_ok=True)
    return path


def _receipts_dir():
    path = Path(os.environ.get("BC_DRILL_RECEIPTS_DIR", "/app/assessment_workspace/phase0/bc_drill_receipts"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _heads(events):
    heads = {}
    for e in events:
        row = e["row"]
        cur = heads.get(row["tenant_id"])
        if cur is None or row["seq"] > cur["seq"]:
            heads[row["tenant_id"]] = {"seq": row["seq"], "hash": row["hash"]}
    return heads


def worm_write(key, raw, meta):
    """BC-3-WORM-INV-01/02/03: versioned key, immutability receipt, refuse overwrite, retention set at write time."""
    path = _worm_dir() / key
    if path.exists() or path.with_suffix(path.suffix + ".receipt.json").exists():
        raise FileExistsError("WORM_KEY_EXISTS:" + key)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw); os.replace(tmp, path); os.chmod(path, 0o444)
    receipt = {"key": key, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "written_at": now(), "object_lock_mode": policy.TIERS["tier_3_worm_artifacts"]["mechanism"]["object_lock_mode"],
               "retention": "permanent (local COMPLIANCE emulation until the owner-provisioned bucket exists)", "immutable": True, **meta}
    rpath = path.with_suffix(path.suffix + ".receipt.json")
    rpath.write_text(json.dumps(receipt, indent=1)); os.chmod(rpath, 0o444)
    return receipt


def worm_list():
    out = []
    for r in sorted(_worm_dir().glob("*.receipt.json")):
        try:
            out.append(json.loads(r.read_text()))
        except (OSError, ValueError):
            continue
    return out


def _remote_copy(host, key, raw):
    """Off-infrastructure copy on a custody host through the pinned SSH seam; remote digest verified before the receipt is written."""
    from services.census_autonomy.remote_dispatch import _connect
    remote_dir = f"~/akki_worm/{mongo_control.COLLECTION}"
    remote_path = f"{remote_dir}/{key}"
    client, _cfg = _connect(host, 20)
    try:
        channel = client.get_transport().open_session(timeout=15); channel.settimeout(120)
        channel.exec_command(f"mkdir -p {remote_dir} && cat > {remote_path}.tmp && mv {remote_path}.tmp {remote_path} && chmod 0444 {remote_path} && sha256sum {remote_path}")
        channel.sendall(raw); channel.shutdown_write()
        out = bytearray()
        deadline = time.time() + 120
        while not (channel.exit_status_ready() and not channel.recv_ready()):
            if channel.recv_ready():
                out.extend(channel.recv(65536))
            if time.time() > deadline:
                raise TimeoutError("REMOTE_COPY_TIMEOUT")
            time.sleep(0.05)
        while channel.recv_ready():
            out.extend(channel.recv(65536))
        rc = channel.recv_exit_status()
    finally:
        client.close()
    remote_sha = out.decode(errors="replace").split()[0] if out else None
    return {"host": host, "remote_path": remote_path, "rc": rc, "remote_sha256": remote_sha, "verified": rc == 0 and remote_sha == hashlib.sha256(raw).hexdigest()}


async def archive(db, replicate_host=None):
    t0 = time.monotonic()
    events = await mongo_control.read_events(db, {})
    archived_at = now()
    payload = {"collection": mongo_control.COLLECTION, "archived_at": archived_at, "row_count": len(events), "heads": _heads(events), "events": events}
    raw = gzip.compress(json.dumps(payload, sort_keys=True, default=str).encode(), mtime=0)
    sha = hashlib.sha256(raw).hexdigest()
    key = f"{archived_at.replace(':', '').replace('-', '')}_{sha[:12]}.json.gz"
    receipt = worm_write(key, raw, {"collection": mongo_control.COLLECTION, "row_count": len(events), "tenants": len(payload["heads"]), "heads": payload["heads"], "archived_at": archived_at,
                                    "read_verify_seconds": round(time.monotonic() - t0, 3), "archive_window_bound_seconds": policy.TIERS["tier_2_ledgers_registry"]["mechanism"]["archive_window_seconds"]})
    if replicate_host:
        try:
            receipt["off_infrastructure_copy"] = _remote_copy(replicate_host, key, raw)
        except Exception as exc:
            receipt["off_infrastructure_copy"] = {"host": replicate_host, "verified": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}
        rpath = _worm_dir() / (key + ".receipt.json")
        os.chmod(rpath, 0o644); rpath.write_text(json.dumps(receipt, indent=1)); os.chmod(rpath, 0o444)
    return receipt


def _load_archive(key=None):
    receipts = worm_list()
    if not receipts:
        raise FileNotFoundError("NO_LEDGER_ARCHIVE_ON_RECORD")
    receipt = next((r for r in receipts if r["key"] == key), None) if key else receipts[-1]
    if receipt is None:
        raise FileNotFoundError("ARCHIVE_KEY_NOT_ON_RECORD:" + str(key))
    raw = (_worm_dir() / receipt["key"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != receipt["sha256"]:
        raise ValueError("ARCHIVE_CHECKSUM_MISMATCH:" + receipt["key"])
    return receipt, json.loads(gzip.decompress(raw))


def verify_chain(events):
    """Row-by-row: payload digest, row hash, prev_hash linkage and seq continuity per tenant."""
    by_tenant = {}
    for e in events:
        mongo_control.verify_event(e)
        by_tenant.setdefault(e["row"]["tenant_id"], []).append(e)
    breaks = []
    for tenant, rows in by_tenant.items():
        rows.sort(key=lambda e: e["row"]["seq"])
        prev = None
        for e in rows:
            row = e["row"]
            if prev is None:
                if row["seq"] != 1:
                    breaks.append({"tenant": tenant, "seq": row["seq"], "kind": "first_seq_not_1"})
            else:
                if row["seq"] != prev["seq"] + 1:
                    breaks.append({"tenant": tenant, "seq": row["seq"], "kind": "seq_gap"})
                if row["prev_hash"] != prev["hash"]:
                    breaks.append({"tenant": tenant, "seq": row["seq"], "kind": "prev_hash_mismatch"})
            prev = row
    return {"rows": len(events), "tenants": len(by_tenant), "breaks": breaks, "intact": not breaks}


def _witness_countersign(host, statement):
    """Ed25519 signature produced on the custody host over the canonical statement; the public key is returned and the signature is verified here."""
    from services.training_runner.ssh_seam import execute_remote_command
    canonical = json.dumps(statement, sort_keys=True, separators=(",", ":")).encode()
    b64 = base64.b64encode(canonical).decode()
    d = WITNESS_KEY_DIR
    command = (f"mkdir -p {d} && chmod 700 {d} && [ -f {d}/ed25519.pem ] || openssl genpkey -algorithm ed25519 -out {d}/ed25519.pem >/dev/null 2>&1; chmod 600 {d}/ed25519.pem; "
               f"echo {b64} | base64 -d > {d}/stmt.$$ && openssl pkeyutl -sign -inkey {d}/ed25519.pem -rawin -in {d}/stmt.$$ | base64 -w0; echo; echo __PUB__; "
               f"openssl pkey -in {d}/ed25519.pem -pubout; rm -f {d}/stmt.$$; echo __HOST__; hostname")
    result = execute_remote_command(host, command, purpose="bc_ledger_countersign", timeout=60)
    sig_text, _, rest = result.stdout_redacted.partition("__PUB__")
    pub_pem, _, hostname = rest.partition("__HOST__")
    signature = sig_text.strip().splitlines()[-1] if sig_text.strip() else ""
    verified = False
    try:
        from cryptography.hazmat.primitives import serialization
        public_key = serialization.load_pem_public_key(pub_pem.strip().encode())
        public_key.verify(base64.b64decode(signature), canonical)
        verified = True
    except Exception as exc:
        verified = False
        error = f"{type(exc).__name__}: {str(exc)[:120]}"
    fingerprint = hashlib.sha256(pub_pem.strip().encode()).hexdigest()[:32]
    return {"witness_host": host, "witness_hostname": hostname.strip(), "signature_ed25519_b64": signature, "public_key_pem": pub_pem.strip(), "public_key_fingerprint": fingerprint,
            "statement_sha256": hashlib.sha256(canonical).hexdigest(), "verified_in_e1": verified, "rc": result.rc, "receipt_id": result.receipt_id, **({} if verified else {"error": error})}


def _ensure_witness(fingerprint, host):
    from services.watch import witness
    if witness._identity_on_record(WITNESS_ID) is None:
        witness.register_identity({"witness_id": WITNESS_ID, "registered_at": now(), "signing_material_ref": f"ed25519:{fingerprint} · private key held only on {host} (~/.akki_witness/ed25519.pem, 0600)",
                                   "independent_of_authorities": True,
                                   "registration_note": (f"Ledger continuity countersigner on custody host {host}: separate machine from the application pod and from the MongoDB Ledger writer; "
                                                         "holds no Watch credentials and no governance credentials; signs restored-head statements only; cannot act on the estate.")})
    return WITNESS_ID


async def restore_drill(db_client, live_db, archive_key=None, witness_host="akki-vm", actor=None):
    from services.watch import continuity
    started = now(); t_all = time.monotonic()
    receipt_meta, archive_doc = _load_archive(archive_key)
    events = archive_doc["events"]
    live_events = await mongo_control.read_events(live_db, {})
    live_heads, archive_heads = _heads(live_events), archive_doc["heads"]
    loss = {tenant: {"archive_seq": archive_heads.get(tenant, {}).get("seq", 0), "live_seq": h["seq"], "committed_rows_after_archive": h["seq"] - archive_heads.get(tenant, {}).get("seq", 0)}
            for tenant, h in live_heads.items() if h["seq"] != archive_heads.get(tenant, {}).get("seq", 0)}
    drill_name = os.environ["DB_NAME"] + "_bc_drill"
    drill_db = db_client[drill_name]
    t0 = time.monotonic()
    await drill_db[mongo_control.COLLECTION].drop()
    await mongo_control.ensure_indexes(drill_db)
    for i in range(0, len(events), 500):
        await drill_db[mongo_control.COLLECTION].insert_many([dict(e) for e in events[i:i + 500]])
    restored = await mongo_control.read_events(drill_db, {})
    restore_seconds = round(time.monotonic() - t0, 3)
    chain = verify_chain(restored)
    restored_heads = _heads(restored)
    checks = {"row_count_archive": len(events), "row_count_restored": len(restored), "row_counts_match": len(restored) == len(events),
              "heads_match_archive": restored_heads == archive_heads, "chain_intact": chain["intact"], "chain_breaks": chain["breaks"][:20],
              "archive_checksum_verified": True, "archive_key": receipt_meta["key"], "archive_sha256": receipt_meta["sha256"]}
    tier2 = policy.TIERS["tier_2_ledgers_registry"]
    statement = {"drill": "M8-T3 ledger recovery", "archive_sha256": receipt_meta["sha256"], "restored_row_count": len(restored), "restored_heads": restored_heads, "chain_intact": chain["intact"],
                 "restored_into": drill_name, "restore_seconds": restore_seconds, "at": now()}
    countersign = _witness_countersign(witness_host, statement)
    witness_id = _ensure_witness(countersign["public_key_fingerprint"], witness_host) if countersign["verified_in_e1"] else None
    outcome = "matches" if all([checks["row_counts_match"], checks["heads_match_archive"], checks["chain_intact"], countersign["verified_in_e1"]]) else "diverges"
    total_seconds = round(time.monotonic() - t_all, 3)
    attestation = None
    if witness_id:
        stamp = started.replace(":", "").replace("-", "").lower()
        payload = {"attestation_id": f"ca_{stamp[:8]}_{stamp[9:15]}_ledger_pitr", "attested_at": now(), "attested_by": witness_id, "attested_scope": "all",
                   "rto_target_seconds": str(continuity.load_policy()["rto_target_seconds"]), "verification_mechanism": continuity.load_policy()["verification_mechanism"],
                   "witness_signature": "ed25519:" + countersign["signature_ed25519_b64"], "outcome": outcome,
                   "summary": (f"Restored {len(restored)} control-Ledger rows ({chain['tenants']} tenants) from WORM archive {receipt_meta['key']} into isolated {drill_name} in {restore_seconds}s; "
                               f"chain {'intact' if chain['intact'] else 'BROKEN'}; heads {'match' if checks['heads_match_archive'] else 'DIVERGE'}; committed rows written after the archive: "
                               f"{sum(v['committed_rows_after_archive'] for v in loss.values())}; countersigned on {countersign['witness_hostname']} (Ed25519 {countersign['public_key_fingerprint'][:16]}).")}
        try:
            attestation = continuity.write_attestation(payload).model_dump()
        except Exception as exc:
            attestation = {"error": f"{type(exc).__name__}: {str(exc)[:200]}"}
    receipt = {"drill": "M8-T3 Ledger recovery (point-in-time restore · independent countersign)", "at": started, "actor": actor, "archive": {k: receipt_meta.get(k) for k in ("key", "sha256", "row_count", "archived_at", "off_infrastructure_copy")},
               "measured": {"restore_seconds": restore_seconds, "total_drill_seconds": total_seconds, "tier2_rto_same_host_seconds": tier2["rto"]["same_host_seconds"], "s10_ledger_rto_seconds": 3600,
                            "within_tier2_rto": restore_seconds <= tier2["rto"]["same_host_seconds"], "within_s10": total_seconds <= 3600,
                            "committed_write_loss_vs_live": loss, "committed_rows_after_archive_total": sum(v["committed_rows_after_archive"] for v in loss.values()), "live_row_count": len(live_events)},
               "integrity_checks": checks, "countersign": {k: v for k, v in countersign.items() if k != "public_key_pem"}, "witness_id": witness_id, "attestation": attestation,
               "isolation": {"restored_into": drill_name, "live_database_untouched": True}, "policy_ref": tier2["ratification_ref"]}
    receipt["verdict"] = "PASS" if outcome == "matches" and receipt["measured"]["within_s10"] else "FAIL"
    path = _receipts_dir() / f"{started.replace(':', '').replace('-', '')}_m8t3_ledger_pitr.json"
    path.write_text(json.dumps(receipt, indent=1, default=str)); receipt["receipt_path"] = str(path)
    return receipt


async def head(db, tenant_id):
    events = await mongo_control.read_events(db, {"row.tenant_id": tenant_id})
    heads = _heads(events)
    return {"tenant_id": tenant_id, "rows": len(events), "head": heads.get(tenant_id), "chain": verify_chain(events)}
