import React, { useRef, useState } from 'react';
import { Upload, RotateCcw, CheckCircle2, FileAudio2 } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { bytes } from './useMediaLibrary';

export const MediaUpload = ({ open, onClose, library }) => {
  const [chosen, setChosen] = useState([]), [confirmed, setConfirmed] = useState(false), [error, setError] = useState('');
  const input = useRef(null); const { config, queue, uploading, upload, retry } = library;
  const choose = incoming => {
    const files = Array.from(incoming); setError('');
    if (files.length > config.max_batch_files) { setError(`Choose up to ${config.max_batch_files} files per batch.`); return; }
    for (const file of files) {
      const ext = `.${file.name.split('.').pop().toLowerCase()}`;
      const max = ['.txt', '.vtt', '.srt', '.json', '.csv'].includes(ext) ? config.max_text_bytes : config.max_file_bytes;
      if (!config.extensions.includes(ext)) { setError(`${file.name}: unsupported format.`); return; }
      if (!file.size || file.size > max) { setError(`${file.name}: choose a non-empty file up to ${bytes(max)}.`); return; }
    }
    setChosen(files);
  };
  const begin = async () => { const batch = chosen; setChosen([]); await upload(batch); };
  return <Dialog open={open} onOpenChange={value => !value && onClose()}><DialogContent className="media-dialog" data-testid="work-media-upload-dialog">
    <DialogTitle data-testid="work-media-upload-title">Add files</DialogTitle>
    <DialogDescription data-testid="work-media-upload-limit">Audio up to {bytes(config?.max_file_bytes || 0)} · Text and labels up to {bytes(config?.max_text_bytes || 0)}</DialogDescription>
    <input ref={input} className="media-file-input" type="file" multiple accept={config?.extensions.join(',')} onChange={e => choose(e.target.files)} disabled={uploading} data-testid="work-media-file-input" aria-label="Choose files" />
    <button type="button" className="media-dropzone" disabled={uploading} data-testid="work-media-dropzone" onClick={() => input.current.click()} onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); if (!uploading) choose(e.dataTransfer.files); }}>
      <Upload size={26} strokeWidth={1.4} /><strong>Choose files or drop them here</strong><span>WAV, MP3, FLAC, OGG, M4A · TXT, VTT, SRT · JSON, CSV</span>
    </button>
    {chosen.length > 0 && <ul className="media-upload-list" data-testid="work-media-chosen-files">{chosen.map((file, i) => <li key={i} data-testid={`work-media-chosen-${i}`}><FileAudio2 size={16} /><span>{file.name}</span><small>{bytes(file.size)}</small></li>)}</ul>}
    <label className="media-check"><input type="checkbox" checked={confirmed} onChange={e => setConfirmed(e.target.checked)} data-testid="work-media-storage-consent" />I have permission to store these files in this private library.</label>
    <p className="media-note" data-testid="work-media-upload-retention">Stored files can be archived, but permanent deletion is unavailable. Uploading does not authorise training.</p>
    {error && <p role="alert" className="media-error" data-testid="work-media-upload-error">{error}</p>}
    {queue.length > 0 && <ul className="media-upload-list" aria-live="polite" data-testid="work-media-upload-queue">{queue.map((item, index) => <li key={item.key} className="media-progress-row" data-testid={`work-media-upload-item-${index}`}><div><span>{item.name}</span><small data-testid={`work-media-upload-state-${index}`}>{item.status === 'Stored' && <CheckCircle2 size={13} />} {item.status}</small></div><progress max="100" value={item.progress} data-testid={`work-media-upload-progress-${index}`} aria-label={`${item.name} upload`} />{item.error && <small role="alert" className="media-error" data-testid={`work-media-upload-failure-${index}`}>{item.error}</small>}</li>)}</ul>}
    <div className="media-actions">{queue.some(q => q.status === 'Failed') && <button className="estate-btn" disabled={uploading} onClick={retry} data-testid="work-media-retry-btn"><RotateCcw size={15} />Retry failed</button>}<button className="estate-btn primary" disabled={!chosen.length || !confirmed || uploading} onClick={begin} data-testid="work-media-start-upload"><Upload size={15} />{uploading ? 'Uploading…' : `Upload${chosen.length ? ` ${chosen.length} file${chosen.length === 1 ? '' : 's'}` : ''}`}</button></div>
  </DialogContent></Dialog>;
};