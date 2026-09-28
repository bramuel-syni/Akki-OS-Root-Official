import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { OwnerMarkup } from '@/components/prototype/OwnerMarkup';
import template from '@/components/prototype/generated/os.json';
import { osModel, osCopy } from '@/components/prototype/osModel';
import { useOperationalWork } from '@/components/prototype/useOperationalWork';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { PrototypeAccount, PrototypeNotice } from '@/components/prototype/PrototypeSupport';
import { CensusAccess } from '@/components/census/CensusAccess';
import { CensusRunDialog } from '@/components/census/CensusRunDialog';
import { featureRoute } from '@/components/prototype/osHierarchy';
import { useNexusExperience } from '@/components/prototype/useNexusExperience';
import '@/components/census/census.css';
import '@/components/prototype/prototype.css';
import '@/components/prototype/nexusOwner.css';

export default function OwnerOSPage() {
  const session = usePrototypeSession();
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const portal = pathname === '/os';
  const feature = featureRoute(pathname);
  const workRoute = feature?.family === 'work';
  const work = useOperationalWork(feature ? session.data?.principal_id : null, 'os', params.get('request'));
  const [navTab, setNavTab] = useState(params.get('nav') || 'work');
  const [selected, setSelected] = useState(params.get('app') === 'registry' ? { label: 'Registry', path: '/os/admin/estate', group: 'Manage Estate' } : { label: 'Chat', path: '/os/work/chat', group: 'WorkStudio' });
  const [disclosure, setDisclosure] = useState({});
  const [message, setMessage] = useState(null);
  const [runOpen, setRunOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const notice = (title, body) => setMessage({ title, body });
  useEffect(() => {
    if (portal && params.get('nav') === 'admin') {
      setNavTab('admin');
      setSelected(params.get('app') === 'greymirror' ? { label: 'Grey Mirror', path: '/os/admin/greymirror', group: 'Manage Estate' }
        : { label: 'Registry', path: '/os/admin/estate', group: 'Manage Estate' });
    }
    if (portal && params.get('app') === 'tasks') {
      setNavTab('work'); setSelected({ label: 'My Work', path: '/os/work/tasks', group: 'WorkStudio' });
    }
  }, [portal, params]);
  const model = osModel({ data: session.data, user: session.user, portal, navTab, setNavTab, selected, setSelected, params, setParams, navigate,
    disclosure, toggle: key => setDisclosure(old => ({ ...old, [key]: !old[key] })), openRun: () => setRunOpen(true), notice });
  const account = { role: 'button', tabIndex: 0, title: 'Your account', 'aria-label': 'Your account', 'data-testid': 'prototype-account-trigger', onClick: () => setAccountOpen(!accountOpen), onKeyDown: event => { if (['Enter', ' '].includes(event.key)) { event.preventDefault(); setAccountOpen(!accountOpen); } } };
  const nexus = useNexusExperience({ feature, work, session, navigate, params, setParams, baseModel:model, account });
  if(nexus.active) Object.assign(model,nexus.model);
  const slots = !session.data ? { 96: <CensusAccess error={session.error} loading={session.loading} retry={session.reload} /> } : {};
  if(nexus.active){slots[36]=nexus.header;if(workRoute)slots[2408]=<>{nexus.content}{nexus.drawer}</>;else slots[96]=<>{nexus.content}{nexus.drawer}</>;}
  const enhance = { 38: account, ...(nexus.active?{36:{className:'nexus-header-actions'}}:{}) };
  return <>
    <OwnerMarkup template={template} surface="os" model={model} replace={osCopy(session.data, params.get('view'))} slots={slots} enhance={enhance} onUnbound={() => nexus.active?nexus.unavailable('Action unavailable'):notice('Action unavailable', 'This action is not connected. No work was started or changed.')} />
    <PrototypeAccount open={accountOpen} session={session} navigate={navigate} close={() => setAccountOpen(false)} />
    <PrototypeNotice message={message} onClose={() => setMessage(null)} />
    {session.data && <CensusRunDialog open={runOpen} onClose={() => setRunOpen(false)} data={session.data} onQueued={() => { setParams({ view: 'history' }); session.reload(); }} />}
  </>;
}