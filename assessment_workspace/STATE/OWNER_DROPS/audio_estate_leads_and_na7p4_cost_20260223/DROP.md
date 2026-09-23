# OWNER DROP + OWNER QUESTION · audio estate leads + na7p4* unarchive cost estimate · 2026-02-23

**Received:** 2026-02-23T08:06:00Z (during CP-AIP-8 build · pre-Commit-A ORCH_BOOT edit).
**Handling:** BANK VERBATIM at CP-AIP-8 State Commit-B (next state-repo touch per owner directive). Two fold-in RECEIPTS delivered alongside this drop.

**Correction filed 2026-02-23T08:09:00Z** — banked verbatim as append-only stanza in `DROP_CORRECTION.md` (this file NOT rewritten per correction directive).

---

## OWNER STATEMENT (verbatim)

1. "More leads to where audio is - On CAL Huawei account, On viusasa - there is a bucket transcoded-content, folder MUSIC and MUSIC-AUDIO"

2. "Response to the blocked buckets - Those buckets (na7p4374) have the initial data sent to AWS, its backup of our video content. See attached. Could be data you already viewed. There is a cost to unarchive them - what the estimate."

## OWNER SCREENSHOT FACTS (verbatim bank)

- Bucket `na7p4374` · Standard | Multi-AZ · region TR-Istanbul · created 2024-04-15.
- Objects under `imported/DR 009 RAW FOO...`.
- Individual objects Storage Class = **Archive** (e.g., "DROUGHT AND FAMINE; KENYANS FOR KENYA, DONATIONS-BOB COLLYMORE.mp4" 264.40 MB; others 225–738 MB).
- Console banner confirms **DIRECT READING FUNCTION IS ALREADY ENABLED** on this bucket ("You can now download Archive data without restoring... direct reading function is billable").

---

## OWNER-Q1 · viusasa transcoded-content census (fold-in)

Using existing sealed census machinery (no new services, §1.2), enumerate on the CAL Huawei account: bucket `transcoded-content`, folders `MUSIC/` and `MUSIC-AUDIO/`. Output a census receipt: object counts, total bytes, storage classes, extension histogram, readability (GetObject yes/no). Additive receipt only; if access fails, record the exact error code as an honest gap.

## OWNER-Q2 · na7p4* unarchive cost ESTIMATE (fold-in · measured not asserted)

The owner wants a number. Produce a cost-estimate receipt built from MEASUREMENTS wherever possible:

1. Enumerate na7p4* buckets via object LISTING (ListObjects is often permitted even where GetObject 403s — verify per bucket). For each: object count, total bytes, bytes by storage class (Archive vs Standard), largest objects. If listing is also denied, fall back to the owner console figures + prior census (~102 TB claim) and FLAG the total as unmeasured.

2. Fetch current Huawei OBS TR-Istanbul rates from https://www.huaweicloud.com/intl/en-us/pricing (or support.huaweicloud.com price-obs pages) for: (a) Archive data restore per GB — Standard speed vs Expedited, (b) direct-reading traffic per GB, (c) restore request fee per 1k requests, (d) temporary Standard-copy storage per GB-month, (e) outbound internet traffic per GB. If the page is unreachable from pod, record the formula with rate placeholders and flag rates as unmeasured.

3. Present THREE scenarios in the receipt, each = measured_bytes × rate with explicit CI/flags:
   - **Scenario A** — Direct read only what we need (already enabled): cost = bytes_read × direct-read rate; supports selective audio-track extraction without full restore; no temp-copy fee.
   - **Scenario B** — Standard restore of full corpus: restore fee + request fees + temp Standard copy for validity window.
   - **Scenario C** — ZERO-RESTORE PATH: owner says na7p4* is a BACKUP of content already sent to AWS. Cross-check the AWS S3/RDS estate census for the same content (filename/size/hash overlap via the occurrence index). Report estimated overlap %. Every byte already readable on AWS is a byte we never pay Huawei to unarchive. If overlap is high, recommend C.

4. Also note in the receipt: these are .mp4 VIDEO files — for the audio plane we only need audio tracks, so even Scenario A/B costs scale by the fraction actually read (direct-read supports ranged reads billed by requested range — cite the range-billing rule).

---

## STANDING FRAMING

Cadence, bans, and all 17 guards unchanged: HALT after CP-AIP-10, immediate HALT on SPEC-CONFLICT.

Deliver both receipts in the next report-and-continue. Then resume the CP-AIP sequence.

---

## ACTION LOG (this drop)

- [x] Verbatim banking at `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/DROP.md` (this file · unrewritten).
- [x] Owner correction (2026-02-23T08:09Z) banked as separate append entry `DROP_CORRECTION.md` — na7p4* is Huawei not AWS · Scenario C direction corrected.
- [x] Two fold-in RECEIPTS delivered at this seal boundary: `receipt_Q1_viusasa_census.md` + `receipt_Q2_na7p4_unarchive_cost.md` (both HONEST-GAP receipts — pod cannot reach Huawei OBS credentials or Huawei public pricing pages; formulae banked with rate placeholders).
- [x] One-line entry in `STATE/DECISIONS.md` (dashes not colons).

**Cadence unchanged.** Continuing CP-AIP-8 → CP-AIP-9 → CP-AIP-10 sequentially. HALT after CP-AIP-10 seals.
