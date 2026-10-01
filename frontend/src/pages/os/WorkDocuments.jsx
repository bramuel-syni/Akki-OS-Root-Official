import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { censusRequest } from '@/components/census/useCensusWorkspace';
import { CommissionDirection, CommissionRevisions } from '@/components/studio/CommissionRevisions';
import { CommissionBuilds } from '@/components/studio/CommissionBuilds';
import { useStudio, stamp } from '@/components/studio/useStudio';
import { PresentationDetails, documentTitle, readableText } from '@/components/shared/PresentationDetails';
import '@/components/estate/estate.css';

export default function WorkDocuments() {
  const session = usePrototypeSession();
  const [params] = useSearchParams();
  const studio = useStudio(session.data?.principal_id, params.get('commission'));
  const [search, setSearch] = useState(''), [filter, setFilter] = useState('All'), [rail, setRail] = useState(true), [askOpen, setAskOpen] = useState(true), [overview, setOverview] = useState(!params.get('commission')), [ascending, setAscending] = useState(false);
  const { commissions, commission, selected, select, loading, error, busy, notice, reload, act, fail } = studio;
  const [creating, setCreating] = useState(false);
  const canOperate = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const rows = (commissions || []).filter(c => documentTitle(c).toLowerCase().includes(search.toLowerCase()) && (filter === 'All' || (filter === 'Ready' ? c.release?.state === 'clear' : c.release?.state !== 'clear'))).sort((a, b) => (ascending ? 1 : -1) * String(a.updated_at || a.created_at || '').localeCompare(b.updated_at || b.created_at || ''));
  const choose = id => { select(id); setOverview(false); };
  const create = async () => {
    if (creating || busy || !canOperate) return;
    setCreating(true);
    try {
      const { report } = await censusRequest('/estate-intelligence/report');
      if (!report) { fail('No verified census is available. Review Registry before creating a board pack.'); return; }
      const result = await act('Commission board pack', `/producers/estate-intelligence/${report.job_id}`, {});
      if (result) setOverview(false);
    } catch { fail('The board pack could not be created. Refresh the census report and try again.'); }
    finally { setCreating(false); }
  };
  const detail = Boolean(commission) && commission.commission_id === selected && !overview;
  const model = { isDocumentsActive: true, docEditorOpen: false, shellHeight: 'calc(100dvh - 152px)', hasSessionBanner: Boolean(error || notice || loading), sessionBanner: readableText(error || notice || (loading ? 'Loading documents…' : '')), sessionBannerColor: error ? 'var(--oxblood)' : 'var(--ink3)', docRailOpen: rail, docRailClosed: !rail, toggleDocRail: () => setRail(v => !v),
    docSearch: search, docSearchChange: e => setSearch(e.target.value), docCount: (commissions || []).length, docsEmpty: !rows.length, docSortLabel: ascending ? 'Oldest' : 'Recent', cycleDocSort: () => setAscending(v => !v), docPageLabel: `${rows.length} documents`,
    docStatusChips: ['All', 'Ready', 'Needs review'].map(label => ({ key: label, label, border: label === filter ? 'var(--blue)' : 'var(--line)', bg: label === filter ? 'var(--blue)' : '#fff', color: label === filter ? '#fff' : 'var(--ink3)', onClick: () => setFilter(label) })),
    docsView: rows.map(c => ({ key: c.commission_id, name: documentTitle(c), status: c.release?.state === 'clear' ? 'Ready' : readableText(c.release?.state || 'Not built'), statusColor: c.release?.state === 'clear' ? 'var(--sage)' : 'var(--brass)', metaPrefix: `Version ${c.current_content_version}`, isSelected: detail && selected === c.commission_id, rowBg: detail && selected === c.commission_id ? 'var(--surface)' : 'transparent', nameWeight: detail && selected === c.commission_id ? '600' : '400', tags: (c.outputs || []).map(f => ({ label: f.toUpperCase() })), hasFit: false, onOpen: () => choose(c.commission_id) })),
    docsOverview: !detail, docsHeadline: 'Your documents', docsSubline: '', toggleDocNewMenu: create,
    docFiguresView: [{ value: (commissions || []).filter(c => c.release?.state === 'clear').length, label: 'ready to download' }, { value: (commissions || []).filter(c => c.release?.state !== 'clear').length, label: 'awaiting a build or review' }],
    docRecentDrafts: (commissions || []).slice(0, 5).map(c => ({ key: c.commission_id, name: documentTitle(c), status: c.release?.state === 'clear' ? 'Ready' : readableText(c.release?.state), statusColor: 'var(--ink3)', age: `v${c.current_content_version}`, onOpen: () => choose(c.commission_id) })),
    docJournalView: (commissions || []).slice(0, 5).map(c => ({ key: c.commission_id, name: documentTitle(c), time: stamp(c.updated_at || c.created_at), onJump: () => choose(c.commission_id) })), docsFooter: loading ? 'Refreshing…' : '',
    docAskVisible: askOpen, docAskHidden: !askOpen, toggleDocAsk: () => setAskOpen(v => !v), docTipsLabel: 'Hide', toggleDocTips: () => setAskOpen(false), docsNoContext: !detail, docDetailOpen: detail, drawerTitleIdle: true, drawerTitleValue: commission ? documentTitle(commission) : '', drawerMetaShort: commission ? `Version ${commission.current_content_version}` : '', drawerNotBrief: false };
  const center = detail ? <div className="owner-document-detail">
    <button className="estate-btn" onClick={() => setOverview(true)} data-testid="studio-overview">← Overview</button>
    <CommissionBuilds commission={commission} canOperate={canOperate} busy={busy} onBuild={() => act('Build', `/commissions/${selected}/build`)} onExport={id => act('Export PDF', `/commissions/${selected}/builds/${id}/export-pdf`)} onThumbnails={id => act('Render thumbnails', `/commissions/${selected}/builds/${id}/thumbnails`)} />
    <PresentationDetails key={selected} id="studio-edit" title={commission.release?.state === 'blocked pending re-verdict' ? 'Review required · revisions' : 'Revise document'} open={commission.release?.state === 'blocked pending re-verdict'}><CommissionRevisions commission={commission} canOperate={canOperate} busy={busy} onRevise={changes => act('Revise', `/commissions/${selected}/revise`, { changes })} onReverdict={() => act('Re-verdict', `/commissions/${selected}/reverdict`)} /></PresentationDetails>
    <PresentationDetails id="studio-sources" title="Sources & editorial direction"><CommissionDirection commission={commission} /></PresentationDetails>
  </div> : null;
  return <OwnerWorkspace session={session} title="Documents" group="WorkStudio" section="documents" model={model}
    slots={{ ...(detail ? { 1632: center } : {}), 1614: <button onClick={() => reload(selected)} disabled={loading} data-testid="work-documents-reload" style={{ border: 0, background: 'transparent', font: 'inherit', cursor: 'pointer' }}>{loading ? 'Refreshing…' : 'Refresh documents'}</button>, 2225: <p className="owner-status" data-testid="document-chat-unavailable">Document chat is not connected. Downloads and revisions are available in the document.</p> }}
    replace={{ 2115: creating ? 'Creating…' : 'New board pack', 2177: '' }}
    enhance={{ 184: { 'aria-disabled': true, onClick: undefined, onKeyDown: undefined, title: 'Exposure mapping is not connected' }, 1564: { 'data-testid': 'studio-search', 'aria-label': 'Search documents' }, 1584: c => ({ 'data-testid': `studio-select-${c.d.key}`, 'aria-pressed': c.d.isSelected }), 2115: { 'data-testid': 'work-documents-commission-census', disabled: creating || Boolean(busy) || !canOperate }, 2156: c => ({ role: 'button', tabIndex: 0, 'data-testid': `studio-recent-${c.rd.key}`, onClick: c.rd.onOpen, onKeyDown: e => { if (e.key === 'Enter') c.rd.onOpen(); } }), 2205: { onClick: undefined, onKeyDown: undefined, role: undefined, title: undefined, tabIndex: undefined }, 2264: { disabled: true, 'aria-label': 'Document chat unavailable' }, 2265: { disabled: true } }}>
  </OwnerWorkspace>;
}