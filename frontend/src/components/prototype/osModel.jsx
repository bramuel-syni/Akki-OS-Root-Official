import React from 'react';
import { Database, MessageSquare, FileText, ShieldCheck, LayoutGrid, Users, FlaskConical, Box, Workflow, BrainCircuit } from 'lucide-react';
import { count, stamp, initials, tile, unmeasuredBar, measuredWays, tabs, groups } from './evidence';
import { historyModel } from './historyModel';

const icons = { Registry: Database, Chat: MessageSquare, Documents: FileText, Shield: ShieldCheck, Board: LayoutGrid, 'My Work': Workflow, 'My Team': Users, 'Seek Clarity': FlaskConical, 'Train Models': BrainCircuit };

export function osModel({ data, user, portal, navTab, setNavTab, selected, setSelected, params, setParams, navigate, disclosure, toggle, openRun, notice, trainCounts }) {
  const latest = data?.latest;
  const history = params.get('view') === 'history';
  const estate = params.get('view') === 'sources';
  const mixed = params.get('view') === 'mix';
  const Icon = icons[selected.label] || Box;
  const status = data?.runs?.[0];
  const running = Boolean(data?.runs?.some(r => r.status === 'PENDING'));
  const train = selected.label === 'Train Models';
  const tc = key => (trainCounts || {})[key] ?? 0;
  const tabProps = ([key, label]) => ({ key, label, color: key === navTab ? 'var(--ink)' : 'var(--ink3)', weight: key === navTab ? '600' : '500', bg: key === navTab ? '#fff' : 'transparent', onClick: () => setNavTab(key) });
  const scope = {
    portalMode: portal, appMode: !portal, anyFullPage: history || estate || mixed,
    rolePerson: user?.name || 'Not signed in', roleDept: data?.tenant_id || 'Admitted access required',
    roleInitials: initials(user?.name),
    navTabsView: tabs.filter(([key]) => key !== 'admin').map(tabProps), navTabsRightView: tabs.filter(([key]) => key === 'admin').map(tabProps),
    navTabEmpty: false,
    navGroupsView: (groups[navTab] || []).map(group => ({ ...group, tabs: false, divider: false, items: group.items.map(([label, path]) => {
      const TileIcon = icons[label] || (group.key === 'thinklab' ? FlaskConical : Box);
      const active = selected.label === label;
      return { key: label, label, icon: <TileIcon size={17} strokeWidth={1.6} />, bg: active ? '#fff' : 'rgba(255,255,255,.56)', color: 'var(--ink)', borderColor: active ? 'var(--hair)' : 'var(--line)', shadow: active ? '0 2px 6px rgba(20,20,10,.04)' : 'none', iconColor: group.key === 'estate' ? 'var(--blue)' : 'var(--accent)', iconBg: group.key === 'estate' ? 'rgba(22,39,74,.08)' : 'var(--accent-soft)', onClick: () => setSelected({ label, path, group: group.label }) };
    }) })),
    landingGroupLabel: selected.group, landingAppName: selected.label, landingIcon: <Icon size={17} strokeWidth={1.6} />,
    landingIconBg: 'rgba(22,39,74,.08)', landingIconColor: 'var(--blue)',
    landingGreeting: selected.label === 'Registry' ? `The ${data?.tenant_id || 'admitted'} estate: census records, what is known, and what remains unmeasured.` : train ? 'Every model on record, with the conversation that produced it. Shape a run in plain language; nothing trains until you approve it.' : `Open ${selected.label} in your admitted workspace. Census evidence and access remain bound to your identity.`,
    landingHasStats: true, landingStats: selected.label === 'Registry' ? [{ v: count(latest?.database_count), l: 'databases recorded' }, { v: count(latest?.table_count), l: 'tables recorded' }, { v: String(data?.records?.length ?? 0), l: 'tenant-attributed census records' }]
      : train ? [{ v: String(tc('Shaping') + tc('In Approval') + tc('Queued') + tc('In training') + tc('Testing')), l: 'Running' }, { v: String(tc('Refused')), l: 'Need attention' }, { v: String(tc('In service') + tc('Retired')), l: 'Complete' }] : [{ v: 'Not measured', l: 'activity for this workspace' }],
    landingHasHistory: false, landingHasTips: true,
    landingTips: selected.label === 'Registry' ? ['Census metadata estimates are distinguished from counted rows.', 'The registry shows retained evidence—not inferred permissions or fresh source availability.']
      : train ? ['Each run carries its own record: recipe, data, checks and the reason it stopped or was admitted.', 'A refused run is never overwritten; a new version opens beside it.'] : ['Your existing workspace opens with your current identity.', 'No sample activity is presented as your operational history.'],
    landingCtaLabel: `Go to ${selected.label} →`, landingContinue: () => navigate(selected.path),
    appTitle: 'Registry', appGroupLabel: 'Manage Estate', exitApp: () => navigate('/os?nav=admin&app=registry'),
    openShieldReport: () => notice('Shield report', 'This census view enforces admitted tenant access and validates result evidence. A system-wide Shield assurance report is not established by these checks.'),
    isRegistryGroup: true, isRegEstate: !history && !estate && !mixed,
    regTabsView: ['Data Connected', 'Compute Connected', 'LLMs & Trained Models'].map((label, i) => ({ key: label, label, color: i === 0 ? 'var(--ink)' : 'var(--ink3)', border: i === 0 ? 'var(--blue)' : 'transparent', onClick: () => i === 0 ? setParams({}) : notice(label, 'This census slice does not establish current compute telemetry or model admission. The Registry tab remains in the original experience; no demonstration figures are substituted.') })),
    isRegMeasure: true, isRegComputeTab: false, isRegLLM: false,
    openConnect: () => notice('Connect', 'This slice uses existing admitted source descriptors. Adding or changing a connector requires the existing connection and admission workflow; no connection has been created by this action.'),
    measureHeld: [tile('Data held', 'Not measured', 'No byte-volume measurement'), tile('Source references', String(data?.sources?.length ?? 0), 'Admitted groups; reachability not implied'), tile('Languages', 'Not measured', 'No language census attestation'), tile('Kinds of data', 'Not measured', 'No measured content distribution')],
    measureRead: [tile('Read', 'Not measured', 'Metadata census does not measure content coverage'), tile('Verified', 'Not measured', 'No source-content verification rate'), tile('Not yet read', 'Not measured', 'Uncounted volume is unknown'), tile('Tables recorded', count(latest?.table_count), 'Historical metadata inventory')],
    measureCare: ['Personal details', 'Restricted use', 'Read with problems', 'Possible duplicates'].map(label => tile(label)),
    censusRunning: running, censusBtnOpacity: data?.can_run ? running ? '.55' : '1' : '.45',
    censusBtnLabel: !data?.can_run ? 'Operator access required' : running ? 'Census running…' : 'Run census now',
    runCensus: () => data?.can_run ? openRun() : notice('Operator access required', 'Your admitted role may read census records but may not commission a run.'),
    censusNextLabel: 'On demand; no automatic schedule is active.',
    censusProgressLabel: 'Akki is checking the selected sources. Completion requires verified output and receipts.',
    censusPauseNeedsInput: status?.stage === 'blocked',
    openCensusPause: () => setParams({ view: 'history', record: status.census_run_id }),
    openMeasured: () => setParams({ view: 'history' }),
    efGapsHook: 'Row content, completeness, null rates, languages and rights were not assessed by this metadata census.',
    opportunitiesView: [{ key: 'unmeasured', title: 'Not established by this census', body: 'A metadata inventory alone does not establish a build-ready corpus or an admitted model opportunity.' }],
    openOppDrawerNew: () => notice('What your data can do', 'No source-derived opportunity assessment is attached to the retained census. This is not a conclusion that your estate has no opportunities.'),
    estateCensusCount: `${data?.records?.length || 0} attributed records`,
    estateConditionBar: unmeasuredBar('Condition not measured'), regQualBar: unmeasuredBar('Content coverage'), regLangBar: unmeasuredBar('Language mix'), regTypeBar: unmeasuredBar('Content distribution'), regRightsBar: unmeasuredBar('Use rights not established'),
    estateHeldRows: (data?.records || []).map(r => ({ key: r.record_id, label: `Census #${r.census_number || 'run'}`, w: '0%', color: 'var(--hair)', value: `${count(r.table_count)} tables`, pct: 'volume unmeasured' })),
    estateConditionSources: 'No measured quality or duplicate inventory is attached.', estateConditionRows: [{ label: 'Not assessed', value: 'Unknown', pct: 'No coverage claim', w: '0%', color: 'var(--hair)' }], measuredWays,
    estateFullOpen: estate, closeEstateFull: () => setParams({}), efNoSelection: !params.get('source'), efHasSelection: Boolean(params.get('source')),
    efCatsView: (data?.sources || []).map(s => ({ label: s.label, count: 'Admitted reference', blurb: s.scope, bg: params.get('source') === s.source_id ? 'var(--blue)' : '#fff', color: params.get('source') === s.source_id ? '#fff' : 'var(--ink)', tags: ['Metadata only'], tagBg: 'var(--surface2)', tagColor: 'var(--ink3)', origin: 'Reachability unverified', onClick: () => setParams({ view: 'sources', source: s.source_id }) })),
    efTopline: [{ l: 'Databases', v: count(latest?.database_count), n: 'Historical inventory' }, { l: 'Tables', v: count(latest?.table_count), n: 'Historical inventory' }, { l: 'Estimated rows', v: count(latest?.row_count_estimate), n: 'Not counted rows' }, { l: 'Volume', v: 'Unknown', n: 'Not measured' }, { l: 'Rights', v: 'Unknown', n: 'Not established' }],
    efGroupsView: (data?.sources || []).filter(s => s.source_id === params.get('source')).map(s => ({ name: s.label, count: '1 admitted reference', blurb: 'Admission and source reachability are different facts. This selection does not attest a fresh read.', rows: [{ source: s.label, size: 'Volume unmeasured', rightsLabel: 'Not established', rightsBg: 'var(--surface2)', rightsColor: 'var(--ink3)', meta: s.scope, dupFlagged: false, onOpen: () => setParams({ view: 'history' }) }] })),
    regFigures: [{ v: count(latest?.database_count), l: 'databases' }, { v: count(latest?.table_count), l: 'tables' }, { v: count(latest?.row_count_estimate), l: 'estimated rows' }, { v: 'Not measured', l: 'content volume' }], regQualReading: 'Content quality and verification rates are not available in this census.',
    mixOpen: mixed, closeMix: () => setParams({}), mixIsRights: true, mixRightsReading: 'The retained census does not establish use rights or a measured estate composition.', mixRightsRows: [{ label: 'No measured distribution', size: 'Not established', w: '0%', bar: 'var(--hair)', labelColor: 'var(--ink2)', valueColor: 'var(--ink3)' }], mixTabsView: [], mixRefs: [],
    ...historyModel(data, params, setParams),
  };
  ['Read', 'Care', 'Mix', 'How'].forEach(part => {
    const open = Boolean(disclosure[part]);
    Object.assign(scope, { [`census${part}Open`]: open, [`census${part}Label`]: open ? 'Hide' : 'Show', [`census${part}Chev`]: open ? 'rotate(180deg)' : 'rotate(0deg)', [`census${part}HeadMb`]: open ? '14px' : '0', [`toggleCensus${part}`]: () => toggle(part) });
  });
  scope.disclosureStates = Object.fromEntries(['Read', 'Care', 'Mix', 'How'].map(p => [`toggleCensus${p}`, Boolean(disclosure[p])]));
  return scope;
}

export function osCopy(data) {
  const latest = data?.latest;
  const reading = `Retained ${data?.tenant_id || 'tenant'} metadata, recorded ${stamp(latest?.finished_at)}. Row totals are estimates; quality, volume and release rights are not established.`;
  return {
    34: 'Akki OS', 5634: 'Every tenant-attributed census and operational run, including blocked or incomplete work. Open a record to inspect its results and evidence.',
    5639: context => context.c.num?.length > 6 ? `Run ${context.c.num}` : `Census #${context.c.num}`,
    5677: context => context.censusTranscriptMeta.num?.length > 6 ? `Run ${context.censusTranscriptMeta.num}` : `Census #${context.censusTranscriptMeta.num}`,
    5765: 'No recorded operator conversation is attached. This does not assert that the run needed nobody or completed successfully.',
    5798: reading, 6001: `Data connected — ${latest?.census_number ? `census #${latest.census_number}` : 'no verified census yet'}`,
    6002: reading, 6007: context => context.mc.value,
    6093: 'Retained measurements only; repeated censuses are not summed as additional holdings.',
    6111: 'Language distribution has not been measured.', 6142: 'Content-type distribution has not been measured.',
    6197: 'See the source and limits of each recorded figure. Estimates and missing measurements remain distinct.',
    6205: reading, 6215: 'Rights are not inferred', 6216: 'Rights require a separately recorded grant and purpose. No rights measurement or release authority is inferred from this census.',
    6235: `Next census: ${data?.can_run ? 'on demand' : 'requires an estate operator'}. No automatic schedule is active.`,
    6229: 'What the retained census recorded, and what it did not establish',
    6244: 'Execution blocked · inspect record',
    6257: latest ? `${count(latest.database_count)} databases and ${count(latest.table_count)} tables were recorded. ${count(latest.row_count_estimate)} rows are estimated from metadata, not counted.` : 'No tenant-attributed census evidence is available.',
    6273: 'Build-ready opportunities have not been established by this metadata-only reading.',
    4763: 'Recommended — inspect the retained census and the most recent run outcome. An unreachable source is not reported as measured.',
    4770: `Retained census · ${stamp(latest?.finished_at)}`, 4771: <>{count(latest?.table_count)} tables recorded.<br />Content volume not measured.</>, 4772: reading,
    4828: 'These figures describe the attributed census, not a measured breakdown of the selected source.',
    5817: 'What the record establishes', 5818: reading,
  };
}