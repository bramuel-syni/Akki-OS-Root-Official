import React from 'react';
import { TurnWorking } from './TurnWorking';

const LOSS = '\n\nContext: ';
const label = { warm: 'Warm · answered from qualified memory', fresh: 'Fresh · gap acknowledged', refused: 'Refused' };

export function TurnCard({ turn }) {
  const kind = turn.refused ? 'refused' : turn.decision;
  const [text, loss] = (turn.answer || '').split(LOSS);
  const cites = turn.evidence?.cited_refs || [];
  return <article className="workchat-turn" data-testid={`workchat-turn-${turn.turn_id}`}>
    <div className="workchat-who">You{turn.compacted && <span className="workchat-badge neutral" data-testid={`workchat-compacted-${turn.turn_id}`}>compacted</span>}</div>
    <div className="workchat-q" data-testid={`workchat-question-${turn.turn_id}`}>{turn.question}</div>
    <div className="workchat-who">Akki <span className={`workchat-badge ${kind}`} data-testid={`workchat-decision-${turn.turn_id}`}>{label[kind] || kind}</span></div>
    <div className={`workchat-a ${kind}`}>
      {turn.refused
        ? <p className="workchat-reason" data-testid={`workchat-refusal-${turn.turn_id}`}>{turn.refusal_reason}</p>
        : <p className="workchat-a-text" data-testid={`workchat-answer-${turn.turn_id}`}>{text}</p>}
      {loss && <p className="workchat-loss" data-testid={`workchat-loss-${turn.turn_id}`}>Context: {loss}</p>}
      {cites.length > 0 && <div className="workchat-cites" data-testid={`workchat-cites-${turn.turn_id}`}>
        {cites.map(ref => <span key={ref} className="workchat-cite" title={ref}>{ref.split('/').slice(-2).join('/')}</span>)}
      </div>}
      <TurnWorking turn={turn} />
    </div>
  </article>;
}
