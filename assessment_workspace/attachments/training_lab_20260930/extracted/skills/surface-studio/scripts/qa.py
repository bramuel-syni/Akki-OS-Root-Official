"""surface-studio qa: mechanical gates on the assembled outputs."""
import html, json, sys
from pathlib import Path


def main(build_dir):
    b = Path(build_dir)
    plan = json.loads((b / "resolved" / "content_plan.resolved.json").read_text())
    rec = json.loads((b / "out" / "content-record.json").read_text())
    prev = (b / "out" / "preview.html").read_text()
    blockers, review = [], []
    for blk in rec["blocks"]:
        if html.escape(blk["text"]) not in prev:
            blockers.append(f"{blk['id']}: block text missing from preview")
        for w in blk["walk"]:
            if plan["walk_affordance"] not in prev:
                blockers.append("walk affordance missing from preview")
                break
    if plan["page_brief"]["silence"] and not rec["silence_surfaced"]:
        blockers.append("silence in page state not surfaced")
    if plan["page_brief"]["silence"] and "hatch" not in prev:
        blockers.append("silence surfaced without hatched treatment")
    if plan["stub"]:
        if rec.get("servable") is not False or "STUB PAGE STATE" not in prev:
            blockers.append("stub page state must produce servable=false and a preview banner")
        review.append("stub page state: content is exercised, never served")
    for blk in rec["blocks"]:
        if blk["degraded"] and "not available" not in blk["text"].lower():
            blockers.append(f"{blk['id']}: degraded block does not say what is unavailable")
    if plan["aggregate_only"] and plan["individual_fields_present"]:
        blockers.append("aggregate-only page assembled with individual-level fields")
    lead = plan["page_policy"]["lead"]
    if rec["blocks"] and rec["blocks"][0]["move"] != lead:
        review.append(f"lead move is {rec['blocks'][0]['move']} against page policy {lead}")
    review.append("Does the voice read as the role's voice (plain for board and floor, full jargon for officer and operator)?")
    out = {"outcome": "blocked" if blockers else "finding-not-blocking", "blockers": blockers, "review": review}
    (b / "out" / "qa-report.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
