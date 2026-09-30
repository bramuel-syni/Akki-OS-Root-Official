"""surface-studio validate. Blockers (RV shape) and review (QA shape). Outcome: pass | finding-not-blocking | blocked."""
import json, re, sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parent.parent
TOKEN = re.compile(r"\{[^}]+\}")
DIGITS = re.compile(r"\b\d[\d,]*\.?\d*%?\b")
DATE = re.compile(r"^\d{4}-\d\d-\d\d$")


def load(p):
    return json.loads(Path(p).read_text())


def pre(fx):
    fx = Path(fx)
    blockers, review = [], []
    spec, ps, brief, verdict = load(fx / "spec.json"), load(fx / "page-state.json"), load(fx / "brief.json"), load(fx / "verdict.json")
    for kind, d in (("spec", spec), ("page-state", ps), ("brief", brief), ("verdict", verdict)):
        jsonschema.validate(d, load(ROOT / "schemas" / f"{kind}.schema.json"))
    policy = load(ROOT / "policies" / "page-policy.json")
    # literal numbers in authored text
    for b in spec["blocks"]:
        stripped = TOKEN.sub("", b["text"])
        for m in DIGITS.finditer(stripped):
            if not DATE.match(m.group()):
                blockers.append(f"{b['id']}: literal number '{m.group()}' in authored text; every figure comes from the page state by reference")
    # every figure/delta/pending/silence in refs must exist and carry a receipt
    for b in spec["blocks"]:
        for r in b["refs"]:
            src = ps["facts"].get(r) or ps.get("deltas", {}).get(r) or ps.get("pending", {}).get(r) or ps.get("silence", {}).get(r)
            if not src:
                blockers.append(f"{b['id']}: ref {r} not in page state")
            elif src.get("receipt") not in ps["receipts"]:
                blockers.append(f"{b['id']}: ref {r} has no resolvable receipt")
    # triggers only from the three permitted kinds, each with its required fields
    for b in spec["blocks"]:
        if b["move"] == "trigger":
            if "kind" not in b or "pending_ref" not in b:
                blockers.append(f"{b['id']}: trigger without kind/pending_ref; triggers come only from decisions pending, advisories or Watch anomalies")
                continue
            p = ps["pending"].get(b["pending_ref"])
            if not p or p["kind"] != b["kind"]:
                blockers.append(f"{b['id']}: trigger kind does not match pending {b['pending_ref']}")
            else:
                for req in policy["trigger_kinds"][b["kind"]]["requires"]:
                    if req not in p:
                        blockers.append(f"{b['id']}: pending {b['pending_ref']} lacks {req} required for {b['kind']}")
    # directive phrasing is never allowed (findings, not directives)
    for b in spec["blocks"]:
        low = b["text"].lower()
        for ph in policy["language"]["directive_phrases"]:
            if ph in low:
                blockers.append(f"{b['id']}: directive phrasing '{ph}'; findings not directives")
    # causal markers need a causal receipt
    for b in spec["blocks"]:
        low = b["text"].lower()
        if any(m in low for m in policy["language"]["causal_markers"]):
            if not b.get("causal_ref") or not ps["receipts"].get(b["causal_ref"], {}).get("causal"):
                blockers.append(f"{b['id']}: causal claim without a receipt marked causal (WPW-5: correlation only)")
    # aggregate-only surface
    if brief["constraints"].get("aggregate_only") and ps["aggregate_only_check"]["individual_fields_present"]:
        blockers.append("aggregate-only page with individual-level fields present in the page state")
    # block cap and silence
    if len(spec["blocks"]) > policy["pages"][spec["page"]]["max_blocks"]:
        blockers.append(f"{len(spec['blocks'])} blocks > page max {policy['pages'][spec['page']]['max_blocks']}")
    if ps.get("silence") and not any(b["move"] == "silence" for b in spec["blocks"]):
        blockers.append("page state records silence but no block surfaces it (unmeasured must read as unmeasured, never blank)")
    if verdict["adopted"] not in {c["idea_id"] for c in verdict["candidates"] if c["verdict"] == "adopt"}:
        blockers.append("verdict: adopted id is not an adopted candidate")
    if not verdict.get("confirmed_by"):
        blockers.append("verdict: no confirmer")
    lead = policy["pages"][spec["page"]]["lead"]
    if spec["blocks"] and spec["blocks"][0]["move"] != lead:
        review.append(f"first block is {spec['blocks'][0]['move']}; page policy leads {spec['page']} with {lead} (direction may override with a recorded reason)")
    review.append("Read the blocks in order: does a reader with this role learn what it means, what moved, and what waits on them, in that priority?")
    return blockers, review


def post(plan_path):
    plan = load(plan_path)
    blockers, review = [], []
    cap = plan["role_policy"]["words_per_block_max"]
    for b in plan["blocks"]:
        aw = b.get("authored_words", b["words"])
        if aw > cap:
            blockers.append(f"{b['id']}: {aw} authored words > role cap {cap}")
        if not b["receipts"]:
            blockers.append(f"{b['id']}: no receipts resolved")
        if b.get("causal_ref") and not b.get("causal_receipt_ok"):
            blockers.append(f"{b['id']}: causal receipt not marked causal")
        if any(t in b["text"] for t in ("{", "}")):
            blockers.append(f"{b['id']}: unresolved token")
    return blockers, review


if __name__ == "__main__":
    fx, out = Path(sys.argv[1]), Path(sys.argv[2])
    b, r = pre(fx)
    pp = out / "resolved" / "content_plan.resolved.json"
    if pp.exists():
        b2, r2 = post(pp)
        b, r = b + b2, r + r2
    rep = {"outcome": "blocked" if b else ("finding-not-blocking" if r else "pass"), "blockers": b, "review": r}
    (out / "validate-report.json").write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps(rep, indent=2))
    sys.exit(1 if b else 0)
