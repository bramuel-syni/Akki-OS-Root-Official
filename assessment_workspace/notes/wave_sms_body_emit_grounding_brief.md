# W-SMS-Body-Emit · grounding brief

**Authored:** 2026-09-06T~15:XXZ (post-W-Multi-Table-Extract close · queue-live · dispatchers waiting)
**Discipline:** STRICT tests-first · mechanical RED before impl · double-green from floor 2956 · two-commit pattern · no push · credentials/PII discipline absolute.

---

## §Authority · owner ruling verbatim (2026-09-06T~15:XXZ, via user proxy)

> "OWNER RULINGS LANDED — bank verbatim: Question #1 (sms_sent drawer item) → "a" — INCLUDE message bodies with mask_regex_scrub. Question #2 (dedup-collapse remedy) → "a" — re-extract with sms_sent-inclusive emit and re-base the queued ablations on the diversified corpus.
>
> Execute W-SMS-Body-Emit as the follow-on wave you chartered:
> 1. Tests-first: update the drawer invariant (test_sms_sent_lives_in_clarification_drawer) to assert the NEW truth — drawer entry resolved by owner ruling 'a' with timestamp, sms_sent now in the ledger with mask_regex_scrub; right-reason RED on the old assertion first. The drawer lifecycle (question → owner answer → governed decision with evidence record → retroactive reclassification) is now exercised end-to-end for real — bank it as the first completed drawer cycle (Ruling #5 architecture proof).
> 2. Re-extract the ussd_plus_sms corpora (dedup + raw variants) with sms_sent included, full scrub pass, held-out slices hash-banked BEFORE staging, sha256-verified staging to akki-vm-ii.
> 3. Re-base the QUEUED-not-yet-started Campaign B runs (B-REF, B3, B4, B5, B6 — and B2 raw if its corpus composition changes) on the new corpora. Do NOT disturb any run already training or sealed. Bank the corpus-swap rationale in the campaign record (which runs trained on which corpus version — the ablation comparisons must be corpus-consistent: if B-REF re-bases, all its comparators must too; verify B1's comparability note).
> 4. Report the new dedup numbers (expect the 87-unique collapse to resolve) and the updated queue state, then STAND DOWN again per runbook.
> Double-green from floor 2956, receipts, two-commit pattern, credentials/PII discipline absolute. Go."

---

## §A · Drawer lifecycle · Ruling #5 architecture proof (first end-to-end cycle)

The `clarification_drawer` design has been in the workspace since 2026-08-31 (Ruling #5 authored). This wave exercises the first COMPLETE drawer cycle:

| Phase | Actor | Timestamp | Artifact |
|---|---|---|---|
| 1. Question raised | shield-train build wave | 2026-09-06T11:34:00Z | drawer entry `shield-2026-09-06-q001` opened with `cautious_default_applied='exclude'` |
| 2. Governance held ambiguity | main agent (this session) | 2026-09-06T~14:37Z | attempted ledger-add reverted after `test_sms_sent_lives_in_clarification_drawer` fired |
| 3. Owner ruling landed | owner (via user proxy) | 2026-09-06T~15:XXZ | ruling 'a' banked verbatim in DECISIONS.md |
| 4. Governed decision executed | main agent (W-SMS-Body-Emit) | 2026-09-06T~15:XXZ | drawer entry marked `state='resolved'`, `resolution` populated with owner_ruling/at_utc/choice_taken/evidence_record_path/retroactive_reclassification=True |
| 5. Evidence record written | this wave | 2026-09-06T~15:XXZ | `phase0/policy_drawer_resolutions/drawer_resolution_shield-2026-09-06-q001_YYYYMMDDTHHMMSSZ.json` |
| 6. Retroactive reclassification | this wave | 2026-09-06T~15:XXZ | `sms_log.sms_sent` moved from drawer → ledger with `action='mask_regex_scrub'`, `authored_by='programme.track-a.W-SMS-Body-Emit'`, `resolves_drawer_question_id='shield-2026-09-06-q001'` |
| 7. Downstream re-extraction | this wave | 2026-09-06T~15:XXZ | Campaign B queued corpora re-extracted with sms_sent-inclusive emit |
| 8. Invariant flip banked | this wave | this commit | pre-existing test rewritten to assert NEW truth; drawer-resolution-shape invariants added |

This is the reference lifecycle. Future drawer entries follow the same 8-step template.

---

## §B · Ledger entry for sms_sent (post-resolution)

```json
{
  "table": "sms_log",
  "column": "sms_sent",
  "class": "non-pii-text",
  "action": "mask_regex_scrub",
  "note": "SMS body free text (longtext). Included per owner Ruling #5(a) via drawer resolution shield-2026-09-06-q001. mask_regex_scrub belt-and-braces scrubs embedded phone/ID/national-ID/breeding-ref patterns; belt-and-braces refuse fires on residual PII shape via CorpusIntegrityRefusal.",
  "authored_at_utc": "<W-SMS-Body-Emit resolution timestamp>",
  "authored_by": "programme.track-a.W-SMS-Body-Emit",
  "resolves_drawer_question_id": "shield-2026-09-06-q001",
  "declassification_path": null
}
```

## §C · Drawer entry (post-resolution, retained for audit trail)

```json
{
  "field": "sms_log.sms_sent",
  "question_id": "shield-2026-09-06-q001",
  "opened_at_utc": "2026-09-06T11:34:00Z",
  "cautious_default_applied": "exclude",
  "note": "<original question text preserved>",
  "state": "resolved",
  "resolution": {
    "owner_ruling": "a",
    "resolved_at_utc": "<owner ruling timestamp>",
    "choice_taken": "INCLUDE with mask_regex_scrub",
    "evidence_record_path": "phase0/policy_drawer_resolutions/drawer_resolution_shield-2026-09-06-q001_YYYYMMDDTHHMMSSZ.json",
    "retroactive_reclassification": true,
    "wave": "W-SMS-Body-Emit"
  }
}
```

## §D · Formatter update

`services/shield_train/multi_table._compose_training_text_sms`:
- Prior wave (Ruling #5 open): survived on `sms_title` alone (topic-only).
- This wave (Ruling #5(a) resolved): survives on `sms_sent` (body); title opportunistic prefix.
- `_TABLE_FORMATTERS["sms_log"].required_fields` changes to `("sms_sent",)`.

## §E · Corpus re-extraction + queue rebase

**Re-extract:**
- `ussd_plus_sms_deduplicated` corpus 2 (post-body-emit) — expect dramatic drop in dedup collapse from 87 unique to ~15-25k unique.
- `ussd_plus_sms_raw` corpus 2 (post-body-emit) — expect ~50-60k rows (30k USSD + 30k SMS with body content).

**Queue rebase (Campaign B):**
- WAITING: B-REF-3B, B2-DEDUP-OFF, B3-RANK-8, B4-RANK-32, B5-CTX-512, B6-CTX-2048 → rebase all onto new corpora (B-REF/B3/B4/B5/B6 → dedup v2; B2 → raw v2).
- RUNNING (do NOT disturb): B1-CORPUS-USSD-ONLY (ussd-only corpus; no sms_sent involvement; ablation comparability preserved — see §F).

**B1 comparability note:**
- B1's corpus is `ussd_deduplicated` (single-table USSD, no SMS at all). The corpus-mix ablation compares B1 vs B-REF/B3/B4/B5/B6 — the SMS content in B-REF's corpus is what B1 is comparing against.
- Under Ruling #5(a) with sms_sent included, B-REF now has diversified SMS bodies (not just titles). The corpus-mix comparison becomes MORE meaningful: B1 (pure USSD) vs B-REF (USSD + full SMS bodies). Comparability preserved; the ablation just measures a stronger effect.
- No re-extraction needed for B1 (already running with its original corpus, which is unaffected by SMS classification).

---

## §F · Ablation-consistency invariant (banked here, tested in code)

For a set of comparator runs (B-REF, B3, B4, B5, B6 all use `ussd_plus_sms_deduplicated`), all runs in the comparator set MUST train on THE SAME corpus (same sha256). Otherwise the ablation isn't measuring the hyperparameter — it's confounded with corpus drift. B-REF/B3/B4/B5/B6 all point to dedup-v2's staged path. B2 points to raw-v2's staged path. B1 unchanged (its own USSD-only corpus).

## §G · Discipline (unchanged)

- STRICT tests-first (mechanical RED with the old assertion still passing before flip → RED right-reason on new assertion → GREEN after policy update).
- Credentials/PII discipline absolute: mask_regex_scrub belt-and-braces + `CorpusIntegrityRefusal` post-scrub PII-shape leak-check unchanged; scrub fires the same regex battery on `sms_sent` as it does on `question_string`/`option_string`.
- Double-green from floor 2956 → target new floor. Tandem ratchet update.
- Two-commit pattern: code + tests → `Extraction-Akki programme/track-a`; STATE + brief + drawer resolution record + updated queue + new receipts → workspace `master`. Local commit only, no push.

## §H · Wave-honest-limits banked

1. **Drawer resolution retroactivity is one-shot.** This wave marks the drawer entry as resolved and moves sms_sent to ledger, but existing on-disk corpora that were extracted PRE-resolution (Campaign B's dedup-v1 87-row corpus + raw-v1 25k corpus) are NOT deleted. They remain as historical evidence. Corpus sha256s stay in receipts as before. Only NEW corpora post-resolution have sms_sent-inclusive content. This is honest: the workspace records what happened when.
2. **Comparability across the corpus-swap is scoped to B-REF/B3/B4/B5/B6 (all rebase together).** Any comparison across the swap boundary (e.g. hypothetical B1 vs B2-v1) would be corpus-inconsistent. This wave ensures the swap is atomic per ablation set.
