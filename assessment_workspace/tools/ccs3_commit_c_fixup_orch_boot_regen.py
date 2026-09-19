#!/usr/bin/env python3
"""CP-CCS3-DAP-RECEIPT-FREEZE Commit-C fixup ORCH_BOOT regen.

Advances heads_last_sealed:
- state_repo.head: 0520469dbf5d836d253244ae820681ac4bc980cd (CCS2 Commit-B) → d48f6e1e049b35dd334d284be9bbfb2f67eed97f (CCS3 Commit-B)
- code_repo.head:  3fde289560830d5dffafe25c52080664625caaf8 (CCS2 Commit-A) → 379e45508bbfbc362f2b28d93065f527bc3864bd (CCS3 Commit-A)

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

OLD_STATE_HEAD = "0520469dbf5d836d253244ae820681ac4bc980cd"
NEW_STATE_HEAD = "d48f6e1e049b35dd334d284be9bbfb2f67eed97f"
OLD_CODE_HEAD = "3fde289560830d5dffafe25c52080664625caaf8"
NEW_CODE_HEAD = "379e45508bbfbc362f2b28d93065f527bc3864bd"

OLD_GEN_AT = "2026-09-19T22:58:00Z"
NEW_GEN_AT = "2026-09-19T23:10:00Z"
OLD_STATE_SEALED = "2026-09-19T22:50:00Z"
NEW_STATE_SEALED = "2026-09-19T23:10:00Z"
OLD_CODE_SEALED = "2026-09-19T22:40:00Z"
NEW_CODE_SEALED = "2026-09-19T23:00:00Z"

NEW_BASELINE_SHA = "8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1"
NEW_PASSED_FLOOR = 5527


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
    old_gen_prefix = "generator: main-agent Autopilot (CP-CCS3-DAP-RECEIPT-FREEZE pre-Commit-A"
    start = body.find(old_gen_prefix)
    assert start != -1, "generator prefix anchor not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1, "generator trailing ')' not found"
    end = end_paren + 1
    new_generator = (
        "generator: main-agent Autopilot (CP-CCS3-DAP-RECEIPT-FREEZE Commit-C fixup "
        "· state master · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim "
        "+ owner PROCEED ratification this-session verbatim (banked at CCS1 Commit-A banking section) "
        "· advances heads_last_sealed.state_repo.head "
        f"`{OLD_STATE_HEAD}` (CCS2 Commit-B) → new Commit-B `{NEW_STATE_HEAD}` (CCS3 Commit-B · "
        f"banks Commit-A `{NEW_CODE_HEAD}`) · advances heads_last_sealed.code_repo.head "
        f"`{OLD_CODE_HEAD}` (CCS2 Commit-A) → this-wave Commit-A `{NEW_CODE_HEAD}` "
        "(CCS3 Commit-A · 12 DAP receipt freeze invariants + baseline ratchet 5515 → 5527) "
        "· ratchet 5527 unchanged at Commit-C · CCS3 R-67 marker flips ⏳→✅ SEALED · "
        "frozen contract pin #3 of 3 achieved · CCS trio complete · absence findings #3/#6/#9/#10 "
        "CLOSED at CCS3 · MEM-R-053 CROWN BAN NOT triggered · owner FRONTENDS-GATE-IS-HALT-POINT "
        "+ owner PROCEED verbatim · Contract Closure Wave 3 FULLY SEALED · HALT at frontends gate "
        "opens next · staleness clock T-~12.4h remains armed)"
    )
    body = body[:start] + new_generator + body[end:]

    # 3. Update regeneration_reason.
    body = _replace_unique(
        body,
        "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-ccs3-dap-receipt-freeze-ratchet-only",
        "regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-ccs3-dap-receipt-freeze-advancing-state-head-and-code-head",
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
    old_state_seal_kind_prefix = '    seal_kind: "CP-CCS2-DAP-ENTITLEMENT-FREEZE · state Commit-B `0520469dbf5d836d253244ae820681ac4bc980cd`'
    start_ssk = body.find(old_state_seal_kind_prefix)
    assert start_ssk != -1, "state_repo seal_kind prefix anchor not found"
    end_quote_newline = body.find('"\n  code_repo:\n', start_ssk)
    assert end_quote_newline != -1, "state_repo seal_kind closing anchor not found"
    end_ssk = end_quote_newline + 1  # include closing '"'
    new_state_seal_kind = (
        '    seal_kind: "CP-CCS3-DAP-RECEIPT-FREEZE · '
        f'state Commit-B `{NEW_STATE_HEAD}` · banks Commit-A `{NEW_CODE_HEAD}` · '
        'Contract Closure Wave 3 · DAP receipt contract freeze (FINAL contract closure wave '
        'before frontends gate HALT) · frozen contract pin #3 of 3 achieved · CCS trio complete '
        '(bundle sha `81d3c0a5e8e54137d96873784dc3714c99f574c40f430996a66b0b17ada68a62` '
        'name-sorted concat canonical JSON bytes of 3 receipt-bundle shapes MeteredEvent + '
        'TrustReceiptV1 + OuterGateReceiptV1 · Canon 3 §9.3 canonicalization discipline · '
        'mirrors CCS1 + CCS2 bundle-sha patterns · closes B-frontends-Q1 frontends-gate '
        'contract-pin triple) · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z '
        'verbatim + owner PROCEED ratification this-session verbatim (both banked at CCS1 '
        'Commit-A banking section) · state-side landing includes STATE/DECISIONS.md CCS3 '
        'Commit-A banking section (12 invariants across 5 sub-wave clusters: W1 DAP-21 '
        'MeteredEvent freeze 3 tests + W2 reliable_time_source wiring 2 tests + W3 related '
        'receipts pinned + non-α gaps banked 4 tests + W4 integration seal 2 tests + W5 '
        'absence findings closure attestation 1 test · absence findings FINAL closure status '
        'post-CCS3: CLOSED across CCS1-3 #2/#3/#4/#5/#6/#9/#10 (7 findings) · BANKED to '
        'frontends-card wave #1/#8 (2 findings) · BANKED to future integration wave #7 · '
        'additional banked at CCS3 TrustReceiptV1_alpha_gap + OuterGateReceiptV1_alpha_gap '
        'owner ratification ceremony · three frozen contract pins table (#1 C.17 seam '
        '`a6107d46…` · #2 DAP entitlement `051f25df…` · #3 DAP receipt `81d3c0a5…`) · '
        'RED-first cycle receipts + pre-Commit-A double-green byte-identical stripped-sha '
        '`5eed33e9384288952e20202b9850fbf3851db239bd9aea4c476b9ec19c26347d` IDENTICAL across '
        'drill_receipts/20260919T225820Z_run1 + 20260919T230129Z_run2 · 5527 passed/1 '
        f'skipped/438 warnings · against FINAL baseline_failures.json sha256 `{NEW_BASELINE_SHA}` '
        '· both counts_at_baseline.passed AND invariants_enforced_when_baseline_guard_1.'
        'passed_floor bumped per CCS2 lesson · sealed contracts NOT edited · canon anchors '
        'Canon 5/3 §9.3/8 §W11 + SO §3.8/3.10-α/6.4/6.7 + M17-W1 milestone precedent + '
        'CCS1-C17 + CCS2 DAP entitlement bundle-sha precedents + B-frontends-Q1 + Doc-3 '
        'DAP-Spec dap_backend_spec_v1 verbatim + FRONTENDS-GATE-IS-HALT-POINT + PROCEED + '
        'owner ruling 2026-09-19T~17:54Z item (e) verbatim · Stop-conditions NOT triggered) + '
        'STATE/NEXT.md R-67 marker ⏳ IN-FLIGHT (flipped to ✅ SEALED at this Commit-C fixup) + '
        'notes/ORCH_BOOT.md R-6 boundary regen advancing state_head from prior CCS2 Commit-B '
        f'`{OLD_STATE_HEAD}` to this CCS3 Commit-B + code_head from prior CCS2 Commit-A '
        f'`{OLD_CODE_HEAD}` to this CCS3 Commit-A + audit copy re-sync byte-identical + '
        'STATE/PINS.md commissioning_record pointer refresh (state-side sensor drift · '
        'R-29-BOOT housekeeping-pickup) · additive-only per SO §3.8 · ratchet 5527 unchanged '
        'at Commit-C state files only Commit-A carried the +12"'
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

    # 7. Replace code_repo seal_kind narrative (the FIRST/top code_repo entry).
    old_code_seal_kind_prefix = '    seal_kind: "CP-CCS2-DAP-ENTITLEMENT-FREEZE · Commit-A `3fde289560830d5dffafe25c52080664625caaf8`'
    start_csk = body.find(old_code_seal_kind_prefix)
    assert start_csk != -1, "code_repo seal_kind prefix anchor not found"
    end_quote = body.find('"\n  code_repo:\n', start_csk)
    assert end_quote != -1, "code_repo seal_kind closing anchor not found"
    end_csk = end_quote + 1  # include closing '"'
    new_code_seal_kind = (
        '    seal_kind: "CP-CCS3-DAP-RECEIPT-FREEZE · '
        f'Commit-A `{NEW_CODE_HEAD}` · Contract Closure Wave 3 · DAP receipt contract freeze '
        '(FINAL contract closure wave before frontends gate HALT) · owner '
        'FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim + owner PROCEED '
        'ratification this-session verbatim + owner ruling 2026-09-19T~17:54Z item (e) verbatim '
        '· new backend/tests/invariants/test_ccs3_dap_receipt_freeze.py (~465 lines · 12 '
        'invariants organised in 4 sub-wave clusters + banking cluster: W1.1 MeteredEvent '
        'schema pin `b354818c…` (DAP-21 metering rail · sealed contracts.dap.MeteredEvent · '
        'absence finding #3 CLOSED via naming resolution: class exists as MeteredEvent not '
        'DAP21MeteredEvent_v0) + W1.2 MeteredEvent carries all 7 DAP-Spec-verbatim fields '
        '(operation_type + accessed_scope + quantity + quantity_unit + terms_id + party_id + '
        'timestamp_iso + R-C2 au_3b_defensible) + W1.3 MeteredEvent SO §3.10-α (frozen=True + '
        'extra=forbid) + W2.1 reliable_time_source module importable from sealed path '
        '(services.reliable_time_source.clock surface presence · ReliableClock + TimeAnchor + '
        'au_3b_defensible_now · absence finding #6 CLOSED) + W2.2 au_3b_defensible_now '
        'callable returns dict with wall_time_iso + au_3b_defensible keys (sealed surface '
        'adherence) + W3.1 TrustReceiptV1 schema pin `d4645512…` (LLM-provenance rail · '
        'sibling · absence finding #9 CLOSED via relationship documentation + pin) + W3.2 '
        'OuterGateReceiptV1 schema pin `196e56f0…` (outer-gate transform-receipt rail · '
        'sibling · absence finding #10 CLOSED via relationship documentation + pin) + W3.3 '
        'TrustReceiptV1 SO §3.10-α NON-COMPLIANCE finding (frozen=False · BANKED for owner '
        'ratification · SO §3.8 forbids editing at this wave) + W3.4 OuterGateReceiptV1 SO '
        '§3.10-α NON-COMPLIANCE finding (frozen=None · BANKED for owner ratification) + W4.1 '
        'DAP receipt bundle sha `81d3c0a5e8e54137d96873784dc3714c99f574c40f430996a66b0b17ada68a62` '
        'FROZEN CONTRACT PIN #3 OF 3 · name-sorted concat canonical JSON bytes · Canon 3 §9.3 '
        'canonicalization discipline · mirrors CCS1 + CCS2 bundle-sha patterns · closes '
        'B-frontends-Q1 frontends-gate contract-pin triple + W4.2 bundle binds all 3 named '
        'shapes (vocabulary containment · exactly 3 receipt shapes: MeteredEvent + '
        'OuterGateReceiptV1 + TrustReceiptV1) + W5 Banking test attests CCS3 closure '
        'disposition #3 CLOSED at W1 · #6 CLOSED at W2 · #7 BANKED to future integration '
        'wave · #9 CLOSED at W3 · #10 CLOSED at W3 · TrustReceiptV1_alpha_gap BANKED · '
        'OuterGateReceiptV1_alpha_gap BANKED) · zero new implementation module (all 3 DAP '
        'receipt shapes already sealed at prior CP · consumed via identity import from '
        'contracts.dap + contracts.trust_receipt_v1 + contracts.outer_gate_receipt_v1 · '
        'reliable_time_source consumed via identity import from services.reliable_time_source.clock) · '
        f'baseline_failures.json ratchet 5515 → {NEW_PASSED_FLOOR} (+12 exactly · zero wizard '
        'trigger · not a contracts/*.py file · zero flip zero regression zero refactor '
        'additive-only · both counts_at_baseline.passed AND '
        'invariants_enforced_when_baseline_guard_1.passed_floor bumped per CCS2 lesson) · '
        'AUTHENTIC RED-first: RED at drill_receipts/20260919T225647Z (2 fail right-reason: '
        '(1) bundle sha computed `81d3c0a5…` != corrupted-all-zeros frozen constant · (2) '
        'au_3b_defensible_now stamp key assertion too narrow · fixed to match sealed surface '
        '(wall_time_iso + au_3b_defensible) · 10/12 pass immediately on clean codebase state) '
        '→ GREEN at drill_receipts/20260919T225712Z (12/12 pass · 0.83s) · pre-Commit-A '
        'double-green byte-identical BASELINE_GUARD=1 stripped-sha256 '
        '`5eed33e9384288952e20202b9850fbf3851db239bd9aea4c476b9ec19c26347d` IDENTICAL across '
        'drill_receipts/20260919T225820Z_run1 + 20260919T230129Z_run2 (both 11124 bytes raw · '
        '11103 bytes stripped · 5527 passed/1 skipped/438 warnings · ~180s each) against final '
        f'baseline_failures.json sha256 `{NEW_BASELINE_SHA}` · additive-only per SO §3.8 · '
        'sealed contracts/dap.py + contracts/trust_receipt_v1.py + contracts/outer_gate_receipt_v1.py '
        '+ services/reliable_time_source/clock.py all NOT edited (all consumed via identity '
        'import) · sealed M17-W1..W6 + M14 + M11 + M16 + W-M2-SW7 + W-7bB + c13_scope + '
        'memory-compaction-v1 (4 sub-waves) + CCS1-C17-seam-bundle + CCS2-DAP-entitlement '
        'modules all NOT edited · Canon anchors: Canon 5 · seam-boundary discipline + Canon '
        '3 §9.3 · append-only writer + Canon 8 §W11 · one-task-one-identity + SO §3.8 + SO '
        '§3.10-α · closed-schema discipline (only MeteredEvent fully compliant · '
        'TrustReceiptV1 + OuterGateReceiptV1 non-α gaps banked) + SO §6.4 NOTHING-BEYOND + '
        'SO §6.7 sequence CCS1 → CCS2 → CCS3 → HALT before frontends (FINAL contract closure '
        'wave completed · frontends gate HALT point next) + M17-W1 milestone precedent + '
        'CCS1-C17 bundle-sha `a6107d46…` precedent + CCS2 DAP entitlement bundle-sha '
        '`051f25df…` precedent + B-frontends-Q1 + Doc-3 DAP-Spec dap_backend_spec_v1 '
        'verbatim (DAP-21 metered event 7-field surface + reliable time source requirement + '
        'R-C2 au_3b_defensible) + owner FRONTENDS-GATE-IS-HALT-POINT + owner PROCEED + '
        'owner ruling 2026-09-19T~17:54Z item (e) verbatim · Stop-conditions NOT triggered · '
        '§6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next '
        'HALT at frontends gate for owner dispatch to specialists"'
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
    assert parsed["ratchet"]["passed_floor"] == NEW_PASSED_FLOOR
    assert parsed["ratchet"]["baseline_failures_sha256"] == NEW_BASELINE_SHA

    # Verify heads present as raw substrings (stacked-duplicates YAML quirk safe).
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
