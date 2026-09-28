import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Database, Shield, FileText } from "lucide-react";

/**
 * DAP Landing — the portal home.
 * Shows the data estate overview matching the DAP reference HTML.
 */

const ESTATES = {
  audio: { label: "Audio", tb: 41.2, pct: 48, fill: "var(--blue, #16274a)", standing: "6.1 TB", approval: "18.4 TB", closed: "16.7 TB" },
  text: { label: "Text & Documents", tb: 9.6, pct: 11, fill: "#4b6a9b", standing: "3.4 TB", approval: "4.1 TB", closed: "2.1 TB" },
  records: { label: "Records", tb: 20.2, pct: 23, fill: "#7d93b6", standing: "—", approval: "4.6 TB", closed: "15.6 TB" },
  logs: { label: "Logs", tb: 5.8, pct: 7, fill: "#9fb0cc", standing: "2.2 TB", approval: "1.9 TB", closed: "1.7 TB" },
  messages: { label: "Messages", tb: 4.2, pct: 5, fill: "#b9c5d8", standing: "—", approval: "1.2 TB", closed: "3.0 TB" },
};

const NOTES = [
  { tag: "What needs sign-off", color: "var(--brass, #b08d2e)", text: "30.2 TB more can be used if Digicow approves the specific request. Anything containing personal or confidential details falls here — 41% of all the data does." },
  { tag: "The biggest set", color: "var(--blue, #16274a)", text: "Call recordings are 41.2 TB — almost half of everything here, and the richest thing you could train on. 16.7 TB of that is internal-only and not available to anyone outside Digicow." },
  { tag: "What you can use today", color: "var(--sage, #1d7a6e)", text: "11.7 TB is open to you now, no sign-off needed: cleared documents, logs, and a de-identified slice of the call recordings." },
  { tag: "Looking is free", color: "var(--ink3, #5b6270)", text: "Nothing on this page is the data itself. You are reading a summary, and browsing it is not recorded beyond a simple access log." },
];

export default function DAPLanding() {
  const totalTB = Object.values(ESTATES).reduce((s, e) => s + e.tb, 0);

  return (
    <div data-testid="dap-landing" className="max-w-5xl mx-auto px-8 py-10">
      {/* Hero */}
      <div className="mb-10">
        <h1
          data-testid="dap-landing-title"
          className="text-2xl font-semibold mb-2"
          style={{ color: "var(--ink, #1b1f27)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
        >
          Data Access Portal
        </h1>
        <p className="text-sm" style={{ color: "var(--ink2, #3d4350)" }}>
          Digicow holds {totalTB.toFixed(1)} TB of data across five estates. This portal shows what is available to you,
          what needs sign-off, and how to request what you need.
        </p>
      </div>

      {/* Estate bar chart */}
      <div data-testid="dap-estate-chart" className="mb-8">
        <div className="flex rounded-lg overflow-hidden h-10 mb-3">
          {Object.entries(ESTATES).map(([key, e]) => (
            <div
              key={key}
              data-testid={`estate-bar-${key}`}
              className="flex items-center justify-center text-[10px] font-medium text-white transition-all"
              style={{ width: `${e.pct}%`, background: e.fill, minWidth: e.pct > 3 ? "auto" : "2px" }}
              title={`${e.label}: ${e.tb} TB (${e.pct}%)`}
            >
              {e.pct > 8 ? `${e.label}` : ""}
            </div>
          ))}
        </div>
        <div className="flex flex-wrap gap-4 text-xs" style={{ color: "var(--ink2, #3d4350)" }}>
          {Object.entries(ESTATES).map(([key, e]) => (
            <div key={key} className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-sm inline-block" style={{ background: e.fill }} />
              <span>{e.label} · {e.tb} TB · {e.pct}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* Availability summary */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div
          data-testid="dap-avail-standing"
          className="rounded-lg p-4 border"
          style={{ borderColor: "var(--sage, #1d7a6e)", background: "rgba(29,122,110,.06)" }}
        >
          <p className="text-xs font-medium mb-1" style={{ color: "var(--sage, #1d7a6e)" }}>Open to you</p>
          <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>11.7 TB</p>
          <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>No sign-off needed</p>
        </div>
        <div
          data-testid="dap-avail-approval"
          className="rounded-lg p-4 border"
          style={{ borderColor: "var(--brass, #b08d2e)", background: "rgba(176,141,46,.06)" }}
        >
          <p className="text-xs font-medium mb-1" style={{ color: "var(--brass, #b08d2e)" }}>Needs sign-off</p>
          <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>30.2 TB</p>
          <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>Digicow reviews the request</p>
        </div>
        <div
          data-testid="dap-avail-closed"
          className="rounded-lg p-4 border"
          style={{ borderColor: "var(--ink3, #5b6270)", background: "rgba(27,31,39,.04)" }}
        >
          <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3, #5b6270)" }}>Not available</p>
          <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>39.1 TB</p>
          <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>Internal-only or restricted</p>
        </div>
      </div>

      {/* Data Estates grid */}
      <h2
        className="text-lg font-semibold mb-4"
        style={{ color: "var(--ink, #1b1f27)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
      >
        Data Estates
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
        {Object.entries(ESTATES).map(([key, e]) => (
          <Link
            key={key}
            to={`/dap/estates/${key}`}
            data-testid={`estate-card-${key}`}
            className="rounded-lg border p-5 transition-all hover:shadow-sm group"
            style={{ borderColor: "var(--line, #e4dfd3)", background: "white" }}
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm font-medium" style={{ color: "var(--ink, #1b1f27)" }}>{e.label}</p>
                <p className="text-2xl font-semibold mt-1" style={{ color: "var(--ink, #1b1f27)" }}>{e.tb} TB</p>
              </div>
              <span
                className="text-xs px-2 py-0.5 rounded-full"
                style={{ color: e.fill, background: `${e.fill}18` }}
              >
                {e.pct}%
              </span>
            </div>
            <div className="flex gap-3 text-[11px] mb-2" style={{ color: "var(--ink3, #5b6270)" }}>
              {e.standing !== "—" && <span style={{ color: "var(--sage)" }}>Open: {e.standing}</span>}
              <span style={{ color: "var(--brass)" }}>Sign-off: {e.approval}</span>
              <span>Closed: {e.closed}</span>
            </div>
            <ArrowRight
              size={14}
              className="mt-2 opacity-0 group-hover:opacity-60 transition-opacity"
              style={{ color: "var(--ink3)" }}
            />
          </Link>
        ))}
      </div>

      {/* Notes */}
      <div className="space-y-3 mb-10">
        {NOTES.map((note, i) => (
          <div
            key={i}
            data-testid={`dap-note-${i}`}
            className="flex gap-3 items-start rounded-lg p-4"
            style={{ background: "var(--surface, #f0ece1)" }}
          >
            <span
              className="text-[10px] font-medium px-2 py-0.5 rounded whitespace-nowrap"
              style={{ color: note.color, background: `${note.color}14` }}
            >
              {note.tag}
            </span>
            <p className="text-sm" style={{ color: "var(--ink2, #3d4350)" }}>{note.text}</p>
          </div>
        ))}
      </div>

      {/* Quick links */}
      <div className="grid grid-cols-3 gap-4">
        <Link
          to="/dap/resources/compute"
          data-testid="dap-quick-resources"
          className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
          style={{ borderColor: "var(--line, #e4dfd3)" }}
        >
          <Database size={18} style={{ color: "var(--blue)" }} />
          <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Available Resources</span>
        </Link>
        <Link
          to="/dap/governance/policies"
          data-testid="dap-quick-governance"
          className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
          style={{ borderColor: "var(--line, #e4dfd3)" }}
        >
          <Shield size={18} style={{ color: "var(--sage)" }} />
          <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Data Governance</span>
        </Link>
        <Link
          to="/dap/requests"
          data-testid="dap-quick-requests"
          className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
          style={{ borderColor: "var(--line, #e4dfd3)" }}
        >
          <FileText size={18} style={{ color: "var(--brass)" }} />
          <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Your Requests</span>
        </Link>
      </div>
    </div>
  );
}
