import { stamp } from './evidence';

const STATE_TONE = {'In effect':['var(--ink)','var(--paper)'],Held:['#7a1f1f','var(--paper)'],Released:['var(--surface2)','var(--ink3)'],Open:['var(--blue)','var(--paper)']};
const WALK_STEPS = [['signal','Signal'],['verdict','Verdict'],['policy','Policy row'],['action','Action'],['outcome','Outcome'],['witness','Witness']];

export function walkBody(row) {
  if(!row.walk) return `${row.basis}. ${row.evidence_ref?`Evidence: ${row.evidence_ref}`:'No terminal evidence retained yet.'}`;
  const steps = WALK_STEPS.map(([key,label])=>`${label}: ${row.walk[key] || 'MISSING — the walk cannot complete'}`);
  return `${row.basis}. ${steps.join(' · ')}.`;
}

export function watchRecordModel({data,error,state,show,navigate,refresh}) {
  if(!data) return error?{gmTopOneliner:error,recordLaneCopy:error,pageSub:error}:{};
  const walk = row => show({title:row.title,subtitle:row.record_id,code:row.walk?(row.walk.complete?row.state:'Walk incomplete'):row.state,
    body:walkBody(row),
    next:'Reading this record does not acknowledge, release or change active protection.',
    actions:[...(row.census_run_id?[{label:'Open census',bg:'var(--blue)',color:'var(--paper)',border:'var(--blue)',onClick:()=>navigate(`/os/admin/estate?view=history&record=${encodeURIComponent(row.census_run_id)}`)}]:[]),
      ...(row.kind==='decision'?[{label:'Open Decisions',bg:'var(--blue)',color:'var(--paper)',border:'var(--blue)',onClick:()=>navigate('/os/admin/greymirror/watch/decisions')}]:[])]});
  const notice = row => show({title:'The notice we sent',subtitle:row.notice.notice_id,code:row.notice.kind,body:row.notice.text,
    next:`Sent ${stamp(row.notice.at)} to ${row.notice.principal_id} · ${row.notice.posture}`});
  const records = data.records || [];
  const filter = state.mirrorFilter || 'All';
  const filtered = records.filter(r=>filter==='All'||(filter==='Refused'&&['REFUSED','Refused','Declined'].includes(r.state))||(filter==='Held'&&['PENDING','In effect','Held','Open'].includes(r.state))||(filter==='Released'&&['Released','Executed'].includes(r.state)));
  const lanes = {Observation:'observation',Action:'action',Decision:'decision'};
  const laneRows = records.filter(r=>!state.lane||state.lane==='All'||r.kind===lanes[state.lane]||(state.lane==='Action'&&r.kind==='verdict'));
  const details = ()=>show({title:'Watch coverage',code:'Never all-clear',body:`${data.coverage}. ${data.detector_status}. ${data.witness_status}. ${data.never_all_clear}`,
    next:'Recorded observations are not proof of detection, enforcement, release or delivery.'});
  const tone = r => STATE_TONE[r.state] || ['var(--surface2)','var(--ink)'];
  return {
    gmIsLedger:true,gmIsRollup:false,gmCol1:'Record',gmCol3:'State',
    drillChipLabel:'Refresh record',
    gmTopOneliner:data.never_all_clear,gmHeadDeck:`${data.counts.observations} retained census observations · ${data.counts.gate_crossings??0} gate crossings · ${data.counts.gate_effects??0} enforced effects · ${data.counts.gate_releases??0} releases`,
    gmHeadSub:data.enforcement_status,gmTableTitle:'Tenant record',gmNarrative:filtered.length?'Observations, verdicts, actions and decisions remain distinct rows; a row whose walk cannot complete says so.':'No records match this filter.',
    gmRowsView:filtered.slice(0,40).map(r=>({key:r.record_id,text:r.title,state:r.state,stateBg:tone(r)[0],stateColor:tone(r)[1],actor:r.actor,when:stamp(r.observed_at),meta:r.walk&&!r.walk.complete?`${r.basis} · walk incomplete (no witness)`:r.basis,link:'Walk this →',onOpen:()=>walk(r),resolved:r.state==='Released'||r.state==='Executed'})),
    recordLaneCopy:`${laneRows.length} records · ${data.counts.gate_crossings??0} gate crossings · ${data.counts.gate_effects??0} enforced effects · ${data.counts.gate_releases??0} releases · lanes: noted-only, acted, held · ${data.coverage}`,
    recordRowsView:laneRows.map(r=>({key:r.record_id,text:`${r.title}${r.lane?` · ${r.lane}`:''}`,meta:`${r.state} · ${stamp(r.observed_at)} · ${r.basis}`,bg:r.lane==='held'?'#fbf3f3':'#fff',border:r.lane==='held'?'#7a1f1f':'var(--line)',color:'var(--ink)',hasWalk:true,hasNotice:Boolean(r.notice),onWalk:()=>walk(r),onNotice:()=>notice(r)})),
    pageSub:data.enforcement_status,gmVisualAsideTitle:'Coverage',gmVisualAsideBody:data.coverage,
    gmTableAsideTitle:'Evidence',gmTableAsideBody:data.witness_status,
    viewAllGm:()=>navigate('/os/admin/greymirror/watch/record'),openBriefGm:details,openBriefGmVisual:details,openBriefGmTable:details,toggleDrills:refresh,
  };
}
