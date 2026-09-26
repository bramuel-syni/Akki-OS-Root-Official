[B1] AKKI PLATFORM  ·  ENGINE SPECIFICATION  ·  CONTEXT MANAGEMENT LAYER

[B2] Data Cleanliness

[B3] data_cleanliness_v1 — which records check out, which do not, and what may enter training

[B4R1] Problem | Garbage in produces garbage out at an unknown rate. Shape — how many tables, which columns are empty, where personal data sits — is not cleanliness. Nothing on the platform yet answers, per record: is this structurally valid, does it agree with itself, does it agree with the other copy, and can it be relied on for a purpose. Marking a record unmeasured is honest; it is not the same as keeping it out.

[B4R2] What exists | The census quality profile (Document 9 B3): null rates, constant columns, cardinality, orphan tables, foreign-key candidates, personal-data signals, drift between runs. Deterministic; every figure carries its method. Structured sources only.

[B4R3] What this adds | Seven check families producing a per-record bitmap; four strata rolled up from it; a garbage register per source; a deterministic gate that decides what may enter a training manifest; and the build decomposition under the Execution Standard.

[B4R4] Principle | Clean is not a property of a dataset. It is a set of verdicts per field, per record, against named checks. A number without its checks is not a measure.

[B4R5] Date | 26 September 2026

[B5] 1   Definitions

[B6] Check  a named, deterministic predicate over one record, or over one record and another it is compared with, returning pass, fail, or not applicable.

[B7] Rule pack  the set of checks that apply to one source, confirmed by the data owner. A check enters a pack only on confirmation.

[B8] Bitmap  the per-record vector of check outcomes. Every bit maps to a named check in the pack.

[B9] Sentinel  a value that passes type checks and carries no information: a placeholder date, a dummy identifier, a required-field filler.

[B10] Natural key  the field or fields that identify the same real-world entity across sources: a phone number, a national identifier, an account number — hashed where personal.

[B11] Stratum  one of Clean, Repairable, Suspect, Junk, assigned to a record from its bitmap by fixed rule.

[B12] Garbage register  the per-source report: share of each stratum, the list of records per stratum, and the failing checks that placed each.

[B13] Repair  a deterministic transformation with a stated inverse or a retained original: trim, normalise a format, parse a date, map an enumeration. Never a guess at a value.

[B14] 2   The Check Families

[B15] Seven families, run in this order because each depends on the last. Each is a subtask under the Execution Standard with its own denominator, artefact, and acceptance.

[B16] 2.1  Structural validity

[B17] DQ-1  Every field parses to its declared type; every formatted field matches its format rule; encodings are valid — a field containing mojibake fails; every foreign key resolves to an existing row. The census foreign-key candidate graph is the input; the check is whether each candidate resolves.  [family 1]

[B18] 2.2  Sentinels

[B19] DQ-2  Every source carries a sentinel list, built from cardinality: a value appearing in a supposedly unique or high-cardinality field at a share above a ruled threshold (R-38) is a sentinel candidate; a candidate becomes a sentinel on the owner's confirmation. A record carrying a sentinel in a field fails that field's check. Sentinels are never silently nulled.  [family 2]

[B20] 2.3  Internal consistency

[B21] DQ-3  Cross-field rules a record must satisfy: ordered dates; totals equal to their parts; enumerations within their set; values inside the window another field defines. Rules come from the owner interview per source; a learned component may propose candidates from profiling, and a candidate is a rule only on confirmation.  [family 3]

[B22] 2.4  Duplication

[B23] DQ-4  Three grades, each producing a match list with tier and evidence: exact, by row hash; key-based, the same natural key on more than one row; fuzzy, normalised fields within a ruled tolerance (R-39). No grade merges. A merge is a human act recorded with the records it joined and the rule it applied.  [family 4]

[B24] 2.5  Cross-source agreement

[B25] DQ-5  Every entity with a natural key in two or more sources is matched and compared field by field where fields are shared. The output is a disagreement list and a disagreement rate per field per source pair. The check records which source disagrees; it does not decide which is right.  [family 5]

[B26] 2.6  Plausibility and drift

[B27] DQ-6  Values outside a physically or logically possible range fail; values beyond a ruled distance from the field's own distribution are flagged, not failed; distribution shift between census runs beyond what growth explains is flagged at the field. Flags are recorded in the bitmap as their own bit.  [family 6]

[B28] 2.7  Provenance

[B29] DQ-7  Every record carries its source, its writing pipeline where known, and its write time where known. A record with none of the three is not failed; it is marked provenance-unknown, which caps its stratum at Suspect for any purpose requiring defensibility.  [family 7]

[B30] 2.8  Media objects

[B31] DQ-8  For audio and video objects, the structural family includes: decodability; header duration against payload duration; sample rate against the channel's declared rate; clipping and silence ratio against ruled thresholds (R-40); duplicate detection by acoustic fingerprint as the fuzzy grade of DQ-4. None of these uses a learned model.  [families 1, 4, 6 for media]

[B32] 3   Strata

[B33R1] Stratum | Assigned when | Consequence

[B33R2] Clean | Every applicable check in the pack passes; no plausibility flag; provenance known | Enters any use its custody class permits

[B33R3] Repairable | Fails only checks with a defined repair (DQ-9); nothing else | Enters use after repair; original retained; repair recorded

[B33R4] Suspect | Fails a consistency, cross-source or plausibility check; or provenance unknown; or a fuzzy-duplicate match | Enters use only on an owner decision per rule, recorded

[B33R5] Junk | Fails structural validity; carries a sentinel in a required field; or is an exact or key duplicate of a retained row | Never enters training; never enters an answer as fact; listed, not deleted

[B34] DQ-9  A repair is deterministic, named in the pack, and either reversible or applied with the original retained alongside. A repair that requires choosing between values is not a repair; it is a Suspect outcome for a human.

[B35] DQ-10  Stratum assignment is a pure function of the bitmap and the pack. Two runs over the same record with the same pack version assign the same stratum. The pack is versioned; a pack change re-strata the source and the change is receipted.

[B36] 4   The Garbage Register

[B37] DQ-11  Every source has a garbage register per pack version: the count and share of each stratum; the list of records per stratum with the checks that placed each; the sentinel list; the duplicate lists by grade; the disagreement list; the repairs applied. It is the artefact of this specification, and every figure on any surface derives from it.

[B38] DQ-12  The register reconciles: Clean + Repairable + Suspect + Junk = the source's record count, exactly, per pack version. A register that does not reconcile is not published.

[B39] DQ-13  Accuracy — whether a value is true — is measured only where ground truth exists and is named. Where it does not, the register states accuracy: not measured. Validity, consistency, uniqueness, plausibility and provenance are never presented as accuracy.

[B40] 5   The Training Gate

[B41] DQ-14  A training manifest cites only records in Clean or Repairable strata. A Suspect record enters a manifest only with an owner decision receipt naming the rule it failed and the reason it is admitted. A Junk record in a manifest is refused at commission. This is one MOAC criterion: every cited unit carries a passing bitmap at the pack version named in the manifest.  [Targeta; MOAC]

[B42] DQ-15  The same gate applies to any unit cited as fact in an answer: a Junk record is never the anchor of a fact-class claim; a Suspect record anchors at most an inference.  [Doc 4 A2; A5.5]

[B43] 6   Build Decomposition — under the Execution Standard

[B44] Each row is a subtask carrying the six fields of the task contract. Denominators are pinned before procedures run; acceptance scripts are written first; reconciliation is the first check in each.

[B45R1] # | Subtask | Denominator | Artefact | Acceptance core

[B45R2] 1 | Enumerate | Every registered source → table → column; every media channel → file | Inventory list, hashed | Every registered source present; every unreachable one with a cause from the closed set; count pinned

[B45R3] 2 | Sentinels | Every column with cardinality below N or a top value above X% | Candidate list: value, count, share, example | Every candidate has all four; owner confirmation recorded per source; no confirmed sentinel absent

[B45R4] 3 | Format rules | Every column with a role signal | Rule pack entries | Every role-tagged column has a rule or an explicit no-rule with reason

[B45R5] 4 | Consistency rules | Every table | Rule pack entries | Every table has ≥ 1 cross-field rule or a recorded none-stated from the owner interview

[B45R6] 5 | Run checks | Every row of every table; every file | Per-record bitmap | Bitmap rows = record count per table; every bit maps to a named check in the pack version

[B45R7] 6 | Duplicates | Every row; every file | Match lists per grade | Every match carries tier and evidence; exact-duplicate share reconciles to hash counts; no merge path exists in code

[B45R8] 7 | Cross-source | Every entity with a natural key in ≥ 2 sources | Disagreement list | Every matched pair compared on every shared field; rate per field per pair

[B45R9] 8 | Media integrity | Every file on every channel | Per-file verdict | Verdict rows = file count; header-vs-payload on every file; fingerprint index complete

[B45R10] 9 | Strata | Every record | Garbage register | DQ-12 reconciliation; every non-Clean record names its failing checks

[B45R11] 10 | Training gate | Every unit in a manifest | MOAC criterion result | Manifest cites only Clean or Repaired; every Suspect carries a decision receipt; Junk refused

[B46] Shortcut list for this specification (EX-5)

[B47] Running checks on a sample of tables and reporting the estate. Declaring sentinels from the heuristic without owner confirmation. A strata total that does not reconcile to the record count. “No duplicates found” with no fingerprint index or hash table on record. A training manifest citing records with no bitmap at the named pack version. Each has a detector in the acceptance script of the subtask it belongs to.

[B48] Build order

[B49] Subtasks 1, 2, 3 and the exact grade of 6 first — days of work over the existing profile, and they find most of the junk. Subtasks 4 and 3 need one owner interview per source. Subtask 7 is the one piece of real engineering. Subtask 8 waits on the media enumeration tools. Subtask 10 is one criterion added to MOAC.

[B50] 7   Placement in the Standing Enumerations

[B51R1] Document | Entry

[B51R2] tcb_enumeration_v1 | IN: the check runner (DQ-1 to DQ-8), stratum assignment (DQ-10), and the training gate (DQ-14) — deterministic; their failure falsifies S-34. OUT: any component that proposes candidate rules or sentinels from profiling — learned or heuristic; it proposes, the owner confirms.

[B51R3] determinism_inventory_v1 | Data cleanliness: Deterministic in all decision paths; Hybrid only in rule-candidate proposal.

[B51R4] failure_posture_v1 | Pack unreadable → no strata published, source marked not-assessed. Check runner cannot reach a record → unmeasured with reason, never Clean by default. Register does not reconcile → not published.

[B51R5] Document 9 (census) | The bitmap and register are census artefacts: per stratum, method-carried, objective-blind. The pack is confirmed by the owner, not shaped by any job.

[B51R6] Master Requirements Registry | DQ-1 through DQ-15 and S-34 at this refresh.

[B52] 8   New Promise

[B53R1] ID | Promise | Rests on

[B53R2] S-34 | The platform knows, per record, which checks it passed and which it failed; no figure about cleanliness is shown without its checks; nothing that failed structural validity or carries a sentinel enters training or anchors a fact; and every source’s strata reconcile to its record count. | DQ-1 to DQ-15. Bounds: R-38 to R-40. Scope edge: accuracy is measured only where ground truth exists and is named.

[B54] 9   What This Does Not Claim

[B55] LIM-1  It does not measure truth. Validity, consistency, uniqueness, plausibility and provenance are what it measures; accuracy only against named ground truth.

[B56] LIM-2  It does not write rule packs. Rules come from owners; the platform proposes candidates and runs what is confirmed.

[B57] LIM-3  It does not delete. Junk is listed and kept out; removal is an owner act under the retention and erasure rules.

[B58] LIM-4  It does not use a learned model to decide a stratum. Any future learned quality signal enters as a plausibility flag through the research queue and never as a bit that fails a record.

[B59] 10   Rulings

[B60] R-38  Sentinel candidate threshold: share of a field above which a single value is a candidate. Recommend 2% in fields with a role signal of identifier or timestamp; 20% elsewhere. DEFAULT-class.

[B61] R-39  Fuzzy-duplicate tolerance per field type (normalised string distance; numeric tolerance). Recommend baseline-period approach from the first run’s match lists. DEFAULT-class.

[B62] R-40  Media thresholds: silence ratio, clipping share, header-payload duration tolerance. Recommend from the first enumerated channel’s distribution. DEFAULT-class.

[B63] Design note. The cheapest checks find the most junk: sentinels, format validity, exact duplicates. The most expensive check — cross-source agreement — finds the junk nobody knew was junk, because both copies looked fine on their own. Build in that order, and publish the register after the first three; a partial register that reconciles is worth more than a complete one that does not exist.
