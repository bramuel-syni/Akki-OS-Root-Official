import React from 'react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { bytes } from './useMediaLibrary';

export const MediaAssessment = ({ run, onClose }) => {
  const report = run.dataset_assessment;
  return <Dialog open onOpenChange={value => !value && onClose()}><DialogContent className="media-dialog" data-testid="work-media-assessment-dialog">
    <DialogTitle data-testid="work-media-assessment-title">Dataset readiness</DialogTitle>
    <DialogDescription data-testid="work-media-assessment-summary">{report.file_count} files · {bytes(report.total_bytes)} · Metadata review</DialogDescription>
    <p className="media-assessment-hold" data-testid="work-media-assessment-hold">Training has not started.</p>
    {run.current_validity?.stale && <p className="media-error" role="alert" data-testid="work-media-assessment-stale">File details or access changed after this review. Select the current files for a new assessment.</p>}
    <ul className="media-review-files">{report.files.map(file => <li key={file.file_id} data-testid={`work-media-reviewed-${file.file_id}`}><strong>{file.title}</strong>{file.issues.length ? <ul>{file.issues.map((issue, i) => <li key={i} data-testid={`work-media-issue-${file.file_id}-${i}`}>{issue}</li>)}</ul> : <p data-testid={`work-media-metadata-complete-${file.file_id}`}>Required declarations recorded. Independent verification remains pending.</p>}</li>)}</ul>
    <h3 className="media-subtitle" data-testid="work-media-next-checks-title">Before training</h3><ul className="media-review-blockers">{report.blockers.map((item, i) => <li key={item} data-testid={`work-media-assessment-blocker-${i}`}>{item}</li>)}</ul>
    <p className="media-note" data-testid="work-media-assessment-scope">Audio duration, recording quality and music content have not been measured by this review.</p>
  </DialogContent></Dialog>;
};