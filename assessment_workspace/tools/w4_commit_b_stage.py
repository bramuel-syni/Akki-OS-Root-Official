#!/usr/bin/env python3
"""
W4 Commit-B stage helper.

Appends the CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-A banking
section to STATE/DECISIONS.md and the R-64 IN-FLIGHT marker to STATE/NEXT.md.

Idempotent by anchor-string check (refuses to double-append).

This is a state-file editor, not production code. Additive-only.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

WORKSPACE = Path("/app/assessment_workspace")
DECISIONS = WORKSPACE / "STATE" / "DECISIONS.md"
NEXT = WORKSPACE / "STATE" / "NEXT.md"

# Sentinel string used inside both appends; used as idempotency check.
COMMIT_A_SHA = "da2642acdcb5f1785d6ca561913f60fceafd2c6b"
IDEMPOTENT_SENTINEL = "CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · Commit-A banking section"
NEXT_SENTINEL = "R-64 · CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-A landed"


DECISIONS_APPEND = """
---

## 2026-09-19T~21:20Z · CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · Commit-A banking section (state master · banks Commit-A `da2642acdcb5f1785d6ca561913f60fceafd2c6b` · memory-layer follow-on wave W4 · MEMORY LAYER CLOSES on this seal · W4 M10-W4e ledger integration landed · CCS1 opens next)

**Owner OPTION 1 ratification (verbatim, 2026-09-19T~20:20Z, banked at R-62 W2 banking section):**

> "W4 (M10-W4e ledger integration): thin adapter from compaction storage to sealed M10 chain writer path services.memory.ledger. Preserve ordering invariant: ledger row lands BEFORE compaction artifact becomes readable. InMemoryCompactionStorage becomes AST-banned from production imports (test-fixture only)."

**Owner W4 EMPHASIS (verbatim, this-session 2026-09-19T~21:00Z):**

> (1) "The ordering invariant must prove SEQUENCE, not co-existence — a test that observes both the ledger row and the readable artifact after the fact proves nothing; author it so a read attempted before the ledger write refuses (or the write path structurally cannot expose the artifact until the chain append returns)."
>
> (2) "The AST ban on InMemoryCompactionStorage from production imports should mirror the negative-scan shape you used at M12-W1a (import-level + call-site level) — tests/** stays allowed."

**Commit-A scope landed at `da2642acdcb5f1785d6ca561913f60fceafd2c6b` on programme/track-a:**

1. **NEW `backend/services/memory/compaction_v1/chain_integration.py`** (335 lines · thin adapter · 4 surfaces per Canon 8 §W11 structural role separation):
   - `ChainAppendReceipt` — frozen carrier (`artefact_hash: str`, `chain_row_id: str`, `chain_appended_at_utc: str`) · `extra="forbid"` · construction-time immutability per Canon 3 §9.3.
   - `ChainGatedReader` — receipt-keyed structural gate · `record_appended(receipt)` mints a lookup entry · `read(artefact_hash)` refuses with `MemoryLedgerRowMissingRefusalError` when no receipt recorded for that hash. STRUCTURAL SEQUENCE PROOF: `read()` lookup is receipt-keyed; a receipt is minted ONLY inside `append_compaction_row_to_chain` AFTER `await emit_deletion_ledger_row(...)` returns; therefore no receipt exists until chain-append is complete; therefore no bytes are exposable until a receipt exists; therefore the write path structurally cannot expose the artefact until the chain append returns.
   - `async def append_compaction_row_to_chain(row: CompactionLedgerRow) -> ChainAppendReceipt` — awaits sealed `services.compliance.deletion_ledger.emit_deletion_ledger_row(...)` with `data_class='memory_publication_landed'` (registry-valid · Canon 3 §13 SyniSense ONE ledger doctrine) and `stamp_audit` `event_kind='compaction_v1_landed'` (distinguishing tag) + `lawful_basis_ref='memory:compaction_v1_landed'` + full CompactionLedgerRow content preserved in `stamp_audit` for later reconstruction.
   - `async def append_compaction_row_and_gate(row, reader) -> ChainAppendReceipt` — combined write path implementing owner W4 EMPHASIS #1 strong-form: chain-append raises → receipt not minted → reader untouched → artefact remains structurally unreadable.

   Data class NOTE (banked in module docstring): `data_class='memory_publication_landed'` is a semantic overload on the existing registry value. A dedicated `memory_compaction_landed` data class would require a sealed `data_class_registry.v4.json → v5` bump per contracts-version-change discipline (SO §3.10 amendment conditions). That bump is DEFERRED and does not block W4 landing under SO §3.8 additive-only.

2. **NEW `backend/tests/invariants/test_memory_compaction_v1_w4_one_chain_integration.py`** (471 lines · 6 invariants):
   - `test_w4_read_before_chain_append_receipt_refuses` (W4.1 · structural SEQUENCE proof) — `ChainGatedReader.read()` refuses with `MemoryLedgerRowMissingRefusalError` when no `ChainAppendReceipt` has been recorded.
   - `test_w4_chain_append_receipt_then_read_returns_bytes` (W4.2 · positive sequence witness) — after `record_appended(receipt)`, `read(receipt.artefact_hash)` returns the byte-identical payload (MEM-R-015).
   - `test_w4_append_compaction_row_routes_through_sealed_m10_emit` (W4.3 · ONE-chain routing proof) — via `unittest.mock` spy on `services.compliance.deletion_ledger.emit_deletion_ledger_row`, asserts single-await + `data_class='memory_publication_landed'` + artefact-hash binding.
   - `test_w4_write_path_structurally_hides_artefact_until_chain_append_returns` (W4.4 · strong-form sequence proof per owner EMPHASIS #1) — chain-append raises → receipt not minted → reader untouched → read still refuses.
   - `test_w4_ast_ban_no_production_import_of_in_memory_compaction_storage` (W4.5 · M12-W1a-shape import-level negative scan) — allow-list: `tests/**` + `services/memory/compaction_v1/**` (self-package · sealed W1 `operations.py` type-annotates `InMemoryCompactionStorage` · grandfathered per SO §3.8 sealed-W1-not-edited discipline).
   - `test_w4_ast_ban_no_production_callsite_instantiation_of_in_memory_compaction_storage` (W4.6 · M12-W1a-shape call-site-level negative scan) — allow-list: `tests/**` ONLY (no production instantiation anywhere including `compaction_v1/**` itself · test-fixture-only per owner ruling).

3. **BUMP `backend/tests/invariants/baseline_failures.json`** — ratchet 5485 → 5491 (+6 exactly reconciled line-by-line · 6 new W4 invariants · zero auto-parametrized wizard triggered · not a `contracts/*.py` file) · new `ratchet_history` entry appended · new sha256 `98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`.

**Sealed modules NOT edited (additive-only per SO §3.8):**
- Sealed W1 `services/memory/compaction_v1/carriers.py` NOT edited (`CompactionLedgerRow` consumed via identity import).
- Sealed W1 `services/memory/compaction_v1/refusals.py` NOT edited (`MemoryLedgerRowMissingRefusalError` consumed via identity import).
- Sealed W1 `services/memory/compaction_v1/verifier.py` NOT edited (imported only).
- Sealed W1 `services/memory/compaction_v1/storage.py` NOT edited (`InMemoryCompactionStorage` now W4-AST-banned from production imports).
- Sealed W1 `services/memory/compaction_v1/retention.py` NOT edited.
- Sealed W1 `services/memory/compaction_v1/operations.py` NOT edited (grandfathered self-package allow-list at import-level; not instantiated at call-site anywhere including here).
- Sealed W-M2-SW7 `services/doc0_attributes/tcb.py` NOT edited (W3 additive tuple-append already banked at R-63).
- Sealed M10 `services/memory/ledger.py` NOT edited.
- Sealed `services/compliance/deletion_ledger.py` NOT edited (consumed via identity import).
- Sealed `services/compliance/data_class_registry.v4.json` NOT edited (semantic overload of `memory_publication_landed` used instead of v5 registry bump).
- Sealed M14 + M11 + M16 + M17-W1..W6 + W-M2-SW7 + W-7bB + c13_scope modules all NOT edited.

**Pre-authoring RED sweep** at `phase0/drill_receipts/20260919T210936Z_cp_memory_compaction_v1_w4_one_chain_integration_RED_pre.log` — 4/6 fail right-reason ModuleNotFoundError `No module named 'services.memory.compaction_v1.chain_integration'` + 2/6 pass right-reason: the 2 AST-ban tests (W4.5 + W4.6) pass immediately as authentic protective bans on the clean codebase state (no production imports of `InMemoryCompactionStorage` existed pre-W4 · matches W2 crown-ban precedent where grep-negative bans passed on clean codebase and stand ready to fire on future violations).

**Post-authoring GREEN** at `phase0/drill_receipts/20260919T211119Z_cp_memory_compaction_v1_w4_one_chain_integration_GREEN_post.log` — 6/6 pass in 2.40s.

**Pre-Commit-A double-green byte-identical BASELINE_GUARD=1:**
- run1 at `phase0/drill_receipts/20260919T211704Z_cp_memory_compaction_v1_w4_preseal_GUARD1_run1.log` · 5491 passed / 1 skipped / 438 warnings · ~182s · raw 58612 B.
- run2 at `phase0/drill_receipts/20260919T212014Z_cp_memory_compaction_v1_w4_preseal_GUARD1_run2.log` · 5491 passed / 1 skipped / 438 warnings · ~182s · raw 58612 B.
- **stripped-sha256 `9fefa0e697f2d3f0175a41367bc7b00530229582a68a3f70cc67d573a60432dd` IDENTICAL** across both runs against FINAL `baseline_failures.json` sha256 `98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`.

**Transparency banking (§6 · SO §3 transparency doctrine):** 1 prior GUARD1 run1 attempt at `20260919T211248Z` (first-attempt) failed `test_decisions_carries_pointer_near_bottom` with 1 fail because `STATE/DECISIONS.md` was missing the `READ STATE/STANDING_ORDERS.md FIRST — permanent standing law` pointer in its last 5 non-empty lines. **Defect INHERITED from prior W3 Commit-C fixup which appended banking section without a trailing pointer line.** Defect not caught at W3 close because only targeted tests were run post-fixup, not full sweep. **Reconciled by pre-W4-Commit-A state-side pointer-append to `STATE/DECISIONS.md`** (housekeeping pickup per R-29-BOOT precedent · state-side edit lands in this W4 Commit-B state seal alongside this banking append). Not a ratchet break; not a Stop-condition trigger. Earlier failed run1 receipt banked as evidence of the drift-and-repair per SO §3 transparency doctrine.

**Canon anchors verbatim (Commit-A scope):**
- MEM-6 [B.4 · DAP-29] · ledger-row-before-artefact-readable — chain-level restatement.
- MEM-10 [C.13 · I-1] · compaction rows on the ONE chain.
- MEM-R-012 · ledger row FIRST at storage boundary — chain-level uplift.
- MEM-R-013 · row-write failure aborts artefact publication.
- MEM-R-050 · grep-negative surface (no compaction without ledger row first) structurally satisfied by `ChainGatedReader` refusal.
- Canon 3 §13 · SyniSense ONE ledger doctrine (memory reconstructs through the same append-only record; no second ledger).
- Canon 8 §W11 · structural role separation (thin binding: frozen carrier + async emitter + gated reader · determinism preserved · learned surface absent).
- SO §3.8 · thin-kernel additive-only.
- SO §6.4 · NOTHING-BEYOND (scope frozen at 4 surfaces + 6 invariants · no scope beyond).
- M12-W1a · AST-ban precedent shape (import-level + call-site-level) verbatim.
- M16 R-3 2026-09-09 precedent shape (additive to sub-package).
- Owner ruling 2a 2026-07-31 verbatim: *"Northena owns the one ledger; memory must be ledger-reconstructible through the same append-only record, one trace thread, no second ledger."*
- Owner MEMORY GO ruling banked verbatim (banked in R-61 build-wave banking section).
- Owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim (banked in R-62 W2 banking section).
- Owner W4 EMPHASIS 2026-09-19T~21:00Z verbatim (banked above in this section).

**Stop-conditions #1/#2/#3 NOT triggered at Commit-A · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.** Ratchet 5485 → 5491 monotonic-up. Zero flip. Zero regression. Zero refactor. Full RED-first tests-first discipline held (mechanical RED banked before module authoring; targeted GREEN after; full double-green before Commit-A; pointer-drift defect surfaced by full sweep, reconciled in state-side fix before final Commit-A landing).

---

### MEMORY-LAYER MILESTONE ROLLUP (owner directive verbatim this-turn: *"Memory layer closes with this W4 seal — include in the Commit-B banking a memory-layer milestone rollup (W1 +7, W2 +6, W3 +3, W4 delta, aggregate + snapshot/pins as your convention requires)"*)

**Memory layer opens at CP-MEMORY-COMPACTION-V1-BUILD-WAVE (R-61 · Commit-A `b1d1183674856c99e85d64b4fbd22a1508ffc4c9` · 2026-09-19T~19:57Z) on M17-W6 seal + M17.md card-repin repair per owner MEMORY GO ruling banked verbatim.**

| Wave | CP | Commit-A SHA | Delta | Ratchet | Scope |
|---|---|---|---|---|---|
| **W1** | CP-MEMORY-COMPACTION-V1-BUILD-WAVE | `b1d1183674856c99e85d64b4fbd22a1508ffc4c9` | **+7** | 5469 → 5476 | New sub-package `services/memory/compaction_v1/` (7 files: `__init__` + `carriers` + `refusals` + `retention` + `verifier` + `storage` + `operations`) · concrete Given/When/Then materialisation of ingestion-authored 7 property tests · 3 entrypoints (`compact` + `reload` + `erasure_query`) per SO §6.4 NOTHING-BEYOND. |
| **W2** | CP-MEMORY-COMPACTION-V1-W2-HARD-BANS-GREP-NEGATIVE | `67b5e070e017ecbbd8645df87d42966721fa082d` | **+6** | 5476 → 5482 | 6 grep-negative invariants MEM-R-048..MEM-R-053 · MEM-R-053 CROWN BAN (design-convergence stop-and-report) NOT triggered on clean codebase · authoring GREEN-pre on clean state per W2 crown-ban precedent. |
| **W3** | CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION | `ebebc46f75494dbaa16efacd7b077c47afcb69f1` | **+3** | 5482 → 5485 | 3 TCB registrations via `tcb.py::_TCB_ENTRIES` additive tuple-append per docstring line 24 amendment method: `mem.retention_engine` (IN · MEM-3) + `mem.reload_verifier` (IN · MEM-7) + `mem.drafting_component` (OUT · MEM-2). Matches M16 R-3 2026-09-09 precedent shape. |
| **W4** | CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION | `da2642acdcb5f1785d6ca561913f60fceafd2c6b` | **+6** | 5485 → 5491 | Thin adapter `chain_integration.py` (4 surfaces) + 6 W4 invariants (structural SEQUENCE proof + ONE-chain routing spy + strong-form sequence + M12-W1a-shape AST bans). InMemoryCompactionStorage AST-banned from production imports (test-fixture only). |
| **AGGREGATE** | Memory layer (W1..W4) | four Commit-A SHAs above | **+22 exactly** | **5469 → 5491** | Full memory_compaction_v1 build-run wave sealed additive-only under SO §3.8 · zero sealed module edited (only tcb.py::_TCB_ENTRIES tuple-append per its own docstring line 24 amendment method) · Canon 3 §13 SyniSense ONE ledger doctrine held · MEM-R-053 CROWN BAN NOT triggered · MEM-R-048..MEM-R-052 all not triggered on clean codebase. |

**Milestone snapshot pin (memory-layer close · this-wave · convention: ratchet-state anchor):**
- `passed_floor: 5491`
- `baseline_failures_sha256: 98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`
- Path-relative: `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json`
- Any drift from these pins is a milestone-close fork per SO §6.7 (§6.2 EXIT clause verbatim: "milestone gate closes on a test that binds all sub-waves' evidence"; the ratchet + baseline_failures_sha256 pair is the binding evidence).

**Memory layer standing bounds (unchanged · pending owner ratification per SO §6.3 tier-3 DEFAULT-class):**
- **R-19 (triggers) = DEFAULT-class · pending owner ratification.** Recommended-defaults trigger schedule from memory_compaction_v1 spec §7 remains in force pending explicit owner ratification; tag `pending ratification` retained across W1..W4 build waves. Owner DECISIONS.md:12333 verbatim: *"R-19 (triggers) and R-20 (retention rule set v1): build against the recommended defaults as DEFAULT-class, tagged pending ratification."* No implementation change at this seal.
- **R-20 (retention rule set v1) = DEFAULT-class · pending owner ratification.** Same tier-3 discipline as R-19. Retention rule set v1 baked into `services/memory/compaction_v1/retention.py::RetentionEngine.decide` (deterministic partition (retained, dropped)); v1 default keeps ALL classes (no drops) per MEMORY GO DEFAULT-class discipline. No implementation change at this seal.
- **R-21 (user-memory class, consent model) = flag-OFF by default · awaiting owner ruling.** Owner DECISIONS.md:12333 + 12366 verbatim: *"R-21 (user-memory class, consent model): owner input outstanding — implement the class behind a tenant-wide flag, off by default, no consent model assumed, no principal data written until ruled."* Enforced structurally across M17-W1..W5 by AST bans on principal-data / user-memory / memory-compaction imports on client surfaces; enforced structurally in memory_compaction_v1 by absence of any user-memory-class implementation. No implementation change at this seal.

---

**Autopilot next per owner directive this-turn (verbatim):**

> "Seal W4 (Commit-B + Commit-C, default W3-mirrored templates are fine) and CONTINUE DIRECTLY into CCS1 without stopping. The banked HALT point is BEFORE FRONTENDS, not before CCS — the owner's sequence clause is explicit: contract closure waves on the survey, frontends on the freezes, and the frontends gate is where you halt and report to me for specialist dispatch. Stopping before CCS1 would idle the run one gate early."
>
> "Then CCS1 (C.17 answering-service seam bundle-freeze) → CCS2 (DAP entitlement) → CCS3 (DAP receipt), each frozen from dap_backend_spec_v1 under T-b (JSON-Schema authoritative — freeze from spec even where backend is thin), tests-first, §3.3 sealed. Work the survey's 10 absence findings into the freeze scope: each finding either closes in its CCS wave or is banked with a reason."
>
> "Staleness ceremony has priority if 11:35Z crosses mid-wave — pause at safe checkpoint, small seal, resume."
>
> "At the frontends gate HALT, report to me: survey findings closure status · the three frozen contract pins · UI Handoff Brief path · anything else the specialists need. Go."

1. **Commit-B (this-turn)** → **Commit-C fixup** (state-only · advances state_repo.head to this Commit-B SHA).
2. **CCS1 (C.17 answering-service seam bundle-freeze)** — frozen from `dap_backend_spec_v1` under T-b · JSON-Schema authoritative · tests-first · §3.3 sealed · works survey's 10 absence findings into freeze scope.
3. **CCS2 (DAP entitlement)** — same freeze mechanism.
4. **CCS3 (DAP receipt)** — same freeze mechanism.
5. **HALT before frontends** — POD-level seal report: survey findings closure status + three frozen contract pins + UI Handoff Brief path + anything else specialists need. Wait for owner dispatch to specialists.

**Time-gated task armed:** Staleness re-scope APPLY-ON-EXPIRY at 2026-09-20T~11:35Z (T-~14.3h at this Commit-A · fires as own small seal per owner order · takes priority as small seal when clock hits · owner reaffirmed this-turn: *"Staleness ceremony has priority if 11:35Z crosses mid-wave — pause at safe checkpoint, small seal, resume."*).

**Standing bounds unchanged:** zero push · terminal pytest only · no testing_agent · additive-only §3.8 · full BASELINE_GUARD=1 pre-Commit-A double-green byte-identical · §3.3 3-Commit Seal on dual branches · ratchet monotonic (floor 5491 · never rebaselined silently).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
"""


NEXT_APPEND = """

---

## R-64 · CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION Commit-A landed · 2026-09-19T~21:20Z

⏳ **IN-FLIGHT (Commit-B this-turn banks Commit-A + authors this marker · Commit-C fixup will advance state_head to Commit-B SHA + flip ⏳→✅):** CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · memory-layer follow-on wave W4 · **MEMORY LAYER CLOSES on this seal** · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim + owner W4 EMPHASIS 2026-09-19T~21:00Z verbatim (SEQUENCE not co-existence + M12-W1a AST-ban shape). Commit-A `da2642acdcb5f1785d6ca561913f60fceafd2c6b` on programme/track-a (2026-09-19T~21:12Z UTC). Commit-B (state master · this-turn) lands: STATE/DECISIONS.md Commit-A banking section + memory-layer milestone rollup (W1 +7 · W2 +6 · W3 +3 · W4 +6 · aggregate +22 · 5469 → 5491) + R-19/R-20 DEFAULT-class pending owner ratification + R-21 flag-OFF awaiting owner ruling + STATE/NEXT.md this R-64 marker ⏳ IN-FLIGHT + notes/ORCH_BOOT.md R-6 boundary regen advancing code_head from prior W3 Commit-A `ebebc46f` to this-wave Commit-A `da2642ac` + audit copy re-sync byte-identical. Commit-C fixup will land: STATE/DECISIONS.md gains Commit-C fixup banking section + this marker flip ⏳→✅ + notes/ORCH_BOOT.md R-6 boundary regen advancing state_head to Commit-B + audit copy re-sync.

**W4 scope (owner OPTION 1 verbatim):** "W4 (M10-W4e ledger integration): thin adapter from compaction storage to sealed M10 chain writer path services.memory.ledger. Preserve ordering invariant: ledger row lands BEFORE compaction artifact becomes readable. InMemoryCompactionStorage becomes AST-banned from production imports (test-fixture only)."

**Owner W4 EMPHASIS verbatim (this-session 2026-09-19T~21:00Z):** (1) *"The ordering invariant must prove SEQUENCE, not co-existence — a test that observes both the ledger row and the readable artifact after the fact proves nothing; author it so a read attempted before the ledger write refuses (or the write path structurally cannot expose the artifact until the chain append returns)."* (2) *"The AST ban on InMemoryCompactionStorage from production imports should mirror the negative-scan shape you used at M12-W1a (import-level + call-site level) — tests/** stays allowed."*

**Files landed at Commit-A (+6 tests · new adapter module additive to compaction_v1 sub-package):**
- NEW `backend/services/memory/compaction_v1/chain_integration.py` (335 lines · 4 surfaces: `ChainAppendReceipt` frozen carrier + `ChainGatedReader` receipt-keyed structural gate + `async append_compaction_row_to_chain` awaiting sealed `emit_deletion_ledger_row` with `data_class='memory_publication_landed'` + `async append_compaction_row_and_gate` combined write path).
- NEW `backend/tests/invariants/test_memory_compaction_v1_w4_one_chain_integration.py` (471 lines · 6 invariants: W4.1 read-before-receipt-refuses (SEQUENCE proof) + W4.2 receipt-then-read positive witness + W4.3 `emit_deletion_ledger_row` mock-spy ONE-chain routing + W4.4 chain-refusal-hides-artefact strong-form sequence + W4.5 import-level AST ban + W4.6 call-site AST ban).
- BUMP `backend/tests/invariants/baseline_failures.json` — ratchet 5485 → 5491 (+6 exactly · zero wizard trigger · not a `contracts/*.py` file) · new sha256 `98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`.

**STRUCTURAL SEQUENCE PROOF (owner W4 EMPHASIS #1):** `ChainGatedReader.read()` lookup is receipt-keyed · receipt is minted ONLY inside `append_compaction_row_to_chain` AFTER `await emit_deletion_ledger_row(...)` returns · therefore no receipt exists until chain-append is complete · therefore no bytes are exposable until a receipt exists · therefore the write path structurally cannot expose the artefact until the chain append returns.

**ONE CHAIN routing:** sealed `services.compliance.deletion_ledger.emit_deletion_ledger_row` is the ONE writer per owner ruling 2a 2026-07-31 verbatim ("Northena owns the one ledger; memory must be ledger-reconstructible through the same append-only record, one trace thread, no second ledger"). `data_class='memory_publication_landed'` semantic overload documented in module docstring; dedicated `memory_compaction_landed` would require sealed `data_class_registry.v4.json → v5` bump, deferred.

**AST-BAN allow-list (owner W4 EMPHASIS #2 · M12-W1a-shape):**
- Import-level (W4.5): allows `tests/**` + `services/memory/compaction_v1/**` (self-package · sealed W1 `operations.py` type-annotates `InMemoryCompactionStorage` · grandfathered per SO §3.8 sealed-W1-not-edited discipline).
- Call-site-level (W4.6): allows `tests/**` ONLY (no production instantiation anywhere including `compaction_v1/**` itself · test-fixture-only per owner).

**Pre-authoring RED sweep** at `phase0/drill_receipts/20260919T210936Z_cp_memory_compaction_v1_w4_one_chain_integration_RED_pre.log` — 4/6 fail right-reason ModuleNotFoundError + 2/6 pass right-reason (AST-ban tests pass on clean codebase per W2 crown-ban precedent).

**Post-authoring GREEN** at `phase0/drill_receipts/20260919T211119Z_cp_memory_compaction_v1_w4_one_chain_integration_GREEN_post.log` — 6/6 pass in 2.40s.

**Pre-Commit-A double-green byte-identical BASELINE_GUARD=1:**
- run1 at `phase0/drill_receipts/20260919T211704Z_cp_memory_compaction_v1_w4_preseal_GUARD1_run1.log` · 5491 passed / 1 skipped / 438 warnings · ~182s · raw 58612 B.
- run2 at `phase0/drill_receipts/20260919T212014Z_cp_memory_compaction_v1_w4_preseal_GUARD1_run2.log` · 5491 passed / 1 skipped / 438 warnings · ~182s · raw 58612 B.
- **stripped-sha256 `9fefa0e697f2d3f0175a41367bc7b00530229582a68a3f70cc67d573a60432dd` IDENTICAL** across both runs against FINAL `baseline_failures.json` sha256 `98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`.

**Transparency banking (§6):** 1 prior GUARD1 run1 attempt at `20260919T211248Z` failed `test_decisions_carries_pointer_near_bottom` because `STATE/DECISIONS.md` was missing the pointer near bottom. Defect INHERITED from W3 Commit-C fixup (banking section without trailing pointer); not caught at W3 close because only targeted tests were run post-fixup. Reconciled by pre-W4-Commit-A state-side pointer-append per R-29-BOOT precedent (state-side edit lands in this W4 Commit-B state seal). Not a ratchet break; not a Stop-condition trigger.

**MEMORY-LAYER MILESTONE ROLLUP (owner directive verbatim this-turn):** Memory layer opens at CP-MEMORY-COMPACTION-V1-BUILD-WAVE (R-61 · b1d11836) and CLOSES on this W4 seal. Cumulative delta = W1 +7 (5469 → 5476) + W2 +6 (5476 → 5482) + W3 +3 (5482 → 5485) + W4 +6 (5485 → 5491) = **+22 exactly · 5469 → 5491**. Milestone snapshot pin: `passed_floor: 5491` + `baseline_failures_sha256: 98d207bae61a8834b245be8664a5fd9634e0adddc0c00a67ea154cd09e84302a`. R-19/R-20 remain **DEFAULT-class · pending owner ratification**. R-21 remains **flag-OFF by default · awaiting owner ruling** (no principal data written until ruled).

**Additive-only per SO §3.8 · sealed modules NOT edited:** sealed W1 `compaction_v1/*` (7 files) NOT edited (imported only · `storage.py::InMemoryCompactionStorage` now W4-AST-banned from production) · sealed W-M2-SW7 `tcb.py` NOT edited (W3 tuple-append already banked) · sealed M10 `services/memory/ledger.py` NOT edited · sealed `services/compliance/deletion_ledger.py` NOT edited · sealed `data_class_registry.v4.json` NOT edited (semantic overload used) · sealed M14/M11/M16/M17-W1..W6/W-M2-SW7/W-7bB/c13_scope modules all NOT edited.

**Canon anchors verbatim (Commit-A scope):** MEM-6 [B.4 · DAP-29] · MEM-10 [C.13 · I-1] · MEM-R-012 · MEM-R-013 · MEM-R-050 (grep-negative satisfied structurally by ChainGatedReader refusal) · Canon 3 §13 SyniSense ONE ledger doctrine · Canon 8 §W11 structural role separation · SO §3.8 thin-kernel additive-only · SO §6.4 NOTHING-BEYOND (scope frozen at 4 surfaces + 6 invariants) · M12-W1a AST-ban precedent · M16 R-3 2026-09-09 precedent · owner ruling 2a 2026-07-31 verbatim · owner MEMORY GO ruling verbatim · owner OPTION 1 ratification verbatim · owner W4 EMPHASIS verbatim.

**Stop-conditions #1/#2/#3 NOT triggered at Commit-A · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.** Ratchet 5485 → 5491 monotonic-up. Zero flip. Zero regression. Zero refactor.

**Autopilot next per owner directive this-turn:**
1. **Commit-B (this-turn) → Commit-C fixup** (state-only · advances state_repo.head to this-Commit-B SHA · flips this marker ⏳→✅).
2. **CCS1 (C.17 answering-service seam bundle-freeze)** — frozen from `dap_backend_spec_v1` under T-b · JSON-Schema authoritative · tests-first · §3.3 sealed · works survey's 10 absence findings into freeze scope.
3. **CCS2 (DAP entitlement)** → **CCS3 (DAP receipt)** — same freeze mechanism.
4. **HALT before frontends** — POD-level seal report: survey findings closure status + three frozen contract pins + UI Handoff Brief path + anything else specialists need. Wait for owner dispatch to specialists.

**Time-gated task armed:** Staleness re-scope APPLY-ON-EXPIRY at 2026-09-20T~11:35Z (T-~14.3h at this Commit-A · fires as own small seal per owner order · takes priority as small seal when clock hits · owner reaffirmed this-turn "Staleness ceremony has priority if 11:35Z crosses mid-wave — pause at safe checkpoint, small seal, resume").

**Standing bounds unchanged:** zero push · terminal pytest only · no testing_agent · additive-only §3.8 · full BASELINE_GUARD=1 pre-Commit-A double-green byte-identical · §3.3 3-Commit Seal on dual branches · ratchet monotonic (floor 5491 · never rebaselined silently).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
"""


def append_if_absent(path: Path, sentinel: str, content: str) -> tuple[bool, str]:
    """Append content to path if sentinel is not present.

    Returns (did_append, message).
    """
    body = path.read_text(encoding="utf-8")
    if sentinel in body:
        return False, f"SKIP (sentinel present): {path}"
    new_body = body + content
    path.write_text(new_body, encoding="utf-8")
    return True, f"APPENDED {len(content)} bytes to {path} (new size {len(new_body)} bytes)"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    print(f"Pre-edit DECISIONS.md sha256: {sha256_of(DECISIONS)}")
    print(f"Pre-edit NEXT.md sha256:      {sha256_of(NEXT)}")
    print()

    did_dec, msg_dec = append_if_absent(DECISIONS, IDEMPOTENT_SENTINEL, DECISIONS_APPEND)
    print(msg_dec)

    did_next, msg_next = append_if_absent(NEXT, NEXT_SENTINEL, NEXT_APPEND)
    print(msg_next)

    print()
    print(f"Post-edit DECISIONS.md sha256: {sha256_of(DECISIONS)}")
    print(f"Post-edit NEXT.md sha256:      {sha256_of(NEXT)}")
    print(f"Post-edit DECISIONS.md lines:  {sum(1 for _ in open(DECISIONS))}")
    print(f"Post-edit NEXT.md lines:       {sum(1 for _ in open(NEXT))}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
