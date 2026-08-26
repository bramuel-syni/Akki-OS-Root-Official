import React from "react";
import { ShieldAlert } from "lucide-react";
import ClassBadge from "./ClassBadge";

/**
 * RefusalCard.jsx — W11 R5 · Canon 5 §9.2 binding-copy card.
 *
 * Owner directive verbatim (2026-08-26):
 *   "lift RefusalCard.js verbatim from RMS/OS-V1 into
 *    pod_shell/frontend/src/components/, wire every refusal surface
 *    (chat, connect, training seal refusal, solva) through it per
 *    Canon 5 §9.2 binding-copy card."
 *
 * Canon 5 §9.2 verbatim (from
 * canon/text/Akki_Canon_5_Interface_Architecture.txt lines 130-140):
 *   "Not to the standard you asked for.
 *    Accept as recorded statement · Narrow the objective · Lower the standard
 *    A refusal is the system keeping its promise.
 *    The title, the three actions, and the footer are binding copy,
 *    reproduced verbatim wherever this card renders. They are never
 *    paraphrased, shortened, or restyled for a particular surface."
 *
 * Canon-vs-donor supersession note: the donor RefusalCard.js in
 * Akki-OS-V1 / RMS-IQ-Core-2 renders headline 'Not to the standard
 * required.' — this is a paraphrase of Canon 5 §9.2 and violates
 * owner Condition 1 (no paraphrasing requirements). This component
 * lifts the DONOR STRUCTURE (React shell + amber styling + ShieldAlert
 * icon + ClassBadge integration + data-testids) but rebases the
 * BINDING COPY on Canon 5 §9.2 verbatim. Recorded in DECISIONS.md
 * at Wave A close 2026-08-26.
 */

// Canon 5 §9.2 verbatim · binding copy · reproduced without change.
const CANON_5_9_2_TITLE = "Not to the standard you asked for.";
const CANON_5_9_2_ACTIONS = [
  "Accept as recorded statement",
  "Narrow the objective",
  "Lower the standard",
];
const CANON_5_9_2_FOOTER = "A refusal is the system keeping its promise.";

export default function RefusalCard({ refusal, onAction }) {
  if (!refusal) return null;
  return (
    <div
      data-testid="refusal-card"
      className="rounded-lg border-2 border-amber-300 bg-amber-50 p-5"
    >
      <div className="flex items-start gap-3">
        <ShieldAlert className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          {/* Canon 5 §9.2 verbatim title. Never paraphrased. */}
          <h3
            data-testid="refusal-headline"
            className="text-sm font-semibold text-amber-900"
          >
            {CANON_5_9_2_TITLE}
          </h3>

          <dl className="mt-3 space-y-2 text-sm">
            {refusal.asked && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Asked</dt>
                <dd data-testid="refusal-asked" className="mt-0.5 text-amber-900">{refusal.asked}</dd>
              </div>
            )}
            {refusal.reason && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Reason</dt>
                <dd data-testid="refusal-reason" className="mt-0.5 text-amber-900 font-mono text-xs">{refusal.reason}</dd>
              </div>
            )}
            {refusal.supported_class && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Supported class</dt>
                <dd data-testid="refusal-supported-class" className="mt-0.5">
                  <ClassBadge defensibilityClass={refusal.supported_class} />
                </dd>
              </div>
            )}
            {refusal.what_would_raise_it && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">What would raise it</dt>
                <dd data-testid="refusal-raise" className="mt-0.5 text-amber-900">{refusal.what_would_raise_it}</dd>
              </div>
            )}
          </dl>

          {/* Canon 5 §9.2 verbatim three-actions row. Never paraphrased. */}
          <div
            data-testid="refusal-actions"
            className="mt-4 flex flex-wrap items-center gap-2"
          >
            {CANON_5_9_2_ACTIONS.map((action, i) => (
              <React.Fragment key={action}>
                {i > 0 && (
                  <span className="text-amber-500 text-xs" aria-hidden="true">·</span>
                )}
                <button
                  data-testid={`refusal-action-${action.split(" ")[0].toLowerCase()}`}
                  onClick={() => onAction && onAction(action)}
                  className="text-xs font-medium text-amber-900 border border-amber-300 bg-amber-100 hover:bg-amber-200 rounded px-2 py-1 transition-colors"
                  type="button"
                >
                  {action}
                </button>
              </React.Fragment>
            ))}
          </div>

          {/* Canon 5 §9.2 verbatim footer. Never paraphrased. */}
          <p
            data-testid="refusal-footer"
            className="mt-4 text-xs text-amber-700 italic"
          >
            {CANON_5_9_2_FOOTER}
          </p>
        </div>
      </div>
    </div>
  );
}

// Named exports for tests that verify verbatim strings live in the module.
export { CANON_5_9_2_TITLE, CANON_5_9_2_ACTIONS, CANON_5_9_2_FOOTER };
