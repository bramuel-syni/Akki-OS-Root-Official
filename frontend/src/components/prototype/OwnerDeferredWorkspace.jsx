import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { OwnerWorkspace } from './OwnerWorkspace';
import { usePrototypeSession } from './usePrototypeSession';
import { apiRequest as getApi } from '../models/useModelApproval';

// Unavailable workflows retain their banked surface; no demonstration records or replacement layouts.
const ROUTES = {
  analyze: ['Analyze', 'Data Suite', 'analyze', 'isAnalyzeActive'],
  clarity: ['Clarity', 'ThinkLab', 'thinklab', 'isThinklabActive'],
  strategy: ['Strategy', 'ThinkLab', 'thinklab', 'isThinklabActive'],
  hypothesis: ['Hypothesis', 'ThinkLab', 'thinklab', 'isThinklabActive'],
  perspective: ['Perspective', 'ThinkLab', 'thinklab', 'isThinklabActive'],
  signals: ['Signals', 'Monitor', 'monitor', 'isMonitorGroup'],
  ideas: ['Ideas', 'Monitor', 'monitor', 'isMonitorGroup'],
  govern: ['Rules & Rails', 'Shield', 'trust', 'isTrustGroup'],
  agentbuild: ['Build Agents', 'Build Your Resources', 'build', 'isBuildGroup'],
  youragents: ['Your Agents', 'Your Resources', 'build', 'isBuildGroup'],
  yourmodels: ['Your Models', 'Your Resources', 'build', 'isBuildGroup'],
  buildskill: ['Build a Skill', 'Build Your Resources', 'buildrun', 'isBuildRunPage'],
  extract: ['Extract Data', 'Build Your Resources', 'buildrun', 'isBuildRunPage'],
  mentions: ['Mentions', 'Collaboration', 'collab', 'isCollabGroup'],
  emails: ['Emails', 'Collaboration', 'collab', 'isCollabGroup'],
  projects: ['Projects', 'Collaboration', 'collab', 'isCollabGroup'],
  hrstuff: ['HR', 'Collaboration', 'collab', 'isCollabGroup'],
  new: ['New Apps', 'Apps', 'apps', 'isThirdpartyGroup'],
  frequent: ['Frequent Apps', 'Apps', 'apps', 'isThirdpartyGroup'],
  connected: ['Connected Apps', 'Apps', 'apps', 'isThirdpartyGroup'],
  requests: ['App Requests', 'Apps', 'apps', 'isThirdpartyGroup'],
};

export default function OwnerDeferredWorkspace() {
  const session = usePrototypeSession(), navigate = useNavigate(), { pathname } = useLocation();
  const key = pathname.split('/').at(-1), [title, group, section, flag] = ROUTES[key];
  const [models, setModels] = useState(null), [error, setError] = useState(null);
  useEffect(() => {
    let live = true;
    if (key === 'yourmodels' && session.data) getApi('/api/training/m9/models').then(value => { if (live) setModels(value.trained_adapters); }).catch(() => { if (live) setError('Model records could not be loaded.'); });
    return () => { live = false; };
  }, [key, session.data]);
  const available = key === 'yourmodels';
  const model = {
    [flag]: true, hasSessionBanner: !available || Boolean(error) || models === null,
    sessionBanner: !available ? `${title} is not available yet. No work has been started.` : error || 'Loading model records…', sessionBannerColor: 'var(--ink3)',
    isBuildAgents: key === 'agentbuild', isBuildYourAgents: key === 'youragents', isBuildYourModels: available,
    yourModelsView: (models || []).map(m => ({ key: m.model_id, name: m.variant === 'pruned' ? 'Language identification · reduced adapter' : 'Language identification · full adapter', origin: typeof m.base === 'string' ? m.base : m.base?.registry_id || m.base_model || '', status: m.status, statusColor: 'var(--sage)', statusBg: 'rgba(29,122,110,.08)' })), agentsListView: [],
    tlSessionOpen: false, tlSessionsView: [], collabHeadline: title, collabSubline: '', collabItems: [],
    isMonSignals: key === 'signals', isMonIdeas: key === 'ideas', sigEmpty: false, ideasEmpty: false, signalsView: [], ideasView: [],
    sigCountLabel: 'Unavailable', ideaCountLabel: 'Unavailable', sigPageLabel: '',
    isTrustRules: true, isRulesInForce: true, rulesRowsView: [], railsRowsView: [], rulesTabsView: [],
    isAnalyzeSources: true, analyzeRailOpen: false, analyzeFilesView: [], analyzeFileCount: '—',
    analyzeTabsView: ['Sources', 'Rapid analysis', 'Deep dive', 'Export'].map(label => ({ key: label, label, color: 'var(--ink3)', border: 'transparent' })),
    tmPageEmpty: true, tmEmptyCopy: `${title} is not available yet.`, tmNewLabel: key === 'buildskill' ? 'Build a skill' : 'Start extraction',
    isAppsRequests: key === 'requests', appsRequestOpen: false, appsListView: [], appsRequestsView: [],
    appsTabsView: ['new', 'frequent', 'connected', 'requests'].map(k => ({ key: k, label: ROUTES[k][0], border: k === key ? 'var(--accent)' : 'transparent', color: k === key ? 'var(--ink)' : 'var(--ink3)', onClick: () => navigate(`/os/apps/${k}`) })),
  };
  return <OwnerWorkspace session={session} title={title} group={group} section={section} model={model}
    enhance={{ 205: { disabled: true, 'data-testid': 'resource-create-unavailable' }, 7977: { disabled: true }, 167: { 'data-testid': 'workspace-title' } }} />;
}