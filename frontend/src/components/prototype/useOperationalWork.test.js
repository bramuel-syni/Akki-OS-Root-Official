import React, { act } from 'react';
import { createRoot } from 'react-dom/client';
import { tryGet } from '@/lib/apiClient';
import { useOperationalWork } from './useOperationalWork';

jest.mock('@/lib/apiClient', () => ({ tryGet: jest.fn(), submitPortalRequest: jest.fn() }), { virtual: true });
global.IS_REACT_ACT_ENVIRONMENT = true;
let root, container, current;
function Probe(props) { current = useOperationalWork(props.principal, 'os', props.selected); return null; }
const ok = data => ({ ok: true, status: 200, data });
const row = { request_id: 'work-a', objective_text: 'SYNTHETIC work fixture' };
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return { promise, resolve }; };
beforeEach(() => {
  container = document.createElement('div'); document.body.appendChild(container); root = createRoot(container);
  tryGet.mockReset().mockImplementation(path => Promise.resolve(ok(path === '/api/os/work' ? { rows: [row] } : path.endsWith('allowance') ? { status: 'unresolved' } : { work_id: path.split('/').pop() })));
});
afterEach(async () => { await act(async () => root.unmount()); container.remove(); });
const show = (selected = null, principal = 'TEST-principal') => act(async () => { root.render(<Probe principal={principal} selected={selected} />); });

test('selecting records makes only the detail request, retaining the list', async () => {
  await show(); expect(tryGet).toHaveBeenCalledTimes(2);
  await show('work-a'); expect(tryGet).toHaveBeenCalledTimes(3); expect(current.rows).toEqual([row]);
  await show('work-b'); expect(tryGet).toHaveBeenCalledTimes(4); expect(current.selected.work_id).toBe('work-b');
  expect(tryGet.mock.calls.filter(([path]) => path === '/api/os/work')).toHaveLength(1);
  expect(tryGet.mock.calls.filter(([path]) => path.endsWith('allowance'))).toHaveLength(1);
});

test('a late detail cannot overwrite the next selected record', async () => {
  const pending = deferred();
  const normal = tryGet.getMockImplementation();
  tryGet.mockImplementation(path => path.endsWith('/work-a') ? pending.promise : normal(path));
  await show('work-a'); expect(current.detailLoading).toBe(true);
  await show('work-b'); expect(current.selected.work_id).toBe('work-b');
  await act(async () => pending.resolve(ok({ work_id: 'work-a' })));
  expect(current.selected.work_id).toBe('work-b');
});

test('logout removes list, entitlement and detail while old requests finish', async () => {
  await show('work-a'); expect(current.selected).not.toBeNull();
  const pending = deferred(); tryGet.mockImplementation(() => pending.promise);
  await show('work-b');
  await show(null, null);
  expect(current.rows).toEqual([]); expect(current.selected).toBeNull(); expect(current.entitlement).toBeNull();
  await act(async () => pending.resolve(ok({ work_id: 'work-b' })));
  expect(current.selected).toBeNull(); expect(current.detailLoading).toBe(false);
});

test('refresh re-reads the list, terms and selected detail without caching authority', async () => {
  await show('work-a'); tryGet.mockClear();
  await act(async () => current.reload());
  expect(tryGet).toHaveBeenCalledTimes(3);
});

test('failed refresh removes stale list/terms and surfaces the failure', async () => {
  await show();
  tryGet.mockResolvedValue({ ok: false, status: 503, data: { detail: 'Records unavailable' } });
  await act(async () => current.reload());
  expect(current.rows).toEqual([]); expect(current.entitlement).toBeNull(); expect(current.error).toBe('Records unavailable');
});

test('switching principal never keeps the previous principal rows visible', async () => {
  await show('work-a');
  const pending = deferred(); tryGet.mockImplementation(() => pending.promise);
  await show('work-b', 'OTHER-principal');
  expect(current.rows).toEqual([]); expect(current.selected).toBeNull(); expect(current.entitlement).toBeNull();
  await act(async () => pending.resolve(ok({ rows: [] })));
});