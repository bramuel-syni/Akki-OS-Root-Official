import "@/App.css";
import { useEffect, useRef } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Registry from "@/components/Registry";
import DataShield from "@/components/DataShield";
import ThinkLab from "@/components/ThinkLab";
import Chat from "@/components/Chat";
import CostLedger from "@/components/CostLedger";
import ModelEcosystem from "@/components/ModelEcosystem";
import Governance from "@/components/Governance";
import Watch from "@/components/Watch";
import GreyMirror from "@/components/GreyMirror";
import AuditTrail from "@/components/AuditTrail";
import Training from "@/components/Training";
import SkillFiles from "@/components/SkillFiles";
import EvidenceRegister from "@/components/EvidenceRegister";
import CommissionWizard from "@/components/CommissionWizard";

/**
 * App.js — Wave G3 · corrected V8 LITERAL adoption
 * (owner re-eyeball verdict 2026-08-28T~07:15Z, banked in DECISIONS.md).
 *
 * Wave G2 shipped injected overlay cards containing backend / engineering
 * vocabulary (cluster names, engine versions, API paths, checkpoint IDs,
 * SSH-key notes). Owner verdict: "Stop reporting back end system/
 * engineering data on the surface." Wave G3 corrects:
 *
 *   Correction 1: no overlay cards, no visible bookkeeping attributes,
 *                 no backend/system/engineering vocabulary on any
 *                 user-facing surface.
 *   Correction 2: replace dummy stat numbers IN PLACE inside the
 *                 prototype's existing text nodes. Values are REAL
 *                 (derivable from live pod endpoints) or HONEST-EMPTY.
 *                 Never invent numbers; never leave the prototype's
 *                 dummy figure in place where it implies a measurement.
 *
 * The prototype ships byte-verbatim at `/v8_prototype.html` (sha256
 * e56871d0…). App.js hosts it in a same-origin iframe. On iframe load
 * (and on subsequent dc-runtime re-renders), the bridge runs the
 * substitution map defined in V8_SUBSTITUTIONS below — walking text
 * nodes only, mutating textContent in place, and never appending or
 * creating any element.
 */

function PortalIframe() {
  const iframeRef = useRef(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    let observer = null;
    let liveValues = { estateSources: null, estateTables: null };

    const applyAll = () => {
      const doc = iframe.contentDocument;
      if (!doc || !doc.body) return;
      applySubstitutions(doc, liveValues);
    };

    const onLoad = async () => {
      // Pull live values first; substitutions read from `liveValues`.
      try {
        const backend = process.env.REACT_APP_BACKEND_URL || "";
        const res = await fetch(`${backend}/api/registry/facts`);
        if (res.ok) {
          const facts = await res.json();
          if (facts && Array.isArray(facts.data_sources)) {
            liveValues.estateSources = facts.data_sources.length;
            // Aggregate table count across all connected sources (aggregate,
            // no PII, no ARNs — table_count is a plain integer).
            let tables = 0;
            for (const s of facts.data_sources) {
              if (typeof s.table_count === "number") tables += s.table_count;
            }
            liveValues.estateTables = tables;
          }
        }
      } catch (_) {
        // Silent — HONEST-EMPTY fallback fires when values are null.
      }

      // Give dc-runtime time for its first render pass.
      await new Promise((r) => setTimeout(r, 400));
      applyAll();

      // Watch for subsequent renders (tab switches, drawer opens, etc.)
      // and re-apply substitutions. Text-only, no structural mutation.
      try {
        const doc = iframe.contentDocument;
        if (doc && doc.body) {
          observer = new MutationObserver(() => {
            applyAll();
          });
          observer.observe(doc.body, {
            childList: true,
            characterData: true,
            subtree: true,
          });
        }
      } catch (_) {
        /* no-op */
      }
    };

    iframe.addEventListener("load", onLoad);
    return () => {
      iframe.removeEventListener("load", onLoad);
      if (observer) observer.disconnect();
    };
  }, []);

  return (
    <div
      data-testid="v8-portal-iframe-host"
      style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
    >
      <iframe
        ref={iframeRef}
        data-testid="v8-prototype-iframe"
        src="/v8_prototype.html"
        title="Akki OS · RMS AI"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}

/**
 * V8_SUBSTITUTIONS — the explicit slot substitution map.
 *
 * Each entry:
 *   signature  — text that identifies the slot inside the prototype's
 *                own DOM. Must exist in the served v8_prototype.html
 *                (fidelity-gate asserted).
 *   render(vals) — returns the replacement text for that slot given
 *                the live values object. Product language only.
 *                Returns null → leave the node untouched (dev signal;
 *                never used in production).
 *
 * Rules:
 *   • Substitutions replace ENTIRE text nodes matching the signature.
 *     No DOM element creation, no attribute setting.
 *   • If a live value is missing, the render function MUST return an
 *     HONEST-EMPTY sentence in product language (not the prototype's
 *     dummy figure, not a fabricated number).
 *   • Product-language only: no ARNs, no engine names, no API paths,
 *     no checkpoint IDs, no SSH/auth notes.
 */
const V8_SUBSTITUTIONS = [
  {
    // Registry surface · primary aside sentence (Step 0.5 inventory).
    // Prototype text (verbatim):
    //   "RMS AI holds 86.4 TB across 12 sources — 78% measured, with
    //    6 opportunities standing ready."
    signature: /^\s*RMS AI holds .* opportunities standing ready\.\s*$/,
    render: (v) => {
      if (v.estateSources == null && v.estateTables == null) {
        // Fully HONEST-EMPTY.
        return "RMS AI is not yet connected to a measured estate — no sources have been read and no size has been computed.";
      }
      const sources = v.estateSources ?? 0;
      const tables = v.estateTables ?? 0;
      const sourcesPhrase =
        sources === 0
          ? "no sources connected yet"
          : sources === 1
          ? "1 connected source"
          : `${sources} connected sources`;
      const tablesPhrase =
        tables === 0
          ? "no tables read yet"
          : tables === 1
          ? "with 1 table read"
          : `with ${tables.toLocaleString()} tables read`;
      return `RMS AI is reading ${sourcesPhrase} ${tablesPhrase} — size and completeness not yet measured across the estate.`;
    },
  },
  {
    // Registry census footer (Step 0.5 inventory).
    // Prototype text (verbatim):
    //   "Every figure on this page traces to a census measurement.
    //    First census May 12, 2026 · Census #4 (ran at 4.00am, 3/7/2026)
    //    by J. Mwangi · "
    // The trailing separator is followed by a clickable span
    // "How the estate is measured" that stays untouched.
    signature: /Every figure on this page traces to a census measurement\. First census May 12, 2026[^]*?J\. Mwangi \u00b7\s*$/,
    render: () =>
      "Every figure on this page traces to a census measurement. No census has been run yet \u00b7 ",
  },
];

function applySubstitutions(doc, vals) {
  const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
  let node;
  const toReplace = [];
  while ((node = walker.nextNode())) {
    const text = node.nodeValue;
    if (!text || text.length < 4) continue;
    for (const rule of V8_SUBSTITUTIONS) {
      if (rule.signature.test(text)) {
        const replacement = rule.render(vals);
        if (replacement != null && replacement !== text) {
          toReplace.push([node, replacement]);
        }
      }
    }
  }
  // Mutate outside the tree walk to avoid disturbing the walker.
  for (const [n, val] of toReplace) {
    n.nodeValue = val;
  }
}

function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f5f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI \u00b7 REGISTRY</div>
        <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: "12px 0 24px 0", color: "#1c2b45" }}>
          This route has been retired.
        </h1>
        <p style={{ color: "#666", lineHeight: 1.6 }} data-testid="not-found-notice">
          Return to <a href="/" style={{ color: "#1c2b45" }}>the portal</a>.
        </p>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PortalIframe />} />
          <Route path="/registry" element={<Registry />} />
          <Route path="/shield" element={<DataShield />} />
          <Route path="/thinklab" element={<ThinkLab />} />
          <Route path="/thinklab/:mode" element={<ThinkLab />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/cost-ledger" element={<CostLedger />} />
          <Route path="/models" element={<ModelEcosystem />} />
          <Route path="/governance" element={<Governance />} />
          <Route path="/watch" element={<Watch />} />
          <Route path="/grey-mirror" element={<GreyMirror />} />
          <Route path="/audit-trail" element={<AuditTrail />} />
          <Route path="/training" element={<Training />} />
          <Route path="/skill-files" element={<SkillFiles />} />
          <Route path="/evidence-register" element={<EvidenceRegister />} />
          <Route path="/commission" element={<CommissionWizard />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
