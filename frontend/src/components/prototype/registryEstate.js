import { registryBytes, registryCount, metricValue } from './registryHistory';
import { censusRequest } from '../census/useCensusWorkspace';
import { registryIntelligence } from './registryIntelligence';

export function registryEstate({data,params,setParams,state,setState,show,run}) {
  const latest = data?.records?.[0];
  const sources = data?.source_details || [];
  const frontier = data?.frontier;
  const exclusionNote = frontier?.excluded_scopes ? `Declared exclusions: ${Object.entries(frontier.exclusion_classes_total || {}).map(([k,v])=>`${v} ${k.replaceAll('_',' ')}`).join(', ') || 'see each source for its cause'}` : 'Every declared scope completed';
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
  const model = {...registryIntelligence({data,show}),isRegEstate:!['history','sources','models'].includes(params.get('view')),isRegMeasure:section==='data',isRegComputeTab:section==='compute',isRegLLM:section==='models',isRegModels:false,isRegConnect:false,
    regTabsView:[['data','Data Connected'],['compute','Compute Connected'],['models','LLMs & Trained Models']].map(([key,label])=>({key,label,color:section===key?'var(--ink)':'var(--ink3)',border:section===key?'var(--blue)':'transparent',onClick:()=>setParams({section:key})})),
    regRightsBar:[],regLangBar:[],regTypeBar:groups.map(kind=>({label:kind,size:`${sources.filter(s=>s.kind===kind).length} sources`,w:`${100*sources.filter(s=>s.kind===kind).length/Math.max(1,sources.length)}%`,fill:kind==='mysql'?'var(--blue)':kind==='nas'?'var(--sage)':'var(--brass)',onClick:()=>selectCategory(kind)})),
    regNotesRef:'Every figure links to its retained census. Sampled and unmeasured portions are not presented as full estate measurements.',
    connectSourcesView:sources.map(s=>({key:s.source_ref,name:s.label,type:s.kind,rights:'Census only',rightsColor:'var(--brass)',rightsBg:'rgba(176,141,46,.14)',use:s.rights_status,declared:'No additional downstream grant is inferred',declaredBy:'Retained census authority'})),
    openMeasured:()=>setParams({view:'history'}),openMeasuredModels:()=>setParams({view:'models'}),openTraffic:()=>setParams({view:'sources'}),
    censusRunning:Boolean(data?.runs?.some(r=>r.status==='PENDING')),censusBtnLabel:data?.runs?.some(r=>r.status==='PENDING')?'Census running':'Run census',censusBtnOpacity:'1',runCensus:run,
    censusProgressLabel:data?.runs?.find(r=>r.status==='PENDING')?.stage || 'No active census',censusNextLabel:latest?`Latest retained result: ${latest.record_id}`:'No census has been retained',
    censusPauseNeedsInput:data?.conversations?.some(c=>c.state==='PENDING'),openCensusPause:()=>setParams({view:'history',record:data?.conversations?.find(c=>c.state==='PENDING')?.census_run_id,detail:'convo'}),
    estateFullOpen:params.get('view')==='sources',closeEstateFull:()=>setParams({}),
    estateCatalogueCount:`${sources.length} source scopes in the retained Registry`,
    estateCatalogueTitle:`${volume} enumerated across ${sources.length} source scopes.`,
    estateCatalogueBasis:latest?`Latest retained census: ${latest.record_id}`:'No census retained',
    efTopline:[{l:'Source scopes',v:String(sources.length),n:'Retained Registry scope'},{l:'Volume enumerated',v:volume,n:'Observed bytes; incomplete sources remain explicit'},{l:'Kinds',v:String(groups.length),n:'Observed source kinds'},{l:'Incomplete scopes',v:frontier?String(frontier.excluded_scopes):String(sources.filter(s=>s.status!=='complete').length),n:frontier?exclusionNote:'Inspect each source for its cause'},{l:'Share measured',v:metricValue(metrics.share_measured),n:metrics.share_measured?.method || 'Not measured'}],
    efNoSelection:!category,efHasSelection:Boolean(category),
    regFigures:[{l:'Source scopes',v:String(sources.length)},{l:'Volume enumerated',v:volume},{l:'Condition',v:frontier?frontier.pinned_accessible_scope:'See assessed coverage'}],
    efCatsView:[{label:'Overview',count:String(sources.length),blurb:'All retained source scopes',tags:[],onClick:()=>setState(s=>({...s,category:null})),bg:!category?'var(--surface)':'#fff',color:'var(--ink)'},...groups.map(kind=>({label:kind,count:String(sources.filter(s=>s.kind===kind).length),blurb:'Measured source records',tags:[],onClick:()=>setState(s=>({...s,category:kind})),bg:category===kind?'var(--surface)':'#fff',color:'var(--ink)'}))],
    efGroupsView:groups.filter(kind=>!category||kind===category).map(kind=>({name:kind,count:`${sources.filter(s=>s.kind===kind).length} sources`,blurb:'Open a source for method, schema, sampling and rights evidence.',rows:sources.filter(s=>s.kind===kind).map(s=>({key:s.source_ref,source:s.label,meta:`${s.status} · ${s.worker_id || 'worker not recorded'}`,size:registryBytes(s.volume_bytes),rightsLabel:'Census scope',rightsColor:'var(--brass)',rightsBg:'rgba(176,141,46,.12)',dupFlagged:false,onOpen:()=>sourceInfo(s)}))})),
  };
  for(const [name,title] of [['censusRead','What was read'],['censusCare','What needs care'],['censusMix','How the estate divides'],['censusHow','How we know'],['usagePattern','Usage patterns'],['computeGraphs','Resource measurements'],['gpuCards','Connected workers'],['llmCards','Registered models'],['llmGraphs','Usage'],['llmCost','Consumption'],['llmCare','Readiness']]) {
    const open=Boolean(state[name]); model[`${name}Open`]=open;model[`${name}HeadMb`]=open?'18px':'0';model[`${name}Label`]=open?'Hide':'Show';model[`${name}Chev`]=open?'rotate(180deg)':'rotate(0deg)';
    model[`toggle${name[0].toUpperCase()+name.slice(1)}`]=()=>setState(s=>({...s,[name]:!s[name]}));
  }
  return model;
}