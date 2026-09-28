/*
 * AppsNew.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
 * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
 */
import React from "react";
export default function AppsNew() {
  return (
    <div data-testid="apps-new-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
      <header style={{marginBottom:32}}>
        <div data-testid="apps-new-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>3RD PARTY APPS · New</div>
        <h1 data-testid="apps-new-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>New</h1>
      </header>
      <section data-testid="apps-new-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
        <p style={{margin:"0 0 24px 0"}}>Newly available third-party apps. Each shows its admission requirements, its trust posture, and the authority admitting it.</p>
      </section>
      <section data-testid="apps-new-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
        <div data-testid="apps-new-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
        <div data-testid="apps-new-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for New not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
        <div data-testid="apps-new-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV apps.appsnew at App.js · surface at pages/os/AppsNew.jsx.</div>
      </section>
    </div>
  );
}
