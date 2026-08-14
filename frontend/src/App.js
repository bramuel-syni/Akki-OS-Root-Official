import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AdminSurface from "@/components/AdminSurface";

/**
 * App.js — Owner stop-order 2026-08-14 shape:
 *   /       → Admin surface (tile grid + detail card)
 *   * (any) → NotFound page
 * The standalone /register/connect/gpu route is retired; the dev-server
 * middleware ('spine-retired-routes') refuses HTTP 404 at the edge before
 * this router is reached.
 */
function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f6f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI · PROGRAMME/TRACK-A</div>
        <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: "12px 0 24px 0", color: "#1c2b45" }}>
          This route has been retired.
        </h1>
        <p style={{ color: "#666", lineHeight: 1.6 }} data-testid="not-found-notice">
          Return to <a href="/" style={{ color: "#1c2b45" }}>the estate</a>.
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
          <Route path="/" element={<AdminSurface />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
