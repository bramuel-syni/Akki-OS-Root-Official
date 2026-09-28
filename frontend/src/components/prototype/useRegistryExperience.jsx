import React, { useCallback, useEffect, useState } from 'react';
import { NexusFragment } from './NexusFragment';
import { registryHistory } from './registryHistory';
import { registryEstate } from './registryEstate';
import { registryCompute } from './registryCompute';
import { registryConnect } from './registryConnect';
import { registrySourceProfile } from './registrySourceProfile';
import { registryResponse } from './registryResponse';
import { registryModelDetail } from './registryModelDetail';
import { registryComputeDetail } from './registryComputeDetail';
import { ownerDrawer } from './nexusShared';
import { censusRequest } from '../census/useCensusWorkspace';
import './registryOwner.css';

export function useRegistryExperience({data,params,setParams,baseModel,run,reload,active}) {
  const [owned,setOwned]=useState({owner:null,value:{}});
  const state=owned.owner===data?.principal_id?owned.value:{};
  const sourceOpen=Boolean(state.source);
  const setState=useCallback(updater=>setOwned(previous=>({owner:data?.principal_id,value:updater(previous.owner===data?.principal_id?previous.value:{})})),[data?.principal_id]);
  const show=value=>setState(previous=>({...previous,drawer:value}));
  const close=useCallback(()=>setState(previous=>({...previous,drawer:null})),[setState]);
  const refresh=async()=>{
    if(state.refreshing)return;
    setState(s=>({...s,refreshing:true}));
    try{await censusRequest('/compute/refresh',{method:'POST'});reload();}
    catch(error){show({title:'Worker observation',body:error.message,code:'Not completed'});}
    finally{setState(s=>({...s,refreshing:false}));}
  };
  // useCensusWorkspace already polls committed work. Never create a competing
  // interval which aborts the same in-flight overview on every tick.
  useEffect(()=>{
    if(!state.drawer&&!state.connectOpen&&!state.source&&!state.responseItem&&!state.modelDetail&&!state.loadOpen)return undefined;
    const previous=document.activeElement;
    const container=document.querySelector('[data-testid="registry-compute-detail"], [data-testid="registry-model-detail"], [data-testid="registry-response-dialog"], [data-testid="registry-source-profile"], [data-testid="registry-evidence-drawer"], [data-testid="registry-connect-drawer"]');
    container?.focus();
    const key=event=>{
      if(event.key==='Escape'){close();setState(s=>({...s,connectOpen:false,source:null,responseItem:null,modelDetail:null,loadOpen:false}));}
      if(event.key==='Tab'&&container){const nodes=[...container.querySelectorAll('button,a,input,select,textarea,[tabindex="0"]')].filter(e=>!e.disabled&&e.offsetParent!==null);const first=nodes[0]||container,last=nodes.at(-1)||container;
        if(event.shiftKey&&(document.activeElement===first||document.activeElement===container)){event.preventDefault();last.focus();}
        else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}
    };
    document.addEventListener('keydown',key);return()=>{document.removeEventListener('keydown',key);if(previous?.isConnected)previous.focus?.();};
  },[state.drawer,state.connectOpen,state.responseItem,state.modelDetail,state.loadOpen,sourceOpen,close,setState]);
  const context={data,params,setParams,state,setState,show,run,reload,refresh};
  const model={...baseModel,...registryHistory(context),...registryEstate(context),...registryCompute(context),...registryComputeDetail(context),...registryConnect(context),...registrySourceProfile(context),...registryResponse(context),...registryModelDetail(context),...ownerDrawer(state.drawer,close)};
  const enhance={
    5805:(ctx,props)=>({'data-testid':'registry-census-layout',style:{...props.style,gridTemplateColumns:'minmax(0,32fr) 1px minmax(0,68fr)'}}),
    5812:ctx=>({'data-testid':`registry-census-open-${ctx.c.key}`}),
    5865:ctx=>({'data-testid':`registry-census-tab-${ctx.t.key}`}),
    5895:ctx=>({'data-testid':`registry-metric-${ctx.r.key}`}),
    5870:{'data-testid':'registry-condition-distribution'},
    6168:ctx=>({'data-testid':`registry-section-${ctx.t.key}`}),
    6408:{'data-testid':'registry-run-census'},
    9327:{role:'dialog','aria-modal':true,'aria-label':'Connect a source',tabIndex:-1,'data-testid':'registry-connect-drawer'},
    9336:{hidden:true},
    9391:{'data-testid':'registry-connect-input',disabled:state.connectPhase!=='name'},
    9392:{'data-testid':'registry-connect-send',disabled:state.connectBusy || state.connectPhase!=='name'},
    9720:{role:'dialog','aria-modal':true,'aria-label':state.drawer?.title,tabIndex:-1,'data-testid':'registry-evidence-drawer'},
    9759:{'aria-label':'Close record','data-testid':'registry-evidence-close'},
    10912:{role:'dialog','aria-modal':true,'aria-label':'Source profile',tabIndex:-1,'data-testid':'registry-source-profile'},
    10942:{'aria-label':'Close source profile','data-testid':'registry-source-profile-close'},
    11156:{'data-field':'Table'},11157:{'data-field':'Records'},11158:{'data-field':'Fields'},11159:{'data-field':'PII'},11160:{'data-field':'Quality'},11161:{'data-field':'Census'},
    11174:{'data-field':'Group'},11175:{'data-field':'Records'},11176:{'data-field':'PII'},11177:{'data-field':'Quality'},11178:{'data-field':'Rule coverage'},11179:{'data-field':'Confidence'},11180:{'data-field':'Grounding'},
    12428:{role:'dialog','aria-modal':true,'aria-label':'Census response',tabIndex:-1,'data-testid':'registry-response-dialog'},
    12449:{'data-testid':'registry-response-input',disabled:state.responseBusy,maxLength:2000},
    12450:{'data-testid':'registry-response-submit',disabled:state.responseBusy || !state.responseInput?.trim()},
    11191:{role:'dialog','aria-modal':true,'aria-label':'Model record',tabIndex:-1,'data-testid':'registry-model-detail'},
    12938:{role:'dialog','aria-modal':true,'aria-label':'Compute record',tabIndex:-1,'data-testid':'registry-compute-detail'},
  };
  const replace={
    6187:'A source is counted as fully read only where the declared population was reached. Samples, estimates and prior observations stay explicit in the report.',
    6210:'Quality findings retain their tested population and method. Unperformed checks and unclassified data are not treated as clean.',
    6285:'Quality strata have not yet been published for the whole estate.',
    6521:'{{ gpuBlurb }}',
    5940:'No operator conversation is retained for this run. This does not establish that every source was read or that no intervention was needed.',
    5973:'Every figure identifies its actual method: full enumeration, sampled inspection, estimate, declaration or unmeasured. Sources read in full requires every declared row or file header; sampled and historical coverage is never presented as a full direct read.',
    12445:'Response retained. The result and its failure history remain unchanged; a changed source must be verified by an authorised successor census.',
  };
  const common={model,enhance,replace,onUnbound:action=>show({title:'Registry action',body:`${action}: no qualified effect is bound to this control yet. No data or authority was changed.`,code:'Unbound'})};
  return {active,content:<div className="registry-owner" data-testid="registry-owner-experience">
    <NexusFragment name="registry" {...common}/><NexusFragment name="censusHistory" {...common}/>
    <NexusFragment name="sourceCatalogue" {...common}/><NexusFragment name="modelFull" {...common}/>
  </div>,drawer:<><NexusFragment name="connectDrawer" {...common}/><NexusFragment name="sourceProfile" {...common}/><NexusFragment name="modelDetail" {...common}/><NexusFragment name="computeDetail" {...common}/><NexusFragment name="censusResponse" {...common}/><NexusFragment name="drawer" {...common}/></>};
}