// Owner correction: product launchers are not an inventory of their components.
export const workSections = [
  { key: 'records', label: 'Work records', path: '/os/work/tasks' },
  { key: 'team', label: 'My Team', path: '/os/work/tasks/team' },
  { key: 'goals', label: 'Company Goals', path: '/os/work/tasks/goals' },
  { key: 'board', label: 'Board', path: '/os/work/tasks/board' },
];
export const watchSections = [
  { key: 'state', label: 'State', path: '/os/admin/greymirror/watch/state' },
  { key: 'record', label: 'Record', path: '/os/admin/greymirror/watch/record' },
  { key: 'under-watch', label: 'Under Watch', path: '/os/admin/greymirror/watch/under-watch' },
  { key: 'decisions', label: 'Decisions', path: '/os/admin/greymirror/watch/decisions' },
];
export const legacyFeaturePaths = {
  '/os/work/team': workSections[1].path,
  '/os/work/performance': workSections[2].path,
  '/os/work/board': workSections[3].path,
  '/os/admin/wstate': watchSections[0].path,
  '/os/admin/wrecord': watchSections[1].path,
  '/os/admin/wunder': watchSections[2].path,
  '/os/admin/wdecisions': watchSections[3].path,
  '/os/work/training': '/os/build/train',
};
export function featureRoute(pathname) {
  const work = workSections.find(section => section.path === pathname);
  if (work) return { family: 'work', section: work.key, label: work.label };
  if (pathname === '/os/build/train') return { family: 'build', section: 'train', label: 'Train Models' };
  if (pathname === '/os/admin/greymirror') return { family: 'mirror', section: 'overview', label: 'Grey Mirror' };
  if (pathname === '/os/admin/greymirror/watch') return { family: 'mirror', section: 'state', label: 'State' };
  const watch = watchSections.find(section => section.path === pathname);
  return watch ? { family: 'mirror', section: watch.key, label: watch.label } : null;
}