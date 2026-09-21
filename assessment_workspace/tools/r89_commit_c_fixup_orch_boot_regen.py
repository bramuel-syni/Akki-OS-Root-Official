"""R-89 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Precedent shape mirrors tools/r88_commit_c_fixup_orch_boot_regen.py exactly.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R89_STATE_HEAD).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R89_STATE_HEAD = "76c530f0819eadf4cfa48a55899fbec86ac61a55"
R89_CODE_HEAD = "49e2a3384f8573a33bfc389362febac766986bce"
R89_STATE_SEALED_AT = "2026-09-20T22:47:00Z"
R89_CODE_SEALED_AT = "2026-09-20T22:44:00Z"
NEW_UTC = "2026-09-20T22:50:00Z"
NEW_REGEN_REASON = (
    "r89-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-76c530f0-"
    "cp-content-registry-wave-second-slice-con-12-to-21-commit-b-plus-new-code-repo-"
    "history-entry-for-r89-commit-a-49e2a338"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R89_STATE_HEAD}
    sealed_at_utc: {R89_STATE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE second slice CON-12..CON-21 · state Commit-B `{R89_STATE_HEAD}` · banks Commit-A `{R89_CODE_HEAD}` on programme/track-a · WAVE R-89 · Ruling 4 second slice + owner standing-GO this-session verbatim (2026-09-20T~22:35Z: 'GO for R-89 second slice (CON-12..CON-21) now, and standing GO for R-90 third slice (CON-22..CON-31 + remaining grep-negative bans) immediately after R-89 seals clean — no per-slice check-in needed; these are inside the ratified Ruling-4 scope and SO §6 autopilot governs. Then G5-v5 SFP-1..7 slice per queue. Unchanged holds: the OWNER-RATIFICATION-PENDING block (D + A rulings) stays flagged until the owner's next reply — if he overrides, execute the mechanical unwind before whatever wave is then in flight opens its Commit-A. R-91 stays at its scheduled slot. HF-HOLD/R-24/R-25 as banked. Standing bounds unchanged. Proceed.') · Straight-shot additive slice within ratified Ruling-4 scope · No new stop-conditions · No card edit · Vocabulary module additively extended with §4 The Resolver + §5 The Slot Model / Salience sections + new pure-data-in scanner for grep-negative ban #3 anchor (CON-18: views/dwell/clicks/replies + learned_score + engagement_score + predicted_ctr) · 10 property invariants CON-12..CON-21 · DELTA +10 MEASURED (5668 → 5678 monotonic-up per CCS2 both fields bumped together · no test flipped to fail · CCS2-aligned across counts.passed/passed_floor/ratchet_history[-1].passed) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 0802eaabbaed0f120686960dbd82034c119b0307a1e3de79c175bed74a1ab900 IDENTICAL across drill_receipts/20260920T223632Z_run1 (181.40s · 5678 passed) + 20260920T224113Z_run2 (180.90s · 5678 passed) both 5 baseline-fails (unchanged from R-88+ · covered by exactly one annotation field under total-coverage guard verified this-slice) 1 skip 438 warnings against post-bump baseline_failures.json sha256 504cc47fd5eeb200d467c179fe4fba054de17dec04b1f125d9e49fa5f518fa12 · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 c9f5c2150fbb0a4822f39a24895446f250bcf3d724c34fa93f9aebe5169bb6b1) · Files (8 tracked at Commit-B): STATE/DECISIONS.md this-append (full seal report + owner standing-GO verbatim) + STATE/NEXT.md this-append + STATE/PINS.md this-append + notes/ORCH_BOOT.md this-ratchet-regen + tools/r89_pre_commit_a_orch_boot_regen.py NEW + 3 drill receipts this-slice · No card edit required for R-89 (CP_APP_JS_UNIFY.md scheduled closure carries forward unchanged from R-88+) · R-88+ OWNER-RATIFICATION-PENDING block (D-ruling + A-extension) carries forward unchanged · Total-coverage guard (Guard #1 from R-88+) still GREEN across this slice's double-sweep (0 uncovered baseline entries · 0 double-covered baseline entries) · R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged this-slice) · Canon anchors verbatim: owner standing-GO this-session + owner Ruling 4 + owner Ruling 5 + SRR v5 rows 577-586 + R-88 first-slice seal db90089d/79d5d38d/0cbfc23b + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance (Ruling-4 scope standing-GO no per-slice check-in) + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered this-slice · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R89_STATE_HEAD} + inserts code_repo entry for R89 Commit-A {R89_CODE_HEAD}) → R-90 third slice CON-22..CON-31 + remaining grep-negative bans #4..#7 opens IMMEDIATELY per owner standing-GO"
"""

NEW_R89_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R89_CODE_HEAD}
    sealed_at_utc: {R89_CODE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE second slice CON-12..CON-21 · Commit-A `{R89_CODE_HEAD}` · code programme/track-a · WAVE R-89 · Ruling 4 second slice + owner standing-GO this-session verbatim (2026-09-20T~22:35Z) · Straight-shot additive slice · Additive extension of services/content_registry/content_registry_vocabulary.py with §4 The Resolver (CON-12..CON-14) + §5 The Slot Model / Salience (CON-15..CON-21) load-bearing Final[...] constants: RENDERING_IS_PURE_FUNCTION + RENDERING_INPUT_TUPLE 3-tuple + GENERATION_REQUEST_MANDATORY_FIELDS 4-tuple + LEARNED_OUTPUT_REENTERS_RESOLVER + LEARNED_CANNOT_ALTER_FIXED_OR_TEMPLATED_RENDER + LEARNED_PROPOSALS_VIA_RESEARCH_QUEUE + PROPOSAL_RATIFIED_BY_CEREMONY_OR_NOTHING + PROPOSALS_NEVER_TAKE_EFFECT_ON_PROPOSAL + RESOLVER_FAILS_CLOSED + MISSING_DEPENDENCY_RENDERS_HONEST_GAP + MISSING_ENTRY_RENDERS_NOTHING + GENERATED_FAILS_CLASSING_OR_GATE_REFUSED_WITH_ONE_REFUSAL_CARD + IMPROVISED_FILL_REFUSED + SALIENCE_CLASS_COUNT=4 + SALIENCE_CLASS_DEFINITIONS 4-pair ordered tuple + RANKING_RULE_R33_VERSIONED + HOOK_SELECTION_LOWEST_SALIENCE_CLASS + HOOK_TIES_RESOLVE_BY_CANDIDATE_LIST_ORDER + RANKING_IS_DETERMINISTIC + INELIGIBLE_CANDIDATE_ANY_DEP_NULL + INELIGIBLE_CANDIDATE_NEVER_HOOK_WHILE_ELIGIBLE_EXISTS + NO_ELIGIBLE_RENDERS_FIRST_CANDIDATE_HONEST_GAP + GAP_NEVER_HEADLINED_OVER_FACT + ENGAGEMENT_SIGNALS_FORBIDDEN_IN_RANKING 4-tuple (views/dwell/clicks/replies SRR byte-verbatim) + LEARNED_SIGNALS_FORBIDDEN_IN_RANKING + RANKING_RULE_READS_VERIFIED_FIELDS_ONLY + HOOK_HOLDS_UNTIL_LOWER_CLASS_ELIGIBLE_OR_DEPS_CHANGE + NO_FLAP_ON_UNRELATED_UPDATES + HOLD_VALUES_RULED_R34 + HOOK_CHOICE_WRITES_CONTENT_RECEIPT + CONTENT_RECEIPT_CARRIES_SALIENCE_TRACE + SALIENCE_TRACE_FIELDS 4-tuple (candidate/class/eligibility/rule_version SRR byte-verbatim) + SURFACE_EXPOSES_TRACE_ON_DEMAND + HOOK_IS_ADVISORY + HOOK_NEVER_GATES_ACTION + HOOK_CLASS_NOT_INPUT_TO_PLATFORM_DECISION · Adds new pure-data-in scanner scan_for_engagement_signals_in_ranking(text) as grep-negative ban #3 anchor of the 7-category ban set (watches 7 patterns byte-verbatim) · Adds 1 NEW test module backend/tests/invariants/test_content_registry_v1_section_4_and_5.py with 10 property tests CON-12..CON-21 · each carries SO §2.5 verbatim-docstring quoting SRR statement byte-verbatim · each asserts Final[...] annotation + value binding · CON-18 test enforces scanner behavior byte-verbatim (clean input → empty · each of 7 watched patterns → hit tuple) · DELTA +10 MEASURED (5668 → 5678 monotonic-up per CCS2 both fields bumped together · new baseline_failures.json sha256 504cc47f was 854e9344 · new ORCH_BOOT.md sha256 c9f5c215 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · R-88 first-slice CON-1..11 module + tests continue verbatim GREEN · R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged · AUTHENTIC additive-only cycle: vocabulary extended in place (module docstring updated to R-88..R-89 range · SO §3.8 additive-only preserved · CON-1..CON-11 sections and existing scanners unchanged byte-verbatim below insertion points) → GREEN at drill_receipts/20260920T223536Z (21/21 pass 0.82s) → BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 0802eaab IDENTICAL run1+run2 both 5 baseline-fails (unchanged from R-88+ · all covered by total-coverage guard) 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r89_pre_commit_a_orch_boot_regen.py) · Canon anchors verbatim: owner standing-GO this-session (2026-09-20T~22:35Z) + owner Ruling 4 CP-CONTENT-REGISTRY-WAVE + owner Ruling 5 SRR-as-authority + SRR v5 rows 577-586 as authority (Ruling 5) + R-88 first-slice seal db90089d/79d5d38d/0cbfc23b (immediately-precedes · establishes vocabulary + module + first-slice test file this wave extends) + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance (Ruling-4 scope · standing-GO no per-slice check-in) + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master → Commit-C fixup → R-90 third slice CON-22..CON-31 + remaining grep-negative bans #4..#7 opens IMMEDIATELY per owner standing-GO"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    if f"head: {R89_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-89 Commit-B.")
    else:
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R89_CODE_REPO_BLOCK + text[m.end():]

    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {NEW_REGEN_REASON}", text, count=1, flags=re.MULTILINE)

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)


def main() -> None:
    regen_orch_boot_commit_c()
    print(f"heads_last_sealed.state_repo.head → {R89_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R89_CODE_HEAD}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
