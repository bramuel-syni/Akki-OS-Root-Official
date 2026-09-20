import React from "react";

/**
 * 403 Allowlist block — per FE Integration Brief §1.3.
 * Full-surface state with the backend's sentence verbatim.
 * No retry button — there is no token gate to satisfy.
 */
export default function AllowlistBlock() {
  return (
    <div
      data-testid="allowlist-block"
      className="min-h-screen flex items-center justify-center px-6"
      style={{ background: "var(--paper, #f5f2ea)" }}
    >
      <p
        data-testid="allowlist-block-message"
        className="text-base"
        style={{ color: "var(--ink, #1b1f27)", fontFamily: "var(--body, Söhne, Helvetica Neue, Arial, sans-serif)" }}
      >
        This surface answers allowlisted addresses only.
      </p>
    </div>
  );
}
