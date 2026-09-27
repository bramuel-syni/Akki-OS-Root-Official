import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server.node';
import { workDetailCopy } from './workCopy';
import { osWorkModel } from './osWorkModel';

const selected = { request_id: 'request-1', work_id: 'request-1', reason_code: 'APPROVAL_GROUP_PENDING',
  reason: 'A required approval group is not satisfied.', next_action: 'Complete the native approval ceremony.',
  objective_hash: 'a'.repeat(64), governing_engine: 'mtafiti', execution_verified: false,
  history: [{ at: '2026-01-01T00:00:00Z', event: 'execution_held', state: 'routing', reason_code: 'APPROVAL_GROUP_PENDING', receipt_hash: 'b'.repeat(64) }] };

test('existing DAP paragraph carries safe reason, action and receipted history without new layout', () => {
  const html = renderToStaticMarkup(workDetailCopy({ selected }));
  expect(html).toContain('APPROVAL_GROUP_PENDING');
  expect(html).toContain('Complete the native approval ceremony.');
  expect(html).toContain('dap-work-detail-reason');
  expect(html.match(/<p /g)).toHaveLength(4);
});

test('OS uses the same reason and does not claim an unverified request is admitted', () => {
  const model = osWorkModel({ work: { selected, rows: [], reload: () => {} }, disclosure: {} });
  expect(model.tmRailHead).toContain(selected.reason_code);
  expect(model.tmRailLines[1].note).toBe(selected.next_action);
  expect(model.tmRail[0].text).toContain(selected.history[0].reason_code);
});

test('reason strings are escaped rather than treated as markup', () => {
  const html = renderToStaticMarkup(workDetailCopy({ selected: { ...selected, reason: '<img src=x onerror=alert(1)>' } }));
  expect(html).toContain('&lt;img');
  expect(html).not.toContain('<img');
});