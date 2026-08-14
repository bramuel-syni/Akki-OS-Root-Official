import { useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import ConnectGpu from "@/components/ConnectGpu";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#f6f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI · PROGRAMME/TRACK-A</div>
        <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: "12px 0 24px 0", color: "#1c2b45" }}>
          The estate
        </h1>
        <p style={{ color: "#666", lineHeight: 1.6 }}>
          Owner surface for governed connections. Head to <a href="/register/connect/gpu" data-testid="link-connect-gpu" style={{ color: "#1c2b45" }}>Connect · GPU</a> to enter the AISCA VM credentials.
        </p>
        <ul style={{ color: "#666", lineHeight: 1.8, marginTop: 20, fontSize: 14 }}>
          <li><a href="/api/deliverables" data-testid="link-deliverables" style={{ color: "#1c2b45" }}>Deliverables snapshot API</a></li>
          <li><a href="/register/connect/gpu" data-testid="link-connect-gpu-2" style={{ color: "#1c2b45" }}>Connect · GPU (owner)</a></li>
        </ul>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register/connect/gpu" element={<ConnectGpu />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
