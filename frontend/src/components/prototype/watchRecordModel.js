import { stamp } from './evidence';

export function watchRecordModel({data,error,state,show,navigate,refresh}) {
  if(!data) return error?{gmTopOneliner:error,recordLaneCopy:error,pageSub:error}:{};
  const walk = row => show({title:row.title,subtitle:row.record_id,code:row.state,
    body:`${row.basis}. ${row.evidence_ref?`Evidence: ${row.evidence_ref}`:'No terminal evidence retained yet.'}`,
    next:'Reading this record does not acknowledge, release or change active protection.',
    actions:row.census_run_id?[{label:'Open census',bg:'var(--blue)',color:'var(--paper)',border:'var(--blue)',onClick:()=>navigate(`/os/admin/estate?view=history&record=${encodeURIComponent(row.census_run_id)}`)}]:[]});
  const records = data.records || [];
  const filter = state.mirrorFilter || 'All';
  const filtered = records.filter(r=>filter==='All'||(filter==='Refused'&&r.state==='REFUSED')||(filter==='Held'&&r.state==='PENDING')||(filter==='Released'&&r.state==='Released'));
  const lanes = {Observation:'observation',Action:'action',Decision:'decision'};
  const laneRows = records.filter(r=>!state.lane||state.lane==='All'||r.kind===lanes[state.lane]);
  const details = ()=>show({title:'Watch coverage',code:'Qualification pending',body:`${data.coverage}. ${data.detector_status}. ${data.witness_status}.`,next:'Recorded observations are not proof of detection, enforcement, release or delivery.'});
  return {
    gmIsLedger:true,gmIsRollup:false,gmCol1:'Record',gmCol3:'State',
    drillChipLabel:'Refresh record',
    gmTopOneliner:data.coverage,gmHeadDeck:`${data.counts.observations} retained census observations · ${data.counts.gate_crossings??0} gate crossings · ${data.counts.gate_effects??0} enforced effects`,
    gmHeadSub:data.enforcement_status,gmTableTitle:'Tenant record',gmNarrative:filtered.length?'Observations and Watch records remain distinct.':'No records match this filter.',
    gmRowsView:filtered.map(r=>({key:r.record_id,text:r.title,state:r.state,stateBg:'var(--surface2)',stateColor:'var(--ink)',actor:r.actor,when:stamp(r.observed_at),meta:r.basis,link:'Walk this →',onOpen:()=>walk(r)})),
    recordLaneCopy:`${laneRows.length} records · ${data.coverage}`,
    recordRowsView:laneRows.map(r=>({key:r.record_id,text:r.title,meta:`${r.state} · ${stamp(r.observed_at)} · ${r.basis}`,bg:'#fff',border:'var(--line)',color:'var(--ink)',hasWalk:true,hasNotice:false,onWalk:()=>walk(r)})),
    pageSub:data.enforcement_status,gmVisualAsideTitle:'Coverage',gmVisualAsideBody:data.coverage,
    gmTableAsideTitle:'Evidence',gmTableAsideBody:data.witness_status,
    viewAllGm:()=>navigate('/os/admin/greymirror/watch/record'),openBriefGm:details,openBriefGmVisual:details,openBriefGmTable:details,toggleDrills:refresh,
  };
}