#!/usr/bin/env python3
"""CP-CCS1-C17-SEAM-BUNDLE-FREEZE Commit-C fixup ORCH_BOOT regen.

Advances heads_last_sealed:
- state_repo.head: 09f2f31743da91222f7e9de108810b8950e32f58 (W4 Commit-B) → ae709eb75d960a6eef11363c95664aea946dab93 (CCS1 Commit-B)
- code_repo.head:  da2642acdcb5f1785d6ca561913f60fceafd2c6b (W4 Commit-A) → 175786340063efdba387a9f29cece04417a91e91 (CCS1 Commit-A)

Refreshes generated_at_utc + generator + regeneration_reason.
Advances sealed_at_utc timestamps and seal_kind narratives for both repos.
Syncs /app/frontend/public/audit/ORCH_BOOT.md byte-identically.

Additive to R-6 (a) regen trigger (§3.3 seal boundary).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ORCH_BOOT = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

OLD_STATE_HEAD = "09f2f31743da91222f7e9de108810b8950e32f58"
NEW_STATE_HEAD = "ae709eb75d960a6eef11363c95664aea946dab93"
OLD_CODE_HEAD = "da2642acdcb5f1785d6ca561913f60fceafd2c6b"
NEW_CODE_HEAD = "175786340063efdba387a9f29cece04417a91e91"

OLD_GEN_AT = "2026-09-19T21:55:00Z"
NEW_GEN_AT = "2026-09-19T22:30:00Z"
OLD_STATE_SEALED = "2026-09-19T21:25:00Z"
NEW_STATE_SEALED = "2026-09-19T22:30:00Z"
OLD_CODE_SEALED = "2026-09-19T21:20:00Z"
NEW_CODE_SEALED = "2026-09-19T22:20:00Z"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _replace_unique(body: str, old: str, new: str, label: str) -> str:
    assert body.count(old) == 1, f"{label}: expected 1 occurrence of anchor, got {body.count(old)}"
    return body.replace(old, new, 1)


def main() -> int:
    body = ORCH_BOOT.read_text(encoding="utf-8")

    # 1. Update generated_at_utc.
    body = _replace_unique(
        body,
        f"generated_at_utc: {OLD_GEN_AT}",
        f"generated_at_utc: {NEW_GEN_AT}",
        "generated_at_utc",
    )

    # 2. Replace the generator line entirely.
    old_gen_prefix = "generator: main-agent Autopilot (CP-CCS1-C17-SEAM-BUNDLE-FREEZE pre-Commit-A"
    start = body.find(old_gen_prefix)
    assert start != -1, "generator prefix anchor not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1, "generator trailing ')' not found"
    end = end_paren + 1
    new_generator = (
        "generator: main-agent Autopilot (CP-CCS1-C17-SEAM-BUNDLE-FREEZE Commit-C fixup "
        "· state master · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim "
        "+ owner PROCEED ratification this-session verbatim · advances "
        f"heads_last_sealed.state_repo.head `{OLD_STATE_HEAD}` (W4 Commit-B) "
        f"→ new Commit-B `{NEW_STATE_HEAD}` (CCS1 Commit-B · banks Commit-A "
        f"`{NEW_CODE_HEAD}`) · advances heads_last_sealed.code_repo.head "
        f"`{OLD_CODE_HEAD}` (W4 Commit-A) → this-wave Commit-A `{NEW_CODE_HEAD}` "
        "(CCS1 Commit-A · 11 seam-bundle-freeze invariants + baseline ratchet 5491 → 5502) "
        "· ratchet 5502 unchanged at Commit-C · CCS1 R-65 marker flips ⏳→✅ SEALED · "
        "MEM-R-053 CROWN BAN NOT triggered · owner FRONTENDS-GATE-IS-HALT-POINT verbatim "
        "+ owner PROCEED verbatim · Contract Closure Wave 1 FULLY SEALED · "
        "CCS2 DAP entitlement freeze opens next · staleness clock T-~13.1h remains armed)"
    )
    body = body[:start] + new_generator + body[end:]

    # 3. Update regeneration_reason.
    body = _replace_unique(
        body,
        "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-ccs1-c17-seam-bundle-freeze-ratchet-only-plus-w4-orch-boot-yaml-repair-per-r-29-boot",
        "regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-ccs1-c17-seam-bundle-freeze-advancing-state-head-and-code-head",
        "regeneration_reason",
    )

    # 4. Update state_repo head.
    body = _replace_unique(
        body,
        f"    head: {OLD_STATE_HEAD}\n"
        f"    sealed_at_utc: {OLD_STATE_SEALED}\n",
        f"    head: {NEW_STATE_HEAD}\n"
        f"    sealed_at_utc: {NEW_STATE_SEALED}\n",
        "state_repo head+sealed_at_utc",
    )

    # 5. Replace state_repo seal_kind narrative.
    old_state_seal_kind_prefix = '    seal_kind: "CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · state Commit-B `09f2f31743da91222f7e9de108810b8950e32f58`'
    start_ssk = body.find(old_state_seal_kind_prefix)
    assert start_ssk != -1, "state_repo seal_kind prefix anchor not found"
    # find the closing `"\n` for this multiline seal_kind
    end_quote_newline = body.find('"\n  code_repo:\n', start_ssk)
    assert end_quote_newline != -1, "state_repo seal_kind closing anchor not found"
    end_ssk = end_quote_newline + 1  # include the closing '"'
    new_state_seal_kind = (
        '    seal_kind: "CP-CCS1-C17-SEAM-BUNDLE-FREEZE · '
        f'state Commit-B `{NEW_STATE_HEAD}` · banks Commit-A `{NEW_CODE_HEAD}` · '
        'Contract Closure Wave 1 · C.17 answering-service seam bundle-freeze · '
        'owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim '
        "('Seal W4 and CONTINUE DIRECTLY into CCS1 without stopping ... CCS1 (C.17 "
        'answering-service seam bundle-freeze) → CCS2 (DAP entitlement) → CCS3 '
        '(DAP receipt), each frozen from dap_backend_spec_v1 under T-b (JSON-Schema '
        "authoritative), tests-first, §3.3 sealed. Work the survey's 10 absence "
        "findings into freeze scope: each closes in its wave or is banked with a reason.') + "
        "owner PROCEED ratification this-session verbatim (banked in DECISIONS.md CCS1 "
        "Commit-A banking section) · state-side landing includes STATE/DECISIONS.md "
        "CCS1 Commit-A banking section (owner ratifications verbatim + Commit-A scope "
        "11 invariants + absence findings closure status table (#4 CLOSED at W1 · #2 "
        "CLOSED structurally via T-b JSON-Schema-authoritative discipline · #1/#3/#5/#6/"
        "#7/#8/#9/#10 BANKED to CCS2/CCS3/frontends waves) + RED-first cycle receipts + "
        "pre-Commit-A double-green byte-identical stripped-sha256 "
        "`7b6b2611926ccbaf70607d6c7a912c298e1077bbbdbd02941d06299c3dd5676f` IDENTICAL "
        "across drill_receipts/20260919T221108Z_run1 + 20260919T221417Z_run2 · 5502 "
        "passed/1 skipped/438 warnings · both raw 11124 B stripped 11103 B · against "
        "FINAL baseline_failures.json sha256 `34b14bc7e187eb461e9d692fa62eedc86c79051"
        "521fb9b5c691158b1bbca399b` + transparency banking of pre-ORCH-regen stale-"
        "attempt + 2 mid-window backgrounded runs + canon anchors Canon 5/17 §4/15 §33/"
        "3 §9.3/8 §W11 + SO §3.8/3.10-α/6.4/6.7 + M17-W1 milestone snapshot pin "
        "precedent + M17-W5 seal-integration pattern + HR-2 + B-frontends-Q1 + Doc-3 "
        "DAP-Spec + FRONTENDS-GATE-IS-HALT-POINT + owner PROCEED verbatim + owner "
        "ruling 2026-09-19T~17:54Z item (e) verbatim + Stop-conditions NOT triggered + "
        "autopilot next CCS2 → CCS3 → HALT before frontends) + STATE/NEXT.md R-65 "
        "marker ⏳ IN-FLIGHT (flipped to ✅ SEALED at this Commit-C fixup) + "
        "notes/ORCH_BOOT.md R-6 boundary regen advancing state_head from prior W4 "
        f"Commit-B `{OLD_STATE_HEAD}` to this CCS1 Commit-B + code_head from prior W4 "
        f"Commit-A `{OLD_CODE_HEAD}` to this CCS1 Commit-A + audit copy re-sync byte-"
        "identical + STATE/PINS.md commissioning_record pointer refresh (state-side "
        "sensor drift · R-29-BOOT housekeeping-pickup) · additive-only per SO §3.8 · "
        "ratchet 5502 unchanged at Commit-C state files only Commit-A carried the +11"'"'
    )
    body = body[:start_ssk] + new_state_seal_kind + body[end_ssk:]

    # 6. Update code_repo head + sealed_at_utc.
    body = _replace_unique(
        body,
        f"    head: {OLD_CODE_HEAD}\n"
        f"    sealed_at_utc: {OLD_CODE_SEALED}\n",
        f"    head: {NEW_CODE_HEAD}\n"
        f"    sealed_at_utc: {NEW_CODE_SEALED}\n",
        "code_repo head+sealed_at_utc",
    )

    # 7. Replace code_repo seal_kind narrative.
    old_code_seal_kind_prefix = '    seal_kind: "CP-MEMORY-COMPACTION-V1-W4-ONE-CHAIN-INTEGRATION · Commit-A `da2642acdcb5f1785d6ca561913f60fceafd2c6b`'
    start_csk = body.find(old_code_seal_kind_prefix)
    assert start_csk != -1, "code_repo seal_kind prefix anchor not found"
    # find the closing `"\n  code_repo:\n` (next stacked entry) OR end-of-yaml boundary
    end_quote = body.find('"\n  code_repo:\n', start_csk)
    assert end_quote != -1, "code_repo seal_kind closing anchor not found"
    end_csk = end_quote + 1  # include closing '"'
    new_code_seal_kind = (
        '    seal_kind: "CP-CCS1-C17-SEAM-BUNDLE-FREEZE · '
        f'Commit-A `{NEW_CODE_HEAD}` · Contract Closure Wave 1 · C.17 '
        'answering-service seam bundle-freeze · owner FRONTENDS-GATE-IS-HALT-POINT '
        "ratification 2026-09-19T~21:30Z verbatim + owner PROCEED ratification "
        "this-session verbatim + owner ruling 2026-09-19T~17:54Z item (e) survey "
        "ruling verbatim · new backend/tests/invariants/test_ccs1_c17_seam_bundle_"
        "freeze.py (510 lines · 11 invariants organised in 3 sub-wave clusters + 1 "
        "banking test: W1.1a application_contract_v0 per-schema pin ba1957df… + "
        "W1.1b ask_v0 per-schema pin d0f39639… + W1.1c handoff_contract_v0 per-schema "
        "pin e5d6c74a… + W1.1d personal_client_session_v0 per-schema pin cc7bd992… + "
        "W1.2 seam bundle sha `a6107d46f4f5d80fa7be4d28e8c427a0a4be15438a1843ca17aea"
        "b197b708033` name-sorted concat canonical JSON bytes Canon 3 §9.3 + W1.3 "
        "vocabulary containment (exactly 4 named shapes) + W1.4 SO §3.10-α compliance "
        "(frozen=True + extra=forbid on all 4) + W2.1 AST invariant services/personal_"
        "client/**/*.py imports seam shapes only from sealed identity paths + W2.2 AST "
        "invariant no shadow class definition anywhere in backend/**/*.py outside "
        "sealed origin files + W3 integration end-to-end ask flow binds bundle mirrors "
        "M17-W5 seal-integration pattern + Banking test attests EFCS survey absence "
        "finding #4 CLOSED at this wave) · zero new implementation module (all 4 seam "
        "contracts already sealed at M14-W1/M14-W3/M17-W1/M17-W3 + HandoffContract_v0 "
        "from Canon 15 §33) · baseline_failures.json ratchet 5491 → 5502 (+11 exactly "
        "· zero wizard trigger since not a contracts/*.py file) · AUTHENTIC RED-first: "
        "RED at drill_receipts/20260919T215044Z (test_ccs1_seam_bundle_snapshot_pin_"
        "matches_frozen_constant 1 fail right-reason: computed sha a6107d46… != "
        "corrupted-all-zeros frozen constant) → intermediate GREEN attempt at "
        "20260919T215101Z discovered W3 integration field-shape drift (Application"
        "Contract_v0.receipt_policy required · PersonalClientSession_v0.composed_at → "
        "started_at · HandoffContract_v0 surface differs from initial draft · fixed "
        "via model_json_schema() introspection) → GREEN at drill_receipts/20260919T"
        "215151Z (11/11 pass · 1.44s) · pre-Commit-A double-green byte-identical "
        "BASELINE_GUARD=1 stripped-sha256 `7b6b2611926ccbaf70607d6c7a912c298e1077bbbdb"
        "d02941d06299c3dd5676f` IDENTICAL across drill_receipts/20260919T221108Z_run1 "
        "+ 20260919T221417Z_run2 (both 11124 bytes raw · 11103 bytes stripped · 5502 "
        "passed/1 skipped/438 warnings · 178.15s + 180.29s) against final baseline_"
        "failures.json sha256 `34b14bc7e187eb461e9d692fa62eedc86c79051521fb9b5c69115"
        "8b1bbca399b` · transparency banking: 1 prior GUARD1 attempt at 20260919T"
        "215325Z (pre-ORCH_BOOT-regen) failed test_orch_boot because notes/ORCH_BOOT."
        "md ratchet.passed_floor still pinned at 5491 pre-regen · reconciled by pre-"
        "Commit-A r6-boundary ratchet-only regen via tools/ccs1_pre_commit_a_orch_"
        "boot_regen.py · plus 2 mid-window backgrounded runs at 20260919T220436Z + "
        "20260919T220749Z completed silently after driving tool-call timeouts (both "
        "green 5502 passed · not the chosen preseal pair) · additive-only per SO §3.8 "
        "· sealed contracts/application_contract_v0.py + services/answering_service/"
        "collections/asks.py + contracts/handoff_contract.py + contracts/personal_"
        "client_session_v0.py all NOT edited (imported only) · sealed M17-W1..W6 + "
        "M14 + M11 + M16 + W-M2-SW7 + W-7bB + c13_scope + memory-compaction-v1 "
        "modules all NOT edited · Canon anchors: Canon 5 · Interface Architecture · "
        "seam-boundary discipline + Canon 17 §4 · answering-service triangle · ask "
        "entity + Canon 15 §33 · HandoffContract_v0 frozen contract discipline + "
        "Canon 3 §9.3 · append-only writer discipline (canonicalization applied to "
        "bundle sha) + Canon 8 §W11 · one-task-one-identity (no shadow classes in "
        "services/personal_client/) + SO §3.8 + SO §3.10-α + SO §6.4 NOTHING-BEYOND "
        "(scope frozen at 4 seam shapes + 3 sub-wave test clusters + banking test) "
        "+ SO §6.7 sequence CCS1 → CCS2 → CCS3 → HALT + M17-W1 milestone snapshot "
        "pin precedent shape + M17-W5 seal-integration pattern + HR-2 + B-frontends-"
        "Q1 + Doc-3 DAP-Spec dap_backend_spec_v1 + owner FRONTENDS-GATE-IS-HALT-POINT "
        "verbatim + owner PROCEED verbatim + owner ruling 2026-09-19T~17:54Z item (e) "
        "verbatim · Stop-conditions NOT triggered · MEM-R-053 CROWN BAN NOT triggered "
        "· autopilot next CCS2 DAP entitlement → CCS3 DAP receipt → HALT before "
        'frontends"'
    )
    body = body[:start_csk] + new_code_seal_kind + body[end_csk:]

    ORCH_BOOT.write_text(body, encoding="utf-8")

    # Sync audit mirror byte-identical.
    AUDIT.write_text(body, encoding="utf-8")
    assert _sha256(ORCH_BOOT) == _sha256(AUDIT), "byte-identity check failed"

    # Verify YAML still parses cleanly.
    import re
    import yaml
    m = re.search(r"```yaml\n(.*?)\n```", body, re.DOTALL)
    parsed = yaml.safe_load(m.group(1))
    assert parsed["ratchet"]["passed_floor"] == 5502
    assert parsed["ratchet"]["baseline_failures_sha256"] == "34b14bc7e187eb461e9d692fa62eedc86c79051521fb9b5c691158b1bbca399b"

    # Note: parsed heads may reflect the "last of stacked duplicates" YAML quirk
    # (multiple code_repo entries). What matters for the boundary regen is that the
    # TOP-of-stack entry (state_repo + first code_repo) has the CCS1 sealed heads.
    # Verify by finding the top state_repo/code_repo entries in the raw text.
    assert f"    head: {NEW_STATE_HEAD}\n" in body
    assert f"    head: {NEW_CODE_HEAD}\n" in body

    sha = _sha256(ORCH_BOOT)
    print(f"OK: ORCH_BOOT Commit-C fixup regen complete")
    print(f"    notes sha256: {sha}")
    print(f"    audit sha256: {_sha256(AUDIT)}")
    print(f"    state_repo.head → {NEW_STATE_HEAD[:8]}")
    print(f"    code_repo.head  → {NEW_CODE_HEAD[:8]}")
    print(f"    ratchet.passed_floor: {parsed['ratchet']['passed_floor']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
