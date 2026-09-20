import React from "react";
import { useParams } from "react-router-dom";
import BackendPending from "@/components/shared/BackendPending";

/**
 * Extract Modes — DAP §4.1
 * 4 modes: raw, processed, finetune, skills
 * All backend pending (no request-submission endpoint exists).
 */

const MODES = {
  raw: {
    label: "Download Raw Data", title: "Download raw data",
    gate: "Highest level of review",
    sub: "The one option where you receive copies of the data itself. Because of that, it gets the most careful review.",
    rows: [
      ["What you send in", "Nothing — just your request"],
      ["What you get back", "Copies of the records you asked for"],
      ["How it is checked", "Every record is screened and redacted before anything is packaged"],
      ["Who has to sign off", "Digicow, whenever the data includes personal or confidential details"],
      ["What goes on the record", "Every record released, the redaction report, and who approved it"],
    ],
    practice: "What can be released depends on the rights Digicow holds and what the data contains. Redaction is not optional and cannot be skipped. Every record that leaves is listed individually.",
  },
  processed: {
    label: "Get Intelligence", title: "Get intelligence",
    gate: "Standard review",
    sub: "Tell Digicow what you want to find out. You get findings and analysis; the underlying records stay put.",
    rows: [
      ["What you send in", "A question or objective"],
      ["What you get back", "Findings and analysis — not the records they came from"],
      ["How it is checked", "Results only state what the data genuinely supports"],
      ["Who has to sign off", "Nobody, unless the data includes personal or confidential details"],
      ["What goes on the record", "Your question, the answer, and which records were used"],
    ],
    practice: "Which records were used is noted on your receipt, but the records themselves cannot be reconstructed from what you receive.",
  },
  finetune: {
    label: "Train a Model", title: "Train a model",
    gate: "Always reviewed",
    sub: "Your model comes to the data and trains here. You take the trained model away; the data never leaves Digicow.",
    rows: [
      ["What you send in", "Your base model, or one Digicow provides"],
      ["What you get back", "The trained model, with its usage rights attached"],
      ["How it is checked", "The model must meet the accuracy targets you set before training starts"],
      ["Who has to sign off", "Digicow, every time — because a trained model leaves with you"],
      ["What goes on the record", "What it was trained on, a fingerprint of the model, and your agreement"],
    ],
    practice: "Training happens on Digicow computers, next to the data. There is no option to move the data to your own systems.",
  },
  skills: {
    label: "Build a Skill", title: "Build a skill",
    gate: "Always reviewed",
    sub: "A skill is a reusable procedure, not a model. You take the file away; what it was built on stays here.",
    rows: [
      ["What you send in", "A description of what the skill should do"],
      ["What you get back", "A skill file you can run elsewhere"],
      ["How it is checked", "The file is fingerprinted and reviewed before release"],
      ["Who has to sign off", "Digicow, every time — because a file leaves with you"],
      ["What goes on the record", "A fingerprint of the file, which records were used, and your agreement"],
    ],
    practice: "The skill is developed against Digicow data and leaves as a file. The data it was developed on is listed on your receipt, not packed inside the file.",
  },
};

export default function ExtractModes() {
  const { mode } = useParams();
  const m = MODES[mode];

  if (!m) {
    return (
      <div className="max-w-5xl mx-auto px-8 py-10">
        <BackendPending surface="Extract mode not found" detail={`Mode "${mode}" is not a valid extract mode.`} />
      </div>
    );
  }

  return (
    <div data-testid={`extract-mode-${mode}`} className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="extract-mode-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
      >
        {m.title}
      </h1>
      <p className="text-xs font-medium mb-4" style={{ color: "var(--brass)" }}>{m.gate}</p>
      <p className="text-sm mb-6" style={{ color: "var(--ink2)" }}>{m.sub}</p>

      {/* How it works table */}
      <div className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
        {m.rows.map(([label, value], i) => (
          <div
            key={i}
            className={`flex items-start px-5 py-3 ${i < m.rows.length - 1 ? "border-b" : ""}`}
            style={{ borderColor: "var(--line)" }}
          >
            <p className="w-48 flex-shrink-0 text-xs font-medium" style={{ color: "var(--ink3)" }}>{label}</p>
            <p className="text-sm" style={{ color: "var(--ink)" }}>{value}</p>
          </div>
        ))}
      </div>

      {/* Practice note */}
      <div className="rounded-lg border-l-4 p-4 mb-6" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
        <p className="text-sm" style={{ color: "var(--ink2)" }}>{m.practice}</p>
      </div>

      {/* Backend pending — no submission endpoint */}
      <BackendPending
        surface={`${m.title} — request submission`}
        detail="The request-submission endpoint does not exist in the backend contract. No route accepts a new request of this type. This is the largest gap in the DAP (§4.2 of the FE Integration Brief)."
      />
    </div>
  );
}
