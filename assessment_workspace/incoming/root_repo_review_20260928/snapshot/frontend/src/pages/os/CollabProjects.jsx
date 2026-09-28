/*
 * CollabProjects.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
 * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
 */
import React from "react";
export default function CollabProjects() {
  return (
    <div data-testid="collab-projects-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
      <header style={{marginBottom:32}}>
        <div data-testid="collab-projects-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>COLLAB · Projects/Tasks</div>
        <h1 data-testid="collab-projects-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Projects/Tasks</h1>
      </header>
      <section data-testid="collab-projects-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
        <p style={{margin:"0 0 24px 0"}}>Projects and tasks with their people, deadlines, and evidence bundles. Each held task shows what's blocking it.</p>
      </section>
      <section data-testid="collab-projects-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
        <div data-testid="collab-projects-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
        <div data-testid="collab-projects-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Projects/Tasks not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
        <div data-testid="collab-projects-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV work.projects at App.js · surface at pages/os/CollabProjects.jsx.</div>
      </section>
    </div>
  );
}
