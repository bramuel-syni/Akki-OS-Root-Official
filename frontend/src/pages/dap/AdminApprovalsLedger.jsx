/*
 * AdminApprovalsLedger.jsx — v2 OS · DAP LATEST view class 10 (working title).
 * R-101 + R-102 + R-103 + R-104 folded (approving authorities named). Turn 4 sub-slice 4h.
 * HONEST-GAP · SO §5.
 */
import React from "react";
export default function AdminApprovalsLedger() {
  return (
    <div data-testid="dap-approvals-ledger-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
      <header style={{marginBottom:32}}>
        <div data-testid="dap-approvals-ledger-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>DAP LATEST · Approvals Ledger</div>
        <h1 data-testid="dap-approvals-ledger-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Approvals Ledger</h1>
      </header>
      <section data-testid="dap-approvals-ledger-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
        <p style={{margin:"0 0 24px 0"}}>Every controlled request the tenant has raised, routed to its authorities, and the first-decision-wins outcome. Each row names the deciding authority, the reason banked, and the receipt trail.</p>
      </section>
      <section data-testid="dap-approvals-ledger-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
        <div data-testid="dap-approvals-ledger-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
        <div data-testid="dap-approvals-ledger-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Approvals routing backend + first-decision-wins ledger not yet wired. Design-of-record surface reveals R-104 authority routing (DAP-15 DEFAULT-class + DAP-17 one-act set/revoke standing approvals). Wire lands at PHASE 2 CP-TENANT-SEPARATION when RMS + DigiCow authorities are seated per R-104 (Fred Afune · Muthoni Kiarie · Samuel Kibacia · Vincent Kimani · Peninah Wanja).</div>
        <div data-testid="dap-approvals-ledger-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: R-104 banked STATE/DECISIONS.md · surface at pages/dap/AdminApprovalsLedger.jsx · route /dap/approvals-ledger.</div>
      </section>
    </div>
  );
}
