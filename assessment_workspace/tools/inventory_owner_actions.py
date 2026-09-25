"""Document original-markup event sites; never execute prototype JavaScript.

This is an audit derivative, not a feature-completion denominator. Repeated
lists, conditional surfaces and script-defined actions need separate review.
"""
import argparse
import hashlib
import json
from pathlib import Path


def inventory(template, surface):
    rows = []

    def walk(nodes, conditions=(), lists=()):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            attributes = node.get("attributes", {})
            gates, repeats = conditions, lists
            if node["tag"] == "sc-if":
                gates = (*conditions, attributes.get("value", ""))
            if node["tag"] == "sc-for":
                repeats = (*lists, {"binding": attributes.get("list"), "alias": attributes.get("as")})
            for event, binding in attributes.items():
                if event.startswith("sc-camel-on-"):
                    rows.append({
                        "id": f"{surface}:{node['line']}:{len(rows) + 1}",
                        "surface": surface, "prototype_line": node["line"],
                        "tag": node["tag"], "event": event, "binding": binding,
                        "conditions": list(gates), "list_context": list(repeats),
                        "component_status": "UNREVIEWED",
                        "canon_anchor": None, "consumer": None, "writer": None,
                        "executor": None, "acceptance_test": None,
                        "functional_status": "UNREVIEWED",
                    })
            walk(node.get("children", []), gates, repeats)

    walk(template["nodes"])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace.resolve()
    base = root / "assessment_workspace/canon/prototypes/20260925_owner_updated"
    output = root / "assessment_workspace/notes/census_operational_v1"
    rows, sources = [], {}
    for surface in ("os", "dap"):
        raw = (base / f"{surface}.html").read_bytes()
        template = json.loads((root / f"frontend/src/components/prototype/generated/{surface}.json").read_text())
        digest = hashlib.sha256(raw).hexdigest()
        if template["source_sha256"] != digest:
            raise ValueError("Prototype source hash disagrees; do not inventory a different design")
        items = inventory(template, surface)
        sources[surface] = {"source_sha256": digest, "event_sites": len(items)}
        rows.extend(items)
    result = {"kind": "documentary_markup_event_inventory", "sources": sources,
              "event_sites": len(rows), "functional_denominator_established": False,
              "limits": ["Event sites are not journeys or requirement counts.",
                         "No script executed, no DOM or application source changed.",
                         "Component, Canon, writer and test joins require review; null means unreviewed, not absent."],
              "rows": rows}
    path = output / "PROTOTYPE_ACTION_INVENTORY.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "sources": sources, "event_sites": len(rows),
                      "unique_ids": len({row['id'] for row in rows}),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()