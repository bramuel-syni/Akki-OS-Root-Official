import React, { useState } from 'react';
import { useLocation, useNavigate, useOutlet, useSearchParams } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { AuthCtx } from './DAPLayout';
import { OwnerMarkup } from '@/components/prototype/OwnerMarkup';
import template from '@/components/prototype/generated/dap.json';
import { dapModel, dapCopy } from '@/components/prototype/dapModel';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { PrototypeAccount, PrototypeNotice } from '@/components/prototype/PrototypeSupport';
import { CensusAccess } from '@/components/census/CensusAccess';
import { CensusRunDialog } from '@/components/census/CensusRunDialog';
import '@/components/census/census.css';
import '@/components/prototype/prototype.css';

export const CensusPrototypeRoute = () => null;

export default function OwnerDAPLayout() {
  const session = usePrototypeSession();
  const { pathname } = useLocation();
  const navigation = useNavigate();
  const outlet = useOutlet();
  const [params, setParams] = useSearchParams();
  const [group, setGroup] = useState('Data Estates');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const [message, setMessage] = useState(null);
  const [runOpen, setRunOpen] = useState(false);
  const navigate = path => { setMobileOpen(false); navigation(path); };
  const notice = (title, body) => setMessage({ title, body });
  const model = dapModel({ data: session.data, user: session.user, path: pathname, params, setParams, navigate, group, setGroup, notice, openRun: () => setRunOpen(true) });
  const scoped = ['/dap', '/dap/census'].includes(pathname) || pathname.startsWith('/dap/estates/');
  const slots = !session.data ? { 72: <CensusAccess error={session.error} loading={session.loading} retry={session.reload} /> } : !scoped ? { 72: outlet } : {};
  const account = { role: 'button', tabIndex: 0, title: 'Your account', 'aria-label': 'Your account', 'data-testid': 'prototype-account-trigger', onClick: () => setAccountOpen(!accountOpen), onKeyDown: event => { if (['Enter', ' '].includes(event.key)) { event.preventDefault(); setAccountOpen(!accountOpen); } } };
  return <AuthCtx.Provider value={{ user: session.user, loading: session.loading, doLogin: session.login, doLogout: session.logout }}>
    <div className={mobileOpen ? 'prototype-dap-container mobile-nav-open' : 'prototype-dap-container'}>
      <button data-testid="prototype-mobile-nav" className="prototype-mobile-nav" aria-controls="dap-nav" aria-expanded={mobileOpen} onClick={() => setMobileOpen(!mobileOpen)}>{mobileOpen ? <X size={15} /> : <Menu size={15} />}Menu</button>
      <OwnerMarkup template={template} surface="dap" model={model} replace={dapCopy(session.data)} slots={slots} enhance={{
        41: account,
        32: { role: 'link', tabIndex: 0, 'data-testid': 'prototype-dap-home', onClick: () => navigate('/dap'), onKeyDown: e => e.key === 'Enter' && navigate('/dap') },
        97: (context, props) => ({ title: context.g.v, style: { ...props.style, fontSize: String(context.g.v).length > 9 && !String(context.g.v).includes(' ') ? '16px' : props.style.fontSize } }),
      }} onUnbound={() => notice('Not activated in this slice', 'This action is not verified in the current census scope. No sample entitlement, payment or execution has been recorded.')} />
    </div>
    <PrototypeAccount open={accountOpen} session={session} navigate={navigate} close={() => setAccountOpen(false)} />
    <PrototypeNotice message={message} onClose={() => setMessage(null)} />
    {session.data && <CensusRunDialog open={runOpen} onClose={() => setRunOpen(false)} data={session.data} onQueued={() => { navigate('/os/admin/estate?view=history'); session.reload(); }} />}
  </AuthCtx.Provider>;
}