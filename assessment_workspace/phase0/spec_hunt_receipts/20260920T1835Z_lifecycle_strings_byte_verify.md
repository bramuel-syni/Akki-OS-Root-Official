# FE Coordination byte-verify · R-85 post-seal · lifecycleStrings.js against journey v2 §11 source bytes

**Timestamp**: 2026-09-20T~18:35Z
**Trigger**: Owner directive verbatim this-session — "at your next clean boundary, byte-match verify lifecycleStrings.js against journey v2 §11 source bytes. [...] If any string mismatches: report the exact expected bytes and I will dispatch the specialist for a one-line fix pass (your frontend write-ban stands)."
**Scope**: Read-only byte-verify against `custody/owner_drops/20260920T1600Z/extraction_request_approval_journey_v2.md`.
**Specialist commit under review**: `f090e8305` on `/app/` main (`feat(lifecycle): journey v2 conformance`).

## Full byte-verify sweep summary

- **19 fixed strings checked** across `lifecycleStrings.js`
- **16 MATCH** (byte-exact verbatim against journey v2)
- **3 MISMATCH** — all of type curly apostrophe U+2019 (UTF-8 `e2 80 99`) where journey v2 has ASCII apostrophe 0x27 (UTF-8 `27`)
- **0 NOT-FOUND**
- **0 REVERSE-MISMATCH**

Owner's Suspect 1 (party_halted what-next missing "it"): **FALSE ALARM** — specialist's `"To try again, submit a new request."` is byte-exact against journey v2 L397's party_halted branch. The doc uses the short form (no "it") for `party_halted` and the long form ("submit it as a new request") only for `check`. Specialist correctly distinguished.

Owner's Suspect 2 (Stop confirm U+2019 vs ASCII): **CONFIRMED MISMATCH** — plus 2 additional apostrophe swaps discovered during the sweep.

## MISMATCH 1 · `STOP_CONFIRM` (lifecycleStrings.js line 17)

**Journey v2 L366 expected bytes (verbatim):**

```
"Stop this request? What's run so far will still be billed; nothing further will execute."
```

- utf-8 hex: `53 74 6f 70 20 74 68 69 73 20 72 65 71 75 65 73 74 3f 20 57 68 61 74 27 73 20 72 75 6e 20 73 6f 20 66 61 72 20 77 69 6c 6c 20 73 74 69 6c 6c 20 62 65 20 62 69 6c 6c 65 64 3b 20 6e 6f 74 68 69 6e 67 20 66 75 72 74 68 65 72 20 77 69 6c 6c 20 65 78 65 63 75 74 65 2e`
- Apostrophe at byte-position after "What": **`27`** (ASCII 0x27 · `'`)

**Specialist current bytes:**

```javascript
export const STOP_CONFIRM =
  "Stop this request? What\u2019s run so far will still be billed; nothing further will execute.";
```

- utf-8 hex: `53 74 6f 70 20 74 68 69 73 20 72 65 71 75 65 73 74 3f 20 57 68 61 74 e2 80 99 73 20 72 75 6e 20 73 6f 20 66 61 72 20 77 69 6c 6c 20 73 74 69 6c 6c 20 62 65 20 62 69 6c 6c 65 64 3b 20 6e 6f 74 68 69 6e 67 20 66 75 72 74 68 65 72 20 77 69 6c 6c 20 65 78 65 63 75 74 65 2e`
- Apostrophe at byte-position after "What": **`e2 80 99`** (U+2019 · `’`)

**First differing byte**: index 23 (specialist `e2 80 99` should be `27`).

**Fix**: replace `What\u2019s` → `What's` (single character).

## MISMATCH 2 · `IN_APPROVAL_WAITING_TPL` (lifecycleStrings.js line 34)

**Journey v2 L321 expected bytes (fixed prose fragment):**

```
, the request expires. It's been waiting
```

- utf-8 hex of the "It's" span: `49 74 27 73` (`I`, `t`, ASCII apostrophe `27`, `s`)

**Specialist current bytes:**

```javascript
`If no one at ${dataOwner} decides by ${windowEndsDate}, the request expires. It\u2019s been waiting ${waitDays} days.`
```

- utf-8 hex of the "It\u2019s" span: `49 74 e2 80 99 73`

**Fix**: replace `It\u2019s` → `It's` (single character).

## MISMATCH 3 · `BLOCK_KIND_CHECK` (lifecycleStrings.js line 68)

**Journey v2 L390 expected bytes (verbatim):**

```
"This block wasn't about your request. A check the platform has to run couldn't complete."
```

- utf-8 hex: `54 68 69 73 20 62 6c 6f 63 6b 20 77 61 73 6e 27 74 20 61 62 6f 75 74 20 79 6f 75 72 20 72 65 71 75 65 73 74 2e 20 41 20 63 68 65 63 6b 20 74 68 65 20 70 6c 61 74 66 6f 72 6d 20 68 61 73 20 74 6f 20 72 75 6e 20 63 6f 75 6c 64 6e 27 74 20 63 6f 6d 70 6c 65 74 65 2e`
- Two apostrophe positions: `wasn` + `27` + `t`, and `couldn` + `27` + `t` — both ASCII `0x27`

**Specialist current bytes:**

```javascript
export const BLOCK_KIND_CHECK =
  "This block wasn\u2019t about your request. A check the platform has to run couldn\u2019t complete.";
```

- utf-8 hex: `54 68 69 73 20 62 6c 6f 63 6b 20 77 61 73 6e e2 80 99 74 20 61 62 6f 75 74 20 79 6f 75 72 20 72 65 71 75 65 73 74 2e 20 41 20 63 68 65 63 6b 20 74 68 65 20 70 6c 61 74 66 6f 72 6d 20 68 61 73 20 74 6f 20 72 75 6e 20 63 6f 75 6c 64 6e e2 80 99 74 20 63 6f 6d 70 6c 65 74 65 2e`

**Fix**: replace `wasn\u2019t` → `wasn't` AND `couldn\u2019t` → `couldn't` (two character positions in the same string).

## Total fix scope for specialist

**4 apostrophe characters across 3 exported constants (1 file · lifecycleStrings.js).** All are single-character `\u2019` → `'` (or byte-level `e2 80 99` → `27`). No other changes. Grep-anchor: `wc -l lifecycleStrings.js` should still show 109 lines (unchanged); only 4 byte positions change.

## Corollary observation (report-only · not scope for specialist)

The 3 mismatches suggest journey v2's markdown source uses **ASCII 0x27 everywhere** for possessive/contraction apostrophes in the fixed strings. If the specialist has other files with `\u2019` in journey-v2-anchored strings (e.g., `RequestLifecycle.jsx` inline literals mentioned in the report but out-of-scope for this-verify), those may share the same defect class. Owner may want a broader specialist sweep including those files.

## MATCH set (16 constants byte-verbatim GREEN)

- `PARTY_HALTED_KIND_LINE` ("You stopped this while it was running.")
- `PARTY_HALTED_WHAT_NEXT` ("To try again, submit a new request.") — Owner's Suspect 1 CLEARED
- `EXPIRED_DATE_TPL` fixed prose (". No decision was made.")
- `EXPIRED_WAITED_TPL` fixed prose (" days, the full review window.")
- `EXPIRED_MEANING_TPL` fixed prose ("said yes or no, so nothing ran. Nothing about your request was refused.")
- `EXPIRED_WHAT_NEXT_TPL` fixed prose ("for sign-off, with a new 14-day window.")
- `BLOCK_KIND_REQUEST` ("This block is about the request. Submitting it again unchanged will be blocked again.")
- `BLOCK_KIND_ESTATE` ("This block is about an estate-level limit, not your request or your agreement.")
- `BLOCK_ESTATE_REASON` ("The platform refused this release. No detail is available.")
- `BLOCK_KIND_SUSPENDED_EXECUTING` ("suspended your access while this was running.")
- `BLOCK_KIND_SUSPENDED_IN_APPROVAL` ("suspended your access before a decision was made.")
- `BLOCK_KIND_SUSPENDED_READY` ("suspended your access before you retrieved this.")
- `BLOCK_WHATNEXT_REQUEST` ("To try again, change the request and submit it as a new one.")
- `BLOCK_WHATNEXT_CHECK` ("To try again, submit it as a new request.")
- `BLOCK_WHATNEXT_ESTATE` fixed fragment ("before submitting again.")
- `BLOCK_WHATNEXT_SUSPENDED` fixed fragment ("A new request will be blocked while your access is withdrawn.")

## Canon anchors

`extraction_request_approval_journey_v2.md` (custody `owner_drops/20260920T1600Z/` drop · file sha256 verified byte-identical to R-83 ingest at CP-CONTENT-REGISTRY-INGEST-DROP `6d910bbe`) §11 lines 321 + 366 + 389 + 390 + 391 + 392 + 393 + 394 + 397 + associated Expired/In-Approval prose · plus `lifecycleStrings.js` at `/app/frontend/src/strings/lifecycleStrings.js` (specialist commit `f090e8305` on `/app/` main).

## Disposition

- Report to owner with exact expected bytes (this file + summary in DECISIONS/NEXT state-only banking).
- **This-desk frontend write-ban stands** — no `/app/frontend/**` edit from this desk (except `/app/frontend/public/audit/`).
- Owner dispatches specialist for one-line fix pass at their convenience.
- Byte-verify half of this cross-check item stays PARTIALLY-OPEN until specialist fix lands (then close via a follow-on state-only banking).
