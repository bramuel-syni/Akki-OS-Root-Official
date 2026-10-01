import React from 'react';

// Presentation only: identifiers remain unchanged in requests, links and downloaded evidence.
export const readableText = (value = '') => String(value)
  .replace(/\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b/gi, 'reference')
  .replace(/\b(?:eij|cr|com|bld|req|drf|lab|lcj|m9j|rev|ses|turn|org)-[a-f0-9]{10,}(?:-pruned)?\b/gi, 'record')
  .replace(/\b[a-f0-9]{24,64}\b/gi, 'reference');

export const documentTitle = document => {
  const title = readableText(document.title || 'Untitled document');
  const clean = title.replace(/\s*[—–-]?\s*record\s*$/i, '').trim() || 'Document';
  const date = new Date(document.created_at);
  return title !== document.title && !Number.isNaN(date.getTime()) ? `${clean} · ${date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })}` : clean;
};

export const PresentationDetails = ({ id, title, children, open = false }) => <details className="presentation-details" data-testid={`${id}-details`} open={open || undefined}>
  <summary data-testid={`${id}-toggle`}>{title}</summary>
  <div className="presentation-details-body">{children}</div>
</details>;