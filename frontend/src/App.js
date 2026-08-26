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

/**
 * App.js - Owner fixture drop 2026-08-14 shape:
 *   /       → Registry surface (three-tab shell + wizard drawer)
 *   * (any) → NotFound page
 * The standalone /register/connect/gpu route stays retired: dev-server
 * middleware ('spine-retired-routes') refuses HTTP 404 at the edge.
 */
function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f6f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
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
          <Route path="/" element={<Registry />} />
          <Route path="/shield" element={<DataShield />} />
          <Route path="/thinklab" element={<ThinkLab />} />
          <Route path="/thinklab/:mode" element={<ThinkLab />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/cost-ledger" element={<CostLedger />} />
          <Route path="/models" element={<ModelEcosystem />} />
          <Route path="/governance" element={<Governance />} />
          <Route path="/watch" element={<Watch />} />
          <Route path="/grey-mirror" element={<GreyMirror />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
