import { count } from './useEstateReport';

export const hours = value => value == null ? '—' : `${count(Math.round(value * 10) / 10)} h`;
export const interval = e => e?.est == null ? '—' : e.lo != null && e.hi != null && e.hi !== e.lo ? `${hours(e.est)} (${hours(e.lo)}–${hours(e.hi)})` : hours(e.est);
export const langs = (map, n = 4) => Object.entries(map || {}).filter(([, e]) => e?.est != null).sort((a, b) => b[1].est - a[1].est).slice(0, n).map(([code, e]) => `${code} ${hours(e.est)}`).join(' · ') || '—';
export const usd = v => v == null ? '—' : `≈ $${count(Math.round(v * 100) / 100)}`;
