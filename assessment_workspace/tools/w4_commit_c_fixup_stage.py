#!/usr/bin/env python3
"""
W4 Commit-C fixup stage helper.

Executes three surgical edits on the state repo working tree:

1. notes/ORCH_BOOT.md — R-6 boundary regen post-Commit-C:
   - Update `generated_at_utc` (Commit-B time -> Commit-C fixup time).
   - Update `generator` narrative (Commit-B -> Commit-C fixup).
   - Update `regeneration_reason` (post-commit-a -> post-commit-c-fixup, advancing state_head).
   - Advance `heads_last_sealed.state_repo` block: head + sealed_at_utc + seal_kind.

2. STATE/DECISIONS.md — Append Commit-C fixup banking section.

3. STATE/NEXT.md — Flip R-64 marker from ⏳ IN-FLIGHT to ✅ SEALED.

Idempotent by anchor-string check.
Additive-only for DECISIONS/NEXT; surgical replacement for ORCH_BOOT (matches R-6 regen doctrine).
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
ORCH_BOOT = WORKSPACE / "notes" / "ORCH_BOOT.md"
DECISIONS = WORKSPACE / "STATE" / "DECISIONS.md"
NEXT = WORKSPACE / "STATE" / "NEXT.md"

# --- Commit metadata for W4 Commit-C fixup ---
W3_COMMIT_B_SHA = "9092674d07931f3b7ab04188ce71f40a19c1cf90"
W4_COMMIT_A_SHA = "da2642acdcb5f1785d6ca561913f60fceafd2c6b"
W4_COMMIT_B_SHA = "09f2f31743da91222f7e9de108810b8950e32f58"
COMMIT_B_TIME = "2026-09-19T21:22:00Z"
COMMIT_C_TIME = "2026-09-19T21:25:00Z"

# --- Anchor strings we expect to find and replace ---
OLD_GENERATED_AT = f"generated_at_utc: {COMMIT_B_TIME}"
NEW_GENERATED_AT = f"generated_at_utc: {COMMIT_C_TIME}"

OLD_GENERATOR_LINE = "generator: main-agent Autopilot (CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-B · state master · banks Commit-A `da2642acdcb5f1785d6ca561913f60fceafd2c6b`"
NEW_GENERATOR = (
    "generator: main-agent Autopilot (CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-C fixup · state master · "
    f"advances state_repo.head `{W3_COMMIT_B_SHA}` → new Commit-B `{W4_COMMIT_B_SHA}` · "
    f"code_repo.head stays at Commit-A `{W4_COMMIT_A_SHA}` · ratchet 5491 unchanged · marker R-64 flips ⏳→✅ · "
    "MEM-R-053 CROWN BAN NOT triggered · owner OPTION 1 verbatim + owner W4 EMPHASIS verbatim + owner FRONTENDS-GATE-IS-HALT-POINT verbatim · "
    "W4 FULLY SEALED · MEMORY LAYER CLOSES · CCS1 opens next · staleness clock T-~14.3h)"
)

OLD_REGEN_REASON = "regeneration_reason: r6-boundary-regen-post-commit-a-at-cp-memory-compaction-v1-w4-one-chain-integration-advancing-code-head"
NEW_REGEN_REASON = "regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-memory-compaction-v1-w4-one-chain-integration-advancing-state-head"

# The state_repo block currently reads with W3 Commit-B seal kind. We advance it in place.
OLD_STATE_REPO_BLOCK = """  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 9092674d07931f3b7ab04188ce71f40a19c1cf90
    sealed_at_utc: 2026-09-19T20:55:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION · state Commit-B `9092674d07931f3b7ab04188ce71f40a19c1cf90` · banks Commit-A `ebebc46f75494dbaa16efacd7b077c47afcb69f1` · memory-layer follow-on wave W3 · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim + owner CLARIFICATION 2026-09-19T~20:35Z verbatim · state-side landing includes STATE/DECISIONS.md Commit-A banking section (W3 scope + owner OPTION 1 + owner CLARIFICATION + amendment method verification per module docstring line 24 + files landed + RED/GREEN receipts + pre-Commit-A double-green byte-identical + transparency banking of ensure_ascii=False intermediate + canon anchors MEM-2/MEM-3/MEM-7 + Spec §4 Table 3 + tcb.py docstring line 24 + Doc-0 Attribute 1 + Canon 8 §W11 + SO §3.8 + SO §6.4 NOTHING-BEYOND + M16 R-3 precedent + owner rulings + Stop-conditions NOT triggered + autopilot next W4 → CCS1/CCS2/CCS3 → HALT before frontends) + STATE/NEXT.md R-63 marker + notes/ORCH_BOOT.md R-6 boundary regen advancing code_head to Commit-A + audit copy re-sync byte-identical · additive-only per SO §3.8 · ratchet 5485 unchanged at Commit-B state files only Commit-A carried the +3\""""

NEW_STATE_REPO_BLOCK = f"""  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {W4_COMMIT_B_SHA}
    sealed_at_utc: {COMMIT_C_TIME}
    seal_kind: "CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · state Commit-B `{W4_COMMIT_B_SHA}` · banks Commit-A `{W4_COMMIT_A_SHA}` · memory-layer follow-on wave W4 · MEMORY LAYER CLOSES on this seal · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim + owner W4 EMPHASIS 2026-09-19T~21:00Z verbatim + owner FRONTENDS-GATE-IS-HALT-POINT ratification this-turn verbatim · state-side landing includes STATE/DECISIONS.md Commit-A banking section (W4 scope + owner OPTION 1 + owner W4 EMPHASIS + files landed + RED/GREEN receipts + pre-Commit-A double-green byte-identical + transparency banking of pointer-drift-and-repair inherited from W3 Commit-C fixup + canon anchors MEM-6/MEM-10/MEM-R-012/MEM-R-013/MEM-R-050/Canon 3 §13/Canon 8 §W11/SO §3.8/SO §6.4 NOTHING-BEYOND/M12-W1a AST-ban precedent/M16 R-3 precedent/owner ruling 2a 2026-07-31/owner MEMORY GO/owner OPTION 1/owner W4 EMPHASIS + Stop-conditions NOT triggered + autopilot next CCS1/CCS2/CCS3 → HALT before frontends) + MEMORY-LAYER MILESTONE ROLLUP (W1 +7 · W2 +6 · W3 +3 · W4 +6 · aggregate +22 exactly · 5469 → 5491 · milestone snapshot pin passed_floor=5491 + baseline_failures_sha256=98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a) + R-19/R-20 DEFAULT-class pending ratification + R-21 flag-OFF awaiting ruling + STATE/NEXT.md R-64 marker ⏳ IN-FLIGHT + notes/ORCH_BOOT.md R-6 boundary regen advancing code_head from prior W3 Commit-A `ebebc46f` to this-wave Commit-A `{W4_COMMIT_A_SHA[:8]}` + audit copy sync deferred to Commit-C fixup boundary · additive-only per SO §3.8 · ratchet 5491 unchanged at Commit-B state files only Commit-A carried the +6\""""


# --- DECISIONS.md Commit-C fixup banking section ---
COMMIT_C_SENTINEL = "CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · Commit-C fixup banking section"

DECISIONS_APPEND = f"""

---

## 2026-09-19T~21:25Z · CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · Commit-C fixup banking section (state master · banks Commit-B `{W4_COMMIT_B_SHA}` · memory-layer follow-on wave W4 FULLY SEALED · **MEMORY LAYER CLOSED** · CCS1 opens next)

**Advances `notes/ORCH_BOOT.md` `heads_last_sealed.state_repo.head`** from `{W3_COMMIT_B_SHA}` (CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION Commit-B) to `{W4_COMMIT_B_SHA}` (this-wave W4 Commit-B). Regenerates `generated_at_utc` ({COMMIT_C_TIME}) + `generator` + `regeneration_reason` per R-6 boundary regen doctrine. Updates `state_repo.sealed_at_utc` ({COMMIT_C_TIME}) + `seal_kind` (Commit-B narrative with memory-layer milestone rollup + R-19/R-20 DEFAULT-class pending + R-21 flag-OFF pending). Mirrors `/app/frontend/public/audit/ORCH_BOOT.md` byte-identically at this fixup boundary per R-6 (a) regen trigger discipline.

**STATE/NEXT.md R-64 marker flips ⏳ IN-FLIGHT → ✅ SEALED** with narrative "W4 ONE-CHAIN INTEGRATION FULLY SEALED · MEMORY LAYER CLOSED · CCS1 C.17 answering-service seam bundle-freeze opens next".

**Commit-C files-changed count:** 3 (STATE/DECISIONS.md this-append + STATE/NEXT.md R-64 marker flip + notes/ORCH_BOOT.md R-6 boundary regen). Additive-only per SO §3.8.

**Seal chain complete for CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION:**
- Commit-A (code · programme/track-a): `{W4_COMMIT_A_SHA}` (2026-09-19T~21:12Z UTC)
- Commit-B (state · master): `{W4_COMMIT_B_SHA}` (2026-09-19T~21:22Z · banks Commit-A + memory-layer milestone rollup)
- Commit-C fixup (state · master): this-commit ({COMMIT_C_TIME} · advances state_head to Commit-B SHA · flips R-64 marker + syncs audit copy byte-identical)

**Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.**

**W4 ONE-CHAIN INTEGRATION FULLY SEALED.** Thin adapter `chain_integration.py` (4 surfaces: `ChainAppendReceipt` frozen carrier + `ChainGatedReader` receipt-keyed structural gate + `async append_compaction_row_to_chain` awaiting sealed `emit_deletion_ledger_row` + `async append_compaction_row_and_gate` combined write path) · 6 W4 invariants proving SEQUENCE (not co-existence) + ONE-chain routing + strong-form sequence + M12-W1a-shape AST bans (import-level + call-site-level) · sealed W1 compaction_v1/* + sealed W-M2-SW7 tcb.py + sealed M10 services/memory/ledger.py + sealed services/compliance/deletion_ledger.py + sealed data_class_registry.v4.json all NOT edited (additive-only per SO §3.8; `data_class='memory_publication_landed'` semantic overload used instead of v5 registry bump) · ratchet 5485 → 5491 monotonic-up.

---

### **MEMORY LAYER FULLY CLOSED** at this seal (per owner directive verbatim this-turn: "Memory layer closes with this W4 seal")

Memory layer opens at CP-MEMORY-COMPACTION-V1-BUILD-WAVE (R-61 · Commit-A `b1d1183674856c99e85d64b4fbd22a1508ffc4c9` · 2026-09-19T~19:57Z) on M17-W6 seal + M17.md card-repin repair per owner MEMORY GO ruling. Four sub-waves landed additive-only under SO §3.8:

- **W1 (BUILD-WAVE)** · `b1d11836` · +7 · 5469 → 5476 · new `services/memory/compaction_v1/` sub-package (7 files).
- **W2 (HARD-BANS-GREP-NEGATIVE)** · `67b5e070` · +6 · 5476 → 5482 · 6 grep-negative invariants MEM-R-048..MEM-R-053 · CROWN BAN NOT triggered.
- **W3 (TCB-REGISTRATION)** · `ebebc46f` · +3 · 5482 → 5485 · 3 additive tuple-appends to `tcb.py::_TCB_ENTRIES` per module docstring line 24 amendment method (matches M16 R-3 precedent).
- **W4 (ONE-CHAIN-INTEGRATION)** · `{W4_COMMIT_A_SHA[:8]}` · +6 · 5485 → 5491 · thin chain adapter + 6 invariants + M12-W1a-shape AST bans.

**Milestone snapshot pin (memory-layer close):**
- `passed_floor: 5491`
- `baseline_failures_sha256: 98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`
- Path-relative: `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json`

**Aggregate delta:** +22 exactly · 5469 → 5491 · full memory_compaction_v1 build-run wave sealed. Zero sealed module edited (only `tcb.py::_TCB_ENTRIES` tuple-append per its own docstring line 24 amendment method). Canon 3 §13 SyniSense ONE ledger doctrine held. MEM-R-053 CROWN BAN NOT triggered. MEM-R-048..MEM-R-052 all not triggered on clean codebase.

**Memory layer standing bounds (unchanged · owner-outstanding · pending owner ratification per SO §6.3 tier-3 / tier-4):**
- **R-19 (triggers) = DEFAULT-class · pending owner ratification.** Recommended-defaults from memory_compaction_v1 spec §7. Tag `pending ratification` retained.
- **R-20 (retention rule set v1) = DEFAULT-class · pending owner ratification.** Retention rule set v1 baked into `RetentionEngine.decide`; v1 default keeps ALL classes (no drops). Tag `pending ratification` retained.
- **R-21 (user-memory class, consent model) = flag-OFF by default · awaiting owner ruling.** Owner input outstanding: no consent model assumed; no principal data written until ruled. Enforced structurally across M17-W1..W5 via AST bans; enforced structurally in `compaction_v1` by absence of any user-memory-class implementation.

---

**Autopilot next per owner directive verbatim this-turn:**
1. **CCS1 (C.17 answering-service seam bundle-freeze)** — frozen from `dap_backend_spec_v1` under T-b · JSON-Schema authoritative (freeze from spec even where backend is thin) · tests-first · §3.3 sealed · works survey's 10 absence findings into freeze scope (each finding either closes in the CCS wave or is banked with a reason).
2. **CCS2 (DAP entitlement)** — same freeze mechanism.
3. **CCS3 (DAP receipt)** — same freeze mechanism.
4. **HALT at frontends gate** — POD-level seal report to owner: survey findings closure status + three frozen contract pins + UI Handoff Brief path + anything else specialists need. Wait for owner dispatch to specialists.

**Time-gated task armed:** Staleness re-scope APPLY-ON-EXPIRY at 2026-09-20T~11:35Z (T-~14.3h · fires as own small seal when clock hits · owner reaffirmed this-turn: "Staleness ceremony has priority if 11:35Z crosses mid-wave — pause at safe checkpoint, small seal, resume").

**Standing bounds unchanged:** zero push · terminal pytest only · no testing_agent · additive-only §3.8 · §3.3 3-Commit Seal on dual branches · ratchet monotonic (floor 5491 · never rebaselined silently).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
"""


# --- NEXT.md R-64 marker flip: replace ⏳ block with ✅ block ---
NEXT_OLD_MARKER_LINE = (
    "⏳ **IN-FLIGHT (Commit-B this-turn banks Commit-A + authors this marker · "
    "Commit-C fixup will advance state_head to Commit-B SHA + flip ⏳→✅):**"
)
NEXT_NEW_MARKER_LINE = (
    "✅ **SEALED (Commit-C fixup at 2026-09-19T~21:25Z · state Commit-C banks Commit-B "
    f"`{W4_COMMIT_B_SHA}` · heads advanced code=`{W4_COMMIT_A_SHA[:8]}` / state=`{W4_COMMIT_B_SHA[:8]}` · "
    "W4 ONE-CHAIN INTEGRATION FULLY SEALED · MEMORY LAYER FULLY CLOSED · CCS1 C.17 answering-service seam bundle-freeze opens next):**"
)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def surgical_replace(path: Path, old: str, new: str, label: str) -> str:
    body = path.read_text(encoding="utf-8")
    if old not in body:
        return f"FAIL: {label}: anchor not found in {path}"
    count = body.count(old)
    if count != 1:
        return f"FAIL: {label}: anchor appears {count} times in {path} (expected exactly 1)"
    new_body = body.replace(old, new, 1)
    path.write_text(new_body, encoding="utf-8")
    return f"OK:   {label}: replaced 1 occurrence ({len(old)} -> {len(new)} bytes)"


def append_if_absent(path: Path, sentinel: str, content: str, label: str) -> str:
    body = path.read_text(encoding="utf-8")
    if sentinel in body:
        return f"SKIP: {label}: sentinel present"
    new_body = body + content
    path.write_text(new_body, encoding="utf-8")
    return f"OK:   {label}: appended {len(content)} bytes"


def main() -> int:
    print(f"Pre-edit ORCH_BOOT.md sha256:  {sha256_of(ORCH_BOOT)}")
    print(f"Pre-edit DECISIONS.md sha256:  {sha256_of(DECISIONS)}")
    print(f"Pre-edit NEXT.md sha256:       {sha256_of(NEXT)}")
    print()

    # 1. ORCH_BOOT surgical edits
    print(surgical_replace(ORCH_BOOT, OLD_GENERATED_AT, NEW_GENERATED_AT, "ORCH_BOOT.generated_at_utc"))
    print(surgical_replace(ORCH_BOOT, OLD_GENERATOR_LINE, NEW_GENERATOR, "ORCH_BOOT.generator"))
    print(surgical_replace(ORCH_BOOT, OLD_REGEN_REASON, NEW_REGEN_REASON, "ORCH_BOOT.regeneration_reason"))
    print(surgical_replace(ORCH_BOOT, OLD_STATE_REPO_BLOCK, NEW_STATE_REPO_BLOCK, "ORCH_BOOT.state_repo block"))

    # 2. DECISIONS append
    print(append_if_absent(DECISIONS, COMMIT_C_SENTINEL, DECISIONS_APPEND, "DECISIONS.Commit-C-fixup-banking"))

    # 3. NEXT surgical flip
    print(surgical_replace(NEXT, NEXT_OLD_MARKER_LINE, NEXT_NEW_MARKER_LINE, "NEXT.R-64 marker flip"))

    print()
    print(f"Post-edit ORCH_BOOT.md sha256: {sha256_of(ORCH_BOOT)}")
    print(f"Post-edit DECISIONS.md sha256: {sha256_of(DECISIONS)}")
    print(f"Post-edit NEXT.md sha256:      {sha256_of(NEXT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
