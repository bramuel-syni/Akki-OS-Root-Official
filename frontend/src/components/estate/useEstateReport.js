import { useCallback, useEffect, useState } from 'react';
import { censusRequest } from '../census/useCensusWorkspace';

// One report read per visit (the report is banked beside the job; nothing is re-measured by reading it).
export function useEstateReport(signedIn) {
  const [state, setState] = useState({ report: null, running: null, loading: false, error: null, composing: false, refusal: null });
  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const result = await censusRequest('/estate-intelligence/report');
      setState(s => ({ ...s, report: result.report, running: result.running, loading: false }));
    } catch (error) {
      setState(s => ({ ...s, loading: false, error: error.message || 'The report could not be read.' }));
    }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const compose = useCallback(async () => {
    if (!state.report) return;
    setState(s => ({ ...s, composing: true, refusal: null, error: null }));
    try {
      const result = await censusRequest(`/estate-intelligence/jobs/${state.report.job_id}/dossier`, { method: 'POST', body: JSON.stringify({}) });
      setState(s => ({ ...s, composing: false, report: result.report || s.report, refusal: result.refused ? result.refusal_reason : null }));
    } catch (error) {
      setState(s => ({ ...s, composing: false, error: error.message || 'The dossier was not composed.' }));
    }
  }, [state.report]);
  return { ...state, reload: load, compose };
}

export const pct = (ratio, digits = 1) => ratio == null ? 'Not measured' : `${(ratio * 100).toFixed(digits)}%`;
export const pctValue = value => value == null ? 'Not measured' : `${value}%`;
export const count = value => typeof value === 'number' ? value.toLocaleString('en-GB', { maximumFractionDigits: 2 }) : 'Not measured';
export const bytes = value => {
  if (typeof value !== 'number') return 'Not measured';
  const index = value ? Math.min(4, Math.floor(Math.log(value) / Math.log(1024))) : 0;
  return `${count(value / (1024 ** index))} ${['B', 'KiB', 'MiB', 'GiB', 'TiB'][index]}`;
};
export const stamp = iso => iso ? new Date(iso).toLocaleString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC' : 'not recorded';
export const signed = (value, format = count) => value == null ? '—' : `${value > 0 ? '+' : value < 0 ? '−' : ''}${format(Math.abs(value))}`;
