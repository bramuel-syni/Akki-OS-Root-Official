READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon/drops/20260913 · MANIFEST (delta 2026-09-13T19:05Z owner drop #2)

## Owner drop #2 · `owner_drop_2/`

| File | sha256 | Bytes | Registered as |
|---|---|---|---|
| `Security_Assurance_Promise_Set_v3.xlsx` | `51d52ebd7acf4ef9d47eaf4634c1970e087cc71d021bc56763c3064f07f86f30` | 18882 | Promise-Set **v3** (authoritative from 2026-09-13T19:05Z) |
| `Watch_Learning_Amendment_v1.docx`       | `eb8a0bec26a519b3cad97d412514775c6560b5553079d8e5802dfe8b2f69a9f1` | 18630 | Watch Learning Amendment v1 (first canonical drop) |

Filenames as delivered ("(3)", "(1)") are dropbox-side dedupe suffixes, NOT version metadata.  Lineage established by hash below.

## Promise-Set version lineage (by hash)

| Version | sha256 | Path | Notes |
|---|---|---|---|
| v1  (2026-09-07) | `f824056dff929fc20c195dd923cb6816e84db3941a9e1f18ce53edce51128f45` | `drops/20260907/extracted/files_12/Security_Assurance_Promise_Set.xlsx` + `.../raw/security_assurance_promise_set.xlsx` + `drops/20260907/extracted/files_13/Security_Assurance_Promise_Set.xlsx` | Initial |
| v1a (2026-09-09) | `8c7a3b7205db0166852ceffc879e2461053ee4af61eedbdb02c253e2deb0010d` | `drops/20260909/extracted/files_14/Security_Assurance_Promise_Set.xlsx` | Republish (same day drop group) |
| **v2  (2026-09-13 owner drop #1)** | `72a4e7620c959a8d0dd36c73ed5c712689ed8f0663630803b79a43f0db453088` | `drops/20260913/raw/Security_Assurance_Promise_Set_v2.xlsx` | Added S-27 (per prior banking) |
| **v3  (2026-09-13 owner drop #2 · THIS)** | `51d52ebd7acf4ef9d47eaf4634c1970e087cc71d021bc56763c3064f07f86f30` | `drops/20260913/owner_drop_2/Security_Assurance_Promise_Set_v3.xlsx` | **AUTHORITATIVE.**  S-7 closed at spec level · S-28 + S-29 new · Legend scope "S-1–S-29" |

## Row-level diff v3 vs v2 (`Security Assurance Set` sheet)

- **rows:** v2 = 29 · v3 = 31 (+2)
- **ADDED (v3):** `S-28`, `S-29` (see §1..§3 below).
- **REMOVED:** none.
- **CHANGED (same id · different row):** `S-7` — 3 columns changed:
  - col `Implementation Status`: v2 `"Absent → gap"` → v3 `"Absent → new (spec-closed, 13 Sep 2026)"`.
  - col `Bound / Ruling`: v2 `"Unruled — no mechanism exists to bound"` → v3 `"Closed by Watch Learning Amendment L-2, L-4.  R-15 (initial library) and R-16 (ratifier, cadence) open."`.
  - col `Where It Lives / Notes`: v2 `"Gap between A1 (plain-language promise) and A5 (constrains learning, never specifies it)"` → v3 same + `"CLOSED AT SPEC LEVEL: what updates — the certificate-requirement library; on what evidence — in-environment data points, each anchored; at what layer — deterministic gates at the verdict interface, not detector weights; under what ceremony — the Watch's own (RBM-8).  Not built."`.
- **Legend sheet:** `Scope of this set` row updated `"S-1–S-27"` → `"S-1–S-29"`.

## New promises S-28 · S-29 (verbatim `Promise` column)

**S-28** — *"The system will never act on a verdict it cannot evidence — every Watch action carries a certificate a human can read, and every behaviour it learns to recognise entered its vocabulary through ceremony, not through silent training."*

**S-29** — *"The system will admit no new class of action into the world without ceremony on the record — every action names the admission it acts under, and no learner ratifies its own."*

## New OPEN rulings introduced by Watch Learning Amendment v1

- **R-15** — initial certificate library seed.  Recommended seed: DAP-32's canary-touch + trigger classes + four AC-1 ceilings, each entering through RBM-8.
- **R-16** — ratifying role for certificate requirements + research-queue review cadence.  Recommended: external witness (C3) as witness role; ratifier is a named role — owner input required; cadence TBD.
- **R-17** — capability-class granularity + each deployment's initial register.  Recommended: seed a deployment's register from action vocabulary + tool surface at admission (one class per tool or output type).

## Cross-references landed this drop

- `notes/canon_grey_mirror_requirements.md` — NEW — first-pass grey-mirror requirements extraction; folds in L-1..L-3 as R-GM-10..R-GM-12.
- `notes/canon_watch_learning_amendment_v1_requirements.md` — NEW — exhaustive L-1..L-5 requirements + S-7 close determination + M2 non-blocking check.
- `notes/MILESTONE_PROMISE_BINDING_20260913_delta_watch_learning.md` — NEW (this drop) — binding delta note; supersedes header of `MILESTONE_PROMISE_BINDING_20260913.md`'s promise-set count for the S-Set scope.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
