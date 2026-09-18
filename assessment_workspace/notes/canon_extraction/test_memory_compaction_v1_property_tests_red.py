"""notes/canon_extraction/test_memory_compaction_v1_property_tests_red.py

Step 3 of memory_compaction_v1 ingestion · Property tests authored RED.

Owner ingest directive 2026-09-18T~11:35Z verbatim:
  "Author the property tests before any implementation, tests-first RED per §3.3:
   fact text_hash unchanged through compaction;
   every provenance reference preserved;
   loss-statement counts equal actual drops by class;
   reload byte-identical for the same (artefact, key);
   reload refuses on hash mismatch;
   erasure query finds every artefact whose provenance cites a given unit;
   no compaction artefact readable without its ledger row."

State-repo mirror location.  Landing in the code repo (backend/tests/invariants/)
is DEFERRED to the memory_compaction_v1 build wave open (M12b → M13-rest interval
per SER v1.1 C.13 delta §7), which is EXPLICITLY OUT-OF-SCOPE for the 4-hour
autonomous window per owner directive:

  "3. memory_compaction_v1 ingestion, steps 1-3 only — atomic-rule extraction,
      the SER v1.1 C.13 delta as a draft, the property tests authored RED.
      No build wave."

Right-reason RED (ModuleNotFoundError) will surface when this file is copied to
the code repo at wave-open, because `services.memory.*` does not exist.  The
imports below are the shape the wave-open agent must satisfy to move to GREEN.

Canon anchors (verbatim):
  * MEM-1: compaction excludes Ledger/receipts/provenance/audit log.
  * MEM-2: fact-class NEVER paraphrased; pointer-by-hash or drop.
  * MEM-3: retention decided by deterministic versioned rule set.
  * MEM-4: triggers deterministic (never model judgement).
  * MEM-5: new hash + lineage; source versions recorded.
  * MEM-6: ledger row BEFORE artefact readable; loss statement = counts by class.
  * MEM-7: reload deterministic; hash-verify or fail closed.
  * MEM-8: reload states class-lost; consumer can't upgrade class.
  * MEM-9: erasure reaches compacted memory via provenance ref (DAP-38 mechanism).
  * MEM-10: user memory is principal data.
  * MEM-11: idempotent per (key, source version hash); concurrent-run isolation.
"""
from __future__ import annotations

# NOTE (STATE-REPO): these imports resolve at code-repo landing wave-open.
# In the state repo, this file is a documentation artefact.  The
# `services.memory.*` module path is what the wave-open build must provide.
#
# from services.memory import (
#     RetentionEngine,        # MEM-3 · deterministic
#     ReloadVerifier,         # MEM-7 · deterministic
#     DraftingComponent,      # MEM-2 · learned (OUT-of-TCB)
#     CompactionArtefactRef,  # frozen carrier
#     CompactionLedgerRow,    # MEM-6 · frozen carrier
#     compact,                # entrypoint · returns (artefact_ref, ledger_row_ref)
#     reload,                 # entrypoint · MEM-7 · returns artefact bytes or refuses
#     erasure_query,          # MEM-9 · returns list of artefacts to re-derive/recall
# )
# from services.data.repository import Repository, Context     # M11-W1 dep

# --- Test 1 · fact_text_hash unchanged through compaction ------------------

def test_fact_text_hash_unchanged_through_compaction():
    """MEM-2 · MEM-R-005 · fact-class claims are pointer-by-hash, never rewritten.

    Given: a run-scoped context with a fact-class claim carrying text_hash T.
    When:  compact() runs against that context under retention rule set v1.
    Then:  the compacted artefact's provenance-anchor for that claim carries
           text_hash T (byte-identical); the compacted artefact contains NO
           text of the fact class (pointer-only).

    Failure mode:
      - text_hash differs -> MEM-2 boundary violated (fact was rewritten).
      - fact-class text present in compacted artefact body -> paraphrase
        occurred (MEM-R-049 hard ban).
    """
    raise AssertionError(
        "Right-reason RED: services.memory.compact not implemented yet.  "
        "Wave-open must implement compact() + retention rule v1 keep-rule (b)."
    )


# --- Test 2 · every provenance reference preserved through compaction -----

def test_every_provenance_reference_preserved_through_compaction():
    """MEM-2 · MEM-R-002 · every claim anchors to a retained source by
    provenance reference AND text hash; an unanchored claim is refused.

    Given: a run-scoped context with N provenance references across classes
           {fact, inference, utterance, receipt_ref, refusal, approval}.
    When:  compact() runs.
    Then:  the compacted artefact's provenance set is a SUPERSET of every
           source provenance reference (nothing dropped without a ledger
           row entry naming the drop).

    Failure mode:
      - any provenance ref missing from artefact AND from loss statement
        -> MEM-2 + MEM-6 dual violation.
    """
    raise AssertionError("Right-reason RED: compact + loss statement not implemented.")


# --- Test 3 · loss-statement counts equal actual drops by class -----------

def test_loss_statement_counts_equal_actual_drops_by_class():
    """MEM-6 · MEM-R-014 · loss statement is enumerated by class.

    Given: a run-scoped context with known population {fact: F, inference: I,
           utterance: U, receipt_ref: R, refusal: Rf, approval: A, objective: O,
           floor: Fl} of provenance references.
    When:  compact() runs under retention rule set v1.
    Then:  the ledger row's loss_statement is exactly:
             {fact: 0,                # MEM-3(b) never dropped without ledger; but see (b): 'MAY be dropped'
              inference: I - I_kept,  # from MEM-3 permit-summary
              utterance: U - U_kept,  # from MEM-3 permit-summary (where quoting)
              receipt_ref: 0,         # MEM-3(a) never paraphrased
              refusal: 0,             # MEM-3(d) always kept
              approval: 0,            # MEM-3(e) always kept
              objective: 0,           # MEM-3(c) verbatim
              floor: 0}               # MEM-3(c) verbatim
           AND the sum-across-classes equals total_drops.

    Failure mode:
      - any class count != actual drop count -> loss statement dishonest.
      - fact drops without a matching ledger row entry naming the drop
        -> MEM-R-005 violated silently.
    """
    raise AssertionError("Right-reason RED: loss statement structure not implemented.")


# --- Test 4 · reload byte-identical for same (artefact, key) --------------

def test_reload_byte_identical_for_same_artefact_key():
    """MEM-7 · MEM-R-015 · reload is deterministic.

    Given: a compacted artefact with hash H under key K.
    When:  reload(K, H) is called TWICE within artefact lifetime.
    Then:  both calls return byte-identical bytes.  NO re-summarisation on read.

    Failure mode:
      - bytes differ -> MEM-R-051 hard ban violated (re-summarised on read).
      - non-deterministic ordering surfaced -> reload contract broken.
    """
    raise AssertionError("Right-reason RED: services.memory.reload not implemented.")


# --- Test 5 · reload refuses on hash mismatch -----------------------------

def test_reload_refuses_on_hash_mismatch():
    """MEM-7 · MEM-R-016 · reload hash-verify or fail closed.

    Given: a compacted artefact registered with hash H under key K; the
           on-disk artefact bytes tampered to yield hash H' != H.
    When:  reload(K, expected_hash=H) is called.
    Then:  reload raises MemoryReloadRefusalError (fail closed; caller refused).
           Downstream reader NEVER sees best-effort bytes.

    Failure mode:
      - reload returns any bytes -> MEM-7 boundary violated (silent serve).
      - reload raises but downstream STILL gets bytes -> caller-refuse contract broken.
    """
    raise AssertionError("Right-reason RED: hash-verify path not implemented.")


# --- Test 6 · erasure_query finds every artefact citing a given unit ------

def test_erasure_query_finds_every_artefact_whose_provenance_cites_a_given_unit():
    """MEM-9 · MEM-R-019 · erasure reaches compacted memory via provenance ref.

    Given: a corpus of compacted artefacts, of which K carry a provenance
           reference to unit U.
    When:  erasure_query(unit=U) is called.
    Then:  the returned set of artefact refs has size == K and each element
           is uniquely one of the K artefacts.  NO omissions; NO extras.
           The mechanism is DAP-38 (per MEM-R-021).

    Failure mode:
      - size != K -> erasure incomplete; MEM-9 not met; Kenya DPA s.40 breach class.
      - includes an artefact NOT citing U -> false positive; erasure over-reaches.
    """
    raise AssertionError("Right-reason RED: services.memory.erasure_query not implemented.")


# --- Test 7 · no compaction artefact readable without its ledger row ------

def test_compaction_artefact_not_readable_without_ledger_row():
    """MEM-6 · MEM-R-012 + MEM-R-013 · ledger row BEFORE artefact readable.

    Given: a partial-completion state — the compacted artefact bytes are
           written to storage but the ledger row write failed OR was skipped.
    When:  reload(K, H) is called against the storage.
    Then:  reload raises MemoryLedgerRowMissingRefusalError (fail closed).
           Downstream reader NEVER sees the artefact.

    Failure mode:
      - reload returns bytes -> MEM-R-050 hard ban violated (compaction
        without ledger row first).  Design converged on 'summarise, delete'
        pattern -> stop-and-report per ingest closing directive.
    """
    raise AssertionError("Right-reason RED: ledger-row-precedes-read discipline not implemented.")


# --- Anti-patterns · hard-ban grep-negative surface (informational) ------

# The following anti-pattern tests will be authored at wave-open as
# grep-negative invariants across the full code repo (backend/**/*.py).
# They are stated here as the ban-surface for the wave-open agent:
#
#   test_no_learned_component_decides_retention          # MEM-R-048
#   test_no_fact_class_text_paraphrased                  # MEM-R-049
#   test_no_compaction_without_ledger_row_first          # MEM-R-050
#   test_no_re_summarisation_on_read                     # MEM-R-051
#   test_no_compaction_of_ledger_receipts_provenance     # MEM-R-052
#   test_design_convergence_stop_and_report              # MEM-R-053
