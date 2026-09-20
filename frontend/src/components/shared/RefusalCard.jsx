import React from "react";

/**
 * RefusalCard — Canon 5 §9.2 refusal display.
 * 
 * Copy is binding verbatim per FE Integration Brief §2.2:
 *  - Title: "Not to the standard you asked for."
 *  - Actions: "Accept as recorded statement" · "Narrow the objective" · "Lower the standard"
 *  - Footer: "A refusal is the system keeping its promise."
 */
export default function RefusalCard({ asked, reason, supportedClass, whatWouldRaiseIt, onAction }) {
  const classLabels = {
    fact: "Established fact",
    utterance: "Recorded statement",
    non_factual: "Non-factual context",
  };

  return (
    <div
      data-testid="refusal-card"
      className="border-l-4 rounded-lg p-6"
      style={{ borderColor: "var(--oxblood, #b8395b)", background: "rgba(184,57,91,.04)" }}
    >
      <h3
        data-testid="refusal-title"
        className="text-lg font-semibold mb-3"
        style={{ color: "var(--ink, #1b1f27)" }}
      >
        Not to the standard you asked for.
      </h3>

      {asked && (
        <p data-testid="refusal-asked" className="text-sm mb-2" style={{ color: "var(--ink2, #3d4350)" }}>
          <span className="font-medium">Asked:</span> {asked}
        </p>
      )}

      {reason && (
        <p data-testid="refusal-reason" className="text-sm mb-2" style={{ color: "var(--ink2, #3d4350)" }}>
          <span className="font-medium">Reason:</span> {reason}
        </p>
      )}

      {supportedClass && classLabels[supportedClass] && (
        <span
          data-testid="refusal-class-badge"
          className="inline-block text-xs px-2 py-1 rounded mb-3"
          style={{ background: "rgba(27,31,39,.06)", color: "var(--ink2, #3d4350)" }}
        >
          {classLabels[supportedClass]}
        </span>
      )}

      {whatWouldRaiseIt && (
        <p data-testid="refusal-raise" className="text-sm mb-3 italic" style={{ color: "var(--ink3, #5b6270)" }}>
          {whatWouldRaiseIt}
        </p>
      )}

      <div className="flex flex-wrap gap-2 mb-4" data-testid="refusal-actions">
        <button
          data-testid="refusal-action-accept"
          className="text-sm px-3 py-1.5 rounded border transition-colors hover:bg-gray-50"
          style={{ borderColor: "var(--hair, #d5cebe)" }}
          onClick={() => onAction?.("accept")}
        >
          Accept as recorded statement
        </button>
        <button
          data-testid="refusal-action-narrow"
          className="text-sm px-3 py-1.5 rounded border transition-colors hover:bg-gray-50"
          style={{ borderColor: "var(--hair, #d5cebe)" }}
          onClick={() => onAction?.("narrow")}
        >
          Narrow the objective
        </button>
        <button
          data-testid="refusal-action-lower"
          className="text-sm px-3 py-1.5 rounded border transition-colors hover:bg-gray-50"
          style={{ borderColor: "var(--hair, #d5cebe)" }}
          onClick={() => onAction?.("lower")}
        >
          Lower the standard
        </button>
      </div>

      <p
        data-testid="refusal-footer"
        className="text-xs italic"
        style={{ color: "var(--ink3, #5b6270)" }}
      >
        A refusal is the system keeping its promise.
      </p>
    </div>
  );
}
