# HF-HOLD closure receipt template · SEC-2026-09-12-01 · hash-delta verification shape

**Status at authoring:** SEC-2026-09-12-01 **OPEN** · owner acting FIRST today (2026-09-20) · HF console token revocation + regeneration + custody drop pending. This template is prepared so closure is mechanical when the drop lands.

**Owner disposition verbatim (2026-09-20T~21:24Z · this-session non-interrupting note):** *"E1 confirms closure by hash delta alone — the new file's hash differs from the byte-identical pair on record — never by opening the value."*

**Authority:** STANDING_ORDERS.md §4.3 HF TOKEN HASH-DELTA GATE (R-18 Part 7(e) · owner ruling 2026-09-18 · binding).

---

## Custody slot (ready to receive the drop)

- **Drop directory:** `custody/owner_drops/hf_token_rotation_SEC-2026-09-12-01/`
- **Expected drop filename shape:** `hf_token_rotated_<YYYYMMDD>.csv` (owner-controlled naming).
- **Alternative canonical shape (per STANDING_ORDERS §4.3):** `estate_keys/data_sources/hf_token_rotated_<yyyymmdd>.csv` (per prior banking).

E1 **MUST NOT** open the file. Only `sha256sum` runs against the drop.

---

## Last-recorded sha256 pair on record (byte-identical evidence · the "leaked-live" state)

Per STANDING_ORDERS §4.3 wording: *"`hf_token_rotated_20260914.csv` byte-identical to `hf_token.csv` stands as evidence that the 2026-09-14 filename-marker rotation never reached the custody store."* The byte-identical pair sha256 is banked at the STANDING_ORDERS reference; this template does NOT re-print it (per §4.1 §E · minimise re-quotation of credential-adjacent artefacts).

At closure time, E1 fetches the current sha256 from STANDING_ORDERS §4.3 wording or from the last close-report that cited it. If in doubt: hash both files at drop-time (the old byte-identical pair AND the new drop) and record all three sha256 in the receipt below.

---

## Hash-delta verification (fill in when the drop lands)

Fill the following table by running `sha256sum` on the specified files ONLY. Do not open, cat, head, tail, or otherwise inspect any of these files' contents. E1's disposition MUST be by hash delta alone.

```
| Reference                                                       | Last-known sha256 (from record)   | sha256 at closure time            |
|-----------------------------------------------------------------|-----------------------------------|-----------------------------------|
| estate_keys/data_sources/hf_token.csv                           | <look up from prior banking>      | <sha256sum at closure time>       |
| estate_keys/data_sources/hf_token_rotated_20260914.csv          | <look up from prior banking>      | <sha256sum at closure time>       |
| custody/owner_drops/hf_token_rotation_SEC-2026-09-12-01/<new>   | (n/a · new drop)                  | <sha256sum at closure time>       |
```

## Closure decision procedure (owner-fixed logic · zero-freedom to E1)

For the new drop at `custody/owner_drops/hf_token_rotation_SEC-2026-09-12-01/<new>`:

1. Compute `sha256sum <new_drop>` → call this `NEW_SHA256`.
2. Compute `sha256sum` on the last-recorded byte-identical pair (both files) → call these `OLD_SHA256_A` and `OLD_SHA256_B` (banked as equal at ingestion).
3. Compare `NEW_SHA256` against `OLD_SHA256_A` (which equals `OLD_SHA256_B` by construction).
4. **If `NEW_SHA256 != OLD_SHA256_A`:** closure PASSES. SEC-2026-09-12-01 **CLOSES**. OWNER-DROP-03 **CLOSES** with it. HF-touching waves may open. Bank the closure receipt (this file · filled in) plus DECISIONS+NEXT append. Not a §3.3 3-Commit Seal — this is a notes-only state-master closure (precedent `1250c39a`).
5. **If `NEW_SHA256 == OLD_SHA256_A`:** closure FAILS. SEC-2026-09-12-01 stays **OPEN**. HF-touching waves remain **HELD**. Bank the failed-closure attempt in DECISIONS with a note that owner must re-drop.
6. **E1 MUST NOT open the file at any point.** The delta test is a pure sha comparison. No `cat`, no `head`, no `less`, no `tail`, no editor open, no `openpyxl`, no `pandas`.

---

## Closure-time receipt (skeleton · to be filled at drop-time)

```
### HF-HOLD CLOSURE RECEIPT · SEC-2026-09-12-01

- Closure UTC: <YYYY-MM-DDTHH:MMZ>
- Drop location: <full path to new hf_token_rotated_*.csv drop>
- Drop sha256 (NEW_SHA256): <sha256>
- Last-recorded byte-identical pair sha256 (OLD_SHA256_A == OLD_SHA256_B): <sha256>
- Delta result: <NEW_SHA256 != OLD_SHA256_A ? "DIFFERENT · CLOSURE PASSES" : "IDENTICAL · CLOSURE FAILS · HOLD STANDS">
- E1 file-open scan: `history | grep -E "cat|head|tail|less|more|edit" | grep hf_token` → expected zero hits (E1 never opened the value).
- Disposition:
  - If DIFFERENT: SEC-2026-09-12-01 CLOSED. OWNER-DROP-03 CLOSED. HF-touching waves may open.
  - If IDENTICAL: HOLD stands. Owner must re-drop.
- Banked at: `phase0/spec_hunt_receipts/<YYYYMMDD>T<HHMM>Z_hf_hold_closure_receipt.md` + DECISIONS.md this-append + NEXT.md this-append.
- Not a §3.3 3-Commit Seal — notes-only state-master closure (precedent `14173772`).
```

---

## Standing bounds unchanged

- E1 opens no file contents. Only `sha256sum`.
- Owner-driven rotation is FIRST (HF console revocation + regeneration + drop) before any E1 action.
- HF-touching waves stay HELD until closure passes.
- Zero push · zero remote configured · terminal-only operations.

READ STATE/STANDING_ORDERS.md §4.3 FIRST — the authoritative HF hash-delta gate.
