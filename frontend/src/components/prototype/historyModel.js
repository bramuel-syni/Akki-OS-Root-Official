import { count, stamp, unmeasuredBar, measuredWays } from './evidence';

export function historyModel(data, params, setParams) {
  const records = data?.records || [];
  const entries = [...(data?.runs || []).filter(r => !records.some(c => c.record_id === r.census_run_id)), ...records];
  const selected = entries.find(r => (r.record_id || r.census_run_id) === params.get('record'));
  const activeTab = params.get('detail') || 'discovery';
  const page = Number(params.get('page') || 1);
  const update = extra => setParams({ view: 'history', ...extra });
  const itemStatus = item => item.stage ? item.stage.replaceAll('_', ' ') : item.execution_verified ? item.status.toLowerCase() : 'Recorded';
  const proof = selected?.proof_ref;
  const hasOutput = selected?.table_count != null;
  return {
    measuredPageOpen: params.get('view') === 'history',
    closeMeasuredPage: () => setParams({}),
    censusHistIsTranscript: Boolean(selected), censusHistIsList: !selected,
    censusHistoryView: entries.slice((page - 1) * 8, page * 8).map(item => ({
      key: item.record_id || item.census_run_id, num: item.census_number || item.census_run_id,
      status: itemStatus(item), statusBg: item.status === 'REFUSED' ? 'rgba(184,57,91,.10)' : 'var(--surface2)',
      statusColor: item.status === 'REFUSED' ? 'var(--oxblood)' : 'var(--ink3)',
      rowBg: selected === item ? 'var(--surface)' : '#fff',
      metaLine: stamp(item.finished_at || item.created_at),
      excludedNote: item.stage === 'blocked' ? 'No verified source execution; excluded from measured figures.' : !item.execution_verified && !item.stage ? 'Historical evidence; not a fresh source verification.' : '',
      onOpen: () => update({ record: item.record_id || item.census_run_id }),
    })),
    censusHistShowPagination: entries.length > 8, censusHistPageLabel: `Page ${page} of ${Math.max(1, Math.ceil(entries.length / 8))}`,
    censusHistPrevPage: () => update({ page: Math.max(1, page - 1) }), censusHistNextPage: () => update({ page: Math.min(Math.ceil(entries.length / 8), page + 1) }),
    measuredProv: [{ k: 'Tenant', v: data?.tenant_id || 'Not signed in' }, { k: 'Latest', v: stamp(data?.latest?.finished_at) }, { k: 'Method', v: 'Retained metadata evidence; estimates labelled separately.' }, { k: 'Custody', v: 'Source data remains at the estate.' }],
    measuredWays, measuredDeclared: 'Rights and personal-data classifications are not measured here. No release permission can be inferred.',
    measuredPopulation: 'Only records attributed to the authenticated tenant are shown. Mixed-tenant and unassigned historical records are withheld.',
    backToCensusHistory: () => update({}),
    censusTranscriptMeta: { num: selected?.census_number || selected?.census_run_id || '',
      status: selected ? itemStatus(selected) : '', duration: 'Duration: not verified',
      metaLine: `${data?.tenant_id || ''} · ${stamp(selected?.finished_at || selected?.created_at)}`,
      excludedNote: selected?.stage === 'blocked' ? 'The configured Akki execution identity could not authenticate. No source data was read.' : selected?.limitations?.[0] || '',
      hasPause: false, found: hasOutput ? [`${count(selected?.database_count)} databases; ${count(selected?.table_count)} tables recorded.`, `${count(selected?.row_count_estimate)} estimated rows; not a counted-row assertion.`] : ['No verified inventory output is available for this run.'] },
    censusDetailStatusBg: selected?.status === 'REFUSED' ? 'rgba(184,57,91,.10)' : 'var(--surface2)', censusDetailStatusColor: selected?.status === 'REFUSED' ? 'var(--oxblood)' : 'var(--ink3)',
    censusDetailTabs: [['discovery', 'Discovery'], ['gpu', 'GPU spend'], ['conversation', 'Conversation'], ['evidence', 'Evidence']].map(([key, label]) => ({ key, label, color: key === activeTab ? 'var(--ink)' : 'var(--ink3)', border: key === activeTab ? 'var(--blue)' : 'transparent', onClick: () => update({ record: params.get('record'), detail: key }) })),
    censusTabIsDiscovery: activeTab === 'discovery', censusTabIsGpu: activeTab === 'gpu', censusTabIsConvo: activeTab === 'conversation', censusTabIsEvidence: activeTab === 'evidence',
    censusConditionTotal: 'Quality distribution is not measured', censusConditionBar: unmeasuredBar('No quality measurement'),
    censusDiscoveryGroups: [{ title: 'Inventory', rows: [
      { label: 'Databases', value: count(selected?.database_count), note: 'Recorded metadata inventory' },
      { label: 'Tables', value: count(selected?.table_count), note: 'Recorded metadata inventory' },
      { label: 'Estimated rows', value: count(selected?.row_count_estimate), note: 'Source metadata estimate, not counted rows' },
      { label: 'Data volume', value: 'Not measured', note: 'No bytes measurement in this record' },
    ].map(r => ({ ...r, valueColor: 'var(--ink)', delta: 'No verified delta', deltaColor: 'var(--ink3)' })) },
    { title: 'Execution outcome', rows: (selected?.outcomes || []).map(o => ({ label: data.sources.find(s => s.source_id === o.source_id)?.label || o.source_id, value: o.status, note: o.reason_code?.replaceAll('_', ' ').toLowerCase() || 'Verified aggregate output', delta: '', valueColor: o.status === 'complete' ? 'var(--sage)' : 'var(--oxblood)' })) }],
    censusGpuSummary: 'No measured GPU-spend evidence is attached to this census. Estimates are not substituted for telemetry.',
    censusGpuRows: ['GPU hours', 'Utilization', 'Cost', 'Energy'].map(label => ({ label, value: 'Not measured' })),
    censusDetailNoPause: true,
    censusEvidenceRows: [{ label: 'Record', value: proof || 'No validated result receipt', color: 'var(--ink)' }, { label: 'SHA-256', value: selected?.proof_sha256 || 'Not available', color: 'var(--ink3)' }, { label: 'Execution', value: selected?.execution_verified ? 'Akki-owned output verified' : 'Not verified by this record', color: 'var(--brass)' }],
  };
}