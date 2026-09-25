import React, { useState } from 'react';
import { LogIn, LockKeyhole } from 'lucide-react';
import { login } from '@/lib/apiClient';

export function CensusAccess({ error, loading, retry }) {
  const [busy, setBusy] = useState(false);
  const [failure, setFailure] = useState('');
  if (loading && !error) return <div data-testid="census-loading" role="status" className="census-empty">Reading census records…</div>;
  if (error?.status !== 401) return <section className="census-empty" data-testid="census-access-error" role="alert">
    <LockKeyhole size={24} /><h2>Census access unavailable</h2><p>{error?.message}</p>
    <button data-testid="census-access-retry" className="census-button" onClick={retry}>Try again</button>
  </section>;
  async function submit(event) {
    event.preventDefault(); setBusy(true); setFailure('');
    const form = new FormData(event.currentTarget);
    try {
      await login(form.get('email'), form.get('password'));
      window.dispatchEvent(new Event('akki-session-changed'));
    } catch (e) { setFailure(e.message); }
    finally { setBusy(false); }
  }
  return <section className="census-signin" data-testid="census-signin">
    <LockKeyhole size={24} strokeWidth={1.5} />
    <h2>Your estate, within its boundaries.</h2>
    <p data-testid="census-signin-message">Sign in to view your admitted tenant’s census and registry records.</p>
    <form onSubmit={submit} data-testid="census-signin-form">
      <label htmlFor="census-email">Email</label>
      <input id="census-email" data-testid="census-email" name="email" type="email" autoComplete="username" required />
      <label htmlFor="census-password">Password</label>
      <input id="census-password" data-testid="census-password" name="password" type="password" autoComplete="current-password" required />
      {failure && <p role="alert" data-testid="census-signin-error" className="census-error">{failure}</p>}
      <button data-testid="census-signin-submit" className="census-button primary" disabled={busy}><LogIn size={16} />{busy ? 'Signing in…' : 'Sign in'}</button>
    </form>
  </section>;
}