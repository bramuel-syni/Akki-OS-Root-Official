export const UNKNOWN = '—';
export const unknownStats = labels => labels.map((label, index) => ({ key: String(index), label, value: UNKNOWN, note: 'Awaiting records',
  subline: 'Awaiting records', color: 'var(--ink3)', tone: 'var(--ink3)', radius: index === 0 ? '10px 0 0 10px' : '0' }));

export function disclosure(state, key, set, initial = false, prefix = key) {
  const open = state[key] ?? initial;
  return { [prefix + 'Open']: open, [prefix + 'Label']: open ? 'Hide' : 'Show',
    [prefix + 'Chev']: open ? 'rotate(180deg)' : 'rotate(0deg)', [prefix + 'HeadMb']: open ? '14px' : '0',
    ['toggle' + prefix[0].toUpperCase() + prefix.slice(1)]: () => set(s => ({ ...s, [key]: !(s[key] ?? initial) })) };
}

export function ownerDrawer(value, close) {
  return { dwOpen: Boolean(value), closeWalk: close, dwXPlain: true, dwShowSub: true, dwShowCards: true,
    dwTitle: value?.title || '', dwSub: value?.subtitle || '', dwHasChip: true, dwChipLabel: value?.code || 'Recorded',
    dwChipBg: 'var(--surface2)', dwChipColor: 'var(--ink3)', dwHideTransitions: true,
    dwCards: value ? [{ q: 'What the record says', a: value.body, hasArrow: false, hasControls: false },
      ...(value.next ? [{ q: 'Next action', a: value.next, hasArrow: false, hasControls: false }] : [])] : [],
    dwHasActions: Boolean(value?.actions?.length), dwActions: value?.actions || [],
  };
}