import { useCallback, useEffect, useState } from 'react';

export function useWatchRecords(principal, active) {
  const [result, setResult] = useState({owner:null,data:null,error:null});
  const [revision,setRevision] = useState(0);
  const refresh = useCallback(()=>setRevision(value=>value+1),[]);
  useEffect(()=>{
    if(!principal || !active) return undefined;
    const controller = new AbortController();
    setResult({owner:principal,data:null,error:null});
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portal/watch/state`, {
      headers:{Authorization:`Bearer ${sessionStorage.getItem('akki_access_token')}`}, signal:controller.signal,
    }).then(async response=>{
      const body = await response.json();
      if(!response.ok) throw new Error(body.detail || 'Watch records unavailable');
      if(!controller.signal.aborted) setResult({owner:principal,data:body,error:null});
    }).catch(error=>{if(!controller.signal.aborted) setResult({owner:principal,data:null,error:error.message});});
    return ()=>controller.abort();
  },[principal,active,revision]);
  return {...(result.owner===principal?result:{data:null,error:null}),refresh};
}