import { censusRequest } from '../census/useCensusWorkspace';

export function registryConnect({data,state,setState,run,reload}) {
  const phase=state.connectPhase || 'source';
  const update=values=>setState(s=>({...s,...values}));
  const choose=source=>update({connectSource:source,connectPhase:'name',connectInput:source.label,connectError:''});
  const send=async()=>{
    if(phase==='name') {
      if(!state.connectInput?.trim())return;
      update({connectName:state.connectInput.trim(),connectInput:'',connectPhase:'confirm'}); return;
    }
    if(phase==='confirm'&&!state.connectBusy) {
      update({connectBusy:true,connectError:''});
      try { const result=await censusRequest('/connections',{method:'POST',body:JSON.stringify({source_id:state.connectSource.source_id,name:state.connectName})});
        update({connectPhase:'done',connectResult:result,connectBusy:false}); reload();
      }catch(error){update({connectError:error.message,connectBusy:false});}
    }
  };
  const bubble=(text,user=false)=>({text,bg:user?'var(--blue)':'var(--surface)',color:user?'var(--paper)':'var(--ink)',ml:user?'auto':'0',radius:user?'11px 11px 3px 11px':'11px 11px 11px 3px'});
  return {
    openConnect:()=>update({connectOpen:true,connectPhase:'source',connectInput:'',connectError:'',connectSource:null,connectResult:null}),
    closeConnect:()=>!state.connectBusy&&update({connectOpen:false}),connectOpen:Boolean(state.connectOpen),connectDone:phase==='done',
    connectMessages:[bubble('Which source in your admitted estate custody are you connecting? Credentials already in custody will not be requested again.'),
      ...(state.connectSource?[bubble(state.connectSource.label,true),bubble('Give this source a name. The existing read-only custody is retained; a declaration does not grant new access.')]:[]),
      ...(state.connectName&&phase!=='name'?[bubble(state.connectName,true),bubble('Confirm the source declaration under your tenant. Then run the census to verify access and publish actual findings.')]:[]),
      ...(phase==='done'?[bubble(state.connectResult?.created?'Source declaration saved. Connection and measurement still require the census.':'This source declaration already exists. No duplicate source was created.')]:[]),
      ...(state.connectError?[bubble(state.connectError)]:[])],
    connectHasChips:phase!=='name',connectChips:phase==='source'?(data?.sources || []).map(source=>({label:source.label,onClick:()=>choose(source)})):phase==='confirm'?[{label:state.connectBusy?'Saving…':'Confirm declaration',onClick:send},{label:'Back',onClick:()=>!state.connectBusy&&update({connectPhase:'name',connectInput:state.connectName})}]:phase==='done'?[{label:'Run census',onClick:()=>{update({connectOpen:false});run();}}]:[],
    connectInput:state.connectInput || '',connectInputChange:e=>update({connectInput:e.target.value}),connectInputKeyDown:e=>{if(e.key==='Enter'){e.preventDefault();send();}},connectSend:send,connectPlaceholder:phase==='name'?'Source name':'Choose an option above',
    connectStatusLine:state.connectBusy?'Saving the declared source…':phase==='done'?'Declared · access not inferred':'Read-only source · existing custody · tenant-bound',
    connectHasSummary:phase==='done',connectSummaryTitle:'Connection record',connectSummary:phase==='done'?[{label:'Source',value:state.connectName},{label:'State',value:'Declared, not yet verified'},{label:'Identity',value:state.connectResult?.connection?.descriptor?.descriptor_id},{label:'Tenant',value:data?.tenant_id}]:[],
    connectHasDiagnostics:Boolean(state.connectError),connectDiagnostics:state.connectError?[{step:'Record declaration',text:state.connectError,color:'var(--brass)'}]:[],connectPreviewLinks:[],
  };
}