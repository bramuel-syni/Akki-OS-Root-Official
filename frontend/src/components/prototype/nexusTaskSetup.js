// Literal TASK_WIZ_STAGES from the owner reference_model_0.js, lines 3477–3482.
// These are form prompts/options, not generated answers or an execution provider.
export const taskSetupStages = [
  { ask: 'What is this task trying to achieve? One line is enough — I’ll sharpen it with you.', key: 'objective', options: null },
  { ask: 'Who owns it, and who contributes?', key: 'team', options: ['Just me', 'Me + Akki', 'Me + named team'] },
  { ask: 'When does it need to be done — and are there milestones on the way?', key: 'deadline', options: ['This week', 'This month', 'This quarter', 'Custom date'] },
  { ask: 'What counts as evidence it’s done well? I’ll track quality against this.', key: 'evidence', options: ['A committed document', 'A compiled pack', 'Sign-off from a named person', 'A metric threshold'] },
];