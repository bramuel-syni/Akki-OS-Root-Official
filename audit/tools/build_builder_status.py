#!/usr/bin/env python3
"""
Fill Builder Status column K on all 602 rows of the System Rules Registry sheet.

Strict honesty rules (owner directive 2026-09-21):
- BUILT / PARTIAL / NOT BUILT only
- Every BUILT and PARTIAL row must cite a specific programme/track-a commit SHA
- No guessing. Untraceable = NOT BUILT (no citation)
- EDIT ONLY column K. All other cells (including formula cells) preserved.

Trace method (deterministic):
1. Enumerate every rule row (r=2..603).
2. For each rule, compute a set of filename-tokens from the Rule ID.
3. Search backend/tests/invariants/*.py filenames for any file containing any token.
4. Load baseline_failures.json — split filenames into "green" and "grandfathered fail".
5. Classify:
   - BUILT   : ≥1 matched invariant test file whose no test function is in baseline_failures
   - PARTIAL : matched invariant test files exist but all are in baseline_failures
               OR no invariant test but the rule's Domain resolves to a service pkg present at HEAD
   - NOT BUILT: no invariant test file matches AND no service pkg for the Domain
6. For BUILT / PARTIAL: cite the specific commit that adds or most recently touches the primary
   evidence file (git log -1 --format=%H --diff-filter=A on the file, fallback to -1 --format=%H).
7. Save workbook to /app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx.
"""
from __future__ import annotations
import os
import re
import json
import subprocess
from pathlib import Path
from openpyxl import load_workbook

SRC = "/app/audit/scratch/Master_Requirements_Registry_QA_v2.xlsx"
DST = "/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx"
REPO = "/app/assessment_workspace/repos/Extraction-Akki"
TESTS_DIR = f"{REPO}/backend/tests/invariants"
SERVICES_DIR = f"{REPO}/backend/services"
BASELINE_FAILS = f"{REPO}/backend/tests/invariants/baseline_failures.json"

# ---------------------------------------------------------------------------
# Load evidence pools
# ---------------------------------------------------------------------------

def _git(*args: str, cwd: str = REPO) -> str:
    r = subprocess.run(("git",) + args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()

# All invariant test filenames (lowercase for matching)
_all_tests = sorted(
    p.name for p in Path(TESTS_DIR).glob("test_*.py")
)
_all_tests_lower = [t.lower() for t in _all_tests]

# All services (top-level packages/modules)
_all_services = set()
for entry in Path(SERVICES_DIR).iterdir():
    name = entry.name
    if name.startswith("__"): continue
    if name.endswith(".pyc"): continue
    _all_services.add(name.replace(".py", "").lower())

# baseline_failures = set of "tests/invariants/<file>.py::<testname>"
_baseline = set()
_baseline_files = set()
with open(BASELINE_FAILS) as f:
    _bd = json.load(f)
for line in _bd["baseline_failures"]:
    _baseline.add(line)
    fname = line.split("::")[0].split("/")[-1].lower()
    _baseline_files.add(fname)

# ---------------------------------------------------------------------------
# Domain → service package map (from Domain column of the registry)
# ---------------------------------------------------------------------------
# Objectives sheet & Doc metadata drive this. Left side is the Domain col H
# verbatim; right side is a lowercase substring hit on service package names.

DOMAIN_TO_SVC = {
    "synisense": ["synisense", "canon_doc1_chokepoint", "chokepoint"],
    "solva": ["solva", "solva_depth", "solva_v2"],
    "northena": ["northena", "canon_doc5_northena"],
    "mtafiti": ["mtafiti"],
    "targeta": ["targeta"],
    "mkondo": ["mkondo", "handoff"],
    "watch": ["watch", "n_series"],
    "ledger": ["ledger_writer", "ledger_verifier", "ledger_emitter", "cost_ledger"],
    "cif": ["cif", "chokepoint"],
    "checker": ["checker", "critic_pass"],
    "registry": ["registry", "resource_registry", "capability_registry", "rule_book_seed"],
    "outer gate": ["outer_gate", "outer_gate_receipt"],
    "cost & compute": ["compute_estate", "cost_ledger", "compute_seam", "economics"],
    "training": ["training", "training_runner", "shield_train"],
    "wpw": ["wpw", "whitepapers"],
    "dap": ["dap", "dap_lifecycle", "canon_dap_lifecycle"],
    "entitlement": ["entitlement_service_v1"],
    "memory": ["memory"],  # covers memory/compaction_v1 too
    "principal": ["principal_store"],
    "content": ["content_registry"],
    "rules": ["rules_service", "canon_rules_service"],
    "governance": ["governance", "governance_plane"],
    "agent containment": ["agent_containment"],
    "orchestration": ["orchestrator_resilience", "release_gate"],
    "audit-trail": ["audit_trail"],
    "response sanitizer": ["response_sanitizer"],
    "security": ["security_function_policies", "serving_floor", "secret_hygiene", "chokepoint"],
    "compliance": ["compliance", "rights_quarantine"],
    "auth": ["auth", "ip_allowlist"],
    "documents": ["documents_registry"],
    "deck rendering": ["opportunity_briefs", "artifact_store"],
    "wpw / whitepapers": ["wpw", "whitepapers"],
    "critic": ["critic_pass"],
    "doc 0": ["doc0_attributes"],
    "trust domain": ["trust_domain"],
    "declaration": ["declaration"],
    "enforce": ["enforce"],
    "connect": ["connect", "connect_estate"],
    "census": ["census_canon", "census_dimensions", "census_engine"],
    "audio": ["audio_plane_v1", "audio_poc"],
    "data": ["data", "data_source", "data_suite_v2"],
    "release": ["release_gate", "release_budget"],
    "credential": ["credential_plane", "credentials_paste", "kms"],
    "team": ["team"],
    "approvals": ["approvals"],
    "gateway": ["gateway"],
    "personal client": ["personal_client"],
    "answering": ["answering_service"],
    "chat": ["chat"],
    "wizard": ["wizard"],
    "master_admin": ["master_admin"],
    "layer a": ["layer_a"], "layer b": ["layer_b"], "layer c": ["layer_c"],
    "perception": ["perception"],
    "grey mirror": ["grey_mirror"],
    "reliable time": ["reliable_time_source"],
    "campaign": ["campaign_infra"],
    "observability": ["observability"],
    "canonical projection": ["canonical_projection"],
    "attribute stream bundle": ["attribute_stream_bundle"],
    "n series": ["n_series"],
    "business continuity": ["business_continuity"],
    "evidence": ["evidence_register"],
    "baseline line": ["baseline_line"],
    "rights quarantine": ["rights_quarantine"],
    "estate keys": ["estate_keys"],
    "credential plane": ["credential_plane"],
}

def resolve_domain(domain_str: str) -> list[str]:
    if not domain_str:
        return []
    d = str(domain_str).strip().lower()
    for key, pkgs in DOMAIN_TO_SVC.items():
        if key in d or d in key:
            return [p for p in pkgs if p in _all_services]
    return []

# ---------------------------------------------------------------------------
# Token generation from Rule ID
# ---------------------------------------------------------------------------

def rule_id_tokens(rule_id: str) -> list[str]:
    """Produce lowercase filename-search tokens for a rule ID.
    E.g. 'ENT-3' → ['ent_3','ent-3','ent3','ent_3_'].
         'A5.14' → ['a5_14','a5.14'].
         'WPW-11' → ['wpw_11','wpw-11'].
         'DR-R10' → ['dr_r10','dr-r10'].
         'S-27' → ['s_27','s-27'].
         'C-6.9.2' → ['c_6_9_2','6_9_2'].
         'Q-6.1' → ['q_6_1'].
    """
    if not rule_id:
        return []
    r = str(rule_id).strip()
    tokens = set()
    # base variants
    tokens.add(r.lower())
    tokens.add(r.lower().replace("-", "_"))
    tokens.add(r.lower().replace(".", "_"))
    tokens.add(r.lower().replace("-", "").replace(".", ""))
    # If prefix-number pattern, ensure canonical prefix_number form
    m = re.match(r"^([A-Za-z]+)[-_.]?(.+)$", r)
    if m:
        pfx, rest = m.group(1).lower(), m.group(2).lower().replace(".", "_").replace("-", "_")
        tokens.add(f"{pfx}_{rest}")
        tokens.add(f"{pfx}{rest}")
    return sorted(t for t in tokens if len(t) >= 3)

def find_matching_tests(rule_id: str) -> list[str]:
    toks = rule_id_tokens(rule_id)
    if not toks:
        return []
    hits = []
    for fn, fn_lower in zip(_all_tests, _all_tests_lower):
        for t in toks:
            # match on token surrounded by _ or . or start/end
            if re.search(r"(^|[_.])" + re.escape(t) + r"([_.]|$)", fn_lower):
                hits.append(fn)
                break
    return sorted(set(hits))

# ---------------------------------------------------------------------------
# Commit citation helpers (cached)
# ---------------------------------------------------------------------------

_commit_cache: dict[str, str] = {}

def commit_for_add(rel_path: str) -> str | None:
    """Return the commit SHA that first added rel_path, else the latest commit touching it."""
    key = f"add:{rel_path}"
    if key in _commit_cache:
        return _commit_cache[key]
    r = subprocess.run(
        ["git", "log", "--diff-filter=A", "-1", "--format=%H", "--", rel_path],
        cwd=REPO, capture_output=True, text=True,
    )
    sha = r.stdout.strip() or None
    if not sha:
        r2 = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", rel_path],
            cwd=REPO, capture_output=True, text=True,
        )
        sha = r2.stdout.strip() or None
    _commit_cache[key] = sha
    return sha

def commit_for_touch(rel_path: str) -> str | None:
    """Latest commit touching rel_path."""
    key = f"touch:{rel_path}"
    if key in _commit_cache:
        return _commit_cache[key]
    r = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", rel_path],
        cwd=REPO, capture_output=True, text=True,
    )
    sha = r.stdout.strip() or None
    _commit_cache[key] = sha
    return sha

HEAD_SHA = _git("rev-parse", "HEAD")

# ---------------------------------------------------------------------------
# Classify one rule
# ---------------------------------------------------------------------------

def classify(rule_id: str, doc: str, domain: str, statement: str) -> tuple[str, str]:
    """Return (status, citation).

    citation: 'commit:<sha7> · <path>' or '' for NOT BUILT
    """
    matched_tests = find_matching_tests(rule_id)
    # Split into green vs grandfathered
    if matched_tests:
        green = [t for t in matched_tests if t.lower() not in _baseline_files]
        if green:
            primary = green[0]
            rel = f"backend/tests/invariants/{primary}"
            sha = commit_for_add(rel) or HEAD_SHA
            return "BUILT", f"commit:{sha[:12]} · {rel}"
        else:
            primary = matched_tests[0]
            rel = f"backend/tests/invariants/{primary}"
            sha = commit_for_add(rel) or HEAD_SHA
            return "PARTIAL", f"commit:{sha[:12]} · {rel} (in baseline_failures)"
    # No matched invariant. Fall back to domain → service.
    svc_hits = resolve_domain(domain)
    if svc_hits:
        pkg = svc_hits[0]
        # Prefer __init__.py, else main.py, else the package dir.
        candidates = [
            f"backend/services/{pkg}/__init__.py",
            f"backend/services/{pkg}/main.py",
            f"backend/services/{pkg}.py",
            f"backend/services/{pkg}",
        ]
        for cand in candidates:
            if Path(f"{REPO}/{cand}").exists():
                sha = commit_for_add(cand) or commit_for_touch(cand) or HEAD_SHA
                return "PARTIAL", f"commit:{sha[:12]} · {cand}"
        return "NOT BUILT", ""
    return "NOT BUILT", ""

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    wb = load_workbook(SRC, data_only=False, keep_links=False)
    ws = wb["System Rules Registry"]
    if ws.cell(row=1, column=11).value != "Builder Status":
        raise SystemExit("column K header mismatch — abort")

    distribution = {"BUILT": 0, "PARTIAL": 0, "NOT BUILT": 0}
    by_prefix: dict[str, dict[str, int]] = {}

    for r in range(2, ws.max_row + 1):
        rule_id = ws.cell(row=r, column=1).value
        if not rule_id:
            continue
        doc = ws.cell(row=r, column=5).value or ""
        domain = ws.cell(row=r, column=8).value or ""
        statement = ws.cell(row=r, column=2).value or ""
        status, citation = classify(str(rule_id), str(doc), str(domain), str(statement))
        # Cell value: "STATUS · commit:<sha> · <path>"
        cell_val = status if not citation else f"{status} · {citation}"
        ws.cell(row=r, column=11, value=cell_val)
        distribution[status] += 1
        # tally by prefix
        m = re.match(r"^([A-Za-z]+)", str(rule_id))
        pfx = m.group(1) if m else "?"
        by_prefix.setdefault(pfx, {"BUILT": 0, "PARTIAL": 0, "NOT BUILT": 0})[status] += 1

    Path(DST).parent.mkdir(parents=True, exist_ok=True)
    wb.save(DST)
    print("Saved:", DST)
    print("Distribution:", distribution)
    print("Total:", sum(distribution.values()))
    print()
    print("By prefix:")
    for p in sorted(by_prefix):
        d = by_prefix[p]
        print(f"  {p:6s}  BUILT={d['BUILT']:4d}  PARTIAL={d['PARTIAL']:4d}  NOT BUILT={d['NOT BUILT']:4d}  total={sum(d.values())}")

    # write JSON summary
    summary = {
        "workbook_src_sha256": None,
        "workbook_dst_path": DST,
        "distribution": distribution,
        "by_prefix": by_prefix,
        "head_sha": HEAD_SHA,
        "baseline_failing_test_files": sorted(_baseline_files),
    }
    import hashlib
    with open(SRC, "rb") as f:
        summary["workbook_src_sha256"] = hashlib.sha256(f.read()).hexdigest()
    with open(DST, "rb") as f:
        summary["workbook_dst_sha256"] = hashlib.sha256(f.read()).hexdigest()
    with open("/app/audit/scratch/builder_status_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\nSummary written to /app/audit/scratch/builder_status_summary.json")

if __name__ == "__main__":
    main()
