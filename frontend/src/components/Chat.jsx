import React, { useState } from "react";
import { Link } from "react-router-dom";

/**
 * Chat.jsx — W5 CP4 · Governed chat surface.
 *
 * Owner Order 2026-08-25 · one question / one answer. Every submit
 * transits the LLM chokepoint (purpose=chat.governed_answer). Response
 * carries: answer + full metering + model provenance line. Refusals
 * render verbatim (A8-Q3).
 *
 * v7 palette · REFERENCE-NOT-COPY on the receipt id.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens.
const paper = "#f5f2ea";
const surface = "#ffffff";
const surface2 = "#f0ebe1";
const ink = "#1b1f27";
const ink2 = "#3a3f4a";
const ink3 = "#7a7f8a";
const line = "#e4dccf";
const blue = "#16274a";
const sage = "#1d7a6e";
const oxblood = "#8a2a44";
const oxblood2 = "#b8395b";
const brass = "#b08d2e";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';


export default function Chat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const submit = async () => {
    if (!question.trim() || busy) return;
    setBusy(true);
    setResponse(null);
    setError(null);
    try {
      const r = await fetch(`${BACKEND_URL}/api/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const body = await r.json();
      setResponse(body);
    } catch (exc) {
      setError(String(exc));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px",
                  fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
      <div style={{ maxWidth: 780, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3,
                      textTransform: "uppercase" }}>
          AKKI · CHAT
        </div>
        <div style={{ display: "flex", justifyContent: "space-between",
                      alignItems: "baseline" }}>
          <h1 style={{ fontFamily: head, fontSize: 42, margin: "10px 0 20px 0",
                       color: blue }}>
            One question. One answer.
          </h1>
          <Link to="/" style={{ color: ink3, fontSize: 12, textDecoration: "none" }}>
            ← Registry
          </Link>
        </div>
        <p style={{ color: ink2, lineHeight: 1.6, fontSize: 14, marginBottom: 24 }}>
          Every submit crosses the governed chokepoint. The receipt is the
          record. The model that answered is on the receipt.
        </p>

        <div style={{ background: surface, padding: "22px 24px",
                      border: `1px solid ${line}`, borderRadius: 10 }}>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                        textTransform: "uppercase", fontWeight: 600,
                        marginBottom: 10 }}>
            Ask
          </div>
          <textarea data-testid="chat-question-input"
                    value={question}
                    onChange={e => setQuestion(e.target.value)}
                    placeholder="Ask a governed question…"
                    rows={4}
                    style={{ width: "100%", padding: "10px 12px",
                             fontFamily: "ui-sans-serif, system-ui, sans-serif",
                             fontSize: 14, color: ink,
                             background: paper, border: `1px solid ${line}`,
                             borderRadius: 6, resize: "vertical" }} />
          <button data-testid="chat-submit-button"
                  onClick={submit}
                  disabled={busy || !question.trim()}
                  style={{ marginTop: 14, padding: "9px 18px",
                           background: busy ? ink3 : blue, color: "#fff",
                           border: `1px solid ${blue}`, borderRadius: 5,
                           cursor: busy ? "wait" : "pointer",
                           fontSize: 13, fontWeight: 700 }}>
            {busy ? "Asking…" : "Ask"}
          </button>
        </div>

        {error && (
          <div data-testid="chat-network-error"
               style={{ marginTop: 20, padding: "14px 18px", background: surface,
                        borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
                        border: `1px solid ${line}` }}>
            <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
                          textTransform: "uppercase", fontWeight: 700 }}>
              Network refused
            </div>
            <div style={{ fontSize: 12, color: ink, marginTop: 6,
                          fontFamily: "ui-monospace, Menlo, monospace" }}>
              {error}
            </div>
          </div>
        )}

        {response && response.refused && (
          <div data-testid="chat-refusal-card"
               style={{ marginTop: 20, padding: "18px 22px", background: surface,
                        borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
                        border: `1px solid ${line}` }}>
            <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
                          textTransform: "uppercase", fontWeight: 700 }}>
              Shield refused
            </div>
            <div style={{ fontSize: 13, color: ink, marginTop: 8,
                          fontFamily: "ui-monospace, Menlo, monospace",
                          background: "#f7ecea", padding: "10px 12px",
                          borderRadius: 4 }}>
              {response.refusal_reason}
            </div>
            <div style={{ fontSize: 11, color: ink3, marginTop: 8,
                          fontStyle: "italic" }}>
              A8-Q3 · verbatim refusal, never a smoothed answer.
            </div>
          </div>
        )}

        {response && !response.refused && (
          <div data-testid="chat-answer-card"
               style={{ marginTop: 20, padding: "22px 24px", background: surface,
                        border: `1px solid ${line}`, borderRadius: 10 }}>
            <div style={{ display: "flex", justifyContent: "space-between",
                          alignItems: "baseline", marginBottom: 12 }}>
              <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
                            textTransform: "uppercase", fontWeight: 700 }}>
                Answer
              </div>
              <div style={{ fontSize: 10, color: ink3,
                            fontFamily: "ui-monospace, Menlo, monospace" }}
                   data-testid="chat-provenance">
                Answered by <b style={{ color: ink }}>{response.model_id}</b> via {response.provider} ·{" "}
                receipt <b>{response.receipt_id}</b>
              </div>
            </div>
            <div style={{ fontSize: 15, color: ink, lineHeight: 1.7,
                          fontFamily: head }}>
              {response.answer}
            </div>
            <div style={{ marginTop: 14, paddingTop: 12,
                          borderTop: `1px solid ${line}`,
                          fontSize: 11, color: ink3,
                          fontFamily: "ui-monospace, Menlo, monospace",
                          display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
                          gap: 12 }}>
              <div>tokens_in · <b>{response.tokens_in}</b></div>
              <div>tokens_out · <b>{response.tokens_out}</b></div>
              <div>latency_ms · <b>{response.latency_ms}</b></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
