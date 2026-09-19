"""Bump baseline_failures.json floor 5238 -> 5279 for CP-M12b-W1.

Additive-only per SO §3.8. Preserves ratchet_history append-only per SO §7 R-5.
"""
import json
from pathlib import Path

BASELINE = Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json"
)

d = json.loads(BASELINE.read_text())

# Sanity-guard: refuse to mutate if the pre-image is not the M10-W4e floor.
assert d["counts_at_baseline"]["passed"] == 5238, (
    f"pre-image floor mismatch: expected 5238, found {d['counts_at_baseline']['passed']}"
)
assert d["ratchet_history"][-1]["checkpoint"] == "CP-M10-W4e-MEMORY-WRITER-CONSOLIDATION"
assert d["ratchet_history"][-1]["passed"] == 5238

new_entry_note = (
    "M12b-W1 · Milestone 3 opener · Watch caller-flip + verdict-schema freeze + "
    "Ed25519 minimum. AUTHENTIC RED-first cycle: RED at "
    "phase0/drill_receipts/20260919T034025Z_cp_m12b_w1_red.log (34/40 fail — "
    "the six passing are anchor/scaffold cases without new modules · 6 passing "
    "under RED do NOT rebaseline any prior floor). Double-GREEN byte-identical "
    "at phase0/drill_receipts/20260919T034819Z_cp_m12b_w1_green1_v2.log + "
    "_cp_m12b_w1_green2.log (both 5279 passed / 1 skipped / 438 warnings). "
    "Delta 41 reconciled line-by-line: 40 new test functions across 5 M12b-W1 "
    "test files ("
    "test_m12b_w1_watch_vocabulary_caller_flip_ast.py 6 · "
    "test_m12b_w1_certificate_carrying_verdict_rows.py 10 · "
    "test_m12b_w1_ed25519_primitive_determinism.py 10 · "
    "test_m12b_w1_signature_as_guard_schema_field_exclusion.py 9 · "
    "test_m12b_w1_m11_gate_release_c2_xfail_retirement.py 5"
    ") + 1 xfail→pass conversion from CP-M11-GATE-RELEASE c2 dated-xfail "
    "retirement (test_cp_m11_gate_release_watch_m9_callers_vs_schema_xfail.py: "
    "xfail marker removed per R-18 T-c Option-α c2 verbatim retirement "
    "mechanism 'at M12b-W1 it xpasses → convert to a real passing test'). "
    "Files landed: "
    "services/watch/schema_verdict.py NEW (167 LOC · Verdict pydantic model + "
    "Certificate pydantic model + canonical_bytes + payload_ref + "
    "signature-as-guard field exclusion) · "
    "services/watch/signature_primitive.py NEW (98 LOC · Ed25519 keygen + "
    "sign + verify · deterministic per RFC 8032 · Watch-trust-boundary scope "
    "only · no key material routed to callers/Mkono per Canon 8 §W10 + §W11) · "
    "services/enforce/watch_action_class_gate.py NEW (87 LOC · schema-derived "
    "caller-flip surface per SO §3.8 Option-C + SO §3.10-α · closed-tuple "
    "ACTION_CLASSES mirror of Canon 8 vocabulary annotate/shape/contain/sever "
    "· destroy REMOVED per Canon 8 §W3 destroy-does-not-exist). "
    "AST caller-flip test asserts every M9 caller sources the Watch vocabulary "
    "through the gate adapter (no local literal). Certificate-carrying verdict "
    "rows carry A5.19-conformant certificate_ref hash-bound via payload_ref. "
    "Ed25519 primitive: keygen produces distinct keys per call · sign is "
    "deterministic per RFC 8032 · verify returns True for valid signature and "
    "False for tampered-message/tampered-signature/wrong-public-key. "
    "Signature-as-guard structurally excludes confidence/score/strength/"
    "probability fields at the pydantic model level + Certificate submodel "
    "level + JSON schema level + module source level (no banned-field literal). "
    "Regression fix (additive-only per SO §4.2 Clause 6 cross-wave modification): "
    "test_m11_mega_close_gate_count_matches_scope updated to allow post-M11 "
    "gates via POST_M11_GATE_NAMES registry — watch_action_class_gate "
    "registered with card citation STATE/OBJECTIVES/M12b_W1.md MUST-DO 1. "
    "Stop-conditions #1/#2/#3 NOT triggered. §6.4 pre-ruling NOT triggered "
    "(banned-field precursors at W2b + W3 already established the structural "
    "exclusion pattern · M12b-W1 extends to Verdict itself). B-M12b-Q1 "
    "(Ed25519 signing scope) answered inline at open: keys held only in "
    "Watch trust boundary, never routed to callers or Mkono. Card citations: "
    "STATE/OBJECTIVES/M12b_W1.md MUST-DO 1 (caller-flip AST) + MUST-DO 2 "
    "(certificate-carrying verdict rows) + MUST-DO 3 (Ed25519 primitive) + "
    "MUST-DO 4 (signature-as-guard banned-field exclusion) + MUST-DO 5 "
    "(M11-GATE-RELEASE c2 xfail retirement) + EXIT (all four M12b-W1 gates "
    "authored) + gate (iii) precondition already cleared at Canon-8 217/217 "
    "mapping (state commit 1e048bf5). Canon anchors: Canon 8 §W1 "
    "(eyes-never-act) · Canon 8 §W10 (watcher-watched-from-outside) · "
    "Canon 8 §W11 (one-task-one-identity) · Canon 8 §A5.19 (certificate on "
    "watch.* rows) · Canon 8 §Line 31 (closed sever-certainty registry · "
    "scoring parameter ban) · B-M10-Q1 (17-field row · payload_ref "
    "hash-binding) · owner run order 2026-09-18T~21:15Z Milestone 3 verbatim · "
    "owner T-c α ruling (SO §3.10-α tuple[str] discipline · "
    "2026-09-17T~13:26Z) · R-18 T-c Option-α c2 retirement contract. "
    "Autopilot R-31 continues NON-STOP under §6 END-OF-BUILD authority."
)

new_entry = {
    "at_utc": "2026-09-19T04:00:00Z",
    "checkpoint": "CP-M12b-W1-CALLER-FLIP-VERDICT-SCHEMA-ED25519",
    "prev_passed": 5238,
    "passed": 5279,
    "delta": 41,
    "note": new_entry_note,
}

d["counts_at_baseline"]["passed"] = 5279
d["recorded_at_utc"] = "2026-09-19T04:00:00Z"
d["ratchet_history"].append(new_entry)

# Preserve stable JSON layout — 2-space indent + trailing newline like prior file.
BASELINE.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

# Re-load + assert postcondition to prove the write is well-formed.
after = json.loads(BASELINE.read_text())
assert after["counts_at_baseline"]["passed"] == 5279
assert after["ratchet_history"][-1]["passed"] == 5279
assert after["ratchet_history"][-1]["delta"] == 41
assert after["ratchet_history"][-1]["checkpoint"] == "CP-M12b-W1-CALLER-FLIP-VERDICT-SCHEMA-ED25519"

import hashlib
new_sha = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
print(f"NEW baseline_failures.json sha256: {new_sha}")
print(f"passed_floor: 5238 -> 5279 (+41)")
print(f"ratchet_history length: {len(after['ratchet_history'])}")
