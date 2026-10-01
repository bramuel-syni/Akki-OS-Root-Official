import { stamp } from './evidence';

export const registryCount = value => typeof value === 'number' ? value.toLocaleString('en-GB', { maximumFractionDigits: 2 }) : 'Not measured';
export const registryBytes = value => {
  if (typeof value !== 'number') return 'Not measured';
  const index = value ? Math.min(4, Math.floor(Math.log(value) / Math.log(1024))) : 0;
  return `${registryCount(value / (1024 ** index))} ${['B', 'KiB', 'MiB', 'GiB', 'TiB'][index]}`;
};
export const metricValue = row => row?.value == null ? 'Not measured' : row.unit === 'bytes' ? registryBytes(row.value) : `${registryCount(row.value)}${row.unit === 'percent' ? '%' : row.unit === 'sources' ? ' sources' : ''}`;
const normalizedStatus = row => String(row?.status || '').toUpperCase();
const statusOf = row => normalizedStatus(row) === 'PENDING' ? 'Running' : ['COMPLETE','COMPLETED'].includes(normalizedStatus(row)) ? 'Complete' : 'Needs attention';
const colorOf = row => statusOf(row) === 'Running' ? 'var(--blue)' : statusOf(row) === 'Complete' ? 'var(--sage)' : 'var(--brass)';
const bgOf = row => statusOf(row) === 'Running' ? 'rgba(22,39,74,.10)' : statusOf(row) === 'Complete' ? 'rgba(29,122,110,.12)' : 'rgba(176,141,46,.14)';
const idOf = row => row?.record_id || row?.census_run_id;
const coverage = row => row?.coverage ? `${row.coverage.completed} of ${row.coverage.declared} source scopes completed` : `${row?.source_count ?? row?.source_ids?.length ?? 'Unrecorded'} source groups`;
const duration = row => row?.status === 'PENDING' ? 'running now' : row?.duration_seconds != null ? `${Math.floor(row.duration_seconds / 60)}m ${Math.round(row.duration_seconds % 60)}s` : 'duration not recorded';
const exclusions = row => row?.source_details?.filter(s => s.status !== 'complete').map(s => `${s.label}: ${s.exclusion?.plain || s.reason_code || s.status}`).join('; ') || row?.reason_code || '';
const description = {
  data_held: 'Total volume across every connected source', sources_full: 'Counted only when every row or file header was reached',
  share_measured: 'Read directly this census, not carried from an earlier run', duplicates: 'Byte-identical or near-identical copies found across sources',
  degraded: 'Corrupt, truncated or unreadable files; audio below transcription quality', incomplete: 'Required fields empty, or rows missing their linked record',
  stale: 'No new rows in the last 90 days — where this source window applies', schema_drift: 'Sources whose shape changed since the previous census',
  verified: 'Checked against a second source or a human sign-off', pii: 'Assessed personal information; masking and estate-boundary evidence stay explicit',
  usable: 'Measured, clean, and not duplicated — what a job can start on now', opportunities: 'Opportunities surfaced from this read',
};

export function registryHistory({ data, params, setParams, state, setState }) {
  const records = data?.records || [];
  const rows = [...records, ...(data?.runs || []).filter(run => !records.some(row => idOf(row) === idOf(run)))].sort((a,b) => (b.finished_at || b.created_at || '').localeCompare(a.finished_at || a.created_at || ''));
  const selected = rows.find(row => idOf(row) === params.get('record'));
  const page = Math.min(Number(params.get('page') || 1), Math.max(1, Math.ceil(rows.length / 5)));
  const tab = params.get('detail') || 'discovery';
  const select = row => setParams({ view: 'history', page: String(page), record: idOf(row), detail: 'discovery' });
  const messages = (data?.conversations || []).filter(item => item.census_run_id === idOf(selected));
  const workers = selected?.workers || [];
  const known = workers.length > 0;
  const model = {
    measuredPageOpen: params.get('view') === 'history',
    closeMeasuredPage: () => setParams({}), backToCensusHistory: () => setParams({ view: 'history', page: String(page) }),
    censusHistoryView: rows.slice((page - 1) * 5, page * 5).map(row => ({
      key: idOf(row), num: row.census_number ?? idOf(row), status: statusOf(row), statusColor: colorOf(row), statusBg: bgOf(row),
      metaLine: `${row.initiated_by || row.principal_id || 'Initiator not retained'} · ${stamp(row.finished_at || row.created_at)} · ${coverage(row)}.`,
      excludedNote: exclusions(row), rowBg: idOf(row) === idOf(selected) ? 'var(--surface)' : '#fff', onOpen: () => select(row),
    })),
    censusHistShowPagination: rows.length > 5, censusHistPageLabel: `Page ${page} of ${Math.max(1,Math.ceil(rows.length / 5))} · ${rows.length} censuses`,
    censusHistPrevPage: () => setParams({ view: 'history', page: String(Math.max(1,page - 1)) }),
    censusHistNextPage: () => setParams({ view: 'history', page: String(Math.min(Math.ceil(rows.length / 5),page + 1)) }),
    censusHistIsList: !selected, censusHistIsTranscript: Boolean(selected),
    censusDetailStatusColor: colorOf(selected), censusDetailStatusBg: bgOf(selected), censusDetailNoPause: messages.length === 0,
    censusTranscriptMeta: { num: selected?.census_number ?? idOf(selected), status: statusOf(selected), duration: duration(selected),
      metaLine: `${selected?.initiated_by || selected?.principal_id || 'Initiator not retained'} · ${stamp(selected?.finished_at || selected?.created_at)} · ${coverage(selected)}.`,
      excludedNote: exclusions(selected), hasPause: messages.length > 0,
      found: selected?.source_details?.map(s => `${s.label}: ${s.kind}; ${s.status}; ${s.table_count || 0} tables; ${registryBytes(s.volume_bytes)}. ${s.method || s.reason_code || ''}`) || selected?.limitations || [],
    },
    censusDetailTabs: [['discovery','Discovery Summary'],['gpu','GPU Spend'],['convo','Conversation with Agent'],['evidence','Discovery Details']].map(([key,label]) => ({key,label,
      onClick: () => setParams({ view: 'history', page: String(page), record: idOf(selected), detail: key }),
      color: tab === key ? 'var(--ink)' : 'var(--ink3)', border: tab === key ? 'var(--blue)' : 'transparent',
    })),
    censusTabIsDiscovery: tab === 'discovery', censusTabIsGpu: tab === 'gpu', censusTabIsConvo: tab === 'convo', censusTabIsEvidence: tab === 'evidence',
    censusDiscoveryGroups: (selected?.report?.groups || []).map(group => ({ title: group.label, rows: group.rows.map(row => ({...row,
      note: description[row.key] || row.description, value: metricValue(row), valueColor: row.status === 'unmeasured' ? 'var(--ink3)' : 'var(--ink)',
      delta: row.delta != null ? `${row.delta > 0 ? '+' : ''}${registryCount(row.delta)}${row.unit === 'percent' ? ' pp' : ''} vs previous` : row.status === 'sampled' ? `sampled · ${registryCount(row.population)} assessed` : row.status === 'unmeasured' ? 'unmeasured' : 'measured · no comparable prior',
      deltaColor: row.status === 'sampled' ? 'var(--brass)' : 'var(--ink3)',
    })) })),
    censusConditionBar: selected?.report?.condition_distribution
      ? selected.report.condition_distribution.map(seg => ({ label: seg.label, pct: `${registryCount(Math.round(seg.share * 1000) / 10)}%`, w: `${Math.max(seg.share > 0 ? 0.5 : 0, seg.share * 100)}%`, color: seg.color }))
      : ['Clean','Duplicate','Degraded','Incomplete','Not read'].map((label,i) => ({label,pct:'Not classified',w:'0%',color:['var(--sage)','var(--brass)','#b04a3a','#c9a24a','#b8b0a0'][i]})),
    censusConditionTotal: selected?.report?.condition_note || 'Condition has not been classified for this record.',
    censusGpuSummary: known ? 'Actual worker receipts for this census. CPU execution on a GPU host is not GPU acceleration; device telemetry is not attributed consumption.' : 'No run-attributed worker telemetry is retained for this historical census.',
    censusGpuRows: [
      {label:'GPU hours',value:known ? `${registryCount(workers.reduce((n,w)=>n+(w.gpu_compute_hours||0),0))} GPU-hrs attributed` : 'Not measured'},
      {label:'Wall time',value:duration(selected)}, {label:'GPUs in parallel',value:known ? '0 used · CPU census' : 'Not recorded'}, {label:'Sources swept',value:coverage(selected)},
    ],
    censusTranscriptMessages: messages.flatMap(item => [{text:`${item.message} · ${item.reason_code}`,bg:'var(--surface)',color:'var(--ink)',radius:'11px 11px 11px 3px',ml:'0',hasMeta:true,meta:stamp(item.banked_at_utc)},
      ...(item.resolution_text ? [{text:item.resolution_text,bg:'var(--blue)',color:'var(--paper)',radius:'11px 11px 3px 11px',ml:'auto',hasMeta:true,meta:`${item.resolved_by} · ${stamp(item.resolved_at_utc)}`}]:[])]),
    censusTranscriptResolution: messages.map(item => item.state === 'PENDING' ? `${item.host_label}: response pending; the original result is preserved.` : `${item.host_label}: ${item.state}. ${item.resolution_text}`).join('\n'),
    censusEvidenceRows: [{label:'Sources checked',value:coverage(selected)},{label:'Left out',value:exclusions(selected) || 'See method and scope; no exclusion does not imply full content measurement'},
      {label:'Read by',value:workers.map(w=>w.runtime_id).join(', ') || 'Reader not retained in this historical record'}, {label:'Run by',value:selected?.initiated_by || selected?.principal_id || 'Not retained'},
      {label:'Retained evidence',value:selected?.proof_ref || selected?.output_hash || 'Awaiting published result'},
      ...(selected?.report?.groups || []).flatMap(g=>g.rows.map(r=>({label:r.label,value:`${r.status}: ${r.method} Recorded ${stamp(r.measured_at)}; ${r.population} in declared population.`}))),
    ].map(row=>({...row,color:'var(--ink2)'})),
    measuredProv: [{k:'Tenant',v:data?.tenant_id},{k:'Registry records',v:String(records.length)},{k:'Source',v:'Canonical census receipts and shared Registry projection'}],
    measuredWays: [{label:'Measured',short:'Observed by the worker; method and population retained'},{label:'Sampled',short:'Only the assessed sample, not the whole estate'},{label:'Declared',short:'Owner statement with its source, not a measured finding'},{label:'Unmeasured',short:'No qualifying measurement; never substituted with zero'}],
    measuredDeclared:'Census authority does not grant unrestricted downstream use.', measuredPopulation:'Historical snapshots remain distinct; later censuses do not overwrite earlier findings.',
  };
  return model;
}