import { unknownStats } from './nexusShared';

export function supportModel({ section, state, setState, unavailable }) {
  const tab = state.boardTab || 'signals';
  const toggle = key => () => setState(s => ({ ...s, [key]: !s[key] }));
  return {
    isBoard360: section === 'board', isMonPerformance: section === 'goals',
    boardTabsView: [['signals', 'Signals'], ['performance', 'Performance'], ['docs', 'Documents'], ['questions', 'Questions']].map(([key, label]) => ({
      key, label, onClick: () => setState(s => ({ ...s, boardTab: key })), color: key === tab ? 'var(--ink)' : 'var(--ink3)', border: key === tab ? 'var(--blue)' : 'transparent' })),
    boardIsSignals: tab === 'signals', boardIsPerformance: tab === 'performance', boardIsDocs: tab === 'docs', boardIsQuestions: tab === 'questions',
    boardSignalsView: [], boardPerfView: [], boardDocsView: [], boardQuestionsView: [], boardSignalCount: 'Signals not yet available', boardDocCount: 'Documents not yet available',
    boardSevOptions: ['All', 'High', 'Medium', 'Low'], boardSevValue: state.severity || 'All', boardSevChange: e => setState(s => ({ ...s, severity: e.target.value })),
    boardDocListOpen: true, boardDocFiltersView: ['All', 'Board pack', 'Minutes', 'Report'].map(label => ({ label, border: 'var(--line)',
      bg: state.boardFilter === label ? 'var(--blue)' : '#fff', color: state.boardFilter === label ? 'var(--paper)' : 'var(--ink3)',
      onClick: () => setState(s => ({ ...s, boardFilter: label })) })),
    boardTipsOpen: Boolean(state.boardTips), boardTipsLabel: state.boardTips ? 'Hide' : 'Show', toggleBoardTips: toggle('boardTips'),
    boardChatInput: state.boardInput || '', onBoardChatInput: e => setState(s => ({ ...s, boardInput: e.target.value })),
    onBoardChatKeyDown: e => { if (e.key === 'Enter') { e.preventDefault(); unavailable('Board answer', 'The board evidence and answering service are not connected. Your question has not been sent.'); } },
    sendBoardChat: () => unavailable('Board answer', 'The board evidence and answering service are not connected. Your question has not been sent.'),
    boardChatLogView: [], boardChatBusy: false, boardPromptsView: [], boardChatSteps: [], qaThreadView: [], qaTeamView: [], qaEmpty: false,
    qaCountLabel: 'Questions not yet available', qaDraft: state.question || '', qaDraftChange: e => setState(s => ({ ...s, question: e.target.value })),
    qaSubmit: () => unavailable('Board question', 'An admitted board and its membership are required before sharing a question.'),
    perfGroups: [], perfTasksEmpty: false, perfNoMatches: false,
    perfSummaryChips: unknownStats(['Company goals', 'On course', 'Needs attention']).map(s => ({ label: `${s.label} ${s.value}`, bg: 'var(--surface2)', color: 'var(--ink3)' })),
    perfOwnerOptions: [{ value: 'all', label: 'All owners' }], perfOwnerValue: state.goalOwner || 'all',
    perfOwnerSelect: e => setState(s => ({ ...s, goalOwner: e.target.value })),
    perfStatusOptions: [{ value: 'all', label: 'All statuses' }, { value: 'progress', label: 'In progress' }, { value: 'risk', label: 'At risk' }],
    perfStatusValue: state.goalStatus || 'all', perfStatusSelect: e => setState(s => ({ ...s, goalStatus: e.target.value })),
    perfSortOptions: ['Newest', 'Due date', 'Owner'], perfSortValue: state.goalSort || 'Newest',
    perfSortChange: e => setState(s => ({ ...s, goalSort: e.target.value })),
  };
}