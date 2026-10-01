import React, { useEffect, useState } from 'react';
import { Waves } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { AcousticProfile } from './AcousticProfile';
import { formatDuration } from './acousticFormat';

export const MediaAcoustics = ({ file, acoustics, canOperate, onClose }) => {
  const summary = acoustics.byFile[file.file_id];
  const [detail, setDetail] = useState(null), [error, setError] = useState(''), [busy, setBusy] = useState(false);
  const status = summary?.status || 'unmeasured';
  useEffect(() => {
    let active = true;
    if (status === 'measured') acoustics.profile(file.file_id).then(d => { if (active) setDetail(d.measurement); }).catch(e => { if (active) setError(e.message); });
    else setDetail(null);
    return () => { active = false; };
  }, [status, summary?.measured_at, file.file_id]);
  const measure = async () => { setBusy(true); setError(''); try { await acoustics.request(file.file_id); } catch (e) { setError(e.message); } finally { setBusy(false); } };
  const duration = detail?.profile?.observables?.wave?.duration_seconds;
  const human = file.label_status === 'human_reviewed' && file.event_label !== 'unknown' ? file.event_label : null;
  return <Dialog open onOpenChange={value => !value && onClose()}><DialogContent className="media-dialog wide" data-testid="work-media-sound-dialog">
    <DialogTitle data-testid="work-media-sound-title">{file.title}</DialogTitle>
    <DialogDescription data-testid="work-media-sound-subtitle">{status === 'measured' && detail ? `${formatDuration(duration)} · ${detail.profile.observables.wave.source_sample_rate_hz ? `${(detail.profile.observables.wave.source_sample_rate_hz / 1000).toFixed(1)} kHz` : ''} ${detail.profile.observables.wave.source_channels === 2 ? 'stereo' : detail.profile.observables.wave.source_channels === 1 ? 'mono' : ''} · measured ${new Date(detail.measured_at).toLocaleString()}` : 'Sound profile'}</DialogDescription>
    {error && <p className="media-error" role="alert" data-testid="work-media-sound-error">{error}</p>}
    {status === 'unmeasured' && <div className="sound-empty" data-testid="work-media-sound-unmeasured"><p>This recording has not been measured.</p>{canOperate && <button className="estate-btn primary" onClick={measure} disabled={busy} data-testid="work-media-sound-measure"><Waves size={16} />{busy ? 'Queuing…' : 'Measure sound'}</button>}</div>}
    {(status === 'queued' || status === 'measuring') && <p className="sound-progress" role="status" data-testid="work-media-sound-progress">{status === 'queued' ? 'Waiting in the measurement queue.' : 'Measuring now.'} A few seconds per minute of audio.</p>}
    {status === 'failed' && <div className="sound-empty" data-testid="work-media-sound-failed"><p className="media-error">{summary.error || 'The measurement failed.'}</p>{canOperate && <button className="estate-btn" onClick={measure} disabled={busy} data-testid="work-media-sound-retry">Try again</button>}</div>}
    {status === 'measured' && !detail && !error && <p className="media-note" data-testid="work-media-sound-loading">Reading the profile…</p>}
    {status === 'measured' && detail?.profile && <AcousticProfile profile={detail.profile} register={acoustics.register} human={human} />}
  </DialogContent></Dialog>;
};
