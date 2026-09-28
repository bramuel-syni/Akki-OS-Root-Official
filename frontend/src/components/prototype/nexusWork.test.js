import { nexusWorkModel } from './nexusWork';
import { supportModel } from './nexusSupport';
import { nexusMirrorModel } from './nexusMirror';
import { ownerDrawer } from './nexusShared';
import { taskSetupStages } from './nexusTaskSetup';

const rows = Array.from({length:1200},(_,i)=>({ request_id:`TEST-${i}`,work_id:`TEST-${i}`,objective_text:`TEST-only objective ${i}`,
  created_at:'2026-09-28T00:00:00+00:00',state:i%2?'routing':'ready',execution_verified:i%2===0,reason_code:'TEST_HOLD',reason:'SYNTHETIC fixture',next_action:'Review evidence' }));
function setup(overrides={}) {
  const args={work:{rows,selected:null,loading:false,detailLoading:false,recordsAvailable:true,reload:jest.fn()},section:'records',
    state:{},setState:jest.fn(),params:new URLSearchParams(),navigate:jest.fn(),setParams:jest.fn(),unavailable:jest.fn(),show:jest.fn(),...overrides};
  return [nexusWorkModel(args),args];
}
test('owner preview shows three without truncating View all or its search',()=>{
  const [preview]=setup(); expect(preview.tmFilteredView).toHaveLength(3);expect(preview.tmHasMore).toBe(true);expect(preview.tmFullGroups).toEqual([]);
  const [full]=setup({params:new URLSearchParams('view=all')});expect(full.tmFullGroups.reduce((n,g)=>n+g.rows.length,0)).toBe(1200);
  const [filtered]=setup({params:new URLSearchParams('view=all'),state:{search:'objective 1199'}});expect(filtered.tmFullGroups[0].rows[0].requestId).toBe('TEST-1199');
});
test('original five My Work lenses plus approved nested support retain one navigation family',()=>{
  const [model,args]=setup({params:new URLSearchParams('request=TEST-2')});
  expect(model.prodTabsView.map(t=>t.label)).toEqual(['Today','My team','The work','Execution score','Sources & governance','Company Goals','Board']);
  model.prodTabsView.find(t=>t.key==='goals').onClick();expect(args.navigate).toHaveBeenCalledWith('/os/work/tasks/goals?request=TEST-2');
});
test('selected record uses original full task workspace, never overwrites the frozen objective',()=>{
  const [model,args]=setup({params:new URLSearchParams('request=TEST-2')});
  expect(model.tmWorkspaceOpen).toBe(true);expect(model.tmListMode).toBe(false);expect(model.wsName).toBe(rows[2].objective_text);
  model.wsToggleObjEdit();expect(args.unavailable).toHaveBeenCalledWith('Frozen objective',expect.any(String));
  model.wsRunCycle();expect(args.show).toHaveBeenCalledWith(expect.objectContaining({title:'TEST_HOLD',next:'Review evidence'}));
});
test('native organisational scores stay unknown instead of adopting reference demo data',()=>{
  const [model]=setup();expect(model.prodTodayStats.every(s=>s.value==='—')).toBe(true);expect(model.prodTeamRows).toEqual([]);expect(model.prodScoreTotal).toBe('—');
});
test('Board retains its original four views, filters and question control without simulated answers',()=>{
  const setState=jest.fn(), unavailable=jest.fn();const model=supportModel({section:'board',state:{},setState,unavailable});
  expect(model.boardTabsView.map(t=>t.label)).toEqual(['Signals','Performance','Documents','Questions']);
  model.boardTabsView[2].onClick();expect(setState.mock.calls[0][0]({}).boardTab).toBe('docs');
  model.sendBoardChat();expect(unavailable).toHaveBeenCalled();expect(model.boardChatLogView).toEqual([]);
});
test('Grey Mirror keeps original parent views and nests Watch lanes; no sample monitoring is imported',()=>{
  const args={section:'overview',state:{},setState:jest.fn(),navigate:jest.fn(),params:new URLSearchParams(),unavailable:jest.fn()};
  const model=nexusMirrorModel(args);expect(model.gmTabsView.map(t=>t.label)).toEqual(['Overview','Monitor & detect','Respond','Users & models','The Watch']);
  model.gmTabsView.at(-1).onClick();expect(args.navigate).toHaveBeenCalledWith('/os/admin/greymirror/watch/state');
  const record=nexusMirrorModel({...args,section:'record'});expect(record.isWatchRecord).toBe(true);expect(record.recordRowsView).toEqual([]);
  expect(model.gmStats.every(s=>s.value==='—')).toBe(true);
  record.exitApp();expect(args.navigate).toHaveBeenLastCalledWith('/os/admin/greymirror');
});
test('original evidence drawer carries exact hold/next action, not an invented resolved verdict',()=>{
  const model=ownerDrawer({title:'Binding required',body:'No worker admitted',next:'Supply original admission',code:'Held'},jest.fn());
  expect(model.dwOpen).toBe(true);expect(model.dwCards.map(c=>c.a)).toEqual(['No worker admitted','Supply original admission']);
  expect(model.dwResolved).toBeUndefined();expect(model.dwHasActions).toBe(false);
});

test('the original task setup retains all four source stages and eleven choice options',()=>{
  expect(taskSetupStages.map(s=>s.key)).toEqual(['objective','team','deadline','evidence']);
  expect(taskSetupStages.slice(1).flatMap(s=>s.options)).toHaveLength(11);
  expect(taskSetupStages[1].options).toContain('Me + named team');expect(taskSetupStages[2].options).toContain('Custom date');
  expect(taskSetupStages[3].options).toContain('A metric threshold');
});