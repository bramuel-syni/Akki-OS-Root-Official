import { censusRequest } from '../census/useCensusWorkspace';
import { stamp } from './evidence';

export function registryResponse({data,state,setState,reload}) {
  const pending=(data?.conversations || []).filter(item=>item.state==='PENDING');
  const item=state.responseItem;
  const update=value=>setState(s=>({...s,...value}));
  const send=async()=>{
    if(!item || !state.responseInput?.trim() || state.responseBusy)return;
    update({responseBusy:true,responseError:null});
    try {const result=await censusRequest(`/conversations/${item.item_id}/resolve`,{method:'POST',body:JSON.stringify({resolution_text:state.responseInput.trim(),state:'RESOLVED_ACCEPTED'})});
      update({responseItem:result.item,responseBusy:false,responseInput:'',responseNext:result.resume_status});reload();
    } catch(error){update({responseBusy:false,responseError:error.message});}
  };
  const message=(text,from=false)=>({text,bg:from?'var(--blue)':'var(--surface)',color:from?'var(--paper)':'var(--ink)',ml:from?'auto':'0',radius:from?'11px 11px 3px 11px':'11px 11px 11px 3px'});
  return {
    censusPauseNeedsInput:pending.length>0,censusPauseOpen:Boolean(item),
    openCensusPause:()=>pending.length&&update({responseItem:pending[0],responseInput:'',responseError:null,responseNext:null}),
    closeCensusPause:()=>!state.responseBusy&&update({responseItem:null}),
    censusPauseMessages:item?[message(`${item.host_label}: ${item.message} (${item.reason_code}). Raised ${stamp(item.banked_at_utc)}. Record the action or disposition; do not paste credentials.`),
      ...(item.resolution_text?[message(item.resolution_text,true),message(state.responseNext || 'The response is retained. Historical work is not silently rewritten or marked successful.')]:[]),
      ...(state.responseError?[message(state.responseError)]:[])]:[],
    censusPauseResolved:Boolean(item&&item.state!=='PENDING'),censusPauseInput:state.responseInput || '',
    censusPauseInputChange:e=>update({responseInput:e.target.value}),censusPauseInputKeyDown:e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}},censusPauseSend:send,
  };
}