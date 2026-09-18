# CHUNK 1 · Task A · Canon Pack Verification

**Session:** 2026-09-18 · Post CP-M11-GATE-RELEASE Commit-C-supplement (`d7dc76f9`).
**Governance:** ingest + ground truth only, per owner Blocker-1 ruling (c) Hybrid.
**Rule set:** 4a strict title match; report anomalies exactly.

---

## 1 · Source URL

Problem-statement URL:

```
https://customer-assets-v7afamib.emergentagent.net/job_a963bf18-f7d3-42c9-b8dd-aba51af40caf/artifacts/96u2c488_files%20%288%29.zip
```

Fresh download to `/tmp/chunk1_fresh/canon_pack_fresh.zip` this session.

## 2 · SHA-256 fingerprint

| Path | sha256 | bytes |
|---|---|---|
| /tmp/chunk1_fresh/canon_pack_fresh.zip (fresh-this-session) | `5a46676d9c8506cc4d65616e3dbfa9db76885362fbaa0c210894295daae30759` | 236,005 |
| /app/assessment_workspace/canon/canon_pack.zip (existing) | `5a46676d9c8506cc4d65616e3dbfa9db76885362fbaa0c210894295daae30759` | 236,005 |
| /app/assessment_workspace/downloads/canon_pack.zip (existing) | `5a46676d9c8506cc4d65616e3dbfa9db76885362fbaa0c210894295daae30759` | 236,005 |

**All three copies are byte-identical.** The disk copies match the current URL exactly. Verified in-session.

## 3 · Zip contents (9 files as expected)

`unzip -l canon_pack_fresh.zip`:

| # | Filename | Bytes | Timestamp | sha256 (extracted) |
|---|---|---|---|---|
| 1 | `Akki_Canon_1_Custody_Platform.docx` | 26,593 | 2026-08-14 05:10 | `b2d59a326490ef99eaa5cd5c3ff3a57e06408283ef7a45a720a9a8bacc15167f` |
| 2 | `Akki_Canon_2_CIF.docx` | 21,918 | 2026-08-14 05:10 | `223ee7fc02a3e81a277022adb6c721a93af39b939dbca874a0820d6c5dc6c372` |
| 3 | `Akki_Canon_3_Governance_Engines.docx` | 30,333 | 2026-08-14 05:10 | `4f31f73b0972fe6b499d41ff2ab2fd30bbe8a177e969c6e091958bc500d1f019` |
| 4 | `Akki_Canon_4_Operating_Engines.docx` | 40,016 | 2026-08-14 05:10 | `c9eee6bf792accdc30fe9979f4422fb47953adafdd8f8ec4d9e10233a0cafd35` |
| 5 | `Akki_Canon_5_Interface_Architecture.docx` | 37,810 | 2026-08-14 05:10 | `d0f17bab1bee9bad478950b491a0764a92363ce6fcba82c7d16822840eaf7780` |
| 6 | `Akki_Canon_6_User_Journeys.docx` | 20,240 | 2026-08-14 05:10 | `3d559a9ced2c3472e8c942ca0217333ff09504ce63a612f95a2b2d23aaf0f02e` |
| 7 | `Akki_Canon_7_Integration_and_Quality.docx` | 33,516 | 2026-08-14 05:10 | `9f03b529244e0099606424f6d754927e7f1513869e141d32fbdbbf85a34a4e51` |
| 8 | `Akki_Canon_8_The_Watch.docx` | 30,451 | 2026-08-14 05:10 | `ea4ce6a92720eaef43aea76887e995709ffc26941ba7f0528cb6ee00aac4f9aa` |
| 9 | `Akki_Canon_9_Mkondo_Charter.docx` | 16,861 | 2026-08-14 05:10 | `ef5f42d32b9e666bef9bf892403cf6174f3bc56e227e2b7f691016c12194ff2b` |
| — | (total) | 257,738 | — | — |

**Zip contains exactly 9 files.** No extras, no missing.

## 4 · Document titles (rule 4a · strict match)

All 9 docs are readable. Titles extracted from first non-empty paragraphs of `word/document.xml`.

| # | Doc header verbatim | Doc title verbatim | Problem-statement expected title | Strict match? |
|---|---|---|---|---|
| 1 | AKKI CANON  ·  DOCUMENT 1 OF 9 | `Akki — The Custody Platform` | `Akki — The Custody Platform` | ✅ EXACT |
| 2 | AKKI CANON  ·  DOCUMENT 2 OF 9 | `The Conditioned Ideation Faculty` | `The Conditioned Ideation Faculty` | ✅ EXACT |
| 3 | AKKI CANON  ·  DOCUMENT 3 OF 9 | `Akki Governance Engines` | `Akki Governance Engines` | ✅ EXACT |
| 4 | AKKI CANON  ·  DOCUMENT 4 OF 9 | `Akki Operating Engines` | `Akki Operating Engines` | ✅ EXACT |
| 5 | AKKI CANON  ·  DOCUMENT 5 OF 9 | `Akki Interface Architecture` | `Akki Interface Architecture` | ✅ EXACT |
| 6 | AKKI CANON  ·  DOCUMENT 6 OF 9 | `Akki User Journeys` | `Akki User Journeys` | ✅ EXACT |
| 7 | AKKI CANON  ·  DOCUMENT 7 OF 9 | `Akki Integration Service and Quality Rulebook` | `Integration Service and Quality Rulebook` | ⚠ NEAR-MATCH · doc title carries prefix `Akki ` that the problem-statement title lacks |
| 8 | AKKI CANON  ·  DOCUMENT 8 OF 9 | `The Watch` | `The Watch` | ✅ EXACT |
| 9 | AKKI CANON  ·  DOCUMENT 9 OF 9 | `The Mkondo Charter` | `The Mkondo Charter` | ✅ EXACT |

**Result: 8/9 EXACT strict matches. 1/9 near-match (Canon 7).**

## 5 · Anomalies (report exactly)

- **A1 · Canon 7 title prefix divergence** (rule 4a strict). The problem statement expects title `Integration Service and Quality Rulebook`. The doc title verbatim is `Akki Integration Service and Quality Rulebook` (has `Akki ` prefix). Content and section numbering appear consistent; this is a title-string prefix delta only. Not fuzzy-matched per rule 4a; surfaced verbatim.
- **A2 · Extra material in `/app/assessment_workspace/canon/`** not present in the canonical zip: file `AKKI_Canon_Addendum_1.docx` (16,794 bytes, 2026-08-25) + subdirs `unpacked/`, `text/`, `addendum_1_extracted/`, `drops/`, `fixtures/`, `prototypes/`, `w11_batch2_v3/`, `w11_new_docs/`. These were added by prior sessions and are outside the CHUNK 1 canonical pack. Reported per binding rule "the zip contains extra material — report it exactly". Note: the zip itself does NOT carry the addendum; the extra material is workspace-only.
- **A3 · Two on-disk copies of the zip** exist (`canon/canon_pack.zip` from 2026-08-14 and `downloads/canon_pack.zip` from 2026-09-13). Both are byte-identical to the fresh-download this session. No divergence.

## 6 · Extraction artefact

Full plain-text extraction of all 9 docs written this session to:

```
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_1_Custody_Platform.txt   (239 lines · 29,802 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_2_CIF.txt                (189 lines · 17,901 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_3_Governance_Engines.txt (309 lines · 35,923 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_4_Operating_Engines.txt  (399 lines · 61,594 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_5_Interface_Architecture.txt (546 lines · 47,130 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_6_User_Journeys.txt      (132 lines · 18,125 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_7_Integration_and_Quality.txt (297 lines · 47,815 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_8_The_Watch.txt          (295 lines · 34,943 B)
/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_9_Mkondo_Charter.txt     (129 lines · 8,625 B)
```

Total 2,535 lines. These are the working sources for Task D requirement extraction below.

## 7 · Conclusion

Canon pack **verified** against problem-statement URL. All 9 required docs present, readable, and title-matched (8/9 EXACT · 1/9 near-match with `Akki ` prefix on Canon 7). Extra workspace material (addendum + subdirs) is not in the canonical zip and does not affect canon integrity.
