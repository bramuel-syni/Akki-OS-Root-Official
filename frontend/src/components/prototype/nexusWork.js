import { osWorkModel } from './osWorkModel';
import { unknownStats } from './nexusShared';
import { stamp } from './evidence';

const tabs = [['today', 'Today'], ['team', 'My team'], ['records', 'The work'], ['score', 'Execution score'],
  ['sources', 'Sources & governance'], ['goals', 'Company Goals'], ['board', 'Board']];

export function nexusWorkModel({ work, section, state, setState, params, navigate, setParams, unavailable, show }) {
  const tab = section === 'records' ? params.get('tab') || 'records' : section;
  const view = params.get('view') || '';
  const isWorkspace = section === 'records' && Boolean(params.get('request')) && view !== 'all';
  const query = value => { const next = new URLSearchParams(params); Object.entries(value).forEach(([k, v]) => v == null ? next.delete(k) : next.set(k, v)); setParams(next); };
  const toggle = key => setState(s => ({ ...s, [key]: !(s[key] ?? false) }));
  const base = osWorkModel({ work, navigate, setParams: value => query({ ...value, view: null }), section, disclosure: state, toggle });
  const filtered = work.rows.filter(r => (state.filter !== 'held' || r.state === 'routing') && (state.filter !== 'ready' || r.execution_verified)
    && (!state.search || `${r.objective_text} ${r.work_id}`.toLowerCase().includes(state.search.toLowerCase())));
  const byId = new Map(filtered.map(row=>[row.request_id,row]));
  const rows = base.tmFilteredView.filter(r => byId.has(r.requestId));
  const selected = work.selected;
  const selectedOrRow = selected || work.rows.find(r => r.request_id === params.get('request'));
  const goTab = key => { const next = new URLSearchParams(params); next.delete('view');
    if (['today', 'records', 'score', 'sources'].includes(key)) { next.set('tab', key); navigate('/os/work/tasks?' + next); }
    else { next.delete('tab'); navigate(`/os/work/tasks/${key}?` + next); } };
  const prod = {};
  for (const [key, suffix, initial] of [['pri','Pri',true],['fol','Fol',false],['adm','Adm',false],['int','Int',true],['appr','Appr',false],['pipe','Pipe',false],['brk','Brk',true],['exc','Exc',false],['src','Src',true],['gov','Gov',false]]) {
    const open = state['prod-'+key] ?? initial;
    Object.assign(prod, { ['prodSec'+suffix]: open, ['prodSec'+suffix+'Label']: open ? 'Hide' : 'Show',
      ['prodSec'+suffix+'Chev']: open ? 'rotate(180deg)' : 'rotate(0deg)', ['prodSec'+suffix+'Mb']: open ? '14px' : '0',
      ['toggleProd'+suffix]: () => setState(s => ({ ...s, ['prod-'+key]: !(s['prod-'+key] ?? initial) })) });
  }
  return { ...base, ...prod, isTasksActive: true, prodIsWork: tab === 'records' && view !== 'create',
    prodIsToday: tab === 'today' && view !== 'create', prodIsTeam: tab === 'team', prodIsScore: tab === 'score', prodIsSources: tab === 'sources',
    prodTabsView: tabs.map(([key,label]) => ({ key,label,active:key===tab,color:key===tab?'var(--ink)':'var(--ink3)',border:key===tab?'var(--ink)':'transparent',onClick:()=>goTab(key) })),
    tmListMode: !isWorkspace && view !== 'all', tmWorkspaceOpen: isWorkspace, tmFullOpen: view === 'all',
    tmFilteredView: rows.slice(0, 3), tmFilteredEmpty: work.recordsAvailable && !work.loading && !rows.length,
    tmHasMore: rows.length > 3, tmMoreLabel: `View all ${rows.length} tasks →`, openTmFull: () => query({ view: 'all' }), closeTmFull: () => query({ view: null }),
    tmFullSearch: state.search || '', tmFullSearchChange: e => setState(s => ({ ...s, search: e.target.value })),
    tmFullGroups: view === 'all' ? ['routing', 'executing', 'ready', 'failed', 'cancelled'].map(key => ({ key,label:key,dot:'var(--ink3)',
      rows:rows.filter(r=>byId.get(r.requestId)?.state===key),count:filtered.filter(f=>f.state===key).length })).filter(g=>g.count) : [],
    tmFullEmpty: work.recordsAvailable && !work.loading && !rows.length, tmFullCount: work.recordsAvailable ? `${rows.length} recorded tasks` : 'Loading records…',
    tmFullLede: 'The same recorded work, with its current state and supporting evidence.', tmTiles: base.taskStats.map(s=>({l:s.label,v:s.value,n:s.subline})),
    tmFilterTabsView: [['all','All work'],['held','Needs you'],['ready','Verified execution']].map(([key,label])=>({ key,label,color:(state.filter||'all')===key?'var(--paper)':'var(--ink3)',
      border:'var(--line)',bg:(state.filter||'all')===key?'var(--ink)':'#fff',onClick:()=>setState(s=>({...s,filter:key})) })),
    setTaskTabCreate: () => query({ view:'create', request:null }), setTaskTabManage: () => query({ view:null, request:null, tab:'records' }),
    isTaskCreate: view === 'create', prodRailIsWork: ['records','board','goals'].includes(tab), prodRailNotWork: !['records','board','goals'].includes(tab),
    prodDateLabel: new Date().toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long'}),
    prodTodayStats: unknownStats(['Due today','Overdue','Waiting on others','Done today']), prodTeamStats: unknownStats(['Team items open','Overdue or blocked','Approvals on you','Timesheets not in']),
    prodScoreStats: unknownStats(['Execution score','Closed this month','Closed late','Not counted']),
    prodSourceStats: unknownStats(['Sources connected','Items generated today','Corrected by you','On the audit trail']),
    prodPriorities: [], prodFollowups: [], prodAdmin: [], prodTeamRows: [], prodApprovals: [], prodPipeline: [], prodSources: [], prodAudit: [],
    prodPrioritiesEmpty:false,prodFollowupsEmpty:false,prodAdminEmpty:false,prodScoreTotal:'—',prodScoreParts:[],
    prodRailHead: work.loading ? 'Loading the current work record…' : 'Source-backed records for this view are not connected yet.',
    prodRailLines:[{label:'Recorded work',value:work.recordsAvailable?String(work.rows.length):'—',note:'The work tab remains available; no source activity is inferred.'}],
    prodAsks:[{key:'blocked',label:'What is holding this work?',onClick:()=>selectedOrRow?show({title:selectedOrRow.reason_code,body:selectedOrRow.reason,next:selectedOrRow.next_action,code:'Work record'}):goTab('records')}],
    closeTaskWorkspace:()=>query({request:null,view:null}), wsName:selectedOrRow?.objective_text || (work.detailLoading?'Loading task…':'Task unavailable'),
    wsMeta:selectedOrRow?.work_id || '',wsObjective:selectedOrRow?.objective_text || '', wsPct:0,wsBarColor:'var(--ink3)',
    wsEvidenceLine:selectedOrRow?.execution_verified?'Execution receipt verified; task-level evidence requires its own acceptance.':'Execution evidence has not been verified.',
    wsDue:'Not supplied',wsCadence:'Not supplied',wsItems:[],wsTeam:[],wsDocs:[],wsQuestions:[],
    wsLog:selected?.history?.map((event,i)=>({key:String(i),tag:event.event,color:'var(--ink3)',text:`${stamp(event.at)} · ${event.event} · ${event.receipt_ref}`})) || [],
    wsRunCycle:()=>selectedOrRow&&show({title:selectedOrRow.reason_code,body:selectedOrRow.reason,next:selectedOrRow.next_action,code:'Current hold',actions:[{
      label:'Review governing record',bg:'var(--blue)',color:'var(--paper)',border:'var(--blue)',onClick:()=>navigate(`/dap/history?request=${encodeURIComponent(selectedOrRow.request_id)}`)}]}),
    wsObjEditing:false,wsObjEditLabel:'Review objective',wsToggleObjEdit:()=>unavailable('Frozen objective','This objective is already part of a recorded request. A change requires a separately reviewed request; the existing record will not be overwritten.'),
    evidenceKinds:[{value:'Recorded source'},{value:'Authorised approval'},{value:'Measured result'}],
  };
}