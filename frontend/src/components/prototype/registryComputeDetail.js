import { registryCount } from './registryHistory';
import { stamp } from './evidence';

export function registryComputeDetail({data,state,setState}) {
  const records=(data?.records || []).filter(r=>r.workers?.length);
  const metric=state.computeMetric || 'hours';
  const tab=state.computeTab || 'door';
  const update=values=>setState(s=>({...s,...values}));
  const rows=records.map(r=>({id:r.record_id,label:r.census_number?`Census #${r.census_number}`:r.record_id,
    hours:r.workers.reduce((n,w)=>n+(w.gpu_compute_hours || 0),0),wall:r.workers.reduce((n,w)=>n+(w.wall_seconds || 0),0),stamp:stamp(r.finished_at),
    workers:r.workers.map(w=>w.runtime_id).join(', ')}));
  return {loadOpen:Boolean(state.loadOpen),openLoad:()=>update({loadOpen:true}),closeLoad:()=>update({loadOpen:false}),
    loadTabsView:[['door','By door'],['week','By month'],['state','By state'],['lever','By cost lever']].map(([key,label])=>({label,color:tab===key?'var(--ink)':'var(--ink3)',border:tab===key?'var(--blue)':'transparent',onClick:()=>update({computeTab:key})})),
    loadIsDoorTab:tab==='door',loadIsNotDoorTab:tab!=='door',loadShowBarTrend:true,loadShowMetricToggle:true,loadHasLegend:false,loadHasHatch:false,loadHasUnit:true,loadHasBInsight:true,
    loadPrimaryTitle:metric==='hours'?'Run-attributed GPU hours':'Recorded spend',loadPrimarySubtitle:'Only retained census execution receipts; no estimate of whole-device use.',
    loadRows:tab==='week'?rows.map(r=>({label:r.stamp,hrs:`${registryCount(r.hours)} GPU-hrs`,spend:'Not measured',hrsWeight:metric==='hours'?'600':'400',spendWeight:metric==='spend'?'600':'400',hasSaving:false,saving:'',size:'0%',pct:r.hours===0?'CPU census; zero attributed GPU work':'See receipt',fill:'var(--sage)'})):(tab==='state'?['BUSY — running now','IDLE — free to allocate','Queued, waiting on a card']:['Recorded cost levers']).map(label=>({label,hrs:'Not measured',spend:'Not measured',hrsWeight:'400',spendWeight:'400',hasSaving:false,size:'0%',pct:'No allocation or saving inferred',fill:'var(--blue)'})),
    loadBCaption:'These workers run the current census on CPU. Device presence is not GPU consumption; monetary cost is not supplied by the execution receipts.',
    loadBInsight:'Zero attributed GPU work is not a claim that every device was idle. Wall time and transport identity remain attached to each census.',
    loadConnector1:'Each retained work record keeps its original resource observation.',loadUnitConnector:'Qualified units and their commercial terms are not inferred from metadata row totals.',
    loadTTitle:'Retained census observations',loadTCaption:rows.length?`${rows.length} completed or partial worker-backed records; no synthetic trend points.`:'No worker-backed records retained yet.',
    loadPeriods:rows.map(r=>({label:r.stamp,total:metric==='hours'?`${registryCount(r.hours)} GPU-hrs`:'Not measured',pad:'0',segs:[{h:'0px',fill:'var(--sage)',isHovered:state.computeHover===r.id,tip:`${r.label}: ${registryCount(r.wall)} worker wall-seconds; ${r.workers}`,onEnter:()=>update({computeHover:r.id}),onLeave:()=>update({computeHover:null})}]})),
    loadLegend:[],loadHatchNote:'No projection is made.',loadUnitTitle:'Execution basis',loadUnitCaption:'CPU census; qualified-unit cost is not measured.',loadUnitPoints:'',loadUnitDots:[],loadUnitLabels:[],loadUnitNote:'A database estimate, source count or device snapshot is not a billable qualified unit.',
    loadRefs:rows.map(r=>({label:r.label,meta:`${r.stamp} · ${registryCount(r.wall)} wall-seconds · ${r.workers}`})),loadDoorRows:['Train','Extract','Export','Measure','Prove'].map(label=>({label,hrs:label==='Measure'&&rows.length?'0 GPU-hrs attributed':'Not measured',spend:'Not measured',hrsWeight:'500',spendWeight:'400',fill:'var(--sage)',size:'0%',pct:'Not an estate-wide usage share',hasSaving:false})),
    setMetricHours:()=>update({computeMetric:'hours'}),setMetricSpend:()=>update({computeMetric:'spend'}),
    metricHoursBg:metric==='hours'?'var(--surface)':'transparent',metricHoursColor:metric==='hours'?'var(--ink)':'var(--ink3)',metricHoursHoverBg:'var(--surface)',metricHoursShadow:'none',
    metricSpendBg:metric==='spend'?'var(--surface)':'transparent',metricSpendColor:metric==='spend'?'var(--ink)':'var(--ink3)',metricSpendHoverBg:'var(--surface)',metricSpendShadow:'none',
  };
}