import { registryBytes, registryCount } from './registryHistory';
import { stamp } from './evidence';

export function registrySourceProfile({state,setState}) {
  const source=state.source;
  const tables=Object.entries(source?.composition?.per_table || {});
  const tableTotal=tables.reduce((n,[,t])=>n+(t.row_count || 0),0);
  const languages=source?.sample?.languages || {};
  const languageTotal=Object.values(languages).reduce((a,b)=>a+b,0);
  const types={}; for(const [,table] of tables)for(const column of table.columns || [])types[column.data_type]=(types[column.data_type] || 0)+1;
  const entries=Object.entries(state.sourceMix==='language'?languages:types);
  const denominator=state.sourceMix==='language'?languageTotal:Object.values(types).reduce((a,b)=>a+b,0);
  const relation=state.sourceRelation;
  return {
    efProfileOpen:Boolean(source),efDeniedOpen:Boolean(state.sourceError),efDeniedName:source?.label,
    efDeniedBack:()=>setState(s=>({...s,source:null,sourceError:null})),efCloseProfile:()=>setState(s=>({...s,source:null,sourceRelation:null})),efHasBack:Boolean(relation),efProfileBack:()=>setState(s=>({...s,sourceRelation:null})),
    efProfileVM:{header:{name:source?.label,rightsLabel:'Census authority only',rightsBg:'rgba(176,141,46,.14)',rightsColor:'var(--brass)',rightsItalic:'normal',typeLabel:source?.kind,isDegraded:false},
      description:state.sourceLoading?'Loading the retained source measurements…':source?.method || source?.reason_code,
      metrics:[{k:'Volume observed',v:registryBytes(source?.volume_bytes)},{k:'Records (estimate)',v:registryCount(source?.row_count_estimate)},{k:'Tables',v:registryCount(source?.table_count)},{k:'Fields',v:registryCount(source?.column_count)},
        {k:'Assessed rows',v:registryCount(source?.sample?.rows)},{k:'Files / objects',v:registryCount(source?.file_count ?? source?.object_count)},{k:'Status',v:source?.status || 'Not retained'},{k:'Observed',v:stamp(source?.observed_at)}],
      proof:relation?`Candidate linkage evidence: ${JSON.stringify(relation)}. Descriptive only; this does not confer access or establish a resolved join.`:`${source?.proof_ref || 'Awaiting receipt'}. Worker: ${source?.worker_id || 'not recorded'}. Structure fingerprint: ${source?.structure_sha256 || 'not applicable or unmeasured'}.`,
      qualityState:'Assessed checks retained; full quality classification not established',
      qualityReason:source?.sample?`${source.sample.rows} bounded sampled rows; ${source.sample.pii_rows} with detected PII; ${source.sample.incomplete_rows} with a null in assessed fields. A null in an optional field is not a required-field failure. ${source.profile?.totals?JSON.stringify(source.profile.totals):''}`:'No qualifying row-quality measurements are retained for this source.',
      hasPerception:['nas','object_store'].includes(source?.kind),perception:`${source?.method || ''}. Inspected media: ${source?.media_samples ?? 'unmeasured'}; duration ${source?.media_duration_seconds ?? 'unmeasured'} seconds refers only to the inspected sample.`,
      mixTabs:[['type','Field types'],['language','Language — assessed sample']].map(([key,label])=>({key,label,color:(state.sourceMix || 'type')===key?'var(--ink)':'var(--ink3)',border:(state.sourceMix || 'type')===key?'var(--blue)':'transparent',onClick:()=>setState(s=>({...s,sourceMix:key}))})),
      mixRows:entries.length?entries.map(([label,count])=>({label,pct:`${registryCount(count)} assessed`,w:`${denominator?100*count/denominator:0}%`})):[{label:'Not measured',pct:'No estimate substituted',w:'0%'}],
      hasRelationships:Boolean(source?.relationships?.length),relationships:(source?.relationships || []).map((item,index)=>({name:item.signal_name || `Candidate ${index+1}`,typeLabel:'Candidate linkage',typeBg:'var(--surface2)',typeColor:'var(--ink2)',hasConfidence:true,confidence:`score ${item.confidence}`,confColor:'var(--brass)',evidence:`${item.source_ref} · ${item.evidence_class} · ${item.detector_version}`,isDup:false,onOpen:()=>setState(s=>({...s,sourceRelation:item}))})),
      hasRecommended:false,recommended:[],hasStale:false,hasTables:tables.length>0,
      tablesBars:tables.map(([label,table])=>({label,records:`${registryCount(table.row_count)} estimated`,w:`${tableTotal?100*(table.row_count || 0)/tableTotal:0}%`})),
      isPerceptionContents:['nas','object_store'].includes(source?.kind),
      contentsStructured:tables.map(([table,value])=>({table,records:`${registryCount(value.row_count)} est.`,fields:registryCount(value.column_count),pii:'Sample evidence above',quality:'See assessed checks',lastCensus:stamp(source?.observed_at)})),
      contentsPerception:Object.entries(source?.formats || {}).map(([group,count])=>({group,records:registryCount(count),pii:'Unmeasured',quality:'See inspected coverage',rule:'Not classified',confidence:'Unmeasured',grounding:source?.source_ref})),
    },
  };
}