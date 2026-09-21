"""R-90 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Precedent shape (mirrors tools/r88_commit_c_fixup_orch_boot_regen.py exactly):
- state_repo (heads_last_sealed.state_repo): replaced with R-90 Commit-B
  `19bfd333e3ef557e55ae359989cde1b9c2fde6d4` entry.
- code_repo history: fresh entry for R-90 Commit-A
  `457d9473ae1a536a9b835b6dfe970faf9596b95b` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-90 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive: heads_last_sealed history is append-only for code_repo entries;
state_repo is a single current-head slot that advances at each Commit-C.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R90_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R90_STATE_HEAD = "19bfd333e3ef557e55ae359989cde1b9c2fde6d4"
R90_CODE_HEAD = "457d9473ae1a536a9b835b6dfe970faf9596b95b"
R90_STATE_SEALED_AT = "2026-09-20T23:15:00Z"
R90_CODE_SEALED_AT = "2026-09-20T23:00:00Z"
NEW_UTC = "2026-09-20T23:18:00Z"
NEW_REGEN_REASON = (
    "r90-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-19bfd333-"
    "cp-content-registry-wave-third-slice-con-22-to-31-plus-grep-negative-bans-4-to-7-"
    "commit-b-plus-new-code-repo-history-entry-for-r90-commit-a-457d947-closes-ruling-4-scope"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R90_STATE_HEAD}
    sealed_at_utc: {R90_STATE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE third slice CON-22..CON-31 + grep-negative bans #4..#7 · state Commit-B `{R90_STATE_HEAD}` · banks Commit-A `{R90_CODE_HEAD}` on programme/track-a · WAVE R-90 · Ruling 4 third slice + owner ruling this-session verbatim (2026-09-20T~23:12Z: complete the R-90 3-Commit Seal now under the already-ratified Ruling-4 standing-GO · work is honest inside ratified scope with double-green byte-identical evidence already banked in receipts · defect is prior fork's REPORT not the repo · rolling back honest sealed-quality work to cure a reporting error would be backwards · execute Commit-B then Commit-C fixup then post-Commit-C verify subset test_orch_boot + baseline manifest + R-90 wave tests via terminal pytest before reporting seal · if anything not GREEN stop-and-report rather than seal · YES bank the spec-hunt receipt documenting the discrepancy with standing lesson session summaries are NEVER evidence of seal state git log on both branches is · then open G5-v5 SFP-1..7 first slice per queue and prior directives) + owner standing-GO (2026-09-20T~22:35Z at R-89 Commit-B) for R-90 immediately-after-R-89-seals-clean under Ruling-4 scope · Prior-fork misreport RESOLVED via ground-truth re-anchor + audit receipt phase0/spec_hunt_receipts/20260920T231420Z_r90_prior_fork_misreport_seal.md · Standing lesson banked · Straight-shot additive slice within ratified Ruling-4 scope · No new stop-conditions · No card edit · Vocabulary module additively extended with §6 The Generated Path (CON-22) + §7 Storage and Persistence (CON-23..CON-26) + §8 Erasure and Retention (CON-27..CON-28) + §9 Freshness (CON-29..CON-31) sections + 4 new pure-data-in scanners completing 7-category grep-negative ban set (ban #4 scan_for_softening_of_unsupported_claims at CON-24 + ban #5 scan_for_templated_text_storage at CON-25 + ban #6 scan_for_generated_text_as_render_dependency at CON-26 + ban #7 scan_for_unsupported_claim_state at CON-24) · 10 property invariants CON-22..CON-31 · DELTA +10 MEASURED (5678 → 5688 monotonic-up per CCS2 both fields bumped together · no test flipped to fail · CCS2-aligned across counts.passed/passed_floor/ratchet_history[-1].passed) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 a767ca9c43549cf570b5f92f83efde58a6e3f4c768d703a07287ae2a24344973 IDENTICAL across drill_receipts/20260920T225736Z_run1 (181.20s · 5688 passed) + 20260920T230212Z_run2 (182.45s · 5688 passed) both 5 baseline-fails (3 mirror-drift + 2 v8 cascade all from R-88+ carrying forward · covered by exactly one annotation field under total-coverage guard verified this-slice) 1 skip 438 warnings against post-bump baseline_failures.json sha256 37eaae80813d4b79a937b08a8e95554f7c3e88661074408561c59232dc69963e · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 6f36497958a9fac78b771198f824bcfa21b7053167305457f4eb55ec7e468a8c) · Files (9 tracked at Commit-B): STATE/DECISIONS.md this-append (full seal report + owner ruling verbatim + prior-fork misreport disposition) + STATE/NEXT.md this-append (R-90 SEALED marker + G5-v5 opens next) + STATE/PINS.md this-append (R-90-THIRD-SLICE-PINS block) + notes/ORCH_BOOT.md this-ratchet-regen + tools/r90_pre_commit_a_orch_boot_regen.py NEW + 3 drill receipts this-slice + phase0/spec_hunt_receipts/20260920T231420Z_r90_prior_fork_misreport_seal.md NEW · No card edit required for R-90 · R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged · Total-coverage guard (Guard #1 from R-88+) still GREEN this-slice (0 uncovered · 0 double-covered) · R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged) · RULING-4 SCOPE CLOSED at this-slice (all 31 CON-1..CON-31 + all 7 grep-negative bans + R-32 surface list binding on Generated-class at CON-22) · Canon anchors verbatim: owner ruling this-session (2026-09-20T~23:12Z) + owner standing-GO (2026-09-20T~22:35Z at R-89 Commit-B) + owner Ruling 4 CP-CONTENT-REGISTRY-WAVE (CLOSED) + owner Ruling 5 SRR-as-authority + SRR v5 rows 587-596 + R-89 seal 49e2a338/76c530f0/f2638177 + R-88 seal db90089d/79d5d38d/0cbfc23b + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R90_STATE_HEAD} + inserts code_repo entry for R90 Commit-A {R90_CODE_HEAD}) → post-Commit-C verify subset per owner ruling → G5-v5 SFP-1..7 first slice per owner canonical directives"
"""

NEW_R90_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R90_CODE_HEAD}
    sealed_at_utc: {R90_CODE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE third slice CON-22..CON-31 + grep-negative bans #4..#7 · Commit-A `{R90_CODE_HEAD}` · code programme/track-a · WAVE R-90 · Ruling 4 third slice + owner standing-GO (2026-09-20T~22:35Z at R-89 Commit-B) · CLOSES Ruling-4 scope · Additive extension of services/content_registry/content_registry_vocabulary.py with §6 The Generated Path (CON-22) + §7 Storage and Persistence (CON-23..CON-26) + §8 Erasure and Retention (CON-27..CON-28) + §9 Freshness (CON-29..CON-31) load-bearing Final[...] constants: GENERATED_R32_SURFACES_ORDERED_BY_SALIENCE + GENERATED_RESOLVER_ORDERS_FINDINGS_BEFORE_DRAFTING + GENERATED_MODEL_WRITES_SENTENCES_NOT_ORDER + GENERATED_GATES 3-tuple + GENERATED_STRING_STORED_AS_ARTEFACT_BY_HASH + GENERATED_ARTEFACT_MANDATORY_FIELDS 5-tuple + GENERATED_ARTEFACT_RETRIEVABLE_BY_HASH + GENERATED_RETENTION_RULE_R35 + READER_MAY_SEE_ANCHORS_ON_DEMAND + GENERATED_UNSUPPORTED_FACT_REFUSED_BEFORE_DISPLAY + SOFTENING_IS_FORBIDDEN (ban #4 anchor) + UNSUPPORTED_CLAIMS_FORBIDDEN (ban #7 anchor) + A5_5_BINDING_FORBIDS_SILENT_DOWNGRADE + TEMPLATED_STRING_NOT_STORED_AS_TEXT (ban #5 anchor) + TEMPLATED_CONTENT_RECEIPT_STORES_TEMPLATE_VERSION_AND_DEPENDENCY_VALUES_BY_REFERENCE + TEMPLATED_STRING_REDERIVED_ON_DEMAND + STORING_TEMPLATED_TEXT_CREATES_DIVERGENCE_RISK + FIXED_STRING_STORED_ONCE_AS_CONTRACT + HOOK_CHOICE_STORED_AS_TRACE_PER_CON_20 + GENERATED_TEXT_NOT_STORED_AS_INPUT_TO_SUBSEQUENT_RENDER (ban #6 anchor) + STORAGE_RULES_BY_CLASS 3-pair + ERASURE_REACHES_GENERATED_ARTEFACTS + WITHDRAWAL_TRIGGERS_ANCHOR_TRACE + GENERATED_ARTEFACT_RECALLED_OR_REDERIVED_WITHOUT_WITHDRAWN_UNIT + ERASURE_MECHANISM_DAP_38_AND_MEM_9 2-tuple + RETENTION_DEFAULT_R35 + ERASURE_PRECEDENCE_OVER_RETENTION_PER_MEM_9 + TEMPLATED_RERENDERS_ON_ANY_DEPENDENCY_CHANGE + LEDGER_EVENT_TYPES_TRIGGERING_RERENDER 3-tuple SRR byte-verbatim + SCHEDULER_NOT_NEEDED_FOR_EVENT_EMITTING_DEPENDENCY + SCHEDULE_ONLY_FOR_ENTRY_WITH_NON_EVENT_DEPENDENCY + SCHEDULED_ENTRY_RECORDS_SCHEDULE_AND_INTERVAL_ON_ENTRY + SCHEDULED_ENTRY_DISPLAYS_AS_OF_TIME + UNREACHABLE_TRIGGER_DISPLAYS_STALE_MARKER + STALE_MARKER_REQUIRES_VISIBLE_INDICATOR_AND_AS_OF_TIME + SILENT_HOLD_AS_CURRENT_FORBIDDEN + STALE_MARKING_IS_THE_ONE_DEGRADATION_PERMITTED · Adds 4 new pure-data-in scanner helpers completing 7-category grep-negative ban set: scan_for_softening_of_unsupported_claims (CON-24 ban #4 · 5 watched patterns) + scan_for_unsupported_claim_state (CON-24 ban #7 · 4 watched patterns) + scan_for_templated_text_storage (CON-25 ban #5 · 4 watched patterns) + scan_for_generated_text_as_render_dependency (CON-26 ban #6 · 4 watched patterns) · Adds 1 NEW test module backend/tests/invariants/test_content_registry_v1_section_6_to_9.py with 10 property tests CON-22..CON-31 · each carries SO §2.5 verbatim-docstring quoting SRR statement byte-verbatim · each asserts Final[...] annotation + value binding · CON-24/CON-25/CON-26 tests each enforce scanner behavior byte-verbatim across all watched patterns · CLOSURE at this-slice: all 31 CON rules registered as Final[...] vocabulary AND all 7 grep-negative bans anchored (ban #1 CON-1 + #2 CON-6 + #3 CON-18 + #4 CON-24 + #5 CON-25 + #6 CON-26 + #7 CON-24) · DELTA +10 MEASURED (5678 → 5688 monotonic-up per CCS2 both fields bumped together · new baseline_failures.json sha256 37eaae80 was 504cc47f · new ORCH_BOOT.md sha256 6f364979 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · R-88/R-89 CON-1..21 module + tests continue verbatim GREEN · R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged · AUTHENTIC additive-only cycle: vocabulary extended in place with §6-§9 sections + 4 scanners (module docstring updated to R-88..R-90 range · SO §3.8 additive-only preserved · CON-1..CON-21 sections and existing scanners unchanged byte-verbatim below insertion points) → GREEN at drill_receipts/20260920T225030Z_r90_third_slice_section_6_to_9_GREEN_post.log (31/31 pass 0.96s all CON-1..31) → BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 a767ca9c43549cf570b5f92f83efde58a6e3f4c768d703a07287ae2a24344973 IDENTICAL run1 (5688 passed) + run2 (5688 passed) both 5 baseline-fails 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r90_pre_commit_a_orch_boot_regen.py) · Canon anchors verbatim: owner standing-GO (2026-09-20T~22:35Z) + owner Ruling 4 CP-CONTENT-REGISTRY-WAVE (CLOSED by this slice) + owner Ruling 5 SRR-as-authority + SRR v5 rows 587-596 as authority (Ruling 5) + R-89 seal 49e2a338/76c530f0/f2638177 (immediately-precedes) + R-88 seal db90089d/79d5d38d/0cbfc23b + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master (this-session-completed via owner ruling 2026-09-20T~23:12Z after prior-fork misreport re-anchor) → Commit-C fixup → post-Commit-C verify subset → G5-v5 SFP-1..7 first slice per queue"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    # Idempotency guard: if state_repo.head already equals R90_STATE_HEAD, skip.
    if f"head: {R90_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-90 Commit-B.")
    else:
        # Replace state_repo section + insert new code_repo entry at top of history.
        state_repo_regex = re.compile(
            r"heads_last_sealed:\n"
            r"  state_repo:\n"
            r"    workdir: /app/assessment_workspace\n"
            r"    branch: master\n"
            r"    head: [0-9a-f]{40}\n"
            r"    sealed_at_utc: [^\n]+\n"
            r'    seal_kind: "[^\n]+"\n',
            re.DOTALL,
        )
        m = state_repo_regex.search(text)
        if not m:
            raise SystemExit("Could not locate heads_last_sealed.state_repo block")
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R90_CODE_REPO_BLOCK + text[m.end():]

    # Update generated_at_utc + regeneration_reason
    text = re.sub(
        r"^generated_at_utc:.*$",
        f"generated_at_utc: {NEW_UTC}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^regeneration_reason:.*$",
        f"regeneration_reason: {NEW_REGEN_REASON}",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)


def main() -> None:
    regen_orch_boot_commit_c()
    print(f"heads_last_sealed.state_repo.head → {R90_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R90_CODE_HEAD}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
