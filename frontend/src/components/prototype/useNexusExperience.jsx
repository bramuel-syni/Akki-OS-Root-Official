import React, { useEffect, useState } from 'react';
import { NexusFragment } from './NexusFragment';
import { nexusWorkModel } from './nexusWork';
import { supportModel } from './nexusSupport';
import { nexusMirrorModel } from './nexusMirror';
import { ownerDrawer } from './nexusShared';
import { stamp } from './evidence';
import { taskSetupStages } from './nexusTaskSetup';

export function useNexusExperience({ feature, work, session, navigate, params, setParams, baseModel, account }) {
  const principal = session.data?.principal_id;
  const [storedState,setStoredState] = useState({owner:null,value:{}});
  const state = storedState.owner === principal ? storedState.value : {};
  const setState = update => setStoredState(old=>({owner:principal,value:update(old.owner===principal?old.value:{})}));
  const [drawer,setDrawer] = useState(null);
  const [bell,setBell] = useState(false);
  const [read,setRead] = useState({});
  useEffect(()=>{ setDrawer(null);setBell(false);setRead({}); },[principal]);
  const currentDrawer = drawer?.owner === principal ? drawer : null;
  const show = value => { setBell(false);setDrawer({...value,owner:principal}); };
  const unavailable = (title, body='This operation requires its connected service and authorisation. No work was started or state changed.')=>show({title,body,code:'Not connected'});
  const active = Boolean(feature && session.data);
  useEffect(()=>{
    if(!bell)return undefined;
    const outside=event=>{const root=document.querySelector('[data-proto-line="nexus-37"]');if(root&&!root.contains(event.target))setBell(false);};
    const escape=event=>{if(event.key==='Escape'){setBell(false);document.querySelector('[data-proto-line="nexus-38"]')?.focus();}};
    document.addEventListener('pointerdown',outside);document.addEventListener('keydown',escape);
    return()=>{document.removeEventListener('pointerdown',outside);document.removeEventListener('keydown',escape);};
  },[bell]);
  const model = { ...baseModel,
    ...(feature?.family==='work'?nexusWorkModel({work,section:feature.section,state,setState,params,navigate,setParams,unavailable,show}):{}),
    ...(feature?.family==='work'?supportModel({section:feature.section,state,setState,unavailable}):{}),
    ...(feature?.family==='mirror'?nexusMirrorModel({section:feature.section,state,setState,params,navigate,unavailable}):{}),
    ...ownerDrawer(currentDrawer,()=>setDrawer(null)),
  };
  const recent = work.rows.filter(row=>row.state==='routing' && Date.now()-Date.parse(row.created_at)<=14*86400000);
  Object.assign(model, {
    rolePerson:session.data?.actor_name || principal || 'Not signed in',roleDept:session.data?.roles?.join(' · ') || '',roleInitials:baseModel.initials || 'AK',
    topBellOpen:bell,topBellToggle:()=>setBell(v=>!v),topBellTitle:work.loading?'Loading work notices…':'Work notices',
    topBellHasCount:recent.some(r=>!read[r.request_id]),topBellCount:recent.filter(r=>!read[r.request_id]).length>99?'99+':String(recent.filter(r=>!read[r.request_id]).length),
    topBellMarkAll:()=>setRead(Object.fromEntries(recent.map(r=>[r.request_id,true]))),
    topBellEmpty:work.recordsAvailable && !work.loading && !recent.length,topBellHasMore:recent.length>8,topBellMore:`Latest 8 of ${recent.length} work notices`,
    topBellItems:recent.slice(0,8).map(row=>({key:row.request_id,kind:'Work held',source:'Work record',headline:row.objective_text,
      hasReason:true,reason:row.reason,hasLine:false,time:stamp(row.created_at),link:'View record',
      onOpen:()=>{setRead(r=>({...r,[row.request_id]:true}));show({title:row.reason_code,subtitle:row.work_id,body:row.reason,next:row.next_action,code:'Work held',actions:[{
        label:'Open task',bg:'var(--blue)',color:'var(--paper)',border:'var(--blue)',onClick:()=>{setDrawer(null);navigate(`/os/work/tasks?request=${encodeURIComponent(row.request_id)}`);}}]});}})),
  });
  const steps = taskSetupStages;
  const answers = state.taskAnswers || [];
  const input = state.taskInput || '';
  const submit = value => { if (!value?.trim() || answers.length>=steps.length) return;setState(s=>({...s,taskAnswers:[...(s.taskAnswers||[]),value.trim()],taskInput:''})); };
  // twDone closes the local intake only. It never marks a task submitted or complete.
  Object.assign(model,{twInput:input,twInputChange:e=>setState(s=>({...s,taskInput:e.target.value})),twKeyDown:e=>{if(e.key==='Enter'){e.preventDefault();submit(input);}},twSubmitText:()=>submit(input),twDone:answers.length===steps.length,
    twHasOptions:Boolean(steps[answers.length]?.options),twOptions:(steps[answers.length]?.options||[]).map(label=>({label,onPick:()=>submit(label)})),
    twMessages:steps.slice(0,Math.min(answers.length+1,steps.length)).flatMap((stage,i)=>[{key:'q'+i,align:'flex-start',fromLabel:'Task setup',bg:'var(--surface2)',color:'var(--ink)',text:stage.ask},
      ...(answers[i]?[{key:'a'+i,align:'flex-end',fromLabel:'You',bg:'var(--blue)',color:'var(--paper)',text:answers[i]}]:[])]).concat(answers.length===steps.length?[{
        key:'pending',align:'flex-start',fromLabel:'Task setup',bg:'var(--surface2)',color:'var(--ink)',text:'Setup captured in this session only. The task service is not connected, so this draft has not been submitted or scheduled.'}]:[]),
  });
  const enhance = {
    38:{'data-testid':'owner-work-notices-trigger','aria-label':`${recent.filter(r=>!read[r.request_id]).length} unread work notices`,'aria-expanded':bell,'aria-controls':'owner-work-notices'},
    43:{id:'owner-work-notices','data-testid':'owner-work-notices','aria-label':'Work notices'},
    47:{'data-testid':'owner-work-notices-mark-read'},63:ctx=>({'data-testid':`owner-work-notice-open-${ctx.nt.key}`}),
    2458:(ctx,props)=>({'data-testid':'my-work-navigation','aria-label':'My Work sections',role:'navigation',style:{...props.style,flexWrap:'wrap'}}),
    2460:ctx=>({'data-testid':`my-work-${ctx.t.key}-link`,'aria-current':ctx.t.active?'page':undefined}),
    2502:ctx=>({'data-testid':`my-work-record-${ctx.t.requestId}`}),3031:ctx=>({'data-testid':`my-work-full-record-${ctx.t.requestId}`}),
    2454:{'aria-disabled':true},2450:{'data-testid':'my-work-scope'},78:account,
    2462:{'data-testid':'my-work-new-task'},2935:{'data-testid':'task-setup-input'},2936:{'data-testid':'task-setup-submit',disabled:answers.length>=steps.length},2940:{'data-testid':'task-setup-back-to-work'},
    8444:ctx=>({'data-testid':`grey-mirror-${ctx.t.key}-link`,'aria-current':ctx.t.active?'page':undefined}),
    ...(feature?.family==='mirror'&&feature.section!=='overview'&&feature.section!=='state'?{
      8451:(ctx,props)=>({style:{...props.style,gridTemplateColumns:'minmax(0,1fr)'}}),
    }:{}),
    ...(feature?.family==='work'&&['board','goals'].includes(feature.section)?{
      2465:(ctx,props)=>({style:{...props.style,gridTemplateColumns:'minmax(0,1fr)',margin:0,width:'100%'}}),
    }:{}),
    3396:{hidden:true},
    9720:{role:'dialog','aria-modal':true,'aria-label':currentDrawer?.title,tabIndex:-1,'data-testid':'owner-evidence-drawer'},9759:{'aria-label':'Close record','data-testid':'owner-evidence-close'},
  };
  const replace = {2511:'{{ t.evidence }}',3034:'{{ t.evidence }}',3104:'Not assessed',2451:'Viewing My Work as —',
    2940:'Back to the work',68:work.recordsAvailable?'No work notices in the last 14 days.':'Work notices are not available yet.',
    2916:'Describe the task, owner, date and evidence. It is not submitted or scheduled until the connected service accepts it.',
    2526:'Actions in the recorded work history. Unverified autonomous follow-ups are not inferred.',
  };
  model.perfLevelsView=[{label:'Your authorised scope',color:'var(--ink)',bg:'#fff',onClick:work.reload}];
  useEffect(()=>{
    if(!currentDrawer)return undefined;
    const previous=document.activeElement;
    const panel=document.querySelector('[data-testid="owner-evidence-drawer"]');
    panel?.focus();
    const key=e=>{if(e.key==='Escape'){e.preventDefault();setDrawer(null);}if(e.key==='Tab'&&panel){
      const elements=[...panel.querySelectorAll('button,a,input,select,textarea,[tabindex="0"]')].filter(el=>!el.disabled&&el.offsetParent!==null);
      const first=elements[0]||panel,last=elements.at(-1)||panel;
      if(e.shiftKey&&(document.activeElement===first||document.activeElement===panel)){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }};
    document.addEventListener('keydown',key);return()=>{document.removeEventListener('keydown',key);
      if(previous?.isConnected&&previous!==document.body)previous.focus?.();else document.querySelector('[data-testid="owner-work-notices-trigger"]')?.focus();};
  },[currentDrawer]);
  const common={model,enhance,replace,onUnbound:action=>unavailable(String(action||'Action').replace(/([a-z])([A-Z])/g,'$1 $2'))};
  const supportSlots=feature?.family==='work'&&['board','goals'].includes(feature.section)?{2465:<NexusFragment name={feature.section==='board'?'board':'company'} {...common}/>} : {};
  const content=feature?.family==='work'?<NexusFragment name="work" {...common} slots={supportSlots}/>:<>
    <NexusFragment name="pageHeader" {...common}/>
    <NexusFragment name="mirror" {...common}/>
    {feature?.section!=='overview'&&feature?.section!=='state'&&<NexusFragment name="mirror" {...common} model={{...model,isGreyMirror:true}} slots={{8451:<NexusFragment name="watch" {...common}/>}}/>}
  </>;
  return {active,model,common,content,header:<NexusFragment name="headerActions" {...common}/>,drawer:<NexusFragment name="drawer" {...common}/>,unavailable};
}