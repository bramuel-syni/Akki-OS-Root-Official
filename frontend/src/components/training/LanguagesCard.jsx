import React, { useState } from 'react';
import { Languages, ShieldAlert } from 'lucide-react';
import { pct } from './useTrainingLab';

const VERDICT = { below_floor: 'Below the floor', at_risk: 'At risk', meets_floor: 'Meets the floor', not_measured: 'Not measured' };
const NAMES = { guz: 'Ekegusii', kam: 'Kikamba', kik: 'Gikuyu', kln: 'Kalenjin', luo: 'Dholuo', lwg: 'Luhya (Wanga)', swa: 'Kiswahili', eng: 'English', sheng: 'Sheng', bxk: 'Bukusu' };

const Reviews = ({ run }) => run?.reviews?.length > 0 && <div className="lab-reviews" data-testid="lab-language-reviews">
  <h4>Specialist advice · {run.specialist_reviews_complete} of {run.reviews.length} complete</h4>
  {run.reviews.map(r => <article key={r.role} className={`lab-review ${r.status}`} data-testid={`lab-review-${r.role}`}><h5>{r.role.replace(/_/g, ' ')}<small>{r.status.replace('_', ' ')}</small></h5>
    {r.review?.findings?.map((f, k) => <p key={k} className={`lab-finding ${f.severity}`}><span className="lab-severity">{f.severity}</span>{f.observation} <em>{f.recommendation}</em></p>)}
    {r.message && <p className="lab-footnote">{r.message}</p>}</article>)}
  <p className="lab-footnote">Advice is advisory and machine-checked for ungrounded numbers; it is not independent expert validation.</p>
</div>;

export const LanguagesCard = ({ lab, canOperate, isRms }) => {
  const [busy, setBusy] = useState(false), [error, setError] = useState(''); const report = lab.weak?.report; const plan = lab.weak?.plan; const latest = lab.plans[0];
  const ask = async () => { setBusy(true); setError(''); try { await lab.post('/languages/reinforcement', { floor: 0.9, model_reviews: true }); } catch (e) { setError(e.message); } finally { setBusy(false); } };
  return <section className="lab-card" data-testid="lab-languages-card">
    <header><h2><Languages size={18} />Languages the audio model handles poorly</h2><p>Read from the measured baseline certificate on the sealed held-out set. Accuracy is on judged windows; abstention is shown beside it.</p></header>
    {!report && <p className="media-note" data-testid="lab-languages-empty">Reading…</p>}
    {report?.status === 'no_measured_baseline' && <p className="lab-hold" data-testid="lab-languages-none">No measured audio baseline certificate is available.</p>}
    {report?.status === 'measured' && <>
      <p className="lab-lede" data-testid="lab-languages-summary">{report.below_floor.length ? <><strong>{report.below_floor.map(l => NAMES[l] || l).join(', ')}</strong> {report.below_floor.length === 1 ? 'sits' : 'sit'} below the {pct(report.floor)} floor.</> : 'Every measured language meets the floor.'}{report.at_risk.length ? ` ${report.at_risk.map(l => NAMES[l] || l).join(', ')} at risk.` : ''}</p>
      <table data-testid="lab-languages-table"><thead><tr><th>Language</th><th>Accuracy (95% interval)</th><th>Abstained</th><th>Judged windows</th><th>Training windows</th><th>Corpus hours</th><th>Verdict</th></tr></thead>
        <tbody>{Object.entries(report.languages).map(([code, v]) => <tr key={code} className={v.verdict} data-testid={`lab-language-${code}`}><td>{NAMES[code] || code} <small>{code}</small></td><td>{pct(v.interval, 1)}</td><td>{pct(v.abstention_rate, 1)}</td><td>{v.judged_windows}</td><td>{v.training_windows}</td><td>{v.corpus_hours}</td><td><span className={`lab-verdict ${v.verdict}`}>{VERDICT[v.verdict]}</span></td></tr>)}</tbody></table>
      <p className="lab-footnote">{report.corrective_runs_note}</p>
      {plan?.targets?.length > 0 && <section className="lab-plan" data-testid="lab-language-plan"><h4>Reinforcement plan · held for your approval</h4>
        {plan.targets.map(t => <article key={t.language} data-testid={`lab-plan-${t.language}`}><p><strong>{NAMES[t.language] || t.language}</strong> · {pct(t.accuracy, 1)} today · {t.training_windows_used} training windows used of about {t.windows_available_estimate} available{t.volume_ratio_to_strong_median ? ` · strong languages trained on ${t.volume_ratio_to_strong_median}× more` : ''}</p>
          <ul>{t.levers.map(l => <li key={l.lever}><strong>{l.lever.replace(/_/g, ' ')}</strong> — {l.change} <small>bounded by {l.bounded_by}</small></li>)}</ul></article>)}
        {plan.scaling_scenarios && !plan.scaling_scenarios.unavailable && <p className="lab-footnote" data-testid="lab-plan-scaling">Windows needed to reach the floor, from the cross-language scaling of this run: about {plan.scaling_scenarios.low}–{plan.scaling_scenarios.high} (middle {plan.scaling_scenarios.mid}). Prior sensitivity, not a forecast.</p>}
        <div className="lab-request" data-testid="lab-plan-request"><ShieldAlert size={16} /><div><strong>Training request · {plan.held_training_request.status.replace(/_/g, ' ')}</strong><p>{plan.held_training_request.phase} · targets {plan.held_training_request.target_languages.join(', ')} · recipe {Object.entries(plan.held_training_request.proposed_recipe_changes).map(([k, v]) => `${k.replace(/_/g, ' ')} ${v}`).join(', ')} · cap {plan.held_training_request.compute_cap_gpu_hours} GPU hours</p><p>{plan.held_training_request.acceptance}</p><p className="lab-footnote">{plan.reading}</p></div></div>
      </section>}
      {canOperate && isRms && <button className="estate-btn" onClick={ask} disabled={busy || ['queued', 'reviewing'].includes(latest?.status)} data-testid="lab-language-reviews-btn">{['queued', 'reviewing'].includes(latest?.status) ? 'Specialists reviewing…' : busy ? 'Sending…' : 'Ask the five specialists to review this plan'}</button>}
      {error && <p className="media-error" role="alert" data-testid="lab-language-error">{error}</p>}
      {latest && <p className="lab-status" data-testid="lab-language-run-status">{latest.status === 'complete' || latest.status === 'partial' ? `Reviewed ${new Date(latest.finished_at).toLocaleString()}${latest.status === 'partial' ? ' · some advice needs a second look' : ''}` : latest.hold_reason || latest.status}</p>}
      <Reviews run={latest} />
    </>}
  </section>;
};
