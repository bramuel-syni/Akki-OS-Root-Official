# FE-FIX-READY · R-87 CP-BLOCKED-VOCABULARY-CORRECTION · specialist dispatch spec

**Ruling authority:** Owner Ruling 2 (2026-09-20T~19:00Z · banked in STATE/DECISIONS.md OWNER RULINGS anchor line 20421 · re-affirmed at CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE Commit-C `e40047f4`).

**Owner ruling verbatim (the load-bearing clause the specialist executes to):**

> "FORK-BLK-KINDS: OPTION A RATIFIED, with a load-bearing vocabulary correction. Owner verbatim: suspension 'is a state of the principal (DAP-27, PRIN-1), not a fourth reason a request is blocked — a different axis, different object.' Sealed enum stays at three. party_halted lives as its own state via the Q5 module tree and its vocab constant, and it NEVER renders in the Blocked reason grammar — no estate copy, no kind label. Correct the wording at source everywhere non-sealed: it is 'three Blocked kinds plus Interrupted plus party_halted' — NOT 'five Blocked kinds.'"

**Owner reinforcement at R-87 open (2026-09-20T~20:30Z verbatim):**

> "(d) author the FE-FIX-READY spec with EXACT expected badge/legend/drawer grammar and strings — the specialist currently renders 'Blocked · suspended' and 'Blocked · party_halted' badges and a 5-kind legend, all of which must be re-shaped per the ruling (party_halted as its own rail state keeping its existing drawer copy; suspended out of request-block rendering entirely, surfacing only via suspension notices)."

**Backend registered vocabulary the FE imports authoritatively:**

- Module: `backend/services/dap_lifecycle/blocked_vocabulary.py` (R-87 Commit-A · sha in Commit-B seal report).
- `BLOCKED_KINDS_COUNT: Final[int] = 3`.
- `BLOCKED_KINDS_TUPLE: Final[tuple[str, ...]] = ("request", "check", "estate")`.
- `SUSPENDED_IS_PRINCIPAL_STATE_NOT_BLOCKED_KIND: Final[bool] = True`.
- `PARTY_HALTED_IS_OWN_RAIL_STATE_NOT_BLOCKED_KIND: Final[bool] = True`.
- `CORRECTED_COMPOSITION_PHRASE: Final[str] = "three Blocked kinds plus Interrupted plus party_halted"`.
- `WRONG_COUNT_PHRASES: Final[tuple[str, ...]]` — 4-variant grep-negative substrate.

**Scope note (specialist-dispatch boundary):** this spec is byte-precise before/after for the three surfaces the specialist currently owns: `StatusBadge.jsx`, `lifecycleStrings.js`, `RequestLifecycle.jsx`. No other file is in scope. Any additional file that renders Blocked/suspended/party_halted vocabulary is out-of-scope for R-87 and gets its own FE-FIX-READY spec.

---

## Surface 1 · `/app/frontend/src/components/dap/StatusBadge.jsx`

### CURRENT (specialist head · pre-R-87)

```jsx
const STATUS_META = {
  "In Approval": { color: "var(--brass, #b08d2e)", bg: "rgba(176,141,46,.14)" },
  "Executing": { color: "var(--accent, #4c5fd5)", bg: "rgba(76,95,213,.12)" },
  "Ready": { color: "var(--gate, #7c3aaf)", bg: "rgba(124,58,175,.12)" },
  "Retrieved": { color: "var(--sage, #1d7a6e)", bg: "rgba(29,122,110,.12)" },
  "Refused": { color: "var(--ink, #1b1f27)", bg: "rgba(27,31,39,.08)" },
  "Blocked": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Expired": { color: "var(--ink3, #5b6270)", bg: "var(--surface2, #ede8da)" },
  "Interrupted (platform fault)": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  // Five blocked kinds per journey v2 §5
  "Blocked \u00b7 request": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Blocked \u00b7 check": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
  "Blocked \u00b7 estate": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  "Blocked \u00b7 suspended": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  "Blocked \u00b7 party_halted": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
};
```

### TARGET (post-R-87)

```jsx
const STATUS_META = {
  "In Approval": { color: "var(--brass, #b08d2e)", bg: "rgba(176,141,46,.14)" },
  "Executing": { color: "var(--accent, #4c5fd5)", bg: "rgba(76,95,213,.12)" },
  "Ready": { color: "var(--gate, #7c3aaf)", bg: "rgba(124,58,175,.12)" },
  "Retrieved": { color: "var(--sage, #1d7a6e)", bg: "rgba(29,122,110,.12)" },
  "Refused": { color: "var(--ink, #1b1f27)", bg: "rgba(27,31,39,.08)" },
  "Blocked": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Expired": { color: "var(--ink3, #5b6270)", bg: "var(--surface2, #ede8da)" },
  "Interrupted (platform fault)": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  // Three Blocked kinds per Ruling 2 (2026-09-20T~19:00Z): request / check / estate.
  // Interrupted (platform fault) is its own rail state (above), NOT a Blocked kind.
  // party_halted is its own rail state (below), NOT a Blocked kind — carries its
  // existing drawer copy from services/dap_lifecycle/party_halted_kind.py.
  // suspended is a principal state (DAP-27, PRIN-1), a different axis, and NEVER
  // renders in the Blocked reason grammar — surfaces only via suspension notices.
  "Blocked \u00b7 request": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Blocked \u00b7 check": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
  "Blocked \u00b7 estate": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  // party_halted rail state · own drawer · not a Blocked variant.
  "party_halted": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
};
```

### Delta summary (StatusBadge.jsx)

| # | Change | Line-context |
|---|---|---|
| 1 | REMOVE `"Blocked · suspended"` STATUS_META entry entirely. | Was line 15. |
| 2 | RESHAPE `"Blocked · party_halted"` → `"party_halted"` (drop the `Blocked · ` prefix; party_halted is own rail state, not a Blocked kind). | Was line 16. |
| 3 | REPLACE comment `// Five blocked kinds per journey v2 §5` with the 5-line block above citing Ruling 2 + the three-axis discipline. | Was line 12. |

**No other change to StatusBadge.jsx.** The component's render logic (`data-testid`, `<span style={{...}}>`, className) is unchanged — the badge label is passed as-is via the `status` prop.

**Caller callsite change (in `RequestLifecycle.jsx` · see Surface 3):** any callsite that previously passed `status="Blocked · suspended"` now must NOT render a StatusBadge at all (suspended surfaces only via suspension notices, not as a request badge). Any callsite that previously passed `status="Blocked · party_halted"` now passes `status="party_halted"` (dropping the `Blocked · ` prefix).

---

## Surface 2 · `/app/frontend/src/strings/lifecycleStrings.js`

### CURRENT (specialist head · pre-R-87)

Full block from line 60 to line 128 (see file). Key exports present:

- `BLOCK_KIND_REQUEST` (§11 line 389) — kind: request.
- `BLOCK_KIND_CHECK` (§11 line 390) — kind: check.
- `BLOCK_KIND_ESTATE` (§11 line 391) — kind: estate.
- `BLOCK_ESTATE_REASON` (§11 line 394, fixed reason, DAP-35).
- `BLOCK_KIND_SUSPENDED_EXECUTING_TPL` (§11 line 392) — kind: suspended from Executing.
- `BLOCK_KIND_SUSPENDED_IN_APPROVAL_TPL` (§11 line 392) — kind: suspended from In Approval.
- `BLOCK_KIND_SUSPENDED_READY_TPL` (§11 line 392) — kind: suspended from Ready.
- `BLOCK_WHATNEXT_REQUEST` / `BLOCK_WHATNEXT_CHECK` / `BLOCK_WHATNEXT_ESTATE_TPL` — what-next for the 3 kinds.
- `BLOCK_WHATNEXT_SUSPENDED_TPL` — what-next for suspended.
- `PARTY_HALTED_KIND_LINE` + `PARTY_HALTED_WHAT_NEXT` — kept as-is per Ruling 2(d).

### TARGET (post-R-87)

**REMOVE four exports** (suspended is a principal state, not a Blocked reason; these strings do not belong in Blocked reason grammar):
- `BLOCK_KIND_SUSPENDED_EXECUTING_TPL`
- `BLOCK_KIND_SUSPENDED_IN_APPROVAL_TPL`
- `BLOCK_KIND_SUSPENDED_READY_TPL`
- `BLOCK_WHATNEXT_SUSPENDED_TPL`

**RESHAPE the section header comment** at line 60. Replace verbatim:

```js
// ── §11 Blocked, kind-line strings for all five kinds ───────────────────
// (request, check, estate already existed in RequestLifecycle.jsx as
//  inline literals; centralized here for the same reason.)
```

with:

```js
// ── §11 Blocked, kind-line strings for the three kinds ─────────────────
// Ruling 2 (2026-09-20T~19:00Z): three Blocked kinds — request / check / estate.
// suspended is a principal state (DAP-27, PRIN-1), a different axis — its
// party-visible strings live in the suspension-notices surface, not here.
// party_halted is its own rail state (Q5 module tree); its drawer strings
// (PARTY_HALTED_KIND_LINE + PARTY_HALTED_WHAT_NEXT above) are retained per
// Ruling 2(d) "party_halted as its own rail state keeping its existing
// drawer copy".
```

**RETAIN unchanged:** `BLOCK_KIND_REQUEST` · `BLOCK_KIND_CHECK` · `BLOCK_KIND_ESTATE` · `BLOCK_ESTATE_REASON` · `BLOCK_WHATNEXT_REQUEST` · `BLOCK_WHATNEXT_CHECK` · `BLOCK_WHATNEXT_ESTATE_TPL` · `PARTY_HALTED_KIND_LINE` · `PARTY_HALTED_WHAT_NEXT` · `STOP_CONFIRM` · `IN_APPROVAL_WAITING_TPL` · `EXPIRED_DATE_TPL` · `EXPIRED_WAITED_TPL` · `EXPIRED_MEANING_TPL` · `EXPIRED_WHAT_NEXT_TPL`.

**RETAIN section-tail comment** `// kind: party_halted  §11 line 393 (same as PARTY_HALTED_KIND_LINE above)` and `// kind: party_halted  §11 line 397 (same as PARTY_HALTED_WHAT_NEXT above)` (these accurately point back to the retained top-of-file exports).

**REMOVE section-tail comment** `// kind: suspended, from Executing  §11 line 392`, `// kind: suspended, from In Approval  §11 line 392`, `// kind: suspended, from Ready  §11 line 392`, `// kind: suspended  §11 line 397`.

### Delta summary (lifecycleStrings.js)

| # | Change |
|---|---|
| 1 | REMOVE 4 suspended-in-Blocked exports (`BLOCK_KIND_SUSPENDED_EXECUTING_TPL` · `BLOCK_KIND_SUSPENDED_IN_APPROVAL_TPL` · `BLOCK_KIND_SUSPENDED_READY_TPL` · `BLOCK_WHATNEXT_SUSPENDED_TPL`) + their per-export section-comments. |
| 2 | RESHAPE section header comment at line 60 (5-kind → 3-kind + axis discipline explainer). |

---

## Surface 3 · `/app/frontend/src/pages/dap/RequestLifecycle.jsx`

### CURRENT specialist head · pre-R-87 (relevant sites)

- Line 6-7: import `PARTY_HALTED_KIND_LINE`, `PARTY_HALTED_WHAT_NEXT`.
- Line 17: import `BLOCK_KIND_SUSPENDED_EXECUTING_TPL` (+ line 18/19 sibling imports if present).
- Line 21: import `BLOCK_WHATNEXT_SUSPENDED_TPL`.
- Line 27: file docstring `* FIVE Blocked kinds: request, check, estate, suspended, party_halted (§5, §11).`.
- Line 62-64: `KIND_META[suspended] = {...}` entry.
- Line 68-70: `KIND_META[party_halted] = { kindLine: PARTY_HALTED_KIND_LINE, whatNext: PARTY_HALTED_WHAT_NEXT }` entry.
- Line 161-170: `party_halted` sample data (retained · own rail state).
- Line 173-183: `suspended` sample data (REMOVE · suspended does not surface in the request-Blocked rail).
- Line 187-189: legend array containing `"Blocked · suspended"` and `"Blocked · party_halted"`.
- Line 213-220: `kindLine` resolver switching on `req.blockKind === "suspended"` (REMOVE branch).
- Line 227-228: `whatNext` resolver switching on `req.blockKind === "suspended"` (REMOVE branch).
- Line 399: comment `Blocked drawer — all five kinds`.
- Line 406, 427, 435, 436, 460: conditional render logic mentioning `suspended` / `party_halted`.

### TARGET (post-R-87)

The RequestLifecycle.jsx changes are structural because party_halted becomes its own rail state (not a Blocked variant) and suspended exits the request-Blocked rendering surface entirely. The specialist executes the following delta:

1. **Imports (lines 6-21):**
   - RETAIN: `PARTY_HALTED_KIND_LINE`, `PARTY_HALTED_WHAT_NEXT`.
   - REMOVE: `BLOCK_KIND_SUSPENDED_EXECUTING_TPL`, `BLOCK_KIND_SUSPENDED_IN_APPROVAL_TPL` (if imported), `BLOCK_KIND_SUSPENDED_READY_TPL` (if imported), `BLOCK_WHATNEXT_SUSPENDED_TPL`.

2. **File docstring (line 27):** replace `FIVE Blocked kinds: request, check, estate, suspended, party_halted (§5, §11).` with `THREE Blocked kinds: request, check, estate (§5, §11) — plus Interrupted (own rail state, platform fault) and party_halted (own rail state, party stopped executing request per Q5 module tree). suspended is a principal state (DAP-27, PRIN-1), a different axis, and surfaces only via suspension notices — never in Blocked reason grammar.`

3. **KIND_META (lines 62-70):**
   - REMOVE the `suspended` entry entirely (lines 62-67 or however the specialist has it).
   - RETAIN the `party_halted` entry AS-IS (kindLine + whatNext) — its drawer copy is preserved per Ruling 2(d). Rename the containing map from `KIND_META` (Blocked-only variant) to a broader `RAIL_STATE_KIND_META` if the specialist chooses, OR keep `KIND_META` and simply route party_halted through its own rendering path (not the Blocked drawer). Structural choice at specialist discretion; the constraint is: party_halted is NOT rendered as a Blocked variant.

4. **Sample data (lines 161-183):**
   - RETAIN `party_halted` sample (own rail state · own drawer).
   - REMOVE `suspended` sample entirely from the Blocked-rail sample list. If a suspended sample is needed elsewhere, it belongs on a separate suspension-notices surface (out of scope for R-87).

5. **Legend array (lines 187-189):**
   - REMOVE `"Blocked · suspended"` entry.
   - REPLACE `"Blocked · party_halted"` with `"party_halted"` (matching the reshaped StatusBadge STATUS_META key).

6. **kindLine resolver (lines 213-220):** remove the `if (req.blockKind === "suspended")` branch and its three sub-branches.

7. **whatNext resolver (line 227-228):** remove the `if (req.blockKind === "suspended")` branch.

8. **Blocked drawer comment (line 399):** replace `Blocked drawer — all five kinds` with `Blocked drawer — three kinds (request / check / estate). party_halted has its own rail drawer (separate render path).`.

9. **Conditional render logic (lines 406-465 approx):**
   - Frozen-progress conditional (line 406): scope to `request` / `check` (party_halted moves to its own drawer). REMOVE `suspended` from any conditional here.
   - Reason conditional (line 427): scope to `request` / `check` (estate uses fixed copy). REMOVE `suspended` / `party_halted` from any conditional here.
   - Who-stopped-it (lines 435-436): party_halted's own drawer renders this; the Blocked drawer does NOT.
   - Copy-into-new-request (line 460): scope to `request` / `check` (per journey v2 §11 L398). party_halted's own drawer renders its own "To try again, submit a new request" phrasing (same string as `PARTY_HALTED_WHAT_NEXT`). REMOVE `suspended` from any conditional here.

10. **NEW party_halted own-drawer render path:** if not already present, add a separate rendering branch outside the Blocked drawer for `party_halted` rail state, rendering:
    - Kind line: `PARTY_HALTED_KIND_LINE` = *"You stopped this while it was running."*
    - What-next: `PARTY_HALTED_WHAT_NEXT` = *"To try again, submit a new request."*
    - Blocked-by shown by name (if `req.blockedBy` present) — current line 435-436 logic retained on this path.

### Delta summary (RequestLifecycle.jsx)

| # | Change |
|---|---|
| 1 | Remove 3 suspended imports (specialist current: 3 imports at lines 17/19/21). |
| 2 | Reshape file docstring 5-kind → 3-kind + axis discipline. |
| 3 | Remove `KIND_META[suspended]` entry entirely. |
| 4 | Remove suspended sample data + retain party_halted sample data. |
| 5 | Legend array: remove `"Blocked · suspended"`, replace `"Blocked · party_halted"` with `"party_halted"`. |
| 6 | Remove suspended branches in kindLine + whatNext resolvers. |
| 7 | Reshape Blocked drawer comment 5-kind → 3-kind. |
| 8 | Blocked drawer conditional-render logic: scope to request/check/estate ONLY; move party_halted to its own rail-drawer render path (retaining its drawer copy per Ruling 2(d)). |
| 9 | Add party_halted own-drawer render path (kind line + what-next + blocked-by-by-name). |

**Reason field discipline (Ruling 2):**
- `request` / `check`: reason field renders `req.reason` verbatim (backend-recorded plain-language text per journey v2 §11 L243).
- `estate`: reason field renders fixed uninformative copy `BLOCK_ESTATE_REASON` per DAP-35 (unchanged).
- `party_halted` (own rail state): NO reason field per journey v2 §11 L394 verbatim (`PARTY_HALTED_KIND_LINE` renders instead of a reason field · no estate copy · no kind label).
- `suspended`: does NOT surface in Blocked drawer at all (principal-state axis · surfaces via suspension notices).

---

## Acceptance criteria for specialist merge-back

1. `grep -rn "Blocked · suspended" /app/frontend/src` → zero hits.
2. `grep -rn "Blocked · party_halted" /app/frontend/src` → zero hits.
3. `grep -rniE "five Blocked kinds|5 Blocked kinds|Blocked has five kinds|five kinds of Blocked" /app/frontend/src` → zero hits.
4. `grep -rn "BLOCK_KIND_SUSPENDED\|BLOCK_WHATNEXT_SUSPENDED" /app/frontend/src` → zero hits.
5. `StatusBadge.jsx STATUS_META` contains exactly the 12 keys enumerated in the TARGET block above (no more, no fewer).
6. `lifecycleStrings.js` exports set = current − 4 suspended-in-Blocked exports; no other export added or removed.
7. `RequestLifecycle.jsx` renders party_halted on its own rail-state drawer (not inside the Blocked drawer conditional).
8. `req.blockKind === "suspended"` occurrences in `RequestLifecycle.jsx` → zero (removed entirely).
9. The three Blocked kinds `request` / `check` / `estate` continue rendering exactly as pre-R-87 (behaviour + copy unchanged).
10. Any data-testid tokens that previously encoded `"blocked-suspended"` or `"blocked-party-halted"` are updated to reflect the reshape (e.g., `data-testid="status-badge-party-halted"` for the party_halted rail badge; no data-testid for suspended-in-Blocked because that surface no longer exists).

---

## Backend authority binding

The specialist MAY import from `backend/services/dap_lifecycle/blocked_vocabulary.py` (or a FE mirror derived from it) to reference `BLOCKED_KINDS_TUPLE` and the axis-binding constants. The load-bearing binding is the Final[...] registration on the backend; the FE surface conforms to it. Any future addition to `BLOCKED_KINDS_TUPLE` requires a Canon 3 §24 4-step rule-change ceremony (owner counter-sign), not a specialist edit.

---

## Standing bounds preserved

- Zero write to sealed backend files.
- Zero write to sealed contracts.
- Additive-only per SO §3.8 (removal of exports/branches in FE non-sealed surfaces is source-fix per Ruling 2(c), not a §3.8-refactor of a sealed surface).
- Specialist dispatch discipline unchanged: this-desk authors the spec; owner dispatches specialist; specialist merges into `/app/frontend/*` per FE COORDINATION seal precedent (`d0a2ea9b` byte-verify + this-wave R-87 mirror-drift-half-post-R-86 · unification eventual at CP-APP-JS-UNIFY R-91).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
