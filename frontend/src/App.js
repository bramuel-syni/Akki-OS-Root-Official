import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

/* ── DAP Portal (Track 1) ─────────────────────────────── */
import DAPLayout from "@/pages/dap/DAPLayout";
import DAPLanding from "@/pages/dap/DAPLanding";
import AvailableResources from "@/pages/dap/AvailableResources";
import DataGovernance from "@/pages/dap/DataGovernance";
import RequestLifecycle from "@/pages/dap/RequestLifecycle";
import DataEstates from "@/pages/dap/DataEstates";
import ExtractModes from "@/pages/dap/ExtractModes";
import ConnectResources from "@/pages/dap/ConnectResources";

/* ── OS Prototype v2 (Track 2) ────────────────────────── */
import OSPrototype from "@/pages/os/OSPrototype";

/**
 * App.js — Wave FE-INTEGRATION · DAP Portal + OS Prototype v2 React surfaces.
 *
 * Two tracks mounted under the same React router:
 *   Track 1 — /dap/*  : The Data Access Portal (full build)
 *   Track 2 — /       : The OS Prototype v2 (iframe-wrapped standalone HTML)
 *
 * The OS Prototype route preserves the existing iframe approach from prior
 * waves (PortalIframe / v8_prototype.html), ensuring backward compatibility
 * with the substitution engine and all existing harness probes.
 */

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* Track 2 — OS Prototype v2 at root */}
          <Route path="/" element={<OSPrototype />} />

          {/* Track 1 — DAP Portal */}
          <Route path="/dap" element={<DAPLayout />}>
            <Route index element={<DAPLanding />} />

            {/* Extract modes */}
            <Route path="extract/:mode" element={<ExtractModes />} />

            {/* Available Resources */}
            <Route path="resources/:tab" element={<AvailableResources />} />

            {/* Data Governance */}
            <Route path="governance/:tab" element={<DataGovernance />} />

            {/* Connect Resources */}
            <Route path="connect/:tab" element={<ConnectResources />} />

            {/* Request Lifecycle */}
            <Route path="requests" element={<RequestLifecycle />} />

            {/* Data Estates */}
            <Route path="estates/:estateId" element={<DataEstates />} />

            {/* Catch-all within DAP */}
            <Route path="*" element={<Navigate to="/dap" replace />} />
          </Route>

          {/* Fallback: anything else goes to OS prototype */}
          <Route path="*" element={<OSPrototype />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
