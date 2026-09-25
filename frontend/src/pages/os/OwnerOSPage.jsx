import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { OwnerMarkup } from '@/components/prototype/OwnerMarkup';
import template from '@/components/prototype/generated/os.json';
import { osModel, osCopy } from '@/components/prototype/osModel';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { PrototypeAccount, PrototypeNotice } from '@/components/prototype/PrototypeSupport';
import { CensusAccess } from '@/components/census/CensusAccess';
import { CensusRunDialog } from '@/components/census/CensusRunDialog';
import '@/components/census/census.css';
import '@/components/prototype/prototype.css';

export default function OwnerOSPage() {
  const session = usePrototypeSession();
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const portal = pathname === '/os';
  const [navTab, setNavTab] = useState(params.get('nav') || 'work');
  const [selected, setSelected] = useState(params.get('app') === 'registry' ? { label: 'Registry', path: '/os/admin/estate', group: 'Manage Estate' } : { label: 'Chat', path: '/os/work/chat', group: 'WorkStudio' });
  const [disclosure, setDisclosure] = useState({});
  const [message, setMessage] = useState(null);
  const [runOpen, setRunOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const notice = (title, body) => setMessage({ title, body });
  useEffect(() => {
    if (portal && params.get('nav') === 'admin') { setNavTab('admin'); setSelected({ label: 'Registry', path: '/os/admin/estate', group: 'Manage Estate' }); }
  }, [portal, params]);
  const model = osModel({ data: session.data, user: session.user, portal, navTab, setNavTab, selected, setSelected, params, setParams, navigate,
    disclosure, toggle: key => setDisclosure(old => ({ ...old, [key]: !old[key] })), openRun: () => setRunOpen(true), notice });
  const account = { role: 'button', tabIndex: 0, title: 'Your account', 'aria-label': 'Your account', 'data-testid': 'prototype-account-trigger', onClick: () => setAccountOpen(!accountOpen), onKeyDown: event => { if (['Enter', ' '].includes(event.key)) { event.preventDefault(); setAccountOpen(!accountOpen); } } };
  const slots = !session.data ? { 96: <CensusAccess error={session.error} loading={session.loading} retry={session.reload} /> } : {};
  return <>
    <OwnerMarkup template={template} surface="os" model={model} replace={osCopy(session.data, params.get('view'))} slots={slots} enhance={{ 38: account }} onUnbound={() => notice('Not activated in this slice', 'This action has no verified operational binding in the current census scope. No work was commissioned or state changed.')} />
    <PrototypeAccount open={accountOpen} session={session} navigate={navigate} close={() => setAccountOpen(false)} />
    <PrototypeNotice message={message} onClose={() => setMessage(null)} />
    {session.data && <CensusRunDialog open={runOpen} onClose={() => setRunOpen(false)} data={session.data} onQueued={() => { setParams({ view: 'history' }); session.reload(); }} />}
  </>;
}