"""Read-only control-ledger verification and non-secret assessment receipt banking."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / "backend/.env")
sys.path.insert(0, str(ROOT / "backend/vendored/extraction_akki/backend"))
from services.ledger_writer.mongo_control import decode_row, verify_event
from services.ledger_verifier.verify import verify_chain

out = ROOT / "assessment_workspace/phase0/drill_receipts/dap_operational_v1"
out.mkdir(parents=True, exist_ok=True)
with MongoClient(os.environ["MONGO_URL"]) as client:
    events = list(client[os.environ["DB_NAME"]]["ledger_v1_control_events"].find({}, {"_id": 0}).sort("row.seq", 1))
groups = {}
for event in events:
    verify_event(event)
    groups.setdefault(event["row"]["tenant_id"], []).append(decode_row(event["row"]))
chains = [asdict(verify_chain(rows_in_seq_order=rows)) for rows in groups.values()]
assert all(r["break_at_seq"] is None for r in chains)

original = ["frontend/src/components/prototype/generated/dap.json", "frontend/src/components/prototype/generated/os.json", "frontend/src/components/prototype/OwnerMarkup.jsx"]
source_proofs = []
for name in original:
    current = (ROOT / name).read_bytes()
    previous = subprocess.run(["git", "show", f"HEAD:{name}"], cwd=ROOT, capture_output=True, check=True).stdout
    assert previous == current, f"Original source changed: {name}"
    source_proofs.append({"path": name, "sha256": hashlib.sha256(current).hexdigest(), "unchanged_from_head": True})

for report in ["iteration_9.json", "iteration_10.json"]:
    shutil.copy2(ROOT / "test_reports" / report, out / report)
screens = Path("/root/.emergent/automation_output/20260926_011455")
for filename in ["dap-verified-desktop-history.jpeg", "dap-verified-mobile-wrap.jpeg"]:
    shutil.copy2(screens / filename, out / filename)
shutil.copy2(ROOT / "test_reports/dap_operational_desktop_1920x800.jpeg", out / "os-work-desktop.jpeg")
for run in ["20260926_010727", "20260926_011615"]:
    source = Path("/root/.emergent/automation_output") / run
    shutil.copy2(source / "test_script.py", out / f"browser_{run}.py")
    shutil.copy2(source / f"console_{run}.log", out / f"browser_{run}.log")

receipt = {
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "scope": "Control-plane metadata only. No source estate, GPU, provider or model execution.",
    "canonical_chain_verification": chains,
    "all_payload_hashes_verified": True,
    "canonical_row_field_counts": sorted({len(e["row"]) for e in events}),
    "original_source_proofs": source_proofs,
    "test_runs": {"run1": {"passed": 146, "skipped": 2}, "run2": {"passed": 146, "skipped": 2}},
    "browser_assertions": {
        "auth_transitions": "operator -> signed-out -> analyst: overview 200 x4, overview401 x0; analyst disabled/no operator rows",
        "worst_case_mobile": "390px: long objective scrollWidth337/clientWidth337/height622, overflow-wrap anywhere; menu absent while drawer open",
        "desktop": "1920px: loaded history, OVERFLOW[]",
        "close": "20260926_011615: named close control hides drawer, mobile navigation visible again",
        "corrected_harness_issues": "Initial screenshot captured loading; retaken after drawer visible. Case-sensitive uppercase label assertion and wrong prototype close locator corrected; final interactions PASS.",
    },
    "mocked_test_boundaries": ["isolated fault injection", "entitlement/admission event fixtures", "skill prerequisite gate/refusal fixtures", "existing census transport units"],
    "not_proven": ["approved extraction", "real skill answer", "live entitlement grant", "executor stop/retry", "verified result retrieval", "full platform completeness"],
}
(out / "VERIFICATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name != "MANIFEST.json"}
(out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"chain_heads": chains, "source_proofs": source_proofs, "banked_files": len(manifest)}, indent=2))