import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Database, Menu, ChevronRight, ArrowUpRight } from 'lucide-react';
import { CensusWorkspace } from '@/components/census/CensusWorkspace';

export default function CensusOSPage() {
  const [menu, setMenu] = useState(false);
  return <div className="census-os" data-testid="census-os-shell">
    <header className="census-os-top"><Link to="/os/admin/estate" data-testid="census-os-brand">Akki <span>OS</span></Link><Link to="/dap" data-testid="census-switch-dap">Data Access Portal <ArrowUpRight size={14} /></Link></header>
    <nav className="census-os-tabs" aria-label="OS navigation">{[['Work', '/os/work/chat'], ['Monitor', '/os/monitor/signals'], ['Build', '/os/build/train'], ['Apps', '/os/apps/frequent'], ['Admin', '/os/admin/estate']].map(([name, to]) => <Link key={name} to={to} data-testid={`census-os-nav-${name.toLowerCase()}`} className={name === 'Admin' ? 'active' : ''}>{name}</Link>)}</nav>
    <button data-testid="census-os-mobile-menu" aria-expanded={menu} aria-controls="census-os-side" className="census-mobile-toggle" onClick={() => setMenu(!menu)}><Menu size={18} />Manage estate</button>
    <div className="census-os-main"><aside id="census-os-side" className={`census-os-sidebar ${menu ? 'open' : ''}`}><p>MANAGE ESTATE</p><Link to="/os/admin/estate" data-testid="census-os-registry" className="active" onClick={() => setMenu(false)}><Database size={16} />Registry <ChevronRight size={14} /></Link><Link to="/os/admin/govern" data-testid="census-os-govern">Governance</Link><Link to="/os/admin/rulesupd" data-testid="census-os-rules">Rules & updates</Link></aside>
      <main><CensusWorkspace surface="os" /></main></div>
  </div>;
}