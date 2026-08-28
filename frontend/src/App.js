import "@/App.css";
import { useEffect } from "react";
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
import Training from "@/components/Training";  // W11 R4.1 · Doc 17
import SkillFiles from "@/components/SkillFiles";  // W11 B CP4 · Doc 18 A18.7
import EvidenceRegister from "@/components/EvidenceRegister";  // W11 B CP6 · Doc 19B §19B.4-6
import CommissionWizard from "@/components/CommissionWizard";  // W11 R3 · Canon 5 §14

/**
 * App.js — Wave G2 · V8 LITERAL adoption (owner ruling 2026-08-28T~06:00Z).
 *
 * Owner verdict on Wave G v8 shell (interpretation-authored):
 *   "What you have build is totally out of touch with the HTML."
 *
 * New method ruling (this file implements):
 *   The v8 prototype ships VERBATIM as a served static asset at
 *   `public/v8_prototype.html`. Root `/` navigates the browser to that
 *   file. The prototype boots its own dc-runtime + main bundle + template
 *   whole-cloth — zero re-authoring, byte-identity gate at
 *   `test_wave_g_v8_shell_port.py`. Interpretation-authored files
 *   (`design/AkkiV8Shell.jsx`, `design/akkiv8_design_system.js`) are
 *   BANNED and deleted.
 *
 * Integration shape (b) per owner ruling item 4: "serving the extracted
 * app shell directly with our data injected". Judgment banked at
 * `phase0/drill_receipts/20260828T060000Z_wave_g2_v8_literal_extraction.log`.
 *
 * Existing pod component routes remain URL-accessible for deep-linking:
 *   /registry, /shield, /thinklab, /thinklab/:mode, /chat, /cost-ledger,
 *   /models, /governance, /watch, /grey-mirror, /audit-trail, /training,
 *   /skill-files, /evidence-register, /commission
 *
 * Mounting pod-live-data INSIDE the prototype's own containers (real
 * data as TEXT-NODE substitution inside prototype structures) is a
 * follow-on and is EXTENSION-PENDING-OWNER-EYEBALL — deferred until
 * owner eyeballs the literal-adopted portal.
 */

function PortalRedirect() {
  useEffect(() => {
    // Full-page navigation to the served static file. The prototype
    // boots its own dc-runtime + main bundle + template — this React
    // app steps aside for `/`.
    window.location.replace("/v8_prototype.html");
  }, []);
  return (
    <div
      data-testid="v8-portal-redirect"
      style={{
        minHeight: "100vh",
        background: "#0f1b33",
        color: "#f5f2ea",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "ui-monospace,Menlo,Consolas,monospace",
        fontSize: 12,
        letterSpacing: ".14em",
        textTransform: "uppercase",
      }}
    >
      Loading Akki OS · RMS AI…
    </div>
  );
}

function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f5f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI · REGISTRY</div>
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
          <Route path="/" element={<PortalRedirect />} />
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
          <Route path="/training" element={<Training />} />{/* W11 R4.1 · Doc 17 */}
          <Route path="/skill-files" element={<SkillFiles />} />{/* W11 B CP4 · Doc 18 A18.7 */}
          <Route path="/evidence-register" element={<EvidenceRegister />} />{/* W11 B CP6 · Doc 19B §19B.4-6 */}
          <Route path="/commission" element={<CommissionWizard />} />{/* W11 R3 · Canon 5 §14 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
