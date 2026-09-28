/**
 * Binding verbatim strings for the Extraction Request Lifecycle.
 * These strings are BINDING on the frontend — a reworded string is a defect.
 *
 * Source: extraction_request_approval_journey_v2.md
 * Drop: custody/owner_drops/20260920T1600Z/
 *
 * Test-case cross-references from extraction_test_cases.xlsx (same drop).
 * Template placeholders ({{ dataOwner }}, {{ date }}, {{ N }}) are filled at
 * render time; the surrounding prose is verbatim.
 */

// ── TC-BLK-24  ·  §11 Executing  ·  Stop confirm ──────────────────────
// "Stop this request? What's run so far will still be billed; nothing
//  further will execute."
export const STOP_CONFIRM =
  "Stop this request? What's run so far will still be billed; nothing further will execute.";

// ── §11 party_halted (own rail state) — kind line ──────────────────────
// "You stopped this while it was running."
export const PARTY_HALTED_KIND_LINE =
  "You stopped this while it was running.";

// ── §11 party_halted (own rail state) — what-next ──────────────────────
// "To try again, submit a new request."
export const PARTY_HALTED_WHAT_NEXT =
  "To try again, submit a new request.";

// ── TC-INA-06  ·  §11 In Approval  ·  waiting + deadline ───────────────
// "If no one at {{ dataOwner }} decides by [date], the request expires.
//  It's been waiting [N] days."
// Rendered with interpolation; the two sentences always appear together.
export const IN_APPROVAL_WAITING_TPL = (dataOwner, windowEndsDate, waitDays) =>
  `If no one at ${dataOwner} decides by ${windowEndsDate}, the request expires. It's been waiting ${waitDays} days.`;

// ── TC-EXP-02  ·  §11 Expired  ·  date line ────────────────────────────
// "Expired [date]. No decision was made."
export const EXPIRED_DATE_TPL = (date) =>
  `Expired ${date}. No decision was made.`;

// ── TC-EXP-02  ·  §11 Expired  ·  waited line ──────────────────────────
// "Waited [N] days, the full review window."
export const EXPIRED_WAITED_TPL = (n) =>
  `Waited ${n} days, the full review window.`;

// ── §11 Expired  ·  meaning line ────────────────────────────────────────
// "No one at {{ dataOwner }} said yes or no, so nothing ran.
//  Nothing about your request was refused."
export const EXPIRED_MEANING_TPL = (dataOwner) =>
  `No one at ${dataOwner} said yes or no, so nothing ran. Nothing about your request was refused.`;

// ── §11 Expired  ·  what-next ───────────────────────────────────────────
// "To try again, submit it as a new request. It will go back to
//  {{ dataOwner }} for sign-off, with a new 14-day window."
export const EXPIRED_WHAT_NEXT_TPL = (dataOwner) =>
  `To try again, submit it as a new request. It will go back to ${dataOwner} for sign-off, with a new 14-day window.`;

// ── §11 Blocked, kind-line strings for the three kinds ─────────────────
// Ruling 2 (2026-09-20T~19:00Z): three Blocked kinds — request / check / estate.
// suspended is a principal state (DAP-27, PRIN-1), a different axis — its
// party-visible strings live in the suspension-notices surface, not here.
// party_halted is its own rail state (Q5 module tree); its drawer strings
// (PARTY_HALTED_KIND_LINE + PARTY_HALTED_WHAT_NEXT above) are retained per
// Ruling 2(d) "party_halted as its own rail state keeping its existing
// drawer copy".

// kind: request  §11 line 389
export const BLOCK_KIND_REQUEST =
  "This block is about the request. Submitting it again unchanged will be blocked again.";

// kind: check  §11 line 390
export const BLOCK_KIND_CHECK =
  "This block wasn't about your request. A check the platform has to run couldn't complete.";

// kind: estate  §11 line 391
export const BLOCK_KIND_ESTATE =
  "This block is about an estate-level limit, not your request or your agreement.";

// kind: estate  §11 line 394  fixed reason (DAP-35)
export const BLOCK_ESTATE_REASON =
  "The platform refused this release. No detail is available.";

// kind: party_halted  §11 line 393 (same as PARTY_HALTED_KIND_LINE above)

// ── §11 Blocked  ·  what-next by kind ───────────────────────────────────
// kind: request  §11 line 397
export const BLOCK_WHATNEXT_REQUEST =
  "To try again, change the request and submit it as a new one.";

// kind: check  §11 line 397
export const BLOCK_WHATNEXT_CHECK =
  "To try again, submit it as a new request.";

// kind: estate  §11 line 397
export const BLOCK_WHATNEXT_ESTATE_TPL = (dataOwner) =>
  `Contact ${dataOwner} before submitting again.`;

// kind: party_halted  §11 line 397 (same as PARTY_HALTED_WHAT_NEXT above)
