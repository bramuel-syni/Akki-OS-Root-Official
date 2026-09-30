"""Tier 1 lab notebook (WPW-3, WPW-4): event-driven, timestamped from build_stamp + seq, classed, append-only, hash-chained.
Human contributions record actor, before, change, after; correlation only (WPW-5). CIF events are mirrored by reference (WPW-6)."""
import hashlib, json
from pathlib import Path


class Notebook:
    def __init__(self, build_stamp, seed):
        self.entries = []
        self.prev = "sha256:" + hashlib.sha256(f"genesis:{seed}".encode()).hexdigest()
        self.stamp = build_stamp

    def add(self, kind, cls, ref, payload):
        assert cls in ("measured", "estimated", "observed"), cls
        seq = len(self.entries) + 1
        e = {"seq": seq, "at": f"{self.stamp}+{seq:04d}", "kind": kind, "class": cls, "ref": ref, "payload": payload, "prev_hash": self.prev}
        h = "sha256:" + hashlib.sha256((self.prev + json.dumps(e, sort_keys=True)).encode()).hexdigest()
        e["hash"] = h
        self.prev = h
        self.entries.append(e)
        return h

    def write(self, path):
        Path(path).write_text("\n".join(json.dumps(e, sort_keys=True) for e in self.entries) + "\n")
        return self.prev


def verify(path):
    prev = None
    for line in Path(path).read_text().splitlines():
        e = json.loads(line)
        h = e.pop("hash")
        if prev is not None and e["prev_hash"] != prev:
            return False, e["seq"]
        if "sha256:" + hashlib.sha256((e["prev_hash"] + json.dumps(e, sort_keys=True)).encode()).hexdigest() != h:
            return False, e["seq"]
        prev = h
    return True, None
