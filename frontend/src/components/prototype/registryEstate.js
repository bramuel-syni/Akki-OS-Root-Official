import { registryBytes, registryCount, metricValue } from './registryHistory';
import { censusRequest } from '../census/useCensusWorkspace';

export function registryEstate({data,params,setParams,state,setState,show,run}) {
  const latest = data?.records?.[0];
  const sources = data?.source_details || [];
  const metrics = latest?.report?.metrics || {};
  const section = params.get('section') || 'data';
  const groups = [...new Set(sources.map(s=>s.kind))];
  const category = state.category;
  const selectCategory = kind => setState(s=>({...s,category:kind}));
  const volume = registryBytes(sources.reduce((n,s)=>n+(s.volume_bytes||0),0));
  const sourceInfo = async source => {
    setState(s=>({...s,source,sourceLoading:true,sourceError:null,sourceRelation:null}));
    try{const result=await censusRequest(`/sources/${source.source_ref}`);setState(s=>s.source?.source_ref===source.source_ref?({...s,source:result.source,sourceLoading:false}):s);}
    catch(error){setState(s=>s.source?.source_ref===source.source_ref?({...s,sourceLoading:false,sourceError:error.message}):s);}
  };
  const model = {isRegEstate:!['history','sources','models'].includes(params.get('view')),isRegMeasure:section==='data',isRegComputeTab:section==='compute',isRegLLM:section==='models',isRegModels:false,isRegConnect:false,
    regTabsView:[['data','Data Connected'],['compute','Compute Connected'],['models','LLMs & Trained Models']].map(([key,label])=>({key,label,color:section===key?'var(--ink)':'var(--ink3)',border:section===key?'var(--blue)':'transparent',onClick:()=>setParams({section:key})})),
    measureHeld:metricValue(metrics.data_held),measureRead:metricValue(metrics.share_measured),measureCare:metricValue(metrics.verified),estateCensusCount:`${data?.records?.length || 0} retained censuses`,
    estateHeldRows:groups.map(kind=>({label:kind,value:registryBytes(sources.filter(s=>s.kind===kind).reduce((n,s)=>n+(s.volume_bytes||0),0)),note:'Observed metadata; scope limitations retained'})),
    estateConditionRows:['duplicates','degraded','incomplete','stale'].map(key=>({label:metrics[key]?.label || key,value:metricValue(metrics[key]),note:metrics[key]?.method || 'Not measured'})),
    estateConditionSources:sources.filter(s=>s.status!=='complete').map(s=>({label:s.label,value:s.status,note:s.reason_code || 'Partial measurement coverage'})),
    estateConditionBar:[],regQualBar:[],regRightsBar:[],regLangBar:[],regTypeBar:groups.map(kind=>({label:kind,size:`${sources.filter(s=>s.kind===kind).length} sources`,w:`${100*sources.filter(s=>s.kind===kind).length/Math.max(1,sources.length)}%`,fill:kind==='mysql'?'var(--blue)':kind==='nas'?'var(--sage)':'var(--brass)',onClick:()=>selectCategory(kind)})),
    regNotesRef:'Every figure links to its retained census. Sampled and unmeasured portions are not presented as full estate measurements.',
    opportunitiesView:[],efGapsHook:sources.some(s=>s.status!=='complete')?'Some declared scopes remain incomplete; inspect the source records.':'Source coverage and unperformed checks remain in each census.',
    connectSourcesView:sources.map(s=>({key:s.source_ref,name:s.label,type:s.kind,rights:'Census only',rightsColor:'var(--brass)',rightsBg:'rgba(176,141,46,.14)',use:s.rights_status,declared:'No additional downstream grant is inferred',declaredBy:'Retained census authority'})),
    openMeasured:()=>setParams({view:'history'}),openMeasuredModels:()=>setParams({view:'models'}),openTraffic:()=>setParams({view:'sources'}),
    openOppDrawerNew:()=>show({title:'Things worth building',body:'No qualified opportunity briefs are linked to this census. This is unmeasured, not a finding that no opportunities exist.',code:'Not yet assessed'}),
    censusRunning:Boolean(data?.runs?.some(r=>r.status==='PENDING')),censusBtnLabel:data?.runs?.some(r=>r.status==='PENDING')?'Census running':'Run census',censusBtnOpacity:'1',runCensus:run,
    censusProgressLabel:data?.runs?.find(r=>r.status==='PENDING')?.stage || 'No active census',censusNextLabel:latest?`Latest retained result: ${latest.record_id}`:'No census has been retained',
    censusPauseNeedsInput:data?.conversations?.some(c=>c.state==='PENDING'),openCensusPause:()=>setParams({view:'history',record:data?.conversations?.find(c=>c.state==='PENDING')?.census_run_id,detail:'convo'}),
    estateFullOpen:params.get('view')==='sources',closeEstateFull:()=>setParams({}),
    estateCatalogueCount:`${sources.length} source scopes in the retained Registry`,
    estateCatalogueTitle:`${volume} enumerated across ${sources.length} source scopes.`,
    estateCatalogueBasis:latest?`Latest retained census: ${latest.record_id}`:'No census retained',
    efTopline:[{l:'Source scopes',v:String(sources.length),n:'Retained Registry scope'},{l:'Volume enumerated',v:volume,n:'Observed bytes; incomplete sources remain explicit'},{l:'Kinds',v:String(groups.length),n:'Observed source kinds'},{l:'Incomplete scopes',v:String(sources.filter(s=>s.status!=='complete').length),n:'Inspect each source for its cause'},{l:'Share measured',v:metricValue(metrics.share_measured),n:metrics.share_measured?.method || 'Not measured'}],
    efNoSelection:!category,efHasSelection:Boolean(category),regQualReading:'No complete condition classification is claimed. Method and coverage are preserved per source.',
    regFigures:[{l:'Source scopes',v:String(sources.length)},{l:'Volume enumerated',v:volume},{l:'Condition',v:'See assessed coverage'}],
    efCatsView:[{label:'Overview',count:String(sources.length),blurb:'All retained source scopes',tags:[],onClick:()=>setState(s=>({...s,category:null})),bg:!category?'var(--surface)':'#fff',color:'var(--ink)'},...groups.map(kind=>({label:kind,count:String(sources.filter(s=>s.kind===kind).length),blurb:'Measured source records',tags:[],onClick:()=>setState(s=>({...s,category:kind})),bg:category===kind?'var(--surface)':'#fff',color:'var(--ink)'}))],
    efGroupsView:groups.filter(kind=>!category||kind===category).map(kind=>({name:kind,count:`${sources.filter(s=>s.kind===kind).length} sources`,blurb:'Open a source for method, schema, sampling and rights evidence.',rows:sources.filter(s=>s.kind===kind).map(s=>({key:s.source_ref,source:s.label,meta:`${s.status} · ${s.worker_id || 'worker not recorded'}`,size:registryBytes(s.volume_bytes),rightsLabel:'Census scope',rightsColor:'var(--brass)',rightsBg:'rgba(176,141,46,.12)',dupFlagged:false,onOpen:()=>sourceInfo(s)}))})),
  };
  for(const [name,title] of [['censusRead','What was read'],['censusCare','What needs care'],['censusMix','How the estate divides'],['censusHow','How we know'],['usagePattern','Usage patterns'],['computeGraphs','Resource measurements'],['gpuCards','Connected workers'],['llmCards','Registered models'],['llmGraphs','Usage'],['llmCost','Consumption'],['llmCare','Readiness']]) {
    const open=Boolean(state[name]); model[`${name}Open`]=open;model[`${name}HeadMb`]=open?'18px':'0';model[`${name}Label`]=open?'Hide':'Show';model[`${name}Chev`]=open?'rotate(180deg)':'rotate(0deg)';
    model[`toggle${name[0].toUpperCase()+name.slice(1)}`]=()=>setState(s=>({...s,[name]:!s[name]}));
  }
  return model;
}