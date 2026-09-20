import React from "react";

/**
 * Transport failure state — per FE Integration Brief §6.
 * Oxblood left-border, raw error in monospace, standing reassurance.
 */
export default function TransportError({ error }) {
  return (
    <div
      data-testid="transport-error"
      className="border-l-4 rounded p-4 my-4"
      style={{ borderColor: "var(--oxblood, #b8395b)", background: "rgba(184,57,91,.04)" }}
    >
      <pre
        data-testid="transport-error-message"
        className="text-xs mb-2 whitespace-pre-wrap"
        style={{ fontFamily: "var(--mono, ui-monospace, Menlo, Consolas, monospace)", color: "var(--ink, #1b1f27)" }}
      >
        {error}
      </pre>
      <p className="text-sm italic" style={{ color: "var(--ink3, #5b6270)" }}>
        This is work done, not work lost — try again in a moment.
      </p>
    </div>
  );
}
