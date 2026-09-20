"""R-88+ Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Precedent shape (mirrors tools/r87_commit_c_fixup_orch_boot_regen.py):
- state_repo (heads_last_sealed.state_repo): replaced with R-88+ Commit-B
  `79d5d38d…` entry.
- code_repo history: fresh entry for R-88+ Commit-A `db90089d…` INSERTED at
  the top of the history (immediately after state_repo), preserving all
  prior code_repo entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-88+ Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive: heads_last_sealed history is append-only for code_repo entries;
state_repo is a single current-head slot that advances at each Commit-C.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R88_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R88_STATE_HEAD = "79d5d38dd5257abb94d1ea8006fd734252e09758"
R88_CODE_HEAD = "db90089d28bd3b4659138150e5b1049f5616cf36"
R88_STATE_SEALED_AT = "2026-09-20T22:25:59Z"
R88_CODE_SEALED_AT = "2026-09-20T22:21:34Z"
NEW_UTC = "2026-09-20T22:30:00Z"
NEW_REGEN_REASON = (
    "r88-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-79d5d38d-"
    "cp-content-registry-wave-first-slice-plus-cp10-harness-scheduled-closure-"
    "annotation-plus-owner-a-extended-umbrella-commit-b-plus-new-code-repo-history-"
    "entry-for-r88-commit-a-db90089d"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R88_STATE_HEAD}
    sealed_at_utc: {R88_STATE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE first slice CON-1..CON-11 + CP10 harness scheduled-closure annotation guard + owner A-extended umbrella (2 v8 cascade artifacts) + total-coverage assertion · state Commit-B `{R88_STATE_HEAD}` · banks Commit-A `{R88_CODE_HEAD}` on programme/track-a · WAVE R-88 · Ruling 4 first slice + owner D-ruling this-session verbatim (2026-09-20T~21:55Z applying Ruling 1 R-86 annotation pattern to a fourth artifact of the dc48d5313 divergence · CP10 harness receipt vacuous-pass) + owner A-ruling this-session verbatim (2026-09-20T~22:05Z extending the umbrella to artifacts 5 and 6 · both v8 substitution rule tests that flipped RED when the necessary CP10 staleness cure refreshed the harness receipt · FLAGGED FOR OWNER RATIFICATION as a single OWNER-RATIFICATION-PENDING block) · Both stop-conditions triggered this-wave and resolved via explicit owner rulings before proceeding · Adds 3 new test modules (CON-1..CON-11 + CP10 annotation guard + total-coverage) + 1 new backend package + additive top-level baseline_failures.json field known_r91_closure_scheduled_receipt_drift_annotations disjoint from R-86 known_runtime_drift_annotations + 2 v8 nodeids into baseline_failures[] + counts_at_baseline.failed 3→5 · DELTA +17 MEASURED (5651 → 5668 monotonic-up per CCS2 lesson both fields bumped together · CCS2-aligned across counts.passed / passed_floor / ratchet_history[-1].passed) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 49738669457bf56a10ff8c1a860d835d4d7220946fbdca68e872d3f7bae19f8c IDENTICAL across drill_receipts/20260920T220939Z_run1 (182.03s · 5668 passed) + 20260920T221421Z_run2 (181.39s · 5668 passed) both 5 baseline-fails 1 skip 438 warnings against post-bump baseline_failures.json sha256 854e9344895e486f3d0e853e7fd4ed1314f10fec4238be0b72de691aa5ff178e · STATE/OBJECTIVES/CP_APP_JS_UNIFY.md additive extension per D-ruling verbatim with new MUST DO #6 CP10 restoration + new EXIT block byte-verbatim closure_card_line + 6 new EXIT nodeids + 4 new ANCHORs + updated ratified_at_utc/ratified_by + recomputed card_sha256 667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61 per SO §6.2 hash-pin discipline verified · Card milestone_status remains SCHEDULED (not-open-ended) · slot R-91 · closure trigger for 3 pod_shell mirror-drift + 2 v8 cascade + CP10 harness receipt vacuous-pass restoration · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 e9d403aa9db3dcd99651cfa3844e89dd4ca502b289373d172ed42ac86bd22104) · Files (15 tracked at Commit-B): STATE/DECISIONS.md this-append (full seal report + both rulings verbatim + OWNER-RATIFICATION-PENDING block) + STATE/NEXT.md this-append + STATE/PINS.md this-append + STATE/OBJECTIVES/CP_APP_JS_UNIFY.md this-additive-extension + notes/ORCH_BOOT.md this-ratchet-regen + tools/r88_pre_commit_a_orch_boot_regen.py NEW + phase0/spec_hunt_receipts/20260920T214836Z_r88_first_slice_STOP_harness_subject_retired.md NEW + phase0/spec_hunt_receipts/20260920T220000Z_r88_first_slice_STOP2_two_additional_same_divergence_artifacts.md NEW + 7 drill receipts this-wave · Canon anchors verbatim: owner D-ruling this-session + owner A-ruling this-session + Ruling 1 R-86 + Ruling 4 CP-CONTENT-REGISTRY-WAVE + Ruling 5 SRR-as-authority + culpable commit dc48d5313 on main + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + M16-W3 + CCS2 · Stop-conditions #1/#2 triggered and RESOLVED this-wave via explicit owner rulings · SO §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · Historical note flagged as-found per D-ruling: specialist claim 'migrated into pages/os/OSPrototype.jsx' vs zero-match grep in /app/frontend/src → R-91 resolves either interpretation · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R88_STATE_HEAD} + inserts code_repo entry for R88 Commit-A {R88_CODE_HEAD} · R-88+ first-slice marker already banked SEALED at Commit-B in STATE/NEXT.md) → R-89 second slice (CON-12..CON-21) at owner next go"
"""

NEW_R88_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R88_CODE_HEAD}
    sealed_at_utc: {R88_CODE_SEALED_AT}
    seal_kind: "CP-CONTENT-REGISTRY-WAVE first slice CON-1..CON-11 + CP10 harness scheduled-closure annotation guard + owner A-extended umbrella (2 v8 cascade artifacts) + total-coverage assertion · Commit-A `{R88_CODE_HEAD}` · code programme/track-a · WAVE R-88 · Ruling 4 first slice + owner D-ruling this-session verbatim (2026-09-20T~21:55Z applying Ruling 1 R-86 annotation pattern to a fourth artifact of the dc48d5313 divergence) + owner A-ruling this-session verbatim (2026-09-20T~22:05Z extending the umbrella to artifacts 5 and 6 · FLAGGED FOR OWNER RATIFICATION) · 1 NEW backend package services/content_registry/__init__.py (SO §2.5 verbatim-docstring package marker) + 1 NEW backend module services/content_registry/content_registry_vocabulary.py (Content Registry Spec v1 §2 Three Classes + §3 The Registry Final[...] constants: FIXED_CLASS/TEMPLATED_CLASS/GENERATED_CLASS + FIXED_RENDER_VERBATIM_REQUIRED + TEMPLATED_DEPENDENCIES_ONLY + TEMPLATED_HONEST_GAP_REQUIRED + GENERATED_CEILING_INFERENCE_ADVISORY_NEVER_FACT + R32_GENERATED_SURFACE_WHITELIST 3-tuple + CONTENT_ENTRY_MANDATORY_FIELDS 7-tuple + SLOT_ENTRY_MANDATORY_FIELDS 5-tuple + REGISTRY_READ_ONLY_EXCEPT_CEREMONY + OBJECTIVE_MANDATORY + OBJECTIVE_MUST_BE_ONE_SENTENCE) · 3 NEW test modules (11 CON-1..CON-11 property tests + 6 CP10 annotation guard property tests + 2 total-coverage property tests · owner A-ruling guard #1 verbatim: 'makes unannotated baseline entry structurally RED and closes the class of this stop-condition permanently') · Adds new top-level baseline_failures.json field known_r91_closure_scheduled_receipt_drift_annotations disjoint from R-86 known_runtime_drift_annotations (preserves R-86 Property-4 set-equality invariant · verified GREEN at guard #2) with 3 keys (CP10 vacuous-pass + v8 rule-binding-fail + v8 slot1-marker-missing) all 8-field shape · baseline_failures[] extended by 2 v8 nodeids in canonical sorted order · counts_at_baseline.failed 3→5 · DELTA +17 MEASURED (5651 → 5668 monotonic-up per CCS2 both fields bumped together · +11 CON pass +6 R-88 guard pass +2 total-coverage pass -2 v8 pass-to-fail flip · new baseline_failures.json sha256 854e9344895e486f3d0e853e7fd4ed1314f10fec4238be0b72de691aa5ff178e was c0af7a314841e78af4507149539e3f59892ace811bf15a5afce527878b65bbb7 · new ORCH_BOOT.md sha256 e9d403aa9db3dcd99651cfa3844e89dd4ca502b289373d172ed42ac86bd22104 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (2 new backend package files + 3 new test modules + additive top-level field + additive baseline extension + additive counts.failed 3→5 + additive ratchet bump · Card additive extension already landed at master pre-Commit-A · ORCH_BOOT ratchet-regen already landed pre-Commit-A · Commit-B state master lands seal-report banking + owner rulings verbatim + OWNER-RATIFICATION-PENDING block) · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · sealed BlockedKind enum + suspension_notices.py + party_halted_kind.py + party_halt_billing.py NOT edited · AUTHENTIC RED-first cycle: RED at drill_receipts/20260920T214119Z_r88_pre_cure_two_reds_reproduction.log (KeyError:passed + age 12.36h right-reason) → cure-#1 schema-fix per owner steer + cure-#2 existing-precedent-ceremony re-run harness → STOP-CONDITION #1 (CP10 vacuous per_rule) → owner D-ruling verbatim → author annotation guard tests (RED-first at 20260920T215529Z 5/6 fail right-reason annotation-missing → GREEN at 20260920T215709Z 6/6 pass 0.75s) → BASELINE_GUARD=1 sweep 1 5666 pass 6 fail reveals cascade → STOP-CONDITION #2 (2 v8 tests flipped) → owner A-ruling verbatim → extend umbrella + total-coverage guard → pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 49738669457bf56a10ff8c1a860d835d4d7220946fbdca68e872d3f7bae19f8c IDENTICAL across drill_receipts/20260920T220939Z_run1 (182.03s · 5668 passed) + 20260920T221421Z_run2 (181.39s · 5668 passed) both 5 baseline-fails (3 mirror-drift + 2 v8 cascade all annotated · covered by exactly one annotation field under total-coverage guard) 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r88_pre_commit_a_orch_boot_regen.py + notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md both sha256 e9d403aa) · pre-Commit-A STATE/OBJECTIVES/CP_APP_JS_UNIFY.md additive extension per D-ruling verbatim (ADD AN EXIT CRITERION LINE) · Canon anchors verbatim: owner D-ruling this-session (2026-09-20T~21:55Z) + owner A-ruling this-session (2026-09-20T~22:05Z) + owner Ruling 1 (R-86 · 2026-09-20T~19:00Z · Coexistence with a closure date is discipline; without one it's drift with a ruling attached) + owner Ruling 4 CP-CONTENT-REGISTRY-WAVE + owner Ruling 5 SRR-as-authority + culpable commit dc48d53131be2a36b36aabab83048cbbb779cfa2 on `main` at 2026-09-20T14:21:07Z (feat(frontend): DAP Portal full build + OS Prototype v2 React surfaces) + Master Requirements Registry v5 SRR sheet rows 566-576 as authority (Ruling 5) + CP-BLOCKED-VOCABULARY-CORRECTION seal 200c2c637/b4526572/9823a520 (R-87 immediately-precedes · establishes Final[...]-constants vocabulary-registration pattern this wave inherits) + CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE seal 2eca0e58/1525ddd0/e40047f4 (R-86 · schedules R-91 closure wave + annotation pattern precedent) + CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal 11afc4f/0cd4c9b8 (R-85) + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM 1250c39a + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + M16-W3 corrected order + CCS2 lesson · Stop-conditions #1/#2 triggered this-wave and RESOLVED via owner D-ruling and A-ruling verbatim (OWNER-RATIFICATION-PENDING banked at Commit-B) · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · Historical note flagged as-found: specialist claim 'migrated into pages/os/OSPrototype.jsx' vs zero-match grep · R-91 resolves either way · autopilot next Commit-B state master → Commit-C fixup → R-89 second slice (CON-12..CON-21) at owner next go"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    # Idempotency guard: if state_repo.head already equals R88_STATE_HEAD, skip.
    if f"head: {R88_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-88 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R88_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R88_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R88_CODE_HEAD}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
