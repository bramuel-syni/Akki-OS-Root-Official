import React from 'react';
import { Download } from 'lucide-react';
import { bytes } from './useEstateReport';
import { PresentationDetails } from '../shared/PresentationDetails';
import { cleanupGuidance, reviewOrder } from './cleanupRecommendations';

const money = (value, currency) => `${currency || ''} ${value.toLocaleString('en-GB', { maximumFractionDigits: 2 })}`.trim();

function Strategy({ s }) {
  const guide = cleanupGuidance[s.key] || { title: s.title, next: s.action, destination: 'No destination recorded.' };
  return <li className="estate-strategy" data-testid={`estate-strategy-${s.key}`}>
    <div className="estate-strategy-row">
      <div className="estate-strategy-title"><h3>{guide.title}</h3><p data-testid={`estate-strategy-next-${s.key}`}>{guide.next}</p></div>
      <div className="estate-strategy-bytes" data-testid={`estate-strategy-impact-${s.key}`}><b>{s.bytes > 0 ? bytes(s.bytes) : 'Quality review'}</b><small>{s.bytes > 0 ? 'Potential scope · estimate' : 'No storage saving measured'}</small></div>
    </div>
    <PresentationDetails id={`estate-strategy-${s.key}`} title="Locations, destination & evidence">
      <p className="estate-destination" data-testid={`estate-strategy-destination-${s.key}`}><b>Destination</b> {guide.destination}</p>
      <h4>Recorded locations</h4>
      {s.evidence?.length ? <ul data-testid={`estate-strategy-locations-${s.key}`}>{s.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul> : <p>No qualifying locations were recorded.</p>}
      <p className="estate-note" data-testid={`estate-strategy-risk-${s.key}`}>{s.risk}</p>
      {s.monthly_saving != null && <p className="estate-note" data-testid={`estate-strategy-saving-${s.key}`}>{s.saving_basis?.startsWith('upper bound') ? 'Storage-cost ceiling' : 'Indicative storage saving'}: {money(s.monthly_saving, s.currency)}/month at reference prices. {s.saving_basis?.startsWith('upper bound') ? 'Not a net saving: archive and retrieval charges are not priced.' : 'Not an invoice or guaranteed saving.'}</p>}
    </PresentationDetails>
  </li>;
}

export function EstateStrategies({ report }) {
  const items = reviewOrder(report.cost_strategies.items);
  const download = () => {
    const rows = [['Recommendation', 'Next review', 'Destination status', 'Recorded location / evidence', 'Estimated scope bytes', 'Measured at']];
    items.forEach(s => (s.evidence?.length ? s.evidence : ['No location recorded']).forEach(evidence => {
      const g = cleanupGuidance[s.key] || {};
      rows.push([g.title || s.title, g.next || s.action, g.destination || 'No destination recorded', evidence, s.bytes ?? '', report.measured_at]);
    }));
    const csv = rows.map(row => row.map(value => `"${String(value ?? '').replace(/^[=+@-]/, "'$&").replaceAll('"', '""')}"`).join(',')).join('\r\n');
    const url = URL.createObjectURL(new Blob(['\uFEFF', csv], { type: 'text/csv;charset=utf-8' }));
    const link = Object.assign(document.createElement('a'), { href: url, download: 'Estate-cleanup-review.csv' });
    document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return <section className="estate-section" data-testid="estate-strategies">
    <header className="estate-head"><div><h2>Recommended next steps</h2><p data-testid="estate-strategies-boundary">Review only. No files have been moved or deleted. Estimates overlap; do not add them together.</p></div>
      <button className="estate-btn" onClick={download} data-testid="estate-download-cleanup"><Download size={15} />Download cleanup review</button></header>
    {!items.length && <p data-testid="estate-strategies-empty">No cleanup recommendations recorded for this census.</p>}
    <ul className="estate-strategies">{items.slice(0, 3).map(s => <Strategy key={s.key} s={s} />)}</ul>
    {items.length > 3 && <PresentationDetails id="estate-more-recommendations" title={`${items.length - 3} more recommendations`}><ul className="estate-strategies">{items.slice(3).map(s => <Strategy key={s.key} s={s} />)}</ul></PresentationDetails>}
  </section>;
}