import React, { useState } from 'react';

export function Composer({ busy, disabled, onAsk, hasSession }) {
  const [value, setValue] = useState('');
  const submit = () => {
    const question = value.trim();
    if (!question || busy || disabled) return;
    setValue('');
    onAsk(question);
  };
  return <div className="workchat-composer" data-testid="workchat-composer">
    <textarea className="workchat-input" data-testid="workchat-input" value={value} rows={2} maxLength={4000} disabled={disabled}
      placeholder={hasSession ? 'Ask a follow-up — the objective stays frozen, memory stays warm' : 'Ask a question — it opens a conversation and freezes its objective'}
      onChange={e => setValue(e.target.value)}
      onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); } }} />
    <button className="workchat-btn primary" data-testid="workchat-ask-submit" onClick={submit} disabled={busy || disabled || !value.trim()}>
      {busy ? 'Asking…' : 'Ask'}
    </button>
  </div>;
}
