# OWNER CORRECTION · na7p4* is Huawei not AWS · 2026-02-23T08:09:00Z

**Received:** 2026-02-23T08:09:00Z (immediately after original drop 2 · during CP-AIP-8 pre-Commit-A build).
**Handling:** Banked as separate append entry per correction directive verbatim ("do not rewrite history"). Sibling file `DROP.md` retained unrewritten.

---

## OWNER CORRECTION (verbatim)

> "na7p4* is huawei not AWS"

## OWNER CORRECTED FRAMING (verbatim)

- The `na7p4*` buckets (incl. `na7p4374`) live on **HUAWEI OBS, TR-Istanbul**. They are **NOT AWS buckets.** Label them as Huawei OBS everywhere in the census and receipts.

- Content relationship per owner: `na7p4*` holds the **INITIAL video-content data**, of which a copy was sent to AWS as backup. So two estates may hold the same content: **Huawei OBS `na7p4*`** (Archive class, blocked GetObject historically, direct-read now enabled) and the **AWS S3 estate** (readable with existing keys).

- **Scenario C in OWNER-Q2 stands but with corrected direction**: cross-check the readable AWS S3 estate for copies of the `na7p4*` content (filename/size/hash overlap via occurrence index). If the AWS copy is readable, we source from AWS and pay Huawei nothing for unarchive. Report estimated overlap %. If AWS overlap can't be established (e.g., the AWS copy was lifecycle-archived to Glacier), report that storage class too — Glacier retrieval has its own fee schedule, and the receipt should then compare Huawei direct-read vs AWS Glacier retrieval cost per GB.

- Fix any line in the banked drop or DECISIONS.md that could read as "na7p4* is on AWS" — **additively (append a correction stanza, do not rewrite history)**.

Everything else unchanged. Continue the CP-AIP sequence; deliver the corrected receipts at the next report-and-continue.

---

## SUPERSEDE MAP (append-only per correction directive)

| Sibling `DROP.md` line reading as (paraphrased) | Correction |
|---|---|
| "na7p4* has data sent to AWS" (original owner statement 2 verbatim) | **CORRECTED**: `na7p4*` is on Huawei OBS TR-Istanbul; it holds the initial video content · a copy was sent to AWS as backup. Two estates may hold the same bytes. |
| "Scenario C: na7p4* is on AWS" | **CORRECTED**: Scenario C = cross-check AWS S3 estate for copies of `na7p4*` (Huawei) content · source from AWS if readable · pay Huawei nothing for unarchive. Also compare Huawei direct-read vs AWS Glacier retrieval (if AWS copy was lifecycle-archived to Glacier). |

The original `DROP.md` retains the owner's verbatim words unrewritten. Downstream receipts (`receipt_Q1_viusasa_census.md` + `receipt_Q2_na7p4_unarchive_cost.md`) are written with this corrected framing in force.
