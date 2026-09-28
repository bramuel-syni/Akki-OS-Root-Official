import { disclosure, unknownStats } from './nexusShared';
import { watchSections } from './osHierarchy';

export function nexusMirrorModel({ section, state, setState, navigate, params, unavailable }) {
  const watching = section !== 'overview';
  const tab = state.mirrorTab || 'overview';
  const mainTabs = [['overview','Overview'],['monitor','Monitor & detect'],['response','Respond'],['people','Users & models'],['watch','The Watch']];
  const links = watching ? watchSections.map(s => [s.key,s.label]) : mainTabs;
  const current = watching ? section : tab;
  const change = key => {
    if (watching) navigate(watchSections.find(s=>s.key===key).path + (params.toString() ? '?' + params : ''));
    else if (key === 'watch') navigate('/os/admin/greymirror/watch/state' + (params.toString()?'?'+params:''));
    else setState(s=>({...s,mirrorTab:key}));
  };
  return {
    appTitle:'Grey Mirror', appGroupLabel:watching?'The Watch':'Manage Estate',
    exitApp:()=>navigate(watching?'/os/admin/greymirror'+(params.toString()?'?'+params:''):'/os?nav=admin&app=greymirror'),
    isGreyMirror: !watching || section === 'state', gmIsFullRecord: Boolean(state.fullRecord),
    gmTabsView: links.map(([key,label])=>({key,label,active:current===key,color:current===key?'var(--ink)':'var(--ink3)',border:current===key?'var(--blue)':'transparent',onClick:()=>change(key)})),
    gmTopEyebrow: watching ? 'The Watch — State' : mainTabs.find(([k])=>k===tab)?.[1],
    gmTopOneliner:'Current security and response records are not connected. No activity, health verdict or successful action is inferred.',
    gmStats:unknownStats(['Waiting for you','People and agents','Open sessions']),gmStatsG2:unknownStats(['Allowed','Refused','Flagged']),gmStatsG3:unknownStats(['Checks passed','Exceptions','Recovery']),
    gmG2Title:'What was let through, and what was not',gmG2Sub:'The outcomes recorded by the owning services.',
    gmG3Title:'Is the watch itself working',gmG3Sub:'Checks and recovery evidence, not a self-reported health claim.',
    gmVisualEyebrow:'How it is moving',gmVisualOneliner:'Trends require measured records.',gmChartTitle:'Measured activity',gmChartCaption:'No connected measurements',
    gmChartOptions:[{key:'activity',label:'Activity'},{key:'responses',label:'Responses'}],gmChart:state.chart||'activity',gmChartChange:e=>setState(s=>({...s,chart:e.target.value})),gmChartRows:[],
    gmVisualFoot:'No trend has been calculated.',gmTableEyebrow:'The record',gmTableOneliner:'Every outcome needs its original evidence.',gmTableTitle:'Current record',gmNarrative:'Awaiting the native record.',
    gmFiltersView:['All','Held','Refused','Released'].map(label=>({label,bg:state.mirrorFilter===label?'var(--blue)':'#fff',color:state.mirrorFilter===label?'var(--paper)':'var(--ink3)',border:'var(--line)',onClick:()=>setState(s=>({...s,mirrorFilter:label}))})),
    gmIsPeople:tab==='people'&&!watching,gmIsLedger:tab!=='people'||watching,gmIsRollup:false,gmRowsView:[],gmPeopleRowsView:[],
    gmCol1:'What happened',gmCol2:'Actor',gmCol3:'Outcome',gmCol4:'When',
    gmHeadEyebrow:'What is happening right now',gmHeadDeck:'The native Watch record is unavailable.',gmHeadSub:'No enforcement, monitoring or notification is claimed here.',
    gmRailSub:'Evidence and actions from the same record',gmBack:()=>navigate('/os/admin/greymirror'),
    viewAllGm:()=>unavailable('The full record','A connected, tenant-authorised Watch ledger is required. No record has been substituted.'),
    openActorWiz:()=>unavailable('Add user / model','Identity admission needs the original identity service and its authorised signers. No account or permission has been created.'),
    ...disclosure(state,'gmG2',setState),...disclosure(state,'gmG3',setState),...disclosure(state,'gmCharts',setState),...disclosure(state,'gmTable',setState,true),
    isWatchGroup:watching&&section!=='state',isWatchRecord:section==='record',isWatchUnder:section==='under-watch',isWatchDecisions:section==='decisions',
    hasPageTopline:true,pageEyebrow:'Grey Mirror · The Watch',pageHeadline:watchSections.find(s=>s.key===section)?.label || '',pageSub:'Awaiting connected records',
    recordLanesView:['All','Observation','Action','Decision'].map(label=>({label,border:'var(--line)',color:state.lane===label?'var(--blue)':'var(--ink3)',onClick:()=>setState(s=>({...s,lane:label}))})),
    recordLaneCopy:'No Watch record is connected.',recordRowsView:[],patternsView:[],decisionsView:[],decisionsFooter:'No decisions have been loaded or signed.',
    decisionNote:state.decisionNote||'',decisionNoteChange:e=>setState(s=>({...s,decisionNote:e.target.value})),
    mirageCopy:'No copy-session evidence is connected.',markedCopy:'No marking or demarking decision has been verified.',mirageFindings:[],
    onRequestDemark:()=>unavailable('Request review','An existing marked subject and its evidence are required before requesting review.'),
    drillChipLabel:'Live record',drillChipBg:'var(--surface2)',toggleDrills:()=>unavailable('Recovery evidence','No physical-host drill or recovery claim has been loaded.'),
  };
}