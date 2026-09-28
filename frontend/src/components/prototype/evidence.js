export const count = value => value == null ? 'Not measured' : new Intl.NumberFormat('en').format(value);
export const initials = value => (value || '').split('@')[0].split(/[.\s·_-]+/).filter(Boolean).map(word => word[0]).slice(0, 2).join('').toUpperCase() || '—';
export const stamp = value => {
  if (!value) return 'Not recorded';
  const normal = value.replace(/^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z$/, '$1-$2-$3T$4:$5:$6Z');
  const ms = Date.parse(normal);
  return Number.isNaN(ms) ? 'Timestamp not verified' : new Date(ms).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC' }) + ' UTC';
};
export const unknownFill = 'repeating-linear-gradient(135deg,#e5dfd1,#e5dfd1 4px,#f5f2ea 4px,#f5f2ea 8px)';
export const unmeasuredBar = label => [{ key: label, label, size: 'Not measured', v: 'Not established', w: '100%', fill: unknownFill, color: unknownFill, pct: 'Not measured', cursor: 'default' }];
export const tile = (label, value = 'Not measured', note = 'No measurement in this census') => ({ label, value, note });
export const measuredWays = [
  { label: 'Source metadata', short: 'Database and table inventory recorded by the retained metadata census. TABLE_ROWS values are estimates, not counted source rows.' },
  { label: 'Content and quality', short: 'Content completeness, null rates, damage, duplicates and language distribution are not established by a metadata-only census.' },
  { label: 'Execution evidence', short: 'A new run is complete only after Akki-owned output, governing receipts and durable result evidence are verified.' },
  { label: 'Permission to use', short: 'Census access is not a data-release grant. Terms, purpose and the applicable approval govern use separately.' },
];
export const tabs = [
  ['work', 'Work'], ['build', 'Build'], ['apps', '3rd Party Apps'], ['admin', 'Admin'],
];
export const groups = {
  work: [{ key: 'workstudio', label: 'WorkStudio', items: [['Chat', '/os/work/chat'], ['Data Suite', '/os/work/analyze'], ['Documents', '/os/work/documents'], ['My Work', '/os/work/tasks']] },
    { key: 'thinklab', label: 'ThinkLab', items: [['Seek Clarity', '/os/work/clarity'], ['Develop Strategy', '/os/work/strategy'], ['Test Hypothesis', '/os/work/hypothesis'], ['Get Perspective', '/os/work/perspective']] },
    { key: 'collab', label: 'Collab', items: [['Mentions', '/os/work/mentions'], ['Emails', '/os/work/emails'], ['Projects/Tasks', '/os/work/projects'], ['HR Stuff', '/os/work/hrstuff']] }],
  admin: [{ key: 'estate', label: 'Manage Estate', items: [['Registry', '/os/admin/estate'], ['Shield', '/os/admin/govern'], ['Grey Mirror', '/os/admin/greymirror'], ['Approvals', '/os/admin/spendreq']] }],
  build: [{ key: 'build', label: 'Build Your Resources', items: [['Train Models', '/os/build/train'], ['Build Agents', '/os/build/agentbuild'], ['Build Skill', '/os/build/buildskill'], ['Extract Data', '/os/build/extract']] }, { key: 'buildlib', label: 'Your Resources', items: [['Agents', '/os/build/youragents'], ['Models', '/os/build/yourmodels']] }],
  apps: [{ key: 'apps', label: '3rd Party Apps', items: [['New', '/os/apps/new'], ['Frequent', '/os/apps/frequent'], ['Connected', '/os/apps/connected'], ['Requests', '/os/apps/requests']] }],
};