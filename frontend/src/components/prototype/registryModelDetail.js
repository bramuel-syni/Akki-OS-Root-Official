const printable=value=>value == null ? 'Not retained' : typeof value==='string'?value:JSON.stringify(value);

export function registryModelDetail({state,setState}) {
  const model=state.modelDetail;
  const open=state.modelEvidence;
  const metric=(key,label,value)=>({k:label,v:value,bg:'var(--surface)',border:open===key?'var(--blue)':'var(--line)',cursor:'pointer',shadow:'none',onClick:()=>setState(s=>({...s,modelEvidence:s.modelEvidence===key?null:key}))});
  return {mrDetailDrawer:Boolean(model),mrCloseDetail:()=>setState(s=>({...s,modelDetail:null,modelEvidence:null})),mrDetailVM:{
    name:model?.name,origin:model?.provider || 'Provider unrecorded',originBg:'var(--surface2)',originColor:'var(--ink2)',
    licence:printable(model?.licence),licenceBg:'rgba(176,141,46,.12)',licenceColor:'var(--brass)',
    statusLabel:'Registered',pillBg:'var(--surface2)',pillColor:'var(--ink2)',hasCode:Boolean(model?.model_id),code:model?.model_id,
    metaLine:`Registry version ${model?.registry_version || 'not retained'}`,
    hasBanner:true,bannerText:'This versioned record is not proof of admission, deployed weights or live capability. Missing measurements are not substituted.',bannerBg:'rgba(176,141,46,.10)',bannerColor:'var(--brass)',
    insight:'Inventory and operational qualification remain distinct. This view does not silently commission a model or change a serving configuration.',
    metrics:[metric('admission','Admission','Not established here'),metric('usage','Calls','Not measured'),metric('latency','Latency','Not measured'),metric('quality','Quality','Not evaluated here')],
    hasMetricsNote:true,metricsNote:'No latency, token allowance, refusal rate, bill or achieved capability is inferred from a registry entry.',
    expandOpen:Boolean(open),expandSummary:open?`${open}: the source registry record does not supply qualified runtime evidence for this measure.`:'',
    answerOpen:open==='usage',answerCards:[],refusalOpen:false,refusalRows:[],refusalTotal:'Not measured',maskedOpen:false,
    trendOpen:false,trendPoints:'',trendDots:[],trendLabels:[],hasTrendNote:false,hasTrendRange:false,trendRange:'',trendNote:'No qualified series',trendClose:()=>setState(s=>({...s,modelEvidence:null})),
    what:'Versioned model inventory retained by the existing registry.',tier:'Not operationally qualified in this view',tierNote:'Candidate selection is not a serving or quality guarantee.',
    onShield:()=>setState(s=>({...s,modelEvidence:'admission'})),hasTrainLink:false,onTrain:()=>setState(s=>({...s,modelEvidence:'training'})),
    provTitle:'Recorded provenance',provRows:[{k:'Model',v:model?.model_id},{k:'Provider',v:printable(model?.provider)},{k:'Licence',v:printable(model?.licence)},{k:'Pinned model hash',v:printable(model?.model_hash)},{k:'Provenance',v:printable(model?.provenance)},{k:'Registry version',v:String(model?.registry_version || 'Unrecorded')}],
    custodyRef:printable(model?.model_hash),custodyPath:'Registry record → admission → runtime → qualified use',custodyPathNote:'Only the registry step is established here.',custodyWhen:'Version as above',
    custodyStages:[{k:'Registry',v:'Recorded'},{k:'Admission',v:'Not established here'},{k:'Runtime',v:'Not established here'},{k:'Evaluation',v:'Not established here'}],
    receipt:printable(model?.model_hash),receiptNote:'A model hash is not an admission or execution receipt.',admBadge:'Not established',admBadgeBg:'rgba(176,141,46,.12)',admBadgeColor:'var(--brass)',admEvents:[],
    checks:[['Identity',model?.model_id],['Licence',model?.licence],['Model hash',model?.model_hash],['Provenance',model?.provenance]].map(([label,value])=>({label,mark:value?'·':'—',color:value?'var(--ink)':'var(--brass)',weight:'500',note:value?'Recorded, not independently qualified':'Not retained',noteColor:'var(--ink3)',hasDetail:true,detail:printable(value)})),
  }};
}