import React, { useState } from 'react';
import { Save } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { mediaRequest } from './useMediaLibrary';

export const MediaMetadata = ({ file, onClose, onSaved }) => {
  const [form, setForm] = useState(Object.fromEntries(['revision', 'title', 'language', 'event_label', 'label_status', 'rights_status', 'rights_basis', 'rights_reference', 'training_permission_confirmed'].map(key => [key, file[key]])));
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  const set = (key, value) => setForm(old => ({ ...old, [key]: value }));
  const submit = async e => {
    e.preventDefault(); setBusy(true); setError('');
    try { await mediaRequest(`/files/${file.file_id}`, { method: 'PATCH', body: JSON.stringify(form) }); await onSaved(); onClose(); }
    catch (failure) { setError(failure.message); } finally { setBusy(false); }
  };
  return <Dialog open onOpenChange={value => !value && !busy && onClose()}><DialogContent className="media-dialog" data-testid="work-media-metadata-dialog">
    <DialogTitle data-testid="work-media-metadata-title">File details</DialogTitle><DialogDescription data-testid="work-media-original-name">{file.filename}</DialogDescription>
    <form onSubmit={submit} className="media-form" data-testid="work-media-metadata-form">
      <label>Name<input required maxLength={140} value={form.title} onChange={e => set('title', e.target.value)} data-testid="work-media-meta-title" /></label>
      <div className="media-form-grid"><label>Language<input maxLength={80} value={form.language} onChange={e => set('language', e.target.value)} placeholder="Not recorded" data-testid="work-media-meta-language" /></label>
        <label>Content label<select value={form.event_label} onChange={e => setForm(old => ({ ...old, event_label: e.target.value, label_status: e.target.value === 'unknown' ? 'unreviewed' : old.label_status }))} data-testid="work-media-meta-label"><option value="unknown">Not labelled</option><option value="speech">Speech</option><option value="music">Music</option><option value="mixed">Speech and music</option></select></label></div>
      <label className="media-check"><input type="checkbox" disabled={form.event_label === 'unknown'} checked={form.label_status === 'human_reviewed'} onChange={e => set('label_status', e.target.checked ? 'human_reviewed' : 'unreviewed')} data-testid="work-media-meta-label-reviewed" />This content label has been reviewed by a person.</label>
      <fieldset><legend>Training rights</legend><label>Status<select value={form.rights_status} onChange={e => setForm(old => ({ ...old, rights_status: e.target.value, training_permission_confirmed: false }))} data-testid="work-media-meta-rights"><option value="pending">Needs review</option><option value="declared">Rights declared</option><option value="withdrawn">Rights withdrawn</option></select></label>
        {form.rights_status === 'declared' && <><label>Basis<select required value={form.rights_basis} onChange={e => set('rights_basis', e.target.value)} data-testid="work-media-meta-basis"><option value="">Choose a basis</option><option value="own_recording">Own recording and applicable rights</option><option value="permission">Explicit permission</option><option value="licensed">Training-compatible licence</option><option value="public_domain">Public domain</option></select></label>
          <label>Evidence reference<input required maxLength={500} value={form.rights_reference} onChange={e => set('rights_reference', e.target.value)} placeholder="Agreement, licence or rights record" data-testid="work-media-meta-reference" /></label>
          <label className="media-check"><input type="checkbox" required checked={form.training_permission_confirmed} onChange={e => set('training_permission_confirmed', e.target.checked)} data-testid="work-media-meta-training-consent" />The referenced permission covers model training.</label>
          <p className="media-note" data-testid="work-media-rights-declaration-note">Your declaration is recorded; it is not independent rights verification.</p></>}
        {form.rights_status === 'withdrawn' && <p className="media-error" data-testid="work-media-withdrawal-notice">Downloads and new assessments will be blocked. Stored bytes are retained.</p>}
      </fieldset>
      {error && <p className="media-error" role="alert" data-testid="work-media-metadata-error">{error}</p>}
      <button type="submit" disabled={busy} className="estate-btn primary" data-testid="work-media-meta-save"><Save size={15} />{busy ? 'Saving…' : 'Save details'}</button>
    </form>
  </DialogContent></Dialog>;
};