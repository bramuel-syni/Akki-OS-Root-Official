import { osWorkModel } from './osWorkModel';

const model = overrides => osWorkModel({ work: { rows: [], selected: null, loading: false, recordsAvailable: false,
  reload: jest.fn(), ...overrides }, navigate: jest.fn(), setParams: jest.fn(), disclosure: {}, toggle: jest.fn() });

test('unknown/loading data never claims zero counts or an empty work list', () => {
  const value = model({ loading: true });
  expect(value.taskStats.every(s => s.value === '—')).toBe(true);
  expect(value.tmFilteredEmpty).toBe(false);
  expect(value.tmRailHead).toContain('Loading');
});

test('only a successfully read empty dataset displays zero counts and the empty state', () => {
  const value = model({ recordsAvailable: true });
  expect(value.taskStats.every(s => s.value === 0)).toBe(true);
  expect(value.tmFilteredEmpty).toBe(true);
});

test('failed reads do not become empty datasets and selected rows stay actionable', () => {
  expect(model({ error: 'Records unavailable' }).tmFilteredEmpty).toBe(false);
  const navigate = jest.fn(), setParams = jest.fn();
  const value = osWorkModel({ work: { recordsAvailable: true, rows: [{ request_id: 'req-one', work_id: 'req-one', state: 'routing', objective_text: 'TEST record' }] },
    navigate, setParams, disclosure: {}, toggle: jest.fn(), search: '?request=req-one', section: 'records' });
  value.tmFilteredView[0].onOpen(); expect(setParams).toHaveBeenCalledWith({ request: 'req-one' });
  value.prodTabsView[1].onClick(); expect(navigate).toHaveBeenCalledWith('/os/work/tasks/team?request=req-one');
});