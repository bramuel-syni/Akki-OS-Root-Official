import React from 'react';
import { Archive, Download, FileAudio2, FileText, ListChecks, Pencil, Waves } from 'lucide-react';
import { bytes } from './useMediaLibrary';
import { CLASS_NAMES } from './acousticFormat';

const rights = { pending: 'Needs rights review', declared: 'Rights declared', withdrawn: 'Rights withdrawn' };
const content = { unknown: 'Not labelled', speech: 'Speech', music: 'Music', mixed: 'Speech and music' };
const reading = m => !m ? null : m.status === 'measured' ? `Reads as ${CLASS_NAMES[m.reads_as]?.toLowerCase()} · ${Math.round((m.confidence || 0) * 100)}%` : m.status === 'failed' ? 'Measurement failed' : m.status === 'measuring' ? 'Measuring sound…' : 'Queued for measurement';

export const MediaFiles = ({ files, selected, onToggle, onEdit, onDownload, onArchive, onSound, acoustics = {}, canOperate, busy }) => <div className="media-files" data-testid="work-media-file-list">
  <div className="media-column-head" aria-hidden="true"><span /><span>File</span><span>Content</span><span>Rights</span><span>Size</span><span /></div>
  {files.map(file => {
    const Icon = file.kind === 'audio' ? FileAudio2 : file.kind === 'labels' ? ListChecks : FileText;
    const active = !file.is_deleted && file.status === 'available'; const downloadable = active && file.rights_status !== 'withdrawn';
    const measured = acoustics[file.file_id]; const note = file.kind === 'audio' ? reading(measured) : null;
    return <article className={`media-file-row ${selected.includes(file.file_id) ? 'selected' : ''}`} data-testid={`work-media-file-${file.file_id}`} key={file.file_id}>
      <input type="checkbox" disabled={!downloadable || !canOperate} checked={selected.includes(file.file_id)} onChange={() => onToggle(file.file_id)} aria-label={`Select ${file.title}`} data-testid={`work-media-select-${file.file_id}`} />
      <div className="media-file-name"><Icon size={22} strokeWidth={1.4} /><div><strong data-testid={`work-media-title-${file.file_id}`}>{file.title}</strong><small data-testid={`work-media-kind-${file.file_id}`}>{file.extension.slice(1).toUpperCase()} · {file.kind === 'labels' ? 'Label manifest' : file.kind === 'audio' ? 'Audio' : 'Transcript'}{file.language ? ` · ${file.language}` : ''}</small></div></div>
      <span className="media-label-cell" data-testid={`work-media-label-${file.file_id}`}>{content[file.event_label]}<small>{file.label_status === 'human_reviewed' ? 'Human-reviewed label' : 'Unreviewed'}</small>{note && <small className={`media-reading ${measured.status}`} data-testid={`work-media-sound-chip-${file.file_id}`}>{note}</small>}</span>
      <span className={`media-rights ${file.is_deleted ? 'archived' : file.rights_status}`} data-testid={`work-media-rights-${file.file_id}`}>{file.is_deleted ? 'Archived' : file.status !== 'available' ? (file.status === 'upload_failed' ? 'Upload failed' : 'Awaiting upload') : rights[file.rights_status]}</span>
      <span className="media-file-size" data-testid={`work-media-size-${file.file_id}`}>{bytes(file.size_bytes)}</span>
      <div className="media-row-actions">
        {file.kind === 'audio' && <button className={`media-icon ${measured?.status === 'measured' ? 'measured' : ''}`} title="Sound profile" aria-label={`Sound profile of ${file.title}`} disabled={!downloadable} onClick={() => onSound(file)} data-testid={`work-media-sound-${file.file_id}`}><Waves size={17} /></button>}
        <button className="media-icon" title="Download file" aria-label={`Download ${file.title}`} disabled={!downloadable || busy === file.file_id} onClick={() => onDownload(file)} data-testid={`work-media-download-${file.file_id}`}><Download size={17} /></button>
        {canOperate && <><button className="media-icon" title="Edit details and rights" aria-label={`Edit ${file.title}`} disabled={!active} onClick={() => onEdit(file)} data-testid={`work-media-edit-${file.file_id}`}><Pencil size={16} /></button><button className="media-icon" title="Archive file" aria-label={`Archive ${file.title}`} disabled={file.is_deleted || file.status === 'uploading'} onClick={() => onArchive(file)} data-testid={`work-media-archive-${file.file_id}`}><Archive size={16} /></button></>}
      </div>
    </article>;
  })}
</div>;
