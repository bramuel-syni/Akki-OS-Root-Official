/**
 * Binding verbatim strings from the Entitlement Service Spec v1.
 * These strings are BINDING on the frontend — a reworded string is a defect.
 *
 * Source: Entitlement_Service_Spec_v1.docx
 * Drop: custody/owner_drops/20260920T1300Z/
 *
 * ENT-23 (§7 Metering and the Bill):
 *   "Quantities always display; money displays only when measured.
 *    A reseller or provider that does not report cost yields cost_total null,
 *    rendered as the fixed string 'cost · not yet measured'."
 *
 * ENT-26 (§8 Credits, Limits, and Exhaustion):
 *   "When allowance is exhausted, the cascade stops escalating to
 *    reseller-frontier rows and serves the job on a local-served row.
 *    The response carries the fixed string 'Frontier allowance used · served locally'."
 *
 * ENT-34 (§10 Managed Frontier Through Reseller Channels):
 *   "A reseller channel that is unreachable or refuses is a closed gate for that row.
 *    The cascade serves the job on a local-served row with the fixed string
 *    'Frontier unavailable · served locally', or refuses if no local-served row can serve it."
 */

// ENT-23: cost_total is null → render this exact string
export const ENT_23_COST_NOT_MEASURED = "cost \u00b7 not yet measured";

// ENT-26: frontier allowance exhausted, served locally
export const ENT_26_FRONTIER_EXHAUSTION = "Frontier allowance used \u00b7 served locally";

// ENT-34: reseller channel unreachable, served locally
export const ENT_34_FRONTIER_UNAVAILABLE = "Frontier unavailable \u00b7 served locally";

/**
 * ENT-43 (§14 Feature Services — Model Picker Badges):
 *   "The model picker lists every catalog row admitted by the licence
 *    with one badge per row — Included · Local, Credits · Frontier,
 *    or Your key — and Auto at the top."
 *
 * Four picker badge strings, binding verbatim.
 */

// ENT-43 badge: local-served included row
export const ENT_43_BADGE_INCLUDED_LOCAL = "Included · Local";

// ENT-43 badge: frontier row paid by credits
export const ENT_43_BADGE_CREDITS_FRONTIER = "Credits · Frontier";

// ENT-43 badge: customer brings their own API key
export const ENT_43_BADGE_YOUR_KEY = "Your key";

// ENT-43 badge: automatic row selection
export const ENT_43_BADGE_AUTO = "Auto";
