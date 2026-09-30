"""surface-studio resolve: spec + page-state + brief + verdict + policy → frozen content plan.

Deterministic: token interpolation, page-brief assembly (deltas, pending by
kind, silence), voice selection by role, cache key. No copy is invented here;
the authored sentences live in the spec and are checked, not written.
"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_.]*)\}")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def dump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(o, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fmt(v, unit):
    if unit == "pct":
        return f"{v*100:.0f}%"
    if unit == "GBP":
        return f"£{v:,.0f}"
    if unit == "count":
        return f"{int(v):,}"
    return str(v)


class PageState:
    def __init__(self, d, policy):
        self.d, self.policy = d, policy
        self.unavailable = set(d.get("unavailable_sources", []))
        self.facts, self.deltas, self.pending, self.silence, self.receipts = d["facts"], d.get("deltas", {}), d.get("pending", {}), d.get("silence", {}), d["receipts"]

    def token(self, tok):
        if tok in self.facts:
            f = self.facts[tok]
            return "[not available]" if f["receipt"] in self.unavailable else fmt(f["value"], f["unit"])
        base, _, field = tok.partition(".")
        if base in self.deltas and field:
            dd = self.deltas[base]
            if field in ("prior", "current"):
                return "[not available]" if dd["receipt"] in self.unavailable else fmt(dd[field], dd["unit"])
            return str(dd[field])
        if base in self.pending and field:
            pp = self.pending[base]
            if field == "phrasing":
                tk = self.policy["trigger_kinds"][pp["kind"]]
                return tk["phrasing"].replace("<seat>", pp.get("seat", "")) if pp["kind"] == "decision_pending" else tk["phrasing"]
            return str(pp[field])
        if base in self.silence and field:
            return str(self.silence[base][field])
        raise KeyError(f"unresolvable reference {{{tok}}}")

    def text(self, s):
        return TOKEN.sub(lambda m: self.token(m.group(1)), s)

    def receipts_for(self, refs):
        out = []
        for r in refs:
            src = self.facts.get(r) or self.deltas.get(r) or self.pending.get(r) or self.silence.get(r)
            if src and src.get("receipt") and src["receipt"] not in out:
                out.append(src["receipt"])
        return out

    def classes_for(self, refs):
        cl = set()
        for r in refs:
            src = self.facts.get(r) or self.deltas.get(r)
            if src:
                cl.add(src["class"])
        return sorted(cl)


def resolve(fixture_dir, out_dir):
    fx, out = Path(fixture_dir), Path(out_dir)
    spec, ps, brief, verdict = load(fx / "spec.json"), load(fx / "page-state.json"), load(fx / "brief.json"), load(fx / "verdict.json")
    policy = load(ROOT / "policies" / "page-policy.json")
    pref = f"{ps['page_state_id']}@{ps['version']}"
    assert spec["page_state_ref"] == pref == brief["page_state_ref"], "page_state_ref mismatch"
    assert spec["verdict_ref"] == verdict["verdict_id"] and verdict["brief_ref"] == brief["brief_id"], "verdict/brief mismatch"
    state = PageState(ps, policy)
    role, page = policy["roles"][spec["role"]], policy["pages"][spec["page"]]
    unavailable = set(ps.get("unavailable_sources", []))
    blocks = []
    for b in spec["blocks"]:
        rcs = state.receipts_for(b["refs"])
        missing = [r for r in rcs if r in unavailable]
        if rcs and all(r in unavailable for r in rcs):
            rb = {"id": b["id"], "move": "silence", "degraded_from": b["move"], "title": b["title"],
                  "text": f"Not available at {ps['as_of']}: {', '.join(state.receipts[r]['resolves_to'] for r in missing)}. Shown as unmeasured, not as unchanged.",
                  "refs": b["refs"], "receipts": rcs, "classes": [], "walk": [], "degraded": True, "missing_sources": missing}
            rb["words"] = len(rb["text"].split()); blocks.append(rb); continue
        authored = state.text(b["text"])
        note = f" (Figures from {', '.join(missing)} not available at {ps['as_of']}.)" if missing else ""
        rb = {"id": b["id"], "move": b["move"], "title": b["title"], "text": authored + note, "authored_words": len(authored.split()), "system_note": note.strip(), "refs": b["refs"], "degraded": bool(missing), "missing_sources": missing,
              "receipts": state.receipts_for(b["refs"]), "classes": state.classes_for(b["refs"]),
              "walk": [{"ref": r, "receipt": rc, "resolves_to": state.receipts[rc]["resolves_to"]} for r in b["refs"] for rc in state.receipts_for([r])]}
        if "kind" in b:
            rb["kind"], rb["pending_ref"] = b["kind"], b["pending_ref"]
        if "causal_ref" in b:
            rb["causal_ref"], rb["causal_receipt_ok"] = b["causal_ref"], bool(state.receipts.get(b["causal_ref"], {}).get("causal"))
        if "silence_ref" in b:
            rb["silence_ref"] = b["silence_ref"]
        rb["words"] = len(rb["text"].split())
        blocks.append(rb)
    page_state_hash = "sha256:" + hashlib.sha256(json.dumps(ps, sort_keys=True).encode()).hexdigest()
    spec_hash = sha(fx / "spec.json")
    cache_key = "sha256:" + hashlib.sha256(f"{page_state_hash}|{spec['role']}|{role['voice']}|{spec_hash}|{policy['version']}".encode()).hexdigest()
    plan = {
        "spec_id": spec["spec_id"], "page": spec["page"], "role": spec["role"], "voice": role["voice"], "page_state_ref": pref, "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
        "direction": verdict["adopted"], "manifest_ids": [m["id"] for m in verdict["manifest"]], "seed": spec["seed"], "build_stamp": spec["build_stamp"],
        "as_of": ps["as_of"], "tenant": ps["tenant"], "page_policy": page, "role_policy": role, "language": policy["language"], "trigger_kinds": policy["trigger_kinds"],
        "source": ps["source"], "stub": ps["source"] == "stub", "unavailable_sources": sorted(unavailable),
        "aggregate_only": brief["constraints"].get("aggregate_only", page["aggregate_only"]), "individual_fields_present": ps["aggregate_only_check"]["individual_fields_present"],
        "page_brief": {"facts": len(state.facts), "deltas": list(state.deltas), "pending": {k: v["kind"] for k, v in state.pending.items()}, "silence": list(state.silence)},
        "blocks": blocks, "page_state_hash": page_state_hash, "cache_key": cache_key, "walk_affordance": policy["receipts"]["walk_affordance"],
        "inputs_sha256": {p.name: sha(p) for p in [fx / "spec.json", fx / "page-state.json", fx / "brief.json", fx / "verdict.json", ROOT / "policies" / "page-policy.json"]},
    }
    dump(plan, out / "content_plan.resolved.json")
    return plan


if __name__ == "__main__":
    p = resolve(sys.argv[1], sys.argv[2])
    print(f"resolved: {p['page']} for {p['role']} · {len(p['blocks'])} blocks · cache {p['cache_key'][:20]}")
