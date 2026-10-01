import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { OwnerMarkup } from './OwnerMarkup';
import source from './generated/owner-workspaces.json';
import { PrototypeAccount, PrototypeNotice } from './PrototypeSupport';
import { CensusAccess } from '../census/CensusAccess';
import { initials } from './evidence';
import './prototype.css';
import './ownerWorkspaces.css';

// Uses the supplied HTML itself, not an approximation of its shell or controls.
export function OwnerWorkspace({ session, title, group, section, model = {}, slots = {}, enhance = {}, replace = {}, children, returnTo = '/os' }) {
  const navigate = useNavigate();
  const [accountOpen, setAccountOpen] = useState(false), [notice, setNotice] = useState(null);
  const bound = { appTitle: title, appGroupLabel: group, anyFullPage: false, rolePerson: session.user?.name || 'Not signed in', roleDept: session.data?.tenant_id || '', roleInitials: initials(session.user?.name),
    exitApp: () => navigate(returnTo), openShieldReport: () => setNotice({ title: 'Shield report', body: 'No page-level assurance report is available. Inspect source evidence before relying on an individual result.' }), ...model };
  const unbound = () => setNotice({ title: 'Not available', body: 'This action is not connected. Nothing has been changed.' });
  const content = session.data ? <>{section && <OwnerMarkup template={source[section]} surface="os" fragment model={bound} slots={slots} enhance={enhance} replace={replace} onUnbound={unbound} />}{children}</> : <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />;
  return <div className={`owner-workspace owner-workspace-${section || 'detail'}`} data-testid={`owner-workspace-${section || 'detail'}`}>
    <OwnerMarkup template={source.shell} surface="os" model={bound} slots={{ 96: <><OwnerMarkup template={source.header} surface="os" fragment model={bound} enhance={enhance} replace={replace} onUnbound={unbound} />{content}</> }} enhance={{ 38: { role: 'button', tabIndex: 0, 'aria-label': 'Your account', 'data-testid': 'prototype-account-trigger', onClick: () => setAccountOpen(!accountOpen), onKeyDown: e => { if (['Enter', ' '].includes(e.key)) { e.preventDefault(); setAccountOpen(!accountOpen); } } } }} />
    <PrototypeAccount open={accountOpen} session={session} navigate={navigate} close={() => setAccountOpen(false)} />
    <PrototypeNotice message={notice} onClose={() => setNotice(null)} />
  </div>;
}