import React from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Lock, Shield, FileText } from "lucide-react";

/**
 * Data Estates — per-estate detail view.
 * Matches the ESTATES map from the DAP reference HTML.
 */

const ESTATES = {
  audio: {
    label: "Audio", title: "Audio", tb: 41.2, pct: 48, fill: "var(--blue, #16274a)",
    stats: [["How much", "41.2 TB · 48% of all Digicow data"], ["What is in it", "287,800 recorded calls · 61,400 hours"], ["Where it comes from", "Digicow customer service lines"], ["Languages", "English · Swahili · Sheng"], ["Collected", "March 2019 to July 2026"], ["Quality", "Phone-call audio · 62% checked against the original"], ["Personal details", "Names and account numbers, spoken · every request needs sign-off"], ["Open to you", "6.1 TB now · 18.4 TB with sign-off · 16.7 TB not available"]],
    custody: "These are real conversations, and people say their names and account numbers out loud. That cannot be edited out field by field, so every request that uses this data needs Digicow sign-off first.",
    avail: { standing: "6.1 TB", approval: "18.4 TB", closed: "16.7 TB" },
    notes: [
      { tag: "The biggest set", color: "var(--blue)", text: "41.2 TB — almost half of everything Digicow holds, and the richest thing you could train on. 16.7 TB of it is internal-only and not available to anyone outside Digicow." },
      { tag: "Why sign-off is always needed", color: "var(--oxblood)", text: "Callers say their names and account numbers. There is no neat field to strip, so Digicow reviews every request that touches these recordings." },
      { tag: "No raw copies", color: "var(--ink3)", text: "You can train on it or get findings from it. You cannot download the recordings themselves." },
      { tag: "How much has been checked", color: "var(--brass)", text: "62% has been checked against the original recordings. The rest has been processed but not verified, so treat results built on it with a little more care." }
    ],
    ops: { connect: "approval", processed: "approval", finetune: "approval", skills: "approval", raw: "closed" }
  },
  text: {
    label: "Text & Documents", title: "Text & Documents", tb: 9.6, pct: 11, fill: "#4b6a9b",
    stats: [["How much", "9.6 TB · 11% of all Digicow data"], ["What is in it", "9,140 complaint files · 2.1M pages"], ["Where it comes from", "Digicow written complaints archive"], ["Languages", "English · Swahili"], ["Collected", "January 2019 to June 2026"], ["Quality", "88% typed, 12% scanned · 11% checked against the original"], ["Personal details", "Complainants named in part of the set · cleared share has none"], ["Open to you", "3.4 TB now · 4.1 TB with sign-off · 2.1 TB not available"]],
    custody: "Part of this set is cleared for outside use and contains no personal details — that part is open to you now. The rest names the people who complained, so using it needs Digicow sign-off.",
    avail: { standing: "3.4 TB", approval: "4.1 TB", closed: "2.1 TB" },
    notes: [
      { tag: "Your easiest start", color: "var(--sage)", text: "3.4 TB is open to you today: the cleared share, with no personal details in it. This is also the only set where downloading raw copies is possible at all." },
      { tag: "Mind the quality", color: "var(--brass)", text: "12% is scanned paper rather than typed text, and only 11% has been checked against the originals. Quality will limit you here more than permissions will." },
      { tag: "The rest names people", color: "var(--oxblood)", text: "Complainants are named in the remaining files. Any request reaching into that part goes to Digicow for sign-off, however small." }
    ],
    ops: { connect: "standing", processed: "standing", finetune: "approval", skills: "approval", raw: "approval" }
  },
  records: {
    label: "Records", title: "Records", tb: 20.2, pct: 23, fill: "#7d93b6",
    stats: [["How much", "20.2 TB · 23% of all Digicow data"], ["What is in it", "Core banking records · 14 groups of fields"], ["Where it comes from", "Digicow core banking system"], ["Languages", "English"], ["Collected", "March 2019 to July 2026"], ["Quality", "Complete records · 94% checked"], ["Personal details", "Account-level personal and financial · marked confidential"], ["Open to you", "4.6 TB with sign-off · 15.6 TB not available"]],
    custody: "Account-level personal and financial information, marked confidential by Digicow. It can be queried and analysed with sign-off, but it cannot be used to train a model and cannot be downloaded.",
    avail: { standing: "—", approval: "4.6 TB", closed: "15.6 TB" },
    notes: [
      { tag: "Two firm limits", color: "var(--oxblood)", text: "No model training and no raw downloads from this set. These are fixed rules, not settings that can be switched on request." },
      { tag: "What you can do", color: "var(--brass)", text: "4.6 TB can be queried or analysed for findings with Digicow sign-off. The remaining 15.6 TB is not available." },
      { tag: "The best-kept data", color: "var(--blue)", text: "Complete records, 94% checked — the most reliable set Digicow holds, and the most tightly held." }
    ],
    ops: { connect: "approval", processed: "approval", finetune: "closed", skills: "closed", raw: "closed" }
  },
  logs: {
    label: "Logs", title: "Logs", tb: 5.8, pct: 7, fill: "#9fb0cc",
    stats: [["How much", "5.8 TB · 7% of all Digicow data"], ["What is in it", "System, access and workflow logs"], ["Where it comes from", "Digicow platform logs"], ["Languages", "English"], ["Collected", "June 2020 to today"], ["Quality", "Machine-written · clean"], ["Personal details", "None · user IDs removed as the data is read"], ["Open to you", "2.2 TB now · 1.9 TB with sign-off · 1.7 TB not available"]],
    custody: "No personal details by design, though log lines carry user IDs. Those IDs are removed automatically as the data is read, so you never see them.",
    avail: { standing: "2.2 TB", approval: "1.9 TB", closed: "1.7 TB" },
    notes: [
      { tag: "Open and tidy", color: "var(--sage)", text: "2.2 TB is open to you now. Machine-written and clean — the easiest set to query if you want to understand how the platform behaves." },
      { tag: "IDs, not identities", color: "var(--brass)", text: "No personal details, but user IDs appear in the lines. They are removed as the data is read, not afterwards on request." },
      { tag: "Still growing", color: "var(--ink3)", text: "Collected since June 2020 and still being written. Anything you take is a snapshot of a moving record." }
    ],
    ops: { connect: "standing", processed: "standing", finetune: "approval", skills: "approval", raw: "approval" }
  },
  messages: {
    label: "Messages", title: "Messages", tb: 4.2, pct: 5, fill: "#b9c5d8",
    stats: [["How much", "4.2 TB · 5% of all Digicow data"], ["What is in it", "1.4M email threads"], ["Where it comes from", "Digicow email archive"], ["Languages", "English · Swahili"], ["Collected", "January 2019 to July 2026"], ["Quality", "Patchy · 6 fields too thin to train on"], ["Personal details", "Named people inside and outside Digicow · never asked about outside use"], ["Open to you", "1.2 TB with sign-off · 3.0 TB not available"]],
    custody: "Correspondence between named people inside and outside Digicow. Those people were never asked about outside use, so most of this set is not available.",
    avail: { standing: "—", approval: "1.2 TB", closed: "3.0 TB" },
    notes: [
      { tag: "Mostly off limits", color: "var(--oxblood)", text: "3.0 TB of 4.2 TB is not available. The people in these emails were never asked about outside use, and that cannot be fixed after the fact." },
      { tag: "Outsiders are in it", color: "var(--brass)", text: "Many threads involve people outside Digicow entirely. Digicow cannot grant access to their words, which is why sign-off here is narrow." },
      { tag: "Thin material", color: "var(--ink3)", text: "Patchy fields throughout, and six were flagged as too thin to train on. Small volume, low yield." }
    ],
    ops: { connect: "approval", processed: "approval", finetune: "closed", skills: "closed", raw: "closed" }
  },
};

const OP_LABELS = {
  standing: { label: "Open to you", color: "var(--sage)", bg: "rgba(29,122,110,.12)" },
  approval: { label: "Needs sign-off", color: "var(--brass)", bg: "rgba(176,141,46,.14)" },
  closed: { label: "Not available", color: "var(--ink3)", bg: "rgba(27,31,39,.06)" },
};

const OPS_LIST = [
  { key: "connect", name: "Query it from your workspace" },
  { key: "processed", name: "Get intelligence from it" },
  { key: "finetune", name: "Train your model on it" },
  { key: "skills", name: "Build a skill on it" },
  { key: "raw", name: "Download the raw data" },
];

export default function DataEstates() {
  const { estateId } = useParams();
  const estate = ESTATES[estateId];

  if (!estate) {
    return (
      <div className="max-w-5xl mx-auto px-8 py-10">
        <Link to="/dap" className="text-sm hover:underline mb-4 inline-flex items-center gap-1" style={{ color: "var(--ink3)" }}>
          <ArrowLeft size={14} /> Back to portal
        </Link>
        <p className="text-sm mt-4" style={{ color: "var(--ink2)" }}>Estate not found.</p>
      </div>
    );
  }

  return (
    <div data-testid={`data-estate-${estateId}`} className="max-w-5xl mx-auto px-8 py-10">
      <Link to="/dap" className="text-sm hover:underline mb-4 inline-flex items-center gap-1" style={{ color: "var(--ink3)" }}>
        <ArrowLeft size={14} /> Back to portal
      </Link>

      <div className="flex items-start justify-between mt-4 mb-6">
        <div>
          <h1
            data-testid="estate-title"
            className="text-2xl font-semibold"
            style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
          >
            {estate.title}
          </h1>
          <p className="text-sm mt-1" style={{ color: "var(--ink3)" }}>{estate.tb} TB · {estate.pct}% of the estate</p>
        </div>
        <div className="w-14 h-14 rounded-lg flex items-center justify-center" style={{ background: `${estate.fill}18` }}>
          <span className="text-lg font-bold" style={{ color: estate.fill }}>{estate.pct}%</span>
        </div>
      </div>

      {/* Stats table */}
      <div className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
        {estate.stats.map(([label, value], i) => (
          <div
            key={i}
            data-testid={`estate-stat-${i}`}
            className={`flex items-start px-5 py-3 ${i < estate.stats.length - 1 ? "border-b" : ""}`}
            style={{ borderColor: "var(--line)" }}
          >
            <p className="w-40 flex-shrink-0 text-xs font-medium" style={{ color: "var(--ink3)" }}>{label}</p>
            <p className="text-sm" style={{ color: "var(--ink)" }}>{value}</p>
          </div>
        ))}
      </div>

      {/* Custody note */}
      <div className="rounded-lg border-l-4 p-4 mb-6" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
        <p className="text-sm" style={{ color: "var(--ink2)" }}>{estate.custody}</p>
      </div>

      {/* Availability */}
      <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>Availability</h2>
      <div className="grid grid-cols-3 gap-3 mb-6">
        {[["standing", estate.avail.standing], ["approval", estate.avail.approval], ["closed", estate.avail.closed]].map(([k, v]) => {
          const meta = OP_LABELS[k];
          return (
            <div key={k} className="rounded-lg border p-3" style={{ borderColor: meta.color, background: meta.bg }}>
              <p className="text-[10px] font-medium mb-0.5" style={{ color: meta.color }}>{meta.label}</p>
              <p className="text-lg font-semibold" style={{ color: "var(--ink)" }}>{v}</p>
            </div>
          );
        })}
      </div>

      {/* Operations */}
      <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>What you can do</h2>
      <div className="space-y-2 mb-6">
        {OPS_LIST.map((op) => {
          const gate = estate.ops[op.key];
          const meta = OP_LABELS[gate];
          return (
            <div
              key={op.key}
              data-testid={`estate-op-${op.key}`}
              className="flex items-center justify-between rounded-lg border p-3"
              style={{ borderColor: "var(--line)", background: "white" }}
            >
              <div className="flex items-center gap-2">
                {gate === "closed" ? <Lock size={14} style={{ color: "var(--ink3)" }} /> : <FileText size={14} style={{ color: meta.color }} />}
                <span className="text-sm" style={{ color: "var(--ink)" }}>{op.name}</span>
              </div>
              <span
                className="text-[10px] font-medium px-2 py-0.5 rounded-full"
                style={{ color: meta.color, background: meta.bg }}
              >
                {meta.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Notes */}
      <div className="space-y-3">
        {estate.notes.map((note, i) => (
          <div
            key={i}
            data-testid={`estate-note-${i}`}
            className="flex gap-3 items-start rounded-lg p-4"
            style={{ background: "var(--surface)" }}
          >
            <span className="text-[10px] font-medium px-2 py-0.5 rounded whitespace-nowrap" style={{ color: note.color, background: `${note.color}14` }}>
              {note.tag}
            </span>
            <p className="text-sm" style={{ color: "var(--ink2)" }}>{note.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
