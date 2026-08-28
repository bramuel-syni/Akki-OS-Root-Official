import "@/App.css";
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
import { AkkiV8ShellLayout } from "./design/AkkiV8Shell";  // Wave G Step 2 · v8 shell mount · notes/prototype_inventory_v8.md §3

/**
 * App.js - Wave G Step 2 · v8 shell adopted (owner ruling 2026-08-28T~04:15Z).
 *
 * Every in-app route now renders inside AkkiV8ShellLayout — v8's top bar
 * (RMS AI wordmark on #0f1b33) + portal/app modes + 10-group NAV lattice
 * (WorkStudio · ThinkLab · Collab · Performance Management · Manage Estate
 * · Approvals · Build Your Resources · Your Resources · 3rd Party Apps ·
 * The Watch) + 4 tab pill row (Work · Build · 3rd Party Apps · Admin-right)
 * + 3 roles (Compliance Owner · Watch Officer · Operator).
 *
 *   /       → Portal mode (v8 landing) — click any NAV tile or pod-only tile
 *   /registry, /shield, /thinklab, /chat, /cost-ledger, /models,
 *   /governance, /watch, /grey-mirror, /audit-trail, /training,
 *   /skill-files, /evidence-register, /commission
 *          → App mode (slim header + <Outlet/> serving the pod component)
 *   *      → NotFound
 *
 * The v4 shell code at frontend/src/design/AkkiV4Shell* is retained as
 * invisible implementation only per owner rescission — v8 is authority.
 * Registry moves from `/` to `/registry` (matches v8-Docx:§12.1 line 234
 * "Manage Estate › Registry" and closes the pod-shell divergence for the
 * MUST_BE_LIVE_SPA_ROUTES `/registry` entry).
 *
 * The standalone /register/connect/gpu route stays retired: dev-server
 * middleware ('spine-retired-routes') refuses HTTP 404 at the edge.
 */
function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f5f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI · REGISTRY</div>
        <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: "12px 0 24px 0", color: "#1c2b45" }}>
          This route has been retired.
        </h1>
        <p style={{ color: "#666", lineHeight: 1.6 }} data-testid="not-found-notice">
          Return to <a href="/" style={{ color: "#1c2b45" }}>the Registry</a>.
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
          <Route element={<AkkiV8ShellLayout />}>
            <Route path="/" element={null} />
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
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
