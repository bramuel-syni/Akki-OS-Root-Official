import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { OwnerMarkup } from '@/components/prototype/OwnerMarkup';
import template from '@/components/prototype/generated/os.json';
import { osModel, osCopy } from '@/components/prototype/osModel';
import { osWorkModel, osWorkCopy } from '@/components/prototype/osWorkModel';
import { useOperationalWork } from '@/components/prototype/useOperationalWork';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { PrototypeAccount, PrototypeNotice } from '@/components/prototype/PrototypeSupport';
import { CensusAccess } from '@/components/census/CensusAccess';
import { CensusRunDialog } from '@/components/census/CensusRunDialog';
import { featureRoute } from '@/components/prototype/osHierarchy';
import { WorkSupportView, GreyMirrorWorkspace } from '@/components/prototype/OSFeatureViews';
import '@/components/census/census.css';
import '@/components/prototype/prototype.css';
import '@/components/prototype/osFeatures.css';

export default function OwnerOSPage() {
  const session = usePrototypeSession();
  const { pathname, search } = useLocation();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const portal = pathname === '/os';
  const feature = featureRoute(pathname);
  const workRoute = feature?.family === 'work';
  const work = useOperationalWork(workRoute ? session.data?.principal_id : null, 'os', params.get('request'));
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
  if (workRoute) Object.assign(model, osWorkModel({ work, navigate, setParams, disclosure, section: feature.section, search,
    toggle: key => setDisclosure(old => ({ ...old, [key]: !old[key] })) }));
  const account = { role: 'button', tabIndex: 0, title: 'Your account', 'aria-label': 'Your account', 'data-testid': 'prototype-account-trigger', onClick: () => setAccountOpen(!accountOpen), onKeyDown: event => { if (['Enter', ' '].includes(event.key)) { event.preventDefault(); setAccountOpen(!accountOpen); } } };
  const slots = !session.data ? { 96: <CensusAccess error={session.error} loading={session.loading} retry={session.reload} /> } : {};
  if (session.data && feature?.family === 'mirror') slots[96] = <GreyMirrorWorkspace section={feature.section} />;
  if (session.data && workRoute && feature.section !== 'records') {
    slots[2426] = <WorkSupportView section={feature.section} />;
    slots[2907] = null;
  }
  const enhance = { 38: account, ...(workRoute ? {
    2418: (context, props) => ({ role: 'navigation', 'aria-label': 'My Work sections', 'data-testid': 'my-work-navigation', style: { ...props.style, flexWrap: 'wrap' } }),
    2420: context => ({ 'aria-current': context.t.active ? 'page' : undefined, 'data-testid': `my-work-${context.t.key}-link` }),
    2462: context => ({ 'data-testid': `my-work-record-${context.t.requestId}` }),
    ...(feature.section !== 'records' ? {
      2425: (context, props) => ({ style: { ...props.style, gridTemplateColumns: 'minmax(0,1fr)', width: '100%', margin: '-26px 0 0' } }),
      2426: (context, props) => ({ style: { ...props.style, marginLeft: 0, marginRight: 0, padding: '26px 0', background: 'transparent' } }),
      2906: { hidden: true }, 2907: { hidden: true },
    } : {}),
  } : {}) };
  return <>
    <OwnerMarkup template={template} surface="os" model={model} replace={{ ...osCopy(session.data, params.get('view')), ...(workRoute ? osWorkCopy : {}) }} slots={slots} enhance={enhance} onUnbound={() => notice('Action unavailable', 'This action is not connected. No work was started or changed.')} />
    <PrototypeAccount open={accountOpen} session={session} navigate={navigate} close={() => setAccountOpen(false)} />
    <PrototypeNotice message={message} onClose={() => setMessage(null)} />
    {session.data && <CensusRunDialog open={runOpen} onClose={() => setRunOpen(false)} data={session.data} onQueued={() => { setParams({ view: 'history' }); session.reload(); }} />}
  </>;
}