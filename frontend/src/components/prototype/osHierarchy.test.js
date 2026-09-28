import { groups } from './evidence';
import { featureRoute, workSections, watchSections, legacyFeaturePaths } from './osHierarchy';

test('delivery support and Watch components are not launcher applications', () => {
  const labels = Object.values(groups).flatMap(list => list.flatMap(group => group.items.map(([label]) => label)));
  ['My Team', 'Company Goals', 'Board', 'State', 'Record', 'Under Watch', 'Decisions'].forEach(label => expect(labels).not.toContain(label));
  ['My Work', 'Grey Mirror', 'Chat', 'Data Suite', 'Documents', 'Shield', 'Approvals'].forEach(label => expect(labels).toContain(label));
  expect(groups.work[0].items).toHaveLength(4);
  expect(groups.admin).toHaveLength(1);
});

test('My Work support sections have exactly one parent and distinct paths', () => {
  expect(workSections.map(s => s.label)).toEqual(['Work records', 'My Team', 'Company Goals', 'Board']);
  workSections.forEach(section => expect(featureRoute(section.path)).toEqual({ family: 'work', section: section.key, label: section.label }));
});

test('Watch subviews are under Grey Mirror, not sibling applications', () => {
  watchSections.forEach(section => {
    expect(section.path.startsWith('/os/admin/greymirror/watch/')).toBe(true);
    expect(featureRoute(section.path).family).toBe('mirror');
  });
  expect(featureRoute('/os/admin/greymirror').section).toBe('overview');
  expect(featureRoute('/os/admin/greymirror/watch').section).toBe('state');
  expect(featureRoute('/os/work/tasks/unknown')).toBeNull();
});

test('all seven former deep links recover an exact nested destination', () => {
  expect(Object.keys(legacyFeaturePaths)).toHaveLength(7);
  Object.values(legacyFeaturePaths).forEach(path => expect(featureRoute(path)).not.toBeNull());
  expect(new Set(Object.values(legacyFeaturePaths)).size).toBe(7);
});