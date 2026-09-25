import React from 'react';
import { count, stamp, initials, unknownFill } from './evidence';

const routes = [
  ['Extract', [['Processed intelligence', '/dap/extract/processed'], ['Trained models', '/dap/extract/finetune'], ['Callable skills', '/dap/extract/skill'], ['Raw data', '/dap/extract/raw']]],
  ['Connect Resources', [['Workspace API Key', '/dap/connect/key'], ['Your AI Agent', '/dap/connect/agents'], ['Your Compute', '/dap/connect/compute'], ['Your Models & Recipes', '/dap/connect/models']]],
  ['Available Resources', [['Compute', '/dap/resources/compute'], ['Base Models', '/dap/resources/base'], ['Trained Models', '/dap/resources/tuned'], ['Skills', '/dap/resources/skills']]],
  ['Data Governance', [['Policies & Regulations', '/dap/governance/policies'], ['Contract & Access Terms', '/dap/governance/contract'], ['Data Collection', '/dap/governance/collection']]],
];

export function dapModel({ data, user, path, params, navigate, group, setGroup, openRun }) {
  const latest = data?.latest;
  const sourceId = path.startsWith('/dap/estates/') ? decodeURIComponent(path.split('/').pop()) : null;
  const source = data?.sources?.find(s => s.source_id === sourceId);
  const history = path === '/dap/census';
  const selected = data?.records?.find(r => r.record_id === params.get('record'));
  const groups = [['Data Estates', [...(data?.sources || []).map(s => [s.label, `/dap/estates/${s.source_id}`]), ['Census records', '/dap/census']]], ...routes];
  const cols = ['#496b8d', '#a78b59', '#7d8f6d'];
  return {
    party: data ? `${data.tenant_id} estate` : 'Admitted access required', principal: user?.name || 'Not signed in',
    initials: initials(user?.name), trustDomain: data?.tenant_id ? `${data.tenant_id} · scoped identity` : 'No tenant selected',
    landingBg: path === '/dap' ? '#fff' : 'transparent', landingColor: 'var(--ink)', landingBorder: path === '/dap' ? 'var(--line)' : 'transparent', landingShadow: 'none', landingWeight: path === '/dap' ? '600' : '400', goLanding: () => navigate('/dap'),
    navGroups: groups.map(([label, items]) => ({ label, open: group === label, onToggle: () => setGroup(group === label ? '' : label), chev: group === label ? 'M4 6.2l4 4 4-4' : 'M6 4l4 4-4 4', labelColor: group === label ? 'var(--ink)' : 'var(--ink3)', headBg: group === label ? 'rgba(22,39,74,.09)' : 'transparent', hasDot: false,
      items: items.map(([name, to]) => ({ label: name, onClick: () => navigate(to), bg: path === to ? '#fff' : 'transparent', color: path === to ? 'var(--ink)' : 'var(--ink2)', border: path === to ? 'var(--line)' : 'transparent', shadow: path === to ? '0 1px 3px rgba(22,39,74,.10)' : 'none', weight: path === to ? '600' : '400', mark: path === to ? 'var(--accent)' : 'transparent' })) })),
    isLanding: path === '/dap', isEstate: Boolean(source) || Boolean(selected), isOverview: history && !selected,
    showPageHead: Boolean(source) || Boolean(selected), estHasSubsets: false,
    censusColor: 'var(--brass)', censusLabel: latest ? `Census #${latest.census_number || 'run'} · retained evidence` : 'No attributed census available',
    censusLede: 'What the admitted estate holds, what its retained census establishes, and what remains unmeasured. No use rights are inferred from an inventory.',
    pageEyebrow: 'Data Estates', pageTitle: selected ? `Census #${selected.census_number || 'run'}` : history ? 'Census records' : source?.label || 'Data access',
    pageSub: selected ? `${data.tenant_id} · ${stamp(selected.finished_at)}` : source ? 'An admitted source reference. Current reachability and content coverage are not implied.' : 'Your admitted estate, its records and governing evidence.', pageHasGate: false,
    landFigures: [{ v: count(latest?.database_count), l: 'Databases recorded' }, { v: count(latest?.table_count), l: 'Tables recorded' }, { v: count(latest?.row_count_estimate), l: 'Estimated rows' }, { v: 'Not measured', l: 'Volume held' }],
    censusStale: Boolean(latest && !latest.execution_verified), censusLive: Boolean(latest?.execution_verified),
    composition: (data?.sources || []).map((s, i) => ({ label: s.label, w: '0%', fill: cols[i % cols.length], cursor: 'pointer', size: 'Volume unmeasured', onClick: () => navigate(`/dap/estates/${s.source_id}`) })),
    availBar: [{ label: 'Use rights not established', v: 'Not a release grant', w: '100%', fill: unknownFill }],
    ovEyebrow: 'Census evidence', ovTitle: 'Every attributed reading.', ovLede: 'Retained census records for your admitted tenant. A historical record is not a fresh source verification.',
    ovRows: (data?.records || []).map(r => ({ n: `#${r.census_number || 'run'}`, title: r.scope, line: stamp(r.finished_at), right: `${count(r.table_count)} tables`, color: 'var(--ink2)', onClick: () => navigate(`/dap/census?record=${r.record_id}`) })),
    ovNote: data?.omission_note || 'Sign in to view records.',
    isEstateAudio: true, isEstateOther: false, backAudioBar: () => source ? navigate('/dap') : navigate('/dap/census'), audioBarIsLesson: true, audioBarIsBars: false,
    audioSelName: selected ? `Census #${selected.census_number || 'run'}` : source?.label,
    audioSelOrigin: selected ? 'Retained evidence' : 'Admitted source descriptor', audioSelSize: selected ? `${count(selected.table_count)} tables` : 'Volume not measured',
    estStats: selected ? [{ l: 'Tenant', v: data.tenant_id }, { l: 'Databases', v: count(selected.database_count) }, { l: 'Tables', v: count(selected.table_count) }, { l: 'Estimated rows', v: count(selected.row_count_estimate) }, { l: 'Counted rows', v: count(selected.row_count_measured) }, { l: 'Data volume', v: 'Not measured' }, { l: 'Record', v: selected.proof_ref }, { l: 'SHA-256', v: selected.proof_sha256 }]
      : [{ l: 'Tenant', v: data?.tenant_id }, { l: 'Source reference', v: source?.source_id }, { l: 'Scope', v: source?.scope }, { l: 'Reachability', v: 'Not freshly verified' }, { l: 'Source inventory', v: 'Not separately attributed' }, { l: 'Volume', v: 'Not measured' }, { l: 'Quality', v: 'Not measured' }, { l: 'Use rights', v: 'Not established' }],
    estCustody: selected ? selected.limitations.join(' ') : 'Census source admission permits only the bounded operation. It does not grant raw release, training or other downstream rights.',
    estOps: [{ name: 'Read census metadata', leaves: 'Tenant-scoped records; no source rows', state: 'Admitted', color: 'var(--sage)', bg: 'rgba(29,122,110,.08)' }, ...['Processed intelligence', 'Model training', 'Callable skills', 'Raw data release'].map(name => ({ name, leaves: 'Not established by this census', state: 'Separate admission required', color: 'var(--brass)', bg: 'rgba(176,141,46,.09)' }))],
    estGoProcessed: () => navigate('/dap/extract/processed'), estGoFinetune: () => navigate('/dap/extract/finetune'), estGoSkills: () => navigate('/dap/extract/skill'), estGoRaw: () => navigate('/dap/extract/raw'),
    railChat: false, railIsNotes: true, railIsChat: false,
    notesTitle: history || selected ? 'Reading the evidence' : source ? 'Source boundaries' : 'Reading this page',
    notesSub: 'What the census does—and does not—establish.',
    notesIntro: `The ${data?.tenant_id || 'admitted'} estate is shown from retained records. Unknowns stay unknown.`,
    notesRows: [{ label: 'Recorded, not newly verified', text: latest ? `Latest retained census: ${stamp(latest.finished_at)}.` : 'No attributed census is available until you sign in.' }, { label: 'Estimates remain estimates', text: 'Database row estimates are not counted rows or a completeness measurement.' }, { label: 'Separate rights', text: 'Census access does not grant extraction, training or external release.' }, { label: 'Execution', text: data?.runs?.[0]?.stage === 'blocked' ? 'The latest operational run is blocked. No verified source output was produced.' : 'New runs complete only after output and receipts are verified.' }],
    hasNotesClose: true, notesClose: data?.omission_note || 'Records are scoped to the admitted identity.',
    notes: [{ tag: 'Recorded, not newly verified', color: 'var(--brass)', text: latest ? `Latest retained census: ${stamp(latest.finished_at)}.` : 'No attributed census is available until you sign in.' },
      { tag: 'Estimates remain estimates', color: 'var(--sage)', text: 'Database row estimates are not counted rows or a completeness measurement. Content volume and quality remain unmeasured.' },
      { tag: 'Separate rights', color: 'var(--gate)', text: 'Census access does not grant extraction, training or external release.' },
      { tag: 'Census evidence', color: 'var(--accent)', text: React.createElement(React.Fragment, null,
        React.createElement('p', { style: { margin: '0 0 10px' }, 'data-testid': 'prototype-dap-run-posture' }, data?.runs?.[0]?.stage === 'blocked' ? 'The latest run is blocked; no verified source output was produced.' : 'New runs complete only after output and receipts are verified.'),
        React.createElement('button', { 'data-testid': 'prototype-dap-history-link', className: 'prototype-text-action', onClick: () => navigate('/os/admin/estate?view=history') }, 'View run history →'),
        data?.can_run && React.createElement('button', { 'data-testid': 'prototype-dap-run-census', className: 'prototype-text-action', onClick: openRun }, 'Run census now →')) }],
    historyRows: ['Queries', 'GPU hours', 'Outputs received', 'Allowance remaining'].map(l => ({ l, v: 'Not measured' })),
  };
}

export const dapCopy = data => ({
  32: `${data?.tenant_id || 'Akki'} Data Access Portal`,
  38: `Scoped access · ${data?.tenant_id || 'sign-in required'}`,
  91: React.createElement(React.Fragment, null, `${count(data?.latest?.table_count)} tables recorded.`, React.createElement('br'), 'Use rights not established.'),
  103: 'Admitted source groups · volume share unmeasured',
  120: 'What you can use · requires separate rights',
  135: 'Use rights are granted deliberately, by source and purpose. This census does not establish access percentages, release authority or uncounted volume.',
  141: 'Source content remains within the estate. Pricing and included allowances are not established by this census.',
  236: 'No rights or source selection are carried over without the destination workflow’s validation.',
  685: 'Usage is not measured in this census view. Missing measurement is not zero usage or an included allowance.',
});