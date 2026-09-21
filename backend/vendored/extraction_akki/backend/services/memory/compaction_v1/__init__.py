"""services.memory.compaction_v1 · Memory Compaction Layer v1.

Owner MEMORY GO order (banked at STATE/DECISIONS.md this-cycle):
  memory_compaction_v1 build wave · 7 ingestion-authored property
  tests drive the build (they were authored RED at ingestion; find
  them in tests/, do not re-author blind) · memory_compaction_v1 spec
  from custody/owner_drops/Memory_Compaction_Spec_v1.docx (sha-pinned
  drop manifest at phase0/credential_drop_manifests/20260918T1139Z) ·
  R-19/R-20 recommended defaults DEFAULT-class · R-21 user-memory class
  behind tenant flag OFF with no principal data · TCB entries via
  tcb_enumeration_v1 method (MEM-3 engine IN, MEM-7 reload verifier IN,
  drafting OUT) · hard bans grep-negative (no learned retention · no
  paraphrase · no ledger-less compaction · no re-summarise on read · no
  compaction of Ledger/receipts/provenance/audit) · compaction rows on
  the ONE chain · §3.3 seals · additive-only · full pre-Commit-A double-
  green.

Landing adaptation from ingestion (banked at DECISIONS.md this-wave):
  Ingestion-authored notes/canon_extraction/test_memory_compaction_v1_
  property_tests_red.py used package-level imports from `services.memory`
  (a pre-existing sealed package · M10-W4e ledger/plane_registry/
  write_back/etc.).  Per SO §3.8 additive-only + c13_scope precedent
  (new sub-package · docstring-only __init__), this wave lands the
  compaction_v1 surface at `services.memory.compaction_v1` as a NEW
  sub-package.  Ingestion-authored SHAPE (module surface, Given/When/
  Then contract per docstring) preserved verbatim; only the import
  path is adapted for additive-only compliance.

Canon 8 §W11 structural role separation preserved:
  - carriers.py: frozen pydantic carriers ONLY (Claim,
    RunScopedContext, CompactionArtefactRef, CompactionLedgerRow,
    ClassAnchor, RetentionRuleSetVersion) · no logic.
  - refusals.py: fail-closed refusal exception types ONLY.
  - retention.py: RetentionEngine (deterministic · TCB IN via MEM-3)
    + DraftingComponent (learned · TCB OUT via MEM-2) · role-separated
    surfaces on the SAME module boundary.
  - verifier.py: ReloadVerifier (deterministic · TCB IN via MEM-7).
  - storage.py: InMemoryCompactionStorage (deterministic ·
    ledger-row-precedes-artefact-readability invariant enforced at
    the storage boundary · MEM-R-012 + MEM-R-013).
  - operations.py: compact + reload + erasure_query entrypoints.

Determinism inventory (`determinism_inventory_v1` per Spec §4):
  Hybrid — drafting Learned; retention decision, trigger, receipt,
  reload Deterministic.  This v1 keeps ALL classes (no drop, no
  summarise); the drafting component is present as an interface
  point for future retention-rule sets but is NOT called from the
  v1 default path.

Failure posture (`failure_posture_v1` per Spec §4):
  Compaction cannot complete (rule set unreadable, receipt unwritable)
  -> fail-closed on the compaction · source retained untouched.
  Reload unverifiable -> refuse (MemoryReloadRefusalError).
  Ledger row missing -> refuse (MemoryLedgerRowMissingRefusalError).

Additive-only per SO §3.8: this sub-package is a new tree; no sealed
module is edited (services/memory/__init__.py NOT edited).
"""

from services.memory.compaction_v1.carriers import (
    Claim,
    ClassAnchor,
    CompactionArtefactRef,
    CompactionLedgerRow,
    RetentionRuleSetVersion,
    RunScopedContext,
)
from services.memory.compaction_v1.operations import (
    compact,
    erasure_query,
    reload,
)
from services.memory.compaction_v1.retention import (
    DraftingComponent,
    RetentionEngine,
)
from services.memory.compaction_v1.verifier import ReloadVerifier

__all__: tuple[str, ...] = (
    "Claim",
    "ClassAnchor",
    "CompactionArtefactRef",
    "CompactionLedgerRow",
    "DraftingComponent",
    "ReloadVerifier",
    "RetentionEngine",
    "RetentionRuleSetVersion",
    "RunScopedContext",
    "compact",
    "erasure_query",
    "reload",
)
