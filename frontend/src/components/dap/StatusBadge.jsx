import React from "react";

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

export default function StatusBadge({ status }) {
  const meta = STATUS_META[status] || { color: "var(--ink3)", bg: "rgba(27,31,39,.06)" };
  return (
    <span
      data-testid={`status-badge-${status?.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      className="inline-flex items-center text-xs font-medium px-2.5 py-1 rounded-full whitespace-nowrap"
      style={{ color: meta.color, background: meta.bg }}
    >
      {status}
    </span>
  );
}
