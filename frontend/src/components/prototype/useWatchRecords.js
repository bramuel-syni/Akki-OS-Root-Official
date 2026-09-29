import { useCallback, useEffect, useState } from 'react';

const auth = () => ({Authorization:`Bearer ${sessionStorage.getItem('akki_access_token')}`});

export function useWatchRecords(principal, active) {
  const [result, setResult] = useState({owner:null,data:null,error:null});
  const [revision,setRevision] = useState(0);
  const refresh = useCallback(()=>setRevision(value=>value+1),[]);
  useEffect(()=>{
    if(!principal || !active) return undefined;
    const controller = new AbortController();
    setResult(old=>({owner:principal,data:old.owner===principal?old.data:null,error:null}));
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portal/watch/state`, {headers:auth(), signal:controller.signal})
      .then(async response=>{
        const body = await response.json();
        if(!response.ok) throw new Error(body.detail || 'Watch records unavailable');
        if(!controller.signal.aborted) setResult({owner:principal,data:body,error:null});
      }).catch(error=>{if(!controller.signal.aborted) setResult({owner:principal,data:null,error:error.message});});
    return ()=>controller.abort();
  },[principal,active,revision]);
  // Every console action lands on the same records and re-reads them; the caller renders the outcome.
  const act = useCallback(async (path, body) => {
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}${path}`, {method:'POST',headers:{...auth(),'Content-Type':'application/json'},body:JSON.stringify(body||{})});
    const payload = await response.json().catch(()=>({}));
    refresh();
    if(!response.ok) throw new Error(payload.detail || `Request failed (${response.status})`);
    return payload;
  },[refresh]);
  return {...(result.owner===principal?result:{data:null,error:null}),refresh,act};
}

export function useWatchNotices(principal) {
  const [notices,setNotices] = useState({owner:null,rows:[]});
  useEffect(()=>{
    if(!principal) return undefined;
    const controller = new AbortController();
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portal/watch/notices`, {headers:auth(), signal:controller.signal})
      .then(r=>r.ok?r.json():{notices:[]}).then(body=>{if(!controller.signal.aborted) setNotices({owner:principal,rows:body.notices||[]});})
      .catch(()=>{if(!controller.signal.aborted) setNotices({owner:principal,rows:[]});});
    return ()=>controller.abort();
  },[principal]);
  return notices.owner===principal?notices.rows:[];
}
